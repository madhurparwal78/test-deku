"""Task fixtures for deku/teamwork-platform-showcase-vb.

Implementation-agnostic (reference/J J.2): assume only the App Contract, the
literals pinned in instruction.md, and the two capability fixtures the declared
slots earn. Observations are made over the JSON API, over the served HTML of the
public routes, over the rows in postgres and over the messages in mailpit.
Nothing here imports an SDK, reads the agent's source, or probes for a feature at
run time. No test function lives in this file.
"""

from __future__ import annotations

import os
import time

import httpx
import pytest
from appclient import app_url, client, login
from capabilities import Backend, make_backend, make_inbox

SETTLE_SECONDS = 2.0
TIMEOUT = 30.0
EMAIL_DEADLINE_SECONDS = 60.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give a side effect time to land before asserting it did not happen."""
    time.sleep(seconds)


PASSWORD = "deku-demo-pw-2026"

ADMIN_EMAIL = "admin@example.com"
MEMBER_EMAIL = "member@example.com"
MEMBER2_EMAIL = "member2@example.com"
REQUESTER_EMAIL = "requester@example.com"
REQUESTER2_EMAIL = "requester2@example.com"

SEEDED_ACCOUNTS = (ADMIN_EMAIL, MEMBER_EMAIL, MEMBER2_EMAIL,
                   REQUESTER_EMAIL, REQUESTER2_EMAIL)

ROLE_REQUESTER = "requester"
ROLE_MEMBER = "member"
ROLE_ADMIN = "admin"

PROJECT_FIN = "FIN"
PROJECT_MKT = "MKT"
PROJECT_SUP = "SUP"
SEEDED_PROJECTS = (PROJECT_FIN, PROJECT_MKT, PROJECT_SUP)

STATUS_BLOCKED = "Blocked"
STATUS_IN_PROGRESS = "In progress"
STATUS_READY = "Ready for review"
STATUS_DONE = "Done"
FIN_STATUSES = (STATUS_BLOCKED, STATUS_IN_PROGRESS, STATUS_READY, STATUS_DONE)

CATEGORY_TO_DO = "to_do"
CATEGORY_IN_PROGRESS = "in_progress"
CATEGORY_DONE = "done"
STATUS_CATEGORIES = (CATEGORY_TO_DO, CATEGORY_IN_PROGRESS, CATEGORY_DONE)

TRANSITION_SEND_TO_REVIEW = "Send to review"
RULE_ASSIGN_REVIEW = "Assign review to the project lead"
FILTER_MY_OPEN_WORK = "My open work"
FILTER_TEXT = "assignee = currentUser() AND status != Done ORDER BY rank ASC"

BOUNDARY_ITEM = "FIN-2"
BOUNDARY_SUMMARY = "Validate transaction UX"
SEEDED_FIN_ITEMS = ("FIN-1", "FIN-2", "FIN-3", "FIN-4", "FIN-5", "FIN-6")
SEEDED_MKT_ITEMS = ("MKT-1", "MKT-2", "MKT-3")
SEEDED_ITEM_COUNT = 9

SUBJECT_PREFIX = "Northwind work update:"
BOUNDARY_SUBJECT = "Northwind work update: FIN-2 Validate transaction UX"

PUBLIC_ROUTES = ("/", "/products", "/products/work", "/products/work/pricing",
                 "/products/docs", "/products/service", "/products/ai",
                 "/platform", "/enterprise", "/customers", "/templates",
                 "/migration", "/company/contact/general", "/terms")

API_HEALTH = "/health"
API_PROJECTS = "/projects"
API_ITEMS = "/items"
API_FILTERS = "/filters"
API_RULES = "/rules"
API_PLANS = "/plans"
API_TEMPLATES = "/templates"
API_SIGNUP = "/signup"
API_PAGE_VIEWS = "/page-views"

STANDARD_MONTHLY_BANDS = ((10, 850), (100, 760), (1000, 640), (None, 520))
PREMIUM_MONTHLY_BANDS = ((10, 1700), (100, 1520), (1000, 1290), (None, 1050))
WORKED_STANDARD_300_TOTAL = 204900
WORKED_STANDARD_300_PER_USER = 683
WORKED_STANDARD_7_TOTAL = 5950
WORKED_STANDARD_7_PER_USER = 850
WORKED_PREMIUM_300_TOTAL = 411800
WORKED_PREMIUM_300_PER_USER = 1373

FREE_CAP_TEXT = "Not available above 10 users"
SAVING_BADGE = "SAVE UP TO 17%"

RULE_ALLOWANCE_FREE = 100
RULE_ALLOWANCE_STANDARD = 1700
RULE_ALLOWANCE_PREMIUM_PER_USER = 1000

OK = (200, 201)
DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
REFUSED = (400, 409, 422)


def probe_token() -> str:
    """A per-run token no other run collides with (reference/J J.5)."""
    return os.urandom(6).hex()


def probe_summary(prefix: str = "Probe item") -> str:
    return f"{prefix} {probe_token()}"


@pytest.fixture(scope="session")
def anon():
    """The JSON API under /api, with no credentials."""
    with client() as c:
        yield c


@pytest.fixture()
def admin_api():
    """A fresh admin token per test (reference/J J.11)."""
    with client(login(ADMIN_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def member_api():
    with client(login(MEMBER_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def member2_api():
    with client(login(MEMBER2_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def requester_api():
    with client(login(REQUESTER_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture(scope="session")
def site():
    """The served site itself, for reading HTML."""
    with httpx.Client(base_url=app_url(), timeout=TIMEOUT,
                      follow_redirects=True) as c:
        yield c


@pytest.fixture(scope="session")
def raw_site():
    """The site without redirect following, for asserting a status itself."""
    with httpx.Client(base_url=app_url(), timeout=TIMEOUT,
                      follow_redirects=False) as c:
        yield c


class WorkStore:
    """Provider-agnostic domain queries composed from Backend primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def item(self, item_key: str) -> dict | None:
        return self._b.one("work_items", item_key=item_key)

    def status_name(self, status_id) -> str | None:
        row = self._b.one("statuses", id=status_id)
        return row.get("name") if row else None

    def item_status_name(self, item_key: str) -> str | None:
        row = self.item(item_key)
        return self.status_name(row["status_id"]) if row else None

    def history(self, item_key: str) -> list[dict]:
        row = self.item(item_key)
        if not row:
            return []
        return self._b.rows("history_entries", item_id=row["id"])

    def history_count(self, item_key: str) -> int:
        row = self.item(item_key)
        return 0 if not row else self._b.count("history_entries", item_id=row["id"])

    def rule_executions(self) -> list[dict]:
        return self._b.rows("rule_executions")

    def rule_execution_count(self) -> int:
        return self._b.count("rule_executions")

    def page_view_count(self) -> int:
        return self._b.count("page_views")

    def user(self, email: str) -> dict | None:
        return self._b.one("users", email=email)

    def project(self, key: str) -> dict | None:
        return self._b.one("projects", key=key)


