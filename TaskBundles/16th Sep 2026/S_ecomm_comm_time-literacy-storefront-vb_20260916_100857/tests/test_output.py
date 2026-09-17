"""Graded substeps for deku/time-literacy-storefront-vb.

One module. API assertions go through the routes the brief pins, stored state through
the backend capability, invoices through the payments capability, mail through the inbox
capability, and rendered surfaces through Playwright pages. A browser cannot tell a real
Kill Bill invoice or a stored hold from a success screen, which is why those live here.
Nothing in this file imports the agent's code or assumes its framework.
"""

from __future__ import annotations

import html
import os
import re
from urllib.parse import urlparse

import httpx
from appclient import client
from conftest import (
    ABOUT_CLOSE, ADDRESS_NEEDED_PREFIX, ANIMATION_SAMPLE_JS, ANIMATION_WATCH_JS, ANNOUNCEMENT,
    AQUA, BLACK38, BUNDLE_BLACK_NAVY, BUNDLE_GLOW_GLOW, BUNDLE_GREY_AQUA, BUNDLE_SHARK_FUCHSIA,
    CART_COPY, CHECKOUT_FIELDS, COLLECTIONS, COLLECTION_TITLES, COMPARISON_TIMES,
    COMPLETE_SET_NOTICE, CONFIRMATION_PREFIX, CONTENTION_ROUNDS, CONTENTION_WRITERS, CONTENT_PAGES,
    CONTRAST_JS, CUSTOMER2_EMAIL, CUSTOMER2_NAME, CUSTOMER_EMAIL, CUSTOMER_NAME, DANA_BODY,
    DANA_REPLY, DERIVED_COLUMNS, DISCLAIMER, DISCLAIMER_PLACEMENT_JS, DOT_LINKS_JS,
    EDITORIAL_HEADINGS, ELAPSED_WATCH_JS, FAQ_BATTERY_ANSWER, FAQ_QUESTIONS, FUCHSIA,
    GIFT_PROMOTION, GLOW33, GLOW38, GREY38, GRID_COLUMNS_JS, GRID_COLUMN_COUNT_JS,
    GUIDE_CLOSING_STEP, GUIDE_HEADINGS, HOME_COPY, HOME_H2_HEADINGS, HOME_SECTION_MARKERS,
    KEYFRAME_WATCH_JS, LABEL_WATCH_JS, LILAC_DRAFT, LINE_FIELDS, LINK_MARKER, MARKETING_SUBJECT_RE,
    MINT31, NATO_AQUA, NATO_NAVY, NAVY, NAV_LINKS, NOTIFICATION_WATCH_JS, ORDER_FIELDS,
    ORDER_LINE_FIELDS, ORDER_NUMBER_RE, OWNER_EMAIL, OWNER_NAME, PO_BOX_RULE, PRICE_AQUA,
    PRICE_NATO, PRICE_TOTE, PRODUCT_COPY, PRODUCT_ELEMENT_FIELDS, PROGRESS_WATCH_JS,
    PROMOTION_REMOVED_MESSAGE, PUBLIC_ROUTES, PUBLISHED_HANDLES, RAIL_CARDS_JS, RAIL_REGION_JS,
    REFERENCE_RE, RESTOCK_PREFIX, RUBBER_NAVY, SCRIPT_RE, SEEDED_PASSWORD, SEED_BUNDLES,
    SEED_REVIEWS, SEED_SKUS, SEND_NEW_LINK, SETTER_ROWS_JS, SHARK38, SIGN_IN_SUBJECT,
    SIZE_STATE_JS, SKU_AQUA, SKU_BEANIE, SKU_BLACK38, SKU_BUNDLE_BLACK_NAVY, SKU_BUNDLE_GLOW_GLOW,
    SKU_BUNDLE_GREY_AQUA, SKU_FUCHSIA, SKU_GLOW33, SKU_GLOW38, SKU_GREY38, SKU_LILAC,
    SKU_NATO_AQUA, SKU_NATO_NAVY, SKU_NAVY, SKU_RUBBER_FUCHSIA_L, SKU_RUBBER_NAVY_L,
    SKU_RUBBER_NAVY_S, SKU_SHARK38, SKU_TOTE, SKU_WOVEN_SAND_L, SKU_WOVEN_SAND_S, SOUND_WATCH_JS,
    SPEC_KEYS, SPENT_LINK_COPY, STICKY_BAR_JS, STRUCK_PRICE_JS, STYLE_SNAPSHOT_JS, TABLET_VIEWPORT,
    TABLE_COLUMNS, TAB_STOPS_JS, TAG_RE, TARGET_SIZES_JS, TOCK31_CHANGES, TOCK31_NOTICE,
    TOCK33_SPECS, TOCK38_CHANGES, TOCK_STARTS, TOTE, TOTE_UNAVAILABLE_MESSAGE, UI_TIMEOUT_MS,
    UNIT_COUNT_KEYS, WORDMARK_OFFSET_JS, WOVEN_SAND, _surface, added_cart, adjust, all_titles,
    api_url, base_url, cart_add, cart_control, cart_delete, cart_get, cart_patch, checkout,
    collection_json, comparison_slider, consume_link, dial, dial_state, ensure_available,
    expect_client_error, gift_lines, handles_of, html_text, internal_hrefs, killbill_account,
    killbill_accounts_keyed, killbill_invoices, killbill_invoices_for_key, latest_link_token,
    line_for, lines_of, link_token_from_mail, lowered_text, mail_subjects, main_text,
    messages_with_subject, new_cart, normalise_text, ok_json, own_orders, page_html,
    pending_review, place_order, poll_until, product_image_markup, product_json, public_reviews,
    race, redirect_target, request_link, run_control, safe_json, set_available, setter_option,
    settle, signup, sitemap_locations, slide_to, slider_value, smallest_container, stock_row,
    stock_rows, swatch, ui_add_to_cart, ui_sign_in, unique_email, unique_key, unique_title,
    us_address, utc_now, visible_named, visit, wide_surface, write_review
)
from playwright.sync_api import expect


def test_tock_33_collection_offers_four_colourways(anon_client):
    """The TOCK 33 collection holds exactly the four colourways.

    cov: C-OV-01
    """
    collection = collection_json(anon_client, "tock-33")
    colourways = sorted(p.get("colourway") for p in collection.get("products", []))
    assert colourways == ["aqua", "fuchsia", "glow", "navy"], (
        f"/api/collections/tock-33 offers colourways {colourways}, expected aqua, fuchsia, "
        f"glow and navy")


def test_catalogue_offers_watch_case_sizes_33_or_38(anon_client):
    """Every TOCK 33 watch is 33mm and every TOCK 38 watch is 38mm.

    cov: C-OV-02
    """
    for handle, size in (("tock-33", 33), ("tock-38", 38)):
        products = collection_json(anon_client, handle).get("products", [])
        assert len(products) == 4, f"/api/collections/<handle> {handle} lists {handles_of(products)}"
        sizes = {int(p.get("case_size")) for p in products}
        assert sizes == {size}, f"/api/collections/<handle> {handle} case sizes are {sizes}, expected {size}"


def test_visitor_fills_cart_without_account(carts, anon_client):
    """An anonymous visitor adds a line to a cart with no bearer token.

    cov: C-RL-01
    """
    token = carts()
    cart = added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    line = line_for(cart, SKU_NATO_AQUA)
    assert line is not None and int(line.get("quantity")) == 1, (
        f"an anonymous cart did not keep the NATO Strap Aqua line: {cart}")


def test_visitor_without_account_cannot_place_order(carts, anon_client):
    """Checkout with a cart token but no bearer token is denied and the cart keeps its line.

    cov: C-RL-02
    """
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    response = checkout(anon_client, token, unique_key())
    expect_client_error(response, "anonymous POST /api/checkout")
    cart = ok_json(cart_get(anon_client, token), "GET /api/cart after a denied checkout")
    assert line_for(cart, SKU_NATO_AQUA) is not None, (
        f"a denied anonymous checkout emptied the cart: {cart}")


def test_customer_calling_owner_endpoint_denied(customer_client):
    """A customer reading the owner console endpoints is denied.

    cov: C-RL-03
    """
    for path in ("/owner/reviews", "/owner/stock"):
        response = customer_client.get(path)
        expect_client_error(response, f"customer GET /api{path}")
        assert not isinstance(safe_json(response), list), (
            f"customer GET /api{path} was refused with a status but still carried the list: "
            f"{response.text[:300]}")


def test_no_account_field_collects_child_name_age_or_birthday(customer_client, db):
    """Neither the accounts table nor the account endpoint holds a child's details.

    cov: C-RL-04
    """
    row = db.account(CUSTOMER_EMAIL)
    assert row is not None, "the accounts table holds no row for customer@example.com"
    account = ok_json(customer_client.get("/account"), "GET /api/account")
    for keys, where in ((row.keys(), "accounts table"), (account.keys(), "GET /api/account")):
        child_keys = [k for k in keys
                      if "child" in k.lower() or "birth" in k.lower() or k.lower() == "age"
                      or k.lower().endswith("_age")]
        assert not child_keys, f"the {where} carries child fields {child_keys}"


def test_every_seeded_account_signs_in_with_password(anon_client):
    """Each seeded account logs in with the literal fixture password.

    cov: C-RL-05
    """
    for email in (CUSTOMER_EMAIL, CUSTOMER2_EMAIL, OWNER_EMAIL):
        response = anon_client.post("/auth/login",
                                    json={"email": email, "password": "deku-demo-pw-2026"})
        payload = ok_json(response, f"POST /api/auth/login for {email}")
        assert payload.get("access_token"), f"login for {email} returned no access_token"


def test_seeded_customer_account_named_casey_rivera(customer_client):
    """customer@example.com is a customer named Casey Rivera.

    cov: C-RL-06
    """
    account = ok_json(customer_client.get("/account"), "GET /api/account")
    assert (account.get("email"), account.get("name"), account.get("role")) == (
        CUSTOMER_EMAIL, CUSTOMER_NAME, "customer"), f"GET /api/account returned {account}"


def test_seeded_customer2_account_named_jordan_lee(customer2_client):
    """customer2@example.com is a customer named Jordan Lee.

    cov: C-RL-07
    """
    account = ok_json(customer2_client.get("/account"), "GET /api/account")
    assert (account.get("email"), account.get("name"), account.get("role")) == (
        CUSTOMER2_EMAIL, CUSTOMER2_NAME, "customer"), f"GET /api/account returned {account}"


def test_seeded_owner_account_named_mara_ellison(owner_client):
    """owner@example.com is the owner named Mara Ellison.

    cov: C-RL-08
    """
    account = ok_json(owner_client.get("/account"), "GET /api/account")
    assert (account.get("email"), account.get("name"), account.get("role")) == (
        OWNER_EMAIL, OWNER_NAME, "owner"), f"GET /api/account returned {account}"


def test_open_signup_creates_customer_account(db):
    """A fresh visitor signs up and holds one customer account row.

    cov: C-RL-09
    """
    email, token = signup(name="Probe Signup")
    with client(token) as c:
        account = ok_json(c.get("/account"), "GET /api/account after signup")
    assert account.get("role") == "customer" and account.get("email") == email, (
        f"signup for {email} produced account {account}")
    assert db.count_accounts(email) == 1, (
        f"the accounts table holds {db.count_accounts(email)} rows for {email}, expected 1")


def test_signup_returns_access_token(anon_client):
    """Signup answers with an access token that authenticates the account endpoint.

    cov: C-CF-01
    """
    email = unique_email()
    response = anon_client.post("/auth/signup", json={"email": email, "password": "probe-pass-2026x",
                                                      "name": "Probe Token"})
    token = ok_json(response, "POST /api/auth/signup").get("access_token")
    assert token, f"signup returned no access_token: {response.text[:400]}"
    with client(token) as c:
        assert c.get("/account").status_code == 200, "the signup token does not authenticate"


def test_login_seeded_customer_password_returns_access_token(anon_client):
    """Login with the seeded customer password returns a working access token.

    cov: C-CF-02
    """
    response = anon_client.post("/auth/login",
                                json={"email": CUSTOMER_EMAIL, "password": SEEDED_PASSWORD})
    token = ok_json(response, "POST /api/auth/login").get("access_token")
    assert token, f"login returned no access_token: {response.text[:400]}"
    with client(token) as c:
        account = ok_json(c.get("/account"), "GET /api/account with the login token")
    assert account.get("email") == CUSTOMER_EMAIL, f"the login token belongs to {account}"


def test_signup_already_registered_email_rejected_without_second_account_row(anon_client, db):
    """A second signup with a registered email is rejected and writes no second row.

    cov: C-CF-03
    """
    email, _ = signup()
    response = anon_client.post("/auth/signup", json={"email": email, "password": "another-pass-2026",
                                                      "name": "Probe Duplicate"})
    expect_client_error(response, f"a second POST /api/auth/signup for {email}")
    assert db.count_accounts(email) == 1, (
        f"the accounts table holds {db.count_accounts(email)} rows for {email} after a duplicate")


def test_signup_password_shorter_than_10_characters_rejected(anon_client, db):
    """A nine character password is rejected and no account is written.

    cov: C-CF-04
    """
    email = unique_email()
    response = anon_client.post("/auth/signup",
                                json={"email": email, "password": "short-9ch", "name": "Probe Short"})
    expect_client_error(response, "POST /api/auth/signup with a 9 character password")
    assert db.count_accounts(email) == 0, f"a rejected signup still wrote an account for {email}"


def test_login_wrong_password_denied(anon_client):
    """A wrong password is denied without issuing a token.

    cov: C-CF-05
    """
    response = anon_client.post("/auth/login",
                                json={"email": CUSTOMER_EMAIL, "password": "not-the-password-1"})
    expect_client_error(response, "POST /api/auth/login with a wrong password")
    assert not (safe_json(response) or {}).get("access_token"), (
        f"a wrong password still issued a token: {response.text[:300]}")


def test_sign_in_link_request_answers_same_body_for_unknown_address(anon_client):
    """The link request answers identically for a known and an unknown address.

    cov: C-CF-06
    """
    known = request_link(CUSTOMER_EMAIL)
    unknown = request_link(unique_email())
    assert known.status_code == unknown.status_code and known.status_code in (200, 201, 202), (
        f"link request statuses differ or failed: known {known.status_code}, "
        f"unknown {unknown.status_code}")
    assert known.json() == unknown.json() == {"status": "sent"}, (
        f"link request bodies differ: known {known.text[:200]}, unknown {unknown.text[:200]}")


def test_sign_in_link_email_arrives_with_subject(inbox):
    """The link mail carries the exact subject and opens with an account link.

    cov: C-CF-07, C-CF-201
    """
    email = unique_email()
    assert request_link(email).status_code in (200, 201, 202), "POST /api/auth/link failed"
    message = poll_until(lambda: inbox.find(to=email, subject_contains=SIGN_IN_SUBJECT))
    assert message is not None, f"no sign-in mail reached {email} within the polling window"
    assert message.subject == SIGN_IN_SUBJECT, f"the sign-in mail subject is {message.subject!r}"
    assert message.body.strip().startswith(f"{base_url()}{LINK_MARKER}"), (
        f"the sign-in mail does not open with {base_url()}{LINK_MARKER}<token>: "
        f"{message.body[:300]!r}")
    settle(2.0)
    count = len([s for s in mail_subjects(inbox, email) if s == SIGN_IN_SUBJECT])
    assert count == 1, f"one link request sent {count} sign-in mails"


def test_consuming_sign_in_link_for_new_address_creates_customer_account(inbox, db):
    """Consuming a link for an address with no account creates a customer account.

    cov: C-CF-08, C-CF-253
    """
    email = unique_email()
    request_link(email)
    token = link_token_from_mail(inbox, email)
    assert token, f"no sign-in link token could be read from the mail to {email}"
    payload = ok_json(consume_link(token), "POST /api/auth/link/consume")
    assert payload.get("access_token"), f"consume returned no access_token: {payload}"
    with client(payload["access_token"]) as c:
        account = ok_json(c.get("/account"), "GET /api/account with the link token")
    assert account.get("email") == email and account.get("role") == "customer", (
        f"the link signed in as {account}, expected a customer {email}")
    assert db.count_accounts(email) == 1, f"the accounts table holds {db.count_accounts(email)} rows"
    assert "return_to" in payload, f"consume returned no return_to: {payload}"
    assert not str(db.account(email).get("password_hash") or ""), "a link-only account stored a password hash"


def test_consumed_sign_in_link_refused_on_second_use(inbox):
    """The same link token is refused the second time and issues no token.

    cov: C-CF-09
    """
    email = unique_email()
    request_link(email)
    token = link_token_from_mail(inbox, email)
    assert token, f"no sign-in link token could be read from the mail to {email}"
    ok_json(consume_link(token), "the first POST /api/auth/link/consume")
    second = consume_link(token)
    expect_client_error(second, "a second POST /api/auth/link/consume of one token")
    assert not (safe_json(second) or {}).get("access_token"), (
        f"a spent link issued a token: {second.text[:300]}")


def test_external_return_to_comes_back_as_account(inbox):
    """An absolute or protocol-relative return_to comes back as /account.

    cov: C-CF-10
    """
    for target in ("https://elsewhere.example/", "//elsewhere.example/account"):
        email = unique_email()
        request_link(email, return_to=target)
        token = link_token_from_mail(inbox, email)
        assert token, f"no sign-in link token could be read from the mail to {email}"
        payload = ok_json(consume_link(token), f"consume for return_to {target}")
        assert payload.get("return_to") == "/account", (
            f"return_to {target!r} came back as {payload.get('return_to')!r}, expected /account")
    email = unique_email()
    request_link(email, return_to="/checkout")
    token = link_token_from_mail(inbox, email)
    assert token, f"no sign-in link token could be read from the mail to {email}"
    relative = ok_json(consume_link(token), "consume for a relative return_to").get("return_to")
    assert relative == "/checkout", f"a relative return_to came back as {relative!r}"


def test_spent_sign_in_link_page_offers_send_new_link(inbox):
    """Opening a spent link shows the no-longer-valid copy with Send a new link.

    cov: C-CF-11
    """
    email = unique_email()
    request_link(email)
    token = link_token_from_mail(inbox, email)
    assert token, f"no sign-in link token could be read from the mail to {email}"
    ok_json(consume_link(token), "POST /api/auth/link/consume")
    response = httpx.get(f"{base_url()}{LINK_MARKER}{token}", timeout=30.0, follow_redirects=True)
    text = normalise_text(TAG_RE.sub(" ", SCRIPT_RE.sub(" ", response.text)))
    assert SPENT_LINK_COPY in text and SEND_NEW_LINK in text, (
        f"{LINK_MARKER}<spent token> does not show {SPENT_LINK_COPY!r} with {SEND_NEW_LINK!r}: "
        f"{text[:400]!r}")


def test_resend_call_mails_fresh_link_to_spent_token_address(inbox, anon_client):
    """Resend with a spent token mails a different link to the same address.

    cov: C-CF-12
    """
    email = unique_email()
    request_link(email)
    first = link_token_from_mail(inbox, email)
    assert first, f"no sign-in link token could be read from the mail to {email}"
    ok_json(consume_link(first), "POST /api/auth/link/consume")
    response = anon_client.post("/auth/link/resend", json={"token": first})
    assert ok_json(response, "POST /api/auth/link/resend") == {"status": "sent"}, response.text[:300]

    def fresh_token():
        token = latest_link_token(inbox, email)
        return token if token and token != first else None

    fresh = poll_until(fresh_token)
    assert fresh, f"no second sign-in link with a new token reached {email}"
    payload = ok_json(consume_link(fresh), "consuming the resent link")
    assert payload.get("access_token"), f"the resent link issued no token: {payload}"


def test_resend_unissued_token_rejected(anon_client):
    """Resend with a token the shop never issued is rejected.

    cov: C-CF-13
    """
    response = anon_client.post("/auth/link/resend", json={"token": f"never-issued-{unique_key()}"})
    expect_client_error(response, "POST /api/auth/link/resend with an unissued token")


def test_account_endpoint_returns_email_name_role(customer_client):
    """GET /api/account carries email, name and role.

    cov: C-CF-14
    """
    account = ok_json(customer_client.get("/account"), "GET /api/account")
    missing = [k for k in ("email", "name", "role") if k not in account]
    assert not missing, f"GET /api/account lacks {missing}: {account}"


def test_account_patch_rejects_child_name_or_birthday_field(fresh_customer):
    """PATCH /api/account with child_name or child_birthday is rejected and writes nothing.

    cov: C-CF-15
    """
    email, buyer = fresh_customer
    before = ok_json(buyer.get("/account"), "GET /api/account")
    for body in ({"name": "Changed Name", "child_name": "Robin"},
                 {"child_birthday": "2019-05-01"}):
        response = buyer.patch("/account", json=body)
        expect_client_error(response, f"PATCH /api/account with {sorted(body)}")
    after = ok_json(buyer.get("/account"), "GET /api/account after the rejected patches")
    assert after.get("name") == before.get("name"), (
        f"a rejected patch still changed the name from {before.get('name')!r} to {after.get('name')!r}")


def test_calls_to_account_order_checkout_review_owner_without_bearer_token_denied(carts, anon_client):
    """Account, order, checkout, review-writing and owner calls with no token are denied.

    cov: C-CF-16
    """
    token = carts()
    calls = [("GET", "/account", None, None), ("GET", "/orders", None, None),
             ("GET", "/orders/TK-SEEDED01", None, None),
             ("POST", "/checkout", {"shipping_address": us_address()},
              {"X-Cart-Token": token, "Idempotency-Key": unique_key()}),
             ("POST", f"/products/{WOVEN_SAND}/reviews",
              {"rating": 5, "title": "Anonymous", "body": "No token.", "mentions_minor": False}, None),
             ("GET", "/owner/reviews", None, None), ("GET", "/owner/stock", None, None),
             ("POST", "/owner/stock-adjustments",
              {"sku": SKU_NATO_AQUA, "delta": 1, "reason": "anonymous"}, None)]
    for method, path, body, headers in calls:
        response = anon_client.request(method, path, json=body, headers=headers)
        expect_client_error(response, f"anonymous {method} /api{path}")

def test_selecting_tock_turns_bezel_by_start_minute_minus_tock_start_times_six(page):
    """Each tock turns the ring by (start minute - tock start) * 6 mod 360.

    cov: C-CF-17
    """
    visit(page, "/")
    for length in (5, 10, 15, 30):
        setter_option(page, f"{length} min").click()
        expect(dial(page, "hero")).to_have_attribute("data-segment-minutes", str(length))
        state = dial_state(page, "hero")
        start = int(state["start"])
        assert 0 <= start <= 59, f"data-start-minute reads {state['start']!r}, outside 0 to 59"
        expected = ((start - TOCK_STARTS[length]) * 6) % 360
        assert int(state["rotation"]) == expected, (
            f"{length} min started at minute {start}: data-bezel-rotation reads "
            f"{state['rotation']!r}, expected {expected}")


def test_hero_dial_bezel_rotation_stays_from_0_to_359_for_every_tock_length(page):
    """The bezel rotation is a whole number from 0 to 359 for all four tocks.

    cov: C-CF-18
    """
    visit(page, "/")
    for length in (5, 10, 15, 30):
        setter_option(page, f"{length} min").click()
        expect(dial(page, "hero")).to_have_attribute("data-segment-minutes", str(length))
        rotation = dial_state(page, "hero")["rotation"] or ""
        assert re.fullmatch(r"\d{1,3}", rotation) and 0 <= int(rotation) <= 359, (
            f"{length} min: data-bezel-rotation reads {rotation!r}, expected a whole number 0 to 359")


def test_timer_setter_single_choice_group_of_four_options(page):
    """The setter is one radio group holding exactly the four tock options.

    cov: C-CF-19
    """
    visit(page, "/")
    group = page.get_by_role("radiogroup").filter(has=setter_option(page, "15 min")).first
    expect(group).to_be_visible()
    assert group.get_by_role("radio").count() == 4, (
        f"the timer setter group holds {group.get_by_role('radio').count()} options, expected 4")
    for label in ("5 min", "10 min", "15 min", "30 min"):
        assert group.get_by_role("radio", name=label, exact=True).count() == 1, (
            f"the timer setter group has no single option named {label!r}")


def test_timer_setter_selects_15_min_when_home_page_loads(page):
    """15 min is the selected option on load.

    cov: C-CF-20
    """
    visit(page, "/")
    expect(setter_option(page, "15 min")).to_be_checked()
    for label in ("5 min", "10 min", "30 min"):
        expect(setter_option(page, label)).not_to_be_checked()


def test_arrow_keys_move_timer_setter_selection(page):
    """ArrowRight and ArrowLeft move the selected tock.

    cov: C-CF-21
    """
    visit(page, "/")
    setter_option(page, "15 min").focus()
    page.keyboard.press("ArrowRight")
    expect(setter_option(page, "30 min")).to_be_checked()
    expect(dial(page, "hero")).to_have_attribute("data-segment-minutes", "30")
    page.keyboard.press("ArrowLeft")
    expect(setter_option(page, "15 min")).to_be_checked()


def test_run_a_tock_fills_elapsed_minutes_up_to_tock_length(page):
    """Run a tock climbs data-elapsed-minutes to 15 within ten seconds, never past it.

    cov: C-CF-22
    """
    visit(page, "/")
    expect(dial(page, "hero")).to_have_attribute("data-segment-minutes", "15")
    page.evaluate(ELAPSED_WATCH_JS)
    run_control(page).click()
    expect(dial(page, "hero")).to_have_attribute("data-elapsed-minutes", re.compile(r"^15(\.0+)?$"),
                                                 timeout=10500)
    peak = page.evaluate("() => window.__probePeakElapsed")
    assert peak <= 15, f"data-elapsed-minutes climbed to {peak}, past the 15 minute tock"


def test_run_a_tock_ends_by_saying_tock_complete(page):
    """The run ends with Tock complete inside a polite live region.

    cov: C-CF-23
    """
    visit(page, "/")
    run_control(page).click()
    region = page.locator("[aria-live='polite'], [role='status']").filter(has_text="Tock complete").first
    expect(region).to_be_visible(timeout=12000)


def test_under_reduced_motion_run_completes_at_once(reduced_page):
    """With reduced motion the run fills the tock and says Tock complete at once.

    cov: C-CF-24
    """
    visit(reduced_page, "/")
    expect(dial(reduced_page, "hero")).to_have_attribute("data-segment-minutes", "15")
    run_control(reduced_page).click()
    expect(dial(reduced_page, "hero")).to_have_attribute(
        "data-elapsed-minutes", re.compile(r"^15(\.0+)?$"), timeout=1000)
    expect(reduced_page.get_by_text("Tock complete").first).to_be_visible(timeout=1000)


def test_demo_never_plays_a_sound(page):
    """Running a tock starts no audio source and plays no media element.

    cov: C-CF-25
    """
    page.add_init_script(SOUND_WATCH_JS)
    visit(page, "/")
    run_control(page).click()
    expect(page.get_by_text("Tock complete").first).to_be_visible(timeout=12000)
    sounds = page.evaluate("() => window.__probeSounds")
    assert sounds == 0, f"the demonstration started {sounds} sound(s)"


def test_demo_never_requests_notification_permission(page):
    """Running a tock never asks for notification permission.

    cov: C-CF-26
    """
    page.add_init_script(NOTIFICATION_WATCH_JS)
    visit(page, "/")
    setter_option(page, "5 min").click()
    run_control(page).click()
    expect(page.get_by_text("Tock complete").first).to_be_visible(timeout=12000)
    asks = page.evaluate("() => window.__probeNotificationAsks")
    assert asks == 0, f"the demonstration asked for notification permission {asks} time(s)"


def test_pressing_colourway_swatch_sets_dial_colourway(page):
    """Each swatch sets data-colourway and shows as pressed.

    cov: C-CF-27
    """
    visit(page, "/")
    for name in ("Navy", "Fuchsia", "Glow", "Aqua"):
        swatch(page, name).click()
        expect(dial(page, "hero")).to_have_attribute("data-colourway", name.lower())
        expect(swatch(page, name)).to_have_attribute("aria-pressed", "true")


def test_exactly_one_colourway_swatch_shows_pressed(page):
    """After pressing Fuchsia exactly one of the four swatches is pressed.

    cov: C-CF-28
    """
    visit(page, "/")
    swatch(page, "Fuchsia").click()
    expect(swatch(page, "Fuchsia")).to_have_attribute("aria-pressed", "true")
    pressed = [name for name in ("Aqua", "Navy", "Fuchsia", "Glow")
               if swatch(page, name).get_attribute("aria-pressed") == "true"]
    assert pressed == ["Fuchsia"], f"pressed swatches read {pressed}, expected only Fuchsia"


def test_on_load_aqua_swatch_pressed_with_15_min_tock_set_on_hero_dial(page):
    """On load Aqua is pressed, the dial is aqua and a 15 minute tock is set.

    cov: C-CF-29
    """
    visit(page, "/")
    expect(swatch(page, "Aqua")).to_have_attribute("aria-pressed", "true")
    state = dial_state(page, "hero")
    assert (state["colourway"], state["segment"]) == ("aqua", "15"), (
        f"on load the hero dial reads colourway {state['colourway']!r} and tock "
        f"{state['segment']!r}, expected aqua and 15")


def test_hero_dial_text_alternative_names_colourway_time_tock_length(page):
    """The hero dial image is named <Colourway> dial at <h:mm> with a <length> minute tock set.

    cov: C-CF-30
    """
    visit(page, "/")
    expect(page.get_by_role("img", name=re.compile(
        r"^Aqua dial at (1[0-2]|[1-9]):[0-5]\d with a 15 minute tock set$")).first).to_be_attached()
    swatch(page, "Navy").click()
    setter_option(page, "30 min").click()
    expect(page.get_by_role("img", name=re.compile(
        r"^Navy dial at (1[0-2]|[1-9]):[0-5]\d with a 30 minute tock set$")).first).to_be_attached()


def test_when_dial_cannot_be_drawn_hero_drops_setter_card(noscript_page):
    """Without scripts to draw the dial the setter card is removed, never left inert.

    cov: C-CF-31
    """
    response = visit(noscript_page, "/")
    assert response is not None and response.status == 200, "the home page did not load without scripts"
    expect(noscript_page.get_by_text("Try it. Set a tock and watch closely")).to_be_hidden()
    expect(noscript_page.get_by_role("radio", name="15 min")).to_be_hidden()


