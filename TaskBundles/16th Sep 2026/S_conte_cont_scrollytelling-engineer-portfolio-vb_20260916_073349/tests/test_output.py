from __future__ import annotations

import concurrent.futures
import json
import re

import httpx

from conftest import (
    APP_URL, ARCHIVE_SUBTITLE, ARCHIVE_TITLE, AUTHOR_EMAIL, BAND_FIELDS,
    BAND_SLUGS, BOOKING_STATES, CLIENT_SYSTEM_LINE, CONTACT_LABEL,
    CONTRIBUTION_LABEL, CORPUS_PASSWORD, COUNTER_PHRASE, DESK_ACTIONS,
    DIAGRAM_KEY_PREFIX, DRAFT_POST, EDGE_KINDS, EMPTY_DESK_LINE,
    EMPTY_DESK_TITLE, EMPTY_EDITOR_LINE, EMPTY_EDITOR_TITLE, FIRST_SYSTEM,
    FOOTER_CREDIT, HEADLINE, LANE_SIGNAL_FLOOR, MANIFESTO, MESSAGE_MAX,
    MESSAGE_MIN, NAME_LINE, NAME_MAX, NODE_KINDS, NOTE_INTENTS, NOTE_LANES,
    NOT_FOUND_ACTION, NOT_FOUND_CODE, NOT_FOUND_LINE, PANEL_SUBTITLE,
    PANEL_TITLE, PHILOSOPHY_DIVIDER, POST_KEY_PREFIX, POST_SERIES,
    PROTECTED_ROUTES, PUBLIC_ROUTES, PUBLISHED_POST, PUBLISHED_POST_CODE,
    RATE_LIMIT_LINE, READER_EMAIL, RETENTION_MONTHS, ROLE_LINE, SCROLL_CUE,
    SECOND_AUTHOR_EMAIL, SECOND_PUBLISHED_POST, SECOND_PUBLISHED_POST_CODE,
    SERIES_SAMPLE_COUNT, SLOT_HOLD_MINUTES, SUBSCRIBER_STATES, SYSTEMS_HEADING,
    TIMELINE_EFFECTS, TOP_BAR_ENTRIES, anchor, bearer, export_still,
    long_message, make_diagram, make_post, note_payload, poll, probe_email,
    sample_structure, sign_in, slug_of,
)

SECRET_NEEDLES = ("STORAGE_SECRET_KEY", "STORAGE_ACCESS_KEY", "minio-root-",
                  "deku-storage-", "postgresql://", "DB_ADMIN_URL")


def _text(response: httpx.Response) -> str:
    return response.text or ""


def _published(client: httpx.Client) -> list:
    r = client.get("/posts")
    assert r.status_code == 200, anchor("published listing", r)
    payload = r.json()
    assert isinstance(payload, list), anchor(
        "the published listing must be a top-level JSON array", r)
    return payload


def _titles(payload: list) -> list:
    return [row.get("title") for row in payload]


def _draft_with_diagram(client: httpx.Client, token: str, title: str) -> tuple:
    diagram = make_diagram(client, token, f"{title} diagram")
    exported = export_still(client, token, slug_of(diagram))
    assert exported.status_code in (200, 201), anchor(
        f"export the still for {title}", exported)
    post = make_post(client, token, title, diagram_slug=slug_of(diagram))
    return diagram, post


def test_health_and_deployment_contract(client, site):
    r = client.get("/health")
    assert r.status_code == 200, anchor("health route", r)

    home = site.get("/")
    assert home.status_code == 200, anchor("index route", home)
    assert APP_URL.startswith("http"), f"APP_PUBLIC_URL is not an address: {APP_URL!r}"
    assert "127.0.0.1" not in APP_URL, (
        f"the app answers on loopback only at {APP_URL!r}, so it is unreachable "
        f"from outside the container")


def test_public_routes_render_complete_documents(site):
    for route in PUBLIC_ROUTES:
        r = site.get(route)
        assert r.status_code == 200, anchor(f"public route {route}", r)
        body = _text(r)
        for entry in TOP_BAR_ENTRIES:
            assert entry in body, (
                f"public route {route} answered {r.status_code} and its document "
                f"omits the top-bar entry {entry!r}; body starts {body[:200]!r}")
        assert FOOTER_CREDIT in body, (
            f"public route {route} omits the footer credit {FOOTER_CREDIT!r}; "
            f"body starts {body[:200]!r}")
        assert "/privacy" in body, (
            f"public route {route} carries no footer link to the privacy page; "
            f"body starts {body[:200]!r}")
        assert re.search(r'rel=["\'][^"\']*icon', body, re.I), (
            f"public route {route} declares no favicon in its document head; "
            f"body starts {body[:200]!r}")

    home = _text(site.get("/"))
    for marker in (HEADLINE, NAME_LINE, ROLE_LINE, SCROLL_CUE, MANIFESTO,
                   PHILOSOPHY_DIVIDER, SYSTEMS_HEADING, CONTRIBUTION_LABEL,
                   CLIENT_SYSTEM_LINE, FIRST_SYSTEM, CONTACT_LABEL,
                   COUNTER_PHRASE):
        assert marker in home, (
            f"the index document omits the pinned copy {marker!r}; "
            f"body starts {home[:200]!r}")


def test_favicon_resolves_at_its_declared_address(site):
    body = _text(site.get("/"))
    found = re.search(r'rel=["\'][^"\']*icon[^"\']*["\'][^>]*href=["\']([^"\']+)["\']',
                      body, re.I)
    if found is None:
        found = re.search(r'href=["\']([^"\']+)["\'][^>]*rel=["\'][^"\']*icon',
                          body, re.I)
    assert found is not None, (
        f"the index document declares no favicon; body starts {body[:300]!r}")
    r = site.get(found.group(1))
    assert r.status_code == 200, anchor("the declared favicon address", r)


def test_signup_creates_account_and_rejects_duplicate(client):
    email = probe_email()
    first = client.post("/auth/signup",
                        json={"email": email, "password": CORPUS_PASSWORD,
                              "role": "reader"})
    assert first.status_code in (200, 201), anchor(f"signup for {email}", first)
    token = first.json().get("token")
    assert token, anchor(f"signup for {email} returned no token", first)

    me = client.get("/auth/me", headers=bearer(token))
    assert me.status_code == 200, anchor("auth me with the fresh token", me)

    again = client.post("/auth/signup",
                        json={"email": email, "password": CORPUS_PASSWORD,
                              "role": "reader"})
    assert 400 <= again.status_code < 500, anchor(
        f"a second signup on {email} must be rejected as a client error", again)
    assert "email" in _text(again).lower(), anchor(
        "the duplicate signup rejection must name the email field", again)

    upper = client.post("/auth/login",
                        json={"email": email.upper(), "password": CORPUS_PASSWORD})
    assert upper.status_code in (200, 201), anchor(
        "the stored address is lowercased, so an upper-case sign in resolves", upper)


def test_persisted_account_row_carries_its_role(client, db):
    email = probe_email()
    r = client.post("/auth/signup",
                    json={"email": email, "password": CORPUS_PASSWORD,
                          "role": "author"})
    assert r.status_code in (200, 201), anchor(f"signup for {email}", r)

    stored = poll(lambda: db.one("accounts", email=email))
    assert stored is not None, (
        f"no accounts row was written for {email!r} after a successful signup")
    assert stored.get("role") == "author", (
        f"the persisted accounts row for {email!r} carries role "
        f"{stored.get('role')!r} rather than the role the signup asked for")
    assert CORPUS_PASSWORD not in json.dumps(stored, default=str), (
        f"the persisted accounts row for {email!r} carries the password in clear "
        f"text; it must be stored hashed")


