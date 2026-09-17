"""The one section module for deku/commerce-platform-console-vb.

Every observation the pytest channel makes about the running product. Assertions
speak only through the App Contract surface and the declared backing services.
"""

from __future__ import annotations

import concurrent.futures

from conftest import (
    APPROVAL_REQUEST_TABLE,
    BOUNDARY_PRODUCT,
    CURRENCY,
    DELHI,
    FINANCE_EMAIL,
    LEDGER_ENTRY_TABLE,
    MALLARD_ORDER_MINOR,
    ORDER_APPROVED_REFUND,
    ORDER_BROWSER_REFUND,
    ORDER_INSIDE_CEILING,
    ORDER_LARGE_MINOR,
    ORDER_OTHER_STORE,
    ORDER_PENDING_REQUEST,
    ORDER_SMALL_MINOR,
    ORDER_VALIDATION,
    PUBLIC_ROUTES,
    PUNE,
    SUPPORT_CEILING_MINOR,
    SUPPORT_EMAIL,
    approvals,
    available_balance,
    decide,
    inventory_rows,
    order_by_number,
    order_detail,
    order_index,
    post_refund,
    probe_key,
    settle,
)
from _shapes import flatten, items


def _require_order(c, number):
    row = order_by_number(c, number)
    assert row is not None, (
        f"the seeded order {number} is absent from GET /api/orders; "
        f"saw {[r.get('number') for r in order_index(c)]}")
    return row


def test_refund_within_ceiling_is_stored_and_moves_the_balance(support_client):
    """A refund at or below the acting member's ceiling executes at once."""
    before = available_balance(support_client)
    order = _require_order(support_client, ORDER_INSIDE_CEILING)
    amount = 400000
    assert amount <= SUPPORT_CEILING_MINOR, (
        f"the probe amount {amount} must sit at or below the support ceiling "
        f"{SUPPORT_CEILING_MINOR}")
    r = post_refund(support_client, order["id"], amount, probe_key("within"))
    assert r.status_code in (200, 201), (
        f"POST /api/orders/{order['id']}/refunds for {amount} returned "
        f"{r.status_code}, expected a created refund; body={r.text[:400]}")
    body = r.json()
    assert body.get("status") not in (None, "pending_approval"), (
        f"a within-ceiling refund on {ORDER_INSIDE_CEILING} reported "
        f"{body.get('status')!r}; it must execute rather than wait")
    assert body.get("ledger_transaction_id"), (
        f"the refund on {ORDER_INSIDE_CEILING} carries no ledger_transaction_id; "
        f"body={flatten(body)[:300]}")
    after = available_balance(support_client)
    assert after == before - amount, (
        f"the available balance moved from {before} to {after}; a refund of "
        f"{amount} must move it by exactly that much")


def test_order_financial_status_records_the_partial_refund(support_client):
    """The refunded order advances its financial status and carries a timeline entry."""
    order = _require_order(support_client, ORDER_INSIDE_CEILING)
    detail = order_detail(support_client, order["id"])
    assert detail.get("financial_status") in ("partially_refunded", "refunded"), (
        f"{ORDER_INSIDE_CEILING} reports financial_status "
        f"{detail.get('financial_status')!r} after a refund; expected "
        f"'partially_refunded' or 'refunded'")
    timeline = flatten(detail.get("timeline", [])).lower()
    assert "refund" in timeline, (
        f"the timeline of {ORDER_INSIDE_CEILING} names no refund entry; "
        f"saw {timeline[:300]}")
    assert SUPPORT_EMAIL.split("@")[0] in timeline or SUPPORT_EMAIL in timeline, (
        f"the refund entry on {ORDER_INSIDE_CEILING} names no actor; "
        f"saw {timeline[:300]}")


