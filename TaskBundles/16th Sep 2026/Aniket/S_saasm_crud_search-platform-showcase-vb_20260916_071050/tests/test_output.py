from __future__ import annotations

import base64
import hashlib
import hmac
import re
import urllib.parse
import uuid

import httpx

from conftest import (
    ACCORDION_ITEMS, AI_MODE, ANALYST_EMAIL, ANALYST_HEADING,
    ASSIST_ACTIONS, ASSIST_ATTRIBUTION, ASSIST_TITLE, BADGES, BARE_ROUTES,
    BLOCK_BUTTON, BLOCK_TERMS, CAPABILITY_BUTTON, CATALOG_CELLS,
    CATALOG_INDEX, CHROME_ROUTES, CLEAR_FILTERS, CLOSING_BUTTONS,
    CLOSING_HEADING, CONTRAST_BODY_RATIO, CORPUS_PASSWORD, COUNTRY_PLACEHOLDER,
    CURRENCY, CUSTOMERS_BUTTON, CUSTOMERS_HEADING, CUSTOM_RANKING,
    DEMO_FIELDS, DEMO_HEADING, DEMO_KEYS, DEMO_STATUS, DEMO_SUBMIT,
    DRAWER_CLOSE, DRAWER_HEADING, FAQ_FIRST, FAQ_HEADING, FILTER_HEADING,
    FIXTURE_INDEX, FOOTER_LEGAL, FOOTER_LINKS, FOOTER_NEWSLETTER,
    FOOTER_SOCIAL_HEADING, FREE_BODY, FREE_NOTE, GEO_POINT, GRID_CATEGORIES,
    GRID_HEADING, GRID_JUMP, GRID_LIMITS, GRID_ROWS, GROW_METERING,
    GROW_RECORDS, HEADER_MENU, HEADER_PRIMARY, HEADER_SECONDARY, HERO_BUTTON,
    HERO_LEAD, HERO_LINES, HIGHLIGHT_POST_TAG, HIGHLIGHT_PRE_TAG,
    HIT_ACTION, HONESTY_FLAGS, IDEMPOTENCY_HEADER, INDUSTRY_COUNTS,
    INGEST_KEY, LANGUAGES, LOAD_MORE, NARROW_VIEWPORT, NOT_FOUND_HEADING,
    NOT_FOUND_LINKS, NOT_FOUND_NUMERAL, NOT_FOUND_SEARCH, OPERATOR_EMAIL,
    OWNER_EMAIL, PLAN_ACTIONS, PLAN_GROUPS, PLAN_NAMES, PLAN_SUBTITLES,
    PRICING_CHOOSER, PRICING_HEADING, PRODUCTS_EYEBROW, PRODUCTS_SECTION,
    PROMO_SLIDES, PUBLIC_ROUTES, QUERY_ID_LENGTH, RANK_ORDER, RANK_POPULARITY,
    RECORD_PRICE_MINOR, REGION_COUNTS, RESULTS_HEADING, ROTATING_PROMPT,
    SEARCH_PLACEHOLDER, SECOND_APP_SLUG, SECOND_OWNER_EMAIL,
    SHIRT_ATTRIBUTE, SHIRT_GROUPS, SHIRT_INDEX, SHIRT_PAGES,
    SHIRT_RED_GROUPS, SHIRT_RED_RECORDS, SHOW_ALL, SITE_INDEX,
    SITE_SEARCH_KEY, SNIPPET_ELLIPSIS, SOLUTIONS_HEADING, SOLUTION_TITLES,
    SOURCE_COUNTS, SOURCE_FACET, SOURCE_VALUES, STAT_ONE, STAT_ONE_LABEL,
    STAT_TWO, STAT_TWO_LABEL, STORY_FACETS, STORY_INDEX, STORY_PLACEHOLDER,
    STORY_SEARCH_KEY, STORY_TITLES, SUGGESTED_QUESTIONS, SUGGESTION_BUTTONS,
    SUGGESTIONS_HEADING, TEXT_FIXTURES, TOOLS_HEADING, TRUST_ROW_ONE,
    TRUST_ROW_TWO, TYPE_FAMILIES, UNIT_PRICE_MINOR, USE_CASES_HEADING,
    UTILITY_ITEMS, VIDEO_BUTTON, WORDMARKS, anchor, api_key, bearer,
    demo_payload, facet_counts, object_ids, poll, probe_email, probe_token,
    search, settle, sign_in,
)

SECRET_NEEDLES = ("postgresql://", "DB_ADMIN_URL", "deku-local-dev",
                  "ik_demo_", "deku_admin")


def _text(response: httpx.Response) -> str:
    return response.text or ""


def _json(response: httpx.Response, label: str):
    assert response.headers.get("content-type", "").startswith("application/json"), (
        anchor(f"{label} did not answer JSON", response))
    return response.json()


def _ok(response: httpx.Response, label: str):
    assert response.status_code in (200, 201), anchor(label, response)
    return _json(response, label)


def _rejected(response: httpx.Response, label: str) -> None:
    assert 400 <= response.status_code < 500, anchor(
        f"{label} was expected to be refused as a client error", response)


def test_health_and_deployment_contract(client, site, app_url):
    r = client.get("/health")
    assert r.status_code == 200, anchor("health route", r)

    home = site.get("/")
    assert home.status_code == 200, anchor("home route", home)
    assert app_url.startswith("http"), f"APP_PUBLIC_URL is not an address: {app_url!r}"
    assert "127.0.0.1" not in app_url, (
        f"the app answers on loopback only at {app_url!r}, so it is unreachable "
        f"from outside the container")


def test_public_routes_render_before_script(site):
    for route in PUBLIC_ROUTES:
        r = site.get(route)
        assert r.status_code == 200, anchor(f"public route {route}", r)
        body = _text(r)
        for entry in HEADER_MENU:
            assert entry in body, (
                f"public route {route} answered {r.status_code} and its served "
                f"document omits the header entry {entry!r}; body starts "
                f"{body[:200]!r}")
        assert SEARCH_PLACEHOLDER in body or route == "/customers", (
            f"public route {route} omits the header search placeholder "
            f"{SEARCH_PLACEHOLDER!r}; body starts {body[:200]!r}")


def test_chrome_carries_promotion_utility_and_footer(site):
    for route in CHROME_ROUTES:
        body = _text(site.get(route))
        for label, message, action in PROMO_SLIDES:
            assert label in body, f"{route} omits the promotion label {label!r}"
            assert message in body, f"{route} omits the promotion message {message!r}"
            assert action in body, f"{route} omits the promotion action {action!r}"
        for item in UTILITY_ITEMS:
            assert item in body, f"{route} omits the utility item {item!r}"
        for language in LANGUAGES:
            assert language in body, f"{route} omits the language {language!r}"
        assert HEADER_SECONDARY in body, f"{route} omits {HEADER_SECONDARY!r}"
        assert HEADER_PRIMARY in body, f"{route} omits {HEADER_PRIMARY!r}"
        for link in FOOTER_LINKS:
            assert link in body, f"{route} omits the footer link {link!r}"
        assert FOOTER_SOCIAL_HEADING in body, f"{route} omits the social heading"
        assert FOOTER_NEWSLETTER in body, f"{route} omits the newsletter line"
        for legal in FOOTER_LEGAL:
            assert legal in body, f"{route} omits the legal entry {legal!r}"
        assert DRAWER_HEADING in body, f"{route} omits {DRAWER_HEADING!r}"
        assert DRAWER_CLOSE in body, f"{route} omits {DRAWER_CLOSE!r}"


def test_bare_routes_carry_no_chrome(site):
    for route in BARE_ROUTES:
        r = site.get(route)
        assert r.status_code == 200, anchor(f"bare route {route}", r)
        body = _text(r)
        for entry in HEADER_MENU:
            assert entry not in body, (
                f"{route} is a capture route and must carry no chrome, yet its "
                f"document contains the header entry {entry!r}")
        for legal in FOOTER_LEGAL:
            assert legal not in body, (
                f"{route} is a capture route and must carry no footer, yet its "
                f"document contains the legal entry {legal!r}")


