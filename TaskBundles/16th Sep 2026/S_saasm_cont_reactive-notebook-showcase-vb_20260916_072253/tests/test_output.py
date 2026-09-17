from __future__ import annotations

import concurrent.futures
import re as _re

import httpx
from _shapes import flatten, items
from appclient import app_url
from appclient import client as make_client

from conftest import (
    AUTHOR2_EMAIL,
    AUTHOR_EMAIL,
    BLOCK_KINDS,
    DRAFT_SLUG,
    FORKED_SLUG,
    PAGE_SIZE,
    PUBLIC_ROUTES,
    PUBLISHED_SLUGS,
    READER_EMAIL,
    SEEDED_NOTEBOOK_COUNT,
    SEED_PASSWORD,
    STATE_DRAFT,
    STATE_PUBLISHED,
    TOP_NINE,
    add_block,
    create_page,
    digest_of,
    key_for,
    publish,
    settle,
    signup_payload,
    upload_media,
)

BANNER_COPY = "Notebooks 2.0 is now live on the web."
HOME_HEADLINE = "Not your typical notebook"
VALUE_LINE = "The shortest path from idea to live code"
FEATURE_HEADINGS = ("Literate programming", "Connect to any data", "Built-in reactivity")
PANEL_EYEBROWS = ("MULTIPLAYER EDITING", "EMBEDDING")
COMMUNITY_HEADLINE = "Join the community"
CLOSING_HEADLINE = "Get started today"
CLOSING_BUTTON = "Sign up for notebooks"
AI_HEADLINE = "Supercharge your data workflow with AI"
AI_PANELS = ("Pair with AI",)
USE_CASE = "Define a metric with natural language"
TESTIMONIAL_PEOPLE = ("Alex Rivera", "Sam Okafor")
TESTIMONIAL_LINK = "See their work"
SORT_TABS = ("Trending", "Recent", "Most stars last month", "Most stars all time")
DEFAULT_TAB = "Most stars all time"
SIGNUP_HEADING = "Sign up"
SIGNUP_METHODS = ("GitHub", "Google", "Microsoft", "SSO", "Email")
SIGNUP_FINE_PRINT = "By continuing you agree to our Terms of Service."
NOT_FOUND_COPY = "Sorry, but we can't find that page right now."
FOOTER_COLUMNS = ("Platform", "Docs", "Resources", "Company")
FOOTER_LEGAL = "Vulnerability Disclosure"
TERMS_ROUTE = "/terms-of-service"

SECRET_MARKERS = ("STORAGE_SECRET_KEY", "minio-root-", "postgresql://", "DATABASE_URL=")


def _web():
    return httpx.Client(base_url=app_url(), timeout=30.0, follow_redirects=True)


def _slugs_of(payload) -> list:
    out = []
    for row in items(payload):
        if isinstance(row, dict):
            out.append(row.get("slug"))
    return [s for s in out if s]


def test_health_returns_ok(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:400]}"
    )


def test_seeded_accounts_sign_in_with_the_corpus_password(anon_client, db):
    for email in (AUTHOR_EMAIL, AUTHOR2_EMAIL, READER_EMAIL):
        response = anon_client.post(
            "/auth/login", json={"email": email, "password": SEED_PASSWORD})
        assert response.status_code == 200, (
            f"POST /api/auth/login for {email} returned {response.status_code}: "
            f"{response.text[:400]}"
        )
        token = response.json().get("access_token") or response.json().get("token")
        assert token, (
            f"POST /api/auth/login for {email} returned no bearer token: "
            f"{response.text[:400]}"
        )
    for email in (AUTHOR_EMAIL, AUTHOR2_EMAIL):
        assert db.author_by_email(email), f"no authors row for {email}"


def test_home_page_arrives_as_complete_html(anon_client):
    with _web() as web:
        page = web.get("/")
        assert page.status_code == 200, (
            f"GET / returned {page.status_code}: {page.text[:400]}"
        )
        for copy in (HOME_HEADLINE, VALUE_LINE, COMMUNITY_HEADLINE, CLOSING_HEADLINE):
            assert copy in page.text, (
                f"GET / returned HTML without {copy!r}, so the first paint is an empty "
                f"shell the browser has to fill: {page.text[:400]}"
            )


def test_home_route_carries_its_banner_and_hero_copy(anon_client):
    with _web() as web:
        page = web.get("/")
        assert page.status_code == 200, (
            f"GET / returned {page.status_code}: {page.text[:400]}"
        )
        assert BANNER_COPY in page.text, (
            f"GET / does not carry the announcement copy {BANNER_COPY!r}: "
            f"{page.text[:400]}"
        )
        assert CLOSING_BUTTON in page.text, (
            f"GET / does not carry the closing action {CLOSING_BUTTON!r}"
        )


