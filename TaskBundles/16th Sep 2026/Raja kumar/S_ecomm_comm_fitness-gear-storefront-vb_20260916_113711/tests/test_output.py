"""Black-box grading for deku/fitness-gear-storefront-vb.

Every assertion reads the running application over HTTP, drives its rendered
pages in Chromium, reads the Mailpit inbox the app sends to, or reads the Kill
Bill tenant the app invoices into. Nothing imports the agent's code or names a
mechanism it was free to choose.
"""

from __future__ import annotations

import re
from datetime import timedelta

import httpx

from conftest import (
    APP_SECRETS, CUSTOMER2_PHONE, CUSTOMER3_PHONE, CUSTOMER4_EMAIL, CUSTOMER4_PHONE,
    GIFT_SKU, MASSAGE_GUN, MASSAGE_GUN_SKU, NOT_FOUND_COPY, PAGE_SIZE, POSTAL_COD,
    POSTAL_HIGH_REFUSAL, POSTAL_PREPAID_ONLY, PRICE_SENTENCE, PUBLIC_ROUTES, TRACK_KEYS,
    add_line, address, advance_for, allocate, amount_of, api, carrier, cart_with, deliver,
    error_code, error_of, expect, first_line, fresh_code, get_cart, guest_cod_order,
    hold_seconds, in_parallel, invoices_for, invoices_settled, keys_named,
    mail_ids, mails_to, merchant_order, merchant_variant, new_cart, new_product, now_utc,
    order_for, pack, place, prepaid_order, product, request_code, rupees, set_variant,
    settle, sign_in, signed, track, transition, unique, unique_email, unique_phone,
    variant_of, wait_for_mail, walk_products,
)
from appclient import app_url

CUSTOMER2_EMAIL = "customer2@example.com"
CUSTOMER3_EMAIL = "customer3@example.com"


def test_cash_on_delivery_order_needs_a_verified_phone(merchant_token):
    """A cash on delivery order is refused until the phone presents its own fresh code."""
    item = new_product(merchant_token, prices=(129900,), on_hand=5)
    sku = item["skus"][0]
    cart = cart_with({sku: 1})
    phone, email = unique_phone(), unique_email()

    missing = place(cart, phone, email, "on_delivery")
    assert missing.status_code == 422 and error_code(missing) == "verification_required", (
        f"a cash on delivery order with no code answered {missing.status_code}: "
        f"{missing.text[:300]}")
    wrong = place(cart, phone, email, "on_delivery", code="000000")
    assert wrong.status_code == 422 and error_code(wrong) == "invalid_code", wrong.text[:300]

    other_phone, other_email = unique_phone(), unique_email()
    borrowed = fresh_code(other_phone, other_email)
    stolen = place(cart, phone, email, "on_delivery", code=borrowed)
    assert stolen.status_code == 422 and error_code(stolen) == "invalid_code", (
        f"a code sent for another phone was accepted: {stolen.status_code} {stolen.text[:300]}")
    assert merchant_variant(merchant_token, sku)["on_hand"] == 5, (
        "a refused placement took stock")

    code = fresh_code(phone, email)
    order = expect(place(cart, phone, email, "on_delivery", code=code), 201)
    assert order["payment_method"] == "on_delivery", order
    assert merchant_variant(merchant_token, sku)["on_hand"] == 4


def test_cash_on_delivery_invoice_appears_only_at_delivery_and_only_once(merchant_token):
    """No invoice while the parcel travels; exactly one, in rupees, once it is delivered."""
    item = new_product(merchant_token, prices=(129900,), on_hand=5)
    placed = guest_cod_order({item["skus"][0]: 1})
    order, phone = placed["order"], placed["phone"]
    number, total = order["number"], order["total_minor"]
    assert order["amount_due_on_delivery_minor"] == total, order

    settle(3)
    assert invoices_for(phone, number) == [], (
        "a cash on delivery order was invoiced before it was delivered")
    pack(merchant_token, number)
    moment = now_utc()
    for offset, status in ((-3, "shipped"), (-2, "out_for_delivery")):
        assert carrier(number, status, moment + timedelta(hours=offset)).status_code == 204
    settle(3)
    assert invoices_for(phone, number) == [], "the order was invoiced while out for delivery"

    delivered = carrier(number, "delivered", moment, event_id=f"evt-delivered-{number}")
    assert delivered.status_code == 204, delivered.text[:300]
    found = invoices_settled(phone, number, 1)
    assert len(found) == 1, f"{len(found)} invoices after delivery, expected exactly one"
    assert amount_of(found[0]) == rupees(total), (
        f"the delivery invoice is {found[0].get('amount')}, expected {rupees(total)}")
    assert str(found[0].get("currency")).upper() == "INR", found[0].get("currency")

    again = carrier(number, "delivered", moment, event_id=f"evt-delivered-{number}")
    assert again.status_code == 204, again.text[:300]
    settle(4)
    assert len(invoices_for(phone, number)) == 1, (
        "a repeated delivery report raised a second invoice")


def test_placed_email_states_the_amount_due_to_the_courier(merchant_token):
    """The placed message names the exact rupees and paise to have ready, once."""
    item = new_product(merchant_token, prices=(129950,), on_hand=5)
    placed = guest_cod_order({item["skus"][0]: 1})
    order, email = placed["order"], placed["email"]
    assert order["amount_due_on_delivery_minor"] == 129950, order
    subject = f"Peakfit order {order['number']} placed"
    message = wait_for_mail(email, subject, set())
    assert message, f"no `{subject}` email reached {email}"
    expected = f"Order {order['number']} placed. Have ₹1,299.50 ready for the courier."
    assert first_line(message["text"]) == expected, (
        f"the placed email opens {first_line(message['text'])!r}, expected {expected!r}")
    settle(3)
    assert len(mails_to(email, subject)) == 1, "the placed email was sent more than once"


def test_prepaid_order_is_invoiced_at_placement_for_the_total(merchant_token):
    """A prepaid order is confirmed and invoiced for its total the moment it is placed."""
    item = new_product(merchant_token, prices=(234500,), on_hand=5)
    placed = prepaid_order({item["skus"][0]: 1})
    order, phone = placed["order"], placed["phone"]
    assert order["state"] == "confirmed", f"a prepaid order is {order['state']}"
    assert order["amount_due_on_delivery_minor"] == 0 and order["advance_minor"] == 0, order
    found = invoices_settled(phone, order["number"], 1)
    assert len(found) == 1, f"{len(found)} invoices for a prepaid order, expected one"
    assert amount_of(found[0]) == rupees(order["total_minor"]), found[0].get("amount")
    assert str(found[0].get("currency")).upper() == "INR"
    token = sign_in(phone, placed["email"])
    with api(token) as c:
        mine = expect(c.get("/api/orders"), 200)
    assert order["number"] in [o.get("number") for o in mine.get("items", [])], (
        "verifying the phone of a guest order did not claim the order")


def test_replayed_placement_is_the_same_order_with_no_second_invoice(merchant_token):
    """The same key and body return the order already made and make nothing more."""
    item = new_product(merchant_token, prices=(159900,), on_hand=6)
    sku = item["skus"][0]
    cart = cart_with({sku: 2})
    phone, email, key = unique_phone(), unique_email(), unique("replay")
    fixed_address = address()
    first = place(cart, phone, email, "prepaid", key=key, ship_to=fixed_address)
    order = expect(first, 201)
    second = place(cart, phone, email, "prepaid", key=key, ship_to=fixed_address)
    replay = expect(second, 200)
    assert replay["number"] == order["number"], (
        f"a replayed placement made order {replay['number']} beside {order['number']}")
    settle(4)
    assert len(invoices_for(phone, order["number"])) == 1, "a replay raised a second invoice"
    assert len(mails_to(email, f"Peakfit order {order['number']} placed")) == 1
    assert merchant_variant(merchant_token, sku)["on_hand"] == 4, "a replay took stock twice"


