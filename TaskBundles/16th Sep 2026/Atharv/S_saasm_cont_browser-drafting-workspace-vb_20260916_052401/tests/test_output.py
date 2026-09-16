from __future__ import annotations

import hashlib
import re
from concurrent.futures import ThreadPoolExecutor

import httpx

import appclient
from conftest import (
    ARCHITECTURAL_LAYERS,
    DENSE_DRAWING,
    DENSE_ENTITIES,
    DENSE_LAYERS,
    COLOUR_BYLAYER,
    DENIED,
    DOCUMENT_TITLE,
    DRAFTER_EMAIL,
    DRAFTER_NAME,
    EXCHANGE_EXTENSION,
    HEALTH_ENDPOINT,
    LIBRARY_ROUTE,
    LOGIN_ROUTE,
    OK,
    PRIVACY_ROUTE,
    PUBLIC_ROUTES,
    REFUSED,
    REVIEWER_EMAIL,
    REVIEWER_NAME,
    ROBOTS_ROUTE,
    ROLE_DRAFTER,
    SECOND_DRAFTER_EMAIL,
    SECOND_OWNER_DRAWING,
    SEEDED_PASSWORD,
    SHARED_DRAWING,
    SIGNUP_ROUTE,
    SITEMAP_ROUTE,
    TERMS_ROUTE,
    UNSHARED_DRAWING,
    WALLS_LAYER,
    app_url,
    body,
    entities_of,
    find_drawing,
    highest_version,
    layer_named,
    layers_of,
    new_drawing,
    new_layer,
    new_line,
    page,
    probe_email,
    probe_name,
    require_drawing,
    save_version,
    settle,
    versions_of,
)

def test_health_route_returns_ok():
    response = httpx.get(f"{app_url()}{HEALTH_ENDPOINT}", timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"GET {HEALTH_ENDPOINT} returned {response.status_code}, expected 200 once "
        f"the app is ready: {body(response)}"
    )


def test_document_title_matches_pinned_copy():
    response = page(LOGIN_ROUTE)
    assert response.status_code in OK, (
        f"GET {LOGIN_ROUTE} returned {response.status_code}: {body(response)}"
    )
    assert DOCUMENT_TITLE in response.text, (
        f"the document served at {LOGIN_ROUTE} does not carry the pinned title "
        f"{DOCUMENT_TITLE!r}; head excerpt: {response.text[:400]}"
    )


def test_signup_persists_drafter_account_row(anonymous):
    email = probe_email("signup")
    response = anonymous.post(
        "/auth/signup",
        json={"email": email, "password": SEEDED_PASSWORD,
              "display_name": probe_name("signup")},
    )
    assert response.status_code in OK, (
        f"POST /api/auth/signup for {email} returned {response.status_code}, "
        f"expected the account to be created: {body(response)}"
    )
    token = appclient.login(email, SEEDED_PASSWORD)
    with appclient.client(token) as signed_in:
        me = signed_in.get("/auth/me")
        assert me.status_code in OK, (
            f"GET /api/auth/me after signup returned {me.status_code}: {body(me)}"
        )
        payload = me.json()
        assert str(payload.get("role")) == ROLE_DRAFTER, (
            f"signup at {email} produced role {payload.get('role')!r}; every signup "
            f"creates a {ROLE_DRAFTER!r}: {body(me)}"
        )
        assert "password_hash" not in payload, (
            f"GET /api/auth/me returned a password hash, which no endpoint may "
            f"return: {body(me)}"
        )


def test_login_returns_bearer_token(anonymous):
    response = anonymous.post(
        "/auth/login", json={"email": DRAFTER_EMAIL, "password": SEEDED_PASSWORD})
    assert response.status_code in OK, (
        f"POST /api/auth/login for the seeded {DRAFTER_EMAIL} returned "
        f"{response.status_code}: {body(response)}"
    )
    token = response.json().get("access_token")
    assert token, (
        f"POST /api/auth/login returned no access_token for {DRAFTER_EMAIL}: "
        f"{body(response)}"
    )
    with appclient.client(token) as signed_in:
        me = signed_in.get("/auth/me")
        assert me.status_code in OK, (
            f"the token returned by login was refused at GET /api/auth/me with "
            f"{me.status_code}: {body(me)}"
        )
        assert str(me.json().get("display_name")) == DRAFTER_NAME, (
            f"GET /api/auth/me for {DRAFTER_EMAIL} named "
            f"{me.json().get('display_name')!r}, expected {DRAFTER_NAME!r}: {body(me)}"
        )


def test_library_lists_reachable_drawings_newest_first(drafter):
    import _shapes

    response = drafter.get("/drawings")
    assert response.status_code in OK, (
        f"GET /api/drawings returned {response.status_code}: {body(response)}"
    )
    rows = _shapes.items(response.json())
    names = [str(r.get("name", "")).strip() for r in rows]
    assert UNSHARED_DRAWING in names, (
        f"the seeded {UNSHARED_DRAWING!r} is absent from {DRAFTER_EMAIL}'s library; "
        f"the library returned {names}"
    )
    assert SHARED_DRAWING in names, (
        f"the seeded {SHARED_DRAWING!r} is absent from {DRAFTER_EMAIL}'s library; "
        f"the library returned {names}"
    )
    assert SECOND_OWNER_DRAWING not in names, (
        f"{SECOND_OWNER_DRAWING!r} belongs to {SECOND_DRAFTER_EMAIL} and was never "
        f"shared, yet it reached {DRAFTER_EMAIL}'s library: {names}"
    )
    stamps = [str(r.get("updated_at") or r.get("created_at") or "") for r in rows]
    assert stamps == sorted(stamps, reverse=True), (
        f"GET /api/drawings is not ordered newest first; the change times came back "
        f"as {stamps}"
    )


