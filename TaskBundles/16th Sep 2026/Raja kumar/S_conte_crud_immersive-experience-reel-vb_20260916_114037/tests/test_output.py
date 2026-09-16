from __future__ import annotations

import json
import re
import uuid
from html.parser import HTMLParser
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import httpx
from appclient import api_base, app_url
from conftest import (
    ADMIN_EMAIL, ALREADY_ON_REEL, CHOOSE_BUDGET, CHOOSE_REPLY, CHOOSE_TIMEFRAME, CONFIRM_SUBJECT,
    CONFIRM_TITLE, DRAFT_SLUG, DRAFT_TITLE, EDITOR_EMAIL, EMAIL_TAKEN, ENQUIRY_LIMIT, ENQUIRY_RECEIPT,
    ENQUIRY_STUDIO, EVENT_PROPERTY, EXPIRED_LINK, INTENT_LINKS, LAST_OWNER, LINK_INVALID, LINK_RE,
    MESSAGE_LIMIT, NO_ITEMS, NO_SCENE_BANNER, NOT_FOUND_COPY, NOT_VERIFIED, NOTE_TOO_LONG,
    OPEN_PITCH_DELETE, OPEN_PITCH_LIMIT, ORDER_INVALID, OWN_ROLE, PASSWORD, PITCH_CHANGE, PITCH_CLOSED,
    PITCH_RECEIPT, PITCH_STUDIO, PITCH_WITHDRAWN, PRODUCER2_EMAIL, PRODUCER_EMAIL, QUESTION,
    QUESTION_LIMIT, QUESTION_TOO_LONG, RECENT_ORDER, REEL_ITEM_LIMIT, REEL_LIMIT, REEL_SENT,
    RESET_MESSAGE, RESET_SUBJECT, SEEDED_PITCH_REFERENCE, SEEDED_REEL_TITLE, SIGNIN_FAILURE,
    STUDIO_QUEUE, STUDIO_REPLIED, SUMMARY_LONG, SUMMARY_SHORT, TIMEOUT, TITLE_ORDER, TRACK_TITLES,
    add_item, at_once, client, document, error_of, mails_to, new_reel, pitch_body, project_id,
    projects, read_reel, reel_with, rows_of, set_project_state, settle, signin, titles, token_from,
    unique, unique_email, wait_for_mails, warm,
)

PUBLIC_TITLES = {
    "/": "Halcyon Works",
    "/work": "Work | Halcyon Works",
    "/work/rally": "Rally | Halcyon Works",
    "/work/eden": "E.D.E.N. | Halcyon Works",
    "/contact": "Contact | Halcyon Works",
    "/legal/privacy": "Privacy Notice | Halcyon Works",
    "/signin": "Sign in | Halcyon Works",
    "/signup": "Sign up | Halcyon Works",
    "/reset": "Reset password | Halcyon Works",
}
SCENE_ROUTES = ("/", "/work", "/work/rally")
REFUSED = (400, 409, 422)
LINK_REFUSED = (400, 404, 409, 410, 422)


class _Head(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = None
        self.meta = {}
        self._parts = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title" and self.title is None:
            self._parts = []
        if tag == "meta":
            key = (attrs.get("name") or attrs.get("property") or "").lower()
            if key and key not in self.meta:
                self.meta[key] = attrs.get("content") or ""

    def handle_endtag(self, tag):
        if tag == "title" and self._parts is not None:
            self.title = "".join(self._parts).strip()
            self._parts = None

    def handle_data(self, data):
        if self._parts is not None:
            self._parts.append(data)


def _head(html: str) -> _Head:
    parser = _Head()
    parser.feed(html)
    return parser


def _exact(text: str):
    return re.compile(rf"^\s*{re.escape(text).replace('/', chr(92) + '/')}\s*$", re.I)


def _path(url: str) -> str:
    return urlparse(url).path


def _press(page, locator, key="Enter"):
    locator.focus()
    page.keyboard.press(key)


def _leave_entry(page, press):
    """Loading holds the address, so an early press may be ignored; press again only while still on /."""
    for _ in range(6):
        press()
        for _ in range(12):
            if _path(page.url) != "/":
                break
            page.wait_for_timeout(250)
        if _path(page.url) != "/":
            break
    assert _path(page.url) == "/work", f"leaving the entry state landed on {page.url}, expected /work"


def _open_entry(page):
    page.goto(f"{app_url()}/")
    page.get_by_role("link", name=_exact(INTENT_LINKS[0][0])).first.wait_for(state="attached")


def _sign_in_through_the_form(page, email, password, next_path=None):
    page.goto(f"{app_url()}/signin" + (f"?next={next_path}" if next_path else ""))
    page.get_by_label(_exact("Email")).first.fill(email)
    page.get_by_label(_exact("Password")).first.fill(password)
    _press(page, page.get_by_role("button", name=_exact("Sign in")).first)


def _missing_id_like(known) -> object:
    if isinstance(known, int) or str(known).isdigit():
        return int(known) + 9_000_000
    if re.fullmatch(r"[0-9a-fA-F-]{32,36}", str(known)):
        return str(uuid.uuid4())
    return f"{known}zz"


def _seeded_reel_id(producer_token):
    with client(producer_token) as c:
        response = c.get("/reels")
    assert response.status_code == 200, response.text[:300]
    found = [r for r in rows_of(response.json()) if r["title"] == SEEDED_REEL_TITLE]
    assert found, f"the seeded producer's reels do not include {SEEDED_REEL_TITLE!r}"
    return found[0]["id"]


def _seeded_pitch(producer_token):
    with client(producer_token) as c:
        response = c.get("/pitches")
    assert response.status_code == 200, response.text[:300]
    found = [p for p in rows_of(response.json()) if p["reference"] == SEEDED_PITCH_REFERENCE]
    assert found, f"the seeded producer's pitches do not include {SEEDED_PITCH_REFERENCE}"
    return found[0]


def _submitted_pitch(token, slugs):
    with client(token) as c:
        reel = reel_with(c, slugs)
        response = c.post("/pitches", json=pitch_body(reel))
    assert response.status_code == 201, f"submitting a pitch returned {response.status_code}: {response.text[:300]}"
    return reel, response.json()


def _open_pitch_without_messages(token, state=None):
    with client(token) as c:
        listed = rows_of(c.get("/pitches").json())
        for summary in listed:
            if summary["state"] not in ("submitted", "acknowledged", "in_conversation"):
                continue
            if state and summary["state"] != state:
                continue
            pitch = c.get(f"/pitches/{summary['id']}").json()
            if not pitch["messages"]:
                return pitch
    raise AssertionError(f"no open pitch without messages among {[(p['reference'], p['state']) for p in listed]}")


def _assistant_cookie(response: httpx.Response):
    for header in response.headers.get_list("set-cookie"):
        name, _, rest = header.partition("=")
        if name.strip() == "assistant_session":
            return rest.split(";", 1)[0]
    return None


def _ask(question, project_slug=None, headers=None):
    return httpx.post(f"{api_base()}/assistant", json={"question": question, "project_slug": project_slug},
                      headers=headers or {}, timeout=TIMEOUT)


def _enquiry(sender, **overrides):
    body = {"name": "Ada Lin", "email": sender, "timing": "this-year",
            "summary": "We would like a pavilion that people remember", "contact_preference": "email",
            "company_website": ""}
    body.update(overrides)
    with client() as c:
        return c.post("/enquiries", json=body)


def test_health_route_answers_ready():
    with client() as c:
        response = c.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, so the app never reported ready: {response.text[:300]}"
    )


def test_entry_state_offers_five_intent_links_as_text(page):
    _open_entry(page)
    assert page.get_by_text(_exact(QUESTION)).count() >= 1, f"{QUESTION!r} is not present as text on /"
    for label, target in INTENT_LINKS:
        link = page.get_by_role("link", name=_exact(label))
        assert link.count() >= 1, f"the intent link {label!r} is not a link in the document on /"
        resolved = urljoin(f"{app_url()}/", link.first.get_attribute("href") or "")
        assert resolved.endswith(target), f"{label!r} resolves to {resolved!r}, expected {target!r}"
    for text in ("WORK", "CONTACT"):
        assert page.get_by_text(_exact(text)).count() >= 1, f"the chrome capsule does not carry {text!r}"
    names = [n.strip().lower() for n in page.get_by_role("link").evaluate_all("els => els.map(e => e.textContent)")]
    positions = [names.index(label.lower()) for label, _ in INTENT_LINKS]
    assert positions == sorted(positions), f"the five intent links are not in the stated order: {names}"


def test_scroll_down_button_and_arrow_key_enter_the_reel(page):
    _open_entry(page)
    page.evaluate("() => { window.__sameDocument = true; }")
    button = page.get_by_role("button", name=_exact("SCROLL DOWN")).first
    _leave_entry(page, lambda: _press(page, button))
    assert page.evaluate("() => window.__sameDocument === true"), "entering the reel loaded a new document"
    page.wait_for_function(
        "() => Array.from(document.querySelectorAll('[aria-live=assertive], [role=alert]')).some(e => /reel/i.test(e.textContent))")
    for title in RECENT_ORDER:
        page.get_by_text(_exact(title)).first.wait_for(state="attached")
    _open_entry(page)
    _leave_entry(page, lambda: page.keyboard.press("ArrowDown"))


def test_tab_never_advances_the_scene(page):
    _open_entry(page)
    page.wait_for_load_state("networkidle")
    focused = []
    for _ in range(6):
        page.keyboard.press("Tab")
        focused.append(page.evaluate("() => document.activeElement ? document.activeElement.tagName : null"))
    page.wait_for_timeout(1500)
    assert _path(page.url) == "/", f"pressing Tab six times moved the address to {page.url}"
    assert all(tag and tag != "BODY" for tag in focused), f"Tab did not move focus through controls: {focused}"


