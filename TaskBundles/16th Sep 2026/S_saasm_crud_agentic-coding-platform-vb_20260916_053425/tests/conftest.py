"""Task fixtures for deku/agentic-coding-platform-vb.

Implementation-agnostic (reference/J J.2): assume only the App Contract, the
literals pinned in instruction.md, and the capability fixtures the declared
backend, email and payments slots earn. Observations are made over the JSON API,
over the served markup of the public and account routes, over the rows in
postgres, over the inbox at mailpit and over the accounts killbill holds.
Nothing here imports an SDK, reads the agent's source, or probes for a feature at
run time. No test function lives in this file.
"""

from __future__ import annotations

import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor

import httpx
import pytest
from appclient import app_url, client
from capabilities import Backend, make_backend, make_inbox, make_payments

SETTLE_SECONDS = 2.0
TIMEOUT = 30.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give a side effect time to land before asserting on it."""
    time.sleep(seconds)


PASSWORD = "deku-demo-pw-2026"

OWNER_EMAIL = "owner@example.com"
MEMBER_EMAIL = "member@example.com"
OWNER2_EMAIL = "owner2@example.com"
SEEDED_ACCOUNTS = (OWNER_EMAIL, MEMBER_EMAIL, OWNER2_EMAIL)

OWNER_NAME = "Devan Ashworth"
MEMBER_NAME = "Priya Raghunathan"
OWNER2_NAME = "Marguerite Sandoval"

ROLE_OWNER = "owner"
ROLE_MEMBER = "member"

WS_AURORA = "aurora-data"
WS_NORTHLIGHT = "northlight"
WS_AURORA_LABEL = "Aurora Data"
WS_NORTHLIGHT_LABEL = "Northlight"

MEMBERSHIP_STATES = ("invited", "active", "removed")
INVITATION_STATES = ("pending", "accepted", "revoked", "expired")
SUBSCRIPTION_STATES = ("active", "past_due", "canceled")
INTERVALS = ("monthly", "yearly")
SURFACES = ("desktop", "terminal", "cloud", "mobile", "review", "automation", "api")

PLAN_CODES = ("hobby", "individual", "teams", "enterprise")
TIER_CODES = ("hobby", "pro", "pro_plus", "ultra", "standard", "premium",
              "enterprise")
TIER_MONTHLY = {"hobby": 0, "pro": 2000, "pro_plus": 6000, "ultra": 20000,
                "standard": 4000, "premium": 8000}
TIER_YEARLY = {"hobby": 0, "pro": 20000, "pro_plus": 60000, "ultra": 200000,
               "standard": 40000, "premium": 80000}
TIER_ALLOWANCE = {"hobby": 500, "pro": 2000, "pro_plus": 6000, "ultra": 20000,
                  "standard": 4000, "premium": 8000}

BENCHMARK_VERSION = "MarlinBench 3.2"
MODEL_COUNT = 15
MODEL_CODES = ("meridian-4-max", "kestrel-4", "corvus-3-pro", "meridian-4",
               "lyra-2-ultra", "tessel-9", "corvus-3", "meridian-4-mini",
               "lyra-2", "kestrel-3-5", "tessel-8", "pallas-1-large",
               "corvus-2", "pallas-1", "glim-7b")
MODEL_NAMES = ("Meridian 4 Max", "Kestrel 4", "Corvus 3 Pro", "Meridian 4",
               "Lyra 2 Ultra", "Tessel 9", "Corvus 3", "Meridian 4 Mini",
               "Lyra 2", "Kestrel 3.5", "Tessel 8", "Pallas 1 Large",
               "Corvus 2", "Pallas 1", "Glim 7B")
MODEL_SCORE_BP = {"meridian-4-max": 7080, "kestrel-4": 7050,
                  "corvus-3-pro": 7000, "meridian-4": 6990,
                  "lyra-2-ultra": 6930, "tessel-9": 6840, "corvus-3": 6720,
                  "meridian-4-mini": 6710, "lyra-2": 6650, "kestrel-3-5": 6580,
                  "tessel-8": 6410, "pallas-1-large": 6270, "corvus-2": 5830,
                  "pallas-1": 5460, "glim-7b": 4720}
MODEL_COST = {"meridian-4-max": 281, "kestrel-4": 1732, "corvus-3-pro": 823,
              "meridian-4": 234, "lyra-2-ultra": 735, "tessel-9": 1173,
              "corvus-3": 569, "meridian-4-mini": 128, "lyra-2": 612,
              "kestrel-3-5": 944, "tessel-8": 358, "pallas-1-large": 1508,
              "corvus-2": 205, "pallas-1": 176, "glim-7b": None}
MODEL_TOKENS = {"meridian-4-max": 41136, "kestrel-4": 103525,
                "corvus-3-pro": 61838, "meridian-4": 32449,
                "lyra-2-ultra": 54239, "tessel-9": 64971, "corvus-3": 28320,
                "meridian-4-mini": 17942, "lyra-2": 30188, "kestrel-3-5": 47210,
                "tessel-8": 22904, "pallas-1-large": 88431, "corvus-2": 19677,
                "pallas-1": 15320, "glim-7b": 9840}
MODEL_STEPS = {"meridian-4-max": 46, "kestrel-4": 72, "corvus-3-pro": 78,
               "meridian-4": 39, "lyra-2-ultra": 72, "tessel-9": 56,
               "corvus-3": 48, "meridian-4-mini": 29, "lyra-2": 51,
               "kestrel-3-5": 63, "tessel-8": 35, "pallas-1-large": 81,
               "corvus-2": 33, "pallas-1": 28, "glim-7b": 24}
MODEL_UNCOSTED = "glim-7b"
MODEL_UNCOSTED_NAME = "Glim 7B"
COST_NOT_MEASURED = "not measured"

CATALOGUE_KINDS = ("plugin", "automation")
CATALOGUE_CATEGORIES = ("Infrastructure", "Data & Analytics", "Productivity",
                        "Communication")
CATALOGUE_SORTS = ("relevance", "recent", "popular")
PLUGIN_SLUGS = ("foolscap", "loop", "trace", "atlas", "klaxon", "radar",
                "shipyard", "tinbox", "quarry", "lumen")
AUTOMATION_SLUGS = ("assign-pr-reviewers", "summarize-changes-daily",
                    "find-vulnerabilities", "fix-bugs-reported-in-loop",
                    "triage-failed-actions", "automatic-test-coverage")
CATALOGUE_PUBLISHED_COUNT = 16
WITHDRAWN_SLUG = "pallas-connect"
INSTALL_COUNTS = {"foolscap": 4820, "loop": 6140, "trace": 3975, "atlas": 3975,
                  "klaxon": 2860, "radar": 2545, "shipyard": 3310,
                  "tinbox": 1490, "quarry": 2280, "lumen": 1725,
                  "assign-pr-reviewers": 1980, "summarize-changes-daily": 1640,
                  "find-vulnerabilities": 2420, "fix-bugs-reported-in-loop": 1215,
                  "triage-failed-actions": 905, "automatic-test-coverage": 1370}
TIE_SLUGS = ("atlas", "trace")
TIE_COUNT = 3975
FOOLSCAP_COUNT = 4820
FOOLSCAP_COUNT_AFTER = 4821

RELEASE_VERSIONS = ("3.16", "3.17", "3.18")
RELEASE_LATEST = "3.18"
RELEASE_PREVIOUS = "3.17"
PLATFORM_ROWS = (("macos", "arm64", "dmg"), ("macos", "x64", "dmg"),
                 ("linux", "x64", "deb"), ("linux", "arm64", "deb"),
                 ("linux", "armv7", "deb"), ("windows", "x64", "exe"),
                 ("windows", "x64", "msi"), ("windows", "x64", "zip"))
ARTIFACT_COUNT = 23
GAP_PLATFORM = ("linux", "armv7", "deb")
LATEST_MACOS_CHECKSUM = (
    "9f2a4c6e8b0d1357a9c2e4f60821b3d5c7e9f0a2b4d6e8f0a1c3e5d7b9f1a3c5")

CHANGELOG_SLUGS = ("cloud-agents-without-a-repository",
                   "subscriptions-and-pinned-skills",
                   "anchor-hosted-repositories", "marlinbench-3-2")

AURORA_USAGE_KEYS = ("seed-usage-aurora-1", "seed-usage-aurora-2",
                     "seed-usage-aurora-3")
NORTHLIGHT_USAGE_KEY = "seed-usage-northlight-1"
AURORA_CONSUMED = 8869
AURORA_INCLUDED = 8000
AURORA_OVERAGE = 869
AURORA_SEATS = 2
AURORA_SPEND_LIMIT = 2500
NORTHLIGHT_CONSUMED = 384
NORTHLIGHT_INCLUDED = 500

BILLING_KEY_AURORA = "marlin-ws-aurora-data"
BILLING_KEY_NORTHLIGHT = "marlin-ws-northlight"
BILLING_KEY_PREFIX = "marlin-ws-"
BILLING_CURRENCY = "USD"
BILLING_COUNTRY = "US"

INVITE_SUBJECT_PREFIX = "Marlin invitation:"
INVITE_SUBJECT_AURORA = "Marlin invitation: Aurora Data"

CALC_BLENDED = "$8.33"
CALC_CHEAPER = "52%"
CALC_SAVED_MONTH = "$2,076.21"
CALC_SAVED_YEAR = "$24,914.55"
CALC_NEW_ANNUAL = "$23,085.45"
CALC_OLD_ANNUAL = "$48,000.00"
CALC_BASELINE_COST = "$17.32"
CALC_SPEND = "$4,000.00"
CALC_TASKS_NEW = "480"
CALC_TASKS_OLD = "231"
CALC_ALLOCATION_TOTAL = "100"

SKIP_LINK = "Skip to content"
HOME_HEADLINE = "Marlin is your coding agent for building ambitious software."
HOME_TRUST = "Trusted every day by teams that build world-class software"
HOME_CHANGELOG_LINK = "See what's new in Marlin"
NARROW_PRIMARY = "Get started"
INSTALL_TABS = ("PowerShell", "Linux / WSL")
COMPLIANCE_LINE = "SOC 2 | ISO27001 | ISO42001 | AIUC-1 Certified"
QUESTIONS_HEADING = "Questions & Answers"
MARKETPLACE_HEADING = "Extend the Agent"
DOWNLOAD_HEADLINE = "Use Marlin everywhere you work"
LEADERBOARD_COLUMNS = ("MODEL", "SCORE", "COST / TASK", "TOKENS / TASK",
                       "STEPS / TASK")
UNIT_SWITCH = ("Cost", "Tokens", "Steps")
CHART_AXIS_SCORE = "MarlinBench 3.2 score"
CHART_AXIS_COST = "Average cost per task"

ROUTE_HOME = "/"
ROUTE_PRODUCT = "/product"
ROUTE_CLOUD = "/cloud"
ROUTE_CLI = "/cli"
ROUTE_FIXBOT = "/fixbot"
ROUTE_AUTOMATE = "/automate"
ROUTE_MOBILE = "/mobile"
ROUTE_MERIDIAN = "/meridian"
ROUTE_KESTREL = "/kestrel"
ROUTE_EVALS = "/evals"
ROUTE_CALCULATOR = "/cost-savings"
ROUTE_MARKETPLACE = "/marketplace"
ROUTE_TEAMS = "/business/teams"
ROUTE_ENTERPRISE = "/enterprise"
ROUTE_PRICING = "/pricing"
ROUTE_DOWNLOAD = "/download"
ROUTE_CHANGELOG = "/changelog"
ROUTE_SECURITY = "/security"
ROUTE_PRIVACY = "/privacy"
ROUTE_TERMS = "/terms-of-service"
ROUTE_DATA_USE = "/data-use"
ROUTE_CONTACT = "/contact-sales"
ROUTE_SIGNIN = "/signin"
ROUTE_SIGNUP = "/signup"
ROUTE_ACCOUNT = "/account"
ROUTE_ACCOUNT_USAGE = "/account/usage"
ROUTE_ACCOUNT_BILLING = "/account/billing"
ROUTE_ACCOUNT_MEMBERS = "/account/members"
ROUTE_ACCOUNT_SETTINGS = "/account/settings"
ROUTE_SITEMAP = "/sitemap.xml"
ROUTE_ROBOTS = "/robots.txt"

PUBLIC_ROUTES = (ROUTE_HOME, ROUTE_PRODUCT, ROUTE_CLOUD, ROUTE_CLI,
                 ROUTE_FIXBOT, ROUTE_AUTOMATE, ROUTE_MOBILE, ROUTE_MERIDIAN,
                 ROUTE_KESTREL, ROUTE_EVALS, ROUTE_CALCULATOR,
                 ROUTE_MARKETPLACE, ROUTE_TEAMS, ROUTE_ENTERPRISE,
                 ROUTE_PRICING, ROUTE_DOWNLOAD, ROUTE_CHANGELOG,
                 ROUTE_SECURITY, ROUTE_PRIVACY, ROUTE_TERMS, ROUTE_DATA_USE,
                 ROUTE_CONTACT, ROUTE_SIGNIN, ROUTE_SIGNUP)
ACCOUNT_ROUTES = (ROUTE_ACCOUNT, ROUTE_ACCOUNT_USAGE, ROUTE_ACCOUNT_BILLING,
                  ROUTE_ACCOUNT_MEMBERS, ROUTE_ACCOUNT_SETTINGS)

API_HEALTH = "/health"
API_SIGNUP = "/auth/signup"
API_SIGNIN = "/auth/signin"
API_ME = "/me"
API_MODELS = "/models"
API_PLANS = "/plans"
API_PLUGINS = "/plugins"
API_RELEASES = "/releases"
API_RESOLVE = "/releases/resolve"
API_CHANGELOG = "/changelog"
API_WORKSPACES = "/workspaces"
API_ACCEPT = "/invitations/accept"
API_CHECKOUT = "/billing/checkout"
API_SUBSCRIPTION = "/billing/subscription"
API_LEADS = "/leads"

OK_READ = (200,)
OK_WRITE = (200, 201)
REFUSED = (400, 409, 422)
DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
NOT_FOUND = (404,)
CONFLICT = (409, 422)
PAYMENT_REQUIRED = (402, 403, 409, 422)

TABLE_USERS = "users"
TABLE_WORKSPACES = "workspaces"
TABLE_MEMBERSHIPS = "memberships"
TABLE_INVITATIONS = "invitations"
TABLE_PLANS = "plans"
TABLE_TIERS = "tiers"
TABLE_ENTITLEMENTS = "entitlements"
TABLE_SUBSCRIPTIONS = "subscriptions"
TABLE_MODELS = "models"
TABLE_PLUGINS = "plugins"
TABLE_INSTALLATIONS = "installations"
TABLE_ARTIFACTS = "release_artifacts"
TABLE_CHANGELOG = "changelog_entries"
TABLE_USAGE = "usage_events"
TABLE_ALLOWANCES = "allowances"
TABLE_LEADS = "leads"

SEEDED_TABLES = (TABLE_USERS, TABLE_WORKSPACES, TABLE_MEMBERSHIPS, TABLE_PLANS,
                 TABLE_TIERS, TABLE_ENTITLEMENTS, TABLE_MODELS, TABLE_PLUGINS,
                 TABLE_ARTIFACTS, TABLE_CHANGELOG, TABLE_USAGE)

SECRET_MARKERS = ("orbit-labs-secret-9f14c73e", "deku-local-dev",
                  "postgresql://", "PAYMENTS_API_SECRET")


@pytest.fixture(scope="session")
def api():
    """The JSON API under /api, unauthenticated."""
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def site():
    """The site itself, for reading served markup."""
    with httpx.Client(base_url=app_url(), timeout=TIMEOUT,
                      follow_redirects=True) as c:
        yield c


@pytest.fixture(scope="session")
def raw_site():
    """The site without redirect following, for asserting a redirect itself."""
    with httpx.Client(base_url=app_url(), timeout=TIMEOUT,
                      follow_redirects=False) as c:
        yield c


class MarlinStore:
    """Provider-agnostic domain queries composed from Backend primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def rows(self, table: str, **where) -> list[dict]:
        return self._b.rows(table, **where)

    def count(self, table: str, **where) -> int:
        return len(self._b.rows(table, **where))


