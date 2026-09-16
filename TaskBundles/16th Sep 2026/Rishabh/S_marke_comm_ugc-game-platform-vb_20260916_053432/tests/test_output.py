"""Observations for deku/ugc-game-platform-vb.

One module, every section and every declared slot. Black box throughout: HTTP
against the deployed app, plus the capability fixtures for the database, the
inbox and the billing platform. Nothing here reads the agent's source.
"""

from __future__ import annotations

import threading

from conftest import (
    ADULT_BAND,
    ADULT_THRESHOLD_YEARS,
    AGE_BAND_CONDITION,
    AURORA_VISOR,
    AURORA_VISOR_CREATOR_KREDZ,
    AURORA_VISOR_KREDZ,
    AURORA_VISOR_PLATFORM_KREDZ,
    BUILDER_PACK,
    BUILDER_PACK_KREDZ,
    BUILDER_PACK_NAME,
    BUILDER_PACK_PRICE_MINOR,
    CHILD_BAND,
    COPPER_HOVERBOARD,
    COPPER_HOVERBOARD_KREDZ,
    CREATOR2_EMAIL,
    CREATOR_EMAIL,
    CREATOR_USERNAME,
    DECOY_FIELD,
    DEEP_VAULT_HEIST,
    DEFAULT_PAGE_LIMIT,
    DENIED_STATUSES,
    LANTERN_DRIFT,
    MALWARE_MARKER,
    MERIDIAN_BANNER,
    MINIMUM_PAYOUT_KREDZ,
    NEBULA_GLIDER,
    OK_STATUSES,
    PENDING_MODERATION,
    PLATFORM_DENOMINATOR,
    PLATFORM_NUMERATOR,
    PLAYER2_EMAIL,
    PLAYER3_EMAIL,
    PLAYER_EMAIL,
    PLAYER_EXTERNAL_KEY,
    PREVIEW_BLOCKED,
    PREVIEW_PENDING,
    PUBLISHED,
    RECEIPT_SUBJECT_PREFIX,
    REFUSED_STATUSES,
    SEARCH_SCOPES,
    SIGN_IN_SUBJECT_PREFIX,
    SKY_FORGE_ARENA,
    SPLIT_RATE_VERSION,
    STARTER_PACK,
    STUDIO_PACK,
    TAX_DOCUMENTS_CONDITION,
    VAULT_KEY,
    as_list,
    body_excerpt,
    extract_code,
    first_instance_id,
    fresh_client,
    poll_until,
    probe_email,
    probe_key,
    settle,
    signup,
    signup_payload,
    today_utc,
    wait_for_email,
    wait_for_invoice,
    years_ago_utc,
)


def _post_ok(response, where: str) -> dict:
    assert response.status_code in OK_STATUSES, (
        where + ": expected a success status, observed "
        + str(response.status_code) + " body " + body_excerpt(response)
    )
    return response.json()


def _refused(response, where: str) -> None:
    assert response.status_code in REFUSED_STATUSES, (
        where + ": expected the request to be refused as a client error, observed "
        + str(response.status_code) + " body " + body_excerpt(response)
    )


