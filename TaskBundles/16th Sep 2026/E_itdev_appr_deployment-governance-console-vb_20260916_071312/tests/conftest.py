"""Fixtures, pinned literals and stores for the Meridian governance console.

Every value here is pinned in instruction.md. Nothing is discovered at run time:
a feature that is not in the brief has no fixture, and a fixture that invented a
value would grade the app against something the builder was never told.

Auth is Keycloak, but every substep authenticates through the app's own
POST /api/auth/login (see appclient.py). Talking through the app keeps the
assertions implementation-agnostic: reaching into Keycloak's admin API directly
would break the moment the identity slot moved to another provider.
"""

from __future__ import annotations

import os
import time
import uuid

import pytest

from appclient import client, login, seeded_password
from capabilities import make_backend

SEED_PASSWORD_VAR = "SEED_PASSWORD"
CORPUS_PASSWORD = "deku-demo-pw-2026"

DEVELOPER_EMAIL = "developer@example.com"
REVIEWER_EMAIL = "reviewer@example.com"
REVIEWER2_EMAIL = "reviewer2@example.com"
FINANCE_EMAIL = "finance@example.com"
VIEWER_EMAIL = "viewer@example.com"
FOREIGN_DEVELOPER_EMAIL = "developer2@example.com"

TEAM_SLUG = "northwind"
FOREIGN_TEAM_SLUG = "atlas"
PROJECT_SLUG = "checkout-web"
FOREIGN_PROJECT_SLUG = "atlas-site"

READY_COMMIT = "a1b2c3d"
LIVE_COMMIT = "9988776"
SUPERSEDED_COMMIT = "5544332"
PRODUCTION_ALIAS_HOST = "checkout-web.meridian.test"

POLICY_NAME = "Production two-eyes"
POLICY_VERSION = 1
REQUIRED_APPROVALS = 2
ELIGIBLE_GROUP = "release-reviewers"

DEPLOYMENT_STATES = ("QUEUED", "BUILDING", "READY", "ERROR", "CANCELED",
                     "PROMOTING", "LIVE", "SUPERSEDED")
REQUEST_STATES = ("OPEN", "APPROVED", "REJECTED", "EXPIRED", "CANCELED",
                  "EXECUTED", "FAILED")
FIREWALL_ACTIONS = ("allow", "deny", "challenge", "log", "rate-limit", "bypass")
SEEDED_FIREWALL_RULES = ("Log request starting with /",
                         "Challenge user agents that look like bots",
                         "Deny traffic from Germany")
SPEND_CAP_ACTIONS = ("notify", "restrict", "pause")
PUBLIC_ROUTES = ("/", "/pricing", "/enterprise", "/security", "/docs",
                 "/templates", "/blog", "/changelog", "/customers", "/ai",
                 "/i", "/login", "/signup", "/privacy", "/terms")
RESERVED_SLUGS = ("login", "signup", "docs", "pricing", "blog", "changelog",
                  "customers", "templates", "security", "enterprise", "ai", "i",
                  "new", "account", "teams", "api", "v1", "sso", "verify",
                  "mfa", "passkey", "notifications", "search", "privacy",
                  "terms")
PLAN_CUSTOM_RULE_CAPS = (("hobby", 3), ("pro", 40), ("enterprise", 1000))
PRO_PRICE_CENTS = 2000
HOBBY_PRICE_CENTS = 0

DENIED = (401, 403, 404)
ACCEPTED = (200, 201, 202, 204)
REFUSED = (400, 409, 422)

SETTLE_ATTEMPTS = 20
SETTLE_INTERVAL = 0.25


def settle(predicate, attempts: int = SETTLE_ATTEMPTS,
           interval: float = SETTLE_INTERVAL):
    """Poll `predicate` until it returns something truthy, then return it.

    The one sanctioned sleep in the suite. An asynchronous side effect that has
    not landed yet is not a failure; an asynchronous side effect that never lands
    is, and the bound is what tells them apart.
    """
    outcome = None
    for _ in range(attempts):
        outcome = predicate()
        if outcome:
            return outcome
        time.sleep(interval)
    return outcome


def unique_suffix() -> str:
    """A per-run identifier, so a second run never collides with the first."""
    return uuid.uuid4().hex[:10]


def password() -> str:
    return seeded_password(SEED_PASSWORD_VAR, CORPUS_PASSWORD)


def _authed(email: str):
    return client(login(email, password()))


@pytest.fixture()
def anon():
    with client() as c:
        yield c


@pytest.fixture()
def developer():
    with _authed(DEVELOPER_EMAIL) as c:
        yield c


@pytest.fixture()
def reviewer():
    with _authed(REVIEWER_EMAIL) as c:
        yield c


@pytest.fixture()
def reviewer_two():
    with _authed(REVIEWER2_EMAIL) as c:
        yield c


@pytest.fixture()
def finance():
    with _authed(FINANCE_EMAIL) as c:
        yield c


@pytest.fixture()
def viewer():
    with _authed(VIEWER_EMAIL) as c:
        yield c


@pytest.fixture()
def foreign_developer():
    with _authed(FOREIGN_DEVELOPER_EMAIL) as c:
        yield c


@pytest.fixture(scope="session")
def db():
    """The relational store behind the `backend` slot, read directly.

    Used to prove a fact reached PostgreSQL rather than a page. An assertion that
    reads only the app's own response cannot tell a stored row from a rendered
    one.
    """
    return make_backend()


@pytest.fixture()
def app_base() -> str:
    return os.environ["APP_PUBLIC_URL"].rstrip("/")
