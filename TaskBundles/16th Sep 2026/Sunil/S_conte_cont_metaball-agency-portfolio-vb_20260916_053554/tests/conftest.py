"""Task fixtures for deku/metaball-agency-portfolio-vb.

Two rules govern this file.

Implementation agnostic. Nothing here assumes the agent's framework, file
layout, ORM or module names. The only assumptions are the App Contract (the app
answers at APP_PUBLIC_URL, HTTP API under /api) and what instruction.md pinned
explicitly: the route set, the endpoint shapes, the seeded accounts, the seeded
records, the six table names and the object-key scheme.

Provider agnostic. The domain helpers are composed from the generic primitives
in capabilities.py, never from a provider SDK, so swapping the backend or the
storage slot replaces the adapter rather than this file.
"""

from __future__ import annotations

import os
import time

import pytest
from appclient import app_url, client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

EDITOR_EMAIL = "editor@example.com"
READER_EMAIL = "reader@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"

PUBLISHED_PROJECT_ID = 1396
DRAFT_PROJECT_ID = 1435
PUBLISHED_TOPIC_ID = 1358
DRAFT_TOPIC_ID = 1364

PROJECT_TITLE = "Forest Economy Recruit"
PROJECT_CLIENT = "Midori Holdings"
FREE_TEXT_YEAR = "2025-26"
DRAFT_PROJECT_TITLE = "Shoegaze Debut Night"
TOPIC_TITLE = "Continuing Is What Showed Us"
DRAFT_TOPIC_TITLE = "Starting From Cannot"
TOPIC_DATE = "2026.3.18"

MEDIA_PREFIX = "media/"
PROJECT_MEDIA_PREFIX = "media/projects/"
MEMBER_MEDIA_PREFIX = "media/members/"

SETTLE_SECONDS = 0.25


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give an asynchronous side effect one bounded moment to land.

    The only sleep in the suite. Every caller asserts afterwards, so a slow
    environment fails on the assertion rather than on the clock.
    """
    time.sleep(seconds)


@pytest.fixture(scope="session")
def base_url() -> str:
    return app_url()


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def editor_token() -> str:
    return login(EDITOR_EMAIL, seeded_password("SEED_EDITOR_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def editor_client(editor_token: str):
    with client(editor_token) as c:
        yield c


@pytest.fixture(scope="session")
def reader_token() -> str:
    return login(READER_EMAIL, seeded_password("SEED_READER_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def reader_client(reader_token: str):
    with client(reader_token) as c:
        yield c


class StudioStore:
    """Domain queries for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def count_projects(self, **where) -> int:
        return self._b.count("projects", **where)

    def project(self, project_id: int) -> dict | None:
        return self._b.one("projects", id=project_id)

    def count_topics(self, **where) -> int:
        return self._b.count("topics", **where)

    def topic(self, topic_id: int) -> dict | None:
        return self._b.one("topics", id=topic_id)

    def members(self) -> list[dict]:
        return self._b.rows("members")

    def count_enquiries(self, **where) -> int:
        return self._b.count("enquiries", **where)

    def enquiries(self, limit: int | None = None, **where) -> list[dict]:
        return self._b.rows("enquiries", limit=limit, **where)

    def account(self, email: str) -> dict | None:
        return self._b.one("accounts", email=email)

    def project_media(self, project_id: int) -> list[dict]:
        return self._b.rows("project_media", project_id=project_id)

    def project_credits(self, project_id: int) -> list[dict]:
        return self._b.rows("project_credits", project_id=project_id)


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def store(backend: Backend) -> StudioStore:
    return StudioStore(backend)


@pytest.fixture(scope="session")
def objects() -> ObjectStore:
    return make_store()


@pytest.fixture()
def unique_suffix(request) -> str:
    """A per-test identifier that cannot collide across runs or within one."""
    return f"{request.node.name}-{os.getpid()}-{id(request)}"


@pytest.fixture()
def valid_enquiry(unique_suffix: str) -> dict:
    return {
        "enquiry_type": "enquiry",
        "name": f"Rei Sasaki {unique_suffix}",
        "company": "Harbour Works",
        "job_title": "Brand Lead",
        "email": f"rei-{unique_suffix}@example.com",
        "address": "Yokohama",
        "interests": ["digital_general", "branding", "film"],
        "timeline": "within_6_months",
        "budget_min": 1000000,
        "budget_max": 30000000,
        "message": "We are planning a brand film and a site refresh together.",
        "consent": True,
        "locale": "ja",
    }
