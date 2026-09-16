"""Fixtures, pinned literals and capability stores for the Milo Rennick Brand
Platform graders.

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

OWNER_EMAIL = "owner@example.com"
EDITOR_EMAIL = "editor@example.com"
CONTRIBUTOR_EMAIL = "contributor@example.com"
VISITOR_EMAIL = "visitor@example.com"

OWNER_ROLE = "owner"
EDITOR_ROLE = "editor"
CONTRIBUTOR_ROLE = "contributor"
VISITOR_ROLE = "visitor"

PUBLIC_STORY_IDS = ("9f3c1a7d42", "4b82e05c17", "d15a6f9b30")
SCHEDULED_STORY_ID = "7e0d4c82a6"
DRAFT_STORY_ID = "2a9b7f31c8"
REVIEW_STORY_ID = "b63e18a70f"
NON_PUBLIC_STORY_IDS = (SCHEDULED_STORY_ID, DRAFT_STORY_ID, REVIEW_STORY_ID)
SEEDED_STORY_IDS = PUBLIC_STORY_IDS + NON_PUBLIC_STORY_IDS

PUBLIC_STORY_COUNT = 3
SEEDED_STORY_COUNT = 6

STORY_STATES = ("draft", "in_review", "scheduled", "published", "unpublished", "archived")
DRAFT_STATE = "draft"
REVIEW_STATE = "in_review"
PUBLISHED_STATE = "published"
UNPUBLISHED_STATE = "unpublished"

ROUND_COUNT = 6
NEXT_ROUND_NUMBER = 4
NEXT_ROUND_CIRCUIT = "Sundown"
COMPLETE_ROUND_NUMBERS = (1, 2, 3)
SCHEDULED_ROUND_NUMBERS = (4, 5, 6)
CIRCUITS = ("Verano", "Kestrel Bay", "Aldenne", "Sundown", "Port Mira", "Caldera")
SESSION_KINDS = ("practice", "qualifying", "sprint", "race")
ROUND_CLOSED_STATES = ("complete", "cancelled")
MISSING_ROUND_STATE = "missing_review"

SEASON_YEAR = 2026
SERIES_NAME = "Prime One"
CONSTRUCTOR = "Halcyon"
DEBUT_YEAR = 2019
NICKNAME = "Milo"
MONOGRAM = "MR"
HOME_TOWN = "Bracken Hill"
HOME_COUNTRY = "Ardenia"

CLASSIFICATION_STATUSES = ("classified", "retired", "disqualified",
                           "did_not_start", "did_not_qualify")
ENQUIRY_TYPES = ("partnership", "media", "appearance", "other")
SUBSCRIBER_STATES = ("pending", "confirmed", "unsubscribed", "suppressed")
PENDING_STATUS = "pending"
CONFIRMED_STATUS = "confirmed"

ASSET_KEY_PREFIX = "assets/"
ENQUIRY_REFERENCE_PREFIX = "ENQ-"
PARTNER_CATEGORIES = ("title", "technical", "official")

PUBLIC_ROUTES = ("/", "/on-track", "/off-track", "/calendar",
                 "/legal/privacy-policy", "/legal/terms-conditions")

PRIVATE_FIELD_NAMES = ("providerId", "authorId", "scheduledFor", "version",
                       "confirmToken", "unsubscribeToken", "passwordHash")

DENIED = (401, 403)
DENIED_OR_ABSENT = (401, 403, 404)
CREATED = (200, 201)
REFUSED_AS_INVALID = (400, 409, 422)

PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)

INGEST_INSTANT_OLD = "2020-01-01T00:00:00Z"
INGEST_INSTANT_NEW = "2099-01-01T00:00:00Z"


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


def public_ids(payload) -> set:
    return {row.get("publicId") for row in payload}


def leaks(node, names=PRIVATE_FIELD_NAMES) -> set:
    """Every banned field name reachable anywhere inside a decoded payload."""
    found = set()
    if isinstance(node, dict):
        for key, value in node.items():
            if key in names:
                found.add(key)
            found |= leaks(value, names)
    elif isinstance(node, list):
        for value in node:
            found |= leaks(value, names)
    return found


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def owner_token():
    return appclient.login(OWNER_EMAIL, CORPUS_PASSWORD)


@pytest.fixture(scope="session")
def editor_token():
    return appclient.login(EDITOR_EMAIL, CORPUS_PASSWORD)


@pytest.fixture(scope="session")
def contributor_token():
    return appclient.login(CONTRIBUTOR_EMAIL, CORPUS_PASSWORD)


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

    The launch-surface routes -- the privacy page, the legal pair and the
    not-found route -- are served by the site, not by the JSON API, so they
    are reached from the root.
    """
    import httpx

    with httpx.Client(base_url=appclient.app_url(), timeout=appclient.TIMEOUT,
                      follow_redirects=True) as http:
        yield http


@pytest.fixture
def owner(owner_token):
    with appclient.client(owner_token) as http:
        yield http


@pytest.fixture
def editor(editor_token):
    with appclient.client(editor_token) as http:
        yield http


@pytest.fixture
def contributor(contributor_token):
    with appclient.client(contributor_token) as http:
        yield http


@pytest.fixture
def visitor(visitor_token):
    with appclient.client(visitor_token) as http:
        yield http
