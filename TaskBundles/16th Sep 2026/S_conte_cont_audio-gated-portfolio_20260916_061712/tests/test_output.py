from __future__ import annotations

import concurrent.futures
import hashlib
import os
import re

import httpx
from _shapes import flatten, items
from appclient import api_base, app_url, client, login
from conftest import (
    AUTHOR2_EMAIL,
    AUTHOR_EMAIL,
    BLOCK_KINDS,
    CORPUS_PASSWORD,
    DRAFT,
    DRAFT_SLUG,
    FACETS,
    LEAD_SLUG,
    POSTER_MAX_BYTES,
    POSTER_PREFIX,
    PUBLISHED,
    READER_EMAIL,
    SECOND_SLUG,
    SEEDED_ENQUIRY_REFERENCE,
    STUDIO_CONTACT_EMAIL,
    THIRD_SLUG,
    enquiry_payload,
    project_payload,
    published_slugs,
    settle,
)

PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)

RESERVED_SEGMENTS = ("projects", "world", "contact", "login", "signup", "studio", "api")


def app_root() -> str:
    return app_url() + "/"


def absolute(path: str) -> str:
    return app_url() + path if path.startswith("/") else app_url() + "/" + path


def _fail(anchor: str, request: str, response) -> str:
    return (
        f"{anchor}: {request} returned {response.status_code} "
        f"with body {response.text[:400]!r}"
    )


