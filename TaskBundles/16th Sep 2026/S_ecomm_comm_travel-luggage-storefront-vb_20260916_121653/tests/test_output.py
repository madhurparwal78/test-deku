"""Observations of the valisette storefront, one function per graded behaviour.

Every test speaks to the running app over HTTP, to PostgreSQL through the backend
capability, to killbill and to Mailpit, or drives the page through Playwright. Shared
state a test moves (the sale end, stock, a product's title) is put back before it ends.
"""

from __future__ import annotations

import os
import re
import urllib.parse

import httpx

from conftest import (
    ACME, ALT_EXAMPLE, AMELIA, BADGES, BADGE_SOLD_OUT, BAG_TYPES, BEST_SELLER_COUNT,
    BEST_SELLING_FIRST, CABIN_PINK, CATEGORY_HANDLES, COLLECTIONS, COLLECTION_KINDS, COLOURWAYS,
    CORPORATE_ACCOUNTS, COUNTRY, CURRENCY, CUSTOMER2_EMAIL, CUSTOMER_EMAIL, DEFAULT_STOCK,
    DERIVED_COLUMNS, DISCOUNT_EXAMPLES, ENDED_SALE_EXAMPLE, ERR_CART_EMPTY, ERR_CORPORATE_CURRENCY,
    ERR_CORPORATE_UNKNOWN, ERR_INSUFFICIENT, ERR_NOT_FOUND, ERR_OUT_OF_STOCK, ERR_PRICE_CHANGED,
    EXPRESS, EXPRESS_COST, EXTERNAL_KEY_PREFIX, FIRST_NEW_ORDER, GIFT_ACTIVE, GIFT_ACTIVE_BALANCE,
    GIFT_LAPSED, GIFT_LAPSED_BALANCE, GIFT_LAPSED_EXPIRY, KB_EUR, KB_HEALTH_PATH, KB_USD,
    KIND_PARENT, LOGIN_PATH, LUGGAGE_TOTAL, MAIL_FROM, MEDIA_KINDS, MEDIA_KIND_IMAGE,
    MONEY_EXAMPLES, MORE_MERIDIAN, MORE_PASSAGE, MOVEMENT_KINDS, MOVE_ADJUSTMENT,
    MOVE_CANCELLATION, MOVE_RESTOCK, MOVE_SALE, MSG_CORPORATE_EUR, MSG_CORPORATE_UNKNOWN,
    MSG_GIFT_UNKNOWN, MSG_LOGIN, MSG_NEWSLETTER, MSG_PRICE_CHANGED, MSG_RECOVER, MSG_SOLD_OUT,
    MSG_TWO_LEFT, NORTHWIND, NOT_FOUND_HEADING, NOT_FOUND_LABELS, NOT_FOUND_LINE, NOT_FOUND_LINKS,
    OLIVE, ON_SALE_PAGE_TWO, ON_SALE_TOTAL, OPENING_EXAMPLE, ORDER3_ADDRESS, ORDER_PREFIX,
    ORDER_STATES, OWNER_EMAIL, PAGES, PAGE_SIZE, PANEL_ENTRIES, PLACEMENTS, PRICE_DESC_FIRST,
    PRICE_EXCEPTIONS, PRIVACY_PATH, PRODUCTS, PUBLIC_ROUTES, RESET_BUTTON, RESET_DONE,
    RESET_HEADING, RESET_PATH, RESET_SUBJECT, ROLE_CUSTOMER, ROLE_OWNER, RULE_MEMBERS, SALE_NAME,
    SALE_WAIT_SECONDS, SCRIPT_BUDGET_BYTES, SEARCH_COASTAL, SEARCH_EXAMPLE, SEARCH_MERIDIAN_LAST,
    SEARCH_OLIVE_COUNT, SEEDED_ACCOUNTS, SEEDED_PASSWORD, SEED_ADDRESS, SEED_NUMBERS, SEED_ORDERS,
    SEED_PLACED_DAYS_BEFORE_START, SELF_BILLED_KEYS, SET_HANDLES_OF_3, SET_HANDLE_OF_2,
    SET_OF_2_FIGURES, SET_OF_3_FIGURES, SIBLING_SIZES, SIGNED_IN_ROUTES, SIZE_CLASSES,
    SIZE_FIGURES, SORTS, STANDARD, STATE_CANCELLED, STATE_FULFILLED, STATE_PAID, STOCK_EXCEPTIONS,
    STORES, STORES_NEW, STORES_PATH, STORES_PORT, SUBJECT_EXAMPLE, TABLES, TAGS, USES,
    VARIANT_COUNT, WALLETS_RANGE, WORKED_EXAMPLES, accepted, add_line, addresses, api, api_base,
    app_path, app_url, body_of, cart, cart_token_in_page, change_line, checkout, checkout_key,
    clock_offset_time, collect_requests, collection, collection_page, collection_titles,
    countdown_seconds, currency_refusal, date_of, delivery_address, denied, describe,
    discount_percent, ensure_stock, error_of, external_key, favicon_href, fetch_asset,
    fetch_document, filled_cart, gzip_size, internal_hrefs, is_client_error, iso_from_now,
    kb_account, kb_open_account, login, login_response, mail_text, mail_to, me, message_of, money,
    move_sale_end, movement_count, movement_sum, movements, new_cart, now_utc, only_left,
    open_page, opening_for, order_count, order_row, orders_for_key, owner_order, owner_orders,
    owner_token, page_text, parse_stamp, pinned_variants, place_order, poll_until, probe_address,
    probe_password, product, product_handles_shown, product_row, record_movement, remove_line,
    run_together, sale, save_address, scalar, script_sources, search, seconds_until, set_stock,
    settle, signup, sql, stock_of, subject_for, table_columns, today_utc, top_level_array,
    unescape, unique_suffix, units_since_start, unnamed_controls, variant, wait_for_mail,
)


def all_products() -> list[dict]:
    return [product(row[0]) for row in PRODUCTS]


def card_handles(cards) -> list[str]:
    return [card["handle"] for card in cards]


def sibling_handle(entry) -> str:
    return entry.get("handle") if isinstance(entry, dict) else str(entry)


def lowest_live_price(read: dict) -> int:
    return min(int(v["price"]) for v in read["variants"])


def seeded_units(sku: str) -> int:
    return sum(qty for order in SEED_ORDERS for line_sku, qty, _, _ in order[3] if line_sku == sku)


def test_checkout_opens_the_billing_account_in_killbill():
    """A paid order is billed to valisette-<number>, and killbill holds that account."""
    ensure_stock(["PSG-CAB-OLV"])
    email = probe_address(unique_suffix())
    address = delivery_address(name="Probe Billing " + unique_suffix())
    cart_token = filled_cart([("PSG-CAB-OLV", 1)])
    response = checkout(cart_token, email=email, address=address)
    assert response.status_code in (200, 201), describe(response, "an in-stock checkout is accepted")
    order = response.json()
    number = order["number"]
    key = external_key(number)
    assert order["state"] == STATE_PAID, describe(response, "an accepted checkout is paid")
    assert order["billing_account"] == key, describe(response, "billing_account is valisette-<number>")
    found = kb_account(key)
    assert found.status_code == 200, describe(found, f"killbill must hold the account {key}")
    account = found.json()
    assert account.get("externalKey") == key, f"killbill account key: {account}"
    assert account.get("name") == address["name"], f"killbill account name: {account}"
    assert (account.get("email") or "").lower() == email.lower(), f"killbill email: {account}"
    assert account.get("currency") == KB_USD, f"killbill currency: {account}"
    assert account.get("country") == COUNTRY, f"killbill country: {account}"
    row = order_row(number)
    assert row is not None, f"{number} is not a row in PostgreSQL"
    assert row["billing_account"] == key and row["state"] == STATE_PAID, f"stored order: {row}"
    assert key.startswith(EXTERNAL_KEY_PREFIX), key


def test_guest_checkout_creates_a_guest_order():
    """A signed-out checkout answers with the whole order and stores it with no account."""
    order = place_order([("MNI-SLG-NSH", 1)])
    for field in ("number", "state", "email", "lines", "address", "delivery_method",
                  "delivery_from", "delivery_to", "subtotal", "discount", "delivery", "total",
                  "currency", "billing_account", "placed_at"):
        assert field in order, f"the order answer lacks {field}: {order}"
    assert order["currency"] == CURRENCY, f"order currency: {order['currency']}"
    assert order["delivery_method"] == STANDARD, f"delivery method: {order}"
    assert order["address"]["postcode"] == delivery_address()["postcode"], order["address"]
    row = order_row(order["number"])
    assert row is not None and row["account_id"] is None, f"a guest order has no account: {row}"


def test_paid_order_rows_are_persisted_with_captured_prices():
    """Order, lines and one sale movement per line are written together, and the cart empties."""
    lines = [("PSG-CAB-SSU", 1), ("MNI-SLG-CSP", 2)]
    ensure_stock([sku for sku, _ in lines])
    before = {sku: stock_of(sku) for sku, _ in lines}
    cart_token = filled_cart(lines)
    key = checkout_key()
    response = checkout(cart_token, key=key)
    assert response.status_code in (200, 201), describe(response, "the checkout is accepted")
    number = response.json()["number"]
    order_columns = table_columns("orders")
    for column in ("number", "account_id", "email", "address_snapshot", "delivery_method",
                   "subtotal", "discount", "delivery", "total", "currency", "state",
                   "checkout_key", "billing_account", "placed_at"):
        assert column in order_columns, f"orders has no column {column}: {sorted(order_columns)}"
    line_columns = table_columns("order_line")
    for column in ("order_id", "variant_id", "sku", "product_title", "colourway", "size_class",
                   "quantity", "unit_price", "list_price", "properties"):
        assert column in line_columns, f"order_line has no column {column}"
    row = order_row(number)
    assert row["checkout_key"] == key and row["state"] == STATE_PAID, f"stored order: {row}"
    stored = {r["sku"]: r for r in sql("SELECT * FROM order_line WHERE order_id = %s", row["id"])}
    assert set(stored) == {sku for sku, _ in lines}, f"stored lines: {stored}"
    assert stored["PSG-CAB-SSU"]["unit_price"] == 17900, stored["PSG-CAB-SSU"]
    assert stored["PSG-CAB-SSU"]["list_price"] == 29900, stored["PSG-CAB-SSU"]
    assert stored["MNI-SLG-CSP"]["unit_price"] == 4900, stored["MNI-SLG-CSP"]
    assert stored["MNI-SLG-CSP"]["quantity"] == 2, stored["MNI-SLG-CSP"]
    sales = sql("SELECT m.delta, m.kind, v.sku FROM stock_movement m JOIN variant v "
                "ON v.id = m.variant_id WHERE m.order_id = %s", row["id"])
    assert sorted((m["sku"], m["delta"], m["kind"]) for m in sales) == sorted(
        (sku, -qty, MOVE_SALE) for sku, qty in lines), f"sale movements: {sales}"
    for sku, qty in lines:
        assert stock_of(sku) == before[sku] - qty, f"{sku} stock did not drop by {qty}"
    assert cart(cart_token)["lines"] == [], "a completed checkout empties the cart"


def test_confirmation_email_is_delivered_once():
    """One email from orders@valisette.example.com with the pinned subject, no cc, no bcc."""
    email = probe_address(unique_suffix())
    order = place_order([("PCK-CUB-SSU", 1)], email=email)
    rows = wait_for_mail(email)
    assert len(rows) == 1, f"expected one confirmation for {email}, found {len(rows)}"
    message = rows[0]
    assert (message.get("From") or {}).get("Address", "").lower() == MAIL_FROM, message.get("From")
    assert message.get("Subject") == subject_for(order["number"]), message.get("Subject")
    assert not message.get("Cc") and not message.get("Bcc"), f"copies were sent: {message}"
    assert subject_for(FIRST_NEW_ORDER) == SUBJECT_EXAMPLE
    settle()
    settle()
    assert len(mail_to(email)) == 1, "the confirmation must be sent exactly once"


def test_confirmation_email_names_the_order():
    """The body opens with the number and total, then lines, personalisation, address, window."""
    ensure_stock(["MRD-CAB-HTG", "MNI-SLG-NSH"])
    email = probe_address(unique_suffix())
    cart_token = new_cart()
    response = add_line(cart_token, "MRD-CAB-HTG", 1, {"initials": "QA", "placement": "top"})
    assert accepted(response), describe(response, "a personalised line joins the cart")
    response = add_line(cart_token, "MNI-SLG-NSH", 2)
    assert accepted(response), describe(response, "a second line joins the cart")
    address = delivery_address(line1="77 Probe Terrace", postcode="97209")
    placed = checkout(cart_token, email=email, address=address)
    assert placed.status_code in (200, 201), describe(placed, "the checkout is accepted")
    order = placed.json()
    rows = wait_for_mail(email)
    assert rows, f"no confirmation reached {email}"
    text = mail_text(rows[0]).strip()
    assert text.startswith(opening_for(order["number"], order["total"])), text[:200]
    for needle in ("Meridian Luggage - Cabin", "Hold The Grey", "Mini Sling", "Night Shift",
                   "Initials: QA, top", "77 Probe Terrace", "97209"):
        assert needle in text, f"the confirmation body lacks {needle!r}: {text[:600]}"
    assert "cabin" in text.lower(), "the body names the size class"
    assert re.search(r"\b2\b", text), "the body names the quantity 2"
    assert opening_for(FIRST_NEW_ORDER, 27700) == OPENING_EXAMPLE
    assert all(money(cents) == shown for cents, shown in MONEY_EXAMPLES)


def test_checkout_totals_match_the_worked_examples():
    """The three sale-time rows of the worked table total as the brief states."""
    for lines, method, subtotal, discount, delivery, total, shown in WORKED_EXAMPLES:
        email = probe_address(unique_suffix())
        order = place_order(list(lines), method=method, email=email)
        assert (order["subtotal"], order["discount"], order["delivery"], order["total"]) == (
            subtotal, discount, delivery, total), f"{lines} on {method}: {order}"
        rows = wait_for_mail(email)
        assert rows, f"no confirmation for {email}"
        opening = f"Order {order['number']}, total charged {shown}."
        assert mail_text(rows[0]).strip().startswith(opening), f"expected {opening}"


def test_checkout_empties_the_cart():
    """A refused checkout keeps the lines; a completed checkout empties the cart."""
    ensure_stock(["TRV-PLW-DEB"])
    cart_token = filled_cart([("TRV-PLW-DEB", 1)])
    refused = checkout(cart_token, address=delivery_address(postcode="12"))
    assert is_client_error(refused), describe(refused, "a bad postcode is refused")
    assert len(cart(cart_token)["lines"]) == 1, "a refused checkout leaves the cart as it was"
    placed = checkout(cart_token)
    assert placed.status_code in (200, 201), describe(placed, "the checkout is accepted")
    after = cart(cart_token)
    assert after["lines"] == [] and after["item_count"] == 0, f"cart after payment: {after}"


def test_order_numbers_count_up_from_the_seed():
    """Numbers read VS- and six digits, rise from VS-100004 and never repeat."""
    first = place_order([("TRV-PLW-HTG", 1)])["number"]
    second = place_order([("TRV-PLW-HTG", 1)])["number"]
    for number in (first, second):
        assert re.fullmatch(r"VS-\d{6}", number), number
        assert number.startswith(ORDER_PREFIX)
    assert int(second[3:]) > int(first[3:]) > int(SEED_NUMBERS[-1][3:]), (first, second)
    lowest = scalar("SELECT min(number) FROM orders WHERE number NOT IN (%s, %s, %s)",
                    *SEED_NUMBERS)
    assert lowest == FIRST_NEW_ORDER, f"the first new order was {lowest}"
    total = scalar("SELECT count(*) FROM orders")
    distinct = scalar("SELECT count(DISTINCT number) FROM orders")
    assert total == distinct, "order numbers repeat"


def test_delivery_estimate_follows_the_method():
    """standard costs 0 and arrives in 3 to 5 days; express costs 1500 and arrives in 1 to 2."""
    today = today_utc()
    with api() as client:
        standard = client.get("/delivery-estimate", params={"method": STANDARD})
        express = client.get("/delivery-estimate", params={"method": EXPRESS})
    assert standard.status_code == 200, describe(standard, "the standard estimate")
    assert express.status_code == 200, describe(express, "the express estimate")
    s, e = standard.json(), express.json()
    assert s["method"] == STANDARD and s["cost"] == 0, s
    assert e["method"] == EXPRESS and e["cost"] == EXPRESS_COST, e
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", s["from"]) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", e["to"])
    assert ((date_of(s["from"]) - today).days, (date_of(s["to"]) - today).days) == (3, 5), s
    assert ((date_of(e["from"]) - today).days, (date_of(e["to"]) - today).days) == (1, 2), e
    order = place_order([("TRV-PLW-DEB", 1)], method=EXPRESS)
    placed = date_of(order["placed_at"])
    assert (date_of(order["delivery_from"]) - placed).days == 1, order
    assert (date_of(order["delivery_to"]) - placed).days == 2, order