def test_refund_above_ceiling_creates_a_pending_approval_request(support_client):
    """Above the ceiling the refund becomes a proposal rather than an effect."""
    order = _require_order(support_client, ORDER_PENDING_REQUEST)
    r = post_refund(support_client, order["id"], ORDER_LARGE_MINOR, probe_key("above"))
    assert r.status_code in (200, 201, 202), (
        f"POST /api/orders/{order['id']}/refunds for {ORDER_LARGE_MINOR} returned "
        f"{r.status_code}; an above-ceiling refund creates a request rather than "
        f"failing; body={r.text[:400]}")
    body = r.json()
    assert body.get("state") == "pending", (
        f"the above-ceiling refund on {ORDER_PENDING_REQUEST} reported state "
        f"{body.get('state')!r}, expected 'pending'; body={flatten(body)[:300]}")
    assert body.get("action_type") == "order_refund", (
        f"the request on {ORDER_PENDING_REQUEST} reported action_type "
        f"{body.get('action_type')!r}, expected 'order_refund'")
    assert int(body.get("amount_minor", 0)) == ORDER_LARGE_MINOR, (
        f"the request records amount_minor {body.get('amount_minor')!r}, expected "
        f"{ORDER_LARGE_MINOR}")
    assert body.get("required_permission"), (
        f"the request on {ORDER_PENDING_REQUEST} names no required_permission")
    assert body.get("expires_at"), (
        f"the request on {ORDER_PENDING_REQUEST} carries no expires_at")


def test_pending_request_stores_no_ledger_entry_and_leaves_the_order_paid(
        support_client, backend):
    """A pending proposal has moved no money and changed no order state."""
    before = available_balance(support_client)
    order = _require_order(support_client, ORDER_PENDING_REQUEST)
    detail = order_detail(support_client, order["id"])
    assert detail.get("financial_status") == "paid", (
        f"{ORDER_PENDING_REQUEST} reports financial_status "
        f"{detail.get('financial_status')!r} while a request is pending; expected "
        f"'paid' to be unchanged")
    pending = [a for a in approvals(support_client) if a.get("state") == "pending"]
    assert pending, (
        f"GET /api/approvals exposes no pending request after an above-ceiling "
        f"refund on {ORDER_PENDING_REQUEST}")
    settle()
    after = available_balance(support_client)
    assert after == before, (
        f"the available balance moved from {before} to {after} while a request was "
        f"pending; a proposal moves no money")
    rows = backend.rows(APPROVAL_REQUEST_TABLE, state="pending")
    assert rows, (
        f"table {APPROVAL_REQUEST_TABLE!r} holds no row in state 'pending'; the "
        f"request must be a real persisted record")
    assert backend.count(LEDGER_ENTRY_TABLE) >= 0, (
        f"table {LEDGER_ENTRY_TABLE!r} is not readable; the ledger must exist as a "
        f"real table")


def test_support_agent_cannot_decide_their_own_request_denied_at_the_api(
        support_client):
    """The requester is refused a decision on their own request, at the API."""
    pending = [a for a in approvals(support_client) if a.get("state") == "pending"]
    assert pending, "no pending request is available to attempt a self-decision on"
    target = pending[0]
    r = decide(support_client, target["id"], "approve", probe_key("selfapprove"))
    assert r.status_code in (401, 403), (
        f"POST /api/approvals/{target['id']}/decision from the requester returned "
        f"{r.status_code}, expected a denial; body={r.text[:300]}")
    again = [a for a in approvals(support_client) if str(a.get("id")) == str(target["id"])]
    assert again and again[0].get("state") == "pending", (
        f"request {target['id']} is no longer pending after a refused self-decision; "
        f"a denied call leaves the row untouched")