def test_meta_tags_are_unique_per_route(site):
    titles, descriptions = {}, {}
    for route in PUBLIC_ROUTES:
        body = _text(site.get(route))
        title = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
        assert title, f"{route} carries no document title"
        description = re.search(
            r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
            body, re.S | re.I)
        assert description, f"{route} carries no meta description"
        titles[route] = title.group(1).strip()
        descriptions[route] = description.group(1).strip()
    assert len(set(titles.values())) == len(titles), (
        f"two public routes share a title: {titles}")
    assert len(set(descriptions.values())) == len(descriptions), (
        f"two public routes share a description: {descriptions}")


def test_home_route_carries_its_pinned_copy(site):
    body = _text(site.get("/"))
    for line in HERO_LINES:
        assert line in body, f"the home hero omits {line!r}"
    for needle in (HERO_LEAD, HERO_BUTTON, USE_CASES_HEADING,
                   CAPABILITY_BUTTON, ANALYST_HEADING, SOLUTIONS_HEADING,
                   CUSTOMERS_HEADING, CUSTOMERS_BUTTON, CLOSING_HEADING):
        assert needle in body, f"the home route omits {needle!r}"
    for item in ACCORDION_ITEMS:
        assert item in body, f"the capability accordion omits {item!r}"
    for title in SOLUTION_TITLES:
        assert title in body, f"the solutions band omits the card title {title!r}"
    for button in CLOSING_BUTTONS:
        assert button in body, f"the closing band omits {button!r}"
    for wordmark in WORDMARKS:
        assert wordmark in body, (
            f"the customer band omits the seeded wordmark {wordmark!r}; every "
            f"wordmark is text rather than an image")


def test_products_route_carries_its_pinned_copy(site):
    body = _text(site.get("/products"))
    for needle in (PRODUCTS_EYEBROW, PRODUCTS_SECTION, BLOCK_BUTTON,
                   VIDEO_BUTTON, TOOLS_HEADING):
        assert needle in body, f"the products route omits {needle!r}"
    for term in BLOCK_TERMS:
        assert term in body, f"the first feature block omits the term {term!r}"


def test_overlay_surface_carries_its_pinned_copy(site):
    body = _text(site.get("/"))
    for needle in (FILTER_HEADING, RESULTS_HEADING, HIT_ACTION, LOAD_MORE,
                   SUGGESTIONS_HEADING, AI_MODE, ASSIST_TITLE,
                   ASSIST_ATTRIBUTION, CLEAR_FILTERS, SHOW_ALL,
                   ROTATING_PROMPT):
        assert needle in body, f"the search surface omits {needle!r}"
    for action in ASSIST_ACTIONS:
        assert action in body, f"the assistant omits the action {action!r}"
    for question in SUGGESTED_QUESTIONS:
        assert question in body, f"the overlay omits the question {question!r}"
    for button in SUGGESTION_BUTTONS:
        assert button in body, f"the overlay omits the suggestion {button!r}"
    for value in SOURCE_VALUES:
        assert value in body, f"the source list omits {value!r}"


def test_search_returns_ranked_hits_with_highlights(client):
    r = search(client, SITE_INDEX, query="search")
    payload = _ok(r, "site search")
    assert payload.get("hits"), anchor("site search returned no hits", r)
    query_id = payload.get("queryID") or ""
    assert len(query_id) == QUERY_ID_LENGTH, (
        f"queryID is {query_id!r}; the contract pins {QUERY_ID_LENGTH} "
        f"hexadecimal characters")
    assert re.fullmatch(r"[0-9a-f]+", query_id), (
        f"queryID {query_id!r} is not hexadecimal")
    for flag in HONESTY_FLAGS:
        assert flag in payload, (
            f"the response omits the honesty flag {flag!r}; every one of "
            f"{HONESTY_FLAGS} is computed and returned")
    marked = [h for h in payload["hits"]
              if HIGHLIGHT_PRE_TAG in str(h.get("_highlightResult", ""))]
    assert marked, (
        f"no hit carries a {HIGHLIGHT_PRE_TAG} highlight for the query "
        f"'search'; the first hit is {payload['hits'][0]!r}")
    assert HIGHLIGHT_POST_TAG in str(marked[0].get("_highlightResult")), (
        f"the highlight opened with {HIGHLIGHT_PRE_TAG} and never closed with "
        f"{HIGHLIGHT_POST_TAG}: {marked[0]!r}")


def test_source_facet_counts_are_disjunctive(client):
    plain = _ok(search(client, SITE_INDEX, query="",
                       facets=[SOURCE_FACET],
                       disjunctiveFacets=[SOURCE_FACET]), "unfiltered sources")
    counts = facet_counts(plain, SOURCE_FACET)
    for value, expected in SOURCE_COUNTS.items():
        assert counts.get(value) == expected, (
            f"the unfiltered count for source {value!r} is {counts.get(value)!r}, "
            f"and the seeded corpus pins {expected}")

    narrowed = _ok(search(client, SITE_INDEX, query="",
                          facetFilters=[["{}:Blog".format(SOURCE_FACET)]],
                          facets=[SOURCE_FACET],
                          disjunctiveFacets=[SOURCE_FACET]),
                   "sources with Blog ticked")
    after = facet_counts(narrowed, SOURCE_FACET)
    for value, expected in SOURCE_COUNTS.items():
        assert after.get(value) == expected, (
            f"with Blog ticked the count for {value!r} is {after.get(value)!r}. "
            f"A disjunctive facet is counted with its own clause pruned, so "
            f"every source keeps its unfiltered count of {expected}")


def test_catalog_disjunctive_counts_match_the_worked_example(client):
    payload = _ok(search(client, CATALOG_INDEX, query="",
                         facetFilters=[["brand:acme"], ["colour:red"]],
                         facets=["brand", "colour"],
                         disjunctiveFacets=["brand", "colour"]),
                  "catalog with brand and colour ticked")
    brand = facet_counts(payload, "brand")
    colour = facet_counts(payload, "colour")
    assert brand.get("acme") == CATALOG_CELLS[("acme", "red")], (
        f"brand.acme is {brand.get('acme')!r}, expected "
        f"{CATALOG_CELLS[('acme', 'red')]}")
    assert brand.get("zeta") == (CATALOG_CELLS[("zeta", "red")]), (
        f"brand.zeta is {brand.get('zeta')!r}, expected "
        f"{CATALOG_CELLS[('zeta', 'red')]}. Counting brand with the brand "
        f"clause pruned is what makes a second brand tickable")
    assert colour.get("red") == CATALOG_CELLS[("acme", "red")], (
        f"colour.red is {colour.get('red')!r}")
    assert colour.get("blue") == CATALOG_CELLS[("acme", "blue")], (
        f"colour.blue is {colour.get('blue')!r}, expected "
        f"{CATALOG_CELLS[('acme', 'blue')]}. A single grouped pass returns 0 "
        f"here, which is the defect this count exists to catch")
    assert payload.get("nbHits") == CATALOG_CELLS[("acme", "red")], (
        f"the hits themselves use the full filter tree, so nbHits is "
        f"{CATALOG_CELLS[('acme', 'red')]}, not {payload.get('nbHits')!r}")


def test_selected_facet_value_with_no_match_is_still_returned(client):
    payload = _ok(search(client, CATALOG_INDEX, query="",
                         facetFilters=[["brand:acme", "brand:zeta"],
                                       ["colour:blue"]],
                         facets=["colour"], disjunctiveFacets=["colour"]),
                  "catalog with both brands and blue ticked")
    colour = facet_counts(payload, "colour")
    assert "blue" in colour, (
        "a selected disjunctive value must be returned even when it matches "
        f"nothing under the pruned tree; the colour facet came back as {colour!r}")


