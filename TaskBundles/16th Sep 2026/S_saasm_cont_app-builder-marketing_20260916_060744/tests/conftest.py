from __future__ import annotations

import os
import time

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

SETTLE_SECONDS = 2.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    time.sleep(seconds)


AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"
SUBSCRIBER_EMAIL = "subscriber@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"

DRAFT_ARTICLE_SLUG = "agents-reading-your-schema"
FEATURED_ARTICLE_SLUG = "spreadsheet-to-app-in-an-afternoon"
SECOND_ARTICLE_SLUG = "what-your-warehouse-sheet-already-knows"
CLOSED_JOB_SLUG = "field-marketing-lead"
OPEN_JOB_SLUG = "staff-frontend-engineer"

COVER_KEY_PREFIX = "covers/"
ATTACHMENT_KEY_PREFIX = "build-requests/"
ATTACHMENT_MAX_BYTES = 26214400
PROMPT_MAX_CHARS = 4000
GRANT_LIFETIME_SECONDS = 300

DENIED = (400, 401, 403, 404)
OK = (200, 201, 202)


def unique_email(label: str) -> str:
    return f"probe-{label}-{os.urandom(6).hex()}@example.com"


def unique_slug(label: str) -> str:
    return f"probe-{label}-{os.urandom(6).hex()}"


def excerpt(response) -> str:
    return response.text[:300]


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def author_token() -> str:
    return login(AUTHOR_EMAIL, seeded_password("SEED_AUTHOR_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def author_client(author_token: str):
    with client(author_token) as c:
        yield c


@pytest.fixture(scope="session")
def author2_token() -> str:
    return login(AUTHOR2_EMAIL, seeded_password("SEED_AUTHOR2_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def author2_client(author2_token: str):
    with client(author2_token) as c:
        yield c


@pytest.fixture(scope="session")
def reader_token() -> str:
    return login(READER_EMAIL, seeded_password("SEED_READER_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def reader_client(reader_token: str):
    with client(reader_token) as c:
        yield c


class SiteStore:
    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def user_by_email(self, email: str) -> dict | None:
        return self._b.one("users", email=email)

    def count_users(self, email: str) -> int:
        return self._b.count("users", email=email)

    def article_by_slug(self, slug: str) -> dict | None:
        return self._b.one("articles", slug=slug)

    def count_articles(self, **where) -> int:
        return self._b.count("articles", **where)

    def articles(self, **where) -> list[dict]:
        return self._b.rows("articles", **where)

    def press_items(self, **where) -> list[dict]:
        return self._b.rows("press_items", **where)

    def job_by_slug(self, slug: str) -> dict | None:
        return self._b.one("jobs", slug=slug)

    def jobs(self, **where) -> list[dict]:
        return self._b.rows("jobs", **where)

    def qa_entries(self, **where) -> list[dict]:
        return self._b.rows("qa_entries", **where)

    def build_requests(self, **where) -> list[dict]:
        return self._b.rows("build_requests", **where)

    def count_subscriptions(self, email: str) -> int:
        return self._b.count("subscriptions", email=email)


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def store(backend: Backend) -> SiteStore:
    return SiteStore(backend)


@pytest.fixture(scope="session")
def objects() -> ObjectStore:
    return make_store()
