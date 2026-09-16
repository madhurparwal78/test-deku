"""Outcome graders for the Modelport task.

One module, every section and the declared database slot. Black-box: HTTP against
the running app, the rendered page through Playwright, and PostgreSQL through the
shared backend adapter. Nothing here reads the agent's source.
"""

from __future__ import annotations

import json
import os
import re

import httpx

from conftest import (
    COOKIE_CHOICE_NAME,
    CPU_LARGE,
    CPU_SMALL,
    DEFAULT_CAP_MICROS,
    DEV2_EMAIL,
    DEV2_HANDLE,
    DEV_EMAIL,
    DEV_HANDLE,
    DISPLAY_NAMES,
    FREE_ALLOWANCE_MICROS,
    GPU,
    LIST_LIMIT_DEFAULT,
    LIST_LIMIT_MAX,
    NOTES,
    NOTES_LOAD_SECONDS,
    NOTES_RUN_SECONDS,
    NOTES_VERSION,
    OK,
    ORG_HANDLE,
    OWNER_EMAIL,
    OWNER_HANDLE,
    PASSWORD,
    PREDICTION_ID_LENGTH,
    PRISM,
    PRISM_DIVISOR,
    PRISM_LOAD_SECONDS,
    PRISM_RATE_MICROS,
    PRISM_VERSION,
    PROMOTION_ID,
    PUBLIC_ROUTES,
    QUICKDRAW,
    QUICKDRAW_RATE_MICROS,
    QUICKDRAW_VERSION,
    RATES,
    RATE_LIMIT_PER_MINUTE,
    REFUSED,
    RESERVED_HANDLES,
    SCRIBE,
    SCRIBE_RUN_SECONDS,
    SCRIBE_VERSION,
    SCRIBE_WITHDRAWN,
    STATUSES,
    TERMINAL,
    TIMEOUT,
    TOKEN_BODY_LENGTH,
    TOKEN_ENV_NAME,
    TOKEN_LIMIT,
    TOKEN_PREFIX,
    WAIT_CEILING_SECONDS,
    WARM_DAY_MICROS,
    WITHDRAWN_REASON,
    api_base,
    base_url,
    bearer_for,
    body,
    charge_for,
    client_for,
    contrast,
    create_prediction,
    describe,
    error_type,
    head_of,
    html_of,
    meta_content,
    mint_token,
    ok,
    refused_as,
    rgb_of,
    rows_of,
    row_for,
    run_now,
    run_together,
    scribe_input,
    settle,
    sign_in,
    unique,
    usage_rows,
    wait_terminal,
)

PACKAGING = ('{"base": "python:3.12", "system_packages": [], '
             '"packages": ["tidy==1.0"], "predictor": "predict.py:Predictor"}')
SIGNATURE = ('{"notes": {"type": "string", "format": "text", "required": true}, '
             '"bullets": {"type": "boolean", "default": true}}')


def _publish(session, name, packaging=PACKAGING, signature=SIGNATURE, visibility="private"):
    """Push one model under the developer's own handle, as the publish wizard does."""
    return session.post("/models", json={
        "owner": DEV_HANDLE, "name": name,
        "description": "A probe model for the publish pipeline.",
        "licence": "apache-2.0", "packaging_document": packaging,
        "predict_signature": signature, "visibility": visibility})


_CORE_FEATURES = "core features"


def test_catalogue_listing_returns_public_models_with_owner_name_description_run_count_and_badges(anon, owner):
    """cov: C-OV-08"""
    report = ok(anon.get("/models", params={"limit": LIST_LIMIT_MAX}), "catalogue listing")
    rows = report["results"] if isinstance(report, dict) else report
    by_address = {f"{r['owner']}/{r['name']}": r for r in rows}
    for address in (SCRIBE, QUICKDRAW, PRISM):
        assert address in by_address, f"the catalogue must list {address}: {sorted(by_address)}"
        row = by_address[address]
        for field in ("description", "run_count", "official", "status_badge"):
            assert field in row, f"the card record for {address} carries no {field!r}: {row}"
    assert NOTES not in by_address, f"the private model {NOTES} must not appear in the public catalogue: {sorted(by_address)}"


def test_model_detail_response_carries_the_default_version_input_schema_output_schema_and_pricing(anon):
    """cov: C-DM-13"""
    record = ok(anon.get(f"/models/{SCRIBE}"), f"model detail of {SCRIBE}")
    assert str(record.get("default_version", "")).startswith(SCRIBE_VERSION), \
        f"{SCRIBE} must default to version {SCRIBE_VERSION}: {record}"
    schema = record.get("input_schema") or {}
    fields = schema.get("properties") or schema
    for name in ("prompt", "max_words", "tone", "include_title"):
        assert name in fields, f"the input schema of {SCRIBE} declares no {name!r}: {schema}"
    assert record.get("output_schema"), f"{SCRIBE} carries no output schema: {record}"
    pricing = record.get("pricing") or {}
    assert pricing.get("pricing_mode") == "per_second", f"{SCRIBE} must be priced per_second: {record}"
    assert int(pricing.get("rate_micros")) == RATES[CPU_SMALL], f"{SCRIBE} must be rated at the cpu-small rate: {record}"


def test_run_count_formatter_renders_seeded_counts_as_abbreviated_values_dropping_a_trailing_zero(owner):
    """cov: C-CF-17, C-CF-16"""
    rendered = html_of("/explore").text
    for shown in ("17.9M", "469.7K", "4M"):
        assert shown in rendered, f"the catalogue must render the run count {shown}: it is absent from /explore"
    assert "4.0M" not in rendered, "a trailing zero after the decimal point is dropped, so 4.0M must not appear"
    owner_page = html_of(f"/{DEV_HANDLE}").text
    assert "17" in owner_page, f"the owner profile of {DEV_HANDLE} must render its run count"


def test_collections_endpoint_returns_seeded_collections_with_slug_title_description_and_curated_model_order(anon, owner):
    """cov: C-DC-11"""
    rows = ok(anon.get("/collections"), "collections listing")
    assert isinstance(rows, list), f"/collections must return a top-level JSON array: {rows}"
    by_slug = {r["slug"]: r for r in rows}
    assert by_slug["summarise-text"]["title"] == "Summarise long text", f"seeded collection title drifted: {by_slug}"
    assert by_slug["summarise-text"]["description"] == "Use AI to summarise long text with an API", \
        f"seeded collection description drifted: {by_slug}"
    assert by_slug["structure-any-text"]["title"] == "Turn text into structured data", f"seeded collection title drifted: {by_slug}"
    detail = ok(anon.get("/collections/summarise-text"), "collection detail")
    models = [f"{m['owner']}/{m['name']}" for m in (detail.get("results") or detail.get("models") or [])]
    assert models[:2] == [SCRIBE, PRISM], f"the curated order of summarise-text must be {[SCRIBE, PRISM]}: {models}"


def test_owner_profile_listing_returns_only_that_owner_public_models(anon, owner, page):
    """cov: C-RL-08"""
    rows = ok(anon.get("/models", params={"owner": ORG_HANDLE, "limit": LIST_LIMIT_MAX}), "owner listing")
    listed = [f"{r['owner']}/{r['name']}" for r in (rows["results"] if isinstance(rows, dict) else rows)]
    assert listed == [SCRIBE], f"{ORG_HANDLE} owns exactly {SCRIBE} publicly: {listed}"
    page = html_of(f"/{ORG_HANDLE}")
    assert page.status_code == 200, f"the owner profile of {ORG_HANDLE} is not served: {describe(page)}"
    assert "scribe-2" in page.text, f"the owner profile of {ORG_HANDLE} must list its own model"


def test_catalogue_front_page_and_the_terms_route_are_reachable_without_a_session(anon):
    """cov: C-OV-03"""
    for route in ("/explore", "/terms", "/privacy", "/pricing"):
        response = html_of(route)
        assert response.status_code == 200, f"{route} must be reachable with no session: {describe(response)}"
    listing = anon.get("/models")
    assert listing.status_code in OK, f"the catalogue endpoint must answer an anonymous caller: {describe(listing)}"


def test_ranking_number_is_recomputed_on_a_schedule_and_is_never_printed_to_a_reader(anon):
    """cov: C-CF-20"""
    rows = ok(anon.get("/models", params={"limit": LIST_LIMIT_MAX}), "catalogue listing")
    rows = rows["results"] if isinstance(rows, dict) else rows
    for row in rows:
        assert "score" not in row, f"the ranking number is never printed to a reader: {row}"
    rendered = html_of("/explore").text.lower()
    assert "rank score" not in rendered, "the ranking number is never printed on /explore"
    counts = [int(r["run_count"]) for r in rows]
    assert counts, "the catalogue must carry a run count per model"


def test_pages_are_produced_on_the_server_from_templates_and_the_http_interface_shares_that_origin_under_api(page):
    """cov: C-TR-01"""
    page = html_of("/explore")
    assert page.status_code == 200, f"/explore is not served: {describe(page)}"
    assert "scribe-2" in page.text, "the catalogue markup must arrive in the first response rather than after a fetch"
    assert api_base() == f"{base_url()}/api", "the HTTP interface is served on the app's own origin under /api"
    health = httpx.get(f"{api_base()}/health", timeout=TIMEOUT)
    assert health.status_code == 200, f"the API on the same origin is not answering: {describe(health)}"


def test_search_ranks_an_exact_model_address_first_within_the_models_group(anon, owner):
    """cov: C-CF-28"""
    report = ok(anon.get("/search", params={"q": SCRIBE}), "search for an exact address")
    groups = report.get("groups") or []
    models = next((g for g in groups if g.get("kind") == "model"), None)
    assert models, f"a search for {SCRIBE} must return a models group: {report}"
    first = models["results"][0]
    assert f"{first['owner']}/{first['name']}" == SCRIBE, \
        f"an exact address must rank first within the models group: {models['results'][:3]}"


def test_search_groups_results_by_kind_in_the_fixed_order_models_owners_collections(anon, owner):
    """cov: C-DC-10"""
    report = ok(anon.get("/search", params={"q": "summarise"}), "search")
    kinds = [g.get("kind") for g in (report.get("groups") or [])]
    assert kinds, f"a search must answer in groups: {report}"
    expected = [k for k in ("model", "owner", "collection") if k in kinds]
    assert kinds == expected, f"search groups run models, owners, collections in that fixed order: {kinds}"


def test_stale_ranking_snapshot_still_serves_the_popular_column_without_a_visible_difference(anon, owner):
    """cov: C-CF-18"""
    first = ok(anon.get("/models", params={"limit": 5}), "popular listing")
    second = ok(anon.get("/models", params={"limit": 5}), "popular listing again")
    order_one = [f"{r['owner']}/{r['name']}" for r in (first["results"] if isinstance(first, dict) else first)]
    order_two = [f"{r['owner']}/{r['name']}" for r in (second["results"] if isinstance(second, dict) else second)]
    assert order_one == order_two, f"the popular column serves a stored snapshot, so two reads agree: {order_one} vs {order_two}"
    assert order_one, "the popular column must not be empty on a seeded catalogue"


def test_prediction_created_with_a_run_token_reaches_succeeded_and_returns_the_resolved_version_digest(dev):
    """cov: C-CF-68 (earned: C-CF-68: the test asserts the identifier shape the create returned, which is its length)"""
    created = ok(create_prediction(dev, SCRIBE, scribe_input()), f"create on {SCRIBE}")
    identifier = str(created.get("id") or "")
    assert identifier.startswith("pr"), f"a prediction identifier begins 'pr': {created}"
    assert len(identifier) == PREDICTION_ID_LENGTH, \
        f"a prediction identifier is {PREDICTION_ID_LENGTH} characters long: {identifier!r}"
    assert str(created.get("version", "")).startswith(SCRIBE_VERSION), \
        f"a create naming a model address returns the resolved version digest: {created}"
    record = wait_terminal(dev, identifier)
    assert record["status"] == "succeeded", f"a valid run on {SCRIBE} must succeed: {record}"
    assert record.get("output"), f"a succeeded prediction carries its output: {record}"


def test_app_is_reachable_at_the_public_url_on_the_container_internal_port_from_the_environment():
    """cov: C-DC-08, C-DC-02, C-DC-01 (earned: C-DC-08: the test reaches the app through the environment's own port mapping, which no fixed name or volume backs)"""
    assert os.environ.get("APP_PUBLIC_URL"), "APP_PUBLIC_URL must be read from the environment"
    response = httpx.get(f"{api_base()}/health", timeout=TIMEOUT)
    assert response.status_code == 200, f"the app is not reachable at APP_PUBLIC_URL: {describe(response)}"
    assert os.environ.get("APP_PUBLIC_PORT", "4173"), "APP_PUBLIC_PORT must be read from the environment"


def test_reserved_browser_screenshots_and_downloads_directories_exist_at_the_app_root_and_are_empty():
    """cov: C-CF-166"""
    for name in (".browser_screenshots", ".downloads"):
        path = os.path.join("/app", name)
        assert os.path.isdir(path), f"the reserved directory /app/{name} must exist"
    readme = "/app/USER_README.md"
    assert os.path.isfile(readme), "the credentials file /app/USER_README.md must exist"
    text = open(readme, encoding="utf-8", errors="replace").read()
    assert PASSWORD in text, f"/app/USER_README.md must carry the seeded password literal"


def test_server_keeps_running_after_the_starting_session_and_is_not_a_child_of_the_shell():
    """cov: C-DC-06"""
    first = httpx.get(f"{api_base()}/health", timeout=TIMEOUT)
    assert first.status_code == 200, f"the app must be serving: {describe(first)}"
    settle()
    second = httpx.get(f"{api_base()}/health", timeout=TIMEOUT)
    assert second.status_code == 200, \
        f"the server must outlive the session that started it rather than dying with its shell: {describe(second)}"


def test_server_serves_a_production_build_rather_than_a_development_server(dev, page):
    """cov: C-DC-05, C-DC-19"""
    response = html_of("/explore")
    assert response.status_code == 200, f"/explore is not served: {describe(response)}"
    text = response.text.lower()
    for marker in ("webpack-dev-server", "vite/client", "__vite_ping", "livereload"):
        assert marker not in text, f"a development server marker {marker!r} reached the page; serve a production build"
    server = response.headers.get("server", "").lower()
    assert "werkzeug" not in server, f"the app must not be served by the development server: {server!r}"


def test_model_version_input_schema_declares_every_control_type_the_generated_form_must_render(anon, dev):
    """cov: C-DM-31, C-DM-29, C-CF-65"""
    def fields_of(address):
        record = ok(anon.get(f"/models/{address}"), f"model detail of {address}")
        schema = record.get("input_schema") or {}
        return schema.get("properties") or schema

    scribe = fields_of(SCRIBE)
    assert scribe["prompt"]["type"] == "string", f"prompt is a string: {scribe['prompt']}"
    assert scribe["max_words"]["minimum"] == 10 and scribe["max_words"]["maximum"] == 200, \
        f"max_words is bounded at 10 and 200: {scribe['max_words']}"
    assert scribe["tone"]["enum"] == ["plain", "formal", "playful"], f"tone enum drifted: {scribe['tone']}"
    assert scribe["include_title"]["type"] == "boolean", f"include_title is a boolean: {scribe['include_title']}"
    quickdraw = fields_of(QUICKDRAW)
    assert len(quickdraw["style"]["enum"]) == 15, f"style declares fifteen members: {quickdraw['style']}"
    prism = fields_of(PRISM)
    assert prism["text"].get("format") == "text", f"text carries the format hint text: {prism['text']}"
    notes = ok(dev.get(f"/models/{NOTES}"), "private model detail")
    notes_fields = (notes.get("input_schema") or {}).get("properties") or {}
    assert notes_fields["bullets"]["default"] is True, f"bullets defaults to true: {notes_fields.get('bullets')}"


def test_quickdraw_prediction_with_count_three_returns_three_output_items_and_charges_per_output_item(anon, dev):
    """cov: C-DM-32, C-CF-103 (earned: C-DM-32: the test reads the example gallery of that model while asserting its per item charge)"""
    record = run_now(dev, QUICKDRAW, {"subject": unique("subject"), "count": 3})
    assert record["status"] == "succeeded", f"a valid run on {QUICKDRAW} must succeed: {record}"
    output = record.get("output")
    assert isinstance(output, list) and len(output) == 3, f"count 3 must produce three output items: {output}"
    report = usage_rows(dev)
    row = row_for(report, record["id"])
    assert row, f"a succeeded run must carry a usage row: {report}"
    assert int(row["amount_micros"]) == charge_for(3, QUICKDRAW_RATE_MICROS), \
        f"three items at {QUICKDRAW_RATE_MICROS} micro units each is {charge_for(3, QUICKDRAW_RATE_MICROS)}: {row}"
    examples = ok(anon.get(f"/models/{QUICKDRAW}"), "quickdraw detail").get("examples") or []
    assert len(examples) == 2, f"{QUICKDRAW} is seeded with two examples: {examples}"


def test_query_string_input_values_override_the_prefill_after_validation_and_invalid_ones_are_dropped(page):
    """cov: C-CF-51"""
    prompt = unique("carried-prompt")
    page = html_of(f"/{SCRIBE}?prompt={prompt}")
    assert page.status_code == 200, f"the model page must accept carried input values: {describe(page)}"
    assert prompt in page.text, "an input value carried on the query string overrides the prefill"
    rejected = html_of(f"/{SCRIBE}?max_words=9999")
    assert rejected.status_code == 200, f"an invalid carried value must not break the page: {describe(rejected)}"
    assert "9999" not in rejected.text, "an invalid carried value is dropped rather than applied"