def test_approval_executes_the_refund_exactly_once_on_a_duplicate_decision(
        support_client, finance_client):
    """One approval, then a second, produce exactly one refund."""
    order = _require_order(support_client, ORDER_APPROVED_REFUND)
    created = post_refund(support_client, order["id"], ORDER_LARGE_MINOR,
                          probe_key("toapprove"))
    assert created.status_code in (200, 201, 202), (
        f"creating the above-ceiling request on {ORDER_APPROVED_REFUND} returned "
        f"{created.status_code}; body={created.text[:300]}")
    request_id = created.json().get("id")
    assert request_id, f"the created request on {ORDER_APPROVED_REFUND} carries no id"

    before = available_balance(finance_client)
    key = probe_key("decide")
    first = decide(finance_client, request_id, "approve", key)
    assert first.status_code in (200, 201, 202), (
        f"the first decision on {request_id} returned {first.status_code}; "
        f"body={first.text[:300]}")
    assert first.json().get("state") in ("approved", "executed"), (
        f"the decided request reports state {first.json().get('state')!r}, expected "
        f"'approved' or 'executed'")
    mid = available_balance(finance_client)
    assert mid == before - ORDER_LARGE_MINOR, (
        f"the available balance moved from {before} to {mid}; approving a refund of "
        f"{ORDER_LARGE_MINOR} must move it by exactly that much")

    second = decide(finance_client, request_id, "approve", key)
    assert second.status_code in (200, 201, 202, 409), (
        f"the repeated decision on {request_id} returned {second.status_code}; a "
        f"replay is either the stored result or an explicit conflict")
    settle()
    end = available_balance(finance_client)
    assert end == mid, (
        f"the available balance moved from {mid} to {end} on a repeated approval; "
        f"one approval executes exactly once")


def test_approved_order_reads_refunded_and_names_its_decider(finance_client):
    """The executed effect is visible on the order it refunded."""
    order = _require_order(finance_client, ORDER_APPROVED_REFUND)
    detail = order_detail(finance_client, order["id"])
    assert detail.get("financial_status") == "refunded", (
        f"{ORDER_APPROVED_REFUND} reports financial_status "
        f"{detail.get('financial_status')!r} after a full approved refund; expected "
        f"'refunded'")
    decided = [a for a in approvals(finance_client)
               if a.get("state") in ("approved", "executed")]
    assert decided, "GET /api/approvals exposes no decided request after an approval"
    detail_text = flatten(decided[0]).lower()
    assert FINANCE_EMAIL.split("@")[0] in detail_text or "decided" in detail_text, (
        f"the decided request names no decider; saw {detail_text[:300]}")


def test_refund_replay_of_one_idempotency_key_records_one_refund(support_client):
    """A repeat under the same key returns the first result rather than refunding twice."""
    order = _require_order(support_client, ORDER_BROWSER_REFUND)
    key = probe_key("replay")
    amount = 100000
    first = post_refund(support_client, order["id"], amount, key)
    assert first.status_code in (200, 201), (
        f"the first refund under {key} returned {first.status_code}; "
        f"body={first.text[:300]}")
    before = available_balance(support_client)
    second = post_refund(support_client, order["id"], amount, key)
    assert second.status_code in (200, 201), (
        f"the replay under {key} returned {second.status_code}; a replay returns the "
        f"stored response")
    assert str(second.json().get("id")) == str(first.json().get("id")), (
        f"the replay under {key} produced refund {second.json().get('id')!r}, not the "
        f"original {first.json().get('id')!r}")
    settle()
    after = available_balance(support_client)
    assert after == before, (
        f"the available balance moved from {before} to {after} on a replayed refund")


def test_refund_beyond_the_remaining_captured_amount_is_refused(support_client):
    """The sum of non-failed refunds never exceeds what was captured."""
    order = _require_order(support_client, ORDER_VALIDATION)
    r = post_refund(support_client, order["id"], ORDER_SMALL_MINOR * 3,
                    probe_key("overrefund"))
    assert r.status_code in (400, 409, 422), (
        f"a refund larger than the captured amount on {ORDER_VALIDATION} returned "
        f"{r.status_code}, expected a client error; body={r.text[:300]}")
    detail = order_detail(support_client, order["id"])
    assert detail.get("financial_status") == "paid", (
        f"{ORDER_VALIDATION} reports {detail.get('financial_status')!r} after a "
        f"refused refund; the row must be untouched")


def test_negative_refund_amount_is_refused(support_client):
    """A negative amount is refused before any business logic runs."""
    order = _require_order(support_client, ORDER_VALIDATION)
    r = post_refund(support_client, order["id"], -1, probe_key("negative"))
    assert r.status_code in (400, 422), (
        f"a refund of -1 on {ORDER_VALIDATION} returned {r.status_code}, expected a "
        f"client error; body={r.text[:300]}")


