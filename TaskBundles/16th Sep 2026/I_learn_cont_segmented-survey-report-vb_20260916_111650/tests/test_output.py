"""Outcome graders for the Studio Signals task.

One module, every section and both declared slots. Black-box: HTTP against the
running app, the rendered page through Playwright, PostgreSQL through the shared
backend adapter and MinIO through the shared storage adapter. Expected figures come
from the reference resolver in conftest, computed from the pinned seed.
"""

from __future__ import annotations

import datetime
import os
import re
import urllib.parse

import httpx

from conftest import (
    ANNOUNCED_CASES,
    CAVEAT_SHORT,
    CELLS,
    CHAPTERS,
    CHAPTER_SLUGS,
    ENVS,
    EXPS,
    EXPORT_KEY_RE,
    PASSWORD,
    Q,
    R,
    READER_EMAIL,
    SIZES,
    TIMEOUT,
    UNKNOWN_SEGMENT,
    WAVES,
    base_url,
    body,
    by_id,
    cell_count,
    cell_text,
    chapter,
    client,
    contrast,
    cookie_session,
    describe,
    export_text,
    goto,
    half_up,
    html_text,
    links_to,
    missing,
    ok,
    opt_index,
    pct,
    refused,
    resolved,
    respondents,
    settle,
    sign_up,
    supported,
    token_for,
    unique,
    val,
)

PUBLIC_PAGES = ("/", "/chapters/tools", "/chapters/craft", "/chapters/teams", "/about", "/terms",
                "/cases/harbour-type", "/sign-in", "/sign-up")

_CURRENT_RAIL = """() => Array.from(document.querySelectorAll('nav a[href*="#"][aria-current]'))
  .filter(a => a.getAttribute('aria-current') !== 'false' && a.getClientRects().length)
  .map(a => a.textContent.trim())"""

_LIVE_TEXT = """() => Array.from(document.querySelectorAll('[aria-live]:not([aria-live="off"]), [role="status"], [role="alert"]'))
  .map(el => el.textContent.trim()).filter(Boolean)"""

_TEXT_COLOURS = """(selector) => {
  const parse = s => { const n = (s.match(/[\\d.]+/g) || []).map(Number);
    return [n[0] || 0, n[1] || 0, n[2] || 0, n.length > 3 ? n[3] : 1]; };
  const ground = el => { let node = el;
    while (node) { const c = parse(getComputedStyle(node).backgroundColor);
      if (c[3] > 0) return c.slice(0, 3); node = node.parentElement; }
    return [255, 255, 255]; };
  return Array.from(document.querySelectorAll(selector))
    .filter(el => el.textContent.trim().length > 1 && el.checkVisibility({checkVisibilityCSS: true})
      && !el.closest('[aria-hidden="true"]') && !el.closest('nav'))
    .map(el => [parse(getComputedStyle(el).color), ground(el)]);
}"""

_FONT_SIZES = """() => {
  const shown = el => el.checkVisibility({checkVisibilityCSS: true}) && el.textContent.trim().length > 1;
  const size = el => parseFloat(getComputedStyle(el).fontSize);
  const main = document.querySelector('main') || document.body;
  return {
    prose: Array.from(main.querySelectorAll('p')).filter(el => shown(el) && el.textContent.trim().split(/\\s+/).length > 12).map(size),
    figures: Array.from(main.querySelectorAll('td')).filter(el => shown(el) && /\\d/.test(el.textContent)).map(size),
  };
}"""


def title_of(markup: str) -> str:
    found = re.search(r"<title[^>]*>(.*?)</title>", markup, re.I | re.S)
    return html_text(found.group(1)) if found else ""


def _over(front: list, back: list) -> tuple:
    alpha = front[3] if len(front) > 3 else 1
    return tuple(round(f * alpha + b * (1 - alpha)) for f, b in zip(front[:3], back[:3]))


def _citation(session: httpx.Client, slug: str, fid: str, seg: dict | None = None) -> dict:
    params = {k: v for k, v in (seg or {}).items() if v}
    return ok(session.get(f"/api/chapters/{slug}/findings/{fid}/citation", params=params), f"citation {slug} {fid}")


def _progress_raw(session: httpx.Client, chapter_slug: str, finding: str) -> httpx.Response:
    return session.put(f"/api/progress/{chapter_slug}", json={"finding": finding})


def _progress(session: httpx.Client, chapter_slug: str, finding: str) -> dict:
    return ok(_progress_raw(session, chapter_slug, finding), f"progress {chapter_slug} {finding}")


def _chapter_raw(session: httpx.Client, slug: str, params: dict) -> httpx.Response:
    return session.get(f"/api/chapters/{slug}", params=params)


def _export_tables(markdown: str) -> dict:
    """Map each exported finding heading to the cell lists of its table, empty when withheld."""
    tables, current = {}, None
    for line in markdown.splitlines():
        if line.startswith("### "):
            current = line[4:].strip()
            tables[current] = []
        elif current is not None and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and not set("".join(cells)) <= set("-:") and cells[0] not in ("Option", "Company size"):
                tables[current].append(cells)
        elif current is not None and line.startswith("#"):
            current = None
    return tables


def _expected_cells(finding: dict) -> list:
    if finding["suppressed"]:
        return []
    if finding["form"] in ("two-wave", "movement-list"):
        out = []
        for row in finding["rows"]:
            state = row["movement"]["state"]
            earlier = "Not asked in 2025" if state == "not-asked" else ("Not compared" if row["previous"] is None else row["previous"])
            out.append([row["label"], earlier, row["display"], cell_text(row["movement"])])
        return out
    return [[row["label"], row["display"], str(row["base"])] for row in finding["rows"]]


_CORE_FEATURES = "core features"


def test_the_report_lists_three_chapters_in_reading_order_with_nine_findings(anon):
    """cov: C-CF-07, C-DC-01"""
    payload = ok(anon.get("/api/report"), "report read")
    chapters = payload["chapters"]
    assert [c["slug"] for c in chapters] == list(CHAPTER_SLUGS), chapters
    assert [(c["number"], c["title"]) for c in chapters] == [(n, t) for _s, n, t, _f in CHAPTERS], chapters
    for got, (_slug, _num, _title, findings) in zip(chapters, CHAPTERS):
        assert [(f["id"], f["short_title"]) for f in got["findings"]] == [(f[0], f[1]) for f in findings], got
        assert isinstance(got["reading_minutes"], int) and got["reading_minutes"] >= 1, got
    assert (int(payload["wave"]), int(payload["previous_wave"])) == (2026, 2025), payload