def test_ranking_cascade_orders_the_fixture_query(client):
    payload = _ok(search(client, FIXTURE_INDEX, query="blue running shoes"),
                  "the ranking fixture query")
    order = [oid for oid in object_ids(payload) if oid in RANK_POPULARITY]
    assert tuple(order) == RANK_ORDER, (
        f"the fixture query returned {order}, and the cascade pins "
        f"{list(RANK_ORDER)}. r2 carries one typo and the highest popularity "
        f"({RANK_POPULARITY['r2']}), so the typo criterion puts r2 last however "
        f"the custom ranking {CUSTOM_RANKING} reads")


def test_cascade_holds_without_custom_ranking(client):
    payload = _ok(search(client, FIXTURE_INDEX, query="blue running shoes",
                         customRanking=[]), "the fixture query without custom ranking")
    order = [oid for oid in object_ids(payload) if oid in RANK_POPULARITY]
    assert tuple(order) == RANK_ORDER, (
        f"removing the custom ranking changed the order to {order}; the eight "
        f"criteria above it already decide this query, so the order is "
        f"{list(RANK_ORDER)} either way")

    strict = _ok(search(client, FIXTURE_INDEX, query="blue running shoes",
                        typoTolerance=False), "the fixture query with typos off")
    strict_order = [oid for oid in object_ids(strict) if oid in RANK_POPULARITY]
    assert "r2" not in strict_order, (
        f"with typo tolerance off r2 must be absent, and the order came back "
        f"{strict_order}")
    assert strict_order == [o for o in RANK_ORDER if o != "r2"], (
        f"with typo tolerance off the remaining three keep their order; got "
        f"{strict_order}")


def test_typo_tolerance_rules_hold(client):
    transposed = _ok(search(client, FIXTURE_INDEX, query="hlelo",
                            getRankingInfo=True), "the transposition query")
    ids = object_ids(transposed)
    assert "t1" in ids, (
        f"the query 'hlelo' must return t1 {TEXT_FIXTURES['t1']!r}: a "
        f"transposition of two adjacent characters costs one, not two. Got {ids}")
    hit = next(h for h in transposed["hits"] if h.get("objectID") == "t1")
    info = hit.get("_rankingInfo") or {}
    assert info.get("nbTypos") == 1, (
        f"t1 came back with nbTypos {info.get('nbTypos')!r} for the query "
        f"'hlelo'; the transposition is one typo")

    first_char = _ok(search(client, FIXTURE_INDEX, query="xello"),
                     "the first-character query")
    assert "t1" not in object_ids(first_char), (
        "the first character may never be substituted, so 'xello' must not "
        f"return t1; got {object_ids(first_char)}")

    digits = _ok(search(client, FIXTURE_INDEX, query="2024"), "the digit query")
    digit_ids = object_ids(digits)
    assert "t4" in digit_ids, f"'2024' must return t4; got {digit_ids}"
    assert "t5" not in digit_ids, (
        f"a digit token gets no typo tolerance, so '2024' must never return t5 "
        f"{TEXT_FIXTURES['t5']!r}; got {digit_ids}")


def test_prefix_matches_only_the_last_word(client):
    single = _ok(search(client, FIXTURE_INDEX, query="hel"), "the prefix query")
    ids = set(object_ids(single))
    assert {"t1", "t2"} <= ids, (
        f"'hel' is the last word, so it is the prefix candidate and must return "
        f"t1 and t2; got {sorted(ids)}")

    two = _ok(search(client, FIXTURE_INDEX, query="hel world"),
              "the two-word prefix query")
    two_ids = set(object_ids(two))
    assert "t1" in two_ids, f"'hel world' must return t1; got {sorted(two_ids)}"
    assert "t2" not in two_ids, (
        "only the last word is a prefix under prefixLast, so 'hel' must match "
        f"exactly in 'hel world' and t2 must be absent; got {sorted(two_ids)}")


def test_text_pipeline_folds_and_tokenizes(client):
    for query, expected in (("creme", "t3"), ("crème", "t3"),
                            ("strasse", "t7"), ("東京", "t6"),
                            ("wor hello", "t1")):
        payload = _ok(search(client, FIXTURE_INDEX, query=query),
                      f"the folding query {query!r}")
        assert expected in object_ids(payload), (
            f"the query {query!r} must return {expected} "
            f"{TEXT_FIXTURES.get(expected)!r}; got {object_ids(payload)}")


def test_highlight_tags_land_in_the_original_text(client):
    payload = _ok(search(client, FIXTURE_INDEX, query="creme",
                         attributesToHighlight=["title"]),
                  "the accented highlight query")
    hit = next((h for h in payload["hits"] if h.get("objectID") == "t3"), None)
    assert hit, f"the query 'creme' returned no t3; got {object_ids(payload)}"
    value = str((hit.get("_highlightResult") or {}).get("title", {}).get("value", ""))
    assert "è" in value, (
        f"the highlighted value is {value!r}: the tags go into the ORIGINAL "
        f"text, so the accent survives and the folded spelling never appears")
    assert HIGHLIGHT_PRE_TAG in value and HIGHLIGHT_POST_TAG in value, (
        f"the highlighted value {value!r} carries no tag pair")

    prefix = _ok(search(client, FIXTURE_INDEX, query="hel",
                        attributesToHighlight=["title"]),
                 "the prefix highlight query")
    prefix_hit = next((h for h in prefix["hits"] if h.get("objectID") == "t1"), None)
    assert prefix_hit, f"the query 'hel' returned no t1; got {object_ids(prefix)}"
    prefix_value = str((prefix_hit.get("_highlightResult") or {})
                       .get("title", {}).get("value", ""))
    assert prefix_value.startswith(f"{HIGHLIGHT_PRE_TAG}Hel{HIGHLIGHT_POST_TAG}"), (
        f"a prefix match highlights only the matched prefix, so the value reads "
        f"{HIGHLIGHT_PRE_TAG}Hel{HIGHLIGHT_POST_TAG}lo World; got {prefix_value!r}")


def test_snippet_is_centred_and_elided(client):
    payload = _ok(search(client, SITE_INDEX, query="search",
                         attributesToSnippet=["body:20"]),
                  "the snippet query")
    snippets = [str((h.get("_snippetResult") or {}).get("body", {}).get("value", ""))
                for h in payload.get("hits", [])]
    assert any(s for s in snippets), (
        f"no hit carries a body snippet; the first hit is "
        f"{payload.get('hits', [{}])[0]!r}")
    assert any(SNIPPET_ELLIPSIS in s for s in snippets), (
        f"no snippet carries the ellipsis {SNIPPET_ELLIPSIS!r} on a side that "
        f"was cut; snippets came back {snippets[:3]!r}")


def test_nested_filter_arrays_carry_the_boolean_structure(client):
    either = _ok(search(client, CATALOG_INDEX, query="",
                        facetFilters=[["brand:acme", "brand:zeta"]]),
                 "one nested array")
    assert either.get("nbHits") == sum(CATALOG_CELLS.values()), (
        f"a nested array is a disjunction, so both brands match and nbHits is "
        f"{sum(CATALOG_CELLS.values())}; got {either.get('nbHits')!r}")

    both = _ok(search(client, CATALOG_INDEX, query="",
                      facetFilters=["brand:acme", "colour:red"]),
               "a flat array")
    assert both.get("nbHits") == CATALOG_CELLS[("acme", "red")], (
        f"a flat array is a conjunction, so nbHits is "
        f"{CATALOG_CELLS[('acme', 'red')]}; got {both.get('nbHits')!r}")

    grouped = _ok(search(client, CATALOG_INDEX, query="",
                         facetFilters=[["brand:acme"], ["colour:red"]]),
                  "two single-entry nested arrays")
    assert grouped.get("nbHits") == both.get("nbHits"), (
        f"two single-entry nested arrays mean the same conjunction as the flat "
        f"form; got {grouped.get('nbHits')!r} against {both.get('nbHits')!r}")

    negated = _ok(search(client, CATALOG_INDEX, query="",
                         facetFilters=["-brand:acme"]), "a negated entry")
    assert negated.get("nbHits") == (CATALOG_CELLS[("zeta", "red")]
                                     + CATALOG_CELLS[("zeta", "blue")]), (
        f"a leading minus negates, so nbHits counts the zeta records; got "
        f"{negated.get('nbHits')!r}")


