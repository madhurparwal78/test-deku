"""Fixtures, domain constants and the pinned literals for Personal Telemetry Workbench.

No test_* function lives here (G10). Every value test_output.py asserts about the
SEEDED world is pinned in this file and appears verbatim in instruction.md (G6): a
grader that asserts a value the brief never pinned grades a working app as broken.
The self-seeded probe values below are generated per run and are only ever compared
against themselves, so they are deliberately not brief literals.

The shared grader (appclient, capabilities, _shapes) is supplied by the
deku-verifier-base image on PYTHONPATH=/tests. Nothing here re-implements it and
nothing here imports a provider SDK.
"""

from __future__ import annotations

import os
import threading
import time
from concurrent import futures

import httpx
import pytest

import appclient
import capabilities

OWNER_EMAIL = "owner@example.com"
OTHER_EMAIL = "other@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"
OWNER_NAME = "Marisol Vega"
OTHER_NAME = "Anders Roeg"

WORKSPACE_OWNER = "Northlight Labs"
WORKSPACE_OTHER = "Coldwater Games"
WORKSPACE_OWNER_SLUG = "northlight-labs"
WORKSPACE_OTHER_SLUG = "coldwater-games"

PROJECT_ARCHIVE = "ledgerline"
PROJECT_EMPTY = "quarry"
PROJECT_OUTSIDE = "stonefall"
OWNER_PROJECTS = (PROJECT_ARCHIVE, PROJECT_EMPTY)

TYPE_APP_OPENED = "app_opened"
TYPE_SEARCH_RUN = "search_run"
TYPE_EXPORT_PANEL = "export_panel_seen"
TYPE_REPORT_EXPORTED = "report_exported"
TYPE_INVITE_SENT = "invite_sent"
TYPE_PLAN_UPGRADED = "plan_upgraded"
SEEDED_TYPES = (TYPE_APP_OPENED, TYPE_SEARCH_RUN, TYPE_EXPORT_PANEL,
                TYPE_REPORT_EXPORTED, TYPE_INVITE_SENT, TYPE_PLAN_UPGRADED)
SEEDED_TYPE_EVENTS = {
    TYPE_APP_OPENED: 960,
    TYPE_SEARCH_RUN: 612,
    TYPE_EXPORT_PANEL: 384,
    TYPE_REPORT_EXPORTED: 312,
    TYPE_INVITE_SENT: 108,
    TYPE_PLAN_UPGRADED: 24,
}
SEEDED_TYPE_PERSONS = {
    TYPE_APP_OPENED: 8,
    TYPE_SEARCH_RUN: 7,
    TYPE_EXPORT_PANEL: 6,
    TYPE_REPORT_EXPORTED: 5,
    TYPE_INVITE_SENT: 4,
    TYPE_PLAN_UPGRADED: 3,
}

ARCHIVE_EVENTS = 2400
ARCHIVE_PERSONS = 8
ARCHIVE_SPAN_DAYS = 180

SEEDED_PERSON_IDS = (
    "anna-reyes", "bo-lindqvist", "cai-oyelaran", "dara-whitlock",
    "emil-sandoval", "fern-adeyemi", "gus-marchetti", "hana-vestergaard",
)
PERSON_WITH_RECORDING = "anna-reyes"

FUNNEL_STEPS = (TYPE_APP_OPENED, TYPE_SEARCH_RUN, TYPE_REPORT_EXPORTED)
FUNNEL_COUNTS = (8, 7, 5)
FUNNEL_SECOND_CONVERSION = "87.50%"
FUNNEL_THIRD_CONVERSION = "71.43%"
FUNNEL_WHOLE_CONVERSION = "62.50%"

BAND_EPOCH = "epoch"
BAND_SEASON = "season"
BAND_WEEK = "week"
BAND_SESSION = "session"
BAND_MOMENT = "moment"
BANDS = (BAND_EPOCH, BAND_SEASON, BAND_WEEK, BAND_SESSION, BAND_MOMENT)

DIM_PERSON = "person"
DIM_SESSION = "session"
DIM_RELEASE = "release"
DIMENSIONS = (DIM_PERSON, DIM_SESSION, DIM_RELEASE)

SOURCE_STORE = "store"
SOURCE_ROLLUP = "rollup"
EXECUTION_SOURCES = (SOURCE_STORE, SOURCE_ROLLUP)
EXECUTION_KEYS = ("source", "rowsScanned", "durationMs", "sampled", "samplingRate")

INSIGHT_KINDS = ("trend", "funnel", "retention", "path", "distribution")
SEEDED_INSIGHT = "Weekly exports"
SEEDED_DASHBOARD = "Ledgerline weekly"
SEEDED_COHORT = "Exported this season"
SEEDED_DASHBOARD_TILES = 3

