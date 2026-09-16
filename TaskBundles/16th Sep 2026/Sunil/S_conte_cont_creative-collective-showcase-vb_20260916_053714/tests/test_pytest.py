from __future__ import annotations

import os
import re

import httpx

import appclient
from conftest import (AUTHOR_EMAIL, CLIENT_MARKER, COVER_KEY_PREFIX, CREATED,
                      DECOY_FIELD, DENIED, DISCIPLINES, DOWNLOAD_DIR,
                      DRAFT_PROJECT_TITLE, FEATURED_HOME_COUNT, NOT_FOUND,
                      PASSWORD, PRESS_COUNTS, PRESS_ITEM_COUNT,
                      PRESS_KIT_KEY_PREFIX, PUBLIC_ROUTES,
                      PUBLISHED_PROJECT_COUNT, READER_EMAIL, REFUSED,
                      SCREENSHOT_DIR, SERIES_VOLUMES, STUDIO_CHAPTER_YEARS,
                      TEAM_MEMBER_COUNT, USER_README, describe, payload,
                      settle, unique_email, unique_slug)

EXTERNAL_URL = re.compile(r"""(?:src|href)\s*=\s*["'](https?://[^"']+)["']""", re.I)
BINARY_ASSET = re.compile(r"""(?:src|href)\s*=\s*["'][^"']+\.(png|jpe?g|gif|webp|avif|svg|mp4|webm|woff2?|ttf|otf|eot)["']""", re.I)
CREDENTIAL_TOKEN = re.compile(r"(secret[_-]?key|access[_-]?key|password|api[_-]?key)\s*[:=]\s*[\"']?[\w-]{6,}", re.I)


def _titles(items):
    return [str(item.get("title", "")) for item in items]


def _project_list(client, discipline=None):
    response = client.get("/projects", params={"discipline": discipline} if discipline else None)
    assert response.status_code == 200, describe(response)
    body = payload(response)
    assert isinstance(body, list), f"/api/projects must return a top-level array: {describe(response)}"
    return body


def test_published_projects_are_listed(anon):
    """cov: C-OV-01, C-DC-13, C-DM-09"""
    projects = _project_list(anon)
    assert len(projects) == PUBLISHED_PROJECT_COUNT, (
        f"GET /api/projects returned {len(projects)} projects, expected the "
        f"{PUBLISHED_PROJECT_COUNT} seeded published ones: {_titles(projects)}")
    for project in projects:
        for field in ("id", "title", "client", "slug", "disciplines"):
            assert field in project, f"project {project!r} carries no {field!r}"


def test_discipline_filter_and_reset_list_published_projects(anon):
    """cov: C-CF-32"""
    everything = _project_list(anon)
    for discipline in DISCIPLINES:
        narrowed = _project_list(anon, discipline)
        assert len(narrowed) <= len(everything), (
            f"filter {discipline!r} returned {len(narrowed)} of {len(everything)} projects")
        for project in narrowed:
            assert discipline in project["disciplines"], (
                f"filter {discipline!r} returned {project['title']!r} whose "
                f"disciplines are {project['disciplines']!r}")
    spatial = _project_list(anon, "SPATIAL")
    assert spatial, "the SPATIAL filter returned nothing, and four seeded projects carry it"


def test_empty_discipline_filter_returns_an_empty_list(anon):
    """cov: C-CF-33"""
    response = anon.get("/projects", params={"discipline": "Sculpture"})
    assert response.status_code in (200, *REFUSED), describe(response)
    if response.status_code == 200:
        assert payload(response) == [], (
            f"a discipline outside the closed set returned rows: {describe(response)}")


def test_home_reel_holds_the_four_featured_projects(anon):
    """cov: C-CF-25, C-CF-26"""
    projects = _project_list(anon)
    featured = [p for p in projects if p.get("featured_home")]
    assert len(featured) == FEATURED_HOME_COUNT, (
        f"{len(featured)} projects carry featured_home, expected {FEATURED_HOME_COUNT}: "
        f"{_titles(featured)}")
    for project in featured:
        assert project.get("status", "published") != "draft", (
            f"the home reel carries the draft project {project['title']!r}")