def test_personalisation_travels_to_the_order():
    """Initials are stored in capitals and reach the order line unchanged."""
    ensure_stock(["MRD-CAB-CCV", "MRD-MED-CCV"])
    cart_token = new_cart()
    first = add_line(cart_token, "MRD-CAB-CCV", 1, {"initials": "ab 1", "placement": "front"})
    assert accepted(first), describe(first, "a front personalisation joins the cart")
    second = add_line(cart_token, "MRD-MED-CCV", 1, {"initials": "Z", "placement": "top"})
    assert accepted(second), describe(second, "a top personalisation joins the cart")
    props = {line["sku"]: line["properties"] for line in cart(cart_token)["lines"]}
    assert props["MRD-CAB-CCV"] == {"initials": "AB 1", "placement": "front"}, props
    assert props["MRD-MED-CCV"] == {"initials": "Z", "placement": "top"}, props
    placed = checkout(cart_token)
    assert placed.status_code in (200, 201), describe(placed, "the checkout is accepted")
    lines = {line["sku"]: line["properties"] for line in placed.json()["lines"]}
    assert lines == props, f"order line properties {lines} differ from the cart {props}"
    assert set(PLACEMENTS) == {"front", "top"}


def test_refused_checkout_sends_no_email():
    """Neither a validation refusal nor a corporate refusal sends mail."""
    ensure_stock(["TRV-PLW-HTG"])
    email = probe_address(unique_suffix())
    cart_token = filled_cart([("TRV-PLW-HTG", 1)])
    bad = checkout(cart_token, email=email, address=delivery_address(country="CA"))
    assert is_client_error(bad), describe(bad, "a foreign country is refused")
    corporate = checkout(cart_token, email=email, corporate="orbit-missing-" + unique_suffix())
    assert is_client_error(corporate), describe(corporate, "an unknown corporate account is refused")
    for _ in range(8):
        settle()
    assert mail_to(email) == [], "a refused checkout sent an email"


def test_non_order_actions_send_no_email():
    """Signup, sign-in, a cart change and a subscription are silent."""
    suffix = unique_suffix()
    account = signup(suffix)
    login(account["email"], account["password"])
    cart_token = new_cart(account["token"])
    assert accepted(add_line(cart_token, "PCK-CUB-HTG", 1, token=account["token"]))
    with api() as client:
        subscribed = client.post("/newsletter", json={"email": account["email"]})
    assert accepted(subscribed), describe(subscribed, "the subscription is accepted")
    for _ in range(8):
        settle()
    assert mail_to(account["email"]) == [], "a non-order action sent an email"


def test_collections_are_listed_in_order():
    """The thirty-one collections list in table order with handle, name, kind and count."""
    with api() as client:
        rows = top_level_array(client.get("/collections"))
    assert [r["handle"] for r in rows] == [c[0] for c in COLLECTIONS], [r["handle"] for r in rows]
    for row, (handle, name, kind, _strap, count) in zip(rows, COLLECTIONS):
        assert (row["name"], row["kind"], row["product_count"]) == (name, kind, count), row
    kinds = [r["kind"] for r in rows]
    assert kinds.count("line") == 6 and "size" in kinds, kinds
    assert set(kinds) <= set(COLLECTION_KINDS), kinds


def test_collection_detail_carries_banner_title_with_siblings():
    """Straplines, banner titles and siblings follow the collection rules."""
    by_kind = {}
    for handle, _name, kind, _strap, _count in COLLECTIONS:
        by_kind.setdefault(kind, []).append(handle)
    for handle, name, kind, strapline, _count in COLLECTIONS:
        detail = collection(handle)
        assert (detail["handle"], detail["name"], detail["kind"]) == (handle, name, kind), detail
        assert detail["strapline"] == strapline, detail
        expected_title = f"The {name} Series" if kind == "line" else name
        assert detail["banner_title"] == expected_title, detail
        siblings = [sibling_handle(s) for s in detail["siblings"]]
        if kind == "all":
            expected = list(CATEGORY_HANDLES)
        else:
            expected = [h for h in by_kind[kind] if h != handle] + [KIND_PARENT[kind]]
        assert siblings == expected, f"{handle} siblings {siblings} != {expected}"
    assert collection("meridian")["banner_title"] == "The Meridian Series"
    positions = sql("SELECT handle FROM collection ORDER BY position")
    assert [r["handle"] for r in positions] == [c[0] for c in COLLECTIONS], positions


def test_collection_membership_follows_the_rules():
    """Each rule collection holds exactly the table's products, in position order."""
    for handle, titles in RULE_MEMBERS:
        found = collection_titles(handle)
        assert found == list(titles), f"{handle}: {found} != {list(titles)}"
    counts = {c[0]: c[4] for c in COLLECTIONS}
    for handle, titles in RULE_MEMBERS:
        assert len(titles) == counts[handle], handle
    assert collection_page("luggage")["total"] == LUGGAGE_TOTAL


def test_panel_entries_resolve_to_collections():
    """Every panel entry names a collection that serves a page."""
    names = {c[1]: c[0] for c in COLLECTIONS}
    for entry in PANEL_ENTRIES:
        assert entry in names, f"panel entry {entry!r} names no collection"
        document = fetch_document(f"/collections/{names[entry]}")
        assert document.status_code == 200, describe(document, f"{entry} collection page")
    for handle in CATEGORY_HANDLES:
        assert fetch_document(f"/collections/{handle}").status_code == 200, handle


def test_unknown_handles_answer_not_found():
    """Unknown collection, cart, product and page handles answer the not-found status."""
    with api() as client:
        missing_collection = client.get("/collections/no-such-collection")
        missing_cart = client.get("/carts/" + "Z" * 32)
        missing_product = client.get("/products/no-such-product")
    assert missing_collection.status_code == 404, describe(missing_collection, "unknown collection")
    assert missing_cart.status_code == 404, describe(missing_cart, "unknown cart token")
    assert missing_product.status_code == 404, describe(missing_product, "unknown product")
    for path in ("/collections/no-such-collection", "/products/no-such-product",
                 "/pages/no-such-page", "/no-such-address"):
        document = fetch_document(path)
        assert document.status_code == 404, describe(document, f"{path} is not found")
        assert "html" in document.headers.get("content-type", ""), describe(document, path)


def test_collection_pages_hold_twenty_four_cards():
    """page_size is 24, page counts from 1, and on-sale page 2 holds 10 of 34."""
    first = collection_page("luggage")
    assert set(first) >= {"products", "total", "page", "page_size"}, first.keys()
    assert first["page_size"] == PAGE_SIZE and first["page"] == 1, first
    second = collection_page("on-sale", page=2)
    assert second["page"] == 2 and second["total"] == ON_SALE_TOTAL, second
    assert len(second["products"]) == ON_SALE_PAGE_TWO, len(second["products"])
    assert len(collection_page("on-sale")["products"]) == PAGE_SIZE


def test_cards_carry_four_colourways_with_the_overflow():
    """A card lists its first four colourways and counts the rest."""
    cards = {c["handle"]: c for c in collection_page("luggage")["products"]}
    for handle, card in cards.items():
        for field in ("handle", "title", "lowest_price", "colourways", "more_colourways"):
            assert field in card, f"{handle} card lacks {field}"
        row = product_row(handle)
        codes = row[14]
        assert [c["sku"] for c in card["colourways"]] == [f"{row[13]}-{x}" for x in codes[:4]], card
        assert card["more_colourways"] == max(0, len(codes) - 4), card
        for swatch in card["colourways"]:
            for field in ("sku", "colourway", "swatch", "price", "list_price", "in_stock", "badge"):
                assert field in swatch, f"{handle} swatch lacks {field}"
        assert card["lowest_price"] == lowest_live_price(product(handle)), card
    assert cards["meridian-luggage-cabin"]["more_colourways"] == MORE_MERIDIAN
    assert cards["passage-luggage-cabin"]["more_colourways"] == MORE_PASSAGE


def test_best_sellers_hold_the_top_twenty():
    """best-sellers holds the twenty highest units_sold, most first."""
    reads = all_products()
    ranked = sorted(zip(reads, range(len(reads))), key=lambda pair: (-pair[0]["units_sold"], pair[1]))
    expected = [r["title"] for r, _ in ranked[:BEST_SELLER_COUNT]]
    assert collection_titles("best-sellers") == expected


def test_home_bestseller_grid_matches_the_collection(page):
    """The home grid shows the same twenty products in the same order."""
    expected = [card["handle"] for card in collection_page("best-sellers")["products"]]
    open_page(page, "/")

    def handles():
        hrefs = page.evaluate(
            "() => Array.from(document.querySelectorAll('main a[href*=\"/products/\"]'))"
            ".map(a => a.getAttribute('href'))")
        seen = []
        for href in hrefs or []:
            handle = urllib.parse.urlparse(href).path.rstrip("/").rsplit("/", 1)[-1]
            if handle not in seen:
                seen.append(handle)
        return seen if len(seen) >= BEST_SELLER_COUNT else None

    found = poll_until(handles) or []
    assert found[:BEST_SELLER_COUNT] == expected, f"home grid {found[:20]} != {expected}"


def test_luggage_carries_a_size_class_bags_a_bag_type():
    """Luggage carries one size class, a bag one bag type, from the closed sets."""
    sizes, types = set(), set()
    for read in all_products():
        if read["category"] == "luggage":
            assert read["size_class"] in SIZE_CLASSES and not read["bag_type"], read["handle"]
            sizes.add(read["size_class"])
        elif read["category"] == "backpacks-and-briefcases":
            assert read["bag_type"] in BAG_TYPES and not read["size_class"], read["handle"]
            types.add(read["bag_type"])
        else:
            assert not read["size_class"] and not read["bag_type"], read["handle"]
    assert sizes == set(SIZE_CLASSES) and types == set(BAG_TYPES), (sizes, types)


def test_products_carry_one_category_with_at_most_one_line():
    """Each product names one category and no more than one of the six lines."""
    lines = {row[3].lower() for row in PRODUCTS if row[3]}
    assert len(lines) == 6, lines
    for read, row in zip(all_products(), PRODUCTS):
        assert read["category"] == row[2] and read["category"] in CATEGORY_HANDLES, read["handle"]
        line = read.get("line")
        assert isinstance(line, (str, type(None))), f"{read['handle']} line {line!r}"
        assert (line or "").lower() == (row[3] or "").lower(), f"{read['handle']} line {line!r}"


def test_use_tag_collections_follow_the_product_table():
    """The use and tag collections hold the products the table marks."""
    for use in USES:
        expected = [row[1] for row in PRODUCTS if use in row[6]]
        assert collection_titles(use) == expected, use
    for tag, handle in zip(TAGS, ("tech-range", "clearance-sale")):
        expected = [row[1] for row in PRODUCTS if tag in row[7]]
        assert collection_titles(handle) == expected, handle


def test_collection_documents_render_on_the_server():
    """The served collection documents already carry titles and live prices."""
    luggage = unescape(fetch_document("/collections/luggage").text)
    for row in PRODUCTS:
        if row[2] == "luggage":
            assert row[1] in luggage, f"{row[1]} is missing from the served luggage document"
    assert money(17900) in luggage and money(59900) in luggage, "live prices are missing"
    everything = unescape(fetch_document("/collections/all").text)
    for row in PRODUCTS[:PAGE_SIZE]:
        assert row[1] in everything, f"{row[1]} is missing from the served all document"


def test_collection_sorts_follow_the_rules():
    """featured, best-selling, the two price sorts and newest order as stated, ties by position."""
    reads = {r["handle"]: r for r in all_products()}
    position = {row[0]: i for i, row in enumerate(PRODUCTS)}
    launched = {row[0]: row[12] for row in PRODUCTS}
    handles = [row[0] for row in PRODUCTS]

    def titles(order):
        return [reads[h]["title"] for h in order]

    expected = {
        "featured": handles,
        "best-selling": sorted(handles, key=lambda h: (-reads[h]["units_sold"], position[h])),
        "price-asc": sorted(handles, key=lambda h: (lowest_live_price(reads[h]), position[h])),
        "price-desc": sorted(handles, key=lambda h: (-lowest_live_price(reads[h]), position[h])),
        "newest": sorted(handles, key=lambda h: (-int(launched[h].replace("-", "")), position[h])),
    }
    assert set(expected) == set(SORTS)
    for sort, order in expected.items():
        assert collection_titles("all", sort=sort) == titles(order), f"sort {sort}"
    assert collection_titles("all") == titles(handles), "featured is the default"
    assert collection_titles("luggage", sort="price-desc")[0] == PRICE_DESC_FIRST
    assert collection_titles("all", sort="best-selling")[:2] == list(BEST_SELLING_FIRST)


def test_unknown_sort_is_rejected():
    """A sort outside the five is a client error with a reason."""
    with api() as client:
        response = client.get("/collections/luggage/products", params={"sort": "cheapest"})
    assert is_client_error(response), describe(response, "an unknown sort is rejected")
    assert error_of(response) and message_of(response), describe(response, "error and message")


def test_filters_combine_across_groups():
    """Groups combine with and, values within a group with or, and total counts survivors."""
    pink_cabin = collection_page("luggage", size="cabin", colour="pink")
    assert [c["title"] for c in pink_cabin["products"]] == list(CABIN_PINK), pink_cabin
    assert pink_cabin["total"] == len(CABIN_PINK)
    both = collection_page("luggage", size=["cabin", "trunk"])
    expected = [row[1] for row in PRODUCTS if row[2] == "luggage" and row[4] in ("cabin", "trunk")]
    assert [c["title"] for c in both["products"]] == expected and both["total"] == len(expected)
    names = {code: family for _n, code, family in COLOURWAYS}
    colours = [row[1] for row in PRODUCTS if row[2] == "luggage" and row[4] == "cabin"
               and {names[c] for c in row[14]} & {"pink", "green"}]
    mixed = collection_page("luggage", size="cabin", colour=["pink", "green"])
    assert [c["title"] for c in mixed["products"]] == colours, mixed


def test_colour_filter_matches_families():
    """A colour family keeps products with any colourway in it."""
    names = {code: family for _n, code, family in COLOURWAYS}
    for family in sorted({f for _n, _c, f in COLOURWAYS}):
        expected = [row[1] for row in PRODUCTS if family in {names[c] for c in row[14]}]
        assert collection_titles("all", colour=family) == expected, family


def test_price_range_includes_both_ends():
    """price_min and price_max compare the lowest live price, ends included."""
    wallets = collection_page("wallets", price_min=4000, price_max=5000)
    assert [c["title"] for c in wallets["products"]] == [WALLETS_RANGE], wallets
    exact = collection_page("wallets", price_min=4900, price_max=4900)
    assert [c["title"] for c in exact["products"]] == [WALLETS_RANGE], exact
    reads = all_products()
    expected = [r["title"] for r in reads if 17900 <= lowest_live_price(r) <= 22900]
    assert collection_titles("all", price_min=17900, price_max=22900) == expected


def test_in_stock_filter_keeps_stocked_products():
    """in_stock=true drops a product whose every colourway is sold out."""
    sku = "STR-CVR-NSH"
    before = stock_of(sku)
    try:
        set_stock(sku, 0)
        titles = collection_titles("accessories", in_stock="true")
        assert "Stretch Luggage Cover" not in titles, titles
        assert "Travel Pillow" in titles, titles
        assert "Stretch Luggage Cover" in collection_titles("accessories"), "the filter is opt-in"
    finally:
        set_stock(sku, before)


def test_paging_continues_a_sorted_filtered_list():
    """Page 2 of a sorted, filtered collection continues where page 1 stopped."""
    first = collection_page("on-sale", sort="price-asc", page=1)
    second = collection_page("on-sale", sort="price-asc", page=2)
    joined = card_handles(first["products"]) + card_handles(second["products"])
    assert len(joined) == len(set(joined)) == ON_SALE_TOTAL, joined
    reads = {h: product(h) for h in joined}
    prices = [lowest_live_price(reads[h]) for h in joined]
    assert prices == sorted(prices), prices
    filtered = collection_titles("all", colour="black", sort="newest")
    one = collection_page("all", colour="black", sort="newest", page=1)
    two = collection_page("all", colour="black", sort="newest", page=2)
    assert [c["title"] for c in one["products"] + two["products"]] == filtered[:48]