def _visible_style(page, text):
    return page.evaluate(
        """text => {
            const wanted = text.toLowerCase();
            for (const el of document.querySelectorAll('body *')) {
                if (el.children.length || el.textContent.trim().toLowerCase() !== wanted) continue;
                const box = el.getBoundingClientRect();
                const style = getComputedStyle(el);
                if (box.width > 0 && box.height > 0 && style.visibility !== 'hidden' && parseFloat(style.fontSize) > 1) {
                    return {size: style.fontSize, line: style.lineHeight, weight: style.fontWeight};
                }
            }
            return null;
        }""", text)


def test_interface_text_follows_the_exact_type_scale(page):
    _open_entry(page)
    page.wait_for_function("() => Array.from(document.querySelectorAll('a')).some(a => a.textContent.trim().toLowerCase() === '-> games' && a.getBoundingClientRect().height > 0)")
    intent = _visible_style(page, INTENT_LINKS[0][0])
    assert intent and intent["size"] == "16px" and intent["line"] == "30px", f"the intent list renders at {intent}"
    page.goto(f"{app_url()}/work/rally")
    page.get_by_text(_exact("2014 / Nimbus / installation")).first.wait_for(state="attached")
    page.wait_for_function("() => Array.from(document.querySelectorAll('body *')).some(e => !e.children.length && e.textContent.trim() === '2014 / Nimbus / installation' && e.getBoundingClientRect().height > 0)")
    meta = _visible_style(page, "2014 / Nimbus / installation")
    assert meta and meta["size"] == "13px" and meta["line"] in ("19.5px", "normal"), f"the metadata line renders at {meta}"
    title = _visible_style(page, "Rally")
    assert title and title["size"] == "14px" and title["weight"] in ("700", "bold"), f"the project title renders at {title}"


def test_document_never_scrolls_on_public_routes(page):
    for route in SCENE_ROUTES:
        page.goto(f"{app_url()}{route}")
        page.wait_for_load_state("networkidle")
        height = page.evaluate("() => [document.documentElement.scrollHeight, window.innerHeight]")
        assert height[0] <= height[1] + 1, f"{route} is {height[0]} tall in a {height[1]} viewport"
        page.keyboard.press("End")
        assert page.evaluate("() => window.scrollY") == 0, f"the document scrolled on {route}"


def test_project_address_opens_cold_and_escape_returns_to_the_reel(page):
    page.goto(f"{app_url()}/work/rally")
    page.get_by_text(_exact("2014 / Nimbus / installation")).first.wait_for(state="attached")
    for text in ("Rally", "A multi-device racing experience that syncs in real-time. Developed for the client's developer conference",
                 "Project Link", "<- Close", "SCROLL TO CLOSE"):
        assert page.get_by_text(_exact(text)).count() >= 1, f"/work/rally opened cold does not carry {text!r}"
    assert page.get_by_placeholder(_exact("ASK ME ANYTHING...")).count() >= 1, "the assistant input is missing"
    page.wait_for_load_state("networkidle")
    page.keyboard.press("Escape")
    page.wait_for_url(re.compile(r"/work(\?[^/]*)?$"))
    page.go_back()
    page.wait_for_url(re.compile(r"/work/rally$"))
    page.goto(f"{app_url()}/work/harmonic-drift")
    page.get_by_text(_exact("2023 / Añejo Records / xr")).first.wait_for(state="attached")


def test_public_pages_fetch_nothing_from_another_origin(page):
    origin = urlparse(app_url())
    seen = []
    page.on("request", lambda request: seen.append((request.url, request.resource_type)))
    for route in ("/", "/work/rally", "/contact"):
        page.goto(f"{app_url()}{route}")
        page.wait_for_load_state("networkidle")
    foreign = [u for u, _ in seen if u.startswith("http")
               and (urlparse(u).hostname, urlparse(u).port) != (origin.hostname, origin.port)]
    assert not foreign, f"public pages fetched from another origin: {foreign[:5]}"
    media = [u for u, kind in seen if kind in ("image", "media") and u.startswith("http") and "icon" not in u]
    assert not media, f"public pages fetched image, video or audio files: {media[:5]}"


def test_missing_render_context_keeps_every_word_usable(browser_page):
    page = browser_page
    page.goto(f"{app_url()}/")
    page.get_by_text(_exact(NO_SCENE_BANNER)).first.wait_for(state="visible")
    page.get_by_text(_exact(QUESTION)).first.wait_for(state="visible")
    for label, _ in INTENT_LINKS:
        page.get_by_role("link", name=_exact(label)).first.wait_for(state="visible")
    button = page.get_by_role("button", name=_exact("SCROLL DOWN")).first
    _leave_entry(page, lambda: _press(page, button))
    page.get_by_text(_exact("Rally")).first.wait_for(state="visible")


def test_audio_starts_off_and_the_setting_survives_a_reload(page):
    page.goto(f"{app_url()}/")
    toggle = page.get_by_role("button").filter(has_text=re.compile(r"toggle audio\s+(on|off)", re.I)).first
    toggle.wait_for(state="attached")
    first = page.locator("a[href], button, input, select, textarea").first
    assert re.search(r"toggle audio", first.text_content() or "", re.I), (
        f"the first control in the document reads {first.text_content()!r}, not Toggle Audio"
    )
    assert re.search(r"off\s*$", toggle.text_content() or "", re.I), (
        f"on first arrival the audio control reads {toggle.text_content()!r}, expected OFF"
    )
    _press(page, toggle)
    page.wait_for_function("() => /toggle audio\\s+on/i.test(document.body.textContent)")
    page.reload()
    toggle = page.get_by_role("button").filter(has_text=re.compile(r"toggle audio\s+(on|off)", re.I)).first
    toggle.wait_for(state="attached")
    assert re.search(r"on\s*$", toggle.text_content() or "", re.I), (
        f"after a reload the audio control reads {toggle.text_content()!r}, expected ON"
    )


def test_ticker_names_the_track_with_two_hyphens(page):
    page.goto(f"{app_url()}/")
    page.wait_for_function(
        "titles => titles.some(t => document.body.textContent.toLowerCase().includes((t + '--Halcyon Works').toLowerCase()))",
        arg=TRACK_TITLES)
    for name in ("Previous track", "Next track"):
        assert page.get_by_role("button", name=_exact(name), include_hidden=True).count() >= 1, f"no {name!r} control"


def test_phone_width_never_scrolls_sideways(page):
    page.set_viewport_size({"width": 375, "height": 812})
    for route in SCENE_ROUTES:
        page.goto(f"{app_url()}{route}")
        page.wait_for_load_state("networkidle")
        widths = page.evaluate("() => [document.documentElement.scrollWidth, window.innerWidth]")
        assert widths[0] <= widths[1], f"{route} at phone width is {widths[0]} wide in {widths[1]}"
    ticker = page.get_by_role("button", name=_exact("Next track"), include_hidden=True)
    assert ticker.count() == 0 or not ticker.first.is_visible(), "the ticker controls are still shown at phone width"


def test_unknown_addresses_answer_not_found_at_the_document_level():
    for path in ("/no-such-place", "/work/not-a-project", f"/work/{DRAFT_SLUG}", f"/shared/{unique('never-minted')}",
                 "/@vite/client"):
        response = document(path)
        assert response.status_code == 404, (
            f"GET {path} returned {response.status_code}; an address that is not served answers not-found"
        )
        assert "text/html" in response.headers.get("content-type", ""), (
            f"GET {path} did not return the application shell: {response.headers.get('content-type')}"
        )
    for path in ("/", "/work", "/work/rally", "/contact"):
        response = document(path)
        assert response.status_code == 200, f"GET {path} returned {response.status_code}"
    with client() as c:
        missing = c.get("/no-such-endpoint")
    assert missing.status_code == 404 and error_of(missing)["code"] == "not_found", (
        f"an unknown API path answered {missing.status_code}: {missing.text[:200]}"
    )


def test_not_found_page_renders_its_own_words(page):
    page.goto(f"{app_url()}/no-such-place")
    page.get_by_text(_exact(NOT_FOUND_COPY)).first.wait_for(state="attached")


def test_public_addresses_carry_distinct_titles_and_descriptions():
    seen = {}
    for path, expected in PUBLIC_TITLES.items():
        response = document(path)
        assert response.status_code == 200, f"GET {path} returned {response.status_code}"
        head = _head(response.text)
        assert head.title == expected, (
            f"the HTML the server returns for {path} carries title {head.title!r} before any script runs, "
            f"expected {expected!r}"
        )
        description = head.meta.get("description", "").strip()
        assert description, f"the HTML for {path} carries no description"
        assert head.meta.get("og:title") == expected, f"og:title for {path} is {head.meta.get('og:title')!r}"
        assert description not in seen, f"{path} shares its description with {seen.get(description)}"
        seen[description] = path
    assert _head(document("/work?category=games&sort=title").text).title == "Work | Halcyon Works"


def test_social_preview_image_is_generated_and_resolves():
    for path in ("/", "/work/rally", "/contact"):
        image = _head(document(path).text).meta.get("og:image", "")
        assert image.startswith(("http://", "https://")), f"og:image for {path} is not absolute: {image!r}"
        parsed = urlparse(image)
        fetched = httpx.get(f"{app_url()}{parsed.path}" + (f"?{parsed.query}" if parsed.query else ""), timeout=TIMEOUT)
        assert fetched.status_code == 200, f"the preview image for {path} returned {fetched.status_code}"
        kind = fetched.headers.get("content-type", "").split(";")[0].strip()
        assert kind in ("image/png", "image/svg+xml"), f"the preview image for {path} is served as {kind!r}"