def test_simultaneous_placements_under_one_key_make_one_order(merchant_token):
    """Two identical placements at the same instant make exactly one order and one invoice."""
    item = new_product(merchant_token, prices=(149900,), on_hand=6)
    sku = item["skus"][0]
    cart = cart_with({sku: 1})
    phone, email, key = unique_phone(), unique_email(), unique("race")
    fixed_address = address()
    results = in_parallel(2, lambda _: place(cart, phone, email, "prepaid", key=key,
                                             ship_to=fixed_address))
    statuses = sorted(r.status_code for r in results)
    assert statuses.count(201) == 1 and statuses[0] in (200, 201, 409), (
        f"two simultaneous placements under one key answered {statuses}")
    numbers = {r.json()["number"] for r in results if r.status_code in (200, 201)}
    assert len(numbers) == 1, f"one key made orders {numbers}"
    settle(4)
    assert len(invoices_for(phone, numbers.pop())) == 1, "two invoices for one key"
    assert merchant_variant(merchant_token, sku)["on_hand"] == 5, "stock was taken twice"


def test_one_key_with_another_bag_is_refused_and_a_placed_bag_is_closed(merchant_token):
    """A reused key with a different body is refused; an ordered bag cannot be ordered again."""
    item = new_product(merchant_token, prices=(99900,), on_hand=8)
    sku = item["skus"][0]
    first_cart, second_cart = cart_with({sku: 1}), cart_with({sku: 2})
    phone, email, key = unique_phone(), unique_email(), unique("reuse")
    expect(place(first_cart, phone, email, "prepaid", key=key), 201)
    reused = place(second_cart, phone, email, "prepaid", key=key)
    assert reused.status_code == 409 and error_code(reused) == "idempotency_key_reused", (
        f"a key reused with another bag answered {reused.status_code}: {reused.text[:300]}")
    assert merchant_variant(merchant_token, sku)["on_hand"] == 7
    expect(place(second_cart, phone, email, "prepaid"), 201)
    closed = place(first_cart, phone, email, "prepaid")
    assert closed.status_code == 409 and error_code(closed) == "cart_closed", closed.text[:300]
    assert merchant_variant(merchant_token, sku)["on_hand"] == 5


def test_two_bags_racing_for_the_last_unit_hold_it_once(merchant_token):
    """Exactly one of two simultaneous holds on the last unit succeeds."""
    item = new_product(merchant_token, prices=(59900,), on_hand=1)
    sku = item["skus"][0]
    carts = [new_cart(), new_cart()]
    results = in_parallel(2, lambda i: add_line(carts[i], sku, 1))
    statuses = sorted(r.status_code for r in results)
    assert statuses == [200, 409], (
        f"two bags asking for the last unit at once answered {statuses}; exactly one may hold it")
    refused = next(r for r in results if r.status_code == 409)
    assert error_code(refused) == "insufficient_stock", refused.text[:300]
    assert variant_of(item["handle"], sku)["available"] == 0


def test_a_hold_ends_on_time_and_returns_its_unit_exactly_once(merchant_token):
    """An expired hold frees its unit once; the bag that let it lapse can no longer buy it."""
    item = new_product(merchant_token, prices=(59900,), on_hand=1)
    sku = item["skus"][0]
    holder = cart_with({sku: 1})
    assert variant_of(item["handle"], sku)["available"] == 0, "a held unit still reads available"
    late = new_cart()
    refused = add_line(late, sku, 1)
    assert refused.status_code == 409 and error_code(refused) == "insufficient_stock"
    settle(hold_seconds() + 4)
    assert variant_of(item["handle"], sku)["available"] == 1, (
        "after the hold ended the unit is not available exactly once")
    expect(add_line(late, sku, 1), 200)
    assert variant_of(item["handle"], sku)["available"] == 0
    lapsed = place(holder, unique_phone(), unique_email(), "prepaid")
    assert lapsed.status_code == 409 and error_code(lapsed) == "stock_changed", (
        f"a bag whose hold ended bought a unit held by another bag: {lapsed.status_code}")
    assert sku in {line.get("sku") for line in error_of(lapsed).get("lines", [])}
    assert merchant_variant(merchant_token, sku)["on_hand"] == 1


def test_placements_needing_more_than_on_hand_sell_it_once(merchant_token):
    """After a recount below what bags hold, simultaneous placements never oversell."""
    item = new_product(merchant_token, prices=(79900,), on_hand=3)
    sku = item["skus"][0]
    carts = [cart_with({sku: 2}), cart_with({sku: 1})]
    set_variant(merchant_token, sku, on_hand=2)
    results = in_parallel(2, lambda i: place(carts[i], unique_phone(), unique_email(), "prepaid"))
    statuses = sorted(r.status_code for r in results)
    assert statuses == [201, 409], (
        f"two placements needing three units of two answered {statuses}; exactly one may succeed")
    loser = next(r for r in results if r.status_code == 409)
    assert error_code(loser) == "stock_changed", loser.text[:300]
    winner = next(r for r in results if r.status_code == 201).json()
    sold = sum(line["quantity"] for line in winner["lines"])
    on_hand = merchant_variant(merchant_token, sku)["on_hand"]
    assert on_hand == 2 - sold and on_hand >= 0, (
        f"on hand is {on_hand} after selling {sold} of 2")


def test_a_price_change_shows_at_the_line(merchant_token):
    """The bag names a changed price on its line and totals at the current price."""
    item = new_product(merchant_token, prices=(129900,), on_hand=5)
    sku = item["skus"][0]
    cart = cart_with({sku: 1})
    set_variant(merchant_token, sku, price_minor=139900)
    line = next(l for l in get_cart(cart["token"])["lines"] if l["sku"] == sku)
    assert line["price_changed"] is True, f"the line does not report its price change: {line}"
    assert (line["unit_price_at_add_minor"], line["current_price_minor"]) == (129900, 139900), line
    assert line["line_total_minor"] == 139900, line


def test_a_stale_total_is_refused_with_the_differences_then_accepted(merchant_token):
    """The server's total wins; a stale or lowered client total stops the order."""
    item = new_product(merchant_token, prices=(129900,), on_hand=5)
    sku = item["skus"][0]
    cart = cart_with({sku: 1})
    phone, email = unique_phone(), unique_email()
    set_variant(merchant_token, sku, price_minor=149900)
    stale = place(cart, phone, email, "prepaid", expected_total=129900)
    assert stale.status_code == 409 and error_code(stale) == "price_changed", (
        f"a placement at a stale price answered {stale.status_code}: {stale.text[:300]}")
    err = error_of(stale)
    assert {"sku": sku, "old_minor": 129900, "new_minor": 149900} in err.get("changes", []), err
    assert err.get("total_minor") == 149900, err
    assert merchant_variant(merchant_token, sku)["on_hand"] == 5, "a refused placement took stock"
    order = expect(place(cart, phone, email, "prepaid", expected_total=149900), 201)
    assert order["total_minor"] == 149900 and order["lines"][0]["unit_price_minor"] == 149900

    other = new_product(merchant_token, prices=(129900,), on_hand=5)
    fresh = cart_with({other["skus"][0]: 1})
    lowered = place(fresh, unique_phone(), unique_email(), "prepaid",
                    expected_total=fresh["total_minor"] - 100)
    assert lowered.status_code == 409 and error_code(lowered) == "price_changed", (
        f"a client total lower than the server's was accepted: {lowered.status_code}")


