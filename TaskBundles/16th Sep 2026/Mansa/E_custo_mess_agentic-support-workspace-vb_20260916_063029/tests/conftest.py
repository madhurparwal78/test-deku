from __future__ import annotations

import os
import time

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, Inbox, make_backend, make_inbox

SETTLE_SECONDS = 2.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    time.sleep(seconds)


ADMIN_EMAIL = "admin@example.com"
MANAGER_EMAIL = "manager@example.com"
TEAMMATE_EMAIL = "teammate@example.com"
TEAMMATE2_EMAIL = "teammate2@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"

WORKSPACE_NAME = "Northwind Trading"
WORKSPACE_SLUG = "northwind"
BILLING_TEAM = "Billing Support"
TECHNICAL_TEAM = "Technical Support"

BILLING_CONVERSATION = "Refund for duplicate charge"
TECHNICAL_CONVERSATION = "Cannot reset my password"
UNROUTED_CONVERSATION = "Invoice shows the wrong tax rate"

PUBLISHED_REFUND_ARTICLE = "Refunds and duplicate charges"
PUBLISHED_PASSWORD_ARTICLE = "Resetting your password"
DRAFT_TAX_ARTICLE = "Tax rates on invoices"
INTERNAL_ARTICLE = "Escalation runbook"

SLA_POLICY_NAME = "Standard support"
FIRST_RESPONSE_MINUTES = 60
RESOLUTION_MINUTES = 480

APPROVAL_CEILING_MINOR_UNITS = 5000
CURRENCY = "usd"

INVITATION_SUBJECT_PREFIX = "Support workspace invitation:"
HANDOVER_SUBJECT_PREFIX = "Handover needed:"

EMPTY_FIRST_RUN_COPY = "No conversations yet. Connect a channel to start receiving them."
EMPTY_FILTERED_COPY = "No conversations match these filters."
EMPTY_CLEARED_COPY = "You are all caught up."
HANDOVER_CUSTOMER_COPY = "Connecting you with a specialist who can help."
SUMMARY_CARD_TITLE = "Summary"
REASONING_TITLE = "Auto Agent's thoughts (Step 1)"

GAP_CONTENT_LABEL = "CONTENT GAP"
GAP_CUSTOMER_DATA_LABEL = "CUSTOMER DATA GAP"
GAP_ACTION_LABEL = "ACTION GAP"
GAP_BADGE_HIGH = "High"
GAP_BADGE_MEDIUM = "Medium"
GAP_BADGE_LOW = "Low"

READ_TOOL = "read_account"
WRITE_TOOL = "issue_credit"

VOLUME_CONVERSATIONS = 2000
VOLUME_PARTS = 50
VOLUME_TEAMMATES = 25

POLL_ATTEMPTS = 15
POLL_INTERVAL = 1.0


