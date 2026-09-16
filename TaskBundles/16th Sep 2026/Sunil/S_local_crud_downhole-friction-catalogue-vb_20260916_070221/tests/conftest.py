from __future__ import annotations

import os
import time
import uuid

import httpx
import pytest

import appclient
import capabilities

SEEDED_PASSWORD = "deku-demo-pw-2026"
ENGINEER_EMAIL = "engineer@example.com"
ENGINEER2_EMAIL = "engineer2@example.com"

SEEDED_REQUEST_REF = "REQ-1001"
SEEDED_REQUEST_STATUS = "new"

REQUEST_STATUSES = ("new", "modelling", "configured", "reported", "declined")

FAMILY_CODES = ("FRS", "SVR", "TRANSFER X1", "TRANSFER X3", "TRANSFER X6")
FAMILY_VARIANTS = {
    "FRS": ("FRS-89", "FRS-102", "FRS-127", "FRS-149"),
    "SVR": ("SVR-120", "SVR-172"),
    "TRANSFER X1": ("89", "102", "127"),
    "TRANSFER X3": ("89", "102", "127"),
    "TRANSFER X6": ("89", "102", "127"),
}

CASE_COUNT = 10
SEEDED_WELL_NUMBER = "22061"
WELL_22061_DEPTH = "4,025 m"
WELL_22061_REACH = "2,938 m"
WELL_22061_TOOL_COUNT = "100"

ENGLISH_PREFIX = "/en"
PUBLIC_ROUTES = (
    "/en",
    "/en/products",
    "/en/products/frs",
    "/en/products/svr",
    "/en/products/x1",
    "/en/products/x3",
    "/en/products/x6",
    "/en/cases",
    "/en/cases/22061",
    "/en/engineering",
    "/en/about",
    "/en/contacts",
    "/en/privacy",
)

REQUEST_TABLE = "modelling_request"
SUBSCRIBER_TABLE = "subscriber"

SETTLE_SECONDS = 0.25
POLL_DEADLINE_SECONDS = 20.0

DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
REFUSED = (400, 409, 422)
CREATED = (200, 201)

NARROW_VIEWPORT = {"width": 390, "height": 844}


def settle() -> None:
    """The one sanctioned sleep in the whole layer (reference/J J.5)."""
    time.sleep(SETTLE_SECONDS)


def unique_suffix() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def wait_for(predicate, what: str):
    """Poll a predicate to a monotonic deadline. Never a bare sleep before an
    assertion that something DID happen."""
    deadline = time.monotonic() + POLL_DEADLINE_SECONDS
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    raise AssertionError(f"timed out after {POLL_DEADLINE_SECONDS}s waiting for {what}")


@pytest.fixture(scope="session")
def app_url() -> str:
    return appclient.app_url()


@pytest.fixture(scope="session")
def api_base() -> str:
    return appclient.api_base()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def engineer_token() -> str:
    return appclient.login(ENGINEER_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def engineer_client(engineer_token):
    with appclient.client(engineer_token) as c:
        yield c


@pytest.fixture()
def anon_client():
    with appclient.client() as c:
        yield c


def enquiry_payload(source_route: str = "/en/cases/22061", **overrides) -> dict:
    payload = {
        "firstName": "Marta",
        "lastName": "Ivanova",
        "email": probe_email(),
        "phone": "+7 (000) 0000001",
        "message": "Hor 90 lateral, 2,700 m reach, torque near the limit at TD.",
        "consent": True,
        "locale": "en",
        "sourceRoute": source_route,
    }
    payload.update(overrides)
    return payload


def submit_enquiry(client: httpx.Client, payload: dict) -> httpx.Response:
    return client.post("/enquiry", json=payload)


def request_rows(backend, **where) -> list:
    return backend.rows(REQUEST_TABLE, **where)


def request_count(backend, **where) -> int:
    return backend.count(REQUEST_TABLE, **where)


def find_request_ref(body: dict) -> str:
    """The reference the product shows the visitor. The field name is pinned;
    the surrounding envelope is the agent's choice, so both shapes are read."""
    if isinstance(body, dict):
        if "request_ref" in body:
            return str(body["request_ref"])
        for value in body.values():
            if isinstance(value, dict) and "request_ref" in value:
                return str(value["request_ref"])
    raise AssertionError(f"no request_ref in the submission response: {str(body)[:400]}")


def fetch(app_url: str, route: str) -> httpx.Response:
    return httpx.get(f"{app_url}{route}", timeout=appclient.TIMEOUT,
                     follow_redirects=False)


def new_page(playwright_browser, **context_kwargs):
    context = playwright_browser.new_context(**context_kwargs)
    page = context.new_page()
    return context, page


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture()
def page(browser):
    context, pg = new_page(browser)
    yield pg
    context.close()


@pytest.fixture()
def narrow_page(browser):
    context, pg = new_page(browser, viewport=NARROW_VIEWPORT)
    yield pg
    context.close()
