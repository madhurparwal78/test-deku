"""Fixtures, pinned literals and domain stores for Aurelia.

Every literal below is pinned in instruction.md. Nothing here defines a test.
"""

from __future__ import annotations

import os
import time
import uuid
from typing import Any

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"

EDITOR_EMAIL = "editor@example.com"
READER_EMAIL = "reader@example.com"
OWNER_EMAIL = "owner@example.com"
ADMIN_EMAIL = "admin@example.com"
APPROVER_EMAIL = "approver@example.com"
INITIATOR_EMAIL = "initiator@example.com"
BOOKKEEPER_EMAIL = "bookkeeper@example.com"
CARDHOLDER_EMAIL = "cardholder@example.com"
OWNER2_EMAIL = "owner2@example.com"

ROLE_OWNER = "owner"
ROLE_ADMIN = "admin"
ROLE_APPROVER = "approver"
ROLE_INITIATOR = "initiator"
ROLE_BOOKKEEPER = "bookkeeper"
ROLE_CARD_ONLY = "card_only"
ROLES = (ROLE_OWNER, ROLE_ADMIN, ROLE_APPROVER, ROLE_INITIATOR,
         ROLE_BOOKKEEPER, ROLE_CARD_ONLY)

ORG_ONE = "Meridian Robotics"
ORG_ONE_SLUG = "meridian-robotics"
ORG_TWO = "Calder Textiles"
ORG_TWO_SLUG = "calder-textiles"

ACCOUNT_OPERATING = "Meridian Operating"
ACCOUNT_TREASURY = "Meridian Treasury"
ACCOUNT_CREDIT = "Meridian Card"
ACCOUNT_OPERATING_TWO = "Calder Operating"

PARTNER_BANK_ONE = "Northgate Bank"
PARTNER_BANK_TWO = "Talbot National"

CURRENCY_STORED = "usd"
CURRENCY_WIRE = "USD"

RECIPIENT_CLEAN = "Jane Black"
RECIPIENT_CLEAN_ID = "rcpt_4d82e1af"
RECIPIENT_LISTED = "Viktor Halberd"
RECIPIENT_LISTED_ID = "rcpt_9c11b7d3"

SANCTIONS_VERSION_CLEAN = "2026-09-01"
SANCTIONS_VERSION_LISTED = "2026-09-15"

RAILS = ("internal", "ach", "wire", "realtime", "cheque", "card")
RAIL_INTERNAL = "internal"
RAIL_ACH = "ach"
RAIL_WIRE = "wire"
RAIL_REALTIME = "realtime"

STATUSES = ("draft", "pendingApproval", "approved", "scheduled", "submitted",
            "settled", "failed", "returned", "cancelled", "recallRequested")
STATUS_PENDING = "pendingApproval"
STATUS_APPROVED = "approved"
STATUS_SCHEDULED = "scheduled"
STATUS_SUBMITTED = "submitted"
STATUS_SETTLED = "settled"
STATUS_RETURNED = "returned"
STATUS_RECALL_REQUESTED = "recallRequested"

RETURN_CODES = ("insufficient_funds", "account_closed", "unauthorised",
                "notification_of_change")
RETURN_INSUFFICIENT = "insufficient_funds"
RETURN_ACCOUNT_CLOSED = "account_closed"

LEDGER_CLASSES = ("customer_deposit", "in_transit", "fee_income",
                  "interest_expense", "card_authorisation_hold",
                  "returns_suspense", "partner_bank_settlement",
                  "unmatched_clearing", "rounding_residual")
CLASS_IN_TRANSIT = "in_transit"
CLASS_RETURNS_SUSPENSE = "returns_suspense"
CLASS_UNMATCHED = "unmatched_clearing"
CLASS_RESIDUAL = "rounding_residual"
CLASS_HOLD = "card_authorisation_hold"

BREAK_KINDS = ("timing", "amount", "missing", "unexpected")

