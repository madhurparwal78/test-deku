"""The one pytest module for the Vocalis Console.

Every observation here is black box: HTTP against the running app and reads of the
declared backend through the capability fixture. Nothing inspects the agent's source.
"""
from __future__ import annotations

import os

import conftest
from conftest import (
    ADMIN_EMAIL,
    AUDIO_SECOND,
    ARCHIVED_PROJECT_SLUG,
    BALANCE_MINOR,
    BATCH_LINE,
    DENIED_MEMBER_EMAIL,
    DENIED_OR_MISSING,
    DENIED_STATUSES,
    DENIED_VIEW_SECONDS,
    EMPTY_PROJECT_SLUG,
    EMPTY_PROJECT_SECONDS,
    FIRST_CLIP,
    FIRST_CLIP_ACCURACY,
    FIRST_CLIP_SECONDS,
    INVOICE_NUMBER,
    INVOICE_TOTAL_MINOR,
    METERED_PROJECT_CHARACTERS,
    METERED_PROJECT_SECONDS,
    METERED_PROJECT_SLUG,
    NEW_CREDENTIAL_LABEL,
    OK_STATUSES,
    ORGANISATION_SECONDS,
    PERIOD_END,
    PERIOD_START,
    PRIMARY_ORG_SLUG,
    REVOKED_PREFIX,
    SECOND_ORG_SLUG,
    SECRET_STEM,
)


def test_health_endpoint_returns_ready(anonymous, api):
    """The app is ready, outlives the session, and carries the App Contract artifacts."""
    response = anonymous.get(f"{api}/health")
    assert response.status_code == 200, (
        f"GET {api}/health returned {response.status_code}, expected 200 once the "
        f"app is ready; body={response.text[:200]}"
    )
    readme = os.path.join("/app", "USER_README.md")
    assert os.path.isfile(readme), (
        "no credentials file at /app/USER_README.md; the login credentials are "
        "written there so they can be read after the session"
    )
    with open(readme, encoding="utf-8", errors="replace") as handle:
        credentials = handle.read()
    assert conftest.CORPUS_PASSWORD in credentials, (
        "the credentials file carries no seeded password; the exact literal must "
        "be written there alongside each account"
    )
    assert conftest.OWNER_EMAIL in credentials, (
        f"the credentials file names no {conftest.OWNER_EMAIL} account"
    )
    for reserved in ("/app/.browser_screenshots", "/app/.downloads"):
        assert os.path.isdir(reserved), (
            f"the reserved directory {reserved} is absent from the app root"
        )
    dev = anonymous.get(f"{conftest.appclient.app_url()}/@vite/client")
    assert dev.status_code >= 400, (
        f"a development-server asset answered {dev.status_code}; a production "
        f"build is served behind a static or preview server"
    )


def test_unauthenticated_request_is_denied(anonymous, api):
    """A caller carrying no bearer token reaches no console data."""
    response = anonymous.get(f"{api}/organisations/{PRIMARY_ORG_SLUG}/projects")
    assert response.status_code in DENIED_STATUSES, (
        f"an anonymous read of the project list returned {response.status_code}, "
        f"expected one of {DENIED_STATUSES}; an unauthenticated caller must reach "
        f"no console data. body={response.text[:300]}"
    )


def test_playground_recognition_reports_accuracy_and_latency(member, api):
    """A playground recognition reports the clip transcript, its accuracy and a measured latency."""
    response = member.post(
        f"{api}/projects/{METERED_PROJECT_SLUG}/playground/recognize",
        json={"clip": FIRST_CLIP},
    )
    assert response.status_code in OK_STATUSES, (
        f"recognising {FIRST_CLIP!r} on {METERED_PROJECT_SLUG!r} returned "
        f"{response.status_code}; body={response.text[:400]}"
    )
    body = response.json()
    assert str(body.get("accuracy")).rstrip("%") == FIRST_CLIP_ACCURACY, (
        f"recognition of {FIRST_CLIP!r} reported accuracy {body.get('accuracy')!r}, "
        f"expected {FIRST_CLIP_ACCURACY}"
    )
    latency = body.get("latency_ms")
    assert isinstance(latency, int) and latency > 0, (
        f"recognition reported latency_ms {latency!r}, expected a positive integer "
        f"measured by the app"
    )
    assert str(body.get("transcript", "")).strip(), (
        "recognition returned an empty transcript for a seeded clip"
    )
    assert int(body.get("quantity", 0)) == FIRST_CLIP_SECONDS, (
        f"recognition billed quantity {body.get('quantity')!r}, expected "
        f"{FIRST_CLIP_SECONDS} audio seconds for {FIRST_CLIP!r}"
    )


