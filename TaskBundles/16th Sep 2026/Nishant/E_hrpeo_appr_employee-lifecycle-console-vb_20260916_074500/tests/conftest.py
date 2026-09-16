"""Task fixtures for deku/employee-lifecycle-console-vb.

Two rules govern this file. Nothing here assumes the agent's framework, file
layout, ORM or module names: the only assumptions are the App Contract and what
instruction.md pinned literally. And nothing here reaches a provider SDK; the
domain helpers are composed from the generic primitives in capabilities.py, so
swapping a slot's provider replaces the adapter rather than this file.
"""

from __future__ import annotations

import os
import time
import uuid

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, make_backend

EMPLOYEE_EMAIL = "employee@example.com"
EMPLOYEE2_EMAIL = "employee2@example.com"
EMPLOYEE3_EMAIL = "employee3@example.com"
MANAGER_EMAIL = "manager@example.com"
MANAGER2_EMAIL = "manager2@example.com"
PAYROLL_EMAIL = "payroll@example.com"
PAYROLL2_EMAIL = "payroll2@example.com"
CORPUS_PASSWORD = "deku-demo-pw-2026"

ORG_NAME = "Cadrix"
CURRENCY = "inr"

EMP_1001 = "E-1001"
EMP_1002 = "E-1002"
EMP_1003 = "E-1003"
EMP_1004 = "E-1004"
MGR_2001 = "E-2001"
MGR_2002 = "E-2002"
PAY_4001 = "E-4001"
PAY_4002 = "E-4002"

NAME_1001 = "Nadia Fernandes"
NAME_1002 = "Arjun Mehta"
NAME_1003 = "Sofia Ruiz"
NAME_1004 = "Marcus Bell"
NAME_2001 = "Priya Raman"
NAME_2002 = "Tomas Lindqvist"
NAME_4001 = "Daniel Okafor"
NAME_4002 = "Helen Zhao"

POLICY_ANNUAL = "ANNUAL"
POLICY_SICK = "SICK"
POLICY_UNPAID = "UNPAID"

CALENDAR_KA = "KA-2026"
CALENDAR_MH = "MH-2026"
HOLIDAY_DATE = "2026-08-19"
HOLIDAY_NAME = "Independence Observance"

LEAVE_FROM = "2026-08-17"
LEAVE_TO = "2026-08-21"
LEAVE_HALVES = 8

ANNUAL_BALANCE_HALVES = 36
ANNUAL_ACCRUAL_HALVES = 4
ANNUAL_CAP_HALVES = 60
ANNUAL_CARRY_HALVES = 10
ANNUAL_NOTICE_DAYS = 2
SICK_ACCRUAL_HALVES = 24
UNPAID_NEGATIVE_HALVES = 20

GROUP_CORE = "MONTHLY-CORE"
GROUP_OPS = "MONTHLY-OPS"
OPEN_PERIOD = "2026-07"
CLOSED_PERIODS = ("2026-05", "2026-06")
FRESH_PERIOD = "2026-08"

GROSS_1001 = 3100000
GROSS_1002 = 5000000
GROSS_1003 = 2000000
GROSS_1004 = 4000000
NET_1001 = 2806000
NET_1002 = 4675000
RUN_TOTAL_GROSS = 14000000
RUN_TOTAL_DEDUCTIONS = 925000
RUN_TOTAL_NET = 13075000
RUN_HEADCOUNT = 4

RULE_SET_CODE = "IN-2026-04"
RULE_SET_VERSION = 1
STATUTORY_CODES = ("PF", "ESI", "PT", "LWF", "TDS")

RECEIPT_THRESHOLD_MINOR = 200000
MANAGER_CLAIM_LIMIT_MINOR = 1000000
ESCALATED_CLAIM_MINOR = 2500000
SEEDED_CLAIM_COUNT = 12
SEEDED_EMPLOYEE_COUNT = 120
SEEDED_ATTENDANCE_DAYS = 31
SEEDED_UNPAIRED_DAYS = 4
SEEDED_OPEN_REGULARISATIONS = 2
ESCALATION_DAYS = 3
BULK_UNDO_SECONDS = 10

