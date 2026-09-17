from __future__ import annotations

import concurrent.futures

import httpx

import appclient
import conftest
from conftest import (ADMINISTRATOR, BRANCH_MERGED_SUBJECT, DECOY_FIELD, DENIED,
                      REVIEW_APPROVED_SUBJECT, mails,
                      DESIGN_FILE, EDITOR, FIRST_COMPONENT, FIRST_FRAME,
                      FIRST_PROJECT, FIRST_TEAM, IN_TEAM_REVIEWER, LIBRARY_FILE,
                      LIBRARY_NAME, PASSWORD, PEER_TEAM_FILE,
                      PEER_TEAM_REVIEWER, REFUSED, REVIEW_REQUESTED_SUBJECT,
                      SECOND_EDITOR, SECOND_FRAME, SECOND_PROJECT, SECOND_TEAM,
                      add_frame, approve, body, decide, design_file_id, file_id,
                      frame_named, frames, library_file_id, merge,
                      merge_versions, ok, open_branch, poll, project_id,
                      push_branch, read_branch, request_review, reviewed_branch,
                      settle, team_id, unique)

"""core features."""


def test_seeded_member_signs_in_and_receives_token(backend):
    for address in (EDITOR, SECOND_EDITOR, IN_TEAM_REVIEWER, PEER_TEAM_REVIEWER,
                    ADMINISTRATOR):
        token = appclient.login(address, PASSWORD)
        assert isinstance(token, str) and token, (
            f"POST /api/auth/login for {address} returned no usable access_token"
        )
    with appclient.client(appclient.login(EDITOR, PASSWORD)) as cl:
        me = ok(cl.get("/me"), "reading the signed-in principal")
    principal = me.get("principal") or {}
    assert principal.get("primary_email") == EDITOR, (
        f"GET /api/me for the token issued to {EDITOR} names "
        f"{principal.get('primary_email')!r}. Body: {str(me)[:300]}"
    )
    row = backend.one("principal", primary_email=EDITOR)
    assert row and row.get("external_id"), (
        f"the principal row for {EDITOR} carries no external_id, so sign-in did not "
        f"join the member to the identity provider subject. Row: {str(row)[:300]}"
    )


def test_frame_move_is_persisted_and_survives_reload(editor, backend):
    file = design_file_id(editor)
    before = frame_named(editor, file, FIRST_FRAME)
    moved_x = int(before.get("x", 0)) + 37
    moved_y = int(before.get("y", 0)) + 53
    response = editor.patch(f"/frames/{before['id']}", json={"x": moved_x, "y": moved_y})
    ok(response, f"moving the frame {FIRST_FRAME!r}")
    after = frame_named(editor, file, FIRST_FRAME)
    assert (int(after["x"]), int(after["y"])) == (moved_x, moved_y), (
        f"GET /api/files/{file}/frames re-read {FIRST_FRAME!r} at "
        f"({after.get('x')}, {after.get('y')}) after a move to ({moved_x}, {moved_y}). "
        f"A position that only ever existed on screen is not a stored position"
    )
    row = backend.one("frame", id=before["id"])
    assert row and (int(row["x"]), int(row["y"])) == (moved_x, moved_y), (
        f"the frame row for {FIRST_FRAME!r} in PostgreSQL reads "
        f"{(row or {}).get('x')!r}, {(row or {}).get('y')!r} after a move to "
        f"({moved_x}, {moved_y})"
    )


def test_frame_delete_removes_it_from_the_stored_board(editor):
    file = design_file_id(editor)
    created = add_frame(editor, file, unique("Scratch Frame"))
    response = editor.delete(f"/frames/{created['id']}")
    assert response.status_code in (200, 202, 204), (
        f"DELETE /api/frames/{created['id']} returned {response.status_code}, "
        f"expected the frame to be deleted. Body: {body(response)}"
    )
    late = editor.patch(f"/frames/{created['id']}", json={"name": unique("Revived")})
    assert late.status_code not in conftest.CREATED or late.json().get("status") == "deleted", (
        f"a rename sent after the delete of {created['name']!r} returned "
        f"{late.status_code} and revived the frame. Body: {body(late)}"
    )
    names = [row.get("name") for row in frames(editor, file)
             if row.get("status") != "deleted"]
    assert created["name"] not in names and not any(
        str(n).startswith("Revived") for n in names), (
        f"the deleted frame {created['name']!r} is still listed on file {file!r}. "
        f"Frames now: {names!r}"
    )


def test_frame_cycle_move_is_refused(editor):
    file = design_file_id(editor)
    parent = add_frame(editor, file, unique("Parent Frame"))
    child = add_frame(editor, file, unique("Child Frame"), parent_id=parent["id"])
    response = editor.patch(f"/frames/{parent['id']}", json={"parent_id": child["id"]})
    assert response.status_code in REFUSED, (
        f"PATCH /api/frames/{parent['id']} making the frame a descendant of its own "
        f"child returned {response.status_code}, expected a refusal. "
        f"Body: {body(response)}"
    )
    reread = ok(editor.get(f"/files/{file}/frames"), "re-reading the frame tree")
    parent_now = [r for r in reread if r.get("id") == parent["id"]]
    assert parent_now and parent_now[0].get("parent_id") != child["id"], (
        f"the refused move was applied anyway: frame {parent['id']!r} now reports "
        f"parent_id {parent_now[0].get('parent_id') if parent_now else None!r}"
    )


def test_concurrent_frame_inserts_are_both_stored(editor, second_editor):
    file = design_file_id(editor)
    anchor = frame_named(editor, file, SECOND_FRAME)
    first_name = unique("Insert A")
    second_name = unique("Insert B")

    def insert(client: httpx.Client, name: str) -> httpx.Response:
        return client.post(f"/files/{file}/frames", json={
            "name": name, "parent_id": anchor.get("parent_id"),
            "after_frame_id": anchor["id"], "x": 10, "y": 10,
            "width": 200, "height": 120})

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(insert, editor, first_name)
        second = pool.submit(insert, second_editor, second_name)
        responses = [first.result(), second.result()]

    accepted = [r for r in responses if r.status_code in conftest.CREATED]
    assert len(accepted) == 2, (
        f"two inserts at one position under one parent returned "
        f"{[r.status_code for r in responses]!r}; both must be accepted. "
        f"Bodies: {[body(r, 160) for r in responses]!r}"
    )
    names = [row.get("name") for row in frames(editor, file)]
    assert first_name in names and second_name in names, (
        f"one of the two simultaneous inserts was lost. Expected both "
        f"{first_name!r} and {second_name!r} on file {file!r}; frames are {names!r}"
    )
    order_keys = [row.get("order_key") for row in frames(editor, file)
                  if row.get("name") in (first_name, second_name)]
    assert len(set(order_keys)) == 2, (
        f"the two inserted frames share an order_key {order_keys!r}, so readers "
        f"cannot agree on their order"
    )


