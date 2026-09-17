"""Outcome graders for the Naught' task.

One module, every section and both declared slots. Black-box: HTTP against the
running app, the rendered page through Playwright, PostgreSQL through the shared
backend adapter and MinIO through the shared storage adapter. Nothing here reads
the agent's source.
"""

from __future__ import annotations

import datetime
import html as html_lib
import os
import re
import urllib.parse

import httpx

from conftest import (
    AUTHOR_NAME,
    BRAND,
    BYLINE,
    CONTACT_EMAIL,
    COPYRIGHT,
    DISCIPLINES,
    DISCIPLINE_SET,
    DRAFT_SLUG,
    FEATURED,
    KEY_RE,
    NOT_FOUND_TITLE,
    OK,
    PASSWORD,
    PEOPLE,
    PUBLISHED,
    READER2_EMAIL,
    READER_EMAIL,
    REFUSED,
    SERVICES,
    TAGLINES,
    TIMEOUT,
    TITLES,
    base_url,
    body,
    client,
    contrast,
    describe,
    enquiry_doc,
    free_ordinal,
    meta_property,
    missing,
    new_work,
    norm,
    ok,
    png_bytes,
    refused,
    settle,
    sha256_hex,
    sign_up,
    title_of,
    unique,
    upload,
    works,
)

PUBLIC_ROUTES = ("/", "/works", "/works/solace", "/privacy")
LAYOUTS = ("full-bleed", "coloured-band", "split", "gradient-band")

_FILMS = """() => Array.from(document.querySelectorAll('video')).map(v => ({
  muted: v.muted, loop: v.loop, controls: v.controls, paused: v.paused}))"""

_MARK_OVERLAY = """() => {
  const row = Array.from(document.querySelectorAll('body *')).find(el =>
    el.children.length === 0 && el.textContent.trim().toLowerCase() === 'contact'
    && el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true}));
  if (!row) return false;
  let box = row;
  while (box.parentElement) {
    const r = box.getBoundingClientRect();
    if (r.width >= innerWidth * 0.9 && r.height >= innerHeight * 0.9) break;
    box = box.parentElement;
  }
  box.setAttribute('data-probe-overlay', '1');
  return true;
}"""

_VISIBLE_LINKS = """() => Array.from(document.querySelectorAll('a[href]')).flatMap(a => {
  const r = a.getBoundingClientRect();
  if (!r.width || !r.height) return [];
  const x = r.left + r.width / 2, y = r.top + r.height / 2;
  if (x < 0 || y < 0 || x > innerWidth || y > innerHeight) return [];
  const hit = document.elementFromPoint(x, y);
  if (!hit || !(a === hit || a.contains(hit))) return [];
  return [[a.textContent.trim().toLowerCase(), new URL(a.href).pathname]];
})"""

_COLOUR_WALK = """
  const parse = s => { const n = (s.match(/[\\d.]+/g) || []).map(Number);
    return [n[0] || 0, n[1] || 0, n[2] || 0, n.length > 3 ? n[3] : 1]; };
  const ground = el => { let node = el;
    while (node) { const c = parse(getComputedStyle(node).backgroundColor);
      if (c[3] > 0) return c.slice(0, 3); node = node.parentElement; }
    return [255, 255, 255]; };
  const blended = el => { let node = el;
    while (node) { if (getComputedStyle(node).mixBlendMode !== 'normal') return true; node = node.parentElement; }
    return false; };
  const shown = el => el.checkVisibility({checkOpacity: false, checkVisibilityCSS: true})
    && !el.closest('[aria-hidden="true"]') && !blended(el);
"""

_TEXT_COLOURS = "(selector) => {" + _COLOUR_WALK + """
  return Array.from(document.querySelectorAll(selector))
    .filter(el => el.textContent.trim().length > 20 && shown(el))
    .map(el => [parse(getComputedStyle(el).color), ground(el)]);
}"""

_EYEBROWS = "(titles) => {" + _COLOUR_WALK + """
  return Array.from(document.querySelectorAll('body *'))
    .filter(el => titles.includes(el.textContent.trim().toUpperCase()) && shown(el)
      && /mono/i.test(getComputedStyle(el).fontFamily)
      && !Array.from(el.children).some(child => child.textContent.trim().length))
    .map(el => { const s = getComputedStyle(el);
      return {color: parse(s.color), back: ground(el), family: s.fontFamily,
              size: s.fontSize, weight: s.fontWeight}; });
}"""

_MASTHEAD = """(text) => {
  const found = Array.from(document.querySelectorAll('body *')).filter(el =>
    el.textContent.replace(/\\s+/g, '') === text
    && el.checkVisibility({checkOpacity: false, checkVisibilityCSS: true}));
  if (!found.length) return null;
  const pick = found.reduce((a, b) =>
    parseFloat(getComputedStyle(b).fontSize) > parseFloat(getComputedStyle(a).fontSize) ? b : a);
  const s = getComputedStyle(pick);
  return {family: s.fontFamily, size: s.fontSize, weight: s.fontWeight};
}"""


def _text(markup: str) -> str:
    """The visible copy of a document: scripts and styles dropped, tags collapsed."""
    markup = re.sub(r"<(script|style|template)\b.*?</\1>", " ", markup, flags=re.S | re.I)
    return re.sub(r"\s+", " ", norm(html_lib.unescape(re.sub(r"<[^>]+>", " ", markup)))).strip()


def _links_to(markup: str, path: str) -> bool:
    pattern = rf"href=[\"'](?:https?://[^\"'/]+)?{re.escape(path)}/?[\"']"
    return re.search(pattern, markup, re.I) is not None


def _record(session: httpx.Client, slug: str) -> dict:
    return ok(session.get(f"/api/works/{slug}"), f"the {slug} record read")


