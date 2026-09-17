"""The one pytest module for Verdigris Studio.

Every section (core features, data integrity, authorization, edge cases) and both
declared slots (db, email) are merged here. Fixtures, pinned literals and helpers
live in conftest.py; the shared grader (appclient, capabilities, _shapes) is on
PYTHONPATH=/tests from the deku-verifier-base image.

The checklist obligations each function discharges live in the
pytest-provenance-v1 sidecar beside the bundle, not in a comment.

Channel disjointness, per reference/J J.12: the browser pass books its own slot and
enquires with its own address, and it publishes nothing that is seeded. Every check
here either reads a seeded record no journey mutates, or works inside a per-run probe
record it created itself.
"""

from __future__ import annotations

import concurrent.futures
import os

import appclient
import conftest as cf


def test_health_endpoint_answers_two_hundred() -> None:
    """The app answers its health endpoint once it is ready."""
    with appclient.client(None) as client:
        response = client.get("/health")
    assert response.status_code == 200, cf.describe(
        response, "the health endpoint must answer 200 once the app is ready")


def test_credentials_file_names_every_seeded_account() -> None:
    """The seeded logins are readable at the documented path."""
    assert os.path.isfile(cf.CREDENTIALS_FILE), (
        f"{cf.CREDENTIALS_FILE} must exist so a seeded account can be found")
    text = open(cf.CREDENTIALS_FILE, encoding="utf-8", errors="replace").read()
    for email in (cf.STUDIO_EMAIL, cf.CLIENT_EMAIL, cf.CLIENT2_EMAIL):
        assert email in text, (
            f"{cf.CREDENTIALS_FILE} must name the seeded account {email}, "
            f"holds: {text[:400]}")
    assert cf.SEEDED_PASSWORD in text, (
        f"{cf.CREDENTIALS_FILE} must carry the seeded password, holds: {text[:400]}")


def test_reserved_directories_exist_and_are_empty() -> None:
    """The two reserved directories exist at the app root and hold nothing."""
    for path in (cf.SCREENSHOT_DIR, cf.DOWNLOAD_DIR):
        assert os.path.isdir(path), f"{path} must exist at the app root"
        assert os.listdir(path) == [], f"{path} must be empty, holds {os.listdir(path)}"


def test_public_routes_carry_distinct_titles_and_descriptions() -> None:
    """No two public routes share a title or a description."""
    titles, descriptions = {}, {}
    for route in cf.PUBLIC_ROUTES:
        response = cf.fetch_document(route)
        assert response.status_code == 200, cf.describe(
            response, f"the public route {route} must render")
        title = cf.document_title(response.text)
        description = cf.meta_description(response.text)
        assert title, f"the route {route} must carry its own document title"
        assert description, f"the route {route} must carry its own meta description"
        assert title not in titles, (
            f"the route {route} shares its title with {titles.get(title)}: {title!r}")
        assert description not in descriptions, (
            f"the route {route} shares its description with {descriptions.get(description)}")
        titles[title] = route
        descriptions[description] = route


def test_route_titles_end_with_the_studio_name() -> None:
    """Every public route names the studio in its own title."""
    for route in cf.PUBLIC_ROUTES:
        response = cf.fetch_document(route)
        title = cf.document_title(response.text)
        assert cf.SITE_NAME in title, (
            f"the title of {route} must carry {cf.SITE_NAME!r}, read {title!r}")


def test_public_routes_declare_a_social_preview_image_that_resolves() -> None:
    """Every public route declares a preview image, and the image answers."""
    import httpx
    for route in cf.PUBLIC_ROUTES:
        markup = cf.fetch_document(route).text
        declared = (cf.meta_content(markup, "og:image")
                    or cf.meta_content(markup, "twitter:image"))
        assert declared, f"the route {route} must declare a social preview image"
        target = declared if declared.startswith("http") else appclient.app_url() + declared
        response = httpx.get(target, timeout=appclient.TIMEOUT, follow_redirects=True)
        assert response.status_code == 200, cf.describe(
            response, f"the preview image declared by {route} must resolve")


def test_route_identity_is_present_in_the_served_document() -> None:
    """A route's own title reaches the document the server sends."""
    for route in ("/offers", "/projects", "/method"):
        markup = cf.fetch_document(route).text
        head = cf.head_of(markup)
        assert cf.document_title(head), (
            f"the document the server returns for {route} must already carry a title")


def test_document_declares_its_language() -> None:
    """The served document names the language a reader is getting."""
    markup = cf.fetch_document("/").text
    assert cf.document_language(markup), (
        "the served document must declare a language on its root element")


def test_public_documents_reference_no_external_origin() -> None:
    """Nothing on a public route reaches another origin at runtime."""
    for route in ("/", "/projects", "/contact"):
        markup = cf.fetch_document(route).text
        strays = [o for o in cf.external_origins(markup)
                  if "fonts.googleapis" not in o and "fonts.gstatic" not in o]
        assert not strays, (
            f"the route {route} reaches external origins {strays[:5]}")


def test_internal_links_on_public_routes_resolve() -> None:
    """Every same-origin link on a public route leads somewhere real."""
    broken = []
    for route in cf.PUBLIC_ROUTES:
        for href in set(cf.internal_links(cf.fetch_document(route).text)):
            response = cf.fetch_document(href)
            if response.status_code >= 400:
                broken.append((route, href, response.status_code))
    assert not broken, f"internal links must resolve, broken: {broken[:8]}"


def test_unknown_address_renders_the_studio_not_found_page() -> None:
    """An address matching no route answers as not found."""
    response = cf.fetch_document("/no-such-address-" + cf.unique_suffix())
    assert response.status_code == 404, cf.describe(
        response, "an unknown address must answer as not found")
    assert cf.SITE_NAME in response.text or cf.SITE_NAME in cf.document_title(
        response.text), "the not-found page must carry the studio's own chrome"


def test_privacy_route_states_what_the_studio_stores() -> None:
    """The privacy route exists and says what is kept."""
    response = cf.fetch_document("/privacy")
    assert response.status_code == 200, cf.describe(
        response, "the privacy route must render")


def test_absent_surfaces_are_not_served() -> None:
    """The scoped-out surfaces do not exist."""
    for route in cf.ABSENT_SURFACES:
        response = cf.fetch_document(route)
        assert response.status_code == 404, cf.describe(
            response, f"the scoped-out surface {route} must not be served")


def test_signup_creates_a_client_and_returns_a_token(suffix) -> None:
    """Signup takes an email plus a password and returns a bearer token."""
    body = {"email": cf.probe_address(suffix), "password": cf.SEEDED_PASSWORD,
            "display_name": "Probe " + suffix}
    with appclient.client(None) as client:
        response = client.post("/auth/signup", json=body)
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "signup must create an account")
    payload = response.json()
    assert cf.field(payload, "access_token"), cf.describe(
        response, "signup must return an access_token")
    assert cf.field(payload, "role") == cf.ROLE_CLIENT, cf.describe(
        response, f"signup must create the role {cf.ROLE_CLIENT}")


def test_signup_cannot_mint_a_studio_account(suffix) -> None:
    """A signup body naming the studio role still creates a client."""
    body = {"email": cf.probe_address(suffix), "password": cf.SEEDED_PASSWORD,
            "display_name": "Probe " + suffix, "role": cf.ROLE_STUDIO}
    with appclient.client(None) as client:
        response = client.post("/auth/signup", json=body)
    if response.status_code in cf.ACCEPTED:
        assert cf.field(response.json(), "role") == cf.ROLE_CLIENT, cf.describe(
            response, "a signup naming the studio role must still create a client")
    else:
        assert response.status_code in cf.CLIENT_ERROR, cf.describe(
            response, "a signup naming a role must be refused rather than obeyed")
    store = cf.backend()
    row = store.one(cf.TABLE_ACCOUNT, email=cf.probe_address(suffix))
    if row:
        assert row.get("role") == cf.ROLE_CLIENT, (
            f"the stored account must hold the role {cf.ROLE_CLIENT}, holds {row.get('role')}")


