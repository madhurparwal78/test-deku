"""Deterministic observations of the deployed Spectre Studio Showcase app.

Every assertion is black box: the app is driven over HTTP on its own origin,
and the two backing services are read through the shared capability adapters.
Nothing here reads the agent's source, its schema, or its file layout.
"""

from __future__ import annotations

import conftest as fx


def _slugs(payload):
    return {row["slug"] for row in payload}


def _make_project(http, slug, title="Discovery Quests", client="Loomis"):
    return http.post(
        "/projects",
        json={
            "slug": slug,
            "title": title,
            "client": client,
            "year": "2026",
            "discipline": "Experience",
            "tags": ["ai", "motion"],
            "summary": "A generated probe project used to exercise the publish path.",
        },
    )


def test_health_endpoint_returns_ok(anon):
    """The app answers its health route once both backing services are reachable."""
    response = anon.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:300]}"
    )


def test_seeded_accounts_sign_in_with_corpus_password(anon):
    """Both seeded accounts sign in with the pinned password and carry their role."""
    for email, role in ((fx.CURATOR_EMAIL, fx.CURATOR_ROLE),
                        (fx.VISITOR_EMAIL, fx.VISITOR_ROLE)):
        response = anon.post("/auth/login", json={"email": email,
                                                  "password": fx.CORPUS_PASSWORD})
        assert response.status_code == 200, (
            f"login for {email} returned {response.status_code}: {response.text[:300]}"
        )
        body = response.json()
        assert body.get("access_token"), f"login for {email} returned no access_token"
        assert body.get("role") == role, (
            f"login for {email} reported role {body.get('role')!r}, expected {role!r}"
        )


def test_signup_creates_a_visitor_account(anon):
    """Open registration always produces a visitor, never a curator."""
    email = f"probe-{fx.unique_token()}@example.com"
    response = anon.post("/auth/signup", json={"email": email,
                                               "password": fx.CORPUS_PASSWORD})
    assert response.status_code in fx.CREATED, (
        f"signup returned {response.status_code}: {response.text[:300]}"
    )
    assert response.json().get("role") == fx.VISITOR_ROLE, (
        f"signup produced role {response.json().get('role')!r}, expected "
        f"{fx.VISITOR_ROLE!r}"
    )


def test_public_catalogue_lists_only_published_projects(anon):
    """The public catalogue carries the six published slugs and neither draft."""
    response = anon.get("/projects")
    assert response.status_code == 200, (
        f"GET /api/projects returned {response.status_code}: {response.text[:300]}"
    )
    payload = response.json()
    assert isinstance(payload, list), "GET /api/projects must return a JSON array"
    slugs = _slugs(payload)
    for slug in fx.PUBLISHED_SLUGS:
        assert slug in slugs, f"published project {slug!r} is absent from the catalogue"
    for slug in fx.DRAFT_SLUGS:
        assert slug not in slugs, f"draft project {slug!r} appears in the public catalogue"
    for row in payload:
        assert row.get("status") == fx.PUBLISHED_STATUS, (
            f"catalogue row {row.get('slug')!r} carries status {row.get('status')!r}"
        )


def test_public_count_endpoint_matches_published_total(anon):
    """The published count is computed from the rows rather than stored."""
    response = anon.get("/projects/count")
    assert response.status_code == 200, (
        f"GET /api/projects/count returned {response.status_code}"
    )
    reported = response.json().get("count")
    listed = len(anon.get("/projects").json())
    assert reported == listed, (
        f"the count endpoint reports {reported} while the catalogue lists {listed}"
    )
    assert reported >= fx.PUBLISHED_COUNT, (
        f"the count endpoint reports {reported}, below the {fx.PUBLISHED_COUNT} seeded "
        f"published projects"
    )


def test_published_ordering_follows_display_order_then_newest(anon):
    """The catalogue is ordered by display_order ascending, then newest first."""
    payload = anon.get("/projects").json()
    orders = [row.get("displayOrder") for row in payload]
    assert all(value is not None for value in orders), (
        "every catalogue row carries displayOrder"
    )
    assert orders == sorted(orders), (
        f"catalogue displayOrder values are not ascending: {orders}"
    )


