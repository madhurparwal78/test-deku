from __future__ import annotations

import os
import re
import threading
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import httpx

import conftest as fx


def test_health_route_answers_ready():
    """The health route answers once the app is ready."""
    response = httpx.get(f"{fx.api_base()}/health", timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code} rather than 200: {response.text[:300]}"
    )


def test_app_serves_pages_and_api_on_one_origin():
    """The home page and the API answer on one origin with the frame, landmarks and no forms."""
    home = fx.fetch("/")
    assert home.status_code == 200, (
        f"GET / at {fx.app_url()} returned {home.status_code}: {home.text[:300]}"
    )
    assert fx.api_base().startswith(fx.app_url()), (
        f"the API base {fx.api_base()} is not on the origin {fx.app_url()}"
    )
    for route in ("/", "/ndrive"):
        cookies = fx.set_cookies(fx.fetch(route))
        assert not cookies, f"{route} sets a cookie before any passcode: {cookies}"
    markup = home.text
    assert re.search(r"data-page=[\"']home[\"']", markup), (
        "the home page root carries no data-page attribute set to home"
    )
    for label in ("atlas", ".design", "Work", "Contact", fx.THEME_LABEL, fx.SOUND_LABEL_OPEN):
        assert fx.contains(markup, label), f"the server-rendered home page does not show {label!r}"
    title = re.search(r"<title[^>]*>(.*?)</title>", markup, re.S | re.I)
    assert title and re.fullmatch(r"atlas\s*(\u00a9|&copy;|&#169;)\s*\d{4}", title.group(1).strip()), (
        f"the home document title is {title.group(1) if title else None!r}"
    )
    tags = fx.parse(markup).tags
    names = {tag for tag, _ in tags}
    roles = {attrs.get("role") for _, attrs in tags}
    assert "header" in names or "banner" in roles, "the home page carries no banner landmark"
    assert "main" in names or "main" in roles, "the home page carries no main landmark"
    assert "footer" in names or "contentinfo" in roles, "the home page carries no contentinfo landmark"
    for route in ("/", "/ndrive"):
        page = fx.fetch(route).text
        page_tags = fx.parse(page).tags
        assert not any(tag in ("form", "textarea") for tag, _ in page_tags), (
            f"{route} carries a form, but the site offers no comment, newsletter or contact form"
        )
        assert not any(tag == "input" and attrs.get("type") in ("search", "email", "password")
                       for tag, attrs in page_tags), (
            f"{route} carries a search, email or password input"
        )
    assert "sign up" not in fx.page_text(markup).lower(), "the home page offers a sign-up"


def test_user_readme_states_the_passcodes():
    """The credential file names both gated paths beside their seeded passcodes."""
    with open("/app/USER_README.md", encoding="utf-8") as handle:
        text = handle.read()
    assert re.search(r"\bno\b[^.\n]{0,40}\baccounts?\b|\baccounts?\W+none\b", text, re.I), (
        "/app/USER_README.md does not state that there are no login accounts"
    )
    for value in (fx.STUDIO_PATH, fx.STUDIO_CODE, fx.GATED_PATH, fx.GATED_CODE):
        assert value in text, f"/app/USER_README.md does not carry {value}"


def test_reserved_directories_exist_and_are_empty():
    """The two reserved directories exist at the app root and hold nothing."""
    for name in (".browser_screenshots", ".downloads"):
        path = os.path.join("/app", name)
        assert os.path.isdir(path), f"/app/{name} does not exist at the app root"
        assert os.listdir(path) == [], f"/app/{name} is not empty: {os.listdir(path)}"


def test_site_profile_carries_the_copy_deck():
    """The site profile returns the owner's pinned copy and socials."""
    response = fx.api("/site")
    assert response.status_code == 200, (
        f"GET /api/site returned {response.status_code}: {response.text[:300]}"
    )
    site = response.json()
    expected = {"brand": "atlas", "brand_suffix": ".design", "person": "Rin Alvez",
                "contact_email": fx.CONTACT_EMAIL, "timezone_label": "GMT+8",
                "region_code": "CN", "redaction_length": 6}
    for key, value in expected.items():
        assert site.get(key) == value, (
            f"GET /api/site reports {key}={site.get(key)!r}, expected {value!r}"
        )
    for line in fx.DISCIPLINE_LINES:
        assert line in str(site.get("discipline_label")), (
            f"discipline_label {site.get('discipline_label')!r} lacks {line!r}"
        )
    for line in fx.TAGLINE_LINES:
        assert line in str(site.get("tagline")), f"tagline {site.get('tagline')!r} lacks {line!r}"
    assert "Rin Alvez" in str(site.get("introduction")), (
        f"introduction {str(site.get('introduction'))[:120]!r} does not name the owner"
    )
    socials = site.get("socials") or []
    labels = [social.get("label") for social in socials]
    assert labels == list(fx.SOCIAL_LABELS), (
        f"GET /api/site lists socials {labels}, expected {list(fx.SOCIAL_LABELS)}"
    )
    assert [social.get("url") for social in socials] == list(fx.SOCIAL_URLS), (
        f"the social links point at {[social.get('url') for social in socials]}"
    )


def test_home_page_renders_the_copy_deck_server_side():
    """The home page HTML already carries every pinned band string and hook before scripts run."""
    home = fx.fetch("/")
    assert home.status_code == 200, f"GET / returned {home.status_code}"
    markup = home.text
    wanted = (fx.HEADLINE_LINES + fx.HELD_WORDS + fx.CONTACT_WORDS + fx.DISCIPLINE_LINES
              + fx.TAGLINE_LINES + fx.SOCIAL_LABELS
              + (fx.PRIMARY_STATEMENT, fx.CONTACT_EMAIL, fx.SELECTED_WORK))
    for phrase in wanted:
        folded = fx.squash(fx.page_text(markup)).replace("’", "'")
        assert fx.squash(phrase) in folded, f"the server-rendered home page does not carry {phrase!r}"
    for anchor in ("selected-work", "contact"):
        assert re.search(rf"id=[\"']{anchor}[\"']", markup), (
            f"the home page carries no element with id {anchor!r}"
        )
    for band in fx.HOME_BANDS:
        assert re.search(rf"data-band=[\"']{band}[\"']", markup), f"no home band carries data-band={band!r}"
    assert len(re.findall(r"<h1\b", markup, re.I)) == 1, (
        "the home page does not carry exactly one level-one heading"
    )
    redacted = re.search(r"<[^>]*data-redacted[^>]*>", markup)
    assert redacted, "the introduction carries no element marked data-redacted"
    nearby = markup[max(0, redacted.start() - 800):redacted.start() + 800]
    assert "redacted" in fx.page_text(nearby).lower() \
        or re.search(r"aria-label=[\"'][^\"']*redacted", nearby, re.I), (
        "the redaction run is not announced as redacted"
    )
    assert re.search(r"href=[\"']mailto:" + re.escape(fx.CONTACT_EMAIL), markup), (
        "the contact mail link does not use a mailto address"
    )
    for phrase in (fx.SECONDARY_STATEMENT, fx.INTRO_HEAD, fx.INTRO_TAIL):
        assert fx.squash(phrase) in fx.squash(fx.page_text(markup)).replace("\u2019", "'"), (
            f"the home page does not carry {phrase!r}"
        )
    hrefs = {href for href, _ in fx.local_hrefs(markup)}
    for target in ("/kindling", "/ndrive", "/teamharbor"):
        assert target in hrefs, f"the home page links nowhere to {target}"


def test_home_page_loads_no_binary_asset():
    """The home page references no image, audio, model or analytics asset of its own."""
    home = fx.fetch("/")
    markup = home.text
    references = set(re.findall(r"(?:src|href)=[\"']([^\"']+)[\"']", markup))
    styles = [ref for ref in references if ref.split("?")[0].endswith(".css")]
    sources = [markup]
    for ref in styles:
        if ref.startswith("/") and not ref.startswith("//"):
            sources.append(fx.fetch(ref).text)
    references |= {url for blob in sources for url in re.findall(r"url\(\s*['\"]?([^'\")]+)", blob)}
    banned = sorted(ref for ref in references
                    if ref.split("?")[0].lower().endswith(fx.BINARY_EXTENSIONS)
                    and not ref.startswith("/api/figures/"))
    assert not banned, f"the home page loads binary asset files: {banned[:6]}"
    fonts = {os.path.splitext(ref.split("?")[0].lower())[1] for ref in references
             if ref.split("?")[0].lower().endswith(fx.WEB_FONT_EXTENSIONS)}
    assert len(fonts) <= 1, f"the home page ships more than one web font format: {fonts}"
    joined = " ".join(sources).lower()
    for host in fx.ANALYTICS_HOSTS:
        assert host not in joined, f"the home page loads third-party analytics from {host}"


def test_chrome_controls_are_buttons():
    """Work, Contact, the theme control and the sound control are real buttons."""
    buttons = [fx.squash(text) for text in fx.parse(fx.fetch("/").text).buttons]
    for label in ("Work", "Contact", fx.THEME_LABEL, fx.SOUND_LABEL_OPEN):
        assert any(fx.squash(label) in text for text in buttons), (
            f"no button on the home page reads {label!r}; buttons read {buttons[:10]}"
        )


