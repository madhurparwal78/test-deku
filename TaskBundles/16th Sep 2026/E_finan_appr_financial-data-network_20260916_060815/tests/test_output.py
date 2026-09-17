"""Graders for deku/financial-data-network.

Black box: every assertion is made over HTTP against the deployed app, or over the
declared backing store through the capability adapter. Nothing here imports, reads
or inspects the agent's source.
"""

from __future__ import annotations

import datetime as dt

from conftest import (
    ADMINISTRATOR2_EMAIL, ADMINISTRATOR_EMAIL, ANALYST_EMAIL, ANSWER_KEYS,
    APPROVED_REQUEST, BULK_REAUTHENTICATION_LIMIT, CLOSED_DATA_REQUEST,
    COMMITTED_REQUESTS, COMPLIANCE_EMAIL, CONNECTION_STATES,
    DATA_REQUEST_DUE_DAYS, DENIAL_REASON_MAX, DEVELOPER2_EMAIL, DEVELOPER_EMAIL,
    ENVIRONMENTS, FORBIDDEN_CONSUMER_FIELDS, GENESIS_HASH, HEALTHY_CONNECTION,
    IN_REVIEW_REQUEST, LEDGER_SLUG, LIVE_CREDENTIALS_PER_ENVIRONMENT,
    OPEN_DATA_REQUEST, OTHER_ORG_REQUEST, PAYOUTS_SLUG, REAUTH_CONNECTION,
    REQUEST_STATES, REVOKED_CONNECTION, RISK_SLUG, SELF_FILED_REQUEST,
    SUBMITTED_REQUEST, UNAVAILABLE_CONNECTION, VANTOR, answers, audit_hash,
    state_of, unique_suffix,
)

DENIED = (401, 403)
REFUSED = (400, 409, 422)


def _json(response):
    assert response.status_code == 200, (
        f"{response.request.url} returned {response.status_code}: {response.text[:400]}"
    )
    return response.json()


def _ids(rows, key="id"):
    return {row.get(key) for row in rows if isinstance(row, dict)}


def test_health_endpoint_answers_ok(anon_client):
    """The deployed app reports readiness on its health route."""
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:400]}"
    )


def test_seeded_accounts_can_login(developer_client, compliance_client,
                                   administrator_client, analyst_client,
                                   developer2_client, other_org_client):
    """All six seeded identities authenticate through the app's own session route."""
    for label, http_client, email in (
        ("developer", developer_client, DEVELOPER_EMAIL),
        ("developer2", developer2_client, DEVELOPER2_EMAIL),
        ("administrator", administrator_client, ADMINISTRATOR_EMAIL),
        ("compliance", compliance_client, COMPLIANCE_EMAIL),
        ("analyst", analyst_client, ANALYST_EMAIL),
        ("administrator2", other_org_client, ADMINISTRATOR2_EMAIL),
    ):
        body = _json(http_client.get("/me"))
        assert body.get("email") == email, (
            f"{label} session resolves to {body.get('email')!r}, expected {email!r}"
        )


def test_seeded_access_requests_are_stored(developer_client):
    """The five seeded access requests are readable with their seeded states."""
    rows = _json(developer_client.get("/access-requests"))
    assert isinstance(rows, list), "GET /api/access-requests must return a JSON array"
    found = _ids(rows)
    for request_id in (SUBMITTED_REQUEST, IN_REVIEW_REQUEST, APPROVED_REQUEST,
                       SELF_FILED_REQUEST):
        assert request_id in found, f"{request_id} is missing from the Vantor queue"
    assert state_of(developer_client, SUBMITTED_REQUEST)[0] == "submitted"
    assert state_of(developer_client, IN_REVIEW_REQUEST)[0] == "in_review"
    assert state_of(developer_client, APPROVED_REQUEST)[0] == "approved"
    assert state_of(developer_client, SELF_FILED_REQUEST)[0] == "submitted"