def test_comment_thread_is_stored_against_its_frame(editor, second_editor):
    file = design_file_id(editor)
    frame = frame_named(editor, file, SECOND_FRAME)
    first_body = unique("first remark")
    thread = ok(editor.post(f"/files/{file}/threads",
                            json={"frame_id": frame["id"], "body": first_body}),
                f"starting a comment thread on the frame {SECOND_FRAME!r}")
    assert str(thread.get("frame_id")) == str(frame["id"]), (
        f"the thread was stored against frame_id {thread.get('frame_id')!r} "
        f"rather than the frame {SECOND_FRAME!r} whose id is {frame['id']!r}"
    )
    second_body = unique("second remark")
    ok(second_editor.post(f"/threads/{thread['id']}/comments", json={"body": second_body}),
       "replying in the thread")
    reread = ok(editor.get(f"/files/{file}/threads"), "re-reading the file threads")
    mine = [t for t in reread if str(t.get("id")) == str(thread["id"])]
    assert mine, f"the thread {thread['id']!r} is absent from the file's thread list"
    bodies = [c.get("body") for c in mine[0].get("comments", [])]
    assert bodies[:2] == [first_body, second_body], (
        f"replies are not ordered oldest first: the thread reads {bodies!r}, "
        f"expected {[first_body, second_body]!r} at its head"
    )


def test_comment_edit_after_window_is_refused(editor, second_editor):
    file = design_file_id(editor)
    frame = frame_named(editor, file, SECOND_FRAME)
    thread = ok(editor.post(f"/files/{file}/threads",
                            json={"frame_id": frame["id"], "body": unique("original")}),
                "starting a comment thread")
    comment_id = thread.get("comments", [{}])[0].get("id") or thread.get("comment_id")
    assert comment_id, (
        f"the created thread carries no comment id to edit. Body: {str(thread)[:300]}"
    )
    stranger = second_editor.patch(f"/comments/{comment_id}", json={"body": unique("hijack")})
    assert stranger.status_code in DENIED, (
        f"PATCH /api/comments/{comment_id} by a member who is not the author returned "
        f"{stranger.status_code}, expected a denial. Body: {body(stranger)}"
    )
    reread = ok(editor.get(f"/files/{file}/threads"), "re-reading the file threads")
    mine = [t for t in reread if str(t.get("id")) == str(thread["id"])][0]
    stored = mine.get("comments", [{}])[0].get("body")
    assert stored and "hijack" not in stored, (
        f"the denied edit changed the stored body anyway: the comment now reads "
        f"{stored!r}"
    )


def test_comment_delete_leaves_a_tombstone_row(editor):
    file = design_file_id(editor)
    frame = frame_named(editor, file, SECOND_FRAME)
    thread = ok(editor.post(f"/files/{file}/threads",
                            json={"frame_id": frame["id"], "body": unique("doomed")}),
                "starting a comment thread")
    comment_id = thread.get("comments", [{}])[0].get("id") or thread.get("comment_id")
    response = editor.delete(f"/comments/{comment_id}")
    assert response.status_code in (200, 202, 204), (
        f"DELETE /api/comments/{comment_id} returned {response.status_code}, "
        f"expected the comment to be tombstoned. Body: {body(response)}"
    )
    reread = ok(editor.get(f"/files/{file}/threads"), "re-reading the file threads")
    mine = [t for t in reread if str(t.get("id")) == str(thread["id"])]
    assert mine, (
        f"deleting a comment removed its whole thread {thread['id']!r}; the thread "
        f"structure must survive the deletion"
    )
    first = mine[0].get("comments", [{}])[0]
    assert first.get("tombstoned") is True, (
        f"the deleted comment is not marked tombstoned: {str(first)[:300]}"
    )


def test_thread_resolution_is_stored_with_its_resolver(editor):
    file = design_file_id(editor)
    frame = frame_named(editor, file, SECOND_FRAME)
    thread = ok(editor.post(f"/files/{file}/threads",
                            json={"frame_id": frame["id"], "body": unique("settled")}),
                "starting a comment thread")
    resolved = ok(editor.post(f"/threads/{thread['id']}/resolve"),
                  f"resolving thread {thread['id']!r}")
    assert resolved.get("resolved") is True, (
        f"POST /api/threads/{thread['id']}/resolve returned resolved="
        f"{resolved.get('resolved')!r}, expected true. Body: {str(resolved)[:300]}"
    )
    assert resolved.get("resolved_by"), (
        f"the resolved thread records no resolver: {str(resolved)[:300]}"
    )


def test_library_publish_stores_an_immutable_version(editor):
    library = _library(editor)
    note = unique("changelog")
    published = ok(editor.post(f"/libraries/{library['id']}/versions",
                               json={"changelog": note}),
                   f"publishing a new version of the library {LIBRARY_NAME!r}")
    assert published.get("changelog") == note, (
        f"the published version stored changelog {published.get('changelog')!r} "
        f"rather than the line written at publish time"
    )
    versions = ok(editor.get(f"/libraries/{library['id']}/versions"),
                  "reading the library versions")
    numbers = [v.get("number") for v in versions]
    assert published.get("number") in numbers and len(numbers) == len(set(numbers)), (
        f"the published version number {published.get('number')!r} is absent or "
        f"duplicated in the library history {numbers!r}"
    )
    again = ok(editor.post(f"/libraries/{library['id']}/versions",
                           json={"changelog": unique("second changelog")}),
               "publishing a second version")
    after = ok(editor.get(f"/libraries/{library['id']}/versions"),
               "re-reading the library versions")
    original = [v for v in after if v.get("number") == published.get("number")]
    assert original and original[0].get("changelog") == note, (
        f"publishing version {again.get('number')!r} rewrote version "
        f"{published.get('number')!r}, whose changelog now reads "
        f"{original[0].get('changelog') if original else None!r}"
    )


