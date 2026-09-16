from __future__ import annotations

import concurrent.futures
import re
import uuid

import httpx
import pytest

from conftest import (
    APP_URL, ASSET_CLASS_TABS, AUTHOR_EMAIL, CAPABILITY_MARKERS, CORPUS_PASSWORD,
    CRYPTO_SYMBOLS, DRAFT_IDEA, FEATURE_CHIPS, FOOTER_BADGE,
    FUTURES_HERO_SUBLINE, FUTURES_PRICE_DISPLAY, FUTURES_PRICE_NOTE,
    HEADER_MENU, HERO_ACTION, HERO_REASSURANCE, HERO_SUBHEADLINE,
    IDEA_BIASES, IDEA_STATUSES, INDEX_SYMBOLS, MARKET_SESSIONS,
    MARKET_SUMMARY_FIELDS, MARKET_SUMMARY_TITLE, MATRIX_TITLE, METRIC_LABELS,
    NARROW_VIEWPORT, NOT_FOUND_ACTION, NOT_FOUND_WORD, PRIMARY_SYMBOL,
    PRIMARY_SYMBOL_NAME, PUBLIC_ROUTES, PUBLISHED_IDEA, RATE_SYMBOLS,
    READER_EMAIL, SEARCH_PLACEHOLDER, SECOND_AUTHOR_EMAIL,
    SECOND_PUBLISHED_IDEA, SECTION_SUBTITLE, SECTION_TITLE, SEEDED_SYMBOLS,
    SUBSCRIBE_LABEL, TICK_DIRECTIONS, anchor, attach_snapshot, bearer,
    make_draft, png_bytes, poll, probe_email, settle, sign_in,
)

SECRET_NEEDLES = ("STORAGE_SECRET_KEY", "STORAGE_ACCESS_KEY", "minio-root-",
                  "deku-storage-", "postgresql://", "DB_ADMIN_URL")


def _text(response: httpx.Response) -> str:
    return response.text or ""


def _slug_of(idea: dict) -> str:
    slug = idea.get("slug")
    assert slug, f"created idea carries no slug: {idea!r}"
    return slug


def _find_idea(payload, title: str):
    for row in payload:
        if row.get("title") == title:
            return row
    return None


def test_health_and_deployment_contract(client, site):
    r = client.get("/health")
    assert r.status_code == 200, anchor("health route", r)

    home = site.get("/")
    assert home.status_code == 200, anchor("home route", home)
    assert APP_URL.startswith("http"), f"APP_PUBLIC_URL is not an address: {APP_URL!r}"
    assert "127.0.0.1" not in APP_URL, (
        f"the app answers on loopback only at {APP_URL!r}, so it is unreachable "
        f"from outside the container")


def test_public_routes_render_before_script(site):
    for route in PUBLIC_ROUTES:
        r = site.get(route)
        assert r.status_code == 200, anchor(f"public route {route}", r)
        body = _text(r)
        for entry in HEADER_MENU:
            assert entry in body, (
                f"public route {route} answered {r.status_code} and its document "
                f"omits the header entry {entry!r}; body starts {body[:200]!r}")
        assert FOOTER_BADGE in body, (
            f"public route {route} omits the footer badge {FOOTER_BADGE!r}; "
            f"body starts {body[:200]!r}")
        assert SEARCH_PLACEHOLDER in body, (
            f"public route {route} omits the search placeholder "
            f"{SEARCH_PLACEHOLDER!r}; body starts {body[:200]!r}")

    home = _text(site.get("/"))
    for marker in (HERO_ACTION, HERO_SUBHEADLINE, HERO_REASSURANCE,
                   SECTION_TITLE, SECTION_SUBTITLE, MARKET_SUMMARY_TITLE):
        assert marker in home, (
            f"the home document omits the pinned copy {marker!r}; "
            f"body starts {home[:200]!r}")
    for chip in FEATURE_CHIPS:
        assert chip in home, (
            f"the home document omits the feature chip {chip!r}; "
            f"body starts {home[:200]!r}")


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


