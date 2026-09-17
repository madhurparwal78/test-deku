from __future__ import annotations

import hashlib
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor

import httpx

import appclient
from conftest import (
    ADMIN_EMAIL,
    API,
    APP_URL,
    BOARD_VIEW,
    CLOSED_TEAMSPACE,
    CORPUS_PASSWORD,
    CREATED_BY_PROPERTY,
    DATABASE_NAME,
    GUEST_EMAIL,
    GROUP_NAME,
    HANDBOOK,
    HANDBOOK_SLUG,
    HIDDEN_PROPERTY,
    KEY_SCHEME_PREFIX,
    MEMBER2_EMAIL,
    MEMBER_EMAIL,
    ONBOARDING,
    OPEN_TEAMSPACE,
    PRIVATE_TEAMSPACE,
    RELEASE_NOTES,
    RELEASE_NOTES_SLUG,
    SECURITY_HEADER_NAMES,
    STATUS_OPTIONS,
    STATUS_PROPERTY,
    TABLE_VIEW,
    TITLE_PROPERTY,
    UNIQUE_ID_PREFIX,
    anon,
    code_of,
    describe,
    page_named,
    probe_id,
    settle,
    teamspace_named,
    token_for,
)

DENIED = (401, 403, 404)


def test_health_route_returns_ok(stranger):
    response = stranger.get("/health")
    assert response.status_code == 200, describe(response)


def test_seeded_accounts_sign_in_with_the_corpus_password():
    for email in (ADMIN_EMAIL, MEMBER_EMAIL, MEMBER2_EMAIL, GUEST_EMAIL):
        token = appclient.login(email, CORPUS_PASSWORD)
        assert token, f"login for {email} returned an empty access_token"


def test_identify_response_is_identical_for_known_and_unknown_address(stranger):
    unknown = f"probe-{probe_id()}@example.com"
    known = stranger.post("/auth/identify", json={"email": MEMBER_EMAIL})
    missing = stranger.post("/auth/identify", json={"email": unknown})
    assert known.status_code == missing.status_code, (
        f"identify status differs between a known and an unknown address: "
        f"{describe(known)} versus {describe(missing)}"
    )
    assert known.text == missing.text, (
        f"identify body differs between a known and an unknown address: "
        f"{known.text[:200]!r} versus {missing.text[:200]!r}"
    )


def test_logout_refuses_the_previous_bearer_token():
    token = token_for(MEMBER2_EMAIL)
    with appclient.client(token) as session:
        before = session.get("/me")
        assert before.status_code == 200, describe(before)
        ended = session.post("/auth/logout")
        assert ended.status_code in (200, 204), describe(ended)
        after = session.get("/me")
    assert after.status_code in DENIED, (
        f"a bearer token kept working after logout: {describe(after)}"
    )


def test_block_insert_edit_and_move_are_persisted_as_rows(member, handbook):
    page_id = handbook["page_id"]
    marker = f"probe-{probe_id()}"
    created = member.post(
        f"/pages/{page_id}/blocks",
        json={"type": "paragraph", "text": marker, "position": 0, "depth": 0},
    )
    assert created.status_code in (200, 201), describe(created)
    block = created.json()
    block_id = block.get("id")
    assert block_id, f"block create returned no id: {describe(created)}"

    edited = member.patch(
        f"/blocks/{block_id}",
        json={"text": marker + "-edited", "version": block.get("version")},
    )
    assert edited.status_code == 200, describe(edited)

    moved = member.post(f"/blocks/{block_id}/move", json={"position": 1, "depth": 0})
    assert moved.status_code == 200, describe(moved)

    listed = member.get(f"/pages/{page_id}/blocks")
    assert listed.status_code == 200, describe(listed)
    rows = listed.json()
    assert isinstance(rows, list), describe(listed)
    found = [row for row in rows if row.get("id") == block_id]
    assert found, f"the inserted block is absent from the page after a move: {describe(listed)}"
    assert found[0].get("text") == marker + "-edited", (
        f"the stored block text is not the edited text: {found[0]!r}"
    )
    assert found[0].get("position") == 1, (
        f"the stored block position is not the moved position: {found[0]!r}"
    )


