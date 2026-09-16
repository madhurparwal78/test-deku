"""The single pytest module for deku/residence-availability-catalogue-vb.

One merged module (CON-2 / G46). Every literal asserted here is pinned verbatim
in instruction.md; diagnostic detail lives in the assertion messages, never in a
graded position.

Each callback test uses a fresh caller email and the availability-mutating tests
target distinct seeded apartments, so no test depends on another's rows; the
sidecars start from a fresh database and a fresh bucket per trial. The coming-soon
apartments 222 and 223 are only ever read, never released.
"""

from __future__ import annotations

import re

from conftest import (
    COMING_SOON_DETAIL,
    COMING_SOON_PLAN,
    COMING_SOON_RELEASE,
    RELEASED_UNIT,
    SOLD_UNIT,
    callback_payload,
    fresh_client,
    unique_token,
)
from _shapes import flatten

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def _ids(listing) -> list:
    return [r.get("id") for r in listing if isinstance(r, dict) and "id" in r]


def test_health_ok(client):
    r = client.get("/api/health")
    assert r.status_code == 200, (
        f"GET /api/health returned {r.status_code}, expected 200: {r.text[:300]}"
    )


def test_units_list_released_only(client):
    r = client.get("/api/units")
    assert r.status_code == 200, (
        f"GET /api/units returned {r.status_code}, expected 200: {r.text[:300]}"
    )
    ids = _ids(r.json())
    assert ids, f"GET /api/units returned no released apartments: {r.text[:300]}"
    for coming in (COMING_SOON_RELEASE, COMING_SOON_DETAIL, COMING_SOON_PLAN):
        assert coming not in ids, (
            f"GET /api/units listed the coming-soon apartment {coming!r}, which must never be "
            f"public: {r.text[:300]}"
        )


def test_units_filter_type_and_bedrooms(client):
    r = client.get("/api/units", params={"type": "penthouse-duplex"})
    assert r.status_code == 200, (
        f"GET /api/units?type=penthouse-duplex returned {r.status_code}, expected 200: {r.text[:300]}"
    )
    rows = r.json()
    assert rows, "the penthouse-duplex filter returned no apartments"
    assert all(row.get("typology") == "penthouse-duplex" for row in rows), (
        f"GET /api/units?type=penthouse-duplex returned an apartment of another typology: {r.text[:300]}"
    )
    combined = client.get("/api/units", params={"type": "ground-floor-basement", "bedrooms": "2"})
    assert combined.status_code == 200, (
        f"combined filter returned {combined.status_code}, expected 200: {combined.text[:300]}"
    )
    assert combined.json() == [], (
        f"GET /api/units?type=ground-floor-basement&bedrooms=2 returned apartments, but the "
        f"basement typology is a three-bedroom, so an AND of the two filters is empty: {combined.text[:300]}"
    )


def test_sort_area_asc_interior_only(client):
    r = client.get("/api/units", params={"sort": "area-asc"})
    assert r.status_code == 200, (
        f"GET /api/units?sort=area-asc returned {r.status_code}, expected 200: {r.text[:300]}"
    )
    rows = r.json()
    areas = [row.get("interior_area") for row in rows]
    assert areas == sorted(areas), (
        f"GET /api/units?sort=area-asc is not ordered by interior area: {areas}"
    )
    by_id = {row.get("id"): row for row in rows}
    if "114" in by_id and "012" in by_id:
        pos_114 = next(i for i, row in enumerate(rows) if row.get("id") == "114")
        pos_012 = next(i for i, row in enumerate(rows) if row.get("id") == "012")
        assert pos_114 < pos_012, (
            f"apartment 114 with a 151 terrace and an 89 interior sorted after apartment 012 with a "
            f"132 interior; the area sort must order by interior area alone"
        )


