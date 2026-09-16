"""The one section module for deku/serverless-compute-platform-vb.

Every assertion here is black box: the app is observed over HTTP at the App
Contract origin and its stored rows are read through the generic backend
adapter. Nothing imports the agent's code.
"""

from __future__ import annotations

import os

import httpx
import pytest
from urllib.parse import urlsplit
from conftest import (
    APP_NOVA,
    CONTAINER_EXIT_REASONS,
    DENIED,
    DEVELOPER_EMAIL,
    OPERATOR2_EMAIL,
    PLATFORM_EXIT_REASONS,
    READONLY_EMAIL,
    REFUSED,
    REQUEST_STATES,
    SEED_PASSWORD,
    WORKSPACE_SLUG,
    apply_request,
    body,
    decide,
    dev,
    field,
    file_a_request,
    find_app,
    items,
    open_request,
    prod,
    request_row,
    settle,
)

SEED_EMAILS = (
    "owner@example.com",
    "operator@example.com",
    "operator2@example.com",
    "developer@example.com",
    "developer2@example.com",
    "readonly@example.com",
)


def test_health_endpoint_returns_200(anon_client):
    """Readiness is reported at the contract path."""
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, expected 200: "
        f"{body(response)}"
    )


def test_seeded_principals_sign_in(anon_client):
    """Every seeded principal exchanges the seeded password for a bearer token."""
    for email in SEED_EMAILS:
        response = anon_client.post(
            "/auth/login", json={"email": email, "password": SEED_PASSWORD}
        )
        assert response.status_code == 200, (
            f"POST /api/auth/login for the seeded principal {email} returned "
            f"{response.status_code}, expected 200: {body(response)}"
        )
        assert response.json().get("access_token"), (
            f"the sign-in response for {email} carries no access_token: "
            f"{body(response)}"
        )


def test_wrong_password_is_rejected(anon_client):
    """A wrong password is refused and issues no token."""
    response = anon_client.post(
        "/auth/login",
        json={"email": DEVELOPER_EMAIL, "password": "not-the-seeded-password"},
    )
    assert response.status_code in DENIED, (
        f"POST /api/auth/login for {DEVELOPER_EMAIL} with a wrong password "
        f"returned {response.status_code}, expected one of {DENIED}: "
        f"{body(response)}"
    )
    payload = response.json() if response.headers.get(
        "content-type", ""
    ).startswith("application/json") else {}
    assert not payload.get("access_token"), (
        f"a refused sign-in for {DEVELOPER_EMAIL} still returned an access_token: "
        f"{body(response)}"
    )


def test_unauthenticated_console_call_is_denied(anon_client):
    """A console endpoint reached with no session is denied at the API."""
    for path in (prod("/apps"), prod("/requests"), prod("/audit")):
        response = anon_client.get(path)
        assert response.status_code in DENIED, (
            f"GET /api{path} with no session returned {response.status_code}, "
            f"expected one of {DENIED}: {body(response)}"
        )


def test_cross_workspace_resource_is_not_found(developer_client):
    """A workspace the principal is not a member of is not disclosed."""
    response = developer_client.get("/w/other-tenant/production/apps")
    assert response.status_code in (401, 403, 404), (
        f"GET /api/w/other-tenant/production/apps from a developer session "
        f"returned {response.status_code}, expected 404 or a denial: "
        f"{body(response)}"
    )
    if response.status_code == 200:
        pytest.fail(
            f"a workspace the principal does not belong to answered 200: "
            f"{body(response)}"
        )


def test_developer_files_production_deploy_request(developer_client, backend):
    """A developer files a promotion request and the row lands in review."""
    request_id = open_request(
        developer_client, APP_NOVA, "Promote the newest built version to production"
    )
    settle()
    read_back = request_row(developer_client, request_id)
    assert read_back.status_code == 200, (
        f"GET the filed request {request_id} returned {read_back.status_code}, "
        f"expected 200: {body(read_back)}"
    )
    state = str(field(read_back.json(), "state", "status", default="")).lower()
    assert state in ("submitted", "in-review"), (
        f"the filed request {request_id} carries state {state!r}, expected "
        f"'submitted' or 'in-review': {body(read_back)}"
    )
    assert state in REQUEST_STATES, (
        f"the filed request {request_id} carries state {state!r}, which is "
        f"outside the closed set {REQUEST_STATES}: {body(read_back)}"
    )