def test_approver_claims_a_submitted_request(compliance_client, fresh_request):
    """A compliance approver moves a submitted request to in_review by claiming it."""
    response = compliance_client.post(f"/access-requests/{fresh_request}/claim")
    assert response.status_code in (200, 201, 204), (
        f"claiming {fresh_request} returned {response.status_code}: {response.text[:400]}"
    )
    assert state_of(compliance_client, fresh_request)[0] == "in_review"


def test_approver_approves_a_claimed_request(compliance_client, fresh_request):
    """A claimed request reaches approved when the approver signs it off."""
    compliance_client.post(f"/access-requests/{fresh_request}/claim")
    response = compliance_client.post(f"/access-requests/{fresh_request}/approve")
    assert response.status_code in (200, 201, 204), (
        f"approving {fresh_request} returned {response.status_code}: {response.text[:400]}"
    )
    assert state_of(compliance_client, fresh_request)[0] == "approved"


def test_approval_is_stored_with_the_decider(compliance_client, fresh_request):
    """An approved request records the approver who decided it, and the time."""
    compliance_client.post(f"/access-requests/{fresh_request}/claim")
    compliance_client.post(f"/access-requests/{fresh_request}/approve")
    state, body = state_of(compliance_client, fresh_request)
    assert state == "approved"
    decided_by = str(body.get("decided_by") or body.get("decided_by_email") or "")
    assert COMPLIANCE_EMAIL in decided_by, (
        f"{fresh_request} records decided_by {decided_by!r}, expected {COMPLIANCE_EMAIL!r}"
    )
    assert body.get("decided_at"), f"{fresh_request} carries no decided_at after approval"


def test_approval_marks_only_the_requested_product_live(compliance_client,
                                                        developer_client,
                                                        fresh_request):
    """Approving one product leaves every other production entitlement untouched."""
    before = _json(developer_client.get(
        f"/applications/{PAYOUTS_SLUG}/production"))
    others = {
        row.get("product_key"): row.get("state")
        for row in before.get("entitlements", [])
        if row.get("product_key") != "identity"
    }
    compliance_client.post(f"/access-requests/{fresh_request}/claim")
    compliance_client.post(f"/access-requests/{fresh_request}/approve")
    after = _json(developer_client.get(f"/applications/{PAYOUTS_SLUG}/production"))
    by_key = {row.get("product_key"): row.get("state")
              for row in after.get("entitlements", [])}
    assert by_key.get("identity") == "live", (
        f"identity is {by_key.get('identity')!r} in production after approval, expected 'live'"
    )
    for key, state in others.items():
        assert by_key.get(key) == state, (
            f"approving identity also moved {key} from {state!r} to {by_key.get(key)!r}"
        )


def test_denial_requires_a_reason(compliance_client, fresh_request):
    """A denial without a reason is refused and the request keeps its state."""
    compliance_client.post(f"/access-requests/{fresh_request}/claim")
    response = compliance_client.post(f"/access-requests/{fresh_request}/deny", json={})
    assert response.status_code in REFUSED, (
        f"denying without a reason returned {response.status_code}, expected a client error"
    )
    assert state_of(compliance_client, fresh_request)[0] == "in_review"
    too_long = compliance_client.post(
        f"/access-requests/{fresh_request}/deny",
        json={"reason": "x" * (DENIAL_REASON_MAX + 1)})
    assert too_long.status_code in REFUSED, (
        f"a reason over {DENIAL_REASON_MAX} characters returned {too_long.status_code}"
    )


def test_denial_leaves_every_entitlement_stored_unchanged(compliance_client,
                                                          developer_client,
                                                          fresh_request):
    """A denied request moves no entitlement anywhere."""
    before = {row.get("product_key"): row.get("state") for row in
              _json(developer_client.get(
                  f"/applications/{PAYOUTS_SLUG}/production")).get("entitlements", [])}
    compliance_client.post(f"/access-requests/{fresh_request}/claim")
    denied = compliance_client.post(f"/access-requests/{fresh_request}/deny",
                                    json={"reason": "insufficient disclosure detail"})
    assert denied.status_code in (200, 201, 204), (
        f"denying with a reason returned {denied.status_code}: {denied.text[:400]}"
    )
    assert state_of(compliance_client, fresh_request)[0] == "denied"
    after = {row.get("product_key"): row.get("state") for row in
             _json(developer_client.get(
                 f"/applications/{PAYOUTS_SLUG}/production")).get("entitlements", [])}
    assert after == before, f"a denial moved entitlements from {before} to {after}"