def test_library_publish_with_unnamed_component_is_refused(editor):
    library = _library(editor)
    source = library_file_id(editor)
    unnamed = add_frame(editor, source, "")
    try:
        response = editor.post(f"/libraries/{library['id']}/versions",
                               json={"changelog": unique("blocked")})
        assert response.status_code in REFUSED, (
            f"POST /api/libraries/{library['id']}/versions with an unnamed component "
            f"returned {response.status_code}, expected a refusal naming the "
            f"component. Body: {body(response)}"
        )
    finally:
        editor.delete(f"/frames/{unnamed['id']}")


def test_library_publish_with_duplicate_name_is_refused(editor):
    library = _library(editor)
    source = library_file_id(editor)
    clash = unique("Duplicated Component")
    added = [add_frame(editor, source, clash), add_frame(editor, source, clash)]
    try:
        response = editor.post(f"/libraries/{library['id']}/versions",
                               json={"changelog": unique("clash")})
        assert response.status_code in REFUSED, (
            f"POST /api/libraries/{library['id']}/versions with two components named "
            f"{clash!r} returned {response.status_code}, expected a refusal naming "
            f"the collision. Body: {body(response)}"
        )
    finally:
        for frame in added:
            editor.delete(f"/frames/{frame['id']}")


def test_subscriber_pin_is_unchanged_until_the_update_is_applied(editor):
    library = _library(editor)
    subscriber = design_file_id(editor)
    pinned_before = _pin(editor, subscriber, library["id"])
    ok(editor.post(f"/libraries/{library['id']}/versions",
                   json={"changelog": unique("newer")}),
       "publishing a newer library version")
    pinned_after = _pin(editor, subscriber, library["id"])
    assert pinned_after == pinned_before, (
        f"publishing moved the subscriber's pin on its own: file {subscriber!r} was "
        f"pinned at {pinned_before!r} and now reports {pinned_after!r}"
    )
    applied = ok(editor.post(f"/files/{subscriber}/library-updates/{library['id']}"),
                 "applying the library update")
    assert applied.get("pinned_version_id") != pinned_before, (
        f"applying the update left the pin at {pinned_before!r}"
    )


def test_branch_creation_records_the_base_version(editor):
    source = design_file_id(editor)
    before = frames(editor, source)
    branch = open_branch(editor, source, unique(conftest.BRANCH_NAME))
    assert branch.get("base_version_id"), (
        f"the branch opened on {DESIGN_FILE!r} records no base_version_id. "
        f"Body: {str(branch)[:300]}"
    )
    push_branch(editor, branch["id"], unique("branch only frame"))
    after = frames(editor, source)
    assert [r.get("id") for r in after] == [r.get("id") for r in before], (
        f"editing the branch changed the main file {DESIGN_FILE!r}: its frames went "
        f"from {[r.get('name') for r in before]!r} to {[r.get('name') for r in after]!r}"
    )


def test_review_request_moves_the_branch_to_in_review(editor):
    source = design_file_id(editor)
    branch = open_branch(editor, source, unique(conftest.BRANCH_NAME))
    push_branch(editor, branch["id"], unique("frame"))
    request_review(editor, branch["id"], IN_TEAM_REVIEWER)
    state = read_branch(editor, branch["id"]).get("state")
    assert state == "in_review", (
        f"after a review request the branch reports state {state!r}, expected "
        f"'in_review'"
    )


def test_approval_is_bound_to_the_branch_version(editor, reviewer):
    made = reviewed_branch(editor, reviewer, unique(conftest.BRANCH_NAME))
    branch_id = made["branch"]["id"]
    before = read_branch(editor, branch_id)
    approve(reviewer, branch_id)
    after = read_branch(editor, branch_id)
    approval = after.get("approval") or {}
    assert after.get("state") == "approved", (
        f"after an approval the branch reports state {after.get('state')!r}, "
        f"expected 'approved'"
    )
    assert approval.get("target_version_id"), (
        f"the recorded approval names no target_version_id: {str(approval)[:300]}"
    )
    assert approval.get("target_version_id") == before.get("current_version_id"), (
        f"the approval is bound to version {approval.get('target_version_id')!r} "
        f"while the branch's current version at approval time was "
        f"{before.get('current_version_id')!r}"
    )


def test_push_after_approval_invalidates_the_approval(editor, reviewer):
    made = reviewed_branch(editor, reviewer, unique(conftest.BRANCH_NAME))
    branch_id = made["branch"]["id"]
    approve(reviewer, branch_id)
    push_branch(editor, branch_id, unique("late change"))
    after = read_branch(editor, branch_id)
    approval = after.get("approval") or {}
    assert approval.get("invalidated_at"), (
        f"a push after the approval left the approval live: {str(approval)[:200]}"
    )
    assert after.get("state") == "in_review", (
        f"the invalidated approval left the branch in state {after.get('state')!r}; "
        f"it returns to 'in_review'"
    )


def test_approval_invalidated_row_names_both_versions(editor, reviewer, administrator):
    made = reviewed_branch(editor, reviewer, unique(conftest.BRANCH_NAME))
    branch_id = made["branch"]["id"]
    before = read_branch(editor, branch_id)
    approve(reviewer, branch_id)
    approved_version = (read_branch(editor, branch_id).get("approval") or {}).get(
        "target_version_id")
    push_branch(editor, branch_id, unique("late change"))
    after = read_branch(editor, branch_id)
    superseding = after.get("current_version_id")

    def read_events():
        return ok(administrator.get("/admin/audit",
                                    params={"action": "approval_invalidated"}),
                  "reading the audit stream for approval_invalidated")

    events = poll(read_events, lambda rows: any(
        str(approved_version) in str(r) and str(superseding) in str(r) for r in rows),
        "the approval_invalidated record naming both versions")
    assert events, (
        f"no approval_invalidated record names both the approved version "
        f"{approved_version!r} and the version {superseding!r} that superseded it"
    )
    assert before.get("current_version_id") != superseding, (
        f"the branch version did not move across the push: it reads "
        f"{superseding!r} before and after"
    )


