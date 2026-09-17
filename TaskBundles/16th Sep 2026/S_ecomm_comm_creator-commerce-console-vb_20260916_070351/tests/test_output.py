"""The one pytest module for deku/creator-commerce-console-vb.

Black box throughout: every assertion runs over HTTP against the deployed app or
over a capability fixture against a real backing service. Nothing here imports,
reads or inspects the agent's source, and nothing assumes a framework, a file
layout, an ORM, an id format or a response envelope the brief did not pin.
"""

from __future__ import annotations

import threading

import httpx
from appclient import app_url

from conftest import (
    ABSENT_STATUSES,
    ACCOUNT_HANDLE,
    CREATOR_EMAIL,
    CREATOR_NAME,
    PAYOUT_CURRENCY,
    READER2_NAME,
    READER_NAME,
    ACCOUNT_CREATOR_PAYABLE,
    ACCOUNT_PAYMENT_EXPENSE,
    ACCOUNT_PLATFORM_REVENUE,
    ACCOUNT_RECEIVABLE,
    ACCOUNT_TAX_PAYABLE,
    CHANNEL_DIRECT,
    CHANNEL_MARKETPLACE,
    CLOSED_CODE,
    CORPUS_PASSWORD,
    CREATOR_ONLY_ROUTES,
    DECOY_FIELD,
    DENIED_STATUSES,
    DIRECTION_CREDIT,
    DIRECTION_DEBIT,
    DIRECT_FIXED_MINOR,
    DIRECT_RATE_BPS,
    FIELD_NOTES,
    FIELD_NOTES_NAME,
    FIELD_NOTES_STANDARD_MINOR,
    JURISDICTION_TAXED,
    JURISDICTION_ZERO,
    LANTERN_KIT,
    MARKETPLACE_FIXED_MINOR,
    MARKETPLACE_NET_MINOR,
    MARKETPLACE_PLATFORM_FEE_MINOR,
    MARKETPLACE_RATE_BPS,
    MOR_ENTITY,
    OK_STATUSES,
    OPEN_CODE,
    OPEN_CODE_BPS,
    ORDER_NUMBER_PREFIX,
    READER2_EMAIL,
    READER2_EXTERNAL_KEY,
    READER_EMAIL,
    READER_EXTERNAL_KEY,
    RECEIPT_SUBJECT_PREFIX,
    REFUSED_STATUSES,
    SEEDED_ACCOUNT_CODES,
    TAXED_RATE_BPS,
    TIDE_TABLES,
    TIER_STANDARD,
    TOKEN_KEY,
    WORKED_DISCOUNT_MINOR,
    WORKED_INVOICE_DECIMAL,
    WORKED_NET_MINOR,
    WORKED_PAYMENT_FEE_MINOR,
    WORKED_PLATFORM_FEE_MINOR,
    WORKED_SUBTOTAL_MINOR,
    WORKED_TAX_MINOR,
    WORKED_TOTAL_MINOR,
    ZERO_RATE_BPS,
    as_list,
    body_excerpt,
    buy_once,
    confirm_session,
    expected_decomposition,
    find_by,
    fresh_client,
    minor,
    open_session,
    order_number_of,
    probe_email,
    probe_key,
    probe_permalink,
    session_id_of,
    settle,
    wait_for_email,
    wait_for_invoice,
    where,
)


def test_checkout_confirm_creates_order_with_worked_decomposition(reader_client, store):
    confirmed = buy_once(reader_client, FIELD_NOTES, channel=CHANNEL_DIRECT,
                         code=OPEN_CODE)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, "confirming the worked-case purchase")
    number = order_number_of(confirmed.json())
    assert number.startswith(ORDER_NUMBER_PREFIX), (
        f"the confirm response carried the order number {number!r}, which does "
        f"not begin with {ORDER_NUMBER_PREFIX!r}: {body_excerpt(confirmed)!r}")

    order = store.order_by_number(number)
    assert order is not None, (
        f"order {number} is absent from the orders table after a confirm that "
        f"answered {confirmed.status_code}")

    want = expected_decomposition(
        FIELD_NOTES_STANDARD_MINOR, 1, OPEN_CODE_BPS, TAXED_RATE_BPS,
        DIRECT_RATE_BPS, DIRECT_FIXED_MINOR)
    assert want["subtotal_minor"] == WORKED_SUBTOTAL_MINOR
    assert want["total_minor"] == WORKED_TOTAL_MINOR
    assert want["net_minor"] == WORKED_NET_MINOR

    for field, expected in want.items():
        assert int(order.get(field, -1)) == expected, (
            f"order {number} carries {field}={order.get(field)!r} where the "
            f"brief's arithmetic gives {expected}; the stored decomposition is "
            f"{ {k: order.get(k) for k in want} }")

    assert (int(order["net_minor"]) ==
            int(order["subtotal_minor"]) - int(order["discount_minor"])
            - int(order["platform_fee_minor"]) - int(order["payment_fee_minor"])
            - int(order["affiliate_fee_minor"])), (
        f"order {number} breaks the net identity: {order!r}")


def test_paid_order_grants_one_entitlement(reader_client, store):
    confirmed = buy_once(reader_client, FIELD_NOTES)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, "confirming a purchase to grant an entitlement")
    number = order_number_of(confirmed.json())
    order = store.order_by_number(number)
    assert order is not None, f"order {number} is absent from the orders table"

    granted = store.entitlements_for_order(order.get("id"))
    assert len(granted) == 1, (
        f"order {number} granted {len(granted)} entitlement rows where the brief "
        f"pins exactly one: {granted!r}")

    listed = reader_client.get("/library")
    assert listed.status_code in OK_STATUSES, where(listed, "reading the library")
    held = as_list(listed.json())
    assert held, (
        f"the library for the buying reader is empty after order {number} was "
        f"confirmed: {body_excerpt(listed)!r}")