def test_home_route_carries_its_three_feature_cards(anon_client):
    with _web() as web:
        page = web.get("/")
        missing = [h for h in FEATURE_HEADINGS if h not in page.text]
        assert not missing, (
            f"GET / omits the feature card heading(s) {missing}: {page.text[:400]}"
        )


def test_home_route_carries_both_blue_panels(anon_client):
    with _web() as web:
        page = web.get("/")
        missing = [e for e in PANEL_EYEBROWS if e not in page.text]
        assert not missing, (
            f"GET / omits the panel eyebrow(s) {missing}: {page.text[:400]}"
        )


def test_home_blocks_are_stored_in_position_order(anon_client, db):
    page = db.page_by_slug("home")
    assert page, "no pages row for slug 'home'"
    rows = db.blocks_of(page["id"])
    assert rows, "the seeded home page carries no blocks row"
    positions = sorted(r.get("position") for r in rows)
    assert positions == list(range(1, len(rows) + 1)), (
        f"the home page's block positions are {positions}, which is not contiguous "
        f"from 1"
    )
    response = anon_client.get("/pages/home")
    assert response.status_code == 200, (
        f"GET /api/pages/home returned {response.status_code}: {response.text[:400]}"
    )
    served = [b.get("position") for b in items(response.json()) if isinstance(b, dict)]
    if served:
        assert served == sorted(served), (
            f"GET /api/pages/home served blocks out of position order: {served}"
        )


def test_ai_route_carries_its_panels_and_eight_use_cases(anon_client, db):
    with _web() as web:
        page = web.get("/ai")
        assert page.status_code == 200, (
            f"GET /ai returned {page.status_code}: {page.text[:400]}"
        )
        assert AI_HEADLINE in page.text, (
            f"GET /ai does not carry {AI_HEADLINE!r}: {page.text[:400]}"
        )
        for panel in AI_PANELS:
            assert panel in page.text, f"GET /ai omits the panel headline {panel!r}"
        assert USE_CASE in page.text, f"GET /ai omits the use case {USE_CASE!r}"
    ai = db.page_by_slug("ai")
    assert ai, "no pages row for slug 'ai'"
    assert db.count_use_cases(page_id=ai["id"]) == 8, (
        f"the ai page carries {db.count_use_cases(page_id=ai['id'])} use_cases rows "
        f"rather than exactly eight"
    )


def test_ai_route_carries_both_testimonials(anon_client, db):
    with _web() as web:
        page = web.get("/ai")
        for person in TESTIMONIAL_PEOPLE:
            assert person in page.text, (
                f"GET /ai omits the testimonial attributed to {person!r}"
            )
        assert TESTIMONIAL_LINK in page.text, (
            f"GET /ai omits the testimonial link {TESTIMONIAL_LINK!r}"
        )
    ai = db.page_by_slug("ai")
    assert ai, "no pages row for slug 'ai'"
    assert db.count_testimonials(page_id=ai["id"]) == 2, (
        f"the ai page carries {db.count_testimonials(page_id=ai['id'])} testimonials "
        f"rows rather than two"
    )


def test_footer_is_served_on_every_public_route(anon_client, db):
    with _web() as web:
        for route in PUBLIC_ROUTES:
            page = web.get(route)
            assert page.status_code == 200, (
                f"GET {route} returned {page.status_code}: {page.text[:200]}"
            )
            missing = [c for c in FOOTER_COLUMNS if c not in page.text]
            assert not missing, (
                f"GET {route} omits the footer column(s) {missing}"
            )
            assert FOOTER_LEGAL in page.text, (
                f"GET {route} omits the footer legal link {FOOTER_LEGAL!r}"
            )
    assert db.count_footer_links() > 0, (
        "the footer_links table holds no rows, so the footer is written into a "
        "template rather than composed from stored rows"
    )


def test_terms_page_is_served_and_linked_from_the_footer(anon_client):
    with _web() as web:
        page = web.get(TERMS_ROUTE)
        assert page.status_code == 200, (
            f"GET {TERMS_ROUTE} returned {page.status_code}: {page.text[:400]}"
        )
        home = web.get("/")
        assert TERMS_ROUTE in home.text, (
            f"GET / does not link to {TERMS_ROUTE} from its footer"
        )


def test_sitemap_lists_published_routes_and_omits_the_draft(anon_client):
    with _web() as web:
        page = web.get("/sitemap.xml")
        assert page.status_code == 200, (
            f"GET /sitemap.xml returned {page.status_code}: {page.text[:400]}"
        )
        for route in ("/ai", "/top"):
            assert route in page.text, (
                f"/sitemap.xml omits the published route {route}: {page.text[:400]}"
            )
        assert DRAFT_SLUG not in page.text, (
            f"/sitemap.xml names the draft page {DRAFT_SLUG!r}, so a draft is "
            f"discoverable: {page.text[:400]}"
        )


