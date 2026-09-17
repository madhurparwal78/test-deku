"""Task fixtures for deku/scheduling-link-platform-vb.

Implementation agnostic: nothing here assumes the agent's framework, file
layout, ORM or module names. The only assumptions are the App Contract and
whatever instruction.md pinned literally, which is the route set, the endpoint
shapes, the seeded accounts, the corpus password, the nine table names, the
page states and the object-key scheme.

Provider agnostic: the domain helpers below are composed from the generic
Backend and ObjectStore primitives in capabilities.py, never from a provider
SDK. Swapping the backend slot from postgres, or the storage slot from minio,
replaces an adapter rather than this file.
"""

from __future__ import annotations

import hashlib
import os
import time

import pytest
from appclient import api_base, app_url, client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

SETTLE_SECONDS = 2.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give an unwanted async side effect time to land before asserting absence."""
    time.sleep(seconds)


AUTHOR_EMAIL = "author@example.com"
READER_EMAIL = "reader@example.com"
CORPUS_PASSWORD = "deku-demo-pw-2026"

DRAFT_ROUTE = "/blog/scheduling-links-that-convert"
DRAFT_TITLE = "Scheduling links that convert"
OBJECT_KEY_PREFIX = "pages/"
STUDIO_ROUTE = "/studio"
STUDIO_VIEWS_ROUTE = "/studio/views"
LOGIN_ROUTE = "/login"
BOOKING_PAGE_ROUTE = "/editor"

PUBLIC_ROUTES = (
    "/", "/teams", "/ai", "/embed", "/app", "/about", "/jobs", "/open",
    "/faq", "/terms", "/font", "/help", "/docs", "/editor", "/visitor",
)

READ_ONLY_PUBLIC_ROUTES = PUBLIC_ROUTES[:13]

STATE_DRAFT = "draft"
STATE_PUBLISHED = "published"

POLL_DEADLINE_SECONDS = 30.0
POLL_INTERVAL_SECONDS = 0.5


def unique_token(prefix: str) -> str:
    return f"{prefix}-{os.urandom(6).hex()}"


def probe_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


def png_bytes(seed: str) -> bytes:
    """A small, deterministic byte payload that is a valid PNG header."""
    body = hashlib.sha256(seed.encode("utf-8")).digest()
    return b"\x89PNG\r\n\x1a\n" + body


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def wait_for(predicate, description: str):
    """Poll to a monotonic deadline for an asynchronous side effect."""
    deadline = time.monotonic() + POLL_DEADLINE_SECONDS
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle(POLL_INTERVAL_SECONDS)
    raise AssertionError(f"{description} did not become true within the deadline")


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def author_token() -> str:
    return login(AUTHOR_EMAIL, seeded_password("SEED_AUTHOR_PASSWORD", CORPUS_PASSWORD))


@pytest.fixture(scope="session")
def author_client(author_token: str):
    with client(author_token) as c:
        yield c


@pytest.fixture(scope="session")
def reader_token() -> str:
    return login(READER_EMAIL, seeded_password("SEED_READER_PASSWORD", CORPUS_PASSWORD))


@pytest.fixture(scope="session")
def reader_client(reader_token: str):
    with client(reader_token) as c:
        yield c


class SiteStore:
    """Domain queries for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def user_by_email(self, email: str) -> dict | None:
        return self._b.one("users", email=email)

    def count_users(self, email: str) -> int:
        return self._b.count("users", email=email)

    def page_by_route(self, route: str) -> dict | None:
        return self._b.one("pages", route=route)

    def page_by_slug(self, slug: str) -> dict | None:
        return self._b.one("pages", slug=slug)

    def pages_in_state(self, state: str) -> list[dict]:
        return self._b.rows("pages", state=state)

    def count_pages(self, **where) -> int:
        return self._b.count("pages", **where)

    def bands_for_page(self, page_id) -> list[dict]:
        return self._b.rows("bands", page_id=page_id)

    def media_for_page(self, page_id) -> list[dict]:
        return self._b.rows("media", page_id=page_id)

    def media_by_key(self, object_key: str) -> dict | None:
        return self._b.one("media", object_key=object_key)

    def count_media(self, **where) -> int:
        return self._b.count("media", **where)

    def count_page_views(self, route: str) -> int:
        return self._b.count("page_views", route=route)

    def booking_page_for_user(self, user_id) -> dict | None:
        return self._b.one("booking_pages", user_id=user_id)

    def count_booking_pages(self, **where) -> int:
        return self._b.count("booking_pages", **where)


@pytest.fixture(scope="session")
def db() -> SiteStore:
    return SiteStore(make_backend())


@pytest.fixture(scope="session")
def store() -> ObjectStore:
    return make_store()


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as driver:
        launched = driver.chromium.launch()
        yield launched
        launched.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    opened = context.new_page()
    yield opened
    context.close()


@pytest.fixture
def ui_page(browser):
    context = browser.new_context(viewport={"width": 390, "height": 844})
    opened = context.new_page()
    yield opened
    context.close()


def create_draft_page(author, slug: str, route: str, title: str = "Draft page") -> dict:
    response = author.post(
        "/pages",
        json={
            "slug": slug,
            "route": route,
            "kind": "editorial",
            "title": title,
            "standfirst": "Composed by the verifier for a substep.",
        },
    )
    assert response.status_code in (200, 201), (
        f"POST /api/pages for slug {slug!r} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    return response.json()


def upload_media(author, page_id, payload: bytes, alt_text: str = "A drawn placeholder"):
    return author.post(
        "/media",
        data={"page_id": str(page_id), "alt_text": alt_text},
        files={"file": ("placeholder.png", payload, "image/png")},
    )


def signup(email: str, username: str, password: str = "verifier-pw-1") -> dict:
    with client() as c:
        response = c.post(
            "/auth/signup",
            json={
                "email": email,
                "password": password,
                "username": username,
                "display_name": "Verifier Visitor",
            },
        )
    return {"status": response.status_code, "body": response.text, "client": None,
            "json": response.json() if response.headers.get("content-type", "").startswith("application/json") else {}}


def page_url(route: str) -> str:
    return f"{app_url()}{route}"


def api_url(path: str) -> str:
    return f"{api_base()}{path}"
