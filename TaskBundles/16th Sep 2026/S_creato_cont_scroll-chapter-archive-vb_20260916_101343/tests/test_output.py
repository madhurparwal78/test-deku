"""The single pytest module for deku/scroll-chapter-archive-vb.

One merged module (CON-2 / G46). Every literal asserted here is pinned verbatim
in instruction.md; diagnostic detail lives in the assertion messages, never in a
graded position.

Each capture and route test uses a fresh title or a fresh route, the curator
publishes only the draft chapter bone (the draft chapter forest-landscape is only
ever read), so no test depends on another's rows; the sidecars start from a fresh
database and a fresh bucket per trial.
"""

from __future__ import annotations

import re

from conftest import (
    DRAFT_STAYS,
    DRAFT_TO_PUBLISH,
    MEMBER_EMAIL,
    PUBLISHED_CHAPTER,
    SEEDED_POSITION,
    fresh_client,
    login_client,
    unique_token,
)
from _shapes import flatten

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def _ids(listing) -> list:
    return [r.get("id") for r in listing if isinstance(r, dict) and "id" in r]


def _archive(member_client) -> dict:
    r = member_client.get("/api/me/archive")
    assert r.status_code == 200, (
        f"GET /api/me/archive returned {r.status_code}, expected 200: {r.text[:300]}"
    )
    return r.json()


def _capture_ids(member_client) -> list:
    caps = _archive(member_client).get("captures") or []
    return [c.get("id") for c in caps]


def test_health_ok(client):
    r = client.get("/api/health")
    assert r.status_code == 200, (
        f"GET /api/health returned {r.status_code}, expected 200: {r.text[:300]}"
    )


def test_chapters_list_published_only(client):
    r = client.get("/api/chapters")
    assert r.status_code == 200, (
        f"GET /api/chapters returned {r.status_code}, expected 200: {r.text[:300]}"
    )
    ids = _ids(r.json())
    assert PUBLISHED_CHAPTER in ids, (
        f"GET /api/chapters did not list the seeded published chapter {PUBLISHED_CHAPTER!r}: {r.text[:300]}"
    )
    assert DRAFT_STAYS not in ids, (
        f"GET /api/chapters listed the draft chapter {DRAFT_STAYS!r}, which must never be public: {r.text[:300]}"
    )


def test_chapter_poster_image_from_store(client, object_store):
    got = client.get(f"/api/chapters/{PUBLISHED_CHAPTER}/poster")
    assert got.status_code == 200, (
        f"public GET poster for {PUBLISHED_CHAPTER} returned {got.status_code}, expected 200 "
        f"streaming the stored object: {got.text[:300]}"
    )
    assert got.content, "the poster endpoint served an empty body"
    stored = object_store.list(f"posters/{PUBLISHED_CHAPTER}/")
    assert stored, (
        f"no poster object is stored under posters/{PUBLISHED_CHAPTER}/ in the object store; the "
        f"image a page shows must be the object under the chapter key, not bytes cached elsewhere"
    )


def test_curator_publishes_chapter(curator_client, client):
    before = client.get("/api/chapters")
    assert DRAFT_TO_PUBLISH not in _ids(before.json()), (
        f"chapter {DRAFT_TO_PUBLISH} is public before it is published: {before.text[:300]}"
    )
    r = curator_client.post(f"/api/chapters/{DRAFT_TO_PUBLISH}/publish")
    assert r.status_code in (200, 201), (
        f"curator publish of {DRAFT_TO_PUBLISH} returned {r.status_code}, expected 200 or 201: {r.text[:300]}"
    )
    after = client.get("/api/chapters")
    assert DRAFT_TO_PUBLISH in _ids(after.json()), (
        f"chapter {DRAFT_TO_PUBLISH} did not appear in the public story after publish: {after.text[:300]}"
    )


def test_member_captures_a_frame(member_client, store):
    title = unique_token("frame")
    r = member_client.post(
        "/api/captures", json={"title": title, "chapter_id": PUBLISHED_CHAPTER, "position": 0.3}
    )
    assert r.status_code == 201, (
        f"POST /api/captures returned {r.status_code}, expected 201: {r.text[:300]}"
    )
    rows = store.rows("captures", title=title)
    assert len(rows) == 1, f"expected exactly one capture row titled {title!r}, found {len(rows)}"
    assert rows[0].get("chapter_id") == PUBLISHED_CHAPTER, (
        f"the capture row recorded chapter_id {rows[0].get('chapter_id')!r}, expected {PUBLISHED_CHAPTER!r}"
    )


def test_capture_missing_title_refused(member_client):
    r = member_client.post("/api/captures", json={"chapter_id": PUBLISHED_CHAPTER, "position": 0.2})
    assert r.status_code in (400, 422), (
        f"POST /api/captures with no title returned {r.status_code}, expected 400 or 422: {r.text[:300]}"
    )
    assert "something-missing-or-wrong" in flatten(r.json()), (
        f"a validation failure did not carry the something-missing-or-wrong kind: {r.text[:300]}"
    )