def test_move_the_time_slider_runs_from_0_to_719_starting_at_158(page):
    """The comparison slider is a 0 to 719 range in steps of 1 starting at 158.

    cov: C-CF-32
    """
    visit(page, "/")
    slider = comparison_slider(page)
    bounds = slider.evaluate(
        "e => e.tagName === 'INPUT' ? [e.min, e.max, e.step || '1', e.value]"
        " : [e.getAttribute('aria-valuemin'), e.getAttribute('aria-valuemax'), '1',"
        " e.getAttribute('aria-valuenow')]")
    assert [float(v) for v in bounds] == [0, 719, 1, 158], (
        f"Move the time reads min, max, step, value {bounds}, expected 0, 719, 1, 158")


def test_arrow_keys_move_comparison_slider_one_minute(page):
    """ArrowRight adds one minute and ArrowLeft takes one away.

    cov: C-CF-33
    """
    visit(page, "/")
    slider = comparison_slider(page)
    slider.focus()
    slider.press("ArrowRight")
    assert slider_value(slider) == 159, f"ArrowRight moved the slider to {slider_value(slider)}"
    slider.press("ArrowLeft")
    slider.press("ArrowLeft")
    assert slider_value(slider) == 157, f"two ArrowLeft presses left the slider at {slider_value(slider)}"


def test_page_keys_move_comparison_slider_one_hour(page):
    """PageUp adds sixty minutes and PageDown takes sixty away.

    cov: C-CF-34
    """
    visit(page, "/")
    slider = comparison_slider(page)
    slider.focus()
    slider.press("PageUp")
    assert slider_value(slider) == 218, f"PageUp moved the slider to {slider_value(slider)}"
    slider.press("PageDown")
    slider.press("PageDown")
    assert slider_value(slider) == 98, f"two PageDown presses left the slider at {slider_value(slider)}"


def test_both_comparison_dials_hour_rotation_follows_slider_time(page):
    """Both comparison dials carry (hour mod 12) * 30 + minute * 0.5 at five times.

    cov: C-CF-35
    """
    visit(page, "/")
    slider = comparison_slider(page)
    for value, clock, rotation, _, _, _ in COMPARISON_TIMES:
        slide_to(slider, value)
        for role in ("plain", "zoned"):
            expect(dial(page, role)).to_have_attribute(
                "data-hour-rotation", re.compile(rf"^{re.escape(rotation)}(\.0)?$"))


def test_tock_dial_lights_current_hour_zone(page):
    """The zoned dial carries the current hour in data-lit-hour at five times.

    cov: C-CF-36
    """
    visit(page, "/")
    slider = comparison_slider(page)
    for value, clock, _, lit, _, _ in COMPARISON_TIMES:
        slide_to(slider, value)
        expect(dial(page, "zoned")).to_have_attribute("data-lit-hour", lit)


def test_conventional_dial_caption_generated_from_slider_time(page):
    """The left caption reads Somewhere between H and N? for the slider time.

    cov: C-CF-37
    """
    visit(page, "/")
    slider = comparison_slider(page)
    for value, clock, _, _, left, _ in COMPARISON_TIMES:
        slide_to(slider, value)
        expect(page.get_by_text(re.compile(re.escape(left))).first).to_be_visible()


def test_tock_dial_caption_generated_from_slider_time(page):
    """The right caption reads It's in the H. H:MM. for the slider time.

    cov: C-CF-38
    """
    visit(page, "/")
    slider = comparison_slider(page)
    for value, clock, _, _, _, right in COMPARISON_TIMES:
        slide_to(slider, value)
        pattern = re.escape(right).replace("'", "['" + chr(0x2019) + "]")
        expect(page.get_by_text(re.compile(pattern)).first).to_be_visible()


def test_comparison_dial_text_alternatives_follow_slider(page):
    """The dial images are named Conventional dial at h:mm and Tock dial at h:mm with the H zone lit.

    cov: C-CF-39
    """
    visit(page, "/")
    slider = comparison_slider(page)
    for value, clock, _, lit, _, _ in COMPARISON_TIMES[:3]:
        slide_to(slider, value)
        expect(page.get_by_role("img", name=f"Conventional dial at {clock}", exact=True).first).to_be_attached()
        expect(page.get_by_role("img", name=f"Tock dial at {clock} with the {lit} zone lit",
                                exact=True).first).to_be_attached()


def test_home_page_sections_follow_stated_order():
    """The nine home sections appear in the stated order in the first HTML.

    cov: C-CF-40
    """
    status, text = html_text("/")
    assert status == 200, f"GET / returned {status}"
    lowered = text.lower()
    positions = [(marker, lowered.find(marker.lower())) for marker in HOME_SECTION_MARKERS]
    missing = [marker for marker, at in positions if at < 0]
    assert not missing, f"the home page lacks the section markers {missing}"
    order = [at for _, at in positions]
    assert order == sorted(order), (
        f"home sections are out of order: {[(m, at) for m, at in positions]}")


def test_home_page_has_one_level_one_heading():
    """The home page carries exactly one h1, and the section headings open at level two.

    cov: C-CF-41
    """
    response = page_html("/")
    count = len(re.findall(r"<h1[\s>]", response.text, re.I))
    assert count == 1, f"the home page carries {count} h1 elements, expected 1"
    headings = [normalise_text(TAG_RE.sub(" ", h)).lower()
                for h in re.findall(r"<h2\b[^>]*>(.*?)</h2>", response.text, re.S | re.I)]
    for heading in HOME_H2_HEADINGS:
        assert any(heading.lower() in h for h in headings), f"the home heading {heading!r} is not an h2"


def test_range_eyebrow_price_is_lowest_in_stock_price_of_family(owner_client):
    """The TOCK 33 eyebrow follows the lowest in-stock price, moving to $229.00 without Aqua.

    cov: C-CF-42
    """
    aqua_before = int(ensure_available(owner_client, SKU_AQUA, 4)["available"])
    ensure_available(owner_client, SKU_GLOW33, 1)
    ensure_available(owner_client, SKU_GREY38, 1)
    _, text = html_text("/")
    assert "Premium kids' watch - From $189.00" in text, (
        "the TOCK 33 eyebrow does not read Premium kids' watch - From $189.00")
    assert "The grown-up one - From $379.00" in text, (
        "the TOCK 38 eyebrow does not read The grown-up one - From $379.00")
    set_available(owner_client, SKU_AQUA, 2)
    try:
        _, low_text = html_text("/")
        assert "Premium kids' watch - From $189.00" in low_text, (
            "with TOCK 33 Aqua low on stock the eyebrow no longer reads From $189.00")
        set_available(owner_client, SKU_AQUA, 0)
        _, sold_out_text = html_text("/")
        assert "Premium kids' watch - From $229.00" in sold_out_text, (
            "with TOCK 33 Aqua sold out the eyebrow does not read From $229.00")
    finally:
        set_available(owner_client, SKU_AQUA, aqua_before)


def test_sold_out_range_card_shows_sold_out_without_add_control(page, owner_client):
    """The TOCK 33 Navy card shows Sold out and carries no add control.

    cov: C-CF-43, C-CF-254
    """
    set_available(owner_client, SKU_NAVY, 0)
    visit(page, "/")
    card = smallest_container(page, ["TOCK 33 Navy", "Sold out"])
    assert card is not None, "no element on the home page holds TOCK 33 Navy beside Sold out"
    adds = card.evaluate(
        "e => Array.from(e.querySelectorAll('button, a, input[type=submit]'))"
        ".filter(c => /add/i.test((c.getAttribute('aria-label') || '') + ' ' + (c.innerText || c.value || ''))).length")
    assert adds == 0, f"the sold-out TOCK 33 Navy card carries {adds} add control(s)"
    ensure_available(owner_client, SKU_AQUA, 4)
    visit(page, "/")
    card = smallest_container(page, ["TOCK 33 Aqua", "$189.00"])
    assert card is not None, "no range card shows TOCK 33 Aqua with its $189.00 price"


def test_walkthrough_stage_dials_show_elapsed_minutes_0_15_30(page):
    """Three stage dials carry elapsed minutes 0, 15 and 30.

    cov: C-CF-44
    """
    visit(page, "/")
    stages = page.locator("[data-dial='stage']")
    expect(stages).to_have_count(3)
    values = [stages.nth(i).get_attribute("data-elapsed-minutes") for i in range(3)]
    assert [float(v) for v in values] == [0, 15, 30], f"stage dials read elapsed {values}"


def test_testimonials_disclaimer_sits_inside_testimonials_section(page):
    """The disclaimer shares its section with the testimonials heading, never the footer.

    cov: C-CF-45
    """
    visit(page, "/")
    verdict = page.evaluate(DISCLAIMER_PLACEMENT_JS)
    assert verdict == "inside", f"the testimonials disclaimer placement reads {verdict!r}"
    _, text = html_text("/")
    assert DISCLAIMER in text, "the testimonials disclaimer differs from the pinned wording"


def test_bundle_band_shows_grey_aqua_bundle_card_with_add_control(page, owner_client):
    """The bundle band shows the Grey and Aqua Bundle with its price and an add control.

    cov: C-CF-46, C-CF-229
    """
    ensure_available(owner_client, SKU_GREY38, 1)
    ensure_available(owner_client, SKU_AQUA, 1)
    visit(page, "/")
    band = smallest_container(page, ["ONE FOR YOU, ONE FOR MINI-YOU", "Grey and Aqua Bundle"])
    assert band is not None, "no home section holds the bundle band heading with the Grey and Aqua Bundle"
    adds = band.evaluate(
        "e => Array.from(e.querySelectorAll('button, a, input[type=submit]'))"
        ".filter(c => /add/i.test((c.getAttribute('aria-label') || '') + ' ' + (c.innerText || c.value || ''))).length")
    assert adds >= 1, "the bundle band card carries no add control"
    assert "$469.00" in normalise_text(band.inner_text()), "the bundle band card does not show the $469.00 bundle price"


def test_home_reassurance_row_shows_returns_warranty_age_cells():
    """The home reassurance row carries the returns, warranty and age cells.

    cov: C-CF-47
    """
    _, text = html_text("/")
    lowered = text.lower()
    for cell in ("30 day returns", "Any reason", "2 year warranty", "Movement and build", "4+",
                 "Ages 4 and up", "No reading needed"):
        assert cell.lower() in lowered, f"the home reassurance row lacks {cell!r}"


def test_announcement_bar_shows_whenever_both_gift_items_have_stock(owner_client):
    """With tote and beanie in stock the announcement runs on every page.

    cov: C-CF-48
    """
    ensure_available(owner_client, SKU_TOTE, 50)
    ensure_available(owner_client, SKU_BEANIE, 50)
    for path in ("/", "/collections/all", "/pages/about"):
        _, text = html_text(path)
        assert ANNOUNCEMENT.lower() in text.lower(), f"{path} lacks the announcement {ANNOUNCEMENT!r}"


def test_announcement_bar_hides_whenever_gift_item_has_no_stock(owner_client):
    """With the tote out of stock the announcement is absent from every page.

    cov: C-CF-49
    """
    tote_before = int(ensure_available(owner_client, SKU_TOTE, 50)["available"])
    ensure_available(owner_client, SKU_BEANIE, 50)
    set_available(owner_client, SKU_TOTE, 0)
    try:
        for path in ("/", "/collections/all", "/pages/about"):
            _, text = html_text(path)
            assert ANNOUNCEMENT.lower() not in text.lower(), (
                f"{path} still shows the announcement while the tote has no stock")
    finally:
        set_available(owner_client, SKU_TOTE, tote_before)

def test_collections_list_only_published_products(anon_client):
    """No collection or search lists the draft lilac, and all lists exactly the published twenty.

    cov: C-CF-50
    """
    for handle in COLLECTIONS:
        products = collection_json(anon_client, handle).get("products", [])
        assert LILAC_DRAFT not in handles_of(products), f"/api/collections/<handle> {handle} lists the draft lilac"
    listed = sorted(handles_of(collection_json(anon_client, "all").get("products", [])))
    assert listed == sorted(PUBLISHED_HANDLES), (
        f"/api/collections/<handle> all lists {listed}, expected exactly the published products")
    search = ok_json(anon_client.get("/search", params={"q": "lilac"}), "GET /api/search?q=lilac")
    assert search == [], f"searching lilac returned the draft product: {search}"


def test_all_collection_count_is_20(anon_client):
    """The all collection counts twenty published products.

    cov: C-CF-51
    """
    collection = collection_json(anon_client, "all")
    assert collection.get("count") == 20, f"/api/collections/<handle> all count reads {collection.get('count')!r}"
    assert collection.get("title") == "Shop All", f"the all collection is titled {collection.get('title')!r}"
    filtered = collection_json(anon_client, "all", {"availability": "in_stock"})
    assert filtered.get("count") == 20, f"count under an availability filter reads {filtered.get('count')!r}"


def test_unpublished_lilac_product_page_answers_not_found(anon_client):
    """The draft lilac product page and API both answer 404.

    cov: C-CF-52
    """
    page_status = page_html(f"/products/{LILAC_DRAFT}").status_code
    api_status = anon_client.get(f"/products/{LILAC_DRAFT}").status_code
    assert (page_status, api_status) == (404, 404), (
        f"the draft lilac answered page {page_status} and API {api_status}, expected 404 and 404")


def test_reviews_or_restock_requests_on_unpublished_lilac_handle_answer_not_found(anon_client, fresh_customer, db):
    """Reviews and restock requests on the draft lilac answer 404 and write nothing.

    cov: C-CF-53
    """
    email, author = fresh_customer
    product = db.product(LILAC_DRAFT)
    assert product is not None, "the products table holds no tock-33-lilac row"
    assert anon_client.get(f"/products/{LILAC_DRAFT}/reviews").status_code == 404, (
        "GET reviews for the draft lilac did not answer 404")
    review = write_review(author, LILAC_DRAFT, unique_title())
    assert review.status_code == 404, f"a review on the draft lilac answered {review.status_code}"
    restock = anon_client.post(f"/products/{LILAC_DRAFT}/restock-subscriptions", json={"email": email})
    assert restock.status_code == 404, f"a restock request on the draft lilac answered {restock.status_code}"
    account = db.account(email)
    assert db.count_reviews(product["id"], account["id"]) == 0, "a review row was written on the draft lilac"
    assert db.subscriptions(product["id"], email) == [], "a restock row was written on the draft lilac"


def test_collection_filters_narrow_products_by_colourway_availability_price_band(anon_client, owner_client):
    """Colourway, availability and price band filters each narrow the products they return.

    cov: C-CF-54, C-CF-237, C-CF-238
    """
    glow = collection_json(anon_client, "tock-33", {"colourway": "glow"})
    assert handles_of(glow.get("products", [])) == [GLOW33], f"colourway=glow returned {handles_of(glow['products'])}"
    for value, allowed in (("in_stock", {"in_stock", "low_stock"}), ("sold_out", {"out_of_stock", "unavailable"})):
        products = collection_json(anon_client, "all", {"availability": value}).get("products", [])
        wrong = [(p["handle"], p["availability"]) for p in products if p.get("availability") not in allowed]
        assert products and not wrong, f"availability={value} returned {wrong or 'nothing'}"
    band = collection_json(anon_client, "all", {"price_band": "300-499"}).get("products", [])
    assert sorted(handles_of(band)) == sorted([GREY38, BLACK38, GLOW38, SHARK38, BUNDLE_GREY_AQUA,
                                               BUNDLE_BLACK_NAVY]), (
        f"price_band=300-499 returned {sorted(handles_of(band))}")
    under = collection_json(anon_client, "all", {"price_band": "under-100"}).get("products", [])
    assert all(int(p["price"]) < 10000 for p in under) and len(under) == 8, (
        f"price_band=under-100 returned {[(p['handle'], p['price']) for p in under]}")
    family = collection_json(anon_client, "all", {"family": "tock-38"}).get("products", [])
    assert family and all(p.get("family") == "tock-38" for p in family), f"family=tock-38 returned {handles_of(family)}"
    sized = collection_json(anon_client, "all", {"case_size": "33"}).get("products", [])
    assert sized and all(str(p.get("case_size")) == "33" for p in sized), f"case_size=33 returned {handles_of(sized)}"
    for band in ("100-299", "500-plus"):
        assert anon_client.get("/collections/all", params={"price_band": band}).status_code == 200, f"price_band={band} was refused"
    before = int(stock_row(owner_client, SKU_GLOW38)["available"])
    set_available(owner_client, SKU_GLOW38, 2)
    set_available(owner_client, SKU_NAVY, 0)
    try:
        in_stock = handles_of(collection_json(anon_client, "all", {"availability": "in_stock"}).get("products", []))
        sold_out = handles_of(collection_json(anon_client, "all", {"availability": "sold_out"}).get("products", []))
        assert GLOW38 in in_stock, "availability=in_stock leaves out the low-stock TOCK 38 Glow"
        assert BUNDLE_BLACK_NAVY in sold_out, "availability=sold_out leaves out the unavailable Black and Navy Bundle"
    finally:
        set_available(owner_client, SKU_GLOW38, before)


def test_collection_page_keeps_engaged_filters_in_address(page):
    """Engaging In stock writes availability=in_stock into the address, and reopening keeps it.

    cov: C-CF-55, C-CF-263
    """
    visit(page, "/collections/tock-33?sort=price-desc")
    option = page.get_by_text(re.compile(r"^\s*In stock")).first
    if not option.is_visible():
        page.get_by_role("button", name=re.compile(r"Filter")).first.click()
    option.click()
    page.wait_for_url(re.compile(r"availability=in_stock"))
    reopened = page.url
    visit(page, reopened.replace(base_url(), ""))
    expect(page.get_by_text("Counts show in-stock items only").first).to_be_visible()
    assert "sort=price-desc" in page.url, f"engaging a filter dropped the sort from the address: {page.url}"


def test_unknown_collection_filter_or_sort_value_rejected_naming_parameter(anon_client):
    """Unknown filter names and values, and unknown sorts, are rejected naming the parameter.

    cov: C-CF-56
    """
    for params, name in (({"material": "steel"}, "material"), ({"sort": "cheapest"}, "sort"),
                         ({"availability": "maybe"}, "availability"),
                         ({"price_band": "cheap"}, "price_band"), ({"colourway": "plaid"}, "colourway")):
        response = anon_client.get("/collections/all", params=params)
        expect_client_error(response, f"GET /api/collections/<handle> all {params}")
        assert name in response.text, f"the rejection of {params} does not name {name!r}: {response.text[:300]}"


def test_collection_product_elements_carry_listed_product_fields(anon_client):
    """Every collection product element carries the twelve listed fields.

    cov: C-CF-57
    """
    fields = {"handle", "title", "family", "colourway", "case_size", "price", "compare_at_price",
              "currency", "availability", "rating_average", "review_count", "siblings"}
    collection = collection_json(anon_client, "all")
    for key in ("handle", "title", "notice", "count", "counts_reflect", "facets", "sort_options", "products"):
        assert key in collection, f"/api/collections/<handle> all lacks {key!r}"
    for product in collection["products"]:
        missing = sorted(fields - set(product))
        assert not missing, f"product {product.get('handle')} lacks {missing}"


def test_single_value_facet_left_out_unless_engaged(anon_client, owner_client):
    """TOCK 33 facets offer colourway and availability only, until case_size is engaged.

    cov: C-CF-58, C-CF-240
    """
    ensure_available(owner_client, SKU_AQUA, 1)
    set_available(owner_client, SKU_NAVY, 0)
    facets = collection_json(anon_client, "tock-33").get("facets", {})
    assert set(facets) == {"colourway", "availability"}, f"/api/collections/tock-33 facets are {sorted(facets)}"
    engaged = collection_json(anon_client, "tock-33", {"case_size": "33"}).get("facets", {})
    assert "case_size" in engaged, f"with case_size engaged the facets are {sorted(engaged)}"
    for name, values in facets.items():
        assert all({"value", "count"} <= set(v) for v in values), f"facet {name} entries lack value or count: {values}"


def test_counts_reflect_equals_engaged_availability_value(anon_client):
    """counts_reflect reads all, in_stock or sold_out with the availability filter.

    cov: C-CF-59
    """
    for params, expected in ((None, "all"), ({"availability": "in_stock"}, "in_stock"),
                             ({"availability": "sold_out"}, "sold_out")):
        value = collection_json(anon_client, "all", params).get("counts_reflect")
        assert value == expected, f"counts_reflect with {params} reads {value!r}, expected {expected!r}"


def test_grid_note_states_whether_counts_include_sold_out_items():
    """The grid note names which counts are shown.

    cov: C-CF-60
    """
    for query, note in (("", "Counts include sold-out items"),
                        ("?availability=in_stock", "Counts show in-stock items only"),
                        ("?availability=sold_out", "Counts show sold-out items only")):
        _, text = html_text(f"/collections/all{query}")
        assert note in text, f"/collections/all{query} does not say {note!r}"


def test_best_rated_sort_offered_only_with_enough_reviewed_products(anon_client):
    """TOCK 33 offers best-rated while TOCK 38 and TOCK 31 do not.

    cov: C-CF-61
    """
    base = {"featured", "price-asc", "price-desc", "newest"}
    tock33 = set(collection_json(anon_client, "tock-33").get("sort_options", []))
    assert tock33 == base | {"best-rated"}, f"tock-33 sort options are {sorted(tock33)}"
    for handle in ("tock-38", "tock-31"):
        options = set(collection_json(anon_client, handle).get("sort_options", []))
        assert options == base, f"{handle} sort options are {sorted(options)}, expected no best-rated"


def test_price_asc_sort_orders_products_by_price_then_title(anon_client):
    """price-asc orders by price, then by title on equal prices.

    cov: C-CF-62, C-CF-241
    """
    products = collection_json(anon_client, "all", {"sort": "price-asc"}).get("products", [])
    pairs = [(int(p["price"]), p["title"]) for p in products]
    assert pairs == sorted(pairs), f"price-asc returned {pairs}"
    assert [p["title"] for p in products[:4]] == ["Tock Tote", "NATO Strap Aqua", "NATO Strap Navy", "Tock Beanie"], (
        f"price-asc opens with {[p['title'] for p in products[:4]]}")
    desc = collection_json(anon_client, "all", {"sort": "price-desc"}).get("products", [])
    keyed = [(-int(p["price"]), p["title"]) for p in desc]
    assert keyed == sorted(keyed), f"price-desc returned {[(p['price'], p['title']) for p in desc]}"


def test_empty_filtered_grid_offers_clear_control_per_engaged_filter(anon_client):
    """A known value matching nothing empties the grid, which offers Clear per filter.

    cov: C-CF-63, C-CF-239
    """
    empty = collection_json(anon_client, "tock-38", {"colourway": "aqua"})
    assert empty.get("products") == [], f"tock-38 colourway=aqua returned {handles_of(empty.get('products', []))}"
    _, text = html_text("/collections/tock-38?colourway=aqua&availability=in_stock")
    for copy in ("No products match these filters.", "Clear Colourway", "Clear Availability"):
        assert copy in text, f"the empty filtered grid lacks {copy!r}"


def test_tock_31_collection_carries_discontinued_notice(anon_client):
    """The tock-31 collection carries the discontinued notice in JSON and on the page.

    cov: C-CF-64
    """
    assert collection_json(anon_client, "tock-31").get("notice") == TOCK31_NOTICE, "the tock-31 notice differs"
    _, text = html_text("/collections/tock-31")
    assert TOCK31_NOTICE in text, "/collections/tock-31 does not show the discontinued notice"


def test_filter_control_shows_word_filter_at_narrow_width(narrow_page):
    """At 390px the filter control still shows the word Filter.

    cov: C-CF-65
    """
    visit(narrow_page, "/collections/all")
    count = visible_named(narrow_page, "button, a, summary, label, [role=button]", r"\bFilter\b")
    assert count >= 1, "no visible control shows the word Filter at 390px"


def test_sort_control_shows_word_sort_at_narrow_width(narrow_page):
    """At 390px the sort control still shows the word Sort.

    cov: C-CF-66
    """
    visit(narrow_page, "/collections/all")
    count = visible_named(narrow_page, "button, a, summary, label, select, [role=button], [role=combobox]",
                          r"\bSort\b")
    assert count >= 1, "no visible control shows the word Sort at 390px"


def test_density_control_sets_grid_column_count(page, anon_client):
    """Choosing 2 columns then 4 columns sets the grid to that many columns.

    cov: C-CF-67, C-FE-12
    """
    titles = [p["title"] for p in collection_json(anon_client, "all").get("products", [])]
    visit(page, "/collections/all")
    for label, columns in (("2 columns", 2), ("4 columns", 4)):
        control = (page.get_by_role("button", name=label, exact=True)
                   .or_(page.get_by_role("radio", name=label, exact=True))
                   .or_(page.get_by_role("link", name=label, exact=True))).first
        control.click()
        expect(control).to_be_visible()
        page.wait_for_function(GRID_COLUMNS_JS, arg=[titles, columns], timeout=UI_TIMEOUT_MS)
    for label in ("1 column", "2 columns", "3 columns", "4 columns"):
        found = (page.get_by_role("button", name=label, exact=True).or_(page.get_by_role("radio", name=label, exact=True))
                 .or_(page.get_by_role("link", name=label, exact=True))).count()
        assert found >= 1, f"the density control offers no {label!r}"


def test_colourway_dots_link_to_sibling_product_page(page):
    """A colourway dot on a TOCK 33 card is a link that opens the sibling page.

    cov: C-CF-68
    """
    visit(page, "/collections/tock-33")
    dots = page.evaluate(DOT_LINKS_JS)
    assert f"/products/{NAVY}" in dots, f"no colourway dot links to /products/{NAVY}; dot links are {dots}"
    page.locator(f"[data-probe-dot='{NAVY}']").first.click()
    page.wait_for_url(re.compile(rf"/products/{NAVY}$"))


def test_superseded_grey_copy_handle_redirects_permanently():
    """tock-38-grey-copy answers a permanent redirect to tock-38-grey.

    cov: C-CF-69
    """
    status, location = redirect_target("/products/tock-38-grey-copy")
    assert status in (301, 308) and location == f"/products/{GREY38}", (
        f"/products/tock-38-grey-copy answered {status} to {location!r}")


def test_superseded_shark_handle_redirects_permanently():
    """tock-33-shark answers a permanent redirect to tock-38-shark.

    cov: C-CF-70
    """
    status, location = redirect_target("/products/tock-33-shark")
    assert status in (301, 308) and location == f"/products/{SHARK38}", (
        f"/products/tock-33-shark answered {status} to {location!r}")


def test_search_returns_published_products_matching_title(anon_client):
    """Searching AQUA returns the three published products whose title holds aqua.

    cov: C-CF-71
    """
    response = anon_client.get("/search", params={"q": "AQUA"})
    results = ok_json(response, "GET /api/search?q=AQUA")
    assert isinstance(results, list), f"search is not a top-level array: {response.text[:300]}"
    assert sorted(handles_of(results)) == sorted([AQUA, NATO_AQUA, BUNDLE_GREY_AQUA]), (
        f"search AQUA returned {handles_of(results)}")
    _, text = html_text("/search?q=aqua")
    assert "TOCK 33 Aqua" in text and "NATO Strap Aqua" in text, "/search?q=aqua does not list the aqua products"
    assert all(PRODUCT_ELEMENT_FIELDS <= set(r) for r in results), "a search result lacks the collection product fields"


def test_empty_search_query_returns_empty_array(anon_client):
    """An empty q returns an empty array.

    cov: C-CF-72
    """
    assert ok_json(anon_client.get("/search", params={"q": ""}), "GET /api/search?q=") == []


def test_product_endpoint_returns_named_product_fields(anon_client):
    """The product endpoint returns the named fields, and a bundle adds its three.

    cov: C-CF-73
    """
    product = product_json(anon_client, AQUA)
    for key in ("handle", "title", "kind", "family", "colourway", "case_size", "price", "compare_at_price",
                "currency", "availability", "variants", "specifications", "rating_average", "review_count",
                "rating_histogram", "siblings"):
        assert key in product, f"GET /api/products/<handle> {AQUA} lacks {key!r}"
    variant = product["variants"][0]
    assert {"sku", "option", "price", "availability"} <= set(variant), f"variant lacks fields: {variant}"
    assert {"key", "value"} <= set(product["specifications"][0]), f"specification lacks fields"
    assert {"handle", "colourway"} <= set(product["siblings"][0]), f"sibling lacks fields"
    bundle = product_json(anon_client, BUNDLE_GREY_AQUA)
    for key in ("components", "missing_components", "saving"):
        assert key in bundle, f"GET /api/products/<handle> {BUNDLE_GREY_AQUA} lacks {key!r}"


def test_product_availability_moves_through_stock_levels_with_units_available(anon_client, owner_client):
    """TOCK 38 Shark reads in_stock at 4, low_stock at 3 and 1, out_of_stock at 0.

    cov: C-CF-74
    """
    before = int(stock_row(owner_client, SKU_SHARK38)["available"])
    try:
        for units, expected in ((4, "in_stock"), (3, "low_stock"), (1, "low_stock"), (0, "out_of_stock")):
            set_available(owner_client, SKU_SHARK38, units)
            value = product_json(anon_client, SHARK38).get("availability")
            assert value == expected, f"with {units} available TOCK 38 Shark reads {value!r}, expected {expected!r}"
    finally:
        set_available(owner_client, SKU_SHARK38, before)


def test_strap_with_sizes_takes_availability_of_best_stocked_size(anon_client, owner_client):
    """Woven Strap Sand follows its better stocked size.

    cov: C-CF-75
    """
    small = int(stock_row(owner_client, SKU_WOVEN_SAND_S)["available"])
    large = int(stock_row(owner_client, SKU_WOVEN_SAND_L)["available"])
    try:
        for s_units, l_units, expected in ((2, 0, "low_stock"), (0, 5, "in_stock"), (0, 0, "out_of_stock")):
            set_available(owner_client, SKU_WOVEN_SAND_S, s_units)
            set_available(owner_client, SKU_WOVEN_SAND_L, l_units)
            value = product_json(anon_client, WOVEN_SAND).get("availability")
            assert value == expected, f"Small {s_units}, Large {l_units}: the strap reads {value!r}, expected {expected!r}"
    finally:
        set_available(owner_client, SKU_WOVEN_SAND_S, small)
        set_available(owner_client, SKU_WOVEN_SAND_L, large)


def test_low_stock_page_shows_only_few_left_never_units_count(anon_client, owner_client):
    """At two units TOCK 38 Glow says Only a few left and states no count anywhere.

    cov: C-CF-76
    """
    before = int(stock_row(owner_client, SKU_GLOW38)["available"])
    set_available(owner_client, SKU_GLOW38, 2)
    try:
        _, text = html_text(f"/products/{GLOW38}")
        assert "Only a few left" in text, "the low stock page does not say Only a few left"
        assert not re.search(r"\b2\s+(left|in stock|units?|remaining|available)\b|only 2\b", text, re.I), (
            "the low stock page states how many units are left")
        product = product_json(anon_client, GLOW38)
        leaked = [k for k in product if k in UNIT_COUNT_KEYS]
        leaked += [k for v in product.get("variants", []) for k in v if k in UNIT_COUNT_KEYS]
        assert not leaked, f"GET /api/products/<handle> {GLOW38} states unit counts in {leaked}"
    finally:
        set_available(owner_client, SKU_GLOW38, before)