def test_persisted_account_row_survives_a_reload(client, db):
    email = probe_email()
    r = client.post("/auth/signup",
                    json={"email": email, "password": CORPUS_PASSWORD,
                          "role": "author"})
    assert r.status_code in (200, 201), anchor(f"signup for {email}", r)

    stored = poll(lambda: db.one("accounts", email=email))
    assert stored is not None, (
        f"no row persisted in accounts for {email!r} after a successful signup")
    assert stored.get("role") == "author", (
        f"the persisted account row for {email!r} carries role "
        f"{stored.get('role')!r} rather than 'author'")
    assert db.count("accounts", email=email) == 1, (
        f"accounts holds {db.count('accounts', email=email)} rows for {email!r}, "
        f"expected exactly one")

    token = sign_in(client, email)
    me = client.get("/auth/me", headers=bearer(token))
    assert me.status_code == 200, anchor("auth me after a fresh sign in", me)


def test_form_validation_refuses_invalid_input(client, db):
    email = probe_email()
    before = db.count("accounts")
    empty_password = client.post("/auth/signup",
                                 json={"email": email, "password": "",
                                       "role": "reader"})
    assert 400 <= empty_password.status_code < 500, anchor(
        "a signup with an empty password must be refused", empty_password)
    assert "password" in _text(empty_password).lower(), anchor(
        "the refusal must name the password field", empty_password)

    unknown = client.post("/auth/login",
                          json={"email": probe_email(), "password": CORPUS_PASSWORD})
    assert 400 <= unknown.status_code < 500, anchor(
        "a sign in for an unknown address must be refused", unknown)

    settle()
    assert db.count("accounts") == before, (
        f"accounts moved from {before} to {db.count('accounts')} rows across two "
        f"refused submissions; a refused form writes nothing")


def test_market_summary_shape_and_direction(client):
    r = client.get("/markets/summary")
    assert r.status_code == 200, anchor("market summary", r)
    payload = r.json()
    assert isinstance(payload, list), anchor(
        "the market summary must answer a top-level JSON array", r)
    assert payload, anchor("the market summary answered an empty array", r)

    tickers = {row.get("symbol") for row in payload}
    assert PRIMARY_SYMBOL in tickers, (
        f"the market summary omits the primary symbol {PRIMARY_SYMBOL!r}; "
        f"it carries {sorted(t for t in tickers if t)!r}")

    for row in payload:
        for field in MARKET_SUMMARY_FIELDS:
            assert field in row, (
                f"a market summary entry omits the field {field!r}; "
                f"the entry reads {row!r}")
        assert row["direction"] in TICK_DIRECTIONS, (
            f"entry {row.get('symbol')!r} carries direction "
            f"{row['direction']!r}, expected one of {TICK_DIRECTIONS!r}")
        assert row["session"] in MARKET_SESSIONS, (
            f"entry {row.get('symbol')!r} carries session {row['session']!r}, "
            f"expected one of {MARKET_SESSIONS!r}")
        change = str(row["change"])
        rising = not change.strip().startswith("-")
        if float(re.sub(r"[^0-9.\-]", "", change) or 0) != 0:
            assert (row["direction"] == "up") == rising, (
                f"entry {row.get('symbol')!r} reports change {change!r} with "
                f"direction {row['direction']!r}; the two disagree")


def test_market_values_move_without_a_reload(client, page):
    first = client.get("/markets/summary")
    assert first.status_code == 200, anchor("first market summary read", first)
    baseline = {row["symbol"]: str(row["value"]) for row in first.json()}

    def moved():
        later = client.get("/markets/summary")
        if later.status_code != 200:
            return None
        current = {row["symbol"]: str(row["value"]) for row in later.json()}
        changed = [s for s, v in current.items() if baseline.get(s) != v]
        return changed or None

    changed = poll(moved)
    assert changed, (
        f"no seeded symbol changed value across {len(baseline)} symbols over "
        f"repeated reads of the market summary; the surface is a snapshot rather "
        f"than a stream")

    page.goto(f"{APP_URL}/", wait_until="networkidle")
    card = page.query_selector(f"text={PRIMARY_SYMBOL}")
    assert card is not None, (
        f"the home route renders no ticker card for {PRIMARY_SYMBOL!r}, so the "
        f"market summary has nothing to move")
    summary = page.query_selector("main") or page.query_selector("body")
    start_box = summary.bounding_box()
    start_text = page.inner_text("body")
    start_url = page.url

    def page_moved():
        return page.inner_text("body") != start_text

    assert poll(page_moved), (
        "no value on the rendered market summary changed while the page stayed "
        "open, so the surface never updates in place")
    assert page.url == start_url, (
        f"the page moved from {start_url!r} to {page.url!r} while values "
        f"updated; a tick must not reload the document")
    end_box = summary.bounding_box()
    assert start_box and end_box and abs(start_box["height"] - end_box["height"]) <= 2, (
        f"the market block changed height from {start_box and start_box['height']!r} "
        f"to {end_box and end_box['height']!r} as values updated; a tick must not "
        f"re-lay out its neighbours")


