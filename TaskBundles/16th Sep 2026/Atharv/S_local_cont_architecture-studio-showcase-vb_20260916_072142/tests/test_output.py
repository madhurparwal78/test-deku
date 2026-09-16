from __future__ import annotations

import hashlib
import json
import re
import urllib.parse

import httpx

import appclient
import conftest as kit


def test_health_endpoint_returns_ok(raw):
    response = raw.get("/api/health")
    assert response.status_code == 200, (
        f"GET /api/health must answer 200 once the app can reach PostgreSQL and the "
        f"object store: {kit.describe(response)}")


def test_seeded_accounts_sign_in_with_the_pinned_password(anon):
    for email, role in kit.ROLES.items():
        token = kit.token_for(email)
        with appclient.client(token) as client:
            me = client.get("/auth/me")
        assert me.status_code == 200, (
            f"seeded account {email!r} must sign in with the pinned password: "
            f"{kit.describe(me)}")
        body = kit.json_of(me)
        assert body.get("email") == email, (
            f"/api/auth/me returned the wrong account for {email!r}: {body!r}")
        assert body.get("role") == role, (
            f"seeded account {email!r} must carry role {role!r}, got {body.get('role')!r}")
        assert body.get("display_name") == kit.DISPLAY_NAMES[email], (
            f"seeded display name for {email!r} must be "
            f"{kit.DISPLAY_NAMES[email]!r}, got {body!r}")


def test_user_readme_carries_every_seeded_login(raw):
    for email in kit.ROLES:
        token = kit.token_for(email)
        with appclient.client(token) as client:
            who = client.get("/auth/me")
        assert who.status_code == 200, (
            f"the credentials written to /app/USER_README.md must work at login; "
            f"{email!r} failed: {kit.describe(who)}")
    unauthenticated = raw.get("/api/auth/me")
    assert unauthenticated.status_code in (401, 403), (
        f"an unauthenticated /api/auth/me must be denied: {kit.describe(unauthenticated)}")


def test_signup_with_an_existing_email_is_refused_and_writes_no_row(anon, db):
    before = db.count("accounts", email=kit.READER)
    assert before == 1, (
        f"exactly one seeded row must exist for {kit.READER!r}, found {before}")
    response = anon.post("/auth/signup", json={"email": kit.READER,
                                               "password": kit.PASSWORD,
                                               "display_name": "Probe"})
    assert 400 <= response.status_code < 500, (
        f"a duplicate signup must be refused as a client error: {kit.describe(response)}")
    assert "email" in response.text.lower(), (
        f"the refusal must name the field at fault: {kit.describe(response)}")
    after = db.count("accounts", email=kit.READER)
    assert after == before, (
        f"a refused signup must write no second row: {before} before, {after} after")


def test_signup_always_produces_a_reader_role(anon, db):
    email = kit.unique_email()
    created = anon.post("/auth/signup", json={"email": email, "password": kit.PASSWORD,
                                              "display_name": "Probe", "role": "editor"})
    assert created.status_code in (200, 201), kit.describe(created)
    token = kit.json_of(created).get("access_token") or kit.token_for(email)
    with appclient.client(token) as client:
        me = kit.json_of(client.get("/auth/me"))
    assert me.get("role") == "reader", (
        f"a signup asking for editor in its body must still produce a reader: {me!r}")
    rows = db.rows("accounts", email=email)
    assert len(rows) == 1 and rows[0].get("role") == "reader", (
        f"the stored row must carry the reader role: {rows!r}")


def test_expired_token_is_denied_on_every_protected_route(anon):
    forged = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwcm9iZSIsImV4cCI6MX0.not-a-real-signature"
    with appclient.client(forged) as client:
        for path in ("/auth/me", "/enquiries", "/page-views"):
            response = client.get(path)
            assert response.status_code in (401, 403), (
                f"a tampered or expired token must be denied on {path}: "
                f"{kit.describe(response)}")
    login = anon.post("/auth/login", json={"email": kit.EDITOR_1,
                                           "password": kit.PASSWORD})
    assert login.status_code == 200, kit.describe(login)
    body = kit.json_of(login)
    assert body.get("expires_in") == kit.TOKEN_LIFETIME_SECONDS or body.get("expires_at"), (
        f"the login response must state the 24 hour token lifetime: {body!r}")


def test_password_hash_is_never_returned_by_any_endpoint(editor, anon):
    watched = ("password_hash", "passwordHash", "$2b$", "$2a$", "$argon2", "pbkdf2",
               "scrypt")
    for path in ("/auth/me", "/projects", "/team", "/offices", "/enquiries",
                 "/page-views"):
        response = editor.get(path)
        assert response.status_code == 200, kit.describe(response)
        for needle in watched:
            assert needle not in response.text, (
                f"{path} leaked a password hash marker {needle!r}: {response.text[:400]}")
        assert kit.PASSWORD not in response.text, (
            f"{path} echoed the seeded password back: {response.text[:400]}")
    login = anon.post("/auth/login", json={"email": kit.EDITOR_1,
                                           "password": kit.PASSWORD})
    for needle in watched:
        assert needle not in login.text, (
            f"the login response leaked {needle!r}: {login.text[:400]}")


def test_project_list_returns_published_projects_in_order(anon, db):
    body = kit.published_projects(anon)
    assert len(body) == kit.PUBLISHED_COUNT, (
        f"the public list carries the {kit.PUBLISHED_COUNT} published projects, "
        f"got {len(body)}: {[p.get('title') for p in body]!r}")
    titles = [p.get("title") for p in body]
    assert titles == [t for t, _a, _f in kit.PUBLISHED_PROJECTS], (
        f"projects are returned in their order field: {titles!r}")
    orders = [p.get("order") for p in body]
    assert orders == sorted(orders), f"the order field must ascend: {orders!r}"
    assert all(p.get("is_published") for p in body), (
        f"every row in the public list is published: {body!r}")
    assert db.count("projects") == kit.PROJECT_COUNT, (
        f"the projects table carries {kit.PROJECT_COUNT} rows, found "
        f"{db.count('projects')}")