def test_the_order_keeps_its_own_copy_of_the_address(customer5_token, merchant_token):
    """Editing a saved address never changes where a placed order was sent."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    with api(customer5_token) as c:
        saved = expect(c.post("/api/account/addresses", json=address()), 201)
    cart = cart_with({item["skus"][0]: 1})
    order = expect(place(cart, "9000000015", "customer5@example.com", "prepaid",
                         token=customer5_token, address_id=saved["id"]), 201)
    assert order["address"]["line1"] == saved["line1"], order["address"]
    with api(customer5_token) as c:
        expect(c.patch(f"/api/account/addresses/{saved['id']}",
                       json={"line1": "99 Changed Street"}), 200)
    reread = expect(order_for(customer5_token, order["number"]), 200)
    assert reread["address"]["line1"] == saved["line1"], (
        f"editing the saved address changed the order's address to {reread['address']['line1']!r}")


def test_a_line_sold_out_before_placement_is_named_and_nothing_is_taken(merchant_token):
    """A line that can no longer be sold stops the whole order and takes no stock at all."""
    kept = new_product(merchant_token, prices=(69900,), on_hand=5)
    gone = new_product(merchant_token, prices=(79900,), on_hand=5)
    cart = cart_with({kept["skus"][0]: 1, gone["skus"][0]: 1})
    set_variant(merchant_token, gone["skus"][0], on_hand=0)
    refused = place(cart, unique_phone(), unique_email(), "prepaid")
    assert refused.status_code == 409 and error_code(refused) == "stock_changed", refused.text[:300]
    named = {line.get("sku") for line in error_of(refused).get("lines", [])}
    assert gone["skus"][0] in named and kept["skus"][0] not in named, named
    assert merchant_variant(merchant_token, kept["skus"][0])["on_hand"] == 5, (
        "the sellable line's stock was taken by an order that was refused")


def test_threshold_discounts_never_stack_and_read_the_subtotal_before_discounts(merchant_token):
    """Only the highest threshold applies, measured on the subtotal before any code."""
    shoe = new_product(merchant_token, department="SPORTS SHOES", sub_category="running",
                       prices=(279900,), on_hand=20)
    band = new_product(merchant_token, prices=(29900,), on_hand=20)
    pair = cart_with({shoe["skus"][0]: 2})
    assert pair["merchandise_subtotal_minor"] == 559800
    assert {d["promotion"]: d["amount_minor"] for d in pair["discounts"]} == {"flat-500-4999": 50000}, (
        f"the discounts on a 5,598 bag are {pair['discounts']}; the flat discounts never stack")
    assert {g["sku"]: g["quantity"] for g in pair["gift_lines"]} == {GIFT_SKU: 1}
    assert (pair["discount_minor"], pair["shipping_minor"], pair["total_minor"]) == (50000, 0, 509800)
    assert pair["next_promotion"] is None, pair["next_promotion"]

    mixed = new_cart()
    expect(add_line(mixed, shoe["skus"][0], 1), 200)
    expect(add_line(mixed, band["skus"][0], 1), 200)
    with api() as c:
        coded = expect(c.post(f"/api/carts/{mixed}/promotions", json={"code": "STRIDE10"}), 200)
    applied = {d["promotion"]: d["amount_minor"] for d in coded["discounts"]}
    assert applied == {"STRIDE10": 27990, "flat-200-2999": 20000}, (
        f"a 3,098 bag with STRIDE10 carries {applied}; the threshold reads the subtotal before "
        f"the code")
    assert (coded["discount_minor"], coded["total_minor"]) == (47990, 261810), coded
    assert coded["next_promotion"] == {"promotion": "flat-500-4999", "threshold_minor": 499900,
                                       "remaining_minor": 190100}, coded["next_promotion"]


def test_a_code_takes_only_its_eligible_lines(merchant_token):
    """STRIDE10 discounts shoes and apparel only, and is refused on a bag with neither."""
    band = new_product(merchant_token, prices=(129900,), on_hand=20)
    tee = new_product(merchant_token, department="APPAREL", sub_category="tops",
                      prices=(69900,), on_hand=20)
    bands_only = new_cart()
    expect(add_line(bands_only, band["skus"][0], 1), 200)
    with api() as c:
        refused = c.post(f"/api/carts/{bands_only}/promotions", json={"code": "STRIDE10"})
    assert refused.status_code == 422 and error_code(refused) == "not_applicable", refused.text[:300]
    small = cart_with({tee["skus"][0]: 1})
    assert (small["shipping_minor"], small["total_minor"]) == (9900, 79800), (
        f"a 699 bag reads shipping {small['shipping_minor']} and total {small['total_minor']}")
    both = new_cart()
    expect(add_line(both, band["skus"][0], 1), 200)
    expect(add_line(both, tee["skus"][0], 1), 200)
    with api() as c:
        coded = expect(c.post(f"/api/carts/{both}/promotions", json={"code": "STRIDE10"}), 200)
    applied = {d["promotion"]: d["amount_minor"] for d in coded["discounts"]}
    assert applied.get("STRIDE10") == 6990, (
        f"STRIDE10 on a band and a tee took {applied.get('STRIDE10')}, expected 6990 from the tee only")


def test_the_meter_counts_from_the_merchandise_subtotal(merchant_token):
    """The gift and the distance to the next offer read the subtotal before any code."""
    shoe = new_product(merchant_token, department="SPORTS SHOES", sub_category="running",
                       prices=(199800,), on_hand=20)
    top_up = new_product(merchant_token, prices=(100,), on_hand=20)
    cart = new_cart()
    expect(add_line(cart, shoe["skus"][0], 1), 200)
    with api() as c:
        coded = expect(c.post(f"/api/carts/{cart}/promotions", json={"code": "STRIDE10"}), 200)
    assert (coded["discount_minor"], coded["total_minor"]) == (19980, 179820), coded
    assert coded["gift_lines"] == [], coded["gift_lines"]
    assert coded["next_promotion"] == {"promotion": "free-gift-1999", "threshold_minor": 199900,
                                       "remaining_minor": 100}, (
        f"with a 1,998 subtotal and a code the meter reads {coded['next_promotion']}; it counts "
        f"from the subtotal before the code")
    reached = expect(add_line(cart, top_up["skus"][0], 1), 200)
    assert reached["merchandise_subtotal_minor"] == 199900, reached
    assert {g["sku"]: g["quantity"] for g in reached["gift_lines"]} == {GIFT_SKU: 1}, (
        f"a subtotal of exactly 1,999 under a code carries gifts {reached['gift_lines']}")
    assert {d["promotion"] for d in reached["discounts"]} == {"STRIDE10"}, reached["discounts"]
    assert reached["next_promotion"] == {"promotion": "flat-200-2999", "threshold_minor": 299900,
                                         "remaining_minor": 100000}, reached["next_promotion"]


def test_an_order_discount_is_split_across_lines_to_the_paisa(merchant_token):
    """Each discount is apportioned by largest remainder and adds up exactly."""
    prices = (33333, 99999, 166668)
    items = [new_product(merchant_token, prices=(p,), on_hand=10) for p in prices]
    cart = new_cart()
    for made in items:
        expect(add_line(cart, made["skus"][0], 1), 200)
    order = expect(place(get_cart(cart), unique_phone(), unique_email(), "prepaid"), 201)
    assert order["discount_minor"] == 20000, order["discount_minor"]
    shares = [line["allocated_discount_minor"] for line in order["lines"]]
    assert shares == allocate(20000, list(prices)) == [2222, 6667, 11111], (
        f"the 200 discount was split {shares}; expected [2222, 6667, 11111]")
    for line in order["lines"]:
        assert line["paid_minor"] == line["line_total_minor"] - line["allocated_discount_minor"], line
    assert order["total_minor"] == 280000, order["total_minor"]
    assert order["tax_minor"] == 42712, (
        f"tax on a 2,800 total is {order['tax_minor']}; tax is the 18 per cent already inside the total")
    even = [new_product(merchant_token, prices=(100000,), on_hand=10) for _ in range(3)]
    third = new_cart()
    for made in even:
        expect(add_line(third, made["skus"][0], 1), 200)
    split = expect(place(get_cart(third), unique_phone(), unique_email(), "prepaid"), 201)
    assert [l["allocated_discount_minor"] for l in split["lines"]] == [6667, 6667, 6666]


def test_a_prepaid_only_postal_code_refuses_cash_on_delivery_at_placement(merchant_token):
    """Payment on delivery is re-checked at placement by postal code; prepaid still goes through."""
    item = new_product(merchant_token, prices=(99900,), on_hand=10)
    cart = cart_with({item["skus"][0]: 1})
    phone, email = unique_phone(), unique_email()
    code = fresh_code(phone, email)
    refused = place(cart, phone, email, "on_delivery", POSTAL_PREPAID_ONLY, code=code)
    assert refused.status_code == 422 and error_code(refused) == "cod_unavailable", refused.text[:300]
    assert error_of(refused).get("reason") == "postal_code", error_of(refused)
    expect(place(cart, phone, email, "prepaid", POSTAL_PREPAID_ONLY), 201)


def test_cash_on_delivery_is_refused_above_the_cap_and_for_an_ineligible_product(merchant_token):
    """The cart value cap and a product's eligibility both bind at placement."""
    costly = new_product(merchant_token, prices=(1060000,), on_hand=5)
    big = cart_with({costly["skus"][0]: 1})
    assert big["total_minor"] > 999900, big["total_minor"]
    phone, email = unique_phone(), unique_email()
    code = fresh_code(phone, email)
    over = place(big, phone, email, "on_delivery", code=code)
    assert over.status_code == 422 and error_of(over).get("reason") == "cart_value", over.text[:300]
    expect(place(big, phone, email, "prepaid"), 201)

    plate = new_product(merchant_token, prices=(159900,), on_hand=5, cod_eligible=False)
    with api() as c:
        check = expect(c.get("/api/delivery-check", params={"postal_code": POSTAL_COD,
                                                              "sku": plate["skus"][0]}), 200)
    assert check.get("cod_available") is False, check
    ineligible = cart_with({plate["skus"][0]: 1})
    other_phone, other_email = unique_phone(), unique_email()
    other_code = fresh_code(other_phone, other_email)
    refused = place(ineligible, other_phone, other_email, "on_delivery", code=other_code)
    assert refused.status_code == 422 and error_of(refused).get("reason") == "product", refused.text[:300]


