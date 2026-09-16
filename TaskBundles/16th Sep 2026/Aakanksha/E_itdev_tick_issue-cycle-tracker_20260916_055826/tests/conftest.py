"""Task fixtures for deku/issue-cycle-tracker.

Two rules from the pytest contract govern this file:

1. Implementation agnostic. Nothing here assumes the agent's framework, file
   layout, ORM or module names. The only things assumed are the App Contract
   (the app answers at APP_PUBLIC_URL, REST under /api, POST /api/auth/login
   returns access_token) and whatever instruction.md pinned explicitly: the
   endpoint paths and bodies, the seeded team and members, the cycle names, the
   workflow states, the team key and the email subject prefixes.

2. Provider agnostic. The domain helpers below are composed from the generic
   Backend and Inbox primitives in capabilities.py, never a provider SDK.
"""

from __future__ import annotations

import time

import pytest
from appclient import client, login
from capabilities import Backend, Inbox, make_backend, make_inbox

PASSWORD = "deku-demo-pw-2026"

ADMIN_EMAIL = "admin@example.com"
LEAD_EMAIL = "lead@example.com"
MEMBER_EMAIL = "member@example.com"
MEMBER2_EMAIL = "member2@example.com"

TEAM_NAME = "Orbit"
TEAM_KEY = "ORB"
ACTIVE_CYCLE = "Cycle 24"
CLOSED_CYCLE = "Cycle 23"
OTHER_TEAM_ISSUE_KEY = "OTR-1"

ASSIGN_SUBJECT = "Assigned to you: "
UPDATE_SUBJECT = "Issue updated: "

STATE_BACKLOG = "backlog"
STATE_UNSTARTED = "unstarted"
STATE_IN_PROGRESS = "in_progress"
STATE_DONE = "done"
STATE_CANCELLED = "cancelled"

ACCEPTED = (200, 201)


def settle(seconds: float = 0.4) -> None:
    """The only sanctioned sleep. Spaces a bounded poll for a side effect that
    settles a moment after the HTTP call returns (mail delivered over SMTP)."""
    time.sleep(seconds)


def find_email_eventually(inbox: Inbox, to: str, subject_contains: str):
    """Poll the inbox to a bounded deadline for a message that has arrived."""
    deadline = time.monotonic() + 8.0
    message = inbox.find(to=to, subject_contains=subject_contains)
    while message is None and time.monotonic() < deadline:
        settle()
        message = inbox.find(to=to, subject_contains=subject_contains)
    return message


def all_issues(payload) -> list[dict]:
    """Flatten whatever board or list shape the app returns into a list of issues."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if isinstance(payload.get("issues"), list):
            return payload["issues"]
        columns = payload.get("columns")
        if isinstance(columns, dict):
            out: list[dict] = []
            for group in columns.values():
                if isinstance(group, list):
                    out.extend(group)
            return out
        if isinstance(columns, list):
            out = []
            for group in columns:
                items = group.get("issues") if isinstance(group, dict) else None
                if isinstance(items, list):
                    out.extend(items)
            return out
    return []


def board_issues(c) -> list[dict]:
    response = c.get("/board")
    assert response.status_code == 200, "a member must be able to read the board"
    return all_issues(response.json())


def inbox_issues(c) -> list[dict]:
    response = c.get("/inbox")
    assert response.status_code == 200, "a lead must be able to read the inbox"
    return response.json()


def cycles(c) -> list[dict]:
    response = c.get("/cycles")
    assert response.status_code == 200, "a member must be able to list cycles"
    return response.json()


def active_cycle(c) -> dict | None:
    for cycle in cycles(c):
        if cycle.get("status") == "active" or cycle.get("name") == ACTIVE_CYCLE:
            return cycle
    return None


def closed_cycle(c) -> dict | None:
    for cycle in cycles(c):
        if cycle.get("status") == "closed" or cycle.get("name") == CLOSED_CYCLE:
            return cycle
    return None


def create_issue(c, title: str, label: str = "bug", priority: str = "med",
                 estimate: int = 1, client_request_id: str | None = None) -> dict:
    body = {"title": title, "label": label, "priority": priority, "estimate": estimate}
    if client_request_id is not None:
        body["client_request_id"] = client_request_id
    response = c.post("/issues", json=body)
    assert response.status_code in ACCEPTED, (
        f"filing an issue must succeed, got {response.status_code}: {response.text[:300]}")
    return response.json()


def get_issue(c, key: str):
    return c.get(f"/issues/{key}")


def patch_issue(c, key: str, **fields):
    return c.patch(f"/issues/{key}", json=fields)


def issue_by_title(c, title: str) -> dict | None:
    for issue in board_issues(c):
        if issue.get("title") == title:
            return issue
    return None


def an_inbox_issue(c) -> dict:
    rows = inbox_issues(c)
    assert rows, "the seed must leave at least one issue in the inbox to triage"
    return rows[0]


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def admin_client():
    with client(login(ADMIN_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture(scope="session")
def lead_client():
    with client(login(LEAD_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture(scope="session")
def member_client():
    with client(login(MEMBER_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture(scope="session")
def member2_client():
    with client(login(MEMBER2_EMAIL, PASSWORD)) as c:
        yield c


class TrackerStore:
    """Domain queries for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def team(self, name: str) -> dict | None:
        return self._b.one("teams", name=name)

    def member(self, email: str) -> dict | None:
        return self._b.one("members", email=email)

    def members_in(self, team_id) -> list[dict]:
        return self._b.rows("members", team_id=team_id)

    def cycle(self, name: str) -> dict | None:
        return self._b.one("cycles", name=name)

    def active_cycles(self, team_id) -> list[dict]:
        return self._b.rows("cycles", team_id=team_id, status="active")

    def issue(self, key: str) -> dict | None:
        return self._b.one("issues", key=key)

    def activity_count(self, issue_id) -> int:
        return self._b.count("activity", issue_id=issue_id)

    def issue_count(self, **where) -> int:
        return self._b.count("issues", **where)


@pytest.fixture(scope="session")
def db() -> TrackerStore:
    return TrackerStore(make_backend())


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    return make_inbox()