def test_archive_and_position_persist_across_session(member_client):
    put = member_client.put("/api/me/position", json={"position": 0.6})
    assert put.status_code in (200, 201), (
        f"PUT /api/me/position returned {put.status_code}, expected 200 or 201: {put.text[:300]}"
    )
    fresh = login_client(MEMBER_EMAIL)
    me = fresh.get("/api/me")
    archive = fresh.get("/api/me/archive")
    fresh.close()
    assert me.status_code == 200, f"fresh GET /api/me returned {me.status_code}: {me.text[:300]}"
    assert abs(float(me.json().get("last_position")) - 0.6) < 1e-6, (
        f"a fresh session read last_position {me.json().get('last_position')!r}, expected 0.6; the "
        f"reading position must be held server-side"
    )
    assert (archive.json().get("captures") or []), (
        f"a fresh session read an empty archive for the seeded member: {archive.text[:300]}"
    )


def test_member_reorders_route_captures(member_client):
    routes = _archive(member_client).get("routes") or []
    target = next((r for r in routes if r.get("status") == "published"), None)
    assert target is not None, "the seeded member has no published route to reorder"
    detail = member_client.get(f"/api/routes/{target['id']}")
    assert detail.status_code == 200, (
        f"owner GET /api/routes/{target['id']} returned {detail.status_code}, expected 200: {detail.text[:300]}"
    )
    caps = detail.json().get("captures") or []
    order = [c.get("id") for c in caps]
    assert len(order) >= 2, f"the published route holds fewer than two captures: {order}"
    reversed_order = list(reversed(order))
    r = member_client.post(f"/api/routes/{target['id']}/order", json={"capture_ids": reversed_order})
    assert r.status_code in (200, 201), (
        f"POST /api/routes/{target['id']}/order returned {r.status_code}, expected 200 or 201: {r.text[:300]}"
    )
    after = member_client.get(f"/api/routes/{target['id']}")
    got = [c.get("id") for c in (after.json().get("captures") or [])]
    assert got == reversed_order, (
        f"the route captures did not take the requested order: asked {reversed_order}, got {got}"
    )


def test_member_publishes_route_to_index(member_client, client):
    caps = _capture_ids(member_client)
    assert len(caps) >= 2, f"the seeded member has fewer than two captures: {caps}"
    name = unique_token("route")
    created = member_client.post("/api/routes", json={"name": name, "capture_ids": caps[:2]})
    assert created.status_code == 201, (
        f"POST /api/routes returned {created.status_code}, expected 201: {created.text[:300]}"
    )
    route_id = created.json().get("id")
    pub = member_client.post(f"/api/routes/{route_id}/publish")
    assert pub.status_code in (200, 201), (
        f"POST /api/routes/{route_id}/publish returned {pub.status_code}, expected 200 or 201: {pub.text[:300]}"
    )
    index = client.get("/api/routes")
    assert route_id in _ids(index.json()), (
        f"the published route {name!r} did not appear on the public index: {index.text[:300]}"
    )


def test_route_publish_below_two_refused(member_client):
    caps = _capture_ids(member_client)
    assert caps, "the seeded member has no captures to build a route from"
    created = member_client.post(
        "/api/routes", json={"name": unique_token("solo"), "capture_ids": caps[:1]}
    )
    assert created.status_code == 201, (
        f"creating a one-capture draft route returned {created.status_code}, expected 201: {created.text[:300]}"
    )
    route_id = created.json().get("id")
    r = member_client.post(f"/api/routes/{route_id}/publish")
    assert r.status_code == 409, (
        f"publishing a one-capture route returned {r.status_code}, expected 409 so a route holding "
        f"fewer than two captures is refused: {r.text[:300]}"
    )
    assert "the-rules-dont-allow-that" in flatten(r.json()), (
        f"an undersized route publish did not carry the the-rules-dont-allow-that kind: {r.text[:300]}"
    )


def test_curator_features_a_route(curator_client, client):
    index = client.get("/api/routes")
    published = _ids(index.json())
    assert published, "there is no published route to feature"
    route_id = published[0]
    r = curator_client.post(f"/api/routes/{route_id}/feature")
    assert r.status_code in (200, 201), (
        f"curator feature of route {route_id} returned {r.status_code}, expected 200 or 201: {r.text[:300]}"
    )
    assert r.json().get("status") == "featured", (
        f"the featured route read back status {r.json().get('status')!r}, expected 'featured'"
    )


def test_public_story_reconciles_rows(client, store):
    r = client.get("/api/chapters")
    listed = len(_ids(r.json()))
    published_rows = store.count("chapters", state="published")
    assert listed == published_rows, (
        f"GET /api/chapters listed {listed} chapters but the database holds {published_rows} published "
        f"rows; the public story must reconcile with the rows"
    )


def test_cookie_choice_persists(client):
    fresh = fresh_client()
    first = fresh.get("/")
    fresh.close()
    assert first.status_code == 200, f"GET / returned {first.status_code}: {first.text[:200]}"
    assert "non-essential cookies" in first.text.lower(), (
        "a first visit with no cookie_choice cookie did not show the non-essential cookies notice"
    )
    remembered = fresh_client()
    second = remembered.get("/", cookies={"cookie_choice": "accepted"})
    remembered.close()
    assert "non-essential cookies" not in second.text.lower(), (
        "a request carrying the cookie_choice cookie still showed the cookie notice"
    )


