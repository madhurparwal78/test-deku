"""Fixtures, domain stores and the pinned literals for Veloce.

No test_* function lives here. Every value test_output.py asserts about the SEEDED
world is pinned in this file and appears verbatim in instruction.md: a grader that
asserts a value the brief never pinned grades a working app as broken. The
self-seeding probe values carry no brief literal of their own: slugs, titles,
bodies, emails and cover bytes are generated per run from unique_suffix() and are
only ever compared against themselves.

The browser pass runs before this module and writes only through the cookie choice
and through articles it creates and removes for itself, so the five seeded articles
and the three seeded accounts are untouched on both sides and the pinned counts
survive two consecutive runs. Every mutation here acts on a probe article or a
probe reader this module creates, and removes what it created before the check
ends.

The shared grader (appclient, capabilities) is supplied by the deku-verifier-base
image on PYTHONPATH=/tests. Nothing here re-implements it and nothing here imports
a provider SDK.
"""

from __future__ import annotations

import hashlib
import os
import time

import httpx
import pytest

import appclient
import capabilities

AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"

AUTHOR_NAME = "Marisol Quint"
AUTHOR2_NAME = "Teodor Vance"
READER_NAME = "Ingrid Salas"

TOKEN_FIELD = "access_token"

ROLE_AUTHOR = "author"
ROLE_READER = "reader"

VISIBILITY_DRAFT = "draft"
VISIBILITY_OPEN = "open"
VISIBILITY_MEMBERS = "members"
VISIBILITIES = (VISIBILITY_DRAFT, VISIBILITY_OPEN, VISIBILITY_MEMBERS)

REFUSED_MAILBOXES = ("gmail.com", "outlook.com", "yahoo.com", "hotmail.com",
                     "icloud.com")

SLUG_MODERN_CDN = "modern-cdn-explained"
SLUG_FEWER_LOCATIONS = "fewer-stronger-locations"
SLUG_SECURITY_REPORT = "edge-security-report-2026"
SLUG_PURGE_PATH = "rewriting-the-purge-path"
SLUG_STREAMING_DIARY = "streaming-migration-diary"

TITLE_MODERN_CDN = "What is a modern CDN and why is it important?"
TITLE_FEWER_LOCATIONS = "Fewer locations, more power"
TITLE_SECURITY_REPORT = "The 2026 edge security report"
TITLE_PURGE_PATH = "Rewriting the purge path"
TITLE_STREAMING_DIARY = "Streaming at the edge, a migration diary"

SEEDED_ARTICLES = {
    SLUG_MODERN_CDN: (TITLE_MODERN_CDN, VISIBILITY_OPEN, AUTHOR_EMAIL),
    SLUG_FEWER_LOCATIONS: (TITLE_FEWER_LOCATIONS, VISIBILITY_OPEN, AUTHOR2_EMAIL),
    SLUG_SECURITY_REPORT: (TITLE_SECURITY_REPORT, VISIBILITY_MEMBERS, AUTHOR_EMAIL),
    SLUG_PURGE_PATH: (TITLE_PURGE_PATH, VISIBILITY_DRAFT, AUTHOR_EMAIL),
    SLUG_STREAMING_DIARY: (TITLE_STREAMING_DIARY, VISIBILITY_DRAFT, AUTHOR2_EMAIL),
}
PUBLISHED_SLUGS = (SLUG_MODERN_CDN, SLUG_FEWER_LOCATIONS, SLUG_SECURITY_REPORT)
DRAFT_SLUGS = (SLUG_PURGE_PATH, SLUG_STREAMING_DIARY)

STATISTICS = (
    ("On average", "<150 ms",
     "regional mean purge time to clear cached content globally",
     "as of December 31, 2025"),
    ("More than", "5 trillion", "Daily requests served", "as of March 31, 2026"),
    ("Almost", "90%", "Of customers run the next-gen firewall in blocking mode",
     "as of March 2023"),
    ("Global", "622 Tbps", "Edge network capacity", "as of June 30, 2026"),
    ("Up to", "32%", "faster time to first byte than other networks",
     "as of June 30, 2026"),
)