def test_seeded_rows_exist_once_with_hashed_passcodes(backend):
    """Every seeded row exists exactly once and the passcodes are stored only as hashes."""
    for slug in fx.SEEDED_SLUGS:
        count = backend.count("case_study", slug=slug)
        assert count == 1, f"case_study holds {count} rows with slug {slug!r}, expected one"
    statuses = {row["status"] for row in backend.query("SELECT DISTINCT status FROM case_study")}
    assert statuses <= set(fx.STATUSES), f"case_study carries statuses outside the three: {statuses}"
    assert backend.one("case_study", slug=fx.DRAFT_SLUG)["status"] == "draft", (
        f"the seeded {fx.DRAFT_SLUG!r} case study is not a draft"
    )
    assert backend.one("case_study", slug=fx.STUB_SLUG)["status"] == "stub", (
        f"the seeded {fx.STUB_SLUG!r} case study is not a stub"
    )
    doubled = backend.query(
        "SELECT case_study_id, count(*) AS n FROM project_card "
        "WHERE case_study_id IS NOT NULL GROUP BY case_study_id HAVING count(*) > 1"
    )
    assert not doubled, f"a case study owns more than one project_card row: {doubled}"
    gates = backend.rows("passcode_gate")
    assert sorted(row["path"] for row in gates) == sorted([fx.GATED_PATH, fx.STUDIO_PATH]), (
        f"passcode_gate holds {[row['path'] for row in gates]}, expected the two gated paths"
    )
    for row in gates:
        stored = str(row.get("code_hash") or "").strip()
        assert stored not in (fx.STUDIO_CODE, fx.GATED_CODE) and not re.fullmatch(r"\d{4}", stored), (
            f"passcode_gate stores a plain passcode for {row['path']}"
        )
        assert len(stored) > 8, f"passcode_gate stores no real hash for {row['path']}: {stored!r}"
    for card in fx.SEEDED_CARDS:
        if card["external_url"]:
            count = backend.count("project_card", external_url=card["external_url"])
            assert count == 1, (
                f"project_card holds {count} rows for {card['title']!r}, expected one"
            )


def test_projects_list_the_ten_seeded_cards_in_order():
    """The listing returns the ten seeded cards in order with their recorded placements."""
    cards = fx.listed_cards()
    orders = [card.get("sort_order") for card in cards]
    assert orders == sorted(orders), f"GET /api/projects is not ordered by position: {orders}"
    for card in cards:
        missing = [field for field in fx.CARD_FIELDS if field not in card]
        assert not missing, f"a listed card lacks {missing}: {card}"
        if card.get("external_url"):
            assert card["external_url"].startswith("https://www.example.com/"), (
                f"outside card {card.get('title')!r} points off the example addresses"
            )
    seeded = [card for card in cards if isinstance(card.get("sort_order"), int)
              and card["sort_order"] <= 10]
    assert [card["sort_order"] for card in seeded] == list(range(1, 11)), (
        f"the listing holds positions {[card['sort_order'] for card in seeded]}, expected 1 to 10"
    )
    for got, want in zip(seeded, fx.SEEDED_CARDS):
        assert str(got.get("title", "")).startswith(want["title"]), (
            f"position {want['sort_order']} holds {got.get('title')!r}, expected {want['title']!r}"
        )
        for field in ("slug", "external_url", "eyebrow", "year_label", "kind", "aspect_ratio",
                      "column_start", "column_span", "column_start_lg", "column_span_lg"):
            assert got.get(field) == want[field], (
                f"{want['title']} reports {field}={got.get(field)!r}, expected {want[field]!r}"
            )


def test_project_media_descriptions_are_present_and_not_titles():
    """Every listed card describes its media in words other than its title."""
    for card in fx.listed_cards():
        alt = str(card.get("media_alt") or "").strip()
        assert alt, f"card {card.get('title')!r} has an empty media description"
        assert alt.lower() != str(card.get("title", "")).strip().lower(), (
            f"card {card.get('title')!r} repeats its title as its media description"
        )


def test_home_index_cards_carry_their_order_attribute():
    """The home index container and each card carry their pinned hooks."""
    markup = fx.fetch("/").text
    assert "data-index-grid" in markup, "the home page carries no data-index-grid container"
    orders = set(re.findall(r"<article\b[^>]*data-order=[\"'](\d+)[\"']", markup))
    for position in range(1, 11):
        assert str(position) in orders, f"no card article carries data-order={position}"
    hrefs = {href for href, _ in fx.local_hrefs(markup)}
    for card in fx.SEEDED_CARDS:
        target = card["external_url"] or f"/{card['slug']}"
        assert target in hrefs, f"no card link on the home page leads to {target}"
    outside = [attrs for tag, attrs in fx.parse(markup).tags
               if tag == "a" and attrs.get("href", "").startswith("https://www.example.com/plugins/")]
    assert outside and all(attrs.get("target") == "_blank" for attrs in outside), (
        "an outside card does not open in a new browsing context"
    )


def test_index_cards_start_on_their_recorded_columns(page, app_base):
    """At the widest layout each seeded card, and a newly published card, starts on its recorded column."""
    measure = """() => Array.from(document.querySelectorAll('[data-index-grid] article[data-order]'))
        .map(el => { const r = el.getBoundingClientRect();
                     return {order: Number(el.dataset.order), left: r.left, width: r.width}; })"""
    position = fx.free_position()
    with fx.client_with(fx.studio_cookie()) as studio:
        probe = fx.create_case_study(studio, card=fx.card_payload(
            position, column_start=9, column_span=4, column_start_lg=9, column_span_lg=4))
        try:
            assert fx.transition(studio, probe["id"], "publish").status_code in (200, 201), (
                "the probe card could not be published"
            )
            page.set_viewport_size(fx.WIDEST_VIEWPORT)
            page.goto(f"{app_base}/")
            page.wait_for_selector(f"[data-index-grid] article[data-order='{position}']", state="attached")
            by_order = {box["order"]: box for box in page.evaluate(measure)}
            first, second = by_order.get(1), by_order.get(2)
            assert first and second, f"the rendered index lacks the first two cards: {sorted(by_order)[:12]}"
            column = first["width"] / 8
            origin = second["left"]
            measured = []
            for order in list(range(1, 11)) + [position]:
                box = by_order.get(order)
                assert box, f"the rendered index lacks the card at position {order}"
                measured.append(round((box["left"] - origin) / column) + 1)
            assert tuple(measured[:10]) == fx.WIDEST_COLUMN_STARTS, (
                f"the seeded cards start on columns {measured[:10]}, expected {list(fx.WIDEST_COLUMN_STARTS)}"
            )
            assert measured[10] == 9, (
                f"a card published with column_start 9 renders on column {measured[10]}"
            )
        finally:
            fx.transition(studio, probe["id"], "hold")


def test_draft_card_is_unlisted_everywhere():
    """The seeded draft and the gated article never appear in the index."""
    cards = fx.listed_cards()
    slugs = {card.get("slug") for card in cards}
    assert fx.DRAFT_SLUG not in slugs, "GET /api/projects lists the seeded draft"
    assert fx.FIELD_NOTES_SLUG not in slugs, "GET /api/projects lists the gated article"
    titles = {card.get("title") for card in cards}
    assert fx.DRAFT_TITLE not in titles, "GET /api/projects lists the draft title"
    text = fx.page_text(fx.fetch("/").text)
    assert fx.DRAFT_TITLE not in text, "the home page shows the draft title"
    assert f"/{fx.DRAFT_SLUG}" not in {href for href, _ in fx.parse(fx.fetch('/').text).anchors}, (
        "the home page links to the draft"
    )


def test_published_case_study_reads_with_derived_fields():
    """The nDrive read carries its derived fields and its nine pinned headings."""
    response = fx.api("/case-studies/ndrive")
    assert response.status_code == 200, (
        f"GET /api/case-studies/ndrive returned {response.status_code}: {response.text[:300]}"
    )
    study = response.json()
    expected = {"status": "published", "dimensions": "1440x900", "last_updated": "2026-01-15",
                "last_updated_label": "Jan 15, 2026", "year_label": "2020-2022",
                "composed_width": 1440, "composed_height": 900}
    for key, value in expected.items():
        assert study.get(key) == value, f"nDrive reports {key}={study.get(key)!r}, expected {value!r}"
    headings = [(h.get("level"), h.get("text"), h.get("slug")) for h in study.get("headings") or []]
    assert headings == list(fx.NDRIVE_HEADINGS), (
        f"nDrive lists headings {headings}, expected {list(fx.NDRIVE_HEADINGS)}"
    )
    body = str(study.get("body", ""))
    count = len(body.replace("\r", "").replace("\n", ""))
    assert study.get("character_count") == count, (
        f"nDrive reports character_count {study.get('character_count')}, the body holds {count}"
    )
    assert study.get("character_label") == f"{count:,}", (
        f"nDrive reports character_label {study.get('character_label')!r}, expected {count:,}"
    )