def test_unit_detail_reads_in_full(client):
    r = client.get(f"/api/units/{RELEASED_UNIT}")
    assert r.status_code == 200, (
        f"GET /api/units/{RELEASED_UNIT} returned {r.status_code}, expected 200: {r.text[:300]}"
    )
    body = r.json()
    for field in ("typology", "bedrooms", "interior_area", "plans"):
        assert field in body, (
            f"the apartment read is missing the {field!r} field: {r.text[:300]}"
        )
    assert isinstance(body.get("plans"), list) and body["plans"], (
        f"the apartment {RELEASED_UNIT} read carried no floor plans: {r.text[:300]}"
    )


def test_unit_floorplan_image_from_store(client, object_store):
    detail = client.get(f"/api/units/{RELEASED_UNIT}")
    assert detail.status_code == 200, (
        f"GET /api/units/{RELEASED_UNIT} returned {detail.status_code}, expected 200: {detail.text[:300]}"
    )
    plans = detail.json().get("plans") or []
    assert plans, f"apartment {RELEASED_UNIT} has no floor plans to read: {detail.text[:300]}"
    index = plans[0].get("index")
    got = client.get(f"/api/units/{RELEASED_UNIT}/plans/{index}/image")
    assert got.status_code == 200, (
        f"public GET floor plan for {RELEASED_UNIT} returned {got.status_code}, expected 200 "
        f"streaming the stored object: {got.text[:300]}"
    )
    assert got.content, "the floor plan endpoint served an empty body"
    stored = object_store.list(f"plans/{RELEASED_UNIT}/")
    assert stored, (
        f"no floor plan object is stored under plans/{RELEASED_UNIT}/ in the object store; the "
        f"image a page shows must be the object under the plan key, not bytes cached elsewhere"
    )


def test_callback_records_unit_and_contact(client, store):
    payload = callback_payload()
    r = client.post("/api/callbacks", json=payload)
    assert r.status_code == 201, (
        f"POST /api/callbacks returned {r.status_code}, expected 201: {r.text[:300]}"
    )
    rows = store.rows("callbacks", email=payload["email"])
    assert len(rows) == 1, (
        f"expected exactly one callback row for {payload['email']!r}, found {len(rows)}"
    )
    assert str(rows[0].get("unit_id")) == payload["unit_id"], (
        f"the callback row recorded unit_id {rows[0].get('unit_id')!r}, expected {payload['unit_id']!r}"
    )


def test_callback_missing_field_refused(client, store):
    r = client.post("/api/callbacks", json={"name": "No Email Given"})
    assert r.status_code in (400, 422), (
        f"POST /api/callbacks with a missing-field payload returned {r.status_code}, expected 400 "
        f"or 422: {r.text[:300]}"
    )
    assert "something-missing-or-wrong" in flatten(r.json()), (
        f"a validation failure did not carry the something-missing-or-wrong kind: {r.text[:300]}"
    )


def test_sales_reads_callbacks(sales_client, client):
    payload = callback_payload()
    made = client.post("/api/callbacks", json=payload)
    assert made.status_code == 201, (
        f"seeding a callback returned {made.status_code}, expected 201: {made.text[:300]}"
    )
    r = sales_client.get("/api/sales/callbacks")
    assert r.status_code == 200, (
        f"sales GET /api/sales/callbacks returned {r.status_code}, expected 200: {r.text[:300]}"
    )
    assert isinstance(r.json(), list), (
        f"sales GET /api/sales/callbacks did not return a JSON array: {r.text[:300]}"
    )
    assert payload["email"] in flatten(r.json()), (
        f"the sales callbacks read did not include the submitted request {payload['email']!r}: {r.text[:300]}"
    )


def test_public_index_reconciles_rows(client, store):
    r = client.get("/api/units")
    assert r.status_code == 200, (
        f"GET /api/units returned {r.status_code}, expected 200: {r.text[:300]}"
    )
    listed = len(_ids(r.json()))
    total = store.count("units")
    coming = store.count("units", availability="coming_soon")
    assert listed == total - coming, (
        f"GET /api/units listed {listed} apartments but the database holds {total} apartments of "
        f"which {coming} are coming soon; the public index must reconcile with the released rows"
    )