CAPABILITY_RESULT_LINES = (
    "Congested region avoided. Every request took the fastest open path.",
    "0 nodes left on the old copy.",
    "0 attack requests reached the origin.",
    "0 requests dropped.",
    "Answered at the edge, not at the origin.",
    "Blocking mode on. Every threat deflected at the perimeter.",
    "Live. The newest value arrives at the right edge.",
    "Encrypted by default. Certificates managed for you.",
)

FAMILY_NETWORK = "Network Services"
FAMILY_SECURITY = "Security"
FAMILY_COMPUTE = "Compute"
FAMILY_OBSERVABILITY = "Observability"
FAMILY_COUNTS = {
    FAMILY_NETWORK: 13,
    FAMILY_SECURITY: 6,
    FAMILY_COMPUTE: 7,
    FAMILY_OBSERVABILITY: 6,
}
SERVICE_TOTAL = 32
SAMPLED_SERVICES = {
    "Content Delivery (CDN)": "Deliver fast, personalized experiences globally",
    "Load Balancer": "Granular control over routing decisions",
    "Object Storage": "Direct access to large files at the edge with zero egress fees",
    "API Security": "Secure your API endpoints",
    "Client-Side Protection": "Defend against client-side attacks",
    "AI Bot Management": "Stop AI bots from scraping website content",
    "Programmable Cache": "Full programmatic access to the same caching that powers our CDN",
    "Alerts": "Create notifications for service-related metrics",
}

PARTNER_TIERS = ("Registered", "Select", "Premier")

FIELD_ID = "id"
FIELD_EMAIL = "email"
FIELD_PASSWORD = "password"
FIELD_DISPLAY_NAME = "display_name"
FIELD_ROLE = "role"
FIELD_PASSWORD_HASH = "password_hash"
FIELD_SLUG = "slug"
FIELD_TITLE = "title"
FIELD_EXCERPT = "excerpt"
FIELD_BODY = "body"
FIELD_CATEGORY = "category"
FIELD_VISIBILITY = "visibility"
FIELD_AUTHOR_ID = "author_id"
FIELD_AUTHOR_NAME = "author_name"
FIELD_COVER_KEY = "cover_key"
FIELD_COVER_URL = "cover_url"
FIELD_PUBLISHED_AT = "published_at"
FIELD_POSITION = "position"
FIELD_QUALIFIER = "qualifier"
FIELD_VALUE = "value"
FIELD_CAPTION = "caption"
FIELD_MEASURED_ON = "measured_on"
FIELD_CLAIM = "claim"
FIELD_RESULT_LINE = "result_line"
FIELD_FAMILY = "family"
FIELD_NAME = "name"
FIELD_BLURB = "blurb"
FIELD_HEADLINE = "headline"
FIELD_DATED_ON = "dated_on"
FIELD_SUMMARY = "summary"
FIELD_STARTS_ON = "starts_on"
FIELD_PLACE = "place"
FIELD_REGISTRATION_NOTE = "registration_note"
FIELD_VISITOR_KEY = "visitor_key"
FIELD_ACCEPTED = "accepted"
FIELD_DECIDED_AT = "decided_at"
FIELD_PATH = "path"
FIELD_ACCOUNT = "account"

PARAM_FAMILY = "family"
PARAM_QUERY = "q"

TABLE_ACCOUNT = "account"
TABLE_ARTICLE = "article"
TABLE_STATISTIC = "statistic"
TABLE_CAPABILITY = "capability"
TABLE_SERVICE = "service"
TABLE_PRESS = "press_release"
TABLE_EVENT = "event"
TABLE_PARTNER = "partner_tier"
TABLE_COOKIE = "cookie_choice"

APP_ROOT = "/app"
CREDENTIALS_FILE = "/app/USER_README.md"

