"""Observations for deku/consumer-device-catalogue-vb.

One module, every section and both declared slots. Each assertion reaches the
deployed app over HTTP, the datastore through the backend capability, or the
mail server through the inbox capability. Nothing reads the agent's source.
"""

from __future__ import annotations

import httpx
from _shapes import items
from appclient import client, login
from conftest import (
    ARC_BUDS_SLUG,
    ARC_WATCH_SLUG,
    CREDENTIAL_MARKERS,
    DIRECT_VARIANTS,
    EARBUD_SLUG,
    EMPTY_FAMILY,
    FAMILIES,
    FLAGSHIP_SLUG,
    HANDOFF_VARIANTS,
    HEADPHONE_SLUG,
    LARGE_CAPACITY,
    LOGIN_FAILURE_WORDING,
    MISSING_PAIR,
    OWNER2_EMAIL,
    OWNER_EMAIL,
    PRODUCT_SLUGS,
    PUBLIC_ROUTES,
    REFERENCE_PREFIX,
    RELEASE_DATES,
    RESOLVED_VARIANT,
    SECOND_PHONE_SLUG,
    SERIAL_MALFORMED,
    SERIAL_OWNED_BY_SECOND,
    SERIAL_UNKNOWN_PRODUCT,
    SERIAL_UNREGISTERED,
    SMALL_CAPACITY,
    SUBJECT_PREFIX,
    SUPPORT_CATEGORY,
    UNAVAILABLE_VARIANTS,
    app_origin,
    owner_password,
    settle,
    signup,
    wait_for_message,
)

TIMEOUT = 30.0


def _page(route: str) -> httpx.Response:
    return httpx.get(f"{app_origin()}{route}", timeout=TIMEOUT,
                     follow_redirects=True)


def _raw(route: str) -> httpx.Response:
    return httpx.get(f"{app_origin()}{route}", timeout=TIMEOUT)


def test_families_endpoint_lists_the_four_families(anon_client):
    """The closed family set is served in catalogue order."""
    response = anon_client.get("/families")
    assert response.status_code == 200, (
        f"GET /api/families returned {response.status_code}: {response.text[:400]}"
    )
    slugs = [f.get("slug") for f in items(response.json())]
    assert slugs == list(FAMILIES), (
        f"GET /api/families returned slugs {slugs}, expected the closed set in "
        f"catalogue order {list(FAMILIES)}"
    )