def test_privacy_page_is_linked_from_consent_and_states_what_is_stored(page):
    page.goto(f"{app_url()}/")
    link = page.get_by_role("link", name=_exact("Privacy Notice."))
    link.first.wait_for(state="attached")
    assert _path(urljoin(f"{app_url()}/", link.first.get_attribute("href") or "")) == "/legal/privacy"
    page.goto(f"{app_url()}/legal/privacy")
    page.get_by_text(re.compile("cookie preferences", re.I)).first.wait_for(state="attached")
    body = (page.evaluate("() => document.body.textContent") or "").lower()
    for phrases in (("email",), ("display name",), ("organisation", "organization"), ("reel",), ("note",),
                    ("pitch",), ("message",), ("enquir", "inquir"), ("thirty days", "30 days"), ("consent",),
                    ("audio",)):
        assert any(p in body for p in phrases), f"the privacy page does not state that it stores {phrases[0]!r}"


def test_consent_is_asked_once_and_reopens_from_privacy(page):
    page.goto(f"{app_url()}/")
    accept = page.get_by_role("button", name=_exact("Accept Cookies")).first
    accept.wait_for(state="visible")
    assert page.get_by_role("button", name=_exact("Reject Cookies")).first.is_visible()
    assert page.get_by_text(re.compile("our site uses essential cookies and, with your consent, analytics cookies", re.I)).count() >= 1
    _press(page, accept)
    accept.wait_for(state="hidden")
    page.reload()
    page.get_by_role("link", name=_exact(INTENT_LINKS[0][0])).first.wait_for(state="attached")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)
    assert not page.get_by_role("button", name=_exact("Accept Cookies")).first.is_visible(), (
        "the consent question was asked again after a reload"
    )
    page.goto(f"{app_url()}/legal/privacy")
    _press(page, page.locator("button, a").filter(has_text=_exact("Cookie preferences")).first)
    page.get_by_role("button", name=_exact("Reject Cookies")).first.wait_for(state="visible")


def test_catalogue_lists_fifteen_published_projects_newest_first():
    with client() as c:
        payload = projects(c)
    assert titles(payload) == RECENT_ORDER, f"the default order is {titles(payload)}"
    assert payload["total"] == 15, f"total reads {payload['total']}"
    assert all("state" not in row for row in rows_of(payload)), "a visitor received project state"


def test_oldest_sort_is_the_exact_reverse_of_recent():
    with client() as c:
        oldest = titles(projects(c, sort="oldest"))
    assert oldest == list(reversed(RECENT_ORDER)), f"sort=oldest returned {oldest}"


def test_filters_widen_within_a_parameter_and_narrow_across():
    with client() as c:
        response = c.get("/projects", params=[("category", "games"), ("year", "2021"), ("year", "2022")])
        assert response.status_code == 200, response.text[:300]
        assert titles(response.json()) == ["Welcome to Stonehall", "20 Years of Nexus", "Discover your Familiar"], (
            f"category=games&year=2021&year=2022 returned {titles(response.json())}"
        )
        assert response.json()["total"] == 3
        both = titles(c.get("/projects", params=[("category", "xr"), ("category", "installation")]).json())
        assert both == ["Secret Tide", "Harmonic Drift", "Frontier Beyond", "E.D.E.N.", "Andes 20", "Glass Planes", "Rally"], (
            f"category=xr&category=installation returned {both}"
        )
        assert titles(projects(c, client="u-s-skyforce", sort="title")) == ["E.D.E.N.", "Frontier Beyond"]
        assert titles(projects(c, client="papier-mache-press")) == ["Glass Planes"]
        assert projects(c, client="no-such-client")["total"] == 0


def test_search_ignores_accents_and_case():
    with client() as c:
        for query, expected in (("societe", ["Archimedes"]), ("MACHE", ["Glass Planes"]),
                                ("cooperative", ["Renewable Frontiers"]), ("Añejo", ["Harmonic Drift"]),
                                ("anejo", ["Harmonic Drift"])):
            found = titles(projects(c, q=query))
            assert found == expected, f"q={query!r} returned {found}, expected {expected}"


def test_search_orders_title_matches_before_description_matches():
    with client() as c:
        found = titles(projects(c, q="frontier"))
    assert found == ["Frontier Beyond", "Renewable Frontiers", "Secret Tide"], (
        f"q=frontier returned {found}; title matches come before a description-only match"
    )


def test_title_sort_folds_case_and_accents():
    with client() as c:
        found = titles(projects(c, sort="title"))
    assert found == TITLE_ORDER, f"sort=title returned {found}"


def test_invalid_catalogue_parameters_are_refused_with_the_field():
    with client() as c:
        for params, field in (({"category": "comics"}, "category"), ({"year": "21"}, "year"),
                              ({"q": "x" * 81}, "q"), ({"sort": "popular"}, "sort")):
            response = c.get("/projects", params=params)
            assert response.status_code == 400, f"GET /api/projects {params} returned {response.status_code}"
            error = error_of(response)
            assert error["code"] == "validation" and error["field"] == field, error
        assert c.get("/projects", params={"q": "x" * 80}).status_code == 200


def test_measured_projects_carry_their_exact_copy():
    with client() as c:
        eden = c.get("/projects/eden").json()["project"]
        rally = c.get("/projects/rally").json()
    assert (eden["title"], eden["year"], eden["client_name"], eden["category_slugs"]) == (
        "E.D.E.N.", 2021, "U.S. Skyforce", ["xr"]), eden
    assert eden["description"] == "A cinematic real-time experience offering guided levels to test and enhance cognitive skills"
    project = rally["project"]
    assert (project["year"], project["client_name"], project["category_slugs"], project["tint"],
            project["key_light"], project["scene_seed"]) == (2014, "Nimbus", ["installation"], "warm-amber",
                                                             "upper-right", 4107), project
    assert project["project_link"] == "https://example.com/work/rally"
    assert [c["slug"] for c in rally["categories"]] == ["installation"], rally["categories"]


def test_empty_filter_offers_clear_filters_that_keeps_the_sort(page):
    page.goto(f"{app_url()}/work?category=games&year=1999&sort=title")
    page.get_by_text(_exact("Nothing matches that.")).first.wait_for(state="attached")
    _press(page, page.locator("button, a").filter(has_text=_exact("Clear filters")).first)
    page.wait_for_function("() => !/year=1999/.test(location.search)")
    query = parse_qs(urlparse(page.url).query)
    assert query.get("sort") == ["title"] and "category" not in query and "year" not in query, page.url


def test_tracks_are_four_generated_tracks():
    with client() as c:
        items = rows_of(c.get("/tracks").json())
    assert [t["title"] for t in items] == TRACK_TITLES, items
    assert all(t["artist"] == "Halcyon Works" for t in items)
    assert [t["source"] for t in items] == ["generated:slow-current", "generated:glass-harbour",
                                           "generated:night-relay", "generated:amber-field"], items


def test_draft_project_is_denied_to_visitors_and_producers(producer2_token):
    for token in (None, producer2_token):
        with client(token) as c:
            assert DRAFT_TITLE not in titles(projects(c)), f"a {'producer' if token else 'visitor'} sees the draft"
            assert c.get(f"/projects/{DRAFT_SLUG}").status_code == 404
            assert projects(c, q="lantern")["total"] == 0, "search reveals the draft project"
            assert projects(c, category="xr", year="2025")["total"] == 0, "a filter reveals the draft project"


def test_editor_sees_the_draft_with_its_state(editor_token):
    with client(editor_token) as c:
        payload = projects(c)
        detail = c.get(f"/projects/{DRAFT_SLUG}")
    assert titles(payload)[0] == DRAFT_TITLE and payload["total"] == 16, titles(payload)
    assert rows_of(payload)[0]["state"] == "draft"
    assert detail.status_code == 200 and detail.json()["project"]["state"] == "draft"


def test_editor_cannot_publish_a_project(editor_token):
    with client(editor_token) as c:
        response = c.patch(f"/projects/{DRAFT_SLUG}", json={"state": "published"})
        assert response.status_code == 403, f"an editor publishing returned {response.status_code}"
        assert error_of(response)["code"] == "forbidden"
        assert c.get(f"/projects/{DRAFT_SLUG}").json()["project"]["state"] == "draft"
    with client() as c:
        assert c.get(f"/projects/{DRAFT_SLUG}").status_code == 404


def test_draft_project_cannot_join_a_reel(editor_token, producer2_token):
    with client(editor_token) as c:
        draft_id = c.get(f"/projects/{DRAFT_SLUG}").json()["project"]["id"]
    with client(producer2_token) as c:
        reel = new_reel(c)
        response = c.post(f"/reels/{reel['id']}/items", json={"project_id": draft_id, "version": reel["version"]})
        assert response.status_code == 404, f"adding the draft project returned {response.status_code}"
        assert read_reel(c, reel["id"])["item_count"] == 0


def test_assistant_denies_a_draft_project_as_context():
    response = _ask("Tell me about this project", DRAFT_SLUG)
    assert response.status_code == 404, f"the assistant took the draft as context: {response.status_code}"
    assert DRAFT_TITLE.lower() not in response.text.lower()


def test_project_link_must_be_http_with_a_host(editor_token):
    with client(editor_token) as c:
        for bad in ("javascript:alert(1)", "ftp://example.com/work", "https://"):
            response = c.patch(f"/projects/{DRAFT_SLUG}", json={"project_link": bad})
            assert response.status_code == 400, f"project_link {bad!r} returned {response.status_code}"
            assert error_of(response)["message"] == LINK_INVALID, response.text[:300]
        good = c.patch(f"/projects/{DRAFT_SLUG}", json={"project_link": "https://example.com/work/lantern-protocol"})
        assert good.status_code == 200, good.text[:300]


def test_signup_email_is_unique_regardless_of_case(fresh_account, backend):
    account = fresh_account["account"]
    assert account["email"] == fresh_account["folded"], f"sign up stored {account['email']!r}"
    assert account["role"] == "producer" and account["verified"] is False, account
    with client() as c:
        again = c.post("/auth/signup", json={"email": fresh_account["folded"], "display_name": "Probe Person",
                                             "organisation": "Probe Studio", "password": "probe-password-2026"})
    assert again.status_code == 409, f"signing up the same email in lower case returned {again.status_code}"
    assert error_of(again)["message"] == EMAIL_TAKEN
    assert backend.count("accounts", email=fresh_account["folded"]) == 1