def test_project_area_renders_with_a_thousands_separator(anon, raw):
    body = kit.published_projects(anon)
    by_title = {p.get("title"): p for p in body}
    for title, area, formatted in kit.PUBLISHED_PROJECTS:
        project = by_title.get(title)
        assert project is not None, f"project {title!r} must be published: {by_title.keys()!r}"
        assert project.get("area_sqm") == area, (
            f"{title!r} carries an area of {area}, got {project.get('area_sqm')!r}")
    page = raw.get("/work")
    assert page.status_code == 200, kit.describe(page)
    assert "58,079 m2" in page.text, (
        f"the index must render the largest area as '58,079 m2', with the separator and "
        f"the space before the unit: {page.text[:400]!r}")
    assert "58079 m2" not in page.text and "58,079m2" not in page.text, (
        "the area format carries a thousands separator and a space before the unit")


def test_project_detail_carries_body_and_gallery_image_rows(anon):
    listed = kit.published_projects(anon)
    slug = listed[0].get("slug")
    assert slug, f"every project carries a slug: {listed[0]!r}"
    response = anon.get(f"/projects/{slug}")
    assert response.status_code == 200, kit.describe(response)
    project = kit.json_of(response)
    assert project.get("body"), f"a project detail carries its body: {project!r}"
    images = project.get("images") or []
    covers = [i for i in images if i.get("kind") == "cover"]
    gallery = [i for i in images if i.get("kind") == "gallery"]
    assert len(covers) == 1, f"a project carries exactly one cover image row: {images!r}"
    assert len(gallery) == kit.GALLERY_PER_PROJECT, (
        f"a project carries {kit.GALLERY_PER_PROJECT} gallery image rows, "
        f"got {len(gallery)}")
    for image in images:
        assert image.get("object_key"), f"every image row carries an object key: {image!r}"


def test_team_offices_awards_publications_are_ordered_collections(anon):
    team = kit.json_of(anon.get("/team"))
    assert len(team) == kit.TEAM_COUNT, (
        f"the team collection carries {kit.TEAM_COUNT} members, got {len(team)}")
    assert team[0].get("name") == kit.FOUNDER, (
        f"the first team member is {kit.FOUNDER!r}: {team[0]!r}")
    assert team[0].get("role_title") == kit.FIRST_TEAM_ROLE, (
        f"the founder's role title is {kit.FIRST_TEAM_ROLE!r}: {team[0]!r}")
    assert team[-1].get("name") == kit.LAST_TEAM_MEMBER, (
        f"the last team member is {kit.LAST_TEAM_MEMBER!r}: {team[-1]!r}")

    offices = kit.json_of(anon.get("/offices"))
    assert len(offices) == kit.OFFICE_COUNT, (
        f"the offices collection carries {kit.OFFICE_COUNT} rows, got {len(offices)}")
    label, country, city, street = kit.FIRST_OFFICE
    assert (offices[0].get("label"), offices[0].get("country"), offices[0].get("city"),
            offices[0].get("street")) == (label, country, city, street), (
        f"the first office is {kit.FIRST_OFFICE!r}: {offices[0]!r}")

    for path in ("/awards", "/publications"):
        rows = kit.json_of(anon.get(path))
        assert isinstance(rows, list) and rows, f"{path} returns a non-empty array: {rows!r}"
        orders = [r.get("order") for r in rows if r.get("order") is not None]
        assert orders == sorted(orders), f"{path} is ordered: {orders!r}"


def test_legal_route_carries_eight_numbered_chapters(anon, raw):
    chapters = kit.json_of(anon.get("/legal"))
    assert len(chapters) == kit.LEGAL_COUNT, (
        f"the legal collection carries {kit.LEGAL_COUNT} chapters, got {len(chapters)}")
    seen = [(c.get("number"), c.get("title")) for c in chapters]
    assert seen == kit.LEGAL_CHAPTERS, (
        f"the eight chapters are numbered and titled exactly {kit.LEGAL_CHAPTERS}: {seen!r}")
    for chapter in chapters:
        assert chapter.get("body"), f"every chapter carries a body: {chapter!r}"
    page = raw.get("/legal")
    assert page.status_code == 200, kit.describe(page)
    for number, title in kit.LEGAL_CHAPTERS:
        assert title in page.text, f"the legal route renders the chapter {title!r}"


def test_gallery_photographs_feed_the_arc_in_order(anon):
    photos = kit.json_of(anon.get("/gallery"))
    assert len(photos) == kit.GALLERY_COUNT, (
        f"the arc gallery carries {kit.GALLERY_COUNT} photographs, got {len(photos)}")
    orders = [p.get("order") for p in photos]
    assert orders == sorted(orders), f"the arc set is ordered: {orders!r}"
    for photo in photos:
        assert photo.get("object_key"), f"an arc photograph carries an object key: {photo!r}"
        assert photo.get("ratio"), f"an arc photograph declares its aspect ratio: {photo!r}"
        assert photo.get("alt_text"), f"an arc photograph carries alt text: {photo!r}"


def test_arc_settings_is_one_editable_record(anon, editor, reader, db):
    settings = kit.json_of(anon.get("/arc-settings"))
    assert settings.get("frame_count") == kit.ARC_FRAME_COUNT, (
        f"the seeded arc frame count is {kit.ARC_FRAME_COUNT}: {settings!r}")
    assert settings.get("sweep_degrees") == kit.ARC_SWEEP_DEGREES, (
        f"the seeded arc sweep is {kit.ARC_SWEEP_DEGREES}: {settings!r}")
    assert settings.get("radius_ratio") == kit.ARC_RADIUS_RATIO, (
        f"the seeded arc radius ratio is {kit.ARC_RADIUS_RATIO}: {settings!r}")
    assert settings.get("tilt_step_degrees") == kit.ARC_TILT_STEP_DEGREES, (
        f"the seeded arc tilt step is {kit.ARC_TILT_STEP_DEGREES}: {settings!r}")
    assert db.count("arc_settings") == 1, (
        f"the arc configuration is one record, found {db.count('arc_settings')}")
    refused = reader.patch("/arc-settings", json={"frame_count": 4})
    assert refused.status_code in (401, 403), (
        f"a reader cannot change the arc configuration: {kit.describe(refused)}")
    changed = editor.patch("/arc-settings", json={"frame_count": kit.ARC_FRAME_COUNT})
    assert changed.status_code in (200, 201), (
        f"an editor changes the arc configuration: {kit.describe(changed)}")


