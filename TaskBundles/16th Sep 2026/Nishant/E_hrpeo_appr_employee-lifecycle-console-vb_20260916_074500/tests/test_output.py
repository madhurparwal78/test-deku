"""The one merged pytest module for deku/employee-lifecycle-console-vb.

Every assertion is black box: HTTP against the deployed app and rows through
the generic backend adapter. Nothing here reads the agent's source, imports a
provider SDK, or assumes a framework.
"""

from __future__ import annotations

import base64
import concurrent.futures
import json

import httpx
from appclient import client, login
from conftest import (
    ANNUAL_ACCRUAL_HALVES,
    ANNUAL_BALANCE_HALVES,
    ANNUAL_NOTICE_DAYS,
    CALENDAR_KA,
    CLOSED_PERIODS,
    CORPUS_PASSWORD,
    CURRENCY,
    CURSOR_HEADER,
    DENIED,
    DENIED_OR_MISSING,
    EMPLOYEE2_EMAIL,
    EMPLOYEE_EMAIL,
    EMP_1001,
    EMP_1002,
    EMP_1003,
    EMP_1004,
    ESCALATED_CLAIM_MINOR,
    expected_issuer,
    GROSS_1001,
    GROSS_1002,
    FRESH_PERIOD,
    GROUP_CORE,
    HOLIDAY_DATE,
    LEAVE_FROM,
    LEAVE_HALVES,
    LEAVE_TO,
    MANAGER_CLAIM_LIMIT_MINOR,
    MANAGER_EMAIL,
    MGR_2001,
    MGR_2002,
    NAME_1001,
    NET_1001,
    NET_1002,
    OK,
    OPEN_PERIOD,
    PAGE_SIZE,
    PAYROLL_EMAIL,
    POLICY_ANNUAL,
    RECEIPT_THRESHOLD_MINOR,
    REFUSED,
    REFUSED_OR_DENIED,
    RULE_SET_CODE,
    RULE_SET_VERSION,
    RUN_HEADCOUNT,
    RUN_TOTAL_DEDUCTIONS,
    RUN_TOTAL_GROSS,
    RUN_TOTAL_NET,
    SECRET_MARKERS,
    SEEDED_ATTENDANCE_DAYS,
    SEEDED_EMPLOYEE_COUNT,
    STATUTORY_CODES,
    api,
    app_origin,
    new_punch,
    open_run_row,
    pending_approval_for,
    poll_until,
    settle,
    unique_suffix,
)



def test_health_endpoint_requires_no_credential(anon_client):
    r = anon_client.get(api("/health"))
    assert r.status_code == 200, (
        f"GET /api/health answered {r.status_code} without a credential; the App "
        f"Contract requires 200 once the app is ready. Body: {r.text[:200]!r}"
    )


def test_login_returns_bearer_token_for_seeded_manager(anon_client):
    r = anon_client.post(api("/auth/login"),
                         json={"email": MANAGER_EMAIL, "password": CORPUS_PASSWORD})
    assert r.status_code in OK, (
        f"POST /api/auth/login as {MANAGER_EMAIL} with the pinned corpus password "
        f"answered {r.status_code}, body {r.text[:200]!r}"
    )
    body = r.json()
    assert body.get("access_token"), (
        f"the sign-in response carries no non-empty `access_token` field: "
        f"keys {sorted(body)}"
    )


def test_me_reports_the_callers_own_employee_number(manager_client):
    r = manager_client.get(api("/me"))
    assert r.status_code in OK, (
        f"GET /api/me as {MANAGER_EMAIL} answered {r.status_code}, "
        f"body {r.text[:200]!r}"
    )
    body = r.json()
    assert body.get("employee_number") == MGR_2001, (
        f"GET /api/me resolved the caller to {body.get('employee_number')!r}; the "
        f"seeded manager {MANAGER_EMAIL} is {MGR_2001!r}. Body: {r.text[:200]!r}"
    )


def test_leave_request_days_exclude_holiday_and_weekend(employee_client, console):
    before = console.count_leave_requests(employee_number=EMP_1001)
    r = employee_client.post(api("/leave-requests"), json={
        "policy_code": POLICY_ANNUAL, "from_date": LEAVE_FROM, "to_date": LEAVE_TO,
        "half_day": False, "reason": f"probe {unique_suffix()}"})
    assert r.status_code in OK, (
        f"POST /api/leave-requests for {LEAVE_FROM}..{LEAVE_TO} answered "
        f"{r.status_code}, body {r.text[:300]!r}"
    )
    body = r.json()
    assert int(body.get("halves", -1)) == LEAVE_HALVES, (
        f"the request from {LEAVE_FROM} to {LEAVE_TO} under calendar {CALENDAR_KA} "
        f"reported {body.get('halves')!r} halves; the holiday {HOLIDAY_DATE} and the "
        f"weekend must be excluded, which leaves {LEAVE_HALVES}. Body: {r.text[:300]!r}"
    )
    after = console.count_leave_requests(employee_number=EMP_1001)
    assert after == before + 1, (
        f"an accepted leave request moved the leave_request row count for "
        f"{EMP_1001} from {before} to {after}; exactly one row must be written"
    )


def test_request_breaching_minimum_notice_writes_no_row(employee_client, console):
    before = console.count_leave_requests(employee_number=EMP_1001)
    r = employee_client.post(api("/leave-requests"), json={
        "policy_code": POLICY_ANNUAL, "from_date": "2026-07-02",
        "to_date": "2026-07-02", "half_day": False,
        "reason": f"probe {unique_suffix()}"})
    assert r.status_code in REFUSED, (
        f"a leave request inside the {ANNUAL_NOTICE_DAYS}-day notice window answered "
        f"{r.status_code}; it must be refused as invalid. Body: {r.text[:300]!r}"
    )
    after = console.count_leave_requests(employee_number=EMP_1001)
    assert after == before, (
        f"a refused leave request still moved the leave_request row count for "
        f"{EMP_1001} from {before} to {after}; a refusal writes no row"
    )


def test_overlapping_leave_request_is_refused(employee_client, console):
    first = employee_client.post(api("/leave-requests"), json={
        "policy_code": POLICY_ANNUAL, "from_date": "2026-09-14",
        "to_date": "2026-09-16", "half_day": False,
        "reason": f"probe {unique_suffix()}"})
    assert first.status_code in OK, (
        f"the first leave request for 2026-09-14..2026-09-16 answered "
        f"{first.status_code}, body {first.text[:300]!r}"
    )
    before = console.count_leave_requests(employee_number=EMP_1001)
    second = employee_client.post(api("/leave-requests"), json={
        "policy_code": POLICY_ANNUAL, "from_date": "2026-09-15",
        "to_date": "2026-09-17", "half_day": False,
        "reason": f"probe {unique_suffix()}"})
    assert second.status_code in REFUSED, (
        f"a leave request overlapping 2026-09-15 for {EMP_1001} answered "
        f"{second.status_code}; an overlap must be refused as invalid. "
        f"Body: {second.text[:300]!r}"
    )
    after = console.count_leave_requests(employee_number=EMP_1001)
    assert after == before, (
        f"a refused overlapping request moved the leave_request row count from "
        f"{before} to {after}; a refusal writes no row"
    )


def test_claim_without_receipt_above_threshold_is_refused(employee_client, console):
    before = console.count_claims(employee_number=EMP_1001)
    r = employee_client.post(api("/claims"), json={
        "category": "TRAVEL", "amount_minor": RECEIPT_THRESHOLD_MINOR + 100000,
        "currency": CURRENCY, "spent_on": "2026-07-04", "receipt_ref": None})
    assert r.status_code in REFUSED, (
        f"a claim of {RECEIPT_THRESHOLD_MINOR + 100000} minor units with no receipt "
        f"reference answered {r.status_code}; above {RECEIPT_THRESHOLD_MINOR} a "
        f"receipt is required. Body: {r.text[:300]!r}"
    )
    after = console.count_claims(employee_number=EMP_1001)
    assert after == before, (
        f"a refused claim moved the claim row count for {EMP_1001} from {before} "
        f"to {after}; a refusal writes no row"
    )


