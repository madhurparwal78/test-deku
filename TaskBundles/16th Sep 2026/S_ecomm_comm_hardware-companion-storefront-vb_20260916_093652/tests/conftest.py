"""Shared fixtures and helpers for the hardware-companion-storefront graders.

The pytest layer is black box: it reaches the app only over HTTP through
appclient, and inspects the declared services only through the capability
adapters. Business rows are read through the Backend adapter, invoices through
the Payments adapter, and confirmation mail through the Inbox adapter, never
through a database, killbill or SMTP client.
"""
from __future__ import annotations

import os
import time

import pytest

from appclient import client, login, seeded_password
from capabilities import Backend, Inbox, Payments, make_backend, make_inbox, make_payments

SEEDED_PASSWORD = "deku-demo-pw-2026"
CUSTOMER_EMAIL = "customer@example.com"
CUSTOMER2_EMAIL = "customer2@example.com"
CAMERA_PRICE_MINOR = 79900
CURRENCY = "usd"
PAID_STATUS = "paid"
FIRMWARE_OLD = "1.0.0"
FIRMWARE_NEW = "1.1.0"
PAGE_SIZE_DEFAULT = 20
CONFLICT_STATUS = 409
SETTLE_SECONDS = 1.0

ADDRESS = {
    "name": "Test Buyer",
    "line1": "1 Workshop Lane",
    "city": "Testville",
    "region": "CA",
    "postal_code": "90001",
    "country": "US",
}


def account_password() -> str:
    """The seeded password. A verifier override may shrink it in CI."""
    return seeded_password("SEED_ACCOUNT_PASSWORD", SEEDED_PASSWORD)


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned wait: let an asynchronous side effect land."""
    time.sleep(seconds)


def fresh_email(prefix: str = "buyer") -> str:
    """A unique seed address so a test never collides with a prior run."""
    return f"{prefix}-{os.urandom(6).hex()}@example.com"


def poll(read, accept, tries: int = 30):
    """Read until accept(value) is truthy or the attempts run out."""
    latest = None
    for _ in range(tries):
        latest = read()
        if accept(latest):
            return latest
        settle(0.5)
    return latest


@pytest.fixture(scope="session")
def customer_token() -> str:
    return login(CUSTOMER_EMAIL, account_password())


@pytest.fixture(scope="session")
def customer2_token() -> str:
    return login(CUSTOMER2_EMAIL, account_password())


@pytest.fixture
def customer_client(customer_token):
    with client(customer_token) as c:
        yield c


@pytest.fixture
def customer2_client(customer2_token):
    with client(customer2_token) as c:
        yield c


@pytest.fixture
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def db() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    return make_inbox()


@pytest.fixture(scope="session")
def payments() -> Payments:
    return make_payments()