def test_entitlement_access_is_recorded(reader_client, store):
    confirmed = buy_once(reader_client, FIELD_NOTES)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, "confirming a purchase before opening the entitlement")
    number = order_number_of(confirmed.json())
    order = store.order_by_number(number)
    assert order is not None, f"order {number} is absent from the orders table"
    granted = store.entitlements_for_order(order.get("id"))
    assert granted, f"order {number} granted no entitlement row"
    entitlement_id = granted[0].get("public_id") or granted[0].get("id")

    before = len(store.access_events(granted[0].get("id")))
    opened = reader_client.post(f"/library/entitlements/{entitlement_id}/access",
                                json={})
    assert opened.status_code in OK_STATUSES, where(
        opened, f"opening entitlement {entitlement_id}")

    after = len(store.access_events(granted[0].get("id")))
    assert after == before + 1, (
        f"opening entitlement {entitlement_id} moved the access-event count from "
        f"{before} to {after}, where the brief records exactly one access")


def test_checkout_session_price_survives_a_reprice(reader_client, creator_client):
    opened = open_session(reader_client, FIELD_NOTES)
    assert opened.status_code in OK_STATUSES, where(
        opened, "opening a session before the reprice")
    session_id = session_id_of(opened.json())
    locked = minor(opened.json().get("total_minor")
                   or opened.json().get("totals", {}).get("total", 0))

    bumped = creator_client.patch(f"/products/{FIELD_NOTES}", json={
        "tiers": [{"code": TIER_STANDARD,
                   "price_minor": FIELD_NOTES_STANDARD_MINOR + 500}]})
    assert bumped.status_code in OK_STATUSES + REFUSED_STATUSES, where(
        bumped, "repricing the tier while a session is open")

    read_back = reader_client.get(f"/checkout/sessions/{session_id}")
    assert read_back.status_code in OK_STATUSES, where(
        read_back, f"re-reading session {session_id} after the reprice")
    still = minor(read_back.json().get("total_minor")
                  or read_back.json().get("totals", {}).get("total", 0))
    assert still == locked, (
        f"session {session_id} locked a total of {locked} minor units at open "
        f"but reads {still} after the tier was repriced")


def test_discount_retaxes_the_discounted_base(reader_client):
    opened = open_session(reader_client, FIELD_NOTES)
    assert opened.status_code in OK_STATUSES, where(
        opened, "opening a session before applying a discount")
    session_id = session_id_of(opened.json())

    applied = reader_client.post(f"/checkout/sessions/{session_id}/discounts",
                                 json={"code": OPEN_CODE.lower()})
    assert applied.status_code in OK_STATUSES, where(
        applied, f"applying {OPEN_CODE} in lower case")
    body = applied.json()
    assert minor(body.get("discount_minor", 0)) == WORKED_DISCOUNT_MINOR, (
        f"applying {OPEN_CODE} gave a discount of {body.get('discount_minor')!r} "
        f"where the brief pins {WORKED_DISCOUNT_MINOR}: {body_excerpt(applied)!r}")
    assert minor(body.get("tax_minor", 0)) == WORKED_TAX_MINOR, (
        f"applying {OPEN_CODE} left a tax of {body.get('tax_minor')!r} where the "
        f"brief re-resolves it on the discounted base to {WORKED_TAX_MINOR}: "
        f"{body_excerpt(applied)!r}")
    assert minor(body.get("total_minor", 0)) == WORKED_TOTAL_MINOR, (
        f"applying {OPEN_CODE} left a total of {body.get('total_minor')!r} where "
        f"the brief pins {WORKED_TOTAL_MINOR}: {body_excerpt(applied)!r}")


def test_pricing_read_matches_the_order_arithmetic(creator_client, reader_client, store):
    priced = creator_client.get(f"/pricing/{FIELD_NOTES}", params={
        "tier_code": TIER_STANDARD,
        "discount_bps": OPEN_CODE_BPS,
        "attribution_channel": CHANNEL_DIRECT,
        "tax_jurisdiction": JURISDICTION_TAXED,
    })
    assert priced.status_code in OK_STATUSES, where(
        priced, f"reading the pricing decomposition for {FIELD_NOTES}")
    figures = priced.json()

    confirmed = buy_once(reader_client, FIELD_NOTES, channel=CHANNEL_DIRECT,
                         code=OPEN_CODE)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, "confirming the order the pricing read must agree with")
    order = store.order_by_number(order_number_of(confirmed.json()))
    assert order is not None, "the order the pricing read must agree with is absent"

    for field in ("subtotal_minor", "discount_minor", "tax_minor", "total_minor",
                  "platform_fee_minor", "payment_fee_minor", "net_minor"):
        assert minor(figures.get(field, -1)) == int(order.get(field, -2)), (
            f"the pricing read gives {field}={figures.get(field)!r} while the "
            f"order it describes carries {order.get(field)!r}; the two must agree "
            f"to the minor unit")


def test_marketplace_channel_raises_the_platform_fee(creator_client):
    params = {
        "tier_code": TIER_STANDARD,
        "discount_bps": OPEN_CODE_BPS,
        "tax_jurisdiction": JURISDICTION_TAXED,
    }
    direct = creator_client.get(f"/pricing/{FIELD_NOTES}", params={
        **params, "attribution_channel": CHANNEL_DIRECT})
    assert direct.status_code in OK_STATUSES, where(
        direct, "reading the direct-channel pricing decomposition")
    marketplace = creator_client.get(f"/pricing/{FIELD_NOTES}", params={
        **params, "attribution_channel": CHANNEL_MARKETPLACE})
    assert marketplace.status_code in OK_STATUSES, where(
        marketplace, "reading the marketplace-channel pricing decomposition")

    want_direct = expected_decomposition(
        FIELD_NOTES_STANDARD_MINOR, 1, OPEN_CODE_BPS, TAXED_RATE_BPS,
        DIRECT_RATE_BPS, DIRECT_FIXED_MINOR)
    want_market = expected_decomposition(
        FIELD_NOTES_STANDARD_MINOR, 1, OPEN_CODE_BPS, TAXED_RATE_BPS,
        MARKETPLACE_RATE_BPS, MARKETPLACE_FIXED_MINOR)
    assert want_direct["platform_fee_minor"] == WORKED_PLATFORM_FEE_MINOR
    assert want_market["platform_fee_minor"] == MARKETPLACE_PLATFORM_FEE_MINOR
    assert want_market["net_minor"] == MARKETPLACE_NET_MINOR

    assert minor(marketplace.json().get("platform_fee_minor", -1)) == \
        MARKETPLACE_PLATFORM_FEE_MINOR, (
        f"the marketplace channel gave a platform fee of "
        f"{marketplace.json().get('platform_fee_minor')!r} where the brief pins "
        f"{MARKETPLACE_PLATFORM_FEE_MINOR}: {body_excerpt(marketplace)!r}")
    assert minor(marketplace.json().get("net_minor", -1)) == MARKETPLACE_NET_MINOR, (
        f"the marketplace channel gave a net of "
        f"{marketplace.json().get('net_minor')!r} where the brief pins "
        f"{MARKETPLACE_NET_MINOR}: {body_excerpt(marketplace)!r}")
    assert minor(direct.json().get("net_minor", -1)) > \
        minor(marketplace.json().get("net_minor", -1)), (
        "moving the attribution channel to marketplace must lower the net, but "
        f"direct gave {direct.json().get('net_minor')!r} and marketplace gave "
        f"{marketplace.json().get('net_minor')!r}")


