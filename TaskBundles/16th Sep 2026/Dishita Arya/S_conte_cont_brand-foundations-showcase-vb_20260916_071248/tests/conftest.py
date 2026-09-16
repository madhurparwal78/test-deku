"""Fixtures, stores and pinned literals for the Latticework Foundations verifier.

Every value here is pinned in instruction.md. Nothing in this file asserts;
assertions live in test_output.py.
"""

from __future__ import annotations

import hashlib
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
AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"
SEED_TRIAL_EMAIL = "hollis@example.com"
AUTHOR_NAME = "Wren Calloway"
AUTHOR2_NAME = "Osian Petrie"
READER_NAME = "Marit Sandoval"

ROLE_AUTHOR = "author"
ROLE_READER = "reader"

CHAPTER_SLUGS = ["color", "logo", "typography", "photography", "motion"]
PUBLISHED_SLUGS = ["color", "logo"]
DRAFT_SLUGS = ["typography", "photography", "motion"]
OTHER_AUTHOR_DRAFT = "motion"
INDEX_LABELS = {"color": "01", "logo": "02", "typography": "03",
                "photography": "04", "motion": "05"}
CARD_EYEBROWS = ["( Color )", "( Logo )", "( Typography )",
                 "( Photography )", "( Motion )"]

TONE_GROUPS = ["Core", "Dark", "Bright", "Light"]
TIERS = ["desktop", "tablet", "mobile"]
TONE_STOP_COUNT = len(TONE_GROUPS) * len(TIERS)
SECTION_KINDS = ["intro", "tone-group", "poster-stack", "rules", "in-use", "cta"]
COLOUR_SECTION_COUNT = 9
LOGO_SECTION_COUNT = 5
COLOUR_CAPTION_COUNT = 9
LOGO_CAPTION_COUNT = 7
FIRST_COLOUR_CAPTION = "Primary, Product UI"
FIRST_LOGO_CAPTION = "Logo, Maker Community, Campaign"
TEMPLATE_NAMES = ["Meridian", "Kiln", "Atelier"]

LOCALE = "en"
WORDMARK = "Latticework Foundations"
INDEX_CONTROL = "Index"
LOADER_TEXT = "Loading"
LOADER_FIGURE = "100%"
TAP_TO_EXPLORE = "Tap to Explore"
TRIAL_TITLE = "A website makes it real"
TRIAL_BODY = "Get your free website trial today. No credit card required."
TRIAL_SUCCESS = "Thank you. You are on the list."
TRIAL_FAILURE = "Something went wrong, please try again."
NOT_FOUND_LINE = "404: Page not found"
SWATCH_LABEL = "HEX"
SHUFFLE_CONTROL = "Shuffle Color"
EXPLORE_COLORS = "Explore Colors"
ENDPOINTS_HEADING = "Lambda Endpoints Test"

PUBLIC_ROUTES = ["/", "/color", "/logo", "/menu", "/webgl"]
AUTHOR_ROUTES = ["/studio", "/studio/trials", "/lambda"]
WIZARD_ROUTES = ["/studio/chapters/new/details", "/studio/chapters/new/sections",
                 "/studio/chapters/new/media", "/studio/chapters/new/review"]
SITEMAP_ROUTE = "/sitemap.xml"
ROBOTS_ROUTE = "/robots.txt"
FAVICON_ROUTE = "/favicon.ico"

MEDIA_KEY_EXAMPLE = "core-poster-01"
OBJECT_PREFIX = "media/"
CONTRAST_BODY = 4.5
CONTRAST_LARGE = 3.0

CLIENT_ERROR = range(400, 500)
OK_CREATED = (200, 201)
DENIED = (401, 403, 404)
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


def probe_slug() -> str:
    return f"probe-{uuid.uuid4().hex[:10]}"


def anon() -> httpx.Client:
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, follow_redirects=False)


def site() -> httpx.Client:
    return httpx.Client(base_url=app_url(), timeout=TIMEOUT, follow_redirects=False)


def bearer(token: str) -> httpx.Client:
    return httpx.Client(
        base_url=api_base(),
        timeout=TIMEOUT,
        follow_redirects=False,
        headers={"Authorization": f"Bearer {token}"},
    )


def sign_in(email: str, password: str = SEED_PASSWORD) -> httpx.Response:
    with anon() as client:
        return client.post("/auth/sign-in", json={"email": email, "password": password})


