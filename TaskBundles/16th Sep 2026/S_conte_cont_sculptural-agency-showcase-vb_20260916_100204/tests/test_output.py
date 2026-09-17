from __future__ import annotations

import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor

import httpx

import _shapes
import appclient
import conftest as fx


def test_health_route_answers_ready():
    """The health route answers once the app is ready."""
    response = httpx.get(f"{fx.api_base()}/health", timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code} rather than 200: {response.text[:300]}"
    )


def test_app_serves_pages_and_api_on_one_origin():
    """The app answers at its public address with the API on the same origin."""
    home = fx.page("/")
    assert home.status_code == 200, (
        f"GET / at {fx.app_url()} returned {home.status_code} rather than a page: {home.text[:300]}"
    )
    assert "Ironwood" in fx.visible_text(home.text), (
        "GET / did not render the home page wordmark 'Ironwood'"
    )
    services = httpx.get(f"{fx.api_base()}/services", timeout=fx.TIMEOUT)
    assert services.status_code == 200, (
        f"GET /api/services on the same origin returned {services.status_code}: {services.text[:300]}"
    )
    assert fx.api_base().startswith(fx.app_url()), (
        f"the API base {fx.api_base()} is not on the origin {fx.app_url()}"
    )


def test_every_public_route_answers():
    """Every public route the brief names answers with a rendered page."""
    failures = []
    for route in fx.PUBLIC_ROUTES:
        response = fx.page(route)
        if response.status_code != 200:
            failures.append((route, response.status_code))
    assert not failures, f"{len(failures)} public routes did not answer 200: {failures}"


def test_public_routes_render_without_client_code():
    """Every public route is complete in the HTML the server sends."""
    expected = (
        ("/", "Our culture, mantra, and beliefs"),
        ("/services", "Agency Services"),
        ("/works", "Lumen Pay"),
        ("/works/lumen-pay", "A payments app that settles an invoice in one tap"),
        ("/about-us", "Our journey"),
        ("/blog", "Shipping an MVP in eight weeks"),
        ("/blog/shipping-an-mvp-in-eight-weeks", "Shipping an MVP in eight weeks"),
        ("/blog-categories/engineering", "When to bring in a fractional CTO"),
        ("/contact", fx.CONTACT_HERO),
        ("/privacy-policy", "Privacy Policy"),
        ("/terms", "Terms of Service"),
    )
    missing = []
    for route, needle in expected:
        text = fx.page_text(route)
        if needle not in text:
            missing.append((route, needle))
    assert not missing, (
        f"these routes do not carry their content in the served HTML: {missing}"
    )


def test_production_build_serves_no_debug_page():
    """An unknown address never reveals a framework debug page."""
    response = fx.page(f"/no-such-page-{fx.unique_suffix()}")
    lowered = response.text.lower()
    for marker in ("traceback", "tried these url patterns", "debug = true", "page not found at"):
        assert marker not in lowered, (
            f"an unknown address served a debug page carrying {marker!r}: {response.text[:300]}"
        )


def test_user_readme_lists_every_seeded_account():
    """The credential file names every seeded account beside the pinned password."""
    with open("/app/USER_README.md", encoding="utf-8") as handle:
        text = handle.read()
    for email, _, _ in fx.SEEDED_ACCOUNTS:
        assert email in text, f"/app/USER_README.md does not name {email}"
    assert fx.CORPUS_PASSWORD in text, (
        f"/app/USER_README.md does not carry the password {fx.CORPUS_PASSWORD}"
    )


def test_reserved_directories_exist_and_are_empty():
    """The two reserved directories exist at the app root and hold nothing."""
    for name in (".browser_screenshots", ".downloads"):
        path = os.path.join("/app", name)
        assert os.path.isdir(path), f"/app/{name} does not exist at the app root"
        assert os.listdir(path) == [], f"/app/{name} is not empty; it holds {os.listdir(path)}"


def test_seeded_accounts_sign_in_with_the_corpus_password():
    """Each seeded account signs in with the pinned password and carries its role."""
    for email, role, display_name in fx.SEEDED_ACCOUNTS:
        body = fx.login_body(email)
        assert body.get("access_token"), f"POST /api/auth/login for {email} returned no access_token"
        user = body.get("user") or {}
        assert user.get("role") == role, (
            f"{email} signed in with role {user.get('role')!r} rather than {role!r}: {body}"
        )
        assert user.get("display_name") == display_name, (
            f"{email} signed in with display name {user.get('display_name')!r} rather than "
            f"{display_name!r}"
        )


def test_passwords_are_stored_as_hashes(backend):
    """No stored password digest equals the password itself."""
    rows = backend.query("SELECT email, password_digest FROM app_user WHERE email = %s",
                         (fx.EDITOR_EMAIL,))
    assert len(rows) == 1, f"app_user holds {len(rows)} rows for {fx.EDITOR_EMAIL}"
    digest = str(rows[0]["password_digest"])
    assert digest and fx.CORPUS_PASSWORD not in digest, (
        f"the password_digest for {fx.EDITOR_EMAIL} carries the plain password"
    )


def test_open_signup_creates_a_client():
    """An open signup creates a client account that can sign in again."""
    email, token, body = fx.register()
    user = body.get("user") or {}
    assert user.get("role") == "client", (
        f"POST /api/auth/sign-up created role {user.get('role')!r} rather than 'client': {body}"
    )
    for field in ("id", "email", "role", "display_name"):
        assert field in user, f"the sign-up response user lacks {field!r}: {body}"
    assert appclient.login(email, fx.CORPUS_PASSWORD), (
        f"the account {email} created by signup cannot sign in afterwards"
    )


def test_signup_never_creates_an_editor(backend):
    """A signup that asks for the editor role is still stored as a client."""
    email = fx.probe_email()
    response = httpx.post(
        f"{fx.api_base()}/auth/sign-up",
        json={"email": email, "password": fx.CORPUS_PASSWORD, "display_name": "Probe", "role": "editor"},
        timeout=fx.TIMEOUT,
    )
    assert response.status_code in (200, 201, 400, 422), (
        f"POST /api/auth/sign-up with a role field returned {response.status_code}: {response.text[:300]}"
    )
    rows = backend.query("SELECT role FROM app_user WHERE email = %s", (email,))
    assert all(row["role"] == "client" for row in rows), (
        f"a signup asking for the editor role stored {rows}"
    )


def test_duplicate_signup_is_refused_and_creates_no_row(backend):
    """A signup reusing an address is refused and writes no second row."""
    email, _, _ = fx.register()
    response = httpx.post(
        f"{fx.api_base()}/auth/sign-up",
        json={"email": email, "password": fx.CORPUS_PASSWORD, "display_name": "Second Claim"},
        timeout=fx.TIMEOUT,
    )
    assert fx.is_client_error(response.status_code), (
        f"POST /api/auth/sign-up reusing {email} returned {response.status_code}: {response.text[:300]}"
    )
    count = backend.count("app_user", email=email)
    assert count == 1, f"app_user holds {count} rows for {email} after a refused duplicate"


def test_protected_pages_redirect_signed_out_visitors():
    """A visitor with no session is sent to sign in from every protected page."""
    for route in fx.PROTECTED_ROUTES:
        response = fx.page(route)
        assert response.status_code in (301, 302, 303, 307, 308, 401, 403), (
            f"GET {route} while signed out returned {response.status_code}: {response.text[:200]}"
        )
        if response.status_code in (301, 302, 303, 307, 308):
            location = response.headers.get("location", "")
            assert "/sign-in" in location, (
                f"GET {route} while signed out redirected to {location!r} rather than /sign-in"
            )


def test_protected_endpoints_refuse_a_missing_token(guest):
    """Every write and the enquiry list refuse a request with no token."""
    attempts = (
        guest.post("/case-studies", json=fx.case_study_payload()),
        guest.post("/articles", json=fx.article_payload()),
        guest.patch("/case-studies/1", json={"title": "Changed"}),
        guest.post("/case-studies/1/publish"),
        guest.post("/articles/1/unpublish"),
        guest.patch("/enquiries/1", json={"state": "closed"}),
    )
    for response in attempts:
        assert fx.is_client_error(response.status_code), (
            f"{response.request.method} {response.request.url.path} with no token returned "
            f"{response.status_code}: {response.text[:200]}"
        )


def test_open_endpoints_answer_without_a_token(guest):
    """Public reads, the bot check and health answer with no token."""
    for path in ("/services", "/case-studies", "/case-studies/lumen-pay", "/articles",
                 "/articles/shipping-an-mvp-in-eight-weeks", "/article-categories", "/bot-check",
                 "/health"):
        response = guest.get(path)
        assert response.status_code == 200, (
            f"GET /api{path} with no token returned {response.status_code}: {response.text[:200]}"
        )


def test_list_endpoints_return_top_level_arrays(guest):
    """Every list endpoint returns a top-level JSON array."""
    for path in ("/services", "/case-studies", "/articles", "/article-categories"):
        response = guest.get(path)
        assert response.status_code == 200, f"GET /api{path} returned {response.status_code}"
        assert isinstance(response.json(), list), (
            f"GET /api{path} returned {type(response.json()).__name__} rather than an array"
        )
    with fx.as_editor() as editor:
        response = editor.get("/enquiries")
        assert isinstance(response.json(), list), (
            f"GET /api/enquiries returned {type(response.json()).__name__} rather than an array"
        )


def test_services_endpoint_lists_the_eight_services(guest, backend):
    """The service list is the eight fixed services, stored as eight rows."""
    names = [item.get("name") for item in _shapes.items(guest.get("/services").json())]
    assert sorted(names) == sorted(fx.SERVICES), f"GET /api/services returned {names}"
    assert backend.count("service") == 8, f"the service table holds {backend.count('service')} rows"