def test_case_study_page_renders_heading_anchors_and_footer():
    """The nDrive page carries every heading id, one level-one heading, the rail, the drawer and the footer."""
    response = fx.fetch("/ndrive")
    assert response.status_code == 200, f"GET /ndrive returned {response.status_code}"
    markup = response.text
    assert re.search(r"data-page=[\"']case-study[\"']", markup), (
        "the nDrive page root carries no data-page attribute set to case-study"
    )
    for _, _, slug in fx.NDRIVE_HEADINGS:
        assert re.search(rf"id=[\"']{slug}[\"']", markup), f"no heading on /ndrive carries id {slug!r}"
    assert len(re.findall(r"<h1\b", markup, re.I)) == 1, "the nDrive page does not carry exactly one h1"
    title = re.search(r"<title[^>]*>(.*?)</title>", markup, re.S | re.I)
    assert title and "ndrive" in fx.squash(title.group(1)), (
        f"the nDrive document title is {title.group(1) if title else None!r}"
    )
    for term in fx.FOOTER_TERMS + ("1440x900", "Jan 15, 2026", "nDrive"):
        assert fx.contains(markup, term), f"the nDrive page does not show {term!r}"
    assert "data-reading-rail" in markup, "the nDrive page carries no data-reading-rail element"
    assert fx.named_navigation(markup, "Contents"), (
        "the nDrive page carries no navigation landmark named Contents"
    )
    assert fx.has_named_button(markup, "Contents"), "the nDrive page carries no drawer opener named Contents"


def test_long_case_studies_carry_their_heading_counts():
    """The Wasm design utils and Coast Icon case studies carry their heading counts and code."""
    for slug, count in (("wasm-design-utils", 7), ("coast-icon", 15)):
        response = fx.api(f"/case-studies/{slug}")
        assert response.status_code == 200, f"GET /api/case-studies/{slug} returned {response.status_code}"
        study = response.json()
        headings = study.get("headings") or []
        assert len(headings) == count, f"{slug} lists {len(headings)} headings, expected {count}"
        assert "```" in str(study.get("body", "")), f"{slug} carries no code block in its body"
    coast = fx.api("/case-studies/coast-icon").json()
    assert coast.get("dimensions") == "390x844", (
        f"Coast Icon reports dimensions {coast.get('dimensions')!r}, expected 390x844"
    )


def test_almanac_mono_offers_the_download_link():
    """The Almanac Mono page offers its download link."""
    anchors = fx.parse(fx.fetch("/almanac-mono").text).anchors
    assert any(fx.DOWNLOAD_LABEL in text and href == fx.DOWNLOAD_URL for href, text in anchors), (
        f"/almanac-mono carries no link reading {fx.DOWNLOAD_LABEL!r} to {fx.DOWNLOAD_URL}"
    )


def test_stub_case_study_renders_notice_without_body():
    """The Teamharbor stub renders its notice, link and footer with no body and no drawer."""
    response = fx.api(f"/case-studies/{fx.STUB_SLUG}")
    assert response.status_code == 200, f"GET /api/case-studies/teamharbor returned {response.status_code}"
    study = response.json()
    assert study.get("status") == "stub", f"Teamharbor reports status {study.get('status')!r}"
    assert study.get("body") == "", f"the stub read carries a body: {str(study.get('body'))[:80]!r}"
    assert study.get("headings") == [], f"the stub read carries headings: {study.get('headings')}"
    assert study.get("outbound_url") == fx.STUB_OUTBOUND, (
        f"Teamharbor reports outbound_url {study.get('outbound_url')!r}"
    )
    markup = fx.fetch(f"/{fx.STUB_SLUG}").text
    assert fx.contains(markup, fx.STUB_NOTICE), "the Teamharbor page does not show the work-in-progress notice"
    assert fx.contains(markup, "Metadata"), "the Teamharbor page omits its metadata footer"
    assert fx.STUB_OUTBOUND in {href for href, _ in fx.local_hrefs(markup)}, (
        "the Teamharbor page does not link to its outbound address"
    )
    assert "data-reading-rail" in markup, "the Teamharbor page omits the reading rail"
    assert not fx.named_navigation(markup, "Contents"), "the Teamharbor stub renders a contents drawer"
    assert not fx.has_named_button(markup, "Contents"), "the Teamharbor stub renders a drawer opener"


def test_draft_case_study_is_indistinguishable_from_an_unknown_slug():
    """The seeded draft answers exactly as an unknown slug on its page and in the API."""
    unknown = fx.probe_slug("no-such-study")
    draft_api = fx.api(f"/case-studies/{fx.DRAFT_SLUG}")
    unknown_api = fx.api(f"/case-studies/{unknown}")
    assert 400 <= draft_api.status_code < 500, (
        f"GET /api/case-studies/tidewater returned {draft_api.status_code} for a draft"
    )
    assert draft_api.status_code == unknown_api.status_code, (
        f"the draft answers {draft_api.status_code} but an unknown slug answers {unknown_api.status_code}"
    )
    assert fx.DRAFT_TITLE not in draft_api.text, "the draft API refusal discloses the draft title"
    draft_page = fx.fetch(f"/{fx.DRAFT_SLUG}")
    unknown_page = fx.fetch(f"/{unknown}")
    assert draft_page.status_code == unknown_page.status_code == 404, (
        f"GET /tidewater answered {draft_page.status_code} and an unknown slug "
        f"{unknown_page.status_code}; both must answer not-found"
    )
    assert fx.DRAFT_TITLE not in draft_page.text, "the draft page discloses the draft title"


def test_unknown_address_renders_the_not_found_page():
    """An unknown address renders the site's own not-found page with a way home."""
    response = fx.fetch(f"/{fx.probe_slug('nothing-here')}")
    assert response.status_code == 404, f"an unknown address answered {response.status_code}"
    markup = response.text
    assert fx.contains(markup, fx.NOT_FOUND_LINE), "the not-found page does not show its pinned line"
    assert re.search(r"data-page=[\"']not-found[\"']", markup), (
        "the not-found page root carries no data-page attribute set to not-found"
    )
    anchors = fx.local_hrefs(markup)
    assert any(fx.squash(fx.NOT_FOUND_ACTION) in fx.squash(label) and href == "/"
               for href, label in anchors), (
        f"the not-found page offers no {fx.NOT_FOUND_ACTION!r} link home"
    )
    assert fx.contains(markup, "Work") and fx.contains(markup, fx.THEME_LABEL), (
        "the not-found page drops the frame"
    )


def test_every_internal_link_resolves():
    """Every internal link on the public pages answers rather than failing."""
    pages = ("/",) + fx.CASE_STUDY_ROUTES + (f"/{fx.probe_slug('missing')}",)
    broken = []
    checked = set()
    for route in pages:
        markup = fx.fetch(route).text
        ids = set(re.findall(r"id=[\"']([^\"']+)[\"']", markup))
        for href, _ in fx.local_hrefs(markup):
            if href.startswith("#") and len(href) > 1:
                if href[1:] not in ids and route != "/":
                    broken.append((route, href))
                continue
            if not href.startswith("/") or href.startswith("//") or href.startswith("/api/"):
                continue
            target = href.split("#")[0] or "/"
            if target in checked:
                continue
            checked.add(target)
            answer = fx.fetch(target, follow=True)
            if answer.status_code >= 400:
                broken.append((route, href, answer.status_code))
    assert not broken, f"internal links that do not resolve: {broken[:8]}"
    assert len(checked) >= len(fx.CASE_STUDY_ROUTES), (
        f"only {len(checked)} internal addresses were linked from the public pages"
    )


def test_correct_passcode_is_admitted_with_a_session_grant():
    """The Field Notes code opens the article for the session through an unreadable cookie."""
    response = fx.submit_passcode(fx.GATED_PATH, fx.GATED_CODE)
    assert response.status_code == 200, f"POST /api/passcode returned {response.status_code}"
    assert response.json() == {fx.GATED_PATH: True}, (
        f"a correct code answered {response.text[:200]} rather than the path mapped to true"
    )
    raw = fx.set_cookies(response)
    assert raw, "a correct code set no grant cookie"
    for header in raw:
        low = header.lower()
        assert "httponly" in low, f"the grant cookie is readable by page script: {header}"
        assert "secure" not in [part.strip() for part in low.split(";")], (
            f"the grant cookie requires an encrypted connection: {header}"
        )
        assert "expires=" not in low and "max-age=" not in low, (
            f"the grant cookie outlives the session: {header}"
        )
    cookie = fx.cookie_header(response)
    article = fx.api(f"/case-studies/{fx.FIELD_NOTES_SLUG}", cookie=cookie)
    assert article.status_code == 200, (
        f"GET /api/case-studies/field-notes with the grant returned {article.status_code}"
    )
    assert article.json().get("lead") == fx.FIELD_NOTES_LEAD, (
        f"the unlocked article carries lead {article.json().get('lead')!r}"
    )
    page = fx.fetch(fx.GATED_PATH, cookie=cookie)
    assert fx.FIELD_NOTES_LEAD in fx.page_text(page.text), (
        "the /field-notes page does not show the article with the grant"
    )