def test_rich_text_annotations_survive_a_reload_as_stored(member, handbook):
    page_id = handbook["page_id"]
    marker = f"probe-{probe_id()}"
    created = member.post(
        f"/pages/{page_id}/blocks",
        json={
            "type": "paragraph",
            "position": 0,
            "depth": 0,
            "text": marker,
            "runs": [{"text": marker, "annotations": ["bold", "code"]}],
        },
    )
    assert created.status_code in (200, 201), describe(created)
    block_id = created.json().get("id")

    listed = member.get(f"/pages/{page_id}/blocks")
    assert listed.status_code == 200, describe(listed)
    rows = [row for row in listed.json() if row.get("id") == block_id]
    assert rows, f"the annotated block is absent after a reload: {describe(listed)}"
    runs = rows[0].get("runs")
    assert runs, f"the stored block carries no runs: {rows[0]!r}"
    annotations = [name for run in runs for name in (run.get("annotations") or [])]
    assert "bold" in annotations, f"the bold annotation was lost: {rows[0]!r}"
    assert "code" in annotations, f"the code annotation was lost: {rows[0]!r}"


def test_publish_reports_the_public_page_count_and_serves_the_slug(member, handbook, site):
    page_id = handbook["page_id"]
    published = member.post(
        f"/pages/{page_id}/publish",
        json={"slug": HANDBOOK_SLUG, "include_subtree": False},
    )
    assert published.status_code in (200, 201), describe(published)
    body = published.json()
    assert body.get("slug") == HANDBOOK_SLUG, (
        f"publish returned a different slug: {describe(published)}"
    )
    assert isinstance(body.get("pages_published"), int), (
        f"publish did not report how many pages became public: {describe(published)}"
    )

    rendered = settle(lambda: _ok(site.get(f"/site/{HANDBOOK_SLUG}")))
    assert rendered is not None, (
        f"the published page is not readable at /site/{HANDBOOK_SLUG} after publishing"
    )
    assert HANDBOOK in rendered.text, (
        f"the published page does not carry its title: {rendered.text[:400]!r}"
    )


def test_published_route_renders_a_title_and_a_description(site):
    response = site.get(f"/site/{RELEASE_NOTES_SLUG}")
    assert response.status_code == 200, describe(response)
    markup = response.text
    assert re.search(r"<title[^>]*>.+?</title>", markup, re.DOTALL | re.IGNORECASE), (
        f"the published route carries no title element: {markup[:400]!r}"
    )
    assert re.search(r'name=["\']description["\']', markup, re.IGNORECASE), (
        f"the published route declares no description: {markup[:400]!r}"
    )


def test_unpublish_makes_the_public_address_gone(member, site):
    page_id = _page_id(member, RELEASE_NOTES)
    before = site.get(f"/site/{RELEASE_NOTES_SLUG}")
    assert before.status_code == 200, describe(before)

    removed = member.delete(f"/pages/{page_id}/publish")
    assert removed.status_code in (200, 204), describe(removed)

    after = settle(lambda: _gone(site.get(f"/site/{RELEASE_NOTES_SLUG}")))
    assert after is not None, (
        f"the public address still serves content after unpublishing "
        f"{RELEASE_NOTES!r}"
    )
    assert 300 > after.status_code or after.status_code >= 400, (
        f"unpublishing produced a redirect rather than a gone answer: {describe(after)}"
    )

    restored = member.post(
        f"/pages/{page_id}/publish",
        json={"slug": RELEASE_NOTES_SLUG, "include_subtree": False},
    )
    assert restored.status_code in (200, 201), describe(restored)


def test_anonymous_request_for_an_unpublished_seeded_page_is_not_found(site):
    for slug in ("onboarding-checklist", "compensation-bands", "board-minutes"):
        response = site.get(f"/site/{slug}")
        assert response.status_code >= 400, (
            f"an unpublished page is served anonymously at /site/{slug}: {describe(response)}"
        )


def test_board_view_groups_rows_by_status_with_counts(member):
    database, views = _database(member)
    board = _view_named(views, BOARD_VIEW)
    assert board is not None, f"the seeded board view {BOARD_VIEW!r} is absent"
    assert board.get("group_by") == STATUS_PROPERTY, (
        f"the board view does not group by {STATUS_PROPERTY!r}: {board!r}"
    )
    rows = _rows(member, database["id"], board["id"])
    seen = {row.get(STATUS_PROPERTY) for row in rows}
    for option in STATUS_OPTIONS:
        assert option in seen, (
            f"the seeded rows do not cover the status option {option!r}: {sorted(seen)!r}"
        )