def test_schema_carries_the_pinned_tables(backend):
    """The datastore carries the pinned tables and their fields."""
    wanted = {
        "app_user": ("id", "email", "password_digest", "role", "display_name", "created_at"),
        "service": ("id", "name", "sort_order"),
        "case_study": ("id", "slug", "name", "label", "title", "subtitle", "summary", "body", "year",
                       "website_url", "owner_id", "state", "published_at", "sort_order", "created_at",
                       "updated_at"),
        "case_study_service": ("case_study_id", "service_id"),
        "article_category": ("id", "slug", "name", "sort_order"),
        "article": ("id", "slug", "title", "summary", "body", "category_id", "read_minutes", "owner_id",
                    "state", "published_at", "created_at", "updated_at"),
        "media_asset": ("id", "entry_kind", "entry_id", "object_key", "content_type", "byte_size",
                        "alt_text", "created_at"),
        "enquiry": ("id", "service", "budget", "name", "email", "message", "state", "client_id",
                    "created_at", "updated_at"),
        "bot_check_token": ("id", "token", "issued_at", "used_at"),
        "culture_value": ("id", "title", "body", "object_name", "sort_order"),
        "testimonial": ("id", "name", "role", "quote", "body", "sort_order"),
        "award_badge": ("id", "name", "link_url", "sort_order"),
        "client_logo": ("id", "name", "placement", "sort_order"),
        "team_member": ("id", "name", "role", "profile_url", "sort_order"),
        "office": ("id", "label", "street", "city", "phone", "sort_order"),
    }
    rows = backend.query(
        "SELECT table_name, column_name FROM information_schema.columns WHERE table_schema = 'public'"
    )
    present = {}
    for row in rows:
        present.setdefault(row["table_name"], set()).add(row["column_name"])
    for table, columns in wanted.items():
        assert table in present, f"the datastore has no table {table!r}"
        missing = [c for c in columns if c not in present[table]]
        assert not missing, f"table {table!r} lacks the columns {missing}"
    for derived in ("is_public", "is_visible", "visibility", "entry_count"):
        assert derived not in present.get("case_study", set()) | present.get("article_category", set()), (
            f"a derived value is stored as the column {derived!r}"
        )


def test_new_entries_are_stored_as_draft_rows(editor, backend):
    """A created case study and a created article are stored as draft rows."""
    case = fx.create_case_study(editor)
    article = fx.create_article(editor)
    case_rows = backend.query("SELECT state, published_at FROM case_study WHERE id = %s", (case["id"],))
    article_rows = backend.query("SELECT state, published_at FROM article WHERE id = %s", (article["id"],))
    assert case_rows and case_rows[0]["state"] == "draft" and case_rows[0]["published_at"] is None, (
        f"the created case study is stored as {case_rows}"
    )
    assert article_rows and article_rows[0]["state"] == "draft", (
        f"the created article is stored as {article_rows}"
    )


def test_invalid_slug_is_refused(editor, backend):
    """A slug that does not start with a letter is refused and writes nothing."""
    for bad in ("9-lives", "Upper-Case", "with space"):
        response = editor.post("/case-studies", json=fx.case_study_payload(slug=bad))
        assert fx.is_client_error(response.status_code), (
            f"POST /api/case-studies with slug {bad!r} returned {response.status_code}"
        )
        assert backend.count("case_study", slug=bad) == 0, f"a case study with slug {bad!r} was stored"


def test_published_case_study_is_readable_by_anyone(editor):
    """A published case study is readable by a visitor and a client."""
    record = fx.published_case_study(editor)
    assert record.get("state") == "published", f"publish returned {record}"
    stamp = str(record.get("published_at") or "")
    assert stamp and re.search(r"(Z|[+-]00:?00)$", stamp), (
        f"published_at {stamp!r} carries no UTC marker"
    )
    with fx.anonymous() as guest:
        response = guest.get(f"/case-studies/{record['slug']}")
        assert response.status_code == 200, (
            f"GET /api/case-studies/{record['slug']} as a visitor returned {response.status_code}"
        )
        assert response.json().get("title") == record["title"], "the served title differs from the stored one"
    with fx.as_client() as client:
        assert client.get(f"/case-studies/{record['slug']}").status_code == 200, (
            "a client cannot read a published case study"
        )
    page = fx.page(f"/works/{record['slug']}")
    assert page.status_code == 200 and record["name"] in fx.visible_text(page.text), (
        f"GET /works/{record['slug']} returned {page.status_code} without the client name"
    )


def test_case_study_record_carries_the_pinned_fields(guest):
    """A case study record carries every pinned field."""
    body = guest.get("/case-studies/lumen-pay").json()
    for field in ("id", "slug", "name", "label", "title", "subtitle", "summary", "body", "year",
                  "website_url", "services", "state", "published_at", "media"):
        assert field in body, f"GET /api/case-studies/lumen-pay lacks {field!r}: {str(body)[:300]}"
    assert sorted(body["services"]) == sorted(fx.LUMEN_PAY_SERVICES), (
        f"Lumen Pay carries services {body['services']}"
    )


def test_article_record_carries_the_pinned_fields(guest):
    """An article record carries every pinned field."""
    body = guest.get("/articles/shipping-an-mvp-in-eight-weeks").json()
    for field in ("id", "slug", "title", "summary", "body", "category", "read_minutes", "state",
                  "published_at", "media"):
        assert field in body, f"the article record lacks {field!r}: {str(body)[:300]}"
    category = body["category"]
    assert isinstance(category, dict) and category.get("slug") == "engineering" and category.get("name") == "Engineering", (
        f"the article category is {category!r}"
    )


def test_publish_adds_the_case_study_to_the_index_and_the_sitemap(editor):
    """Publishing appends the case study to the index and adds its sitemap address."""
    record = fx.published_case_study(editor)
    slugs = fx.index_slugs()
    assert slugs and slugs[-1] == record["slug"], (
        f"the newly published {record['slug']} is not the last index row: {slugs[-3:]}"
    )
    listing = [item.get("slug") for item in _shapes.items(httpx.get(f"{fx.api_base()}/case-studies", timeout=fx.TIMEOUT).json())]
    assert listing and listing[-1] == record["slug"], f"GET /api/case-studies ends with {listing[-3:]}"
    assert f"/works/{record['slug']}" in fx.sitemap_paths(), (
        f"/sitemap.xml does not list /works/{record['slug']}"
    )


def test_unpublish_withdraws_page_record_and_media(editor, store):
    """Unpublishing withdraws the page, the record, the image, the listing and the sitemap address."""
    record = fx.published_case_study(editor)
    asset = fx.upload(editor, "case-studies", record["id"])
    assert asset.status_code in (200, 201), f"upload returned {asset.status_code}: {asset.text[:300]}"
    asset_id = asset.json()["id"]
    withdrawn = fx.unpublish(editor, "case-studies", record["id"])
    assert withdrawn.status_code in (200, 201) and withdrawn.json().get("state") == "draft", (
        f"unpublish returned {withdrawn.status_code}: {withdrawn.text[:300]}"
    )
    with fx.anonymous() as guest:
        assert fx.is_client_error(guest.get(f"/case-studies/{record['slug']}").status_code), (
            "the withdrawn case study record is still served"
        )
        assert fx.is_client_error(guest.get(f"/media/{asset_id}/content").status_code), (
            "the withdrawn case study image is still served"
        )
    assert fx.is_client_error(fx.page(f"/works/{record['slug']}").status_code), (
        "the withdrawn case study page is still served"
    )
    assert record["slug"] not in fx.index_slugs(), "the withdrawn case study is still in the index"
    assert f"/works/{record['slug']}" not in fx.sitemap_paths(), "the withdrawn case study is still in the sitemap"
    assert store.exists(asset.json()["object_key"]), "unpublishing deleted the stored object"


def test_owning_editor_reads_the_draft_record_and_its_image(editor):
    """The owning editor reads a draft record and its stored image."""
    record = fx.create_case_study(editor)
    payload = fx.png_bytes()
    asset = fx.upload(editor, "case-studies", record["id"], payload=payload)
    assert asset.status_code in (200, 201), f"upload returned {asset.status_code}: {asset.text[:300]}"
    own = editor.get(f"/case-studies/{record['slug']}")
    assert own.status_code == 200 and own.json().get("state") == "draft", (
        f"the owning editor cannot read the draft: {own.status_code}"
    )
    content = editor.get(f"/media/{asset.json()['id']}/content")
    assert content.status_code == 200 and content.content == payload, (
        f"the owning editor cannot read the draft image: {content.status_code}"
    )


def test_draft_case_study_is_denied_to_an_anonymous_visitor(guest):
    """A visitor with no session is refused the seeded draft on its page and its record."""
    record = guest.get(f"/case-studies/{fx.DRAFT_CASE_STUDY_SLUG}")
    assert fx.is_client_error(record.status_code), (
        f"GET /api/case-studies/{fx.DRAFT_CASE_STUDY_SLUG} as a visitor returned {record.status_code}"
    )
    page = fx.page(f"/works/{fx.DRAFT_CASE_STUDY_SLUG}")
    assert fx.is_client_error(page.status_code), (
        f"GET /works/{fx.DRAFT_CASE_STUDY_SLUG} as a visitor returned {page.status_code}"
    )
    assert fx.DRAFT_CASE_STUDY_NAME not in record.text, "the refusal names the draft"