def test_unpublish_keeps_an_existing_entitlement(reader_client, creator_client, store):
    permalink = probe_permalink()
    created = creator_client.post("/products", json={
        "name": "Probe Ledger Notes", "permalink": permalink})
    assert created.status_code in OK_STATUSES, where(
        created, f"raising the probe product {permalink}")
    tiered = creator_client.post(f"/products/{permalink}/tiers", json={
        "code": TIER_STANDARD, "name": "Standard",
        "price_minor": FIELD_NOTES_STANDARD_MINOR})
    assert tiered.status_code in OK_STATUSES, where(
        tiered, f"adding the base tier to {permalink}")
    published = creator_client.post(f"/products/{permalink}/publish", json={})
    assert published.status_code in OK_STATUSES, where(
        published, f"publishing {permalink}")

    confirmed = buy_once(reader_client, permalink)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, f"buying {permalink} before it is withdrawn")
    order = store.order_by_number(order_number_of(confirmed.json()))
    assert order is not None, f"the order for {permalink} is absent"
    before = store.entitlements_for_order(order.get("id"))
    assert before, f"buying {permalink} granted no entitlement"

    withdrawn = creator_client.post(f"/products/{permalink}/unpublish", json={})
    assert withdrawn.status_code in OK_STATUSES, where(
        withdrawn, f"unpublishing {permalink}")

    after = store.entitlements_for_order(order.get("id"))
    assert len(after) == len(before), (
        f"unpublishing {permalink} changed the entitlement count from "
        f"{len(before)} to {len(after)}")
    assert all(row.get("state") != "revoked" for row in after), (
        f"unpublishing {permalink} revoked an entitlement already granted: "
        f"{after!r}")

    listed = reader_client.get("/library")
    assert listed.status_code in OK_STATUSES, where(
        listed, "reading the library after the product was withdrawn")


def test_permalink_is_fixed_after_the_first_paid_order(reader_client, creator_client):
    permalink = probe_permalink()
    created = creator_client.post("/products", json={
        "name": "Probe Tide Charts", "permalink": permalink})
    assert created.status_code in OK_STATUSES, where(
        created, f"raising the probe product {permalink}")
    tiered = creator_client.post(f"/products/{permalink}/tiers", json={
        "code": TIER_STANDARD, "name": "Standard",
        "price_minor": FIELD_NOTES_STANDARD_MINOR})
    assert tiered.status_code in OK_STATUSES, where(
        tiered, f"adding the base tier to {permalink}")
    assert creator_client.post(f"/products/{permalink}/publish",
                               json={}).status_code in OK_STATUSES

    early = probe_permalink()
    renamed = creator_client.patch(f"/products/{permalink}",
                                   json={"permalink": early})
    assert renamed.status_code in OK_STATUSES, where(
        renamed, "renaming a permalink before the first paid order")

    confirmed = buy_once(reader_client, early)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, f"buying {early} to fix its permalink")

    late = creator_client.patch(f"/products/{early}",
                                json={"permalink": probe_permalink()})
    assert late.status_code in REFUSED_STATUSES, (
        f"renaming {early} after its first paid order answered "
        f"{late.status_code}, where the brief fixes the permalink: "
        f"{body_excerpt(late)!r}")


def test_paid_order_ledger_postings_are_stored_and_balance(reader_client, store):
    confirmed = buy_once(reader_client, FIELD_NOTES, channel=CHANNEL_DIRECT,
                         code=OPEN_CODE)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, "confirming the purchase whose entry must balance")
    number = order_number_of(confirmed.json())
    order = store.order_by_number(number)
    assert order is not None, f"order {number} is absent from the orders table"

    entries = store.ledger_entries_for_source(order.get("id"))
    assert len(entries) == 1, (
        f"order {number} produced {len(entries)} ledger entries where the brief "
        f"pins exactly one: {entries!r}")
    legs = store.postings_for(entries[0].get("id"))
    assert legs, f"the ledger entry for order {number} carries no postings"

    debits = sum(int(row["amount_minor"]) for row in legs
                 if row.get("direction") == DIRECTION_DEBIT)
    credits = sum(int(row["amount_minor"]) for row in legs
                  if row.get("direction") == DIRECTION_CREDIT)
    assert debits == credits, (
        f"the entry for order {number} carries {debits} in debits against "
        f"{credits} in credits: {legs!r}")
    assert debits == int(order["total_minor"]), (
        f"the entry for order {number} debits {debits} where the order total is "
        f"{order['total_minor']}")
    assert all(int(row["amount_minor"]) > 0 for row in legs), (
        f"the entry for order {number} carries a leg worth nothing: {legs!r}")

    by_code = store.legs_by_account_code(entries[0].get("id"))
    receivable = by_code.get(ACCOUNT_RECEIVABLE, [])
    assert receivable, (
        f"the entry for order {number} posts nothing to {ACCOUNT_RECEIVABLE}; "
        f"the codes it touches are {sorted(by_code)}")
    assert all(row.get("direction") == DIRECTION_DEBIT for row in receivable), (
        f"the entry for order {number} does not debit {ACCOUNT_RECEIVABLE}: "
        f"{receivable!r}")
    for code in (ACCOUNT_CREATOR_PAYABLE, ACCOUNT_PLATFORM_REVENUE,
                 ACCOUNT_PAYMENT_EXPENSE, ACCOUNT_TAX_PAYABLE):
        legs_here = by_code.get(code, [])
        assert all(row.get("direction") == DIRECTION_CREDIT for row in legs_here), (
            f"the entry for order {number} does not credit {code}: {legs_here!r}")
    assert sum(int(row["amount_minor"]) for row in
               by_code.get(ACCOUNT_CREATOR_PAYABLE, [])) == int(order["net_minor"]), (
        f"the entry for order {number} credits {ACCOUNT_CREATOR_PAYABLE} with an "
        f"amount other than the order net of {order['net_minor']}: "
        f"{by_code.get(ACCOUNT_CREATOR_PAYABLE)!r}")