def test_nested_filter_tree_round_trips_through_storage(member):
    database, views = _database(member)
    table = _view_named(views, TABLE_VIEW)
    assert table is not None, f"the seeded table view {TABLE_VIEW!r} is absent"
    tree = {
        "operator": "or",
        "conditions": [
            {"property": STATUS_PROPERTY, "op": "is", "value": "In progress"},
            {
                "operator": "and",
                "conditions": [
                    {"property": STATUS_PROPERTY, "op": "is", "value": "In review"},
                    {"property": TITLE_PROPERTY, "op": "is_not_empty"},
                ],
            },
        ],
    }
    saved = member.patch(f"/views/{table['id']}", json={"filter": tree})
    assert saved.status_code == 200, describe(saved)

    reread = member.get(f"/databases/{database['id']}")
    assert reread.status_code == 200, describe(reread)
    back = _view_named(reread.json().get("views") or [], TABLE_VIEW)
    assert back is not None, f"the table view vanished after a filter save: {describe(reread)}"
    assert back.get("filter") == tree, (
        f"the nested filter tree did not round trip: stored {back.get('filter')!r}"
    )

    restored = member.patch(f"/views/{table['id']}", json={"filter": table.get("filter")})
    assert restored.status_code == 200, describe(restored)


def test_search_matches_page_title_and_block_text(member):
    by_title = member.get("/search", params={"q": "Onboarding"})
    assert by_title.status_code == 200, describe(by_title)
    titles = [row.get("title") for row in by_title.json()]
    assert ONBOARDING in titles, (
        f"search on a page title did not return {ONBOARDING!r}: {titles!r}"
    )

    page_id = _page_id(member, HANDBOOK)
    marker = f"probe-{probe_id()}"
    created = member.post(
        f"/pages/{page_id}/blocks",
        json={"type": "paragraph", "text": marker, "position": 0, "depth": 0},
    )
    assert created.status_code in (200, 201), describe(created)
    hit = settle(lambda: _has_page(member.get("/search", params={"q": marker}), HANDBOOK))
    assert hit, f"search on block text did not return the page carrying {marker!r}"


def test_not_found_page_is_the_products_own_page(site):
    response = site.get(f"/no-such-address-{probe_id()}")
    assert response.status_code == 404, describe(response)
    body = response.text
    assert "Meridian" in body, (
        f"the not-found page does not carry the product name: {body[:400]!r}"
    )
    assert re.search(r"href=[\"']/w[\"']?", body), (
        f"the not-found page offers no link back to the workspace home: {body[:400]!r}"
    )


def test_every_internal_link_on_a_served_route_resolves(site):
    root = site.get("/")
    assert root.status_code == 200, describe(root)
    links = {
        href
        for href in re.findall(r'href="(/[^"#?]*)"', root.text)
        if not href.startswith("//")
    }
    broken = []
    for href in sorted(links):
        probe = site.get(href)
        if probe.status_code == 404:
            broken.append((href, probe.status_code))
    assert not broken, f"internal links resolve to nothing: {broken!r}"


def test_unique_id_counter_never_reissues_a_stored_key(member):
    database, views = _database(member)
    table = _view_named(views, TABLE_VIEW)
    rows = _rows(member, database["id"], table["id"])
    keys = [str(row.get("unique_id") or "") for row in rows]
    issued = [key for key in keys if key.startswith(UNIQUE_ID_PREFIX + "-")]
    assert issued, f"no row carries a {UNIQUE_ID_PREFIX} key: {keys!r}"
    assert len(set(issued)) == len(issued), f"a unique-id key was reissued: {issued!r}"


def test_page_row_persisted_matches_what_the_page_endpoint_returned(member, backend, handbook):
    page_id = handbook["page_id"]
    served = member.get(f"/pages/{page_id}")
    assert served.status_code == 200, describe(served)
    shown = served.json()
    stored = backend.rows("pages", limit=500)
    matching = [row for row in stored if str(row.get("id")) == str(page_id)]
    assert matching, f"page {page_id} is served but has no row in the pages table"
    assert matching[0].get("title") == shown.get("title"), (
        f"the stored title {matching[0].get('title')!r} is not the served title "
        f"{shown.get('title')!r}"
    )


def test_seeded_rows_are_stored_exactly_once(backend):
    principals = backend.rows("principals", limit=500)
    emails = [row.get("email") for row in principals]
    for email in (ADMIN_EMAIL, MEMBER_EMAIL, MEMBER2_EMAIL, GUEST_EMAIL):
        assert emails.count(email) == 1, (
            f"seeded principal {email} appears {emails.count(email)} times, so seeding "
            f"is not idempotent"
        )
    teamspaces = backend.rows("teamspaces", limit=500)
    names = [row.get("name") for row in teamspaces]
    for name in (OPEN_TEAMSPACE, CLOSED_TEAMSPACE, PRIVATE_TEAMSPACE):
        assert names.count(name) == 1, (
            f"seeded teamspace {name!r} appears {names.count(name)} times"
        )