def _media_path(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    assert path.startswith("/media/"), f"an image address outside /media/: {url}"
    return path


def _published_probe(author: httpx.Client, **over) -> tuple[dict, str]:
    """A throwaway case study with one cover, published; callers unpublish it."""
    work = new_work(author, **over)
    media = ok(upload(author, work["id"], png_bytes(unique("probe-cover"))), "probe cover upload")
    ok(author.post(f"/api/works/{work['id']}/publish"), "probe publish")
    return work, media["storage_key"]


def _cookie_session(email: str) -> httpx.Client:
    """A client carrying only the session cookie, as a browser page request would."""
    session = httpx.Client(base_url=base_url(), timeout=TIMEOUT, follow_redirects=False)
    ok(session.post("/api/auth/sign-in", json={"email": email, "password": PASSWORD}), f"sign in {email}")
    return session


def _draft_keys(author: httpx.Client) -> list[str]:
    record = ok(author.get(f"/api/works/{DRAFT_SLUG}"), "draft read")
    urls = [record["cover"]["url"]] + [image["url"] for image in record["gallery"]]
    return [_media_path(url)[len("/media/"):] for url in urls]


def _over(front: list, back: list) -> tuple:
    alpha = front[3] if len(front) > 3 else 1
    return tuple(round(f * alpha + b * (1 - alpha)) for f, b in zip(front[:3], back[:3]))


def _goto(tab, path: str) -> None:
    tab.goto(base_url() + path, wait_until="load")
    settle(2.5)


def _scroll_through(tab) -> None:
    """Wheel down the whole document so every scroll-driven band has been reached."""
    for _step in range(90):
        before = tab.evaluate("() => scrollY")
        tab.mouse.wheel(0, 700)
        tab.wait_for_timeout(120)
        if tab.evaluate("() => scrollY") == before and before > 0:
            break


def _open_menu(tab, path: str) -> list:
    _goto(tab, path)
    tab.get_by_role("button", name=re.compile("menu", re.I)).first.click()
    settle(1.5)
    return [tuple(pair) for pair in tab.evaluate(_VISIBLE_LINKS)]


def _sound_toggle(tab):
    candidates = tab.locator("[aria-pressed], [aria-checked]")
    for index in range(candidates.count()):
        candidate = candidates.nth(index)
        label = (candidate.text_content() or "") + (candidate.get_attribute("aria-label") or "")
        if re.search("sound", label, re.I) and candidate.is_visible():
            return candidate
    raise AssertionError("no visible SOUND toggle announcing a pressed or checked state")


_CORE_FEATURES = "core features"


def test_the_home_route_is_served_to_a_visitor_with_no_session(anon):
    """cov: C-OV-01, C-UF-02"""
    response = anon.get("/")
    assert response.status_code == 200, describe(response)
    assert title_of(response.text) == f"{BRAND} | Home", title_of(response.text)


def test_the_home_route_featured_rail_count_reads_the_published_catalogue_length(anon, author):
    """cov: C-CF-03"""
    assert re.search(r"View all\s*\(\s*07\s*\)", _text(anon.get("/").text)), "View all ( 07 ) missing"
    probe, _key = _published_probe(author)
    try:
        home = _text(anon.get("/").text)
        assert re.search(r"View all\s*\(\s*08\s*\)", home), "the count did not follow the catalogue"
    finally:
        author.post(f"/api/works/{probe['id']}/unpublish")


def test_the_home_route_markup_carries_every_band_headline_in_order(anon):
    """cov: C-CF-04"""
    text = _text(anon.get("/").text)
    phrases = ["Not a style, a perspective.", "Most brands produce content.", "We prefer ideas.",
               "( The step aside )", "Good brands communicate.", "Great brands surprise.",
               "View all", "( The Studio )", "Forms follow", "We design",
               "Naught' without people", "Let's start"]
    cursor = 0
    for phrase in phrases:
        found = text.find(phrase, cursor)
        assert found >= 0, f"{phrase!r} missing or out of order on the home route"
        cursor = found + len(phrase)


def test_the_home_route_markup_omits_the_reference_editor_leftovers(anon):
    """cov: C-CN-01"""
    for path in ("/", "/works", "/works/solace", "/privacy"):
        text = _text(anon.get(path).text)
        assert "No items found" not in text, path
        assert "inside of a div block" not in text, path
        assert not re.search(r"(?<![\w.,©'])000(?![\w.,])", text), f"a bare 000 on {path}"


def test_the_health_route_answers_ok(anon):
    """cov: C-DC-04"""
    payload = ok(anon.get("/api/health"), "health read")
    assert payload.get("status") == "ok", payload


def test_the_works_read_returns_the_seven_published_case_studies_in_ordinal_order(anon):
    """cov: C-CF-07, C-DC-05"""
    rows = works(anon)
    seeded = [row["slug"] for row in rows if not row["slug"].startswith("probe-")]
    assert seeded == list(PUBLISHED), seeded
    ordinals = [int(row["ordinal"]) for row in rows]
    assert ordinals == sorted(ordinals), ordinals
    assert all(row["published"] is True for row in rows), rows


def test_the_works_index_title_is_the_brand_then_works_joined_by_the_bar_separator(anon):
    """cov: C-UF-03, C-UF-04"""
    assert title_of(anon.get("/works").text) == f"{BRAND} | Works"


def test_a_published_case_study_route_answers_with_its_title_in_the_document_title(anon):
    """cov: C-UF-06"""
    for slug in PUBLISHED:
        response = anon.get(f"/works/{slug}")
        assert response.status_code == 200, describe(response)
        assert title_of(response.text) == f"{BRAND} | {TITLES[slug]}", title_of(response.text)


def test_the_last_case_study_names_the_first_as_its_next_subject(anon):
    """cov: C-CF-11"""
    for slug, expected in (("chemie-union", "solace"), ("solace", "urbana")):
        text = _text(anon.get(f"/works/{slug}").text)
        tail = text[text.rfind("Let's start from naught'"):]
        positions = {other: tail.find(TITLES[other]) for other in PUBLISHED
                     if other != slug and TITLES[other] in tail}
        assert positions, f"no next subject after the closing panel on {slug}"
        assert min(positions, key=positions.get) == expected, positions


def test_the_case_study_compact_list_omits_the_current_subject(anon):
    """cov: C-CF-12"""
    markup = anon.get("/works/solace").text
    assert not _links_to(markup, "/works/solace"), "the current case study links to itself"
    for slug in PUBLISHED[1:]:
        assert _links_to(markup, f"/works/{slug}"), f"the compact list misses {slug}"


def test_a_case_study_with_no_gallery_images_renders_no_gallery_placeholder_text(anon, author):
    """cov: C-CF-13"""
    probe, key = _published_probe(author)
    try:
        response = anon.get(f"/works/{probe['slug']}")
        assert response.status_code == 200, describe(response)
        keys = set(re.findall(r"/media/(works/[^\"'\s)?]+)", response.text))
        assert keys == {key}, keys
        assert "No items found" not in _text(response.text)
    finally:
        author.post(f"/api/works/{probe['id']}/unpublish")


def test_a_visitor_with_no_session_files_an_enquiry_with_status_new(anon):
    """cov: C-CF-18, C-CF-19"""
    payload = ok(anon.post("/api/enquiries", json=enquiry_doc()), "booking")
    assert payload.get("id") is not None and payload.get("created_at"), payload
    assert payload["status"] == "new", payload


def test_signing_up_creates_a_reader_account_usable_at_once(anon):
    """cov: C-RL-02, C-DC-09"""
    address = f"{unique('reader')}@example.com"
    payload = ok(anon.post("/api/auth/sign-up", json={
        "display_name": "Probe Reader", "email": address, "password": PASSWORD}), "sign up")
    assert payload["role"] == "reader" and payload["email"] == address, payload
    with client(str(payload["token"])) as session:
        me = ok(session.get("/api/auth/me"), "me read")
    assert me["role"] == "reader" and me["display_name"] == "Probe Reader", me


def test_an_author_creates_a_case_study_as_a_draft(anon, author, backend):
    """cov: C-CF-41, C-DC-11"""
    work = new_work(author)
    assert work["published"] is False, work
    row = backend.one("work", id=work["id"])
    assert row and row["published"] is False, row
    missing(anon.get(f"/api/works/{work['slug']}"), "a new draft record")


def test_publishing_a_draft_exposes_its_route_record_and_cover(anon, author):
    """cov: C-CF-46, C-DC-13"""
    work = new_work(author)
    media = ok(upload(author, work["id"], png_bytes(unique("publish"))), "cover upload")
    key = media["storage_key"]
    missing(anon.get(f"/works/{work['slug']}"), "the draft route")
    missing(anon.get(f"/media/{key}"), "the draft cover")
    try:
        assert ok(author.post(f"/api/works/{work['id']}/publish"), "publish")["published"] is True
        assert anon.get(f"/works/{work['slug']}").status_code == 200
        assert ok(anon.get(f"/api/works/{work['slug']}"), "published record")["slug"] == work["slug"]
        served = anon.get(f"/media/{key}")
        assert served.status_code == 200, describe(served)
        assert served.headers.get("content-type", "").startswith("image/png"), served.headers
    finally:
        author.post(f"/api/works/{work['id']}/unpublish")


def test_an_author_reads_the_draft_record_and_its_image(author):
    """cov: C-CF-57, C-DC-15"""
    record = ok(author.get(f"/api/works/{DRAFT_SLUG}"), "draft read")
    assert record["published"] is False and record["title"] == TITLES[DRAFT_SLUG], record
    listed = {row["slug"]: row for row in works(author)}
    assert listed[DRAFT_SLUG]["published"] is False, listed[DRAFT_SLUG]
    served = author.get(_media_path(record["cover"]["url"]))
    assert served.status_code == 200, describe(served)
    assert served.headers.get("content-type", "").startswith("image/"), served.headers


def test_an_author_lists_every_enquiry_newest_first(anon, author, reader, reader2):
    """cov: C-RL-11, C-DC-17"""
    filed = [ok(session.post("/api/enquiries", json=enquiry_doc(email=address)), "booking")["id"]
             for session, address in ((reader, READER_EMAIL), (reader2, READER2_EMAIL), (anon, f"{unique('visitor')}@example.com"))]
    listed = ok(author.get("/api/enquiries"), "author enquiries")
    ids = [item["id"] for item in listed]
    assert all(item in ids for item in filed), (filed, ids[:10])
    stamps = [item["created_at"] for item in listed]
    assert stamps == sorted(stamps, reverse=True), stamps[:10]


def test_an_author_moves_an_enquiry_to_contacted_then_closed(anon, author, backend):
    """cov: C-CF-69, C-DC-18"""
    filed = ok(anon.post("/api/enquiries", json=enquiry_doc()), "booking")
    for status in ("contacted", "closed"):
        payload = ok(author.patch(f"/api/enquiries/{filed['id']}", json={"status": status}), status)
        assert payload["status"] == status, payload
        assert backend.one("enquiry", id=filed["id"])["status"] == status


def test_marking_a_sixth_case_study_featured_keeps_the_rail_at_five(anon, author):
    """cov: C-CF-70"""
    kine = {row["slug"]: row for row in works(author)}["kine"]
    ok(author.patch(f"/api/works/{kine['id']}", json={"featured": True}), "feature kine")
    try:
        home = anon.get("/").text
        linked = [slug for slug in PUBLISHED if _links_to(home, f"/works/{slug}")]
        assert linked == list(FEATURED), linked
    finally:
        author.patch(f"/api/works/{kine['id']}", json={"featured": False})


def test_an_unmatched_path_answers_404_with_the_not_found_title(anon):
    """cov: C-CF-73, C-TR-06"""
    response = anon.get(f"/{unique('nowhere')}")
    missing(response, "an unmatched path")
    assert title_of(response.text) == NOT_FOUND_TITLE, title_of(response.text)


def test_the_not_found_page_keeps_the_chrome_and_a_hidden_error_404_heading(anon):
    """cov: C-CF-74"""
    markup = anon.get("/nowhere").text
    headings = [_text(inner) for inner in re.findall(r"<h[1-6][^>]*>(.*?)</h[1-6]>", markup, re.S | re.I)]
    assert "ERROR 404" in headings, headings
    assert "Homepage" in _text(markup)
    assert _links_to(markup, "/"), "no link home"
    assert re.search(r">\s*EN\s*<", markup), "no language chip"
    assert re.search(r"menu", markup, re.I), "no menu control"
    assert BYLINE in _text(markup)


def test_six_unmatched_analytics_style_paths_answer_404_with_the_not_found_title(anon):
    """cov: C-UF-18"""
    for path in ("/wp-login.php", "/.env", f"/works/{unique('nope')}", "/about", "/blog", "/contact"):
        response = anon.get(path)
        missing(response, path)
        assert title_of(response.text) == NOT_FOUND_TITLE, (path, title_of(response.text))


def test_the_menu_overlay_first_row_reads_works_on_home_and_home_elsewhere(page):
    """cov: C-FE-55"""
    home_links = _open_menu(page, "/")
    assert ("works", "/works") in home_links, home_links
    assert not any(text == "home" for text, _href in home_links), home_links
    works_links = _open_menu(page, "/works")
    assert ("home", "/") in works_links, works_links
    assert not any(text == "works" for text, _href in works_links), works_links


def test_every_public_route_carries_the_menu_control_the_language_chip_and_the_header_mark_link(anon):
    """cov: C-FE-56, C-FE-57"""
    for path in PUBLIC_ROUTES + ("/nowhere",):
        markup = anon.get(path).text
        assert _links_to(markup, "/"), f"no header mark link on {path}"
        assert re.search(r">\s*EN\s*<", markup), f"no language chip on {path}"
        assert re.search(r"\bmenu\b", markup, re.I), f"no menu control on {path}"
        assert BYLINE in _text(markup), f"no byline on {path}"


def test_every_public_route_footer_links_to_the_privacy_page(anon):
    """cov: C-CF-75"""
    for path in PUBLIC_ROUTES:
        markup = anon.get(path).text
        assert _links_to(markup, "/privacy"), f"no privacy link on {path}"
        assert "Privacy" in _text(markup), path


def test_the_menu_overlay_traps_focus_while_open(page):
    """cov: C-UX-12"""
    _goto(page, "/works")
    page.get_by_role("button", name=re.compile("menu", re.I)).first.click()
    settle(1.5)
    assert page.evaluate(_MARK_OVERLAY), "no overlay covering the window with a contact row"
    for _step in range(24):
        page.keyboard.press("Tab")
        inside = page.evaluate(
            "() => { const a = document.activeElement; const o = document.querySelector('[data-probe-overlay]');"
            " return !!a && (o.contains(a) || /menu/i.test((a.getAttribute('aria-label') || '') + a.textContent)); }")
        assert inside, "focus left the open menu overlay"
    page.keyboard.press("Escape")
    settle(1.0)
    label = page.evaluate("() => { const a = document.activeElement;"
                          " return a ? (a.getAttribute('aria-label') || '') + ' ' + a.textContent : ''; }")
    assert re.search("menu", label, re.I), f"focus did not return to the menu control: {label!r}"


def test_every_film_starts_muted_looping_without_controls_until_the_sound_toggle_is_pressed(page):
    """cov: C-CF-78, C-FE-60"""
    _goto(page, "/")
    _scroll_through(page)
    films = page.evaluate(_FILMS)
    assert len(films) >= 2, films
    assert all(film["muted"] and film["loop"] and not film["controls"] for film in films), films
    page.evaluate("() => document.querySelector('video').scrollIntoView({block: 'center'})")
    settle(1.5)
    toggle = _sound_toggle(page)
    toggle.click()
    settle(1.0)
    assert any(not film["muted"] for film in page.evaluate(_FILMS)), "the toggle turned no sound on"


def test_the_sound_toggle_announces_its_state_to_assistive_technology(page):
    """cov: C-CF-79"""
    _goto(page, "/")
    _scroll_through(page)
    page.evaluate("() => document.querySelector('video').scrollIntoView({block: 'center'})")
    settle(1.5)
    toggle = _sound_toggle(page)
    before = toggle.get_attribute("aria-pressed") or toggle.get_attribute("aria-checked")
    toggle.click()
    settle(1.0)
    after = toggle.get_attribute("aria-pressed") or toggle.get_attribute("aria-checked")
    assert (before, after) == ("false", "true"), (before, after)


def test_a_film_starts_muted_again_after_a_route_change(page):
    """cov: C-CF-80"""
    _goto(page, "/")
    _scroll_through(page)
    page.evaluate("() => document.querySelector('video').scrollIntoView({block: 'center'})")
    settle(1.5)
    _sound_toggle(page).click()
    settle(1.0)
    _goto(page, "/works")
    _goto(page, "/")
    films = page.evaluate(_FILMS)
    assert films and all(film["muted"] for film in films), films


def test_no_film_is_fetched_while_its_band_is_far_below_the_window(page):
    """cov: C-CF-81"""
    fetched = []
    page.on("request", lambda request: fetched.append(request.url)
            if request.resource_type == "media" or re.search(r"\.(mp4|webm|mov|m4v)(\?|$)", request.url)
            else None)
    _goto(page, "/")
    settle(2.0)
    assert fetched == [], fetched


def test_reduced_motion_renders_no_followers_and_no_autoplaying_film(reduced_page):
    """cov: C-UX-15"""
    _goto(reduced_page, "/")
    _scroll_through(reduced_page)
    films = reduced_page.evaluate(_FILMS)
    assert films and all(film["paused"] for film in films), films
    assert reduced_page.get_by_role("button", name=re.compile("play", re.I)).count() >= 1


def test_the_followers_and_the_work_label_are_hidden_from_assistive_technology(page):
    """cov: C-UX-16"""
    _goto(page, "/works")
    hidden = page.evaluate(
        "() => { const label = Array.from(document.querySelectorAll('body *'))"
        ".find(el => el.children.length === 0 && el.textContent.trim().toUpperCase() === 'VIEW');"
        " return label ? !!label.closest('[aria-hidden=\"true\"]') : null; }")
    assert hidden is True, f"the work label is exposed to assistive technology: {hidden}"


def test_each_film_carries_a_caption_track_and_a_text_description(page):
    """cov: C-UX-17"""
    _goto(page, "/")
    described = page.evaluate(
        "() => Array.from(document.querySelectorAll('video')).map(v => ({"
        " track: !!v.querySelector('track[kind=\"captions\"], track[kind=\"subtitles\"]'),"
        " text: !!(v.getAttribute('aria-describedby') || v.closest('figure')?.querySelector('figcaption')"
        " || v.getAttribute('aria-label')) }))")
    assert len(described) >= 2, described
    assert all(film["track"] and film["text"] for film in described), described


def test_the_privacy_route_carries_its_title_retention_and_the_deletion_contact(anon):
    """cov: C-CF-83, C-UF-20"""
    response = anon.get("/privacy")
    assert response.status_code == 200, describe(response)
    assert title_of(response.text) == f"{BRAND} | Privacy"
    text = _text(response.text).lower()
    assert "twelve months" in text and CONTACT_EMAIL in text, text[:400]
    for kept in ("name", "email", "company", "service", "preferred date", "time window", "message"):
        assert kept in text, kept


def test_every_public_route_declares_og_title_and_an_og_image_that_answers_200(anon):
    """cov: C-CF-84, C-TR-07"""
    for path in PUBLIC_ROUTES + tuple(f"/works/{slug}" for slug in PUBLISHED[1:]):
        markup = anon.get(path).text
        assert meta_property(markup, "og:title"), f"no og:title on {path}"
        image = meta_property(markup, "og:image")
        assert image, f"no og:image on {path}"
        served = anon.get(urllib.parse.urlparse(image).path)
        assert served.status_code == 200, describe(served)
        assert served.headers.get("content-type", "").startswith("image/"), (path, served.headers)


def test_a_case_study_preview_image_is_its_cover_media_address(anon):
    """cov: C-TR-08"""
    for slug in PUBLISHED:
        record = ok(anon.get(f"/api/works/{slug}"), f"{slug} read")
        image = meta_property(anon.get(f"/works/{slug}").text, "og:image")
        assert urllib.parse.urlparse(image).path == _media_path(record["cover"]["url"]), (slug, image)


def test_the_generated_preview_images_for_home_works_and_privacy_answer_as_png(anon):
    """cov: C-TR-09"""
    for name, path in (("home", "/"), ("works", "/works"), ("privacy", "/privacy")):
        image = meta_property(anon.get(path).text, "og:image")
        assert urllib.parse.urlparse(image).path == f"/og/{name}.png", (path, image)
        served = anon.get(f"/og/{name}.png")
        assert served.status_code == 200 and served.content.startswith(b"\x89PNG"), describe(served)


def test_every_internal_link_on_every_public_route_answers_200():
    """cov: C-CF-85"""
    seen = set()
    with httpx.Client(base_url=base_url(), timeout=TIMEOUT, follow_redirects=True) as walker:
        for path in PUBLIC_ROUTES:
            for href in re.findall(r"<a\b[^>]*\bhref=[\"']([^\"']+)[\"']", walker.get(path).text, re.I):
                parsed = urllib.parse.urlparse(urllib.parse.urljoin(base_url() + path, html_lib.unescape(href)))
                if parsed.scheme not in ("http", "https") or parsed.netloc != urllib.parse.urlparse(base_url()).netloc:
                    continue
                target = parsed.path + (f"?{parsed.query}" if parsed.query else "")
                if target in seen:
                    continue
                seen.add(target)
                response = walker.get(target)
                assert response.status_code == 200, f"{href} on {path}: {describe(response)}"
    assert "/works" in seen and "/privacy" in seen, seen


def test_an_image_is_served_through_the_media_route_with_its_content_type(anon):
    """cov: C-TR-11"""
    record = _record(anon, "solace")
    for url in [record["cover"]["url"]] + [image["url"] for image in record["gallery"]]:
        served = anon.get(_media_path(url))
        assert served.status_code == 200 and served.content, describe(served)
        assert re.match(r"image/(png|jpeg|webp)", served.headers.get("content-type", "")), served.headers


def test_body_text_meets_the_4_5_contrast_bar_on_both_grounds(page):
    """cov: C-UX-23"""
    for path in ("/works/solace", "/privacy", "/works"):
        _goto(page, path)
        pairs = page.evaluate(_TEXT_COLOURS, "p")
        assert pairs, f"no body text found on {path}"
        worst = min(contrast(_over(front, back), back) for front, back in pairs)
        assert worst >= 4.5, (path, worst)


def test_the_eyebrow_on_the_dark_ground_meets_the_4_5_contrast_bar(page):
    """cov: C-UX-24"""
    _goto(page, "/works")
    eyebrows = page.evaluate(_EYEBROWS, [TITLES[slug].upper() for slug in PUBLISHED])
    assert eyebrows, "no eyebrow found on the works index"
    for eyebrow in eyebrows:
        back = eyebrow["back"]
        assert contrast(_over(eyebrow["color"], back), back) >= 4.5, eyebrow


def test_the_full_width_masthead_renders_inter_at_100px_medium(page):
    """cov: C-UX-25"""
    _goto(page, "/works")
    style = page.evaluate(_MASTHEAD, "Works")
    assert style, "no masthead reading Works"
    assert "inter" in style["family"].lower(), style
    assert style["size"] == "100px" and style["weight"] == "500", style


def test_the_eyebrow_renders_ibm_plex_mono_at_12px_bold(page):
    """cov: C-UX-26"""
    _goto(page, "/works")
    eyebrows = page.evaluate(_EYEBROWS, [TITLES[slug].upper() for slug in PUBLISHED])
    assert eyebrows, "no eyebrow found on the works index"
    for eyebrow in eyebrows:
        assert "plex mono" in eyebrow["family"].lower(), eyebrow
        assert eyebrow["size"] == "12px" and eyebrow["weight"] == "700", eyebrow


def test_the_type_scales_to_nine_tenths_below_the_laptop_breakpoint(tablet_page):
    """cov: C-UX-27"""
    _goto(tablet_page, "/works")
    style = tablet_page.evaluate(_MASTHEAD, "Works")
    assert style and style["size"] == "90px", style
    eyebrows = tablet_page.evaluate(_EYEBROWS, [TITLES[slug].upper() for slug in PUBLISHED])
    assert eyebrows and all(eyebrow["size"] == "10.8px" for eyebrow in eyebrows), eyebrows


def test_the_skip_link_is_the_first_focusable_element_on_every_public_route(page):
    """cov: C-UX-28"""
    for path in PUBLIC_ROUTES:
        _goto(page, path)
        page.keyboard.press("Tab")
        first = page.evaluate(
            "() => { const a = document.activeElement; const href = a && a.getAttribute('href');"
            " return {tag: a ? a.tagName : '', href: href || '',"
            " target: !!(href && href.startsWith('#') && href.length > 1 && document.querySelector(href))}; }")
        assert first["tag"] == "A" and first["target"], (path, first)


def test_nothing_overflows_sideways_at_a_phone_width(phone_page):
    """cov: C-UX-29"""
    for path in PUBLIC_ROUTES + ("/nowhere",):
        _goto(phone_page, path)
        _scroll_through(phone_page)
        widths = phone_page.evaluate(
            "() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        assert widths[0] <= widths[1] + 1, (path, widths)


def test_the_work_label_at_zero_scale_holds_nothing_focusable(page):
    """cov: C-FE-61"""
    _goto(page, "/works")
    focusable = page.evaluate(
        "() => { const label = Array.from(document.querySelectorAll('body *'))"
        ".find(el => el.children.length === 0 && el.textContent.trim().toUpperCase() === 'VIEW');"
        " if (!label) return null; let box = label;"
        " while (box.parentElement && box.parentElement.textContent.trim().toUpperCase() === 'VIEW') box = box.parentElement;"
        " const inner = box.querySelectorAll('a[href], button, input, select, textarea, [tabindex]:not([tabindex=\"-1\"])');"
        " return inner.length + (box.tabIndex >= 0 ? 1 : 0); }")
    assert focusable == 0, f"the work label holds focusable content: {focusable}"


def test_every_image_carries_its_stored_description_as_alternative_text(anon):
    """cov: C-CF-91"""
    record = _record(anon, "solace")
    expected = {norm(record["cover"]["description"])} | {norm(image["description"]) for image in record["gallery"]}
    markup = anon.get("/works/solace").text
    alts = {norm(html_lib.unescape(alt)) for alt in re.findall(r"<img\b[^>]*\balt=[\"']([^\"']*)[\"']", markup, re.I)}
    assert expected <= alts, expected - alts


_DATA_INTEGRITY = "data integrity"


def test_the_services_endpoint_returns_the_five_services_in_order(anon):
    """cov: C-DM-01, C-DC-01"""
    payload = ok(anon.get("/api/services"), "services read")
    assert [row["label"] for row in payload] == list(SERVICES), payload


def test_the_people_endpoint_returns_founders_and_management_then_creative_partners_in_order(anon):
    """cov: C-DM-02, C-DC-02"""
    payload = ok(anon.get("/api/people"), "people read")
    assert [(row["name"], row["group"]) for row in payload] == list(PEOPLE), payload


def test_the_settings_endpoint_returns_the_stored_byline_contact_and_copyright_range(anon, backend):
    """cov: C-DM-03, C-DC-03"""
    payload = ok(anon.get("/api/settings"), "settings read")
    assert payload["byline"] == BYLINE, payload
    assert payload["contact_email"] == CONTACT_EMAIL, payload
    assert (int(payload["copyright_from"]), int(payload["copyright_to"])) == (24, 26), payload
    stored = backend.query("SELECT * FROM settings")
    assert stored and stored[0]["byline"] == BYLINE, stored


def test_every_published_case_study_carries_its_pinned_title_ordinal_and_tagline(anon):
    """cov: C-DM-04, C-DM-05"""
    rows = {row["slug"]: row for row in works(anon)}
    for index, slug in enumerate(PUBLISHED, start=1):
        row = rows[slug]
        assert row["title"] == TITLES[slug], row
        assert int(row["ordinal"]) == index, row
        assert norm(row["tagline"]) == TAGLINES[slug], row


def test_every_published_case_study_carries_its_stored_disciplines_and_year_range(anon):
    """cov: C-DM-06, C-DM-07"""
    rows = {row["slug"]: row for row in works(anon)}
    for slug, expected in DISCIPLINES.items():
        assert list(rows[slug]["disciplines"]) == expected, rows[slug]
    for slug in PUBLISHED:
        row = rows[slug]
        assert all(item in DISCIPLINE_SET for item in row["disciplines"]), row
        assert int(row["year_from"]) <= int(row["year_to"]), row
    assert (int(rows["solace"]["year_from"]), int(rows["solace"]["year_to"])) == (25, 26)


def test_a_case_study_read_returns_brief_concept_credits_cover_and_ordered_gallery(anon):
    """cov: C-DC-06, C-DM-10"""
    for slug in PUBLISHED:
        record = ok(anon.get(f"/api/works/{slug}"), f"{slug} read")
        assert record["brief"].strip(), record
        assert record["concept"].strip().startswith("So"), record["concept"]
        assert isinstance(record["credits"], list) and record["credits"], record
        assert "/media/" in record["cover"]["url"], record["cover"]
        assert len(record["gallery"]) == 4, record["gallery"]
        for image in record["gallery"]:
            assert "/media/" in image["url"] and image["description"].strip(), image
    solace = _record(anon, "solace")
    assert norm(solace["brief"]).startswith("A Swiss specialty coffee house and roaster:")


def test_the_urbana_credit_carries_its_stored_role_before_the_name(anon):
    """cov: C-DM-11"""
    record = _record(anon, "urbana")
    assert {"role": "Motion & development by", "name": "Amelie Ronsard"} in [
        {"role": credit.get("role"), "name": credit.get("name")} for credit in record["credits"]], record
    assert "Motion & development by Amelie Ronsard" in _text(anon.get("/works/urbana").text)


def test_a_case_study_gallery_image_carries_a_layout_from_the_four_layouts(anon):
    """cov: C-DM-12"""
    for slug in PUBLISHED:
        record = ok(anon.get(f"/api/works/{slug}"), f"{slug} read")
        layouts = [image["layout"] for image in record["gallery"]]
        assert all(layout in LAYOUTS for layout in layouts), layouts


def test_a_filed_enquiry_is_stored_as_a_row_carrying_every_submitted_field(anon, backend):
    """cov: C-DC-07, C-DM-13"""
    doc = enquiry_doc(service="Events", time_window="afternoon", message=unique("message"))
    payload = ok(anon.post("/api/enquiries", json=doc), "booking")
    row = backend.one("enquiry", id=payload["id"])
    assert row, f"no enquiry row for {payload}"
    for field in ("name", "email", "company", "service", "time_window", "message"):
        assert row[field] == doc[field], (field, row)
    assert str(row["preferred_date"])[:10] == doc["preferred_date"], row
    assert row["status"] == "new", row


def test_a_visitor_enquiry_is_attached_to_no_account(anon, backend):
    """cov: C-DM-14"""
    payload = ok(anon.post("/api/enquiries", json=enquiry_doc()), "booking")
    row = backend.one("enquiry", id=payload["id"])
    assert row and row["account_id"] is None, row


def test_a_signed_in_reader_enquiry_is_attached_to_the_account_and_listed_as_own(backend):
    """cov: C-CF-36, C-DC-10"""
    session, address = sign_up()
    with session:
        me = ok(session.get("/api/auth/me"), "me read")
        payload = ok(session.post("/api/enquiries", json=enquiry_doc(email=address)), "signed-in booking")
        listed = ok(session.get("/api/enquiries"), "own enquiries")
    row = backend.one("enquiry", id=payload["id"])
    assert row and str(row["account_id"]) == str(me["id"]), row
    assert [item["id"] for item in listed] == [payload["id"]], listed


def test_an_uploaded_cover_is_stored_in_the_object_store_under_the_key_scheme(author, backend, store):
    """cov: C-CF-42, C-CF-43, C-DC-12"""
    work = new_work(author)
    data = png_bytes(unique("cover"))
    media = ok(upload(author, work["id"], data), "cover upload")
    matched = KEY_RE.match(media["storage_key"])
    assert matched, media
    assert matched["work"] == str(work["id"]) and matched["digest"] == sha256_hex(data), media
    assert matched["ext"] == "png", media
    assert store.exists(media["storage_key"]), f"no object at {media['storage_key']}"
    assert backend.one("media", id=media["id"])["storage_key"] == media["storage_key"]


def test_the_stored_key_digest_is_the_sha256_of_the_uploaded_bytes(author):
    """cov: C-CF-44"""
    work = new_work(author)
    data = png_bytes(unique("digest"))
    media = ok(upload(author, work["id"], data), "cover upload")
    assert media["sha256"] == sha256_hex(data), media
    assert media["storage_key"].endswith(f"{sha256_hex(data)}.png"), media
    served = author.get(f"/media/{media['storage_key']}")
    assert served.status_code == 200 and served.content == data, describe(served)


def test_uploading_the_same_bytes_twice_stores_one_object(author, store):
    """cov: C-CF-45"""
    work = new_work(author)
    data = png_bytes(unique("twice"))
    ok(upload(author, work["id"], data, kind="gallery", layout="full-bleed"), "first upload")
    upload(author, work["id"], data, kind="gallery", layout="full-bleed")
    keys = [key for key in store.list(f"works/{work['id']}/") if sha256_hex(data) in key]
    assert len(keys) == 1, keys


def test_removing_an_image_removes_its_object_from_the_store(author, backend, store):
    """cov: C-CF-47"""
    work = new_work(author)
    media = ok(upload(author, work["id"], png_bytes(unique("remove"))), "cover upload")
    assert store.exists(media["storage_key"])
    ok(author.delete(f"/api/works/{work['id']}/media/{media['id']}"), "remove image")
    assert not store.exists(media["storage_key"]), media
    assert backend.one("media", id=media["id"]) is None


def test_a_draft_image_object_still_exists_in_the_store(author, backend, store):
    """cov: C-CF-56"""
    draft = ok(author.get(f"/api/works/{DRAFT_SLUG}"), "draft read")
    stored = set(store.list(f"works/{draft['id']}/"))
    rows = backend.query("SELECT storage_key FROM media WHERE work_id = %s", (draft["id"],))
    assert rows and {row["storage_key"] for row in rows} <= stored, (rows, stored)


def test_unpublishing_keeps_every_stored_object_so_a_republish_needs_no_upload(anon, author, store):
    """cov: C-CF-63"""
    probe, key = _published_probe(author)
    try:
        ok(author.post(f"/api/works/{probe['id']}/unpublish"), "unpublish")
        assert store.exists(key), key
        ok(author.post(f"/api/works/{probe['id']}/publish"), "republish")
        assert anon.get(f"/media/{key}").status_code == 200
    finally:
        author.post(f"/api/works/{probe['id']}/unpublish")


def test_unpublishing_one_case_study_renumbers_no_other_ordinal(anon, author):
    """cov: C-CF-64, C-DM-21"""
    first, _first_key = _published_probe(author)
    second, _second_key = _published_probe(author)
    try:
        before = {row["slug"]: int(row["ordinal"]) for row in works(author)}
        ok(author.post(f"/api/works/{first['id']}/unpublish"), "unpublish")
        after = {row["slug"]: int(row["ordinal"]) for row in works(author)}
        assert after == before, (before, after)
        public = {row["slug"]: int(row["ordinal"]) for row in works(anon)}
        assert public[second["slug"]] == before[second["slug"]], public
    finally:
        author.post(f"/api/works/{first['id']}/unpublish")
        author.post(f"/api/works/{second['id']}/unpublish")


def test_a_published_case_study_ordinal_is_stored_rather_than_derived_from_position(anon, author, backend):
    """cov: C-CF-65"""
    taken = {int(row["ordinal"]) for row in works(author)}
    ordinal = next(n for n in range(97, 9, -1) if n not in taken)
    probe, _key = _published_probe(author, ordinal=ordinal)
    try:
        public = {row["slug"]: int(row["ordinal"]) for row in works(anon)}
        assert public[probe["slug"]] == ordinal, public
        assert backend.one("work", id=probe["id"])["ordinal"] == ordinal
        assert f"W'{ordinal:02d}" in _text(anon.get(f"/works/{probe['slug']}").text)
    finally:
        author.post(f"/api/works/{probe['id']}/unpublish")


def test_the_footer_copyright_range_is_read_from_the_stored_settings(anon, backend):
    """cov: C-FE-58"""
    row = backend.query("SELECT copyright_from, copyright_to FROM settings")[0]
    assert (int(row["copyright_from"]), int(row["copyright_to"])) == (24, 26), row
    for path in ("/", "/works", "/works/solace"):
        assert f"{COPYRIGHT} - Founded by {AUTHOR_NAME}" in _text(anon.get(path).text), path


def test_a_public_page_view_is_stored_as_a_row_with_route_and_time(anon, backend):
    """cov: C-CF-86, C-DM-23"""
    before = backend.count("page_view", route="/privacy")
    started = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=5)
    assert anon.get("/privacy").status_code == 200
    settle()
    rows = backend.query("SELECT route, viewed_at FROM page_view WHERE route = %s ORDER BY viewed_at DESC",
                         ("/privacy",))
    assert len(rows) >= before + 1, (before, len(rows))
    stamp = rows[0]["viewed_at"]
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=datetime.timezone.utc)
    assert stamp >= started, stamp