def test_trial_balance_is_zero_after_purchase(reader_client, creator_client, store):
    confirmed = buy_once(reader_client, FIELD_NOTES)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, "confirming the purchase before reading the trial balance")

    assert store.trial_balance_minor() == 0, (
        f"the stored postings net to {store.trial_balance_minor()} minor units "
        f"where the brief pins exactly zero")

    read = creator_client.get("/ledger/trial-balance")
    assert read.status_code in OK_STATUSES, where(read, "reading the trial balance")
    flat = str(read.json())
    assert "0" in flat, (
        f"the trial-balance response carries no zero figure: {body_excerpt(read)!r}")


def test_seeded_chart_of_accounts_rows_exist(store, creator_client):
    rows = store.ledger_accounts()
    codes = {str(row.get("code")) for row in rows}
    for code in SEEDED_ACCOUNT_CODES:
        assert code in codes, (
            f"the seeded chart of accounts is missing code {code}; the stored "
            f"codes are {sorted(codes)}")

    tax_rows = [row for row in rows if str(row.get("code")) == ACCOUNT_TAX_PAYABLE]
    jurisdictions = {row.get("jurisdiction") for row in tax_rows}
    assert JURISDICTION_TAXED in jurisdictions, (
        f"the tax payable account carries no row for {JURISDICTION_TAXED}: "
        f"{tax_rows!r}")
    assert JURISDICTION_ZERO in jurisdictions, (
        f"the tax payable account carries no row for {JURISDICTION_ZERO}: "
        f"{tax_rows!r}")

    listed = creator_client.get("/ledger/accounts")
    assert listed.status_code in OK_STATUSES, where(
        listed, "reading the chart of accounts")
    served = str(listed.json())
    for code in (ACCOUNT_RECEIVABLE, ACCOUNT_CREATOR_PAYABLE,
                 ACCOUNT_PLATFORM_REVENUE, ACCOUNT_PAYMENT_EXPENSE):
        assert code in served, (
            f"the served chart of accounts omits {code}: {body_excerpt(listed)!r}")


def test_repeated_checkout_confirm_is_idempotent(reader_client, store, inbox,
                                                 payments):
    opened = open_session(reader_client, FIELD_NOTES)
    assert opened.status_code in OK_STATUSES, where(
        opened, "opening the session that will be confirmed twice")
    session_id = session_id_of(opened.json())
    key = probe_key()

    first = confirm_session(reader_client, session_id, key=key)
    assert first.status_code in OK_STATUSES, where(first, "the first confirm")
    number = order_number_of(first.json())
    assert number, f"the first confirm returned no order number: {body_excerpt(first)!r}"

    second = confirm_session(reader_client, session_id, key=key)
    assert second.status_code in OK_STATUSES + REFUSED_STATUSES, where(
        second, "the replayed confirm")
    settle()

    assert store.count_orders_by_key(key) == 1, (
        f"replaying the confirm with key {key} left "
        f"{store.count_orders_by_key(key)} orders where the brief pins one")
    order = store.order_by_number(number)
    assert order is not None, f"order {number} is absent after the replay"
    assert len(store.entitlements_for_order(order.get("id"))) == 1, (
        f"replaying the confirm left "
        f"{len(store.entitlements_for_order(order.get('id')))} entitlements for "
        f"order {number}")
    assert len(store.ledger_entries_for_source(order.get("id"))) == 1, (
        f"replaying the confirm left "
        f"{len(store.ledger_entries_for_source(order.get('id')))} ledger entries "
        f"for order {number}")

    invoices = [row for row in store.all_invoices()
                if row.get("order_id") == order.get("id")]
    assert len(invoices) == 1, (
        f"replaying the confirm left {len(invoices)} invoice rows for order "
        f"{number}: {invoices!r}")


def test_billing_account_external_key_is_stored_once(reader_client, reader2_client,
                                                     store, payments):
    assert buy_once(reader_client, FIELD_NOTES).status_code in OK_STATUSES
    assert buy_once(reader_client, FIELD_NOTES).status_code in OK_STATUSES
    settle()

    assert store.count_billing_accounts(READER_EXTERNAL_KEY) == 1, (
        f"two purchases by the same reader left "
        f"{store.count_billing_accounts(READER_EXTERNAL_KEY)} billing accounts "
        f"under the external key {READER_EXTERNAL_KEY}, where the brief pins one")

    assert buy_once(reader2_client, FIELD_NOTES).status_code in OK_STATUSES
    settle()
    assert store.count_billing_accounts(READER2_EXTERNAL_KEY) == 1, (
        f"the second reader has "
        f"{store.count_billing_accounts(READER2_EXTERNAL_KEY)} billing accounts "
        f"under {READER2_EXTERNAL_KEY}, where the brief pins one")

    keys = [row.get("external_key") for row in
            [store.billing_account(READER_EXTERNAL_KEY),
             store.billing_account(READER2_EXTERNAL_KEY)] if row]
    assert READER_EXTERNAL_KEY in keys, (
        f"the first reader billing account is not keyed {READER_EXTERNAL_KEY}: "
        f"{keys!r}")
    assert READER2_EXTERNAL_KEY in keys, (
        f"the second reader billing account is not keyed {READER2_EXTERNAL_KEY}: "
        f"{keys!r}")

    remote = payments.accounts()
    remote_keys = {str(row.get("externalKey")) for row in remote}
    assert READER_EXTERNAL_KEY in remote_keys, (
        f"the billing platform holds no account under {READER_EXTERNAL_KEY}; the "
        f"tenant carries {sorted(remote_keys)}")