def test_draft_case_study_is_denied_to_a_client(founder):
    """A client is refused the seeded draft record."""
    response = founder.get(f"/case-studies/{fx.DRAFT_CASE_STUDY_SLUG}")
    assert fx.is_client_error(response.status_code), (
        f"GET /api/case-studies/{fx.DRAFT_CASE_STUDY_SLUG} as a client returned {response.status_code}"
    )
    drafts = founder.get("/case-studies", params={"state": "draft"})
    assert drafts.status_code in (200, 401, 403), f"GET /api/case-studies?state=draft returned {drafts.status_code}"
    if drafts.status_code == 200:
        assert not _shapes.items(drafts.json()), f"a client listed drafts: {drafts.text[:300]}"


def test_draft_article_is_denied_to_a_second_editor(second_editor, editor):
    """A second editor is refused another editor's draft article and draft case study."""
    record = fx.create_article(editor)
    response = second_editor.get(f"/articles/{record['slug']}")
    assert fx.is_client_error(response.status_code), (
        f"GET /api/articles/{record['slug']} as the second editor returned {response.status_code}"
    )
    seeded = second_editor.get(f"/case-studies/{fx.DRAFT_CASE_STUDY_SLUG}")
    assert fx.is_client_error(seeded.status_code), (
        f"the second editor read the seeded draft case study: {seeded.status_code}"
    )
    own = second_editor.get(f"/articles/{fx.DRAFT_ARTICLE_SLUG}")
    assert own.status_code == 200 and own.json().get("title") == fx.DRAFT_ARTICLE_TITLE, (
        f"editor2 cannot read the seeded draft article it owns: {own.status_code}"
    )
    assert fx.is_client_error(editor.get(f"/articles/{fx.DRAFT_ARTICLE_SLUG}").status_code), (
        "the first editor read the second editor's seeded draft article"
    )


def test_draft_media_is_denied_to_everyone_but_its_owner(editor, second_editor, founder, guest, store):
    """A draft image is stored in the bucket and refused to everyone but its owner."""
    seeded = editor.get(f"/case-studies/{fx.DRAFT_CASE_STUDY_SLUG}")
    assert seeded.status_code == 200, f"the owning editor cannot read the seeded draft: {seeded.status_code}"
    media = seeded.json().get("media") or []
    assert media, "the seeded draft Nightjar carries no stored image"
    asset = media[0]
    assert asset.get("alt_text") == "Nightjar concept board", f"the seeded draft image carries {asset.get('alt_text')!r}"
    assert store.exists(asset["object_key"]), f"the seeded draft image is not in the bucket at {asset['object_key']}"
    for label, client in (("visitor", guest), ("client", founder), ("second editor", second_editor)):
        response = client.get(f"/media/{asset['id']}/content")
        assert fx.is_client_error(response.status_code), (
            f"the {label} read the draft image with {response.status_code}"
        )
    assert editor.get(f"/media/{asset['id']}/content").status_code == 200, "the owner cannot read the draft image"


def test_draft_refusal_matches_an_unknown_slug(guest):
    """Refusing a draft looks the same as asking for an entry that does not exist."""
    unknown = f"missing-{fx.unique_suffix()}"
    draft = guest.get(f"/case-studies/{fx.DRAFT_CASE_STUDY_SLUG}")
    missing = guest.get(f"/case-studies/{unknown}")
    assert draft.status_code == missing.status_code, (
        f"a draft answers {draft.status_code} while an unknown slug answers {missing.status_code}"
    )
    assert fx.page(f"/works/{fx.DRAFT_CASE_STUDY_SLUG}").status_code == fx.page(f"/works/{unknown}").status_code, (
        "the draft page and an unknown page answer differently"
    )


def test_draft_never_appears_in_listings_counts_or_the_sitemap(editor):
    """Drafts stay out of the index, the archive, the counts and the sitemap."""
    draft = fx.create_article(editor, category="studio-life")
    before = {c["slug"]: c["entry_count"] for c in httpx.get(f"{fx.api_base()}/article-categories", timeout=fx.TIMEOUT).json()}
    assert fx.DRAFT_CASE_STUDY_SLUG not in fx.index_slugs(), "the draft Nightjar appears in the index"
    assert fx.DRAFT_CASE_STUDY_NAME not in fx.page_text("/works"), "the index page names the draft Nightjar"
    listed = [a.get("slug") for page in (1, 2, 3) for a in _shapes.items(
        httpx.get(f"{fx.api_base()}/articles", params={"page": page}, timeout=fx.TIMEOUT).json())]
    assert draft["slug"] not in listed and fx.DRAFT_ARTICLE_SLUG not in listed, "a draft article is listed"
    assert fx.DRAFT_ARTICLE_TITLE not in fx.page_text("/blog-categories/studio-life"), "the category route lists a draft"
    after = {c["slug"]: c["entry_count"] for c in httpx.get(f"{fx.api_base()}/article-categories", timeout=fx.TIMEOUT).json()}
    assert after.get("studio-life") == before.get("studio-life"), "creating a draft changed a category count"
    paths = fx.sitemap_paths()
    for path in (f"/works/{fx.DRAFT_CASE_STUDY_SLUG}", f"/blog/{fx.DRAFT_ARTICLE_SLUG}", f"/blog/{draft['slug']}"):
        assert path not in paths, f"/sitemap.xml lists the draft address {path}"


def test_client_cannot_create_upload_or_publish(founder, backend):
    """A client session is refused every editor write and nothing changes."""
    payload = fx.case_study_payload()
    created = founder.post("/case-studies", json=payload)
    assert fx.is_client_error(created.status_code), f"a client created a case study: {created.status_code}"
    assert backend.count("case_study", slug=payload["slug"]) == 0, "a refused client write stored a row"
    before = backend.query("SELECT state FROM case_study WHERE slug = %s", ("lumen-pay",))
    for response in (founder.post("/case-studies/1/unpublish"),
                     founder.post("/articles", json=fx.article_payload()),
                     fx.upload(founder, "case-studies", 1)):
        assert fx.is_client_error(response.status_code), (
            f"{response.request.method} {response.request.url.path} as a client returned {response.status_code}"
        )
    after = backend.query("SELECT state FROM case_study WHERE slug = %s", ("lumen-pay",))
    assert before == after, "a refused client write changed a stored case study"


def test_second_editor_cannot_publish_or_edit_another_editors_entry(editor, second_editor, backend):
    """A second editor cannot publish, edit or withdraw an entry it does not own."""
    draft = fx.create_case_study(editor)
    attempt = fx.publish(second_editor, "case-studies", draft["id"])
    assert fx.is_client_error(attempt.status_code), f"the second editor published a draft: {attempt.status_code}"
    live = fx.published_case_study(editor)
    edit = second_editor.patch(f"/case-studies/{live['id']}", json={"title": "Hijacked"})
    withdraw = fx.unpublish(second_editor, "case-studies", live["id"])
    for response in (edit, withdraw):
        assert fx.is_client_error(response.status_code), (
            f"the second editor changed a published entry it does not own: {response.status_code}"
        )
    rows = backend.query("SELECT state, title FROM case_study WHERE id IN (%s, %s) ORDER BY id",
                         (draft["id"], live["id"]))
    assert rows[0]["state"] == "draft", "the refused publish changed the draft"
    assert rows[1]["state"] == "published" and rows[1]["title"] == live["title"], "the refused edit changed the entry"


def test_uploaded_image_is_stored_in_the_bucket_at_the_pinned_key(editor, store):
    """An uploaded image lives in the bucket at its key and streams back through the app."""
    record = fx.create_case_study(editor)
    payload = fx.png_bytes()
    response = fx.upload(editor, "case-studies", record["id"], payload=payload)
    assert response.status_code in (200, 201), f"upload returned {response.status_code}: {response.text[:300]}"
    asset = response.json()
    key = f"media/case-study/{record['id']}/{fx.digest_of(payload)}.png"
    assert asset.get("object_key") == key, f"the object key is {asset.get('object_key')!r}, expected {key!r}"
    assert store.exists(key), f"no object exists in the bucket at {key}"
    content = editor.get(f"/media/{asset['id']}/content")
    assert content.content == payload, "the streamed bytes differ from the uploaded bytes"


def test_media_object_key_follows_the_pinned_scheme(editor, backend):
    """Every stored media row carries a key in the pinned scheme and its metadata."""
    article = fx.create_article(editor)
    payload = fx.png_bytes()
    response = fx.upload(editor, "articles", article["id"], payload=payload, alt_text="A probe diagram")
    assert response.status_code in (200, 201), f"article upload returned {response.status_code}"
    asset = response.json()
    for field in ("id", "object_key", "content_type", "byte_size", "alt_text"):
        assert field in asset, f"the upload response lacks {field!r}: {asset}"
    assert asset["object_key"] == f"media/article/{article['id']}/{fx.digest_of(payload)}.png", (
        f"the article image key is {asset['object_key']!r}"
    )
    assert asset["byte_size"] == len(payload) and asset["content_type"] == "image/png", f"metadata is {asset}"
    rows = backend.query("SELECT object_key, entry_kind FROM media_asset")
    bad = [r["object_key"] for r in rows if not fx.MEDIA_KEY_RE.match(str(r["object_key"]))]
    assert not bad, f"media_asset rows carry keys outside the scheme: {bad[:5]}"


def test_no_column_stores_image_bytes(backend):
    """No table carries a binary column holding image bytes."""
    rows = backend.query(
        "SELECT table_name, column_name FROM information_schema.columns "
        "WHERE table_schema = 'public' AND data_type = 'bytea'"
    )
    assert not rows, f"these columns can hold image bytes: {rows}"


