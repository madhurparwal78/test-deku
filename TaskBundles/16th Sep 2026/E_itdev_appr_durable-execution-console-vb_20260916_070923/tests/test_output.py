"""The one pytest module for Perpetua Cloud.

Every assertion here is black-box: HTTP against the deployed app, or a read of
the declared backing service through the shared capability adapter. Nothing
inspects the source the agent wrote.
"""

from __future__ import annotations

import threading

import httpx
import pytest

import appclient
import conftest as fx



def test_health_route_reports_ready(public):
    """The health route answers with success once the app is ready."""
    response = public.get("/api/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:200]}"
    )


def test_seeded_namespace_rows_exist(backend):
    """The three seeded namespaces are stored rows, readable by a second connection."""
    for namespace in (fx.GRADED_NAMESPACE, fx.SECOND_NAMESPACE, fx.FOREIGN_NAMESPACE):
        assert backend.count("namespace", name=namespace) == 1, (
            f"expected exactly one stored namespace row named {namespace!r}, "
            f"found {backend.count('namespace', name=namespace)}"
        )
    graded = backend.one("namespace", name=fx.GRADED_NAMESPACE)
    assert graded is not None, f"no stored row for {fx.GRADED_NAMESPACE}"
    assert str(graded.get("region")) == fx.GRADED_REGION, (
        f"{fx.GRADED_NAMESPACE} region is {graded.get('region')!r}, "
        f"expected {fx.GRADED_REGION!r}"
    )
    assert int(graded.get("retention_days")) == fx.GRADED_RETENTION_DAYS, (
        f"{fx.GRADED_NAMESPACE} retention_days is {graded.get('retention_days')!r}, "
        f"expected {fx.GRADED_RETENTION_DAYS}"
    )