def test_a_partial_advance_is_invoiced_at_placement_and_the_rest_at_delivery(merchant_token):
    """Above 4,999 payment on delivery takes a rounded-up advance now and the rest on delivery."""
    shoe = new_product(merchant_token, department="SPORTS SHOES", sub_category="running",
                       prices=(279900,), on_hand=10)
    placed = guest_cod_order({shoe["skus"][0]: 2})
    order, phone, email = placed["order"], placed["phone"], placed["email"]
    total = order["total_minor"]
    assert total == 509800, total
    assert order["payment_method"] == "partial_advance", order["payment_method"]
    assert order["advance_minor"] == advance_for(total) == 102000, order["advance_minor"]
    assert order["amount_due_on_delivery_minor"] == 407800, order["amount_due_on_delivery_minor"]
    at_placement = invoices_settled(phone, order["number"], 1)
    assert [amount_of(i) for i in at_placement] == ["1020.00"], (
        f"invoices at placement are {[i.get('amount') for i in at_placement]}; expected the advance")
    message = wait_for_mail(email, f"Peakfit order {order['number']} placed", set())
    assert message and first_line(message["text"]) == (
        f"Order {order['number']} placed. Have ₹4,078 ready for the courier."), message
    deliver(merchant_token, order["number"])
    after = invoices_settled(phone, order["number"], 2)
    assert sorted(amount_of(i) for i in after) == ["1020.00", "4078.00"], (
        f"invoices after delivery are {[i.get('amount') for i in after]}")


def test_an_unsigned_or_stale_carrier_event_changes_nothing(merchant_token):
    """A carrier event needs a fresh signature made with the carrier secret."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    order = prepaid_order({item["skus"][0]: 1})["order"]
    number = order["number"]
    pack(merchant_token, number)
    for signature in ("t=1,v1=deadbeef", None, "stale"):
        event_id = unique("evt")
        raw = ('{"event_id":"%s","order_number":"%s","status":"shipped","occurred_at":"%s"}'
               % (event_id, number, now_utc().strftime("%Y-%m-%dT%H:%M:%SZ")))
        if signature is None:
            header = signed(raw, secret="not-the-carrier-secret")
        elif signature == "stale":
            header = signed(raw, at=int(now_utc().timestamp()) - 900)
        else:
            header = signature
        with api() as c:
            response = c.post("/api/webhooks/carrier", content=raw.encode(),
                              headers={"Content-Type": "application/json",
                                       "X-Carrier-Signature": header})
        assert response.status_code == 401, (
            f"a carrier event with signature {header[:24]!r} answered {response.status_code}")
    state = merchant_order(merchant_token, number)
    assert state["state"] == "packed", f"a refused carrier event moved the order to {state['state']}"
    assert "shipped" not in [t.get("status") for t in state.get("timeline", [])]


def test_a_repeated_carrier_event_applies_once(merchant_token):
    """The same event identifier twice changes nothing more; a new attempt is recorded."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    placed = prepaid_order({item["skus"][0]: 1})
    number, email = placed["order"]["number"], placed["email"]
    subject = f"Peakfit order {number} arrives today"
    pack(merchant_token, number)
    assert carrier(number, "shipped", event_id=f"ship-{number}").status_code == 204
    for _ in range(2):
        response = carrier(number, "out_for_delivery", event_id=f"ofd-{number}")
        assert response.status_code == 204, response.text[:300]
    timeline = [t.get("status") for t in merchant_order(merchant_token, number)["timeline"]]
    assert timeline.count("out_for_delivery") == 1, f"the timeline reads {timeline}"
    settle(4)
    arrives = mails_to(email, subject)
    assert len(arrives) == 1, f"{len(arrives)} out for delivery emails for one event"

    attempt = carrier(number, "out_for_delivery", event_id=f"ofd-again-{number}",
                      window="15:00 and 18:00")
    assert attempt.status_code == 204, attempt.text[:300]
    timeline = [t.get("status") for t in merchant_order(merchant_token, number)["timeline"]]
    assert timeline.count("out_for_delivery") == 2, (
        f"a further delivery attempt was not recorded: the timeline reads {timeline}")
    second = wait_for_mail(email, subject, {m["id"] for m in arrives})
    assert second and "15:00 and 18:00" in first_line(second["text"]), (
        "the further attempt sent no out for delivery email naming its window")