def test_non_image_upload_is_refused_and_stores_nothing(editor, backend, store):
    """A file that is not an accepted image is refused and reaches neither store."""
    record = fx.create_case_study(editor)
    for payload, content_type, name in ((b"plain text, not an image", "text/plain", "note.txt"),
                                        (b"%PDF-1.4 probe", "application/pdf", "brief.pdf")):
        response = fx.upload(editor, "case-studies", record["id"], payload=payload,
                             content_type=content_type, filename=name)
        assert fx.is_client_error(response.status_code), (
            f"uploading {content_type} returned {response.status_code}: {response.text[:200]}"
        )
    assert backend.count("media_asset", entry_id=record["id"], entry_kind="case-study") == 0, (
        "a refused upload stored a media row"
    )
    assert not store.list(f"media/case-study/{record['id']}/"), "a refused upload reached the bucket"


def test_oversized_upload_is_refused(editor, backend):
    """An image larger than the ceiling is refused and stores nothing."""
    record = fx.create_case_study(editor)
    payload = fx.png_bytes() + os.urandom(fx.MAX_UPLOAD_BYTES)
    response = fx.upload(editor, "case-studies", record["id"], payload=payload)
    assert fx.is_client_error(response.status_code), f"a {len(payload)} byte upload returned {response.status_code}"
    assert backend.count("media_asset", entry_id=record["id"], entry_kind="case-study") == 0, (
        "an oversized upload stored a media row"
    )


def test_upload_without_alternative_text_is_refused(editor, backend):
    """An upload with no alternative text is refused and stores nothing."""
    record = fx.create_case_study(editor)
    response = fx.upload(editor, "case-studies", record["id"], alt_text=None)
    assert fx.is_client_error(response.status_code), f"an upload with no alt_text returned {response.status_code}"
    assert backend.count("media_asset", entry_id=record["id"], entry_kind="case-study") == 0, (
        "an upload with no alternative text stored a row"
    )


def test_duplicate_media_upload_is_idempotent(editor, backend, store):
    """The same bytes uploaded twice to one entry leave one object and one row."""
    record = fx.create_case_study(editor)
    payload = fx.png_bytes()
    first = fx.upload(editor, "case-studies", record["id"], payload=payload)
    second = fx.upload(editor, "case-studies", record["id"], payload=payload)
    assert first.status_code in (200, 201) and second.status_code in (200, 201), (
        f"the uploads returned {first.status_code} and {second.status_code}"
    )
    assert first.json()["id"] == second.json()["id"], "the repeated upload returned a different asset"
    assert backend.count("media_asset", entry_id=record["id"], entry_kind="case-study") == 1, (
        "the repeated upload stored a second media row"
    )
    assert len(store.list(f"media/case-study/{record['id']}/")) == 1, "the repeated upload stored a second object"


def test_published_media_is_served_and_appears_with_its_alt_text(editor):
    """A published entry's image streams to anyone and appears on its page with its text."""
    record = fx.create_case_study(editor)
    alt = f"Probe dashboard screen {fx.unique_suffix()}"
    later_alt = f"Probe checkout screen {fx.unique_suffix()}"
    payload = fx.png_bytes()
    asset = fx.upload(editor, "case-studies", record["id"], payload=payload, alt_text=alt).json()
    fx.upload(editor, "case-studies", record["id"], alt_text=later_alt)
    fx.publish(editor, "case-studies", record["id"])
    content = httpx.get(f"{fx.api_base()}/media/{asset['id']}/content", timeout=fx.TIMEOUT)
    assert content.status_code == 200 and content.content == payload, (
        f"GET /api/media/{asset['id']}/content returned {content.status_code}"
    )
    markup = fx.rendered(f"/works/{record['slug']}")
    images = [attrs for tag, attrs in fx.tags_of(markup) if tag == "img" and attrs.get("alt") == alt]
    assert images, f"/works/{record['slug']} carries no image with the alternative text {alt!r}"
    assert f"/api/media/{asset['id']}/content" in images[0].get("src", ""), (
        f"the uploaded image is not served through the content route: {images[0]}"
    )
    order = [attrs.get("alt") for tag, attrs in fx.tags_of(markup) if tag == "img" and attrs.get("alt") in (alt, later_alt)]
    assert order == [alt, later_alt], f"the uploaded images appear in the order {order}, not upload order"


def test_bucket_refuses_anonymous_reads(editor):
    """The bucket never answers an unsigned read and no signed link is issued."""
    record = fx.create_case_study(editor)
    asset = fx.upload(editor, "case-studies", record["id"]).json()
    fx.publish(editor, "case-studies", record["id"])
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    bucket = os.environ["STORAGE_BUCKET"]
    direct = httpx.get(f"{endpoint}/{bucket}/{asset['object_key']}", timeout=fx.TIMEOUT)
    assert direct.status_code in (401, 403), f"the bucket served an unsigned read with {direct.status_code}"
    served = httpx.get(f"{fx.api_base()}/case-studies/{record['slug']}", timeout=fx.TIMEOUT).text
    assert "X-Amz-Signature" not in served and endpoint not in served, (
        "the case study record carries a direct or signed bucket address"
    )


def test_concurrent_publish_of_one_slug_yields_exactly_one_winner(editor):
    """Two simultaneous publishes claiming one slug leave exactly one published case study."""
    contested = fx.probe_slug("contested")
    first = fx.create_case_study(editor, slug=contested)
    second = fx.create_case_study(editor, slug=contested)
    gate = threading.Barrier(2)
    headers = dict(editor.headers)

    def race(record_id):
        with httpx.Client(base_url=fx.api_base(), timeout=fx.TIMEOUT, headers=headers) as racer:
            gate.wait(timeout=10)
            return racer.post(f"/case-studies/{record_id}/publish")

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(race, (first["id"], second["id"])))
    codes = [r.status_code for r in results]
    assert sum(1 for c in codes if c in (200, 201)) == 1, f"the contended publishes returned {codes}"
    assert sum(1 for c in codes if fx.is_client_error(c)) == 1, f"the losing publish returned {codes}"
    holders = [s for s in fx.index_slugs() if s == contested]
    assert len(holders) == 1, f"the index lists {len(holders)} rows for {contested}"


def test_losing_publish_leaves_no_partial_state(editor, backend):
    """A publish onto a taken slug is refused and leaves the draft untouched."""
    contested = fx.probe_slug("taken")
    winner = fx.published_case_study(editor, slug=contested)
    loser = fx.create_case_study(editor, slug=contested)
    refusal = fx.publish(editor, "case-studies", loser["id"])
    assert fx.is_client_error(refusal.status_code), (
        f"publishing onto the taken slug {contested} returned {refusal.status_code}"
    )
    rows = backend.query("SELECT id, state, published_at FROM case_study WHERE slug = %s ORDER BY id", (contested,))
    states = {row["id"]: (row["state"], row["published_at"]) for row in rows}
    assert states[winner["id"]][0] == "published", f"the winner changed: {states}"
    assert states[loser["id"]] == ("draft", None), f"the loser was left as {states[loser['id']]}"
    assert sum(1 for s in fx.index_slugs() if s == contested) == 1, "the loser took an index position"
    assert f"/works/{contested}" in fx.sitemap_paths(), "the winner's sitemap address is missing"


def test_publishing_onto_a_taken_article_slug_is_refused(editor, backend):
    """A second article cannot be published onto a slug a published article holds."""
    contested = fx.probe_slug("article-taken")
    fx.published_article(editor, slug=contested)
    loser = fx.create_article(editor, slug=contested)
    refusal = fx.publish(editor, "articles", loser["id"])
    assert fx.is_client_error(refusal.status_code), f"the second article publish returned {refusal.status_code}"
    count = backend.count("article", slug=contested, state="published")
    assert count == 1, f"{count} published articles hold {contested}"


def test_case_study_services_are_a_relation(editor, backend):
    """A case study's services are stored as relation rows to the service table."""
    record = fx.create_case_study(editor, services=["Fractional CTO", "Dedicated team"])
    rows = backend.query(
        "SELECT s.name FROM case_study_service cs JOIN service s ON s.id = cs.service_id "
        "WHERE cs.case_study_id = %s ORDER BY s.name",
        (record["id"],),
    )
    assert [r["name"] for r in rows] == ["Dedicated team", "Fractional CTO"], (
        f"the case study's relation rows are {rows}"
    )


def test_unknown_service_on_a_case_study_is_refused(editor, backend):
    """Naming a service outside the eight is refused and writes nothing."""
    payload = fx.case_study_payload(services=["UX/UI design", "Growth hacking"])
    response = editor.post("/case-studies", json=payload)
    assert fx.is_client_error(response.status_code), f"an unknown service returned {response.status_code}"
    assert backend.count("case_study", slug=payload["slug"]) == 0, "the refused case study was stored"


def test_article_requires_exactly_one_known_category(editor, backend):
    """An article with no category or an unknown one is refused and writes nothing."""
    for category in (None, "gardening"):
        payload = fx.article_payload()
        if category is None:
            payload.pop("category")
        else:
            payload["category"] = category
        response = editor.post("/articles", json=payload)
        assert fx.is_client_error(response.status_code), (
            f"an article with category {category!r} returned {response.status_code}"
        )
        assert backend.count("article", slug=payload["slug"]) == 0, "the refused article was stored"


def test_case_study_index_lists_published_rows_in_index_order():
    """The index leads with the ten seeded case studies in their seeded order."""
    slugs = fx.index_slugs()
    seeded = [row[0] for row in fx.SEEDED_CASE_STUDIES]
    assert slugs[:10] == seeded, f"the index opens with {slugs[:10]}"
    text = fx.page_text("/works")
    for _, name, label, title, _ in fx.SEEDED_CASE_STUDIES:
        for value in (name, label, title):
            assert value in text, f"the index page does not show {value!r}"
    for line in fx.WORKS_HERO_LINES:
        assert line in text, f"the index hero lacks {line!r}"


