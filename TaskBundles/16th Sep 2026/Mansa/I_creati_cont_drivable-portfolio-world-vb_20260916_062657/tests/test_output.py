from __future__ import annotations

import os
import re
from concurrent.futures import ThreadPoolExecutor

from _shapes import flatten, items
from appclient import client
from conftest import (
    CONFLICT,
    CONFLICT_ERROR,
    CONFLICT_MESSAGE,
    CREATED,
    DENIED,
    DENIED_OR_MISSING,
    DRAFT_SLUG,
    DRAFT_TITLE,
    OBJECT_KEY_MIDDLE,
    OBJECT_KEY_PREFIX,
    OWNER_EMAIL,
    PNG_HEADER,
    POSTER_ERROR,
    PUBLISHED_SLUGS,
    SEEDED_PASSWORD_DEFAULT,
    create_draft,
    free_point,
    manifest_slugs,
    occupied_point,
    page,
    png_bytes,
    project_id_of,
    public_project_slugs,
    publish,
    sha256_hex,
    settle,
    unpublish,
    upload_poster,
    probe_suffix,
    wait_for_object,
    world_manifest,
)


def test_owner_login_returns_access_token(owner_token, db):
    assert isinstance(owner_token, str) and owner_token.strip(), (
        f"login for {OWNER_EMAIL} returned no usable access_token: {owner_token!r}"
    )
    row = db.owner_row()
    assert row is not None, (
        f"the seeded account {OWNER_EMAIL} has no row in owner_account, so the seed "
        f"never ran or the table carries a different name"
    )
    stored = str(row.get("password_hash", ""))
    assert stored, (
        f"the seeded account {OWNER_EMAIL} carries no password_hash column value"
    )
    assert SEEDED_PASSWORD_DEFAULT not in stored, (
        f"owner_account.password_hash holds the password in plain text for "
        f"{OWNER_EMAIL}"
    )


def test_world_manifest_lists_only_published_projects(anon_client, db):
    manifest = world_manifest(anon_client)
    slugs = manifest_slugs(manifest)
    for slug in PUBLISHED_SLUGS:
        assert slug in slugs, (
            f"GET /api/world omits the published project {slug!r}; it carries "
            f"{sorted(slugs)}"
        )
    assert DRAFT_SLUG not in slugs, (
        f"GET /api/world carries the draft {DRAFT_SLUG!r}, so an unpublished project "
        f"reached the world manifest; it carries {sorted(slugs)}"
    )
    draft = db.project_by_slug(DRAFT_SLUG)
    assert draft is not None, (
        f"the seeded draft {DRAFT_SLUG!r} has no project row, so the seed never ran"
    )
    assert not draft.get("published"), (
        f"the seeded draft {DRAFT_SLUG!r} carries published={draft.get('published')!r}, "
        f"so the seed published it"
    )


def test_published_project_detail_is_public(anon_client):
    response = anon_client.get(f"/projects/{PUBLISHED_SLUGS[0]}")
    assert response.status_code == 200, (
        f"GET /api/projects/{PUBLISHED_SLUGS[0]} returned {response.status_code} to an "
        f"anonymous caller: {response.text[:400]}"
    )
    body = response.json()
    assert PUBLISHED_SLUGS[0] in flatten(body), (
        f"GET /api/projects/{PUBLISHED_SLUGS[0]} returned a body that never names the "
        f"slug: {response.text[:400]}"
    )


def test_project_order_follows_adjacency_not_dates(anon_client):
    ordered = [s for s in public_project_slugs(anon_client) if s in PUBLISHED_SLUGS]
    assert ordered == list(PUBLISHED_SLUGS), (
        f"GET /api/projects returned the published projects in the order {ordered}, "
        f"but the adjacency relation orders them {list(PUBLISHED_SLUGS)}"
    )


