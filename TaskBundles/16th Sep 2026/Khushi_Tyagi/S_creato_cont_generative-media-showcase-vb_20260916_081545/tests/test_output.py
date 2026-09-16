"""Black-box checks for deku/generative-media-showcase-vb.

Every assertion is made over HTTP against the running app, against the database
the app writes, or against the object store the app uploads to. Nothing imports
the agent's code, reads the agent's files, or assumes a framework.

The spine of the bundle is the draft boundary: an unpublished item and the bytes
of its poster must both be unreachable, and the refusal must be the same refusal
a caller gets for something that never existed.
"""

from __future__ import annotations

import re

from conftest import (
    AUTHOR2_EMAIL, AUTHOR_EMAIL, CORPUS_PASSWORD, DRAFT_SLUG, KEY_SCHEME,
    MISSING_SLUG, MODEL_PRICES_MINOR, MODEL_SPEC_FIELDS, OTHER_DRAFT_SLUG,
    PUBLIC_ROUTES, SECURITY_HEADERS, SMALLEST_PNG, STUDIO_ENDPOINTS,
    attach_poster, base_url, comparable, create_draft, fetch_media, item_by_slug,
    media_key_of, probe_email, probe_key, probe_slug, public_news, publish,
    settle, sha256_hex, studio_news, unpublish,
)
from _shapes import flatten
from appclient import client, login

HREF_RE = re.compile(r'href="(/[^"#?]*)"')
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
ALT_RE = re.compile(r'\balt\s*=\s*"', re.IGNORECASE)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
DESCRIPTION_RE = re.compile(
    r'<meta[^>]+name="description"[^>]+content="([^"]*)"', re.IGNORECASE)




def test_signup_creates_an_account_that_can_then_sign_in(anon_client):
    email = probe_email("newcomer")
    r = anon_client.post("/api/auth/signup", json={
        "email": email, "password": "a-long-enough-password",
        "idempotency_key": probe_key("signup")})
    assert r.status_code in (200, 201), (
        f"POST /api/auth/signup returned {r.status_code}, expected 201; "
        f"body={r.text[:300]}")
    body = r.json()
    assert str(body.get("email", "")).lower() == email, (
        f"the signup response names {body.get('email')!r}, expected {email!r}")

    token = login(email, "a-long-enough-password")
    assert token, f"the account created at {email!r} cannot sign in afterwards"


def test_a_repeated_signup_under_one_idempotency_key_creates_one_account(
        anon_client, backend):
    email = probe_email("twice")
    key = probe_key("signup-replay")
    payload = {"email": email, "password": "a-long-enough-password",
               "idempotency_key": key}

    first = anon_client.post("/api/auth/signup", json=payload)
    assert first.status_code in (200, 201), (
        f"the first signup returned {first.status_code}; body={first.text[:300]}")
    second = anon_client.post("/api/auth/signup", json=payload)
    assert second.status_code in (200, 201, 409), (
        f"the replayed signup returned {second.status_code}; body={second.text[:300]}")

    rows = backend.rows("account", email=email)
    assert len(rows) == 1, (
        f"the replayed signup under key {key!r} stored {len(rows)} account rows for "
        f"{email!r}, expected exactly 1")


def test_a_duplicate_email_is_refused_without_confirming_the_address(anon_client):
    r = anon_client.post("/api/auth/signup", json={
        "email": AUTHOR_EMAIL, "password": "a-long-enough-password",
        "idempotency_key": probe_key("duplicate")})
    assert r.status_code in (400, 409, 422), (
        f"signing up under the seeded address {AUTHOR_EMAIL!r} returned "
        f"{r.status_code}, expected a 4xx refusal; body={r.text[:300]}")
    said = r.text.lower()
    for leak in ("already registered", "already exists", "taken"):
        assert leak not in said, (
            f"the duplicate-address refusal says {leak!r}, which confirms the "
            f"address belongs to somebody; body={r.text[:300]}")


def test_a_short_password_is_refused_and_names_the_field(anon_client):
    r = anon_client.post("/api/auth/signup", json={
        "email": probe_email("short"), "password": "abc",
        "idempotency_key": probe_key("short")})
    assert r.status_code in (400, 422), (
        f"a three character password returned {r.status_code}, expected a 4xx "
        f"refusal; body={r.text[:300]}")
    assert "password" in r.text.lower(), (
        f"the refusal does not name the password field; body={r.text[:300]}")




