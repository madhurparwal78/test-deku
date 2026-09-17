"""Task fixtures for deku/internal-tools-builder-vb.

Implementation-agnostic (reference/J J.2): assume only the App Contract, the
literals pinned in instruction.md, and the two capability fixtures the declared
`db` and `email` slots earn. Observations are made over the JSON API, over the
served markup of the public routes, over the rows in postgres and over the
messages in the mail sink. Nothing here imports a vendor SDK, reads the agent's
source, or probes for a feature at run time. No test function lives in this file.
"""

from __future__ import annotations

import os
import time
from concurrent.futures import ThreadPoolExecutor

import httpx
import pytest
from appclient import api_base, app_url, client, login
from capabilities import Backend, Inbox, make_backend, make_inbox

TIMEOUT = 30.0
SETTLE_SECONDS = 2.0
POLL_ATTEMPTS = 15


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give a side effect time to land before asserting on it."""
    time.sleep(seconds)


def unique(prefix: str) -> str:
    """A per-run identifier, so a re-run never collides with its predecessor."""
    return f"{prefix}-{os.urandom(6).hex()}"


def probe_email(prefix: str = "probe") -> str:
    return f"{unique(prefix)}@example.com"


PASSWORD = "deku-demo-pw-2026"

OWNER_EMAIL = "owner@example.com"
BUILDER_EMAIL = "builder@example.com"
BUILDER2_EMAIL = "builder2@example.com"
OPERATOR_EMAIL = "operator@example.com"
OPERATOR2_EMAIL = "operator2@example.com"
AUDITOR_EMAIL = "auditor@example.com"

SEEDED_ACCOUNTS = (OWNER_EMAIL, BUILDER_EMAIL, BUILDER2_EMAIL,
                   OPERATOR_EMAIL, OPERATOR2_EMAIL, AUDITOR_EMAIL)

ROLE_OWNER = "owner"
ROLE_BUILDER = "builder"
ROLE_OPERATOR = "operator"
ROLE_AUDITOR = "auditor"

WORKSPACE = "Northgate Operations"

ENV_STAGING = "staging"
ENV_PRODUCTION = "production"
ENVIRONMENTS = (ENV_STAGING, ENV_PRODUCTION)

RESOURCE_OK = "Orders Warehouse"
RESOURCE_STALE = "Ledger Archive"
RESOURCE_KIND = "postgres"
RESOURCE_KINDS = ("postgres", "http_api", "object_store", "queue",
                  "warehouse", "model_provider")

APP_PUBLISHED = "Order Desk"
APP_DRAFT = "Refund Desk"
SLUG_PUBLISHED = "order-desk"
SLUG_DRAFT = "refund-desk"

QUERY_READ = "orders_recent"
QUERY_WRITE = "order_mark_delayed"

GROUP_BUILDERS = "Platform Builders"
GROUP_OPERATIONS = "Operations"
GROUP_SUPPORT = "Support Desk"
POLICY_MASK = "Support masking"
MASKED_COLUMN = "customer_name"

ORDER_COLUMNS = ("order_ref", "customer_name", "amount_minor", "status",
                 "placed_at")
ORDER_STATUSES = ("open", "delayed", "settled")
SEEDED_ORDER_ROWS = 50000

ORDER_ONE = "NG-1001"
ORDER_TWO = "NG-1002"
ORDER_THREE = "NG-1003"
ORDER_ONE_AMOUNT = 124500
ORDER_TWO_AMOUNT = 98000
ORDER_THREE_AMOUNT = 1000

RUN_STATES = ("ok", "denied", "invalid", "unreachable", "timeout",
              "quota_exceeded", "failed")
PROBE_STATES = ("reachable", "unreachable")
ACTIONS = ("read", "write", "execute", "publish", "promote", "administer",
           "export")
EFFECTS = ("allow", "deny")
APPROVAL_DECISIONS = ("pending", "granted", "refused", "lapsed")
DEMO_STATES = ("sent", "invalid", "spam", "failed")
SUBSCRIPTION_STATES = ("sent", "invalid", "already", "failed")
SEARCH_STATES = ("ok", "invalid", "failed")
OPERATION_KINDS = ("add", "remove", "move", "resize", "reparent",
                   "set-property", "bind", "unbind", "rename")

INVITE_SUBJECT_PREFIX = "Girder invitation: "
INVITE_SUBJECT = "Girder invitation: Northgate Operations"

OK_STATUS = (200, 201)
DENIED_STATUS = (401, 403)
REFUSED_STATUS = (400, 401, 403, 404, 409, 422)
CONFLICT_STATUS = (409, 412, 422)


def describe(response: httpx.Response, what: str) -> str:
    """Failure prose naming the anchor, the request, the status and the body."""
    return (f"{what}: {response.request.method} {response.request.url} "
            f"returned {response.status_code}, body {response.text[:400]!r}")


@pytest.fixture(scope="session")
def base_url() -> str:
    return app_url()


@pytest.fixture(scope="session")
def api() -> str:
    return api_base()


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    return make_inbox()


@pytest.fixture(scope="session")
def owner_token() -> str:
    return login(OWNER_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def builder_token() -> str:
    return login(BUILDER_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def builder2_token() -> str:
    return login(BUILDER2_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def operator_token() -> str:
    return login(OPERATOR_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def operator2_token() -> str:
    return login(OPERATOR2_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def auditor_token() -> str:
    return login(AUDITOR_EMAIL, PASSWORD)


@pytest.fixture()
def owner(owner_token: str):
    with client(owner_token) as c:
        yield c


@pytest.fixture()
def builder(builder_token: str):
    with client(builder_token) as c:
        yield c


@pytest.fixture()
def builder2(builder2_token: str):
    with client(builder2_token) as c:
        yield c


@pytest.fixture()
def operator(operator_token: str):
    with client(operator_token) as c:
        yield c


@pytest.fixture()
def operator2(operator2_token: str):
    with client(operator2_token) as c:
        yield c


@pytest.fixture()
def auditor(auditor_token: str):
    with client(auditor_token) as c:
        yield c


@pytest.fixture()
def anonymous():
    with client(None) as c:
        yield c


@pytest.fixture()
def web():
    """An unauthenticated client against the served routes, not the API."""
    with httpx.Client(base_url=app_url(), timeout=TIMEOUT,
                      follow_redirects=True) as c:
        yield c


def json_of(response: httpx.Response, what: str):
    assert response.status_code in OK_STATUS, describe(response, what)
    return response.json()


def find_named(rows, name: str):
    """The row whose `name` field equals `name`, or None."""
    for row in rows:
        if isinstance(row, dict) and row.get("name") == name:
            return row
    return None


def app_id_for(session: httpx.Client, name: str) -> str:
    payload = json_of(session.get("/apps"), f"the app catalog listing {name!r}")
    from _shapes import items
    row = find_named(items(payload), name)
    assert row is not None, (
        f"the app catalog names no app {name!r}; seeded apps are "
        f"{APP_PUBLISHED!r} and {APP_DRAFT!r}. Listing was {payload!r}"[:500])
    return str(row.get("id") or row.get("slug"))


def resource_id_for(session: httpx.Client, name: str) -> str:
    payload = json_of(session.get("/resources"),
                      f"the resource catalog listing {name!r}")
    from _shapes import items
    row = find_named(items(payload), name)
    assert row is not None, (
        f"the resource catalog names no resource {name!r}; seeded resources are "
        f"{RESOURCE_OK!r} and {RESOURCE_STALE!r}. Listing was {payload!r}"[:500])
    return str(row.get("id"))


def run_query(session: httpx.Client, app: str, query: str, environment: str,
              parameters=None, idempotency_key: str | None = None):
    body = {"app_version": app, "query": query, "environment": environment,
            "parameters": parameters or {}}
    if idempotency_key is not None:
        body["idempotency_key"] = idempotency_key
    return session.post("/query-runs", json=body)


def state_of(response: httpx.Response, what: str) -> str:
    payload = response.json() if response.content else {}
    assert isinstance(payload, dict), describe(response, what)
    state = payload.get("state")
    assert isinstance(state, str), (
        f"{what}: the answer carries no string `state`; body "
        f"{response.text[:400]!r}")
    return state


def poll_for(predicate, attempts: int = POLL_ATTEMPTS):
    """Bounded polling for an asynchronous side effect. Never an unbounded loop
    and never a retry that hides a failure: the last observation is returned and
    the caller asserts on it."""
    observed = None
    for _ in range(attempts):
        observed = predicate()
        if observed:
            return observed
        settle(1.0)
    return observed


def in_parallel(call, count: int = 2):
    """Fire `count` identical calls at once and return every response."""
    with ThreadPoolExecutor(max_workers=count) as pool:
        futures = [pool.submit(call) for _ in range(count)]
        return [f.result() for f in futures]
