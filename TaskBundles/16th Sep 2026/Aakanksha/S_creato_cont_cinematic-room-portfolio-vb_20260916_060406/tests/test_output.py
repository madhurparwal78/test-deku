"""The single pytest module for deku/cinematic-room-portfolio-vb.

One merged module (CON-2 / G46). Sections are grouped by function order: public
reads, guest book, studio writes and object storage, publish and snapshot
semantics, authorization, draft privacy, and the launch surfaces. Every literal
asserted here is pinned verbatim in instruction.md; diagnostic detail lives in the
assertion messages, never in a graded position.

Each mutating test creates its own room under a fresh name or signs as a
fresh-signed-up visitor, so no test depends on another's rows; the sidecars start
from a fresh database and a fresh bucket per trial (no persistent volumes). The
seeded draft site is only ever read, never published.
"""

from __future__ import annotations

import re

from conftest import (
    DRAFT_HANDLE,
    ONE_PX_PNG_B64,
    ONE_PX_PNG_BYTES,
    PUBLISHED_HANDLE,
    fresh_visitor_client,
    note_payload,
    room_payload,
    unique_token,
)
from _shapes import flatten

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def _rooms(body) -> list:
    rooms = body.get("rooms") if isinstance(body, dict) else None
    return rooms if isinstance(rooms, list) else []


def _positions(rows) -> list:
    return [r.get("position") for r in rows if isinstance(r, dict) and "position" in r]


def _create_room(creator_client, **over) -> str:
    r = creator_client.post("/api/studio/rooms", json=room_payload(**over))
    assert r.status_code in (200, 201), (
        f"POST /api/studio/rooms returned {r.status_code}, expected 200 or 201 for a room "
        f"create: {r.text[:300]}"
    )
    room_id = r.json().get("id")
    assert room_id is not None, f"POST /api/studio/rooms returned no id: {r.text[:300]}"
    return room_id


def _put_scene(creator_client, room_id) -> str:
    r = creator_client.put(
        f"/api/studio/rooms/{room_id}/scene",
        json={"image": ONE_PX_PNG_B64, "content_type": "image/png"},
    )
    assert r.status_code in (200, 201), (
        f"PUT /api/studio/rooms/{room_id}/scene returned {r.status_code}, expected 200 or 201: "
        f"{r.text[:300]}"
    )
    key = r.json().get("object_key", "")
    assert key, f"PUT scene for room {room_id} returned no object_key: {r.text[:300]}"
    return key


def _publish(creator_client) -> None:
    r = creator_client.post("/api/studio/publish")
    assert r.status_code in (200, 201), (
        f"POST /api/studio/publish returned {r.status_code}, expected 200 or 201: {r.text[:300]}"
    )


def _first_room_id(client) -> str:
    r = client.get(f"/api/sites/{PUBLISHED_HANDLE}")
    assert r.status_code == 200, (
        f"GET /api/sites/{PUBLISHED_HANDLE} returned {r.status_code}, expected 200: {r.text[:300]}"
    )
    rooms = _rooms(r.json())
    assert rooms, f"the published site read carried no rooms: {r.text[:300]}"
    return rooms[0].get("id")



def test_health_ok(client):
    r = client.get("/api/health")
    assert r.status_code == 200, (
        f"GET /api/health returned {r.status_code}, expected 200: {r.text[:300]}"
    )


def test_published_site_lists_rooms_in_order(client):
    r = client.get(f"/api/sites/{PUBLISHED_HANDLE}")
    assert r.status_code == 200, (
        f"GET /api/sites/{PUBLISHED_HANDLE} returned {r.status_code}, expected 200: {r.text[:300]}"
    )
    rooms = _rooms(r.json())
    assert len(rooms) >= 3, (
        f"the published site read carried {len(rooms)} rooms, expected at least the three seeded "
        f"rooms: {r.text[:300]}"
    )
    positions = _positions(rooms)
    assert positions == sorted(positions), (
        f"the published rooms are not in position order: {positions}"
    )


def test_header_player_lists_releases_in_order(client):
    r = client.get(f"/api/sites/{PUBLISHED_HANDLE}")
    assert r.status_code == 200, (
        f"GET /api/sites/{PUBLISHED_HANDLE} returned {r.status_code}, expected 200: {r.text[:300]}"
    )
    releases = r.json().get("releases") if isinstance(r.json(), dict) else None
    assert isinstance(releases, list) and len(releases) >= 3, (
        f"the site read carried {releases!r} releases, expected at least the three seeded "
        f"releases in order: {r.text[:300]}"
    )
    positions = _positions(releases)
    assert positions == sorted(positions), (
        f"the releases are not in position order: {positions}"
    )