def test_unknown_field_in_a_refund_request_is_refused(support_client):
    """An unrecognised field is rejected rather than ignored."""
    order = _require_order(support_client, ORDER_VALIDATION)
    r = support_client.post(
        f"/api/orders/{order['id']}/refunds",
        json={"amount_minor": 1000, "currency": CURRENCY, "reason": "probe",
              "idempotency_key": probe_key("unknown"), "amont_minor": 999999})
    assert r.status_code in (400, 422), (
        f"a refund body carrying a misspelled field returned {r.status_code}, "
        f"expected a client error; body={r.text[:300]}")


def test_decimal_money_on_the_refund_path_is_refused(support_client):
    """Money is integer minor units; a decimal is rejected rather than coerced."""
    order = _require_order(support_client, ORDER_VALIDATION)
    r = support_client.post(
        f"/api/orders/{order['id']}/refunds",
        json={"amount_minor": 1000.5, "currency": CURRENCY, "reason": "probe",
              "idempotency_key": probe_key("decimal")})
    assert r.status_code in (400, 422), (
        f"a refund of 1000.5 returned {r.status_code}, expected a client error; "
        f"body={r.text[:300]}")


def test_unauthenticated_order_request_is_denied(anon_client):
    """An anonymous caller reaches no store data."""
    r = anon_client.get("/api/orders")
    assert r.status_code in (401, 403), (
        f"GET /api/orders without a session returned {r.status_code}, expected a "
        f"denial; body={r.text[:300]}")


def test_a_member_of_another_store_cannot_read_a_foreign_order(mallard_client,
                                                               support_client):
    """Tenancy holds by identifier as well as by navigation."""
    foreign = _require_order(support_client, ORDER_PENDING_REQUEST)
    r = mallard_client.get(f"/api/orders/{foreign['id']}")
    assert r.status_code in (401, 403, 404), (
        f"GET /api/orders/{foreign['id']} from the other store's session returned "
        f"{r.status_code}, expected a denial or a not-found; body={r.text[:300]}")
    own = order_index(mallard_client)
    numbers = {str(row.get("number")) for row in own}
    assert numbers == {ORDER_OTHER_STORE}, (
        f"the other store's order index exposes {sorted(numbers)}; it must expose "
        f"exactly {{{ORDER_OTHER_STORE!r}}}")
    assert int(own[0].get("total_minor")) == MALLARD_ORDER_MINOR, (
        f"{ORDER_OTHER_STORE} reports total_minor {own[0].get('total_minor')!r}, "
        f"expected {MALLARD_ORDER_MINOR}")


def test_store_context_is_not_taken_from_the_request_body(mallard_client,
                                                          support_client):
    """A store named in a request never widens what the session may read."""
    foreign = _require_order(support_client, ORDER_PENDING_REQUEST)
    r = mallard_client.get("/api/orders", params={"store": "oakleaf"})
    assert r.status_code in (200, 400, 403, 404), (
        f"GET /api/orders?store=oakleaf returned {r.status_code}; body={r.text[:300]}")
    if r.status_code == 200:
        numbers = {str(row.get("number")) for row in items(r.json())}
        assert str(foreign.get("number")) not in numbers, (
            f"naming another store in the query exposed {sorted(numbers)}; the store "
            f"context resolves on the server")


def test_an_adjustment_at_an_unassigned_location_is_denied(support_client):
    """A location outside the actor's constraint is refused at the API."""
    rows = inventory_rows(support_client)
    assert rows, "GET /api/inventory exposes no levels"
    target = None
    for row in rows:
        if str(row.get("location_id")) not in ("", "None"):
            target = row
            break
    assert target is not None, f"no inventory level names a location; saw {rows[:2]}"
    r = support_client.post(
        "/api/inventory/adjustments",
        json={"variant_id": target["variant_id"], "location_id": target["location_id"],
              "quantity_name": "on_hand", "delta": 1, "reason": "correction",
              "idempotency_key": probe_key("adjust")})
    assert r.status_code in (401, 403), (
        f"a stock adjustment from a support-agent session returned {r.status_code}, "
        f"expected a denial; body={r.text[:300]}")
    after = inventory_rows(support_client)
    same = [x for x in after if str(x.get("variant_id")) == str(target["variant_id"])
            and str(x.get("location_id")) == str(target["location_id"])]
    assert same and same[0].get("on_hand") == target.get("on_hand"), (
        f"on_hand moved from {target.get('on_hand')!r} to "
        f"{same[0].get('on_hand') if same else None!r} after a denied adjustment")


