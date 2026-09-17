"""Task fixtures for deku/immersive-factory-tour-vb.

Two rules from the pytest contract govern this file:

1. Implementation agnostic. Nothing here assumes the agent's framework, file
   layout, ORM or module names. The only things assumed are the App Contract
   (the app answers at APP_PUBLIC_URL, REST under /api, POST /api/auth/login
   returns access_token) and whatever instruction.md pinned explicitly: the
   endpoint paths and bodies, the seeded accounts, the station names, the prize
   names, the poster key scheme and the consent flag.

2. Provider agnostic. Business rows are read through the Backend adapter and
   stored posters through the ObjectStore adapter, never through a database or
   storage SDK.
"""

from __future__ import annotations

import time
import uuid

import httpx
import pytest
from appclient import app_url, client, login
from capabilities import Backend, ObjectStore, make_backend, make_store

PASSWORD = "deku-demo-pw-2026"

AUTHOR_EMAIL = "author@example.com"
READER_EMAIL = "reader@example.com"
READER2_EMAIL = "reader2@example.com"

STATIONS = ["knitting", "dyeing", "embroidering"]
PRIZES = ["Signature Green", "Sunbeam Yellow", "Sky Blue"]

POSTER_PREFIX = "chapters/"
PRIZE_PREFIX = "prizes/"
CONSENT_FLAG = "consent_terms"
CONFIRMATION = "If you are selected, we will contact you by email. Stay tuned."

ACCEPTED = (200, 201)

PNG_1PX = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _client_error(code: int) -> bool:
    return 400 <= code < 500


def settle(seconds: float = 0.4) -> None:
    """The only sanctioned sleep. Spaces a bounded poll for a side effect that
    settles a moment after the HTTP call returns (an object written to the store)."""
    time.sleep(seconds)


def poll(read, accept, tries: int = 20):
    """Poll a read to a bounded deadline until accept is satisfied."""
    deadline = time.monotonic() + 8.0
    value = read()
    while not accept(value) and time.monotonic() < deadline:
        settle()
        value = read()
    return value


def signup(email: str, password: str = PASSWORD, name: str = "Probe") -> str:
    response = httpx.post(
        f"{app_url()}/api/auth/signup",
        json={"email": email, "password": password, "name": name},
        timeout=30.0,
    )
    assert response.status_code in ACCEPTED, (
        f"open signup must create a reader, got {response.status_code}: {response.text[:200]}")
    token = response.json().get("access_token")
    assert token, "signup must return an access token"
    return token


def fresh_reader():
    """Sign up a brand-new reader and return (client, email)."""
    email = f"probe-{uuid.uuid4().hex[:10]}@example.com"
    token = signup(email)
    return client(token), email


def create_chapter(c, station: str = "knitting", title: str | None = None) -> dict:
    """Create a draft chapter with a poster, returning the chapter record."""
    title = title or f"Chapter {uuid.uuid4().hex[:8]}"
    response = c.post(
        "/chapters",
        data={"station": station, "title": title, "body": "How the fabric is made."},
        files={"poster": ("poster.png", PNG_1PX, "image/png")},
    )
    assert response.status_code in ACCEPTED, (
        f"the author must be able to create a chapter, got {response.status_code}: {response.text[:200]}")
    return response.json()


def publish_chapter(c, chapter_id) -> httpx.Response:
    return c.post(f"/chapters/{chapter_id}/publish")


def a_draft_chapter(author_c) -> dict:
    """A draft chapter belonging to the author, created if none is seeded."""
    listed = author_c.get("/chapters")
    if listed.status_code == 200:
        for chapter in listed.json():
            if chapter.get("state") == "draft":
                return chapter
    return create_chapter(author_c)


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def author_client():
    with client(login(AUTHOR_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture(scope="session")
def reader_client():
    with client(login(READER_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture(scope="session")
def reader2_client():
    with client(login(READER2_EMAIL, PASSWORD)) as c:
        yield c


class TourStore:
    """Domain queries for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def account(self, email: str) -> dict | None:
        return self._b.one("accounts", email=email)

    def accounts_by_role(self, role: str) -> list[dict]:
        return self._b.rows("accounts", role=role)

    def chapters(self, **where) -> list[dict]:
        return self._b.rows("chapters", **where)

    def chapter_count(self, **where) -> int:
        return self._b.count("chapters", **where)

    def prize_count(self, **where) -> int:
        return self._b.count("prizes", **where)

    def entries_for(self, reader_id) -> list[dict]:
        return self._b.rows("entries", reader_id=reader_id)

    def entry_count(self, **where) -> int:
        return self._b.count("entries", **where)


@pytest.fixture(scope="session")
def db() -> TourStore:
    return TourStore(make_backend())


@pytest.fixture(scope="session")
def object_store() -> ObjectStore:
    return make_store()