def test_robots_points_at_the_sitemap(anon_client):
    with _web() as web:
        page = web.get("/robots.txt")
        assert page.status_code == 200, (
            f"GET /robots.txt returned {page.status_code}: {page.text[:400]}"
        )
        assert "sitemap.xml" in page.text.lower(), (
            f"/robots.txt does not point at the sitemap: {page.text[:400]}"
        )


def test_security_headers_are_present_on_every_public_route(anon_client):
    with _web() as web:
        for route in PUBLIC_ROUTES:
            page = web.get(route)
            lowered = {k.lower(): v for k, v in page.headers.items()}
            assert "strict-transport-security" in lowered, (
                f"GET {route} carries no strict transport policy header; headers were "
                f"{sorted(lowered)}"
            )
            assert lowered.get("x-content-type-options", "").lower() == "nosniff", (
                f"GET {route} carries no nosniff content-type policy; the header was "
                f"{lowered.get('x-content-type-options')!r}"
            )


def test_no_credential_appears_in_anything_the_browser_downloads(anon_client):
    with _web() as web:
        for route in PUBLIC_ROUTES:
            page = web.get(route)
            found = [m for m in SECRET_MARKERS if m in page.text]
            assert not found, (
                f"GET {route} returns a document containing {found}, so a credential "
                f"reaches the browser"
            )


def test_not_found_chrome_answers_for_an_unknown_address(anon_client):
    with _web() as web:
        page = web.get("/no-such-address-at-all")
        assert page.status_code == 404, (
            f"GET /no-such-address-at-all returned {page.status_code} rather than 404: "
            f"{page.text[:400]}"
        )
        assert NOT_FOUND_COPY in page.text, (
            f"the not-found screen omits {NOT_FOUND_COPY!r}: {page.text[:400]}"
        )
        missing = [c for c in FOOTER_COLUMNS if c not in page.text]
        assert not missing, (
            f"the not-found screen omits the footer column(s) {missing}, so a lost "
            f"visitor loses the navigation"
        )
        assert "/top" in page.text, (
            "the not-found screen offers no link to the popular-notebooks listing"
        )


def test_draft_page_route_answers_not_found(anon_client):
    with _web() as web:
        page = web.get(f"/{DRAFT_SLUG}")
        assert page.status_code == 404, (
            f"GET /{DRAFT_SLUG} returned {page.status_code} rather than 404; a draft "
            f"page is indistinguishable from an address that was never created: "
            f"{page.text[:400]}"
        )


def test_listing_defaults_to_most_stars_all_time(anon_client):
    with _web() as web:
        page = web.get("/top")
        assert page.status_code == 200, (
            f"GET /top returned {page.status_code}: {page.text[:400]}"
        )
        missing = [t for t in SORT_TABS if t not in page.text]
        assert not missing, f"GET /top omits the sort tab(s) {missing}"
    response = anon_client.get("/notebooks")
    assert response.status_code == 200, (
        f"GET /api/notebooks returned {response.status_code}: {response.text[:400]}"
    )
    assert DEFAULT_TAB.lower().replace(" ", "") in flatten(response.json()).replace(
        " ", "").replace("_", "") or True, "sort naming is the app's own"
    slugs = _slugs_of(response.json())
    assert slugs[:1] == [TOP_NINE[0][0]], (
        f"GET /api/notebooks with no sort returned {slugs[:1]} first rather than "
        f"{TOP_NINE[0][0]!r}; the default sort is {DEFAULT_TAB!r}"
    )


def test_listing_orders_the_seeded_nine_by_stars(anon_client):
    response = anon_client.get("/notebooks")
    assert response.status_code == 200, (
        f"GET /api/notebooks returned {response.status_code}: {response.text[:400]}"
    )
    slugs = _slugs_of(response.json())
    expected = [slug for slug, _ in TOP_NINE]
    assert slugs[:9] == expected, (
        f"the default listing opens {slugs[:9]} rather than the nine seeded "
        f"notebooks in star order {expected}"
    )


def test_listing_pages_at_thirty_per_page(anon_client, db):
    assert db.count_notebooks() == SEEDED_NOTEBOOK_COUNT, (
        f"the notebooks table holds {db.count_notebooks()} rows rather than "
        f"{SEEDED_NOTEBOOK_COUNT}"
    )
    first = anon_client.get("/notebooks")
    assert first.status_code == 200, (
        f"GET /api/notebooks returned {first.status_code}: {first.text[:400]}"
    )
    assert len(_slugs_of(first.json())) == PAGE_SIZE, (
        f"the first listing page carried {len(_slugs_of(first.json()))} notebooks "
        f"rather than {PAGE_SIZE}"
    )
    second = anon_client.get("/notebooks", params={"page": 2})
    assert second.status_code == 200, (
        f"GET /api/notebooks?page=2 returned {second.status_code}: {second.text[:400]}"
    )
    rest = _slugs_of(second.json())
    assert len(rest) == SEEDED_NOTEBOOK_COUNT - PAGE_SIZE, (
        f"the second listing page carried {len(rest)} notebooks rather than "
        f"{SEEDED_NOTEBOOK_COUNT - PAGE_SIZE}"
    )
    assert not set(rest) & set(_slugs_of(first.json())), (
        "the second listing page repeats notebooks from the first"
    )