def test_editor_creates_a_project_from_the_studio_surface(editor, db):
    slug = kit.unique_slug()
    created = kit.create_project(editor, slug=slug, title="Probe Civic Hall")
    assert created.status_code in (200, 201), kit.describe(created)
    project = kit.json_of(created)
    assert project.get("is_published") is False, (
        f"a newly created project starts unpublished: {project!r}")
    rows = db.rows("projects", slug=slug)
    assert len(rows) == 1, f"creating a project writes exactly one row: {rows!r}"
    clash = kit.create_project(editor, slug=slug, title="Probe Civic Hall Again")
    assert 400 <= clash.status_code < 500, (
        f"a repeated slug is refused as a client error: {kit.describe(clash)}")
    assert db.count("projects", slug=slug) == 1, (
        "a refused create writes no second row")


def test_image_reference_carries_alt_text_ratio_and_seed(anon):
    listed = kit.published_projects(anon)
    detail = kit.json_of(anon.get(f"/projects/{listed[0]['slug']}"))
    for image in detail.get("images") or []:
        assert image.get("alt_text"), (
            f"an image reference carries an accessible description: {image!r}")
        assert image.get("ratio"), f"an image reference declares its aspect ratio: {image!r}"
        assert image.get("seed"), f"an image reference carries a generator seed: {image!r}"
        key = image.get("object_key") or ""
        assert not key.startswith("/") and "://" not in key, (
            f"an image reference carries an object key, never a file path: {image!r}")
    team = kit.json_of(anon.get("/team"))
    for member in team:
        assert member.get("portrait_alt"), (
            f"a portrait carries an accessible description: {member!r}")


def test_draft_project_is_absent_from_every_public_list(anon, reader, editor, db):
    draft_titles = {t for t, _a in kit.DRAFT_PROJECTS}
    assert db.count("projects", is_published=False) == kit.DRAFT_COUNT, (
        f"exactly {kit.DRAFT_COUNT} seeded projects are unpublished, found "
        f"{db.count('projects', is_published=False)}")
    for client, who in ((anon, "an anonymous visitor"), (reader, "a reader")):
        listed = kit.published_projects(client)
        titles = {p.get("title") for p in listed}
        leaked = titles & draft_titles
        assert not leaked, f"{who} can see the draft project(s) {sorted(leaked)!r}"
        blob = json.dumps(listed)
        for title in draft_titles:
            assert title not in blob, (
                f"{who} received the draft title {title!r} in the list payload")
    seen_by_editor = {p.get("title") for p in kit.draft_projects(editor)}
    assert draft_titles <= seen_by_editor, (
        f"an editor reads every draft: expected {sorted(draft_titles)}, "
        f"got {sorted(seen_by_editor)}")


def test_draft_project_address_answers_not_found_to_a_visitor(anon, editor, raw):
    drafts = kit.draft_projects(editor)
    assert drafts, "the seed carries at least one unpublished project"
    slug = drafts[0].get("slug")
    api = anon.get(f"/projects/{slug}")
    assert api.status_code == 404, (
        f"a draft project address answers not found rather than forbidden, so the index "
        f"reveals nothing: {kit.describe(api)}")
    page = raw.get(f"/work/{slug}")
    assert page.status_code == 404, (
        f"the draft project page answers not found to a visitor: {kit.describe(page)}")


def test_draft_object_is_not_publicly_readable_from_the_bucket(editor, store):
    drafts = kit.draft_projects(editor)
    assert drafts, "the seed carries at least one unpublished project"
    detail = kit.json_of(editor.get(f"/projects/{drafts[0]['slug']}"))
    images = detail.get("images") or []
    assert images, f"a draft project carries image rows: {detail!r}"
    key = images[0]["object_key"]
    assert store.exists(key), (
        f"the draft object {key!r} must exist in the bucket for an editor to serve")
    response = kit.fetch_object_anonymously(key)
    assert response.status_code >= 400, (
        f"the draft object {key!r} must be refused to a caller with no credential, got "
        f"{response.status_code}: {response.text[:200]}")


def test_published_cover_object_is_readable_from_the_bucket(anon, store):
    listed = kit.published_projects(anon)
    detail = kit.json_of(anon.get(f"/projects/{listed[0]['slug']}"))
    covers = [i for i in (detail.get("images") or []) if i.get("kind") == "cover"]
    assert covers, f"a published project carries a cover row: {detail!r}"
    key = covers[0]["object_key"]
    assert store.exists(key), (
        f"the published cover object {key!r} must exist in the bucket")
    response = kit.fetch_object_anonymously(key)
    assert response.status_code == 200, (
        f"a published cover must be readable from the store: {response.status_code} "
        f"for {key!r}")
    assert response.content, f"the published cover object {key!r} carries bytes"


def test_cover_bytes_are_uploaded_to_the_bucket_at_the_key_scheme(anon, store):
    listed = kit.published_projects(anon)
    checked = 0
    for project in listed:
        detail = kit.json_of(anon.get(f"/projects/{project['slug']}"))
        for image in detail.get("images") or []:
            key = image["object_key"]
            parts = key.split("/")
            assert len(parts) == 3 and parts[0] == "projects", (
                f"a project image key reads projects/{{project_id}}/"
                f"{{sha256_of_bytes}}.png, got {key!r}")
            assert parts[1] == str(detail.get("id")), (
                f"the key names the project id {detail.get('id')!r}: {key!r}")
            assert re.fullmatch(r"[0-9a-f]{64}\.png", parts[2]), (
                f"the key's last segment is the hex digest of the bytes: {key!r}")
            assert store.exists(key), (
                f"the bytes for {key!r} must have been uploaded to the bucket")
            checked += 1
    assert checked >= kit.PUBLISHED_COUNT, (
        f"every published project uploads at least a cover, checked {checked}")
    keys = store.list("projects/")
    assert len(keys) >= checked, (
        f"the bucket holds at least the {checked} project objects the rows name, "
        f"listed {len(keys)}")