RELEASES = ("1.4.0", "1.5.0", "1.6.0")
NEWEST_RELEASE = "1.6.0"

FLAG_BOOLEAN = "fast-search"
FLAG_MULTIVARIATE = "export-v2"
FLAG_VARIANTS = {"control": 55, "compact": 30, "wide": 15}
FLAG_DEFAULT_VARIANT = "control"
FLAG_STATES = ("draft", "active", "scheduled", "ramping", "halted", "killed", "archived")
EVALUATION_REASONS = ("targeting_match", "rollout_bucket", "default", "killed",
                      "error_fallback")

EXPERIMENT_KEY = "export-v2-trial"
EXPERIMENT_SALT = "northlight-export-2026"
EXPERIMENT_PRIMARY_METRIC = TYPE_REPORT_EXPORTED
EXPERIMENT_GUARDRAIL_METRIC = "error_rate"
EXPERIMENT_EXPOSURE_EVENT = TYPE_EXPORT_PANEL

ISSUE_RESOLVED_TITLE = "TypeError: cannot read length of undefined"
ISSUE_UNRESOLVED_TITLE = "Timeout while exporting report"
ISSUE_RESOLVED_OCCURRENCES = 24
ISSUE_UNRESOLVED_OCCURRENCES = 9
ISSUE_STATUSES = ("unresolved", "resolved", "auto_resolved", "ignored", "regressed",
                  "muted")

SURVEY_KEY = "why-export"
SURVEY_QUESTION_KINDS = ("open_text", "single_choice", "multiple_choice", "rating",
                         "recommendation")
SURVEY_ANSWERS = 18
SURVEY_SMALL_THEME = 5

DESTINATION_OPEN = "warehouse-sink"
DESTINATION_HEALTHY = "metrics-mirror"
DESTINATION_BACKLOG = 41

STATE_CHIPS = ("draft", "active", "scheduled", "paused", "failed", "archived")
SCRUBBER_TRACKS = ("frames", "events", "errors", "gaps", "activity")
FIELD_STATES = ("live", "brushing", "cohort-resolved", "held")
RAIL_DESTINATIONS = ("grain", "insights", "dashboards", "replay", "flags",
                     "experiments", "issues", "pipeline")
SHARE_SCOPES = ("frozen", "live")

HOOK_BAND = "data-band"
HOOK_FIELD_STATE = "data-field-state"
HOOK_SOURCE = "data-source"
HOOK_RAIL = "data-rail"
HOOK_STATE_CHIP = "data-state-chip"
HOOK_TRACK = "data-track"
HOOK_SHARE_SCOPE = "data-share-scope"

LIMIT_KEYS = ("eventsPerRequest", "eventsPerProject", "projectsPerWorkspace",
              "flagsPerProject", "variantsPerFlag", "stepsPerFunnel",
              "tilesPerDashboard", "questionsPerSurvey", "conditionsPerRule",
              "ruleNestingDepth", "sharesPerProject", "rowsPerQuery",
              "breakdownCardinality")
LIMIT_EVENTS_PER_REQUEST = 500
LIMIT_STEPS_PER_FUNNEL = 20
LIMIT_TILES_PER_DASHBOARD = 40
LIMIT_QUESTIONS_PER_SURVEY = 20
LIMIT_CONDITIONS_PER_RULE = 24
LIMIT_RULE_NESTING = 3
LIMIT_VARIANTS_PER_FLAG = 8
LIMIT_SHARES_PER_PROJECT = 50
LIMIT_ROWS_PER_QUERY = 2000000
LIMIT_BREAKDOWN_CARDINALITY = 10000
LIMIT_DRY_RUN_EVENTS = 100

DEDUPE_WINDOW_HOURS = 24
MERGE_REVERSAL_DAYS = 30
SHARE_DEFAULT_EXPIRY_DAYS = 7
ROLLOUT_CONFIRMATION_JUMP = 25
POWER_CONFIRMATION_FLOOR = 0.60

ERROR_CODES = (
    "unauthenticated", "invalid_credential", "insufficient_scope", "forbidden",
    "not_found", "conflict", "version_mismatch", "validation_failed",
    "payload_too_large", "rate_limited", "quota_exceeded", "idempotency_key_reused",
    "cursor_sort_mismatch", "sort_not_indexed", "project_mismatch", "person_erased",
    "workspace_held", "local_only_processing", "dry_run_required", "internal",
)
CODE_HELD = "workspace_held"
CODE_LOCAL_ONLY = "local_only_processing"
CODE_ERASED = "person_erased"
CODE_PROJECT_MISMATCH = "project_mismatch"
CODE_DRY_RUN = "dry_run_required"
CODE_VERSION = "version_mismatch"
CODE_SCOPE = "insufficient_scope"