def test_quantity_limit_is_never_oversold_under_contention(store):
    barrier = threading.Barrier(2)
    outcomes: list = []
    lock = threading.Lock()

    def race(email: str) -> None:
        http = fresh_client(email)
        opened = open_session(http, LANTERN_KIT)
        session_id = session_id_of(opened.json()) if opened.status_code in OK_STATUSES else ""
        barrier.wait(timeout=30)
        answered = confirm_session(http, session_id) if session_id else opened
        with lock:
            outcomes.append((email, answered.status_code, answered.text[:200]))
        http.close()

    threads = [threading.Thread(target=race, args=(email,))
               for email in (READER_EMAIL, READER2_EMAIL)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=90)
    settle()

    won = [row for row in outcomes if row[1] in OK_STATUSES]
    assert len(won) == 1, (
        f"two simultaneous confirms of the last unit of {LANTERN_KIT} answered "
        f"{[(row[0], row[1]) for row in outcomes]}, where the brief pins exactly "
        f"one winner")

    product = store.product_by_permalink(LANTERN_KIT)
    assert product is not None, f"the limited product {LANTERN_KIT} is absent"
    limit = product.get("quantity_limit")
    sold = int(product.get("quantity_sold", 0))
    assert limit is not None, (
        f"{LANTERN_KIT} carries no quantity limit, so the contention rule cannot "
        f"hold: {product!r}")
    assert sold <= int(limit), (
        f"{LANTERN_KIT} sold {sold} units against a limit of {limit}")

    sold_orders = [row for row in store.all_orders()
                   if row.get("product_id") == product.get("id")]
    if sold_orders:
        assert len(sold_orders) <= int(limit), (
            f"{LANTERN_KIT} carries {len(sold_orders)} orders against a limit of "
            f"{limit}")


def test_reader_cannot_read_creator_orders(reader_client, creator_client):
    denied = reader_client.get("/orders")
    assert denied.status_code in DENIED_STATUSES, (
        f"a reader session reading the creator order list answered "
        f"{denied.status_code}, where the brief denies it: "
        f"{body_excerpt(denied)!r}")

    allowed = creator_client.get("/orders")
    assert allowed.status_code in OK_STATUSES, where(
        allowed, "the creator reading the order list")

    for route in CREATOR_ONLY_ROUTES:
        refused = reader_client.get(route)
        assert refused.status_code in DENIED_STATUSES, (
            f"a reader session reading {route} answered {refused.status_code}, "
            f"where the brief denies it: {body_excerpt(refused)!r}")


def test_reader_order_view_omits_creator_figures(reader_client):
    confirmed = buy_once(reader_client, FIELD_NOTES)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, "confirming the order the reader will read back")
    number = order_number_of(confirmed.json())

    read = reader_client.get(f"/library/orders/{number}")
    assert read.status_code in OK_STATUSES, where(
        read, f"the reader reading their own order {number}")
    served = read.text
    for hidden in ("platform_fee_minor", "payment_fee_minor",
                   "affiliate_fee_minor", "net_minor"):
        assert hidden not in served, (
            f"the reader-facing view of order {number} carries {hidden}, which "
            f"the brief holds back: {body_excerpt(read)!r}")
    assert "total_minor" in served or "total" in served, (
        f"the reader-facing view of order {number} carries no total: "
        f"{body_excerpt(read)!r}")


def test_reader_cannot_read_the_pricing_decomposition(reader_client):
    denied = reader_client.get(f"/pricing/{FIELD_NOTES}", params={
        "tier_code": TIER_STANDARD,
        "discount_bps": 0,
        "attribution_channel": CHANNEL_DIRECT,
        "tax_jurisdiction": JURISDICTION_ZERO,
    })
    assert denied.status_code in DENIED_STATUSES, (
        f"a reader session reading the pricing decomposition answered "
        f"{denied.status_code}, where the brief denies it: "
        f"{body_excerpt(denied)!r}")


def test_other_reader_entitlement_is_absent(reader_client, reader2_client, store):
    confirmed = buy_once(reader_client, FIELD_NOTES)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, "confirming the order the other reader must not see")
    number = order_number_of(confirmed.json())
    order = store.order_by_number(number)
    assert order is not None, f"order {number} is absent from the orders table"
    granted = store.entitlements_for_order(order.get("id"))
    assert granted, f"order {number} granted no entitlement"
    entitlement_id = granted[0].get("public_id") or granted[0].get("id")

    peeked = reader2_client.get(f"/library/orders/{number}")
    assert peeked.status_code in ABSENT_STATUSES, (
        f"the second reader asking for order {number} answered "
        f"{peeked.status_code}, where the brief answers absent rather than "
        f"forbidden: {body_excerpt(peeked)!r}")

    opened = reader2_client.post(
        f"/library/entitlements/{entitlement_id}/access", json={})
    assert opened.status_code in ABSENT_STATUSES, (
        f"the second reader opening entitlement {entitlement_id} answered "
        f"{opened.status_code}, where the brief answers absent: "
        f"{body_excerpt(opened)!r}")

    listed = reader2_client.get("/library")
    assert listed.status_code in OK_STATUSES, where(
        listed, "the second reader reading their own library")
    assert number not in listed.text, (
        f"the second reader library carries order {number}, which belongs to "
        f"another reader: {body_excerpt(listed)!r}")