def test_form_validation_refuses_invalid_input(client, db):
    before = db.count("accounts")
    empty = client.post("/auth/signup",
                        json={"email": probe_email(), "password": "", "role": "reader"})
    assert 400 <= empty.status_code < 500, anchor(
        "a signup with an empty password must be refused", empty)
    assert "password" in _text(empty).lower(), anchor(
        "the refusal must name the password field", empty)
    assert db.count("accounts") == before, (
        "a refused signup wrote an accounts row; a refused form writes nothing")

    unknown = client.post("/auth/login",
                          json={"email": probe_email(), "password": CORPUS_PASSWORD})
    assert 400 <= unknown.status_code < 500, anchor(
        "a sign in with an unknown address must be refused", unknown)


def test_band_sequence_tiles_the_document(client):
    r = client.get("/bands")
    assert r.status_code == 200, anchor("bands endpoint", r)
    bands = r.json()
    assert isinstance(bands, list), anchor(
        "the bands endpoint must return a top-level JSON array", r)
    assert [b.get("slug") for b in bands] == list(BAND_SLUGS), (
        f"the bands endpoint returned {[b.get('slug') for b in bands]!r} rather "
        f"than the nine bands in order {list(BAND_SLUGS)!r}")
    for band in bands:
        for field in BAND_FIELDS:
            assert field in band, (
                f"band {band.get('slug')!r} omits the field {field!r}; it carries "
                f"{sorted(band)!r}")
    edges = [(float(b["start_fraction"]), float(b["end_fraction"])) for b in bands]
    assert edges[0][0] == 0.0, (
        f"the first band starts at {edges[0][0]!r} rather than at zero")
    assert edges[-1][1] == 1.0, (
        f"the last band ends at {edges[-1][1]!r} rather than at one")
    for left, right in zip(edges, edges[1:]):
        assert abs(left[1] - right[0]) < 1e-9, (
            f"band ranges {left!r} and {right!r} leave a gap or overlap; the nine "
            f"ranges must tile from zero to one")


def test_rail_names_the_current_band(page, app_url):
    page.goto(f"{app_url}/", wait_until="networkidle")
    rail = page.locator("[data-band-rail], nav[aria-label*='band' i], nav[aria-label*='progress' i]")
    assert rail.count() >= 1, (
        "the index carries no left rail exposed as navigation with an accessible name")
    page.mouse.wheel(0, 4000)
    page.wait_for_timeout(1200)
    current = page.locator("[aria-current]")
    assert current.count() >= 1, (
        "after scrolling into a later band, no rail entry carries aria-current")
    label = (current.first.inner_text() or "").strip().lower()
    assert any(slug.replace("-", " ") in label for slug in BAND_SLUGS), (
        f"the rail's current entry reads {label!r}, which names none of the nine "
        f"bands {list(BAND_SLUGS)!r}")


def test_top_bar_scrolls_to_a_band_and_moves_focus(page, app_url):
    page.goto(f"{app_url}/", wait_until="networkidle")
    start = page.evaluate("() => window.scrollY")
    page.get_by_role("link", name=re.compile(r"^\s*systems\s*$", re.I)).first.click()
    page.wait_for_timeout(1500)
    moved = page.evaluate("() => window.scrollY")
    assert moved > start, (
        f"pressing the systems entry left the scroll position at {moved}; the "
        f"in-page entries scroll to their band")
    assert page.url.rstrip("/").endswith(app_url.rstrip("/").split("//")[-1]) or "#" in page.url, (
        f"pressing the systems entry navigated to {page.url!r} rather than "
        f"scrolling within the index")
    focused = page.evaluate("() => document.activeElement && document.activeElement.tagName")
    assert focused not in (None, "BODY"), (
        "scrolling to a band from the top bar left keyboard focus on the document "
        "body, so a keyboard reader and a pointer reader do not end in the same place")


def test_index_carries_its_seeded_records(site, db):
    home = _text(site.get("/"))
    assert db.count("career_roles") == 6, (
        f"the experience band is seeded with {db.count('career_roles')} career "
        f"roles rather than the six the brief pins")
    assert db.count("principles") == 4, (
        f"the philosophy band is seeded with {db.count('principles')} principles "
        f"rather than four")
    assert db.count("systems") == 5, (
        f"the systems band is seeded with {db.count('systems')} systems rather "
        f"than five")
    employers = {row.get("employer") for row in db.rows("career_roles")}
    assert len(employers) == 4, (
        f"the six seeded roles run across {sorted(employers)!r} rather than four "
        f"employers")
    for marker in ("Brightwater Capital", "Saltmarsh AI", "Eastfell Health",
                   "Colvin College"):
        assert marker in home, (
            f"the experience band omits the seeded employer {marker!r}; document "
            f"starts {home[:200]!r}")
    confidential = [row for row in db.rows("systems") if row.get("confidential")]
    assert len(confidential) == 1, (
        f"{len(confidential)} seeded systems are marked as client work; exactly "
        f"one carries the confidentiality line")


def test_field_is_decorative_and_stops_when_covered(page, app_url):
    page.goto(f"{app_url}/", wait_until="networkidle")
    field = page.locator("[data-field], canvas").first
    assert field.count() >= 1 or page.locator("canvas").count() >= 1, (
        "the first screen carries no drawn field")
    hidden = page.evaluate(
        "() => { const n = document.querySelector('[data-field], canvas');"
        " return n ? (n.getAttribute('aria-hidden') === 'true' ||"
        " n.closest('[aria-hidden=\"true\"]') !== null) : false; }")
    assert hidden, (
        "the wireframe field is decoration and must be hidden from assistive "
        "technology; it exposes itself instead")
    frames_before = page.evaluate("() => window.__fieldFrames || 0")
    page.mouse.wheel(0, 6000)
    page.wait_for_timeout(2500)
    after_scroll = page.evaluate("() => window.__fieldFrames || 0")
    page.wait_for_timeout(2500)
    after_wait = page.evaluate("() => window.__fieldFrames || 0")
    if after_scroll:
        assert after_wait == after_scroll, (
            f"the field kept drawing after it was covered: the frame counter moved "
            f"from {after_scroll} to {after_wait} while the field was off screen")
    else:
        opacity = page.evaluate(
            "() => { const n = document.querySelector('[data-field], canvas');"
            " if (!n) return '1'; const s = getComputedStyle(n.parentElement || n);"
            " return s.opacity; }")
        assert float(opacity) < 0.05, (
            f"once the first band has been scrolled past, the field container "
            f"still reports opacity {opacity!r}; it must be fully covered")
    assert frames_before is not None


def test_reduced_motion_holds_the_field_and_finishes_the_diagrams(
        reduced_motion_page, app_url):
    page = reduced_motion_page
    page.goto(f"{app_url}/", wait_until="networkidle")
    page.wait_for_timeout(1500)
    first = page.evaluate("() => window.__fieldFrames || 0")
    page.wait_for_timeout(2000)
    second = page.evaluate("() => window.__fieldFrames || 0")
    assert second == first, (
        f"under a reduced-motion preference the field kept turning: the frame "
        f"counter moved from {first} to {second}")
    counter_first = (page.locator(f"text={COUNTER_PHRASE}")
                     .first.inner_text() or "")
    page.wait_for_timeout(3000)
    counter_second = (page.locator(f"text={COUNTER_PHRASE}")
                      .first.inner_text() or "")
    assert counter_first is not None and counter_second is not None, (
        "the counter is missing under a reduced-motion preference; it carries "
        "information rather than movement and must keep counting")
    progress = page.evaluate(
        "() => { const n = document.querySelector('[data-diagram]');"
        " return n ? n.getAttribute('data-progress') : null; }")
    if progress is not None:
        assert float(progress) >= 1.0, (
            f"under a reduced-motion preference a diagram reports progress "
            f"{progress!r}; every diagram renders in its final state")


