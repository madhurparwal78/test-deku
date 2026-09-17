from __future__ import annotations

import concurrent.futures
import re
import threading

import httpx
from appclient import api_base, app_url
from conftest import (
    ATOMIC_KEEP, ATOMIC_KEEP_SKU, ATOMIC_LAST, ATOMIC_LAST_SKU, LANYARD_LIVE,
    LANYARD_SAGE_SKU, PLATE_CYPRESS_SKU, PLATE_FERN_SKU, WALLET, WALLET_LIST,
    WALLET_LIVE, WALLET_UMBER_SKU, WALLET_UMBER_TITLE,
    BASALT_CASE_SKU, BASICS_CASE, CASES, CASES_TOTAL, CATEGORIES, CERISE_SKU,
    CINNABAR_LIST, CINNABAR_LIVE, CINNABAR_SKU, CLARITY_CASE, CLIENT_ERRORS,
    CODE_SUBJECT, COMPATIBILITY_WARNING, DENIALS, DISCOUNT_ORDER, EXPRESS_PRICE,
    EXPRESS_WINDOW, FLEX, FLEX_LIVE, FLEX_PANEL, FLEX_SAGE_SKU, GRIP_MARIGOLD_SKU,
    HEADING_WITH_MODEL, HEADING_WITHOUT_MODEL, LATCH_CASE, LATCH_CASE_PANEL,
    LATCH_CASE_PANEL_TITLES, LATCH_CLEAR, MAGNETIC_CASES, MODEL,
    MODEL_LISTING_TOTAL, NEWEST_FIRST_FOUR, NEWSLETTER_MESSAGE, NOT_SERVED,
    OCHRE_SKU, ORDER_SUBJECT, PAGE_SIZE, PLATE_LIVE, PLATE_VIOLET_SKU,
    PRICE_HIGH_LOW, PRICE_LOW_HIGH, PUBLISHED_TOTAL, RETIRED_MODEL, RING_MOUNT,
    RING_MOUNT_SKU, SECOND_EMAIL, SECOND_PHONE, SERVED_PINCODE, SHOPPER_PHONE,
    STANDARD_ONLY_PINCODE, STANDARD_WINDOW, TWO_ATTEMPTS_LEFT, UMBER_LIST,
    UMBER_LIVE, UMBER_OR_CINNABAR_TOTAL, UMBER_SKU, UMBER_TOTAL,
    UNDER_1000_TOTAL, UNPUBLISHED_BASICS, UNSERVED_PINCODE, add_line, app_page,
    cart, client, codes_for, handles, killbill_account,
    killbill_invoices_for_order, line_for, listing, mails_to, order_body, pay,
    place_order, product, request_code, rows_of, settle, unique_email,
    unique_phone, verify_code,
)


def test_health_route_answers_ready():
    with client() as c:
        response = c.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:300]}"
    )


def test_listing_first_page_is_full_after_unpublished_are_excluded():
    with client() as c:
        page = listing(c, category=CASES, model=MODEL, sort="newest", page=1)
    found = handles(page)
    assert len(found) == PAGE_SIZE, (
        f"page 1 of {CASES} for {MODEL} holds {len(found)} products; "
        f"{MODEL_LISTING_TOTAL} published products match, so a full page of "
        f"{PAGE_SIZE} exists. A page filtered after it was read comes back short"
    )
    leaked = sorted(set(found) & set(UNPUBLISHED_BASICS))
    assert not leaked, f"unpublished products appear in the listing: {leaked}"
    assert page["total_count"] == MODEL_LISTING_TOTAL, (
        f"total_count reads {page.get('total_count')!r}, expected "
        f"{MODEL_LISTING_TOTAL} published products"
    )


def test_listing_total_count_and_next_page_on_every_page():
    with client() as c:
        pages = [listing(c, category=CASES, model=MODEL, sort="newest", page=n)
                 for n in (1, 2, 3)]
    sizes = [len(rows_of(p)) for p in pages]
    assert sizes == [24, 24, 12], f"the three pages hold {sizes}, expected 24, 24, 12"
    assert pages[0]["has_more"] is True and pages[0]["next_page"] == 2, (
        f"page 1 reports has_more {pages[0].get('has_more')!r} next_page "
        f"{pages[0].get('next_page')!r}"
    )
    assert pages[2]["has_more"] is False, (
        f"the last page reports has_more {pages[2].get('has_more')!r}"
    )
    assert pages[2]["next_page"] is None, (
        f"the last page reports next_page {pages[2].get('next_page')!r}, expected null"
    )
    walked = [h for p in pages for h in handles(p)]
    assert len(walked) == len(set(walked)) == MODEL_LISTING_TOTAL, (
        f"walking three pages collected {len(walked)} handles, "
        f"{len(set(walked))} distinct, expected {MODEL_LISTING_TOTAL}"
    )


def test_listing_newest_sort_orders_by_sequence():
    with client() as c:
        page = listing(c, category=CASES, model=MODEL, sort="newest", page=1)
    found = handles(page)
    assert found[:4] == NEWEST_FIRST_FOUR, (
        f"newest first begins {found[:4]}, expected {NEWEST_FIRST_FOUR}"
    )
    assert found[4] == "basics-clear-case-60-arbone-16-pro", (
        f"the fifth newest product is {found[4]!r}, expected basics-clear-case-60-arbone-16-pro"
    )


def test_generated_basics_rows_match_the_rule():
    with client() as c:
        seven = product(c, "basics-clear-case-07-arbone-16-pro")
        sixty = product(c, "basics-clear-case-60-arbone-16-pro")
    assert seven.status_code == 200, seven.text[:300]
    variant = seven.json()["variants"][0]
    assert variant["sku"] == "basics-clear-case-07-arbone-16-pro-cinnabar", variant
    assert (variant["colourway"], variant["list_price"], variant["live_price"],
            variant["stock"]) == ("Cinnabar", 159900, 149900, 8), (
        f"basics row 7 reads {variant}, expected Cinnabar list 159900 live 149900 stock 8"
    )
    assert sixty.status_code == 200, sixty.text[:300]
    last = sixty.json()["variants"][0]
    assert last["live_price"] == last["list_price"] == 189900, (
        f"basics row 60 reads live {last['live_price']} list {last['list_price']}, "
        f"expected both 189900"
    )


def test_published_catalogue_counts_across_categories():
    with client() as c:
        totals = {slug: listing(c, category=slug, sort="newest")["total_count"]
                  for slug in CATEGORIES}
    assert totals[CASES] == CASES_TOTAL, (
        f"the unconstrained {CASES} listing counts {totals[CASES]}, expected {CASES_TOTAL}"
    )
    assert sum(totals.values()) == PUBLISHED_TOTAL, (
        f"published products across the six categories total {sum(totals.values())} "
        f"({totals}), expected {PUBLISHED_TOTAL}"
    )