def test_snapshot_bytes_are_stored_in_the_bucket_at_their_key(client, author_token,
                                                              storage):
    idea = make_draft(client, author_token, f"Probe Upload {uuid.uuid4().hex[:6]}")
    slug = _slug_of(idea)
    uploaded = attach_snapshot(client, author_token, slug,
                               png_bytes(uuid.uuid4().bytes))
    assert uploaded.status_code in (200, 201), anchor(
        f"snapshot upload for {slug}", uploaded)

    key = uploaded.json().get("snapshot_key")
    assert key, anchor(
        f"the idea {slug} carries no snapshot_key after a successful upload",
        uploaded)
    assert key.startswith("ideas/"), (
        f"the stored key {key!r} does not follow the pinned scheme "
        f"ideas/<idea_id>/<sha256_of_bytes>.<ext>")
    assert re.fullmatch(r"ideas/[^/]+/[0-9a-f]{64}\.[A-Za-z0-9]+", key), (
        f"the stored key {key!r} does not follow the pinned scheme "
        f"ideas/<idea_id>/<sha256_of_bytes>.<ext>")

    present = poll(lambda: storage.exists(key))
    assert present, (
        f"the object store holds no object at {key!r} after a successful upload; "
        f"the bucket currently lists {storage.list('ideas/')[:10]!r}")


def test_snapshot_upload_across_accounts_is_denied(client, author_token,
                                                   second_author_token, storage):
    idea = make_draft(client, author_token, f"Probe Guard {uuid.uuid4().hex[:6]}")
    slug = _slug_of(idea)
    before = set(storage.list("ideas/"))

    denied = attach_snapshot(client, second_author_token, slug,
                             png_bytes(uuid.uuid4().bytes))
    assert denied.status_code in (401, 403, 404), anchor(
        f"a second author attaching a snapshot to {slug} must be denied", denied)

    settle()
    assert set(storage.list("ideas/")) == before, (
        f"the bucket gained an object after a denied upload for {slug}; "
        f"a denied attach writes nothing")


def test_draft_idea_is_private_to_its_author(client, author_token, reader_token,
                                             second_author_token):
    idea = make_draft(client, author_token, f"Probe Draft {uuid.uuid4().hex[:6]}")
    slug = _slug_of(idea)

    owner = client.get(f"/ideas/{slug}", headers=bearer(author_token))
    assert owner.status_code == 200, anchor(
        f"the owning author reading its own draft {slug}", owner)

    for label, headers in (("an anonymous caller", {}),
                           ("a reader account", bearer(reader_token)),
                           ("a second author", bearer(second_author_token))):
        r = client.get(f"/ideas/{slug}", headers=headers)
        assert r.status_code in (401, 403, 404), anchor(
            f"{label} reading the draft {slug} must be denied", r)
        assert slug not in _text(r) or r.status_code == 404, anchor(
            f"{label} received draft content for {slug}", r)

    listing = client.get("/ideas")
    assert listing.status_code == 200, anchor("published ideas listing", listing)
    titles = [row.get("title") for row in listing.json()]
    assert idea.get("title") not in titles, (
        f"the draft {idea.get('title')!r} appears in the published listing "
        f"{titles!r}")
    assert DRAFT_IDEA not in titles, (
        f"the seeded draft {DRAFT_IDEA!r} appears in the published listing "
        f"{titles!r}")


def test_draft_snapshot_is_denied_to_other_accounts(client, author_token,
                                                    reader_token):
    idea = make_draft(client, author_token, f"Probe Bytes {uuid.uuid4().hex[:6]}")
    slug = _slug_of(idea)
    uploaded = attach_snapshot(client, author_token, slug,
                               png_bytes(uuid.uuid4().bytes))
    assert uploaded.status_code in (200, 201), anchor(
        f"snapshot upload for {slug}", uploaded)

    owner = client.get(f"/ideas/{slug}/snapshot", headers=bearer(author_token))
    assert owner.status_code == 200, anchor(
        f"the owning author reading its own draft snapshot {slug}", owner)
    assert owner.content, anchor(
        f"the owning author received an empty body for {slug}", owner)

    for label, headers in (("an anonymous caller", {}),
                           ("a reader account", bearer(reader_token))):
        r = client.get(f"/ideas/{slug}/snapshot", headers=headers)
        assert r.status_code in (401, 403, 404), anchor(
            f"{label} reading the draft snapshot {slug} must be denied", r)
        assert not r.content or r.status_code != 200, anchor(
            f"{label} received image bytes for the draft {slug}", r)