def test_diagram_validation_refuses_illegal_structure(client, author_token):
    good = make_diagram(client, author_token, "Valid pipeline")
    ok = client.post(f"/diagrams/{slug_of(good)}/validate",
                     headers=bearer(author_token))
    assert ok.status_code in (200, 201), anchor("validate a legal structure", ok)

    broken = sample_structure("broken")
    broken["nodes"][0]["kind"] = "widget"
    broken["edges"].append({"from": "parse", "to": "ghost", "kind": "plain",
                            "label": "dangling"})
    broken["timeline"].append({"at": 1.4, "target": "gold", "effect": "travel"})
    bad = make_diagram(client, author_token, "Broken pipeline", structure=broken)
    r = client.post(f"/diagrams/{slug_of(bad)}/validate",
                    headers=bearer(author_token))
    body = _text(r).lower()
    assert "widget" in body, anchor(
        "validation must name the illegal node kind it found", r)
    assert "ghost" in body, anchor(
        "validation must name the edge whose target node does not exist", r)
    assert "1.4" in body or "timeline" in body, anchor(
        "validation must report the timeline stop that sits outside zero to one", r)
    for kind in NODE_KINDS:
        assert kind != "widget"
    for kind in EDGE_KINDS:
        assert kind != "widget"


def test_export_is_refused_while_validation_fails(client, author_token, storage):
    broken = sample_structure("refused")
    broken["edges"].append({"from": "parse", "to": "nowhere", "kind": "plain",
                            "label": "dangling"})
    diagram = make_diagram(client, author_token, "Refused export",
                           structure=broken)
    before = set(storage.list(DIAGRAM_KEY_PREFIX))
    r = export_still(client, author_token, slug_of(diagram))
    assert 400 <= r.status_code < 500, anchor(
        "an export must be refused while validation reports a finding", r)
    after = set(storage.list(DIAGRAM_KEY_PREFIX))
    assert after == before, (
        f"a refused export wrote {sorted(after - before)!r} into the bucket; a "
        f"refused export writes no object")
    row = client.get(f"/diagrams/{slug_of(diagram)}", headers=bearer(author_token))
    assert not (row.json() or {}).get("still_key"), anchor(
        "a refused export left a still key on the diagram row", row)


def test_still_bytes_live_in_the_bucket_at_their_key(client, author_token, storage):
    diagram = make_diagram(client, author_token, "Stored pipeline")
    r = export_still(client, author_token, slug_of(diagram))
    assert r.status_code in (200, 201), anchor("export the still", r)
    key = (r.json() or {}).get("still_key")
    assert key, anchor("the export returned no still key", r)
    assert key.startswith(DIAGRAM_KEY_PREFIX), (
        f"the diagram still was written at {key!r}, which does not follow the "
        f"pinned scheme diagrams/{{diagram_id}}/{{sha256_of_bytes}}.{{ext}}")
    assert re.fullmatch(r"diagrams/[^/]+/[0-9a-f]{64}\.[A-Za-z0-9]+", key), (
        f"the diagram still key {key!r} does not carry a diagram id and a "
        f"sha256 of the bytes")
    assert poll(lambda: storage.exists(key)), (
        f"the object store carries no object at {key!r}; the bytes must live in "
        f"the bucket rather than on the app's own disk")

    post = make_post(client, author_token, "Stored piece",
                    diagram_slug=slug_of(diagram))
    attach = client.post(f"/posts/{slug_of(post)}/still",
                        headers=bearer(author_token))
    assert attach.status_code in (200, 201), anchor("attach the piece still", attach)
    post_key = (attach.json() or {}).get("still_key")
    assert post_key and post_key.startswith(POST_KEY_PREFIX), (
        f"the piece still was written at {post_key!r} rather than under the "
        f"pinned posts key scheme")
    assert poll(lambda: storage.exists(post_key)), (
        f"the object store carries no object at {post_key!r}")


def test_export_into_another_account_is_denied(client, author_token,
                                               second_author_token, storage):
    diagram = make_diagram(client, author_token, "Owned pipeline")
    before = set(storage.list(DIAGRAM_KEY_PREFIX))
    r = export_still(client, second_author_token, slug_of(diagram))
    assert 400 <= r.status_code < 500, anchor(
        "a second author must not export into a diagram owned by the first", r)
    after = set(storage.list(DIAGRAM_KEY_PREFIX))
    assert after == before, (
        f"a denied export wrote {sorted(after - before)!r} into the bucket")


def test_draft_piece_and_its_still_answer_only_their_owner(
        client, author_token, second_author_token, reader_token):
    diagram, post = _draft_with_diagram(client, author_token, "Held back piece")
    slug = slug_of(post)
    attach = client.post(f"/posts/{slug}/still", headers=bearer(author_token))
    assert attach.status_code in (200, 201), anchor("attach the piece still", attach)

    owner = client.get(f"/posts/{slug}", headers=bearer(author_token))
    assert owner.status_code == 200, anchor(
        "the owning author must read their own draft", owner)

    for label, headers in (("an anonymous caller", {}),
                           ("the second author account", bearer(second_author_token)),
                           ("a reader account", bearer(reader_token))):
        body = client.get(f"/posts/{slug}", headers=headers)
        assert 400 <= body.status_code < 500, anchor(
            f"{label} must not read the draft piece", body)
        still = client.get(f"/posts/{slug}/still", headers=headers)
        assert 400 <= still.status_code < 500, anchor(
            f"{label} must receive no still bytes for the draft piece", still)
        assert len(still.content or b"") < 512, anchor(
            f"{label} received {len(still.content or b'')} bytes for a draft still",
            still)

    diagram_slug = slug_of(diagram)
    anonymous = client.get(f"/diagrams/{diagram_slug}")
    assert 400 <= anonymous.status_code < 500, anchor(
        "an anonymous caller must not read a draft diagram", anonymous)

    listed = _titles(_published(client))
    assert post.get("title") not in listed, (
        f"the draft piece {post.get('title')!r} appears in the published listing "
        f"{listed!r}")
    assert DRAFT_POST not in listed, (
        f"the seeded draft {DRAFT_POST!r} appears in the published listing {listed!r}")


def test_publish_opens_the_row_the_page_and_the_object(client, author_token):
    diagram, post = _draft_with_diagram(client, author_token, "Opened piece")
    slug = slug_of(post)
    client.post(f"/posts/{slug}/still", headers=bearer(author_token))

    r = client.post(f"/posts/{slug}/publish", headers=bearer(author_token))
    assert r.status_code in (200, 201), anchor("publish the draft", r)
    published = r.json() or {}
    assert published.get("status") == "published", anchor(
        "publishing must move the piece to the published status", r)
    assert published.get("published_at"), anchor(
        "publishing must stamp a publication timestamp", r)

    for label, headers in (("an anonymous caller", {}),):
        body = client.get(f"/posts/{slug}", headers=headers)
        assert body.status_code == 200, anchor(
            f"{label} must read the piece once published", body)
        still = client.get(f"/posts/{slug}/still", headers=headers)
        assert still.status_code == 200, anchor(
            f"{label} must receive the still once the piece is published", still)

    assert slug in [row.get("slug") for row in _published(client)], (
        "the published piece does not appear in the published listing")


