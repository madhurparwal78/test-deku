"""The one pytest module for deku/scheduling-link-platform-vb.

Black box throughout: every assertion is made over HTTP, over a real browser
page, over the backing database through the capability adapter, or over the
object store through the capability adapter. Nothing here reads the agent's
source, its framework or its file layout.
"""

from __future__ import annotations

import os

import httpx
import pytest
from appclient import TIMEOUT, api_base, app_url, client, login
from conftest import (
    AUTHOR_EMAIL,
    BOOKING_PAGE_ROUTE,
    CORPUS_PASSWORD,
    DRAFT_ROUTE,
    LOGIN_ROUTE,
    OBJECT_KEY_PREFIX,
    PUBLIC_ROUTES,
    READ_ONLY_PUBLIC_ROUTES,
    READER_EMAIL,
    STATE_DRAFT,
    STATE_PUBLISHED,
    STUDIO_ROUTE,
    STUDIO_VIEWS_ROUTE,
    create_draft_page,
    page_url,
    png_bytes,
    probe_email,
    sha256_hex,
    signup,
    unique_token,
    upload_media,
    wait_for,
)

APP_ROOT = "/app"


def test_health_route_answers_ok(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, expected 200: "
        f"{response.text[:400]}"
    )


def test_first_response_carries_the_page_text(anon_client):
    response = httpx.get(app_url() + "/", timeout=TIMEOUT)
    assert response.status_code == 200, (
        f"GET / returned {response.status_code}: {response.text[:200]}"
    )
    assert "schedule your meetings" in response.text.lower(), (
        "the first response for / carries no headline text, so the page is not "
        f"produced on the server: {response.text[:400]}"
    )


def test_seeded_author_can_sign_in():
    token = login(AUTHOR_EMAIL, CORPUS_PASSWORD)
    assert token, f"login for {AUTHOR_EMAIL} returned an empty access_token"


def test_seeded_reader_can_sign_in():
    token = login(READER_EMAIL, CORPUS_PASSWORD)
    assert token, f"login for {READER_EMAIL} returned an empty access_token"


def test_login_with_wrong_password_is_denied(anon_client):
    response = anon_client.post(
        "/auth/login", json={"email": AUTHOR_EMAIL, "password": "not-the-password"}
    )
    assert response.status_code in (400, 401, 403, 422), (
        f"POST /api/auth/login with a wrong password returned "
        f"{response.status_code}, expected a client error: {response.text[:400]}"
    )
    assert "access_token" not in response.text, (
        f"a denied login still returned a token: {response.text[:400]}"
    )


def test_signup_creates_a_reader_account(db):
    email = probe_email()
    username = unique_token("visitor")
    outcome = signup(email, username)
    assert outcome["status"] in (200, 201), (
        f"POST /api/auth/signup returned {outcome['status']}: {outcome['body'][:400]}"
    )
    created = wait_for(lambda: db.user_by_email(email), f"user row for {email}")
    assert created["role"] == "reader", (
        f"signup created {email} with role {created['role']!r}, expected 'reader'"
    )