def test_playground_recognition_meters_exactly_one_row(member, api, backend):
    """A playground recognition writes exactly one metering row attributed to the project."""
    before = backend.count("usage_events")
    response = member.post(
        f"{api}/projects/{METERED_PROJECT_SLUG}/playground/recognize",
        json={"clip": FIRST_CLIP},
    )
    assert response.status_code in OK_STATUSES, (
        f"recognition returned {response.status_code}; body={response.text[:300]}"
    )
    after = conftest.poll_until(
        lambda: backend.count("usage_events") if
        backend.count("usage_events") > before else None,
        f"no metering row appeared after a playground recognition on "
        f"{METERED_PROJECT_SLUG!r}",
    )
    assert after == before + 1, (
        f"a playground recognition moved the metering row count from {before} to "
        f"{after}; exactly one row is written per request"
    )


def test_playground_request_appears_in_request_list(member, api):
    """A playground request is recorded and inspectable afterwards."""
    member.post(
        f"{api}/projects/{METERED_PROJECT_SLUG}/playground/recognize",
        json={"clip": FIRST_CLIP},
    )
    response = member.get(f"{api}/projects/{METERED_PROJECT_SLUG}/requests")
    assert response.status_code in OK_STATUSES, (
        f"reading the request list returned {response.status_code}; "
        f"body={response.text[:300]}"
    )
    rows = response.json()
    assert isinstance(rows, list) and rows, (
        "the request list is empty after a playground recognition; every request "
        "is recorded and inspectable"
    )
    assert any(str(r.get("clip")) == FIRST_CLIP for r in rows), (
        f"no entry for {FIRST_CLIP!r} in the request list; entries carried "
        f"{[r.get('clip') for r in rows][:5]}"
    )


def test_auditor_cannot_use_playground(auditor, api, backend):
    """An auditor writes nothing, so a playground request is denied and meters nothing."""
    before = backend.count("usage_events")
    response = auditor.post(
        f"{api}/projects/{METERED_PROJECT_SLUG}/playground/recognize",
        json={"clip": FIRST_CLIP},
    )
    assert response.status_code in DENIED_OR_MISSING, (
        f"an auditor playground request returned {response.status_code}, expected "
        f"one of {DENIED_OR_MISSING}; an auditor reads and writes nothing"
    )
    conftest.settle()
    assert backend.count("usage_events") == before, (
        "a denied auditor playground request wrote a metering row; a refused "
        "request meters nothing"
    )
    audit = auditor.get(f"{api}/organisations/{PRIMARY_ORG_SLUG}/audit")
    assert audit.status_code in OK_STATUSES, (
        f"an auditor reading the audit record returned {audit.status_code}; the "
        f"auditor role reads that record"
    )
    rows = audit.json()
    assert isinstance(rows, list) and rows, (
        "the audit record is empty though decisions have been made"
    )
    assert any(str(r.get("outcome")) == "denied" for r in rows), (
        f"no denied decision appears in the audit record; every refusal appends "
        f"one row. outcomes seen: "
        f"{sorted({str(r.get('outcome')) for r in rows})}"
    )


def test_first_credential_issue_returns_secret_once(administrator, api):
    """Issuing a credential returns a secret of the pinned shape exactly once."""
    body = conftest.issue_credential(
        administrator, api, EMPTY_PROJECT_SLUG, NEW_CREDENTIAL_LABEL,
        ["recognize:batch", "usage:read"],
    )
    secret = body.get("secret")
    assert isinstance(secret, str) and len(secret) == 40, (
        f"the issue response carried secret {secret!r}; a credential secret is "
        f"forty characters"
    )
    assert secret.startswith(SECRET_STEM), (
        f"the issued secret {secret[:8]!r} does not begin {SECRET_STEM!r}"
    )
    assert body.get("prefix") == secret[:8], (
        f"the issue response carried prefix {body.get('prefix')!r}, which is not "
        f"the first eight characters of the secret"
    )
    audit = administrator.get(f"{api}/organisations/{PRIMARY_ORG_SLUG}/audit")
    assert audit.status_code in OK_STATUSES or audit.status_code in DENIED_STATUSES, (
        f"reading the audit record returned {audit.status_code}, which is neither "
        f"a read nor a refusal"
    )


