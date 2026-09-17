"""The one merged pytest module for deku/interactive-animation-studio.

Every assertion is black box: HTTP against the deployed app, rows through the
generic backend adapter, objects through the generic store adapter. Nothing
here reads the agent's source, imports a provider SDK, or assumes a framework.
"""

from __future__ import annotations

import concurrent.futures

from conftest import (
    CACHE_INTERVAL_SECONDS,
    CHANNEL_PUBLISHED,
    CHANNEL_SECOND,
    CORPUS_PASSWORD,
    CURSOR_HEADER,
    DENIED,
    DENIED_OR_MISSING,
    DOC_DRAFT,
    DOC_PUBLISHED,
    DOC_SECOND,
    DOCUMENT_KEY_SUFFIX,
    EDITOR3_EMAIL,
    EDITOR_EMAIL,
    FOLDER_BROADCAST,
    FOLDER_GAME_UI,
    FOLDER_PRODUCT_UI,
    HANDLE_RAE,
    LIKES_LOADER_RING,
    LIKES_MATCH_TICKER,
    OK,
    PAGE_SIZE,
    REFUSED,
    REVISION_KEY_PREFIX,
    SEAT_CAP,
    api,
    new_operation,
    poll_until,
    poster_keys,
    probe_email,
    probe_handle,
    revision_keys,
    seed_document_id,
    settle,
    unique_suffix,
)
from appclient import client, login


def test_health_endpoint_requires_no_credential(anon_client):
    r = anon_client.get(api("/health"))
    assert r.status_code == 200, (
        f"GET /api/health answered {r.status_code} without a credential; the App "
        f"Contract requires 200 once the app is ready"
    )


def test_login_returns_bearer_token_for_seeded_editor(anon_client):
    r = anon_client.post(api("/auth/login"),
                         json={"email": EDITOR_EMAIL, "password": CORPUS_PASSWORD})
    assert r.status_code in OK, (
        f"login as {EDITOR_EMAIL} with the pinned corpus password answered "
        f"{r.status_code}, body {r.text[:200]!r}"
    )
    body = r.json()
    assert body.get("token"), (
        f"login response carries no non-empty `token` field: keys {sorted(body)}"
    )


def test_unauthenticated_request_to_workspace_endpoint_denied(anon_client, studio):
    before = studio.count_documents()
    r = anon_client.post(api("/documents"),
                         json={"folder_id": 1, "name": f"Anon {unique_suffix()}"})
    assert r.status_code in DENIED_OR_MISSING, (
        f"an unauthenticated POST /api/documents answered {r.status_code}; a request "
        f"with no bearer token must be denied, not served"
    )
    assert studio.count_documents() == before, (
        f"an unauthenticated create changed the document row count from {before} to "
        f"{studio.count_documents()}"
    )


def test_viewer_create_document_denied_leaves_row_count_unchanged(viewer_client, studio):
    before = studio.count_documents()
    folder = studio.folder_by_name(FOLDER_BROADCAST)
    assert folder is not None, f"seed folder {FOLDER_BROADCAST!r} is missing"
    r = viewer_client.post(api("/documents"),
                           json={"folder_id": folder["id"],
                                 "name": f"Viewer {unique_suffix()}"})
    assert r.status_code in DENIED, (
        f"a viewer session POSTing /api/documents answered {r.status_code}; the role "
        f"cannot create, so the server must deny it"
    )
    after = studio.count_documents()
    assert after == before, (
        f"a denied viewer create still moved the document row count from {before} "
        f"to {after}; the protected state must be unchanged"
    )


def test_viewer_cannot_read_folder_names_off_granted_path(viewer_client):
    r = viewer_client.get(api("/folders"))
    assert r.status_code in OK, (
        f"GET /api/folders as the seeded viewer answered {r.status_code}"
    )
    names = {row.get("name") for row in r.json()}
    assert FOLDER_PRODUCT_UI not in names, (
        f"the viewer's folder list leaked {FOLDER_PRODUCT_UI!r}; the grant covers "
        f"{FOLDER_BROADCAST!r} alone, so no other folder name may appear. Saw {sorted(n for n in names if n)}"
    )
    assert FOLDER_GAME_UI not in names, (
        f"the viewer's folder list leaked {FOLDER_GAME_UI!r}; the grant covers "
        f"{FOLDER_BROADCAST!r} alone. Saw {sorted(n for n in names if n)}"
    )