def test_seeding_twice_leaves_one_row_and_one_object_for_every_seeded_image(author, backend, store):
    """cov: C-TR-10, C-CF-90"""
    for slug in PUBLISHED + (DRAFT_SLUG,):
        record = ok(author.get(f"/api/works/{slug}"), f"{slug} read")
        rows = backend.query("SELECT kind, storage_key FROM media WHERE work_id = %s", (record["id"],))
        kinds = sorted(row["kind"] for row in rows)
        assert kinds == ["cover"] + ["gallery"] * 4, (slug, kinds)
        keys = [row["storage_key"] for row in rows]
        assert len(set(keys)) == len(keys), (slug, keys)
        assert set(store.list(f"works/{record['id']}/")) == set(keys), slug


_AUTHORIZATION = "authorization"


def test_the_works_index_markup_lists_every_published_title_and_no_draft(anon):
    """cov: C-CF-08"""
    response = anon.get("/works")
    assert response.status_code == 200, describe(response)
    for slug in PUBLISHED:
        assert _links_to(response.text, f"/works/{slug}"), f"no card link to {slug}"
    assert not _links_to(response.text, f"/works/{DRAFT_SLUG}"), "the draft is linked"
    assert TITLES[DRAFT_SLUG] not in _text(response.text)


def test_a_wrong_password_and_an_unknown_address_answer_the_same_message(anon):
    """cov: C-CF-33"""
    wrong = anon.post("/api/auth/sign-in", json={"email": READER_EMAIL, "password": "wrong-password-1"})
    unknown = anon.post("/api/auth/sign-in", json={"email": f"{unique()}@example.com", "password": PASSWORD})
    refused(wrong, "a wrong password")
    refused(unknown, "an unknown address")
    assert body(wrong).get("error") == "That email and password do not match", describe(wrong)
    assert body(unknown).get("error") == body(wrong).get("error"), describe(unknown)