def test_request_without_reason_is_refused(developer_client):
    """A promotion request filed with an empty reason is refused and stores nothing."""
    before = developer_client.get(prod("/requests"))
    assert before.status_code == 200, (
        f"GET {prod('/requests')} returned {before.status_code}, expected 200: "
        f"{body(before)}"
    )
    count_before = len(items(before.json()))
    response = file_a_request(developer_client, APP_NOVA, 1, "")
    assert response.status_code in REFUSED, (
        f"POST {prod('/requests')} with an empty reason returned "
        f"{response.status_code}, expected one of {REFUSED}: {body(response)}"
    )
    after = developer_client.get(prod("/requests"))
    assert len(items(after.json())) == count_before, (
        f"a refused request filing changed the request count from "
        f"{count_before} to {len(items(after.json()))}: {body(after)}"
    )


def test_direct_promote_by_developer_is_denied(developer_client):
    """A developer promoting a production version without a request is denied."""
    listing = developer_client.get(prod("/apps"))
    assert listing.status_code == 200, (
        f"GET {prod('/apps')} returned {listing.status_code}, expected 200: "
        f"{body(listing)}"
    )
    row = find_app(items(listing.json()), APP_NOVA)
    assert row is not None, (
        f"seeded app {APP_NOVA!r} is absent from {prod('/apps')}: {body(listing)}"
    )
    app_key = field(row, "id", "slug", "name")
    live_before = field(row, "live_version", "current_version", "version")
    response = developer_client.post(
        prod(f"/apps/{app_key}/promote"), json={"requested_version": 3}
    )
    assert response.status_code in DENIED, (
        f"POST {prod('/apps/{app}/promote')} from a developer session returned "
        f"{response.status_code}, expected one of {DENIED}: {body(response)}"
    )
    after = developer_client.get(prod("/apps"))
    live_after = field(find_app(items(after.json()), APP_NOVA) or {},
                       "live_version", "current_version", "version")
    assert live_after == live_before, (
        f"a denied direct promote changed the live version of {APP_NOVA!r} from "
        f"{live_before!r} to {live_after!r}: {body(after)}"
    )


def test_operator_decides_request_and_records_reason(
    developer_client, operator2_client
):
    """An operator who is not the requester approves and the reason is recorded."""
    request_id = open_request(
        developer_client, APP_NOVA, "Promote after the staging soak"
    )
    reason = "Soak is clean and the rollback path is confirmed"
    response = decide(operator2_client, request_id, "approve", reason)
    assert response.status_code in (200, 201), (
        f"POST the decision on request {request_id} as {OPERATOR2_EMAIL} returned "
        f"{response.status_code}, expected 200 or 201: {body(response)}"
    )
    read_back = request_row(operator2_client, request_id)
    payload = read_back.json()
    state = str(field(payload, "state", "status", default="")).lower()
    assert state == "approved", (
        f"request {request_id} carries state {state!r} after an approval, "
        f"expected 'approved': {body(read_back)}"
    )
    stored_reason = str(
        field(payload, "decision_reason", "decided_reason", default="")
    )
    assert reason in stored_reason, (
        f"request {request_id} carries decision reason {stored_reason!r}, which "
        f"does not carry the reason the approver supplied: {body(read_back)}"
    )
    decider = str(field(payload, "decided_by", "decider", default=""))
    assert OPERATOR2_EMAIL in decider, (
        f"request {request_id} records decider {decider!r}, expected "
        f"{OPERATOR2_EMAIL}: {body(read_back)}"
    )