def test_viewer_publish_denied_leaves_channel_build_unchanged(viewer_client, studio):
    document_id = seed_document_id(studio, DOC_PUBLISHED)
    before = studio.channel_by_slug(CHANNEL_PUBLISHED)
    assert before is not None, f"seed channel {CHANNEL_PUBLISHED!r} is missing"
    revisions = studio.revisions_for(document_id)
    assert revisions, f"{DOC_PUBLISHED!r} carries no revision to publish"
    r = viewer_client.post(api(f"/documents/{document_id}/publish"),
                           json={"revision_id": revisions[0]["id"],
                                 "channel_slug": CHANNEL_PUBLISHED,
                                 "title": DOC_PUBLISHED, "tags": ["ui"]})
    assert r.status_code in DENIED, (
        f"a viewer session publishing answered {r.status_code}; publishing is an "
        f"editor action and must be denied at the server"
    )
    after = studio.channel_by_slug(CHANNEL_PUBLISHED)
    assert after.get("current_build_id") == before.get("current_build_id"), (
        f"a denied viewer publish still moved the channel from build "
        f"{before.get('current_build_id')} to {after.get('current_build_id')}"
    )


def test_operation_seq_strictly_increases_per_document(editor_client, studio):
    document_id = seed_document_id(studio, DOC_DRAFT)
    seqs = []
    for index in range(3):
        r = editor_client.post(
            api(f"/documents/{document_id}/operations"),
            json=new_operation("node-alpha", "fill", f"value-{unique_suffix()}-{index}"))
        assert r.status_code in OK, (
            f"appending operation {index} answered {r.status_code}, body {r.text[:200]!r}"
        )
        seqs.append(r.json()["seq"])
    assert seqs == sorted(seqs), f"assigned sequences {seqs} are not increasing"
    assert len(set(seqs)) == len(seqs), f"assigned sequences {seqs} are not distinct"