def test_created_drawing_row_carries_template_layers(drafter):
    created = new_drawing(drafter, probe_name("plan"), "millimeters", "architectural")
    assert created.status_code in OK, (
        f"POST /api/drawings for an architectural drawing returned "
        f"{created.status_code}: {body(created)}"
    )
    drawing_id = created.json().get("id")
    assert drawing_id is not None, (
        f"POST /api/drawings returned no id: {body(created)}"
    )
    names = {str(r.get("name", "")).strip() for r in layers_of(drafter, drawing_id)}
    missing = [n for n in ARCHITECTURAL_LAYERS if n not in names]
    assert not missing, (
        f"a drawing created from the architectural template is missing the layers "
        f"{missing}; GET /api/drawings/{drawing_id}/layers returned {sorted(names)}"
    )


def test_entity_created_on_layer_is_persisted(drafter):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    walls = layer_named(drafter, drawing_id, WALLS_LAYER)
    assert walls is not None, (
        f"the seeded layer {WALLS_LAYER!r} is absent from {UNSHARED_DRAWING!r}; "
        f"the layer list returned "
        f"{[r.get('name') for r in layers_of(drafter, drawing_id)]}"
    )
    created = new_line(drafter, drawing_id, walls["id"], (0, 0), (2500, 0))
    assert created.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/entities returned {created.status_code}: "
        f"{body(created)}"
    )
    entity_id = created.json().get("id")
    stored = [e for e in entities_of(drafter, drawing_id)
              if str(e.get("id")) == str(entity_id)]
    assert stored, (
        f"the entity created at POST /api/drawings/{drawing_id}/entities is absent "
        f"from a later GET of the same collection"
    )
    assert str(stored[0].get("layer_id")) == str(walls["id"]), (
        f"the stored entity sits on layer {stored[0].get('layer_id')!r}, expected "
        f"the {WALLS_LAYER!r} layer {walls['id']!r}"
    )


def test_layer_row_stores_colour_index(drafter):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    name = probe_name("layer")
    created = new_layer(drafter, drawing_id, name, colour_index=3)
    assert created.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/layers for {name!r} returned "
        f"{created.status_code}: {body(created)}"
    )
    stored = layer_named(drafter, drawing_id, name)
    assert stored is not None, (
        f"the layer {name!r} was accepted but is absent from a later "
        f"GET /api/drawings/{drawing_id}/layers"
    )
    assert int(stored.get("color_index")) == 3, (
        f"layer {name!r} came back at colour index {stored.get('color_index')!r}, "
        f"expected 3"
    )


def test_entity_colour_follows_layer_when_unset(drafter):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    name = probe_name("inherit")
    created_layer = new_layer(drafter, drawing_id, name, colour_index=3)
    assert created_layer.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/layers returned "
        f"{created_layer.status_code}: {body(created_layer)}"
    )
    layer_id = created_layer.json()["id"]
    created = new_line(drafter, drawing_id, layer_id, (0, 0), (100, 0),
                       colour_index=None)
    assert created.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/entities with no colour index returned "
        f"{created.status_code}: {body(created)}"
    )
    entity_id = created.json()["id"]
    recolour = drafter.patch(f"/drawings/{drawing_id}/layers/{layer_id}",
                             json={"color_index": 6})
    assert recolour.status_code in OK, (
        f"PATCH /api/drawings/{drawing_id}/layers/{layer_id} returned "
        f"{recolour.status_code}: {body(recolour)}"
    )
    stored = [e for e in entities_of(drafter, drawing_id)
              if str(e.get("id")) == str(entity_id)]
    assert stored, f"the entity {entity_id!r} disappeared after its layer was recoloured"
    raw = stored[0].get("color_index")
    assert raw is None or str(raw).upper() == COLOUR_BYLAYER, (
        f"the entity stored a resolved colour {raw!r} instead of leaving it unset, so "
        f"it no longer follows its layer"
    )
    effective = stored[0].get("effective_color_index", stored[0].get("resolved_color_index"))
    if effective is not None:
        assert int(effective) == 6, (
            f"the entity reports an effective colour of {effective!r} after its layer "
            f"moved to colour index 6"
        )


def test_coordinates_round_trip_without_rounding(drafter):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    walls = layer_named(drafter, drawing_id, WALLS_LAYER)
    fine, far = 0.125, 1450000.5
    created = new_line(drafter, drawing_id, walls["id"], (fine, fine), (far, far))
    assert created.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/entities returned {created.status_code}: "
        f"{body(created)}"
    )
    entity_id = created.json()["id"]
    stored = [e for e in entities_of(drafter, drawing_id)
              if str(e.get("id")) == str(entity_id)]
    assert stored, f"the entity {entity_id!r} is absent from a later entity read"
    points = stored[0].get("points") or []
    assert len(points) == 2, (
        f"the stored entity carries {len(points)} coordinates, expected the two it "
        f"was written with: {points}"
    )
    assert float(points[0]["x"]) == fine and float(points[0]["y"]) == fine, (
        f"a coordinate written at {fine} came back as {points[0]}, so it was rounded "
        f"on write"
    )
    assert float(points[1]["x"]) == far and float(points[1]["y"]) == far, (
        f"a coordinate written at {far} came back as {points[1]}, so precision was "
        f"lost far from the origin"
    )