def test_wrong_passcode_and_unknown_gate_answer_alike():
    """A wrong code and an ungated path both answer false and grant nothing."""
    wrong = fx.submit_passcode(fx.GATED_PATH, fx.WRONG_CODE)
    assert wrong.status_code == 200, f"a wrong code answered {wrong.status_code}"
    assert wrong.json() == {fx.GATED_PATH: False}, f"a wrong code answered {wrong.text[:200]}"
    assert fx.GATED_CODE not in wrong.text, "the refusal discloses the passcode"
    ghost = f"/{fx.probe_slug('no-gate')}"
    missing = fx.submit_passcode(ghost, fx.WRONG_CODE)
    assert missing.status_code == 200, f"an ungated path answered {missing.status_code}"
    assert missing.json() == {ghost: False}, f"an ungated path answered {missing.text[:200]}"
    cookie = fx.cookie_header(wrong)
    article = fx.api(f"/case-studies/{fx.FIELD_NOTES_SLUG}", cookie=cookie or None)
    assert 400 <= article.status_code < 500, (
        f"after a wrong code the gated article answered {article.status_code}"
    )


def test_malformed_passcode_is_rejected_as_invalid():
    """Malformed submissions are refused as invalid and never count toward the lock."""
    ghost = f"/{fx.probe_slug('shape')}"
    for code in ("12a4", "123", "12345", ""):
        response = fx.submit_passcode(ghost, code)
        assert 400 <= response.status_code < 500 and response.status_code != 429, (
            f"code {code!r} answered {response.status_code} rather than an invalid-input refusal"
        )
    bare = httpx.post(f"{fx.api_base()}/passcode", json={"code": "1234"}, timeout=fx.TIMEOUT)
    assert 400 <= bare.status_code < 500, f"a body with no path answered {bare.status_code}"
    codeless = httpx.post(f"{fx.api_base()}/passcode", json={"path": fx.GATED_PATH}, timeout=fx.TIMEOUT)
    assert 400 <= codeless.status_code < 500 and codeless.status_code != 429, (
        f"a body with no code answered {codeless.status_code}"
    )
    for code in ("12a4", "123"):
        fx.submit_passcode(ghost, code)
    counted = fx.submit_passcode(ghost, "2468")
    assert counted.status_code == 200, (
        f"a well-formed attempt after malformed ones answered {counted.status_code}; "
        f"malformed codes were counted toward the lock"
    )


def test_refused_attempts_are_rate_limited():
    """The sixth refused attempt for one path within a minute is locked out."""
    ghost = f"/{fx.probe_slug('locked')}"
    for attempt in range(5):
        response = fx.submit_passcode(ghost, "0000")
        assert response.status_code == 200, (
            f"refused attempt {attempt + 1} answered {response.status_code} before the limit"
        )
    locked = fx.submit_passcode(ghost, "0000")
    assert locked.status_code == 429, f"the sixth refused attempt answered {locked.status_code}"
    assert fx.error_code(locked) == fx.RATE_LIMITED, (
        f"the locked attempt carried {locked.text[:200]} rather than error rate_limited"
    )


def test_gated_article_is_denied_without_a_grant():
    """Without a grant the gated article is refused in the API and replaced by the gate."""
    denied = fx.api(f"/case-studies/{fx.FIELD_NOTES_SLUG}")
    assert 400 <= denied.status_code < 500, (
        f"GET /api/case-studies/field-notes with no grant returned {denied.status_code}"
    )
    assert fx.FIELD_NOTES_LEAD not in denied.text, "the API refusal carries the article lead"
    page = fx.fetch(fx.GATED_PATH)
    text = fx.page_text(page.text)
    assert fx.GATE_PROMPT in text, "the /field-notes page does not show the passcode prompt"
    assert fx.GATE_LABEL in text and fx.GATED_PATH in page.text, (
        "the passcode field lacks its hidden labels naming the gated path"
    )
    assert fx.FIELD_NOTES_LEAD not in page.text, "the gate screen leaks the article lead"
    assert re.search(r"data-page=[\"']gate[\"']", page.text), (
        "the gate screen root carries no data-page attribute set to gate"
    )
    title = re.search(r"<title[^>]*>(.*?)</title>", page.text, re.S | re.I)
    assert title and re.fullmatch(r"atlas\s*(\u00a9|&copy;|&#169;)\s*\d{4}", title.group(1).strip()), (
        f"the gate screen title is {title.group(1) if title else None!r}"
    )


def test_field_notes_grant_is_scoped_to_its_path():
    """The Field Notes grant opens nothing in the studio and reveals no draft."""
    cookie = fx.field_notes_cookie()
    with fx.client_with(cookie) as scoped:
        listing = scoped.get("/studio/case-studies")
        assert 400 <= listing.status_code < 500, (
            f"the studio list answered {listing.status_code} to a field notes grant"
        )
        created = scoped.post("/studio/case-studies", json=fx.case_study_payload())
        assert 400 <= created.status_code < 500, (
            f"a field notes grant created a case study with {created.status_code}"
        )
        views = scoped.get("/studio/page-views")
        assert 400 <= views.status_code < 500, (
            f"the page-view record answered {views.status_code} to a field notes grant"
        )
    unknown = fx.api(f"/case-studies/{fx.probe_slug('absent')}", cookie=cookie)
    draft = fx.api(f"/case-studies/{fx.DRAFT_SLUG}", cookie=cookie)
    assert draft.status_code == unknown.status_code, (
        f"with a field notes grant the draft answers {draft.status_code}, "
        f"an unknown slug {unknown.status_code}"
    )


def test_studio_endpoints_are_denied_without_the_studio_grant(anonymous, studio, store):
    """Every studio call from a visitor is denied and changes nothing."""
    listing = anonymous.get("/studio/case-studies")
    assert 400 <= listing.status_code < 500, f"the studio list answered {listing.status_code}"
    payload = fx.case_study_payload()
    created = anonymous.post("/studio/case-studies", json=payload)
    assert 400 <= created.status_code < 500, f"a visitor create answered {created.status_code}"
    assert fx.studio_find(studio, payload["slug"]) is None, "a visitor create wrote a case study"
    draft = fx.studio_find(studio, fx.DRAFT_SLUG)
    assert draft, "the studio list does not show the seeded draft"
    published = anonymous.post(f"/studio/case-studies/{draft['id']}/publish")
    assert 400 <= published.status_code < 500, f"a visitor publish answered {published.status_code}"
    assert fx.studio_find(studio, fx.DRAFT_SLUG)["status"] == "draft", "a visitor publish moved the draft"
    before = store.list(f"case-studies/{draft['id']}/")
    uploaded = fx.upload(anonymous, draft["id"], fx.random_png())
    assert 400 <= uploaded.status_code < 500, f"a visitor upload answered {uploaded.status_code}"
    assert store.list(f"case-studies/{draft['id']}/") == before, "a visitor upload wrote to the bucket"


def test_release_ends_the_grant(backend):
    """Releasing the studio grant closes the studio even for a replayed cookie."""
    cookie = fx.studio_cookie()
    with fx.client_with(cookie) as client:
        assert client.get("/studio/case-studies").status_code == 200, "the fresh studio grant was refused"
        released = client.post("/passcode/release", json={"path": fx.STUDIO_PATH})
        assert 200 <= released.status_code < 300, f"POST /api/passcode/release answered {released.status_code}"
        after = client.get("/studio/case-studies")
        assert 400 <= after.status_code < 500, (
            f"the released studio cookie still opened the studio with {after.status_code}"
        )
    marked = backend.query("SELECT count(*) AS n FROM passcode_grant WHERE released_at IS NOT NULL")
    assert marked[0]["n"] >= 1, "no passcode_grant row is marked released after a release"


def test_studio_page_shows_the_gate_until_unlocked(page, app_base):
    """The studio shows the gate, then its sidebar and status rows once 5093 is entered."""
    page.goto(f"{app_base}{fx.STUDIO_PATH}")
    page.get_by_text(fx.GATE_PROMPT).first.wait_for()
    assert page.get_by_text(fx.NEW_CASE_STUDY).count() == 0, "the locked studio shows its controls"
    field = page.get_by_label(re.compile(fx.GATE_LABEL))
    field.first.focus()
    page.keyboard.type(fx.STUDIO_CODE)
    page.get_by_text(fx.NEW_CASE_STUDY).first.wait_for()
    for label in fx.STUDIO_SIDEBAR:
        assert page.get_by_text(label).count() >= 1, f"the unlocked studio does not show {label!r}"
    page.wait_for_selector("[data-status='draft']", state="attached")
    assert page.evaluate("document.documentElement.dataset.page") == "studio", (
        "the unlocked studio root carries no data-page attribute set to studio"
    )
    statuses = page.eval_on_selector_all("[data-status]", "els => els.map(el => el.dataset.status)")
    assert set(statuses) >= {"draft", "stub", "published"}, (
        f"studio rows carry statuses {sorted(set(statuses))}, expected all three"
    )