def test_health_endpoint_answers_ready(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, _fail(
        "readiness", "GET /api/health", response
    )


def test_login_issues_bearer_token(anon_client):
    response = anon_client.post(
        "/auth/login", json={"email": AUTHOR_EMAIL, "password": CORPUS_PASSWORD}
    )
    assert response.status_code == 200, _fail(
        "author login", "POST /api/auth/login", response
    )
    assert response.json().get("access_token"), (
        f"author login returned no access_token: {response.text[:400]!r}"
    )


def test_published_projects_listed_by_position(anon_client):
    response = anon_client.get("/projects")
    assert response.status_code == 200, _fail(
        "public wall", "GET /api/projects", response
    )
    slugs = published_slugs(response.json())
    assert slugs == [LEAD_SLUG, SECOND_SLUG, THIRD_SLUG], (
        f"GET /api/projects returned {slugs!r}, expected the three published slugs "
        f"in position order"
    )


def test_projects_list_is_top_level_array(anon_client):
    response = anon_client.get("/projects")
    assert response.status_code == 200, _fail(
        "public wall", "GET /api/projects", response
    )
    payload = response.json()
    assert isinstance(payload, list), (
        f"GET /api/projects returned {type(payload).__name__}, not a top-level array: "
        f"{response.text[:400]!r}"
    )


def test_draft_project_absent_from_public_list(anon_client, db):
    response = anon_client.get("/projects")
    assert response.status_code == 200, _fail(
        "public wall", "GET /api/projects", response
    )
    slugs = published_slugs(response.json())
    assert DRAFT_SLUG not in slugs, (
        f"the draft slug {DRAFT_SLUG!r} appears on the public wall: {slugs!r}"
    )
    row = db.project_by_slug(DRAFT_SLUG)
    assert row is not None, f"the seeded draft project {DRAFT_SLUG!r} is missing from projects"
    assert row["status"] == DRAFT, (
        f"the seeded project {DRAFT_SLUG!r} has status {row['status']!r}, expected {DRAFT!r}"
    )


def test_facet_filter_returns_only_matching_projects(anon_client):
    response = anon_client.get("/projects", params={"facet": "Motion"})
    assert response.status_code == 200, _fail(
        "facet filter", "GET /api/projects?facet=Motion", response
    )
    slugs = published_slugs(response.json())
    assert sorted(slugs) == sorted([LEAD_SLUG, THIRD_SLUG]), (
        f"GET /api/projects?facet=Motion returned {slugs!r}, expected the two Motion projects"
    )


def test_empty_facet_returns_empty_array(anon_client):
    response = anon_client.get("/projects", params={"facet": "Nonexistent"})
    assert response.status_code == 200, _fail(
        "empty facet", "GET /api/projects?facet=Nonexistent", response
    )
    assert items(response.json()) == [], (
        f"an unmatched facet returned {response.text[:400]!r}, expected an empty array"
    )


def test_case_study_returns_ordered_blocks(anon_client, db):
    response = anon_client.get(f"/projects/{LEAD_SLUG}")
    assert response.status_code == 200, _fail(
        "case study", f"GET /api/projects/{LEAD_SLUG}", response
    )
    project = db.project_by_slug(LEAD_SLUG)
    assert project is not None, f"the seeded project {LEAD_SLUG!r} is missing from projects"
    rows = db.blocks_for(project["id"])
    assert len(rows) == 5, (
        f"project {LEAD_SLUG!r} has {len(rows)} block rows, expected the five seeded blocks"
    )
    positions = [r["position"] for r in sorted(rows, key=lambda r: r["position"])]
    assert positions == sorted(positions), (
        f"project {LEAD_SLUG!r} block positions are {positions!r}, expected an ordered run"
    )
    for row in rows:
        assert row["kind"] in BLOCK_KINDS, (
            f"project {LEAD_SLUG!r} carries block kind {row['kind']!r}, "
            f"outside the four pinned kinds {BLOCK_KINDS!r}"
        )


def test_case_study_returns_ordered_awards(anon_client, db):
    response = anon_client.get(f"/projects/{LEAD_SLUG}")
    assert response.status_code == 200, _fail(
        "case study", f"GET /api/projects/{LEAD_SLUG}", response
    )
    project = db.project_by_slug(LEAD_SLUG)
    assert project is not None, f"the seeded project {LEAD_SLUG!r} is missing from projects"
    rows = db.awards_for(project["id"])
    assert len(rows) == 2, (
        f"project {LEAD_SLUG!r} has {len(rows)} award rows, expected the two seeded awards"
    )
    positions = sorted(r["position"] for r in rows)
    assert positions == [1, 2], (
        f"project {LEAD_SLUG!r} award positions are {positions!r}, expected [1, 2]"
    )


def test_globals_row_seeded_and_served(anon_client, db):
    assert db.count_globals() == 1, (
        f"site_globals holds {db.count_globals()} rows, expected exactly one"
    )
    response = anon_client.get("/globals")
    assert response.status_code == 200, _fail(
        "studio globals", "GET /api/globals", response
    )
    assert STUDIO_CONTACT_EMAIL in flatten(response.json()), (
        f"GET /api/globals does not carry {STUDIO_CONTACT_EMAIL!r}: {response.text[:400]!r}"
    )


def test_enquiry_stored_row_returns_reference(anon_client, db, unique_email, unique_message):
    before = db.count_enquiries()
    response = anon_client.post(
        "/enquiries",
        json=enquiry_payload("Probe Visitor", unique_email, unique_message),
    )
    assert response.status_code in (200, 201), _fail(
        "enquiry submission", "POST /api/enquiries", response
    )
    reference = response.json().get("reference")
    assert reference, (
        f"POST /api/enquiries returned no reference: {response.text[:400]!r}"
    )
    stored = db.enquiries(email=unique_email)
    assert len(stored) == 1, (
        f"POST /api/enquiries stored {len(stored)} rows for {unique_email!r}, expected one"
    )
    assert db.count_enquiries() == before + 1, (
        f"the enquiries table moved from {before} to {db.count_enquiries()}, expected one new row"
    )
    assert db.count_enquiries(reference=SEEDED_ENQUIRY_REFERENCE) == 1, (
        f"the seeded enquiry {SEEDED_ENQUIRY_REFERENCE!r} is missing from the enquiries table"
    )


def test_duplicate_enquiry_stores_one_row(anon_client, db, unique_email, unique_message):
    body = enquiry_payload("Probe Visitor", unique_email, unique_message)
    first = anon_client.post("/enquiries", json=body)
    assert first.status_code in (200, 201), _fail(
        "first enquiry", "POST /api/enquiries", first
    )
    settle()
    second = anon_client.post("/enquiries", json=body)
    assert second.status_code in (200, 201), _fail(
        "replayed enquiry", "POST /api/enquiries", second
    )
    assert db.count_enquiries(email=unique_email) == 1, (
        f"replaying the same enquiry left "
        f"{db.count_enquiries(email=unique_email)} rows for {unique_email!r}, expected one"
    )
    assert first.json().get("reference") == second.json().get("reference"), (
        f"replay returned reference {second.json().get('reference')!r}, "
        f"expected the first reference {first.json().get('reference')!r}"
    )


def test_invalid_enquiry_refused_and_nothing_stored(anon_client, db, unique_email):
    before = db.count_enquiries()
    response = anon_client.post(
        "/enquiries",
        json={"name": "", "email": "not-an-address", "message": ""},
    )
    assert 400 <= response.status_code < 500, _fail(
        "invalid enquiry", "POST /api/enquiries", response
    )
    assert db.count_enquiries() == before, (
        f"an invalid enquiry moved the table from {before} to {db.count_enquiries()}"
    )
    assert db.count_enquiries(email="not-an-address") == 0, (
        "an invalid enquiry email was stored despite the rejection"
    )


def test_honeypot_enquiry_stores_nothing(anon_client, db, unique_email, unique_message):
    before = db.count_enquiries()
    response = anon_client.post(
        "/enquiries",
        json=enquiry_payload(
            "Probe Visitor",
            unique_email,
            unique_message,
            company_website="https://spam.example.com",
        ),
    )
    assert response.status_code in (200, 201), _fail(
        "honeypot enquiry", "POST /api/enquiries", response
    )
    assert db.count_enquiries() == before, (
        f"a honeypot enquiry moved the table from {before} to {db.count_enquiries()}"
    )
    assert db.count_enquiries(email=unique_email) == 0, (
        f"a honeypot enquiry stored a row for {unique_email!r}"
    )


def test_project_route_reserved_segments_refused(author_client, db, unique_slug):
    before = db.count_projects()
    for segment in RESERVED_SEGMENTS:
        response = author_client.post("/projects", json=project_payload(segment))
        assert 400 <= response.status_code < 500, _fail(
            f"reserved slug {segment!r}", "POST /api/projects", response
        )
    assert db.count_projects() == before, (
        f"reserved-slug creations moved the projects table from {before} "
        f"to {db.count_projects()}"
    )


def test_project_slug_shape_refused(author_client, db):
    before = db.count_projects()
    for bad in ("m", "marlow", "M1", "m-"):
        response = author_client.post("/projects", json=project_payload(bad))
        assert 400 <= response.status_code < 500, _fail(
            f"malformed slug {bad!r}", "POST /api/projects", response
        )
    assert db.count_projects() == before, (
        f"malformed-slug creations moved the projects table from {before} "
        f"to {db.count_projects()}"
    )


def test_seed_counts_persisted_in_database(db):
    assert db.count_users(role="author") == 2, (
        f"the users table holds {db.count_users(role='author')} author rows, expected two"
    )
    assert db.count_users(role="reader") >= 1, (
        f"the users table holds {db.count_users(role='reader')} reader rows, expected at least one"
    )
    assert db.count_projects() >= 4, (
        f"the projects table holds {db.count_projects()} rows, expected the four seeded projects"
    )
    assert db.count_projects(status=PUBLISHED) == 3, (
        f"the projects table holds {db.count_projects(status=PUBLISHED)} published rows, expected three"
    )
    assert db.count_projects(status=DRAFT) >= 1, (
        f"the projects table holds {db.count_projects(status=DRAFT)} draft rows, expected at least one"
    )
    assert db.count_pages(slug="contact") == 1, (
        "the pages table has no row with slug 'contact'"
    )
    for email in (AUTHOR_EMAIL, AUTHOR2_EMAIL, READER_EMAIL):
        assert db.user_by_email(email) is not None, (
            f"the seeded account {email!r} is missing from the users table"
        )


def test_published_at_set_exactly_on_published_rows(db):
    for row in db.projects():
        if row["status"] == PUBLISHED:
            assert row.get("published_at") is not None, (
                f"published project {row['slug']!r} has a null published_at"
            )
        else:
            assert row.get("published_at") is None, (
                f"draft project {row['slug']!r} carries published_at {row.get('published_at')!r}"
            )


def test_lead_flag_on_exactly_one_stored_row(db):
    leads = [r for r in db.projects() if r.get("lead")]
    assert len(leads) == 1, (
        f"the projects table holds {len(leads)} rows with lead true, expected exactly one"
    )
    assert leads[0]["status"] == PUBLISHED, (
        f"the lead project {leads[0]['slug']!r} has status {leads[0]['status']!r}, "
        f"expected {PUBLISHED!r}"
    )


def test_reader_denied_author_only_endpoints(reader_client, db, unique_slug):
    before = db.count_projects()
    created = reader_client.post("/projects", json=project_payload(unique_slug))
    assert created.status_code in (401, 403), _fail(
        "reader creating a project", "POST /api/projects", created
    )
    queue = reader_client.get("/enquiries")
    assert queue.status_code in (401, 403), _fail(
        "reader reading the enquiry queue", "GET /api/enquiries", queue
    )
    promoted = reader_client.patch(f"/projects/{LEAD_SLUG}", json={"lead": True})
    assert promoted.status_code in (401, 403), _fail(
        "reader promoting a project", f"PATCH /api/projects/{LEAD_SLUG}", promoted
    )
    assert db.count_projects() == before, (
        f"a denied reader moved the projects table from {before} to {db.count_projects()}"
    )


def test_anonymous_cannot_read_draft_project(anon_client, db):
    row = db.project_by_slug(DRAFT_SLUG)
    assert row is not None, f"the seeded draft project {DRAFT_SLUG!r} is missing"
    response = anon_client.get(f"/projects/{DRAFT_SLUG}")
    assert response.status_code in (401, 403, 404), _fail(
        "anonymous draft read", f"GET /api/projects/{DRAFT_SLUG}", response
    )
    after = db.project_by_slug(DRAFT_SLUG)
    assert after["status"] == DRAFT, (
        f"the denied read changed {DRAFT_SLUG!r} to status {after['status']!r}"
    )


def test_other_author_cannot_read_draft_project(author2_client, author_client, db):
    owner = author_client.get(f"/projects/{DRAFT_SLUG}")
    assert owner.status_code == 200, _fail(
        "owning author draft read", f"GET /api/projects/{DRAFT_SLUG}", owner
    )
    intruder = author2_client.get(f"/projects/{DRAFT_SLUG}")
    assert intruder.status_code in (401, 403, 404), _fail(
        "other author draft read", f"GET /api/projects/{DRAFT_SLUG}", intruder
    )
    row = db.project_by_slug(DRAFT_SLUG)
    assert row["status"] == DRAFT, (
        f"the denied read changed {DRAFT_SLUG!r} to status {row['status']!r}"
    )


def test_expired_token_rejected_and_row_unchanged(db):
    before = db.project_by_slug(LEAD_SLUG)
    with client("expired.bearer.token") as bad:
        response = bad.patch(f"/projects/{LEAD_SLUG}", json={"title": "Rewritten"})
    assert response.status_code in (401, 403), _fail(
        "stale bearer token", f"PATCH /api/projects/{LEAD_SLUG}", response
    )
    after = db.project_by_slug(LEAD_SLUG)
    assert after["title"] == before["title"], (
        f"a rejected stale-token call changed the title of {LEAD_SLUG!r} from "
        f"{before['title']!r} to {after['title']!r}"
    )


def test_signup_creates_reader_not_author(anon_client, db, unique_email):
    response = anon_client.post(
        "/auth/signup", json={"email": unique_email, "password": CORPUS_PASSWORD}
    )
    assert response.status_code in (200, 201), _fail(
        "open signup", "POST /api/auth/signup", response
    )
    row = db.user_by_email(unique_email)
    assert row is not None, f"signup stored no users row for {unique_email!r}"
    assert row["role"] == "reader", (
        f"signup created {unique_email!r} with role {row['role']!r}, expected 'reader'"
    )


def test_concurrent_lead_promotion_yields_at_most_one(author_client, author_token, db):
    targets = (SECOND_SLUG, THIRD_SLUG)
    base = api_base()
    headers = {"Authorization": f"Bearer {author_token}"}

    def promote(slug: str) -> int:
        return httpx.patch(
            f"{base}/projects/{slug}", json={"lead": True}, headers=headers, timeout=30.0
        ).status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        statuses = list(pool.map(promote, targets))

    winners = [s for s in statuses if 200 <= s < 300]
    assert len(winners) <= 1, (
        f"two simultaneous promotions of {targets!r} both succeeded with {statuses!r}"
    )
    settle()
    leads = [r for r in db.projects() if r.get("lead")]
    assert len(leads) == 1, (
        f"after simultaneous promotion the projects table holds {len(leads)} lead rows, "
        f"expected exactly one"
    )


def test_unknown_path_is_not_found(anon_client):
    unknown = "zz"
    response = anon_client.get(f"/projects/{unknown}")
    assert response.status_code in (401, 403, 404), _fail(
        "unknown project slug", f"GET /api/projects/{unknown}", response
    )


def test_published_poster_object_present_in_bucket(anon_client, db, store):
    row = db.project_by_slug(LEAD_SLUG)
    assert row is not None, f"the seeded project {LEAD_SLUG!r} is missing"
    key = row.get("poster_key")
    assert key, f"the seeded project {LEAD_SLUG!r} carries no poster_key"
    assert store.exists(key), (
        f"poster_key {key!r} on project {LEAD_SLUG!r} names no object in the bucket"
    )
    response = anon_client.get(f"/posters/{LEAD_SLUG}")
    assert response.status_code == 200, _fail(
        "published poster", f"GET /api/posters/{LEAD_SLUG}", response
    )


def test_uploaded_poster_object_key_matches_scheme(author_client, db, store, unique_slug):
    created = author_client.post("/projects", json=project_payload(unique_slug))
    assert created.status_code in (200, 201), _fail(
        "author creating a project", "POST /api/projects", created
    )
    upload = author_client.post(
        f"/projects/{unique_slug}/poster",
        content=PNG_BYTES,
        headers={"Content-Type": "image/png"},
    )
    assert upload.status_code in (200, 201), _fail(
        "poster upload", f"POST /api/projects/{unique_slug}/poster", upload
    )
    key = upload.json().get("poster_key")
    assert key, f"the poster upload returned no poster_key: {upload.text[:400]!r}"
    digest = hashlib.sha256(PNG_BYTES).hexdigest()
    assert key == f"{POSTER_PREFIX}{unique_slug}/{digest}.png", (
        f"the poster upload produced key {key!r}, expected "
        f"{POSTER_PREFIX}{unique_slug}/{digest}.png"
    )
    assert store.exists(key), f"the uploaded poster key {key!r} names no object in the bucket"
    assert len(PNG_BYTES) <= POSTER_MAX_BYTES, (
        "the probe image exceeds the pinned poster byte ceiling"
    )
    row = db.project_by_slug(unique_slug)
    assert row is not None and row.get("poster_key") == key, (
        f"the projects row for {unique_slug!r} does not carry the uploaded key {key!r}"
    )


def test_draft_poster_object_denied_to_anonymous_media_request(
    anon_client, reader_client, author2_client, author_client, db, store
):
    row = db.project_by_slug(DRAFT_SLUG)
    assert row is not None, f"the seeded draft project {DRAFT_SLUG!r} is missing"
    key = row.get("poster_key")
    assert key, f"the seeded draft project {DRAFT_SLUG!r} carries no poster_key"
    assert store.exists(key), (
        f"the draft poster key {key!r} names no object in the bucket"
    )
    for name, caller in (
        ("anonymous", anon_client),
        ("reader", reader_client),
        ("other author", author2_client),
    ):
        response = caller.get(f"/posters/{DRAFT_SLUG}")
        assert response.status_code in (401, 403, 404), _fail(
            f"{name} draft poster read", f"GET /api/posters/{DRAFT_SLUG}", response
        )
    owner = author_client.get(f"/posters/{DRAFT_SLUG}")
    assert owner.status_code == 200, _fail(
        "owning author draft poster read", f"GET /api/posters/{DRAFT_SLUG}", owner
    )
    direct = httpx.get(
        f"{os.environ['STORAGE_ENDPOINT'].rstrip('/')}/{os.environ['STORAGE_BUCKET']}/{key}",
        timeout=30.0,
    )
    assert direct.status_code >= 400, (
        f"the draft poster object {key!r} is readable straight from the bucket with "
        f"status {direct.status_code}"
    )
def test_favicon_served_and_declared_in_head(anon_client):
    root = httpx.get(app_root(), timeout=30.0)
    assert root.status_code == 200, (
        f"index route: GET / returned {root.status_code} with body {root.text[:300]!r}"
    )
    head = root.text[:root.text.lower().find("</head>") + 7]
    link = re.search(r'<link[^>]+rel=["\'][^"\']*icon[^"\']*["\'][^>]*>', head, re.I)
    assert link, (
        f"the document head declares no favicon link: {head[:400]!r}"
    )
    href = re.search(r'href=["\']([^"\']+)["\']', link.group(0), re.I)
    assert href, f"the favicon link carries no href: {link.group(0)!r}"
    served = httpx.get(absolute(href.group(1)), timeout=30.0)
    assert served.status_code == 200, (
        f"favicon: GET {href.group(1)} returned {served.status_code}"
    )
    assert served.content, f"favicon at {href.group(1)} is empty"


def test_security_headers_on_every_response(anon_client):
    seen = {}
    for path in ("/", "/projects", "/contact", "/terms"):
        response = httpx.get(absolute(path), timeout=30.0)
        assert response.status_code == 200, (
            f"public route {path}: GET returned {response.status_code} with body "
            f"{response.text[:300]!r}"
        )
        lowered = {k.lower(): v for k, v in response.headers.items()}
        seen[path] = sorted(lowered)
        assert lowered.get("x-content-type-options", "").lower() == "nosniff", (
            f"{path} carries no nosniff content-type policy: {seen[path]}"
        )
        assert "strict-transport-security" in lowered, (
            f"{path} carries no strict transport policy: {seen[path]}"
        )


def test_no_frontend_secrets_in_downloaded_assets(anon_client):
    root = httpx.get(app_root(), timeout=30.0)
    assert root.status_code == 200, (
        f"index route: GET / returned {root.status_code}"
    )
    bodies = [root.text]
    for src in re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', root.text, re.I):
        asset = httpx.get(absolute(src), timeout=30.0)
        assert asset.status_code == 200, (
            f"script {src} returned {asset.status_code} to a browser that just asked for it"
        )
        bodies.append(asset.text)
    forbidden = (
        os.environ["STORAGE_SECRET_KEY"],
        os.environ["STORAGE_ACCESS_KEY"],
        os.environ["DATABASE_URL"],
        CORPUS_PASSWORD,
    )
    for body in bodies:
        for secret in forbidden:
            assert secret not in body, (
                f"a downloaded asset carries the literal {secret[:6]!r}..., which the browser "
                f"must never receive"
            )


def test_internal_links_resolve_on_public_routes(anon_client):
    checked = set()
    for path in ("/", "/projects", "/contact", "/terms", f"/{LEAD_SLUG}"):
        page = httpx.get(absolute(path), timeout=30.0)
        assert page.status_code == 200, (
            f"public route {path}: GET returned {page.status_code}"
        )
        for href in re.findall(r'<a[^>]+href=["\'](/[^"\'#?]*)["\']', page.text, re.I):
            if href in checked:
                continue
            checked.add(href)
            target = httpx.get(absolute(href), timeout=30.0)
            assert target.status_code == 200, (
                f"internal link {href!r} found on {path} returned {target.status_code}, "
                f"so it resolves to nothing"
            )
    assert checked, "no internal link was found on any public route"


def test_terms_page_reachable_from_footer_and_signup(anon_client):
    terms = httpx.get(absolute("/terms"), timeout=30.0)
    assert terms.status_code == 200, (
        f"terms page: GET /terms returned {terms.status_code} with body {terms.text[:300]!r}"
    )
    assert len(terms.text) > 200, (
        f"the terms page is effectively empty: {terms.text[:300]!r}"
    )
    for path in ("/", "/projects", "/contact", "/signup"):
        page = httpx.get(absolute(path), timeout=30.0)
        assert page.status_code == 200, (
            f"public route {path}: GET returned {page.status_code}"
        )
        assert re.search(r'href=["\']/terms["\']', page.text, re.I), (
            f"{path} carries no link to the terms page"
        )