def test_dimension_measurement_follows_moved_geometry(drafter):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    walls = layer_named(drafter, drawing_id, WALLS_LAYER)
    line = new_line(drafter, drawing_id, walls["id"], (0, 0), (1000, 0))
    assert line.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/entities returned {line.status_code}: "
        f"{body(line)}"
    )
    line_id = line.json()["id"]
    dimension = drafter.post(
        f"/drawings/{drawing_id}/entities",
        json={"layer_id": walls["id"], "kind": "dimension",
              "points": [{"x": 0, "y": -200}, {"x": 1000, "y": -200}],
              "color_index": None, "linetype": "continuous", "lineweight": -1,
              "properties": {"measures": line_id}},
    )
    assert dimension.status_code in OK, (
        f"creating a dimension measuring entity {line_id!r} returned "
        f"{dimension.status_code}: {body(dimension)}"
    )
    dimension_id = dimension.json()["id"]

    def measured():
        for e in entities_of(drafter, drawing_id):
            if str(e.get("id")) == str(dimension_id):
                props = e.get("properties") or {}
                return props.get("measured_value", e.get("measured_value"))
        return None

    before = settle(lambda: measured() is not None and measured())
    assert before is not None, (
        f"the dimension {dimension_id!r} reports no measured value, so nothing "
        f"records the length it claims to measure"
    )
    moved = drafter.patch(
        f"/drawings/{drawing_id}/entities/{line_id}",
        json={"points": [{"x": 0, "y": 0}, {"x": 2000, "y": 0}]},
    )
    assert moved.status_code in OK, (
        f"PATCH /api/drawings/{drawing_id}/entities/{line_id} returned "
        f"{moved.status_code}: {body(moved)}"
    )
    after = settle(lambda: measured() not in (None, before) and measured())
    assert after is not None and float(after) != float(before), (
        f"the dimension still reports {before!r} after the entity it measures was "
        f"lengthened from 1000 to 2000, so its stored measurement went stale"
    )


def test_restore_writes_new_highest_version(drafter):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    before = versions_of(drafter, drawing_id)
    assert before, (
        f"the seeded {UNSHARED_DRAWING!r} reports no versions, so there is nothing "
        f"to restore"
    )
    target = min(int(r["number"]) for r in before)
    top_before = highest_version(drafter, drawing_id)
    response = drafter.post(f"/drawings/{drawing_id}/versions/{target}/restore")
    assert response.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/versions/{target}/restore returned "
        f"{response.status_code}: {body(response)}"
    )
    after = versions_of(drafter, drawing_id)
    assert highest_version(drafter, drawing_id) == top_before + 1, (
        f"restoring version {target} did not write a new highest version; the "
        f"numbers went from {top_before} to {highest_version(drafter, drawing_id)}"
    )
    original = [r for r in before if int(r["number"]) == target][0]
    restored_row = [r for r in after if int(r["number"]) == target][0]
    assert restored_row.get("byte_digest") == original.get("byte_digest"), (
        f"version {target} was rewritten by the restore: its digest moved from "
        f"{original.get('byte_digest')!r} to {restored_row.get('byte_digest')!r}"
    )


def test_share_invitation_reaches_invitee_library(drafter, reviewer):
    drawing = require_drawing(drafter, SHARED_DRAWING)
    drawing_id = drawing["id"]
    response = drafter.post(f"/drawings/{drawing_id}/shares",
                            json={"email": REVIEWER_EMAIL, "access": "comment"})
    assert response.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/shares inviting {REVIEWER_EMAIL} at comment "
        f"returned {response.status_code}: {body(response)}"
    )
    found = settle(lambda: find_drawing(reviewer, SHARED_DRAWING))
    assert found is not None, (
        f"{SHARED_DRAWING!r} was shared with {REVIEWER_EMAIL} but never appeared in "
        f"that account's library"
    )
    import _shapes

    shares = _shapes.items(drafter.get(f"/drawings/{drawing_id}/shares").json())
    for_reviewer = [s for s in shares
                    if str(s.get("email", "")).lower() == REVIEWER_EMAIL]
    assert len(for_reviewer) == 1, (
        f"inviting {REVIEWER_EMAIL} a second time produced {len(for_reviewer)} share "
        f"rows; re-inviting changes the access rather than adding a row: {shares}"
    )
    share_id = for_reviewer[0]["id"]
    removed = drafter.delete(f"/drawings/{drawing_id}/shares/{share_id}")
    assert removed.status_code in OK, (
        f"DELETE /api/drawings/{drawing_id}/shares/{share_id} returned "
        f"{removed.status_code}; the owner removes an access: {body(removed)}"
    )
    left = _shapes.items(drafter.get(f"/drawings/{drawing_id}/shares").json())
    assert not [s for s in left
                if str(s.get("email", "")).lower() == REVIEWER_EMAIL], (
        f"the share for {REVIEWER_EMAIL} survives its removal: {left}"
    )
    restored = drafter.post(f"/drawings/{drawing_id}/shares",
                            json={"email": REVIEWER_EMAIL, "access": "comment"})
    assert restored.status_code in OK, (
        f"re-inviting {REVIEWER_EMAIL} after removal returned "
        f"{restored.status_code}: {body(restored)}"
    )