def test_anonymous_console_request_is_denied(anon_client):
    for route in CREATOR_ONLY_ROUTES:
        denied = anon_client.get(route)
        assert denied.status_code in DENIED_STATUSES, (
            f"an unauthenticated request for {route} answered "
            f"{denied.status_code}, where the brief denies it: "
            f"{body_excerpt(denied)!r}")

    written = anon_client.post("/products", json={
        "name": "Probe Unauthorized", "permalink": probe_permalink()})
    assert written.status_code in DENIED_STATUSES, (
        f"an unauthenticated product write answered {written.status_code}, where "
        f"the brief denies it: {body_excerpt(written)!r}")


def test_draft_product_is_not_publicly_readable(anon_client, store):
    seeded = store.product_by_permalink(TIDE_TABLES)
    assert seeded is not None, f"the seeded draft product {TIDE_TABLES} is absent"
    assert seeded.get("state") == "draft", (
        f"{TIDE_TABLES} is seeded in state {seeded.get('state')!r} where the brief "
        f"pins a draft")

    listed = anon_client.get("/storefront/products")
    assert listed.status_code in OK_STATUSES, where(
        listed, "the public storefront listing")
    assert TIDE_TABLES not in listed.text, (
        f"the public storefront listing carries the draft {TIDE_TABLES}: "
        f"{body_excerpt(listed)!r}")

    read = anon_client.get(f"/storefront/products/{TIDE_TABLES}")
    assert read.status_code in DENIED_STATUSES, (
        f"a stranger reading the draft {TIDE_TABLES} answered {read.status_code}, "
        f"where the brief holds it back: {body_excerpt(read)!r}")


def test_expired_discount_code_is_refused(reader_client):
    opened = open_session(reader_client, FIELD_NOTES)
    assert opened.status_code in OK_STATUSES, where(
        opened, "opening the session a closed code will be applied to")
    session_id = session_id_of(opened.json())
    before = minor(opened.json().get("total_minor")
                   or opened.json().get("totals", {}).get("total", 0))

    refused = reader_client.post(f"/checkout/sessions/{session_id}/discounts",
                                 json={"code": CLOSED_CODE})
    assert refused.status_code in REFUSED_STATUSES, (
        f"applying the closed code {CLOSED_CODE} answered {refused.status_code}, "
        f"where the brief refuses it: {body_excerpt(refused)!r}")

    read_back = reader_client.get(f"/checkout/sessions/{session_id}")
    assert read_back.status_code in OK_STATUSES, where(
        read_back, f"re-reading session {session_id} after the refusal")
    after = minor(read_back.json().get("total_minor")
                  or read_back.json().get("totals", {}).get("total", 0))
    assert after == before, (
        f"refusing {CLOSED_CODE} moved the session total from {before} to "
        f"{after}, where the brief leaves it unchanged")

    unknown = reader_client.post(f"/checkout/sessions/{session_id}/discounts",
                                 json={"code": "NOSUCHCODE2026"})
    assert unknown.status_code in REFUSED_STATUSES, (
        f"applying a code belonging to no account answered "
        f"{unknown.status_code}, where the brief refuses it: "
        f"{body_excerpt(unknown)!r}")


def test_per_reader_discount_cap_refuses_a_second_use(reader_client):
    first = buy_once(reader_client, FIELD_NOTES, code=OPEN_CODE)
    assert first.status_code in OK_STATUSES, where(
        first, f"the first use of {OPEN_CODE} by this reader")

    opened = open_session(reader_client, FIELD_NOTES)
    assert opened.status_code in OK_STATUSES, where(
        opened, "opening the session for the capped second use")
    session_id = session_id_of(opened.json())

    second = reader_client.post(f"/checkout/sessions/{session_id}/discounts",
                                json={"code": OPEN_CODE})
    assert second.status_code in REFUSED_STATUSES, (
        f"a second use of {OPEN_CODE} by one reader answered "
        f"{second.status_code}, where the brief caps it at one: "
        f"{body_excerpt(second)!r}")


def test_decoy_field_submission_is_refused(anon_client):
    address = probe_email()
    refused = anon_client.post("/auth/signup", json={
        "email": address,
        "display_name": "Probe Reader",
        "country": JURISDICTION_ZERO,
        "password": CORPUS_PASSWORD,
        DECOY_FIELD: "https://spam.example",
    })
    assert refused.status_code in REFUSED_STATUSES, (
        f"a signup filling the decoy field {DECOY_FIELD} answered "
        f"{refused.status_code}, where the brief refuses it: "
        f"{body_excerpt(refused)!r}")

    denied = anon_client.post("/auth/login", json={
        "email": address, "password": CORPUS_PASSWORD})
    assert denied.status_code in DENIED_STATUSES, (
        f"the refused signup for {address} still produced an account that can "
        f"sign in, answering {denied.status_code}: {body_excerpt(denied)!r}")


def test_duplicate_signup_email_is_refused(anon_client):
    refused = anon_client.post("/auth/signup", json={
        "email": READER_EMAIL,
        "display_name": "Probe Duplicate",
        "country": JURISDICTION_ZERO,
        "password": CORPUS_PASSWORD,
        DECOY_FIELD: "",
    })
    assert refused.status_code in REFUSED_STATUSES, (
        f"signing up with the address {READER_EMAIL}, already in use, answered "
        f"{refused.status_code}, where the brief refuses it: "
        f"{body_excerpt(refused)!r}")

    signed_in = anon_client.post("/auth/login", json={
        "email": READER_EMAIL, "password": CORPUS_PASSWORD})
    assert signed_in.status_code in OK_STATUSES, where(
        signed_in, f"signing in as {READER_EMAIL} after the refused duplicate")
    assert signed_in.json().get(TOKEN_KEY), (
        f"the sign-in response for {READER_EMAIL} carries no {TOKEN_KEY}: "
        f"{body_excerpt(signed_in)!r}")