def test_a_created_item_is_stored_as_a_draft_owned_by_its_author(
        author_client, backend):
    slug = probe_slug("draft")
    created = create_draft(author_client, slug)
    assert str(created.get("status")) == "draft", (
        f"a freshly created item reports status {created.get('status')!r}, "
        f"expected 'draft'")

    rows = backend.rows("content_item", slug=slug)
    assert len(rows) == 1, (
        f"the database holds {len(rows)} rows for slug {slug!r}, expected 1")
    assert str(rows[0].get("status")) == "draft", (
        f"the stored row for {slug!r} reports status {rows[0].get('status')!r}, "
        f"expected 'draft'")


def test_a_draft_does_not_appear_on_the_public_listing(author_client, anon_client):
    slug = probe_slug("unlisted")
    create_draft(author_client, slug)
    settle()

    slugs = [str(row.get("slug")) for row in public_news(anon_client)]
    assert slug not in slugs, (
        f"the public listing exposes the draft {slug!r}; it listed {slugs}")
    assert DRAFT_SLUG not in slugs, (
        f"the public listing exposes the seeded draft {DRAFT_SLUG!r}")


def test_an_anonymous_request_for_a_draft_matches_a_request_for_a_missing_slug(
        anon_client):
    draft = anon_client.get(f"/api/news/{DRAFT_SLUG}")
    missing = anon_client.get(f"/api/news/{MISSING_SLUG}")
    assert draft.status_code == 404, (
        f"an anonymous request for the draft {DRAFT_SLUG!r} returned "
        f"{draft.status_code}, expected 404; body={draft.text[:300]}")
    assert comparable(draft) == comparable(missing), (
        f"the draft answers {comparable(draft)} while a slug that never existed "
        f"answers {comparable(missing)}; a caller can tell the two apart")


def test_a_reader_session_gets_the_same_refusal_for_a_draft(reader_client):
    draft = reader_client.get(f"/api/news/{DRAFT_SLUG}")
    missing = reader_client.get(f"/api/news/{MISSING_SLUG}")
    assert draft.status_code == 404, (
        f"a reader session reading the draft {DRAFT_SLUG!r} got "
        f"{draft.status_code}, expected 404; body={draft.text[:300]}")
    assert comparable(draft) == comparable(missing), (
        f"for a reader the draft answers {comparable(draft)} while a missing slug "
        f"answers {comparable(missing)}")


def test_an_author_cannot_read_another_authors_draft(author_client):
    other = author_client.get(f"/api/news/{OTHER_DRAFT_SLUG}")
    missing = author_client.get(f"/api/news/{MISSING_SLUG}")
    assert other.status_code == 404, (
        f"the first author reading {OTHER_DRAFT_SLUG!r}, owned by {AUTHOR2_EMAIL}, "
        f"got {other.status_code}, expected 404; body={other.text[:300]}")
    assert comparable(other) == comparable(missing), (
        f"another author's draft answers {comparable(other)} while a missing slug "
        f"answers {comparable(missing)}")


def test_an_author_cannot_publish_another_authors_item(author_client, author2_client,
                                                       backend):
    owned = item_by_slug(studio_news(author2_client), OTHER_DRAFT_SLUG)
    assert owned is not None, (
        f"the seeded draft {OTHER_DRAFT_SLUG!r} is not in {AUTHOR2_EMAIL}'s own list")

    r = publish(author_client, owned.get("id"))
    assert r.status_code in (403, 404), (
        f"the first author publishing {AUTHOR2_EMAIL}'s item returned "
        f"{r.status_code}, expected 403 or 404; body={r.text[:300]}")

    rows = backend.rows("content_item", slug=OTHER_DRAFT_SLUG)
    assert rows and str(rows[0].get("status")) == "draft", (
        f"after the refused publish {OTHER_DRAFT_SLUG!r} reports status "
        f"{rows[0].get('status') if rows else None!r}, expected 'draft'")




def test_an_uploaded_poster_exists_in_the_object_store_under_the_pinned_key_scheme(
        author_client, store):
    created = create_draft(author_client, probe_slug("stored"))
    r = attach_poster(author_client, created.get("id"))
    assert r.status_code in (200, 201), (
        f"attaching a poster returned {r.status_code}, expected 201; "
        f"body={r.text[:300]}")

    key = media_key_of(r.json())
    assert KEY_SCHEME.match(key), (
        f"the stored key {key!r} does not follow media/{{item_id}}/"
        f"{{sha256_of_bytes}}.{{ext}}")
    assert store.exists(key), (
        f"the object store holds nothing at {key!r}; the bytes are somewhere else")