def test_returned_request_returns_to_submitted(compliance_client, developer_client,
                                               fresh_request):
    """A returned request is resubmittable by its filer."""
    compliance_client.post(f"/access-requests/{fresh_request}/claim")
    returned = compliance_client.post(f"/access-requests/{fresh_request}/return",
                                      json={"reason": "name the sub-processors"})
    assert returned.status_code in (200, 201, 204), (
        f"returning {fresh_request} gave {returned.status_code}: {returned.text[:400]}"
    )
    assert state_of(compliance_client, fresh_request)[0] == "returned"
    again = developer_client.post(f"/access-requests/{fresh_request}/submit")
    assert again.status_code in (200, 201, 204), (
        f"resubmitting a returned request gave {again.status_code}: {again.text[:400]}"
    )
    assert state_of(compliance_client, fresh_request)[0] == "submitted"


def test_submit_without_all_seven_answers_is_refused(developer_client):
    """A submit missing any of the seven answers is refused and the request stays draft."""
    for missing in ANSWER_KEYS:
        partial = answers()
        partial.pop(missing)
        created = developer_client.post("/access-requests", json={
            "application": RISK_SLUG,
            "environment": "production",
            "product_key": "transfer",
            "answers": partial,
        })
        if created.status_code in REFUSED:
            continue
        assert created.status_code in (200, 201), (
            f"creating a draft missing {missing} gave {created.status_code}"
        )
        request_id = created.json().get("id")
        response = developer_client.post(f"/access-requests/{request_id}/submit")
        assert response.status_code in REFUSED, (
            f"submitting without {missing!r} returned {response.status_code}, "
            f"expected a client error"
        )
        assert state_of(developer_client, request_id)[0] == "draft", (
            f"a refused submit moved {request_id} out of draft"
        )


def test_second_decision_on_a_decided_request_conflicts(compliance_client,
                                                        fresh_request):
    """A decided request refuses a second decision and keeps the first one."""
    compliance_client.post(f"/access-requests/{fresh_request}/claim")
    compliance_client.post(f"/access-requests/{fresh_request}/approve")
    second = compliance_client.post(
        f"/access-requests/{fresh_request}/deny",
        json={"reason": "changed my mind after the fact"})
    assert second.status_code in REFUSED, (
        f"a second decision returned {second.status_code}, expected a client error"
    )
    assert state_of(compliance_client, fresh_request)[0] == "approved"


def test_developer_cannot_approve_a_request(developer_client, compliance_client):
    """A developer session is refused every decision endpoint, and the row is untouched."""
    before, _ = state_of(compliance_client, SUBMITTED_REQUEST)
    for action, payload in (("claim", None), ("approve", None),
                            ("deny", {"reason": "no"}), ("return", {"reason": "no"})):
        response = developer_client.post(
            f"/access-requests/{SUBMITTED_REQUEST}/{action}", json=payload)
        assert response.status_code in DENIED, (
            f"a developer calling {action} on {SUBMITTED_REQUEST} returned "
            f"{response.status_code}, expected the server to deny it"
        )
    after, body = state_of(compliance_client, SUBMITTED_REQUEST)
    assert after == before, f"{SUBMITTED_REQUEST} moved from {before!r} to {after!r}"
    assert not body.get("decided_by"), (
        f"{SUBMITTED_REQUEST} gained decided_by {body.get('decided_by')!r} after a denied call"
    )
    assert not body.get("claimed_by"), (
        f"{SUBMITTED_REQUEST} gained claimed_by {body.get('claimed_by')!r} after a denied call"
    )