FEE_WIRE_DOMESTIC = "wire_outgoing_domestic"
FEE_WIRE_DOMESTIC_MINOR = 1500
FEE_WIRE_INTERNATIONAL = "wire_outgoing_international"
FEE_WIRE_INTERNATIONAL_MINOR = 2500
FEE_ACH = "ach_outgoing"
FEE_ACH_MINOR = 0
FEE_REALTIME = "realtime_outgoing"
FEE_REALTIME_MINOR = 0
FEE_CHEQUE = "cheque_outgoing"
FEE_CHEQUE_MINOR = 150
FEE_CARD_REPLACEMENT = "card_replacement"
FEE_CARD_REPLACEMENT_MINOR = 500
FEE_MAINTENANCE = "monthly_maintenance"
FEE_MAINTENANCE_MINOR = 0
FEE_EFFECTIVE_FROM = "2026-09-01"
FEES = {
    FEE_WIRE_DOMESTIC: FEE_WIRE_DOMESTIC_MINOR,
    FEE_WIRE_INTERNATIONAL: FEE_WIRE_INTERNATIONAL_MINOR,
    FEE_ACH: FEE_ACH_MINOR,
    FEE_REALTIME: FEE_REALTIME_MINOR,
    FEE_CHEQUE: FEE_CHEQUE_MINOR,
    FEE_CARD_REPLACEMENT: FEE_CARD_REPLACEMENT_MINOR,
    FEE_MAINTENANCE: FEE_MAINTENANCE_MINOR,
}

FOOTNOTE_MARKERS = (1, 2, 3, 4, 5, 6, 7)
APPLY_MINUTES = "10"
YIELD_RATE = "4.20%"
YIELD_BASIS_POINTS = 420
YIELD_DAY_COUNT = 365
YIELD_AS_OF = "2026-09-01"
CUSTOMER_COUNT = "200,000"
INSURED_LIMIT_MINOR = 25000000

POLICY_VERSION = 1
POLICY_THRESHOLD_MINOR = 1000000
POLICY_REQUIRED_APPROVALS = 2
STEP_UP_ACTIONS = ("add_recipient", "first_payment_to_recipient",
                   "change_approval_policy", "change_payout_details",
                   "add_user", "large_payment")

CUTOFF_ACH = "16:30"
CUTOFF_WIRE = "15:00"
CUTOFF_TIMEZONE = "America/New_York"
HOLIDAY_ONE = "2026-11-26"
HOLIDAY_TWO = "2026-12-25"

HOLD_EXPIRY_RESTAURANT_DAYS = 2
HOLD_EXPIRY_HOTEL_DAYS = 31
HOLD_EXPIRY_DEFAULT_DAYS = 7
MERCHANT_RESTAURANT = "restaurant"
MERCHANT_HOTEL = "hotel"

CARD_AUTHORISATION_MINOR = 4000
CARD_CLEARING_MINOR = 4800

READ_LIMIT_PER_MINUTE = 120
PAYMENT_LIMIT_PER_MINUTE = 10
IDEMPOTENCY_RETENTION_HOURS = 24
IDEMPOTENCY_HEADER = "Idempotency-Key"

STATEMENT_PERIOD = "2026-08"
DRAFT_PAGE_TITLE = "Treasury sweep explained"
DRAFT_PAGE_ROUTE = "/products/treasury-sweep"
PAGE_STATE_DRAFT = "draft"
PAGE_STATE_PUBLISHED = "published"

OBJECT_KEY_PREFIX = "vault"
OBJECT_KINDS = ("statement", "formation", "receipt", "export")

RECONCILIATION_RUN_DATE = "2026-09-15"

WORDMARK = "A U R E L I A"
DISCLOSURE = ("Aurelia is a fintech company, not an FDIC-insured bank. "
              "Banking services provided through Northgate Bank and "
              "Talbot National, Members FDIC.")