def test_text_route_lists_published_projects_only(anon_client):
    response = anon_client.get(page("/content"))
    assert response.status_code == 200, (
        f"GET /content returned {response.status_code} to an anonymous visitor: "
        f"{response.text[:400]}"
    )
    body = response.text
    for slug in PUBLISHED_SLUGS:
        assert slug in body, (
            f"the text route at /content never names the published project {slug!r}"
        )
    assert DRAFT_SLUG not in body and DRAFT_TITLE not in body, (
        f"the text route at /content names the draft {DRAFT_SLUG!r}, so an unpublished "
        f"project reached a public listing"
    )


def test_internal_links_on_public_routes_resolve(anon_client):
    broken = []
    for route in ("/", "/content"):
        response = anon_client.get(page(route))
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}: {response.text[:300]}"
        )
        targets = set(re.findall(r'href="(/[^"#?]*)"', response.text))
        for target in sorted(targets):
            if target.startswith("/studio"):
                continue
            hit = anon_client.get(page(target))
            if hit.status_code >= 400:
                broken.append((route, target, hit.status_code))
    assert not broken, (
        f"internal links on the public routes do not resolve: {broken}"
    )


def test_unknown_address_answers_not_found(anon_client):
    unknown = f"/no-such-place-{probe_suffix()}"
    response = anon_client.get(page(unknown))
    assert response.status_code == 404, (
        f"GET {unknown} returned {response.status_code}, but an unknown address answers "
        f"not-found: {response.text[:300]}"
    )
    assert response.text.strip(), (
        f"GET {unknown} answered not-found with an empty body, so the product renders "
        f"no not-found page of its own"
    )


def test_health_endpoint_reports_ready(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:300]}"
    )


def test_cookie_choice_survives_a_reload(anon_client):
    with client() as fresh:
        response = fresh.post("/cookie-choice", json={"choice": "declined"})
        assert response.status_code in CREATED, (
            f"POST /api/cookie-choice returned {response.status_code}: "
            f"{response.text[:300]}"
        )
        assert "declined" in flatten(response.json()), (
            f"POST /api/cookie-choice did not echo the stored answer: "
            f"{response.text[:300]}"
        )
        again = fresh.get("/cookie-choice")
        assert again.status_code == 200, (
            f"GET /api/cookie-choice returned {again.status_code} after the answer was "
            f"stored: {again.text[:300]}"
        )
        assert "declined" in flatten(again.json()), (
            f"the stored cookie answer did not survive: {again.text[:300]}"
        )


def test_seeded_projects_row_state_matches_manifest(anon_client, db):
    slugs = manifest_slugs(world_manifest(anon_client))
    for slug in PUBLISHED_SLUGS:
        row = db.project_by_slug(slug)
        assert row is not None, (
            f"the seeded project {slug!r} has no row in project, so the seed never ran"
        )
        assert row.get("published"), (
            f"the seeded project {slug!r} carries published={row.get('published')!r} in "
            f"the database while the world manifest lists {sorted(slugs)}"
        )
        assert row.get("zone"), (
            f"the seeded project {slug!r} carries no zone, but every project is "
            f"assigned to one of the authored area keys"
        )
    for slug in PUBLISHED_SLUGS:
        assert db.count_projects_with_slug(slug) == 1, (
            f"the project table holds "
            f"{db.count_projects_with_slug(slug)} rows for the seeded slug {slug!r}; a "
            f"seed that is not idempotent duplicates its rows on every restart"
        )