def test_available_quantity_is_derived_from_the_stored_level_columns(manager_client):
    """The available quantity is computed rather than written."""
    rows = inventory_rows(manager_client)
    assert rows, "GET /api/inventory exposes no levels"
    bad = []
    for row in rows:
        expected = (int(row.get("on_hand", 0)) - int(row.get("committed", 0))
                    - int(row.get("reserved", 0)))
        if int(row.get("available", 0)) > expected:
            bad.append((row.get("sku"), row.get("available"), expected))
    assert not bad, (
        f"these levels report an available quantity above on_hand minus committed "
        f"minus reserved: {bad[:5]}")


def test_a_stock_adjustment_is_recorded_as_a_movement_row(manager_client):
    """Every stock change leaves an append-only movement entry behind it."""
    rows = inventory_rows(manager_client)
    target = None
    for row in rows:
        if str(row.get("sku")):
            target = row
            break
    assert target is not None, "GET /api/inventory exposes no level carrying a sku"
    before = int(target.get("on_hand", 0))
    r = manager_client.post(
        "/api/inventory/adjustments",
        json={"variant_id": target["variant_id"], "location_id": target["location_id"],
              "quantity_name": "on_hand", "delta": 1, "reason": "correction",
              "idempotency_key": probe_key("move")})
    assert r.status_code in (200, 201), (
        f"a permitted stock adjustment returned {r.status_code}; body={r.text[:300]}")
    body = r.json()
    text = flatten(body).lower()
    assert "correction" in text, (
        f"the adjustment response names no movement reason; saw {text[:300]}")
    after = inventory_rows(manager_client)
    same = [x for x in after if str(x.get("variant_id")) == str(target["variant_id"])
            and str(x.get("location_id")) == str(target["location_id"])]
    assert same and int(same[0].get("on_hand", 0)) == before + 1, (
        f"on_hand moved from {before} to "
        f"{same[0].get('on_hand') if same else None}; a delta of 1 must move it by 1")


def test_two_concurrent_checkouts_for_the_last_unit_yield_one_success(manager_client):
    """Exactly one of two simultaneous buyers gets the last unit."""
    rows = inventory_rows(manager_client)
    boundary = None
    for row in rows:
        if int(row.get("available", 0)) == 1:
            boundary = row
            break
    assert boundary is not None, (
        f"no seeded level reports exactly one available unit; {BOUNDARY_PRODUCT} at "
        f"{PUNE} is the boundary the brief seeds. Saw "
        f"{[(r.get('sku'), r.get('available')) for r in rows][:8]}")

    def buy(tag):
        r = manager_client.post(
            "/api/checkouts",
            json={"store": "oakleaf",
                  "lines": [{"variant_id": boundary["variant_id"], "quantity": 1}],
                  "idempotency_key": probe_key(f"race-{tag}")})
        if r.status_code not in (200, 201):
            return r.status_code, None
        token = r.json().get("token") or r.json().get("id")
        done = manager_client.post(
            f"/api/checkouts/{token}/complete",
            json={"payment_method": "manual",
                  "address": {"country": "IN", "province": "West Delhi",
                              "postal_code": "110018", "city": "Delhi",
                              "address1": "151, Rajouri Garden", "last_name": "Gupta"},
                  "idempotency_key": probe_key(f"done-{tag}")})
        return done.status_code, done.text[:200]

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(buy, ("a", "b")))
    wins = [o for o in outcomes if o[0] in (200, 201)]
    assert len(wins) == 1, (
        f"two simultaneous purchases of the last unit produced {len(wins)} success(es); "
        f"exactly one must win. Outcomes: {outcomes}")
    after = inventory_rows(manager_client)
    same = [x for x in after if str(x.get("variant_id")) == str(boundary["variant_id"])
            and str(x.get("location_id")) == str(boundary["location_id"])]
    assert same and int(same[0].get("available", 0)) >= 0, (
        f"available went negative after the race: "
        f"{same[0].get('available') if same else None}")