def test_every_heading_for_all_respondents_matches_its_regenerated_template(anon):
    """cov: C-CF-08, C-CF-09"""
    for slug in CHAPTER_SLUGS:
        got = by_id(resolved(anon, slug))
        for expected in chapter(slug, {})["findings"]:
            assert got[expected["id"]]["heading"] == expected["heading"], (slug, got[expected["id"]]["heading"])


def test_the_chapter_markup_carries_each_heading_source_line_and_figures_table(anon):
    """cov: C-CF-10, C-FE-06"""
    for slug in CHAPTER_SLUGS:
        response = anon.get(f"/chapters/{slug}")
        assert response.status_code == 200, describe(response)
        text = html_text(response.text)
        for expected in chapter(slug, {})["findings"]:
            assert expected["heading"] in text, (slug, expected["heading"])
            assert expected["source"] in text, (slug, expected["source"])
        assert text.count("The figures behind this chart") >= 3, slug


def test_key_takeaways_repeat_each_findings_heading_in_order(anon):
    """cov: C-CF-11, C-DC-02"""
    for seg in ({}, {"size": "startup"}):
        for slug in CHAPTER_SLUGS:
            payload = resolved(anon, slug, seg)
            expected = [(f["id"], f["heading"]) for f in chapter(slug, seg)["findings"]]
            assert [(t["finding"], t["text"]) for t in payload["takeaways"]] == expected, (slug, seg)


def test_the_reading_time_is_a_whole_number_of_minutes_with_charts_excluded(anon):
    """cov: C-CF-12"""
    report = ok(anon.get("/api/report"), "report read")
    for item in report["chapters"]:
        minutes = item["reading_minutes"]
        assert isinstance(minutes, int) and minutes >= 1, item
        text = html_text(anon.get(f"/chapters/{item['slug']}").text)
        assert f"{minutes} min read, charts excluded" in text, item["slug"]


def test_the_first_chapter_has_no_previous_control_and_the_last_has_no_next(anon):
    """cov: C-CF-13"""
    tools = html_text(anon.get("/chapters/tools").text)
    craft = html_text(anon.get("/chapters/craft").text)
    teams = html_text(anon.get("/chapters/teams").text)
    assert "02 . Craft" in tools and "03 . Teams" not in tools, "chapter one controls"
    assert "01 . Tools" in craft and "03 . Teams" in craft, "chapter two controls"
    assert "02 . Craft" in teams and "01 . Tools" not in teams, "chapter three controls"


def test_the_rail_marks_one_current_entry_programmatically(page):
    """cov: C-UX-01"""
    goto(page, "/chapters/tools")
    current = page.evaluate(_CURRENT_RAIL)
    assert len(current) == 1, current
    page.evaluate("() => window.scrollTo(0, document.documentElement.scrollHeight)")
    settle(1.5)
    current = page.evaluate(_CURRENT_RAIL)
    assert len(current) == 1 and "Relevant posts" in current[0], current


def test_reduced_motion_renders_every_chart_at_its_final_values(reduced_page):
    """cov: C-UX-02"""
    goto(reduced_page, "/chapters/tools")
    running = 0
    for _step in range(40):
        reduced_page.mouse.wheel(0, 900)
        reduced_page.wait_for_timeout(80)
        running = max(running, reduced_page.evaluate(
            "() => document.getAnimations().filter(a => a.playState === 'running').length"))
    assert running == 0, f"{running} animations ran under reduced motion"
    assert "The figures behind this chart" in reduced_page.evaluate("() => document.body.innerText")


def test_single_shares_sum_to_one_and_multi_shares_do_not(anon):
    """cov: C-CF-18"""
    tools = by_id(resolved(anon, "tools"))
    single = sum(r["value"] for r in tools["usage-frequency"]["rows"])
    multi = sum(r["value"] for r in tools["stack-ranked"]["rows"])
    assert abs(single - 1) < 1e-9, single
    expected = sum(val(2026, "stack-tools", i, {})[0] for i in range(len(Q["stack-tools"][3])))
    assert abs(multi - expected) < 1e-9 and multi > 1.5, multi


def test_the_numeric_mean_is_summed_tenths_over_respondents(anon, backend):
    """cov: C-CF-19, C-CF-20"""
    finding = by_id(resolved(anon, "craft"))["tool-count"]
    assert finding["heading"] == "Designers use 5.8 AI tools in a typical week.", finding["heading"]
    for row in finding["rows"]:
        tenths = backend.query("SELECT SUM(count) AS n FROM result WHERE wave = 2026 AND question = 'tool-count' AND size = %s",
                               (row["option"],))[0]["n"]
        people = backend.query("SELECT SUM(respondents) AS n FROM cell WHERE wave = 2026 AND size = %s", (row["option"],))[0]["n"]
        assert abs(row["value"] - int(tenths) / 10 / int(people)) < 1e-9, row
        assert row.get("margin_points") is None, row


def test_a_movement_is_rounded_from_full_precision_not_from_rounded_shares(anon):
    """cov: C-CF-21, C-CF-22"""
    rows = {r["option"]: r for r in by_id(resolved(anon, "tools"))["usage-frequency"]["rows"]}
    p26, _ = val(2026, "usage-frequency", 0, {})
    p25, _ = val(2025, "usage-frequency", 0, {})
    assert half_up(p26 * 100) - half_up(p25 * 100) == 17
    assert rows["daily"]["movement"] == {"state": "rise", "points": 16}, rows["daily"]
    assert rows["daily"]["display"] == "46%", rows["daily"]


def test_margin_points_follow_the_stated_interval_formula(anon):
    """cov: C-CF-23"""
    for seg in ({}, {"env": "agency"}, {"size": "scale-up"}):
        for got, expected in zip(by_id(resolved(anon, "tools", seg))["usage-frequency"]["rows"],
                                 chapter("tools", seg)["findings"][0]["rows"]):
            assert got["margin_points"] == expected["margin_points"], (seg, got)


