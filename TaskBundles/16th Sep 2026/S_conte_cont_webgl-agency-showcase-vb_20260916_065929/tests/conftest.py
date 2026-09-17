"""Fixtures, pinned literals and capability stores for the Spectre Studio
Showcase graders.

Every literal here is pinned verbatim in instruction.md. Nothing is inferred
from the agent's implementation: the app is reached over HTTP on its own
origin, and the two backing services are read through the shared capability
adapters.
"""

from __future__ import annotations

import os
import time

import pytest

import appclient
import capabilities

CORPUS_PASSWORD = appclient.seeded_password("DEKU_SEED_PASSWORD", "deku-demo-pw-2026")

CURATOR_EMAIL = "curator@example.com"
VISITOR_EMAIL = "visitor@example.com"

PUBLISHED_SLUGS = (
    "beacon-world-cup-2026",
    "free-signals-center",
    "powering-progress",
    "transforming-ventures",
    "campus-visitor-guide",
    "midnight-woods-tour",
)
DRAFT_SLUGS = ("brand-standards", "handset-for-travel")
SEEDED_SLUGS = PUBLISHED_SLUGS + DRAFT_SLUGS

PUBLISHED_COUNT = 6
SEEDED_COUNT = 8

OPEN_ROLE_SLUGS = (
    "frontend-engineer-ldn",
    "senior-partnerships-manager-ldn",
    "design-lead-ldn",
    "designer-ldn",
)
CLOSED_ROLE_SLUG = "motion-designer-akl"

DISCIPLINES = ("Experience", "Communication", "Product")
INTENTS = ("collaboration", "hiring", "anything-else")
READINESS_STOPS = (0, 1, 2)

PROJECT_KEY_PREFIX = "projects/"
APPLICATION_KEY_PREFIX = "applications/"
ENQUIRY_REFERENCE_PREFIX = "ENQ-"
APPLICATION_REFERENCE_PREFIX = "WLD-"

DRAFT_STATUS = "draft"
PUBLISHED_STATUS = "published"

CURATOR_ROLE = "curator"
VISITOR_ROLE = "visitor"

DENIED = (401, 403)
DENIED_OR_ABSENT = (401, 403, 404)
CREATED = (200, 201)
REFUSED_AS_INVALID = (400, 409, 422)

PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


def unique_token() -> str:
    """A per-run identifier so a repeated sweep never collides with itself."""
    return os.urandom(6).hex()


def settle(predicate, timeout: float = 20.0, interval: float = 0.5):
    """Poll a predicate to a definite end state, bounded by a monotonic clock."""
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        time.sleep(interval)
    return last


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def curator_token():
    return appclient.login(CURATOR_EMAIL, CORPUS_PASSWORD)


@pytest.fixture(scope="session")
def visitor_token():
    return appclient.login(VISITOR_EMAIL, CORPUS_PASSWORD)


@pytest.fixture
def anon():
    with appclient.client() as http:
        yield http


@pytest.fixture
def site():
    """A client at the app's own origin rather than under the /api prefix.

    The launch-surface routes -- the privacy page, the terms page, the sitemap
    and the robots file -- are served by the site, not by the JSON API, so they
    are reached from the root.
    """
    import httpx

    with httpx.Client(base_url=appclient.app_url(), timeout=appclient.TIMEOUT,
                      follow_redirects=True) as http:
        yield http


@pytest.fixture
def curator(curator_token):
    with appclient.client(curator_token) as http:
        yield http


@pytest.fixture
def visitor(visitor_token):
    with appclient.client(visitor_token) as http:
        yield http