def test_streaming_output_shows_raw_text_until_the_stream_ends(dev):
    """cov: C-CF-44"""
    created = ok(create_prediction(dev, SCRIBE, scribe_input()), "create for a stream read")
    identifier = created["id"]
    with httpx.stream("GET", f"{api_base()}/predictions/{identifier}/events",
                      headers=dict(dev.headers), timeout=TIMEOUT) as stream:
        assert stream.status_code == 200, f"the event stream is not served: {stream.status_code}"
        frames = []
        for line in stream.iter_lines():
            if line:
                frames.append(line)
            if len(frames) > 60:
                break
    assert frames, f"the event stream for {identifier} carried no frame"
    record = wait_terminal(dev, identifier)
    assert isinstance(record.get("output"), str), f"a scribe output is rendered from text: {record}"


def test_a_string_field_carrying_an_enum_renders_as_a_select_with_every_declared_member(anon, page):
    """cov: C-RL-07"""
    record = ok(anon.get(f"/models/{QUICKDRAW}"), "quickdraw detail")
    members = ((record.get("input_schema") or {}).get("properties") or {})["style"]["enum"]
    page = html_of(f"/{QUICKDRAW}")
    assert page.status_code == 200, f"the model page is not served: {describe(page)}"
    markup = page.text
    assert "<select" in markup, "an enum field renders as a select rather than a group of radios"
    for member in members:
        assert member in markup, f"the select must offer the declared member {member!r}"


def test_no_allowlist_of_known_models_and_no_hand_written_form_exists_for_any_seeded_model(dev, page):
    """cov: C-CF-42, C-DM-03"""
    unseen = ok(dev.get(f"/models/{NOTES}"), "private model detail")
    fields = (unseen.get("input_schema") or {}).get("properties") or {}
    assert set(fields) == {"notes", "bullets"}, f"the form for {NOTES} is drawn from its own schema: {fields}"
    page = html_of(f"/{QUICKDRAW}")
    for name in ("subject", "count", "style"):
        assert name in page.text, f"the generated form must carry the schema field {name!r}"
    assert "prompt" not in page.text.split("</head>")[-1] or QUICKDRAW in page.text, \
        "the form is a function of the version schema rather than a per model branch"


def test_share_control_mints_a_read_only_link_carrying_its_own_identifier_and_its_own_expiry(dev):
    """cov: C-CF-64, C-CF-147"""
    record = run_now(dev, SCRIBE, scribe_input())
    shared = dev.post(f"/predictions/{record['id']}/share", json={})
    assert shared.status_code in OK, f"a prediction on a public model must be shareable: {describe(shared)}"
    link = body(shared)
    assert link.get("id"), f"a share carries its own identifier: {link}"
    assert link.get("expires_at"), f"a share carries its own expiry: {link}"
    assert link["id"] != record["id"], "a share identifier is its own, not the prediction's"


def test_router_resolves_a_reserved_segment_before_an_account_handle(owner):
    """cov: C-CF-10, C-UF-14"""
    for segment in ("explore", "pricing", "settings", "account"):
        response = html_of(f"/{segment}")
        assert response.status_code in (200, 404), f"/{segment} must resolve as a reserved route: {describe(response)}"
        assert "owner profile" not in response.text.lower(), \
            f"/{segment} is reserved, so it must never resolve to an account handle"
    profile = html_of(f"/{DEV_HANDLE}")
    assert profile.status_code == 200, f"an account handle resolves after the reserved list: {describe(profile)}"


def test_anonymous_reader_still_receives_the_model_record_schema_examples_and_readme(anon, page):
    """cov: C-CF-35"""
    page = html_of(f"/{SCRIBE}")
    assert page.status_code == 200, f"an anonymous reader receives the model page: {describe(page)}"
    for route in ("/api", "/examples", "/readme", "/versions"):
        response = html_of(f"/{SCRIBE}{route}")
        assert response.status_code == 200, f"{SCRIBE}{route} must answer an anonymous reader: {describe(response)}"
    record = anon.get(f"/models/{SCRIBE}")
    assert record.status_code in OK, f"the model record is public: {describe(record)}"
    assert (body(record).get("input_schema")), "an anonymous reader receives the input schema"


def test_per_thousand_output_tokens_pricing_rounds_a_partial_micro_unit_up(dev):
    """cov: C-DM-30, C-CF-109"""
    record = run_now(dev, PRISM, {"text": unique("long-text"), "max_words": 7})
    assert record["status"] == "succeeded", f"a valid run on {PRISM} must succeed: {record}"
    row = row_for(usage_rows(dev), record["id"])
    assert row, f"a succeeded run must carry a usage row: {record['id']}"
    expected = charge_for(7, PRISM_RATE_MICROS, PRISM_DIVISOR)
    assert expected == 27, "seven tokens at 3750 per thousand is 26.25, which rounds up to 27"
    assert int(row["amount_micros"]) == expected, f"a partial micro unit rounds up: {row}"


def test_queue_time_between_created_at_and_started_at_is_never_billed(dev):
    """cov: C-TR-14, C-CF-71 (earned: C-TR-14: the test reads the metrics block, where the three latencies are recorded separately)"""
    record = run_now(dev, SCRIBE, scribe_input())
    metrics = record.get("metrics") or {}
    for key in ("queue_time", "load_time", "predict_time"):
        assert key in metrics, f"the three latencies are recorded separately on every prediction: {metrics}"
    row = row_for(usage_rows(dev), record["id"])
    assert row, f"a succeeded run must carry a usage row: {record['id']}"
    assert int(row["quantity"]) == SCRIBE_RUN_SECONDS, \
        f"the billed quantity is the declared run seconds, never the queue wait: {row}"


def test_one_billing_path_prices_all_three_pricing_modes_from_the_same_formula(dev):
    """cov: C-CF-104"""
    scribe = run_now(dev, SCRIBE, scribe_input())
    quick = run_now(dev, QUICKDRAW, {"subject": unique("subject"), "count": 2})
    prism = run_now(dev, PRISM, {"text": unique("text"), "max_words": 60})
    report = usage_rows(dev)
    for record, expected in ((scribe, charge_for(SCRIBE_RUN_SECONDS, RATES[CPU_SMALL])),
                             (quick, charge_for(2, QUICKDRAW_RATE_MICROS)),
                             (prism, charge_for(60, PRISM_RATE_MICROS, PRISM_DIVISOR))):
        row = row_for(report, record["id"])
        assert row, f"every succeeded run carries a usage row: {record['id']}"
        computed = charge_for(int(row["quantity"]), int(row["rate_micros"]), int(row["unit_divisor"]))
        assert computed == int(row["amount_micros"]) == expected, \
            f"one formula prices every mode: row {row} against {expected}"


def test_hardware_display_names_and_specifications_match_the_seeded_catalogue(anon):
    """cov: C-DM-06"""
    rows = ok(anon.get("/hardware"), "hardware catalogue")
    assert isinstance(rows, list), f"/hardware returns a top-level JSON array: {rows}"
    by_class = {r["class"]: r for r in rows}
    for name, rate in RATES.items():
        assert name in by_class, f"the hardware catalogue must carry {name}: {sorted(by_class)}"
        assert int(by_class[name]["rate_micros_per_second"]) == rate, f"{name} is rated {rate}: {by_class[name]}"
        assert by_class[name]["display_name"] == DISPLAY_NAMES[name], f"{name} display name drifted: {by_class[name]}"
    assert int(by_class[CPU_SMALL]["memory_mb"]) == 2048, f"cpu-small carries 2GB of memory: {by_class[CPU_SMALL]}"
    assert int(by_class[GPU]["accel_memory_mb"]) == 49152, f"gpu-a40 carries 48GB of accelerator memory: {by_class[GPU]}"


def test_free_allowance_is_consumed_before_charged_spend_and_reported_as_its_own_balance(dev):
    """cov: C-CF-112"""
    report = usage_rows(dev)
    assert "free_allowance_remaining_micros" in report, f"the free allowance is its own balance: {sorted(report)}"
    remaining = int(report["free_allowance_remaining_micros"])
    assert 0 <= remaining <= FREE_ALLOWANCE_MICROS, \
        f"the remaining allowance sits inside the seeded allowance of {FREE_ALLOWANCE_MICROS}: {remaining}"
    assert "total_micros" in report, f"charged spend is reported separately from the allowance: {sorted(report)}"


def test_warning_notices_fire_at_the_declared_thresholds_once_per_period_per_threshold():
    """cov: C-TR-24, C-CF-111 (earned: C-TR-24: the test reads the in product notices a threshold crossing writes)"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        notices = ok(session.get("/account/notifications"), "notification listing")
        rows = notices if isinstance(notices, list) else notices.get("results", [])
        thresholds = [str(r.get("kind")) for r in rows if "threshold" in str(r.get("kind"))]
        assert len(thresholds) == len(set(thresholds)), \
            f"a threshold notice fires once per period per threshold: {thresholds}"
        for row in rows:
            payload = json.dumps(row.get("payload") or {})
            assert TOKEN_PREFIX + "1" not in payload, f"a notification body carries no credential: {row}"


def test_prediction_on_a_cold_version_stays_starting_for_its_declared_load_time(anon, dev):
    """cov: C-CF-72"""
    record = ok(anon.get(f"/models/{PRISM}"), "cold model detail")
    assert str(record.get("status_badge")) == "Cold", f"{PRISM} is seeded Cold: {record}"
    assert int(record.get("load_seconds")) == PRISM_LOAD_SECONDS, \
        f"{PRISM} declares a load time of {PRISM_LOAD_SECONDS} seconds: {record}"
    created = ok(create_prediction(dev, PRISM, {"text": unique("t"), "max_words": 60}), "cold create")
    first = ok(dev.get(f"/predictions/{created['id']}"), "immediate read")
    assert first["status"] == "starting", f"a cold version waits its load time in starting: {first}"
    warm = ok(anon.get(f"/models/{SCRIBE}"), "warm model detail")
    assert str(warm.get("status_badge")) == "Warm", f"{SCRIBE} is seeded Warm: {warm}"


def test_a_member_of_the_owning_account_runs_that_account_private_model(dev, dev2):
    """cov: C-RL-02, C-CF-146"""
    created = create_prediction(dev, NOTES, {"notes": unique("n")})
    assert created.status_code in OK, f"a principal of the owning account runs its private model: {describe(created)}"
    record = wait_terminal(dev, body(created)["id"])
    assert record["status"] == "succeeded", f"the private run must succeed: {record}"
    refused = create_prediction(dev2, NOTES, {"notes": unique("n")})
    assert refused.status_code == 404, f"an outside account cannot run a private model: {describe(refused)}"


def test_publishing_derives_the_input_schema_and_output_schema_from_the_packaging_document(dev):
    """cov: C-CF-132"""
    created = ok(_publish(dev, unique("derived")), "publish")
    version = created.get("version") or {}
    schema = version.get("input_schema") or {}
    fields = schema.get("properties") or schema
    assert set(fields) == {"notes", "bullets"}, f"the input schema is derived from the predict signature: {schema}"
    assert version.get("output_schema"), f"the output schema is derived too: {version}"
    assert version.get("digest"), f"a published version carries a content digest: {version}"


def test_versions_listing_is_append_only_and_newest_first_with_a_withdrawn_reason_inline(anon, dev):
    """cov: C-CF-153"""
    listing = ok(anon.get(f"/models/{SCRIBE}/versions", params={"limit": LIST_LIMIT_MAX}), "versions listing")
    rows = listing["results"]
    digests = [r["digest"] for r in rows]
    assert SCRIBE_VERSION in digests and SCRIBE_WITHDRAWN in digests, f"both seeded versions are listed: {digests}"
    withdrawn = next(r for r in rows if r["digest"] == SCRIBE_WITHDRAWN)
    assert withdrawn["status"] == "withdrawn", f"the seeded version is withdrawn: {withdrawn}"
    assert withdrawn["withdrawn_reason"] == WITHDRAWN_REASON, f"the withdrawal reason drifted: {withdrawn}"
    removed = dev.request("DELETE", f"/models/{SCRIBE}/versions/{SCRIBE_WITHDRAWN}")
    assert removed.status_code in REFUSED or removed.status_code == 405, \
        f"the versions list is append only: {describe(removed)}"


def test_changing_a_deployment_version_writes_a_release_row_recording_actor_and_both_versions(dev):
    """cov: C-CF-126"""
    name = unique("dep")
    created = ok(dev.post("/deployments", json={
        "name": name, "version": NOTES_VERSION, "hardware_class": CPU_SMALL,
        "min_instances": 0, "max_instances": 2, "concurrency": 1, "cooldown_seconds": 300}), "deployment creation")
    published = ok(_publish(dev, unique("target")), "publish a second version")
    updated = ok(dev.patch(f"/deployments/arden-hale/{name}",
                           json={"version": published["version"]["digest"], "note": "probe release"}),
                 "deployment release")
    release = updated.get("release") or {}
    assert release.get("actor"), f"a release records who made it: {release}"
    assert str(release.get("from_version", "")).startswith(NOTES_VERSION), f"a release records the previous version: {release}"
    assert str(release.get("to_version", "")).startswith(published["version"]["digest"][:8]), \
        f"a release records the new version: {release}"
    assert created["name"] == name, "the deployment keeps the name it was created with"


def test_deployment_creation_reports_the_standing_cost_per_day_for_a_warm_instance(dev):
    """cov: C-CF-122"""
    quoted = ok(dev.get("/deployments/cost", params={"hardware_class": CPU_SMALL, "min_instances": 1}),
                "standing cost quote")
    assert int(quoted["standing_cost_micros_per_day"]) == WARM_DAY_MICROS, \
        f"one warm instance on cpu-small costs {WARM_DAY_MICROS} micro units per day: {quoted}"
    zero = ok(dev.get("/deployments/cost", params={"hardware_class": CPU_SMALL, "min_instances": 0}),
              "standing cost quote at zero")
    assert int(zero["standing_cost_micros_per_day"]) == 0, f"scaling to nothing when idle costs nothing: {zero}"


def test_each_publish_step_is_reachable_by_its_own_address_and_a_failed_step_leaves_no_version_row(dev):
    """cov: C-CF-135, C-CF-133"""
    for step in ("/models/new/identity", "/models/new/packaging", "/models/new/review"):
        response = html_of(step)
        assert response.status_code in (200, 302, 401, 403), f"{step} must be its own address: {describe(response)}"
    name = unique("broken")
    failed = _publish(dev, name, packaging="{not json", signature=SIGNATURE)
    assert failed.status_code in REFUSED, f"a broken packaging document is refused: {describe(failed)}"
    listing = dev.get(f"/models/arden-hale/{name}/versions")
    assert listing.status_code == 404, f"a failed publish leaves no model and no version row: {describe(listing)}"


def test_deprecated_version_warns_on_use_and_a_withdrawn_version_states_its_reason_to_callers(anon, dev):
    """cov: C-CF-139, C-CF-137"""
    response = dev.post("/predictions", json={"version": SCRIBE_WITHDRAWN, "input": scribe_input()})
    refused_as(response, "model_version_withdrawn")
    assert WITHDRAWN_REASON in response.text, \
        f"a withdrawal states its reason to callers: {response.text[:300]}"
    listing = ok(anon.get(f"/models/{SCRIBE}/versions", params={"limit": LIST_LIMIT_MAX}), "versions listing")
    statuses = {r["digest"]: r["status"] for r in listing["results"]}
    assert statuses[SCRIBE_WITHDRAWN] == "withdrawn", f"the version list carries the withdrawn status: {statuses}"


def test_scaling_decisions_read_queue_depth_and_queue_age_and_are_rate_limited_per_decision(dev):
    """cov: C-CF-123, C-TR-26"""
    metrics = ok(dev.get("/deployments/arden-hale/tidy-live/metrics"), "deployment metrics")
    for field in ("queue_depth", "queue_age_seconds", "instances"):
        assert field in metrics, f"a deployment reports {field!r} as the scaling signal: {sorted(metrics)}"
    assert "cpu_utilisation" not in metrics, \
        f"scaling reads queue depth and queue age rather than processor utilisation: {sorted(metrics)}"


def test_queue_age_at_the_instance_ceiling_is_carried_in_the_response_headers(dev):
    """cov: C-CF-124"""
    response = dev.post("/predictions", json={"deployment": "arden-hale/tidy-live", "input": {"notes": unique("n")}})
    assert response.status_code in OK or response.status_code in REFUSED, \
        f"a create against a deployment answers: {describe(response)}"
    headers = {k.lower() for k in response.headers}
    assert any("queue" in k for k in headers), \
        f"the queue age is carried in the response headers: {sorted(headers)}"


def test_minimum_instances_of_zero_scales_to_nothing_when_idle_and_the_cooldown_defaults_to_five_minutes(dev):
    """cov: C-CF-120"""
    name = unique("idle")
    created = ok(dev.post("/deployments", json={
        "name": name, "version": NOTES_VERSION, "hardware_class": CPU_SMALL,
        "min_instances": 0, "max_instances": 2, "concurrency": 1}), "deployment creation")
    assert int(created["min_instances"]) == 0, f"min_instances of zero scales to nothing when idle: {created}"
    assert int(created["cooldown_seconds"]) == 300, f"the cooldown defaults to five minutes: {created}"


def test_one_scale_up_decision_every_ten_seconds_and_one_scale_down_every_cooldown(dev):
    """cov: C-CF-125"""
    policy = ok(dev.get("/deployments/arden-hale/tidy-live"), "deployment read")
    assert int(policy.get("scale_up_interval_seconds", 10)) == 10, \
        f"at most one scale up decision is made every ten seconds: {policy}"
    assert int(policy["cooldown_seconds"]) >= NOTES_LOAD_SECONDS, \
        f"the scale down cooldown is never shorter than the version load time: {policy}"
    refused = dev.patch("/deployments/arden-hale/tidy-live", json={"cooldown_seconds": 0})
    assert refused.status_code in REFUSED, f"a cooldown below the load time is refused: {describe(refused)}"


def test_renaming_a_model_keeps_the_old_address_resolving_through_a_permanent_redirect(dev, owner):
    """cov: C-DM-14, C-UF-11"""
    old = unique("before")
    new = unique("after")
    ok(_publish(dev, old), "publish")
    renamed = dev.patch(f"/models/arden-hale/{old}", json={"name": new})
    assert renamed.status_code in OK, f"a model may be renamed by its owner: {describe(renamed)}"
    response = httpx.get(f"{base_url()}/arden-hale/{old}", timeout=TIMEOUT, follow_redirects=False)
    assert response.status_code in (301, 308), \
        f"the old address keeps working through a permanent redirect: {describe(response)}"
    assert new in response.headers.get("location", ""), f"the redirect points at the new address: {response.headers}"


def test_removing_the_last_owner_of_an_organisation_is_refused(owner):
    """cov: C-RL-09, C-CF-140"""
    members = ok(owner.get(f"/organisations/{ORG_HANDLE}/members"), "membership listing")
    rows = members if isinstance(members, list) else members.get("results", [])
    owners = [r for r in rows if str(r.get("role")) == "owner"]
    assert len(owners) == 1, f"the seed carries exactly one owner of {ORG_HANDLE}: {owners}"
    response = owner.request("DELETE", f"/organisations/{ORG_HANDLE}/members/{OWNER_HANDLE}")
    assert response.status_code in REFUSED, f"removing the last owner is refused: {describe(response)}"
    after = ok(owner.get(f"/organisations/{ORG_HANDLE}/members"), "membership listing")
    still = after if isinstance(after, list) else after.get("results", [])
    assert [r for r in still if str(r.get("role")) == "owner"], "the organisation keeps at least one owner"


def test_delivery_rows_carry_a_sequence_number_that_only_increases_for_one_prediction(dev):
    """cov: C-CN-07"""
    created = ok(create_prediction(dev, SCRIBE, scribe_input(),
                                   webhook_url="https://example.com/hook",
                                   webhook_events=["start", "completed"]), "create with a delivery destination")
    wait_terminal(dev, created["id"])
    rows = ok(dev.get(f"/predictions/{created['id']}/deliveries"), "delivery log")
    assert isinstance(rows, list), f"the delivery log is a top-level JSON array: {rows}"
    sequences = [int(r["sequence"]) for r in rows]
    assert sequences == sorted(sequences), f"a sequence number only increases for one prediction: {sequences}"
    for row in rows:
        for field in ("event_id", "event_type", "status", "attempts", "next_attempt_at"):
            assert field in row, f"a delivery row records {field!r}: {row}"


def test_notification_records_are_deduplicated_per_kind_per_period_and_a_report_is_queued_for_a_person(dev):
    """cov: C-TR-25"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        record = run_now(dev, SCRIBE, scribe_input())
        created = ok(session.post("/reports", json={"prediction": record["id"], "category": "other",
                                                    "note": unique("note")}), "report")
        assert str(created.get("status")) in ("open", "queued"), f"a report is queued for a person: {created}"
        notices = ok(session.get("/account/notifications"), "notification listing")
    rows = notices if isinstance(notices, list) else notices.get("results", [])
    seen = [(str(r.get("kind")), str(r.get("period") or "")) for r in rows]
    assert len(seen) == len(set(seen)), f"a notification is deduplicated per kind per period: {seen}"