def test_confirmation_mail_link_verifies_once_and_resend_replaces_it(fresh_account):
    email = fresh_account["folded"]
    first = wait_for_mails(email, CONFIRM_SUBJECT)
    assert len(first) == 1 and first[0]["subject"] == CONFIRM_SUBJECT, first
    mail = first[0]
    assert mail["html"].strip() == "" and len(LINK_RE.findall(mail["text"])) == 1, mail["text"][:300]
    assert email in mail["text"].lower() and mail["cc"] == [] and mail["bcc"] == []
    with client(fresh_account["token"]) as c:
        assert c.post("/auth/verify/resend").status_code == 202
    both = wait_for_mails(email, CONFIRM_SUBJECT, at_least=2)
    assert len(both) == 2, f"resend produced {len(both)} confirmation mails in all"
    newest, older = token_from(both[0], "/verify"), token_from(both[1], "/verify")
    with client() as c:
        stale = c.post("/auth/verify", json={"token": older})
        assert stale.status_code in LINK_REFUSED and error_of(stale)["message"] == EXPIRED_LINK, stale.text[:300]
        fresh = c.post("/auth/verify", json={"token": newest})
        assert fresh.status_code == 200 and fresh.json()["account"]["verified"] is True, fresh.text[:300]
        reused = c.post("/auth/verify", json={"token": newest})
        assert reused.status_code in LINK_REFUSED, f"a confirmation link verified twice: {reused.status_code}"


def test_signup_refuses_invalid_fields_writing_nothing(backend):
    for override, field in (({"email": "not-an-address"}, "email"), ({"password": "short-pw9"}, "password"),
                            ({"display_name": ""}, "display_name"), ({"display_name": "D" * 61}, "display_name"),
                            ({"organisation": "O" * 121}, "organisation")):
        body = {"email": unique_email("invalid"), "display_name": "Probe Person", "organisation": "Probe Studio",
                "password": "probe-password-2026"}
        body.update(override)
        with client() as c:
            response = c.post("/auth/signup", json=body)
        assert response.status_code == 400, f"sign up with {override} returned {response.status_code}"
        assert error_of(response)["field"] == field, response.text[:300]
        assert backend.count("accounts", email=body["email"].lower()) == 0


def test_signin_matches_the_email_regardless_of_case():
    assert signin(PRODUCER2_EMAIL.upper())


def test_five_failures_in_any_casing_lock_the_email(unverified_account):
    email = unverified_account["folded"]
    with client() as c:
        for variant in (email.upper(), email, email.title(), email[:4].upper() + email[4:], email.capitalize()):
            response = c.post("/auth/signin", json={"email": variant, "password": "wrong-password-0"})
            assert response.status_code in (400, 401), f"a wrong password for {variant} returned {response.status_code}"
            assert error_of(response)["message"] == SIGNIN_FAILURE
        for variant in (email, email.upper()):
            locked = c.post("/auth/signin", json={"email": variant, "password": unverified_account["password"]})
            assert locked.status_code == 429, (
                f"the correct password after five failures across casings returned {locked.status_code}"
            )
            assert error_of(locked)["message"] == SIGNIN_FAILURE


def test_failed_signin_never_says_which_half_was_wrong():
    with client() as c:
        unknown = c.post("/auth/signin", json={"email": unique_email("nobody"), "password": "wrong-password-0"})
        wrong = c.post("/auth/signin", json={"email": PRODUCER2_EMAIL, "password": "wrong-password-0"})
    assert unknown.status_code == wrong.status_code and unknown.status_code in (400, 401)
    assert error_of(unknown)["message"] == error_of(wrong)["message"] == SIGNIN_FAILURE


def test_sign_out_ends_the_session_on_the_server():
    with client() as c:
        signed = c.post("/auth/signin", json={"email": PRODUCER2_EMAIL, "password": PASSWORD})
        assert signed.status_code == 200, signed.text[:300]
        forged = c.post("/reels", json={"title": unique("Cookie only")})
    assert forged.status_code in (401, 403), (
        f"a write carrying only the session cookies and no request token returned {forged.status_code}"
    )
    token = signin(PRODUCER2_EMAIL)
    with client(token) as c:
        assert c.get("/me").status_code == 200
        assert c.post("/auth/signout").status_code == 204
        after = c.get("/me")
    assert after.status_code == 401, f"the signed-out token still reads /api/me with {after.status_code}"


def test_visitor_is_denied_every_producer_endpoint():
    with client() as c:
        for method, path, body in (("GET", "/me", None), ("GET", "/reels", None), ("POST", "/reels", {"title": "x"}),
                                   ("GET", "/pitches", None), ("POST", "/pitches", {}), ("GET", "/accounts", None)):
            response = c.request(method, path, json=body)
            assert response.status_code == 401, f"a visitor {method} {path} returned {response.status_code}"
            assert error_of(response)["code"] == "unauthenticated"


def test_unsafe_next_falls_back_to_the_desk(page):
    issued = []

    def capture(response):
        if response.request.method == "POST" and urlparse(response.url).path == "/api/auth/signin" and response.status == 200:
            issued.append(response.json().get("access_token") or "")

    page.on("response", capture)
    _sign_in_through_the_form(page, PRODUCER2_EMAIL, PASSWORD, next_path="//example.org/steal")
    page.wait_for_url(re.compile(r"/desk$"))
    assert urlparse(page.url).hostname == urlparse(app_url()).hostname
    stored = page.evaluate("() => [localStorage, sessionStorage].map(s => Object.keys(s).map(k => s.getItem(k)).join(' ')).join(' ')")
    assert issued and issued[0], "signing in through the form returned no access_token"
    assert issued[0] not in stored, "the session token was kept in browser storage"


def test_desk_route_sends_a_visitor_to_sign_in(page):
    page.goto(f"{app_url()}/desk")
    page.wait_for_url(re.compile(r"/signin\?"))
    assert parse_qs(urlparse(page.url).query).get("next") == ["/desk"], page.url


def test_signed_out_star_routes_to_sign_in(page):
    page.goto(f"{app_url()}/work")
    star = page.get_by_role("button", name=_exact("Add Archimedes to your reel")).first
    star.wait_for(state="attached")
    _press(page, star)
    page.wait_for_url(re.compile(r"/signin\?"))
    assert unquote(parse_qs(urlparse(page.url).query).get("next", [""])[0]) == "/work", page.url


def test_reset_answers_identically_for_unknown_addresses(reel_producer):
    with client() as c:
        unknown = c.post("/auth/reset", json={"email": unique_email("nobody")})
        known = c.post("/auth/reset", json={"email": reel_producer["email"]})
    assert unknown.status_code == known.status_code == 202
    assert unknown.json() == known.json() == {"message": RESET_MESSAGE}, (unknown.text, known.text)


def test_three_resets_send_one_mail_with_a_single_use_link(fresh_account):
    email = fresh_account["folded"]
    with client() as c:
        for variant in (email, email.upper(), fresh_account["email"]):
            assert c.post("/auth/reset", json={"email": variant}).status_code == 202
    wait_for_mails(email, RESET_SUBJECT)
    settle(3.0)
    mails = mails_to(email, RESET_SUBJECT)
    assert len(mails) == 1, f"three reset requests sent {len(mails)} reset mails, expected exactly one"
    assert mails[0]["html"].strip() == "" and len(LINK_RE.findall(mails[0]["text"])) == 1
    token = token_from(mails[0], "/reset")
    with client() as c:
        done = c.post("/auth/reset/complete", json={"token": token, "password": "renewed-password-2026"})
        assert done.status_code == 200, done.text[:300]
        again = c.post("/auth/reset/complete", json={"token": token, "password": "another-password-2026"})
        assert again.status_code in LINK_REFUSED and error_of(again)["message"] == EXPIRED_LINK, again.text[:300]
        old = c.post("/auth/signin", json={"email": email, "password": fresh_account["password"]})
        assert old.status_code in (400, 401), f"the replaced password still signs in: {old.status_code}"
    assert signin(email, "renewed-password-2026")


def test_reset_link_dies_on_a_successful_signin():
    with client() as c:
        assert c.post("/auth/reset", json={"email": PRODUCER2_EMAIL}).status_code == 202
    mails = wait_for_mails(PRODUCER2_EMAIL, RESET_SUBJECT)
    assert mails, f"no {RESET_SUBJECT!r} mail reached {PRODUCER2_EMAIL}"
    token = token_from(mails[0], "/reset")
    assert signin(PRODUCER2_EMAIL)
    with client() as c:
        late = c.post("/auth/reset/complete", json={"token": token, "password": "should-not-apply-2026"})
    assert late.status_code in LINK_REFUSED and error_of(late)["message"] == EXPIRED_LINK, (
        f"a reset link used after a successful sign in returned {late.status_code}: {late.text[:300]}"
    )
    assert signin(PRODUCER2_EMAIL, PASSWORD)


def test_producer_is_denied_studio_endpoints(producer2_token):
    with client(producer2_token) as c:
        own_id = c.get("/me").json()["account"]["id"]
        for method, path, body in (("GET", "/accounts", None), ("PATCH", f"/accounts/{own_id}", {"role": "admin"}),
                                   ("PATCH", "/projects/rally", {"state": "draft"})):
            response = c.request(method, path, json=body)
            assert response.status_code in (403, 404), f"a producer {method} {path} returned {response.status_code}"
        assert c.get("/me").json()["account"]["role"] == "producer"
    with client() as c:
        assert c.get("/projects/rally").status_code == 200


