"""The one pytest module for deku/editorial-photography-exhibition-vb.

Every section and every declared slot is merged here. Assertions are black box: HTTP
against the deployed app, rows read through the backend capability, mail read through
the inbox capability and its message API, and rendered surfaces read through a real
browser page where the ask is a rendered one.
"""

from __future__ import annotations

import datetime
import re

import httpx
from appclient import api_base, client, login
from conftest import (AURA_MANIFESTO, CAPACITY, CHOOSER_PROMPT, CITY, CONFIRMED, CANCELLED,
                      DEBUG_MARKERS, DEEPEST_TEXT_JS, ENTRY_TIMES, EXHIBITION_TITLE, FRAMES,
                      FRAME_FIELDS, GALLERIES, GALLERY_FIELDS, GAZETTE_MANIFESTO,
                      LARGEST_CONTAINING_TEXT_JS, LARGEST_EXACT_TEXT_JS, LOCKUP_WORDS,
                      LOOPING_ANIMATIONS_JS, MENU_LINKS, MENU_ROUTES, NARROW_WIDTH, NOT_FOUND_COPY,
                      PAGE_TITLES, PRIVACY_NOUNS, PROBE_PASSWORD, PUBLIC_ROUTES, ASSET_TYPES, CROPS,
                      RESERVATION_FIELDS, RUN_DAYS, SCROLL_PROMPT, SECRET_MARKERS, SEED_RESERVATIONS,
                      SEED_STARTED, SEEDED_NAMES, SEEDED_PASSWORD, SELECTION_FIELDS, SLOT_COUNT,
                      SLOT_FIELDS, SOUND_OFF, SUBJECT_PREFIX, SUBTITLE_LINE_ONE, TABLES,
                      TERMS_SENTENCE, VENUE, VISITOR2_EMAIL, VISITOR3_EMAIL, VISITOR_EMAIL, WIDE_WIDTH,
                      all_slots, confirmed_code, exhibition, families, fetch_page, fill_slot, frame_id,
                      gallery, me, menu_control, page_url, poll_until, race, refusal, rendered,
                      reservation_body, reserve, reserve_fresh, run_start, save, selection, settle,
                      sign_in_page, signup, slot_by_id, slot_date, slot_on, slot_time, tomorrow,
                      unique_email, unique_local, untouched_slot)
from playwright.sync_api import expect