def test_merge_is_refused_while_the_approval_is_invalidated(editor, reviewer):
    made = reviewed_branch(editor, reviewer, unique(conftest.BRANCH_NAME))
    branch_id = made["branch"]["id"]
    source = made["source_file_id"]
    merges_before = len(merge_versions(editor, source))
    approve(reviewer, branch_id)
    push_branch(editor, branch_id, unique("late change"))
    response = merge(reviewer, branch_id)
    assert response.status_code in REFUSED, (
        f"POST /api/branches/{branch_id}/merge after the approval was invalidated "
        f"returned {response.status_code}, expected a refusal. Body: {body(response)}"
    )
    merges_after = len(merge_versions(editor, source))
    assert merges_after == merges_before, (
        f"the refused merge appended a merge version to {DESIGN_FILE!r}: the file "
        f"carried {merges_before} merge version(s) before and {merges_after} after"
    )
    state = read_branch(editor, branch_id).get("state")
    assert state != "applied", (
        f"the refused merge moved the branch to state {state!r}; it must stay out "
        f"of 'applied'"
    )


def test_second_approval_allows_the_merge_to_append_one_version(editor, reviewer):
    name = unique(conftest.BRANCH_NAME)
    made = reviewed_branch(editor, reviewer, name)
    branch_id = made["branch"]["id"]
    source = made["source_file_id"]
    branch_file = read_branch(editor, branch_id).get("branch_file_id")
    branch_frames = frames(editor, branch_file)
    assert branch_frames, f"branch {branch_id!r} carries no frame to comment on"
    note = unique("branch remark")
    ok(editor.post(f"/files/{branch_file}/threads",
                   json={"frame_id": branch_frames[0]["id"], "body": note}),
       "starting a thread on the branch")
    merges_before = len(merge_versions(editor, source))
    approve(reviewer, branch_id)
    push_branch(editor, branch_id, unique("late change"))
    merge(reviewer, branch_id)
    approve(reviewer, branch_id)
    merged = merge(reviewer, branch_id)
    ok(merged, f"merging branch {branch_id!r} after a fresh approval")
    merges_after = len(merge_versions(editor, source))
    assert merges_after == merges_before + 1, (
        f"the merge appended {merges_after - merges_before} merge version(s) to "
        f"{DESIGN_FILE!r}, expected exactly one"
    )
    after = read_branch(editor, branch_id)
    assert after.get("state") == "applied", (
        f"after a successful merge the branch reports state {after.get('state')!r}, "
        f"expected 'applied'"
    )
    assert after.get("merged_version_id"), (
        f"the applied branch records no merged_version_id: {str(after)[:300]}"
    )
    threads = ok(editor.get(f"/files/{source}/threads"), "reading the main file threads")
    carried = [t for t in threads
               if any(c.get("body") == note for c in t.get("comments", []))]
    assert carried and carried[0].get("origin_branch_name") == name, (
        f"the thread started on branch {name!r} did not travel to {DESIGN_FILE!r} "
        f"naming its branch: {str(carried)[:300]}"
    )


def test_repeat_merge_creates_no_second_merge_version(editor, reviewer):
    made = reviewed_branch(editor, reviewer, unique(conftest.BRANCH_NAME))
    branch_id = made["branch"]["id"]
    source = made["source_file_id"]
    approve(reviewer, branch_id)
    ok(merge(reviewer, branch_id), f"merging branch {branch_id!r}")
    merges_after_first = len(merge_versions(editor, source))
    second = merge(reviewer, branch_id)
    assert second.status_code in REFUSED, (
        f"a second POST /api/branches/{branch_id}/merge returned "
        f"{second.status_code}, expected a refusal. Body: {body(second)}"
    )
    merges_after_second = len(merge_versions(editor, source))
    assert merges_after_second == merges_after_first, (
        f"merging the same branch twice produced {merges_after_second} merge "
        f"version(s), expected {merges_after_first}"
    )


def test_branch_withdrawal_is_stored(editor):
    source = design_file_id(editor)
    branch = open_branch(editor, source, unique(conftest.BRANCH_NAME))
    push_branch(editor, branch["id"], unique("frame"))
    request_review(editor, branch["id"], IN_TEAM_REVIEWER)
    ok(decide(editor, branch["id"], "withdrawn", "no longer needed"),
       f"withdrawing branch {branch['id']!r}")
    state = read_branch(editor, branch["id"]).get("state")
    assert state == "withdrawn", (
        f"after a withdrawal the branch reports state {state!r}, expected 'withdrawn'"
    )


def test_changes_requested_returns_the_branch_to_in_review_on_push(editor, reviewer):
    made = reviewed_branch(editor, reviewer, unique(conftest.BRANCH_NAME))
    branch_id = made["branch"]["id"]
    ok(decide(reviewer, branch_id, "changes_requested", "tighten the spacing"),
       f"requesting changes on branch {branch_id!r}")
    assert read_branch(editor, branch_id).get("state") == "changes_requested", (
        f"a changes_requested decision left the branch in state "
        f"{read_branch(editor, branch_id).get('state')!r}"
    )
    push_branch(editor, branch_id, unique("revision"))
    state = read_branch(editor, branch_id).get("state")
    assert state == "in_review", (
        f"after the requester pushed, the branch reports state {state!r}, expected "
        f"'in_review'"
    )


def test_file_version_sequence_rises_by_one_per_file(editor):
    source = design_file_id(editor)
    branch = open_branch(editor, source, unique(conftest.BRANCH_NAME))
    first = push_branch(editor, branch["id"], unique("one"))
    second = push_branch(editor, branch["id"], unique("two"))
    assert int(second["sequence"]) == int(first["sequence"]) + 1, (
        f"two consecutive versions on branch {branch['id']!r} carry sequences "
        f"{first.get('sequence')!r} then {second.get('sequence')!r}; the sequence "
        f"rises by one per file"
    )