def test_feature_filter_excludes_products_that_carry_no_features():
    with client() as c:
        page = listing(c, category=CASES, model=MODEL, feature="magnetic", sort="newest")
    assert page["total_count"] == len(MAGNETIC_CASES), (
        f"the magnetic feature filter counts {page.get('total_count')!r}; exactly "
        f"{len(MAGNETIC_CASES)} cases carry that feature, and a product with no "
        f"features at all never matches a feature filter"
    )
    assert sorted(handles(page)) == sorted(MAGNETIC_CASES), (
        f"the magnetic feature filter returned {handles(page)}"
    )


def test_colour_facet_matches_any_colourway():
    with client() as c:
        umber = listing(c, category=CASES, model=MODEL, colour="Umber")
        either = c.get("/products", params=[("category", CASES), ("model", MODEL),
                                            ("colour", "Umber"), ("colour", "Cinnabar")])
    assert umber["total_count"] == UMBER_TOTAL, (
        f"colour=Umber counts {umber.get('total_count')!r}, expected {UMBER_TOTAL}"
    )
    assert either.status_code == 200, either.text[:300]
    assert either.json()["total_count"] == UMBER_OR_CINNABAR_TOTAL, (
        f"colour=Umber&colour=Cinnabar counts {either.json().get('total_count')!r}, "
        f"expected {UMBER_OR_CINNABAR_TOTAL}"
    )


def test_clearing_the_model_widens_the_listing():
    with client() as c:
        narrow = listing(c, category=CASES, model=MODEL)
        wide = listing(c, category=CASES)
    assert narrow["heading"] == HEADING_WITH_MODEL, (
        f"the model listing heading reads {narrow.get('heading')!r}"
    )
    assert wide["heading"] == HEADING_WITHOUT_MODEL, (
        f"the listing heading without a model reads {wide.get('heading')!r}"
    )
    assert wide["total_count"] == CASES_TOTAL > narrow["total_count"], (
        f"clearing the model changed total_count from {narrow.get('total_count')!r} "
        f"to {wide.get('total_count')!r}; it widens to {CASES_TOTAL}"
    )


def test_retired_model_listing_still_resolves():
    with client() as c:
        page = listing(c, category=CASES, model=RETIRED_MODEL)
    assert page["retired_model"] is True, (
        f"the {RETIRED_MODEL} listing reports retired_model {page.get('retired_model')!r}"
    )
    assert handles(page) == ["latch-phone-case-arbone-15"], (
        f"the retired model listing returned {handles(page)}"
    )


def test_price_band_filters_on_lowest_live_price():
    with client() as c:
        page = listing(c, category=CASES, model=MODEL, price_band="under-1000")
    assert page["total_count"] == UNDER_1000_TOTAL, (
        f"price_band=under-1000 counts {page.get('total_count')!r}, expected {UNDER_1000_TOTAL}"
    )


def test_search_matches_titles_and_redirects_an_exact_model_name():
    with client() as c:
        by_colour = c.get("/search", params={"q": "Cinnabar"})
        by_model = c.get("/search", params={"q": "  arbone 16 pro "})
    assert by_colour.status_code == 200, by_colour.text[:300]
    assert LATCH_CLEAR in handles(by_colour.json()), (
        f"searching Cinnabar did not return {LATCH_CLEAR}"
    )
    assert by_model.status_code == 200, by_model.text[:300]
    assert by_model.json().get("redirect") == "/list/arbor/arbone-16-pro", (
        f"an exact model name search returned redirect {by_model.json().get('redirect')!r}"
    )


def test_price_low_high_sorts_by_lowest_colourway_live_price():
    with client() as c:
        page = listing(c, category=CASES, model=MODEL, feature="magnetic",
                       sort="price-low-high")
    assert handles(page) == PRICE_LOW_HIGH, (
        f"price-low-high returned {handles(page)}, expected {PRICE_LOW_HIGH}: a "
        f"product sorts on its lowest live price across colourways, so "
        f"{LATCH_CLEAR} sorts at 159900, not at its first colourway's 179900"
    )


def test_price_high_low_sorts_on_the_same_lowest_price():
    with client() as c:
        page = listing(c, category=CASES, model=MODEL, feature="magnetic",
                       sort="price-high-low")
    assert handles(page) == PRICE_HIGH_LOW, (
        f"price-high-low returned {handles(page)}, expected {PRICE_HIGH_LOW}"
    )


def test_discount_sort_uses_the_largest_percentage_off():
    with client() as c:
        page = listing(c, category=CASES, model=MODEL, feature="magnetic", sort="discount")
    assert handles(page) == DISCOUNT_ORDER, (
        f"discount sort returned {handles(page)}, expected {DISCOUNT_ORDER}"
    )


def test_device_options_list_unavailable_models_and_skip_retired():
    with client() as c:
        response = c.get(f"/products/{LATCH_CASE}/device-options",
                         params={"colourway": "Amber"})
    assert response.status_code == 200, response.text[:300]
    options = {o["slug"]: o for o in response.json()["options"]}
    order = [o["slug"] for o in response.json()["options"]]
    assert order == ["arbone-17-pro-max", "arbone-17-pro", "arbone-17", MODEL,
                     "arbone-16", "solarion-s26-ultra", "solarion-s25-ultra"], (
        f"device options read {order}; every non retired phone model is listed in "
        f"rank order and the retired {RETIRED_MODEL} is not"
    )
    assert options["solarion-s25-ultra"]["available"] is False, options["solarion-s25-ultra"]
    assert options["arbone-17"]["available"] is False, (
        "arbone-17 has only an unpublished product of this design and must read unavailable"
    )
    assert options["arbone-17-pro"]["available"] is True, options["arbone-17-pro"]


def test_device_option_keeps_colourway_or_falls_back_to_first():
    with client() as c:
        amber = c.get(f"/products/{LATCH_CASE}/device-options", params={"colourway": "Amber"})
        sage = c.get(f"/products/{LATCH_CASE}/device-options", params={"colourway": "Sage"})
    a = {o["slug"]: o for o in amber.json()["options"]}
    s = {o["slug"]: o for o in sage.json()["options"]}
    assert a["arbone-17-pro"]["handle"] == "latch-phone-case-arbone-17-pro", a["arbone-17-pro"]
    assert a["arbone-17-pro"]["colourway"] == "Basalt", (
        f"Amber is not cut for arbone-17-pro, so the option falls back to its first "
        f"colourway Basalt; it reads {a['arbone-17-pro'].get('colourway')!r}"
    )
    assert s["arbone-17-pro"]["colourway"] == "Sage", (
        f"Sage exists on arbone-17-pro and is kept; it reads {s['arbone-17-pro'].get('colourway')!r}"
    )
    assert a["solarion-s26-ultra"]["colourway"] == "Amber", a["solarion-s26-ultra"]