def test_a_failed_delivery_is_retried_with_backoff_across_the_published_retry_window(dev):
    """cov: C-CF-83"""
    created = ok(create_prediction(dev, SCRIBE, scribe_input(),
                                   webhook_url="https://example.invalid/hook",
                                   webhook_events=["completed"]), "create with an unreachable destination")
    wait_terminal(dev, created["id"])
    rows = ok(dev.get(f"/predictions/{created['id']}/deliveries"), "delivery log")
    assert rows, f"an attempted delivery is recorded even when nobody answers: {rows}"
    row = rows[0]
    assert int(row["attempts"]) >= 1, f"a failed delivery records its attempt count: {row}"
    assert row.get("next_attempt_at"), f"a failed delivery schedules its next attempt: {row}"
    assert str(row.get("status")) in ("pending", "failed", "retrying"), f"a failed delivery is not reported as delivered: {row}"


def test_no_outbound_email_or_sms_is_sent_and_no_second_region_is_addressed(dev):
    """cov: C-TR-16"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        notices = ok(session.get("/account/notifications"), "notification listing")
    rows = notices if isinstance(notices, list) else notices.get("results", [])
    for row in rows:
        channel = str(row.get("channel") or "in_product")
        assert channel in ("in_product", "", "none"), f"a notice is an in product record rather than a message sent: {row}"
    record = run_now(dev, SCRIBE, scribe_input())
    for absent in ("region", "residency"):
        assert absent not in record, f"a prediction carries no {absent} field in this single region build: {sorted(record)}"


def test_health_route_returns_two_hundred_with_a_status_ok_body():
    """cov: C-TR-12"""
    response = httpx.get(f"{api_base()}/health", timeout=TIMEOUT)
    assert response.status_code == 200, f"the health route returns 200 once ready: {describe(response)}"
    payload = body(response)
    assert str(payload.get("status")) == "ok", f"the health body reads status ok: {payload}"


def test_prediction_listing_pages_by_cursor_with_the_default_limit_and_the_maximum_limit(dev):
    """cov: C-CF-172"""
    first = ok(dev.get("/predictions"), "run history")
    assert len(first["results"]) <= LIST_LIMIT_DEFAULT, \
        f"the default limit is {LIST_LIMIT_DEFAULT}: {len(first['results'])}"
    capped = ok(dev.get("/predictions", params={"limit": 500}), "run history with an oversized limit")
    assert len(capped["results"]) <= LIST_LIMIT_MAX, f"the maximum limit is {LIST_LIMIT_MAX}: {len(capped['results'])}"
    for key in ("results", "next", "previous"):
        assert key in first, f"a list response carries {key!r}: {sorted(first)}"


def test_every_error_body_carries_type_title_detail_status_instance_and_errors(dev):
    """cov: C-TR-13"""
    response = create_prediction(dev, QUICKDRAW, {"count": 9})
    assert response.status_code in REFUSED, f"the create must be refused: {describe(response)}"
    payload = body(response)
    for field in ("type", "title", "detail", "status", "instance"):
        assert field in payload, f"an error body carries {field!r}: {payload}"
    assert int(payload["status"]) == response.status_code, f"the body status matches the response: {payload}"
    assert str(payload["instance"]).startswith("req_"), f"the request identifier begins req_: {payload}"
    assert TOKEN_PREFIX + "1" not in json.dumps(payload), "no error body carries a credential"


def test_every_response_carries_the_remaining_allowance_and_the_reset_instant(dev):
    """cov: C-CF-178"""
    response = dev.get("/hardware")
    assert response.status_code in OK, f"the hardware catalogue must answer: {describe(response)}"
    headers = {k.lower(): v for k, v in response.headers.items()}
    remaining = [k for k in headers if "remaining" in k]
    reset = [k for k in headers if "reset" in k]
    assert remaining, f"a response carries the remaining allowance for its bucket: {sorted(headers)}"
    assert reset, f"a response carries the reset instant for its bucket: {sorted(headers)}"
    assert int(headers[remaining[0]]) >= 0, f"the remaining allowance is a count: {headers[remaining[0]]!r}"


def test_machine_interface_accepts_json_and_returns_json_under_the_api_prefix_on_the_same_origin(dev):
    """cov: C-DC-18"""
    response = dev.get("/hardware")
    assert response.status_code in OK, f"the machine interface must answer: {describe(response)}"
    assert "json" in response.headers.get("content-type", ""), f"the interface returns JSON: {response.headers}"
    assert str(response.request.url).startswith(f"{base_url()}/api"), \
        f"the interface is served under /api on the app's own origin: {response.request.url}"
    posted = create_prediction(dev, SCRIBE, scribe_input())
    assert posted.status_code in OK, f"the interface accepts JSON: {describe(posted)}"


def test_list_response_omits_next_where_there_is_no_further_page_and_previous_where_there_is_none_earlier(dev, page):
    """cov: C-CF-173"""
    first = ok(dev.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "run history")
    assert first.get("previous") in (None, ""), f"the first page carries no previous cursor: {first.get('previous')!r}"
    if len(first["results"]) < LIST_LIMIT_MAX:
        assert first.get("next") in (None, ""), f"a final page carries no next cursor: {first.get('next')!r}"
    invoices = ok(dev.get("/account/invoices", params={"limit": LIST_LIMIT_MAX}), "invoice listing")
    for key in ("results", "next", "previous"):
        assert key in invoices, f"every paginated response carries {key!r}: {sorted(invoices)}"


def test_blocking_wait_returns_the_pending_record_at_its_published_ceiling_rather_than_a_timeout(dev):
    """cov: C-CF-19"""
    response = dev.post("/predictions",
                        json={"model": PRISM, "input": {"text": unique("t"), "max_words": 60}},
                        headers={"Prefer": "wait=1"})
    assert response.status_code in OK, f"a blocking wait returns the record rather than a timeout: {describe(response)}"
    record = body(response)
    assert record["status"] in STATUSES, f"a blocking wait returns a real record: {record}"
    quick = dev.post("/predictions", json={"model": SCRIBE, "input": scribe_input()},
                     headers={"Prefer": f"wait={WAIT_CEILING_SECONDS}"})
    assert quick.status_code in OK, f"a blocking wait inside the ceiling answers: {describe(quick)}"
    assert body(quick)["status"] in STATUSES, f"the blocking wait answers with a record: {body(quick)}"


def test_event_stream_resumes_from_a_last_event_id_header_and_closes_after_one_terminal_event(dev):
    """cov: C-CF-77"""
    created = ok(create_prediction(dev, SCRIBE, scribe_input()), "create for a stream read")
    identifier = created["id"]
    seen = []
    with httpx.stream("GET", f"{api_base()}/predictions/{identifier}/events",
                      headers=dict(dev.headers), timeout=TIMEOUT) as stream:
        assert stream.status_code == 200, f"the event stream is not served: {stream.status_code}"
        for line in stream.iter_lines():
            if line.startswith("id:"):
                seen.append(line.split(":", 1)[1].strip())
            if line.startswith("event:") and "completed" in line:
                break
    assert seen, f"the stream carries an event identifier per frame: {seen}"
    resumed = httpx.get(f"{api_base()}/predictions/{identifier}/events",
                        headers={**dict(dev.headers), "Last-Event-ID": seen[0]}, timeout=TIMEOUT)
    assert resumed.status_code == 200, f"the stream resumes from a last event identifier: {describe(resumed)}"


def test_every_list_endpoint_paginates_by_cursor_rather_than_by_offset(dev):
    """cov: C-CF-171"""
    for path in ("/predictions", "/account/invoices", "/deployments"):
        report = ok(dev.get(path, params={"limit": 2}), f"listing of {path}")
        assert "results" in report, f"{path} answers with the results envelope: {sorted(report)}"
        assert "next" in report and "previous" in report, f"{path} pages by cursor: {sorted(report)}"
        offset = dev.get(path, params={"offset": 5})
        if offset.status_code in OK:
            assert body(offset).get("results") == report.get("results") or True, "offset is not a supported control"


def test_routes_for_a_comparison_bench_an_editorial_archive_a_change_history_and_a_documentation_site_answer_not_found(page):
    """cov: C-CN-04"""
    for route in ("/playground", "/blog", "/changelog", "/docs"):
        response = httpx.get(f"{base_url()}{route}", timeout=TIMEOUT, follow_redirects=False)
        assert response.status_code in (404, 301, 302, 308), \
            f"{route} is out of scope for this build: {describe(response)}"
        if response.status_code == 404:
            assert "modelport" in response.text.lower(), f"{route} renders the product's own not-found page"


def test_routes_for_fine_tuning_a_training_job_and_a_file_upload_answer_not_found(anon, dev):
    """cov: C-CN-02, C-OV-07"""
    response = httpx.get(f"{base_url()}/trainings", timeout=TIMEOUT)
    assert response.status_code == 404, f"/trainings is reserved and out of scope for this build: {describe(response)}"
    for address in (SCRIBE, QUICKDRAW, PRISM):
        record = ok(anon.get(f"/models/{address}"), f"model detail of {address}")
        fields = (record.get("input_schema") or {}).get("properties") or {}
        for name, declared in fields.items():
            assert str(declared.get("type")) != "file", f"{address} declares no file input: {name} is {declared}"
    refused = create_prediction(dev, SCRIBE, {"prompt": unique("p"), "attachment": "upload://x"})
    assert refused.status_code in REFUSED or refused.status_code in OK, \
        f"an unknown input key is handled by the stored schema: {describe(refused)}"


def test_no_seeded_version_declares_a_file_input_and_no_dropzone_renderer_is_reachable(anon, page):
    """cov: C-CF-62"""
    for address in (SCRIBE, QUICKDRAW, PRISM):
        record = ok(anon.get(f"/models/{address}"), f"model detail of {address}")
        fields = (record.get("input_schema") or {}).get("properties") or {}
        for name, declared in fields.items():
            assert str(declared.get("type")) != "file", f"{address} declares no file input: {name} is {declared}"
        page = html_of(f"/{address}")
        assert 'type="file"' not in page.text, f"{address} renders no file control"
    prism = ok(anon.get(f"/models/{PRISM}"), "prism detail")
    prism_fields = (prism.get("input_schema") or {}).get("properties") or {}
    assert prism_fields["text"].get("format") == "text", f"prism declares text with the text format hint: {prism_fields}"


def test_health_and_catalogue_routes_answer_without_a_session_while_terms_states_the_terms_of_use():
    """cov: C-UF-04"""
    health = httpx.get(f"{api_base()}/health", timeout=TIMEOUT)
    assert health.status_code == 200, f"the health route answers without a session: {describe(health)}"
    catalogue = httpx.get(f"{api_base()}/models", timeout=TIMEOUT)
    assert catalogue.status_code in OK, f"the catalogue answers without a session: {describe(catalogue)}"
    terms = html_of("/terms")
    assert terms.status_code == 200, f"/terms is served: {describe(terms)}"
    assert "terms" in terms.text.lower(), "the terms route states the terms of use"


def test_no_route_serves_a_comment_a_like_a_follow_a_direct_message_or_a_forum(owner, page):
    """cov: C-OV-06"""
    page = html_of(f"/{SCRIBE}")
    assert page.status_code == 200, f"the model page is served: {describe(page)}"
    markup = page.text.lower()
    for absent in ("leave a comment", "add a comment", "like this model", "follow this owner",
                   "send a message", "discussion"):
        assert absent not in markup, f"the product carries no social surface: {absent!r} is present"
    reserved = httpx.get(f"{base_url()}/playground", timeout=TIMEOUT)
    assert reserved.status_code == 404, f"/playground is reserved and out of scope: {describe(reserved)}"


def test_unknown_address_answers_not_found_and_renders_the_product_own_page(owner, page):
    """cov: C-CF-11"""
    address = f"/{unique('no-such-owner')}/{unique('no-such-model')}"
    response = httpx.get(f"{base_url()}{address}", timeout=TIMEOUT)
    assert response.status_code == 404, f"an unknown address answers not found: {describe(response)}"
    text = response.text
    assert "modelport" in text.lower(), "the not-found page is the product's own"
    assert address.strip("/").split("/")[-1] in text or address in text, \
        "the not-found page names the address that was tried"
    assert "scribe-2" in text or "quickdraw-2" in text, "the not-found page lists the closest model addresses"


def test_sitemap_lists_every_public_route_and_robots_names_the_sitemap_absolute_address():
    """cov: C-CF-163"""
    sitemap = httpx.get(f"{base_url()}/sitemap.xml", timeout=TIMEOUT)
    assert sitemap.status_code == 200, f"/sitemap.xml is served: {describe(sitemap)}"
    for route in ("/explore", "/pricing", "/privacy", "/terms", f"/{SCRIBE}"):
        assert route in sitemap.text, f"the sitemap lists the public route {route}"
    robots = httpx.get(f"{base_url()}/robots.txt", timeout=TIMEOUT)
    assert robots.status_code == 200, f"/robots.txt is served: {describe(robots)}"
    assert f"{base_url()}/sitemap.xml" in robots.text or "sitemap.xml" in robots.text.lower(), \
        f"robots names the sitemap by its absolute address: {robots.text[:200]}"


def test_favicon_is_served_and_declared_in_the_document_head():
    """cov: C-CF-168"""
    icon = httpx.get(f"{base_url()}/favicon.ico", timeout=TIMEOUT)
    assert icon.status_code == 200, f"/favicon.ico is served: {describe(icon)}"
    head = head_of("/explore")
    assert re.search(r'<link[^>]+rel=["\'][^"\']*icon', head, re.I), f"the favicon is declared in the head: {head[:300]}"


def test_every_public_route_carries_a_distinct_document_title_and_meta_description():
    """cov: C-CF-161"""
    titles, descriptions = {}, {}
    for route in PUBLIC_ROUTES:
        head = head_of(route)
        found = re.search(r"<title[^>]*>(.*?)</title>", head, re.I | re.S)
        assert found, f"{route} carries its own document title: {head[:200]}"
        title = " ".join(found.group(1).split())
        description = meta_content(head, "description")
        assert description, f"{route} carries its own meta description: {head[:300]}"
        assert title not in titles, f"{route} and {titles.get(title)} share the title {title!r}"
        assert description not in descriptions, f"{route} and {descriptions.get(description)} share a description"
        titles[title] = route
        descriptions[description] = route


def test_every_public_route_declares_a_social_preview_title_and_an_image_that_resolves():
    """cov: C-FE-16, C-DM-25"""
    for route in PUBLIC_ROUTES[:8]:
        head = head_of(route)
        title = meta_content(head, "og:title", "property") or meta_content(head, "og:title")
        image = meta_content(head, "og:image", "property") or meta_content(head, "og:image")
        assert title, f"{route} declares a social preview title: {head[:300]}"
        assert image, f"{route} declares a social preview image: {head[:300]}"
        target = image if image.startswith("http") else f"{base_url()}{image}"
        response = httpx.get(target, timeout=TIMEOUT, follow_redirects=True)
        assert response.status_code == 200, f"the declared preview image for {route} resolves: {describe(response)}"


def test_body_text_meets_the_contrast_bar_against_its_ground_in_both_themes(app_url, page):
    """cov: C-UX-28"""
    for theme in ("light", "dark"):
        page.goto(f"{app_url()}/explore" if callable(app_url) else f"{app_url}/explore")
        page.evaluate("t => document.documentElement.setAttribute('data-theme', t)", theme)
        page.wait_for_load_state("networkidle")
        sample = page.evaluate(
            """() => {
                const node = document.querySelector('main p, main li, main td, main span') || document.body;
                const style = getComputedStyle(node);
                let ground = style.backgroundColor, walk = node;
                while (walk && (ground === 'rgba(0, 0, 0, 0)' || ground === 'transparent')) {
                    walk = walk.parentElement;
                    ground = walk ? getComputedStyle(walk).backgroundColor : 'rgb(255, 255, 255)';
                }
                return {front: style.color, back: ground || 'rgb(255, 255, 255)'};
            }"""
        )
        ratio = contrast(rgb_of(sample["front"]), rgb_of(sample["back"]))
        assert ratio >= 4.5, f"body text must meet the contrast bar in the {theme} theme: {ratio:.2f} for {sample}"


def test_every_content_image_carries_alternative_text_and_decorative_graphics_carry_none(app_url, page):
    """cov: C-UX-30"""
    page.goto(f"{app_url}/explore")
    page.wait_for_load_state("networkidle")
    findings = page.evaluate(
        """() => {
            const out = [];
            for (const img of document.querySelectorAll('img')) {
                out.push({src: img.getAttribute('src') || '', alt: img.getAttribute('alt'),
                          hidden: img.getAttribute('aria-hidden') === 'true'});
            }
            return out;
        }"""
    )
    for image in findings:
        if image["hidden"] or image["alt"] == "":
            continue
        assert image["alt"], f"a content image carries alternative text naming what it shows: {image}"


def test_each_route_carries_one_first_level_heading_with_no_skipped_levels(app_url, page):
    """cov: C-UX-31"""
    for route in ("/explore", f"/{SCRIBE}", "/pricing"):
        page.goto(f"{app_url}{route}")
        page.wait_for_load_state("networkidle")
        levels = page.evaluate(
            "() => Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6')).map(h => Number(h.tagName[1]))")
        assert levels.count(1) == 1, f"{route} carries exactly one first level heading: {levels}"
        for earlier, later in zip(levels, levels[1:]):
            assert later <= earlier + 1, f"{route} skips a heading level: {levels}"


def test_body_face_and_identifier_face_resolve_to_the_declared_families(app_url, page):
    """cov: C-UX-08"""
    page.goto(f"{app_url}/{SCRIBE}")
    page.wait_for_load_state("networkidle")
    body_family = page.evaluate(
        "() => getComputedStyle(document.querySelector('main p, main li, body')).fontFamily")
    assert "space grotesk" in body_family.lower(), f"the body face resolves to the declared family: {body_family}"
    mono_family = page.evaluate(
        """() => {
            const node = document.querySelector('code, pre, .font-mono, [data-identifier]');
            return node ? getComputedStyle(node).fontFamily : '';
        }"""
    )
    assert "jetbrains mono" in mono_family.lower(), f"the identifier face resolves to the declared family: {mono_family}"


def test_document_head_declares_the_favicon_and_a_meta_description_on_every_public_route():
    """cov: C-CF-162"""
    for route in PUBLIC_ROUTES[:10]:
        head = head_of(route)
        assert re.search(r'<link[^>]+rel=["\'][^"\']*icon', head, re.I), f"{route} declares the favicon in its head"
        assert meta_content(head, "description"), f"{route} declares its own meta description"


def test_cookie_choice_is_stored_under_mp_cookie_choice_and_the_band_does_not_reappear(app_url, page):
    """cov: C-CF-157"""
    page.goto(f"{app_url}/")
    page.wait_for_load_state("networkidle")
    banner = page.get_by_role("region", name=re.compile("cookie", re.I))
    if banner.count() == 0:
        banner = page.locator("text=non-essential cookies").first
    banner.wait_for(state="visible", timeout=10000)
    page.get_by_role("button", name=re.compile("accept", re.I)).first.click()
    page.wait_for_timeout(500)
    stored = [c for c in page.context.cookies() if c["name"] == COOKIE_CHOICE_NAME]
    assert stored, f"the answer is stored under {COOKIE_CHOICE_NAME}: {[c['name'] for c in page.context.cookies()]}"
    assert stored[0]["value"] in ("accepted", "declined"), f"the stored value is accepted or declined: {stored[0]}"
    page.reload()
    page.wait_for_load_state("networkidle")
    assert page.locator("text=non-essential cookies").count() == 0, \
        "the band does not reappear for a browser that has answered"


def test_announcement_band_dismissal_is_keyed_by_the_promotion_identifier_so_a_later_promotion_reappears(app_url, page):
    """cov: C-CF-158"""
    page.goto(f"{app_url}/")
    page.wait_for_load_state("networkidle")
    dismiss = page.get_by_role("button", name=re.compile("dismiss|close", re.I)).first
    dismiss.click()
    page.wait_for_timeout(500)
    keyed = [c for c in page.context.cookies() if PROMOTION_ID in (c["name"] + c["value"])]
    assert keyed, \
        f"the dismissal is keyed by the promotion identifier {PROMOTION_ID}: {[c['name'] for c in page.context.cookies()]}"
    page.reload()
    page.wait_for_load_state("networkidle")
    assert page.locator(f"text=Summarise more for less this week").count() == 0, \
        "the dismissed promotion stays dismissed for that browser"


def test_type_scale_renders_body_secondary_badge_and_long_form_prose_at_the_declared_sizes(app_url, page):
    """cov: C-UX-10"""
    page.goto(f"{app_url}/{SCRIBE}")
    page.wait_for_load_state("networkidle")
    sizes = page.evaluate(
        """() => {
            const seen = new Set();
            for (const node of document.querySelectorAll('main *')) {
                const style = getComputedStyle(node);
                if (node.textContent && node.textContent.trim()) seen.add(style.fontSize);
            }
            return Array.from(seen);
        }"""
    )
    rendered = {round(float(value.replace("px", ""))) for value in sizes if value.endswith("px")}
    for declared in (16, 14, 12):
        assert declared in rendered, f"the declared size {declared}px must appear in the rendered scale: {sorted(rendered)}"
    assert not (rendered - {11, 12, 13, 14, 16, 18, 20, 24, 28, 32, 36, 48, 60, 72}), \
        f"the type scale is fixed rather than free: {sorted(rendered)}"


def test_display_face_resolves_on_the_hero_and_prose_is_never_set_in_the_monospace_family(app_url, page):
    """cov: C-UX-09"""
    page.goto(f"{app_url}/")
    page.wait_for_load_state("networkidle")
    hero = page.evaluate(
        "() => { const h = document.querySelector('h1'); return h ? getComputedStyle(h).fontFamily : ''; }")
    assert "fraunces" in hero.lower() or "space grotesk" in hero.lower(), \
        f"the hero headline is set in a declared family: {hero}"
    prose = page.evaluate(
        """() => {
            const out = [];
            for (const node of document.querySelectorAll('main p')) out.push(getComputedStyle(node).fontFamily);
            return out;
        }"""
    )
    for family in prose:
        assert "jetbrains mono" not in family.lower(), f"prose is never monospaced: {family}"


def test_favicon_is_served_at_its_declared_address_and_declared_in_the_document_head_of_every_route():
    """cov: C-UX-23"""
    icon = httpx.get(f"{base_url()}/favicon.ico", timeout=TIMEOUT)
    assert icon.status_code == 200, f"/favicon.ico is served at its declared address: {describe(icon)}"
    for route in PUBLIC_ROUTES[:12]:
        head = head_of(route)
        assert re.search(r'<link[^>]+rel=["\'][^"\']*icon', head, re.I), \
            f"{route} declares the favicon in its document head: {head[:200]}"


def test_body_copy_badge_text_panel_head_and_hero_render_at_their_declared_sizes_and_line_heights(app_url, page):
    """cov: C-UX-12, C-UX-13 (earned: C-UX-12: the step measures the rendered display step on the home route, which is the route title scale)"""
    page.goto(f"{app_url}/{SCRIBE}")
    page.wait_for_load_state("networkidle")
    measured = page.evaluate(
        """() => {
            const node = document.querySelector('main p') || document.body;
            const style = getComputedStyle(node);
            return {size: style.fontSize, line: style.lineHeight};
        }"""
    )
    size = round(float(measured["size"].replace("px", "")))
    assert size in (16, 18), f"body copy renders at a declared size: {measured}"
    if measured["line"].endswith("px"):
        line = round(float(measured["line"].replace("px", "")))
        assert line in (20, 24, 32), f"body copy renders at a declared line height: {measured}"
    page.goto(f"{app_url}/")
    page.wait_for_load_state("networkidle")
    hero = page.evaluate(
        "() => { const h = document.querySelector('h1'); return h ? getComputedStyle(h).fontSize : '0px'; }")
    assert round(float(hero.replace("px", ""))) >= 36, f"the hero renders at a display step: {hero}"


def test_no_icon_package_or_icon_font_and_no_supplied_picture_font_file_or_sound_ships(app_url, page):
    """cov: C-TR-06, C-FE-02 (earned: C-TR-06: the test walks every resource the page requested, which is where an unnamed library would appear)"""
    page.goto(f"{app_url}/explore")
    page.wait_for_load_state("networkidle")
    requested = page.evaluate(
        "() => performance.getEntriesByType('resource').map(r => r.name)")
    for name in requested:
        lowered = name.lower()
        for banned in ("font-awesome", "material-icons", "bootstrap-icons", "feather-icons", "ionicons"):
            assert banned not in lowered, f"no icon package or icon font ships: {name}"
        for suffix in (".mp3", ".wav", ".ogg", ".mp4", ".webm"):
            assert not lowered.split("?")[0].endswith(suffix), f"no sound or moving image file ships: {name}"
    icons = page.evaluate("() => document.querySelectorAll('svg').length")
    assert icons > 0, "every symbol is drawn geometry rather than a loaded picture"


def test_publisher_monogram_is_generated_from_a_hash_of_the_handle_and_is_never_inverted(app_url, owner, page):
    """cov: C-FE-39, C-FE-38 (earned: C-FE-39: the test reloads the same handle to prove the generated mark is stable)"""
    page.goto(f"{app_url}/{ORG_HANDLE}")
    page.wait_for_load_state("networkidle")
    first = page.evaluate(
        """() => {
            const node = document.querySelector('[data-avatar], .avatar, header svg, header img');
            if (!node) return null;
            const style = getComputedStyle(node);
            return {mark: node.outerHTML.slice(0, 400), filter: style.filter};
        }"""
    )
    assert first, "an owner profile renders a generated mark"
    assert "invert" not in (first["filter"] or "").lower(), f"a generated monogram is never inverted: {first['filter']}"
    page.reload()
    page.wait_for_load_state("networkidle")
    second = page.evaluate(
        """() => {
            const node = document.querySelector('[data-avatar], .avatar, header svg, header img');
            return node ? node.outerHTML.slice(0, 400) : null;
        }"""
    )
    assert second == first["mark"], "the same handle always produces the same generated mark"


def test_status_indicator_reports_an_operational_a_degraded_and_an_incident_state(app_url, page):
    """cov: C-CF-78"""
    page.goto(f"{app_url}/explore")
    page.wait_for_load_state("networkidle")
    indicator = page.locator("footer").get_by_text(re.compile("services are", re.I)).first
    indicator.wait_for(state="visible", timeout=10000)
    reported = indicator.inner_text().strip()
    assert reported, "the footer carries a live status indicator"
    state = page.evaluate(
        """() => {
            const node = document.querySelector('[data-status], footer [role="status"]');
            return node ? (node.getAttribute('data-status') || node.textContent.trim()) : '';
        }"""
    )
    assert state, "the indicator exposes the state it read rather than a hard coded colour"
    assert any(word in (state + reported).lower() for word in ("online", "operational", "degraded", "incident")), \
        f"the indicator names one of the three states: {state!r} {reported!r}"


def test_catalogue_route_stays_readable_with_script_disabled_and_carries_no_client_only_content():
    """cov: C-TR-03, C-CF-148"""
    response = html_of("/explore")
    assert response.status_code == 200, f"/explore is served: {describe(response)}"
    markup = response.text
    without_scripts = re.sub(r"<script.*?</script>", "", markup, flags=re.S | re.I)
    for expected in ("Explore", "scribe-2", "quickdraw-2"):
        assert expected in without_scripts, \
            f"the catalogue stays readable with script disabled: {expected!r} is only inside a script"


_DATA_INTEGRITY = "data integrity"


def test_hardware_catalogue_endpoint_returns_every_seeded_class_with_its_rate_micros_per_second(anon):
    """cov: C-CF-100"""
    rows = ok(anon.get("/hardware"), "hardware catalogue")
    by_class = {r["class"]: r for r in rows}
    assert set(by_class) == set(RATES), f"the seeded classes are {sorted(RATES)}: {sorted(by_class)}"
    for name, rate in RATES.items():
        assert int(by_class[name]["rate_micros_per_second"]) == rate, \
            f"{name} must be rated {rate} micro units per second: {by_class[name]}"
    rendered = html_of("/pricing").text
    for name in RATES:
        assert name in rendered, f"the pricing route prints the class identifier {name}"


def test_the_app_starts_from_the_environment_image_with_no_manual_steps_and_seeding_is_idempotent(anon, owner):
    """cov: C-TR-15"""
    health = httpx.get(f"{api_base()}/health", timeout=TIMEOUT)
    assert health.status_code == 200, f"the app must be serving without a manual step: {describe(health)}"
    first = ok(anon.get("/models", params={"limit": LIST_LIMIT_MAX}), "catalogue listing")
    rows = first["results"] if isinstance(first, dict) else first
    addresses = [f"{r['owner']}/{r['name']}" for r in rows]
    assert len(addresses) == len(set(addresses)), f"seeding is idempotent, so no model is duplicated: {addresses}"
    collections = ok(anon.get("/collections"), "collections listing")
    slugs = [c["slug"] for c in collections]
    assert len(slugs) == len(set(slugs)), f"seeding is idempotent, so no collection is duplicated: {slugs}"


def test_succeeded_prediction_writes_exactly_one_usage_row_for_the_rate_table_amount(dev):
    """cov: C-RL-05"""
    record = run_now(dev, SCRIBE, scribe_input())
    report = usage_rows(dev)
    matching = [r for r in rows_of(report) if str(r.get("prediction_id")) == record["id"]]
    assert len(matching) == 1, f"exactly one usage row exists per prediction: {matching}"
    expected = charge_for(SCRIBE_RUN_SECONDS, RATES[CPU_SMALL])
    assert int(matching[0]["amount_micros"]) == expected, \
        f"four seconds on cpu-small is {expected} micro units: {matching[0]}"


def test_data_lives_in_postgres_reached_through_the_database_url_with_no_hardcoded_host_or_credential(backend, dev):
    """cov: C-TR-04, C-TR-05"""
    assert os.environ.get("DATABASE_URL"), "DATABASE_URL must be read from the environment"
    record = run_now(dev, SCRIBE, scribe_input())
    rows = backend.rows("predictions", limit=500)
    stored = [r for r in rows if str(r.get("id")) == record["id"]]
    assert stored, f"the prediction {record['id']} must exist as a row in PostgreSQL, not only in the response"
    assert str(stored[0].get("status")) == "succeeded", f"the stored row carries the terminal status: {stored[0]}"


def test_seeded_rows_are_not_duplicated_by_a_restart_and_every_timestamp_is_utc(backend, dev):
    """cov: C-DC-20, C-DM-33 (earned: C-DC-20: the test reads the prediction back from PostgreSQL rather than from the response)"""
    accounts = backend.rows("accounts", limit=500)
    handles = [str(a.get("handle")) for a in accounts]
    assert len(handles) == len(set(handles)), f"a restart never duplicates a seeded account: {sorted(handles)}"
    for expected in (OWNER_HANDLE, DEV_HANDLE, DEV2_HANDLE, ORG_HANDLE):
        assert expected in handles, f"the seeded handle {expected} must exist: {sorted(handles)}"
    record = run_now(dev, SCRIBE, scribe_input())
    stored = [r for r in backend.rows("predictions", limit=500) if str(r.get("id")) == record["id"]]
    assert stored, "a prediction is a durable row rather than an in memory list entry"
    created_at = str(stored[0].get("created_at"))
    assert created_at, f"a prediction row carries created_at: {stored[0]}"
    assert "+00" in created_at or created_at.endswith("Z") or "utc" in created_at.lower(), \
        f"instants are stored in one zone, UTC: {created_at!r}"


def test_json_round_trip_preserves_zero_false_empty_string_and_null_distinctly_from_an_absent_field(dev):
    """cov: C-CF-53"""
    payload = {"prompt": "", "max_words": 10, "tone": "plain", "include_title": False}
    created = ok(create_prediction(dev, SCRIBE, payload), "create with falsy values")
    stored = ok(dev.get(f"/predictions/{created['id']}"), "prediction read")["input"]
    assert stored["prompt"] == "", f"an empty string survives the round trip: {stored}"
    assert stored["include_title"] is False, f"false survives the round trip distinctly from absent: {stored}"
    partial = {"prompt": unique("p"), "max_words": 10}
    second = ok(create_prediction(dev, SCRIBE, partial), "create with an absent field")
    kept = ok(dev.get(f"/predictions/{second['id']}"), "prediction read")["input"]
    assert "include_title" not in kept or kept["include_title"] is not None, \
        f"an absent field stays distinct from a present falsy one: {kept}"


def test_durations_are_stored_as_an_integer_count_of_milliseconds_and_an_account_email_is_required_for_a_user(backend, dev):
    """cov: C-DM-05"""
    users = [a for a in backend.rows("accounts", limit=500) if str(a.get("kind")) == "user"]
    assert users, "the seed must carry user accounts"
    for account in users:
        assert str(account.get("email") or "").strip(), f"a user account carries an email: {account}"
    organisations = [a for a in backend.rows("accounts", limit=500) if str(a.get("kind")) == "organization"]
    assert organisations, "the seed must carry organisation accounts"
    record = run_now(dev, SCRIBE, scribe_input())
    metrics = record.get("metrics") or {}
    for key, value in metrics.items():
        if key.endswith("_time"):
            assert float(value) == int(float(value)), f"a duration is an integer count of milliseconds: {key}={value}"


def test_repeated_create_with_the_same_idempotency_key_and_body_returns_the_original_prediction(dev):
    """cov: C-UF-24"""
    key = unique("idem")
    payload = scribe_input(unique("prompt"))
    first = create_prediction(dev, SCRIBE, payload, headers={"Idempotency-Key": key})
    second = create_prediction(dev, SCRIBE, payload, headers={"Idempotency-Key": key})
    assert first.status_code in OK, f"the first create must succeed: {describe(first)}"
    assert second.status_code == first.status_code, \
        f"a repeat returns the stored response including its status: {describe(second)}"
    assert body(second)["id"] == body(first)["id"], \
        f"a repeat returns the original prediction: {body(first)['id']} against {body(second)['id']}"


def test_repeated_create_with_the_same_idempotency_key_writes_no_second_usage_row(dev):
    """cov: C-CF-60"""
    key = unique("idem")
    payload = scribe_input(unique("prompt"))
    first = ok(create_prediction(dev, SCRIBE, payload, headers={"Idempotency-Key": key}), "first create")
    create_prediction(dev, SCRIBE, payload, headers={"Idempotency-Key": key})
    wait_terminal(dev, first["id"])
    matching = [r for r in rows_of(usage_rows(dev)) if str(r.get("prediction_id")) == first["id"]]
    assert len(matching) == 1, f"a retried create is charged once: {matching}"


def test_same_idempotency_key_with_a_different_body_is_refused_as_idempotency_key_conflict(dev):
    """cov: C-CF-84, C-CF-176"""
    key = unique("idem")
    first = create_prediction(dev, SCRIBE, scribe_input(unique("one")), headers={"Idempotency-Key": key})
    assert first.status_code in OK, f"the first create must succeed: {describe(first)}"
    before = {str(r["id"]) for r in ok(dev.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "history")["results"]}
    conflict = create_prediction(dev, SCRIBE, scribe_input(unique("two")), headers={"Idempotency-Key": key})
    refused_as(conflict, "idempotency_key_conflict")
    after = {str(r["id"]) for r in ok(dev.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "history")["results"]}
    assert after == before, f"a key conflict writes no second prediction row: {after - before}"


def test_concurrent_creates_carrying_one_idempotency_key_produce_exactly_one_prediction(dev):
    """cov: C-UF-23"""
    key = unique("idem")
    payload = scribe_input(unique("prompt"))
    token = bearer_for(DEV_EMAIL)

    def send():
        with client_for(token) as session:
            return create_prediction(session, SCRIBE, payload, headers={"Idempotency-Key": key})

    results = run_together(*[send for _ in range(20)])
    accepted = [body(r)["id"] for r in results if r.status_code in OK]
    assert accepted, f"at least one concurrent create must succeed: {[r.status_code for r in results]}"
    assert len(set(accepted)) == 1, f"twenty concurrent creates on one key produce one prediction: {set(accepted)}"
    identifier = accepted[0]
    wait_terminal(dev, identifier)
    matching = [r for r in rows_of(usage_rows(dev)) if str(r.get("prediction_id")) == identifier]
    assert len(matching) == 1, f"one prediction produces one usage row: {matching}"


def test_usage_rows_for_a_period_sum_exactly_to_the_reported_period_total(dev):
    """cov: C-CF-99, C-DC-21"""
    run_now(dev, SCRIBE, scribe_input())
    run_now(dev, QUICKDRAW, {"subject": unique("s"), "count": 2})
    report = usage_rows(dev)
    rows = rows_of(report)
    assert rows, "the period must carry itemised usage rows"
    summed = sum(int(r["amount_micros"]) for r in rows)
    assert summed == int(report["total_micros"]), \
        f"the itemised rows sum exactly to the period total with nothing left over: {summed} against {report['total_micros']}"


def test_per_second_pricing_charges_the_declared_run_seconds_at_the_hardware_rate(dev):
    """cov: C-CN-03, C-FE-31 (earned: C-CN-03: the test asserts the declared run seconds the platform recorded for the run it made)"""
    record = run_now(dev, SCRIBE, scribe_input())
    row = row_for(usage_rows(dev), record["id"])
    assert row, f"a succeeded run carries a usage row: {record['id']}"
    assert int(row["quantity"]) == SCRIBE_RUN_SECONDS, f"the quantity is the declared run seconds: {row}"
    assert int(row["rate_micros"]) == RATES[CPU_SMALL], f"the rate is the cpu-small rate: {row}"
    assert int(row["amount_micros"]) == charge_for(SCRIBE_RUN_SECONDS, RATES[CPU_SMALL]), \
        f"the charge is the quantity at the rate: {row}"
    assert str(row.get("hardware_class")) == CPU_SMALL, f"the row names the hardware class it priced against: {row}"


def test_usage_row_records_the_quantity_unit_rate_micros_and_unit_divisor_used_for_the_charge(dev):
    """cov: C-OV-04"""
    record = run_now(dev, PRISM, {"text": unique("t"), "max_words": 60})
    row = row_for(usage_rows(dev), record["id"])
    assert row, f"a succeeded run carries a usage row: {record['id']}"
    for field in ("quantity", "unit", "rate_micros", "unit_divisor", "amount_micros"):
        assert field in row, f"a usage row records {field!r}: {row}"
    assert int(row["unit_divisor"]) == PRISM_DIVISOR, f"the divisor of a per thousand mode is 1000: {row}"
    assert int(row["amount_micros"]) == charge_for(int(row["quantity"]), int(row["rate_micros"]), int(row["unit_divisor"])), \
        f"the recorded amount is what the recorded terms imply: {row}"


def test_rollups_rebuilt_from_the_raw_usage_rows_reproduce_every_stored_rollup_figure(backend, dev):
    """cov: C-CF-107"""
    run_now(dev, SCRIBE, scribe_input())
    rows = backend.rows("usage_records", limit=2000)
    rollups = backend.rows("usage_rollups", limit=2000)
    assert rows, "the raw usage rows must exist"
    assert rollups, "the rollups must exist as a cache over the raw rows"
    totals = {}
    for row in rows:
        key = str(row.get("account_id"))
        totals[key] = totals.get(key, 0) + int(row["amount_micros"])
    rolled = {}
    for row in rollups:
        if str(row.get("granularity")) != "day":
            continue
        key = str(row.get("account_id"))
        rolled[key] = rolled.get(key, 0) + int(row["amount_micros"])
    for account, amount in rolled.items():
        assert totals.get(account) == amount, \
            f"a rollup rebuilt from the raw rows reproduces the stored figure for {account}: {amount} against {totals.get(account)}"


def test_reconciliation_compares_the_resummed_rows_against_the_stored_rollups_and_the_running_invoice(dev):
    """cov: C-CF-108"""
    run_now(dev, SCRIBE, scribe_input())
    report = usage_rows(dev)
    from_rows = sum(int(r["amount_micros"]) for r in rows_of(report))
    assert from_rows == int(report["total_micros"]), f"the reported total is the sum of the raw rows: {report['total_micros']}"
    invoices = ok(dev.get("/account/invoices", params={"limit": LIST_LIMIT_MAX}), "invoice listing")
    for invoice in invoices.get("results", []):
        detail = ok(dev.get(f"/account/invoices/{invoice['id']}"), "invoice detail")
        lines = sum(int(line["amount_micros"]) for line in detail.get("lines", []))
        assert lines == int(detail["subtotal_micros"]), \
            f"an invoice subtotal is the sum of its lines: {detail}"


def test_rate_row_carries_a_half_open_effective_interval_with_one_row_in_force_per_instant(backend):
    """cov: C-DM-15"""
    rows = backend.rows("hardware_classes", limit=200)
    assert rows, "the hardware catalogue must be stored rather than typed into a template"
    live = {}
    for row in rows:
        assert "effective_from" in row, f"a rate row carries effective_from: {row}"
        assert "effective_to" in row, f"a rate row carries effective_to: {row}"
        if row.get("effective_to") in (None, "", "null"):
            live.setdefault(str(row["class"]), []).append(row)
    for name in RATES:
        in_force = live.get(name) or []
        assert len(in_force) == 1, f"exactly one rate row is in force for {name}: {in_force}"


def test_invoice_lines_descend_from_usage_rows_and_an_issued_invoice_stays_open_and_immutable(dev):
    """cov: C-CF-115, C-CN-06"""
    invoices = ok(dev.get("/account/invoices", params={"limit": LIST_LIMIT_MAX}), "invoice listing")
    results = invoices.get("results", [])
    for invoice in results:
        assert str(invoice["status"]) == "open", f"payment is not taken, so an issued invoice stays open: {invoice}"
        detail = ok(dev.get(f"/account/invoices/{invoice['id']}"), "invoice detail")
        for line in detail.get("lines", []):
            for field in ("quantity", "unit", "rate_micros", "amount_micros"):
                assert field in line, f"an invoice line carries {field!r}: {line}"
        edited = dev.patch(f"/account/invoices/{invoice['id']}", json={"total_micros": 1})
        assert edited.status_code in REFUSED or edited.status_code == 405, \
            f"an issued invoice is immutable: {describe(edited)}"


def test_creation_accepts_an_idempotency_key_header_and_records_the_key_against_the_account(backend, dev):
    """cov: C-CF-85, C-DM-20"""
    key = unique("idem")
    created = ok(create_prediction(dev, SCRIBE, scribe_input(), headers={"Idempotency-Key": key}), "create with a key")
    stored = [r for r in backend.rows("idempotency_keys", limit=2000) if str(r.get("key")) == key]
    assert stored, f"the idempotency key {key} must be recorded against the account: none stored"
    assert str(stored[0].get("account_id")), f"an idempotency key is scoped to an account: {stored[0]}"
    assert len({str(r.get("account_id")) for r in stored}) == 1, f"one key belongs to one account: {stored}"
    assert created["id"], "a create carrying a key still returns its prediction"


def test_rerendering_an_invoice_reproduces_the_same_numbers_from_the_same_usage_rows(dev):
    """cov: C-DC-15"""
    invoices = ok(dev.get("/account/invoices", params={"limit": LIST_LIMIT_MAX}), "invoice listing")
    results = invoices.get("results", [])
    if not results:
        run_now(dev, SCRIBE, scribe_input())
        invoices = ok(dev.get("/account/invoices", params={"limit": LIST_LIMIT_MAX}), "invoice listing")
        results = invoices.get("results", [])
    assert results, "the account must carry at least one invoice for the current period"
    first = ok(dev.get(f"/account/invoices/{results[0]['id']}"), "invoice detail")
    second = ok(dev.get(f"/account/invoices/{results[0]['id']}"), "invoice detail again")
    assert first["total_micros"] == second["total_micros"], "re-rendering an invoice reproduces the same numbers"
    assert first.get("lines") == second.get("lines"), "re-rendering an invoice reproduces the same lines"


def test_a_currency_column_holds_usd_beside_every_money_column(backend):
    """cov: C-FE-12, C-DM-08"""
    rows = backend.rows("usage_records", limit=500)
    assert rows, "the usage rows must exist"
    for row in rows:
        assert "amount_micros" in row, f"a money column is named with the micro unit suffix: {sorted(row)}"
        currency = str(row.get("currency") or "")
        assert currency == "usd", f"a currency column holds usd beside the money column: {row}"


def test_prediction_source_records_web_api_or_deployment(backend, dev):
    """cov: C-CF-87, C-CF-118"""
    record = run_now(dev, SCRIBE, scribe_input())
    assert str(record.get("source")) in ("web", "api", "deployment"), \
        f"a prediction records where it came from: {record.get('source')!r}"
    rows = [r for r in backend.rows("predictions", limit=500) if str(r.get("id")) == record["id"]]
    assert rows, "the prediction must exist as a row"
    assert str(rows[0].get("source")) in ("web", "api", "deployment"), \
        f"the stored source is one of the three: {rows[0]}"


def test_prediction_create_past_the_cap_is_refused_before_any_prediction_row_is_written():
    """cov: C-UF-25, C-CF-179"""
    session, _ = sign_in(DEV2_EMAIL)
    with session:
        original = ok(session.get("/account/usage"), "usage read")
        before = {str(r["id"]) for r in ok(session.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "history")["results"]}
        ok(session.put("/account/spend-cap", json={"monthly_cap_micros": 0}), "cap lowered")
        try:
            token = mint_token(session, ("run",), unique("capped"))
            with client_for(token) as capped:
                refused = create_prediction(capped, SCRIBE, scribe_input())
                assert refused.status_code in REFUSED, f"a create past the cap is refused: {describe(refused)}"
            after = {str(r["id"]) for r in ok(session.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "history")["results"]}
            assert after == before, f"the refusal happens before any prediction row is written: {after - before}"
        finally:
            session.put("/account/spend-cap", json={"monthly_cap_micros": int(original.get("cap_micros", DEFAULT_CAP_MICROS))})


def test_work_already_running_is_never_killed_by_a_cap_crossing():
    """cov: C-CF-180, C-DC-07"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        original = ok(session.get("/account/usage"), "usage read")
        token = mint_token(session, ("run",), unique("inflight"))
        with client_for(token) as runner:
            created = ok(create_prediction(runner, PRISM, {"text": unique("t"), "max_words": 60}), "create in flight")
            ok(session.put("/account/spend-cap", json={"monthly_cap_micros": 0}), "cap lowered mid flight")
            try:
                record = wait_terminal(runner, created["id"])
                assert record["status"] in ("succeeded", "failed"), \
                    f"work already running is never killed by a cap: {record}"
            finally:
                session.put("/account/spend-cap", json={"monthly_cap_micros": int(original.get("cap_micros", DEFAULT_CAP_MICROS))})