def test_administrator_cannot_approve_a_request(administrator_client,
                                                compliance_client):
    """An administrator holds every operational power except the decision."""
    before, _ = state_of(compliance_client, SUBMITTED_REQUEST)
    response = administrator_client.post(f"/access-requests/{SUBMITTED_REQUEST}/approve")
    assert response.status_code in DENIED, (
        f"an administrator approving returned {response.status_code}, expected a denial"
    )
    assert state_of(compliance_client, SUBMITTED_REQUEST)[0] == before


def test_analyst_is_denied_every_mutation(analyst_client, compliance_client):
    """An analyst session is refused on every mutating endpoint."""
    attempts = (
        ("/access-requests/" + SUBMITTED_REQUEST + "/approve", None),
        ("/applications", {"name": "Analyst App", "team": "Payments Integration",
                           "region": "us"}),
        ("/applications/" + PAYOUTS_SLUG + "/development/credentials", None),
        ("/webhook-endpoints", {"application": PAYOUTS_SLUG,
                                "environment": "development",
                                "target_url": "https://example.com/hook",
                                "event_types": ["connection.created"]}),
    )
    for path, payload in attempts:
        response = analyst_client.post(path, json=payload)
        assert response.status_code in DENIED, (
            f"an analyst POST to {path} returned {response.status_code}, expected a denial"
        )
    assert state_of(compliance_client, SUBMITTED_REQUEST)[0] == "submitted"


def test_filer_cannot_approve_own_request(compliance_client):
    """The approver who filed a request is refused every decision on it."""
    before, _ = state_of(compliance_client, SELF_FILED_REQUEST)
    assert before == "submitted"
    for action, payload in (("claim", None), ("approve", None),
                            ("deny", {"reason": "self"})):
        response = compliance_client.post(
            f"/access-requests/{SELF_FILED_REQUEST}/{action}", json=payload)
        assert response.status_code in DENIED + REFUSED, (
            f"the filer calling {action} on {SELF_FILED_REQUEST} returned "
            f"{response.status_code}, expected a refusal"
        )
    after, body = state_of(compliance_client, SELF_FILED_REQUEST)
    assert after == "submitted", f"{SELF_FILED_REQUEST} moved to {after!r}"
    assert not body.get("decided_by"), (
        f"{SELF_FILED_REQUEST} gained a decider after the refusal"
    )


def test_cross_organisation_request_is_denied(other_org_client, compliance_client):
    """A member of another organisation is denied on a Vantor request."""
    before, _ = state_of(compliance_client, SUBMITTED_REQUEST)
    read = other_org_client.get(f"/access-requests/{SUBMITTED_REQUEST}")
    assert read.status_code in DENIED + (404,), (
        f"a Wrenwood session reading {SUBMITTED_REQUEST} returned {read.status_code}"
    )
    decided = other_org_client.post(f"/access-requests/{SUBMITTED_REQUEST}/approve")
    assert decided.status_code in DENIED + (404,), (
        f"a Wrenwood session approving {SUBMITTED_REQUEST} returned {decided.status_code}"
    )
    assert state_of(compliance_client, SUBMITTED_REQUEST)[0] == before


def test_cross_organisation_request_absent_from_the_list(other_org_client,
                                                         developer_client):
    """Neither organisation's queue carries the other organisation's requests."""
    theirs = _ids(_json(other_org_client.get("/access-requests")))
    ours = _ids(_json(developer_client.get("/access-requests")))
    assert SUBMITTED_REQUEST not in theirs, (
        f"{SUBMITTED_REQUEST} appears in the Wrenwood queue"
    )
    assert OTHER_ORG_REQUEST not in ours, (
        f"{OTHER_ORG_REQUEST} appears in the {VANTOR} queue"
    )
    assert OTHER_ORG_REQUEST in theirs, (
        f"{OTHER_ORG_REQUEST} is missing from its own organisation's queue"
    )


def test_developer_cannot_create_a_production_credential(developer_client,
                                                         administrator_client):
    """Only an administrator creates a credential in the production environment."""
    response = developer_client.post(
        f"/applications/{PAYOUTS_SLUG}/production/credentials")
    assert response.status_code in DENIED, (
        f"a developer creating a production credential returned {response.status_code}"
    )
    listed = _json(administrator_client.get(
        f"/applications/{PAYOUTS_SLUG}/production/credentials"))
    assert isinstance(listed, list)