def test_device_models_endpoint_excludes_retired():
    with client() as c:
        response = c.get("/device-models")
    assert response.status_code == 200, response.text[:300]
    slugs = [row["slug"] for row in rows_of(response.json())]
    assert RETIRED_MODEL not in slugs, f"the retired model is listed: {slugs}"
    assert MODEL in slugs, f"{MODEL} is missing from {slugs}"


def test_product_document_carries_variants_in_position_order():
    with client() as c:
        response = product(c, LATCH_CLEAR)
    assert response.status_code == 200, response.text[:300]
    body = response.json()
    assert body["title"] == "Umber Latch Clear Phone Case Cover for Arbone 16 Pro", body.get("title")
    variants = [(v["colourway"], v["live_price"], v["list_price"]) for v in body["variants"]]
    assert variants == [("Umber", UMBER_LIVE, UMBER_LIST), ("Cinnabar", CINNABAR_LIVE, CINNABAR_LIST)], (
        f"{LATCH_CLEAR} variants read {variants}"
    )


def test_build_panel_offers_four_published_modules_in_rank_order():
    with client() as c:
        response = c.get(f"/products/{LATCH_CASE}/compatible")
    assert response.status_code == 200, response.text[:300]
    rows = rows_of(response.json())
    assert [r["handle"] for r in rows] == LATCH_CASE_PANEL, (
        f"the build panel reads {[r['handle'] for r in rows]}, expected {LATCH_CASE_PANEL}: "
        f"only published modules, by edge rank, at most four, so the unpublished "
        f"{RING_MOUNT} never appears and never takes a slot"
    )
    assert [r["title"] for r in rows] == LATCH_CASE_PANEL_TITLES, (
        f"build panel titles read {[r['title'] for r in rows]}"
    )


def test_maglock_case_is_offered_only_the_magnetic_stand():
    with client() as c:
        response = c.get(f"/products/{CLARITY_CASE}/compatible")
    assert response.status_code == 200, response.text[:300]
    assert [r["handle"] for r in rows_of(response.json())] == [FLEX], (
        f"the MagLock case panel reads {[r['handle'] for r in rows_of(response.json())]}; "
        f"a case without the lock pattern is offered only {FLEX}"
    )


def test_case_without_edges_has_an_empty_panel():
    with client() as c:
        response = c.get(f"/products/{BASICS_CASE}/compatible")
    assert response.status_code == 200, response.text[:300]
    assert rows_of(response.json()) == [], (
        f"{BASICS_CASE} has no compatibility edges but its panel returned "
        f"{rows_of(response.json())}"
    )


def test_module_panel_offers_compatible_cases_symmetrically():
    with client() as c:
        response = c.get(f"/products/{FLEX}/compatible")
    assert response.status_code == 200, response.text[:300]
    assert [r["handle"] for r in rows_of(response.json())] == FLEX_PANEL, (
        f"the flex stand panel reads {[r['handle'] for r in rows_of(response.json())]}, "
        f"expected {FLEX_PANEL}"
    )


def test_unpublished_product_is_denied_by_handle(shopper_token):
    with client() as anon, client(shopper_token) as signed_in:
        anonymous = product(anon, RING_MOUNT)
        shopper = product(signed_in, RING_MOUNT)
    assert anonymous.status_code == 404, (
        f"GET /api/products/{RING_MOUNT} answered a visitor with {anonymous.status_code}"
    )
    assert shopper.status_code == 404, (
        f"GET /api/products/{RING_MOUNT} answered a signed in shopper with {shopper.status_code}"
    )


def test_unpublished_variant_is_denied_from_the_cart():
    with client() as c:
        response = add_line(c, RING_MOUNT_SKU, 1)
        after = cart(c)
    assert response.status_code in CLIENT_ERRORS, (
        f"adding the unpublished SKU {RING_MOUNT_SKU} by name returned {response.status_code}"
    )
    assert line_for(after, RING_MOUNT_SKU) is None, "the unpublished variant reached the cart"


def test_unpublished_product_is_absent_from_search_and_listings():
    with client() as c:
        found = c.get("/search", params={"q": "Ring Mount"})
        grips = listing(c, category="phone-grips")
    assert found.status_code == 200, found.text[:300]
    assert RING_MOUNT not in handles(found.json()), "the unpublished product appears in search"
    assert RING_MOUNT not in handles(grips), "the unpublished product appears in a listing"
    assert grips["total_count"] == 1, f"phone-grips counts {grips.get('total_count')!r}, expected 1"


def test_unpublished_product_cannot_be_saved_to_a_wishlist(shopper_token):
    with client(shopper_token) as c:
        response = c.post("/wishlist", json={"handle": RING_MOUNT})
        saved = c.get("/wishlist")
    assert response.status_code in CLIENT_ERRORS, (
        f"saving the unpublished {RING_MOUNT} returned {response.status_code}"
    )
    assert RING_MOUNT not in [r.get("handle") for r in rows_of(saved.json())]


def test_cart_totals_two_colourways_at_their_own_prices():
    with client() as c:
        assert add_line(c, UMBER_SKU, 1).status_code in (200, 201)
        assert add_line(c, CINNABAR_SKU, 1).status_code in (200, 201)
        body = cart(c)
    assert body["subtotal"] == UMBER_LIVE + CINNABAR_LIVE, (
        f"a cart of one Umber and one Cinnabar {LATCH_CLEAR} totals {body.get('subtotal')!r}; "
        f"each colourway is priced as itself, {UMBER_LIVE} plus {CINNABAR_LIVE}"
    )
    assert body["list_total"] == UMBER_LIST + CINNABAR_LIST, body
    assert body["currency"] == "inr", f"cart currency reads {body.get('currency')!r}"


def test_cart_discount_is_list_total_minus_subtotal():
    with client() as c:
        add_line(c, UMBER_SKU, 2)
        add_line(c, FLEX_SAGE_SKU, 1)
        body = cart(c)
    assert body["discount"] == body["list_total"] - body["subtotal"] == (
        2 * (UMBER_LIST - UMBER_LIVE) + (129900 - FLEX_LIVE)), (
        f"the cart discount reads {body.get('discount')!r} over list {body.get('list_total')!r} "
        f"and subtotal {body.get('subtotal')!r}"
    )