def test_publish_opens_the_idea_and_repeats_cleanly(client, author_token,
                                                    reader_token, storage):
    idea = make_draft(client, author_token, f"Probe Publish {uuid.uuid4().hex[:6]}")
    slug = _slug_of(idea)
    uploaded = attach_snapshot(client, author_token, slug,
                               png_bytes(uuid.uuid4().bytes))
    assert uploaded.status_code in (200, 201), anchor(
        f"snapshot upload for {slug}", uploaded)
    key = uploaded.json().get("snapshot_key")

    first = client.post(f"/ideas/{slug}/publish", headers=bearer(author_token))
    assert first.status_code in (200, 201), anchor(f"publishing {slug}", first)
    assert first.json().get("status") == "published", anchor(
        f"the published idea {slug} does not carry the published status", first)
    assert first.json().get("published_at"), anchor(
        f"the published idea {slug} carries no published_at stamp", first)

    public = client.get(f"/ideas/{slug}")
    assert public.status_code == 200, anchor(
        f"an anonymous caller reading the published idea {slug}", public)
    public_bytes = client.get(f"/ideas/{slug}/snapshot")
    assert public_bytes.status_code == 200, anchor(
        f"an anonymous caller reading the published snapshot {slug}", public_bytes)

    again = client.post(f"/ideas/{slug}/publish", headers=bearer(author_token))
    assert again.status_code < 500, anchor(
        f"a repeated publish of {slug} must not fail the server", again)

    settle()
    listing = client.get("/ideas")
    matches = [row for row in listing.json() if row.get("slug") == slug]
    assert len(matches) == 1, (
        f"the published listing carries {len(matches)} entries for {slug}, "
        f"expected exactly one after a repeated publish")
    keys = [k for k in storage.list("ideas/") if k == key]
    assert len(keys) == 1, (
        f"the bucket holds {len(keys)} objects at {key!r} after a repeated "
        f"publish, expected exactly one")


def test_concurrent_publish_accepts_exactly_one(client, author_token, api_base):
    idea = make_draft(client, author_token, f"Probe Race {uuid.uuid4().hex[:6]}")
    slug = _slug_of(idea)
    uploaded = attach_snapshot(client, author_token, slug,
                               png_bytes(uuid.uuid4().bytes))
    assert uploaded.status_code in (200, 201), anchor(
        f"snapshot upload for {slug}", uploaded)

    def publish():
        with httpx.Client(base_url=api_base, timeout=30.0) as c:
            return c.post(f"/ideas/{slug}/publish", headers=bearer(author_token))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        responses = [f.result() for f in
                     [pool.submit(publish), pool.submit(publish)]]

    accepted = [r for r in responses if r.status_code in (200, 201)]
    statuses = [r.status_code for r in responses]
    assert len(accepted) == 1, (
        f"two simultaneous publishes of {slug} answered {statuses!r}; exactly one "
        f"must be accepted and the other rejected")

    settle()
    listing = client.get("/ideas")
    matches = [row for row in listing.json() if row.get("slug") == slug]
    assert len(matches) == 1, (
        f"the published listing carries {len(matches)} entries for {slug} after "
        f"a contested publish, expected exactly one")


def test_publish_across_accounts_is_denied(client, author_token,
                                           second_author_token):
    idea = make_draft(client, author_token, f"Probe Cross {uuid.uuid4().hex[:6]}")
    slug = _slug_of(idea)
    uploaded = attach_snapshot(client, author_token, slug,
                               png_bytes(uuid.uuid4().bytes))
    assert uploaded.status_code in (200, 201), anchor(
        f"snapshot upload for {slug}", uploaded)

    denied = client.post(f"/ideas/{slug}/publish",
                         headers=bearer(second_author_token))
    assert denied.status_code in (401, 403, 404), anchor(
        f"a second author publishing {slug} must be denied", denied)

    settle()
    still_draft = client.get(f"/ideas/{slug}", headers=bearer(author_token))
    assert still_draft.status_code == 200, anchor(
        f"the owning author reading {slug} after a denied publish", still_draft)
    assert still_draft.json().get("status") == "draft", anchor(
        f"the idea {slug} left the draft status after a denied publish",
        still_draft)