def test_filter_grammar_refuses_a_quoted_numeric(client):
    r = search(client, CATALOG_INDEX, query="", filters='price > "10"')
    _rejected(r, "a numeric comparison against a quoted value")
    body = _text(r)
    assert "price" in body, (
        f"the refusal must name the offending span; the body came back {body[:300]!r}")

    deep = search(client, CATALOG_INDEX, query="",
                  facetFilters=[[["brand:acme"]]])
    _rejected(deep, "a doubly nested facet filter array")

    unknown = search(client, CATALOG_INDEX, query="", filters="unlisted:1")
    _rejected(unknown, "a filter on an attribute outside attributesForFaceting")


def test_deduplication_counts_groups_before_pagination(client):
    payload = _ok(search(client, SHIRT_INDEX, query="",
                         attributeForDistinct=SHIRT_ATTRIBUTE, distinct=1,
                         page=0, hitsPerPage=20), "the deduplicated first page")
    assert payload.get("nbHits") == SHIRT_GROUPS, (
        f"with distinct on, nbHits counts groups: {SHIRT_GROUPS}, not "
        f"{payload.get('nbHits')!r}")
    assert payload.get("nbPages") == SHIRT_PAGES, (
        f"nbPages follows the group count: {SHIRT_PAGES}, not "
        f"{payload.get('nbPages')!r}")
    groups = [h.get(SHIRT_ATTRIBUTE) for h in payload.get("hits", [])]
    assert len(groups) == 20, f"page zero returned {len(groups)} hits, expected 20"
    assert len(set(groups)) == 20, (
        f"deduplication runs before pagination, so page zero carries 20 distinct "
        f"{SHIRT_ATTRIBUTE} values; got {len(set(groups))} distinct of {groups}")

    records = _ok(search(client, SHIRT_INDEX, query="",
                         attributeForDistinct=SHIRT_ATTRIBUTE, distinct=1,
                         facets=["colour"]), "facet counts under distinct")
    assert facet_counts(records, "colour").get("red") == SHIRT_RED_RECORDS, (
        f"facet counts count RECORDS by default: {SHIRT_RED_RECORDS}; got "
        f"{facet_counts(records, 'colour').get('red')!r}")

    groups_counted = _ok(search(client, SHIRT_INDEX, query="",
                                attributeForDistinct=SHIRT_ATTRIBUTE, distinct=1,
                                facets=["colour"], facetingAfterDistinct=True),
                         "facet counts after distinct")
    assert facet_counts(groups_counted, "colour").get("red") == SHIRT_RED_GROUPS, (
        f"with facetingAfterDistinct on the count is groups: {SHIRT_RED_GROUPS}; "
        f"got {facet_counts(groups_counted, 'colour').get('red')!r}")


def test_pagination_is_stable_across_every_page(client):
    seen = []
    for page in range(SHIRT_PAGES):
        payload = _ok(search(client, SHIRT_INDEX, query="",
                             attributeForDistinct=SHIRT_ATTRIBUTE, distinct=1,
                             page=page, hitsPerPage=20),
                      f"deduplicated page {page}")
        seen.extend(object_ids(payload))
    assert len(seen) == SHIRT_GROUPS, (
        f"collecting every page returned {len(seen)} hits; the group count is "
        f"{SHIRT_GROUPS}")
    assert len(set(seen)) == SHIRT_GROUPS, (
        f"collecting every page repeated an objectID: {len(seen) - len(set(seen))} "
        f"duplicate(s). The cascade needs a final tie-break on objectID or a hit "
        f"appears on two pages")

    first = object_ids(_ok(search(client, SITE_INDEX, query="search"),
                           "a repeated query"))
    for _ in range(4):
        again = object_ids(_ok(search(client, SITE_INDEX, query="search"),
                               "a repeated query"))
        assert again == first, (
            f"the same query returned a different order on a repeat: {again} "
            f"against {first}")

    past_cap = search(client, SHIRT_INDEX, query="", page=0, hitsPerPage=20,
                      offset=5000, length=20)
    _rejected(past_cap, "an offset past paginationLimitedTo")


def test_geo_bucket_ties_before_custom_ranking(client):
    payload = _ok(search(client, CATALOG_INDEX, query="",
                         aroundLatLng=GEO_POINT, getRankingInfo=True),
                  "the geo query")
    hits = [h for h in payload.get("hits", []) if h.get("_geoloc")]
    assert len(hits) >= 3, (
        f"the seeded catalog carries three geo records; the query returned "
        f"{len(hits)}")
    popularities = [h.get("popularity") for h in hits[:3]]
    assert popularities[0] == 100, (
        f"the two nearest records tie on the geo bucket, so popularity breaks "
        f"the tie and the eight-metre record comes first; the first three "
        f"popularities came back {popularities}")
    assert popularities[1] == 1, (
        f"the five-metre record ranks second on popularity; got {popularities}")
    assert popularities[2] == 50, (
        f"the sixty-metre record sits in its own bucket and ranks last; got "
        f"{popularities}")


def test_customer_story_facets_are_multi_select(client, site):
    body = _text(site.get("/customers"))
    assert STORY_PLACEHOLDER in body, (
        f"the customers route omits the placeholder {STORY_PLACEHOLDER!r}")
    for facet in STORY_FACETS:
        assert facet in body, f"the customers route omits the facet {facet!r}"
    for title in STORY_TITLES:
        assert title in body, f"the customers route omits the story {title!r}"

    plain = _ok(search(client, STORY_INDEX, key=STORY_SEARCH_KEY, query="",
                       facets=["industry", "region"],
                       disjunctiveFacets=["industry", "region"]),
                "the unfiltered story facets")
    industry = facet_counts(plain, "industry")
    for value, expected in INDUSTRY_COUNTS.items():
        assert industry.get(value) == expected, (
            f"the unfiltered industry count for {value!r} is "
            f"{industry.get(value)!r}, and the seed pins {expected}")
    region = facet_counts(plain, "region")
    for value, expected in REGION_COUNTS.items():
        assert region.get(value) == expected, (
            f"the unfiltered region count for {value!r} is {region.get(value)!r}, "
            f"and the seed pins {expected}")

    two = _ok(search(client, STORY_INDEX, key=STORY_SEARCH_KEY, query="",
                     facetFilters=[["industry:Ecommerce", "industry:Media"]],
                     facets=["industry", "region"],
                     disjunctiveFacets=["industry", "region"]),
              "two industries ticked")
    still = facet_counts(two, "industry")
    for value, expected in INDUSTRY_COUNTS.items():
        assert still.get(value) == expected, (
            f"with two industries ticked the industry group is counted with its "
            f"own clause pruned, so {value!r} keeps {expected}; got "
            f"{still.get(value)!r}")
    assert two.get("nbHits") == (INDUSTRY_COUNTS["Ecommerce"]
                                 + INDUSTRY_COUNTS["Media"]), (
        f"the hits themselves use the full tree, so nbHits is the two industries "
        f"summed; got {two.get('nbHits')!r}")


def test_customer_facet_state_is_linkable(page, app_url):
    page.goto(f"{app_url}/customers?industry=Ecommerce&industry=Media")
    page.wait_for_load_state("networkidle")
    content = page.content()
    assert "Ecommerce" in content and "Media" in content, (
        "opening the customers route with two industries in the address bar "
        "must restore both selections; neither appeared on the rendered page")
    assert CLEAR_FILTERS in content, (
        f"a filtered view must offer {CLEAR_FILTERS!r}; the rendered page omits it")