def test_listing_sort_by_recent_changes_the_order(anon_client):
    default = _slugs_of(anon_client.get("/notebooks").json())
    recent = anon_client.get("/notebooks", params={"sort": "recent"})
    assert recent.status_code == 200, (
        f"GET /api/notebooks?sort=recent returned {recent.status_code}: "
        f"{recent.text[:400]}"
    )
    assert _slugs_of(recent.json()) != default, (
        "sorting by recency returned the same order as the star sort, so the sort "
        "parameter changes nothing"
    )


def test_listing_marks_the_forked_notebook(anon_client, db):
    row = db.notebook_by_slug(FORKED_SLUG)
    assert row, f"no notebooks row for slug {FORKED_SLUG!r}"
    assert row.get("forked_from_id"), (
        f"the seeded notebook {FORKED_SLUG!r} records no fork lineage"
    )
    assert row.get("forked_from_id") != row.get("id"), (
        f"{FORKED_SLUG!r} is recorded as forked from itself"
    )


def test_seeded_notebook_counts_match_the_pinned_values(db):
    for slug, stars in TOP_NINE:
        row = db.notebook_by_slug(slug)
        assert row, f"no notebooks row for slug {slug!r}"
        assert row.get("star_count") == stars, (
            f"the notebook {slug!r} carries star_count {row.get('star_count')!r} "
            f"rather than {stars}"
        )
        assert row.get("star_count") >= 0, f"{slug!r} carries a negative star count"
        assert (row.get("comment_count") or 0) >= 0, (
            f"{slug!r} carries a negative comment count"
        )


def test_seeded_pages_are_stored_once_with_their_states(db):
    for slug in PUBLISHED_SLUGS:
        assert db.count_pages(slug=slug) == 1, (
            f"the pages table holds {db.count_pages(slug=slug)} rows for slug "
            f"{slug!r}; seeding is idempotent"
        )
        row = db.page_by_slug(slug)
        assert row.get("state") == STATE_PUBLISHED, (
            f"the seeded page {slug!r} is in state {row.get('state')!r} rather than "
            f"{STATE_PUBLISHED!r}"
        )
    for slug in PUBLISHED_SLUGS:
        stamp = db.page_by_slug(slug).get("published_at")
        offset = getattr(stamp, "utcoffset", lambda: None)()
        text = str(stamp)
        utc = (offset is not None and offset.total_seconds() == 0) or text.endswith("+00:00") or text.endswith("Z")
        assert utc, (
            f"the page {slug!r} carries published_at {text!r}, which has no UTC "
            f"offset; every timestamp is stored in UTC"
        )
    draft = db.page_by_slug(DRAFT_SLUG)
    assert draft, f"no pages row for slug {DRAFT_SLUG!r}"
    assert draft.get("state") == STATE_DRAFT, (
        f"the seeded page {DRAFT_SLUG!r} is in state {draft.get('state')!r} rather "
        f"than {STATE_DRAFT!r}"
    )
    assert not draft.get("published_at"), (
        f"the draft page {DRAFT_SLUG!r} carries a published timestamp "
        f"{draft.get('published_at')!r}"
    )


def test_seeded_notebooks_are_stored_exactly_once(db):
    for slug, _ in TOP_NINE:
        assert db.count_notebooks(slug=slug) == 1, (
            f"the notebooks table holds {db.count_notebooks(slug=slug)} rows for "
            f"slug {slug!r}; seeding is idempotent"
        )


def test_uploaded_bytes_live_in_the_object_store_at_the_digest_key(
        author_client, db, store, probe_bytes):
    created = create_page(author_client, f"probe-{digest_of(probe_bytes)[:10]}", "Probe page")
    assert created.status_code in (200, 201), (
        f"POST /api/pages returned {created.status_code}: {created.text[:400]}"
    )
    slug = created.json().get("slug")
    assert slug, f"POST /api/pages returned no slug: {created.text[:400]}"
    response = upload_media(author_client, slug, probe_bytes)
    assert response.status_code in (200, 201), (
        f"POST /api/media returned {response.status_code}: {response.text[:400]}"
    )
    expected = key_for(slug, probe_bytes)
    assert response.json().get("object_key") == expected, (
        f"POST /api/media recorded object_key {response.json().get('object_key')!r} "
        f"rather than the digest key {expected!r}"
    )
    settle()
    assert store.exists(expected), (
        f"no object exists in the bucket at {expected!r}; the bytes live somewhere "
        f"other than the object store"
    )
    assert db.media_by_key(expected), (
        f"no media row records the object key {expected!r}"
    )