def test_credential_secret_never_returned_after_creation(administrator, api):
    """No read after creation returns a credential secret."""
    label = f"{NEW_CREDENTIAL_LABEL} {conftest.run_tag()}"
    issued = conftest.issue_credential(
        administrator, api, EMPTY_PROJECT_SLUG, label, ["recognize:batch"],
    )
    secret = issued["secret"]
    response = administrator.get(f"{api}/projects/{EMPTY_PROJECT_SLUG}/keys")
    assert response.status_code in OK_STATUSES, (
        f"reading the credential index returned {response.status_code}"
    )
    assert secret not in response.text, (
        "the credential index response carried the full secret; a secret is shown "
        "exactly once at creation and is never recoverable"
    )
    rows = response.json()
    assert any(r.get("label") == label for r in rows), (
        f"the credential {label!r} is absent from the index after issue"
    )
    for row in rows:
        assert "secret" not in row, (
            f"the credential index row for {row.get('label')!r} carries a secret field"
        )


def test_never_used_credential_renders_never(administrator, api):
    """A credential that has never been used reports never in its last-used field."""
    response = administrator.get(f"{api}/projects/{METERED_PROJECT_SLUG}/keys")
    assert response.status_code in OK_STATUSES, (
        f"reading the credential index returned {response.status_code}"
    )
    rows = response.json()
    unused = [r for r in rows if r.get("last_used_at") in (None, "", "never")]
    assert unused, (
        f"no credential on {METERED_PROJECT_SLUG!r} reports an absent last use, "
        f"though one is seeded never used"
    )


def test_issued_credential_authenticates_usage_intake(administrator, api, backend):
    """A credential secret authenticates the usage intake and the project total rises."""
    label = f"{NEW_CREDENTIAL_LABEL} {conftest.run_tag()}"
    issued = conftest.issue_credential(
        administrator, api, EMPTY_PROJECT_SLUG, label, ["recognize:batch"],
    )
    before = conftest.total_for_unit(
        conftest.read_usage(administrator, api, f"projects/{EMPTY_PROJECT_SLUG}",
                            PERIOD_START, PERIOD_END),
        AUDIO_SECOND,
    )
    with conftest.credential_client(issued["secret"]) as caller:
        response = conftest.submit_usage(
            caller, api, conftest.idempotency_key(), BATCH_LINE, 240,
            f"{PERIOD_START}T09:00:00Z",
        )
    assert response.status_code in OK_STATUSES, (
        f"a usage submission presenting a freshly issued credential returned "
        f"{response.status_code}; body={response.text[:300]}"
    )
    after = conftest.total_for_unit(
        conftest.read_usage(administrator, api, f"projects/{EMPTY_PROJECT_SLUG}",
                            PERIOD_START, PERIOD_END),
        AUDIO_SECOND,
    )
    assert after == before + 240, (
        f"the project total moved from {before} to {after}; a submission of 240 "
        f"audio seconds raises it by exactly that quantity"
    )
    assert backend.count("usage_events", idempotency_key=None) >= 0, (
        "the metering table is unreadable through the declared backend"
    )


def test_intake_refuses_credential_without_scope(administrator, api, backend):
    """A credential lacking the scope for a submitted line is refused and writes nothing."""
    label = f"Scopeless {conftest.run_tag()}"
    issued = conftest.issue_credential(
        administrator, api, EMPTY_PROJECT_SLUG, label, ["usage:read"],
    )
    before = backend.count("usage_events")
    with conftest.credential_client(issued["secret"]) as caller:
        response = conftest.submit_usage(
            caller, api, conftest.idempotency_key(), BATCH_LINE, 120,
            f"{PERIOD_START}T10:00:00Z",
        )
    assert response.status_code in DENIED_OR_MISSING, (
        f"a submission on line {BATCH_LINE!r} by a credential holding only "
        f"usage:read returned {response.status_code}, expected one of "
        f"{DENIED_OR_MISSING}"
    )
    conftest.settle()
    assert backend.count("usage_events") == before, (
        "a refused submission wrote a metering row; a refusal writes nothing"
    )


