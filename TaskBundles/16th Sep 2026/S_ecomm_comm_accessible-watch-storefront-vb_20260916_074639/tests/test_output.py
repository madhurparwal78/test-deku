"""The one pytest module for deku/accessible-watch-storefront-vb.

Black box throughout: HTTP against the deployed app, reads of the declared store, the
real inbox and the real billing tenant. Nothing here imports the agent's code or
inspects its layout.
"""

from __future__ import annotations

import json
import os

import httpx
from appclient import api_base, app_url
from conftest import (
    ACCOUNT_HANDOFF_ROUTE,
    APP_ROOT,
    AUTHORED_PAGE_ROUTES,
    BLOG_ROUTE,
    BRAND_FULL,
    BUNDLE_BADGE,
    BUSINESS_COLOURWAYS,
    BUSINESS_TITLE,
    CARD_FIELDS,
    CART_FIELDS,
    CART_LINE_FIELDS,
    CART_ROUTE,
    CATALOGUE_TABLES,
    CATALOGUE_TOTAL,
    CATCH_ALL_HANDLE,
    CATCH_ALL_ROUTE,
    CHECKOUT_FIELDS,
    CHECKOUT_ROUTE,
    COLLECTION_FIELDS,
    CURATED_HANDLES,
    DIAMOND_CHEAPEST_AVAILABLE_MINOR,
    DIAMOND_COLOURWAYS,
    DIAMOND_TITLE,
    DISPLAY_CURRENCIES,
    HOME_PRODUCTS,
    HOME_ROUTE,
    INR_PREFIX,
    INR_RATE,
    IN_STOCK_COUNT,
    NOSNIFF_VALUE,
    OTHER_MAKER_TITLES,
    OUT_OF_STOCK_COUNT,
    PAGE_COUNT,
    PAGE_SIZE,
    POLICY_ROUTES,
    PRICE_FIELDS,
    PRODUCT_FIELDS,
    PUBLIC_ROUTES,
    REBEL_COLOURWAYS,
    REBEL_COMPARE_MINOR,
    REBEL_HANDLE,
    REBEL_OFFER_LINE,
    REBEL_OPTION_NAME,
    REBEL_TITLE,
    REQUEST_LOG_KEYS,
    REQUEST_LOG_PATH,
    RESERVED_DIRECTORIES,
    ROBOTS_ROUTE,
    SALE_BADGE,
    SECURITY_HEADER_NAMES,
    SIGNUP_CODE,
    SIGNUP_SUBJECT,
    SIGNUP_SUBJECT_PREFIX,
    SITEMAP_ROUTE,
    SORT_OPTIONS,
    STORE_CURRENCY,
    UPSELL_COMPARE_MINOR,
    UPSELL_DESCRIPTION,
    UPSELL_HANDLE,
    UPSELL_PRICE_MINOR,
    UPSELL_TITLE,
    USD_PREFIX,
    USER_README_PATH,
    VARIANT_FIELDS,
    WORKED_INR,
    WORKED_MINOR,
    WORKED_USD,
    WRITE_PROBES,
    add_line,
    cart,
    collection,
    find_account,
    find_message,
    first_available_variant,
    poll_account,
    probe_email,
    probe_reference,
    product,
)


def test_health_route_answers_two_hundred(site):
    response = site.get("/api/health")
    assert response.status_code == 200, (
        f"GET {app_url()}/api/health returned {response.status_code}, expected 200 "
        f"once the app is ready: {response.text[:400]}"
    )


def test_catch_all_reports_one_hundred_and_seventy_four_products(anon_client):
    payload = collection(anon_client)
    for field in COLLECTION_FIELDS:
        assert field in payload, (
            f"the collection payload carries no {field!r} key; it carries "
            f"{sorted(payload)}"
        )
    assert payload["count"] == CATALOGUE_TOTAL, (
        f"the catch-all collection reports count={payload['count']!r}, expected "
        f"{CATALOGUE_TOTAL}"
    )
    assert payload["pages"] == PAGE_COUNT, (
        f"the catch-all reports {payload['pages']!r} page(s) at {PAGE_SIZE} products "
        f"a page, expected {PAGE_COUNT} for {CATALOGUE_TOTAL} products"
    )
    assert len(payload["products"]) == PAGE_SIZE, (
        f"page one of the catch-all carries {len(payload['products'])} product(s), "
        f"expected {PAGE_SIZE}"
    )


def test_facet_counts_sum_to_the_collection_total(anon_client):
    payload = collection(anon_client)
    facets = payload["facets"]
    assert "availability" in facets, (
        f"the facets object carries no 'availability' key, only {sorted(facets)}"
    )
    availability = facets["availability"]
    for key, want in (("in_stock", IN_STOCK_COUNT),
                      ("out_of_stock", OUT_OF_STOCK_COUNT)):
        assert availability.get(key) == want, (
            f"the availability facet reports {key}={availability.get(key)!r}, "
            f"expected {want}. Reported facet: {availability}"
        )
    total = availability["in_stock"] + availability["out_of_stock"]
    assert total == payload["count"], (
        f"the two availability facet counts sum to {total} against a stated count of "
        f"{payload['count']}. Both are computed over the same set, so they agree"
    )


def test_seeded_catalogue_rows_are_persisted_in_the_store(store, anon_client):
    held = store.count("products")
    assert held == CATALOGUE_TOTAL, (
        f"the products table holds {held} row(s), expected {CATALOGUE_TOTAL}"
    )
    assert store.count("collections") == len(CURATED_HANDLES) + 1, (
        f"the collections table holds {store.count('collections')} row(s), expected "
        f"{len(CURATED_HANDLES) + 1}"
    )
    for handle in CURATED_HANDLES + (CATCH_ALL_HANDLE,):
        row = store.one("collections", handle=handle)
        assert row is not None, (
            f"the collections table holds no row handled {handle!r}"
        )
    upsell = store.product(UPSELL_HANDLE)
    assert upsell is not None, (
        f"the products table holds no row handled {UPSELL_HANDLE!r}; the upsell is a "
        f"product record rather than a checkout fee"
    )
    for title, *_rest in HOME_PRODUCTS:
        row = store.one("products", title=title)
        assert row is not None, (
            f"the products table holds no row titled {title!r}"
        )


