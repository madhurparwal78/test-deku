"""Observations over the deployed Valdris vehicle range catalogue.

Every assertion here reads the app over HTTP, a rendered page, or the PostgreSQL
database behind it. Nothing reads the source the agent wrote.
"""

from __future__ import annotations

import httpx

import appclient
import capabilities
import conftest


def test_health_endpoint_reports_ready():
    response = httpx.get(f"{appclient.app_url()}/api/health", timeout=conftest.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, expected 200 once the app "
        f"is ready: {response.text[:300]}"
    )


def test_seeded_range_holds_six_families_and_ninety_two_variants():
    backend = conftest.backend()
    families = backend.count("families")
    variants = backend.count("variants")
    assert families == conftest.FAMILY_COUNT, (
        f"the families table holds {families} rows, expected {conftest.FAMILY_COUNT}"
    )
    assert variants == conftest.TOTAL_VARIANTS, (
        f"the variants table holds {variants} rows, expected {conftest.TOTAL_VARIANTS}"
    )


def test_families_endpoint_lists_six_families_in_facet_order():
    client = conftest.anonymous()
    response = client.get("/families")
    assert response.status_code == 200, (
        f"GET /api/families returned {response.status_code}: {response.text[:300]}"
    )
    payload = response.json()
    assert isinstance(payload, list), (
        f"GET /api/families must return a top-level JSON array, got {type(payload).__name__}"
    )
    names = [f.get("display_name") or f.get("name") or f.get("key") for f in payload]
    assert names == list(conftest.FAMILY_FACET_ORDER), (
        f"the families endpoint lists {names}, expected the facet order "
        f"{list(conftest.FAMILY_FACET_ORDER)}"
    )


def test_home_payload_lists_families_in_home_order():
    client = conftest.anonymous()
    response = client.get("/home", params={"locale": conftest.DEFAULT_LOCALE})
    assert response.status_code == 200, (
        f"GET /api/home returned {response.status_code}: {response.text[:300]}"
    )
    families = response.json().get("families", [])
    names = [f.get("display_name") or f.get("name") or f.get("key") for f in families]
    assert names == list(conftest.FAMILY_HOME_ORDER), (
        f"the home payload lists {names}, expected the home grid order "
        f"{list(conftest.FAMILY_HOME_ORDER)}. The home order and the facet order are "
        f"two stored orderings and are deliberately different"
    )


def test_unavailable_family_carries_the_unavailable_chip():
    client = conftest.anonymous()
    families = client.get("/families").json()
    match = [f for f in families
             if (f.get("display_name") or f.get("name") or f.get("key"))
             == conftest.UNAVAILABLE_FAMILY]
    assert match, f"the family {conftest.UNAVAILABLE_FAMILY} is absent from the range"
    family = match[0]
    chips = family.get("chips") or family.get("powertrains") or []
    flat = " ".join(str(c) for c in chips)
    assert conftest.UNAVAILABLE_CHIP in flat, (
        f"the family {conftest.UNAVAILABLE_FAMILY} carries chips {chips}, expected the "
        f"single wide chip {conftest.UNAVAILABLE_CHIP!r}"
    )
    state = str(family.get("availability_state", "")).lower()
    assert "unavail" in state, (
        f"the family {conftest.UNAVAILABLE_FAMILY} reports availability_state {state!r}, "
        f"expected the unavailable state"
    )


def test_series_counts_sum_to_the_all_count():
    client = conftest.anonymous()
    counts = conftest.series_counts(conftest.variants_payload(client))
    assert counts, "GET /api/variants returned no counts for the Model series facet"
    for row, expected in conftest.SERIES_COUNTS.items():
        assert counts.get(row) == expected, (
            f"the series row {row!r} shows {counts.get(row)}, expected {expected}"
        )
    family_total = sum(v for k, v in counts.items() if k != "All")
    assert family_total == counts.get("All"), (
        f"the six family counts sum to {family_total} but the All row shows "
        f"{counts.get('All')}. A count is computed against the other facets, never "
        f"against the facet whose row displays it, which is why they must agree"
    )


def test_series_counts_ignore_the_series_selection():
    client = conftest.anonymous()
    unfiltered = conftest.series_counts(conftest.variants_payload(client))
    narrowed = conftest.series_counts(conftest.variants_payload(client, series="900"))
    assert narrowed == unfiltered, (
        f"selecting the series 900 changed the series counts from {unfiltered} to "
        f"{narrowed}. Every series count stays as it was, because a count is never "
        f"computed against its own facet"
    )