def test_card_links_carry_the_chosen_colourway(page):
    """A card title links to /products/<handle>?sku=<sku> for the chosen colourway."""
    open_page(page, "/collections/luggage")

    def hrefs():
        found = page.evaluate(
            "() => Array.from(document.querySelectorAll('a[href*=\"?sku=\"]'))"
            ".map(a => a.getAttribute('href'))")
        return found if found else None

    found = [app_path(h) for h in poll_until(hrefs) or []]
    assert "/products/passage-luggage-cabin?sku=PSG-CAB-OLV" in found, found[:10]
    assert "/products/meridian-luggage-cabin?sku=MRD-CAB-HTG" in found, found[:10]


def test_failed_load_more_keeps_the_cards(page):
    """A failed next page keeps the cards shown and adds a Try again row."""
    open_page(page, "/collections/on-sale")
    assert poll_until(lambda: len(product_handles_shown(page)) >= PAGE_SIZE), "page 1 did not load"
    before = product_handles_shown(page)
    page.route(lambda url: "/api/collections/on-sale/products" in url and "page=2" in url,
               lambda route: route.abort())
    page.get_by_text("Load more", exact=True).first.click()
    assert poll_until(lambda: "Try again" in page_text(page)), "no Try again row after a failed load"
    assert product_handles_shown(page)[:len(before)] == before, "the loaded cards were cleared"


def test_product_detail_lists_variants_in_order():
    """Every product lists its colourways in table order, each identified by its sku."""
    for read, row in zip(all_products(), PRODUCTS):
        skus = [v["sku"] for v in read["variants"]]
        assert skus == [f"{row[13]}-{code}" for code in row[14]], f"{row[0]}: {skus}"
        assert len(skus) >= 1


def test_product_detail_carries_its_fields():
    """The product read carries the named fields, and each variant its own."""
    for read in all_products():
        for field in ("handle", "title", "category", "line", "size_class", "bag_type", "badge",
                      "personalisable", "units_sold", "weight_kg", "capacity_litres",
                      "dimensions", "description", "variants", "siblings"):
            assert field in read, f"{read.get('handle')} lacks {field}"
        for item in read["variants"]:
            for field in ("sku", "colourway", "colour_family", "swatch", "price", "list_price",
                          "discount_percent", "on_sale", "stock", "in_stock", "badge", "media"):
                assert field in item, f"{item.get('sku')} lacks {field}"
        assert "discountPercent" not in read["variants"][0], "field names are exact"


def test_product_siblings_are_the_line_sizes():
    """Siblings are the other same-line products sized cabin, check-in, check-in-large or set."""
    for read, row in zip(all_products(), PRODUCTS):
        expected = {r[0] for r in PRODUCTS
                    if r[3] and r[3] == row[3] and r[0] != row[0] and r[4] in SIBLING_SIZES}
        found = {s["handle"] for s in read["siblings"]}
        assert found == expected, f"{row[0]} siblings {found} != {expected}"
        for entry in read["siblings"]:
            assert {"handle", "title", "size_class"} <= set(entry), entry
    passage = {s["handle"] for s in product("passage-luggage-cabin")["siblings"]}
    assert passage == {"passage-luggage-medium", "passage-luggage-large", "passage-luggage-set-of-3"}


def test_discount_percent_is_derived():
    """discount_percent is the rounded share between the two live prices."""
    for price, list_price, percent in DISCOUNT_EXAMPLES:
        assert discount_percent(price, list_price) == percent
    for read in all_products():
        for item in read["variants"]:
            expected = discount_percent(int(item["price"]), int(item["list_price"]))
            assert item["discount_percent"] == expected, item["sku"]
    assert variant("PSG-CAB-OLV")["discount_percent"] == 40
    assert variant("MRD-CAB-STB")["discount_percent"] == 33
    assert variant("PSG-SET-NSH")["discount_percent"] == 45
    assert variant("TRV-PLW-HTG")["discount_percent"] == 0


def test_colourway_badges_follow_the_order():
    """sold-out beats the product badge, and a colourway reads at most one badge."""
    for read, row in zip(all_products(), PRODUCTS):
        assert (read["badge"] or None) == row[8], row[0]
        for item in read["variants"]:
            expected = BADGE_SOLD_OUT if int(item["stock"]) == 0 else row[8]
            assert (item["badge"] or None) == expected, f"{item['sku']} badge {item['badge']!r}"
            assert isinstance(item["badge"], (str, type(None))), item["sku"]
    assert {row[8] for row in PRODUCTS if row[8]} == set(BADGES)
    cabin = {v["sku"]: v["badge"] for v in product("passage-luggage-cabin")["variants"]}
    assert cabin.pop("PSG-CAB-CSP") == BADGE_SOLD_OUT and set(cabin.values()) == {"hot"}, cabin
    assert variant("VLT-CSE-NSH")["badge"] == BADGE_SOLD_OUT


def test_luggage_dimensions_follow_the_size_class():
    """Weight, capacity and dimensions follow the size class; sets sum their pieces."""
    for read, row in zip(all_products(), PRODUCTS):
        if row[2] != "luggage":
            continue
        if row[0] in SET_HANDLES_OF_3:
            weight, capacity, dims = SET_OF_3_FIGURES
        elif row[0] == SET_HANDLE_OF_2:
            weight, capacity, dims = SET_OF_2_FIGURES
        else:
            weight, capacity, dims = SIZE_FIGURES[row[4]]
        assert abs(float(read["weight_kg"]) - float(weight)) < 0.001, (row[0], read["weight_kg"])
        assert float(read["capacity_litres"]) == float(capacity), (row[0], read["capacity_litres"])
        assert read["dimensions"] == dims, (row[0], read["dimensions"])


def test_media_lists_four_views_with_alt_text():
    """Each colourway lists four image shots at positions 1 to 4 naming product and colourway."""
    for read in all_products():
        for item in read["variants"]:
            shots = sorted(item["media"], key=lambda m: m["position"])
            assert [m["position"] for m in shots] == [1, 2, 3, 4], item["sku"]
            for shot in shots:
                assert shot["kind"] == MEDIA_KIND_IMAGE, shot
                assert read["title"] in shot["alt"] and item["colourway"] in shot["alt"], shot
    first = sorted(variant("PSG-CAB-OLV")["media"], key=lambda m: m["position"])[0]
    assert first["alt"] == ALT_EXAMPLE, first


def test_only_luggage_is_personalisable():
    """personalisable is true on luggage and false on everything else."""
    for read in all_products():
        assert read["personalisable"] is (read["category"] == "luggage"), read["handle"]


def test_price_exception_on_static_blue():
    """MRD-CAB-STB carries its own price; its siblings keep the product price."""
    cabin = {v["sku"]: v for v in product("meridian-luggage-cabin")["variants"]}
    for sku, item in cabin.items():
        expected = PRICE_EXCEPTIONS.get(sku, (17900, 29900))
        assert (item["price"], item["list_price"]) == expected, sku
    assert (cabin["MRD-CAB-STB"]["price"], cabin["MRD-CAB-STB"]["list_price"]) == (19900, 29900)


def test_swatches_carry_names_with_pressed_state(page):
    """Swatch discs are named buttons in a group named for the product, one pressed."""
    titles = {row[1] for row in PRODUCTS}
    names = {name for name, _c, _f in COLOURWAYS}
    for path in ("/collections/luggage", "/products/meridian-luggage-cabin"):
        open_page(page, path)
        poll_until(lambda: page.locator("[role=group][aria-label]").count())
        groups = page.locator("[role=group][aria-label]")
        assert groups.count() >= 1, f"no swatch group on {path}"
        for index in range(min(groups.count(), 8)):
            group = groups.nth(index)
            label = group.get_attribute("aria-label")
            if label not in titles:
                continue
            discs = group.locator("button[aria-label]")
            assert discs.count() >= 1, f"{label} group has no disc buttons"
            pressed = []
            for d in range(discs.count()):
                disc = discs.nth(d)
                assert disc.get_attribute("aria-label") in names, disc.get_attribute("aria-label")
                assert disc.get_attribute("aria-pressed") in ("true", "false"), label
                if disc.get_attribute("aria-pressed") == "true":
                    pressed.append(disc.get_attribute("aria-label"))
            assert len(pressed) == 1, f"{label} has {len(pressed)} pressed discs"
        assert any(groups.nth(i).get_attribute("aria-label") in titles
                   for i in range(groups.count())), f"no group on {path} is named for a product"


def test_drawn_pictures_carry_alternative_text(page):
    """Drawn pictures are role=img with an aria-label naming product and colourway."""
    open_page(page, "/products/passage-luggage-cabin")
    poll_until(lambda: page.locator("[role=img][aria-label]").count())
    labels = page.eval_on_selector_all(
        "[role=img]", "els => els.map(e => e.getAttribute('aria-label') || '')")
    assert labels and all(label.strip() for label in labels), labels
    assert any("Passage Luggage - Cabin" in label and OLIVE in label for label in labels), labels
    open_page(page, "/collections/wallets")
    poll_until(lambda: page.locator("[role=img][aria-label]").count())
    labels = page.eval_on_selector_all(
        "[role=img]", "els => els.map(e => e.getAttribute('aria-label') || '')")
    assert any("Vault Card Case" in label for label in labels), labels
    for path in ("/", "/collections/luggage", "/products/passage-luggage-cabin", "/cart"):
        open_page(page, path)
        settle()
        labels = page.eval_on_selector_all(
            "[role=img]", "els => els.map(e => e.getAttribute('aria-label') || '')")
        assert all(label.strip() for label in labels), f"an unlabelled drawn picture on {path}"
        assert unnamed_controls(page) == [], f"icon-only controls without a name on {path}"
    open_page(page, "/")
    home_labels = " ".join(page.eval_on_selector_all(
        "main [role=img]", "els => els.map(e => e.getAttribute('aria-label') || '')"))
    assert poll_until(lambda: len(product_handles_shown(page)) >= 1), "the home grid did not load"
    assert len(home_labels) > 0, "the home page carries no labelled drawn picture"


def test_seeded_products_match_the_table():
    """The thirty-nine products carry the table's identity, axes and figures."""
    for read, row in zip(all_products(), PRODUCTS):
        handle = row[0]
        assert (read["handle"], read["title"], read["category"]) == (handle, row[1], row[2])
        assert (read.get("line") or "").lower() == (row[3] or "").lower(), handle
        assert (read["size_class"] or None) == (row[4] if row[2] == "luggage" else None), handle
        assert (read["bag_type"] or None) == row[5], handle
        assert (read["badge"] or None) == row[8], handle
        plain = [v for v in read["variants"] if v["sku"] not in PRICE_EXCEPTIONS]
        assert all((v["price"], v["list_price"]) == (row[9], row[10]) for v in plain), handle
        assert read["units_sold"] == row[11] + units_since_start(handle), handle
    launched = {r["handle"]: str(r["launched_on"])[:10]
                for r in sql("SELECT handle, launched_on FROM product")}
    assert launched == {row[0]: row[12] for row in PRODUCTS}, launched
    for use in USES:
        assert collection_titles(use) == [row[1] for row in PRODUCTS if use in row[6]], use
    assert collection_titles("clearance-sale") == [row[1] for row in PRODUCTS if "clearance" in row[7]]


def test_colourway_families_match_the_table():
    """The thirteen colourways carry their names and families wherever they appear."""
    by_code = {code: (name, family) for name, code, family in COLOURWAYS}
    seen = set()
    for read in all_products():
        for item in read["variants"]:
            code = item["sku"].rsplit("-", 1)[1]
            assert (item["colourway"], item["colour_family"]) == by_code[code], item["sku"]
            seen.add(code)
    assert seen == set(by_code), seen


def test_swatches_are_hex_strings():
    """Every swatch is a #RRGGBB string."""
    for read in all_products():
        for item in read["variants"]:
            assert re.fullmatch(r"#[0-9A-Fa-f]{6}", str(item["swatch"])), item["sku"]


def test_skus_follow_the_prefix_code_scheme():
    """A sku is the product prefix, a hyphen and the colourway code."""
    codes = {code for _n, code, _f in COLOURWAYS}
    for read, row in zip(all_products(), PRODUCTS):
        for item in read["variants"]:
            prefix, code = item["sku"].rsplit("-", 1)
            assert prefix == row[13] and code in codes, item["sku"]
    assert variant("PSG-CAB-OLV")["colourway"] == OLIVE


def test_prices_are_integer_cents():
    """Every amount is an integer number of cents in usd."""
    for read in all_products():
        for item in read["variants"]:
            for field in ("price", "list_price"):
                assert type(item[field]) is int, f"{item['sku']} {field} {item[field]!r}"
    assert variant("PSG-CAB-OLV")["price"] == 17900 and money(17900) == "$179"
    cart_token = filled_cart([("PCK-CUB-HTG", 1)])
    current = cart(cart_token)
    assert current["currency"] == CURRENCY, current
    for field in ("subtotal", "discount", "delivery", "total"):
        assert type(current[field]) is int, f"cart {field} {current[field]!r}"
    currencies = sql("SELECT DISTINCT lower(currency) AS c FROM orders")
    assert {r["c"] for r in currencies} <= {CURRENCY}, currencies


def test_catalogue_rows_are_stored():
    """The catalogue tables hold the categories, collections, products, colourways and media."""
    expectations = {
        "category": ("handle", "name", "position"),
        "collection": ("handle", "name", "kind", "rule", "strapline", "position"),
        "product": ("handle", "title", "category_id", "line", "size_class", "bag_type", "uses",
                    "tags", "badge", "personalisable", "weight_kg", "capacity_litres",
                    "dimensions", "description", "seed_units_sold", "launched_on", "position",
                    "published"),
        "variant": ("product_id", "sku", "colourway", "colour_family", "swatch", "price",
                    "list_price", "position"),
        "media": ("variant_id", "kind", "position", "alt"),
    }
    for table, columns in expectations.items():
        present = table_columns(table)
        missing = [c for c in columns if c not in present]
        assert not missing, f"{table} lacks {missing}"
    assert scalar("SELECT count(*) FROM category") == len(CATEGORY_HANDLES)
    assert scalar("SELECT count(*) FROM collection") == len(COLLECTIONS)
    assert scalar("SELECT count(*) FROM product") == len(PRODUCTS)
    assert scalar("SELECT count(*) FROM variant") == VARIANT_COUNT
    kinds = {r["kind"] for r in sql("SELECT DISTINCT kind FROM collection")}
    assert kinds == set(COLLECTION_KINDS), kinds
    media_kinds = {r["kind"] for r in sql("SELECT DISTINCT kind FROM media")}
    assert media_kinds <= set(MEDIA_KINDS) and MEDIA_KIND_IMAGE in media_kinds, media_kinds
    assert scalar("SELECT count(*) FROM media WHERE kind = 'image'") == VARIANT_COUNT * 4


def test_seeded_stock_matches_the_table():
    """Each colourway opened at 20 units unless the table names an exception."""
    token = owner_token()
    for _handle, sku, _name, _family, _price, _list, table_stock in pinned_variants():
        rows = movements(sku, token)
        assert rows, f"{sku} has no movements"
        opening = rows[0]
        assert opening["kind"] == MOVE_RESTOCK, f"{sku} opens with {opening}"
        seeded_sales = [m for m in rows if m["kind"] == MOVE_SALE and m.get("order_number") in SEED_NUMBERS]
        opened = int(opening["delta"]) + sum(int(m["delta"]) for m in seeded_sales)
        assert opened == table_stock, f"{sku} opened at {opened}, not {table_stock}"
        assert table_stock == STOCK_EXCEPTIONS.get(sku, DEFAULT_STOCK)
    for sku, units in STOCK_EXCEPTIONS.items():
        assert stock_of(sku) == units, f"{sku} holds {stock_of(sku)}, not {units}"
        assert isinstance(variant(sku)["stock"], int)