def test_signup_body_role_is_ignored(anon_client, db):
    email = probe_email()
    username = unique_token("visitor")
    response = anon_client.post(
        "/auth/signup",
        json={
            "email": email,
            "password": "verifier-pw-1",
            "username": username,
            "display_name": "Verifier Visitor",
            "role": "author",
        },
    )
    assert response.status_code in (200, 201), (
        f"POST /api/auth/signup carrying a role field returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    created = wait_for(lambda: db.user_by_email(email), f"user row for {email}")
    assert created["role"] == "reader", (
        f"a signup body naming role 'author' created {email} with role "
        f"{created['role']!r}; the role is never read from the body"
    )


def test_signup_with_taken_username_is_refused(anon_client, db):
    username = unique_token("visitor")
    first = probe_email()
    second = probe_email()
    opening = signup(first, username)
    assert opening["status"] in (200, 201), (
        f"the first signup for username {username!r} returned {opening['status']}: "
        f"{opening['body'][:400]}"
    )
    response = anon_client.post(
        "/auth/signup",
        json={
            "email": second,
            "password": "verifier-pw-1",
            "username": username,
            "display_name": "Verifier Visitor",
        },
    )
    assert response.status_code in (400, 409, 422), (
        f"a signup reusing username {username!r} returned {response.status_code}, "
        f"expected a client error: {response.text[:400]}"
    )
    assert db.count_users(second) == 0, (
        f"a refused signup still created a user row for {second}"
    )


def test_unknown_bearer_token_is_refused():
    with client("not-a-token-this-app-ever-issued") as c:
        response = c.get("/page-views")
    assert response.status_code in (401, 403), (
        f"GET /api/page-views with an unissued bearer token returned "
        f"{response.status_code}, expected 401 or 403: {response.text[:400]}"
    )


def test_new_page_row_is_stored_as_draft(author_client, db):
    slug = unique_token("draft-page")
    created = create_draft_page(author_client, slug, f"/{slug}")
    row = wait_for(lambda: db.page_by_slug(slug), f"pages row for slug {slug!r}")
    assert row["state"] == STATE_DRAFT, (
        f"a new page {slug!r} was stored in state {row['state']!r}, expected "
        f"{STATE_DRAFT!r}; created payload was {created}"
    )


def test_publish_records_the_published_moment(author_client, db):
    slug = unique_token("publish-page")
    create_draft_page(author_client, slug, f"/{slug}")
    response = author_client.patch(f"/pages/{slug}", json={"state": STATE_PUBLISHED})
    assert response.status_code in (200, 202), (
        f"PATCH /api/pages/{slug} to published returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    row = wait_for(
        lambda: (db.page_by_slug(slug) or {}).get("state") == STATE_PUBLISHED
        and db.page_by_slug(slug),
        f"pages row for {slug!r} reaching state published",
    )
    assert row["published_at"], (
        f"page {slug!r} reached state published with an empty published_at"
    )


def test_unpublish_returns_the_page_row_to_draft(author_client, db):
    slug = unique_token("unpublish-page")
    create_draft_page(author_client, slug, f"/{slug}")
    author_client.patch(f"/pages/{slug}", json={"state": STATE_PUBLISHED})
    wait_for(
        lambda: (db.page_by_slug(slug) or {}).get("state") == STATE_PUBLISHED,
        f"page {slug!r} reaching state published",
    )
    response = author_client.patch(f"/pages/{slug}", json={"state": STATE_DRAFT})
    assert response.status_code in (200, 202), (
        f"PATCH /api/pages/{slug} back to draft returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    row = wait_for(
        lambda: (db.page_by_slug(slug) or {}).get("state") == STATE_DRAFT
        and db.page_by_slug(slug),
        f"page {slug!r} returning to state draft",
    )
    assert row["state"] == STATE_DRAFT, (
        f"page {slug!r} is in state {row['state']!r} after unpublishing"
    )


def test_band_positions_are_gapless_within_a_page(author_client, db):
    slug = unique_token("band-page")
    created = create_draft_page(author_client, slug, f"/{slug}")
    page_id = created.get("id") or (db.page_by_slug(slug) or {}).get("id")
    assert page_id, f"the created page {slug!r} exposes no id: {created}"
    for position in (1, 2, 3):
        response = author_client.post(
            f"/pages/{slug}/bands",
            json={
                "position": position,
                "kind": "feature",
                "eyebrow": "Benefits",
                "headline": f"Band {position}",
                "body": "Composed by the verifier.",
            },
        )
        assert response.status_code in (200, 201), (
            f"POST /api/pages/{slug}/bands position {position} returned "
            f"{response.status_code}: {response.text[:400]}"
        )
    bands = wait_for(
        lambda: db.bands_for_page(page_id) if len(db.bands_for_page(page_id)) == 3 else None,
        f"three bands rows for page {slug!r}",
    )
    positions = sorted(int(band["position"]) for band in bands)
    assert positions == [1, 2, 3], (
        f"band positions for page {slug!r} are {positions}, expected a gapless "
        f"run from one upward"
    )


def test_second_published_route_is_refused(author_client, db):
    route = f"/{unique_token('shared-route')}"
    first = unique_token("route-one")
    second = unique_token("route-two")
    create_draft_page(author_client, first, route)
    author_client.patch(f"/pages/{first}", json={"state": STATE_PUBLISHED})
    wait_for(
        lambda: (db.page_by_slug(first) or {}).get("state") == STATE_PUBLISHED,
        f"page {first!r} reaching state published",
    )
    create_draft_page(author_client, second, route)
    response = author_client.patch(f"/pages/{second}", json={"state": STATE_PUBLISHED})
    assert response.status_code in (400, 409, 422), (
        f"publishing a second page onto route {route!r} returned "
        f"{response.status_code}, expected a client error: {response.text[:400]}"
    )
    assert (db.page_by_slug(second) or {}).get("state") == STATE_DRAFT, (
        f"the refused publish still moved page {second!r} out of state draft"
    )


def test_page_list_hides_drafts_from_anonymous(anon_client):
    response = anon_client.get("/pages")
    assert response.status_code == 200, (
        f"GET /api/pages without a session returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    listed = response.json()
    assert isinstance(listed, list), (
        f"GET /api/pages returned {type(listed).__name__}, expected a top-level array"
    )
    states = {str(entry.get("state")) for entry in listed}
    assert states <= {STATE_PUBLISHED}, (
        f"GET /api/pages without a session exposed page states {sorted(states)}, "
        f"expected only {STATE_PUBLISHED!r}"
    )


def test_list_endpoint_returns_a_top_level_array(author_client):
    response = author_client.get("/pages")
    assert response.status_code == 200, (
        f"GET /api/pages with an author session returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    assert isinstance(response.json(), list), (
        f"GET /api/pages returned a {type(response.json()).__name__}; a list "
        f"endpoint returns a top-level JSON array"
    )


def test_invalid_body_is_refused_as_a_client_error(author_client):
    response = author_client.post("/pages", json={"slug": ""})
    assert 400 <= response.status_code < 500, (
        f"POST /api/pages with an empty slug returned {response.status_code}; an "
        f"invalid call is a client error, never a 5xx and never a silent success"
    )


def test_unknown_address_answers_not_found():
    response = httpx.get(page_url("/this-address-was-never-published"), timeout=TIMEOUT)
    assert response.status_code == 404, (
        f"an unknown address returned {response.status_code}, expected 404: "
        f"{response.text[:200]}"
    )
    assert "could not be found" in response.text.lower(), (
        "the not-found page carries none of the pinned copy: "
        f"{response.text[:400]}"
    )


def test_fifteen_public_routes_answer_without_a_session():
    unreachable = []
    for route in PUBLIC_ROUTES:
        response = httpx.get(page_url(route), timeout=TIMEOUT)
        if response.status_code != 200:
            unreachable.append((route, response.status_code))
    assert not unreachable, (
        f"{len(unreachable)} of {len(PUBLIC_ROUTES)} public routes did not answer "
        f"200 without a session: {unreachable}"
    )


def test_response_carries_a_request_id_header(anon_client):
    response = anon_client.get("/health")
    candidates = [
        name for name in response.headers
        if "request" in name.lower() and "id" in name.lower()
    ]
    assert candidates, (
        f"GET /api/health carried no request-id header; headers were "
        f"{sorted(response.headers.keys())}"
    )
    value = response.headers[candidates[0]]
    assert value.strip(), (
        f"the request-id header {candidates[0]!r} is empty on GET /api/health"
    )


def test_signup_creates_one_booking_page_row(db):
    email = probe_email()
    username = unique_token("visitor")
    outcome = signup(email, username)
    assert outcome["status"] in (200, 201), (
        f"POST /api/auth/signup returned {outcome['status']}: {outcome['body'][:400]}"
    )
    user = wait_for(lambda: db.user_by_email(email), f"user row for {email}")
    booking = wait_for(
        lambda: db.booking_page_for_user(user["id"]),
        f"booking_pages row for {email}",
    )
    assert str(booking["username"]).lower() == username.lower(), (
        f"the booking page for {email} carries username {booking['username']!r}, "
        f"expected {username!r}"
    )
    assert db.count_booking_pages(user_id=user["id"]) == 1, (
        f"{email} holds {db.count_booking_pages(user_id=user['id'])} booking pages, "
        f"expected exactly one"
    )
    landed = httpx.get(page_url(f"/{username}"), timeout=TIMEOUT)
    assert landed.status_code == 200, (
        f"the new booking page at /{username} answered {landed.status_code}"
    )


def test_username_uniqueness_is_case_folded(anon_client):
    username = unique_token("Visitor")
    first = signup(probe_email(), username)
    assert first["status"] in (200, 201), (
        f"the first signup for {username!r} returned {first['status']}: "
        f"{first['body'][:400]}"
    )
    response = anon_client.post(
        "/auth/signup",
        json={
            "email": probe_email(),
            "password": "verifier-pw-1",
            "username": username.upper(),
            "display_name": "Verifier Visitor",
        },
    )
    assert response.status_code in (400, 409, 422), (
        f"a signup reusing {username.upper()!r} returned {response.status_code}; "
        f"a username is compared case-folded: {response.text[:400]}"
    )


def test_reader_publish_is_denied_and_row_unchanged(author_client, reader_client, db):
    slug = unique_token("guarded-page")
    create_draft_page(author_client, slug, f"/{slug}")
    response = reader_client.patch(f"/pages/{slug}", json={"state": STATE_PUBLISHED})
    assert response.status_code in (401, 403), (
        f"a reader session publishing {slug!r} returned {response.status_code}, "
        f"expected 401 or 403: {response.text[:400]}"
    )
    row = db.page_by_slug(slug)
    assert row["state"] == STATE_DRAFT, (
        f"the denied publish still moved {slug!r} to state {row['state']!r}"
    )


def test_reader_cannot_read_page_view_totals(reader_client):
    response = reader_client.get("/page-views")
    assert response.status_code in (401, 403), (
        f"a reader session reading the page-view totals returned "
        f"{response.status_code}, expected 401 or 403: {response.text[:400]}"
    )


def test_studio_routes_refuse_an_anonymous_caller():
    response = httpx.get(page_url(STUDIO_ROUTE), timeout=TIMEOUT, follow_redirects=False)
    assert response.status_code in (302, 303, 307, 401, 403), (
        f"{STUDIO_ROUTE} answered {response.status_code} without a session, "
        f"expected a redirect to {LOGIN_ROUTE} or a refusal"
    )
    if response.status_code in (302, 303, 307):
        assert LOGIN_ROUTE in response.headers.get("location", ""), (
            f"{STUDIO_ROUTE} redirected to "
            f"{response.headers.get('location')!r}, expected {LOGIN_ROUTE}"
        )


def test_reader_session_is_refused_at_the_studio(reader_client):
    response = reader_client.get("/pages?state=draft")
    assert response.status_code in (200, 401, 403), (
        f"a reader reading drafts returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    if response.status_code == 200:
        states = {str(entry.get("state")) for entry in response.json()}
        assert states <= {STATE_PUBLISHED}, (
            f"a reader asking for drafts received states {sorted(states)}"
        )


def test_draft_page_is_absent_by_slug_without_author_session(author_client, anon_client, db):
    slug = unique_token("hidden-page")
    create_draft_page(author_client, slug, f"/{slug}")
    wait_for(lambda: db.page_by_slug(slug), f"pages row for {slug!r}")
    response = anon_client.get(f"/pages/{slug}")
    assert response.status_code in (401, 403, 404), (
        f"GET /api/pages/{slug} without a session returned {response.status_code}; "
        f"a draft page is absent to everyone except an author: {response.text[:400]}"
    )
    seen = author_client.get(f"/pages/{slug}")
    assert seen.status_code == 200, (
        f"GET /api/pages/{slug} with an author session returned {seen.status_code}"
    )


def test_password_is_not_stored_in_readable_form(db):
    row = db.user_by_email(AUTHOR_EMAIL)
    assert row, f"the seeded account {AUTHOR_EMAIL} has no users row"
    assert CORPUS_PASSWORD not in str(row.get("password_hash", "")), (
        f"the stored credential for {AUTHOR_EMAIL} contains the literal password"
    )


def test_seed_is_present_and_survives_a_reload(db):
    published = db.pages_in_state(STATE_PUBLISHED)
    assert len(published) >= 15, (
        f"the seed holds {len(published)} published pages, expected at least 15"
    )
    again = db.pages_in_state(STATE_PUBLISHED)
    assert len(again) == len(published), (
        f"a second read returned {len(again)} published pages, the first returned "
        f"{len(published)}; seeding is idempotent"
    )
    author = db.user_by_email(AUTHOR_EMAIL)
    assert db.count_users(AUTHOR_EMAIL) == 1, (
        f"{AUTHOR_EMAIL} has {db.count_users(AUTHOR_EMAIL)} rows, expected one; "
        f"restarting the app duplicates no row. Row: {author}"
    )


def test_seeded_draft_page_record_carries_one_media_object(db):
    row = db.page_by_route(DRAFT_ROUTE)
    assert row, f"no pages row is seeded at route {DRAFT_ROUTE!r}"
    assert row["state"] == STATE_DRAFT, (
        f"the page at {DRAFT_ROUTE!r} is in state {row['state']!r}, expected draft"
    )
    objects = db.media_for_page(row["id"])
    assert len(objects) == 1, (
        f"the seeded draft page carries {len(objects)} media rows, expected one"
    )
    assert str(objects[0].get("alt_text") or "").strip(), (
        f"the seeded draft media row carries empty alternative text: {objects[0]}"
    )


def test_page_view_rows_are_recorded_per_route(db):
    route = "/teams"
    before = db.count_page_views(route)
    httpx.get(page_url(route), timeout=TIMEOUT)
    after = wait_for(
        lambda: db.count_page_views(route) > before and db.count_page_views(route),
        f"a page_views row for {route!r}",
    )
    assert after > before, (
        f"page_views for {route!r} went from {before} to {after}; each view is recorded"
    )


def test_page_view_log_only_ever_grows(db, author_client):
    route = "/faq"
    before = db.count_page_views(route)
    httpx.get(page_url(route), timeout=TIMEOUT)
    wait_for(lambda: db.count_page_views(route) > before, f"a view row for {route!r}")
    middle = db.count_page_views(route)
    removal = author_client.delete("/page-views")
    assert removal.status_code in (401, 403, 404, 405), (
        f"DELETE /api/page-views returned {removal.status_code}; the log is only "
        f"ever added to"
    )
    assert db.count_page_views(route) >= middle, (
        f"page_views for {route!r} fell from {middle} to "
        f"{db.count_page_views(route)}"
    )


def test_author_reads_the_per_route_view_totals(author_client):
    response = author_client.get("/page-views")
    assert response.status_code == 200, (
        f"GET /api/page-views with an author session returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    totals = response.json()
    assert isinstance(totals, list), (
        f"GET /api/page-views returned {type(totals).__name__}, expected an array"
    )
    routes = {str(entry.get("route")) for entry in totals}
    assert "/" in routes, (
        f"the page-view totals name no home route; routes were {sorted(routes)}"
    )
    for entry in totals:
        assert "views" in entry, (
            f"a page-view total carries no views field: {entry}"
        )


def test_concurrent_publish_to_one_route_leaves_one_winner(author_token, db):
    route = f"/{unique_token('contested-route')}"
    slugs = [unique_token("racer-one"), unique_token("racer-two")]
    with client(author_token) as author:
        for slug in slugs:
            create_draft_page(author, slug, route)
    outcomes = []
    with httpx.Client(base_url=api_base(), timeout=TIMEOUT,
                      headers={"Authorization": f"Bearer {author_token}"}) as racer:
        requests = [
            racer.build_request("PATCH", f"/pages/{slug}",
                                json={"state": STATE_PUBLISHED})
            for slug in slugs
        ]
        for request in requests:
            outcomes.append(racer.send(request))
    accepted = [r for r in outcomes if r.status_code in (200, 202)]
    published = [
        slug for slug in slugs
        if (db.page_by_slug(slug) or {}).get("state") == STATE_PUBLISHED
    ]
    assert len(published) == 1, (
        f"{len(published)} pages reached state published on route {route!r}, "
        f"expected exactly one. Responses were "
        f"{[(r.status_code, r.text[:80]) for r in outcomes]}"
    )
    assert len(accepted) <= 1, (
        f"{len(accepted)} of the racing publishes were accepted on route {route!r}"
    )


def test_failed_publish_leaves_no_orphaned_media_row(author_client, db):
    slug = unique_token("orphan-page")
    created = create_draft_page(author_client, slug, f"/{slug}")
    page_id = created.get("id") or (db.page_by_slug(slug) or {}).get("id")
    before = db.count_media(page_id=page_id)
    response = author_client.patch(f"/pages/{slug}", json={"state": "retired"})
    assert 400 <= response.status_code < 500, (
        f"PATCH /api/pages/{slug} to an unknown state returned "
        f"{response.status_code}, expected a client error"
    )
    assert db.count_media(page_id=page_id) == before, (
        f"a refused publish changed the media row count for {slug!r} from "
        f"{before} to {db.count_media(page_id=page_id)}"
    )
    assert (db.page_by_slug(slug) or {}).get("state") == STATE_DRAFT, (
        f"a refused publish left {slug!r} in state "
        f"{(db.page_by_slug(slug) or {}).get('state')!r}"
    )


def test_upload_lands_in_the_bucket_under_the_key_scheme(author_client, db, store):
    slug = unique_token("upload-page")
    created = create_draft_page(author_client, slug, f"/{slug}")
    page_id = created.get("id") or (db.page_by_slug(slug) or {}).get("id")
    payload = png_bytes(slug)
    response = upload_media(author_client, page_id, payload)
    assert response.status_code in (200, 201), (
        f"POST /api/media for page {slug!r} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    object_key = response.json().get("object_key")
    assert object_key, f"POST /api/media returned no object_key: {response.text[:400]}"
    digest = sha256_hex(payload)
    assert object_key.startswith(f"{OBJECT_KEY_PREFIX}{page_id}/"), (
        f"object key {object_key!r} does not open with the pinned scheme "
        f"{OBJECT_KEY_PREFIX}{{page_id}}/"
    )
    assert digest in object_key, (
        f"object key {object_key!r} does not carry the sha256 of the bytes {digest}"
    )
    assert wait_for(lambda: store.exists(object_key), f"object {object_key!r} in the bucket"), (
        f"object {object_key!r} is absent from the bucket, so the bytes never "
        f"reached the store"
    )


def test_duplicate_upload_creates_one_object_row(author_client, db, store):
    slug = unique_token("dedupe-page")
    created = create_draft_page(author_client, slug, f"/{slug}")
    page_id = created.get("id") or (db.page_by_slug(slug) or {}).get("id")
    payload = png_bytes(f"{slug}-dedupe")
    first = upload_media(author_client, page_id, payload)
    assert first.status_code in (200, 201), (
        f"the first upload for {slug!r} returned {first.status_code}: "
        f"{first.text[:400]}"
    )
    wait_for(lambda: db.count_media(page_id=page_id) >= 1, f"a media row for {slug!r}")
    after_first = db.count_media(page_id=page_id)
    second = upload_media(author_client, page_id, payload)
    assert second.status_code in (200, 201, 409), (
        f"the repeated upload for {slug!r} returned {second.status_code}: "
        f"{second.text[:400]}"
    )
    assert db.count_media(page_id=page_id) == after_first, (
        f"the same bytes uploaded twice to page {slug!r} produced "
        f"{db.count_media(page_id=page_id)} media rows, expected {after_first}"
    )


def test_media_row_holds_the_object_key_only(author_client, db):
    slug = unique_token("keyonly-page")
    created = create_draft_page(author_client, slug, f"/{slug}")
    page_id = created.get("id") or (db.page_by_slug(slug) or {}).get("id")
    payload = png_bytes(f"{slug}-keyonly")
    response = upload_media(author_client, page_id, payload)
    object_key = response.json().get("object_key")
    row = wait_for(lambda: db.media_by_key(object_key), f"media row for {object_key!r}")
    serialised = "".join(str(value) for value in row.values())
    assert "data:image" not in serialised, (
        f"the media row for {object_key!r} carries an inline image payload: {row}"
    )
    assert len(serialised) < 4096, (
        f"the media row for {object_key!r} is {len(serialised)} characters wide, "
        f"which is bytes rather than metadata: {str(row)[:400]}"
    )
    assert row["object_key"] == object_key, (
        f"the media row records object_key {row['object_key']!r}, the interface "
        f"returned {object_key!r}"
    )


def test_draft_media_object_is_refused_without_author_session(author_client, anon_client, db):
    slug = unique_token("private-page")
    created = create_draft_page(author_client, slug, f"/{slug}")
    page_id = created.get("id") or (db.page_by_slug(slug) or {}).get("id")
    payload = png_bytes(f"{slug}-private")
    response = upload_media(author_client, page_id, payload)
    object_key = response.json().get("object_key")
    assert object_key, f"POST /api/media returned no object_key: {response.text[:400]}"
    refused = anon_client.get(f"/media/{object_key}")
    assert refused.status_code in (401, 403, 404), (
        f"GET /api/media/{object_key} without a session returned "
        f"{refused.status_code}; media on a draft page is unreadable to everyone "
        f"except an author: {refused.text[:200]}"
    )
    allowed = author_client.get(f"/media/{object_key}")
    assert allowed.status_code == 200, (
        f"GET /api/media/{object_key} with an author session returned "
        f"{allowed.status_code}"
    )


def test_published_media_file_streams_to_anyone(author_client, anon_client, db):
    slug = unique_token("public-page")
    route = f"/{slug}"
    created = create_draft_page(author_client, slug, route)
    page_id = created.get("id") or (db.page_by_slug(slug) or {}).get("id")
    payload = png_bytes(f"{slug}-public")
    object_key = upload_media(author_client, page_id, payload).json().get("object_key")
    author_client.patch(f"/pages/{slug}", json={"state": STATE_PUBLISHED})
    wait_for(
        lambda: (db.page_by_slug(slug) or {}).get("state") == STATE_PUBLISHED,
        f"page {slug!r} reaching state published",
    )
    served = wait_for(
        lambda: anon_client.get(f"/media/{object_key}") if
        anon_client.get(f"/media/{object_key}").status_code == 200 else None,
        f"media {object_key!r} becoming readable once the page is published",
    )
    assert served.content, (
        f"GET /api/media/{object_key} returned an empty body once published"
    )
    opened = httpx.get(page_url(route), timeout=TIMEOUT)
    assert opened.status_code == 200, (
        f"the published route {route!r} answered {opened.status_code}"
    )


def test_upload_without_alternative_text_is_refused(author_client, db):
    slug = unique_token("noalt-page")
    created = create_draft_page(author_client, slug, f"/{slug}")
    page_id = created.get("id") or (db.page_by_slug(slug) or {}).get("id")
    before = db.count_media(page_id=page_id)
    response = upload_media(author_client, page_id, png_bytes(f"{slug}-noalt"), alt_text="")
    assert 400 <= response.status_code < 500, (
        f"an upload carrying empty alternative text returned "
        f"{response.status_code}, expected a client error: {response.text[:400]}"
    )
    assert db.count_media(page_id=page_id) == before, (
        f"the refused upload still created a media row for {slug!r}"
    )


def test_user_readme_records_the_seeded_accounts():
    path = os.path.join(APP_ROOT, "USER_README.md")
    assert os.path.isfile(path), (
        f"{path} is absent, so the seeded credentials are undocumented"
    )
    with open(path, encoding="utf-8", errors="replace") as handle:
        body = handle.read()
    assert AUTHOR_EMAIL in body, f"{path} does not name {AUTHOR_EMAIL}"
    assert READER_EMAIL in body, f"{path} does not name {READER_EMAIL}"
    assert CORPUS_PASSWORD in body, f"{path} does not carry the seeded password"


def test_reserved_browser_screenshots_directory_exists():
    path = os.path.join(APP_ROOT, ".browser_screenshots")
    assert os.path.isdir(path), f"the reserved directory {path} is absent"


def test_reserved_downloads_directory_exists():
    path = os.path.join(APP_ROOT, ".downloads")
    assert os.path.isdir(path), f"the reserved directory {path} is absent"


def test_draft_route_renders_not_found_for_anonymous(page):
    response = page.goto(page_url(DRAFT_ROUTE))
    assert response is not None, f"{DRAFT_ROUTE} produced no response"
    assert response.status == 404, (
        f"{DRAFT_ROUTE} answered {response.status} to an anonymous visitor, "
        f"expected 404 because the page is in state draft"
    )
    assert "could not be found" in page.content().lower(), (
        f"{DRAFT_ROUTE} answered 404 without rendering the not-found copy"
    )


def test_wizard_step_data_survives_a_return_visit(page):
    page.goto(page_url("/studio/new/details"))
    assert LOGIN_ROUTE in page.url or "sign in" in page.content().lower(), (
        f"/studio/new/details opened at {page.url} without a session, expected "
        f"the sign-in surface"
    )


def test_internal_links_on_public_routes_resolve(page):
    broken = []
    for route in READ_ONLY_PUBLIC_ROUTES:
        page.goto(page_url(route))
        hrefs = page.eval_on_selector_all(
            "a[href]", "nodes => nodes.map(n => n.getAttribute('href'))"
        )
        internal = sorted({h for h in hrefs if h and h.startswith("/") and not h.startswith("//")})
        for href in internal:
            target = href.split("#")[0].split("?")[0] or "/"
            answer = httpx.get(page_url(target), timeout=TIMEOUT)
            if answer.status_code >= 400:
                broken.append((route, href, answer.status_code))
    assert not broken, (
        f"{len(broken)} internal link(s) on the public routes do not resolve: "
        f"{broken[:10]}"
    )


def test_every_public_route_declares_a_unique_description(page):
    seen = {}
    missing = []
    for route in READ_ONLY_PUBLIC_ROUTES:
        page.goto(page_url(route))
        title = page.title()
        description = page.eval_on_selector_all(
            "meta[name='description']", "nodes => nodes.map(n => n.content)"
        )
        text = description[0].strip() if description else ""
        if not title.strip() or not text:
            missing.append((route, title, text))
        seen.setdefault((title.strip(), text), []).append(route)
    assert not missing, (
        f"{len(missing)} public route(s) declare no title or no description: {missing}"
    )
    shared = {key: routes for key, routes in seen.items() if len(routes) > 1}
    assert not shared, (
        f"public routes share a title and description: {list(shared.values())}"
    )


def test_every_public_route_declares_a_preview_image_that_resolves(page):
    findings = []
    for route in READ_ONLY_PUBLIC_ROUTES:
        page.goto(page_url(route))
        previews = page.eval_on_selector_all(
            "meta[property='og:image'], meta[name='og:image'], "
            "meta[property='twitter:image'], meta[name='twitter:image']",
            "nodes => nodes.map(n => n.content)",
        )
        titles = page.eval_on_selector_all(
            "meta[property='og:title'], meta[name='og:title']",
            "nodes => nodes.map(n => n.content)",
        )
        if not previews or not titles:
            findings.append((route, "declares no preview title or preview image"))
            continue
        target = previews[0]
        if target.startswith("/"):
            target = page_url(target)
        answer = httpx.get(target, timeout=TIMEOUT)
        if answer.status_code != 200:
            findings.append((route, f"preview image answered {answer.status_code}"))
    assert not findings, (
        f"{len(findings)} public route(s) carry a broken social preview: {findings}"
    )


def test_every_content_image_carries_alternative_text(page):
    findings = []
    for route in READ_ONLY_PUBLIC_ROUTES:
        page.goto(page_url(route))
        undescribed = page.eval_on_selector_all(
            "img",
            "nodes => nodes.filter(n => n.getAttribute('alt') === null && "
            "n.getAttribute('role') !== 'presentation' && "
            "n.getAttribute('aria-hidden') !== 'true').map(n => n.getAttribute('src'))",
        )
        if undescribed:
            findings.append((route, undescribed[:5]))
    assert not findings, (
        f"{len(findings)} public route(s) carry a content image with no "
        f"alternative text: {findings}"
    )


def test_narrow_viewport_has_no_sideways_overflow(ui_page):
    findings = []
    for route in READ_ONLY_PUBLIC_ROUTES:
        ui_page.goto(page_url(route))
        widths = ui_page.evaluate(
            "() => [document.documentElement.scrollWidth, window.innerWidth]"
        )
        if widths[0] > widths[1] + 1:
            findings.append((route, widths[0], widths[1]))
    assert not findings, (
        f"{len(findings)} public route(s) overflow sideways at a narrow viewport: "
        f"{findings}"
    )


def test_no_third_party_script_blocks_the_first_paint(page):
    findings = []
    for route in READ_ONLY_PUBLIC_ROUTES[:5]:
        page.goto(page_url(route))
        sources = page.eval_on_selector_all(
            "script[src]", "nodes => nodes.map(n => n.src)"
        )
        foreign = [
            src for src in sources
            if not src.startswith(app_url()) and "fonts.googleapis.com" not in src
            and "fonts.gstatic.com" not in src
        ]
        if foreign:
            findings.append((route, foreign[:5]))
    assert not findings, (
        f"{len(findings)} public route(s) load a script from a third host: {findings}"
    )


def test_booking_page_for_the_seeded_author_is_public():
    response = httpx.get(page_url(BOOKING_PAGE_ROUTE), timeout=TIMEOUT)
    assert response.status_code == 200, (
        f"the seeded booking page at {BOOKING_PAGE_ROUTE} answered "
        f"{response.status_code}"
    )
    assert "editor" in response.text.lower(), (
        f"the booking page at {BOOKING_PAGE_ROUTE} does not name its username"
    )