def test_case_study_rows_alternate_image_side():
    """Rows alternate the picture side, starting on the right, and open their pages."""
    markup = fx.rendered("/works")
    rows = fx.tags_with(markup, "data-case-study-row")
    sides = [attrs.get("data-image-side") for _, attrs in rows]
    expected = ["right" if i % 2 == 0 else "left" for i in range(len(sides))]
    assert len(sides) >= 10 and sides == expected, f"the row sides are {sides}"
    hrefs = {attrs.get("href") for tag, attrs in fx.tags_of(markup) if tag == "a"}
    for slug, *_ in fx.SEEDED_CASE_STUDIES:
        assert f"/works/{slug}" in hrefs, f"no row links to /works/{slug}"


def test_case_study_rows_and_pages_share_one_services_list():
    """The services shown on a row match the services shown on its page."""
    row_text = fx.page_text("/works")
    page_text = fx.page_text("/works/lumen-pay")
    for service in fx.LUMEN_PAY_SERVICES:
        assert service in row_text, f"the index does not show the service {service!r}"
        assert service in page_text, f"the Lumen Pay page does not show the service {service!r}"


def test_case_study_page_carries_its_fact_sheet():
    """A case study page carries the name, subtitle, fact labels, body and site link."""
    body = httpx.get(f"{fx.api_base()}/case-studies/lumen-pay", timeout=fx.TIMEOUT).json()
    markup = fx.rendered("/works/lumen-pay")
    text = fx.visible_text(markup)
    assert body["subtitle"] == "Fintech product, designed and built by Iron Wood", f"the Lumen Pay subtitle is {body['subtitle']!r}"
    assert body["website_url"] == "https://lumen-pay.example.com", f"the Lumen Pay site address is {body['website_url']!r}"
    for value in ("Lumen Pay", body["subtitle"], "Visit site", "Industry", "Fintech", "Year", "2026"):
        assert value in text, f"the Lumen Pay page lacks {value!r}"
    opening = " ".join(fx.visible_text(body["body"]).split()[:5])
    assert opening in text, f"the Lumen Pay page lacks its body opening {opening!r}"
    links = {attrs.get("href") for tag, attrs in fx.tags_of(markup) if tag == "a"}
    assert body["website_url"] in links, f"the Visit site link does not point at {body['website_url']}"


def test_next_project_follows_index_order_and_wraps():
    """The next-project section names the next case study and the last wraps to the first."""
    first = fx.page_text("/works/lumen-pay")
    assert "Next project" in first, "the Lumen Pay page lacks the Next project section"
    assert fx.SEEDED_CASE_STUDIES[1][3] in first, "Lumen Pay's next project is not Haven Health"
    slugs = fx.index_slugs()
    last = fx.page_text(f"/works/{slugs[-1]}")
    assert fx.SEEDED_CASE_STUDIES[0][3] in last, (
        f"the last case study {slugs[-1]} does not wrap to Lumen Pay"
    )
    assert fx.DRAFT_CASE_STUDY_NAME not in last, "the next-project section names a draft"


def test_article_archive_paginates_newest_first():
    """The archive lists four articles to a page, newest first, with an appending control."""
    listed = httpx.get(f"{fx.api_base()}/articles", params={"page": 1}, timeout=fx.TIMEOUT).json()
    assert len(listed) == fx.PAGE_SIZE, f"page 1 of GET /api/articles holds {len(listed)} articles"
    stamps = [str(a.get("published_at")) for a in listed]
    assert stamps == sorted(stamps, reverse=True), f"page 1 is not newest first: {stamps}"
    markup = fx.rendered("/blog")
    rows = fx.tags_with(markup, "data-article-row")
    assert len(rows) == fx.PAGE_SIZE, f"/blog renders {len(rows)} rows"
    assert [a.get("data-slug") for _, a in rows] == [a["slug"] for a in listed], "the page and the API disagree"
    nexts = [a for _, a in fx.tags_with(markup, "data-pagination") if a.get("data-pagination") == "next"]
    assert nexts and "page=2" in nexts[0].get("href", ""), f"the More control is {nexts}"
    assert "More" in fx.visible_text(markup), "the pagination control is not labelled More"
    total = sum(c["entry_count"] for c in httpx.get(f"{fx.api_base()}/article-categories", timeout=fx.TIMEOUT).json())
    last_page = (total + fx.PAGE_SIZE - 1) // fx.PAGE_SIZE
    tail = fx.rendered(f"/blog?page={last_page}")
    assert fx.tags_with(tail, "data-article-row"), f"/blog?page={last_page} renders no rows"
    assert not [a for _, a in fx.tags_with(tail, "data-pagination") if a.get("data-pagination") == "next"], (
        "the last archive page still offers More"
    )


def test_article_rows_show_category_date_and_reading_time():
    """Each seeded article row shows its category, date and reading time."""
    text = " ".join(fx.page_text(f"/blog?page={page}") for page in (1, 2, 3))
    names = dict(fx.CATEGORIES)
    for slug, title, category, reading, date in fx.SEEDED_ARTICLES:
        for value in (title, names[category], reading, date):
            assert value in text, f"the archive does not show {value!r} for {slug}"


def test_category_tabs_carry_counts_and_the_current_state():
    """The tabs run All then the three categories, with counts and a current tab."""
    markup = fx.rendered("/blog-categories/engineering")
    text = fx.visible_text(markup)
    positions = [text.find(label) for label in ("All", "Product design", "Engineering", "Studio life")]
    assert all(p >= 0 for p in positions) and positions == sorted(positions), f"tab order is {positions}"
    counts = {c["slug"]: c["entry_count"] for c in httpx.get(f"{fx.api_base()}/article-categories", timeout=fx.TIMEOUT).json()}
    tabs = [a for tag, a in fx.tags_of(markup) if tag == "a" and "data-count" in a]
    for slug, _ in fx.CATEGORIES:
        tab = [a for a in tabs if a.get("href", "").rstrip("/").endswith(f"/blog-categories/{slug}")]
        assert tab, f"no tab carrying data-count links to /blog-categories/{slug}"
        assert tab[0].get("data-count") == str(counts[slug]), (
            f"the {slug} tab carries data-count {tab[0].get('data-count')!r}, expected {counts[slug]}"
        )
    current = [a for _, a in fx.tags_with(markup, "aria-current") if a.get("aria-current") == "page"]
    assert len(current) == 1 and current[0].get("href", "").rstrip("/").endswith("/blog-categories/engineering"), (
        f"the current tab is {current}"
    )


def test_category_route_lists_only_its_articles():
    """A category route lists only that category's published articles."""
    slugs = fx.listed_article_slugs("/blog-categories/engineering")
    api = [a["slug"] for a in httpx.get(f"{fx.api_base()}/articles", params={"category": "engineering", "page": 1}, timeout=fx.TIMEOUT).json()]
    assert slugs == api, f"the engineering route lists {slugs} while the API lists {api}"
    for article in httpx.get(f"{fx.api_base()}/articles", params={"category": "engineering", "page": 1}, timeout=fx.TIMEOUT).json():
        assert article["category"]["slug"] == "engineering", f"{article['slug']} is not an engineering article"
    assert "shipping-an-mvp-in-eight-weeks" in slugs and "a-week-inside-the-studio" not in slugs, (
        f"the engineering route lists {slugs}"
    )


def test_category_counts_follow_publication(editor):
    """Publishing and withdrawing an article moves its category count."""
    def count():
        return {c["slug"]: c["entry_count"] for c in httpx.get(f"{fx.api_base()}/article-categories", timeout=fx.TIMEOUT).json()}["product-design"]
    before = count()
    record = fx.published_article(editor, category="product-design")
    assert count() == before + 1, "publishing did not raise the product-design count"
    fx.unpublish(editor, "articles", record["id"])
    assert count() == before, "withdrawing did not lower the product-design count"


def test_article_page_carries_its_parts():
    """An article page carries its title, category, date, reading time, body and contents."""
    body = httpx.get(f"{fx.api_base()}/articles/shipping-an-mvp-in-eight-weeks", timeout=fx.TIMEOUT).json()
    text = fx.page_text("/blog/shipping-an-mvp-in-eight-weeks")
    for value in ("Shipping an MVP in eight weeks", "Engineering", "Sep 2, 2026", "7 min read", "Contents",
                  "Related articles"):
        assert value in text, f"the article page lacks {value!r}"
    opening = " ".join(fx.visible_text(body["body"]).split()[:5])
    assert opening in text, f"the article page lacks its body opening {opening!r}"


def test_reading_progress_appears_on_article_pages_only():
    """Only article pages carry the reading progress bar."""
    assert fx.tags_with(fx.rendered("/blog/shipping-an-mvp-in-eight-weeks"), "data-reading-progress"), (
        "the article page carries no data-reading-progress bar"
    )
    for route in fx.CONTENT_ROUTES:
        if route.startswith("/blog/"):
            continue
        assert not fx.tags_with(fx.rendered(route), "data-reading-progress"), f"{route} carries a reading progress bar"


def test_related_articles_come_from_the_same_category(editor):
    """Related articles are published articles of the same category, never a draft."""
    draft = fx.create_article(editor, category="engineering")
    text = fx.page_text("/blog/shipping-an-mvp-in-eight-weeks")
    assert "When to bring in a fractional CTO" in text, "the related section omits the other engineering article"
    assert draft["title"] not in text, "the related section shows a draft"
    assert "A week inside the studio" not in text.split("Related articles")[-1], (
        "the related section shows an article from another category"
    )
    related = text.split("Related articles")[-1]
    assert "Shipping an MVP in eight weeks" not in related, "the related section repeats the current article"


