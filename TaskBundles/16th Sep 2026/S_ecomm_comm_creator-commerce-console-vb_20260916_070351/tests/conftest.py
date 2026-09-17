"""Task fixtures for deku/creator-commerce-console-vb.

Implementation agnostic: nothing here assumes the agent's framework, file
layout, ORM or module names. The only assumptions are the App Contract and what
instruction.md pinned literally, which is the route set, the `access_token`
login key, the seeded accounts, the seeded catalog, the fee schedule, the tax
table, the table names of `## Data model`, and the receipt subject prefix.

Provider agnostic: every domain helper is composed from the generic primitives
in capabilities.py, never from a provider SDK. Swapping the backend, email or
payments slot replaces an adapter rather than this file.
"""

from __future__ import annotations

import os
import time
from decimal import Decimal, ROUND_HALF_UP

import pytest
from _shapes import items
from appclient import api_base, client, login, seeded_password
from capabilities import Backend, Inbox, Payments, make_backend, make_inbox, make_payments

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 30.0
POLL_INTERVAL_SECONDS = 0.5

CORPUS_PASSWORD = "deku-demo-pw-2026"

CREATOR_EMAIL = "creator@example.com"
READER_EMAIL = "buyer@example.com"
READER2_EMAIL = "buyer2@example.com"

CREATOR_NAME = "Marlowe Quill"
READER_NAME = "Ines Calder"
READER2_NAME = "Tobias Renn"

ACCOUNT_HANDLE = "marlowe-quill"
MOR_ENTITY = "Handsel Commerce Ltd"
PAYOUT_CURRENCY = "usd"

FIELD_NOTES = "field-notes-vol-one"
LANTERN_KIT = "lantern-press-kit"
TIDE_TABLES = "tide-tables-draft"

FIELD_NOTES_NAME = "Field Notes Volume One"
LANTERN_KIT_NAME = "Lantern Press Kit"
TIDE_TABLES_NAME = "Tide Tables Draft"

TIER_STANDARD = "standard"
TIER_STUDIO = "studio"
TIER_STANDARD_NAME = "Standard"
TIER_STUDIO_NAME = "Studio"

FIELD_NOTES_STANDARD_MINOR = 2400
FIELD_NOTES_STUDIO_MINOR = 5600
LANTERN_KIT_STANDARD_MINOR = 1000
TIDE_TABLES_STANDARD_MINOR = 1800

CHANNEL_DIRECT = "direct"
CHANNEL_MARKETPLACE = "marketplace"

DIRECT_RATE_BPS = 1000
DIRECT_FIXED_MINOR = 30
MARKETPLACE_RATE_BPS = 2000
MARKETPLACE_FIXED_MINOR = 0
PAYMENT_RATE_BPS = 290
PAYMENT_FIXED_MINOR = 30
FEE_SCHEDULE_VERSION = 1

JURISDICTION_TAXED = "IE"
JURISDICTION_ZERO = "US"
TAXED_RATE_BPS = 1900
ZERO_RATE_BPS = 0

OPEN_CODE = "LAUNCH20"
OPEN_CODE_BPS = 2000
OPEN_CODE_MAX_USES = 5
OPEN_CODE_MAX_PER_READER = 1
CLOSED_CODE = "EXPIRED10"
CLOSED_CODE_BPS = 1000

WORKED_SUBTOTAL_MINOR = 2400
WORKED_DISCOUNT_MINOR = 480
WORKED_TAX_MINOR = 365
WORKED_TOTAL_MINOR = 2285
WORKED_PLATFORM_FEE_MINOR = 222
WORKED_PAYMENT_FEE_MINOR = 96
WORKED_AFFILIATE_MINOR = 0
WORKED_NET_MINOR = 1602
WORKED_INVOICE_DECIMAL = "22.85"

ZERO_RATED_TOTAL_MINOR = 2400
ZERO_RATED_PLATFORM_FEE_MINOR = 480
ZERO_RATED_PAYMENT_FEE_MINOR = 100
ZERO_RATED_NET_MINOR = 1820

MARKETPLACE_PLATFORM_FEE_MINOR = 384
MARKETPLACE_NET_MINOR = 1440