def test_comment_thread_persisted_with_anchor_point(reviewer):
    import _shapes

    drawing = require_drawing(reviewer, SHARED_DRAWING)
    drawing_id = drawing["id"]
    marker = probe_name("note")
    response = reviewer.post(
        f"/drawings/{drawing_id}/comments",
        json={"parent_id": None, "anchor_x": 1250.5, "anchor_y": -430.25,
              "body": marker},
    )
    assert response.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/comments from the reviewer returned "
        f"{response.status_code}: {body(response)}"
    )
    root_id = response.json().get("id")
    threads = _shapes.items(reviewer.get(f"/drawings/{drawing_id}/comments").json())
    flat = " ".join(_shapes.flatten(t) for t in threads)
    assert marker in flat, (
        f"the comment {marker!r} is absent from GET /api/drawings/{drawing_id}/comments"
    )
    assert "1250.5" in flat and "-430.25" in flat, (
        f"the comment came back without the point it was pinned to; the thread list "
        f"reads {flat[:400]}"
    )
    reply_marker = probe_name("reply")
    reply = reviewer.post(
        f"/drawings/{drawing_id}/comments",
        json={"parent_id": root_id, "anchor_x": 1250.5, "anchor_y": -430.25,
              "body": reply_marker},
    )
    assert reply.status_code in OK, (
        f"replying to comment {root_id!r} returned {reply.status_code}; a thread "
        f"carries replies: {body(reply)}"
    )
    resolved = reviewer.post(f"/drawings/{drawing_id}/comments/{root_id}/resolve")
    assert resolved.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/comments/{root_id}/resolve returned "
        f"{resolved.status_code}: {body(resolved)}"
    )
    after = _shapes.items(reviewer.get(f"/drawings/{drawing_id}/comments").json())
    after_flat = " ".join(_shapes.flatten(t) for t in after)
    assert reply_marker in after_flat, (
        f"the reply {reply_marker!r} is absent from the thread after it was written"
    )
    root = [t for t in after if str(t.get("id")) == str(root_id)]
    assert root and root[0].get("resolved") is True, (
        f"comment {root_id!r} does not report resolved after the resolve call; the "
        f"thread list reads {after_flat[:400]}"
    )


def test_presence_lists_accounts_in_the_drawing(drafter, reviewer):
    import _shapes

    drawing = require_drawing(drafter, SHARED_DRAWING)
    drawing_id = drawing["id"]
    for client in (drafter, reviewer):
        beat = client.post(f"/drawings/{drawing_id}/presence")
        assert beat.status_code in OK, (
            f"POST /api/drawings/{drawing_id}/presence returned {beat.status_code}: "
            f"{body(beat)}"
        )
    present = settle(
        lambda: [p for p in _shapes.items(
            drafter.get(f"/drawings/{drawing_id}/presence").json())] or None)
    assert present, (
        f"GET /api/drawings/{drawing_id}/presence is empty after two accounts "
        f"refreshed their presence"
    )
    flat = " ".join(_shapes.flatten(p) for p in present)
    assert DRAFTER_NAME in flat, (
        f"presence does not name {DRAFTER_NAME!r} after that account refreshed it; "
        f"the list reads {flat[:400]}"
    )
    assert REVIEWER_NAME in flat, (
        f"presence does not name {REVIEWER_NAME!r} after that account refreshed it; "
        f"the list reads {flat[:400]}"
    )


def test_saved_version_file_stored_at_key_scheme(drafter, store):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    base = highest_version(drafter, drawing_id)
    response = save_version(drafter, drawing_id, base, "Setting out")
    assert response.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/versions from base {base} returned "
        f"{response.status_code}: {body(response)}"
    )
    saved = response.json()
    key = saved.get("object_key")
    digest = saved.get("byte_digest")
    number = saved.get("number")
    assert key and digest and number is not None, (
        f"the created version reported object_key={key!r}, byte_digest={digest!r}, "
        f"number={number!r}; all three are recorded on a version: {body(response)}"
    )
    expected = f"drawings/{drawing_id}/v{number}/{digest}{EXCHANGE_EXTENSION}"
    assert key == expected, (
        f"the version stored its bytes at {key!r}; the pinned scheme produces "
        f"{expected!r}"
    )
    found = settle(lambda: store.exists(key))
    assert found, (
        f"no object exists in the bucket at {key!r}, so the saved version's bytes "
        f"never reached the store; the bucket holds "
        f"{store.list(f'drawings/{drawing_id}/')[:10]}"
    )


def test_version_download_bytes_match_recorded_digest(drafter):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    base = highest_version(drafter, drawing_id)
    saved = save_version(drafter, drawing_id, base, "Digest probe")
    assert saved.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/versions returned {saved.status_code}: "
        f"{body(saved)}"
    )
    number = saved.json()["number"]
    digest = saved.json()["byte_digest"]
    download = drafter.get(f"/drawings/{drawing_id}/versions/{number}/download")
    assert download.status_code in OK, (
        f"GET /api/drawings/{drawing_id}/versions/{number}/download returned "
        f"{download.status_code}: {body(download)}"
    )
    payload = download.content
    assert hashlib.sha256(payload).hexdigest() == str(digest).lower(), (
        f"the downloaded bytes hash to {hashlib.sha256(payload).hexdigest()!r} but "
        f"the version recorded {digest!r}, so the download is not the stored object"
    )
    text = payload.decode("utf-8", errors="replace")
    assert text.startswith("DRAWING "), (
        f"the downloaded exchange document does not open on a DRAWING line: "
        f"{text[:200]!r}"
    )
    assert text.rstrip().endswith("END"), (
        f"the downloaded exchange document does not close on an END line: "
        f"{text[-200:]!r}"
    )
    assert "\nLAYER " in text, (
        f"the downloaded exchange document carries no LAYER line: {text[:400]!r}"
    )


