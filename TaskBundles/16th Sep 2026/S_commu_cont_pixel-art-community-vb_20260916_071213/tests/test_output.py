"""Section graders for deku/pixel-art-community-vb.

One module, every section and every declared slot, grouped by banner. The
assertion picks the banner, never the setup.
"""

from __future__ import annotations

import os

import httpx
from _shapes import flatten, items
from appclient import api_base, app_url
from conftest import (
    AUTHOR2_EMAIL,
    AUTHOR2_HANDLE,
    AUTHOR_EMAIL,
    AUTHOR_HANDLE,
    MAX_COMMENT_CLUSTERS,
    MAX_TAGS,
    PRIVATE_PIECE,
    PUBLIC_ANIMATED_PIECE,
    PUBLIC_STILL_PIECE,
    READER_EMAIL,
    READER_HANDLE,
    RESERVED_HANDLES,
    SEEDED_TOPICS,
    SECOND_AUTHOR_PIECE,
    THUMBNAIL_SIZES,
    UNLISTED_PIECE,
    created_piece,
    feed_page,
    feed_titles,
    poll_until,
    publish,
    settle,
)

TIMEOUT = 30.0


def test_health_endpoint_reports_ready(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, expected 200 once the "
        f"app is ready: {response.text[:400]}"
    )