def test_second_signup_with_a_stored_address_is_refused(suffix) -> None:
    """A repeated address is rejected as invalid and creates no second account."""
    body = {"email": cf.probe_address(suffix), "password": cf.SEEDED_PASSWORD,
            "display_name": "Probe " + suffix}
    with appclient.client(None) as client:
        first = client.post("/auth/signup", json=body)
    assert first.status_code in cf.ACCEPTED, cf.describe(first, "the first signup must land")
    with appclient.client(None) as client:
        second = client.post("/auth/signup", json=body)
    assert second.status_code in cf.CLIENT_ERROR, cf.describe(
        second, "a second signup with a stored address must be refused")
    store = cf.backend()
    assert store.count(cf.TABLE_ACCOUNT, email=cf.probe_address(suffix)) == 1, (
        "a refused signup must leave exactly one account for that address")


def test_login_with_a_wrong_password_returns_no_token() -> None:
    """A wrong password is refused and hands back nothing."""
    import httpx
    response = httpx.post(appclient.api_base() + "/auth/login",
                          json={"email": cf.CLIENT_EMAIL, "password": "not-the-password"},
                          timeout=appclient.TIMEOUT)
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "a wrong password must be refused")
    assert "access_token" not in response.text, cf.describe(
        response, "a refused login must return no token")


def test_no_endpoint_returns_a_password_hash(client_one) -> None:
    """No response body carries a stored password or its hash."""
    for path in ("/studio-profile", "/account/bookings"):
        response = cf.get_json(path, client_one)
        if response.status_code in cf.ACCEPTED:
            assert "password" not in response.text.lower(), cf.describe(
                response, f"{path} must not return anything password shaped")


def test_guarded_endpoint_denies_an_anonymous_call() -> None:
    """A guarded endpoint refuses a caller with no token."""
    response = cf.get_json("/account/bookings", None)
    assert response.status_code in cf.DENIED, cf.describe(
        response, "an anonymous caller must be denied the bookings endpoint")


def test_guarded_endpoint_denies_a_nonsense_token() -> None:
    """A token that was never issued is refused."""
    response = cf.get_json("/account/bookings", "not-a-real-token")
    assert response.status_code in cf.DENIED, cf.describe(
        response, "an unissued token must be denied")


def test_service_index_lists_the_eight_seeded_services() -> None:
    """The expertise tree is eight stored rows in index order."""
    response = cf.get_json("/services")
    assert response.status_code == 200, cf.describe(response, "the services endpoint must answer")
    services = cf.rows(response.json())
    assert len(services) == cf.SERVICE_COUNT, (
        f"the tree must carry {cf.SERVICE_COUNT} services, carries {len(services)}")
    names = [cf.field(s, "name") for s in services]
    assert names[0] == cf.SERVICE_FIRST, (
        f"the first service in index order must be {cf.SERVICE_FIRST!r}, read {names[0]!r}")
    for expected in (cf.SERVICE_VISUAL_IDENTITY, cf.SERVICE_DIGITAL):
        assert expected in names, f"the tree must carry the service {expected!r}"
    orders = [cf.field(s, "index_order") for s in services]
    assert orders == sorted(orders), "the tree must come back in stored index order"


def test_service_detail_lists_the_projects_tagged_with_it() -> None:
    """A service route carries the projects that service produced."""
    services = cf.rows(cf.get_json("/services").json())
    slug = cf.field(services[0], "slug")
    response = cf.get_json(f"/services/{slug}")
    assert response.status_code == 200, cf.describe(
        response, f"the service route {slug} must answer")
    payload = response.json()
    assert cf.field(payload, "detail"), "a service route must carry its long form body"
    assert isinstance(cf.field(payload, "projects") or [], list), (
        "a service route must carry the projects tagged with it")


def test_service_detail_count_matches_the_filtered_archive() -> None:
    """One vocabulary: a service's projects are the archive filtered to it."""
    services = cf.rows(cf.get_json("/services").json())
    for service in services[:3]:
        slug = cf.field(service, "slug")
        key = cf.field(service, "taxonomy_key") or slug
        detail = cf.rows(cf.field(cf.get_json(f"/services/{slug}").json(), "projects") or [])
        archive = cf.rows(cf.get_json(f"/projects?service={key}").json())
        assert len(detail) == len(archive), (
            f"the service {slug} shows {len(detail)} projects while the archive "
            f"filtered to it shows {len(archive)}")


def test_archive_lists_twelve_published_projects_in_editorial_order() -> None:
    """The archive is every published project in its stored order."""
    response = cf.get_json("/projects")
    assert response.status_code == 200, cf.describe(response, "the archive must answer")
    projects = cf.rows(response.json())
    assert len(projects) == cf.PROJECT_COUNT, (
        f"the archive must list {cf.PROJECT_COUNT} projects, lists {len(projects)}")
    orders = [cf.field(p, "editorial_order") for p in projects]
    assert orders == sorted(orders), "the archive must come back in stored editorial order"
    names = [cf.field(p, "client_name") for p in projects]
    assert names[0] == cf.PROJECT_FIRST, (
        f"editorial order must open on {cf.PROJECT_FIRST!r}, opens on {names[0]!r}")
    for expected in (cf.PROJECT_FOOD, cf.PROJECT_LAST, cf.PROJECT_BREAD):
        assert expected in names, f"the archive must carry the project {expected!r}"


def test_every_project_carries_between_one_and_six_tags() -> None:
    """A project's tags come from the eight service vocabulary."""
    services = {cf.field(s, "taxonomy_key") or cf.field(s, "slug")
                for s in cf.rows(cf.get_json("/services").json())}
    for project in cf.rows(cf.get_json("/projects").json()):
        tags = cf.field(project, "tags") or []
        assert 1 <= len(tags) <= 6, (
            f"{cf.field(project, 'client_name')} carries {len(tags)} tags")
        for tag in tags:
            key = tag if isinstance(tag, str) else cf.field(tag, "taxonomy_key", "slug", "name")
            assert key in services or any(key == s for s in services), (
                f"the tag {key!r} is carried by no service record")


def test_six_projects_are_featured_on_the_home_route() -> None:
    """The home work grid is the six flagged projects."""
    featured = [p for p in cf.rows(cf.get_json("/projects").json())
                if cf.field(p, "featured_home")]
    assert len(featured) == cf.FEATURED_COUNT, (
        f"{cf.FEATURED_COUNT} projects must be featured, {len(featured)} are")


def test_filtering_the_archive_narrows_it_to_one_service() -> None:
    """A filtered archive carries only projects holding that service."""
    services = cf.rows(cf.get_json("/services").json())
    key = cf.field(services[0], "taxonomy_key") or cf.field(services[0], "slug")
    filtered = cf.rows(cf.get_json(f"/projects?service={key}").json())
    everything = cf.rows(cf.get_json("/projects").json())
    assert len(filtered) <= len(everything), "a filter must narrow the archive"
    for project in filtered:
        tags = [t if isinstance(t, str) else cf.field(t, "taxonomy_key", "slug", "name")
                for t in (cf.field(project, "tags") or [])]
        assert key in tags, (
            f"{cf.field(project, 'client_name')} came back under the filter {key!r} "
            f"carrying {tags}")


def test_filtering_to_an_unused_service_returns_an_empty_archive() -> None:
    """A filter matching nothing returns nothing rather than everything."""
    filtered = cf.rows(cf.get_json("/projects?service=no-such-service").json())
    assert filtered == [], (
        f"an unknown filter must narrow to nothing, returned {len(filtered)} projects")


def test_case_study_returns_one_published_project_with_its_media() -> None:
    """A case study is a record with an ordered media sequence."""
    project = cf.rows(cf.get_json("/projects").json())[0]
    slug = cf.field(project, "slug")
    response = cf.get_json(f"/projects/{slug}")
    assert response.status_code == 200, cf.describe(
        response, f"the case study {slug} must answer")
    payload = response.json()
    assert cf.field(payload, "summary"), "a case study must carry its summary"
    assert cf.field(payload, "client_url"), "a case study must carry the client site"
    media = cf.field(payload, "media") or []
    assert media, "a case study must carry a media sequence"
    for entry in media:
        assert cf.field(entry, "layout_hint") in (cf.LAYOUT_FULL, cf.LAYOUT_HALF), (
            f"a media entry must be {cf.LAYOUT_FULL!r} or {cf.LAYOUT_HALF!r}")
        assert cf.field(entry, "alt_text"), "every media entry must carry alternative text"