def test_visitor_signs_one_note(visitor2_client, client):
    room_id = _first_room_id(client)
    text = unique_token("note")
    r = visitor2_client.post(
        f"/api/sites/{PUBLISHED_HANDLE}/guestbook", json=note_payload(room_id, text=text)
    )
    assert r.status_code in (200, 201), (
        f"POST /api/sites/{PUBLISHED_HANDLE}/guestbook returned {r.status_code}, expected 200 or "
        f"201 for a signed-in visitor: {r.text[:300]}"
    )
    book = client.get(f"/api/sites/{PUBLISHED_HANDLE}/guestbook")
    assert book.status_code == 200, (
        f"public GET guestbook returned {book.status_code}, expected 200: {book.text[:300]}"
    )
    assert text in flatten(book.json()), (
        f"the signed note {text!r} did not appear in the public guest book: {book.text[:300]}"
    )


def test_anonymous_sign_refused(client):
    room_id = _first_room_id(client)
    r = client.post(
        f"/api/sites/{PUBLISHED_HANDLE}/guestbook",
        json=note_payload(room_id, text="anon should not persist"),
    )
    assert r.status_code in (401, 403), (
        f"anonymous POST guestbook returned {r.status_code}, expected 401 or 403 so signing "
        f"needs an account: {r.text[:300]}"
    )
    assert "not-signed-in" in flatten(r.json()), (
        f"the anonymous sign refusal did not carry the not-signed-in kind: {r.text[:300]}"
    )


def test_duplicate_note_refused(visitor_client, client):
    room_id = _first_room_id(client)
    r = visitor_client.post(
        f"/api/sites/{PUBLISHED_HANDLE}/guestbook",
        json=note_payload(room_id, text="a second note from the same visitor"),
    )
    assert r.status_code == 409, (
        f"a second sign by the seeded visitor returned {r.status_code}, expected 409 so one "
        f"visitor holds at most one standing note: {r.text[:300]}"
    )
    assert "that-clashes" in flatten(r.json()), (
        f"a duplicate sign did not carry the that-clashes kind: {r.text[:300]}"
    )


def test_sign_missing_text_refused(client):
    room_id = _first_room_id(client)
    visitor = fresh_visitor_client()
    r = visitor.post(f"/api/sites/{PUBLISHED_HANDLE}/guestbook", json={"room_id": room_id})
    visitor.close()
    assert r.status_code in (400, 422), (
        f"a sign missing the note text returned {r.status_code}, expected 400 or 422: {r.text[:300]}"
    )
    assert "something-missing-or-wrong" in flatten(r.json()), (
        f"a validation failure did not carry the something-missing-or-wrong kind: {r.text[:300]}"
    )



def test_creator_upload_writes_scene_object(creator_client, object_store):
    room_id = _create_room(creator_client, name=unique_token("room"))
    object_key = _put_scene(creator_client, room_id)
    assert object_store.exists(object_key), (
        f"the room scene image {object_key!r} was not written to the object store"
    )


def test_creator_reorders_rooms(creator_client):
    site = creator_client.get("/api/studio/site")
    assert site.status_code == 200, (
        f"GET /api/studio/site returned {site.status_code}, expected 200: {site.text[:300]}"
    )
    ids = [r.get("id") for r in _rooms(site.json())]
    assert len(ids) >= 2, f"the studio site has fewer than two rooms to reorder: {ids}"
    reversed_ids = list(reversed(ids))
    r = creator_client.post("/api/studio/rooms/order", json={"order": reversed_ids})
    assert r.status_code in (200, 201), (
        f"POST /api/studio/rooms/order returned {r.status_code}, expected 200 or 201: {r.text[:300]}"
    )
    after = creator_client.get("/api/studio/site")
    got = [r.get("id") for r in _rooms(after.json())]
    assert got == reversed_ids, (
        f"the studio rooms did not take the requested order: asked {reversed_ids}, got {got}"
    )



def test_published_scene_served_from_store(creator_client, client, object_store):
    room_id = _create_room(creator_client, name=unique_token("scene-room"))
    object_key = _put_scene(creator_client, room_id)
    _publish(creator_client)
    assert object_store.exists(object_key), (
        f"the scene object {object_key!r} was not found in the store after publish"
    )
    got = client.get(f"/api/sites/{PUBLISHED_HANDLE}/rooms/{room_id}/scene")
    assert got.status_code == 200, (
        f"public GET scene for the published room returned {got.status_code}, expected 200 "
        f"streaming the stored object: {got.text[:300]}"
    )
    assert got.content == ONE_PX_PNG_BYTES, (
        f"the scene endpoint served {len(got.content)} bytes that do not match the "
        f"{len(ONE_PX_PNG_BYTES)} bytes written to the stored object; the image a page shows "
        f"must be the object under the room key, not bytes cached elsewhere"
    )