DISABLED_CAPABILITIES = ("survey_theme_clustering", "destination_delivery")
METERED_DIMENSIONS = ("events", "recordings", "flagEvaluations", "exceptions",
                      "rowsScanned")
HELD_REFUSED_OPERATIONS = ("flag_publish", "flag_kill", "experiment_ship",
                           "person_erase", "share_revoke", "key_revoke")
KEY_SCOPES = ("event:read", "insight:write", "flag:write", "experiment:write",
              "pipeline:write", "share:write")
PROJECTION_WINDOW_DAYS = 7

RATE_LIMIT_HEADERS = ("X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset")
SECURITY_HEADERS = ("Strict-Transport-Security", "X-Content-Type-Options")

ROUTE_LOGIN = "/login"
ROUTE_SIGNUP = "/signup"
ROUTE_PRIVACY = "/privacy"
ROUTE_COMMAND = "/go"
ROUTE_HEALTH_PAGE = "/w/health"
ROUTE_SYNC = "/w/sync"
ROUTE_SHARES = "/w/shares"
ROUTE_SETTINGS = "/w/settings"
PUBLIC_ROUTES = (ROUTE_LOGIN, ROUTE_SIGNUP, ROUTE_PRIVACY)

APP_ROOT = "/app"
CREDENTIALS_FILE = "/app/USER_README.md"
SCREENSHOT_DIR = "/app/.browser_screenshots"
DOWNLOAD_DIR = "/app/.downloads"

TABLE_EVENTS = "events"
TABLE_PERSONS = "persons"
TABLE_OPERATIONS = "operations"

SETTLE_SECONDS = 0.25
POLL_TIMEOUT_SECONDS = 25.0
THREAD_TIMEOUT_SECONDS = 30.0

CLIENT_ERROR = range(400, 500)
DENIED = (401, 403)
NOT_FOUND = (403, 404)
CONFLICT = (409,)
CREATED = (200, 201)
OK = (200, 201, 202, 204)
REFUSED = (400, 401, 403, 404, 409, 422)


def settle() -> None:
    """Yield briefly so a write can land before the next read."""
    time.sleep(SETTLE_SECONDS)


def poll_until(predicate, timeout: float = POLL_TIMEOUT_SECONDS):
    """Bounded poll on a monotonic clock. Returns the last value the predicate saw."""
    deadline = time.monotonic() + timeout
    value = None
    while time.monotonic() < deadline:
        value = predicate()
        if value:
            return value
        settle()
    return value


def unique_suffix() -> str:
    """A per-run identifier so a self-seeding check never collides with itself."""
    return os.urandom(5).hex()


def probe_distinct_id(suffix: str) -> str:
    return "probe-" + suffix


def probe_address(suffix: str) -> str:
    """A per-run address, only ever compared against itself."""
    return "probe-" + suffix + "@" + "example.com"


def probe_name(suffix: str) -> str:
    return "Probe " + suffix


def describe(response: httpx.Response, what: str) -> str:
    """The failure-message shape reference/J requires: anchor, request, status, body."""
    return (f"{what}: {response.request.method} {response.request.url} returned "
            f"{response.status_code}: {response.text[:400]}")


def is_client_error(response: httpx.Response) -> bool:
    return response.status_code in CLIENT_ERROR


def error_body(response: httpx.Response) -> dict:
    """The `error` object of a refusal, which carries `code`, `message`, `traceId`."""
    try:
        payload = response.json()
    except ValueError:
        raise AssertionError(describe(
            response, "a refusal must carry a JSON body naming its error")) from None
    error = payload.get("error") if isinstance(payload, dict) else None
    if not isinstance(error, dict):
        raise AssertionError(describe(
            response, "a refusal must carry an `error` object"))
    return error


def error_code(response: httpx.Response) -> str:
    return str(error_body(response).get("code") or "")


def fetch_document(path: str) -> httpx.Response:
    """Fetch a page from the app origin rather than from the API base."""
    return httpx.get(appclient.app_url() + path, timeout=30.0, follow_redirects=True)


def ingest_url() -> str:
    return appclient.app_url() + "/i/v1/events"


def projects_path() -> str:
    return "/projects"


def project_path(slug: str) -> str:
    return f"/projects/{slug}"


def field_path(slug: str) -> str:
    return f"/projects/{slug}/field"