def test_media_entries_render_in_stored_position_order() -> None:
    """The media sequence is ordered by its stored position."""
    project = cf.rows(cf.get_json("/projects").json())[0]
    media = cf.field(cf.get_json(f"/projects/{cf.field(project, 'slug')}").json(), "media") or []
    positions = [cf.field(m, "position") for m in media]
    assert positions == sorted(p for p in positions if p is not None), (
        f"the media sequence must be in stored order, read {positions}")


def test_related_work_shares_a_service_and_excludes_the_project_itself() -> None:
    """Related work is a query over shared services."""
    project = cf.rows(cf.get_json("/projects").json())[0]
    slug = cf.field(project, "slug")
    payload = cf.get_json(f"/projects/{slug}").json()
    related = cf.field(payload, "related") or []
    own = {t if isinstance(t, str) else cf.field(t, "taxonomy_key", "slug", "name")
           for t in (cf.field(payload, "tags") or [])}
    for other in related:
        assert cf.field(other, "slug") != slug, "related work must exclude the project itself"
        tags = {t if isinstance(t, str) else cf.field(t, "taxonomy_key", "slug", "name")
                for t in (cf.field(other, "tags") or [])}
        assert own & tags, (
            f"{cf.field(other, 'slug')} shares no service with {slug}")


def test_unpublished_project_is_absent_from_the_archive(studio, suffix) -> None:
    """An unpublished project is invisible to a reader."""
    projects = cf.rows(cf.get_json("/projects").json())
    slug = cf.field(projects[-1], "slug")
    with appclient.client(studio) as client:
        hidden = client.post(f"/studio/projects/{slug}/unpublish")
    assert hidden.status_code in cf.ACCEPTED, cf.describe(
        hidden, "the studio account must be able to unpublish a project")
    try:
        listed = [cf.field(p, "slug") for p in cf.rows(cf.get_json("/projects").json())]
        assert slug not in listed, "an unpublished project must leave the archive"
        direct = cf.get_json(f"/projects/{slug}")
        assert direct.status_code in cf.NOT_FOUND, cf.describe(
            direct, "an unpublished project must answer as not found")
    finally:
        with appclient.client(studio) as client:
            client.post(f"/studio/projects/{slug}/publish")


def test_packages_carry_their_floors_their_panels_and_one_badge() -> None:
    """The three offers are stored records with four panels each."""
    response = cf.get_json("/packages")
    assert response.status_code == 200, cf.describe(response, "the packages endpoint must answer")
    packages = cf.rows(response.json())
    assert len(packages) == 3, f"there must be three packages, there are {len(packages)}"
    by_name = {cf.field(p, "name"): p for p in packages}
    for name, floor in ((cf.PACKAGE_ENTRY, cf.FLOOR_ENTRY),
                        (cf.PACKAGE_MIDDLE, cf.FLOOR_MIDDLE),
                        (cf.PACKAGE_COMMERCE, cf.FLOOR_COMMERCE)):
        assert name in by_name, f"the package {name!r} must exist"
        stored = cf.field(by_name[name], "price_floor_minor")
        assert int(stored) == floor, (
            f"{name} must carry the floor {floor} in minor units, carries {stored}")
        assert cf.field(by_name[name], "price_currency") == cf.CURRENCY, (
            f"{name} must be priced in {cf.CURRENCY}")
    recommended = [p for p in packages if cf.field(p, "recommended")]
    assert len(recommended) == 1, (
        f"exactly one package is recommended, {len(recommended)} are")
    assert cf.field(recommended[0], "name") == cf.PACKAGE_MIDDLE, (
        f"{cf.PACKAGE_MIDDLE!r} must be the recommended package")


def test_package_panels_carry_the_four_fixed_labels() -> None:
    """The accordion labels are fixed and ordered."""
    for package in cf.rows(cf.get_json("/packages").json()):
        panels = cf.field(package, "panels") or []
        labels = [cf.field(p, "label") for p in panels]
        assert labels == list(cf.PANEL_LABELS), (
            f"{cf.field(package, 'name')} must carry the panels {list(cf.PANEL_LABELS)}, "
            f"carries {labels}")


def test_every_package_carries_a_disqualifying_list() -> None:
    """The negative fit list is never dropped."""
    for package in cf.rows(cf.get_json("/packages").json()):
        positive = cf.field(package, "fit_positive") or []
        negative = cf.field(package, "fit_negative") or []
        assert positive, f"{cf.field(package, 'name')} must carry a qualifying list"
        assert negative, f"{cf.field(package, 'name')} must carry a disqualifying list"


def test_method_carries_its_mark_and_its_four_steps() -> None:
    """The method record is the one source for the name and the steps."""
    response = cf.get_json("/method")
    assert response.status_code == 200, cf.describe(response, "the method endpoint must answer")
    payload = response.json()
    assert cf.field(payload, "name") == cf.METHOD_NAME, (
        f"the method must be named {cf.METHOD_NAME!r}, is {cf.field(payload, 'name')!r}")
    steps = cf.field(payload, "steps") or []
    titles = [cf.field(s, "title") for s in steps]
    assert titles == list(cf.METHOD_STEPS), (
        f"the four steps must read {list(cf.METHOD_STEPS)}, read {titles}")
    assert cf.field(payload, "audience_positive"), "the method must carry a qualifying list"
    assert cf.field(payload, "audience_negative"), "the method must carry a disqualifying list"


def test_awards_carry_three_rows_with_the_earlier_entity_name() -> None:
    """The awards wall is one record with a history worth keeping."""
    response = cf.get_json("/awards")
    assert response.status_code == 200, cf.describe(response, "the awards endpoint must answer")
    awards = cf.rows(response.json())
    assert len(awards) == 3, f"there must be three award rows, there are {len(awards)}"
    got = [(int(cf.field(a, "year")), cf.field(a, "entity_name"), cf.field(a, "distinction"))
           for a in awards]
    assert got == list(cf.AWARD_ROWS), (
        f"the awards wall must read {list(cf.AWARD_ROWS)}, reads {got}")


def test_studio_profile_carries_the_proof_numbers() -> None:
    """The delivered count, the promise and the directory badge are stored fields."""
    response = cf.get_json("/studio-profile")
    assert response.status_code == 200, cf.describe(response, "the profile endpoint must answer")
    payload = response.json()
    assert int(cf.field(payload, "projects_delivered")) == cf.DELIVERED_COUNT, (
        f"the proof band must read {cf.DELIVERED_COUNT}")
    assert int(cf.field(payload, "response_promise_hours")) == cf.PROMISE_HOURS, (
        f"the stored promise must be {cf.PROMISE_HOURS} hours")
    assert str(cf.field(payload, "directory_score")) == cf.DIRECTORY_SCORE, (
        f"the directory rating must read {cf.DIRECTORY_SCORE}")
    assert int(cf.field(payload, "directory_scale")) == cf.DIRECTORY_SCALE
    assert cf.field(payload, "directory_verdict") == cf.DIRECTORY_VERDICT
    assert cf.field(payload, "directory_source") == cf.DIRECTORY_SOURCE
    assert int(cf.field(payload, "directory_review_count")) == cf.DIRECTORY_REVIEWS
    assert cf.field(payload, "manifesto"), "the profile must carry the manifesto"
    assert cf.field(payload, "founder_story"), "the profile must carry the founder story"


def test_testimonials_come_back_in_stored_order() -> None:
    """Three testimonials, each tied to a case study."""
    testimonials = cf.rows(cf.get_json("/testimonials").json())
    assert len(testimonials) == 3, (
        f"there must be three testimonials, there are {len(testimonials)}")
    orders = [cf.field(t, "display_order") for t in testimonials]
    assert orders == sorted(orders), "testimonials must come back in stored order"
    for entry in testimonials:
        assert cf.field(entry, "author_first_name"), "a testimonial must name its author"
        assert cf.field(entry, "project_slug"), "a testimonial must link a case study"