def test_studio_grant_previews_drafts_and_the_gated_article(studio):
    """The studio grant lists every status and previews the draft and the gated article."""
    rows = fx.studio_list(studio)
    by_slug = {row.get("slug"): row for row in rows}
    for slug in fx.SEEDED_SLUGS:
        assert slug in by_slug, f"the studio list omits {slug!r}"
    assert by_slug[fx.DRAFT_SLUG]["status"] == "draft", "the studio list misreports the draft"
    one = studio.get(f"/studio/case-studies/{by_slug[fx.DRAFT_SLUG]['id']}")
    assert one.status_code == 200 and one.json().get("status") == "draft", (
        f"GET /api/studio/case-studies/{{id}} for the draft answered {one.status_code}"
    )
    cookie = studio.headers["Cookie"]
    preview = fx.api(f"/case-studies/{fx.DRAFT_SLUG}", cookie=cookie)
    assert preview.status_code == 200 and preview.json().get("title") == fx.DRAFT_TITLE, (
        f"the studio grant could not preview the draft: {preview.status_code}"
    )
    page = fx.fetch(f"/{fx.DRAFT_SLUG}", cookie=cookie)
    assert page.status_code == 200 and fx.DRAFT_TITLE in fx.page_text(page.text), (
        f"the draft page answered {page.status_code} to the studio grant"
    )
    gated = fx.api(f"/case-studies/{fx.FIELD_NOTES_SLUG}", cookie=cookie)
    assert gated.status_code == 200 and gated.json().get("lead") == fx.FIELD_NOTES_LEAD, (
        f"the studio grant could not read the gated article: {gated.status_code}"
    )


def test_publish_lists_the_card_and_opens_the_page(studio):
    """Publishing a new case study lists its card and opens its page."""
    study = fx.create_case_study(studio)
    position = study["card"]["sort_order"]
    try:
        assert not fx.holders_of(position), "a draft card was listed before publication"
        assert fx.fetch(f"/{study['slug']}").status_code == 404, "the draft page answered before publication"
        result = fx.transition(studio, study["id"], "publish")
        assert result.status_code in (200, 201), f"publish answered {result.status_code}: {result.text[:300]}"
        assert result.json().get("status") == "published", f"publish reported {result.text[:200]}"
        assert result.json().get("published_at"), "publish left published_at empty"
        holders = fx.holders_of(position)
        assert len(holders) == 1 and holders[0].get("slug") == study["slug"], (
            f"the published card is not listed at position {position}: {holders}"
        )
        assert holders[0].get("column_start") == 1 and holders[0].get("column_span") == 4, (
            f"the listed card lost its placement: {holders[0]}"
        )
        opened = fx.fetch(f"/{study['slug']}")
        assert opened.status_code == 200 and study["title"] in fx.page_text(opened.text), (
            f"the published page answered {opened.status_code}"
        )
    finally:
        fx.transition(studio, study["id"], "hold")
    cardless = fx.create_case_study(studio, card=None)
    try:
        published = fx.transition(studio, cardless["id"], "publish")
        assert published.status_code in (200, 201), f"publishing a case study with no card answered {published.status_code}"
        assert fx.fetch(f"/{cardless['slug']}").status_code == 200, "a published case study with no card is unreadable"
        assert all(card.get("slug") != cardless["slug"] for card in fx.listed_cards()), (
            "a case study with no card was listed"
        )
    finally:
        fx.transition(studio, cardless["id"], "hold")


def test_stub_lists_the_card_with_the_notice_state(studio):
    """Marking a case study as a stub lists its card and renders the notice state."""
    study = fx.create_case_study(studio)
    try:
        result = fx.transition(studio, study["id"], "stub")
        assert result.status_code in (200, 201), f"stub answered {result.status_code}: {result.text[:300]}"
        assert result.json().get("status") == "stub", f"stub reported {result.text[:200]}"
        assert len(fx.holders_of(study["card"]["sort_order"])) == 1, "the stub card is not listed"
        read = fx.api(f"/case-studies/{study['slug']}").json()
        assert read.get("body") == "" and read.get("headings") == [], (
            f"the stub read carries body or headings: {read.get('headings')}"
        )
        assert read.get("character_count") == 0, (
            f"the stub read reports character_count {read.get('character_count')}"
        )
        assert fx.contains(fx.fetch(f"/{study['slug']}").text, fx.STUB_NOTICE), (
            "the stub page does not show the work-in-progress notice"
        )
        kept = studio.get(f"/studio/case-studies/{study['id']}").json()
        assert kept.get("body") == study["body"], "stubbing discarded the stored body"
        assert fx.transition(studio, study["id"], "publish").status_code in (200, 201), "publish refused"
        served = fx.api(f"/case-studies/{study['slug']}").json()
        assert served.get("body") == study["body"], "the body was not served again after publishing"
    finally:
        fx.transition(studio, study["id"], "hold")


def test_hold_withdraws_page_card_and_figures(studio, anonymous):
    """Holding a published case study closes its page, card and figures at once."""
    study = fx.create_case_study(studio)
    noop = fx.transition(studio, study["id"], "hold")
    assert noop.status_code in (200, 201) and noop.json().get("status") == "draft", (
        f"holding a draft answered {noop.status_code}: {noop.text[:200]}"
    )
    figure = fx.upload(studio, study["id"], fx.random_png())
    assert figure.status_code in (200, 201), f"upload answered {figure.status_code}: {figure.text[:300]}"
    figure_id = figure.json()["id"]
    assert fx.transition(studio, study["id"], "publish").status_code in (200, 201), "publish was refused"
    assert anonymous.get(f"/figures/{figure_id}").status_code == 200, "a published figure was refused"
    held = fx.transition(studio, study["id"], "hold")
    assert held.status_code in (200, 201), f"hold answered {held.status_code}: {held.text[:300]}"
    assert held.json().get("status") == "draft", f"hold reported {held.text[:200]}"
    assert fx.fetch(f"/{study['slug']}").status_code == 404, "the held page still answers"
    assert not fx.holders_of(study["card"]["sort_order"]), "the held card is still listed"
    denied = anonymous.get(f"/figures/{figure_id}")
    assert 400 <= denied.status_code < 500, f"the held figure answered {denied.status_code}"


def test_concurrent_publish_at_one_position_has_one_winner(studio, backend):
    """Two simultaneous publishes claiming one free position leave exactly one listed card."""
    position = fx.free_position()
    first = fx.create_case_study(studio, card=fx.card_payload(position))
    second = fx.create_case_study(studio, card=fx.card_payload(position))
    cookie = studio.headers["Cookie"]
    barrier = threading.Barrier(2)
    results = {}

    def publish(study):
        with fx.client_with(cookie) as racer:
            barrier.wait()
            results[study["id"]] = racer.post(f"/studio/case-studies/{study['id']}/publish")

    threads = [threading.Thread(target=publish, args=(study,)) for study in (first, second)]
    try:
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(fx.TIMEOUT)
        codes = sorted(response.status_code for response in results.values())
        accepted = [r for r in results.values() if r.status_code in (200, 201)]
        refused = [r for r in results.values() if 400 <= r.status_code < 500]
        assert len(accepted) == 1 and len(refused) == 1, (
            f"two publishes at position {position} answered {codes}, expected one win and one refusal"
        )
        assert fx.error_code(refused[0]) == fx.POSITION_TAKEN, (
            f"the losing publish carried {refused[0].text[:200]}"
        )
        assert len(fx.holders_of(position)) == 1, "the contended position is held by more than one card"
        stored = backend.query(
            "SELECT count(*) AS n FROM project_card AS card JOIN case_study AS study "
            "ON study.id = card.case_study_id WHERE card.sort_order = %s "
            "AND study.status IN ('published', 'stub')", (position,))
        assert stored[0]["n"] == 1, f"the database lists {stored[0]['n']} cards at position {position}"
    finally:
        for study in (first, second):
            fx.transition(studio, study["id"], "hold")


def test_rejected_publish_leaves_the_loser_a_draft(studio):
    """Publishing onto a taken position is refused and the loser stays an unlisted draft."""
    position = fx.free_position()
    winner = fx.create_case_study(studio, card=fx.card_payload(position))
    loser = fx.create_case_study(studio, card=fx.card_payload(position))
    try:
        assert fx.transition(studio, winner["id"], "publish").status_code in (200, 201), (
            "the first publish was refused"
        )
        refusal = fx.transition(studio, loser["id"], "publish")
        assert 400 <= refusal.status_code < 500, f"the second publish answered {refusal.status_code}"
        assert fx.error_code(refusal) == fx.POSITION_TAKEN, f"the refusal carried {refusal.text[:200]}"
        again = studio.get(f"/studio/case-studies/{loser['id']}").json()
        assert again.get("status") == "draft", f"the loser reports status {again.get('status')!r}"
        holders = fx.holders_of(position)
        assert [card.get("slug") for card in holders] == [winner["slug"]], (
            f"position {position} is held by {holders}"
        )
    finally:
        fx.transition(studio, winner["id"], "hold")


