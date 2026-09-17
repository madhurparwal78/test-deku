"""Fixtures, pinned literals and domain helpers for Perpetua Cloud.

No test functions live here. Every literal below is pinned in instruction.md and
recorded in the bundle's literals ledger, so a grader never asserts a value the
brief did not state.
"""

from __future__ import annotations

import os
import time
import uuid

import httpx
import pytest

import appclient
import capabilities

CORPUS_PASSWORD = "deku-demo-pw-2026"

DEVELOPER_EMAIL = "developer@example.com"
DEVELOPER2_EMAIL = "developer2@example.com"
NAMESPACE_ADMIN_EMAIL = "namespace-admin@example.com"
NAMESPACE_ADMIN2_EMAIL = "namespace-admin2@example.com"
OWNER_EMAIL = "owner@example.com"

ROLE_DEVELOPER = "developer"
ROLE_NAMESPACE_ADMIN = "namespace-admin"
ROLE_OWNER = "owner"

FIRST_ORG = "Northwind Trading"
FIRST_ORG_SLUG = "northwind"
SECOND_ORG = "Forgelab"
SECOND_ORG_SLUG = "forgelab"

GRADED_NAMESPACE = "payments-prod"
SECOND_NAMESPACE = "orders-prod"
FOREIGN_NAMESPACE = "ledger-prod"
MISSING_NAMESPACE = "namespace-that-does-not-exist"

GRADED_REGION = "eu-central-1"
SECOND_REGION = "us-east-1"

GRADED_RETENTION_DAYS = 30
PROPOSED_RETENTION_DAYS = 7
CAPACITY_ON_DEMAND = "on-demand"

REVIEWABLE_KIND = "reduce_retention"

STATE_PENDING = "pending"
STATE_APPROVED = "approved"
STATE_APPLIED = "applied"
STATE_REJECTED = "rejected"
STATE_FAILED = "failed"
STATE_EXPIRED = "expired"
STATE_WITHDRAWN = "withdrawn"
REQUEST_STATES = (
    "draft", "pending", "approved", "applying", "applied",
    "failed", "rejected", "expired", "withdrawn",
)

STATE_RUNNING = "running"
NAMESPACE_STATE_READY = "ready"

FAILED_WORKFLOW_ID = "subscription-9f21c4d0"
FAILED_RUN_ID = "01J7Y6M2R8"
FOREIGN_WORKFLOW_ID = "ledger-close-11f0"
FOREIGN_RUN_ID = "01J7Y6M5U3"
GRADED_TASK_QUEUE = "billing-tq"

DENIED = (401, 403, 404)
REFUSED = (400, 401, 403, 404, 409, 422)
CREATED = (200, 201)
OK = (200,)

SETTLE_SECONDS = 0.25
POLL_DEADLINE_SECONDS = 30.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The only sanctioned pause in the suite (reference/J J.5)."""
    time.sleep(seconds)


def probe_suffix() -> str:
    """A per-run unique suffix, so a rerun never collides with its own rows."""
    return uuid.uuid4().hex[:10]


def org_base(slug: str) -> str:
    return f"/organisations/{slug}"


def namespace_path(slug: str, namespace: str) -> str:
    return f"{org_base(slug)}/namespaces/{namespace}"


def change_requests_path(slug: str) -> str:
    return f"{org_base(slug)}/change-requests"


def poll_until(predicate, deadline: float = POLL_DEADLINE_SECONDS):
    """Poll to a deadline rather than sleeping once and hoping."""
    waited = 0.0
    last = None
    while waited < deadline:
        last = predicate()
        if last:
            return last
        settle()
        waited += SETTLE_SECONDS
    return last


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture()
def anonymous():
    with appclient.client() as session:
        yield session


def _session_for(email: str):
    token = appclient.login(email, CORPUS_PASSWORD)
    return appclient.client(token)


@pytest.fixture()
def developer():
    with _session_for(DEVELOPER_EMAIL) as session:
        yield session


@pytest.fixture()
def developer2():
    with _session_for(DEVELOPER2_EMAIL) as session:
        yield session


@pytest.fixture()
def namespace_admin():
    with _session_for(NAMESPACE_ADMIN_EMAIL) as session:
        yield session


@pytest.fixture()
def namespace_admin2():
    with _session_for(NAMESPACE_ADMIN2_EMAIL) as session:
        yield session


@pytest.fixture()
def owner():
    with _session_for(OWNER_EMAIL) as session:
        yield session


@pytest.fixture()
def public():
    with httpx.Client(base_url=appclient.app_url(), timeout=appclient.TIMEOUT) as session:
        yield session


def file_change_request(session, slug: str = FIRST_ORG_SLUG,
                        namespace: str = GRADED_NAMESPACE,
                        retention: int = PROPOSED_RETENTION_DAYS) -> dict:
    """File a retention reduction and return the created request body."""
    response = session.post(
        change_requests_path(slug),
        json={
            "kind": REVIEWABLE_KIND,
            "subject_ref": namespace,
            "proposed": {"retention_days": retention},
            "reason": f"probe-{probe_suffix()}",
        },
    )
    assert response.status_code in CREATED, (
        f"filing a {REVIEWABLE_KIND} request returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    return response.json()


def request_id_of(body: dict) -> str:
    for key in ("id", "request_id", "change_request_id"):
        value = body.get(key)
        if value:
            return str(value)
    raise AssertionError(f"filed change request carries no identifier: {body}")


def read_request(session, request_id: str, slug: str = FIRST_ORG_SLUG):
    return session.get(f"{change_requests_path(slug)}/{request_id}")


def state_of(body: dict) -> str:
    for key in ("state", "status"):
        value = body.get(key)
        if isinstance(value, str):
            return value
    raise AssertionError(f"change request carries no state field: {body}")


def approve(session, request_id: str, slug: str = FIRST_ORG_SLUG):
    return session.post(
        f"{change_requests_path(slug)}/{request_id}/approve",
        json={"reason": f"approved-{probe_suffix()}"},
    )


def apply_request(session, request_id: str, slug: str = FIRST_ORG_SLUG,
                  request_key: str | None = None):
    return session.post(
        f"{change_requests_path(slug)}/{request_id}/apply",
        json={"request_id": request_key or f"apply-{probe_suffix()}"},
    )


def read_namespace(session, namespace: str = GRADED_NAMESPACE,
                   slug: str = FIRST_ORG_SLUG):
    return session.get(namespace_path(slug, namespace))


def retention_of(body: dict) -> int:
    value = body.get("retention_days")
    assert value is not None, f"namespace body carries no retention_days: {body}"
    return int(value)


def audit_rows(backend_conn, **where):
    return backend_conn.query(
        "SELECT * FROM audit_entry ORDER BY occurred_at, id"
    ) if not where else backend_conn.rows("audit_entry", **where)


def audit_count(backend_conn, **where) -> int:
    return backend_conn.count("audit_entry", **where)


def namespace_count(backend_conn, **where) -> int:
    return backend_conn.count("namespace", **where)


def change_request_count(backend_conn, **where) -> int:
    return backend_conn.count("change_request", **where)


def approval_count(backend_conn, **where) -> int:
    return backend_conn.count("change_approval", **where)