def test_cart_quantity_above_stock_is_refused_and_unchanged():
    with client() as c:
        assert add_line(c, OCHRE_SKU, 1).status_code in (200, 201)
        response = c.patch(f"/cart/lines/{OCHRE_SKU}", json={"quantity": 2})
        body = cart(c)
    assert response.status_code in CLIENT_ERRORS, (
        f"raising {OCHRE_SKU} above its stock of 1 returned {response.status_code}"
    )
    assert line_for(body, OCHRE_SKU)["quantity"] == 1, line_for(body, OCHRE_SKU)


def test_cart_quantity_below_one_is_refused():
    with client() as c:
        add_line(c, FLEX_SAGE_SKU, 1)
        response = c.patch(f"/cart/lines/{FLEX_SAGE_SKU}", json={"quantity": 0})
        body = cart(c)
    assert response.status_code in CLIENT_ERRORS, (
        f"setting a quantity of 0 returned {response.status_code}; removal is its own action"
    )
    assert line_for(body, FLEX_SAGE_SKU)["quantity"] == 1


def test_cart_survives_with_the_same_cart_token():
    with client() as first:
        add_line(first, PLATE_VIOLET_SKU, 1)
        token = first.cookies.get("cart_token")
    assert token, "the first cart write set no cart_token cookie"
    with client() as later:
        later.cookies.set("cart_token", token)
        body = cart(later)
    assert line_for(body, PLATE_VIOLET_SKU) is not None, (
        "a later request carrying the same cart_token does not see the cart's line"
    )


def test_module_without_a_case_carries_the_compatibility_warning():
    with client() as c:
        add_line(c, GRIP_MARIGOLD_SKU, 1)
        alone = line_for(cart(c), GRIP_MARIGOLD_SKU)
        add_line(c, BASALT_CASE_SKU, 1)
        paired = line_for(cart(c), GRIP_MARIGOLD_SKU)
    assert alone.get("warning") == COMPATIBILITY_WARNING, (
        f"a grip with no case reads warning {alone.get('warning')!r}"
    )
    assert not paired.get("warning"), (
        f"after adding a compatible case the grip still reads warning {paired.get('warning')!r}"
    )


def test_sign_in_code_email_arrives_in_the_inbox():
    phone, email = unique_phone(), unique_email()
    response = request_code(phone, email)
    assert response.status_code in (200, 201, 202), response.text[:300]
    settle()
    mails = mails_to(email, CODE_SUBJECT)
    assert len(mails) == 1, f"{email} received {len(mails)} sign in code emails, expected 1"
    assert re.match(r"\s*\d{6}", mails[0]["text"]), (
        f"the code email body does not begin with six digits: {mails[0]['text'][:80]!r}"
    )


def test_sign_in_code_cannot_be_used_twice():
    phone, email = unique_phone(), unique_email()
    request_code(phone, email)
    settle()
    code = codes_for(email)[0]
    first = verify_code(phone, code)
    second = verify_code(phone, code)
    assert first.status_code == 200 and first.json().get("access_token"), first.text[:300]
    assert second.status_code in CLIENT_ERRORS, (
        f"verifying an already used code returned {second.status_code}: {second.text[:300]}"
    )
    assert "access_token" not in second.text, "a reused code issued a session"


def test_newer_sign_in_code_cancels_the_older():
    phone, email = unique_phone(), unique_email()
    request_code(phone, email)
    settle()
    older = codes_for(email)[0]
    request_code(phone, email)
    settle()
    newer = codes_for(email)[0]
    stale = verify_code(phone, older)
    fresh = verify_code(phone, newer)
    assert stale.status_code in CLIENT_ERRORS, (
        f"an older code verified after a newer one was requested: {stale.status_code}"
    )
    assert fresh.status_code == 200, f"the newer code was refused: {fresh.text[:300]}"


def test_code_for_an_existing_phone_goes_only_to_the_email_on_file():
    stranger = unique_email()
    before = len(codes_for(SECOND_EMAIL))
    response = request_code(SECOND_PHONE, stranger)
    assert response.status_code in (200, 201, 202), response.text[:300]
    settle()
    assert codes_for(stranger) == [], (
        f"a code for the existing phone {SECOND_PHONE} was sent to the email supplied "
        f"in the request, {stranger}, instead of the email on file"
    )
    assert len(codes_for(SECOND_EMAIL)) == before + 1, (
        f"the code for {SECOND_PHONE} did not reach the email on file, {SECOND_EMAIL}"
    )


def test_code_request_response_does_not_reveal_an_existing_phone():
    existing = request_code(SHOPPER_PHONE, unique_email())
    fresh = request_code(unique_phone(), unique_email())
    assert existing.status_code == fresh.status_code, (
        f"a known phone answered {existing.status_code} and a new one {fresh.status_code}"
    )
    assert existing.json() == fresh.json(), (
        f"a known phone answered {existing.json()} and a new one {fresh.json()}"
    )


def test_new_phone_becomes_a_shopper_on_first_verify():
    phone, email = unique_phone(), unique_email()
    request_code(phone, email)
    settle()
    verified = verify_code(phone, codes_for(email)[0])
    assert verified.status_code == 200, verified.text[:300]
    shopper = verified.json()["shopper"]
    assert (shopper["phone"], shopper["email"]) == (phone, email), shopper


def test_sign_out_ends_the_session():
    phone, email = unique_phone(), unique_email()
    request_code(phone, email)
    settle()
    token = verify_code(phone, codes_for(email)[0]).json()["access_token"]
    with client(token) as c:
        assert c.get("/orders").status_code == 200
        signed_out = c.post("/auth/sign-out")
        after = c.get("/orders")
    assert signed_out.status_code in (200, 204), signed_out.text[:300]
    assert after.status_code in DENIALS, (
        f"the token still reads orders after sign out: {after.status_code}"
    )


def test_six_wrong_codes_lock_the_phone_even_for_the_right_code():
    phone, email = unique_phone(), unique_email()
    request_code(phone, email)
    settle()
    right = codes_for(email)[0]
    wrong = "000000" if right != "000000" else "111111"
    for _ in range(6):
        verify_code(phone, wrong)
    locked = verify_code(phone, right)
    assert locked.status_code in CLIENT_ERRORS, (
        f"the correct code verified after six wrong codes: {locked.status_code}"
    )
    assert "lock" in locked.text.lower(), (
        f"the refusal does not say the number is locked: {locked.text[:300]}"
    )