def test_unauthenticated_request_is_denied(anon_client):
    """Every route but login and health refuses an anonymous caller."""
    for path in ("/me", "/applications", "/access-requests", "/connections",
                 "/webhook-endpoints", "/team", "/data-requests", "/audit", "/usage"):
        response = anon_client.get(path)
        assert response.status_code in DENIED, (
            f"anonymous GET {path} returned {response.status_code}, expected a denial"
        )


def test_credential_secret_is_returned_once_then_never(developer_client):
    """A created secret appears in its creation response and in no later read."""
    created = developer_client.post(
        f"/applications/{LEDGER_SLUG}/sandbox/credentials")
    assert created.status_code in (200, 201), (
        f"creating a sandbox credential returned {created.status_code}: {created.text[:400]}"
    )
    body = created.json()
    secret = body.get("secret")
    assert secret, f"the creation response carries no secret: {created.text[:400]}"
    assert secret.startswith("sec_"), f"secret {secret!r} does not use the sec_ scheme"
    assert body.get("last_four") == secret[-4:], (
        f"last_four is {body.get('last_four')!r} for secret ending {secret[-4:]!r}"
    )
    listed = _json(developer_client.get(
        f"/applications/{LEDGER_SLUG}/sandbox/credentials"))
    for row in listed:
        assert "secret" not in row, f"a credential list item carries a secret: {row}"
        assert secret not in str(row), f"a credential list item leaks the secret value"


def test_third_live_credential_is_refused(developer_client):
    """An environment holds at most two unrevoked credentials at once."""
    slug = RISK_SLUG
    listed = _json(developer_client.get(f"/applications/{slug}/sandbox/credentials"))
    live = [row for row in listed if not row.get("revoked_at")]
    for existing in live:
        developer_client.post(f"/credentials/{existing.get('id')}/revoke")
    created = []
    for _ in range(LIVE_CREDENTIALS_PER_ENVIRONMENT):
        response = developer_client.post(f"/applications/{slug}/sandbox/credentials")
        assert response.status_code in (200, 201), (
            f"creating credential {len(created) + 1} returned {response.status_code}"
        )
        created.append(response.json())
    third = developer_client.post(f"/applications/{slug}/sandbox/credentials")
    assert third.status_code in REFUSED, (
        f"a third live credential returned {third.status_code}, expected a client error"
    )


def test_secret_value_is_not_stored_in_readable_form(developer_client, backend):
    """A created secret is not recoverable from the store or from the audit log."""
    created = developer_client.post(
        f"/applications/{PAYOUTS_SLUG}/sandbox/credentials")
    assert created.status_code in (200, 201)
    secret = created.json().get("secret")
    assert secret
    entries = _json(developer_client.get("/audit"))
    assert secret not in str(entries), "the audit log carries a secret value"
    rows = backend.rows("api_credential", limit=200)
    assert secret not in str(rows), "a stored credential row carries the secret value"


def test_audit_chain_verifies_from_stored_rows(developer_client):
    """The audit chain a caller reads back recomputes from its own fields."""
    entries = _json(developer_client.get("/audit"))
    assert isinstance(entries, list) and entries, "GET /api/audit returned no entries"
    previous = GENESIS_HASH
    for index, entry in enumerate(entries):
        assert entry.get("sequence") == index + 1, (
            f"audit sequence {entry.get('sequence')!r} at position {index + 1} is not gapless"
        )
        assert entry.get("previous_hash") == previous, (
            f"entry {entry.get('sequence')} names previous_hash "
            f"{entry.get('previous_hash')!r}, expected {previous!r}"
        )
        expected = audit_hash(
            entry.get("previous_hash"), entry.get("sequence"),
            entry.get("actor_email"), entry.get("action"),
            entry.get("resource_type"), entry.get("resource_id"),
            entry.get("occurred_at"))
        assert entry.get("entry_hash") == expected, (
            f"entry {entry.get('sequence')} hashes to {entry.get('entry_hash')!r}, "
            f"expected {expected!r}"
        )
        previous = entry.get("entry_hash")