def test_a_stale_event_never_moves_an_order_backwards(merchant_token):
    """An earlier status arriving late changes nothing; a status that skips ahead is refused."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    number = prepaid_order({item["skus"][0]: 1})["order"]["number"]
    deliver(merchant_token, number)
    late = carrier(number, "shipped")
    assert late.status_code == 204, late.text[:300]
    after = merchant_order(merchant_token, number)
    assert after["state"] == "delivered", f"a late shipped event moved the order to {after['state']}"
    assert [t.get("status") for t in after["timeline"]].count("shipped") == 1

    other = prepaid_order({item["skus"][0]: 1})["order"]["number"]
    pack(merchant_token, other)
    jump = carrier(other, "delivered")
    assert jump.status_code == 409 and error_code(jump) == "illegal_transition", jump.text[:300]
    assert merchant_order(merchant_token, other)["state"] == "packed"


def test_a_refused_parcel_returns_its_units_to_stock_exactly_once(merchant_token):
    """Refused is its own state, and returned to origin restores stock once however often it is reported."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    sku = item["skus"][0]
    placed = guest_cod_order({sku: 2})
    number, phone = placed["order"]["number"], placed["phone"]
    assert merchant_variant(merchant_token, sku)["on_hand"] == 3
    pack(merchant_token, number)
    for status in ("shipped", "out_for_delivery", "refused"):
        assert carrier(number, status).status_code == 204
    assert merchant_order(merchant_token, number)["state"] == "refused"
    assert carrier(number, "returning").status_code == 204
    home = carrier(number, "returned_to_origin", event_id=f"rto-{number}")
    assert home.status_code == 204
    assert merchant_variant(merchant_token, sku)["on_hand"] == 5
    assert carrier(number, "returned_to_origin", event_id=f"rto-{number}").status_code == 204
    assert carrier(number, "returned_to_origin").status_code == 204
    assert merchant_variant(merchant_token, sku)["on_hand"] == 5, (
        "stock was restored more than once for one returned parcel")
    assert merchant_order(merchant_token, number)["state"] == "returned_to_origin"
    settle(3)
    assert invoices_for(phone, number) == [], "a refused cash on delivery order was invoiced"


def test_a_customer_cancels_before_packing_and_the_units_return(customer5_token, merchant_token):
    """Cancelling a placed order returns its units and raises no invoice."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    sku = item["skus"][0]
    cart = cart_with({sku: 2})
    order = expect(place(cart, "9000000015", "customer5@example.com", "on_delivery",
                         token=customer5_token), 201)
    assert merchant_variant(merchant_token, sku)["on_hand"] == 3
    with api(merchant_token) as c:
        bare = c.post(f"/api/merchant/orders/{order['number']}/transitions", json={"to": "cancelled"})
    assert bare.status_code == 422 and error_code(bare) == "reason_required", bare.text[:300]
    assert merchant_order(merchant_token, order["number"])["state"] in ("placed", "confirmed")
    with api(customer5_token) as c:
        cancelled = expect(c.post(f"/api/orders/{order['number']}/cancel",
                                  json={"reason": "changed my mind"}), 200)
    assert cancelled["state"] == "cancelled", cancelled["state"]
    assert merchant_variant(merchant_token, sku)["on_hand"] == 5
    settle(3)
    assert invoices_for("9000000015", order["number"]) == []


def test_cancelling_after_packing_is_refused_and_the_order_is_unchanged(customer5_token, merchant_token):
    """From packed onward a cancellation is refused and nothing moves."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    cart = cart_with({item["skus"][0]: 1})
    order = expect(place(cart, "9000000015", "customer5@example.com", "on_delivery",
                         token=customer5_token), 201)
    pack(merchant_token, order["number"])
    with api(customer5_token) as c:
        refused = c.post(f"/api/orders/{order['number']}/cancel", json={"reason": "too late"})
    assert refused.status_code == 409 and error_code(refused) == "already_packed", (
        f"cancelling a packed order answered {refused.status_code}: {refused.text[:300]}")
    assert merchant_order(merchant_token, order["number"])["state"] == "packed"


def test_another_customer_cannot_read_or_cancel_an_order(customer_token, customer5_token, merchant_token):
    """One customer's session sees another's order as not found and cannot change it."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    cart = cart_with({item["skus"][0]: 1})
    order = expect(place(cart, "9000000015", "customer5@example.com", "prepaid",
                         token=customer5_token), 201)
    peek = order_for(customer_token, order["number"])
    assert peek.status_code == 404, f"another customer read the order: {peek.status_code}"
    with api(customer_token) as c:
        cancel = c.post(f"/api/orders/{order['number']}/cancel", json={"reason": "not mine"})
    assert cancel.status_code == 404, f"another customer's cancel answered {cancel.status_code}"
    assert merchant_order(merchant_token, order["number"])["state"] == "confirmed"


def test_a_customer_is_denied_every_merchant_route(customer_token, merchant_token):
    """Merchant endpoints refuse a customer session and leave their state untouched."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    sku = item["skus"][0]
    number = prepaid_order({sku: 1})["order"]["number"]
    with api(customer_token) as c:
        attempts = [
            c.patch(f"/api/merchant/variants/{sku}", json={"price_minor": 100}),
            c.post(f"/api/merchant/orders/{number}/transitions", json={"to": "packed", "reason": "x"}),
            c.post("/api/merchant/products", json={"handle": unique("sneak"), "title": "x",
                                                    "department": "EQUIPMENTS",
                                                    "sub_category": "massagers",
                                                    "cod_eligible": True, "variants": []}),
            c.get("/api/merchant/confirmation-queue"),
        ]
    for response in attempts:
        assert response.status_code == 403 and error_code(response) == "forbidden", (
            f"{response.request.method} {response.request.url.path} as a customer answered "
            f"{response.status_code}")
    assert merchant_variant(merchant_token, sku)["price_minor"] == 99900
    assert merchant_order(merchant_token, number)["state"] == "confirmed"


def test_tracking_returns_the_timeline_and_nothing_else(merchant_token):
    """The number and four digits reveal the progress of one order and nothing personal."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    placed = prepaid_order({item["skus"][0]: 1})
    number, phone = placed["order"]["number"], placed["phone"]
    pack(merchant_token, number)
    assert carrier(number, "shipped").status_code == 204
    found = expect(track(number, phone[-4:]), 200)
    assert set(found) == TRACK_KEYS, f"tracking answered keys {sorted(found)}"
    assert found["state"] == "shipped"
    for event in found["timeline"]:
        assert set(event) <= {"status", "occurred_at"}, event
    text = str(found)
    for secret in (phone, placed["email"], placed["order"]["address"]["line1"]):
        assert secret not in text, f"tracking revealed {secret!r}"


def test_wrong_digits_answer_exactly_as_an_unknown_order(merchant_token):
    """A wrong phone suffix is indistinguishable from a number that does not exist."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    placed = prepaid_order({item["skus"][0]: 1})
    number, phone = placed["order"]["number"], placed["phone"]
    wrong = "0000" if phone[-4:] != "0000" else "1111"
    by_digits = track(number, wrong)
    by_number = track("PF-999999", phone[-4:])
    assert by_digits.status_code == by_number.status_code == 404, (
        by_digits.status_code, by_number.status_code)
    for response in (by_digits, by_number):
        assert response.headers.get("x-request-id"), "a response carries no X-Request-Id header"
    left, right = error_of(by_digits), error_of(by_number)
    assert (left.get("code"), left.get("message")) == (right.get("code"), right.get("message")), (
        f"a wrong suffix answers {left} while an unknown number answers {right}")