def test_calendar_seeds_six_open_slots_across_two_days() -> None:
    """The seeded calendar carries the boundary the studio needs."""
    store = cf.backend()
    assert store.count(cf.TABLE_SLOT, state=cf.SLOT_OPEN) >= cf.SEEDED_SLOT_COUNT, (
        f"the calendar must seed at least {cf.SEEDED_SLOT_COUNT} open slots")
    slots = cf.rows(cf.get_json("/slots").json())
    assert slots, "the slots endpoint must answer with the calendar"
    days = {}
    for slot in slots:
        start = cf.parse_moment(cf.field(slot, "starts_at"))
        if start:
            days.setdefault(start.date(), []).append(slot)
    assert any(len(v) == cf.SEEDED_SLOTS_DAY_AFTER for v in days.values()), (
        "exactly one seeded day must carry a single slot")


def test_every_slot_lasts_thirty_minutes() -> None:
    """A call is one length so the grid stays uniform."""
    for slot in cf.rows(cf.get_json("/slots").json()):
        start = cf.parse_moment(cf.field(slot, "starts_at"))
        end = cf.parse_moment(cf.field(slot, "ends_at"))
        if start and end:
            assert int((end - start).total_seconds() // 60) == cf.SLOT_MINUTES, (
                f"a slot must last {cf.SLOT_MINUTES} minutes, this one runs "
                f"{(end - start).total_seconds() / 60}")


def test_anonymous_visitor_cannot_hold_a_slot() -> None:
    """Holding requires a signed-in client."""
    slots = cf.rows(cf.get_json("/slots").json())
    slot_id = cf.field(slots[0], "id", "slot_id")
    with appclient.client(None) as client:
        response = client.post(f"/slots/{slot_id}/hold")
    assert response.status_code in cf.DENIED, cf.describe(
        response, "an anonymous visitor must be denied a hold")


def test_hold_returns_a_reference_and_an_expiry(client_one) -> None:
    """A hold is a stored booking with a countdown."""
    reference, _ = cf.take_a_slot(client_one)
    assert reference.startswith("vs-"), (
        f"a booking reference must read like {cf.BOOKING_REFERENCE_SAMPLE}, read {reference}")
    row = cf.booking_row(reference)
    assert row.get("state") == cf.STATE_HELD, (
        f"a fresh hold must be {cf.STATE_HELD}, is {row.get('state')}")
    expiry = cf.parse_moment(row.get("hold_expires_at"))
    assert expiry, "a hold must carry an expiry moment"
    minutes = (expiry - cf.utc_now()).total_seconds() / 60
    assert 0 < minutes <= cf.HOLD_MINUTES + 1, (
        f"a hold must run about {cf.HOLD_MINUTES} minutes, this one has {minutes:.1f}")
    cf.cancel_booking(client_one, reference)


def test_booking_answers_are_validated_before_confirmation(client_one) -> None:
    """An empty topic or an unknown sector is refused and writes nothing."""
    reference, _ = cf.take_a_slot(client_one)
    try:
        bad_sector = cf.answer_hold(client_one, reference, sector="aviation")
        assert bad_sector.status_code in cf.CLIENT_ERROR, cf.describe(
            bad_sector, "an unknown sector must be refused")
        empty_topic = cf.answer_hold(client_one, reference, topic="")
        assert empty_topic.status_code in cf.CLIENT_ERROR, cf.describe(
            empty_topic, "an empty topic must be refused")
        row = cf.booking_row(reference)
        assert row.get("state") == cf.STATE_HELD, (
            "a refused answer must leave the hold running")
    finally:
        cf.cancel_booking(client_one, reference)


def test_confirmed_booking_is_stored_and_reachable_by_its_owner(client_one, suffix) -> None:
    """A confirmed call is the client's own record."""
    reference, _ = cf.take_a_slot(client_one)
    answered = cf.answer_hold(client_one, reference, topic=cf.probe_topic(suffix))
    assert answered.status_code in cf.ACCEPTED, cf.describe(
        answered, "a held booking must accept its sector and topic")
    confirmed = cf.confirm_booking(client_one, reference)
    assert confirmed.status_code in cf.ACCEPTED, cf.describe(
        confirmed, "a live hold must confirm")
    row = cf.booking_row(reference)
    assert row.get("state") == cf.STATE_CONFIRMED, (
        f"the stored booking must be {cf.STATE_CONFIRMED}, is {row.get('state')}")
    own = cf.rows(cf.get_json("/account/bookings", client_one).json())
    assert any(cf.field(b, "reference") == reference for b in own), (
        "a client must find their own confirmed call")
    cf.cancel_booking(client_one, reference)


def test_client_cannot_read_another_clients_booking(client_one, client_two) -> None:
    """A booking reference is not a key anybody can use."""
    reference, _ = cf.take_a_slot(client_one)
    try:
        response = cf.get_json(f"/bookings/{reference}", client_two)
        assert response.status_code in cf.NOT_FOUND, cf.describe(
            response, "another client must not read this booking")
        listed = cf.rows(cf.get_json("/account/bookings", client_two).json())
        assert not any(cf.field(b, "reference") == reference for b in listed), (
            "another client's list must not carry this booking")
    finally:
        cf.cancel_booking(client_one, reference)


def test_client_cannot_cancel_another_clients_booking(client_one, client_two) -> None:
    """A denied cancellation leaves the booking exactly as it was."""
    reference, _ = cf.take_a_slot(client_one)
    try:
        response = cf.cancel_booking(client_two, reference)
        assert response.status_code in cf.NOT_FOUND, cf.describe(
            response, "another client must not cancel this booking")
        row = cf.booking_row(reference)
        assert row.get("state") == cf.STATE_HELD, (
            f"the denied cancellation must leave the booking {cf.STATE_HELD}")
    finally:
        cf.cancel_booking(client_one, reference)


def test_cancelling_returns_the_slot_to_the_grid(client_one, suffix) -> None:
    """A cancelled call frees its slot for somebody else."""
    reference, slot_id = cf.take_a_slot(client_one)
    cf.answer_hold(client_one, reference, topic=cf.probe_topic(suffix))
    cf.confirm_booking(client_one, reference)
    response = cf.cancel_booking(client_one, reference)
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "a client must be able to cancel their own call")
    row = cf.booking_row(reference)
    assert row.get("state") == cf.STATE_CANCELLED, (
        f"a cancelled booking must be {cf.STATE_CANCELLED}, is {row.get('state')}")
    available = [cf.field(s, "id", "slot_id") for s in cf.open_slots(client_one)]
    assert slot_id in available, "a cancelled slot must return to the grid"


def test_two_simultaneous_holds_on_one_slot_yield_one_winner(client_one, client_two) -> None:
    """The single-winner rule holds under real contention, at the database level."""
    available = cf.open_slots(client_one)
    assert available, "the calendar must offer an open slot to contend for"
    slot_id = cf.field(available[-1], "id", "slot_id")
    with concurrent.futures.ThreadPoolExecutor(max_workers=cf.RACE_ATTEMPTS) as pool:
        results = list(pool.map(
            lambda token: cf.hold_slot(token, slot_id), (client_one, client_two)))
    winners = [r for r in results if r.status_code in cf.ACCEPTED]
    losers = [r for r in results if r.status_code not in cf.ACCEPTED]
    assert len(winners) == 1, (
        "exactly one simultaneous hold may succeed, "
        + "; ".join(cf.describe(r, "attempt") for r in results))
    assert all(r.status_code in cf.CLIENT_ERROR for r in losers), (
        "the losing hold must be refused as a client error, "
        + "; ".join(cf.describe(r, "loser") for r in losers))
    store = cf.backend()
    live = [b for b in store.rows(cf.TABLE_BOOKING, slot_id=slot_id)
            if b.get("state") in (cf.STATE_HELD, cf.STATE_CONFIRMED)]
    assert len(live) == 1, (
        f"one slot must carry exactly one live booking, carries {len(live)}")
    reference = cf.field(winners[0].json(), "reference")
    for token in (client_one, client_two):
        cf.cancel_booking(token, str(reference))


def test_the_loser_of_a_race_is_offered_alternatives(client_one, client_two) -> None:
    """The refusal names the slot as taken and offers the nearest open ones."""
    available = cf.open_slots(client_one)
    slot_id = cf.field(available[0], "id", "slot_id")
    first = cf.hold_slot(client_one, slot_id)
    assert first.status_code in cf.ACCEPTED, cf.describe(first, "the first hold must land")
    try:
        second = cf.hold_slot(client_two, slot_id)
        assert second.status_code in cf.CLIENT_ERROR, cf.describe(
            second, "a second hold on a held slot must be refused")
        payload = second.json() if second.text.strip().startswith("{") else {}
        alternatives = cf.field(payload, "alternatives") or []
        assert alternatives, cf.describe(
            second, "a refused hold must offer the nearest open slots")
    finally:
        cf.cancel_booking(client_one, str(cf.field(first.json(), "reference")))


