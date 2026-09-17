from __future__ import annotations

import concurrent.futures
import json
import os

import httpx
from _shapes import flatten, items
from appclient import api_base, app_url, login, seeded_password
from conftest import (
    APPROVAL_STEP,
    CODE_STEP_MUTATE,
    CODE_STEP_REACH_HOST,
    CODE_STEP_SPIN,
    INTERNAL_URLS,
    RUN_STATUSES,
    APPROVER2_EMAIL,
    APPROVER_EMAIL,
    CORPUS_PASSWORD,
    INCIDENT_TRIAGE,
    LEAD_HANDOFF,
    NIGHTLY_BACKUP,
    OPERATOR_EMAIL,
    OWNER_EMAIL,
    PLATFORM_OPS,
    REVENUE_OPS,
    SEEDED_STEPS,
    contact_payload,
    deadline_budget,
    failed_step,
    fetch,
    page,
    poll_until,
    run_to_rest,
    save_probe_workflow,
    settle,
    start_run,
    step_row,
    unique_email,
    unique_ref,
    fresh_waiting_run,
    workflow_id_by_name,
)


def test_health_endpoint_returns_200():
    response = httpx.get(f"{api_base()}/health", timeout=30.0)
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, and the deployment "
        f"contract pins 200 once the app is ready: {response.text[:400]}")


def test_operator_login_returns_token():
    token = login(OPERATOR_EMAIL, seeded_password("SEED_PASSWORD", CORPUS_PASSWORD))
    assert isinstance(token, str) and token.strip(), (
        f"POST /api/auth/login for {OPERATOR_EMAIL} returned no usable "
        f"access_token; the seeded password {CORPUS_PASSWORD!r} must work at login")

    bad = httpx.post(
        f"{api_base()}/auth/login",
        json={"email": OPERATOR_EMAIL, "password": "not-the-corpus-password"},
        timeout=30.0,
    )
    assert bad.status_code in (400, 401, 403, 422), (
        f"POST /api/auth/login with a wrong password for {OPERATOR_EMAIL} returned "
        f"{bad.status_code}, and a wrong password must be refused as a client "
        f"error: {bad.text[:400]}")
    assert "access_token" not in bad.text, (
        f"a refused sign-in for {OPERATOR_EMAIL} still handed back an access_token: "
        f"{bad.text[:400]}")


def test_manual_run_is_queued_then_claimed_by_a_worker(operator_client, db):
    workflow_id = workflow_id_by_name(operator_client, PLATFORM_OPS, INCIDENT_TRIAGE)
    created = start_run(operator_client, workflow_id)
    run_id = created.get("id")
    assert run_id is not None, (
        f"POST /api/workflows/{workflow_id}/runs returned no run id: {created}")
    assert created.get("status") in ("new", "running"), (
        f"a newly started run of {INCIDENT_TRIAGE!r} reported status "
        f"{created.get('status')!r}; a run is created at 'new' and placed on the "
        f"queue: {created}")

    def claimed():
        row = db.run_by_id(run_id)
        if row and row.get("status") in ("running", "waiting", "succeeded", "failed"):
            return row
        return None

    row = poll_until(claimed)
    assert row is not None, (
        f"run {run_id} never left status 'new' within the poll budget; a worker "
        f"must claim a queued run")
    assert row.get("worker_id") or row.get("status") in ("waiting", "succeeded", "failed"), (
        f"run {run_id} reached status {row.get('status')!r} with no worker_id "
        f"recorded; claiming a run records the worker that holds it: {row}")


def test_approval_step_parks_the_run_at_waiting(operator_client, db):
    workflow_id = workflow_id_by_name(operator_client, PLATFORM_OPS, INCIDENT_TRIAGE)
    run_id = start_run(operator_client, workflow_id).get("id")

    def parked():
        row = db.run_by_id(run_id)
        return row if row and row.get("status") == "waiting" else None

    row = poll_until(parked)
    assert row is not None, (
        f"run {run_id} of {INCIDENT_TRIAGE!r} never reached status 'waiting'; the "
        f"step {APPROVAL_STEP!r} must park the run for a person")

    approvals = db.approvals_of_run(run_id)
    assert approvals, (
        f"run {run_id} is 'waiting' but carries no approvals row; the approval "
        f"step records what a person has to decide")
    assert any(a.get("step_name") == APPROVAL_STEP for a in approvals), (
        f"run {run_id} carries approval rows for "
        f"{[a.get('step_name') for a in approvals]}, and the seeded workflow parks "
        f"at {APPROVAL_STEP!r}")
    assert any(a.get("decision") == "pending" for a in approvals), (
        f"run {run_id} is 'waiting' but no approval row reads decision 'pending': "
        f"{approvals}")


def test_approver_decision_resumes_the_run_to_succeeded(operator_client,
                                                        approver_client, db):
    queued = fresh_waiting_run(operator_client, approver_client)
    approval_id = queued.get("id")
    run_id = queued.get("run_id")

    response = approver_client.post(
        f"/approvals/{approval_id}/decision", json={"decision": "approved"})
    assert response.status_code in (200, 201), (
        f"POST /api/approvals/{approval_id}/decision as {APPROVER_EMAIL} returned "
        f"{response.status_code}; an approver in the run's project decides it: "
        f"{response.text[:400]}")
    body = response.json()
    assert body.get("decision") == "approved", (
        f"the recorded decision for approval {approval_id} reads "
        f"{body.get('decision')!r} rather than 'approved': {body}")

    def resumed():
        row = db.run_by_id(run_id)
        return row if row and row.get("status") == "succeeded" else None

    row = poll_until(resumed)
    assert row is not None, (
        f"run {run_id} did not reach 'succeeded' after approval; an approved run "
        f"is re-queued and continues from where it stopped")
    assert not row.get("worker_id") or row.get("stopped_at"), (
        f"run {run_id} reads 'succeeded' but still looks held by a worker: {row}")


def test_rejection_marks_the_run_failed(operator_client, approver_client, db):
    workflow_id = workflow_id_by_name(operator_client, PLATFORM_OPS, INCIDENT_TRIAGE)
    run_id = start_run(operator_client, workflow_id).get("id")

    def parked():
        rows = db.approvals_of_run(run_id)
        return rows if rows and any(r.get("decision") == "pending" for r in rows) else None

    rows = poll_until(parked)
    assert rows is not None, (
        f"run {run_id} never produced a pending approval to reject")
    approval_id = [r for r in rows if r.get("decision") == "pending"][0]["id"]

    response = approver_client.post(
        f"/approvals/{approval_id}/decision", json={"decision": "rejected"})
    assert response.status_code in (200, 201), (
        f"POST /api/approvals/{approval_id}/decision with 'rejected' returned "
        f"{response.status_code}: {response.text[:400]}")

    def failed():
        row = db.run_by_id(run_id)
        return row if row and row.get("status") == "failed" else None

    row = poll_until(failed)
    assert row is not None, (
        f"run {run_id} did not reach 'failed' after a rejection; a rejected run "
        f"fails rather than continuing")

    steps = db.steps_of_run(run_id)
    after = [s for s in steps if s.get("step_name") == "Post to channel"]
    assert all(s.get("status") in ("skipped", "pending") for s in after), (
        f"run {run_id} was rejected but the step after {APPROVAL_STEP!r} reads "
        f"{[s.get('status') for s in after]}; steps after a rejected approval are "
        f"skipped, never run")