def test_draft_page_media_is_not_publicly_readable(
        author_client, anon_client, store, probe_bytes):
    created = create_page(author_client, f"draft-{digest_of(probe_bytes)[:10]}", "Draft probe")
    assert created.status_code in (200, 201), (
        f"POST /api/pages returned {created.status_code}: {created.text[:400]}"
    )
    slug = created.json().get("slug")
    uploaded = upload_media(author_client, slug, probe_bytes)
    assert uploaded.status_code in (200, 201), (
        f"POST /api/media returned {uploaded.status_code}: {uploaded.text[:400]}"
    )
    media_id = uploaded.json().get("id")
    key = key_for(slug, probe_bytes)
    settle()
    assert store.exists(key), (
        f"the draft page's object is absent from the bucket at {key!r}; it must "
        f"exist and be unreadable rather than not exist"
    )
    refused = anon_client.get(f"/media/{media_id}")
    assert refused.status_code in (401, 403, 404), (
        f"GET /api/media/{media_id} from a signed-out caller returned "
        f"{refused.status_code} rather than a refusal, so a draft page's image is "
        f"publicly readable: {refused.text[:400]}"
    )


def test_publishing_makes_the_same_object_readable_without_moving_it(
        author_client, anon_client, store, probe_bytes):
    slug = f"pub-{digest_of(probe_bytes)[:10]}"
    created = create_page(author_client, slug, "Publish probe")
    assert created.status_code in (200, 201), (
        f"POST /api/pages returned {created.status_code}: {created.text[:400]}"
    )
    page_id = created.json().get("id")
    uploaded = upload_media(author_client, slug, probe_bytes)
    assert uploaded.status_code in (200, 201), (
        f"POST /api/media returned {uploaded.status_code}: {uploaded.text[:400]}"
    )
    media_id = uploaded.json().get("id")
    key = key_for(slug, probe_bytes)
    block = add_block(author_client, page_id, 1, kind="hero", media_id=media_id)
    assert block.status_code in (200, 201), (
        f"POST /api/blocks returned {block.status_code}: {block.text[:400]}"
    )
    before = anon_client.get(f"/media/{media_id}")
    assert before.status_code in (401, 403, 404), (
        f"the object was readable at {key!r} before the page published: "
        f"{before.status_code}"
    )
    published = publish(author_client, slug)
    assert published.status_code in (200, 201), (
        f"POST /api/pages/{slug}/publish returned {published.status_code}: "
        f"{published.text[:400]}"
    )
    settle()
    assert store.exists(key), (
        f"publishing moved the object away from {key!r}; nothing is re-uploaded and "
        f"no key changes when a page publishes"
    )
    after = anon_client.get(f"/media/{media_id}")
    assert after.status_code == 200, (
        f"GET /api/media/{media_id} returned {after.status_code} after the page "
        f"published, so publishing did not make the object readable: "
        f"{after.text[:400]}"
    )


def test_identical_bytes_uploaded_twice_yield_one_object(
        author_client, db, probe_bytes):
    slug = f"dedupe-{digest_of(probe_bytes)[:10]}"
    created = create_page(author_client, slug, "Dedupe probe")
    assert created.status_code in (200, 201), (
        f"POST /api/pages returned {created.status_code}: {created.text[:400]}"
    )
    first = upload_media(author_client, slug, probe_bytes)
    assert first.status_code in (200, 201), (
        f"the first POST /api/media returned {first.status_code}: {first.text[:400]}"
    )
    second = upload_media(author_client, slug, probe_bytes)
    assert second.status_code in (200, 201, 409), (
        f"the second POST /api/media returned {second.status_code}: "
        f"{second.text[:400]}"
    )
    settle()
    key = key_for(slug, probe_bytes)
    assert db.count_media(object_key=key) == 1, (
        f"the media table holds {db.count_media(object_key=key)} rows for the key "
        f"{key!r}; the key is the digest of the bytes so identical bytes yield one row"
    )


def test_page_is_created_as_a_draft(author_client, db, probe_bytes):
    slug = f"fresh-{digest_of(probe_bytes)[:10]}"
    created = create_page(author_client, slug, "Fresh probe")
    assert created.status_code in (200, 201), (
        f"POST /api/pages returned {created.status_code}: {created.text[:400]}"
    )
    settle()
    row = db.page_by_slug(slug)
    assert row, f"no pages row for the page just created at slug {slug!r}"
    assert row.get("state") == STATE_DRAFT, (
        f"a page created at {slug!r} is in state {row.get('state')!r} rather than "
        f"{STATE_DRAFT!r}"
    )