def test_contact_page_carries_the_form_and_both_result_panels():
    """The contact page carries the named fields, a token and both hidden panels."""
    markup = fx.rendered("/contact")
    forms = fx.tags_with(markup, "data-enquiry-form")
    assert len(forms) == 1, f"/contact carries {len(forms)} enquiry forms"
    fields = {attrs.get("name"): (tag, attrs) for tag, attrs in fx.tags_of(markup) if attrs.get("name")}
    for name in ("Service", "Budget", "Name", "Email", "Message", "bpGCap", "Website"):
        assert name in fields, f"the enquiry form has no field named {name!r}"
    assert fields["bpGCap"][1].get("type") == "hidden" and fields["bpGCap"][1].get("value"), (
        f"bpGCap is not a hidden field carrying a token: {fields['bpGCap']}"
    )
    panels = {attrs.get("data-form-result"): attrs for _, attrs in fx.tags_with(markup, "data-form-result")}
    for state in ("success", "failure"):
        assert state in panels, f"/contact carries no data-form-result={state!r} panel"
        attrs = panels[state]
        assert "hidden" in attrs or "display:none" in attrs.get("style", "").replace(" ", "") or attrs.get("aria-hidden") == "true", (
            f"the {state} panel is not hidden before submission: {attrs}"
        )
    page_text = fx.visible_text(markup)
    for line in (fx.SUCCESS_HEADING, fx.SUCCESS_LINE, fx.FAILURE_LINE):
        assert line in page_text, f"/contact lacks the panel copy {line!r}"
    for value in (fx.CONTACT_HERO, "Email", "Careers", "Follow us", fx.CONTACT_MAILBOX, fx.CAREERS_MAILBOX):
        assert value in page_text, f"/contact lacks {value!r}"
    assert "Send enquiry" in markup, "the send control has no accessible name 'Send enquiry'"


def test_contact_form_offers_the_fixed_options():
    """Service and Budget are chosen from the fixed option lists."""
    markup = fx.rendered("/contact")
    options = [attrs.get("value", "") for tag, attrs in fx.tags_of(markup) if tag == "option"]
    for value in fx.SERVICES + fx.BUDGETS:
        assert value in options, f"the enquiry form offers no option {value!r}"


def test_anonymous_enquiry_is_stored_with_state_new(backend):
    """An accepted anonymous enquiry is stored as a new row with no account."""
    response, payload = fx.send_enquiry()
    assert response.status_code in (200, 201), f"POST /api/enquiries returned {response.status_code}: {response.text[:300]}"
    body = response.json()
    assert body.get("state") == "new" and body.get("id"), f"the enquiry response is {body}"
    rows = fx.enquiry_rows_for(backend, payload["Email"])
    assert len(rows) == 1, f"{len(rows)} enquiry rows stored for {payload['Email']}"
    row = rows[0]
    assert (row["service"], row["budget"], row["state"], row["client_id"]) == (
        payload["Service"], payload["Budget"], "new", None), f"the stored enquiry is {row}"


def test_signed_in_enquiry_is_attached_to_the_client(backend):
    """An enquiry sent while signed in is attached to the sender's account."""
    email, token, body = fx.register()
    with appclient.client(token) as client:
        response, payload = fx.send_enquiry(client, Email=email)
        assert response.status_code in (200, 201), f"the signed-in enquiry returned {response.status_code}"
        mine = client.get("/enquiries").json()
    rows = fx.enquiry_rows_for(backend, email)
    assert len(rows) == 1 and rows[0]["client_id"] == body["user"]["id"], f"the stored rows are {rows}"
    assert [e.get("message") for e in mine] == [payload["Message"]], f"the client sees {mine}"


def test_enquiry_with_an_unknown_service_or_budget_is_refused(backend):
    """A value outside the fixed options is refused and stores nothing."""
    for override in ({"Service": "Growth hacking"}, {"Budget": "$1m"}):
        response, payload = fx.send_enquiry(**override)
        assert fx.is_client_error(response.status_code), f"{override} returned {response.status_code}"
        assert not fx.enquiry_rows_for(backend, payload["Email"]), f"{override} stored a row"


def test_enquiry_missing_a_required_field_is_refused(backend):
    """A missing name, email or message is refused, named, and stores nothing."""
    for field in ("Name", "Email", "Message"):
        payload = fx.enquiry_payload()
        email = payload["Email"]
        payload[field] = ""
        response = httpx.post(f"{fx.api_base()}/enquiries", json=payload, timeout=fx.TIMEOUT)
        assert fx.is_client_error(response.status_code), f"an empty {field} returned {response.status_code}"
        assert field.lower() in response.text.lower(), f"the refusal does not name the field {field}: {response.text[:200]}"
        assert not fx.enquiry_rows_for(backend, email), f"an empty {field} stored a row"


def test_enquiry_with_an_invalid_email_is_refused(backend):
    """An address that is not an email address is refused and stores nothing."""
    for bad in ("not-an-address", "founder@", "@example.com"):
        response, _ = fx.send_enquiry(Email=bad)
        assert fx.is_client_error(response.status_code), f"the address {bad!r} returned {response.status_code}"
        assert not fx.enquiry_rows_for(backend, bad), f"the address {bad!r} stored a row"


def test_bot_check_token_is_single_use(backend):
    """A token spent once is refused the second time."""
    token = fx.bot_token()
    first, _ = fx.send_enquiry(bpGCap=token)
    assert first.status_code in (200, 201), f"the first use of a token returned {first.status_code}"
    second, payload = fx.send_enquiry(bpGCap=token)
    assert fx.is_client_error(second.status_code), f"a reused token returned {second.status_code}"
    assert not fx.enquiry_rows_for(backend, payload["Email"]), "a reused token stored a row"


def test_enquiry_without_a_valid_bot_check_token_is_refused(backend):
    """A missing or unknown token is refused and stores nothing."""
    for token in ("", f"forged-{fx.unique_suffix()}"):
        response, payload = fx.send_enquiry(bpGCap=token)
        assert fx.is_client_error(response.status_code), f"the token {token!r} returned {response.status_code}"
        assert not fx.enquiry_rows_for(backend, payload["Email"]), f"the token {token!r} stored a row"


def test_expired_bot_check_token_is_refused(backend):
    """A token older than its lifetime is refused and stores nothing."""
    token = fx.bot_token()
    backend.query(
        "UPDATE bot_check_token SET issued_at = issued_at - make_interval(mins => %s) WHERE token = %s",
        (fx.BOT_TOKEN_LIFETIME_MINUTES + 1, token),
    )
    response, payload = fx.send_enquiry(bpGCap=token)
    assert fx.is_client_error(response.status_code), f"an expired token returned {response.status_code}"
    assert not fx.enquiry_rows_for(backend, payload["Email"]), "an expired token stored a row"


def test_enquiry_with_a_filled_decoy_is_refused(backend):
    """An enquiry whose decoy field arrives filled is refused and stores nothing."""
    response, payload = fx.send_enquiry(Website="https://spam.example.com")
    assert fx.is_client_error(response.status_code), f"a filled decoy returned {response.status_code}"
    assert not fx.enquiry_rows_for(backend, payload["Email"]), "a filled decoy stored a row"


def test_repeated_enquiries_from_one_address_are_refused(backend):
    """A third enquiry from one address within the window is refused."""
    email = fx.probe_email()
    codes = [fx.send_enquiry(Email=email)[0].status_code for _ in range(3)]
    assert codes[0] in (200, 201) and codes[1] in (200, 201), f"the first two enquiries returned {codes}"
    assert fx.is_client_error(codes[2]), f"the third enquiry within {fx.RATE_WINDOW_SECONDS} seconds returned {codes[2]}"
    assert len(fx.enquiry_rows_for(backend, email)) == 2, "the refused third enquiry stored a row"


def test_enquiry_list_is_denied_to_an_unauthenticated_visitor(guest):
    """The enquiry list is refused to a visitor with no session."""
    response = guest.get("/enquiries")
    assert fx.is_client_error(response.status_code), f"GET /api/enquiries with no session returned {response.status_code}"
    assert fx.ANONYMOUS_ENQUIRER_EMAIL not in response.text, "the refusal disclosed an enquiry"


def test_editor_reads_every_enquiry(editor):
    """An editor reads every enquiry, including both seeded ones, with the pinned fields."""
    rows = editor.get("/enquiries").json()
    emails = {row.get("email") for row in rows}
    assert {fx.CLIENT_EMAIL, fx.ANONYMOUS_ENQUIRER_EMAIL} <= emails, f"the editor sees {sorted(emails)[:6]}"
    for field in ("id", "service", "budget", "name", "email", "message", "state", "created_at"):
        assert field in rows[0], f"an enquiry record lacks {field!r}: {rows[0]}"
    seeded = [r for r in rows if r.get("email") == fx.ANONYMOUS_ENQUIRER_EMAIL][0]
    assert seeded.get("state") == "in_conversation", f"the seeded anonymous enquiry is in state {seeded.get('state')!r}"
    assert seeded.get("message") == "We want a faster marketing site with a case study library.", "the seeded enquiry message differs"
    assert (seeded["name"], seeded["service"], seeded["budget"]) == ("Ada Quinn", "Website development", "$10k - $30k"), (
        f"the seeded anonymous enquiry is {seeded}"
    )