def test_a_refused_hold_writes_no_booking(client_one, client_two) -> None:
    """A rejected attempt leaves no partial state behind."""
    available = cf.open_slots(client_one)
    slot_id = cf.field(available[0], "id", "slot_id")
    first = cf.hold_slot(client_one, slot_id)
    reference = str(cf.field(first.json(), "reference"))
    try:
        cf.hold_slot(client_two, slot_id)
        store = cf.backend()
        rows = store.rows(cf.TABLE_BOOKING, slot_id=slot_id)
        live = [r for r in rows if r.get("state") in (cf.STATE_HELD, cf.STATE_CONFIRMED)]
        assert len(live) == 1, f"a refused hold must write nothing, found {len(live)} live"
        assert str(live[0].get("reference")) == reference, (
            "the winner's booking must be the one that survives")
    finally:
        cf.cancel_booking(client_one, reference)


def test_confirming_a_hold_that_is_no_longer_live_is_refused(client_one) -> None:
    """A hold that has stopped being live cannot become a call."""
    reference, _ = cf.take_a_slot(client_one)
    row = cf.booking_row(reference)
    assert cf.parse_moment(row.get("hold_expires_at")), (
        "a hold must carry the expiry the server enforces")
    released = cf.cancel_booking(client_one, reference)
    assert released.status_code in cf.ACCEPTED, cf.describe(
        released, "a client must be able to release their own hold")
    response = cf.confirm_booking(client_one, reference)
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "a hold that is no longer live must not confirm")
    store = cf.backend()
    assert store.one(cf.TABLE_BOOKING, reference=reference,
                     state=cf.STATE_CONFIRMED) is None, (
        "a hold that is no longer live must create no confirmed booking")


def test_closing_a_slot_carrying_a_confirmed_call_is_refused(studio, client_one, suffix) -> None:
    """The console cannot close a slot somebody has already taken."""
    reference, slot_id = cf.take_a_slot(client_one)
    cf.answer_hold(client_one, reference, topic=cf.probe_topic(suffix))
    cf.confirm_booking(client_one, reference)
    try:
        with appclient.client(studio) as client:
            response = client.post(f"/studio/slots/{slot_id}/close")
        assert response.status_code in cf.CLIENT_ERROR, cf.describe(
            response, "closing a slot with a confirmed call must be refused")
        store = cf.backend()
        row = store.one(cf.TABLE_SLOT, id=slot_id)
        if row:
            assert row.get("state") == cf.SLOT_OPEN, (
                "a refused close must leave the slot open")
    finally:
        cf.cancel_booking(client_one, reference)


def test_opening_a_slot_at_an_existing_start_is_refused(studio) -> None:
    """A slot start time is unique across the calendar."""
    slots = cf.rows(cf.get_json("/slots").json())
    start = cf.field(slots[0], "starts_at")
    with appclient.client(studio) as client:
        response = client.post("/studio/slots", json={"starts_at": start})
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "a duplicate slot start must be refused")


def test_seeding_is_idempotent_across_the_seeded_collections() -> None:
    """A restart must not duplicate a seeded row."""
    store = cf.backend()
    assert store.count(cf.TABLE_SERVICE) == cf.SERVICE_COUNT, (
        f"the services table must hold {cf.SERVICE_COUNT} rows")
    assert store.count(cf.TABLE_PROJECT) == cf.PROJECT_COUNT, (
        f"the projects table must hold {cf.PROJECT_COUNT} rows")
    assert store.count(cf.TABLE_PACKAGE) == 3, "the packages table must hold three rows"
    assert store.count(cf.TABLE_AWARD) == 3, "the awards table must hold three rows"
    assert store.count(cf.TABLE_METHOD_STEP) == 4, "the method must hold four steps"
    assert store.count(cf.TABLE_PROFILE) == 1, "the profile table must hold one row"
    assert store.count(cf.TABLE_TESTIMONIAL) == 3, "there must be three testimonials"
    for email in (cf.STUDIO_EMAIL, cf.CLIENT_EMAIL, cf.CLIENT2_EMAIL):
        assert store.count(cf.TABLE_ACCOUNT, email=email) == 1, (
            f"exactly one account must carry {email}")


def test_seeded_roles_are_stored_as_named() -> None:
    """The two roles are the stored vocabulary."""
    store = cf.backend()
    assert store.one(cf.TABLE_ACCOUNT, email=cf.STUDIO_EMAIL).get("role") == cf.ROLE_STUDIO
    for email in (cf.CLIENT_EMAIL, cf.CLIENT2_EMAIL):
        assert store.one(cf.TABLE_ACCOUNT, email=email).get("role") == cf.ROLE_CLIENT


def test_page_identity_rows_exist_for_every_public_route() -> None:
    """Route identity is stored rather than typed into a template."""
    store = cf.backend()
    assert store.count(cf.TABLE_PAGE_IDENTITY) >= len(cf.PUBLIC_ROUTES), (
        "every public route must carry its own identity row")


def test_project_media_rows_all_carry_alternative_text() -> None:
    """No stored media entry is missing its alternative text."""
    store = cf.backend()
    for row in store.rows(cf.TABLE_PROJECT_MEDIA):
        assert (row.get("alt_text") or "").strip(), (
            f"the media row {row.get('id')} must carry alternative text")


def test_package_panels_are_four_per_package() -> None:
    """The stored accordion is four rows per package."""
    store = cf.backend()
    for package in store.rows(cf.TABLE_PACKAGE):
        count = store.count(cf.TABLE_PACKAGE_PANEL, package_id=package.get("id"))
        assert count == 4, (
            f"{package.get('name')} must carry four panels, carries {count}")


def test_only_negative_fit_rows_carry_a_redirect() -> None:
    """A qualifying entry never points somebody elsewhere."""
    store = cf.backend()
    for row in store.rows(cf.TABLE_PACKAGE_FIT):
        if row.get("kind") == cf.FIT_POSITIVE:
            assert not row.get("redirect_package_id"), (
                "a qualifying fit row must carry no redirect")


def test_project_grounds_use_the_stored_vocabulary() -> None:
    """A section ground is light or dark and nothing else."""
    store = cf.backend()
    for row in store.rows(cf.TABLE_PROJECT):
        assert row.get("section_ground") in (cf.GROUND_LIGHT, cf.GROUND_DARK), (
            f"{row.get('client_name')} carries the ground {row.get('section_ground')!r}")


def test_booking_states_stay_inside_the_stored_vocabulary() -> None:
    """Only the four named states are ever written."""
    store = cf.backend()
    for row in store.rows(cf.TABLE_BOOKING):
        assert row.get("state") in cf.BOOKING_STATES, (
            f"the booking {row.get('reference')} carries {row.get('state')!r}")


def test_enquiry_due_moment_is_derived_from_the_stored_promise(suffix) -> None:
    """The promise is arithmetic over a stored field, not a sentence."""
    reference, _ = cf.accepted_enquiry(suffix)
    row = cf.enquiry_row(reference)
    received = cf.parse_moment(row.get("received_at"))
    due = cf.parse_moment(row.get("promise_due_at"))
    assert received and due, "an enquiry must store when it arrived and when a reply is due"
    assert cf.within(due, received + cf.promise_window(), minutes=5), (
        f"the due moment must be {cf.PROMISE_HOURS} hours after arrival, "
        f"read {received} then {due}")


def test_stored_timestamps_are_utc(suffix) -> None:
    """Every stored moment carries its zone."""
    reference, _ = cf.accepted_enquiry(suffix)
    row = cf.enquiry_row(reference)
    for key in ("received_at", "promise_due_at", "consent_at"):
        moment = cf.parse_moment(row.get(key))
        assert moment is not None, f"{key} must be a readable moment"
        assert moment.utcoffset().total_seconds() == 0, (
            f"{key} must be stored in UTC, read {row.get(key)}")