def test_tracking_stops_answering_after_five_wrong_attempts(merchant_token):
    """Five wrong guesses lock the number, even against the right digits."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    placed = prepaid_order({item["skus"][0]: 1})
    number, phone = placed["order"]["number"], placed["phone"]
    wrong = "0000" if phone[-4:] != "0000" else "1111"
    for _ in range(5):
        assert track(number, wrong).status_code == 404
    locked = track(number, phone[-4:])
    assert locked.status_code == 429 and error_code(locked) == "too_many_attempts", (
        f"the right digits after five wrong guesses answered {locked.status_code}")
    assert track(number, wrong).status_code == 429


def test_a_return_refunds_what_the_line_actually_paid(customer5_token, merchant_token):
    """A returned line refunds its line total less its share of the order discount."""
    items = [new_product(merchant_token, prices=(100000,), on_hand=10) for _ in range(3)]
    cart = new_cart()
    for made in items:
        expect(add_line(cart, made["skus"][0], 1), 200)
    order = expect(place(get_cart(cart), "9000000015", "customer5@example.com", "on_delivery",
                         token=customer5_token), 201)
    deliver(merchant_token, order["number"])
    middle = order["lines"][1]
    assert middle["allocated_discount_minor"] == 6667, middle
    with api(customer5_token) as c:
        made = expect(c.post("/api/returns", json={"order_number": order["number"],
                                                    "line_ids": [middle["id"]],
                                                    "reason": "changed_mind"}), 201)
    assert made["refund_minor"] == 93333, (
        f"returning a line that paid 93,333 paise refunds {made['refund_minor']}")
    assert made["lines"] == [{"line_id": middle["id"], "refund_minor": 93333}], made["lines"]
    assert made["refund_method"] == "store_credit" and made["state"] == "return_requested", made


def test_a_return_after_seven_days_is_refused(customer5_token, merchant_token):
    """The window runs seven days from the carrier's delivery time, not from the request."""
    item = new_product(merchant_token, prices=(99900,), on_hand=10)
    lines = []
    for days in (8, 6):
        cart = cart_with({item["skus"][0]: 1})
        order = expect(place(cart, "9000000015", "customer5@example.com", "prepaid",
                             token=customer5_token), 201)
        deliver(merchant_token, order["number"], now_utc() - timedelta(days=days))
        lines.append(order)
    with api(customer5_token) as c:
        late = c.post("/api/returns", json={"order_number": lines[0]["number"],
                                             "line_ids": [lines[0]["lines"][0]["id"]],
                                             "reason": "too_large"})
        inside = c.post("/api/returns", json={"order_number": lines[1]["number"],
                                               "line_ids": [lines[1]["lines"][0]["id"]],
                                               "reason": "too_large"})
    assert late.status_code == 422 and error_code(late) == "outside_window", (
        f"a return eight days after delivery answered {late.status_code}: {late.text[:300]}")
    assert inside.status_code == 201, f"a return six days after delivery answered {inside.status_code}"
    assert inside.json()["refund_method"] == "original"


def test_a_return_before_delivery_or_with_an_unlisted_reason_is_refused(customer5_token, merchant_token):
    """Returns need a delivered order, a listed reason, no exchange on equipment, and a line not already returned."""
    item = new_product(merchant_token, prices=(99900, 99900), on_hand=10)
    cart = cart_with({item["skus"][0]: 1})
    order = expect(place(cart, "9000000015", "customer5@example.com", "prepaid",
                         token=customer5_token), 201)
    line_id = order["lines"][0]["id"]
    request = {"order_number": order["number"], "line_ids": [line_id], "reason": "damaged"}
    with api(customer5_token) as c:
        early = c.post("/api/returns", json=request)
    assert early.status_code == 422 and error_code(early) == "not_delivered", early.text[:300]
    deliver(merchant_token, order["number"])
    with api(customer5_token) as c:
        unlisted = c.post("/api/returns", json={**request, "reason": "too_expensive"})
        assert unlisted.status_code == 422 and error_code(unlisted) == "invalid_reason", unlisted.text[:300]
        swap = c.post("/api/returns", json={**request, "reason": "too_small",
                                            "exchange_sku": item["skus"][1]})
        assert swap.status_code == 422 and error_code(swap) == "exchange_not_offered", swap.text[:300]
        expect(c.post("/api/returns", json=request), 201)
        twice = c.post("/api/returns", json=request)
    assert twice.status_code == 409 and error_code(twice) == "already_returned", twice.text[:300]


def test_a_merchant_cannot_type_a_struck_through_price(merchant_token):
    """A compare price is never accepted as input, alone or beside a price change."""
    item = new_product(merchant_token, prices=(129900,), on_hand=5)
    sku = item["skus"][0]
    with api(merchant_token) as c:
        typed = c.patch(f"/api/merchant/variants/{sku}", json={"compare_at_minor": 999900})
        mixed = c.patch(f"/api/merchant/variants/{sku}",
                        json={"price_minor": 99900, "compare_at_minor": 199900})
    for response in (typed, mixed):
        assert response.status_code == 422 and error_code(response) == "compare_at_not_settable", (
            f"a typed compare price answered {response.status_code}: {response.text[:300]}")
    variant = variant_of(item["handle"], sku)
    assert variant["price_minor"] == 129900 and variant.get("compare_at_minor") is None, variant


def test_the_struck_through_price_follows_the_price_history(merchant_token):
    """The compare price is the highest recent price above the current one, and nothing else."""
    item = new_product(merchant_token, prices=(299900,), on_hand=5)
    sku = item["skus"][0]
    variant = variant_of(item["handle"], sku)
    assert variant.get("compare_at_minor") is None and variant.get("saving_percent") is None, variant
    for price, compare, saving in ((199900, 299900, 33), (249900, 299900, 16), (349900, None, None),
                                   (249900, 349900, 28)):
        set_variant(merchant_token, sku, price_minor=price)
        variant = variant_of(item["handle"], sku)
        assert (variant["price_minor"], variant.get("compare_at_minor"),
                variant.get("saving_percent")) == (price, compare, saving), (
            f"after a price of {price} the variant reads compare {variant.get('compare_at_minor')} "
            f"and saving {variant.get('saving_percent')}; expected {compare} and {saving}")
    seeded = variant_of(MASSAGE_GUN, MASSAGE_GUN_SKU)
    assert (seeded["price_minor"], seeded["compare_at_minor"], seeded["saving_percent"]) == (
        189900, 349900, 45), seeded


def test_a_low_stock_badge_counts_units_held_in_bags(merchant_token):
    """The badge reads available stock, never on hand alone, and never on backorderable stock."""
    item = new_product(merchant_token, prices=(99900,), on_hand=6, low_threshold=5)
    sku = item["skus"][0]
    assert "LOW STOCK" not in variant_of(item["handle"], sku)["badges"]
    cart_with({sku: 1})
    held = variant_of(item["handle"], sku)
    assert held["available"] == 5 and "LOW STOCK" in held["badges"], (
        f"with one unit held the variant reads {held}")
    backorder = new_product(merchant_token, prices=(99900,), on_hand=2, low_threshold=5,
                            backorderable=True)
    assert "LOW STOCK" not in variant_of(backorder["handle"], backorder["skus"][0])["badges"]
    empty = new_product(merchant_token, prices=(99900,), on_hand=0, low_threshold=5)
    badges = variant_of(empty["handle"], empty["skus"][0])["badges"]
    assert "SOLD OUT" in badges and "LOW STOCK" not in badges, badges


def test_a_code_for_a_known_phone_goes_only_to_the_email_on_file():
    """Asking for a code with someone else's email sends it to the account's own email."""
    intruder = unique_email()
    known = mail_ids(CUSTOMER4_EMAIL)
    request = request_code(CUSTOMER4_PHONE, intruder)
    assert request.status_code == 202, request.text[:300]
    arrived = wait_for_mail(CUSTOMER4_EMAIL, "Your Peakfit code", known)
    assert arrived, "no code reached the email on file"
    settle(3)
    assert mails_to(intruder) == [], "a code for a known phone was sent to the email in the request"