def test_every_accepted_reel_write_raises_the_version_by_one(reel_producer):
    with client(reel_producer["token"]) as c:
        reel = new_reel(c)
        assert reel["version"] == 1 and reel["state"] == "draft", reel
        rally, eden = project_id(c, "rally"), project_id(c, "eden")
        steps = []
        for call in (lambda r: c.post(f"/reels/{r['id']}/items", json={"project_id": rally, "version": r["version"]}),
                     lambda r: c.patch(f"/reels/{r['id']}", json={"title": unique("Renamed"), "version": r["version"]}),
                     lambda r: c.patch(f"/reels/{r['id']}/items/{rally}", json={"note": "keep", "version": r["version"]}),
                     lambda r: c.post(f"/reels/{r['id']}/items", json={"project_id": eden, "version": r["version"]}),
                     lambda r: c.put(f"/reels/{r['id']}/order", json={"project_ids": [eden, rally], "version": r["version"]}),
                     lambda r: c.delete(f"/reels/{r['id']}/items/{eden}", params={"version": r["version"]}),
                     lambda r: c.patch(f"/reels/{r['id']}", json={"share": True, "version": r["version"]})):
            response = call(reel)
            assert response.status_code in (200, 201), f"an accepted reel write returned {response.status_code}: {response.text[:300]}"
            reel = response.json()
            steps.append(reel["version"])
    assert steps == [2, 3, 4, 5, 6, 7, 8], f"successive accepted writes produced versions {steps}"


def test_stale_reel_write_is_refused_with_the_current_state(reel_producer):
    with client(reel_producer["token"]) as c:
        reel = reel_with(c, ["rally"])
        stale = c.post(f"/reels/{reel['id']}/items", json={"project_id": project_id(c, "eden"),
                                                         "version": reel["version"] - 1})
        assert stale.status_code == 409, f"a write on a stale version returned {stale.status_code}"
        error = error_of(stale)
        assert error["code"] == "conflict" and error["version"] == reel["version"], error
        assert [i["slug"] for i in error["current"]["items"]] == ["rally"], error["current"]
        after = read_reel(c, reel["id"])
    assert (after["version"], after["item_count"]) == (reel["version"], 1), after


def test_simultaneous_reel_writes_on_one_version_accept_exactly_one(reel_producer):
    with client(reel_producer["token"]) as c:
        reel = new_reel(c)
        ids = [project_id(c, slug) for slug in ("archimedes", "glass-planes", "chromatik", "andes-20",
                                                 "secret-tide", "harmonic-drift")]
    clients = warm(len(ids), reel_producer["token"])
    try:
        responses = at_once([lambda c=c, pid=pid: c.post(f"/reels/{reel['id']}/items",
                                                         json={"project_id": pid, "version": reel["version"]})
                             for c, pid in zip(clients, ids)])
    finally:
        for c in clients:
            c.close()
    statuses = sorted(r.status_code for r in responses)
    assert statuses == [201, 409, 409, 409, 409, 409], (
        f"six simultaneous writes carrying version {reel['version']} returned {statuses}; exactly one is accepted"
    )
    with client(reel_producer["token"]) as c:
        after = read_reel(c, reel["id"])
    assert (after["item_count"], after["version"]) == (1, reel["version"] + 1), after


def test_reel_order_and_notes_persist_as_stored_rows(reel_producer, backend):
    note = "<b>Keep this</b> & the sync"
    with client(reel_producer["token"]) as c:
        reel = reel_with(c, ["archimedes", "glass-planes", "chromatik"])
        ids = {slug: project_id(c, slug) for slug in ("archimedes", "glass-planes", "chromatik")}
        reel = c.put(f"/reels/{reel['id']}/order", json={"project_ids": [ids["chromatik"], ids["archimedes"], ids["glass-planes"]],
                                                         "version": reel["version"]}).json()
        reel = c.patch(f"/reels/{reel['id']}/items/{ids['chromatik']}", json={"note": note, "version": reel["version"]}).json()
    with client(reel_producer["token"]) as fresh:
        stored = read_reel(fresh, reel["id"])
    assert [(i["slug"], i["position"]) for i in stored["items"]] == [("chromatik", 1), ("archimedes", 2), ("glass-planes", 3)]
    assert stored["items"][0]["note"] == note, stored["items"][0]
    rows = backend.query("SELECT project_id::text AS project, position, note FROM reel_items "
                         "WHERE reel_id::text = %s ORDER BY position", (str(reel["id"]),))
    assert [(r["project"], r["position"]) for r in rows] == [(str(ids["chromatik"]), 1), (str(ids["archimedes"]), 2),
                                                           (str(ids["glass-planes"]), 3)], rows
    assert rows[0]["note"] == note, rows


def test_removing_an_item_closes_the_position_gap(reel_producer, backend):
    with client(reel_producer["token"]) as c:
        reel = reel_with(c, ["archimedes", "rally", "eden"])
        response = c.delete(f"/reels/{reel['id']}/items/{project_id(c, 'rally')}", params={"version": reel["version"]})
    assert response.status_code == 200, response.text[:300]
    assert [(i["slug"], i["position"]) for i in response.json()["items"]] == [("archimedes", 1), ("eden", 2)]
    positions = [r["position"] for r in backend.query(
        "SELECT position FROM reel_items WHERE reel_id::text = %s ORDER BY position", (str(reel["id"]),))]
    assert positions == [1, 2], positions


def test_reorder_must_list_every_project_exactly_once(reel_producer):
    with client(reel_producer["token"]) as c:
        reel = reel_with(c, ["archimedes", "rally", "eden"])
        a, r, e = (project_id(c, s) for s in ("archimedes", "rally", "eden"))
        for bad in ([a, r], [a, r, r], [a, r, e, project_id(c, "chromatik")]):
            response = c.put(f"/reels/{reel['id']}/order", json={"project_ids": bad, "version": reel["version"]})
            assert response.status_code == 400 and error_of(response)["message"] == ORDER_INVALID, response.text[:300]
        after = read_reel(c, reel["id"])
    assert [i["slug"] for i in after["items"]] == ["archimedes", "rally", "eden"]
    assert after["version"] == reel["version"]


def test_note_is_plain_text_up_to_five_hundred_characters(reel_producer):
    with client(reel_producer["token"]) as c:
        reel = reel_with(c, ["rally"])
        rally = project_id(c, "rally")
        too_long = c.patch(f"/reels/{reel['id']}/items/{rally}", json={"note": "n" * 501, "version": reel["version"]})
        assert too_long.status_code == 400 and error_of(too_long)["message"] == NOTE_TOO_LONG, too_long.text[:300]
        fits = c.patch(f"/reels/{reel['id']}/items/{rally}", json={"note": "n" * 500, "version": reel["version"]})
        assert fits.status_code == 200 and fits.json()["items"][0]["note"] == "n" * 500


def test_duplicate_or_sixteenth_item_is_refused(reel_producer):
    set_project_state(DRAFT_SLUG, "published")
    try:
        with client(reel_producer["token"]) as c:
            slugs = [row["slug"] for row in rows_of(projects(c))]
            assert len(slugs) == 16, slugs
            reel = reel_with(c, slugs[:14])
            duplicate = add_item(c, reel, slugs[0])
            assert duplicate.status_code == 409 and error_of(duplicate)["message"] == ALREADY_ON_REEL, duplicate.text[:300]
            fifteenth = add_item(c, reel, slugs[14])
            assert fifteenth.status_code == 201, f"a fifteenth item returned {fifteenth.status_code}"
            sixteenth = add_item(c, fifteenth.json(), slugs[15])
            assert sixteenth.status_code == 409, f"a sixteenth item returned {sixteenth.status_code}"
            assert error_of(sixteenth)["message"] == REEL_ITEM_LIMIT
    finally:
        set_project_state(DRAFT_SLUG, "draft")


def test_offline_star_is_held_then_sent_in_order(page, reel_producer):
    with client(reel_producer["token"]) as c:
        reel = new_reel(c, title=unique("Offline reel"))
    _sign_in_through_the_form(page, reel_producer["email"], reel_producer["password"])
    page.wait_for_url(re.compile(r"/desk"))
    page.goto(f"{app_url()}/work")
    star = page.get_by_role("button", name=_exact("Add Archimedes to your reel")).first
    star.wait_for(state="attached")
    page.get_by_text(re.compile(r"PP_00", re.I)).first.wait_for(state="attached")
    page.context.set_offline(True)
    page.get_by_text(_exact("You are offline. Changes are held.")).first.wait_for(state="attached")
    _press(page, star)
    page.get_by_text(re.compile(r"PP_01", re.I)).first.wait_for(state="attached")
    page.context.set_offline(False)
    page.wait_for_function("() => !/you are offline\\. changes are held\\./i.test(document.body.textContent)",
                           timeout=20000)
    with client(reel_producer["token"]) as c:
        for _ in range(10):
            stored = read_reel(c, reel["id"])
            if stored["items"]:
                break
            settle(1.0)
    assert [i["slug"] for i in stored["items"]] == ["archimedes"], (
        f"the star held offline did not reach the reel once online: {stored['items']}"
    )


def test_refused_star_rolls_back_before_the_failure_shows(page, reel_producer):
    _sign_in_through_the_form(page, reel_producer["email"], reel_producer["password"])
    page.wait_for_url(re.compile(r"/desk"))
    page.goto(f"{app_url()}/work")
    star = page.get_by_role("button", name=_exact("Add Chromatik to your reel")).first
    star.wait_for(state="attached")
    page.wait_for_function("() => /PP_\\d{2}/i.test(document.body.textContent)")
    before = re.search(r"PP_(\d{2})", page.evaluate("() => document.body.textContent"), re.I).group(0).upper()
    refusal = {"error": {"code": "limit", "message": REEL_ITEM_LIMIT, "field": None, "version": None, "current": None}}

    def refuse(route):
        if route.request.method == "POST":
            route.fulfill(status=409, content_type="application/json", body=json.dumps(refusal))
        else:
            route.continue_()

    page.route(re.compile(r".*/api/reels/[^/?]+/items.*"), refuse)
    _press(page, star)
    page.get_by_text(_exact(REEL_ITEM_LIMIT)).first.wait_for(state="attached")
    shown = re.search(r"PP_(\d{2})", page.evaluate("() => document.body.textContent"), re.I).group(0).upper()
    assert shown == before, f"the failure showed while the capsule still read {shown}, expected {before} restored"
    assert page.get_by_role("button", name=_exact("Add Chromatik to your reel")).count() >= 1, (
        "the refused star was not put back before the failure appeared"
    )