def test_developer_cannot_decide_request(developer_client, developer2_client):
    """A developer calling the decision endpoint is denied at the API."""
    request_id = open_request(
        developer_client, APP_NOVA, "Promote the rerank fix to production"
    )
    response = decide(
        developer2_client, request_id, "approve", "Looks fine to me"
    )
    assert response.status_code in DENIED, (
        f"POST the decision on request {request_id} from a developer session "
        f"returned {response.status_code}, expected one of {DENIED}: "
        f"{body(response)}"
    )


def test_decision_leaves_row_untouched_for_developer(
    developer_client, developer2_client, operator_client
):
    """A denied decision changes no field of the request row."""
    request_id = open_request(
        developer_client, APP_NOVA, "Promote the embed rebuild to production"
    )
    before = request_row(operator_client, request_id).json()
    decide(developer2_client, request_id, "approve", "Approving anyway")
    settle()
    after = request_row(operator_client, request_id).json()
    for key in ("state", "status"):
        assert field(before, key) == field(after, key), (
            f"the {key!r} of request {request_id} moved from "
            f"{field(before, key)!r} to {field(after, key)!r} after a denied "
            f"decision by a developer"
        )
    for key in ("decided_by", "decider", "decision_reason", "decided_reason"):
        assert field(before, key) == field(after, key), (
            f"the {key!r} of request {request_id} moved from "
            f"{field(before, key)!r} to {field(after, key)!r} after a denied "
            f"decision by a developer"
        )


def test_requester_cannot_decide_own_request(operator_client):
    """The member who filed a request may not decide it, whatever role they hold."""
    request_id = open_request(
        operator_client, APP_NOVA, "Promote the nightly rollup change"
    )
    response = decide(
        operator_client, request_id, "approve", "Approving my own request"
    )
    assert response.status_code in DENIED, (
        f"POST the decision on request {request_id} by the member who filed it "
        f"returned {response.status_code}, expected one of {DENIED}: "
        f"{body(response)}"
    )


def test_decision_leaves_row_untouched_for_requester(
    operator_client, operator2_client
):
    """A decision denied for separation of duties changes no field of the row."""
    request_id = open_request(
        operator_client, APP_NOVA, "Promote the scheduler patch to production"
    )
    before = request_row(operator2_client, request_id).json()
    decide(operator_client, request_id, "approve", "Approving my own request")
    settle()
    after = request_row(operator2_client, request_id).json()
    for key in ("state", "status", "decided_by", "decider", "decision_reason"):
        assert field(before, key) == field(after, key), (
            f"the {key!r} of request {request_id} moved from "
            f"{field(before, key)!r} to {field(after, key)!r} after a decision "
            f"denied for separation of duties"
        )


def test_approval_does_not_change_live_version(
    developer_client, operator2_client
):
    """Approval alone promotes nothing: the live version is unchanged."""
    listing = developer_client.get(prod("/apps"))
    live_before = field(
        find_app(items(listing.json()), APP_NOVA) or {},
        "live_version", "current_version", "version",
    )
    request_id = open_request(
        developer_client, APP_NOVA, "Promote the newest built version"
    )
    decide(operator2_client, request_id, "approve", "Approved for the release window")
    settle()
    after = developer_client.get(prod("/apps"))
    live_after = field(
        find_app(items(after.json()), APP_NOVA) or {},
        "live_version", "current_version", "version",
    )
    assert live_after == live_before, (
        f"approving a request changed the live version of {APP_NOVA!r} from "
        f"{live_before!r} to {live_after!r} before any apply step ran: "
        f"{body(after)}"
    )