def test_concurrent_block_writes_from_one_version_produce_one_winner(member, handbook):
    page_id = handbook["page_id"]
    marker = f"probe-{probe_id()}"
    created = member.post(
        f"/pages/{page_id}/blocks",
        json={"type": "paragraph", "text": marker, "position": 0, "depth": 0},
    )
    assert created.status_code in (200, 201), describe(created)
    block = created.json()
    block_id = block["id"]
    seen_version = block.get("version")

    def write(suffix: str):
        with appclient.client(_member_token()) as session:
            return session.patch(
                f"/blocks/{block_id}",
                json={"text": f"{marker}-{suffix}", "version": seen_version},
            )

    with ThreadPoolExecutor(max_workers=2) as pool:
        first, second = [job.result() for job in [pool.submit(write, "a"), pool.submit(write, "b")]]

    accepted = [r for r in (first, second) if r.status_code in (200, 201)]
    rejected = [r for r in (first, second) if r.status_code not in (200, 201)]
    assert len(accepted) == 1, (
        f"two writes from one block version both succeeded: "
        f"{describe(first)} and {describe(second)}"
    )
    assert rejected and rejected[0].status_code < 500, (
        f"the losing write was not rejected as a client error: {describe(rejected[0])}"
    )

    final = member.get(f"/pages/{page_id}/blocks")
    stored = [row for row in final.json() if row.get("id") == block_id]
    assert stored, f"the contended block vanished: {describe(final)}"
    assert stored[0].get("text") == accepted[0].json().get("text"), (
        f"the stored text is not the accepted writer value: {stored[0]!r}"
    )


def test_block_version_advances_by_one_on_each_accepted_write(member, handbook):
    page_id = handbook["page_id"]
    marker = f"probe-{probe_id()}"
    created = member.post(
        f"/pages/{page_id}/blocks",
        json={"type": "paragraph", "text": marker, "position": 0, "depth": 0},
    )
    assert created.status_code in (200, 201), describe(created)
    block = created.json()
    start = block.get("version")
    assert isinstance(start, int), f"a block carries no integer version: {block!r}"

    edited = member.patch(
        f"/blocks/{block['id']}", json={"text": marker + "-1", "version": start}
    )
    assert edited.status_code == 200, describe(edited)
    assert edited.json().get("version") == start + 1, (
        f"the block version did not advance by one: {edited.json()!r}"
    )


def test_number_property_is_stored_as_an_exact_decimal_string(member, backend):
    database, views = _database(member)
    table = _view_named(views, TABLE_VIEW)
    rows = _rows(member, database["id"], table["id"])
    assert rows, "the seeded database returned no rows"
    stored = backend.rows("row_values", limit=2000)
    assert stored, "row_values carries no stored property value"
    for row in stored:
        value = row.get("value")
        assert not isinstance(value, float), (
            f"a property value is stored as a floating-point type: {row!r}"
        )


def test_activity_record_rows_are_stored_for_each_mutation(admin, member, handbook, backend):
    page_id = handbook["page_id"]
    before = len(backend.rows("activity", limit=5000))
    marker = f"probe-{probe_id()}"
    created = member.post(
        f"/pages/{page_id}/blocks",
        json={"type": "paragraph", "text": marker, "position": 0, "depth": 0},
    )
    assert created.status_code in (200, 201), describe(created)
    removed = member.delete(f"/blocks/{created.json()['id']}")
    assert removed.status_code in (200, 204), describe(removed)

    after = settle(lambda: len(backend.rows("activity", limit=5000)) > before)
    assert after, "a page mutation wrote no row into the activity record"

    listed = admin.get("/admin/activity")
    assert listed.status_code == 200, describe(listed)
    rows = listed.json()
    assert isinstance(rows, list) and rows, describe(listed)
    for key in ("actor_principal_id", "action", "resource_type", "resource_id", "at"):
        assert key in rows[0], f"an activity row is missing {key!r}: {rows[0]!r}"


def test_repeated_publish_writes_no_second_activity_row(member, backend, site):
    page_id = _page_id(member, RELEASE_NOTES)
    first = member.post(
        f"/pages/{page_id}/publish",
        json={"slug": RELEASE_NOTES_SLUG, "include_subtree": False},
    )
    assert first.status_code in (200, 201), describe(first)
    before = len(backend.rows("activity", limit=5000))
    second = member.post(
        f"/pages/{page_id}/publish",
        json={"slug": RELEASE_NOTES_SLUG, "include_subtree": False},
    )
    assert second.status_code in (200, 201), describe(second)
    assert second.json().get("slug") == first.json().get("slug"), (
        f"a repeated publish returned a different slug: {describe(second)}"
    )
    after = len(backend.rows("activity", limit=5000))
    assert after == before, (
        f"a repeated publish wrote {after - before} extra activity row(s)"
    )