def test_fourth_wrong_code_reports_two_attempts_left():
    phone, email = unique_phone(), unique_email()
    request_code(phone, email)
    settle()
    right = codes_for(email)[0]
    wrong = "000000" if right != "000000" else "111111"
    responses = [verify_code(phone, wrong) for _ in range(4)]
    fourth = responses[-1]
    assert fourth.status_code in CLIENT_ERRORS, fourth.text[:300]
    assert fourth.json().get("attempts_left") == 2, fourth.json()
    assert TWO_ATTEMPTS_LEFT in fourth.text, fourth.text[:300]


def test_sixth_code_request_repeatedly_in_ten_minutes_is_refused():
    phone, email = unique_phone(), unique_email()
    codes = [request_code(phone, email).status_code for _ in range(6)]
    assert all(c in (200, 201, 202) for c in codes[:5]), f"the first five requests returned {codes[:5]}"
    assert codes[5] in CLIENT_ERRORS, (
        f"a sixth code request inside ten minutes returned {codes[5]}"
    )


def test_invalid_phone_is_refused():
    response = request_code("12345", unique_email())
    assert response.status_code in CLIENT_ERRORS, (
        f"a five digit phone returned {response.status_code}"
    )


def _at_once(calls):
    gate = threading.Barrier(len(calls))

    def fire(call):
        gate.wait()
        return call()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(calls)) as pool:
        return list(pool.map(fire, calls))


def _warm(count, token=None):
    clients = [client(token) for _ in range(count)]
    for c in clients:
        c.get("/health")
    return clients


def _close(clients):
    for c in clients:
        c.close()


def _variant(handle, sku):
    with client() as c:
        response = product(c, handle)
    assert response.status_code == 200, f"GET /api/products/{handle} returned {response.status_code}"
    return [v for v in response.json()["variants"] if v["sku"] == sku][0]


def test_simultaneous_verifications_of_one_code_issue_one_session():
    phone, email = unique_phone(), unique_email()
    request_code(phone, email)
    settle()
    code = codes_for(email)[0]
    clients = _warm(16)
    try:
        responses = _at_once([lambda c=c: c.post("/auth/verify-code", json={"phone": phone, "code": code})
                              for c in clients])
    finally:
        _close(clients)
    codes = [r.status_code for r in responses]
    sessions = [r for r in responses if r.status_code == 200 and "access_token" in r.text]
    assert len(sessions) == 1, (
        f"sixteen simultaneous verifications of one code returned {sorted(codes)}; exactly "
        f"one of them issues a session"
    )
    refused = [c for c in codes if c != 200]
    assert len(refused) == 15 and all(c in CLIENT_ERRORS for c in refused), (
        f"the other verifications of the used code returned {sorted(refused)}"
    )


def test_a_code_presented_with_another_phone_is_refused():
    phone, email = unique_phone(), unique_email()
    other, other_email = unique_phone(), unique_email()
    request_code(phone, email)
    request_code(other, other_email)
    settle()
    code = codes_for(email)[0]
    if codes_for(other_email)[0] == code:
        request_code(other, other_email)
        settle()
    borrowed = verify_code(other, code)
    assert borrowed.status_code in CLIENT_ERRORS and "access_token" not in borrowed.text, (
        f"the code sent for {phone} opened a session for {other}: "
        f"{borrowed.status_code} {borrowed.text[:300]}"
    )
    own = verify_code(phone, code)
    assert own.status_code == 200 and own.json()["shopper"]["phone"] == phone, (
        f"the code stopped working for its own phone after it was presented with another: "
        f"{own.status_code} {own.text[:300]}"
    )


def test_a_burst_of_simultaneous_wrong_codes_still_locks_the_phone():
    phone, email = unique_phone(), unique_email()
    request_code(phone, email)
    settle()
    right = codes_for(email)[0]
    wrong = "000000" if right != "000000" else "111111"
    clients = _warm(16)
    try:
        burst = _at_once([lambda c=c: c.post("/auth/verify-code", json={"phone": phone, "code": wrong})
                          for c in clients])
    finally:
        _close(clients)
    statuses = sorted(r.status_code for r in burst)
    assert all(s in CLIENT_ERRORS for s in statuses), (
        f"sixteen simultaneous wrong codes returned {statuses}"
    )
    locked = verify_code(phone, right)
    assert locked.status_code in CLIENT_ERRORS and "access_token" not in locked.text, (
        f"the correct code verified after sixteen simultaneous wrong codes: "
        f"{locked.status_code} {locked.text[:300]}"
    )
    assert "lock" in locked.text.lower(), (
        f"the refusal after a burst of wrong codes does not say the number is locked: "
        f"{locked.text[:300]}"
    )


def test_simultaneous_code_requests_send_at_most_five_codes():
    phone, email = unique_phone(), unique_email()
    clients = _warm(10)
    try:
        burst = _at_once([lambda c=c: c.post("/auth/request-code", json={"phone": phone, "email": email})
                          for c in clients])
    finally:
        _close(clients)
    statuses = sorted(r.status_code for r in burst)
    accepted = [s for s in statuses if s in (200, 201, 202)]
    assert all(s in (200, 201, 202) or s in CLIENT_ERRORS for s in statuses), (
        f"ten simultaneous code requests for one phone returned {statuses}; a refusal is a "
        f"client error, never a server error"
    )
    assert 1 <= len(accepted) <= 5, (
        f"ten simultaneous code requests accepted {len(accepted)}: {statuses}; at most five "
        f"codes are sent inside ten minutes"
    )
    settle(5.0)
    sent = len(mails_to(email, CODE_SUBJECT))
    assert sent == len(accepted), (
        f"{email} received {sent} sign in code emails for {len(accepted)} accepted requests"
    )


def _race(tokens, sku, quantity):
    clients = [client(token) for token in tokens]
    try:
        for c in clients:
            added = add_line(c, sku, quantity)
            assert added.status_code in (200, 201), (
                f"preparing the race, adding {quantity} of {sku} returned "
                f"{added.status_code}: {added.text[:300]}"
            )
        gate = threading.Barrier(len(clients))

        def fire(c):
            gate.wait()
            return c.post("/orders", json=order_body())

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(clients)) as pool:
            responses = list(pool.map(fire, clients))
        return [(response, cart(c)) for response, c in zip(responses, clients)]
    finally:
        for c in clients:
            c.close()