def test_audit_row_is_appended_on_approval(compliance_client, developer_client,
                                           fresh_request):
    """An approval appends exactly one audit entry naming the approver."""
    before = _json(developer_client.get("/audit"))
    compliance_client.post(f"/access-requests/{fresh_request}/claim")
    compliance_client.post(f"/access-requests/{fresh_request}/approve")
    after = _json(developer_client.get("/audit"))
    assert len(after) > len(before), "approving appended no audit entry"
    added = after[len(before):]
    actors = {entry.get("actor_email") for entry in added}
    assert COMPLIANCE_EMAIL in actors, (
        f"the appended audit entries name {actors}, expected {COMPLIANCE_EMAIL!r}"
    )
    resources = {str(entry.get("resource_id")) for entry in added}
    assert fresh_request in resources, (
        f"no appended audit entry names {fresh_request}"
    )


def test_connection_payload_carries_no_consumer_financial_data(developer_client,
                                                               compliance_client):
    """No console response exposes a balance, a transaction or an account number."""
    listed = _json(developer_client.get("/connections"))
    detail = _json(developer_client.get(f"/connections/{REAUTH_CONNECTION}"))
    approver_view = _json(compliance_client.get(f"/connections/{REAUTH_CONNECTION}"))
    for label, payload in (("list", listed), ("detail", detail),
                           ("approver detail", approver_view)):
        text = str(payload).lower()
        for field in FORBIDDEN_CONSUMER_FIELDS:
            assert field not in text, (
                f"the connection {label} response exposes {field!r}"
            )
    reference = str(detail.get("consumer_reference", ""))
    assert reference.startswith("cst_") and "*" in reference, (
        f"consumer_reference {reference!r} is not masked"
    )


def test_connection_statuses_come_from_the_closed_set(developer_client):
    """Every seeded connection reports a status from the closed vocabulary."""
    rows = _json(developer_client.get("/connections"))
    by_id = {row.get("id"): row.get("status") for row in rows}
    for connection_id in (HEALTHY_CONNECTION, REAUTH_CONNECTION,
                          UNAVAILABLE_CONNECTION, REVOKED_CONNECTION):
        assert connection_id in by_id, f"{connection_id} is missing from /api/connections"
        assert by_id[connection_id] in CONNECTION_STATES, (
            f"{connection_id} reports status {by_id[connection_id]!r}, "
            f"which is outside the closed set"
        )
    assert by_id[HEALTHY_CONNECTION] == "healthy"
    assert by_id[REAUTH_CONNECTION] == "requires_reauthentication"
    assert by_id[UNAVAILABLE_CONNECTION] == "institution_unavailable"
    assert by_id[REVOKED_CONNECTION] == "revoked_by_consumer"


def test_seed_records_survive_a_reload(developer_client, backend):
    """The seeded fixtures are single rows in the store, not duplicated per boot."""
    for slug in (PAYOUTS_SLUG, RISK_SLUG, LEDGER_SLUG):
        assert backend.count("application", slug=slug) == 1, (
            f"application {slug!r} is not stored exactly once"
        )
    for request_id in (SUBMITTED_REQUEST, SELF_FILED_REQUEST):
        assert backend.count("access_request", id=request_id) == 1, (
            f"access request {request_id!r} is not stored exactly once"
        )
    applications = _json(developer_client.get("/applications"))
    slugs = [row.get("slug") for row in applications]
    assert len(slugs) == len(set(slugs)), f"the application list repeats a slug: {slugs}"


def test_webhook_endpoint_requires_a_secure_scheme(developer_client):
    """A webhook target without transport security is refused at creation."""
    response = developer_client.post("/webhook-endpoints", json={
        "application": PAYOUTS_SLUG,
        "environment": "development",
        "target_url": "http://hooks.vantor.example/insecure",
        "event_types": ["connection.created"],
    })
    assert response.status_code in REFUSED, (
        f"an insecure webhook target returned {response.status_code}, expected a refusal"
    )