def test_explicit_deny_denies_one_member_and_no_other(member, member2):
    allowed = page_named(member, ONBOARDING)
    assert allowed is not None, (
        f"{ONBOARDING!r} is not readable by {MEMBER_EMAIL}, so the deny grant is too wide"
    )
    served = member.get(f"/pages/{allowed['page_id']}")
    assert served.status_code == 200, describe(served)

    denied = member2.get(f"/pages/{allowed['page_id']}")
    assert denied.status_code in DENIED, (
        f"the explicit deny did not refuse {MEMBER2_EMAIL}: {describe(denied)}"
    )


def test_private_teamspace_is_absent_from_the_listing_and_denied_directly(member, admin):
    assert teamspace_named(member, PRIVATE_TEAMSPACE) is None, (
        f"the private teamspace {PRIVATE_TEAMSPACE!r} is listed to {MEMBER_EMAIL}"
    )
    assert teamspace_named(member, OPEN_TEAMSPACE) is not None, (
        f"the open teamspace {OPEN_TEAMSPACE!r} is missing from the listing"
    )
    private = teamspace_named(admin, PRIVATE_TEAMSPACE)
    assert private is not None, (
        f"an admin cannot see the private teamspace {PRIVATE_TEAMSPACE!r}"
    )
    direct = member.get(f"/teamspaces/{private['id']}")
    assert direct.status_code in DENIED, (
        f"a direct request for a private teamspace was served: {describe(direct)}"
    )
    assert code_of(direct) in ("", "not_found"), (
        f"the refusal confirms the private teamspace exists: {describe(direct)}"
    )


def test_member_is_denied_every_admin_endpoint_and_nothing_is_written(member, admin, backend):
    before = len(backend.rows("activity", limit=5000))
    for path in ("/admin/members", "/admin/groups", "/admin/activity"):
        response = member.get(path)
        assert response.status_code in DENIED, (
            f"a member session read the admin endpoint {path}: {describe(response)}"
        )
    listed = admin.get("/admin/members")
    assert listed.status_code == 200, describe(listed)
    target = [row for row in listed.json() if row.get("email") == GUEST_EMAIL]
    assert target, f"{GUEST_EMAIL} is absent from the admin member list"
    attempt = member.post(f"/admin/members/{target[0]['id']}/deactivate")
    assert attempt.status_code in DENIED, (
        f"a member session deactivated a principal: {describe(attempt)}"
    )
    still = [row for row in admin.get("/admin/members").json() if row.get("email") == GUEST_EMAIL]
    assert still and still[0].get("is_active") is not False, (
        f"the denied deactivation changed the stored principal: {still!r}"
    )
    assert len(backend.rows("activity", limit=5000)) == before, (
        "a denied admin call wrote a row into the activity record"
    )


def test_grant_change_from_a_member_session_is_denied(member, admin, handbook, backend):
    before = len(backend.rows("grants", limit=2000))
    attempt = member.post(
        "/grants",
        json={
            "resource_type": "page",
            "resource_id": handbook["page_id"],
            "subject_type": "principal",
            "subject_id": 0,
            "level": "full_access",
            "effect": "allow",
        },
    )
    assert attempt.status_code in DENIED, (
        f"a member session created a grant: {describe(attempt)}"
    )
    assert len(backend.rows("grants", limit=2000)) == before, (
        "a denied grant call changed the stored grants"
    )


def test_guest_row_response_omits_the_hidden_property(guest, member):
    database, views = _database(member)
    table = _view_named(views, TABLE_VIEW)
    member_rows = _rows(member, database["id"], table["id"])
    assert any(HIDDEN_PROPERTY in row for row in member_rows), (
        f"{HIDDEN_PROPERTY!r} is absent for a member, so the hidden-property rule "
        f"cannot be observed"
    )
    guest_response = guest.get(f"/databases/{database['id']}/views/{table['id']}/rows")
    assert guest_response.status_code == 200, describe(guest_response)
    for row in guest_response.json():
        assert HIDDEN_PROPERTY not in row, (
            f"{HIDDEN_PROPERTY!r} is present in a guest row response: {row!r}"
        )