def test_client_sees_only_their_own_enquiries(founder):
    """A client reads only the enquiries attached to that account."""
    rows = founder.get("/enquiries").json()
    emails = {row.get("email") for row in rows}
    assert emails == {fx.CLIENT_EMAIL}, f"client@example.com sees enquiries from {emails}"
    assert any(r.get("service") == "UX/UI design" and r.get("budget") == "$30k - $60k" for r in rows), (
        f"the seeded client enquiry is missing: {rows}"
    )


def test_enquiry_state_moves_forward_only(editor, backend):
    """An enquiry moves forward to in_conversation and closed, and never back."""
    response, payload = fx.send_enquiry()
    enquiry_id = response.json()["id"]
    forward = editor.patch(f"/enquiries/{enquiry_id}", json={"state": "in_conversation"})
    assert forward.status_code == 200 and forward.json().get("state") == "in_conversation", (
        f"moving to in_conversation returned {forward.status_code}: {forward.text[:200]}"
    )
    backward = editor.patch(f"/enquiries/{enquiry_id}", json={"state": "new"})
    assert fx.is_client_error(backward.status_code), f"moving back to new returned {backward.status_code}"
    closed = editor.patch(f"/enquiries/{enquiry_id}", json={"state": "closed"})
    assert closed.status_code == 200, f"closing returned {closed.status_code}"
    reopen = editor.patch(f"/enquiries/{enquiry_id}", json={"state": "in_conversation"})
    assert fx.is_client_error(reopen.status_code), f"reopening a closed enquiry returned {reopen.status_code}"
    assert fx.enquiry_rows_for(backend, payload["Email"])[0]["state"] == "closed", "the refused moves changed the row"
    second, _ = fx.send_enquiry()
    direct = editor.patch(f"/enquiries/{second.json()['id']}", json={"state": "closed"})
    assert direct.status_code == 200, f"closing a new enquiry returned {direct.status_code}"


def test_client_cannot_change_an_enquiry_state(founder, backend):
    """A client is refused when moving an enquiry, and the row keeps its state."""
    rows = founder.get("/enquiries").json()
    target = rows[0]
    response = founder.patch(f"/enquiries/{target['id']}", json={"state": "closed"})
    assert fx.is_client_error(response.status_code), f"a client changed an enquiry state: {response.status_code}"
    stored = backend.query("SELECT state FROM enquiry WHERE id = %s", (target["id"],))
    assert stored[0]["state"] == target["state"], "the refused change moved the stored state"


def test_bot_check_loads_on_the_contact_route_only():
    """Only the contact route carries the bot check."""
    assert len(fx.tags_with(fx.rendered("/contact"), "data-bot-check")) == 1, "/contact does not carry one bot check"
    for route in fx.PUBLIC_ROUTES:
        if route == "/contact":
            continue
        assert not fx.tags_with(fx.rendered(route), "data-bot-check"), f"{route} carries a bot check"


def test_live_scenes_mount_only_on_home_and_works():
    """Scenes mount on the home page and the index only."""
    expected = {
        "/": ["mascot-hero"] + ["culture-object"] * 7,
        "/works": ["works-field", "works-preview"],
    }
    for route in fx.PUBLIC_ROUTES:
        scenes = sorted(attrs.get("data-scene") for _, attrs in fx.tags_with(fx.rendered(route), "data-scene"))
        assert scenes == sorted(expected.get(route, [])), f"{route} carries scenes {scenes}"


def test_home_culture_section_carries_seven_objects_in_order():
    """The seven culture objects appear in their pinned order beside their values."""
    markup = fx.rendered("/")
    objects = [attrs.get("data-object") for _, attrs in fx.tags_with(markup, "data-object")]
    assert objects == list(fx.CULTURE_OBJECTS), f"the culture objects are {objects}"
    text = fx.visible_text(markup)
    for title in fx.CULTURE_TITLES:
        assert title in text, f"the home page lacks the culture value {title!r}"


def test_home_carries_the_seeded_copy():
    """The home page carries its measured copy, testimonials, awards and client marks."""
    text = fx.page_text("/")
    for value in ("Ironwood", "Agency", "Award-winning digital agency specializing in design and development",
                  "See our services", "See our work",
                  "We rapidly transform ideas into problem-solving products, designed to adapt swiftly to the evolving market demands.",
                  "We team up with great minds who think alike, regardless of business size.") + fx.PROCESS_WORDS + fx.TESTIMONIAL_NAMES + fx.TESTIMONIAL_QUOTES + fx.AWARD_NAMES:
        assert value in text, f"the home page lacks {value!r}"
    for name in ("Lumen Pay", "Haven Health", "Kitefolio", "Orchard Market", "Tidewater"):
        assert name in text, f"the home client strip lacks {name!r}"


def test_services_page_carries_its_copy():
    """The services page carries its hero, service rows and sections."""
    text = fx.page_text("/services")
    for value in (fx.SERVICES_HERO, "Agency Services", "MVP", "UX/UI design", "Website development",
                  "Software development", "Branding design", "Dedicated team", "Fractional CTO",
                  "How we work with you", "Discover", "Design", "Deliver", "A team that ships alongside yours",
                  "Senior by default", "One channel, one owner", "Built to hand over"):
        assert value in text, f"the services page lacks {value!r}"


def test_services_motif_runs_one_orbit_in_reverse_phase():
    """The hive motif carries one hive part and three orbits, one in reverse phase."""
    markup = fx.rendered("/services")
    motifs = [a for _, a in fx.tags_with(markup, "data-motif") if a.get("data-motif") == "hive"]
    assert len(motifs) == 1, f"/services carries {len(motifs)} hive motifs"
    parts = [a for _, a in fx.tags_with(markup, "data-motif-part")]
    assert [a.get("data-motif-part") for a in parts].count("hive") == 1, f"the motif parts are {parts}"
    orbits = [a for a in parts if a.get("data-motif-part") == "orbit"]
    assert len(orbits) == 3, f"the motif carries {len(orbits)} orbits"
    assert sum(1 for a in orbits if a.get("data-phase") == "reverse") == 1, f"the orbit phases are {orbits}"


def test_about_page_carries_team_and_offices():
    """The about page carries its sections, six team members and two offices."""
    text = fx.page_text("/about-us")
    for value in ("About Iron Wood", "Our journey", "Trusted by product teams at", "The people behind the work",
                  "Two offices, one studio", "Northstar Learning", "Parcelio", "+1 555 0100") + fx.TEAM_MEMBERS + fx.OFFICE_LABELS + fx.OFFICE_STREETS:
        assert value in text, f"the about page lacks {value!r}"


def test_office_switcher_is_built_from_buttons():
    """The office switcher is two real buttons beside two images, one active."""
    markup = fx.rendered("/about-us")
    switches = fx.tags_with(markup, "data-office-switch")
    assert len(switches) == 2 and all(tag == "button" for tag, _ in switches), f"the switches are {switches}"
    assert all("aria-pressed" in attrs for _, attrs in switches), "a switch button carries no aria-pressed"
    images = fx.tags_with(markup, "data-office-image")
    assert len(images) == 2, f"the about page carries {len(images)} office images"
    assert sum(1 for _, a in images if a.get("data-active") == "true") == 1, f"the office images are {images}"


def test_office_details_are_read_from_the_office_table(backend):
    """The office details on the pages come from the office table."""
    rows = backend.query("SELECT id, phone FROM office WHERE label = %s", ("Second Office",))
    assert len(rows) == 1, f"the office table holds {len(rows)} rows for Second Office"
    original = rows[0]["phone"]
    probe = f"+61 2 5550 {fx.unique_suffix()[:4]}"
    backend.query("UPDATE office SET phone = %s WHERE id = %s", (probe, rows[0]["id"]))
    try:
        shown = fx.page_text("/contact")
    finally:
        backend.query("UPDATE office SET phone = %s WHERE id = %s", (original, rows[0]["id"]))
    assert probe in shown, "the contact page does not read the telephone number from the office table"


def test_split_headings_expose_their_full_text():
    """Every word-by-word heading carries its complete text as one accessible name."""
    markup = fx.rendered("/")
    labels = [a.get("aria-label", "") for _, a in fx.tags_with(markup, "data-split-heading")]
    for heading in fx.HOME_HEADINGS:
        assert heading in labels, f"no split heading carries the aria-label {heading!r}; found {labels[:6]}"


def test_header_drawer_and_footer_carry_their_link_sets():
    """The header, drawer and footer carry their own link sets and fixed copy."""
    markup = fx.rendered("/services")
    text = fx.visible_text(markup)
    for value in fx.HEADER_LINKS + fx.DRAWER_LINKS + fx.DRAWER_SOCIALS + (
            fx.HEADER_BUTTON, fx.CONTACT_MAILBOX, fx.CAREERS_MAILBOX, fx.FOOTER_LEAD_IN, fx.FOOTER_LINK,
            fx.COPYRIGHT_LINE, fx.PRIVACY_LABEL, fx.TERMS_LABEL) + fx.OFFICE_STREETS:
        assert value in text, f"the chrome on /services lacks {value!r}"
    footer = markup[markup.lower().rfind("<footer"):]
    footer_text = fx.visible_text(footer)
    for label in fx.FOOTER_SOCIALS:
        assert label in footer_text, f"the footer lacks the social label {label!r}"
    assert "behance" not in footer_text, "the footer carries behance, which only the drawer carries"
    hrefs = {a.get("href") for tag, a in fx.tags_of(footer) if tag == "a"}
    for target in ("/contact", "/privacy-policy", "/terms"):
        assert target in hrefs, f"the footer does not link to {target}"


def test_drawer_trigger_is_a_button_reporting_its_state():
    """The drawer is opened by a button that reports its closed state."""
    markup = fx.rendered("/")
    assert fx.tags_with(markup, "data-drawer"), "the page carries no data-drawer element"
    triggers = fx.tags_with(markup, "data-drawer-trigger")
    assert triggers and triggers[0][0] == "button", f"the drawer trigger is {triggers}"
    assert triggers[0][1].get("aria-expanded") == "false", f"the closed trigger reports {triggers[0][1]}"