ACCOUNT_RECEIVABLE = "1100"
ACCOUNT_CREATOR_PAYABLE = "2000"
ACCOUNT_TAX_PAYABLE = "2100"
ACCOUNT_PLATFORM_REVENUE = "4000"
ACCOUNT_PAYMENT_EXPENSE = "5000"
SEEDED_ACCOUNT_CODES = (
    ACCOUNT_RECEIVABLE,
    ACCOUNT_CREATOR_PAYABLE,
    ACCOUNT_TAX_PAYABLE,
    ACCOUNT_PLATFORM_REVENUE,
    ACCOUNT_PAYMENT_EXPENSE,
)

TYPE_ASSET = "asset"
TYPE_LIABILITY = "liability"
TYPE_REVENUE = "revenue"
TYPE_EXPENSE = "expense"

DIRECTION_DEBIT = "debit"
DIRECTION_CREDIT = "credit"

STATE_DRAFT = "draft"
STATE_PUBLISHED = "published"
STATE_UNPUBLISHED = "unpublished"
SESSION_OPEN = "open"
SESSION_CONFIRMED = "confirmed"
SESSION_REFUSED = "refused"
SESSION_EXPIRED = "expired"
ENTITLEMENT_ACTIVE = "active"
ENTITLEMENT_REVOKED = "revoked"

ORDER_NUMBER_PREFIX = "HS-"
FIRST_ORDER_NUMBER = "HS-00001"

READER_EXTERNAL_KEY = "handsel-ines-calder"
READER2_EXTERNAL_KEY = "handsel-tobias-renn"

RECEIPT_SUBJECT_PREFIX = "Handsel receipt: "
DECOY_FIELD = "company_website"
TOKEN_KEY = "access_token"

CREATOR_ONLY_ROUTES = (
    "/orders",
    "/ledger/accounts",
    "/ledger/entries",
    "/ledger/trial-balance",
    "/discount-codes",
)

REFUSED_STATUSES = (400, 403, 409, 422)
DENIED_STATUSES = (401, 403, 404)
ABSENT_STATUSES = (404,)
OK_STATUSES = (200, 201)


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned sleep: give an unwanted side effect a fair chance to land."""
    time.sleep(seconds)


def poll_until(predicate, deadline_seconds: float = POLL_DEADLINE_SECONDS):
    """Poll a predicate to a monotonic deadline. Returns the last value seen."""
    limit = time.monotonic() + deadline_seconds
    seen = None
    while time.monotonic() < limit:
        seen = predicate()
        if seen:
            return seen
        settle(POLL_INTERVAL_SECONDS)
    return seen


def round_half_up(numerator: int, rate_bps: int) -> int:
    """The brief's one rounding rule, applied to a basis-point rate."""
    value = Decimal(numerator) * Decimal(rate_bps) / Decimal(10000)
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def expected_decomposition(unit_minor: int, quantity: int, discount_bps: int,
                           tax_bps: int, rate_bps: int, fixed_minor: int) -> dict:
    """The brief's arithmetic, restated once so a test never recomputes it inline."""
    subtotal = unit_minor * quantity
    discount = round_half_up(subtotal, discount_bps)
    taxable = subtotal - discount
    tax = round_half_up(taxable, tax_bps)
    total = taxable + tax
    platform_fee = round_half_up(taxable, rate_bps) + fixed_minor
    payment_fee = round_half_up(total, PAYMENT_RATE_BPS) + PAYMENT_FIXED_MINOR
    affiliate_fee = 0
    net = subtotal - discount - platform_fee - payment_fee - affiliate_fee
    return {
        "subtotal_minor": subtotal,
        "discount_minor": discount,
        "tax_minor": tax,
        "total_minor": total,
        "platform_fee_minor": platform_fee,
        "payment_fee_minor": payment_fee,
        "affiliate_fee_minor": affiliate_fee,
        "net_minor": net,
    }


def probe_email() -> str:
    return "probe-" + os.urandom(6).hex() + "@example.com"


def probe_key() -> str:
    return "probe-" + os.urandom(8).hex()


def probe_permalink() -> str:
    return "probe-" + os.urandom(6).hex()