def test_sale_is_active_with_road_week():
    """Road Week is active, ends at 00:00 UTC seven days after first start, and prices hold."""
    current = sale()
    for field in ("name", "ends_at", "active", "server_time"):
        assert field in current, f"the sale lacks {field}"
    assert current["name"] == SALE_NAME and current["active"] is True, current
    ends = parse_stamp(current["ends_at"])
    assert (ends.hour, ends.minute, ends.second) == (0, 0, 0), current["ends_at"]
    started = scalar("SELECT min(created_at) FROM account")
    assert (ends.date() - started.date()).days == 7, (ends, started)
    assert parse_stamp(current["server_time"]) < ends, current
    columns = table_columns("sale")
    assert {"name", "ends_at"} <= columns, columns
    for row in PRODUCTS[:6]:
        read = product(row[0])
        plain = [v for v in read["variants"] if v["sku"] not in PRICE_EXCEPTIONS]
        assert all(v["price"] == row[9] and v["on_sale"] == (row[9] < row[10]) for v in plain), row[0]


def test_sale_end_reprices_the_cart_at_checkout():
    """After ends_at every read and checkout uses the list price, and moving it back restores the sale."""
    owner = owner_token()
    original = sale()["ends_at"]
    sku, subtotal, discount, total, shown = ENDED_SALE_EXAMPLE
    ensure_stock([sku])
    cart_token = filled_cart([(sku, 1)])
    assert cart(cart_token)["lines"][0]["unit_price"] == 59900
    try:
        moved = move_sale_end(owner, iso_from_now(-60))
        assert accepted(moved), describe(moved, "the owner moves the end of the sale")
        assert sale()["active"] is False, "the sale reads ended on the very next read"
        ended = variant(sku)
        assert (ended["price"], ended["discount_percent"], ended["on_sale"]) == (109900, 0, False)
        for read in all_products():
            for item in read["variants"]:
                assert item["price"] == item["list_price"], item["sku"]
        assert collection_page("on-sale")["total"] == 0
        served = unescape(fetch_document("/collections/luggage").text)
        assert money(109900) in served and money(59900) not in served, "stale sale price served"
        stock_before, orders_before = stock_of(sku), order_count()
        key = checkout_key()
        email = probe_address(unique_suffix())
        refused = checkout(cart_token, key=key, email=email)
        assert is_client_error(refused), describe(refused, "a changed price refuses the checkout")
        assert error_of(refused) == ERR_PRICE_CHANGED, describe(refused, "price_changed")
        assert message_of(refused) == MSG_PRICE_CHANGED, describe(refused, "the price message")
        assert cart(cart_token)["lines"][0]["unit_price"] == 109900, "lines take the live price"
        assert orders_for_key(key) == 0 and order_count() == orders_before
        assert stock_of(sku) == stock_before
        retried = checkout(cart_token, email=email)
        assert retried.status_code in (200, 201), describe(retried, "the second submission proceeds")
        order = retried.json()
        assert (order["subtotal"], order["discount"], order["delivery"], order["total"]) == (
            subtotal, discount, 0, total), order
        rows = wait_for_mail(email)
        assert rows and mail_text(rows[0]).strip().startswith(
            f"Order {order['number']}, total charged {shown}."), "the email charges $1,099"
    finally:
        restored = move_sale_end(owner, original)
        assert accepted(restored), describe(restored, "the owner moves the sale end back")
    assert sale()["active"] is True
    assert variant(sku)["price"] == 59900, "moving ends_at forward brings the sale price back"


def test_countdown_ignores_the_visitor_clock(page):
    """The countdown reads ends_at and server_time, not the visitor's clock."""
    current = sale()
    page.clock.install(time=clock_offset_time(3))
    open_page(page, "/products/passage-luggage-cabin")
    poll_until(lambda: page.locator("[data-ends-at]").count())
    holder = page.locator("[data-ends-at]").first
    assert parse_stamp(holder.get_attribute("data-ends-at")) == parse_stamp(current["ends_at"])
    units = page.eval_on_selector_all("[data-unit]", "els => els.map(e => e.getAttribute('data-unit'))")
    assert sorted(set(units)) == ["d", "h", "m", "s"], units
    shown = countdown_seconds(page)
    expected = seconds_until(current["ends_at"], sale()["server_time"])
    assert abs(shown - expected) <= 180, f"countdown shows {shown}s, the server says {expected}s"


def test_offer_strip_expires_on_the_product_page(page):
    """At zero the offer strip leaves, prices are read again and the ticker hides."""
    owner = owner_token()
    original = sale()["ends_at"]
    try:
        moved = move_sale_end(owner, iso_from_now(25))
        assert accepted(moved), describe(moved, "the owner moves the end of the sale")
        open_page(page, "/products/passage-luggage-cabin")
        assert poll_until(lambda: "Sale Extended! Ends in" in page_text(page)), "no offer strip"
        assert money(17900) in page_text(page), "the sale price shows while the sale runs"

        def expired():
            text = page_text(page)
            return "Sale Extended! Ends in" not in text and money(17900) not in text
        assert poll_until(expired, timeout=SALE_WAIT_SECONDS), "the offer strip outlived the sale"
        assert money(29900) in page_text(page), "the list price is the live price after the sale"
        open_page(page, "/")
        assert "LIVE NOW" not in page_text(page), "the ticker shows after the sale ended"
    finally:
        restored = move_sale_end(owner, original)
        assert accepted(restored), describe(restored, "the owner moves the sale end back")
    open_page(page, "/")
    assert poll_until(lambda: "LIVE NOW" in page_text(page)), "the ticker returns with the sale"


def test_units_sold_counts_paid_orders_only():
    """units_sold adds paid units since first start and drops a cancelled order."""
    handle = "travel-pillow"
    before = product(handle)["units_sold"]
    order = place_order([("TRV-PLW-HTG", 2)])
    assert product(handle)["units_sold"] == before + 2
    with api(owner_token()) as client:
        cancelled = client.post(f"/owner/orders/{order['number']}/cancel")
    assert accepted(cancelled), describe(cancelled, "the owner cancels a paid order")
    assert product(handle)["units_sold"] == before
    assert product(handle)["units_sold"] == product_row(handle)[11] + units_since_start(handle)


def test_concurrent_checkouts_sell_the_last_unit_once():
    """Two checkouts for the last unit: one paid order, one out_of_stock, stock at zero."""
    sku = "RDG-TRL-SFL"
    try:
        set_stock(sku, 1)
        carts = [filled_cart([(sku, 1)]), filled_cart([(sku, 1)])]
        keys = [checkout_key(), checkout_key()]
        results = run_together(lambda: checkout(carts[0], key=keys[0]),
                               lambda: checkout(carts[1], key=keys[1]))
        winners = [r for r in results if r.status_code in (200, 201)]
        losers = [r for r in results if is_client_error(r)]
        assert len(winners) == 1 and len(losers) == 1, [describe(r, "race") for r in results]
        assert winners[0].json()["state"] == STATE_PAID
        assert error_of(losers[0]) == ERR_OUT_OF_STOCK, describe(losers[0], "out_of_stock")
        assert body_of(losers[0]).get("sku") == sku, describe(losers[0], "the refusal names the sku")
        assert stock_of(sku) == 0 and movement_sum(sku) == 0, "the last unit sold more than once"
        loser_cart = carts[results.index(losers[0])]
        assert cart(loser_cart)["lines"][0]["sold_out"] is True, "the losing line is sold_out"
        assert orders_for_key(keys[results.index(losers[0])]) == 0
    finally:
        set_stock(sku, STOCK_EXCEPTIONS[sku])
    assert stock_of(sku) >= 0


def test_repeated_checkout_key_returns_one_order():
    """The same checkout_key twice is one order, one movement, one account and one email."""
    ensure_stock(["PCK-CUB-HTG"])
    email = probe_address(unique_suffix())
    cart_token = filled_cart([("PCK-CUB-HTG", 1)])
    key = checkout_key()
    first = checkout(cart_token, key=key, email=email)
    second = checkout(cart_token, key=key, email=email)
    assert first.status_code in (200, 201), describe(first, "the first attempt is accepted")
    assert second.status_code in (200, 201), describe(second, "the repeat answers the order")
    number = first.json()["number"]
    assert second.json()["number"] == number
    assert orders_for_key(key) == 1
    row = order_row(number)
    assert scalar("SELECT count(*) FROM stock_movement WHERE order_id = %s", row["id"]) == 1
    assert kb_account(external_key(number)).status_code == 200
    wait_for_mail(email)
    for _ in range(6):
        settle()
    assert len(mail_to(email)) == 1, "a repeated checkout sent a second email"


def test_simultaneous_checkout_repeats_make_one_order():
    """Three simultaneous submissions of one key still make one order."""
    ensure_stock(["PCK-CUB-SSU"])
    cart_token = filled_cart([("PCK-CUB-SSU", 1)])
    key = checkout_key()
    email = probe_address(unique_suffix())
    results = run_together(*[lambda: checkout(cart_token, key=key, email=email) for _ in range(3)])
    numbers = {r.json()["number"] for r in results if r.status_code in (200, 201)}
    assert len(numbers) == 1, [describe(r, "repeat") for r in results]
    assert all(r.status_code < 500 for r in results), [r.status_code for r in results]
    assert orders_for_key(key) == 1


def test_provider_refuses_a_reused_external_key():
    """killbill answers 201 for a new key, 409 for a held one, 200 or 404 on lookup."""
    order = place_order([("PCK-CUB-HTG", 1)])
    key = external_key(order["number"])
    reused = kb_open_account(key, "Probe Reuse", probe_address(unique_suffix()))
    assert reused.status_code == 409, describe(reused, "a held externalKey is refused")
    fresh_key = "probe-" + unique_suffix()
    created = kb_open_account(fresh_key, "Probe Fresh", probe_address(unique_suffix()))
    assert created.status_code == 201, describe(created, "a new externalKey is created")
    assert kb_account(fresh_key).status_code == 200
    assert kb_account("probe-missing-" + unique_suffix()).status_code == 404


def test_concurrent_movement_with_checkout_never_overdraws():
    """A checkout and an owner adjustment racing for one unit never take stock below zero."""
    sku = "SWV-BPK-FLA"
    before = stock_of(sku)
    try:
        set_stock(sku, 1)
        cart_token = filled_cart([(sku, 1)])
        results = run_together(lambda: checkout(cart_token),
                               lambda: record_movement(sku, -1, MOVE_ADJUSTMENT))
        assert all(r.status_code < 500 for r in results), [describe(r, "race") for r in results]
        winners = sum(1 for r in results if accepted(r))
        assert winners <= 1, [describe(r, "race") for r in results]
        assert stock_of(sku) == 1 - winners and stock_of(sku) >= 0
        assert movement_sum(sku) == stock_of(sku)
    finally:
        set_stock(sku, before)


def test_checkout_refuses_more_than_the_stock():
    """A line above the stock is refused with out_of_stock and nothing is written."""
    sku = "CST-LRG-NSH"
    before = stock_of(sku)
    try:
        set_stock(sku, 2)
        cart_token = filled_cart([(sku, 2)])
        set_stock(sku, 1)
        orders_before, moves_before = order_count(), movement_count()
        key = checkout_key()
        refused = checkout(cart_token, key=key)
        assert is_client_error(refused), describe(refused, "the checkout is refused")
        assert error_of(refused) == ERR_OUT_OF_STOCK and body_of(refused).get("sku") == sku
        assert message_of(refused) == only_left(1), describe(refused, "the cart-rule message")
        assert order_count() == orders_before and movement_count() == moves_before
        assert orders_for_key(key) == 0
        orphans = scalar("SELECT count(*) FROM orders o WHERE NOT EXISTS "
                         "(SELECT 1 FROM order_line l WHERE l.order_id = o.id)")
        loose = scalar("SELECT count(*) FROM stock_movement WHERE kind IN ('sale', "
                       "'cancellation') AND order_id IS NULL")
        assert orphans == 0 and loose == 0, (orphans, loose)
    finally:
        set_stock(sku, before)


def test_sold_out_line_is_marked_in_the_cart(page):
    """A line that sold out during checkout reads SOLD OUT with unavailable quantity controls."""
    sku = "CST-MED-SFL"
    before = stock_of(sku)
    ensure_stock([sku], 2)
    open_page(page, "/products/coastal-luggage-medium?sku=" + sku)
    page.get_by_role("button", name="ADD TO CART").first.click()
    cart_token = poll_until(lambda: cart_token_in_page(page, sku))
    assert cart_token, "the page's cart token could not be found in its storage or cookies"
    try:
        set_stock(sku, 0)
        refused = checkout(cart_token)
        assert is_client_error(refused) and error_of(refused) == ERR_OUT_OF_STOCK, describe(
            refused, "the sold-out checkout is refused")
        open_page(page, "/cart")
        assert poll_until(lambda: "SOLD OUT" in page_text(page)), "the cart line is not marked SOLD OUT"
        disabled = page.locator("main button:disabled, main [aria-disabled=true], main input:disabled")
        assert disabled.count() >= 1, "the sold-out line keeps live quantity controls"
    finally:
        set_stock(sku, before)


def test_stock_ceiling_refuses_the_extra_units():
    """An add or change past the stock is refused with the available count."""
    sku = "CTR-CAB-CSP"
    cart_token = new_cart()
    over = add_line(cart_token, sku, 3)
    assert is_client_error(over), describe(over, "three of two is refused")
    assert error_of(over) == ERR_INSUFFICIENT and body_of(over).get("available") == 2
    assert message_of(over) == MSG_TWO_LEFT == only_left(2)
    assert cart(cart_token)["lines"] == []
    assert accepted(add_line(cart_token, sku, 1))
    line = cart(cart_token)["lines"][0]
    raised = change_line(cart_token, line["id"], 3)
    assert is_client_error(raised) and error_of(raised) == ERR_INSUFFICIENT
    again = add_line(cart_token, sku, 2)
    assert is_client_error(again), describe(again, "1 + 2 of 2 is refused")
    assert cart(cart_token)["lines"][0]["quantity"] == 1, "the line keeps its quantity"


def test_stock_bound_is_read_at_every_change():
    """A change is checked against the stock at that moment, not the stock at add."""
    sku = "CTR-MED-FLA"
    before = stock_of(sku)
    try:
        set_stock(sku, 3)
        cart_token = filled_cart([(sku, 2)])
        set_stock(sku, 1)
        line = cart(cart_token)["lines"][0]
        changed = change_line(cart_token, line["id"], 2)
        assert is_client_error(changed), describe(changed, "the change reads the live stock")
        assert body_of(changed).get("available") == 1
        added = add_line(cart_token, sku, 1)
        assert is_client_error(added), describe(added, "the add reads the live stock")
    finally:
        set_stock(sku, before)


def test_sold_out_colourway_is_refused():
    """A colourway with no stock is refused with the sold-out message."""
    cart_token = new_cart()
    refused = add_line(cart_token, "PSG-CAB-CSP", 1)
    assert is_client_error(refused), describe(refused, "a sold-out colourway is refused")
    assert error_of(refused) == ERR_INSUFFICIENT and body_of(refused).get("available") == 0
    assert message_of(refused) == MSG_SOLD_OUT
    assert cart(cart_token)["lines"] == []


def test_cart_quantity_must_be_positive():
    """A quantity below one is invalid, on add and on change."""
    cart_token = new_cart()
    for bad in (0, -1, 1.5):
        response = add_line(cart_token, "PCK-CUB-HTG", bad)
        assert is_client_error(response), describe(response, f"quantity {bad} is invalid")
    assert accepted(add_line(cart_token, "PCK-CUB-HTG", 1))
    line = cart(cart_token)["lines"][0]
    zero = change_line(cart_token, line["id"], 0)
    assert is_client_error(zero), describe(zero, "a change to 0 is invalid")
    assert cart(cart_token)["lines"][0]["quantity"] == 1


def test_unknown_sku_is_rejected():
    """An unknown sku is a client error and the cart stays empty."""
    cart_token = new_cart()
    response = add_line(cart_token, "ZZZ-ZZZ-ZZZ", 1)
    assert is_client_error(response), describe(response, "an unknown sku is rejected")
    assert error_of(response) and message_of(response)
    assert cart(cart_token)["lines"] == []


def test_line_colourway_never_changes():
    """A line's sku cannot be switched by a change."""
    cart_token = filled_cart([("PCK-CUB-HTG", 1)])
    line = cart(cart_token)["lines"][0]
    with api() as client:
        client.patch(f"/carts/{cart_token}/lines/{line['id']}", json={"quantity": 2, "sku": "PCK-CUB-SSU"})
    after = cart(cart_token)["lines"]
    assert [entry["sku"] for entry in after] == ["PCK-CUB-HTG"], after


def test_cart_add_holds_no_stock():
    """Adding to a cart leaves the stock where it was."""
    sku = "KTL-BPK-HTG"
    ensure_stock([sku])
    before = stock_of(sku)
    filled_cart([(sku, 3)])
    assert stock_of(sku) == before and movement_sum(sku) == before