def test_presence_lists_the_other_member_with_a_stable_colour(editor, second_editor):
    file = design_file_id(editor)

    def both_present():
        editor.get(f"/files/{file}/presence")
        second_editor.get(f"/files/{file}/presence")
        return ok(editor.get(f"/files/{file}/presence"),
                  f"reading presence on file {file!r}")

    rows = poll(both_present,
                lambda rs: len({r.get("primary_email") for r in rs}) >= 2,
                f"both {EDITOR} and {SECOND_EDITOR} listed in the presence of "
                f"file {file!r}")
    addresses = {r.get("primary_email") for r in rows}
    assert {EDITOR, SECOND_EDITOR} <= addresses, (
        f"GET /api/files/{file}/presence lists {sorted(a for a in addresses if a)!r}; "
        f"both members with the file open must appear"
    )
    for row in rows:
        assert row.get("display_name"), (
            f"a presence row carries no display_name: {str(row)[:200]}"
        )
        assert row.get("colour"), (
            f"a presence row carries no colour: {str(row)[:200]}"
        )
    colours = [r.get("colour") for r in rows if r.get("primary_email") in
               (EDITOR, SECOND_EDITOR)]
    assert len(set(colours)) == len(colours), (
        f"two members in one file were given the same presence colour: {colours!r}"
    )
    mine = [r.get("colour") for r in rows if r.get("primary_email") == EDITOR]
    with conftest.api_for(EDITOR) as later:
        later.get(f"/files/{file}/presence")
        second_editor.get(f"/files/{file}/presence")
        again = poll(lambda: ok(later.get(f"/files/{file}/presence"),
                                "re-reading presence in a later session"),
                     lambda rs: any(r.get("primary_email") == EDITOR for r in rs),
                     f"{EDITOR} listed in the presence of file {file!r} in a later "
                     f"session")
    later_colour = [r.get("colour") for r in again
                    if r.get("primary_email") == EDITOR]
    assert later_colour == mine, (
        f"the presence colour for {EDITOR} was {mine!r} in one session and "
        f"{later_colour!r} in a later one; it is derived from the member identity "
        f"and does not move between sessions"
    )


"""authorization."""


def test_editor_is_denied_on_the_decision_endpoint(editor, reviewer):
    made = reviewed_branch(editor, reviewer, unique(conftest.BRANCH_NAME))
    branch_id = made["branch"]["id"]
    with conftest.api_for(SECOND_EDITOR) as other_editor:
        response = decide(other_editor, branch_id, "approved", "looks fine")
    assert response.status_code in DENIED, (
        f"POST /api/branches/{branch_id}/decisions from an editor session returned "
        f"{response.status_code}, expected a denial. Body: {body(response)}"
    )
    state = read_branch(editor, branch_id).get("state")
    assert state == "in_review", (
        f"the denied decision changed the branch anyway: state is now {state!r}"
    )


def test_editor_is_denied_on_the_merge_endpoint(editor, reviewer):
    made = reviewed_branch(editor, reviewer, unique(conftest.BRANCH_NAME))
    branch_id = made["branch"]["id"]
    source = made["source_file_id"]
    approve(reviewer, branch_id)
    before = len(merge_versions(editor, source))
    response = merge(editor, branch_id)
    assert response.status_code in DENIED, (
        f"POST /api/branches/{branch_id}/merge from an editor session returned "
        f"{response.status_code}, expected a denial. Body: {body(response)}"
    )
    assert len(merge_versions(editor, source)) == before, (
        f"the denied merge appended a merge version to {DESIGN_FILE!r}"
    )


def test_self_approval_is_denied(reviewer):
    source = design_file_id(reviewer)
    branch = open_branch(reviewer, source, unique(conftest.BRANCH_NAME))
    push_branch(reviewer, branch["id"], unique("frame"))
    request_review(reviewer, branch["id"], IN_TEAM_REVIEWER)
    response = decide(reviewer, branch["id"], "approved", "mine")
    assert response.status_code in DENIED, (
        f"a reviewer approving their own branch {branch['id']!r} received "
        f"{response.status_code}, expected a denial. Body: {body(response)}"
    )
    state = read_branch(reviewer, branch["id"]).get("state")
    assert state == "in_review", (
        f"the denied self-approval changed the branch state to {state!r}"
    )


def test_peer_team_reviewer_is_denied_on_the_decision(editor, reviewer, peer_reviewer):
    made = reviewed_branch(editor, reviewer, unique(conftest.BRANCH_NAME))
    branch_id = made["branch"]["id"]
    response = decide(peer_reviewer, branch_id, "approved", "from another team")
    assert response.status_code in DENIED, (
        f"POST /api/branches/{branch_id}/decisions from {PEER_TEAM_REVIEWER}, who "
        f"belongs to {SECOND_TEAM} and not to {FIRST_TEAM}, returned "
        f"{response.status_code}, expected a denial. Body: {body(response)}"
    )
    state = read_branch(editor, branch_id).get("state")
    assert state == "in_review", (
        f"the denied peer-team decision changed the branch state to {state!r}"
    )
    merged = merge(peer_reviewer, branch_id)
    assert merged.status_code in DENIED, (
        f"POST /api/branches/{branch_id}/merge from the peer-team reviewer returned "
        f"{merged.status_code}, expected a denial. Body: {body(merged)}"
    )


def test_editor_is_denied_on_every_admin_endpoint(editor):
    attempts = {
        "GET /api/admin/members": editor.get("/admin/members"),
        "GET /api/admin/audit": editor.get("/admin/audit"),
        "GET /api/admin/identity": editor.get("/admin/identity"),
        "PATCH /api/admin/identity": editor.patch(
            "/admin/identity", json={"enforcement": "optional",
                                     "break_glass_emails": [ADMINISTRATOR]}),
    }
    served = {name: r.status_code for name, r in attempts.items()
              if r.status_code not in DENIED}
    assert not served, (
        f"an editor session reached administration endpoints that must deny it: "
        f"{served!r}"
    )


def test_anonymous_request_is_denied(anonymous):
    attempts = {
        "GET /api/me": anonymous.get("/me"),
        "GET /api/teams": anonymous.get("/teams"),
        "GET /api/admin/members": anonymous.get("/admin/members"),
    }
    served = {name: r.status_code for name, r in attempts.items()
              if r.status_code not in DENIED}
    assert not served, (
        f"an unauthenticated caller reached endpoints that require a session: "
        f"{served!r}"
    )
    health = anonymous.get("/health")
    assert health.status_code == 200, (
        f"GET /api/health returned {health.status_code} without a session, expected "
        f"200. Body: {body(health)}"
    )
    signup = httpx.get(f"{appclient.app_url()}/signup", timeout=appclient.TIMEOUT)
    assert signup.status_code == 404, (
        f"GET /signup returned {signup.status_code}; accounts are seeded and no "
        f"signup page is served. Body: {body(signup)}"
    )