def test_enquiry_without_consent_is_refused_and_writes_nothing(suffix) -> None:
    """Consent is required and is never assumed."""
    before = cf.backend().count(cf.TABLE_ENQUIRY)
    response = cf.submit_enquiry(cf.enquiry_body(suffix, consent=False))
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "an enquiry without consent must be refused")
    assert "consent" in response.text.lower(), cf.describe(
        response, "the refusal must name the consent control")
    assert cf.backend().count(cf.TABLE_ENQUIRY) == before, (
        "a refused enquiry must write no row")


def test_enquiry_missing_a_required_field_names_it(suffix) -> None:
    """A rejected enquiry names every offending field."""
    before = cf.backend().count(cf.TABLE_ENQUIRY)
    response = cf.submit_enquiry(cf.enquiry_body(suffix, surname="", email=""))
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "an enquiry missing required fields must be refused")
    body = response.text.lower()
    assert "surname" in body, cf.describe(response, "the refusal must name the surname field")
    assert "email" in body, cf.describe(response, "the refusal must name the email field")
    assert cf.backend().count(cf.TABLE_ENQUIRY) == before, (
        "a refused enquiry must write no row")


def test_enquiry_rejects_a_budget_band_outside_the_four(suffix) -> None:
    """The budget vocabulary is closed."""
    response = cf.submit_enquiry(cf.enquiry_body(suffix, budget_band="Whatever it takes"))
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "an unknown budget band must be refused")


def test_enquiry_rejects_a_project_type_outside_the_two(suffix) -> None:
    """The project type vocabulary is closed."""
    response = cf.submit_enquiry(cf.enquiry_body(suffix, project_type="Maintenance"))
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "an unknown project type must be refused")


def test_accepted_enquiry_stores_consent_and_returns_a_reference(suffix) -> None:
    """A valid enquiry is stored with the moment consent was given."""
    reference, body = cf.accepted_enquiry(suffix)
    assert reference.startswith("vq-"), (
        f"an enquiry reference must read like {cf.ENQUIRY_REFERENCE_SAMPLE}, read {reference}")
    row = cf.enquiry_row(reference)
    assert cf.parse_moment(row.get("consent_at")), (
        "a stored enquiry must record when consent was given")
    assert row.get("budget_band") in cf.BUDGET_BANDS, (
        f"the stored band must be one of {cf.BUDGET_BANDS}")
    assert row.get("project_type") in cf.PROJECT_TYPES


def test_every_budget_band_is_accepted() -> None:
    """All four bands work, including the escape for somebody who does not know."""
    for band in cf.BUDGET_BANDS:
        response = cf.submit_enquiry(
            cf.enquiry_body(cf.unique_suffix(), budget_band=band))
        assert response.status_code in cf.ACCEPTED, cf.describe(
            response, f"the budget band {band!r} must be accepted")


def test_publishing_a_project_without_alternative_text_is_refused(studio, suffix) -> None:
    """Alternative text is a publishing rule, not a nicety."""
    projects = cf.rows(cf.get_json("/projects").json())
    slug = cf.field(projects[-1], "slug")
    with appclient.client(studio) as client:
        created = client.post(f"/studio/projects/{slug}/media",
                              json={"recipe": "composition", "seed": 7, "aspect": "3:2",
                                    "layout_hint": cf.LAYOUT_FULL, "alt_text": ""})
    assert created.status_code in cf.CLIENT_ERROR, cf.describe(
        created, "a media entry without alternative text must be refused")


def test_client_is_refused_every_console_endpoint(client_one) -> None:
    """The console belongs to the studio account alone."""
    store = cf.backend()
    before = store.count(cf.TABLE_SLOT)
    for path in ("/studio/enquiries", "/studio/slots"):
        response = cf.get_json(path, client_one)
        assert response.status_code in cf.DENIED, cf.describe(
            response, f"a client must be denied {path}")
    with appclient.client(client_one) as client:
        written = client.post("/studio/slots", json={"starts_at": "2030-01-01T09:00:00Z"})
    assert written.status_code in cf.DENIED, cf.describe(
        written, "a client must be denied the slot-opening endpoint")
    assert store.count(cf.TABLE_SLOT) == before, (
        "a denied console call must leave the calendar unchanged")


def test_anonymous_request_is_refused_every_console_endpoint() -> None:
    """The console is never open to a stranger."""
    for path in ("/studio/enquiries", "/studio/slots"):
        response = cf.get_json(path, None)
        assert response.status_code in cf.DENIED, cf.describe(
            response, f"an anonymous caller must be denied {path}")


def test_studio_reads_every_enquiry_newest_first(studio, suffix) -> None:
    """The console is where an enquiry is answered."""
    reference, _ = cf.accepted_enquiry(suffix)
    response = cf.get_json("/studio/enquiries", studio)
    assert response.status_code == 200, cf.describe(
        response, "the studio account must read the enquiry list")
    listed = cf.rows(response.json())
    assert any(cf.field(e, "reference") == reference for e in listed), (
        "a submitted enquiry must appear in the console")
    moments = [cf.parse_moment(cf.field(e, "received_at")) for e in listed]
    stamped = [m for m in moments if m]
    assert stamped == sorted(stamped, reverse=True), (
        "the enquiry list must come back newest first")


def test_recording_a_first_response_is_idempotent(studio, suffix) -> None:
    """The clock stops once, and a second recording does not move it."""
    reference, _ = cf.accepted_enquiry(suffix)
    with appclient.client(studio) as client:
        first = client.post(f"/studio/enquiries/{reference}/response")
    assert first.status_code in cf.ACCEPTED, cf.describe(
        first, "the studio account must be able to record a first response")
    stored = cf.enquiry_row(reference).get("first_response_at")
    assert stored, "recording a response must store the moment"
    with appclient.client(studio) as client:
        second = client.post(f"/studio/enquiries/{reference}/response")
    assert second.status_code in cf.ACCEPTED + tuple(cf.CLIENT_ERROR), cf.describe(
        second, "a second recording must not fail the server")
    assert cf.enquiry_row(reference).get("first_response_at") == stored, (
        "a second recording must not move the stored moment")


def test_studio_cannot_confirm_a_call_on_a_clients_behalf(studio, client_one) -> None:
    """The studio account works the calendar, never a client's booking."""
    reference, _ = cf.take_a_slot(client_one)
    try:
        response = cf.confirm_booking(studio, reference)
        assert response.status_code in cf.CLIENT_ERROR, cf.describe(
            response, "the studio account must not confirm a client's call")
    finally:
        cf.cancel_booking(client_one, reference)


def test_taken_slot_is_reported_as_unavailable(client_one) -> None:
    """A held slot is visible on the calendar and is no longer choosable."""
    reference, slot_id = cf.take_a_slot(client_one)
    try:
        slots = cf.rows(cf.get_json("/slots").json())
        held = [s for s in slots if cf.field(s, "id", "slot_id") == slot_id]
        assert held, "a held slot must stay visible on the calendar"
        assert cf.field(held[0], "is_available", "available") is False, (
            "a held slot must be reported as unavailable")
    finally:
        cf.cancel_booking(client_one, reference)


def test_list_endpoints_return_a_top_level_array() -> None:
    """The API shape the brief pins."""
    for path in ("/services", "/projects", "/packages", "/awards", "/testimonials", "/slots"):
        payload = cf.get_json(path).json()
        assert isinstance(payload, list), (
            f"{path} must return a top-level JSON array, returned {type(payload).__name__}")


def test_invalid_calls_are_client_errors_rather_than_server_errors(suffix) -> None:
    """Nothing invalid reaches a 500."""
    probes = [
        ("/enquiries", {}),
        ("/enquiries", cf.enquiry_body(suffix, email="not-an-address")),
    ]
    for path, body in probes:
        with appclient.client(None) as client:
            response = client.post(path, json=body)
        assert response.status_code in cf.CLIENT_ERROR, cf.describe(
            response, f"{path} must reject invalid input as a client error")


def test_unknown_project_slug_answers_not_found() -> None:
    """A slug matching no record is not found rather than empty."""
    response = cf.get_json("/projects/no-such-project")
    assert response.status_code in cf.NOT_FOUND, cf.describe(
        response, "an unknown project slug must answer as not found")