def test_pricing_grid_names_every_plan_and_row(site):
    body = _text(site.get("/pricing"))
    for needle in (PRICING_HEADING, PRICING_CHOOSER, GRID_JUMP, GRID_HEADING,
                   FAQ_HEADING, FAQ_FIRST, GROW_METERING, GROW_RECORDS,
                   FREE_BODY, FREE_NOTE):
        assert needle in body, f"the pricing route omits {needle!r}"
    for plan in PLAN_NAMES:
        assert plan in body, f"the pricing route omits the plan {plan!r}"
    for group in PLAN_GROUPS:
        assert group in body, f"the pricing route omits the group {group!r}"
    for subtitle in PLAN_SUBTITLES:
        assert subtitle in body, f"the pricing route omits the subtitle {subtitle!r}"
    for action in PLAN_ACTIONS:
        assert action in body, f"the pricing route omits the action {action!r}"
    for category in GRID_CATEGORIES:
        assert category in body, f"the comparison grid omits {category!r}"
    for row in GRID_ROWS:
        assert row in body, f"the comparison grid omits the row {row!r}"
    for limit in GRID_LIMITS:
        assert limit in body, f"the comparison grid omits the limit {limit!r}"


def test_pricing_money_is_held_in_minor_units(client):
    payload = _ok(client.get("/plans"), "the plans endpoint")
    rows = payload if isinstance(payload, list) else payload.get("plans", [])
    assert rows, f"the plans endpoint returned nothing usable: {payload!r}"
    minors = []
    for row in rows:
        for key in ("searchUnitPriceMinor", "recordUnitPriceMinor"):
            if key in row:
                minors.append(row[key])
        assert row.get("currency", CURRENCY) == CURRENCY, (
            f"plan {row.get('name')!r} carries currency {row.get('currency')!r}; "
            f"the contract pins {CURRENCY!r} lowercase")
    assert UNIT_PRICE_MINOR in minors, (
        f"$0.50 is {UNIT_PRICE_MINOR} in integer minor units; the plans carry "
        f"{minors!r}")
    assert RECORD_PRICE_MINOR in minors, (
        f"$0.40 is {RECORD_PRICE_MINOR} in integer minor units; the plans carry "
        f"{minors!r}")


def test_demo_request_is_stored_and_survives_a_reload(client, db):
    body = demo_payload()
    created = _ok(client.post("/demo-requests", json=body), "a demo request")
    request_id = created.get("id")
    assert request_id, f"the stored demo request carries no id: {created!r}"
    assert created.get("status") == DEMO_STATUS, (
        f"a stored demo request carries status {DEMO_STATUS!r}; got "
        f"{created.get('status')!r}")

    again = _ok(client.get(f"/demo-requests/{request_id}"), "the stored request")
    for key in DEMO_KEYS:
        assert again.get(key) == body[key], (
            f"the stored demo request came back with {key}={again.get(key)!r} "
            f"and the submitted value was {body[key]!r}")

    rows = db.query(
        "select first_name, last_name, email, phone, company, country, status "
        "from demo_requests where email = %s", (body["email"],))
    assert len(rows) == 1, (
        f"the demo request must be one row in postgres; the table holds "
        f"{len(rows)} row(s) for {body['email']!r}")
    stored = rows[0]
    assert stored[2] == body["email"], (
        f"the persisted row carries email {stored[2]!r}, submitted "
        f"{body['email']!r}")
    assert stored[4] == body["company"], (
        f"the persisted row carries company {stored[4]!r}, submitted "
        f"{body['company']!r}")
    assert stored[6] == DEMO_STATUS, (
        f"the persisted row carries status {stored[6]!r}, expected {DEMO_STATUS!r}")


def test_demo_request_refuses_an_incomplete_submission(client, db, site):
    body = _text(site.get("/demorequest"))
    for field in DEMO_FIELDS:
        assert field in body, f"the demo request route omits the label {field!r}"
    assert DEMO_SUBMIT in body, f"the demo request route omits {DEMO_SUBMIT!r}"
    assert DEMO_HEADING in body, f"the demo request route omits {DEMO_HEADING!r}"
    assert COUNTRY_PLACEHOLDER in body, (
        f"the country select omits {COUNTRY_PLACEHOLDER!r}")
    for needle in (STAT_ONE, STAT_ONE_LABEL, STAT_TWO, STAT_TWO_LABEL,
                   TRUST_ROW_ONE, TRUST_ROW_TWO):
        assert needle in body, f"the demo request proof column omits {needle!r}"
    for badge in BADGES:
        assert badge in body, f"the compliance badges omit {badge!r}"

    before = db.query("select count(*) from demo_requests")[0][0]
    blank = demo_payload(email="")
    r = client.post("/demo-requests", json=blank)
    _rejected(r, "a demo request with a blank business email")
    assert "email" in _text(r), (
        f"the refusal must name the failing field; got {_text(r)[:300]!r}")
    after = db.query("select count(*) from demo_requests")[0][0]
    assert after == before, (
        f"a refused demo request writes nothing; the table grew from {before} "
        f"to {after}")


def test_signup_creates_workspace_and_rejects_duplicate(client, db):
    email = probe_email()
    name = f"Probe Workspace {uuid.uuid4().hex[:6]}"
    created = _ok(client.post("/auth/signup",
                              json={"email": email, "password": CORPUS_PASSWORD,
                                    "workspaceName": name}), "signup")
    assert created.get("token"), f"signup returned no token: {created!r}"

    rows = db.query("select count(*) from accounts where email = %s", (email,))
    assert rows[0][0] == 1, (
        f"signup must create exactly one account row for {email!r}; found "
        f"{rows[0][0]}")
    memberships = db.query(
        "select role from memberships m join accounts a on a.id = m.account_id "
        "where a.email = %s", (email,))
    assert [row[0] for row in memberships] == ["owner"], (
        f"a new signup owns its own workspace; the memberships came back "
        f"{[row[0] for row in memberships]}")

    again = client.post("/auth/signup",
                        json={"email": email, "password": CORPUS_PASSWORD,
                              "workspaceName": name})
    _rejected(again, "a second signup on a taken email")
    assert "email" in _text(again), (
        f"the refusal must name the email field; got {_text(again)[:300]!r}")
    rows = db.query("select count(*) from accounts where email = %s", (email,))
    assert rows[0][0] == 1, (
        f"the refused signup created a second account row for {email!r}")


def test_form_validation_refuses_invalid_input(client, db):
    before = db.query("select count(*) from accounts")[0][0]
    _rejected(client.post("/auth/signup",
                          json={"email": probe_email(), "password": "",
                                "workspaceName": "Probe"}),
              "a signup with an empty password")
    _rejected(client.post("/newsletter", json={"email": "not-an-address"}),
              "a newsletter signup with a malformed address")
    after = db.query("select count(*) from accounts")[0][0]
    assert after == before, (
        f"a refused form writes nothing; the accounts table grew from {before} "
        f"to {after}")


def test_analyst_cannot_write_a_rule_or_a_record(client, db):
    token = sign_in(client, ANALYST_EMAIL)
    before = db.query("select count(*) from rules")[0][0]
    rule = client.post(f"/1/indexes/{CATALOG_INDEX}/rules",
                       json={"id": f"probe-{uuid.uuid4().hex[:8]}",
                             "enabled": True, "conditions": [],
                             "consequence": {"promote": []}, "priority": 10},
                       headers=bearer(token))
    assert rule.status_code in (401, 403), anchor(
        "an analyst writing a rule must be denied by the server", rule)
    after = db.query("select count(*) from rules")[0][0]
    assert after == before, (
        f"the denied rule write changed the rules table from {before} to {after}")

    record = client.post(f"/1/indexes/{CATALOG_INDEX}/batch",
                         json={"requests": [{"action": "addObject",
                                             "body": {"brand": "acme",
                                                      "colour": "red"}}]},
                         headers=bearer(token))
    assert record.status_code in (401, 403), anchor(
        "an analyst writing a record must be denied by the server", record)

    reading = client.get(f"/1/indexes/{CATALOG_INDEX}/rules", headers=bearer(token))
    assert reading.status_code == 200, anchor(
        "an analyst may read the rule list", reading)