def test_selecting_a_family_updates_the_other_facet_counts():
    client = conftest.anonymous()
    unfiltered = conftest.variants_payload(client)
    narrowed = conftest.variants_payload(client, series="Terra")
    before = (unfiltered.get("counts") or {}).get("drive") or {}
    after = (narrowed.get("counts") or {}).get("drive") or {}
    assert before, "GET /api/variants returned no counts for the Drive facet"
    assert after != before, (
        f"selecting the series Terra left the Drive counts unchanged at {before}. "
        f"A count on another facet is computed against the current selection"
    )


def test_results_are_grouped_by_body_style():
    client = conftest.anonymous()
    groups = conftest.grouped_variants(conftest.variants_payload(client, series="900"))
    assert groups, (
        "GET /api/variants returned no result groups. Results are gathered by body "
        "style under a heading, never served as one flat list"
    )
    for heading in conftest.GROUP_HEADINGS:
        assert heading in groups, (
            f"the group heading {heading!r} is absent; the 900 family answers as "
            f"{sorted(groups)}"
        )


def test_seeded_corsa_variants_carry_their_measured_figures():
    client = conftest.anonymous()
    payload = conftest.variants_payload(client, series="900")
    rows = {}
    for group in (payload.get("groups") or payload.get("result_groups") or []):
        for variant in group.get("variants", []):
            rows[variant.get("display_name") or variant.get("name")] = variant
    for name, expected in conftest.SEEDED_VARIANTS.items():
        assert name in rows, f"the seeded variant {name!r} is absent from the 900 family"
        got = rows[name]
        flat = str(got)
        for field in ("acceleration", "power", "top_speed"):
            assert expected[field] in flat, (
                f"the variant {name!r} does not carry its {field} figure "
                f"{expected[field]!r}: {flat[:400]}"
            )
        assert conftest.MODEL_YEAR in flat, (
            f"the variant {name!r} does not carry the model year chip "
            f"{conftest.MODEL_YEAR!r}"
        )


def test_variant_statistics_carry_per_variant_labels():
    client = conftest.anonymous()
    payload = conftest.variants_payload(client, series="900")
    rows = {}
    for group in (payload.get("groups") or payload.get("result_groups") or []):
        for variant in group.get("variants", []):
            rows[variant.get("display_name") or variant.get("name")] = str(variant)
    plain = rows.get("Corsa T", "")
    assert conftest.ACCELERATION_LABEL_PLAIN in plain, (
        f"Corsa T must carry the plain acceleration label "
        f"{conftest.ACCELERATION_LABEL_PLAIN!r}: {plain[:400]}"
    )
    assert conftest.ACCELERATION_LABEL_PACKAGE not in plain, (
        "Corsa T carries the Sport Chrono acceleration label, which belongs to the "
        "other five seeded variants. The label is stored per variant"
    )
    combined = rows.get("Corsa GTS", "")
    assert conftest.POWER_LABEL_COMBINED in combined, (
        f"Corsa GTS must carry the combined power label "
        f"{conftest.POWER_LABEL_COMBINED!r}: {combined[:400]}"
    )
    base = rows.get("Corsa", "")
    assert conftest.POWER_LABEL_PLAIN in base, (
        f"Corsa must carry the plain power label {conftest.POWER_LABEL_PLAIN!r}"
    )


def test_comparison_set_round_trips_through_the_query_string():
    client = conftest.anonymous()
    picked = ("Corsa GTS", "Corsa 4 GTS")
    page = httpx.get(
        f"{appclient.app_url()}/{conftest.DEFAULT_LOCALE}/models/900",
        params={"compare": ",".join(picked)},
        timeout=conftest.TIMEOUT,
    )
    assert page.status_code == 200, (
        f"a filtered and ticked address returned {page.status_code}: {page.text[:300]}"
    )
    payload = conftest.variants_payload(client, series="900", compare=",".join(picked))
    selected = payload.get("compare") or payload.get("comparison_set") or []
    names = [s if isinstance(s, str) else (s.get("display_name") or s.get("name"))
             for s in selected]
    for name in picked:
        assert name in names, (
            f"the variant {name!r} was named in the address but is absent from the "
            f"comparison set the app read back: {names}. A ticked set must be "
            f"addressable so a comparison can be shared"
        )