def test_stored_availability_matches_the_facet_counts(store):
    available = store.count("products", available=True)
    unavailable = store.count("products", available=False)
    assert available == IN_STOCK_COUNT, (
        f"the products table holds {available} available row(s), expected "
        f"{IN_STOCK_COUNT}"
    )
    assert unavailable == OUT_OF_STOCK_COUNT, (
        f"the products table holds {unavailable} unavailable row(s), expected "
        f"{OUT_OF_STOCK_COUNT}"
    )
    assert available + unavailable == CATALOGUE_TOTAL, (
        f"available plus unavailable is {available + unavailable}, expected "
        f"{CATALOGUE_TOTAL}"
    )


def test_variant_prices_and_availability_are_stored_per_variant(store):
    rebel = store.variants_of(REBEL_HANDLE)
    assert len(rebel) == len(REBEL_COLOURWAYS), (
        f"the variants table holds {len(rebel)} row(s) for {REBEL_HANDLE!r}, expected "
        f"{len(REBEL_COLOURWAYS)}"
    )
    by_value = {row.get("option_value"): row for row in rebel}
    for value, price, available in REBEL_COLOURWAYS:
        row = by_value.get(value)
        assert row is not None, (
            f"{REBEL_HANDLE!r} holds no variant valued {value!r}; values present: "
            f"{sorted(by_value)}"
        )
        assert int(row["price_minor"]) == price, (
            f"variant {value!r} is stored at {row['price_minor']!r} minor units, "
            f"expected {price}"
        )
        assert bool(row["available"]) is available, (
            f"variant {value!r} is stored available={row['available']!r}, expected "
            f"{available}"
        )
        assert row.get("option_name") == REBEL_OPTION_NAME, (
            f"variant {value!r} carries option_name={row.get('option_name')!r}, "
            f"expected {REBEL_OPTION_NAME!r}"
        )


def test_from_price_names_the_cheapest_available_variant(anon_client):
    payload = collection(anon_client, sort_by="Featured")
    catalogue = {row["title"]: row for row in payload["products"]}
    for page in range(1, PAGE_COUNT + 1):
        if DIAMOND_TITLE in catalogue:
            break
        catalogue.update({row["title"]: row
                          for row in collection(anon_client, page=page)["products"]})
    card = catalogue.get(DIAMOND_TITLE)
    assert card is not None, (
        f"no card titled {DIAMOND_TITLE!r} was served across the catch-all's "
        f"{PAGE_COUNT} pages"
    )
    for field in CARD_FIELDS:
        assert field in card, (
            f"the card for {DIAMOND_TITLE!r} carries no {field!r} key; it carries "
            f"{sorted(card)}"
        )
    for field in PRICE_FIELDS:
        assert field in card["price"], (
            f"the price object on {DIAMOND_TITLE!r} carries no {field!r} key; it "
            f"carries {sorted(card['price'])}"
        )
    assert card["price"]["from"] is True, (
        f"{DIAMOND_TITLE!r} has colourways at different prices, so its card carries "
        f"the From form; the payload reports from={card['price']['from']!r}"
    )
    cheapest_overall = min(price for _v, price, _a in DIAMOND_COLOURWAYS)
    assert card["price"]["amount_minor"] == DIAMOND_CHEAPEST_AVAILABLE_MINOR, (
        f"{DIAMOND_TITLE!r} is served at {card['price']['amount_minor']!r} minor "
        f"units, expected {DIAMOND_CHEAPEST_AVAILABLE_MINOR}, the cheapest AVAILABLE "
        f"colourway. Its cheapest colourway overall is {cheapest_overall} and that one "
        f"is sold out, so naming it would promise a price the shop cannot honour"
    )


def test_card_rating_is_nullable_and_never_reserved(anon_client):
    payload = collection(anon_client)
    seen_titles = {row["title"]: row for row in payload["products"]}
    for page in range(2, PAGE_COUNT + 1):
        seen_titles.update({row["title"]: row
                            for row in collection(anon_client, page=page)["products"]})
    rated = [row for row in seen_titles.values() if row.get("rating")]
    unrated = [row for row in seen_titles.values() if row.get("rating") is None]
    assert rated, "no served card carries a rating; the twelve home products do"
    assert unrated, (
        "every served card carries a rating. The card must reflow rather than reserve, "
        "so the catalogue holds at least one product with none"
    )
    for row in rated:
        rating = row["rating"]
        for field in ("score", "count"):
            assert field in rating, (
                f"the rating on {row['title']!r} carries no {field!r} key; it carries "
                f"{sorted(rating)}"
            )
        assert len(str(rating["score"]).split(".")[-1]) == 1, (
            f"the rating on {row['title']!r} renders as {rating['score']!r}; a rating "
            f"renders to one decimal place always, so a perfect one renders as '5.0'"
        )


