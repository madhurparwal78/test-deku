from __future__ import annotations

import os
import time

import pytest
from _shapes import items
from appclient import client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"
CORPUS_PASSWORD = "deku-demo-pw-2026"

LEAD_SLUG = "ma"
SECOND_SLUG = "ls"
THIRD_SLUG = "hf"
DRAFT_SLUG = "mr"

FACETS = ("Brand", "Digital", "Motion")
BLOCK_KINDS = ("full_bleed_media", "paired_detail", "pull_quote", "filmstrip_row")
PUBLISHED = "published"
DRAFT = "draft"
SEEDED_ENQUIRY_REFERENCE = "ENQ-1001"
STUDIO_CONTACT_EMAIL = "projects@vellum.co"
POSTER_PREFIX = "projects/"
POSTER_MAX_BYTES = 8388608

SETTLE_SECONDS = 0.25


def settle(seconds: float = SETTLE_SECONDS) -> None:
    time.sleep(seconds)


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
def author2_client():
    token = login(AUTHOR2_EMAIL, seeded_password("SEED_AUTHOR2_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture(scope="session")
def reader_client():
    token = login(READER_EMAIL, seeded_password("SEED_READER_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


class StudioStore:
    """Domain queries composed from the generic capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def count_users(self, **where) -> int:
        return self._b.count("users", **where)

    def user_by_email(self, email: str) -> dict | None:
        return self._b.one("users", email=email)

    def count_projects(self, **where) -> int:
        return self._b.count("projects", **where)

    def project_by_slug(self, slug: str) -> dict | None:
        return self._b.one("projects", slug=slug)

    def projects(self, limit: int = 200, **where) -> list[dict]:
        return self._b.rows("projects", limit=limit, **where)

    def count_blocks_for(self, project_id) -> int:
        return self._b.count("project_blocks", project_id=project_id)

    def blocks_for(self, project_id, limit: int = 50) -> list[dict]:
        return self._b.rows("project_blocks", limit=limit, project_id=project_id)

    def count_awards_for(self, project_id) -> int:
        return self._b.count("project_awards", project_id=project_id)

    def awards_for(self, project_id, limit: int = 50) -> list[dict]:
        return self._b.rows("project_awards", limit=limit, project_id=project_id)

    def count_enquiries(self, **where) -> int:
        return self._b.count("enquiries", **where)

    def enquiries(self, limit: int = 200, **where) -> list[dict]:
        return self._b.rows("enquiries", limit=limit, **where)

    def count_globals(self) -> int:
        return self._b.count("site_globals")

    def globals_row(self) -> dict | None:
        rows = self._b.rows("site_globals", limit=2)
        return rows[0] if rows else None

    def count_pages(self, **where) -> int:
        return self._b.count("pages", **where)


@pytest.fixture(scope="session")
def db() -> StudioStore:
    return StudioStore(make_backend())


@pytest.fixture(scope="session")
def store() -> ObjectStore:
    return make_store()


@pytest.fixture
def unique_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


@pytest.fixture
def unique_message() -> str:
    return f"Probe enquiry {os.urandom(6).hex()} about a motion identity."


@pytest.fixture
def unique_slug() -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    raw = os.urandom(2)
    return alphabet[raw[0] % 26] + alphabet[raw[1] % 26]


def published_slugs(payload) -> list[str]:
    return [str(p.get("slug")) for p in items(payload)]


def enquiry_payload(name: str, email: str, message: str, **extra) -> dict:
    body = {"name": name, "email": email, "message": message}
    body.update(extra)
    return body


def project_payload(slug: str, **extra) -> dict:
    body = {
        "slug": slug,
        "title": "Probe Commission",
        "client": "Probe Client",
        "facets": ["Brand"],
        "summary": "A probe commission created by the reference walkthrough.",
        "credits": "Direction: Probe",
        "status": DRAFT,
    }
    body.update(extra)
    return body