def test_apply_promotes_version_and_marks_applied(
    developer_client, operator2_client
):
    """A separate apply step promotes the version and the request reaches applied."""
    request_id = open_request(
        developer_client, APP_NOVA, "Promote the newest built version"
    )
    decide(operator2_client, request_id, "approve", "Approved for the release window")
    response = apply_request(operator2_client, request_id)
    assert response.status_code in (200, 201, 202), (
        f"POST the apply step on request {request_id} returned "
        f"{response.status_code}, expected 200, 201 or 202: {body(response)}"
    )
    settle()
    read_back = request_row(operator2_client, request_id)
    payload = read_back.json()
    state = str(field(payload, "state", "status", default="")).lower()
    assert state == "applied", (
        f"request {request_id} carries state {state!r} after the apply step, "
        f"expected 'applied': {body(read_back)}"
    )
    requested = field(payload, "requested_version", "version")
    listing = developer_client.get(prod("/apps"))
    live_after = field(
        find_app(items(listing.json()), APP_NOVA) or {},
        "live_version", "current_version", "version",
    )
    assert str(live_after) == str(requested), (
        f"after applying request {request_id} the live version of {APP_NOVA!r} is "
        f"{live_after!r}, expected the requested version {requested!r}: "
        f"{body(listing)}"
    )


def test_second_decision_conflicts(developer_client, operator2_client, owner_client):
    """A decision against an already decided request conflicts."""
    request_id = open_request(
        developer_client, APP_NOVA, "Promote the newest built version"
    )
    first = decide(operator2_client, request_id, "approve", "Approved for release")
    assert first.status_code in (200, 201), (
        f"the first decision on request {request_id} returned {first.status_code}, "
        f"expected 200 or 201: {body(first)}"
    )
    second = decide(owner_client, request_id, "reject", "Changed my mind")
    assert second.status_code == 409, (
        f"a second decision on the already decided request {request_id} returned "
        f"{second.status_code}, expected 409: {body(second)}"
    )


def test_transition_outside_state_machine_is_refused(
    developer_client, operator2_client
):
    """A transition the state machine does not allow is refused."""
    request_id = open_request(
        developer_client, APP_NOVA, "Promote the newest built version"
    )
    response = apply_request(operator2_client, request_id)
    assert response.status_code in (400, 409, 422), (
        f"applying request {request_id} while it is still in review returned "
        f"{response.status_code}, expected 400, 409 or 422: {body(response)}"
    )


def test_container_exit_reason_is_from_closed_vocabulary(operator_client):
    """Every terminated container carries a reason from the closed vocabulary."""
    response = operator_client.get(prod("/containers"))
    assert response.status_code == 200, (
        f"GET {prod('/containers')} returned {response.status_code}, expected "
        f"200: {body(response)}"
    )
    rows = items(response.json())
    assert rows, (
        f"{prod('/containers')} lists no seeded containers: {body(response)}"
    )
    terminated = [
        row for row in rows
        if str(field(row, "state", "status", default="")).lower()
        in ("terminated", "failed")
    ]
    assert terminated, (
        f"{prod('/containers')} lists no terminated container, so no exit reason "
        f"can be read: {body(response)}"
    )
    for row in terminated:
        reason = str(field(row, "exit_reason", "exit", "reason", default=""))
        assert reason in CONTAINER_EXIT_REASONS, (
            f"a terminated container carries exit reason {reason!r}, which is "
            f"outside the closed vocabulary {CONTAINER_EXIT_REASONS}: "
            f"{body(response)}"
        )


def test_invalid_container_exit_reason_is_refused(operator_client):
    """A container exit reason outside the closed vocabulary is refused."""
    response = operator_client.post(
        prod("/containers"),
        json={
            "function": "embed",
            "state": "terminated",
            "exit_reason": "exploded-spectacularly",
        },
    )
    assert response.status_code in (400, 403, 422), (
        f"POST {prod('/containers')} with an exit reason outside the closed "
        f"vocabulary returned {response.status_code}, expected 400, 403 or 422: "
        f"{body(response)}"
    )


def test_platform_faults_excluded_from_error_rate(operator_client):
    """A platform fault is marked as the platform's own, not the customer's."""
    response = operator_client.get(prod("/containers"))
    rows = items(response.json())
    platform_rows = [
        row for row in rows
        if str(field(row, "exit_reason", "exit", "reason", default=""))
        in PLATFORM_EXIT_REASONS
    ]
    assert platform_rows, (
        f"{prod('/containers')} lists no container carrying a platform exit "
        f"reason from {PLATFORM_EXIT_REASONS}: {body(response)}"
    )
    for row in platform_rows:
        flag = field(
            row, "platform_fault", "is_platform_fault", "counts_toward_error_rate",
            "customer_error",
        )
        assert flag is not None, (
            f"a container carrying exit reason "
            f"{field(row, 'exit_reason', 'exit', 'reason')!r} states nothing about "
            f"whether the fault is the platform's own: {body(response)}"
        )


