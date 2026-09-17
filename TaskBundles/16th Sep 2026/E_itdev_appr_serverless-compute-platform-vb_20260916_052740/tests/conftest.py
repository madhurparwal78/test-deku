"""Task fixtures for deku/serverless-compute-platform-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout
or module names. The only assumptions are the App Contract and what
instruction.md pinned literally, which is the HTTP surface table, the seeded
principals, the closed vocabularies and the seeded workspace slug.

Provider agnostic: the domain helpers are composed from the generic Backend
primitives in capabilities.py, never from a provider SDK.
"""

from __future__ import annotations

import os
import time

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, make_backend

OWNER_EMAIL = "owner@example.com"
OPERATOR_EMAIL = "operator@example.com"
OPERATOR2_EMAIL = "operator2@example.com"
DEVELOPER_EMAIL = "developer@example.com"
DEVELOPER2_EMAIL = "developer2@example.com"
READONLY_EMAIL = "readonly@example.com"

SEED_PASSWORD = "deku-demo-pw-2026"

WORKSPACE_SLUG = "vireo-research"
PRODUCTION_ENV = "production"
DEVELOPMENT_ENV = "development"

APP_NOVA = "Nova Inference"
APP_ATLAS = "Atlas Batch"

CONTAINER_EXIT_REASONS = (
    "completed",
    "idle-scaledown",
    "deploy-superseded",
    "customer-terminated",
    "customer-code-error",
    "out-of-memory",
    "timeout",
    "preempted",
    "worker-lost",
    "platform-error",
    "quota-exceeded",
    "policy-denied",
)

PLATFORM_EXIT_REASONS = ("worker-lost", "platform-error")

REQUEST_STATES = (
    "draft",
    "submitted",
    "in-review",
    "approved",
    "rejected",
    "withdrawn",
    "expired",
    "applied",
    "failed-to-apply",
)

DENIED = (401, 403)
REFUSED = (400, 422)


def settle(seconds: float = 1.0) -> None:
    """The one sanctioned pause, for a side effect the app writes asynchronously."""
    time.sleep(seconds)


def prod(path: str) -> str:
    """A production console path under the seeded workspace."""
    return f"/w/{WORKSPACE_SLUG}/{PRODUCTION_ENV}{path}"


def dev(path: str) -> str:
    """A development console path under the seeded workspace."""
    return f"/w/{WORKSPACE_SLUG}/{DEVELOPMENT_ENV}{path}"


def body(response) -> str:
    """A bounded excerpt of a response body, for an assertion message."""
    return response.text[:400]


def _authed(email: str):
    return client(login(email, seeded_password("SEED_PASSWORD", SEED_PASSWORD)))


@pytest.fixture
def anon_client():
    with client() as c:
        yield c


@pytest.fixture
def owner_client():
    with _authed(OWNER_EMAIL) as c:
        yield c


@pytest.fixture
def operator_client():
    with _authed(OPERATOR_EMAIL) as c:
        yield c


@pytest.fixture
def operator2_client():
    with _authed(OPERATOR2_EMAIL) as c:
        yield c


@pytest.fixture
def developer_client():
    with _authed(DEVELOPER_EMAIL) as c:
        yield c


@pytest.fixture
def developer2_client():
    with _authed(DEVELOPER2_EMAIL) as c:
        yield c


@pytest.fixture
def readonly_client():
    with _authed(READONLY_EMAIL) as c:
        yield c


@pytest.fixture
def backend() -> Backend:
    return make_backend()


@pytest.fixture
def app_base_url() -> str:
    return os.environ["APP_PUBLIC_URL"].rstrip("/")


def items(payload):
    """The rows out of a list response, whatever envelope the app chose."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "data", "results", "rows", "records"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def find_app(rows, name: str):
    for row in rows:
        if str(row.get("name", "")).strip() == name:
            return row
    return None


def field(row, *names, default=None):
    """The first present key out of several spellings the app may have chosen."""
    for name in names:
        if isinstance(row, dict) and name in row and row[name] is not None:
            return row[name]
    return default


def file_a_request(http_client, app_name: str, version, reason: str):
    """File a promotion request against the production environment."""
    return http_client.post(
        prod("/requests"),
        json={
            "app": app_name,
            "requested_version": version,
            "target_environment": PRODUCTION_ENV,
            "reason": reason,
        },
    )


def request_row(http_client, request_id):
    return http_client.get(prod(f"/requests/{request_id}"))


def decide(http_client, request_id, decision: str, reason: str):
    return http_client.post(
        prod(f"/requests/{request_id}/decision"),
        json={"decision": decision, "reason": reason},
    )


def apply_request(http_client, request_id):
    return http_client.post(prod(f"/requests/{request_id}/apply"), json={})


def open_request(http_client, app_name: str, reason: str):
    """File a request against the newest non-live version of an app.

    Returns the parsed request id. The caller asserts on the response itself
    where the filing is the thing under observation.
    """
    listing = http_client.get(prod("/apps"))
    assert listing.status_code == 200, (
        f"GET {prod('/apps')} returned {listing.status_code}: {body(listing)}"
    )
    row = find_app(items(listing.json()), app_name)
    assert row is not None, (
        f"seeded app {app_name!r} is absent from {prod('/apps')}: {body(listing)}"
    )
    detail = http_client.get(prod(f"/apps/{field(row, 'id', 'slug', 'name')}"))
    assert detail.status_code == 200, (
        f"GET the app detail for {app_name!r} returned {detail.status_code}: "
        f"{body(detail)}"
    )
    versions = items(field(detail.json(), "versions", default=[]))
    assert versions, (
        f"the seeded app {app_name!r} carries no versions: {body(detail)}"
    )
    candidate = None
    for version in versions:
        if str(field(version, "status", "state", default="")).lower() != "live":
            candidate = version
    assert candidate is not None, (
        f"the seeded app {app_name!r} carries no non-live version to promote: "
        f"{body(detail)}"
    )
    filed = file_a_request(
        http_client, app_name, field(candidate, "ordinal", "id", "version"), reason
    )
    assert filed.status_code in (200, 201), (
        f"POST {prod('/requests')} for {app_name!r} returned {filed.status_code}: "
        f"{body(filed)}"
    )
    request_id = field(filed.json(), "id", "request_id")
    assert request_id is not None, (
        f"the filed request carries no id: {body(filed)}"
    )
    return request_id