def test_published_thumbnail_bytes_are_served_to_anonymous(anon):
    """A published project's stored image is readable without a session."""
    response = anon.get(f"/projects/{fx.PUBLISHED_SLUGS[0]}/thumbnail")
    assert response.status_code == 200, (
        f"the published thumbnail route returned {response.status_code}"
    )
    assert len(response.content) > 0, "the published thumbnail route returned no bytes"


def test_seeded_thumbnail_objects_exist_in_the_store(anon, store, curator):
    """Every seeded project, drafts included, has a real object in the bucket."""
    keys = set(store.list(fx.PROJECT_KEY_PREFIX))
    assert keys, (
        f"the bucket holds no object under {fx.PROJECT_KEY_PREFIX!r}; seeded thumbnails "
        f"must be real objects rather than local files"
    )
    console = curator.get("/studio/projects")
    assert console.status_code == 200, (
        f"GET /api/studio/projects returned {console.status_code}"
    )
    rows = {row["slug"]: row for row in console.json()}
    for slug in fx.SEEDED_SLUGS:
        assert slug in rows, f"seeded project {slug!r} is absent from the console"
        key = rows[slug].get("thumbnailKey")
        assert key, f"seeded project {slug!r} carries no thumbnailKey"
        assert key in keys, (
            f"seeded project {slug!r} names key {key!r}, which is not in the bucket"
        )


def test_draft_project_detail_is_refused_to_anonymous(anon):
    """A draft project is refused by slug with no session."""
    for slug in fx.DRAFT_SLUGS:
        response = anon.get(f"/projects/{slug}")
        assert response.status_code in fx.DENIED_OR_ABSENT, (
            f"anonymous GET /api/projects/{slug} returned {response.status_code}"
        )
        assert slug not in response.text, (
            f"the refusal for {slug!r} still discloses the project slug"
        )


def test_draft_project_detail_is_refused_to_visitor(visitor):
    """A draft project is refused by slug to a signed-in visitor."""
    for slug in fx.DRAFT_SLUGS:
        response = visitor.get(f"/projects/{slug}")
        assert response.status_code in fx.DENIED_OR_ABSENT, (
            f"visitor GET /api/projects/{slug} returned {response.status_code}"
        )


def test_draft_thumbnail_bytes_are_refused_to_anonymous(anon):
    """The draft image route returns no bytes and no redirect without a session."""
    response = anon.get(f"/projects/{fx.DRAFT_SLUGS[0]}/thumbnail",
                        follow_redirects=False)
    assert response.status_code in fx.DENIED_OR_ABSENT, (
        f"anonymous draft thumbnail request returned {response.status_code}"
    )
    assert "location" not in {k.lower() for k in response.headers}, (
        "the refusal redirected the caller to the object store"
    )


def test_draft_thumbnail_bytes_are_refused_to_visitor(visitor, store):
    """The draft image route refuses a visitor while the object still exists."""
    response = visitor.get(f"/projects/{fx.DRAFT_SLUGS[0]}/thumbnail",
                           follow_redirects=False)
    assert response.status_code in fx.DENIED_OR_ABSENT, (
        f"visitor draft thumbnail request returned {response.status_code}"
    )
    assert store.list(fx.PROJECT_KEY_PREFIX), (
        "the refusal removed or emptied the stored objects"
    )


def test_draft_thumbnail_bytes_are_served_to_curator(curator):
    """The same draft image is served to a signed-in curator."""
    response = curator.get(f"/projects/{fx.DRAFT_SLUGS[0]}/thumbnail")
    assert response.status_code == 200, (
        f"curator draft thumbnail request returned {response.status_code}"
    )
    assert len(response.content) > 0, "the curator received no image bytes"


def test_wizard_created_project_starts_as_draft(curator, anon):
    """A newly created project is a draft and stays out of the public catalogue."""
    slug = f"probe-project-{fx.unique_token()}"
    created = _make_project(curator, slug)
    assert created.status_code in fx.CREATED, (
        f"POST /api/projects returned {created.status_code}: {created.text[:300]}"
    )
    assert created.json().get("status") == fx.DRAFT_STATUS, (
        f"a created project carries status {created.json().get('status')!r}, expected "
        f"{fx.DRAFT_STATUS!r}"
    )
    assert slug not in _slugs(anon.get("/projects").json()), (
        f"the newly created draft {slug!r} is already on the public catalogue"
    )


