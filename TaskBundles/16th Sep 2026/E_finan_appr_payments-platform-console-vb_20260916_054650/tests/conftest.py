"""Task fixtures for deku/payments-platform-console-vb.

Implementation-agnostic (reference/J J.2): assume only the App Contract, the
literals pinned in instruction.md, and the backend capability fixture the
declared `db` slot earns. Observations are made over the JSON API, over the
served markup of the public routes, and over the rows in postgres. The `auth`
slot is observed at the interface boundary, which is where the brief states its
obligations: a wrong password returns no token, a lower role is refused, a
member of one organisation cannot reach another's rows. Nothing here imports an
SDK, reads the agent's source, or probes for a feature at run time. No test
function lives in this file.
"""

from __future__ import annotations

import os
import re
import time
from concurrent.futures import ThreadPoolExecutor

import httpx
import pytest
from appclient import app_url, client
from capabilities import Backend, make_backend

SETTLE_SECONDS = 2.0
TIMEOUT = 30.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give a side effect time to land before asserting on it."""
    time.sleep(seconds)


PASSWORD = "deku-demo-pw-2026"

SUPPORT_EMAIL = "support@example.com"
FINANCE_EMAIL = "finance@example.com"
ADMIN_EMAIL = "admin@example.com"
SUPPORT2_EMAIL = "support2@example.com"

SEEDED_ACCOUNTS = (SUPPORT_EMAIL, FINANCE_EMAIL, ADMIN_EMAIL, SUPPORT2_EMAIL)

SUPPORT_NAME = "Asha Rao"
FINANCE_NAME = "Kiran Mathew"
ADMIN_NAME = "Devika Nair"
SUPPORT2_NAME = "Damian Mueller"

ROLE_SUPPORT = "support"
ROLE_FINANCE = "finance"
ROLE_ADMIN = "administrator"
ROLES = (ROLE_SUPPORT, ROLE_FINANCE, ROLE_ADMIN)

ORG_NORTHBEAM = "northbeam"
ORG_WELLSPRING = "wellspring"
ORG_NORTHBEAM_LABEL = "Northbeam Retail"
ORG_WELLSPRING_LABEL = "Wellspring Studios"
ORGANISATIONS = (ORG_NORTHBEAM, ORG_WELLSPRING)

ENV_LIVE = "live"
ENV_SANDBOX = "sandbox"
ENVIRONMENTS = (ENV_SANDBOX, ENV_LIVE)

CURRENCY = "inr"
SUPPORT_CEILING = 500000

PAY_BEANBAR = "pay_beanbar_2280"
PAY_KAUFHAUS = "pay_kaufhaus_200000"
PAY_NORTHWIND = "pay_northwind_75000"
PAY_STREAMLY = "pay_streamly_4500"
PAY_CORVID = "pay_corvid_12345"
PAY_PLANSMITH = "pay_plansmith_12500"
PAY_SANDBOX_BEANBAR = "pay_sandbox_beanbar_1000"
PAY_LUMEN = "pay_lumen_7750"

NORTHBEAM_LIVE_PAYMENTS = {
    PAY_BEANBAR: 228000,
    PAY_KAUFHAUS: 20000000,
    PAY_NORTHWIND: 7500000,
    PAY_STREAMLY: 450000,
    PAY_CORVID: 12345,
    PAY_PLANSMITH: 1250000,
}
NORTHBEAM_LIVE_FEES = {
    PAY_BEANBAR: 4860,
    PAY_KAUFHAUS: 400300,
    PAY_NORTHWIND: 150300,
    PAY_STREAMLY: 9300,
    PAY_CORVID: 547,
    PAY_PLANSMITH: 25300,
}
SANDBOX_PAYMENT_AMOUNT = 100000
SANDBOX_PAYMENT_FEE = 2300
WELLSPRING_PAYMENT_AMOUNT = 775000
WELLSPRING_PAYMENT_FEE = 15800

PAYMENT_STATES = ("succeeded", "partially_refunded", "refunded", "disputed")
REQUEST_STATES = ("pending_approval", "executed", "rejected", "expired",
                  "withdrawn", "execution_failed")
BALANCE_KINDS = ("available", "pending", "disputed", "fee", "in_transit",
                 "settlement")

NORTHBEAM_LIVE_BALANCES = {
    "available": 27226598,
    "disputed": 1250000,
    "fee": 740607,
    "in_transit": 0,
    "pending": 0,
    "settlement": -29217205,
}
NORTHBEAM_SANDBOX_BALANCES = {
    "available": 97700,
    "disputed": 0,
    "fee": 2300,
    "in_transit": 0,
    "pending": 0,
    "settlement": -100000,
}
WELLSPRING_LIVE_BALANCES = {
    "available": 759200,
    "disputed": 0,
    "fee": 15800,
    "in_transit": 0,
    "pending": 0,
    "settlement": -775000,
}

DISPUTE_PLANSMITH = "dp_plansmith_0001"
DISPUTE_FEE = 150000
PAYOUT_NORTHBEAM = "po_northbeam_2231"
PAYOUT_AMOUNT = 223140
PAYOUT_DESCRIPTOR = "NIMBUS NORTHBEAM"

KEY_LIVE = "key_northbeam_live_01"
KEY_SANDBOX = "key_northbeam_sandbox_01"
PREFIX_SECRET_LIVE = "sk_live_"
PREFIX_SECRET_SANDBOX = "sk_sandbox_"
PREFIX_PUBLISHABLE_LIVE = "pk_live_"
PREFIX_PUBLISHABLE_SANDBOX = "pk_sandbox_"

ENDPOINT_NORTHBEAM = "whe_northbeam_live_01"
ENDPOINT_URL = "https://hooks.northbeam.example/nimbus"
FORBIDDEN_ENDPOINTS = (
    "http://127.0.0.1/hooks",
    "https://localhost/hooks",
    "https://10.0.0.7/hooks",
    "https://169.254.169.254/latest",
)
EVENT_TYPES = (
    "payment.succeeded", "payment.disputed", "refund.created", "refund.failed",
    "approval_request.created", "approval_request.approved",
    "approval_request.rejected", "approval_request.expired", "payout.paid",
)

CODE_APPROVAL_REQUIRED = "approval_required"
CODE_APPROVAL_EXPIRED = "approval_expired"
CODE_SELF_APPROVAL = "self_approval_forbidden"
CODE_AMOUNT_TOO_LARGE = "amount_too_large"
CODE_PAYMENT_DISPUTED = "payment_disputed"
CODE_IDEMPOTENCY_CONFLICT = "idempotency_conflict"
CODE_ENDPOINT_FORBIDDEN = "endpoint_address_forbidden"
CODE_SPAM = "spam_suspected"

DECOY_FIELD = "company_fax"
VOLUME_BANDS = ("under_1_crore", "1_to_10_crore", "10_to_50_crore",
                "50_to_250_crore", "over_250_crore")

NOT_FOUND_COPY = "We cannot find that page."
AVAILABILITY_BADGE = "Not available in your country"
GATED_ACTION = "Join the waitlist"
HERO_EYEBROW = "Global GDP running on Nimbus:"
HERO_LEAD = "Financial infrastructure to grow your revenue."
HERO_ACTION = "Request an invite"
LOCALE_LABEL = "India (English)"
COPYRIGHT = "(c) 2026 Nimbus"
SANDBOX_BAND = "Sandbox. No real money moves here."
CEILING_NOTICE = "This is above your refund limit of"
JUSTIFICATION_PROMPT = "Why is this needed? Approvers will read this."
SECRET_ONCE_NOTICE = "Copy this now. It will not be shown again."

ROUTE_ROOT = "/"
ROUTE_HOME = "/in"
ROUTE_BILLING = "/in/billing"
ROUTE_GUARD = "/in/guard"
ROUTE_QUERY = "/in/query"
ROUTE_PRICING = "/in/pricing"
ROUTE_GUIDES = "/in/guides"
ROUTE_STORIES = "/in/customer-stories"
ROUTE_PRIVACY = "/in/privacy-and-terms"
ROUTE_CONTACT = "/in/contact-sales"
ROUTE_SITEMAP = "/sitemap.xml"
ROUTE_ROBOTS = "/robots.txt"
ROUTE_FAVICON = "/favicon.ico"
ROUTE_SIGNIN = "/signin"
ROUTE_ACCOUNTS = "/accounts"

PUBLIC_ROUTES = (ROUTE_HOME, ROUTE_BILLING, ROUTE_GUARD, ROUTE_QUERY,
                 ROUTE_PRICING, ROUTE_GUIDES, ROUTE_STORIES, ROUTE_PRIVACY,
                 ROUTE_CONTACT)

README_PATH = "/app/USER_README.md"
SCREENSHOT_DIR = "/app/.browser_screenshots"
DOWNLOAD_DIR = "/app/.downloads"

API_HEALTH = "/health"
API_LOGIN = "/auth/login"
API_ME = "/me"
API_ACCOUNTS = "/accounts"
API_LEADS = "/leads"

OK_READ = (200,)
OK_WRITE = (200, 201)
REFUSED = (400, 409, 422)
DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
NOT_FOUND = (404,)
CONFLICT = (409, 422)

TABLE_PERSON = "person"
TABLE_ACCOUNT = "account"
TABLE_MEMBERSHIP = "membership"
TABLE_PAYMENT = "payment"
TABLE_REFUND = "refund"
TABLE_REQUEST = "approval_request"
TABLE_BALANCE = "balance"
TABLE_LEDGER_TRANSACTION = "ledger_transaction"
TABLE_LEDGER_ENTRY = "ledger_entry"
TABLE_PAYOUT = "payout"
TABLE_PAYOUT_ITEM = "payout_item"
TABLE_DISPUTE = "dispute"
TABLE_CREDENTIAL = "api_credential"
TABLE_ENDPOINT = "webhook_endpoint"
TABLE_EVENT = "event"
TABLE_AUDIT = "audit_record"
TABLE_IDEMPOTENCY = "idempotency_key"
TABLE_LEAD = "lead"

SEEDED_TABLES = (
    TABLE_PERSON, TABLE_ACCOUNT, TABLE_MEMBERSHIP, TABLE_PAYMENT,
    TABLE_BALANCE, TABLE_LEDGER_TRANSACTION, TABLE_LEDGER_ENTRY,
    TABLE_PAYOUT, TABLE_DISPUTE, TABLE_CREDENTIAL, TABLE_ENDPOINT,
)

AMOUNT_ABOVE_CEILING = 600000
AMOUNT_WITHIN_CEILING = 100000
AMOUNT_BEYOND_REMAINDER = 99999999

OG_TITLE_RE = re.compile(
    r"<meta[^>]+property=[\"']og:title[\"'][^>]*content=[\"']([^\"']+)[\"']",
    re.IGNORECASE)
OG_IMAGE_RE = re.compile(
    r"<meta[^>]+property=[\"']og:image[\"'][^>]*content=[\"']([^\"']+)[\"']",
    re.IGNORECASE)
OG_DESC_RE = re.compile(
    r"<meta[^>]+property=[\"']og:description[\"'][^>]*content=[\"']([^\"']+)[\"']",
    re.IGNORECASE)
ICON_RE = re.compile(
    r"<link[^>]+rel=[\"'][^\"']*icon[^\"']*[\"']", re.IGNORECASE)
SITEMAP_LINE_RE = re.compile(r"(?im)^\s*sitemap\s*:\s*(\S+)\s*$")


def ttl_seconds() -> int:
    """The refund-request lifetime the environment injects (reference/J J.9)."""
    raw = str(os.environ.get("REFUND_REQUEST_TTL_SEC", "")).strip()
    value = int(raw) if raw.isdigit() else 0
    return value if value > 0 else 8


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
    """The site without redirect following, so a redirect is observable."""
    with httpx.Client(base_url=app_url(), timeout=TIMEOUT,
                      follow_redirects=False) as c:
        yield c


class LedgerStore:
    """Provider-agnostic domain queries composed from Backend primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def rows(self, table: str, **where) -> list[dict]:
        return self._b.rows(table, **where)

    def count(self, table: str, **where) -> int:
        return self._b.count(table, **where)

    def one(self, table: str, **where):
        return self._b.one(table, **where)

    def payment(self, payment_id: str):
        return self._b.one(TABLE_PAYMENT, id=payment_id)

    def refunds_of(self, payment_id: str) -> list[dict]:
        return self._b.rows(TABLE_REFUND, payment_id=payment_id)

    def request(self, request_id: str):
        return self._b.one(TABLE_REQUEST, id=request_id)

    def audit(self, **where) -> list[dict]:
        return self._b.rows(TABLE_AUDIT, **where)