def test_the_about_page_states_both_populations_the_confidence_and_the_caveat(anon):
    """cov: C-CF-25"""
    response = anon.get("/about")
    assert response.status_code == 200, describe(response)
    text = html_text(response.text)
    for phrase in ("About this report", "869", "709", "Figures carry a 95% confidence interval.",
                   "Because of how the survey was distributed",
                   "We present these findings as directional rather than as absolute benchmarks."):
        assert phrase in text, phrase


def test_every_heading_recomputes_for_each_single_band_segment(anon):
    """cov: C-CF-35, C-UF-03"""
    for key, bands in (("size", SIZES), ("env", ENVS), ("exp", EXPS)):
        for slug_band, _label in bands:
            seg = {key: slug_band}
            for slug in CHAPTER_SLUGS:
                got = [f["heading"] for f in resolved(anon, slug, seg)["findings"]]
                assert got == [f["heading"] for f in chapter(slug, seg)["findings"]], (seg, slug, got)


def test_segment_controls_compose_into_an_intersection_with_a_smaller_base(anon):
    """cov: C-CF-36, C-CF-37"""
    size_only = resolved(anon, "tools", {"size": "startup"})
    env_only = resolved(anon, "tools", {"env": "agency"})
    both = resolved(anon, "tools", {"size": "startup", "env": "agency"})
    assert (size_only["segment"]["base"], env_only["segment"]["base"], both["segment"]["base"]) == (223, 195, 68)
    assert both["segment"]["label"] == "Startups (1 to 50), Agency", both["segment"]
    expected = chapter("tools", {"size": "startup", "env": "agency"})["findings"]
    assert [f["heading"] for f in both["findings"]] == [f["heading"] for f in expected]


def test_the_segment_state_line_names_the_segment_base_and_population(anon):
    """cov: C-CF-38"""
    assert "Showing all respondents." in html_text(anon.get("/chapters/craft").text)
    text = html_text(anon.get("/chapters/craft", params={"size": "startup"}).text)
    assert "Showing Startups (1 to 50). 223 of 869 respondents." in text
    text = html_text(anon.get("/chapters/craft", params={"size": "startup", "env": "agency"}).text)
    assert "Showing Startups (1 to 50), Agency. 68 of 869 respondents." in text


def test_a_segment_change_is_announced_once_naming_the_segment_and_base(page):
    """cov: C-CF-39, C-UX-03"""
    goto(page, "/chapters/tools")
    page.get_by_label("Company size", exact=True).first.select_option(label="Startups (1 to 50)")
    page.wait_for_url(re.compile(r"size=startup"), timeout=15000)
    settle(2.0)
    announcements = page.evaluate(_LIVE_TEXT)
    joined = " ".join(announcements)
    assert joined.count("Now showing Startups (1 to 50), 223 respondents.") == 1, announcements


def test_a_segment_change_keeps_the_page_loaded_and_its_scroll_position(page):
    """cov: C-CF-40"""
    goto(page, "/chapters/tools")
    page.evaluate("() => { document.getElementById('stack-movement').scrollIntoView(); window.__probeLoaded = 1; }")
    settle(1.0)
    before = page.evaluate("() => document.getElementById('stack-movement').getBoundingClientRect().top")
    page.get_by_label("Company size", exact=True).first.select_option(label="Enterprise (2,000+)")
    page.wait_for_url(re.compile(r"size=enterprise"), timeout=15000)
    settle(2.0)
    assert page.evaluate("() => window.__probeLoaded") == 1, "the segment change reloaded the page"
    after = page.evaluate("() => document.getElementById('stack-movement').getBoundingClientRect().top")
    assert abs(after - before) < 150, (before, after)


def test_the_stick_reasons_ranking_reorders_under_enterprise_and_its_heading_follows(anon):
    """cov: C-CF-41, C-CF-42"""
    everyone = by_id(resolved(anon, "craft"))["stick-reasons"]
    enterprise = by_id(resolved(anon, "craft", {"size": "enterprise"}))["stick-reasons"]
    assert [r["option"] for r in everyone["rows"]] == ["speed", "quality", "team-standard", "integration", "cost"]
    assert [r["option"] for r in enterprise["rows"]] == [r["option"] for r in chapter("craft", {"size": "enterprise"})["findings"][2]["rows"]]
    assert enterprise["heading"] == "Speed and Team standard are the first reasons a tool sticks, too close to separate.", enterprise["heading"]


def test_a_deep_link_address_carries_the_segment_and_the_finding_anchor(anon):
    """cov: C-CF-43"""
    citation = _citation(anon, "tools", "usage-frequency", {"size": "startup"})
    parsed = urllib.parse.urlparse(citation["url"])
    assert parsed.path == "/chapters/tools", citation["url"]
    assert urllib.parse.parse_qs(parsed.query) == {"size": ["startup"]}, citation["url"]
    assert parsed.fragment == "usage-frequency", citation["url"]
    markup = anon.get("/chapters/tools", params={"size": "startup"}).text
    assert re.search(r"id=[\"']usage-frequency[\"']", markup), "no finding anchor"


def test_a_segment_below_thirty_withdraws_every_finding_with_its_reason(anon):
    """cov: C-CF-47, C-CF-48"""
    seg = {"size": "growth", "env": "freelance"}
    for slug in CHAPTER_SLUGS:
        payload = resolved(anon, slug, seg)
        assert int(payload["segment"]["base"]) == 20, payload["segment"]
        for got, (fid, short, *_rest) in zip(payload["findings"], [c for c in CHAPTERS if c[0] == slug][0][3]):
            assert got["suppressed"] is True and got["rows"] == [], got
            assert got["heading"] == f"{short}: not reported for this group.", got["heading"]
            assert got["message"] == "Too few respondents in this group to report. 20 answered.", got["message"]
        assert [t["text"] for t in payload["takeaways"]] == [f["heading"] for f in payload["findings"]]
    assert "Too few respondents in this group to report. 20 answered." in html_text(anon.get("/chapters/teams", params=seg).text)


def test_a_breakdown_band_below_thirty_carries_no_value(anon):
    """cov: C-CF-49"""
    finding = by_id(resolved(anon, "craft", {"env": "freelance"}))["confidence-by-size"]
    rows = {r["option"]: r for r in finding["rows"]}
    assert int(rows["startup"]["base"]) == 70 and rows["startup"]["display"] == "30%", rows["startup"]
    for band, base in (("growth", 20), ("scale-up", 9), ("enterprise", 5)):
        assert rows[band]["suppressed"] is True and rows[band]["value"] is None, rows[band]
        assert int(rows[band]["base"]) == base and rows[band]["display"] == "not reported, base too small", rows[band]