def test_secret_value_never_returned(owner_client, developer_client):
    """No route, for any role, returns a secret value."""
    created = owner_client.post(
        prod("/secrets"),
        json={
            "name": "probe-secret",
            "description": "A probe for the read-back rule",
            "entries": {"PROBE_KEY": "probe-value-never-readable"},
        },
    )
    assert created.status_code in (200, 201), (
        f"POST {prod('/secrets')} returned {created.status_code}, expected 200 "
        f"or 201: {body(created)}"
    )
    assert "probe-value-never-readable" not in created.text, (
        f"the secret creation response returned the value that was written: "
        f"{body(created)}"
    )
    for http_client, who in ((owner_client, "an owner"),
                             (developer_client, "a developer")):
        listing = http_client.get(prod("/secrets"))
        assert "probe-value-never-readable" not in listing.text, (
            f"GET {prod('/secrets')} as {who} returned the stored secret value: "
            f"{body(listing)}"
        )


def test_secret_delete_with_live_reference_conflicts(owner_client):
    """A secret a live deployment references cannot be deleted."""
    listing = owner_client.get(prod("/secrets"))
    assert listing.status_code == 200, (
        f"GET {prod('/secrets')} returned {listing.status_code}, expected 200: "
        f"{body(listing)}"
    )
    referenced = None
    for row in items(listing.json()):
        granted = field(row, "functions", "granted_to", "grants", default=[])
        if granted:
            referenced = row
    assert referenced is not None, (
        f"{prod('/secrets')} lists no secret granted to a function, so the "
        f"refusal cannot be observed: {body(listing)}"
    )
    secret_key = field(referenced, "id", "name")
    response = owner_client.delete(prod(f"/secrets/{secret_key}"))
    assert response.status_code == 409, (
        f"DELETE {prod('/secrets/{id}')} for a secret a live deployment "
        f"references returned {response.status_code}, expected 409: "
        f"{body(response)}"
    )


def test_machine_token_secret_shown_once(developer_client):
    """A machine token secret is returned at creation and never again."""
    created = developer_client.post(
        prod("/tokens"),
        json={"name": "probe-token", "scopes": ["app.read"],
              "environment": "production"},
    )
    assert created.status_code in (200, 201), (
        f"POST {prod('/tokens')} returned {created.status_code}, expected 200 or "
        f"201: {body(created)}"
    )
    payload = created.json()
    secret = field(payload, "secret", "token", "value")
    assert secret, (
        f"the token creation response carries no secret, so it can never be "
        f"copied: {body(created)}"
    )
    token_key = field(payload, "id", "prefix", "name")
    listing = developer_client.get(prod("/tokens"))
    assert str(secret) not in listing.text, (
        f"GET {prod('/tokens')} returned the token secret a second time: "
        f"{body(listing)}"
    )
    detail = developer_client.get(prod(f"/tokens"), params={"id": token_key})
    assert str(secret) not in detail.text, (
        f"reading the token back returned its secret a second time: "
        f"{body(detail)}"
    )


def test_token_revoke_by_other_developer_is_denied(
    developer_client, developer2_client
):
    """A developer revoking a token another principal created is denied."""
    created = developer_client.post(
        prod("/tokens"),
        json={"name": "probe-token-owned", "scopes": ["app.read"],
              "environment": "production"},
    )
    assert created.status_code in (200, 201), (
        f"POST {prod('/tokens')} returned {created.status_code}, expected 200 or "
        f"201: {body(created)}"
    )
    token_key = field(created.json(), "id", "prefix", "name")
    response = developer2_client.post(
        prod(f"/tokens/{token_key}/revoke"), json={}
    )
    assert response.status_code in DENIED, (
        f"POST {prod('/tokens/{id}/revoke')} from a developer who did not create "
        f"the token returned {response.status_code}, expected one of {DENIED}: "
        f"{body(response)}"
    )


