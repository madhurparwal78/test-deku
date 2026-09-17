"""Fixtures, domain helpers and the pinned literals for Verdigris Studio.

No test_* function lives here (G10). Every value the one pytest module asserts about
the SEEDED world is pinned in this file and appears verbatim in instruction.md (G6): a
grader that asserts a value the brief never pinned grades a working app as broken.
The per-run probe values are generated here and are only ever compared against
themselves, so they are deliberately not brief literals.

The shared grader (appclient, capabilities, _shapes) is supplied by the
deku-verifier-base image on PYTHONPATH=/tests. Nothing here re-implements it and
nothing here imports a provider SDK.
"""

from __future__ import annotations

import os
import re
import time
from datetime import datetime, timedelta, timezone

import httpx
import pytest

import appclient
import capabilities

STUDIO_EMAIL = "studio@example.com"
CLIENT_EMAIL = "client@example.com"
CLIENT2_EMAIL = "client2@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"

SITE_NAME = "Verdigris Studio"
METHOD_NAME = "Throughline(TM)"

ROLE_STUDIO = "studio"
ROLE_CLIENT = "client"

STATE_HELD = "held"
STATE_CONFIRMED = "confirmed"
STATE_CANCELLED = "cancelled"
STATE_EXPIRED = "expired"
BOOKING_STATES = (STATE_HELD, STATE_CONFIRMED, STATE_CANCELLED, STATE_EXPIRED)

SLOT_OPEN = "open"
SLOT_CLOSED = "closed"

GROUND_LIGHT = "light"
GROUND_DARK = "dark"

LAYOUT_FULL = "full"
LAYOUT_HALF = "half"

FIT_POSITIVE = "positive"
FIT_NEGATIVE = "negative"

SECTORS = ("beauty", "wellness", "food", "lifestyle")
PROJECT_TYPES = ("Launch", "Redesign")
BUDGET_BANDS = ("Under $5,000", "$5,000 to $10,000", "Over $10,000", "Not sure yet")

SERVICE_FIRST = "Experience design"
SERVICE_VISUAL_IDENTITY = "Visual identity"
SERVICE_DIGITAL = "Digital communication"
SERVICE_COUNT = 8

PACKAGE_ENTRY = "Opening Note"
PACKAGE_MIDDLE = "Full Measure"
PACKAGE_COMMERCE = "Open Shelf"
FLOOR_ENTRY = 350000
FLOOR_MIDDLE = 750000
FLOOR_COMMERCE = 1200000
CURRENCY = "usd"
PRICE_RENDERED = "From $3,500 plus tax"
BADGE_RECOMMENDED = "Recommended"
PANEL_LABELS = ("Who the package suits", "What the package contains",
                "What the studio delivers", "What can be added")

METHOD_STEPS = ("Diagnostic", "Art direction", "Digital experience", "Brand alignment")

AWARD_ROWS = ((2023, "Vare Studio", "Honourable Mention"),
              (2024, "Verdigris Studio", "Nominee"),
              (2025, "Verdigris Studio", "Nominee"))
DELIVERED_COUNT = 148
DIRECTORY_SCORE = "4.3"
DIRECTORY_SCALE = 5
DIRECTORY_VERDICT = "Very good"
DIRECTORY_SOURCE = "Studio Index"
DIRECTORY_REVIEWS = 4

PROJECT_COUNT = 12
FEATURED_COUNT = 6
PROJECT_FIRST = "Aster & Bloom"
PROJECT_FOOD = "Saltbox Kitchen"
PROJECT_LAST = "Slow Sunday"
PROJECT_BREAD = "Bread & Bone"

FILTER_ALL = "All"
PROMISE_LINE = "reply within 24 hours"
PROMISE_HOURS = 24
CONFIRMATION_SUBJECT_PREFIX = "Call confirmed:"
BOOKING_REFERENCE_SAMPLE = "vs-7f3a9c1d4e20"
ENQUIRY_REFERENCE_SAMPLE = "vq-4c81be09fa37"

SLOT_MINUTES = 30
HOLD_MINUTES = 8
SEEDED_SLOT_COUNT = 6
SEEDED_SLOTS_NEXT_DAY = 5
SEEDED_SLOTS_DAY_AFTER = 1

