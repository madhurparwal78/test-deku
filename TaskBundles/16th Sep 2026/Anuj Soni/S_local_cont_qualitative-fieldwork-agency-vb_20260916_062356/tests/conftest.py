"""Fixtures, domain helpers and the pinned literals for Qualitative Fieldwork Agency.

No test_* function lives here (G10). Every value test_output.py asserts about the
SEEDED world is pinned in this file and appears verbatim in instruction.md (G6): a
grader that asserts a value the brief never pinned grades a working app as broken.
The per-run probe values are generated here and are only ever compared against
themselves, so they are deliberately not brief literals.

The shared grader (appclient, capabilities, _shapes) is supplied by the
deku-verifier-base image on PYTHONPATH=/tests. Nothing here re-implements it and
nothing here imports a provider SDK.
"""

from __future__ import annotations

import os
import time

import httpx
import pytest

import appclient
import capabilities

EDITOR_EMAIL = "editor@example.com"
EDITOR2_EMAIL = "editor2@example.com"
CLIENT_EMAIL = "client@example.com"
CLIENT2_EMAIL = "client2@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"

SITE_NAME = "Meridian Field"

ROLE_EDITOR = "editor"
ROLE_CLIENT = "client"

STATUS_DRAFT = "draft"
STATUS_IN_REVIEW = "in_review"
STATUS_PUBLISHED = "published"
STATUS_ARCHIVED = "archived"

SENSITIVITY_STANDARD = "standard"
SENSITIVITY_ELEVATED = "elevated"

STAGES = ("Brief", "Select", "Validate", "Confirm", "Execute", "Report")
STAGE_FIRST = "Brief"
STAGE_SECOND = "Select"
STAGE_THIRD = "Validate"

REASON_SECTOR_OWNER = "sector_owner"
REASON_NO_SECTOR_OWNER = "no_sector_owner"

REFERENCE_PREFIX = "MF-"
SEEDED_REFERENCE_ONE = "MF-2026-00001"
SEEDED_REFERENCE_TWO = "MF-2026-00002"

SECTOR_ELEVATED_OWNED = "pharmaceutical"
SECTOR_ELEVATED_SECOND = "beauty-cosmetics"
SECTOR_STANDARD_OWNED = "technology"
SECTOR_STANDARD_UNOWNED = "crypto"

METHOD_COUNT = 13
SECTOR_COUNT = 12
SERVICE_COUNT = 9
REGION_COUNT = 7
CATEGORY_COUNT = 5
COUNTRY_COUNT = 24
FEATURED_COUNTRY_COUNT = 22
PUBLISHED_ARTICLE_COUNT = 6

METHOD_SLUG = "focus-groups"
METHOD_TITLE = "Focus Groups"
METHOD_EXTRA_TITLE = "Co-Creation Workshops"
SERVICE_PRIMARY = "Qualitative Research"
SERVICE_SECOND_PRIMARY = "Behavioural Analysis"
SERVICE_SUPPORTING = "Translation and Transcripts"
KIND_PRIMARY = "primary"
KIND_SUPPORTING = "supporting"

CASE_STUDY_SLUG = "five-markets-one-brief"
CASE_STUDY_TITLE = "Five Markets, One Brief"
CASE_STUDY_APPROVAL = "CA-2026-014"
DRAFT_SLUG = "field-notes-from-lagos"
DRAFT_TITLE = "Field Notes From Lagos"
CATEGORY_CASE_STUDIES = "Case Studies"
CATEGORY_EDUCATIONAL = "Educational"
CATEGORY_METHODOLOGY = "Methodology"
REGION_WORLDWIDE = "Worldwide"
REGION_EUROPE = "Europe"
REGION_AFRICA = "Africa"
REGION_AMERICAS = "The Americas"

MARKET_ONE = "Germany"
MARKET_TWO = "Japan"
MARKET_THREE = "Nigeria"
DECOY_FIELD = "company_website"
ATTRIBUTION_OTHER = "Other"
CARD_LABEL_PREFIX = "Read more about"
COOKIE_CONTROL_LABEL = "Cookie Preferences"

OBJECT_KEY_PREFIX = "articles/"