def test_cart_lines_change_then_leave():
    """PATCH changes a line's quantity and DELETE removes it."""
    cart_token = filled_cart([("PCK-CUB-HTG", 1)])
    line = cart(cart_token)["lines"][0]
    changed = change_line(cart_token, line["id"], 2)
    assert accepted(changed), describe(changed, "the quantity changes")
    assert cart(cart_token)["lines"][0]["quantity"] == 2
    removed = remove_line(cart_token, line["id"])
    assert accepted(removed), describe(removed, "the line is removed")
    after = cart(cart_token)
    assert after["lines"] == [] and after["item_count"] == 0, after


def test_adding_the_same_sku_merges_lines():
    """The same sku and properties merge; different properties split."""
    sku = "MRD-CAB-LWR"
    cart_token = new_cart()
    assert accepted(add_line(cart_token, sku, 1)) and accepted(add_line(cart_token, sku, 1))
    lines = cart(cart_token)["lines"]
    assert len(lines) == 1 and lines[0]["quantity"] == 2, lines
    tagged = {"initials": "KR", "placement": "front"}
    assert accepted(add_line(cart_token, sku, 1, tagged))
    assert accepted(add_line(cart_token, sku, 1, tagged))
    lines = cart(cart_token)["lines"]
    assert sorted(entry["quantity"] for entry in lines) == [2, 2] and len(lines) == 2, lines
    columns = table_columns("cart_line")
    for column in ("cart_id", "variant_id", "quantity", "properties", "unit_price_captured", "added_at"):
        assert column in columns, f"cart_line lacks {column}"


def test_cart_summary_is_arithmetic():
    """Line totals, savings and the summary follow the cart rules."""
    cart_token = filled_cart([("PSG-CAB-OLV", 1), ("MNI-SLG-NSH", 2), ("PCK-CUB-HTG", 1)])
    current = cart(cart_token)
    for field in ("token", "lines", "item_count", "subtotal", "discount", "delivery", "total", "currency"):
        assert field in current, f"the cart lacks {field}"
    for line in current["lines"]:
        for field in ("id", "sku", "product_title", "colourway", "size_class", "quantity",
                      "unit_price", "list_price", "line_total", "line_saving", "properties", "sold_out"):
            assert field in line, f"a line lacks {field}"
        assert line["line_total"] == line["unit_price"] * line["quantity"], line
        assert line["line_saving"] == (line["list_price"] - line["unit_price"]) * line["quantity"], line
    assert current["subtotal"] == sum(l["list_price"] * l["quantity"] for l in current["lines"]) == 48600
    assert current["discount"] == sum(l["line_saving"] for l in current["lines"]) == 18000
    assert current["delivery"] == 0
    assert current["total"] == current["subtotal"] - current["discount"] + current["delivery"] == 30600
    assert current["item_count"] == 4 and current["currency"] == CURRENCY


def test_cart_is_created_without_an_account():
    """A signed-out cart has a long random token that is its only key."""
    cart_token = new_cart()
    assert re.fullmatch(r"[A-Za-z0-9]{24,}", cart_token), cart_token
    assert cart(cart_token)["lines"] == []
    row = sql("SELECT * FROM cart WHERE token = %s", cart_token)
    assert row and row[0]["account_id"] is None, row
    wrong = cart_token[:-1] + ("A" if cart_token[-1] != "A" else "B")
    with api() as client:
        assert client.get(f"/carts/{wrong}").status_code == 404


def test_cart_claim_attaches_once():
    """A signed-in claim attaches a signed-out cart; a second account is denied."""
    first = signup(unique_suffix())
    second = signup(unique_suffix())
    cart_token = filled_cart([("PCK-CUB-HTG", 1)])
    with api() as client:
        anonymous = client.post(f"/carts/{cart_token}/claim")
    assert denied(anonymous), describe(anonymous, "a claim needs a session")
    with api(first["token"]) as client:
        claimed = client.post(f"/carts/{cart_token}/claim")
    assert accepted(claimed), describe(claimed, "the first account claims the cart")
    owner_id = sql("SELECT account_id FROM cart WHERE token = %s", cart_token)[0]["account_id"]
    assert owner_id is not None
    with api(second["token"]) as client:
        stolen = client.post(f"/carts/{cart_token}/claim")
    assert is_client_error(stolen), describe(stolen, "another account's cart is denied")
    assert sql("SELECT account_id FROM cart WHERE token = %s", cart_token)[0]["account_id"] == owner_id


def test_signed_in_cart_is_attached_to_the_account():
    """A bearer cart belongs to the account and survives a fresh sign-in."""
    account = signup(unique_suffix())
    with api(account["token"]) as client:
        none_yet = client.get("/me/cart")
    assert none_yet.status_code == 404, describe(none_yet, "no cart with lines yet")
    cart_token = new_cart(account["token"])
    assert sql("SELECT account_id FROM cart WHERE token = %s", cart_token)[0]["account_id"] is not None
    assert accepted(add_line(cart_token, "PCK-CUB-SSU", 2, token=account["token"]))
    fresh = login(account["email"], account["password"])
    with api(fresh) as client:
        mine = client.get("/me/cart")
    assert mine.status_code == 200, describe(mine, "the account's cart is returned")
    assert mine.json()["token"] == cart_token and mine.json()["lines"][0]["quantity"] == 2
    columns = table_columns("cart")
    assert {"token", "account_id", "created_at", "updated_at"} <= columns, columns


def test_invalid_personalisation_is_rejected():
    """Bad placements, lengths, characters or a non-luggage product are invalid."""
    cart_token = new_cart()
    for props in ({"initials": "AB", "placement": "side"}, {"initials": "", "placement": "front"},
                  {"initials": "ABCDEFGH", "placement": "front"}, {"initials": "A!", "placement": "top"}):
        response = add_line(cart_token, "MRD-CAB-NSH", 1, props)
        assert is_client_error(response), describe(response, f"{props} is invalid")
    other = add_line(cart_token, "MNI-SLG-NSH", 1, {"initials": "AB", "placement": "front"})
    assert is_client_error(other), describe(other, "a sling is not personalisable")
    assert cart(cart_token)["lines"] == []
    ok = add_line(cart_token, "MRD-CAB-NSH", 1, {"initials": "abcdefg", "placement": "top"})
    assert accepted(ok), describe(ok, "seven characters are allowed")
    assert cart(cart_token)["lines"][0]["properties"]["initials"] == "ABCDEFG"


def test_other_accounts_order_is_refused_like_a_missing_one(customer, customer2):
    """Another account's order and a missing number get the same status and body."""
    with api(customer2) as client:
        foreign = client.get("/orders/VS-100001")
        missing = client.get("/orders/VS-999999")
    assert denied(foreign), describe(foreign, "another account's order is refused")
    assert (foreign.status_code, foreign.text) == (missing.status_code, missing.text), (
        describe(foreign, "foreign"), describe(missing, "missing"))
    with api(customer) as client:
        other = client.get("/orders/VS-100003")
        absent = client.get("/orders/VS-999998")
    assert denied(other) and (other.status_code, other.text) == (absent.status_code, absent.text)
    assert "Noor Haddad" not in other.text and "9 Birch Court" not in other.text


def test_other_accounts_address_is_not_found(customer, customer2):
    """Another account's address id answers not found and stays as it was."""
    mine = addresses(customer)
    seeded = [a for a in mine if a["line1"] == SEED_ADDRESS[1]]
    assert seeded, f"the seeded address is missing: {mine}"
    target = seeded[0]["id"]
    with api(customer2) as client:
        changed = client.patch(f"/me/addresses/{target}", json={"line1": "1 Stolen Street"})
        removed = client.delete(f"/me/addresses/{target}")
    assert changed.status_code == 404, describe(changed, "another account's address is not found")
    assert removed.status_code == 404, describe(removed, "another account's address is not found")
    after = [a for a in addresses(customer) if a["id"] == target]
    assert after and after[0]["line1"] == SEED_ADDRESS[1], after


def test_guest_order_is_owner_only(customer):
    """A guest order is read only through the owner endpoints."""
    order = place_order([("PCK-CUB-HTG", 1)])
    number = order["number"]
    with api(customer) as client:
        by_customer = client.get(f"/orders/{number}")
        missing = client.get("/orders/VS-999997")
    assert denied(by_customer), describe(by_customer, "a customer cannot read a guest order")
    assert (by_customer.status_code, by_customer.text) == (missing.status_code, missing.text)
    with api() as client:
        anonymous = client.get(f"/orders/{number}")
    assert denied(anonymous), describe(anonymous, "a guest order is not public")
    assert owner_order(number)["number"] == number


def test_order_read_is_refused_without_a_session():
    """An order read without a token is refused and carries no order data."""
    with api() as client:
        response = client.get("/orders/VS-100001")
    assert response.status_code in (401, 403), describe(response, "an order read needs a session")
    assert "PSG-CAB-OLV" not in response.text and "Passage Luggage" not in response.text


def test_signed_out_account_pages_send_to_login(page):
    """A signed-out visit to an account page lands on the sign-in page with next."""
    for path in SIGNED_IN_ROUTES:
        open_page(page, path)
        poll_until(lambda: LOGIN_PATH in page.url)
        parsed = urllib.parse.urlparse(page.url)
        assert parsed.path == LOGIN_PATH, f"{path} landed on {page.url}"
        assert urllib.parse.parse_qs(parsed.query).get("next") == [path], page.url


def test_customer_lists_own_orders_newest_first(customer):
    """/me/orders lists the caller's orders newest first with the summary fields."""
    with api(customer) as client:
        rows = top_level_array(client.get("/me/orders"))
    numbers = [r["number"] for r in rows]
    assert "VS-100001" in numbers and "VS-100002" in numbers, numbers
    assert "VS-100003" not in numbers, numbers
    assert numbers.index("VS-100002") < numbers.index("VS-100001"), numbers
    stamps = [parse_stamp(r["placed_at"]) for r in rows]
    assert stamps == sorted(stamps, reverse=True), numbers
    for row in rows:
        assert {"number", "placed_at", "total", "currency", "state"} <= set(row), row


def test_customer_reads_own_order_with_captured_lines(customer):
    """The placing account reads its order with lines, address, state, window and totals."""
    with api(customer) as client:
        response = client.get("/orders/VS-100001")
    assert response.status_code == 200, describe(response, "the owner of an order reads it")
    order = response.json()
    line = order["lines"][0]
    assert (line["sku"], line["quantity"], line["unit_price"], line["list_price"]) == (
        "PSG-CAB-OLV", 1, 17900, 29900), line
    assert line["product_title"] == "Passage Luggage - Cabin" and line["colourway"] == OLIVE, line
    assert line["size_class"] == "cabin", line
    assert order["address"]["name"] == SEED_ADDRESS[0], order["address"]
    assert order["state"] == STATE_FULFILLED
    assert order["billing_account"] == "valisette-VS-100001"
    assert (order["subtotal"], order["discount"], order["delivery"], order["total"]) == (
        29900, 12000, 0, 17900)
    assert order["delivery_from"] and order["delivery_to"], order


def test_order_states_stay_in_the_set():
    """States come from the four; settled orders carry an account and one sale per line."""
    states = {r["state"] for r in sql("SELECT DISTINCT state FROM orders")}
    assert states <= set(ORDER_STATES), states
    unbilled = scalar("SELECT count(*) FROM orders WHERE state IN ('paid', 'fulfilled', "
                      "'cancelled') AND (billing_account IS NULL OR billing_account = '')")
    assert unbilled == 0, f"{unbilled} settled orders have no billing account"
    mismatched = sql(
        "SELECT o.number FROM orders o WHERE o.state IN ('paid', 'fulfilled', 'cancelled') AND "
        "(SELECT count(*) FROM order_line l WHERE l.order_id = o.id) <> "
        "(SELECT count(*) FROM stock_movement m WHERE m.order_id = o.id AND m.kind = 'sale')")
    assert mismatched == [], mismatched


def test_seeded_orders_are_persisted(customer2):
    """The three seeded orders hold their accounts, states, lines, totals and accounts."""
    token = owner_token()
    for number, email, state, lines, method, subtotal, discount, delivery, total, billing in SEED_ORDERS:
        order = owner_order(number, token)
        assert order["email"].lower() == email and order["state"] == state, order
        assert order["delivery_method"] == method, order
        assert (order["subtotal"], order["discount"], order["delivery"], order["total"]) == (
            subtotal, discount, delivery, total), order
        assert order["billing_account"] == billing, order
        found = sorted((l["sku"], l["quantity"], l["unit_price"], l["list_price"]) for l in order["lines"])
        assert found == sorted(lines), found
        owner_email = scalar("SELECT a.email FROM orders o JOIN account a ON a.id = o.account_id "
                             "WHERE o.number = %s", number)
        assert owner_email == email, (number, owner_email)
        placed = parse_stamp(order["placed_at"]).date()
        started = scalar("SELECT min(created_at) FROM account").date()
        assert (started - placed).days == SEED_PLACED_DAYS_BEFORE_START[number], (number, placed, started)
        if number != "VS-100003":
            assert order["address"]["line1"] == SEED_ADDRESS[1], order["address"]
            assert order["address"]["name"] == SEED_ADDRESS[0], order["address"]
    with api(customer2) as client:
        response = client.get("/orders/VS-100003")
    assert response.status_code == 200, describe(response, "customer2 reads VS-100003")
    shipped = response.json()["address"]
    for field, value in zip(("name", "line1", "city", "region", "postcode", "country", "phone"),
                            ORDER3_ADDRESS):
        assert shipped[field] == value, (field, shipped)


def test_owner_endpoints_deny_customers_and_visitors(customer):
    """Every owner endpoint denies a customer and a signed-out caller, changing nothing."""
    before = (product("vault-card-case")["title"], variant("VLT-CSE-SFL")["price"],
              stock_of("VLT-CSE-SFL"), sale()["ends_at"])
    calls = (
        ("patch", "/owner/products/vault-card-case", {"title": "Denied Title", "published": False}),
        ("patch", "/owner/variants/VLT-CSE-SFL", {"price": 100, "list_price": 4900}),
        ("get", "/owner/stock-movements?sku=VLT-CSE-SFL", None),
        ("post", "/owner/stock-movements", {"sku": "VLT-CSE-SFL", "delta": -5,
                                            "kind": MOVE_ADJUSTMENT, "note": "denied"}),
        ("patch", "/owner/sale", {"ends_at": iso_from_now(-3600)}),
        ("get", "/owner/orders", None),
        ("post", "/owner/orders/VS-100002/fulfil", None),
        ("post", "/owner/orders/VS-100002/cancel", None),
    )
    for token in (customer, None):
        with api(token) as client:
            for method, path, body in calls:
                response = client.request(method.upper(), path, json=body)
                assert response.status_code in (401, 403), describe(
                    response, f"{'a customer' if token else 'a visitor'} is denied")
    after = (product("vault-card-case")["title"], variant("VLT-CSE-SFL")["price"],
             stock_of("VLT-CSE-SFL"), sale()["ends_at"])
    assert after == before, f"a denied owner call changed state: {before} -> {after}"
    assert owner_order("VS-100002")["state"] == STATE_PAID
    assert login_response(OWNER_EMAIL, SEEDED_PASSWORD).json()["role"] == ROLE_OWNER


def test_guarded_endpoints_deny_missing_or_foreign_tokens(customer):
    """No token or a token the app never issued is turned away and changes nothing."""
    forged = "forged" + unique_suffix() * 4
    calls = (("get", "/me", None), ("get", "/me/orders", None), ("get", "/me/cart", None),
             ("post", "/me/addresses", delivery_address()), ("get", "/orders/VS-100001", None),
             ("get", "/owner/orders", None), ("post", "/auth/logout", None))
    before = scalar("SELECT count(*) FROM address")
    for token in (None, forged):
        with api(token) as client:
            for method, path, body in calls:
                response = client.request(method.upper(), path, json=body)
                assert response.status_code in (401, 403), describe(response, "the call is turned away")
    cart_token = filled_cart([("PCK-CUB-HTG", 1)])
    with api(forged) as client:
        claim = client.post(f"/carts/{cart_token}/claim")
    assert claim.status_code in (401, 403), describe(claim, "a forged claim is turned away")
    assert scalar("SELECT count(*) FROM address") == before
    assert me(customer).status_code == 200, "a real bearer token is accepted"