FONT_DISPLAY = "Playfair Display"
FONT_INTERFACE = "Syne"
FONT_BODY = "Lexend Deca"
TYPE_RAMP = ("12px", "13px", "14px", "15px", "16px", "20px", "30px")
MANIFESTO_SIZE = "16px"
MANIFESTO_LEADING = "24px"

PUBLIC_ROUTES = ("/", "/offers", "/expertise", "/projects", "/method", "/about",
                 "/contact", "/privacy", "/book")
CLIENT_ROUTES = ("/account/bookings",)
CONSOLE_ROUTES = ("/studio", "/studio/slots", "/studio/enquiries", "/studio/projects")
ABSENT_SURFACES = ("/cart", "/checkout", "/comments", "/shortlist", "/quote",
                   "/messages")

APP_ROOT = "/app"
CREDENTIALS_FILE = "/app/USER_README.md"
SCREENSHOT_DIR = "/app/.browser_screenshots"
DOWNLOAD_DIR = "/app/.downloads"

TABLE_ACCOUNT = "accounts"
TABLE_SERVICE = "services"
TABLE_PROJECT = "projects"
TABLE_PROJECT_TAG = "project_tags"
TABLE_PROJECT_MEDIA = "project_media"
TABLE_PACKAGE = "packages"
TABLE_PACKAGE_PANEL = "package_panels"
TABLE_PACKAGE_FIT = "package_fit"
TABLE_TESTIMONIAL = "testimonials"
TABLE_AWARD = "awards"
TABLE_METHOD_STEP = "method_steps"
TABLE_METHOD_AUDIENCE = "method_audience"
TABLE_PROFILE = "studio_profile"
TABLE_SLOT = "slots"
TABLE_BOOKING = "bookings"
TABLE_ENQUIRY = "enquiries"
TABLE_PAGE_IDENTITY = "page_identity"
TABLE_COUNT = 16

ISO_MOMENT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2})?(\.\d+)?([+-]\d{2}:?\d{2})?$")

SETTLE_SECONDS = 0.25
POLL_TIMEOUT_SECONDS = 20.0
RACE_ATTEMPTS = 2

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


def probe_surname(suffix: str) -> str:
    return "Probe " + suffix


def probe_topic(suffix: str) -> str:
    return "A first conversation about a rebuild, reference " + suffix


def probe_message(suffix: str) -> str:
    return ("We are relaunching a small range next season and want the site to carry "
            "the new positioning, reference " + suffix)


def describe(response: httpx.Response, what: str) -> str:
    """The failure-message shape reference/J requires: anchor, request, status, body."""
    return (f"{what}: {response.request.method} {response.request.url} returned "
            f"{response.status_code}: {response.text[:400]}")


def backend() -> capabilities.Backend:
    """The persisted-state view the brief's own table names address."""
    return capabilities.make_backend()


def inbox() -> capabilities.Inbox:
    """The mail provider the brief names, reached with the shared credentials."""
    return capabilities.make_inbox()


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


def meta_content(markup: str, needle: str) -> str:
    """The content of the first meta tag whose attributes mention `needle`."""
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
        if needle in tag.lower():
            for quote in ('content="', "content='"):
                at = tag.find(quote)
                if at >= 0:
                    rest = tag[at + len(quote):]
                    stop = rest.find(quote[-1])
                    return rest[:stop].strip() if stop >= 0 else rest.strip()
        cursor = end + 1


def meta_description(markup: str) -> str:
    return meta_content(markup, 'name="description"') or meta_content(markup, "description")


def document_language(markup: str) -> str:
    found = re.search(r"<html[^>]*\blang=[\"']([^\"']+)", markup, re.IGNORECASE)
    return found.group(1).strip() if found else ""


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


def get_json(path: str, token: str | None = None):
    with appclient.client(token) as client:
        response = client.get(path)
    return response