def test_revoked_credential_refused_at_intake(administrator, api, backend):
    """A revoked credential is refused from the instant of revocation."""
    label = f"Doomed {conftest.run_tag()}"
    issued = conftest.issue_credential(
        administrator, api, EMPTY_PROJECT_SLUG, label, ["recognize:batch"],
    )
    prefix = issued["prefix"]
    revoked = administrator.post(
        f"{api}/projects/{EMPTY_PROJECT_SLUG}/keys/{prefix}/revoke"
    )
    assert revoked.status_code in OK_STATUSES, (
        f"revoking credential {prefix!r} returned {revoked.status_code}; "
        f"body={revoked.text[:300]}"
    )
    before = backend.count("usage_events")
    with conftest.credential_client(issued["secret"]) as caller:
        response = conftest.submit_usage(
            caller, api, conftest.idempotency_key(), BATCH_LINE, 60,
            f"{PERIOD_START}T11:00:00Z",
        )
    assert response.status_code in DENIED_OR_MISSING, (
        f"a submission presenting revoked credential {prefix!r} returned "
        f"{response.status_code}, expected one of {DENIED_OR_MISSING}"
    )
    conftest.settle()
    assert backend.count("usage_events") == before, (
        "a submission by a revoked credential wrote a metering row"
    )


def test_repeat_idempotency_key_writes_no_second_row(administrator, api, backend):
    """A redelivered metering event writes no second row and moves no total."""
    label = f"Retry {conftest.run_tag()}"
    issued = conftest.issue_credential(
        administrator, api, EMPTY_PROJECT_SLUG, label, ["recognize:batch"],
    )
    key = conftest.idempotency_key()
    with conftest.credential_client(issued["secret"]) as caller:
        first = conftest.submit_usage(
            caller, api, key, BATCH_LINE, 300, f"{PERIOD_START}T12:00:00Z",
        )
        assert first.status_code in OK_STATUSES, (
            f"the first submission returned {first.status_code}; "
            f"body={first.text[:300]}"
        )
        settled = backend.count("usage_events")
        second = conftest.submit_usage(
            caller, api, key, BATCH_LINE, 300, f"{PERIOD_START}T12:00:00Z",
        )
    assert second.status_code in OK_STATUSES, (
        f"a redelivery carrying an idempotency key already seen returned "
        f"{second.status_code}; a retry is accepted rather than treated as an error"
    )
    conftest.settle()
    assert backend.count("usage_events") == settled, (
        f"a redelivery carrying key {key!r} wrote a second metering row; an "
        f"idempotency key appears on at most one row"
    )


def test_project_usage_total_equals_sum_of_rows(owner, api):
    """A project usage total equals the sum of the rows beneath it."""
    payload = conftest.read_usage(
        owner, api, f"projects/{METERED_PROJECT_SLUG}", PERIOD_START, PERIOD_END,
    )
    total = conftest.total_for_unit(payload, AUDIO_SECOND)
    assert total == METERED_PROJECT_SECONDS, (
        f"{METERED_PROJECT_SLUG!r} reported {total} audio seconds for "
        f"{PERIOD_START}..{PERIOD_END}, expected {METERED_PROJECT_SECONDS}"
    )
    assert conftest.rows_sum(payload, AUDIO_SECOND) == total, (
        f"the rows beneath the total sum to "
        f"{conftest.rows_sum(payload, AUDIO_SECOND)} while the total reads {total}; "
        f"a total equals the sum of its rows"
    )
    organisation = conftest.read_usage(
        owner, api, f"organisations/{PRIMARY_ORG_SLUG}", PERIOD_START, PERIOD_END,
    )
    org_total = conftest.total_for_unit(organisation, AUDIO_SECOND)
    assert org_total == ORGANISATION_SECONDS, (
        f"the organisation reported {org_total} audio seconds, expected "
        f"{ORGANISATION_SECONDS}"
    )