@pytest.fixture(scope="session")
def db() -> LedgerStore:
    return LedgerStore(make_backend())


def probe_token() -> str:
    """A per-run token no other run collides with (reference/J J.5)."""
    return os.urandom(6).hex()


def probe_key() -> str:
    """A fresh idempotency key for this run."""
    return "probe-%s" % probe_token()


PROBE_DOMAIN = "deku.test"


def probe_email() -> str:
    return "probe-%s@%s" % (probe_token(), PROBE_DOMAIN)


def probe_reason(prefix: str = "Probe refund") -> str:
    return "%s %s" % (prefix, probe_token())


def probe_justification() -> str:
    return ("A customer of long standing asked for a goodwill return, probe %s"
            % probe_token())


def login(api_client, email: str, password: str = PASSWORD):
    """Sign in, returning the raw response so a caller can assert on refusal."""
    return api_client.post(API_LOGIN, json={"email": email, "password": password})


def token_of(payload) -> str:
    if isinstance(payload, dict):
        for key in ("access_token", "token", "bearer", "accessToken"):
            if isinstance(payload.get(key), str) and payload[key]:
                return payload[key]
    return ""


def bearer(api_client, email: str, password: str = PASSWORD) -> dict:
    """Authorization header for a seeded account, acquired per call (J.11)."""
    response = login(api_client, email, password)
    assert response.status_code in OK_WRITE, (
        "%s refused the seeded account %r with the pinned password: status %s, "
        "body %r" % (API_LOGIN, email, response.status_code, response.text[:300]))
    value = token_of(response.json())
    assert value, (
        "%s returned no bearer token for %r: body %r"
        % (API_LOGIN, email, response.text[:300]))
    return {"Authorization": "Bearer %s" % value}