def test_hidden_property_filter_and_sort_are_refused(guest, member):
    database, views = _database(member)
    table = _view_named(views, TABLE_VIEW)
    path = f"/databases/{database['id']}/views/{table['id']}/rows"
    filtered = guest.get(path, params={"filter_property": HIDDEN_PROPERTY, "filter_value": "x"})
    assert filtered.status_code >= 400, (
        f"a guest filtered on a hidden property: {describe(filtered)}"
    )
    sorted_response = guest.get(path, params={"sort_property": HIDDEN_PROPERTY})
    assert sorted_response.status_code >= 400, (
        f"a guest sorted on a hidden property: {describe(sorted_response)}"
    )


def test_search_results_exclude_a_denied_page(member2):
    response = member2.get("/search", params={"q": "Onboarding"})
    assert response.status_code == 200, describe(response)
    titles = [row.get("title") for row in response.json()]
    assert ONBOARDING not in titles, (
        f"a denied page appears in the search results of {MEMBER2_EMAIL}: {titles!r}"
    )
    for hidden in (CLOSED_TEAMSPACE, PRIVATE_TEAMSPACE):
        leak = member2.get("/search", params={"q": hidden})
        assert leak.status_code == 200, describe(leak)


def test_grant_provenance_names_where_each_grant_came_from(admin, handbook):
    response = admin.get(f"/pages/{handbook['page_id']}/access")
    assert response.status_code == 200, describe(response)
    rows = response.json()
    assert isinstance(rows, list) and rows, describe(response)
    for row in rows:
        for key in ("subject_type", "subject_id", "level", "effect", "source"):
            assert key in row, f"an access row is missing {key!r}: {row!r}"
        assert str(row["source"]).strip(), f"an access row names no grant source: {row!r}"


def test_anonymous_request_to_a_workspace_endpoint_is_denied(stranger):
    for path in ("/me", "/teamspaces", "/search", "/admin/activity"):
        response = stranger.get(path, params={"q": "x"})
        assert response.status_code in DENIED, (
            f"an anonymous caller read {path}: {describe(response)}"
        )


def test_deactivated_principal_token_stops_working(admin):
    token = token_for(GUEST_EMAIL)
    listed = admin.get("/admin/members")
    assert listed.status_code == 200, describe(listed)
    target = [row for row in listed.json() if row.get("email") == GUEST_EMAIL]
    assert target, f"{GUEST_EMAIL} is absent from the admin member list"
    principal_id = target[0]["id"]

    deactivated = admin.post(f"/admin/members/{principal_id}/deactivate")
    assert deactivated.status_code in (200, 201, 204), describe(deactivated)
    try:
        with appclient.client(token) as session:
            after = session.get("/me")
        assert after.status_code in DENIED, (
            f"a deactivated principal kept reading: {describe(after)}"
        )
    finally:
        admin.post(f"/admin/members/{principal_id}/activate")


def test_group_removal_denies_the_next_read(admin, member, backend):
    groups = admin.get("/admin/groups")
    assert groups.status_code == 200, describe(groups)
    editors = [row for row in groups.json() if row.get("name") == GROUP_NAME]
    assert editors, f"the seeded group {GROUP_NAME!r} is absent"
    group_id = editors[0]["id"]

    members_listed = admin.get("/admin/members")
    principal = [r for r in members_listed.json() if r.get("email") == MEMBER_EMAIL]
    assert principal, f"{MEMBER_EMAIL} is absent from the admin member list"
    principal_id = principal[0]["id"]

    removed = admin.delete(f"/admin/groups/{group_id}/members/{principal_id}")
    assert removed.status_code in (200, 204), describe(removed)
    listed = admin.get("/admin/groups")
    after = [row for row in listed.json() if row.get("id") == group_id]
    assert after, describe(listed)
    remaining = [str(m) for m in (after[0].get("members") or [])]
    assert str(principal_id) not in remaining, (
        f"the principal is still in the group after removal: {after[0]!r}"
    )

    restored = admin.post(f"/admin/groups/{group_id}/members", json={"principal_id": principal_id})
    assert restored.status_code in (200, 201), describe(restored)


