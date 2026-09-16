from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor

import httpx
from _shapes import flatten, items
from appclient import client
from conftest import (
    AREA_ONE,
    AREA_TWO,
    AUDITOR_EMAIL,
    CLEAN_LOADING,
    CODE_ALARM_ALREADY_ACKNOWLEDGED,
    CODE_CONFIRMATION_REQUIRED,
    CODE_COMMAND_VERSION_CONFLICT,
    CODE_LEASE_HELD,
    CODE_OUT_OF_AREA,
    CODE_SAFETY_DOCUMENT_CONFLICT,
    CODE_SAFETY_VALIDATION_FAILED,
    CODE_SELF_APPROVAL_DENIED,
    CODE_STEP_OUT_OF_ORDER,
    CODE_SUPPRESSION_BLOCKED,
    CODE_UNDISPOSITIONED_ITEMS,
    CODE_VERSION_CONFLICT,
    CONTROLLER_EMAIL,
    COORDINATOR_EMAIL,
    CREATED,
    CREW_ONE,
    CURRENCY,
    DENIED,
    DENIED_OR_MISSING,
    ESTIMATED_COST_MINOR,
    FAR_CONDUCTOR_KEY,
    HARBOURSIDE_CONDUCTOR_KEY,
    IMPACT_MAX,
    IMPACT_MIN,
    INCIDENT_REFERENCE,
    ISOLATED_CONDUCTOR_KEY,
    OPERATOR_EMAIL,
    ORDER_REFERENCE,
    OVERLOADED_LOADING,
    PUBLISHED_TRAIN,
    READY_TRAIN,
    RECLOSER_KEY,
    REFUSED,
    SEEDED_ALARM_PRIORITY,
    SEEDED_PASSWORD_DEFAULT,
    SECTIONALIZER_KEY,
    SENSITIVE_COUNT,
    SUPPRESSION_MAX_SECONDS,
    TIE_KEY,
    VERIFY_WINDOW_DAYS,
    VIOLATION_KIND,
    add_step,
    alarm_id_of,
    alarm_list,
    api,
    approve,
    approved_hash_of,
    confirm_token,
    error_code,
    execute_step,
    new_order,
    order_body,
    page,
    probe_suffix,
    reference_of,
    run_study,
    seeded_alarm,
    settle,
    step_id_of,
    submit,
    token_for,
)

def test_health_endpoint_reports_ready():
    response = httpx.get(api("/health"), timeout=30.0)
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:400]}"
    )


def test_operator_login_returns_access_token(operator_token, db):
    assert isinstance(operator_token, str) and operator_token.strip(), (
        f"login for {OPERATOR_EMAIL} returned no usable access_token: {operator_token!r}"
    )
    row = db.user_row(OPERATOR_EMAIL)
    assert row is not None, (
        f"the seeded account {OPERATOR_EMAIL} has no row in app_user, so the seed "
        f"never ran or the table carries a different name"
    )
    assert SEEDED_PASSWORD_DEFAULT not in flatten(row), (
        f"the app_user row for {OPERATOR_EMAIL} carries the seeded password, so the "
        f"product stores a credential the identity provider owns"
    )


def test_login_with_wrong_password_is_rejected():
    response = httpx.post(
        api("/auth/login"),
        json={"email": OPERATOR_EMAIL, "password": "not-the-seeded-password"},
        timeout=30.0,
    )
    assert response.status_code in DENIED, (
        f"POST /api/auth/login with a wrong password returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}"
    )
    assert "access_token" not in response.text, (
        f"a rejected sign-in returned a token: {response.text[:400]}"
    )


def test_signup_route_does_not_exist():
    for path in ("/auth/signup", "/auth/register", "/v1/users"):
        response = httpx.post(api(path), json={"email": f"probe-{probe_suffix()}@example.com"}, timeout=30.0)
        assert response.status_code not in CREATED, (
            f"POST /api{path} returned {response.status_code}, so an account can be "
            f"created from inside the product: {response.text[:400]}"
        )


def test_malformed_token_is_denied():
    with client("not-a-real-token") as bad:
        response = bad.get("/v1/me")
    assert response.status_code in DENIED, (
        f"GET /api/v1/me with a malformed token returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}"
    )


def test_seeded_model_version_is_the_only_published_one(operator_client, db):
    assert db.count_published_versions() == 1, (
        f"model_version holds {db.count_published_versions()} rows in state "
        f"'published', and exactly one version is published at a time"
    )
    published = db.published_version()
    assert published is not None, "no model_version row is in state 'published'"
    assert int(published["train"]) == PUBLISHED_TRAIN, (
        f"the published model version is train {published['train']}, expected "
        f"{PUBLISHED_TRAIN}"
    )
    ready = db.version_by_train(READY_TRAIN)
    assert ready is not None, f"train {READY_TRAIN} has no model_version row"
    assert str(ready["state"]) == "ready", (
        f"train {READY_TRAIN} is in state {ready['state']!r}, expected 'ready'"
    )


def test_seeded_network_elements_match_the_published_train(operator_client, db):
    for key in (RECLOSER_KEY, SECTIONALIZER_KEY, TIE_KEY, ISOLATED_CONDUCTOR_KEY,
                FAR_CONDUCTOR_KEY, HARBOURSIDE_CONDUCTOR_KEY):
        row = db.element_by_key(key)
        assert row is not None, (
            f"network_element has no row with stable_key {key!r}, so the seed never ran"
        )
    response = operator_client.get("/v1/elements")
    assert response.status_code == 200, (
        f"GET /api/v1/elements returned {response.status_code}: {response.text[:400]}"
    )
    served = flatten(response.json())
    for key in (RECLOSER_KEY, SECTIONALIZER_KEY, TIE_KEY):
        assert key.lower() in served, (
            f"GET /api/v1/elements omits {key!r}, so the published model is not served"
        )


def test_alarm_list_orders_by_computed_priority(operator_client):
    rows = alarm_list(operator_client)
    assert rows, "GET /api/v1/alarms returned no active alarm, so the seed never ran"
    values = []
    for row in rows:
        value = row.get("computed_priority")
        assert value is not None, (
            f"an alarm carries no computed_priority field: {str(row)[:300]}"
        )
        values.append(int(value))
    assert values == sorted(values, reverse=True), (
        f"GET /api/v1/alarms returned computed_priority values {values}, which are not "
        f"in descending order"
    )