def test_claim_above_manager_limit_escalates_to_payroll(employee_client):
    r = employee_client.post(api("/claims"), json={
        "category": "EQUIPMENT", "amount_minor": ESCALATED_CLAIM_MINOR,
        "currency": CURRENCY, "spent_on": "2026-07-06",
        "receipt_ref": f"RCPT-{unique_suffix()}"})
    assert r.status_code in OK, (
        f"POST /api/claims for {ESCALATED_CLAIM_MINOR} minor units answered "
        f"{r.status_code}, body {r.text[:300]!r}"
    )
    body = r.json()
    assert body.get("decided_by_role") == "payroll", (
        f"a claim of {ESCALATED_CLAIM_MINOR} minor units is above the manager limit "
        f"of {MANAGER_CLAIM_LIMIT_MINOR} and must escalate, so the submission "
        f"response must name `payroll` as the deciding role; it named "
        f"{body.get('decided_by_role')!r}. Body: {r.text[:300]!r}"
    )


def test_unpaired_punch_surfaces_as_its_own_status(console, manager_client):
    days = console.attendance_days(EMP_1001)
    assert days, f"no attendance_day rows exist for {EMP_1001}"
    statuses = [str(row.get("status")) for row in days]
    assert "unpaired" in statuses, (
        f"the seeded July attendance for the core group carries four unpaired days, "
        f"so at least one attendance_day row must carry the status `unpaired`. "
        f"Seen: {sorted(set(statuses))}"
    )
    served = manager_client.get(api("/attendance/days"),
                                params={"employee_number": EMP_1001,
                                        "month": OPEN_PERIOD})
    assert served.status_code in OK, (
        f"GET /api/attendance/days for {EMP_1001} answered {served.status_code}, "
        f"body {served.text[:300]!r}"
    )
    rows = served.json()
    assert isinstance(rows, list) and rows, (
        f"GET /api/attendance/days must return a non-empty top-level array; got "
        f"{served.text[:300]!r}"
    )
    for row in rows:
        assert str(row.get("status")) in ("present", "half_day", "absent",
                                          "weekly_off", "holiday", "on_leave",
                                          "unpaired"), (
            f"a served attendance day carries the status {row.get('status')!r}, which "
            f"is not one of the seven named statuses"
        )
        assert "worked_minutes" in row, (
            f"a served attendance day carries no worked_minutes; the day is computed "
            f"on the server rather than in the browser. Keys: {sorted(row)}"
        )


def test_second_decision_on_a_decided_request_is_refused(employee2_client,
                                                         manager_client, console):
    created = employee2_client.post(api("/leave-requests"), json={
        "policy_code": POLICY_ANNUAL, "from_date": "2026-10-05",
        "to_date": "2026-10-06", "half_day": False,
        "reason": f"probe {unique_suffix()}"})
    assert created.status_code in OK, (
        f"POST /api/leave-requests as {EMPLOYEE2_EMAIL} answered "
        f"{created.status_code}, body {created.text[:300]!r}"
    )
    approval_id = created.json().get("approval_id")
    assert approval_id, (
        f"the leave-request response carries no `approval_id`: "
        f"{created.text[:300]!r}"
    )
    first = manager_client.post(api(f"/approvals/{approval_id}/decide"),
                                json={"decision": "approved", "reason": "ok"})
    assert first.status_code in OK, (
        f"the first decision on approval {approval_id} answered {first.status_code}, "
        f"body {first.text[:300]!r}"
    )
    second = manager_client.post(api(f"/approvals/{approval_id}/decide"),
                                 json={"decision": "rejected", "reason": "again"})
    assert second.status_code in REFUSED, (
        f"a second decision on the already decided approval {approval_id} answered "
        f"{second.status_code}; it must be refused. Body: {second.text[:300]!r}"
    )
    row = console.approval(approval_id)
    assert row is not None, f"approval {approval_id} is missing from the approval table"
    assert str(row.get("state")) == "approved", (
        f"the refused second decision changed approval {approval_id} to state "
        f"{row.get('state')!r}; the first decision must stand"
    )


def test_escalation_never_decides_a_request(console):
    for row in console.approvals(state="escalated"):
        assert not row.get("decided_by"), (
            f"escalated approval {row.get('id')!r} carries a decider "
            f"{row.get('decided_by')!r}; an escalation moves a request up the chain "
            f"and never decides it"
        )


def test_opening_a_second_run_for_a_covered_period_is_refused(payroll_client, console):
    before = console.count_runs(group_code=GROUP_CORE)
    r = payroll_client.post(api("/payroll-runs"),
                            json={"group_code": GROUP_CORE, "period": OPEN_PERIOD})
    assert r.status_code in REFUSED, (
        f"opening a second run for {GROUP_CORE} period {OPEN_PERIOD} answered "
        f"{r.status_code}; exactly one run exists per period per group. "
        f"Body: {r.text[:300]!r}"
    )
    after = console.count_runs(group_code=GROUP_CORE)
    assert after == before, (
        f"a refused second run moved the payroll_run row count for {GROUP_CORE} "
        f"from {before} to {after}"
    )


def test_review_before_compute_is_refused(payroll_client, console):
    before = console.run(FRESH_PERIOD, GROUP_CORE)
    assert before is not None, (
        f"the seeded open run for {FRESH_PERIOD} in {GROUP_CORE} is missing"
    )
    r = payroll_client.post(api(f"/payroll-runs/{FRESH_PERIOD}/review"),
                            json={"group_code": GROUP_CORE})
    assert r.status_code in REFUSED, (
        f"moving run {FRESH_PERIOD} to review from state {before.get('state')!r} "
        f"answered {r.status_code}; a run reaches review only once it is computed. "
        f"Body: {r.text[:300]!r}"
    )
    after = console.run(FRESH_PERIOD, GROUP_CORE)
    assert after.get("state") == before.get("state"), (
        f"a refused review moved run {FRESH_PERIOD} from state "
        f"{before.get('state')!r} to {after.get('state')!r}"
    )


def test_second_payroll_account_signs_off_the_reviewed_run(payroll_client,
                                                           payroll2_client, console):
    payroll_client.post(api(f"/payroll-runs/{OPEN_PERIOD}/lock"),
                        json={"group_code": GROUP_CORE})
    payroll_client.post(api(f"/payroll-runs/{OPEN_PERIOD}/compute"),
                        json={"group_code": GROUP_CORE})
    poll_until(lambda: (console.run(OPEN_PERIOD, GROUP_CORE) or {}).get("state")
               in ("computed", "in_review", "signed_off"))
    payroll_client.post(api(f"/payroll-runs/{OPEN_PERIOD}/review"),
                        json={"group_code": GROUP_CORE})
    r = payroll2_client.post(api(f"/payroll-runs/{OPEN_PERIOD}/signoff"), json={
        "group_code": GROUP_CORE, "confirm_total_net_minor": RUN_TOTAL_NET})
    assert r.status_code in OK, (
        f"sign-off of {OPEN_PERIOD} by the second payroll account with the exact "
        f"total net {RUN_TOTAL_NET} answered {r.status_code}. "
        f"Body: {r.text[:300]!r}"
    )
    row = console.run(OPEN_PERIOD, GROUP_CORE)
    assert row is not None, f"run {OPEN_PERIOD} for {GROUP_CORE} is missing"
    assert str(row.get("state")) == "signed_off", (
        f"after an accepted sign-off the run is in state {row.get('state')!r}; it "
        f"must be `signed_off`"
    )
    assert row.get("signed_off_by") and row.get("signed_off_by") != row.get("reviewed_by"), (
        f"the run records reviewed_by {row.get('reviewed_by')!r} and signed_off_by "
        f"{row.get('signed_off_by')!r}; the two must differ and neither may be empty"
    )