def test_sales_releases_unit_to_public(sales_client, client):
    before = client.get("/api/units")
    assert COMING_SOON_RELEASE not in _ids(before.json()), (
        f"apartment {COMING_SOON_RELEASE} is public before release: {before.text[:300]}"
    )
    r = sales_client.patch(
        f"/api/sales/units/{COMING_SOON_RELEASE}/availability", json={"availability": "available"}
    )
    assert r.status_code in (200, 201), (
        f"PATCH availability for {COMING_SOON_RELEASE} returned {r.status_code}, expected 200 or 201: "
        f"{r.text[:300]}"
    )
    after = client.get("/api/units")
    assert COMING_SOON_RELEASE in _ids(after.json()), (
        f"apartment {COMING_SOON_RELEASE} did not appear in the public index after release: {after.text[:300]}"
    )


def test_illegal_availability_step_refused(sales_client):
    r = sales_client.patch(
        f"/api/sales/units/{SOLD_UNIT}/availability", json={"availability": "available"}
    )
    assert r.status_code == 409, (
        f"moving the sold apartment {SOLD_UNIT} back to available returned {r.status_code}, expected "
        f"409 so an illegal availability step is refused: {r.text[:300]}"
    )
    assert "the-rules-dont-allow-that" in flatten(r.json()), (
        f"an illegal availability step did not carry the the-rules-dont-allow-that kind: {r.text[:300]}"
    )


def test_coming_soon_detail_not_found(client):
    r = client.get(f"/api/units/{COMING_SOON_DETAIL}")
    assert r.status_code == 404, (
        f"public GET /api/units/{COMING_SOON_DETAIL} for a coming-soon apartment returned "
        f"{r.status_code}, expected 404: {r.text[:300]}"
    )
    assert "no-such-thing" in flatten(r.json()), (
        f"a coming-soon apartment read did not carry the no-such-thing kind: {r.text[:300]}"
    )


def test_coming_soon_floorplan_not_public(client):
    plan_index = 1
    r = client.get(f"/api/units/{COMING_SOON_PLAN}/plans/{plan_index}/image")
    assert r.status_code == 404, (
        f"public GET floor plan for the coming-soon apartment {COMING_SOON_PLAN} returned "
        f"{r.status_code}, expected 404 so protected content is not publicly readable: {r.text[:300]}"
    )
    assert "no-such-thing" in flatten(r.json()), (
        f"a coming-soon floor plan read did not carry the no-such-thing kind: {r.text[:300]}"
    )


def test_sales_endpoint_denied_to_anonymous(client):
    r = client.get("/api/sales/callbacks")
    assert r.status_code in (401, 403), (
        f"anonymous GET /api/sales/callbacks returned {r.status_code}, expected 401 or 403 so a "
        f"sales endpoint is never open: {r.text[:300]}"
    )
    assert "not-signed-in" in flatten(r.json()), (
        f"the anonymous sales refusal did not carry the not-signed-in kind: {r.text[:300]}"
    )


def test_cookie_choice_persists(client):
    fresh = fresh_client()
    first = fresh.get("/")
    fresh.close()
    assert first.status_code == 200, (
        f"GET / returned {first.status_code}, expected 200: {first.text[:200]}"
    )
    assert "non-essential cookies" in first.text.lower(), (
        "a first visit with no cookie_choice cookie did not show the non-essential cookies notice"
    )
    remembered = fresh_client()
    second = remembered.get("/", cookies={"cookie_choice": "accepted"})
    remembered.close()
    assert "non-essential cookies" not in second.text.lower(), (
        "a request carrying the cookie_choice cookie still showed the cookie notice; the choice "
        "must survive a reload"
    )


def test_public_routes_have_distinct_titles(client):
    titles = []
    for path in ("/", "/apartments", "/contact"):
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