def test_expired_grant_denies_the_next_read(admin, guest, backend):
    members_listed = admin.get("/admin/members")
    assert members_listed.status_code == 200, describe(members_listed)
    principal = [r for r in members_listed.json() if r.get("email") == GUEST_EMAIL]
    assert principal, f"{GUEST_EMAIL} is absent from the admin member list"
    principal_id = principal[0]["id"]

    page = page_named(admin, CLOSED_TEAMSPACE) or page_named(admin, "Compensation Bands")
    assert page is not None, "no page inside the closed teamspace was found"

    created = admin.post(
        "/grants",
        json={
            "resource_type": "page",
            "resource_id": page["page_id"],
            "subject_type": "principal",
            "subject_id": principal_id,
            "level": "read",
            "effect": "allow",
            "expires_at": "2020-01-01T00:00:00Z",
        },
    )
    assert created.status_code in (200, 201), describe(created)

    response = guest.get(f"/pages/{page['page_id']}")
    assert response.status_code in DENIED, (
        f"an expired grant still allowed a read: {describe(response)}"
    )
    rows = backend.rows("grants", limit=2000)
    assert any(str(r.get("id")) == str(created.json().get("id")) for r in rows), (
        "the expired grant row was deleted rather than retained"
    )


def test_block_depth_bound_is_enforced_at_the_api(member, handbook):
    page_id = handbook["page_id"]
    before = len(member.get(f"/pages/{page_id}/blocks").json())
    response = member.post(
        f"/pages/{page_id}/blocks",
        json={"type": "paragraph", "text": f"probe-{probe_id()}", "position": 0, "depth": 9},
    )
    assert response.status_code >= 400, (
        f"a block deeper than the bound was accepted: {describe(response)}"
    )
    assert response.status_code < 500, (
        f"an over-deep block produced a server error: {describe(response)}"
    )
    after = len(member.get(f"/pages/{page_id}/blocks").json())
    assert after == before, "a refused over-deep insert still wrote a block"


def test_duplicate_public_slug_is_refused(member):
    page_id = _page_id(member, ONBOARDING)
    response = member.post(
        f"/pages/{page_id}/publish",
        json={"slug": RELEASE_NOTES_SLUG, "include_subtree": False},
    )
    assert response.status_code >= 400, (
        f"a slug already in use was accepted for a second page: {describe(response)}"
    )
    assert response.status_code < 500, (
        f"a duplicate slug produced a server error: {describe(response)}"
    )


def test_rate_limited_after_five_failed_password_attempts(stranger):
    address = f"probe-{probe_id()}@example.com"
    statuses = []
    for _ in range(7):
        response = stranger.post(
            "/auth/login", json={"email": address, "password": "not-the-password"}
        )
        statuses.append(response.status_code)
        if code_of(response) == "rate_limited" or response.status_code == 429:
            return
    assert False, (
        f"seven failed password attempts for one address were never refused: {statuses!r}"
    )


def test_uploaded_attachment_object_exists_in_the_bucket_at_its_key(member, handbook, store):
    page_id = handbook["page_id"]
    payload = f"probe-{probe_id()}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    response = member.post(
        f"/pages/{page_id}/attachments",
        files={"file": (f"probe-{digest[:8]}.png", payload, "image/png")},
        data={"filename": f"probe-{digest[:8]}.png"},
    )
    assert response.status_code in (200, 201), describe(response)
    body = response.json()
    key = body.get("object_key")
    assert key, f"the upload response carries no object_key: {describe(response)}"
    assert key.startswith(KEY_SCHEME_PREFIX), (
        f"the object key {key!r} does not follow the pinned scheme prefix "
        f"{KEY_SCHEME_PREFIX!r}"
    )
    assert digest in key, (
        f"the object key {key!r} does not carry the sha256 of the uploaded bytes"
    )
    assert settle(lambda: store.exists(key)), (
        f"no object exists in the bucket at {key!r}, so the bytes are not in the store"
    )


def test_attachment_bytes_are_not_stored_in_a_database_column(member, handbook, backend):
    page_id = handbook["page_id"]
    payload = f"probe-{probe_id()}".encode("utf-8") * 8
    response = member.post(
        f"/pages/{page_id}/attachments",
        files={"file": ("probe-bytes.png", payload, "image/png")},
        data={"filename": "probe-bytes.png"},
    )
    assert response.status_code in (200, 201), describe(response)
    rows = backend.rows("attachments", limit=500)
    assert rows, "the attachments table holds no row after an upload"
    needle = payload.decode("utf-8")
    for row in rows:
        blob = json.dumps(row, default=str)
        assert needle not in blob, (
            f"the uploaded bytes are stored inside the attachments row: {row!r}"
        )