def test_press_feed_is_newest_first(anon):
    """cov: C-CF-37, C-UF-02"""
    response = anon.get("/press")
    assert response.status_code == 200, describe(response)
    items = payload(response)
    assert isinstance(items, list), f"/api/press must return a top-level array: {describe(response)}"
    assert len(items) == PRESS_ITEM_COUNT, (
        f"/api/press returned {len(items)} items, expected the {PRESS_ITEM_COUNT} seeded")
    dates = [str(item["published_on"]) for item in items]
    assert dates == sorted(dates, reverse=True), (
        f"/api/press is not newest first: {dates}")


def test_press_category_badges_match_the_seeded_collection(anon):
    """cov: C-CF-35, C-CF-36, C-DM-05"""
    response = anon.get("/press/categories")
    assert response.status_code == 200, describe(response)
    rows = payload(response)
    assert isinstance(rows, list), f"/api/press/categories must return an array: {describe(response)}"
    counts = {str(row["category"]): int(row["count"]) for row in rows}
    for category, expected in PRESS_COUNTS:
        assert counts.get(category) == expected, (
            f"category {category!r} reports {counts.get(category)!r}, expected "
            f"{expected} from the seeded collection: {counts}")


def test_series_volumes_are_served(anon):
    """cov: C-CF-39, C-CF-40"""
    response = anon.get("/series")
    assert response.status_code == 200, describe(response)
    volumes = payload(response)
    assert isinstance(volumes, list), f"/api/series must return an array: {describe(response)}"
    labels = [str(volume["index_label"]) for volume in volumes]
    assert labels == list(SERIES_VOLUMES), (
        f"/api/series reports volumes {labels}, expected {list(SERIES_VOLUMES)}")
    for volume in volumes:
        assert str(volume["tag"]) == "Designing for the future", (
            f"volume {volume['index_label']!r} carries tag {volume['tag']!r}")


def test_team_members_carry_a_derived_count(anon):
    """cov: C-CF-47, C-DM-06, C-UF-03"""
    response = anon.get("/team")
    assert response.status_code == 200, describe(response)
    members = payload(response)
    assert isinstance(members, list), f"/api/team must return an array: {describe(response)}"
    assert len(members) == TEAM_MEMBER_COUNT, (
        f"/api/team returned {len(members)} members, expected {TEAM_MEMBER_COUNT}")
    for member in members:
        assert member.get("roles"), f"member {member.get('name')!r} carries no roles"


def test_studio_chapters_are_served(anon):
    """cov: C-CF-48"""
    response = anon.get("/chapters")
    assert response.status_code == 200, describe(response)
    chapters = payload(response)
    years = [str(chapter["year"]) for chapter in chapters]
    assert years == list(STUDIO_CHAPTER_YEARS), (
        f"/api/chapters reports years {years}, expected {list(STUDIO_CHAPTER_YEARS)}")


def test_project_titles_carry_the_client_marker(anon):
    """cov: C-FE-07"""
    projects = _project_list(anon)
    carrying = [t for t in _titles(projects) if CLIENT_MARKER in t]
    assert len(carrying) == len(projects), (
        f"{len(projects) - len(carrying)} project titles carry no {CLIENT_MARKER!r} "
        f"between the client and the piece: {_titles(projects)}")


def test_enquiry_is_persisted(anon, as_author):
    """cov: C-OV-03, C-CF-51"""
    message = f"probe enquiry {os.urandom(6).hex()}"
    response = anon.post("/enquiries", json={
        "name": "Probe Visitor", "email": unique_email("enquiry"),
        "message": message, "source": "footer"})
    assert response.status_code in CREATED, describe(response)
    listed = settle(lambda: [e for e in payload(as_author.get("/enquiries"))
                             if e.get("message") == message])
    assert listed, f"the stored enquiry carrying {message!r} is not in /api/enquiries"
    assert listed[0]["source"] == "footer", (
        f"the stored enquiry reports source {listed[0]['source']!r}, expected 'footer'")