def test_home_products_are_served_with_their_originals_and_badges(anon_client, store):
    for title, compare_at, price, has_bundle, score, count in HOME_PRODUCTS:
        row = store.one("products", title=title)
        assert row is not None, f"the products table holds no row titled {title!r}"
        payload = product(anon_client, row["handle"])
        assert payload["compare_at"]["amount_minor"] == compare_at, (
            f"{title!r} is served with a compare-at of "
            f"{payload['compare_at']['amount_minor']!r} minor units, expected "
            f"{compare_at}"
        )
        cheapest = min(v["price"]["amount_minor"] for v in payload["variants"])
        assert cheapest == price, (
            f"{title!r} is served from {cheapest!r} minor units, expected {price}"
        )
        assert compare_at > price, (
            f"{title!r} carries a compare-at of {compare_at} against a price of "
            f"{price}; the struck-through original is the higher of the two"
        )
        badges = payload.get("badges") or []
        assert SALE_BADGE in badges, (
            f"{title!r} is served with badges {badges!r}; every product carrying a "
            f"compare-at above its price shows the Sale badge"
        )
        if has_bundle:
            assert BUNDLE_BADGE in badges, (
                f"{title!r} is one of the bundle products but is served with badges "
                f"{badges!r}, which does not include {BUNDLE_BADGE!r}"
            )
        else:
            assert BUNDLE_BADGE not in badges, (
                f"{title!r} is not a bundle product yet is served with "
                f"{BUNDLE_BADGE!r}"
            )
        rating = payload.get("rating") or {}
        assert str(rating.get("score")) == score, (
            f"{title!r} is served rated {rating.get('score')!r}, expected {score!r}"
        )
        assert rating.get("count") == count, (
            f"{title!r} is served with {rating.get('count')!r} review(s), expected "
            f"{count}"
        )


def test_the_catalogue_carries_several_maker_names(anon_client, store):
    makers = {row.get("maker") for row in store.rows("products")}
    makers.discard(None)
    assert len(makers) >= 5, (
        f"the catalogue carries {len(makers)} distinct maker(s): {sorted(makers)}. It "
        f"carries at least five, VOLARI among them"
    )
    assert "VOLARI" in makers, (
        f"the catalogue carries no product made by 'VOLARI'; makers: {sorted(makers)}"
    )
    titles = {row.get("title") for row in store.rows("products")}
    for title in OTHER_MAKER_TITLES:
        assert title in titles, (
            f"the catalogue holds no product titled {title!r}. The card must survive a "
            f"title that does not begin with the shop's own name"
        )
    for row in store.rows("products"):
        maker = row.get("maker") or ""
        if maker and not str(row.get("title", "")).startswith(maker):
            break
    else:
        raise AssertionError(
            "every product title begins with its own maker, so the maker could have "
            "been parsed out of the title. The catalogue holds titles where it cannot"
        )


def test_sort_and_filter_survive_in_the_address(anon_client):
    plain = collection(anon_client)
    filtered = collection(anon_client, availability="in_stock")
    assert filtered["count"] == IN_STOCK_COUNT, (
        f"the in-stock facet selection yields count={filtered['count']!r}, expected "
        f"{IN_STOCK_COUNT}"
    )
    assert filtered["count"] < plain["count"], (
        f"selecting a facet did not reduce the result: {filtered['count']} against "
        f"{plain['count']}"
    )
    low = collection(anon_client, sort_by="Price, low to high")
    high = collection(anon_client, sort_by="Price, high to low")
    low_prices = [row["price"]["amount_minor"] for row in low["products"]]
    high_prices = [row["price"]["amount_minor"] for row in high["products"]]
    assert low_prices == sorted(low_prices), (
        f"'Price, low to high' served {low_prices[:6]}, which is not ascending"
    )
    assert high_prices == sorted(high_prices, reverse=True), (
        f"'Price, high to low' served {high_prices[:6]}, which is not descending"
    )
    assert low_prices[0] <= high_prices[0], (
        "the two price sorts served the same first product, so the sort parameter was "
        "ignored"
    )


def test_every_sort_option_is_accepted(anon_client):
    for option in SORT_OPTIONS:
        payload = collection(anon_client, sort_by=option)
        assert payload["count"] == CATALOGUE_TOTAL, (
            f"sorting by {option!r} changed the result count to "
            f"{payload['count']!r}; a sort reorders without filtering"
        )


def test_pagination_is_numbered_and_addressable(anon_client):
    first = collection(anon_client, page=1)
    seventh = collection(anon_client, page=7)
    last = collection(anon_client, page=PAGE_COUNT)
    first_handles = [row["handle"] for row in first["products"]]
    seventh_handles = [row["handle"] for row in seventh["products"]]
    assert first_handles != seventh_handles, (
        "page one and page seven served the same products, so the page parameter was "
        "ignored"
    )
    assert not set(first_handles) & set(seventh_handles), (
        f"page one and page seven overlap on "
        f"{sorted(set(first_handles) & set(seventh_handles))}"
    )
    assert 1 <= len(last["products"]) <= PAGE_SIZE, (
        f"the last page carries {len(last['products'])} product(s), expected between "
        f"1 and {PAGE_SIZE}"
    )
    again = collection(anon_client, page=7)
    assert [row["handle"] for row in again["products"]] == seventh_handles, (
        "two identical requests for page seven served different products"
    )


def test_repeated_identical_collection_request_is_stable(anon_client):
    first = collection(anon_client, availability="in_stock",
                       sort_by="Alphabetically, A-Z", page=2)
    second = collection(anon_client, availability="in_stock",
                        sort_by="Alphabetically, A-Z", page=2)
    assert first["products"] == second["products"], (
        "two identical requests for the same collection, facet, sort and page served "
        "different products"
    )
    assert first["facets"] == second["facets"], (
        f"two identical requests served different facet counts: {first['facets']} then "
        f"{second['facets']}"
    )