def test_version_numbers_are_contiguous_from_one(drafter):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    save_version(drafter, drawing_id, highest_version(drafter, drawing_id), "Run on")
    numbers = sorted(int(r["number"]) for r in versions_of(drafter, drawing_id))
    assert numbers == list(range(1, len(numbers) + 1)), (
        f"the version numbers for drawing {drawing_id} are {numbers}; they run from 1 "
        f"upward in steps of one with no gap"
    )
    current = drafter.get(f"/drawings/{drawing_id}").json().get("current_version")
    assert int(current) == numbers[-1], (
        f"the drawing reports current_version {current!r} while its highest version "
        f"is {numbers[-1]}"
    )


def test_concurrent_saves_from_one_base_produce_one_winner(drafter_token):
    with appclient.client(drafter_token) as reader:
        drawing = require_drawing(reader, UNSHARED_DRAWING)
        drawing_id = drawing["id"]
        base = highest_version(reader, drawing_id)
        before = len(versions_of(reader, drawing_id))

    def attempt(label):
        with appclient.client(drafter_token) as writer:
            return save_version(writer, drawing_id, base, f"Race {label}")

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = [f.result() for f in [pool.submit(attempt, "a"),
                                        pool.submit(attempt, "b")]]
    accepted = [r for r in results if r.status_code in OK]
    refused = [r for r in results if r.status_code not in OK]
    assert len(accepted) == 1, (
        f"two saves naming base version {base} produced {len(accepted)} accepted "
        f"responses; exactly one wins. Statuses: "
        f"{[r.status_code for r in results]}, bodies: {[body(r) for r in results]}"
    )
    assert refused and refused[0].status_code in REFUSED + (401, 403), (
        f"the losing save returned {refused[0].status_code if refused else 'nothing'}, "
        f"expected a client error naming the version that now exists: "
        f"{body(refused[0]) if refused else ''}"
    )
    with appclient.client(drafter_token) as reader:
        after = len(versions_of(reader, drawing_id))
    assert after == before + 1, (
        f"the drawing gained {after - before} versions from two concurrent saves of "
        f"base {base}; exactly one is written"
    )


def test_refused_save_leaves_no_row_and_no_stored_file(drafter, store):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    top = highest_version(drafter, drawing_id)
    rows_before = len(versions_of(drafter, drawing_id))
    keys_before = set(store.list(f"drawings/{drawing_id}/"))
    stale = max(top - 1, 0)
    response = save_version(drafter, drawing_id, stale, "Stale base")
    assert response.status_code not in OK, (
        f"a save naming the stale base version {stale} while {top} exists was "
        f"accepted with {response.status_code}; it is refused: {body(response)}"
    )
    rows_after = len(versions_of(drafter, drawing_id))
    assert rows_after == rows_before, (
        f"the refused save wrote {rows_after - rows_before} version row(s); a refused "
        f"save writes none"
    )
    keys_after = set(store.list(f"drawings/{drawing_id}/"))
    assert keys_after == keys_before, (
        f"the refused save left {sorted(keys_after - keys_before)} in the bucket; a "
        f"refused save leaves no object"
    )


def test_undo_restores_every_dependent_entity(drafter):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    walls = layer_named(drafter, drawing_id, WALLS_LAYER)
    line = new_line(drafter, drawing_id, walls["id"], (0, 0), (900, 0))
    assert line.status_code in OK, (
        f"creating the measured entity returned {line.status_code}: {body(line)}"
    )
    line_id = line.json()["id"]
    dimension = drafter.post(
        f"/drawings/{drawing_id}/entities",
        json={"layer_id": walls["id"], "kind": "dimension",
              "points": [{"x": 0, "y": -150}, {"x": 900, "y": -150}],
              "color_index": None, "linetype": "continuous", "lineweight": -1,
              "properties": {"measures": line_id}},
    )
    assert dimension.status_code in OK, (
        f"creating the dependent dimension returned {dimension.status_code}: "
        f"{body(dimension)}"
    )
    dimension_id = dimension.json()["id"]

    def snapshot():
        out = {}
        for e in entities_of(drafter, drawing_id):
            if str(e.get("id")) in (str(line_id), str(dimension_id)):
                props = e.get("properties") or {}
                out[str(e["id"])] = (e.get("points"),
                                     props.get("measured_value",
                                               e.get("measured_value")))
        return out

    before = settle(lambda: snapshot() if len(snapshot()) == 2 else None)
    assert before and len(before) == 2, (
        f"the measured entity and its dimension are not both readable before the "
        f"undo; read back {before}"
    )
    moved = drafter.patch(
        f"/drawings/{drawing_id}/entities/{line_id}",
        json={"points": [{"x": 0, "y": 0}, {"x": 1800, "y": 0}]},
    )
    assert moved.status_code in OK, (
        f"PATCH on the measured entity returned {moved.status_code}: {body(moved)}"
    )
    undo = drafter.post(f"/drawings/{drawing_id}/undo")
    assert undo.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/undo returned {undo.status_code}: "
        f"{body(undo)}"
    )
    after = settle(lambda: snapshot() if snapshot() == before else None)
    assert after == before, (
        f"one undo did not restore both the moved entity and the dimension that "
        f"depends on it; before the move the pair read {before}, after the undo "
        f"{snapshot()}"
    )