def test_ten_reels_per_producer_with_title_confirmed_delete(reel_producer, backend):
    with client(reel_producer["token"]) as c:
        refused = None
        for _ in range(11):
            response = c.post("/reels", json={"title": unique("Limit reel")})
            if response.status_code != 201:
                refused = response
                break
        assert refused is not None and refused.status_code == 409, "an eleventh reel was accepted"
        assert error_of(refused)["message"] == REEL_LIMIT
        listed = rows_of(c.get("/reels").json())
        assert len(listed) == 10, f"the producer lists {len(listed)} reels"
        target = [r for r in listed if r["state"] == "draft"][0]
        wrong = c.delete(f"/reels/{target['id']}", params={"version": target["version"], "confirm_title": "wrong title"})
        assert wrong.status_code in (400, 409) and error_of(wrong)["message"] == CONFIRM_TITLE, wrong.text[:300]
        right = c.delete(f"/reels/{target['id']}", params={"version": target["version"], "confirm_title": target["title"]})
        assert right.status_code == 200, right.text[:300]
        assert c.get(f"/reels/{target['id']}").status_code == 404
        assert c.post("/reels", json={"title": unique("After delete")}).status_code == 201
    kept = backend.query("SELECT deleted_at FROM reels WHERE id::text = %s", (str(target["id"]),))
    assert len(kept) == 1 and kept[0]["deleted_at"] is not None, "a deleted reel was erased rather than kept recoverable"


def test_seeded_catalogue_rows_persist_exactly_once(backend):
    assert backend.count("categories") == 5
    assert backend.count("projects") == 16
    assert backend.count("tracks") == 4
    for email in (ADMIN_EMAIL, EDITOR_EMAIL, PRODUCER_EMAIL, PRODUCER2_EMAIL):
        rows = backend.query("SELECT password_hash::text AS hash FROM accounts WHERE email = %s", (email,))
        assert len(rows) == 1, f"{email} is stored {len(rows)} times"
        assert PASSWORD not in (rows[0]["hash"] or ""), f"{email} stores a readable password"
    assert backend.count("reels", title=SEEDED_REEL_TITLE) == 1
    assert backend.count("pitches", reference=SEEDED_PITCH_REFERENCE) == 1


def test_other_producers_reel_answers_like_a_missing_one(producer_token, producer2_token):
    seeded = _seeded_reel_id(producer_token)
    with client(producer2_token) as c:
        rally = project_id(c, "rally")
        answers = [c.get(f"/reels/{seeded}"), c.get(f"/reels/{_missing_id_like(seeded)}"), c.get("/reels/not-a-reel-id")]
        writes = [c.patch(f"/reels/{seeded}", json={"title": "taken", "version": 1}),
                  c.post(f"/reels/{seeded}/items", json={"project_id": rally, "version": 1}),
                  c.put(f"/reels/{seeded}/order", json={"project_ids": [rally], "version": 1})]
    statuses = [r.status_code for r in answers + writes]
    assert statuses == [404] * 6, f"another producer's, a missing and a malformed reel answered {statuses}"
    bodies = [r.json() for r in answers]
    assert bodies[0] == bodies[1] == bodies[2], f"the not-found bodies differ: {bodies}"
    with client(producer_token) as c:
        kept = read_reel(c, seeded)
    assert kept["title"] == SEEDED_REEL_TITLE and kept["item_count"] == 3


def test_editor_reads_any_reel_but_is_denied_writes(producer_token, editor_token):
    seeded = _seeded_reel_id(producer_token)
    with client(editor_token) as c:
        read = c.get(f"/reels/{seeded}")
        assert read.status_code == 200 and read.json()["title"] == SEEDED_REEL_TITLE
        write = c.patch(f"/reels/{seeded}", json={"title": "Editor rename", "version": read.json()["version"]})
        assert write.status_code == 403 and error_of(write)["code"] == "forbidden", write.text[:300]


def test_shared_link_reads_notes_for_any_signed_in_role(producer2_token, reel_producer, editor_token):
    with client(producer2_token) as c:
        reel = reel_with(c, ["rally"])
        rally = project_id(c, "rally")
        reel = c.patch(f"/reels/{reel['id']}/items/{rally}", json={"note": "shared note", "version": reel["version"]}).json()
        shared = c.patch(f"/reels/{reel['id']}", json={"share": True, "version": reel["version"]}).json()
    token = shared["share_token"]
    assert token, shared
    for viewer in (reel_producer["token"], editor_token):
        with client(viewer) as c:
            response = c.get(f"/shared/{token}")
        assert response.status_code == 200 and response.json()["items"][0]["note"] == "shared note", response.text[:300]
        assert response.json()["owner_organisation"] == "Farrow Kiln"
    with client() as c:
        assert c.get(f"/shared/{token}").status_code == 401
    with client(producer2_token) as c:
        revoked = c.patch(f"/reels/{reel['id']}", json={"share": False, "version": shared["version"]})
        assert revoked.status_code == 200 and revoked.json()["share_token"] is None, revoked.text[:300]
    with client(reel_producer["token"]) as c:
        after = c.get(f"/shared/{token}")
        never = c.get(f"/shared/{unique('never-minted')}")
    assert after.status_code == never.status_code == 404 and after.json() == never.json(), (after.text, never.text)


def test_other_producers_pitch_answers_like_a_missing_one(producer_token, producer2_token):
    pitch = _seeded_pitch(producer_token)
    with client(producer2_token) as c:
        answers = [c.get(f"/pitches/{pitch['id']}"), c.get(f"/pitches/{_missing_id_like(pitch['id'])}"),
                   c.post(f"/pitches/{pitch['id']}/messages", json={"body": "hello"}),
                   c.patch(f"/pitches/{pitch['id']}", json={"state": "withdrawn"})]
    assert [r.status_code for r in answers] == [404] * 4, [r.status_code for r in answers]
    assert answers[0].json() == answers[1].json()


def test_seeded_reel_and_pitch_belong_to_the_seeded_producer(producer_token):
    with client(producer_token) as c:
        reel = read_reel(c, _seeded_reel_id(producer_token))
        pitch = c.get(f"/pitches/{_seeded_pitch(producer_token)['id']}").json()
    assert reel["state"] == "submitted"
    assert [(i["slug"], i["position"]) for i in reel["items"]] == [("rally", 1), ("eden", 2), ("glass-planes", 3)]
    assert reel["items"][0]["note"] == "The sync across devices is the part to show"
    assert (pitch["state"], pitch["budget_band"], pitch["timing"], pitch["organisation"]) == (
        "in_conversation", "100k-250k", "next-quarter", "Northlight Agency"), pitch
    assert pitch["messages"][0]["body"] == "Thanks, this is a good fit. We will set up a call."
    assert pitch["messages"][0]["author_role"] == "editor"


def test_simultaneous_submissions_create_one_pitch_and_one_mail_pair(pitch_producer):
    with client(pitch_producer["token"]) as c:
        reel = reel_with(c, ["archimedes", "rally"])
    clients = warm(4, pitch_producer["token"])
    try:
        responses = at_once([lambda c=c: c.post("/pitches", json=pitch_body(reel)) for c in clients])
    finally:
        for c in clients:
            c.close()
    statuses = sorted(r.status_code for r in responses)
    assert statuses == [201, 422, 422, 422], f"four simultaneous submissions of one reel returned {statuses}"
    reference = [r.json() for r in responses if r.status_code == 201][0]["reference"]
    assert re.fullmatch(r"PT-\d{6}", reference), reference
    with client(pitch_producer["token"]) as c:
        mine = [p for p in rows_of(c.get("/pitches").json()) if str(p["reel_id"]) == str(reel["id"])]
    assert len(mine) == 1, f"the reel carries {len(mine)} pitches"
    wait_for_mails(pitch_producer["email"], f"{PITCH_RECEIPT} {reference}")
    settle(3.0)
    receipts = mails_to(pitch_producer["email"], f"{PITCH_RECEIPT} {reference}")
    studio = [m for m in mails_to(STUDIO_QUEUE, PITCH_STUDIO)
              if m["subject"] == f"{PITCH_STUDIO} {pitch_producer['organisation']} {reference}"]
    assert len(receipts) == 1 and receipts[0]["subject"] == f"{PITCH_RECEIPT} {reference}", receipts
    assert len(studio) == 1, f"the studio queue received {len(studio)} mails for {reference}"
    assert receipts[0]["html"].strip() == "" and len(LINK_RE.findall(receipts[0]["text"])) == 1
    assert "/desk/pitches/" in LINK_RE.findall(receipts[0]["text"])[0], receipts[0]["text"][:300]
    assert "/studio/pitches" in LINK_RE.findall(studio[0]["text"])[0], studio[0]["text"][:300]