def test_approved_leave_day_reaches_the_open_payroll_run(employee_client,
                                                         manager_client, console):
    created = employee_client.post(api("/leave-requests"), json={
        "policy_code": POLICY_ANNUAL, "from_date": "2026-11-09",
        "to_date": "2026-11-09", "half_day": False,
        "reason": f"probe {unique_suffix()}"})
    assert created.status_code in OK, (
        f"POST /api/leave-requests answered {created.status_code}, "
        f"body {created.text[:300]!r}"
    )
    approval_id = created.json().get("approval_id")
    assert approval_id, f"no `approval_id` in {created.text[:300]!r}"
    decided = manager_client.post(api(f"/approvals/{approval_id}/decide"),
                                  json={"decision": "approved", "reason": "granted"})
    assert decided.status_code in OK, (
        f"the manager of {EMP_1001} approving approval {approval_id} answered "
        f"{decided.status_code}, body {decided.text[:300]!r}"
    )
    days = poll_until(lambda: [d for d in console.attendance_days(EMP_1001)
                               if str(d.get("on_date")).startswith("2026-11-09")])
    assert days, (
        f"an approved leave day for {EMP_1001} on 2026-11-09 produced no "
        f"attendance_day row; an approved day is what reaches the run as an input"
    )
    assert str(days[0].get("status")) == "on_leave", (
        f"the attendance day for an approved leave date carries status "
        f"{days[0].get('status')!r}; it must be `on_leave`"
    )




def test_unauthenticated_decision_request_denied(anon_client, console):
    approval = pending_approval_for(console, EMP_1001) or pending_approval_for(console, EMP_1002)
    assert approval is not None, (
        f"the seed carries no pending leave approval for {EMP_1001} or {EMP_1002}"
    )
    before = console.approval(approval["id"])
    r = anon_client.post(api(f"/approvals/{approval['id']}/decide"),
                         json={"decision": "approved", "reason": "anon"})
    assert r.status_code in DENIED_OR_MISSING, (
        f"an unauthenticated POST to /api/approvals/{approval['id']}/decide answered "
        f"{r.status_code}; a request with no bearer credential must be denied, not "
        f"served. Body: {r.text[:300]!r}"
    )
    after = console.approval(approval["id"])
    assert after.get("state") == before.get("state"), (
        f"a denied unauthenticated decision moved approval {approval['id']} from "
        f"state {before.get('state')!r} to {after.get('state')!r}"
    )
    assert not after.get("decided_by"), (
        f"a denied unauthenticated decision wrote decided_by "
        f"{after.get('decided_by')!r} on approval {approval['id']}"
    )


def test_employee_cannot_read_another_employees_record(employee_client):
    r = employee_client.get(api(f"/employees/{EMP_1003}"))
    assert r.status_code in DENIED_OR_MISSING, (
        f"{EMPLOYEE_EMAIL} reading /api/employees/{EMP_1003} answered "
        f"{r.status_code}; an employee reads only their own record. "
        f"Body: {r.text[:300]!r}"
    )


def test_employee_cannot_read_any_salary_figure(employee_client):
    r = employee_client.get(api(f"/payroll-runs/{OPEN_PERIOD}/register"),
                            params={"group_code": GROUP_CORE})
    assert r.status_code in DENIED_OR_MISSING, (
        f"{EMPLOYEE_EMAIL} reading the register answered {r.status_code}; salary is "
        f"readable only by a payroll account. Body: {r.text[:300]!r}"
    )


def test_peer_manager_decision_denied_leaves_request_row_unchanged(manager2_client,
                                                                   console):
    approval = pending_approval_for(console, EMP_1001)
    assert approval is not None, (
        f"the seed carries no pending leave approval raised by {EMP_1001}"
    )
    before = console.approval(approval["id"])
    r = manager2_client.post(api(f"/approvals/{approval['id']}/decide"),
                             json={"decision": "approved", "reason": "peer"})
    assert r.status_code in DENIED, (
        f"the peer manager deciding approval {approval['id']}, raised by {EMP_1001} "
        f"who reports to {MGR_2001}, answered {r.status_code}; a manager decides only "
        f"their own direct reports. Body: {r.text[:300]!r}"
    )
    after = console.approval(approval["id"])
    assert after.get("state") == before.get("state"), (
        f"a denied peer-manager decision moved approval {approval['id']} from state "
        f"{before.get('state')!r} to {after.get('state')!r}"
    )
    assert after.get("decided_by") == before.get("decided_by"), (
        f"a denied peer-manager decision changed decided_by on approval "
        f"{approval['id']} from {before.get('decided_by')!r} to "
        f"{after.get('decided_by')!r}"
    )


def test_manager_cannot_decide_their_own_request(manager_client, console):
    created = manager_client.post(api("/leave-requests"), json={
        "policy_code": POLICY_ANNUAL, "from_date": "2026-10-19",
        "to_date": "2026-10-20", "half_day": False,
        "reason": f"probe {unique_suffix()}"})
    assert created.status_code in OK, (
        f"a manager applying for their own leave answered {created.status_code}, "
        f"body {created.text[:300]!r}"
    )
    approval_id = created.json().get("approval_id")
    assert approval_id, f"no `approval_id` in {created.text[:300]!r}"
    r = manager_client.post(api(f"/approvals/{approval_id}/decide"),
                            json={"decision": "approved", "reason": "self"})
    assert r.status_code in DENIED, (
        f"{MANAGER_EMAIL} deciding their own approval {approval_id} answered "
        f"{r.status_code}; nobody decides their own request. "
        f"Body: {r.text[:300]!r}"
    )
    row = console.approval(approval_id)
    assert str(row.get("state")) == "pending", (
        f"a denied self-decision moved approval {approval_id} to state "
        f"{row.get('state')!r}; the row must be unchanged"
    )
    assert not row.get("decided_by"), (
        f"a denied self-decision wrote decided_by {row.get('decided_by')!r} on "
        f"approval {approval_id}"
    )


def test_manager_denied_access_to_payroll_register(manager_client, console):
    before = console.run(OPEN_PERIOD, GROUP_CORE)
    r = manager_client.get(api(f"/payroll-runs/{OPEN_PERIOD}/register"),
                           params={"group_code": GROUP_CORE})
    assert r.status_code in DENIED_OR_MISSING, (
        f"{MANAGER_EMAIL} reading the register for {OPEN_PERIOD} answered "
        f"{r.status_code}; a manager reads no salary figure. Body: {r.text[:300]!r}"
    )
    lock = manager_client.post(api(f"/payroll-runs/{OPEN_PERIOD}/lock"),
                               json={"group_code": GROUP_CORE})
    assert lock.status_code in DENIED_OR_MISSING, (
        f"{MANAGER_EMAIL} locking run {OPEN_PERIOD} answered {lock.status_code}; a "
        f"manager works no run transition. Body: {lock.text[:300]!r}"
    )
    after = console.run(OPEN_PERIOD, GROUP_CORE)
    assert after.get("state") == before.get("state"), (
        f"a denied manager lock moved run {OPEN_PERIOD} from state "
        f"{before.get('state')!r} to {after.get('state')!r}"
    )


def test_employee_denied_access_to_another_employees_payslip(employee3_client):
    r = employee3_client.get(api(f"/me/payslips/{CLOSED_PERIODS[0]}"),
                             params={"employee_number": EMP_1002})
    body = r.text
    assert r.status_code in OK + DENIED_OR_MISSING, (
        f"GET /api/me/payslips/{CLOSED_PERIODS[0]} answered {r.status_code}, which is "
        f"neither a success nor a denial. Body: {body[:300]!r}"
    )
    assert EMP_1002 not in body, (
        f"an employee reading their own payslip surface received the payslip of "
        f"{EMP_1002}; the own-payslip route carries nobody else's record. "
        f"Body: {body[:300]!r}"
    )


def test_payroll_account_cannot_decide_a_leave_request(payroll_client, console):
    approval = pending_approval_for(console, EMP_1001) or pending_approval_for(console, EMP_1002)
    assert approval is not None, "the seed carries no pending leave approval"
    before = console.approval(approval["id"])
    r = payroll_client.post(api(f"/approvals/{approval['id']}/decide"),
                            json={"decision": "approved", "reason": "payroll"})
    assert r.status_code in DENIED, (
        f"{PAYROLL_EMAIL} deciding approval {approval['id']} answered "
        f"{r.status_code}; a payroll account decides no leave request. "
        f"Body: {r.text[:300]!r}"
    )
    after = console.approval(approval["id"])
    assert after.get("state") == before.get("state"), (
        f"a denied payroll decision moved approval {approval['id']} from state "
        f"{before.get('state')!r} to {after.get('state')!r}"
    )