def test_product_payload_carries_its_colourways_with_their_own_prices(anon_client):
    payload = product(anon_client, REBEL_HANDLE)
    for field in PRODUCT_FIELDS:
        assert field in payload, (
            f"{REBEL_HANDLE!r} is served without a {field!r} key; it carries "
            f"{sorted(payload)}"
        )
    assert payload["title"] == REBEL_TITLE, (
        f"{REBEL_HANDLE!r} is served titled {payload['title']!r}, expected "
        f"{REBEL_TITLE!r}"
    )
    assert payload["option_name"] == REBEL_OPTION_NAME, (
        f"{REBEL_HANDLE!r} is served with option_name={payload['option_name']!r}, "
        f"expected {REBEL_OPTION_NAME!r}"
    )
    assert payload["compare_at"]["amount_minor"] == REBEL_COMPARE_MINOR, (
        f"{REBEL_HANDLE!r} is served with a compare-at of "
        f"{payload['compare_at']['amount_minor']!r} minor units, expected "
        f"{REBEL_COMPARE_MINOR}"
    )
    assert payload.get("offer_line") == REBEL_OFFER_LINE, (
        f"{REBEL_HANDLE!r} is served with offer_line={payload.get('offer_line')!r}, "
        f"expected {REBEL_OFFER_LINE!r}"
    )
    served = {v["option_value"]: v for v in payload["variants"]}
    assert len(served) == len(REBEL_COLOURWAYS), (
        f"{REBEL_HANDLE!r} is served with {len(served)} colourway(s), expected "
        f"{len(REBEL_COLOURWAYS)}: {sorted(served)}"
    )
    for value, price, available in REBEL_COLOURWAYS:
        variant = served.get(value)
        assert variant is not None, (
            f"{REBEL_HANDLE!r} is served with no colourway {value!r}; served: "
            f"{sorted(served)}"
        )
        for field in VARIANT_FIELDS:
            assert field in variant, (
                f"colourway {value!r} carries no {field!r} key; it carries "
                f"{sorted(variant)}"
            )
        assert variant["price"]["amount_minor"] == price, (
            f"colourway {value!r} is served at "
            f"{variant['price']['amount_minor']!r} minor units, expected {price}"
        )
        assert bool(variant["available"]) is available, (
            f"colourway {value!r} is served available={variant['available']!r}, "
            f"expected {available}"
        )


def test_unavailable_colourway_is_served_rather_than_removed(anon_client):
    payload = product(anon_client, REBEL_HANDLE)
    served = {v["option_value"]: v for v in payload["variants"]}
    sold_out = [value for value, _p, available in REBEL_COLOURWAYS if not available]
    for value in sold_out:
        variant = served.get(value)
        assert variant is not None, (
            f"the unavailable colourway {value!r} was dropped from the payload. An "
            f"unavailable swatch stays selectable so its price and image can be seen"
        )
        assert variant["price"]["amount_minor"] > 0, (
            f"the unavailable colourway {value!r} is served without a price: "
            f"{variant['price']!r}"
        )
        assert variant.get("media_seed"), (
            f"the unavailable colourway {value!r} is served without a media seed, so "
            f"it has no image to show"
        )
    still_available = [v for v in payload["variants"] if v.get("available")]
    assert len(still_available) == len(REBEL_COLOURWAYS) - len(sold_out), (
        f"one unavailable colourway disabled the rest of the grid: "
        f"{len(still_available)} available, expected "
        f"{len(REBEL_COLOURWAYS) - len(sold_out)}"
    )


def test_a_product_with_two_priced_colourways_is_served_intact(anon_client, store):
    row = store.one("products", title=BUSINESS_TITLE)
    assert row is not None, f"no product titled {BUSINESS_TITLE!r} is stored"
    payload = product(anon_client, row["handle"])
    served = {v["option_value"]: v["price"]["amount_minor"]
              for v in payload["variants"]}
    for value, price, _available in BUSINESS_COLOURWAYS:
        assert served.get(value) == price, (
            f"{BUSINESS_TITLE!r} colourway {value!r} is served at {served.get(value)!r} "
            f"minor units, expected {price}"
        )


def test_prices_convert_by_one_rate_in_one_pass(anon_client):
    assert DISPLAY_CURRENCIES[0].lower() == STORE_CURRENCY, (
        f"the first display currency is {DISPLAY_CURRENCIES[0]!r} against a store "
        f"currency of {STORE_CURRENCY!r}; the store currency is the default display"
    )
    usd = product(anon_client, REBEL_HANDLE, currency="USD")
    inr = product(anon_client, REBEL_HANDLE, currency="INR")
    usd_variant = usd["variants"][0]
    inr_variant = next(v for v in inr["variants"]
                       if v["option_value"] == usd_variant["option_value"])
    assert usd_variant["price"]["amount_minor"] == WORKED_MINOR, (
        f"the first colourway is served at "
        f"{usd_variant['price']['amount_minor']!r} minor units, expected "
        f"{WORKED_MINOR}"
    )
    assert usd_variant["price"]["formatted"].startswith(USD_PREFIX), (
        f"the USD rendering is {usd_variant['price']['formatted']!r}, which does not "
        f"open with {USD_PREFIX!r}"
    )
    assert inr_variant["price"]["formatted"].startswith(INR_PREFIX), (
        f"the INR rendering is {inr_variant['price']['formatted']!r}, which does not "
        f"open with {INR_PREFIX!r}"
    )
    assert usd_variant["price"]["formatted"] == WORKED_USD, (
        f"the first colourway renders as {usd_variant['price']['formatted']!r} in USD, "
        f"expected {WORKED_USD!r}"
    )
    assert inr_variant["price"]["formatted"] == WORKED_INR, (
        f"the first colourway renders as {inr_variant['price']['formatted']!r} in INR, "
        f"expected {WORKED_INR!r} at a rate of {INR_RATE}"
    )
    usd_compare = usd["compare_at"]["amount_minor"] / 100
    inr_compare_text = inr["compare_at"]["formatted"]
    want_compare = f"{usd_compare * INR_RATE:,.2f}"
    assert want_compare in inr_compare_text, (
        f"the struck-through original renders as {inr_compare_text!r} in INR. It "
        f"converts by the same rate in the same pass as the sale price, so it reads "
        f"{want_compare}"
    )