def test_a_withheld_finding_exports_its_reason_rather_than_a_table(anon):
    """cov: C-CF-50"""
    lines = export_text(anon, {"size": "growth", "env": "freelance"}).splitlines()
    headings = [i for i, line in enumerate(lines) if line.startswith("### ")]
    assert len(headings) == 9, headings
    for i in headings:
        following = [line for line in lines[i + 1:] if line.strip()][0]
        assert following == "Too few respondents in this group to report. 20 answered.", (lines[i], following)
    assert not any(line.startswith("| Option |") for line in lines), "a withheld export still carries a table"


def test_a_movement_is_suppressed_when_the_2025_base_is_below_thirty(anon):
    """cov: C-CF-51"""
    seg = {"size": "startup", "env": "freelance", "exp": "10-plus"}
    finding = by_id(resolved(anon, "tools", seg))["usage-frequency"]
    assert int(finding["base"]) == 30 and finding["suppressed"] is False, finding
    assert all(r["movement"] == {"state": "suppressed", "points": None} for r in finding["rows"]), finding["rows"]
    assert finding["heading"] == chapter("tools", seg)["findings"][0]["heading"], finding["heading"]
    assert "Too few 2025 answers to compare." in export_text(anon, seg)


def test_the_chapter_page_prints_the_interval_in_words_for_a_base_under_two_hundred(anon):
    """cov: C-FE-07"""
    text = html_text(anon.get("/chapters/tools", params={"env": "agency"}).text)
    assert "47%, give or take 7. Based on 195 answers." in text
    assert "give or take" not in html_text(anon.get("/chapters/tools").text)


def test_the_stack_movement_rows_carry_the_state_the_rule_assigns(anon):
    """cov: C-CF-55, C-CF-56"""
    rows = {r["option"]: r for r in by_id(resolved(anon, "tools"))["stack-movement"]["rows"]}
    expected = {"canvas-assistant": ("rise", 19), "image-generator": ("not-detectable", 3), "code-copilot": ("no-change", 0),
                "research-summariser": ("fall", -9), "prototype-builder": ("not-asked", None)}
    for option, (state, points) in expected.items():
        assert rows[option]["movement"] == {"state": state, "points": points}, rows[option]
    text = html_text(anon.get("/chapters/tools").text)
    for cell in ("+19pts", "-9pts", "No change since 2025.", "No detectable change since 2025.", "Not asked in 2025"):
        assert cell in text, cell


def test_a_non_comparable_question_never_yields_a_movement(anon):
    """cov: C-CF-58, C-DM-04"""
    for seg in ({}, {"size": "enterprise"}, {"env": "in-house"}):
        finding = by_id(resolved(anon, "teams", seg))["team-policy"]
        assert len(finding["rows"]) == 1, finding["rows"]
        row = finding["rows"][0]
        assert row["movement"] == {"state": "not-comparable", "points": None} and row["previous"] is None, (seg, row)
        assert "since 2025" not in finding["heading"], finding["heading"]
    assert "Asked differently in 2025, so the two are not compared." in html_text(anon.get("/chapters/teams").text)


def test_adjacent_ranks_too_close_to_separate_are_flagged_tied(anon):
    """cov: C-DC-05"""
    for slug, fid in (("craft", "stick-reasons"), ("tools", "stack-ranked")):
        for seg in ({}, {"env": "freelance"}):
            got = by_id(resolved(anon, slug, seg))[fid]["rows"]
            expected = [f for f in chapter(slug, seg)["findings"] if f["id"] == fid][0]["rows"]
            assert [(r["option"], r["tied_with_next"]) for r in got] == [(r["option"], r["tied_with_next"]) for r in expected], (fid, seg)
    assert "These two are too close to separate." in html_text(anon.get("/chapters/craft").text)


def test_an_exact_tie_in_a_ranking_is_broken_by_option_order(anon):
    """cov: C-DM-05"""
    rows = by_id(resolved(anon, "craft", {"size": "enterprise"}))["stick-reasons"]["rows"]
    assert abs(rows[0]["value"] - rows[1]["value"]) < 1e-12, rows[:2]
    assert [r["option"] for r in rows[:2]] == ["speed", "team-standard"], rows[:2]


def test_a_comparison_row_states_support_by_the_difference_rule(anon):
    """cov: C-CF-62, C-DC-06"""
    a, b = {"size": "startup"}, {"size": "enterprise"}
    payload = resolved(anon, "tools", a, b)
    assert payload["comparison"]["label"] == "Enterprise (2,000+)" and int(payload["comparison"]["base"]) == 242
    for row in by_id(payload)["usage-frequency"]["rows"]:
        i = opt_index("usage-frequency", row["option"])
        pa, na = val(2026, "usage-frequency", i, a)
        pb, nb = val(2026, "usage-frequency", i, b)
        assert row["compare"]["display"] == pct(pb) and int(row["compare"]["base"]) == nb, row
        assert row["compare"]["supported"] is supported(pa, na, pb, nb), row


def test_a_comparison_sentence_takes_the_supported_or_unsupported_form(anon):
    """cov: C-CF-63"""
    craft = by_id(resolved(anon, "craft", {"size": "startup"}, {"size": "enterprise"}))
    assert craft["confidence-by-size"]["comparison_sentence"] == (
        "Startups (1 to 50) 30%, Enterprise (2,000+) 17%. A real difference between these two groups.")
    tools = by_id(resolved(anon, "tools", {"env": "in-house"}, {"env": "agency"}))
    assert tools["usage-frequency"]["comparison_sentence"] == "In-house 45%, Agency 47%. Too close to call for these two groups."


def test_a_comparison_with_a_short_side_shows_one_segment_and_says_why(anon):
    """cov: C-CF-64"""
    payload = resolved(anon, "tools", {"size": "startup"}, {"size": "growth", "env": "freelance"})
    assert payload["comparison"]["suppressed"] is True, payload["comparison"]
    for row in by_id(payload)["usage-frequency"]["rows"]:
        assert row.get("compare") is None or row["compare"].get("suppressed") is True, row
    text = html_text(anon.get("/chapters/tools", params={"size": "startup", "vs_size": "growth", "vs_env": "freelance"}).text)
    assert "Growth (51 to 500), Freelance has too few respondents to compare." in text


