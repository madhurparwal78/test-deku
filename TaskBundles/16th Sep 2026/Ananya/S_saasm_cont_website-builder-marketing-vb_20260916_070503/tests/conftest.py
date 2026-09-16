"""Fixtures, pinned literals and bounded-wait helpers for the Orb bundle.

No test function lives here. Every literal below is pinned verbatim in
instruction.md and recorded in the Literals Ledger.
"""

from __future__ import annotations

import hashlib
import os
import struct
import time
import zlib

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"

OWNER_EMAIL = "owner@example.com"
OWNER2_EMAIL = "owner2@example.com"
VISITOR_EMAIL = "visitor@example.com"

PUBLISHED_SITE_SLUG = "kestrel"
DRAFT_SITE_SLUG = "ivory-and-interval"
SECOND_OWNER_DRAFT_SLUG = "cedar-and-sage"

FREE_ADDRESS_SUFFIX = ".orbsite.com"

REGISTERED_NAME = "cedarandsage.com"
REGISTERED_NAME_ALT = "orb.com"
FREE_NAME = "forknframe.com"
FREE_NAME_ALT = "velatov.com"
FREE_NAME_PRICE = 1200
CURRENCY = "usd"

TEMPLATE_COUNT = 33
TEMPLATE_LIMIT_CAP = 48
TEMPLATE_CATEGORIES = [
    "eCommerce",
    "Portfolio",
    "Business",
    "Landing page",
    "Blog",
    "Real estate",
    "Weddings",
]

ALIAS_PATHS = ["/as", "/gs", "/v1", "/v2", "/412", "/416", "/417", "/419", "/md/"]

MARKETING_ROUTES = ["/", "/pos", "/terms", "/privacy"]

STATUS_DRAFT = "draft"
STATUS_PUBLISHED = "published"
REGISTRY_REGISTERED = "registered"
REGISTRY_AVAILABLE = "available"

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 30.0


def settle() -> None:
    """The one sanctioned sleep in the suite."""
    time.sleep(SETTLE_SECONDS)


def probe_suffix() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{probe_suffix()}@example.com"


def png_bytes(seed: int) -> bytes:
    """A tiny, valid single-pixel image whose bytes depend on the seed."""
    raw = b"\x00" + bytes([seed % 256, (seed * 7) % 256, (seed * 13) % 256])

    def chunk(tag: bytes, payload: bytes) -> bytes:
        body = tag + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(
            ">I", zlib.crc32(body) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw))
            + chunk(b"IEND", b""))


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def wait_for(predicate, deadline_seconds: float = POLL_DEADLINE_SECONDS):
    """Poll a predicate to a monotonic deadline, returning its last value."""
    deadline = time.monotonic() + deadline_seconds
    value = None
    while time.monotonic() < deadline:
        value = predicate()
        if value:
            return value
        settle()
    return value


@pytest.fixture(scope="session")
def app_base() -> str:
    return appclient.app_url()


@pytest.fixture(scope="session")
def api_base() -> str:
    return appclient.api_base()


@pytest.fixture()
def anon() -> httpx.Client:
    with appclient.client() as client:
        yield client


@pytest.fixture()
def raw() -> httpx.Client:
    with httpx.Client(base_url=appclient.app_url(), timeout=30.0,
                      follow_redirects=True) as client:
        yield client


@pytest.fixture()
def owner() -> httpx.Client:
    with appclient.client(appclient.login(OWNER_EMAIL, PASSWORD)) as client:
        yield client


@pytest.fixture()
def owner2() -> httpx.Client:
    with appclient.client(appclient.login(OWNER2_EMAIL, PASSWORD)) as client:
        yield client


@pytest.fixture()
def visitor() -> httpx.Client:
    with appclient.client(appclient.login(VISITOR_EMAIL, PASSWORD)) as client:
        yield client


@pytest.fixture(scope="session")
def store() -> capabilities.ObjectStore:
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend() -> capabilities.Backend:
    return capabilities.make_backend()


def signup(client: httpx.Client, email: str, password: str = PASSWORD,
           domain_query: str = "forknframe", **extra):
    body = {"email": email, "password": password, "domain_query": domain_query}
    body.update(extra)
    return client.post("/accounts", json=body)


def new_owner(client: httpx.Client) -> tuple[str, dict]:
    """A fresh tenant, so a test never depends on a browser journey's leftovers."""
    email = probe_email()
    response = signup(client, email)
    assert response.status_code in (200, 201), (
        f"sign-up for {email} returned {response.status_code}: {response.text[:400]}")
    payload = response.json()
    assert payload.get("access_token"), (
        f"sign-up for {email} returned no access_token: {response.text[:400]}")
    assert payload.get("site_id") is not None, (
        f"sign-up for {email} returned no site_id: {response.text[:400]}")
    return email, payload


def upload_picture(client: httpx.Client, site_id, payload: bytes,
                   alt_text: str = "A probe picture"):
    return client.post(
        f"/sites/{site_id}/media",
        files={"file": (f"probe-{probe_suffix()}.png", payload, "image/png")},
        data={"alt_text": alt_text},
    )