def test_paid_checkout_invoice_exists_for_worked_total(reader_client, store, payments):
    confirmed = buy_once(reader_client, FIELD_NOTES, channel=CHANNEL_DIRECT,
                         code=OPEN_CODE)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, "confirming the purchase whose invoice must exist")
    number = order_number_of(confirmed.json())
    order = store.order_by_number(number)
    assert order is not None, f"order {number} is absent from the orders table"
    assert int(order["total_minor"]) == WORKED_TOTAL_MINOR, (
        f"order {number} carries a total of {order['total_minor']} where the "
        f"brief's worked case gives {WORKED_TOTAL_MINOR}")

    found = wait_for_invoice(payments, WORKED_TOTAL_MINOR)
    assert found is not None, (
        f"no invoice for {WORKED_TOTAL_MINOR} minor units, which reads "
        f"{WORKED_INVOICE_DECIMAL} as a decimal, exists in the billing platform "
        f"after order {number} was confirmed")
    assert found.currency.lower() == "usd", (
        f"the invoice for order {number} carries currency {found.currency!r} "
        f"where the brief pins the account payout currency")

    row = store.invoice_for_order(order.get("id"))
    assert row is not None, (
        f"order {number} has an invoice in the billing platform but no invoice "
        f"row of its own, so the app's tables do not reflect the provider")
    assert int(row.get("amount_minor", -1)) == WORKED_TOTAL_MINOR, (
        f"the invoice row for order {number} carries "
        f"{row.get('amount_minor')!r} where the order total is "
        f"{WORKED_TOTAL_MINOR}")


def test_receipt_email_reaches_the_buying_reader_only(reader_client, store, inbox):
    confirmed = buy_once(reader_client, FIELD_NOTES)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, "confirming the purchase whose receipt must arrive")
    number = order_number_of(confirmed.json())

    subject = RECEIPT_SUBJECT_PREFIX + FIELD_NOTES_NAME
    message = wait_for_email(inbox, READER_EMAIL, subject)
    assert message is not None, (
        f"no message with a subject beginning {subject!r} reached "
        f"{READER_EMAIL} after order {number} was confirmed")

    body = str(getattr(message, "body", "") or getattr(message, "text", ""))
    assert body.strip(), (
        f"the receipt for order {number} carries an empty body")
    assert FIELD_NOTES_NAME in body or FIELD_NOTES_NAME in str(message), (
        f"the receipt for order {number} never names {FIELD_NOTES_NAME!r}: "
        f"{body[:300]!r}")

    other = inbox.find(READER2_EMAIL, subject)
    assert other is None, (
        f"a receipt for order {number} also reached {READER2_EMAIL}, which did "
        f"not buy anything: {other!r}")


def test_refused_confirm_sends_no_receipt_email(reader_client, store, inbox):
    before = inbox.count(READER_EMAIL)

    opened = open_session(reader_client, FIELD_NOTES)
    assert opened.status_code in OK_STATUSES, where(
        opened, "opening the session whose discount will be refused")
    session_id = session_id_of(opened.json())
    refused = reader_client.post(f"/checkout/sessions/{session_id}/discounts",
                                 json={"code": CLOSED_CODE})
    assert refused.status_code in REFUSED_STATUSES, (
        f"applying the closed code {CLOSED_CODE} answered {refused.status_code}, "
        f"where the brief refuses it: {body_excerpt(refused)!r}")

    missing = confirm_session(reader_client, "handsel-no-such-session")
    assert missing.status_code in DENIED_STATUSES + REFUSED_STATUSES, (
        f"confirming a session that does not exist answered "
        f"{missing.status_code}: {body_excerpt(missing)!r}")
    settle()

    after = inbox.count(READER_EMAIL)
    assert after == before, (
        f"a refused discount followed by a refused confirm moved the message "
        f"count for {READER_EMAIL} from {before} to {after}, where the brief "
        f"sends nothing")


def test_product_page_html_carries_the_price(anon_client):
    served = anon_client.get(f"/storefront/products/{FIELD_NOTES}")
    assert served.status_code in OK_STATUSES, where(
        served, f"the public product read for {FIELD_NOTES}")
    payload = served.text
    assert FIELD_NOTES_NAME in payload, (
        f"the public product read for {FIELD_NOTES} never names "
        f"{FIELD_NOTES_NAME!r}: {body_excerpt(served)!r}")
    assert str(FIELD_NOTES_STANDARD_MINOR) in payload, (
        f"the public product read for {FIELD_NOTES} carries no base tier price "
        f"of {FIELD_NOTES_STANDARD_MINOR}: {body_excerpt(served)!r}")
    assert TIER_STANDARD in payload, (
        f"the public product read for {FIELD_NOTES} names no tier code "
        f"{TIER_STANDARD!r}: {body_excerpt(served)!r}")


def test_terms_page_names_the_seller_of_record(anon_client):
    with httpx.Client(base_url=app_url(), timeout=30.0) as browserless:
        page = browserless.get("/terms")
        assert page.status_code in OK_STATUSES, where(
            page, "the public terms page")
        assert MOR_ENTITY in page.text, (
            f"the terms page never names the seller of record {MOR_ENTITY!r}: "
            f"{page.text[:400]!r}")


def test_unknown_address_answers_not_found(anon_client):
    with httpx.Client(base_url=app_url(), timeout=30.0) as browserless:
        page = browserless.get("/handsel-no-such-address-" + probe_key())
        assert page.status_code in ABSENT_STATUSES, (
            f"an unknown address answered {page.status_code}, where the brief "
            f"answers not-found: {page.text[:300]!r}")
        assert page.text.strip(), (
            "the not-found page carries no body, so it offers no way back")


def test_health_route_answers_ready(anon_client):
    ready = anon_client.get("/health")
    assert ready.status_code in OK_STATUSES, where(
        ready, "the readiness route under the api prefix")