def test_the_export_downloads_without_an_account_as_markdown_attachment(anon):
    """cov: C-CF-67"""
    response = anon.get("/api/export.md", params={"size": "startup"})
    assert response.status_code == 200, describe(response)
    assert response.headers.get("content-type", "").startswith("text/markdown"), response.headers
    disposition = response.headers.get("content-disposition", "")
    assert "attachment" in disposition and "studio-signals-2026.md" in disposition, disposition


def test_every_export_table_row_equals_the_chapter_figure_for_the_same_segment(anon):
    """cov: C-CF-68, C-TR-01"""
    for seg in ({}, {"size": "startup"}, {"env": "agency"}):
        tables = _export_tables(export_text(anon, seg))
        for slug in CHAPTER_SLUGS:
            for finding in resolved(anon, slug, seg)["findings"]:
                assert finding["heading"] in tables, (seg, finding["heading"])
                assert tables[finding["heading"]] == _expected_cells(finding), (seg, finding["id"])


def test_the_export_head_names_the_segment_and_the_utc_date(anon):
    """cov: C-CF-69, C-CF-70"""
    before = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    lines = export_text(anon, {"size": "startup"}).splitlines()
    after = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    assert lines[0] in {f"# Studio Signals, 2026 wave. Exported {d}. Startups (1 to 50)." for d in (before, after)}, lines[0]
    assert lines[2] == CAVEAT_SHORT and lines[3] == "Figures carry a 95% confidence interval.", lines[:4]
    head = export_text(anon).splitlines()[0]
    assert head.endswith(". All respondents."), head


def test_the_export_tables_use_the_pinned_headers_for_each_form(anon):
    """cov: C-CF-71, C-CF-72"""
    text = export_text(anon)
    assert text.count("| Option | 2026 | Base |") == 4, text.count("| Option | 2026 | Base |")
    assert text.count("| Option | 2025 | 2026 | Change |") == 3
    assert text.count("| Company size | 2026 | Base |") == 2
    positions = [text.index(h) for h in ("## 01 Tools", "## 02 Craft", "## 03 Teams")]
    assert positions == sorted(positions), positions


def test_the_export_follows_the_filter_for_each_single_band(anon):
    """cov: C-CF-73"""
    for key, bands in (("size", SIZES), ("env", ENVS)):
        for slug_band, band_label in bands:
            lines = export_text(anon, {key: slug_band}).splitlines()
            assert lines[0].endswith(f". {band_label}."), lines[0]
            sources = [line for line in lines if line.startswith("Source: Studio Signals survey")]
            assert len(sources) == 9 and all(f", {band_label}, base " in line for line in sources), (band_label, sources[:2])


def test_the_citation_carries_heading_base_segment_and_the_reproducing_address(anon):
    """cov: C-CF-74, C-DC-07"""
    heading = chapter("tools", {"size": "startup"})["findings"][0]["heading"]
    citation = _citation(anon, "tools", "usage-frequency", {"size": "startup"})
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    expected = (f'Studio Signals, 2026 wave. "{heading}" Base 223, Startups (1 to 50). {CAVEAT_SHORT} '
                f"Retrieved {citation['record']['retrieved']} from {citation['url']}.")
    assert citation["sentence"] == expected, citation["sentence"]
    assert citation["record"]["retrieved"][:4] == today[:4], citation["record"]
    record = citation["record"]
    assert (record["heading"], int(record["base"]), record["segment"], record["url"]) == (
        heading, 223, "Startups (1 to 50)", citation["url"]), record


def test_a_filtered_citation_carries_the_filter_note(anon):
    """cov: C-CF-75"""
    filtered = _citation(anon, "craft", "tool-count", {"size": "startup"})
    assert filtered["filtered_note"] == "This citation records that you filtered to Startups (1 to 50).", filtered
    plain = _citation(anon, "craft", "tool-count")
    assert plain["filtered_note"] is None, plain


def test_the_library_lists_the_readers_own_exports_newest_first(fresh):
    """cov: C-DC-09"""
    first = ok(fresh.post("/api/exports", json={"size": "startup"}), "first export")
    settle(1.2)
    second = ok(fresh.post("/api/exports", json={"env": "freelance"}), "second export")
    listed = ok(fresh.get("/api/exports"), "library read")
    assert [e["id"] for e in listed] == [second["id"], first["id"]], listed


def test_a_comparison_export_is_labelled_with_both_segments(fresh):
    """cov: C-CF-83"""
    saved = ok(fresh.post("/api/exports", json={"size": "startup", "vs_size": "enterprise"}), "comparison export")
    assert saved["label"] == "Comparing Startups (1 to 50) with Enterprise (2,000+)", saved
    head = fresh.get(f"/api/exports/{saved['id']}/download").text.splitlines()[0]
    assert head.endswith("Startups (1 to 50). Comparing Startups (1 to 50) with Enterprise (2,000+)."), head


def test_progress_states_follow_the_recorded_finding(fresh):
    """cov: C-CF-89, C-DC-10"""
    rows = ok(fresh.get("/api/progress"), "progress read")
    assert [(r["chapter"], r["finding"], r["state"]) for r in rows] == [(s, None, "not-started") for s in CHAPTER_SLUGS], rows
    _progress(fresh, "tools", "usage-frequency")
    assert ok(fresh.get("/api/progress"), "progress")[0]["state"] == "part-way"
    _progress(fresh, "tools", "closers")
    rows = ok(fresh.get("/api/progress"), "progress")
    assert (rows[0]["state"], rows[1]["state"]) == ("finished", "not-started"), rows


def test_a_stored_segment_redirects_a_chapter_opened_with_no_segment():
    """cov: C-CF-90"""
    _session, address = sign_up()
    _session.close()
    with cookie_session(address) as browser_like:
        ok(browser_like.put("/api/preferences", json={"size": "startup", "env": None, "exp": None}), "store segment")
        response = browser_like.get("/chapters/craft")
        assert response.status_code in (301, 302, 303, 307, 308), describe(response)
        assert "size=startup" in response.headers.get("location", ""), response.headers