def test_reseeding_does_not_duplicate_seeded_rows(drafter, backend):
    import _shapes

    names = [str(r.get("name", "")).strip() for r in
             _shapes.items(drafter.get("/drawings").json())]
    for seeded in (UNSHARED_DRAWING, SHARED_DRAWING):
        assert names.count(seeded) == 1, (
            f"the library carries {names.count(seeded)} rows named {seeded!r}; a "
            f"seeded drawing exists exactly once however often the seed runs"
        )
    for email in (DRAFTER_EMAIL, SECOND_DRAFTER_EMAIL, REVIEWER_EMAIL):
        count = backend.count("accounts", email=email)
        assert count == 1, (
            f"the accounts table holds {count} rows for {email!r}; seeding is "
            f"idempotent, so a restart writes no second copy"
        )
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    layer_names = [str(r.get("name", "")).strip()
                   for r in layers_of(drafter, drawing["id"])]
    for seeded_layer in ARCHITECTURAL_LAYERS:
        assert layer_names.count(seeded_layer) == 1, (
            f"{UNSHARED_DRAWING!r} carries {layer_names.count(seeded_layer)} layers "
            f"named {seeded_layer!r}; the seed writes one"
        )


def test_unauthenticated_request_is_denied(anonymous):
    for path in ("/drawings", "/auth/me"):
        response = anonymous.get(path)
        assert response.status_code in DENIED, (
            f"GET /api{path} with no bearer token returned {response.status_code}; "
            f"a protected endpoint denies an unauthenticated caller: {body(response)}"
        )
    created = anonymous.post("/drawings",
                             json={"name": probe_name("anon"),
                                   "units": "millimeters", "template": "blank"})
    assert created.status_code in DENIED, (
        f"POST /api/drawings with no bearer token returned {created.status_code}; "
        f"a write from an unauthenticated caller is denied: {body(created)}"
    )


def test_expired_token_is_denied():
    stale = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiIxIiwiZXhwIjoxMDAwMDAwMDAwfQ."
        "0000000000000000000000000000000000000000000"
    )
    with appclient.client(stale) as client:
        response = client.get("/drawings")
    assert response.status_code in DENIED, (
        f"GET /api/drawings with a token whose expiry is long past returned "
        f"{response.status_code}; an expired token is denied: {body(response)}"
    )


def test_reviewer_entity_write_is_denied_row_unchanged(reviewer, drafter):
    drawing = require_drawing(drafter, SHARED_DRAWING)
    drawing_id = drawing["id"]
    layers = layers_of(drafter, drawing_id)
    assert layers, f"{SHARED_DRAWING!r} reports no layers to draw onto"
    layer_id = layers[0]["id"]
    before = entities_of(drafter, drawing_id)
    response = new_line(reviewer, drawing_id, layer_id, (0, 0), (10, 10))
    assert response.status_code in DENIED, (
        f"POST /api/drawings/{drawing_id}/entities from the {REVIEWER_EMAIL} session "
        f"returned {response.status_code}; a reviewer never writes geometry, whatever "
        f"the share access says: {body(response)}"
    )
    after = entities_of(drafter, drawing_id)
    assert len(after) == len(before), (
        f"the reviewer's refused write changed the entity count from {len(before)} to "
        f"{len(after)}; a denial leaves the rows untouched"
    )
    if before:
        assert after[0] == before[0], (
            f"the reviewer's refused write altered a stored entity: {before[0]} "
            f"became {after[0]}"
        )


def test_reviewer_drawing_create_is_denied(reviewer, drafter):
    import _shapes

    before = len(_shapes.items(drafter.get("/drawings").json()))
    name = probe_name("reviewer")
    response = new_drawing(reviewer, name)
    assert response.status_code in DENIED, (
        f"POST /api/drawings from the {REVIEWER_EMAIL} session returned "
        f"{response.status_code}; a reviewer creates no drawing: {body(response)}"
    )
    assert find_drawing(reviewer, name) is None, (
        f"the drawing {name!r} exists in the reviewer's library after a refused "
        f"create call"
    )
    after = len(_shapes.items(drafter.get("/drawings").json()))
    assert after == before, (
        f"the refused create changed the drawing count from {before} to {after}"
    )


def test_unshared_drawing_is_denied_to_other_account(drafter, reviewer):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    for path in (f"/drawings/{drawing_id}",
                 f"/drawings/{drawing_id}/entities",
                 f"/drawings/{drawing_id}/layers",
                 f"/drawings/{drawing_id}/versions",
                 f"/drawings/{drawing_id}/comments",
                 f"/drawings/{drawing_id}/shares"):
        response = reviewer.get(path)
        assert response.status_code in DENIED, (
            f"GET /api{path} as {REVIEWER_EMAIL} returned {response.status_code}; "
            f"{UNSHARED_DRAWING!r} carries no share row, so every other account is "
            f"denied: {body(response)}"
        )
        assert UNSHARED_DRAWING not in response.text, (
            f"the refusal at /api{path} names {UNSHARED_DRAWING!r}, which confirms "
            f"the drawing exists: {body(response)}"
        )
    assert find_drawing(reviewer, UNSHARED_DRAWING) is None, (
        f"{UNSHARED_DRAWING!r} reached the {REVIEWER_EMAIL} library without a share"
    )


def test_unshared_drawing_file_is_denied_to_other_account(drafter, reviewer):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    numbers = [int(r["number"]) for r in versions_of(drafter, drawing_id)]
    assert numbers, (
        f"{UNSHARED_DRAWING!r} has no saved version, so there are no stored bytes to "
        f"protect"
    )
    for number in numbers[:3]:
        response = reviewer.get(f"/drawings/{drawing_id}/versions/{number}/download")
        assert response.status_code in DENIED, (
            f"GET /api/drawings/{drawing_id}/versions/{number}/download as "
            f"{REVIEWER_EMAIL} returned {response.status_code}; the stored bytes of "
            f"an unshared drawing are denied with the drawing: {body(response)}"
        )
        assert not response.content.startswith(b"DRAWING "), (
            f"the refused download returned an exchange document body: "
            f"{response.content[:200]!r}"
        )