def test_same_actor_signoff_denied_leaves_run_in_review(payroll_client, console):
    period = FRESH_PERIOD
    payroll_client.post(api(f"/payroll-runs/{period}/lock"),
                        json={"group_code": GROUP_CORE})
    payroll_client.post(api(f"/payroll-runs/{period}/compute"),
                        json={"group_code": GROUP_CORE})
    payroll_client.post(api(f"/payroll-runs/{period}/review"),
                        json={"group_code": GROUP_CORE})
    before = console.run(period, GROUP_CORE)
    assert before is not None, f"run {period} for {GROUP_CORE} is missing"
    r = payroll_client.post(api(f"/payroll-runs/{period}/signoff"), json={
        "group_code": GROUP_CORE,
        "confirm_total_net_minor": before.get("total_net_minor")})
    assert r.status_code in DENIED, (
        f"the account that moved run {period} into review signing it off answered "
        f"{r.status_code}; the preparer may never be the signer. "
        f"Body: {r.text[:300]!r}"
    )
    after = console.run(period, GROUP_CORE)
    assert after.get("state") == before.get("state"), (
        f"a denied same-actor sign-off moved run {period} from state "
        f"{before.get('state')!r} to {after.get('state')!r}"
    )
    assert not after.get("signed_off_by"), (
        f"a denied same-actor sign-off wrote signed_off_by "
        f"{after.get('signed_off_by')!r} on run {period}"
    )


def test_signoff_total_mismatch_is_refused(payroll2_client, console):
    period = FRESH_PERIOD
    before = console.run(period, GROUP_CORE)
    assert before is not None, f"run {period} for {GROUP_CORE} is missing"
    r = payroll2_client.post(api(f"/payroll-runs/{period}/signoff"), json={
        "group_code": GROUP_CORE, "confirm_total_net_minor": 1})
    assert r.status_code in REFUSED_OR_DENIED, (
        f"a sign-off carrying a total net of 1 answered {r.status_code}; a mismatched "
        f"total must be refused. Body: {r.text[:300]!r}"
    )
    after = console.run(period, GROUP_CORE)
    assert after.get("state") == before.get("state"), (
        f"a refused sign-off moved run {period} from state {before.get('state')!r} "
        f"to {after.get('state')!r}"
    )


def test_no_frontend_asset_carries_a_credential():
    with httpx.Client(base_url=app_origin(), timeout=30.0,
                      follow_redirects=True) as raw:
        page = raw.get("/login")
        assert page.status_code in OK, (
            f"GET /login answered {page.status_code}; the sign-in route must render "
            f"for a signed-out visitor"
        )
        body = page.text
        for marker in SECRET_MARKERS:
            assert marker not in body, (
                f"the sign-in page the browser downloads contains {marker!r}; no "
                f"credential, client secret or connection string may reach the client"
            )




def test_leave_balance_equals_the_sum_of_its_ledger_rows(employee_client, console):
    r = employee_client.get(api("/leave-balances"),
                            params={"employee_number": EMP_1001,
                                    "policy_code": POLICY_ANNUAL})
    assert r.status_code in OK, (
        f"GET /api/leave-balances for {EMP_1001} answered {r.status_code}, "
        f"body {r.text[:300]!r}"
    )
    rows = r.json()
    assert isinstance(rows, list) and rows, (
        f"GET /api/leave-balances must return a non-empty top-level array; got "
        f"{r.text[:300]!r}"
    )
    reported = int(rows[0].get("halves", -1))
    stored = console.ledger_balance_halves(EMP_1001, POLICY_ANNUAL)
    assert reported == stored, (
        f"the balance endpoint reports {reported} halves for {EMP_1001} on "
        f"{POLICY_ANNUAL} while the leave_ledger_entry rows sum to {stored}; the "
        f"balance is the sum of its ledger and is never a stored column"
    )
    ledger = employee_client.get(api("/leave-ledger"),
                                 params={"employee_number": EMP_1001,
                                         "policy_code": POLICY_ANNUAL})
    assert ledger.status_code in OK, (
        f"GET /api/leave-ledger for {EMP_1001} answered {ledger.status_code}, "
        f"body {ledger.text[:300]!r}"
    )
    entries = ledger.json()
    assert isinstance(entries, list) and entries, (
        f"GET /api/leave-ledger must return a non-empty top-level array; got "
        f"{ledger.text[:300]!r}"
    )
    signed = 0
    for entry in entries:
        kind = str(entry.get("kind"))
        assert kind in ("opening", "accrual", "availed", "pending", "correction",
                        "encashment", "lapse"), (
            f"a ledger entry carries the kind {kind!r}, which is not one of the seven "
            f"named kinds"
        )
        signed += (1 if kind in ("opening", "accrual", "correction") else -1) * int(
            entry.get("halves") or 0)
    assert signed == reported, (
        f"the ledger endpoint's entries sum to {signed} halves while the balance "
        f"endpoint reports {reported}; the expansion sums to the figure shown"
    )


def test_seeded_annual_balance_matches_the_pinned_figure(console):
    stored = console.ledger_balance_halves(EMP_1001, POLICY_ANNUAL)
    assert stored == ANNUAL_BALANCE_HALVES, (
        f"the seeded {POLICY_ANNUAL} ledger for {EMP_1001} sums to {stored} halves; "
        f"the pinned seed is {ANNUAL_BALANCE_HALVES} halves, from an opening of 20, "
        f"seven accruals of {ANNUAL_ACCRUAL_HALVES}, 8 availed and 4 pending"
    )


def test_approval_persists_an_availed_ledger_row(employee2_client, manager_client,
                                                 console):
    created = employee2_client.post(api("/leave-requests"), json={
        "policy_code": POLICY_ANNUAL, "from_date": "2026-11-16",
        "to_date": "2026-11-16", "half_day": False,
        "reason": f"probe {unique_suffix()}"})
    assert created.status_code in OK, (
        f"POST /api/leave-requests answered {created.status_code}, "
        f"body {created.text[:300]!r}"
    )
    approval_id = created.json().get("approval_id")
    before = console.count_ledger(employee_number=EMP_1002, policy_code=POLICY_ANNUAL,
                                  kind="availed")
    decided = manager_client.post(api(f"/approvals/{approval_id}/decide"),
                                  json={"decision": "approved", "reason": "granted"})
    assert decided.status_code in OK, (
        f"approving approval {approval_id} answered {decided.status_code}, "
        f"body {decided.text[:300]!r}"
    )
    after = poll_until(lambda: console.count_ledger(
        employee_number=EMP_1002, policy_code=POLICY_ANNUAL, kind="availed") > before)
    assert after, (
        f"approving a leave request for {EMP_1002} wrote no `availed` "
        f"leave_ledger_entry row; the availed count stayed at {before}"
    )


def test_rejection_removes_the_pending_ledger_row(employee2_client, manager_client,
                                                  console):
    created = employee2_client.post(api("/leave-requests"), json={
        "policy_code": POLICY_ANNUAL, "from_date": "2026-11-23",
        "to_date": "2026-11-23", "half_day": False,
        "reason": f"probe {unique_suffix()}"})
    assert created.status_code in OK, (
        f"POST /api/leave-requests answered {created.status_code}, "
        f"body {created.text[:300]!r}"
    )
    approval_id = created.json().get("approval_id")
    balance_before_decision = console.ledger_balance_halves(EMP_1002, POLICY_ANNUAL)
    decided = manager_client.post(api(f"/approvals/{approval_id}/decide"),
                                  json={"decision": "rejected", "reason": "no"})
    assert decided.status_code in OK, (
        f"rejecting approval {approval_id} answered {decided.status_code}, "
        f"body {decided.text[:300]!r}"
    )
    restored = poll_until(lambda: console.ledger_balance_halves(
        EMP_1002, POLICY_ANNUAL) > balance_before_decision)
    assert restored, (
        f"rejecting a pending request for {EMP_1002} left the ledger balance at "
        f"{balance_before_decision} halves; a rejection removes the pending entry "
        f"and returns the balance"
    )