def test_chart_and_table_report_the_same_total(owner, api):
    """The chart series and the table rows report one figure for one range."""
    payload = conftest.read_usage(
        owner, api, f"projects/{METERED_PROJECT_SLUG}", PERIOD_START, PERIOD_END,
    )
    table = conftest.rows_sum(payload, AUDIO_SECOND)
    chart = conftest.series_sum(payload, AUDIO_SECOND)
    assert chart == table, (
        f"the chart series sums to {chart} while the table rows sum to {table}; "
        f"both surfaces read one figure"
    )
    characters = conftest.total_for_unit(payload, "character")
    assert characters == METERED_PROJECT_CHARACTERS, (
        f"{METERED_PROJECT_SLUG!r} reported {characters} characters, expected "
        f"{METERED_PROJECT_CHARACTERS}"
    )


def test_daily_rollup_recomputes_from_rows(owner, api, backend):
    """A daily rollup equals the metering rows it summarises."""
    rollups = backend.rows("usage_rollup_daily", limit=500)
    assert rollups, (
        "the daily rollup table is empty though seeded usage exists for "
        f"{PERIOD_START}..{PERIOD_END}"
    )
    events = backend.rows("usage_events", limit=2000)
    assert events, "the metering table is empty though seeded usage exists"
    rolled = sum(int(r.get("quantity", 0)) for r in rollups)
    raw = sum(int(e.get("quantity", 0)) for e in events)
    assert rolled == raw, (
        f"the daily rollups sum to {rolled} while the metering rows sum to {raw}; "
        f"a rollup is recomputable from the rows beneath it"
    )


def test_denied_project_usage_excluded_from_org_total(denied_member, api):
    """An organisation figure excludes a project the reader may not read."""
    payload = conftest.read_usage(
        denied_member, api, f"organisations/{PRIMARY_ORG_SLUG}",
        PERIOD_START, PERIOD_END,
    )
    total = conftest.total_for_unit(payload, AUDIO_SECOND)
    assert total == DENIED_VIEW_SECONDS, (
        f"{DENIED_MEMBER_EMAIL} was shown {total} audio seconds for the "
        f"organisation, expected {DENIED_VIEW_SECONDS}; the denied project's "
        f"{EMPTY_PROJECT_SECONDS} audio seconds must be excluded"
    )


def test_project_deny_override_hides_project(denied_member, api):
    """A per-project deny defeats the organisation role on every read path."""
    direct = denied_member.get(f"{api}/projects/{EMPTY_PROJECT_SLUG}")
    assert direct.status_code == 404, (
        f"reading the denied project by address returned {direct.status_code}, "
        f"expected 404; a project the principal may not read is not found rather "
        f"than forbidden"
    )
    listed = denied_member.get(f"{api}/organisations/{PRIMARY_ORG_SLUG}/projects")
    assert listed.status_code in OK_STATUSES, (
        f"the project index returned {listed.status_code} for a member"
    )
    slugs = [p.get("slug") for p in listed.json()]
    assert EMPTY_PROJECT_SLUG not in slugs, (
        f"the denied project {EMPTY_PROJECT_SLUG!r} appears in the project index "
        f"{slugs} for {DENIED_MEMBER_EMAIL}"
    )
    assert METERED_PROJECT_SLUG in slugs, (
        f"the readable project {METERED_PROJECT_SLUG!r} is absent from the index "
        f"{slugs}; only the denied project is withheld"
    )


def test_member_cannot_create_project(member, api, backend):
    """A member is refused project creation at the service and nothing is written."""
    before = backend.count("projects")
    response = member.post(
        f"{api}/organisations/{PRIMARY_ORG_SLUG}/projects",
        json={"name": f"Member Attempt {conftest.run_tag()}",
              "region": "eu-west", "retention_days": 90},
    )
    assert response.status_code in DENIED_OR_MISSING, (
        f"a member creating a project returned {response.status_code}, expected "
        f"one of {DENIED_OR_MISSING}"
    )
    conftest.settle()
    assert backend.count("projects") == before, (
        "a denied project creation wrote a project row; the protected state is "
        "left unchanged"
    )


def test_administrator_cannot_read_invoice(administrator, api):
    """An administrator is refused reading an invoice."""
    response = administrator.get(f"{api}/invoices/{INVOICE_NUMBER}")
    assert response.status_code in DENIED_OR_MISSING, (
        f"an administrator reading invoice {INVOICE_NUMBER!r} returned "
        f"{response.status_code}, expected one of {DENIED_OR_MISSING}; only an "
        f"owner or an auditor reads an invoice"
    )