def test_member_endpoint_denied_to_anonymous(client):
    r = client.get("/api/me/archive")
    assert r.status_code in (401, 403), (
        f"anonymous GET /api/me/archive returned {r.status_code}, expected 401 or 403 so a member "
        f"endpoint is never open: {r.text[:300]}"
    )
    assert "not-signed-in" in flatten(r.json()), (
        f"the anonymous member refusal did not carry the not-signed-in kind: {r.text[:300]}"
    )


def test_curator_endpoint_denied_to_member(member_client):
    r = member_client.post(f"/api/chapters/{DRAFT_STAYS}/publish")
    assert r.status_code == 403, (
        f"a member publishing a chapter returned {r.status_code}, expected 403 so a curator endpoint "
        f"is closed to a member: {r.text[:300]}"
    )
    assert "not-allowed-for-you" in flatten(r.json()), (
        f"a member curator refusal did not carry the not-allowed-for-you kind: {r.text[:300]}"
    )


def test_member_cannot_write_others_route(member2_client, member_client):
    routes = _archive(member_client).get("routes") or []
    target = next((r for r in routes if r.get("status") in ("published", "featured")), None)
    assert target is not None, "the seeded member has no published route to target"
    r = member2_client.post(
        f"/api/routes/{target['id']}/order", json={"capture_ids": ["not-a-real-capture"]}
    )
    assert r.status_code == 403, (
        f"a member reordering a route they do not own returned {r.status_code}, expected 403: {r.text[:300]}"
    )
    assert "not-allowed-for-you" in flatten(r.json()), (
        f"a cross-owner route write refusal did not carry the not-allowed-for-you kind: {r.text[:300]}"
    )


def test_draft_chapter_read_not_found(client):
    r = client.get(f"/api/chapters/{DRAFT_STAYS}")
    assert r.status_code == 404, (
        f"public GET /api/chapters/{DRAFT_STAYS} for a draft chapter returned {r.status_code}, expected 404: {r.text[:300]}"
    )
    assert "no-such-thing" in flatten(r.json()), (
        f"a draft chapter read did not carry the no-such-thing kind: {r.text[:300]}"
    )


def test_draft_chapter_poster_not_public(client):
    r = client.get(f"/api/chapters/{DRAFT_STAYS}/poster")
    assert r.status_code == 404, (
        f"public GET poster for the draft chapter {DRAFT_STAYS} returned {r.status_code}, expected 404 "
        f"so protected content is not publicly readable: {r.text[:300]}"
    )
    assert "no-such-thing" in flatten(r.json()), (
        f"a draft poster read did not carry the no-such-thing kind: {r.text[:300]}"
    )


def test_draft_route_not_public(client, member_client):
    routes = _archive(member_client).get("routes") or []
    draft = next((r for r in routes if r.get("status") == "draft"), None)
    assert draft is not None, "the seeded member has no draft route"
    r = client.get(f"/api/routes/{draft['id']}")
    assert r.status_code == 404, (
        f"anonymous GET /api/routes/{draft['id']} for a draft route returned {r.status_code}, expected 404: {r.text[:300]}"
    )
    assert "no-such-thing" in flatten(r.json()), (
        f"a draft route read did not carry the no-such-thing kind: {r.text[:300]}"
    )


def test_public_routes_have_distinct_titles(client):
    titles = []
    for path in ("/", "/routes", "/privacy"):
        r = client.get(path)
        assert r.status_code == 200, f"GET {path} returned {r.status_code}: {r.text[:200]}"
        m = TITLE_RE.search(r.text)
        assert m, f"GET {path} returned a document with no title element"
        titles.append(m.group(1).strip().lower())
    assert len(set(titles)) == len(titles), f"two public routes share a document title: {titles}"


def test_responses_carry_security_headers(client):
    r = client.get("/")
    assert r.status_code == 200, f"GET / returned {r.status_code}: {r.text[:200]}"
    headers = {k.lower(): v.lower() for k, v in r.headers.items()}
    assert "strict-transport-security" in headers, (
        "the response carries no strict transport policy header"
    )
    assert headers.get("x-content-type-options") == "nosniff", (
        f"the response x-content-type-options is {headers.get('x-content-type-options')!r}, expected nosniff"
    )


def test_no_frontend_secrets(client):
    for path in ("/", "/routes"):
        r = client.get(path)
        body = r.text
        assert "deku-secret-3d81f7a2" not in body, (
            f"GET {path} leaked the object-store secret key into the browser download"
        )
        assert "deku-demo-pw-2026" not in body, (
            f"GET {path} leaked a seeded password into the browser download"
        )


def test_public_routes_declare_social_preview(client):
    r = client.get("/")
    body = r.text.lower()
    assert "og:title" in body, "the home document declares no social preview title"
    assert "og:image" in body, "the home document declares no social preview image"