def test_duplicate_punch_raw_ref_writes_no_second_row(console, employee3_client):
    punch = new_punch(EMP_1003, "2026-07-20T09:02:00Z", "in")
    first = employee3_client.post(api("/attendance/punches"), json=punch)
    assert first.status_code in OK, (
        f"POST /api/attendance/punches with a signed-in caller answered "
        f"{first.status_code}; the endpoint accepts a bearer credential. "
        f"Body: {first.text[:300]!r}"
    )
    settle()
    count_after_first = console.count_punches(raw_ref=punch["raw_ref"])
    assert count_after_first == 1, (
        f"an accepted punch wrote {count_after_first} rows for raw_ref "
        f"{punch['raw_ref']!r}; exactly one row must exist"
    )
    employee3_client.post(api("/attendance/punches"), json=punch)
    settle()
    count_after_replay = console.count_punches(raw_ref=punch["raw_ref"])
    assert count_after_replay == 1, (
        f"replaying raw_ref {punch['raw_ref']!r} left {count_after_replay} "
        f"attendance_punch rows; a repeated source reference writes no second row"
    )


def test_punch_rows_are_never_updated_or_deleted(console, employee3_client):
    before = console.punches_on(EMP_1003)
    assert before, f"no attendance_punch rows exist for {EMP_1003}"
    fingerprint = sorted((str(row.get("id")), str(row.get("at")),
                          str(row.get("direction"))) for row in before)
    employee3_client.post(api("/regularisations"), json={
        "on_date": "2026-07-20", "in_at": "2026-07-20T09:00:00Z",
        "out_at": "2026-07-20T18:00:00Z", "reason": f"probe {unique_suffix()}"})
    settle()
    after = console.punches_on(EMP_1003)
    after_fingerprint = sorted((str(row.get("id")), str(row.get("at")),
                                str(row.get("direction"))) for row in after)
    for row in fingerprint:
        assert row in after_fingerprint, (
            f"attendance_punch row {row} for {EMP_1003} was altered or removed after "
            f"a regularisation was raised; punches are append only"
        )


def test_regularisation_leaves_the_original_punches_stored(console, employee3_client):
    punches_before = console.count_punches(employee_number=EMP_1003)
    regs_before = console.count_regularisations(employee_number=EMP_1003)
    r = employee3_client.post(api("/regularisations"), json={
        "on_date": "2026-07-21", "in_at": "2026-07-21T09:00:00Z",
        "out_at": "2026-07-21T18:00:00Z", "reason": f"probe {unique_suffix()}"})
    assert r.status_code in OK, (
        f"POST /api/regularisations answered {r.status_code}, "
        f"body {r.text[:300]!r}"
    )
    settle()
    assert console.count_punches(employee_number=EMP_1003) == punches_before, (
        f"raising a regularisation changed the attendance_punch row count for "
        f"{EMP_1003}; the original punches remain untouched"
    )
    assert console.count_regularisations(employee_number=EMP_1003) == regs_before + 1, (
        f"raising a regularisation wrote no regularisation row for {EMP_1003}; the "
        f"correction sits on top of the punches as its own record"
    )


def test_concurrent_decisions_record_exactly_one_decider(employee_client, console):
    created = employee_client.post(api("/leave-requests"), json={
        "policy_code": POLICY_ANNUAL, "from_date": "2026-12-07",
        "to_date": "2026-12-07", "half_day": False,
        "reason": f"probe {unique_suffix()}"})
    assert created.status_code in OK, (
        f"POST /api/leave-requests answered {created.status_code}, "
        f"body {created.text[:300]!r}"
    )
    approval_id = created.json().get("approval_id")
    token = login(MANAGER_EMAIL, CORPUS_PASSWORD)

    def decide(decision: str):
        with client(token) as c:
            return c.post(api(f"/approvals/{approval_id}/decide"),
                          json={"decision": decision, "reason": "race"})

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(decide, "approved"), pool.submit(decide, "rejected")]
        results = [f.result() for f in futures]
    accepted = [r for r in results if r.status_code in OK]
    assert len(accepted) == 1, (
        f"two simultaneous decisions on approval {approval_id} produced "
        f"{len(accepted)} acceptances with statuses "
        f"{[r.status_code for r in results]}; exactly one must win"
    )
    row = console.approval(approval_id)
    assert str(row.get("state")) in ("approved", "rejected"), (
        f"after two simultaneous decisions approval {approval_id} is in state "
        f"{row.get('state')!r}; exactly one decision must have landed"
    )


def test_concurrent_decisions_move_the_ledger_once(employee_client, console):
    created = employee_client.post(api("/leave-requests"), json={
        "policy_code": POLICY_ANNUAL, "from_date": "2026-12-14",
        "to_date": "2026-12-14", "half_day": False,
        "reason": f"probe {unique_suffix()}"})
    assert created.status_code in OK, (
        f"POST /api/leave-requests answered {created.status_code}, "
        f"body {created.text[:300]!r}"
    )
    approval_id = created.json().get("approval_id")
    before = console.count_ledger(employee_number=EMP_1001, policy_code=POLICY_ANNUAL,
                                  kind="availed")
    token = login(MANAGER_EMAIL, CORPUS_PASSWORD)

    def decide():
        with client(token) as c:
            return c.post(api(f"/approvals/{approval_id}/decide"),
                          json={"decision": "approved", "reason": "race"})

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        [f.result() for f in [pool.submit(decide), pool.submit(decide)]]
    settle()
    after = console.count_ledger(employee_number=EMP_1001, policy_code=POLICY_ANNUAL,
                                kind="availed")
    assert after - before <= 1, (
        f"two simultaneous approvals of approval {approval_id} wrote "
        f"{after - before} `availed` leave_ledger_entry rows for {EMP_1001}; the "
        f"ledger moves exactly once"
    )


def test_seeded_schema_carries_the_pinned_columns(console):
    row = console.employee(EMP_1001)
    assert row is not None, f"seed employee {EMP_1001} is missing"
    for column in ("employee_number", "full_name", "state",
                   "manager_employee_number", "department_code", "location_code",
                   "payroll_group_code"):
        assert column in row, (
            f"the employee row for {EMP_1001} has no {column!r} column; the pinned "
            f"columns are part of the data model. Columns seen: {sorted(row)}"
        )
    assert row.get("full_name") == NAME_1001, (
        f"seed employee {EMP_1001} is named {row.get('full_name')!r}; the pinned seed "
        f"name is {NAME_1001!r}"
    )
    assert row.get("manager_employee_number") == MGR_2001, (
        f"seed employee {EMP_1001} reports to "
        f"{row.get('manager_employee_number')!r}; the pinned reporting line is "
        f"{MGR_2001!r}"
    )
    assert str(row.get("state")) in ("pre_joining", "active", "on_notice", "exited",
                                     "alumni"), (
        f"seed employee {EMP_1001} carries state {row.get('state')!r}, which is not "
        f"one of the five named employee states"
    )