def test_signing_out_revokes_the_bearer_token():
    """cov: C-TR-01"""
    session, _address = sign_up()
    with session:
        ok(session.get("/api/auth/me"), "me before sign out")
        ok(session.post("/api/auth/sign-out"), "sign out")
        refused(session.get("/api/auth/me"), "me after sign out")


def test_sign_in_returns_a_token_and_sets_an_http_only_session_cookie(anon):
    """cov: C-TR-02"""
    response = anon.post("/api/auth/sign-in", json={"email": READER_EMAIL, "password": PASSWORD})
    payload = ok(response, "sign in")
    assert payload.get("token"), payload
    cookies = response.headers.get_list("set-cookie")
    assert any("httponly" in cookie.lower() for cookie in cookies), cookies


def test_a_reader_listing_enquiries_never_sees_another_readers_enquiry(reader, reader2, backend):
    """cov: C-RL-04, C-DM-17"""
    other = ok(reader2.post("/api/enquiries", json=enquiry_doc(email=READER2_EMAIL)), "reader2 booking")
    me = ok(reader.get("/api/auth/me"), "reader me")
    listed = ok(reader.get("/api/enquiries"), "reader enquiries")
    assert other["id"] not in [item["id"] for item in listed], listed
    for item in listed:
        row = backend.one("enquiry", id=item["id"])
        assert str(row["account_id"]) == str(me["id"]), row