def test_concurrent_operations_receive_distinct_seq_values(studio):
    document_id = seed_document_id(studio, DOC_DRAFT)
    token = login(EDITOR_EMAIL, CORPUS_PASSWORD)

    def append(index: int) -> int:
        with client(token) as c:
            r = c.post(api(f"/documents/{document_id}/operations"),
                       json=new_operation("node-beta", f"prop-{index}", index))
            assert r.status_code in OK, (
                f"concurrent append {index} answered {r.status_code}, "
                f"body {r.text[:200]!r}"
            )
            return r.json()["seq"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        seqs = list(pool.map(append, range(4)))
    assert len(set(seqs)) == 4, (
        f"four concurrent appends returned sequences {seqs}; every accepted "
        f"operation takes its own seq and none is lost"
    )


def test_same_property_conflict_resolves_to_higher_seq(editor_client, editor2_client, studio):
    document_id = seed_document_id(studio, DOC_DRAFT)
    target = f"node-{unique_suffix()}"
    first = editor_client.post(api(f"/documents/{document_id}/operations"),
                               json=new_operation(target, "opacity", 10))
    second = editor2_client.post(api(f"/documents/{document_id}/operations"),
                                 json=new_operation(target, "opacity", 90))
    assert first.status_code in OK and second.status_code in OK, (
        f"the two competing appends answered {first.status_code} and "
        f"{second.status_code}"
    )
    winner = max(first.json()["seq"], second.json()["seq"])
    read = editor_client.get(api(f"/documents/{document_id}/operations"),
                             params={"since": 0})
    assert read.status_code in OK, f"reading the log answered {read.status_code}"
    rows = [row for row in read.json() if row.get("target") == target
            and row.get("property") == "opacity"]
    applied = [row for row in rows if row.get("outcome") == "applied"]
    assert len(applied) == 1, (
        f"two operations on one property of {target!r} left {len(applied)} rows at "
        f"outcome 'applied'; exactly the higher seq wins"
    )
    assert applied[0]["seq"] == winner, (
        f"the surviving operation carries seq {applied[0]['seq']}, not the higher "
        f"seq {winner}"
    )
    superseded = [row for row in rows if row.get("outcome") == "superseded"]
    assert len(superseded) == 1, (
        f"the losing operation was not recorded 'superseded'; outcomes seen: "
        f"{[row.get('outcome') for row in rows]}"
    )


def test_discarded_operation_names_deleting_member(editor_client, editor2_client, studio):
    document_id = seed_document_id(studio, DOC_DRAFT)
    target = f"node-{unique_suffix()}"
    created = editor_client.post(api(f"/documents/{document_id}/operations"),
                                 json=new_operation(target, "fill", "#111111"))
    assert created.status_code in OK, f"creating the node answered {created.status_code}"
    deleted = editor_client.post(api(f"/documents/{document_id}/operations"),
                                 json=new_operation(target, "deleted", True))
    assert deleted.status_code in OK, f"deleting the node answered {deleted.status_code}"
    late = editor2_client.post(api(f"/documents/{document_id}/operations"),
                               json=new_operation(target, "fill", "#ff3b58"))
    assert late.status_code in OK, (
        f"an edit against a deleted node answered {late.status_code}; the operation "
        f"is recorded as discarded rather than refused"
    )
    body = late.json()
    assert body.get("outcome") == "discarded", (
        f"an edit against a deleted node carries outcome {body.get('outcome')!r}, "
        f"expected 'discarded'"
    )
    assert body.get("discarded_by"), (
        f"a discarded operation carries no `discarded_by`; the author must be told "
        f"who deleted the node. Body keys: {sorted(body)}"
    )


def test_duplicate_op_id_returns_original_seq_without_second_row(editor_client, studio):
    document_id = seed_document_id(studio, DOC_DRAFT)
    payload = new_operation(f"node-{unique_suffix()}", "rotation", 45)
    before = studio.count_operations(document_id)
    first = editor_client.post(api(f"/documents/{document_id}/operations"), json=payload)
    assert first.status_code in OK, f"the first append answered {first.status_code}"
    after_first = studio.count_operations(document_id)
    replay = editor_client.post(api(f"/documents/{document_id}/operations"), json=payload)
    assert replay.status_code in OK, (
        f"replaying a known op_id answered {replay.status_code}; a replay is a no-op, "
        f"not a rejection"
    )
    assert replay.json()["seq"] == first.json()["seq"], (
        f"the replay returned seq {replay.json()['seq']} instead of the original "
        f"{first.json()['seq']}"
    )
    after_replay = studio.count_operations(document_id)
    assert after_replay == after_first, (
        f"the replay wrote a second operation row: count moved {before} -> "
        f"{after_first} -> {after_replay}"
    )


def test_revision_content_hash_matches_stored_object_key(editor_client, studio, store):
    document_id = seed_document_id(studio, DOC_DRAFT)
    editor_client.post(api(f"/documents/{document_id}/operations"),
                       json=new_operation(f"node-{unique_suffix()}", "scale", 120))
    r = editor_client.post(api(f"/documents/{document_id}/revisions"),
                           json={"label": f"probe-{unique_suffix()}"})
    assert r.status_code in OK, (
        f"materialising a revision answered {r.status_code}, body {r.text[:200]!r}"
    )
    body = r.json()
    content_hash = body.get("content_hash", "")
    object_key = body.get("object_key", "")
    assert len(content_hash) == 64 and content_hash == content_hash.lower(), (
        f"content_hash {content_hash!r} is not a 64-character lowercase hex digest"
    )
    assert object_key == f"{REVISION_KEY_PREFIX}{document_id}/{content_hash}{DOCUMENT_KEY_SUFFIX}", (
        f"object_key {object_key!r} does not follow "
        f"documents/{{document_id}}/{{sha256_of_bytes}}.mot"
    )
    assert store.exists(object_key), (
        f"no object exists in the bucket at {object_key!r}; the revision bytes must "
        f"live in the object store"
    )


def test_unchanged_document_materialises_no_new_revision(editor_client, studio):
    document_id = seed_document_id(studio, DOC_DRAFT)
    editor_client.post(api(f"/documents/{document_id}/operations"),
                       json=new_operation(f"node-{unique_suffix()}", "skew", 3))
    first = editor_client.post(api(f"/documents/{document_id}/revisions"), json={"label": ""})
    assert first.status_code in OK, f"the first materialise answered {first.status_code}"
    before = studio.count_revisions(document_id)
    second = editor_client.post(api(f"/documents/{document_id}/revisions"), json={"label": ""})
    assert second.status_code in OK + REFUSED, (
        f"materialising an unchanged document answered {second.status_code}"
    )
    after = studio.count_revisions(document_id)
    assert after == before, (
        f"materialising an unchanged document created a revision: row count moved "
        f"{before} -> {after}. An unchanged content hash produces no revision"
    )


def test_restore_creates_new_revision_with_two_parents(editor_client, studio):
    document_id = seed_document_id(studio, DOC_PUBLISHED)
    listed = editor_client.get(api(f"/documents/{document_id}/revisions"))
    assert listed.status_code in OK, f"listing revisions answered {listed.status_code}"
    revisions = listed.json()
    assert len(revisions) >= 2, (
        f"{DOC_PUBLISHED!r} carries {len(revisions)} revisions; the seed must supply "
        f"at least two so a restore has something to restore"
    )
    oldest = revisions[-1]
    before_ids = {row["id"] for row in revisions}
    before_count = studio.count_revisions(document_id)
    r = editor_client.post(
        api(f"/documents/{document_id}/revisions/{oldest['id']}/restore"), json={})
    assert r.status_code in OK, (
        f"restoring revision {oldest['id']} answered {r.status_code}, "
        f"body {r.text[:200]!r}"
    )
    body = r.json()
    parents = body.get("parent_revision_ids") or []
    assert len(parents) == 2, (
        f"the restore revision names {len(parents)} parents {parents}; a restore "
        f"carries the current head and the restored revision"
    )
    assert oldest["id"] in parents, (
        f"the restore revision's parents {parents} do not include the restored "
        f"revision {oldest['id']}"
    )
    assert studio.count_revisions(document_id) == before_count + 1, (
        f"the restore did not append exactly one revision row (was {before_count})"
    )
    again = editor_client.get(api(f"/documents/{document_id}/revisions"))
    still_there = {row["id"] for row in again.json()}
    assert before_ids <= still_there, (
        f"revisions {sorted(before_ids - still_there)} became unreachable after a "
        f"restore; history only grows"
    )


def test_published_revision_object_exists_in_bucket_at_pinned_key(editor_client, studio, store):
    document_id = seed_document_id(studio, DOC_PUBLISHED)
    channel = studio.channel_by_slug(CHANNEL_PUBLISHED)
    assert channel is not None, f"seed channel {CHANNEL_PUBLISHED!r} is missing"
    builds = studio.builds_for(document_id)
    assert builds, f"{DOC_PUBLISHED!r} carries no build row"
    current = [b for b in builds if b["id"] == channel.get("current_build_id")]
    assert current, (
        f"channel {CHANNEL_PUBLISHED!r} refers to build "
        f"{channel.get('current_build_id')!r}, which is not a build of this document"
    )
    key = current[0].get("object_key", "")
    assert key.startswith(f"{REVISION_KEY_PREFIX}{document_id}/"), (
        f"the current build's object_key {key!r} does not follow the pinned scheme"
    )
    assert store.exists(key), (
        f"the published build's bytes are absent from the bucket at {key!r}; the "
        f"object store is where a document's bytes live"
    )
    assert revision_keys(store, document_id), (
        f"no object at all under {REVISION_KEY_PREFIX}{document_id}/ in the bucket"
    )


def test_poster_asset_object_exists_in_bucket_after_publish(editor_client, studio, store):
    document_id = seed_document_id(studio, DOC_SECOND)
    listed = editor_client.get(api(f"/documents/{document_id}/revisions"))
    assert listed.status_code in OK, f"listing revisions answered {listed.status_code}"
    revisions = listed.json()
    assert revisions, f"{DOC_SECOND!r} carries no revision to publish"
    r = editor_client.post(api(f"/documents/{document_id}/publish"),
                           json={"revision_id": revisions[0]["id"],
                                 "channel_slug": CHANNEL_SECOND,
                                 "title": DOC_SECOND, "tags": ["broadcast"]})
    assert r.status_code in OK, (
        f"publishing {DOC_SECOND!r} answered {r.status_code}, body {r.text[:200]!r}"
    )
    body = r.json()
    poster_key = body.get("poster_key", "")
    build_id = body.get("build_id")
    assert poster_key.startswith(f"posters/{build_id}/"), (
        f"poster_key {poster_key!r} does not follow posters/{{build_id}}/"
        f"{{sha256_of_bytes}}.svg for build {build_id!r}"
    )
    assert store.exists(poster_key), (
        f"the poster frame is absent from the bucket at {poster_key!r}"
    )
    assert poster_keys(store, build_id), (
        f"no poster object under posters/{build_id}/ in the bucket"
    )


def test_runtime_endpoint_serves_current_build_bytes(anon_client, studio):
    channel = studio.channel_by_slug(CHANNEL_PUBLISHED)
    assert channel is not None, f"seed channel {CHANNEL_PUBLISHED!r} is missing"
    r = anon_client.get(api(f"/runtime/{CHANNEL_PUBLISHED}"))
    assert r.status_code == 200, (
        f"GET /api/runtime/{CHANNEL_PUBLISHED} answered {r.status_code} with no "
        f"credential; a live channel is served to anybody"
    )
    assert r.content, (
        f"the runtime address served an empty body for {CHANNEL_PUBLISHED!r}"
    )
    cache = r.headers.get("cache-control", "")
    assert "max-age=10" in cache.replace(" ", ""), (
        f"the runtime response carries Cache-Control {cache!r}; the channel is a "
        f"short-lived pointer and must answer with max-age=10"
    )


def test_unpublished_document_has_no_public_runtime_route(anon_client, studio, store):
    document_id = seed_document_id(studio, DOC_DRAFT)
    assert studio.count_builds(document_id) == 0, (
        f"{DOC_DRAFT!r} carries a build row; the seed document must never have been "
        f"published"
    )
    keys = revision_keys(store, document_id)
    assert keys, (
        f"{DOC_DRAFT!r} has no object under {REVISION_KEY_PREFIX}{document_id}/; the "
        f"draft's bytes belong in the bucket even though nothing public serves them"
    )
    for slug in ("menu-transition", DOC_DRAFT.lower().replace(" ", "-")):
        r = anon_client.get(api(f"/runtime/{slug}"))
        assert r.status_code not in (200, 201), (
            f"GET /api/runtime/{slug} answered {r.status_code} for a document that "
            f"has never been published; no unauthenticated route reaches its bytes"
        )


def test_unpublished_document_absent_from_every_listing_ordering(anon_client, studio):
    assert studio.document_by_name(DOC_DRAFT) is not None, (
        f"seed document {DOC_DRAFT!r} is missing"
    )
    for order in ("featured", "latest", "for-hire"):
        r = anon_client.get(api("/listings"), params={"order": order})
        assert r.status_code in OK, (
            f"GET /api/listings?order={order} answered {r.status_code}"
        )
        titles = {row.get("title") for row in r.json()}
        assert DOC_DRAFT not in titles, (
            f"the {order!r} ordering returned the unpublished document {DOC_DRAFT!r}; "
            f"a listing exists only for a published build"
        )
    search = anon_client.get(api("/listings"), params={"q": "menu"})
    assert search.status_code in OK, f"searching answered {search.status_code}"
    found = {row.get("title") for row in search.json()}
    assert DOC_DRAFT not in found, (
        f"searching 'menu' returned the unpublished document {DOC_DRAFT!r}"
    )


def test_concurrent_publish_leaves_channel_with_single_current_build(studio):
    document_id = seed_document_id(studio, DOC_PUBLISHED)
    token = login(EDITOR_EMAIL, CORPUS_PASSWORD)
    with client(token) as reader:
        listed = reader.get(api(f"/documents/{document_id}/revisions"))
        assert listed.status_code in OK, f"listing revisions answered {listed.status_code}"
        revisions = listed.json()
    assert revisions, f"{DOC_PUBLISHED!r} carries no revision to publish"
    revision_id = revisions[0]["id"]

    def publish(_index: int) -> int:
        with client(token) as c:
            r = c.post(api(f"/documents/{document_id}/publish"),
                       json={"revision_id": revision_id,
                             "channel_slug": CHANNEL_PUBLISHED,
                             "title": DOC_PUBLISHED, "tags": ["ui", "loader"]})
            return r.status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        codes = list(pool.map(publish, range(2)))
    winners = [c for c in codes if c in OK]
    assert len(winners) == 1, (
        f"two simultaneous publishes to {CHANNEL_PUBLISHED!r} answered {codes}; "
        f"exactly one wins and the other is rejected"
    )
    channel = studio.channel_by_slug(CHANNEL_PUBLISHED)
    assert channel.get("current_build_id") is not None, (
        f"channel {CHANNEL_PUBLISHED!r} refers to no build after the race"
    )
    builds = studio.builds_for(document_id)
    build_ids = {b["id"] for b in builds}
    assert channel["current_build_id"] in build_ids, (
        f"channel {CHANNEL_PUBLISHED!r} refers to build "
        f"{channel['current_build_id']!r}, which is not a build row of this document"
    )


def test_rollback_repoints_channel_to_earlier_build(editor_client, studio):
    document_id = seed_document_id(studio, DOC_PUBLISHED)
    builds = sorted(studio.builds_for(document_id), key=lambda b: b["id"])
    assert len(builds) >= 2, (
        f"{DOC_PUBLISHED!r} carries {len(builds)} builds; a rollback needs an "
        f"earlier one to return to"
    )
    earlier = builds[0]["id"]
    r = editor_client.post(api(f"/channels/{CHANNEL_PUBLISHED}/rollback"),
                           json={"build_id": earlier})
    assert r.status_code in OK, (
        f"rolling back to build {earlier} answered {r.status_code}, "
        f"body {r.text[:200]!r}"
    )
    landed = poll_until(
        lambda: studio.channel_by_slug(CHANNEL_PUBLISHED).get("current_build_id") == earlier,
        timeout=CACHE_INTERVAL_SECONDS * 3)
    assert landed, (
        f"channel {CHANNEL_PUBLISHED!r} still refers to build "
        f"{studio.channel_by_slug(CHANNEL_PUBLISHED).get('current_build_id')!r} "
        f"rather than {earlier} after a rollback"
    )


def test_unpublish_removes_listing_but_keeps_build_row(editor_client, studio):
    document_id = seed_document_id(studio, DOC_SECOND)
    builds_before = studio.count_builds(document_id)
    assert builds_before >= 1, f"{DOC_SECOND!r} carries no build row"
    r = editor_client.post(api(f"/channels/{CHANNEL_SECOND}/unpublish"), json={})
    assert r.status_code in OK, (
        f"unpublishing {CHANNEL_SECOND!r} answered {r.status_code}, "
        f"body {r.text[:200]!r}"
    )
    gone = poll_until(
        lambda: (studio.listing_by_slug(CHANNEL_SECOND) or {}).get("visibility") != "public",
        timeout=CACHE_INTERVAL_SECONDS * 3)
    assert gone, (
        f"the listing for {CHANNEL_SECOND!r} is still visibility 'public' after an "
        f"unpublish"
    )
    assert studio.count_builds(document_id) == builds_before, (
        f"unpublishing deleted a build row: count moved {builds_before} -> "
        f"{studio.count_builds(document_id)}. Unpublishing removes delivery only"
    )


def test_featured_ordering_is_not_like_count_ordering(anon_client, studio):
    loader = studio.listing_by_slug(CHANNEL_PUBLISHED)
    ticker = studio.listing_by_slug(CHANNEL_SECOND)
    assert loader is not None and ticker is not None, (
        f"the seed listings {CHANNEL_PUBLISHED!r} and {CHANNEL_SECOND!r} are not both "
        f"present"
    )
    assert loader.get("like_count") == LIKES_LOADER_RING, (
        f"{CHANNEL_PUBLISHED!r} carries like_count {loader.get('like_count')!r}, "
        f"expected {LIKES_LOADER_RING}"
    )
    assert ticker.get("like_count") == LIKES_MATCH_TICKER, (
        f"{CHANNEL_SECOND!r} carries like_count {ticker.get('like_count')!r}, "
        f"expected {LIKES_MATCH_TICKER}"
    )
    r = anon_client.get(api("/listings"), params={"order": "featured"})
    assert r.status_code in OK, f"GET /api/listings?order=featured answered {r.status_code}"
    slugs = [row.get("slug") for row in r.json()]
    assert CHANNEL_PUBLISHED in slugs, (
        f"the featured ordering omits {CHANNEL_PUBLISHED!r}; slugs seen: {slugs}"
    )
    if CHANNEL_SECOND in slugs:
        assert slugs.index(CHANNEL_PUBLISHED) < slugs.index(CHANNEL_SECOND), (
            f"the featured ordering put {CHANNEL_SECOND!r} (likes "
            f"{LIKES_MATCH_TICKER}) ahead of {CHANNEL_PUBLISHED!r} (likes "
            f"{LIKES_LOADER_RING}); featured is an editorial ordering, not a like "
            f"ordering"
        )


def test_cursor_paging_returns_no_duplicate_listing(anon_client):
    seen: list[str] = []
    cursor = None
    for _page in range(5):
        params = {"order": "featured"}
        if cursor:
            params["cursor"] = cursor
        r = anon_client.get(api("/listings"), params=params)
        assert r.status_code in OK, (
            f"paging /api/listings answered {r.status_code} on page {_page}"
        )
        rows = r.json()
        assert len(rows) <= PAGE_SIZE, (
            f"page {_page} returned {len(rows)} listings, over the page size "
            f"{PAGE_SIZE}"
        )
        seen.extend(row.get("slug") for row in rows)
        cursor = r.headers.get(CURSOR_HEADER)
        if not cursor:
            break
    assert len(seen) == len(set(seen)), (
        f"cursor paging returned a listing twice within one session: {sorted(seen)}"
    )


def test_repeat_like_leaves_like_count_unchanged(editor_client, studio):
    listing = studio.listing_by_slug(CHANNEL_PUBLISHED)
    assert listing is not None, f"seed listing {CHANNEL_PUBLISHED!r} is missing"
    first = editor_client.post(api(f"/listings/{listing['id']}/likes"), json={})
    assert first.status_code in OK, (
        f"liking listing {listing['id']} answered {first.status_code}"
    )
    after_first = studio.listing_by_slug(CHANNEL_PUBLISHED).get("like_count")
    rows_after_first = studio.count_listing_likes(listing["id"])
    second = editor_client.post(api(f"/listings/{listing['id']}/likes"), json={})
    assert second.status_code in OK + REFUSED, (
        f"a repeat like answered {second.status_code}"
    )
    settle()
    assert studio.listing_by_slug(CHANNEL_PUBLISHED).get("like_count") == after_first, (
        f"a repeat like moved like_count from {after_first} to "
        f"{studio.listing_by_slug(CHANNEL_PUBLISHED).get('like_count')}"
    )
    assert studio.count_listing_likes(listing["id"]) == rows_after_first, (
        f"a repeat like wrote a second listing_like row: {rows_after_first} -> "
        f"{studio.count_listing_likes(listing['id'])}"
    )


def test_seat_blocked_invitation_writes_no_member_row(editor_client, studio):
    assert studio.seats_used() == SEAT_CAP, (
        f"the seeded workspace holds {studio.seats_used()} seats against a cap of "
        f"{SEAT_CAP}; the seat-blocked path needs a full workspace"
    )
    email = probe_email()
    invited = editor_client.post(api("/invitations"), json={"email": email, "role": "editor"})
    assert invited.status_code in OK, (
        f"inviting {email} as an editor answered {invited.status_code}, "
        f"body {invited.text[:200]!r}"
    )
    token = invited.json().get("token")
    assert token, f"the invitation response carries no `token`: keys {sorted(invited.json())}"
    before_members = studio.count_members()
    accepted = editor_client.post(
        api(f"/invitations/{token}/accept"),
        json={"password": CORPUS_PASSWORD, "display_name": "Probe Editor",
              "handle": probe_handle()})
    assert accepted.status_code in REFUSED, (
        f"accepting an editor invitation over the seat cap answered "
        f"{accepted.status_code}; it must be refused"
    )
    assert studio.count_members() == before_members, (
        f"a refused acceptance wrote a member row: count moved {before_members} -> "
        f"{studio.count_members()}"
    )
    held = studio.invitation_by_email(email)
    assert held is not None and held.get("state") == "seat_blocked", (
        f"the invitation for {email} is in state "
        f"{(held or {}).get('state')!r}, expected 'seat_blocked'"
    )
    assert studio.seats_used() == SEAT_CAP, (
        f"the derived seat count moved to {studio.seats_used()} after a refused "
        f"acceptance"
    )


def test_viewer_invitation_accepted_at_full_seat_cap(editor_client, studio):
    email = probe_email()
    invited = editor_client.post(api("/invitations"), json={"email": email, "role": "viewer"})
    assert invited.status_code in OK, (
        f"inviting {email} as a viewer answered {invited.status_code}"
    )
    token = invited.json().get("token")
    assert token, f"the invitation response carries no `token`: keys {sorted(invited.json())}"
    accepted = editor_client.post(
        api(f"/invitations/{token}/accept"),
        json={"password": CORPUS_PASSWORD, "display_name": "Probe Viewer",
              "handle": probe_handle()})
    assert accepted.status_code in OK, (
        f"accepting a viewer invitation at a full seat cap answered "
        f"{accepted.status_code}; a viewer holds no seat"
    )
    assert studio.member_by_email(email) is not None, (
        f"no member row was stored for the accepted viewer {email}"
    )
    assert studio.seats_used() == SEAT_CAP, (
        f"accepting a viewer moved the derived seat count to {studio.seats_used()}"
    )


def test_new_signup_workspace_returns_empty_document_array(anon_client):
    email = probe_email()
    r = anon_client.post(api("/auth/signup"),
                         json={"email": email, "password": CORPUS_PASSWORD,
                               "display_name": "Probe Founder", "handle": probe_handle()})
    assert r.status_code in OK, (
        f"signing up {email} answered {r.status_code}, body {r.text[:200]!r}"
    )
    token = r.json().get("token")
    assert token, f"the signup response carries no `token`: keys {sorted(r.json())}"
    with client(token) as fresh:
        documents = fresh.get(api("/documents"))
        assert documents.status_code in OK, (
            f"a fresh workspace answered {documents.status_code} on GET /api/documents; "
            f"an empty collection is an empty array, never an error"
        )
        rows = documents.json()
        assert isinstance(rows, list) and rows == [], (
            f"a fresh workspace returned {rows!r} rather than an empty top-level array"
        )
        folders = fresh.get(api("/folders"))
        assert folders.status_code in OK, (
            f"a fresh workspace answered {folders.status_code} on GET /api/folders"
        )


def test_new_signup_cannot_read_seeded_workspace_documents(anon_client, studio):
    email = probe_email()
    r = anon_client.post(api("/auth/signup"),
                         json={"email": email, "password": CORPUS_PASSWORD,
                               "display_name": "Probe Outsider", "handle": probe_handle()})
    assert r.status_code in OK, f"signing up {email} answered {r.status_code}"
    token = r.json().get("token")
    document_id = seed_document_id(studio, DOC_PUBLISHED)
    with client(token) as outsider:
        got = outsider.get(api(f"/documents/{document_id}"))
        assert got.status_code in DENIED_OR_MISSING, (
            f"a member of a different workspace read document {document_id} with "
            f"status {got.status_code}; one workspace never reads another's rows"
        )


def test_seeded_editor_reads_own_workspace_documents(editor_client, studio):
    r = editor_client.get(api("/documents"))
    assert r.status_code in OK, f"GET /api/documents answered {r.status_code}"
    names = {row.get("name") for row in r.json()}
    for expected in (DOC_PUBLISHED, DOC_DRAFT):
        assert expected in names, (
            f"the seeded editor's document list omits {expected!r}; names seen: "
            f"{sorted(n for n in names if n)}"
        )


def test_third_editor_holds_the_last_seat(studio):
    member = studio.member_by_email(EDITOR3_EMAIL)
    assert member is not None, f"seed member {EDITOR3_EMAIL} is missing"
    assert member.get("status") == "active", (
        f"{EDITOR3_EMAIL} is stored with status {member.get('status')!r}, expected "
        f"'active'"
    )
    assert studio.seats_used() == SEAT_CAP, (
        f"the derived seat count is {studio.seats_used()} against the pinned cap "
        f"{SEAT_CAP}"
    )


def test_listing_handle_matches_its_author(studio):
    listing = studio.listing_by_slug(CHANNEL_PUBLISHED)
    assert listing is not None, f"seed listing {CHANNEL_PUBLISHED!r} is missing"
    assert listing.get("handle") == HANDLE_RAE, (
        f"listing {CHANNEL_PUBLISHED!r} carries handle {listing.get('handle')!r}, "
        f"expected {HANDLE_RAE!r}"
    )


def test_seeded_schema_carries_the_pinned_columns(studio, backend):
    workspace = backend.one("workspace", slug=WORKSPACE_SLUG)
    assert workspace is not None, f"no workspace row with slug {WORKSPACE_SLUG!r}"
    for column in ("id", "name", "slug", "seat_cap", "created_at"):
        assert column in workspace, (
            f"the workspace row is missing the pinned column {column!r}; columns "
            f"present: {sorted(workspace)}"
        )
    animation = backend.one("animation", name="Spin")
    assert animation is not None, "no animation row named 'Spin'"
    frames = animation.get("frame_count")
    assert isinstance(frames, int) and frames == 120, (
        f"Spin carries frame_count {frames!r}; the pinned value is the integer 120, "
        f"and a duration in seconds is a different quantity"
    )
    transitions = backend.rows("transition")
    assert transitions, "no transition rows were seeded"
    indexes = [row.get("index") for row in transitions]
    assert all(isinstance(i, int) for i in indexes), (
        f"transition.index carries {indexes!r}; declaration order is an integer and "
        f"it is what decides which transition wins"
    )