def test_add_control_passes_through_adding_to_cart_before_added_to_cart(page, owner_client):
    """The add control reads Adding to Cart before Added to Cart.

    cov: C-CF-77
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 5)
    visit(page, f"/products/{NATO_AQUA}")
    page.evaluate(LABEL_WATCH_JS)
    page.get_by_role("button", name="Add to Cart", exact=True).first.click()
    expect(page.get_by_role("button", name="Added to Cart").first).to_be_visible()
    seen = page.evaluate("() => window.__probeLabels")
    assert "Adding to Cart" in seen and seen.index("Adding to Cart") < seen.index("Added to Cart"), (
        f"the add control labels seen were {seen}")


def test_out_of_stock_product_shows_restock_form_instead_of_add_control(owner_client):
    """NATO Strap Navy at zero shows the restock form and its price, and no add control.

    cov: C-CF-78
    """
    set_available(owner_client, SKU_NATO_NAVY, 0)
    _, text = html_text(f"/products/{NATO_NAVY}")
    for copy in ("Item is out of stock", "Email me when it is back", "$22.00"):
        assert copy in text, f"the out-of-stock NATO Strap Navy page lacks {copy!r}"
    assert "Add to Cart" not in text, "the out-of-stock NATO Strap Navy page still offers Add to Cart"


def test_sold_out_strap_size_shows_as_unavailable(page, owner_client):
    """A sold-out Large size is shown as unavailable rather than removed.

    cov: C-CF-79
    """
    ensure_available(owner_client, SKU_WOVEN_SAND_S, 5)
    set_available(owner_client, SKU_WOVEN_SAND_L, 0)
    visit(page, f"/products/{WOVEN_SAND}")
    verdict = page.evaluate(SIZE_STATE_JS, "Large")
    assert verdict == "unavailable", f"the sold-out Large size reads {verdict!r}"
    assert page.evaluate(SIZE_STATE_JS, "Small") == "available", "the stocked Small size is not offered"


def test_tock_31_sale_shows_compare_at_price_with_save_amount(anon_client, page):
    """TOCK 31 Mint shows Sale, Save $40.00 and $99.00 struck through beside $59.00.

    cov: C-CF-80
    """
    mint = product_json(anon_client, MINT31)
    assert (mint.get("price"), mint.get("compare_at_price")) == (5900, 9900), f"TOCK 31 Mint prices {mint}"
    visit(page, f"/products/{MINT31}")
    text = main_text(page)
    for copy in ("Sale", "Save $40.00", "$59.00", "$99.00"):
        assert copy in text, f"the TOCK 31 Mint page lacks {copy!r}"
    struck = page.evaluate(STRUCK_PRICE_JS, "$99.00")
    assert struck, "the $99.00 compare-at price is not struck through"


def test_watch_specification_lists_fourteen_keys_in_fixed_order(anon_client):
    """The specifications list and the page definition list carry the fourteen keys in order.

    cov: C-CF-81
    """
    keys = [s.get("key") for s in product_json(anon_client, AQUA).get("specifications", [])]
    assert keys == SPEC_KEYS, f"API specification keys are {keys}"
    markup = page_html(f"/products/{AQUA}").text
    terms = [normalise_text(TAG_RE.sub(" ", t)) for t in re.findall(r"<dt\b[^>]*>(.*?)</dt>", markup, re.S | re.I)]
    listed = [t for t in terms if t in SPEC_KEYS]
    assert listed == SPEC_KEYS, f"the page definition list terms are {terms}"
    assert "Specifications" in normalise_text(TAG_RE.sub(" ", markup)), "the watch page has no Specifications block"


def test_product_reassurance_row_carries_shipping_returns_warranty_cells():
    """A TOCK 38 page carries the shipping, returns and warranty cells.

    cov: C-CF-82
    """
    _, text = html_text(f"/products/{GREY38}")
    for cell in ("Swiftpost 2 day in the US", "Flat $15", "30 day returns", "Any reason", "2 year warranty",
                 "Movement and build"):
        assert cell.lower() in text.lower(), f"the TOCK 38 Grey reassurance row lacks {cell!r}"


def test_tock_33_reassurance_row_adds_age_cell():
    """TOCK 33 and bundle pages add the 4+ age cell.

    cov: C-CF-83
    """
    for path in (f"/products/{AQUA}", f"/products/{BUNDLE_GREY_AQUA}"):
        _, text = html_text(path)
        for cell in ("4+", "Ages 4 and up", "No reading needed"):
            assert cell.lower() in text.lower(), f"{path} lacks the age cell text {cell!r}"


def test_carousel_position_text_moves_with_arrow_keys(page):
    """Arrow keys inside the product carousel move 1 of 4 to 2 of 4.

    cov: C-CF-84
    """
    visit(page, f"/products/{AQUA}")
    group = page.get_by_role("group").filter(has_text="1 of 4").first
    expect(group).to_be_visible()
    group.locator("button").first.focus()
    page.keyboard.press("ArrowRight")
    expect(page.get_by_text("2 of 4").first).to_be_visible()
    page.keyboard.press("ArrowLeft")
    expect(page.get_by_text("1 of 4").first).to_be_visible()


def test_zoom_dialog_closes_on_escape_returning_focus(page):
    """The zoom dialog takes focus, closes on Escape and hands focus back to the zoom control.

    cov: C-CF-85, C-CF-232
    """
    visit(page, f"/products/{AQUA}")
    zoom = page.get_by_role("button", name=re.compile(r"zoom", re.I)).first
    zoom.click()
    dialog = page.get_by_role("dialog").first
    expect(dialog).to_be_visible()
    assert dialog.evaluate("d => d.contains(document.activeElement)"), "the open zoom dialog did not take focus"
    page.keyboard.press("Escape")
    expect(dialog).to_be_hidden()
    assert zoom.evaluate("e => e === document.activeElement"), "focus did not return to the zoom control"


def test_watch_page_carries_seven_editorial_block_headings():
    """A watch page carries all seven editorial headings.

    cov: C-CF-86
    """
    _, text = html_text(f"/products/{AQUA}")
    missing = [h for h in EDITORIAL_HEADINGS if h not in text]
    assert not missing, f"the TOCK 33 Aqua page lacks the editorial headings {missing}"


def test_related_products_rail_lists_family_colourways():
    """The Related products rail lists the other TOCK 33 colourways.

    cov: C-CF-87
    """
    _, text = html_text(f"/products/{AQUA}")
    at = text.find("Related products")
    assert at >= 0, "the TOCK 33 Aqua page has no Related products rail"
    rail = text[at:]
    missing = [t for t in ("TOCK 33 Navy", "TOCK 33 Fuchsia", "TOCK 33 Glow") if t not in rail]
    assert not missing, f"the Related products rail lacks {missing}"


def test_bundle_owns_no_stock_row(owner_client, db):
    """No bundle sku has an owner stock row or an inventory_items row.

    cov: C-CF-88
    """
    skus = [row.get("sku") for row in stock_rows(owner_client)]
    assert not [s for s in skus if str(s).startswith("BNDL-")], f"owner stock lists bundle rows {skus}"
    for sku in (SKU_BUNDLE_GREY_AQUA, SKU_BUNDLE_BLACK_NAVY):
        variant = db.variant(sku)
        assert variant is not None, f"no variants row for {sku}"
        assert db.count_inventory_for_variant(variant["id"]) == 0, f"{sku} owns an inventory_items row"


def test_bundle_availability_follows_smaller_watch_count(anon_client, owner_client):
    """Glow and Glow reads low_stock, in_stock and unavailable from its two watches.

    cov: C-CF-89
    """
    big = int(stock_row(owner_client, SKU_GLOW38)["available"])
    small = int(stock_row(owner_client, SKU_GLOW33)["available"])
    try:
        for glow38, glow33, expected in ((2, 6, "low_stock"), (5, 4, "in_stock"), (5, 3, "low_stock"),
                                         (5, 0, "unavailable")):
            set_available(owner_client, SKU_GLOW38, glow38)
            set_available(owner_client, SKU_GLOW33, glow33)
            value = product_json(anon_client, BUNDLE_GLOW_GLOW).get("availability")
            assert value == expected, (
                f"with TK38-GLOW {glow38} and TK33-GLOW {glow33} the bundle reads {value!r}, expected {expected!r}")
    finally:
        set_available(owner_client, SKU_GLOW38, big)
        set_available(owner_client, SKU_GLOW33, small)


def test_bundle_missing_watch_unavailable_listing_missing_watch_title(anon_client, owner_client):
    """Black and Navy lists TOCK 33 Navy as missing, and Grey and Aqua lists nothing.

    cov: C-CF-90
    """
    set_available(owner_client, SKU_NAVY, 0)
    ensure_available(owner_client, SKU_BLACK38, 1)
    ensure_available(owner_client, SKU_GREY38, 1)
    ensure_available(owner_client, SKU_AQUA, 1)
    black_navy = product_json(anon_client, BUNDLE_BLACK_NAVY)
    assert black_navy.get("availability") == "unavailable", f"Black and Navy reads {black_navy.get('availability')!r}"
    assert black_navy.get("missing_components") == ["TOCK 33 Navy"], (
        f"Black and Navy missing_components reads {black_navy.get('missing_components')!r}")
    assert product_json(anon_client, BUNDLE_GREY_AQUA).get("missing_components") == [], (
        "Grey and Aqua lists a missing watch while both are available")


def test_bundle_components_list_both_watches(anon_client):
    """Grey and Aqua components name both watches with title, availability and quantity.

    cov: C-CF-91
    """
    components = product_json(anon_client, BUNDLE_GREY_AQUA).get("components", [])
    assert sorted(handles_of(components)) == sorted([GREY38, AQUA]), f"components are {components}"
    for component in components:
        assert {"handle", "title", "availability", "quantity"} <= set(component), f"component lacks fields: {component}"
        assert int(component["quantity"]) == 1, f"component quantity reads {component['quantity']}"


def test_bundle_page_names_missing_watch_with_restock_form(anon_client, owner_client):
    """The Black and Navy page names TOCK 33 Navy with a restock form, and the bundle takes no subscription.

    cov: C-CF-92, C-CF-219
    """
    set_available(owner_client, SKU_NAVY, 0)
    _, text = html_text(f"/products/{BUNDLE_BLACK_NAVY}")
    for copy in ("Item is unavailable", "This bundle is unavailable because TOCK 33 Navy is out of stock.",
                 "Email me when it is back"):
        assert copy in text, f"the Black and Navy Bundle page lacks {copy!r}"
    response = anon_client.post(f"/products/{BUNDLE_BLACK_NAVY}/restock-subscriptions", json={"email": unique_email()})
    expect_client_error(response, "a restock subscription on a bundle")


def test_bundle_compare_at_price_sums_watch_prices(anon_client):
    """Each bundle compare-at price sums its watches and saving is that sum minus the price.

    cov: C-CF-93
    """
    for handle in (BUNDLE_BLACK_NAVY, BUNDLE_GREY_AQUA, BUNDLE_GLOW_GLOW, BUNDLE_SHARK_FUCHSIA):
        bundle = product_json(anon_client, handle)
        total = sum(int(product_json(anon_client, c["handle"])["price"]) * int(c.get("quantity", 1))
                    for c in bundle.get("components", []))
        assert int(bundle.get("compare_at_price")) == total, f"{handle} compare_at_price {bundle.get('compare_at_price')} != {total}"
        assert int(bundle.get("saving")) == total - int(bundle["price"]), f"{handle} saving {bundle.get('saving')}"


def test_black_navy_bundle_page_shows_save_69():
    """The Black and Navy Bundle page shows Save $69.00.

    cov: C-CF-94
    """
    _, text = html_text(f"/products/{BUNDLE_BLACK_NAVY}")
    assert "Save $69.00" in text, "the Black and Navy Bundle page does not show Save $69.00"


def test_bundle_buy_box_shows_complete_set_returns_notice():
    """A bundle page carries the complete-set returns notice.

    cov: C-CF-95
    """
    _, text = html_text(f"/products/{BUNDLE_GREY_AQUA}")
    assert COMPLETE_SET_NOTICE in text, "the Grey and Aqua Bundle page lacks the complete-set returns notice"

def test_published_reviews_render_in_first_html_of_product_page():
    """The first HTML of the aqua page already carries its published reviews.

    cov: C-CF-96
    """
    response = page_html(f"/products/{AQUA}")
    assert response.status_code == 200, f"GET /products/{AQUA} returned {response.status_code}"
    text = normalise_text(TAG_RE.sub(" ", SCRIPT_RE.sub(" ", response.text)))
    for copy in ("Fewer questions in the car", "Strap tore at the buckle holes", "Priya"):
        assert copy in text, f"the first HTML of the aqua page lacks the published review text {copy!r}"


def test_aqua_review_summary_shows_4_1_based_on_7_reviews(anon_client):
    """TOCK 33 Aqua shows 4.1 based on 7 reviews on the page and in the API.

    cov: C-CF-97
    """
    product = product_json(anon_client, AQUA)
    assert (product.get("rating_average"), product.get("review_count")) == (4.1, 7), (
        f"aqua rating reads {product.get('rating_average')!r} from {product.get('review_count')!r}")
    _, text = html_text(f"/products/{AQUA}")
    assert "4.1" in text and "Based on 7 reviews" in text, "the aqua page does not show 4.1 and Based on 7 reviews"


def test_pending_review_neither_listed_nor_counted(fresh_customer, anon_client):
    """A pending review changes neither the list, the count nor the page.

    cov: C-CF-98
    """
    _, author = fresh_customer
    before = product_json(anon_client, WOVEN_SAND).get("review_count")
    review = pending_review(author, WOVEN_SAND)
    after = product_json(anon_client, WOVEN_SAND).get("review_count")
    assert after == before, f"a pending review moved review_count from {before} to {after}"
    titles = [r.get("title") for r in public_reviews(anon_client, WOVEN_SAND)]
    assert review["title"] not in titles, "the pending review is listed publicly"
    _, text = html_text(f"/products/{WOVEN_SAND}")
    assert review["title"] not in text, "the pending review shows on the product page"


def test_rating_histogram_counts_published_reviews(anon_client):
    """The aqua histogram maps 5 to 1 onto the published counts.

    cov: C-CF-99
    """
    product = product_json(anon_client, AQUA)
    histogram = {str(k): int(v) for k, v in (product.get("rating_histogram") or {}).items()}
    assert histogram == {"5": 4, "4": 2, "3": 0, "2": 0, "1": 1}, f"aqua rating_histogram reads {histogram}"
    assert sum(histogram.values()) == product.get("review_count"), "the histogram does not sum to review_count"


def test_histogram_text_alternative_gives_counts():
    """The aqua page carries the histogram text alternative with the counts.

    cov: C-CF-100
    """
    markup = normalise_text(page_html(f"/products/{AQUA}").text)
    assert "5 stars: 4, 4 stars: 2, 3 stars: 0, 2 stars: 0, 1 star: 1" in markup, (
        "the aqua page lacks the histogram text alternative 5 stars: 4, 4 stars: 2, 3 stars: 0, 2 stars: 0, 1 star: 1")


def test_reviews_rating_filter_returns_only_that_rating(anon_client):
    """rating=1 returns Dana's review alone and rating=5 returns four five-star reviews.

    cov: C-CF-101
    """
    ones = public_reviews(anon_client, AQUA, rating=1)
    assert [r.get("author_name") for r in ones] == ["Dana"], f"rating=1 returned {ones}"
    fives = public_reviews(anon_client, AQUA, rating=5)
    assert len(fives) == 4 and all(int(r.get("rating")) == 5 for r in fives), f"rating=5 returned {fives}"
    for key in ("id", "rating", "title", "body", "author_name", "status", "verified_purchase", "reply"):
        assert key in ones[0], f"a review element lacks {key!r}"


def test_histogram_row_links_to_rating_filtered_page():
    """The page links the one-star row to ?rating=1, which shows only one-star reviews.

    cov: C-CF-102
    """
    markup = html.unescape(page_html(f"/products/{AQUA}").text)
    assert f"/products/{AQUA}?rating=1" in markup, "no histogram row links to /products/tock-33-aqua?rating=1"
    _, text = html_text(f"/products/{AQUA}?rating=1")
    assert "Strap tore at the buckle holes" in text, "the rating=1 page does not show Dana's review"
    assert "Fewer questions in the car" not in text, "the rating=1 page still shows a five-star review"


def test_customer_review_stored_pending(fresh_customer, db):
    """A customer review is answered and stored as pending.

    cov: C-CF-103
    """
    _, author = fresh_customer
    review = pending_review(author, WOVEN_SAND, rating=5)
    assert review.get("status") == "pending", f"the new review reads status {review.get('status')!r}"
    row = db.review(review["id"])
    assert row is not None and row.get("status") == "pending", f"the reviews row reads {row}"


def test_second_review_of_product_by_one_account_rejected_as_duplicate(fresh_customer, db):
    """A second review of the same product by one account is rejected and writes nothing.

    cov: C-CF-104
    """
    email, author = fresh_customer
    pending_review(author, WOVEN_SAND)
    second = write_review(author, WOVEN_SAND, unique_title())
    expect_client_error(second, "a second review of one product by one account")
    count = db.count_reviews(db.product(WOVEN_SAND)["id"], db.account(email)["id"])
    assert count == 1, f"the reviews table holds {count} reviews by {email} for the strap"


def test_review_rating_outside_1_to_5_rejected(fresh_customer, db):
    """Ratings 0 and 6 are rejected and write nothing.

    cov: C-CF-105
    """
    email, author = fresh_customer
    for rating in (0, 6):
        expect_client_error(write_review(author, WOVEN_SAND, unique_title(), rating=rating),
                            f"a review with rating {rating}")
    count = db.count_reviews(db.product(WOVEN_SAND)["id"], db.account(email)["id"])
    assert count == 0, f"rejected ratings wrote {count} review rows"


def test_verified_purchase_flag_follows_account_order_history(fresh_customer, second_fresh_customer, anon_client, owner_client):
    """A buyer's review is verified and a non-buyer's is not.

    cov: C-CF-106, C-CF-246, C-CF-262
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    _, buyer = fresh_customer
    _, browser_only = second_fresh_customer
    place_order(anon_client, buyer, [SKU_NATO_AQUA])
    bought = pending_review(buyer, NATO_AQUA)
    not_bought = pending_review(browser_only, NATO_AQUA)
    assert bought.get("verified_purchase") is True, f"the buyer's review reads verified_purchase {bought.get('verified_purchase')!r}"
    assert not_bought.get("verified_purchase") is False, (
        f"the non-buyer's review reads verified_purchase {not_bought.get('verified_purchase')!r}")
    _, claimant_token = signup()
    with client(claimant_token) as claimant:
        response = claimant.post(f"/products/{NATO_AQUA}/reviews", json={"rating": 5, "title": unique_title(),
                                 "body": "Claims a purchase.", "mentions_minor": False, "verified_purchase": True})
    if response.status_code in (200, 201):
        assert response.json().get("verified_purchase") is False, "a reviewer-supplied verified_purchase set the flag"
    else:
        expect_client_error(response, "a review body claiming verified_purchase")
    ensure_available(owner_client, SKU_GREY38, 1)
    ensure_available(owner_client, SKU_AQUA, 1)
    _, bundle_token = signup()
    with client(bundle_token) as bundle_buyer:
        place_order(anon_client, bundle_buyer, [SKU_BUNDLE_GREY_AQUA])
        through_bundle = pending_review(bundle_buyer, GREY38)
    assert through_bundle.get("verified_purchase") is True, (
        "a review on a watch bought inside a bundle reads verified_purchase "
        f"{through_bundle.get('verified_purchase')!r}")


def test_owner_publish_lists_review_counting_review(fresh_customer, owner_client, anon_client):
    """Publishing a pending review lists it and adds one to review_count.

    cov: C-CF-107
    """
    _, author = fresh_customer
    review = pending_review(author, RUBBER_NAVY)
    before = product_json(anon_client, RUBBER_NAVY).get("review_count")
    published = ok_json(owner_client.post(f"/owner/reviews/{review['id']}/publish", json={}), "owner publish")
    assert published.get("status") == "published", f"the published review reads {published.get('status')!r}"
    assert review["title"] in [r.get("title") for r in public_reviews(anon_client, RUBBER_NAVY)], (
        "the published review is not listed")
    after = product_json(anon_client, RUBBER_NAVY).get("review_count")
    assert after == before + 1, f"publishing moved review_count from {before} to {after}"


def test_publishing_review_not_pending_rejected_with_review_unchanged(fresh_customer, owner_client, db):
    """Publishing or rejecting an already published review is rejected and leaves it published.

    cov: C-CF-108
    """
    _, author = fresh_customer
    review = pending_review(author, RUBBER_NAVY)
    ok_json(owner_client.post(f"/owner/reviews/{review['id']}/publish", json={}), "the first publish")
    expect_client_error(owner_client.post(f"/owner/reviews/{review['id']}/publish", json={}), "a second publish")
    expect_client_error(owner_client.post(f"/owner/reviews/{review['id']}/reject", json={"policy_clause": "spam"}),
                        "rejecting a published review")
    assert db.review(review["id"]).get("status") == "published", "the published review changed status"


def test_reject_without_allowed_policy_clause_refused(fresh_customer, owner_client, db):
    """A reject with no clause or an unknown clause is refused; spam is accepted.

    cov: C-CF-109, C-DM-30
    """
    _, author = fresh_customer
    review = pending_review(author, WOVEN_SAND, rating=1)
    for body in ({}, {"policy_clause": "too-negative"}):
        expect_client_error(owner_client.post(f"/owner/reviews/{review['id']}/reject", json=body),
                            f"reject with {body}")
        assert db.review(review["id"]).get("status") == "pending", f"reject with {body} changed the review"
    rejected = ok_json(owner_client.post(f"/owner/reviews/{review['id']}/reject", json={"policy_clause": "spam"}),
                       "reject with spam")
    assert rejected.get("status") == "rejected", f"reject with spam left status {rejected.get('status')!r}"
    assert db.review(review["id"]).get("rejection_clause") == "spam", "the rejection clause was not stored"


def test_minor_review_cannot_publish_without_basis(fresh_customer, owner_client, db):
    """A review mentioning a minor needs a non-empty basis to publish, which is recorded.

    cov: C-CF-110, C-DM-29
    """
    _, author = fresh_customer
    review = pending_review(author, RUBBER_NAVY, mentions_minor=True)
    for body in ({}, {"basis": ""}):
        expect_client_error(owner_client.post(f"/owner/reviews/{review['id']}/publish", json=body),
                            f"publishing a minor review with {body}")
        assert db.review(review["id"]).get("status") == "pending", f"publish with {body} changed the review"
    basis = "Parent confirmed consent by email"
    ok_json(owner_client.post(f"/owner/reviews/{review['id']}/publish", json={"basis": basis}), "publish with a basis")
    row = db.review(review["id"])
    assert (row.get("status"), row.get("minor_basis")) == ("published", basis), f"the reviews row reads {row}"


def test_owner_reply_shows_labelled_reply_from_tock(fresh_customer, owner_client, anon_client):
    """The owner reply is returned, listed and shown labelled Reply from Tock.

    cov: C-CF-111, C-CF-252
    """
    _, author = fresh_customer
    review = pending_review(author, RUBBER_NAVY)
    ok_json(owner_client.post(f"/owner/reviews/{review['id']}/publish", json={}), "owner publish")
    body = f"Thanks for the note {os.urandom(3).hex()}"
    replied = ok_json(owner_client.post(f"/owner/reviews/{review['id']}/reply", json={"body": body}), "owner reply")
    assert body in str(replied.get("reply")), f"the reply response carries {replied.get('reply')!r}"
    listed = [r for r in public_reviews(anon_client, RUBBER_NAVY) if r.get("id") == review["id"]]
    assert listed and body in str(listed[0].get("reply")), f"the listed review carries reply {listed}"
    _, text = html_text(f"/products/{RUBBER_NAVY}")
    at = text.find(body)
    assert at >= 0 and "Reply from Tock" in text, "the product page does not show the reply labelled Reply from Tock"
    assert replied.get("id") == review["id"], f"the reply call did not return the review: {replied}"


def test_second_owner_reply_to_one_review_rejected_with_first_reply_unchanged(fresh_customer, owner_client, anon_client, db):
    """A second reply and an empty reply are rejected and the first reply stays.

    cov: C-CF-112
    """
    _, author = fresh_customer
    review = pending_review(author, RUBBER_NAVY)
    ok_json(owner_client.post(f"/owner/reviews/{review['id']}/publish", json={}), "owner publish")
    ok_json(owner_client.post(f"/owner/reviews/{review['id']}/reply", json={"body": "First reply"}), "first reply")
    expect_client_error(owner_client.post(f"/owner/reviews/{review['id']}/reply", json={"body": "Second reply"}),
                        "a second reply")
    expect_client_error(owner_client.post(f"/owner/reviews/{review['id']}/reply", json={"body": ""}), "an empty reply")
    listed = [r for r in public_reviews(anon_client, RUBBER_NAVY) if r.get("id") == review["id"]]
    assert listed and "First reply" in str(listed[0].get("reply")), f"the first reply changed: {listed}"
    assert db.count_replies(review["id"]) == 1, f"review_replies holds {db.count_replies(review['id'])} rows"


def test_customer_owner_review_call_denied_with_review_unchanged(fresh_customer, customer_client, db):
    """A customer calling publish, reject or reply is denied and nothing changes.

    cov: C-CF-113
    """
    _, author = fresh_customer
    review = pending_review(author, WOVEN_SAND)
    for action, body in (("publish", {"basis": "customer"}), ("reject", {"policy_clause": "spam"}),
                         ("reply", {"body": "customer reply"})):
        expect_client_error(customer_client.post(f"/owner/reviews/{review['id']}/{action}", json=body),
                            f"customer POST /api/owner/reviews/<id>/{action}")
    assert db.review(review["id"]).get("status") == "pending", "a denied customer call changed the review"
    assert db.count_replies(review["id"]) == 0, "a denied customer reply was written"


def test_review_body_markup_shows_as_text(fresh_customer, owner_client):
    """A published body carrying <b> shows the characters, never bold markup.

    cov: C-CF-114
    """
    _, author = fresh_customer
    marker = f"probe-bold-{os.urandom(3).hex()}"
    review = pending_review(author, RUBBER_NAVY, body=f"<b>{marker}</b> strap")
    ok_json(owner_client.post(f"/owner/reviews/{review['id']}/publish", json={}), "owner publish")
    markup = page_html(f"/products/{RUBBER_NAVY}").text
    assert f"<b>{marker}</b>" not in markup, "the review body was rendered as markup"
    assert re.search(rf"&lt;b&gt;{marker}|&#60;b&#62;{marker}|&#x3c;b&#x3e;{marker}", markup, re.I), (
        "the review body markup is not shown as text")
    _, other_token = signup()
    title_marker = f"probe-title-{os.urandom(3).hex()}"
    with client(other_token) as other:
        titled = pending_review(other, RUBBER_NAVY, title=f"<i>{title_marker}</i> title")
    ok_json(owner_client.post(f"/owner/reviews/{titled['id']}/publish", json={}), "owner publish")
    assert f"<i>{title_marker}</i>" not in page_html(f"/products/{RUBBER_NAVY}").text, "the review title was rendered as markup"


def test_product_without_reviews_shows_no_reviews_yet(anon_client):
    """TOCK 33 Navy has no published reviews and invites the first.

    cov: C-CF-115, C-CF-209
    """
    product = product_json(anon_client, NAVY)
    assert (product.get("review_count"), product.get("rating_average")) == (0, None), (
        f"TOCK 33 Navy reads review_count {product.get('review_count')!r}, rating {product.get('rating_average')!r}")
    _, text = html_text(f"/products/{NAVY}")
    assert "No reviews yet. Be the first to write one." in text, "the Navy page does not invite the first review"


def test_cart_create_returns_cart_token(anon_client, carts):
    """POST /api/cart returns a token for an empty cart.

    cov: C-CF-116
    """
    token = carts()
    cart = ok_json(cart_get(anon_client, token), "GET /api/cart")
    assert cart.get("token") == token and lines_of(cart) == [], f"the new cart reads {cart}"
    assert (cart.get("subtotal"), cart.get("item_count")) == (0, 0), f"the empty cart totals read {cart}"
    for key in ("lines", "notices", "subtotal", "item_count", "hold_seconds_remaining"):
        assert key in cart, f"the new cart lacks {key!r}: {cart}"