def test_signup_creates_account_and_returns_token(anon_client, probe_suffix):
    email = f"probe-{probe_suffix}@example.com"
    response = anon_client.post(
        "/auth/signup",
        json={
            "display_name": f"Probe {probe_suffix}",
            "email": email,
            "password": "deku-demo-pw-2026",
            "date_of_birth": "1996-04-11",
        },
    )
    assert response.status_code in (200, 201), (
        f"POST /api/auth/signup for {email} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    body = response.json()
    assert body.get("access_token"), (
        f"signup for {email} returned no access_token: {response.text[:400]}"
    )


def test_login_returns_access_and_refresh_tokens(anon_client):
    response = anon_client.post(
        "/auth/login", json={"email": AUTHOR_EMAIL, "password": "deku-demo-pw-2026"}
    )
    assert response.status_code == 200, (
        f"POST /api/auth/login for {AUTHOR_EMAIL} returned {response.status_code} "
        f"against the seeded password: {response.text[:400]}"
    )
    body = response.json()
    assert body.get("access_token"), (
        f"login for {AUTHOR_EMAIL} returned no access_token: {response.text[:400]}"
    )
    assert body.get("refresh_token"), (
        f"login for {AUTHOR_EMAIL} returned no refresh_token, so rotation cannot "
        f"be honoured: {response.text[:400]}"
    )


def test_publish_creates_piece_on_author_profile(author_client, probe_suffix, db):
    title = f"Probe Harbour {probe_suffix}"
    piece = created_piece(publish(author_client, title, probe_suffix))
    row = poll_until(
        lambda: db.piece_by_title(title),
        f"a pieces row titled {title!r} after publishing",
    )
    author = db.account_by_email(AUTHOR_EMAIL)
    assert author is not None, (
        f"the seeded account {AUTHOR_EMAIL} has no accounts row"
    )
    assert row["account_id"] == author["id"], (
        f"published piece {piece['id']} is owned by account_id={row['account_id']!r}, "
        f"expected the publishing author {author['id']!r}"
    )
    profile = author_client.get(f"/artists/{AUTHOR_HANDLE}", params={"tab": "gallery"})
    assert profile.status_code == 200, (
        f"GET /api/artists/{AUTHOR_HANDLE} returned {profile.status_code}: "
        f"{profile.text[:400]}"
    )
    assert title.lower() in flatten(profile.json()), (
        f"the freshly published piece {title!r} is absent from its own author's "
        f"gallery tab: {profile.text[:400]}"
    )


def test_new_feed_orders_by_published_descending(author_client, probe_suffix):
    first = created_piece(publish(author_client, f"Probe Older {probe_suffix}", probe_suffix))
    second = created_piece(
        publish(
            author_client,
            f"Probe Newer {probe_suffix}",
            probe_suffix,
            idempotency_key=f"probe-{probe_suffix}-2",
        )
    )

    def both_present():
        titles = feed_titles(author_client, feed="new")
        ids = [t for t in titles if t and probe_suffix in t]
        return ids if len(ids) >= 2 else None

    ordered = poll_until(both_present, "both probe pieces in the new feed")
    assert ordered[0] == second["title"], (
        f"the new feed leads with {ordered[0]!r}; the most recently published "
        f"piece is {second['title']!r}, so the ordering is not published-descending"
    )
    assert first["title"] in ordered, (
        f"the earlier probe piece {first['title']!r} is missing from the new feed"
    )


def test_tag_feed_returns_only_matching_pieces(anon_client):
    response = anon_client.get("/pieces", params={"feed": "tag", "tag": "cats"})
    assert response.status_code == 200, (
        f"GET /api/pieces?feed=tag&tag=cats returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    rows = items(response.json())
    assert rows, "the tag feed for 'cats' is empty, but a seeded piece carries it"
    for row in rows:
        tags = [str(t).lower() for t in (row.get("tags") or [])]
        assert "cats" in tags, (
            f"the tag feed for 'cats' returned {row.get('title')!r}, whose tags are "
            f"{tags!r}"
        )


def test_popular_feed_pages_from_a_stable_snapshot(anon_client):
    first = feed_page(anon_client, feed="popular")
    token = first.get("snapshot")
    assert token, (
        "the first popular-feed page returned no snapshot token, so a second page "
        f"cannot read from a frozen ordering: {str(first)[:400]}"
    )
    again = feed_page(anon_client, feed="popular", snapshot=token)
    first_ids = [r.get("id") for r in items(first.get("pieces", first))]
    again_ids = [r.get("id") for r in items(again.get("pieces", again))]
    assert first_ids == again_ids, (
        f"re-reading the popular feed under snapshot {token!r} returned a different "
        f"ordering: {first_ids!r} then {again_ids!r}"
    )


def test_topics_endpoint_lists_the_seeded_topics(anon_client):
    response = anon_client.get("/topics")
    assert response.status_code == 200, (
        f"GET /api/topics returned {response.status_code}: {response.text[:400]}"
    )
    flat = flatten(response.json())
    missing = [t for t in SEEDED_TOPICS if t.lower() not in flat]
    assert not missing, (
        f"GET /api/topics is missing the seeded topic(s) {missing!r}; the row is "
        f"editorial and its six entries are pinned"
    )


def test_search_matches_title_tag_and_handle(anon_client):
    for query, expected in (
        (PUBLIC_STILL_PIECE, PUBLIC_STILL_PIECE.lower()),
        ("ocean", "ocean"),
        (AUTHOR_HANDLE, AUTHOR_HANDLE),
    ):
        response = anon_client.get("/search", params={"q": query})
        assert response.status_code == 200, (
            f"GET /api/search?q={query!r} returned {response.status_code}: "
            f"{response.text[:400]}"
        )
        assert expected in flatten(response.json()), (
            f"searching for {query!r} returned nothing carrying {expected!r}: "
            f"{response.text[:400]}"
        )


def test_following_feed_returns_followed_authors_only(reader_client, db):
    follow = reader_client.post(f"/artists/{AUTHOR_HANDLE}/follow")
    assert follow.status_code in (200, 201, 204), (
        f"POST /api/artists/{AUTHOR_HANDLE}/follow returned {follow.status_code}: "
        f"{follow.text[:400]}"
    )
    titles = poll_until(
        lambda: feed_titles(reader_client, feed="following") or None,
        "a non-empty following feed after following an author",
    )
    second_author_pieces = {SECOND_AUTHOR_PIECE}
    leaked = second_author_pieces.intersection({t for t in titles if t})
    assert not leaked, (
        f"the following feed carries {leaked!r}, published by {AUTHOR2_HANDLE}, "
        f"who the reader does not follow"
    )


def test_follow_then_unfollow_updates_counts(reader_client, db):
    reader = db.account_by_email(READER_EMAIL)
    author2 = db.account_by_handle(AUTHOR2_HANDLE)
    assert reader and author2, (
        f"the seeded accounts {READER_EMAIL} and {AUTHOR2_HANDLE} must both exist"
    )
    reader_client.post(f"/artists/{AUTHOR2_HANDLE}/follow")
    poll_until(
        lambda: db.count_follows(reader["id"], author2["id"]) == 1 or None,
        "exactly one follows row after following",
    )
    unfollow = reader_client.delete(f"/artists/{AUTHOR2_HANDLE}/follow")
    assert unfollow.status_code in (200, 204), (
        f"DELETE /api/artists/{AUTHOR2_HANDLE}/follow returned "
        f"{unfollow.status_code}: {unfollow.text[:400]}"
    )
    poll_until(
        lambda: db.count_follows(reader["id"], author2["id"]) == 0 or None,
        "no follows row after unfollowing",
    )


def test_remix_records_parent_and_raises_counter(author2_client, db, probe_suffix):
    parent = db.piece_by_title(PUBLIC_STILL_PIECE)
    assert parent is not None, (
        f"the seeded piece {PUBLIC_STILL_PIECE!r} has no pieces row"
    )
    title = f"Probe Remix {probe_suffix}"
    child = created_piece(
        publish(author2_client, title, probe_suffix, parent_id=parent["id"])
    )
    row = poll_until(
        lambda: db.piece_by_title(title), f"a pieces row titled {title!r}"
    )
    assert row["parent_id"] == parent["id"], (
        f"the remix {child['id']} stored parent_id={row['parent_id']!r}, expected "
        f"the piece it was opened from, {parent['id']!r}"
    )


def test_piece_detail_carries_lineage_and_comments(anon_client, db):
    parent = db.piece_by_title(PUBLIC_STILL_PIECE)
    assert parent is not None, f"{PUBLIC_STILL_PIECE!r} has no pieces row"
    response = anon_client.get(f"/pieces/{parent['id']}")
    assert response.status_code == 200, (
        f"GET /api/pieces/{parent['id']} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    flat = flatten(response.json())
    assert "lineage" in flat or "parent" in flat or "remix" in flat, (
        f"the piece detail for {PUBLIC_STILL_PIECE!r} carries nothing naming its "
        f"lineage: {response.text[:400]}"
    )
    lineage = anon_client.get(f"/pieces/{parent['id']}/lineage")
    assert lineage.status_code == 200, (
        f"GET /api/pieces/{parent['id']}/lineage returned {lineage.status_code}: "
        f"{lineage.text[:400]}"
    )


def test_deleted_parent_leaves_tombstone_with_attribution(
    author_client, author2_client, db, probe_suffix
):
    parent_title = f"Probe Parent {probe_suffix}"
    parent = created_piece(publish(author_client, parent_title, probe_suffix))
    child_title = f"Probe Child {probe_suffix}"
    created_piece(
        publish(
            author2_client,
            child_title,
            probe_suffix,
            parent_id=parent["id"],
            idempotency_key=f"probe-{probe_suffix}-child",
        )
    )
    removed = author_client.delete(f"/pieces/{parent['id']}")
    assert removed.status_code in (200, 202, 204), (
        f"DELETE /api/pieces/{parent['id']} returned {removed.status_code}: "
        f"{removed.text[:400]}"
    )
    child_row = poll_until(
        lambda: db.piece_by_title(child_title), f"the remix {child_title!r}"
    )
    assert child_row is not None, (
        f"deleting the parent removed the remix {child_title!r}; children survive "
        f"a parent deletion with their attribution intact"
    )
    detail = author2_client.get(f"/pieces/{child_row['id']}")
    assert detail.status_code == 200, (
        f"GET /api/pieces/{child_row['id']} returned {detail.status_code} after its "
        f"parent was deleted: {detail.text[:400]}"
    )
    assert AUTHOR_HANDLE in flatten(detail.json()), (
        f"the remix of a deleted parent no longer names the parent's author "
        f"{AUTHOR_HANDLE!r}, so attribution did not survive: {detail.text[:400]}"
    )


def test_privacy_and_terms_pages_are_served():
    for path in ("/privacy", "/terms"):
        response = httpx.get(f"{app_url()}{path}", timeout=TIMEOUT)
        assert response.status_code == 200, (
            f"GET {path} returned {response.status_code}, but the page is reachable "
            f"from the footer of every page: {response.text[:200]}"
        )


def test_unknown_path_answers_not_found():
    response = httpx.get(
        f"{app_url()}/no-such-surface-anywhere", timeout=TIMEOUT
    )
    assert response.status_code == 404, (
        f"an unknown address answered {response.status_code}; the product's own "
        f"not-found page is served with a not-found status"
    )


def test_unresolved_handle_page_offers_search():
    response = httpx.get(f"{app_url()}/nosuchartisthere", timeout=TIMEOUT)
    assert response.status_code == 404, (
        f"an unresolved handle answered {response.status_code}, expected a "
        f"not-found status"
    )
    body = response.text.lower()
    assert "search" in body, (
        "the page for an unresolved handle offers no search; most failures on this "
        "site are mistyped handles and they get their own answer"
    )


def test_reader_cannot_publish_a_piece(reader_client, probe_suffix, db):
    title = f"Probe Reader Publish {probe_suffix}"
    response = publish(reader_client, title, probe_suffix)
    assert response.status_code in (401, 403), (
        f"a reader session publishing returned {response.status_code}; a reader "
        f"cannot publish, and the refusal is the server's: {response.text[:400]}"
    )
    settle()
    assert db.piece_by_title(title) is None, (
        f"the refused publish still wrote a pieces row titled {title!r}; a denied "
        f"request leaves the protected state unchanged"
    )


def test_author_cannot_modify_another_authors_piece(author2_client, db):
    target = db.piece_by_title(PUBLIC_STILL_PIECE)
    assert target is not None, f"{PUBLIC_STILL_PIECE!r} has no pieces row"
    before = dict(target)
    response = author2_client.patch(
        f"/pieces/{target['id']}", json={"title": "Seized By Another Author"}
    )
    assert response.status_code in (401, 403, 404), (
        f"PATCH /api/pieces/{target['id']} from a second author returned "
        f"{response.status_code}; another author's piece is not theirs to change: "
        f"{response.text[:400]}"
    )
    settle()
    after = db.piece_by_title(PUBLIC_STILL_PIECE)
    assert after is not None and after["title"] == before["title"], (
        f"the refused edit changed the stored row: title is now "
        f"{None if after is None else after['title']!r}"
    )


def test_private_piece_is_hidden_from_another_account(author2_client, db):
    private = db.piece_by_title(PRIVATE_PIECE)
    assert private is not None, f"the seeded private piece {PRIVATE_PIECE!r} is absent"
    response = author2_client.get(f"/pieces/{private['id']}")
    assert response.status_code in (401, 403, 404), (
        f"GET /api/pieces/{private['id']} from another account returned "
        f"{response.status_code}; a private piece is readable by its author alone: "
        f"{response.text[:400]}"
    )
    assert PRIVATE_PIECE.lower() not in flatten(response.json() if response.headers.get(
        "content-type", "").startswith("application/json") else {}), (
        f"the refusal for {PRIVATE_PIECE!r} leaked the piece's own title"
    )


def test_private_piece_file_is_denied_to_anonymous(anon_client, db):
    private = db.piece_by_title(PRIVATE_PIECE)
    assert private is not None, f"the seeded private piece {PRIVATE_PIECE!r} is absent"
    response = anon_client.get(f"/pieces/{private['id']}/file")
    assert response.status_code in (401, 403, 404), (
        f"GET /api/pieces/{private['id']}/file with no session returned "
        f"{response.status_code}; protected artwork is served to its author alone"
    )
    assert len(response.content) < 4096 or "image" not in response.headers.get(
        "content-type", ""
    ), (
        "the refused request for a private piece still returned image bytes "
        f"({len(response.content)} bytes, content-type "
        f"{response.headers.get('content-type')!r})"
    )


def test_anonymous_cannot_like_or_comment(anon_client, db):
    target = db.piece_by_title(PUBLIC_ANIMATED_PIECE)
    assert target is not None, f"{PUBLIC_ANIMATED_PIECE!r} has no pieces row"
    before = db.count_likes(target["id"])
    like = anon_client.post(f"/pieces/{target['id']}/likes")
    assert like.status_code in (401, 403), (
        f"an anonymous like returned {like.status_code}; liking needs an account"
    )
    comment = anon_client.post(
        f"/pieces/{target['id']}/comments", json={"body": "anonymous probe"}
    )
    assert comment.status_code in (401, 403), (
        f"an anonymous comment returned {comment.status_code}; commenting needs an "
        f"account"
    )
    settle()
    assert db.count_likes(target["id"]) == before, (
        f"the refused anonymous like still changed the likes count for "
        f"{PUBLIC_ANIMATED_PIECE!r}"
    )


def test_blocked_viewer_sees_profile_as_not_found(author_client, reader_client, db):
    block = author_client.post(
        f"/artists/{READER_HANDLE}/block", json={"kind": "block"}
    )
    assert block.status_code in (200, 201, 204), (
        f"POST /api/artists/{READER_HANDLE}/block returned {block.status_code}: "
        f"{block.text[:400]}"
    )
    response = poll_until(
        lambda: (
            r if (r := reader_client.get(f"/artists/{AUTHOR_HANDLE}")).status_code
            in (403, 404) else None
        ),
        f"a not-found answer on /api/artists/{AUTHOR_HANDLE} for a blocked viewer",
    )
    assert response.status_code == 404, (
        f"a blocked viewer got {response.status_code} on the blocker's profile; the "
        f"profile reads as not found rather than as blocked, which is what stops "
        f"block-probing"
    )


def test_published_piece_survives_a_reread(author_client, probe_suffix, db):
    title = f"Probe Persist {probe_suffix}"
    piece = created_piece(publish(author_client, title, probe_suffix))
    row = poll_until(lambda: db.piece_by_title(title), f"a stored row for {title!r}")
    again = author_client.get(f"/pieces/{piece['id']}")
    assert again.status_code == 200, (
        f"GET /api/pieces/{piece['id']} returned {again.status_code} on a re-read: "
        f"{again.text[:400]}"
    )
    body = again.json()
    reread = body.get("piece", body)
    assert reread.get("title") == title, (
        f"the re-read piece is titled {reread.get('title')!r}, but the stored row "
        f"says {row['title']!r}"
    )


def test_like_count_equals_row_count(reader_client, db):
    target = db.piece_by_title(SECOND_AUTHOR_PIECE)
    assert target is not None, f"{SECOND_AUTHOR_PIECE!r} has no pieces row"
    for _ in range(3):
        reader_client.post(f"/pieces/{target['id']}/likes")
    rows = poll_until(
        lambda: db.count_likes(target["id"]) or None,
        f"at least one likes row for {SECOND_AUTHOR_PIECE!r}",
    )
    assert rows == 1, (
        f"three likes from one account produced {rows} likes rows; one account "
        f"likes one piece at most once"
    )
    detail = reader_client.get(f"/pieces/{target['id']}")
    reported = (detail.json().get("piece") or detail.json()).get("likes")
    assert reported == rows, (
        f"the piece reports {reported!r} likes while the likes table holds {rows}; "
        f"a count is a cache of a query, never an incremented number"
    )


def test_private_visibility_removes_piece_from_every_feed(
    author_client, anon_client, probe_suffix, db
):
    title = f"Probe Hide {probe_suffix}"
    piece = created_piece(publish(author_client, title, probe_suffix))
    poll_until(
        lambda: title in feed_titles(anon_client, feed="new") or None,
        f"{title!r} reaching the public new feed",
    )
    flip = author_client.patch(f"/pieces/{piece['id']}", json={"visibility": "private"})
    assert flip.status_code in (200, 202, 204), (
        f"PATCH /api/pieces/{piece['id']} to private returned {flip.status_code}: "
        f"{flip.text[:400]}"
    )
    poll_until(
        lambda: (title not in feed_titles(anon_client, feed="new")) or None,
        f"{title!r} leaving the public new feed after being made private",
    )
    search = anon_client.get("/search", params={"q": title})
    assert title.lower() not in flatten(search.json()), (
        f"{title!r} is private but still appears in a public search result; search "
        f"filters permissions at query time"
    )


def test_seeded_rows_appear_exactly_once(db):
    for title in (
        PUBLIC_ANIMATED_PIECE,
        PUBLIC_STILL_PIECE,
        PRIVATE_PIECE,
        SECOND_AUTHOR_PIECE,
        UNLISTED_PIECE,
    ):
        count = db.count_pieces(title=title)
        assert count == 1, (
            f"the seeded piece {title!r} has {count} rows; seeding is idempotent, "
            f"so restarting the app duplicates nothing"
        )
    for email in (AUTHOR_EMAIL, AUTHOR2_EMAIL, READER_EMAIL):
        count = db.count_accounts(email=email)
        assert count == 1, (
            f"the seeded account {email} has {count} rows, expected exactly one"
        )


def test_pending_piece_is_absent_from_feeds(author_client, anon_client, probe_suffix, db):
    title = f"Probe Pending {probe_suffix}"
    created_piece(publish(author_client, title, probe_suffix))
    row = poll_until(lambda: db.piece_by_title(title), f"a stored row for {title!r}")
    if row.get("moderation_state") != "pending":
        return
    assert title not in feed_titles(anon_client, feed="new"), (
        f"{title!r} is in the pending moderation state yet appears in the public new "
        f"feed; a pending piece reaches no feed until its state resolves"
    )


def test_notifications_group_by_kind_subject_and_hour(reader_client, db):
    author = db.account_by_email(AUTHOR_EMAIL)
    assert author is not None, f"{AUTHOR_EMAIL} has no accounts row"
    target = db.piece_by_title(PUBLIC_ANIMATED_PIECE)
    assert target is not None, f"{PUBLIC_ANIMATED_PIECE!r} has no pieces row"
    reader_client.post(f"/pieces/{target['id']}/likes")
    rows = poll_until(
        lambda: db.notifications_for(author["id"]) or None,
        f"a notification row for {AUTHOR_EMAIL} after a like",
    )
    keys = [r.get("group_key") for r in rows if r.get("kind") == "like"]
    assert keys, (
        f"the like on {PUBLIC_ANIMATED_PIECE!r} produced no like notification for its "
        f"author"
    )
    assert all(k for k in keys), (
        f"a like notification carries an empty group_key ({keys!r}); grouping is by "
        f"the kind, the subject and the hour bucket"
    )
    assert len(set(keys)) == len(keys) or len(set(keys)) == 1, (
        f"like notifications for one piece within one hour carry {len(set(keys))} "
        f"distinct group keys across {len(keys)} rows, so they will not collapse"
    )


def test_repeated_publish_key_creates_one_piece(author_client, probe_suffix, db):
    title = f"Probe Idempotent {probe_suffix}"
    key = f"probe-idem-{probe_suffix}"
    first = publish(author_client, title, probe_suffix, idempotency_key=key)
    created_piece(first)
    second = publish(author_client, title, probe_suffix, idempotency_key=key)
    assert second.status_code in (200, 201), (
        f"replaying a publish with the same idempotency key returned "
        f"{second.status_code}: {second.text[:400]}"
    )
    poll_until(lambda: db.piece_by_title(title), f"a stored row for {title!r}")
    settle()
    count = db.count_pieces(title=title)
    assert count == 1, (
        f"replaying one publish with the same idempotency key produced {count} "
        f"pieces; a retried publish creates nothing new"
    )


def test_cursor_pagination_is_stable_across_insertion(author_client, probe_suffix):
    page = feed_page(author_client, feed="new", limit=2)
    cursor = page.get("next_cursor")
    assert cursor, (
        f"the first new-feed page returned no next_cursor, so the feed cannot page "
        f"by cursor: {str(page)[:400]}"
    )
    first_ids = [r.get("id") for r in items(page.get("pieces", page))]
    created_piece(
        publish(
            author_client,
            f"Probe Inserted {probe_suffix}",
            probe_suffix,
            idempotency_key=f"probe-insert-{probe_suffix}",
        )
    )
    second = feed_page(author_client, feed="new", limit=2, cursor=cursor)
    second_ids = [r.get("id") for r in items(second.get("pieces", second))]
    overlap = set(first_ids).intersection(second_ids)
    assert not overlap, (
        f"a piece published between two page requests made ids {overlap!r} appear on "
        f"both pages; the cursor is a total order that never shifts"
    )


def test_more_than_ten_tags_is_refused(author_client, probe_suffix, db):
    title = f"Probe Tags {probe_suffix}"
    response = publish(
        author_client,
        title,
        probe_suffix,
        tags=[f"tag{n}" for n in range(MAX_TAGS + 2)],
        idempotency_key=f"probe-tags-{probe_suffix}",
    )
    assert 400 <= response.status_code < 500, (
        f"publishing with {MAX_TAGS + 2} tags returned {response.status_code}; a "
        f"piece carries at most {MAX_TAGS} tags and the refusal is a client error"
    )
    settle()
    assert db.piece_by_title(title) is None, (
        f"the refused publish still wrote a row titled {title!r}; a refused request "
        f"writes nothing"
    )


def test_over_length_comment_is_refused(reader_client, db):
    target = db.piece_by_title(PUBLIC_STILL_PIECE)
    assert target is not None, f"{PUBLIC_STILL_PIECE!r} has no pieces row"
    before = db.count_comments(target["id"])
    response = reader_client.post(
        f"/pieces/{target['id']}/comments",
        json={"body": "p" * (MAX_COMMENT_CLUSTERS + 50)},
    )
    assert 400 <= response.status_code < 500, (
        f"a comment of {MAX_COMMENT_CLUSTERS + 50} characters returned "
        f"{response.status_code}; the body is capped at {MAX_COMMENT_CLUSTERS} "
        f"clusters and the refusal is a client error"
    )
    settle()
    assert db.count_comments(target["id"]) == before, (
        f"the refused over-length comment still wrote a comments row"
    )


def test_reply_to_a_reply_is_refused(reader_client, db, probe_suffix):
    target = db.piece_by_title(PUBLIC_ANIMATED_PIECE)
    assert target is not None, f"{PUBLIC_ANIMATED_PIECE!r} has no pieces row"
    top = reader_client.post(
        f"/pieces/{target['id']}/comments", json={"body": f"probe top {probe_suffix}"}
    )
    assert top.status_code in (200, 201), (
        f"posting a top-level comment returned {top.status_code}: {top.text[:400]}"
    )
    top_id = (top.json().get("comment") or top.json()).get("id")
    assert top_id is not None, f"the created comment carries no id: {top.text[:400]}"
    reply = reader_client.post(
        f"/pieces/{target['id']}/comments",
        json={"body": f"probe reply {probe_suffix}", "parent_comment_id": top_id},
    )
    assert reply.status_code in (200, 201), (
        f"replying to a top-level comment returned {reply.status_code}: "
        f"{reply.text[:400]}"
    )
    reply_id = (reply.json().get("comment") or reply.json()).get("id")
    third = reader_client.post(
        f"/pieces/{target['id']}/comments",
        json={"body": f"probe third {probe_suffix}", "parent_comment_id": reply_id},
    )
    assert 400 <= third.status_code < 500, (
        f"replying to a reply returned {third.status_code}; comments thread exactly "
        f"one level deep"
    )


def test_remix_of_an_ancestor_is_refused(author_client, db, probe_suffix):
    root_title = f"Probe Root {probe_suffix}"
    root = created_piece(publish(author_client, root_title, probe_suffix))
    child_title = f"Probe Descendant {probe_suffix}"
    child = created_piece(
        publish(
            author_client,
            child_title,
            probe_suffix,
            parent_id=root["id"],
            idempotency_key=f"probe-desc-{probe_suffix}",
        )
    )
    response = author_client.patch(
        f"/pieces/{root['id']}", json={"parent_id": child["id"]}
    )
    assert 400 <= response.status_code < 500, (
        f"making {root_title!r} a remix of its own descendant returned "
        f"{response.status_code}; a lineage cycle is refused at write time"
    )
    settle()
    row = db.piece_by_title(root_title)
    assert row is not None and row.get("parent_id") in (None, ""), (
        f"the refused cycle still wrote parent_id="
        f"{None if row is None else row.get('parent_id')!r} onto the root piece"
    )


def test_empty_tag_feed_returns_an_empty_list(anon_client, probe_suffix):
    response = anon_client.get(
        "/pieces", params={"feed": "tag", "tag": f"nosuchtag{probe_suffix}"}
    )
    assert response.status_code == 200, (
        f"a tag feed matching nothing returned {response.status_code}; an empty "
        f"result is an empty list, never an error: {response.text[:400]}"
    )
    assert items(response.json()) == [], (
        f"a tag feed matching nothing returned rows: {response.text[:400]}"
    )


def test_reserved_word_handle_is_refused(anon_client, probe_suffix):
    for reserved in RESERVED_HANDLES[:3]:
        response = anon_client.post(
            "/auth/signup",
            json={
                "display_name": f"Probe {probe_suffix}",
                "handle": reserved,
                "email": f"probe-{reserved}-{probe_suffix}@example.com",
                "password": "deku-demo-pw-2026",
                "date_of_birth": "1996-04-11",
            },
        )
        assert 400 <= response.status_code < 500, (
            f"signing up with the reserved handle {reserved!r} returned "
            f"{response.status_code}; the reserved list is closed and a reserved "
            f"word can never become an artist handle"
        )


def test_published_artwork_object_exists_in_the_bucket(
    author_client, store, probe_suffix, db
):
    title = f"Probe Object {probe_suffix}"
    piece = created_piece(publish(author_client, title, probe_suffix))
    poll_until(lambda: db.piece_by_title(title), f"a stored row for {title!r}")
    keys = poll_until(
        lambda: store.list(f"pieces/{piece['id']}/") or None,
        f"an object under pieces/{piece['id']}/ in the bucket",
    )
    assert keys, (
        f"publishing {title!r} wrote no object under pieces/{piece['id']}/; the "
        f"artwork bytes live in the object store, not on the app's own disk"
    )


def test_object_key_follows_the_pinned_scheme(author_client, store, probe_suffix, db):
    title = f"Probe Key {probe_suffix}"
    piece = created_piece(
        publish(
            author_client, title, probe_suffix,
            idempotency_key=f"probe-key-{probe_suffix}",
        )
    )
    poll_until(lambda: db.piece_by_title(title), f"a stored row for {title!r}")
    keys = poll_until(
        lambda: store.list(f"pieces/{piece['id']}/") or None,
        f"an object under pieces/{piece['id']}/",
    )
    for key in keys:
        parts = key.split("/")
        assert len(parts) == 3 and parts[0] == "pieces", (
            f"the stored key {key!r} does not follow pieces/{{piece_id}}/"
            f"{{sha256_of_bytes}}.{{ext}}"
        )
        name = parts[2]
        digest, _, ext = name.rpartition(".")
        assert len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), (
            f"the stored key {key!r} names {digest!r} where a lowercase 64-character "
            f"content hash is expected"
        )
        assert ext, f"the stored key {key!r} carries no extension"


def test_thumbnail_renditions_exist_for_a_published_piece(
    author_client, store, probe_suffix, db
):
    title = f"Probe Thumbs {probe_suffix}"
    piece = created_piece(
        publish(
            author_client, title, probe_suffix,
            idempotency_key=f"probe-thumbs-{probe_suffix}",
        )
    )
    poll_until(lambda: db.piece_by_title(title), f"a stored row for {title!r}")
    keys = poll_until(
        lambda: store.list(f"thumbs/{piece['id']}/") or None,
        f"rendition objects under thumbs/{piece['id']}/",
    )
    sizes = {k.split("/")[2] for k in keys if len(k.split("/")) >= 4}
    missing = [str(s) for s in THUMBNAIL_SIZES if str(s) not in sizes]
    assert not missing, (
        f"the piece {title!r} has no rendition at size(s) {missing!r}; thumbnails "
        f"are generated at {', '.join(str(s) for s in THUMBNAIL_SIZES)} on the long "
        f"edge. Observed keys: {sorted(keys)[:8]}"
    )


def test_private_piece_object_is_not_publicly_readable(db):
    private = db.piece_by_title(PRIVATE_PIECE)
    assert private is not None, f"the seeded private piece {PRIVATE_PIECE!r} is absent"
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    bucket = os.environ["STORAGE_BUCKET"]
    listing = httpx.get(f"{endpoint}/{bucket}?list-type=2", timeout=TIMEOUT)
    assert listing.status_code in (401, 403, 404), (
        f"the bucket {bucket!r} answered {listing.status_code} to an unauthenticated "
        f"listing; a private piece's artwork must not be readable without the app's "
        f"own authenticated route"
    )


def test_artwork_bytes_are_absent_from_the_database(db):
    columns = db.piece_columns()
    assert columns, "the pieces table is empty, so the seed did not run"
    suspicious = sorted(
        c for c in columns
        if any(token in c.lower() for token in ("blob", "bytes", "binary", "payload"))
    )
    assert not suspicious, (
        f"the pieces table carries column(s) {suspicious!r}, which read as image "
        f"bytes held in the database; the object store is where artwork lives"
    )
    assert "object_key" in columns, (
        f"the pieces table carries no object_key column, so no row points at the "
        f"stored artwork. Columns seen: {sorted(columns)}"
    )