def account_path(account: str, *parts) -> str:
    tail = "/".join(str(p).strip("/") for p in parts if str(p).strip("/"))
    return "%s/%s%s" % (API_ACCOUNTS, account, ("/" + tail) if tail else "")


def as_list(payload) -> list:
    """A list endpoint returns a top-level JSON array; tolerate nothing else."""
    return payload if isinstance(payload, list) else []


def field(row, *names):
    """First present value among tolerated field spellings."""
    for name in names:
        if isinstance(row, dict) and name in row and row[name] not in (None, ""):
            return row[name]
    return None


def body_text(response) -> str:
    return getattr(response, "text", "") or ""


def json_body(response):
    """The decoded body when the response declares JSON, else an empty map."""
    kind = str(response.headers.get("content-type", "")).lower()
    if "json" not in kind:
        return {}
    return response.json()


def error_code(response) -> str:
    """The stable machine-readable code out of the pinned error envelope."""
    payload = json_body(response)
    if isinstance(payload, dict):
        err = payload.get("error")
        if isinstance(err, dict):
            value = field(err, "code", "type")
            if value:
                return str(value)
        value = field(payload, "code", "error_code")
        if value:
            return str(value)
    return ""


def mentions(response, *needles) -> bool:
    """The response body names every needle, case-insensitively."""
    low = body_text(response).lower()
    return all(str(n).lower() in low for n in needles)