def test_adding_line_holds_stock_for_cart(anon_client, carts, owner_client, db):
    """Adding two units holds two units at once.

    cov: C-CF-117
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 5)
    before = stock_row(owner_client, SKU_NATO_AQUA)
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 2)
    after = stock_row(owner_client, SKU_NATO_AQUA)
    assert int(after["reserved"]) == int(before["reserved"]) + 2, f"reserved moved {before['reserved']} to {after['reserved']}"
    assert int(after["available"]) == int(before["available"]) - 2, f"available moved {before['available']} to {after['available']}"
    cart_row = db.cart(token)
    held = sum(int(r["quantity"]) for r in db.cart_reservations(cart_row["id"]) if r.get("status") == "held")
    assert held == 2, f"the reservations table holds {held} units for this cart"


def test_adding_same_sku_raises_line_quantity(anon_client, carts):
    """Adding a sku twice leaves one line with quantity two.

    cov: C-CF-118
    """
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    cart = added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    lines = [l for l in lines_of(cart) if l.get("sku") == SKU_NATO_AQUA and not l.get("is_gift")]
    assert len(lines) == 1 and int(lines[0]["quantity"]) == 2, f"the cart lines read {lines}"


def test_adding_unpublished_lilac_sku_to_cart_rejected(anon_client, carts, db):
    """TK33-LILAC and an unknown sku are rejected and hold nothing.

    cov: C-CF-119
    """
    token = carts()
    reserved = int(db.inventory(SKU_LILAC)["reserved"])
    for sku in (SKU_LILAC, "NO-SUCH-SKU-1"):
        expect_client_error(cart_add(anon_client, token, sku, 1), f"adding {sku}")
    cart = ok_json(cart_get(anon_client, token), "GET /api/cart")
    assert lines_of(cart) == [], f"a rejected add left lines {lines_of(cart)}"
    assert int(db.inventory(SKU_LILAC)["reserved"]) == reserved, "the lilac add still held stock"


def test_buying_tote_sku_beside_free_tote_line_adds_separate_paid_line(anon_client, carts, owner_client):
    """A paid TOTE-BONE line sits beside the free gift tote line.

    cov: C-CF-120
    """
    ensure_available(owner_client, SKU_AQUA, 2)
    ensure_available(owner_client, SKU_TOTE, 10)
    ensure_available(owner_client, SKU_BEANIE, 10)
    token = carts()
    added_cart(anon_client, token, SKU_AQUA, 1)
    cart = added_cart(anon_client, token, SKU_TOTE, 1)
    paid = line_for(cart, SKU_TOTE, gift=False)
    gifts = gift_lines(cart, SKU_TOTE)
    assert paid is not None and int(paid["unit_price"]) == PRICE_TOTE, f"no paid tote line at 2000: {lines_of(cart)}"
    assert len(gifts) == 1 and int(gifts[0]["unit_price"]) == 0, f"the gift tote line changed: {gifts}"


def test_line_quantity_outside_1_to_5_rejected(anon_client, carts):
    """Quantities 0 and 6 are rejected on add and on patch, and nothing changes.

    cov: C-CF-121
    """
    token = carts()
    for quantity in (0, 6):
        expect_client_error(cart_add(anon_client, token, SKU_NATO_AQUA, quantity), f"adding quantity {quantity}")
    cart = added_cart(anon_client, token, SKU_NATO_AQUA, 2)
    line = line_for(cart, SKU_NATO_AQUA)
    for quantity in (6, 0):
        expect_client_error(cart_patch(anon_client, token, line["id"], quantity), f"patching to {quantity}")
    after = line_for(ok_json(cart_get(anon_client, token), "GET /api/cart"), SKU_NATO_AQUA)
    assert int(after["quantity"]) == 2, f"a rejected patch changed the quantity to {after['quantity']}"


def test_bundle_line_holds_each_watch(anon_client, carts, owner_client):
    """One Grey and Aqua Bundle holds one TOCK 38 Grey and one TOCK 33 Aqua.

    cov: C-CF-122
    """
    ensure_available(owner_client, SKU_GREY38, 2)
    ensure_available(owner_client, SKU_AQUA, 2)
    grey = int(stock_row(owner_client, SKU_GREY38)["reserved"])
    aqua = int(stock_row(owner_client, SKU_AQUA)["reserved"])
    token = carts()
    added_cart(anon_client, token, SKU_BUNDLE_GREY_AQUA, 1)
    assert int(stock_row(owner_client, SKU_GREY38)["reserved"]) == grey + 1, "the bundle did not hold TOCK 38 Grey"
    assert int(stock_row(owner_client, SKU_AQUA)["reserved"]) == aqua + 1, "the bundle did not hold TOCK 33 Aqua"


def test_add_exceeding_availability_holds_nothing(anon_client, carts, owner_client):
    """Adds beyond availability, for a watch or a bundle, are rejected whole.

    cov: C-CF-123
    """
    glow38 = int(stock_row(owner_client, SKU_GLOW38)["available"])
    glow33 = int(stock_row(owner_client, SKU_GLOW33)["available"])
    set_available(owner_client, SKU_GLOW38, 2)
    set_available(owner_client, SKU_GLOW33, 1)
    try:
        reserved38 = int(stock_row(owner_client, SKU_GLOW38)["reserved"])
        reserved33 = int(stock_row(owner_client, SKU_GLOW33)["reserved"])
        token = carts()
        expect_client_error(cart_add(anon_client, token, SKU_GLOW38, 3), "adding 3 x TK38-GLOW with 2 available")
        expect_client_error(cart_add(anon_client, token, SKU_BUNDLE_GLOW_GLOW, 2), "adding 2 bundles with 1 TK33-GLOW")
        assert int(stock_row(owner_client, SKU_GLOW38)["reserved"]) == reserved38, "a rejected add held TK38-GLOW"
        assert int(stock_row(owner_client, SKU_GLOW33)["reserved"]) == reserved33, "a rejected add held TK33-GLOW"
    finally:
        set_available(owner_client, SKU_GLOW38, glow38)
        set_available(owner_client, SKU_GLOW33, glow33)


def test_concurrent_adds_of_last_unit_admit_exactly_one(anon_client, owner_client, db):
    """Eight carts released together contend for the last unit, round after round.

    cov: C-CF-124
    """
    before = int(stock_row(owner_client, SKU_RUBBER_FUCHSIA_L)["available"])
    set_available(owner_client, SKU_RUBBER_FUCHSIA_L, 1)
    try:
        for round_n in range(CONTENTION_ROUNDS):
            tokens = [new_cart(anon_client) for _ in range(CONTENTION_WRITERS)]
            results = race([{"method": "POST", "path": "/cart/lines",
                             "json": {"sku": SKU_RUBBER_FUCHSIA_L, "quantity": 1},
                             "headers": {"X-Cart-Token": t}} for t in tokens])
            statuses = [r.status_code if r is not None else None for r in results]
            winners = [t for t, s in zip(tokens, statuses) if s in (200, 201)]
            assert len(winners) == 1, f"round {round_n}: {len(winners)} adds won the last unit, statuses {statuses}"
            losers = [s for s in statuses if s not in (200, 201)]
            assert all(s is not None and 400 <= s < 500 for s in losers), f"round {round_n}: losers answered {losers}"
            assert all(r.text.strip() for r in results if r is not None and r.status_code not in (200, 201)), (
                f"round {round_n}: a losing add gave no reason")
            row = db.inventory(SKU_RUBBER_FUCHSIA_L)
            assert int(row["reserved"]) <= int(row["on_hand"]), f"round {round_n}: reserved {row['reserved']} > on_hand {row['on_hand']}"
            cart = ok_json(cart_get(anon_client, winners[0]), "GET /api/cart for the winner")
            ok_json(cart_delete(anon_client, winners[0], line_for(cart, SKU_RUBBER_FUCHSIA_L)["id"]), "releasing the winner")
    finally:
        set_available(owner_client, SKU_RUBBER_FUCHSIA_L, before)


def test_held_units_never_exceed_units_on_hand(anon_client, owner_client, db):
    """Six carts racing for two units win at most two, and reserved stays within on_hand.

    cov: C-CF-125
    """
    before = int(stock_row(owner_client, SKU_RUBBER_NAVY_L)["available"])
    set_available(owner_client, SKU_RUBBER_NAVY_L, 2)
    tokens = [new_cart(anon_client) for _ in range(6)]
    try:
        results = race([{"method": "POST", "path": "/cart/lines",
                         "json": {"sku": SKU_RUBBER_NAVY_L, "quantity": 1},
                         "headers": {"X-Cart-Token": t}} for t in tokens])
        winners = [r for r in results if r is not None and r.status_code in (200, 201)]
        assert len(winners) <= 2, f"{len(winners)} adds were admitted for 2 available units"
        for row in db.inventory_rows():
            assert 0 <= int(row["reserved"]) <= int(row["on_hand"]), f"inventory row {row} holds more than it has"
    finally:
        for token in tokens:
            cart = ok_json(cart_get(anon_client, token), "GET /api/cart")
            for line in lines_of(cart):
                cart_delete(anon_client, token, line["id"])
        set_available(owner_client, SKU_RUBBER_NAVY_L, before)


def test_removing_line_releases_hold(anon_client, carts, owner_client, db):
    """Lowering a line releases units and deleting it releases the rest.

    cov: C-CF-126, C-CF-213, C-CF-249
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 5)
    base = int(stock_row(owner_client, SKU_NATO_AQUA)["reserved"])
    token = carts()
    line = line_for(added_cart(anon_client, token, SKU_NATO_AQUA, 3), SKU_NATO_AQUA)
    ok_json(cart_patch(anon_client, token, line["id"], 1), "lowering the line to 1")
    assert int(stock_row(owner_client, SKU_NATO_AQUA)["reserved"]) == base + 1, "lowering the line did not release two units"
    ok_json(cart_delete(anon_client, token, line["id"]), "deleting the line")
    assert int(stock_row(owner_client, SKU_NATO_AQUA)["reserved"]) == base, "deleting the line did not release its hold"
    cart_row = db.cart(token)
    statuses = [r.get("status") for r in db.cart_reservations(cart_row["id"])]
    assert "released" in statuses and "held" not in statuses, f"the removed line's reservations read {statuses}"


def test_watch_cart_carries_one_gift_tote_line_with_one_gift_beanie_line(anon_client, carts, owner_client):
    """A watch in the cart brings exactly one gift tote line and one gift beanie line.

    cov: C-CF-127
    """
    ensure_available(owner_client, SKU_AQUA, 2)
    ensure_available(owner_client, SKU_TOTE, 10)
    ensure_available(owner_client, SKU_BEANIE, 10)
    token = carts()
    cart = added_cart(anon_client, token, SKU_AQUA, 1)
    for sku in (SKU_TOTE, SKU_BEANIE):
        gifts = gift_lines(cart, sku)
        assert len(gifts) == 1 and int(gifts[0]["quantity"]) == 1, f"gift lines for {sku} read {gifts}"


def test_gift_line_carries_promotion_gift_with_purchase_at_price_0(anon_client, carts, owner_client):
    """A bundle brings gift lines at 0 labelled Gift with purchase.

    cov: C-CF-128, C-CF-255
    """
    ensure_available(owner_client, SKU_GREY38, 2)
    ensure_available(owner_client, SKU_AQUA, 2)
    ensure_available(owner_client, SKU_TOTE, 10)
    ensure_available(owner_client, SKU_BEANIE, 10)
    token = carts()
    cart = added_cart(anon_client, token, SKU_BUNDLE_GREY_AQUA, 1)
    for sku, title in ((SKU_TOTE, "Tock Tote"), (SKU_BEANIE, "Tock Beanie")):
        gifts = gift_lines(cart, sku)
        assert len(gifts) == 1, f"the bundle cart carries gift lines {gifts} for {sku}"
        gift = gifts[0]
        assert (gift.get("title"), gift.get("promotion"), int(gift.get("unit_price")), int(gift.get("line_total"))) == (
            title, GIFT_PROMOTION, 0, 0), f"the gift line reads {gift}"
    promotions = {l.get("promotion") for l in lines_of(cart) if l.get("promotion")}
    assert promotions <= {GIFT_PROMOTION}, f"cart lines carry promotions {promotions}"


def test_more_watches_add_no_extra_gifts(anon_client, carts, owner_client):
    """Two Aqua and one Glow still carry one tote and one beanie gift line.

    cov: C-CF-129
    """
    ensure_available(owner_client, SKU_AQUA, 3)
    ensure_available(owner_client, SKU_GLOW33, 2)
    ensure_available(owner_client, SKU_TOTE, 10)
    ensure_available(owner_client, SKU_BEANIE, 10)
    token = carts()
    added_cart(anon_client, token, SKU_AQUA, 2)
    cart = added_cart(anon_client, token, SKU_GLOW33, 1)
    for sku in (SKU_TOTE, SKU_BEANIE):
        gifts = gift_lines(cart, sku)
        assert len(gifts) == 1 and int(gifts[0]["quantity"]) == 1, f"more watches changed the {sku} gifts: {gifts}"


def test_gift_line_patch_or_delete_rejected(anon_client, carts, owner_client):
    """PATCH and DELETE on a gift line are rejected and the line stays.

    cov: C-CF-130
    """
    ensure_available(owner_client, SKU_AQUA, 2)
    ensure_available(owner_client, SKU_TOTE, 10)
    ensure_available(owner_client, SKU_BEANIE, 10)
    token = carts()
    gift = gift_lines(added_cart(anon_client, token, SKU_AQUA, 1), SKU_TOTE)[0]
    expect_client_error(cart_patch(anon_client, token, gift["id"], 2), "patching a gift line")
    expect_client_error(cart_delete(anon_client, token, gift["id"]), "deleting a gift line")
    after = gift_lines(ok_json(cart_get(anon_client, token), "GET /api/cart"), SKU_TOTE)
    assert len(after) == 1 and int(after[0]["quantity"]) == 1, f"the gift line changed: {after}"


def test_removing_last_watch_removes_gifts_with_notice(anon_client, carts, owner_client):
    """Deleting the only watch removes both gifts, releases them and adds promotion_removed.

    cov: C-CF-131
    """
    ensure_available(owner_client, SKU_AQUA, 2)
    ensure_available(owner_client, SKU_TOTE, 10)
    ensure_available(owner_client, SKU_BEANIE, 10)
    tote = int(stock_row(owner_client, SKU_TOTE)["reserved"])
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    watch = line_for(added_cart(anon_client, token, SKU_AQUA, 1), SKU_AQUA)
    cart = ok_json(cart_delete(anon_client, token, watch["id"]), "deleting the only watch")
    assert not [l for l in lines_of(cart) if l.get("is_gift")], f"gift lines survived: {lines_of(cart)}"
    assert line_for(cart, SKU_NATO_AQUA) is not None, "deleting the watch removed the strap line"
    notices = [(n.get("kind"), n.get("message")) for n in cart.get("notices") or []]
    assert ("promotion_removed", PROMOTION_REMOVED_MESSAGE) in notices, f"the cart notices read {notices}"
    assert int(stock_row(owner_client, SKU_TOTE)["reserved"]) == tote, "the removed gift tote still holds stock"


def test_gift_without_stock_left_out_with_notice(anon_client, carts, owner_client):
    """With the tote at zero only the beanie gift is added, with a gift_unavailable notice.

    cov: C-CF-132
    """
    ensure_available(owner_client, SKU_AQUA, 2)
    ensure_available(owner_client, SKU_BEANIE, 10)
    tote = int(ensure_available(owner_client, SKU_TOTE, 10)["available"])
    set_available(owner_client, SKU_TOTE, 0)
    try:
        token = carts()
        cart = added_cart(anon_client, token, SKU_AQUA, 1)
        assert gift_lines(cart, SKU_TOTE) == [], f"a tote gift was added with no stock: {lines_of(cart)}"
        assert len(gift_lines(cart, SKU_BEANIE)) == 1, "the beanie gift was left out as well"
        notices = [(n.get("kind"), n.get("message")) for n in cart.get("notices") or []]
        assert ("gift_unavailable", TOTE_UNAVAILABLE_MESSAGE) in notices, f"the cart notices read {notices}"
    finally:
        set_available(owner_client, SKU_TOTE, tote)


def test_hold_seconds_remaining_restart_after_cart_change(anon_client, carts):
    """hold_seconds_remaining reads 1800 after a change, runs down, and restarts on the next change.

    cov: C-CF-133
    """
    token = carts()
    first = added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    assert 1795 <= int(first["hold_seconds_remaining"]) <= 1800, f"after an add the hold reads {first['hold_seconds_remaining']}"
    settle(4.0)
    waited = ok_json(cart_get(anon_client, token), "GET /api/cart")
    assert int(waited["hold_seconds_remaining"]) <= 1797, f"four seconds later the hold reads {waited['hold_seconds_remaining']}"
    changed = added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    assert int(changed["hold_seconds_remaining"]) > int(waited["hold_seconds_remaining"]), (
        f"a cart change did not restart the hold: {waited['hold_seconds_remaining']} then {changed['hold_seconds_remaining']}")


def test_cart_subtotal_sums_non_gift_lines(anon_client, carts, owner_client):
    """One Aqua and two NATO straps give a subtotal of 23300 with gifts at 0.

    cov: C-CF-134, C-CF-248
    """
    ensure_available(owner_client, SKU_AQUA, 2)
    token = carts()
    added_cart(anon_client, token, SKU_AQUA, 1)
    cart = added_cart(anon_client, token, SKU_NATO_AQUA, 2)
    assert int(cart["subtotal"]) == PRICE_AQUA + 2 * PRICE_NATO, f"the subtotal reads {cart['subtotal']}"
    for line in lines_of(cart):
        assert int(line["line_total"]) == int(line["unit_price"]) * int(line["quantity"]), f"line total mismatch {line}"
    assert all(LINE_FIELDS <= set(line) for line in lines_of(cart)), "a cart line lacks the listed line fields"


def test_cart_item_count_sums_non_gift_quantities(anon_client, carts, owner_client):
    """One Aqua and two NATO straps give item_count 3 despite two gift lines.

    cov: C-CF-135
    """
    ensure_available(owner_client, SKU_AQUA, 2)
    token = carts()
    added_cart(anon_client, token, SKU_AQUA, 1)
    cart = added_cart(anon_client, token, SKU_NATO_AQUA, 2)
    assert int(cart["item_count"]) == 3, f"item_count reads {cart['item_count']}, expected 3"


def test_empty_cart_control_reads_zero_dollars_with_zero_count():
    """A visitor with no cart sees $0.00 and (0) in the header cart control.

    cov: C-CF-136
    """
    _, text = html_text("/")
    assert "$0.00" in text and "(0)" in text, "the header cart control does not read $0.00 and (0)"


def test_bundle_cart_line_lists_two_watches(page, owner_client):
    """The cart page lists a bundle line with its two watches and the complete-set notice.

    cov: C-CF-137
    """
    ensure_available(owner_client, SKU_GREY38, 2)
    ensure_available(owner_client, SKU_AQUA, 2)
    ui_add_to_cart(page, BUNDLE_GREY_AQUA)
    visit(page, "/cart")
    text = main_text(page)
    at = text.find("Grey and Aqua Bundle")
    assert at >= 0, "the cart page does not list the Grey and Aqua Bundle"
    tail = text[at:]
    for copy in ("TOCK 38 Grey", "TOCK 33 Aqua", COMPLETE_SET_NOTICE):
        assert copy in tail, f"the bundle cart line does not list {copy!r}"

def test_anonymous_checkout_visit_redirects_to_login_with_return_to():
    """An anonymous /checkout visit redirects to the login page with return_to=/checkout.

    cov: C-CF-138
    """
    status, location = redirect_target("/checkout")
    assert 300 <= status < 400 and location == "/account/login?return_to=/checkout", (
        f"anonymous GET /checkout answered {status} to {location!r}")


def test_checkout_without_idempotency_key_rejected(fresh_customer, anon_client, carts):
    """A checkout with no Idempotency-Key is rejected, writes no order and keeps the cart.

    cov: C-CF-139
    """
    _, buyer = fresh_customer
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    expect_client_error(checkout(buyer, token, key=None), "POST /api/checkout without Idempotency-Key")
    assert own_orders(buyer) == [], "a checkout without an Idempotency-Key created an order"
    assert line_for(ok_json(cart_get(anon_client, token), "GET /api/cart"), SKU_NATO_AQUA) is not None, (
        "the rejected checkout emptied the cart")


def test_checkout_of_empty_cart_creates_no_order(fresh_customer, anon_client, carts, payments):
    """Checking out an empty cart is rejected with no order and no Kill Bill invoice.

    cov: C-CF-140
    """
    email, buyer = fresh_customer
    token = carts()
    expect_client_error(checkout(buyer, token, unique_key()), "POST /api/checkout of an empty cart")
    assert own_orders(buyer) == [], "checking out an empty cart created an order"
    settle()
    account = killbill_account(payments, f"tock-{email}")
    invoices = killbill_invoices(payments, account.get("accountId")) if account else []
    assert invoices == [], f"checking out an empty cart raised Kill Bill invoices {invoices}"


def test_checkout_country_other_than_us_rejected(fresh_customer, anon_client, carts, owner_client):
    """A Canadian address is rejected naming country, with no order and the hold kept.

    cov: C-CF-141
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    _, buyer = fresh_customer
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    reserved = int(stock_row(owner_client, SKU_NATO_AQUA)["reserved"])
    address = dict(us_address(), country="CA")
    response = checkout(buyer, token, unique_key(), address)
    expect_client_error(response, "POST /api/checkout to country CA")
    assert "country" in response.text, f"the rejection does not name country: {response.text[:300]}"
    assert own_orders(buyer) == [], "a non-US checkout created an order"
    assert int(stock_row(owner_client, SKU_NATO_AQUA)["reserved"]) == reserved, "the rejected checkout released the hold"


def test_checkout_missing_address_field_rejected(fresh_customer, anon_client, carts):
    """Missing postcode or city is rejected naming the field, and no order is written.

    cov: C-CF-142
    """
    _, buyer = fresh_customer
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    for field in ("postcode", "city"):
        address = {k: v for k, v in us_address().items() if k != field}
        response = checkout(buyer, token, unique_key(), address)
        expect_client_error(response, f"POST /api/checkout without {field}")
        assert field in response.text, f"the rejection does not name {field}: {response.text[:300]}"
    assert own_orders(buyer) == [], "an incomplete address created an order"


def test_checkout_order_number_matches_tk_eight_uppercase_letters_or_digits(fresh_customer, anon_client, owner_client):
    """A placed order number reads TK- and eight uppercase letters or digits.

    cov: C-CF-143
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    _, buyer = fresh_customer
    order = place_order(anon_client, buyer, [SKU_NATO_AQUA])
    assert ORDER_NUMBER_RE.match(order["number"]), f"order number {order['number']!r} does not match TK-XXXXXXXX"
    assert order.get("status") == "placed", f"a street address order reads status {order.get('status')!r}"
    assert ORDER_FIELDS <= set(order), f"the checkout response lacks {sorted(ORDER_FIELDS - set(order))}"


def test_order_totals_add_shipping_1500_to_subtotal_with_gift_lines_at_0(fresh_customer, anon_client, owner_client, db):
    """TOCK 33 Aqua alone totals 20400 in the response and in the stored order and lines.

    cov: C-CF-144, C-DM-05, C-DM-07, C-CF-234
    """
    ensure_available(owner_client, SKU_AQUA, 2)
    ensure_available(owner_client, SKU_TOTE, 10)
    ensure_available(owner_client, SKU_BEANIE, 10)
    _, buyer = fresh_customer
    order = place_order(anon_client, buyer, [SKU_AQUA])
    assert (order["subtotal"], order["shipping"], order["total"], order["currency"]) == (18900, 1500, 20400, "usd"), (
        f"the Aqua order reads {order}")
    gifts = [l for l in order.get("lines", []) if l.get("is_gift")]
    assert sorted(l["sku"] for l in gifts) == [SKU_BEANIE, SKU_TOTE] and all(int(l["unit_price"]) == 0 for l in gifts), (
        f"the order gift lines read {gifts}")
    row = db.order(order["number"])
    assert row is not None, f"the orders table has no row for {order['number']}"
    assert int(row["total"]) == int(row["subtotal"]) + int(row["shipping"]) == 20400, f"the orders row reads {row}"
    top = sum(int(l["unit_price"]) * int(l["quantity"]) for l in db.order_lines(row["id"]) if l.get("parent_line_id") is None)
    assert top == int(row["subtotal"]), f"order_lines without a parent sum to {top}, the stored subtotal is {row['subtotal']}"


def test_bundle_order_line_expands_into_two_watch_lines_naming_bundle_in_parent_sku(fresh_customer, anon_client, owner_client, db):
    """A bundle order line is followed by two watch lines at 0 naming the bundle, stored as child lines.

    cov: C-CF-145, C-DM-06
    """
    ensure_available(owner_client, SKU_GREY38, 2)
    ensure_available(owner_client, SKU_AQUA, 2)
    _, buyer = fresh_customer
    order = place_order(anon_client, buyer, [SKU_BUNDLE_GREY_AQUA])
    lines = order.get("lines", [])
    bundle = [l for l in lines if l.get("sku") == SKU_BUNDLE_GREY_AQUA]
    watches = [l for l in lines if l.get("parent_sku") == SKU_BUNDLE_GREY_AQUA]
    assert len(bundle) == 1 and int(bundle[0]["unit_price"]) == 46900 and bundle[0].get("parent_sku") is None, (
        f"the bundle order line reads {bundle}")
    assert sorted(l["sku"] for l in watches) == [SKU_AQUA, SKU_GREY38], f"the watch lines read {watches}"
    assert all(int(l["unit_price"]) == 0 for l in watches), f"watch lines inside a bundle are priced {watches}"
    row = db.order(order["number"])
    stored = db.order_lines(row["id"])
    parents = [l for l in stored if l.get("sku_snapshot") == SKU_BUNDLE_GREY_AQUA]
    assert len(parents) == 1, f"order_lines holds {len(parents)} bundle lines"
    children = [l for l in stored if l.get("parent_line_id") == parents[0]["id"]]
    assert len(children) == 2 and all(int(l["unit_price"]) == 0 for l in children), f"child lines read {children}"
    assert all(ORDER_LINE_FIELDS <= set(line) for line in lines), "an order line lacks the listed line fields"


def test_checkout_converts_hold_into_sale_ledger_entry_then_checked_out_cart_rejects_adds(fresh_customer, anon_client, owner_client, db):
    """Checkout moves the unit off on_hand and reserved, logs a sale noting the order, and closes the cart.

    cov: C-CF-146, C-CF-147, C-CF-250
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    _, buyer = fresh_customer
    token = new_cart(anon_client)
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    held = stock_row(owner_client, SKU_NATO_AQUA)
    response = checkout(buyer, token, unique_key())
    order = ok_json(response, "POST /api/checkout")
    after = stock_row(owner_client, SKU_NATO_AQUA)
    assert int(after["on_hand"]) == int(held["on_hand"]) - 1, f"on_hand moved {held['on_hand']} to {after['on_hand']}"
    assert int(after["reserved"]) == int(held["reserved"]) - 1, f"reserved moved {held['reserved']} to {after['reserved']}"
    item = db.inventory(SKU_NATO_AQUA)
    sales = [r for r in db.ledger_rows(item["id"]) if r.get("reason") == "sale" and order["number"] in str(r.get("note"))]
    assert len(sales) == 1 and int(sales[0]["delta"]) == -1, f"sale ledger rows for {order['number']}: {sales}"
    expect_client_error(cart_add(anon_client, token, SKU_NATO_AQUA, 1), "adding to a checked-out cart")
    cart_row = db.cart(token)
    assert cart_row["status"] == "checked_out", f"the checked-out cart row reads {cart_row['status']!r}"
    statuses = {r.get("status") for r in db.cart_reservations(cart_row["id"])}
    assert "converted" in statuses and "held" not in statuses, f"checked-out reservations read {statuses}"


def test_checkout_invoice_exists_on_killbill_account_keyed_tock_plus_account_email(anon_client, owner_client, payments):
    """A mixed-case signup is billed on the Kill Bill account keyed tock- plus the lowercase email.

    cov: C-CF-148, C-TR-10 (earned: an invoice on the tenant proves the call carried the pinned Basic login with both Kill Bill key headers, which no response exposes)
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    hexpart = os.urandom(5).hex()
    email, token = signup(email=f"Probe-{hexpart}@Example.com")
    with client(token) as buyer:
        order = place_order(anon_client, buyer, [SKU_NATO_AQUA])
    key = f"tock-probe-{hexpart}@example.com"
    account, invoices = killbill_invoices_for_key(payments, key, 1)
    assert account is not None, f"Kill Bill holds no account keyed {key!r} after order {order['number']}"
    assert str(account.get("currency", "")).upper() == "USD", f"the Kill Bill account currency is {account.get('currency')!r}"
    assert [i.amount for i in invoices] == [order["total"]], f"the account invoices are {[i.amount for i in invoices]}"
    assert str(account.get("email", "")).lower() == key[len("tock-"):], f"the Kill Bill account email is {account.get('email')!r}"


def test_checkout_invoice_amount_is_order_total_in_usd(fresh_customer, anon_client, owner_client, payments):
    """The order's invoice amount equals its total in USD.

    cov: C-CF-149
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    email, buyer = fresh_customer
    order = place_order(anon_client, buyer, [SKU_NATO_AQUA])
    account, invoices = killbill_invoices_for_key(payments, f"tock-{email}", 1)
    assert account is not None, f"Kill Bill holds no account for {email}"
    assert len(invoices) == 1, f"Kill Bill holds {len(invoices)} invoices for one order"
    assert (invoices[0].amount, invoices[0].currency.upper()) == (order["total"], "USD"), (
        f"the invoice reads {invoices[0].amount} {invoices[0].currency}, the order total is {order['total']} usd")


def test_second_order_reuses_killbill_account_with_second_invoice(fresh_customer, anon_client, owner_client, payments):
    """Two orders leave one Kill Bill account holding two invoices for their totals.

    cov: C-CF-150, C-TR-04
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 4)
    email, buyer = fresh_customer
    first = place_order(anon_client, buyer, [SKU_NATO_AQUA])
    second = place_order(anon_client, buyer, [SKU_NATO_AQUA, SKU_NATO_AQUA])
    account, invoices = killbill_invoices_for_key(payments, f"tock-{email}", 2)
    keyed = killbill_accounts_keyed(payments, f"tock-{email}")
    assert len(keyed) == 1, f"Kill Bill holds {len(keyed)} accounts for {email}"
    assert sorted(i.amount for i in invoices) == sorted([first["total"], second["total"]]), (
        f"the account invoices are {[i.amount for i in invoices]}, the order totals {first['total']} and {second['total']}")


def test_replayed_idempotency_key_returns_same_order_with_one_invoice(fresh_customer, anon_client, owner_client, payments, db, inbox):
    """Replaying a checkout key returns the same order, one row, one invoice and one confirmation.

    cov: C-CF-151, C-DM-19
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    email, buyer = fresh_customer
    token = new_cart(anon_client)
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    key = unique_key()
    first = ok_json(checkout(buyer, token, key), "the first checkout")
    replay = ok_json(checkout(buyer, token, key), "the replayed checkout")
    assert replay.get("number") == first["number"], f"the replay returned {replay.get('number')!r}, not {first['number']!r}"
    assert db.count_orders(db.account(email)["id"], key) == 1, "the replay wrote a second order row"
    _, invoices = killbill_invoices_for_key(payments, f"tock-{email}", 1)
    poll_until(lambda: inbox.find(to=email, subject_contains=first["number"]))
    settle()
    assert len(invoices) == 1 and len(killbill_invoices_for_key(payments, f"tock-{email}", 1)[1]) == 1, (
        "the replay raised a second invoice")
    confirmations = [s for s in mail_subjects(inbox, email) if s.startswith(CONFIRMATION_PREFIX)]
    assert len(confirmations) == 1, f"the replay sent confirmations {confirmations}"


def test_concurrent_duplicate_checkout_produces_one_order(fresh_customer, anon_client, owner_client, db, payments, inbox):
    """Six simultaneous checkouts with one key and one cart produce one order, one invoice and one email.

    cov: C-CF-152
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    email, token_client = fresh_customer
    bearer = token_client.headers["Authorization"].split(" ", 1)[1]
    cart_token = new_cart(anon_client)
    added_cart(anon_client, cart_token, SKU_NATO_AQUA, 1)
    key = unique_key()
    results = race([{"method": "POST", "path": "/checkout", "token": bearer,
                     "json": {"shipping_address": us_address()},
                     "headers": {"X-Cart-Token": cart_token, "Idempotency-Key": key}} for _ in range(6)])
    numbers = {r.json().get("number") for r in results if r is not None and r.status_code in (200, 201)}
    assert len(numbers) == 1, f"simultaneous checkouts returned order numbers {numbers}"
    assert db.count_account_orders(db.account(email)["id"]) == 1, "simultaneous checkouts wrote more than one order"
    _, invoices = killbill_invoices_for_key(payments, f"tock-{email}", 1)
    settle()
    assert len(killbill_invoices_for_key(payments, f"tock-{email}", 1)[1]) == 1, (
        f"simultaneous checkouts raised {len(invoices)} or more invoices")
    number = next(iter(numbers))
    poll_until(lambda: inbox.find(to=email, subject_contains=number))
    confirmations = [s for s in mail_subjects(inbox, email) if s.startswith(CONFIRMATION_PREFIX)]
    assert len(confirmations) == 1, f"simultaneous checkouts sent confirmations {confirmations}"