def test_ticked_variant_survives_a_facet_change():
    client = conftest.anonymous()
    ticked = "Corsa GTS"
    hidden = conftest.variants_payload(client, series="Terra", compare=ticked)
    selected = hidden.get("compare") or hidden.get("comparison_set") or []
    names = [s if isinstance(s, str) else (s.get("display_name") or s.get("name"))
             for s in selected]
    assert ticked in names, (
        f"the variant {ticked!r} was ticked and then filtered out of view by the Terra "
        f"series, and the app dropped it from the comparison set: {names}. The set "
        f"belongs to the route rather than to the rendered list, so a variant filtered "
        f"out of sight stays in the set"
    )
    restored = conftest.variants_payload(client, series="900", compare=ticked)
    back = restored.get("compare") or restored.get("comparison_set") or []
    back_names = [s if isinstance(s, str) else (s.get("display_name") or s.get("name"))
                  for s in back]
    assert ticked in back_names, (
        f"the variant {ticked!r} did not return ticked when the series facet was set "
        f"back to 900: {back_names}"
    )


def test_empty_result_promotes_the_reset_control():
    client = conftest.anonymous()
    payload = conftest.variants_payload(client, series="Terra", body="Cabriolet",
                                        drive="Rear-Wheel Drive", seats="2")
    names = conftest.flat_variants(payload)
    assert names == [], (
        f"a facet combination that matches nothing returned {names}. An empty result "
        f"is a valid answer rather than an error"
    )
    page = httpx.get(
        f"{appclient.app_url()}/{conftest.DEFAULT_LOCALE}/models/Terra",
        params={"body": "Cabriolet", "drive": "Rear-Wheel Drive", "seats": "2"},
        timeout=conftest.TIMEOUT,
    )
    assert page.status_code == 200, (
        f"an empty result rendered {page.status_code}; it is a valid page, never the "
        f"not-found surface"
    )
    text = conftest.visible_text(page.text)
    assert conftest.RESET_CONTROL in text, (
        f"the reset control {conftest.RESET_CONTROL!r} is absent from an empty result "
        f"region: {text[:400]}"
    )


def test_overview_offers_no_sort_control():
    page = httpx.get(
        f"{appclient.app_url()}/{conftest.DEFAULT_LOCALE}/models/900",
        timeout=conftest.TIMEOUT,
    )
    assert page.status_code == 200, (
        f"the model overview returned {page.status_code}: {page.text[:300]}"
    )
    lowered = conftest.visible_text(page.text).lower()
    found = [word for word in conftest.SORT_WORDS if word in lowered]
    assert not found, (
        f"the model overview offers a way to reorder the results ({found}). Ordering "
        f"within a group is the stored house order, and no sort control may be added"
    )


def test_saved_comparison_persists_and_restores_its_state():
    owner = conftest.session(conftest.OWNER_ONE)
    name = conftest.unique("probe-set")
    made = owner.post("/comparisons", json={
        "name": name,
        "variant_keys": ["Corsa GTS", "Corsa 4 GTS"],
        "facet_state": {"series": "900"},
    })
    assert made.status_code in (200, 201), (
        f"POST /api/comparisons returned {made.status_code}: {made.text[:300]}"
    )
    saved_id = made.json().get("id")
    assert saved_id is not None, f"the created saved comparison carries no id: {made.json()}"

    fresh = conftest.session(conftest.OWNER_ONE)
    read = fresh.get(f"/comparisons/{saved_id}")
    assert read.status_code == 200, (
        f"a saved comparison could not be read back in a new session: "
        f"{read.status_code} {read.text[:300]}"
    )
    body = str(read.json())
    for variant in ("Corsa GTS", "Corsa 4 GTS"):
        assert variant in body, (
            f"the saved comparison lost the variant {variant!r} across a reload: "
            f"{body[:400]}"
        )
    assert "900" in body, (
        f"the saved comparison lost the facets in force when it was saved: {body[:400]}"
    )


def test_saved_comparison_name_is_unique_per_owner():
    owner = conftest.session(conftest.OWNER_ONE)
    name = conftest.unique("duplicate-set")
    payload = {"name": name, "variant_keys": ["Corsa S"], "facet_state": {"series": "900"}}
    first = owner.post("/comparisons", json=payload)
    assert first.status_code in (200, 201), (
        f"the first save returned {first.status_code}: {first.text[:300]}"
    )
    before = conftest.backend_count("saved_comparisons")
    second = owner.post("/comparisons", json=payload)
    assert 400 <= second.status_code < 500, (
        f"saving a second comparison under the name {name!r} returned "
        f"{second.status_code}; one owner cannot hold two of the same name"
    )
    after = conftest.backend_count("saved_comparisons")
    assert after == before, (
        f"the refused duplicate wrote a row anyway: saved_comparisons went from "
        f"{before} to {after}"
    )

    other = conftest.session(conftest.OWNER_TWO)
    theirs = other.post("/comparisons", json=payload)
    assert theirs.status_code in (200, 201), (
        f"a different owner was refused the name {name!r} with {theirs.status_code}; "
        f"the name is unique per owner rather than globally"
    )