ANNOUNCEMENT = "Real-time payments are here - instant, free, 24/7/365."
NAV_ITEMS = ("Products", "Solutions", "Resources", "About", "Pricing")
HOME_TITLE = ("Online Business Banking For Startups, Small Businesses & "
              "Scaling Companies")
DEVELOPER_TITLE = ("Full Banking API, Terminal-Native CLI & AI-Ready MCP "
                   "Server | Aurelia")
SUPPORT_TITLE = "FAQs | Pricing, Moving Your Money & More | Aurelia"
SERVER_ERROR_TITLE = "500: Internal Server Error"
HERO_HEADLINE = "Radically different banking"
HERO_FIELD = "Enter your email"
HERO_PRIMARY = "Open account"
HERO_SECONDARY = "Launch demo"
FEATURE_HEADING = "Get started fast. And never stop moving."
DEVELOPER_HEADLINE = "Programmable finances for developers & agents"
CLI_CONTROL = "Install CLI"
SKIP_LINK = "Skip to main content"

RESOURCES = {
    "cards": "List debit and credit cards for an account",
    "categories": "List expense categories",
    "credit": "List credit accounts",
    "customers": "Create, update, and manage customers",
    "events": "List and inspect API events",
    "invoices": "Create, update, and manage invoices",
    "org": "View organization details",
    "payments": "Send money, request approvals, and transfer between accounts",
    "recipients": "Add, update, and manage payment recipients",
    "safes": "List and download SAFE agreements",
    "statements": "Download account statements as PDF",
    "transactions": "Search, update, and attach files to transactions",
    "treasury": "View treasury accounts",
    "users": "List and view organization team members",
    "webhooks": "Set up and manage webhook endpoints",
}

PUBLIC_ROUTES = (
    "/", "/pricing", "/products/accounts", "/products/payments",
    "/products/cards", "/products/treasury", "/products/spend-controls",
    "/products/invoicing", "/products/capital", "/solutions/stage",
    "/solutions/sector", "/solutions/role", "/resources/blog",
    "/resources/guides", "/resources/customers", "/faq", "/developers",
    "/about/company", "/about/careers", "/about/security", "/legal/terms",
    "/legal/privacy", "/legal/deposit-agreement", "/legal/disclosures",
    "/legal/fees", "/legal/complaints", "/legal/partner-banks",
)
CLAIMING_ROUTES = ("/", "/pricing", "/products/accounts", "/products/payments",
                   "/products/treasury", "/developers", "/faq")
CAMPAIGN_PATHS = ("/as", "/gs", "/pb", "/a/b", "/a/i", "/g/d", "/wa")
PRODUCT_ROUTES = ("/app", "/app/accounts", "/app/transactions", "/app/payments",
                  "/app/approvals", "/app/statements", "/app/audit")
STUDIO_ROUTES = ("/studio", "/studio/pages", "/studio/fees",
                 "/studio/footnotes")

CORRELATION_FIELD = "request_id"

SUCCESS_STATUSES = (200, 201, 202)
REDIRECT_STATUSES = (301, 302, 307, 308)
REFUSAL_STATUSES = (400, 401, 403, 404, 409, 422, 429)
DENIAL_STATUSES = (401, 403, 404)
NOT_FOUND_STATUSES = (404,)
CONFLICT_STATUSES = (409, 422)
RATE_LIMITED_STATUSES = (429,)