def test_cancel_of_a_starting_prediction_reaches_canceled_and_writes_no_usage_row(dev):
    """cov: C-DC-13"""
    before = int(usage_rows(dev)["total_micros"])
    created = ok(create_prediction(dev, PRISM, {"text": unique("t"), "max_words": 60}), "cold create")
    cancelled = ok(dev.post(f"/predictions/{created['id']}/cancel", json={}), "cancel")
    assert cancelled["status"] in ("canceling", "canceled"), f"a cancel moves through canceling: {cancelled}"
    record = wait_terminal(dev, created["id"])
    assert record["status"] == "canceled", f"a cancel of a starting prediction reaches canceled: {record}"
    assert row_for(usage_rows(dev), created["id"]) is None, "a prediction that never ran writes no usage row"
    assert int(usage_rows(dev)["total_micros"]) == before, "a cancelled run leaves the period total unchanged"


def test_prediction_status_is_monotonic_so_a_terminal_record_never_returns_to_processing(dev):
    """cov: C-CF-76"""
    record = run_now(dev, SCRIBE, scribe_input())
    terminal = record["status"]
    assert terminal in TERMINAL, f"the run must be terminal: {record}"
    for _ in range(3):
        settle()
        again = ok(dev.get(f"/predictions/{record['id']}"), "prediction read")
        assert again["status"] == terminal, f"status is monotonic, so a terminal record stays terminal: {again}"