def test_enquiry_list_is_served_to_the_editor(as_author):
    """cov: C-CF-58"""
    response = as_author.get("/enquiries")
    assert response.status_code == 200, describe(response)
    assert isinstance(payload(response), list), (
        f"/api/enquiries must return a top-level array: {describe(response)}")


def test_enquiry_list_stays_responsive_at_volume(as_author):
    """cov: C-CN-05"""
    response = as_author.get("/enquiries")
    assert response.status_code == 200, describe(response)
    assert response.elapsed.total_seconds() < 10.0, (
        f"/api/enquiries took {response.elapsed.total_seconds():.1f}s to answer")


def test_consent_choice_is_recorded(anon):
    """cov: C-CF-60"""
    response = anon.post("/consent", json={"accepted": True})
    assert response.status_code in CREATED, describe(response)
    body = payload(response)
    assert body.get("accepted") is True, (
        f"the recorded consent reports {body!r}, expected accepted true")


def test_page_view_is_recorded(site, as_author):
    """cov: C-CF-62"""
    before = len(payload(as_author.get("/page-views")))
    visit = site.get("/work")
    assert visit.status_code == 200, describe(visit)
    after = settle(lambda: len(payload(as_author.get("/page-views"))) > before)
    assert after, "opening /work recorded no page view the studio can read"
    rows = payload(as_author.get("/page-views"))
    assert any(str(row.get("route", "")).endswith("/work") for row in rows), (
        f"no page-view row names the /work route: {rows[:5]}")


def test_public_routes_are_open_to_an_anonymous_visitor(site):
    """cov: C-RL-01"""
    for route in PUBLIC_ROUTES:
        response = site.get(route)
        assert response.status_code == 200, (
            f"an anonymous visitor cannot read {route}: {describe(response)}")


def test_cold_load_of_a_deep_path_renders_that_route(site):
    """cov: C-CF-08"""
    response = site.get("/work")
    assert response.status_code == 200, describe(response)
    body = response.text
    for label in DISCIPLINES:
        assert label in body, (
            f"a cold load of /work does not render the filter {label!r}; the route "
            f"appears to be served by the home document instead")


def test_public_routes_each_carry_a_distinct_title(site):
    """cov: C-TR-06"""
    seen = {}
    for route in PUBLIC_ROUTES:
        response = site.get(route)
        assert response.status_code == 200, describe(response)
        found = re.search(r"<title[^>]*>(.*?)</title>", response.text, re.S | re.I)
        assert found, f"{route} carries no title element"
        title = " ".join(found.group(1).split())
        assert title, f"{route} carries an empty title"
        assert title not in seen, (
            f"{route} and {seen[title]} share the title {title!r}; every public "
            f"route carries its own")
        seen[title] = route


def test_sitemap_lists_every_public_route(site):
    """cov: C-CF-84, C-UF-04"""
    response = site.get("/sitemap.xml")
    assert response.status_code == 200, describe(response)
    body = response.text
    for route in PUBLIC_ROUTES:
        assert route in body, f"/sitemap.xml does not list {route!r}"


def test_robots_names_the_sitemap(site):
    """cov: C-CF-86"""
    response = site.get("/robots.txt")
    assert response.status_code == 200, describe(response)
    assert "sitemap.xml" in response.text.lower(), (
        f"/robots.txt does not name the sitemap: {response.text[:200]!r}")


def test_health_route_is_ready(anon):
    """cov: C-DC-01, C-DC-02, C-DC-03, C-DC-04, C-DC-05, C-DC-08, C-DC-09, C-DC-10, C-DC-11, C-DC-12, C-TR-01"""
    response = anon.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health did not answer 200 at {appclient.api_base()}: {describe(response)}")


def test_unknown_address_answers_not_found(site):
    """cov: C-CF-50"""
    response = site.get(f"/{unique_slug('no-such-route')}")
    assert response.status_code in NOT_FOUND, (
        f"an unknown address answered {response.status_code}, expected not found: "
        f"{describe(response)}")
    assert "Page not found" in response.text, (
        "the not-found response does not render the studio's own page")