SETTLE_SECONDS = 0.4
POLL_BUDGET_SECONDS = 25.0
CONCURRENT_POSTINGS = 200
CONCURRENT_IDEMPOTENT_CALLS = 50
NARROW_VIEWPORT_WIDTH = 390
WIDE_VIEWPORT_WIDTH = 1280
CONTRAST_BAR = 4.5
LARGE_TEXT_CONTRAST_BAR = 3.0
RESPONSIVE_TIERS = 6


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned pause, for an effect the app writes just after replying."""
    time.sleep(seconds)


def poll_until(predicate, budget: float = POLL_BUDGET_SECONDS):
    """Bounded polling on a monotonic clock. Returns the last value the predicate saw."""
    deadline = time.monotonic() + budget
    value = predicate()
    while not value and time.monotonic() < deadline:
        settle()
        value = predicate()
    return value


def unique_suffix() -> str:
    return uuid.UUID(bytes=os.urandom(16), version=4).hex[:10]


def idempotency_key() -> str:
    return f"probe-{unique_suffix()}"


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code} :: {response.text[:400]}")


def minor_to_decimal(minor: int) -> str:
    sign = "-" if minor < 0 else ""
    value = abs(minor)
    return f"{sign}{value // 100}.{value % 100:02d}"


def relative_luminance(rgb: tuple[float, float, float]) -> float:
    channels = []
    for raw in rgb:
        channel = raw / 255.0
        channels.append(channel / 12.92 if channel <= 0.03928
                        else ((channel + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(first: tuple[float, float, float],
                   second: tuple[float, float, float]) -> float:
    one = relative_luminance(first)
    two = relative_luminance(second)
    lighter, darker = max(one, two), min(one, two)
    return (lighter + 0.05) / (darker + 0.05)


def parse_rgb(value: str) -> tuple[float, float, float]:
    numbers = [float(part) for part in
               value.replace("rgba", "").replace("rgb", "")
                    .strip("() ").split(",")[:3]]
    return (numbers[0], numbers[1], numbers[2])


class Session:
    """One signed-in or anonymous caller against the app's own API."""

    def __init__(self, token: str | None = None, email: str | None = None) -> None:
        self.token = token
        self.email = email
        self._cookies = httpx.Cookies()

    def _client(self) -> httpx.Client:
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        return httpx.Client(base_url=appclient.api_base(), timeout=30.0,
                            headers=headers, cookies=self._cookies)

    def request(self, method: str, path: str, body: dict | None = None,
                params: dict | None = None,
                headers: dict | None = None) -> httpx.Response:
        with self._client() as client:
            response = client.request(method, path, json=body, params=params,
                                      headers=headers or {})
        self._cookies.update(response.cookies)
        return response

    def get(self, path: str, **params: Any) -> httpx.Response:
        return self.request("GET", path,
                            params={k: v for k, v in params.items() if v is not None})

    def post(self, path: str, body: dict | None = None,
             key: str | None = None) -> httpx.Response:
        headers = {IDEMPOTENCY_HEADER: key} if key else {}
        return self.request("POST", path, body=body, headers=headers)

    def patch(self, path: str, body: dict | None = None) -> httpx.Response:
        return self.request("PATCH", path, body=body)

    def delete(self, path: str) -> httpx.Response:
        return self.request("DELETE", path)

    def accounts(self) -> httpx.Response:
        return self.get("/accounts")

    def balance(self, account_id: Any, as_of: str | None = None) -> httpx.Response:
        return self.get(f"/accounts/{account_id}/balance", as_of=as_of)

    def transactions(self, **params: Any) -> httpx.Response:
        return self.get("/transactions", **params)

    def payments(self, **params: Any) -> httpx.Response:
        return self.get("/payments", **params)

    def create_payment(self, body: dict, key: str | None = None) -> httpx.Response:
        return self.post("/payments", body, key=key or idempotency_key())

    def approve_payment(self, payment_id: Any, note: str = "approved") -> httpx.Response:
        return self.post(f"/payments/{payment_id}/approve", {"note": note})

    def amend_payment(self, payment_id: Any, body: dict) -> httpx.Response:
        return self.patch(f"/payments/{payment_id}", body)

    def recall_payment(self, payment_id: Any) -> httpx.Response:
        return self.post(f"/payments/{payment_id}/recall", {})

    def recipients(self) -> httpx.Response:
        return self.get("/recipients")

    def create_recipient(self, body: dict) -> httpx.Response:
        return self.post("/recipients", body)

    def cards(self) -> httpx.Response:
        return self.get("/cards")

    def authorise_card(self, card_id: Any, body: dict) -> httpx.Response:
        return self.post(f"/cards/{card_id}/authorisations", body)

    def clear_card(self, card_id: Any, body: dict) -> httpx.Response:
        return self.post(f"/cards/{card_id}/clearings", body)

    def statements(self) -> httpx.Response:
        return self.get("/statements")

    def statement_content(self, statement_id: Any) -> httpx.Response:
        return self.get(f"/statements/{statement_id}/content")

    def document_content(self, document_id: Any) -> httpx.Response:
        return self.get(f"/documents/{document_id}/content")

    def reconciliation(self, run_date: str) -> httpx.Response:
        return self.get("/reconciliation", run_date=run_date)

    def audit(self, **params: Any) -> httpx.Response:
        return self.get("/audit", **params)

    def events(self, **params: Any) -> httpx.Response:
        return self.get("/events", **params)

    def fees(self) -> httpx.Response:
        return self.get("/fees")

    def treasury(self) -> httpx.Response:
        return self.get("/treasury")

    def create_token(self, body: dict) -> httpx.Response:
        return self.post("/tokens", body)

    def revoke_token(self, token_id: Any) -> httpx.Response:
        return self.delete(f"/tokens/{token_id}")

    def step_up(self, action: str) -> httpx.Response:
        return self.post("/auth/step-up", {"password": PASSWORD, "action": action})