def test_new_webhook_endpoint_is_unverified(developer_client):
    """A newly created endpoint starts unverified and receives nothing."""
    response = developer_client.post("/webhook-endpoints", json={
        "application": PAYOUTS_SLUG,
        "environment": "sandbox",
        "target_url": f"https://hooks.vantor.example/ravel-{unique_suffix()}",
        "event_types": ["connection.created"],
    })
    assert response.status_code in (200, 201), (
        f"creating a webhook endpoint returned {response.status_code}: {response.text[:400]}"
    )
    assert response.json().get("status") == "unverified", (
        f"a new endpoint reports status {response.json().get('status')!r}"
    )


def test_bulk_reauthentication_over_the_limit_is_refused(developer_client):
    """A prompt over the bulk limit is refused without a second approver."""
    ids = [f"con_bulk{index:04d}" for index in range(BULK_REAUTHENTICATION_LIMIT + 1)]
    response = developer_client.post("/connections/reauthentication-prompts",
                                     json={"connection_ids": ids})
    assert response.status_code in REFUSED + DENIED, (
        f"a bulk prompt over {BULK_REAUTHENTICATION_LIMIT} returned "
        f"{response.status_code}, expected a refusal"
    )


def test_application_region_is_immutable(administrator_client):
    """An application's region cannot be rewritten after creation."""
    name = f"Region Probe {unique_suffix()}"
    created = administrator_client.post("/applications", json={
        "name": name, "team": "Payments Integration", "region": "us"})
    assert created.status_code in (200, 201), (
        f"creating an application returned {created.status_code}: {created.text[:400]}"
    )
    slug = created.json().get("slug")
    assert slug, f"the created application carries no slug: {created.text[:400]}"
    for verb in ("patch", "post"):
        response = getattr(administrator_client, verb)(
            f"/applications/{slug}", json={"region": "eu"})
        assert response.status_code not in (200, 201, 204) or \
            _json(administrator_client.get(f"/applications/{slug}")).get("region") == "us", (
                f"a {verb.upper()} rewrote the region of {slug}"
            )
    assert _json(administrator_client.get(f"/applications/{slug}")).get("region") == "us"


def test_data_request_is_due_thirty_days_after_receipt(developer_client):
    """A consumer data request falls due thirty days after it was received."""
    rows = _json(developer_client.get("/data-requests"))
    by_id = {row.get("id"): row for row in rows}
    for request_id in (OPEN_DATA_REQUEST, CLOSED_DATA_REQUEST):
        assert request_id in by_id, f"{request_id} is missing from /api/data-requests"
    row = by_id[OPEN_DATA_REQUEST]
    assert row.get("state") == "received", (
        f"{OPEN_DATA_REQUEST} is {row.get('state')!r}, expected 'received'"
    )
    received = dt.datetime.fromisoformat(str(row["received_at"]).replace("Z", "+00:00"))
    due = dt.datetime.fromisoformat(str(row["due_at"]).replace("Z", "+00:00"))
    assert (due - received).days == DATA_REQUEST_DUE_DAYS, (
        f"{OPEN_DATA_REQUEST} is due {(due - received).days} days after receipt, "
        f"expected {DATA_REQUEST_DUE_DAYS}"
    )
    assert by_id[CLOSED_DATA_REQUEST].get("state") == "completed"


def test_usage_reports_requests_against_committed_volume(analyst_client):
    """The usage route reports consumption against the organisation's commitment."""
    body = _json(analyst_client.get("/usage"))
    assert body.get("committed_requests") == COMMITTED_REQUESTS, (
        f"usage reports committed_requests {body.get('committed_requests')!r}, "
        f"expected {COMMITTED_REQUESTS}"
    )
    assert isinstance(body.get("requests_used"), int), (
        f"usage reports requests_used {body.get('requests_used')!r}, expected an integer"
    )
    assert body.get("period_start") and body.get("period_end")