def test_invalid_placement_is_refused_and_writes_nothing(studio):
    """Placements outside the grid, unknown ratios, zero positions and empty media descriptions are refused."""
    bad_cards = (
        (fx.card_payload(fx.free_position(), column_start=10, column_span=5), fx.INVALID_PLACEMENT),
        (fx.card_payload(fx.free_position(), column_start_lg=13), fx.INVALID_PLACEMENT),
        (fx.card_payload(fx.free_position(), aspect_ratio="4:3"), fx.INVALID_PLACEMENT),
        (fx.card_payload(0), fx.INVALID_PLACEMENT),
        (fx.card_payload(fx.free_position(), media_alt=""), fx.INVALID_MEDIA_ALT),
    )
    for card, code in bad_cards:
        payload = fx.case_study_payload(card=card)
        response = studio.post("/studio/case-studies", json=payload)
        assert 400 <= response.status_code < 500, (
            f"card {card} answered {response.status_code} rather than an invalid refusal"
        )
        assert fx.error_code(response) == code, f"card {card} carried {response.text[:200]}"
        assert fx.studio_find(studio, payload["slug"]) is None, (
            f"a refused card still wrote {payload['slug']}"
        )


def test_moving_a_listed_card_onto_a_taken_position_is_refused(studio):
    """Editing a listed card onto another listed card's position is refused."""
    first = fx.create_case_study(studio)
    second = fx.create_case_study(studio)
    try:
        for study in (first, second):
            assert fx.transition(studio, study["id"], "publish").status_code in (200, 201), "publish refused"
        moved = fx.card_payload(first["card"]["sort_order"])
        response = studio.patch(f"/studio/case-studies/{second['id']}", json={"card": moved})
        assert 400 <= response.status_code < 500, f"the move answered {response.status_code}"
        assert fx.error_code(response) == fx.POSITION_TAKEN, f"the move carried {response.text[:200]}"
        kept = studio.get(f"/studio/case-studies/{second['id']}").json()
        assert kept["card"]["sort_order"] == second["card"]["sort_order"], (
            f"the refused move still changed the position to {kept['card']['sort_order']}"
        )
    finally:
        for study in (first, second):
            fx.transition(studio, study["id"], "hold")


def test_incomplete_case_study_is_refused(studio):
    """Missing required fields and wrongly shaped fields are refused as client errors and write nothing."""
    cases = []
    for missing in ("title", "slug", "lead"):
        payload = fx.case_study_payload()
        payload.pop(missing)
        cases.append((payload, fx.INCOMPLETE))
    cases.append((fx.case_study_payload(last_updated="yesterday"), fx.INVALID_FIELD))
    cases.append((fx.case_study_payload(outbound_url="not an address"), fx.INVALID_FIELD))
    for payload, code in cases:
        slug = payload.get("slug") or ""
        before = len(fx.studio_list(studio))
        response = studio.post("/studio/case-studies", json=payload)
        assert 400 <= response.status_code < 500, (
            f"payload {sorted(payload)} answered {response.status_code}"
        )
        assert fx.error_code(response) == code, f"payload carried {response.text[:200]}, expected {code}"
        assert len(fx.studio_list(studio)) == before, f"a refused create for {slug!r} was written"


def test_invalid_or_reserved_or_taken_slug_is_refused(studio):
    """Bad, reserved and taken slugs are refused with their own codes."""
    for slug, code in (("Bad Slug", fx.INVALID_SLUG), ("trailing-", fx.INVALID_SLUG),
                       ("studio", fx.SLUG_RESERVED), ("api", fx.SLUG_RESERVED),
                       ("ndrive", fx.SLUG_TAKEN)):
        payload = fx.case_study_payload(slug=slug)
        before = len(fx.studio_list(studio))
        response = studio.post("/studio/case-studies", json=payload)
        assert 400 <= response.status_code < 500, f"slug {slug!r} answered {response.status_code}"
        assert fx.error_code(response) == code, f"slug {slug!r} carried {response.text[:200]}"
        assert len(fx.studio_list(studio)) == before, f"slug {slug!r} still wrote a case study"


def test_slug_change_leaves_a_permanent_redirect(studio, backend):
    """Renaming a published slug leaves a permanent redirect and retires the old slug."""
    study = fx.create_case_study(studio)
    old = study["slug"]
    new = fx.probe_slug("renamed")
    try:
        assert fx.transition(studio, study["id"], "publish").status_code in (200, 201), "publish refused"
        patched = studio.patch(f"/studio/case-studies/{study['id']}", json={"slug": new})
        assert patched.status_code in (200, 201), f"PATCH answered {patched.status_code}: {patched.text[:300]}"
        moved = fx.fetch(f"/{old}")
        assert moved.status_code in (301, 308), f"the old address answered {moved.status_code}"
        assert moved.headers.get("location", "").rstrip("/").endswith(f"/{new}"), (
            f"the old address redirects to {moved.headers.get('location')!r}"
        )
        assert fx.fetch(f"/{new}").status_code == 200, "the new address does not answer"
        assert backend.count("slug_redirect", old_slug=old) == 1, "no slug_redirect row records the old slug"
        clash = studio.post("/studio/case-studies", json=fx.case_study_payload(slug=old))
        assert fx.error_code(clash) == fx.SLUG_TAKEN, f"the retired slug was reusable: {clash.text[:200]}"
    finally:
        fx.transition(studio, study["id"], "hold")


def test_heading_slugs_follow_the_pinned_rule(studio):
    """Heading slugs collapse punctuation, number repeats, follow edits, and skipped levels are refused."""
    body = ("## Notes\n\nFirst.\n\n### Offline, then online\n\nSecond.\n\n"
            "## Notes\n\nThird.\n\n### What I would change\n\nFourth.")
    study = fx.create_case_study(studio, body=body)
    cookie = studio.headers["Cookie"]
    read = fx.api(f"/case-studies/{study['slug']}", cookie=cookie)
    assert read.status_code == 200, f"the studio preview read answered {read.status_code}"
    headings = [(h.get("level"), h.get("slug")) for h in read.json().get("headings") or []]
    assert headings == [(2, "notes"), (3, "offline-then-online"), (2, "notes-2"),
                        (3, "what-i-would-change")], f"the headings read {headings}"
    markup = fx.fetch(f"/{study['slug']}", cookie=cookie).text
    for slug in ("notes", "notes-2", "offline-then-online", "what-i-would-change"):
        assert re.search(rf"id=[\"']{slug}[\"']", markup), f"the page carries no heading id {slug!r}"
    edited = body.replace("### Offline, then online", "### Back online")
    patched = studio.patch(f"/studio/case-studies/{study['id']}", json={"body": edited})
    assert patched.status_code in (200, 201), f"PATCH body answered {patched.status_code}"
    slugs = [h.get("slug") for h in fx.api(f"/case-studies/{study['slug']}", cookie=cookie).json().get("headings") or []]
    assert "back-online" in slugs and "offline-then-online" not in slugs, (
        f"after the edit the headings read {slugs}"
    )
    skipping = studio.post("/studio/case-studies", json=fx.case_study_payload(
        body="## Top\n\nText.\n\n#### Too deep\n\nMore."))
    assert 400 <= skipping.status_code < 500, f"a skipped heading level answered {skipping.status_code}"
    assert fx.error_code(skipping) == fx.INVALID_HEADING_LEVELS, (
        f"a skipped heading level carried {skipping.text[:200]}"
    )


def test_character_count_is_derived_from_the_body(studio):
    """The character count leaves out line breaks and the label groups thousands."""
    line = "Almanac notes keep their rhythm across long pages."
    body = "\n".join([line] * 32 + ["xy"])
    study = fx.create_case_study(studio, body=body)
    read = fx.api(f"/case-studies/{study['slug']}", cookie=studio.headers["Cookie"]).json()
    expected = len(body.replace("\n", ""))
    assert expected == 1602, f"the probe body was built with {expected} characters"
    assert read.get("character_count") == expected, (
        f"character_count reads {read.get('character_count')}, expected {expected}"
    )
    assert read.get("character_label") == "1,602", (
        f"character_label reads {read.get('character_label')!r}, expected '1,602'"
    )


def test_figure_upload_is_stored_in_the_bucket_at_the_pinned_key(studio, store, backend):
    """An uploaded figure lands in the bucket at its pinned key with its metadata recorded."""
    study = fx.create_case_study(studio)
    payload = fx.random_png()
    response = fx.upload(studio, study["id"], payload, alt_text="A two-pixel probe figure.")
    assert response.status_code in (200, 201), f"upload answered {response.status_code}: {response.text[:300]}"
    figure = response.json()
    key = fx.OBJECT_KEY_TEMPLATE.format(case_study_id=study["id"], digest=fx.digest_of(payload))
    assert figure.get("object_key") == key, f"the figure key is {figure.get('object_key')!r}, expected {key!r}"
    assert store.exists(key), f"no object exists in the bucket at {key}"
    assert figure.get("content_type") == "image/png", f"content_type is {figure.get('content_type')!r}"
    assert figure.get("byte_size") == len(payload), f"byte_size is {figure.get('byte_size')}"
    assert (figure.get("width"), figure.get("height")) == (2, 1), (
        f"the recorded size is {figure.get('width')}x{figure.get('height')}"
    )
    assert figure.get("url") == f"/api/figures/{figure.get('id')}", f"the figure url is {figure.get('url')!r}"
    row = backend.one("figure", object_key=key)
    assert row is not None, f"no figure row records {key}"
    assert row.get("alt_text") == "A two-pixel probe figure.", f"the stored alt text is {row.get('alt_text')!r}"