def test_an_address_segment_replaces_the_stored_segment():
    """cov: C-CF-91"""
    _session, address = sign_up()
    _session.close()
    with cookie_session(address) as browser_like:
        ok(browser_like.put("/api/preferences", json={"size": "startup", "env": None, "exp": None}), "store segment")
        assert browser_like.get("/chapters/tools", params={"size": "enterprise"}).status_code == 200
        prefs = ok(browser_like.get("/api/preferences"), "preferences")
        assert (prefs["size"], prefs["env"], prefs["exp"]) == ("enterprise", None, None), prefs


def test_segment_all_clears_the_stored_segment():
    """cov: C-CF-92"""
    _session, address = sign_up()
    _session.close()
    with cookie_session(address) as browser_like:
        ok(browser_like.put("/api/preferences", json={"size": "startup", "env": None, "exp": None}), "store segment")
        assert browser_like.get("/chapters/tools", params={"segment": "all"}).status_code == 200
        prefs = ok(browser_like.get("/api/preferences"), "preferences")
        assert (prefs["size"], prefs["env"], prefs["exp"]) == (None, None, None), prefs
        assert browser_like.get("/chapters/tools").status_code == 200


def test_signing_up_creates_a_reader_usable_at_once(anon):
    """cov: C-RL-04, C-DC-11"""
    address = f"{unique('reader')}@example.com"
    payload = ok(anon.post("/api/auth/sign-up", json={
        "display_name": "New Reader", "email": address, "password": PASSWORD, "website": ""}), "sign up")
    assert payload["role"] == "reader" and payload["email"] == address and payload.get("token"), payload
    with client(str(payload["token"])) as session:
        assert ok(session.get("/api/exports"), "library read") == []


def test_the_terms_page_is_linked_from_every_footer_and_the_sign_up_form(anon):
    """cov: C-CF-101"""
    response = anon.get("/terms")
    assert response.status_code == 200 and title_of(response.text) == "Terms | Studio Signals", describe(response)
    for path in PUBLIC_PAGES:
        assert links_to(anon.get(path).text, "/terms"), path
    form = re.search(r"<form\b.*?</form>", anon.get("/sign-up").text, re.S | re.I)
    assert form and links_to(form.group(0), "/terms"), "the sign-up form carries no terms link"


def test_an_unknown_path_answers_404_with_the_not_found_page(anon):
    """cov: C-CF-102"""
    response = anon.get("/chapters/methods")
    missing(response, "an unknown chapter path")
    text = html_text(response.text)
    assert "Page not found" in text and "Back to the report" in text, text[:300]
    assert title_of(response.text) == "Page not found | Studio Signals"
    assert links_to(response.text, "/")


def test_an_announced_case_study_answers_404_and_is_never_linked(anon):
    """cov: C-CF-103"""
    cover = anon.get("/").text
    for slug in ANNOUNCED_CASES:
        missing(anon.get(f"/cases/{slug}"), f"announced case study {slug}")
        missing(anon.get(f"/api/cases/{slug}"), f"announced case study record {slug}")
        assert not links_to(cover, f"/cases/{slug}"), slug
    assert html_text(cover).count("Coming soon") >= 4


def test_a_published_case_study_reads_its_number_subject_and_category(anon):
    """cov: C-CF-104"""
    expected = {"harbour-type": ("01", "Harbour Type Co.", "TYPE FOUNDRY"), "kestrel-health": ("02", "Kestrel Health", "HEALTHCARE"),
                "fieldwork-studio": ("03", "Fieldwork Studio", "AGENCY")}
    for slug, (position, subject, category) in expected.items():
        record = ok(anon.get(f"/api/cases/{slug}"), slug)
        assert (record["position"], record["subject"], record["category"]) == (position, subject, category), record
        response = anon.get(f"/cases/{slug}")
        assert title_of(response.text) == f"{subject} | Studio Signals", title_of(response.text)
        assert category in html_text(response.text), slug


def test_every_internal_link_on_every_public_page_answers_200():
    """cov: C-CF-105"""
    seen = set()
    with httpx.Client(base_url=base_url(), timeout=TIMEOUT, follow_redirects=True) as walker:
        for path in PUBLIC_PAGES:
            for href in re.findall(r"<a\b[^>]*\bhref=[\"']([^\"']+)[\"']", walker.get(path).text, re.I):
                parsed = urllib.parse.urlparse(urllib.parse.urljoin(base_url() + path, href.replace("&amp;", "&")))
                if parsed.scheme not in ("http", "https") or parsed.netloc != urllib.parse.urlparse(base_url()).netloc:
                    continue
                target = parsed.path + (f"?{parsed.query}" if parsed.query else "")
                if target in seen:
                    continue
                seen.add(target)
                response = walker.get(target)
                assert response.status_code == 200, f"{href} on {path}: {describe(response)}"
    assert "/chapters/tools" in seen and "/terms" in seen, sorted(seen)[:20]


def test_body_text_and_chart_values_meet_the_4_5_contrast_bar(page):
    """cov: C-UX-04"""
    for path in ("/chapters/tools", "/about"):
        goto(page, path)
        pairs = page.evaluate(_TEXT_COLOURS, "p, td, th, li")
        assert pairs, f"no text found on {path}"
        worst = min(contrast(_over(front, back), back) for front, back in pairs)
        assert worst >= 4.5, (path, worst)


def test_prose_renders_at_16px_and_figures_at_13px_or_above(page):
    """cov: C-UX-05"""
    goto(page, "/chapters/tools")
    sizes = page.evaluate(_FONT_SIZES)
    assert sizes["prose"] and min(sizes["prose"]) >= 16, sizes["prose"][:5]
    assert sizes["figures"] and min(sizes["figures"]) >= 13, sizes["figures"][:5]