def test_seeded_accounts_sign_in():
    """cov: C-RL-09, C-RL-10, C-DM-07, C-CF-01"""
    for email in (AUTHOR_EMAIL, READER_EMAIL):
        token = appclient.login(email, PASSWORD)
        assert token, f"sign-in for {email} returned no access_token"


def test_wrong_password_returns_no_token():
    """cov: C-CF-02"""
    response = httpx.post(f"{appclient.api_base()}/auth/login",
                          json={"email": AUTHOR_EMAIL, "password": "deku-wrong-pw-2026"},
                          timeout=30.0)
    assert response.status_code in DENIED or response.status_code in REFUSED, (
        f"a wrong password answered {response.status_code}: {describe(response)}")
    assert "access_token" not in response.text, (
        f"a wrong password returned a token: {describe(response)}")


def test_signup_creates_a_reader_only(anon):
    """cov: C-RL-07"""
    email = unique_email("press-contact")
    response = anon.post("/auth/signup", json={"email": email, "password": PASSWORD})
    assert response.status_code in CREATED, describe(response)
    token = appclient.login(email, PASSWORD)
    with appclient.client(token) as client:
        denied = client.get("/enquiries")
    assert denied.status_code in DENIED, (
        f"an account made at signup could read the enquiry list: {describe(denied)}")


def test_reader_token_is_denied_the_enquiry_list(as_reader):
    """cov: C-RL-04"""
    response = as_reader.get("/enquiries")
    assert response.status_code in DENIED, (
        f"a reader token read the enquiry list: {describe(response)}")


def test_reader_token_is_denied_a_console_write(as_reader, anon):
    """cov: C-RL-05, C-CF-64, C-DC-14"""
    before = len(_project_list(anon))
    response = as_reader.post("/projects", json={
        "title": f"READER {CLIENT_MARKER} ATTEMPT", "client": "READER",
        "slug": unique_slug("reader-attempt"), "disciplines": ["Digital"]})
    assert response.status_code in DENIED, (
        f"a reader token created a project: {describe(response)}")
    assert len(_project_list(anon)) == before, (
        "a denied reader write still changed the project list")


def test_anonymous_request_is_denied_an_author_endpoint(anon):
    """cov: C-CF-03, C-CF-63, C-UF-07"""
    before = len(_project_list(anon))
    response = anon.post("/projects", json={
        "title": f"ANON {CLIENT_MARKER} ATTEMPT", "client": "ANON",
        "slug": unique_slug("anon-attempt"), "disciplines": ["Digital"]})
    assert response.status_code in DENIED, (
        f"an unauthenticated request created a project: {describe(response)}")
    assert len(_project_list(anon)) == before, (
        "a denied anonymous write still changed the project list")


def test_author_creates_a_draft_project(draft_project, anon):
    """cov: C-CF-68"""
    assert str(draft_project.get("status")) == "draft", (
        f"a project made through the console reports status "
        f"{draft_project.get('status')!r}, expected 'draft'")
    titles = _titles(_project_list(anon))
    assert draft_project["title"] not in titles, (
        f"the new draft {draft_project['title']!r} is already on the public index")


def test_draft_project_is_absent_from_every_listing(anon):
    """cov: C-CF-75, C-CF-76, C-DM-10"""
    everything = _titles(_project_list(anon))
    assert DRAFT_PROJECT_TITLE not in everything, (
        f"the seeded draft {DRAFT_PROJECT_TITLE!r} is on the unfiltered index")
    for discipline in DISCIPLINES:
        titles = _titles(_project_list(anon, discipline))
        assert DRAFT_PROJECT_TITLE not in titles, (
            f"the seeded draft appears under the {discipline!r} filter")


def test_draft_project_address_answers_not_found(anon, draft_project, site):
    """cov: C-CF-77"""
    response = site.get(f"/work/{draft_project['slug']}")
    assert response.status_code in NOT_FOUND, (
        f"a draft project's own address answered {response.status_code}: {describe(response)}")
    api = anon.get(f"/projects/{draft_project['slug']}")
    assert api.status_code in NOT_FOUND, (
        f"GET /api/projects/<draft slug> answered {api.status_code}: {describe(api)}")