def test_plan_prices_switch_between_monthly_and_annual():
    monthly = httpx.get(f"{api_base()}/plans", params={"period": "monthly"}, timeout=30.0)
    annual = httpx.get(f"{api_base()}/plans", params={"period": "annual"}, timeout=30.0)
    assert monthly.status_code == 200 and annual.status_code == 200, (
        f"GET /api/plans returned {monthly.status_code} for monthly and "
        f"{annual.status_code} for annual: {monthly.text[:200]} / {annual.text[:200]}")

    monthly_rows = items(monthly.json())
    annual_rows = items(annual.json())
    assert len(monthly_rows) == 4, (
        f"GET /api/plans returned {len(monthly_rows)} plans; the brief pins four: "
        f"Starter, Pro, Business, Enterprise")

    by_name_monthly = {r.get("name"): r for r in monthly_rows}
    by_name_annual = {r.get("name"): r for r in annual_rows}
    for name in ("Starter", "Pro", "Business", "Enterprise"):
        assert name in by_name_monthly, (
            f"plan {name!r} is missing from GET /api/plans; the four plan names "
            f"are pinned: {sorted(by_name_monthly)}")

    expected = {"Starter": (2900, 2400), "Pro": (7200, 6000), "Business": (80000, 66700)}
    for name, (month_cents, annual_cents) in expected.items():
        blob_m = flatten(by_name_monthly[name])
        blob_a = flatten(by_name_annual[name])
        assert str(month_cents) in blob_m, (
            f"plan {name!r} under the monthly period does not carry {month_cents} "
            f"minor units anywhere in its payload: {blob_m[:400]}")
        assert str(annual_cents) in blob_a, (
            f"plan {name!r} under the annual period does not carry {annual_cents} "
            f"minor units anywhere in its payload: {blob_a[:400]}")


def test_catalogue_search_filters_and_counts(db):
    seeded = db.count_connectors()
    assert seeded == 30, (
        f"the connectors table holds {seeded} rows; the brief seeds 30 across "
        f"eight categories")

    unfiltered = httpx.get(f"{api_base()}/connectors", timeout=30.0)
    assert unfiltered.status_code == 200, (
        f"GET /api/connectors returned {unfiltered.status_code}: "
        f"{unfiltered.text[:400]}")
    body = unfiltered.json()
    assert body.get("total") == 30, (
        f"GET /api/connectors reported total {body.get('total')!r}; 30 connectors "
        f"are seeded: {flatten(body)[:300]}")
    assert body.get("per_page") == 24, (
        f"GET /api/connectors reported per_page {body.get('per_page')!r}; the "
        f"default page size is 24")
    assert len(body.get("results") or []) <= 24, (
        f"GET /api/connectors returned {len(body.get('results') or [])} results on "
        f"one page, above the default page size of 24")

    typed = httpx.get(f"{api_base()}/connectors",
                      params={"type": "trigger"}, timeout=30.0)
    assert typed.status_code == 200, (
        f"GET /api/connectors?type=trigger returned {typed.status_code}: "
        f"{typed.text[:400]}")
    typed_body = typed.json()
    assert typed_body.get("total") <= 30, (
        f"filtering by type raised the total to {typed_body.get('total')!r}, above "
        f"the 30 seeded connectors")
    for row in typed_body.get("results") or []:
        assert row.get("node_type") == "trigger", (
            f"GET /api/connectors?type=trigger returned a row whose node_type is "
            f"{row.get('node_type')!r}: {row}")
    assert "facets" in typed_body, (
        f"GET /api/connectors returned no facets block; facet counts follow the "
        f"active filters: {flatten(typed_body)[:300]}")


def test_case_study_article_carries_its_quote():
    index = httpx.get(f"{api_base()}/case-studies", timeout=30.0)
    assert index.status_code == 200, (
        f"GET /api/case-studies returned {index.status_code}: {index.text[:400]}")
    rows = items(index.json())
    assert len(rows) == 4, (
        f"GET /api/case-studies returned {len(rows)} rows; the brief seeds four")

    vantage = [r for r in rows if r.get("customer_name") == "Vantage"]
    assert vantage, (
        f"no seeded case study names the customer 'Vantage': "
        f"{[r.get('customer_name') for r in rows]}")
    slug = vantage[0].get("slug")

    article = httpx.get(f"{api_base()}/case-studies/{slug}", timeout=30.0)
    assert article.status_code == 200, (
        f"GET /api/case-studies/{slug} returned {article.status_code}: "
        f"{article.text[:400]}")
    body = article.json()
    assert body.get("quote_author") == "Ollie Marchese", (
        f"the Vantage case study reports quote_author {body.get('quote_author')!r}; "
        f"the brief pins 'Ollie Marchese'")
    assert body.get("quote_author_title") == "Chief Technology Officer", (
        f"the Vantage case study reports quote_author_title "
        f"{body.get('quote_author_title')!r}; the brief pins 'Chief Technology "
        f"Officer'")
    assert (body.get("quote") or "").strip(), (
        f"the Vantage case study article carries an empty quote; the card "
        f"truncates it and the article carries it whole: {flatten(body)[:300]}")


def test_saved_workflow_version_is_persisted_and_immutable(operator_client, db):
    workflow_id = workflow_id_by_name(operator_client, PLATFORM_OPS, INCIDENT_TRIAGE)
    before = db.versions_of(workflow_id)
    assert before, (
        f"workflow {workflow_id} ({INCIDENT_TRIAGE!r}) carries no workflow_versions "
        f"rows; every save writes one and the seed pins version 1")
    baseline = {row["id"]: dict(row) for row in before}

    step_name = unique_ref("Notify")
    current = operator_client.get(f"/workflows/{workflow_id}")
    assert current.status_code == 200, (
        f"GET /api/workflows/{workflow_id} returned {current.status_code}: "
        f"{current.text[:400]}")
    graph = current.json()
    steps = list(graph.get("steps") or [])
    steps.append({"name": step_name, "step_type": "regular",
                  "position_x": 900, "position_y": 200, "on_error": "stop",
                  "disabled": False})

    saved = operator_client.post(
        f"/workflows/{workflow_id}/versions",
        json={"message": "verifier probe", "steps": steps,
              "connections": graph.get("connections") or []})
    assert saved.status_code in (200, 201), (
        f"POST /api/workflows/{workflow_id}/versions returned {saved.status_code}: "
        f"{saved.text[:400]}")

    after = db.versions_of(workflow_id)
    assert len(after) == len(before) + 1, (
        f"saving produced {len(after) - len(before)} new workflow_versions rows; a "
        f"save writes exactly one new version")

    for row in after:
        if row["id"] in baseline:
            assert dict(row) == baseline[row["id"]], (
                f"workflow_versions row {row['id']} changed when a new version was "
                f"saved; a version is never rewritten once stored. before="
                f"{baseline[row['id']]} after={dict(row)}")


def test_seeded_rows_exist_for_every_project_and_workflow(db):
    for slug in (PLATFORM_OPS, REVENUE_OPS):
        assert db.project_by_slug(slug) is not None, (
            f"no projects row with slug {slug!r}; the brief seeds both "
            f"{PLATFORM_OPS!r} and {REVENUE_OPS!r}")

    for email in (OWNER_EMAIL, APPROVER_EMAIL, APPROVER2_EMAIL, OPERATOR_EMAIL):
        assert db.user_by_email(email) is not None, (
            f"no users row for {email!r}; the brief seeds five accounts")

    for name in (INCIDENT_TRIAGE, NIGHTLY_BACKUP, LEAD_HANDOFF):
        assert db.workflow_by_name(name) is not None, (
            f"no workflows row named {name!r}; the brief seeds three workflows")

    assert db.count_plans() == 4, (
        f"the plans table holds {db.count_plans()} rows; the brief seeds four")

    triage = db.workflow_by_name(INCIDENT_TRIAGE)
    versions = db.versions_of(triage["id"])
    assert versions, (
        f"{INCIDENT_TRIAGE!r} carries no workflow_versions row, though the brief "
        f"seeds version 1 with five steps")


