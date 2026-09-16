"""Shared fixtures and helpers for the voice-synthesis-workbench graders.

The pytest layer is black box: it reaches the app only over HTTP through
appclient, and inspects the declared services only through the capability
adapters. Business rows are read through the Backend adapter and stored audio
through the ObjectStore adapter, never through a database or storage SDK.
"""
from __future__ import annotations

import os
import time

import pytest

from appclient import client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

SEEDED_PASSWORD = "deku-demo-pw-2026"
AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"
GENERATION_COST = 100
AUTHOR_BALANCE = 300
AUTHOR2_BALANCE = 50
PAGE_SIZE_DEFAULT = 20
TAKE_OBJECT_PREFIX = "takes/"
SETTLE_SECONDS = 1.0


def account_password() -> str:
    """The seeded password. A verifier override may shrink it in CI."""
    return seeded_password("SEED_ACCOUNT_PASSWORD", SEEDED_PASSWORD)


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned wait: let an asynchronous side effect land."""
    time.sleep(seconds)


def fresh_email(prefix: str = "probe") -> str:
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
def author_token() -> str:
    return login(AUTHOR_EMAIL, account_password())


@pytest.fixture(scope="session")
def author2_token() -> str:
    return login(AUTHOR2_EMAIL, account_password())


@pytest.fixture(scope="session")
def reader_token() -> str:
    return login(READER_EMAIL, account_password())


@pytest.fixture
def author_client(author_token):
    with client(author_token) as c:
        yield c


@pytest.fixture
def author2_client(author2_token):
    with client(author2_token) as c:
        yield c


@pytest.fixture
def reader_client(reader_token):
    with client(reader_token) as c:
        yield c


@pytest.fixture
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def object_store() -> ObjectStore:
    return make_store()


@pytest.fixture(scope="session")
def db() -> Backend:
    return make_backend()