def test_figure_bytes_stream_back_unchanged(studio, anonymous):
    """A published figure streams back byte for byte and is placed with its size reserved."""
    study = fx.create_case_study(studio)
    payload = fx.random_png()
    figure = fx.upload(studio, study["id"], payload, alt_text="A streamed probe figure.").json()
    body = f"## Figure\n\n[[figure:{figure['id']}]]\n\nAfter the figure."
    patched = studio.patch(f"/studio/case-studies/{study['id']}", json={"body": body})
    assert patched.status_code in (200, 201), f"PATCH body answered {patched.status_code}"
    try:
        assert fx.transition(studio, study["id"], "publish").status_code in (200, 201), "publish refused"
        streamed = anonymous.get(f"/figures/{figure['id']}")
        assert streamed.status_code == 200, f"the published figure answered {streamed.status_code}"
        assert streamed.content == payload, "the streamed bytes differ from the uploaded bytes"
        assert streamed.headers.get("content-type", "").startswith("image/png"), (
            f"the figure streamed as {streamed.headers.get('content-type')!r}"
        )
        markup = fx.fetch(f"/{study['slug']}").text
        tag = re.search(rf"<img\b[^>]*/api/figures/{figure['id']}[^>]*>", markup)
        assert tag, "the published page does not place the uploaded figure"
        assert "A streamed probe figure." in tag.group(0), "the placed figure lacks its alternative text"
        around = markup[max(0, tag.start() - 600):tag.end()]
        sized = (re.search(r"width=[\"']?2[\"'\s>]", tag.group(0))
                 and re.search(r"height=[\"']?1[\"'\s>]", tag.group(0))) \
            or re.search(r"aspect-ratio\s*:\s*2\s*/\s*1", around) \
            or re.search(r"--[\w-]*(?:ratio|aspect)[\w-]*\s*:\s*2\s*/\s*1", around)
        assert sized, f"the placed figure reserves no box from its recorded size: {tag.group(0)[:200]}"
    finally:
        fx.transition(studio, study["id"], "hold")


def test_duplicate_figure_upload_creates_one_object(studio, store, backend):
    """Uploading the same bytes twice keeps one object and one figure record."""
    study = fx.create_case_study(studio)
    payload = fx.random_png()
    first = fx.upload(studio, study["id"], payload)
    second = fx.upload(studio, study["id"], payload)
    assert first.status_code in (200, 201) and second.status_code in (200, 201), (
        f"the uploads answered {first.status_code} and {second.status_code}"
    )
    assert first.json()["id"] == second.json()["id"], "the repeat upload returned a new figure"
    objects = store.list(f"case-studies/{study['id']}/figures/")
    assert len(objects) == 1, f"the bucket holds {len(objects)} objects for one repeated upload"
    assert backend.count("figure", case_study_id=study["id"]) == 1, "the repeat upload wrote a second row"


def test_figure_without_alt_text_is_refused(studio, store, backend):
    """An upload with no alternative text is refused and stores nothing."""
    study = fx.create_case_study(studio)
    for alt in (None, "   "):
        response = fx.upload(studio, study["id"], fx.random_png(), alt_text=alt)
        assert 400 <= response.status_code < 500, f"alt text {alt!r} answered {response.status_code}"
        assert fx.error_code(response) == fx.ALT_TEXT_REQUIRED, f"alt text {alt!r} carried {response.text[:200]}"
    assert store.list(f"case-studies/{study['id']}/") == [], "a refused upload wrote to the bucket"
    assert backend.count("figure", case_study_id=study["id"]) == 0, "a refused upload wrote a row"


def test_figure_upload_refusals_name_their_reason(studio, store):
    """Wrong types, bad or mismatched sizes and oversized files are refused with their own codes."""
    study = fx.create_case_study(studio)
    gif = (b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00"
           b",\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;")
    cases = (
        (dict(content_type="image/gif", filename="figure.gif", width="1", height="1"), gif, fx.UNSUPPORTED_TYPE),
        (dict(width="0"), fx.random_png(), fx.INVALID_DIMENSIONS),
        (dict(height="tall"), fx.random_png(), fx.INVALID_DIMENSIONS),
        (dict(width="3"), fx.random_png(), fx.INVALID_DIMENSIONS),
        ({}, fx.random_png() + b"\x00" * (fx.FIVE_MEGABYTES + 1), fx.FILE_TOO_LARGE),
    )
    for options, payload, code in cases:
        response = fx.upload(studio, study["id"], payload, **options)
        assert 400 <= response.status_code < 500, f"{code} case answered {response.status_code}"
        assert fx.error_code(response) == code, f"{code} case carried {response.text[:200]}"
    assert store.list(f"case-studies/{study['id']}/") == [], "a refused upload wrote to the bucket"


def test_draft_figure_is_denied_to_visitors(studio, anonymous, store):
    """A draft's figure exists in the bucket and is refused to everyone but the studio."""
    study = fx.create_case_study(studio)
    payload = fx.random_png()
    figure = fx.upload(studio, study["id"], payload).json()
    assert store.exists(figure["object_key"]), "the draft figure is absent from the bucket"
    denied = anonymous.get(f"/figures/{figure['id']}")
    assert 400 <= denied.status_code < 500, f"a visitor read of a draft figure answered {denied.status_code}"
    owner = studio.get(f"/figures/{figure['id']}")
    assert owner.status_code == 200, f"the studio read of a draft figure answered {owner.status_code}"
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    bucket = os.environ["STORAGE_BUCKET"]
    direct = httpx.get(f"{endpoint}/{bucket}/{figure['object_key']}", timeout=fx.TIMEOUT)
    assert direct.status_code >= 400 and direct.content != payload, (
        f"an anonymous request straight to the bucket answered {direct.status_code} with the figure"
    )


def test_gated_figure_needs_its_grant(studio, anonymous):
    """A figure on the gated article opens only with that article's grant or the studio grant."""
    gated = fx.studio_find(studio, fx.FIELD_NOTES_SLUG)
    assert gated, "the studio list omits the gated article"
    response = fx.upload(studio, gated["id"], fx.png_bytes(90, 60, 30), alt_text="A field notes sketch.")
    assert response.status_code in (200, 201), f"upload to the gated article answered {response.status_code}"
    figure_id = response.json()["id"]
    denied = anonymous.get(f"/figures/{figure_id}")
    assert 400 <= denied.status_code < 500, f"a visitor read of a gated figure answered {denied.status_code}"
    with fx.client_with(fx.field_notes_cookie()) as reader:
        assert reader.get(f"/figures/{figure_id}").status_code == 200, "the field notes grant was refused its figure"
    assert studio.get(f"/figures/{figure_id}").status_code == 200, "the studio grant was refused the gated figure"


def _moment(stamp: str) -> datetime:
    """An ISO 8601 or RFC 1123 timestamp as an aware datetime."""
    if re.match(r"\d{4}-\d{2}-\d{2}", stamp):
        moment = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    else:
        moment = parsedate_to_datetime(stamp)
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def test_page_view_is_recorded_for_the_owner(studio, anonymous, backend):
    """A public page view is recorded newest first, holds no visitor identifier, and is readable by the studio alone."""
    assert fx.fetch("/coast-icon").status_code == 200, "GET /coast-icon failed"
    fx.api("/projects")

    def views():
        response = studio.get("/studio/page-views")
        assert response.status_code == 200, f"GET /api/studio/page-views answered {response.status_code}"
        return response.json()

    seen = fx.wait_for(views, lambda rows: any(row.get("route") == "/coast-icon" for row in rows))
    assert any(row.get("route") == "/coast-icon" for row in seen), "the /coast-icon view was not recorded"
    stamps = [str(row.get("viewed_at") or "") for row in seen[:50]]
    assert all(stamps), f"a page view lacks viewed_at: {seen[:3]}"
    moments = [_moment(stamp) for stamp in stamps]
    assert moments == sorted(moments, reverse=True), "the page-view record is not newest first"
    for row in seen[:50]:
        assert not str(row.get("route", "")).startswith("/api"), f"an API call was recorded: {row}"
    assert backend.count("page_view", route="/coast-icon") >= 1, "no page_view row stores /coast-icon"
    stored = backend.rows("page_view", limit=1)
    identifying = [column for column in (stored[0] if stored else {})
                   if any(word in column.lower() for word in fx.VISITOR_IDENTIFIER_WORDS)]
    assert stored and not identifying, f"page_view stores visitor identifiers: {identifying}"
    denied = anonymous.get("/studio/page-views")
    assert 400 <= denied.status_code < 500, f"a visitor read the page-view record with {denied.status_code}"