def test_publish_persists_row_and_stored_object(owner_client, db, bucket):
    suffix = probe_suffix()
    x, y, z = free_point(db, 11)
    created = create_draft(owner_client, suffix, x, y, z)
    pid = project_id_of(created)
    upload_poster(owner_client, pid, png_bytes(suffix))
    response = publish(owner_client, pid)
    assert response.status_code in CREATED, (
        f"publishing project {pid} at a free point returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    row = db.project_by_slug(f"probe-{suffix}")
    assert row is not None, (
        f"project probe-{suffix} was created through the API but has no row in project"
    )
    assert row.get("published"), (
        f"project probe-{suffix} was published but its row carries "
        f"published={row.get('published')!r}"
    )
    images = db.images_for(row["id"])
    assert images, (
        f"project probe-{suffix} was published with a poster but project_image holds no "
        f"row for it"
    )
    key = str(images[0].get("object_key", ""))
    assert wait_for_object(bucket, key), (
        f"project_image row names object key {key!r}, but the bucket holds no object at "
        f"that key, so the bytes never reached the store"
    )


def test_poster_upload_lands_in_bucket_at_scheme_key(owner_client, db, bucket):
    suffix = probe_suffix()
    x, y, z = free_point(db, 23)
    created = create_draft(owner_client, suffix, x, y, z)
    pid = project_id_of(created)
    payload = png_bytes(suffix)
    image = upload_poster(owner_client, pid, payload)
    key = str(image.get("object_key", ""))
    assert key.startswith(f"{OBJECT_KEY_PREFIX}{pid}{OBJECT_KEY_MIDDLE}"), (
        f"the stored object key {key!r} does not follow the pinned scheme "
        f"projects/{{project_id}}/posters/{{sha256_of_bytes}}.{{ext}} for project {pid}"
    )
    assert sha256_hex(payload) in key, (
        f"the stored object key {key!r} does not carry the sha256 of the uploaded "
        f"bytes, so the key is not derived from the bytes"
    )
    assert wait_for_object(bucket, key), (
        f"no object exists in the bucket at {key!r} after the upload returned success, "
        f"so the bytes are not in the object store"
    )


def test_duplicate_poster_upload_stores_one_object(owner_client, db, bucket):
    suffix = probe_suffix()
    x, y, z = free_point(db, 37)
    created = create_draft(owner_client, suffix, x, y, z)
    pid = project_id_of(created)
    payload = png_bytes(suffix)
    first = upload_poster(owner_client, pid, payload)
    second = upload_poster(owner_client, pid, payload)
    assert str(first.get("object_key")) == str(second.get("object_key")), (
        f"uploading one file twice produced two object keys, "
        f"{first.get('object_key')!r} then {second.get('object_key')!r}; the key is "
        f"derived from the bytes so both uploads name one object"
    )
    stored = bucket.list(f"{OBJECT_KEY_PREFIX}{pid}{OBJECT_KEY_MIDDLE}")
    assert len(stored) == 1, (
        f"the bucket holds {len(stored)} objects under project {pid} after one file was "
        f"uploaded twice: {stored}"
    )
    rows = db.images_for(project_id_of(created))
    assert len(rows) == 1, (
        f"project_image holds {len(rows)} rows for project {pid} after one file was "
        f"uploaded twice"
    )


def test_published_poster_file_streams_to_anonymous_reader(owner_client, anon_client, db):
    suffix = probe_suffix()
    x, y, z = free_point(db, 53)
    created = create_draft(owner_client, suffix, x, y, z)
    pid = project_id_of(created)
    image = upload_poster(owner_client, pid, png_bytes(suffix))
    assert image.get("alt_text"), (
        f"the uploaded poster carries no alt_text, but alternative text travels with "
        f"the image: {str(image)[:300]}"
    )
    published = publish(owner_client, pid)
    assert published.status_code in CREATED, (
        f"publishing project {pid} returned {published.status_code}: "
        f"{published.text[:400]}"
    )
    response = anon_client.get(f"/projects/{pid}/images/{image['id']}")
    assert response.status_code == 200, (
        f"an anonymous reader got {response.status_code} for the poster of the "
        f"published project {pid}: {response.text[:300]}"
    )
    assert response.content.startswith(PNG_HEADER), (
        f"the poster endpoint for published project {pid} returned "
        f"{response.content[:16]!r}, which is not the uploaded bytes"
    )


def test_unpublish_frees_coordinates_for_another_draft(owner_client, db):
    first_suffix = probe_suffix()
    second_suffix = probe_suffix()
    x, y, z = free_point(db, 71)
    first = create_draft(owner_client, first_suffix, x, y, z)
    first_id = project_id_of(first)
    upload_poster(owner_client, first_id, png_bytes(first_suffix))
    opened = publish(owner_client, first_id)
    assert opened.status_code in CREATED, (
        f"publishing the first project at a free point returned {opened.status_code}: "
        f"{opened.text[:400]}"
    )
    second = create_draft(owner_client, second_suffix, x, y, z)
    second_id = project_id_of(second)
    upload_poster(owner_client, second_id, png_bytes(second_suffix))
    blocked = publish(owner_client, second_id)
    assert blocked.status_code in CONFLICT, (
        f"publishing a second project onto an occupied point returned "
        f"{blocked.status_code}: {blocked.text[:400]}"
    )
    released = unpublish(owner_client, first_id)
    assert released.status_code in CREATED, (
        f"unpublishing project {first_id} returned {released.status_code}: "
        f"{released.text[:400]}"
    )
    retried = publish(owner_client, second_id)
    assert retried.status_code in CREATED, (
        f"publishing onto the point freed by the unpublish returned "
        f"{retried.status_code}, so unpublishing did not free the coordinates: "
        f"{retried.text[:400]}"
    )


def test_whisper_wall_never_exceeds_thirty_rows(anon_client, db):
    for index in range(4):
        payload = {
            "uuid": f"probe-{probe_suffix()}",
            "message": f"probe {index}",
            "country_code": "fr",
            "x": 1,
            "y": 0,
            "z": 1,
        }
        response = anon_client.post("/whispers", json=payload)
        assert response.status_code in CREATED, (
            f"POST /api/whispers returned {response.status_code} for a valid message: "
            f"{response.text[:300]}"
        )
    stored = db.count_whispers()
    assert stored <= 30, (
        f"the whisper table holds {stored} rows, but the wall holds at most 30 and the "
        f"newest insert evicts the oldest"
    )
    listed = items(anon_client.get("/whispers").json())
    assert len(listed) <= 30, (
        f"GET /api/whispers returned {len(listed)} whispers, but the wall holds at most 30"
    )


def test_draft_direct_address_is_denied_to_anonymous(anon_client):
    api_response = anon_client.get(f"/projects/{DRAFT_SLUG}")
    assert api_response.status_code in DENIED_OR_MISSING, (
        f"GET /api/projects/{DRAFT_SLUG} returned {api_response.status_code} to an "
        f"anonymous caller who guessed the draft slug exactly: "
        f"{api_response.text[:300]}"
    )
    page_response = anon_client.get(page(f"/content/projects/{DRAFT_SLUG}"))
    assert page_response.status_code in DENIED_OR_MISSING, (
        f"GET /content/projects/{DRAFT_SLUG} returned {page_response.status_code}, so "
        f"the draft is reachable at its own address: {page_response.text[:300]}"
    )
    assert DRAFT_TITLE not in page_response.text, (
        f"the response for the draft address carries the draft title {DRAFT_TITLE!r}, "
        f"so unpublished content reached an anonymous reader"
    )


def test_draft_poster_upload_is_denied_without_token(owner_client, anon_client, db):
    suffix = probe_suffix()
    x, y, z = free_point(db, 89)
    created = create_draft(owner_client, suffix, x, y, z)
    pid = project_id_of(created)
    image = upload_poster(owner_client, pid, png_bytes(suffix))
    owner_read = owner_client.get(f"/projects/{pid}/images/{image['id']}")
    assert owner_read.status_code == 200, (
        f"the owner got {owner_read.status_code} reading the poster of their own draft "
        f"{pid}: {owner_read.text[:300]}"
    )
    anon_read = anon_client.get(f"/projects/{pid}/images/{image['id']}")
    assert anon_read.status_code in DENIED_OR_MISSING, (
        f"an anonymous caller got {anon_read.status_code} for the poster of the "
        f"unpublished project {pid}, so draft bytes are readable without an owner token"
    )
    assert not anon_read.content.startswith(PNG_HEADER), (
        f"the anonymous poster request for draft {pid} returned the stored bytes"
    )


def test_draft_is_absent_from_the_text_route(anon_client):
    listed = public_project_slugs(anon_client)
    assert DRAFT_SLUG not in listed, (
        f"GET /api/projects lists the draft {DRAFT_SLUG!r} among {listed}"
    )
    response = anon_client.get(page("/content"))
    assert response.status_code == 200, (
        f"GET /content returned {response.status_code}: {response.text[:300]}"
    )
    assert DRAFT_SLUG not in response.text, (
        f"the text route listing carries the draft slug {DRAFT_SLUG!r}"
    )


def test_anonymous_cannot_create_project_denied(anon_client, db):
    before = len(db.published_projects())
    payload = {
        "slug": f"intruder-{probe_suffix()}",
        "title": "Intruder",
        "summary": "written without a session",
        "link": "https://example.com/intruder",
        "world_x": 1234,
        "world_y": 0,
        "world_z": 4321,
        "zone": "projects",
    }
    response = anon_client.post("/studio/projects", json=payload)
    assert response.status_code in DENIED, (
        f"POST /api/studio/projects returned {response.status_code} to a caller with no "
        f"owner session: {response.text[:300]}"
    )
    assert db.project_by_slug(payload["slug"]) is None, (
        f"the denied request still wrote a project row for {payload['slug']!r}"
    )
    assert len(db.published_projects()) == before, (
        f"the published project count changed from {before} after a denied write"
    )


def test_anonymous_cannot_publish_project_denied(anon_client, db):
    draft = db.project_by_slug(DRAFT_SLUG)
    assert draft is not None, (
        f"the seeded draft {DRAFT_SLUG!r} has no project row, so the seed never ran"
    )
    response = anon_client.post(f"/studio/projects/{draft['id']}/publish")
    assert response.status_code in DENIED, (
        f"POST /api/studio/projects/{draft['id']}/publish returned "
        f"{response.status_code} to a caller with no owner session: "
        f"{response.text[:300]}"
    )
    after = db.project_by_slug(DRAFT_SLUG)
    assert not after.get("published"), (
        f"the draft {DRAFT_SLUG!r} is published after a denied publish request"
    )


def test_anonymous_cannot_read_page_view_record_denied(anon_client):
    response = anon_client.get("/page-views")
    assert response.status_code in DENIED, (
        f"GET /api/page-views returned {response.status_code} to a caller with no owner "
        f"session: {response.text[:300]}"
    )


def test_login_with_wrong_password_is_rejected(anon_client):
    response = anon_client.post(
        "/auth/login", json={"email": OWNER_EMAIL, "password": "not-the-password-2026"}
    )
    assert response.status_code >= 400, (
        f"POST /api/auth/login with a wrong password returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    assert response.status_code < 500, (
        f"POST /api/auth/login with a wrong password returned a server error "
        f"{response.status_code}, but a bad credential is a client error: "
        f"{response.text[:300]}"
    )
    assert "access_token" not in response.text, (
        f"a rejected sign-in still returned a token: {response.text[:300]}"
    )
    assert SEEDED_PASSWORD_DEFAULT not in response.text, (
        f"the rejected sign-in response names the real password: {response.text[:300]}"
    )


def test_publish_onto_occupied_coordinates_is_rejected(owner_client, db):
    x, y, z = occupied_point(db)
    occupant = [
        row for row in db.published_projects()
        if (int(row["world_x"]), int(row["world_y"]), int(row["world_z"])) == (x, y, z)
    ][0]
    suffix = probe_suffix()
    created = create_draft(owner_client, suffix, x, y, z)
    pid = project_id_of(created)
    upload_poster(owner_client, pid, png_bytes(suffix))
    response = publish(owner_client, pid)
    assert response.status_code in CONFLICT, (
        f"publishing project {pid} onto coordinates ({x}, {y}, {z}) already held by "
        f"{occupant['slug']!r} returned {response.status_code}: {response.text[:400]}"
    )
    body = response.text
    assert CONFLICT_ERROR in body, (
        f"the refusal does not carry the error code {CONFLICT_ERROR!r}: {body[:400]}"
    )
    assert CONFLICT_MESSAGE in body, (
        f"the refusal does not carry the pinned message {CONFLICT_MESSAGE!r}: "
        f"{body[:400]}"
    )
    assert str(occupant["slug"]) in body, (
        f"the refusal never names the slug of the project already standing at those "
        f"coordinates ({occupant['slug']!r}): {body[:400]}"
    )
    refused = db.project_by_slug(f"probe-{suffix}")
    assert not refused.get("published"), (
        f"the refused project probe-{suffix} is published anyway"
    )
    assert not refused.get("published_at"), (
        f"the refused project probe-{suffix} carries a published timestamp "
        f"{refused.get('published_at')!r}"
    )
    still_there = db.project_by_slug(str(occupant["slug"]))
    assert still_there.get("published"), (
        f"the refused publish disturbed the project already in place, "
        f"{occupant['slug']!r}"
    )
    assert db.count_published_at(x, y, z) == 1, (
        f"{db.count_published_at(x, y, z)} published projects now sit at "
        f"({x}, {y}, {z}); at most one may"
    )


def test_concurrent_publish_at_one_point_yields_one_winner(owner_client, owner_token, db):
    x, y, z = free_point(db, 101)
    ids = []
    for _ in range(2):
        suffix = probe_suffix()
        created = create_draft(owner_client, suffix, x, y, z)
        pid = project_id_of(created)
        upload_poster(owner_client, pid, png_bytes(suffix))
        ids.append(pid)

    def attempt(project_id):
        with client(owner_token) as racer:
            return racer.post(f"/studio/projects/{project_id}/publish").status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(attempt, ids))

    winners = [code for code in results if code in CREATED]
    assert len(winners) == 1, (
        f"two simultaneous publish requests for ({x}, {y}, {z}) returned {results}; "
        f"exactly one may succeed"
    )
    assert db.count_published_at(x, y, z) == 1, (
        f"{db.count_published_at(x, y, z)} published projects sit at ({x}, {y}, {z}) "
        f"after two simultaneous publish requests"
    )