def test_run_steps_record_one_row_per_attempt(operator_client, db):
    workflow_id = workflow_id_by_name(operator_client, PLATFORM_OPS, INCIDENT_TRIAGE)
    run_id = start_run(operator_client, workflow_id).get("id")

    def stepped():
        rows = db.steps_of_run(run_id)
        return rows if len(rows) >= 2 else None

    rows = poll_until(stepped)
    assert rows is not None, (
        f"run {run_id} produced fewer than two run_steps rows; each step that runs "
        f"records its own row")

    for row in rows:
        assert row.get("step_name") in SEEDED_STEPS, (
            f"run {run_id} recorded a step named {row.get('step_name')!r}, which is "
            f"not one of the seeded steps {SEEDED_STEPS}")
        assert int(row.get("attempt") or 0) >= 1, (
            f"run_steps row {row.get('id')} reports attempt "
            f"{row.get('attempt')!r}; attempts count from 1")

    seen = [(r.get("step_name"), r.get("attempt")) for r in rows]
    assert len(seen) == len(set(seen)), (
        f"run {run_id} carries two run_steps rows for the same step name at the "
        f"same attempt number, so a retry replaced a row rather than appending "
        f"one: {seen}")


def test_idempotent_inbound_call_stores_no_second_run(db):
    triage = db.workflow_by_name(INCIDENT_TRIAGE)
    slug = triage.get("slug") or "incident-triage"
    key = unique_ref("idem")
    before = db.count_runs(workflow_id=triage["id"])

    first = httpx.post(f"{api_base()}/hooks/{slug}", json={"probe": key},
                       headers={"Idempotency-Key": key}, timeout=30.0)
    assert first.status_code in (200, 201, 202), (
        f"POST /api/hooks/{slug} returned {first.status_code} on a first call: "
        f"{first.text[:400]}")
    first_run = first.json().get("run_id")
    assert first_run is not None, (
        f"the inbound receiver returned no run_id: {first.text[:400]}")

    second = httpx.post(f"{api_base()}/hooks/{slug}", json={"probe": key},
                        headers={"Idempotency-Key": key}, timeout=30.0)
    assert second.status_code in (200, 201, 202), (
        f"POST /api/hooks/{slug} returned {second.status_code} on a repeat carrying "
        f"the same Idempotency-Key: {second.text[:400]}")
    assert second.json().get("run_id") == first_run, (
        f"a repeat carrying Idempotency-Key {key!r} returned run "
        f"{second.json().get('run_id')!r} rather than the original {first_run!r}")

    settle()
    after = db.count_runs(workflow_id=triage["id"])
    assert after == before + 1, (
        f"two calls carrying one Idempotency-Key created {after - before} runs of "
        f"{INCIDENT_TRIAGE!r}; a repeat within the window starts no second run")


def test_waiting_run_holds_no_worker_row(operator_client, db):
    workflow_id = workflow_id_by_name(operator_client, PLATFORM_OPS, INCIDENT_TRIAGE)
    run_id = start_run(operator_client, workflow_id).get("id")

    def parked():
        row = db.run_by_id(run_id)
        return row if row and row.get("status") == "waiting" else None

    row = poll_until(parked)
    assert row is not None, (
        f"run {run_id} never reached 'waiting', so the worker-release rule could "
        f"not be observed")
    assert not row.get("worker_id"), (
        f"run {run_id} reads status 'waiting' while still recording worker_id "
        f"{row.get('worker_id')!r}; a paused run releases its worker entirely, so "
        f"a thousand paused runs cost rows rather than workers")

    for other in db.runs_with_status("waiting"):
        assert not other.get("worker_id"), (
            f"run {other.get('id')} reads 'waiting' while holding worker_id "
            f"{other.get('worker_id')!r}")


def test_approval_token_is_single_use_and_decision_survives_replay(operator_client, db):
    workflow_id = workflow_id_by_name(operator_client, PLATFORM_OPS, INCIDENT_TRIAGE)
    run_id = start_run(operator_client, workflow_id).get("id")

    def parked():
        rows = db.approvals_of_run(run_id)
        return rows if rows and any(r.get("approve_token") for r in rows) else None

    rows = poll_until(parked)
    assert rows is not None, (
        f"run {run_id} produced no approval carrying an approve_token")
    approval = [r for r in rows if r.get("approve_token")][0]
    token = approval["approve_token"]

    first = httpx.post(f"{api_base()}/approvals/token/{token}", timeout=30.0)
    assert first.status_code in (200, 201), (
        f"POST /api/approvals/token/<token> returned {first.status_code} on its "
        f"first use: {first.text[:400]}")

    settle()
    recorded = [r for r in db.approvals_of_run(run_id) if r["id"] == approval["id"]][0]
    decision_after_first = recorded.get("decision")
    assert decision_after_first in ("approved", "rejected"), (
        f"using the minted address left approval {approval['id']} at decision "
        f"{decision_after_first!r}; presenting it records a decision")

    second = httpx.post(f"{api_base()}/approvals/token/{token}", timeout=30.0)
    assert second.status_code in (400, 403, 404, 409, 410, 422), (
        f"POST /api/approvals/token/<token> returned {second.status_code} on a "
        f"SECOND use; each minted address works once: {second.text[:400]}")

    settle()
    final = [r for r in db.approvals_of_run(run_id) if r["id"] == approval["id"]][0]
    assert final.get("decision") == decision_after_first, (
        f"replaying the single-use address changed the recorded decision from "
        f"{decision_after_first!r} to {final.get('decision')!r}")


def test_audit_event_is_stored_for_every_approval_decision(operator_client,
                                                           approver_client, db):
    workflow_id = workflow_id_by_name(operator_client, PLATFORM_OPS, INCIDENT_TRIAGE)
    run_id = start_run(operator_client, workflow_id).get("id")

    def parked():
        rows = db.approvals_of_run(run_id)
        return rows if rows and any(r.get("decision") == "pending" for r in rows) else None

    rows = poll_until(parked)
    assert rows is not None, (
        f"run {run_id} produced no pending approval to decide")
    approval_id = [r for r in rows if r.get("decision") == "pending"][0]["id"]

    before = db.count_audit(actor_email=APPROVER_EMAIL)
    response = approver_client.post(
        f"/approvals/{approval_id}/decision", json={"decision": "approved"})
    assert response.status_code in (200, 201), (
        f"POST /api/approvals/{approval_id}/decision returned "
        f"{response.status_code}: {response.text[:400]}")

    def recorded():
        after = db.count_audit(actor_email=APPROVER_EMAIL)
        return after if after > before else None

    after = poll_until(recorded)
    assert after is not None, (
        f"deciding approval {approval_id} as {APPROVER_EMAIL} added no "
        f"audit_events row; every approval decision is an audit event")


def test_contact_request_is_stored_with_its_consent_text(db):
    email = unique_email()
    response = httpx.post(f"{api_base()}/contact", json=contact_payload(email),
                          timeout=30.0)
    assert response.status_code in (200, 201), (
        f"POST /api/contact returned {response.status_code} for a valid "
        f"submission: {response.text[:400]}")

    def stored():
        return db.contact_request_by_email(email)

    row = poll_until(stored)
    assert row is not None, (
        f"a valid submission for {email!r} wrote no contact_requests row")
    assert row.get("consent") in (True, 1, "true", "t"), (
        f"contact_requests row for {email!r} records consent "
        f"{row.get('consent')!r}; consent must be stored as given")
    assert (row.get("consent_text") or "").strip(), (
        f"contact_requests row for {email!r} carries no consent_text; the wording "
        f"shown at the time is stored with the decision: {row}")
    assert row.get("consent_at") is not None, (
        f"contact_requests row for {email!r} carries no consent_at timestamp: {row}")
    assert row.get("campaign_source") == "probe-source", (
        f"contact_requests row for {email!r} records campaign_source "
        f"{row.get('campaign_source')!r}; the hidden campaign fields travel with "
        f"the request")
    assert row.get("campaign_medium") == "probe-medium", (
        f"contact_requests row for {email!r} records campaign_medium "
        f"{row.get('campaign_medium')!r}")
    assert row.get("campaign_name") == "probe-campaign", (
        f"contact_requests row for {email!r} records campaign_name "
        f"{row.get('campaign_name')!r}")