def test_seeded_tables_carry_their_pinned_columns(console):
    policy = console.policy(POLICY_ANNUAL)
    assert policy is not None, f"the seeded leave policy {POLICY_ANNUAL} is missing"
    for column in ("accrual", "accrual_halves", "accrual_cap_halves",
                   "carry_forward_halves", "carry_forward_expires_on", "encashable",
                   "min_notice_days", "max_consecutive_halves",
                   "requires_document_after_halves", "half_day",
                   "negative_balance_halves", "holiday_calendar_id",
                   "approval_levels"):
        assert column in policy, (
            f"the leave_policy row for {POLICY_ANNUAL} has no {column!r} column; a "
            f"policy is data and carries every pinned field. Columns seen: "
            f"{sorted(policy)}"
        )
    assert int(policy.get("accrual_halves") or 0) == ANNUAL_ACCRUAL_HALVES, (
        f"{POLICY_ANNUAL} accrues {policy.get('accrual_halves')!r} halves a month; "
        f"the pinned seed is {ANNUAL_ACCRUAL_HALVES}"
    )
    assert int(policy.get("min_notice_days") or 0) == ANNUAL_NOTICE_DAYS, (
        f"{POLICY_ANNUAL} requires {policy.get('min_notice_days')!r} days notice; the "
        f"pinned seed is {ANNUAL_NOTICE_DAYS}"
    )
    calendar = console.holiday_calendars()
    assert calendar, "no holiday_calendar rows exist"
    for column in ("code", "location_code", "weekend_days"):
        assert column in calendar[0], (
            f"a holiday_calendar row has no {column!r} column; columns seen: "
            f"{sorted(calendar[0])}"
        )
    punches = console.punches_on(EMP_1001)
    assert punches, f"no attendance_punch rows exist for {EMP_1001}"
    for column in ("employee_number", "at", "direction", "source", "device_id",
                   "location_code", "confidence", "raw_ref"):
        assert column in punches[0], (
            f"an attendance_punch row has no {column!r} column; columns seen: "
            f"{sorted(punches[0])}"
        )
    days = console.attendance_days(EMP_1001)
    assert days, f"no attendance_day rows exist for {EMP_1001}"
    for column in ("on_date", "worked_minutes", "status", "late_minutes",
                   "early_minutes", "overtime_minutes", "regularisation_id"):
        assert column in days[0], (
            f"an attendance_day row has no {column!r} column; columns seen: "
            f"{sorted(days[0])}"
        )
    run = open_run_row(console)
    for column in ("group_code", "period", "state", "reviewed_by", "signed_off_by",
                   "total_gross_minor", "total_deductions_minor", "total_net_minor",
                   "headcount_paid", "locked_at"):
        assert column in run, (
            f"the payroll_run row for {OPEN_PERIOD} has no {column!r} column; "
            f"columns seen: {sorted(run)}"
        )
    rules = console.statutory_rules()
    assert rules, "no statutory_rule rows exist"
    for column in ("code", "state_code", "basis", "rate_bp", "threshold_minor",
                   "cap_minor", "flat_minor", "rounding"):
        assert column in rules[0], (
            f"a statutory_rule row has no {column!r} column; columns seen: "
            f"{sorted(rules[0])}"
        )


def test_seeded_organisation_carries_the_pinned_row_counts(console):
    employees = console.count_employees()
    assert employees == SEEDED_EMPLOYEE_COUNT, (
        f"the employee table holds {employees} rows; the pinned seed is "
        f"{SEEDED_EMPLOYEE_COUNT}"
    )
    calendars = {str(c.get("code")) for c in console.holiday_calendars()}
    assert CALENDAR_KA in calendars, (
        f"the seeded holiday calendars are {sorted(calendars)}; {CALENDAR_KA!r} must "
        f"be among them"
    )
    groups = {str(g.get("code")) for g in console.payroll_groups()}
    assert GROUP_CORE in groups, (
        f"the seeded payroll groups are {sorted(groups)}; {GROUP_CORE!r} must be "
        f"among them"
    )


def test_seeded_open_run_is_locked_with_four_employees(console):
    row = open_run_row(console)
    assert str(row.get("state")) in ("locked", "computed", "in_review", "signed_off"), (
        f"the seeded run for {OPEN_PERIOD} is in state {row.get('state')!r}; the seed "
        f"leaves it at `locked`"
    )
    members = console.count_employees(payroll_group_code=GROUP_CORE)
    assert members == RUN_HEADCOUNT, (
        f"the payroll group {GROUP_CORE} holds {members} employees; the pinned seed "
        f"is {RUN_HEADCOUNT}"
    )
    days = console.count_attendance_days(employee_number=EMP_1001)
    assert days >= SEEDED_ATTENDANCE_DAYS, (
        f"{EMP_1001} carries {days} attendance_day rows; the seed carries at least "
        f"{SEEDED_ATTENDANCE_DAYS} days of the open period"
    )


def test_computed_payslip_matches_the_pinned_worked_example(payroll_client, console):
    payroll_client.post(api(f"/payroll-runs/{OPEN_PERIOD}/compute"),
                        json={"group_code": GROUP_CORE})
    run = poll_until(lambda: console.payslips(open_run_row(console)["id"]) or None)
    assert run, (
        f"computing run {OPEN_PERIOD} produced no payslip rows for group {GROUP_CORE}"
    )
    slip_1002 = console.payslip(open_run_row(console)["id"], EMP_1002)
    assert slip_1002 is not None, (
        f"no payslip row exists for {EMP_1002} in the {OPEN_PERIOD} run"
    )
    assert int(slip_1002.get("gross_minor")) == GROSS_1002, (
        f"the payslip for {EMP_1002} carries gross {slip_1002.get('gross_minor')!r}; "
        f"with no leave without pay the prorated gross is {GROSS_1002}"
    )
    assert int(slip_1002.get("net_minor")) == NET_1002, (
        f"the payslip for {EMP_1002} carries net {slip_1002.get('net_minor')!r}; the "
        f"worked example gives {NET_1002} from a gross of {GROSS_1002} less 325000 "
        f"of deductions"
    )
    slip_1001 = console.payslip(open_run_row(console)["id"], EMP_1001)
    assert slip_1001 is not None, (
        f"no payslip row exists for {EMP_1001} in the {OPEN_PERIOD} run"
    )
    assert int(slip_1001.get("net_minor")) == NET_1001, (
        f"the payslip for {EMP_1001} carries net {slip_1001.get('net_minor')!r}; one "
        f"leave-without-pay day prorates a gross of {GROSS_1001} to 3000000 and the "
        f"worked example gives {NET_1001}"
    )


def test_run_totals_reconcile_with_its_payslip_rows(payroll_client, console):
    payroll_client.post(api(f"/payroll-runs/{OPEN_PERIOD}/compute"),
                        json={"group_code": GROUP_CORE})
    poll_until(lambda: console.payslips(open_run_row(console)["id"]) or None)
    run = open_run_row(console)
    slips = console.payslips(run["id"])
    assert len(slips) == RUN_HEADCOUNT, (
        f"the {OPEN_PERIOD} run produced {len(slips)} payslips; the group holds "
        f"{RUN_HEADCOUNT} employees and a run completes for all of them or none"
    )
    gross = sum(int(s.get("gross_minor") or 0) for s in slips)
    net = sum(int(s.get("net_minor") or 0) for s in slips)
    deductions = sum(int(s.get("deductions_minor") or 0) for s in slips)
    assert gross == RUN_TOTAL_GROSS, (
        f"the payslip gross figures sum to {gross}; the pinned run total gross is "
        f"{RUN_TOTAL_GROSS}"
    )
    assert deductions == RUN_TOTAL_DEDUCTIONS, (
        f"the payslip deduction figures sum to {deductions}; the pinned run total is "
        f"{RUN_TOTAL_DEDUCTIONS}"
    )
    assert net == RUN_TOTAL_NET, (
        f"the payslip net figures sum to {net}; the pinned run total net is "
        f"{RUN_TOTAL_NET}"
    )
    assert int(run.get("total_net_minor") or 0) == RUN_TOTAL_NET, (
        f"the run row records total_net_minor {run.get('total_net_minor')!r} while "
        f"its payslips sum to {net}; the recorded total must reconcile"
    )


def test_statutory_lines_record_the_rule_set_version(payroll_client, console):
    payroll_client.post(api(f"/payroll-runs/{OPEN_PERIOD}/compute"),
                        json={"group_code": GROUP_CORE})
    poll_until(lambda: console.payslips(open_run_row(console)["id"]) or None)
    slip = console.payslip(open_run_row(console)["id"], EMP_1002)
    assert slip is not None, f"no payslip row exists for {EMP_1002}"
    lines = console.payslip_lines(slip["id"])
    assert lines, f"the payslip for {EMP_1002} carries no payslip_line rows"
    statutory = [ln for ln in lines if str(ln.get("code")) in STATUTORY_CODES]
    assert statutory, (
        f"the payslip for {EMP_1002} carries no line from the statutory heads "
        f"{list(STATUTORY_CODES)}; codes seen: "
        f"{sorted({str(ln.get('code')) for ln in lines})}"
    )
    for line in statutory:
        assert line.get("rule_version") is not None and str(line.get("rule_version")) != "", (
            f"the statutory line {line.get('code')!r} on the payslip for {EMP_1002} "
            f"records no rule_version; every statutory line records the version that "
            f"produced it"
        )


