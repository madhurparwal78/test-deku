from __future__ import annotations

import os
import time

import httpx
import pytest

import appclient
import capabilities

TIMEOUT = 30.0
SETTLE_SECONDS = 0.5
SETTLE_ATTEMPTS = 20

PASSWORD = "deku-demo-pw-2026"
AUTHOR_EMAIL = "author@example.com"
READER_EMAIL = "reader@example.com"

PUBLIC_ROUTES = ("/", "/work", "/press", "/team", "/services", "/contact", "/privacy")
DISCIPLINES = ("SPATIAL", "Campaign", "Photography", "Brand design", "Video",
               "Digital", "Illustration")
PRESS_CATEGORIES = ("News", "Events", "Features", "Articles")
PRESS_COUNTS = (("News", 2), ("Events", 2), ("Features", 3), ("Articles", 0))

PUBLISHED_PROJECT_COUNT = 8
DRAFT_PROJECT_TITLE = "AMBERLINE ‣ STUDIO REBRAND"
FEATURED_HOME_COUNT = 4
PRESS_ITEM_COUNT = 7
SERIES_VOLUMES = ("Vol 01", "Vol 02", "Vol 03")
TEAM_MEMBER_COUNT = 11
STUDIO_CHAPTER_YEARS = ("2011", "2019")
CLIENT_MARKER = "‣"

COVER_KEY_PREFIX = "projects/"
PRESS_KIT_KEY_PREFIX = "press-kits/"
DECOY_FIELD = "company_website"
ENQUIRY_WINDOW_SECONDS = 60

USER_README = "/app/USER_README.md"
SCREENSHOT_DIR = "/app/.browser_screenshots"
DOWNLOAD_DIR = "/app/.downloads"

DENIED = (401, 403)
NOT_FOUND = (404,)
CREATED = (200, 201)
REFUSED = (400, 409, 422, 429)


def settle(check, attempts: int = SETTLE_ATTEMPTS, seconds: float = SETTLE_SECONDS):
    """Poll `check` until it returns a truthy value, bounded. The one sanctioned sleep."""
    result = None
    for _ in range(attempts):
        result = check()
        if result:
            return result
        time.sleep(seconds)
    return result


def unique_email(prefix: str) -> str:
    return f"{prefix}-{os.urandom(6).hex()}@example.com"


def unique_slug(prefix: str) -> str:
    return f"{prefix}-{os.urandom(6).hex()}"


def describe(response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}: {response.text[:400]}")


def payload(response):
    assert response.headers.get("content-type", "").startswith("application/json"), (
        f"expected a JSON body, got {describe(response)}")
    return response.json()


@pytest.fixture(scope="session")
def app_url() -> str:
    return appclient.app_url()


@pytest.fixture(scope="session")
def api_base() -> str:
    return appclient.api_base()


@pytest.fixture(scope="session")
def author_token() -> str:
    return appclient.login(AUTHOR_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def reader_token() -> str:
    return appclient.login(READER_EMAIL, PASSWORD)


@pytest.fixture()
def anon():
    with appclient.client() as client:
        yield client


@pytest.fixture()
def as_author(author_token):
    with appclient.client(author_token) as client:
        yield client


@pytest.fixture()
def as_reader(reader_token):
    with appclient.client(reader_token) as client:
        yield client


@pytest.fixture()
def site():
    with httpx.Client(base_url=appclient.app_url(), timeout=TIMEOUT,
                      follow_redirects=True) as client:
        yield client


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def draft_project(as_author):
    slug = unique_slug("probe-project")
    response = as_author.post("/projects", json={
        "title": f"PROBE {CLIENT_MARKER} DRAFT {slug}",
        "client": "PROBE STUDIO",
        "slug": slug,
        "disciplines": ["Digital"],
    })
    assert response.status_code in CREATED, describe(response)
    body = payload(response)
    assert "id" in body, f"created project carries no id: {describe(response)}"
    return body