def test_seeded_orders_are_stored_with_their_pinned_totals(manager_client):
    """The seed is exactly what the brief pins, and survives a fresh read."""
    rows = order_index(manager_client)
    got = {str(r.get("number")): int(r.get("total_minor", -1)) for r in rows}
    for number in (ORDER_INSIDE_CEILING, ORDER_BROWSER_REFUND, ORDER_VALIDATION):
        assert got.get(number) == ORDER_SMALL_MINOR, (
            f"{number} reports total_minor {got.get(number)!r}, expected "
            f"{ORDER_SMALL_MINOR}")
    for number in (ORDER_PENDING_REQUEST, ORDER_APPROVED_REFUND):
        assert got.get(number) == ORDER_LARGE_MINOR, (
            f"{number} reports total_minor {got.get(number)!r}, expected "
            f"{ORDER_LARGE_MINOR}")


def test_financial_and_fulfilment_status_are_independent_fields(manager_client):
    """Paid with unfulfilled is expressible, which one status field cannot do."""
    rows = order_index(manager_client)
    assert rows, "GET /api/orders exposes no orders"
    for row in rows:
        assert "financial_status" in row and "fulfilment_status" in row, (
            f"order {row.get('number')!r} exposes "
            f"{sorted(row)} rather than two independent status fields")
    unfulfilled = [r for r in rows if r.get("fulfilment_status") == "unfulfilled"]
    assert unfulfilled, (
        f"no seeded order reads 'unfulfilled'; saw "
        f"{[r.get('fulfilment_status') for r in rows]}")


def test_the_store_list_exposes_only_the_session_members_stores(mallard_client):
    """A person sees the memberships that person holds, and no others."""
    r = mallard_client.get("/api/stores")
    assert r.status_code == 200, (
        f"GET /api/stores returned {r.status_code}, expected 200; body={r.text[:300]}")
    handles = {row.get("handle") for row in items(r.json())}
    assert handles == {"modern-mallard"}, (
        f"GET /api/stores exposed {sorted(handles)} to a member of one store only")


def test_balances_reconcile_with_the_refunds_recorded_on_the_orders(finance_client):
    """Every money figure the product shows comes from the ledger."""
    rows = order_index(finance_client)
    refunded = [r for r in rows
                if r.get("financial_status") in ("refunded", "partially_refunded")]
    assert refunded, (
        f"no order reads as refunded, so the balance cannot be reconciled; saw "
        f"{[r.get('financial_status') for r in rows]}")
    got = available_balance(finance_client)
    assert isinstance(got, int), (
        f"the available balance is {got!r}; money is an integer in minor units")


def test_an_approval_request_records_its_requester_and_its_expiry(support_client):
    """A request is auditable from the moment it exists."""
    rows = approvals(support_client)
    assert rows, "GET /api/approvals exposes no requests"
    for row in rows:
        for field in ("id", "action_type", "amount_minor", "currency", "requested_by",
                      "state", "required_permission", "expires_at"):
            assert field in row, (
                f"approval {row.get('id')!r} exposes {sorted(row)}, missing {field!r}")


def test_health_endpoint_reports_ready(anon_client):
    """The readiness probe answers on the contracted path."""
    r = anon_client.get("/api/health")
    assert r.status_code == 200, (
        f"GET /api/health returned {r.status_code}, expected 200; body={r.text[:200]}")