def test_sitemap_names_no_draft_project(site, draft_project):
    """cov: C-CF-85"""
    response = site.get("/sitemap.xml")
    assert response.status_code == 200, describe(response)
    assert draft_project["slug"] not in response.text, (
        f"/sitemap.xml names the draft project {draft_project['slug']!r}")


def test_publishing_makes_the_project_visible(as_author, anon, draft_project):
    """cov: C-CF-72"""
    response = as_author.post(f"/projects/{draft_project['id']}/publish")
    assert response.status_code in CREATED, describe(response)
    titles = settle(lambda: draft_project["title"] in _titles(_project_list(anon)))
    assert titles, f"{draft_project['title']!r} is not on the index after publishing"


def test_unpublishing_removes_the_project_from_filters(as_author, anon, draft_project):
    """cov: C-CF-73"""
    published = as_author.post(f"/projects/{draft_project['id']}/publish")
    assert published.status_code in CREATED, describe(published)
    response = as_author.post(f"/projects/{draft_project['id']}/unpublish")
    assert response.status_code in CREATED, describe(response)
    for discipline in ("Digital", *DISCIPLINES):
        titles = _titles(_project_list(anon, discipline))
        assert draft_project["title"] not in titles, (
            f"{draft_project['title']!r} still appears under {discipline!r} after unpublishing")


def test_republishing_creates_no_second_project(as_author, anon, draft_project):
    """cov: C-CF-74"""
    first = as_author.post(f"/projects/{draft_project['id']}/publish")
    assert first.status_code in CREATED, describe(first)
    after_first = _project_list(anon)
    second = as_author.post(f"/projects/{draft_project['id']}/publish")
    assert second.status_code in (*CREATED, *REFUSED), describe(second)
    after_second = _project_list(anon)
    assert len(after_second) == len(after_first), (
        f"publishing an already-published project changed the index from "
        f"{len(after_first)} to {len(after_second)} projects")


def test_seed_rows_are_not_duplicated(backend):
    """cov: C-DM-12, C-DM-11, C-DM-01, C-DM-02, C-DM-03"""
    assert backend.count("projects", status="published") == PUBLISHED_PROJECT_COUNT, (
        f"the projects table holds "
        f"{backend.count('projects', status='published')} published rows, expected "
        f"{PUBLISHED_PROJECT_COUNT}")
    assert backend.count("projects", status="draft") >= 1, (
        "the projects table holds no draft row, so the protected boundary has nothing to guard")
    assert backend.count("press_items") == PRESS_ITEM_COUNT, (
        f"the press_items table holds {backend.count('press_items')} rows, expected "
        f"{PRESS_ITEM_COUNT}")
    assert backend.count("project_disciplines") >= PUBLISHED_PROJECT_COUNT, (
        "the project_disciplines table holds fewer rows than there are projects")


def test_enquiry_with_an_empty_name_writes_no_row(anon, backend):
    """cov: C-CF-53, C-CF-57"""
    before = backend.count("enquiries")
    response = anon.post("/enquiries", json={
        "name": "", "email": unique_email("empty-name"),
        "message": "probe", "source": "footer"})
    assert response.status_code in REFUSED, (
        f"an enquiry with an empty name answered {response.status_code}: {describe(response)}")
    assert backend.count("enquiries") == before, (
        "a refused enquiry still wrote an enquiries row")


def test_enquiry_with_a_malformed_address_writes_no_row(anon, backend):
    """cov: C-DM-04"""
    before = backend.count("enquiries")
    response = anon.post("/enquiries", json={
        "name": "Probe Visitor", "email": "not-an-address",
        "message": "probe", "source": "press"})
    assert response.status_code in REFUSED, (
        f"an enquiry with a malformed address answered {response.status_code}: "
        f"{describe(response)}")
    assert backend.count("enquiries") == before, (
        "a refused enquiry still wrote an enquiries row")