def test_operator_approval_is_denied_and_run_untouched(operator_client,
                                                       approver_client, db):
    queued = fresh_waiting_run(operator_client, approver_client)
    approval_id = queued.get("id")
    run_id = queued.get("run_id")

    before_run = dict(db.run_by_id(run_id) or {})
    assert before_run.get("status") == "waiting", (
        f"run {run_id} reads status {before_run.get('status')!r} rather than "
        f"'waiting' before the denial probe")
    before_approvals = [dict(r) for r in db.approvals_of_run(run_id)]

    response = operator_client.post(
        f"/approvals/{approval_id}/decision", json={"decision": "approved"})
    assert response.status_code in (401, 403), (
        f"POST /api/approvals/{approval_id}/decision from an {OPERATOR_EMAIL} "
        f"session returned {response.status_code}; only an approver or an owner in "
        f"the run's project decides it, and the server must refuse the rest: "
        f"{response.text[:400]}")

    settle()
    after_run = dict(db.run_by_id(run_id) or {})
    assert after_run.get("status") == "waiting", (
        f"the denied request still moved run {run_id} from 'waiting' to "
        f"{after_run.get('status')!r}; a denied mutation leaves the row unchanged")
    assert after_run.get("stopped_at") == before_run.get("stopped_at"), (
        f"run {run_id} gained a stopped_at of {after_run.get('stopped_at')!r} from a "
        f"request the server refused")

    after_approvals = [dict(r) for r in db.approvals_of_run(run_id)]
    assert after_approvals == before_approvals, (
        f"the denied decision changed the approvals rows for run {run_id}. "
        f"before={before_approvals} after={after_approvals}")
    assert all(r.get("decision") == "pending" for r in after_approvals), (
        f"approval rows for run {run_id} read "
        f"{[r.get('decision') for r in after_approvals]} after a refused request; "
        f"no decision may be recorded")
    assert all(not r.get("decided_by_id") for r in after_approvals), (
        f"a refused request recorded a decider on run {run_id}: {after_approvals}")


def test_cross_project_approver_is_denied(operator_client, approver2_client,
                                          approver_client, db):
    queued = fresh_waiting_run(operator_client, approver_client)
    approval_id = queued.get("id")
    run_id = queued.get("run_id")
    before = [dict(r) for r in db.approvals_of_run(run_id)]

    response = approver2_client.post(
        f"/approvals/{approval_id}/decision", json={"decision": "approved"})
    assert response.status_code in (401, 403, 404), (
        f"POST /api/approvals/{approval_id}/decision from {APPROVER2_EMAIL}, who "
        f"belongs to {REVENUE_OPS!r} and not to {PLATFORM_OPS!r}, returned "
        f"{response.status_code}; an approver decides only inside a project they "
        f"belong to: {response.text[:400]}")

    settle()
    after = [dict(r) for r in db.approvals_of_run(run_id)]
    assert after == before, (
        f"the cross-project request changed the approvals rows for run {run_id}. "
        f"before={before} after={after}")

    listing = approver2_client.get(f"/projects/{PLATFORM_OPS}/approvals")
    assert listing.status_code in (401, 403, 404), (
        f"GET /api/projects/{PLATFORM_OPS}/approvals as {APPROVER2_EMAIL} returned "
        f"{listing.status_code}; a person outside a project reads nothing in it: "
        f"{listing.text[:400]}")


def test_anonymous_console_request_is_unauthenticated(anon_client):
    for path in (f"/projects/{PLATFORM_OPS}/workflows",
                 f"/projects/{PLATFORM_OPS}/runs",
                 f"/projects/{PLATFORM_OPS}/approvals",
                 f"/projects/{PLATFORM_OPS}/credentials",
                 "/me"):
        response = anon_client.get(path)
        assert response.status_code in (401, 403), (
            f"GET /api{path} with no bearer token returned {response.status_code}; "
            f"a console endpoint is refused to an anonymous caller: "
            f"{response.text[:400]}")


def test_credential_value_is_never_returned_to_any_role(owner_client,
                                                        approver_client,
                                                        operator_client):
    secret = unique_ref("probe-secret")
    created = owner_client.post(
        f"/projects/{PLATFORM_OPS}/credentials",
        json={"name": unique_ref("Probe credential"),
              "credential_type": "header_auth", "secret": secret})
    assert created.status_code in (200, 201), (
        f"POST /api/projects/{PLATFORM_OPS}/credentials as {OWNER_EMAIL} returned "
        f"{created.status_code}; an owner creates credentials: "
        f"{created.text[:400]}")
    assert secret not in created.text, (
        f"the create response handed the stored value back: {created.text[:400]}")
    credential_id = created.json().get("id")

    listing = owner_client.get(f"/projects/{PLATFORM_OPS}/credentials")
    assert listing.status_code == 200, (
        f"GET /api/projects/{PLATFORM_OPS}/credentials as {OWNER_EMAIL} returned "
        f"{listing.status_code}: {listing.text[:400]}")
    assert secret not in listing.text, (
        f"the credential list handed back the stored value for credential "
        f"{credential_id}; the interface shows which fields are set, never what "
        f"is in them: {listing.text[:600]}")

    detail = owner_client.get(f"/projects/{PLATFORM_OPS}/credentials/{credential_id}")
    assert secret not in detail.text, (
        f"reading credential {credential_id} as {OWNER_EMAIL} returned the stored "
        f"value: {detail.text[:600]}")

    for label, client_ in ((APPROVER_EMAIL, approver_client),
                           (OPERATOR_EMAIL, operator_client)):
        lower = client_.get(f"/projects/{PLATFORM_OPS}/credentials")
        assert lower.status_code in (401, 403), (
            f"GET /api/projects/{PLATFORM_OPS}/credentials as {label} returned "
            f"{lower.status_code}; only an owner reads the credential list: "
            f"{lower.text[:400]}")
        assert secret not in lower.text, (
            f"the refusal for {label} still leaked the stored value: "
            f"{lower.text[:400]}")


def test_operator_cannot_read_the_audit_stream(operator_client, approver_client,
                                               owner_client):
    for label, client_ in ((OPERATOR_EMAIL, operator_client),
                           (APPROVER_EMAIL, approver_client)):
        response = client_.get(f"/projects/{PLATFORM_OPS}/audit")
        assert response.status_code in (401, 403), (
            f"GET /api/projects/{PLATFORM_OPS}/audit as {label} returned "
            f"{response.status_code}; the audit stream is readable only by an "
            f"owner: {response.text[:400]}")
        members = client_.get(f"/projects/{PLATFORM_OPS}/members")
        assert members.status_code in (401, 403), (
            f"GET /api/projects/{PLATFORM_OPS}/members as {label} returned "
            f"{members.status_code}; the member list is an owner surface: "
            f"{members.text[:400]}")

    allowed = owner_client.get(f"/projects/{PLATFORM_OPS}/audit")
    assert allowed.status_code == 200, (
        f"GET /api/projects/{PLATFORM_OPS}/audit as {OWNER_EMAIL} returned "
        f"{allowed.status_code}; an owner reads the audit stream: "
        f"{allowed.text[:400]}")
    assert isinstance(allowed.json(), list), (
        f"GET /api/projects/{PLATFORM_OPS}/audit must return a top-level JSON "
        f"array: {allowed.text[:400]}")