def token_of(payload: dict) -> str | None:
    for key in ("access_token", "token", "bearer_token"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def token_for(email: str, password: str = SEED_PASSWORD) -> str:
    response = sign_in(email, password)
    assert response.status_code == 200, (
        f"POST /api/auth/sign-in for {email} returned {response.status_code}, "
        f"expected 200: {excerpt(response)}"
    )
    token = token_of(response.json())
    assert token, (
        f"POST /api/auth/sign-in for {email} returned 200 with no bearer token "
        f"field: {excerpt(response)}"
    )
    return token


def sign_up(email: str | None = None, password: str = SEED_PASSWORD,
            display_name: str = "Probe Reader", **extra) -> httpx.Response:
    body = {"email": email or probe_email(), "password": password,
            "display_name": display_name}
    body.update(extra)
    with anon() as client:
        return client.post("/auth/sign-up", json=body)


def new_reader() -> tuple[str, str]:
    """Create a fresh reader account and return its address with a token."""
    email = probe_email()
    response = sign_up(email=email)
    assert response.status_code in OK_CREATED, (
        f"POST /api/auth/sign-up for {email} returned {response.status_code}, "
        f"expected one of {OK_CREATED}: {excerpt(response)}"
    )
    return email, token_of(response.json()) or token_for(email)


def chapter_rows(client: httpx.Client) -> list[dict]:
    response = client.get("/chapters")
    assert response.status_code == 200, (
        f"GET /api/chapters returned {response.status_code}, expected 200: "
        f"{excerpt(response)}"
    )
    rows = response.json()
    assert isinstance(rows, list), (
        f"GET /api/chapters did not return a top-level JSON array: {str(rows)[:300]}"
    )
    return rows


def chapter_by_slug(rows: list[dict], slug: str) -> dict | None:
    for row in rows:
        if row.get("slug") == slug:
            return row
    return None


def sections_of(client: httpx.Client, slug: str) -> list[dict]:
    response = client.get(f"/chapters/{slug}/sections")
    assert response.status_code == 200, (
        f"GET /api/chapters/{slug}/sections returned {response.status_code}, "
        f"expected 200: {excerpt(response)}"
    )
    rows = response.json()
    assert isinstance(rows, list), (
        f"GET /api/chapters/{slug}/sections did not return a top-level JSON array: "
        f"{str(rows)[:300]}"
    )
    return rows


def section_ids(rows: list[dict]) -> list[str]:
    return [str(row["id"]) for row in rows]


def positions(rows: list[dict]) -> list[int]:
    return [int(row["position"]) for row in rows]


def create_chapter(client: httpx.Client, slug: str | None = None) -> dict:
    slug = slug or probe_slug()
    response = client.post("/chapters", json={
        "slug": slug, "index_label": "09", "eyebrow": f"( {slug} )",
        "title": "Probe", "lead": "A probe chapter written by the verifier.",
    })
    assert response.status_code in OK_CREATED, (
        f"POST /api/chapters for {slug!r} returned {response.status_code}, "
        f"expected one of {OK_CREATED}: {excerpt(response)}"
    )
    body = response.json()
    return body.get("chapter", body)


def add_section(client: httpx.Client, slug: str, heading: str,
                kind: str = "intro") -> dict:
    response = client.post(f"/chapters/{slug}/sections", json={
        "kind": kind, "eyebrow": "( Probe )", "index_label": "01",
        "heading": heading, "body": "A probe section written by the verifier.",
    })
    assert response.status_code in OK_CREATED, (
        f"POST /api/chapters/{slug}/sections returned {response.status_code}, "
        f"expected one of {OK_CREATED}: {excerpt(response)}"
    )
    body = response.json()
    return body.get("section", body)


def media_rows(client: httpx.Client, slug: str) -> list[dict]:
    """Every media row reachable through a chapter's sections."""
    out = []
    for section in sections_of(client, slug):
        for ref in section.get("media") or []:
            out.append(ref)
    return out


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def submit_trial(email: str, slug: str = "color") -> httpx.Response:
    with anon() as client:
        return client.post("/trials",
                           json={"email": email, "source_chapter_slug": slug})


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def anonymous():
    with anon() as client:
        yield client


@pytest.fixture()
def public():
    with site() as client:
        yield client


@pytest.fixture()
def author():
    with bearer(token_for(AUTHOR_EMAIL)) as client:
        yield client


@pytest.fixture()
def other_author():
    with bearer(token_for(AUTHOR2_EMAIL)) as client:
        yield client


@pytest.fixture()
def reader():
    with bearer(token_for(READER_EMAIL)) as client:
        yield client


@pytest.fixture()
def fresh_reader():
    """A brand new reader account, so a test never mutates a seeded one."""
    email, token = new_reader()
    with bearer(token) as client:
        client.probe_email = email
        yield client