def test_publish_without_poster_is_rejected(owner_client, db):
    suffix = probe_suffix()
    x, y, z = free_point(db, 131)
    created = create_draft(owner_client, suffix, x, y, z)
    pid = project_id_of(created)
    response = publish(owner_client, pid)
    assert response.status_code >= 400, (
        f"publishing project {pid} with no poster returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    assert response.status_code < 500, (
        f"publishing with no poster returned a server error {response.status_code}, but "
        f"an invalid publish is a client error: {response.text[:400]}"
    )
    assert POSTER_ERROR in response.text, (
        f"the refusal does not carry the error code {POSTER_ERROR!r}: "
        f"{response.text[:400]}"
    )
    row = db.project_by_slug(f"probe-{suffix}")
    assert not row.get("published"), (
        f"project probe-{suffix} is published despite carrying no poster"
    )


def test_whisper_over_limit_is_refused(anon_client, db):
    before = db.count_whispers()
    payload = {
        "uuid": f"probe-{probe_suffix()}",
        "message": "x" * 31,
        "country_code": "fr",
        "x": 2,
        "y": 0,
        "z": 2,
    }
    response = anon_client.post("/whispers", json=payload)
    assert response.status_code >= 400, (
        f"POST /api/whispers accepted a 31-character message with "
        f"{response.status_code}: {response.text[:300]}"
    )
    assert response.status_code < 500, (
        f"an over-limit message returned a server error {response.status_code}, but an "
        f"invalid message is a client error: {response.text[:300]}"
    )
    assert db.count_whispers() == before, (
        f"the whisper count moved from {before} to {db.count_whispers()} after a "
        f"refused message"
    )