def test_non_owner_share_write_is_denied(drafter, second_drafter):
    import _shapes

    drawing = require_drawing(drafter, SHARED_DRAWING)
    drawing_id = drawing["id"]
    before = _shapes.items(drafter.get(f"/drawings/{drawing_id}/shares").json())
    response = second_drafter.post(
        f"/drawings/{drawing_id}/shares",
        json={"email": SECOND_DRAFTER_EMAIL, "access": "edit"})
    assert response.status_code in DENIED, (
        f"POST /api/drawings/{drawing_id}/shares from {SECOND_DRAFTER_EMAIL}, who does "
        f"not own {SHARED_DRAWING!r}, returned {response.status_code}; only the owner "
        f"changes a share list: {body(response)}"
    )
    after = _shapes.items(drafter.get(f"/drawings/{drawing_id}/shares").json())
    assert len(after) == len(before), (
        f"the refused share write changed the share count from {len(before)} to "
        f"{len(after)}"
    )


def test_duplicate_layer_name_is_refused(drafter):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    before = len(layers_of(drafter, drawing_id))
    response = new_layer(drafter, drawing_id, WALLS_LAYER.lower(), colour_index=1)
    assert response.status_code in REFUSED, (
        f"POST /api/drawings/{drawing_id}/layers named {WALLS_LAYER.lower()!r} beside "
        f"the existing {WALLS_LAYER!r} returned {response.status_code}; a layer name "
        f"is unique within a drawing under case folding: {body(response)}"
    )
    assert "name" in response.text.lower(), (
        f"the refusal does not name the field at fault: {body(response)}"
    )
    after = len(layers_of(drafter, drawing_id))
    assert after == before, (
        f"the refused layer write changed the layer count from {before} to {after}"
    )


def test_empty_comment_body_is_refused(drafter):
    import _shapes

    drawing = require_drawing(drafter, SHARED_DRAWING)
    drawing_id = drawing["id"]
    before = len(_shapes.items(drafter.get(f"/drawings/{drawing_id}/comments").json()))
    response = drafter.post(
        f"/drawings/{drawing_id}/comments",
        json={"parent_id": None, "anchor_x": 10, "anchor_y": 10, "body": ""})
    assert response.status_code in REFUSED, (
        f"POST /api/drawings/{drawing_id}/comments with an empty body returned "
        f"{response.status_code}; an empty comment is refused: {body(response)}"
    )
    after = len(_shapes.items(drafter.get(f"/drawings/{drawing_id}/comments").json()))
    assert after == before, (
        f"the refused comment changed the thread count from {before} to {after}"
    )


def test_duplicate_signup_email_is_refused(anonymous, backend):
    email = probe_email("dup")
    first = anonymous.post("/auth/signup",
                           json={"email": email, "password": SEEDED_PASSWORD,
                                 "display_name": probe_name("dup")})
    assert first.status_code in OK, (
        f"the first POST /api/auth/signup for {email} returned {first.status_code}: "
        f"{body(first)}"
    )
    second = anonymous.post("/auth/signup",
                            json={"email": email, "password": SEEDED_PASSWORD,
                                  "display_name": probe_name("dup")})
    assert second.status_code in REFUSED, (
        f"the second POST /api/auth/signup for {email} returned {second.status_code}; "
        f"a repeated email is refused: {body(second)}"
    )
    count = backend.count("accounts", email=email)
    assert count == 1, (
        f"the accounts table holds {count} rows for {email!r} after a refused "
        f"duplicate signup; a refused signup writes nothing"
    )


def test_layer_delete_holding_entities_is_refused(drafter):
    drawing = require_drawing(drafter, UNSHARED_DRAWING)
    drawing_id = drawing["id"]
    name = probe_name("occupied")
    created = new_layer(drafter, drawing_id, name, colour_index=4)
    assert created.status_code in OK, (
        f"POST /api/drawings/{drawing_id}/layers returned {created.status_code}: "
        f"{body(created)}"
    )
    layer_id = created.json()["id"]
    placed = new_line(drafter, drawing_id, layer_id, (0, 0), (50, 50))
    assert placed.status_code in OK, (
        f"placing an entity on the new layer returned {placed.status_code}: "
        f"{body(placed)}"
    )
    response = drafter.delete(f"/drawings/{drawing_id}/layers/{layer_id}")
    assert response.status_code in REFUSED, (
        f"DELETE /api/drawings/{drawing_id}/layers/{layer_id} returned "
        f"{response.status_code} while the layer still holds an entity; the deletion "
        f"is refused: {body(response)}"
    )
    assert layer_named(drafter, drawing_id, name) is not None, (
        f"the layer {name!r} is gone after a refused deletion"
    )


def test_invite_to_unknown_email_is_refused(drafter):
    import _shapes

    drawing = require_drawing(drafter, SHARED_DRAWING)
    drawing_id = drawing["id"]
    before = len(_shapes.items(drafter.get(f"/drawings/{drawing_id}/shares").json()))
    unknown = probe_email("nobody")
    response = drafter.post(f"/drawings/{drawing_id}/shares",
                            json={"email": unknown, "access": "view"})
    assert response.status_code in REFUSED, (
        f"POST /api/drawings/{drawing_id}/shares inviting {unknown}, which has no "
        f"account, returned {response.status_code}; the invitation is refused: "
        f"{body(response)}"
    )
    after = len(_shapes.items(drafter.get(f"/drawings/{drawing_id}/shares").json()))
    assert after == before, (
        f"the refused invitation changed the share count from {before} to {after}"
    )