def test_concurrent_orders_for_the_last_unit_create_exactly_one(shopper_token, second_token):
    results = _race([shopper_token, second_token], OCHRE_SKU, 1)
    codes = sorted(r[0].status_code for r in results)
    created = [c for c in codes if c in (200, 201)]
    assert len(created) == 1, (
        f"two simultaneous orders for the last {OCHRE_SKU} returned {codes}; exactly one "
        f"order is created"
    )
    assert 409 in codes, f"the losing order returned {codes}, expected a 409 conflict response"
    with client() as c:
        stock = [v for v in product(c, "latch-signature-phone-case-arbone-16-pro").json()["variants"]
                 if v["sku"] == OCHRE_SKU][0]["stock"]
    assert stock == 0, f"after the race {OCHRE_SKU} stock reads {stock}, expected 0"


def test_contention_over_limited_stock_never_goes_negative(shopper_token, second_token):
    results = _race([shopper_token, second_token], CERISE_SKU, 2)
    codes = sorted(r[0].status_code for r in results)
    assert len([c for c in codes if c in (200, 201)]) == 1, (
        f"two simultaneous orders for two units each of {CERISE_SKU}, stock 3, returned {codes}"
    )
    with client() as c:
        stock = [v for v in product(c, "latch-signature-phone-case-arbone-16-pro").json()["variants"]
                 if v["sku"] == CERISE_SKU][0]["stock"]
    assert stock == 1, f"after the race {CERISE_SKU} stock reads {stock}, expected 1, never below 0"
    loser = [r for r in results if r[0].status_code == 409][0]
    assert loser[0].json().get("sku") == CERISE_SKU, (
        f"the conflict response does not name the SKU: {loser[0].text[:300]}"
    )
    assert line_for(loser[1], CERISE_SKU)["quantity"] == 1, (
        f"the losing cart line reads {line_for(loser[1], CERISE_SKU)}; its quantity is "
        f"reduced to the 1 unit still available"
    )


def test_a_refused_order_takes_no_stock_from_its_other_lines(shopper_token, second_token):
    keep_before = _variant(ATOMIC_KEEP, ATOMIC_KEEP_SKU)["stock"]
    assert _variant(ATOMIC_LAST, ATOMIC_LAST_SKU)["stock"] == 1, "the last unit variant is not at stock 1"
    clients = [client(token) for token in (shopper_token, second_token)]
    try:
        for c in clients:
            for sku in (ATOMIC_KEEP_SKU, ATOMIC_LAST_SKU):
                added = add_line(c, sku, 1)
                assert added.status_code in (200, 201), (
                    f"preparing the race, adding {sku} returned {added.status_code}: {added.text[:300]}"
                )
        responses = _at_once([lambda c=c: c.post("/orders", json=order_body()) for c in clients])
        carts = [cart(c) for c in clients]
    finally:
        for c in clients:
            c.close()
    statuses = [r.status_code for r in responses]
    assert sorted(s in (200, 201) for s in statuses) == [False, True] and 409 in statuses, (
        f"two simultaneous orders each holding {ATOMIC_KEEP_SKU} and the last {ATOMIC_LAST_SKU} "
        f"returned {statuses}; exactly one order is created and the other is refused with a 409"
    )
    loser = statuses.index(409)
    assert responses[loser].json().get("sku") == ATOMIC_LAST_SKU, responses[loser].text[:300]
    keep_after = _variant(ATOMIC_KEEP, ATOMIC_KEEP_SKU)["stock"]
    assert keep_after == keep_before - 1, (
        f"{ATOMIC_KEEP_SKU} went from {keep_before} to {keep_after} after one order took one unit; "
        f"a refused order takes no stock from any of its lines"
    )
    assert _variant(ATOMIC_LAST, ATOMIC_LAST_SKU)["stock"] == 0
    kept = line_for(carts[loser], ATOMIC_KEEP_SKU)
    assert kept is not None and kept["quantity"] == 1, (
        f"the refused shopper's {ATOMIC_KEEP_SKU} line reads {kept}"
    )


def test_order_is_created_pending_and_empties_the_cart(shopper_token):
    with client(shopper_token) as c:
        add_line(c, FLEX_SAGE_SKU, 1)
        response = place_order(c)
        after = cart(c)
    assert response.status_code in (200, 201), response.text[:300]
    body = response.json()
    assert body["state"] == "pending", f"a new order reads state {body.get('state')!r}"
    assert body["total"] == FLEX_LIVE and body["currency"] == "inr", body
    assert after.get("lines") == [], f"the cart still holds lines after ordering: {after.get('lines')}"


def test_visitor_cannot_place_an_order():
    with client() as c:
        add_line(c, FLEX_SAGE_SKU, 1)
        response = place_order(c)
    assert response.status_code in DENIALS, (
        f"a visitor placing an order returned {response.status_code}"
    )


def test_order_to_an_unserved_pincode_is_refused(shopper_token):
    with client(shopper_token) as c:
        add_line(c, FLEX_SAGE_SKU, 1)
        response = place_order(c, pincode=UNSERVED_PINCODE)
        after = cart(c)
    assert response.status_code in CLIENT_ERRORS, (
        f"an order to the unserved pincode {UNSERVED_PINCODE} returned {response.status_code}"
    )
    assert line_for(after, FLEX_SAGE_SKU) is not None, "a refused order emptied the cart"


def test_order_lines_snapshot_title_and_prices(shopper_token):
    with client(shopper_token) as c:
        add_line(c, UMBER_SKU, 1)
        body = place_order(c).json()
        again = c.get(f"/orders/{body['number']}").json()
    line = body["lines"][0]
    assert (line["sku"], line["unit_price"], line["list_price"]) == (UMBER_SKU, UMBER_LIVE, UMBER_LIST), line
    assert line["title"] == "Umber Latch Clear Phone Case Cover for Arbone 16 Pro", line
    assert again["lines"] == body["lines"], "the stored order lines differ from the placed ones"