def test_footer_appears_on_every_route_except_contact():
    """Every public route ends with the footer except the contact page."""
    for route in fx.PUBLIC_ROUTES:
        has_footer = "<footer" in fx.rendered(route).lower()
        if route in fx.FOOTERLESS_ROUTES:
            assert not has_footer, f"{route} carries a footer"
        else:
            assert has_footer, f"{route} carries no footer"


def test_bands_alternate_ground_on_every_route():
    """Every route's bands carry their pinned ground sequence and no neighbours match."""
    for route, expected in fx.GROUND_SEQUENCES:
        markup = fx.rendered(route)
        grounds = tuple(a.get("data-ground") for tag, a in fx.tags_with(markup, "data-ground") if tag != "footer")
        assert grounds == expected, f"{route} carries grounds {grounds}, expected {expected}"
        assert all(g in fx.GROUND_VALUES for g in grounds), f"{route} carries an unknown ground {grounds}"
        assert all(a != b for a, b in zip(grounds, grounds[1:])), f"{route} repeats a ground {grounds}"
        assert not [t for t, _ in fx.tags_with(markup, "data-ground") if t == "footer"], f"{route}'s footer carries a ground"


def test_routes_open_on_their_pinned_ground():
    """Every route opens dark except the case study index, which opens light."""
    for route, _ in fx.GROUND_SEQUENCES:
        first = fx.tags_with(fx.rendered(route), "data-ground")[0][1].get("data-ground")
        wanted = "light" if route == "/works" else "dark"
        assert first == wanted, f"{route} opens on {first!r} rather than {wanted!r}"


def test_no_binary_media_file_is_referenced():
    """No page references a video, model, raster or icon file."""
    for route in fx.PUBLIC_ROUTES + ("/not-a-real-page",):
        markup = fx.page(route).text
        found = fx.BINARY_REFERENCE_RE.findall(markup)
        assert not found, f"{route} references binary files: {found[:4]}"
        assert "<video" not in markup.lower(), f"{route} carries a video element"


def test_pages_reference_no_third_party_origin():
    """No page loads a script, style, image or frame from another origin."""
    own = httpx.URL(fx.app_url()).host
    for route in fx.PUBLIC_ROUTES:
        for tag, attrs in fx.tags_of(fx.rendered(route)):
            if tag not in fx.ASSET_TAGS:
                continue
            relation = attrs.get("rel", "")
            if tag == "link" and not any(kind in relation for kind in ("stylesheet", "preload", "icon", "modulepreload")):
                continue
            address = attrs.get("src") or attrs.get("href") or ""
            if address.startswith(("http://", "https://", "//")):
                host = httpx.URL(address if not address.startswith("//") else f"http:{address}").host
                assert host == own, f"{route} loads {address} from another origin"


def test_every_public_route_has_a_distinct_title_and_description():
    """Every public route carries its own title and meta description."""
    titles, descriptions = {}, {}
    for route in fx.PUBLIC_ROUTES:
        markup = fx.rendered(route)
        title = fx.title_of(markup)
        description = fx.head_meta(markup).get("description", "").strip()
        assert title, f"{route} carries no title"
        assert description, f"{route} carries no meta description"
        titles.setdefault(title, []).append(route)
        descriptions.setdefault(description, []).append(route)
    shared = {k: v for k, v in titles.items() if len(v) > 1}
    assert not shared, f"routes share a title: {shared}"
    shared = {k: v for k, v in descriptions.items() if len(v) > 1}
    assert not shared, f"routes share a description: {shared}"


def test_sitemap_lists_public_routes_and_robots_points_at_it():
    """The sitemap lists the public routes and published entries, and robots points at it."""
    paths = fx.sitemap_paths()
    wanted = set(fx.CONTENT_ROUTES) | {f"/works/{row[0]}" for row in fx.SEEDED_CASE_STUDIES} | {
        f"/blog/{row[0]}" for row in fx.SEEDED_ARTICLES} | {f"/blog-categories/{slug}" for slug, _ in fx.CATEGORIES}
    missing = sorted(wanted - paths)
    assert not missing, f"/sitemap.xml omits {missing[:8]}"
    robots = fx.page("/robots.txt")
    assert robots.status_code == 200, f"GET /robots.txt returned {robots.status_code}"
    lines = [line.split(":", 1)[1].strip() for line in robots.text.splitlines() if line.lower().startswith("sitemap:")]
    assert lines and lines[0].startswith("http") and httpx.URL(lines[0]).path == "/sitemap.xml", (
        f"/robots.txt carries no full Sitemap: line: {robots.text[:200]}"
    )


def test_every_public_route_declares_a_social_preview_that_resolves():
    """Every public route declares a preview title and a generated preview image."""
    home_image = fx.head_meta(fx.rendered("/")).get("og:image", "")
    assert httpx.URL(home_image).path == "/social-preview/home", f"the home preview image is {home_image!r}"
    for route in fx.PUBLIC_ROUTES:
        meta = fx.head_meta(fx.rendered(route))
        assert meta.get("og:title"), f"{route} declares no og:title"
        image = meta.get("og:image", "")
        path = httpx.URL(image).path
        assert path.startswith("/social-preview/"), f"{route} declares the preview image {image!r}"
        assert "." not in path.rsplit("/", 1)[-1], f"the preview image address {path} carries a file extension"
        response = fx.page(path)
        assert response.status_code == 200 and response.headers.get("content-type", "").startswith("image/"), (
            f"GET {path} returned {response.status_code} {response.headers.get('content-type')}"
        )


def test_terms_page_is_linked_from_footers_and_the_signup_form():
    """The terms page answers and is linked from footers and the sign-up form."""
    text = fx.page_text("/terms")
    assert "Terms of Service" in text and "enquiry" in text.lower(), "the terms page does not state its terms"
    signup = fx.rendered("/sign-up")
    assert fx.TERMS_SENTENCE in fx.visible_text(signup), "the sign-up form lacks the terms sentence"
    for route in fx.PUBLIC_ROUTES:
        if route in fx.FOOTERLESS_ROUTES:
            continue
        hrefs = {a.get("href") for tag, a in fx.tags_of(fx.rendered(route)) if tag == "a"}
        assert "/terms" in hrefs, f"{route} does not link to /terms"


def test_privacy_policy_names_the_removal_address():
    """The privacy policy states what is stored and how to ask for removal."""
    text = fx.page_text("/privacy-policy")
    assert "Privacy Policy" in text and fx.CONTACT_MAILBOX in text, "the privacy policy lacks its removal address"
    assert "enquiry" in text.lower() and "account" in text.lower(), "the privacy policy does not name what it stores"


def test_unknown_address_answers_not_found_with_the_pinned_copy():
    """An unknown address answers not-found with the site's own page."""
    response = fx.page(f"/nothing-here-{fx.unique_suffix()}")
    assert response.status_code == 404, f"an unknown address returned {response.status_code}"
    text = fx.visible_text(response.text)
    for value in (fx.NOT_FOUND_LINE, fx.NOT_FOUND_CODE, fx.NOT_FOUND_ACTION):
        assert value in text, f"the not-found page lacks {value!r}"
    links = [a for tag, a in fx.tags_of(response.text) if tag == "a" and a.get("href") == "/"]
    assert links, "the not-found page offers no link back to /"


def test_error_page_keeps_the_chrome_without_a_footer():
    """The not-found page keeps the header and drawer and carries no footer."""
    response = fx.page(f"/missing-{fx.unique_suffix()}")
    markup = response.text
    assert fx.tags_with(markup, "data-drawer") and fx.tags_with(markup, "data-drawer-trigger"), (
        "the not-found page drops the drawer"
    )
    for label in fx.HEADER_LINKS:
        assert label in fx.visible_text(markup), f"the not-found page drops the header link {label!r}"
    assert "<footer" not in markup.lower(), "the not-found page carries a footer"


def test_seeding_is_idempotent_across_restarts(backend):
    """Every seeded record exists exactly once."""
    for slug, *_ in fx.SEEDED_CASE_STUDIES:
        assert backend.count("case_study", slug=slug) == 1, f"case_study holds duplicate rows for {slug}"
    for slug, *_ in fx.SEEDED_ARTICLES:
        assert backend.count("article", slug=slug) == 1, f"article holds duplicate rows for {slug}"
    for email, _, _ in fx.SEEDED_ACCOUNTS:
        assert backend.count("app_user", email=email) == 1, f"app_user holds duplicate rows for {email}"
    assert backend.count("culture_value") == 7, "culture_value does not hold exactly seven rows"
    assert backend.count("testimonial") == 3, "testimonial does not hold exactly three rows"
    assert backend.count("award_badge") == 5, "award_badge does not hold exactly five rows"
    assert backend.count("team_member") == 6, "team_member does not hold exactly six rows"
    assert backend.count("office") == 2, "office does not hold exactly two rows"
    assert backend.count("article_category") == 3, "article_category does not hold exactly three rows"
    assert backend.count("enquiry", email=fx.ANONYMOUS_ENQUIRER_EMAIL) == 1, "the seeded anonymous enquiry is duplicated"
    owners = backend.query(
        "SELECT a.email FROM case_study c JOIN app_user a ON a.id = c.owner_id WHERE c.slug = %s",
        (fx.DRAFT_CASE_STUDY_SLUG,),
    )
    assert owners == [{"email": fx.EDITOR_EMAIL}], f"Nightjar is owned by {owners}"