class Store:
    """Domain reads over the persisted rows the brief pins by name."""

    def __init__(self, backend: Any) -> None:
        self.backend = backend

    def query(self, sql: str, params: tuple = ()) -> list[dict]:
        return self.backend.query(sql, params)

    def count(self, table: str, **where: Any) -> int:
        return self.backend.count(table, **where)

    def rows(self, table: str, limit: int | None = None, **where: Any) -> list[dict]:
        return self.backend.rows(table, limit=limit, **where)

    def organisation(self, slug: str) -> dict | None:
        found = self.query("SELECT * FROM organisation WHERE slug = %s", (slug,))
        return found[0] if found else None

    def account_by_email(self, email: str) -> dict | None:
        found = self.query(
            "SELECT * FROM account WHERE lower(email) = lower(%s)", (email,))
        return found[0] if found else None

    def bank_account(self, name: str) -> dict | None:
        found = self.query("SELECT * FROM bank_account WHERE name = %s", (name,))
        return found[0] if found else None

    def ledger_account(self, account_class: str) -> dict | None:
        found = self.query(
            "SELECT * FROM ledger_account WHERE class = %s LIMIT 1", (account_class,))
        return found[0] if found else None

    def entries_for(self, ledger_account_id: Any) -> list[dict]:
        return self.query(
            "SELECT * FROM entry WHERE ledger_account_id = %s", (ledger_account_id,))

    def derived_balance(self, ledger_account_id: Any) -> int:
        total = 0
        for row in self.entries_for(ledger_account_id):
            amount = int(row["amount_minor"])
            total += amount if row["direction"] == "credit" else -amount
        return total

    def posting_is_balanced(self, posting_id: Any) -> bool:
        debit = credit = 0
        for row in self.query("SELECT * FROM entry WHERE posting_id = %s",
                              (posting_id,)):
            amount = int(row["amount_minor"])
            if row["direction"] == "debit":
                debit += amount
            else:
                credit += amount
        return debit == credit

    def payment(self, external_id: str) -> dict | None:
        found = self.query("SELECT * FROM payment WHERE external_id = %s",
                           (external_id,))
        return found[0] if found else None

    def page(self, route: str) -> dict | None:
        found = self.query("SELECT * FROM page WHERE route = %s", (route,))
        return found[0] if found else None

    def fee(self, code: str) -> dict | None:
        found = self.query("SELECT * FROM fee WHERE code = %s", (code,))
        return found[0] if found else None

    def statement(self, period: str) -> dict | None:
        found = self.query("SELECT * FROM statement WHERE period = %s", (period,))
        return found[0] if found else None

    def recipient(self, external_id: str) -> dict | None:
        found = self.query("SELECT * FROM recipient WHERE external_id = %s",
                           (external_id,))
        return found[0] if found else None

    def audit_chain(self, organisation_id: Any) -> list[dict]:
        return self.query(
            "SELECT * FROM audit_entry WHERE organisation_id = %s ORDER BY id",
            (organisation_id,))