def test_a_chapter_never_scrolls_sideways_at_a_phone_width(phone_page):
    """cov: C-UX-06"""
    for path in ("/chapters/tools", "/chapters/craft?size=startup&vs_size=enterprise", "/"):
        goto(phone_page, path)
        widths = phone_page.evaluate("() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        assert widths[0] <= widths[1] + 1, (path, widths)


def test_the_footer_names_both_publishers_with_the_wave_year(anon):
    """cov: C-UF-09"""
    for path in ("/", "/about", "/chapters/teams"):
        assert "©2026 Northbeam Research, Aster & Vale. All rights reserved" in html_text(anon.get(path).text), path


_DATA_INTEGRITY = "data integrity"


def test_every_stored_result_row_matches_the_seed_generation_rule(backend):
    """cov: C-DM-01, C-DM-02"""
    stored = {}
    for row in backend.query("SELECT wave, question, option, size, env, exp, count FROM result"):
        stored[(int(row["wave"]), row["question"], row["option"], row["size"], row["env"], row["exp"])] = int(row["count"])
    expected = {}
    for wave in WAVES:
        for q, (typ, _w, _c, opts) in Q.items():
            for i, o in enumerate(opts):
                for cell in CELLS:
                    value = cell_count(wave, q, i, cell)
                    if value is not None:
                        expected[(wave, q, o[0]) + cell] = value
    assert len(stored) == len(expected), (len(stored), len(expected))
    wrong = [k for k, v in expected.items() if stored.get(k) != v]
    assert not wrong, [(k, stored.get(k), expected[k]) for k in wrong[:5]]
    cells = {(int(r["wave"]), r["size"], r["env"], r["exp"]): int(r["respondents"])
             for r in backend.query("SELECT wave, size, env, exp, respondents FROM cell")}
    assert cells == {(w,) + c: R[c][WAVES.index(w)] for w in WAVES for c in CELLS}


def test_a_published_share_reconciles_with_the_stored_result_rows(anon, backend):
    """cov: C-CF-17, C-OV-01, C-CN-01"""
    seg = {"size": "growth", "env": "in-house"}
    row = [r for r in by_id(resolved(anon, "tools", seg))["usage-frequency"]["rows"] if r["option"] == "daily"][0]
    count = backend.query("SELECT SUM(count) AS n FROM result WHERE wave = 2026 AND question = 'usage-frequency' "
                          "AND option = 'daily' AND size = 'growth' AND env = 'in-house'")[0]["n"]
    people = backend.query("SELECT SUM(respondents) AS n FROM cell WHERE wave = 2026 AND size = 'growth' AND env = 'in-house'")[0]["n"]
    assert abs(row["value"] - int(count) / int(people)) < 1e-9, (row, count, people)
    assert row["display"] == pct(int(count) / int(people)), row
    assert html_text(anon.get("/chapters/tools", params=seg).text).count(row["display"]) >= 1


def test_the_segments_endpoint_reports_population_and_composition_from_the_cells(anon):
    """cov: C-CF-24, C-DC-03"""
    payload = ok(anon.get("/api/segments"), "segments read")
    assert int(payload["threshold"]) == 30 and int(payload["confidence"]) == 95, payload
    assert {str(k): int(v) for k, v in payload["population"].items()} == {"2025": 709, "2026": 869}
    dims = {d["key"]: d for d in payload["dimensions"]}
    for key, bands in (("size", SIZES), ("env", ENVS), ("exp", EXPS)):
        assert [(b["slug"], b["label"]) for b in dims[key]["bands"]] == list(bands), dims[key]
        for band in dims[key]["bands"]:
            got = {str(k): int(v) for k, v in band["respondents"].items()}
            assert got == {str(w): respondents(w, {key: band["slug"]}) for w in WAVES}, band


def test_a_not_asked_option_has_no_2025_rows_and_no_movement_points(anon, backend):
    """cov: C-DM-03, C-CF-57"""
    assert backend.count("result", wave=2025, question="stack-tools", option="prototype-builder") == 0
    assert backend.count("result", wave=2026, question="stack-tools", option="prototype-builder") == 24
    row = [r for r in by_id(resolved(anon, "tools"))["stack-movement"]["rows"] if r["option"] == "prototype-builder"][0]
    assert row["movement"] == {"state": "not-asked", "points": None} and row["previous"] is None, row
    assert re.search(r"^\| Prototype builder \| Not asked in 2025 \| 32% \| Not asked in 2025 \|$", export_text(anon), re.M)


def test_a_reading_position_survives_a_reload_and_a_new_session(backend):
    """cov: C-CF-88, C-DM-09"""
    session, address = sign_up()
    with session:
        _progress(session, "tools", "stack-movement")
        me = ok(session.get("/api/auth/me"), "me read")
    with client(token_for(address)) as again:
        rows = {r["chapter"]: r for r in ok(again.get("/api/progress"), "progress read")}
    assert rows["tools"]["finding"] == "stack-movement" and rows["tools"]["state"] == "part-way", rows
    stored = backend.one("progress", account_id=me["id"], chapter="tools")
    assert stored and stored["finding"] == "stack-movement", stored


def test_a_subscription_is_stored_once_as_a_row(anon, backend):
    """cov: C-CF-99"""
    local = unique("Mixed")
    payload = ok(anon.post("/api/subscriptions", json={"email": f"  {local}@Example.COM ", "consent": True, "website": ""}), "subscribe")
    rows = backend.rows("subscription", email=f"{local.lower()}@example.com")
    assert len(rows) == 1 and payload["email"] == f"{local.lower()}@example.com", (rows, payload)


_AUTHORIZATION = "authorization"


def test_the_library_routes_redirect_a_visitor_to_sign_in_with_next(anon):
    """cov: C-UF-07"""
    for path in ("/library", "/library/new", "/library/new/compare", "/library/new/review"):
        response = anon.get(path)
        assert response.status_code in (301, 302, 303, 307, 308), describe(response)
        location = urllib.parse.unquote(response.headers.get("location", ""))
        assert location.endswith(f"/sign-in?next={path}"), (path, location)


def test_another_reader_downloading_a_saved_export_is_answered_as_missing(fresh, fresh2):
    """cov: C-RL-01, C-DM-08"""
    saved = ok(fresh.post("/api/exports", json={"size": "enterprise"}), "save export")
    missing(fresh2.get(f"/api/exports/{saved['id']}/download"), "another reader's export download")
    assert fresh.get(f"/api/exports/{saved['id']}/download").status_code == 200


def test_a_download_with_no_session_answers_401(anon, fresh):
    """cov: C-CF-85"""
    saved = ok(fresh.post("/api/exports", json={"size": "startup"}), "save export")
    response = anon.get(f"/api/exports/{saved['id']}/download")
    assert response.status_code == 401, describe(response)


def test_another_reader_cannot_remove_a_saved_export(reader, fresh, fresh2, store):
    """cov: C-RL-02"""
    saved = ok(fresh.post("/api/exports", json={"env": "in-house"}), "save export")
    missing(fresh2.delete(f"/api/exports/{saved['id']}"), "another reader removing an export")
    assert store.exists(saved["storage_key"]), saved
    assert fresh.get(f"/api/exports/{saved['id']}/download").status_code == 200


def test_the_object_store_refuses_an_anonymous_read_of_an_export_key(fresh):
    """cov: C-TR-04"""
    saved = ok(fresh.post("/api/exports", json={"exp": "under-10"}), "save export")
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    with httpx.Client(timeout=TIMEOUT) as direct:
        response = direct.get(f"{endpoint}/{os.environ['STORAGE_BUCKET']}/{saved['storage_key']}")
    assert response.status_code in (401, 403), describe(response)


def test_another_readers_export_never_appears_in_the_library_list(fresh, fresh2):
    """cov: C-RL-03"""
    saved = ok(fresh.post("/api/exports", json={"size": "growth"}), "save export")
    assert saved["id"] not in [e["id"] for e in ok(fresh2.get("/api/exports"), "second library")]
    assert saved["id"] in [e["id"] for e in ok(fresh.get("/api/exports"), "own library")]


def test_a_sign_up_with_the_decoy_field_filled_is_rejected_and_creates_no_account(anon, backend):
    """cov: C-CF-97"""
    address = f"{unique('bot')}@example.com"
    response = anon.post("/api/auth/sign-up", json={
        "display_name": "Bot", "email": address, "password": PASSWORD, "website": "https://spam.example.com"})
    assert response.status_code == 400, describe(response)
    assert backend.count("account", email=address) == 0
    notice = anon.post("/api/subscriptions", json={"email": address, "consent": True, "website": "spam"})
    assert notice.status_code == 400, describe(notice)
    assert backend.count("subscription", email=address) == 0


def test_a_repeated_subscription_within_sixty_seconds_is_refused_with_429(anon, backend):
    """cov: C-CF-98"""
    address = f"{unique('notice')}@example.com"
    first = anon.post("/api/subscriptions", json={"email": address, "consent": True, "website": ""})
    assert first.status_code == 201, describe(first)
    second = anon.post("/api/subscriptions", json={"email": address, "consent": True, "website": ""})
    assert second.status_code == 429, describe(second)
    assert backend.count("subscription", email=address) == 1


def test_a_wrong_password_and_an_unknown_address_answer_the_same_message(anon):
    """cov: C-CF-100"""
    wrong = anon.post("/api/auth/sign-in", json={"email": READER_EMAIL, "password": "wrong-password-1"})
    unknown = anon.post("/api/auth/sign-in", json={"email": f"{unique()}@example.com", "password": PASSWORD})
    refused(wrong, "a wrong password")
    refused(unknown, "an unknown address")
    assert body(wrong).get("error") == "That email and password do not match" == body(unknown).get("error"), (wrong.text, unknown.text)


_EDGE_CASES = "edge cases"


def test_an_unknown_band_resolves_to_all_respondents_with_the_invalid_segment_notice(anon):
    """cov: C-CF-34, C-DC-04"""
    payload = ok(_chapter_raw(anon, "tools", {"size": "galactic"}), "unknown band")
    assert payload["notice"] == UNKNOWN_SEGMENT, payload["notice"]
    assert int(payload["segment"]["base"]) == 869, payload["segment"]
    assert [f["heading"] for f in payload["findings"]] == [f["heading"] for f in chapter("tools", {})["findings"]]
    page_response = anon.get("/chapters/tools", params={"size": "galactic"})
    assert page_response.status_code == 200, describe(page_response)
    assert UNKNOWN_SEGMENT in html_text(page_response.text)
    assert resolved(anon, "tools")["notice"] is None


def test_an_unknown_finding_in_a_progress_write_is_refused(fresh):
    """cov: C-DM-10"""
    refused(_progress_raw(fresh, "tools", "hiring-outlook"), "a finding from another chapter")
    refused(_progress_raw(fresh, "tools", "nowhere"), "an unknown finding")
    assert ok(fresh.get("/api/progress"), "progress")[0]["state"] == "not-started"


_STORAGE = "storage"


def test_a_saved_export_is_stored_as_an_object_whose_bytes_match_the_export_download(anon, fresh, store):
    """cov: C-CF-81, C-DM-06, C-TR-02"""
    response = fresh.post("/api/exports", json={"size": "enterprise"})
    assert response.status_code == 201, describe(response)
    saved = body(response)
    expected = export_text(anon, {"size": "enterprise"})
    assert store.exists(saved["storage_key"]), saved
    download = fresh.get(f"/api/exports/{saved['id']}/download")
    assert download.status_code == 200 and download.text == expected, describe(download)
    assert download.headers.get("content-type", "").startswith("text/markdown"), download.headers


def test_a_saved_export_object_key_follows_the_account_and_export_scheme(fresh):
    """cov: C-TR-03, C-DC-08"""
    me = ok(fresh.get("/api/auth/me"), "me read")
    saved = ok(fresh.post("/api/exports", json={"env": "agency"}), "save export")
    matched = EXPORT_KEY_RE.match(saved["storage_key"])
    assert matched, saved
    assert matched["account"] == str(me["id"]) and matched["export"] == str(saved["id"]), saved
    assert saved["label"] == "Agency" and saved.get("created_at"), saved


def test_the_export_record_is_stored_as_a_row_with_segment_and_label(fresh, backend):
    """cov: C-DM-07"""
    saved = ok(fresh.post("/api/exports", json={"size": "scale-up", "exp": "10-plus"}), "save export")
    row = backend.one("export", id=saved["id"])
    assert row, saved
    assert (row["size"], row["env"], row["exp"], row["vs_size"]) == ("scale-up", None, "10-plus", None), row
    assert row["label"] == "Scale-up (501 to 2K), 10 years or more" and row["storage_key"] == saved["storage_key"], row


def test_removing_a_saved_export_deletes_its_row_and_its_object(fresh, backend, store):
    """cov: C-CF-82"""
    saved = ok(fresh.post("/api/exports", json={"size": "growth"}), "save export")
    assert store.exists(saved["storage_key"])
    ok(fresh.delete(f"/api/exports/{saved['id']}"), "remove export")
    assert backend.one("export", id=saved["id"]) is None
    assert not store.exists(saved["storage_key"]), saved
    missing(fresh.get(f"/api/exports/{saved['id']}/download"), "a removed export")
