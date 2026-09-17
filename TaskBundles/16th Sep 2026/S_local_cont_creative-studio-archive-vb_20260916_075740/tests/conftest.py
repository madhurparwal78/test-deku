"""Fixtures, domain helpers and the pinned literals for Creative Studio Archive.

No test_* function lives here (G10). Every value the one pytest module asserts about
the SEEDED world is pinned here and appears verbatim in instruction.md (G6): a grader
that asserts a value the brief never pinned grades a working app as broken. Per-run
probe values are generated here and are only ever compared against themselves, so they
are deliberately not brief literals.

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

LEAD_EMAIL = "lead@example.com"
LEAD2_EMAIL = "lead2@example.com"
WRITER_EMAIL = "writer@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"

STUDIO_NAME = "Halftone"
STUDIO_ADDRESS = "hey@halftone.studio"

ROLE_WRITER = "writer"
ROLE_LEAD = "lead"

STATE_DRAFT = "draft"
STATE_IN_REVIEW = "in_review"
STATE_APPROVED = "approved"
STATE_PUBLISHED = "published"
STATE_UNPUBLISHED = "unpublished"
STATE_ARCHIVED = "archived"
CASE_STATES = (STATE_DRAFT, STATE_IN_REVIEW, STATE_APPROVED, STATE_PUBLISHED,
               STATE_UNPUBLISHED, STATE_ARCHIVED)

INQUIRY_NEW = "new"
INQUIRY_ASSIGNED = "assigned"
INQUIRY_REPLIED = "replied"
INQUIRY_SPAM = "spam"
INQUIRY_STATES = (INQUIRY_NEW, INQUIRY_ASSIGNED, INQUIRY_REPLIED, "won", "lost",
                  INQUIRY_SPAM)

BLOCK_KINDS = ("text", "image_full", "image_pair", "video", "quote", "stat", "gallery")
SEQUENCE_BLOCKS = ("hero", "seal", "services", "cases-heading", "case-stack",
                   "awards", "contact", "footer")
MENU_VALUES = ("about", "work", "recognition", "contact", "archive")
MODE_SEQUENCE = "sequence"
MODE_ARCHIVE = "archive"

BUDGET_TOP = "over-200k"
BUDGET_MID = "75k-200k"
BUDGET_BANDS = ("under-25k", "25k-75k", "75k-200k", "over-200k", "not-sure")
TIMELINES = ("now", "this-quarter", "this-year", "exploring")

PUBLISHED_CASE_COUNT = 12
PUBLISHED_SLUGS = ("northline-ventures", "isla-sereno", "halcyon-frozen",
                   "hero-assembly", "playful-works", "marlow-field", "verrine",
                   "essence-atelier", "kasper-wend", "aurelio-sant", "cure-studio",
                   "wildberry-care")
FIRST_SLUG = "northline-ventures"
LINKED_SLUG = "isla-sereno"
REVIEW_SLUG = "harbourline-freight"
DRAFT_SLUG = "quiet-hours"

FIRST_VEIL = "0.9625"
SECOND_VEIL = "0.9250"
LAST_VEIL = "0.5500"
THIRTEENTH_FIRST_VEIL = "0.9654"

ARCHIVE_SEED = "halftone-wall-2026"
ARCHIVE_ITEM_COUNT = 240

DISCIPLINE_SLUGS = ("art-direction", "branding", "web-design", "mobile-design",
                    "content-production", "motion-design", "front-end-development",
                    "back-end")
DISCIPLINE_COUNT = 8
LEAD_DISCIPLINE = "art-direction"
LEAD2_DISCIPLINE = "web-design"

AWARD_BODY_PRIMARY = "Prixel"
AWARD_BODY_SECOND = "Flux"
AWARD_BODY_THIRD = "Portfolia"
AWARD_TYPE_COUNTED = "Site of the Day"
AWARD_TYPE_COUNTED_TOTAL = 24
AWARD_TYPE_EMPTY = "Gallery, Illustration"

ERASURE_MARKER = "[erased]"
DECOY_FIELD = "company_website"
FORM_OPENED_AT = "2026-01-01T09:00:00Z"
FILL_TIME_FLOOR_SECONDS = 3
COVER_KEY_PREFIX = "cases/"
ARCHIVE_KEY_PREFIX = "archive/"

MESSAGE_FLOOR = 20
MESSAGE_CEILING = 5000
NAME_FLOOR = 2
RATE_CEILING_PER_ADDRESS = 5

TABLE_MEMBER = "members"
TABLE_CASE = "cases"
TABLE_REVISION = "case_revisions"
TABLE_BLOCK = "case_blocks"
TABLE_ARCHIVE_ITEM = "archive_items"
TABLE_ARCHIVE_LAYOUT = "archive_layout"
TABLE_AWARD_BODY = "award_bodies"
TABLE_AWARD_TYPE = "award_types"
TABLE_AWARD = "awards"
TABLE_INQUIRY = "inquiries"
TABLE_INQUIRY_EVENT = "inquiry_events"
TABLE_REVIEW_TOKEN = "review_tokens"
TABLE_REVIEW_COMMENT = "review_comments"
TABLE_AUDIT = "audit_events"
TABLE_MEDIA = "media_assets"
TABLE_PAGE_BLOCK = "page_blocks"
TABLE_COUNT = 16

PUBLIC_ROUTES = ("/", "/showreel", "/legal/privacy")
CONSOLE_ROUTES = ("/console/cases", "/console/archive", "/console/awards",
                  "/console/media")
LEAD_ONLY_ROUTES = ("/console/inquiries", "/console/audit")

APP_ROOT = "/app"
CREDENTIALS_FILE = "/app/USER_README.md"
SCREENSHOT_DIR = "/app/.browser_screenshots"
DOWNLOAD_DIR = "/app/.downloads"

SETTLE_SECONDS = 0.25
POLL_TIMEOUT_SECONDS = 20.0

ACCEPTED = (200, 201, 202)
DENIED = (401, 403)
NOT_FOUND = (403, 404)
REFUSED = (400, 401, 403, 404, 409, 410, 422, 429)
CLIENT_ERROR = range(400, 500)


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
    return "probe-" + suffix + "@" + "example.com"


def probe_slug(suffix: str) -> str:
    return "probe-case-" + suffix


def probe_message(suffix: str) -> str:
    return ("We are planning a brand refresh with a new site to follow it, "
            "reference " + suffix)


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


def fetch_document_no_redirect(path: str) -> httpx.Response:
    return httpx.get(appclient.app_url() + path, timeout=appclient.TIMEOUT,
                     follow_redirects=False)


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


def attribute_values(markup: str, name: str) -> list[str]:
    """Every value a named attribute takes in a rendered document, in order."""
    found = []
    marker = name + '="'
    lower = markup.lower()
    cursor = 0
    while True:
        at = lower.find(marker, cursor)
        if at < 0:
            return found
        rest = markup[at + len(marker):]
        stop = rest.find('"')
        cursor = at + len(marker) + (stop if stop > 0 else 1)
        if stop < 0:
            return found
        found.append(rest[:stop].strip())


def external_origins(markup: str) -> list[str]:
    """Absolute addresses a rendered document reaches for, excluding the app's own."""
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