def test_invoice_total_equals_sum_of_lines(owner, api):
    """An invoice total equals the sum of its lines."""
    response = owner.get(f"{api}/invoices/{INVOICE_NUMBER}")
    assert response.status_code in OK_STATUSES, (
        f"an owner reading invoice {INVOICE_NUMBER!r} returned "
        f"{response.status_code}; body={response.text[:300]}"
    )
    body = response.json()
    assert int(body.get("total_minor", -1)) == INVOICE_TOTAL_MINOR, (
        f"invoice {INVOICE_NUMBER!r} reported total_minor "
        f"{body.get('total_minor')!r}, expected {INVOICE_TOTAL_MINOR}"
    )
    lines = body.get("lines")
    assert isinstance(lines, list) and lines, (
        f"invoice {INVOICE_NUMBER!r} carries no lines"
    )
    assert sum(int(x.get("amount_minor", 0)) for x in lines) == INVOICE_TOTAL_MINOR, (
        f"the invoice lines sum to "
        f"{sum(int(x.get('amount_minor', 0)) for x in lines)} while the total reads "
        f"{INVOICE_TOTAL_MINOR}"
    )


def test_balance_equals_sum_of_ledger_entries(owner, api):
    """The organisation balance equals the sum of its ledger entries."""
    response = owner.get(f"{api}/organisations/{PRIMARY_ORG_SLUG}/ledger")
    assert response.status_code in OK_STATUSES, (
        f"reading the ledger returned {response.status_code}; "
        f"body={response.text[:300]}"
    )
    body = response.json()
    entries = body if isinstance(body, list) else body.get("entries")
    assert isinstance(entries, list) and entries, (
        "the ledger carries no entries though a grant and a drawdown are seeded"
    )
    total = sum(int(e.get("amount_minor", 0)) for e in entries)
    assert total == BALANCE_MINOR, (
        f"the ledger entries sum to {total}, expected the seeded balance "
        f"{BALANCE_MINOR}"
    )
    if isinstance(body, dict) and "balance_minor" in body:
        assert int(body["balance_minor"]) == total, (
            f"the reported balance {body['balance_minor']!r} disagrees with the "
            f"sum of its entries {total}"
        )


def test_late_event_restates_period_without_touching_invoice(administrator, owner, api):
    """A late event restates a closed period and leaves the finalised invoice unchanged."""
    label = f"Late {conftest.run_tag()}"
    issued = conftest.issue_credential(
        administrator, api, METERED_PROJECT_SLUG, label, ["recognize:batch"],
    )
    before_invoice = owner.get(f"{api}/invoices/{INVOICE_NUMBER}").json()
    before_period = conftest.total_for_unit(
        conftest.read_usage(owner, api, f"projects/{METERED_PROJECT_SLUG}",
                            PERIOD_START, PERIOD_END),
        AUDIO_SECOND,
    )
    with conftest.credential_client(issued["secret"]) as caller:
        response = conftest.submit_usage(
            caller, api, conftest.idempotency_key(), BATCH_LINE, 60,
            f"{PERIOD_END}T23:00:00Z",
        )
    assert response.status_code in OK_STATUSES, (
        f"a late submission inside the closed period returned {response.status_code}; "
        f"a late arrival is accepted. body={response.text[:300]}"
    )
    after_period = conftest.total_for_unit(
        conftest.read_usage(owner, api, f"projects/{METERED_PROJECT_SLUG}",
                            PERIOD_START, PERIOD_END),
        AUDIO_SECOND,
    )
    assert after_period == before_period + 60, (
        f"the closed period total moved from {before_period} to {after_period}; a "
        f"late event restates the period it occurred in"
    )
    after_invoice = owner.get(f"{api}/invoices/{INVOICE_NUMBER}").json()
    assert int(after_invoice.get("total_minor", -1)) == INVOICE_TOTAL_MINOR, (
        f"invoice {INVOICE_NUMBER!r} moved from "
        f"{before_invoice.get('total_minor')!r} to "
        f"{after_invoice.get('total_minor')!r}; a finalised invoice is never updated"
    )


def test_archived_project_refuses_new_usage(administrator, api, backend):
    """An archived project accepts no new metering row."""
    before = backend.count("usage_events")
    response = administrator.post(
        f"{api}/projects/{ARCHIVED_PROJECT_SLUG}/playground/recognize",
        json={"clip": FIRST_CLIP},
    )
    assert response.status_code in DENIED_OR_MISSING or response.status_code >= 400, (
        f"a playground request against the archived project returned "
        f"{response.status_code}; an archived project refuses new usage"
    )
    conftest.settle()
    assert backend.count("usage_events") == before, (
        "a request against an archived project wrote a metering row"
    )