def test_uploaded_thumbnail_lands_in_the_store_under_the_key_scheme(curator, store):
    """An uploaded image becomes a real object under the pinned key scheme."""
    slug = f"probe-upload-{fx.unique_token()}"
    created = _make_project(curator, slug)
    assert created.status_code in fx.CREATED, (
        f"POST /api/projects returned {created.status_code}: {created.text[:300]}"
    )
    upload = curator.post(
        f"/projects/{slug}/thumbnail",
        files={"file": ("probe.png", fx.PNG_BYTES, "image/png")},
    )
    assert upload.status_code in fx.CREATED, (
        f"the thumbnail upload returned {upload.status_code}: {upload.text[:300]}"
    )
    key = upload.json().get("thumbnailKey")
    assert key, "the upload response carries no thumbnailKey"
    assert key.startswith(fx.PROJECT_KEY_PREFIX), (
        f"the stored key {key!r} does not follow the projects/ key scheme"
    )
    assert fx.settle(lambda: store.exists(key)), (
        f"the uploaded bytes are not in the bucket at {key!r}"
    )


def test_publishing_reveals_the_project_and_raises_the_count(curator, anon):
    """Publishing adds the project to the public catalogue and moves the count."""
    slug = f"probe-publish-{fx.unique_token()}"
    created = _make_project(curator, slug)
    assert created.status_code in fx.CREATED, (
        f"POST /api/projects returned {created.status_code}: {created.text[:300]}"
    )
    before = anon.get("/projects/count").json()["count"]
    published = curator.post(f"/projects/{slug}/publish")
    assert published.status_code in fx.CREATED, (
        f"the publish call returned {published.status_code}: {published.text[:300]}"
    )
    assert published.json().get("status") == fx.PUBLISHED_STATUS, (
        f"the published project carries status {published.json().get('status')!r}"
    )
    assert published.json().get("publishedAt"), "publishing stamped no publishedAt"
    after = anon.get("/projects/count").json()["count"]
    assert after == before + 1, (
        f"the published count moved from {before} to {after}, expected {before + 1}"
    )
    assert slug in _slugs(anon.get("/projects").json()), (
        f"the published project {slug!r} is absent from the public catalogue"
    )
    again = curator.post(f"/projects/{slug}/publish")
    assert again.status_code in fx.CREATED, (
        f"republishing returned {again.status_code}, which reads as an error"
    )
    assert anon.get("/projects/count").json()["count"] == after, (
        "republishing changed the published count"
    )


def test_duplicate_slug_create_is_refused(curator, anon):
    """A create carrying a slug already taken leaves no second row behind."""
    before = len(curator.get("/studio/projects").json())
    response = _make_project(curator, fx.PUBLISHED_SLUGS[0], title="Duplicate Probe")
    assert response.status_code in fx.REFUSED_AS_INVALID, (
        f"a duplicate slug create returned {response.status_code}, expected a refusal"
    )
    after = curator.get("/studio/projects").json()
    assert len(after) == before, (
        f"the refused create left the project count at {len(after)}, was {before}"
    )
    titles = [row["title"] for row in after if row["slug"] == fx.PUBLISHED_SLUGS[0]]
    assert "Duplicate Probe" not in titles, (
        "the refused create overwrote the existing project"
    )


def test_visitor_cannot_create_a_project(visitor, curator):
    """A project create issued from a visitor session is refused at the API."""
    before = len(curator.get("/studio/projects").json())
    slug = f"probe-denied-{fx.unique_token()}"
    response = _make_project(visitor, slug)
    assert response.status_code in fx.DENIED, (
        f"a visitor create returned {response.status_code}, expected a denial"
    )
    assert len(curator.get("/studio/projects").json()) == before, (
        "the denied create still added a project row"
    )