HEALTH_PATH = "/health"
SIGNUP_PATH = "/auth/signup"
LOGIN_PATH = "/auth/login"
ME_PATH = "/me"
STATISTICS_PATH = "/statistics"
CAPABILITIES_PATH = "/capabilities"
SERVICES_PATH = "/services"
ARTICLES_PATH = "/articles"
DESK_ARTICLES_PATH = "/desk/articles"
PRESS_PATH = "/press"
EVENTS_PATH = "/events"
PARTNER_TIERS_PATH = "/partner-tiers"
SEARCH_PATH = "/search"
COOKIE_PATH = "/cookie-choice"

COVER_KEY_PREFIX = "covers"

SETTLE_SECONDS = 0.25
POLL_TIMEOUT_SECONDS = 20.0

CLIENT_ERROR = range(400, 500)
DENIED = (401, 403, 404)


def settle() -> None:
    """Yield briefly so an asynchronous side effect can land."""
    time.sleep(SETTLE_SECONDS)


def poll_until(predicate, timeout: float = POLL_TIMEOUT_SECONDS):
    """Bounded poll on a monotonic clock. Returns the last value the predicate saw."""
    deadline = time.monotonic() + timeout
    value = None
    while time.monotonic() < deadline:
        value = predicate()
        if value:
            return value
        settle()
    return value


def unique_suffix() -> str:
    """A per-run identifier so a self-seeding check never collides with itself."""
    return os.urandom(3).hex()


def probe_slug(suffix: str) -> str:
    return f"probe-article-{suffix}"


def probe_title(suffix: str) -> str:
    return f"Probe Article {suffix[:4]}"


def probe_excerpt(suffix: str) -> str:
    return f"A probe opening written by the grading pass under the mark {suffix}."


def probe_body(suffix: str) -> str:
    return (f"A probe article written by the grading pass under the mark {suffix}, "
            f"long enough to clear the shortest body the desk accepts.")


def probe_category(suffix: str) -> str:
    return f"Probe {suffix[:2].upper()}"


def probe_email(suffix: str) -> str:
    return f"probe-{suffix}@example.com"


def probe_display_name(suffix: str) -> str:
    return f"Probe Reader {suffix[:4]}"


def probe_cover_bytes(suffix: str) -> bytes:
    """Deterministic per-run cover bytes, distinct between runs."""
    return b"veloce-probe-cover-" + suffix.encode("ascii") + b"-" + b"\x89PNG" * 8