def test_order_confirmation_email_subject_names_order_addressed_only_to_account_opens_with_number_total(fresh_customer, anon_client, owner_client, inbox):
    """The confirmation mail subject names the order, is addressed to the account alone, and opens with number and total.

    cov: C-CF-153, C-CF-154, C-CF-155
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    email, buyer = fresh_customer
    order = place_order(anon_client, buyer, [SKU_NATO_AQUA])
    subject = f"{CONFIRMATION_PREFIX} {order['number']}"
    message = poll_until(lambda: inbox.find(to=email, subject_contains=subject))
    assert message is not None, f"no mail with subject {subject!r} reached {email}"
    assert message.subject.startswith(subject), f"the confirmation subject is {message.subject!r}"
    assert [a.lower() for a in message.to] == [email.lower()], f"the confirmation is addressed to {message.to}"
    others = [m.to for m in messages_with_subject(inbox, order["number"]) if [a.lower() for a in m.to] != [email.lower()]]
    assert not others, f"mail naming {order['number']} also went to {others}"
    total = f"${order['total'] / 100:.2f}"
    opening = message.body[:160]
    assert order["number"] in opening and total in opening, (
        f"the confirmation body does not open with {order['number']} and {total}: {message.body[:200]!r}")


def test_po_box_order_on_hold_invoiced_for_total_sends_address_needed_email(fresh_customer, anon_client, owner_client, inbox, payments):
    """A p.o. box in line 2 places the order on hold, invoices it and mails Address needed.

    cov: C-CF-156, C-CF-157, C-CF-256
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    email, buyer = fresh_customer
    order = place_order(anon_client, buyer, [SKU_NATO_AQUA], us_address(line2="p.o. box 77"))
    assert (order.get("status"), order.get("hold_reason")) == ("on_hold", "po_box"), (
        f"the PO box order reads status {order.get('status')!r} and hold_reason {order.get('hold_reason')!r}")
    subject = f"{ADDRESS_NEEDED_PREFIX} {order['number']}"
    message = poll_until(lambda: inbox.find(to=email, subject_contains=subject))
    assert message is not None and message.subject.startswith(subject), f"no mail beginning {subject!r} reached {email}"
    _, invoices = killbill_invoices_for_key(payments, f"tock-{email}", 1)
    assert [i.amount for i in invoices] == [order["total"]], "the PO box order was not invoiced like any other"


def test_street_address_order_sends_no_address_needed_email(fresh_customer, anon_client, owner_client, inbox):
    """A street address order gets its confirmation and never an Address needed mail.

    cov: C-CF-158
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    email, buyer = fresh_customer
    order = place_order(anon_client, buyer, [SKU_NATO_AQUA], us_address("400 Pine Street"))
    assert poll_until(lambda: inbox.find(to=email, subject_contains=order["number"])), "no confirmation arrived"
    settle()
    wrong = [s for s in mail_subjects(inbox, email) if s.startswith(ADDRESS_NEEDED_PREFIX)]
    assert not wrong, f"a street address order was sent {wrong}"


def test_orders_endpoint_returns_own_orders_newest_first_with_non_sequential_numbers(fresh_customer, anon_client, owner_client):
    """Two orders come back newest first, and their numbers are not consecutive.

    cov: C-CF-159, C-TR-07
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    _, buyer = fresh_customer
    first = place_order(anon_client, buyer, [SKU_NATO_AQUA])
    second = place_order(anon_client, buyer, [SKU_NATO_AQUA])
    numbers = [o.get("number") for o in own_orders(buyer)]
    assert numbers == [second["number"], first["number"]], f"GET /api/orders lists {numbers}"
    suffixes = [n[3:] for n in numbers]
    assert not all(s.isdigit() for s in suffixes) or abs(int(suffixes[0]) - int(suffixes[1])) > 1, (
        f"order numbers {numbers} are sequential")
    assert len(set(numbers)) == 2 and suffixes[0][:6] != suffixes[1][:6], f"order numbers {numbers} share a counting prefix"
    assert ok_json(buyer.get(f"/orders/{first['number']}"), "GET own order").get("number") == first["number"], "an own order is unreadable"
    refs = [ok_json(anon_client.post("/support-requests", json={"name": "Probe", "email": unique_email(), "subject": "Press",
                                                                 "message": "Hi"}), "support request").get("reference") for _ in range(2)]
    tails = [r[3:] for r in refs]
    assert not all(t.isdigit() for t in tails) or abs(int(tails[0]) - int(tails[1])) > 1, f"support references {refs} are sequential"


def test_foreign_order_number_answers_404_like_missing_one(customer_client):
    """Another customer's order and a missing order both answer 404.

    cov: C-CF-160
    """
    foreign = customer_client.get("/orders/TK-SEEDED01")
    missing = customer_client.get("/orders/TK-ZZZZZZZ9")
    assert (foreign.status_code, missing.status_code) == (404, 404), (
        f"foreign order answered {foreign.status_code}, missing order {missing.status_code}")
    assert "3700" not in foreign.text and "NATO" not in foreign.text, "the 404 still leaks the foreign order"


def test_owner_reading_seeded_customer_order_gets_404(owner_client, customer2_client):
    """The owner gets 404 on TK-SEEDED01 while its owner reads it.

    cov: C-CF-161
    """
    assert owner_client.get("/orders/TK-SEEDED01").status_code == 404, "the owner can read customer2's order"
    own = ok_json(customer2_client.get("/orders/TK-SEEDED01"), "customer2 GET /api/orders/<number> TK-SEEDED01")
    assert own.get("number") == "TK-SEEDED01", f"customer2 reads {own}"


def test_non_order_actions_send_no_order_mail(fresh_customer, anon_client, carts, owner_client, inbox):
    """Cart, review, restock and support actions send no order mail.

    cov: C-CF-162
    """
    email, customer = fresh_customer
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    pending_review(customer, WOVEN_SAND)
    set_available(owner_client, SKU_NATO_NAVY, 0)
    ok_json(anon_client.post(f"/products/{NATO_NAVY}/restock-subscriptions", json={"email": email}), "restock")
    ok_json(anon_client.post("/support-requests", json={"name": "Probe", "email": email, "subject": "Press",
                                                         "message": "Hello"}), "support request")
    settle(3.0)
    wrong = [s for s in mail_subjects(inbox, email) if s.startswith((CONFIRMATION_PREFIX, ADDRESS_NEEDED_PREFIX))]
    assert not wrong, f"non-order actions sent order mail {wrong}"


def test_restock_subscription_on_out_of_stock_product_is_waiting(anon_client, owner_client, db):
    """Subscribing to NATO Strap Navy at zero returns and stores a waiting subscription.

    cov: C-CF-163
    """
    set_available(owner_client, SKU_NATO_NAVY, 0)
    email = unique_email()
    response = anon_client.post(f"/products/{NATO_NAVY}/restock-subscriptions", json={"email": email})
    payload = ok_json(response, "POST restock-subscriptions")
    assert payload == {"product": NATO_NAVY, "email": email, "status": "waiting"}, f"the subscription reads {payload}"
    rows = db.subscriptions(db.product(NATO_NAVY)["id"], email)
    assert [r.get("status") for r in rows] == ["waiting"], f"restock_subscriptions rows read {rows}"


def test_restock_subscription_on_in_stock_product_rejected(anon_client, owner_client, db):
    """In-stock and low-stock products reject a restock subscription and store nothing.

    cov: C-CF-164
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 5)
    before = int(stock_row(owner_client, SKU_GLOW38)["available"])
    set_available(owner_client, SKU_GLOW38, 2)
    try:
        for handle in (NATO_AQUA, GLOW38):
            email = unique_email()
            response = anon_client.post(f"/products/{handle}/restock-subscriptions", json={"email": email})
            expect_client_error(response, f"a restock subscription on {handle}")
            assert db.subscriptions(db.product(handle)["id"], email) == [], f"a rejected subscription on {handle} was stored"
    finally:
        set_available(owner_client, SKU_GLOW38, before)


def test_repeat_restock_subscription_creates_no_second_row(anon_client, owner_client, db):
    """Asking twice while waiting stores one subscription.

    cov: C-CF-165
    """
    set_available(owner_client, SKU_NATO_NAVY, 0)
    email = unique_email()
    ok_json(anon_client.post(f"/products/{NATO_NAVY}/restock-subscriptions", json={"email": email}), "first subscription")
    anon_client.post(f"/products/{NATO_NAVY}/restock-subscriptions", json={"email": email})
    rows = db.subscriptions(db.product(NATO_NAVY)["id"], email)
    assert len(rows) == 1, f"two requests stored {len(rows)} subscriptions"


def test_owner_stock_rows_carry_on_hand_reserved_available(owner_client):
    """Every owner stock row carries sku, title, on_hand, reserved and available that agree.

    cov: C-CF-166
    """
    rows = stock_rows(owner_client)
    assert SKU_NATO_AQUA in [r.get("sku") for r in rows], "owner stock has no STRAP-NATO-AQUA row"
    for row in rows:
        missing = [k for k in ("sku", "title", "on_hand", "reserved", "available") if k not in row]
        assert not missing, f"stock row {row} lacks {missing}"
        assert int(row["available"]) == int(row["on_hand"]) - int(row["reserved"]), f"stock row {row} does not add up"


def test_stock_adjustment_moves_on_hand_with_ledger_entry(owner_client, db):
    """A +2 adjustment moves on_hand by 2 and records an adjustment ledger row.

    cov: C-CF-167
    """
    item = db.inventory(SKU_RUBBER_NAVY_S)
    before = stock_row(owner_client, SKU_RUBBER_NAVY_S)
    rows_before = len(db.ledger_rows(item["id"]))
    payload = ok_json(adjust(owner_client, SKU_RUBBER_NAVY_S, 2, "probe restock"), "a +2 adjustment")
    try:
        assert int(payload["on_hand"]) == int(before["on_hand"]) + 2, f"the adjustment returned {payload}"
        rows = db.ledger_rows(item["id"])
        assert len(rows) == rows_before + 1, f"the ledger gained {len(rows) - rows_before} rows"
        assert (rows[-1]["reason"], int(rows[-1]["delta"])) == ("adjustment", 2), f"the new ledger row reads {rows[-1]}"
    finally:
        adjust(owner_client, SKU_RUBBER_NAVY_S, -2, "probe restore")
    assert {"sku", "on_hand", "reserved", "available"} <= set(payload), f"the adjustment answered {payload}"


def test_adjustment_below_reserved_rejected(anon_client, carts, owner_client):
    """An adjustment that would leave on_hand under reserved is rejected and changes nothing.

    cov: C-CF-168
    """
    ensure_available(owner_client, SKU_RUBBER_NAVY_L, 3)
    token = carts()
    added_cart(anon_client, token, SKU_RUBBER_NAVY_L, 2)
    row = stock_row(owner_client, SKU_RUBBER_NAVY_L)
    delta = -(int(row["on_hand"]) - int(row["reserved"]) + 1)
    expect_client_error(adjust(owner_client, SKU_RUBBER_NAVY_L, delta), f"an adjustment of {delta}")
    assert stock_row(owner_client, SKU_RUBBER_NAVY_L)["on_hand"] == row["on_hand"], "the rejected adjustment moved on_hand"


def test_zero_delta_adjustment_rejected(owner_client, db):
    """A zero delta and an unknown sku are rejected and add no ledger row.

    cov: C-CF-169
    """
    item = db.inventory(SKU_RUBBER_NAVY_S)
    rows_before = len(db.ledger_rows(item["id"]))
    expect_client_error(adjust(owner_client, SKU_RUBBER_NAVY_S, 0), "a zero delta adjustment")
    expect_client_error(adjust(owner_client, "NO-SUCH-SKU-2", 1), "an adjustment on an unknown sku")
    assert len(db.ledger_rows(item["id"])) == rows_before, "a rejected adjustment wrote a ledger row"


def test_restock_mails_each_waiting_subscriber_once_with_back_in_stock_mailed_again_after_resubscribing(anon_client, owner_client, inbox):
    """Two waiting subscribers each get one Back in stock mail, a second restock mails nobody again, and a resubscriber is mailed again.

    cov: C-CF-170, C-CF-220
    """
    set_available(owner_client, SKU_NATO_NAVY, 0)
    emails = [unique_email(), unique_email()]
    for email in emails:
        ok_json(anon_client.post(f"/products/{NATO_NAVY}/restock-subscriptions", json={"email": email}), "subscribe")
    subject = f"{RESTOCK_PREFIX} NATO Strap Navy"
    try:
        set_available(owner_client, SKU_NATO_NAVY, 3)
        for email in emails:
            assert poll_until(lambda: inbox.find(to=email, subject_contains=subject)), f"no {subject!r} mail reached {email}"
        set_available(owner_client, SKU_NATO_NAVY, 0)
        set_available(owner_client, SKU_NATO_NAVY, 2)
        settle(3.0)
        for email in emails:
            count = len([s for s in mail_subjects(inbox, email) if s.startswith(subject)])
            assert count == 1, f"{email} received {count} restock mails"
        set_available(owner_client, SKU_NATO_NAVY, 0)
        ok_json(anon_client.post(f"/products/{NATO_NAVY}/restock-subscriptions", json={"email": emails[0]}), "resubscribe")
        set_available(owner_client, SKU_NATO_NAVY, 1)

        def mailed_twice():
            return len([s for s in mail_subjects(inbox, emails[0]) if s.startswith(subject)]) == 2

        assert poll_until(mailed_twice), f"{emails[0]} subscribed again but was not mailed again"
    finally:
        set_available(owner_client, SKU_NATO_NAVY, 0)


def test_mailed_restock_subscriptions_become_notified(anon_client, owner_client, inbox, db):
    """A mailed subscription is stored as notified.

    cov: C-CF-171
    """
    set_available(owner_client, SKU_FUCHSIA, 0)
    email = unique_email()
    ok_json(anon_client.post(f"/products/{FUCHSIA}/restock-subscriptions", json={"email": email}), "subscribe")
    try:
        set_available(owner_client, SKU_FUCHSIA, 1)
        assert poll_until(lambda: inbox.find(to=email, subject_contains=f"{RESTOCK_PREFIX} TOCK 33 Fuchsia")), (
            f"no restock mail reached {email}")
        product_id = db.product(FUCHSIA)["id"]
        rows = poll_until(lambda: [r for r in db.subscriptions(product_id, email) if r.get("status") == "notified"])
        assert rows and rows[0].get("notified_at") is not None, f"the subscription rows read {db.subscriptions(product_id, email)}"
    finally:
        set_available(owner_client, SKU_FUCHSIA, 0)


def test_adjustment_on_in_stock_product_sends_no_restock_mail(anon_client, carts, owner_client, inbox):
    """Raising a product that already has stock mails no waiting subscriber.

    cov: C-CF-172
    """
    before = int(stock_row(owner_client, SKU_SHARK38)["available"])
    set_available(owner_client, SKU_SHARK38, 1)
    token = carts()
    line = line_for(added_cart(anon_client, token, SKU_SHARK38, 1), SKU_SHARK38)
    email = unique_email()
    try:
        ok_json(anon_client.post(f"/products/{SHARK38}/restock-subscriptions", json={"email": email}), "subscribe")
        ok_json(cart_delete(anon_client, token, line["id"]), "releasing the held unit")
        settle(3.0)
        mailed = len(mail_subjects(inbox, email))
        ok_json(adjust(owner_client, SKU_SHARK38, 2, "probe top-up"), "a +2 adjustment on an in-stock product")
        settle(3.0)
        assert len(mail_subjects(inbox, email)) == mailed, "an adjustment on an in-stock product sent restock mail"
    finally:
        set_available(owner_client, SKU_SHARK38, before)


def test_customer_owner_stock_call_denied_with_stock_unchanged(customer_client, db):
    """A customer reading stock or adjusting it is denied and on_hand stays.

    cov: C-CF-173
    """
    on_hand = int(db.inventory(SKU_NATO_AQUA)["on_hand"])
    expect_client_error(customer_client.get("/owner/stock"), "customer GET /api/owner/stock")
    expect_client_error(adjust(customer_client, SKU_NATO_AQUA, 5), "customer POST /api/owner/stock-adjustments")
    assert int(db.inventory(SKU_NATO_AQUA)["on_hand"]) == on_hand, "a denied customer adjustment moved on_hand"


def test_policies_endpoint_returns_returns_window_30(anon_client):
    """GET /api/policies returns the five pinned values.

    cov: C-CF-174
    """
    policies = ok_json(anon_client.get("/policies"), "GET /api/policies")
    expected = {"returns_window_days": 30, "warranty_years": 2, "minimum_age_years": 4, "flat_shipping": 1500,
                "currency": "usd"}
    assert {k: policies.get(k) for k in expected} == expected, f"GET /api/policies returned {policies}"


def test_four_policy_surfaces_state_thirty_day_returns_with_cart_trust_row_easy_returns(page, owner_client):
    """Home, product, cart and shipping surfaces all state thirty day returns.

    cov: C-CF-175, C-FE-11
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    for path in ("/", f"/products/{AQUA}"):
        _, text = html_text(path)
        assert "30 day returns" in text.lower(), f"{path} does not state 30 day returns"
    _, shipping = html_text("/pages/shipping-and-returns")
    assert re.search(r"\b(30|thirty)[- ]day", shipping, re.I), "the shipping page does not state thirty day returns"
    ui_add_to_cart(page, NATO_AQUA)
    visit(page, "/cart")
    assert "Easy 30-Day Returns" in main_text(page), "the cart trust row does not carry Easy 30-Day Returns"


def test_about_page_ends_with_indestructible_close():
    """The about page closes with the indestructible line signed by the founders.

    cov: C-CF-176
    """
    _, text = html_text("/pages/about")
    at = text.find(ABOUT_CLOSE)
    assert at >= 0, "the about page lacks the indestructible close"
    assert "Mara and Joel Ellison" in text[at:], "the close is not signed by Mara and Joel Ellison"


def test_faq_carries_six_anchored_questions():
    """The FAQ carries the six questions with their six anchors.

    cov: C-CF-177
    """
    markup = page_html("/pages/faq").text
    text = normalise_text(TAG_RE.sub(" ", markup))
    for anchor, question in FAQ_QUESTIONS:
        assert re.search(rf"""id\s*=\s*["']{anchor}["']""", markup), f"the FAQ has no #{anchor} anchor"
        assert question in text, f"the FAQ lacks the question {question!r}"


def test_user_guide_carries_three_ordered_procedures():
    """Each user guide heading is followed by an ordered list.

    cov: C-CF-178
    """
    markup = html.unescape(page_html("/pages/user-guide").text)
    positions = [markup.find(h) for h in GUIDE_HEADINGS]
    assert all(p >= 0 for p in positions), f"the user guide lacks headings {GUIDE_HEADINGS}"
    bounds = positions[1:] + [len(markup)]
    for heading, start, end in zip(GUIDE_HEADINGS, positions, bounds):
        assert re.search(r"<ol[\s>]", markup[start:end], re.I), f"{heading!r} is not followed by an ordered list"


def test_user_guide_dial_set_to_15_min_at_minute_38_with_rotation_138(page):
    """The user guide dial carries 15, 38 and 138.

    cov: C-CF-179
    """
    visit(page, "/pages/user-guide")
    state = dial_state(page, "guide")
    assert (state["segment"], state["start"], state["rotation"]) == ("15", "38", "138"), f"the guide dial reads {state}"


def test_shipping_page_carries_po_box_rule():
    """The shipping page is headed Shipping & Returns and carries the PO box rule.

    cov: C-CF-180
    """
    _, text = html_text("/pages/shipping-and-returns")
    assert "Shipping & Returns" in text and PO_BOX_RULE in text, "the shipping page lacks its heading or the PO box rule"


def test_contact_page_shows_mailboxes_with_hours():
    """The contact page shows both mailboxes and the hours.

    cov: C-CF-181
    """
    _, text = html_text("/pages/contact-us")
    for copy in ("Customer care and general inquiries: care@example.com", "Press inquiries: press@example.com",
                 "We are available Monday through Friday, 10am - 5pm EST"):
        assert copy in text, f"the contact page lacks {copy!r}"


def test_support_request_returns_reference_with_routed_queue(anon_client, db):
    """Each subject routes to its queue with an SR- reference stored.

    cov: C-CF-182
    """
    email = unique_email()
    for subject, queue in (("Order question", "orders"), ("Warranty or repair", "warranty"), ("Press", "press"),
                           ("Something else", "general")):
        payload = ok_json(anon_client.post("/support-requests", json={"name": "Probe", "email": email,
                                                                       "subject": subject, "message": "Hello"}),
                          f"support request {subject}")
        assert REFERENCE_RE.match(str(payload.get("reference"))) and payload.get("queue") == queue, (
            f"subject {subject!r} returned {payload}")
        row = db.support_request(payload["reference"])
        assert row is not None and row.get("queue") == queue, f"the support_requests row reads {row}"
    assert db.count_support_requests(email) == 4, "four support requests were not all stored"


def test_support_request_with_invalid_email_rejected(anon_client, db):
    """An invalid email, an unknown subject or a missing message is rejected naming the field.

    cov: C-CF-183
    """
    email = unique_email()
    for body, field in (({"name": "Probe", "email": "not-an-email", "subject": "Press", "message": "Hi"}, "email"),
                        ({"name": "Probe", "email": email, "subject": "Refund", "message": "Hi"}, "subject"),
                        ({"name": "Probe", "email": email, "subject": "Press"}, "message")):
        response = anon_client.post("/support-requests", json=body)
        expect_client_error(response, f"a support request with a bad {field}")
        assert field in response.text, f"the rejection does not name {field}: {response.text[:300]}"
    assert db.count_support_requests(email) == 0, "a rejected support request was stored"


def test_footer_links_privacy_page_on_every_public_page():
    """Every public page links /pages/privacy.

    cov: C-CF-184
    """
    for path in PUBLIC_ROUTES:
        assert "/pages/privacy" in internal_hrefs(page_html(path).text), f"{path} does not link /pages/privacy"


def test_footer_links_terms_page_on_every_public_page():
    """Every public page links /pages/terms.

    cov: C-CF-185
    """
    for path in PUBLIC_ROUTES:
        assert "/pages/terms" in internal_hrefs(page_html(path).text), f"{path} does not link /pages/terms"


def test_privacy_page_states_what_shop_records():
    """The privacy page names what is kept, and what never is.

    cov: C-CF-186
    """
    _, text = html_text("/pages/privacy")
    lowered = text.lower()
    for word in ("email", "name", "shipping address", "order", "review", "child", "birthday", "card"):
        assert word in lowered, f"the privacy page does not mention {word!r}"


def test_sitemap_lists_every_public_route(anon_client):
    """The sitemap lists the absolute address of every public route.

    cov: C-CF-187
    """
    locs = sitemap_locations()
    assert all(loc.startswith(("http://", "https://")) for loc in locs), "the sitemap lists relative addresses"
    paths = {urlparse(loc).path.rstrip("/") or "/" for loc in locs}
    expected = {"/", "/search"} | {f"/collections/{c}" for c in COLLECTIONS} | set(CONTENT_PAGES)
    expected |= {f"/products/{h}" for h in handles_of(collection_json(anon_client, "all")["products"])}
    missing = sorted(expected - paths)
    assert not missing, f"the sitemap lacks {missing}"


def test_sitemap_excludes_private_routes():
    """The sitemap lists no account, cart, checkout, order, owner or unpublished page.

    cov: C-CF-188
    """
    paths = [urlparse(loc).path for loc in sitemap_locations()]
    private = [p for p in paths if p.startswith(("/account", "/cart", "/checkout", "/orders", "/owner"))
               or p.endswith(LILAC_DRAFT)]
    assert not private, f"the sitemap lists private routes {private}"


def test_robots_file_names_sitemap_with_disallow_owner():
    """robots.txt names the sitemap and disallows the private areas.

    cov: C-CF-189
    """
    response = page_html("/robots.txt")
    lines = [line.strip() for line in response.text.splitlines()]
    for line in (f"Sitemap: {base_url()}/sitemap.xml", "Disallow: /owner/", "Disallow: /account", "Disallow: /checkout",
                 "Disallow: /cart"):
        assert line in lines, f"robots.txt lacks the line {line!r}"


def test_every_internal_link_on_public_routes_resolves():
    """Every same-origin link on the public routes reaches a real page.

    cov: C-CF-190
    """
    targets = sorted({href for path in PUBLIC_ROUTES for href in internal_hrefs(page_html(path).text)})
    broken = []
    for href in targets[:250]:
        response = httpx.get(f"{base_url()}{href}", timeout=30.0, follow_redirects=True)
        if response.status_code >= 400:
            broken.append((href, response.status_code))
    assert not broken, f"internal links that do not resolve: {broken}"


def test_content_images_carry_alternative_text():
    """Every img carries an alt attribute and the aqua front view is described.

    cov: C-CF-191
    """
    for path in ("/", f"/products/{AQUA}", "/collections/all"):
        markup = page_html(path).text
        bare = [tag[:80] for tag in re.findall(r"<img\b[^>]*>", markup, re.I) if not re.search(r"\balt\s*=", tag, re.I)]
        assert not bare, f"{path} carries images without alternative text: {bare}"
    assert "TOCK 33 Aqua, front view" in html.unescape(page_html(f"/products/{AQUA}").text), (
        "the aqua page has no image described as TOCK 33 Aqua, front view")


def test_narrow_viewport_pages_never_scroll_sideways(narrow_page):
    """At 390px home, a collection, a product and the cart never scroll sideways.

    cov: C-CF-192
    """
    for path in ("/", "/collections/all", f"/products/{AQUA}", "/cart"):
        visit(narrow_page, path)
        overflow = narrow_page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        assert overflow <= 1, f"{path} scrolls sideways by {overflow}px at 390px"


def test_narrow_viewport_menu_reveals_navigation_links(narrow_page):
    """At 390px the menu control reveals the five navigation links.

    cov: C-CF-193
    """
    visit(narrow_page, "/")
    narrow_page.get_by_role("button", name=re.compile(r"menu|navigation", re.I)).first.click()
    for name in NAV_LINKS:
        link = narrow_page.locator("a:visible").filter(has_text=re.compile(rf"^\s*{re.escape(name)}\s*$")).first
        expect(link).to_be_visible()


def test_owner_stock_page_shows_stock_columns(page):
    """The owner stock page shows the four columns and the adjustment controls.

    cov: C-CF-194
    """
    ui_sign_in(page, OWNER_EMAIL, return_to="/owner/stock")
    page.wait_for_url(re.compile(r"/owner/stock"))
    for column in ("SKU", "On hand", "Held", "Available"):
        expect(page.get_by_role("columnheader", name=column, exact=True).first).to_be_visible()
    text = main_text(page)
    for copy in ("Adjust by", "Reason", "Save adjustment"):
        assert copy in text, f"the owner stock page lacks {copy!r}"


def test_owner_console_asks_basis_before_publishing_minor_review(page, fresh_customer, db):
    """Publishing a review that mentions a child first asks for Basis for publishing.

    cov: C-CF-195
    """
    _, author = fresh_customer
    review = pending_review(author, WOVEN_SAND, mentions_minor=True)
    ui_sign_in(page, OWNER_EMAIL, return_to="/owner/reviews")
    page.wait_for_url(re.compile(r"/owner/reviews"))
    expect(page.get_by_text("Reviews waiting").first).to_be_visible()
    row = smallest_container(page, [review["title"], "Publish"])
    assert row is not None, f"the moderation queue does not show {review['title']!r} with Publish"
    row.query_selector("text=Publish").click()
    expect(page.get_by_text("Basis for publishing").first).to_be_visible()
    assert db.review(review["id"]).get("status") == "pending", "the minor review published before a basis was given"


def test_customer_opening_owner_page_sees_not_found(page):
    """A signed-in customer gets the 404 page on both owner pages.

    cov: C-CF-196
    """
    ui_sign_in(page, CUSTOMER_EMAIL)
    for path in ("/owner/reviews", "/owner/stock"):
        response = visit(page, path)
        assert response is not None and response.status == 404, f"a customer opening {path} got {response and response.status}"


def test_anonymous_owner_page_visit_redirects_to_login_with_return_to():
    """Anonymous owner page visits redirect to login carrying the page path.

    cov: C-CF-197
    """
    for path in ("/owner/reviews", "/owner/stock"):
        status, location = redirect_target(path)
        assert 300 <= status < 400 and location == f"/account/login?return_to={path}", (
            f"anonymous GET {path} answered {status} to {location!r}")


def test_anonymous_account_or_order_visit_redirects_to_login_with_return_to():
    """Anonymous account and order visits redirect to login carrying the path.

    cov: C-UF-01
    """
    for path in ("/account", "/orders/TK-SEEDED01"):
        status, location = redirect_target(path)
        assert 300 <= status < 400 and location == f"/account/login?return_to={path}", (
            f"anonymous GET {path} answered {status} to {location!r}")


def test_password_sign_in_lands_on_return_to_path(page):
    """Password sign-in lands on a valid return_to, and on /account without one.

    cov: C-UF-02
    """
    ui_sign_in(page, CUSTOMER_EMAIL, return_to="/pages/faq")
    page.wait_for_url(re.compile(r"/pages/faq$"))
    page.context.clear_cookies()
    ui_sign_in(page, CUSTOMER_EMAIL)
    page.wait_for_url(re.compile(r"/account$"))


def test_sign_out_ends_session_landing_home(page):
    """Sign out lands on / and the account page then asks to sign in again.

    cov: C-UF-03
    """
    email, _ = signup()
    ui_sign_in(page, email, password="probe-pass-2026x", return_to="/account")
    page.wait_for_url(re.compile(r"/account$"))
    page.get_by_role("button", name="Sign out").or_(page.get_by_role("link", name="Sign out")).first.click()
    page.wait_for_url(re.compile(r"^" + re.escape(base_url()) + r"/?$"))
    visit(page, "/account")
    page.wait_for_url(re.compile(r"/account/login"))


