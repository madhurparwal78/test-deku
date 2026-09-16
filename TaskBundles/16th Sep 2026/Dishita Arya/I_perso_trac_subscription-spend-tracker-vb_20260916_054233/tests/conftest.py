"""Fixtures, pinned literals and helpers for Driplog.

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

OWNER_EMAIL = "user@example.com"
OWNER2_EMAIL = "user2@example.com"
OWNER_NAME = "Nadia Ferreira"
OWNER2_NAME = "Owen Mbeki"
OWNER_ZONE = "UTC"
OWNER2_ZONE = "America/New_York"

HOME_CURRENCY = "usd"
CURRENCY_EUR = "eur"
CURRENCY_GBP = "gbp"
CURRENCY_AED = "aed"
CURRENCY_JPY = "jpy"

RATE_AS_OF = "2026-09-15"
RATE_EUR = "1.0850"
RATE_GBP = "1.2640"
RATE_AED = "0.2723"
RATE_JPY = "0.006740"

CATEGORY_GROCERIES = "Groceries"
CATEGORY_LOANS = "Loans"
CATEGORY_CAFES = "Cafes & Dining"
CATEGORY_SHOPPING = "Shopping"
CATEGORY_HEALTH = "Health & Fitness"
CATEGORY_ENTERTAINMENT = "Entertainment"
CATEGORY_UTILITIES = "Utilities"
CATEGORY_STUDIO = "Studio"
BUILTIN_CATEGORIES = (
    CATEGORY_GROCERIES, CATEGORY_LOANS, CATEGORY_CAFES, CATEGORY_SHOPPING,
    CATEGORY_HEALTH, CATEGORY_ENTERTAINMENT, CATEGORY_UTILITIES,
)

DEMO_MONTH_MINOR = 126219
DEMO_YEAR_MINOR = 1514633
DEMO_DAY_MINOR = 4150
DEMO_SUBSCRIPTION_COUNT = 30

DEMO_CATEGORY_MONTH = {
    CATEGORY_GROCERIES: 36800,
    CATEGORY_LOANS: 32000,
    CATEGORY_CAFES: 16700,
    CATEGORY_SHOPPING: 12000,
    CATEGORY_HEALTH: 11019,
    CATEGORY_ENTERTAINMENT: 8900,
    CATEGORY_UTILITIES: 8800,
}
DEMO_CATEGORY_YEAR = {
    CATEGORY_GROCERIES: 441600,
    CATEGORY_LOANS: 384000,
    CATEGORY_CAFES: 200400,
    CATEGORY_SHOPPING: 144000,
    CATEGORY_HEALTH: 132233,
    CATEGORY_ENTERTAINMENT: 106800,
    CATEGORY_UTILITIES: 105600,
}
GROCERIES_YEAR_APPROX_MINOR = 442000

OWNER_MONTH_MINOR = 21180
OWNER_YEAR_MINOR = 254155
OWNER_DAY_MINOR = 696
OWNER_SUBSCRIPTION_COUNT = 6

OWNER2_MONTH_MINOR = 31159
OWNER2_YEAR_MINOR = 373910
OWNER2_DAY_MINOR = 1024
OWNER2_SUBSCRIPTION_COUNT = 9

FREE_CAP = 6
PREMIUM_MONTHLY_MINOR = 799
PREMIUM_YEARLY_MINOR = 2972
PREMIUM_TWELVE_MONTHS_MINOR = 9588
PREMIUM_SAVING_PERCENT = 69

SUB_HARVEST_BOX = "Harvest Box"
SUB_LUMEN_PLAY = "Lumen Play"
SUB_KETTLE_CLUB = "Kettle Club"
SUB_NORTHWIND_FIBRE = "Northwind Fibre"
SUB_VAULTLINE_BACKUP = "Vaultline Backup"
SUB_BASIN_LANE = "Basin Lane Fitness"
SUB_NORTHBRIDGE_AUTO = "Northbridge Auto"
SUB_CALM_CURRENT = "Calm Current"
SUB_THREAD_AND_LAST = "Thread & Last"
SUB_ROASTLINE_BEANS = "Roastline Beans"
SUB_CELLAR_AND_VINE = "Cellar & Vine"
SUB_RADIOLARK = "Radiolark"
SUB_PILATES_QUARTERLY = "Pilates Quarterly"
SUB_ATELIER_PRINT_CLUB = "Atelier Print Club"
SUB_STREAMIO_PREMIUM = "Streamio Premium"
SUB_TOKYO_PANTRY = "Tokyo Pantry"
SUB_PAPERCUT = "Papercut Stationery"
SUB_GRID_AND_EMBER = "Grid & Ember Energy"
SUB_FOLDSPACE_STUDIO = "Foldspace Studio"
SUB_KINOTECA = "Kinoteca"
EXPENSE_WINTER_TYRES = "Winter Tyres"

ANCHOR_NORTHBRIDGE = "2024-01-31"
ANCHOR_CALM_CURRENT = "2024-02-29"
ANCHOR_KETTLE_CLUB = "2026-03-31"
ANCHOR_ROASTLINE = "2026-05-02"
ANCHOR_HARVEST_BOX = "2026-02-04"

PRICE_NORTHBRIDGE_OLD_MINOR = 17500
PRICE_NORTHBRIDGE_NEW_MINOR = 18500
PRICE_CHANGE_EFFECTIVE_ON = "2026-04-01"
PRICE_LUMEN_PLAY_MINOR = 1099
PRICE_HARVEST_BOX_MINOR = 1799
PRICE_KETTLE_CLUB_MINOR = 1200
PRICE_NORTHWIND_MINOR = 5500
PRICE_VAULTLINE_MINOR = 7900
PRICE_BASIN_LANE_MINOR = 4900
PRICE_RADIOLARK_MINOR = 980
PRICE_STREAMIO_MINOR = 8400
PRICE_PAPERCUT_MINOR = 1800
PRICE_CELLAR_MINOR = 2490
PRICE_GRID_EMBER_IMPORT_MINOR = 131700

TRIAL_SUBSCRIPTION = SUB_FOLDSPACE_STUDIO
TRIAL_ENDS_ON = "2026-09-28"
TRIAL_POST_PRICE_MINOR = 1499
CANCELLED_SUBSCRIPTION = SUB_KINOTECA
CANCELLED_EFFECTIVE_ON = "2026-06-30"
ONE_TIME_AMOUNT_MINOR = 24000
ONE_TIME_ON = "2026-08-14"

CYCLE_WEEKLY = "weekly"
CYCLE_FORTNIGHTLY = "every_two_weeks"
CYCLE_MONTHLY = "monthly"
CYCLE_QUARTERLY = "quarterly"
CYCLE_HALF_YEARLY = "half_yearly"
CYCLE_YEARLY = "yearly"
CYCLE_EVERY_N_DAYS = "every_n_days"
ALL_CYCLES = (CYCLE_WEEKLY, CYCLE_FORTNIGHTLY, CYCLE_MONTHLY, CYCLE_QUARTERLY,
              CYCLE_HALF_YEARLY, CYCLE_YEARLY, CYCLE_EVERY_N_DAYS)

FILTER_ALL = "all"
FILTER_RECURRING = "recurring"
FILTER_ONE_TIME = "one-time"

OFFSET_DAY_BEFORE = "day_before"
OFFSET_SAME_DAY = "same_day"
OFFSET_THREE_DAYS = "three_days_before"
REMINDER_LOCAL_TIME = "09:00"
REMINDER_STATE_FIRED = "fired"
REMINDER_STATE_MISSED = "missed"
MISSED_AFTER_HOURS = 24

MODE_NEXT_RENEWAL = "next_renewal"
MODE_CORRECT_HISTORY = "correct_history"

CSV_HEADER = ("name,price_minor,currency,cycle,cycle_days,anchor_date,category,"
              "icon,colour,kind,status,cancelled_on,trial_ends_on,"
              "trial_price_minor,notes")

IMPORT_LINE_US = "Lumen Play - Monthly - Renews Jan 15, 2027 - $10.99"
IMPORT_LINE_GB = "Papercut Stationery - Every 90 days - Renews 17/02/2026 - GBP 18.00"
IMPORT_LINE_DE = "Cellar & Vine - Monatlich - Verlaengert am 05.12.2026 - 24,90 EUR"
IMPORT_LINE_FR = ("Grid & Ember Energy - Annuel - Renouvellement le 01/12/2026 - "
                  "1 317,00 EUR")
IMPORT_LINES = (IMPORT_LINE_US, IMPORT_LINE_GB, IMPORT_LINE_DE, IMPORT_LINE_FR)
IMPORT_EXPECTED = {
    SUB_LUMEN_PLAY: (PRICE_LUMEN_PLAY_MINOR, HOME_CURRENCY, "2027-01-15"),
    SUB_PAPERCUT: (PRICE_PAPERCUT_MINOR, CURRENCY_GBP, "2026-02-17"),
    SUB_CELLAR_AND_VINE: (PRICE_CELLAR_MINOR, CURRENCY_EUR, "2026-12-05"),
    SUB_GRID_AND_EMBER: (PRICE_GRID_EMBER_IMPORT_MINOR, CURRENCY_EUR, "2026-12-01"),
}
CONFIDENCE_LOW = "low"
DUPLICATE_MERGE = "Merge"
DUPLICATE_SKIP = "Skip"
DUPLICATE_PRICE_TOLERANCE_PERCENT = 5

RECEIPT_SAMPLES = {
    "receipt-01": ("Kettle Club", "2026-08-02", 1200, HOME_CURRENCY, CATEGORY_CAFES),
    "receipt-02": ("Harvest Box", "2026-08-05", 1799, HOME_CURRENCY, CATEGORY_GROCERIES),
    "receipt-03": ("Cafe Meridien", "2026-08-09", 5500, CURRENCY_AED, CATEGORY_CAFES),
    "receipt-04": ("Thread & Last", "2026-07-28", 6500, CURRENCY_GBP, CATEGORY_SHOPPING),
    "receipt-05": ("Northwind Fibre", "2026-08-01", 5500, HOME_CURRENCY, CATEGORY_UTILITIES),
}
RECEIPT_05_LINES = (("Fibre 300", 4500), ("Router rental", 1000))

UNDO_DEPTH = 50
UNDO_TOAST_SECONDS = 8
BIN_RETENTION_DAYS = 30
STRESS_SUBSCRIPTIONS = 1000
WIDGET_MAX_BYTES = 50 * 1024
WIDGET_FRESH_SECONDS = 60
TOUCH_TARGET_PX = 44

PAGE_SIZE_PARAM = "page_size"
PAGE_SIZE_DEFAULT = 20
PAGE_SIZE_MAX = 100
CURSOR_FIELD = "next_cursor"
MORE_FLAG = "has_more"

PUBLIC_ROUTES = ("/", "/blog", "/privacy", "/terms", "/sign-in", "/sign-up", "/demo")
APP_ROUTES = ("/app", "/app/import", "/app/ai-spend", "/app/insights", "/app/settings")
EDITOR_STEPS = ("/app/subscriptions/new/basics", "/app/subscriptions/new/cost",
                "/app/subscriptions/new/schedule")
WIDGET_ROUTES = ("/w/small", "/w/medium", "/w/lock", "/w/watch")
RESERVED_DIRECTORIES = (".browser_screenshots", ".downloads")
CREDENTIALS_PATH = "/app/USER_README.md"

COPY_NOT_FOUND = "Page not found"
COPY_HERO_OPENING = "All your subscriptions."
COPY_SPENDING_TITLE = "Your spending"
COPY_WHERE_MONEY_GOES = "Where your money goes"
COPY_PRICING_HEADLINE = "Free to start. Premium when you grow."
COPY_BLOG_TITLE = "Things we learned while staring."
COPY_FOOTER_RIGHTS = "(C) 2026 Driplog. All rights reserved."
COPY_PRIVACY_UPDATED = "Last updated: August 11, 2026"
COPY_TERMS_UPDATED = "Last updated: July 8, 2026"
COPY_EMPTY_LIST = "Nothing is tracked yet"
COPY_EMPTY_TIMELINE = "No charges scheduled"
COPY_SUPPORT_EMAIL = "hello@driplog.app"
COPY_SOCIAL_HANDLE = "@driplog"

BLOG_TITLES = (
    "Too Lazy to Type In Every Expense? Let AI Read Your Receipts",
    "How Much Do Your Subscriptions Really Cost Per Year?",
    "Forgot to Cancel a Free Trial? Here Is How to Stop Paying for It",
    "The Best Way to Track Subscriptions on iPhone in 2026",
    "Subscription Creep: Why Your Money Quietly Disappears Every Month",
)
PRIVACY_HEADINGS = (
    "Who We Are", "What We Collect", "AI Processing (AI Spend)",
    "Analytics & Advertising", "Third-Party Services", "Website Analytics",
    "Purchases", "Data Storage & Deletion", "Your Rights", "Contact",
)
TERMS_HEADINGS = (
    "Eligibility", "Subscription (Premium)", "AI Features", "Receipt Scanning",
    "Intellectual Property", "Trademarks", "Disclaimer",
    "Limitation of Liability", "Termination", "Contact",
)

SUCCESS_STATUSES = (200, 201, 202)
REFUSAL_STATUSES = (400, 401, 403, 404, 409, 422)
DENIAL_STATUSES = (401, 403)
NOT_FOUND_STATUSES = (404,)
CONFLICT_STATUSES = (409, 422)

SETTLE_SECONDS = 0.4
POLL_BUDGET_SECONDS = 25.0


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


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def batch_key() -> str:
    return f"probe-{unique_suffix()}"


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code} :: {response.text[:400]}")


def minor_to_decimal(minor: int) -> str:
    return f"{minor // 100}.{minor % 100:02d}"


def half_even(numerator: int, denominator: int) -> int:
    """Integer division rounding half to even, the rule the brief pins."""
    quotient, remainder = divmod(numerator, denominator)
    twice = remainder * 2
    if twice > denominator or (twice == denominator and quotient % 2 == 1):
        quotient += 1
    return quotient


class Session:
    """One signed-in owner, or an anonymous visitor when no token is held."""

    def __init__(self, token: str | None = None, email: str | None = None) -> None:
        self.token = token
        self.email = email

    def _client(self) -> httpx.Client:
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        return httpx.Client(base_url=appclient.api_base(), timeout=30.0,
                            headers=headers)

    def request(self, method: str, path: str, body: dict | None = None,
                params: dict | None = None,
                headers: dict | None = None) -> httpx.Response:
        with self._client() as client:
            return client.request(method, path, json=body, params=params,
                                  headers=headers or {})

    def get(self, path: str, **params: Any) -> httpx.Response:
        return self.request("GET", path,
                            params={k: v for k, v in params.items() if v is not None})

    def post(self, path: str, body: dict | None = None) -> httpx.Response:
        return self.request("POST", path, body=body)

    def patch(self, path: str, body: dict | None = None) -> httpx.Response:
        return self.request("PATCH", path, body=body)

    def delete(self, path: str) -> httpx.Response:
        return self.request("DELETE", path)

    def overview(self, filter_name: str | None = None) -> httpx.Response:
        return self.get("/app/overview", filter=filter_name)

    def subscriptions(self, **params: Any) -> httpx.Response:
        return self.get("/app/subscriptions", **params)

    def create_subscription(self, body: dict) -> httpx.Response:
        return self.post("/app/subscriptions", body)

    def charges(self, subscription_id: Any, start: str, end: str) -> httpx.Response:
        return self.get(f"/app/subscriptions/{subscription_id}/charges",
                        **{"from": start, "to": end})

    def reminder_schedule(self, start: str, end: str) -> httpx.Response:
        return self.get("/app/reminders/schedule", **{"from": start, "to": end})

    def run_reminders(self, as_of: str) -> httpx.Response:
        return self.post("/app/reminders/run", {"as_of": as_of})

    def reminder_timeline(self, **params: Any) -> httpx.Response:
        return self.get("/app/reminders/timeline", **params)

    def settings(self) -> httpx.Response:
        return self.get("/app/settings")

    def entitlement(self) -> httpx.Response:
        return self.get("/app/entitlement")

    def parse_import(self, text: str) -> httpx.Response:
        return self.post("/app/import/parse", {"text": text})

    def commit_import(self, rows: list, batch_id: str) -> httpx.Response:
        return self.post("/app/import/commit", {"rows": rows, "batch_id": batch_id})

    def scan(self, body: dict) -> httpx.Response:
        return self.post("/app/scans", body)

    def undo(self) -> httpx.Response:
        return self.post("/app/undo", {})

    def find_subscription(self, name: str) -> dict | None:
        response = self.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX})
        assert response.status_code in SUCCESS_STATUSES, describe(response)
        for row in response.json().get("data", []):
            if row.get("name") == name:
                return row
        return None


def sign_in(email: str, password: str = PASSWORD) -> Session:
    anonymous = Session()
    response = anonymous.post("/auth/login", {"email": email, "password": password})
    assert response.status_code in SUCCESS_STATUSES, (
        f"sign-in for {email} must succeed with the seeded password. {describe(response)}")
    token = response.json().get("access_token")
    assert token, f"login for {email} returned no access_token. {describe(response)}"
    return Session(token=token, email=email)


@pytest.fixture(scope="session")
def anonymous() -> Session:
    return Session()


@pytest.fixture(scope="session")
def owner() -> Session:
    return sign_in(OWNER_EMAIL)


@pytest.fixture(scope="session")
def owner2() -> Session:
    return sign_in(OWNER2_EMAIL)


class Store:
    """The persisted rows behind the app, read through the shared backend adapter."""

    def __init__(self, backend) -> None:
        self.backend = backend

    def count(self, table: str, **where) -> int:
        return self.backend.count(table, **where)

    def rows(self, table: str, limit: int | None = None, **where) -> list:
        return self.backend.rows(table, limit=limit, **where)

    def one(self, table: str, **where):
        return self.backend.one(table, **where)


@pytest.fixture(scope="session")
def store() -> Store:
    return Store(capabilities.make_backend())


def page(path: str) -> httpx.Response:
    """One public document, fetched from the app origin rather than the api base."""
    with httpx.Client(base_url=appclient.app_url(), timeout=30.0,
                      follow_redirects=True) as client:
        return client.get(path)


def raw_page(path: str) -> httpx.Response:
    """One public document with redirects left unfollowed, so a status can be read."""
    with httpx.Client(base_url=appclient.app_url(), timeout=30.0,
                      follow_redirects=False) as client:
        return client.get(path)