def test_image_row_digest_matches_the_stored_object_bytes(anon):
    listed = kit.published_projects(anon)
    detail = kit.json_of(anon.get(f"/projects/{listed[0]['slug']}"))
    for image in detail.get("images") or []:
        key = image["object_key"]
        digest = image.get("byte_digest")
        assert digest, f"an image row records the digest of its bytes: {image!r}"
        assert key.endswith(f"{digest}.png"), (
            f"the object key is derived from the digest the row records: {key!r} "
            f"against {digest!r}")
        fetched = kit.fetch_object_anonymously(key)
        if fetched.status_code == 200:
            actual = hashlib.sha256(fetched.content).hexdigest()
            assert actual == digest, (
                f"the digest in the row must be the digest of the stored bytes for "
                f"{key!r}: row {digest!r}, bytes {actual!r}")


def test_regenerating_an_image_from_one_seed_writes_no_second_object(editor, store):
    created = kit.create_project(editor)
    assert created.status_code in (200, 201), kit.describe(created)
    project = kit.json_of(created)
    seed = "probe-seed-0001"
    first = kit.add_image(editor, project["id"], seed=seed)
    assert first.status_code in (200, 201), kit.describe(first)
    one = kit.json_of(first)
    before = len(store.list(f"projects/{project['id']}/"))
    second = kit.add_image(editor, project["id"], seed=seed)
    assert second.status_code in (200, 201, 409), kit.describe(second)
    after = len(store.list(f"projects/{project['id']}/"))
    assert after == before, (
        f"one seed produces one set of bytes, so regenerating writes no second object: "
        f"{before} then {after}")
    if second.status_code in (200, 201):
        two = kit.json_of(second)
        assert two.get("object_key") == one.get("object_key"), (
            f"the regenerated image lands at the same key: {one.get('object_key')!r} "
            f"then {two.get('object_key')!r}")


def test_publish_flips_the_flag_and_records_when(editor, anon, db):
    created = kit.json_of(kit.create_project(editor))
    assert kit.add_image(editor, created["id"]).status_code in (200, 201)
    before = len(kit.published_projects(anon))
    published = editor.post(f"/projects/{created['id']}/publish")
    assert published.status_code in (200, 201), kit.describe(published)
    body = kit.json_of(published)
    assert body.get("is_published") is True, f"publishing flips the flag: {body!r}"
    assert body.get("published_at"), f"publishing records when it happened: {body!r}"
    rows = db.rows("projects", id=created["id"])
    assert rows and rows[0].get("is_published"), (
        f"the stored row carries the published flag: {rows!r}")
    after = len(kit.published_projects(anon))
    assert after == before + 1, (
        f"a published project joins the public list: {before} then {after}")


def test_unpublish_returns_the_project_and_its_objects_to_invisible(editor, anon):
    created = kit.json_of(kit.create_project(editor))
    assert kit.add_image(editor, created["id"]).status_code in (200, 201)
    assert editor.post(f"/projects/{created['id']}/publish").status_code in (200, 201)
    detail = kit.json_of(editor.get(f"/projects/{created['slug']}"))
    key = (detail.get("images") or [{}])[0].get("object_key")
    assert kit.fetch_object_anonymously(key).status_code == 200, (
        f"while published, the object {key!r} is readable")
    withdrawn = editor.post(f"/projects/{created['id']}/unpublish")
    assert withdrawn.status_code in (200, 201), kit.describe(withdrawn)
    assert kit.json_of(withdrawn).get("is_published") is False, (
        "unpublishing returns the project to invisible")
    assert anon.get(f"/projects/{created['slug']}").status_code == 404, (
        "an unpublished project answers not found again")
    after = kit.settle(lambda: kit.fetch_object_anonymously(key).status_code >= 400)
    assert after, (
        f"unpublishing returns the object {key!r} to not publicly readable")


def test_enquiry_is_stored_with_a_unique_twelve_character_reference(anon, db):
    before = db.count("enquiries")
    sent = anon.post("/enquiries", json=kit.enquiry_body())
    assert sent.status_code in (200, 201), kit.describe(sent)
    body = kit.json_of(sent)
    reference = body.get("reference")
    assert isinstance(reference, str), f"an enquiry returns its reference: {body!r}"
    assert re.fullmatch(r"[a-z0-9]{%d}" % kit.REFERENCE_LENGTH, reference), (
        f"the reference is {kit.REFERENCE_LENGTH} lowercase characters, got "
        f"{reference!r}")
    rows = db.rows("enquiries", reference=reference)
    assert len(rows) == 1, f"the enquiry is stored exactly once: {rows!r}"
    assert db.count("enquiries") == before + 1, (
        f"one enquiry writes one row: {before} then {db.count('enquiries')}")
    other = kit.json_of(anon.post("/enquiries", json=kit.enquiry_body()))
    assert other.get("reference") != reference, (
        f"two enquiries carry different references: {reference!r} twice")


def test_duplicate_enquiry_submission_creates_one_row(anon, db):
    payload = kit.enquiry_body()
    before = db.count("enquiries")
    first = anon.post("/enquiries", json=payload)
    assert first.status_code in (200, 201), kit.describe(first)
    one = kit.json_of(first)
    second = anon.post("/enquiries", json=payload)
    assert second.status_code in (200, 201, 409), kit.describe(second)
    after = db.count("enquiries")
    assert after == before + 1, (
        f"repeating one enquiry submission stores one row: {before} then {after}")
    if second.status_code in (200, 201):
        two = kit.json_of(second)
        assert two.get("reference") == one.get("reference"), (
            f"a repeated submission returns the first reference: "
            f"{one.get('reference')!r} then {two.get('reference')!r}")


def test_enquiry_rows_persist_and_survive_a_reread(anon, editor, db):
    payload = kit.enquiry_body()
    sent = kit.json_of(anon.post("/enquiries", json=payload))
    reference = sent["reference"]
    rows = db.rows("enquiries", reference=reference)
    assert len(rows) == 1, f"the enquiry row persists: {rows!r}"
    stored = rows[0]
    assert stored.get("name") == payload["name"], (
        f"the stored name is what was sent: {stored!r}")
    assert stored.get("email") == payload["email"], (
        f"the stored email is what was sent: {stored!r}")
    assert stored.get("message") == payload["message"], (
        f"the stored message is what was sent: {stored!r}")
    listed = kit.json_of(editor.get("/enquiries"))
    assert any(e.get("reference") == reference for e in listed), (
        f"the stored enquiry is readable again by an editor: {reference!r}")