def test_one_product_costs_the_same_on_two_surfaces(anon_client, store):
    row = store.one("products", title=REBEL_TITLE)
    assert row is not None, f"no product titled {REBEL_TITLE!r} is stored"
    detail = product(anon_client, row["handle"], currency="INR")
    catalogue = {}
    for page in range(1, PAGE_COUNT + 1):
        catalogue.update({p["title"]: p for p in
                          collection(anon_client, page=page,
                                     currency="INR")["products"]})
        if REBEL_TITLE in catalogue:
            break
    card = catalogue.get(REBEL_TITLE)
    assert card is not None, (
        f"no card titled {REBEL_TITLE!r} was served across the catch-all"
    )
    detail_cheapest = min(v["price"]["amount_minor"] for v in detail["variants"]
                          if v.get("available"))
    assert card["price"]["amount_minor"] == detail_cheapest, (
        f"{REBEL_TITLE!r} is served at {card['price']['amount_minor']!r} on the "
        f"collection and {detail_cheapest!r} on its own route, in the same currency at "
        f"the same moment"
    )
    assert card["price"]["formatted"] == next(
        v["price"]["formatted"] for v in detail["variants"]
        if v["price"]["amount_minor"] == detail_cheapest), (
        f"{REBEL_TITLE!r} renders as {card['price']['formatted']!r} on the collection "
        f"and differently on its own route"
    )


def test_cart_unit_count_sums_quantities_rather_than_lines(fresh_client, anon_client):
    rebel = product(anon_client, REBEL_HANDLE)
    first = first_available_variant(rebel)
    body = add_line(fresh_client, first["id"], 2)
    assert body["unit_count"] == 2, (
        f"one line at quantity two gives unit_count={body['unit_count']!r}, expected 2. "
        f"The count sums quantities rather than counting lines"
    )
    assert len(body["lines"]) == 1, (
        f"one add created {len(body['lines'])} line(s), expected 1"
    )
    other = next(v for v in rebel["variants"]
                 if v.get("available") and v["id"] != first["id"])
    body = add_line(fresh_client, other["id"], 1)
    assert body["unit_count"] == 3, (
        f"a second colourway at quantity one gives unit_count={body['unit_count']!r}, "
        f"expected 3"
    )
    assert len(body["lines"]) == 2, (
        f"two colourways created {len(body['lines'])} line(s), expected 2"
    )
    for field in CART_FIELDS:
        assert field in body, (
            f"the cart carries no {field!r} key; it carries {sorted(body)}"
        )
    for line in body["lines"]:
        for field in CART_LINE_FIELDS:
            assert field in line, (
                f"a cart line carries no {field!r} key; it carries {sorted(line)}"
            )