def test_archived_project_keeps_billable_history(owner, api):
    """An archived project keeps every metering row it already held."""
    payload = conftest.read_usage(
        owner, api, f"projects/{ARCHIVED_PROJECT_SLUG}", PERIOD_START, PERIOD_END,
    )
    total = conftest.total_for_unit(payload, AUDIO_SECOND)
    assert total == 300, (
        f"the archived project reported {total} audio seconds for "
        f"{PERIOD_START}..{PERIOD_END}, expected its seeded 300; archiving keeps "
        f"the billable history"
    )
    assert conftest.rows_sum(payload, AUDIO_SECOND) == total, (
        "the archived project's rows disagree with its total"
    )


def test_self_approval_issues_no_credential(owner, api, backend):
    """An approval decided by its own requester issues no credential."""
    before = backend.count("api_keys")
    requested = owner.post(
        f"{api}/projects/{METERED_PROJECT_SLUG}/keys",
        json={"label": f"Escalate {conftest.run_tag()}",
              "scopes": ["manage:keys"],
              "reason": "rotating the ingest credentials for the quarter",
              "expires_at": None},
    )
    assert requested.status_code in OK_STATUSES, (
        f"requesting an elevated credential returned {requested.status_code}; "
        f"body={requested.text[:300]}"
    )
    body = requested.json()
    assert "secret" not in body, (
        "a request for an elevated scope returned a secret; an elevated credential "
        "issues only after a second owner approves"
    )
    approval_id = body.get("id") or body.get("approval_id")
    assert approval_id, (
        f"the elevated request returned no approval identifier; body={body!r}"
    )
    self_approved = owner.post(f"{api}/approvals/{approval_id}/approve")
    assert self_approved.status_code in DENIED_OR_MISSING, (
        f"the requester approving their own request returned "
        f"{self_approved.status_code}, expected one of {DENIED_OR_MISSING}; "
        f"self-approval is refused at the service"
    )
    conftest.settle()
    assert backend.count("api_keys") == before, (
        "a self-approved request issued a credential"
    )


def test_elevated_scope_requires_second_owner(owner, second_owner, api):
    """A second owner approving an elevated request issues a credential carrying an expiry."""
    requested = owner.post(
        f"{api}/projects/{METERED_PROJECT_SLUG}/keys",
        json={"label": f"Elevated {conftest.run_tag()}",
              "scopes": ["manage:keys"],
              "reason": "issuing a scoped minting credential for the ingest fleet",
              "expires_at": None},
    )
    assert requested.status_code in OK_STATUSES, (
        f"requesting an elevated credential returned {requested.status_code}"
    )
    approval_id = requested.json().get("id") or requested.json().get("approval_id")
    assert approval_id, "the elevated request returned no approval identifier"
    approved = second_owner.post(f"{api}/approvals/{approval_id}/approve")
    assert approved.status_code in OK_STATUSES, (
        f"a second owner approving the request returned {approved.status_code}; "
        f"body={approved.text[:300]}"
    )
    body = approved.json()
    secret = body.get("secret")
    assert isinstance(secret, str) and secret.startswith(SECRET_STEM), (
        f"approval returned secret {secret!r}; an approved elevated request issues "
        f"the credential"
    )
    assert body.get("expires_at"), (
        "the approved elevated credential carries no expiry; an elevated scope "
        "carries a mandatory expiry"
    )


def test_organisation_switch_drops_previous_project_scope(owner, api):
    """A project of one organisation is unreachable under another organisation."""
    organisations = owner.get(f"{api}/organisations")
    assert organisations.status_code in OK_STATUSES, (
        f"reading the organisation list returned {organisations.status_code}"
    )
    slugs = [o.get("slug") for o in organisations.json()]
    assert PRIMARY_ORG_SLUG in slugs and SECOND_ORG_SLUG in slugs, (
        f"the owner belongs to both organisations but the switcher listed {slugs}"
    )
    listed = owner.get(f"{api}/organisations/{SECOND_ORG_SLUG}/projects")
    assert listed.status_code in OK_STATUSES, (
        f"reading the second organisation's projects returned {listed.status_code}"
    )
    second_slugs = [p.get("slug") for p in listed.json()]
    assert METERED_PROJECT_SLUG not in second_slugs, (
        f"the project {METERED_PROJECT_SLUG!r} of {PRIMARY_ORG_SLUG!r} appears "
        f"under {SECOND_ORG_SLUG!r} as {second_slugs}; a project identifier never "
        f"crosses an organisation boundary"
    )