def test_signup_role_in_body_is_ignored():
    """A signup naming a role, in the body or a header, still makes a customer."""
    suffix = unique_suffix()
    with api() as client:
        response = client.post("/auth/signup", headers={"X-Role": ROLE_OWNER},
                               json={"name": "Probe " + suffix, "email": probe_address(suffix),
                                     "password": probe_password(suffix), "role": ROLE_OWNER})
    assert accepted(response), describe(response, "the signup is accepted")
    assert response.json().get("role") == ROLE_CUSTOMER, response.json()
    assert me(response.json()["access_token"]).json()["role"] == ROLE_CUSTOMER
    stored = scalar("SELECT role FROM account WHERE email = %s", probe_address(suffix))
    assert stored == ROLE_CUSTOMER, stored
    assert scalar("SELECT count(*) FROM account WHERE role = 'owner'") == 1


def test_signup_creates_a_customer_with_a_token():
    """Signup with name, email and password returns a working customer token."""
    account = signup(unique_suffix())
    payload = account["payload"]
    assert payload.get("email") == account["email"] and payload.get("role") == ROLE_CUSTOMER, payload
    assert me(account["token"]).status_code == 200


def test_no_credential_reaches_the_browser(customer):
    """Documents and scripts carry no database or payments credential and no shopper token."""
    secrets = [os.environ.get(name, "") for name in ("PAYMENTS_API_SECRET", "PAYMENTS_ADMIN_PASSWORD")]
    db_password = urllib.parse.urlparse(os.environ.get("DB_ADMIN_URL", "")).password or ""
    secrets = [s for s in secrets + [db_password, customer] if len(s) >= 6]
    shipped = []
    for path in ("/", "/collections/luggage", "/products/passage-luggage-cabin", "/cart"):
        document = fetch_document(path)
        shipped.append(document.text)
        for src in script_sources(document.text):
            shipped.append(fetch_asset(src).text)
    blob = "\n".join(shipped)
    for secret in secrets:
        assert secret not in blob, "a credential reaches the browser"
    assert "postgresql://" not in blob and "postgres://" not in blob


def test_public_reads_need_no_session():
    """Catalogue, search, stores, pages, sale, estimates and carts answer without a session."""
    with api() as client:
        for path in ("/products/passage-luggage-cabin", "/collections", "/collections/luggage",
                     "/collections/luggage/products", "/search?q=olive", "/stores", "/pages/faq",
                     "/sale", "/delivery-estimate?method=standard", "/health"):
            response = client.get(path)
            assert response.status_code == 200, describe(response, f"{path} is public")
        created = client.post("/carts")
    assert accepted(created), describe(created, "a cart needs no session")


def test_owner_renames_reprices_and_delists():
    """Owner edits change the catalogue and never a past order; a delisted product disappears."""
    handle, sku = "vault-card-sleeve", "VLT-SLV-NSH"
    token = owner_token()
    ensure_stock([sku])
    order = place_order([(sku, 1)])
    new_title = "Probe Sleeve " + unique_suffix()
    try:
        with api(token) as client:
            renamed = client.patch(f"/owner/products/{handle}", json={"title": new_title})
            repriced = client.patch(f"/owner/variants/{sku}",
                                    json={"colourway": "Probe Night", "price": 3100, "list_price": 6100})
        assert accepted(renamed), describe(renamed, "the owner renames a product")
        assert accepted(repriced), describe(repriced, "the owner reprices a colourway")
        assert product(handle)["title"] == new_title
        edited = variant(sku)
        assert (edited["colourway"], edited["price"], edited["list_price"]) == ("Probe Night", 3100, 6100)
        past = owner_order(order["number"], token)["lines"][0]
        assert (past["product_title"], past["colourway"], past["unit_price"], past["list_price"]) == (
            "Vault Card Sleeve", "Night Shift", 3900, 5900), past
        assert not past.get("size_class"), past
        with api(token) as client:
            delisted = client.patch(f"/owner/products/{handle}", json={"published": False})
        assert accepted(delisted), describe(delisted, "the owner delists a product")
        with api() as client:
            assert client.get(f"/products/{handle}").status_code == 404
        assert fetch_document(f"/products/{handle}").status_code == 404
        assert new_title not in collection_titles("wallets")
        assert new_title not in collection_titles("best-sellers")
        assert new_title not in [c["title"] for c in search("sleeve")["products"]]
        blocked = add_line(new_cart(), sku, 1)
        assert is_client_error(blocked), describe(blocked, "a delisted colourway cannot join a cart")
        with api(token) as client:
            reached = client.patch(f"/owner/products/{handle}", json={"title": new_title + " B"})
        assert accepted(reached), describe(reached, "the owner reaches a delisted product")
        assert owner_order(order["number"], token)["lines"][0]["product_title"] == "Vault Card Sleeve"
    finally:
        with api(token) as client:
            client.patch(f"/owner/products/{handle}", json={"title": "Vault Card Sleeve", "published": True})
            client.patch(f"/owner/variants/{sku}",
                         json={"colourway": "Night Shift", "price": 3900, "list_price": 5900})
    assert product(handle)["title"] == "Vault Card Sleeve"
    assert variant(sku)["price"] == 3900


def test_owner_stock_movement_changes_stock():
    """A restock moves the stock and lists last among the colourway's movements."""
    sku = "PCK-CUB-SSU"
    token = owner_token()
    before = stock_of(sku)
    note = "probe restock " + unique_suffix()
    response = record_movement(sku, 3, MOVE_RESTOCK, token, note)
    assert accepted(response), describe(response, "the owner records a restock")
    assert response.json().get("stock") == before + 3, response.json()
    assert stock_of(sku) == before + 3
    rows = movements(sku, token)
    stamps = [parse_stamp(r["created_at"]) for r in rows]
    assert stamps == sorted(stamps), "movements list oldest first"
    last = rows[-1]
    assert (last["sku"], last["delta"], last["kind"], last["note"]) == (sku, 3, MOVE_RESTOCK, note), last
    assert "order_number" in last and not last["order_number"], last
    undo = record_movement(sku, -3, MOVE_ADJUSTMENT, token, "probe undo")
    assert accepted(undo) and stock_of(sku) == before


def test_owner_lists_every_order():
    """The owner list carries every order, guest and seeded, newest first."""
    order = place_order([("PCK-CUB-HTG", 1)])
    rows = owner_orders()
    numbers = [r["number"] for r in rows]
    assert order["number"] in numbers and set(SEED_NUMBERS) <= set(numbers), numbers[:10]
    stamps = [parse_stamp(r["placed_at"]) for r in rows]
    assert stamps == sorted(stamps, reverse=True), numbers[:10]
    assert len(rows) == scalar("SELECT count(*) FROM orders")


def test_owner_fulfils_a_paid_order():
    """fulfil moves a paid order to fulfilled."""
    order = place_order([("PCK-CUB-HTG", 1)])
    with api(owner_token()) as client:
        response = client.post(f"/owner/orders/{order['number']}/fulfil")
    assert accepted(response), describe(response, "the owner fulfils a paid order")
    assert response.json()["state"] == STATE_FULFILLED
    assert order_row(order["number"])["state"] == STATE_FULFILLED


def test_owner_cancel_restores_stock_with_a_new_movement():
    """cancel adds one positive cancellation per line and keeps the sale movements and account."""
    sku = "PCK-CUB-SSU"
    order = place_order([(sku, 2)])
    number = order["number"]
    after_sale = stock_of(sku)
    token = owner_token()
    with api(token) as client:
        response = client.post(f"/owner/orders/{number}/cancel")
    assert accepted(response), describe(response, "the owner cancels a paid order")
    assert response.json()["state"] == STATE_CANCELLED
    assert stock_of(sku) == after_sale + 2
    mine = [m for m in movements(sku, token) if m.get("order_number") == number]
    assert sorted((m["kind"], m["delta"]) for m in mine) == [(MOVE_CANCELLATION, 2), (MOVE_SALE, -2)], mine
    assert kb_account(external_key(number)).status_code == 200, "cancelling leaves the account"


def test_stock_movements_cannot_be_edited():
    """A written movement can be neither changed nor removed."""
    sku = "PCK-CUB-HTG"
    token = owner_token()
    ensure_stock([sku])
    row = sql("SELECT m.id, m.delta, m.kind FROM stock_movement m JOIN variant v ON v.id = m.variant_id "
              "WHERE v.sku = %s ORDER BY m.id DESC LIMIT 1", sku)[0]
    count = movement_count()
    with api(token) as client:
        for method in ("PATCH", "PUT", "DELETE"):
            response = client.request(method, f"/owner/stock-movements/{row['id']}",
                                      json={"delta": 99, "kind": MOVE_RESTOCK})
            assert is_client_error(response), describe(response, f"{method} on a movement is refused")
    assert movement_count() == count
    again = sql("SELECT delta, kind FROM stock_movement WHERE id = %s", row["id"])[0]
    assert (again["delta"], again["kind"]) == (row["delta"], row["kind"])


def test_owner_order_transitions_are_limited():
    """Nothing leaves cancelled or fulfilled; other transitions are invalid."""
    token = owner_token()
    cancelled = place_order([("PCK-CUB-HTG", 1)])["number"]
    fulfilled = place_order([("PCK-CUB-HTG", 1)])["number"]
    with api(token) as client:
        assert accepted(client.post(f"/owner/orders/{cancelled}/cancel"))
        assert accepted(client.post(f"/owner/orders/{fulfilled}/fulfil"))
        for number, action in ((cancelled, "fulfil"), (cancelled, "cancel"),
                               (fulfilled, "cancel"), (fulfilled, "fulfil")):
            response = client.post(f"/owner/orders/{number}/{action}")
            assert is_client_error(response), describe(response, f"{action} on {number} is invalid")
    assert order_row(cancelled)["state"] == STATE_CANCELLED
    assert order_row(fulfilled)["state"] == STATE_FULFILLED


def test_stock_equals_the_sum_of_movements():
    """Every colourway's stock is the sum of its movements, of the four kinds only."""
    columns = table_columns("stock_movement")
    assert {"variant_id", "delta", "kind", "order_id", "note", "created_at"} <= columns, columns
    for read in all_products():
        for item in read["variants"]:
            assert int(item["stock"]) == movement_sum(item["sku"]), item["sku"]
            assert item["in_stock"] is (int(item["stock"]) > 0), item["sku"]
    kinds = {r["kind"] for r in sql("SELECT DISTINCT kind FROM stock_movement")}
    assert kinds <= set(MOVEMENT_KINDS), kinds
    assert "stock" not in table_columns("variant"), "stock is a stored column"


def test_invalid_stock_movements_are_rejected():
    """Zero, fractional, hand-written sale or cancellation, and overdrawing movements are refused."""
    token = owner_token()
    count = movement_count()
    for sku, delta, kind in (("PCK-CUB-HTG", 0, MOVE_RESTOCK), ("PCK-CUB-HTG", 1.5, MOVE_RESTOCK),
                             ("PCK-CUB-HTG", -1, MOVE_SALE), ("PCK-CUB-HTG", 1, MOVE_CANCELLATION),
                             ("PSG-CAB-CSP", -1, MOVE_ADJUSTMENT)):
        response = record_movement(sku, delta, kind, token)
        assert is_client_error(response), describe(response, f"{kind} {delta} on {sku} is refused")
    assert movement_count() == count
    assert stock_of("PSG-CAB-CSP") == 0


def test_invalid_variant_prices_are_rejected():
    """A price above the list price, or a figure at or below zero, changes nothing."""
    sku = "TRV-PLW-DEB"
    before = variant(sku)
    with api(owner_token()) as client:
        for body in ({"price": 4000, "list_price": 3500}, {"price": 0}, {"list_price": -1},
                     {"price": -100}):
            response = client.patch(f"/owner/variants/{sku}", json=body)
            assert is_client_error(response), describe(response, f"{body} is invalid")
    after = variant(sku)
    assert (after["price"], after["list_price"]) == (before["price"], before["list_price"])
    assert scalar("SELECT count(*) FROM variant WHERE price > list_price OR price <= 0") == 0


def test_seeded_movements_open_each_colourway():
    """Seeding wrote one opening restock per colourway and one sale per seeded line, once."""
    token = owner_token()
    for _handle, sku, _name, _family, _price, _list, table_stock in pinned_variants():
        rows = movements(sku, token)
        assert rows[0]["kind"] == MOVE_RESTOCK and rows[0]["delta"] == table_stock + seeded_units(sku), (sku, rows[0])
    for number, _email, _state, lines, *_rest in SEED_ORDERS:
        for sku, qty, _price, _list in lines:
            sales = [m for m in movements(sku, token)
                     if m.get("order_number") == number and m["kind"] == MOVE_SALE]
            assert [m["delta"] for m in sales] == [-qty], (number, sku, sales)


def test_checkout_validation_writes_nothing():
    """Bad addresses, emails, methods and keys are refused before anything is written."""
    ensure_stock(["TRV-PLW-HTG"])
    cart_token = filled_cart([("TRV-PLW-HTG", 1)])
    orders_before, moves_before = order_count(), movement_count()
    missing_name = delivery_address()
    missing_name.pop("name")
    for address, field in ((missing_name, "name"), (delivery_address(postcode="9720"), "postcode"),
                           (delivery_address(postcode="97A05"), "postcode"),
                           (delivery_address(country="CA"), "country")):
        response = checkout(cart_token, address=address)
        assert is_client_error(response), describe(response, f"a bad {field} is invalid")
        assert body_of(response).get("field") == field, describe(response, f"field names {field}")
    for kwargs in ({"email": "not-an-email"}, {"method": "drone"}, {"key": "short"},
                   {"key": "k" * 65}):
        response = checkout(cart_token, **kwargs)
        assert is_client_error(response), describe(response, f"{kwargs} is invalid")
    assert order_count() == orders_before and movement_count() == moves_before
    assert len(cart(cart_token)["lines"]) == 1
    no_line2 = delivery_address()
    no_line2.pop("line2")
    placed = checkout(cart_token, address=no_line2)
    assert placed.status_code in (200, 201), describe(placed, "line2 is optional")


def test_empty_cart_checkout_is_refused():
    """An empty cart is refused with cart_empty."""
    orders_before = order_count()
    response = checkout(new_cart())
    assert is_client_error(response), describe(response, "an empty cart is refused")
    assert error_of(response) == ERR_CART_EMPTY and message_of(response)
    assert order_count() == orders_before


def test_invalid_address_is_rejected(shopper):
    """A saved address is validated like a checkout address."""
    token = shopper["token"]
    missing_city = delivery_address()
    missing_city.pop("city")
    with api(token) as client:
        for body in (delivery_address(postcode="ABCDE"), delivery_address(country="GB"), missing_city):
            response = client.post("/me/addresses", json=body)
            assert is_client_error(response), describe(response, "an invalid address is refused")
    assert addresses(token) == []


def test_malformed_requests_are_client_errors():
    """Malformed calls are client errors with error and message, never a server error or trace."""
    base = api_base()
    cart_token = new_cart()
    probes = (
        httpx.post(base + "/checkout", content=b"{not json", timeout=30,
                   headers={"Content-Type": "application/json"}),
        httpx.post(base + "/auth/login", content=b"email=x", timeout=30,
                   headers={"Content-Type": "application/json"}),
        add_line(cart_token, "PCK-CUB-HTG", "two"),
        checkout(cart_token, method=None),
    )
    for response in probes:
        assert is_client_error(response), describe(response, "a malformed call is a client error")
        payload = body_of(response)
        assert payload.get("error") and payload.get("message"), describe(response, "error and message")
        assert "node_modules" not in response.text and "    at " not in response.text


def test_signed_in_checkout_links_the_order(shopper):
    """A checkout with a bearer token links the order to the account."""
    token = shopper["token"]
    ensure_stock(["PCK-CUB-SSU"])
    cart_token = filled_cart([("PCK-CUB-SSU", 1)], token)
    response = checkout(cart_token, email=shopper["email"], token=token)
    assert response.status_code in (200, 201), describe(response, "a signed-in checkout passes")
    number = response.json()["number"]
    with api(token) as client:
        mine = [r["number"] for r in top_level_array(client.get("/me/orders"))]
    assert number in mine
    linked = scalar("SELECT a.email FROM orders o JOIN account a ON a.id = o.account_id "
                    "WHERE o.number = %s", number)
    assert linked == shopper["email"]