def test_visitor_cannot_publish_a_project(visitor, curator, anon):
    """A publish issued from a visitor session is refused and changes nothing."""
    before = anon.get("/projects/count").json()["count"]
    response = visitor.post(f"/projects/{fx.DRAFT_SLUGS[1]}/publish")
    assert response.status_code in fx.DENIED_OR_ABSENT, (
        f"a visitor publish returned {response.status_code}, expected a denial"
    )
    assert anon.get("/projects/count").json()["count"] == before, (
        "the denied publish still moved the published count"
    )
    assert fx.DRAFT_SLUGS[1] not in _slugs(anon.get("/projects").json()), (
        f"the denied publish revealed {fx.DRAFT_SLUGS[1]!r} on the public catalogue"
    )


def test_public_roles_exclude_the_closed_role(anon):
    """The public roles list holds the four open roles and not the closed one."""
    response = anon.get("/roles")
    assert response.status_code == 200, f"GET /api/roles returned {response.status_code}"
    payload = response.json()
    assert isinstance(payload, list), "GET /api/roles must return a JSON array"
    slugs = _slugs(payload)
    for slug in fx.OPEN_ROLE_SLUGS:
        assert slug in slugs, f"open role {slug!r} is absent from the public list"
    assert fx.CLOSED_ROLE_SLUG not in slugs, (
        f"closed role {fx.CLOSED_ROLE_SLUG!r} appears in the public list"
    )
    for row in payload:
        assert row.get("open") is True, (
            f"public role {row.get('slug')!r} is not open"
        )
    direct = anon.get(f"/roles/{fx.CLOSED_ROLE_SLUG}")
    assert direct.status_code in fx.DENIED_OR_ABSENT, (
        f"a direct request for the closed role returned {direct.status_code}"
    )


def test_enquiry_persists_and_returns_its_reference(anon, curator):
    """A stored enquiry returns an ENQ reference the curator inbox also shows."""
    marker = fx.unique_token()
    response = anon.post(
        "/enquiries",
        json={
            "intent": fx.INTENTS[0],
            "readiness": fx.READINESS_STOPS[1],
            "name": "Probe Sender",
            "email": f"probe-{marker}@example.com",
            "company": "Probe Company",
            "message": f"probe {marker}",
        },
    )
    assert response.status_code in fx.CREATED, (
        f"POST /api/enquiries returned {response.status_code}: {response.text[:300]}"
    )
    reference = response.json().get("reference")
    assert reference, "the enquiry response carries no reference"
    assert reference.startswith(fx.ENQUIRY_REFERENCE_PREFIX), (
        f"the enquiry reference {reference!r} does not begin "
        f"{fx.ENQUIRY_REFERENCE_PREFIX!r}"
    )
    inbox = curator.get("/enquiries")
    assert inbox.status_code == 200, f"GET /api/enquiries returned {inbox.status_code}"
    stored = [row for row in inbox.json() if row.get("reference") == reference]
    assert stored, f"the enquiry reference {reference!r} is absent from the inbox"
    assert stored[0].get("readiness") == fx.READINESS_STOPS[1], (
        f"the stored enquiry carries readiness {stored[0].get('readiness')!r}"
    )
    assert stored[0].get("intent") == fx.INTENTS[0], (
        f"the stored enquiry carries intent {stored[0].get('intent')!r}"
    )


def test_enquiry_missing_a_required_field_is_refused(anon, curator):
    """An enquiry missing a required field is refused and stores nothing."""
    before = len(curator.get("/enquiries").json())
    marker = fx.unique_token()
    response = anon.post(
        "/enquiries",
        json={
            "intent": fx.INTENTS[0],
            "readiness": fx.READINESS_STOPS[0],
            "name": "Probe Sender",
            "email": f"probe-{marker}@example.com",
            "company": "",
            "message": f"probe {marker}",
        },
    )
    assert response.status_code in fx.REFUSED_AS_INVALID, (
        f"an enquiry with an empty company returned {response.status_code}"
    )
    assert response.status_code < 500, "a refused enquiry must not be a server error"
    assert len(curator.get("/enquiries").json()) == before, (
        "the refused enquiry was stored anyway"
    )


