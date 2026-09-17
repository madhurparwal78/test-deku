"""Fixtures, stores and pinned literals for the Vesper verifier.

Every value here is pinned in instruction.md. Nothing in this file asserts;
assertions live in test_output.py.
"""

from __future__ import annotations

import os
import time
import uuid

import httpx
import pytest

import capabilities

TIMEOUT = 30.0
SETTLE_STEP = 0.25
SETTLE_LIMIT = 15.0

SEED_PASSWORD = "deku-demo-pw-2026"
CLIENT_EMAIL = "client@example.com"
CLIENT2_EMAIL = "client2@example.com"
CLIENT3_EMAIL = "client3@example.com"
CURATOR_EMAIL = "curator@example.com"
CLIENT_NAME = "Nadia Fell"
CLIENT2_NAME = "Tomas Renn"
CLIENT3_NAME = "Priya Sandoval"
CURATOR_NAME = "Imogen Shaw"

PROJECT_COUNT = 15
SIGNAL_COUNT = 10
CLIENT_MARK_COUNT = 12
AWARD_COUNT = 4
REEL_CEILING = 12
TITLE_MAX = 80
NOTE_MAX = 280
BRIEF_MAX = 2000
DISPLAY_NAME_MAX = 60
PASSWORD_MIN = 8
PASSWORD_MAX = 200

PRACTICE_SLUGS = ["brand-identity", "website", "visuals", "extended-reality"]
PRACTICE_LABELS = ["All", "Brand Identity", "Website", "Visuals", "Extended Reality"]
SIGNAL_KINDS = ["editorial", "events", "news"]
JOURNAL_LABELS = ["All", "Editorial", "Events", "News"]

FIRST_PROJECT_SLUG = "nightshift"
SECOND_PROJECT_SLUG = "ferrous"
THIRD_PROJECT_SLUG = "kiln-house"
MULTI_FIELD_SLUGS = ["second-skin", "tessellate", "oxbow"]
ARCHIVE_SLUGS = [
    "nightshift", "ferrous", "kiln-house", "second-skin", "cold-open",
    "marrow", "halyard", "tessellate", "drylands", "pale-horse",
    "foundry-row", "oxbow", "signal-box", "quiet-mile", "lantern",
]
FIRST_SIGNAL_SLUG = "the-long-take"
JOURNAL_SLUGS = [
    "the-long-take", "notes-from-the-floor", "against-the-grid",
    "a-room-with-no-corners", "studio-of-the-year", "six-weeks-in-ceramic",
    "open-house", "ferrous-goes-live", "light-as-material", "the-first-reel",
]

DEFAULT_REEL_TITLE = "Untitled reel"
STATE_EMPTY = "empty"
STATE_DRAFT = "draft"
STATE_SENT = "sent"
STATE_ANSWERED = "answered"
ROLE_CLIENT = "client"
ROLE_CURATOR = "curator"

STUDIO_ADDRESS = "contact@vesper.works"
WELCOME_SUBJECT = "Vesper: your reel"
RESET_SUBJECT = "Vesper: reset your password"
CLIENT_SEND_SUBJECT = "Vesper: we have your reel"
STUDIO_SEND_SUBJECT_PREFIX = "New reel from "

HOME_TITLE = "Vesper - Creative Innovation and Digital Futures"
ARCHIVE_TITLE = "Our Portfolio - Vesper"
JOURNAL_TITLE = "Signals"
REEL_TITLE = "Your reel - Vesper"
PRIVACY_ROUTE = "/legal/imprint-privacy-policy"
TERMS_ROUTE = "/legal/terms"
PUBLIC_ROUTES = ["/", "/work", "/blog", "/contact", PRIVACY_ROUTE, TERMS_ROUTE]

REFUSAL_ALREADY_REGISTERED = "That email is already registered"
REFUSAL_SIGN_IN = "That email and password do not match"
REFUSAL_EMPTY_REEL = "Add at least one project"
REFUSAL_CEILING = "A reel holds twelve projects at most"
REFUSAL_NO_TITLE = "Give the reel a name"
REFUSAL_BRIEF_LONG = "The brief is too long"
REFUSAL_NOTE_LONG = "A note is too long"
REFUSAL_WITHDRAWN = "One of your projects is no longer available"
REFUSAL_ALREADY_SENT = "This reel has already been sent"

CLIENT_ERROR = range(400, 500)
OK_CREATED = (200, 201)
DENIED = (401, 403)
REFUSED = (400, 409, 422)


def app_url() -> str:
    return os.environ["APP_PUBLIC_URL"].rstrip("/")


def api_base() -> str:
    return f"{app_url()}/api"


def excerpt(response: httpx.Response) -> str:
    return response.text[:300]