def rectangles_overlap(a: dict, b: dict) -> bool:
    """True when two placed archive rectangles share any area on the plane."""
    ax, ay, aw, ah = float(a["x"]), float(a["y"]), float(a["w"]), float(a["h"])
    bx, by, bw, bh = float(b["x"]), float(b["y"]), float(b["w"]), float(b["h"])
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def inquiry_body(suffix: str, **overrides) -> dict:
    """A work inquiry the server must accept, with any field overridden."""
    body = {
        "name": "Probe Client " + suffix,
        "email": probe_address(suffix),
        "company": "Probe Works " + suffix,
        "budget_band": BUDGET_MID,
        "timeline": "this-quarter",
        "disciplines": [LEAD_DISCIPLINE],
        "message": probe_message(suffix),
        "consent": True,
        "source_block": "contact",
        "submission_key": "probe-key-" + suffix,
        "form_opened_at": FORM_OPENED_AT,
        DECOY_FIELD: "",
    }
    body.update(overrides)
    return body


def submit_inquiry(body: dict) -> httpx.Response:
    with appclient.client(None) as api:
        return api.post("/inquiries", json=body)


def accepted_inquiry(suffix: str, **overrides) -> tuple[dict, dict]:
    """Submit an inquiry that must be accepted; return the payload plus the body."""
    body = inquiry_body(suffix, **overrides)
    response = submit_inquiry(body)
    assert response.status_code in ACCEPTED, describe(
        response, "a complete work inquiry must be accepted")
    payload = response.json()
    assert isinstance(payload, dict), describe(
        response, "an accepted inquiry must return an object carrying its id")
    return payload, body


def inquiry_row(key: str) -> dict:
    store = backend()
    row = poll_until(lambda: store.one(TABLE_INQUIRY, submission_key=key))
    assert row, f"no {TABLE_INQUIRY} row carries the submission_key {key}"
    return row


def case_body(suffix: str, **overrides) -> dict:
    body = {
        "slug": probe_slug(suffix),
        "client": "Probe Client " + suffix,
        "title": "Probe Case " + suffix,
        "summary": ("A probe case written by a check so the publishing rules can be "
                    "walked end to end without touching a seeded record, " + suffix),
        "description": ("A PROBE CASE WRITTEN BY A CHECK SO THE PUBLISHING RULES CAN "
                        "BE WALKED WITHOUT A SEEDED RECORD " + suffix.upper()),
        "year": 2026,
        "disciplines": [LEAD_DISCIPLINE],
    }
    body.update(overrides)
    return body


def create_case(token: str, suffix: str, **overrides) -> dict:
    with appclient.client(token) as api:
        response = api.post("/console/cases", json=case_body(suffix, **overrides))
    assert response.status_code in ACCEPTED, describe(
        response, "a member must be able to create a draft case")
    return response.json()


def publish_case(token: str, slug: str) -> httpx.Response:
    with appclient.client(token) as api:
        return api.post(f"/console/cases/{slug}/publish")


def probe_png(suffix: str) -> bytes:
    """Deterministic bytes per run: a tiny PNG header plus a per-run tail."""
    return b"\x89PNG\r\n\x1a\n" + suffix.encode("ascii")


def upload_cover(token: str, slug: str, payload: bytes, alt_text: str = "A probe cover",
                 filename: str = "cover.png",
                 content_type: str = "image/png") -> httpx.Response:
    files = {"file": (filename, payload, content_type)}
    data = {"alt_text": alt_text}
    with appclient.client(token) as api:
        return api.post(f"/console/cases/{slug}/cover", files=files, data=data)


def stored_keys(prefix: str = COVER_KEY_PREFIX) -> list[str]:
    return object_store().list(prefix)


@pytest.fixture()
def lead() -> str:
    return appclient.login(LEAD_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def lead_two() -> str:
    return appclient.login(LEAD2_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def writer() -> str:
    return appclient.login(WRITER_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def suffix() -> str:
    return unique_suffix()