def test_a_code_is_single_use_and_belongs_to_its_phone():
    """A code verifies only its own phone, and only once."""
    first_phone, first_email = unique_phone(), unique_email()
    second_phone, second_email = unique_phone(), unique_email()
    first_code = fresh_code(first_phone, first_email)
    fresh_code(second_phone, second_email)
    with api() as c:
        crossed = c.post("/api/auth/verify", json={"phone": second_phone, "code": first_code})
        assert crossed.status_code == 401 and error_code(crossed) == "invalid_code", (
            f"another phone's code verified: {crossed.status_code}")
        expect(c.post("/api/auth/verify", json={"phone": first_phone, "code": first_code}), 200)
        reused = c.post("/api/auth/verify", json={"phone": first_phone, "code": first_code})
    assert reused.status_code == 401 and error_code(reused) == "invalid_code", (
        f"a used code verified again: {reused.status_code}")
    third_phone, third_email = unique_phone(), unique_email()
    third_code = fresh_code(third_phone, third_email)
    wrong = "111111" if third_code != "111111" else "222222"
    with api() as c:
        for _ in range(5):
            assert c.post("/api/auth/verify", json={"phone": third_phone, "code": wrong}).status_code == 401
        voided = c.post("/api/auth/verify", json={"phone": third_phone, "code": third_code})
    assert voided.status_code == 401 and error_code(voided) == "invalid_code", (
        f"the right code after five wrong ones answered {voided.status_code}")


def test_a_second_code_request_inside_thirty_seconds_is_refused():
    """Codes cannot be requested faster than one every thirty seconds per phone."""
    phone, email = unique_phone(), unique_email()
    assert request_code(phone, email).status_code == 202
    again = request_code(phone, email)
    assert again.status_code == 429 and error_code(again) == "resend_too_soon", again.text[:300]
    retry = body_of(again).get("error", {}).get("retry_after_seconds")
    assert isinstance(retry, int) and 1 <= retry <= 30, f"retry_after_seconds is {retry!r}"


def test_a_guest_bag_merges_into_the_account_bag_by_summing(merchant_token):
    """Claiming a guest bag adds its quantities to the account's bag rather than replacing it."""
    shoe = new_product(merchant_token, prices=(99900,), on_hand=10)
    tee = new_product(merchant_token, prices=(49900,), on_hand=10)
    token = sign_in(unique_phone(), unique_email())
    with api(token) as c:
        mine = expect(c.get("/api/account/cart"), 200)
    expect(add_line(mine["token"], shoe["skus"][0], 1), 200)
    guest = new_cart()
    expect(add_line(guest, shoe["skus"][0], 2), 200)
    expect(add_line(guest, tee["skus"][0], 1), 200)
    with api(token) as c:
        merged = expect(c.post(f"/api/carts/{guest}/claim"), 200)
    quantities = {line["sku"]: line["quantity"] for line in merged["lines"]}
    assert quantities == {shoe["skus"][0]: 3, tee["skus"][0]: 1}, (
        f"the merged bag holds {quantities}; quantities are summed, never replaced")


def test_two_delivered_orders_are_confirmed_at_once(customer_token, merchant_token):
    """A phone with two delivered orders gets the high band and is confirmed immediately."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    cart = cart_with({item["skus"][0]: 1})
    order = expect(place(cart, "9000000011", "customer@example.com", "on_delivery",
                         token=customer_token), 201)
    assert order["state"] == "confirmed", f"a high band order is {order['state']}"
    assert merchant_order(merchant_token, order["number"])["band"] == "high"


def test_postal_history_alone_never_puts_a_first_order_below_medium(merchant_token):
    """A first order in a high refusal postal code is medium and asked to confirm."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    placed = guest_cod_order({item["skus"][0]: 1}, POSTAL_HIGH_REFUSAL)
    order = placed["order"]
    assert order["state"] == "placed", order["state"]
    assert merchant_order(merchant_token, order["number"])["band"] == "medium", (
        "postal refusal statistics alone lowered a first order below medium")
    message = wait_for_mail(placed["email"], f"Please confirm Peakfit order {order['number']}", set())
    assert message, "a medium band order was not asked to confirm"
    assert len(first_line(message["text"])) < 160


def test_a_blocked_band_refuses_cash_on_delivery_but_takes_prepaid(merchant_token):
    """Two refusals in a year block payment on delivery for that phone; prepaid is still offered."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    cart = cart_with({item["skus"][0]: 1})
    code = fresh_code(CUSTOMER3_PHONE, unique_email(), inbox=CUSTOMER3_EMAIL)
    blocked = place(cart, CUSTOMER3_PHONE, CUSTOMER3_EMAIL, "on_delivery", code=code)
    assert blocked.status_code == 422 and error_code(blocked) == "cod_unavailable", blocked.text[:300]
    assert error_of(blocked).get("reason") == "delivery_confidence", error_of(blocked)
    expect(place(cart, CUSTOMER3_PHONE, CUSTOMER3_EMAIL, "prepaid"), 201)


def test_a_low_band_order_cannot_be_packed_before_confirmation(merchant_token):
    """One refusal puts an order in the low band, and packing waits for confirmation."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    cart = cart_with({item["skus"][0]: 1})
    code = fresh_code(CUSTOMER2_PHONE, unique_email(), inbox=CUSTOMER2_EMAIL)
    order = expect(place(cart, CUSTOMER2_PHONE, CUSTOMER2_EMAIL, "on_delivery", code=code), 201)
    assert merchant_order(merchant_token, order["number"])["band"] == "low"
    early = transition(merchant_token, order["number"], "packed")
    assert early.status_code == 409 and error_code(early) == "confirmation_required", early.text[:300]
    expect(transition(merchant_token, order["number"], "confirmed"), 200)
    expect(transition(merchant_token, order["number"], "packed"), 200)


def test_no_confidence_score_reaches_a_customer_or_the_merchant(merchant_token):
    """Customers see no band and no signal; the merchant sees band and signals but never a score."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    placed = guest_cod_order({item["skus"][0]: 1}, POSTAL_HIGH_REFUSAL)
    order = placed["order"]
    for name in ("score", "band", "signals"):
        assert keys_named(order, name) == [], f"the customer's order carries {name!r}"
    view = merchant_order(merchant_token, order["number"])
    assert view["band"] == "medium" and isinstance(view["signals"], list) and view["signals"], view
    with api(merchant_token) as c:
        queue = expect(c.get("/api/merchant/confirmation-queue"), 200)
    assert order["number"] in [i.get("number") for i in queue.get("items", [])]
    assert keys_named(view, "score") == [] and keys_named(queue, "score") == [], (
        "a numeric confidence score reached the merchant")


def test_a_review_needs_a_delivered_order_of_that_product(customer5_token, merchant_token):
    """Only a delivered order of the product lets a customer review it, once."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    sku = item["skus"][0]
    review = {"sku": sku, "rating": 4, "body": "solid and quiet"}
    with api(customer5_token) as c:
        stranger = c.post(f"/api/products/{item['handle']}/reviews", json=review)
    assert stranger.status_code == 403 and error_code(stranger) == "not_eligible", stranger.text[:300]
    cart = cart_with({sku: 1})
    order = expect(place(cart, "9000000015", "customer5@example.com", "prepaid",
                         token=customer5_token), 201)
    with api(customer5_token) as c:
        undelivered = c.post(f"/api/products/{item['handle']}/reviews", json=review)
    assert undelivered.status_code == 403, f"a review before delivery answered {undelivered.status_code}"
    deliver(merchant_token, order["number"])
    with api(customer5_token) as c:
        made = expect(c.post(f"/api/products/{item['handle']}/reviews", json=review), 201)
        twice = c.post(f"/api/products/{item['handle']}/reviews", json=review)
    assert made["state"] == "held" and made["verified_purchase"] is True, made
    assert twice.status_code == 409 and error_code(twice) == "already_reviewed", twice.text[:300]