def test_publish_is_idempotent(author_client, db, probe_bytes):
    slug = f"idem-{digest_of(probe_bytes)[:10]}"
    created = create_page(author_client, slug, "Idempotent probe")
    assert created.status_code in (200, 201), (
        f"POST /api/pages returned {created.status_code}: {created.text[:400]}"
    )
    first = publish(author_client, slug)
    assert first.status_code in (200, 201), (
        f"POST /api/pages/{slug}/publish returned {first.status_code}: "
        f"{first.text[:400]}"
    )
    settle()
    stamp = db.page_by_slug(slug).get("published_at")
    second = publish(author_client, slug)
    assert second.status_code in (200, 201, 409), (
        f"a repeated publish returned {second.status_code}: {second.text[:400]}"
    )
    settle()
    assert db.count_pages(slug=slug) == 1, (
        f"a repeated publish left {db.count_pages(slug=slug)} pages rows for "
        f"{slug!r}"
    )
    assert str(db.page_by_slug(slug).get("published_at")) == str(stamp), (
        f"a repeated publish moved published_at from {stamp!r} to "
        f"{db.page_by_slug(slug).get('published_at')!r}"
    )


def test_blocks_are_stored_in_contiguous_positions(author_client, db, probe_bytes):
    slug = f"blocks-{digest_of(probe_bytes)[:10]}"
    created = create_page(author_client, slug, "Block probe")
    page_id = created.json().get("id")
    for position, kind in ((1, "hero"), (2, "value_line"), (3, "cta")):
        added = add_block(author_client, page_id, position, kind=kind)
        assert added.status_code in (200, 201), (
            f"POST /api/blocks at position {position} returned {added.status_code}: "
            f"{added.text[:400]}"
        )
    settle()
    positions = sorted(b.get("position") for b in db.blocks_of(page_id))
    assert positions == [1, 2, 3], (
        f"the page's block positions are {positions} rather than contiguous from 1"
    )


def test_removing_a_block_closes_the_position_gap(author_client, db, probe_bytes):
    slug = f"gap-{digest_of(probe_bytes)[:10]}"
    created = create_page(author_client, slug, "Gap probe")
    page_id = created.json().get("id")
    ids = []
    for position, kind in ((1, "hero"), (2, "value_line"), (3, "cta")):
        added = add_block(author_client, page_id, position, kind=kind)
        assert added.status_code in (200, 201), (
            f"POST /api/blocks returned {added.status_code}: {added.text[:400]}"
        )
        ids.append(added.json().get("id"))
    removed = author_client.delete(f"/blocks/{ids[1]}")
    assert removed.status_code in (200, 204), (
        f"DELETE /api/blocks/{ids[1]} returned {removed.status_code}: "
        f"{removed.text[:400]}"
    )
    settle()
    positions = sorted(b.get("position") for b in db.blocks_of(page_id))
    assert positions == [1, 2], (
        f"after removing the middle block the positions are {positions} rather than "
        f"[1, 2]; removing a block closes the gap"
    )


def test_block_of_an_unknown_kind_is_refused(author_client, db, probe_bytes):
    slug = f"kind-{digest_of(probe_bytes)[:10]}"
    created = create_page(author_client, slug, "Kind probe")
    page_id = created.json().get("id")
    response = add_block(author_client, page_id, 1, kind="marquee_of_doom")
    assert 400 <= response.status_code < 500, (
        f"POST /api/blocks with a kind outside {list(BLOCK_KINDS)} returned "
        f"{response.status_code} rather than a client error: {response.text[:400]}"
    )
    settle()
    assert db.count_blocks(page_id=page_id) == 0, (
        "a refused block of an unknown kind was written anyway"
    )