def test_enquiry_filling_the_decoy_field_is_refused(anon, backend):
    """cov: C-CF-55"""
    before = backend.count("enquiries")
    response = anon.post("/enquiries", json={
        "name": "Probe Visitor", "email": unique_email("decoy"),
        "message": "probe", "source": "footer", DECOY_FIELD: "https://example.invalid"})
    assert response.status_code in REFUSED, (
        f"an enquiry carrying {DECOY_FIELD!r} answered {response.status_code}: "
        f"{describe(response)}")
    assert backend.count("enquiries") == before, (
        f"an enquiry carrying {DECOY_FIELD!r} still wrote an enquiries row")


def test_fourth_enquiry_inside_the_window_is_refused(anon, backend):
    """cov: C-CF-56"""
    sender = unique_email("rate")
    accepted = 0
    last = None
    for index in range(4):
        last = anon.post("/enquiries", json={
            "name": "Probe Visitor", "email": sender,
            "message": f"probe {index}", "source": "footer"})
        if last.status_code in CREATED:
            accepted += 1
    assert accepted == 3, (
        f"{accepted} of four rapid enquiries were accepted, expected three")
    assert last.status_code in REFUSED, (
        f"the fourth rapid enquiry answered {last.status_code}: {describe(last)}")


def test_cover_upload_is_stored_in_the_bucket(as_author, store, draft_project):
    """cov: C-CF-69, C-CF-71, C-DC-15, C-TR-02"""
    response = as_author.post(
        f"/projects/{draft_project['id']}/media",
        files={"file": ("cover.webp", os.urandom(512), "image/webp")},
        data={"kind": "cover"})
    assert response.status_code in CREATED, describe(response)
    key = str(payload(response).get("object_key", ""))
    assert key.startswith(f"{COVER_KEY_PREFIX}{draft_project['id']}/"), (
        f"the upload reports object key {key!r}, expected the scheme "
        f"{COVER_KEY_PREFIX}{{project_id}}/{{sha256_of_bytes}}.{{ext}}")
    assert settle(lambda: store.exists(key)), (
        f"the uploaded cover is not an object in the bucket at {key!r}; bytes on the "
        f"app's own filesystem do not count")


def test_press_kit_upload_is_stored_in_the_bucket(as_author, store, draft_project):
    """cov: C-CF-70"""
    response = as_author.post(
        f"/projects/{draft_project['id']}/media",
        files={"file": ("kit.pdf", os.urandom(512), "application/pdf")},
        data={"kind": "press_kit"})
    assert response.status_code in CREATED, describe(response)
    key = str(payload(response).get("object_key", ""))
    assert key.startswith(f"{PRESS_KIT_KEY_PREFIX}{draft_project['id']}/"), (
        f"the upload reports object key {key!r}, expected the scheme "
        f"{PRESS_KIT_KEY_PREFIX}{{project_id}}/{{sha256_of_bytes}}.{{ext}}")
    assert settle(lambda: store.exists(key)), (
        f"the uploaded press kit is not an object in the bucket at {key!r}")


def test_draft_cover_file_is_denied_to_a_reader(as_author, as_reader, anon, draft_project):
    """cov: C-CF-78, C-CF-79"""
    upload = as_author.post(
        f"/projects/{draft_project['id']}/media",
        files={"file": ("cover.webp", os.urandom(256), "image/webp")},
        data={"kind": "cover"})
    assert upload.status_code in CREATED, describe(upload)
    key = str(payload(upload)["object_key"])
    for name, client in (("reader", as_reader), ("anonymous", anon)):
        response = client.get(f"/media/{key}")
        assert response.status_code in DENIED or response.status_code in NOT_FOUND, (
            f"a {name} request for a draft cover answered {response.status_code}: "
            f"{describe(response)}")
        assert not response.content or response.status_code != 200, (
            f"a {name} request for a draft cover returned bytes")


def test_draft_cover_file_is_served_to_the_editor(as_author, draft_project):
    """cov: C-RL-08"""
    upload = as_author.post(
        f"/projects/{draft_project['id']}/media",
        files={"file": ("cover.webp", os.urandom(256), "image/webp")},
        data={"kind": "cover"})
    assert upload.status_code in CREATED, describe(upload)
    key = str(payload(upload)["object_key"])
    response = as_author.get(f"/media/{key}")
    assert response.status_code == 200, (
        f"the studio editor cannot read a draft cover: {describe(response)}")
    assert response.content, "the editor's request for a draft cover returned no bytes"