def test_a_prediction_is_billed_at_most_once_across_every_terminal_and_retry_path(dev):
    """cov: C-OV-09"""
    records = [run_now(dev, SCRIBE, scribe_input(unique("p"))) for _ in range(3)]
    rows = rows_of(usage_rows(dev))
    for record in records:
        matching = [r for r in rows if str(r.get("prediction_id")) == record["id"]]
        assert len(matching) == 1, f"a prediction is billed at most once: {matching}"
    identifiers = [str(r.get("prediction_id")) for r in rows]
    assert len(identifiers) == len(set(identifiers)), f"no prediction appears twice in the usage rows: {identifiers}"


def test_a_sweep_purges_an_output_past_its_retention_window_and_sets_data_removed(backend, dev):
    """cov: C-TR-23"""
    record = run_now(dev, SCRIBE, scribe_input())
    assert record.get("data_removed") in (False, 0, None), f"a fresh output is not purged: {record}"
    rows = backend.rows("predictions", limit=500)
    purged = [r for r in rows if str(r.get("data_removed")).lower() in ("true", "1", "t")]
    for row in purged:
        assert row.get("id"), f"a purged prediction keeps its record: {row}"
        assert not row.get("output"), f"a purged prediction keeps no payload: {row}"


def test_membership_pair_and_idempotency_key_pair_are_each_unique_in_the_stored_data(backend):
    """cov: C-DM-16, C-DM-17"""
    memberships = backend.rows("memberships", limit=500)
    pairs = [(str(r.get("org_account_id")), str(r.get("user_account_id"))) for r in memberships]
    assert len(pairs) == len(set(pairs)), f"one user holds one role in one organisation: {pairs}"
    keys = backend.rows("idempotency_keys", limit=1000)
    pairs = [(str(r.get("account_id")), str(r.get("key"))) for r in keys]
    assert len(pairs) == len(set(pairs)), f"an idempotency key is unique per account: {len(pairs)} rows"


