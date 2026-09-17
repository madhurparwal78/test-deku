from __future__ import annotations

import hashlib
import os
import time

import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"
AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"

PRODUCT_ORIGIN = "https://app.sheaf.example"
TEAM_SITE_SUFFIX = ".sheaf.example"
HOME_TITLE_PREFIX = "Spreadsheet Software to End Data Chaos"
HERO_HEADLINE = "Turn the spreadsheets running your business into secure applications"
HERO_PRIMARY = "Get started"
HERO_SECONDARY = "Build with a prompt"
HERO_TERTIARY = "Security for regulated industries"
CLOSING_BAND_HEADING = "Create a free site"
SHARED_CORE_CLAIM = "The structure of a database, the flexibility of a spreadsheet"
ALL_POSTS_HEADING = "All Posts"
ANNOUNCEMENT_COPY = "Looking for a Latticework alternative? See how Sheaf compares."
STAR_LABEL = "Star"
MENU_TRIGGERS = ("Product", "Solutions", "Developers", "Resources", "Pricing")
MENU_STRIP = ("Get started", "Contact sales")
CAPABILITY_HEADINGS = ("AI Assistant", "Access rules", "Forms & surveys",
                       "Flexible layout", "Visualizations", "More features")
POWER_TOOLS = ("Super-charged formulas", "Extensible", "Unprecedented control")
POWER_TOOL_LINKS = ("Sheaf for developers", "open source")
REFERENCE_CUSTOMERS = ("Northgate Digital Service", "Merrow Instruments",
                       "Halliwell Electrical")
FEATURED_TEMPLATES = ("Investment Research Tracker", "Class Enrolment Register",
                      "Customer Records Lite")
SECURITY_CARD_LINE = "Lock down insider risk by eliminating spreadsheet sprawl."
ACCESS_RULES_LINE = ("Collaborate with confidence and peace of mind, using a unique "
                     "system of granular data permissions.")
FLEXIBLE_LAYOUT_LINE = ("Arrange your data on screen to maximize the productivity of "
                        "you and your team.")
CLOSING_HEADING = "Unlock a better way to organize data."

HOME_SLUG = "/"
PUBLISHED_SECTOR_SLUG = "/solutions/nonprofit/"
DRAFT_SECTOR_SLUG = "/solutions/legal/"
DRAFT_COMPARISON_SLUG = "/lookup/rowbase/"
PUBLISHED_COMPARISON_SLUG = "/lookup/latticework/"
CASE_STUDY_INDEX_SLUG = "/case-studies/"
PRICING_SLUG = "/pricing/"
TRIAL_SLUG = "/trial/"

SEEDED_TEAM_NAME = "Merrow Instruments"
SEEDED_TEAM_SLUG = "merrow-instruments"
SEEDED_SECTOR = "nonprofit"

MEDIA_PREFIX = "media/"
SETTLE_SECONDS = 0.4
SETTLE_ATTEMPTS = 25


def settle(predicate, attempts: int = SETTLE_ATTEMPTS, delay: float = SETTLE_SECONDS):
    """Poll a bounded number of times for an asynchronous side effect."""
    outcome = None
    for _ in range(attempts):
        outcome = predicate()
        if outcome:
            return outcome
        time.sleep(delay)
    return outcome


def unique_suffix() -> str:
    return os.urandom(6).hex()


def probe_team_name() -> str:
    return f"Probe Team {unique_suffix()}"


def probe_slug(prefix: str = "/lookup/probe-") -> str:
    return f"{prefix}{unique_suffix()}/"


def sha256_of(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def expected_object_key(route_id, payload: bytes, ext: str) -> str:
    return f"{MEDIA_PREFIX}{route_id}/{sha256_of(payload)}.{ext}"


def probe_bytes() -> bytes:
    return b"sheaf-probe-" + os.urandom(24)


def body_excerpt(response) -> str:
    return response.text[:400]


@pytest.fixture(scope="session")
def app_origin() -> str:
    return appclient.app_url()


@pytest.fixture(scope="session")
def author_token() -> str:
    return appclient.login(AUTHOR_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def author2_token() -> str:
    return appclient.login(AUTHOR2_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def reader_token() -> str:
    return appclient.login(READER_EMAIL, PASSWORD)


@pytest.fixture()
def anon():
    with appclient.client() as http:
        yield http


@pytest.fixture()
def author(author_token: str):
    with appclient.client(author_token) as http:
        yield http


@pytest.fixture()
def author2(author2_token: str):
    with appclient.client(author2_token) as http:
        yield http


@pytest.fixture()
def reader(reader_token: str):
    with appclient.client(reader_token) as http:
        yield http


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()