def test_owner_can_change_membership(owner_client, operator_client,
                                    operator2_client, db):
    listing = owner_client.get(f"/projects/{PLATFORM_OPS}/members")
    assert listing.status_code == 200, (
        f"GET /api/projects/{PLATFORM_OPS}/members as {OWNER_EMAIL} returned "
        f"{listing.status_code}: {listing.text[:400]}")
    rows = listing.json()
    assert isinstance(rows, list) and rows, (
        f"GET /api/projects/{PLATFORM_OPS}/members returned no members, though the "
        f"brief seeds three: {listing.text[:400]}")

    emails = {r.get("email") for r in rows}
    for expected in (OWNER_EMAIL, APPROVER_EMAIL, OPERATOR_EMAIL):
        assert expected in emails, (
            f"{expected!r} is missing from the {PLATFORM_OPS!r} member list: "
            f"{sorted(emails)}")
    assert OPERATOR2_EMAIL not in emails, (
        f"{OPERATOR2_EMAIL!r} appears in the {PLATFORM_OPS!r} member list, but the "
        f"brief seeds that account into {REVENUE_OPS!r} only: {sorted(emails)}")

    for row in rows:
        assert row.get("project_role") in ("admin", "editor", "viewer"), (
            f"member {row.get('email')!r} carries project_role "
            f"{row.get('project_role')!r}, outside the pinned three")

    blocked = operator2_client.get(f"/projects/{PLATFORM_OPS}/members")
    assert blocked.status_code in (401, 403, 404), (
        f"GET /api/projects/{PLATFORM_OPS}/members as {OPERATOR2_EMAIL} returned "
        f"{blocked.status_code}; that account belongs to another project: "
        f"{blocked.text[:400]}")

    target = [r for r in rows if r.get("email") == OPERATOR_EMAIL][0]
    was = target.get("project_role")
    user_id = target.get("user_id")
    before_audit = db.count_audit(actor_email=OWNER_EMAIL)

    changed = owner_client.patch(
        f"/projects/{PLATFORM_OPS}/members/{user_id}", json={"project_role": "viewer"})
    assert changed.status_code in (200, 201), (
        f"PATCH /api/projects/{PLATFORM_OPS}/members/{user_id} as {OWNER_EMAIL} "
        f"returned {changed.status_code}; an owner changes a member's project "
        f"role: {changed.text[:400]}")
    assert changed.json().get("project_role") == "viewer", (
        f"the membership for {OPERATOR_EMAIL} reads project_role "
        f"{changed.json().get('project_role')!r} after a change to 'viewer'")

    def recorded():
        after = db.count_audit(actor_email=OWNER_EMAIL)
        return after if after > before_audit else None

    assert poll_until(recorded) is not None, (
        f"changing the project role of {OPERATOR_EMAIL} added no audit_events row "
        f"for {OWNER_EMAIL}; every membership change is recorded with its actor")

    refused = operator_client.patch(
        f"/projects/{PLATFORM_OPS}/members/{user_id}", json={"project_role": "admin"})
    assert refused.status_code in (401, 403), (
        f"PATCH /api/projects/{PLATFORM_OPS}/members/{user_id} from an "
        f"{OPERATOR_EMAIL} session returned {refused.status_code}; only an owner "
        f"changes membership: {refused.text[:400]}")

    restored = owner_client.patch(
        f"/projects/{PLATFORM_OPS}/members/{user_id}", json={"project_role": was})
    assert restored.status_code in (200, 201), (
        f"restoring {OPERATOR_EMAIL} to project_role {was!r} returned "
        f"{restored.status_code}: {restored.text[:400]}")


def test_two_concurrent_claims_leave_exactly_one_winner(operator_client, db):
    workflow_id = workflow_id_by_name(operator_client, PLATFORM_OPS, INCIDENT_TRIAGE)
    run_id = start_run(operator_client, workflow_id).get("id")

    url = f"{api_base()}/runs/{run_id}/claim"
    worker_a = unique_ref("worker-a")
    worker_b = unique_ref("worker-b")

    def claim(worker_id: str) -> int:
        return httpx.post(url, json={"worker_id": worker_id}, timeout=30.0).status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(claim, worker_a), pool.submit(claim, worker_b)]
        codes = sorted(f.result() for f in futures)

    winners = [c for c in codes if c in (200, 201)]
    losers = [c for c in codes if c in (400, 403, 404, 409, 410, 422)]
    assert len(winners) == 1, (
        f"two simultaneous claims of run {run_id} returned {codes}; exactly one "
        f"must win and the other must be refused")
    assert len(losers) == 1, (
        f"two simultaneous claims of run {run_id} returned {codes}; the loser must "
        f"be refused as a client error rather than served or crashed")

    settle()
    row = db.run_by_id(run_id)
    assert row is not None, f"run {run_id} disappeared after two concurrent claims"
    holder = row.get("worker_id")
    assert holder in (worker_a, worker_b, None), (
        f"run {run_id} records worker_id {holder!r}, which is neither claimant")
    if holder is not None:
        assert holder in (worker_a, worker_b), (
            f"run {run_id} ended up held by {holder!r}, which neither claim sent")


def test_expired_approval_deadline_is_a_distinct_outcome(operator_client, db):
    configured = os.environ.get("APPROVAL_DEADLINE_SEC")
    assert configured, (
        "APPROVAL_DEADLINE_SEC is unset in the verifier environment, so the "
        "approval deadline cannot be observed without waiting on a wall clock")

    workflow_id = workflow_id_by_name(operator_client, PLATFORM_OPS, INCIDENT_TRIAGE)
    run_id = start_run(operator_client, workflow_id).get("id")

    def parked():
        rows = db.approvals_of_run(run_id)
        return rows if rows and any(r.get("decision") == "pending" for r in rows) else None

    rows = poll_until(parked)
    assert rows is not None, (
        f"run {run_id} produced no pending approval whose deadline could lapse")
    approval_id = [r for r in rows if r.get("decision") == "pending"][0]["id"]

    def expired():
        response = httpx.get(f"{api_base()}/runs/{run_id}", timeout=30.0)
        if response.status_code != 200:
            return None
        current = [r for r in db.approvals_of_run(run_id) if r["id"] == approval_id]
        if current and current[0].get("decision") == "expired":
            return current[0]
        return None

    row = poll_until(expired, budget=deadline_budget())
    assert row is not None, (
        f"approval {approval_id} on run {run_id} never read 'expired' within twice "
        f"the configured deadline of {configured}s; running out of time is its own "
        f"outcome, distinct from a rejection, and is computed when the approval is "
        f"next read")
    assert row.get("decision") == "expired", (
        f"approval {approval_id} reads decision {row.get('decision')!r}; an "
        f"approval past its deadline is 'expired', never 'rejected'")
    assert not row.get("decided_by_id"), (
        f"approval {approval_id} expired but records a decider "
        f"{row.get('decided_by_id')!r}; nobody decided it")


def test_invalid_contact_form_is_refused_with_nothing_written(db):
    before = db.count_contact_requests()

    bad_email = httpx.post(f"{api_base()}/contact",
                           json=contact_payload("not-an-address"), timeout=30.0)
    assert bad_email.status_code in (400, 422), (
        f"POST /api/contact with an email that is not an address returned "
        f"{bad_email.status_code}; invalid input is rejected as a client error: "
        f"{bad_email.text[:400]}")
    assert "email" in bad_email.text.lower(), (
        f"the rejection does not name the field that is wrong: "
        f"{bad_email.text[:400]}")

    no_consent = httpx.post(f"{api_base()}/contact",
                            json=contact_payload(unique_email(), consent=False),
                            timeout=30.0)
    assert no_consent.status_code in (400, 422), (
        f"POST /api/contact with consent false returned {no_consent.status_code}; "
        f"consent is required and must be true: {no_consent.text[:400]}")

    settle()
    after = db.count_contact_requests()
    assert after == before, (
        f"two refused submissions wrote {after - before} contact_requests rows; a "
        f"rejected submission writes nothing")


def test_spam_decoy_field_submission_is_refused(db):
    before = db.count_contact_requests()
    email = unique_email()

    payload = contact_payload(email)
    payload["website"] = "https://example.com/bot"
    payload["nickname"] = "bot"
    decoy = httpx.post(f"{api_base()}/contact", json=payload, timeout=30.0)
    assert decoy.status_code in (400, 403, 422), (
        f"POST /api/contact carrying a filled unattended decoy field returned "
        f"{decoy.status_code}; a submission that fills a field no person sees is "
        f"refused: {decoy.text[:400]}")

    burst = [httpx.post(f"{api_base()}/contact", json=contact_payload(unique_email()),
                        timeout=30.0).status_code for _ in range(8)]
    assert any(code in (400, 403, 429) for code in burst), (
        f"eight submissions in quick succession from one address all returned "
        f"{burst}; a form submitted repeatedly in quick succession is refused")

    settle()
    after = db.count_contact_requests()
    assert after <= before + len(burst), (
        f"the refused decoy submission still wrote a row: before={before} "
        f"after={after}")
    assert db.contact_request_by_email(email) is None, (
        f"the decoy submission for {email!r} was stored despite being refused")