def test_unknown_address_shows_shop_own_not_found_page_with_404():
    """An unknown address answers the shop's own 404 page linking home.

    cov: C-UF-04
    """
    response = page_html(f"/no-such-page-{os.urandom(3).hex()}")
    assert response.status_code == 404, f"an unknown address answered {response.status_code}"
    assert "text/html" in response.headers.get("content-type", ""), "the 404 is not the shop's HTML page"
    assert "/" in internal_hrefs(response.text), "the not-found page has no link back to /"


def test_account_with_no_orders_shows_you_have_no_orders_yet(page):
    """A new account shows You have no orders yet. with a link to Shop All.

    cov: C-UF-17
    """
    email, _ = signup()
    ui_sign_in(page, email, password="probe-pass-2026x", return_to="/account")
    page.wait_for_url(re.compile(r"/account$"))
    expect(page.get_by_text("You have no orders yet.").first).to_be_visible()
    assert page.locator("a[href$='/collections/all']").count() >= 1, "the empty account links nowhere to /collections/all"


def test_empty_cart_shows_your_cart_is_empty():
    """The cart page with no cart says Your cart is empty. with Continue browsing.

    cov: C-UF-18
    """
    _, text = html_text("/cart")
    assert "Your cart is empty." in text and "Continue browsing" in text, "the empty cart page lacks its empty state"


def test_refused_action_shows_inline_banner_naming_reason(page):
    """A refused sign-in keeps the page and shows a message naming the refusal.

    cov: C-UF-19
    """
    visit(page, "/account/login")
    form = page.locator("form").filter(has=page.get_by_label("Password", exact=True)).first
    form.get_by_label("Email", exact=True).fill(CUSTOMER_EMAIL)
    form.get_by_label("Password", exact=True).fill("wrong-password-2026")
    form.get_by_role("button", name="Sign in", exact=True).click()
    banner = page.get_by_text(re.compile(r"incorrect|invalid|wrong|did not match|does not match|could not|couldn't",
                                         re.I)).first
    expect(banner).to_be_visible()
    expect(page.get_by_label("Password", exact=True).first).to_be_visible()


def test_new_address_signs_in_by_emailed_link_landing_on_account_page(page, inbox):
    """The sign-in page mails a link to a new address, and opening it lands signed in on /account.

    cov: C-UF-11
    """
    email = unique_email()
    visit(page, "/account/login")
    form = page.locator("form").filter(has=page.get_by_role("button", name="Send link")).first
    form.get_by_label("Email", exact=True).fill(email)
    form.get_by_role("button", name="Send link").click()
    expect(page.get_by_text("If that address can receive mail, a sign-in link is on its way.").first).to_be_visible()
    token = link_token_from_mail(inbox, email)
    assert token, f"no sign-in link reached {email}"
    visit(page, f"{LINK_MARKER}{token}")
    page.wait_for_url(re.compile(r"/account$"))
    expect(page.get_by_text("Your account").first).to_be_visible()

def test_body_text_meets_wcag_aa_contrast_against_background(page):
    """Body paragraphs on home and a product page reach 4.5:1 against their ground.

    cov: C-UX-05
    """
    for path in ("/", f"/products/{AQUA}"):
        visit(page, path)
        failures = page.evaluate(CONTRAST_JS)
        assert not failures, f"{path} body text below 4.5:1: {failures[:5]}"


def test_headings_set_in_jost_with_body_text_in_cabin(page):
    """The h1 is set in Jost and body text in Cabin, both loaded.

    cov: C-UX-06
    """
    visit(page, "/")
    heading = page.locator("h1").first.evaluate("e => getComputedStyle(e).fontFamily")
    body = page.locator("p").first.evaluate("e => getComputedStyle(e).fontFamily")
    assert heading.strip("'\" ").lower().startswith("jost"), f"the h1 font-family is {heading!r}"
    assert body.strip("'\" ").lower().startswith("cabin"), f"body text font-family is {body!r}"
    loaded = page.evaluate("async () => { await document.fonts.ready;"
                           " return [document.fonts.check('600 20px Jost'), document.fonts.check('400 16px Cabin')]; }")
    assert loaded == [True, True], f"Jost and Cabin loaded states read {loaded}"
    weight = page.locator("h1").first.evaluate("e => getComputedStyle(e).fontWeight")
    assert str(weight) in ("600", "700"), f"the h1 weight is {weight}"


def test_cart_drawer_closes_on_escape_returning_focus(page):
    """The header cart control opens a dialog that Escape closes, handing focus back.

    cov: C-UX-09
    """
    visit(page, "/")
    control = page.get_by_role("button", name=re.compile(r"^(?!Add).*\bCart\b")).first
    control.click()
    drawer = page.get_by_role("dialog").first
    expect(drawer).to_be_visible()
    page.keyboard.press("Escape")
    expect(drawer).to_be_hidden()
    assert control.evaluate("e => e === document.activeElement"), "focus did not return to the cart control"


def test_under_reduced_motion_no_decorative_animation_runs(reduced_page):
    """With reduced motion no animation longer than a short cross-fade runs as the home page arrives.

    cov: C-UX-12
    """
    reduced_page.add_init_script(ANIMATION_WATCH_JS)
    visit(reduced_page, "/")
    settle(1.5)
    running = reduced_page.evaluate("() => window.__probeAnimations || []")
    assert not running, f"decorative animations ran under reduced motion: {running[:5]}"


def test_dark_colour_scheme_preference_keeps_light_design(page, dark_page):
    """A dark scheme preference renders the same page, header and text colours as light.

    cov: C-UX-13
    """
    readings = []
    for surface in (page, dark_page):
        visit(surface, "/")
        readings.append(surface.evaluate(
            "() => [getComputedStyle(document.body).backgroundColor, getComputedStyle(document.body).color,"
            " getComputedStyle(document.querySelector('h1')).color]"))
    assert readings[0] == readings[1], f"light reads {readings[0]}, dark reads {readings[1]}"


def test_skip_to_content_is_first_keyboard_stop(page):
    """The first Tab lands on Skip to content.

    cov: C-UX-15
    """
    visit(page, "/")
    page.keyboard.press("Tab")
    focused = page.evaluate("() => (document.activeElement.innerText || document.activeElement.textContent || '').trim()")
    assert focused == "Skip to content", f"the first keyboard stop is {focused!r}"


def test_icon_only_controls_carry_hidden_labels_my_account_search_cart(page):
    """The header icon controls are named My Account, Search and Cart.

    cov: C-UX-16
    """
    visit(page, "/")
    for name in ("My Account", "Search"):
        named = page.get_by_role("link", name=name, exact=True).or_(page.get_by_role("button", name=name, exact=True))
        assert named.count() >= 1, f"no control carries the label {name!r}"
    cart = page.get_by_role("link", name=re.compile(r"^(?!Add).*\bCart\b")).or_(
        page.get_by_role("button", name=re.compile(r"^(?!Add).*\bCart\b")))
    assert cart.count() >= 1, "no control carries the label Cart"


def test_every_page_declares_its_language():
    """Every public route declares a language on its html element.

    cov: C-UX-17
    """
    for path in PUBLIC_ROUTES:
        markup = page_html(path).text
        assert re.search(r"""<html\b[^>]*\blang\s*=\s*["'][A-Za-z]""", markup, re.I), f"{path} declares no language"


def test_health_route_api_health_answers_200_once_ready_without_token():
    """GET /api/health answers 200 with no token.

    cov: C-TR-01, C-DC-04
    """
    response = httpx.get(f"{api_url()}/health", timeout=30.0)
    assert response.status_code == 200, f"GET /api/health returned {response.status_code}"


def test_product_pages_arrive_as_complete_server_rendered_html_with_prices(anon_client):
    """Product and collection HTML carries copy, prices, availability and reviews before scripts.

    cov: C-TR-02
    """
    availability_copy = {"in_stock": "Item is in stock", "low_stock": "Only a few left",
                         "out_of_stock": "Item is out of stock", "unavailable": "Item is unavailable"}
    status, text = html_text(f"/products/{AQUA}")
    assert status == 200, f"GET /products/{AQUA} returned {status}"
    expected = availability_copy[product_json(anon_client, AQUA)["availability"]]
    for copy in ("TOCK 33 Aqua", "$189.00", expected, "Fewer questions in the car"):
        assert copy in text, f"the first HTML of the aqua page lacks {copy!r}"
    _, grid = html_text("/collections/tock-38")
    assert "TOCK 38 Grey" in grid and "$379.00" in grid, "the first HTML of the TOCK 38 grid lacks titles or prices"


def test_typefaces_served_from_app_own_origin(page):
    """Every font file the home page loads comes from the app's origin.

    cov: C-TR-03
    """
    fonts = []
    page.on("request", lambda request: fonts.append(request.url) if request.resource_type == "font" else None)
    visit(page, "/")
    page.evaluate("async () => { await document.fonts.ready; }")
    assert fonts, "the home page loaded no font files"
    foreign = [url for url in fonts if not url.startswith(base_url())]
    assert not foreign, f"fonts loaded from other origins: {foreign}"


def test_api_money_fields_integer_cents_with_currency_usd(anon_client, customer2_client, carts):
    """Product, cart and order money is integer cents with currency usd.

    cov: C-TR-05
    """
    product = product_json(anon_client, AQUA)
    assert isinstance(product["price"], int) and product["currency"] == "usd", f"product money reads {product['price']!r} {product['currency']!r}"
    token = carts()
    cart = added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    assert isinstance(cart["subtotal"], int), f"cart subtotal reads {cart['subtotal']!r}"
    order = ok_json(customer2_client.get("/orders/TK-SEEDED01"), "GET /api/orders/<number> TK-SEEDED01")
    assert [order["subtotal"], order["shipping"], order["total"], order["currency"]] == [2200, 1500, 3700, "usd"], (
        f"the seeded order money reads {order}")
    assert all(isinstance(order[k], int) for k in ("subtotal", "shipping", "total")), f"order money is not integer: {order}"


def test_bundle_add_holds_both_watches_or_neither(anon_client, owner_client):
    """Six carts racing for one Glow and Glow bundle hold both watches once, and a missing watch holds neither.

    cov: C-TR-06
    """
    glow38 = int(stock_row(owner_client, SKU_GLOW38)["available"])
    glow33 = int(stock_row(owner_client, SKU_GLOW33)["available"])
    set_available(owner_client, SKU_GLOW38, 1)
    set_available(owner_client, SKU_GLOW33, 4)
    tokens = [new_cart(anon_client) for _ in range(6)]
    try:
        r38 = int(stock_row(owner_client, SKU_GLOW38)["reserved"])
        r33 = int(stock_row(owner_client, SKU_GLOW33)["reserved"])
        results = race([{"method": "POST", "path": "/cart/lines", "json": {"sku": SKU_BUNDLE_GLOW_GLOW, "quantity": 1},
                         "headers": {"X-Cart-Token": t}} for t in tokens])
        winners = [r for r in results if r is not None and r.status_code in (200, 201)]
        assert len(winners) == 1, f"{len(winners)} bundle adds won one TK38-GLOW"
        assert int(stock_row(owner_client, SKU_GLOW38)["reserved"]) == r38 + 1, "TK38-GLOW holds do not match one bundle"
        assert int(stock_row(owner_client, SKU_GLOW33)["reserved"]) == r33 + 1, "TK33-GLOW holds do not match one bundle"
        set_available(owner_client, SKU_NAVY, 0)
        black = int(ensure_available(owner_client, SKU_BLACK38, 1)["reserved"])
        expect_client_error(cart_add(anon_client, new_cart(anon_client), SKU_BUNDLE_BLACK_NAVY, 1),
                            "adding Black and Navy with no TOCK 33 Navy")
        assert int(stock_row(owner_client, SKU_BLACK38)["reserved"]) == black, "the refused bundle still held TOCK 38 Black"
    finally:
        for token in tokens:
            for line in lines_of(ok_json(cart_get(anon_client, token), "GET /api/cart")):
                if not line.get("is_gift"):
                    cart_delete(anon_client, token, line["id"])
        set_available(owner_client, SKU_GLOW38, glow38)
        set_available(owner_client, SKU_GLOW33, glow33)


def test_accounts_table_stores_seeded_accounts_by_email(db):
    """The accounts table stores the three seeded rows with roles and hashed passwords.

    cov: C-DM-01
    """
    for email, name, role in ((CUSTOMER_EMAIL, CUSTOMER_NAME, "customer"), (CUSTOMER2_EMAIL, CUSTOMER2_NAME, "customer"),
                              (OWNER_EMAIL, OWNER_NAME, "owner")):
        row = db.account(email)
        assert row is not None, f"the accounts table has no row for {email}"
        assert (row.get("name"), row.get("role")) == (name, role), f"the {email} row reads {row}"
        stored = str(row.get("password_hash") or "")
        assert stored and SEEDED_PASSWORD not in stored, f"the {email} password is not stored hashed"


def test_reserved_count_never_exceeds_on_hand_in_inventory_items(anon_client, carts, db):
    """With a live hold every inventory_items row keeps 0 <= reserved <= on_hand.

    cov: C-DM-02
    """
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    rows = db.inventory_rows()
    assert rows, "the inventory_items table is empty"
    bad = [r for r in rows if not (0 <= int(r["reserved"]) <= int(r["on_hand"]))]
    assert not bad, f"inventory rows break reserved <= on_hand: {bad}"


def test_stock_ledger_deltas_sum_to_on_hand_for_every_inventory_item_row(db):
    """For every inventory row the stock ledger deltas sum to on_hand.

    cov: C-DM-03
    """
    totals = {}
    for entry in db.all_ledger_rows():
        totals[entry["inventory_item_id"]] = totals.get(entry["inventory_item_id"], 0) + int(entry["delta"])
    rows = db.inventory_rows()
    assert rows, "the inventory_items table is empty"
    bad = [(r["id"], r["on_hand"], totals.get(r["id"], 0)) for r in rows if int(r["on_hand"]) != totals.get(r["id"], 0)]
    assert not bad, f"inventory rows whose ledger does not sum to on_hand (id, on_hand, sum): {bad}"


def test_held_reservations_sum_to_reserved_count(anon_client, carts, db):
    """For every inventory row the held reservation quantities sum to reserved.

    cov: C-DM-04
    """
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 2)
    held = {}
    for reservation in db.all_held_reservations():
        key = reservation["inventory_item_id"]
        held[key] = held.get(key, 0) + int(reservation["quantity"])
    bad = [(r["id"], r["reserved"], held.get(r["id"], 0)) for r in db.inventory_rows()
           if int(r["reserved"]) != held.get(r["id"], 0)]
    assert not bad, f"inventory rows whose held reservations differ from reserved (id, reserved, held): {bad}"


def test_restock_subscriptions_table_holds_one_waiting_row_per_product_email(anon_client, owner_client, db):
    """No product and email pair holds two waiting subscriptions, even after a repeat request.

    cov: C-DM-08
    """
    set_available(owner_client, SKU_NATO_NAVY, 0)
    email = unique_email()
    for _ in range(2):
        anon_client.post(f"/products/{NATO_NAVY}/restock-subscriptions", json={"email": email})
    pairs = {}
    for row in db.waiting_subscriptions():
        key = (row["product_id"], str(row["email"]).lower())
        pairs[key] = pairs.get(key, 0) + 1
    doubled = {k: v for k, v in pairs.items() if v > 1}
    assert not doubled, f"product and email pairs with more than one waiting row: {doubled}"
    assert db.count_waiting_subscriptions(db.product(NATO_NAVY)["id"], email) == 1, "the repeat request left no single waiting row"


def test_seeded_aqua_product_carries_sku_tk33_aqua_at_price_18900(db, anon_client):
    """TOCK 33 Aqua is stored and served with sku TK33-AQUA at 18900.

    cov: C-DM-09
    """
    variant = db.variant(SKU_AQUA)
    product = db.product(AQUA)
    assert variant is not None and product is not None, "the aqua product or its TK33-AQUA variant is missing"
    assert (variant["product_id"], int(variant["price"])) == (product["id"], 18900), f"the TK33-AQUA variant reads {variant}"
    served = product_json(anon_client, AQUA)["variants"]
    assert [(v["sku"], v["price"]) for v in served] == [(SKU_AQUA, 18900)], f"the API variants read {served}"


def test_seeded_bundles_pair_tock_38_watch_with_tock_33_watch(anon_client):
    """Each seeded bundle holds one TOCK 38 watch and one TOCK 33 watch.

    cov: C-DM-10
    """
    pairs = {BUNDLE_BLACK_NAVY: {BLACK38, NAVY}, BUNDLE_GREY_AQUA: {GREY38, AQUA}, BUNDLE_GLOW_GLOW: {GLOW38, GLOW33},
             BUNDLE_SHARK_FUCHSIA: {SHARK38, FUCHSIA}}
    for bundle, watches in pairs.items():
        components = set(handles_of(product_json(anon_client, bundle).get("components", [])))
        assert components == watches, f"{bundle} components are {sorted(components)}, expected {sorted(watches)}"


def test_seeded_order_tk_seeded01_belongs_to_customer2_with_killbill_invoice_37(db, payments):
    """TK-SEEDED01 belongs to customer2, totals 3700 and has one 37.00 USD Kill Bill invoice.

    cov: C-DM-11
    """
    order = db.order("TK-SEEDED01")
    assert order is not None, "the orders table has no TK-SEEDED01"
    assert order["account_id"] == db.account(CUSTOMER2_EMAIL)["id"], "TK-SEEDED01 does not belong to customer2"
    assert (int(order["subtotal"]), int(order["shipping"]), int(order["total"])) == (2200, 1500, 3700), f"TK-SEEDED01 reads {order}"
    account, invoices = killbill_invoices_for_key(payments, "tock-customer2@example.com", 1)
    assert account is not None, "Kill Bill has no account keyed tock-customer2@example.com"
    assert [(i.amount, i.currency.upper()) for i in invoices] == [(3700, "USD")], f"customer2 invoices read {invoices}"
    assert order["status"] == "placed" and order.get("shipping_country") == "US", f"TK-SEEDED01 reads {order}"
    assert [l.get("sku_snapshot") for l in db.order_lines(order["id"])] == [SKU_NATO_AQUA], "TK-SEEDED01 does not hold one NATO Strap Aqua"
    notes = [r for r in db.ledger_rows(db.inventory(SKU_NATO_AQUA)["id"]) if "TK-SEEDED01" in str(r.get("note"))]
    assert not notes, "seeding TK-SEEDED01 wrote a stock ledger entry"


def test_restarting_app_duplicates_no_seeded_rows(db):
    """Each seeded account, product, sku, imported review and the seeded order exists exactly once.

    cov: C-DM-12
    """
    for email in (CUSTOMER_EMAIL, CUSTOMER2_EMAIL, OWNER_EMAIL):
        assert db.count_accounts(email) == 1, f"{email} has {db.count_accounts(email)} rows"
    for handle in PUBLISHED_HANDLES + [LILAC_DRAFT]:
        assert db.count_products(handle) == 1, f"{handle} has {db.count_products(handle)} rows"
    for sku in (SKU_AQUA, SKU_NATO_AQUA, SKU_TOTE, SKU_BUNDLE_GREY_AQUA, SKU_LILAC):
        assert db.count_variants(sku) == 1, f"{sku} has {db.count_variants(sku)} variant rows"
    aqua = db.product(AQUA)["id"]
    for author in ("Priya", "Tom", "Lena", "Marco", "Ada", "Sam", "Dana"):
        assert db.count_seeded_reviews(aqua, author) == 1, f"the {author} review exists {db.count_seeded_reviews(aqua, author)} times"
    assert db.count_order_numbers("TK-SEEDED01") == 1, "TK-SEEDED01 is duplicated"
    for row in db.inventory_rows():
        seeds = [e for e in db.ledger_rows(row["id"]) if e.get("reason") == "seed"]
        assert len(seeds) <= 1, f"inventory item {row['id']} carries {len(seeds)} seed ledger rows"


def test_every_dial_root_carries_data_dial_hook_with_role(page):
    """Hero, plain, zoned, three stage and the guide dial roots carry data-dial and an image role.

    cov: C-FE-01, C-FE-59
    """
    visit(page, "/")
    for role, count in (("hero", 1), ("plain", 1), ("zoned", 1), ("stage", 3)):
        roots = page.locator(f"[data-dial='{role}']")
        expect(roots).to_have_count(count)
        for i in range(count):
            assert roots.nth(i).get_attribute("role") == "img", f"a {role} dial root has no image role"
            assert roots.nth(i).get_attribute("data-colourway") is not None, f"a {role} dial root has no data-colourway"
    visit(page, "/pages/user-guide")
    expect(page.locator("[data-dial='guide']")).to_have_count(1)
    visit(page, "/")
    for attr in ("data-colourway", "data-segment-minutes", "data-start-minute", "data-bezel-rotation", "data-elapsed-minutes",
                 "data-hour-rotation"):
        assert dial(page, "hero").get_attribute(attr) is not None, f"the hero dial root lacks {attr}"
    assert dial(page, "zoned").get_attribute("data-lit-hour") is not None, "the zoned dial root lacks data-lit-hour"
    assert (dial(page, "plain").get_attribute("data-segment-minutes") or "") == "", "the plain dial with no tock carries a length"


def test_hero_headline_renders_at_step_10_desktop_size(page):
    """At 1280px the hero headline renders at 56px.

    cov: C-FE-04, C-FE-60
    """
    visit(page, "/")
    size = page.locator("h1").first.evaluate("e => parseFloat(getComputedStyle(e).fontSize)")
    assert abs(size - 56) <= 0.5, f"the hero headline renders at {size}px, expected 56px"
    for width, lede in ((390, 17), (900, 19), (1280, 21)):
        page.set_viewport_size({"width": width, "height": 900})
        visit(page, "/")
        size = page.get_by_text("Rotate the bezel and align the start of a tock").first.evaluate(
            "e => parseFloat(getComputedStyle(e).fontSize)")
        assert abs(size - lede) <= 0.5, f"at {width}px the hero lede renders at {size}px, expected {lede}px"


def test_header_carries_five_links_tock_33_tock_38_bundles_straps_about(page):
    """The desktop header shows the five links.

    cov: C-FE-05
    """
    visit(page, "/")
    for name in NAV_LINKS:
        link = page.locator("a:visible").filter(has_text=re.compile(rf"^\s*{re.escape(name)}\s*$")).first
        expect(link).to_be_visible()


def test_footer_carries_statement_why_tock():
    """The footer carries the Why Tock? statement.

    cov: C-FE-06
    """
    _, text = html_text("/")
    statement = "Why Tock? We believe time management is a superpower and the tradition of analog is worth preserving."
    assert statement in text, "the footer lacks the Why Tock? statement"


def test_hero_carries_headline_nobody_is_born_knowing():
    """The h1 reads Nobody is born knowing how long fifteen minutes is.

    cov: C-FE-08
    """
    markup = page_html("/").text
    found = re.search(r"<h1\b[^>]*>(.*?)</h1>", markup, re.S | re.I)
    assert found, "the home page has no h1"
    headline = normalise_text(TAG_RE.sub(" ", found.group(1)))
    assert headline == "Nobody is born knowing how long fifteen minutes is.", f"the h1 reads {headline!r}"


def test_comparison_carries_heading_most_of_clocks_day():
    """The comparison heading reads Most of a clock's day is spent between the numbers.

    cov: C-FE-09
    """
    _, text = html_text("/")
    assert "Most of a clock's day is spent between the numbers." in text, "the comparison heading is missing"


def test_construction_section_carries_four_specification_card_titles():
    """The construction section carries its four card titles.

    cov: C-FE-10
    """
    _, text = html_text("/")
    at = text.find("Kids' watches usually fail at the bit you look through.")
    assert at >= 0, "the construction heading is missing"
    for title in ("Sapphire crystal", "100m water resistance", "Screw-down crown", "Swiss ETA quartz movement"):
        assert title in text[at:], f"the construction section lacks the card {title!r}"


def test_storefront_shows_no_pop_up_overlay(page):
    """Home and a product page open no modal overlay on their own.

    cov: C-CN-01
    """
    for path in ("/", f"/products/{AQUA}"):
        visit(page, path)
        settle(3.0)
        overlays = page.evaluate(
            "() => Array.from(document.querySelectorAll('[role=dialog], [aria-modal=true], dialog[open]'))"
            ".filter(e => e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden').length")
        assert overlays == 0, f"{path} opened {overlays} overlay(s) unprompted"