def test_press_kit_file_is_denied_to_anonymous(as_author, anon, draft_project):
    """cov: C-CF-80, C-CF-81, C-RL-02"""
    upload = as_author.post(
        f"/projects/{draft_project['id']}/media",
        files={"file": ("kit.pdf", os.urandom(256), "application/pdf")},
        data={"kind": "press_kit"})
    assert upload.status_code in CREATED, describe(upload)
    key = str(payload(upload)["object_key"])
    published = as_author.post(f"/projects/{draft_project['id']}/publish")
    assert published.status_code in CREATED, describe(published)
    response = anon.get(f"/media/{key}")
    assert response.status_code in DENIED or response.status_code in NOT_FOUND, (
        f"an anonymous request for a press kit answered {response.status_code}: "
        f"{describe(response)}")


def test_reader_downloads_the_press_kit_file(as_author, as_reader, draft_project):
    """cov: C-RL-03"""
    upload = as_author.post(
        f"/projects/{draft_project['id']}/media",
        files={"file": ("kit.pdf", os.urandom(256), "application/pdf")},
        data={"kind": "press_kit"})
    assert upload.status_code in CREATED, describe(upload)
    key = str(payload(upload)["object_key"])
    published = as_author.post(f"/projects/{draft_project['id']}/publish")
    assert published.status_code in CREATED, describe(published)
    response = as_reader.get(f"/media/{key}")
    assert response.status_code == 200, (
        f"a signed-in reader cannot download a published project's press kit: "
        f"{describe(response)}")
    assert response.content, "the reader's press-kit download returned no bytes"


def test_bucket_is_not_publicly_readable(as_author, draft_project):
    """cov: C-CF-82, C-CF-83"""
    upload = as_author.post(
        f"/projects/{draft_project['id']}/media",
        files={"file": ("cover.webp", os.urandom(256), "image/webp")},
        data={"kind": "cover"})
    assert upload.status_code in CREATED, describe(upload)
    key = str(payload(upload)["object_key"])
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    bucket = os.environ["STORAGE_BUCKET"]
    direct = httpx.get(f"{endpoint}/{bucket}/{key}", timeout=30.0)
    assert direct.status_code != 200, (
        f"a request made straight to the store for {key!r} returned bytes, so the "
        f"bucket or the object is publicly readable: {direct.status_code}")


def test_served_documents_reference_no_external_origin(site):
    """cov: C-CN-02, C-CN-03, C-CN-04, C-TR-03, C-TR-04, C-TR-05"""
    own = appclient.app_url()
    for route in PUBLIC_ROUTES:
        response = site.get(route)
        assert response.status_code == 200, describe(response)
        for url in EXTERNAL_URL.findall(response.text):
            assert url.startswith(own), (
                f"{route} pulls {url!r} from another origin at run time")
        leak = CREDENTIAL_TOKEN.search(response.text)
        assert leak is None, (
            f"{route} ships something shaped like a credential: {leak.group(0)[:60]!r}")


def test_served_documents_reference_no_binary_asset(site):
    """cov: C-TR-07, C-TR-08"""
    for route in PUBLIC_ROUTES:
        response = site.get(route)
        assert response.status_code == 200, describe(response)
        found = BINARY_ASSET.search(response.text)
        assert found is None, (
            f"{route} references the shipped asset {found.group(0)[:80]!r}; the build "
            f"generates every image, film, preview and face instead")


def test_app_readme_and_reserved_directories_exist():
    """cov: C-DC-06, C-DC-07, C-DM-08"""
    assert os.path.isfile(USER_README), f"{USER_README} does not exist"
    body = open(USER_README, encoding="utf-8", errors="replace").read()
    for email in (AUTHOR_EMAIL, READER_EMAIL):
        assert email in body, f"{USER_README} does not name the seeded account {email}"
    assert PASSWORD in body, f"{USER_README} does not carry the seeded password"
    for directory in (SCREENSHOT_DIR, DOWNLOAD_DIR):
        assert os.path.isdir(directory), f"the reserved directory {directory} does not exist"