PAGE_SIZE = 50
PAGE_SIZE_MAX = 500
CURSOR_HEADER = "X-Next-Cursor"

PUNCH_RETENTION_YEARS = 3
AUDIT_RETENTION_YEARS = 7

COPY_EMPTY_DIRECTORY = "No people yet"
COPY_EMPTY_QUEUE = "Nothing waiting"
COPY_NOT_YOUR_REPORT = "Not your report"
COPY_SELF_DECISION = "You cannot decide your own request"
COPY_ALREADY_DECIDED = "Already decided"
COPY_SAME_ACTOR = "Sign-off needs a second pair of eyes"
COPY_TOTAL_MISMATCH = "That total does not match the run"
COPY_NARROW_REGISTER = "The register needs a wider window"
COPY_NOT_FOUND = "That page does not exist"

OK = (200, 201, 202)
DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
REFUSED = (400, 403, 409, 422)
REFUSED_OR_DENIED = (400, 401, 403, 409, 422)

SETTLE_SECONDS = 2.0
POLL_SECONDS = 60.0

SECRET_MARKERS = (
    "AUTH_CLIENT_SECRET",
    "cadrix-client-7f3b19d4",
    "deku-local-dev",
    "postgresql://",
    "deku-realm-admin",
)


def settle() -> None:
    """The one sanctioned sleep: a bounded wait before asserting a non-event."""
    time.sleep(SETTLE_SECONDS)


def poll_until(predicate, timeout: float = POLL_SECONDS):
    """Poll a predicate to a monotonic deadline. Returns the truthy value or None."""
    deadline = time.monotonic() + timeout
    while True:
        value = predicate()
        if value:
            return value
        if time.monotonic() >= deadline:
            return None
        settle()


def unique_suffix() -> str:
    return uuid.uuid4().hex[:10]


def api(path: str) -> str:
    return f"/api{path}"


def app_origin() -> str:
    return os.environ["APP_PUBLIC_URL"].rstrip("/")