def test_whisper_decoy_field_submission_is_refused(anon_client, db):
    before = db.count_whispers()
    payload = {
        "uuid": f"probe-{probe_suffix()}",
        "message": "a passing robot",
        "country_code": "fr",
        "x": 3,
        "y": 0,
        "z": 3,
        "website": "https://example.com/bot",
    }
    response = anon_client.post("/whispers", json=payload)
    assert response.status_code >= 400, (
        f"POST /api/whispers accepted a submission that filled the unattended decoy "
        f"field, returning {response.status_code}: {response.text[:300]}"
    )
    assert db.count_whispers() == before, (
        f"the whisper count moved from {before} to {db.count_whispers()} after a "
        f"submission that filled the decoy field"
    )


def test_repeated_whisper_submissions_are_refused(anon_client, db):
    visitor = f"probe-{probe_suffix()}"
    codes = []
    for index in range(5):
        response = anon_client.post(
            "/whispers",
            json={
                "uuid": visitor,
                "message": f"burst {index}",
                "country_code": "fr",
                "x": 4,
                "y": 0,
                "z": 4,
            },
        )
        codes.append(response.status_code)
    assert any(code >= 400 for code in codes), (
        f"five whispers sent back to back from one visitor identifier all succeeded "
        f"({codes}); a rapid repeat is refused"
    )
    rows = db.count_whispers()
    assert rows <= 30, (
        f"the whisper table holds {rows} rows after a burst from one visitor"
    )


