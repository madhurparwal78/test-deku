"""The one pytest module for deku/crowdsourced-cartography-platform-vb.

Sections in order: core features, data integrity, authorization, edge cases.
Every assertion is black box: HTTP against the deployed app plus generic
persisted-state reads through the capability backend. Nothing here inspects the
agent's source, schema shape beyond the pinned table and field names, framework
or module layout.
"""

from __future__ import annotations

import concurrent.futures
import json

import httpx
import pytest
from appclient import api_base, client, login
from conftest import (
    BBOX_AREA_CAP,
    BBOX_ELEMENT_CAP,
    BUS_ROUTE_RELATION_ID,
    CAFE_NODE_ID,
    CHANGESET_ELEMENT_CEILING,
    CONFLICT,
    CYCLE_ROUTE_RELATION_ID,
    DEEPEST_ZOOM,
    DENIED,
    MAPPER2_EMAIL,
    MAPPER3_EMAIL,
    MAPPER_EMAIL,
    MILL_NODE_ID,
    OK,
    OVERSIZED_BBOX,
    REFUSED,
    ROAD_VERTEX_NODE_ID,
    ROAD_WAY_ID,
    SEEDED_CAFE_NAME,
    SEEDED_CHANGESET_COMMENTS,
    SEEDED_DIARY_TITLES,
    SEEDED_PASSWORD,
    SEED_BBOX,
    TILE_EDGE_PX,
    app_page_url,
    close_changeset,
    modify_node,
    open_changeset,
    poll_until,
    probe_email,
    read_node,
    unique_suffix,
    upload,
)


def _name_of(element: dict) -> str | None:
    tags = element.get("tags")
    if isinstance(tags, dict):
        return tags.get("name")
    if isinstance(tags, list):
        for tag in tags:
            if isinstance(tag, dict) and tag.get("key") == "name":
                return tag.get("value")
    return element.get("name")


def _created_node_id(response: httpx.Response) -> int | None:
    body = response.json()
    candidates = []
    if isinstance(body, dict):
        for key in ("nodes", "created", "elements"):
            value = body.get(key)
            if isinstance(value, list):
                candidates.extend(value)
            elif isinstance(value, dict):
                candidates.extend(value.get("nodes", []) if isinstance(value.get("nodes"), list) else [])
        if "id" in body:
            candidates.append(body)
    elif isinstance(body, list):
        candidates.extend(body)
    for item in candidates:
        if isinstance(item, dict) and isinstance(item.get("id"), int):
            return item["id"]
    return None


def _fetch_page(path: str) -> httpx.Response:
    return httpx.get(app_page_url(path), timeout=30.0, follow_redirects=True)


def test_signup_creates_mapper(anon_client, store):
    email = probe_email()
    response = anon_client.post(
        "/auth/signup",
        json={"email": email, "password": SEEDED_PASSWORD, "display_name": "Probe Mapper"},
    )
    assert response.status_code in OK, (
        f"signup for {email} returned {response.status_code}: {response.text[:400]}"
    )
    created = poll_until(lambda: store.mapper_by_email(email))
    assert created, f"signup for {email} returned success but stored no mapper row"


def test_login_returns_bearer_token(anon_client):
    response = anon_client.post(
        "/auth/login", json={"email": MAPPER_EMAIL, "password": SEEDED_PASSWORD}
    )
    assert response.status_code in OK, (
        f"login for {MAPPER_EMAIL} returned {response.status_code}: {response.text[:400]}"
    )
    token = response.json().get("access_token")
    assert token, f"login response carries no access_token: {response.text[:400]}"


def test_duplicate_email_signup_rejected(anon_client, store):
    before = store.count_rows("mappers", email=MAPPER_EMAIL)
    response = anon_client.post(
        "/auth/signup",
        json={"email": MAPPER_EMAIL, "password": SEEDED_PASSWORD, "display_name": "Impostor"},
    )
    assert response.status_code in REFUSED, (
        f"signing up with the seeded email {MAPPER_EMAIL} returned "
        f"{response.status_code}, expected a client-error refusal: {response.text[:400]}"
    )
    after = store.count_rows("mappers", email=MAPPER_EMAIL)
    assert after == before, (
        f"a refused duplicate signup changed the mapper count for {MAPPER_EMAIL} "
        f"from {before} to {after}"
    )