def test_wildcard_application_file_lands_in_the_store(anon, store):
    """The wildcard application stores its file under the applications key scheme."""
    marker = fx.unique_token()
    response = anon.post(
        "/applications",
        data={
            "name": "Probe Applicant",
            "email": f"probe-{marker}@example.com",
            "portfolioUrl": "https://example.com/probe",
            "message": f"probe {marker}",
        },
        files={"file": ("probe.png", fx.PNG_BYTES, "image/png")},
    )
    assert response.status_code in fx.CREATED, (
        f"POST /api/applications returned {response.status_code}: {response.text[:300]}"
    )
    body = response.json()
    reference = body.get("reference")
    assert reference, "the application response carries no reference"
    assert reference.startswith(fx.APPLICATION_REFERENCE_PREFIX), (
        f"the application reference {reference!r} does not begin "
        f"{fx.APPLICATION_REFERENCE_PREFIX!r}"
    )
    assert fx.settle(lambda: bool(store.list(fx.APPLICATION_KEY_PREFIX))), (
        f"the bucket holds no object under {fx.APPLICATION_KEY_PREFIX!r}"
    )


def test_site_config_returns_offices_and_counts(anon):
    """The configuration document drives the offices, the links and the counts."""
    response = anon.get("/config")
    assert response.status_code == 200, f"GET /api/config returned {response.status_code}"
    payload = response.json()
    for key in ("offices", "social", "legal", "counts"):
        assert key in payload, f"GET /api/config omits {key!r}"
    cities = {office.get("city") for office in payload["offices"]}
    assert {"London", "Auckland"} <= cities, (
        f"the configuration names offices {sorted(cities)}, expected London and Auckland"
    )
    functions = {row.get("function") for row in payload["counts"]}
    assert set(fx.DISCIPLINES) <= functions, (
        f"the configuration counts cover {sorted(functions)}, expected the three "
        f"disciplines"
    )


def test_privacy_page_is_reachable_and_states_what_is_stored(site):
    """The privacy page answers publicly and names what an enquiry stores."""
    response = site.get("/privacy")
    assert response.status_code == 200, (
        f"the privacy route returned {response.status_code}"
    )
    body = response.text.lower()
    assert any(word in body for word in ("privacy", "store", "data")), (
        "the privacy page names nothing it stores"
    )


def test_terms_page_is_reachable_from_every_route(site):
    """The terms page answers publicly."""
    response = site.get("/terms")
    assert response.status_code == 200, (
        f"the terms route returned {response.status_code}"
    )
    assert len(response.text) > 0, "the terms route returned an empty document"


def test_no_credential_appears_in_anything_the_browser_downloads(site):
    """No served document leaks a database, object-store or account credential."""
    secrets = ("deku-local-dev", "minio-root", "minioadmin", fx.CORPUS_PASSWORD)
    for route in ("/", "/privacy", "/terms"):
        served = site.get(route)
        if served.status_code != 200:
            continue
        lowered = served.text.lower()
        for secret in secrets:
            assert secret.lower() not in lowered, (
                f"the document at {route} carries the credential {secret!r}"
            )


def test_every_response_carries_the_security_headers(anon):
    """Responses declare a strict transport policy and a nosniff content type."""
    response = anon.get("/health")
    headers = {k.lower(): v.lower() for k, v in response.headers.items()}
    assert "strict-transport-security" in headers, (
        f"no strict transport policy on the response; headers were {sorted(headers)}"
    )
    assert headers.get("x-content-type-options") == "nosniff", (
        f"the nosniff content-type policy is {headers.get('x-content-type-options')!r}"
    )


def test_sitemap_lists_public_routes_and_robots_points_at_it(site):
    """A sitemap lists the public routes and the robots file points at it."""
    sitemap = site.get("/sitemap.xml")
    assert sitemap.status_code == 200, (
        f"the sitemap returned {sitemap.status_code}"
    )
    for route in ("/about", "/careers", "/privacy"):
        assert route in sitemap.text, f"the sitemap omits the public route {route}"
    robots = site.get("/robots.txt")
    assert robots.status_code == 200, f"the robots file returned {robots.status_code}"
    assert "sitemap" in robots.text.lower(), (
        "the robots file does not point at the sitemap"
    )
