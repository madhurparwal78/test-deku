"""Task fixtures for deku/scroll-chapter-archive-vb.

Two rules govern this file:

1. Implementation agnostic. Nothing here assumes the agent's framework, file
   layout, ORM or module names. The only assumptions are the App Contract (the
   app answers at APP_PUBLIC_URL, REST under /api) and whatever instruction.md
   pinned explicitly: the endpoint paths and bodies, the failure kinds, the
   table names, the poster object key scheme, the seeded accounts and the seeded
   chapter slugs.

2. Provider agnostic. The persistence and object-store helpers are composed from
   the generic capability primitives in capabilities.py, never a provider SDK, so
   swapping a slot away from postgres or minio replaces an adapter, not this file.
"""

from __future__ import annotations

import os

import httpx
import pytest
from capabilities import make_backend, make_store

TIMEOUT = 30.0

SEEDED_PASSWORD = "deku-demo-pw-2026"
CURATOR_EMAIL = "curator@example.com"
MEMBER_EMAIL = "visitor@example.com"
MEMBER2_EMAIL = "visitor2@example.com"

PUBLISHED_CHAPTER = "solar"
DRAFT_TO_PUBLISH = "bone"
DRAFT_STAYS = "forest-landscape"
SEEDED_POSITION = 0.42


def app_url() -> str:
    return os.environ.get("APP_PUBLIC_URL", "http://localhost:4173")


def unique_token(tag: str = "verifier") -> str:
    return f"{tag}-{os.urandom(6).hex()}"


def login_client(email: str) -> httpx.Client:
    c = httpx.Client(base_url=app_url(), timeout=TIMEOUT, follow_redirects=True)
    r = c.post("/api/auth/login", json={"email": email, "password": SEEDED_PASSWORD})
    assert r.status_code in (200, 201), (
        f"POST /api/auth/login for {email!r} returned {r.status_code}, expected 200 or 201 "
        f"so the seeded account can sign in: {r.text[:300]}"
    )
    token = r.json().get("access_token", "")
    assert token, f"login for {email!r} returned no access_token: {r.text[:300]}"
    c.headers.update({"Authorization": f"Bearer {token}"})
    return c


def fresh_client() -> httpx.Client:
    """A brand-new client with no cookies, for the cookie-consent contract."""
    return httpx.Client(base_url=app_url(), timeout=TIMEOUT, follow_redirects=True)


@pytest.fixture(scope="session")
def client():
    with httpx.Client(base_url=app_url(), timeout=TIMEOUT, follow_redirects=True) as c:
        yield c


@pytest.fixture(scope="session")
def curator_client():
    c = login_client(CURATOR_EMAIL)
    yield c
    c.close()


@pytest.fixture(scope="session")
def member_client():
    c = login_client(MEMBER_EMAIL)
    yield c
    c.close()


@pytest.fixture(scope="session")
def member2_client():
    c = login_client(MEMBER2_EMAIL)
    yield c
    c.close()


@pytest.fixture(scope="session")
def store():
    return make_backend()


@pytest.fixture(scope="session")
def object_store():
    return make_store()