def events_path(slug: str) -> str:
    return f"/projects/{slug}/events"


def cohort_resolve_path(slug: str) -> str:
    return f"/projects/{slug}/cohorts/resolve"


def cohorts_path(slug: str) -> str:
    return f"/projects/{slug}/cohorts"


def query_path(slug: str) -> str:
    return f"/projects/{slug}/query"


def insights_path(slug: str) -> str:
    return f"/projects/{slug}/insights"


def insight_result_path(slug: str, insight_id: str) -> str:
    return f"/projects/{slug}/insights/{insight_id}/result"


def dashboards_path(slug: str) -> str:
    return f"/projects/{slug}/dashboards"


def person_path(slug: str, person_id: str) -> str:
    return f"/projects/{slug}/persons/{person_id}"


def person_resolve_path(slug: str) -> str:
    return f"/projects/{slug}/persons/resolve"


def access_package_path(slug: str, person_id: str) -> str:
    return f"/projects/{slug}/persons/{person_id}/access-package"


def erase_path(slug: str, person_id: str) -> str:
    return f"/projects/{slug}/persons/{person_id}/erase"


def erasure_path(slug: str, erasure_id: str) -> str:
    return f"/projects/{slug}/erasures/{erasure_id}"


def flags_path(slug: str) -> str:
    return f"/projects/{slug}/flags"


def flag_path(slug: str, key: str) -> str:
    return f"/projects/{slug}/flags/{key}"


def blast_radius_path(slug: str, key: str) -> str:
    return f"/projects/{slug}/flags/{key}/blast-radius"


def kill_path(slug: str, key: str) -> str:
    return f"/projects/{slug}/flags/{key}/kill"


def evaluate_path(slug: str) -> str:
    return f"/projects/{slug}/flags/evaluate"


def evaluations_path(slug: str, key: str) -> str:
    return f"/projects/{slug}/flags/{key}/evaluations"


def scheduled_changes_path(slug: str, key: str) -> str:
    return f"/projects/{slug}/flags/{key}/scheduled-changes"


def experiments_path(slug: str) -> str:
    return f"/projects/{slug}/experiments"


def experiment_path(slug: str, key: str) -> str:
    return f"/projects/{slug}/experiments/{key}"


def power_path(slug: str, key: str) -> str:
    return f"/projects/{slug}/experiments/{key}/power"


def results_path(slug: str, key: str) -> str:
    return f"/projects/{slug}/experiments/{key}/results"


def ship_path(slug: str, key: str) -> str:
    return f"/projects/{slug}/experiments/{key}/ship"


def issues_path(slug: str) -> str:
    return f"/projects/{slug}/issues"


def issue_path(slug: str, issue_id: str) -> str:
    return f"/projects/{slug}/issues/{issue_id}"


def recordings_path(slug: str) -> str:
    return f"/projects/{slug}/recordings"


def recording_path(slug: str, recording_id: str) -> str:
    return f"/projects/{slug}/recordings/{recording_id}"


def surveys_path(slug: str) -> str:
    return f"/projects/{slug}/surveys"


def destinations_path(slug: str) -> str:
    return f"/projects/{slug}/destinations"


def dry_run_path(slug: str, destination_id: str) -> str:
    return f"/projects/{slug}/destinations/{destination_id}/dry-run"


def replay_path(slug: str, destination_id: str) -> str:
    return f"/projects/{slug}/destinations/{destination_id}/replay"


def shares_path(slug: str) -> str:
    return f"/projects/{slug}/shares"


def share_path(slug: str, share_id: str) -> str:
    return f"/projects/{slug}/shares/{share_id}"


def public_share_path(token: str) -> str:
    return f"/public/shares/{token}"


def held_path() -> str:
    return "/workspace/held"


def pending_path() -> str:
    return "/workspace/pending"


def release_hold_path() -> str:
    return "/workspace/release"


def conflicts_path() -> str:
    return "/workspace/conflicts"


def processing_path() -> str:
    return "/workspace/processing"


def operations_path() -> str:
    return "/workspace/operations"


def audit_verify_path() -> str:
    return "/workspace/audit/verify"


def workspace_health_path() -> str:
    return "/workspace/health"


def keys_path() -> str:
    return "/keys"


def step_up_path() -> str:
    return "/auth/step-up"


def read_envelope(client: httpx.Client, path: str, **params) -> dict:
    """A list endpoint answers `{data: [...], page: {...}}`; nothing else is accepted."""
    response = client.get(path, params=params or None)
    assert response.status_code == 200, describe(
        response, f"the list at {path} must answer")
    payload = response.json()
    assert isinstance(payload, dict), describe(
        response, f"the list at {path} must answer an object carrying data and page")
    assert isinstance(payload.get("data"), list), describe(
        response, f"the list at {path} must carry a `data` array")
    assert isinstance(payload.get("page"), dict), describe(
        response, f"the list at {path} must carry a `page` object")
    return payload