def test_catalogue_edit_after_ordering_leaves_the_order_lines_unchanged(shopper_token, backend):
    with client(shopper_token) as c:
        add_line(c, WALLET_UMBER_SKU, 1)
        placed = place_order(c)
    assert placed.status_code in (200, 201), placed.text[:300]
    number = placed.json()["number"]
    tail = backend.query("SELECT title_tail FROM products WHERE handle = %s", (WALLET,))[0]["title_tail"]
    try:
        backend.query("UPDATE variants SET live_price = live_price - 100 WHERE sku = %s",
                      (WALLET_UMBER_SKU,))
        backend.query("UPDATE products SET title_tail = %s WHERE handle = %s",
                      (f"{tail} Edition", WALLET))
        edited = _variant(WALLET, WALLET_UMBER_SKU)["live_price"]
        with client(shopper_token) as c:
            again = c.get(f"/orders/{number}")
    finally:
        backend.query("UPDATE variants SET live_price = live_price + 100 WHERE sku = %s",
                      (WALLET_UMBER_SKU,))
        backend.query("UPDATE products SET title_tail = %s WHERE handle = %s", (tail, WALLET))
    assert edited < WALLET_LIVE, (
        f"after the live price of {WALLET_UMBER_SKU} was lowered in the catalogue the product "
        f"still reads {edited}; the storefront shows an edited price on its next read"
    )
    assert again.status_code == 200, again.text[:300]
    line = [row for row in again.json()["lines"] if row["sku"] == WALLET_UMBER_SKU][0]
    assert (line["unit_price"], line["list_price"], line["title"]) == (
        WALLET_LIVE, WALLET_LIST, WALLET_UMBER_TITLE), (
        f"order {number} now reads {line} after a catalogue edit; an order line keeps the title "
        f"and prices snapshotted at the moment of ordering"
    )


def test_paid_order_invoice_in_kill_bill_matches_the_total(shopper_token):
    with client(shopper_token) as c:
        add_line(c, UMBER_SKU, 1)
        add_line(c, FLEX_SAGE_SKU, 1)
        order = place_order(c).json()
        paid = pay(c, order["number"])
    assert paid.status_code == 200, paid.text[:300]
    assert paid.json()["state"] == "paid", paid.json()
    assert order["total"] == UMBER_LIVE + FLEX_LIVE, order
    settle()
    invoices = killbill_invoices_for_order(SHOPPER_PHONE, order["number"])
    assert len(invoices) == 1, (
        f"Kill Bill holds {len(invoices)} invoices for order {order['number']}, expected 1"
    )
    assert float(invoices[0]["amount"]) == order["total"] / 100, (
        f"the invoice for {order['number']} is {invoices[0]['amount']}, expected {order['total'] / 100}"
    )
    assert invoices[0]["currency"] == "INR", invoices[0]["currency"]


def test_idempotent_payment_replay_creates_no_second_invoice(shopper_token):
    with client(shopper_token) as c:
        add_line(c, PLATE_VIOLET_SKU, 2)
        order = place_order(c).json()
        first = pay(c, order["number"])
        second = pay(c, order["number"])
    assert first.status_code == second.status_code == 200, (first.text[:200], second.text[:200])
    assert first.json()["invoice_id"] == second.json()["invoice_id"], (
        "replaying payment returned a different invoice"
    )
    settle()
    invoices = killbill_invoices_for_order(SHOPPER_PHONE, order["number"])
    assert len(invoices) == 1, (
        f"after a replayed payment Kill Bill holds {len(invoices)} invoices for "
        f"{order['number']}; a replay must not create a second"
    )
    assert float(invoices[0]["amount"]) == 2 * PLATE_LIVE / 100, invoices[0]["amount"]


def test_simultaneous_payments_for_one_order_create_one_invoice(shopper_token):
    email = unique_email()
    with client(shopper_token) as c:
        add_line(c, PLATE_FERN_SKU, 1)
        placed = place_order(c, email=email)
    assert placed.status_code in (200, 201), placed.text[:300]
    number = placed.json()["number"]
    payers = _warm(4, shopper_token)
    try:
        responses = _at_once([lambda p=p: pay(p, number) for p in payers])
    finally:
        _close(payers)
    statuses = sorted(r.status_code for r in responses)
    assert all(s in (200, 409) for s in statuses), (
        f"four simultaneous payments for {number} returned {statuses}; each is answered with the "
        f"invoice or refused with a 409"
    )
    paid = [r.json() for r in responses if r.status_code == 200]
    assert paid and len({p["invoice_id"] for p in paid}) == 1, (
        f"simultaneous payments for {number} answered {paid}; every answer carries one invoice_id"
    )
    settle()
    invoices = killbill_invoices_for_order(SHOPPER_PHONE, number)
    assert len(invoices) == 1, (
        f"four simultaneous payments left {len(invoices)} invoices for {number} in Kill Bill, "
        f"expected 1"
    )
    assert len(mails_to(email, ORDER_SUBJECT)) == 1, (
        f"four simultaneous payments sent {len(mails_to(email, ORDER_SUBJECT))} confirmation "
        f"emails for {number}, expected 1"
    )


def test_paid_invoice_itemises_each_line_total_plus_paid_delivery(shopper_token):
    with client(shopper_token) as c:
        add_line(c, LANYARD_SAGE_SKU, 2)
        add_line(c, PLATE_CYPRESS_SKU, 1)
        placed = place_order(c, method="express")
        assert placed.status_code in (200, 201), placed.text[:300]
        order = placed.json()
        paid = pay(c, order["number"])
    assert paid.status_code == 200, paid.text[:300]
    assert (order["delivery"], order["total"]) == (
        EXPRESS_PRICE, 2 * LANYARD_LIVE + PLATE_LIVE + EXPRESS_PRICE), order
    settle()
    invoices = killbill_invoices_for_order(SHOPPER_PHONE, order["number"])
    assert len(invoices) == 1, f"Kill Bill holds {len(invoices)} invoices for {order['number']}"
    items = invoices[0].get("items") or []
    amounts = sorted(round(float(i["amount"]), 2) for i in items)
    expected = sorted([2 * LANYARD_LIVE / 100, PLATE_LIVE / 100, EXPRESS_PRICE / 100])
    assert amounts == expected, (
        f"the invoice for {order['number']} itemises {amounts}; expected one item per order line "
        f"at its line total plus one for paid delivery, {expected}"
    )
    assert all(str(i.get("description", "")).startswith(f"Order {order['number']}") for i in items), (
        [i.get("description") for i in items]
    )


def test_paid_order_sends_exactly_one_confirmation_email(shopper_token):
    email = unique_email()
    with client(shopper_token) as c:
        add_line(c, FLEX_SAGE_SKU, 1)
        order = place_order(c, email=email).json()
        pay(c, order["number"])
        pay(c, order["number"])
    settle()
    mails = mails_to(email, ORDER_SUBJECT)
    assert len(mails) == 1, f"{email} received {len(mails)} confirmation emails, expected 1"
    assert mails[0]["subject"] == f"{ORDER_SUBJECT} {order['number']}", mails[0]["subject"]
    assert mails[0]["to"] == [email] and not mails[0]["cc"] and not mails[0]["bcc"], mails[0]