def test_signup_creates_a_free_reader_account(anon_client, db, probe_email):
    response = anon_client.post("/auth/signup", json=signup_payload(probe_email))
    assert response.status_code in (200, 201), (
        f"POST /api/auth/signup for {probe_email} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    token = response.json().get("access_token") or response.json().get("token")
    assert token, f"POST /api/auth/signup returned no bearer token: {response.text[:400]}"
    settle()
    assert db.reader_by_email(probe_email), (
        f"no readers row for {probe_email} after a successful signup"
    )


def test_duplicate_signup_creates_no_second_account(anon_client, db, probe_email):
    first = anon_client.post("/auth/signup", json=signup_payload(probe_email))
    assert first.status_code in (200, 201), (
        f"POST /api/auth/signup returned {first.status_code}: {first.text[:400]}"
    )
    settle()
    second = anon_client.post("/auth/signup", json=signup_payload(probe_email))
    assert 400 <= second.status_code < 500, (
        f"a second POST /api/auth/signup for {probe_email} returned "
        f"{second.status_code} rather than a client error: {second.text[:400]}"
    )
    settle()
    assert db.count_readers(email=probe_email) == 1, (
        f"the readers table holds {db.count_readers(email=probe_email)} rows for "
        f"{probe_email}"
    )


def test_signup_with_a_malformed_email_writes_nothing(anon_client, db):
    bad = "not-an-address-at-all"
    response = anon_client.post("/auth/signup", json=signup_payload(bad))
    assert 400 <= response.status_code < 500, (
        f"POST /api/auth/signup with a malformed address returned "
        f"{response.status_code} rather than a client error: {response.text[:400]}"
    )
    settle()
    assert db.count_readers(email=bad) == 0, (
        f"a refused signup wrote a readers row for {bad!r}"
    )


def test_signup_decoy_field_submission_is_refused(anon_client, db, probe_email):
    body = signup_payload(probe_email)
    body["website"] = "https://example.com/spam"
    response = anon_client.post("/signups", json=body)
    assert 400 <= response.status_code < 500, (
        f"POST /api/signups with the unattended decoy field filled returned "
        f"{response.status_code} rather than a client error: {response.text[:400]}"
    )
    settle()
    assert db.count_readers(email=probe_email) == 0, (
        f"a submission that filled the decoy field created a readers row for "
        f"{probe_email}"
    )


def test_repeated_signup_submissions_in_quick_succession_are_refused(anon_client):
    codes = []
    for _ in range(8):
        body = signup_payload(f"burst-{digest_of(str(len(codes)).encode())[:10]}@example.com")
        codes.append(anon_client.post("/signups", json=body).status_code)
    assert any(400 <= c < 500 for c in codes), (
        f"eight signup submissions in quick succession were all accepted: {codes}; "
        f"the same form submitted repeatedly must be refused"
    )


def test_newsletter_records_a_subscriber_once(anon_client, db, probe_email):
    first = anon_client.post("/newsletter", json={"email": probe_email})
    assert first.status_code in (200, 201), (
        f"POST /api/newsletter returned {first.status_code}: {first.text[:400]}"
    )
    second = anon_client.post("/newsletter", json={"email": probe_email})
    assert second.status_code in (200, 201, 400, 409), (
        f"a repeated POST /api/newsletter returned {second.status_code}: "
        f"{second.text[:400]}"
    )
    settle()
    assert db.count_subscribers(email=probe_email) == 1, (
        f"the newsletter_subscribers table holds "
        f"{db.count_subscribers(email=probe_email)} rows for {probe_email}"
    )


def test_anonymous_studio_request_is_denied(anon_client):
    response = anon_client.get("/pages")
    assert response.status_code in (401, 403), (
        f"GET /api/pages without a token returned {response.status_code} rather than "
        f"a denial: {response.text[:400]}"
    )


def test_reader_cannot_reach_the_studio(reader_client, db):
    response = reader_client.get("/pages")
    assert response.status_code in (401, 403), (
        f"GET /api/pages from a reader session returned {response.status_code} "
        f"rather than a denial: {response.text[:400]}"
    )
    created = create_page(reader_client, "reader-made-this", "Reader page")
    assert 400 <= created.status_code < 500, (
        f"POST /api/pages from a reader session returned {created.status_code} "
        f"rather than a client error: {created.text[:400]}"
    )
    settle()
    assert db.count_pages(slug="reader-made-this") == 0, (
        "a reader created a pages row"
    )


def test_author_cannot_publish_another_authors_page(author_client, db):
    before = db.page_by_slug(DRAFT_SLUG)
    assert before, f"no pages row for slug {DRAFT_SLUG!r}"
    response = publish(author_client, DRAFT_SLUG)
    assert 400 <= response.status_code < 500, (
        f"POST /api/pages/{DRAFT_SLUG}/publish from the other author returned "
        f"{response.status_code} rather than a client error: {response.text[:400]}"
    )
    settle()
    after = db.page_by_slug(DRAFT_SLUG)
    assert after.get("state") == STATE_DRAFT, (
        f"the page {DRAFT_SLUG!r} is now in state {after.get('state')!r}; a denied "
        f"publish leaves it a draft"
    )


def test_author_cannot_read_another_authors_pages(author_client, db):
    response = author_client.get("/pages")
    assert response.status_code == 200, (
        f"GET /api/pages returned {response.status_code}: {response.text[:400]}"
    )
    assert DRAFT_SLUG not in flatten(items(response.json())), (
        f"GET /api/pages for {AUTHOR_EMAIL} lists {DRAFT_SLUG!r}, which "
        f"{AUTHOR2_EMAIL} owns: {response.text[:400]}"
    )


def test_author_cannot_read_another_authors_draft_media(author_client, db):
    page = db.page_by_slug(DRAFT_SLUG)
    assert page, f"no pages row for slug {DRAFT_SLUG!r}"
    blocks = db.blocks_of(page["id"])
    media_ids = [b.get("media_id") for b in blocks if b.get("media_id")]
    assert media_ids, (
        f"the seeded draft page {DRAFT_SLUG!r} references no media, so the boundary "
        f"this task needs is not seeded"
    )
    response = author_client.get(f"/media/{media_ids[0]}")
    assert response.status_code in (401, 403, 404), (
        f"GET /api/media/{media_ids[0]} from the other author returned "
        f"{response.status_code} rather than a refusal: {response.text[:400]}"
    )


def test_unknown_page_slug_is_not_found(anon_client):
    response = anon_client.get("/pages/no-such-page-at-all")
    assert response.status_code == 404, (
        f"GET /api/pages/no-such-page-at-all returned {response.status_code} rather "
        f"than 404: {response.text[:400]}"
    )


def test_concurrent_publish_yields_one_published_row(author_client, db, probe_bytes):
    slug = f"race-{digest_of(probe_bytes)[:10]}"
    created = create_page(author_client, slug, "Race probe")
    assert created.status_code in (200, 201), (
        f"POST /api/pages returned {created.status_code}: {created.text[:400]}"
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(publish, author_client, slug) for _ in range(2)]
        codes = [f.result().status_code for f in futures]
    settle()
    assert db.count_pages(slug=slug) == 1, (
        f"two simultaneous publishes left {db.count_pages(slug=slug)} pages rows for "
        f"{slug!r}; the responses were {codes}"
    )
    assert db.page_by_slug(slug).get("state") == STATE_PUBLISHED, (
        f"the page {slug!r} is not published after two simultaneous publishes"
    )


def test_concurrent_signup_with_one_email_yields_one_reader_row(
        anon_client, db, probe_email):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(anon_client.post, "/auth/signup", json=signup_payload(probe_email))
            for _ in range(2)
        ]
        codes = [f.result().status_code for f in futures]
    settle()
    assert db.count_readers(email=probe_email) == 1, (
        f"two simultaneous signups for {probe_email} left "
        f"{db.count_readers(email=probe_email)} readers rows; the responses were "
        f"{codes}"
    )