def test_unknown_corporate_account_is_refused():
    """A corporate key the provider does not hold is refused, writing no order and moving no stock."""
    sku = "TRV-PLW-DEB"
    ensure_stock([sku])
    cart_token = filled_cart([(sku, 1)])
    before, orders_before = stock_of(sku), order_count()
    key = checkout_key()
    unknown = "orbit-nowhere-" + unique_suffix()
    assert kb_account(unknown).status_code == 404
    response = checkout(cart_token, key=key, corporate=unknown)
    assert is_client_error(response), describe(response, "an unknown corporate account is refused")
    assert error_of(response) == ERR_CORPORATE_UNKNOWN and message_of(response) == MSG_CORPORATE_UNKNOWN
    assert orders_for_key(key) == 0 and order_count() == orders_before and stock_of(sku) == before
    assert len(cart(cart_token)["lines"]) == 1


def test_foreign_currency_corporate_account_is_refused():
    """A corporate account billed in EUR is refused with the currency message."""
    sku = "TRV-PLW-DEB"
    ensure_stock([sku])
    cart_token = filled_cart([(sku, 1)])
    before, orders_before = stock_of(sku), order_count()
    for key, name, currency in CORPORATE_ACCOUNTS:
        found = kb_account(key)
        assert found.status_code == 200, describe(found, f"killbill holds {key}")
        assert (found.json()["name"], found.json()["currency"]) == (name, currency), found.json()
    acme = checkout(cart_token, corporate=ACME)
    assert is_client_error(acme) and error_of(acme) == ERR_CORPORATE_CURRENCY, describe(acme, "acme")
    assert message_of(acme) == MSG_CORPORATE_EUR == currency_refusal(KB_EUR)
    amelia = checkout(cart_token, corporate=AMELIA)
    assert is_client_error(amelia) and message_of(amelia) == currency_refusal(KB_EUR)
    assert order_count() == orders_before and stock_of(sku) == before


def test_corporate_order_bills_the_existing_account():
    """A USD corporate account takes the order without a new account being opened."""
    ensure_stock(["PCK-CUB-HTG"])
    order_cart = filled_cart([("PCK-CUB-HTG", 1)])
    response = checkout(order_cart, corporate=NORTHWIND)
    assert response.status_code in (200, 201), describe(response, "a USD corporate account is billed")
    order = response.json()
    assert order["billing_account"] == NORTHWIND and order["state"] == STATE_PAID, order
    assert kb_account(external_key(order["number"])).status_code == 404, "no new account is opened"
    assert kb_account(NORTHWIND).json()["currency"] == KB_USD


def test_seeded_billing_accounts_exist_in_killbill():
    """The two self-paid seeded orders have their accounts in killbill."""
    for key in SELF_BILLED_KEYS:
        found = kb_account(key)
        assert found.status_code == 200, describe(found, f"killbill holds {key}")
        assert found.json()["externalKey"] == key
    stored = {r["number"]: r["billing_account"] for r in sql(
        "SELECT number, billing_account FROM orders WHERE number IN (%s, %s, %s)", *SEED_NUMBERS)}
    assert stored == {o[0]: o[9] for o in SEED_ORDERS}, stored


def test_search_matches_colourway_names():
    """olive finds the eight products that come in Field Olive, in any letter case."""
    result = search(SEARCH_EXAMPLE)
    assert {"query", "count", "products"} <= set(result), result.keys()
    expected = {row[1] for row in PRODUCTS if "OLV" in row[14]}
    assert result["count"] == SEARCH_OLIVE_COUNT == len(expected)
    assert {c["title"] for c in result["products"]} == expected
    assert search("OLIVE")["count"] == SEARCH_OLIVE_COUNT
    assert result["query"] == SEARCH_EXAMPLE
    assert "lowest_price" in result["products"][0] and "colourways" in result["products"][0]


def test_search_ranks_titles_before_colourways():
    """Title matches, then colourway matches, then line matches, each by position."""
    assert [c["title"] for c in search("coastal")["products"]] == list(SEARCH_COASTAL)
    meridian = [c["title"] for c in search("meridian")["products"]]
    assert meridian[-1] == SEARCH_MERIDIAN_LAST, meridian
    assert meridian[:-1] == [row[1] for row in PRODUCTS if row[1].startswith("Meridian")], meridian
    passage = [c["title"] for c in search("passage")["products"]]
    assert passage == [row[1] for row in PRODUCTS if row[3] == "Passage"], passage


def test_search_accepts_sort_without_filters():
    """A sort reorders the results; filters are ignored."""
    ranked = search(SEARCH_EXAMPLE, sort="price-asc")["products"]
    prices = [c["lowest_price"] for c in ranked]
    assert prices == sorted(prices), prices
    assert search(SEARCH_EXAMPLE, size="cabin")["count"] == SEARCH_OLIVE_COUNT


def test_search_without_a_match_is_empty():
    """A query with no match returns count 0."""
    result = search("zzqx" + unique_suffix())
    assert result["count"] == 0 and result["products"] == [], result


def test_recent_searches_stay_in_the_browser(page):
    """Searching and viewing products sends no history to the server."""
    posted = []
    page.on("request", lambda request: posted.append((request.method, request.url,
                                                       request.post_data or "")))
    open_page(page, "/")
    page.get_by_text("SEARCH", exact=True).first.click()
    field = page.locator("input:visible").first
    field.fill(SEARCH_EXAMPLE)
    field.press("Enter")
    poll_until(lambda: "/search" in page.url)
    assert urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query).get("q") == [SEARCH_EXAMPLE]
    open_page(page, "/products/passage-luggage-cabin")
    open_page(page, "/")
    for method, url, data in posted:
        if method != "GET":
            assert SEARCH_EXAMPLE not in data and "passage-luggage-cabin" not in data, (method, url)
        else:
            path = urllib.parse.urlparse(url).path
            if SEARCH_EXAMPLE in url:
                assert path in ("/search", "/api/search"), url
    other = page.context.browser.new_context()
    fresh = other.new_page()
    open_page(fresh, "/")
    fresh.get_by_text("SEARCH", exact=True).first.click()
    settle()
    assert SEARCH_EXAMPLE not in page_text(fresh).lower(), "recent searches leaked to a new browser"
    other.close()


def test_stores_are_listed_by_city_then_name():
    """Every store lists, ordered by city then name, with the named fields."""
    with api() as client:
        rows = top_level_array(client.get("/stores"))
        blank = top_level_array(client.get("/stores", params={"q": ""}))
    assert [r["name"] for r in rows] == [s[0] for s in STORES]
    assert [(r["city"], r["name"]) for r in rows] == sorted((r["city"], r["name"]) for r in rows)
    assert [r["name"] for r in blank] == [s[0] for s in STORES]
    for row in rows:
        assert {"name", "city", "region", "address", "postcode", "phone", "hours"} <= set(row), row


def test_store_filter_matches_city_or_name():
    """q narrows by city or name, ignoring case, in the same order."""
    with api() as client:
        port = top_level_array(client.get("/stores", params={"q": "port"}))
        new = top_level_array(client.get("/stores", params={"q": "NEW"}))
        pike = top_level_array(client.get("/stores", params={"q": "pike"}))
    assert [r["name"] for r in port] == list(STORES_PORT)
    assert [r["name"] for r in new] == list(STORES_NEW)
    assert [r["name"] for r in pike] == ["Pike Place"]


def test_seeded_stores_match_the_table():
    """The fourteen stores carry the table's fields exactly."""
    with api() as client:
        rows = top_level_array(client.get("/stores"))
    found = [(r["name"], r["city"], r["region"], r["address"], r["postcode"], r["phone"], r["hours"])
             for r in rows]
    assert found == [tuple(s) for s in STORES], found
    columns = table_columns("store")
    assert {"name", "city", "region", "address", "postcode", "phone", "hours"} <= columns


def test_newsletter_subscription_is_stored_once():
    """A subscription is stored lowercased once and answers the same when repeated."""
    suffix = unique_suffix()
    address = probe_address(suffix)
    with api() as client:
        first = client.post("/newsletter", json={"email": address.upper()})
        second = client.post("/newsletter", json={"email": address})
    assert accepted(first) and message_of(first) == MSG_NEWSLETTER, describe(first, "subscribe")
    assert accepted(second) and message_of(second) == MSG_NEWSLETTER, describe(second, "repeat")
    assert first.status_code == second.status_code
    assert scalar("SELECT count(*) FROM subscriber WHERE email = %s", address) == 1
    assert scalar("SELECT count(*) FROM subscriber WHERE email = %s", address.upper()) == 0
    assert {"email", "created_at"} <= table_columns("subscriber")


def test_invalid_newsletter_address_is_rejected():
    """A value that is not an email address is refused and stores nothing."""
    before = scalar("SELECT count(*) FROM subscriber")
    with api() as client:
        response = client.post("/newsletter", json={"email": "not-an-address"})
    assert is_client_error(response), describe(response, "a bad address is refused")
    assert scalar("SELECT count(*) FROM subscriber") == before


def test_gift_card_balance_answers_for_the_active_card():
    """VSGC-2026-AMBER holds 5000 cents in usd."""
    with api() as client:
        response = client.post("/gift-cards/balance", json={"code": GIFT_ACTIVE})
    assert response.status_code == 200, describe(response, "the active card answers")
    assert response.json() == {**response.json(), "balance": GIFT_ACTIVE_BALANCE, "currency": CURRENCY}


def test_unknown_or_lapsed_gift_cards_look_the_same():
    """The lapsed card and an unknown code get the same status and body."""
    with api() as client:
        lapsed = client.post("/gift-cards/balance", json={"code": GIFT_LAPSED})
        unknown = client.post("/gift-cards/balance", json={"code": "VSGC-0000-" + unique_suffix()})
    assert is_client_error(lapsed), describe(lapsed, "the lapsed card is refused")
    assert (lapsed.status_code, lapsed.text) == (unknown.status_code, unknown.text)
    assert message_of(lapsed) == MSG_GIFT_UNKNOWN


def test_gift_card_rows_are_seeded():
    """The two gift cards are stored with balance, currency and expiry."""
    rows = {r["code"]: r for r in sql("SELECT code, balance, currency, expires_on FROM gift_card")}
    assert rows[GIFT_ACTIVE]["balance"] == GIFT_ACTIVE_BALANCE and rows[GIFT_ACTIVE]["expires_on"] is None
    assert rows[GIFT_LAPSED]["balance"] == GIFT_LAPSED_BALANCE
    assert str(rows[GIFT_LAPSED]["expires_on"])[:10] == GIFT_LAPSED_EXPIRY
    assert {str(r["currency"]).lower() for r in rows.values()} == {CURRENCY}


def test_standing_pages_are_served():
    """The ten standing pages answer at /api/pages and /pages with their titles."""
    with api() as client:
        for handle, title, _link in PAGES:
            response = client.get(f"/pages/{handle}")
            assert response.status_code == 200, describe(response, f"page {handle}")
            payload = response.json()
            assert (payload["handle"], payload["title"]) == (handle, title) and payload["body"], payload
            assert fetch_document(f"/pages/{handle}").status_code == 200
    assert scalar("SELECT count(*) FROM page") == len(PAGES)
    assert {"handle", "title", "body"} <= table_columns("page")


def test_privacy_page_states_what_is_kept():
    """The privacy page names what is kept, for how long, and what never leaves the browser."""
    with api() as client:
        body = client.get("/pages/privacy").json()["body"].lower()
    for word in ("account", "address", "order", "cart", "newsletter", "card", "search", "browser",
                 "removal"):
        assert word in body, f"the privacy page does not mention {word}"
    assert "seven years" in body or "7 years" in body, "orders are kept seven years"
    assert "ninety days" in body or "90 days" in body, "carts are kept ninety days"
    assert "recently viewed" in body


def test_every_footer_links_the_privacy_page(page):
    """The footer of each page links the privacy page."""
    for path in ("/", "/collections/luggage", "/products/passage-luggage-cabin", STORES_PATH, "/cart"):
        open_page(page, path)
        found = poll_until(lambda: page.locator(
            f"footer a[href$='{PRIVACY_PATH}'], [role=contentinfo] a[href$='{PRIVACY_PATH}']").count())
        assert found, f"the footer of {path} does not link {PRIVACY_PATH}"


def test_seed_rows_are_not_duplicated():
    """The seed exists once: stores, pages, sale, cards, catalogue, accounts and seed sales."""
    for table, expected in (("store", len(STORES)), ("page", len(PAGES)), ("sale", 1),
                            ("gift_card", 2), ("category", len(CATEGORY_HANDLES)),
                            ("collection", len(COLLECTIONS)), ("product", len(PRODUCTS))):
        assert scalar(f"SELECT count(*) FROM {table}") == expected, table
    assert scalar("SELECT name FROM sale") == SALE_NAME
    for email, _role, _name in SEEDED_ACCOUNTS:
        assert scalar("SELECT count(*) FROM account WHERE email = %s", email) == 1, email
    for number in SEED_NUMBERS:
        assert scalar("SELECT count(*) FROM orders WHERE number = %s", number) == 1, number
    doubled = sql("SELECT o.number, m.variant_id, count(*) AS n FROM stock_movement m JOIN orders o "
                  "ON o.id = m.order_id WHERE m.kind = 'sale' AND o.number IN (%s, %s, %s) "
                  "GROUP BY o.number, m.variant_id HAVING count(*) > 1", *SEED_NUMBERS)
    assert doubled == [], doubled


def test_seeded_accounts_sign_in_with_the_corpus_password():
    """Each seeded account signs in with deku-demo-pw-2026 and reads its role."""
    for email, role, _name in SEEDED_ACCOUNTS:
        response = login_response(email, SEEDED_PASSWORD)
        assert response.status_code == 200, describe(response, f"{email} signs in")
        assert response.json()["access_token"] and response.json()["role"] == role


def test_seeded_accounts_are_stored_with_their_roles():
    """The accounts table holds the three seeded accounts with their roles and names."""
    columns = table_columns("account")
    assert {"email", "password_hash", "name", "role", "created_at"} <= columns, columns
    for email, role, name in SEEDED_ACCOUNTS:
        row = sql("SELECT email, role, name FROM account WHERE email = %s", email)
        assert row and (row[0]["role"], row[0]["name"]) == (role, name), row
    assert scalar("SELECT count(*) FROM account WHERE role = 'owner'") == 1
    assert scalar("SELECT email FROM account WHERE role = 'owner'") == OWNER_EMAIL
    assert os.environ.get("DB_ADMIN_URL"), "PostgreSQL is reachable at DB_ADMIN_URL"


def test_login_returns_token_role_with_expiry():
    """Sign-in returns access_token, role and a UTC expires_at."""
    response = login_response(CUSTOMER_EMAIL, SEEDED_PASSWORD)
    payload = response.json()
    assert payload["access_token"] and payload["role"] == ROLE_CUSTOMER, payload
    assert str(payload["expires_at"]).endswith("Z"), payload
    with api(payload["access_token"]) as client:
        assert client.get("/me").status_code == 200


def test_remember_me_extends_the_session_to_thirty_days():
    """Without remember a token lasts twelve hours; with remember thirty days."""
    started = now_utc()
    short = login_response(CUSTOMER_EMAIL, SEEDED_PASSWORD).json()
    long = login_response(CUSTOMER_EMAIL, SEEDED_PASSWORD, remember=True).json()
    short_hours = (parse_stamp(short["expires_at"]) - started).total_seconds() / 3600
    long_days = (parse_stamp(long["expires_at"]) - started).total_seconds() / 86400
    assert abs(short_hours - 12) < 0.25, short
    assert abs(long_days - 30) < 0.02, long


def test_failed_login_hides_which_part_was_wrong():
    """A wrong password and an unknown email get the same status and body."""
    wrong = login_response(CUSTOMER_EMAIL, "not-the-password-1")
    unknown = login_response(probe_address(unique_suffix()), "not-the-password-1")
    assert is_client_error(wrong), describe(wrong, "a wrong password is refused")
    assert (wrong.status_code, wrong.text) == (unknown.status_code, unknown.text)
    assert message_of(wrong) == MSG_LOGIN


def test_logout_ends_the_token(shopper):
    """After logout the token is turned away everywhere."""
    token = login(shopper["email"], shopper["password"])
    with api(token) as client:
        assert client.get("/me").status_code == 200
        out = client.post("/auth/logout")
        assert accepted(out), describe(out, "logout succeeds")
        for path in ("/me", "/me/orders", "/me/addresses"):
            assert client.get(path).status_code in (401, 403), path
    columns = table_columns("session_token")
    assert {"account_id", "token_hash", "expires_at", "revoked_at", "created_at"} <= columns


def test_recover_answers_the_same_for_every_address(shopper):
    """Recovery answers identically for known and unknown addresses."""
    with api() as client:
        known = client.post("/auth/recover", json={"email": shopper["email"]})
        unknown = client.post("/auth/recover", json={"email": probe_address(unique_suffix())})
    assert known.status_code == unknown.status_code and accepted(known), describe(known, "recover")
    assert message_of(known) == message_of(unknown) == MSG_RECOVER