def body_excerpt(response) -> str:
    return response.text[:400]


def where(response, what: str) -> str:
    """One failure-message shape: the anchor, the request, the status, the body."""
    request = getattr(response, "request", None)
    method = getattr(request, "method", "?")
    url = str(getattr(request, "url", api_base()))
    return (f"{what}: {method} {url} returned {response.status_code} "
            f"with body {body_excerpt(response)!r}")


def as_list(payload) -> list:
    return items(payload)


def minor(value) -> int:
    """Read a money field whichever pinned shape the app returns it in."""
    if isinstance(value, dict):
        value = value.get("amount_minor", value.get("amount"))
    return int(value)


def find_by(rows: list, key: str, value) -> dict | None:
    for row in rows:
        if isinstance(row, dict) and row.get(key) == value:
            return row
    return None


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


def _token(email: str) -> str:
    return login(email, seeded_password("SEED_PASSWORD", CORPUS_PASSWORD))


@pytest.fixture()
def creator_client():
    with client(_token(CREATOR_EMAIL)) as c:
        yield c


@pytest.fixture()
def reader_client():
    with client(_token(READER_EMAIL)) as c:
        yield c


@pytest.fixture()
def reader2_client():
    with client(_token(READER2_EMAIL)) as c:
        yield c


def fresh_client(email: str):
    return client(_token(email))


class HandselStore:
    """Domain queries composed from the generic capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def user_by_email(self, email: str) -> dict | None:
        return self._b.one("users", email=email)

    def count_users(self, email: str) -> int:
        return self._b.count("users", email=email)

    def account_row(self) -> dict | None:
        return self._b.one("accounts", handle=ACCOUNT_HANDLE)

    def users_with_role(self, role: str) -> list[dict]:
        return self._b.rows("users", role=role)

    def count_products(self, permalink: str) -> int:
        return self._b.count("products", permalink=permalink)

    def product_by_permalink(self, permalink: str) -> dict | None:
        return self._b.one("products", permalink=permalink)

    def tiers_for(self, product_id) -> list[dict]:
        return self._b.rows("tiers", product_id=product_id)

    def order_by_number(self, number: str) -> dict | None:
        return self._b.one("orders", number=number)

    def orders_for_reader(self, reader_id) -> list[dict]:
        return self._b.rows("orders", reader_id=reader_id)

    def all_orders(self) -> list[dict]:
        return self._b.rows("orders")

    def count_orders_by_key(self, key: str) -> int:
        return self._b.count("orders", idempotency_key=key)

    def sessions_for_reader(self, reader_id) -> list[dict]:
        return self._b.rows("checkout_sessions", reader_id=reader_id)

    def invoice_for_order(self, order_id) -> dict | None:
        return self._b.one("invoices", order_id=order_id)

    def all_invoices(self) -> list[dict]:
        return self._b.rows("invoices")

    def billing_account(self, external_key: str) -> dict | None:
        return self._b.one("billing_accounts", external_key=external_key)

    def count_billing_accounts(self, external_key: str) -> int:
        return self._b.count("billing_accounts", external_key=external_key)

    def entitlements_for(self, reader_id) -> list[dict]:
        return self._b.rows("entitlements", reader_id=reader_id)

    def entitlements_for_order(self, order_id) -> list[dict]:
        return self._b.rows("entitlements", order_id=order_id)

    def access_events(self, entitlement_id) -> list[dict]:
        return self._b.rows("access_events", entitlement_id=entitlement_id)

    def ledger_accounts(self) -> list[dict]:
        return self._b.rows("ledger_accounts")

    def ledger_account_by_code(self, code: str) -> dict | None:
        return self._b.one("ledger_accounts", code=code)

    def ledger_account_by_id(self, account_id) -> dict | None:
        return self._b.one("ledger_accounts", id=account_id)

    def legs_by_account_code(self, entry_id) -> dict:
        """An entry's legs keyed by the account code each one posts to."""
        out: dict = {}
        for row in self.postings_for(entry_id):
            account = self.ledger_account_by_id(row.get("ledger_account_id"))
            code = str(account.get("code")) if account else "?"
            out.setdefault(code, []).append(row)
        return out

    def ledger_entry_by_key(self, key: str) -> dict | None:
        return self._b.one("ledger_entries", idempotency_key=key)

    def ledger_entries_for_source(self, source_id) -> list[dict]:
        return self._b.rows("ledger_entries", source_id=source_id)

    def all_ledger_entries(self) -> list[dict]:
        return self._b.rows("ledger_entries")

    def postings_for(self, entry_id) -> list[dict]:
        return self._b.rows("ledger_postings", entry_id=entry_id)

    def all_postings(self) -> list[dict]:
        return self._b.rows("ledger_postings")

    def discount_code(self, code: str) -> dict | None:
        return self._b.one("discount_codes", code=code)

    def fee_schedule(self, channel: str) -> dict | None:
        return self._b.one("fee_schedules", channel=channel)

    def tax_rate(self, jurisdiction: str) -> dict | None:
        return self._b.one("tax_rates", jurisdiction=jurisdiction)

    def trial_balance_minor(self) -> int:
        total = 0
        for row in self.all_postings():
            amount = int(row.get("amount_minor", 0))
            total += amount if row.get("direction") == DIRECTION_DEBIT else -amount
        return total