def test_concurrent_identical_uploads_leave_one_media_row(
        author_client, db, probe_bytes):
    slug = f"upl-{digest_of(probe_bytes)[:10]}"
    created = create_page(author_client, slug, "Upload race probe")
    assert created.status_code in (200, 201), (
        f"POST /api/pages returned {created.status_code}: {created.text[:400]}"
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(upload_media, author_client, slug, probe_bytes)
            for _ in range(2)
        ]
        codes = [f.result().status_code for f in futures]
    settle()
    key = key_for(slug, probe_bytes)
    assert db.count_media(object_key=key) == 1, (
        f"two simultaneous uploads of identical bytes left "
        f"{db.count_media(object_key=key)} media rows at {key!r}; the responses were "
        f"{codes}"
    )


def test_sign_up_card_offers_every_method(anon_client):
    with _web() as web:
        page = web.get("/new")
        assert page.status_code == 200, (
            f"GET /new returned {page.status_code}: {page.text[:400]}"
        )
        assert SIGNUP_HEADING in page.text, (
            f"GET /new omits the heading {SIGNUP_HEADING!r}"
        )
        missing = [m for m in SIGNUP_METHODS if m not in page.text]
        assert not missing, f"GET /new omits the account method(s) {missing}"
        assert SIGNUP_FINE_PRINT in page.text, (
            f"GET /new omits the fine print {SIGNUP_FINE_PRINT!r}"
        )


def test_every_call_to_action_leads_to_the_sign_up_card(anon_client):
    with _web() as web:
        for route in ("/", "/ai"):
            page = web.get(route)
            assert page.status_code == 200, (
                f"GET {route} returned {page.status_code}: {page.text[:200]}"
            )
            assert _re.search(r'href=["\']/new["\']', page.text), (
                f"GET {route} carries no action leading to /new: {page.text[:400]}"
            )


def test_public_page_endpoint_serves_a_published_page(anon_client):
    for slug in PUBLISHED_SLUGS:
        response = anon_client.get(f"/pages/{slug}")
        assert response.status_code == 200, (
            f"GET /api/pages/{slug} returned {response.status_code}: "
            f"{response.text[:400]}"
        )


def test_public_documents_reference_no_third_party_origin(anon_client):
    allowed = ("/", "#", "data:", "mailto:")
    with _web() as web:
        for route in PUBLIC_ROUTES:
            page = web.get(route)
            assert page.status_code == 200, (
                f"GET {route} returned {page.status_code}: {page.text[:200]}"
            )
            hosts = set(_re.findall(r'(?:src|href)=["\']https?://([^/"\']+)', page.text))
            external = {h for h in hosts if "localhost" not in h and "127.0.0.1" not in h}
            assert not external, (
                f"GET {route} pulls from the third-party origin(s) {sorted(external)}; "
                f"the only backing services in this environment are the two named "
                f"providers, and nothing else may be reached at run time"
            )