@pytest.fixture(scope="session")
def db() -> MarlinStore:
    return MarlinStore(make_backend())


@pytest.fixture(scope="session")
def inbox():
    return make_inbox()


@pytest.fixture(scope="session")
def payments():
    return make_payments()


def probe_token() -> str:
    """A per-run token no other run collides with (reference/J J.5)."""
    return os.urandom(6).hex()


def probe_email(prefix: str = "probe") -> str:
    return "%s-%s@%s" % (prefix, probe_token(), "example.com")


def probe_slug(prefix: str = "probe") -> str:
    return "%s-%s" % (prefix, probe_token())


def signup(api_client, email: str, display_name: str = "Probe Person",
           password: str = PASSWORD):
    return api_client.post(API_SIGNUP, json={"email": email,
                                             "password": password,
                                             "display_name": display_name})


def signin(api_client, email: str, password: str = PASSWORD):
    return api_client.post(API_SIGNIN, json={"email": email,
                                             "password": password})


def token_of(payload) -> str:
    if isinstance(payload, dict):
        for key in ("token", "access_token", "bearer", "accessToken"):
            if isinstance(payload.get(key), str) and payload[key]:
                return payload[key]
        data = payload.get("data")
        if isinstance(data, dict):
            return token_of(data)
    return ""