def read_rows(client: httpx.Client, path: str, **params) -> list:
    return read_envelope(client, path, **params)["data"]


def read_all_rows(client: httpx.Client, path: str, limit: int = 200, **params) -> list:
    """Every row of a keyset-paginated collection, following the cursor to the end."""
    rows, cursor, guard = [], None, 0
    while guard < 200:
        guard += 1
        query = dict(params)
        query["limit"] = limit
        if cursor:
            query["cursor"] = cursor
        page = read_envelope(client, path, **query)
        rows.extend(page["data"])
        meta = page["page"]
        cursor = meta.get("nextCursor")
        if not meta.get("hasMore") or not cursor:
            break
    return rows


def find_by(rows: list, key: str, value):
    for row in rows:
        if isinstance(row, dict) and row.get(key) == value:
            return row
    return None


def project_document(client: httpx.Client, slug: str) -> dict:
    response = client.get(project_path(slug))
    assert response.status_code == 200, describe(
        response, f"the project {slug} must answer with its limits")
    return response.json()


def archive_bounds(client: httpx.Client, slug: str = PROJECT_ARCHIVE) -> tuple[str, str]:
    """The whole-archive span, taken from the project document rather than a clock."""
    doc = project_document(client, slug)
    lo = doc.get("archiveFrom") or doc.get("firstEventAt")
    hi = doc.get("archiveTo") or doc.get("lastEventAt")
    assert lo and hi, (
        f"the project {slug} must state the bounds of its archive so a viewport can "
        f"be framed on the whole of it, saw keys {sorted(doc)}")
    return str(lo), str(hi)


def field_answer(client: httpx.Client, slug: str, band: str, lo: str, hi: str,
                 **params) -> dict:
    query = {"from": lo, "to": hi, "band": band}
    query.update(params)
    response = client.get(field_path(slug), params=query)
    assert response.status_code == 200, describe(
        response, f"the field at band {band} must answer for the requested span")
    payload = response.json()
    assert isinstance(payload, dict), describe(
        response, "the field answer must be an object carrying band, total, persons")
    return payload


def resolve_cohort(client: httpx.Client, slug: str, lo: str, hi: str,
                   **body) -> dict:
    payload = {"from": lo, "to": hi}
    payload.update(body)
    response = client.post(cohort_resolve_path(slug), json=payload)
    assert response.status_code in CREATED, describe(
        response, "resolving a brushed region must answer a cohort")
    return response.json()


def run_query(client: httpx.Client, slug: str, body: dict) -> dict:
    response = client.post(query_path(slug), json=body)
    assert response.status_code in CREATED, describe(
        response, "a typed query must answer a result with its execution provenance")
    return response.json()


def execution_of(result: dict) -> dict:
    execution = result.get("execution")
    assert isinstance(execution, dict), (
        f"every result must carry an `execution` object, saw keys {sorted(result)}")
    return execution


def step_up_token(client: httpx.Client) -> str:
    response = client.post(step_up_path(), json={"password": SEEDED_PASSWORD})
    assert response.status_code in CREATED, describe(
        response, "re-confirming the password must return a step-up token")
    token = response.json().get("stepUpToken")
    assert token, "the step-up answer must carry a stepUpToken"
    return str(token)


def run_together(calls: list) -> list:
    """Run callables at the same moment and return their results in order.

    A future re-raises in the calling thread, so a failure inside one call surfaces
    as a failure here rather than being caught and turned into a value.
    """
    barrier = threading.Barrier(len(calls))

    def runner(call):
        barrier.wait(timeout=THREAD_TIMEOUT_SECONDS)
        return call()

    with futures.ThreadPoolExecutor(max_workers=len(calls)) as pool:
        pending = [pool.submit(runner, call) for call in calls]
        return [future.result(timeout=THREAD_TIMEOUT_SECONDS) for future in pending]


def _client_for(email: str) -> httpx.Client:
    return appclient.client(appclient.login(email, SEEDED_PASSWORD))


@pytest.fixture()
def owner():
    with _client_for(OWNER_EMAIL) as client:
        yield client


@pytest.fixture()
def outsider():
    with _client_for(OTHER_EMAIL) as client:
        yield client


@pytest.fixture()
def anonymous():
    with appclient.client(None) as client:
        yield client


@pytest.fixture()
def backend():
    return capabilities.make_backend()