def test_cart_line_order_is_insertion_order(fresh_client, anon_client):
    payload = product(anon_client, REBEL_HANDLE)
    available = [v for v in payload["variants"] if v.get("available")][:3]
    assert len(available) >= 3, (
        f"{REBEL_HANDLE!r} serves {len(available)} available colourway(s), expected at "
        f"least 3"
    )
    for variant in available:
        add_line(fresh_client, variant["id"], 1)
    before = [line["variant_id"] for line in cart(fresh_client)["lines"]]
    second_key = cart(fresh_client)["lines"][1]["key"]
    response = fresh_client.patch(f"/cart/lines/{second_key}", json={"quantity": 4})
    assert response.status_code == 200, (
        f"PATCH {api_base()}/cart/lines/{second_key} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    after = [line["variant_id"] for line in response.json()["lines"]]
    assert after == before, (
        f"incrementing the second line reordered the cart: {before} became {after}. "
        f"Line order is insertion order and never changes"
    )


def test_cart_survives_a_reload_on_the_same_token(fresh_client, anon_client):
    payload = product(anon_client, REBEL_HANDLE)
    variant = first_available_variant(payload)
    added = add_line(fresh_client, variant["id"], 2)
    token = added["token"]
    assert token, "the cart was returned without a token, so nothing can carry it"
    with httpx.Client(base_url=api_base(), timeout=30.0,
                      cookies=fresh_client.cookies) as revisit:
        again = cart(revisit)
    assert again["token"] == token, (
        f"a fresh client on the same session read cart token {again['token']!r}, "
        f"expected {token!r}"
    )
    assert again["unit_count"] == added["unit_count"], (
        f"the cart read back {again['unit_count']!r} unit(s), expected "
        f"{added['unit_count']!r}. The cart survives a reload"
    )


def test_upsell_line_is_a_real_product_record(store, anon_client):
    row = store.product(UPSELL_HANDLE)
    assert row is not None, (
        f"the products table holds no row handled {UPSELL_HANDLE!r}"
    )
    assert row.get("title") == UPSELL_TITLE, (
        f"the upsell row is titled {row.get('title')!r}, expected {UPSELL_TITLE!r}"
    )
    assert row.get("description") == UPSELL_DESCRIPTION, (
        f"the upsell row carries description={row.get('description')!r}, expected "
        f"{UPSELL_DESCRIPTION!r}"
    )
    variants = store.variants_of(UPSELL_HANDLE)
    assert variants, f"{UPSELL_HANDLE!r} holds no variant row"
    assert int(variants[0]["price_minor"]) == UPSELL_PRICE_MINOR, (
        f"the upsell is stored at {variants[0]['price_minor']!r} minor units, expected "
        f"{UPSELL_PRICE_MINOR}"
    )
    assert int(variants[0]["compare_at_minor"]) == UPSELL_COMPARE_MINOR, (
        f"the upsell is stored with a compare-at of "
        f"{variants[0]['compare_at_minor']!r}, expected {UPSELL_COMPARE_MINOR}"
    )
    payload = product(anon_client, UPSELL_HANDLE)
    assert any(b == SALE_BADGE for b in payload.get("badges") or []), (
        f"the upsell is served with badges {payload.get('badges')!r}; it appears in the "
        f"catch-all as an ordinary product with a Sale badge"
    )


def test_upsell_is_never_the_only_line_in_a_cart(fresh_client, store):
    variants = store.variants_of(UPSELL_HANDLE)
    response = fresh_client.post("/cart/lines",
                                 json={"variant_id": variants[0]["id"],
                                       "quantity": 1})
    if response.status_code in (200, 201):
        body = response.json()
        assert body["unit_count"] == 0 or len(body["lines"]) == 0, (
            f"adding the upsell to an empty cart produced a cart of "
            f"{len(body['lines'])} line(s). A cart holding nothing but the upsell is an "
            f"empty cart with a fee"
        )
    else:
        assert 400 <= response.status_code < 500, (
            f"adding the upsell to an empty cart returned {response.status_code}; it is "
            f"refused as an invalid request rather than with a server error: "
            f"{response.text[:400]}"
        )


def test_catalogue_write_is_denied_and_the_rows_are_unchanged(anon_client, store):
    before = {table: store.count(table) for table in CATALOGUE_TABLES}
    before_row = store.product(REBEL_HANDLE)
    for method, path in WRITE_PROBES:
        response = anon_client.request(
            method, path,
            json={"handle": "phantom", "title": "Phantom", "maker": "PHANTOM",
                  "available": True},
        )
        assert 400 <= response.status_code < 500, (
            f"{method} {api_base()}{path} returned {response.status_code}. The "
            f"catalogue is read-only at the server, so a write is refused as an invalid "
            f"request, never served and never a server error: {response.text[:400]}"
        )
    for table, count in before.items():
        assert store.count(table) == count, (
            f"a refused write changed the {table} table from {count} row(s) to "
            f"{store.count(table)}"
        )
    assert store.product(REBEL_HANDLE) == before_row, (
        f"a refused write changed the stored {REBEL_HANDLE!r} row"
    )


def test_security_headers_are_present_on_every_response(site):
    probes = [HOME_ROUTE, "/api/health", "/api" + CATCH_ALL_ROUTE,
              SITEMAP_ROUTE, ROBOTS_ROUTE]
    for path in probes:
        response = site.get(path)
        lowered = {k.lower(): v for k, v in response.headers.items()}
        for header in SECURITY_HEADER_NAMES:
            assert header in lowered, (
                f"GET {app_url()}{path} answered without the {header!r} security "
                f"header. Headers present: {sorted(lowered)}"
            )
        assert lowered["x-content-type-options"].strip().lower() == NOSNIFF_VALUE, (
            f"GET {app_url()}{path} answered with x-content-type-options="
            f"{lowered['x-content-type-options']!r}, expected {NOSNIFF_VALUE!r}"
        )


def test_checkout_summary_equals_the_cart_line_for_line(fresh_client, anon_client):
    payload = product(anon_client, REBEL_HANDLE)
    variant = first_available_variant(payload)
    add_line(fresh_client, variant["id"], 2)
    other = next(v for v in payload["variants"]
                 if v.get("available") and v["id"] != variant["id"])
    before = add_line(fresh_client, other["id"], 1)
    address = probe_email()
    response = fresh_client.post("/checkout", json={"email": address})
    assert response.status_code in (200, 201), (
        f"POST {api_base()}/checkout returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    summary = response.json()
    for field in CHECKOUT_FIELDS:
        assert field in summary, (
            f"the checkout summary carries no {field!r} key; it carries "
            f"{sorted(summary)}"
        )
    assert summary["unit_count"] == before["unit_count"], (
        f"the checkout summary reports {summary['unit_count']!r} unit(s) against the "
        f"cart's {before['unit_count']!r}. The summary is the cart, with no additions "
        f"and no omissions"
    )
    assert len(summary["lines"]) == len(before["lines"]), (
        f"the checkout summary lists {len(summary['lines'])} line(s) against the cart's "
        f"{len(before['lines'])}"
    )
    cart_keys = sorted(line["variant_id"] for line in before["lines"])
    summary_keys = sorted(line["variant_id"] for line in summary["lines"])
    assert cart_keys == summary_keys, (
        f"the checkout summary lists variants {summary_keys} against the cart's "
        f"{cart_keys}"
    )
    assert summary["total"]["amount_minor"] == before["subtotal"]["amount_minor"], (
        f"the checkout total is {summary['total']['amount_minor']!r} minor units "
        f"against the cart subtotal of {before['subtotal']['amount_minor']!r}"
    )


def test_checkout_creates_exactly_one_billing_account_for_the_order(
        fresh_client, anon_client, payments, store):
    payload = product(anon_client, REBEL_HANDLE)
    variant = first_available_variant(payload)
    add_line(fresh_client, variant["id"], 1)
    address = probe_email()
    response = fresh_client.post("/checkout", json={"email": address})
    assert response.status_code in (200, 201), (
        f"POST {api_base()}/checkout returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    reference = response.json()["reference"]
    assert reference, "the checkout returned no order reference"
    account = poll_account(payments, reference)
    assert account is not None, (
        f"no account in the billing tenant carries externalKey={reference!r}. The "
        f"account must exist as a real record in killbill; an order the app records "
        f"without it is a contract violation"
    )
    assert str(account.get("currency", "")).upper() in ("USD", "INR"), (
        f"the billing account for {reference!r} carries currency="
        f"{account.get('currency')!r}, expected the cart's display currency in uppercase"
    )
    stored = store.order(reference)
    assert stored is not None, (
        f"the orders table holds no row referenced {reference!r}"
    )
    direct = find_account(payments, reference)
    assert direct is not None, (
        f"the billing tenant serves no account under externalKey {reference!r} when "
        f"asked for it by key"
    )
    matching = [a for a in payments.accounts()
                if a.get("externalKey") == reference]
    assert len(matching) == 1, (
        f"the billing tenant holds {len(matching)} account(s) under externalKey "
        f"{reference!r}, expected exactly 1"
    )


def test_resubmitting_an_order_creates_no_second_billing_account(
        fresh_client, anon_client, payments):
    payload = product(anon_client, REBEL_HANDLE)
    variant = first_available_variant(payload)
    add_line(fresh_client, variant["id"], 1)
    address = probe_email()
    first = fresh_client.post("/checkout", json={"email": address})
    assert first.status_code in (200, 201), (
        f"the first checkout returned {first.status_code}: {first.text[:400]}"
    )
    reference = first.json()["reference"]
    assert poll_account(payments, reference) is not None, (
        f"the first checkout created no billing account under {reference!r}"
    )
    second = fresh_client.post("/checkout", json={"email": address,
                                                  "reference": reference})
    assert second.status_code < 500, (
        f"re-submitting order {reference!r} returned {second.status_code}. A repeat is "
        f"refused by the billing store's own unique-key conflict, so the app reports "
        f"the existing order rather than failing: {second.text[:400]}"
    )
    matching = [a for a in payments.accounts()
                if a.get("externalKey") == reference]
    assert len(matching) == 1, (
        f"re-submitting order {reference!r} left {len(matching)} account(s) under that "
        f"externalKey, expected exactly 1. externalKey is unique per tenant, so the "
        f"store refuses the repeat rather than an application guard"
    )


def test_an_order_reference_the_shop_never_issued_has_no_billing_account(payments):
    invented = probe_reference()
    assert find_account(payments, invented) is None, (
        f"the billing tenant holds an account under externalKey {invented!r}, a "
        f"reference no checkout ever issued. Accounts are opened by a completed order "
        f"and by nothing else"
    )


def test_completed_checkout_clears_the_cart(fresh_client, anon_client):
    payload = product(anon_client, REBEL_HANDLE)
    variant = first_available_variant(payload)
    add_line(fresh_client, variant["id"], 1)
    address = probe_email()
    response = fresh_client.post("/checkout", json={"email": address})
    assert response.status_code in (200, 201), (
        f"POST {api_base()}/checkout returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    after = cart(fresh_client)
    assert after["unit_count"] == 0, (
        f"the cart holds {after['unit_count']!r} unit(s) after a completed order, "
        f"expected 0"
    )
    assert after["lines"] == [], (
        f"the cart holds {len(after['lines'])} line(s) after a completed order"
    )


def test_signup_delivers_the_discount_code_by_mail(fresh_client, inbox, store):
    address = probe_email()
    response = fresh_client.post("/newsletter", json={"email": address})
    assert response.status_code in (200, 201), (
        f"POST {api_base()}/newsletter returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    message = find_message(inbox, address, SIGNUP_SUBJECT_PREFIX)
    assert message is not None, (
        f"no message addressed to {address!r} with a subject beginning "
        f"{SIGNUP_SUBJECT_PREFIX!r} reached the inbox. The code arrives as a real "
        f"message; a row saying mail was sent is not mail"
    )
    assert message.subject.startswith(SIGNUP_SUBJECT_PREFIX), (
        f"the signup message carries the subject {message.subject!r}, which does not "
        f"begin {SIGNUP_SUBJECT_PREFIX!r}"
    )
    assert message.subject == SIGNUP_SUBJECT, (
        f"the signup message carries the subject {message.subject!r}, expected "
        f"{SIGNUP_SUBJECT!r}"
    )
    assert [a.lower() for a in message.to] == [address.lower()], (
        f"the signup message is addressed to {message.to!r}, expected {[address]} "
        f"alone, with no cc and no bcc"
    )
    body = message.body or ""
    assert SIGNUP_CODE in body or SIGNUP_CODE in message.subject, (
        f"the signup message body names neither the code nor the store: {body[:200]!r}"
    )
    stored = store.one("newsletter_signups", email=address)
    assert stored is not None, (
        f"the newsletter_signups table holds no row for {address!r}"
    )


def test_rejected_signup_sends_no_mail(fresh_client, inbox):
    address = probe_email()
    first = fresh_client.post("/newsletter", json={"email": address})
    assert first.status_code in (200, 201), (
        f"the first signup returned {first.status_code}: {first.text[:400]}"
    )
    assert find_message(inbox, address, SIGNUP_SUBJECT_PREFIX) is not None, (
        f"the first signup for {address!r} delivered no message"
    )
    before = inbox.count(address)
    repeat = fresh_client.post("/newsletter", json={"email": address})
    assert 400 <= repeat.status_code < 500, (
        f"repeating a signup for {address!r} returned {repeat.status_code}; a repeat of "
        f"an address already on the list is refused: {repeat.text[:400]}"
    )
    malformed = fresh_client.post("/newsletter", json={"email": "not-an-address"})
    assert 400 <= malformed.status_code < 500, (
        f"a malformed address returned {malformed.status_code}, expected a client "
        f"error: {malformed.text[:400]}"
    )
    assert inbox.count(address) == before, (
        f"a rejected signup delivered mail: {address!r} went from {before} message(s) "
        f"to {inbox.count(address)}"
    )


def test_a_decoy_field_submission_is_refused_and_writes_nothing(fresh_client, store):
    address = probe_email()
    before = store.count("newsletter_signups")
    response = fresh_client.post("/newsletter",
                                 json={"email": address, "company": "bot"})
    assert 400 <= response.status_code < 500, (
        f"a signup carrying a filled unattended decoy field returned "
        f"{response.status_code}, expected a client error: {response.text[:400]}"
    )
    assert store.count("newsletter_signups") == before, (
        f"a refused submission wrote a row: newsletter_signups went from {before} to "
        f"{store.count('newsletter_signups')}"
    )
    assert store.one("newsletter_signups", email=address) is None, (
        f"a refused submission stored {address!r}"
    )


def test_a_form_submitted_repeatedly_is_refused(fresh_client):
    outcomes = []
    for _ in range(6):
        response = fresh_client.post("/contact",
                                     json={"name": "Probe",
                                           "email": probe_email(),
                                           "message": "Probe message."})
        outcomes.append(response.status_code)
    assert any(400 <= code < 500 for code in outcomes), (
        f"six contact submissions in quick succession from one session all answered "
        f"{outcomes}. The same form submitted repeatedly in quick succession is refused"
    )


def test_contact_message_is_recorded_without_sending_mail(fresh_client, inbox):
    address = probe_email()
    before = inbox.count(address)
    response = fresh_client.post("/contact",
                                 json={"name": "Probe",
                                       "email": address,
                                       "message": "A question about the warranty."})
    assert response.status_code < 500, (
        f"POST {api_base()}/contact returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    assert inbox.count(address) == before, (
        f"the contact form delivered mail to {address!r}: {before} message(s) became "
        f"{inbox.count(address)}. The contact form records the message and sends none"
    )


def test_invalid_facet_value_is_refused(anon_client):
    response = anon_client.get(f"/collections/{CATCH_ALL_HANDLE}",
                               params={"availability": "levitating"})
    assert 400 <= response.status_code < 500, (
        f"an availability value outside the declared set returned "
        f"{response.status_code}, expected a client error rather than a silent ignore "
        f"or a server error: {response.text[:400]}"
    )


def test_unknown_collection_and_product_answer_as_not_found(anon_client):
    for path in (f"/collections/pocket-sundials", "/products/no-such-watch"):
        response = anon_client.get(path)
        assert response.status_code == 404, (
            f"GET {api_base()}{path} returned {response.status_code}, expected 404"
        )


def test_page_views_are_recorded_and_readable(site, anon_client):
    site.get(HOME_ROUTE)
    site.get(CART_ROUTE)
    response = anon_client.get("/page-views")
    assert response.status_code == 200, (
        f"GET {api_base()}/page-views returned {response.status_code}, expected 200: "
        f"{response.text[:400]}"
    )
    rows = response.json()
    assert isinstance(rows, list) and rows, (
        f"GET {api_base()}/page-views must return a non-empty top-level JSON array, got "
        f"{type(rows).__name__}: {response.text[:400]}"
    )
    for row in rows[:5]:
        for field in ("route", "viewed_at"):
            assert field in row, (
                f"a page-view row carries no {field!r} key; it carries {sorted(row)}"
            )
    stamps = [row["viewed_at"] for row in rows]
    assert stamps == sorted(stamps, reverse=True), (
        f"the page-view rows are not newest first: {stamps[:5]}"
    )


def test_sitemap_lists_every_public_route(site):
    response = site.get(SITEMAP_ROUTE)
    assert response.status_code == 200, (
        f"GET {app_url()}{SITEMAP_ROUTE} returned {response.status_code}, expected 200: "
        f"{response.text[:400]}"
    )
    body = response.text
    for route in PUBLIC_ROUTES:
        assert route in body, (
            f"the sitemap does not list the public route {route!r}. First 400 "
            f"characters: {body[:400]}"
        )


def test_home_page_names_the_shop(site):
    response = site.get(HOME_ROUTE)
    assert response.status_code == 200, (
        f"GET {app_url()}{HOME_ROUTE} returned {response.status_code}, expected 200"
    )
    assert BRAND_FULL in response.text, (
        f"the home page does not name {BRAND_FULL!r} anywhere in what it serves"
    )


def test_robots_file_names_the_sitemap(site):
    response = site.get(ROBOTS_ROUTE)
    assert response.status_code == 200, (
        f"GET {app_url()}{ROBOTS_ROUTE} returned {response.status_code}, expected 200: "
        f"{response.text[:400]}"
    )
    assert SITEMAP_ROUTE in response.text, (
        f"the robots file does not name {SITEMAP_ROUTE!r}. Body: "
        f"{response.text[:400]}"
    )


def test_every_public_route_is_served(site):
    for route in PUBLIC_ROUTES + (CHECKOUT_ROUTE,):
        response = site.get(route)
        assert response.status_code == 200, (
            f"GET {app_url()}{route} returned {response.status_code}, expected 200: "
            f"{response.text[:200]}"
        )
    for route in POLICY_ROUTES + AUTHORED_PAGE_ROUTES + (BLOG_ROUTE,):
        assert route in PUBLIC_ROUTES, (
            f"the policy, authored and journal route {route!r} is not among the routes "
            f"the sitemap is checked against"
        )


def test_account_handoff_route_leads_away_rather_than_to_a_dead_end(site):
    response = site.get(ACCOUNT_HANDOFF_ROUTE)
    assert response.status_code in (200, 301, 302, 303, 307, 308), (
        f"GET {app_url()}{ACCOUNT_HANDOFF_ROUTE} returned {response.status_code}. The "
        f"account link hands the visitor off rather than opening a sign-in the shop "
        f"does not run: {response.text[:200]}"
    )


def test_app_root_carries_the_readme_the_reserved_directories_and_the_request_log(
        site):
    assert os.path.isdir(APP_ROOT), (
        f"the app root {APP_ROOT} does not exist"
    )
    assert os.path.isfile(USER_README_PATH), (
        f"{USER_README_PATH} does not exist. The deployment contract requires login "
        f"credentials, or an explicit statement that there are none, to be written there"
    )
    with open(USER_README_PATH, encoding="utf-8", errors="replace") as fh:
        readme = fh.read()
    assert readme.strip(), f"{USER_README_PATH} is empty"
    for directory in RESERVED_DIRECTORIES:
        assert os.path.isdir(directory), (
            f"the reserved directory {directory} does not exist at the app root"
        )
    site.get("/api/health")
    assert os.path.isfile(REQUEST_LOG_PATH), (
        f"{REQUEST_LOG_PATH} does not exist after a request was served"
    )
    with open(REQUEST_LOG_PATH, encoding="utf-8", errors="replace") as fh:
        lines = [ln for ln in fh.read().splitlines() if ln.strip()]
    assert lines, f"{REQUEST_LOG_PATH} holds no record after a request was served"
    record = json.loads(lines[-1])
    for key in REQUEST_LOG_KEYS:
        assert key in record, (
            f"the last record in {REQUEST_LOG_PATH} carries no {key!r} key; it carries "
            f"{sorted(record)}"
        )