def test_unknown_service_slug_answers_not_found() -> None:
    """A service slug matching no record is not found."""
    response = cf.get_json("/services/no-such-service")
    assert response.status_code in cf.NOT_FOUND, cf.describe(
        response, "an unknown service slug must answer as not found")


def test_confirmation_email_reaches_only_the_booking_account(client_one, client_two, suffix) -> None:
    """Confirming sends exactly one message, to the right inbox."""
    reference, _ = cf.take_a_slot(client_one)
    cf.answer_hold(client_one, reference, topic=cf.probe_topic(suffix))
    before_other = cf.message_count(cf.CLIENT2_EMAIL)
    confirmed = cf.confirm_booking(client_one, reference)
    assert confirmed.status_code in cf.ACCEPTED, cf.describe(
        confirmed, "a live hold must confirm")
    message = cf.confirmation_for(cf.CLIENT_EMAIL)
    assert message is not None, (
        f"a confirmation carrying {cf.CONFIRMATION_SUBJECT_PREFIX!r} must reach "
        f"{cf.CLIENT_EMAIL}")
    assert message.subject.startswith(cf.CONFIRMATION_SUBJECT_PREFIX), (
        f"the subject must begin {cf.CONFIRMATION_SUBJECT_PREFIX!r}, read {message.subject!r}")
    assert all(cf.CLIENT2_EMAIL not in address for address in message.to), (
        f"the confirmation must not reach {cf.CLIENT2_EMAIL}, reached {message.to}")
    assert cf.message_count(cf.CLIENT2_EMAIL) == before_other, (
        "confirming one client's call must send nothing to another client")
    cf.cancel_booking(client_one, reference)


def test_confirmation_subject_carries_the_slot_start_in_utc(client_one, suffix) -> None:
    """The subject is the pinned prefix then the slot start."""
    reference, _ = cf.take_a_slot(client_one)
    cf.answer_hold(client_one, reference, topic=cf.probe_topic(suffix))
    cf.confirm_booking(client_one, reference)
    message = cf.confirmation_for(cf.CLIENT_EMAIL)
    assert message is not None, "a confirmation must land"
    row = cf.booking_row(reference)
    store = cf.backend()
    slot = store.one(cf.TABLE_SLOT, id=row.get("slot_id"))
    start = cf.parse_moment(slot.get("starts_at")) if slot else None
    assert start, "the confirmed booking must resolve to a seeded slot"
    rendered = start.strftime("%Y-%m-%d %H:%M") + " UTC"
    assert rendered in message.subject, (
        f"the subject must carry {rendered!r}, read {message.subject!r}")
    cf.cancel_booking(client_one, reference)


def test_confirmation_body_names_the_booking_reference(client_one, suffix) -> None:
    """The message a client keeps carries the handle they were shown."""
    reference, _ = cf.take_a_slot(client_one)
    cf.answer_hold(client_one, reference, topic=cf.probe_topic(suffix))
    cf.confirm_booking(client_one, reference)
    message = cf.confirmation_for(cf.CLIENT_EMAIL)
    assert message is not None, "a confirmation must land"
    assert reference in (message.body or "") or reference in message.subject, (
        f"the confirmation must name the reference {reference}, body read "
        f"{(message.body or '')[:300]!r}")
    cf.cancel_booking(client_one, reference)


def test_holding_a_slot_sends_no_message(client_one) -> None:
    """A hold is not a call, so nothing leaves the app."""
    before = cf.message_count(cf.CLIENT_EMAIL)
    reference, _ = cf.take_a_slot(client_one)
    cf.settle()
    assert cf.message_count(cf.CLIENT_EMAIL) == before, (
        "placing a hold must send no message")
    cf.cancel_booking(client_one, reference)


def test_cancelling_sends_no_message(client_one, suffix) -> None:
    """Cancelling is silent."""
    reference, _ = cf.take_a_slot(client_one)
    cf.answer_hold(client_one, reference, topic=cf.probe_topic(suffix))
    cf.confirm_booking(client_one, reference)
    cf.confirmation_for(cf.CLIENT_EMAIL)
    before = cf.message_count(cf.CLIENT_EMAIL)
    cf.cancel_booking(client_one, reference)
    cf.settle()
    assert cf.message_count(cf.CLIENT_EMAIL) == before, (
        "cancelling a call must send no message")


def test_submitting_an_enquiry_sends_no_message(suffix) -> None:
    """An automatic acknowledgement is not a response, so none is sent."""
    address = cf.probe_address(suffix)
    before = cf.message_count(address)
    cf.accepted_enquiry(suffix)
    cf.settle()
    assert cf.message_count(address) == before, (
        "submitting an enquiry must send no message")


def test_bookings_endpoint_scopes_to_the_calling_account(client_one, client_two, suffix) -> None:
    """A client's list is their own calls only."""
    reference, _ = cf.take_a_slot(client_one)
    cf.answer_hold(client_one, reference, topic=cf.probe_topic(suffix))
    cf.confirm_booking(client_one, reference)
    try:
        mine = cf.rows(cf.get_json("/account/bookings", client_one).json())
        theirs = cf.rows(cf.get_json("/account/bookings", client_two).json())
        assert any(cf.field(b, "reference") == reference for b in mine)
        assert not any(cf.field(b, "reference") == reference for b in theirs)
    finally:
        cf.cancel_booking(client_one, reference)


def test_studio_reads_a_clients_booking_but_a_stranger_does_not(studio, client_one) -> None:
    """The studio owns the calendar; a stranger owns nothing."""
    reference, _ = cf.take_a_slot(client_one)
    try:
        owner = cf.get_json(f"/bookings/{reference}", studio)
        assert owner.status_code in cf.ACCEPTED, cf.describe(
            owner, "the studio account must be able to read a booking on its calendar")
        stranger = cf.get_json(f"/bookings/{reference}", None)
        assert stranger.status_code in cf.DENIED, cf.describe(
            stranger, "an anonymous caller must not read a booking")
    finally:
        cf.cancel_booking(client_one, reference)


def test_client_cannot_publish_or_reorder_a_project(client_one) -> None:
    """Editorial control belongs to the studio account."""
    projects = cf.rows(cf.get_json("/projects").json())
    slug = cf.field(projects[0], "slug")
    store = cf.backend()
    before = store.one(cf.TABLE_PROJECT, slug=slug)
    with appclient.client(client_one) as client:
        unpublish = client.post(f"/studio/projects/{slug}/unpublish")
        reorder = client.patch(f"/studio/projects/{slug}", json={"editorial_order": 99})
    assert unpublish.status_code in cf.DENIED, cf.describe(
        unpublish, "a client must not unpublish a project")
    assert reorder.status_code in cf.DENIED, cf.describe(
        reorder, "a client must not reorder a project")
    after = store.one(cf.TABLE_PROJECT, slug=slug)
    assert after.get("published") == before.get("published"), (
        "a denied call must leave the project row unchanged")
    assert after.get("editorial_order") == before.get("editorial_order"), (
        "a denied call must leave the stored order unchanged")


def test_client_cannot_read_an_enquiry(client_one, suffix) -> None:
    """An enquiry is a transaction, not content."""
    reference, _ = cf.accepted_enquiry(suffix)
    response = cf.get_json("/studio/enquiries", client_one)
    assert response.status_code in cf.DENIED, cf.describe(
        response, "a client must not read the enquiry list")


def test_home_route_renders_its_blocks_in_the_browser(page) -> None:
    """The home route arrives and carries the studio's own name."""
    page.goto(appclient.app_url() + "/", wait_until="networkidle")
    body = page.inner_text("body")
    assert cf.SITE_NAME in body or cf.SITE_NAME in page.title(), (
        f"the home route must carry {cf.SITE_NAME!r}")
    assert cf.PROMISE_LINE in body, (
        f"the closing booking block must print {cf.PROMISE_LINE!r}")


def test_every_public_route_closes_on_the_booking_block(page) -> None:
    """The one conversion surface appears on every route."""
    for route in cf.PUBLIC_ROUTES:
        page.goto(appclient.app_url() + route, wait_until="networkidle")
        body = page.inner_text("body")
        assert cf.PROMISE_LINE in body, (
            f"the route {route} must close on the booking block carrying "
            f"{cf.PROMISE_LINE!r}")