def test_catalogue_page_past_the_last_page_returns_empty():
    response = httpx.get(f"{api_base()}/connectors",
                         params={"page": 99, "per_page": 24}, timeout=30.0)
    assert response.status_code == 200, (
        f"GET /api/connectors?page=99 returned {response.status_code}; a page past "
        f"the last one is an empty result set, never an error: "
        f"{response.text[:400]}")
    body = response.json()
    assert body.get("results") == [], (
        f"GET /api/connectors?page=99 returned {len(body.get('results') or [])} "
        f"results; past the last page the result set is empty")
    assert body.get("total") == 30, (
        f"GET /api/connectors?page=99 reported total {body.get('total')!r}; the "
        f"total stays correct past the last page, and 30 connectors are seeded")

    oversized = httpx.get(f"{api_base()}/connectors",
                          params={"per_page": 500}, timeout=30.0)
    assert oversized.status_code in (200, 400, 422), (
        f"GET /api/connectors?per_page=500 returned {oversized.status_code}: "
        f"{oversized.text[:400]}")
    if oversized.status_code == 200:
        assert len(oversized.json().get("results") or []) <= 60, (
            f"GET /api/connectors?per_page=500 returned "
            f"{len(oversized.json().get('results') or [])} results, above the "
            f"maximum page size of 60")


def test_unknown_address_answers_not_found():
    for path in (f"/{unique_ref('no-such-page')}", "/as", "/gs", "/g/d"):
        response = httpx.get(page(path), timeout=30.0, follow_redirects=True)
        assert response.status_code == 404, (
            f"GET {path} returned {response.status_code}; an unknown address "
            f"answers not found rather than answering as though the page existed")
        body = response.text.lower()
        assert "ooops" in body or "not found" in body or "404" in body, (
            f"GET {path} answered 404 with no not-found page rendered; the "
            f"product's own page carries a way back: {response.text[:300]}")


def test_public_routes_carry_distinct_titles_and_descriptions():
    routes = ["/", "/product", "/ai", "/pricing", "/integrations", "/enterprise",
              "/case-studies", "/contact", "/vs", "/legal/privacy"]
    titles, descriptions = {}, {}
    for route in routes:
        response = fetch(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}; it is a public route: "
            f"{response.text[:300]}")
        html = response.text
        lowered = html.lower()

        start = lowered.find("<title")
        assert start != -1, f"GET {route} returned a document with no title element"
        open_end = lowered.find(">", start)
        close = lowered.find("</title>", open_end)
        title = html[open_end + 1:close].strip()
        assert title, f"GET {route} returned an empty title element"
        titles[route] = title

        marker = lowered.find('name="description"')
        if marker == -1:
            marker = lowered.find("name='description'")
        assert marker != -1, (
            f"GET {route} declares no meta description; every public route carries "
            f"its own")
        tag_start = lowered.rfind("<meta", 0, marker)
        tag_end = lowered.find(">", marker)
        descriptions[route] = html[tag_start:tag_end].strip()

    duplicates = [t for t in titles.values() if list(titles.values()).count(t) > 1]
    assert not duplicates, (
        f"these routes share a title, and no two routes may: "
        f"{sorted({t for t in duplicates})}")
    dupe_descriptions = [d for d in descriptions.values()
                         if list(descriptions.values()).count(d) > 1]
    assert not dupe_descriptions, (
        f"two public routes share a meta description: "
        f"{sorted({d[:80] for d in dupe_descriptions})}")


def test_favicon_is_served_and_declared():
    home = fetch("/")
    assert home.status_code == 200, (
        f"GET / returned {home.status_code}: {home.text[:300]}")
    lowered = home.text.lower()
    assert "icon" in lowered and "<link" in lowered, (
        f"the home document declares no icon link element; the site declares its "
        f"favicon in the document head")

    marker = lowered.find('rel="icon"')
    for candidate in ('rel="shortcut icon"', "rel='icon'", 'rel="apple-touch-icon"'):
        if marker == -1:
            marker = lowered.find(candidate)
    assert marker != -1, (
        f"no icon link element found in the home document head: "
        f"{home.text[:600]}")

    tag_start = lowered.rfind("<link", 0, marker)
    tag_end = lowered.find(">", marker)
    tag = home.text[tag_start:tag_end]
    href_marker = tag.lower().find("href=")
    assert href_marker != -1, f"the icon link element declares no href: {tag}"
    quote = tag[href_marker + 5]
    href = tag[href_marker + 6:tag.find(quote, href_marker + 6)]

    target = href if href.startswith("http") else f"{app_url()}{href if href.startswith('/') else '/' + href}"
    served = httpx.get(target, timeout=30.0, follow_redirects=True)
    assert served.status_code == 200, (
        f"the declared favicon at {href!r} answered {served.status_code}; the site "
        f"serves the icon it declares")
    assert served.content, (
        f"the declared favicon at {href!r} answered 200 with an empty body")


def test_security_headers_and_no_frontend_secrets():
    home = fetch("/")
    assert home.status_code == 200, (
        f"GET / returned {home.status_code}: {home.text[:300]}")

    headers = {k.lower(): v for k, v in home.headers.items()}
    assert "strict-transport-security" in headers, (
        f"GET / carries no strict transport policy header; every response carries "
        f"the standard security headers. Saw: {sorted(headers)}")
    assert headers.get("x-content-type-options", "").lower() == "nosniff", (
        f"GET / reports x-content-type-options "
        f"{headers.get('x-content-type-options')!r}; the nosniff content-type "
        f"policy is one of the standard security headers")

    body = home.text
    for leaked in ("deku-local-dev", "flowmark-client-9f14c73e", "AUTH_CLIENT_SECRET",
                   "DB_ADMIN_URL", "AUTH_ADMIN_TOKEN"):
        assert leaked not in body, (
            f"the home document the browser downloads carries {leaked!r}; no "
            f"credential, interface key or admin token appears in anything the "
            f"browser downloads")


def test_user_readme_records_the_seeded_logins():
    readme = "/app/USER_README.md"
    assert os.path.isfile(readme), (
        f"{readme} does not exist; the deployment contract writes the login "
        f"credentials there so a grader can sign in")
    text = open(readme, encoding="utf-8", errors="replace").read()
    assert CORPUS_PASSWORD in text, (
        f"{readme} does not carry the seeded password {CORPUS_PASSWORD!r}, so the "
        f"credentials it records cannot be used")
    for email in (OWNER_EMAIL, APPROVER_EMAIL, OPERATOR_EMAIL):
        assert email in text, (
            f"{readme} does not name the seeded account {email!r}; every seeded "
            f"account is written there alongside the password")
    for reserved in ("/app/.browser_screenshots", "/app/.downloads"):
        assert os.path.isdir(reserved), (
            f"{reserved} does not exist; the deployment contract reserves both "
            f"directories at the app root")


def test_expired_bearer_token_is_refused_and_changes_nothing(operator_client,
                                                             approver_client, db):
    queued = fresh_waiting_run(operator_client, approver_client)
    approval_id = queued.get("id")
    run_id = queued.get("run_id")
    before = [dict(r) for r in db.approvals_of_run(run_id)]

    stale = httpx.Client(base_url=api_base(), timeout=30.0,
                         headers={"Authorization": f"Bearer {unique_ref('stale')}"})
    with stale as c:
        response = c.post(f"/approvals/{approval_id}/decision",
                          json={"decision": "approved"})
        assert response.status_code in (401, 403), (
            f"POST /api/approvals/{approval_id}/decision with a token the server "
            f"never issued returned {response.status_code}; a token that does not "
            f"resolve leaves the action unapplied: {response.text[:400]}")
        listing = c.get(f"/projects/{PLATFORM_OPS}/runs")
        assert listing.status_code in (401, 403), (
            f"GET /api/projects/{PLATFORM_OPS}/runs with an unresolvable token "
            f"returned {listing.status_code}: {listing.text[:400]}")

    settle()
    after = [dict(r) for r in db.approvals_of_run(run_id)]
    assert after == before, (
        f"a request carrying an unresolvable token still changed the approvals "
        f"rows for run {run_id}. before={before} after={after}")