def test_attachment_read_is_denied_to_an_anonymous_caller_while_unpublished(member, handbook, stranger):
    page_id = handbook["page_id"]
    unpublish = member.delete(f"/pages/{page_id}/publish")
    assert unpublish.status_code in (200, 204, 404, 409), describe(unpublish)

    payload = f"probe-{probe_id()}".encode("utf-8")
    uploaded = member.post(
        f"/pages/{page_id}/attachments",
        files={"file": ("probe-private.png", payload, "image/png")},
        data={"filename": "probe-private.png"},
    )
    assert uploaded.status_code in (200, 201), describe(uploaded)
    attachment_id = uploaded.json()["id"]

    denied = stranger.get(f"/attachments/{attachment_id}")
    assert denied.status_code in DENIED, (
        f"an anonymous caller read an attachment on an unpublished page: {describe(denied)}"
    )
    public = stranger.get(f"/public/attachments/{attachment_id}")
    assert public.status_code in DENIED, (
        f"the public attachment route served an unpublished page file: {describe(public)}"
    )


def test_attachment_on_a_published_page_is_readable_anonymously(member, stranger):
    page_id = _page_id(member, RELEASE_NOTES)
    payload = f"probe-{probe_id()}".encode("utf-8")
    uploaded = member.post(
        f"/pages/{page_id}/attachments",
        files={"file": ("probe-public.png", payload, "image/png")},
        data={"filename": "probe-public.png"},
    )
    assert uploaded.status_code in (200, 201), describe(uploaded)
    attachment_id = uploaded.json()["id"]

    published = member.post(
        f"/pages/{page_id}/publish",
        json={"slug": RELEASE_NOTES_SLUG, "include_subtree": False},
    )
    assert published.status_code in (200, 201), describe(published)

    served = settle(lambda: _ok(stranger.get(f"/public/attachments/{attachment_id}")))
    assert served is not None, (
        f"an attachment on the published page {RELEASE_NOTES!r} is not readable anonymously"
    )


def test_every_response_carries_the_security_headers(site):
    for path in ("/", f"/site/{RELEASE_NOTES_SLUG}", "/api/health"):
        response = site.get(path)
        lowered = {name.lower() for name in response.headers.keys()}
        for header in SECURITY_HEADER_NAMES:
            assert header in lowered, (
                f"{path} carries no {header} header: {sorted(lowered)!r}"
            )


def test_no_credential_appears_in_anything_the_browser_downloads(site):
    root = site.get("/")
    assert root.status_code == 200, describe(root)
    assets = set(re.findall(r'(?:src|href)="(/[^"#?]*\.(?:js|css|mjs))"', root.text))
    bodies = [root.text]
    for asset in sorted(assets):
        fetched = site.get(asset)
        if fetched.status_code == 200:
            bodies.append(fetched.text)
    needles = [
        CORPUS_PASSWORD,
        "minio-root-3d81f7a2",
        "deku-local-dev",
        "STORAGE_SECRET_KEY",
        "DB_ADMIN_URL",
    ]
    for body in bodies:
        for needle in needles:
            assert needle not in body, (
                f"a credential {needle!r} appears in something the browser downloads"
            )


def test_favicon_is_served_and_declared_in_the_document_head(site):
    root = site.get("/")
    assert root.status_code == 200, describe(root)
    declared = re.search(r'<link[^>]+rel="[^"]*icon[^"]*"[^>]*href="([^"]+)"', root.text)
    assert declared, f"the document head declares no favicon: {root.text[:400]!r}"
    href = declared.group(1)
    if href.startswith("http"):
        return
    fetched = site.get(href if href.startswith("/") else "/" + href)
    assert fetched.status_code == 200, (
        f"the declared favicon does not resolve: {describe(fetched)}"
    )


def _ok(response):
    return response if response.status_code == 200 else None


def _gone(response):
    return response if response.status_code >= 400 else None


def _has_page(response, title):
    if response.status_code != 200:
        return False
    return any(row.get("title") == title for row in response.json())


def _member_token():
    return token_for(MEMBER_EMAIL)


def _page_id(client, title):
    row = page_named(client, title)
    assert row is not None, f"the seeded page {title!r} was not found through search"
    return row["page_id"]


def _database(client):
    row = page_named(client, DATABASE_NAME)
    assert row is not None, f"the seeded database page {DATABASE_NAME!r} was not found"
    response = client.get(f"/databases/{row.get('database_id') or row['page_id']}")
    assert response.status_code == 200, describe(response)
    body = response.json()
    return body, body.get("views") or []


def _view_named(views, name):
    for view in views:
        if view.get("name") == name:
            return view
    return None


def _rows(client, database_id, view_id):
    response = client.get(f"/databases/{database_id}/views/{view_id}/rows")
    assert response.status_code == 200, describe(response)
    body = response.json()
    assert isinstance(body, list), describe(response)
    return body