def test_submitted_reel_refuses_writes_but_still_shares(pitch_producer):
    reel, _ = _submitted_pitch(pitch_producer["token"], ["glass-planes"])
    with client(pitch_producer["token"]) as c:
        current = read_reel(c, reel["id"])
        assert current["state"] == "submitted", current
        glass = project_id(c, "glass-planes")
        for response in (add_item(c, current, "eden"),
                         c.put(f"/reels/{reel['id']}/order", json={"project_ids": [glass], "version": current["version"]}),
                         c.patch(f"/reels/{reel['id']}/items/{glass}", json={"note": "late", "version": current["version"]}),
                         c.patch(f"/reels/{reel['id']}", json={"title": "late", "version": current["version"]})):
            assert response.status_code == 409 and error_of(response)["message"] == REEL_SENT, response.text[:300]
        shared = c.patch(f"/reels/{reel['id']}", json={"share": True, "version": current["version"]})
        assert shared.status_code == 200 and shared.json()["share_token"], shared.text[:300]
        deleted = c.delete(f"/reels/{reel['id']}", params={"version": shared.json()["version"],
                                                          "confirm_title": current["title"]})
        assert deleted.status_code in (400, 409) and error_of(deleted)["message"] == OPEN_PITCH_DELETE, deleted.text[:300]


def test_pitch_fields_are_refused_with_their_messages(pitch_producer):
    with client(pitch_producer["token"]) as c:
        reel = reel_with(c, ["chromatik"])
        before = c.get("/me").json()["pitch_counts"]
        for override, field, message in (({"budget_band": None}, "budget_band", CHOOSE_BUDGET),
                                         ({"timing": "soon"}, "timing", CHOOSE_TIMEFRAME),
                                         ({"summary": "x" * 19}, "summary", SUMMARY_SHORT),
                                         ({"summary": "x" * 2001}, "summary", SUMMARY_LONG),
                                         ({"contact_preference": "fax"}, "contact_preference", CHOOSE_REPLY)):
            response = c.post("/pitches", json=pitch_body(reel, **override))
            assert response.status_code == 400, f"a pitch with {override} returned {response.status_code}"
            error = error_of(response)
            assert (error["field"], error["message"]) == (field, message), error
        empty = new_reel(c)
        refused = c.post("/pitches", json=pitch_body(empty))
        assert refused.status_code in REFUSED and error_of(refused)["message"] == NO_ITEMS, refused.text[:300]
        assert c.get("/me").json()["pitch_counts"] == before
        assert read_reel(c, reel["id"])["state"] == "draft"


def test_unverified_producer_is_denied_a_pitch(unverified_account):
    with client(unverified_account["token"]) as c:
        reel = reel_with(c, ["rally"])
        response = c.post("/pitches", json=pitch_body(reel))
        assert response.status_code in (403, 422) and error_of(response)["message"] == NOT_VERIFIED, response.text[:300]
        assert read_reel(c, reel["id"])["state"] == "draft"


def test_unavailable_item_is_excluded_from_the_pitch(pitch_producer):
    with client(pitch_producer["token"]) as c:
        reel = reel_with(c, ["archimedes", "chromatik"])
    set_project_state("chromatik", "draft")
    try:
        with client(pitch_producer["token"]) as c:
            current = read_reel(c, reel["id"])
            assert [(i["slug"], i["available"]) for i in current["items"]] == [("archimedes", True), ("chromatik", False)], current["items"]
            response = c.post("/pitches", json=pitch_body(current))
        assert response.status_code == 201, response.text[:300]
        assert (response.json()["items"], response.json()["excluded"]) == (["Archimedes"], ["Chromatik"]), response.json()
    finally:
        set_project_state("chromatik", "published")


def test_open_pitches_stop_at_five(pitch_producer):
    with client(pitch_producer["token"]) as c:
        refused = None
        for _ in range(6 - c.get("/me").json()["pitch_counts"]["open"]):
            reel = reel_with(c, ["frontier-beyond"])
            response = c.post("/pitches", json=pitch_body(reel))
            if response.status_code != 201:
                refused = response
                break
        assert refused is not None, "a sixth open pitch was accepted"
        assert c.get("/me").json()["pitch_counts"]["open"] == 5
    assert refused.status_code == 422 and error_of(refused)["message"] == OPEN_PITCH_LIMIT, refused.text[:300]


def test_studio_reply_moves_the_pitch_and_mails_the_producer(pitch_producer, editor_token):
    pitch = _open_pitch_without_messages(pitch_producer["token"], state="submitted")
    with client(editor_token) as c:
        replied = c.post(f"/pitches/{pitch['id']}/messages", json={"body": "We would love to talk."})
    assert replied.status_code == 201 and replied.json()["state"] == "in_conversation", replied.text[:300]
    subject = f"{STUDIO_REPLIED} {pitch['reference']}"
    mails = [m for m in wait_for_mails(pitch_producer["email"], subject) if m["subject"] == subject]
    assert len(mails) == 1, f"the producer received {len(mails)} {subject!r} mails"
    assert mails[0]["to"] == [pitch_producer["email"]] and mails[0]["html"].strip() == ""
    with client(pitch_producer["token"]) as c:
        kept = c.post(f"/pitches/{pitch['id']}/messages", json={"body": "Thank you, talk soon."})
        assert kept.status_code == 201 and kept.json()["state"] == "in_conversation", kept.text[:300]
        forbidden = c.patch(f"/pitches/{pitch['id']}", json={"state": "closed"})
        assert forbidden.status_code == 403, f"the producer closing their pitch returned {forbidden.status_code}"
    settle(3.0)
    assert len([m for m in mails_to(pitch_producer["email"], subject) if m["subject"] == subject]) == 1, (
        "a producer's own message sent another studio reply mail"
    )


def test_pitch_page_shows_a_studio_reply_without_a_reload(page, pitch_producer, editor_token):
    with client(pitch_producer["token"]) as c:
        live = [p for p in rows_of(c.get("/pitches").json()) if p["state"] == "in_conversation"]
    assert live, "the pitch producer has no pitch in conversation to watch"
    pitch = live[0]
    _sign_in_through_the_form(page, pitch_producer["email"], pitch_producer["password"])
    page.wait_for_url(re.compile(r"/desk"))
    page.goto(f"{app_url()}/desk/pitches/{pitch['id']}")
    page.get_by_text(re.compile(re.escape(pitch["reference"]), re.I)).first.wait_for(state="attached")
    page.evaluate("() => { window.__sameDocument = true; }")
    body = unique("Live reply")
    with client(editor_token) as c:
        assert c.post(f"/pitches/{pitch['id']}/messages", json={"body": body}).status_code == 201
    page.get_by_text(re.compile(re.escape(body), re.I)).first.wait_for(state="attached", timeout=25000)
    assert page.evaluate("() => window.__sameDocument === true"), "the pitch page reloaded to show the reply"


def test_withdrawing_returns_the_reel_to_draft_and_mails_the_studio(pitch_producer):
    pitch = _open_pitch_without_messages(pitch_producer["token"], state="submitted")
    with client(pitch_producer["token"]) as c:
        withdrawn = c.patch(f"/pitches/{pitch['id']}", json={"state": "withdrawn"})
        assert withdrawn.status_code == 200 and withdrawn.json()["state"] == "withdrawn", withdrawn.text[:300]
        reel = read_reel(c, pitch["reel_id"])
        assert reel["state"] == "draft", reel
        assert add_item(c, reel, "welcome-to-stonehall").status_code == 201
        again = c.patch(f"/pitches/{pitch['id']}", json={"state": "withdrawn"})
        assert again.status_code in REFUSED and error_of(again)["message"] == PITCH_CHANGE, again.text[:300]
    subject = f"{PITCH_WITHDRAWN} {pitch['reference']}"
    mails = [m for m in wait_for_mails(STUDIO_QUEUE, subject) if m["subject"] == subject]
    assert len(mails) == 1, f"the studio queue received {len(mails)} withdrawal mails for {pitch['reference']}"


def test_closed_pitch_refuses_messages_and_changes(pitch_producer, editor_token):
    pitch = _open_pitch_without_messages(pitch_producer["token"])
    with client(editor_token) as c:
        closed = c.patch(f"/pitches/{pitch['id']}", json={"state": "closed"})
        assert closed.status_code == 200 and closed.json()["state"] == "closed", closed.text[:300]
        reopened = c.patch(f"/pitches/{pitch['id']}", json={"state": "acknowledged"})
        assert reopened.status_code in REFUSED and error_of(reopened)["message"] == PITCH_CHANGE, reopened.text[:300]
    with client(pitch_producer["token"]) as c:
        late = c.post(f"/pitches/{pitch['id']}/messages", json={"body": "One more thing"})
    assert late.status_code in REFUSED and error_of(late)["message"] == PITCH_CLOSED, late.text[:300]


def test_pitch_messages_stop_at_twenty_an_hour(pitch_producer):
    pitch = _open_pitch_without_messages(pitch_producer["token"])
    with client(pitch_producer["token"]) as c:
        statuses = [c.post(f"/pitches/{pitch['id']}/messages", json={"body": f"note {n}"}).status_code for n in range(20)]
        assert statuses == [201] * 20, statuses
        limited = c.post(f"/pitches/{pitch['id']}/messages", json={"body": "one too many"})
        assert limited.status_code == 429 and error_of(limited)["message"] == MESSAGE_LIMIT, limited.text[:300]
        assert len(c.get(f"/pitches/{pitch['id']}").json()["messages"]) == 20


def test_studio_queue_lists_pitches_newest_first(pitch_producer, editor_token, producer2_token):
    with client(pitch_producer["token"]) as c:
        mine = rows_of(c.get("/pitches").json())
    newest = max(mine, key=lambda p: p["submitted_at"])
    with client(editor_token) as c:
        queue = rows_of(c.get("/pitches").json())
    assert queue[0]["reference"] == newest["reference"], [p["reference"] for p in queue[:3]]
    assert queue[0]["organisation"] == pitch_producer["organisation"]
    stamps = [p["submitted_at"] for p in queue]
    assert stamps == sorted(stamps, reverse=True), "the studio queue is not newest first"
    assert SEEDED_PITCH_REFERENCE in [p["reference"] for p in queue]
    with client(producer2_token) as c:
        assert newest["reference"] not in [p["reference"] for p in rows_of(c.get("/pitches").json())]


