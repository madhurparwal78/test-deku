"""Task fixtures for deku/cinematic-room-portfolio-vb.

Two rules govern this file:

1. Implementation agnostic. Nothing here assumes the agent's framework, file
   layout, ORM or module names. The only assumptions are the App Contract (the
   app answers at APP_PUBLIC_URL, REST under /api) and whatever instruction.md
   pinned explicitly: the endpoint paths and bodies, the failure kinds, the
   table names, the scene object key scheme, and the seeded accounts and sites.

2. Provider agnostic. The persistence and object-store helpers are composed from
   the generic capability primitives in capabilities.py, never a provider SDK, so
   swapping a slot away from postgres or minio replaces an adapter, not this file.
"""

from __future__ import annotations

import base64
import os

import httpx
import pytest
from capabilities import make_backend, make_store

TIMEOUT = 30.0

SEEDED_PASSWORD = "deku-demo-pw-2026"
CREATOR_EMAIL = "creator@example.com"
CREATOR2_EMAIL = "creator2@example.com"
VISITOR_EMAIL = "visitor@example.com"
VISITOR2_EMAIL = "visitor2@example.com"

PUBLISHED_HANDLE = "atrium"
DRAFT_HANDLE = "nightshift"

ONE_PX_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)
ONE_PX_PNG_BYTES = base64.b64decode(ONE_PX_PNG_B64)


def app_url() -> str:
    return os.environ.get("APP_PUBLIC_URL", "http://localhost:4173")


def unique_token(tag: str = "verifier") -> str:
    """A fresh token per call, so no test depends on another's rows."""
    return f"{tag}-{os.urandom(6).hex()}"


def room_payload(**over) -> dict:
    body = {
        "label": "Verifier Label",
        "name": "Verifier Room",
        "sentence": "A room created by the verifier.",
        "paragraph": "",
        "align": "left",
        "buttons": [],
    }
    body.update(over)
    return body


def note_payload(room_id, **over) -> dict:
    body = {"text": "A note left by the verifier.", "room_id": room_id}
    body.update(over)
    return body


@pytest.fixture(scope="session")
def client():
    with httpx.Client(base_url=app_url(), timeout=TIMEOUT, follow_redirects=True) as c:
        yield c


def _login_client(email: str) -> httpx.Client:
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


@pytest.fixture(scope="session")
def creator_client():
    c = _login_client(CREATOR_EMAIL)
    yield c
    c.close()


@pytest.fixture(scope="session")
def creator2_client():
    c = _login_client(CREATOR2_EMAIL)
    yield c
    c.close()


@pytest.fixture(scope="session")
def visitor_client():
    c = _login_client(VISITOR_EMAIL)
    yield c
    c.close()


@pytest.fixture(scope="session")
def visitor2_client():
    c = _login_client(VISITOR2_EMAIL)
    yield c
    c.close()


def fresh_visitor_client() -> httpx.Client:
    """Sign up and sign in a brand-new visitor, so a moderation or validation
    test never collides with the seeded one-note-per-visitor constraint."""
    email = unique_token("visitor") + "@example.com"
    c = httpx.Client(base_url=app_url(), timeout=TIMEOUT, follow_redirects=True)
    r = c.post("/api/auth/signup", json={
        "email": email,
        "password": SEEDED_PASSWORD,
        "display_name": "Verifier Visitor",
    })
    assert r.status_code in (200, 201), (
        f"POST /api/auth/signup for {email!r} returned {r.status_code}, expected 200 or 201: "
        f"{r.text[:300]}"
    )
    login = c.post("/api/auth/login", json={"email": email, "password": SEEDED_PASSWORD})
    assert login.status_code in (200, 201), (
        f"POST /api/auth/login for the new visitor returned {login.status_code}: {login.text[:300]}"
    )
    token = login.json().get("access_token", "")
    assert token, f"a fresh visitor login returned no access_token: {login.text[:300]}"
    c.headers.update({"Authorization": f"Bearer {token}"})
    return c


@pytest.fixture(scope="session")
def store():
    """Domain queries over the app's own tables, composed from capability
    primitives, never a provider SDK."""
    return make_backend()


@pytest.fixture(scope="session")
def object_store():
    """The task's object-store slot, composed from capabilities.make_store -- an
    S3-compatible adapter, never a provider SDK, so the storage assertions read
    the same bucket the app wrote the scene image to."""
    return make_store()