def test_lap_with_inconsistent_splits_is_refused(anon_client, db):
    before = db.count_laps()
    payload = {
        "uuid": f"probe-{probe_suffix()}",
        "tag": "PRB",
        "country_code": "fr",
        "duration_ms": 91000,
        "checkpoint_splits": [1000, 1000, 1000],
    }
    response = anon_client.post("/laps", json=payload)
    assert response.status_code >= 400, (
        f"POST /api/laps accepted a lap whose splits sum to 3000 against a stated "
        f"duration of 91000, returning {response.status_code}: {response.text[:300]}"
    )
    assert response.status_code < 500, (
        f"an inconsistent lap returned a server error {response.status_code}, but an "
        f"invalid lap is a client error: {response.text[:300]}"
    )
    assert db.count_laps() == before, (
        f"the lap count moved from {before} to {db.count_laps()} after a refused lap"
    )


def test_empty_leaderboard_returns_empty_array(anon_client):
    response = anon_client.get("/leaderboard")
    assert response.status_code == 200, (
        f"GET /api/leaderboard returned {response.status_code}: {response.text[:300]}"
    )
    rows = items(response.json())
    assert isinstance(rows, list), (
        f"GET /api/leaderboard did not return a list: {response.text[:300]}"
    )


def test_page_views_are_recorded_for_public_routes(anon_client, owner_client, db):
    before = db.count_page_views("/content")
    visit = anon_client.get(page("/content"))
    assert visit.status_code == 200, (
        f"GET /content returned {visit.status_code}: {visit.text[:300]}"
    )
    settle()
    after = db.count_page_views("/content")
    assert after > before, (
        f"the page_view count for /content stayed at {before} after a public visit, so "
        f"page views are not recorded"
    )
    owner_read = owner_client.get("/page-views")
    assert owner_read.status_code == 200, (
        f"the owner got {owner_read.status_code} reading the page view record: "
        f"{owner_read.text[:300]}"
    )
    assert "/content" in flatten(owner_read.json()), (
        f"the owner-readable page view record never names the /content route: "
        f"{owner_read.text[:300]}"
    )