def test_seeded_statutory_rule_set_is_data_not_code(console):
    sets = console.rule_sets(code=RULE_SET_CODE)
    assert sets, (
        f"no statutory_rule_set row carries the code {RULE_SET_CODE!r}; the rule set "
        f"is data, versioned by an effective date"
    )
    assert int(sets[0].get("version") or 0) == RULE_SET_VERSION, (
        f"the seeded rule set {RULE_SET_CODE!r} is version "
        f"{sets[0].get('version')!r}; the pinned seed is version {RULE_SET_VERSION}"
    )
    codes = {str(rule.get("code")) for rule in console.statutory_rules()}
    for head in STATUTORY_CODES:
        assert head in codes, (
            f"the statutory_rule rows carry the codes {sorted(codes)}; the seeded "
            f"rule set carries {head!r} as one of its five heads"
        )


def test_signed_off_run_payslip_figures_do_not_change(payroll_client, console):
    period = CLOSED_PERIODS[0]
    run = console.run(period, GROUP_CORE)
    assert run is not None, f"the closed run for {period} is missing"
    before = {str(s.get("employee_number")): int(s.get("net_minor") or 0)
              for s in console.payslips(run["id"])}
    assert before, f"the closed run for {period} carries no payslips"
    payroll_client.post(api(f"/payroll-runs/{period}/compute"),
                        json={"group_code": GROUP_CORE})
    settle()
    after = {str(s.get("employee_number")): int(s.get("net_minor") or 0)
             for s in console.payslips(run["id"])}
    assert after == before, (
        f"recomputing the closed run {period} changed its payslip net figures from "
        f"{before} to {after}; a signed-off run's figures never change"
    )


def test_directory_cursor_paging_repeats_no_row(payroll_client):
    seen = []
    cursor = None
    for _ in range(6):
        params = {"cursor": cursor} if cursor else {}
        r = payroll_client.get(api("/employees"), params=params)
        assert r.status_code in OK, (
            f"GET /api/employees answered {r.status_code}, body {r.text[:300]!r}"
        )
        rows = r.json()
        assert isinstance(rows, list), (
            f"GET /api/employees must return a top-level array; got {r.text[:200]!r}"
        )
        assert len(rows) <= PAGE_SIZE, (
            f"a directory page carried {len(rows)} rows; the default page size is "
            f"{PAGE_SIZE}"
        )
        seen.extend(str(row.get("employee_number")) for row in rows)
        cursor = r.headers.get(CURSOR_HEADER)
        if not cursor:
            break
    assert len(seen) == len(set(seen)), (
        f"a cursor paging session over the directory returned "
        f"{len(seen) - len(set(seen))} repeated employee number(s); a paging session "
        f"repeats no row"
    )


def test_register_paging_reports_totals_and_a_cursor(payroll_client):
    r = payroll_client.get(api(f"/payroll-runs/{OPEN_PERIOD}/register"),
                           params={"group_code": GROUP_CORE})
    assert r.status_code in OK, (
        f"GET /api/payroll-runs/{OPEN_PERIOD}/register as a payroll account answered "
        f"{r.status_code}, body {r.text[:300]!r}"
    )
    body = r.json()
    assert "rows" in body and "totals" in body, (
        f"the register response carries the keys {sorted(body)}; `rows` and `totals` "
        f"are pinned field names"
    )
    assert len(body["rows"]) <= PAGE_SIZE, (
        f"a register page carried {len(body['rows'])} rows; the default page size is "
        f"{PAGE_SIZE}"
    )


def test_claim_is_never_paid_through_both_routes(payroll_client):
    batch = payroll_client.get(api("/claims"), params={"state": "paid"})
    payroll = payroll_client.get(api("/claims"),
                                 params={"state": "reimbursed_via_payroll"})
    assert batch.status_code in OK, (
        f"GET /api/claims?state=paid answered {batch.status_code}, "
        f"body {batch.text[:300]!r}"
    )
    assert payroll.status_code in OK, (
        f"GET /api/claims?state=reimbursed_via_payroll answered "
        f"{payroll.status_code}, body {payroll.text[:300]!r}"
    )
    batch_ids = {str(row.get("id")) for row in batch.json()}
    payroll_ids = {str(row.get("id")) for row in payroll.json()}
    overlap = batch_ids & payroll_ids
    assert not overlap, (
        f"claim(s) {sorted(overlap)} are reported both as paid through a batch and as "
        f"reimbursed through payroll; a claim takes one route, never both"
    )




def test_unknown_address_answers_not_found():
    with httpx.Client(base_url=app_origin(), timeout=30.0) as raw:
        r = raw.get(f"/payroll/2026-99-{unique_suffix()}")
        assert r.status_code == 404, (
            f"an address matching no route answered {r.status_code}; the product's "
            f"own not-found page answers as not found"
        )
        assert r.text.strip(), (
            "the not-found response carried an empty body; the product renders its "
            "own not-found page with a way back into the console"
        )


def test_favicon_is_served_and_declared():
    with httpx.Client(base_url=app_origin(), timeout=30.0,
                      follow_redirects=True) as raw:
        page = raw.get("/login")
        assert page.status_code in OK, (
            f"GET /login answered {page.status_code}"
        )
        assert "icon" in page.text.lower(), (
            f"the sign-in page declares no icon link in its document head; every page "
            f"declares the favicon. Head excerpt: {page.text[:400]!r}"
        )
        icon = raw.get("/favicon.ico")
        assert icon.status_code in OK, (
            f"GET /favicon.ico answered {icon.status_code}; the app serves a favicon"
        )


def test_manager_queue_carries_only_their_own_direct_reports(manager2_client, console):
    r = manager2_client.get(api("/approvals"), params={"state": "pending"})
    assert r.status_code in OK, (
        f"GET /api/approvals as the peer manager answered {r.status_code}, "
        f"body {r.text[:300]!r}"
    )
    rows = r.json()
    assert isinstance(rows, list), (
        f"GET /api/approvals must return a top-level array; got {r.text[:200]!r}"
    )
    leaked = []
    for row in rows:
        requester = str(row.get("requested_by"))
        employee = console.employee(requester)
        assert employee is not None, (
            f"the queue names requester {requester!r}, which is in no employee row"
        )
        if str(employee.get("manager_employee_number")) != MGR_2002:
            leaked.append(requester)
    assert not leaked, (
        f"the peer manager's queue carries request(s) from {sorted(set(leaked))}, who "
        f"do not report to {MGR_2002}; the queue is filtered to the caller's own "
        f"direct reports"
    )


def test_run_transitions_advance_only_in_order(payroll_client, console):
    period = OPEN_PERIOD
    before = console.run(period, GROUP_CORE)
    assert before is not None, f"run {period} for {GROUP_CORE} is missing"
    r = payroll_client.post(api(f"/payroll-runs/{period}/signoff"), json={
        "group_code": GROUP_CORE, "confirm_total_net_minor": RUN_TOTAL_NET})
    assert r.status_code in REFUSED_OR_DENIED, (
        f"signing off run {period} from state {before.get('state')!r} answered "
        f"{r.status_code}; a run advances only through review. "
        f"Body: {r.text[:300]!r}"
    )


def test_bank_field_change_without_confirmation_is_refused(employee_client, console):
    before = console.count_audit(subject_kind="employee")
    r = employee_client.post(api(f"/employees/{EMP_1001}/changes"), json={
        "field": "bank_account", "to_value": f"ACC-{unique_suffix()}",
        "effective_from": "2026-08-01", "reason": f"probe {unique_suffix()}"})
    assert r.status_code in OK + REFUSED_OR_DENIED, (
        f"POST /api/employees/{EMP_1001}/changes answered {r.status_code}, which is "
        f"neither an acceptance nor a refusal. Body: {r.text[:300]!r}"
    )
    if r.status_code in OK:
        body = r.json()
        assert not body.get("approved_by"), (
            f"an employee proposing their own bank change received an already "
            f"approved change record ({body.get('approved_by')!r}); the proposal is "
            f"held until a payroll account confirms"
        )
    assert console.count_audit(subject_kind="employee") >= before, (
        "the audit trail lost rows while a bank change was proposed"
    )