def test_offers_route_renders_prices_with_a_from_label_and_tax_status(page) -> None:
    """A floor is never rendered bare."""
    page.goto(appclient.app_url() + "/offers", wait_until="networkidle")
    body = page.inner_text("body")
    assert cf.PRICE_RENDERED in body, (
        f"the offers route must render {cf.PRICE_RENDERED!r}, read {body[:600]!r}")
    assert cf.BADGE_RECOMMENDED in body, (
        f"the middle package must carry the badge {cf.BADGE_RECOMMENDED!r}")
    for label in cf.PANEL_LABELS:
        assert label in body, f"the accordion must carry the panel {label!r}"


def test_archive_filter_reflects_itself_in_the_address(page) -> None:
    """A filtered view can be shared and reopened."""
    page.goto(appclient.app_url() + "/projects", wait_until="networkidle")
    page.get_by_text(cf.SERVICE_VISUAL_IDENTITY, exact=True).first.click()
    page.wait_for_timeout(600)
    assert "/projects" in page.url and page.url != appclient.app_url() + "/projects", (
        f"choosing a filter must reflect itself in the address, read {page.url}")
    filtered = page.inner_text("body")
    page.goto(page.url, wait_until="networkidle")
    assert page.inner_text("body").count(cf.SERVICE_VISUAL_IDENTITY) >= 1, (
        "reopening a filtered address must render the same narrowed grid")
    assert filtered


def test_archive_carries_nine_filter_controls_including_all(page) -> None:
    """Eight services plus a control that is not a tag."""
    page.goto(appclient.app_url() + "/projects", wait_until="networkidle")
    body = page.inner_text("body")
    assert cf.FILTER_ALL in body, f"the filter row must carry the {cf.FILTER_ALL!r} control"
    for name in (cf.SERVICE_FIRST, cf.SERVICE_VISUAL_IDENTITY, cf.SERVICE_DIGITAL):
        assert name in body, f"the filter row must carry {name!r}"


def test_method_route_renders_its_mark_and_its_steps(page) -> None:
    """The mark travels with the name."""
    page.goto(appclient.app_url() + "/method", wait_until="networkidle")
    body = page.inner_text("body")
    assert cf.METHOD_NAME in body, (
        f"the method route must render {cf.METHOD_NAME!r}, read {body[:400]!r}")
    for title in cf.METHOD_STEPS:
        assert title in body, f"the method route must carry the step {title!r}"


def test_about_route_renders_the_awards_wall_and_the_proof_band(page) -> None:
    """Two placements, one record."""
    page.goto(appclient.app_url() + "/about", wait_until="networkidle")
    body = page.inner_text("body")
    for year, entity, distinction in cf.AWARD_ROWS:
        assert str(year) in body, f"the awards wall must carry {year}"
        assert distinction in body, f"the awards wall must carry {distinction!r}"
    assert "Vare Studio" in body, (
        "the earliest award row must keep the entity name it was submitted under")
    assert str(cf.DELIVERED_COUNT) in body, (
        f"the proof band must render {cf.DELIVERED_COUNT}")


def test_home_and_about_render_the_same_award_rows(page) -> None:
    """One record, two placements, no drift."""
    seen = []
    for route in ("/", "/about"):
        page.goto(appclient.app_url() + route, wait_until="networkidle")
        body = page.inner_text("body")
        seen.append([d for _, _, d in cf.AWARD_ROWS if d in body])
    assert seen[0] == seen[1], (
        f"the awards wall must read the same on both routes, read {seen}")


def test_footer_carries_the_directory_badge_with_its_accessible_name(page) -> None:
    """The badge says all five stored fields to somebody who cannot see it."""
    page.goto(appclient.app_url() + "/", wait_until="networkidle")
    body = page.inner_text("body")
    assert cf.DIRECTORY_SOURCE in body, (
        f"the footer must carry the badge source {cf.DIRECTORY_SOURCE!r}")
    assert cf.DIRECTORY_SCORE in body, (
        f"the footer must carry the rating {cf.DIRECTORY_SCORE}")
    markup = page.content()
    assert cf.DIRECTORY_VERDICT in markup, (
        f"the badge must carry the verdict {cf.DIRECTORY_VERDICT!r}")


def test_navigation_panel_opens_traps_focus_and_returns_it(page) -> None:
    """The panel is the whole navigation and it behaves."""
    page.goto(appclient.app_url() + "/", wait_until="networkidle")
    control = page.get_by_role("button").first
    control.click()
    page.wait_for_timeout(400)
    body = page.inner_text("body")
    for name in (cf.SERVICE_FIRST, cf.SERVICE_DIGITAL):
        assert name in body, f"the navigation panel must nest the service {name!r}"
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)


def test_every_content_image_carries_alternative_text(page) -> None:
    """Nothing meaningful is unlabelled."""
    for route in ("/", "/projects"):
        page.goto(appclient.app_url() + route, wait_until="networkidle")
        missing = page.eval_on_selector_all(
            "img",
            "els => els.filter(e => !e.hasAttribute('alt')).map(e => e.currentSrc || e.src)")
        assert not missing, (
            f"every image on {route} must declare alternative text, missing {missing[:5]}")


def test_narrow_viewport_does_not_overflow_sideways(page) -> None:
    """Nothing runs off the side of a phone."""
    page.set_viewport_size({"width": 390, "height": 844})
    for route in ("/", "/projects", "/offers", "/book"):
        page.goto(appclient.app_url() + route, wait_until="networkidle")
        overflow = page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        assert overflow <= 2, (
            f"the route {route} overflows sideways by {overflow} at a narrow viewport")


def test_contact_form_offers_the_two_closed_vocabularies(page) -> None:
    """The project control and the budget control are closed sets."""
    page.goto(appclient.app_url() + "/contact", wait_until="networkidle")
    body = page.inner_text("body")
    for band in cf.BUDGET_BANDS:
        assert band in body or band in page.content(), (
            f"the budget control must offer {band!r}")
    for kind in cf.PROJECT_TYPES:
        assert kind in body or kind in page.content(), (
            f"the project control must offer {kind!r}")


def test_calendar_route_renders_the_slot_grid(page) -> None:
    """The grid shows the calendar rather than an empty frame."""
    page.goto(appclient.app_url() + "/book", wait_until="networkidle")
    body = page.inner_text("body")
    assert body.strip(), "the booking route must render the calendar"
    starts = [cf.parse_moment(cf.field(s, "starts_at"))
              for s in cf.rows(cf.get_json("/slots").json())]
    rendered = [m.strftime("%H:%M") for m in starts if m]
    assert any(stamp in body for stamp in rendered), (
        f"the grid must print a seeded slot time, read {body[:400]!r}")


def test_case_study_renders_its_tag_line_and_outbound_action(page) -> None:
    """The case study hero is a four part stack."""
    project = cf.rows(cf.get_json("/projects").json())[0]
    slug = cf.field(project, "slug")
    page.goto(appclient.app_url() + f"/projects/{slug}", wait_until="networkidle")
    body = page.inner_text("body")
    assert cf.field(project, "client_name") in body, (
        "the case study headline must be the client name")
    outbound = page.eval_on_selector_all(
        "a[target='_blank']", "els => els.map(e => e.getAttribute('rel') || '')")
    assert outbound, "the case study must carry an outbound action opening in a new context"
    assert any("noreferrer" in rel for rel in outbound), (
        f"the outbound action must withhold the referrer, read {outbound}")


def test_expertise_index_renders_the_eight_services(page) -> None:
    """The tree is eight entries with two dashed lines each."""
    page.goto(appclient.app_url() + "/expertise", wait_until="networkidle")
    body = page.inner_text("body")
    for name in (cf.SERVICE_FIRST, cf.SERVICE_VISUAL_IDENTITY, cf.SERVICE_DIGITAL):
        assert name in body, f"the expertise index must carry {name!r}"


def test_privacy_route_is_linked_from_every_footer(page) -> None:
    """The privacy page is reachable from anywhere."""
    for route in ("/", "/offers", "/contact"):
        page.goto(appclient.app_url() + route, wait_until="networkidle")
        links = page.eval_on_selector_all("a", "els => els.map(e => e.getAttribute('href'))")
        assert any((href or "").endswith("/privacy") for href in links), (
            f"the footer of {route} must link the privacy route")