def test_operator_cannot_manage_keys_or_members(client):
    token = sign_in(client, OPERATOR_EMAIL)
    keys = client.post("/1/keys",
                       json={"kind": "search", "acl": ["search"],
                             "indices": [SITE_INDEX]},
                       headers=bearer(token))
    assert keys.status_code in (401, 403), anchor(
        "an operator creating a key must be denied by the server", keys)

    members = client.post("/members",
                          json={"email": probe_email(), "role": "analyst"},
                          headers=bearer(token))
    assert members.status_code in (401, 403), anchor(
        "an operator inviting a member must be denied by the server", members)


def test_cross_workspace_request_is_denied(client):
    token = sign_in(client, SECOND_OWNER_EMAIL)
    r = client.get(f"/1/indexes/{CATALOG_INDEX}/settings", headers=bearer(token))
    assert r.status_code in (401, 403, 404), anchor(
        "an owner of another workspace reaching this index must be denied", r)

    listing = _ok(client.get("/applications", headers=bearer(token)),
                  "the application list for the second workspace")
    rows = listing if isinstance(listing, list) else listing.get("applications", [])
    slugs = {row.get("slug") for row in rows}
    assert slugs == {SECOND_APP_SLUG}, (
        f"the second owner may see only {SECOND_APP_SLUG!r}; the list came back "
        f"{sorted(s for s in slugs if s)}")


def test_search_key_outside_its_patterns_is_denied(client):
    allowed = search(client, STORY_INDEX, key=STORY_SEARCH_KEY, query="")
    assert allowed.status_code == 200, anchor(
        "the story key searching its own index", allowed)

    refused = search(client, SITE_INDEX, key=STORY_SEARCH_KEY, query="")
    assert refused.status_code in (401, 403), anchor(
        "the story key reaching an index outside its patterns", refused)

    absent = search(client, "no_such_index", key=STORY_SEARCH_KEY, query="")
    assert absent.status_code == refused.status_code, (
        f"a refusal for an out-of-scope index answered {refused.status_code} and "
        f"a refusal for an absent index answered {absent.status_code}; the two "
        f"must be indistinguishable or the difference enumerates the indices")

    writing = client.post(f"/1/indexes/{SITE_INDEX}/batch",
                          json={"requests": []},
                          headers=api_key(SITE_SEARCH_KEY))
    assert writing.status_code in (401, 403), anchor(
        "a search key writing records must be denied", writing)


def test_secured_key_restriction_is_combined_by_conjunction(client):
    restrictions = urllib.parse.urlencode(
        sorted({"filters": "industry:Ecommerce",
                "userToken": "u_1029"}.items()))
    signature = hmac.new(SITE_SEARCH_KEY.encode("utf-8"),
                         restrictions.encode("utf-8"),
                         hashlib.sha256).hexdigest()
    secured = base64.b64encode(
        (signature + restrictions).encode("utf-8")).decode("ascii")

    scoped = _ok(search(client, STORY_INDEX, key=secured, query=""),
                 "a secured key restricted to one industry")
    assert scoped.get("nbHits") == INDUSTRY_COUNTS["Ecommerce"], (
        f"the secured key restricts to Ecommerce, so nbHits is "
        f"{INDUSTRY_COUNTS['Ecommerce']}; got {scoped.get('nbHits')!r}")

    widened = _ok(search(client, STORY_INDEX, key=secured, query="",
                         filters="industry:Media"),
                  "a secured key asked for another industry")
    assert widened.get("nbHits") == 0, (
        f"the key's filters and the request's filters are combined by "
        f"conjunction, so asking for Media under an Ecommerce key returns zero "
        f"hits; got {widened.get('nbHits')!r}. Letting the request replace the "
        f"key's restriction makes every restriction advisory")

    tampered = base64.b64encode(
        (signature + restrictions.replace("Ecommerce", "Media")
         ).encode("utf-8")).decode("ascii")
    refused = search(client, STORY_INDEX, key=tampered, query="")
    assert refused.status_code in (401, 403), anchor(
        "a secured key whose restriction string was edited", refused)


def test_no_secret_reaches_the_browser(site):
    for route in PUBLIC_ROUTES:
        body = _text(site.get(route))
        for needle in SECRET_NEEDLES:
            assert needle not in body, (
                f"{route} hands the browser {needle!r}; no admin key, ingest "
                f"key or database address may appear in anything the browser "
                f"downloads")
        for script in re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', body):
            if script.startswith("http") and "//" in script[8:]:
                continue
            asset = site.get(script)
            if asset.status_code != 200:
                continue
            payload = _text(asset)
            for needle in SECRET_NEEDLES:
                assert needle not in payload, (
                    f"the bundle {script} served from {route} carries {needle!r}")


def test_console_inline_edit_persists_the_new_value(client, db):
    token = sign_in(client, OPERATOR_EMAIL)
    marker = f"probe-{uuid.uuid4().hex[:8]}"
    r = client.post(f"/1/indexes/{CATALOG_INDEX}/batch",
                    json={"requests": [{"action": "partialUpdateObject",
                                        "body": {"objectID": "c_001",
                                                 "note": marker}}]},
                    headers=bearer(token))
    accepted = _ok(r, "an inline edit from the record browser")
    task_id = accepted.get("taskID")
    assert task_id is not None, f"the edit returned no taskID: {accepted!r}"

    published = poll(lambda: (client.get(
        f"/1/indexes/{CATALOG_INDEX}/task/{task_id}",
        headers=bearer(token)).json().get("status") == "published") or None)
    assert published, (
        f"task {task_id} never reported published for the inline edit on c_001")

    rows = db.query(
        "select attributes from records r join indices i on i.id = r.index_id "
        "where i.name = %s and r.object_id = %s", (CATALOG_INDEX, "c_001"))
    assert rows, f"no persisted row for c_001 in {CATALOG_INDEX}"
    assert marker in str(rows[0][0]), (
        f"the persisted attributes for c_001 are {rows[0][0]!r} and carry no "
        f"{marker!r}; the edited value must be the stored value")

    fresh = _ok(client.get(f"/1/indexes/{CATALOG_INDEX}/objects/c_001",
                           headers=bearer(token)), "a fresh read of c_001")
    assert marker in str(fresh), (
        f"a fresh read of c_001 came back {fresh!r} without {marker!r}, so the "
        f"edit did not survive")

    found = _ok(search(client, CATALOG_INDEX, query=marker), "a search for the edit")
    assert "c_001" in object_ids(found), (
        f"the edited value must be searchable; the query {marker!r} returned "
        f"{object_ids(found)}")


def test_idempotency_key_replay_creates_no_second_task(client, db):
    token = sign_in(client, OPERATOR_EMAIL)
    key = f"probe-{uuid.uuid4().hex}"
    body = {"requests": [{"action": "partialUpdateObject",
                          "body": {"objectID": "c_002",
                                   "note": f"probe-{uuid.uuid4().hex[:6]}"}}]}
    before = db.query("select count(*) from tasks")[0][0]
    first = _ok(client.post(f"/1/indexes/{CATALOG_INDEX}/batch", json=body,
                            headers={**bearer(token), IDEMPOTENCY_HEADER: key}),
                "the first idempotent write")
    replay = client.post(f"/1/indexes/{CATALOG_INDEX}/batch", json=body,
                         headers={**bearer(token), IDEMPOTENCY_HEADER: key})
    replayed = _ok(replay, "the replayed idempotent write")
    assert replayed.get("taskID") == first.get("taskID"), (
        f"the replay returned taskID {replayed.get('taskID')!r} and the first "
        f"call returned {first.get('taskID')!r}; a replay returns the stored "
        f"response verbatim")
    after = db.query("select count(*) from tasks")[0][0]
    assert after == before + 1, (
        f"the replay enqueued a second task: the tasks table went from {before} "
        f"to {after}")

    conflicting = client.post(
        f"/1/indexes/{CATALOG_INDEX}/batch",
        json={"requests": [{"action": "partialUpdateObject",
                            "body": {"objectID": "c_003", "note": "other"}}]},
        headers={**bearer(token), IDEMPOTENCY_HEADER: key})
    _rejected(conflicting, "the same idempotency key carrying a different body")
    final = db.query("select count(*) from tasks")[0][0]
    assert final == after, (
        f"the refused reuse applied its body anyway: tasks went from {after} to "
        f"{final}")