def test_the_stored_object_key_carries_the_checksum_of_the_uploaded_bytes(
        author_client):
    created = create_draft(author_client, probe_slug("checksum"))
    r = attach_poster(author_client, created.get("id"))
    assert r.status_code in (200, 201), (
        f"attaching a poster returned {r.status_code}; body={r.text[:300]}")

    key = media_key_of(r.json())
    digest = key.rsplit("/", 1)[1].rsplit(".", 1)[0]
    assert digest == sha256_hex(SMALLEST_PNG), (
        f"the key carries checksum {digest!r} but the uploaded bytes hash to "
        f"{sha256_hex(SMALLEST_PNG)!r}")


def test_a_draft_poster_key_is_refused_for_an_anonymous_caller(author_client,
                                                               anon_client):
    created = create_draft(author_client, probe_slug("private"))
    r = attach_poster(author_client, created.get("id"))
    assert r.status_code in (200, 201), (
        f"attaching a poster returned {r.status_code}; body={r.text[:300]}")
    key = media_key_of(r.json())

    refused = fetch_media(anon_client, key)
    unknown = fetch_media(anon_client, "media/0/" + ("0" * 64) + ".png")
    assert refused.status_code == 404, (
        f"an anonymous fetch of the draft poster key {key!r} returned "
        f"{refused.status_code}, expected 404; body={refused.text[:300]}")
    assert comparable(refused) == comparable(unknown), (
        f"the private key answers {comparable(refused)} while a key that never "
        f"existed answers {comparable(unknown)}")


def test_a_refused_media_fetch_leaves_the_object_in_the_store(author_client,
                                                              anon_client, store):
    created = create_draft(author_client, probe_slug("intact"))
    r = attach_poster(author_client, created.get("id"))
    key = media_key_of(r.json())

    fetch_media(anon_client, key)
    settle()
    assert store.exists(key), (
        f"the object at {key!r} disappeared from the store after a refused fetch")


def test_an_upload_whose_bytes_contradict_its_declared_type_is_refused(author_client,
                                                                      store):
    created = create_draft(author_client, probe_slug("liar"))
    before = set(store.list("media/"))
    r = attach_poster(author_client, created.get("id"),
                      payload=b"this is not an image at all",
                      declared_type="image/webp", filename="poster.webp")
    assert r.status_code in (400, 415, 422), (
        f"an upload whose bytes are not an image returned {r.status_code}, "
        f"expected a 4xx refusal; body={r.text[:300]}")
    settle()
    assert set(store.list("media/")) == before, (
        "the refused upload still wrote an object to the store")




def test_publishing_makes_the_item_readable_and_its_poster_fetchable_together(
        author_client, anon_client):
    slug = probe_slug("live")
    created = create_draft(author_client, slug)
    key = media_key_of(attach_poster(author_client, created.get("id")).json())

    assert anon_client.get(f"/api/news/{slug}").status_code == 404, (
        f"{slug!r} is readable before it was published")
    assert fetch_media(anon_client, key).status_code == 404, (
        f"the poster at {key!r} is fetchable before its item was published")

    r = publish(author_client, created.get("id"))
    assert r.status_code == 200, (
        f"publishing returned {r.status_code}, expected 200; body={r.text[:300]}")
    settle()

    assert anon_client.get(f"/api/news/{slug}").status_code == 200, (
        f"{slug!r} is still unreadable after publication")
    assert fetch_media(anon_client, key).status_code == 200, (
        f"the poster at {key!r} is still unfetchable after publication, so the "
        f"item published without its bytes")


def test_unpublishing_hides_the_item_and_its_poster_together(author_client,
                                                             anon_client):
    slug = probe_slug("retract")
    created = create_draft(author_client, slug)
    key = media_key_of(attach_poster(author_client, created.get("id")).json())
    assert publish(author_client, created.get("id")).status_code == 200
    settle()

    r = unpublish(author_client, created.get("id"))
    assert r.status_code == 200, (
        f"unpublishing returned {r.status_code}, expected 200; body={r.text[:300]}")
    settle()

    assert anon_client.get(f"/api/news/{slug}").status_code == 404, (
        f"{slug!r} is still readable after it was unpublished")
    assert fetch_media(anon_client, key).status_code == 404, (
        f"the poster at {key!r} is still fetchable after its item was unpublished")


def test_publishing_one_item_changes_no_other_items_status(author_client, backend):
    before = {str(row.get("slug")): str(row.get("status"))
              for row in backend.rows("content_item")}
    created = create_draft(author_client, probe_slug("solo"))
    attach_poster(author_client, created.get("id"))
    assert publish(author_client, created.get("id")).status_code == 200
    settle()

    after = {str(row.get("slug")): str(row.get("status"))
             for row in backend.rows("content_item")}
    changed = {slug for slug, status in before.items()
               if after.get(slug) != status}
    assert not changed, (
        f"publishing one item also changed the status of {sorted(changed)}")


