"""Fixtures, domain constants and the pinned literals for Relational Database Platform.

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
CREATOR_EMAIL = "creator@example.com"
EDITOR_EMAIL = "editor@example.com"
COMMENTER_EMAIL = "commenter@example.com"
READER_EMAIL = "reader@example.com"
OWNER2_EMAIL = "owner2@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"

OWNER_NAME = "Nadia Holt"
CREATOR_NAME = "Piotr Selby"
EDITOR_NAME = "Rosa Ibekwe"
COMMENTER_NAME = "Tomas Frey"
READER_NAME = "Lena Ward"
OWNER2_NAME = "Idris Vaughn"

ROLE_OWNER = "owner"
ROLE_CREATOR = "creator"
ROLE_EDITOR = "editor"
ROLE_COMMENTER = "commenter"
ROLE_READER = "reader"
ALL_ROLES = (ROLE_OWNER, ROLE_CREATOR, ROLE_EDITOR, ROLE_COMMENTER, ROLE_READER)

NORTHFIELD_SLUG = "northfield-commercial"
HARBOURLINE_SLUG = "harbourline-studio"
NORTHFIELD_NAME = "Northfield Commercial"
HARBOURLINE_NAME = "Harbourline Studio"

BASE_CAMPAIGN_PLANNING = "Campaign Planning"
BASE_STUDIO_ROSTER = "Studio Roster"

TABLE_CAMPAIGNS = "Campaigns"
TABLE_DELIVERABLES = "Deliverables"
TABLE_TASKS = "Tasks"
TABLE_PEOPLE = "People"
CAMPAIGN_PLANNING_TABLES = (TABLE_CAMPAIGNS, TABLE_DELIVERABLES, TABLE_TASKS)

FIELD_NAME = "Name"
FIELD_STAGE = "Stage"
FIELD_BUDGET = "Budget"
FIELD_DELIVERABLES = "Deliverables"
FIELD_TOTAL_HOURS = "Total Hours"
FIELD_DELIVERABLE_COUNT = "Deliverable Count"
FIELD_OWNER_NOTE = "Owner Note"
FIELD_TITLE = "Title"
FIELD_DUE = "Due"
FIELD_DONE = "Done"
FIELD_ESTIMATE = "Estimate"
FIELD_TASKS = "Tasks"
FIELD_HOURS = "Hours"
FIELD_TASK_NAMES = "Task Names"
FIELD_MINUTES = "Minutes"
FIELD_URGENCY = "Urgency"
FIELD_LABELS = "Labels"
FIELD_LOGGED = "Logged"
FIELD_CREATED = "Created"
FIELD_REF = "Ref"
FIELD_CRAFT = "Craft"

CAMPAIGN_AUTUMN = "Autumn Lantern"
CAMPAIGN_HARBOUR = "Harbour Nights"
CAMPAIGN_WINTER = "Winter Ledger"
SEEDED_CAMPAIGNS = (CAMPAIGN_AUTUMN, CAMPAIGN_HARBOUR, CAMPAIGN_WINTER)
DELIVERABLE_LAUNCH_FILM = "Launch film"
DELIVERABLE_PRINT_RUN = "Print run"
DELIVERABLE_SITE_REFRESH = "Site refresh"
DELIVERABLE_PRESS_PACK = "Press pack"
DELIVERABLE_SIGNAGE = "Signage"
DELIVERABLE_MAILER = "Mailer"
SEEDED_DELIVERABLES = (
    DELIVERABLE_LAUNCH_FILM, DELIVERABLE_PRINT_RUN, DELIVERABLE_SITE_REFRESH,
    DELIVERABLE_PRESS_PACK, DELIVERABLE_SIGNAGE, DELIVERABLE_MAILER,
)
PERSON_ADA = "Ada Renn"
PERSON_BO = "Bo Kessler"

STAGE_PLANNING = "Planning"
STAGE_LIVE = "Live"
STAGE_WRAPPED = "Wrapped"
SEEDED_STAGES = (STAGE_PLANNING, STAGE_LIVE, STAGE_WRAPPED)

BUDGET_AUTUMN = "1200.00"
BUDGET_HARBOUR = "800.00"
BUDGET_WINTER = "450.00"
BUDGET_PROBE = "1450.00"
BUDGET_SUM = "2000.00"

FIELD_TYPE_SLUGS = (
    "singleLineText", "multilineText", "number", "currency", "percent", "checkbox",
    "singleSelect", "multipleSelects", "date", "dateTime", "rating", "duration",
    "multipleRecordLinks", "multipleLookupValues", "rollup", "count", "formula",
    "createdTime", "autoNumber",
)
COMPUTED_TYPE_SLUGS = (
    "multipleLookupValues", "rollup", "count", "formula", "createdTime", "autoNumber",
)
FIELD_TYPE_COUNT = 19

ROLLUP_AGGREGATIONS = (
    "AND", "OR", "XOR", "SUM", "AVERAGE", "MAX", "MIN", "COUNT", "COUNTA", "COUNTALL",
    "ARRAYCOMPACT", "ARRAYFLATTEN", "ARRAYJOIN", "ARRAYSLICE", "ARRAYUNIQUE",
    "CONCATENATE",
)
ROLLUP_COUNT = 16

FORMULA_FUNCTIONS = (
    "IF", "CONCATENATE", "LEN", "LOWER", "UPPER", "TRIM", "FIND", "SEARCH", "SUM",
    "ROUND", "DATETIME_DIFF", "TODAY",
)
FORMULA_FUNCTION_COUNT = 12

VIEW_GRID = "grid"
VIEW_GALLERY = "gallery"
VIEW_KANBAN = "kanban"
VIEW_TYPES = (VIEW_GRID, VIEW_GALLERY, VIEW_KANBAN)
MODE_COLLABORATIVE = "collaborative"
MODE_PERSONAL = "personal"
MODE_LOCKED = "locked"
VIEW_MODES = (MODE_COLLABORATIVE, MODE_PERSONAL, MODE_LOCKED)

GUARD_BLOCKING = "blocking"
GUARD_ADVISORY = "advisory"
GUARD_BLOCKING_MESSAGE = "A deliverable cannot be marked Done with an empty estimate."
GUARD_ADVISORY_MESSAGE = "A campaign over 40 hours of tasks usually needs a second owner."

MAX_FIELDS_PER_TABLE = 500
MAX_TABLES_PER_BASE = 100
MAX_BASES_PER_WORKSPACE = 1000
MAX_VIEWS_PER_TABLE = 1000
MAX_FILTER_CONDITIONS = 49
MAX_FILTER_NESTING = 3
MAX_GROUP_LEVELS = 3
MAX_SORT_LEVELS = 10
MAX_KANBAN_STACKS = 200
MAX_RECORDS_PER_BASE = 50000
MAX_GUARDS_PER_BASE = 200

IDENTIFIER_LENGTH = 17
PREFIX_WORKSPACE = "wsp"
PREFIX_BASE = "bas"
PREFIX_TABLE = "tbl"
PREFIX_VIEW = "viw"
PREFIX_FIELD = "fld"
PREFIX_RECORD = "rec"
PREFIX_GUARD = "grd"
PREFIX_OPERATION = "opn"
IDENTIFIER_EXAMPLE = "rec7QW2M4KX9T0ZB1"

CHOICE_COLOURS = ("blue", "cyan", "teal", "green", "yellow", "orange", "red", "pink",
                  "purple", "grey")
CHOICE_COLOUR_COUNT = 10

NINETY_MINUTES_SECONDS = 5400
WORKED_COUNT = 2
WORKED_COUNTA = 3
WORKED_COUNTALL = 4
WORKED_SUM = 12

HOOK_VIEW = "data-view"
HOOK_MODE = "data-mode"
HOOK_FIELD_TYPE = "data-field-type"
HOOK_RECORD_ID = "data-record-id"
HOOK_GUARD_MODE = "data-guard-mode"
MODE_LIVE = "live"
MODE_HISTORY = "history"

ROUTE_LOGIN = "/login"
ROUTE_SIGNUP = "/signup"
ROUTE_PALETTE = "/go"
ROUTE_WORKSPACES = "/workspaces"
ROUTE_PRIVACY = "/privacy"
PUBLIC_ROUTES = (ROUTE_LOGIN, ROUTE_SIGNUP, ROUTE_PRIVACY)

APP_ROOT = "/app"
CREDENTIALS_FILE = "/app/USER_README.md"
SCREENSHOT_DIR = "/app/.browser_screenshots"
DOWNLOAD_DIR = "/app/.downloads"

TABLE_OPERATIONS = "operations"
TABLE_RECORDS = "records"
TABLE_CELLS = "cells"

SETTLE_SECONDS = 0.25
POLL_TIMEOUT_SECONDS = 25.0
THREAD_TIMEOUT_SECONDS = 30.0

CLIENT_ERROR = range(400, 500)
DENIED = (401, 403)
NOT_FOUND = (403, 404)
CONFLICT = (409,)
CREATED = (200, 201)
OK = (200, 201, 204)
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
    return os.urandom(4).hex()


def probe_title(suffix: str) -> str:
    return "Probe " + suffix


def probe_address(suffix: str) -> str:
    """A per-run address, only ever compared against itself."""
    return "probe-" + suffix + "@" + "example.com"


def describe(response: httpx.Response, what: str) -> str:
    """The failure-message shape reference/J requires: anchor, request, status, body."""
    return (f"{what}: {response.request.method} {response.request.url} returned "
            f"{response.status_code}: {response.text[:400]}")


def is_client_error(response: httpx.Response) -> bool:
    return response.status_code in CLIENT_ERROR


def error_message(response: httpx.Response) -> str:
    """The `message` of a refusal body, which a blocking guard carries verbatim."""
    try:
        payload = response.json()
    except ValueError:
        raise AssertionError(describe(
            response, "a refusal must carry a JSON body naming its message")) from None
    error = payload.get("error") if isinstance(payload, dict) else None
    if isinstance(error, dict):
        return str(error.get("message") or "")
    return ""


def fetch_document(path: str) -> httpx.Response:
    """Fetch a page from the app origin rather than from the API base."""
    return httpx.get(appclient.app_url() + path, timeout=30.0, follow_redirects=True)


def workspaces_path() -> str:
    return "/workspaces"


def bases_path(workspace_id: str) -> str:
    return f"/workspaces/{workspace_id}/bases"


def base_path(base_id: str) -> str:
    return f"/bases/{base_id}"


def records_path(base_id: str, table_id: str) -> str:
    return f"/bases/{base_id}/tables/{table_id}/records"


def record_path(base_id: str, table_id: str, record_id: str) -> str:
    return f"/bases/{base_id}/tables/{table_id}/records/{record_id}"


def record_history_path(base_id: str, table_id: str, record_id: str) -> str:
    return f"/bases/{base_id}/tables/{table_id}/records/{record_id}/history"


def fields_path(base_id: str, table_id: str) -> str:
    return f"/bases/{base_id}/tables/{table_id}/fields"


def field_path(base_id: str, table_id: str, field_id: str) -> str:
    return f"/bases/{base_id}/tables/{table_id}/fields/{field_id}"


def view_path(base_id: str, view_id: str) -> str:
    return f"/bases/{base_id}/views/{view_id}"


def operations_path(base_id: str) -> str:
    return f"/bases/{base_id}/operations"


def replay_path(base_id: str) -> str:
    return f"/bases/{base_id}/operations/replay"


def guards_path(base_id: str) -> str:
    return f"/bases/{base_id}/guards"


def guard_path(base_id: str, guard_id: str) -> str:
    return f"/bases/{base_id}/guards/{guard_id}"


def field_types_path() -> str:
    return "/field-types"


def read_array(client: httpx.Client, path: str, **params) -> list:
    """A list endpoint answers with a TOP-LEVEL JSON array; nothing else is accepted."""
    response = client.get(path, params=params or None)
    assert response.status_code == 200, describe(
        response, f"the list at {path} must answer")
    payload = response.json()
    assert isinstance(payload, list), describe(
        response, f"the list at {path} must be a top-level JSON array")
    return payload


def find_by(rows: list, key: str, value):
    for row in rows:
        if isinstance(row, dict) and row.get(key) == value:
            return row
    return None


def workspace_by_slug(client: httpx.Client, slug: str) -> dict:
    rows = read_array(client, workspaces_path())
    found = find_by(rows, "slug", slug)
    assert found is not None, (
        f"the workspace {slug} must appear in the workspace list, saw "
        f"{[r.get('slug') for r in rows if isinstance(r, dict)]}")
    return found


def base_by_name(client: httpx.Client, workspace_id: str, name: str) -> dict:
    rows = read_array(client, bases_path(workspace_id))
    found = find_by(rows, "name", name)
    assert found is not None, (
        f"the base {name} must appear in workspace {workspace_id}, saw "
        f"{[r.get('name') for r in rows if isinstance(r, dict)]}")
    return found


def base_document(client: httpx.Client, base_id: str) -> dict:
    response = client.get(base_path(base_id))
    assert response.status_code == 200, describe(
        response, f"the base {base_id} must answer with its tables, fields and views")
    return response.json()


def table_in(base: dict, name: str) -> dict:
    found = find_by(base.get("tables") or [], "name", name)
    assert found is not None, (
        f"the table {name} must exist in the base, saw "
        f"{[t.get('name') for t in (base.get('tables') or [])]}")
    return found


def field_in(table: dict, name: str) -> dict:
    found = find_by(table.get("fields") or [], "name", name)
    assert found is not None, (
        f"the field {name} must exist on table {table.get('name')}, saw "
        f"{[f.get('name') for f in (table.get('fields') or [])]}")
    return found


def grid_view_of(table: dict) -> dict:
    for view in table.get("views") or []:
        if isinstance(view, dict) and view.get("type") == VIEW_GRID:
            return view
    raise AssertionError(
        f"table {table.get('name')} must carry at least one grid view, saw "
        f"{[v.get('type') for v in (table.get('views') or [])]}")


def record_by_primary(client: httpx.Client, base_id: str, table: dict, value: str) -> dict:
    primary = next((f for f in (table.get("fields") or []) if f.get("isPrimary")), None)
    assert primary is not None, f"table {table.get('name')} must carry a primary field"
    rows = read_array(client, records_path(base_id, table["id"]))
    for row in rows:
        cells = row.get("cells") or {}
        if cells.get(primary["id"]) == value:
            return row
    raise AssertionError(
        f"the record {value} must exist in {table.get('name')}, saw "
        f"{[(r.get('cells') or {}).get(primary['id']) for r in rows]}")


def campaign_planning(client: httpx.Client) -> tuple[str, dict]:
    """(base_id, base document) for the seeded demonstration base."""
    workspace = workspace_by_slug(client, NORTHFIELD_SLUG)
    base = base_by_name(client, workspace["id"], BASE_CAMPAIGN_PLANNING)
    return base["id"], base_document(client, base["id"])


def latest_sequence(client: httpx.Client, base_id: str) -> int:
    rows = read_array(client, operations_path(base_id))
    assert rows, f"the operation log of base {base_id} must carry at least one operation"
    return max(int(row["sequence"]) for row in rows)


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
def creator():
    with _client_for(CREATOR_EMAIL) as client:
        yield client


@pytest.fixture()
def editor():
    with _client_for(EDITOR_EMAIL) as client:
        yield client


@pytest.fixture()
def commenter():
    with _client_for(COMMENTER_EMAIL) as client:
        yield client


@pytest.fixture()
def reader():
    with _client_for(READER_EMAIL) as client:
        yield client


@pytest.fixture()
def outsider():
    with _client_for(OWNER2_EMAIL) as client:
        yield client


@pytest.fixture()
def anonymous():
    with appclient.client(None) as client:
        yield client


@pytest.fixture()
def backend():
    return capabilities.make_backend()
