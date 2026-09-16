from __future__ import annotations

import os
import time
import hashlib
import mimetypes

import httpx
import pytest

import appclient
import capabilities

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 30.0

APP_PASSWORD = "deku-demo-pw-2026"
EDITOR_EMAIL = "editor@example.com"
READER_EMAIL = "reader@example.com"
READER2_EMAIL = "reader2@example.com"

DRAFT_CASE_SLUG = "substation-twin"
DRAFT_CASE_NUMBER = "08"
DRAFT_CASE_CLIENT = "Kessel"
DRAFT_CASE_TITLE = "Substation Twin"

SOLUTION_SLUGS = ("cirrus", "emporium", "facet")
SOLUTION_NAMES = ("Cirrus", "Emporium", "Facet")
SERVICE_ANCHORS = ("graphics", "ui", "assets", "cloud")
SERVICE_HEADINGS = (
    "3D Web Graphics",
    "Dynamic User Interfaces",
    "3D Asset Pipelines",
    "Kubernetes Deployments for Big Data",
)
SEEDED_CASE_NUMBERS = ("01", "02", "03", "04", "05", "06", "07")
SEEDED_CASE_CLIENTS = (
    "Delta AI",
    "Corvus Europe",
    "Modellia",
    "Flowforge",
    "Corvus Europe",
    "Flowforge",
    "Kessel",
)
FIRST_CASE_TITLE = "Oil & Gas Data Visualization"

PUBLIC_ROUTES = (
    "/",
    "/cirrus/",
    "/emporium/",
    "/facet/",
    "/services/",
    "/cases/",
    "/contact/",
    "/terms/",
    "/privacy/",
    "/cookies/",
)
LEGAL_ROUTES = ("/terms/", "/privacy/", "/cookies/")
STUDIO_API_ROUTES = ("/api/enquiries", "/api/page-views")

MEDIA_KEY_PREFIX = "cases/"
OBJECT_KEY_TEMPLATE = "cases/{case_id}/{digest}{ext}"


def settle() -> None:
    time.sleep(SETTLE_SECONDS)


def unique_token() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{unique_token()}@example.com"


def probe_slug(stem: str) -> str:
    return f"{stem}-{unique_token()}"


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def expected_object_key(case_id, payload: bytes, content_type: str) -> str:
    ext = mimetypes.guess_extension(content_type) or ""
    return OBJECT_KEY_TEMPLATE.format(
        case_id=case_id, digest=sha256_hex(payload), ext=ext)


def describe(response) -> str:
    body = response.text[:400]
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}; body: {body}")


def poll_until(predicate, deadline_seconds: float = POLL_DEADLINE_SECONDS):
    deadline = time.monotonic() + deadline_seconds
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    return last


@pytest.fixture(scope="session")
def api_base() -> str:
    return appclient.api_base()


@pytest.fixture(scope="session")
def app_base() -> str:
    return appclient.app_url()


@pytest.fixture()
def anon():
    with appclient.client() as c:
        yield c


@pytest.fixture()
def editor_token() -> str:
    return appclient.login(EDITOR_EMAIL, APP_PASSWORD)


@pytest.fixture()
def reader_token() -> str:
    return appclient.login(READER_EMAIL, APP_PASSWORD)


@pytest.fixture()
def editor(editor_token):
    with appclient.client(editor_token) as c:
        yield c


@pytest.fixture()
def reader(reader_token):
    with appclient.client(reader_token) as c:
        yield c


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def site():
    with httpx.Client(base_url=appclient.app_url(), timeout=30.0,
                      follow_redirects=True) as c:
        yield c


@pytest.fixture()
def site_direct():
    with httpx.Client(base_url=appclient.app_url(), timeout=30.0) as c:
        yield c
