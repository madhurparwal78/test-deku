"""Shared fixtures and helpers for the studio-capability-index graders.

The pytest layer is black box: it reaches the app only over HTTP through
appclient, and inspects the declared services only through the capability
adapters. Business rows are read through the Backend adapter and stored media
through the ObjectStore adapter, never through a database or storage SDK.
"""
from __future__ import annotations

import os
import time

import pytest

from appclient import client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

SEEDED_PASSWORD = "deku-demo-pw-2026"
EDITOR_EMAIL = "editor@example.com"
EDITOR2_EMAIL = "editor2@example.com"
VISITOR_EMAIL = "visitor@example.com"
PAGE_SIZE_DEFAULT = 20
MESSAGE_MAX = 4000
MEDIA_PREFIX = "casestudies/"
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
def editor_token() -> str:
    return login(EDITOR_EMAIL, account_password())


@pytest.fixture(scope="session")
def editor2_token() -> str:
    return login(EDITOR2_EMAIL, account_password())


@pytest.fixture(scope="session")
def visitor_token() -> str:
    return login(VISITOR_EMAIL, account_password())


@pytest.fixture
def editor_client(editor_token):
    with client(editor_token) as c:
        yield c


@pytest.fixture
def visitor_client(visitor_token):
    with client(visitor_token) as c:
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