def bearer(api_client, email: str, password: str = PASSWORD) -> dict:
    """The Authorization header for a seeded account, as the brief pins it."""
    response = signin(api_client, email, password)
    assert response.status_code in OK_WRITE, (
        "POST /api%s for %r returned %s: %r"
        % (API_SIGNIN, email, response.status_code, response.text[:300]))
    token = token_of(json_body(response))
    assert token, (
        "POST /api%s for %r returned no bearer token: %r"
        % (API_SIGNIN, email, response.text[:300]))
    return {"Authorization": "Bearer %s" % token}


def json_body(response):
    """The decoded body, or None when the response carries no JSON document."""
    text = (response.text or "").strip()
    if not text or text[0] not in "[{":
        return None
    return json.loads(text)


def as_list(payload) -> list:
    """A listing shape, whether the brief pins a bare array or an envelope."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "items", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def field(row, *names, default=None):
    """Read the first present spelling of a field from a mapping."""
    if not isinstance(row, dict):
        return default
    for name in names:
        if name in row and row[name] is not None:
            return row[name]
    return default


def workspace_path(slug: str, suffix: str = "") -> str:
    return "%s/%s%s" % (API_WORKSPACES, slug, suffix)


def plugin_path(kind: str, slug: str, suffix: str = "") -> str:
    return "%s/%s/%s%s" % (API_PLUGINS, kind, slug, suffix)


def mentions(text: str, needle: str) -> bool:
    return needle.lower() in (text or "").lower()


def visible_text(markup: str) -> str:
    """Served markup with tags removed, so a copy assertion reads what a person
    reads rather than an attribute value."""
    without_script = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", markup or "")
    return re.sub(r"<[^>]+>", " ", without_script)


def in_parallel(call, count: int = 2) -> list:
    """Fire `count` identical requests at once and return every response."""
    with ThreadPoolExecutor(max_workers=count) as pool:
        futures = [pool.submit(call) for _ in range(count)]
        return [f.result() for f in futures]


def accounts_with_key(payments_client, external_key: str) -> list[dict]:
    """Every killbill account carrying this external key."""
    return [a for a in payments_client.accounts()
            if str(field(a, "externalKey", "external_key", default="")) == external_key]