def test_owner_cannot_read_another_owners_saved_comparison():
    owner = conftest.session(conftest.OWNER_ONE)
    made = owner.post("/comparisons", json={
        "name": conftest.unique("private-set"),
        "variant_keys": ["Corsa 4S"],
        "facet_state": {"series": "900"},
    })
    assert made.status_code in (200, 201), (
        f"POST /api/comparisons returned {made.status_code}: {made.text[:300]}"
    )
    saved_id = made.json().get("id")

    intruder = conftest.session(conftest.OWNER_TWO)
    read = intruder.get(f"/comparisons/{saved_id}")
    assert read.status_code in (403, 404), (
        f"{conftest.OWNER_TWO} read {conftest.OWNER_ONE}'s saved comparison with "
        f"{read.status_code}: {read.text[:300]}"
    )
    listed = intruder.get("/comparisons")
    assert str(saved_id) not in str(listed.json()), (
        f"{conftest.OWNER_ONE}'s saved comparison appears in {conftest.OWNER_TWO}'s own "
        f"list, so the list is not scoped to the session owner"
    )

    missing = intruder.get("/comparisons/99999999")
    assert missing.status_code == read.status_code, (
        f"a saved comparison owned by somebody else answers {read.status_code} while "
        f"one that does not exist answers {missing.status_code}. The two refusals must "
        f"be indistinguishable, or an owner can enumerate what others hold"
    )


def test_denied_saved_comparison_leaves_the_stored_row_unchanged():
    owner = conftest.session(conftest.OWNER_ONE)
    original = conftest.unique("untouched-set")
    made = owner.post("/comparisons", json={
        "name": original,
        "variant_keys": ["Corsa"],
        "facet_state": {"series": "900"},
    })
    saved_id = made.json().get("id")

    intruder = conftest.session(conftest.OWNER_TWO)
    renamed = intruder.patch(f"/comparisons/{saved_id}", json={"name": "taken-over"})
    assert renamed.status_code in (403, 404), (
        f"{conftest.OWNER_TWO} renamed another owner's saved comparison with "
        f"{renamed.status_code}"
    )
    removed = intruder.delete(f"/comparisons/{saved_id}")
    assert removed.status_code in (403, 404), (
        f"{conftest.OWNER_TWO} deleted another owner's saved comparison with "
        f"{removed.status_code}"
    )
    still = conftest.session(conftest.OWNER_ONE).get(f"/comparisons/{saved_id}")
    assert still.status_code == 200, (
        f"the owner can no longer read their own saved comparison after the refused "
        f"requests: {still.status_code}"
    )
    assert original in str(still.json()), (
        f"the refused rename changed the stored row: expected the name {original!r}, "
        f"got {still.json()}"
    )


def test_anonymous_saved_comparison_request_is_denied():
    client = conftest.anonymous()
    listed = client.get("/comparisons")
    assert listed.status_code in (401, 403), (
        f"an anonymous caller listed saved comparisons with {listed.status_code}: "
        f"{listed.text[:300]}"
    )
    before = conftest.backend_count("saved_comparisons")
    made = client.post("/comparisons", json={
        "name": conftest.unique("anon-set"),
        "variant_keys": ["Corsa"],
        "facet_state": {"series": "900"},
    })
    assert made.status_code in (401, 403), (
        f"an anonymous caller saved a comparison with {made.status_code}"
    )
    after = conftest.backend_count("saved_comparisons")
    assert after == before, (
        f"the refused anonymous save wrote a row anyway: saved_comparisons went from "
        f"{before} to {after}"
    )


def test_markets_are_grouped_by_stored_region_key():
    client = conftest.anonymous()
    response = client.get("/markets")
    assert response.status_code == 200, (
        f"GET /api/markets returned {response.status_code}: {response.text[:300]}"
    )
    payload = response.json()
    assert isinstance(payload, list), (
        f"GET /api/markets must return a top-level JSON array, got "
        f"{type(payload).__name__}"
    )
    keys = {str(m.get("region_key") or m.get("region")) for m in payload}
    for region in conftest.REGIONS:
        assert region in keys, (
            f"no market carries the region key {region!r}; the selector renders its "
            f"seven groups from this field rather than from a fixed list. Present: "
            f"{sorted(keys)}"
        )
    locales = {str(m.get("locale_segment") or m.get("locale")) for m in payload}
    assert conftest.DEFAULT_LOCALE in locales, (
        f"the default locale {conftest.DEFAULT_LOCALE!r} is absent from the markets"
    )