def test_assistant_answer_names_the_project_without_a_link():
    response = _ask("What is the project link for this one, and who was it for?", "rally")
    assert response.status_code == 200, response.text[:300]
    assert response.headers.get("content-type", "").startswith("text/plain"), response.headers.get("content-type")
    assert "rally" in response.text.lower(), f"the answer does not name the project: {response.text[:300]}"
    assert "http://" not in response.text and "https://" not in response.text, (
        f"the assistant answer carries an outbound link: {response.text[:300]}"
    )


def test_assistant_refuses_empty_or_long_questions():
    long = _ask("q" * 501)
    assert long.status_code == 400 and error_of(long)["message"] == QUESTION_TOO_LONG, long.text[:300]
    empty = _ask("")
    assert empty.status_code == 400 and error_of(empty)["message"] == "Ask a question first.", empty.text[:300]
    assert _ask("q" * 500).status_code == 200


def test_assistant_stops_at_forty_questions_a_session():
    first = _ask("What does the studio make?")
    assert first.status_code == 200, first.text[:300]
    cookie = _assistant_cookie(first)
    assert cookie, "the first answer set no assistant_session cookie"
    headers = {"Cookie": f"assistant_session={cookie}"}
    statuses = [_ask(f"What does the studio make? {n}", headers=headers).status_code for n in range(39)]
    assert statuses == [200] * 39, statuses
    limited = _ask("One more?", headers=headers)
    assert limited.status_code == 429 and error_of(limited)["message"] == QUESTION_LIMIT, limited.text[:300]


def test_assistant_turn_is_stored_without_an_account(backend, producer2_token):
    before = backend.count("assistant_turns")
    assert _ask("What is this one about?", "eden", headers={"Authorization": f"Bearer {producer2_token}"}).status_code == 200
    assert backend.count("assistant_turns") == before + 1
    columns = [r["column_name"] for r in backend.query(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'assistant_turns'")]
    leaked = [col for col in columns if any(word in col for word in ("account", "owner", "user", "email"))]
    assert not leaked, f"assistant_turns carries account columns {leaked}"


def test_events_before_consent_store_only_the_exempt_three(backend):
    marker = unique("probe-slug")
    duration = 7_000_000 + int.from_bytes(uuid.uuid4().bytes[:2], "big")
    with client() as c:
        for consent, expected in (("unanswered", False), ("rejected", False), ("accepted", True)):
            response = c.post("/events", json={"name": "state_enter", "consent": consent,
                                               "properties": {"state": "reel", "slug": marker, "role": "anonymous"}})
            assert response.status_code == 202 and response.json() == {"stored": expected}, (consent, response.text[:300])
        exempt = c.post("/events", json={"name": "loader_complete", "consent": "unanswered",
                                         "properties": {"duration": duration, "asset_count": 75}})
        assert exempt.status_code == 202 and exempt.json() == {"stored": True}, exempt.text[:300]
    rows = backend.query("SELECT name FROM analytics_events WHERE properties::text LIKE %s", (f"%{marker}%",))
    assert [r["name"] for r in rows] == ["state_enter"], f"stored rows for the marker: {rows}"
    assert len(backend.query("SELECT name FROM analytics_events WHERE properties::text LIKE %s", (f"%{duration}%",))) == 1


def test_event_carrying_typed_text_is_refused(backend):
    secret = unique("secret words")
    with client() as c:
        response = c.post("/events", json={"name": "search_submit", "consent": "accepted",
                                           "properties": {"length": len(secret), "query": secret}})
        unknown = c.post("/events", json={"name": "keystroke", "consent": "accepted", "properties": {}})
    assert response.status_code in (400, 422) and error_of(response)["message"] == EVENT_PROPERTY, response.text[:300]
    assert unknown.status_code in (400, 422), unknown.text[:300]
    assert backend.query("SELECT count(*) AS n FROM analytics_events WHERE properties::text LIKE %s",
                         (f"%{secret}%",))[0]["n"] == 0


def test_enquiry_decoy_field_refuses_and_stores_nothing(backend):
    email = unique_email("decoy")
    before = backend.count("enquiries")
    response = _enquiry(email, company_website="https://spam.example.com")
    assert response.status_code == 400, f"an enquiry with the decoy filled returned {response.status_code}"
    assert backend.count("enquiries") == before
    settle(2.0)
    assert mails_to(email) == [], "a refused enquiry still sent mail"


def test_enquiry_fields_are_refused_with_their_messages(backend):
    before = backend.count("enquiries")
    for override, field in (({"name": ""}, "name"), ({"email": "nope"}, "email"), ({"timing": "whenever"}, "timing"),
                            ({"summary": "short"}, "summary"), ({"contact_preference": "pigeon"}, "contact_preference")):
        response = _enquiry(unique_email("fields"), **override)
        assert response.status_code == 400 and error_of(response)["field"] == field, (override, response.text[:300])
    assert backend.count("enquiries") == before


def test_enquiry_sends_two_plain_text_mails_with_its_reference():
    email = unique_email("enquiry")
    response = _enquiry(email)
    assert response.status_code == 201, response.text[:300]
    reference = response.json()["reference"]
    assert re.fullmatch(r"EN-\d{6}", reference), reference
    mine = wait_for_mails(email, f"{ENQUIRY_RECEIPT} {reference}")
    subject = f"{ENQUIRY_STUDIO} Ada Lin {reference}"
    studio = [m for m in wait_for_mails(STUDIO_QUEUE, subject) if m["subject"] == subject]
    assert len(mine) == 1 and mine[0]["subject"] == f"{ENQUIRY_RECEIPT} {reference}", mine
    assert len(studio) == 1, f"the studio queue received {len(studio)} mails for {reference}"
    for mail in (mine[0], studio[0]):
        assert mail["html"].strip() == "" and len(LINK_RE.findall(mail["text"])) == 1, mail["text"][:300]
        assert mail["cc"] == [] and mail["bcc"] == []
        assert LINK_RE.findall(mail["text"])[0].rstrip(".").endswith("/contact"), mail["text"][:300]
    assert email in mine[0]["text"] and STUDIO_QUEUE in studio[0]["text"]


def test_enquiries_beyond_five_an_hour_are_refused():
    statuses = []
    last = None
    for _ in range(6):
        last = _enquiry(unique_email("burst"))
        statuses.append(last.status_code)
    assert 429 in statuses, f"six enquiries in a row returned {statuses}; the sixth in an hour is refused"
    cut = statuses.index(429)
    assert set(statuses[:cut]) <= {201} and set(statuses[cut:]) == {429}, statuses
    assert error_of(last)["message"] == ENQUIRY_LIMIT


def test_role_change_ends_every_session_of_that_account(role_account):
    with client(role_account["token"]) as c:
        account_id = c.get("/me").json()["account"]["id"]
    with client(signin(ADMIN_EMAIL)) as admin:
        promoted = admin.patch(f"/accounts/{account_id}", json={"role": "editor"})
        assert promoted.status_code == 200, promoted.text[:300]
        with client(role_account["token"]) as old:
            stale = old.get("/me")
        assert stale.status_code == 401, f"a token issued before the role change still reads /api/me: {stale.status_code}"
        with client(signin(role_account["email"], role_account["password"])) as fresh:
            assert fresh.get("/me").json()["account"]["role"] == "editor"
            assert fresh.get(f"/projects/{DRAFT_SLUG}").status_code == 200
        assert admin.patch(f"/accounts/{account_id}", json={"role": "producer"}).status_code == 200


def test_admin_cannot_change_their_own_role():
    with client(signin(ADMIN_EMAIL)) as c:
        admin_id = c.get("/me").json()["account"]["id"]
        response = c.patch(f"/accounts/{admin_id}", json={"role": "editor"})
        assert response.status_code in (400, 403, 409, 422), response.text[:300]
        assert error_of(response)["message"] == OWN_ROLE, response.text[:300]
        assert c.get("/me").json()["account"]["role"] == "admin"


def test_simultaneous_admin_demotions_keep_one_admin(role_account):
    with client(signin(role_account["email"], role_account["password"])) as c:
        other_id = c.get("/me").json()["account"]["id"]
    with client(signin(ADMIN_EMAIL)) as admin:
        admin_id = admin.get("/me").json()["account"]["id"]
        assert admin.patch(f"/accounts/{other_id}", json={"role": "admin"}).status_code == 200
    first = warm(1, signin(ADMIN_EMAIL))[0]
    second = warm(1, signin(role_account["email"], role_account["password"]))[0]
    try:
        responses = at_once([lambda: first.patch(f"/accounts/{other_id}", json={"role": "editor"}),
                             lambda: second.patch(f"/accounts/{admin_id}", json={"role": "editor"})])
    finally:
        first.close()
        second.close()
    accepted = [r for r in responses if r.status_code == 200]
    refused = [r for r in responses if r.status_code != 200]
    assert len(accepted) == 1 and len(refused) == 1, (
        f"two admins demoting each other at once returned {[r.status_code for r in responses]}; exactly one change succeeds"
    )
    assert refused[0].status_code in (400, 401, 403, 409, 422), refused[0].text[:300]
    if refused[0].status_code != 401:
        assert error_of(refused[0])["message"] == LAST_OWNER, refused[0].text[:300]
    admin_kept = responses[0].status_code == 200
    survivor = signin(ADMIN_EMAIL) if admin_kept else signin(role_account["email"], role_account["password"])
    with client(survivor) as c:
        roles = [a["role"] for a in rows_of(c.get("/accounts").json())]
        assert roles.count("admin") == 1, f"after the race the product has {roles.count('admin')} admins"
        if not admin_kept:
            assert c.patch(f"/accounts/{admin_id}", json={"role": "admin"}).status_code == 200
    with client(signin(ADMIN_EMAIL)) as c:
        assert c.patch(f"/accounts/{other_id}", json={"role": "producer"}).status_code == 200