TABLE_ACCOUNT = "account"
TABLE_METHOD = "method"
TABLE_SECTOR = "sector"
TABLE_SERVICE = "service"
TABLE_REGION = "region"
TABLE_COUNTRY = "country"
TABLE_CATEGORY = "category"
TABLE_ARTICLE = "article"
TABLE_BRIEF = "brief"
TABLE_OPPORTUNITY = "opportunity"
TABLE_NOTE = "opportunity_note"
TABLE_ASSET = "content_asset"
TABLE_SETTING = "site_setting"

PUBLIC_ROUTES = ("/", "/services", "/methodology", "/sectors", "/network",
                 "/about-us", "/articles", "/contact", "/privacy")
CONSOLE_ROUTES = ("/console", "/console/articles")
ABSENT_SURFACES = ("/search", "/checkout", "/comments", "/participants",
                   "/recordings", "/newsletter")

SETTLE_SECONDS = 0.25
POLL_TIMEOUT_SECONDS = 20.0
MIN_CHALLENGE_CHARS = 20
REPEAT_LIMIT = 3

CLIENT_ERROR = range(400, 500)
DENIED = (401, 403)
NOT_FOUND = (403, 404)
ACCEPTED = (200, 201, 202)
REFUSED = (400, 401, 403, 404, 409, 422, 429)


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
    return os.urandom(5).hex()


def probe_address(suffix: str) -> str:
    """A per-run address, only ever compared against itself."""
    return "probe-" + suffix + "@" + "example.com"


def probe_company(suffix: str) -> str:
    return "Probe Partners " + suffix


def probe_slug(suffix: str) -> str:
    return "probe-article-" + suffix


def probe_challenge(suffix: str) -> str:
    return ("We need to understand why our service is not landing in two markets "
            "and what to change, reference " + suffix)


def describe(response: httpx.Response, what: str) -> str:
    """The failure-message shape reference/J requires: anchor, request, status, body."""
    return (f"{what}: {response.request.method} {response.request.url} returned "
            f"{response.status_code}: {response.text[:400]}")


def backend() -> capabilities.Backend:
    """The persisted-state view the brief's own table names address."""
    return capabilities.make_backend()


def object_store() -> capabilities.ObjectStore:
    """The object store the brief names, reached with the shared credentials."""
    return capabilities.make_store()


def fetch_document(path: str) -> httpx.Response:
    """Fetch a rendered document from the app origin rather than from the API base."""
    return httpx.get(appclient.app_url() + path, timeout=appclient.TIMEOUT,
                     follow_redirects=True)


def head_of(markup: str) -> str:
    lower = markup.lower()
    end = lower.find("</head>")
    return markup[:end] if end > 0 else markup


def document_title(markup: str) -> str:
    lower = markup.lower()
    start = lower.find("<title")
    if start < 0:
        return ""
    open_end = lower.find(">", start)
    close = lower.find("</title>", open_end)
    if open_end < 0 or close < 0:
        return ""
    return markup[open_end + 1:close].strip()


def meta_description(markup: str) -> str:
    head = head_of(markup)
    lower = head.lower()
    cursor = 0
    while True:
        start = lower.find("<meta", cursor)
        if start < 0:
            return ""
        end = lower.find(">", start)
        if end < 0:
            return ""
        tag = head[start:end]
        if "description" in tag.lower():
            for quote in ('content="', "content='"):
                at = tag.find(quote)
                if at >= 0:
                    rest = tag[at + len(quote):]
                    stop = rest.find(quote[-1])
                    return rest[:stop].strip() if stop >= 0 else rest.strip()
        cursor = end + 1


def internal_links(markup: str) -> list[str]:
    """Every same-origin href in a rendered document, as a path."""
    found = []
    lower = markup.lower()
    cursor = 0
    while True:
        at = lower.find('href="', cursor)
        if at < 0:
            return found
        rest = markup[at + 6:]
        stop = rest.find('"')
        if stop < 0:
            return found
        href = rest[:stop].strip()
        cursor = at + 6 + stop
        if href.startswith("/") and not href.startswith("//"):
            found.append(href.split("#")[0].split("?")[0])