def read_payments(api_client, headers: dict, account: str,
                  environment: str = ENV_LIVE):
    return api_client.get(account_path(account, "payments"),
                          params={"environment": environment}, headers=headers)


def read_payment(api_client, headers: dict, account: str, payment_id: str,
                 environment: str = ENV_LIVE):
    return api_client.get(account_path(account, "payments", payment_id),
                          params={"environment": environment}, headers=headers)


def read_balances(api_client, headers: dict, account: str,
                  environment: str = ENV_LIVE) -> dict:
    """kind -> amount_minor, read back through the interface."""
    response = api_client.get(account_path(account, "balances"),
                              params={"environment": environment},
                              headers=headers)
    assert response.status_code in OK_READ, (
        "reading balances of %r in %r returned %s: %r"
        % (account, environment, response.status_code, response.text[:300]))
    out = {}
    for row in as_list(response.json()):
        kind = field(row, "kind", "balance_kind")
        amount = field(row, "amount_minor", "amount")
        if kind is not None and amount is not None:
            out[str(kind)] = int(amount)
    assert out, (
        "balances of %r in %r came back empty; the brief seeds six kinds"
        % (account, environment))
    return out


def available_of(api_client, headers: dict, account: str,
                 environment: str = ENV_LIVE) -> int:
    return read_balances(api_client, headers, account, environment)["available"]