def test_run_logs_are_structured_and_carry_no_secret(operator_client, db):
    queued = fresh_waiting_run(operator_client, operator_client)
    run_id = queued.get("run_id")

    response = operator_client.get(f"/runs/{run_id}/logs")
    assert response.status_code == 200, (
        f"GET /api/runs/{run_id}/logs returned {response.status_code}; a run's "
        f"log records are readable: {response.text[:400]}")
    rows = response.json()
    assert isinstance(rows, list) and rows, (
        f"GET /api/runs/{run_id}/logs returned no records, though the run has "
        f"executed steps: {response.text[:400]}")

    for row in rows:
        for field in ("run_id", "workflow_id", "project_id", "correlation_id",
                      "level", "message", "occurred_at"):
            assert field in row, (
                f"a log record for run {run_id} carries no {field!r}; every record "
                f"carries the run, workflow, project and correlation identifiers "
                f"so one run can be traced across processes: {row}")
        assert str(row.get("correlation_id") or "").strip(), (
            f"a log record for run {run_id} carries an empty correlation_id: {row}")

    correlations = {r.get("correlation_id") for r in rows}
    assert len(correlations) == 1, (
        f"run {run_id} produced {len(correlations)} correlation identifiers; one "
        f"run carries one, which is what makes it traceable: {sorted(correlations)}")

    blob = flatten(rows)
    for secret in (CORPUS_PASSWORD, "deku-local-dev", "flowmark-client-9f14c73e"):
        assert secret not in blob, (
            f"a log record for run {run_id} carries {secret!r}; no credential "
            f"value and no resolved secret appears in a log record")

    for row in db.steps_of_run(run_id):
        assert CORPUS_PASSWORD not in str(row.get("output_summary") or ""), (
            f"run_steps row {row.get('id')} carries the seeded password in its "
            f"output; a credential never reaches the run's stored output")


def test_metrics_expose_the_named_series():
    response = httpx.get(f"{api_base()}/metrics", timeout=30.0)
    assert response.status_code == 200, (
        f"GET /api/metrics returned {response.status_code}; the metrics are "
        f"exposed for scraping: {response.text[:400]}")
    body = response.json()
    for series in ("queue_depth", "jobs_waiting", "jobs_running", "worker_count",
                   "runs_by_status", "active_workflow_count"):
        assert series in body, (
            f"GET /api/metrics does not report {series!r}; the brief names the "
            f"series that are exposed: {flatten(body)[:400]}")
    assert isinstance(body.get("runs_by_status"), dict), (
        f"GET /api/metrics reports runs_by_status as "
        f"{type(body.get('runs_by_status')).__name__}, not a mapping of status to "
        f"count: {flatten(body)[:300]}")
    for status in body["runs_by_status"]:
        assert status in RUN_STATUSES, (
            f"GET /api/metrics counts runs under status {status!r}, which is not "
            f"one of the pinned run statuses {RUN_STATUSES}")


def test_project_insights_reconcile_with_runs(owner_client, db):
    response = owner_client.get(f"/projects/{PLATFORM_OPS}/insights")
    assert response.status_code == 200, (
        f"GET /api/projects/{PLATFORM_OPS}/insights returned "
        f"{response.status_code}: {response.text[:400]}")
    body = response.json()
    for field in ("total_runs", "failed_runs", "average_duration_ms",
                  "retention_days", "run_output_max_bytes"):
        assert field in body, (
            f"GET /api/projects/{PLATFORM_OPS}/insights does not report {field!r}: "
            f"{flatten(body)[:400]}")

    triage = db.workflow_by_name(INCIDENT_TRIAGE)
    nightly = db.workflow_by_name(NIGHTLY_BACKUP)
    counted = db.count_runs(workflow_id=triage["id"]) + db.count_runs(
        workflow_id=nightly["id"])
    assert int(body["total_runs"]) >= counted, (
        f"insights report {body['total_runs']} total runs for {PLATFORM_OPS} while "
        f"the run rows for its workflows number {counted}; the rollup is "
        f"accumulated from the runs, so it cannot report fewer")
    assert int(body["run_output_max_bytes"]) > 0, (
        f"insights report run_output_max_bytes {body['run_output_max_bytes']!r}; "
        f"the ceiling is read from RUN_OUTPUT_MAX_BYTES and is a positive size")
    assert int(body["retention_days"]) > 0, (
        f"insights report retention_days {body['retention_days']!r}; retention is "
        f"configured per project")


def test_step_output_is_readable_before_the_run_finishes(operator_client, db):
    queued = fresh_waiting_run(operator_client, operator_client)
    run_id = queued.get("run_id")

    row = db.run_by_id(run_id)
    assert row is not None and row.get("status") == "waiting", (
        f"run {run_id} reads status {row and row.get('status')!r}; the probe needs "
        f"a run that has stopped part way so the earlier steps can be read")

    steps = db.steps_of_run(run_id)
    finished = [s for s in steps if s.get("status") == "succeeded"]
    assert finished, (
        f"run {run_id} is 'waiting' but records no finished step; output is "
        f"written as each step completes rather than flushed when the run ends")
    assert any(str(s.get("output_summary") or "").strip() for s in finished), (
        f"run {run_id} records finished steps with no output at all while the run "
        f"is still going: {[s.get('step_name') for s in finished]}")

    detail = operator_client.get(f"/runs/{run_id}")
    assert detail.status_code == 200, (
        f"GET /api/runs/{run_id} returned {detail.status_code}: "
        f"{detail.text[:400]}")
    assert detail.json().get("output_bytes") is not None, (
        f"GET /api/runs/{run_id} reports no output_bytes; a run reports the size "
        f"of the step output stored against it: {flatten(detail.json())[:300]}")


def test_annotated_run_is_exempt_and_output_stays_under_the_ceiling(
        operator_client, owner_client, db):
    queued = fresh_waiting_run(operator_client, operator_client)
    run_id = queued.get("run_id")

    note = unique_ref("keep-for-triage")
    response = operator_client.post(f"/runs/{run_id}/annotation", json={"note": note})
    assert response.status_code in (200, 201), (
        f"POST /api/runs/{run_id}/annotation returned {response.status_code}; a run "
        f"can be annotated: {response.text[:400]}")
    assert response.json().get("note") == note, (
        f"the annotation for run {run_id} reads {response.json().get('note')!r} "
        f"rather than the note that was sent")

    settle()
    stored = db.annotations_of_run(run_id)
    assert stored, (
        f"run {run_id} was annotated but no run_annotations row exists; the note "
        f"is what exempts the run from pruning")

    insights = owner_client.get(f"/projects/{PLATFORM_OPS}/insights").json()
    ceiling = int(insights["run_output_max_bytes"])
    row = db.run_by_id(run_id)
    size = int(row.get("output_bytes") or 0)
    assert 0 <= size <= ceiling, (
        f"run {run_id} reports output_bytes {size} against a ceiling of {ceiling}; "
        f"a run at or past the ceiling fails with run_output_ceiling_exceeded "
        f"rather than storing past it")