def test_publish_copies_working_copy_to_snapshot(creator_client, client):
    marker = unique_token("published-name")
    _create_room(creator_client, name=marker)
    _publish(creator_client)
    site = client.get(f"/api/sites/{PUBLISHED_HANDLE}")
    assert site.status_code == 200, (
        f"public GET site after publish returned {site.status_code}, expected 200: {site.text[:300]}"
    )
    assert marker in flatten(site.json()), (
        f"the newly published room {marker!r} did not appear on the public site after publish: "
        f"{site.text[:300]}"
    )


def test_edit_after_publish_hidden_until_republish(creator_client, client):
    room_id = _create_room(creator_client, sentence="the first published sentence")
    _publish(creator_client)
    edited = unique_token("edited-sentence")
    patch = creator_client.patch(f"/api/studio/rooms/{room_id}", json={"sentence": edited})
    assert patch.status_code in (200, 201), (
        f"PATCH /api/studio/rooms/{room_id} returned {patch.status_code}, expected 200 or 201: "
        f"{patch.text[:300]}"
    )
    before = client.get(f"/api/sites/{PUBLISHED_HANDLE}")
    assert edited not in flatten(before.json()), (
        f"the edited sentence {edited!r} reached the public site before a republish; a dirty "
        f"edit must stay off the public read until the next publish"
    )
    _publish(creator_client)
    after = client.get(f"/api/sites/{PUBLISHED_HANDLE}")
    assert edited in flatten(after.json()), (
        f"the edited sentence {edited!r} did not reach the public site after republish: "
        f"{after.text[:300]}"
    )


def test_public_read_reconciles_snapshot(creator_client, client, store):
    _publish(creator_client)
    site = store.one("sites", handle=PUBLISHED_HANDLE)
    assert site and site.get("id") is not None, (
        f"the {PUBLISHED_HANDLE!r} site row was not found in the database"
    )
    room_rows = store.count("rooms", site_id=site["id"])
    public = client.get(f"/api/sites/{PUBLISHED_HANDLE}")
    listed = len(_rooms(public.json()))
    assert listed == room_rows, (
        f"the public site read listed {listed} rooms but the database holds {room_rows} rooms for "
        f"the published site; the public read must reconcile with the rows"
    )



def test_studio_denied_to_anonymous(client):
    r = client.get("/api/studio/site")
    assert r.status_code in (401, 403), (
        f"anonymous GET /api/studio/site returned {r.status_code}, expected 401 or 403 so a "
        f"studio endpoint is never open: {r.text[:300]}"
    )
    assert "not-signed-in" in flatten(r.json()), (
        f"the anonymous studio refusal did not carry the not-signed-in kind: {r.text[:300]}"
    )


def test_studio_denied_to_visitor(visitor_client):
    r = visitor_client.get("/api/studio/site")
    assert r.status_code == 403, (
        f"a visitor GET /api/studio/site returned {r.status_code}, expected 403 so the studio is "
        f"closed to a visitor: {r.text[:300]}"
    )
    assert "not-allowed-for-you" in flatten(r.json()), (
        f"a visitor studio refusal did not carry the not-allowed-for-you kind: {r.text[:300]}"
    )


def test_creator_cannot_write_others_site(creator2_client, client):
    room_id = _first_room_id(client)
    r = creator2_client.patch(
        f"/api/studio/rooms/{room_id}", json={"sentence": "a sentence from the wrong owner"}
    )
    assert r.status_code == 403, (
        f"a creator patching a room on a site the caller does not own returned {r.status_code}, "
        f"expected 403: {r.text[:300]}"
    )
    assert "not-allowed-for-you" in flatten(r.json()), (
        f"a cross-owner write refusal did not carry the not-allowed-for-you kind: {r.text[:300]}"
    )



def test_draft_site_read_not_found(client):
    r = client.get(f"/api/sites/{DRAFT_HANDLE}")
    assert r.status_code == 404, (
        f"public GET /api/sites/{DRAFT_HANDLE} for a draft site returned {r.status_code}, "
        f"expected 404: {r.text[:300]}"
    )
    assert "no-such-thing" in flatten(r.json()), (
        f"a draft site read did not carry the no-such-thing kind: {r.text[:300]}"
    )