def test_publishing_without_alternative_text_is_refused_and_names_the_field(
        author_client, backend):
    slug = probe_slug("noalt")
    created = create_draft(author_client, slug)
    attach_poster(author_client, created.get("id"), alt_text="")

    r = publish(author_client, created.get("id"))
    assert r.status_code in (400, 409, 422), (
        f"publishing an item whose poster carries empty alternative text returned "
        f"{r.status_code}, expected a 4xx refusal; body={r.text[:300]}")
    assert "alt" in r.text.lower(), (
        f"the refusal does not name the alternative-text field; body={r.text[:300]}")

    rows = backend.rows("content_item", slug=slug)
    assert rows and str(rows[0].get("status")) == "draft", (
        f"{slug!r} is no longer a draft after the refused publish")




def test_a_reader_session_is_refused_every_studio_endpoint(reader_client):
    for method, path, body in STUDIO_ENDPOINTS:
        r = reader_client.request(method, path, json=body)
        assert r.status_code in (403, 404), (
            f"{method} {path} from a reader session returned {r.status_code}, "
            f"expected 403 or 404; body={r.text[:300]}")


def test_an_anonymous_caller_is_refused_every_studio_endpoint(anon_client):
    for method, path, body in STUDIO_ENDPOINTS:
        r = anon_client.request(method, path, json=body)
        assert r.status_code in (401, 403, 404), (
            f"{method} {path} without a session returned {r.status_code}, "
            f"expected 401, 403 or 404; body={r.text[:300]}")




def test_every_model_record_carries_every_spec_field(anon_client):
    r = anon_client.get("/api/models")
    assert r.status_code == 200, (
        f"GET /api/models returned {r.status_code}, expected 200; "
        f"body={r.text[:300]}")
    rows = r.json()
    rows = rows if isinstance(rows, list) else rows.get("items", [])
    names = {str(row.get("name")) for row in rows}
    assert set(MODEL_PRICES_MINOR) <= names, (
        f"the catalog exposes {sorted(names)}, missing "
        f"{sorted(set(MODEL_PRICES_MINOR) - names)}")
    for row in rows:
        missing = [f for f in MODEL_SPEC_FIELDS if not row.get(f)]
        assert not missing, (
            f"the model row {row.get('name')!r} carries no {missing}; a catalog "
            f"row with a hole in it cannot be compared")


def test_the_seeded_model_prices_are_stored_in_minor_units_per_second(backend):
    rows = {str(row.get("name")): row for row in backend.rows("model_spec")}
    for name, price in MODEL_PRICES_MINOR.items():
        assert name in rows, f"the database holds no model_spec row named {name!r}"
        got = rows[name].get("price_minor_per_second")
        assert int(got) == price, (
            f"{name!r} is stored at {got!r} minor units per second, expected {price}")




def test_the_home_document_carries_its_hero_and_switcher_copy_as_text(anon_client):
    r = anon_client.get("/")
    assert r.status_code == 200, (
        f"GET / returned {r.status_code}, expected 200")
    body = r.text
    for phrase in ("Building Real-World Intelligence", "Try Lumina for free",
                   "Lumina Creative", "Lumina Dev", "Lumina Robotics"):
        assert phrase in body, (
            f"the first response for / does not carry {phrase!r} as text, so the "
            f"document is filled in after it arrives")


def test_the_portal_document_carries_every_capability_column_and_model_row(
        anon_client):
    r = anon_client.get("/api-platform")
    assert r.status_code == 200, (
        f"GET /api-platform returned {r.status_code}, expected 200")
    body = r.text
    for phrase in ("Access", "Evaluate", "Automate", "Control",
                   "Nova-4.5", "Chisel-2.0", "Worldscape-1", "Perform-2"):
        assert phrase in body, (
            f"the first response for /api-platform does not carry {phrase!r}")


def test_the_connector_document_carries_every_accordion_answer(anon_client):
    r = anon_client.get("/mcp")
    assert r.status_code == 200, (
        f"GET /mcp returned {r.status_code}, expected 200")
    body = r.text
    for phrase in ("Frequently asked questions",
                   "What agents can connect to Lumina Connector?",
                   "Which models can agents use?",
                   "How are connector generations billed?",
                   "Is an API key required?"):
        assert phrase in body, (
            f"the first response for /mcp does not carry {phrase!r}, so an "
            f"in-page find cannot reach the answer")