def test_home_scrolls_an_inner_element_with_the_keyboard(page, app_base):
    """The window never scrolls; the scroller element moves on page down."""
    page.goto(f"{app_base}/")
    page.wait_for_selector("[data-scroller]", state="attached")
    measures = page.evaluate(
        """() => { const s = document.querySelector('[data-scroller]');
                   return {doc: document.documentElement.scrollHeight, win: window.innerHeight,
                           inner: s.scrollHeight, client: s.clientHeight}; }"""
    )
    assert measures["doc"] <= measures["win"] + 2, f"the document grows past the window: {measures}"
    assert measures["inner"] > measures["client"] * 3, f"the scroller holds too little content: {measures}"
    page.locator("h1").first.click()
    page.keyboard.press("PageDown")
    moved = fx.wait_for(lambda: page.evaluate("document.querySelector('[data-scroller]').scrollTop"),
                        lambda top: top > 0, limit=5.0)
    assert moved > 0, "page down did not move the scroller"
    assert page.evaluate("window.scrollY") == 0, "page down scrolled the window"


def test_theme_control_toggles_and_survives_a_reload(page, app_base):
    """The theme starts light, toggles the root class, persists, applies before paint and answers A."""
    page.add_init_script(
        """window.__classAtBody = null;
           new MutationObserver((m, o) => { if (document.body) {
               window.__classAtBody = document.documentElement.className; o.disconnect(); } })
             .observe(document, {childList: true, subtree: true});"""
    )
    page.goto(f"{app_base}/")
    root = "document.documentElement.classList"
    assert page.evaluate(f"{root}.contains('light')") and not page.evaluate(f"{root}.contains('dark')"), (
        "a first visit does not show the light theme"
    )
    control = page.locator("button", has_text=fx.THEME_LABEL).first
    control.click()
    assert page.evaluate(f"{root}.contains('dark')"), "the theme button did not switch to dark"
    assert control.get_attribute("aria-pressed") == "true", (
        f"the theme button reports aria-pressed={control.get_attribute('aria-pressed')!r} in dark"
    )
    page.reload()
    assert page.evaluate(f"{root}.contains('dark')"), "the dark choice did not survive a reload"
    first_class = page.evaluate("window.__classAtBody") or ""
    assert "dark" in first_class.split(), (
        f"the theme class was {first_class!r} when the body first appeared"
    )
    page.locator("body").press("a")
    assert page.evaluate(f"{root}.contains('light')"), "the A key did not switch back to light"


def test_sound_control_starts_off(page, app_base):
    """The sound control is a button that reports off on a first visit."""
    page.goto(f"{app_base}/")
    control = page.locator("button", has_text=fx.SOUND_LABEL_OPEN).first
    control.wait_for()
    assert control.get_attribute("aria-pressed") == "false", (
        f"the sound button reports aria-pressed={control.get_attribute('aria-pressed')!r} on a first visit"
    )


def test_narrow_viewport_has_no_sideways_overflow(narrow_page, app_base):
    """At a narrow viewport nothing scrolls sideways and the Menu button reaches the frame controls."""
    for route in ("/", "/ndrive"):
        narrow_page.goto(f"{app_base}{route}")
        widths = narrow_page.evaluate(
            """() => { const s = document.querySelector('[data-scroller]') || document.documentElement;
                       return {doc: document.documentElement.scrollWidth, inner: s.scrollWidth,
                               client: s.clientWidth, win: window.innerWidth}; }"""
        )
        assert widths["doc"] <= widths["win"] and widths["inner"] <= widths["client"] + 1, (
            f"{route} overflows sideways at a narrow viewport: {widths}"
        )
    narrow_page.goto(f"{app_base}/")
    menu = narrow_page.get_by_role("button", name=fx.MENU_NAME, exact=True).first
    menu.click()
    narrow_page.locator("button:visible", has_text="Work").first.wait_for()
    assert narrow_page.locator("button:visible", has_text="Contact").count() >= 1, (
        "the opened menu does not reach Contact"
    )


def test_passcode_slots_submit_on_the_fourth_digit(page, app_base):
    """Backspace clears a digit, the fourth digit submits, and the article stays open after a reload."""
    page.goto(f"{app_base}{fx.GATED_PATH}")
    page.get_by_text(fx.GATE_PROMPT).first.wait_for()
    assert page.locator("[data-slot-state]").count() == 4, "the gate does not draw four slots"
    field = page.get_by_label(re.compile(fx.GATE_LABEL))
    field.first.focus()
    page.keyboard.type("27")
    page.keyboard.press("Backspace")
    slots = lambda: page.eval_on_selector_all("[data-slot-state]", "els => els.map(el => el.dataset.slotState)")
    states = fx.wait_for(slots, lambda got: got == ["filled", "next", "empty", "empty"], limit=5.0)
    assert states == ["filled", "next", "empty", "empty"], f"after 2, 7 and Backspace the slots read {states}"
    page.keyboard.type("718")
    page.get_by_text(fx.FIELD_NOTES_LEAD).first.wait_for()
    assert page.url.rstrip("/").endswith(fx.GATED_PATH), f"the unlocked article moved to {page.url}"
    page.reload()
    page.get_by_text(fx.FIELD_NOTES_LEAD).first.wait_for()


def test_wrong_code_clears_the_slots_in_the_page(page, app_base):
    """A wrong code clears the slots, returns the waiting slot to the first and shows the message."""
    page.goto(f"{app_base}{fx.GATED_PATH}")
    page.get_by_text(fx.GATE_PROMPT).first.wait_for()
    field = page.get_by_label(re.compile(fx.GATE_LABEL))
    field.first.focus()
    page.keyboard.type(fx.WRONG_CODE)
    page.get_by_text(fx.WRONG_CODE_MESSAGE).first.wait_for()
    slots = lambda: page.eval_on_selector_all("[data-slot-state]", "els => els.map(el => el.dataset.slotState)")
    states = fx.wait_for(slots, lambda got: got == ["next", "empty", "empty", "empty"], limit=5.0)
    assert states == ["next", "empty", "empty", "empty"], f"after a wrong code the slots read {states}"
    assert page.get_by_text(fx.FIELD_NOTES_LEAD).count() == 0, "a wrong code revealed the article"


def test_rate_limited_answer_shows_the_lock_message(page, app_base):
    """A rate-limited answer from the server shows the too-many-attempts message."""
    page.route(
        "**/api/passcode",
        lambda route: route.fulfill(status=429, content_type="application/json",
                                    body='{"error": "rate_limited", "message": "locked"}'),
    )
    page.goto(f"{app_base}{fx.GATED_PATH}")
    page.get_by_text(fx.GATE_PROMPT).first.wait_for()
    field = page.get_by_label(re.compile(fx.GATE_LABEL))
    field.first.focus()
    page.keyboard.type("4680")
    page.get_by_text(fx.RATE_LIMIT_MESSAGE).first.wait_for()


def test_code_block_line_numbers_cannot_be_selected(page, app_base):
    """Code line numbers are unselectable and the copy control swaps to its copied label."""
    page.goto(f"{app_base}/wasm-design-utils")
    page.wait_for_selector("[data-line-number]", state="attached")
    selectable = page.eval_on_selector_all(
        "[data-line-number]",
        "els => els.map(el => getComputedStyle(el).userSelect || getComputedStyle(el).webkitUserSelect)",
    )
    assert selectable and all(value == "none" for value in selectable), (
        f"code line numbers report user-select values {sorted(set(selectable))}"
    )
    copy = page.locator("button", has_text=fx.COPY_LABEL).first
    copy.click()
    page.locator("button", has_text=fx.COPIED_LABEL).first.wait_for()


def test_reduced_motion_holds_the_band_to_one_screen(page, reduced_page, app_base):
    """The held band spans many screens normally and one screen under reduced motion."""
    page.goto(f"{app_base}/")
    page.wait_for_selector("[data-band='held']", state="attached")
    tall = page.evaluate("document.querySelector(\"[data-band='held']\").getBoundingClientRect().height")
    window = page.evaluate("window.innerHeight")
    assert tall >= window * 6, f"the held band is {tall} tall against a {window} window"
    reduced_page.goto(f"{app_base}/")
    reduced_page.wait_for_selector("[data-band='held']", state="attached")
    short = reduced_page.evaluate("document.querySelector(\"[data-band='held']\").getBoundingClientRect().height")
    assert short <= window * 1.5, f"under reduced motion the held band is still {short} tall"
    assert reduced_page.get_by_text("Innovate").count() >= 1, "under reduced motion the held words are absent"


def test_pointer_readout_follows_the_pointer(page, app_base):
    """The frame's readout shows the pointer position as two zero-padded four-digit numbers."""
    page.goto(f"{app_base}/")
    page.wait_for_selector("[data-scroller]", state="attached")
    page.mouse.move(100, 200)
    page.get_by_text(re.compile(r"0100\s*X\s*0200\s*Y")).first.wait_for()
    page.mouse.move(640, 360)
    page.get_by_text(re.compile(r"0640\s*X\s*0360\s*Y")).first.wait_for()