def test_page_views_are_recorded_with_their_route(editor, raw, reader):
    before = len(kit.json_of(editor.get("/page-views")))
    visited = raw.get("/about")
    assert visited.status_code == 200, kit.describe(visited)
    grew = kit.settle(lambda: len(kit.json_of(editor.get("/page-views"))) > before)
    assert grew, f"a page view is recorded with its route: the count stayed at {before}"
    views = kit.json_of(editor.get("/page-views"))
    for view in views:
        assert view.get("route"), f"a recorded view names its route: {view!r}"
        assert view.get("viewed_at"), f"a recorded view names when it happened: {view!r}"
    refused = reader.get("/page-views")
    assert refused.status_code in (401, 403), (
        f"a reader cannot read the recorded views: {kit.describe(refused)}")


def test_seeding_is_idempotent_across_a_restart(db):
    for email in kit.ROLES:
        assert db.count("accounts", email=email) == 1, (
            f"seeding must not duplicate {email!r}, found "
            f"{db.count('accounts', email=email)}")
    for title, _area, _formatted in kit.PUBLISHED_PROJECTS:
        assert db.count("projects", title=title) == 1, (
            f"project {title!r} is seeded once, found {db.count('projects', title=title)}")
    for title, _area in kit.DRAFT_PROJECTS:
        assert db.count("projects", title=title) == 1, (
            f"draft {title!r} is seeded once, found {db.count('projects', title=title)}")
    assert db.count("team_members") == kit.TEAM_COUNT, (
        f"the team table holds {kit.TEAM_COUNT} rows, found {db.count('team_members')}")
    assert db.count("offices") == kit.OFFICE_COUNT, (
        f"the offices table holds {kit.OFFICE_COUNT} rows, found {db.count('offices')}")
    assert db.count("gallery_photos") == kit.GALLERY_COUNT, (
        f"the gallery table holds {kit.GALLERY_COUNT} rows, found "
        f"{db.count('gallery_photos')}")
    assert db.count("legal_sections") == kit.LEGAL_COUNT, (
        f"the legal table holds {kit.LEGAL_COUNT} rows, found "
        f"{db.count('legal_sections')}")


def test_project_images_are_unique_on_project_kind_and_order(anon, db):
    listed = kit.published_projects(anon)
    for project in listed:
        rows = db.rows("project_images", project_id=project["id"])
        keys = [(r.get("kind"), r.get("order")) for r in rows]
        assert len(keys) == len(set(keys)), (
            f"project {project['title']!r} carries a duplicate image slot: {keys!r}")
        covers = [k for k in keys if k[0] == "cover"]
        assert len(covers) == 1, (
            f"project {project['title']!r} carries exactly one cover: {keys!r}")


def test_reader_cannot_publish_or_edit_any_content(reader, editor, anon, db):
    drafts = kit.draft_projects(editor)
    target = drafts[0]
    before = db.rows("projects", id=target["id"])
    attempts = (
        ("post", f"/projects/{target['id']}/publish", None),
        ("post", f"/projects/{target['id']}/unpublish", None),
        ("patch", f"/projects/{target['id']}", {"title": "Rewritten"}),
        ("post", "/projects", {"slug": kit.unique_slug(), "title": "Intruder",
                               "area_sqm": 10, "category": "x", "body": "x", "order": 1}),
        ("patch", "/arc-settings", {"frame_count": 2}),
    )
    for verb, path, payload in attempts:
        call = getattr(reader, verb)
        response = call(path, json=payload) if payload is not None else call(path)
        assert response.status_code in (401, 403), (
            f"a reader must be denied at {verb.upper()} {path}: {kit.describe(response)}")
    after = db.rows("projects", id=target["id"])
    assert after == before, (
        f"a denied editorial write leaves the row unchanged: {before!r} then {after!r}")
    listed = kit.published_projects(anon)
    assert not any(p.get("title") == "Intruder" for p in listed), (
        "a denied create wrote a row anyway")


def test_reader_cannot_read_a_draft_project_by_any_route(reader, editor):
    drafts = kit.draft_projects(editor)
    slug = drafts[0]["slug"]
    detail = reader.get(f"/projects/{slug}")
    assert detail.status_code == 404, (
        f"a reader asking for a draft by slug is answered not found: "
        f"{kit.describe(detail)}")
    listed = reader.get("/projects", params={"include": "drafts"})
    assert listed.status_code < 500, kit.describe(listed)
    if listed.status_code == 200:
        titles = {p.get("title") for p in kit.json_of(listed)}
        assert slug not in json.dumps(sorted(titles)), (
            f"a reader cannot ask for drafts by a query parameter: {sorted(titles)!r}")
        assert all(p.get("is_published") for p in kit.json_of(listed)), (
            "every row a reader receives is published")


def test_reader_cannot_read_another_accounts_enquiry(reader, anon, editor):
    sent = kit.json_of(anon.post("/enquiries", json=kit.enquiry_body()))
    reference = sent["reference"]
    listed = reader.get("/enquiries")
    assert listed.status_code < 500, kit.describe(listed)
    if listed.status_code == 200:
        blob = json.dumps(kit.json_of(listed))
        assert reference not in blob, (
            f"a reader must not receive another account's enquiry {reference!r}: "
            f"{blob[:400]}")
    direct = reader.get(f"/enquiries/{reference}")
    assert direct.status_code in (401, 403, 404), (
        f"a reader reaching for another account's enquiry is refused: "
        f"{kit.describe(direct)}")
    editors_view = kit.json_of(editor.get("/enquiries"))
    assert any(e.get("reference") == reference for e in editors_view), (
        f"an editor does read that enquiry: {reference!r}")


def test_unauthenticated_studio_route_is_denied(anon, raw):
    for path in ("/enquiries", "/page-views"):
        response = anon.get(path)
        assert response.status_code in (401, 403), (
            f"an unauthenticated call to {path} must be denied: {kit.describe(response)}")
    for route in kit.EDITOR_ROUTES + kit.READER_ROUTES:
        page = raw.get(route)
        assert page.status_code in (301, 302, 303, 307, 308, 401, 403), (
            f"an unauthenticated visit to {route} must redirect to the sign-in page "
            f"rather than serve it: {kit.describe(page)}")
        if page.status_code in (301, 302, 303, 307, 308):
            target = page.headers.get("location", "")
            assert "/login" in target, (
                f"{route} must redirect to /login, got {target!r}")