def test_seeded_alarm_priority_matches_the_pinned_value(operator_client):
    alarm = seeded_alarm(operator_client)
    assert int(alarm["computed_priority"]) == SEEDED_ALARM_PRIORITY, (
        f"the seeded alarm on {RECLOSER_KEY} carries computed_priority "
        f"{alarm['computed_priority']}, expected {SEEDED_ALARM_PRIORITY}"
    )


def test_alarm_acknowledge_is_recorded_once(operator_client, db):
    alarm = seeded_alarm(operator_client)
    alarm_id = alarm_id_of(alarm)
    before = db.count_audit()
    first = operator_client.post(f"/v1/alarms/{alarm_id}/acknowledge", json={})
    assert first.status_code in CREATED, (
        f"acknowledging alarm {alarm_id} returned {first.status_code}: "
        f"{first.text[:400]}"
    )
    second = operator_client.post(f"/v1/alarms/{alarm_id}/acknowledge", json={})
    assert second.status_code in REFUSED, (
        f"acknowledging alarm {alarm_id} a second time returned {second.status_code}, "
        f"expected a refusal: {second.text[:400]}"
    )
    assert error_code(second) == CODE_ALARM_ALREADY_ACKNOWLEDGED, (
        f"the second acknowledgement returned code {error_code(second)!r}, expected "
        f"{CODE_ALARM_ALREADY_ACKNOWLEDGED!r}: {second.text[:400]}"
    )
    after = db.count_audit()
    assert after - before == 1, (
        f"two acknowledgements of alarm {alarm_id} wrote {after - before} record "
        f"entries, expected exactly 1"
    )


def test_suppression_reason_below_the_floor_is_refused(operator_client):
    alarm = seeded_alarm(operator_client)
    response = operator_client.post(
        f"/v1/alarms/{alarm_id_of(alarm)}/suppress",
        json={"reason": "short", "duration_s": 600},
    )
    assert response.status_code in REFUSED, (
        f"suppressing with a five-character reason returned {response.status_code}, "
        f"expected a refusal: {response.text[:400]}"
    )


def test_suppression_duration_above_the_cap_is_refused(operator_client):
    alarm = seeded_alarm(operator_client)
    response = operator_client.post(
        f"/v1/alarms/{alarm_id_of(alarm)}/suppress",
        json={"reason": "field crew on site", "duration_s": SUPPRESSION_MAX_SECONDS + 1},
    )
    assert response.status_code in REFUSED, (
        f"suppressing for {SUPPRESSION_MAX_SECONDS + 1} seconds returned "
        f"{response.status_code}, expected a refusal: {response.text[:400]}"
    )


def test_incident_command_assume_with_stale_version_is_refused(coordinator_client, db):
    row = db.incident_row(INCIDENT_REFERENCE)
    assert row is not None, (
        f"incident {INCIDENT_REFERENCE} has no row, so the seed never ran"
    )
    current = int(row.get("command_version", 0))
    response = coordinator_client.post(
        f"/v1/incidents/{INCIDENT_REFERENCE}/command",
        json={"expected_command_version": current + 99},
    )
    assert response.status_code in REFUSED, (
        f"assuming command with a stale version returned {response.status_code}, "
        f"expected a refusal: {response.text[:400]}"
    )
    assert error_code(response) == CODE_COMMAND_VERSION_CONFLICT, (
        f"the stale assume returned code {error_code(response)!r}, expected "
        f"{CODE_COMMAND_VERSION_CONFLICT!r}: {response.text[:400]}"
    )


def test_incident_timeline_sequence_is_gapless(coordinator_client, db):
    for n in range(2):
        response = coordinator_client.post(
            f"/v1/incidents/{INCIDENT_REFERENCE}/timeline",
            json={"kind": "note", "body": f"probe note {probe_suffix()} {n}"},
        )
        assert response.status_code in CREATED, (
            f"posting a timeline note returned {response.status_code}: "
            f"{response.text[:400]}"
        )
    row = db.incident_row(INCIDENT_REFERENCE)
    entries = db.timeline_for(row["id"])
    sequences = sorted(int(e["sequence"]) for e in entries)
    assert sequences == list(range(sequences[0], sequences[0] + len(sequences))), (
        f"incident_timeline_entry sequences {sequences} are not gapless within "
        f"{INCIDENT_REFERENCE}"
    )


def test_order_study_returns_per_step_predicted_results(operator_client):
    reference = reference_of(new_order(operator_client))
    for key, action in ((SECTIONALIZER_KEY, "open"), (TIE_KEY, "close")):
        created = add_step(operator_client, reference, key, action)
        assert created.status_code in CREATED, (
            f"adding the {action} step on {key} returned {created.status_code}: "
            f"{created.text[:400]}"
        )
    study = run_study(operator_client, reference)
    assert study.status_code in CREATED, (
        f"running the study on {reference} returned {study.status_code}: "
        f"{study.text[:400]}"
    )
    text = flatten(study.json())
    assert "loading" in text, (
        f"the study result carries no per-conductor loading: {study.text[:600]}"
    )


def test_study_flags_the_overloaded_transfer_as_a_thermal_violation(operator_client):
    reference = reference_of(new_order(operator_client))
    created = add_step(operator_client, reference, TIE_KEY, "close")
    assert created.status_code in CREATED, (
        f"adding the close step on {TIE_KEY} returned {created.status_code}: "
        f"{created.text[:400]}"
    )
    study = run_study(operator_client, reference)
    assert study.status_code in CREATED, (
        f"running the study returned {study.status_code}: {study.text[:400]}"
    )
    text = flatten(study.json())
    assert OVERLOADED_LOADING in text, (
        f"closing {TIE_KEY} with {SECTIONALIZER_KEY} closed should load "
        f"{HARBOURSIDE_CONDUCTOR_KEY} to {OVERLOADED_LOADING}; the study returned "
        f"{study.text[:600]}"
    )
    assert VIOLATION_KIND in text, (
        f"the overloaded transfer produced no {VIOLATION_KIND!r} violation: "
        f"{study.text[:600]}"
    )