def test_published_ideas_list_newest_first(client):
    r = client.get("/ideas")
    assert r.status_code == 200, anchor("published ideas listing", r)
    payload = r.json()
    assert isinstance(payload, list), anchor(
        "the ideas listing must answer a top-level JSON array", r)

    titles = [row.get("title") for row in payload]
    for seeded in (PUBLISHED_IDEA, SECOND_PUBLISHED_IDEA):
        assert seeded in titles, (
            f"the published listing omits the seeded idea {seeded!r}; "
            f"it carries {titles!r}")

    for row in payload:
        assert row.get("status", "published") == "published", (
            f"the listing carries {row.get('title')!r} with status "
            f"{row.get('status')!r}, expected published only")
        assert row.get("bias") in IDEA_BIASES, (
            f"idea {row.get('title')!r} carries bias {row.get('bias')!r}, "
            f"expected one of {IDEA_BIASES!r}")

    stamps = [row.get("published_at") for row in payload if row.get("published_at")]
    assert stamps == sorted(stamps, reverse=True), (
        f"the listing is not ordered newest first; published_at reads {stamps!r}")


def test_boost_counts_once_per_account(client, reader_token, db):
    listing = client.get("/ideas")
    idea = _find_idea(listing.json(), PUBLISHED_IDEA)
    assert idea is not None, (
        f"the seeded published idea {PUBLISHED_IDEA!r} is absent from the listing")
    slug = idea["slug"]
    before = int(idea.get("boost_count") or 0)

    first = client.post(f"/ideas/{slug}/boost", headers=bearer(reader_token))
    assert first.status_code in (200, 201), anchor(f"boosting {slug}", first)

    after_one = poll(lambda: _find_idea(client.get("/ideas").json(), PUBLISHED_IDEA))
    assert after_one is not None, f"the idea {PUBLISHED_IDEA!r} left the listing"
    raised = int(after_one.get("boost_count") or 0)
    assert raised == before + 1, (
        f"the boost count for {slug} moved from {before} to {raised}, expected "
        f"exactly one more")

    repeat = client.post(f"/ideas/{slug}/boost", headers=bearer(reader_token))
    assert repeat.status_code < 500, anchor(
        f"a repeated boost of {slug} must not fail the server", repeat)

    settle()
    final = _find_idea(client.get("/ideas").json(), PUBLISHED_IDEA)
    assert int(final.get("boost_count") or 0) == raised, (
        f"the boost count for {slug} moved to {final.get('boost_count')!r} on a "
        f"repeat from the same account, expected it to stay at {raised}")

    rows = db.rows("boosts")
    assert rows is not None, "the boosts table is unreadable in the database"


def test_anonymous_boost_is_denied(client):
    listing = client.get("/ideas")
    idea = _find_idea(listing.json(), SECOND_PUBLISHED_IDEA)
    assert idea is not None, (
        f"the seeded published idea {SECOND_PUBLISHED_IDEA!r} is absent from the "
        f"listing")
    slug = idea["slug"]
    before = int(idea.get("boost_count") or 0)

    denied = client.post(f"/ideas/{slug}/boost")
    assert denied.status_code in (401, 403), anchor(
        f"an anonymous boost of {slug} must be denied", denied)

    settle()
    after = _find_idea(client.get("/ideas").json(), SECOND_PUBLISHED_IDEA)
    assert int(after.get("boost_count") or 0) == before, (
        f"the boost count for {slug} moved from {before} to "
        f"{after.get('boost_count')!r} after a denied anonymous boost")


def test_reader_is_denied_the_studio_surface(client, reader_token):
    mine = client.get("/ideas?mine=true", headers=bearer(reader_token))
    assert mine.status_code in (401, 403, 200), anchor(
        "a reader asking for its own ideas", mine)
    if mine.status_code == 200:
        assert mine.json() == [], anchor(
            "a reader account owns no ideas, so the reply must be empty", mine)

    created = client.post("/ideas",
                          json={"title": f"Reader Attempt {uuid.uuid4().hex[:6]}",
                                "thesis": "A reader must not compose.",
                                "symbol": "SPX", "bias": "long", "tags": []},
                          headers=bearer(reader_token))
    assert created.status_code in (401, 403), anchor(
        "a reader account composing an idea must be denied", created)


