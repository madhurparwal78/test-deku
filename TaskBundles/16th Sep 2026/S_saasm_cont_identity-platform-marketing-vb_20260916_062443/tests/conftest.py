from __future__ import annotations

import hashlib
import os
import re
import time
import uuid

import httpx
import pytest

import appclient
import capabilities

TIMEOUT = 30.0
SETTLE_STEP = 0.25
SETTLE_LIMIT = 20.0

CORPUS_PASSWORD = "deku-demo-pw-2026"
AUTHOR_EMAIL = "author@example.com"
SECOND_AUTHOR_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"

PUBLIC_ROUTES = (
    "/",
    "/user-authentication",
    "/multi-tenancy",
    "/billing",
    "/react-authentication",
    "/nextjs-authentication",
    "/expo-authentication",
    "/agents",
    "/cli",
    "/pricing",
    "/docs",
    "/changelog",
    "/glossary",
    "/llm-leaderboard",
    "/components/theme-editor",
    "/blog",
    "/company",
    "/careers",
    "/startups",
    "/security",
    "/contact",
    "/brand-assets",
    "/legal",
    "/legal/privacy",
    "/legal/standard-terms",
    "/legal/website-terms",
    "/sign-in",
    "/sign-up",
)

ENTRY_KINDS = ("doc", "changelog", "glossary", "blog", "legal")
PLAN_CODES = ("hobby", "pro", "business", "enterprise")
CELL_BANDS = ("above", "below", "bottom-decile", "absent")
CONSENT_STATES = ("granted", "declined", "undecided")
INSTANCE_STATES = ("pending", "provisioning", "live", "failed")
COMPLIANCE_STATUSES = ("Held", "Not applicable", "Not offered")
DOC_VERSIONS = ("Core 3", "Core 2", "Core 1")
INERT_LETTERS = ("k", "q", "x", "y")
THEME_PRESETS = ("Default", "Dark", "Simple", "Library")
THEME_FIELDS = (
    "primary",
    "background",
    "foreground",
    "foreground_primary",
    "neutral",
    "muted",
    "foreground_muted",
    "ring",
    "input",
    "input_foreground",
    "border",
    "shadow",
    "modal_backdrop",
    "success",
    "warning",
    "danger",
)
TASK_FAMILIES = (
    "Organizations",
    "Billing",
    "Webhooks",
    "Add Auth",
    "Auth",
    "Quickstarts",
    "UI Components",
    "Upgrades",
    "User Management",
)
NOT_FOUND_LINE = "Sorry, we can't find the page you're looking for."
NOT_FOUND_ACTION = "Go to homepage"
SKIP_LINK_COPY = "Skip to main content"
TRUST_STRIP_CAPTION = "Trusted by fast-growing companies around the world."
COPIED_LABEL = "Copied!"
CAREERS_EMPTY_LINE = "We don't have any open positions at the moment."
PRIVACY_EMAIL = "privacy@aegis.dev"
OBJECT_KEY_RE = re.compile(r"^library/\d+/[0-9a-f]{64}\.[A-Za-z0-9]+$")
BINARY_ASSET_RE = re.compile(
    r"\.(?:woff2?|ttf|otf|eot|jpe?g|png|gif|webp|avif|bmp|ico|mp4|webm|mov|m4v)\b",
    re.IGNORECASE,
)
FAVICON_DECLARATION_RE = re.compile(r"<link[^>]+rel=[\"'][^\"']*icon[^\"']*[\"']", re.IGNORECASE)
META_DESCRIPTION_RE = re.compile(
    r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"']([^\"']*)[\"']", re.IGNORECASE
)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
NARROW_VIEWPORT_WIDTH = 390

ONE_PIXEL_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
    "890000000a49444154789c6360000002000100ffff03000006000557bfabd400"
    "00000049454e44ae426082"
)
SECOND_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000020000000108060000007f1900"
    "d80000001149444154789c6360606060000000050001a5f645bf000000004945"
    "4e44ae426082"
)


def settle(seconds: float = SETTLE_STEP) -> None:
    """The one sanctioned pause. A raw sleep in a test module is a finding."""
    time.sleep(seconds)


def unique_suffix() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def probe_slug(stem: str = "probe") -> str:
    return f"{stem}-{unique_suffix()}"