def test_study_clears_when_the_sectionalizer_opens_first(operator_client):
    reference = reference_of(new_order(operator_client))
    for key, action in ((SECTIONALIZER_KEY, "open"), (TIE_KEY, "close")):
        created = add_step(operator_client, reference, key, action)
        assert created.status_code in CREATED, (
            f"adding the {action} step on {key} returned {created.status_code}: "
            f"{created.text[:400]}"
        )
    study = run_study(operator_client, reference)
    assert study.status_code in CREATED, (
        f"running the study returned {study.status_code}: {study.text[:400]}"
    )
    text = flatten(study.json())
    assert CLEAN_LOADING in text, (
        f"opening {SECTIONALIZER_KEY} before closing {TIE_KEY} should load "
        f"{HARBOURSIDE_CONDUCTOR_KEY} to {CLEAN_LOADING}; the study returned "
        f"{study.text[:600]}"
    )


def test_study_is_deterministic_across_runs(operator_client):
    reference = reference_of(new_order(operator_client))
    created = add_step(operator_client, reference, TIE_KEY, "close")
    assert created.status_code in CREATED, (
        f"adding the close step returned {created.status_code}: {created.text[:400]}"
    )
    first = run_study(operator_client, reference)
    second = run_study(operator_client, reference)
    assert first.status_code in CREATED and second.status_code in CREATED, (
        f"the two study runs returned {first.status_code} and {second.status_code}"
    )
    keep = re.compile(r"\d+\.\d{3}")
    assert keep.findall(flatten(first.json())) == keep.findall(flatten(second.json())), (
        f"two studies of the same order against the same pinned version returned "
        f"different loadings: {first.text[:400]} versus {second.text[:400]}"
    )


def test_submit_moves_the_order_to_pending_approval(operator_client):
    reference = reference_of(new_order(operator_client))
    add_step(operator_client, reference, SECTIONALIZER_KEY, "open")
    run_study(operator_client, reference)
    response = submit(operator_client, reference)
    assert response.status_code in CREATED, (
        f"submitting {reference} returned {response.status_code}: {response.text[:400]}"
    )
    assert str(order_body(operator_client, reference)["state"]) == "pending_approval", (
        f"{reference} is in state "
        f"{order_body(operator_client, reference)['state']!r} after submit, expected "
        f"'pending_approval'"
    )


def test_coordinator_approval_binds_the_step_sequence_digest(
    operator_client, coordinator_client, db
):
    reference = reference_of(new_order(operator_client))
    add_step(operator_client, reference, SECTIONALIZER_KEY, "open")
    run_study(operator_client, reference)
    submit(operator_client, reference)
    body = order_body(operator_client, reference)
    response = approve(coordinator_client, reference, approved_hash_of(body))
    assert response.status_code in CREATED, (
        f"approving {reference} returned {response.status_code}: {response.text[:400]}"
    )
    after = order_body(operator_client, reference)
    assert str(after["state"]) == "approved", (
        f"{reference} is in state {after['state']!r} after approval, expected 'approved'"
    )
    row = db.order_row(reference)
    assert row is not None and row.get("approved_hash"), (
        f"the switching_order row for {reference} carries no approved_hash"
    )
    assert str(row["approved_hash"]) == str(row["step_sequence_hash"]), (
        f"approved_hash {row['approved_hash']!r} differs from step_sequence_hash "
        f"{row['step_sequence_hash']!r} on an approved order"
    )


def test_editing_an_approved_order_voids_the_approval(
    operator_client, coordinator_client, db
):
    reference = reference_of(new_order(operator_client))
    add_step(operator_client, reference, SECTIONALIZER_KEY, "open")
    run_study(operator_client, reference)
    submit(operator_client, reference)
    approve(coordinator_client, reference, approved_hash_of(order_body(operator_client, reference)))
    added = add_step(operator_client, reference, TIE_KEY, "close")
    assert added.status_code in CREATED, (
        f"editing an approved order returned {added.status_code}, and an edit is "
        f"permitted because it voids the approval: {added.text[:400]}"
    )
    after = order_body(operator_client, reference)
    assert str(after["state"]) == "draft", (
        f"{reference} is in state {after['state']!r} after an edit, expected 'draft'"
    )
    row = db.order_row(reference)
    assert not row.get("approved_hash"), (
        f"the switching_order row for {reference} still carries approved_hash "
        f"{row.get('approved_hash')!r} after an edit voided the approval"
    )


def test_execute_without_a_confirmation_token_is_refused(
    operator_client, coordinator_client, db
):
    reference = reference_of(new_order(operator_client))
    created = add_step(operator_client, reference, SECTIONALIZER_KEY, "open")
    step_id = step_id_of(created.json())
    run_study(operator_client, reference)
    submit(operator_client, reference)
    approve(coordinator_client, reference, approved_hash_of(order_body(operator_client, reference)))
    response = execute_step(operator_client, reference, step_id, None)
    assert response.status_code in REFUSED, (
        f"executing without a confirmation token returned {response.status_code}, "
        f"expected a refusal: {response.text[:400]}"
    )
    assert error_code(response) == CODE_CONFIRMATION_REQUIRED, (
        f"the refusal returned code {error_code(response)!r}, expected "
        f"{CODE_CONFIRMATION_REQUIRED!r}: {response.text[:400]}"
    )
    assert db.count_attempts(step_id) == 0, (
        f"a refused execution wrote {db.count_attempts(step_id)} execution attempts "
        f"for step {step_id}, expected 0"
    )


def test_execute_with_a_spent_confirmation_token_is_refused(
    operator_client, coordinator_client
):
    reference = reference_of(new_order(operator_client))
    created = add_step(operator_client, reference, SECTIONALIZER_KEY, "open")
    step_id = step_id_of(created.json())
    run_study(operator_client, reference)
    submit(operator_client, reference)
    approve(coordinator_client, reference, approved_hash_of(order_body(operator_client, reference)))
    token = confirm_token(operator_client, reference, step_id)
    first = execute_step(operator_client, reference, step_id, token)
    assert first.status_code in CREATED, (
        f"the first execution returned {first.status_code}: {first.text[:400]}"
    )
    second = execute_step(operator_client, reference, step_id, token)
    assert second.status_code in REFUSED or second.status_code in CREATED, (
        f"re-using a spent confirmation token returned {second.status_code}: "
        f"{second.text[:400]}"
    )
    if second.status_code in REFUSED:
        assert error_code(second) == CODE_CONFIRMATION_REQUIRED, (
            f"the refusal returned code {error_code(second)!r}, expected "
            f"{CODE_CONFIRMATION_REQUIRED!r}: {second.text[:400]}"
        )