@pytest.fixture(scope="session")
def db() -> WorkStore:
    return WorkStore(make_backend())


@pytest.fixture(scope="session")
def inbox():
    """The mail inbox the email slot declares."""
    return make_inbox()


def create_item(api, project: str, summary: str) -> str:
    """Create a probe item and return its item_key. Self-seeding per J.5."""
    response = api.post(API_ITEMS, json={"project": project, "summary": summary,
                                         "item_type": "task"})
    assert response.status_code in OK, (
        f"POST {API_ITEMS} for {project} returned {response.status_code}: "
        f"{response.text[:400]}")
    key = response.json().get("item_key")
    assert key, f"created item carries no item_key: {response.text[:400]}"
    return key


def transition(api, item_key: str, to_status: str):
    return api.post(f"{API_ITEMS}/{item_key}/transition",
                    json={"to_status": to_status})


def advance_to_ready(api, item_key: str) -> None:
    """Walk a fresh item from its first status up to Ready for review."""
    for target in (STATUS_IN_PROGRESS, STATUS_READY):
        response = transition(api, item_key, target)
        assert response.status_code in OK, (
            f"transition of {item_key} to {target!r} returned "
            f"{response.status_code}: {response.text[:400]}")


def wait_for_message(inbox, to: str, subject_contains: str,
                     deadline_seconds: float = EMAIL_DEADLINE_SECONDS):
    """Poll to a monotonic deadline for an async side effect (reference/J J.5)."""
    deadline = time.monotonic() + deadline_seconds
    found = None
    while time.monotonic() < deadline:
        found = inbox.find(to, subject_contains)
        if found is not None:
            return found
        settle(1.0)
    return None


def graduated_total(user_count: int, bands) -> int:
    """The graduated-band total the pricing route must reproduce."""
    total = 0
    previous = 0
    for ceiling, rate in bands:
        top = user_count if ceiling is None else min(user_count, ceiling)
        if top > previous:
            total += (top - previous) * rate
            previous = top
        if ceiling is not None and user_count <= ceiling:
            break
    return total