def test_editor_reads_every_enquiry_received(editor, anon):
    first = kit.json_of(anon.post("/enquiries", json=kit.enquiry_body()))
    listed = editor.get("/enquiries")
    assert listed.status_code == 200, kit.describe(listed)
    rows = kit.json_of(listed)
    assert isinstance(rows, list) and rows, f"/api/enquiries returns an array: {rows!r}"
    assert any(e.get("reference") == first["reference"] for e in rows), (
        f"the enquiry just sent is in the editor's list: {first['reference']!r}")
    stamps = [e.get("created_at") for e in rows if e.get("created_at")]
    assert stamps == sorted(stamps, reverse=True), (
        f"the editor's list is newest first: {stamps[:4]!r}")
    for row in rows:
        assert row.get("reference"), f"every row carries its reference: {row!r}"


def test_public_list_query_cannot_ask_for_unpublished_rows(anon, editor):
    draft_titles = {p["title"] for p in kit.draft_projects(editor)}
    for params in ({"include": "drafts"}, {"is_published": "false"},
                   {"status": "draft"}, {"all": "true"}, {"published": "0"}):
        response = anon.get("/projects", params=params)
        assert response.status_code < 500, (
            f"a public list with {params!r} must not be a server error: "
            f"{kit.describe(response)}")
        if response.status_code == 200:
            body = kit.json_of(response)
            titles = {p.get("title") for p in body}
            leaked = titles & draft_titles
            assert not leaked, (
                f"the query {params!r} leaked the draft(s) {sorted(leaked)!r}")


def test_invalid_enquiry_is_refused_and_names_the_field(anon, db):
    before = db.count("enquiries")
    cases = (("name", kit.enquiry_body(name="")),
             ("email", kit.enquiry_body(email="not-an-address")),
             ("message", kit.enquiry_body(message="")))
    for field, payload in cases:
        response = anon.post("/enquiries", json=payload)
        assert 400 <= response.status_code < 500, (
            f"an enquiry with a bad {field} must be refused as a client error: "
            f"{kit.describe(response)}")
        assert field in response.text.lower(), (
            f"the refusal must name the field at fault ({field}): "
            f"{kit.describe(response)}")
    assert db.count("enquiries") == before, (
        f"a refused enquiry writes nothing: {before} then {db.count('enquiries')}")


def test_decoy_field_marks_an_enquiry_invalid(anon, db):
    before = db.count("enquiries")
    response = anon.post("/enquiries",
                         json=kit.enquiry_body(company="Norrgaard Holdings"))
    assert 400 <= response.status_code < 500, (
        f"an enquiry whose unattended decoy field is filled must be refused: "
        f"{kit.describe(response)}")
    assert db.count("enquiries") == before, (
        f"a refused decoy submission writes nothing: {before} then "
        f"{db.count('enquiries')}")


def test_repeated_enquiries_from_one_origin_are_refused(anon, db):
    before = db.count("enquiries")
    accepted = 0
    refused = 0
    for _ in range(kit.ENQUIRY_RATE_LIMIT + 2):
        response = anon.post("/enquiries", json=kit.enquiry_body())
        if response.status_code in (200, 201):
            accepted += 1
        else:
            assert 400 <= response.status_code < 500, (
                f"a rate-limited enquiry is refused as a client error: "
                f"{kit.describe(response)}")
            refused += 1
    assert refused >= 1, (
        f"more than {kit.ENQUIRY_RATE_LIMIT} enquiries from one origin inside "
        f"{kit.ENQUIRY_RATE_WINDOW_SECONDS} seconds must be refused, all "
        f"{accepted} were accepted")
    assert accepted <= kit.ENQUIRY_RATE_LIMIT, (
        f"at most {kit.ENQUIRY_RATE_LIMIT} are accepted, got {accepted}")
    assert db.count("enquiries") == before + accepted, (
        "a refused enquiry writes no row")


def test_enquiry_confirmation_address_shows_its_reference(anon, raw):
    sent = kit.json_of(anon.post("/enquiries", json=kit.enquiry_body()))
    reference = sent["reference"]
    page = raw.get(f"/contact/sent/{reference}")
    assert page.status_code == 200, (
        f"the confirmation address must be openable and bookmarkable: "
        f"{kit.describe(page)}")
    assert reference in page.text, (
        f"the confirmation page shows the reference {reference!r}: {page.text[:400]!r}")
    again = raw.get(f"/contact/sent/{reference}")
    assert again.status_code == 200, (
        "the confirmation address can be reopened")


def test_unknown_address_answers_not_found_with_an_honest_title(raw):
    missing = f"/definitely-not-a-route-{'x' * 12}"
    response = raw.get(missing)
    assert response.status_code == 404, (
        f"an unknown address answers not found: {kit.describe(response)}")
    title = re.search(r"<title[^>]*>(.*?)</title>", response.text, re.S | re.I)
    assert title, "the not-found response carries a document title"
    assert re.search(r"(not found|404|doesn't exist)", title.group(1), re.I), (
        f"the document title of a not-found response says so, got "
        f"{title.group(1).strip()!r}")
    assert kit.NOT_FOUND_HEADING in response.text, (
        f"the not-found page carries {kit.NOT_FOUND_HEADING!r}: {response.text[:400]!r}")
    assert kit.NOT_FOUND_LINE in response.text, (
        f"the not-found page carries {kit.NOT_FOUND_LINE!r}: {response.text[:400]!r}")


def test_every_internal_link_on_a_public_route_resolves(raw):
    seen = {}
    for route in kit.PUBLIC_ROUTES:
        response = raw.get(route)
        assert response.status_code == 200, (
            f"a public route that exists must be served with a success response: "
            f"{kit.describe(response)}")
        for href in re.findall(r'href="([^"#?]+)', response.text):
            if href.startswith("http") or href.startswith("mailto:") or \
                    href.startswith("tel:") or not href.startswith("/"):
                continue
            seen.setdefault(href, route)
    assert seen, "the public pages must carry internal links"
    broken = []
    for href, source in sorted(seen.items()):
        target = raw.get(href)
        if target.status_code >= 400:
            broken.append((href, source, target.status_code))
    assert not broken, (
        f"every internal link on every public route resolves; broken: {broken!r}")