def test_no_credential_appears_in_a_served_page(anon_client):
    with httpx.Client(base_url=app_url(), timeout=30.0) as browserless:
        for path in ("/", "/terms", "/login", "/signup"):
            page = browserless.get(path)
            assert page.status_code in OK_STATUSES, where(
                page, f"the public page at {path}")
            assert CORPUS_PASSWORD not in page.text, (
                f"the page at {path} carries the seeded password in what the "
                f"browser downloads: {page.text[:300]!r}")
            for secret in ("orbit-labs-secret-9f14c73e", "deku-local-dev"):
                assert secret not in page.text, (
                    f"the page at {path} carries the credential {secret!r} in "
                    f"what the browser downloads")


def test_seeding_is_idempotent_and_the_account_is_seeded(store):
    for address in (CREATOR_EMAIL, READER_EMAIL, READER2_EMAIL):
        assert store.count_users(address) == 1, (
            f"the users table holds {store.count_users(address)} rows for "
            f"{address}, where seeding writes exactly one")

    account = store.account_row()
    assert account is not None, (
        f"no account row carries the handle {ACCOUNT_HANDLE}")
    assert str(account.get("payout_currency", "")).lower() == PAYOUT_CURRENCY, (
        f"the account carries payout currency "
        f"{account.get('payout_currency')!r} where the brief pins "
        f"{PAYOUT_CURRENCY!r}")

    for permalink in (FIELD_NOTES, LANTERN_KIT, TIDE_TABLES):
        assert store.count_products(permalink) == 1, (
            f"the products table holds {store.count_products(permalink)} rows "
            f"for {permalink}, where seeding writes exactly one")

    for address, name, country in (
            (CREATOR_EMAIL, CREATOR_NAME, JURISDICTION_ZERO),
            (READER_EMAIL, READER_NAME, JURISDICTION_TAXED),
            (READER2_EMAIL, READER2_NAME, JURISDICTION_ZERO)):
        row = store.user_by_email(address)
        assert row is not None, f"no user row carries the address {address}"
        assert row.get("display_name") == name, (
            f"{address} is seeded with the display name "
            f"{row.get('display_name')!r} where the brief pins {name!r}")
        assert str(row.get("country", "")).upper() == country, (
            f"{address} is seeded with the country {row.get('country')!r} "
            f"where the brief pins {country!r}")

    creators = store.users_with_role("creator")
    assert len(creators) == 1, (
        f"the users table holds {len(creators)} principals in the creator role, "
        f"where the brief pins exactly one")


def test_list_endpoints_return_a_top_level_array(anon_client, creator_client):
    listed = anon_client.get("/storefront/products")
    assert listed.status_code in OK_STATUSES, where(
        listed, "the public storefront listing")
    assert isinstance(listed.json(), list), (
        f"the storefront listing returned {type(listed.json()).__name__} where "
        f"the brief pins a top-level array: {body_excerpt(listed)!r}")

    owned = creator_client.get("/products")
    assert owned.status_code in OK_STATUSES, where(
        owned, "the creator catalog listing")
    assert isinstance(owned.json(), list), (
        f"the creator catalog returned {type(owned.json()).__name__} where the "
        f"brief pins a top-level array: {body_excerpt(owned)!r}")


def test_creator_holds_no_library(creator_client):
    denied = creator_client.get("/library")
    assert denied.status_code in DENIED_STATUSES, (
        f"the creator reading a reader library answered {denied.status_code}, "
        f"where the brief denies it: {body_excerpt(denied)!r}")

    bought = open_session(creator_client, FIELD_NOTES)
    assert bought.status_code in DENIED_STATUSES + REFUSED_STATUSES, (
        f"the creator opening a checkout answered {bought.status_code}, where "
        f"the brief holds the creator out of the buying path: "
        f"{body_excerpt(bought)!r}")


def test_signed_in_principal_reports_its_role(creator_client, reader_client):
    for http, role in ((creator_client, "creator"), (reader_client, "reader")):
        read = http.get("/me")
        assert read.status_code in OK_STATUSES, where(
            read, "reading the signed-in principal")
        assert role in read.text, (
            f"the principal read for the {role} never names the role held: "
            f"{body_excerpt(read)!r}")


def test_out_of_scope_surfaces_are_absent(creator_client):
    for route in ("/memberships", "/refunds", "/disputes", "/payouts",
                  "/broadcasts", "/segments", "/reviews", "/affiliates",
                  "/webhooks", "/search", "/media", "/uploads",
                  "/storefront/domains", "/certificates"):
        answered = creator_client.get(route)
        assert answered.status_code in ABSENT_STATUSES + DENIED_STATUSES, (
            f"the out-of-scope surface {route} answered "
            f"{answered.status_code}; the brief places it outside this product, "
            f"so nothing should serve it: {body_excerpt(answered)!r}")


def test_every_money_figure_carries_one_currency(reader_client, store):
    confirmed = buy_once(reader_client, FIELD_NOTES)
    assert confirmed.status_code in OK_STATUSES, where(
        confirmed, "confirming the order whose currency is read back")
    order = store.order_by_number(order_number_of(confirmed.json()))
    assert order is not None, "the order whose currency is read back is absent"
    assert str(order.get("currency", "")).lower() == PAYOUT_CURRENCY, (
        f"the order carries currency {order.get('currency')!r} where the brief "
        f"pins the one currency {PAYOUT_CURRENCY!r}")
    for row in store.all_postings():
        assert str(row.get("currency", "")).lower() == PAYOUT_CURRENCY, (
            f"a ledger posting carries currency {row.get('currency')!r} where "
            f"the brief pins the one currency {PAYOUT_CURRENCY!r}")


def test_discount_depth_below_zero_is_refused(creator_client):
    refused = creator_client.post("/discount-codes", json={
        "code": "PROBE" + probe_key()[:6].upper(),
        "value_bps": 12000,
        "max_uses": 1,
        "max_per_reader": 1,
        "starts_at": "2026-01-01T00:00:00Z",
        "ends_at": "2027-01-01T00:00:00Z",
    })
    assert refused.status_code in REFUSED_STATUSES, (
        f"raising a code whose depth would take a total below zero answered "
        f"{refused.status_code}, where the brief refuses it: "
        f"{body_excerpt(refused)!r}")