CODE_PATTERN = re.compile(r"^[A-Z0-9]{8}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SIZE_TOLERANCE = 0.5
MANIFESTO_OPENING = "AURA has long been a partner for women in Hollywood"
SOUND_IN_OVERLAY_JS = (
    "() => { for (const link of document.querySelectorAll('a')) { "
    "if (!link.textContent.split(/[\\s\\u00a0]+/).join(' ').trim().startsWith('AURA introduction')) continue; "
    "let node = link.parentElement; "
    "while (node && node !== document.body) { "
    "if (/Sound:\\s*(off|on)/.test(node.textContent)) { "
    "const views = [...node.querySelectorAll('button, a')].filter(e => e.textContent.trim() === 'View'); "
    "if (views.length === 0) return true; break; } "
    "node = node.parentElement; } } return false; }"
)
AUDIO_PROBE_SCRIPT = (
    "window.__soundStarts = 0; "
    "const bump = () => { window.__soundStarts += 1; }; "
    "if (window.AudioScheduledSourceNode) { const start = AudioScheduledSourceNode.prototype.start; "
    "AudioScheduledSourceNode.prototype.start = function () { bump(); return start.apply(this, arguments); }; } "
    "if (window.HTMLMediaElement) { const play = HTMLMediaElement.prototype.play; "
    "HTMLMediaElement.prototype.play = function () { bump(); return play.apply(this, arguments); }; }"
)
MASTHEAD_RECTS_JS = (
    "text => [...document.body.querySelectorAll('*')]"
    ".filter(e => e.textContent.split(/[\\s\\u00a0]+/).join('') === text)"
    ".map(e => { const r = e.getBoundingClientRect(); return {x: r.x, y: r.y, width: r.width, height: r.height}; })"
    ".filter(r => r.width > 0 && r.height > 0)"
)
FIELD_MESSAGE_JS = (
    "label => { const field = [...document.querySelectorAll('input, select, textarea')].find(e => "
    "(e.labels && [...e.labels].some(l => l.textContent.trim().startsWith(label))) || "
    "(e.getAttribute('aria-label') || '').startsWith(label)); "
    "if (!field) return {described: '', nearby: ''}; "
    "const ids = ((field.getAttribute('aria-describedby') || '') + ' ' + (field.getAttribute('aria-errormessage') || '')).split(/\\s+/).filter(Boolean); "
    "const described = ids.map(id => (document.getElementById(id) || {}).textContent || '').join(' '); "
    "let node = field.parentElement, nearby = ''; "
    "for (let i = 0; i < 2 && node; i += 1) { nearby = node.textContent; node = node.parentElement; } "
    "return {described: described, nearby: nearby}; }"
)
ROW_TABULAR_JS = (
    "([code, time]) => { let node = [...document.body.querySelectorAll('*')].filter(e => e.textContent.includes(code)).pop(); "
    "while (node && !node.textContent.includes(time)) node = node.parentElement; "
    "if (!node) return null; "
    "const own = e => [...e.childNodes].filter(c => c.nodeType === 3).map(c => c.textContent).join(''); "
    "const figures = [node, ...node.querySelectorAll('*')].filter(e => { const t = own(e); "
    "return t.includes(code) || t.includes(time) || /20\\d\\d/.test(t); }); "
    "return figures.length >= 2 && figures.every(e => { const st = getComputedStyle(e); "
    "return st.fontVariantNumeric.includes('tabular-nums') || st.fontFeatureSettings.includes('tnum'); }); }"
)
TABULAR_JS = (
    "root => { const nodes = [root, ...root.querySelectorAll('*')]; "
    "return nodes.some(e => { const st = getComputedStyle(e); "
    "return st.fontVariantNumeric.includes('tabular-nums') || st.fontFeatureSettings.includes('tnum'); }); }"
)


def utc_moment(value) -> datetime.datetime:
    moment = datetime.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    assert moment.utcoffset() == datetime.timedelta(0), f"{value} is not written in UTC"
    return moment


def size_at(page, route: str, width: int, script: str, text: str) -> float:
    page.set_viewport_size({"width": width, "height": 900})
    page.goto(page_url(route))
    settle(1.0)
    return float(rendered(page, script, text)["size"])


def assert_fluid(page, route: str, script: str, text: str, low: float, high: float, what: str) -> None:
    narrow = size_at(page, route, NARROW_WIDTH, script, text)
    assert abs(narrow - low) <= SIZE_TOLERANCE, (
        f"{what} on {route} measures {narrow}px at {NARROW_WIDTH} wide, expected {low}px")
    wide = size_at(page, route, WIDE_WIDTH, script, text)
    assert abs(wide - high) <= SIZE_TOLERANCE, (
        f"{what} on {route} measures {wide}px at {WIDE_WIDTH} wide, expected {high}px")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", str(text))


def overlaps(box: dict, rect: dict) -> bool:
    return (min(box["x"] + box["width"], rect["x"] + rect["width"]) > max(box["x"], rect["x"])
            and min(box["y"] + box["height"], rect["y"] + rect["height"]) > max(box["y"], rect["y"]))


def open_frame(page, name: str) -> None:
    image = page.get_by_role("img", name=name, exact=True).first
    image.scroll_into_view_if_needed()
    image.click()
    settle(1.0)


def labelled_control(page, name: str):
    return page.get_by_role("button", name=name, exact=True).or_(
        page.get_by_role("link", name=name, exact=True))


def test_every_exhibition_route_answers_for_a_signed_out_visitor():
    for route in PUBLIC_ROUTES:
        response = fetch_page(route)
        assert response.status_code == 200, (
            f"GET {route} with no session returned {response.status_code}: {response.text[:300]}")
        assert "html" in response.headers.get("content-type", "").lower(), (
            f"GET {route} did not answer with an HTML document: {response.headers.get('content-type')}")


def test_document_titles_name_each_exhibition_route(page):
    for route, title in PAGE_TITLES:
        page.goto(page_url(route))
        assert page.title().strip() == title, (
            f"the document title of {route} reads {page.title()!r}, expected {title!r}")


def test_landing_copy_carries_lockup_subtitle_and_prompt(page):
    page.goto(page_url("/"))
    markup = page.content()
    for word in LOCKUP_WORDS:
        assert word in markup, f"the landing carries no {word!r} in its lock-up"
    assert SUBTITLE_LINE_ONE in markup, f"the landing subtitle {SUBTITLE_LINE_ONE!r} is missing"
    assert CITY in markup, f"the landing subtitle's second line {CITY!r} is missing"
    assert CHOOSER_PROMPT in markup, f"the chooser prompt {CHOOSER_PROMPT!r} is missing"


def test_chooser_covers_link_to_both_introductions(page):
    page.goto(page_url("/"))
    assert page.locator('a[href$="/aura-intro"]').count() >= 1, (
        "the landing carries no chooser cover linking to /aura-intro")
    assert page.locator('a[href$="/gazette-intro"]').count() >= 1, (
        "the landing carries no chooser cover linking to /gazette-intro")


def test_landing_carries_no_menu_control(page):
    page.goto(page_url("/"))
    menus = menu_control(page).count()
    assert menus == 0, f"the landing carries {menus} Menu control(s); the landing has no menu"
    banners = page.get_by_role("banner").count()
    assert banners == 0, f"the landing carries {banners} header landmark(s); the landing has no header"


def test_routes_arrive_server_rendered_with_their_copy():
    landing = fetch_page("/")
    assert CHOOSER_PROMPT in landing.text, (
        "the first HTML response for / does not carry the chooser prompt, so the page copy is "
        "not rendered on the server")
    aura_intro = fetch_page("/aura-intro")
    assert MANIFESTO_OPENING in aura_intro.text, (
        "the first HTML response for /aura-intro does not carry the AURA manifesto")
    gazette_intro = fetch_page("/gazette-intro")
    assert "Gazette has spent decades writing about the men of Hollywood" in gazette_intro.text, (
        "the first HTML response for /gazette-intro does not carry the Gazette manifesto")


def test_lockup_connector_names_pinyon_script(page):
    page.goto(page_url("/"))
    settle(1.0)
    connector = rendered(page, LARGEST_EXACT_TEXT_JS, "and")
    assert families(connector["family"])[0] == "pinyon script", (
        f"the lock-up connector 'and' names the font stack {connector['family']!r}, "
        f"expected Pinyon Script first")


def test_aura_manifesto_returns_the_three_pinned_paragraphs(page):
    intro = gallery("aura")["introduction"]
    assert {"heading", "manifesto", "photographer"} <= set(intro), (
        f"the AURA introduction carries fields {sorted(intro)}, expected heading, manifesto, photographer")
    assert intro.get("heading") == "THE NEW HOLLYWOOD", (
        f"the AURA introduction heading reads {intro.get('heading')!r}, expected 'THE NEW HOLLYWOOD'")
    manifesto = [str(p).strip() for p in intro["manifesto"]]
    assert manifesto == list(AURA_MANIFESTO), (
        f"GET /api/galleries/aura returns a manifesto that differs from the pinned three "
        f"paragraphs: {manifesto!r}")
    page.goto(page_url("/aura-intro"))
    shown = compact(page.evaluate("() => document.body.textContent"))
    for paragraph in AURA_MANIFESTO:
        assert compact(paragraph) in shown, f"/aura-intro does not render the paragraph {paragraph[:60]!r}"

def test_gazette_manifesto_returns_the_three_pinned_paragraphs(page):
    intro = gallery("gazette")["introduction"]
    assert intro.get("heading") == "THE NEW HOLLYWOOD", (
        f"the Gazette introduction heading reads {intro.get('heading')!r}, expected 'THE NEW HOLLYWOOD'")
    manifesto = [str(p).strip() for p in intro["manifesto"]]
    assert manifesto == list(GAZETTE_MANIFESTO), (
        f"GET /api/galleries/gazette returns a manifesto that differs from the pinned three "
        f"paragraphs: {manifesto!r}")
    page.goto(page_url("/gazette-intro"))
    shown = compact(page.evaluate("() => document.body.textContent"))
    for paragraph in GAZETTE_MANIFESTO:
        assert compact(paragraph) in shown, f"/gazette-intro does not render the paragraph {paragraph[:60]!r}"

def test_introduction_credits_name_each_photographer(page):
    for slug, title, face, ground, mast, order, photographer in GALLERIES:
        intro = gallery(slug)["introduction"]
        assert intro.get("photographer") == photographer, (
            f"the {title} introduction credits {intro.get('photographer')!r}, expected {photographer!r}")
        page.goto(page_url(f"/{slug}-intro"))
        text = page.locator("body").inner_text()
        credit = f"Photographs by {photographer}"
        assert credit in text, f"/{slug}-intro does not show the credit {credit!r}"
        assert f"for {title}" in text, f"/{slug}-intro does not show the credit line 'for {title}'"
        assert text.index(credit) < text.rindex(f"for {title}"), (
            f"/{slug}-intro does not set 'for {title}' after {credit!r}")


def test_manifesto_body_holds_16px_narrow_and_20px_wide(page):
    assert_fluid(page, "/aura-intro", DEEPEST_TEXT_JS, MANIFESTO_OPENING, 16, 20, "the manifesto body")


def test_type_never_steps_at_a_breakpoint(page):
    page.goto(page_url("/aura-intro"))
    settle(1.0)
    previous = None
    for width in range(380, 1911, 10):
        page.set_viewport_size({"width": width, "height": 900})
        body = float(rendered(page, DEEPEST_TEXT_JS, MANIFESTO_OPENING)["size"])
        heading = float(rendered(page, LARGEST_CONTAINING_TEXT_JS, "HOLLYWOOD")["size"])
        if previous is not None:
            assert body >= previous[0] - 0.05 and body - previous[0] <= 0.5, (
                f"the manifesto body jumps from {previous[0]}px to {body}px at {width} wide")
            assert heading >= previous[1] - 0.05 and heading - previous[1] <= 1.5, (
                f"the introduction heading jumps from {previous[1]}px to {heading}px at {width} wide")
        previous = (body, heading)


def test_type_roles_hold_their_pinned_ranges(page):
    roles = (
        ("/signup", "Display name", 12, 14, "the form field label"),
        ("/", CHOOSER_PROMPT, 30, 40, "the chooser prompt"),
        (f"/{unique_local()}", "Page Not Found", 35, 60, "the not-found heading"),
        ("/aura", "AURA introduction", 36, 54, "the menu overlay link"),
    )
    for route, text, low, high, what in roles:
        for width, expected in ((NARROW_WIDTH, low), (WIDE_WIDTH, high)):
            page.set_viewport_size({"width": width, "height": 900})
            page.goto(page_url(route))
            if text == "AURA introduction":
                menu_control(page).first.click()
            settle(1.0)
            size = float(rendered(page, DEEPEST_TEXT_JS, text)["size"])
            assert abs(size - expected) <= SIZE_TOLERANCE, (
                f"{what} measures {size}px at {width} wide, expected {expected}px")
    sign_in_page(page, VISITOR3_EMAIL, SEEDED_PASSWORD)
    for width, expected in ((NARROW_WIDTH, 20), (WIDE_WIDTH, 30)):
        page.set_viewport_size({"width": width, "height": 900})
        page.goto(page_url("/visit"))
        settle(1.0)
        size = float(rendered(page, DEEPEST_TEXT_JS, "Your visits")["size"])
        assert abs(size - expected) <= SIZE_TOLERANCE, (
            f"the Your visits heading measures {size}px at {width} wide, expected {expected}px")


def test_introduction_heading_holds_50px_narrow_and_100px_wide(page):
    assert_fluid(page, "/aura-intro", LARGEST_CONTAINING_TEXT_JS, "HOLLYWOOD", 50, 100,
                 "the introduction heading")


def test_gallery_scroll_prompt_reads_scroll_to_explore(page):
    for slug in ("aura", "gazette"):
        page.goto(page_url(f"/{slug}"))
        assert SCROLL_PROMPT in page.content(), f"/{slug} carries no {SCROLL_PROMPT!r} prompt"


def test_gallery_api_returns_frames_in_column_order():
    for slug in ("aura", "gazette"):
        body = gallery(slug)
        missing = (GALLERY_FIELDS | {"introduction", "frames"}) - set(body)
        assert not missing, f"GET /api/galleries/{slug} lacks the fields {sorted(missing)}"
        subjects = [f.get("subject") for f in body.get("frames", [])]
        expected = [row[2] for row in FRAMES if row[0] == slug]
        assert subjects == expected, (
            f"GET /api/galleries/{slug} returns frames {subjects}, expected column order {expected}")
        for frame in body["frames"]:
            assert FRAME_FIELDS <= set(frame), (
                f"a frame in GET /api/galleries/{slug} carries {sorted(frame)}, "
                f"expected {sorted(FRAME_FIELDS)}")


def test_galleries_api_returns_two_galleries_in_order(anon_client, db):
    response = anon_client.get("/galleries")
    assert response.status_code == 200, (
        f"GET /api/galleries returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    assert isinstance(body, list), f"GET /api/galleries is not a top-level array: {response.text[:300]}"
    assert [g.get("slug") for g in body] == ["aura", "gazette"], (
        f"GET /api/galleries lists {[g.get('slug') for g in body]}, expected aura then gazette")
    for row, (slug, title, face, ground, mast, order, _) in zip(body, GALLERIES):
        assert GALLERY_FIELDS <= set(row), f"gallery {slug} carries {sorted(row)}"
        observed = (row.get("title"), row.get("wordmarkFace"), row.get("ground"),
                    row.get("mastheadColour"), row.get("order"))
        assert observed == (title, face, ground, mast, order), (
            f"gallery {slug} reads {observed}, expected {(title, face, ground, mast, order)}")
    assert db.count("exhibitions") == 1 and db.count("galleries") == 2, (
        f"the site holds {db.count('exhibitions')} exhibitions and {db.count('galleries')} galleries")


def test_frame_api_returns_subject_photographer_publication_year(anon_client):
    identifier, slug = frame_id("Odessa Vane")
    response = anon_client.get(f"/frames/{identifier}")
    assert response.status_code == 200, (
        f"GET /api/frames/<id> for Odessa Vane returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    assert FRAME_FIELDS <= set(body), f"GET /api/frames/<id> carries {sorted(body)}, expected {sorted(FRAME_FIELDS)}"
    observed = (body.get("id"), body.get("subject"), body.get("photographer"), body.get("publication"),
                body.get("year"), body.get("galleryId"), body.get("aspect"), body.get("crop"), body.get("order"))
    expected = (identifier, "Odessa Vane", "Celine Armand", "AURA", 2025, "aura", "portrait", "240x320", 1)
    assert observed == expected, f"GET /api/frames/<id> for Odessa Vane reads {observed}, expected {expected}"

def test_unknown_gallery_slug_answers_not_found(anon_client):
    response = anon_client.get(f"/galleries/{unique_local()}")
    assert response.status_code == 404, (
        f"GET /api/galleries/<unknown> returned {response.status_code}, expected not-found")


def test_unknown_frame_id_answers_not_found(anon_client):
    response = anon_client.get("/frames/987654321")
    assert response.status_code == 404, (
        f"GET /api/frames/987654321 returned {response.status_code}, expected not-found")


def test_frame_alternative_text_names_subject_and_photographer(page):
    page.goto(page_url("/aura"))
    expected = "Odessa Vane, photographed by Celine Armand"
    assert page.get_by_role("img", name=expected, exact=True).count() >= 1, (
        f"/aura exposes no image named {expected!r}")
    page.goto(page_url("/gazette"))
    expected = "Rafe Okonkwo, photographed by Tomas Ekwueme"
    assert page.get_by_role("img", name=expected, exact=True).count() >= 1, (
        f"/gazette exposes no image named {expected!r}")


def test_pointer_mark_and_grain_never_intercept_pointer_events(page):
    page.goto(page_url("/aura"))
    image = page.get_by_role("img", name="Wren Adebayo, photographed by Noor Haddad", exact=True).first
    image.scroll_into_view_if_needed()
    box = image.bounding_box()
    assert box is not None, "the Wren Adebayo frame has no rendered box on /aura"
    x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    page.mouse.move(x, y)
    page.mouse.click(x, y)
    expect(page.get_by_text("Noor Haddad").first).to_be_visible(timeout=15000)


def test_seeded_frames_match_the_frame_table(db):
    assert db.count("frames") == len(FRAMES), (
        f"the frames table holds {db.count('frames')} rows, expected {len(FRAMES)}")
    titles = {slug: title for slug, title, *_ in GALLERIES}
    for slug in ("aura", "gazette"):
        frames = {f.get("subject"): f for f in gallery(slug).get("frames", [])}
        for row in (r for r in FRAMES if r[0] == slug):
            frame = frames.get(row[2])
            assert frame is not None, f"seeded frame {row[2]} is missing from /api/galleries/{slug}"
            observed = (frame.get("order"), frame.get("photographer"), frame.get("year"),
                        frame.get("aspect"), frame.get("crop"))
            assert observed == row[1:2] + row[3:], f"frame {row[2]} reads {observed}, expected {row}"
            assert frame.get("crop") in CROPS, f"frame {row[2]} carries crop {frame.get('crop')!r}"
            assert frame.get("publication") == titles[slug], (
                f"frame {row[2]} names publication {frame.get('publication')!r}, expected {titles[slug]!r}")


def test_mastheads_are_live_text_over_each_photograph(page):
    for slug, title in (("aura", "AURA"), ("gazette", "Gazette")):
        page.goto(page_url(f"/{slug}"))
        settle(1.0)
        images = page.get_by_role("img", name=re.compile(r"photographed by"))
        count = images.count()
        assert count >= len([r for r in FRAMES if r[0] == slug]), f"/{slug} exposes {count} photographs"
        rects = page.evaluate(MASTHEAD_RECTS_JS, title)
        for index in range(count):
            box = images.nth(index).bounding_box()
            assert box is not None, f"photograph {index + 1} on /{slug} has no rendered box"
            assert any(overlaps(box, rect) for rect in rects), (
                f"photograph {index + 1} on /{slug} carries no live-text {title} masthead over it")


def test_frame_detail_controls_carry_text_labels(page):
    page.goto(page_url("/aura"))
    open_frame(page, "Lilou Marchetti, photographed by Celine Armand")
    for name in ("Previous", "Next", "Close"):
        assert labelled_control(page, name).count() >= 1, (
            f"the open frame detail exposes no control labelled {name!r} to assistive technology")


def test_manifesto_names_bodoni_moda_at_the_wordmark_weight(page):
    page.goto(page_url("/aura-intro"))
    settle(1.0)
    body = rendered(page, DEEPEST_TEXT_JS, MANIFESTO_OPENING)
    assert families(body["family"])[0] == "bodoni moda", (
        f"the manifesto names the font stack {body['family']!r}, expected Bodoni Moda first")
    page.goto(page_url("/aura"))
    settle(1.0)
    wordmark = rendered(page, LARGEST_EXACT_TEXT_JS, "AURA")
    assert str(body["weight"]) == str(wordmark["weight"]), (
        f"the manifesto is set at weight {body['weight']} but the AURA wordmark at {wordmark['weight']}; "
        f"both use the serif's thinnest weight")


def test_chooser_prompt_and_not_found_lines_name_inter_light(page):
    for route, text in (("/", CHOOSER_PROMPT), (f"/{unique_local()}", "You may have made a mistake.")):
        page.goto(page_url(route))
        settle(1.0)
        found = rendered(page, DEEPEST_TEXT_JS, text)
        assert families(found["family"])[0] == "inter", (
            f"{text!r} names the font stack {found['family']!r}, expected Inter first")
        assert str(found["weight"]) == "300", f"{text!r} is set at weight {found['weight']}, expected 300"


def test_aura_wordmark_names_bodoni_moda_first(page):
    page.goto(page_url("/aura"))
    settle(1.0)
    wordmark = rendered(page, LARGEST_EXACT_TEXT_JS, "AURA")
    stack = families(wordmark["family"])
    assert stack[:3] == ["bodoni moda", "didot", "times new roman"], (
        f"the AURA wordmark names the font stack {wordmark['family']!r}, expected Bodoni Moda, Didot, "
        f"Times New Roman first")
    assert "serif" in stack[3:], f"the AURA wordmark stack {wordmark['family']!r} ends without serif"


def test_wordmark_holds_50px_narrow_and_100px_wide(page):
    assert_fluid(page, "/aura", LARGEST_EXACT_TEXT_JS, "AURA", 50, 100, "the AURA wordmark")


def test_menu_overlay_links_every_route(page):
    page.goto(page_url("/aura"))
    menu_control(page).first.click()
    for text, route in MENU_LINKS:
        link = page.get_by_role("link", name=re.compile(rf"^{re.escape(text)}")).first
        expect(link).to_be_visible(timeout=10000)
        href = link.get_attribute("href") or ""
        assert href.rstrip("/").endswith(route), (
            f"the overlay link {text!r} points at {href!r}, expected {route}")
    labelled_control(page, "Sign in").first.click()
    page.wait_for_url(lambda url: "/login" in url, timeout=15000)


def test_menu_overlay_states_exhibition_facts(page):
    facts = exhibition()
    page.goto(page_url("/gazette"))
    menu_control(page).first.click()
    settle(1.0)
    text = page.locator("body").inner_text()
    for fact in (EXHIBITION_TITLE, VENUE, CITY):
        assert fact in text, f"the open menu overlay does not state {fact!r}"
    run = f"{str(facts['runStart'])[:10]} to {str(facts['runEnd'])[:10]}"
    assert run in text, f"the open menu overlay does not state the run as {run!r}"


def test_exhibition_api_returns_title_venue_city_run(db):
    facts = exhibition()
    assert (facts.get("title"), facts.get("venue"), facts.get("city")) == (EXHIBITION_TITLE, VENUE, CITY), (
        f"GET /api/exhibition reads {facts}")
    start = datetime.date.fromisoformat(str(facts["runStart"])[:10])
    end = datetime.date.fromisoformat(str(facts["runEnd"])[:10])
    assert (end - start).days == RUN_DAYS - 1, (
        f"the run spans {start} to {end}, which is not thirty days")
    assert db.count("exhibitions") == 1, f"the exhibitions table holds {db.count('exhibitions')} rows"


def test_sound_control_starts_off(page):
    sign_in_page(page, VISITOR3_EMAIL, SEEDED_PASSWORD)
    for route in MENU_ROUTES + ("/selection",):
        page.goto(page_url(route))
        expect(page.get_by_text(SOUND_OFF).first).to_be_visible(timeout=10000)
    page.goto(page_url("/gazette"))
    menu_control(page).first.click()
    settle(1.0)
    assert page.evaluate(SOUND_IN_OVERLAY_JS), "the open menu overlay carries no sound control of its own"

def test_no_sound_plays_before_a_gesture(page):
    page.add_init_script(AUDIO_PROBE_SCRIPT)
    for route in ("/", "/aura"):
        page.goto(page_url(route))
        page.mouse.move(640, 450)
        page.mouse.wheel(0, 1200)
        settle()
        starts = page.evaluate("() => window.__soundStarts")
        assert starts == 0, f"{route} started {starts} sound source(s) before the visitor pressed the sound control"


def test_interface_controls_name_inter_light(page):
    page.goto(page_url("/aura"))
    menu = menu_control(page).first
    family = menu.evaluate("e => getComputedStyle(e).fontFamily")
    weight = menu.evaluate("e => getComputedStyle(e).fontWeight")
    assert families(family)[0] == "inter", f"the Menu control's font family is {family!r}, expected Inter first"
    assert str(weight) == "300", f"the Menu control's font weight is {weight!r}, expected 300"


def test_go_to_gallery_holds_14px_narrow_and_16px_wide(page):
    assert_fluid(page, "/aura-intro", DEEPEST_TEXT_JS, "Go to Gallery", 14, 16, "Go to Gallery")

def test_scroll_prompt_names_inter_at_400_or_500(page):
    page.goto(page_url("/aura"))
    settle(1.0)
    prompt = rendered(page, DEEPEST_TEXT_JS, SCROLL_PROMPT)
    assert families(prompt["family"])[0] == "inter", (
        f"the scroll prompt names the font stack {prompt['family']!r}, expected Inter first")
    assert str(prompt["weight"]) in ("400", "500"), (
        f"the scroll prompt is set at weight {prompt['weight']!r}, expected 400 or 500")


def test_header_controls_offer_touch_targets_of_44_by_44(page):
    page.goto(page_url("/aura"))
    for name in ("View", "Menu"):
        box = labelled_control(page, name).first.bounding_box()
        assert box is not None, f"the {name} control has no rendered box on /aura"
        assert box["width"] >= 44 and box["height"] >= 44, (
            f"the {name} control measures {box['width']} by {box['height']}, under 44 by 44")
    page.goto(page_url("/aura-intro"))
    button = labelled_control(page, "Go to Gallery").first
    button.scroll_into_view_if_needed()
    box = button.bounding_box()
    assert box is not None and box["width"] >= 44 and box["height"] >= 44, (
        f"Go to Gallery measures {box}, under 44 by 44")


def test_menu_control_appears_on_the_exhibition_routes(page):
    for route in MENU_ROUTES:
        page.goto(page_url(route))
        expect(menu_control(page).first).to_be_attached(timeout=10000)


def test_gazette_wordmark_names_playfair_display_italic(page):
    page.goto(page_url("/gazette"))
    settle(1.0)
    wordmark = rendered(page, LARGEST_EXACT_TEXT_JS, "Gazette")
    assert families(wordmark["family"])[0] == "playfair display", (
        f"the Gazette wordmark names the font stack {wordmark['family']!r}, expected Playfair Display first")
    assert wordmark["style"] == "italic", f"the Gazette wordmark is set {wordmark['style']!r}, expected italic"


def test_signup_creates_visitor_row_carrying_display_name(anon_client, db):
    address = unique_email()
    response = anon_client.post("/auth/signup", json={
        "email": address, "password": PROBE_PASSWORD, "displayName": "Probe Visitor"})
    assert response.status_code in (200, 201), (
        f"POST /api/auth/signup returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    assert body.get("email") == address and body.get("displayName") == "Probe Visitor", (
        f"signup returned {body}")
    assert isinstance(body.get("id"), int), f"signup returned no integer id: {body}"
    row = db.visitor(address)
    assert row is not None, f"signup wrote no visitors row for {address}"
    assert row.get("display_name") == "Probe Visitor", f"visitors row carries {row.get('display_name')!r}"


def test_signup_stores_the_email_lowercased(anon_client, db):
    local = unique_local()
    response = anon_client.post("/auth/signup", json={
        "email": f"{local.upper()}@Example.COM", "password": PROBE_PASSWORD, "displayName": "Case Probe"})
    assert response.status_code in (200, 201), (
        f"POST /api/auth/signup returned {response.status_code}: {response.text[:400]}")
    assert db.visitor(f"{local}@example.com") is not None, (
        "a mixed-case signup email was not stored lowercased in visitors")


def test_signup_with_registered_email_in_another_case_is_rejected(anon_client, db):
    address = unique_email()
    signup(address)
    response = anon_client.post("/auth/signup", json={
        "email": address.upper(), "password": PROBE_PASSWORD, "displayName": "Second Probe"})
    assert 400 <= response.status_code < 500, (
        f"a second signup for {address.upper()} returned {response.status_code}: {response.text[:300]}")
    assert db.count_visitors(email=address) == 1, (
        f"a duplicate signup left {db.count_visitors(email=address)} visitors rows for {address}")


def test_signup_with_empty_or_long_display_name_is_rejected(anon_client, db):
    for display_name in ("", "D" * 61):
        address = unique_email()
        response = anon_client.post("/auth/signup", json={
            "email": address, "password": PROBE_PASSWORD, "displayName": display_name})
        assert 400 <= response.status_code < 500, (
            f"a display name of {len(display_name)} characters returned {response.status_code}: "
            f"{response.text[:300]}")
        assert "displayname" in response.text.lower(), (
            f"the refusal does not name displayName: {response.text[:300]}")
        assert db.count_visitors(email=address) == 0, "a refused signup still wrote a visitors row"


def test_signup_password_shorter_than_ten_characters_is_rejected(anon_client, db):
    address = unique_email()
    response = anon_client.post("/auth/signup", json={
        "email": address, "password": "short-pw9", "displayName": "Short Probe"})
    assert 400 <= response.status_code < 500, (
        f"a nine-character password returned {response.status_code}: {response.text[:300]}")
    assert "password" in response.text.lower(), f"the refusal does not name password: {response.text[:300]}"
    assert db.count_visitors(email=address) == 0, "a refused signup still wrote a visitors row"


def test_signup_with_malformed_email_is_rejected(anon_client, db):
    local = unique_local()
    for malformed in ("not-an-email", f"{local}@localhost", "@example.com", f"{local}@@example.com"):
        name = f"Malformed {unique_local()}"
        response = anon_client.post("/auth/signup", json={
            "email": malformed, "password": PROBE_PASSWORD, "displayName": name})
        assert 400 <= response.status_code < 500, (
            f"the malformed email {malformed!r} returned {response.status_code}: {response.text[:300]}")
        assert "email" in response.text.lower(), f"the refusal does not name email: {response.text[:300]}"
        assert db.count_visitors(display_name=name) == 0, "a refused signup still wrote a visitors row"


def test_login_returns_access_token(anon_client):
    response = anon_client.post("/auth/login", json={"email": VISITOR_EMAIL, "password": SEEDED_PASSWORD})
    assert response.status_code == 200, (
        f"POST /api/auth/login returned {response.status_code}: {response.text[:400]}")
    assert response.json().get("access_token"), f"login returned no access_token: {response.text[:300]}"


def test_wrong_password_refusal_matches_unregistered_email_refusal(anon_client):
    wrong = anon_client.post("/auth/login", json={"email": VISITOR_EMAIL, "password": "not-the-password-26"})
    unknown = anon_client.post("/auth/login", json={"email": unique_email(), "password": "not-the-password-26"})
    assert 400 <= wrong.status_code < 500, (
        f"a wrong password returned {wrong.status_code}: {wrong.text[:300]}")
    assert wrong.status_code == unknown.status_code, (
        f"a wrong password answers {wrong.status_code} but an unregistered email answers "
        f"{unknown.status_code}")
    assert wrong.text == unknown.text, (
        f"the refusals differ, so they say which half was wrong: {wrong.text[:200]!r} vs "
        f"{unknown.text[:200]!r}")


def test_malformed_bearer_token_is_denied(visitor_token):
    with client("not-a-real-token") as forged:
        response = forged.get("/selection")
    assert response.status_code in (401, 403), (
        f"GET /api/selection with a malformed bearer token returned {response.status_code}")
    bare = httpx.get(f"{api_base()}/selection", headers={"Authorization": visitor_token}, timeout=30.0)
    assert bare.status_code in (401, 403), (
        f"GET /api/selection with the token but no Bearer scheme returned {bare.status_code}")
    scheme = httpx.get(f"{api_base()}/selection", headers={"Authorization": f"Bearer {visitor_token}"},
                       timeout=30.0)
    assert scheme.status_code == 200, (
        f"GET /api/selection with Bearer and the token returned {scheme.status_code}")


def test_me_returns_the_tokens_own_visitor():
    address, token = signup(display_name="Me Probe")
    body = me(token)
    assert (body.get("email"), body.get("displayName")) == (address, "Me Probe"), (
        f"GET /api/me returned {body}")
    assert isinstance(body.get("id"), int), f"GET /api/me returned a non-integer id {body.get('id')!r}"
    identifier, _ = frame_id("Odessa Vane")
    assert isinstance(identifier, int), f"frame ids are not integers: {identifier!r}"
    assert isinstance(all_slots()[0]["id"], int), "entry time ids are not integers"


def test_password_is_stored_hashed_rather_than_as_written(db):
    address, _ = signup()
    row = db.visitor(address)
    assert row is not None, f"signup wrote no visitors row for {address}"
    assert row.get("password_hash") and row.get("password_hash") != PROBE_PASSWORD, (
        "visitors.password_hash holds the password as written")
    assert PROBE_PASSWORD not in " ".join(str(v) for v in row.values()), (
        "the plain password appears in the visitors row")


def test_seeded_visitors_sign_in_with_the_corpus_password():
    for email, _ in SEEDED_NAMES:
        assert login(email, SEEDED_PASSWORD), f"{email} cannot sign in with the corpus password"


def test_seeded_visitors_carry_their_display_names():
    for email, name in SEEDED_NAMES:
        body = me(login(email, SEEDED_PASSWORD))
        assert body.get("displayName") == name, f"{email} carries display name {body.get('displayName')!r}"


def field_refused_inline(page, label: str) -> bool:
    found = page.evaluate(FIELD_MESSAGE_JS, label)
    named = label.lower()
    return named in found["described"].lower() or found["nearby"].lower().count(named) >= 2

def test_account_forms_reject_invalid_email_inline(page, db):
    name = f"Inline {unique_local()}"
    page.goto(page_url("/signup"))
    page.get_by_label("Email", exact=True).fill("not-an-email")
    page.get_by_label("Password", exact=True).fill(PROBE_PASSWORD)
    page.get_by_label("Display name", exact=True).fill(name)
    page.get_by_role("button", name="Create account", exact=True).click()
    settle()
    assert "/signup" in page.url, f"an invalid email left the signup route for {page.url}"
    assert field_refused_inline(page, "Email"), (
        "the signup form shows no inline message beside the email field naming it")
    assert page.get_by_label("Email", exact=True).input_value() == "not-an-email", (
        "the signup form dropped the typed email after the refusal")
    assert page.get_by_label("Display name", exact=True).input_value() == name, (
        "the signup form dropped the typed display name after the refusal")
    assert db.count_visitors(display_name=name) == 0, "an invalid signup form still wrote a visitors row"
    page.goto(page_url("/login"))
    page.get_by_label("Email", exact=True).fill("not-an-email")
    page.get_by_label("Password", exact=True).fill(PROBE_PASSWORD)
    page.get_by_role("button", name="Sign in", exact=True).click()
    settle()
    assert "/login" in page.url, f"an invalid email left the sign-in route for {page.url}"
    assert field_refused_inline(page, "Email"), "the sign-in form shows no inline refusal naming the email field"
    assert page.get_by_label("Email", exact=True).input_value() == "not-an-email", (
        "the sign-in form dropped the typed email after the refusal")


def test_account_forms_link_signup_terms_and_privacy(page):
    page.goto(page_url("/signup"))
    assert page.locator('a[href$="/terms"]').count() >= 1, "the signup form carries no link to /terms"
    assert page.locator('a[href$="/privacy"]').count() >= 1, "the signup form carries no link to /privacy"
    assert TERMS_SENTENCE in page.locator("body").inner_text(), (
        f"the signup form does not read {TERMS_SENTENCE!r}")
    assert page.get_by_role("button", name="Create account", exact=True).count() >= 1, (
        "the signup form carries no Create account button")
    page.goto(page_url("/login"))
    link = page.get_by_role("link", name="Create an account", exact=True).first
    assert (link.get_attribute("href") or "").rstrip("/").endswith("/signup"), (
        "the sign-in form carries no Create an account link to /signup")
    assert page.get_by_role("button", name="Sign in", exact=True).count() >= 1, (
        "the sign-in form carries no Sign in button")


def test_saving_a_frame_persists_a_selection_row(db):
    _, token = signup()
    visitor_id = me(token)["id"]
    identifier, slug = frame_id("Priya Castellane")
    response = save(token, identifier, slug)
    assert response.status_code == 200 and response.json().get("ok") is True, (
        f"POST /api/selection add returned {response.status_code}: {response.text[:400]}")
    assert db.count("selections", visitor_id=visitor_id, frame_id=identifier) == 1, (
        "a saved frame wrote no row in selections")


def test_removing_a_saved_frame_deletes_the_selection_row(db):
    _, token = signup()
    visitor_id = me(token)["id"]
    identifier, slug = frame_id("Saskia Moreau")
    save(token, identifier, slug)
    response = save(token, identifier, slug, action="remove")
    assert response.status_code == 200 and response.json().get("ok") is True, (
        f"POST /api/selection remove returned {response.status_code}: {response.text[:400]}")
    assert db.count("selections", visitor_id=visitor_id, frame_id=identifier) == 0, (
        "a removed frame still has a row in selections")
    assert str(identifier) not in {str(i.get("frameId")) for i in selection(token)}, (
        "a removed frame is still listed by GET /api/selection")


def test_selection_write_returns_the_whole_selection():
    _, token = signup()
    first, first_slug = frame_id("Odessa Vane")
    second, second_slug = frame_id("Kofi Brandt")
    save(token, first, first_slug)
    settle(1.2)
    response = save(token, second, second_slug)
    assert response.status_code == 200, f"POST /api/selection returned {response.status_code}"
    rows = response.json().get("selection", [])
    assert [str(item.get("frameId")) for item in rows][:2] == [str(second), str(first)], (
        f"the write returned selection {rows}, expected both frames newest first")
    for item in rows:
        assert SELECTION_FIELDS <= set(item), f"a selection row in the write carries {sorted(item)}"


def test_adding_an_already_saved_frame_leaves_one_selection_row(db):
    _, token = signup()
    visitor_id = me(token)["id"]
    identifier, slug = frame_id("Wren Adebayo")
    save(token, identifier, slug)
    again = save(token, identifier, slug)
    assert again.status_code == 200 and again.json().get("ok") is True, (
        f"adding an already saved frame returned {again.status_code}: {again.text[:300]}")
    assert db.count("selections", visitor_id=visitor_id, frame_id=identifier) == 1, (
        "adding a saved frame twice left more than one selections row")


def test_removing_an_unsaved_frame_returns_success():
    _, token = signup()
    identifier, slug = frame_id("Ines Valcourt")
    response = save(token, identifier, slug, action="remove")
    assert response.status_code == 200 and response.json().get("ok") is True, (
        f"removing an unsaved frame returned {response.status_code}: {response.text[:300]}")


def test_selection_list_returns_saved_frames_newest_first():
    _, token = signup()
    older, older_slug = frame_id("Saskia Moreau")
    newer, newer_slug = frame_id("Dario Fontaine")
    save(token, older, older_slug)
    settle(1.2)
    save(token, newer, newer_slug)
    rows = selection(token)
    listed = [str(item.get("frameId")) for item in rows]
    assert listed[:2] == [str(newer), str(older)], f"GET /api/selection lists {listed}, not newest first"
    for item in rows:
        assert SELECTION_FIELDS <= set(item), f"a selection row carries {sorted(item)}"
    assert {item.get("galleryId") for item in rows} == {"aura", "gazette"}, (
        f"selection rows name galleries {[item.get('galleryId') for item in rows]}, expected slugs")


def test_selection_survives_a_new_sign_in():
    address, token = signup()
    identifier, slug = frame_id("Teodor Lindqvist")
    save(token, identifier, slug)
    fresh = login(address, PROBE_PASSWORD)
    assert str(identifier) in {str(i.get("frameId")) for i in selection(fresh)}, (
        "a saved frame is missing from the selection after a new sign in")


def test_failed_save_returns_the_control_to_save_to_selection(page):
    address, _ = signup()
    sign_in_page(page, address, PROBE_PASSWORD)
    page.goto(page_url("/aura"))
    page.route("**/api/selection", lambda route: route.fulfill(
        status=503, content_type="application/json", body='{"ok": false, "message": "unavailable"}'))
    open_frame(page, "Ines Valcourt, photographed by Jun Takeda")
    before = {line.strip() for line in page.locator("body").inner_text().splitlines() if line.strip()}
    with page.expect_response(lambda r: "/api/selection" in r.url and r.request.method == "POST"):
        page.get_by_role("button", name="Save to selection", exact=True).first.click()
    expect(page.get_by_role("button", name="Save to selection", exact=True).first).to_be_visible(timeout=15000)
    settle(0.5)
    assert page.get_by_role("button", name="Saved", exact=True).count() == 0, (
        "a failed save left the control reading Saved")
    text = page.locator("body").inner_text()
    after = {line.strip() for line in text.splitlines() if line.strip()}
    assert after - before - {"Save to selection", "Saved"}, (
        "a failed save shows no message in place saying the frame was not saved")
    for raw in ('{"ok"', "Traceback", "TypeError", "Service Unavailable", "undefined"):
        assert raw not in text, f"a failed save shows a raw error ({raw!r})"


def test_concurrent_saves_of_one_frame_leave_one_selection_row(db):
    _, token = signup()
    visitor_id = me(token)["id"]
    identifier, slug = frame_id("Elias Navarro")
    race([lambda: save(token, identifier, slug), lambda: save(token, identifier, slug)])
    assert db.count("selections", visitor_id=visitor_id, frame_id=identifier) == 1, (
        "two simultaneous saves of one frame left more than one selections row")


def test_seeded_selections_match_the_seed(visitor_token, visitor2_token):
    listed = [str(i.get("frameId")) for i in selection(visitor_token)]
    odessa, rafe = str(frame_id("Odessa Vane")[0]), str(frame_id("Rafe Okonkwo")[0])
    for subject, identifier in (("Odessa Vane", odessa), ("Rafe Okonkwo", rafe)):
        assert identifier in listed, f"{VISITOR_EMAIL} is missing seeded frame {subject}"
    assert listed.index(rafe) < listed.index(odessa), (
        f"{VISITOR_EMAIL} lists Odessa Vane before Rafe Okonkwo, but Rafe Okonkwo was saved after it")
    saved2 = {str(i.get("frameId")) for i in selection(visitor2_token)}
    assert str(frame_id("Lilou Marchetti")[0]) in saved2, f"{VISITOR2_EMAIL} is missing Lilou Marchetti"


def test_selection_write_with_unknown_frame_is_rejected(db):
    _, token = signup()
    visitor_id = me(token)["id"]
    refusal(save(token, 987654321, "aura"))
    assert db.count("selections", visitor_id=visitor_id) == 0, "an unknown frame still wrote a selections row"


def test_selection_write_with_mismatched_gallery_is_rejected(db):
    _, token = signup()
    visitor_id = me(token)["id"]
    identifier, _ = frame_id("Odessa Vane")
    refusal(save(token, identifier, "gazette"))
    assert db.count("selections", visitor_id=visitor_id) == 0, "a mismatched gallery still wrote a row"


def test_selection_write_with_unknown_action_is_rejected(db):
    _, token = signup()
    visitor_id = me(token)["id"]
    identifier, slug = frame_id("Odessa Vane")
    refusal(save(token, identifier, slug, action="toggle"))
    assert db.count("selections", visitor_id=visitor_id) == 0, "an unknown action still wrote a row"


def test_signup_and_saving_a_frame_send_no_email(inbox):
    address, token = signup()
    identifier, slug = frame_id("Kofi Brandt")
    save(token, identifier, slug)
    settle()
    assert inbox.count(to=address) == 0, f"signing up or saving a frame sent mail to {address}"


def test_signed_out_selection_write_is_denied(anon_client):
    identifier, slug = frame_id("Odessa Vane")
    response = anon_client.post("/selection", json={"frameId": identifier, "galleryId": slug, "action": "add"})
    assert response.status_code in (401, 403), (
        f"a signed-out POST /api/selection returned {response.status_code}, expected a denial")


def test_token_only_endpoints_deny_a_missing_token(anon_client, db):
    row = db.reservation("SEEDA14B")
    assert row is not None, "seeded reservation SEEDA14B is missing"
    for method, path in (("GET", "/me"), ("GET", "/reservations"), ("POST", f"/reservations/{row['id']}/cancel")):
        response = anon_client.request(method, path)
        assert response.status_code in (401, 403), (
            f"{method} /api{path} with no token returned {response.status_code}, expected a client-error denial")
    assert db.reservation("SEEDA14B").get("status") == CONFIRMED, "a signed-out cancel changed SEEDA14B"


def test_signed_out_selection_read_is_denied(anon_client):
    response = anon_client.get("/selection")
    assert response.status_code in (401, 403), (
        f"a signed-out GET /api/selection returned {response.status_code}, expected a denial")


def test_signed_out_reservation_request_is_denied(anon_client, db):
    email = unique_email()
    slot = untouched_slot()
    response = anon_client.post("/reservations", json=reservation_body(slot["id"], email=email))
    assert response.status_code in (401, 403), (
        f"a signed-out POST /api/reservations returned {response.status_code}, expected a denial")
    assert db.count("reservations", guest_email=email) == 0, "a denied reservation still wrote a row"


def test_cancelling_another_visitors_reservation_is_denied(visitor_token, db):
    row = db.reservation("SEEDE16F")
    assert row is not None, "seeded reservation SEEDE16F is missing"
    before = int(slot_by_id(row["slot_id"])["placesLeft"])
    with client(visitor_token) as visitor:
        response = visitor.post(f"/reservations/{row['id']}/cancel")
    assert response.status_code in (401, 403, 404), (
        f"visitor@example.com cancelling SEEDE16F returned {response.status_code}, expected a denial")
    assert db.reservation("SEEDE16F").get("status") == CONFIRMED, "a denied cancel changed SEEDE16F"
    assert int(slot_by_id(row["slot_id"])["placesLeft"]) == before, "a denied cancel changed the places left"


def test_reservation_list_holds_only_the_callers_reservations(visitor_token):
    _, reservation = reserve_fresh(untouched_slot()["id"])
    _, other = signup()
    with client(other) as visitor:
        codes = {r.get("code") for r in visitor.get("/reservations").json()}
    assert reservation["code"] not in codes, "another visitor's reservation appears in the caller's list"
    with client(visitor_token) as visitor:
        seeded = {r.get("code") for r in visitor.get("/reservations").json()}
    assert "SEEDA14B" not in seeded, "visitor2's seeded reservation appears in visitor@example.com's list"


def test_selection_list_holds_only_the_callers_frames():
    _, first = signup()
    identifier, slug = frame_id("Marcus Delacroix-Bell")
    save(first, identifier, slug)
    _, second = signup()
    assert selection(second) == [], "a fresh visitor's selection lists another visitor's frames"


def test_reservation_request_confirms_with_a_code():
    slot = untouched_slot()
    _, token = signup()
    reservation = confirmed_code(reserve(token, reservation_body(slot["id"])))
    assert str(reservation.get("slotId")) == str(slot["id"]), (
        f"the confirmation names entry time {reservation.get('slotId')}, expected {slot['id']}")
    assert reservation.get("id") is not None, "the confirmation carries no reservation id"


def test_confirmed_reservation_row_is_stored_in_reservations(db):
    slot = untouched_slot()
    email = unique_email()
    _, reservation = reserve_fresh(slot["id"], party=2, email=email)
    row = db.reservation(reservation["code"])
    assert row is not None, f"no reservations row carries code {reservation['code']}"
    observed = (row.get("status"), row.get("party_size"), row.get("guest_email"), str(row.get("slot_id")))
    assert observed == (CONFIRMED, 2, email, str(slot["id"])), f"the reservations row reads {observed}"


def test_reservation_code_is_eight_capitals_or_digits():
    _, reservation = reserve_fresh(untouched_slot()["id"])
    assert CODE_PATTERN.match(str(reservation["code"])), (
        f"reservation code {reservation['code']!r} is not 8 capital letters or digits")


def test_reservation_codes_are_unique_across_reservations(db):
    slot_id = untouched_slot()["id"]
    codes = [reserve_fresh(slot_id)[1]["code"] for _ in range(3)]
    assert len(set(codes)) == 3, f"three reservations share codes: {codes}"
    for code in codes:
        assert db.count("reservations", code=code) == 1, f"code {code} appears on more than one row"


def test_confirmation_email_reaches_the_reservation_address(inbox):
    email = unique_email()
    _, reservation = reserve_fresh(untouched_slot()["id"], email=email)
    message = poll_until(lambda: inbox.find(to=email, subject_contains=SUBJECT_PREFIX))
    assert message is not None, f"no confirmation mail reached {email} for {reservation['code']}"
    assert inbox.count(to=email) == 1, f"{email} received {inbox.count(to=email)} messages, expected one"


def test_confirmation_email_carries_no_cc_or_bcc(inbox, mail):
    email = unique_email()
    reserve_fresh(untouched_slot()["id"], email=email)
    poll_until(lambda: inbox.find(to=email, subject_contains=SUBJECT_PREFIX))
    found = mail.messages_to(email)
    assert len(found) == 1, f"expected one message to {email}, found {len(found)}"
    detail = mail.detail(found[0]["ID"])
    assert [str(a.get("Address")).lower() for a in detail.get("To") or []] == [email], (
        f"the confirmation is addressed to {detail.get('To')}")
    assert not detail.get("Cc") and not detail.get("Bcc"), (
        f"the confirmation carries cc {detail.get('Cc')} or bcc {detail.get('Bcc')}")


def test_confirmation_subject_begins_visit_reserved_with_the_code(inbox):
    email = unique_email()
    _, reservation = reserve_fresh(untouched_slot()["id"], email=email)
    message = poll_until(lambda: inbox.find(to=email, subject_contains=SUBJECT_PREFIX))
    assert message is not None, f"no confirmation mail reached {email}"
    assert message.subject.startswith(f"{SUBJECT_PREFIX} {reservation['code']}"), (
        f"the subject reads {message.subject!r}, expected 'Visit reserved: {reservation['code']}'")


def test_confirmation_body_names_venue_date_time_party_and_code(inbox, mail):
    email = unique_email()
    slot = untouched_slot()
    _, reservation = reserve_fresh(slot["id"], party=3, email=email)
    poll_until(lambda: inbox.find(to=email, subject_contains=SUBJECT_PREFIX))
    found = mail.messages_to(email)
    assert found, f"no confirmation mail reached {email}"
    detail = mail.detail(found[0]["ID"])
    text = f"{detail.get('Text') or ''} {detail.get('HTML') or ''}"
    for needle in (VENUE, slot_date(slot), f"{slot_time(slot)} UTC", reservation["code"]):
        assert needle in text, f"the confirmation body does not carry {needle!r}"
    remainder = text.replace(slot_date(slot), " ").replace(slot_time(slot), " ").replace(reservation["code"], " ")
    assert re.search(r"(?<![\d:-])3(?![\d:-])", remainder), "the confirmation body does not carry the party size 3"


def test_places_left_equals_capacity_minus_confirmed_party_sizes(db):
    slot = untouched_slot()
    reserve_fresh(slot["id"], party=3)
    after = slot_by_id(slot["id"])
    assert int(after["placesLeft"]) == CAPACITY - 3, (
        f"a party of 3 left placesLeft {after['placesLeft']}, expected {CAPACITY - 3}")
    assert db.confirmed_places(slot["id"]) == CAPACITY - int(after["placesLeft"]), (
        "placesLeft disagrees with the confirmed party sizes stored in reservations")


def test_concurrent_requests_for_the_last_place_confirm_exactly_one(db):
    slot_id = untouched_slot()["id"]
    fill_slot(slot_id, leave=1)
    _, first = signup()
    _, second = signup()
    results = race([lambda: reserve(first, reservation_body(slot_id)),
                    lambda: reserve(second, reservation_body(slot_id))])
    winners = [r for r in results if r.status_code in (200, 201)]
    losers = [r for r in results if 400 <= r.status_code < 500]
    assert len(winners) == 1 and len(losers) == 1, (
        f"two requests for the last place answered {[r.status_code for r in results]}")
    assert refusal(losers[0]).get("field") == "slotId", f"the losing refusal reads {losers[0].text[:300]}"
    assert db.confirmed_places(slot_id) == CAPACITY, "the confirmed party sizes no longer equal capacity"
    assert int(slot_by_id(slot_id)["placesLeft"]) == 0, "the contended entry time still shows a place"


def test_booked_places_never_exceed_capacity_under_concurrency(db):
    slot_id = untouched_slot()["id"]
    tokens = [signup()[1] for _ in range(6)]
    results = race([lambda t=t: reserve(t, reservation_body(slot_id, party=2)) for t in tokens])
    confirmed = sum(1 for r in results if r.status_code in (200, 201))
    booked = db.confirmed_places(slot_id)
    assert booked <= CAPACITY, f"simultaneous parties booked {booked} places into {CAPACITY}"
    assert booked == confirmed * 2, f"{confirmed} confirmations but {booked} places stored"
    assert int(slot_by_id(slot_id)["placesLeft"]) == CAPACITY - booked, "placesLeft disagrees with rows"


def test_party_larger_than_places_left_is_rejected(db):
    slot_id = untouched_slot()["id"]
    fill_slot(slot_id, leave=2)
    email = unique_email()
    _, token = signup()
    body = refusal(reserve(token, reservation_body(slot_id, party=3, email=email)))
    assert body.get("field") == "partySize", f"the refusal names {body.get('field')!r}, expected partySize"
    assert db.count("reservations", guest_email=email) == 0, "a refused party still wrote a row"


def test_party_size_outside_one_to_four_is_rejected():
    slot_id = untouched_slot()["id"]
    _, token = signup()
    for party in (0, 5, 2.5):
        body = refusal(reserve(token, reservation_body(slot_id, party=party)))
        assert body.get("field") == "partySize", f"party size {party} refusal names {body.get('field')!r}"


def test_reservation_for_a_past_entry_time_is_rejected():
    earliest = all_slots()[0]
    assert earliest.get("status") == "past", f"the run's first entry time reads {earliest.get('status')!r}"
    _, token = signup()
    body = refusal(reserve(token, reservation_body(earliest["id"])))
    assert body.get("field") == "slotId", f"a past entry time refusal names {body.get('field')!r}"


def test_reservation_for_a_full_entry_time_is_rejected(db):
    full = slot_on(tomorrow(), "16:00")
    _, token = signup()
    for party in (1, 2):
        email = unique_email()
        body = refusal(reserve(token, reservation_body(full["id"], party=party, email=email)))
        assert body.get("field") == "slotId", (
            f"a party of {party} for a full entry time names {body.get('field')!r}, expected slotId")
        assert db.count("reservations", guest_email=email) == 0, "a refused reservation still wrote a row"


def test_second_reservation_for_the_same_entry_time_is_rejected():
    slot_id = untouched_slot()["id"]
    _, token = signup()
    confirmed_code(reserve(token, reservation_body(slot_id)))
    body = refusal(reserve(token, reservation_body(slot_id)))
    assert body.get("field") == "slotId", f"a second reservation refusal names {body.get('field')!r}"


def test_reservation_missing_the_name_is_rejected():
    _, token = signup()
    body = refusal(reserve(token, reservation_body(untouched_slot()["id"], name="")))
    assert body.get("field") == "name", f"a missing name refusal names {body.get('field')!r}"


def test_reservation_name_longer_than_eighty_characters_is_rejected(db):
    email = unique_email()
    _, token = signup()
    body = refusal(reserve(token, reservation_body(untouched_slot()["id"], name="N" * 81, email=email)))
    assert body.get("field") == "name", f"an 81-character name refusal names {body.get('field')!r}"
    assert db.count("reservations", guest_email=email) == 0, "a refused reservation still wrote a row"


def test_request_breaking_several_rules_names_the_first_failing_field(db):
    full_id = slot_on(tomorrow(), "16:00")["id"]
    _, token = signup()
    cases = (
        ({"name": "", "email": "not-an-email", "partySize": 9}, "name"),
        ({"name": "Probe Guest", "email": "not-an-email", "partySize": 9}, "email"),
        ({"name": "Probe Guest", "partySize": 9}, "partySize"),
    )
    for overrides, expected in cases:
        email = unique_email()
        body = {"name": "Probe Guest", "email": email, "partySize": 1, "slotId": full_id, **overrides}
        refused = refusal(reserve(token, body))
        assert refused.get("field") == expected, (
            f"a request breaking several rules ({overrides}) names {refused.get('field')!r}, expected {expected!r}")
        assert db.count("reservations", guest_email=email) == 0, "a refused reservation still wrote a row"


def test_reservation_with_a_malformed_email_is_rejected(db):
    _, token = signup()
    visitor_id = me(token)["id"]
    body = refusal(reserve(token, reservation_body(untouched_slot()["id"], email="not-an-email")))
    assert body.get("field") == "email", f"a malformed email refusal names {body.get('field')!r}"
    assert db.count("reservations", visitor_id=visitor_id) == 0, "a refused reservation still wrote a row"


def test_rejected_reservation_sends_no_email(inbox):
    email = unique_email()
    _, token = signup()
    refusal(reserve(token, reservation_body(slot_on(tomorrow(), "16:00")["id"], email=email)))
    settle()
    assert inbox.count(to=email) == 0, f"a rejected reservation sent mail to {email}"


def test_cancelling_a_reservation_returns_cancelled_status(db):
    token, reservation = reserve_fresh(untouched_slot()["id"])
    with client(token) as visitor:
        response = visitor.post(f"/reservations/{reservation['id']}/cancel")
        listed = visitor.get("/reservations").json()
    assert response.status_code == 200, f"cancel returned {response.status_code}: {response.text[:300]}"
    body = response.json()
    cancelled = body.get("reservation") or {}
    assert body.get("ok") is True and {"id", "slotId", "code", "status"} <= set(cancelled), (
        f"cancel returned {response.text[:300]}")
    assert cancelled.get("status") == CANCELLED, f"cancel returned {response.text[:300]}"
    assert db.reservation(reservation["code"]).get("status") == CANCELLED, "the row is not cancelled"
    statuses = {r.get("code"): r.get("status") for r in listed}
    assert statuses.get(reservation["code"]) == CANCELLED, (
        f"GET /api/reservations does not list the cancelled reservation: {statuses}")


def test_cancelling_a_reservation_returns_its_places():
    slot_id = untouched_slot()["id"]
    token, reservation = reserve_fresh(slot_id, party=2)
    assert int(slot_by_id(slot_id)["placesLeft"]) == CAPACITY - 2, "the reservation did not take two places"
    with client(token) as visitor:
        visitor.post(f"/reservations/{reservation['id']}/cancel")
    assert int(slot_by_id(slot_id)["placesLeft"]) == CAPACITY, "cancelling did not return the places"


def test_cancelling_an_already_cancelled_reservation_is_rejected(db):
    token, reservation = reserve_fresh(untouched_slot()["id"])
    with client(token) as visitor:
        visitor.post(f"/reservations/{reservation['id']}/cancel")
        again = visitor.post(f"/reservations/{reservation['id']}/cancel")
    assert 400 <= again.status_code < 500, f"a second cancel returned {again.status_code}: {again.text[:300]}"
    assert db.reservation(reservation["code"]).get("status") == CANCELLED, "a second cancel changed the row"


def test_cancelling_a_started_reservation_is_rejected(db):
    code, email, hhmm, party, name = SEED_STARTED
    row = db.reservation(code)
    assert row is not None, f"seeded reservation {code} is missing"
    slot = slot_by_id(row["slot_id"])
    observed = (row.get("party_size"), row.get("guest_name"), row.get("guest_email"),
                slot_date(slot), slot_time(slot), row.get("status"), slot.get("status"))
    assert observed == (party, name, email, run_start().isoformat(), hhmm, CONFIRMED, "past"), (
        f"seeded reservation {code} reads {observed}")
    with client(login(VISITOR3_EMAIL, SEEDED_PASSWORD)) as visitor:
        response = visitor.post(f"/reservations/{row['id']}/cancel")
    assert 400 <= response.status_code < 500, (
        f"cancelling {code}, whose entry time has started, returned {response.status_code}: {response.text[:300]}")
    assert db.reservation(code).get("status") == CONFIRMED, f"a refused cancel changed {code}"


def test_cancelling_an_unknown_reservation_answers_not_found(visitor_token):
    with client(visitor_token) as visitor:
        response = visitor.post("/reservations/987654321/cancel")
    assert response.status_code == 404, (
        f"cancelling reservation id 987654321 returned {response.status_code}, expected not-found")


def test_started_visit_shows_no_cancel_control(page):
    sign_in_page(page, VISITOR3_EMAIL, SEEDED_PASSWORD)
    page.goto(page_url("/visit"))
    expect(page.get_by_text(SEED_STARTED[0]).first).to_be_visible(timeout=15000)
    controls = labelled_control(page, "Cancel visit").count()
    assert controls == 2, (
        f"{VISITOR3_EMAIL} sees {controls} Cancel visit controls; SEEDC14D and SEEDG16H can be cancelled "
        f"but SEEDP10Q has started")


def test_cancelling_a_reservation_sends_no_email(inbox):
    email = unique_email()
    token, reservation = reserve_fresh(untouched_slot()["id"], email=email)
    assert poll_until(lambda: inbox.count(to=email) == 1), f"no confirmation reached {email}"
    with client(token) as visitor:
        visitor.post(f"/reservations/{reservation['id']}/cancel")
    settle()
    assert inbox.count(to=email) == 1, f"cancelling sent further mail to {email}"


def test_reservation_list_returns_earliest_entry_first():
    later = untouched_slot(skip=6)
    earlier = untouched_slot(skip=1)
    _, token = signup()
    confirmed_code(reserve(token, reservation_body(later["id"])))
    confirmed_code(reserve(token, reservation_body(earlier["id"])))
    with client(token) as visitor:
        rows = visitor.get("/reservations").json()
    starts = [r.get("startsAt") for r in rows]
    assert starts == sorted(starts), f"GET /api/reservations lists {starts}, not earliest first"
    for row in rows:
        assert RESERVATION_FIELDS <= set(row), f"a reservation row carries {sorted(row)}"


def test_slots_api_lists_every_run_day_at_five_entry_times():
    slots = all_slots()
    assert len(slots) == SLOT_COUNT, f"GET /api/slots lists {len(slots)} entry times, expected {SLOT_COUNT}"
    starts = [str(s["startsAt"]) for s in slots]
    assert starts == sorted(starts), "GET /api/slots is not earliest first"
    by_day = {}
    for slot in slots:
        assert SLOT_FIELDS <= set(slot), f"an entry time carries {sorted(slot)}"
        by_day.setdefault(slot_date(slot), []).append(slot_time(slot))
        assert int(slot.get("capacity")) == CAPACITY, f"entry time {slot['id']} holds {slot.get('capacity')}"
    for day, times in by_day.items():
        assert tuple(times) == ENTRY_TIMES, f"{day} carries entry times {times}"
    later = (run_start() + datetime.timedelta(days=5)).isoformat()
    for slot in slots:
        if slot_date(slot) >= later and int(slot["placesLeft"]) > 0:
            assert slot.get("status") == "open", f"entry time {slot['id']} with places left reads {slot.get('status')!r}"


def test_first_run_day_entry_times_read_past():
    start = run_start()
    first_day = [s for s in all_slots() if slot_date(s) == start.isoformat()]
    assert len(first_day) == len(ENTRY_TIMES), f"the run's first day {start} has {len(first_day)} entry times"
    assert all(s.get("status") == "past" for s in first_day), (
        f"entry times on the run's first day read {[s.get('status') for s in first_day]}")


def test_seeded_full_entry_time_reads_full(db):
    full = slot_on(tomorrow(), "16:00")
    assert full.get("status") == "full" and int(full.get("placesLeft")) == 0, f"tomorrow 16:00 reads {full}"
    for code, email, hhmm, party, name in SEED_RESERVATIONS:
        if hhmm != "16:00":
            continue
        row = db.reservation(code)
        assert row is not None, f"seeded reservation {code} is missing"
        observed = (row.get("party_size"), row.get("guest_name"), row.get("guest_email"),
                    str(row.get("slot_id")), row.get("status"))
        assert observed == (party, name, email, str(full["id"]), CONFIRMED), (
            f"seeded reservation {code} reads {observed}")


def test_seeded_reservations_match_the_seed(db):
    for code, email, hhmm, party, name in SEED_RESERVATIONS:
        row = db.reservation(code)
        assert row is not None, f"seeded reservation {code} is missing"
        slot = slot_by_id(row["slot_id"])
        observed = (row.get("party_size"), row.get("guest_name"), row.get("guest_email"),
                    slot_date(slot), slot_time(slot), row.get("status"))
        assert observed == (party, name, email, tomorrow().isoformat(), hhmm, CONFIRMED), (
            f"seeded reservation {code} reads {observed}")
        owner = db.visitor(email)
        assert owner is not None and row.get("visitor_id") == owner.get("id"), (
            f"seeded reservation {code} does not belong to {email}")


def test_visit_figures_use_tabular_numerals(page):
    sign_in_page(page, VISITOR3_EMAIL, SEEDED_PASSWORD)
    page.goto(page_url("/visit"))
    cell = page.locator('[data-slot-state="open"]').first
    expect(cell).to_be_attached(timeout=15000)
    assert cell.evaluate(TABULAR_JS), "the open grid cells do not set their places left in tabular numerals"
    expect(page.get_by_text("SEEDC14D").first).to_be_visible(timeout=15000)
    assert page.evaluate(ROW_TABULAR_JS, ["SEEDC14D", "14:00"]), (
        "the date, time and code of SEEDC14D under Your visits are not set in tabular numerals")

def test_visit_grid_cells_carry_slot_id_and_slot_state(page):
    one_left = untouched_slot()["id"]
    fill_slot(one_left, leave=1)
    two_left = untouched_slot()["id"]
    fill_slot(two_left, leave=2)
    eight_left = untouched_slot()["id"]
    slots = all_slots()
    page.goto(page_url("/visit"))
    expect(page.locator("[data-slot-id]").first).to_be_attached(timeout=15000)
    assert page.locator("[data-slot-id]").count() == len(slots), (
        f"/visit carries {page.locator('[data-slot-id]').count()} cells, expected {len(slots)}")
    for slot in (slots[0], slot_on(tomorrow(), "16:00"), slot_by_id(eight_left)):
        state = page.locator(f'[data-slot-id="{slot["id"]}"]').first.get_attribute("data-slot-state")
        assert state == slot["status"], f"cell {slot['id']} carries data-slot-state {state!r}"
    for slot_id, copy in ((one_left, "1 place left"), (two_left, "2 places left"), (eight_left, "8 places left")):
        text = page.locator(f'[data-slot-id="{slot_id}"]').first.inner_text()
        assert copy in text, f"cell {slot_id} reads {text!r}, expected {copy!r}"


def test_every_entry_time_is_stored_in_utc(visitor_token):
    for slot in all_slots():
        moment = utc_moment(slot["startsAt"])
        assert moment.strftime("%H:%M") in ENTRY_TIMES, f"startsAt {slot['startsAt']} is off the hours"
    for row in selection(visitor_token):
        utc_moment(row["savedAt"])
    facts = exhibition()
    for key in ("runStart", "runEnd"):
        assert DATE_PATTERN.match(str(facts.get(key))), f"GET /api/exhibition writes {key} as {facts.get(key)!r}"


def test_slot_rows_store_no_places_left_or_status(db):
    rows = db.rows("slots", limit=1)
    assert rows, "the slots table is empty"
    stored = {key.lower() for key in rows[0]}
    assert not stored & {"places_left", "placesleft", "status", "available"}, (
        f"slots stores a derived column: {sorted(stored)}")


def test_seeded_rows_appear_exactly_once(db):
    for email, _ in SEEDED_NAMES:
        assert db.count_visitors(email=email) == 1, f"{email} appears {db.count_visitors(email=email)} times"
    assert db.count("galleries") == 2, f"galleries holds {db.count('galleries')} rows"
    assert db.count("introductions") == 2, f"introductions holds {db.count('introductions')} rows"
    assert db.count("slots") == SLOT_COUNT, f"slots holds {db.count('slots')} rows"
    for code, *_ in SEED_RESERVATIONS + (SEED_STARTED,):
        assert db.count("reservations", code=code) == 1, f"{code} appears more than once"


def test_unknown_address_renders_the_not_found_document(page):
    response = page.goto(page_url(f"/{unique_local()}"))
    assert response is not None and response.status == 404, (
        f"an unknown address answered {response.status if response else None}, expected not-found")
    markup = page.content()
    for copy in NOT_FOUND_COPY:
        assert copy in markup, f"the not-found document is missing {copy!r}"
    link = page.get_by_role("link", name="Back to Homepage").first
    assert (link.get_attribute("href") or "") in ("/", page_url("/"), page_url("")), (
        "Back to Homepage does not link to /")
    assert menu_control(page).count() == 0, "the not-found document has a menu"
    assert page.get_by_role("banner").count() == 0, "the not-found document carries a header"
    assert page.get_by_role("img", name=re.compile(r"photographed by")).count() == 0, (
        "the not-found document carries a gallery body")


def test_privacy_page_names_what_is_kept(page):
    response = page.goto(page_url("/privacy"))
    assert response is not None and response.status == 200, "/privacy did not answer"
    text = page.locator("body").inner_text().lower()
    for noun in PRIVACY_NOUNS:
        assert noun in text, f"the privacy page does not name {noun!r}"


def test_administrator_address_answers_not_found():
    response = fetch_page("/admin/")
    assert response.status_code == 404, (
        f"/admin/ answered {response.status_code}; the product has no administrator address")


def test_tab_icon_is_an_inline_vector_data_address(page):
    page.goto(page_url("/"))
    href = page.evaluate("() => { const l = document.querySelector('link[rel~=\"icon\"]'); "
                         "return l ? l.getAttribute('href') : ''; }")
    assert str(href).startswith("data:image/svg+xml"), f"the tab icon is declared as {str(href)[:60]!r}"


def test_no_image_font_audio_or_video_file_loads(page):
    seen = []
    page.on("request", lambda request: seen.append((request.url, "")))
    page.on("response", lambda response: seen.append(
        (response.url, response.headers.get("content-type", ""))))
    origin = httpx.URL(page_url("/")).host
    for route in ("/", "/aura", "/gazette-intro", "/visit"):
        page.goto(page_url(route))
        settle()
    for url, kind in seen:
        if url.startswith("data:") or url.startswith("blob:"):
            continue
        assert httpx.URL(url).host == origin, f"{url} left the app origin at run time"
        assert not kind.lower().startswith(ASSET_TYPES), f"{url} loaded an asset file of type {kind}"


def test_nothing_the_browser_downloads_carries_a_credential(page):
    bodies = []

    def collect(response):
        if response.request.resource_type in ("document", "script", "stylesheet"):
            bodies.append((response.url, response.text()))

    page.on("response", collect)
    for route in ("/", "/aura", "/visit", "/login"):
        page.goto(page_url(route))
    settle()
    for url, body in bodies:
        for marker in SECRET_MARKERS:
            assert marker not in body, f"{url} carries the credential marker {marker!r}"


def test_health_route_answers_ok_without_a_token(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, f"GET /api/health returned {response.status_code}"
    assert response.json().get("status") == "ok", f"GET /api/health returned {response.text[:200]}"


def test_backend_serves_json_under_the_api_prefix(anon_client):
    response = anon_client.get("/galleries")
    assert "application/json" in response.headers.get("content-type", ""), (
        f"GET /api/galleries answered {response.headers.get('content-type')}, not JSON")


def test_unknown_address_serves_no_development_debug_page():
    response = fetch_page(f"/{unique_local()}")
    for marker in DEBUG_MARKERS:
        assert marker not in response.text, f"an unknown address shows a development debug page ({marker!r})"


def test_seeded_rows_live_in_the_postgres_database(db):
    assert db.visitor(VISITOR_EMAIL) is not None, "visitor@example.com is not stored in visitors"
    assert db.reservation("SEEDA14B") is not None, "SEEDA14B is not stored in reservations"
    assert db.count("frames") == len(FRAMES), "the frames are not stored in frames"
    for table in TABLES:
        assert db.count(table) >= 0, f"the {table} table is missing"


def test_every_list_endpoint_returns_a_top_level_json_array(anon_client, visitor_token):
    for path in ("/galleries", "/slots"):
        assert isinstance(anon_client.get(path).json(), list), f"GET /api{path} is not a top-level array"
    with client(visitor_token) as visitor:
        for path in ("/selection", "/reservations"):
            assert isinstance(visitor.get(path).json(), list), f"GET /api{path} is not a top-level array"


def test_public_endpoints_answer_without_a_token(anon_client):
    identifier, _ = frame_id("Odessa Vane")
    for path in ("/health", "/exhibition", "/galleries", "/galleries/aura", f"/frames/{identifier}", "/slots"):
        response = anon_client.get(path)
        assert response.status_code == 200, f"GET /api{path} without a token returned {response.status_code}"
    address = unique_email()
    created = anon_client.post("/auth/signup", json={
        "email": address, "password": PROBE_PASSWORD, "displayName": "Public Probe"})
    assert created.status_code in (200, 201), f"signup without a token returned {created.status_code}"
    signed_in = anon_client.post("/auth/login", json={"email": address, "password": PROBE_PASSWORD})
    assert signed_in.status_code == 200, f"login without a token returned {signed_in.status_code}"


def test_root_element_carries_fonts_ready_and_scrolled_classes(page):
    page.goto(page_url("/aura"))
    page.wait_for_function("() => document.documentElement.classList.contains('is-fonts-ready')",
                           timeout=20000)
    page.mouse.move(640, 450)
    page.mouse.wheel(0, 800)
    page.wait_for_function("() => document.documentElement.classList.contains('has-scrolled')",
                           timeout=20000)


def test_reduced_motion_landing_presents_the_settled_chooser(page):
    page.emulate_media(reduced_motion="reduce")
    page.goto(page_url("/"))
    boxes = {}
    for route in ("/aura-intro", "/gazette-intro"):
        cover = page.locator(f'a[href$="{route}"]').first
        expect(cover).to_be_visible(timeout=15000)
        box = cover.bounding_box()
        assert box is not None and box["y"] < 900, f"the {route} cover is not settled in view under reduced motion"
        boxes[route] = box
    assert boxes["/aura-intro"]["x"] < boxes["/gazette-intro"]["x"], (
        "the AURA cover does not sit left of the Gazette cover in the settled chooser")


def test_touch_landing_presents_the_settled_chooser(chromium):
    context = chromium.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    try:
        surface = context.new_page()
        surface.goto(page_url("/"))
        for route in ("/aura-intro", "/gazette-intro"):
            cover = surface.locator(f'a[href$="{route}"]').first
            expect(cover).to_be_visible(timeout=15000)
            box = cover.bounding_box()
            assert box is not None and box["y"] < 844, (
                f"the {route} cover is not settled in view on a device without hover")
    finally:
        context.close()


def test_reduced_motion_page_scrolls_natively(page):
    page.emulate_media(reduced_motion="reduce")
    page.goto(page_url("/aura"))
    page.mouse.move(640, 450)
    page.mouse.wheel(0, 900)
    page.wait_for_function("() => window.scrollY > 0", timeout=15000)


def test_reduced_motion_keeps_the_page_text_and_its_order(page):
    for route in ("/aura-intro", "/aura"):
        page.goto(page_url(route))
        settle()
        full = compact(page.evaluate("() => document.body.textContent"))
        page.emulate_media(reduced_motion="reduce")
        page.goto(page_url(route))
        settle()
        reduced = compact(page.evaluate("() => document.body.textContent"))
        page.emulate_media(reduced_motion="no-preference")
        assert reduced == full, f"{route} changes its text or its order under a reduced-motion preference"


def test_reduced_motion_runs_no_looping_animation(page):
    page.emulate_media(reduced_motion="reduce")
    page.goto(page_url("/"))
    settle()
    looping = page.evaluate(LOOPING_ANIMATIONS_JS)
    assert looping == 0, f"{looping} looping animation(s) keep running under reduced motion"


def test_narrow_viewport_scrolls_nothing_sideways(page):
    page.set_viewport_size({"width": 375, "height": 812})
    for route in ("/", "/aura", "/visit"):
        page.goto(page_url(route))
        settle(1.0)
        overflow = page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        assert overflow <= 1, f"{route} scrolls {overflow} sideways at a narrow viewport"


def test_colour_scheme_preference_changes_nothing(page):
    grounds = {}
    for scheme in ("light", "dark"):
        page.emulate_media(color_scheme=scheme)
        for route in ("/", "/aura-intro", "/gazette"):
            page.goto(page_url(route))
            settle(1.0)
            grounds[(scheme, route)] = page.evaluate(
                "() => [getComputedStyle(document.documentElement).backgroundColor, "
                "getComputedStyle(document.body).backgroundColor, getComputedStyle(document.body).color]")
    for route in ("/", "/aura-intro", "/gazette"):
        assert grounds[("light", route)] == grounds[("dark", route)], (
            f"{route} changes its colours with the colour scheme preference: "
            f"{grounds[('light', route)]} vs {grounds[('dark', route)]}")