def test_a_reader_asking_for_another_readers_enquiry_is_answered_as_missing(reader, reader2):
    """cov: C-RL-05"""
    other = ok(reader2.post("/api/enquiries", json=enquiry_doc(email=READER2_EMAIL)), "reader2 booking")
    missing(reader.get(f"/api/enquiries/{other['id']}"), "another reader's enquiry")
    ok(reader2.get(f"/api/enquiries/{other['id']}"), "the owner's own enquiry")


def test_a_reader_cannot_change_any_enquiry_status(reader, reader2, backend):
    """cov: C-RL-06, C-RL-07"""
    own = ok(reader.post("/api/enquiries", json=enquiry_doc(email=READER_EMAIL)), "reader booking")
    other = ok(reader2.post("/api/enquiries", json=enquiry_doc(email=READER2_EMAIL)), "reader2 booking")
    for target in (own, other):
        refused(reader.patch(f"/api/enquiries/{target['id']}", json={"status": "contacted"}),
                "a reader changing a status")
        assert backend.one("enquiry", id=target["id"])["status"] == "new"


def test_a_reader_cannot_create_publish_or_upload_a_case_study(author, reader, backend):
    """cov: C-RL-08"""
    before = backend.count("work")
    refused(reader.post("/api/works", json={"slug": unique("probe"), "title": "Nope", "ordinal": 98,
                                            "year_from": 25, "year_to": 26, "disciplines": ["Branding"],
                                            "tagline": "Nope.", "brief": "Nope.", "concept": "So nope.",
                                            "credits": []}), "a reader creating a case study")
    assert backend.count("work") == before
    draft = ok(author.get(f"/api/works/{DRAFT_SLUG}"), "draft read")
    refused(reader.post(f"/api/works/{draft['id']}/publish"), "a reader publishing")
    assert ok(author.get(f"/api/works/{DRAFT_SLUG}"), "draft read")["published"] is False
    media_before = backend.count("media")
    refused(upload(reader, draft["id"], png_bytes(unique())), "a reader uploading")
    assert backend.count("media") == media_before