def test_public_routes_declare_unique_titles_and_descriptions(raw):
    titles, descriptions = {}, {}
    for route in kit.PUBLIC_ROUTES:
        response = raw.get(route)
        assert response.status_code == 200, kit.describe(response)
        title = re.search(r"<title[^>]*>(.*?)</title>", response.text, re.S | re.I)
        description = re.search(
            r'<meta[^>]+name="description"[^>]+content="([^"]*)"', response.text)
        assert title and title.group(1).strip(), (
            f"{route} declares its own title: {response.text[:300]!r}")
        assert description and description.group(1).strip(), (
            f"{route} declares its own description: {response.text[:300]!r}")
        assert title.group(1) not in titles, (
            f"{route} repeats the title of {titles.get(title.group(1))!r}")
        assert description.group(1) not in descriptions, (
            f"{route} repeats the description of "
            f"{descriptions.get(description.group(1))!r}")
        titles[title.group(1)] = route
        descriptions[description.group(1)] = route


def test_legal_route_is_linked_from_the_signup_form(raw):
    signup = raw.get("/signup")
    assert signup.status_code == 200, kit.describe(signup)
    assert 'href="/legal' in signup.text, (
        f"the signup form links the legal route as the terms page: "
        f"{signup.text[:600]!r}")
    for route in ("/", "/work", "/about", "/contact"):
        page = raw.get(route)
        assert 'href="/legal' in page.text, (
            f"{route} must reach the legal route from its footer")


def test_empty_enquiry_list_renders_its_own_empty_state(fresh):
    response = fresh.get("/enquiries")
    assert response.status_code in (200, 401, 403), kit.describe(response)
    if response.status_code == 200:
        body = kit.json_of(response)
        assert body == [], (
            f"an account that has sent nothing reads an empty list rather than "
            f"another account's rows: {body!r}")
    account = fresh.get("/auth/me")
    assert account.status_code == 200, kit.describe(account)
    assert kit.json_of(account).get("role") == "reader", (
        "a fresh signup is a reader")


def test_list_endpoints_return_top_level_arrays(anon, editor):
    for client, path in ((anon, "/projects"), (anon, "/team"), (anon, "/offices"),
                         (anon, "/awards"), (anon, "/publications"), (anon, "/legal"),
                         (anon, "/gallery"), (editor, "/enquiries"),
                         (editor, "/page-views")):
        response = client.get(path)
        assert response.status_code == 200, kit.describe(response)
        body = kit.json_of(response)
        assert isinstance(body, list), (
            f"{path} must return a top-level JSON array, got {type(body).__name__}: "
            f"{body!r}")


def test_invalid_call_is_a_client_error_naming_the_reason(editor, anon):
    bad = ((editor, "post", "/projects", {"slug": "", "title": "", "area_sqm": "lots"}),
           (editor, "patch", "/arc-settings", {"frame_count": "many"}),
           (anon, "post", "/enquiries", {"name": "x"}))
    for client, verb, path, payload in bad:
        response = getattr(client, verb)(path, json=payload)
        assert 400 <= response.status_code < 500, (
            f"{verb.upper()} {path} with {payload!r} must be rejected as a client error, "
            f"never as a server error and never as a silent success: "
            f"{kit.describe(response)}")
        assert response.text.strip(), (
            f"{path} must carry a message naming the reason: {kit.describe(response)}")


def test_no_address_outside_the_application_is_referenced(raw):
    origin = urllib.parse.urlparse(kit.app_url()).netloc
    for route in kit.PUBLIC_ROUTES:
        response = raw.get(route)
        assert response.status_code == 200, kit.describe(response)
        external = []
        for url in re.findall(r'(?:src|href)="(https?://[^"]+)"', response.text):
            host = urllib.parse.urlparse(url).netloc
            if host and host != origin:
                external.append(url)
        assert not external, (
            f"{route} references an address outside the application: {external!r}")
        assert "fonts.googleapis.com" not in response.text, (
            f"{route} reaches a hosted font service")
        assert not re.search(r"(api[_-]?key|secret|bearer\s+ey)", response.text, re.I), (
            f"{route} ships something usable as a credential: {response.text[:300]!r}")


def test_no_binary_asset_is_referenced_anywhere_in_the_build(raw):
    offenders = {}
    for route in kit.PUBLIC_ROUTES:
        response = raw.get(route)
        assert response.status_code == 200, kit.describe(response)
        for attr in ("src", "href"):
            for ref in re.findall(rf'{attr}="([^"?#]+)"', response.text):
                if ref.lower().endswith(kit.BINARY_SUFFIXES):
                    offenders.setdefault(route, []).append(ref)
    assert not offenders, (
        f"no binary asset may be referenced anywhere in the build: {offenders!r}")


def test_body_text_meets_the_contrast_bar(page):
    page.goto(kit.absolute("/"))
    ratio = page.evaluate(
        """() => {
          const parse = (value) => {
            const parts = value.match(/[\\d.]+/g).slice(0, 3).map(Number);
            return parts.map(c => {
              const s = c / 255;
              return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
            });
          };
          const lum = (rgb) => 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
          const body = document.body;
          const style = getComputedStyle(body);
          let bg = style.backgroundColor;
          let node = body;
          while (bg === 'rgba(0, 0, 0, 0)' && node.parentElement) {
            node = node.parentElement;
            bg = getComputedStyle(node).backgroundColor;
          }
          if (bg === 'rgba(0, 0, 0, 0)') bg = 'rgb(255, 255, 255)';
          const a = lum(parse(style.color));
          const b = lum(parse(bg));
          const hi = Math.max(a, b);
          const lo = Math.min(a, b);
          return (hi + 0.05) / (lo + 0.05);
        }""")
    assert ratio >= kit.CONTRAST_AA, (
        f"body text against its background must meet the WCAG AA contrast bar of "
        f"{kit.CONTRAST_AA}, measured {ratio:.2f}")


def test_narrow_viewport_has_no_sideways_overflow(page):
    page.set_viewport_size(kit.NARROW_VIEWPORT)
    for route in ("/", "/work", "/about", "/contact", "/legal"):
        page.goto(kit.absolute(route))
        overflow = page.evaluate(
            "() => document.documentElement.scrollWidth - "
            "document.documentElement.clientWidth")
        assert overflow <= 1, (
            f"{route} overflows sideways by {overflow}px at "
            f"{kit.NARROW_VIEWPORT['width']}px wide")