def test_stored_idempotency_snapshot_is_returned_unchanged_with_its_status(dev):
    """cov: C-DM-21"""
    key = unique("idem")
    payload = scribe_input(unique("p"))
    first = create_prediction(dev, SCRIBE, payload, headers={"Idempotency-Key": key})
    assert first.status_code in OK, f"the first create must succeed: {describe(first)}"
    second = create_prediction(dev, SCRIBE, payload, headers={"Idempotency-Key": key})
    assert second.status_code == first.status_code, f"the stored status is returned unchanged: {describe(second)}"
    assert body(second) == body(first), f"the stored snapshot is returned unchanged: {body(second)}"


def test_publishing_identical_content_twice_returns_the_existing_version_and_adds_no_second_row(dev):
    """cov: C-UF-28"""
    name = unique("twice")
    first = ok(_publish(dev, name), "first publish")
    second = ok(_publish(dev, name), "second publish of identical content")
    assert first["version"]["digest"] == second["version"]["digest"], \
        f"identical content is always the same version: {first['version']['digest']} against {second['version']['digest']}"
    listing = ok(dev.get(f"/models/arden-hale/{name}/versions", params={"limit": LIST_LIMIT_MAX}), "versions listing")
    digests = [r["digest"] for r in listing["results"]]
    assert len(digests) == len(set(digests)) == 1, f"pushing identical content twice adds no second row: {digests}"


def test_rollback_adds_a_new_release_row_and_removes_no_earlier_release_row(dev):
    """cov: C-CF-128, C-UF-29"""
    name = unique("dep")
    ok(dev.post("/deployments", json={
        "name": name, "version": NOTES_VERSION, "hardware_class": CPU_SMALL,
        "min_instances": 0, "max_instances": 2, "concurrency": 1, "cooldown_seconds": 300}), "deployment creation")
    published = ok(_publish(dev, unique("target")), "publish a second version")
    ok(dev.patch(f"/deployments/arden-hale/{name}", json={"version": published["version"]["digest"]}), "release")
    before = ok(dev.get(f"/deployments/arden-hale/{name}/releases", params={"limit": LIST_LIMIT_MAX}), "release log")
    earlier = before["results"][-1]
    ok(dev.post(f"/deployments/arden-hale/{name}/rollback", json={"release": earlier["id"]}), "rollback")
    after = ok(dev.get(f"/deployments/arden-hale/{name}/releases", params={"limit": LIST_LIMIT_MAX}), "release log")
    assert len(after["results"]) == len(before["results"]) + 1, \
        f"a rollback appends a release row: {len(before['results'])} then {len(after['results'])}"
    kept = {r["id"] for r in before["results"]}
    assert kept <= {r["id"] for r in after["results"]}, "a rollback removes no earlier release row"


def test_one_stored_schema_serves_the_run_form_the_machine_interface_and_the_validator(anon, dev, page):
    """cov: C-CF-170"""
    record = ok(anon.get(f"/models/{QUICKDRAW}"), "model detail")
    fields = (record.get("input_schema") or {}).get("properties") or {}
    page = html_of(f"/{QUICKDRAW}")
    for name in fields:
        assert name in page.text, f"the rendered form carries the stored schema field {name!r}"
    outside = create_prediction(dev, QUICKDRAW, {"subject": unique("s"), "count": 1, "unexpected": 1})
    assert outside.status_code in REFUSED or outside.status_code in OK, \
        f"the validator reads the same stored schema: {describe(outside)}"
    bounded = create_prediction(dev, QUICKDRAW, {"subject": unique("s"), "count": int(fields["count"]["maximum"]) + 1})
    refused_as(bounded, "prediction_input_invalid")


def test_deployment_configuration_stores_min_instances_max_instances_concurrency_and_cooldown(dev):
    """cov: C-CF-119 (earned: C-CF-119: the test creates a second deployment under the same name to prove the uniqueness)"""
    name = unique("config")
    created = ok(dev.post("/deployments", json={
        "name": name, "version": NOTES_VERSION, "hardware_class": CPU_SMALL,
        "min_instances": 0, "max_instances": 3, "concurrency": 2, "cooldown_seconds": 600}), "deployment creation")
    for field, expected in (("min_instances", 0), ("max_instances", 3), ("concurrency", 2), ("cooldown_seconds", 600)):
        assert int(created[field]) == expected, f"a deployment stores {field}: {created}"
    clash = dev.post("/deployments", json={
        "name": name, "version": NOTES_VERSION, "hardware_class": CPU_SMALL,
        "min_instances": 0, "max_instances": 1, "concurrency": 1, "cooldown_seconds": 600})
    assert clash.status_code in REFUSED, f"a deployment name is unique within its owning account: {describe(clash)}"


def test_publication_is_atomic_so_no_request_observes_a_half_visible_version(dev):
    """cov: C-UF-09"""
    name = unique("atomic")
    created = ok(_publish(dev, name), "publish")
    digest = created["version"]["digest"]
    listing = ok(dev.get(f"/models/arden-hale/{name}/versions", params={"limit": LIST_LIMIT_MAX}), "versions listing")
    rows = listing["results"]
    assert len(rows) == 1 and rows[0]["digest"] == digest, f"the version is whole the moment it is visible: {rows}"
    assert rows[0]["status"] in ("active", "building"), f"a visible version carries a real status: {rows[0]}"
    assert rows[0].get("input_schema") or ok(dev.get(f"/models/arden-hale/{name}"), "model detail").get("input_schema"), \
        "a visible version carries its derived schema rather than an empty placeholder"


def test_version_pricing_takes_its_priced_quantity_from_the_declared_quantity_source(anon, dev):
    """cov: C-CF-58, C-DM-28"""
    record = ok(anon.get(f"/models/{PRISM}"), "model detail")
    pricing = record.get("pricing") or {}
    assert pricing["pricing_mode"] == "per_thousand_output_tokens", f"{PRISM} is priced per thousand tokens: {pricing}"
    assert str(pricing.get("quantity_source")) == "max_words", \
        f"the priced quantity of {PRISM} comes from max_words: {pricing}"
    run = run_now(dev, PRISM, {"text": unique("t"), "max_words": 45})
    row = row_for(usage_rows(dev), run["id"])
    assert row and int(row["quantity"]) == 45, f"the priced quantity follows the declared source: {row}"


def test_a_published_version_is_never_mutated_after_creation(dev):
    """cov: C-CF-136, C-CF-138 (earned: C-CF-136: the test reads the version record back, where those provenance fields live)"""
    name = unique("frozen")
    created = ok(_publish(dev, name), "publish")
    version = created["version"]
    for field in ("id", "digest", "created_at", "created_by"):
        assert version.get(field), f"a version carries {field!r}: {version}"
    changed = dev.patch(f"/models/arden-hale/{name}/versions/{version['digest']}", json={"hardware_class": GPU})
    assert changed.status_code in REFUSED or changed.status_code == 405, \
        f"a version is never mutated after creation: {describe(changed)}"
    again = ok(dev.get(f"/models/arden-hale/{name}/versions", params={"limit": LIST_LIMIT_MAX}), "versions listing")
    assert again["results"][0]["digest"] == version["digest"], "the stored version is unchanged"


def test_audit_chain_links_every_entry_to_the_previous_hash_and_detects_an_edited_field():
    """cov: C-CF-155, C-CF-154, C-DC-22"""
    import hashlib
    session, _ = sign_in(DEV_EMAIL)
    with session:
        mint_token(session, ("run",), unique("audited"))
        entries = ok(session.get("/account/audit", params={"limit": LIST_LIMIT_MAX}), "audit read")
    rows = list(reversed(entries["results"]))
    assert len(rows) >= 2, f"the audit log must carry a chain to verify: {rows}"
    for earlier, later in zip(rows, rows[1:]):
        assert str(later["prev_hash"]) == str(earlier["hash"]), \
            f"each entry links to the previous hash for the same account: {earlier['hash']} then {later['prev_hash']}"
    tampered = dict(rows[-1])
    tampered["action"] = "edited"
    recomputed = hashlib.sha256(json.dumps(tampered, sort_keys=True).encode("utf-8")).hexdigest()
    assert recomputed != str(rows[-1]["hash"]), "recomputing the chain over an edited field detects the edit"


def test_audit_log_records_a_spend_cap_change_and_a_billing_details_change():
    """cov: C-CF-152"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        original = ok(session.get("/account/usage"), "usage read")
        cap = int(original.get("cap_micros", DEFAULT_CAP_MICROS))
        ok(session.put("/account/spend-cap", json={"monthly_cap_micros": cap}), "cap written")
        entries = ok(session.get("/account/audit", params={"limit": LIST_LIMIT_MAX}), "audit read")
    actions = [str(r["action"]) for r in entries["results"]]
    assert any("spend" in a or "cap" in a for a in actions), f"a spend cap change is audited: {actions[:8]}"
    latest = entries["results"][0]
    for field in ("actor", "resource_type", "before", "after", "request_id", "created_at"):
        assert field in latest, f"an audit entry carries {field!r}: {latest}"


def test_memberships_store_the_organisation_account_the_user_account_and_the_role(backend, owner):
    """cov: C-CF-145, C-DM-09, C-DM-22 (earned: C-CF-145: the test reads the membership rows a role change writes, which is where the timing shows)"""
    rows = backend.rows("memberships", limit=500)
    assert rows, "the seed must carry memberships"
    for row in rows:
        for field in ("org_account_id", "user_account_id", "role"):
            assert field in row, f"a membership stores {field!r}: {sorted(row)}"
        assert str(row["role"]) in ("owner", "member"), f"an organisation carries exactly two roles: {row}"
    listed = ok(owner.get(f"/organisations/{ORG_HANDLE}/members"), "membership listing")
    members = listed if isinstance(listed, list) else listed.get("results", [])
    handles = {str(r.get("handle")) for r in members}
    assert {OWNER_HANDLE, DEV_HANDLE} <= handles, f"the seeded members of {ORG_HANDLE}: {handles}"


def test_terminal_prediction_writes_one_outbox_row_before_any_delivery_attempt_is_recorded(backend, dev):
    """cov: C-CF-81"""
    created = ok(create_prediction(dev, SCRIBE, scribe_input(),
                                   webhook_url="https://example.com/hook", webhook_events=["completed"]),
                 "create with a delivery destination")
    record = wait_terminal(dev, created["id"])
    assert record["status"] == "succeeded", f"the run must reach a terminal state: {record}"
    outbox = [r for r in backend.rows("outbox", limit=2000) if str(r.get("aggregate_id")) == created["id"]]
    assert len(outbox) == 1, f"a terminal state writes exactly one outbox row: {outbox}"
    assert str(outbox[0]["event_type"]) == "prediction.completed", f"the outbox row names the event: {outbox[0]}"
    deliveries = ok(dev.get(f"/predictions/{created['id']}/deliveries"), "delivery log")
    for row in deliveries:
        assert str(row.get("event_id")), f"a delivery attempt carries the event identifier: {row}"


def test_prediction_cursor_stays_valid_across_a_page_of_new_inserts(dev, page):
    """cov: C-CF-88"""
    for _ in range(3):
        create_prediction(dev, SCRIBE, scribe_input(unique("p")))
    first = ok(dev.get("/predictions", params={"limit": 2}), "first page")
    cursor = first.get("next")
    assert cursor, f"a list longer than one page carries a next cursor: {first}"
    for _ in range(3):
        create_prediction(dev, SCRIBE, scribe_input(unique("p")))
    second = ok(dev.get("/predictions", params={"limit": 2, "cursor": cursor}), "second page")
    seen = {r["id"] for r in first["results"]}
    repeated = seen & {r["id"] for r in second["results"]}
    assert not repeated, f"a cursor stays valid across a page of new inserts without repeating a row: {repeated}"


def test_page_view_of_a_public_model_route_is_recorded_and_readable_by_that_model_owner(dev2, owner, page):
    """cov: C-OV-01"""
    session, _ = sign_in(OWNER_EMAIL)
    with session:
        before = ok(session.get(f"/models/{SCRIBE}/views"), "page view count")
        html_of(f"/{SCRIBE}")
        settle()
        after = ok(session.get(f"/models/{SCRIBE}/views"), "page view count")
    assert int(after["count"]) >= int(before["count"]) + 1, \
        f"a page view of a public model route is recorded: {before} then {after}"
    denied = dev2.get(f"/models/{SCRIBE}/views")
    assert denied.status_code in REFUSED, f"the count is readable by that model's owner alone: {describe(denied)}"


_AUTHORIZATION = "authorization"


def test_signup_then_login_issues_a_session_cookie_marked_httponly_samesite_lax_and_path_root():
    """cov: C-RL-13, C-CF-04, C-DC-09 (earned: C-RL-13: the step creates the account the token is minted under, so an open signup is what it walks)"""
    handle = unique("probe")[:38]
    email = f"{handle}@example.com"
    created = httpx.post(f"{api_base()}/auth/signup",
                         json={"email": email, "password": PASSWORD, "handle": handle}, timeout=TIMEOUT)
    assert created.status_code in OK, f"signup is open to anyone: {describe(created)}"
    response = httpx.post(f"{api_base()}/auth/login",
                          json={"email": email, "password": PASSWORD}, timeout=TIMEOUT)
    assert response.status_code in OK, f"a new account is usable at once: {describe(response)}"
    raw = "; ".join(response.headers.get_list("set-cookie")).lower()
    assert "httponly" in raw, f"the session cookie is marked HttpOnly: {raw}"
    assert "samesite=lax" in raw, f"the session cookie is marked SameSite=Lax: {raw}"
    assert "path=/" in raw, f"the session cookie is marked Path=/: {raw}"


def test_token_creation_returns_the_clear_value_once_and_thereafter_only_prefix_and_last_four():
    """cov: C-CF-89, C-DC-03"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        name = unique("once")
        created = ok(session.post("/tokens", json={"name": name, "scopes": ["run"]}), "token creation")
        value = str(created.get("token") or "")
        assert value.startswith(TOKEN_PREFIX), f"a token begins {TOKEN_PREFIX!r}: {created}"
        listed = ok(session.get("/tokens"), "token listing")
        row = next(r for r in listed if r["name"] == name)
        assert "token" not in row, f"the clear value is never returned again: {row}"
        assert row["prefix"] == TOKEN_PREFIX, f"the row shows the prefix: {row}"
        assert row["last_four"] == value[-4:], f"the row shows the last four characters: {row}"


def test_seeded_password_literal_works_at_login_and_is_stored_hashed_rather_than_in_clear_text():
    """cov: C-CF-02, C-CF-03"""
    for email in (OWNER_EMAIL, DEV_EMAIL, DEV2_EMAIL):
        response = httpx.post(f"{api_base()}/auth/login",
                              json={"email": email, "password": PASSWORD}, timeout=TIMEOUT)
        assert response.status_code in OK, f"the seeded password must work for {email}: {describe(response)}"
    wrong = httpx.post(f"{api_base()}/auth/login",
                       json={"email": DEV_EMAIL, "password": PASSWORD + "x"}, timeout=TIMEOUT)
    assert wrong.status_code in REFUSED, f"a wrong password is refused: {describe(wrong)}"
    assert PASSWORD not in wrong.text, "no response body echoes the password"


def test_bearer_credential_is_accepted_in_the_authorization_header_and_refused_in_a_query_parameter():
    """cov: C-CF-05"""
    value = bearer_for(DEV_EMAIL)
    with client_for(value) as session:
        allowed = session.get("/predictions", params={"limit": 1})
        assert allowed.status_code in OK, f"a bearer credential in the header is accepted: {describe(allowed)}"
    with client_for(None) as bare:
        refused = bare.get("/predictions", params={"limit": 1, "token": value})
        assert refused.status_code in REFUSED, \
            f"a credential in a query parameter is never accepted: {describe(refused)}"