def test_the_studio_route_answers_404_to_a_reader_and_redirects_a_visitor_to_sign_in(anon, reader):
    """cov: C-UF-13, C-UF-14"""
    response = anon.get("/studio")
    assert response.status_code in (301, 302, 303, 307, 308), describe(response)
    location = urllib.parse.unquote(response.headers.get("location", ""))
    assert location.endswith("/sign-in?next=/studio"), location
    with _cookie_session(READER_EMAIL) as session:
        for path in ("/studio", "/studio/enquiries"):
            missing(session.get(path), f"a reader asking for {path}")


def test_no_route_grants_the_author_role_on_sign_up(anon, backend):
    """cov: C-RL-09"""
    address = f"{unique('climber')}@example.com"
    response = anon.post("/api/auth/sign-up", json={
        "display_name": "Climber", "email": address, "password": PASSWORD, "role": "author"})
    if response.status_code in OK:
        assert body(response)["role"] == "reader", describe(response)
    for row in backend.rows("account", email=address):
        assert row["role"] == "reader", row


def test_a_visitor_with_no_account_cannot_read_any_enquiry(anon):
    """cov: C-RL-10"""
    refused(anon.get("/api/enquiries"), "a visitor listing enquiries")
    filed = ok(anon.post("/api/enquiries", json=enquiry_doc()), "booking")
    assert anon.get(f"/api/enquiries/{filed['id']}").status_code in REFUSED