def test_futures_route_carries_price_and_matrix(site, page):
    r = site.get("/futures")
    assert r.status_code == 200, anchor("futures route", r)
    body = _text(r)
    for marker in (FUTURES_PRICE_DISPLAY, FUTURES_PRICE_NOTE, SUBSCRIBE_LABEL,
                   FUTURES_HERO_SUBLINE, MATRIX_TITLE):
        assert marker in body, (
            f"the futures document omits the pinned copy {marker!r}; "
            f"body starts {body[:200]!r}")
    for tab in ASSET_CLASS_TABS:
        assert tab in body, (
            f"the futures document omits the asset-class tab {tab!r}; "
            f"body starts {body[:200]!r}")
    for label in METRIC_LABELS:
        assert label in body, (
            f"the futures document omits the metric label {label!r}; "
            f"body starts {body[:200]!r}")
    assert body.count(SUBSCRIBE_LABEL) >= 2, (
        f"the futures document names {SUBSCRIBE_LABEL!r} "
        f"{body.count(SUBSCRIBE_LABEL)} time(s); the closing data-access band "
        f"repeats the action the price block offers")

    page.goto(f"{APP_URL}/futures", wait_until="networkidle")
    before_url = page.url
    before = page.inner_text("body")
    metals = page.get_by_text("Metals", exact=True)
    assert metals.count() >= 1, (
        "the rendered futures route offers no Metals tab, so the asset-class "
        "matrix cannot be moved between its nine classes")
    metals.first.click()
    settle()
    assert page.url == before_url, (
        f"selecting the Metals tab moved the reader from {before_url!r} to "
        f"{page.url!r}; the matrix swaps its card in place")
    assert page.inner_text("body") != before, (
        "selecting the Metals tab changed nothing on the page, so the matrix "
        "card did not swap")


def test_platform_route_states_six_capabilities(site):
    r = site.get("/platform")
    assert r.status_code == 200, anchor("platform route", r)
    lowered = _text(r).lower()
    for marker in CAPABILITY_MARKERS:
        assert marker.lower() in lowered, (
            f"the platform document omits the capability marker {marker!r}; "
            f"body starts {_text(r)[:200]!r}")


def test_markets_route_lists_every_seeded_symbol(site, client):
    page = site.get("/markets")
    assert page.status_code == 200, anchor("markets route", page)
    body = _text(page)
    for ticker in SEEDED_SYMBOLS:
        assert ticker in body, (
            f"the markets document omits the seeded symbol {ticker!r}; "
            f"body starts {body[:200]!r}")

    api = client.get("/markets")
    assert api.status_code == 200, anchor("markets listing", api)
    payload = api.json()
    assert isinstance(payload, list), anchor(
        "the markets listing must answer a top-level JSON array", api)
    tickers = {row.get("symbol") for row in payload}
    missing = [t for t in SEEDED_SYMBOLS if t not in tickers]
    assert not missing, (
        f"the markets listing omits the seeded symbols {missing!r}; "
        f"it carries {sorted(t for t in tickers if t)!r}")
    assert PRIMARY_SYMBOL_NAME in body or PRIMARY_SYMBOL in body, (
        f"the markets document names neither {PRIMARY_SYMBOL_NAME!r} nor "
        f"{PRIMARY_SYMBOL!r}")
    for group in (INDEX_SYMBOLS, CRYPTO_SYMBOLS, RATE_SYMBOLS):
        assert any(t in tickers for t in group), (
            f"the markets listing carries none of {group!r}")