def test_health_reports_the_database_and_the_store_separately(anon_client):
    r = anon_client.get("/api/health")
    assert r.status_code == 200, (
        f"GET /api/health returned {r.status_code}, expected 200; "
        f"body={r.text[:300]}")
    said = flatten(r.json()).lower()
    assert "database" in said or "db" in said, (
        f"the readiness body names no database state; body={r.text[:300]}")
    assert "storage" in said or "store" in said, (
        f"the readiness body names no object-store state; body={r.text[:300]}")


def test_the_news_listing_returns_a_top_level_array(anon_client):
    r = anon_client.get("/api/news")
    assert r.status_code == 200, (
        f"GET /api/news returned {r.status_code}, expected 200")
    assert isinstance(r.json(), list), (
        f"GET /api/news returned {type(r.json()).__name__}, expected a top-level "
        f"JSON array")


def test_an_unknown_address_renders_the_products_own_not_found_shell(anon_client):
    r = anon_client.get("/this-route-does-not-exist")
    assert r.status_code == 404, (
        f"an unknown address returned {r.status_code}, expected 404")
    body = r.text
    assert "Take me home" in body, (
        "the not-found response carries no way back to the home route")
    assert "Lumina" in body, (
        "the not-found response is not rendered inside the product's own chrome")


def test_every_public_route_carries_its_own_title_and_description(anon_client):
    seen = {}
    for route in PUBLIC_ROUTES:
        r = anon_client.get(route)
        assert r.status_code == 200, (
            f"GET {route} returned {r.status_code}, expected 200")
        title = TITLE_RE.search(r.text)
        description = DESCRIPTION_RE.search(r.text)
        assert title and title.group(1).strip(), f"{route} carries no title"
        assert description and description.group(1).strip(), (
            f"{route} carries no meta description")
        seen[route] = title.group(1).strip()
    assert len(set(seen.values())) > 1, (
        f"every public route shares one title {sorted(set(seen.values()))}")


def test_the_sitemap_lists_public_routes_and_omits_every_draft(anon_client):
    r = anon_client.get("/sitemap.xml")
    assert r.status_code == 200, (
        f"GET /sitemap.xml returned {r.status_code}, expected 200")
    body = r.text
    for route in ("/news", "/models", "/pricing"):
        assert route in body, f"the sitemap omits the public route {route}"
    assert DRAFT_SLUG not in body, (
        f"the sitemap carries the draft slug {DRAFT_SLUG!r}")
    assert OTHER_DRAFT_SLUG not in body, (
        f"the sitemap carries the draft slug {OTHER_DRAFT_SLUG!r}")

    robots = anon_client.get("/robots.txt")
    assert robots.status_code == 200, (
        f"GET /robots.txt returned {robots.status_code}, expected 200")
    assert "sitemap" in robots.text.lower(), (
        "robots.txt names no sitemap location")


def test_every_internal_link_on_the_public_routes_resolves(anon_client):
    broken = []
    for route in PUBLIC_ROUTES:
        page = anon_client.get(route)
        for href in sorted(set(HREF_RE.findall(page.text))):
            if href.startswith("//"):
                continue
            target = anon_client.get(href)
            if target.status_code >= 400:
                broken.append((route, href, target.status_code))
    assert not broken, f"these internal links lead nowhere: {broken}"


def test_every_content_image_carries_alternative_text(anon_client):
    missing = []
    for route in PUBLIC_ROUTES:
        page = anon_client.get(route)
        for tag in IMG_TAG_RE.findall(page.text):
            if not ALT_RE.search(tag):
                missing.append((route, tag[:120]))
    assert not missing, f"these images carry no alternative text: {missing}"




def test_no_store_credential_reaches_the_browser(anon_client):
    import os

    secrets = [os.environ.get("STORAGE_SECRET_KEY"),
               os.environ.get("STORAGE_ACCESS_KEY")]
    secrets = [s for s in secrets if s]
    assert secrets, (
        "the verifier holds no STORAGE_* credential, so this check cannot run")

    leaked = []
    for route in PUBLIC_ROUTES:
        page = anon_client.get(route)
        for secret in secrets:
            if secret in page.text:
                leaked.append(route)
    assert not leaked, (
        f"a store credential is served to the browser on {sorted(set(leaked))}")


def test_public_responses_carry_the_declared_security_headers(anon_client):
    r = anon_client.get("/")
    present = {name.lower() for name in r.headers}
    missing = [h for h in SECURITY_HEADERS if h not in present]
    assert not missing, (
        f"the home response carries no {missing}; it sent {sorted(present)}")