def poll(predicate, attempts: int = POLL_ATTEMPTS, interval: float = POLL_INTERVAL):
    """Bounded poll for an asynchronous side effect. Returns the first truthy value."""
    found = predicate()
    for _ in range(attempts):
        if found:
            return found
        settle(interval)
        found = predicate()
    return found


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def admin_token() -> str:
    return login(ADMIN_EMAIL, seeded_password("SEED_ADMIN_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def admin_client(admin_token: str):
    with client(admin_token) as c:
        yield c


@pytest.fixture(scope="session")
def manager_token() -> str:
    return login(MANAGER_EMAIL, seeded_password("SEED_MANAGER_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def manager_client(manager_token: str):
    with client(manager_token) as c:
        yield c


@pytest.fixture(scope="session")
def teammate_token() -> str:
    return login(TEAMMATE_EMAIL, seeded_password("SEED_TEAMMATE_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def teammate_client(teammate_token: str):
    with client(teammate_token) as c:
        yield c


@pytest.fixture(scope="session")
def teammate2_token() -> str:
    return login(TEAMMATE2_EMAIL, seeded_password("SEED_TEAMMATE2_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def teammate2_client(teammate2_token: str):
    with client(teammate2_token) as c:
        yield c


class WorkspaceStore:
    """Domain queries for this task, composed from the generic capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def workspace(self) -> dict | None:
        return self._b.one("workspace", slug=WORKSPACE_SLUG)

    def team_by_name(self, name: str) -> dict | None:
        return self._b.one("team", name=name)

    def teams(self) -> list[dict]:
        return self._b.rows("team")

    def membership_count(self) -> int:
        return self._b.count("membership")

    def memberships_with_status(self, status: str) -> list[dict]:
        return self._b.rows("membership", status=status)

    def invitations_for(self, email: str) -> list[dict]:
        return self._b.rows("invitation", email=email)

    def conversation_by_subject(self, subject: str) -> dict | None:
        return self._b.one("conversation", subject=subject)

    def conversations(self) -> list[dict]:
        return self._b.rows("conversation")

    def parts_of(self, conversation_id) -> list[dict]:
        return self._b.rows("conversation_part", conversation_id=conversation_id)

    def parts_of_kind(self, conversation_id, kind: str) -> list[dict]:
        return self._b.rows("conversation_part", conversation_id=conversation_id, kind=kind)

    def count_parts_of_kind(self, conversation_id, kind: str) -> int:
        return self._b.count("conversation_part", conversation_id=conversation_id, kind=kind)

    def article_by_title(self, title: str) -> dict | None:
        return self._b.one("article", title=title)

    def article_versions(self, article_id) -> list[dict]:
        return self._b.rows("article_version", article_id=article_id)

    def collection_by_name(self, name: str) -> dict | None:
        return self._b.one("collection", name=name)

    def agent_runs_for(self, conversation_id) -> list[dict]:
        return self._b.rows("agent_run", conversation_id=conversation_id)

    def agent_steps_for(self, run_id) -> list[dict]:
        return self._b.rows("agent_step", agent_run_id=run_id)

    def sla_policy(self, name: str) -> dict | None:
        return self._b.one("sla_policy", name=name)

    def audit_entries_for_action(self, action: str) -> list[dict]:
        return self._b.rows("audit_entry", action=action)

    def count_audit_entries(self) -> int:
        return self._b.count("audit_entry")

    def gaps(self) -> list[dict]:
        return self._b.rows("knowledge_gap")


@pytest.fixture(scope="session")
def db() -> WorkspaceStore:
    return WorkspaceStore(make_backend())


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    """The mail server inbox, inspected out of band. Never call smtplib here."""
    return make_inbox()


@pytest.fixture
def unique_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


@pytest.fixture(scope="session")
def billing_conversation(db: WorkspaceStore) -> dict:
    row = db.conversation_by_subject(BILLING_CONVERSATION)
    assert row is not None, (
        f"seeded conversation {BILLING_CONVERSATION!r} is missing from the store"
    )
    return row


@pytest.fixture(scope="session")
def technical_conversation(db: WorkspaceStore) -> dict:
    row = db.conversation_by_subject(TECHNICAL_CONVERSATION)
    assert row is not None, (
        f"seeded conversation {TECHNICAL_CONVERSATION!r} is missing from the store"
    )
    return row


@pytest.fixture(scope="session")
def unrouted_conversation(db: WorkspaceStore) -> dict:
    row = db.conversation_by_subject(UNROUTED_CONVERSATION)
    assert row is not None, (
        f"seeded conversation {UNROUTED_CONVERSATION!r} is missing from the store"
    )
    return row


def invite(http, email: str, role: str = "teammate", team_id=None) -> "object":
    body = {"email": email, "role": role}
    if team_id is not None:
        body["team_id"] = team_id
    return http.post("/teammates/invitations", json=body)


def open_conversation(http, conversation_id) -> "object":
    return http.get(f"/conversations/{conversation_id}")


def send_part(http, conversation_id, kind: str, body: str, client_key: str) -> "object":
    return http.post(
        f"/conversations/{conversation_id}/parts",
        json={"kind": kind, "body": body, "client_key": client_key},
    )


def run_agent(http, conversation_id) -> "object":
    return http.post(f"/conversations/{conversation_id}/agent-run", json={})


def fresh_key() -> str:
    return f"probe-{os.urandom(8).hex()}"