def test_cookie_choice_survives_a_reload(page):
    page.goto(f"{APP_URL}/", wait_until="networkidle")
    body = page.content()
    assert "cookie" in body.lower(), (
        "the home route asks a first-time visitor nothing about cookies; "
        f"the document starts {body[:200]!r}")

    refuse = page.get_by_role("button", name=re.compile(
        r"refuse|reject|decline|only essential", re.I))
    assert refuse.count() >= 1, (
        "the cookie band offers no refusing control beside the accepting one, so "
        "refusing is harder to press than accepting")
    accept = page.get_by_role("button", name=re.compile(r"accept|allow|agree", re.I))
    assert accept.count() >= 1, (
        "the cookie band offers no accepting control, so the question cannot be "
        "answered either way")
    refuse.first.click()
    settle()

    page.goto(f"{APP_URL}/", wait_until="networkidle")
    assert page.get_by_role("button", name=re.compile(
        r"refuse|reject|decline|only essential", re.I)).count() == 0, (
        "the cookie question returned on a reload after it had been answered; the "
        "answer must outlive the page")

    page.goto(f"{APP_URL}/ideas", wait_until="networkidle")
    assert page.get_by_role("button", name=re.compile(
        r"refuse|reject|decline|only essential", re.I)).count() == 0, (
        "the cookie band reappeared on a later route after the visitor answered")


def test_unknown_address_renders_the_not_found_chrome(site, page):
    unknown = f"/no-such-route-{uuid.uuid4().hex[:8]}"
    r = site.get(unknown)
    assert r.status_code == 404, anchor(
        "an unknown address must answer not found", r)
    body = _text(r)
    for marker in (NOT_FOUND_WORD, NOT_FOUND_ACTION, FOOTER_BADGE):
        assert marker in body, (
            f"the not-found document omits {marker!r}; body starts {body[:200]!r}")
    for entry in HEADER_MENU:
        assert entry in body, (
            f"the not-found document omits the header entry {entry!r}, so the "
            f"global chrome does not wrap it; body starts {body[:200]!r}")

    page.goto(f"{APP_URL}{unknown}", wait_until="networkidle")
    way_home = page.get_by_role("link", name=re.compile(NOT_FOUND_ACTION, re.I))
    if way_home.count() == 0:
        way_home = page.get_by_role("button", name=re.compile(NOT_FOUND_ACTION, re.I))
    assert way_home.count() >= 1, (
        f"the rendered not-found page offers no control reading "
        f"{NOT_FOUND_ACTION!r}, so a lost visitor has no way back")


def test_content_images_carry_alternative_text(page):
    missing = []
    for route in ("/", "/ideas", "/futures"):
        page.goto(f"{APP_URL}{route}", wait_until="networkidle")
        for handle in page.query_selector_all("img"):
            alt = handle.get_attribute("alt")
            aria_hidden = handle.get_attribute("aria-hidden")
            role = handle.get_attribute("role")
            decorative = alt == "" or aria_hidden == "true" or role == "presentation"
            if alt is None and not decorative:
                missing.append((route, handle.get_attribute("src")))
    assert not missing, (
        f"{len(missing)} content image(s) carry neither alternative text nor a "
        f"declaration that they are decorative: {missing[:5]!r}")


def test_narrow_viewport_has_no_sideways_overflow(page):
    page.set_viewport_size(NARROW_VIEWPORT)
    overflowing = []
    for route in ("/", "/markets", "/futures", "/ideas"):
        page.goto(f"{APP_URL}{route}", wait_until="networkidle")
        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        client_width = page.evaluate("document.documentElement.clientWidth")
        if scroll_width > client_width + 1:
            overflowing.append((route, scroll_width, client_width))
    assert not overflowing, (
        f"at a narrow viewport of {NARROW_VIEWPORT['width']} the following routes "
        f"scroll sideways as route, scrollWidth, clientWidth: {overflowing!r}")


def test_no_credential_reaches_the_browser(site, client):
    leaks = []
    for route in PUBLIC_ROUTES + ("/login", "/signup"):
        r = site.get(route)
        assert r.status_code in (200, 404), anchor(f"route {route}", r)
        body = _text(r)
        for needle in SECRET_NEEDLES:
            if needle in body:
                leaks.append((route, needle))
        for match in re.findall(r'(?:src|href)="([^"]+\.js[^"]*)"', body):
            if match.startswith("http") and APP_URL not in match:
                continue
            asset = site.get(match if match.startswith("/") else f"/{match}")
            if asset.status_code != 200:
                continue
            for needle in SECRET_NEEDLES:
                if needle in _text(asset):
                    leaks.append((match, needle))

    summary = client.get("/markets/summary")
    for needle in SECRET_NEEDLES:
        if needle in _text(summary):
            leaks.append(("/api/markets/summary", needle))

    assert not leaks, (
        f"the browser downloads carrying a credential: {leaks!r}; no store key "
        f"and no database address may reach anything the browser receives")