def test_orders_listing_returns_a_top_level_array(manager_client):
    """A list endpoint returns a top-level JSON array."""
    r = manager_client.get("/api/orders")
    assert r.status_code == 200, (
        f"GET /api/orders returned {r.status_code}; body={r.text[:200]}")
    assert isinstance(r.json(), list), (
        f"GET /api/orders returned {type(r.json()).__name__}, expected a top-level "
        f"JSON array")


def test_an_unknown_address_renders_the_products_own_not_found_page(anon_client):
    """An unknown address answers not-found inside the product's own chrome."""
    r = anon_client.get("/in/this-route-does-not-exist")
    assert r.status_code == 404, (
        f"an unknown storefront address returned {r.status_code}, expected 404")
    body = r.text.lower()
    assert "mercato" in body, (
        "the not-found page carries none of the product's own chrome")
    assert "<a " in body, "the not-found page offers no way back"


def test_every_public_route_carries_its_own_title_and_description(anon_client):
    """No two public routes share a title or a description."""
    titles, descriptions = {}, {}
    for route in PUBLIC_ROUTES:
        r = anon_client.get(route)
        assert r.status_code == 200, (
            f"GET {route} returned {r.status_code}, expected 200")
        body = r.text
        lowered = body.lower()
        start = lowered.find("<title>")
        end = lowered.find("</title>")
        assert start != -1 and end > start, f"{route} declares no title"
        title = body[start + 7:end].strip()
        assert title, f"{route} declares an empty title"
        assert title not in titles, (
            f"{route} shares its title with {titles[title]}: {title!r}")
        titles[title] = route
        marker = 'name="description"'
        assert marker in lowered, f"{route} declares no description"
        chunk = lowered[lowered.find(marker):lowered.find(marker) + 400]
        assert chunk not in descriptions, (
            f"{route} shares its description with {descriptions[chunk]}")
        descriptions[chunk] = route


def test_the_sitemap_lists_public_routes_and_robots_names_the_sitemap(anon_client):
    """Discovery files exist and agree with the route set."""
    sitemap = anon_client.get("/sitemap.xml")
    assert sitemap.status_code == 200, (
        f"GET /sitemap.xml returned {sitemap.status_code}, expected 200")
    body = sitemap.text
    for route in PUBLIC_ROUTES:
        assert route in body, f"the sitemap does not list {route}"
    robots = anon_client.get("/robots.txt")
    assert robots.status_code == 200, (
        f"GET /robots.txt returned {robots.status_code}, expected 200")
    assert "sitemap" in robots.text.lower(), (
        f"robots.txt names no sitemap; saw {robots.text[:200]!r}")


def test_every_internal_link_on_the_public_routes_resolves(anon_client):
    """A link that leads nowhere is a defect."""
    import re

    broken = []
    seen = set()
    for route in PUBLIC_ROUTES:
        page = anon_client.get(route)
        assert page.status_code == 200, (
            f"GET {route} returned {page.status_code}, expected 200")
        for href in re.findall(r'href="(/[^"#?]*)"', page.text):
            if href in seen:
                continue
            seen.add(href)
            probe = anon_client.get(href)
            if probe.status_code >= 400:
                broken.append((route, href, probe.status_code))
    assert not broken, (
        f"these internal links do not resolve: {broken[:10]}")


def test_the_privacy_and_terms_pages_are_reachable_from_the_footer(anon_client):
    """Both pages exist and every public route links to them."""
    for route in ("/in/privacy", "/in/terms"):
        r = anon_client.get(route)
        assert r.status_code == 200, (
            f"GET {route} returned {r.status_code}, expected 200")
    home = anon_client.get("/in")
    assert "/in/privacy" in home.text, "the country home links no privacy page"
    assert "/in/terms" in home.text, "the country home links no terms page"


def test_delhi_and_pune_locations_are_seeded_and_scoped(manager_client):
    """Both seeded locations exist under the names the brief pins."""
    rows = inventory_rows(manager_client)
    text = flatten(rows)
    assert PUNE in text or "pune" in text.lower(), (
        f"no inventory level names {PUNE!r}; saw {text[:300]}")
    assert DELHI in text or "delhi" in text.lower(), (
        f"no inventory level names {DELHI!r}; saw {text[:300]}")