def test_binary_step_output_is_a_reference_not_the_bytes(operator_client, db):
    queued = fresh_waiting_run(operator_client, operator_client)
    run_id = queued.get("run_id")

    for row in db.steps_of_run(run_id):
        ref = row.get("binary_ref")
        if not ref:
            continue
        if isinstance(ref, str):
            ref = json.loads(ref)
        for field in ("object_id", "size_bytes", "media_type", "checksum"):
            assert field in ref, (
                f"run_steps row {row.get('id')} records a binary reference with no "
                f"{field!r}; a reference carries an object identifier, a size, a "
                f"media type and a checksum: {ref}")
        assert int(ref["size_bytes"]) >= 0, (
            f"binary reference on run_steps row {row.get('id')} reports size_bytes "
            f"{ref['size_bytes']!r}")

    step = step_row("Emit bytes", parameters={"emit_binary": True})
    workflow_id = save_probe_workflow(operator_client, PLATFORM_OPS,
                                      unique_ref("Binary probe"), [step])
    probe_run = start_run(operator_client, workflow_id).get("id")
    run_to_rest(db, probe_run)
    for row in db.steps_of_run(probe_run):
        summary = str(row.get("output_summary") or "")
        assert len(summary) < 100000, (
            f"run_steps row {row.get('id')} stores {len(summary)} characters of "
            f"output; bytes are referenced, never stored as the step's output")


def test_code_step_cannot_reach_the_host_environment(operator_client, db):
    step = step_row("Reach out", step_type="code",
                    parameters={"code": CODE_STEP_REACH_HOST}, on_error="stop")
    workflow_id = save_probe_workflow(operator_client, PLATFORM_OPS,
                                      unique_ref("Sandbox probe"), [step])
    run_id = start_run(operator_client, workflow_id).get("id")
    run_to_rest(db, run_id)

    row = failed_step(db, run_id, "Reach out")
    assert row is not None, (
        f"the code step in run {run_id} did not fail; a body reaching for the "
        f"host's environment is refused by the sandbox")
    assert row.get("error_code") == "sandbox_denied", (
        f"the code step failed with error_code {row.get('error_code')!r}; reaching "
        f"for the host is refused as 'sandbox_denied': {row.get('error_message')}")

    blob = flatten(db.steps_of_run(run_id))
    for secret in ("deku-local-dev", "flowmark-client-9f14c73e", CORPUS_PASSWORD):
        assert secret not in blob, (
            f"the refused code step still surfaced {secret!r} in the run's output; "
            f"the credential store is out of the sandbox's reach")


def test_code_step_over_its_limit_is_killed_without_taking_the_worker(
        operator_client, db):
    step = step_row("Spin", step_type="code",
                    parameters={"code": CODE_STEP_SPIN}, on_error="stop")
    workflow_id = save_probe_workflow(operator_client, PLATFORM_OPS,
                                      unique_ref("Timeout probe"), [step])
    run_id = start_run(operator_client, workflow_id).get("id")
    row = run_to_rest(db, run_id)
    assert row is not None and row.get("status") == "failed", (
        f"the spinning code step left run {run_id} at status "
        f"{row and row.get('status')!r}; a body past its ceiling is stopped from "
        f"outside rather than allowed to run on")

    step_state = failed_step(db, run_id, "Spin")
    assert step_state is not None, (
        f"run {run_id} records no failed step for the spinning body")
    assert step_state.get("error_code") == "sandbox_timeout", (
        f"the spinning code step failed with error_code "
        f"{step_state.get('error_code')!r}, not 'sandbox_timeout'")

    after_id = start_run(operator_client,
                         workflow_id_by_name(operator_client, PLATFORM_OPS,
                                             INCIDENT_TRIAGE)).get("id")
    after = run_to_rest(db, after_id)
    assert after is not None and after.get("status") in ("waiting", "running",
                                                         "succeeded"), (
        f"a run started after the sandbox kill reached status "
        f"{after and after.get('status')!r}; stopping one code execution must not "
        f"disturb anything else on the worker")


def test_code_step_input_is_cloned_not_shared(operator_client, db):
    source = step_row("Source", parameters={"emit": [{"value": "original"}]},
                      position_x=100)
    mutator = step_row("Mutator", step_type="code",
                       parameters={"code": CODE_STEP_MUTATE}, position_x=300)
    observer = step_row("Observer", parameters={"passthrough": True}, position_x=500)
    links = [
        {"from_step": "Source", "from_output_index": 0, "to_step": "Mutator",
         "to_input_index": 0, "connection_type": "main"},
        {"from_step": "Source", "from_output_index": 0, "to_step": "Observer",
         "to_input_index": 0, "connection_type": "main"},
    ]
    workflow_id = save_probe_workflow(operator_client, PLATFORM_OPS,
                                      unique_ref("Clone probe"),
                                      [source, mutator, observer], links)
    run_id = start_run(operator_client, workflow_id).get("id")
    run_to_rest(db, run_id)

    observed = [s for s in db.steps_of_run(run_id)
                if s.get("step_name") == "Observer"]
    assert observed, (
        f"run {run_id} records no output for the sibling branch, so the clone rule "
        f"could not be observed")
    assert "touched" not in str(observed[0].get("output_summary") or ""), (
        f"the sibling branch saw the code step's mutation: "
        f"{observed[0].get('output_summary')}. A code step receives its items "
        f"copied, so a mutation on one branch cannot reach another")


def test_outbound_request_to_an_internal_address_is_refused(operator_client, db):
    for url in INTERNAL_URLS:
        step = step_row("Fetch inward", parameters={"url": url}, on_error="stop")
        workflow_id = save_probe_workflow(operator_client, PLATFORM_OPS,
                                          unique_ref("Egress probe"), [step])
        run_id = start_run(operator_client, workflow_id).get("id")
        run_to_rest(db, run_id)

        row = failed_step(db, run_id, "Fetch inward")
        assert row is not None, (
            f"a step addressing {url!r} did not fail; an internal address is "
            f"refused, and the whole product exists to fetch addresses an "
            f"operator typed")
        assert row.get("error_code") == "egress_denied", (
            f"a step addressing {url!r} failed with error_code "
            f"{row.get('error_code')!r}, not 'egress_denied': "
            f"{row.get('error_message')}")


def test_expression_resolves_against_its_named_ancestor_step(operator_client, db):
    queued = fresh_waiting_run(operator_client, operator_client)
    run_id = queued.get("run_id")

    fetched = [s for s in db.steps_of_run(run_id)
               if s.get("step_name") == "Fetch incident"]
    assert fetched, (
        f"run {run_id} records no output for 'Fetch incident', so the value the "
        f"later step binds from it cannot be compared")

    for row in db.steps_of_run(run_id):
        summary = str(row.get("output_summary") or "")
        assert "{{" not in summary and "}}" not in summary, (
            f"run_steps row {row.get('id')} for step {row.get('step_name')!r} "
            f"stores an unresolved expression in its output: {summary[:200]}. A "
            f"bound value is resolved just before its step runs")

    detail = operator_client.get(f"/runs/{run_id}")
    assert detail.status_code == 200, (
        f"GET /api/runs/{run_id} returned {detail.status_code}: "
        f"{detail.text[:300]}")
    assert "{{" not in flatten(detail.json()), (
        f"run {run_id} reports an unresolved expression through its own detail "
        f"route: {flatten(detail.json())[:300]}")


def test_expression_error_names_the_step_and_the_field(operator_client, db):
    step = step_row("Bind from nowhere",
                    parameters={"message": "{{ steps['No Such Step'].id }}"},
                    on_error="stop")
    workflow_id = save_probe_workflow(operator_client, PLATFORM_OPS,
                                      unique_ref("Expression probe"), [step])
    run_id = start_run(operator_client, workflow_id).get("id")
    run_to_rest(db, run_id)

    row = failed_step(db, run_id, "Bind from nowhere")
    assert row is not None, (
        f"run {run_id} did not fail the step binding from a step that never ran")
    assert row.get("error_code") == "expression_unresolved_reference", (
        f"the step failed with error_code {row.get('error_code')!r}, not "
        f"'expression_unresolved_reference': {row.get('error_message')}")
    message = str(row.get("error_message") or "")
    assert "Bind from nowhere" in message, (
        f"the expression error does not name the step it failed on: {message}")
    assert "message" in message, (
        f"the expression error does not name the field it failed on: {message}")
