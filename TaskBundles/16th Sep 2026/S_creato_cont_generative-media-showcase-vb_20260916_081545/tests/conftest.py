"""Task fixtures for deku/generative-media-showcase-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout,
ORM or module names. The only assumptions are the App Contract and what
instruction.md pinned literally.

Provider agnostic: domain helpers are composed from the generic primitives in
capabilities.py, never from a provider SDK.

Accounts belong to the app itself, so every fixture authenticates through the
app's own session surface. Clients are function scoped so no bearer token is held
across the run.
"""

from __future__ import annotations

import hashlib
import os
import re
import time

import pytest
from _shapes import items
from appclient import app_url, client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"

CORPUS_PASSWORD = "deku-demo-pw-2026"

DRAFT_SLUG = "the-media-router-preview"
OTHER_DRAFT_SLUG = "partner-campaign-preview"
MISSING_SLUG = "no-such-item-at-all"

CURRENCY = "usd"
MODEL_PRICES_MINOR = {
    "Nova-4.5": 12,
    "Chisel-2.0": 18,
    "Worldscape-1": 30,
    "Perform-2": 9,
}
MODEL_SPEC_FIELDS = (
    "name", "tagline", "resolution", "aspect_ratios", "inputs",
    "max_duration_seconds", "price_minor_per_second",
)

KEY_SCHEME = re.compile(r"^media/[^/]+/[0-9a-f]{64}\.[A-Za-z0-9]+$")

PUBLIC_ROUTES = ("/", "/api-platform", "/mcp", "/news", "/models", "/pricing",
                 "/privacy", "/terms", "/signup", "/login")

STUDIO_ENDPOINTS = (
    ("GET", "/api/studio/news", None),
    ("POST", "/api/studio/news", {"title": "probe", "dek": "probe",
                                  "body": "probe", "slug": "probe-item"}),
)

SECURITY_HEADERS = ("content-security-policy", "referrer-policy",
                    "x-content-type-options")

STORE_SECRET_ENV = ("STORAGE_SECRET_KEY", "STORAGE_ACCESS_KEY")

SETTLE_SECONDS = float(os.environ.get("DEKU_SETTLE_SECONDS", "2"))
POLL_SECONDS = 30.0

SMALLEST_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000"
    "000a49444154789c6360000002000100ffff03000006000557bfabd40000000049454e"
    "44ae426082"
)


def settle() -> None:
    """The one sanctioned sleep: a bounded wait before asserting a non-event."""
    time.sleep(SETTLE_SECONDS)


def probe_key(prefix: str) -> str:
    """A per-run unique idempotency key, so a rerun never replays a stored response."""
    return f"{prefix}-{os.urandom(6).hex()}"


def probe_slug(prefix: str) -> str:
    return f"{prefix}-{os.urandom(4).hex()}"


def probe_email(prefix: str) -> str:
    return f"{prefix}-{os.urandom(4).hex()}@example.com"


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
def author_client():
    with _authed(AUTHOR_EMAIL) as c:
        yield c


@pytest.fixture()
def author2_client():
    with _authed(AUTHOR2_EMAIL) as c:
        yield c


@pytest.fixture()
def reader_client():
    with _authed(READER_EMAIL) as c:
        yield c


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def store() -> ObjectStore:
    return make_store()


def base_url() -> str:
    return app_url().rstrip("/")


def public_news(c) -> list:
    r = c.get("/api/news")
    assert r.status_code == 200, (
        f"GET /api/news returned {r.status_code}, expected 200; body={r.text[:300]}")
    return items(r.json())


def studio_news(c) -> list:
    r = c.get("/api/studio/news")
    assert r.status_code == 200, (
        f"GET /api/studio/news returned {r.status_code}, expected 200; "
        f"body={r.text[:300]}")
    return items(r.json())


def item_by_slug(rows: list, slug: str) -> dict | None:
    for row in rows:
        if str(row.get("slug")) == slug:
            return row
    return None


def create_draft(c, slug: str, title: str = "A probe item") -> dict:
    r = c.post("/api/studio/news", json={
        "title": title, "dek": "A one line summary.", "body": "The body text.",
        "slug": slug})
    assert r.status_code in (200, 201), (
        f"POST /api/studio/news returned {r.status_code}, expected 201; "
        f"body={r.text[:300]}")
    return r.json()


def attach_poster(c, item_id, alt_text: str = "A gradient placeholder poster",
                  payload: bytes = SMALLEST_PNG, declared_type: str = "image/png",
                  filename: str = "poster.png"):
    return c.post(
        f"/api/studio/news/{item_id}/media",
        files={"file": (filename, payload, declared_type)},
        data={"alt_text": alt_text})


def publish(c, item_id):
    return c.post(f"/api/studio/news/{item_id}/publish")


def unpublish(c, item_id):
    return c.post(f"/api/studio/news/{item_id}/unpublish")


def media_key_of(payload: dict) -> str:
    for candidate in ("key", "object_key", "storage_key"):
        if payload.get(candidate):
            return str(payload[candidate])
    poster = payload.get("poster") or {}
    for candidate in ("key", "object_key", "storage_key"):
        if poster.get(candidate):
            return str(poster[candidate])
    raise AssertionError(
        f"the media response exposes no object key; saw keys {sorted(payload)}")


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def fetch_media(c, key: str):
    return c.get(f"/media/{key}")


def comparable(response) -> tuple:
    """The three facets a draft response and a missing response must share."""
    return (response.status_code,
            response.text.strip(),
            response.headers.get("content-type", "").split(";")[0].strip())


ACCOUNT_TABLE = "account"
CONTENT_ITEM_TABLE = "content_item"
MEDIA_OBJECT_TABLE = "media_object"
MODEL_SPEC_TABLE = "model_spec"


def account_rows(backend: Backend, **where) -> list:
    return backend.rows(ACCOUNT_TABLE, **where)


def content_item_rows(backend: Backend, **where) -> list:
    return backend.rows(CONTENT_ITEM_TABLE, **where)


def media_object_rows(backend: Backend, **where) -> list:
    return backend.rows(MEDIA_OBJECT_TABLE, **where)


def model_spec_rows(backend: Backend, **where) -> list:
    return backend.rows(MODEL_SPEC_TABLE, **where)
