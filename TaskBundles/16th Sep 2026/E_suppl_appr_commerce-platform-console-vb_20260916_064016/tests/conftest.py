"""Task fixtures for deku/commerce-platform-console-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout,
ORM or module names. The only assumptions are the App Contract and what
instruction.md pinned literally.

Provider agnostic: domain helpers are composed from the generic primitives in
capabilities.py, never from a provider SDK.

Auth is Keycloak, and every fixture authenticates through the app's own session
surface rather than through the issuer's admin API. Clients are function scoped
so no bearer token is held across the run.
"""

from __future__ import annotations

import os
import time

import pytest
from _shapes import items
from appclient import client, login, seeded_password
from capabilities import Backend, make_backend

OWNER_EMAIL = "owner@example.com"
MANAGER_EMAIL = "manager@example.com"
SUPPORT_EMAIL = "support@example.com"
FINANCE_EMAIL = "finance@example.com"
MALLARD_EMAIL = "mallard@example.com"

CORPUS_PASSWORD = "deku-demo-pw-2026"

OAKLEAF_HANDLE = "oakleaf"
MALLARD_HANDLE = "modern-mallard"

CURRENCY = "inr"
SUPPORT_CEILING_MINOR = 500000
FINANCE_CEILING_MINOR = 20000000

ORDER_SMALL_MINOR = 850900
ORDER_LARGE_MINOR = 3411200
MALLARD_ORDER_MINOR = 1998640

ORDER_INSIDE_CEILING = "#2050"
ORDER_PENDING_REQUEST = "#2049"
ORDER_BROWSER_REFUND = "#2048"
ORDER_APPROVED_REFUND = "#2047"
ORDER_VALIDATION = "#2046"
ORDER_OTHER_STORE = "#3001"

PUNE = "Pune Warehouse"
DELHI = "Delhi Flagship"

BOUNDARY_PRODUCT = "Carry"
BOUNDARY_PRICE_MINOR = 5986900

PUBLIC_ROUTES = ("/in", "/in/pricing", "/in/orders", "/in/privacy", "/in/terms")

SETTLE_SECONDS = float(os.environ.get("DEKU_SETTLE_SECONDS", "2"))
POLL_SECONDS = 30.0


def settle() -> None:
    """The one sanctioned sleep: a bounded wait before asserting a non-event."""
    time.sleep(SETTLE_SECONDS)


def probe_key(prefix: str) -> str:
    """A per-run unique idempotency key, so a rerun never replays a stored response."""
    return f"{prefix}-{os.urandom(6).hex()}"


def poll_until(predicate, deadline_seconds: float = POLL_SECONDS):
    """Poll to a monotonic deadline, routing every wait through settle()."""
    deadline = time.monotonic() + deadline_seconds
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    return last


def _authed(email: str):
    return client(login(email, seeded_password("SEED_PASSWORD", CORPUS_PASSWORD)))


@pytest.fixture()
def anon_client():
    with client() as c:
        yield c


@pytest.fixture()
def owner_client():
    with _authed(OWNER_EMAIL) as c:
        yield c


@pytest.fixture()
def manager_client():
    with _authed(MANAGER_EMAIL) as c:
        yield c


@pytest.fixture()
def support_client():
    with _authed(SUPPORT_EMAIL) as c:
        yield c


@pytest.fixture()
def finance_client():
    with _authed(FINANCE_EMAIL) as c:
        yield c


@pytest.fixture()
def mallard_client():
    with _authed(MALLARD_EMAIL) as c:
        yield c


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


def order_index(c) -> list:
    """Every order the session's store exposes, as a top-level array."""
    r = c.get("/api/orders")
    assert r.status_code == 200, (
        f"GET /api/orders returned {r.status_code}, expected 200; body={r.text[:300]}")
    return items(r.json())


def order_by_number(c, number: str) -> dict | None:
    for row in order_index(c):
        if str(row.get("number")) == number:
            return row
    return None


def order_detail(c, order_id) -> dict:
    r = c.get(f"/api/orders/{order_id}")
    assert r.status_code == 200, (
        f"GET /api/orders/{order_id} returned {r.status_code}, expected 200; "
        f"body={r.text[:300]}")
    return r.json()


def post_refund(c, order_id, amount_minor: int, key: str, reason: str = "goodwill",
                restock: bool = False):
    return c.post(
        f"/api/orders/{order_id}/refunds",
        json={"amount_minor": amount_minor, "currency": CURRENCY, "reason": reason,
              "restock": restock, "idempotency_key": key})


def approvals(c, state: str | None = None) -> list:
    r = c.get("/api/approvals", params={"state": state} if state else None)
    assert r.status_code == 200, (
        f"GET /api/approvals returned {r.status_code}, expected 200; body={r.text[:300]}")
    return items(r.json())


def decide(c, request_id, decision: str, key: str, note: str = "reviewed"):
    return c.post(
        f"/api/approvals/{request_id}/decision",
        json={"decision": decision, "note": note, "idempotency_key": key})


def balances(c) -> dict:
    r = c.get("/api/balances")
    assert r.status_code == 200, (
        f"GET /api/balances returned {r.status_code}, expected 200; body={r.text[:300]}")
    return {(row.get("currency"), row.get("kind")): row.get("amount_minor")
            for row in items(r.json())}


def available_balance(c) -> int:
    got = balances(c)
    for (currency, kind), amount in got.items():
        if currency == CURRENCY and kind == "available":
            return int(amount)
    raise AssertionError(
        f"GET /api/balances exposes no ('{CURRENCY}', 'available') row; saw {sorted(got)}")


def inventory_rows(c, location_id=None) -> list:
    r = c.get("/api/inventory", params={"location": location_id} if location_id else None)
    assert r.status_code == 200, (
        f"GET /api/inventory returned {r.status_code}, expected 200; body={r.text[:300]}")
    return items(r.json())


LEDGER_ENTRY_TABLE = "ledger_entry"
APPROVAL_REQUEST_TABLE = "approval_request"
INVENTORY_LEVEL_TABLE = "inventory_level"


def ledger_entry_count(backend: Backend, **where) -> int:
    return backend.count(LEDGER_ENTRY_TABLE, **where)


def approval_request_rows(backend: Backend, **where) -> list:
    return backend.rows(APPROVAL_REQUEST_TABLE, **where)


def inventory_level_rows(backend: Backend, **where) -> list:
    return backend.rows(INVENTORY_LEVEL_TABLE, **where)