@pytest.fixture(scope="session")
def store() -> HandselStore:
    return HandselStore(make_backend())


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    return make_inbox()


@pytest.fixture(scope="session")
def payments() -> Payments:
    return make_payments()


def wait_for_email(inbox_handle: Inbox, address: str, subject_contains: str):
    """Bounded poll for a message, routed through settle()."""
    return poll_until(lambda: inbox_handle.find(address, subject_contains))


def wait_for_invoice(payments_handle: Payments, amount_minor: int,
                     currency: str = PAYOUT_CURRENCY):
    """Bounded poll for an invoice of an exact amount, routed through settle()."""
    return poll_until(lambda: payments_handle.find_charge(amount_minor, currency))


def open_session(http, permalink: str, tier_code: str = TIER_STANDARD,
                 quantity: int = 1, channel: str = CHANNEL_DIRECT,
                 key: str | None = None):
    """Open a checkout session through the pinned route, with a fresh key."""
    return http.post("/checkout/sessions", json={
        "permalink": permalink,
        "tier_code": tier_code,
        "quantity": quantity,
        "attribution_channel": channel,
        "idempotency_key": key or probe_key(),
    })


def session_id_of(payload) -> str:
    body = payload if isinstance(payload, dict) else {}
    for key in ("id", "session_id", "checkout_session_id"):
        if body.get(key):
            return str(body[key])
    data = body.get("data")
    if isinstance(data, dict):
        for key in ("id", "session_id", "checkout_session_id"):
            if data.get(key):
                return str(data[key])
    return ""


def order_number_of(payload) -> str:
    body = payload if isinstance(payload, dict) else {}
    for key in ("number", "order_number"):
        if body.get(key):
            return str(body[key])
    for nest in ("order", "data"):
        inner = body.get(nest)
        if isinstance(inner, dict):
            for key in ("number", "order_number"):
                if inner.get(key):
                    return str(inner[key])
    return ""


def confirm_session(http, session_id: str, key: str | None = None):
    return http.post(f"/checkout/sessions/{session_id}/confirm",
                     json={"idempotency_key": key or probe_key()})


def buy_once(http, permalink: str, tier_code: str = TIER_STANDARD,
             channel: str = CHANNEL_DIRECT, code: str | None = None):
    """The whole pinned purchase path, returned as the confirm response."""
    opened = open_session(http, permalink, tier_code=tier_code, channel=channel)
    assert opened.status_code in OK_STATUSES, where(
        opened, f"opening a checkout session for {permalink}")
    session_id = session_id_of(opened.json())
    assert session_id, (
        f"opening a checkout session for {permalink} returned no session "
        f"identifier: {body_excerpt(opened)!r}")
    if code:
        applied = http.post(f"/checkout/sessions/{session_id}/discounts",
                            json={"code": code})
        assert applied.status_code in OK_STATUSES, where(
            applied, f"applying the discount code {code}")
    return confirm_session(http, session_id)