def test_restricted_field_direct_edit_is_refused(employee_client):
    r = employee_client.post(api(f"/employees/{EMP_1004}/changes"), json={
        "field": "designation", "to_value": "Director",
        "effective_from": "2026-08-01", "reason": f"probe {unique_suffix()}"})
    assert r.status_code in REFUSED_OR_DENIED, (
        f"an employee writing a restricted field on {EMP_1004} answered "
        f"{r.status_code}; a restricted field is never edited in place by an "
        f"employee. Body: {r.text[:300]!r}"
    )


def test_app_is_reachable_at_its_public_address():
    with httpx.Client(base_url=app_origin(), timeout=30.0,
                      follow_redirects=True) as raw:
        root = raw.get("/")
        assert root.status_code in OK + (302, 303, 307, 308), (
            f"the app answered {root.status_code} at its public address; it must be "
            f"reachable there, on the published port, from outside its own container"
        )
        health = raw.get("/api/health")
        assert health.status_code == 200, (
            f"GET /api/health at the same origin answered {health.status_code}; the "
            f"JSON API is served on the app's own origin under the /api prefix"
        )
        assert root.text.strip(), (
            "the app's public address answered with an empty body; a production "
            "build serves a rendered page there"
        )


def test_issued_token_is_minted_by_the_declared_identity_provider(anon_client):
    r = anon_client.post(api("/auth/login"),
                         json={"email": PAYROLL_EMAIL, "password": CORPUS_PASSWORD})
    assert r.status_code in OK, (
        f"POST /api/auth/login as {PAYROLL_EMAIL} answered {r.status_code}, "
        f"body {r.text[:300]!r}"
    )
    token = r.json().get("access_token")
    assert token, f"no access_token in the sign-in response: {r.text[:300]!r}"
    parts = token.split(".")
    assert len(parts) == 3, (
        f"the issued credential is not a signed token in three parts; it has "
        f"{len(parts)}. Identity is the declared provider's, so the app hands back "
        f"the provider's token rather than one of its own invention"
    )
    padded = parts[1] + "=" * (-len(parts[1]) % 4)
    claims = json.loads(base64.urlsafe_b64decode(padded.encode("ascii")))
    issuer = str(claims.get("iss", ""))
    assert issuer, (
        f"the issued token carries no `iss` claim; its claims are "
        f"{sorted(claims)}"
    )
    assert issuer.rstrip("/") == expected_issuer().rstrip("/"), (
        f"the issued token names the issuer {issuer!r}; the environment declares "
        f"{expected_issuer()!r}. A token the app signs for itself is a users table "
        f"standing in for the declared identity provider"
    )
    assert claims.get("employee_number") or claims.get("preferred_username"), (
        f"the issued token carries neither an employee number nor a username claim, "
        f"so the app has nothing from the provider to resolve the caller by. Claims: "
        f"{sorted(claims)}"
    )


def test_tampered_token_is_rejected(anon_client):
    r = anon_client.post(api("/auth/login"),
                         json={"email": MANAGER_EMAIL, "password": CORPUS_PASSWORD})
    assert r.status_code in OK, (
        f"POST /api/auth/login answered {r.status_code}, body {r.text[:300]!r}"
    )
    token = r.json()["access_token"]
    head, payload, signature = token.split(".")
    flipped = "A" if signature[0] != "A" else "B"
    forged = f"{head}.{payload}.{flipped}{signature[1:]}"
    with client(forged) as bad:
        me = bad.get(api("/me"))
    assert me.status_code in DENIED, (
        f"a credential whose signature was altered answered {me.status_code} at "
        f"/api/me; the signature is checked on every request. "
        f"Body: {me.text[:300]!r}"
    )


def test_role_in_the_request_body_is_never_authority(employee_client, console):
    before = console.run(OPEN_PERIOD, GROUP_CORE)
    r = employee_client.post(api(f"/payroll-runs/{OPEN_PERIOD}/lock"),
                             json={"group_code": GROUP_CORE, "role": "payroll"})
    assert r.status_code in DENIED_OR_MISSING, (
        f"an employee session carrying \"role\": \"payroll\" in the body locked the "
        f"run with {r.status_code}; authority comes from the validated credential, "
        f"never from the request body. Body: {r.text[:300]!r}"
    )
    after = console.run(OPEN_PERIOD, GROUP_CORE)
    assert after.get("state") == before.get("state"), (
        f"a denied lock moved run {OPEN_PERIOD} from state {before.get('state')!r} "
        f"to {after.get('state')!r}"
    )


def test_written_row_is_visible_in_the_declared_database(employee_client, console):
    reason = f"probe {unique_suffix()}"
    r = employee_client.post(api("/claims"), json={
        "category": "MEALS", "amount_minor": 150000, "currency": CURRENCY,
        "spent_on": "2026-07-09", "receipt_ref": reason})
    assert r.status_code in OK, (
        f"POST /api/claims answered {r.status_code}, body {r.text[:300]!r}"
    )
    claim_id = r.json().get("id")
    assert claim_id is not None, f"no `id` in the claim response: {r.text[:300]!r}"
    stored = poll_until(lambda: console.claim(claim_id))
    assert stored is not None, (
        f"claim {claim_id!r} was accepted over HTTP but is in no row of the declared "
        f"PostgreSQL database; the named provider is the only place the data lives"
    )
    assert int(stored.get("amount_minor")) == 150000, (
        f"the stored claim carries amount_minor {stored.get('amount_minor')!r}; money "
        f"is an integer in the currency's minor unit and 150000 was submitted"
    )
    assert str(stored.get("currency")) == CURRENCY, (
        f"the stored claim carries currency {stored.get('currency')!r}; the pinned "
        f"currency is {CURRENCY!r}"
    )
    assert not isinstance(stored.get("amount_minor"), float), (
        f"the stored amount is a floating-point value "
        f"({stored.get('amount_minor')!r}); money is never a float"
    )


def test_refused_request_carries_a_reason_body(employee_client):
    r = employee_client.post(api("/leave-requests"), json={
        "policy_code": "NOT-A-POLICY", "from_date": "2026-09-01",
        "to_date": "2026-09-01", "half_day": False, "reason": "probe"})
    assert r.status_code in REFUSED, (
        f"a leave request naming an unknown policy answered {r.status_code}; it must "
        f"be refused as invalid. Body: {r.text[:300]!r}"
    )
    body = r.json()
    error = body.get("error") if isinstance(body, dict) else None
    assert isinstance(error, dict), (
        f"a refused request answered with the body {r.text[:300]!r}; the pinned error "
        f"shape carries an `error` object"
    )
    assert error.get("code") and error.get("message"), (
        f"the error object carries the keys {sorted(error)}; the pinned shape carries "
        f"a code beside a message"
    )


def test_seeded_runs_and_claims_match_their_pinned_states(console):
    for period in CLOSED_PERIODS:
        row = console.run(period, GROUP_CORE)
        assert row is not None, f"the seeded run for {period} is missing"
        assert str(row.get("state")) in ("closed", "paid", "signed_off"), (
            f"the seeded run for {period} is in state {row.get('state')!r}; the two "
            f"earlier runs are seeded closed with their published payslips"
        )
        assert console.payslips(row["id"]), (
            f"the closed run for {period} carries no payslip rows"
        )
    fresh = console.run(FRESH_PERIOD, GROUP_CORE)
    assert fresh is not None, f"the seeded open run for {FRESH_PERIOD} is missing"
    open_row = open_run_row(console)
    assert str(open_row.get("period")) == OPEN_PERIOD, (
        f"the run read for {OPEN_PERIOD} reports period {open_row.get('period')!r}"
    )
    escalated = [c for c in console.approvals(kind="claim")
                 if str(c.get("approver_role")) == "payroll"]
    assert escalated, (
        f"the seed carries a claim of {ESCALATED_CLAIM_MINOR} minor units above the "
        f"manager limit, so at least one claim approval waits on a payroll account"
    )