def expected_issuer() -> str:
    """The realm the environment declares, which is the only legal token issuer."""
    return os.environ["AUTH_ISSUER_URL"].rstrip("/")


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture()
def employee_client():
    token = login(EMPLOYEE_EMAIL, seeded_password("SEED_EMPLOYEE_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def employee2_client():
    token = login(EMPLOYEE2_EMAIL, seeded_password("SEED_EMPLOYEE2_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def employee3_client():
    token = login(EMPLOYEE3_EMAIL, seeded_password("SEED_EMPLOYEE3_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def manager_client():
    token = login(MANAGER_EMAIL, seeded_password("SEED_MANAGER_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def manager2_client():
    token = login(MANAGER2_EMAIL, seeded_password("SEED_MANAGER2_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def payroll_client():
    token = login(PAYROLL_EMAIL, seeded_password("SEED_PAYROLL_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def payroll2_client():
    token = login(PAYROLL2_EMAIL, seeded_password("SEED_PAYROLL2_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


class ConsoleStore:
    """Domain queries for this task, composed from capability primitives."""

    LEDGER_SIGN = {
        "opening": 1, "accrual": 1, "correction": 1,
        "availed": -1, "pending": -1, "encashment": -1, "lapse": -1,
    }

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def employee(self, employee_number: str) -> dict | None:
        return self._b.one("employee", employee_number=employee_number)

    def count_employees(self, **where) -> int:
        return self._b.count("employee", **where)

    def ledger_rows(self, employee_number: str, policy_code: str) -> list[dict]:
        return self._b.rows("leave_ledger_entry",
                            employee_number=employee_number, policy_code=policy_code)

    def ledger_balance_halves(self, employee_number: str, policy_code: str) -> int:
        total = 0
        for row in self.ledger_rows(employee_number, policy_code):
            total += self.LEDGER_SIGN.get(str(row.get("kind")), 0) * int(row.get("halves") or 0)
        return total

    def count_ledger(self, **where) -> int:
        return self._b.count("leave_ledger_entry", **where)

    def leave_request(self, request_id) -> dict | None:
        return self._b.one("leave_request", id=request_id)

    def count_leave_requests(self, **where) -> int:
        return self._b.count("leave_request", **where)

    def approval(self, approval_id) -> dict | None:
        return self._b.one("approval", id=approval_id)

    def approvals(self, **where) -> list[dict]:
        return self._b.rows("approval", **where)

    def count_punches(self, **where) -> int:
        return self._b.count("attendance_punch", **where)

    def punch_by_raw_ref(self, raw_ref: str) -> dict | None:
        return self._b.one("attendance_punch", raw_ref=raw_ref)

    def punches_on(self, employee_number: str) -> list[dict]:
        return self._b.rows("attendance_punch", employee_number=employee_number)

    def attendance_days(self, employee_number: str) -> list[dict]:
        return self._b.rows("attendance_day", employee_number=employee_number)

    def count_attendance_days(self, **where) -> int:
        return self._b.count("attendance_day", **where)

    def count_regularisations(self, **where) -> int:
        return self._b.count("regularisation", **where)

    def count_claims(self, **where) -> int:
        return self._b.count("claim", **where)

    def claim(self, claim_id) -> dict | None:
        return self._b.one("claim", id=claim_id)

    def run(self, period: str, group_code: str) -> dict | None:
        return self._b.one("payroll_run", period=period, group_code=group_code)

    def count_runs(self, **where) -> int:
        return self._b.count("payroll_run", **where)

    def payslips(self, run_id) -> list[dict]:
        return self._b.rows("payslip", run_id=run_id)

    def payslip(self, run_id, employee_number: str) -> dict | None:
        return self._b.one("payslip", run_id=run_id, employee_number=employee_number)

    def payslip_lines(self, payslip_id) -> list[dict]:
        return self._b.rows("payslip_line", payslip_id=payslip_id)

    def rule_sets(self, **where) -> list[dict]:
        return self._b.rows("statutory_rule_set", **where)

    def statutory_rules(self, **where) -> list[dict]:
        return self._b.rows("statutory_rule", **where)

    def count_audit(self, **where) -> int:
        return self._b.count("audit_entry", **where)

    def policy(self, code: str) -> dict | None:
        return self._b.one("leave_policy", code=code)

    def holiday_calendars(self) -> list[dict]:
        return self._b.rows("holiday_calendar")

    def payroll_groups(self) -> list[dict]:
        return self._b.rows("payroll_group")


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def console(backend: Backend) -> ConsoleStore:
    return ConsoleStore(backend)


def seed_employee_id(console: ConsoleStore, employee_number: str):
    row = console.employee(employee_number)
    assert row is not None, (
        f"seed employee {employee_number!r} is missing from the employee table"
    )
    return row["id"]


def open_run_row(console: ConsoleStore):
    row = console.run(OPEN_PERIOD, GROUP_CORE)
    assert row is not None, (
        f"the seeded open payroll run for period {OPEN_PERIOD!r} in group "
        f"{GROUP_CORE!r} is missing from the payroll_run table"
    )
    return row


def pending_approval_for(console: ConsoleStore, requester: str) -> dict | None:
    for row in console.approvals(kind="leave", requested_by=requester):
        if str(row.get("state")) == "pending":
            return row
    return None


def new_punch(employee_number: str, at: str, direction: str) -> dict:
    return {
        "employee_number": employee_number,
        "at": at,
        "direction": direction,
        "source": "device",
        "device_id": f"probe-{unique_suffix()}",
        "raw_ref": f"probe-{unique_suffix()}",
    }