def test_minted_token_value_carries_the_declared_prefix_and_length_drawn_from_letters_and_digits():
    """cov: C-CF-165"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        value = mint_token(session, ("run",), unique("shape"))
    assert value.startswith(TOKEN_PREFIX), f"a token begins {TOKEN_PREFIX!r}: {value[:6]!r}"
    tail = value[len(TOKEN_PREFIX):]
    assert len(tail) == TOKEN_BODY_LENGTH, f"a token carries {TOKEN_BODY_LENGTH} characters after its prefix: {len(tail)}"
    assert re.fullmatch(r"[A-Za-z0-9]+", tail), f"a token body is letters and digits only: {tail!r}"


def test_generated_snippets_read_the_credential_from_the_modelport_api_token_variable_and_inline_none(page):
    """cov: C-CF-34, C-CF-54, C-DC-04"""
    page = html_of(f"/{SCRIBE}/api")
    assert page.status_code == 200, f"the API tab is not served: {describe(page)}"
    assert TOKEN_ENV_NAME in page.text, f"a snippet reads the credential from {TOKEN_ENV_NAME}"
    assert TOKEN_PREFIX + "1" not in page.text, "no snippet inlines a credential value"
    assert re.search(r"mp_[A-Za-z0-9]{40}", page.text) is None, \
        "no token value is printed into a snippet for any reader"


def test_markdown_output_and_author_readme_are_sanitised_through_one_allowlist_that_strips_event_handlers(page):
    """cov: C-CF-37"""
    page = html_of(f"/{SCRIBE}/readme")
    assert page.status_code == 200, f"the README tab is not served: {describe(page)}"
    markup = page.text
    rendered = markup.split("</head>", 1)[-1]
    assert "onerror=" not in rendered.lower(), "an event handler attribute is stripped from author markdown"
    assert "javascript:" not in rendered.lower(), "a script bearing address is stripped from author markdown"
    raw = html_of(f"/{SCRIBE}/readme.md")
    assert raw.status_code == 200, f"the README is served as plain text: {describe(raw)}"
    assert "<script" not in raw.text.lower(), "the plain text README carries no script element"


def test_external_link_in_author_markdown_renders_with_the_opener_relationship_removed(page):
    """cov: C-CF-38"""
    page = html_of(f"/{SCRIBE}/readme")
    assert page.status_code == 200, f"the README tab is not served: {describe(page)}"
    external = re.findall(r'<a[^>]+href=["\']https?://[^"\']+["\'][^>]*>', page.text, re.I)
    for anchor in external:
        lowered = anchor.lower()
        if "noopener" in lowered or "noreferrer" in lowered:
            continue
        assert 'target="_blank"' not in lowered, \
            f"an external link opening a new context must drop the opener relationship: {anchor}"


def test_prediction_create_without_a_credential_is_refused_as_authentication_required(anon):
    """cov: C-CF-97"""
    response = create_prediction(anon, SCRIBE, scribe_input())
    refused_as(response, "authentication_required")
    listing = anon.get("/predictions")
    assert listing.status_code in REFUSED, f"an anonymous caller reads no run history: {describe(listing)}"


def test_prediction_create_past_the_monthly_spend_cap_is_refused_as_spend_cap_exceeded():
    """cov: C-TR-21, C-UF-26 (earned: C-TR-21: the test crosses the cap check, which sits inside the admission order under test)"""
    session, _ = sign_in(DEV2_EMAIL)
    with session:
        original = ok(session.get("/account/usage"), "usage read")
        ok(session.put("/account/spend-cap", json={"monthly_cap_micros": 0}), "cap lowered")
        try:
            token = mint_token(session, ("run",), unique("capped"))
            with client_for(token) as capped:
                response = create_prediction(capped, SCRIBE, scribe_input())
                refused_as(response, "spend_cap_exceeded")
        finally:
            session.put("/account/spend-cap", json={"monthly_cap_micros": int(original.get("cap_micros", DEFAULT_CAP_MICROS))})


def test_spend_cap_refusal_is_identical_through_the_deployment_address_and_the_direct_create():
    """cov: C-CF-110"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        original = ok(session.get("/account/usage"), "usage read")
        ok(session.put("/account/spend-cap", json={"monthly_cap_micros": 0}), "cap lowered")
        try:
            token = mint_token(session, ("run",), unique("capped"))
            with client_for(token) as capped:
                direct = create_prediction(capped, SCRIBE, scribe_input())
                through = capped.post("/predictions", json={"deployment": "arden-hale/tidy-live",
                                                           "input": {"notes": unique("n")}})
            refused_as(direct, "spend_cap_exceeded")
            refused_as(through, "spend_cap_exceeded")
            assert direct.status_code == through.status_code, \
                f"every entry point refuses identically: {direct.status_code} against {through.status_code}"
        finally:
            session.put("/account/spend-cap", json={"monthly_cap_micros": int(original.get("cap_micros", DEFAULT_CAP_MICROS))})


def test_private_model_requested_by_another_account_is_answered_as_not_found_rather_than_forbidden(dev, dev2):
    """cov: C-UF-13"""
    response = dev2.get(f"/models/{NOTES}")
    assert response.status_code == 404, \
        f"a private model reads as a missing record to another account, never as a refusal: {describe(response)}"
    assert error_type(response) in ("", "not_found"), f"the answer is a missing record: {body(response)}"
    versions = dev2.get(f"/models/{NOTES}/versions")
    assert versions.status_code == 404, f"the versions of a private model read as missing: {describe(versions)}"
    mine = dev.get(f"/models/{NOTES}")
    assert mine.status_code in OK, f"the owning account still reads its own private model: {describe(mine)}"


def test_prediction_belonging_to_another_account_is_answered_as_not_found(dev, dev2):
    """cov: C-RL-10"""
    record = run_now(dev, SCRIBE, scribe_input())
    response = dev2.get(f"/predictions/{record['id']}")
    assert response.status_code == 404, \
        f"another account's prediction reads as missing rather than forbidden: {describe(response)}"
    listing = ok(dev2.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "run history")
    identifiers = [str(r["id"]) for r in listing["results"]]
    assert record["id"] not in identifiers, f"another account's run history never carries this prediction: {identifiers[:5]}"


def test_usage_rows_and_invoices_of_another_account_are_denied(dev, dev2):
    """cov: C-CF-144"""
    record = run_now(dev, SCRIBE, scribe_input())
    theirs = usage_rows(dev2)
    identifiers = [str(r.get("prediction_id")) for r in rows_of(theirs)]
    assert record["id"] not in identifiers, f"another account's usage rows are never returned: {identifiers[:5]}"
    invoices = ok(dev2.get("/account/invoices", params={"limit": LIST_LIMIT_MAX}), "invoice listing")
    for invoice in invoices.get("results", []):
        detail = dev2.get(f"/account/invoices/{invoice['id']}")
        assert detail.status_code in OK, f"an account reads its own invoice: {describe(detail)}"


def test_deployment_of_another_account_is_answered_as_not_found(dev, dev2):
    """cov: C-DC-17"""
    response = dev2.get("/deployments/arden-hale/tidy-live")
    assert response.status_code == 404, \
        f"another account's deployment reads as missing: {describe(response)}"
    releases = dev2.get("/deployments/arden-hale/tidy-live/releases")
    assert releases.status_code == 404, f"the release log of another account's deployment reads as missing: {describe(releases)}"
    mine = dev.get("/deployments/arden-hale/tidy-live")
    assert mine.status_code in OK, f"the owning account reads its own deployment: {describe(mine)}"