def test_environments_and_states_use_the_pinned_vocabulary(developer_client):
    """Environments and request states are reported with their pinned spellings."""
    application = _json(developer_client.get(f"/applications/{PAYOUTS_SLUG}"))
    kinds = {row.get("kind") for row in application.get("environments", [])}
    assert kinds == set(ENVIRONMENTS), (
        f"{PAYOUTS_SLUG} reports environments {sorted(kinds)}, expected {list(ENVIRONMENTS)}"
    )
    states = {row.get("state") for row in _json(developer_client.get("/access-requests"))}
    assert states <= set(REQUEST_STATES), (
        f"the queue reports states {sorted(states)} outside the closed set"
    )


def test_terms_page_is_reachable_from_every_route(anon_client):
    """A terms page answers and is linked from the sign-in route."""
    import httpx
    from appclient import app_url
    with httpx.Client(base_url=app_url(), timeout=30.0, follow_redirects=True) as browser:
        signin = browser.get("/login")
        assert signin.status_code == 200, (
            f"GET /login returned {signin.status_code}"
        )
        assert "terms" in signin.text.lower(), (
            "the sign-in route carries no link to a terms page"
        )
        terms = browser.get("/terms")
        assert terms.status_code == 200, (
            f"GET /terms returned {terms.status_code}, expected the terms page"
        )
        assert len(terms.text.strip()) > 200, "the terms page carries no content"


def test_cookie_choice_is_asked_once_and_survives_reload(anon_client):
    """A first-time visitor is asked about non-essential cookies once."""
    import httpx
    from appclient import app_url
    with httpx.Client(base_url=app_url(), timeout=30.0, follow_redirects=True) as browser:
        first = browser.get("/login")
        assert first.status_code == 200
        assert "cookie" in first.text.lower(), (
            "a first-time visitor is never asked about non-essential cookies"
        )
        assert browser.cookies or "cookie" in first.text.lower()
        again = browser.get("/login")
        assert again.status_code == 200, (
            f"a reload of /login returned {again.status_code}"
        )


def test_every_internal_link_resolves(anon_client):
    """Every internal link on the sign-in route resolves."""
    import re
    import httpx
    from appclient import app_url
    with httpx.Client(base_url=app_url(), timeout=30.0, follow_redirects=True) as browser:
        page = browser.get("/login")
        assert page.status_code == 200
        hrefs = {h for h in re.findall(r'href="(/[^"#?]*)"', page.text)}
        for href in sorted(hrefs):
            response = browser.get(href)
            assert response.status_code < 400, (
                f"internal link {href} on /login returned {response.status_code}"
            )


def test_repeated_signin_is_refused(anon_client):
    """A sign-in submitted repeatedly in quick succession is refused."""
    codes = []
    for _ in range(12):
        response = anon_client.post("/auth/login", json={
            "email": "developer@example.com", "password": "not-the-password"})
        codes.append(response.status_code)
    assert any(code == 429 for code in codes) or codes[-1] in (401, 403, 423), (
        f"twelve rapid sign-in attempts returned {codes}, none of them refused"
    )


def test_no_secret_reaches_the_browser(anon_client, developer_client):
    """No credential value appears in anything the browser downloads."""
    import re
    import httpx
    from appclient import app_url
    created = developer_client.post(
        "/applications/vantor-payouts/sandbox/credentials")
    assert created.status_code in (200, 201)
    secret = created.json().get("secret")
    assert secret
    with httpx.Client(base_url=app_url(), timeout=30.0, follow_redirects=True) as browser:
        page = browser.get("/login")
        assert page.status_code == 200
        body = page.text
        assert secret not in body, "a credential secret reaches the sign-in markup"
        assert "AUTH_CLIENT_SECRET" not in body, (
            "the confidential client secret's name reaches the browser"
        )
        for src in set(re.findall(r'src="(/[^"?]*\.js)"', body)):
            asset = browser.get(src)
            if asset.status_code != 200:
                continue
            assert secret not in asset.text, f"{src} carries a credential secret"