def test_signup_route_does_not_exist(anon_client):
    for path in ("/auth/signup", "/auth/register"):
        response = anon_client.post(
            path, json={"email": f"intruder-{probe_suffix()}@example.com", "password": "x"}
        )
        assert response.status_code >= 400, (
            f"POST /api{path} returned {response.status_code}, so a public route creates "
            f"an account: {response.text[:300]}"
        )


def test_malformed_token_is_denied(db):
    draft = db.project_by_slug(DRAFT_SLUG)
    assert draft is not None, (
        f"the seeded draft {DRAFT_SLUG!r} has no project row, so the seed never ran"
    )
    with client("not-a-real-token") as impostor:
        response = impostor.post(f"/studio/projects/{draft['id']}/publish")
        assert response.status_code in DENIED, (
            f"a malformed bearer token got {response.status_code} on the publish "
            f"endpoint: {response.text[:300]}"
        )
    after = db.project_by_slug(DRAFT_SLUG)
    assert not after.get("published"), (
        f"the draft {DRAFT_SLUG!r} is published after a request carrying a malformed "
        f"token"
    )


def test_self_adjacent_project_is_refused(owner_client, db):
    suffix = probe_suffix()
    x, y, z = free_point(db, 149)
    created = create_draft(owner_client, suffix, x, y, z)
    pid = project_id_of(created)
    response = owner_client.patch(
        f"/studio/projects/{pid}", json={"previous_slug": f"probe-{suffix}"}
    )
    assert response.status_code >= 400, (
        f"PATCH /api/studio/projects/{pid} accepted a project naming itself as its own "
        f"previous neighbour, returning {response.status_code}: {response.text[:300]}"
    )
    row = db.project_by_slug(f"probe-{suffix}")
    assert str(row.get("previous_slug") or "") != f"probe-{suffix}", (
        f"project probe-{suffix} names itself as its own previous neighbour in the "
        f"database"
    )