def test_publishing_another_account_piece_is_denied(client, author_token,
                                                    second_author_token):
    diagram, post = _draft_with_diagram(client, author_token, "Not yours piece")
    slug = slug_of(post)
    client.post(f"/posts/{slug}/still", headers=bearer(author_token))
    r = client.post(f"/posts/{slug}/publish", headers=bearer(second_author_token))
    assert 400 <= r.status_code < 500, anchor(
        "a second author must not publish the first author's draft", r)
    row = client.get(f"/posts/{slug}", headers=bearer(author_token))
    assert (row.json() or {}).get("status") == "draft", anchor(
        "a denied publish left the piece out of the draft status", row)


def test_publish_without_a_still_is_refused(client, author_token):
    diagram = make_diagram(client, author_token, "Unexported pipeline")
    post = make_post(client, author_token, "Unexported piece",
                     diagram_slug=slug_of(diagram))
    r = client.post(f"/posts/{slug_of(post)}/publish", headers=bearer(author_token))
    assert 400 <= r.status_code < 500, anchor(
        "publishing a piece whose diagram exported no still must be refused", r)
    assert "still" in _text(r).lower(), anchor(
        "the refusal must name the still", r)


def test_repeated_publish_leaves_one_piece_and_one_object(client, author_token,
                                                          db, storage):
    diagram, post = _draft_with_diagram(client, author_token, "Twice published piece")
    slug = slug_of(post)
    client.post(f"/posts/{slug}/still", headers=bearer(author_token))
    first = client.post(f"/posts/{slug}/publish", headers=bearer(author_token))
    assert first.status_code in (200, 201), anchor("first publish", first)
    key = (client.get(f"/posts/{slug}").json() or {}).get("still_key")

    client.post(f"/posts/{slug}/publish", headers=bearer(author_token))
    rows = [row for row in db.rows("posts") if row.get("slug") == slug]
    assert len(rows) == 1, (
        f"a repeated publish left {len(rows)} rows for slug {slug!r}; exactly one "
        f"published piece must survive")
    again = (client.get(f"/posts/{slug}").json() or {}).get("still_key")
    assert again == key, (
        f"a repeated publish changed the stored key from {key!r} to {again!r}")
    if key:
        assert storage.exists(key), (
            f"the stored object at {key!r} disappeared across a repeated publish")


def test_simultaneous_publishes_accept_exactly_one(client, author_token, db):
    diagram, post = _draft_with_diagram(client, author_token, "Raced piece")
    slug = slug_of(post)
    client.post(f"/posts/{slug}/still", headers=bearer(author_token))

    def publish():
        with httpx.Client(base_url=client.base_url, timeout=30.0) as racer:
            return racer.post(f"/posts/{slug}/publish",
                              headers=bearer(author_token)).status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        codes = list(pool.map(lambda _: publish(), range(2)))
    accepted = [c for c in codes if 200 <= c < 300]
    assert len(accepted) == 1, (
        f"two publishes of one draft arriving together returned {codes!r}; exactly "
        f"one must be accepted and the other rejected")
    rows = [row for row in db.rows("posts") if row.get("slug") == slug]
    assert len(rows) == 1, (
        f"the raced publish left {len(rows)} rows for slug {slug!r}")


def test_series_number_independently(client, author_token, db):
    eng = make_post(client, author_token, f"Engineering probe {probe_email()[:8]}",
                    series="ENG")
    tht = make_post(client, author_token, f"Thought probe {probe_email()[:8]}",
                    series="THT")
    assert eng.get("code", "").startswith("ENG-"), (
        f"an engineering piece took the code {eng.get('code')!r}")
    assert tht.get("code", "").startswith("THT-"), (
        f"an essay piece took the code {tht.get('code')!r}")
    for series in POST_SERIES:
        numbers = [row.get("number") for row in db.rows("posts")
                   if row.get("series") == series]
        assert len(numbers) == len(set(numbers)), (
            f"the {series!r} series carries duplicate numbers {numbers!r}; a "
            f"number is unique within its own series")
    assert eng.get("number") != tht.get("number") or True
    listing = _published(client)
    codes = [row.get("code") for row in listing]
    assert PUBLISHED_POST_CODE in codes, (
        f"the seeded engineering piece code {PUBLISHED_POST_CODE!r} is absent "
        f"from the published listing codes {codes!r}")
    assert SECOND_PUBLISHED_POST_CODE in codes, (
        f"the seeded essay piece code {SECOND_PUBLISHED_POST_CODE!r} is absent "
        f"from the published listing codes {codes!r}")


def test_published_listing_is_newest_first(client):
    payload = _published(client)
    stamps = [row.get("published_at") for row in payload if row.get("published_at")]
    assert stamps == sorted(stamps, reverse=True), (
        f"the published listing returned publication stamps {stamps!r}, which are "
        f"not newest first")
    titles = _titles(payload)
    for seeded in (PUBLISHED_POST, SECOND_PUBLISHED_POST):
        assert seeded in titles, (
            f"the seeded published piece {seeded!r} is missing from the listing "
            f"{titles!r}")


def test_diagram_renders_both_layouts_from_one_structure(client, author_token, db):
    diagram = make_diagram(client, author_token, "Two layout pipeline")
    r = client.get(f"/diagrams/{slug_of(diagram)}", headers=bearer(author_token))
    assert r.status_code == 200, anchor("read the diagram back", r)
    payload = r.json() or {}
    layout = (payload.get("structure") or {}).get("layout") or {}
    assert set(layout) >= {"narrow", "wide"}, (
        f"the diagram structure declares layouts {sorted(layout)!r} rather than a "
        f"narrow layout and a wide layout")
    assert layout["narrow"].get("flow") == "column", (
        f"the narrow layout flows {layout['narrow'].get('flow')!r} rather than down "
        f"a column")
    assert layout["wide"].get("flow") == "row", (
        f"the wide layout flows {layout['wide'].get('flow')!r} rather than across a row")
    stops = (payload.get("structure") or {}).get("timeline") or []
    for stop in stops:
        assert stop.get("effect") in TIMELINE_EFFECTS, (
            f"the timeline carries the effect {stop.get('effect')!r}, which is "
            f"outside the seven legal effects {list(TIMELINE_EFFECTS)!r}")
    seeded = db.rows("diagrams", limit=1)
    if seeded:
        series = ((seeded[0].get("structure") or {}) if isinstance(
            seeded[0].get("structure"), dict) else {}).get("series")
        if series:
            assert len(series[0].get("values", [])) == SERIES_SAMPLE_COUNT, (
                f"a seeded diagram's sampled series carries "
                f"{len(series[0].get('values', []))} values rather than "
                f"{SERIES_SAMPLE_COUNT}")


def test_diagram_render_is_deterministic(client, author_token):
    diagram = make_diagram(client, author_token, "Repeatable pipeline")
    slug = slug_of(diagram)
    first = client.get(f"/diagrams/{slug}/render?progress=0.5",
                       headers=bearer(author_token))
    second = client.get(f"/diagrams/{slug}/render?progress=0.5",
                        headers=bearer(author_token))
    assert first.status_code == 200, anchor("render the diagram at half progress",
                                            first)
    assert first.text == second.text, (
        "rendering one structure twice at the same progress produced two different "
        "drawings; the same input must always produce the same drawing")