def test_seeded_principal_login_token_is_accepted(developer):
    """A seeded principal signs in and the returned credential is accepted."""
    response = developer.get("/me")
    assert response.status_code in fx.OK, (
        f"GET /api/me with a seeded credential returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    body = response.json()
    assert fx.DEVELOPER_EMAIL in str(body), (
        f"GET /api/me does not name the signed-in principal {fx.DEVELOPER_EMAIL}: {body}"
    )


def test_developer_files_retention_request_row_saved(developer, backend):
    """A filed retention reduction is stored pending with no approval recorded."""
    before = fx.change_request_count(backend)
    filed = fx.file_change_request(developer)
    request_id = fx.request_id_of(filed)
    after = fx.change_request_count(backend)
    assert after == before + 1, (
        f"filing one request changed the stored change_request count from "
        f"{before} to {after}"
    )
    assert fx.state_of(filed) == fx.STATE_PENDING, (
        f"a freshly filed request is {fx.state_of(filed)!r}, expected "
        f"{fx.STATE_PENDING!r}"
    )
    assert fx.approval_count(backend, change_request_id=request_id) == 0, (
        f"request {request_id} carries an approval row before anyone approved it"
    )


def test_request_states_match_the_pinned_lifecycle(developer, namespace_admin, backend):
    """Every state a request reports is one of the nine pinned names."""
    filed = fx.file_change_request(developer)
    request_id = fx.request_id_of(filed)
    seen = {fx.state_of(filed)}
    approved = fx.approve(namespace_admin, request_id)
    assert approved.status_code in fx.CREATED, (
        f"approving {request_id} as a second principal returned "
        f"{approved.status_code}: {approved.text[:300]}"
    )
    seen.add(fx.state_of(fx.read_request(namespace_admin, request_id).json()))
    applied = fx.apply_request(namespace_admin, request_id)
    assert applied.status_code in fx.CREATED, (
        f"applying {request_id} returned {applied.status_code}: {applied.text[:300]}"
    )
    seen.add(fx.state_of(fx.read_request(namespace_admin, request_id).json()))
    unknown = seen - set(fx.REQUEST_STATES)
    assert not unknown, (
        f"the request reported state(s) {sorted(unknown)} outside the pinned set "
        f"{list(fx.REQUEST_STATES)}"
    )


def test_execution_detail_omits_history_payload(developer):
    """The execution detail answers without returning the event history."""
    path = (f"{fx.namespace_path(fx.FIRST_ORG_SLUG, fx.GRADED_NAMESPACE)}"
            f"/executions/{fx.FAILED_WORKFLOW_ID}/{fx.FAILED_RUN_ID}")
    response = developer.get(path)
    assert response.status_code in fx.OK, (
        f"execution detail for {fx.FAILED_WORKFLOW_ID} returned "
        f"{response.status_code}: {response.text[:300]}"
    )
    body = response.json()
    assert isinstance(body, dict), f"execution detail is not an object: {body!r}"
    for key in ("history", "events", "event_history"):
        value = body.get(key)
        assert not (isinstance(value, list) and value), (
            f"execution detail returned the event history inline under {key!r}; "
            f"the header and summary must render without it"
        )



def test_developer_cannot_approve_own_request(developer, backend):
    """An approve call from the requesting principal is refused."""
    filed = fx.file_change_request(developer)
    request_id = fx.request_id_of(filed)
    response = fx.approve(developer, request_id)
    assert response.status_code in fx.DENIED, (
        f"a developer approving their own request returned {response.status_code}, "
        f"expected a refusal: {response.text[:300]}"
    )
    assert fx.approval_count(backend, change_request_id=request_id) == 0, (
        f"request {request_id} recorded an approval row for its own requester"
    )
    after = fx.read_request(developer, request_id)
    assert fx.state_of(after.json()) == fx.STATE_PENDING, (
        f"request {request_id} left {fx.STATE_PENDING!r} after a refused "
        f"self-approval: {after.text[:300]}"
    )


def test_owner_with_every_role_cannot_self_approve(owner, backend):
    """A principal holding every role is still refused on a self-filed request."""
    filed = fx.file_change_request(owner)
    request_id = fx.request_id_of(filed)
    response = fx.approve(owner, request_id)
    assert response.status_code in fx.DENIED, (
        f"an owner holding every role approved their own request with "
        f"{response.status_code}; separation of duty is not configurable: "
        f"{response.text[:300]}"
    )
    assert fx.approval_count(backend, change_request_id=request_id) == 0, (
        f"request {request_id} recorded a self-approval row from an owner"
    )


def test_developer_cannot_apply_approved_request(developer, namespace_admin, backend):
    """An apply call from a developer session is refused and the row is unchanged."""
    filed = fx.file_change_request(developer)
    request_id = fx.request_id_of(filed)
    approved = fx.approve(namespace_admin, request_id)
    assert approved.status_code in fx.CREATED, (
        f"approving {request_id} returned {approved.status_code}: {approved.text[:300]}"
    )
    before = fx.retention_of(fx.read_namespace(namespace_admin).json())
    response = fx.apply_request(developer, request_id)
    assert response.status_code in fx.DENIED, (
        f"a developer applying an approved request returned {response.status_code}, "
        f"expected a refusal: {response.text[:300]}"
    )
    after = fx.retention_of(fx.read_namespace(namespace_admin).json())
    assert after == before, (
        f"{fx.GRADED_NAMESPACE} retention moved from {before} to {after} on a "
        f"refused apply"
    )


def test_developer_cannot_create_namespace(developer, backend):
    """A namespace creation call from a developer session is refused."""
    name = f"probe-{fx.probe_suffix()}"
    before = fx.namespace_count(backend)
    response = developer.post(
        f"{fx.org_base(fx.FIRST_ORG_SLUG)}/namespaces",
        json={
            "name": name,
            "region": fx.SECOND_REGION,
            "retention_days": fx.PROPOSED_RETENTION_DAYS,
            "capacity_mode": fx.CAPACITY_ON_DEMAND,
        },
    )
    assert response.status_code in fx.DENIED, (
        f"a developer creating a namespace returned {response.status_code}, "
        f"expected a refusal: {response.text[:300]}"
    )
    assert fx.namespace_count(backend, name=name) == 0, (
        f"a refused creation stored a namespace row named {name!r}"
    )
    assert fx.namespace_count(backend) == before, (
        f"the stored namespace count changed on a refused creation"
    )


def test_cross_tenant_namespace_read_is_denied(developer2, backend):
    """A credential for one organisation cannot read another organisation's namespace."""
    before = backend.one("namespace", name=fx.GRADED_NAMESPACE)
    response = fx.read_namespace(developer2)
    assert response.status_code in fx.DENIED, (
        f"a {fx.SECOND_ORG} credential read {fx.GRADED_NAMESPACE} in {fx.FIRST_ORG} "
        f"with {response.status_code}: {response.text[:300]}"
    )
    after = backend.one("namespace", name=fx.GRADED_NAMESPACE)
    assert after == before, (
        f"the {fx.GRADED_NAMESPACE} row changed during a refused cross-tenant read"
    )


def test_cross_tenant_refusal_matches_missing_resource(developer2):
    """A forbidden namespace answers exactly as a namespace that does not exist."""
    forbidden = fx.read_namespace(developer2, fx.GRADED_NAMESPACE)
    missing = fx.read_namespace(developer2, fx.MISSING_NAMESPACE)
    assert forbidden.status_code == missing.status_code, (
        f"a forbidden namespace answered {forbidden.status_code} while a missing one "
        f"answered {missing.status_code}; the difference is an existence oracle"
    )
    assert fx.GRADED_NAMESPACE not in forbidden.text, (
        f"the refusal for {fx.GRADED_NAMESPACE} names the resource it refused to "
        f"reveal: {forbidden.text[:300]}"
    )


def test_unauthenticated_mutation_is_denied(anonymous, backend):
    """A mutating request carrying no credential is refused."""
    before = fx.change_request_count(backend)
    response = anonymous.post(
        fx.change_requests_path(fx.FIRST_ORG_SLUG),
        json={
            "kind": fx.REVIEWABLE_KIND,
            "subject_ref": fx.GRADED_NAMESPACE,
            "proposed": {"retention_days": fx.PROPOSED_RETENTION_DAYS},
            "reason": "anonymous probe",
        },
    )
    assert response.status_code in fx.DENIED, (
        f"an unauthenticated filing returned {response.status_code}, expected a "
        f"refusal: {response.text[:300]}"
    )
    assert fx.change_request_count(backend) == before, (
        f"an unauthenticated filing stored a change_request row"
    )


def test_expired_grant_is_denied_at_decision_time(developer):
    """The namespace covered only by an expired grant is refused at request time."""
    response = fx.read_namespace(developer, fx.SECOND_NAMESPACE)
    assert response.status_code in fx.DENIED, (
        f"reading {fx.SECOND_NAMESPACE} through an expired grant returned "
        f"{response.status_code}, expected a refusal: {response.text[:300]}"
    )


def test_explicit_deny_defeats_wider_allow_scope(namespace_admin2):
    """A namespace-scoped deny defeats an allow held at organisation scope."""
    allowed = fx.read_namespace(namespace_admin2, fx.GRADED_NAMESPACE)
    assert allowed.status_code in fx.OK, (
        f"the organisation-scope allow does not reach {fx.GRADED_NAMESPACE}: "
        f"{allowed.status_code} {allowed.text[:200]}"
    )
    denied = fx.read_namespace(namespace_admin2, fx.SECOND_NAMESPACE)
    assert denied.status_code in fx.DENIED, (
        f"the explicit deny on {fx.SECOND_NAMESPACE} did not defeat the wider allow: "
        f"{denied.status_code} {denied.text[:300]}"
    )


def test_audit_trail_read_is_owner_only(owner, developer):
    """The audit read answers an owner session and refuses a developer session."""
    permitted = owner.get(f"{fx.org_base(fx.FIRST_ORG_SLUG)}/audit")
    assert permitted.status_code in fx.OK, (
        f"an owner reading the audit trail returned {permitted.status_code}: "
        f"{permitted.text[:300]}"
    )
    refused = developer.get(f"{fx.org_base(fx.FIRST_ORG_SLUG)}/audit")
    assert refused.status_code in fx.DENIED, (
        f"a developer reading the audit trail returned {refused.status_code}, "
        f"expected a refusal: {refused.text[:300]}"
    )



def test_approved_request_applies_and_persists_retention(developer, namespace_admin,
                                                         backend):
    """An approved request applies once and the namespace reports the new retention."""
    filed = fx.file_change_request(developer)
    request_id = fx.request_id_of(filed)
    approved = fx.approve(namespace_admin, request_id)
    assert approved.status_code in fx.CREATED, (
        f"approving {request_id} returned {approved.status_code}: {approved.text[:300]}"
    )
    applied = fx.apply_request(namespace_admin, request_id)
    assert applied.status_code in fx.CREATED, (
        f"applying {request_id} returned {applied.status_code}: {applied.text[:300]}"
    )
    final = fx.poll_until(
        lambda: fx.state_of(fx.read_request(namespace_admin, request_id).json())
        == fx.STATE_APPLIED
    )
    assert final, (
        f"request {request_id} never reached {fx.STATE_APPLIED!r}: "
        f"{fx.read_request(namespace_admin, request_id).text[:300]}"
    )
    stored = backend.one("namespace", name=fx.GRADED_NAMESPACE)
    assert int(stored.get("retention_days")) == fx.PROPOSED_RETENTION_DAYS, (
        f"{fx.GRADED_NAMESPACE} retention_days is {stored.get('retention_days')!r} "
        f"in the store after an applied reduction, expected "
        f"{fx.PROPOSED_RETENTION_DAYS}"
    )
    served = fx.retention_of(fx.read_namespace(namespace_admin).json())
    assert served == fx.PROPOSED_RETENTION_DAYS, (
        f"the namespace endpoint reports retention {served}, the store holds "
        f"{stored.get('retention_days')!r}"
    )


def test_policy_reevaluated_at_apply_rejects_revoked_permission(developer,
                                                                namespace_admin,
                                                                owner, backend):
    """A filer who lost the permission after submission fails at application."""
    filed = fx.file_change_request(developer)
    request_id = fx.request_id_of(filed)
    approved = fx.approve(namespace_admin, request_id)
    assert approved.status_code in fx.CREATED, (
        f"approving {request_id} returned {approved.status_code}: {approved.text[:300]}"
    )
    before = fx.retention_of(fx.read_namespace(namespace_admin).json())
    grants = owner.get(f"{fx.org_base(fx.FIRST_ORG_SLUG)}/grants")
    assert grants.status_code in fx.OK, (
        f"an owner listing grants returned {grants.status_code}: {grants.text[:300]}"
    )
    target = None
    for row in grants.json().get("items", grants.json() if isinstance(grants.json(), list) else []):
        holder = str(row.get("subject_id", "")) + str(row.get("subject", ""))
        if fx.DEVELOPER_EMAIL in holder and fx.GRADED_NAMESPACE in str(row):
            target = row.get("id")
            break
    assert target, (
        f"no grant for {fx.DEVELOPER_EMAIL} on {fx.GRADED_NAMESPACE} is listed, so "
        f"the revocation step cannot run: {grants.text[:300]}"
    )
    revoked = owner.delete(f"{fx.org_base(fx.FIRST_ORG_SLUG)}/grants/{target}")
    assert revoked.status_code in fx.CREATED + (204,), (
        f"revoking grant {target} returned {revoked.status_code}: {revoked.text[:300]}"
    )
    applied = fx.apply_request(namespace_admin, request_id)
    body = fx.read_request(namespace_admin, request_id).json()
    assert fx.state_of(body) == fx.STATE_FAILED, (
        f"request {request_id} is {fx.state_of(body)!r} after its filer lost the "
        f"underlying permission, expected {fx.STATE_FAILED!r} "
        f"(apply answered {applied.status_code})"
    )
    assert "permission" in str(body).lower() or "grant" in str(body).lower(), (
        f"the failure reason does not name the lost permission: {body}"
    )
    after = fx.retention_of(fx.read_namespace(namespace_admin).json())
    assert after == before, (
        f"{fx.GRADED_NAMESPACE} retention moved from {before} to {after} although "
        f"application failed"
    )


def test_repeated_apply_stores_one_audit_row(developer, namespace_admin, backend):
    """A repeated application under one request identifier leaves one audit row."""
    filed = fx.file_change_request(developer)
    request_id = fx.request_id_of(filed)
    fx.approve(namespace_admin, request_id)
    key = f"apply-{fx.probe_suffix()}"
    first = fx.apply_request(namespace_admin, request_id, request_key=key)
    assert first.status_code in fx.CREATED, (
        f"the first apply returned {first.status_code}: {first.text[:300]}"
    )
    second = fx.apply_request(namespace_admin, request_id, request_key=key)
    assert second.status_code in fx.CREATED + fx.REFUSED, (
        f"a retried apply returned {second.status_code}: {second.text[:300]}"
    )
    rows = backend.count("audit_entry", resource_id=str(request_id), action="apply")
    assert rows <= 1, (
        f"a retried apply of {request_id} stored {rows} audit rows for one action; "
        f"application is idempotent on the caller-supplied request identifier"
    )


def test_concurrent_approvals_apply_exactly_once(developer, backend):
    """Two simultaneous approvals produce exactly one applied change."""
    filed = fx.file_change_request(developer)
    request_id = fx.request_id_of(filed)
    barrier = threading.Barrier(2)
    results: list[int] = []
    lock = threading.Lock()

    def approve_as(email: str) -> None:
        token = appclient.login(email, fx.CORPUS_PASSWORD)
        with appclient.client(token) as session:
            barrier.wait()
            response = fx.approve(session, request_id)
            with lock:
                results.append(response.status_code)

    threads = [
        threading.Thread(target=approve_as, args=(fx.NAMESPACE_ADMIN_EMAIL,)),
        threading.Thread(target=approve_as, args=(fx.NAMESPACE_ADMIN2_EMAIL,)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert results, "neither concurrent approval recorded a result"
    applications = backend.count("audit_entry", resource_id=str(request_id),
                                 action="apply")
    assert applications <= 1, (
        f"two concurrent approvals produced {applications} applications of "
        f"{request_id}; exactly one must win"
    )


def test_concurrent_namespace_create_stores_one_row(backend):
    """Two simultaneous creations of one name produce exactly one namespace row."""
    name = f"probe-{fx.probe_suffix()}"
    barrier = threading.Barrier(2)
    codes: list[int] = []
    lock = threading.Lock()

    def create() -> None:
        token = appclient.login(fx.NAMESPACE_ADMIN_EMAIL, fx.CORPUS_PASSWORD)
        with appclient.client(token) as session:
            barrier.wait()
            response = session.post(
                f"{fx.org_base(fx.FIRST_ORG_SLUG)}/namespaces",
                json={
                    "name": name,
                    "region": fx.SECOND_REGION,
                    "retention_days": fx.PROPOSED_RETENTION_DAYS,
                    "capacity_mode": fx.CAPACITY_ON_DEMAND,
                },
            )
            with lock:
                codes.append(response.status_code)

    threads = [threading.Thread(target=create) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    stored = backend.count("namespace", name=name)
    assert stored == 1, (
        f"two simultaneous creations of {name!r} stored {stored} rows; exactly one "
        f"must win (answers were {codes})"
    )


def test_audit_row_is_append_only(owner, backend):
    """An audit row is never observed with different content after it was written."""
    rows = backend.rows("audit_entry", limit=1)
    assert rows, "the audit trail holds no row to read"
    row = rows[0]
    row_id = row.get("id")
    listing = owner.get(f"{fx.org_base(fx.FIRST_ORG_SLUG)}/audit")
    assert listing.status_code in fx.OK, (
        f"an owner reading the audit trail returned {listing.status_code}"
    )
    mutate = owner.patch(f"{fx.org_base(fx.FIRST_ORG_SLUG)}/audit/{row_id}",
                         json={"outcome": "rewritten"})
    assert mutate.status_code in fx.REFUSED + (405,), (
        f"an audit row accepted an update with {mutate.status_code}; the trail is "
        f"append-only: {mutate.text[:300]}"
    )
    remove = owner.delete(f"{fx.org_base(fx.FIRST_ORG_SLUG)}/audit/{row_id}")
    assert remove.status_code in fx.REFUSED + (405,), (
        f"an audit row accepted a delete with {remove.status_code}; the trail is "
        f"append-only: {remove.text[:300]}"
    )
    again = backend.one("audit_entry", id=row_id)
    assert again == row, (
        f"audit row {row_id} reads differently after a refused update"
    )


def test_audit_rows_chain_to_the_previous_row(backend):
    """Each audit row carries the hash of the previous row for its organisation."""
    rows = backend.query(
        "SELECT id, organisation_id, prev_hash, hash FROM audit_entry "
        "ORDER BY organisation_id, occurred_at, id"
    )
    assert len(rows) >= 2, (
        f"the audit trail holds {len(rows)} row(s); the chain needs at least two"
    )
    by_org: dict = {}
    for row in rows:
        by_org.setdefault(row["organisation_id"], []).append(row)
    checked = 0
    for org, chain in by_org.items():
        for earlier, later in zip(chain, chain[1:]):
            assert later["prev_hash"] == earlier["hash"], (
                f"audit row {later['id']} in organisation {org} carries prev_hash "
                f"{later['prev_hash']!r}, but the row before it hashes to "
                f"{earlier['hash']!r}"
            )
            checked += 1
    assert checked >= 1, "no organisation holds two audit rows to chain"


def test_denied_attempt_is_recorded_in_audit(developer, backend):
    """A refused attempt appears in the audit trail with a denied outcome."""
    before = backend.count("audit_entry")
    refused = developer.post(
        f"{fx.org_base(fx.FIRST_ORG_SLUG)}/namespaces",
        json={
            "name": f"probe-{fx.probe_suffix()}",
            "region": fx.SECOND_REGION,
            "retention_days": fx.PROPOSED_RETENTION_DAYS,
            "capacity_mode": fx.CAPACITY_ON_DEMAND,
        },
    )
    assert refused.status_code in fx.DENIED, (
        f"the probe call was not refused: {refused.status_code}"
    )
    grew = fx.poll_until(lambda: backend.count("audit_entry") > before)
    assert grew, (
        f"a refused attempt wrote no audit row; the count stayed at {before}. The "
        f"entries an intrusion generates are precisely the refused ones"
    )
    denied_rows = backend.query(
        "SELECT count(*) AS n FROM audit_entry WHERE outcome ILIKE %s", ("%deni%",)
    )
    assert denied_rows[0]["n"] >= 1, (
        "no audit row records a denied outcome"
    )


def test_execution_status_survives_reload_from_history(developer):
    """An execution status is recomputed from its event history on a fresh read."""
    path = (f"{fx.namespace_path(fx.FIRST_ORG_SLUG, fx.GRADED_NAMESPACE)}"
            f"/executions/{fx.FAILED_WORKFLOW_ID}/{fx.FAILED_RUN_ID}")
    first = developer.get(path)
    assert first.status_code in fx.OK, (
        f"execution detail returned {first.status_code}: {first.text[:300]}"
    )
    second = developer.get(path)
    assert second.status_code in fx.OK, (
        f"a second read of the execution detail returned {second.status_code}"
    )
    first_status = str(first.json().get("status"))
    second_status = str(second.json().get("status"))
    assert first_status == second_status, (
        f"the execution status changed between two reads, {first_status!r} then "
        f"{second_status!r}; a projection of an append-only history is stable"
    )
    history = developer.get(f"{path}/history")
    assert history.status_code in fx.OK, (
        f"the event history returned {history.status_code}: {history.text[:300]}"
    )
    events = history.json().get("items", [])
    assert events, f"the seeded failed execution returned no events: {history.text[:300]}"



def test_history_pages_by_cursor_without_duplicates(developer):
    """Paging the event history by cursor repeats no event and skips none."""
    base = (f"{fx.namespace_path(fx.FIRST_ORG_SLUG, fx.GRADED_NAMESPACE)}"
            f"/executions/{fx.FAILED_WORKFLOW_ID}/{fx.FAILED_RUN_ID}/history")
    first = developer.get(base, params={"limit": 10})
    assert first.status_code in fx.OK, (
        f"the first history page returned {first.status_code}: {first.text[:300]}"
    )
    first_body = first.json()
    cursor = first_body.get("next_cursor")
    assert cursor, (
        f"the first history page carries no next_cursor, so the table cannot page "
        f"by cursor: {first.text[:300]}"
    )
    second = developer.get(base, params={"limit": 10, "cursor": cursor})
    assert second.status_code in fx.OK, (
        f"the second history page returned {second.status_code}: {second.text[:300]}"
    )
    first_ids = [event.get("event_id") for event in first_body.get("items", [])]
    second_ids = [event.get("event_id") for event in second.json().get("items", [])]
    assert first_ids, "the first history page is empty"
    assert second_ids, "the second history page is empty"
    overlap = set(first_ids) & set(second_ids)
    assert not overlap, (
        f"cursor paging repeated event id(s) {sorted(overlap)} across two pages"
    )
    assert max(first_ids) < min(second_ids), (
        f"the second page does not continue the first: page one ends at "
        f"{max(first_ids)}, page two starts at {min(second_ids)}"
    )


def test_cursor_from_another_sort_is_refused(developer):
    """A cursor minted under one sort is refused by a differently sorted query."""
    base = f"{fx.namespace_path(fx.FIRST_ORG_SLUG, fx.GRADED_NAMESPACE)}/executions"
    ascending = developer.get(base, params={"limit": 2, "sort": "start_time:asc"})
    assert ascending.status_code in fx.OK, (
        f"the ascending execution page returned {ascending.status_code}: "
        f"{ascending.text[:300]}"
    )
    cursor = ascending.json().get("next_cursor")
    assert cursor, (
        f"the execution list carries no next_cursor: {ascending.text[:300]}"
    )
    reused = developer.get(base, params={"limit": 2, "sort": "start_time:desc",
                                         "cursor": cursor})
    assert reused.status_code in fx.REFUSED, (
        f"a cursor from the ascending sort was accepted by the descending query with "
        f"{reused.status_code}; a stale cursor must be refused rather than "
        f"reinterpreted: {reused.text[:300]}"
    )


def test_invalid_namespace_create_stores_nothing(namespace_admin, backend):
    """A namespace creation that fails validation leaves no row behind."""
    before = fx.namespace_count(backend)
    response = namespace_admin.post(
        f"{fx.org_base(fx.FIRST_ORG_SLUG)}/namespaces",
        json={
            "name": "",
            "region": "nowhere-central-9",
            "retention_days": -1,
            "capacity_mode": "unlimited",
        },
    )
    assert response.status_code in fx.REFUSED, (
        f"an invalid creation returned {response.status_code}, expected a client "
        f"error: {response.text[:300]}"
    )
    assert response.status_code < 500, (
        f"an invalid creation answered {response.status_code}, a server error"
    )
    assert fx.namespace_count(backend) == before, (
        f"the stored namespace count moved from {before} on a refused creation"
    )


def test_expired_request_cannot_be_applied(namespace_admin, backend):
    """An expired change request is refused at application."""
    rows = backend.rows("change_request", state=fx.STATE_EXPIRED, limit=1)
    if not rows:
        rows = backend.query(
            "SELECT * FROM change_request WHERE expires_at < now() "
            "AND state <> %s ORDER BY id LIMIT 1", (fx.STATE_APPLIED,)
        )
    assert rows, (
        "no expired or past-expiry change request exists to apply, so the expiry "
        "rule cannot be observed"
    )
    request_id = str(rows[0].get("id"))
    response = fx.apply_request(namespace_admin, request_id)
    assert response.status_code in fx.REFUSED, (
        f"applying an expired request returned {response.status_code}, expected a "
        f"refusal: {response.text[:300]}"
    )
    body = fx.read_request(namespace_admin, request_id)
    if body.status_code in fx.OK:
        assert fx.state_of(body.json()) != fx.STATE_APPLIED, (
            f"an expired request reached {fx.STATE_APPLIED!r}"
        )


def test_rate_limit_answer_differs_from_validation(developer):
    """An exceeded rate limit is answered distinctly from a validation failure."""
    path = f"{fx.namespace_path(fx.FIRST_ORG_SLUG, fx.GRADED_NAMESPACE)}/executions"
    codes = []
    for _ in range(40):
        response = developer.get(path, params={"limit": 1})
        codes.append(response.status_code)
        if response.status_code == 429:
            assert response.headers.get("retry-after") or "retry" in response.text.lower(), (
                f"the rate-limited answer carries no retry hint: "
                f"{dict(response.headers)} {response.text[:200]}"
            )
            break
    invalid = developer.get(path, params={"limit": "not-a-number"})
    assert invalid.status_code in fx.REFUSED, (
        f"an invalid query answered {invalid.status_code}, expected a client error"
    )
    if 429 in codes:
        assert invalid.status_code != 429, (
            "a validation failure answers with the rate-limit code, so a client "
            "cannot tell a bad request from a limit"
        )
    else:
        assert all(code < 500 for code in codes), (
            f"the execution list answered a server error under repeated reads: {codes}"
        )



def test_privacy_page_is_linked_from_every_footer(public):
    """A privacy page is reachable from the footer of every public page."""
    privacy = public.get("/privacy")
    assert privacy.status_code == 200, (
        f"GET /privacy returned {privacy.status_code}: {privacy.text[:200]}"
    )
    for route in ("/", "/product", "/pricing", "/security", "/get-cloud"):
        page = public.get(route)
        assert page.status_code == 200, (
            f"GET {route} returned {page.status_code}"
        )
        assert "/privacy" in page.text, (
            f"{route} carries no link to /privacy in its markup, so the privacy page "
            f"is unreachable from that page's footer"
        )


def test_sitemap_lists_every_public_route(public):
    """The sitemap lists every public route the build serves."""
    response = public.get("/sitemap.xml")
    assert response.status_code == 200, (
        f"GET /sitemap.xml returned {response.status_code}: {response.text[:200]}"
    )
    body = response.text
    for route in ("/product", "/pricing", "/security", "/privacy", "/get-cloud"):
        assert route in body, f"the sitemap omits the public route {route}"


def test_robots_refers_to_the_sitemap(public):
    """The robots file refers to the sitemap."""
    response = public.get("/robots.txt")
    assert response.status_code == 200, (
        f"GET /robots.txt returned {response.status_code}: {response.text[:200]}"
    )
    assert "sitemap" in response.text.lower(), (
        f"/robots.txt carries no sitemap reference: {response.text[:200]}"
    )


def test_favicon_is_declared_in_the_document_head(public):
    """The site serves a favicon and declares it in the document head."""
    home = public.get("/")
    assert home.status_code == 200, f"GET / returned {home.status_code}"
    assert "icon" in home.text.lower(), (
        f"the document head declares no favicon link: {home.text[:400]}"
    )
    for candidate in ("/favicon.ico", "/favicon.svg", "/favicon.png"):
        served = public.get(candidate)
        if served.status_code == 200:
            return
    raise AssertionError(
        "no favicon is served at /favicon.ico, /favicon.svg or /favicon.png"
    )


def test_invalid_form_submission_is_refused_inline(public):
    """An invalid enquiry is refused as a client error and writes nothing."""
    response = public.post("/api/enquiries",
                           json={"email": "not-an-address",
                                 "organisation_name": "",
                                 "region": "nowhere-central-9"})
    assert response.status_code in fx.REFUSED, (
        f"an invalid enquiry returned {response.status_code}, expected a client "
        f"error: {response.text[:300]}"
    )
    assert response.status_code < 500, (
        f"an invalid enquiry answered {response.status_code}, a server error"
    )
    listed = public.get("/api/enquiries")
    if listed.status_code == 200:
        assert "nowhere-central-9" not in listed.text, (
            "the refused enquiry was stored anyway and is listed back"
        )



def test_principal_kinds_are_modelled_separately(backend):
    """A principal is its own row, distinct from the person it may point at."""
    kinds = backend.query("SELECT DISTINCT kind FROM principal")
    assert kinds, "the principal table holds no row"
    seen = {str(row["kind"]) for row in kinds}
    assert "person" in seen, (
        f"the principal table records no person kind, only {sorted(seen)}; a "
        f"service account squeezed into a person row is the defect this separation "
        f"exists to prevent"
    )
    people = backend.count("person")
    principals = backend.count("principal")
    assert principals >= people, (
        f"there are {principals} principal row(s) for {people} person row(s); every "
        f"person acts through a principal"
    )


def test_person_email_is_unique_case_folded(namespace_admin, backend):
    """A person cannot be added at an address that already exists in another case."""
    existing = fx.DEVELOPER_EMAIL.upper()
    before = backend.count("person")
    response = namespace_admin.post(
        f"{fx.org_base(fx.FIRST_ORG_SLUG)}/members",
        json={"email": existing, "roles": [fx.ROLE_DEVELOPER]},
    )
    assert response.status_code in fx.REFUSED, (
        f"adding {existing} returned {response.status_code}; the address already "
        f"belongs to this organisation in a different case: {response.text[:300]}"
    )
    assert backend.count("person") == before, (
        f"a refused invitation stored a person row; the count moved from {before}"
    )


def test_invitation_to_existing_member_is_refused(namespace_admin, backend):
    """An invitation to an address already in the organisation is refused."""
    before = backend.count("invitation")
    response = namespace_admin.post(
        f"{fx.org_base(fx.FIRST_ORG_SLUG)}/members",
        json={"email": fx.NAMESPACE_ADMIN2_EMAIL, "roles": [fx.ROLE_DEVELOPER]},
    )
    assert response.status_code in fx.REFUSED, (
        f"inviting an existing member returned {response.status_code}, expected a "
        f"refusal naming the existing membership: {response.text[:300]}"
    )
    assert backend.count("invitation") == before, (
        "a refused invitation stored an invitation row"
    )


def test_removing_a_person_revokes_grants_and_keeps_audit(owner, backend):
    """Removing a person revokes the grants held and leaves the audit rows intact."""
    audit_before = backend.count("audit_entry")
    members = owner.get(f"{fx.org_base(fx.FIRST_ORG_SLUG)}/members")
    assert members.status_code in fx.OK, (
        f"listing members returned {members.status_code}: {members.text[:300]}"
    )
    target = None
    for row in members.json().get("items", []):
        if str(row.get("email")) == fx.DEVELOPER_EMAIL:
            target = row.get("id") or row.get("principal_id")
            break
    assert target, (
        f"the members list does not name {fx.DEVELOPER_EMAIL}: {members.text[:300]}"
    )
    removed = owner.delete(f"{fx.org_base(fx.FIRST_ORG_SLUG)}/members/{target}")
    assert removed.status_code in fx.CREATED + (204,) + fx.REFUSED, (
        f"removing a member returned {removed.status_code}: {removed.text[:300]}"
    )
    if removed.status_code in fx.CREATED + (204,):
        assert backend.count("audit_entry") >= audit_before, (
            f"removing a person reduced the audit row count from {audit_before}; a "
            f"record that disappears with the person is not a record"
        )


def test_last_owner_cannot_be_removed(owner, backend):
    """The last owner of an organisation is refused removal by the server."""
    owner_grants = backend.query(
        "SELECT g.id FROM grant g JOIN role r ON r.id = g.role_id "
        "WHERE r.name = %s AND g.effect = %s", (fx.ROLE_OWNER, "allow")
    )
    assert owner_grants, "no owner grant exists to reason about"
    members = owner.get(f"{fx.org_base(fx.FIRST_ORG_SLUG)}/members")
    assert members.status_code in fx.OK, (
        f"listing members returned {members.status_code}"
    )
    target = None
    for row in members.json().get("items", []):
        if str(row.get("email")) == fx.OWNER_EMAIL:
            target = row.get("id") or row.get("principal_id")
            break
    assert target, f"the members list does not name {fx.OWNER_EMAIL}"
    if len(owner_grants) <= 1:
        response = owner.delete(f"{fx.org_base(fx.FIRST_ORG_SLUG)}/members/{target}")
        assert response.status_code in fx.REFUSED, (
            f"the last owner was removed with {response.status_code}; the server "
            f"refuses this independently of the console: {response.text[:300]}"
        )


def test_directory_group_membership_is_read_only(namespace_admin, backend):
    """A directory-provisioned group refuses a membership edit in the console."""
    groups = backend.rows("group", source="directory", limit=1)
    if not groups:
        namespace_admin.post(
            f"{fx.org_base(fx.FIRST_ORG_SLUG)}/groups",
            json={"name": f"probe-{fx.probe_suffix()}", "source": "directory"},
        )
        groups = backend.rows("group", source="directory", limit=1)
    assert groups, (
        "no directory-provisioned group exists, so the read-only rule cannot be "
        "observed"
    )
    group_id = groups[0].get("id")
    response = namespace_admin.post(
        f"{fx.org_base(fx.FIRST_ORG_SLUG)}/groups/{group_id}/members",
        json={"email": fx.DEVELOPER_EMAIL},
    )
    assert response.status_code in fx.REFUSED, (
        f"the console added a member to a synchronised group with "
        f"{response.status_code}; the next synchronisation would destroy that edit: "
        f"{response.text[:300]}"
    )


def test_sso_enforcement_without_verified_domain_is_refused(owner, backend):
    """Sign-on enforcement is refused while no verified domain exists."""
    verified = backend.count("verified_domain")
    response = owner.patch(
        f"{fx.org_base(fx.FIRST_ORG_SLUG)}/identity",
        json={"enforced": True},
    )
    if verified == 0:
        assert response.status_code in fx.REFUSED, (
            f"enforcement was enabled with {response.status_code} while no domain is "
            f"verified; an unverified claim lets an organisation capture accounts at "
            f"a company it does not own: {response.text[:300]}"
        )
    else:
        assert response.status_code < 500, (
            f"the enforcement switch answered a server error: {response.status_code}"
        )



def test_certificate_bundle_overlap_is_accepted(namespace_admin, backend):
    """A trust bundle rotation accepts the old entry beside the new one."""
    path = f"{fx.namespace_path(fx.FIRST_ORG_SLUG, fx.GRADED_NAMESPACE)}/trust-bundle"
    before = backend.count("trust_bundle_entry")
    response = namespace_admin.post(
        path,
        json={"subject": f"CN=probe-{fx.probe_suffix()}",
              "fingerprint": fx.probe_suffix()},
    )
    assert response.status_code in fx.CREATED + fx.REFUSED, (
        f"adding a trust bundle entry returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    if response.status_code in fx.CREATED:
        after = backend.count("trust_bundle_entry")
        assert after > before, (
            f"the added trust bundle entry stored no row; the count stayed at {before}"
        )
        listing = namespace_admin.get(path)
        assert listing.status_code in fx.OK, (
            f"reading the trust bundle returned {listing.status_code}"
        )
        entries = listing.json().get("items", [])
        assert len(entries) >= 2, (
            f"the bundle holds {len(entries)} entry after a rotation; a hard cutover "
            f"disconnects every worker at once, so both entries stay valid across the "
            f"overlap window"
        )


def test_namespace_replication_reports_lag_per_standby(namespace_admin, backend):
    """A replicated namespace reports its primary, its standbys and the lag."""
    replicas = backend.count("namespace_replica")
    response = fx.read_namespace(namespace_admin)
    assert response.status_code in fx.OK, (
        f"reading {fx.GRADED_NAMESPACE} returned {response.status_code}"
    )
    assert "region" in response.json(), (
        f"the namespace body names no region: {response.text[:300]}"
    )
    if replicas:
        rows = backend.query(
            "SELECT role, lag_seconds_observed_at FROM namespace_replica"
        )
        roles = {str(row["role"]) for row in rows}
        assert "primary" in roles, (
            f"a replicated namespace records no primary region, only {sorted(roles)}"
        )
        assert any(row["lag_seconds_observed_at"] is not None for row in rows), (
            "no standby records an observed replication lag, so an operator cannot "
            "see the loss a failover would accept"
        )


def test_search_attribute_types_are_the_declared_set(namespace_admin, backend):
    """Every declared search attribute carries a type from the closed set."""
    legal = {"keyword", "text", "integer", "double", "boolean", "datetime",
             "keyword_list"}
    rows = backend.query("SELECT name, type FROM search_attribute")
    assert rows, "no search attribute is declared on any namespace"
    for row in rows:
        assert str(row["type"]) in legal, (
            f"search attribute {row['name']!r} carries type {row['type']!r}, outside "
            f"the declared set {sorted(legal)}"
        )
    refused = namespace_admin.post(
        f"{fx.namespace_path(fx.FIRST_ORG_SLUG, fx.GRADED_NAMESPACE)}"
        f"/search-attributes",
        json={"name": f"probe_{fx.probe_suffix()}", "type": "geo_point"},
    )
    assert refused.status_code in fx.REFUSED, (
        f"declaring a search attribute of an unknown type returned "
        f"{refused.status_code}: {refused.text[:300]}"
    )


def test_worker_fleet_marks_a_stale_poller_unreachable(developer, backend):
    """A worker that stopped polling is marked unreachable rather than deleted."""
    stored = backend.count("worker")
    assert stored >= 2, (
        f"the fleet holds {stored} worker row(s); the seed carries one recent poller "
        f"beside one stale one"
    )
    response = developer.get(
        f"{fx.namespace_path(fx.FIRST_ORG_SLUG, fx.GRADED_NAMESPACE)}/workers"
    )
    assert response.status_code in fx.OK, (
        f"reading the worker fleet returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    items = response.json().get("items", [])
    assert len(items) >= 2, (
        f"the fleet endpoint returned {len(items)} worker(s) for {stored} stored "
        f"rows; a worker that stopped polling stays listed"
    )
    states = {str(row.get("state", "")).lower() for row in items}
    assert any("unreach" in state or "stale" in state or "offline" in state
               for state in states), (
        f"no listed worker is marked unreachable, although one seeded worker last "
        f"polled outside the window: states were {sorted(states)}"
    )


def test_trust_bundle_expiry_is_surfaced(namespace_admin, backend):
    """A certificate approaching expiry is surfaced with its expiry date."""
    rows = backend.query(
        "SELECT subject, not_after FROM trust_bundle_entry ORDER BY not_after"
    )
    assert rows, "no trust bundle entry is stored"
    response = namespace_admin.get(
        f"{fx.namespace_path(fx.FIRST_ORG_SLUG, fx.GRADED_NAMESPACE)}/trust-bundle"
    )
    assert response.status_code in fx.OK, (
        f"reading the trust bundle returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    body = response.text.lower()
    assert "expir" in body or "not_after" in body, (
        f"the trust bundle view names no expiry for any entry, so an operator cannot "
        f"see a certificate about to lapse: {response.text[:300]}"
    )


def test_task_queue_backlog_is_reported(developer, backend):
    """Each task queue reports its backlog so piling work is visible."""
    stored = backend.count("task_queue")
    assert stored >= 2, (
        f"the seed holds {stored} task queue row(s), expected at least two"
    )
    response = developer.get(
        f"{fx.namespace_path(fx.FIRST_ORG_SLUG, fx.GRADED_NAMESPACE)}/task-queues"
    )
    assert response.status_code in fx.OK, (
        f"reading the task queues returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    body = response.json()
    rows = body if isinstance(body, list) else body.get("items", [])
    assert rows, f"the task queue endpoint returned nothing: {response.text[:300]}"
    names = {str(row.get("name")) for row in rows}
    assert fx.GRADED_TASK_QUEUE in names, (
        f"the seeded task queue {fx.GRADED_TASK_QUEUE} is absent from {sorted(names)}"
    )
    assert any("backlog" in str(row).lower() or "depth" in str(row).lower()
               for row in rows), (
        f"no task queue reports a backlog: {response.text[:300]}"
    )


def test_security_headers_are_present(public):
    """Every response carries the standard security headers and leaks no secret."""
    for route in ("/", "/privacy", "/api/health"):
        response = public.get(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}"
        )
        headers = {k.lower(): v for k, v in response.headers.items()}
        assert "strict-transport-security" in headers, (
            f"{route} carries no strict transport policy: {sorted(headers)}"
        )
        nosniff = headers.get("x-content-type-options", "").lower()
        assert nosniff == "nosniff", (
            f"{route} carries x-content-type-options {nosniff!r}, expected nosniff"
        )
    home = public.get("/")
    lowered = home.text.lower()
    for secret in ("deku-local-dev", "auth_admin_token", "db_admin_url"):
        assert secret not in lowered, (
            f"the home document leaks {secret!r} to the browser"
        )


def test_first_paint_carries_an_application_shell(public):
    """The first response is an application shell rather than a rendered route."""
    home = public.get("/")
    assert home.status_code == 200, f"GET / returned {home.status_code}"
    assert "<script" in home.text.lower(), (
        "the first response references no script, so the browser receives no "
        "application shell to compose the route with"
    )
    lowered = home.text.lower()
    for element in ("<video", "<audio", "<img "):
        assert element not in lowered, (
            f"the home document references {element!r}; the demonstrator and the "
            f"page are drawn rather than fetched as media"
        )
    console = public.get("/o/northwind/requests")
    assert console.status_code in (200, 401, 403, 404), (
        f"a console route answered {console.status_code} to an anonymous fetch"
    )
    if console.status_code == 200:
        assert "reduce_retention" not in console.text, (
            "the anonymous first response already carries signed-in route content; "
            "the shell must compose the screen in the browser from the API"
        )


def test_placeholder_customer_marks_are_used(public):
    """The customer logo band carries the placeholder marks, never a real name."""
    home = public.get("/")
    assert home.status_code == 200, f"GET / returned {home.status_code}"
    marks = ("Northwind", "Vanta Bank", "Skyward", "Forgelab", "Sendwise",
             "Cascade Air", "Braddock", "Larkspur", "Kestrel Pay", "Orbis")
    found = [mark for mark in marks if mark in home.text]
    assert len(found) >= 4, (
        f"the customer logo band names only {found} of the pinned placeholder "
        f"marks; every customer mark in this build is a placeholder, so at least "
        f"the band's own names must appear"
    )