def test_checkout_offers_no_discount_code_tax_quote_or_wallet_payment_button(page, owner_client):
    """The checkout page offers no discount field, no tax or duty line and no wallet button.

    cov: C-CN-02, C-CN-04, C-CN-05, C-CN-14
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    ui_add_to_cart(page, NATO_AQUA)
    ui_sign_in(page, CUSTOMER_EMAIL, return_to="/checkout")
    page.wait_for_url(re.compile(r"/checkout"))
    expect(page.get_by_role("button", name="Place order").first).to_be_visible()
    text = main_text(page).lower()
    for word in ("discount", "promo code", "coupon", "voucher"):
        assert word not in text, f"the checkout page mentions {word!r}"
    tax_lines = visible_named(page, "body *", r"^([Ee]stimated )?([Tt]ax|[Tt]axes|[Dd]uty|[Dd]uties)$")
    assert tax_lines == 0, "the checkout summary carries a tax or duty line"
    wallets = visible_named(page, "button, a, [role=button]", r"[Aa]pple [Pp]ay|[Gg]oogle [Pp]ay|[Ss]hop [Pp]ay|PayPal|[Aa]mazon [Pp]ay")
    assert wallets == 0, "the checkout offers a wallet payment button"
    card_fields = page.locator("input[autocomplete^='cc-'], input[name*='card' i], input[id*='card' i]").count()
    card_labels = visible_named(page, "label", r"[Cc]ard number|CVC|CVV|[Ee]xpiry|[Pp]ayment method")
    assert card_fields == 0 and card_labels == 0, "the checkout carries a card or payment method field"


def test_home_page_plays_no_video_or_press_ticker(page):
    """The home page carries no video element, embedded player or press ticker.

    cov: C-CN-03, C-CN-11
    """
    markup = page_html("/").text
    assert not re.search(r"<video\b|youtube\.com|vimeo\.com", markup, re.I), "the home page markup embeds video"
    visit(page, "/")
    assert page.locator("video, iframe").count() == 0, "the rendered home page carries a video or player frame"
    ticker = re.search(r"as seen in|featured in|in the press", normalise_text(TAG_RE.sub(" ", markup)), re.I)
    assert not ticker, f"the home page carries a press ticker: {ticker.group(0) if ticker else ''!r}"
    for path in PUBLIC_ROUTES:
        assert not re.search(r"as seen in|featured in|in the press", html_text(path)[1], re.I), f"{path} carries a press ticker"


def test_app_answers_at_app_public_url():
    """The home page answers 200 HTML at APP_PUBLIC_URL.

    cov: C-DC-01
    """
    response = httpx.get(f"{base_url()}/", timeout=30.0)
    assert response.status_code == 200 and "text/html" in response.headers.get("content-type", ""), (
        f"APP_PUBLIC_URL / answered {response.status_code} {response.headers.get('content-type')}")


def test_container_internal_port_4173_serves_health_at_public_url():
    """The port mapping onto 4173 reaches a healthy app at APP_PUBLIC_URL.

    cov: C-DC-02
    """
    response = httpx.get(f"{api_url()}/health", timeout=30.0)
    assert response.status_code == 200, f"APP_PUBLIC_URL, mapped onto 4173, answered health {response.status_code}"


def test_http_api_served_under_api_prefix_on_same_origin():
    """JSON is served under /api on the page origin.

    cov: C-DC-03
    """
    response = httpx.get(f"{base_url()}/api/policies", timeout=30.0)
    assert response.status_code == 200 and "json" in response.headers.get("content-type", ""), (
        f"/api/policies on the page origin answered {response.status_code} {response.headers.get('content-type')}")


def test_server_outlives_session_that_started_process():
    """After the agent session has ended the server still answers.

    cov: C-DC-06
    """
    assert httpx.get(f"{api_url()}/health", timeout=30.0).status_code == 200, "the server is not running after the session"


def test_server_binds_every_interface_rather_than_loopback():
    """The app answers from outside its own container.

    cov: C-DC-07
    """
    response = httpx.get(f"{base_url()}/", timeout=30.0)
    assert response.status_code == 200, f"the app is unreachable from the verifier: {response.status_code}"


def test_list_endpoints_return_top_level_json_array(anon_client, customer2_client, owner_client):
    """Search, reviews, orders, owner reviews and owner stock return top-level arrays.

    cov: C-DC-08
    """
    for c, path, params in ((anon_client, "/search", {"q": "tock"}), (anon_client, f"/products/{AQUA}/reviews", None),
                            (customer2_client, "/orders", None), (owner_client, "/owner/reviews", {"status": "pending"}),
                            (owner_client, "/owner/stock", None)):
        payload = ok_json(c.get(path, params=params), f"GET /api{path}")
        assert isinstance(payload, list), f"GET /api{path} is not a top-level JSON array"


def test_invalid_call_rejected_as_client_error_never_server_error(anon_client, carts):
    """Malformed and incomplete calls answer 4xx, never 5xx.

    cov: C-DC-09
    """
    token = carts()
    calls = [anon_client.post("/cart/lines", content=b"{not json", headers={"X-Cart-Token": token,
                                                                          "Content-Type": "application/json"}),
             anon_client.post("/auth/signup", json={"email": "x"}),
             anon_client.post("/cart/lines", json={"sku": SKU_NATO_AQUA, "quantity": "many"},
                              headers={"X-Cart-Token": token}),
             anon_client.get("/cart", headers={"X-Cart-Token": "no-such-cart-token"})]
    for response in calls:
        expect_client_error(response, f"{response.request.method} {response.request.url.path}")


def test_cart_holds_live_in_datastore_rows_rather_than_browser(anon_client, carts, db):
    """A cart and its hold exist as carts, cart_lines and reservations rows.

    cov: C-DC-10
    """
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    cart = db.cart(token)
    assert cart is not None and cart.get("status") == "open", f"the carts table row for the token reads {cart}"
    assert len(db.cart_line_rows(cart["id"])) == 1, "the cart_lines table holds no line for the cart"
    held = [r for r in db.cart_reservations(cart["id"]) if r.get("status") == "held"]
    assert held and int(held[0]["quantity"]) == 1, f"the reservations table holds {held} for the cart"

def test_passwords_stored_hashed_never_in_readable_form(db):
    """A signup password is stored hashed, never as the readable password.

    cov: C-CF-198
    """
    password = f"probe-readable-{os.urandom(3).hex()}"
    email, _ = signup(password=password)
    row = db.account(email)
    assert row is not None, f"the accounts table has no row for {email}"
    stored = str(row.get("password_hash") or "")
    assert stored and password not in stored, "the password is stored in readable form"
    assert stored.startswith(("pbkdf2:", "scrypt:")), f"the password hash is not a werkzeug.security hash: {stored[:12]!r}"


def test_email_addresses_sign_in_without_regard_to_letter_case(anon_client):
    """The seeded customer signs in with the email in upper case.

    cov: C-CF-199
    """
    response = anon_client.post("/auth/login", json={"email": CUSTOMER_EMAIL.upper(), "password": SEEDED_PASSWORD})
    assert ok_json(response, "POST /api/auth/login with an upper-case email").get("access_token"), (
        "an upper-case email did not sign in")


def test_wrong_password_login_answers_same_as_unknown_email_login(anon_client):
    """A wrong password and an unknown email get the same status and the same body.

    cov: C-CF-200
    """
    unknown = unique_email()
    wrong = anon_client.post("/auth/login", json={"email": CUSTOMER_EMAIL, "password": "not-the-password-1"})
    missing = anon_client.post("/auth/login", json={"email": unknown, "password": "not-the-password-1"})
    assert wrong.status_code == missing.status_code and 400 <= wrong.status_code < 500, (
        f"wrong password answered {wrong.status_code}, unknown email {missing.status_code}")
    assert wrong.text.replace(CUSTOMER_EMAIL, "<email>") == missing.text.replace(unknown, "<email>"), (
        f"the two denials differ: {wrong.text[:200]!r} versus {missing.text[:200]!r}")


def test_customer_changes_own_name_through_account_patch(fresh_customer):
    """PATCH /api/account with a name changes the customer's name.

    cov: C-CF-202
    """
    _, customer = fresh_customer
    patched = ok_json(customer.patch("/account", json={"name": "Renamed Probe"}), "PATCH /api/account with a name")
    assert patched.get("name") == "Renamed Probe", f"the patch returned {patched}"
    account = ok_json(customer.get("/account"), "GET /api/account after the patch")
    assert account.get("name") == "Renamed Probe", f"the account name reads {account.get('name')!r}"


def test_timer_setter_group_is_single_tab_stop(page):
    """Tab leaves the setter group from its selected option, and Shift+Tab returns to that option.

    cov: C-CF-203
    """
    visit(page, "/")
    setter_option(page, "15 min").focus()
    page.keyboard.press("Tab")
    on_radio = page.evaluate("() => { const e = document.activeElement;"
                             " return !!e && (e.getAttribute('role') === 'radio' || (e.tagName === 'INPUT' && e.type === 'radio')); }")
    assert not on_radio, "Tab moved to another tock option instead of leaving the setter group"
    page.keyboard.press("Shift+Tab")
    expect(setter_option(page, "15 min")).to_be_focused()


def test_under_reduced_motion_selecting_tock_moves_ring_straight_to_final_turn(reduced_page):
    """With reduced motion a selection runs no ring animation and the hooks read the final turn at once.

    cov: C-CF-204
    """
    visit(reduced_page, "/")
    reduced_page.evaluate(ANIMATION_SAMPLE_JS)
    setter_option(reduced_page, "30 min").click()
    state = dial_state(reduced_page, "hero")
    assert state["segment"] == "30" and int(state["rotation"]) == ((int(state["start"]) - 30) * 6) % 360, (
        f"the ring did not reach its final turn at once: {state}")
    settle(1.5)
    running = reduced_page.evaluate("() => window.__probeAnimations")
    assert not running, f"selecting a tock under reduced motion animated {running}"


def test_comparison_readout_shows_slider_time_in_polite_live_region(page):
    """At 3:04 the slider readout shows 3:04 inside a polite live region.

    cov: C-CF-205
    """
    visit(page, "/")
    slide_to(comparison_slider(page), 184)
    readout = page.locator("[aria-live='polite'], [role='status'], output").filter(
        has_text=re.compile(r"(^|\s)3:04(\s|$)")).first
    expect(readout).to_be_visible()


def test_best_rated_sort_orders_products_by_average_rating_with_under_three_review_products_after(anon_client):
    """Best-rated puts products with three or more reviews first by average, then the rest.

    cov: C-CF-206
    """
    products = collection_json(anon_client, "tock-33", {"sort": "best-rated"}).get("products", [])
    rated = [p for p in products if int(p.get("review_count") or 0) >= 3]
    head = products[:len(rated)]
    assert [p["handle"] for p in head] == [p["handle"] for p in sorted(rated, key=lambda p: -float(p["rating_average"]))], (
        f"best-rated opens with {handles_of(head)}")
    assert all(int(p.get("review_count") or 0) < 3 for p in products[len(rated):]), "a well-reviewed product sorts late"
    assert handles_of(products).index(GLOW33) < handles_of(products).index(AQUA), "TOCK 33 Glow does not lead TOCK 33 Aqua"


def test_newest_sort_orders_products_by_publication_newest_first(anon_client, db):
    """The newest sort lists products in falling publication time.

    cov: C-CF-207, C-DM-27
    """
    handles = handles_of(collection_json(anon_client, "all", {"sort": "newest"}).get("products", []))
    stamps = [db.product(h)["published_at"] for h in handles]
    assert all(a >= b for a, b in zip(stamps, stamps[1:])), f"newest order is not by publication: {list(zip(handles, stamps))}"
    featured = handles_of(collection_json(anon_client, "all", {"sort": "featured"}).get("products", []))
    positions = [db.product(h)["position"] for h in featured]
    assert positions == sorted(positions), f"featured order is not by position: {list(zip(featured, positions))}"


def test_every_compare_at_price_greater_than_its_price(anon_client):
    """Every compare-at price across the catalogue is above the product price.

    cov: C-CF-208
    """
    products = collection_json(anon_client, "all").get("products", [])
    discounted = [p for p in products if p.get("compare_at_price") is not None]
    assert discounted, "no product carries a compare-at price"
    bad = [(p["handle"], p["price"], p["compare_at_price"]) for p in discounted if int(p["compare_at_price"]) <= int(p["price"])]
    assert not bad, f"compare-at prices at or under the price: {bad}"


def test_published_reviews_list_newest_first(fresh_customer, second_fresh_customer, owner_client, anon_client):
    """The later published review lists before the earlier one.

    cov: C-CF-210
    """
    _, first_author = fresh_customer
    _, second_author = second_fresh_customer
    earlier = pending_review(first_author, RUBBER_NAVY)
    later = pending_review(second_author, RUBBER_NAVY)
    ok_json(owner_client.post(f"/owner/reviews/{earlier['id']}/publish", json={}), "publishing the earlier review")
    settle(1.1)
    ok_json(owner_client.post(f"/owner/reviews/{later['id']}/publish", json={}), "publishing the later review")
    ids = [r.get("id") for r in public_reviews(anon_client, RUBBER_NAVY)]
    assert ids.index(later["id"]) < ids.index(earlier["id"]), f"reviews are not newest first: {ids}"


def test_cart_follows_visitor_across_pages_surviving_signing_in(page, owner_client):
    """A line added before signing in shows on another page and stays after sign-in.

    cov: C-CF-211
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    ui_add_to_cart(page, NATO_AQUA)
    visit(page, "/pages/about")
    assert "(1)" in main_text(page), "the header cart count does not follow the visitor to the about page"
    ui_sign_in(page, CUSTOMER2_EMAIL, return_to="/cart")
    page.wait_for_url(re.compile(r"/cart"))
    assert "NATO Strap Aqua" in main_text(page), "the cart lost its line when the visitor signed in"


def test_held_reservation_expires_thirty_minutes_after_cart_last_activity(anon_client, carts, db):
    """A held reservation expires 1800 seconds after the cart's last activity.

    cov: C-CF-212
    """
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    cart = db.cart(token)
    held = [r for r in db.cart_reservations(cart["id"]) if r.get("status") == "held"]
    assert held, "the add wrote no held reservation"
    gap = (held[0]["expires_at"] - cart["last_activity_at"]).total_seconds()
    assert abs(gap - 1800) <= 5, f"the hold expires {gap} seconds after the last activity, expected 1800"


def test_owner_review_queue_shows_reviews_waiting_with_publish_reject_reply_controls(page, fresh_customer):
    """The owner queue heading is Reviews waiting and a pending row offers Publish, Reject and Reply.

    cov: C-CF-214
    """
    _, author = fresh_customer
    review = pending_review(author, WOVEN_SAND)
    ui_sign_in(page, OWNER_EMAIL, return_to="/owner/reviews")
    page.wait_for_url(re.compile(r"/owner/reviews"))
    expect(page.get_by_text("Reviews waiting").first).to_be_visible()
    row = smallest_container(page, [review["title"], "Publish", "Reject", "Reply"])
    assert row is not None, f"the queue row for {review['title']!r} lacks Publish, Reject or Reply"
    controls = row.evaluate("e => Array.from(e.querySelectorAll('button, a, [role=button]')).map(c => (c.innerText || '').trim())")
    for name in ("Publish", "Reject", "Reply"):
        assert name in controls, f"the queue row carries controls {controls}, missing {name}"


def test_owner_reviews_endpoint_filtered_by_status_returns_reviews_in_that_status(owner_client, fresh_customer):
    """GET /api/owner/reviews?status= returns only reviews in that status.

    cov: C-CF-215
    """
    _, author = fresh_customer
    review = pending_review(author, WOVEN_SAND)
    pending = ok_json(owner_client.get("/owner/reviews", params={"status": "pending"}), "owner reviews pending")
    assert review["id"] in [r.get("id") for r in pending], "the new pending review is not listed as pending"
    assert all(r.get("status") == "pending" for r in pending), "status=pending returned other statuses"
    published = ok_json(owner_client.get("/owner/reviews", params={"status": "published"}), "owner reviews published")
    assert published and all(r.get("status") == "published" for r in published), "status=published returned other statuses"


def test_at_phone_width_hero_stacks_dial_below_copy(narrow_page):
    """At 390px the hero dial sits below the headline.

    cov: C-UX-28
    """
    visit(narrow_page, "/")
    heading = narrow_page.locator("h1").first.bounding_box()
    hero = dial(narrow_page, "hero").bounding_box()
    assert heading and hero and hero["y"] >= heading["y"] + heading["height"] - 1, (
        f"the hero dial at {hero} does not sit below the headline at {heading}")


def test_at_phone_width_header_centres_wordmark(narrow_page):
    """At 390px the header wordmark sits in the middle of the bar.

    cov: C-UX-29
    """
    visit(narrow_page, "/")
    offset = narrow_page.evaluate(WORDMARK_OFFSET_JS)
    assert offset is not None and offset <= 24, f"the header wordmark sits {offset}px off centre"


def test_at_small_phone_width_timer_setter_chips_wrap_to_two_rows(narrow_page):
    """At 390px the four tock chips sit on two rows.

    cov: C-FE-15
    """
    visit(narrow_page, "/")
    rows = narrow_page.evaluate(SETTER_ROWS_JS)
    assert rows == 2, f"the tock chips sit on {rows} rows at 390px"


def test_at_phone_width_cart_shows_stacked_cards_per_line(narrow_page, owner_client):
    """At 390px the cart shows its line as a card with no visible table column header.

    cov: C-FE-16
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    ui_add_to_cart(narrow_page, NATO_AQUA)
    visit(narrow_page, "/cart")
    assert "NATO Strap Aqua" in main_text(narrow_page), "the phone cart does not show its line"
    headers = visible_named(narrow_page, "th, [role=columnheader]", r"^Quantity$")
    assert headers == 0, "the phone cart still shows a table with a Quantity column header"


def test_at_phone_width_sticky_action_bar_never_covers_end_of_product_page(narrow_page):
    """At 390px the end of the product page stays above any sticky action bar.

    cov: C-FE-17
    """
    visit(narrow_page, f"/products/{AQUA}")
    verdict = narrow_page.evaluate(STICKY_BAR_JS)
    assert verdict == "clear", f"the sticky action bar covers the end of the page: {verdict}"


def test_at_phone_width_footer_groups_fold_into_accordions(narrow_page):
    """At 390px the Main menu footer group is a collapsed toggle that opens.

    cov: C-FE-18
    """
    visit(narrow_page, "/")
    toggle = narrow_page.locator("button, summary, [role=button]").filter(has_text=re.compile(r"^\s*Main menu\s*$")).first
    expect(toggle).to_be_visible()
    state = ("e => e.getAttribute('aria-expanded') || (e.closest('details') && e.closest('details').open ? 'true' : 'false')")
    assert toggle.evaluate(state) == "false", "the Main menu footer group is open before it is toggled"
    toggle.click()
    assert toggle.evaluate(state) == "true", "the Main menu footer group did not open"


def test_at_400_percent_zoom_home_page_reflows_to_one_column_without_sideways_scrolling(browser):
    """At a 320px wide viewport the home page stacks and never scrolls sideways.

    cov: C-FE-19
    """
    context, surface = _surface(browser, viewport={"width": 320, "height": 568})
    visit(surface, "/")
    overflow = surface.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
    heading = surface.locator("h1").first.bounding_box()
    hero = dial(surface, "hero").bounding_box()
    context.close()
    assert overflow <= 1, f"the home page scrolls sideways by {overflow}px at 320px"
    assert heading and hero and hero["y"] >= heading["y"] + heading["height"] - 1, "the hero keeps two columns at 320px"


def test_cart_drawer_keeps_focus_inside_when_open_with_page_behind_held_still(page):
    """Tabbing stays inside the open drawer and the page behind does not scroll.

    cov: C-FE-20
    """
    visit(page, "/")
    cart_control(page).click()
    drawer = page.get_by_role("dialog").first
    expect(drawer).to_be_visible()
    for step in range(15):
        page.keyboard.press("Tab")
        assert drawer.evaluate("d => d.contains(document.activeElement)"), f"Tab {step + 1} left the open drawer"
    before = page.evaluate("() => window.scrollY")
    page.mouse.move(40, 450)
    page.mouse.wheel(0, 900)
    settle(0.6)
    assert page.evaluate("() => window.scrollY") == before, "the page behind the open drawer scrolled"


def test_footer_carries_main_menu_group_with_more_links_group(anon_client):
    """The footer carries Main menu and More Links with their links.

    cov: C-FE-22
    """
    text = lowered_text("/")
    for copy in HOME_COPY["footer_groups"]:
        assert copy.lower() in text, f"the footer lacks {copy!r}"


def test_footer_cards_read_watch_faqs_with_need_help_lines():
    """The footer cards read Watch FAQs and Need Help? over their lines.

    cov: C-FE-23
    """
    text = lowered_text("/")
    for copy in HOME_COPY["footer_cards"]:
        assert copy.lower() in text, f"the footer cards lack {copy!r}"


def test_drawer_enters_on_slide_in_keyframes_leaving_on_slide_back_out(page):
    """Opening the drawer runs slide-in and closing it runs slide-back-out.

    cov: C-FE-24
    """
    page.add_init_script(KEYFRAME_WATCH_JS)
    visit(page, "/")
    cart_control(page).click()
    drawer = page.get_by_role("dialog").first
    expect(drawer).to_be_visible()
    page.keyboard.press("Escape")
    expect(drawer).to_be_hidden()
    names = page.evaluate("() => window.__probeKeyframes")
    assert "slide-in" in names and "slide-back-out" in names, f"the drawer ran keyframes {names}"


def test_above_fold_home_headings_fade_up_on_herofade_keyframes(page):
    """The home page runs heroFade as its first screen arrives.

    cov: C-FE-25
    """
    page.add_init_script(KEYFRAME_WATCH_JS)
    visit(page, "/")
    settle(1.5)
    names = page.evaluate("() => window.__probeKeyframes")
    assert "heroFade" in names, f"the home page ran keyframes {names}"


def test_jost_with_cabin_load_under_swap_font_display_policy(page):
    """The Jost and Cabin font faces load with font-display swap.

    cov: C-FE-26
    """
    visit(page, "/")
    faces = page.evaluate("async () => { await document.fonts.ready;"
                          " return Array.from(document.fonts).map(f => [f.family.replace(/[\"']/g, ''), f.display]); }")
    for family in ("Jost", "Cabin"):
        assert any(name == family and display == "swap" for name, display in faces), (
            f"{family} has no swap font face: {faces}")


def test_timer_setter_card_carries_label_readout_run_a_tock_with_fast_demo():
    """The setter card carries its label, readout, Run a tock and fast demo.

    cov: C-FE-27
    """
    text = lowered_text("/")
    for copy in HOME_COPY["setter"]:
        assert copy.lower() in text, f"the timer setter card lacks {copy!r}"


def test_hero_carries_eyebrow_lede_four_specification_chips():
    """The hero carries its eyebrow, lede and four chips.

    cov: C-FE-28
    """
    text = lowered_text("/")
    for copy in HOME_COPY["hero"]:
        assert copy.lower() in text, f"the hero lacks {copy!r}"


def test_two_range_sections_carry_their_headings_with_their_lines():
    """The TOCK 33 and TOCK 38 ranges carry their headings and lines.

    cov: C-FE-29
    """
    text = lowered_text("/")
    for copy in HOME_COPY["ranges"]:
        assert copy.lower() in text, f"the range sections lack {copy!r}"


def test_comparison_carries_eyebrow_lede_two_card_texts():
    """The comparison carries its eyebrow, lede and both card texts.

    cov: C-FE-30
    """
    text = lowered_text("/")
    for copy in HOME_COPY["comparison"]:
        assert copy.lower() in text, f"the comparison lacks {copy!r}"


def test_founder_proof_carries_kicker_pull_quote_body_close():
    """The founder proof carries its kicker, pull quote, body and close.

    cov: C-FE-31
    """
    text = lowered_text("/")
    for copy in HOME_COPY["founder"]:
        assert copy.lower() in text, f"the founder proof lacks {copy!r}"


def test_duration_walkthrough_carries_overlay_three_stage_captions_footnote(page):
    """The walkthrough carries its overlay, three captions and footnote.

    cov: C-FE-32, C-CF-260, C-CF-261
    """
    text = lowered_text("/")
    for copy in HOME_COPY["walkthrough"]:
        assert copy.lower() in text, f"the walkthrough lacks {copy!r}"
    raw = html_text("/")[1]
    for caption in ("Set", "Halfway", "Done"):
        assert re.search(rf"\b{caption}\b", raw), f"the walkthrough stage caption {caption!r} is missing"
    visit(page, "/")
    stages = page.locator("[data-dial='stage']")
    expect(stages).to_have_count(3)
    running = [stages.nth(i).evaluate("e => getComputedStyle(e).animationName") for i in range(3)]
    assert all(name in ("none", "") for name in running), f"the walkthrough stage dials animate: {running}"
    places = [raw.find(caption) for caption in ("Set", "Halfway", "Done")]
    assert places == sorted(places), f"the stage captions do not read Set, Halfway, Done in order: {places}"


def test_testimonials_carry_eyebrow_heading_lede_six_attributed_quotes():
    """The testimonials carry their eyebrow, heading, lede and six attributed quotes.

    cov: C-FE-33
    """
    text = lowered_text("/")
    for copy in HOME_COPY["testimonials"]:
        assert copy.lower() in text, f"the testimonials lack {copy!r}"


def test_construction_section_carries_eyebrow_heading_lede_four_card_bodies():
    """The construction section carries its eyebrow, heading, lede and card bodies.

    cov: C-FE-34
    """
    text = lowered_text("/")
    for copy in HOME_COPY["construction"]:
        assert copy.lower() in text, f"the construction section lacks {copy!r}"


def test_product_pages_carry_materials_care_size_fit_shipping_returns_customer_reviews_blocks():
    """A watch page carries the four blocks and the size and fit text.

    cov: C-FE-35
    """
    text = lowered_text(f"/products/{AQUA}")
    for copy in PRODUCT_COPY:
        assert copy.lower() in text, f"the product page lacks {copy!r}"


def test_cart_page_carries_your_cart_three_columns_subtotal_trust_rows(page, owner_client):
    """The cart page carries its heading, columns, subtotal and trust rows.

    cov: C-FE-36
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    ui_add_to_cart(page, NATO_AQUA)
    visit(page, "/cart")
    text = main_text(page).lower()
    for copy in CART_COPY:
        assert copy.lower() in text, f"the cart page lacks {copy!r}"