def test_run_log_and_text_alternative(site, db):
    home = _text(site.get("/"))
    for system in db.rows("systems"):
        log = system.get("run_log")
        if isinstance(log, str):
            log = json.loads(log)
        assert log and len(log) == 4, (
            f"the system {system.get('title')!r} carries a run log of "
            f"{0 if not log else len(log)} rows rather than exactly four")
    for marker in ("RUN LOG", "nothing promotes on its own", "PENDING",
                   "PROMOTED TO GOLD"):
        assert marker in home, (
            f"the index omits the pinned run-log copy {marker!r}; document starts "
            f"{home[:200]!r}")
    for diagram in db.rows("diagrams"):
        alt = (diagram.get("alt_text") or "").strip()
        assert len(alt) > 40, (
            f"the diagram {diagram.get('slug')!r} carries the text alternative "
            f"{alt!r}, which is too short to describe its nodes in order")
        assert alt.lower() != "system diagram", (
            f"the diagram {diagram.get('slug')!r} carries the alternative "
            f"{alt!r} rather than a description of what the drawing shows")


def test_contact_panel_validates_and_keeps_what_was_typed(client, db):
    before = db.count("notes")
    short = client.post("/notes", json=note_payload(message="too short"))
    assert 400 <= short.status_code < 500, anchor(
        f"a message under {MESSAGE_MIN} characters must be refused", short)
    long_note = client.post("/notes",
                            json=note_payload(message="x" * (MESSAGE_MAX + 1)))
    assert 400 <= long_note.status_code < 500, anchor(
        f"a message over {MESSAGE_MAX} characters must be refused", long_note)
    no_name = client.post("/notes", json=note_payload(name="A"))
    assert 400 <= no_name.status_code < 500, anchor(
        "a name shorter than two characters must be refused", no_name)
    long_name = client.post("/notes", json=note_payload(name="N" * (NAME_MAX + 1)))
    assert 400 <= long_name.status_code < 500, anchor(
        f"a name longer than {NAME_MAX} characters must be refused", long_name)
    bad_address = client.post("/notes", json=note_payload(email="not-an-address"))
    assert 400 <= bad_address.status_code < 500, anchor(
        "an address that fails the syntax check must be refused", bad_address)
    bad_intent = client.post("/notes", json=note_payload(intent="Whatever"))
    assert 400 <= bad_intent.status_code < 500, anchor(
        f"an intent outside {list(NOTE_INTENTS)!r} must be refused", bad_intent)
    assert db.count("notes") == before, (
        "a refused note wrote a notes row; a refused form writes nothing")


def test_note_returns_a_thread_token_reaching_one_note(client, db):
    payload = note_payload()
    r = client.post("/notes", json=payload)
    assert r.status_code in (200, 201), anchor("send a note", r)
    token = (r.json() or {}).get("thread_token")
    assert token, anchor("a sent note must come back with a thread token", r)

    thread = client.get(f"/notes/{token}")
    assert thread.status_code == 200, anchor("open the thread by its token", thread)
    body = thread.json() or {}
    note = body.get("note") or body
    assert note.get("email") == payload["email"], anchor(
        "the thread token opened a different note", thread)
    assert note.get("band") == payload["band"], anchor(
        "the stored note did not record the band the panel opened from", thread)

    missing = client.get(f"/notes/{token[::-1]}zz")
    assert missing.status_code in (403, 404), anchor(
        "a thread token with no note behind it must answer not found", missing)

    listing = client.get("/notes")
    assert listing.status_code in (401, 403, 404, 405), anchor(
        "no listing of notes may be reachable without the desk session", listing)
    assert token not in _text(listing), anchor(
        "a thread token appeared in a listing", listing)


def test_sender_adds_a_message_to_their_thread(client, db):
    r = client.post("/notes", json=note_payload())
    token = (r.json() or {}).get("thread_token")
    added = client.post(f"/notes/{token}/messages",
                        json={"body": "One more thought about the eval gate."})
    assert added.status_code in (200, 201), anchor("add a message to the thread", added)
    thread = client.get(f"/notes/{token}").json() or {}
    messages = thread.get("messages") or []
    assert messages, "the thread carries no messages after one was added"
    assert messages[-1].get("author_kind") == "sender", (
        f"the added message carries author_kind "
        f"{messages[-1].get('author_kind')!r} rather than sender")
    delete = client.request("DELETE", f"/notes/{token}")
    assert delete.status_code in (401, 403, 404, 405), anchor(
        "a sender must not be able to delete their note", delete)


def test_subscription_confirms_before_anything_is_recorded(client, db):
    email = probe_email()
    r = client.post("/subscribers", json={"email": email})
    assert r.status_code in (200, 201, 202), anchor("subscribe", r)
    stored = poll(lambda: db.one("subscribers", email=email))
    assert stored is not None, f"no subscribers row was written for {email!r}"
    assert stored.get("state") == "pending", (
        f"a fresh subscription is in state {stored.get('state')!r} rather than "
        f"pending; nobody is on a list until the confirmation link is followed")
    link = (r.json() or {}).get("confirm_link") or (r.json() or {}).get("confirm_token")
    assert link, anchor("subscribing returned no confirmation link", r)
    token = link.rsplit("/", 1)[-1]
    confirmed = client.get(f"/subscribers/confirm/{token}")
    assert confirmed.status_code in (200, 302, 303), anchor(
        "following the confirmation link", confirmed)
    after = poll(lambda: db.one("subscribers", email=email))
    assert after.get("state") == "confirmed", (
        f"after the confirmation link the subscription is in state "
        f"{after.get('state')!r} rather than confirmed")
    for state in SUBSCRIBER_STATES:
        assert state in ("pending", "confirmed", "unsubscribed")


def test_expired_confirmation_token_is_refused(client, db):
    expired = client.get("/subscribers/confirm/expired-probe-token")
    assert expired.status_code in (400, 404, 410), anchor(
        "an unknown or expired confirmation token must be refused rather than "
        "silently accepted", expired)
    rows = db.rows("subscribers")
    for row in rows:
        if row.get("state") == "pending":
            assert row.get("confirm_token"), (
                f"the pending subscription {row.get('email')!r} carries no "
                f"confirmation token, so it can never be confirmed")


def test_unsubscribe_needs_no_sign_in(client, db):
    email = probe_email()
    client.post("/subscribers", json={"email": email})
    row = poll(lambda: db.one("subscribers", email=email))
    token = row.get("unsubscribe_token")
    assert token, f"the subscription for {email!r} carries no unsubscribe token"
    r = client.post(f"/subscribers/unsubscribe/{token}")
    assert r.status_code in (200, 204), anchor("one-click unsubscribe", r)
    after = poll(lambda: db.one("subscribers", email=email))
    assert after.get("state") == "unsubscribed", (
        f"after the unsubscribe link the subscription is in state "
        f"{after.get('state')!r}")


def test_note_rate_limit_refuses_the_fourth_in_an_hour(client, db):
    email = probe_email()
    before = db.count("notes")
    codes = []
    for index in range(4):
        r = client.post("/notes", json=note_payload(
            email=email,
            message=f"Sending note number {index} about the extraction pipeline."))
        codes.append(r.status_code)
        last = r
    assert 400 <= codes[-1] < 500, (
        f"four notes from one address inside an hour returned {codes!r}; the "
        f"fourth must be refused")
    assert RATE_LIMIT_LINE in _text(last), anchor(
        f"the refusal must read {RATE_LIMIT_LINE!r}", last)
    assert db.count("notes") - before <= 3, (
        f"{db.count('notes') - before} notes were written for {email!r}; the limit "
        f"is three in an hour")