APP_DB_ROLE = "deku_app"
BINARY_ASSET_SUFFIXES = (".woff", ".woff2", ".ttf", ".otf", ".png", ".jpg",
                         ".jpeg", ".gif", ".webp", ".svgz", ".mp4", ".lottie")


@pytest.fixture(scope="session")
def store() -> Store:
    return Store(capabilities.make_backend())


@pytest.fixture(scope="session")
def objects():
    return capabilities.make_store()


@pytest.fixture(scope="session")
def app_base() -> str:
    return appclient.api_base()


@pytest.fixture(scope="session")
def site_base() -> str:
    return appclient.app_url()


@pytest.fixture()
def anonymous() -> Session:
    return Session()


@pytest.fixture()
def editor() -> Session:
    return Session(appclient.login(EDITOR_EMAIL, PASSWORD), EDITOR_EMAIL)


@pytest.fixture()
def owner() -> Session:
    return Session(appclient.login(OWNER_EMAIL, PASSWORD), OWNER_EMAIL)


@pytest.fixture()
def admin() -> Session:
    return Session(appclient.login(ADMIN_EMAIL, PASSWORD), ADMIN_EMAIL)


@pytest.fixture()
def approver() -> Session:
    return Session(appclient.login(APPROVER_EMAIL, PASSWORD), APPROVER_EMAIL)


@pytest.fixture()
def initiator() -> Session:
    return Session(appclient.login(INITIATOR_EMAIL, PASSWORD), INITIATOR_EMAIL)


@pytest.fixture()
def bookkeeper() -> Session:
    return Session(appclient.login(BOOKKEEPER_EMAIL, PASSWORD), BOOKKEEPER_EMAIL)


@pytest.fixture()
def cardholder() -> Session:
    return Session(appclient.login(CARDHOLDER_EMAIL, PASSWORD), CARDHOLDER_EMAIL)


@pytest.fixture()
def owner_two() -> Session:
    return Session(appclient.login(OWNER2_EMAIL, PASSWORD), OWNER2_EMAIL)


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as driver:
        engine = driver.chromium.launch()
        yield engine
        engine.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context(viewport={"width": WIDE_VIEWPORT_WIDTH,
                                            "height": 900})
    opened = context.new_page()
    yield opened
    context.close()


def payload_of(response: httpx.Response) -> dict:
    body = response.json()
    assert isinstance(body, dict), f"expected a JSON object: {describe(response)}"
    return body


def rows_of(response: httpx.Response) -> list:
    body = response.json()
    assert isinstance(body, list), (
        f"a list endpoint returns a top-level JSON array: {describe(response)}")
    return body


def field_of(payload: dict, *names: str) -> Any:
    for name in names:
        if name in payload:
            return payload[name]
    raise AssertionError(f"none of {names} present in {sorted(payload)[:20]}")


def first_operating_account(session: Session) -> dict:
    response = session.accounts()
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    for row in rows_of(response):
        if row.get("name") == ACCOUNT_OPERATING:
            return row
    raise AssertionError(f"{ACCOUNT_OPERATING} is absent from {describe(response)}")


def payment_body(account_id: Any, recipient_id: str, amount: str,
                 rail: str = RAIL_ACH, memo: str = "probe payment") -> dict:
    return {
        "account_id": account_id,
        "recipient_id": recipient_id,
        "amount": amount,
        "currency": CURRENCY_WIRE,
        "payment_method": rail,
        "external_memo": memo,
    }