def test_readonly_member_denied_log_body(readonly_client):
    """A read-only member is denied a log body."""
    response = readonly_client.get(
        prod("/logs"), params={"app": APP_NOVA, "range": "1h"}
    )
    assert response.status_code in DENIED, (
        f"GET {prod('/logs')} as {READONLY_EMAIL} returned "
        f"{response.status_code}, expected one of {DENIED}: {body(response)}"
    )


def test_unbounded_log_query_is_refused(operator_client):
    """A log query with no bound is refused rather than executed."""
    response = operator_client.get(prod("/logs"), params={"range": "all"})
    assert response.status_code in (400, 422), (
        f"GET {prod('/logs')} with an unbounded range returned "
        f"{response.status_code}, expected 400 or 422: {body(response)}"
    )


def test_rollback_without_reason_is_refused(operator_client):
    """A production rollback with no reason is refused."""
    listing = operator_client.get(prod("/apps"))
    row = find_app(items(listing.json()), APP_NOVA)
    assert row is not None, (
        f"seeded app {APP_NOVA!r} is absent from {prod('/apps')}: {body(listing)}"
    )
    app_key = field(row, "id", "slug", "name")
    response = operator_client.post(
        prod(f"/apps/{app_key}/rollback"), json={"reason": ""}
    )
    assert response.status_code in REFUSED, (
        f"POST {prod('/apps/{app}/rollback')} with an empty reason returned "
        f"{response.status_code}, expected one of {REFUSED}: {body(response)}"
    )


def test_rollback_creates_new_version(operator_client):
    """A rollback adds a version rather than mutating history."""
    listing = operator_client.get(prod("/apps"))
    row = find_app(items(listing.json()), APP_NOVA)
    app_key = field(row, "id", "slug", "name")
    detail_before = operator_client.get(prod(f"/apps/{app_key}"))
    count_before = len(items(field(detail_before.json(), "versions", default=[])))
    response = operator_client.post(
        prod(f"/apps/{app_key}/rollback"),
        json={"reason": "The newest version raised the error rate"},
    )
    assert response.status_code in (200, 201, 202), (
        f"POST {prod('/apps/{app}/rollback')} with a reason returned "
        f"{response.status_code}, expected 200, 201 or 202: {body(response)}"
    )
    settle()
    detail_after = operator_client.get(prod(f"/apps/{app_key}"))
    count_after = len(items(field(detail_after.json(), "versions", default=[])))
    assert count_after == count_before + 1, (
        f"a rollback of {APP_NOVA!r} left the version count at {count_after}, "
        f"expected {count_before + 1}: a rollback is a new version pointing at "
        f"the previous artifact: {body(detail_after)}"
    )


def test_audit_entry_update_is_forbidden(owner_client):
    """An audit entry cannot be updated through any endpoint."""
    listing = owner_client.get(prod("/audit"))
    assert listing.status_code == 200, (
        f"GET {prod('/audit')} returned {listing.status_code}, expected 200: "
        f"{body(listing)}"
    )
    rows = items(listing.json())
    assert rows, f"{prod('/audit')} carries no entries: {body(listing)}"
    entry_key = field(rows[0], "id", "entry_id")
    response = owner_client.patch(
        prod(f"/audit/{entry_key}"), json={"action": "rewritten"}
    )
    assert response.status_code in (403, 404, 405), (
        f"PATCH {prod('/audit/{id}')} returned {response.status_code}, expected "
        f"403, 404 or 405: an audit entry is append-only: {body(response)}"
    )


def test_audit_entry_delete_is_forbidden(owner_client):
    """An audit entry cannot be deleted through any endpoint."""
    listing = owner_client.get(prod("/audit"))
    rows = items(listing.json())
    assert rows, f"{prod('/audit')} carries no entries: {body(listing)}"
    entry_key = field(rows[0], "id", "entry_id")
    response = owner_client.delete(prod(f"/audit/{entry_key}"))
    assert response.status_code in (403, 404, 405), (
        f"DELETE {prod('/audit/{id}')} returned {response.status_code}, expected "
        f"403, 404 or 405: an audit entry is append-only: {body(response)}"
    )