def test_storage_choice_persists_across_a_reload():
    client = httpx.Client(base_url=appclient.api_base(), timeout=conftest.TIMEOUT)
    recorded = client.post("/consent", json={"storage_choice": "necessary"})
    assert recorded.status_code in (200, 201), (
        f"POST /api/consent returned {recorded.status_code}: {recorded.text[:300]}"
    )
    read_back = client.get("/consent")
    assert read_back.status_code == 200, (
        f"the recorded storage choice could not be read back: {read_back.status_code}"
    )
    body = str(read_back.json())
    assert "necessary" in body, (
        f"the storage choice did not survive: {body[:300]}. The answer persists so the "
        f"panel does not return"
    )


def test_privacy_route_is_reachable_from_the_footer():
    home = httpx.get(f"{appclient.app_url()}/{conftest.DEFAULT_LOCALE}",
                     timeout=conftest.TIMEOUT)
    assert home.status_code == 200, (
        f"the home route returned {home.status_code}: {home.text[:300]}"
    )
    refs = conftest.asset_refs(home.text)
    assert any("privacy" in ref for ref in refs), (
        f"no privacy link is present on the home route; the legal row is in the footer "
        f"of every route. Links found: {refs[:40]}"
    )
    privacy = httpx.get(f"{appclient.app_url()}/{conftest.DEFAULT_LOCALE}/privacy",
                        timeout=conftest.TIMEOUT)
    assert privacy.status_code == 200, (
        f"the privacy route returned {privacy.status_code}: {privacy.text[:300]}"
    )
    text = conftest.visible_text(privacy.text).lower()
    assert len(text) > 400, (
        f"the privacy route carries {len(text)} characters of prose; it states what the "
        f"product stores about a visitor"
    )


def test_every_response_carries_the_security_headers():
    for route in conftest.PUBLIC_ROUTES:
        response = httpx.get(f"{appclient.app_url()}{route}", timeout=conftest.TIMEOUT)
        lowered = {k.lower(): v for k, v in response.headers.items()}
        for header in conftest.SECURITY_HEADERS:
            assert header in lowered, (
                f"{route} answered without the {header} header; every response carries "
                f"the standard security headers. Present: {sorted(lowered)}"
            )
        assert lowered.get("x-content-type-options", "").lower() == "nosniff", (
            f"{route} sets x-content-type-options to "
            f"{lowered.get('x-content-type-options')!r}, expected 'nosniff'"
        )


def test_sitemap_lists_every_public_route():
    response = httpx.get(f"{appclient.app_url()}/sitemap.xml", timeout=conftest.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /sitemap.xml returned {response.status_code}: {response.text[:300]}"
    )
    body = response.text
    for route in conftest.PUBLIC_ROUTES:
        assert route in body, (
            f"the public route {route} is absent from the sitemap. A sitemap lists "
            f"every public route"
        )


def test_robots_names_the_sitemap():
    response = httpx.get(f"{appclient.app_url()}/robots.txt", timeout=conftest.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /robots.txt returned {response.status_code}: {response.text[:300]}"
    )
    assert "sitemap" in response.text.lower(), (
        f"the robots file does not name the sitemap: {response.text[:300]}"
    )


def test_body_text_meets_contrast_in_both_schemes():
    browser = capabilities.make_browser()
    findings = []
    for scheme in ("light", "dark"):
        page = browser.open(f"{appclient.app_url()}/{conftest.DEFAULT_LOCALE}",
                            color_scheme=scheme)
        sample = page.computed_style("body", ("color", "background-color"))
        ratio = conftest.relative_contrast(
            capabilities.parse_rgb(sample["color"]),
            capabilities.parse_rgb(sample["background-color"]),
        )
        if ratio < conftest.CONTRAST_FLOOR:
            findings.append(f"{scheme} scheme: body text contrast is {ratio:.2f}")
    assert not findings, (
        f"body text falls below the WCAG AA contrast floor of "
        f"{conftest.CONTRAST_FLOOR}: {'; '.join(findings)}. Body text uses the primary "
        f"token against the ground in both schemes and nothing quieter"
    )


def test_hero_headline_renders_before_any_video_byte():
    browser = capabilities.make_browser()
    page = browser.open(f"{appclient.app_url()}/{conftest.DEFAULT_LOCALE}",
                        block=("video", "media"))
    text = conftest.visible_text(page.content())
    assert conftest.HERO_ACTION in text, (
        f"the hero call to action {conftest.HERO_ACTION!r} is absent when video is "
        f"blocked; the headline and its action are readable before any video byte is "
        f"requested: {text[:400]}"
    )
    assert len(text) > 400, (
        f"the home route rendered {len(text)} characters with video blocked; the route "
        f"stays complete and usable when the film never plays"
    )