def test_invalid_project_name_is_refused(administrator, api, backend):
    """A project creation carrying no usable name is refused and writes nothing."""
    before = backend.count("projects")
    response = administrator.post(
        f"{api}/organisations/{PRIMARY_ORG_SLUG}/projects",
        json={"name": "   ", "region": "eu-west", "retention_days": 90},
    )
    assert 400 <= response.status_code < 500, (
        f"creating a project with a blank name returned {response.status_code}, "
        f"expected a client-error class response"
    )
    conftest.settle()
    assert backend.count("projects") == before, (
        "a refused project creation wrote a project row"
    )


def test_security_headers_present_on_every_response(anonymous, api):
    """Every response carries a strict transport policy and a nosniff content-type policy."""
    targets = [f"{api}/health",
               f"{conftest.appclient.app_url()}/sign-in",
               f"{conftest.appclient.app_url()}/terms"]
    for target in targets:
        response = anonymous.get(target)
        headers = {k.lower(): v for k, v in response.headers.items()}
        assert "strict-transport-security" in headers, (
            f"the response to {target!r} carries no strict transport policy "
            f"header; headers were {sorted(headers)}"
        )
        assert headers.get("x-content-type-options", "").lower() == "nosniff", (
            f"the response to {target!r} carries "
            f"x-content-type-options {headers.get('x-content-type-options')!r}, "
            f"expected nosniff"
        )
        assert "referrer-policy" in headers, (
            f"the response to {target!r} carries no referrer policy header; "
            f"headers were {sorted(headers)}"
        )


def test_unknown_address_answers_not_found(anonymous):
    """An unmatched address answers not found, and no out-of-scope surface is served."""
    base = conftest.appclient.app_url()
    with conftest.appclient.client(None) as page:
        response = page.get(f"{base}/no-such-console-route-{conftest.run_tag()}")
        absent = {}
        for address in ("/pricing", "/stream", "/uploads", "/mail", "/payments"):
            absent[address] = page.get(f"{base}{address}").status_code
    assert response.status_code == 404, (
        f"an unmatched address returned {response.status_code}, expected 404"
    )
    assert response.text.strip(), (
        "the not-found response carried an empty body; the product renders its own "
        "not-found page"
    )
    served = {a: code for a, code in absent.items() if code < 400}
    assert not served, (
        f"addresses outside the console scope answered: {served}; the marketing "
        f"site, the audio socket, object upload, mail and payments are out of scope"
    )


def test_terms_page_reachable_from_footer(anonymous):
    """The terms page is served and the sign-in page links to it."""
    with conftest.appclient.client(None) as page:
        terms = page.get(f"{conftest.appclient.app_url()}/terms")
        sign_in = page.get(f"{conftest.appclient.app_url()}/sign-in")
    assert terms.status_code == 200, (
        f"the terms route returned {terms.status_code}, expected 200"
    )
    assert terms.text.strip(), "the terms page carried an empty body"
    assert "/terms" in sign_in.text, (
        "the sign-in page carries no link to the terms page, though the terms page "
        "is reachable from the footer of every page"
    )


def test_internal_links_all_resolve(anonymous):
    """Every internal link on the public pages resolves."""
    import re

    base = conftest.appclient.app_url()
    seen = set()
    with conftest.appclient.client(None) as page:
        for route in conftest.public_routes():
            body = page.get(f"{base}{route}").text
            for href in re.findall(r'href="(/[^"#?]*)"', body):
                seen.add(href)
        assert seen, (
            f"no internal link was found on the public routes "
            f"{conftest.public_routes()}"
        )
        broken = []
        for href in sorted(seen):
            status = page.get(f"{base}{href}").status_code
            if status >= 400:
                broken.append((href, status))
    assert not broken, (
        f"internal links that do not resolve: {broken}; every internal link on "
        f"every reachable page resolves"
    )