def digest_of(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def cover_prefix(article_id) -> str:
    return f"{COVER_KEY_PREFIX}/{article_id}/"


def expected_cover_key(article_id, payload: bytes, ext: str = "png") -> str:
    return f"{cover_prefix(article_id)}{digest_of(payload)}.{ext}"


def describe(response: httpx.Response, what: str) -> str:
    """The failure-message shape reference/J requires: anchor, request, status, body."""
    return (f"{what}: {response.request.method} {response.request.url} returned "
            f"{response.status_code}: {response.text[:400]}")


def is_client_error(response: httpx.Response) -> bool:
    return response.status_code in CLIENT_ERROR


def is_denied(response: httpx.Response) -> bool:
    return response.status_code in DENIED


def article_path(slug: str) -> str:
    return f"{ARTICLES_PATH}/{slug}"


def article_id_path(article_id) -> str:
    return f"{ARTICLES_PATH}/{article_id}"


def cover_path(article_id) -> str:
    return f"{ARTICLES_PATH}/{article_id}/cover"


def article_payload(suffix: str, **overrides) -> dict:
    body = {
        FIELD_SLUG: probe_slug(suffix),
        FIELD_TITLE: probe_title(suffix),
        FIELD_EXCERPT: probe_excerpt(suffix),
        FIELD_BODY: probe_body(suffix),
        FIELD_CATEGORY: probe_category(suffix),
        FIELD_VISIBILITY: VISIBILITY_DRAFT,
    }
    body.update(overrides)
    return body


def create_article(client: httpx.Client, suffix: str, **overrides) -> dict:
    """Store one probe article at visibility draft and hand back the stored record."""
    response = client.post(ARTICLES_PATH, json=article_payload(suffix, **overrides))
    assert response.status_code in (200, 201), describe(
        response, "an author must be able to store a probe article")
    body = response.json()
    assert body.get(FIELD_ID) is not None, describe(
        response, "a stored article must carry an id")
    return body


def upload_cover(client: httpx.Client, article_id, payload: bytes, suffix: str):
    return client.post(
        cover_path(article_id),
        files={"file": (f"probe-{suffix}.png", payload, "image/png")},
    )


def set_visibility(client: httpx.Client, article_id, visibility: str):
    return client.patch(article_id_path(article_id),
                        json={FIELD_VISIBILITY: visibility})


def remove_article(client: httpx.Client, article_id) -> None:
    client.delete(article_id_path(article_id))


def read_index(client: httpx.Client, **params) -> list:
    response = client.get(ARTICLES_PATH, params=params or None)
    assert response.status_code == 200, describe(
        response, "the published article index must be readable")
    payload = response.json()
    assert isinstance(payload, list), describe(
        response, "the article index must return a top-level JSON array")
    return payload


def index_slugs(payload: list) -> list:
    return [row.get(FIELD_SLUG) for row in payload]


def read_article(client: httpx.Client, slug: str) -> dict:
    response = client.get(article_path(slug))
    assert response.status_code == 200, describe(
        response, f"the published article {slug} must be readable")
    return response.json()


def read_list(client: httpx.Client, path: str) -> list:
    response = client.get(path)
    assert response.status_code == 200, describe(
        response, f"the read at {path} must answer with its seeded rows")
    payload = response.json()
    assert isinstance(payload, list), describe(
        response, f"the read at {path} must return a top-level JSON array")
    return payload


def sign_up_probe_reader(suffix: str) -> str:
    """Open signup mints a reader whose account is the probe's own."""
    with appclient.client(None) as anonymous:
        response = anonymous.post(SIGNUP_PATH, json={
            FIELD_EMAIL: probe_email(suffix),
            FIELD_PASSWORD: SEEDED_PASSWORD,
        })
    assert response.status_code in (200, 201), describe(
        response, "signup must be open to a new reader")
    token = response.json().get(TOKEN_FIELD)
    assert token, describe(response, "signup must return access_token")
    return token


@pytest.fixture(scope="session")
def app_base() -> str:
    return appclient.app_url()


@pytest.fixture()
def author_token() -> str:
    """A fresh token per check: one login held for a whole run goes stale."""
    return appclient.login(AUTHOR_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def author2_token() -> str:
    return appclient.login(AUTHOR2_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def reader_token() -> str:
    return appclient.login(READER_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def author(author_token: str):
    with appclient.client(author_token) as client:
        yield client


@pytest.fixture()
def author2(author2_token: str):
    with appclient.client(author2_token) as client:
        yield client


@pytest.fixture()
def reader(reader_token: str):
    with appclient.client(reader_token) as client:
        yield client


@pytest.fixture()
def anonymous():
    with appclient.client(None) as client:
        yield client


@pytest.fixture()
def suffix() -> str:
    return unique_suffix()


@pytest.fixture()
def probe_reader(suffix: str):
    """A freshly signed-up reader holding an account of their own."""
    with appclient.client(sign_up_probe_reader(suffix)) as client:
        yield client


@pytest.fixture(scope="session")
def backend():
    """Persisted-state reader over the declared backend slot."""
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    """Object-store reader over the declared storage slot."""
    return capabilities.make_store()


def account_row(backend, email: str):
    return backend.one(TABLE_ACCOUNT, email=email)


def account_rows(backend, **where) -> list:
    return backend.rows(TABLE_ACCOUNT, **where)


def article_rows(backend, **where) -> list:
    return backend.rows(TABLE_ARTICLE, **where)


def article_row_by_slug(backend, slug: str):
    return backend.one(TABLE_ARTICLE, slug=slug)


def statistic_rows(backend, **where) -> list:
    return backend.rows(TABLE_STATISTIC, **where)


def capability_rows(backend, **where) -> list:
    return backend.rows(TABLE_CAPABILITY, **where)


def service_rows(backend, **where) -> list:
    return backend.rows(TABLE_SERVICE, **where)


def cookie_rows(backend, **where) -> list:
    return backend.rows(TABLE_COOKIE, **where)