def external_origins(markup: str) -> list[str]:
    """Absolute origins a rendered document reaches for, excluding the app's own."""
    own = appclient.app_url()
    found = []
    for marker in ('src="', 'href="'):
        lower = markup.lower()
        cursor = 0
        while True:
            at = lower.find(marker, cursor)
            if at < 0:
                break
            rest = markup[at + len(marker):]
            stop = rest.find('"')
            cursor = at + len(marker) + (stop if stop > 0 else 1)
            if stop < 0:
                break
            value = rest[:stop].strip()
            if value.startswith("http") and not value.startswith(own):
                found.append(value)
    return found


def brief_body(suffix: str, **overrides) -> dict:
    """A brief the server must accept, with any field overridden for a refusal check."""
    body = {
        "full_name": "Probe Buyer " + suffix,
        "work_email": probe_address(suffix),
        "company": probe_company(suffix),
        "sector_slug": SECTOR_STANDARD_OWNED,
        "markets": [MARKET_ONE, MARKET_TWO],
        "methods": [METHOD_TITLE],
        "services": [SERVICE_PRIMARY],
        "sample_size": 12,
        "budget_band": "50k-100k",
        "challenge": probe_challenge(suffix),
        "attribution_key": "google_search",
        "attribution_detail": "",
        DECOY_FIELD: "",
    }
    body.update(overrides)
    return body


def submit_brief(body: dict, token: str | None = None) -> httpx.Response:
    with appclient.client(token) as client:
        return client.post("/briefs", json=body)


def accepted_brief(suffix: str, **overrides) -> tuple[str, dict]:
    """Submit a brief that must be accepted; return its reference and the body sent."""
    body = brief_body(suffix, **overrides)
    response = submit_brief(body)
    assert response.status_code in ACCEPTED, describe(
        response, "a complete brief must be accepted")
    payload = response.json()
    reference = payload.get("reference") if isinstance(payload, dict) else None
    assert reference, describe(response, "an accepted brief must carry a reference")
    return str(reference), body


def opportunity_row(reference: str) -> dict:
    """The stored opportunity for a reference, polled until the write has landed."""
    store = backend()
    row = poll_until(lambda: store.one(TABLE_OPPORTUNITY, reference=reference))
    assert row, f"no {TABLE_OPPORTUNITY} row carries the reference {reference}"
    return row


def brief_row(reference: str) -> dict:
    store = backend()
    row = poll_until(lambda: store.one(TABLE_BRIEF, reference=reference))
    assert row, f"no {TABLE_BRIEF} row carries the reference {reference}"
    return row


def article_body(suffix: str, **overrides) -> dict:
    body = {
        "title": "Probe Field Note " + suffix,
        "slug": probe_slug(suffix),
        "summary": "A probe record written by a check, " + suffix,
        "body": "A probe body long enough to publish, written for " + suffix + ".",
        "region": REGION_AFRICA,
        "categories": [CATEGORY_EDUCATIONAL],
        "seo_description": ("A probe article used to confirm the publishing rules "
                            "hold end to end for " + suffix),
        "client_approval_reference": "",
    }
    body.update(overrides)
    return body


def create_article(token: str, suffix: str, **overrides) -> dict:
    with appclient.client(token) as client:
        response = client.post("/articles", json=article_body(suffix, **overrides))
    assert response.status_code in ACCEPTED, describe(
        response, "an editor must be able to create a draft article")
    return response.json()


def publish_article(token: str, slug: str) -> httpx.Response:
    with appclient.client(token) as client:
        return client.post(f"/articles/{slug}/publish")


def upload_cover(token: str, slug: str, payload: bytes, alt_text: str = "A probe cover",
                 filename: str = "cover.png") -> httpx.Response:
    files = {"file": (filename, payload, "image/png")}
    data = {"alt_text": alt_text}
    with appclient.client(token) as client:
        return client.post(f"/articles/{slug}/cover", files=files, data=data)


def probe_png(suffix: str) -> bytes:
    """Deterministic bytes per run: a tiny PNG header plus a per-run tail."""
    return b"\x89PNG\r\n\x1a\n" + suffix.encode("ascii")


def stored_keys(prefix: str = OBJECT_KEY_PREFIX) -> list[str]:
    return object_store().list(prefix)


@pytest.fixture()
def editor() -> str:
    return appclient.login(EDITOR_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def editor_two() -> str:
    return appclient.login(EDITOR2_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def buyer() -> str:
    return appclient.login(CLIENT_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def second_buyer() -> str:
    return appclient.login(CLIENT2_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def suffix() -> str:
    return unique_suffix()