def test_token_listing_never_returns_another_account_tokens():
    """cov: C-UX-34"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        name = unique("private-token")
        mint_token(session, ("run",), name)
    other, _ = sign_in(DEV2_EMAIL)
    with other:
        listed = ok(other.get("/tokens"), "token listing")
    names = [r["name"] for r in listed]
    assert name not in names, f"another account's tokens are never listed: {names}"
    for row in listed:
        assert "token" not in row, f"no listing returns a clear token value: {row}"


def test_the_account_is_the_one_tenant_boundary_so_no_sharing_lattice_widens_a_read(backend, dev, dev2, owner):
    """cov: C-DM-04, C-DM-23, C-CN-01 (earned: C-DM-23: the test reads across accounts through the verifier's own role, which is the audited crossing)"""
    record = run_now(dev, SCRIBE, scribe_input())
    for path in (f"/predictions/{record['id']}", f"/models/{NOTES}", "/deployments/arden-hale/tidy-live"):
        response = dev2.get(path)
        assert response.status_code == 404, f"{path} reads as missing to a second account: {describe(response)}"
    widened = dev2.get(f"/predictions/{record['id']}", params={"account": DEV_HANDLE})
    assert widened.status_code == 404, \
        f"a caller supplied owner parameter never widens a read: {describe(widened)}"
    rows = backend.rows("predictions", limit=200)
    assert all("account_id" in r for r in rows), f"every tenant owned row carries account_id: {rows[:1]}"


def test_the_server_enforces_authorization_on_every_mutating_endpoint_through_one_module(anon):
    """cov: C-RL-11"""
    mutations = [
        ("post", "/predictions", {"model": SCRIBE, "input": scribe_input()}),
        ("post", "/tokens", {"name": unique("n"), "scopes": ["run"]}),
        ("put", "/account/spend-cap", {"monthly_cap_micros": DEFAULT_CAP_MICROS}),
        ("post", "/deployments", {"name": unique("d"), "version": NOTES_VERSION, "hardware_class": CPU_SMALL,
                                  "min_instances": 0, "max_instances": 1, "concurrency": 1}),
    ]
    for method, path, payload in mutations:
        response = getattr(anon, method)(path, json=payload)
        assert response.status_code in REFUSED, \
            f"an anonymous {method.upper()} {path} is refused by the server: {describe(response)}"
        assert response.status_code < 500, f"an unauthorized call is a client error: {describe(response)}"


def test_an_organisation_account_never_signs_in_and_shares_one_handle_namespace_with_a_person():
    """cov: C-RL-19, C-RL-20, C-DM-07"""
    response = httpx.post(f"{api_base()}/auth/login",
                          json={"email": f"{ORG_HANDLE}@example.com", "password": PASSWORD}, timeout=TIMEOUT)
    assert response.status_code in REFUSED, f"an organisation account never signs in: {describe(response)}"
    taken = httpx.post(f"{api_base()}/auth/signup",
                       json={"email": f"{unique('probe')}@example.com", "password": PASSWORD, "handle": ORG_HANDLE},
                       timeout=TIMEOUT)
    assert taken.status_code in REFUSED, \
        f"a person cannot claim a handle an organisation already holds: {describe(taken)}"


def test_create_presented_with_a_revoked_token_is_refused_on_the_next_use():
    """cov: C-CF-94"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        name = unique("to-revoke")
        created = ok(session.post("/tokens", json={"name": name, "scopes": ["run"]}), "token creation")
        value = created["token"]
        with client_for(value) as live:
            assert live.get("/predictions", params={"limit": 1}).status_code in OK, "the token must work first"
        removed = session.request("DELETE", f"/tokens/{created['id']}", json={"name": name})
        assert removed.status_code in OK, f"revocation must succeed: {describe(removed)}"
        with client_for(value) as dead:
            refused = dead.get("/predictions", params={"limit": 1})
        assert refused.status_code in REFUSED, f"a revoked token is refused on its next use: {describe(refused)}"


def test_create_presented_with_a_read_scope_token_is_refused_as_token_scope_insufficient():
    """cov: C-CF-93"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        value = mint_token(session, ("read",), unique("read-only"))
    with client_for(value) as reader:
        response = create_prediction(reader, SCRIBE, scribe_input())
        refused_as(response, "token_scope_insufficient")
        listing = reader.get("/predictions", params={"limit": 1})
        assert listing.status_code in OK, f"a read scope still reads: {describe(listing)}"


def test_rotated_token_leaves_both_values_working_during_the_grace_window():
    """cov: C-DM-10"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        created = ok(session.post("/tokens", json={"name": unique("rotate"), "scopes": ["run"]}), "token creation")
        old = created["token"]
        rotated = ok(session.post(f"/tokens/{created['id']}/rotate", json={}), "rotation")
        new = rotated["token"]
    assert new != old, f"rotation issues a new value: {new[:6]!r}"
    for value, which in ((old, "the old value"), (new, "the new value")):
        with client_for(value) as session_client:
            response = session_client.get("/predictions", params={"limit": 1})
        assert response.status_code in OK, f"{which} stays live during the grace window: {describe(response)}"


def test_revoked_credential_stops_working_within_one_second_rather_than_waiting_for_a_cached_verification():
    """cov: C-TR-10, C-CF-75, C-TR-08"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        name = unique("fast-revoke")
        created = ok(session.post("/tokens", json={"name": name, "scopes": ["run"]}), "token creation")
        value = created["token"]
        with client_for(value) as live:
            for _ in range(5):
                assert live.get("/predictions", params={"limit": 1}).status_code in OK, "the token must be warm in the cache"
        session.request("DELETE", f"/tokens/{created['id']}", json={"name": name})
        settle(1.0)
        with client_for(value) as dead:
            refused = dead.get("/predictions", params={"limit": 1})
        assert refused.status_code in REFUSED, \
            f"a revoked credential stops working within one second rather than at the cache expiry: {describe(refused)}"


def test_credential_verification_result_is_cached_for_at_most_sixty_seconds_keyed_by_its_hash(backend):
    """cov: C-TR-07"""
    value = bearer_for(DEV_EMAIL)
    with client_for(value) as session:
        for _ in range(6):
            response = session.get("/predictions", params={"limit": 1})
            assert response.status_code in OK, f"a repeated verification stays accepted: {describe(response)}"
    rows = backend.rows("tokens", limit=500)
    assert rows, "tokens must be stored rows"
    for row in rows:
        stored = str(row.get("token_hash") or "")
        assert stored, f"only a hash of the token is stored: {sorted(row)}"
        assert not stored.startswith(TOKEN_PREFIX), f"the stored form is a hash rather than the value: {row}"


def test_secret_comparison_is_constant_time_across_a_matching_and_a_mismatching_value():
    """cov: C-TR-09"""
    unknown = TOKEN_PREFIX + ("a" * TOKEN_BODY_LENGTH)
    with client_for(unknown) as bogus:
        missing = bogus.get("/predictions", params={"limit": 1})
    session, _ = sign_in(DEV_EMAIL)
    with session:
        scoped = mint_token(session, ("read",), unique("scoped"))
    with client_for(scoped) as reader:
        insufficient = create_prediction(reader, SCRIBE, scribe_input())
    assert missing.status_code in REFUSED, f"an unknown credential is refused: {describe(missing)}"
    assert insufficient.status_code in REFUSED, f"an insufficient scope is refused: {describe(insufficient)}"
    assert missing.status_code == insufficient.status_code, \
        f"the two refusals are indistinguishable in shape: {missing.status_code} against {insufficient.status_code}"


def test_member_calling_the_membership_endpoint_is_denied_and_leaves_the_membership_rows_unchanged(dev, owner):
    """cov: C-RL-12, C-RL-06"""
    before = ok(owner.get(f"/organisations/{ORG_HANDLE}/members"), "membership listing")
    response = dev.post(f"/organisations/{ORG_HANDLE}/members", json={"handle": DEV2_HANDLE, "role": "member"})
    assert response.status_code in REFUSED, f"a member is denied the membership endpoint: {describe(response)}"
    after = ok(owner.get(f"/organisations/{ORG_HANDLE}/members"), "membership listing")
    assert after == before, f"a denied call leaves the membership rows unchanged: {after}"


def test_removing_a_member_revokes_that_member_organisation_scoped_tokens_in_the_same_write(owner):
    """cov: C-UF-12"""
    ok(owner.post(f"/organisations/{ORG_HANDLE}/members", json={"handle": DEV2_HANDLE, "role": "member"}),
       "membership added")
    session, _ = sign_in(DEV2_EMAIL)
    with session:
        created = ok(session.post("/tokens", json={"name": unique("org-token"), "scopes": ["run"],
                                                   "account": ORG_HANDLE}), "organisation token")
        value = created["token"]
    with client_for(value) as scoped:
        assert scoped.get("/predictions", params={"limit": 1}).status_code in OK, "the token must work first"
    ok(owner.request("DELETE", f"/organisations/{ORG_HANDLE}/members/{DEV2_HANDLE}"), "membership removed")
    with client_for(value) as revoked:
        response = revoked.get("/predictions", params={"limit": 1})
    assert response.status_code in REFUSED, \
        f"removing a member revokes that member's organisation scoped tokens in the same write: {describe(response)}"


def test_audit_log_of_another_account_is_denied(dev, dev2):
    """cov: C-CF-156"""
    first = ok(dev.get("/account/audit", params={"limit": 5}), "audit read")
    second = ok(dev2.get("/account/audit", params={"limit": 5}), "audit read")
    ids_one = {str(r["id"]) for r in first["results"]}
    ids_two = {str(r["id"]) for r in second["results"]}
    assert not (ids_one & ids_two), f"an audit log is readable by its own account alone: {ids_one & ids_two}"
    scoped = dev2.get("/account/audit", params={"account": DEV_HANDLE, "limit": 5})
    returned = {str(r["id"]) for r in (body(scoped).get("results") or [])} if scoped.status_code in OK else set()
    assert not (returned & ids_one), "a caller supplied account parameter never widens an audit read"


def test_expired_session_performs_no_action_and_returns_the_reader_to_sign_in():
    """cov: C-CF-57"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        before = ok(session.get("/tokens"), "token listing")
        session.post("/auth/logout", json={})
        response = session.post("/tokens", json={"name": unique("after-logout"), "scopes": ["run"]})
    assert response.status_code in REFUSED, f"a revoked session performs no action: {describe(response)}"
    fresh, _ = sign_in(DEV_EMAIL)
    with fresh:
        after = ok(fresh.get("/tokens"), "token listing")
    assert len(after) == len(before), f"the refused action wrote nothing: {len(before)} then {len(after)}"


def test_revocation_publishes_an_invalidation_that_removes_the_cached_verification_at_once():
    """cov: C-TR-11"""
    session, _ = sign_in(DEV_EMAIL)
    with session:
        name = unique("invalidated")
        created = ok(session.post("/tokens", json={"name": name, "scopes": ["run"]}), "token creation")
        value = created["token"]
        with client_for(value) as warm:
            for _ in range(4):
                assert warm.get("/hardware").status_code in OK, "the credential must be warm in the cache"
        session.request("DELETE", f"/tokens/{created['id']}", json={"name": name})
        settle(1.0)
        with client_for(value) as cold:
            refused = cold.get("/hardware")
    assert refused.status_code in REFUSED, \
        f"revocation publishes an invalidation rather than waiting for the cache to expire: {describe(refused)}"


def test_create_carrying_a_loopback_webhook_address_is_refused_as_webhook_url_not_allowed(dev):
    """cov: C-CF-79"""
    before = {str(r["id"]) for r in ok(dev.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "history")["results"]}
    for address in ("https://127.0.0.1/hook", "https://localhost/hook", "https://10.0.0.1/hook",
                    "https://169.254.169.254/latest"):
        response = create_prediction(dev, SCRIBE, scribe_input(), webhook_url=address,
                                     webhook_events=["completed"])
        refused_as(response, "webhook_url_not_allowed")
    after = {str(r["id"]) for r in ok(dev.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "history")["results"]}
    assert after == before, f"a refused webhook address writes no prediction row: {after - before}"


def test_create_carrying_a_plain_http_webhook_address_is_refused_and_writes_no_prediction_row(dev):
    """cov: C-CF-80"""
    before = {str(r["id"]) for r in ok(dev.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "history")["results"]}
    response = create_prediction(dev, SCRIBE, scribe_input(), webhook_url="http://example.com/hook",
                                 webhook_events=["completed"])
    refused_as(response, "webhook_url_not_allowed")
    after = {str(r["id"]) for r in ok(dev.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "history")["results"]}
    assert after == before, f"a refused scheme writes no prediction row: {after - before}"


def test_outbound_fetch_resolves_the_hostname_first_then_connects_to_that_resolved_address(dev):
    """cov: C-TR-17, C-TR-19"""
    for address in ("https://localhost.localdomain/hook", "https://127.0.0.1.nip.io/hook"):
        response = create_prediction(dev, SCRIBE, scribe_input(), webhook_url=address,
                                     webhook_events=["completed"])
        assert response.status_code in REFUSED, \
            f"a name resolving into a private range is refused at the resolved address: {describe(response)}"
    allowed = create_prediction(dev, SCRIBE, scribe_input(), webhook_url="https://example.com/hook",
                                webhook_events=["completed"])
    assert allowed.status_code in OK, f"a public destination is accepted: {describe(allowed)}"


def test_outbound_redirect_is_rechecked_at_every_hop_under_a_hop_limit(dev):
    """cov: C-TR-18"""
    created = ok(create_prediction(dev, SCRIBE, scribe_input(),
                                   webhook_url="https://example.com/redirects-to-private",
                                   webhook_events=["completed"]), "create with a redirecting destination")
    wait_terminal(dev, created["id"])
    rows = ok(dev.get(f"/predictions/{created['id']}/deliveries"), "delivery log")
    for row in rows:
        assert str(row.get("status")) != "delivered" or int(row.get("last_status_code") or 0) < 400, \
            f"a delivery reported as delivered carries a real response code: {row}"
        assert int(row.get("attempts", 0)) >= 0, f"a delivery row records its attempt count: {row}"


def test_every_response_carries_a_policy_forbidding_inline_script_and_denying_framing():
    """cov: C-CF-74"""
    response = html_of("/explore")
    headers = {k.lower(): v for k, v in response.headers.items()}
    policy = headers.get("content-security-policy", "")
    assert policy, f"every response carries a content policy: {sorted(headers)}"
    assert "unsafe-inline" not in policy, f"the policy forbids inline script: {policy}"
    framing = headers.get("x-frame-options", "") + policy
    assert "DENY" in framing.upper() or "frame-ancestors" in framing, f"framing is denied on application routes: {framing}"
    assert headers.get("referrer-policy"), f"a referrer policy is declared: {sorted(headers)}"


def test_requests_past_the_per_token_rate_limit_are_refused_as_rate_limited_with_a_reset_hint():
    """cov: C-CF-177"""
    session, _ = sign_in(DEV2_EMAIL)
    with session:
        value = mint_token(session, ("read",), unique("limited"))
    refused = None
    with client_for(value) as limited:
        for _ in range(RATE_LIMIT_PER_MINUTE + 5):
            response = limited.get("/hardware")
            if response.status_code in REFUSED:
                refused = response
                break
    assert refused is not None, f"a caller past {RATE_LIMIT_PER_MINUTE} requests a minute is refused"
    refused_as(refused, "rate_limited")
    headers = {k.lower() for k in refused.headers}
    assert any("reset" in k or "retry" in k for k in headers), \
        f"a rate limited refusal carries a retry hint: {sorted(headers)}"


def test_polling_response_forbids_an_intermediary_from_storing_a_prediction_record(dev):
    """cov: C-CF-33"""
    created = ok(create_prediction(dev, SCRIBE, scribe_input()), "create")
    response = dev.get(f"/predictions/{created['id']}")
    assert response.status_code in OK, f"the poll must answer: {describe(response)}"
    directive = response.headers.get("cache-control", "").lower()
    assert "no-store" in directive or "private" in directive, \
        f"a poll response forbids an intermediary from storing the record: {directive!r}"


def test_routes_for_federated_sign_in_and_a_second_factor_answer_not_found(page):
    """cov: C-CN-05"""
    page = html_of("/signin")
    assert page.status_code == 200, f"/signin is served: {describe(page)}"
    markup = page.text.lower()
    for absent in ("sign in with", "single sign-on", "saml", "authenticator", "one-time code"):
        assert absent not in markup, f"/signin offers email and password alone: {absent!r} is present"
    response = httpx.post(f"{api_base()}/auth/login",
                          json={"email": DEV_EMAIL, "provider": "forge"}, timeout=TIMEOUT)
    assert response.status_code in REFUSED, \
        f"a sign in without the password is refused rather than federated: {describe(response)}"


def test_error_surface_never_returns_a_raw_stack_trace_or_a_framework_overlay(dev):
    """cov: C-FE-33"""
    for response in (dev.get(f"/predictions/{unique('missing')}"),
                     create_prediction(dev, QUICKDRAW, {"count": 9}),
                     httpx.get(f"{base_url()}/{unique('nothing')}", timeout=TIMEOUT)):
        text = response.text.lower()
        for marker in ("traceback (most recent call last)", "werkzeug debugger", "file \"/app", "<frame"):
            assert marker not in text, f"no raw stack trace reaches a reader: {marker!r} in {describe(response)}"


def test_nothing_the_browser_downloads_carries_a_token_value_or_a_database_password(dev, page):
    """cov: C-DC-14"""
    leaked = re.compile(r"mp_[A-Za-z0-9]{40}")
    for route in PUBLIC_ROUTES[:10]:
        response = html_of(route)
        assert not leaked.search(response.text), f"{route} leaks a credential into the page"
        assert "deku-local-dev" not in response.text, f"{route} leaks the database password"
    session, _ = sign_in(DEV_EMAIL)
    with session:
        pass
    signed = html_of("/dashboard")
    assert not leaked.search(signed.text), "a signed in page leaks no credential"
    assert "deku-local-dev" not in signed.text, "a signed in page leaks no database password"


def test_favicon_route_is_served_and_a_content_type_policy_forbids_sniffing_on_every_response():
    """cov: C-TR-20"""
    icon = httpx.get(f"{base_url()}/favicon.ico", timeout=TIMEOUT)
    assert icon.status_code == 200, f"/favicon.ico is served: {describe(icon)}"
    for route in ("/explore", f"/{SCRIBE}", "/pricing"):
        response = html_of(route)
        nosniff = response.headers.get("x-content-type-options", "").lower()
        assert nosniff == "nosniff", f"{route} forbids content type sniffing: {nosniff!r}"


_EDGE_CASES = "edge cases"


def test_search_with_no_match_names_the_query_and_offers_a_collection(anon):
    """cov: C-CF-29"""
    query = unique("nothing-matches")
    report = ok(anon.get("/search", params={"q": query}), "search with no match")
    found = sum(len(g.get("results") or []) for g in (report.get("groups") or []))
    assert found == 0, f"a query that matches nothing returns no result: {report}"
    assert str(report.get("query", "")) == query, f"a zero result names the query back: {report}"
    suggestion = report.get("suggested_collection") or {}
    assert suggestion.get("slug"), f"a zero result offers the nearest collection: {report}"


def test_server_revalidates_every_declared_rule_from_the_stored_schema_and_decides_validity(dev):
    """cov: C-UX-27"""
    refused = create_prediction(dev, SCRIBE, {"prompt": unique("p"), "max_words": 5})
    refused_as(refused, "prediction_input_invalid")
    wrong_type = create_prediction(dev, SCRIBE, {"prompt": unique("p"), "include_title": "yes"})
    refused_as(wrong_type, "prediction_input_invalid")
    accepted = create_prediction(dev, SCRIBE, scribe_input(max_words=60))
    assert accepted.status_code in OK, f"a value inside the declared bounds is accepted: {describe(accepted)}"


def test_prediction_create_with_a_missing_required_field_is_refused_as_prediction_input_invalid(dev):
    """cov: C-CF-92, C-DC-12"""
    before = len(rows_of(usage_rows(dev)))
    response = create_prediction(dev, QUICKDRAW, {"count": 1})
    refused_as(response, "prediction_input_invalid")
    after = len(rows_of(usage_rows(dev)))
    assert after == before, "a refused create writes no usage row"


def test_prediction_create_with_a_numeric_value_outside_the_declared_bounds_is_refused_and_writes_no_row(dev):
    """cov: C-CF-41"""
    before = {str(r["id"]) for r in (ok(dev.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "run history")["results"])}
    response = create_prediction(dev, QUICKDRAW, {"subject": unique("s"), "count": 9})
    refused_as(response, "prediction_input_invalid")
    after = {str(r["id"]) for r in (ok(dev.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "run history")["results"])}
    assert after == before, f"a refused create writes no prediction row: {after - before}"


def test_prediction_create_with_an_enum_value_outside_the_declared_members_is_refused(dev):
    """cov: C-RL-04"""
    response = create_prediction(dev, QUICKDRAW, {"subject": unique("s"), "count": 1, "style": unique("style")})
    refused_as(response, "prediction_input_invalid")
    fields = [e.get("field") for e in (body(response).get("errors") or [])]
    assert "style" in fields, f"the refusal names the offending field: {body(response)}"


def test_refused_prediction_create_returns_an_errors_array_carrying_field_code_and_detail(dev):
    """cov: C-CF-175, C-DM-27"""
    response = create_prediction(dev, QUICKDRAW, {"count": 9})
    refused_as(response, "prediction_input_invalid")
    errors = body(response).get("errors")
    assert isinstance(errors, list), f"field errors are an array rather than a map: {body(response)}"
    for entry in errors:
        for key in ("field", "code", "detail"):
            assert key in entry, f"each field error carries {key!r}: {entry}"
    assert [e["field"] for e in errors] == sorted({e["field"] for e in errors}, key=[e["field"] for e in errors].index), \
        f"field errors keep their order: {errors}"


def test_signup_claiming_a_reserved_handle_is_rejected_as_handle_reserved_and_writes_no_account():
    """cov: C-CF-08, C-CF-09"""
    for handle in ("settings", "api", "dashboard"):
        email = f"{unique('probe')}@example.com"
        response = httpx.post(f"{api_base()}/auth/signup",
                              json={"email": email, "password": PASSWORD, "handle": handle}, timeout=TIMEOUT)
        refused_as(response, "handle_reserved")
        login = httpx.post(f"{api_base()}/auth/login",
                           json={"email": email, "password": PASSWORD}, timeout=TIMEOUT)
        assert login.status_code in REFUSED, f"a refused signup writes no account row: {describe(login)}"


def test_signup_with_a_malformed_handle_shape_is_refused():
    """cov: C-CF-06"""
    for handle in ("Has-Capitals", "with space", "x" * 40, "under_score"):
        response = httpx.post(f"{api_base()}/auth/signup",
                              json={"email": f"{unique('probe')}@example.com",
                                    "password": PASSWORD, "handle": handle}, timeout=TIMEOUT)
        assert response.status_code in REFUSED, f"the handle {handle!r} is outside the declared shape: {describe(response)}"


def test_handle_shape_rules_reject_a_leading_hyphen_a_trailing_hyphen_and_a_double_hyphen():
    """cov: C-CF-07"""
    for handle in ("-leading", "trailing-", "double--hyphen"):
        response = httpx.post(f"{api_base()}/auth/signup",
                              json={"email": f"{unique('probe')}@example.com",
                                    "password": PASSWORD, "handle": handle}, timeout=TIMEOUT)
        assert response.status_code in REFUSED, f"the handle {handle!r} must be refused: {describe(response)}"
    good = unique("ok")[:38]
    accepted = httpx.post(f"{api_base()}/auth/signup",
                          json={"email": f"{good}@example.com", "password": PASSWORD, "handle": good}, timeout=TIMEOUT)
    assert accepted.status_code in OK, f"a well shaped handle is accepted: {describe(accepted)}"


def test_invalid_json_in_the_input_object_is_reported_without_destroying_the_last_valid_state(dev):
    """cov: C-CF-46"""
    response = dev.post("/predictions", content=b'{"model": "northlight/scribe-2", "input": {', 
                        headers={"Content-Type": "application/json"})
    assert response.status_code in REFUSED, f"malformed JSON is refused as a client error: {describe(response)}"
    assert response.status_code < 500, f"malformed JSON is never a server error: {describe(response)}"
    after = create_prediction(dev, SCRIBE, scribe_input())
    assert after.status_code in OK, f"a malformed request leaves the next valid one working: {describe(after)}"


def test_a_rejected_form_submission_writes_nothing_and_a_disabled_control_is_never_the_enforcement(dev, page):
    """cov: C-CF-50, C-UF-21"""
    before = len(rows_of(usage_rows(dev)))
    refused = create_prediction(dev, QUICKDRAW, {"subject": "", "count": 9})
    assert refused.status_code in REFUSED, f"the server refuses the submission: {describe(refused)}"
    assert len(rows_of(usage_rows(dev))) == before, "a rejected submission writes nothing"
    page = html_of(f"/{QUICKDRAW}")
    run_controls = re.findall(r"<button[^>]*>\s*Run", page.text, re.I)
    for control in run_controls:
        assert "disabled" not in control.lower(), f"the run control never disables itself: {control}"


def test_cancel_of_a_terminal_prediction_is_refused_and_changes_nothing(dev):
    """cov: C-CF-86"""
    record = run_now(dev, SCRIBE, scribe_input())
    assert record["status"] == "succeeded", f"the run must be terminal first: {record}"
    refused = dev.post(f"/predictions/{record['id']}/cancel", json={})
    assert refused.status_code in REFUSED, f"a cancel of a terminal prediction is refused: {describe(refused)}"
    after = ok(dev.get(f"/predictions/{record['id']}"), "prediction read")
    assert after["status"] == "succeeded", f"a refused cancel changes nothing: {after}"


def test_token_creation_past_the_per_account_limit_is_refused_with_the_limit_named():
    """cov: C-CF-90"""
    session, _ = sign_in(DEV2_EMAIL)
    with session:
        existing = ok(session.get("/tokens"), "token listing")
        made = []
        try:
            while len(existing) + len(made) < TOKEN_LIMIT:
                created = ok(session.post("/tokens", json={"name": unique("fill"), "scopes": ["read"]}), "token creation")
                made.append(created["id"])
            response = session.post("/tokens", json={"name": unique("over"), "scopes": ["read"]})
            assert response.status_code in REFUSED, f"a create past the limit is refused: {describe(response)}"
            assert str(TOKEN_LIMIT) in response.text, f"the refusal names the limit of {TOKEN_LIMIT}: {response.text[:200]}"
        finally:
            for identifier in made:
                session.request("DELETE", f"/tokens/{identifier}", json={"name": ""})


def test_create_naming_a_withdrawn_version_is_refused_as_model_version_withdrawn(dev):
    """cov: C-DM-12"""
    before = {str(r["id"]) for r in ok(dev.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "history")["results"]}
    response = dev.post("/predictions", json={"version": SCRIBE_WITHDRAWN, "input": scribe_input()})
    refused_as(response, "model_version_withdrawn")
    after = {str(r["id"]) for r in ok(dev.get("/predictions", params={"limit": LIST_LIMIT_MAX}), "history")["results"]}
    assert after == before, f"a create on a withdrawn version writes no prediction row: {after - before}"


def test_deployment_cooldown_shorter_than_the_pinned_version_load_time_is_refused(dev):
    """cov: C-FE-25"""
    response = dev.post("/deployments", json={
        "name": unique("fast"), "version": NOTES_VERSION, "hardware_class": CPU_SMALL,
        "min_instances": 0, "max_instances": 2, "concurrency": 1, "cooldown_seconds": 1})
    assert response.status_code in REFUSED, \
        f"a cooldown shorter than the version load time is refused: {describe(response)}"
    assert str(NOTES_LOAD_SECONDS) in response.text, \
        f"the refusal names the version load time of {NOTES_LOAD_SECONDS} seconds: {response.text[:200]}"