def test_audit_row_persisted_after_refused_update(owner_client):
    """The stored audit row is unchanged after a refused update."""
    listing = owner_client.get(prod("/audit"))
    rows = items(listing.json())
    assert rows, f"{prod('/audit')} carries no entries: {body(listing)}"
    entry_key = field(rows[0], "id", "entry_id")
    before = rows[0]
    owner_client.patch(prod(f"/audit/{entry_key}"), json={"action": "rewritten"})
    settle()
    after_listing = owner_client.get(prod("/audit"))
    after = None
    for row in items(after_listing.json()):
        if field(row, "id", "entry_id") == entry_key:
            after = row
    assert after is not None, (
        f"the audit entry {entry_key} disappeared after a refused update: "
        f"{body(after_listing)}"
    )
    assert field(after, "action") == field(before, "action"), (
        f"the stored audit entry {entry_key} changed its action from "
        f"{field(before, 'action')!r} to {field(after, 'action')!r} after a "
        f"refused update"
    )


def test_form_validation_writes_nothing(developer_client):
    """A refused creation leaves the stored record count unchanged."""
    before = developer_client.get(prod("/tokens"))
    assert before.status_code == 200, (
        f"GET {prod('/tokens')} returned {before.status_code}, expected 200: "
        f"{body(before)}"
    )
    count_before = len(items(before.json()))
    response = developer_client.post(
        prod("/tokens"), json={"name": "", "scopes": []}
    )
    assert response.status_code in REFUSED, (
        f"POST {prod('/tokens')} with an empty name returned "
        f"{response.status_code}, expected one of {REFUSED}: {body(response)}"
    )
    after = developer_client.get(prod("/tokens"))
    assert len(items(after.json())) == count_before, (
        f"a refused token creation changed the token count from {count_before} "
        f"to {len(items(after.json()))}: {body(after)}"
    )


def test_seeded_roles_persisted(backend, owner_client):
    """Every seeded principal is stored with the role the brief pins."""
    response = owner_client.get(prod("/team"))
    if response.status_code == 200:
        rows = items(response.json())
        emails = {
            str(field(row, "email", "member", "username", default="")).lower()
            for row in rows
        }
        for email in SEED_EMAILS:
            assert email in emails, (
                f"the seeded principal {email} is absent from {prod('/team')}: "
                f"{body(response)}"
            )
        return
    assert response.status_code in DENIED or response.status_code == 404, (
        f"GET {prod('/team')} returned {response.status_code}, expected 200 or a "
        f"denial: {body(response)}"
    )
    for email in SEED_EMAILS:
        login_probe = httpx.post(
            f"{os.environ['APP_PUBLIC_URL'].rstrip('/')}/api/auth/login",
            json={"email": email, "password": SEED_PASSWORD},
            timeout=30.0,
        )
        assert login_probe.status_code == 200, (
            f"the seeded principal {email} could not sign in, so the seeded "
            f"membership is not stored: {login_probe.status_code} "
            f"{login_probe.text[:400]}"
        )


def test_seed_is_idempotent(owner_client):
    """The seeded rows appear exactly once, so a restart duplicated nothing."""
    listing = owner_client.get(prod("/apps"))
    assert listing.status_code == 200, (
        f"GET {prod('/apps')} returned {listing.status_code}, expected 200: "
        f"{body(listing)}"
    )
    names = [str(field(row, "name", default="")) for row in items(listing.json())]
    assert names.count(APP_NOVA) == 1, (
        f"the seeded app {APP_NOVA!r} appears {names.count(APP_NOVA)} times in "
        f"{prod('/apps')}, expected exactly one row: seeding is idempotent: "
        f"{body(listing)}"
    )
    dev_listing = owner_client.get(dev("/apps"))
    assert dev_listing.status_code == 200, (
        f"GET {dev('/apps')} returned {dev_listing.status_code}, expected 200: "
        f"{body(dev_listing)}"
    )
    dev_names = [
        str(field(row, "name", default="")) for row in items(dev_listing.json())
    ]
    assert dev_names.count(APP_NOVA) == 1, (
        f"the seeded app {APP_NOVA!r} appears {dev_names.count(APP_NOVA)} times "
        f"in {dev('/apps')}, expected exactly one row: {body(dev_listing)}"
    )