def test_every_generated_image_carries_alternative_text(page):
    for route in ("/", "/work", "/about"):
        page.goto(kit.absolute(route))
        missing = page.eval_on_selector_all(
            "img",
            """nodes => nodes
                 .filter(n => n.getAttribute('aria-hidden') !== 'true')
                 .filter(n => !(n.getAttribute('alt') || '').trim())
                 .map(n => n.getAttribute('src') || n.outerHTML.slice(0, 80))""")
        assert not missing, (
            f"{route} carries content images with no alternative text: {missing!r}")


def test_project_index_opens_in_list_mode(raw, page):
    response = raw.get("/work")
    assert response.status_code == 200, kit.describe(response)
    for mode in kit.VIEW_MODES:
        assert mode in response.text, (
            f"the index offers the {mode!r} view mode: {response.text[:400]!r}")
    page.goto(kit.absolute("/work"))
    active = page.eval_on_selector_all(
        "[aria-selected='true'], [aria-current='true'], .is-active, [data-active='true']",
        "nodes => nodes.map(n => (n.textContent || '').trim()).filter(Boolean)")
    assert any(kit.DEFAULT_VIEW_MODE.lower() in a.lower() for a in active), (
        f"the index opens in {kit.DEFAULT_VIEW_MODE!r}, marked active; the marked "
        f"controls read {active!r}")


def test_view_mode_choice_survives_a_move_to_another_route(page):
    page.goto(kit.absolute("/work"))
    page.get_by_text("Gallery", exact=True).first.click()
    page.goto(kit.absolute("/about"))
    page.goto(kit.absolute("/work"))
    active = page.eval_on_selector_all(
        "[aria-selected='true'], [aria-current='true'], .is-active, [data-active='true']",
        "nodes => nodes.map(n => (n.textContent || '').trim()).filter(Boolean)")
    assert any("gallery" in a.lower() for a in active), (
        f"the chosen view mode survives a move to another route and back; the marked "
        f"controls read {active!r}")


def test_pinned_interface_copy_appears_verbatim(page):
    page.goto(kit.absolute("/"))
    home = page.inner_text("body")
    for word in kit.HERO_WORDS:
        assert word in home, f"the hero carries the word {word!r}"
    for statement in kit.HOME_STATEMENTS:
        assert statement in home, f"the home route carries the statement {statement!r}"
    for statistic in kit.STATISTICS:
        assert statistic in home, f"the home route carries the statistic {statistic!r}"
    assert kit.AWARD_SUMMARY in home, f"the awards list ends on {kit.AWARD_SUMMARY!r}"
    assert kit.PUBLICATION_SUMMARY in home, (
        f"the publications list ends on {kit.PUBLICATION_SUMMARY!r}")
    assert kit.FOOTER_IDENTITY in home, f"the footer carries {kit.FOOTER_IDENTITY!r}"
    for entry in kit.FOOTER_NAV + kit.FOOTER_MEDIA + kit.FOOTER_HOURS + kit.LICENCES + \
            kit.CREDITS + kit.ADDRESSES:
        assert entry in home, f"the footer carries {entry!r}"
    page.goto(kit.absolute("/contact"))
    contact = page.inner_text("body")
    for email in kit.CONTACT_EMAILS:
        assert email in contact, f"the contact route carries {email!r}"


def test_navigation_marks_the_active_route(page):
    for route, label in (("/work", "Work"), ("/about", "About"), ("/contact", "Contact")):
        page.goto(kit.absolute(route))
        marked = page.eval_on_selector_all(
            "nav [aria-current], nav .is-active, nav [data-active='true']",
            "nodes => nodes.map(n => (n.textContent || '').trim()).filter(Boolean)")
        assert any(label.lower() == m.lower() for m in marked), (
            f"{route} marks {label!r} as the active navigation link; marked links read "
            f"{marked!r}")
        for link in kit.NAV_LINKS:
            assert link in page.inner_text("body"), (
                f"{route} carries the navigation link {link!r}")


def test_public_routes_resolve_at_their_pinned_addresses(raw):
    for route in kit.PUBLIC_ROUTES:
        response = raw.get(route)
        assert response.status_code == 200, (
            f"the public route {route} must resolve when opened cold: "
            f"{kit.describe(response)}")
        assert "<html" in response.text.lower(), (
            f"{route} must answer with finished markup rather than an empty shell: "
            f"{response.text[:200]!r}")
    detail = raw.get("/work/" + "pokrovskoe-private-house")
    assert detail.status_code in (200, 404), kit.describe(detail)


def test_reduced_motion_resolves_every_reveal_to_its_end_state(page):
    page.emulate_media(reduced_motion="reduce")
    page.goto(kit.absolute("/"))
    hidden = page.evaluate(
        """() => {
          const nodes = Array.from(document.querySelectorAll('h1, h2, h3, p'))
            .filter(n => (n.textContent || '').trim().length > 8)
            .slice(0, 40);
          return nodes.filter(n => {
            const s = getComputedStyle(n);
            const r = n.getBoundingClientRect();
            if (r.top > window.innerHeight * 1.2) return false;
            return parseFloat(s.opacity) < 0.9;
          }).map(n => (n.textContent || '').trim().slice(0, 40));
        }""")
    assert not hidden, (
        f"under a reduced-motion preference every reveal resolves to its end state, so "
        f"nothing above the fold stays transparent: {hidden!r}")


def test_legal_chapters_expand_and_expose_their_state(page):
    page.goto(kit.absolute("/legal"))
    states = page.eval_on_selector_all(
        "[aria-expanded]", "nodes => nodes.map(n => n.getAttribute('aria-expanded'))")
    assert len(states) >= kit.LEGAL_COUNT, (
        f"each of the {kit.LEGAL_COUNT} chapters exposes whether it is open; found "
        f"{len(states)} controls that do")
    control = page.locator("[aria-expanded]").first
    before = control.get_attribute("aria-expanded")
    control.focus()
    page.keyboard.press("Enter")
    after = page.locator("[aria-expanded]").first.get_attribute("aria-expanded")
    assert after != before, (
        f"a chapter opens from the keyboard and says so: stayed {before!r}")