def test_variant_resolution_returns_one_row(anon_client):
    """A colourway with a capacity resolves to exactly one variant."""
    response = anon_client.get(f"/variants/{RESOLVED_VARIANT}")
    assert response.status_code == 200, (
        f"GET /api/variants/{RESOLVED_VARIANT} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    body = response.json()
    assert body.get("colourway") == "Midnight", (
        f"variant {RESOLVED_VARIANT} reports colourway {body.get('colourway')!r}, "
        f"expected 'Midnight'"
    )
    assert body.get("capacity") == LARGE_CAPACITY, (
        f"variant {RESOLVED_VARIANT} reports capacity {body.get('capacity')!r}, "
        f"expected {LARGE_CAPACITY!r}"
    )
    assert body.get("buy_route") == "direct", (
        f"variant {RESOLVED_VARIANT} reports buy_route {body.get('buy_route')!r}, "
        f"expected 'direct'"
    )


def test_impossible_capacity_pair_is_refused(anon_client, db):
    """The seeded hole in the colourway by capacity matrix resolves to nothing."""
    product_slug, colourway, capacity = MISSING_PAIR
    rows = [v for v in db.variants_for(product_slug)
            if v.get("colourway") == colourway and v.get("capacity") == capacity]
    assert rows == [], (
        f"the seeded matrix holds {len(rows)} row(s) for {product_slug} in "
        f"{colourway!r} at {capacity!r}; that pair is the deliberate hole and must "
        f"have none"
    )
    response = anon_client.get(f"/products/{product_slug}/variants",
                               params={"colourway": colourway, "capacity": capacity})
    assert response.status_code in (200, 400, 404, 422), (
        f"GET /api/products/{product_slug}/variants for an impossible pair returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    if response.status_code == 200:
        resolved = items(response.json())
        assert resolved == [], (
            f"an impossible colourway with capacity pair resolved to {len(resolved)} "
            f"variant(s): {str(resolved)[:300]}"
        )


def test_handoff_variant_exposes_outbound_route_not_a_cart_add(anon_client):
    """A handed off variant refuses a cart line and names an outbound destination."""
    handoff_id = HANDOFF_VARIANTS[0]
    response = anon_client.get(f"/variants/{handoff_id}")
    assert response.status_code == 200, (
        f"GET /api/variants/{handoff_id} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    assert response.json().get("buy_route") == "handoff", (
        f"variant {handoff_id} reports buy_route "
        f"{response.json().get('buy_route')!r}, expected 'handoff'"
    )
    added = anon_client.post("/cart/lines",
                             json={"variant_id": handoff_id, "quantity": 1})
    assert added.status_code in (400, 409, 422), (
        f"POST /api/cart/lines for handed off variant {handoff_id} returned "
        f"{added.status_code}, expected a client error refusing it: "
        f"{added.text[:400]}"
    )


def test_direct_variant_add_creates_a_cart_line(anon_client, db):
    """A direct variant is added to the cart at its seeded price."""
    variant_id = "headphone-2--black"
    expected_price = DIRECT_VARIANTS[variant_id]
    before = db.count_cart_lines(variant_id)
    added = anon_client.post("/cart/lines",
                             json={"variant_id": variant_id, "quantity": 1})
    assert added.status_code in (200, 201), (
        f"POST /api/cart/lines for direct variant {variant_id} returned "
        f"{added.status_code}: {added.text[:400]}"
    )
    after = db.count_cart_lines(variant_id)
    assert after == before + 1, (
        f"cart_lines rows for {variant_id} moved from {before} to {after}; a direct "
        f"add must write exactly one line"
    )
    stored = db.variant(variant_id)
    assert stored is not None, f"variant row {variant_id} is missing from the store"
    assert int(stored.get("unit_price_minor")) == expected_price, (
        f"variant {variant_id} stores unit_price_minor "
        f"{stored.get('unit_price_minor')!r}, expected {expected_price}"
    )


def test_listing_shows_one_card_per_variant(anon_client):
    """A family listing returns one entry per variant rather than per product."""
    phones = anon_client.get("/collections/phones")
    assert phones.status_code == 200, (
        f"GET /api/collections/phones returned {phones.status_code}: "
        f"{phones.text[:400]}"
    )
    phone_entries = items(phones.json())
    assert len(phone_entries) == 7, (
        f"the phones listing returned {len(phone_entries)} entries, expected seven, "
        f"one per seeded phone variant"
    )
    audio = anon_client.get("/collections/audio")
    assert audio.status_code == 200, (
        f"GET /api/collections/audio returned {audio.status_code}: "
        f"{audio.text[:400]}"
    )
    audio_entries = items(audio.json())
    assert len(audio_entries) == 4, (
        f"the audio listing returned {len(audio_entries)} entries, expected four, "
        f"one per seeded audio variant"
    )


def test_listing_facets_intersect_across_axes(anon_client):
    """Facets widen within an axis and narrow across axes."""
    one_colour = anon_client.get("/collections/phones", params={"colourway": "Chalk"})
    assert one_colour.status_code == 200, (
        f"GET /api/collections/phones?colourway=Chalk returned "
        f"{one_colour.status_code}: {one_colour.text[:400]}"
    )
    chalk = items(one_colour.json())
    assert len(chalk) == 3, (
        f"the phones listing filtered to Chalk returned {len(chalk)} entries, "
        f"expected three"
    )
    narrowed = anon_client.get("/collections/phones",
                               params={"colourway": "Chalk",
                                       "capacity": LARGE_CAPACITY})
    assert narrowed.status_code == 200, (
        f"GET /api/collections/phones with a colourway and a capacity returned "
        f"{narrowed.status_code}: {narrowed.text[:400]}"
    )
    narrow_entries = items(narrowed.json())
    assert len(narrow_entries) == 1, (
        f"Chalk with {LARGE_CAPACITY!r} returned {len(narrow_entries)} entries, "
        f"expected exactly one"
    )


def test_listing_sort_newest_orders_by_release_date(anon_client):
    """The newest order runs by release date descending."""
    response = anon_client.get("/collections/phones", params={"sort": "Newest"})
    assert response.status_code == 200, (
        f"GET /api/collections/phones?sort=Newest returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    slugs = [e.get("product_slug") for e in items(response.json())]
    assert slugs, "the newest sort returned no entries for the phones family"
    first_dates = [RELEASE_DATES.get(s) for s in slugs if s in RELEASE_DATES]
    assert first_dates == sorted(first_dates, reverse=True), (
        f"the newest sort returned release dates {first_dates}, which is not "
        f"descending; the seeded dates are {RELEASE_DATES}"
    )


def test_empty_family_listing_is_not_a_not_found(anon_client):
    """A family holding no products is an empty listing, never a miss."""
    response = anon_client.get(f"/collections/{EMPTY_FAMILY}")
    assert response.status_code == 200, (
        f"GET /api/collections/{EMPTY_FAMILY} returned {response.status_code}; a "
        f"family with no products is a valid, empty listing: {response.text[:400]}"
    )
    entries = items(response.json())
    assert entries == [], (
        f"the {EMPTY_FAMILY} listing returned {len(entries)} entries; that family is "
        f"seeded with no products"
    )
    page = _page(f"/collections/{EMPTY_FAMILY}")
    assert page.status_code == 200, (
        f"the {EMPTY_FAMILY} family route answered {page.status_code}; the route is "
        f"valid and the catalogue is simply empty"
    )


def test_unknown_family_slug_is_not_found(anon_client):
    """A family slug outside the closed set is a miss."""
    response = _raw("/collections/kettles")
    assert response.status_code == 404, (
        f"an unknown family slug answered {response.status_code}, expected 404"
    )
    api = anon_client.get("/collections/kettles")
    assert api.status_code == 404, (
        f"GET /api/collections/kettles returned {api.status_code}, expected 404: "
        f"{api.text[:400]}"
    )


def test_unknown_address_answers_not_found():
    """An unmatched address answers not found rather than serving a shell."""
    response = _raw("/this-address-matches-no-route")
    assert response.status_code == 404, (
        f"an unmatched address answered {response.status_code}, expected 404. An "
        f"application shell served with a success status is what makes addresses "
        f"that do not exist look real"
    )
    assert "404" in response.text, (
        "the not found surface does not carry the numeral 404 anywhere in its body"
    )


def test_seeded_variant_matrix_is_stored_as_fourteen_rows(db):
    """The seeded catalogue is fourteen variants over six products in four families."""
    assert db.count_families() == len(FAMILIES), (
        f"families holds {db.count_families()} rows, expected {len(FAMILIES)}"
    )
    assert db.count_products() == len(PRODUCT_SLUGS), (
        f"products holds {db.count_products()} rows, expected {len(PRODUCT_SLUGS)}"
    )
    assert db.count_variants() == 14, (
        f"variants holds {db.count_variants()} rows, expected fourteen"
    )


def test_resolved_variant_persisted_row_matches_the_api(anon_client, db):
    """What the resolution serves and what the store holds agree, after a re-read."""
    response = anon_client.get(f"/variants/{RESOLVED_VARIANT}")
    assert response.status_code == 200, (
        f"GET /api/variants/{RESOLVED_VARIANT} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    served = response.json()
    stored = db.variant(RESOLVED_VARIANT)
    assert stored is not None, (
        f"variant row {RESOLVED_VARIANT} is absent from the variants table, so the "
        f"resolution is not being read from a stored row"
    )
    for field in ("colourway", "capacity", "buy_route"):
        assert str(served.get(field)) == str(stored.get(field)), (
            f"variant {RESOLVED_VARIANT} field {field!r} is {served.get(field)!r} over "
            f"HTTP and {stored.get(field)!r} in the store; the two must agree"
        )
    again = anon_client.get(f"/variants/{RESOLVED_VARIANT}")
    assert again.status_code == 200 and again.json().get("buy_route") == \
        served.get("buy_route"), (
        f"a second read of {RESOLVED_VARIANT} returned {again.status_code} and "
        f"buy_route {again.json().get('buy_route')!r}; the resolution must survive a "
        f"reload"
    )


def test_handoff_variant_stores_no_price(anon_client, db):
    """A variant the catalogue does not sell direct carries no price anywhere."""
    for variant_id in HANDOFF_VARIANTS + UNAVAILABLE_VARIANTS:
        stored = db.variant(variant_id)
        assert stored is not None, f"variant row {variant_id} is missing from the store"
        assert stored.get("unit_price_minor") in (None, "", 0), (
            f"variant {variant_id} stores unit_price_minor "
            f"{stored.get('unit_price_minor')!r}; only a direct variant carries a price"
        )
    listing = anon_client.get("/collections/phones")
    assert listing.status_code == 200, (
        f"GET /api/collections/phones returned {listing.status_code}: "
        f"{listing.text[:400]}"
    )
    for entry in items(listing.json()):
        assert entry.get("unit_price_minor") in (None, "", 0), (
            f"a phones listing entry carries unit_price_minor "
            f"{entry.get('unit_price_minor')!r}; a listing card shows no price"
        )


def test_registration_is_persisted_and_survives_a_reread(owner_client, db):
    """A registration lands as a real row the owner can read back."""
    created = owner_client.post("/registrations", json={"serial": SERIAL_UNREGISTERED})
    assert created.status_code in (200, 201, 409), (
        f"POST /api/registrations for {SERIAL_UNREGISTERED} returned "
        f"{created.status_code}: {created.text[:400]}"
    )
    stored = db.registration(SERIAL_UNREGISTERED)
    assert stored is not None, (
        f"no registrations row exists for {SERIAL_UNREGISTERED} after the owner "
        f"registered it; an in-memory list does not satisfy this"
    )
    assert stored.get("product_slug") == HEADPHONE_SLUG, (
        f"registration for {SERIAL_UNREGISTERED} names product "
        f"{stored.get('product_slug')!r}, expected {HEADPHONE_SLUG!r}"
    )
    listed = owner_client.get("/registrations")
    assert listed.status_code == 200, (
        f"GET /api/registrations returned {listed.status_code}: {listed.text[:400]}"
    )
    serials = [r.get("serial") for r in items(listed.json())]
    assert SERIAL_UNREGISTERED in serials, (
        f"the owner's registrations are {serials}; {SERIAL_UNREGISTERED} was just "
        f"registered and must be readable back"
    )


def test_outbound_click_row_is_recorded_without_an_order(anon_client, db):
    """A handoff is recorded as an outbound click and never as a sale."""
    variant_id = HANDOFF_VARIANTS[2]
    before = db.count_outbound_clicks(variant_id)
    recorded = anon_client.post(
        "/outbound-clicks",
        json={"variant_id": variant_id,
              "destination": "https://www.bazaario.example/p/phone-5a"},
    )
    assert recorded.status_code in (200, 201, 202, 204), (
        f"POST /api/outbound-clicks for {variant_id} returned "
        f"{recorded.status_code}: {recorded.text[:400]}"
    )
    after = db.count_outbound_clicks(variant_id)
    assert after == before + 1, (
        f"outbound_clicks rows for {variant_id} moved from {before} to {after}; a "
        f"followed handoff writes exactly one row"
    )
    assert db.count_cart_lines(variant_id) == 0, (
        f"a handed off variant {variant_id} has {db.count_cart_lines(variant_id)} "
        f"cart line(s); a handoff is a click, never an order"
    )


def test_cart_line_persists_across_a_fresh_session(db):
    """A cart line written by one client is still there for the next read."""
    variant_id = "arc-watch-2--grey"
    with client() as first:
        added = first.post("/cart/lines", json={"variant_id": variant_id, "quantity": 1})
        assert added.status_code in (200, 201), (
            f"POST /api/cart/lines for {variant_id} returned {added.status_code}: "
            f"{added.text[:400]}"
        )
        cookies = dict(first.cookies)
    stored = db.count_cart_lines(variant_id)
    assert stored >= 1, (
        f"cart_lines holds {stored} row(s) for {variant_id} after an add; the cart "
        f"lives on the server, not in the page"
    )
    with client() as second:
        second.cookies.update(cookies)
        read_back = second.get("/cart")
        assert read_back.status_code == 200, (
            f"GET /api/cart returned {read_back.status_code}: {read_back.text[:400]}"
        )
        flat = str(read_back.json())
        assert variant_id in flat, (
            f"the cart read back on a fresh client does not carry {variant_id}; the "
            f"cart must survive a reload"
        )


def test_anonymous_registration_request_is_denied(anon_client, db):
    """An anonymous caller cannot register a device, and nothing is written."""
    before = db.count_registrations(SERIAL_UNKNOWN_PRODUCT)
    response = anon_client.post("/registrations",
                                json={"serial": SERIAL_UNKNOWN_PRODUCT})
    assert response.status_code in (401, 403), (
        f"POST /api/registrations without a token returned {response.status_code}, "
        f"expected 401 or 403: {response.text[:400]}"
    )
    after = db.count_registrations(SERIAL_UNKNOWN_PRODUCT)
    assert after == before, (
        f"registrations rows for {SERIAL_UNKNOWN_PRODUCT} moved from {before} to "
        f"{after} on a denied call; a denial leaves the store unchanged"
    )
    listed = anon_client.get("/registrations")
    assert listed.status_code in (401, 403), (
        f"GET /api/registrations without a token returned {listed.status_code}, "
        f"expected 401 or 403: {listed.text[:400]}"
    )


def test_cross_account_support_request_is_denied(owner_client, second_owner_client, db):
    """A request naming another account's registration is refused on the server."""
    owned = owner_client.get("/registrations")
    assert owned.status_code == 200, (
        f"GET /api/registrations returned {owned.status_code}: {owned.text[:400]}"
    )
    rows = items(owned.json())
    assert rows, "the first owner holds no registration to attack from the other side"
    target = rows[0].get("id")
    before = db.count_support_requests()
    response = second_owner_client.post(
        "/support-requests",
        json={"registration_id": target, "category": SUPPORT_CATEGORY,
              "body": "Opened against a registration this account does not hold.",
              "idempotency_key": "cross-account-probe"},
    )
    assert response.status_code in (401, 403, 404), (
        f"POST /api/support-requests naming another account's registration "
        f"{target!r} returned {response.status_code}, expected a refusal: "
        f"{response.text[:400]}"
    )
    after = db.count_support_requests()
    assert after == before, (
        f"support_requests moved from {before} to {after} rows on a refused "
        f"cross-account request; nothing may be written"
    )


def test_registrations_listing_is_scoped_to_the_signed_in_owner(
        owner_client, second_owner_client):
    """Each owner reads only their own registrations."""
    first = owner_client.get("/registrations")
    second = second_owner_client.get("/registrations")
    assert first.status_code == 200 and second.status_code == 200, (
        f"GET /api/registrations returned {first.status_code} for the first owner "
        f"and {second.status_code} for the second"
    )
    first_serials = {r.get("serial") for r in items(first.json())}
    second_serials = {r.get("serial") for r in items(second.json())}
    assert SERIAL_OWNED_BY_SECOND not in first_serials, (
        f"the first owner reads {SERIAL_OWNED_BY_SECOND}, which belongs to the "
        f"second owner; the listing is scoped to the session"
    )
    assert SERIAL_OWNED_BY_SECOND in second_serials, (
        f"the second owner's registrations are {second_serials}; the seeded serial "
        f"{SERIAL_OWNED_BY_SECOND} must be among them"
    )


def test_support_requests_listing_is_scoped_to_the_signed_in_owner(
        owner_client, second_owner_client):
    """Each owner reads only their own support requests."""
    first = owner_client.get("/support-requests")
    second = second_owner_client.get("/support-requests")
    assert first.status_code == 200 and second.status_code == 200, (
        f"GET /api/support-requests returned {first.status_code} for the first owner "
        f"and {second.status_code} for the second"
    )
    first_ids = {r.get("id") for r in items(first.json())}
    second_ids = {r.get("id") for r in items(second.json())}
    assert first_ids.isdisjoint(second_ids), (
        f"the two owners share request ids {sorted(first_ids & second_ids)}; each "
        f"owner reads only their own"
    )


def test_duplicate_serial_across_accounts_is_refused_without_naming_the_holder(
        owner_client, db):
    """A serial held by another account is refused, and the refusal names nobody."""
    before = db.count_registrations(SERIAL_OWNED_BY_SECOND)
    assert before == 1, (
        f"registrations holds {before} row(s) for {SERIAL_OWNED_BY_SECOND}; exactly "
        f"one is seeded, against the second owner"
    )
    response = owner_client.post("/registrations",
                                 json={"serial": SERIAL_OWNED_BY_SECOND})
    assert response.status_code in (400, 403, 409, 422), (
        f"POST /api/registrations for a serial held by another account returned "
        f"{response.status_code}, expected a refusal: {response.text[:400]}"
    )
    assert OWNER2_EMAIL not in response.text, (
        f"the refusal for {SERIAL_OWNED_BY_SECOND} names {OWNER2_EMAIL}; a refusal "
        f"that identifies the holder turns the form into a lookup"
    )
    after = db.count_registrations(SERIAL_OWNED_BY_SECOND)
    assert after == before, (
        f"registrations rows for {SERIAL_OWNED_BY_SECOND} moved from {before} to "
        f"{after}; a serial belongs to at most one account"
    )


def test_malformed_serial_is_refused_and_writes_nothing(owner_client, db):
    """A serial that does not match the shape is refused and writes nothing."""
    before = db.count_registrations(SERIAL_MALFORMED)
    response = owner_client.post("/registrations", json={"serial": SERIAL_MALFORMED})
    assert response.status_code in (400, 422), (
        f"POST /api/registrations for malformed serial {SERIAL_MALFORMED} returned "
        f"{response.status_code}, expected a client error: {response.text[:400]}"
    )
    after = db.count_registrations(SERIAL_MALFORMED)
    assert after == before == 0, (
        f"registrations rows for {SERIAL_MALFORMED} went from {before} to {after}; a "
        f"refused serial writes nothing"
    )


def test_unknown_serial_is_refused_and_writes_nothing(owner_client, db):
    """A well formed serial naming no product is refused and writes nothing."""
    before = db.count_registrations(SERIAL_UNKNOWN_PRODUCT)
    response = owner_client.post("/registrations",
                                 json={"serial": SERIAL_UNKNOWN_PRODUCT})
    assert response.status_code in (400, 404, 422), (
        f"POST /api/registrations for {SERIAL_UNKNOWN_PRODUCT}, a well formed serial "
        f"naming no product, returned {response.status_code}: {response.text[:400]}"
    )
    after = db.count_registrations(SERIAL_UNKNOWN_PRODUCT)
    assert after == before == 0, (
        f"registrations rows for {SERIAL_UNKNOWN_PRODUCT} went from {before} to "
        f"{after}; a refused serial writes nothing"
    )


def test_support_request_with_an_empty_body_is_refused(owner_client, db):
    """An empty body or an unknown category is refused and writes nothing."""
    registrations = items(owner_client.get("/registrations").json())
    assert registrations, "the first owner holds no registration to file against"
    target = registrations[0].get("id")
    before = db.count_support_requests()
    empty = owner_client.post(
        "/support-requests",
        json={"registration_id": target, "category": SUPPORT_CATEGORY, "body": "",
              "idempotency_key": "empty-body-probe"},
    )
    assert empty.status_code in (400, 422), (
        f"POST /api/support-requests with an empty body returned "
        f"{empty.status_code}, expected a client error: {empty.text[:400]}"
    )
    bad_category = owner_client.post(
        "/support-requests",
        json={"registration_id": target, "category": "Weather",
              "body": "A category outside the closed set.",
              "idempotency_key": "bad-category-probe"},
    )
    assert bad_category.status_code in (400, 422), (
        f"POST /api/support-requests with category 'Weather' returned "
        f"{bad_category.status_code}, expected a client error: "
        f"{bad_category.text[:400]}"
    )
    after = db.count_support_requests()
    assert after == before, (
        f"support_requests moved from {before} to {after} rows on two refused "
        f"submissions; a refusal writes nothing"
    )


def test_article_vote_updates_rather_than_inserts(anon_client, db, probe_token):
    """A second vote from one visitor updates the stored answer."""
    article = "battery-drains-overnight"
    anonymous_id = f"probe-{probe_token}"
    first = anon_client.post(f"/articles/{article}/vote",
                             json={"helpful": True, "anonymous_id": anonymous_id})
    assert first.status_code in (200, 201), (
        f"POST /api/articles/{article}/vote returned {first.status_code}: "
        f"{first.text[:400]}"
    )
    second = anon_client.post(f"/articles/{article}/vote",
                              json={"helpful": False, "anonymous_id": anonymous_id})
    assert second.status_code in (200, 201), (
        f"a second vote for {article} returned {second.status_code}: "
        f"{second.text[:400]}"
    )
    rows = db.count_article_votes(article, anonymous_id)
    assert rows == 1, (
        f"article_votes holds {rows} rows for {article} and {anonymous_id}; a second "
        f"answer updates the stored one rather than adding another"
    )
    stored = db.article_vote(article, anonymous_id)
    assert stored is not None and str(stored.get("helpful")).lower() in ("false", "0"), (
        f"the stored vote for {article} reads {stored!r}; the second answer was no "
        f"and must have replaced the first"
    )


def test_login_failure_wording_does_not_distinguish_the_two_causes(anon_client, db,
                                                                    probe_token):
    """An unknown address and a wrong password answer with the same wording."""
    wrong_password = anon_client.post(
        "/auth/login", json={"email": OWNER_EMAIL, "password": "not-the-password"})
    unknown_address = anon_client.post(
        "/auth/login",
        json={"email": f"absent-{probe_token}@example.com",
              "password": owner_password()})
    assert wrong_password.status_code in (400, 401), (
        f"login with a wrong password returned {wrong_password.status_code}: "
        f"{wrong_password.text[:400]}"
    )
    assert unknown_address.status_code in (400, 401), (
        f"login with an unknown address returned {unknown_address.status_code}: "
        f"{unknown_address.text[:400]}"
    )
    assert LOGIN_FAILURE_WORDING in wrong_password.text, (
        f"the wrong-password refusal reads {wrong_password.text[:200]!r}; the pinned "
        f"wording is {LOGIN_FAILURE_WORDING!r}"
    )
    assert LOGIN_FAILURE_WORDING in unknown_address.text, (
        f"the unknown-address refusal reads {unknown_address.text[:200]!r}; the "
        f"pinned wording is {LOGIN_FAILURE_WORDING!r}"
    )
    stored = db.account(OWNER_EMAIL)
    assert stored is not None, f"no accounts row exists for {OWNER_EMAIL}"
    assert owner_password() not in str(stored), (
        f"the accounts row for {OWNER_EMAIL} carries the password in clear; it must "
        f"be stored hashed"
    )


def test_support_request_delivers_one_confirmation_email(owner_client, inbox, db,
                                                         probe_token):
    """A filed request delivers one real acknowledgement to the owner's address."""
    registrations = items(owner_client.get("/registrations").json())
    assert registrations, "the first owner holds no registration to file against"
    target = registrations[0].get("id")
    key = f"ack-{probe_token}"
    before = inbox.count(to=OWNER_EMAIL)
    response = owner_client.post(
        "/support-requests",
        json={"registration_id": target, "category": SUPPORT_CATEGORY,
              "body": "The device stops charging overnight.",
              "idempotency_key": key},
    )
    assert response.status_code in (200, 201), (
        f"POST /api/support-requests returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    reference = response.json().get("reference")
    assert isinstance(reference, str) and reference.startswith(REFERENCE_PREFIX), (
        f"the request returned reference {reference!r}; a reference begins "
        f"{REFERENCE_PREFIX!r} followed by eight digits"
    )
    assert db.support_request(reference) is not None, (
        f"no support_requests row carries reference {reference!r}; the request must "
        f"be a real stored row"
    )
    message = wait_for_message(inbox, to=OWNER_EMAIL,
                               subject_contains=f"{SUBJECT_PREFIX}{reference}")
    assert message is not None, (
        f"no message with subject beginning {SUBJECT_PREFIX + reference!r} arrived "
        f"for {OWNER_EMAIL}. The inbox held {before} message(s) for that address "
        f"before the request and holds {inbox.count(to=OWNER_EMAIL)} now; a real "
        f"SMTP send must have happened"
    )


def test_duplicate_support_request_sends_no_second_confirmation_email(
        owner_client, inbox, db, probe_token):
    """A replayed submission returns the first reference and sends nothing more."""
    registrations = items(owner_client.get("/registrations").json())
    assert registrations, "the first owner holds no registration to file against"
    target = registrations[0].get("id")
    key = f"replay-{probe_token}"
    payload = {"registration_id": target, "category": SUPPORT_CATEGORY,
               "body": "Filed twice on purpose.", "idempotency_key": key}
    first = owner_client.post("/support-requests", json=payload)
    assert first.status_code in (200, 201), (
        f"the first submission returned {first.status_code}: {first.text[:400]}"
    )
    reference = first.json().get("reference")
    assert wait_for_message(inbox, to=OWNER_EMAIL,
                            subject_contains=f"{SUBJECT_PREFIX}{reference}") is not None, (
        f"the first submission sent no acknowledgement carrying "
        f"{SUBJECT_PREFIX + str(reference)!r}"
    )
    count_after_first = inbox.count(to=OWNER_EMAIL)
    second = owner_client.post("/support-requests", json=payload)
    assert second.status_code in (200, 201, 409), (
        f"the replayed submission returned {second.status_code}: {second.text[:400]}"
    )
    assert second.json().get("reference") == reference, (
        f"the replay returned reference {second.json().get('reference')!r}, expected "
        f"the original {reference!r}"
    )
    assert db.count_requests_for_key(key) == 1, (
        f"support_requests holds {db.count_requests_for_key(key)} rows for "
        f"idempotency key {key!r}; a replay writes no second row"
    )
    settle()
    assert inbox.count(to=OWNER_EMAIL) == count_after_first, (
        f"the inbox for {OWNER_EMAIL} moved from {count_after_first} to "
        f"{inbox.count(to=OWNER_EMAIL)} messages after a replay; the acknowledgement "
        f"is sent once"
    )


def test_device_registration_sends_no_mail(inbox, probe_token):
    """Registering a device, and a refused request, both send nothing."""
    email = f"probe-{probe_token}@example.com"
    token = signup(email, "probe-pw-2026")
    with client(token) as fresh:
        before = inbox.count(to=email)
        refused = fresh.post("/registrations", json={"serial": SERIAL_MALFORMED})
        assert refused.status_code in (400, 422), (
            f"POST /api/registrations for a malformed serial returned "
            f"{refused.status_code}: {refused.text[:400]}"
        )
    settle()
    after = inbox.count(to=email)
    assert after == before == 0, (
        f"the inbox for the fresh account {email} moved from {before} to {after}; "
        f"registering a device and refusing one both send no mail"
    )


def test_health_endpoint_answers_ready(anon_client):
    """The health route answers ready and the API lives under the api prefix."""
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:400]}"
    )
    families = anon_client.get("/families")
    assert families.status_code == 200, (
        f"GET /api/families returned {families.status_code}; the HTTP API is served "
        f"on the app origin under the api prefix"
    )
    payload = families.json()
    assert isinstance(payload, list), (
        f"GET /api/families returned {type(payload).__name__}; a list endpoint "
        f"returns a top-level JSON array"
    )


def test_sitemap_and_robots_are_served():
    """The sitemap lists every public route and the robots file names it."""
    sitemap = _raw("/sitemap.xml")
    assert sitemap.status_code == 200, (
        f"GET /sitemap.xml returned {sitemap.status_code}: {sitemap.text[:200]}"
    )
    body = sitemap.text
    missing = [r for r in PUBLIC_ROUTES if r != "/" and r not in body]
    assert not missing, (
        f"the sitemap omits {len(missing)} public route(s): {missing[:6]}"
    )
    robots = _raw("/robots.txt")
    assert robots.status_code == 200, (
        f"GET /robots.txt returned {robots.status_code}: {robots.text[:200]}"
    )
    assert "sitemap" in robots.text.lower(), (
        f"the robots file does not name the sitemap: {robots.text[:200]!r}"
    )


def test_favicon_is_served_and_declared():
    """A favicon is served and declared in the document head."""
    icon = _raw("/favicon.ico")
    assert icon.status_code == 200, (
        f"GET /favicon.ico returned {icon.status_code}; the site serves its own icon"
    )
    home = _page("/")
    assert home.status_code == 200, (
        f"the home route answered {home.status_code}: {home.text[:200]}"
    )
    assert "icon" in home.text.lower(), (
        "the home document head declares no icon link"
    )


def test_public_routes_carry_distinct_titles_and_descriptions():
    """No two public routes share a title or a description."""
    import re as _re
    titles, descriptions = {}, {}
    for route in PUBLIC_ROUTES:
        page = _page(route)
        assert page.status_code == 200, (
            f"the public route {route} answered {page.status_code}: {page.text[:200]}"
        )
        title = _re.search(r"<title[^>]*>(.*?)</title>", page.text,
                           _re.S | _re.I)
        assert title is not None, f"the route {route} carries no title element"
        description = _re.search(
            r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
            page.text, _re.S | _re.I)
        assert description is not None, (
            f"the route {route} declares no description"
        )
        titles.setdefault(title.group(1).strip(), []).append(route)
        descriptions.setdefault(description.group(1).strip(), []).append(route)
    shared_titles = {t: r for t, r in titles.items() if len(r) > 1}
    assert not shared_titles, (
        f"these titles are shared by more than one public route: {shared_titles}"
    )
    shared_descriptions = {d: r for d, r in descriptions.items() if len(r) > 1}
    assert not shared_descriptions, (
        f"these descriptions are shared by more than one public route: "
        f"{shared_descriptions}"
    )


def test_social_preview_is_declared_on_every_public_route():
    """Every public route declares a social preview title and a resolving image."""
    import re as _re
    for route in PUBLIC_ROUTES:
        page = _page(route)
        assert page.status_code == 200, (
            f"the public route {route} answered {page.status_code}"
        )
        title = _re.search(
            r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']',
            page.text, _re.S | _re.I)
        assert title is not None, (
            f"the route {route} declares no social preview title"
        )
        image = _re.search(
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']',
            page.text, _re.S | _re.I)
        assert image is not None, (
            f"the route {route} declares no social preview image"
        )
        target = image.group(1).strip()
        if target.startswith("/"):
            target = f"{app_origin()}{target}"
        resolved = httpx.get(target, timeout=TIMEOUT, follow_redirects=True)
        assert resolved.status_code == 200, (
            f"the social preview image for {route} at {target} answered "
            f"{resolved.status_code}"
        )


def test_no_credential_appears_in_what_the_browser_downloads():
    """Nothing the browser downloads carries a credential or a store address."""
    import re as _re
    for route in ("/", "/products/phone-5a-pro", "/cart", "/account"):
        page = _page(route)
        assert page.status_code == 200, (
            f"the route {route} answered {page.status_code}"
        )
        for marker in CREDENTIAL_MARKERS:
            assert marker not in page.text, (
                f"the document served at {route} carries {marker!r}; nothing the "
                f"browser downloads may carry a credential or a store address"
            )
        for src in _re.findall(r'<script[^>]+src=["\'](.*?)["\']', page.text, _re.I):
            target = f"{app_origin()}{src}" if src.startswith("/") else src
            if not target.startswith(app_origin()):
                continue
            asset = httpx.get(target, timeout=TIMEOUT, follow_redirects=True)
            assert asset.status_code == 200, (
                f"the script {src} referenced by {route} answered "
                f"{asset.status_code}"
            )
            for marker in CREDENTIAL_MARKERS:
                assert marker not in asset.text, (
                    f"the script {src} downloaded by {route} carries {marker!r}"
                )
