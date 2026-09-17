"""Task fixtures for deku/financial-data-network.

Implementation agnostic: nothing here assumes the agent's framework, file layout,
ORM or module names. The only assumptions are the App Contract (the app answers at
APP_PUBLIC_URL, REST under /api, POST /api/auth/login returns access_token) and the
literals instruction.md pinned.

Provider agnostic: domain helpers are composed from the generic Backend primitives
in capabilities.py, never from a provider SDK.
"""

from __future__ import annotations

import hashlib
import os
import uuid

import pytest
from appclient import client, login, seeded_password
from capabilities import make_backend

PASSWORD = "deku-demo-pw-2026"

DEVELOPER_EMAIL = "developer@example.com"
DEVELOPER2_EMAIL = "developer2@example.com"
ADMINISTRATOR_EMAIL = "administrator@example.com"
COMPLIANCE_EMAIL = "compliance@example.com"
ANALYST_EMAIL = "analyst@example.com"
ADMINISTRATOR2_EMAIL = "administrator2@example.com"

VANTOR = "Vantor"
WRENWOOD = "Wrenwood"

PAYOUTS_SLUG = "vantor-payouts"
RISK_SLUG = "vantor-risk-signals"
LEDGER_SLUG = "vantor-ledger-sync"
ONBOARDING_SLUG = "wrenwood-onboarding"

SUBMITTED_REQUEST = "AR-1001"
IN_REVIEW_REQUEST = "AR-1002"
APPROVED_REQUEST = "AR-1003"
SELF_FILED_REQUEST = "AR-1004"
OTHER_ORG_REQUEST = "AR-2001"

HEALTHY_CONNECTION = "con_7hq2"
REAUTH_CONNECTION = "con_9km4"
UNAVAILABLE_CONNECTION = "con_3wp8"
REVOKED_CONNECTION = "con_5tz1"

OPEN_DATA_REQUEST = "dsr_4410"
CLOSED_DATA_REQUEST = "dsr_4411"

SEEDED_WEBHOOK = "https://hooks.vantor.example/ravel"

REQUEST_STATES = (
    "draft", "submitted", "in_review", "returned", "approved",
    "denied", "live", "revoked", "suspended",
)
CONNECTION_STATES = (
    "healthy", "degraded", "requires_reauthentication", "institution_unavailable",
    "revoked_by_consumer", "revoked_by_customer", "expired", "suspended",
)
ANSWER_KEYS = (
    "intended_use", "consumer_disclosure", "retention_period_days", "sub_processors",
    "security_contact", "expected_monthly_volume", "regulatory_basis",
)
ROLES = ("developer", "administrator", "compliance_approver", "analyst")
ENVIRONMENTS = ("sandbox", "development", "production")
PRODUCTS = ("auth", "balance", "identity", "transactions", "signal", "transfer")

GENESIS_HASH = "0" * 64
DEVELOPMENT_CONNECTION_CAP = 25
PRODUCTION_SECRET_DAYS = 365
LIVE_CREDENTIALS_PER_ENVIRONMENT = 2
WEBHOOK_ENDPOINTS_PER_ENVIRONMENT = 5
BULK_REAUTHENTICATION_LIMIT = 100
DATA_REQUEST_DUE_DAYS = 30
COMMITTED_REQUESTS = 50000
DENIAL_REASON_MAX = 280

FORBIDDEN_CONSUMER_FIELDS = (
    "balance", "available_balance", "current_balance", "transaction", "transactions",
    "account_number", "routing_number", "identity_record", "holdings",
)


def answers():
    return {key: "recorded for grading" for key in ANSWER_KEYS}


def audit_hash(previous_hash, sequence, actor_email, action,
               resource_type, resource_id, occurred_at):
    joined = "|".join([
        str(previous_hash), str(sequence), str(actor_email), str(action),
        str(resource_type), str(resource_id), str(occurred_at),
    ])
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def unique_suffix():
    return uuid.uuid4().hex[:8]


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


def _authed(email):
    token = login(email, seeded_password("SEED_PASSWORD", PASSWORD))
    return client(token)


@pytest.fixture(scope="session")
def developer_client():
    with _authed(DEVELOPER_EMAIL) as c:
        yield c


@pytest.fixture(scope="session")
def developer2_client():
    with _authed(DEVELOPER2_EMAIL) as c:
        yield c


@pytest.fixture(scope="session")
def administrator_client():
    with _authed(ADMINISTRATOR_EMAIL) as c:
        yield c


@pytest.fixture(scope="session")
def compliance_client():
    with _authed(COMPLIANCE_EMAIL) as c:
        yield c


@pytest.fixture(scope="session")
def analyst_client():
    with _authed(ANALYST_EMAIL) as c:
        yield c


@pytest.fixture(scope="session")
def other_org_client():
    with _authed(ADMINISTRATOR2_EMAIL) as c:
        yield c


@pytest.fixture(scope="session")
def backend():
    return make_backend()


@pytest.fixture()
def fresh_request(developer_client):
    created = developer_client.post("/access-requests", json={
        "application": PAYOUTS_SLUG,
        "environment": "production",
        "product_key": "identity",
        "answers": answers(),
    })
    assert created.status_code in (200, 201), (
        f"creating a draft access request returned {created.status_code}: "
        f"{created.text[:400]}"
    )
    body = created.json()
    request_id = body.get("id") or body.get("request_id")
    assert request_id, f"created access request carries no id: {created.text[:400]}"
    submitted = developer_client.post(f"/access-requests/{request_id}/submit")
    assert submitted.status_code in (200, 201, 204), (
        f"submitting {request_id} returned {submitted.status_code}: "
        f"{submitted.text[:400]}"
    )
    return request_id


def state_of(http_client, request_id):
    response = http_client.get(f"/access-requests/{request_id}")
    assert response.status_code == 200, (
        f"reading {request_id} returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    return body.get("state"), body