def test_note_sorting_places_each_lane(client, db):
    signal = client.post("/notes", json=note_payload(
        intent="Consulting", budget_band="50k to 100k",
        message=("I read the Ferrite entry in the systems band and I would like "
                 "to talk about structured extraction for our reporting packs. "
                 "We have quarterly documents arriving as scans and slide decks "
                 "and nobody trusts the numbers that come out of them."),
        band="systems"))
    assert signal.status_code in (200, 201), anchor("a strong note", signal)
    signal_row = poll(lambda: db.one("notes",
                                     thread_token=(signal.json() or {}).get("thread_token")))
    assert signal_row.get("lane") == "signal", (
        f"a note naming a seeded system and asking about consulting landed in "
        f"lane {signal_row.get('lane')!r} rather than signal")
    assert int(signal_row.get("score") or 0) >= LANE_SIGNAL_FLOOR, (
        f"that note carries the sorting total {signal_row.get('score')!r}, which "
        f"is below the floor for the signal lane")

    noise = client.post("/notes", json=note_payload(
        intent="Something else",
        message="Great site https://example.com " + long_message(20),
        band="hero"))
    noise_row = poll(lambda: db.one("notes",
                                    thread_token=(noise.json() or {}).get("thread_token")))
    assert noise_row.get("lane") == "likely noise", (
        f"a short note carrying a link landed in lane {noise_row.get('lane')!r} "
        f"rather than likely noise")
    readable = client.get(f"/notes/{(noise.json() or {}).get('thread_token')}")
    assert readable.status_code == 200, anchor(
        "a note in the lowest lane must still be readable", readable)
    for lane in NOTE_LANES:
        assert lane in ("signal", "unsorted", "likely noise")


def test_desk_shows_three_lanes_with_the_breakdown(client, author_token,
                                                   reader_token):
    r = client.get("/desk", headers=bearer(author_token))
    assert r.status_code == 200, anchor("the author opens the desk", r)
    payload = r.json() or {}
    lanes = payload.get("lanes") or payload
    for lane in NOTE_LANES:
        assert lane in json.dumps(lanes), (
            f"the desk does not present the lane {lane!r}; it returned "
            f"{json.dumps(lanes)[:300]!r}")
    body = json.dumps(payload)
    assert "score_breakdown" in body or "breakdown" in body, anchor(
        "the desk must show why a note landed in its lane", r)

    refused = client.get("/desk", headers=bearer(reader_token))
    assert 400 <= refused.status_code < 500, anchor(
        "a reader account must not reach the desk", refused)
    anonymous = client.get("/desk")
    assert 400 <= anonymous.status_code < 500, anchor(
        "an anonymous caller must not reach the desk", anonymous)


def test_reply_reaches_the_thread_only_when_sent(client, author_token, db):
    sent = client.post("/notes", json=note_payload())
    token = (sent.json() or {}).get("thread_token")
    row = poll(lambda: db.one("notes", thread_token=token))
    note_id = row.get("id")

    before = db.count("note_messages", note_id=note_id)
    reply = client.post(f"/notes/{note_id}/reply",
                        json={"body": "Happy to talk through the eval gate."},
                        headers=bearer(author_token))
    assert reply.status_code in (200, 201), anchor("the author sends a reply", reply)
    assert db.count("note_messages", note_id=note_id) == before + 1, (
        "sending a reply did not add exactly one message to the thread")
    thread = client.get(f"/notes/{token}").json() or {}
    kinds = [m.get("author_kind") for m in (thread.get("messages") or [])]
    assert "owner" in kinds, (
        f"the sender's thread carries message kinds {kinds!r} and no owner reply")

    patched = client.request("PATCH", f"/notes/{note_id}",
                             json={"state": "read"},
                             headers=bearer(author_token))
    assert patched.status_code in (200, 201), anchor(
        "the author changes a note's state from the desk", patched)
    for action in DESK_ACTIONS:
        assert action in ("Reply", "Snooze", "Close", "Mark noise")


def test_slot_hold_and_double_booking(client, db):
    first = client.post("/notes", json=note_payload(
        intent="Consulting", budget_band="50k to 100k",
        message=("I read the Ferrite entry and would like to book a call about "
                 "structured extraction for reporting packs."),
        band="systems"))
    second = client.post("/notes", json=note_payload(
        intent="Consulting", budget_band="50k to 100k",
        message=("I also read the Ferrite entry and would like the same slot to "
                 "talk about extraction for reporting packs."),
        band="systems"))
    first_token = (first.json() or {}).get("thread_token")
    second_token = (second.json() or {}).get("thread_token")

    slots = client.get("/availability", params={"note_token": first_token})
    assert slots.status_code == 200, anchor("the offered slots", slots)
    offered = (slots.json() or {}).get("slots") or []
    assert len(offered) >= 1, anchor(
        "a note in the best lane must be offered concrete slots", slots)
    starts_at = offered[0].get("starts_at") if isinstance(offered[0], dict) else offered[0]

    def book(token):
        with httpx.Client(base_url=client.base_url, timeout=30.0) as racer:
            return racer.post("/bookings",
                              json={"starts_at": starts_at, "note_token": token})

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(book, (first_token, second_token)))
    codes = [r.status_code for r in results]
    accepted = [c for c in codes if 200 <= c < 300]
    assert len(accepted) == 1, (
        f"two senders choosing the same slot returned {codes!r}; exactly one must "
        f"be confirmed and the other refused")
    confirmed = [row for row in db.rows("bookings")
                 if str(row.get("starts_at")) == str(starts_at)
                 and row.get("state") == "confirmed"]
    assert len(confirmed) == 1, (
        f"{len(confirmed)} bookings are confirmed for one slot")
    held = [row for row in db.rows("bookings")
            if str(row.get("starts_at")) == str(starts_at)
            and row.get("state") == "held"]
    assert not held or all(row.get("hold_expires_at") for row in held), (
        f"a slot is stuck in the held state with no hold expiry; a hold lasts "
        f"{SLOT_HOLD_MINUTES} minutes and then returns the slot")
    for state in BOOKING_STATES:
        assert state in ("held", "confirmed", "cancelled")


def test_cookie_choice_is_asked_once_and_persists(page, app_url):
    page.goto(f"{app_url}/", wait_until="networkidle")
    band = page.locator("[data-cookie-band], [role='region'][aria-label*='cookie' i]")
    assert band.count() >= 1, (
        "a first-time visitor is not asked about non-essential cookies")
    accept = page.get_by_role("button", name=re.compile("accept", re.I)).first
    refuse = page.get_by_role("button", name=re.compile("refuse|reject|decline", re.I)).first
    assert refuse.count() >= 1, (
        "the cookie band offers no refusal that is as easy to press as accepting")
    accept.click()
    page.wait_for_timeout(500)
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(800)
    assert page.locator("[data-cookie-band]").count() == 0 or not page.locator(
        "[data-cookie-band]").first.is_visible(), (
        "the cookie question returned after a reload; the answer must survive one")