def test_cross_team_file_read_is_denied_with_the_not_found_shape(editor, peer_reviewer):
    peer_file = file_id(peer_reviewer,
                        project_id(peer_reviewer, team_id(peer_reviewer, SECOND_TEAM),
                                   SECOND_PROJECT),
                        PEER_TEAM_FILE)
    forbidden = editor.get(f"/files/{peer_file}/frames")
    absent = editor.get(f"/files/{unique('nosuchfile')}/frames")
    assert forbidden.status_code in DENIED, (
        f"GET /api/files/{peer_file}/frames from a member of {FIRST_TEAM} returned "
        f"{forbidden.status_code}, expected a denial. Body: {body(forbidden)}"
    )
    assert forbidden.status_code == absent.status_code, (
        f"a file the caller may not see answered {forbidden.status_code} while a "
        f"file that does not exist answered {absent.status_code}; the two must be "
        f"indistinguishable"
    )
    assert forbidden.text == absent.text, (
        f"the forbidden answer body {body(forbidden, 160)!r} differs from the absent "
        f"answer body {body(absent, 160)!r}, which discloses that the file exists"
    )


def test_read_only_member_write_is_denied_and_changes_no_row(editor, administrator):
    file = design_file_id(editor)
    frame = frame_named(editor, file, FIRST_FRAME)
    before = (frame.get("x"), frame.get("y"))
    response = administrator.patch(f"/frames/{frame['id']}", json={"x": 999, "y": 999})
    assert response.status_code in DENIED, (
        f"PATCH /api/frames/{frame['id']} from a session holding no grant on the "
        f"file returned {response.status_code}, expected a denial. "
        f"Body: {body(response)}"
    )
    after = frame_named(editor, file, FIRST_FRAME)
    assert (after.get("x"), after.get("y")) == before, (
        f"the denied write moved {FIRST_FRAME!r} from {before!r} to "
        f"{(after.get('x'), after.get('y'))!r}"
    )


def test_org_admin_holds_no_implicit_file_grant(editor, administrator):
    file = design_file_id(editor)
    response = administrator.get(f"/files/{file}/frames")
    assert response.status_code in DENIED, (
        f"GET /api/files/{file}/frames from {ADMINISTRATOR}, who belongs to no team, "
        f"returned {response.status_code}; administering an organization and reading "
        f"its designs are separate powers. Body: {body(response)}"
    )


def test_role_change_is_stored_on_the_membership_row(administrator):
    members = ok(administrator.get("/admin/members"), "reading the member list")
    by_address = {m.get("primary_email"): m for m in members}
    assert SECOND_EDITOR in by_address, (
        f"the seeded member {SECOND_EDITOR} is absent from GET /api/admin/members, "
        f"which returned {sorted(a for a in by_address if a)!r}"
    )
    admin_row = by_address.get(ADMINISTRATOR) or {}
    assert (admin_row.get("org_role"), admin_row.get("seat_type")) == ("org_admin", "view_only"), (
        f"{ADMINISTRATOR} reads role {admin_row.get('org_role')!r} on seat "
        f"{admin_row.get('seat_type')!r}; the seat is stored independently of the role"
    )
    principal = by_address[SECOND_EDITOR].get("principal_id")
    try:
        ok(administrator.patch(f"/admin/members/{principal}",
                               json={"org_role": "reviewer", "seat_type": "full"}),
           f"changing the role of {SECOND_EDITOR}")
        reread = ok(administrator.get("/admin/members"), "re-reading the member list")
        now = [m for m in reread if m.get("primary_email") == SECOND_EDITOR][0]
        assert now.get("org_role") == "reviewer", (
            f"the membership row for {SECOND_EDITOR} reports org_role "
            f"{now.get('org_role')!r} after the change, expected 'reviewer'"
        )
    finally:
        administrator.patch(f"/admin/members/{principal}",
                            json={"org_role": "editor", "seat_type": "full"})


"""data integrity."""


def test_audit_stream_stores_every_review_transition(editor, reviewer, administrator):
    made = reviewed_branch(editor, reviewer, unique(conftest.BRANCH_NAME))
    branch_id = made["branch"]["id"]
    approve(reviewer, branch_id)
    ok(merge(reviewer, branch_id), f"merging branch {branch_id!r}")

    def read_events():
        return ok(administrator.get("/admin/audit"), "reading the audit stream")

    rows = poll(read_events, lambda rs: {"review_requested", "review_approved",
                                         "branch_merged"}.issubset(
        {r.get("action") for r in rs}), "the three review transitions in the audit stream")
    assert isinstance(rows, list), (
        f"GET /api/admin/audit returned {type(rows).__name__}, not a top-level array"
    )
    for row in rows:
        assert row.get("actor_principal_id"), (
            f"an audit row carries no actor: {str(row)[:300]}"
        )
        assert row.get("outcome") in ("allowed", "denied", "error"), (
            f"an audit row carries outcome {row.get('outcome')!r}, which is outside "
            f"the closed set"
        )
        assert row.get("action") in conftest.AUDIT_ACTIONS, (
            f"an audit row carries action {row.get('action')!r}, which is not in the "
            f"closed vocabulary"
        )


def test_audit_row_update_is_refused_append_only(administrator):
    rows = ok(administrator.get("/admin/audit"), "reading the audit stream")
    assert rows, "the audit stream is empty, so append-only cannot be observed"
    target = rows[0]
    event_id = target.get("id")
    attempts = [
        administrator.patch(f"/admin/audit/{event_id}", json={"action": "sign_in"}),
        administrator.delete(f"/admin/audit/{event_id}"),
    ]
    served = [r.status_code for r in attempts if r.status_code in conftest.CREATED]
    assert not served, (
        f"the application accepted a change to a recorded audit event: "
        f"{served!r}. The stream is append-only in the store, not by convention"
    )
    reread = ok(administrator.get("/admin/audit"), "re-reading the audit stream")
    same = [r for r in reread if r.get("id") == event_id]
    assert same and same[0].get("action") == target.get("action"), (
        f"the recorded event {event_id!r} changed from action "
        f"{target.get('action')!r} to "
        f"{same[0].get('action') if same else 'absent'!r}"
    )