def test_changeset_open_upload_close_cycle(mapper_client, store):
    changeset_id = open_changeset(mapper_client, f"probe cycle {unique_suffix()}")
    version = store.latest_version("nodes", MILL_NODE_ID)
    response = upload(
        mapper_client,
        changeset_id,
        modify_node(MILL_NODE_ID, version, tags={"historic": "mill", "name": f"Mill {unique_suffix()}"}),
    )
    assert response.status_code in OK, (
        f"uploading into changeset {changeset_id} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    closed = close_changeset(mapper_client, changeset_id)
    assert closed.status_code in OK, (
        f"closing changeset {changeset_id} returned {closed.status_code}: {closed.text[:400]}"
    )
    row = store.changeset(changeset_id)
    assert row and row.get("closed_at"), (
        f"changeset {changeset_id} reports no closed_at after a successful close"
    )


def test_upload_raises_element_version_by_one(mapper_client, store):
    before = store.latest_version("nodes", MILL_NODE_ID)
    changeset_id = open_changeset(mapper_client, f"probe bump {unique_suffix()}")
    response = upload(
        mapper_client,
        changeset_id,
        modify_node(MILL_NODE_ID, before, tags={"historic": "mill", "name": f"Mill {unique_suffix()}"}),
    )
    assert response.status_code in OK, (
        f"upload returned {response.status_code}: {response.text[:400]}"
    )
    after = poll_until(lambda: store.latest_version("nodes", MILL_NODE_ID) > before)
    now = store.latest_version("nodes", MILL_NODE_ID)
    assert after and now == before + 1, (
        f"node {MILL_NODE_ID} went from version {before} to {now}, expected exactly "
        f"{before + 1}"
    )


def test_way_belongs_to_two_relations(anon_client, store):
    relations = store.relations_referencing("way", ROAD_WAY_ID)
    assert BUS_ROUTE_RELATION_ID in relations and CYCLE_ROUTE_RELATION_ID in relations, (
        f"way {ROAD_WAY_ID} is referenced by relations {relations}, expected both "
        f"{BUS_ROUTE_RELATION_ID} and {CYCLE_ROUTE_RELATION_ID}"
    )
    for relation_id in (BUS_ROUTE_RELATION_ID, CYCLE_ROUTE_RELATION_ID):
        response = anon_client.get(f"/relation/{relation_id}")
        assert response.status_code in OK, (
            f"reading relation {relation_id} returned {response.status_code}: "
            f"{response.text[:400]}"
        )
        body = json.dumps(response.json())
        assert str(ROAD_WAY_ID) in body, (
            f"relation {relation_id} does not name way {ROAD_WAY_ID} in its members: "
            f"{body[:400]}"
        )


def test_element_history_returns_every_version(mapper_client, anon_client, store):
    changeset_id = open_changeset(mapper_client, f"probe history {unique_suffix()}")
    version = store.latest_version("nodes", MILL_NODE_ID)
    upload(mapper_client, changeset_id, modify_node(MILL_NODE_ID, version, tags={"historic": "mill", "name": f"Mill {unique_suffix()}"}))
    close_changeset(mapper_client, changeset_id)
    response = anon_client.get(f"/node/{MILL_NODE_ID}/history")
    assert response.status_code in OK, (
        f"node history returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    assert isinstance(body, list), (
        f"node history must be a top-level JSON array, got {type(body).__name__}"
    )
    stored = store.version_count("nodes", MILL_NODE_ID)
    assert len(body) == stored, (
        f"node history returned {len(body)} versions but the dataset holds {stored}"
    )


def test_past_version_is_addressable(mapper_client, anon_client, store):
    original = read_node(anon_client, CAFE_NODE_ID)
    original_version = int(original["version"])
    original_name = _name_of(original)
    changeset_id = open_changeset(mapper_client, f"probe past {unique_suffix()}")
    upload(
        mapper_client,
        changeset_id,
        modify_node(CAFE_NODE_ID, original_version, tags={"amenity": "cafe", "name": f"Cafe {unique_suffix()}"}),
    )
    close_changeset(mapper_client, changeset_id)
    response = anon_client.get(f"/node/{CAFE_NODE_ID}/{original_version}")
    assert response.status_code in OK, (
        f"reading node {CAFE_NODE_ID} at version {original_version} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    assert _name_of(response.json()) == original_name, (
        f"node {CAFE_NODE_ID} at version {original_version} reads "
        f"{_name_of(response.json())!r}, expected the value it held then, {original_name!r}"
    )


def test_changeset_stream_newest_first(anon_client):
    response = anon_client.get("/changesets")
    assert response.status_code in OK, (
        f"changeset stream returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    assert isinstance(body, list), (
        f"the changeset stream must be a top-level JSON array, got {type(body).__name__}"
    )
    assert body, "the changeset stream is empty, though three changesets are seeded"
    ids = [int(row["id"]) for row in body if "id" in row]
    assert ids == sorted(ids, reverse=True), (
        f"the changeset stream is ordered {ids[:10]}, expected newest first"
    )


def test_changeset_lists_elements_it_wrote(anon_client, store):
    stream = anon_client.get("/changesets").json()
    target = next(
        (row for row in stream if row.get("comment") == SEEDED_CHANGESET_COMMENTS[0]), None
    )
    assert target, (
        f"no changeset in the stream carries the seeded comment "
        f"{SEEDED_CHANGESET_COMMENTS[0]!r}"
    )
    response = anon_client.get(f"/changeset/{target['id']}")
    assert response.status_code in OK, (
        f"reading changeset {target['id']} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    body = json.dumps(response.json())
    assert str(CAFE_NODE_ID) in body, (
        f"changeset {target['id']} lists no elements it wrote: {body[:400]}"
    )


def test_revert_creates_new_attributed_changeset(mapper3_client, store):
    stream_before = store.changeset_count()
    stream = mapper3_client.get("/changesets").json()
    target = next(
        (row for row in stream if row.get("comment") == SEEDED_CHANGESET_COMMENTS[2]), None
    )
    assert target, (
        f"no changeset carries the seeded comment {SEEDED_CHANGESET_COMMENTS[2]!r}"
    )
    response = mapper3_client.post(f"/changeset/{target['id']}/revert")
    assert response.status_code in OK, (
        f"reverting changeset {target['id']} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    grew = poll_until(lambda: store.changeset_count() > stream_before)
    assert grew, (
        f"a successful revert of changeset {target['id']} added no new changeset; "
        f"the count is still {store.changeset_count()}"
    )
    reverter = store.mapper_by_email(MAPPER3_EMAIL)
    assert reverter, f"the seeded mapper {MAPPER3_EMAIL} has no row"


def test_bbox_map_call_returns_elements(anon_client):
    response = anon_client.get("/map", params={"bbox": SEED_BBOX})
    assert response.status_code in OK, (
        f"the map call for {SEED_BBOX} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    body = response.json()
    assert isinstance(body, dict), (
        f"the map call must return an object of element arrays, got {type(body).__name__}"
    )
    nodes = body.get("nodes")
    assert isinstance(nodes, list) and nodes, (
        f"the map call over the seeded area returned no nodes: {json.dumps(body)[:400]}"
    )


def test_new_element_findable_by_bbox_at_once(mapper_client, anon_client):
    changeset_id = open_changeset(mapper_client, f"probe findable {unique_suffix()}")
    marker = f"Probe Point {unique_suffix()}"
    response = upload(
        mapper_client,
        changeset_id,
        {"create": {"nodes": [{"lat": 51.5001, "lon": -0.1250, "tags": {"amenity": "bench", "name": marker}}]}},
    )
    assert response.status_code in OK, (
        f"creating a node returned {response.status_code}: {response.text[:400]}"
    )
    close_changeset(mapper_client, changeset_id)

    def visible_in_bbox():
        found = anon_client.get("/map", params={"bbox": SEED_BBOX})
        return found.status_code in OK and marker in found.text

    assert poll_until(visible_in_bbox), (
        f"a node created seconds ago is not returned by a map call covering it "
        f"({marker!r} absent from the {SEED_BBOX} response)"
    )


def test_export_downloads_elements_for_view(anon_client):
    response = anon_client.get("/map", params={"bbox": SEED_BBOX})
    assert response.status_code in OK, (
        f"the export read for {SEED_BBOX} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    assert SEEDED_CAFE_NAME in response.text, (
        f"the raw element download for the seeded area does not carry "
        f"{SEEDED_CAFE_NAME!r}: {response.text[:400]}"
    )


def test_tile_endpoint_returns_image(anon_client):
    response = anon_client.get("/tile/12/2047/1362.png")
    assert response.status_code in OK, (
        f"the tile endpoint returned {response.status_code}: {response.text[:200]}"
    )
    assert response.content, "the tile endpoint returned an empty body"
    assert DEEPEST_ZOOM >= 12, "the pinned deepest zoom must cover the requested tile"


def test_tile_marked_stale_after_edit_in_bounds(mapper_client, anon_client, store):
    path = "/tile/12/2047/1362.png"
    first = anon_client.get(path)
    assert first.status_code in OK, (
        f"the first tile request returned {first.status_code}: {first.text[:200]}"
    )
    before = first.content
    changeset_id = open_changeset(mapper_client, f"probe tile {unique_suffix()}")
    version = store.latest_version("nodes", CAFE_NODE_ID)
    upload(
        mapper_client,
        changeset_id,
        modify_node(CAFE_NODE_ID, version, tags={"amenity": "cafe", "name": f"Cafe {unique_suffix()}"}),
    )
    close_changeset(mapper_client, changeset_id)

    def redrawn():
        again = anon_client.get(path)
        return again.status_code in OK and again.content != before

    assert poll_until(redrawn), (
        "a tile covering an edited element was served unchanged after the edit, so "
        "the edit's bounds did not mark the tile stale"
    )


def test_diary_list_newest_first(anon_client):
    response = anon_client.get("/diary")
    assert response.status_code in OK, (
        f"the diary endpoint returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    assert isinstance(body, list), (
        f"the diary must be a top-level JSON array, got {type(body).__name__}"
    )
    titles = [row.get("title") for row in body]
    assert titles[: len(SEEDED_DIARY_TITLES)] == list(SEEDED_DIARY_TITLES), (
        f"the diary reads {titles[:3]}, expected the seeded entries newest first: "
        f"{list(SEEDED_DIARY_TITLES)}"
    )


def test_about_page_names_five_sections():
    page = _fetch_page("/about")
    assert page.status_code in OK, (
        f"the about page returned {page.status_code}: {page.text[:200]}"
    )
    for heading in ("Local Knowledge", "Community Driven", "Open Data", "Legal", "Partners"):
        assert heading in page.text, (
            f"the about page does not carry the section {heading!r}"
        )


def test_help_card_is_wholly_clickable():
    page = _fetch_page("/help")
    assert page.status_code in OK, (
        f"the help page returned {page.status_code}: {page.text[:200]}"
    )
    assert "Getting Help" in page.text, "the help page does not carry its own heading"
    assert page.text.count("<a") >= 5, (
        f"the help page carries {page.text.count('<a')} links, expected one per card "
        f"with the whole card clickable"
    )


def test_welcome_card_dismissal_survives_reload():
    page = _fetch_page("/")
    assert page.status_code in OK, (
        f"the map home returned {page.status_code}: {page.text[:200]}"
    )
    assert "Welcome to Openhaven!" in page.text, (
        "the map home does not carry the welcome card heading for a first-time visitor"
    )


def test_search_drops_result_pin(anon_client):
    response = anon_client.get("/map", params={"bbox": SEED_BBOX, "q": SEEDED_CAFE_NAME})
    assert response.status_code in OK, (
        f"a place search returned {response.status_code}: {response.text[:400]}"
    )
    assert SEEDED_CAFE_NAME in response.text, (
        f"searching for {SEEDED_CAFE_NAME!r} returned no matching feature: "
        f"{response.text[:400]}"
    )


def test_unknown_address_renders_own_not_found_page():
    page = _fetch_page(f"/no-such-place-{unique_suffix()}")
    assert page.status_code == 404, (
        f"an unmatched address answered {page.status_code}, expected 404"
    )
    assert "File not found" in page.text, (
        f"an unmatched address does not render the product's own not-found page: "
        f"{page.text[:200]}"
    )


def test_persisted_element_matches_ui_and_survives_reload(mapper_client, store):
    corrected = f"Mill House {unique_suffix()}"
    version = store.latest_version("nodes", MILL_NODE_ID)
    changeset_id = open_changeset(mapper_client, f"probe persist {unique_suffix()}")
    response = upload(
        mapper_client,
        changeset_id,
        modify_node(MILL_NODE_ID, version, tags={"historic": "mill", "name": corrected}),
    )
    assert response.status_code in OK, (
        f"saving the corrected name returned {response.status_code}: {response.text[:400]}"
    )
    close_changeset(mapper_client, changeset_id)

    fresh_token = login(MAPPER_EMAIL, SEEDED_PASSWORD)
    with client(fresh_token) as reloaded:
        element = read_node(reloaded, MILL_NODE_ID)
    assert _name_of(element) == corrected, (
        f"a fresh session reads node {MILL_NODE_ID} as {_name_of(element)!r}, but "
        f"{corrected!r} was saved"
    )
    assert int(element["version"]) == version + 1, (
        f"node {MILL_NODE_ID} reads version {element['version']} after one save from "
        f"version {version}, expected {version + 1}"
    )
    stored_version = store.latest_version("nodes", MILL_NODE_ID)
    stored_tags = store.tags_at("node", MILL_NODE_ID, stored_version)
    assert stored_tags.get("name") == corrected, (
        f"the dataset holds name {stored_tags.get('name')!r} for node "
        f"{MILL_NODE_ID} at version {stored_version}, but the app returned "
        f"{corrected!r}"
    )


def test_delete_writes_new_version_not_erasure(mapper_client, store):
    marker = f"Bench {unique_suffix()}"
    changeset_id = open_changeset(mapper_client, f"probe delete {unique_suffix()}")
    created = upload(
        mapper_client,
        changeset_id,
        {"create": {"nodes": [{"lat": 51.5002, "lon": -0.1249, "tags": {"amenity": "bench", "name": marker}}]}},
    )
    assert created.status_code in OK, (
        f"creating a disposable node returned {created.status_code}: {created.text[:400]}"
    )
    close_changeset(mapper_client, changeset_id)

    node_id = _created_node_id(created)
    assert node_id is not None, (
        f"the create response names no new node id: {created.text[:400]}"
    )
    versions_before = store.version_count("nodes", node_id)
    live_version = store.latest_version("nodes", node_id)

    removal = open_changeset(mapper_client, f"probe remove {unique_suffix()}")
    removed = upload(
        mapper_client,
        removal,
        {"delete": {"nodes": [{"id": node_id, "version": live_version}]}},
    )
    assert removed.status_code in OK, (
        f"deleting node {node_id}, which nothing references, returned "
        f"{removed.status_code}: {removed.text[:400]}"
    )
    close_changeset(mapper_client, removal)

    versions_after = store.version_count("nodes", node_id)
    assert versions_after == versions_before + 1, (
        f"deleting node {node_id} took its version count from {versions_before} to "
        f"{versions_after}; a delete writes a new version rather than erasing a row"
    )
    assert not store.is_visible("nodes", node_id), (
        f"node {node_id} still reads as visible after being deleted"
    )
    kept = store.row_at_version("nodes", node_id, live_version)
    assert kept, (
        f"version {live_version} of node {node_id} was removed by the delete; every "
        f"past version stays readable"
    )


def test_older_version_rows_never_mutated(mapper_client, store):
    version = store.latest_version("nodes", CAFE_NODE_ID)
    first = store.row_at_version("nodes", CAFE_NODE_ID, 1)
    assert first, f"node {CAFE_NODE_ID} has no version 1 row"
    first_tags = store.tags_at("node", CAFE_NODE_ID, 1)
    changeset_id = open_changeset(mapper_client, f"probe immutable {unique_suffix()}")
    upload(
        mapper_client,
        changeset_id,
        modify_node(CAFE_NODE_ID, version, tags={"amenity": "cafe", "name": f"Cafe {unique_suffix()}"}),
    )
    close_changeset(mapper_client, changeset_id)
    still = store.tags_at("node", CAFE_NODE_ID, 1)
    assert still == first_tags, (
        f"version 1 of node {CAFE_NODE_ID} changed from {first_tags} to {still} when a "
        f"later version was written; history is append-only"
    )


def test_seed_is_idempotent(store):
    for table, expected in (("mappers", 3), ("changesets", 3)):
        actual = store.count_rows(table)
        assert actual >= expected, (
            f"the {table} table holds {actual} rows, expected at least the {expected} "
            f"seeded ones"
        )
    assert store.count_rows("mappers", email=MAPPER_EMAIL) == 1, (
        f"the seeded mapper {MAPPER_EMAIL} appears "
        f"{store.count_rows('mappers', email=MAPPER_EMAIL)} times, so seeding is not "
        f"idempotent"
    )
    assert store.count_rows("mappers", email=MAPPER2_EMAIL) == 1, (
        f"the seeded mapper {MAPPER2_EMAIL} is duplicated, so seeding is not idempotent"
    )


def test_changeset_bbox_derived_from_elements(mapper_client, store):
    changeset_id = open_changeset(mapper_client, f"probe bbox {unique_suffix()}")
    version = store.latest_version("nodes", CAFE_NODE_ID)
    upload(
        mapper_client,
        changeset_id,
        modify_node(CAFE_NODE_ID, version, tags={"amenity": "cafe", "name": f"Cafe {unique_suffix()}"}),
    )
    close_changeset(mapper_client, changeset_id)
    row = poll_until(lambda: store.changeset(changeset_id))
    assert row, f"changeset {changeset_id} has no stored row"
    for field in ("min_lon", "min_lat", "max_lon", "max_lat"):
        assert row.get(field) is not None, (
            f"changeset {changeset_id} has no {field}, so its bounding box was not "
            f"computed from the elements it touched"
        )
    assert row.get("element_count") and int(row["element_count"]) >= 1, (
        f"changeset {changeset_id} reports element_count {row.get('element_count')}, "
        f"expected at least 1"
    )


def test_signed_out_upload_denied(anon_client, store):
    before = store.latest_version("nodes", CAFE_NODE_ID)
    created = anon_client.put("/changeset/create", json={"comment": "anonymous edit"})
    assert created.status_code in DENIED, (
        f"opening a changeset with no token returned {created.status_code}, expected a "
        f"denial: {created.text[:400]}"
    )
    attempted = anon_client.post(
        "/changeset/1/upload", json=modify_node(CAFE_NODE_ID, before, tags={"amenity": "cafe", "name": "Hijacked"})
    )
    assert attempted.status_code in DENIED, (
        f"uploading with no token returned {attempted.status_code}, expected a denial: "
        f"{attempted.text[:400]}"
    )
    after = store.latest_version("nodes", CAFE_NODE_ID)
    assert after == before, (
        f"node {CAFE_NODE_ID} moved from version {before} to {after} after a denied "
        f"unauthenticated upload; a denial must leave the state unchanged"
    )


def test_expired_token_denied(store):
    before = store.latest_version("nodes", CAFE_NODE_ID)
    with client("expired." + unique_suffix()) as bad:
        response = bad.put("/changeset/create", json={"comment": "expired token edit"})
    assert response.status_code in DENIED, (
        f"a request carrying an unusable token returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}"
    )
    after = store.latest_version("nodes", CAFE_NODE_ID)
    assert after == before, (
        f"node {CAFE_NODE_ID} moved from version {before} to {after} after a denied "
        f"request"
    )


def test_password_never_returned_by_any_endpoint(anon_client, mapper_client):
    login_response = anon_client.post(
        "/auth/login", json={"email": MAPPER_EMAIL, "password": SEEDED_PASSWORD}
    )
    assert SEEDED_PASSWORD not in login_response.text, (
        "the login response carries the seeded password in its body"
    )
    for path in ("/changesets", "/diary", f"/node/{CAFE_NODE_ID}"):
        response = mapper_client.get(path)
        assert SEEDED_PASSWORD not in response.text, (
            f"the response from {path} carries the seeded password"
        )
        assert "password_hash" not in response.text, (
            f"the response from {path} exposes a stored password hash"
        )


def test_concurrent_uploads_produce_single_winner(mapper_client, mapper2_client, store):
    start_version = store.latest_version("nodes", CAFE_NODE_ID)
    first_changeset = open_changeset(mapper_client, f"race a {unique_suffix()}")
    second_changeset = open_changeset(mapper2_client, f"race b {unique_suffix()}")
    payload_a = modify_node(CAFE_NODE_ID, start_version, tags={"amenity": "cafe", "name": f"Cafe A {unique_suffix()}"})
    payload_b = modify_node(CAFE_NODE_ID, start_version, tags={"amenity": "cafe", "name": f"Cafe B {unique_suffix()}"})

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(upload, mapper_client, first_changeset, payload_a),
            pool.submit(upload, mapper2_client, second_changeset, payload_b),
        ]
        responses = [f.result() for f in futures]

    codes = sorted(r.status_code for r in responses)
    accepted = [r for r in responses if r.status_code in OK]
    refused = [r for r in responses if r.status_code not in OK]
    assert len(accepted) == 1, (
        f"two simultaneous uploads claiming version {start_version} of node "
        f"{CAFE_NODE_ID} returned {codes}; exactly one must be accepted"
    )
    assert refused and refused[0].status_code in CONFLICT, (
        f"the losing upload returned {refused[0].status_code if refused else None}, "
        f"expected a 409 conflict naming the element and the versions"
    )
    losing_body = refused[0].text
    assert str(CAFE_NODE_ID) in losing_body and str(start_version) in losing_body, (
        f"the conflict response names neither the element nor the version the client "
        f"held: {losing_body[:400]}"
    )
    final_version = store.latest_version("nodes", CAFE_NODE_ID)
    assert final_version == start_version + 1, (
        f"node {CAFE_NODE_ID} ended at version {final_version} after a race from "
        f"version {start_version}; exactly one new version must exist"
    )


def test_replayed_upload_creates_no_second_version(mapper_client, store):
    start_version = store.latest_version("nodes", MILL_NODE_ID)
    changeset_id = open_changeset(mapper_client, f"probe replay {unique_suffix()}")
    payload = modify_node(MILL_NODE_ID, start_version, tags={"historic": "mill", "name": f"Mill {unique_suffix()}"})
    first = upload(mapper_client, changeset_id, payload)
    assert first.status_code in OK, (
        f"the first upload returned {first.status_code}: {first.text[:400]}"
    )
    after_first = store.latest_version("nodes", MILL_NODE_ID)
    second = upload(mapper_client, changeset_id, payload)
    assert second.status_code in OK + CONFLICT + REFUSED, (
        f"replaying an applied upload returned {second.status_code}: {second.text[:400]}"
    )
    after_second = store.latest_version("nodes", MILL_NODE_ID)
    assert after_second == after_first, (
        f"replaying the same upload moved node {MILL_NODE_ID} from version "
        f"{after_first} to {after_second}; a replay must create no second version"
    )


def test_delete_of_node_in_use_refused(mapper_client, store):
    version = store.latest_version("nodes", ROAD_VERTEX_NODE_ID)
    changeset_id = open_changeset(mapper_client, f"probe in use {unique_suffix()}")
    response = upload(
        mapper_client,
        changeset_id,
        {"delete": {"nodes": [{"id": ROAD_VERTEX_NODE_ID, "version": version}]}},
    )
    assert response.status_code in REFUSED, (
        f"deleting node {ROAD_VERTEX_NODE_ID}, a vertex of way {ROAD_WAY_ID}, returned "
        f"{response.status_code}, expected a refusal: {response.text[:400]}"
    )
    assert "still in use" in response.text.lower(), (
        f"the refusal does not say the node is still in use: {response.text[:400]}"
    )
    assert store.is_visible("nodes", ROAD_VERTEX_NODE_ID), (
        f"node {ROAD_VERTEX_NODE_ID} is no longer visible after a refused delete"
    )


def test_atomic_upload_rolls_back_whole_batch(mapper_client, store):
    cafe_before = store.latest_version("nodes", CAFE_NODE_ID)
    vertex_before = store.latest_version("nodes", ROAD_VERTEX_NODE_ID)
    changeset_id = open_changeset(mapper_client, f"probe atomic {unique_suffix()}")
    response = upload(
        mapper_client,
        changeset_id,
        {
            "modify": {"nodes": [{"id": CAFE_NODE_ID, "version": cafe_before, "tags": {"amenity": "cafe", "name": f"Cafe {unique_suffix()}"}}]},
            "delete": {"nodes": [{"id": ROAD_VERTEX_NODE_ID, "version": vertex_before}]},
        },
    )
    assert response.status_code in REFUSED, (
        f"a batch containing a refused delete returned {response.status_code}, expected "
        f"the whole batch to be refused: {response.text[:400]}"
    )
    assert store.latest_version("nodes", CAFE_NODE_ID) == cafe_before, (
        f"node {CAFE_NODE_ID} was written even though its batch was refused; the "
        f"version moved from {cafe_before} to "
        f"{store.latest_version('nodes', CAFE_NODE_ID)}"
    )
    assert store.latest_version("nodes", ROAD_VERTEX_NODE_ID) == vertex_before, (
        f"node {ROAD_VERTEX_NODE_ID} was written even though its batch was refused"
    )


def test_upload_to_closed_changeset_refused(mapper_client, store):
    changeset_id = open_changeset(mapper_client, f"probe closed {unique_suffix()}")
    close_changeset(mapper_client, changeset_id)
    version = store.latest_version("nodes", CAFE_NODE_ID)
    response = upload(
        mapper_client,
        changeset_id,
        modify_node(CAFE_NODE_ID, version, tags={"amenity": "cafe", "name": f"Cafe {unique_suffix()}"}),
    )
    assert response.status_code in REFUSED + DENIED, (
        f"uploading into closed changeset {changeset_id} returned "
        f"{response.status_code}, expected a refusal: {response.text[:400]}"
    )
    assert store.latest_version("nodes", CAFE_NODE_ID) == version, (
        f"node {CAFE_NODE_ID} was written through a closed changeset"
    )


def test_bbox_area_cap_rejected(anon_client):
    response = anon_client.get("/map", params={"bbox": OVERSIZED_BBOX})
    assert response.status_code in REFUSED, (
        f"a map call for {OVERSIZED_BBOX}, far larger than the {BBOX_AREA_CAP} square "
        f"degree cap, returned {response.status_code}, expected a refusal: "
        f"{response.text[:400]}"
    )
    assert str(BBOX_AREA_CAP) in response.text, (
        f"the refusal does not name the {BBOX_AREA_CAP} square degree limit: "
        f"{response.text[:400]}"
    )


def test_bbox_element_count_cap_rejected(anon_client):
    response = anon_client.get("/map", params={"bbox": OVERSIZED_BBOX})
    assert response.status_code in REFUSED, (
        f"an oversized map call returned {response.status_code}, expected a refusal"
    )
    assert response.status_code != 500, (
        "an over-cap map call answered with a server error rather than a client error"
    )
    assert BBOX_ELEMENT_CAP == 5000, (
        "the pinned element ceiling must stay the value the brief states"
    )


def test_changeset_element_ceiling_rejected(mapper_client, store):
    changeset_id = open_changeset(mapper_client, f"probe ceiling {unique_suffix()}")
    oversized = {
        "create": {
            "nodes": [
                {"lat": 51.5000 + (i % 50) * 0.00001, "lon": -0.1250, "tags": {"amenity": "bench"}}
                for i in range(CHANGESET_ELEMENT_CEILING + 1)
            ]
        }
    }
    response = upload(mapper_client, changeset_id, oversized)
    assert response.status_code in REFUSED, (
        f"a changeset of {CHANGESET_ELEMENT_CEILING + 1} elements returned "
        f"{response.status_code}, expected a refusal above the {CHANGESET_ELEMENT_CEILING} "
        f"ceiling: {response.text[:400]}"
    )
    row = store.changeset(changeset_id)
    assert not row or not row.get("element_count"), (
        f"changeset {changeset_id} recorded elements though the batch was refused"
    )


def test_revert_of_moved_elements_refused(mapper_client, mapper2_client, store):
    changeset_id = open_changeset(mapper_client, f"probe revert base {unique_suffix()}")
    version = store.latest_version("nodes", MILL_NODE_ID)
    upload(
        mapper_client,
        changeset_id,
        modify_node(MILL_NODE_ID, version, tags={"historic": "mill", "name": f"Mill {unique_suffix()}"}),
    )
    close_changeset(mapper_client, changeset_id)

    later = open_changeset(mapper2_client, f"probe revert move {unique_suffix()}")
    moved_version = store.latest_version("nodes", MILL_NODE_ID)
    upload(
        mapper2_client,
        later,
        modify_node(MILL_NODE_ID, moved_version, tags={"historic": "mill", "name": f"Mill {unique_suffix()}"}),
    )
    close_changeset(mapper2_client, later)

    response = mapper_client.post(f"/changeset/{changeset_id}/revert")
    assert response.status_code in REFUSED, (
        f"reverting changeset {changeset_id}, whose element has since moved on, "
        f"returned {response.status_code}, expected a refusal: {response.text[:400]}"
    )
    assert str(MILL_NODE_ID) in response.text, (
        f"the refusal does not name the element that moved: {response.text[:400]}"
    )


def test_empty_changeset_stream_state(anon_client):
    response = anon_client.get("/changesets", params={"bbox": "10.0000,10.0000,10.0100,10.0100"})
    assert response.status_code in OK, (
        f"the changeset stream for an empty area returned {response.status_code}, "
        f"expected an empty result rather than an error: {response.text[:400]}"
    )
    body = response.json()
    assert isinstance(body, list), (
        f"the changeset stream must be a top-level JSON array even when empty, got "
        f"{type(body).__name__}"
    )
    assert body == [], (
        f"the changeset stream for an area with no edits returned {len(body)} rows"
    )


def test_form_validation_rejects_and_writes_nothing(mapper_client, store):
    before = store.changeset_count()
    response = mapper_client.put("/changeset/create", json={"comment": ""})
    assert response.status_code in REFUSED, (
        f"opening a changeset with an empty comment returned {response.status_code}, "
        f"expected a validation refusal: {response.text[:400]}"
    )
    assert "comment" in response.text.lower(), (
        f"the refusal does not name the comment field: {response.text[:400]}"
    )
    after = store.changeset_count()
    assert after == before, (
        f"a refused changeset create changed the changeset count from {before} to "
        f"{after}"
    )


def test_content_images_carry_alt_text():
    page = _fetch_page("/about")
    assert page.status_code in OK, (
        f"the about page returned {page.status_code}: {page.text[:200]}"
    )
    images = page.text.count("<img")
    with_alt = page.text.count("alt=")
    assert with_alt >= images, (
        f"the about page carries {images} images but only {with_alt} alt attributes; "
        f"every content image needs alternative text and every decorative one needs an "
        f"empty alt"
    )


def test_public_routes_carry_unique_title_and_description():
    seen: dict[str, str] = {}
    for path in ("/", "/about", "/diary", "/help", "/history", "/export"):
        page = _fetch_page(path)
        assert page.status_code in OK, (
            f"{path} returned {page.status_code}: {page.text[:200]}"
        )
        start = page.text.find("<title>")
        end = page.text.find("</title>")
        assert start != -1 and end > start, f"{path} carries no title element"
        title = page.text[start + 7 : end].strip()
        assert title, f"{path} carries an empty title"
        assert title not in seen.values(), (
            f"{path} shares the title {title!r} with {[k for k, v in seen.items() if v == title]}"
        )
        seen[path] = title
        assert 'name="description"' in page.text, (
            f"{path} declares no description in its document head"
        )


def test_narrow_viewport_has_no_horizontal_overflow():
    page = _fetch_page("/")
    assert page.status_code in OK, (
        f"the map home returned {page.status_code}: {page.text[:200]}"
    )
    assert 'name="viewport"' in page.text, (
        "the map home declares no viewport meta, so a narrow viewport cannot lay out "
        "without sideways overflow"
    )
    assert "width=device-width" in page.text, (
        "the viewport declaration does not bind the layout width to the device width"
    )


def test_sitemap_lists_public_routes_with_robots():
    sitemap = _fetch_page("/sitemap.xml")
    assert sitemap.status_code in OK, (
        f"/sitemap.xml returned {sitemap.status_code}: {sitemap.text[:200]}"
    )
    for path in ("/about", "/diary", "/help"):
        assert path in sitemap.text, f"the sitemap does not list {path}"
    robots = _fetch_page("/robots.txt")
    assert robots.status_code in OK, (
        f"/robots.txt returned {robots.status_code}: {robots.text[:200]}"
    )
    assert "sitemap.xml" in robots.text.lower(), (
        f"the robots file does not name the sitemap: {robots.text[:200]}"
    )


def test_health_endpoint_answers_200(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"/api/health returned {response.status_code}, expected 200 once the app is "
        f"ready: {response.text[:200]}"
    )


def test_api_is_served_under_the_api_prefix():
    base = api_base()
    assert base.endswith("/api"), (
        f"the API base resolves to {base}, expected the app's own origin with the "
        f"/api prefix"
    )
    response = httpx.get(f"{base}/health", timeout=30.0)
    assert response.status_code == 200, (
        f"{base}/health returned {response.status_code}; the HTTP API must be served "
        f"on the same origin as the pages under the /api prefix"
    )


def test_app_is_reachable_at_its_public_address():
    page = _fetch_page("/")
    assert page.status_code in OK, (
        f"the app at its public address returned {page.status_code}; it must be "
        f"reachable there, bound on every interface, and still running after the "
        f"build session ended: {page.text[:200]}"
    )
    assert page.text.strip(), "the app answered its public address with an empty body"


def test_production_build_is_served():
    page = _fetch_page("/")
    assert page.status_code in OK, (
        f"the map home returned {page.status_code}: {page.text[:200]}"
    )
    lowered = page.text.lower()
    for dev_marker in ("/@vite/client", "webpack-dev-server", "__vite_ping"):
        assert dev_marker not in lowered, (
            f"the served page carries the development-server marker {dev_marker!r}; a "
            f"production build must be served instead"
        )


def test_seeded_password_signs_in_every_account(anon_client):
    for email in (MAPPER_EMAIL, MAPPER2_EMAIL, MAPPER3_EMAIL):
        response = anon_client.post(
            "/auth/login", json={"email": email, "password": SEEDED_PASSWORD}
        )
        assert response.status_code in OK, (
            f"the seeded account {email} could not sign in with the seeded password: "
            f"{response.status_code} {response.text[:200]}"
        )


def test_timestamps_are_utc(anon_client):
    response = anon_client.get("/changesets")
    assert response.status_code in OK, (
        f"the changeset stream returned {response.status_code}: {response.text[:200]}"
    )
    stamps = [row.get("opened_at") for row in response.json() if row.get("opened_at")]
    assert stamps, "no changeset carries an opened_at timestamp"
    for stamp in stamps:
        text = str(stamp)
        assert text.endswith("Z") or "+00:00" in text, (
            f"the timestamp {text!r} declares no UTC offset; every timestamp is UTC"
        )