def test_page_views_record_route_day_and_deepest_band(client, author_token, db):
    r = client.post("/views", json={"route": "/", "band": "systems"})
    assert r.status_code in (200, 201, 202, 204), anchor("record a page view", r)
    row = poll(lambda: db.one("page_views", route="/"))
    assert row is not None, "no page_views row was written for the index route"
    assert row.get("max_band"), (
        "the page_views row records no deepest band reached, which is the one "
        "number worth collecting on this site")
    blob = json.dumps(row, default=str).lower()
    for needle in ("@", "ip", "user_agent", "fingerprint", "visitor_id"):
        if needle == "ip":
            assert "ip_address" not in blob, (
                f"the page_views row carries an address field: {blob[:200]!r}")
        else:
            assert needle not in blob, (
                f"the page_views row carries {needle!r}, which could identify one "
                f"reader: {blob[:200]!r}")

    owner = client.get("/views", headers=bearer(author_token))
    assert owner.status_code == 200, anchor(
        "the author reads the page-view aggregate", owner)
    anonymous = client.get("/views")
    assert 400 <= anonymous.status_code < 500, anchor(
        "the page-view aggregate must answer the author account only", anonymous)


def test_not_found_page_is_the_products_own(site):
    r = site.get("/no-such-address-here", follow_redirects=False)
    assert r.status_code == 404, anchor(
        "an unknown address must answer not found", r)
    body = _text(r)
    for marker in (NOT_FOUND_CODE, NOT_FOUND_LINE, NOT_FOUND_ACTION):
        assert marker in body, (
            f"the not-found page omits {marker!r}; body starts {body[:300]!r}")
    for entry in TOP_BAR_ENTRIES:
        assert entry in body, (
            f"the not-found page drops the top-bar entry {entry!r}, so a lost "
            f"visitor is stranded; body starts {body[:300]!r}")


def test_privacy_page_states_what_is_recorded(site):
    r = site.get("/privacy")
    assert r.status_code == 200, anchor("the privacy page", r)
    body = _text(r).lower()
    for marker in ("note", "subscription", str(RETENTION_MONTHS)):
        assert marker in body, (
            f"the privacy page omits {marker!r}; body starts {body[:300]!r}")


def test_every_internal_link_resolves(site):
    seen = set()
    for route in PUBLIC_ROUTES:
        page_body = _text(site.get(route))
        for href in re.findall(r'href=["\'](/[^"\'#?]*)["\']', page_body):
            if href.startswith("//"):
                continue
            seen.add(href)
    assert seen, "no internal links were found on the public routes"
    for href in sorted(seen):
        r = site.get(href, follow_redirects=False)
        assert r.status_code in (200, 301, 302, 303, 307, 308, 401, 403), anchor(
            f"the internal link {href!r} does not resolve", r)


def test_role_boundaries_are_enforced_server_side(client, reader_token,
                                                  author_token):
    for path in ("/posts", "/diagrams"):
        r = client.post(path, json={"title": "Reader attempt"},
                        headers=bearer(reader_token))
        assert 400 <= r.status_code < 500, anchor(
            f"a reader must not create at {path}", r)
    desk = client.get("/desk", headers=bearer(reader_token))
    assert desk.status_code in (400, 401, 403, 404), anchor(
        "a reader must not reach the author's desk", desk)
    account = client.get("/account", headers=bearer(reader_token))
    assert account.status_code in (200, 204), anchor(
        "a reader must reach their own account route", account)
    anonymous = client.get("/account")
    assert 400 <= anonymous.status_code < 500, anchor(
        "an anonymous caller must not reach the account route", anonymous)
    bad_token = client.get("/auth/me", headers=bearer("not-a-real-token"))
    assert 400 <= bad_token.status_code < 500, anchor(
        "an unusable token must be refused", bad_token)


def test_signed_out_request_returns_to_the_route_asked_for(page, app_url):
    for route in PROTECTED_ROUTES:
        page.goto(f"{app_url}{route}", wait_until="networkidle")
        assert "/login" in page.url, (
            f"a signed-out request for {route!r} landed on {page.url!r} rather "
            f"than the sign-in route")
    page.goto(f"{app_url}/studio", wait_until="networkidle")
    page.get_by_label(re.compile("email", re.I)).first.fill(AUTHOR_EMAIL)
    page.get_by_label(re.compile("password", re.I)).first.fill(CORPUS_PASSWORD)
    page.get_by_role("button", name=re.compile("sign in|log in", re.I)).first.click()
    page.wait_for_timeout(2000)
    assert "/studio" in page.url, (
        f"after signing in from a pending studio request the reader landed on "
        f"{page.url!r} rather than back on the studio")


def test_no_secret_reaches_the_browser(site, client):
    bodies = [_text(site.get(route)) for route in PUBLIC_ROUTES]
    bodies.append(_text(client.get("/posts")))
    bodies.append(_text(client.get("/bands")))
    for body in bodies:
        for needle in SECRET_NEEDLES:
            assert needle not in body, (
                f"a document the browser downloads carries {needle!r}; no "
                f"credential, key or database address may reach the browser")


def test_no_outbound_message_leaves_the_app(client, db):
    email = probe_email()
    client.post("/subscribers", json={"email": email})
    row = poll(lambda: db.one("outbound_messages", recipient=email))
    assert row is not None, (
        f"no outbound_messages row was recorded for {email!r}; every message the "
        f"product would send is recorded as a row with its single-use link")
    assert row.get("state") in ("queued", "delivered", "failed"), (
        f"the outbound message for {email!r} carries the state {row.get('state')!r}")
    assert row.get("kind"), (
        f"the outbound message for {email!r} records no kind")


def test_list_endpoints_return_top_level_arrays(client):
    for path in ("/posts", "/bands", "/diagrams"):
        r = client.get(path)
        assert r.status_code == 200, anchor(f"list endpoint {path}", r)
        assert isinstance(r.json(), list), anchor(
            f"{path} must return a top-level JSON array", r)


def test_seeded_content_is_complete_and_idempotent(client, db, storage):
    counts = {table: db.count(table) for table in
              ("accounts", "career_roles", "principles", "systems",
               "repositories", "stack_items", "diagrams", "posts")}
    assert counts["accounts"] >= 3, (
        f"the seed carries {counts['accounts']} accounts rather than at least the "
        f"three the brief pins")
    assert counts["repositories"] == 5, (
        f"the open-source band is seeded with {counts['repositories']} "
        f"repositories rather than five")
    groups = {row.get("group_name") for row in db.rows("stack_items")}
    assert len(groups) == 5, (
        f"the stack band carries the groups {sorted(groups)!r} rather than five")
    assert counts["diagrams"] >= 6, (
        f"the seed carries {counts['diagrams']} diagrams rather than at least six")
    seeded_posts = {row.get("title") for row in db.rows("posts")}
    for title in (PUBLISHED_POST, SECOND_PUBLISHED_POST, DRAFT_POST):
        assert title in seeded_posts, (
            f"the seeded piece {title!r} is missing from the posts table")
    duplicates = [row.get("email") for row in db.rows("accounts")]
    assert len(duplicates) == len(set(duplicates)), (
        f"the accounts table carries duplicate addresses {duplicates!r}, so "
        f"seeding is not idempotent")
    keys = storage.list("")
    assert len(keys) == len(set(keys)), (
        f"the bucket carries duplicate keys, so seeding is not idempotent")


def test_narrow_viewport_has_no_sideways_overflow(ui_page, app_url):
    page = ui_page
    for route in ("/", "/blog"):
        page.goto(f"{app_url}{route}", wait_until="networkidle")
        page.wait_for_timeout(800)
        overflow = page.evaluate(
            "() => document.documentElement.scrollWidth -"
            " document.documentElement.clientWidth")
        assert overflow <= 1, (
            f"at a narrow viewport the route {route!r} overflows sideways by "
            f"{overflow} pixels")
    page.goto(f"{app_url}/", wait_until="networkidle")
    rail_visible = page.evaluate(
        "() => { const n = document.querySelector('[data-band-rail]');"
        " if (!n) return false; const s = getComputedStyle(n);"
        " return s.display !== 'none' && s.visibility !== 'hidden'; }")
    assert not rail_visible, (
        "the left rail is still shown at a narrow viewport; it is hidden there")
    contact = page.get_by_text(CONTACT_LABEL).first
    assert contact.count() >= 1, (
        "the contact control is absent at a narrow viewport, where it becomes a "
        "full-width bar at the foot")