def _balance(client_handle) -> int:
    response = client_handle.get("/economy/balance")
    assert response.status_code == 200, (
        "GET /api/economy/balance returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    payload = response.json()
    value = payload.get("balance_kredz")
    assert value is not None, (
        "GET /api/economy/balance carries no balance_kredz: " + body_excerpt(response)
    )
    return int(value)


def _buy_item(client_handle, slug: str, key: str):
    return client_handle.post(
        "/economy/items/" + slug + "/purchase", json={"idempotency_key": key}
    )


def _buy_pack(client_handle, code: str, key: str):
    return client_handle.post(
        "/economy/purchases", json={"pack_code": code, "idempotency_key": key}
    )


def _publish_asset(client_handle, name: str, declared_type: str = "text/plain",
                   payload: str = "a small creator asset payload"):
    return client_handle.post(
        "/creator/assets",
        json={"name": name, "declared_type": declared_type, "payload": payload},
    )


def test_signup_persists_a_stored_identity_row(anon_client, store):
    email = probe_email()
    response = signup(anon_client, signup_payload(years_ago_utc(25), "Probe " + email[6:14], email))
    payload = _post_ok(response, "POST /api/auth/signup")
    assert payload.get("access_token"), (
        "POST /api/auth/signup returned no access_token: " + body_excerpt(response)
    )
    row = poll_until(lambda: store.identity_by_email(email))
    assert row is not None, (
        "signup for " + email + " left no row in the identities table"
    )


def test_signup_stores_the_date_of_birth_rather_than_a_band(anon_client, store):
    email = probe_email()
    dob = years_ago_utc(25)
    signup(anon_client, signup_payload(dob, "Probe " + email[6:14], email))
    row = poll_until(lambda: store.identity_by_email(email))
    assert row is not None, "signup for " + email + " left no identities row"
    stored = str(row.get("date_of_birth") or "")
    assert stored.startswith(dob), (
        "identities.date_of_birth for " + email + " is " + stored
        + ", expected the submitted date " + dob
    )


def test_child_band_is_derived_for_the_seeded_child_account(player2_client):
    response = player2_client.get("/users/authenticated")
    assert response.status_code == 200, (
        "GET /api/users/authenticated for " + PLAYER2_EMAIL + " returned "
        + str(response.status_code) + " body " + body_excerpt(response)
    )
    payload = response.json()
    assert payload.get("age_band") == CHILD_BAND, (
        PLAYER2_EMAIL + " resolves age_band " + str(payload.get("age_band"))
        + ", expected " + CHILD_BAND + " body " + body_excerpt(response)
    )


def test_adult_band_is_derived_for_a_fresh_adult_signup(anon_client):
    email = probe_email()
    dob = years_ago_utc(ADULT_THRESHOLD_YEARS + 7)
    payload = _post_ok(
        signup(anon_client, signup_payload(dob, "Probe " + email[6:14], email)),
        "POST /api/auth/signup",
    )
    with fresh_client(email) as fresh:
        response = fresh.get("/users/authenticated")
    assert response.status_code == 200, (
        "GET /api/users/authenticated returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    assert response.json().get("age_band") == ADULT_BAND, (
        "an account born " + dob + " resolves "
        + str(response.json().get("age_band")) + ", expected " + ADULT_BAND
    )
    assert payload.get("access_token"), "signup returned no access_token"


def test_leap_day_birth_date_resolves_a_band(anon_client):
    email = probe_email()
    response = signup(anon_client, signup_payload("2008-02-29", "Probe " + email[6:14], email))
    _post_ok(response, "POST /api/auth/signup with a 29 February date of birth")
    with fresh_client(email) as fresh:
        who = fresh.get("/users/authenticated")
    assert who.status_code == 200, (
        "a 29 February account could not read its own record: "
        + str(who.status_code) + " " + body_excerpt(who)
    )
    assert who.json().get("age_band") in (CHILD_BAND, "teen", ADULT_BAND), (
        "a 29 February account resolves no known band: " + body_excerpt(who)
    )


def test_short_password_signup_is_refused_as_invalid(anon_client, store):
    email = probe_email()
    body = signup_payload(years_ago_utc(30), "Probe " + email[6:14], email, "short")
    response = signup(anon_client, body)
    _refused(response, "POST /api/auth/signup with a seven-character password")
    settle()
    assert store.count_identities(email) == 0, (
        "a refused signup for " + email + " still wrote an identities row"
    )


def test_signup_carrying_the_decoy_field_is_refused(anon_client, store):
    email = probe_email()
    body = signup_payload(years_ago_utc(30), "Probe " + email[6:14], email)
    body[DECOY_FIELD] = "filled by a robot"
    response = signup(anon_client, body)
    _refused(response, "POST /api/auth/signup with the decoy field filled")
    settle()
    assert store.count_identities(email) == 0, (
        "a decoy-filled signup for " + email + " still wrote an identities row"
    )


def test_repeated_signup_attempts_in_quick_succession_are_refused(anon_client):
    statuses = []
    for _ in range(6):
        email = probe_email()
        response = signup(anon_client, signup_payload(years_ago_utc(30), "Probe " + email[6:14], email))
        statuses.append(response.status_code)
    assert any(code in REFUSED_STATUSES for code in statuses), (
        "six signups submitted back to back from one caller were all accepted: "
        + str(statuses) + ", expected the repeat bar to refuse at least one"
    )


def test_login_answers_with_an_access_token(anon_client):
    response = anon_client.post(
        "/auth/login", json={"email": PLAYER_EMAIL, "password": "deku-demo-pw-2026"}
    )
    assert response.status_code == 200, (
        "POST /api/auth/login for " + PLAYER_EMAIL + " returned "
        + str(response.status_code) + " body " + body_excerpt(response)
    )
    assert response.json().get("access_token"), (
        "login for " + PLAYER_EMAIL + " carries no access_token: " + body_excerpt(response)
    )


def test_capability_metadata_answers_without_a_session(anon_client):
    response = anon_client.get("/auth/metadata")
    assert response.status_code == 200, (
        "GET /api/auth/metadata answered " + str(response.status_code)
        + " to an anonymous caller; capability discovery is anonymous. Body "
        + body_excerpt(response)
    )
    flat = body_excerpt(response).lower()
    assert "password" in flat, (
        "GET /api/auth/metadata names no authentication route: " + body_excerpt(response)
    )


def test_agreements_answer_without_a_session(anon_client):
    response = anon_client.get("/users/agreements", params={"surface": "signup", "locale": "en-US"})
    assert response.status_code == 200, (
        "GET /api/users/agreements answered " + str(response.status_code)
        + " to an anonymous caller. Body " + body_excerpt(response)
    )
    assert as_list(response.json()), (
        "GET /api/users/agreements returned nothing for the signup surface: "
        + body_excerpt(response)
    )


def test_anonymous_authenticated_call_is_denied(anon_client):
    response = anon_client.get("/users/authenticated")
    assert response.status_code in DENIED_STATUSES, (
        "GET /api/users/authenticated answered " + str(response.status_code)
        + " with no session; member data requires one. Body " + body_excerpt(response)
    )


def test_credential_kinds_are_enrolled_and_revocable(player_client):
    response = player_client.get("/auth/credentials")
    assert response.status_code == 200, (
        "GET /api/auth/credentials returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    kinds = set()
    for row in as_list(response.json()):
        kinds.add(str(row.get("kind")))
    assert "password" in kinds, (
        "GET /api/auth/credentials lists no password credential: " + body_excerpt(response)
    )


def test_one_time_code_email_reaches_the_account_inbox(anon_client, inbox):
    response = anon_client.post("/auth/one-time-code", json={"email": PLAYER_EMAIL})
    assert response.status_code in OK_STATUSES, (
        "POST /api/auth/one-time-code returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    message = wait_for_email(inbox, PLAYER_EMAIL, SIGN_IN_SUBJECT_PREFIX)
    assert message is not None, (
        "no message with subject prefix " + SIGN_IN_SUBJECT_PREFIX
        + " reached " + PLAYER_EMAIL
    )
    assert message.to and PLAYER_EMAIL in " ".join(message.to), (
        "the sign-in code went to " + str(message.to) + " rather than " + PLAYER_EMAIL
    )


def test_reused_one_time_code_is_refused(anon_client, inbox):
    anon_client.post("/auth/one-time-code", json={"email": PLAYER3_EMAIL})
    message = wait_for_email(inbox, PLAYER3_EMAIL, SIGN_IN_SUBJECT_PREFIX)
    assert message is not None, (
        "no sign-in code reached " + PLAYER3_EMAIL + " so reuse cannot be observed"
    )
    code = extract_code(message.body)
    assert code, "the sign-in message body carries no six-digit code: " + str(message.body)[:200]
    first = anon_client.post(
        "/auth/one-time-code/verify", json={"email": PLAYER3_EMAIL, "code": code}
    )
    assert first.status_code in OK_STATUSES, (
        "the first redemption of a fresh code returned " + str(first.status_code)
        + " body " + body_excerpt(first)
    )
    second = anon_client.post(
        "/auth/one-time-code/verify", json={"email": PLAYER3_EMAIL, "code": code}
    )
    _refused(second, "redeeming the same one-time code a second time")


def test_pack_catalogue_lists_the_three_seeded_packs(anon_client):
    response = anon_client.get("/economy/packs")
    assert response.status_code == 200, (
        "GET /api/economy/packs returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    codes = set()
    for row in as_list(response.json()):
        codes.add(str(row.get("code")))
    for code in (STARTER_PACK, BUILDER_PACK, STUDIO_PACK):
        assert code in codes, (
            "GET /api/economy/packs omits " + code + ": " + body_excerpt(response)
        )


def test_item_catalogue_lists_the_seeded_marketplace_rows(anon_client):
    response = anon_client.get("/economy/items")
    assert response.status_code == 200, (
        "GET /api/economy/items returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    slugs = set()
    for row in as_list(response.json()):
        slugs.add(str(row.get("slug")))
    for slug in (AURORA_VISOR, NEBULA_GLIDER, COPPER_HOVERBOARD, MERIDIAN_BANNER, VAULT_KEY):
        assert slug in slugs, (
            "GET /api/economy/items omits " + slug + ": " + body_excerpt(response)
        )


def test_item_purchase_splits_the_gross_by_the_seeded_rate(player_client, store):
    before = _balance(player_client)
    response = _buy_item(player_client, AURORA_VISOR, probe_key())
    payload = _post_ok(response, "POST /api/economy/items/" + AURORA_VISOR + "/purchase")
    assert int(payload.get("gross_kredz", -1)) == AURORA_VISOR_KREDZ, (
        "the sale reports gross " + str(payload.get("gross_kredz"))
        + ", expected " + str(AURORA_VISOR_KREDZ)
    )
    assert int(payload.get("platform_kredz", -1)) == AURORA_VISOR_PLATFORM_KREDZ, (
        "the sale reports a platform share of " + str(payload.get("platform_kredz"))
        + ", expected " + str(AURORA_VISOR_PLATFORM_KREDZ)
        + " from rate version " + str(SPLIT_RATE_VERSION)
    )
    assert int(payload.get("creator_kredz", -1)) == AURORA_VISOR_CREATOR_KREDZ, (
        "the sale reports a creator share of " + str(payload.get("creator_kredz"))
        + ", expected " + str(AURORA_VISOR_CREATOR_KREDZ)
    )
    after = _balance(player_client)
    assert before - after == AURORA_VISOR_KREDZ, (
        "the buyer balance moved from " + str(before) + " to " + str(after)
        + ", expected a debit of " + str(AURORA_VISOR_KREDZ)
    )


def test_indivisible_gross_gives_the_remainder_to_the_creator(player_client):
    response = _buy_item(player_client, COPPER_HOVERBOARD, probe_key())
    payload = _post_ok(response, "POST /api/economy/items/" + COPPER_HOVERBOARD + "/purchase")
    platform = int(payload.get("platform_kredz", -1))
    creator = int(payload.get("creator_kredz", -1))
    assert platform == 0, (
        "a gross of " + str(COPPER_HOVERBOARD_KREDZ) + " split "
        + str(PLATFORM_NUMERATOR) + " of " + str(PLATFORM_DENOMINATOR)
        + " truncates the platform share to 0, observed " + str(platform)
    )
    assert creator == COPPER_HOVERBOARD_KREDZ, (
        "the remainder must reach the creator: observed " + str(creator)
        + ", expected " + str(COPPER_HOVERBOARD_KREDZ)
    )
    assert platform + creator == COPPER_HOVERBOARD_KREDZ, (
        "the two shares sum to " + str(platform + creator)
        + ", expected the gross " + str(COPPER_HOVERBOARD_KREDZ)
    )


def test_purchase_below_the_items_minimum_band_is_denied(player2_client, store):
    before = store.all_sales()
    response = _buy_item(player2_client, VAULT_KEY, probe_key())
    _refused(response, PLAYER2_EMAIL + " buying the teen-only item " + VAULT_KEY)
    settle()
    after = store.all_sales()
    assert len(after) == len(before), (
        "a refused age-gated purchase still wrote a sales row: "
        + str(len(before)) + " before, " + str(len(after)) + " after"
    )


def test_creator_buying_its_own_item_is_denied(creator_client, store):
    before = store.all_sales()
    response = _buy_item(creator_client, AURORA_VISOR, probe_key())
    _refused(response, CREATOR_EMAIL + " buying the creator's own item")
    settle()
    assert len(store.all_sales()) == len(before), (
        "a creator buying its own item still wrote a sales row"
    )


def test_short_balance_purchase_is_refused(player3_client, store):
    response = _buy_item(player3_client, NEBULA_GLIDER, probe_key())
    _refused(response, PLAYER3_EMAIL + " buying an item beyond the seeded balance")
    settle()
    assert _balance(player3_client) >= 0, (
        "a refused purchase pushed the balance below zero for " + PLAYER3_EMAIL
    )


def test_payout_refusal_names_the_failing_payout_condition(creator2_client):
    response = creator2_client.post(
        "/economy/payouts", json={"amount_kredz": MINIMUM_PAYOUT_KREDZ, "idempotency_key": probe_key()}
    )
    _refused(response, CREATOR2_EMAIL + " requesting a payout with tax documents unmet")
    flat = body_excerpt(response).lower()
    assert TAX_DOCUMENTS_CONDITION in flat, (
        "the refusal for " + CREATOR2_EMAIL + " names no failing condition; expected "
        + TAX_DOCUMENTS_CONDITION + ", body " + body_excerpt(response)
    )


def test_payout_eligibility_answers_every_condition_separately(creator_client):
    response = creator_client.get("/economy/payouts/eligibility")
    assert response.status_code == 200, (
        "GET /api/economy/payouts/eligibility returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    flat = body_excerpt(response).lower()
    for condition in (AGE_BAND_CONDITION, "identity_verified", TAX_DOCUMENTS_CONDITION,
                      "minimum_balance", "good_standing", "region_supported"):
        assert condition in flat, (
            "GET /api/economy/payouts/eligibility omits " + condition + ": "
            + body_excerpt(response)
        )


def test_payout_above_the_derived_balance_is_refused(creator_client, store):
    identity = store.identity_by_email(CREATOR_EMAIL)
    assert identity is not None, CREATOR_EMAIL + " has no identities row"
    before = store.payout_requests_for(identity.get("id"))
    response = creator_client.post(
        "/economy/payouts", json={"amount_kredz": 10000000, "idempotency_key": probe_key()}
    )
    _refused(response, "a payout far above the creator's derived balance")
    settle()
    after = store.payout_requests_for(identity.get("id"))
    settled = 0
    for row in after:
        if str(row.get("state")) == "settled":
            settled += 1
    assert settled == 0, (
        "an over-balance payout settled anyway: " + str(len(before)) + " requests before, "
        + str(len(after)) + " after, " + str(settled) + " settled"
    )


def test_asset_state_move_outside_the_permitted_table_is_refused(creator_client):
    created = _post_ok(_publish_asset(creator_client, "Probe Asset " + probe_key()[6:14]),
                       "POST /api/creator/assets")
    asset_id = created.get("id")
    assert asset_id is not None, "POST /api/creator/assets returned no id"
    response = creator_client.patch(
        "/creator/assets/" + str(asset_id), json={"state": "deleted"}
    )
    _refused(response, "moving a fresh asset straight to deleted")


def test_rename_of_a_published_asset_returns_to_moderation(creator_client, store):
    created = _post_ok(_publish_asset(creator_client, "Probe Rename " + probe_key()[6:14]),
                       "POST /api/creator/assets")
    asset_id = created.get("id")
    published = poll_until(
        lambda: store.asset_by_id(asset_id) if
        str((store.asset_by_id(asset_id) or {}).get("state")) == PUBLISHED else None
    )
    assert published is not None, (
        "asset " + str(asset_id) + " never reached " + PUBLISHED
        + ", observed " + str((store.asset_by_id(asset_id) or {}).get("state"))
    )
    response = creator_client.patch(
        "/creator/assets/" + str(asset_id), json={"name": "Probe Renamed " + probe_key()[6:14]}
    )
    assert response.status_code in OK_STATUSES, (
        "renaming a published asset returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    row = poll_until(
        lambda: store.asset_by_id(asset_id) if
        str((store.asset_by_id(asset_id) or {}).get("state")) == PENDING_MODERATION else None
    )
    assert row is not None, (
        "a renamed published asset stayed at "
        + str((store.asset_by_id(asset_id) or {}).get("state"))
        + ", expected " + PENDING_MODERATION
    )


def test_declared_type_disagreeing_with_the_payload_is_refused(creator_client):
    response = _publish_asset(
        creator_client, "Probe Mismatch " + probe_key()[6:14],
        declared_type="image/png", payload="this is plainly not a png payload",
    )
    _refused(response, "an asset declaring image/png with a text payload")


def test_payload_carrying_the_malware_marker_is_refused(creator_client):
    response = _publish_asset(
        creator_client, "Probe Malware " + probe_key()[6:14], payload=MALWARE_MARKER
    )
    _refused(response, "an asset payload carrying the malware marker")


def test_preview_of_a_fresh_asset_is_pending(creator_client, anon_client):
    created = _post_ok(_publish_asset(creator_client, "Probe Preview " + probe_key()[6:14]),
                       "POST /api/creator/assets")
    asset_id = created.get("id")
    response = anon_client.get(
        "/thumbnails/previews", params={"asset_ids": str(asset_id), "size": "medium"}
    )
    assert response.status_code == 200, (
        "GET /api/thumbnails/previews returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    states = set()
    for row in as_list(response.json()):
        states.add(str(row.get("state")))
    assert states, "GET /api/thumbnails/previews answered no rows: " + body_excerpt(response)
    assert states <= {PREVIEW_PENDING, "ready", "unavailable", PREVIEW_BLOCKED}, (
        "GET /api/thumbnails/previews answered unknown state(s) " + str(states)
    )


def test_preview_batch_answers_many_asset_ids_in_one_response(creator_client, anon_client):
    first = _post_ok(_publish_asset(creator_client, "Probe Batch A " + probe_key()[6:14]),
                     "POST /api/creator/assets")
    second = _post_ok(_publish_asset(creator_client, "Probe Batch B " + probe_key()[6:14]),
                      "POST /api/creator/assets")
    ids = str(first.get("id")) + "," + str(second.get("id"))
    response = anon_client.get(
        "/thumbnails/previews", params={"asset_ids": ids, "size": "small"}
    )
    assert response.status_code == 200, (
        "GET /api/thumbnails/previews for two asset ids returned "
        + str(response.status_code) + " body " + body_excerpt(response)
    )
    assert len(as_list(response.json())) >= 2, (
        "a two-id preview request answered fewer than two rows: " + body_excerpt(response)
    )


def test_search_resolves_each_of_the_four_scopes(anon_client):
    for scope in SEARCH_SCOPES:
        response = anon_client.get(
            "/games/search", params={"q": "a", "scope": scope, "limit": DEFAULT_PAGE_LIMIT}
        )
        assert response.status_code == 200, (
            "GET /api/games/search scope " + scope + " returned "
            + str(response.status_code) + " body " + body_excerpt(response)
        )


def test_age_ineligible_experience_is_filtered_before_ranking(player2_client):
    response = player2_client.get(
        "/games/search", params={"q": "vault", "scope": "games", "limit": DEFAULT_PAGE_LIMIT}
    )
    assert response.status_code == 200, (
        "GET /api/games/search for the child account returned "
        + str(response.status_code) + " body " + body_excerpt(response)
    )
    flat = body_excerpt(response)
    assert DEEP_VAULT_HEIST not in flat, (
        DEEP_VAULT_HEIST + " reached a " + CHILD_BAND + " viewer: " + flat
    )


def test_charts_page_by_cursor_shows_every_row_once(anon_client):
    first = anon_client.get("/games/charts", params={"limit": 2})
    assert first.status_code == 200, (
        "GET /api/games/charts returned " + str(first.status_code)
        + " body " + body_excerpt(first)
    )
    payload = first.json()
    page_one = as_list(payload)
    cursor = None
    if isinstance(payload, dict):
        cursor = payload.get("cursor") or payload.get("next_cursor")
    if not cursor:
        assert page_one, "GET /api/games/charts answered an empty first page"
        return
    second = anon_client.get("/games/charts", params={"limit": 2, "cursor": cursor})
    assert second.status_code == 200, (
        "GET /api/games/charts with a cursor returned " + str(second.status_code)
        + " body " + body_excerpt(second)
    )
    seen_one = set()
    for row in page_one:
        seen_one.add(str(row.get("slug")))
    for row in as_list(second.json()):
        assert str(row.get("slug")) not in seen_one, (
            "slug " + str(row.get("slug")) + " appears on two consecutive pages"
        )


def test_empty_search_result_is_a_defined_state(anon_client):
    response = anon_client.get(
        "/games/search",
        params={"q": "zzq" + probe_key()[6:14], "scope": "games", "limit": DEFAULT_PAGE_LIMIT},
    )
    assert response.status_code == 200, (
        "an empty search answered " + str(response.status_code)
        + " rather than an empty result: " + body_excerpt(response)
    )
    assert as_list(response.json()) == [], (
        "a query matching nothing returned rows: " + body_excerpt(response)
    )


def test_join_records_a_reservation_row_and_drops_free_slots(player_client, store):
    instance_id = first_instance_id(store, LANTERN_DRIFT)
    before = store.reservations_for(instance_id)
    response = player_client.post("/games/" + LANTERN_DRIFT + "/join", json={})
    payload = _post_ok(response, "POST /api/games/" + LANTERN_DRIFT + "/join")
    assert payload.get("token"), (
        "the join response carries no reservation token: " + body_excerpt(response)
    )
    after = poll_until(
        lambda: store.reservations_for(instance_id)
        if len(store.reservations_for(instance_id)) > len(before) else None
    )
    assert after is not None, (
        "joining " + LANTERN_DRIFT + " wrote no reservations row: "
        + str(len(before)) + " before"
    )


def test_reservation_token_cannot_be_consumed_twice(player_client, store):
    payload = _post_ok(
        player_client.post("/games/" + LANTERN_DRIFT + "/join", json={}),
        "POST /api/games/" + LANTERN_DRIFT + "/join",
    )
    token = payload.get("token")
    assert token, "the join response carries no reservation token"
    first = player_client.post("/games/reservations/" + str(token) + "/connect", json={})
    assert first.status_code in OK_STATUSES, (
        "the first connect with a fresh reservation token returned "
        + str(first.status_code) + " body " + body_excerpt(first)
    )
    second = player_client.post("/games/reservations/" + str(token) + "/connect", json={})
    _refused(second, "consuming one reservation token twice")


def test_age_ineligible_join_is_refused_at_placement(player2_client, store):
    experience = store.experience_by_slug(DEEP_VAULT_HEIST)
    assert experience is not None, DEEP_VAULT_HEIST + " is missing from experiences"
    before = store.instances_for(experience.get("id"))
    response = player2_client.post("/games/" + DEEP_VAULT_HEIST + "/join", json={})
    _refused(response, PLAYER2_EMAIL + " joining the teen-only experience")
    settle()
    after = store.instances_for(experience.get("id"))
    assert len(after) == len(before), (
        "a refused placement changed the instance rows for " + DEEP_VAULT_HEIST
    )


def test_presence_row_carries_a_lease_expiry(player_client, store):
    payload = _post_ok(
        player_client.post("/games/" + LANTERN_DRIFT + "/join", json={}),
        "POST /api/games/" + LANTERN_DRIFT + "/join",
    )
    token = payload.get("token")
    player_client.post("/games/reservations/" + str(token) + "/connect", json={})
    instance_id = first_instance_id(store, LANTERN_DRIFT)
    rows = poll_until(lambda: store.presences_for(instance_id))
    assert rows, "connecting to " + LANTERN_DRIFT + " wrote no presences row"
    assert rows[0].get("expires_at") is not None, (
        "a presences row carries no expires_at, so presence is a record rather than a lease"
    )


def test_restricted_communication_direct_call_is_denied(player2_client):
    response = player2_client.post(
        "/users/messages", json={"to": PLAYER_EMAIL, "body": "hello from a restricted account"}
    )
    assert response.status_code in DENIED_STATUSES + REFUSED_STATUSES, (
        "a restricted communication straight against the API answered "
        + str(response.status_code) + " body " + body_excerpt(response)
    )


def test_telemetry_event_redacts_a_member_identifier(anon_client):
    marker = probe_key()
    response = anon_client.post(
        "/metrics/events",
        json={
            "application": "web",
            "event": "authPageload",
            "context": "loginPage",
            "address": "/settings/sessions?member=" + marker,
        },
    )
    assert response.status_code in OK_STATUSES, (
        "POST /api/metrics/events returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    assert marker not in body_excerpt(response), (
        "the recorded event echoed the member identifier " + marker
        + " rather than redacting it: " + body_excerpt(response)
    )


def test_locale_bundle_answers_one_namespace(anon_client):
    response = anon_client.get("/locale/bundles/navigation", params={"locale": "en-US"})
    assert response.status_code == 200, (
        "GET /api/locale/bundles/navigation returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    assert body_excerpt(response).strip(), (
        "the navigation namespace answered an empty body"
    )


def test_experiment_assignment_is_stable_across_two_clients(player_client):
    first = player_client.get("/experiments/layers")
    assert first.status_code == 200, (
        "GET /api/experiments/layers returned " + str(first.status_code)
        + " body " + body_excerpt(first)
    )
    with fresh_client(PLAYER_EMAIL) as other:
        second = other.get("/experiments/layers")
    assert second.status_code == 200, (
        "a second client reading /api/experiments/layers returned " + str(second.status_code)
    )
    assert first.json() == second.json(), (
        "one member received two different assignments: "
        + body_excerpt(first) + " then " + body_excerpt(second)
    )


def test_flags_answer_for_an_anonymous_caller(anon_client):
    response = anon_client.get("/flags", params={"application": "web", "namespace": "navigation"})
    assert response.status_code == 200, (
        "GET /api/flags answered " + str(response.status_code)
        + " to an anonymous caller; the surface needs a defined answer. Body "
        + body_excerpt(response)
    )


def test_health_route_answers_ready(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        "GET /api/health returned " + str(response.status_code)
        + " body " + body_excerpt(response)
    )


def test_security_headers_are_present_on_every_response(anon_client):
    response = anon_client.get("/health")
    headers = {}
    for key in response.headers:
        headers[key.lower()] = response.headers[key]
    assert headers.get("x-content-type-options", "").lower() == "nosniff", (
        "no nosniff content-type policy on GET /api/health: " + str(sorted(headers))
    )
    assert "strict-transport-security" in headers, (
        "no strict transport policy on GET /api/health: " + str(sorted(headers))
    )


def test_no_secret_appears_in_what_the_browser_downloads(anon_client):
    response = anon_client.get("/auth/metadata")
    flat = response.text
    for forbidden in ("orbit-labs-secret-9f14c73e", "deku-local-dev", "kbdb-root-5c92e4a1"):
        assert forbidden not in flat, (
            "a service credential reached a browser-readable response: " + forbidden
        )


def test_sitemap_and_robots_resolve(anon_client):
    base = anon_client.base_url
    import httpx

    root = str(base).rsplit("/api", 1)[0]
    with httpx.Client(timeout=30.0) as raw:
        sitemap = raw.get(root + "/sitemap.xml")
        robots = raw.get(root + "/robots.txt")
    assert sitemap.status_code == 200, (
        "/sitemap.xml returned " + str(sitemap.status_code)
    )
    assert robots.status_code == 200, (
        "/robots.txt returned " + str(robots.status_code)
    )
    assert "sitemap" in robots.text.lower(), (
        "/robots.txt names no sitemap: " + robots.text[:200]
    )


def test_unknown_path_answers_not_found(anon_client):
    import httpx

    root = str(anon_client.base_url).rsplit("/api", 1)[0]
    with httpx.Client(timeout=30.0, follow_redirects=False) as raw:
        response = raw.get(root + "/no-such-place-" + probe_key()[6:14])
    assert response.status_code == 404, (
        "an unknown address answered " + str(response.status_code)
        + " rather than a not-found status"
    )


def test_balance_is_derived_from_stored_ledger_rows(player_client, store):
    identity = store.identity_by_email(PLAYER_EMAIL)
    assert identity is not None, PLAYER_EMAIL + " has no identities row"
    account = store.account_for(identity.get("id"), "user")
    assert account is not None, PLAYER_EMAIL + " has no user account row"
    rows = store.entries_for_account(account.get("id"))
    assert rows, "the user account for " + PLAYER_EMAIL + " has no ledger entries"
    reported = _balance(player_client)
    assert store.sum_entries(rows) == reported, (
        "GET /api/economy/balance reports " + str(reported)
        + " but the stored entries sum to " + str(store.sum_entries(rows))
    )


def test_transaction_entries_sum_to_zero(player_client, store):
    key = probe_key()
    _post_ok(_buy_item(player_client, MERIDIAN_BANNER, key),
             "POST /api/economy/items/" + MERIDIAN_BANNER + "/purchase")
    transaction = poll_until(lambda: store.transaction_by_key(key))
    assert transaction is not None, "no transaction row carries idempotency_key " + key
    rows = store.entries_for(transaction.get("id"))
    assert len(rows) >= 3, (
        "an item purchase wrote " + str(len(rows)) + " entries, expected at least three"
    )
    assert store.sum_entries(rows) == 0, (
        "the entries of transaction " + key + " sum to " + str(store.sum_entries(rows))
    )


def test_duplicate_idempotency_key_creates_one_stored_transaction(player_client, store):
    key = probe_key()
    first = _buy_item(player_client, MERIDIAN_BANNER, key)
    _post_ok(first, "the first purchase with a fresh idempotency key")
    before = _balance(player_client)
    for _ in range(4):
        _buy_item(player_client, MERIDIAN_BANNER, key)
    settle()
    assert store.count_transactions_by_key(key) == 1, (
        "idempotency key " + key + " produced "
        + str(store.count_transactions_by_key(key)) + " transactions, expected one"
    )
    assert _balance(player_client) == before, (
        "a repeated purchase with one idempotency key moved the balance again"
    )


def test_ledger_entries_are_never_updated_after_commit(player_client, store):
    key = probe_key()
    _post_ok(_buy_item(player_client, MERIDIAN_BANNER, key),
             "POST /api/economy/items/" + MERIDIAN_BANNER + "/purchase")
    transaction = poll_until(lambda: store.transaction_by_key(key))
    assert transaction is not None, "no transaction row carries idempotency_key " + key
    before = store.entries_for(transaction.get("id"))
    _buy_item(player_client, MERIDIAN_BANNER, probe_key())
    settle()
    after = store.entries_for(transaction.get("id"))
    assert len(after) == len(before), (
        "the entry count for transaction " + key + " changed from "
        + str(len(before)) + " to " + str(len(after))
    )
    assert store.sum_entries(after) == store.sum_entries(before), (
        "the entries of a committed transaction were rewritten"
    )


def test_issued_minus_redeemed_reconciles_with_every_balance(store):
    rows = store.all_entries()
    assert rows, "the ledger_entries table is empty"
    assert store.sum_entries(rows) == 0, (
        "every ledger entry in the system sums to "
        + str(store.sum_entries(rows)) + ", expected zero across issuance and redemption"
    )


def test_sale_row_records_the_rate_version_it_was_priced_at(player_client, store):
    key = probe_key()
    _post_ok(_buy_item(player_client, NEBULA_GLIDER, key),
             "POST /api/economy/items/" + NEBULA_GLIDER + "/purchase")
    item = store.item_by_slug(NEBULA_GLIDER)
    assert item is not None, NEBULA_GLIDER + " is missing from the items table"
    rows = poll_until(lambda: store.sales_for_item(item.get("id")))
    assert rows, "buying " + NEBULA_GLIDER + " wrote no sales row"
    latest = rows[-1]
    assert int(latest.get("rate_version", -1)) == SPLIT_RATE_VERSION, (
        "the sale records rate_version " + str(latest.get("rate_version"))
        + ", expected " + str(SPLIT_RATE_VERSION)
    )
    assert (int(latest.get("creator_kredz", 0)) + int(latest.get("platform_kredz", 0))
            == int(latest.get("gross_kredz", -1))), (
        "the stored shares do not sum to the stored gross on the sales row"
    )


def test_seeding_twice_creates_no_duplicate_stored_row(store):
    assert store.count_identities(PLAYER_EMAIL) == 1, (
        PLAYER_EMAIL + " appears " + str(store.count_identities(PLAYER_EMAIL))
        + " times in identities; seeding must be idempotent"
    )
    assert store.count_identities(CREATOR_EMAIL) == 1, (
        CREATOR_EMAIL + " appears " + str(store.count_identities(CREATOR_EMAIL))
        + " times in identities; seeding must be idempotent"
    )


def test_item_version_survives_a_later_price_change(creator_client, store):
    item = store.item_by_slug(AURORA_VISOR)
    assert item is not None, AURORA_VISOR + " is missing from the items table"
    versions_before = store.item_versions(item.get("id"))
    assert versions_before, AURORA_VISOR + " has no item_versions rows"
    original = versions_before[0]
    response = creator_client.patch(
        "/creator/assets/" + str(item.get("id")), json={"price_kredz": AURORA_VISOR_KREDZ + 5}
    )
    assert response.status_code in OK_STATUSES + REFUSED_STATUSES + DENIED_STATUSES, (
        "a price change returned an unexpected status " + str(response.status_code)
    )
    settle()
    versions_after = store.item_versions(item.get("id"))
    kept = None
    for row in versions_after:
        if row.get("version") == original.get("version"):
            kept = row
    assert kept is not None, (
        "version " + str(original.get("version")) + " of " + AURORA_VISOR
        + " no longer resolves after a price change"
    )
    assert kept.get("price_kredz") == original.get("price_kredz"), (
        "an earlier item version was rewritten by a later price change"
    )


def test_player_calling_a_creator_route_is_denied(player_client, store):
    response = player_client.get("/economy/sales")
    assert response.status_code in DENIED_STATUSES, (
        PLAYER_EMAIL + " reading /api/economy/sales answered "
        + str(response.status_code) + ", expected a denial. Body " + body_excerpt(response)
    )


def test_creator_cannot_read_another_creators_sales(creator2_client, store):
    item = store.item_by_slug(AURORA_VISOR)
    assert item is not None, AURORA_VISOR + " is missing from the items table"
    response = creator2_client.get("/economy/sales")
    if response.status_code == 200:
        for row in as_list(response.json()):
            assert str(row.get("item_id")) != str(item.get("id")), (
                CREATOR2_EMAIL + " read a sale belonging to " + CREATOR_USERNAME
            )
    else:
        assert response.status_code in DENIED_STATUSES, (
            "reading another creator's sales answered " + str(response.status_code)
        )


def test_role_in_the_request_body_is_ignored(player_client, store):
    response = player_client.post(
        "/creator/assets",
        json={"name": "Probe Escalation", "declared_type": "text/plain",
              "payload": "escalation attempt", "role": "creator"},
    )
    assert response.status_code in DENIED_STATUSES + REFUSED_STATUSES, (
        "a player claiming role creator in the body answered "
        + str(response.status_code) + " body " + body_excerpt(response)
    )


def test_age_band_in_the_request_body_is_ignored(player2_client, store):
    before = store.all_sales()
    response = player2_client.post(
        "/economy/items/" + VAULT_KEY + "/purchase",
        json={"idempotency_key": probe_key(), "age_band": ADULT_BAND},
    )
    _refused(response, "a child account asserting an adult band in the request body")
    settle()
    assert len(store.all_sales()) == len(before), (
        "a client-asserted age band let a restricted purchase through"
    )


def test_session_revocation_leaves_other_sessions_alive(player_client):
    with fresh_client(PLAYER_EMAIL) as other:
        logout = other.post("/auth/logout", json={})
        assert logout.status_code in OK_STATUSES, (
            "POST /api/auth/logout returned " + str(logout.status_code)
            + " body " + body_excerpt(logout)
        )
    survivor = player_client.get("/users/authenticated")
    assert survivor.status_code == 200, (
        "revoking one session also ended another: GET /api/users/authenticated "
        "answered " + str(survivor.status_code)
    )


def test_concurrent_purchases_of_the_last_affordable_item(player3_client, store):
    results = []
    barrier = threading.Barrier(2)

    def attempt():
        with fresh_client(PLAYER3_EMAIL) as c:
            barrier.wait()
            results.append(_buy_item(c, AURORA_VISOR, probe_key()).status_code)

    workers = [threading.Thread(target=attempt) for _ in range(2)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join(timeout=60)
    accepted = 0
    for code in results:
        if code in OK_STATUSES:
            accepted += 1
    assert accepted == 1, (
        "two simultaneous purchases against a balance covering one produced "
        + str(accepted) + " successes, statuses " + str(results)
    )
    assert _balance(player3_client) >= 0, (
        "the balance for " + PLAYER3_EMAIL + " went negative under contention"
    )


def test_concurrent_joins_against_one_free_slot(store):
    results = []
    barrier = threading.Barrier(2)

    def attempt():
        with fresh_client(PLAYER_EMAIL) as c:
            barrier.wait()
            results.append(c.post("/games/" + SKY_FORGE_ARENA + "/join", json={}).status_code)

    workers = [threading.Thread(target=attempt) for _ in range(2)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join(timeout=60)
    accepted = 0
    for code in results:
        if code in OK_STATUSES:
            accepted += 1
    assert accepted == 1, (
        "two simultaneous joins against one free slot produced " + str(accepted)
        + " reservations, statuses " + str(results)
    )
    instance_id = first_instance_id(store, SKY_FORGE_ARENA)
    rows = store.instances_for(store.experience_by_slug(SKY_FORGE_ARENA).get("id"))
    for row in rows:
        if row.get("id") == instance_id:
            assert int(row.get("free_slots", 0)) >= 0, (
                "free_slots went negative on " + SKY_FORGE_ARENA
            )


def test_kredz_pack_purchase_creates_one_billing_account(player_client, store, payments):
    _post_ok(_buy_pack(player_client, STARTER_PACK, probe_key()),
             "POST /api/economy/purchases for " + STARTER_PACK)
    row = poll_until(lambda: store.billing_account(PLAYER_EXTERNAL_KEY))
    assert row is not None, (
        "no billing_accounts row carries external_key " + PLAYER_EXTERNAL_KEY
    )
    assert store.count_billing_accounts(PLAYER_EXTERNAL_KEY) == 1, (
        "external_key " + PLAYER_EXTERNAL_KEY + " appears "
        + str(store.count_billing_accounts(PLAYER_EXTERNAL_KEY)) + " times"
    )
    keys = set()
    for account in payments.accounts():
        keys.add(str(account.get("externalKey")))
    assert PLAYER_EXTERNAL_KEY in keys, (
        "the billing platform holds no account with external key "
        + PLAYER_EXTERNAL_KEY + "; observed " + str(sorted(keys))[:300]
    )


def test_kredz_pack_purchase_creates_one_invoice_for_the_price(player_client, payments):
    before = _balance(player_client)
    _post_ok(_buy_pack(player_client, BUILDER_PACK, probe_key()),
             "POST /api/economy/purchases for " + BUILDER_PACK)
    charge = wait_for_invoice(payments, BUILDER_PACK_PRICE_MINOR, "usd")
    assert charge is not None, (
        "no invoice for " + str(BUILDER_PACK_PRICE_MINOR)
        + " minor units in usd reached the billing platform after buying "
        + BUILDER_PACK_NAME
    )
    assert charge.amount == BUILDER_PACK_PRICE_MINOR, (
        "the invoice amount is " + str(charge.amount) + ", expected "
        + str(BUILDER_PACK_PRICE_MINOR)
    )
    after = _balance(player_client)
    assert after - before == BUILDER_PACK_KREDZ, (
        "buying " + BUILDER_PACK_NAME + " moved the balance by "
        + str(after - before) + ", expected " + str(BUILDER_PACK_KREDZ)
    )


def test_resubmitted_pack_purchase_creates_no_second_invoice(player_client, store):
    key = probe_key()
    _post_ok(_buy_pack(player_client, STARTER_PACK, key),
             "the first pack purchase with a fresh idempotency key")
    before = _balance(player_client)
    for _ in range(3):
        _buy_pack(player_client, STARTER_PACK, key)
    settle()
    assert store.count_transactions_by_key(key) == 1, (
        "a resubmitted pack purchase produced "
        + str(store.count_transactions_by_key(key)) + " transactions"
    )
    assert _balance(player_client) == before, (
        "a resubmitted pack purchase credited the balance twice"
    )


def test_payout_settles_as_a_ledger_transaction(creator_client, store):
    identity = store.identity_by_email(CREATOR_EMAIL)
    assert identity is not None, CREATOR_EMAIL + " has no identities row"
    response = creator_client.post(
        "/economy/payouts",
        json={"amount_kredz": MINIMUM_PAYOUT_KREDZ, "idempotency_key": probe_key()},
    )
    assert response.status_code in OK_STATUSES + REFUSED_STATUSES, (
        "a payout request answered " + str(response.status_code)
        + " body " + body_excerpt(response)
    )
    if response.status_code in OK_STATUSES:
        rows = poll_until(lambda: store.transactions_of_type("creator_payout"))
        assert rows, "a settled payout wrote no creator_payout transaction"
        entries = store.entries_for(rows[-1].get("id"))
        assert store.sum_entries(entries) == 0, (
            "the entries of a creator_payout transaction sum to "
            + str(store.sum_entries(entries))
        )
    else:
        assert store.payout_requests_for(identity.get("id")) is not None, (
            "a refused payout left no payout_requests row to explain the refusal"
        )


def test_pack_receipt_email_reaches_the_buyer(player_client, inbox):
    _post_ok(_buy_pack(player_client, BUILDER_PACK, probe_key()),
             "POST /api/economy/purchases for " + BUILDER_PACK)
    message = wait_for_email(inbox, PLAYER_EMAIL, RECEIPT_SUBJECT_PREFIX)
    assert message is not None, (
        "no message with subject prefix " + RECEIPT_SUBJECT_PREFIX
        + " reached " + PLAYER_EMAIL + " after buying " + BUILDER_PACK_NAME
    )
    assert message.subject.startswith(RECEIPT_SUBJECT_PREFIX), (
        "the receipt subject is " + message.subject + ", expected it to open "
        + RECEIPT_SUBJECT_PREFIX
    )
    assert BUILDER_PACK_NAME in message.subject, (
        "the receipt subject names no pack: " + message.subject
    )
    assert len(message.to) == 1, (
        "the receipt went to " + str(message.to) + ", expected the buyer alone with no cc"
    )


def test_item_purchase_sends_no_confirmation_mail(player_client, inbox):
    before = inbox.count(PLAYER_EMAIL)
    _post_ok(_buy_item(player_client, MERIDIAN_BANNER, probe_key()),
             "POST /api/economy/items/" + MERIDIAN_BANNER + "/purchase")
    settle()
    after = inbox.count(PLAYER_EMAIL)
    assert after == before, (
        "an item purchase sent mail: the inbox for " + PLAYER_EMAIL
        + " moved from " + str(before) + " to " + str(after)
    )


def test_refused_pack_purchase_sends_no_mail(player_client, inbox):
    before = inbox.count(PLAYER_EMAIL)
    response = _buy_pack(player_client, "no-such-pack", probe_key())
    _refused(response, "buying a pack code that does not exist")
    settle()
    assert inbox.count(PLAYER_EMAIL) == before, (
        "a refused pack purchase still sent mail to " + PLAYER_EMAIL
    )