def test_reset_email_goes_to_known_addresses_only(shopper):
    """A known address gets one reset email; an unknown one gets nothing."""
    stranger = probe_address(unique_suffix())
    with api() as client:
        client.post("/auth/recover", json={"email": shopper["email"]})
        client.post("/auth/recover", json={"email": stranger})
    rows = wait_for_mail(shopper["email"])
    assert len(rows) == 1 and rows[0]["Subject"] == RESET_SUBJECT, rows
    for _ in range(4):
        settle()
    assert mail_to(stranger) == []


def reset_token_for(email: str) -> str:
    with api() as client:
        client.post("/auth/recover", json={"email": email})
    rows = wait_for_mail(email)
    assert rows, f"no reset email for {email}"
    text = mail_text(rows[-1]).strip()
    prefix = app_url() + RESET_PATH
    assert text.startswith(prefix), f"the reset email opens with {text[:80]!r}"
    return re.split(r"\s", text[len(prefix):], maxsplit=1)[0]


def test_password_reset_works_once(shopper):
    """The emailed token replaces the password once; a short, used or unknown token changes nothing."""
    token = reset_token_for(shopper["email"])
    new_password = "probe-new-" + unique_suffix()
    with api() as client:
        short = client.post("/auth/reset", json={"token": token, "password": "short9pw"})
        assert is_client_error(short), describe(short, "a short password is refused")
        done = client.post("/auth/reset", json={"token": token, "password": new_password})
        assert accepted(done), describe(done, "the reset succeeds")
        reused = client.post("/auth/reset", json={"token": token, "password": new_password + "x"})
        assert is_client_error(reused), describe(reused, "a used token is refused")
        unknown = client.post("/auth/reset", json={"token": "unknown" + unique_suffix(),
                                                   "password": new_password + "y"})
        assert is_client_error(unknown), describe(unknown, "an unknown token is refused")
    assert login_response(shopper["email"], new_password).status_code == 200
    assert is_client_error(login_response(shopper["email"], shopper["password"]))
    assert is_client_error(login_response(shopper["email"], new_password + "x"))
    assert {"account_id", "token_hash", "used_at", "created_at"} <= table_columns("password_reset")


def test_reset_page_sets_a_new_password(page, shopper):
    """The reset page takes a new password and confirms the change."""
    token = reset_token_for(shopper["email"])
    open_page(page, RESET_PATH + token)
    assert poll_until(lambda: RESET_HEADING in page_text(page)), page_text(page)[:300]
    new_password = "probe-page-" + unique_suffix()
    page.locator("input[type=password]").first.fill(new_password)
    page.get_by_role("button", name=RESET_BUTTON).click()
    assert poll_until(lambda: RESET_DONE in page_text(page)), page_text(page)[:300]
    assert login_response(shopper["email"], new_password).status_code == 200


def test_me_returns_the_signed_in_account(customer):
    """/me returns name, email and role, and nothing about the password."""
    response = me(customer)
    payload = response.json()
    assert (payload["name"], payload["email"], payload["role"]) == (
        SEEDED_ACCOUNTS[1][2], CUSTOMER_EMAIL, ROLE_CUSTOMER), payload
    assert "password" not in response.text.lower()


def test_passwords_are_stored_hashed_never_returned(shopper):
    """Only a salted hash is stored, and no response carries the password or its hash."""
    stored = scalar("SELECT password_hash FROM account WHERE email = %s", shopper["email"])
    assert stored and shopper["password"] not in stored and len(stored) >= 20, "the password is not hashed"
    seeded = sql("SELECT password_hash FROM account WHERE email IN (%s, %s)", CUSTOMER_EMAIL, CUSTOMER2_EMAIL)
    assert seeded[0]["password_hash"] != seeded[1]["password_hash"], "hashes carry no salt"
    responses = [login_response(shopper["email"], shopper["password"]), me(shopper["token"])]
    for response in responses:
        assert shopper["password"] not in response.text and stored not in response.text
        assert "password" not in response.text.lower()
    assert "password" not in str(shopper["payload"]).lower()


def test_emails_are_unique_ignoring_case():
    """Emails are stored lowercased and a second signup in any case is refused."""
    suffix = unique_suffix()
    mixed = "Probe-" + suffix + "@" + "Example.com"
    with api() as client:
        first = client.post("/auth/signup", json={"name": "Probe", "email": mixed,
                                                  "password": probe_password(suffix)})
        again = client.post("/auth/signup", json={"name": "Probe", "email": mixed.upper(),
                                                  "password": probe_password(suffix)})
    assert accepted(first), describe(first, "the first signup passes")
    assert is_client_error(again), describe(again, "the address is already in use")
    assert scalar("SELECT count(*) FROM account WHERE lower(email) = %s", mixed.lower()) == 1
    assert scalar("SELECT email FROM account WHERE lower(email) = %s", mixed.lower()) == mixed.lower()


def test_short_signup_password_is_rejected():
    """A nine-character password is refused and no account is created."""
    suffix = unique_suffix()
    with api() as client:
        response = client.post("/auth/signup", json={"name": "Probe", "email": probe_address(suffix),
                                                     "password": "abcdefgh9"})
    assert is_client_error(response), describe(response, "a short password is refused")
    assert scalar("SELECT count(*) FROM account WHERE email = %s", probe_address(suffix)) == 0


def test_addresses_are_saved_with_one_default(shopper):
    """The first saved address is the default, and a second does not take it."""
    token = shopper["token"]
    assert addresses(token) == []
    first = save_address(token, line1="1 First Street")
    second = save_address(token, line1="2 Second Street")
    assert accepted(first) and accepted(second), describe(second, "addresses are saved")
    rows = {a["line1"]: a for a in addresses(token)}
    assert rows["1 First Street"]["is_default"] is True and rows["2 Second Street"]["is_default"] is False
    for field in ("id", "name", "line1", "line2", "city", "region", "postcode", "country", "phone"):
        assert field in rows["1 First Street"], field


def test_default_address_moves_on_change(shopper):
    """is_default true makes an address the only default; a change edits the address."""
    token = shopper["token"]
    save_address(token, line1="1 First Street")
    second = save_address(token, line1="2 Second Street").json()
    with api(token) as client:
        made = client.patch(f"/me/addresses/{second['id']}", json={"is_default": True})
        assert accepted(made), describe(made, "the default moves")
    rows = {a["line1"]: a for a in addresses(token)}
    assert rows["2 Second Street"]["is_default"] is True and rows["1 First Street"]["is_default"] is False
    with api(token) as client:
        edited = client.patch(f"/me/addresses/{rows['1 First Street']['id']}", json={"line1": "3 Third Street"})
    assert accepted(edited), describe(edited, "an address changes")
    assert {a["line1"] for a in addresses(token)} == {"2 Second Street", "3 Third Street"}
    defaults = scalar("SELECT count(*) FROM address a JOIN account c ON c.id = a.account_id "
                      "WHERE c.email = %s AND a.is_default", shopper["email"])
    assert defaults == 1


def test_deleting_the_default_promotes_the_oldest(shopper):
    """Removing the default makes the oldest remaining address the default."""
    token = shopper["token"]
    for line in ("1 Oldest Street", "2 Middle Street"):
        save_address(token, line1=line)
    newest = save_address(token, line1="3 Newest Street", is_default=True).json()
    with api(token) as client:
        removed = client.delete(f"/me/addresses/{newest['id']}")
    assert accepted(removed), describe(removed, "the default is removed")
    rows = {a["line1"]: a["is_default"] for a in addresses(token)}
    assert rows == {"1 Oldest Street": True, "2 Middle Street": False}, rows


def test_seeded_addresses_are_persisted(customer, customer2, owner):
    """The seeded customer holds one default address; the others hold none."""
    columns = table_columns("address")
    assert {"name", "line1", "line2", "city", "region", "postcode", "country", "phone", "is_default"} <= columns
    seeded = [a for a in addresses(customer) if a["line1"] == SEED_ADDRESS[1]]
    assert len(seeded) == 1, seeded
    found = seeded[0]
    assert (found["name"], found["line1"], found["line2"], found["city"], found["region"],
            found["postcode"], found["country"], found["phone"]) == SEED_ADDRESS
    assert found["is_default"] is True
    assert addresses(customer2) == [] and addresses(owner) == []
    with api(owner) as client:
        assert top_level_array(client.get("/me/orders")) == []


def test_health_answers_ok():
    """/api/health answers 200 ok, and killbill's healthcheck needs no credentials."""
    with api() as client:
        response = client.get("/health")
    assert response.status_code == 200 and response.json() == {"status": "ok"}, describe(response, "health")
    kb = httpx.get(os.environ["PAYMENTS_API_URL"].rstrip("/") + KB_HEALTH_PATH, timeout=30)
    assert kb.status_code == 200, describe(kb, "the killbill healthcheck")


def test_app_answers_at_its_public_url():
    """The app answers at APP_PUBLIC_URL with the API on the same origin."""
    document = fetch_document("/")
    assert document.status_code == 200 and "html" in document.headers.get("content-type", "")
    assert str(document.url).startswith(app_url())
    api_response = httpx.get(app_url() + "/api/health", timeout=30)
    assert api_response.status_code == 200, describe(api_response, "the API shares the origin")
    assert urllib.parse.urlparse(app_url()).hostname not in ("127.0.0.1", "localhost")


def test_production_build_is_served():
    """A built Svelte bundle is served, not a dev server."""
    document = fetch_document("/").text
    assert "/@vite/client" not in document and "/src/main" not in document, "a dev server answers"
    sources = script_sources(document)
    assert sources, "the document references no script"
    bundle = "\n".join(fetch_asset(s).text for s in sources)
    assert "svelte" in bundle.lower() or "svelte" in document.lower(), "no Svelte build is served"
    assert "hmr" not in " ".join(sources).lower()


def test_page_scripts_stay_within_the_budget():
    """The scripts a document references add up to 180 KB or less gzipped."""
    for path in ("/", "/collections/luggage", "/products/passage-luggage-cabin"):
        document = fetch_document(path).text
        total = 0
        for src in script_sources(document):
            asset = fetch_asset(src)
            assert asset.status_code == 200, describe(asset, f"script {src}")
            total += gzip_size(asset.content)
        assert total <= SCRIPT_BUDGET_BYTES, f"{path} scripts weigh {total} bytes gzipped"


def test_public_routes_are_served():
    """Every public route serves an HTML document."""
    routes = list(PUBLIC_ROUTES) + [f"/pages/{handle}" for handle, _t, _l in PAGES]
    for path in routes:
        document = fetch_document(path)
        assert document.status_code == 200, describe(document, f"{path} is served")
        assert "html" in document.headers.get("content-type", ""), path


def test_not_found_page_renders_inside_the_chrome(page):
    """Unknown addresses render the own not-found page with its three links and a 404."""
    for path in ("/no-such-address", "/products/no-such-product", "/pages/no-such-page"):
        response = page.goto(app_url() + path, wait_until="networkidle")
        assert response.status == 404, f"{path} answered {response.status}"
        assert poll_until(lambda: NOT_FOUND_HEADING in page_text(page)), page_text(page)[:300]
        text = page_text(page)
        assert NOT_FOUND_LINE in text and "valisette" in text, text[:300]
        main = page.locator("main")
        for label, href in zip(NOT_FOUND_LABELS, NOT_FOUND_LINKS):
            link = main.get_by_role("link", name=label, exact=True)
            assert link.count() >= 1, f"no {label} link on {path}"
            assert app_path(link.first.get_attribute("href")) == href
        assert page.get_by_role("contentinfo").count() == 1


def test_unknown_api_address_answers_json():
    """An unknown /api address answers JSON not_found."""
    with api() as client:
        response = client.get("/no-such-endpoint")
    assert response.status_code == 404, describe(response, "unknown API address")
    assert "json" in response.headers.get("content-type", "")
    assert error_of(response) == ERR_NOT_FOUND


def test_internal_links_resolve(page):
    """Every internal link on the main pages leads to a page that exists."""
    targets = set()
    for path in ("/", "/collections/luggage", "/products/passage-luggage-cabin", STORES_PATH,
                 "/pages/faq"):
        open_page(page, path)
        settle()
        targets |= set(internal_hrefs(page))
    assert targets, "no internal links were found"
    for href in sorted(targets):
        document = fetch_document(href)
        assert document.status_code == 200, describe(document, f"internal link {href}")


def test_documents_declare_a_favicon_that_resolves():
    """Each document declares a favicon, served as a vector image."""
    for path in ("/", "/collections/luggage", "/products/passage-luggage-cabin", "/cart"):
        href = favicon_href(fetch_document(path).text)
        assert href, f"{path} declares no favicon"
        icon = fetch_asset(href)
        assert icon.status_code == 200, describe(icon, "the favicon")
        assert icon.headers.get("content-type", "").startswith("image/"), icon.headers
        assert "<svg" in icon.text, "the favicon is drawn vector markup"


def test_pages_carry_one_of_each_landmark(page):
    """Each page has one banner, one main and one contentinfo landmark."""
    for path in ("/", "/collections/luggage", "/products/passage-luggage-cabin", "/cart", STORES_PATH):
        open_page(page, path)
        for role in ("banner", "main", "contentinfo"):
            assert page.get_by_role(role).count() == 1, f"{path} has {page.get_by_role(role).count()} {role}"


def test_pages_fetch_no_image_font_or_video_files(page):
    """No page requests a raster image, a font, a video or a sprite; only the favicon is fetched."""
    seen = collect_requests(page)
    for path in ("/", "/collections/luggage", "/products/passage-luggage-cabin"):
        open_page(page, path)
        page.mouse.wheel(0, 6000)
        settle()
    favicon = favicon_href(fetch_document("/").text)
    for url, kind in seen:
        path = urllib.parse.urlparse(url).path.lower()
        if favicon and path.endswith(urllib.parse.urlparse(favicon).path.lower()):
            continue
        assert kind not in ("image", "media", "font"), f"{kind} request {url}"
        assert not re.search(r"\.(png|jpe?g|gif|webp|avif|mp4|webm|woff2?|ttf|otf)$", path), url


def test_pages_load_nothing_from_other_origins(page):
    """Every request a page makes stays on the app's own origin."""
    seen = collect_requests(page)
    for path in ("/", "/collections/luggage", "/products/passage-luggage-cabin", "/checkout"):
        open_page(page, path)
    origin = urllib.parse.urlparse(app_url())
    for url, _kind in seen:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme in ("data", "blob"):
            continue
        assert (parsed.scheme, parsed.netloc) == (origin.scheme, origin.netloc), url


def test_timestamps_are_utc_strings(customer):
    """Timestamps end in Z and dates are YYYY-MM-DD."""
    stamp = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z")
    current = sale()
    assert stamp.fullmatch(current["ends_at"]) and stamp.fullmatch(current["server_time"]), current
    assert stamp.fullmatch(login_response(CUSTOMER_EMAIL, SEEDED_PASSWORD).json()["expires_at"])
    with api(customer) as client:
        for row in top_level_array(client.get("/me/orders")):
            assert stamp.fullmatch(row["placed_at"]), row
    assert stamp.fullmatch(movements("PCK-CUB-HTG")[0]["created_at"])
    with api() as client:
        estimate = client.get("/delivery-estimate", params={"method": STANDARD}).json()
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", estimate["from"]), estimate


def test_list_endpoints_return_arrays(customer):
    """List endpoints return top-level arrays; collection and search return their objects."""
    token = owner_token()
    with api() as client:
        top_level_array(client.get("/collections"))
        top_level_array(client.get("/stores"))
        assert isinstance(client.get("/collections/luggage/products").json()["products"], list)
        assert isinstance(client.get("/search", params={"q": "olive"}).json()["products"], list)
    with api(customer) as client:
        top_level_array(client.get("/me/orders"))
        top_level_array(client.get("/me/addresses"))
    with api(token) as client:
        top_level_array(client.get("/owner/orders"))
        top_level_array(client.get("/owner/stock-movements", params={"sku": "PCK-CUB-HTG"}))


def test_derived_figures_are_not_stored_columns():
    """Stock, discount, badge, units sold, members, sums and windows are never columns."""
    tables = {r["table_name"] for r in sql(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")}
    assert set(TABLES) <= tables, sorted(set(TABLES) - tables)
    for table, column in DERIVED_COLUMNS:
        assert column not in table_columns(table), f"{table}.{column} is a stored column"
