"""Fixtures, pinned literals and helpers for the Design Agent Showcase graders.

No test_ function lives here. Every value the module asserts about the seeded
world is pinned in this file and appears verbatim in instruction.md: a grader
that asserts a value the brief never pinned grades a working app as broken.
Probe values minted per run are only ever compared against themselves.

The shared grader (appclient, capabilities, _shapes) is supplied by the
deku-verifier-base image on PYTHONPATH=/tests. Nothing here re-implements it and
nothing here imports a provider driver.
"""

from __future__ import annotations

import concurrent.futures
import re
import uuid

import pytest

import appclient
import capabilities

SEEDED_PASSWORD = "deku-demo-pw-2026"

AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"

AUTHOR_NAME = "Marek Vantly"
AUTHOR2_NAME = "Elian Brooks"
READER_NAME = "Priya Raman"

ROLE_AUTHOR = "author"
ROLE_READER = "reader"

STATE_DRAFT = "draft"
STATE_PUBLISHED = "published"
ACCESS_OPEN = "open"
ACCESS_MEMBERS = "members"

OPEN_SLUG = "loopwork-ai-search-brand-site"
OPEN_TITLE = "How Loopwork launched their AI search brand site"
SECOND_OPEN_SLUG = "ledgera-marketing-site-redesign"
SECOND_OPEN_TITLE = "How Ledgera redesigned their marketing site"
THIRD_OPEN_SLUG = "zaptask-global-fan-experience"
MEMBERS_SLUG = "vega-community-platform"
MEMBERS_TITLE = "How Vega rebuilt their community platform"
DRAFT_SLUG = "calday-landing-pages"
DRAFT_TITLE = "How Calday ships landing pages 10x faster"

CATEGORY_AI = "AI"
CATEGORY_ENTERPRISE = "Enterprise"
CATEGORY_DESIGN = "Design"
CATEGORY_SAAS = "SaaS"
CATEGORIES = ("AI", "Enterprise", "Sports", "Design", "SaaS", "Consumer", "Startup")

SCAN_STATUS_QUEUED = "queued"
SCAN_STATUS_RUNNING = "running"
SCAN_STATUS_COMPLETE = "complete"
SCAN_GRADES = ("strong", "adequate", "weak")
SCAN_SECTIONS = ("discoverability", "structure-and-metadata",
                 "trust-signals", "answerability")
SCAN_REFERENCE_RE = re.compile(r"^scan-[0-9a-f]{12}$")
SCAN_TARGET = "yoursite.com"
SCAN_FIRST_NAME = "Dana"
SCAN_LAST_NAME = "Whitfield"
SCAN_BUSINESS_EMAIL = "dana@northpost.co"
CONSUMER_MAIL_DOMAINS = ("gmail.com", "outlook.com", "yahoo.com",
                         "hotmail.com", "icloud.com")

SUBSCRIBER_PENDING = "pending"
SUBSCRIBER_CONFIRMED = "confirmed"
MESSAGE_SOURCE_NOT_FOUND = "not-found"
MESSAGE_SOURCE_ENTERPRISE = "enterprise"

HERO_METRIC_LINE = "#15 on the open model index: 377.8B tokens this week"
NOT_FOUND_HEADING = "Page not found"
COOKIE_COPY = ("We use cookies to personalize content, run ads, and analyze "
               "traffic. Read our Cookie Policy.")

COVER_KEY_PREFIX = "stories"
ACCEPTED_IMAGE_TYPES = ("image/png", "image/jpeg", "image/webp")
COVER_ALT_TEXT = "Illustration of a stack"

CREDENTIALS_FILE = "/app/USER_README.md"
SCREENSHOT_DIR = "/app/.browser_screenshots"
DOWNLOAD_DIR = "/app/.downloads"

MIN_CONTRAST_RATIO = "4.5:1"
MIN_TARGET_SIZE = "44x44"
CONTAINER_PORT = "4173"

PNG_BYTES = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
    "890000000a49444154789c6360000002000100ffff0300000600055773d8d100"
    "00000049454e44ae426082")
GIF_BYTES = bytes.fromhex(
    "47494638396101000100800000000000ffffff21f90401000000002c00000000"
    "010001000002024401003b")


def describe(response, expectation: str) -> str:
    return (f"{expectation}; got status {response.status_code} with body "
            f"{response.text[:400]}")


def probe_slug(label: str) -> str:
    return f"probe-{label}-{uuid.uuid4().hex[:10]}"


def probe_email(label: str) -> str:
    return f"probe-{label}-{uuid.uuid4().hex[:10]}@northpost.co"


def backend():
    return capabilities.make_backend()


def store():
    return capabilities.make_store()


def stories_path() -> str:
    return "/stories"


def studio_stories_path() -> str:
    return "/studio/stories"


def scans_path() -> str:
    return "/scans"


def subscribers_path() -> str:
    return "/subscribers"


def messages_path() -> str:
    return "/messages"


def leads_path() -> str:
    return "/studio/leads"


def story_row(slug: str) -> dict | None:
    return backend().one("stories", slug=slug)


def story_id(slug: str) -> int:
    row = story_row(slug)
    assert row is not None, f"the seeded story {slug} must exist as a stored row"
    return row["id"]


def rows_of(payload) -> list:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "stories", "results", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def create_probe_story(token: str, slug: str, access: str = ACCESS_OPEN) -> dict:
    with appclient.client(token) as client:
        response = client.post(studio_stories_path(), json={
            "title": f"How Metricly rebuilt its docs in a week {slug}",
            "slug": slug,
            "category": CATEGORY_DESIGN,
            "intro": "A short opening for a probe story.",
            "body": "A longer body for a probe story.",
            "access": access,
        })
    assert response.status_code < 300, describe(
        response, f"an author must be able to create the story {slug}")
    return response.json()


def settle(seconds: float = 0.4) -> None:
    import time
    time.sleep(seconds)


def wait_for_scan(reference: str, tries: int = 30) -> dict:
    with appclient.client(None) as client:
        for _ in range(tries):
            response = client.get(f"{scans_path()}/{reference}")
            assert response.status_code == 200, describe(
                response, f"the scan {reference} must be readable by its reference")
            payload = response.json()
            if payload.get("status") == SCAN_STATUS_COMPLETE:
                return payload
            settle(1.0)
    raise AssertionError(
        f"the scan {reference} never reached status {SCAN_STATUS_COMPLETE}; a "
        f"submitted scan must advance without further visitor action")


def submit_scan(business_email: str, target: str = SCAN_TARGET) -> dict:
    with appclient.client(None) as client:
        response = client.post(scans_path(), json={
            "url": target,
            "first_name": SCAN_FIRST_NAME,
            "last_name": SCAN_LAST_NAME,
            "business_email": business_email,
        })
    assert response.status_code < 300, describe(
        response, f"a well formed scan submission for {target} must be accepted")
    return response.json()


def run_together(first, second) -> list:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(first), pool.submit(second)]
        return [future.result(timeout=60) for future in futures]


@pytest.fixture()
def author_token() -> str:
    return appclient.login(AUTHOR_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def author2_token() -> str:
    return appclient.login(AUTHOR2_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def reader_token() -> str:
    return appclient.login(READER_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def fresh_reader_token() -> str:
    email = probe_email("reader")
    with appclient.client(None) as client:
        response = client.post("/auth/signup", json={
            "email": email,
            "password": SEEDED_PASSWORD,
            "display_name": "Probe Reader",
        })
    assert response.status_code < 300, describe(
        response, f"signup must create a {ROLE_READER} account for {email}")
    return appclient.login(email, SEEDED_PASSWORD)