def test_batch_is_not_a_transaction(client, db):
    token = sign_in(client, OPERATOR_EMAIL)
    oversize = {"objectID": f"probe-{uuid.uuid4().hex[:8]}",
                "blob": "x" * 200000, "brand": "acme", "colour": "red"}
    good = {"objectID": f"probe-{uuid.uuid4().hex[:8]}",
            "brand": "acme", "colour": "blue"}
    payload = _ok(client.post(
        f"/1/indexes/{CATALOG_INDEX}/batch",
        json={"requests": [{"action": "addObject", "body": good},
                           {"action": "addObject", "body": oversize}]},
        headers=bearer(token)), "a batch carrying one over-size record")
    results = payload.get("objectIDs")
    assert isinstance(results, list) and len(results) == 2, (
        f"the batch response must carry one result per operation; got "
        f"{results!r}")
    assert results[0], (
        f"the first operation was accepted, so its slot carries an objectID; "
        f"got {results!r}")
    assert results[1] is None, (
        f"the over-size operation is rejected on its own and its slot carries "
        f"null; got {results!r}. Rolling the whole batch back loses the record "
        f"that was fine")
    rows = db.query(
        "select count(*) from records r join indices i on i.id = r.index_id "
        "where i.name = %s and r.object_id = %s",
        (CATALOG_INDEX, good["objectID"]))
    assert rows[0][0] == 1, (
        f"the accepted record was not persisted; the table holds {rows[0][0]} "
        f"row(s) for {good['objectID']!r}")


def test_task_ids_are_monotonic_within_one_index(client, db):
    token = sign_in(client, OPERATOR_EMAIL)
    ids = []
    for target in ("c_004", "c_005"):
        payload = _ok(client.post(
            f"/1/indexes/{CATALOG_INDEX}/batch",
            json={"requests": [{"action": "partialUpdateObject",
                                "body": {"objectID": target,
                                         "note": f"probe-{uuid.uuid4().hex[:6]}"}}]},
            headers=bearer(token)), f"a write to {target}")
        ids.append(payload.get("taskID"))
    assert ids[1] > ids[0], (
        f"taskID is monotonic within one index; two writes to {CATALOG_INDEX} "
        f"returned {ids}")

    other = _ok(client.post(
        f"/1/indexes/{SHIRT_INDEX}/batch",
        json={"requests": [{"action": "partialUpdateObject",
                            "body": {"objectID": "s_0001",
                                     "note": f"probe-{uuid.uuid4().hex[:6]}"}}]},
        headers=bearer(token)), "a write to a second index")
    rows = db.query(
        "select i.name, max(t.id) from tasks t join indices i on i.id = t.index_id "
        "where i.name in (%s, %s) group by i.name", (CATALOG_INDEX, SHIRT_INDEX))
    assert len(rows) == 2, (
        f"both indices must carry their own task sequence; got {rows!r}")
    assert other.get("taskID") is not None, (
        f"the second index write returned no taskID: {other!r}")


def test_rule_hide_beats_promote(client, db):
    token = sign_in(client, OPERATOR_EMAIL)
    promote_id = f"probe-promote-{uuid.uuid4().hex[:6]}"
    hide_id = f"probe-hide-{uuid.uuid4().hex[:6]}"
    _ok(client.post(f"/1/indexes/{CATALOG_INDEX}/rules",
                    json={"id": promote_id, "enabled": True,
                          "conditions": [{"anchoring": "is", "pattern": "sofa"}],
                          "consequence": {"promote": [{"objectID": "c_001",
                                                       "position": 0}]},
                          "priority": 10},
                    headers=bearer(token)), "a promote rule")
    settle()
    promoted = _ok(search(client, CATALOG_INDEX, query="sofa"),
                   "the promoted query")
    assert object_ids(promoted)[:1] == ["c_001"], (
        f"the promote rule puts c_001 first for 'sofa'; got "
        f"{object_ids(promoted)[:3]}")

    _ok(client.post(f"/1/indexes/{CATALOG_INDEX}/rules",
                    json={"id": hide_id, "enabled": True,
                          "conditions": [{"anchoring": "is", "pattern": "sofa"}],
                          "consequence": {"hide": ["c_001"]},
                          "priority": 20},
                    headers=bearer(token)), "a hide rule")
    settle()
    hidden = _ok(search(client, CATALOG_INDEX, query="sofa"), "the hidden query")
    assert "c_001" not in object_ids(hidden), (
        f"a hide beats a promote, so c_001 is absent; got {object_ids(hidden)}")
    assert promote_id in (hidden.get("appliedRules") or []), (
        f"the applied rules must name the promote rule that ran; got "
        f"{hidden.get('appliedRules')!r}")

    client.delete(f"/1/indexes/{CATALOG_INDEX}/rules/{hide_id}",
                  headers=bearer(token))
    client.delete(f"/1/indexes/{CATALOG_INDEX}/rules/{promote_id}",
                  headers=bearer(token))


def test_events_deduplicate_and_rollups_recompute(client, db):
    token = sign_in(client, OPERATOR_EMAIL)
    user = probe_token()
    found = _ok(search(client, SITE_INDEX, query="search"), "a search for events")
    query_id = found.get("queryID")
    hit = object_ids(found)[0]
    event = {"eventType": "click", "eventName": "Result Clicked",
             "index": SITE_INDEX, "userToken": user, "objectIDs": [hit],
             "positions": [1], "queryID": query_id}
    for _ in range(2):
        _ok(client.post("/1/events", json={"events": [event]}), "an event")
    rows = db.query(
        "select count(*) from interaction_events where user_token = %s", (user,))
    assert rows[0][0] == 1, (
        f"two identical clicks inside one minute are one event; the table holds "
        f"{rows[0][0]} rows for {user!r}")

    malformed = _ok(client.post("/1/events", json={"events": [
        {"eventType": "click", "eventName": "Result Clicked",
         "index": SITE_INDEX, "userToken": probe_token(),
         "objectIDs": [hit], "queryID": query_id}]}), "a malformed click")
    dropped = malformed.get("dropped") or {}
    assert dropped.get("malformed"), (
        f"a click carrying a queryID without positions is dropped as malformed; "
        f"the intake reported {malformed!r}")

    token_free = _ok(client.post("/1/events", json={"events": [
        {"eventType": "view", "eventName": "Result Viewed",
         "index": SITE_INDEX, "objectIDs": [hit]}]}), "an event with no user token")
    assert (token_free.get("dropped") or {}), (
        f"an event carrying no user token is dropped; the intake reported "
        f"{token_free!r}")

    overview = _ok(client.get("/analytics/overview",
                              params={"index": SITE_INDEX},
                              headers=bearer(token)), "the analytics overview")
    assert "users" in str(overview), (
        f"the overview reports a distinct user count; got {overview!r}")
    assert "approximate" in str(overview).lower(), (
        f"a distinct count is marked approximate in the figure itself; got "
        f"{overview!r}")