def digest_of(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def app_url() -> str:
    return appclient.app_url()


def api_base() -> str:
    return appclient.api_base()


def page(path: str, *, width: int | None = None) -> httpx.Response:
    headers = {}
    if width is not None:
        headers["Viewport-Width"] = str(width)
    return httpx.get(f"{app_url()}{path}", timeout=TIMEOUT, headers=headers,
                     follow_redirects=False)


def rendered(path: str, *, width: int | None = None) -> str:
    response = page(path, width=width)
    assert response.status_code in (200, 304), (
        f"GET {path} returned {response.status_code} rather than a rendered page: "
        f"{response.text[:300]}"
    )
    return response.text


def token_for(email: str) -> str:
    return appclient.login(email, CORPUS_PASSWORD)


def as_author() -> httpx.Client:
    return appclient.client(token_for(AUTHOR_EMAIL))


def as_second_author() -> httpx.Client:
    return appclient.client(token_for(SECOND_AUTHOR_EMAIL))


def as_reader() -> httpx.Client:
    return appclient.client(token_for(READER_EMAIL))


def anonymous() -> httpx.Client:
    return appclient.client(None)


def register(display_name: str = "Probe Reader") -> tuple[str, str]:
    email = probe_email()
    response = httpx.post(
        f"{api_base()}/auth/sign-up",
        json={"email": email, "password": CORPUS_PASSWORD, "display_name": display_name},
        timeout=TIMEOUT,
    )
    assert response.status_code in (200, 201), (
        f"POST /api/auth/sign-up for {email} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    body = response.json()
    token = body.get("access_token")
    assert token, (
        f"POST /api/auth/sign-up for {email} returned no access_token: {response.text[:400]}"
    )
    return email, token


def draft_payload(kind: str = "doc", **overrides) -> dict:
    payload = {
        "kind": kind,
        "slug": probe_slug(kind),
        "title": f"Probe {kind} {unique_suffix()}",
        "summary": "A probe entry created by the grading run.",
        "body": "Probe body text for the grading run.",
        "category_label": "Product",
    }
    payload.update(overrides)
    return payload


def create_draft(client: httpx.Client, **overrides) -> dict:
    response = client.post("/entries", json=draft_payload(**overrides))
    assert response.status_code in (200, 201), (
        f"POST /api/entries returned {response.status_code} rather than creating a draft: "
        f"{response.text[:400]}"
    )
    entry = response.json()
    assert entry.get("state") == "draft", (
        f"POST /api/entries returned state {entry.get('state')!r} rather than 'draft': "
        f"{response.text[:400]}"
    )
    return entry


def publish(client: httpx.Client, entry_id) -> httpx.Response:
    return client.post(f"/entries/{entry_id}/publish")


def attach_image(client: httpx.Client, entry_id, payload: bytes = ONE_PIXEL_PNG,
                 alt_text: str = "A probe image") -> httpx.Response:
    return client.post(
        f"/entries/{entry_id}/assets",
        files={"file": (f"{unique_suffix()}.png", payload, "image/png")},
        data={"alt_text": alt_text},
    )


def await_instance_state(client: httpx.Client, instance_id, wanted: str) -> dict:
    """Bounded polling. A state machine that never arrives fails rather than hangs."""
    waited = 0.0
    seen = []
    while waited < SETTLE_LIMIT:
        response = client.get(f"/instances/{instance_id}")
        assert response.status_code == 200, (
            f"GET /api/instances/{instance_id} returned {response.status_code}: "
            f"{response.text[:300]}"
        )
        body = response.json()
        state = body.get("state")
        if not seen or seen[-1] != state:
            seen.append(state)
        if state == wanted:
            return {"body": body, "seen": seen}
        settle()
        waited += SETTLE_STEP
    raise AssertionError(
        f"instance {instance_id} never reached {wanted!r} within {SETTLE_LIMIT} seconds; "
        f"states observed: {seen}"
    )


@pytest.fixture(scope="session")
def store() -> capabilities.ObjectStore:
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend() -> capabilities.Backend:
    return capabilities.make_backend()


@pytest.fixture
def author_client():
    with as_author() as client:
        yield client


@pytest.fixture
def second_author_client():
    with as_second_author() as client:
        yield client


@pytest.fixture
def reader_client():
    with as_reader() as client:
        yield client


@pytest.fixture
def anonymous_client():
    with anonymous() as client:
        yield client


@pytest.fixture
def owned_draft(author_client):
    return create_draft(author_client)