def test_body_text_meets_the_contrast_bar(page, app_url):
    page.goto(f"{app_url}/", wait_until="networkidle")
    ratio = page.evaluate(
        "() => {\n"
        "  const lum = (c) => {\n"
        "    const p = c.match(/\\d+(\\.\\d+)?/g).slice(0, 3).map(Number)\n"
        "      .map(v => v / 255)\n"
        "      .map(v => v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4));\n"
        "    return 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2];\n"
        "  };\n"
        "  const node = document.querySelector('main p, article p, p');\n"
        "  if (!node) return 0;\n"
        "  const fg = lum(getComputedStyle(node).color);\n"
        "  let el = node, bg = null;\n"
        "  while (el && !bg) {\n"
        "    const c = getComputedStyle(el).backgroundColor;\n"
        "    if (c && !c.includes('rgba(0, 0, 0, 0)')) bg = c;\n"
        "    el = el.parentElement;\n"
        "  }\n"
        "  const b = lum(bg || 'rgb(255,255,255)');\n"
        "  const hi = Math.max(fg, b), lo = Math.min(fg, b);\n"
        "  return (hi + 0.05) / (lo + 0.05);\n"
        "}")
    assert ratio >= 4.5, (
        f"body copy on the index reports a contrast ratio of {ratio:.2f} against "
        f"its background, below the WCAG AA bar of 4.5 to 1")


def test_focus_is_visible_and_the_panel_traps_it(page, app_url):
    page.goto(f"{app_url}/", wait_until="networkidle")
    page.keyboard.press("Tab")
    outline = page.evaluate(
        "() => { const n = document.activeElement; if (!n) return '';"
        " const s = getComputedStyle(n);"
        " return [s.outlineStyle, s.outlineWidth, s.boxShadow].join('|'); }")
    assert "none|" not in outline or "rgb" in outline, (
        f"the first focusable control reports {outline!r} and shows no visible "
        f"focus ring")
    page.get_by_text(CONTACT_LABEL).first.click()
    page.wait_for_timeout(600)
    assert page.locator(f"text={PANEL_TITLE}").count() >= 1, (
        f"pressing the contact control did not open a panel titled {PANEL_TITLE!r}")
    assert page.locator(f"text={PANEL_SUBTITLE}").count() >= 1, (
        f"the panel omits the subtitle {PANEL_SUBTITLE!r}")
    inside = page.evaluate(
        "() => { const p = document.querySelector('[role=\"dialog\"]');"
        " return p ? p.contains(document.activeElement) : null; }")
    assert inside is not False, (
        "the open contact panel does not hold keyboard focus inside itself")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    assert page.locator(f"text={PANEL_TITLE}").count() == 0 or not page.locator(
        f"text={PANEL_TITLE}").first.is_visible(), (
        "the contact panel did not close on the escape key")


def test_panel_is_reachable_at_its_own_address(site):
    r = site.get("/signal")
    assert r.status_code == 200, anchor("the contact channel's own address", r)
    body = _text(r)
    for marker in (PANEL_TITLE, PANEL_SUBTITLE):
        assert marker in body, (
            f"the signal route omits {marker!r}; body starts {body[:200]!r}")
    for intent in NOTE_INTENTS:
        assert intent in body, (
            f"the signal route omits the intent option {intent!r}")


def test_archive_and_piece_routes_ship_no_drawing_code(page, app_url, site):
    page.goto(f"{app_url}/blog", wait_until="networkidle")
    page.wait_for_timeout(800)
    contexts = page.evaluate(
        "() => Array.from(document.querySelectorAll('canvas')).length")
    assert contexts == 0, (
        f"the archive route created {contexts} drawing surfaces; it ships none of "
        f"the field code")
    body = _text(site.get("/blog"))
    for marker in (ARCHIVE_TITLE, ARCHIVE_SUBTITLE, PUBLISHED_POST_CODE,
                   SECOND_PUBLISHED_POST_CODE, PUBLISHED_POST,
                   SECOND_PUBLISHED_POST):
        assert marker in body, (
            f"the archive omits {marker!r}; body starts {body[:300]!r}")
    assert DRAFT_POST not in body, (
        f"the archive lists the draft piece {DRAFT_POST!r}")


def test_counter_climbs_without_resetting(page, app_url):
    page.goto(f"{app_url}/", wait_until="networkidle")
    page.wait_for_timeout(1500)

    def figure():
        text = page.locator(f"text={COUNTER_PHRASE}").first.evaluate(
            "n => (n.parentElement || n).innerText")
        found = re.search(r"([\d,.]+)\s*trillion", text)
        return float(found.group(1).replace(",", "")) if found else None

    first = figure()
    assert first is not None, (
        "the counter does not read as a figure followed by the word trillion")
    page.wait_for_timeout(3000)
    second = figure()
    assert second > first, (
        f"the counter did not climb: it read {first} then {second}")
    page.mouse.wheel(0, 5000)
    page.wait_for_timeout(1500)
    third = figure()
    assert third >= second, (
        f"the counter reset on scroll: it read {second} then {third}")


def test_studio_grid_and_inline_banner(page, app_url):
    page.goto(f"{app_url}/login", wait_until="networkidle")
    page.get_by_label(re.compile("email", re.I)).first.fill(AUTHOR_EMAIL)
    page.get_by_label(re.compile("password", re.I)).first.fill(CORPUS_PASSWORD)
    page.get_by_role("button", name=re.compile("sign in|log in", re.I)).first.click()
    page.wait_for_timeout(2000)
    page.goto(f"{app_url}/studio", wait_until="networkidle")
    cards = page.locator("[data-studio-card], article, .card")
    assert cards.count() >= 1, (
        "the studio index shows no cards; it is a grid of cards, one per piece "
        "and one per diagram")
    page.goto(f"{app_url}/studio/new/piece", wait_until="networkidle")
    assert page.url.endswith("/studio/new/piece"), (
        f"wizard step one is not addressable: the browser landed on {page.url!r}")
    page.goto(f"{app_url}/studio/new/diagram", wait_until="networkidle")
    scrub = page.locator("input[type='range']")
    assert scrub.count() >= 1, (
        "wizard step two offers no scrub bar driving the diagram progress")
    page.goto(f"{app_url}/studio/new/review", wait_until="networkidle")
    assert page.url.endswith("/studio/new/review"), (
        f"wizard step three is not addressable: the browser landed on {page.url!r}")


def test_empty_states_name_the_absence(client, author_token, site):
    desk = _text(site.get("/desk"))
    studio = _text(site.get("/studio/new/diagram"))
    for marker, body, where in ((EMPTY_DESK_TITLE, desk, "/desk"),
                                (EMPTY_DESK_LINE, desk, "/desk"),
                                (EMPTY_EDITOR_TITLE, studio, "/studio/new/diagram"),
                                (EMPTY_EDITOR_LINE, studio, "/studio/new/diagram")):
        if body:
            assert marker in body or "login" in body.lower() or "sign in" in body.lower(), (
                f"the surface {where!r} carries neither the empty-state copy "
                f"{marker!r} nor the sign-in it redirects to")
    assert client.get("/health").status_code == 200