def test_checkout_carries_seven_address_fields_summary_place_order(page, owner_client):
    """The checkout carries its seven labelled fields, the summary and Place order.

    cov: C-FE-37
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    ui_add_to_cart(page, NATO_AQUA)
    ui_sign_in(page, CUSTOMER_EMAIL, return_to="/checkout")
    page.wait_for_url(re.compile(r"/checkout"))
    for label in CHECKOUT_FIELDS:
        expect(page.get_by_label(label, exact=True).first).to_be_visible()
    text = main_text(page)
    for copy in ("Subtotal", "Shipping", "Total", "United States"):
        assert copy in text, f"the checkout lacks {copy!r}"
    expect(page.get_by_role("button", name="Place order").first).to_be_visible()


def test_account_page_carries_your_account_with_order_placed_status_total_columns(page):
    """The account page shows Your account and the four order columns.

    cov: C-FE-38
    """
    ui_sign_in(page, CUSTOMER2_EMAIL, return_to="/account")
    page.wait_for_url(re.compile(r"/account$"))
    expect(page.get_by_text("Your account").first).to_be_visible()
    for column in ("Order", "Placed", "Status", "Total"):
        expect(page.get_by_role("columnheader", name=column, exact=True).first).to_be_visible()


def test_sign_in_page_carries_link_form_password_form_create_account_link():
    """The sign-in page carries both forms and links Create an account to signup.

    cov: C-FE-39
    """
    status, text = html_text("/account/login")
    assert status == 200, f"GET /account/login returned {status}"
    for copy in ("Sign in", "Email me a sign-in link", "Send link", "Password", "Create an account"):
        assert copy in text, f"the sign-in page lacks {copy!r}"
    assert "/account/signup" in internal_hrefs(page_html("/account/login").text), "Create an account does not link signup"


def test_faq_battery_answer_with_user_guide_closing_step_carry_pinned_text():
    """The FAQ battery answer and the guide's closing step read as pinned.

    cov: C-FE-40
    """
    assert FAQ_BATTERY_ANSWER in html_text("/pages/faq")[1], "the FAQ battery answer differs"
    assert GUIDE_CLOSING_STEP in html_text("/pages/user-guide")[1], "the user guide closing step differs"


def test_each_range_rail_is_keyboard_focusable_scroll_region(page):
    """The TOCK 33 range rail sits in a scroll region that takes keyboard focus.

    cov: C-FE-41
    """
    visit(page, "/")
    verdict = page.evaluate(RAIL_REGION_JS, [["TOCK 33 Aqua", "TOCK 33 Navy", "TOCK 33 Fuchsia", "TOCK 33 Glow"]])
    assert verdict == "ok", f"the TOCK 33 range rail: {verdict}"


def test_collection_grid_shows_one_or_two_columns_on_small_phone(page, anon_client):
    """At 360px the Shop All grid shows one or two columns.

    cov: C-FE-12
    """
    titles = all_titles(anon_client)
    page.set_viewport_size({"width": 360, "height": 800})
    visit(page, "/collections/all")
    columns = page.evaluate(GRID_COLUMN_COUNT_JS, [titles])
    assert 1 <= columns <= 2, f"the phone grid shows {columns} columns"


def test_stored_timestamps_are_in_utc(db):
    """A new account's created_at matches the current UTC time.

    cov: C-TR-08
    """
    email, _ = signup()
    created = db.account(email)["created_at"]
    now = utc_now()
    if created.tzinfo is None:
        now = now.replace(tzinfo=None)
    drift = abs((now - created).total_seconds())
    assert drift < 900, f"created_at {created} is {drift} seconds away from UTC now"


def test_absolute_links_in_sitemap_robots_file_sign_in_email_use_app_public_url(inbox):
    """Sitemap locations, the robots Sitemap line and the sign-in link all start with APP_PUBLIC_URL.

    cov: C-TR-09
    """
    locations = sitemap_locations()
    assert locations and all(loc.startswith(base_url()) for loc in locations), "sitemap locations ignore APP_PUBLIC_URL"
    assert f"Sitemap: {base_url()}/sitemap.xml" in page_html("/robots.txt").text, "robots.txt ignores APP_PUBLIC_URL"
    email = unique_email()
    request_link(email)
    message = poll_until(lambda: inbox.find(to=email, subject_contains=SIGN_IN_SUBJECT))
    assert message is not None and f"{base_url()}{LINK_MARKER}" in message.body, "the sign-in link ignores APP_PUBLIC_URL"


def test_production_server_answers_rather_than_development_server():
    """The app answers from a production server, never the Werkzeug development server.

    cov: C-DC-11
    """
    response = httpx.get(f"{api_url()}/health", timeout=30.0)
    assert "werkzeug" not in response.headers.get("server", "").lower(), (
        f"the development server answers: {response.headers.get('server')!r}")
    missing = page_html(f"/no-such-page-{os.urandom(3).hex()}")
    assert "werkzeug debugger" not in missing.text.lower(), "the development debugger is exposed"


def test_seeded_products_carry_skus_prices_seed_ledger_units(db):
    """Every seeded sku carries its price and its seed ledger units.

    cov: C-DM-13
    """
    for sku, (price, units) in SEED_SKUS.items():
        variant = db.variant(sku)
        assert variant is not None and int(variant["price"]) == price, f"{sku} reads {variant}"
        if units is None:
            continue
        item = db.inventory(sku)
        seeded = sum(int(r["delta"]) for r in db.ledger_rows(item["id"]) if r.get("reason") == "seed")
        assert seeded == units, f"{sku} seed ledger units read {seeded}, expected {units}"


def test_seeded_units_leave_bundles_unavailable_low_stock_in_stock_at_seed_time(db):
    """The seed ledger units put the four bundles in their pinned seed-time states.

    cov: C-DM-14
    """
    def seeded(sku):
        return sum(int(r["delta"]) for r in db.ledger_rows(db.inventory(sku)["id"]) if r.get("reason") == "seed")

    for bundle, (big, small, expected) in SEED_BUNDLES.items():
        units = min(seeded(big), seeded(small))
        state = "unavailable" if units == 0 else ("low_stock" if units <= 3 else "in_stock")
        assert state == expected, f"{bundle} seeds {units} pairs, reading {state}, expected {expected}"


def test_imported_reviews_carry_authors_ratings_titles_verified_flags(db):
    """Each imported review row carries its author, rating, title and verified flag.

    cov: C-DM-15, C-DM-28
    """
    for handle, author, rating, title, verified in SEED_REVIEWS:
        row = db.seeded_review(db.product(handle)["id"], author)
        assert row is not None, f"no imported review by {author} on {handle}"
        assert (int(row["rating"]), row["title"], bool(row["verified_purchase"])) == (rating, title, verified), (
            f"the {author} review reads {row}")
    nora = db.seeded_review(db.product(GLOW33)["id"], "Nora")
    assert nora.get("mentions_minor") is True, "Nora's review does not mention a minor"
    for handle, author, *_ in SEED_REVIEWS:
        assert db.seeded_review(db.product(handle)["id"], author).get("account_id") is None, f"the {author} import carries an account"


def test_seeded_ratings_read_grey_4_5_from_2_with_glow_4_7_from_imported_reviews(anon_client, db):
    """TOCK 38 Grey reads 4.5 from 2 and the three imported Glow reviews average 4.7.

    cov: C-DM-16
    """
    grey = product_json(anon_client, GREY38)
    assert (grey.get("rating_average"), grey.get("review_count")) == (4.5, 2), f"TOCK 38 Grey reads {grey.get('rating_average')} from {grey.get('review_count')}"
    glow = [int(db.seeded_review(db.product(GLOW33)["id"], a)["rating"]) for a in ("Iris", "Ben", "Kofi")]
    assert round(sum(glow) / len(glow), 1) == 4.7, f"the imported Glow ratings {glow} do not average 4.7"


def test_product_published_only_with_active_or_discontinued_status_plus_published_at(db):
    """Published products are active or discontinued with a published_at, and the lilac draft is neither.

    cov: C-DM-17
    """
    for handle in PUBLISHED_HANDLES:
        row = db.product(handle)
        assert row["status"] in ("active", "discontinued") and row["published_at"] is not None, f"{handle} reads {row}"
    assert db.product(MINT31)["status"] == "discontinued", "TOCK 31 Mint is not discontinued"
    assert db.product(LILAC_DRAFT)["status"] == "draft", "TOCK 33 Lilac is not a draft"


def test_stock_ledger_rows_only_ever_added(owner_client, db):
    """Two adjustments append two ledger rows and leave the earlier rows untouched.

    cov: C-DM-18
    """
    item = db.inventory(SKU_RUBBER_NAVY_S)
    before = db.ledger_rows(item["id"])
    ok_json(adjust(owner_client, SKU_RUBBER_NAVY_S, 1, "probe add"), "a +1 adjustment")
    ok_json(adjust(owner_client, SKU_RUBBER_NAVY_S, -1, "probe remove"), "a -1 adjustment")
    after = db.ledger_rows(item["id"])
    assert len(after) == len(before) + 2, f"the ledger moved from {len(before)} to {len(after)} rows"
    assert after[:len(before)] == before, "an earlier ledger row changed"


def test_storefront_offers_no_market_country_or_currency_selector(page):
    """Home and a product page carry no market, country or currency selector.

    cov: C-CN-06
    """
    for path in ("/", f"/products/{AQUA}"):
        visit(page, path)
        found = visible_named(page, "select, [role=combobox], [role=listbox]", r"[Cc]ountry|[Cc]urrency|[Mm]arket|USD|EUR|GBP")
        assert found == 0, f"{path} offers a market, country or currency selector"


def test_every_catalogue_price_in_usd(anon_client):
    """Every catalogue product and the product endpoint price in usd.

    cov: C-CN-07
    """
    products = collection_json(anon_client, "all").get("products", [])
    assert all(p.get("currency") == "usd" for p in products), "a catalogue product prices in another currency"
    assert product_json(anon_client, AQUA).get("currency") == "usd", "the product endpoint prices in another currency"


def test_home_page_offers_no_newsletter_signup():
    """The home page carries no email capture for a newsletter.

    cov: C-CN-08
    """
    markup = page_html("/").text
    assert not re.search(r"""type\s*=\s*["']email["']""", markup, re.I), "the home page carries an email input"
    assert not re.search(r"newsletter|subscribe", normalise_text(TAG_RE.sub(" ", markup)), re.I), (
        "the home page invites a newsletter subscription")
    for path in PUBLIC_ROUTES:
        text = html_text(path)[1]
        assert not re.search(r"newsletter|subscribe to our", text, re.I), f"{path} invites a newsletter subscription"


def test_product_pages_carry_no_recently_viewed_rail_or_product_structured_data():
    """A watch page carries no recently viewed rail and no product structured data.

    cov: C-CN-09, C-CN-10
    """
    markup = page_html(f"/products/{AQUA}").text
    assert "recently viewed" not in normalise_text(TAG_RE.sub(" ", SCRIPT_RE.sub(" ", markup))).lower(), (
        "the product page carries a recently viewed rail")
    blocks = re.findall(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", markup, re.S | re.I)
    assert not any('"product"' in b.lower() for b in blocks), "the product page carries product structured data"


def test_review_dialog_with_contact_form_offer_no_file_upload(page):
    """The contact form and the Write a review dialog carry no file input.

    cov: C-CN-12, C-CF-258
    """
    assert not re.search(r"""type\s*=\s*["']file["']""", page_html("/pages/contact-us").text, re.I), (
        "the contact form offers a file upload")
    ui_sign_in(page, CUSTOMER_EMAIL, return_to=f"/products/{GREY38}")
    page.wait_for_url(re.compile(rf"/products/{GREY38}"))
    page.get_by_role("button", name="Write a review").first.click()
    dialog = page.get_by_role("dialog").first
    expect(dialog).to_be_visible()
    assert dialog.locator("input[type=file]").count() == 0, "the review dialog offers a file upload"
    page.keyboard.press("Escape")
    expect(dialog).to_be_hidden()
    assert page.get_by_role("button", name="Write a review").first.evaluate("e => e === document.activeElement"), (
        "focus did not return to Write a review")
    for path in PUBLIC_ROUTES:
        assert not re.search(r"""type\s*=\s*["']file["']""", page_html(path).text, re.I), f"{path} offers a file upload"


def test_order_page_offers_no_refund_action(page):
    """The seeded order page shows the order with no refund control.

    cov: C-CN-13, C-CN-15
    """
    ui_sign_in(page, CUSTOMER2_EMAIL, return_to="/orders/TK-SEEDED01")
    page.wait_for_url(re.compile(r"/orders/TK-SEEDED01"))
    expect(page.get_by_text("TK-SEEDED01").first).to_be_visible()
    assert visible_named(page, "button, a, [role=button]", r"[Rr]efund") == 0, "the order page offers a refund action"
    others = visible_named(page, "button, a, [role=button]", r"[Ww]arranty claim|[Rr]eturn request|[Ss]tart a return|[Tt]rack (my )?(order|package|shipment)")
    assert others == 0, "the order page offers a warranty claim, return request or tracking control"

def test_signup_with_letter_case_variant_of_registered_email_rejected(anon_client, db):
    """A signup with the upper-case form of a registered email is rejected and writes nothing.

    cov: C-CF-216
    """
    email, _ = signup()
    response = anon_client.post("/auth/signup", json={"email": email.upper(), "password": "another-pass-2026",
                                                      "name": "Probe Case"})
    expect_client_error(response, f"POST /api/auth/signup for {email.upper()}")
    assert db.count_accounts(email) + db.count_accounts(email.upper()) == 1, "a letter-case variant wrote a second account"


def test_hero_price_beside_shop_tock_33_follows_from_price_rule_without_cents(owner_client):
    """The hero price beside Shop TOCK 33 reads $189 with no cents while Aqua is in stock.

    cov: C-CF-217
    """
    ensure_available(owner_client, SKU_AQUA, 4)
    _, text = html_text("/")
    at = text.find("Shop TOCK 33")
    assert at >= 0, "the hero carries no Shop TOCK 33 action"
    nearby = text[max(0, at - 60):at + 80]
    assert re.search(r"\$189(?![.\d])", nearby), f"the hero price beside Shop TOCK 33 reads {nearby!r}"


def test_comparison_stacks_on_phones_with_slider_between_dials(narrow_page):
    """At 390px the conventional dial, the slider and the Tock dial stack in that order.

    cov: C-UX-14
    """
    visit(narrow_page, "/")
    plain = dial(narrow_page, "plain").bounding_box()
    slider = comparison_slider(narrow_page).bounding_box()
    zoned = dial(narrow_page, "zoned").bounding_box()
    assert plain and slider and zoned, "the comparison dials or slider are not rendered at 390px"
    assert plain["y"] + plain["height"] <= slider["y"] + 1 and slider["y"] + slider["height"] <= zoned["y"] + 1, (
        f"the comparison does not stack plain {plain}, slider {slider}, zoned {zoned}")


def test_in_progress_action_shows_primary_blue_beside_moving_indicator(page, owner_client):
    """While Add to Cart is in flight a moving indicator runs beside the primary blue.

    cov: C-UX-27
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    visit(page, f"/products/{NATO_AQUA}")
    page.evaluate(PROGRESS_WATCH_JS)
    page.route("**/*", lambda route: (settle(1.5) if route.request.method == "POST" else None, route.continue_()))
    page.get_by_role("button", name="Add to Cart", exact=True).first.click()
    page.wait_for_function("() => window.__probeProgress && window.__probeProgress.pending === false", timeout=UI_TIMEOUT_MS)
    progress = page.evaluate("() => window.__probeProgress")
    primary = page.evaluate("() => window.__probePrimary")
    assert progress["moving"], "no moving indicator ran while the add was in progress"
    assert progress.get("busy") == primary or primary in progress["colours"], (
        f"the in-progress state does not wear the primary blue {primary}")


def test_pointing_at_cart_control_grows_faint_wash_behind_icon(page):
    """Hovering the header cart control changes a background layer behind its icon.

    cov: C-UX-31
    """
    visit(page, "/")
    control = cart_control(page)
    page.mouse.move(5, 600)
    before = control.evaluate(STYLE_SNAPSHOT_JS)
    control.hover()
    settle(0.8)
    after = control.evaluate(STYLE_SNAPSHOT_JS)
    assert before != after, "pointing at the cart control changes nothing behind the icon"


def test_tock_chips_with_colourway_swatches_change_appearance_under_pointer(page):
    """Hovering an unselected tock chip and an unpressed swatch changes how each looks.

    cov: C-UX-32
    """
    visit(page, "/")
    for target in (page.get_by_text("5 min", exact=True).first, swatch(page, "Navy")):
        page.mouse.move(5, 600)
        settle(0.5)
        before = target.evaluate(STYLE_SNAPSHOT_JS)
        target.hover()
        settle(0.8)
        after = target.evaluate(STYLE_SNAPSHOT_JS)
        assert before != after, f"{target} shows no pointed-at state"


def test_keyboard_navigation_reaches_header_controls_in_visual_order(page):
    """Tabbing after the skip link walks the header controls from left to right.

    cov: C-UX-33
    """
    visit(page, "/")
    stops = []
    for _ in range(20):
        page.keyboard.press("Tab")
        stop = page.evaluate(TAB_STOPS_JS)
        if stop is None or stop["text"] == "Skip to content":
            continue
        if stop["top"] > 160:
            break
        stops.append(stop)
    xs = [s["x"] for s in stops]
    assert len(stops) >= 8, f"the header offers {len(stops)} keyboard stops: {[s['text'] for s in stops]}"
    assert xs == sorted(xs), f"header focus order leaves visual order: {[(s['text'], round(s['x'])) for s in stops]}"


def test_colourway_swatches_with_tock_chips_meet_24_pixel_target_size(page):
    """Every swatch and tock chip measures at least 24 by 24 pixels.

    cov: C-UX-34
    """
    visit(page, "/")
    sizes = page.evaluate(TARGET_SIZES_JS, ["Aqua", "Navy", "Fuchsia", "Glow", "5 min", "10 min", "15 min", "30 min"])
    small = [(n, w, h) for n, w, h in sizes if w < 24 or h < 24]
    assert not small, f"targets under 24 by 24 pixels: {small}"


def test_loading_same_product_page_twice_draws_same_product_image():
    """Two loads of a product page draw identical product images.

    cov: C-FE-42
    """
    first = product_image_markup(f"/products/{AQUA}")
    second = product_image_markup(f"/products/{AQUA}")
    assert first, "the product page draws no image"
    assert first == second, "the product image changes between loads"


def test_tock_33_range_rail_shows_1_5_2_3_4_cards_from_small_phone_to_desktop(browser):
    """The TOCK 33 rail fits about 1.5, 2, 3 and 4 cards at 390, 600, 900 and 1280 pixels.

    cov: C-FE-43
    """
    titles = [["TOCK 33 Aqua", "TOCK 33 Navy", "TOCK 33 Fuchsia", "TOCK 33 Glow"]]
    readings = []
    for width, expected in ((390, 1.5), (600, 2), (900, 3), (1280, 4)):
        context, surface = wide_surface(browser, {"width": width, "height": 900})
        visit(surface, "/")
        ratio = surface.evaluate(RAIL_CARDS_JS, titles)
        context.close()
        readings.append((width, expected, ratio))
    wrong = [(w, e, r) for w, e, r in readings if r is None or abs(r - e) > 0.4]
    assert not wrong, f"rail cards per width (width, expected, seen): {wrong}"


def test_from_tablet_width_header_shows_full_link_row(browser):
    """At 900px the five header links show without opening a menu.

    cov: C-FE-44
    """
    context, surface = wide_surface(browser, TABLET_VIEWPORT)
    visit(surface, "/")
    missing = [n for n in NAV_LINKS
               if visible_named(surface, "a", rf"^{re.escape(n)}$") == 0]
    context.close()
    assert not missing, f"at 900px the header hides {missing}"


def test_from_tablet_width_hero_sets_dial_right_of_copy(browser):
    """At 900px the hero dial sits to the right of the headline.

    cov: C-FE-45
    """
    context, surface = wide_surface(browser, TABLET_VIEWPORT)
    visit(surface, "/")
    heading = surface.locator("h1").first.bounding_box()
    hero = dial(surface, "hero").bounding_box()
    context.close()
    assert heading and hero and hero["x"] >= heading["x"] + heading["width"] * 0.5 and hero["y"] < heading["y"] + 400, (
        f"at 900px the hero dial {hero} is not right of the copy {heading}")


def test_from_tablet_width_comparison_sets_two_dials_side_by_side(browser):
    """At 900px the conventional and Tock dials share a row.

    cov: C-FE-46
    """
    context, surface = wide_surface(browser, TABLET_VIEWPORT)
    visit(surface, "/")
    plain = dial(surface, "plain").bounding_box()
    zoned = dial(surface, "zoned").bounding_box()
    context.close()
    assert plain and zoned and abs(plain["y"] - zoned["y"]) <= 40 and zoned["x"] > plain["x"], (
        f"at 900px the comparison dials are not side by side: {plain} {zoned}")


def test_on_phones_walkthrough_stacks_its_three_stage_dials(narrow_page):
    """At 390px the three stage dials stack top to bottom.

    cov: C-FE-47
    """
    visit(narrow_page, "/")
    stages = narrow_page.locator("[data-dial='stage']")
    boxes = [stages.nth(i).bounding_box() for i in range(3)]
    assert all(boxes) and boxes[0]["y"] < boxes[1]["y"] < boxes[2]["y"], f"stage dials at 390px: {boxes}"


def test_from_tablet_width_walkthrough_sets_its_three_stage_dials_across(browser):
    """At 900px the three stage dials share a row left to right.

    cov: C-FE-48
    """
    context, surface = wide_surface(browser, TABLET_VIEWPORT)
    visit(surface, "/")
    stages = surface.locator("[data-dial='stage']")
    boxes = [stages.nth(i).bounding_box() for i in range(3)]
    context.close()
    assert all(boxes) and max(b["y"] for b in boxes) - min(b["y"] for b in boxes) <= 40, f"stage dials at 900px: {boxes}"
    assert boxes[0]["x"] < boxes[1]["x"] < boxes[2]["x"], f"stage dials at 900px are not across: {boxes}"


def test_from_tablet_width_buy_box_sits_beside_product_media(browser):
    """At 900px the Add to Cart control sits to the right of the image carousel.

    cov: C-FE-49
    """
    context, surface = wide_surface(browser, TABLET_VIEWPORT)
    visit(surface, f"/products/{AQUA}")
    media = surface.get_by_role("group").filter(has_text="1 of 4").first.bounding_box()
    button = surface.get_by_role("button", name="Add to Cart", exact=True).first.bounding_box()
    context.close()
    assert media and button and button["x"] >= media["x"] + media["width"] - 1, (
        f"at 900px the buy box {button} is not beside the media {media}")


def test_at_tablet_width_collection_grid_shows_three_columns(browser, anon_client):
    """At 900px the Shop All grid shows three columns.

    cov: C-FE-50
    """
    titles = all_titles(anon_client)
    context, surface = wide_surface(browser, TABLET_VIEWPORT)
    visit(surface, "/collections/all")
    columns = surface.evaluate(GRID_COLUMN_COUNT_JS, [titles])
    context.close()
    assert columns == 3, f"at 900px the grid shows {columns} columns"


def test_storefront_sends_no_marketing_email(fresh_customer, anon_client, owner_client, inbox):
    """Signing up, subscribing to a restock and contacting support send no marketing mail.

    cov: C-CN-16
    """
    email, _ = fresh_customer
    set_available(owner_client, SKU_NATO_NAVY, 0)
    anon_client.post(f"/products/{NATO_NAVY}/restock-subscriptions", json={"email": email})
    anon_client.post("/support-requests", json={"name": "Probe", "email": email, "subject": "Press", "message": "Hi"})
    settle(3.0)
    marketing = [s for s in mail_subjects(inbox, email) if MARKETING_SUBJECT_RE.search(s)]
    assert not marketing, f"the storefront sent marketing mail {marketing}"


def test_no_account_role_exists_besides_customer_with_owner(db):
    """Every account row carries the role customer or owner.

    cov: C-CN-17
    """
    roles = {row.get("role") for row in db.accounts()}
    assert roles <= {"customer", "owner"}, f"account roles include {sorted(roles - {'customer', 'owner'})}"


def test_product_with_collection_pages_play_no_video():
    """A product page and a collection page embed no video or player.

    cov: C-CN-18
    """
    for path in (f"/products/{AQUA}", "/collections/all"):
        markup = page_html(path).text
        assert not re.search(r"<video\b|youtube\.com|vimeo\.com", markup, re.I), f"{path} embeds video"

def test_public_product_collection_search_responses_state_no_unit_counts(anon_client):
    """Product, collection and search responses carry no unit count at any level.

    cov: C-CF-218
    """
    payloads = [product_json(anon_client, AQUA), product_json(anon_client, BUNDLE_GREY_AQUA),
                collection_json(anon_client, "all"), ok_json(anon_client.get("/search", params={"q": "tock"}), "search")]
    leaked = []

    def walk(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in UNIT_COUNT_KEYS:
                    leaked.append(f"{path}.{key}")
                walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{path}[{index}]")

    for index, payload in enumerate(payloads):
        walk(payload, f"response{index}")
    assert not leaked, f"public responses state unit counts at {leaked[:8]}"


def test_shipping_page_states_us_only_swiftpost_flat_15_complete_set_rule_two_year_warranty():
    """The shipping page states US-only Swiftpost shipping in two days for $15, the complete-set rule and the warranty.

    cov: C-CF-221, C-CF-222, C-CF-223
    """
    _, text = html_text("/pages/shipping-and-returns")
    lowered = text.lower()
    assert "united states" in lowered and "swiftpost" in lowered and "$15" in text, "the shipping terms are incomplete"
    assert re.search(r"\b(two|2)[- ]day", lowered), "the shipping page does not state two day delivery"
    assert re.search(r"complete", lowered) and re.search(r"bundle|set", lowered), "the complete-set bundle rule is missing"
    assert re.search(r"\b(two|2)[- ]year warranty", lowered), "the shipping page does not state the two year warranty"


def test_owner_console_reject_asks_for_policy_clause(page, fresh_customer, db):
    """Rejecting from the owner queue asks for a Policy clause and leaves the review pending until one is given.

    cov: C-CF-224
    """
    _, author = fresh_customer
    review = pending_review(author, WOVEN_SAND, rating=2)
    ui_sign_in(page, OWNER_EMAIL, return_to="/owner/reviews")
    page.wait_for_url(re.compile(r"/owner/reviews"))
    row = smallest_container(page, [review["title"], "Reject"])
    assert row is not None, f"the queue shows no Reject control beside {review['title']!r}"
    row.query_selector("button:has-text('Reject'), a:has-text('Reject')").click()
    expect(page.get_by_text("Policy clause").first).to_be_visible()
    assert db.review(review["id"]).get("status") == "pending", "the review was rejected before a clause was chosen"


def test_owner_stock_row_takes_adjustment_through_adjust_by_reason_save_adjustment(page, owner_client):
    """An owner stock row adjusts on hand through Adjust by, Reason and Save adjustment.

    cov: C-CF-225
    """
    before = int(stock_row(owner_client, SKU_RUBBER_NAVY_S)["on_hand"])
    ui_sign_in(page, OWNER_EMAIL, return_to="/owner/stock")
    page.wait_for_url(re.compile(r"/owner/stock"))
    row = smallest_container(page, [SKU_RUBBER_NAVY_S, "Save adjustment"])
    assert row is not None, "the stock row for STRAP-RUBBER-NAVY-S offers no Save adjustment"
    fields = row.query_selector_all("input:not([type=hidden]), textarea")
    assert len(fields) >= 2, "the stock row lacks its Adjust by and Reason fields"
    try:
        fields[0].fill("1")
        fields[1].fill("probe console adjustment")
        row.query_selector("button:has-text('Save adjustment')").click()
        after = poll_until(lambda: int(stock_row(owner_client, SKU_RUBBER_NAVY_S)["on_hand"]) == before + 1)
        assert after, "saving the adjustment did not move on hand by one"
    finally:
        now = int(stock_row(owner_client, SKU_RUBBER_NAVY_S)["on_hand"])
        if now != before:
            adjust(owner_client, SKU_RUBBER_NAVY_S, before - now, "probe restore")


def test_watch_specification_values_follow_tock_33_tock_38_tock_31_families(anon_client):
    """TOCK 33 carries the pinned values; TOCK 38 differs in Case, Movement, Dial; TOCK 31 in Case.

    cov: C-CF-226, C-CF-227, C-CF-228
    """
    def specs(handle):
        return {s["key"]: s["value"] for s in product_json(anon_client, handle).get("specifications", [])}

    assert specs(AQUA) == TOCK33_SPECS, f"TOCK 33 Aqua specifications read {specs(AQUA)}"
    assert specs(GREY38) == dict(TOCK33_SPECS, **TOCK38_CHANGES), f"TOCK 38 Grey specifications read {specs(GREY38)}"
    assert specs(MINT31) == dict(TOCK33_SPECS, **TOCK31_CHANGES), f"TOCK 31 Mint specifications read {specs(MINT31)}"


def test_body_text_renders_at_14_25_px_on_phones_16_15_px_on_desktop_with_line_height_1_5(browser):
    """Body paragraphs render at 14.25px on phones and 16.15px on desktop, line height 1.5.

    cov: C-FE-55
    """
    for width, size in ((390, 14.25), (1280, 16.15)):
        context, surface = wide_surface(browser, {"width": width, "height": 900})
        visit(surface, "/pages/about")
        font, line = surface.locator("main p, p").first.evaluate(
            "e => [parseFloat(getComputedStyle(e).fontSize), parseFloat(getComputedStyle(e).lineHeight)]")
        context.close()
        assert abs(font - size) <= 0.3, f"at {width}px body text renders at {font}px, expected {size}px"
        assert abs(line / font - 1.5) <= 0.05, f"at {width}px body line height is {line / font:.2f}, expected 1.5"


def test_header_sticks_to_top_on_scroll(page):
    """After scrolling the header banner stays at the top of the viewport.

    cov: C-FE-56
    """
    visit(page, "/")
    page.mouse.wheel(0, 2400)
    settle(0.8)
    assert page.evaluate("() => window.scrollY") > 500, "the home page did not scroll"
    box = page.get_by_role("banner").first.bounding_box()
    assert box is not None and -1 <= box["y"] <= 60, f"the header sits at {box} after scrolling"


def test_collection_card_shows_title_price_or_sold_out_with_rating_summary(owner_client):
    """TOCK 33 cards show titles, a price, Sold out for Navy and Aqua's 4.1 rating.

    cov: C-CF-230
    """
    ensure_available(owner_client, SKU_AQUA, 1)
    set_available(owner_client, SKU_NAVY, 0)
    _, text = html_text("/collections/tock-33")
    for copy in ("TOCK 33 Aqua", "TOCK 33 Navy", "$189.00", "Sold out", "4.1"):
        assert copy in text, f"the TOCK 33 collection cards lack {copy!r}"


def test_product_carousel_is_labelled_group_with_previous_next_controls(page):
    """The watch carousel is a named group carrying previous and next controls.

    cov: C-CF-231
    """
    visit(page, f"/products/{AQUA}")
    group = page.get_by_role("group").filter(has_text="1 of 4").first
    expect(group).to_be_visible()
    label = group.evaluate(
        "e => { const id = e.getAttribute('aria-labelledby'); const byId = id ? document.getElementById(id) : null;"
        " return (e.getAttribute('aria-label') || (byId ? byId.textContent : '') || '').trim(); }")
    assert label, "the carousel group carries no accessible label"
    controls = group.evaluate("e => Array.from(e.querySelectorAll('button')).map(b => ((b.getAttribute('aria-label') || '') + ' ' + (b.innerText || '')).toLowerCase())")
    assert any("prev" in c for c in controls) and any("next" in c for c in controls), f"carousel controls read {controls}"


def test_refused_checkout_leaves_cart_holding_its_units(fresh_customer, anon_client, carts, owner_client):
    """A checkout refused for a missing postcode leaves the cart's hold in place.

    cov: C-CF-233
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 3)
    _, buyer = fresh_customer
    token = carts()
    added_cart(anon_client, token, SKU_NATO_AQUA, 1)
    reserved = int(stock_row(owner_client, SKU_NATO_AQUA)["reserved"])
    address = {k: v for k, v in us_address().items() if k != "postcode"}
    expect_client_error(checkout(buyer, token, unique_key(), address), "a checkout without a postcode")
    assert int(stock_row(owner_client, SKU_NATO_AQUA)["reserved"]) == reserved, "the refused checkout released the hold"
    assert line_for(ok_json(cart_get(anon_client, token), "GET /api/cart"), SKU_NATO_AQUA) is not None, "the cart lost its line"


def test_foreign_order_page_shows_not_found_page(page):
    """A signed-in customer opening another customer's order page gets the 404 page.

    cov: C-CF-235
    """
    ui_sign_in(page, CUSTOMER_EMAIL)
    response = visit(page, "/orders/TK-SEEDED01")
    assert response is not None and response.status == 404, f"the foreign order page answered {response and response.status}"


def test_dana_imported_review_carries_pinned_body_with_pinned_reply(db):
    """Dana's imported review and the owner's reply carry the pinned text.

    cov: C-DM-20
    """
    row = db.seeded_review(db.product(AQUA)["id"], "Dana")
    assert row is not None and normalise_text(row["body"]) == DANA_BODY, f"Dana's review body reads {row and row['body']!r}"
    reply = db.reply_for(row["id"])
    assert reply is not None and normalise_text(reply["body"]) == DANA_REPLY, f"the reply reads {reply and reply['body']!r}"

def test_six_collections_render_product_grids_titled_by_handle(anon_client):
    """Each of the six collections answers with its pinned title and renders a product grid.

    cov: C-CF-236
    """
    for handle, title in COLLECTION_TITLES.items():
        collection = collection_json(anon_client, handle)
        assert collection.get("title") == title, f"/api/collections/<handle> for {handle} is titled {collection.get('title')!r}"
        products = collection.get("products", [])
        assert products, f"the {handle} collection lists no products"
        status, text = html_text(f"/collections/{handle}")
        assert status == 200, f"/collections/{handle} answered {status}"
        assert products[0]["title"] in text, f"the {handle} grid does not show {products[0]['title']!r}"


def test_sized_strap_pages_offer_small_large_size_control_absent_elsewhere(page, owner_client):
    """The woven strap page offers Small with Large; watches, bundles, NATO straps and soft goods offer none.

    cov: C-CF-242, C-CF-243
    """
    ensure_available(owner_client, SKU_WOVEN_SAND_S, 2)
    visit(page, f"/products/{WOVEN_SAND}")
    for option in ("Small", "Large"):
        assert page.evaluate(SIZE_STATE_JS, option) != "removed", f"the woven strap page offers no {option} size"
    for handle in (AQUA, BUNDLE_GREY_AQUA, NATO_AQUA, TOTE):
        visit(page, f"/products/{handle}")
        states = [page.evaluate(SIZE_STATE_JS, option) for option in ("Small", "Large")]
        assert states == ["removed", "removed"], f"/products/{handle} shows a size control: {states}"


def test_bundle_page_links_each_component_watch_to_product_page():
    """The Black and Navy Bundle page links both component watches to their own pages.

    cov: C-CF-244
    """
    links = internal_hrefs(page_html(f"/products/{BUNDLE_BLACK_NAVY}").text)
    for handle in (BLACK38, NAVY):
        assert f"/products/{handle}" in links, f"the bundle page does not link /products/{handle}"


def test_rejected_review_neither_listed_nor_counted(fresh_customer, owner_client, anon_client):
    """A rejected review stays off the public list, leaving the count unchanged.

    cov: C-CF-245
    """
    _, author = fresh_customer
    before = product_json(anon_client, WOVEN_SAND).get("review_count")
    review = pending_review(author, WOVEN_SAND, rating=2)
    ok_json(owner_client.post(f"/owner/reviews/{review['id']}/reject", json={"policy_clause": "spam"}), "owner reject")
    titles = [r.get("title") for r in public_reviews(anon_client, WOVEN_SAND)]
    assert review["title"] not in titles, "the rejected review is listed publicly"
    assert product_json(anon_client, WOVEN_SAND).get("review_count") == before, "the rejected review moved the count"


def test_verified_review_shows_verified_purchase():
    """The aqua page marks its verified imported reviews Verified purchase.

    cov: C-CF-247
    """
    _, text = html_text(f"/products/{AQUA}")
    assert "Verified purchase" in text, "no review on the aqua page shows Verified purchase"


def test_line_add_patch_delete_calls_each_return_the_cart(anon_client, carts, owner_client):
    """Adding, patching and deleting a line each answer with the cart.

    cov: C-CF-251
    """
    ensure_available(owner_client, SKU_NATO_AQUA, 4)
    token = carts()
    added = ok_json(cart_add(anon_client, token, SKU_NATO_AQUA, 2), "POST /api/cart/lines")
    line = line_for(added, SKU_NATO_AQUA)
    patched = ok_json(cart_patch(anon_client, token, line["id"], 1), "PATCH /api/cart/lines/<id>")
    deleted = ok_json(cart_delete(anon_client, token, line["id"]), "DELETE /api/cart/lines/<id>")
    for name, payload in (("add", added), ("patch", patched), ("delete", deleted)):
        assert payload.get("token") == token and "lines" in payload, f"the {name} call did not answer the cart: {payload}"


def test_catalogue_cart_restock_support_policy_search_endpoints_answer_without_bearer_token(anon_client, owner_client):
    """The public endpoints answer with no bearer token on the request.

    cov: C-CF-257
    """
    set_available(owner_client, SKU_NATO_NAVY, 0)
    reads = [("/collections/all", None), (f"/products/{AQUA}", None), ("/search", {"q": "tock"}), ("/policies", None),
             (f"/products/{AQUA}/reviews", None)]
    for path, params in reads:
        assert anon_client.get(path, params=params).status_code == 200, f"GET /api{path} needs a token"
    token = new_cart(anon_client)
    assert cart_get(anon_client, token).status_code == 200, "GET /api/cart needs a token"
    ok_json(anon_client.post(f"/products/{NATO_NAVY}/restock-subscriptions", json={"email": unique_email()}), "restock")
    ok_json(anon_client.post("/support-requests", json={"name": "Probe", "email": unique_email(), "subject": "Press",
                                                         "message": "Hello"}), "support request")


def test_contact_page_support_form_carries_name_email_subject_message_fields(page):
    """The contact page support form labels its four fields.

    cov: C-CF-259
    """
    visit(page, "/pages/contact-us")
    for label in ("Name", "Email", "Subject", "Message"):
        expect(page.get_by_label(label, exact=True).first).to_be_visible()


def test_database_holds_eighteen_named_tables_with_listed_columns(db):
    """Every named table exists, each carrying the columns the data model lists.

    cov: C-DM-21, C-DM-22
    """
    missing_columns = {}
    for table, columns in TABLE_COLUMNS.items():
        present = db.columns_of(table)
        assert present, f"the {table} table is missing or empty of columns"
        absent = [c for c in columns if c not in present]
        if absent:
            missing_columns[table] = absent
    assert len(TABLE_COLUMNS) == 18, "the data model names eighteen tables"
    assert not missing_columns, f"tables missing listed columns: {missing_columns}"


def test_no_table_stores_derived_availability_saving_rating_values(db):
    """Derived values live in no column, and a bundle variant stores no compare-at price.

    cov: C-DM-23
    """
    stored = {}
    for table, columns in DERIVED_COLUMNS.items():
        present = db.columns_of(table)
        found = [c for c in columns if c in present]
        if found:
            stored[table] = found
    assert not stored, f"derived values are stored as columns: {stored}"
    assert db.variant(SKU_BUNDLE_GREY_AQUA).get("compare_at_price") is None, "a bundle variant stores a compare-at price"


def test_product_kind_variant_sku_present_unique_grams_above_zero(db, anon_client):
    """Product kind stays in its four values, every variant sku is present and unique, grams stay above zero.

    cov: C-DM-24, C-DM-25, C-DM-26
    """
    kinds = {row.get("kind") for row in db.rows_of("products")}
    assert kinds <= {"watch", "strap", "bundle", "accessory"}, f"product kinds include {sorted(kinds)}"
    variants = db.rows_of("variants")
    skus = [row.get("sku") for row in variants]
    assert all(skus) and len(set(skus)) == len(skus), "variant skus are missing or repeated"
    light = [(row.get("sku"), row.get("grams")) for row in variants if not (row.get("grams") or 0) > 0]
    assert not light, f"variants carrying no positive grams: {light}"


def test_product_pages_carry_read_more_with_see_all():
    """A watch page offers Read more, and its rails offer See all.

    cov: C-FE-61
    """
    _, text = html_text(f"/products/{AQUA}")
    for copy in ("Read more", "See all"):
        assert copy in text, f"the aqua page lacks {copy!r}"


def test_no_page_collects_or_shows_watch_serial_number():
    """No public page mentions a watch serial number.

    cov: C-CN-19
    """
    for path in PUBLIC_ROUTES:
        assert not re.search(r"serial number", html_text(path)[1], re.I), f"{path} mentions a serial number"