def test_privacy_page_linked_from_public_footer():
    served = page(PRIVACY_ROUTE)
    assert served.status_code in OK, (
        f"GET {PRIVACY_ROUTE} returned {served.status_code}: {body(served)}"
    )
    for route in (LOGIN_ROUTE, SIGNUP_ROUTE):
        document = page(route)
        assert document.status_code in OK, (
            f"GET {route} returned {document.status_code}: {body(document)}"
        )
        assert PRIVACY_ROUTE in document.text, (
            f"the page at {route} carries no link to {PRIVACY_ROUTE}; the privacy "
            f"page is reachable from the footer of every public page"
        )


def test_terms_page_linked_from_signup_form():
    served = page(TERMS_ROUTE)
    assert served.status_code in OK, (
        f"GET {TERMS_ROUTE} returned {served.status_code}: {body(served)}"
    )
    signup = page(SIGNUP_ROUTE)
    assert signup.status_code in OK, (
        f"GET {SIGNUP_ROUTE} returned {signup.status_code}: {body(signup)}"
    )
    assert TERMS_ROUTE in signup.text, (
        f"the signup form at {SIGNUP_ROUTE} carries no link to {TERMS_ROUTE}"
    )


def test_sitemap_lists_every_public_route():
    response = page(SITEMAP_ROUTE)
    assert response.status_code in OK, (
        f"GET {SITEMAP_ROUTE} returned {response.status_code}: {body(response)}"
    )
    missing = [r for r in (LOGIN_ROUTE, SIGNUP_ROUTE, PRIVACY_ROUTE, TERMS_ROUTE)
               if r not in response.text]
    assert not missing, (
        f"the sitemap at {SITEMAP_ROUTE} omits {missing}; it lists every public "
        f"route. Body excerpt: {response.text[:400]}"
    )


def test_robots_file_references_the_sitemap():
    response = page(ROBOTS_ROUTE)
    assert response.status_code in OK, (
        f"GET {ROBOTS_ROUTE} returned {response.status_code}: {body(response)}"
    )
    assert SITEMAP_ROUTE in response.text, (
        f"the robots file at {ROBOTS_ROUTE} does not name {SITEMAP_ROUTE}: "
        f"{response.text[:400]}"
    )
    assert re.search(r"(?im)^\s*sitemap\s*:\s*https?://", response.text), (
        f"the robots file names the sitemap without an absolute address: "
        f"{response.text[:400]}"
    )


def test_public_routes_declare_distinct_social_previews():
    title_re = re.compile(
        r"""<meta[^>]+(?:property|name)=["'](?:og:title|twitter:title)["'][^>]*"""
        r"""content=["']([^"']+)["']""", re.I)
    image_re = re.compile(
        r"""<meta[^>]+(?:property|name)=["'](?:og:image|twitter:image)["'][^>]*"""
        r"""content=["']([^"']+)["']""", re.I)
    seen = {}
    for route in PUBLIC_ROUTES:
        document = page(route)
        assert document.status_code in OK, (
            f"GET {route} returned {document.status_code}: {body(document)}"
        )
        titles = title_re.findall(document.text)
        images = image_re.findall(document.text)
        assert titles, (
            f"the public route {route} declares no social preview title: "
            f"{document.text[:400]}"
        )
        assert images, (
            f"the public route {route} declares no social preview image: "
            f"{document.text[:400]}"
        )
        pair = (titles[0].strip(), images[0].strip())
        assert pair not in seen, (
            f"{route} declares the same social preview pair as {seen[pair]}: {pair}"
        )
        seen[pair] = route
        target = images[0] if images[0].startswith("http") else f"{app_url()}{images[0]}"
        resolved = httpx.get(target, timeout=appclient.TIMEOUT,
                             follow_redirects=True)
        assert resolved.status_code in OK, (
            f"the social preview image {target} declared by {route} returned "
            f"{resolved.status_code}"
        )
        assert resolved.headers.get("content-type", "").startswith("image/"), (
            f"the social preview image {target} declared by {route} came back as "
            f"{resolved.headers.get('content-type')!r}, not an image"
        )


def test_dense_drawing_is_seeded_at_the_stated_bar(drafter):
    drawing = require_drawing(drafter, DENSE_DRAWING)
    drawing_id = drawing["id"]
    layers = layers_of(drafter, drawing_id)
    assert len(layers) == DENSE_LAYERS, (
        f"the density fixture {DENSE_DRAWING!r} carries {len(layers)} layers, "
        f"expected exactly {DENSE_LAYERS}; without it the responsiveness bar is a "
        f"figure no channel can observe"
    )
    entities = entities_of(drafter, drawing_id)
    assert len(entities) == DENSE_ENTITIES, (
        f"the density fixture {DENSE_DRAWING!r} carries {len(entities)} entities, "
        f"expected exactly {DENSE_ENTITIES}"
    )
    populated = {str(e.get("layer_id")) for e in entities}
    empty = [l for l in layers if str(l["id"]) not in populated]
    assert not empty, (
        f"{len(empty)} of the density fixture's layers hold no geometry "
        f"({[l.get('name') for l in empty][:5]}); every layer carries a share of "
        f"the drawing"
    )