def test_repeat_invitation_stores_no_second_membership_row(administrator):
    before = ok(administrator.get("/admin/members"), "reading the member list")
    count_before = len([m for m in before if m.get("primary_email") == EDITOR])
    response = administrator.post("/admin/members/invitations",
                                  json={"email": EDITOR, "org_role": "editor",
                                        "seat_type": "full"})
    assert response.status_code in conftest.CREATED, (
        f"re-inviting an existing member returned {response.status_code}, expected "
        f"the existing membership. Body: {body(response)}"
    )
    after = ok(administrator.get("/admin/members"), "re-reading the member list")
    count_after = len([m for m in after if m.get("primary_email") == EDITOR])
    assert count_after == count_before == 1, (
        f"re-inviting {EDITOR} left {count_after} membership row(s), expected the "
        f"single existing one"
    )
    malformed = administrator.post("/admin/members/invitations",
                                   json={"email": "not-an-address", "org_role": "editor",
                                         "seat_type": "full"})
    assert malformed.status_code in REFUSED, (
        f"an invitation for a malformed address returned {malformed.status_code}, "
        f"expected a refusal naming the field. Body: {body(malformed)}"
    )
    final = ok(administrator.get("/admin/members"), "re-reading the member list")
    assert len(final) == len(after), (
        f"the refused invitation changed the member count from {len(after)} to "
        f"{len(final)}"
    )


"""edge cases."""


def test_review_request_without_a_reviewer_is_refused(editor):
    source = design_file_id(editor)
    branch = open_branch(editor, source, unique(conftest.BRANCH_NAME))
    push_branch(editor, branch["id"], unique("frame"))
    response = editor.post(f"/branches/{branch['id']}/review-requests",
                           json={"reviewer_email": ""})
    assert response.status_code in REFUSED, (
        f"POST /api/branches/{branch['id']}/review-requests naming no reviewer "
        f"returned {response.status_code}, expected a refusal. Body: {body(response)}"
    )
    assert "reviewer" in response.text.lower(), (
        f"the refusal does not name the reviewer field that failed. "
        f"Body: {body(response)}"
    )
    state = read_branch(editor, branch["id"]).get("state")
    assert state == "draft", (
        f"the refused review request moved the branch to state {state!r}, which must "
        f"stay 'draft'"
    )


def test_changes_requested_without_a_comment_is_refused(editor, reviewer):
    made = reviewed_branch(editor, reviewer, unique(conftest.BRANCH_NAME))
    branch_id = made["branch"]["id"]
    response = decide(reviewer, branch_id, "changes_requested", "")
    assert response.status_code in REFUSED, (
        f"a changes_requested decision carrying no comment returned "
        f"{response.status_code}, expected a refusal. Body: {body(response)}"
    )
    state = read_branch(editor, branch_id).get("state")
    assert state == "in_review", (
        f"the refused decision moved the branch to state {state!r}"
    )


def test_access_request_with_the_decoy_field_is_refused(anonymous, backend):
    address = f"{unique('probe')}@example.com"
    response = anonymous.post("/access-requests",
                              json={"email": address, "note": "please let me in",
                                    DECOY_FIELD: "https://filled-by-a-bot.example"})
    assert response.status_code in REFUSED, (
        f"POST /api/access-requests carrying a filled {DECOY_FIELD} returned "
        f"{response.status_code}, expected a refusal. Body: {body(response)}"
    )
    assert backend.count("access_request", email=address) == 0, (
        f"the refused submission for {address} still wrote an access_request row"
    )
    honest = anonymous.post("/access-requests",
                            json={"email": address, "note": "please let me in",
                                  DECOY_FIELD: ""})
    assert honest.status_code in conftest.CREATED, (
        f"POST /api/access-requests with an empty {DECOY_FIELD} returned "
        f"{honest.status_code}, expected the request to be recorded. "
        f"Body: {body(honest)}"
    )
    assert backend.count("access_request", email=address) == 1, (
        f"the accepted submission for {address} wrote no access_request row"
    )
    burst = [anonymous.post("/access-requests",
                            json={"email": address, "note": "again", DECOY_FIELD: ""})
             for _ in range(5)]
    assert burst[-1].status_code in REFUSED, (
        f"seven submissions from one source inside a minute were all accepted: "
        f"{[r.status_code for r in burst]!r}"
    )


def test_unknown_address_answers_not_found():
    target = f"{appclient.app_url()}/{unique('no-such-page')}"
    response = httpx.get(target, timeout=appclient.TIMEOUT, follow_redirects=True)
    assert response.status_code == 404, (
        f"GET {target} returned {response.status_code}, expected 404 from the "
        f"product's own not-found page. Body: {body(response)}"
    )
    assert len(response.text) > 200, (
        f"the not-found page at {target} returned {len(response.text)} characters, "
        f"which is too little to carry the product's own page and a way back"
    )


def test_sitemap_lists_the_public_routes():
    target = f"{appclient.app_url()}/sitemap.xml"
    response = httpx.get(target, timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"GET {target} returned {response.status_code}, expected 200. "
        f"Body: {body(response)}"
    )
    for route in ("/access", "/signin"):
        assert route in response.text, (
            f"the sitemap at {target} does not list the public route {route!r}. "
            f"Body: {body(response, 400)}"
        )


def test_robots_names_the_sitemap():
    target = f"{appclient.app_url()}/robots.txt"
    response = httpx.get(target, timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"GET {target} returned {response.status_code}, expected 200. "
        f"Body: {body(response)}"
    )
    assert "sitemap" in response.text.lower(), (
        f"the robots file at {target} does not name the sitemap. "
        f"Body: {body(response, 400)}"
    )