def test_unpaid_order_sends_no_confirmation_email(shopper_token):
    email = unique_email()
    with client(shopper_token) as c:
        add_line(c, FLEX_SAGE_SKU, 1)
        place_order(c, email=email)
    settle()
    assert mails_to(email, ORDER_SUBJECT) == [], "an order that was never paid sent a confirmation"


def test_kill_bill_account_is_keyed_by_the_shopper_phone(second_token):
    with client(second_token) as c:
        add_line(c, FLEX_SAGE_SKU, 1)
        order = place_order(c).json()
        assert pay(c, order["number"]).status_code == 200
    account = killbill_account(SECOND_PHONE)
    assert account is not None, f"no Kill Bill account has external key shopper-{SECOND_PHONE}"
    assert account["currency"] == "INR", account


def test_other_shopper_is_denied_the_order(shopper_token, second_token):
    with client(shopper_token) as owner:
        add_line(owner, FLEX_SAGE_SKU, 1)
        order = place_order(owner).json()
    with client(second_token) as other:
        read = other.get(f"/orders/{order['number']}")
        paid = other.post(f"/orders/{order['number']}/pay")
    assert read.status_code in DENIALS, f"another shopper read the order: {read.status_code}"
    assert paid.status_code in DENIALS, f"another shopper paid the order: {paid.status_code}"
    with client(shopper_token) as owner:
        assert owner.get(f"/orders/{order['number']}").json()["state"] == "pending"


def test_visitor_is_denied_the_order_history_and_wishlist():
    with client() as c:
        orders = c.get("/orders")
        wishlist = c.get("/wishlist")
    assert orders.status_code in DENIALS, f"a visitor read order history: {orders.status_code}"
    assert wishlist.status_code in DENIALS, f"a visitor read a wishlist: {wishlist.status_code}"


def test_order_history_limit_outside_the_band_is_refused(shopper_token):
    with client(shopper_token) as c:
        low = c.get("/orders", params={"limit": 0})
        high = c.get("/orders", params={"limit": 51})
        ok = c.get("/orders", params={"limit": 1})
    assert low.status_code in CLIENT_ERRORS and high.status_code in CLIENT_ERRORS, (
        f"limit=0 returned {low.status_code} and limit=51 returned {high.status_code}"
    )
    assert ok.status_code == 200 and len(rows_of(ok.json())) <= 1, ok.text[:300]
    assert "has_more" in ok.json() and "total_count" in ok.json(), ok.json()


def test_shopper_saves_and_removes_a_wishlist_item(shopper_token):
    with client(shopper_token) as c:
        saved = c.post("/wishlist", json={"handle": FLEX})
        removed = c.delete(f"/wishlist/{FLEX}")
    assert saved.status_code in (200, 201), saved.text[:300]
    assert FLEX in [r.get("handle") for r in rows_of(saved.json())], saved.json()
    assert FLEX not in [r.get("handle") for r in rows_of(removed.json())], removed.json()


def test_delivery_check_follows_the_served_prefixes():
    with client() as c:
        mumbai = c.get("/delivery", params={"pincode": SERVED_PINCODE}).json()
        pune = c.get("/delivery", params={"pincode": STANDARD_ONLY_PINCODE}).json()
        nowhere = c.get("/delivery", params={"pincode": UNSERVED_PINCODE}).json()
        short = c.get("/delivery", params={"pincode": "40005"})
    methods = {m["code"]: m for m in mumbai["methods"]}
    assert mumbai["serviceable"] is True and methods["standard"]["price"] == 0, mumbai
    assert methods["standard"]["window"] == STANDARD_WINDOW, methods["standard"]
    assert methods["express"]["price"] == EXPRESS_PRICE, methods["express"]
    assert methods["express"]["window"] == EXPRESS_WINDOW, methods["express"]
    assert [m["code"] for m in pune["methods"]] == ["standard"], pune
    assert nowhere["serviceable"] is False and nowhere["message"] == NOT_SERVED, nowhere
    assert short.status_code in CLIENT_ERRORS, f"a five digit pincode returned {short.status_code}"


def test_newsletter_answers_repeat_subscriptions_identically():
    email = unique_email()
    with client() as c:
        first = c.post("/newsletter", json={"email": email})
        second = c.post("/newsletter", json={"email": email})
        invalid = c.post("/newsletter", json={"email": "not-an-address"})
    assert first.status_code == second.status_code == 200, (first.status_code, second.status_code)
    assert first.json() == second.json() == {"message": NEWSLETTER_MESSAGE}, (first.json(), second.json())
    assert invalid.status_code in CLIENT_ERRORS, invalid.status_code


def test_store_directory_lists_active_stores_by_type_and_place():
    with client() as c:
        airports = c.get("/stores", params={"type": "airport_outlet"}).json()
        mumbai = c.get("/stores", params={"q": "Mumbai"}).json()
        pincode = c.get("/stores", params={"q": "560038"}).json()
    assert len(rows_of(airports)) == 3, [r["name"] for r in rows_of(airports)]
    names = [r["name"] for r in rows_of(mumbai)]
    assert len(names) == 2 and "LatticeGoods Store Colaba" not in names, (
        f"Mumbai lists {names}; the inactive Colaba store is never listed"
    )
    assert [r["name"] for r in rows_of(pincode)] == ["Arbor Premium Partner Indiranagar"]


def test_favicon_is_declared_and_served():
    shell = app_page("/")
    assert shell.status_code == 200, shell.status_code
    match = re.search(r'<link[^>]*rel="(?:shortcut )?icon"[^>]*href="([^"]+)"', shell.text) or \
        re.search(r'<link[^>]*href="([^"]+)"[^>]*rel="(?:shortcut )?icon"', shell.text)
    assert match, "the document head declares no favicon"
    href = match.group(1)
    icon = httpx.get(href if href.startswith("http") else f"{app_url()}/{href.lstrip('/')}",
                     timeout=30.0)
    assert icon.status_code == 200, f"the declared favicon {href} answered {icon.status_code}"


def test_api_prefix_serves_json_on_the_app_origin():
    response = httpx.get(f"{api_base()}/device-models", timeout=30.0)
    assert response.status_code == 200, response.status_code
    assert "application/json" in response.headers.get("content-type", ""), response.headers
    assert "items" in response.json(), f"a list endpoint returned no items key: {response.json()}"


def test_seeding_twice_duplicates_no_product_row(backend):
    counts = {table: backend.count(table) for table in ("products", "variants", "stores")}
    assert counts == {"products": 434, "variants": 463, "stores": 12}, (
        f"seeded row counts read {counts}; seeding is idempotent, so a restart never "
        f"duplicates a product, variant or store row"
    )