def create_refund(api_client, headers: dict, account: str, payment_id: str,
                  amount: int, key: str | None = None, reason: str | None = None):
    payload = {
        "amount_minor": amount,
        "currency": CURRENCY,
        "reason": reason or probe_reason(),
    }
    send = dict(headers)
    send["Idempotency-Key"] = key or probe_key()
    return api_client.post(account_path(account, "payments", payment_id, "refunds"),
                           json=payload, headers=send)


def raise_request(api_client, headers: dict, account: str, payment_id: str,
                  amount: int, key: str | None = None):
    payload = {
        "amount_minor": amount,
        "currency": CURRENCY,
        "reason": probe_reason("Probe request"),
        "justification": probe_justification(),
    }
    send = dict(headers)
    send["Idempotency-Key"] = key or probe_key()
    return api_client.post(
        account_path(account, "payments", payment_id, "refund-requests"),
        json=payload, headers=send)


def approve_request(api_client, headers: dict, account: str, request_id: str,
                    note: str | None = None):
    payload = {} if note is None else {"note": note}
    return api_client.post(
        account_path(account, "approval-requests", request_id, "approve"),
        json=payload, headers=headers)


def reject_request(api_client, headers: dict, account: str, request_id: str,
                   note: str):
    return api_client.post(
        account_path(account, "approval-requests", request_id, "reject"),
        json={"note": note}, headers=headers)


def read_request(api_client, headers: dict, account: str, request_id: str):
    return api_client.get(
        account_path(account, "approval-requests", request_id), headers=headers)


def id_of(payload) -> str:
    value = field(payload, "id", "request_id", "refund_id", "identifier")
    return str(value) if value else ""


def state_of(payload) -> str:
    value = field(payload, "state", "status")
    return str(value) if value else ""


def raised_request_id(api_client, headers: dict, account: str, payment_id: str,
                      amount: int) -> str:
    """Raise a request above the ceiling and return the identifier it was given."""
    response = raise_request(api_client, headers, account, payment_id, amount)
    assert response.status_code in OK_WRITE, (
        "raising a refund request on %r for %s returned %s: %r"
        % (payment_id, amount, response.status_code, response.text[:300]))
    value = id_of(response.json())
    assert value, (
        "the raised request carried no identifier: body %r"
        % response.text[:300])
    return value


def wait_for_state(api_client, headers: dict, account: str, request_id: str,
                   wanted, deadline_seconds: float):
    """Poll to a monotonic deadline for a request to reach one of `wanted`."""
    wanted = tuple(wanted)
    end = time.monotonic() + deadline_seconds
    seen = ""
    while time.monotonic() < end:
        response = read_request(api_client, headers, account, request_id)
        if response.status_code in OK_READ:
            seen = state_of(response.json())
            if seen in wanted:
                return seen
        settle(0.5)
    return seen


def in_parallel(calls):
    """Run callables at the same instant and return their results in order."""
    with ThreadPoolExecutor(max_workers=len(calls)) as pool:
        futures = [pool.submit(c) for c in calls]
        return [f.result() for f in futures]