def test_unknown_address_renders_not_found_page(app_base_url):
    """An unknown address renders the product's own not-found page."""
    response = httpx.get(
        f"{app_base_url}/no-such-route-probe", timeout=30.0, follow_redirects=True
    )
    assert response.status_code == 404, (
        f"GET /no-such-route-probe returned {response.status_code}, expected "
        f"404: {response.text[:400]}"
    )
    text = response.text.lower()
    assert "vireo" in text, (
        f"the not-found page does not carry the product wordmark, so it is not "
        f"the product's own page: {response.text[:400]}"
    )
    assert "href=" in text, (
        f"the not-found page offers no way back: {response.text[:400]}"
    )


def test_privacy_page_reachable_from_footer(app_base_url):
    """A privacy page is reachable and the public page links to it."""
    privacy = httpx.get(
        f"{app_base_url}/privacy", timeout=30.0, follow_redirects=True
    )
    assert privacy.status_code == 200, (
        f"GET /privacy returned {privacy.status_code}, expected 200: "
        f"{privacy.text[:400]}"
    )
    home = httpx.get(f"{app_base_url}/", timeout=30.0, follow_redirects=True)
    assert home.status_code == 200, (
        f"GET / returned {home.status_code}, expected 200: {home.text[:400]}"
    )
    assert "/privacy" in home.text, (
        f"the public page carries no link to /privacy, so the privacy page is "
        f"not reachable from the footer: {home.text[:400]}"
    )


def test_public_route_declares_social_preview(app_base_url):
    """Every public route declares a social preview title and an image."""
    for path in ("/", "/privacy"):
        response = httpx.get(
            f"{app_base_url}{path}", timeout=30.0, follow_redirects=True
        )
        assert response.status_code == 200, (
            f"GET {path} returned {response.status_code}, expected 200: "
            f"{response.text[:400]}"
        )
        markup = response.text.lower()
        assert "og:title" in markup, (
            f"the public route {path} declares no social preview title: "
            f"{response.text[:400]}"
        )
        assert "og:image" in markup, (
            f"the public route {path} declares no social preview image: "
            f"{response.text[:400]}"
        )
        assert "<title" in markup, (
            f"the public route {path} carries no document title: "
            f"{response.text[:400]}"
        )


def _infra_secrets() -> tuple[str, ...]:
    """The credential strings the verifier holds, taken from its own environment.

    Read rather than hardcoded so the assertion follows the deployed values and
    the brief never has to pin an infrastructure credential.
    """
    found = []
    for name in ("DATABASE_URL", "DB_URL", "DB_ADMIN_URL", "AUTH_URL"):
        raw = os.environ.get(name, "")
        parsed = urlsplit(raw)
        for part in (parsed.username, parsed.password):
            if part and len(part) > 3:
                found.append(part)
    return tuple(dict.fromkeys(found))


def test_no_credential_in_browser_payload(app_base_url):
    """Nothing the browser downloads carries a credential."""
    forbidden = (SEED_PASSWORD,) + _infra_secrets()
    for path in ("/", "/privacy", "/login"):
        response = httpx.get(
            f"{app_base_url}{path}", timeout=30.0, follow_redirects=True
        )
        assert response.status_code == 200, (
            f"GET {path} returned {response.status_code}, expected 200: "
            f"{response.text[:400]}"
        )
        for needle in forbidden:
            assert needle not in response.text, (
                f"the public route {path} ships the credential {needle!r} in "
                f"what the browser downloads: {response.text[:400]}"
            )