def test_the_draft_route_answers_404_to_a_visitor_and_to_a_reader(anon):
    """cov: C-CF-52, C-UF-17"""
    response = anon.get(f"/works/{DRAFT_SLUG}")
    missing(response, "the draft route for a visitor")
    assert title_of(response.text) == NOT_FOUND_TITLE, title_of(response.text)
    with _cookie_session(READER_EMAIL) as session:
        missing(session.get(f"/works/{DRAFT_SLUG}"), "the draft route for a reader")


def test_the_draft_record_answers_404_and_is_absent_from_the_works_read(anon, reader):
    """cov: C-CF-53, C-CF-54"""
    missing(anon.get(f"/api/works/{DRAFT_SLUG}"), "the draft record for a visitor")
    missing(reader.get(f"/api/works/{DRAFT_SLUG}"), "the draft record for a reader")
    for session in (anon, reader):
        assert DRAFT_SLUG not in [row["slug"] for row in works(session)]


def test_a_draft_image_answers_404_by_its_exact_storage_key_to_a_visitor_and_a_reader(anon, author, reader, store):
    """cov: C-CF-55, C-TR-04"""
    keys = _draft_keys(author)
    assert len(keys) == 5, keys
    with _cookie_session(READER_EMAIL) as cookie_reader:
        for key in keys:
            assert store.exists(key), f"the draft object {key} is absent from the store"
            missing(anon.get(f"/media/{key}"), f"the draft image {key} for a visitor")
            missing(reader.get(f"/media/{key}"), f"the draft image {key} for a bearer reader")
            missing(cookie_reader.get(f"/media/{key}"), f"the draft image {key} for a cookie reader")


def test_the_object_store_refuses_an_anonymous_read_of_any_image(anon):
    """cov: C-CF-58, C-TR-05"""
    record = _record(anon, "solace")
    key = _media_path(record["cover"]["url"])[len("/media/"):]
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    bucket = os.environ["STORAGE_BUCKET"]
    with httpx.Client(timeout=TIMEOUT) as direct:
        response = direct.get(f"{endpoint}/{bucket}/{key}")
    assert response.status_code in (401, 403), describe(response)


def test_the_draft_never_appears_in_any_next_subject_row_or_compact_list(anon):
    """cov: C-CF-59"""
    for slug in PUBLISHED:
        markup = anon.get(f"/works/{slug}").text
        assert not _links_to(markup, f"/works/{DRAFT_SLUG}"), slug
        assert TITLES[DRAFT_SLUG] not in _text(markup), slug


def test_the_draft_never_appears_in_the_home_route_featured_rail(anon, author):
    """cov: C-DM-20"""
    draft = ok(author.get(f"/api/works/{DRAFT_SLUG}"), "draft read")
    ok(author.patch(f"/api/works/{draft['id']}", json={"featured": True}), "feature the draft")
    try:
        home = anon.get("/").text
        assert not _links_to(home, f"/works/{DRAFT_SLUG}"), "the draft sits in the rail"
        assert DRAFT_SLUG not in [row["slug"] for row in works(anon, featured="true")]
    finally:
        author.patch(f"/api/works/{draft['id']}", json={"featured": bool(draft["featured"])})


def test_unpublishing_withdraws_the_route_the_record_and_every_image(anon, author):
    """cov: C-CF-62, C-DC-16"""
    probe, key = _published_probe(author)
    assert anon.get(f"/works/{probe['slug']}").status_code == 200
    assert anon.get(f"/media/{key}").status_code == 200
    payload = ok(author.post(f"/api/works/{probe['id']}/unpublish"), "unpublish")
    assert payload["published"] is False, payload
    missing(anon.get(f"/works/{probe['slug']}"), "a withdrawn route")
    missing(anon.get(f"/api/works/{probe['slug']}"), "a withdrawn record")
    missing(anon.get(f"/media/{key}"), "a withdrawn image")


def test_an_author_cannot_delete_an_enquiry(anon, author, backend):
    """cov: C-RL-12"""
    filed = ok(anon.post("/api/enquiries", json=enquiry_doc()), "booking")
    response = author.delete(f"/api/enquiries/{filed['id']}")
    assert response.status_code in REFUSED, describe(response)
    assert backend.one("enquiry", id=filed["id"]) is not None