def rows(payload) -> list:
    """A list endpoint returns a top-level JSON array; tolerate a wrapped shape."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "results", "data"):
            if isinstance(payload.get(key), list):
                return payload[key]
    return []


def field(record: dict, *names):
    """The first present field among a few conventional spellings."""
    for name in names:
        if isinstance(record, dict) and name in record:
            return record[name]
    return None


def open_slots(token: str | None = None) -> list:
    response = get_json("/slots", token)
    return [s for s in rows(response.json())
            if field(s, "is_available", "available") is not False
            and field(s, "state") != SLOT_CLOSED]


def hold_slot(token: str, slot_id) -> httpx.Response:
    with appclient.client(token) as client:
        return client.post(f"/slots/{slot_id}/hold")


def answer_hold(token: str, reference: str, **overrides) -> httpx.Response:
    body = {"sector": SECTORS[0], "topic": probe_topic(unique_suffix())}
    body.update(overrides)
    with appclient.client(token) as client:
        return client.patch(f"/bookings/{reference}", json=body)


def confirm_booking(token: str, reference: str) -> httpx.Response:
    with appclient.client(token) as client:
        return client.post(f"/bookings/{reference}/confirm")


def cancel_booking(token: str, reference: str) -> httpx.Response:
    with appclient.client(token) as client:
        return client.post(f"/bookings/{reference}/cancel")


def take_a_slot(token: str) -> tuple[str, object]:
    """Hold the first open slot and return its booking reference plus the slot id."""
    available = open_slots(token)
    assert available, "the seeded calendar must offer an open slot to hold"
    slot = available[0]
    slot_id = field(slot, "id", "slot_id")
    response = hold_slot(token, slot_id)
    assert response.status_code in ACCEPTED, describe(
        response, "a signed-in client must be able to hold an open slot")
    reference = field(response.json(), "reference")
    assert reference, describe(response, "a hold must return a booking reference")
    return str(reference), slot_id


def booking_row(reference: str) -> dict:
    store = backend()
    row = poll_until(lambda: store.one(TABLE_BOOKING, reference=reference))
    assert row, f"no {TABLE_BOOKING} row carries the reference {reference}"
    return row


def enquiry_row(reference: str) -> dict:
    store = backend()
    row = poll_until(lambda: store.one(TABLE_ENQUIRY, reference=reference))
    assert row, f"no {TABLE_ENQUIRY} row carries the reference {reference}"
    return row


def enquiry_body(suffix: str, **overrides) -> dict:
    body = {
        "surname": probe_surname(suffix),
        "first_name": "Robin",
        "telephone": "",
        "email": probe_address(suffix),
        "project_type": PROJECT_TYPES[0],
        "budget_band": BUDGET_BANDS[3],
        "message": probe_message(suffix),
        "source": "A friend",
        "consent": True,
    }
    body.update(overrides)
    return body


def submit_enquiry(body: dict) -> httpx.Response:
    with appclient.client(None) as client:
        return client.post("/enquiries", json=body)


def accepted_enquiry(suffix: str, **overrides) -> tuple[str, dict]:
    body = enquiry_body(suffix, **overrides)
    response = submit_enquiry(body)
    assert response.status_code in ACCEPTED, describe(
        response, "a complete enquiry must be accepted")
    reference = field(response.json(), "reference")
    assert reference, describe(response, "an accepted enquiry must carry a reference")
    return str(reference), body


def confirmation_for(address: str):
    """The confirmation the mail provider holds for one recipient, once it lands."""
    box = inbox()
    return poll_until(lambda: box.find(address, CONFIRMATION_SUBJECT_PREFIX))


def message_count(address: str | None = None) -> int:
    """How many messages the mail provider holds, for one recipient or for all."""
    return inbox().count(address)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_moment(value) -> datetime | None:
    """A stored moment as a timezone-aware datetime, or None when it is absent.

    An unreadable moment is returned as None rather than raised, so the caller
    asserts on the value it expected and names the field in its own message.
    """
    if not value:
        return None
    text = str(value).replace("Z", "+00:00")
    if not ISO_MOMENT_RE.match(text):
        return None
    moment = datetime.fromisoformat(text)
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def within(actual: datetime, expected: datetime, minutes: int = 5) -> bool:
    return abs((actual - expected).total_seconds()) <= minutes * 60


def promise_window() -> timedelta:
    return timedelta(hours=PROMISE_HOURS)


@pytest.fixture()
def studio() -> str:
    return appclient.login(STUDIO_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def client_one() -> str:
    return appclient.login(CLIENT_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def client_two() -> str:
    return appclient.login(CLIENT2_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def suffix() -> str:
    return unique_suffix()