def test_sign_in_lockout_after_repeated_failures():
    unknown = f"{unique('locked')}@example.com"

    def attempt(address: str) -> httpx.Response:
        return httpx.post(f"{appclient.api_base()}/auth/login",
                          json={"email": address, "password": "not-the-password"},
                          timeout=appclient.TIMEOUT)

    first_unknown = attempt(unknown)
    known = attempt(EDITOR)
    assert first_unknown.status_code not in conftest.CREATED, (
        f"a wrong password for {unknown} was accepted: {first_unknown.status_code}"
    )
    assert known.status_code == first_unknown.status_code, (
        f"a wrong password answered {known.status_code} for the seeded {EDITOR} but "
        f"{first_unknown.status_code} for an unknown address, which discloses that "
        f"the account exists"
    )
    for _ in range(10):
        attempt(unknown)
    last = attempt(unknown)
    assert last.status_code not in conftest.CREATED, (
        f"attempt twelve for {unknown} was accepted: {last.status_code}"
    )
    assert last.status_code == 429 or "lock" in last.text.lower(), (
        f"after eleven failures inside the window the answer for {unknown} is still "
        f"{last.status_code} without saying the address is locked. Body: {body(last)}"
    )


"""email."""


def test_review_request_delivers_mail_to_the_reviewer(editor, inbox):
    source = design_file_id(editor)
    name = unique(conftest.BRANCH_NAME)
    branch = open_branch(editor, source, name)
    push_branch(editor, branch["id"], unique("frame"))
    request_review(editor, branch["id"], IN_TEAM_REVIEWER)

    message = poll(
        lambda: inbox.find(IN_TEAM_REVIEWER, REVIEW_REQUESTED_SUBJECT),
        lambda m: m is not None,
        f"a message to {IN_TEAM_REVIEWER} whose subject begins "
        f"{REVIEW_REQUESTED_SUBJECT!r}")
    assert message.subject.startswith(REVIEW_REQUESTED_SUBJECT), (
        f"the delivered subject {message.subject!r} does not begin "
        f"{REVIEW_REQUESTED_SUBJECT!r}"
    )
    assert name in message.subject, (
        f"the delivered subject {message.subject!r} does not name the branch {name!r}"
    )
    assert message.to == [IN_TEAM_REVIEWER], (
        f"the review request reached {message.to!r}; it must reach "
        f"{[IN_TEAM_REVIEWER]!r} alone, with no copy address"
    )
    assert name in message.body and DESIGN_FILE in message.body, (
        f"the message body names neither the branch {name!r} nor the file "
        f"{DESIGN_FILE!r}. Body: {message.body[:300]}"
    )


def test_merge_delivers_confirmation_mail_to_the_requester(editor, reviewer, inbox):
    name = unique(conftest.BRANCH_NAME)
    made = reviewed_branch(editor, reviewer, name)
    branch_id = made["branch"]["id"]
    approve(reviewer, branch_id)
    approved = poll(lambda: mails(inbox, EDITOR, name),
                    lambda ms: any(m.subject.startswith(REVIEW_APPROVED_SUBJECT) for m in ms),
                    f"an approval mail to {EDITOR} whose subject begins "
                    f"{REVIEW_APPROVED_SUBJECT!r}")
    assert len([m for m in approved if m.subject.startswith(REVIEW_APPROVED_SUBJECT)]) == 1, (
        f"the approval of {name!r} reached {EDITOR} more than once"
    )
    ok(merge(reviewer, branch_id), f"merging branch {branch_id!r}")
    merged = poll(lambda: mails(inbox, EDITOR, name),
                  lambda ms: any(m.subject.startswith(BRANCH_MERGED_SUBJECT) for m in ms),
                  f"a merge confirmation to {EDITOR} whose subject begins "
                  f"{BRANCH_MERGED_SUBJECT!r}")
    confirmation = [m for m in merged if m.subject.startswith(BRANCH_MERGED_SUBJECT)][0]
    assert confirmation.to == [EDITOR], (
        f"the merge confirmation reached {confirmation.to!r}; it must reach the member "
        f"who requested the review alone"
    )


def test_changes_requested_delivers_no_mail(editor, reviewer, inbox):
    asked = unique(conftest.BRANCH_NAME)
    first = reviewed_branch(editor, reviewer, asked)
    ok(decide(reviewer, first["branch"]["id"], "changes_requested", "tighten the spacing"),
       "requesting changes")

    withdrawn = unique(conftest.BRANCH_NAME)
    second = reviewed_branch(editor, reviewer, withdrawn)
    ok(decide(editor, second["branch"]["id"], "withdrawn", "no longer needed"),
       "withdrawing a branch")

    voided = unique(conftest.BRANCH_NAME)
    third = reviewed_branch(editor, reviewer, voided)
    approve(reviewer, third["branch"]["id"])
    poll(lambda: mails(inbox, EDITOR, voided),
         lambda ms: len(ms) == 1, f"the single approval mail for {voided!r}")
    push_branch(editor, third["branch"]["id"], unique("late change"))

    settle()
    settle()
    settle()
    assert mails(inbox, EDITOR, asked) == [], (
        f"a changes_requested decision on {asked!r} delivered mail to {EDITOR}"
    )
    assert mails(inbox, EDITOR, withdrawn) == [], (
        f"a withdrawal of {withdrawn!r} delivered mail to {EDITOR}"
    )
    assert len(mails(inbox, EDITOR, voided)) == 1, (
        f"an invalidated approval on {voided!r} delivered more mail to {EDITOR}; "
        f"only the approval itself sends"
    )
    for name in (asked, withdrawn, voided):
        assert len(mails(inbox, IN_TEAM_REVIEWER, name)) == 1, (
            f"{IN_TEAM_REVIEWER} received a message other than the one review request "
            f"for {name!r}"
        )


def _library(cl: httpx.Client) -> dict:
    """The seeded library, read through the file it is published from."""
    source = library_file_id(cl)
    libraries = ok(cl.get(f"/files/{source}/libraries"),
                   f"reading the library published from {LIBRARY_FILE!r}")
    named = [row for row in libraries if row.get("name") == LIBRARY_NAME]
    assert named, (
        f"the seeded library {LIBRARY_NAME!r} is absent from the libraries of "
        f"{LIBRARY_FILE!r}, which reported {[r.get('name') for r in libraries]!r}"
    )
    return named[0]


def _pin(cl: httpx.Client, subscriber, library_id) -> object:
    subs = ok(cl.get(f"/files/{subscriber}/subscriptions"),
              f"reading the library subscriptions of file {subscriber!r}")
    mine = [s for s in subs if str(s.get("library_id")) == str(library_id)]
    assert mine, (
        f"file {subscriber!r} does not subscribe to library {library_id!r}; "
        f"subscriptions are {subs!r}"
    )
    return mine[0].get("pinned_version_id")