def settle(predicate, limit: float = SETTLE_LIMIT):
    """Poll a predicate until it returns a truthy value, or give up.

    The only sanctioned sleep in this layer. Returns whatever the predicate
    last returned, so a caller asserts on the value rather than on the wait.
    """
    deadline = time.monotonic() + limit
    value = predicate()
    while not value and time.monotonic() < deadline:
        time.sleep(SETTLE_STEP)
        value = predicate()
    return value


def probe_email() -> str:
    return f"probe-{uuid.uuid4().hex[:12]}@example.com"


def anon() -> httpx.Client:
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT)


def sign_in(email: str, password: str = SEED_PASSWORD) -> httpx.Response:
    with anon() as client:
        return client.post("/auth/sign-in", json={"email": email, "password": password})


def token_for(email: str, password: str = SEED_PASSWORD) -> str:
    response = sign_in(email, password)
    assert response.status_code == 200, (
        f"POST /api/auth/sign-in for {email} returned {response.status_code}, "
        f"expected 200: {excerpt(response)}"
    )
    body = response.json()
    token = body.get("access_token")
    assert token, (
        f"POST /api/auth/sign-in for {email} returned 200 with no access_token "
        f"field: {excerpt(response)}"
    )
    return token


def bearer(token: str) -> httpx.Client:
    return httpx.Client(
        base_url=api_base(),
        timeout=TIMEOUT,
        headers={"Authorization": f"Bearer {token}"},
    )


def create_account(display_name: str | None = None,
                   email: str | None = None,
                   password: str = SEED_PASSWORD) -> tuple[str, str]:
    """Create a fresh account and return its address with its bearer token."""
    email = email or probe_email()
    display_name = display_name or "Probe Client"
    with anon() as client:
        response = client.post(
            "/auth/sign-up",
            json={"display_name": display_name, "email": email, "password": password},
        )
    assert response.status_code in OK_CREATED, (
        f"POST /api/auth/sign-up for {email} returned {response.status_code}, "
        f"expected one of {OK_CREATED}: {excerpt(response)}"
    )
    token = response.json().get("access_token") or token_for(email, password)
    return email, token


def read_reel(client: httpx.Client) -> dict:
    response = client.get("/reel")
    assert response.status_code == 200, (
        f"GET /api/reel returned {response.status_code}, expected 200: "
        f"{excerpt(response)}"
    )
    return response.json()


def reel_items(payload: dict) -> list[dict]:
    items = payload.get("items")
    assert isinstance(items, list), (
        f"GET /api/reel returned no top-level items array: {str(payload)[:300]}"
    )
    return items


def add_project(client: httpx.Client, project_id: str) -> httpx.Response:
    return client.post("/reel/items", json={"project_id": project_id})


def project_rows() -> list[dict]:
    with anon() as client:
        response = client.get("/projects")
    assert response.status_code == 200, (
        f"GET /api/projects returned {response.status_code}, expected 200: "
        f"{excerpt(response)}"
    )
    rows = response.json()
    assert isinstance(rows, list), (
        f"GET /api/projects did not return a top-level JSON array: "
        f"{str(rows)[:300]}"
    )
    return rows


def project_id_by_slug(slug: str) -> str:
    for row in project_rows():
        if row.get("slug") == slug:
            return str(row["id"])
    raise AssertionError(
        f"GET /api/projects carries no project with slug {slug!r}; the fifteen "
        f"seeded slugs are pinned in the brief"
    )


def fill_reel(client: httpx.Client, count: int) -> list[str]:
    """Add `count` distinct seeded projects to the caller's reel."""
    added = []
    for slug in ARCHIVE_SLUGS[:count]:
        response = add_project(client, project_id_by_slug(slug))
        assert response.status_code in OK_CREATED, (
            f"POST /api/reel/items for {slug!r} returned {response.status_code}, "
            f"expected one of {OK_CREATED}: {excerpt(response)}"
        )
        added.append(str(response.json()["item"]["id"]))
    return added


def set_order(client: httpx.Client, order: list[str]) -> httpx.Response:
    return client.put("/reel/order", json={"order": order})


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture()
def anonymous():
    with anon() as client:
        yield client


@pytest.fixture()
def client_token():
    return token_for(CLIENT_EMAIL)


@pytest.fixture()
def curator_token():
    return token_for(CURATOR_EMAIL)


@pytest.fixture()
def curator():
    with bearer(token_for(CURATOR_EMAIL)) as client:
        yield client


@pytest.fixture()
def fresh_client():
    """A brand new account with an empty reel, so a test never mutates a seed."""
    email, token = create_account()
    with bearer(token) as client:
        client.probe_email = email
        yield client