def test_ratings_count_published_reviews_only(customer5_token, merchant_token):
    """A held review changes no rating; publishing it does."""
    item = new_product(merchant_token, prices=(99900,), on_hand=5)
    sku = item["skus"][0]
    cart = cart_with({sku: 1})
    order = expect(place(cart, "9000000015", "customer5@example.com", "prepaid",
                         token=customer5_token), 201)
    deliver(merchant_token, order["number"])
    with api(customer5_token) as c:
        made = expect(c.post(f"/api/products/{item['handle']}/reviews",
                             json={"sku": sku, "rating": 3, "body": "fits as described"}), 201)
    held = product(item["handle"])
    assert held["review_count"] == 0, f"a held review counted: {held['review_count']}"
    with api(merchant_token) as c:
        expect(c.post(f"/api/merchant/reviews/{made['id']}/publish"), 200)
    published = product(item["handle"])
    assert published["review_count"] == 1 and float(published["rating_average"]) == 3.0, published


def test_filters_and_price_sort_apply_before_paging(merchant_token):
    """Filtering happens before paging: full pages of matches, in price order, counted exactly."""
    handles, expected = [], []
    for index in range(60):
        deep = index % 2 == 0
        high = (400000 if deep else 200000) + index * 1000
        low = high * 45 // 100 if deep else high * 80 // 100
        made = new_product(merchant_token, prices=(high,), on_hand=5)
        set_variant(merchant_token, made["skus"][0], price_minor=low)
        handles.append(made["handle"])
        if deep:
            expected.append((low, made["handle"]))
    collection = unique("deep-discounts")
    with api(merchant_token) as c:
        expect(c.post("/api/merchant/collections", json={"handle": collection, "title": collection,
                                                          "product_handles": handles}), 201)
    items, sizes, count = walk_products({"collection": collection, "discount": 50,
                                         "sort": "price_asc"})
    assert count == 30, f"count is {count} for 30 matching products"
    assert sizes[0] == PAGE_SIZE and sum(sizes) == 30, (
        f"pages held {sizes}; filters apply before paging, so the first page is full")
    got = [(i["price_minor"], i["handle"]) for i in items]
    assert got == sorted(expected), "the filtered walk is not in price order, then handle"
    assert all(i["saving_percent"] >= 50 for i in items), [i["saving_percent"] for i in items]


def test_out_of_stock_products_stay_listed(merchant_token):
    """A sold out product stays in its collection unless in stock only is asked for."""
    live = [new_product(merchant_token, prices=(99900,), on_hand=5) for _ in range(2)]
    gone = new_product(merchant_token, prices=(99900,), on_hand=0)
    collection = unique("mixed-stock")
    with api(merchant_token) as c:
        expect(c.post("/api/merchant/collections", json={
            "handle": collection, "title": collection,
            "product_handles": [p["handle"] for p in live] + [gone["handle"]]}), 201)
    everything, _, count = walk_products({"collection": collection})
    assert count == 3 and len(everything) == 3, f"{count} listed, expected all three"
    sold_out = next(i for i in everything if i["handle"] == gone["handle"])
    assert sold_out["in_stock"] is False, sold_out
    stocked, _, stocked_count = walk_products({"collection": collection, "in_stock": "true"})
    assert stocked_count == 2 and gone["handle"] not in [i["handle"] for i in stocked]


def test_an_unknown_address_renders_the_not_found_page(page):
    """An unmatched path is Peakfit's own not-found page, with search and best sellers, answering 404."""
    raw = httpx.get(f"{app_url()}/no-such-peakfit-page", timeout=30.0, follow_redirects=False)
    assert raw.status_code == 404, f"an unknown address answered {raw.status_code}"
    page.goto("/no-such-peakfit-page")
    page.get_by_text(NOT_FOUND_COPY, exact=True).wait_for()
    assert page.get_by_role("searchbox").or_(page.get_by_role("textbox")).count() >= 1, (
        "the not-found page carries no search field")
    assert "/no-such-peakfit-page" in page.url, "the not-found page redirected away"


def test_the_privacy_page_is_linked_from_every_footer(page):
    """Every page's footer links the privacy page, and the page says what is recorded."""
    for route in PUBLIC_ROUTES:
        page.goto(route)
        footer = page.get_by_role("contentinfo")
        footer.wait_for()
        assert footer.locator("a[href$='/pages/privacy']").count() >= 1, (
            f"the footer on {route} does not link the privacy page")
    page.goto("/pages/privacy")
    page.get_by_role("heading").first.wait_for()
    text = page.inner_text("body").lower()
    for recorded in ("phone", "email", "address", "order"):
        assert recorded in text, f"the privacy page does not mention {recorded}"


def test_every_content_image_carries_alternative_text(page):
    """No rendered image lacks an alt attribute, and product imagery is named."""
    for route in ("/", f"/products/{MASSAGE_GUN}"):
        page.goto(route)
        page.wait_for_load_state("networkidle")
        missing = page.eval_on_selector_all("img", "els => els.filter(e => !e.hasAttribute('alt')).length")
        assert missing == 0, f"{route} renders {missing} image(s) with no alt attribute"
    named = page.eval_on_selector_all("img", "els => els.filter(e => (e.getAttribute('alt') || '').trim()).length")
    assert named >= 1, "the product page names none of its images"


def test_every_public_route_declares_its_own_social_preview():
    """Each public route's served HTML carries its own preview title and a resolving image."""
    titles = set()
    for route in PUBLIC_ROUTES:
        html = httpx.get(f"{app_url()}{route}", timeout=30.0).text
        tags = {}
        for tag in re.findall(r"<meta\b[^>]*>", html, re.I):
            attrs = {k.lower(): v for k, _, v in re.findall(r'([\w:-]+)\s*=\s*(["\'])(.*?)\2', tag)}
            if attrs.get("property", "").lower() in ("og:title", "og:image") and attrs.get("content"):
                tags.setdefault(attrs["property"].lower(), attrs["content"])
        assert "og:title" in tags and "og:image" in tags, (
            f"{route} declares no social preview in its served HTML")
        titles.add(tags["og:title"])
        src = tags["og:image"]
        target = src if src.startswith("http") else f"{app_url()}{src}"
        assert target.startswith(app_url()), f"{route} names a preview image off its own origin"
        assert httpx.get(target, timeout=30.0).status_code == 200, f"{route} preview image does not resolve"
    assert len(titles) == len(PUBLIC_ROUTES), "two public routes share a preview title"


def test_no_credential_reaches_the_browser():
    """No secret, database address or provider credential is in anything the browser downloads."""
    home = httpx.get(f"{app_url()}/", timeout=30.0).text
    assets = sorted(set(re.findall(r'(?:src|href)=["\'](/[^"\']+\.(?:js|css))["\']', home)))
    assert assets, "the home page loads no script or style of its own"
    blob = home
    for asset in assets[:20]:
        response = httpx.get(f"{app_url()}{asset}", timeout=30.0)
        assert response.status_code == 200, f"{asset} answered {response.status_code}"
        blob += response.text
    for secret in APP_SECRETS:
        assert secret not in blob, f"{secret!r} reached the browser"


def test_a_price_block_reads_as_one_sentence(page):
    """The price block's accessible name relates the three numbers in one sentence."""
    page.goto(f"/products/{MASSAGE_GUN}")
    block = page.get_by_label(PRICE_SENTENCE, exact=True)
    block.first.wait_for()
    assert block.count() >= 1, f"no price block is named {PRICE_SENTENCE!r}"


def body_of(response: httpx.Response) -> dict:
    return response.json() if "json" in response.headers.get("content-type", "") else {}