def test_draft_scene_not_public(client, creator2_client):
    site = creator2_client.get("/api/studio/site")
    assert site.status_code == 200, (
        f"GET /api/studio/site for the draft owner returned {site.status_code}, expected 200: "
        f"{site.text[:300]}"
    )
    rooms = _rooms(site.json())
    assert rooms, f"the draft site carried no rooms to read a scene from: {site.text[:300]}"
    room_id = rooms[0].get("id")
    r = client.get(f"/api/sites/{DRAFT_HANDLE}/rooms/{room_id}/scene")
    assert r.status_code == 404, (
        f"public GET scene for a draft room returned {r.status_code}, expected 404 so a draft "
        f"scene is not publicly readable: {r.text[:300]}"
    )
    assert "no-such-thing" in flatten(r.json()), (
        f"a draft scene read did not carry the no-such-thing kind: {r.text[:300]}"
    )



def test_creator_hides_note_off_public_book(creator_client, client):
    text = unique_token("hide-note")
    visitor = fresh_visitor_client()
    room_id = _first_room_id(client)
    signed = visitor.post(
        f"/api/sites/{PUBLISHED_HANDLE}/guestbook", json=note_payload(room_id, text=text)
    )
    visitor.close()
    assert signed.status_code in (200, 201), (
        f"a fresh visitor sign returned {signed.status_code}, expected 200 or 201: {signed.text[:300]}"
    )
    note_id = signed.json().get("id")
    assert note_id is not None, f"a signed note returned no id: {signed.text[:300]}"
    assert text in flatten(client.get(f"/api/sites/{PUBLISHED_HANDLE}/guestbook").json()), (
        f"the note {text!r} did not appear in the public book before hiding"
    )
    r = creator_client.post(f"/api/studio/guestbook/{note_id}/hide")
    assert r.status_code in (200, 201), (
        f"POST hide for note {note_id} returned {r.status_code}, expected 200 or 201: {r.text[:300]}"
    )
    assert text not in flatten(client.get(f"/api/sites/{PUBLISHED_HANDLE}/guestbook").json()), (
        f"the hidden note {text!r} still appears in the public guest book"
    )


def test_creator_restores_hidden_note(creator_client, client):
    text = unique_token("restore-note")
    visitor = fresh_visitor_client()
    room_id = _first_room_id(client)
    signed = visitor.post(
        f"/api/sites/{PUBLISHED_HANDLE}/guestbook", json=note_payload(room_id, text=text)
    )
    visitor.close()
    note_id = signed.json().get("id")
    assert note_id is not None, f"a signed note returned no id: {signed.text[:300]}"
    hide = creator_client.post(f"/api/studio/guestbook/{note_id}/hide")
    assert hide.status_code in (200, 201), (
        f"POST hide for note {note_id} returned {hide.status_code}: {hide.text[:300]}"
    )
    r = creator_client.post(f"/api/studio/guestbook/{note_id}/restore")
    assert r.status_code in (200, 201), (
        f"POST restore for note {note_id} returned {r.status_code}, expected 200 or 201: {r.text[:300]}"
    )
    assert text in flatten(client.get(f"/api/sites/{PUBLISHED_HANDLE}/guestbook").json()), (
        f"the restored note {text!r} did not return to the public guest book"
    )



def test_privacy_page_reachable(client):
    r = client.get("/privacy")
    assert r.status_code == 200, (
        f"GET /privacy returned {r.status_code}, expected 200: {r.text[:200]}"
    )
    home = client.get("/")
    assert home.status_code == 200, (
        f"GET / returned {home.status_code}, expected 200: {home.text[:200]}"
    )
    assert "/privacy" in home.text, (
        "the home page carries no footer link to /privacy"
    )


def test_public_routes_have_distinct_titles(client):
    titles = []
    for path in ("/", "/privacy", "/sign-in"):
        r = client.get(path)
        assert r.status_code == 200, (
            f"GET {path} returned {r.status_code}, expected 200: {r.text[:200]}"
        )
        m = TITLE_RE.search(r.text)
        assert m, f"GET {path} returned a document with no title element"
        titles.append(m.group(1).strip().lower())
    assert len(set(titles)) == len(titles), (
        f"two public routes share a document title: {titles}"
    )


def test_sitemap_lists_public_routes(client):
    r = client.get("/sitemap.xml")
    assert r.status_code == 200, (
        f"GET /sitemap.xml returned {r.status_code}, expected 200: {r.text[:200]}"
    )
    assert "/privacy" in r.text, (
        f"the sitemap does not list the /privacy route: {r.text[:300]}"
    )