def test_the_page_view_record_carries_nothing_identifying_a_visitor(backend):
    """cov: C-CF-87"""
    columns = {row["column_name"] for row in backend.query(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'page_view'")}
    assert {"route", "viewed_at"} <= columns, columns
    for column in columns:
        assert not re.search(r"ip|agent|session|account|user|cookie|referr|visitor|fingerprint", column), columns


def test_only_an_author_reads_the_page_view_record_filtered_by_route(anon, author, reader, page):
    """cov: C-CF-88, C-RL-13"""
    anon.get("/works")
    settle()
    refused(anon.get("/api/page-views", params={"route": "/works"}), "a visitor reading page views")
    refused(reader.get("/api/page-views", params={"route": "/works"}), "a reader reading page views")
    rows = ok(author.get("/api/page-views", params={"route": "/works"}), "author page views")
    assert rows and all(row["route"] == "/works" and row["viewed_at"] for row in rows), rows[:5]


def test_no_public_route_loads_third_party_analytics_or_a_consent_banner(page):
    """cov: C-CF-89"""
    hosts = set()
    page.on("request", lambda request: hosts.add(urllib.parse.urlparse(request.url).netloc))
    for path in PUBLIC_ROUTES:
        _goto(page, path)
        text = page.evaluate("() => document.body.innerText").lower()
        assert "accept cookies" not in text and "cookie consent" not in text, path
    trackers = [host for host in hosts if re.search(
        r"google-analytics|googletagmanager|doubleclick|plausible|segment|hotjar|mixpanel|clarity\.ms|facebook", host)]
    assert trackers == [], trackers


_EDGE_CASES = "edge cases"


def test_an_enquiry_email_is_trimmed_and_lowercased_when_stored(anon, backend):
    """cov: C-CF-20"""
    address = f"{unique('Mixed')}@Example.COM"
    payload = ok(anon.post("/api/enquiries", json=enquiry_doc(email=f"  {address}  ")), "booking")
    row = backend.one("enquiry", id=payload["id"])
    assert row["email"] == address.lower(), row


def test_an_enquiry_with_an_empty_name_is_refused_and_files_nothing(anon, backend):
    """cov: C-CF-25"""
    before = backend.count("enquiry")
    for name in ("   ", "n" * 81):
        response = anon.post("/api/enquiries", json=enquiry_doc(name=name))
        refused(response, f"a booking named {name[:5]!r}")
        assert body(response).get("field") == "name", describe(response)
    assert norm(body(anon.post("/api/enquiries", json=enquiry_doc(name=""))).get("error")) == "Tell us your name"
    assert backend.count("enquiry") == before


def test_an_enquiry_with_a_service_outside_the_five_is_refused_as_invalid(anon):
    """cov: C-CF-26, C-DM-15"""
    response = anon.post("/api/enquiries", json=enquiry_doc(service="Consulting"))
    refused(response, "a booking for an unknown service")
    assert body(response).get("error") == "Pick what you have in mind", describe(response)
    for label in SERVICES:
        ok(anon.post("/api/enquiries", json=enquiry_doc(service=label)), f"booking for {label}")


def test_an_enquiry_with_a_past_preferred_date_is_refused(anon):
    """cov: C-CF-27"""
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    response = anon.post("/api/enquiries", json=enquiry_doc(preferred_date=yesterday))
    refused(response, "a booking for yesterday")
    assert body(response).get("error") == "Pick a date from today on", describe(response)
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    ok(anon.post("/api/enquiries", json=enquiry_doc(preferred_date=tomorrow)), "a booking for tomorrow")


def test_an_enquiry_with_a_time_window_other_than_morning_or_afternoon_is_refused(anon):
    """cov: C-CF-28"""
    response = anon.post("/api/enquiries", json=enquiry_doc(time_window="evening"))
    refused(response, "an evening booking")
    assert body(response).get("error") == "Pick a time of day", describe(response)
    ok(anon.post("/api/enquiries", json=enquiry_doc(time_window="afternoon")), "an afternoon booking")


def test_an_enquiry_message_longer_than_one_thousand_characters_is_refused(anon):
    """cov: C-CF-29, C-DM-16"""
    response = anon.post("/api/enquiries", json=enquiry_doc(message="m" * 1001))
    refused(response, "a booking message of 1001 characters")
    assert body(response).get("error") == "Say a little about the project", describe(response)
    ok(anon.post("/api/enquiries", json=enquiry_doc(message="m" * 1000)), "a booking message of 1000")


def test_an_enquiry_company_longer_than_eighty_characters_is_refused(anon):
    """cov: C-CF-30"""
    response = anon.post("/api/enquiries", json=enquiry_doc(company="c" * 81))
    refused(response, "a company of 81 characters")
    assert body(response).get("error") == "That company name is too long", describe(response)
    ok(anon.post("/api/enquiries", json=enquiry_doc(company="")), "a booking with no company")


def test_a_refused_enquiry_names_the_field_at_fault_in_the_error_body(anon):
    """cov: C-DC-08"""
    response = anon.post("/api/enquiries", json=enquiry_doc(email="not-an-address"))
    refused(response, "a booking with an invalid email")
    payload = body(response)
    assert payload.get("error") == "We need an email to reply to", payload
    assert payload.get("field") == "email", payload
    missing_message = anon.post("/api/enquiries", json=enquiry_doc(message="  "))
    refused(missing_message, "a booking with a blank message")
    assert body(missing_message).get("field") == "message", describe(missing_message)


def test_signing_up_on_an_address_already_registered_answers_that_email_is_already_registered(anon):
    """cov: C-CF-32"""
    response = anon.post("/api/auth/sign-up", json={
        "display_name": "Second Paolo", "email": READER_EMAIL, "password": PASSWORD})
    refused(response, "a second sign up on a registered address")
    assert body(response).get("error") == "That email is already registered", describe(response)


def test_a_display_name_longer_than_sixty_characters_is_refused(anon):
    """cov: C-CF-34"""
    response = anon.post("/api/auth/sign-up", json={
        "display_name": "d" * 61, "email": f"{unique()}@example.com", "password": PASSWORD})
    refused(response, "a display name of 61 characters")
    ok(anon.post("/api/auth/sign-up", json={
        "display_name": "d" * 60, "email": f"{unique()}@example.com", "password": PASSWORD}),
       "a display name of 60 characters")


def test_a_password_shorter_than_eight_characters_is_refused(anon):
    """cov: C-CF-35"""
    response = anon.post("/api/auth/sign-up", json={
        "display_name": "Short", "email": f"{unique()}@example.com", "password": "p" * 7})
    refused(response, "a password of 7 characters")
    ok(anon.post("/api/auth/sign-up", json={
        "display_name": "Short", "email": f"{unique()}@example.com", "password": "p" * 8}),
       "a password of 8 characters")


def test_an_upload_that_is_not_an_image_is_refused_as_invalid(author, store):
    """cov: C-TR-03"""
    work = new_work(author)
    response = author.post(f"/api/works/{work['id']}/media",
                           data={"kind": "cover", "description": "A text file"},
                           files={"file": ("notes.txt", b"plain words", "text/plain")})
    refused(response, "a text upload")
    assert store.list(f"works/{work['id']}/") == []


def test_an_upload_without_a_description_is_refused(author, store):
    """cov: C-DM-18"""
    work = new_work(author)
    refused(upload(author, work["id"], png_bytes(unique()), description=""), "an upload with no description")
    refused(upload(author, work["id"], png_bytes(unique()), description="d" * 201), "a description of 201")
    assert store.list(f"works/{work['id']}/") == []


def test_a_slug_or_ordinal_already_in_use_is_refused_with_409(author):
    """cov: C-DM-19, C-DC-14"""
    base = {"title": "Clash", "year_from": 25, "year_to": 26, "disciplines": ["Branding"],
            "tagline": "A clash.", "brief": "A clash.", "concept": "So a clash.", "credits": []}
    taken_slug = author.post("/api/works", json=dict(base, slug="solace", ordinal=free_ordinal(author)))
    assert taken_slug.status_code == 409, describe(taken_slug)
    taken_ordinal = author.post("/api/works", json=dict(base, slug=unique("probe"), ordinal=1))
    assert taken_ordinal.status_code == 409, describe(taken_ordinal)


def test_an_enquiry_status_outside_new_contacted_closed_is_refused(anon, author, backend):
    """cov: C-DM-22"""
    filed = ok(anon.post("/api/enquiries", json=enquiry_doc()), "booking")
    refused(author.patch(f"/api/enquiries/{filed['id']}", json={"status": "archived"}), "status archived")
    assert backend.one("enquiry", id=filed["id"])["status"] == "new"