def test_cookie_choice_survives_a_reload(client, db):
    visitor = probe_token()
    empty = _ok(client.get("/cookie-choice", params={"visitor": visitor}),
                "an unanswered cookie question")
    assert not empty.get("accepted"), (
        f"a first-time visitor has no recorded answer; got {empty!r}")

    _ok(client.post("/cookie-choice",
                    json={"visitor": visitor, "accepted": False}),
        "refusing non-essential cookies")
    again = _ok(client.get("/cookie-choice", params={"visitor": visitor}),
                "the recorded cookie answer")
    assert again.get("accepted") is False, (
        f"the recorded answer must survive; got {again!r}")
    rows = db.query(
        "select accepted from cookie_choices where visitor_token = %s", (visitor,))
    assert len(rows) == 1 and rows[0][0] is False, (
        f"the cookie answer is one first-party row; the table holds {rows!r}")


def test_privacy_page_is_linked_from_every_footer(site):
    for route in CHROME_ROUTES:
        body = _text(site.get(route))
        assert "Privacy Policy" in body, (
            f"{route} omits the footer link to the privacy page")
    privacy = site.get("/privacy")
    assert privacy.status_code == 200, anchor("the privacy route", privacy)
    text = _text(privacy).lower()
    for subject in ("demo request", "newsletter", "cookie", "search"):
        assert subject in text, (
            f"the privacy page must state what is recorded; it omits {subject!r}")


def test_unknown_path_answers_not_found(site):
    r = site.get(f"/no-such-route-{uuid.uuid4().hex[:8]}")
    assert r.status_code == 404, anchor(
        "an unmatched path must answer not found, never a soft 200", r)
    body = _text(r)
    for needle in (NOT_FOUND_NUMERAL, NOT_FOUND_HEADING, NOT_FOUND_SEARCH):
        assert needle in body, f"the not-found route omits {needle!r}"
    for link in NOT_FOUND_LINKS:
        assert link in body, f"the not-found route omits the link {link!r}"


def test_degradation_is_flagged_rather_than_silent(client):
    payload = _ok(search(client, SITE_INDEX, query="search"), "a plain search")
    assert "degraded" in payload, (
        f"every response carries a degraded list, empty when nothing was shed; "
        f"got keys {sorted(payload)}")
    assert isinstance(payload["degraded"], list), (
        f"degraded is a list of the stages that were shed; got "
        f"{payload['degraded']!r}")

    truncated = _ok(search(client, SITE_INDEX, query="a" * 600),
                    "an over-long query")
    assert truncated.get("truncatedQuery") is True, (
        f"a query past 512 characters is truncated and reported; got "
        f"{truncated.get('truncatedQuery')!r}")

    capped = _ok(search(client, SHIRT_INDEX, query="", facets=["colour"],
                        maxValuesPerFacet=1), "a capped facet")
    assert capped.get("exhaustiveFacetsCount") is False, (
        f"a grouping that reached maxValuesPerFacet reports "
        f"exhaustiveFacetsCount false; got "
        f"{capped.get('exhaustiveFacetsCount')!r}")


def test_narrow_viewport_has_no_sideways_overflow(page, app_url):
    page.set_viewport_size(NARROW_VIEWPORT)
    for route in PUBLIC_ROUTES:
        page.goto(f"{app_url}{route}")
        page.wait_for_load_state("networkidle")
        overflow = page.evaluate(
            "() => document.documentElement.scrollWidth - "
            "document.documentElement.clientWidth")
        assert overflow <= 1, (
            f"{route} overflows sideways by {overflow} pixels at "
            f"{NARROW_VIEWPORT['width']} wide; nothing may overflow sideways at "
            f"a narrow viewport")


def test_body_text_meets_the_contrast_bar(page, app_url):
    page.goto(f"{app_url}/")
    page.wait_for_load_state("networkidle")
    ratio = page.evaluate(
        """() => {
            const lum = (c) => {
                const v = c.map(x => {
                    x = x / 255;
                    return x <= 0.03928 ? x / 12.92 :
                        Math.pow((x + 0.055) / 1.055, 2.4);
                });
                return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
            };
            const parse = (s) => (s.match(/\\d+(\\.\\d+)?/g) || [0, 0, 0])
                .slice(0, 3).map(Number);
            const node = document.querySelector('main p, main li, main span, p');
            if (!node) { return 0; }
            let bg = node, colour = getComputedStyle(node).color;
            let background = getComputedStyle(bg).backgroundColor;
            while (bg && (background === 'rgba(0, 0, 0, 0)' ||
                          background === 'transparent')) {
                bg = bg.parentElement;
                if (!bg) { break; }
                background = getComputedStyle(bg).backgroundColor;
            }
            if (!background || background === 'rgba(0, 0, 0, 0)') {
                background = 'rgb(255, 255, 255)';
            }
            const a = lum(parse(colour)), b = lum(parse(background));
            const hi = Math.max(a, b), lo = Math.min(a, b);
            return (hi + 0.05) / (lo + 0.05);
        }""")
    assert ratio >= CONTRAST_BODY_RATIO, (
        f"body text on the home route sits at a contrast ratio of {ratio:.2f} "
        f"against its own background; the bar is {CONTRAST_BODY_RATIO} to 1")


def test_type_families_are_declared(site):
    body = _text(site.get("/"))
    for family in TYPE_FAMILIES:
        assert family in body, (
            f"the served document never names the type family {family!r}; both "
            f"families are named rather than shipped as files")
    assert "<img" not in body.lower() or "data:image" not in body.lower(), (
        "no binary image ships with this build")


def test_search_preview_explains_why_one_hit_outranks_another(client):
    token = sign_in(client, OPERATOR_EMAIL)
    payload = _ok(client.post(f"/1/indexes/{FIXTURE_INDEX}/query",
                              json={"query": "blue running shoes",
                                    "getRankingInfo": True},
                              headers=bearer(token)),
                  "the console search preview")
    hits = payload.get("hits", [])
    assert len(hits) >= 2, f"the preview returned {len(hits)} hits"
    for hit in hits:
        info = hit.get("_rankingInfo")
        assert info, (
            f"the preview turns getRankingInfo on by default, so every hit "
            f"carries its ranking info; hit {hit.get('objectID')!r} carries none")
        for field in ("nbTypos", "proximityDistance", "nbExactWords",
                      "firstMatchedWord", "userScore"):
            assert field in info, (
                f"the ranking info for {hit.get('objectID')!r} omits {field!r}; "
                f"the disclosure needs one value per criterion")
    last = next(h for h in hits if h.get("objectID") == "r2")
    assert (last.get("_rankingInfo") or {}).get("nbTypos") == 1, (
        f"r2 is last because of the typo criterion, so its ranking info reports "
        f"one typo; got {last.get('_rankingInfo')!r}")


def test_ingest_key_writes_and_cannot_read_analytics(client, db):
    marker = f"probe-{uuid.uuid4().hex[:8]}"
    written = _ok(client.post(
        f"/1/indexes/{CATALOG_INDEX}/batch",
        json={"requests": [{"action": "addObject",
                            "body": {"objectID": marker, "brand": "acme",
                                     "colour": "blue"}}]},
        headers=api_key(INGEST_KEY)), "an ingest key writing a record")
    assert written.get("taskID") is not None, (
        f"the ingest write returned no taskID: {written!r}")
    rows = db.query(
        "select count(*) from records r join indices i on i.id = r.index_id "
        "where i.name = %s and r.object_id = %s", (CATALOG_INDEX, marker))
    assert rows[0][0] == 1, (
        f"the ingest key's record was not persisted; found {rows[0][0]} row(s)")

    reading = client.get("/analytics/overview",
                         params={"index": SITE_INDEX},
                         headers=api_key(INGEST_KEY))
    assert reading.status_code in (401, 403), anchor(
        "an ingest key reading analytics must be denied", reading)

    searching = search(client, CATALOG_INDEX, key=INGEST_KEY, query="")
    assert searching.status_code in (401, 403), anchor(
        "an ingest key searching must be denied", searching)