def test_step_out_of_order_execution_is_refused(operator_client, coordinator_client):
    reference = reference_of(new_order(operator_client))
    first_step = add_step(operator_client, reference, SECTIONALIZER_KEY, "open")
    second_step = add_step(operator_client, reference, TIE_KEY, "close")
    assert second_step.status_code in CREATED, (
        f"adding the second step returned {second_step.status_code}: "
        f"{second_step.text[:400]}"
    )
    run_study(operator_client, reference)
    submit(operator_client, reference)
    approve(coordinator_client, reference, approved_hash_of(order_body(operator_client, reference)))
    later_id = step_id_of(second_step.json())
    token = confirm_token(operator_client, reference, later_id)
    response = execute_step(operator_client, reference, later_id, token)
    assert response.status_code in REFUSED, (
        f"executing step two before step one returned {response.status_code}, "
        f"expected a refusal: {response.text[:400]}"
    )
    assert error_code(response) == CODE_STEP_OUT_OF_ORDER, (
        f"the refusal returned code {error_code(response)!r}, expected "
        f"{CODE_STEP_OUT_OF_ORDER!r}: {response.text[:400]}"
    )
    assert step_id_of(first_step.json()) is not None


def test_permit_validation_names_the_indeterminate_device(coordinator_client):
    response = coordinator_client.post(
        "/v1/safety-documents/validate",
        json={
            "order_reference": ORDER_REFERENCE,
            "isolated_element_keys": [ISOLATED_CONDUCTOR_KEY],
            "isolating_device_keys": [RECLOSER_KEY, SECTIONALIZER_KEY],
        },
    )
    assert response.status_code == 200, (
        f"POST /api/v1/safety-documents/validate returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    body = response.json()
    body = body.get("data", body) if isinstance(body.get("data"), dict) else body
    assert body.get("valid") is False, (
        f"validation over {ISOLATED_CONDUCTOR_KEY} reported valid={body.get('valid')!r}, "
        f"and {SECTIONALIZER_KEY} reports an indeterminate position quality"
    )
    assert SECTIONALIZER_KEY.lower() in flatten(body), (
        f"the failed validation does not name {SECTIONALIZER_KEY}: "
        f"{response.text[:600]}"
    )
    assert "indeterminate" in flatten(body), (
        f"the failed validation does not name the quality that failed it: "
        f"{response.text[:600]}"
    )


def test_permit_issue_without_validation_is_refused(coordinator_client, db):
    before = len(db.permit_rows())
    response = coordinator_client.post(
        "/v1/safety-documents",
        json={
            "order_reference": ORDER_REFERENCE,
            "crew_call_sign": CREW_ONE,
            "isolated_element_keys": [ISOLATED_CONDUCTOR_KEY],
            "isolating_device_keys": [RECLOSER_KEY, SECTIONALIZER_KEY],
        },
    )
    assert response.status_code in REFUSED, (
        f"issuing a permit whose validation fails returned {response.status_code}, "
        f"expected a refusal: {response.text[:400]}"
    )
    assert error_code(response) == CODE_SAFETY_VALIDATION_FAILED, (
        f"the refusal returned code {error_code(response)!r}, expected "
        f"{CODE_SAFETY_VALIDATION_FAILED!r}: {response.text[:400]}"
    )
    assert len(db.permit_rows()) == before, (
        f"a refused permit issue created a safety_document row"
    )


def test_permit_blocks_a_re_energizing_step_at_authoring_time(
    operator_client, coordinator_client, db
):
    live = [p for p in db.permit_rows() if str(p.get("state")) == "live"]
    if not live:
        override = operator_client.post(
            f"/v1/elements/{SECTIONALIZER_KEY}/position-override",
            json={
                "asserted_position": "open",
                "reason": "field verification by the attending crew lead",
                "field_reference": f"FV-{probe_suffix()}",
            },
        )
        assert override.status_code in CREATED, (
            f"recording a manual position override returned {override.status_code}: "
            f"{override.text[:400]}"
        )
        issued = coordinator_client.post(
            "/v1/safety-documents",
            json={
                "order_reference": ORDER_REFERENCE,
                "crew_call_sign": CREW_ONE,
                "isolated_element_keys": [ISOLATED_CONDUCTOR_KEY],
                "isolating_device_keys": [RECLOSER_KEY, SECTIONALIZER_KEY],
            },
        )
        assert issued.status_code in CREATED, (
            f"issuing a permit after a passing validation returned "
            f"{issued.status_code}: {issued.text[:400]}"
        )
    reference = reference_of(new_order(operator_client))
    response = add_step(operator_client, reference, RECLOSER_KEY, "close")
    assert response.status_code in REFUSED, (
        f"adding a step that would energize an element under a live permit returned "
        f"{response.status_code}, expected a refusal at authoring time: "
        f"{response.text[:400]}"
    )
    assert error_code(response) == CODE_SAFETY_DOCUMENT_CONFLICT, (
        f"the refusal returned code {error_code(response)!r}, expected "
        f"{CODE_SAFETY_DOCUMENT_CONFLICT!r}: {response.text[:400]}"
    )


def test_permit_release_without_all_clear_is_refused(coordinator_client, db):
    live = [p for p in db.permit_rows() if str(p.get("state")) == "live"]
    assert live, (
        "no safety_document row is in state 'live', so the permit path never ran"
    )
    reference = str(live[0].get("reference"))
    response = coordinator_client.post(
        f"/v1/safety-documents/{reference}/release",
        json={"all_clear_confirmed": False, "confirmed_by": "the dispatcher"},
    )
    assert response.status_code in REFUSED, (
        f"releasing permit {reference} without the all-clear returned "
        f"{response.status_code}, expected a refusal: {response.text[:400]}"
    )
    after = [p for p in db.permit_rows() if str(p.get("reference")) == reference]
    assert after and str(after[0].get("state")) == "live", (
        f"permit {reference} left state 'live' on a refused release"
    )


def test_handover_submit_with_an_undispositioned_item_is_refused(operator_client):
    created = operator_client.post(
        "/v1/handovers",
        json={"incoming_email": OPERATOR_EMAIL, "shift_ends_at": "2026-09-17T06:00:00Z"},
    )
    assert created.status_code in CREATED, (
        f"opening a handover returned {created.status_code}: {created.text[:400]}"
    )
    body = created.json()
    body = body.get("data", body) if isinstance(body.get("data"), dict) else body
    handover_id = body.get("id") or body.get("handover_id")
    assert handover_id, f"the handover carries no id: {created.text[:400]}"
    response = operator_client.post(f"/v1/handovers/{handover_id}/submit", json={})
    assert response.status_code in REFUSED, (
        f"submitting a handover holding an undispositioned item returned "
        f"{response.status_code}, expected a refusal: {response.text[:400]}"
    )
    assert error_code(response) == CODE_UNDISPOSITIONED_ITEMS, (
        f"the refusal returned code {error_code(response)!r}, expected "
        f"{CODE_UNDISPOSITIONED_ITEMS!r}: {response.text[:400]}"
    )


def test_terms_page_is_reachable_and_linked():
    response = httpx.get(page("/terms"), timeout=30.0, follow_redirects=True)
    assert response.status_code == 200, (
        f"GET /terms returned {response.status_code}: {response.text[:400]}"
    )
    entry = httpx.get(page("/"), timeout=30.0, follow_redirects=True)
    assert "/terms" in entry.text, (
        f"the sign-in entry carries no link to /terms, so the footer link is absent"
    )


def test_cookie_choice_survives_a_reload():
    with httpx.Client(timeout=30.0, follow_redirects=True) as session:
        session.get(page("/"))
        recorded = session.post(
            api("/v1/cookie-choice"), json={"non_essential_accepted": True}
        )
        assert recorded.status_code in CREATED, (
            f"recording the cookie choice returned {recorded.status_code}: "
            f"{recorded.text[:400]}"
        )
        again = session.get(api("/v1/cookie-choice"))
        assert again.status_code == 200, (
            f"reading the cookie choice back returned {again.status_code}: "
            f"{again.text[:400]}"
        )
        assert "true" in flatten(again.json()), (
            f"the recorded cookie choice did not survive a reload: {again.text[:400]}"
        )


def test_unknown_address_answers_not_found():
    response = httpx.get(page(f"/no-such-surface-{probe_suffix()}"), timeout=30.0)
    assert response.status_code == 404, (
        f"an unknown address returned {response.status_code}, expected 404"
    )


def test_credentials_note_and_reserved_directories_exist(operator_client):
    response = operator_client.get("/v1/me")
    assert response.status_code == 200, (
        f"GET /api/v1/me returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    body = body.get("data", body) if isinstance(body.get("data"), dict) else body
    assert str(body.get("email")) == OPERATOR_EMAIL, (
        f"GET /api/v1/me returned email {body.get('email')!r}, expected "
        f"{OPERATOR_EMAIL!r}"
    )
    assert str(body.get("role")) == "operator", (
        f"GET /api/v1/me returned role {body.get('role')!r}, expected 'operator'"
    )
    assert AREA_ONE in flatten(body), (
        f"GET /api/v1/me does not carry the assigned area {AREA_ONE!r}: "
        f"{response.text[:400]}"
    )


def test_operator_cannot_approve_an_order(operator_client, db):
    reference = reference_of(new_order(operator_client))
    add_step(operator_client, reference, SECTIONALIZER_KEY, "open")
    run_study(operator_client, reference)
    submit(operator_client, reference)
    before = order_body(operator_client, reference)
    response = approve(operator_client, reference, approved_hash_of(before))
    assert response.status_code in DENIED, (
        f"an operator approving {reference} returned {response.status_code}, expected "
        f"a denial: {response.text[:400]}"
    )
    after = order_body(operator_client, reference)
    assert str(after["state"]) == "pending_approval", (
        f"{reference} moved to {after['state']!r} on a denied approval"
    )
    row = db.order_row(reference)
    assert not row.get("approved_hash"), (
        f"a denied approval wrote approved_hash {row.get('approved_hash')!r}"
    )
    assert db.approvals_for(row["id"]) == [], (
        f"a denied approval wrote an approval_record row for {reference}"
    )


def test_self_approval_at_risk_class_two_or_above_is_denied(coordinator_client, db):
    reference = reference_of(new_order(coordinator_client))
    add_step(coordinator_client, reference, SECTIONALIZER_KEY, "open")
    add_step(coordinator_client, reference, TIE_KEY, "close")
    run_study(coordinator_client, reference)
    submit(coordinator_client, reference)
    body = order_body(coordinator_client, reference)
    assert int(body.get("risk_class", 0)) >= 2, (
        f"{reference} came back at risk class {body.get('risk_class')!r}; a transfer "
        f"putting thousands of customers at risk is class 2 or above"
    )
    response = approve(coordinator_client, reference, approved_hash_of(body))
    assert response.status_code in DENIED or response.status_code in REFUSED, (
        f"a coordinator approving their own order returned {response.status_code}, "
        f"expected a refusal: {response.text[:400]}"
    )
    assert error_code(response) == CODE_SELF_APPROVAL_DENIED, (
        f"the refusal returned code {error_code(response)!r}, expected "
        f"{CODE_SELF_APPROVAL_DENIED!r}: {response.text[:400]}"
    )
    after = order_body(coordinator_client, reference)
    assert str(after["state"]) == "pending_approval", (
        f"{reference} moved to {after['state']!r} on a refused self-approval"
    )


def test_operator_outside_the_area_is_denied_every_write(operator2_client, db):
    row = db.order_row(ORDER_REFERENCE)
    assert row is not None, f"{ORDER_REFERENCE} has no switching_order row"
    before = len(db.steps_for(row["id"]))
    response = add_step(operator2_client, ORDER_REFERENCE, SECTIONALIZER_KEY, "open")
    assert response.status_code in DENIED, (
        f"an operator assigned to {AREA_TWO} writing to a {AREA_ONE} order returned "
        f"{response.status_code}, expected a denial: {response.text[:400]}"
    )
    assert error_code(response) == CODE_OUT_OF_AREA, (
        f"the denial returned code {error_code(response)!r}, expected "
        f"{CODE_OUT_OF_AREA!r}: {response.text[:400]}"
    )
    assert len(db.steps_for(row["id"])) == before, (
        f"a denied out-of-area write changed the step list of {ORDER_REFERENCE}"
    )


def test_operator_cannot_publish_a_model_version(operator_client, db):
    response = operator_client.post(
        f"/v1/model-versions/{READY_TRAIN}/publish", json={"acknowledged_warnings": []}
    )
    assert response.status_code in DENIED, (
        f"an operator publishing train {READY_TRAIN} returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}"
    )
    assert str(db.version_by_train(READY_TRAIN)["state"]) == "ready", (
        f"train {READY_TRAIN} left state 'ready' on a denied publish"
    )


def test_coordinator_cannot_publish_a_model_version(coordinator_client, db):
    response = coordinator_client.post(
        f"/v1/model-versions/{READY_TRAIN}/publish", json={"acknowledged_warnings": []}
    )
    assert response.status_code in DENIED, (
        f"a coordinator publishing train {READY_TRAIN} returned "
        f"{response.status_code}, expected a denial: {response.text[:400]}"
    )
    assert db.count_published_versions() == 1, (
        f"a denied publish left {db.count_published_versions()} published versions"
    )


def test_auditor_cannot_touch_an_order(auditor_client, db):
    row = db.order_row(ORDER_REFERENCE)
    before = len(db.steps_for(row["id"]))
    response = add_step(auditor_client, ORDER_REFERENCE, SECTIONALIZER_KEY, "open")
    assert response.status_code in DENIED, (
        f"an auditor writing a step returned {response.status_code}, expected a "
        f"denial: {response.text[:400]}"
    )
    assert len(db.steps_for(row["id"])) == before, (
        f"a denied auditor write changed the step list of {ORDER_REFERENCE}"
    )


def test_operator_cannot_read_the_record(operator_client):
    response = operator_client.get("/v1/audit/events")
    assert response.status_code in DENIED, (
        f"an operator reading the record returned {response.status_code}, expected a "
        f"denial: {response.text[:400]}"
    )


def test_no_endpoint_deletes_a_record_entry(auditor_client, controller_client, db):
    rows = db.audit_rows(limit=5)
    assert rows, "audit_event holds no rows, so nothing has been recorded"
    entry_id = rows[0].get("id")
    before = db.count_audit()
    for actor in (auditor_client, controller_client):
        deleted = actor.delete(f"/v1/audit/events/{entry_id}")
        assert deleted.status_code in DENIED_OR_MISSING or deleted.status_code == 405, (
            f"deleting record entry {entry_id} returned {deleted.status_code}, and no "
            f"role may delete one: {deleted.text[:400]}"
        )
    assert db.count_audit() >= before, (
        f"the record lost entries: {before} before, {db.count_audit()} after"
    )


def test_human_session_cannot_write_a_measurement(operator_client, coordinator_client, db):
    before = db.count_samples()
    payload = {
        "samples": [
            {
                "point_stable_key": f"{RECLOSER_KEY}-POS",
                "observed_at": "2026-09-16T08:00:00Z",
                "value": 1,
                "quality": "good",
                "unit": "state",
                "source": "probe",
            }
        ]
    }
    for actor in (operator_client, coordinator_client):
        response = actor.post("/v1/measurements/ingest", json=payload)
        assert response.status_code in DENIED, (
            f"a signed-in human session writing a measurement returned "
            f"{response.status_code}, expected a denial: {response.text[:400]}"
        )
    assert db.count_samples() == before, (
        f"a denied measurement write added rows: {before} before, "
        f"{db.count_samples()} after"
    )


def test_seeded_rows_survive_a_re_read(operator_client, db):
    first = order_body(operator_client, ORDER_REFERENCE)
    settle()
    second = order_body(operator_client, ORDER_REFERENCE)
    assert str(first["state"]) == str(second["state"]), (
        f"{ORDER_REFERENCE} reported state {first['state']!r} then "
        f"{second['state']!r} with nothing between the two reads"
    )
    row = db.order_row(ORDER_REFERENCE)
    assert str(row["state"]) == str(second["state"]), (
        f"the switching_order row says {row['state']!r} while the API says "
        f"{second['state']!r}"
    )
    assert str(row["operating_area_id"]), (
        f"{ORDER_REFERENCE} carries no operating area"
    )


def test_approved_order_digest_equals_the_current_digest(db):
    for row in [db.order_row(ORDER_REFERENCE)]:
        if row and str(row.get("state")) in ("approved", "executing", "completed"):
            assert str(row.get("approved_hash")) == str(row.get("step_sequence_hash")), (
                f"{ORDER_REFERENCE} is in state {row['state']!r} with approved_hash "
                f"{row.get('approved_hash')!r} against step_sequence_hash "
                f"{row.get('step_sequence_hash')!r}"
            )
    assert db.order_row(ORDER_REFERENCE) is not None, (
        f"{ORDER_REFERENCE} has no switching_order row"
    )


def test_step_idempotency_key_exists_at_creation(operator_client, db):
    reference = reference_of(new_order(operator_client))
    created = add_step(operator_client, reference, SECTIONALIZER_KEY, "open")
    assert created.status_code in CREATED, (
        f"adding a step returned {created.status_code}: {created.text[:400]}"
    )
    row = db.order_row(reference)
    steps = db.steps_for(row["id"])
    assert steps, f"{reference} has no switching_step rows after a step was added"
    assert steps[0].get("idempotency_key"), (
        f"the switching_step row carries no idempotency_key at creation: "
        f"{str(steps[0])[:300]}"
    )


def test_record_chain_recomputation_matches_the_expected_root(auditor_client):
    response = auditor_client.post(
        "/v1/audit/verify",
        json={"from": "2026-01-01T00:00:00Z", "to": "2027-01-01T00:00:00Z"},
    )
    assert response.status_code == 200, (
        f"POST /api/v1/audit/verify returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    body = response.json()
    body = body.get("data", body) if isinstance(body.get("data"), dict) else body
    assert body.get("verified") is True, (
        f"the chain recomputation reported verified={body.get('verified')!r} with "
        f"first_divergent_sequence={body.get('first_divergent_sequence')!r}"
    )
    assert str(body.get("computed_root")) == str(body.get("expected_root")), (
        f"computed_root {body.get('computed_root')!r} differs from expected_root "
        f"{body.get('expected_root')!r}"
    )
    assert int(body.get("entry_count", 0)) > 0, (
        f"the recomputation covered {body.get('entry_count')!r} entries"
    )


def test_seeding_is_idempotent(db):
    assert db.count_published_versions() == 1, (
        f"model_version holds {db.count_published_versions()} published rows, so the "
        f"seed ran more than once"
    )
    for key in (RECLOSER_KEY, SECTIONALIZER_KEY, TIE_KEY):
        row = db.element_by_key(key)
        assert row is not None, f"network_element has no row for {key!r}"
    assert db.crew_row(CREW_ONE) is not None, (
        f"crew has no row for {CREW_ONE!r}, so the seed never ran"
    )
    assert db.incident_row(INCIDENT_REFERENCE) is not None, (
        f"incident has no row for {INCIDENT_REFERENCE!r}"
    )


def test_impact_snapshot_keeps_the_range_while_estimating(coordinator_client, db):
    row = db.incident_row(INCIDENT_REFERENCE)
    assert row is not None, f"{INCIDENT_REFERENCE} has no incident row"
    response = coordinator_client.get(f"/v1/incidents/{INCIDENT_REFERENCE}")
    assert response.status_code == 200, (
        f"GET /api/v1/incidents/{INCIDENT_REFERENCE} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    text = flatten(response.json())
    assert str(IMPACT_MIN) in text and str(IMPACT_MAX) in text, (
        f"the impact snapshot does not carry the range {IMPACT_MIN} to {IMPACT_MAX}: "
        f"{response.text[:600]}"
    )
    assert str(SENSITIVE_COUNT) in text, (
        f"the impact snapshot does not carry the sensitive register count "
        f"{SENSITIVE_COUNT}: {response.text[:600]}"
    )
    assert str(ESTIMATED_COST_MINOR) in text and CURRENCY in text, (
        f"the impact snapshot does not carry {ESTIMATED_COST_MINOR} in {CURRENCY}: "
        f"{response.text[:600]}"
    )


def test_measurement_without_quality_is_rejected(db):
    before = db.count_samples()
    response = httpx.post(
        api("/v1/measurements/ingest"),
        json={
            "samples": [
                {
                    "point_stable_key": f"{RECLOSER_KEY}-POS",
                    "observed_at": "2026-09-16T08:00:00Z",
                    "value": 1,
                    "unit": "state",
                    "source": "probe",
                }
            ]
        },
        timeout=30.0,
    )
    assert response.status_code not in (200, 201), (
        f"ingesting a sample with no quality flag returned {response.status_code}, "
        f"expected a rejection: {response.text[:400]}"
    )
    assert db.count_samples() == before, (
        f"a rejected sample was stored: {before} rows before, {db.count_samples()} after"
    )


def test_measurement_with_a_mismatched_unit_is_rejected(db):
    before = db.count_samples()
    response = httpx.post(
        api("/v1/measurements/ingest"),
        json={
            "samples": [
                {
                    "point_stable_key": f"{HARBOURSIDE_CONDUCTOR_KEY}-I",
                    "observed_at": "2026-09-16T08:00:00Z",
                    "value": 118.0,
                    "unit": "kV",
                    "quality": "good",
                    "source": "probe",
                }
            ]
        },
        timeout=30.0,
    )
    assert response.status_code not in (200, 201), (
        f"ingesting a current reading declared in kV returned {response.status_code}, "
        f"expected a rejection: {response.text[:400]}"
    )
    assert db.count_samples() == before, (
        f"a unit-mismatched sample was stored: {before} before, "
        f"{db.count_samples()} after"
    )


def test_concurrent_execute_emits_exactly_one_instruction(
    operator_client, coordinator_client, operator_token, db
):
    reference = reference_of(new_order(operator_client))
    created = add_step(operator_client, reference, SECTIONALIZER_KEY, "open")
    step_id = step_id_of(created.json())
    run_study(operator_client, reference)
    submit(operator_client, reference)
    approve(coordinator_client, reference, approved_hash_of(order_body(operator_client, reference)))
    token_a = confirm_token(operator_client, reference, step_id)
    token_b = confirm_token(operator_client, reference, step_id)

    def fire(token: str):
        with client(operator_token) as c:
            return execute_step(c, reference, step_id, token)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = [f.result() for f in [pool.submit(fire, token_a), pool.submit(fire, token_b)]]
    accepted = [r for r in results if r.status_code in CREATED]
    assert accepted, (
        f"neither concurrent execution was accepted: "
        f"{[(r.status_code, r.text[:120]) for r in results]}"
    )
    settle()
    assert db.count_attempts(step_id) == 1, (
        f"two simultaneous executions of step {step_id} produced "
        f"{db.count_attempts(step_id)} execution attempts, expected exactly 1"
    )


def test_concurrent_approve_records_exactly_one_approval(operator_client, db):
    reference = reference_of(new_order(operator_client))
    add_step(operator_client, reference, SECTIONALIZER_KEY, "open")
    run_study(operator_client, reference)
    submit(operator_client, reference)
    digest = approved_hash_of(order_body(operator_client, reference))
    coordinator = token_for(COORDINATOR_EMAIL)
    controller = token_for(CONTROLLER_EMAIL)

    def fire(token: str):
        with client(token) as c:
            return approve(c, reference, digest)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = [
            f.result()
            for f in [pool.submit(fire, coordinator), pool.submit(fire, controller)]
        ]
    settle()
    row = db.order_row(reference)
    approvals = db.approvals_for(row["id"])
    assert len(approvals) == 1, (
        f"two simultaneous approvals of {reference} wrote {len(approvals)} "
        f"approval_record rows, expected exactly 1"
    )
    losers = [r for r in results if r.status_code in REFUSED]
    if losers:
        assert error_code(losers[0]) == CODE_VERSION_CONFLICT, (
            f"the losing approval returned code {error_code(losers[0])!r}, expected "
            f"{CODE_VERSION_CONFLICT!r}: {losers[0].text[:400]}"
        )


def test_concurrent_crew_assignment_yields_one_holder(db):
    coordinator = token_for(COORDINATOR_EMAIL)
    crew = db.crew_row(CREW_ONE)
    assert crew is not None, f"crew has no row for {CREW_ONE!r}"
    before = db.count_assignments(crew["id"])
    payload = {
        "crew_call_sign": CREW_ONE,
        "incident_reference": INCIDENT_REFERENCE,
        "target_element_key": ISOLATED_CONDUCTOR_KEY,
    }

    def fire():
        with client(coordinator) as c:
            return c.post("/v1/dispatch/assignments", json=payload)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = [f.result() for f in [pool.submit(fire), pool.submit(fire)]]
    settle()
    accepted = [r for r in results if r.status_code in CREATED]
    assert len(accepted) == 1, (
        f"two simultaneous assignments of {CREW_ONE} produced {len(accepted)} "
        f"acceptances, expected exactly 1: "
        f"{[(r.status_code, r.text[:120]) for r in results]}"
    )
    refused = [r for r in results if r.status_code in REFUSED]
    assert refused and error_code(refused[0]) == CODE_LEASE_HELD, (
        f"the losing assignment returned code "
        f"{error_code(refused[0]) if refused else 'nothing'!r}, expected "
        f"{CODE_LEASE_HELD!r}"
    )
    assert db.count_assignments(crew["id"]) == before + 1, (
        f"two simultaneous assignments of {CREW_ONE} wrote "
        f"{db.count_assignments(crew['id']) - before} assignment rows, expected 1"
    )


def test_suppression_blocked_by_a_live_permit(operator_client, db):
    live = [p for p in db.permit_rows() if str(p.get("state")) == "live"]
    assert live, "no safety_document row is in state 'live', so the permit path never ran"
    alarms = [a for a in alarm_list(operator_client) if ISOLATED_CONDUCTOR_KEY in str(a)]
    target = alarms[0] if alarms else seeded_alarm(operator_client)
    response = operator_client.post(
        f"/v1/alarms/{alarm_id_of(target)}/suppress",
        json={"reason": "isolated section under a live permit", "duration_s": 600},
    )
    if response.status_code in REFUSED:
        assert error_code(response) in (CODE_SUPPRESSION_BLOCKED, CODE_OUT_OF_AREA), (
            f"the refusal returned code {error_code(response)!r}, expected "
            f"{CODE_SUPPRESSION_BLOCKED!r}: {response.text[:400]}"
        )
    else:
        assert response.status_code in CREATED, (
            f"suppressing returned {response.status_code}: {response.text[:400]}"
        )


def test_publishing_is_refused_while_an_order_executes(
    operator_client, coordinator_client, controller_client, db
):
    reference = reference_of(new_order(operator_client))
    created = add_step(operator_client, reference, SECTIONALIZER_KEY, "open")
    step_id = step_id_of(created.json())
    run_study(operator_client, reference)
    submit(operator_client, reference)
    approve(coordinator_client, reference, approved_hash_of(order_body(operator_client, reference)))
    token = confirm_token(operator_client, reference, step_id)
    execute_step(operator_client, reference, step_id, token)
    settle()
    approved = coordinator_client.post(
        f"/v1/model-versions/{READY_TRAIN}/approve", json={"comment": "reviewed"}
    )
    assert approved.status_code in CREATED or approved.status_code in REFUSED, (
        f"approving train {READY_TRAIN} returned {approved.status_code}: "
        f"{approved.text[:400]}"
    )
    response = controller_client.post(
        f"/v1/model-versions/{READY_TRAIN}/publish", json={"acknowledged_warnings": []}
    )
    if str(order_body(operator_client, reference)["state"]) == "executing":
        assert response.status_code in REFUSED, (
            f"publishing train {READY_TRAIN} while {reference} is executing returned "
            f"{response.status_code}, expected a refusal: {response.text[:400]}"
        )
        assert reference.lower() in flatten(response.json()), (
            f"the refusal does not name the blocking order {reference}: "
            f"{response.text[:600]}"
        )


def test_decoy_field_submission_is_refused():
    response = httpx.post(
        api("/auth/login"),
        json={
            "email": OPERATOR_EMAIL,
            "password": SEEDED_PASSWORD_DEFAULT,
            "company_website": "https://spam.example.com",
        },
        timeout=30.0,
    )
    assert response.status_code not in (200, 201), (
        f"a sign-in carrying the filled decoy field returned {response.status_code}, "
        f"expected a refusal: {response.text[:400]}"
    )
    assert "access_token" not in response.text, (
        f"a decoy submission returned a token: {response.text[:400]}"
    )


def test_repeated_sign_in_attempts_are_refused():
    statuses = []
    with httpx.Client(timeout=30.0) as session:
        for _ in range(8):
            response = session.post(
                api("/auth/login"),
                json={"email": OPERATOR_EMAIL, "password": "still-not-the-password"},
            )
            statuses.append(response.status_code)
    assert 429 in statuses or statuses[-1] in DENIED, (
        f"eight rapid sign-in attempts returned {statuses}, and a burst from one "
        f"client is refused"
    )


def test_recomputation_window_beyond_the_cap_is_refused(auditor_client):
    response = auditor_client.post(
        "/v1/audit/verify",
        json={"from": "2020-01-01T00:00:00Z", "to": "2027-01-01T00:00:00Z"},
    )
    assert response.status_code in REFUSED, (
        f"a recomputation window longer than {VERIFY_WINDOW_DAYS} days returned "
        f"{response.status_code}, expected a refusal: {response.text[:400]}"
    )


def test_empty_alarm_list_returns_an_empty_array(operator_client):
    response = operator_client.get(
        "/v1/alarms", params={"state": f"no-such-state-{probe_suffix()}"}
    )
    assert response.status_code in (200, 400, 422), (
        f"GET /api/v1/alarms with an unknown state returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    if response.status_code == 200:
        assert items(response.json()) == [], (
            f"a filter matching nothing returned rows: {response.text[:400]}"
        )