def test_root_document_is_server_rendered_with_state_classes(anon_client):
    response = anon_client.get(page("/"))
    assert response.status_code == 200, (
        f"GET / returned {response.status_code}: {response.text[:300]}"
    )
    body = response.text
    assert "<html" in body.lower(), (
        f"GET / did not return an HTML document: {body[:300]}"
    )
    filters = [
        "input-filter-intro",
        "input-filter-wandering",
        "input-filter-menu",
        "input-filter-modal",
        "input-filter-cinematic",
    ]
    assert any(name in body for name in filters), (
        f"the document served at / carries none of the input-filter class names "
        f"{filters}, so the root element does not name which consumer owns the keyboard"
    )
    for family in ("is-server-offline", "is-mode-"):
        assert family in body, (
            f"the document served at / never carries the {family!r} state class family"
        )


def test_behaviour_hooks_are_prefixed_separately_from_styling(anon_client):
    body = anon_client.get(page("/")).text
    hooks = ["js-close", "js-content", "js-audio-toggle", "js-respawn"]
    found = [hook for hook in hooks if hook in body]
    assert found, (
        f"the document served at / carries none of the prefixed behaviour hooks "
        f"{hooks}, so code and styling share one set of names"
    )
    assert "data-tabs-name" in body, (
        f"the document served at / carries no data-tabs-name attribute, so tab identity "
        f"has no configuration hook"
    )


def test_credentials_note_and_reserved_directories_exist():
    note = "/app/USER_README.md"
    assert os.path.isfile(note), (
        f"{note} does not exist, so the seeded sign-in is written nowhere"
    )
    with open(note, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    assert OWNER_EMAIL in text, (
        f"{note} never names the seeded account {OWNER_EMAIL}"
    )
    assert SEEDED_PASSWORD_DEFAULT in text, (
        f"{note} never names the seeded password"
    )
    for reserved in ("/app/.browser_screenshots", "/app/.downloads"):
        assert os.path.isdir(reserved), (
            f"the reserved directory {reserved} does not exist at the app root"
        )


def test_public_pages_serve_no_binary_asset_files(anon_client):
    binary_types = ("image/", "audio/", "video/", "model/")
    offenders = []
    for route in ("/", "/content"):
        response = anon_client.get(page(route))
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}: {response.text[:300]}"
        )
        targets = set(re.findall(r'src="(/[^"#?]*)"', response.text))
        for target in sorted(targets):
            hit = anon_client.get(page(target))
            kind = hit.headers.get("content-type", "")
            if any(kind.startswith(prefix) for prefix in binary_types):
                offenders.append((route, target, kind))
    assert not offenders, (
        f"the deployed build serves binary asset files from its public pages: "
        f"{offenders}"
    )


def test_public_surfaces_need_no_sign_in(anon_client):
    for path in ("/world", "/projects", "/whispers", "/leaderboard", "/areas",
                 "/achievements"):
        response = anon_client.get(path)
        assert response.status_code == 200, (
            f"GET /api{path} returned {response.status_code} to a visitor with no "
            f"account: {response.text[:300]}"
        )
    for route in ("/", "/content"):
        response = anon_client.get(page(route))
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code} to a visitor with no account: "
            f"{response.text[:300]}"
        )
