from __future__ import annotations

import os
import time
import uuid

import httpx
import pytest
from playwright.sync_api import sync_playwright

from capabilities import make_backend, make_store

APP_URL = os.environ.get("APP_PUBLIC_URL", "http://localhost:4173").rstrip("/")
API = f"{APP_URL}/api"

CORPUS_PASSWORD = "deku-demo-pw-2026"
AUTHOR_EMAIL = "author@example.com"
SECOND_AUTHOR_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"
AUTHOR_NAME = "Nils Adeyemi Karlsen"
SECOND_AUTHOR_NAME = "Wren Adeyemi Karlsen"
READER_NAME = "Juno Castellane"

BAND_SLUGS = ("hero", "manifesto", "experience", "philosophy", "systems",
              "open-source", "stack", "signal", "footer")
BAND_FIELDS = ("slug", "name", "start_fraction", "end_fraction")

NODE_KINDS = ("box", "gate", "store", "terminal")
EDGE_KINDS = ("plain", "active", "drift")
TIMELINE_EFFECTS = ("travel", "sweep", "gate", "promote", "drift", "enter", "pulse")

POST_STATUSES = ("draft", "published")
POST_SERIES = ("ENG", "THT")
NOTE_INTENTS = ("Hiring", "Consulting", "Collaboration", "Something else")
NOTE_STATES = ("new", "read", "replied", "closed", "spam")
NOTE_LANES = ("signal", "unsorted", "likely noise")
SUBSCRIBER_STATES = ("pending", "confirmed", "unsubscribed")
BOOKING_STATES = ("held", "confirmed", "cancelled")

DIAGRAM_KEY_SCHEME = "diagrams/{diagram_id}/{sha256_of_bytes}.{ext}"
POST_KEY_SCHEME = "posts/{post_id}/{sha256_of_bytes}.{ext}"
DIAGRAM_KEY_PREFIX = "diagrams/"
POST_KEY_PREFIX = "posts/"

NAME_MIN = 2
NAME_MAX = 80
MESSAGE_MIN = 20
MESSAGE_MAX = 4000
CONFIRM_TOKEN_DAYS = 7
SLOT_HOLD_MINUTES = 10
RETENTION_MONTHS = 13
SERIES_SAMPLE_COUNT = 70
LANE_SIGNAL_FLOOR = 4
LANE_UNSORTED_FLOOR = 0
LANE_UNSORTED_CEILING = 3
NOTES_PER_HOUR = 3
TOKEN_LIFETIME_HOURS = 12

PUBLISHED_POST = "Most video AI gives you bullet points. I built one that gives you a map."
SECOND_PUBLISHED_POST = "A developer's guide to taste in the age of AI"
DRAFT_POST = "Everything I got wrong about retrieval"
PUBLISHED_POST_CODE = "ENG-001"
SECOND_PUBLISHED_POST_CODE = "THT-001"
DRAFT_POST_CODE = "ENG-002"

FIRST_SYSTEM = "Ferrite"
CLIENT_SYSTEM_LINE = ("Client system. The names, the internals, and the data "
                      "stay with the client.")
HEADLINE = "I build machines that read the world."
MANIFESTO = "I learned engineering from broken things."
ROLE_LINE = "AI Engineer / Founder of Ferrite / Halifax"
NAME_LINE = "Nils Adeyemi Karlsen"
SCROLL_CUE = "scroll down"
PHILOSOPHY_DIVIDER = "HOW I BUILD"
SYSTEMS_HEADING = "Things people depend on at work."
CONTRIBUTION_LABEL = "MY PART:"
ARCHIVE_TITLE = "Blog"
ARCHIVE_SUBTITLE = "Frequency log - tuning into thoughts on AI, taste, and craft"
CONTACT_LABEL = "LET'S TALK"
FOOTER_CREDIT = "Designed by Studio Halvard"
COUNTER_PHRASE = "synapses fired while you're here"
PANEL_TITLE = "Send a signal"
PANEL_SUBTITLE = "A sentence about what you are working on is plenty."
SHORT_MESSAGE_LINE = "A little more detail would help."
BAD_ADDRESS_LINE = "That address does not look right."
RATE_LIMIT_LINE = "That is a few too many in an hour. Try again later."
NOT_FOUND_CODE = "404"
NOT_FOUND_LINE = "This page could not be found."
NOT_FOUND_ACTION = "Return home"
EMPTY_DESK_TITLE = "Nothing waiting"
EMPTY_DESK_LINE = "Notes appear here as they arrive."
EMPTY_EDITOR_TITLE = "No diagram open"
EMPTY_EDITOR_LINE = "Create one or open an existing diagram to begin."
DESK_ACTIONS = ("Reply", "Snooze", "Close", "Mark noise")

TOP_BAR_ENTRIES = ("blog", "systems", "open source", "signal")
PUBLIC_ROUTES = ("/", "/blog", "/signal", "/privacy")
PROTECTED_ROUTES = ("/studio", "/desk", "/account")
NARROW_VIEWPORT = {"width": 390, "height": 844}
WIDE_VIEWPORT = {"width": 1440, "height": 900}
SETTLE_SECONDS = 0.5
SETTLE_ATTEMPTS = 40


def settle(seconds: float = SETTLE_SECONDS) -> None:
    time.sleep(seconds)


def poll(predicate, attempts: int = SETTLE_ATTEMPTS):
    last = None
    for _ in range(attempts):
        last = predicate()
        if last:
            return last
        settle()
    return last


def probe_email() -> str:
    return f"probe-{uuid.uuid4().hex[:10]}@example.com"


def anchor(label: str, response: httpx.Response) -> str:
    body = response.text[:400] if response.text else ""
    return (f"{label}: {response.request.method} {response.request.url} "
            f"answered {response.status_code} with body {body!r}")


@pytest.fixture(scope="session")
def api_base() -> str:
    return API


@pytest.fixture(scope="session")
def app_url() -> str:
    return APP_URL


@pytest.fixture()
def client():
    with httpx.Client(base_url=API, timeout=30.0, follow_redirects=False) as c:
        yield c


@pytest.fixture()
def site():
    with httpx.Client(base_url=APP_URL, timeout=30.0, follow_redirects=True) as c:
        yield c


def sign_in(client: httpx.Client, email: str, password: str = CORPUS_PASSWORD) -> str:
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code in (200, 201), anchor(f"sign in for {email}", r)
    token = r.json().get("token")
    assert token, anchor(f"sign in for {email} returned no token", r)
    return token


def bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def author_token(client) -> str:
    return sign_in(client, AUTHOR_EMAIL)


@pytest.fixture()
def second_author_token(client) -> str:
    return sign_in(client, SECOND_AUTHOR_EMAIL)


@pytest.fixture()
def reader_token(client) -> str:
    return sign_in(client, READER_EMAIL)


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as driver:
        engine = driver.chromium.launch()
        yield engine
        engine.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context(viewport=WIDE_VIEWPORT)
    sheet = context.new_page()
    yield sheet
    context.close()


@pytest.fixture()
def reduced_motion_page(browser):
    context = browser.new_context(viewport=WIDE_VIEWPORT, reduced_motion="reduce")
    sheet = context.new_page()
    yield sheet
    context.close()


@pytest.fixture()
def ui_page(browser):
    context = browser.new_context(viewport=NARROW_VIEWPORT, is_mobile=True,
                                  has_touch=True)
    sheet = context.new_page()
    yield sheet
    context.close()


@pytest.fixture(scope="session")
def db():
    return make_backend()


@pytest.fixture(scope="session")
def storage():
    return make_store()


def sample_structure(marker: str) -> dict:
    return {
        "nodes": [
            {"id": "source", "kind": "terminal", "label": "SOURCE",
             "sublabel": marker, "state": "idle"},
            {"id": "parse", "kind": "box", "label": "01 PARSE",
             "sublabel": "text, tables, charts, audio, video", "state": "idle"},
            {"id": "evalgate", "kind": "gate", "label": "EVAL",
             "sublabel": "12 / 12 cases", "state": "idle"},
            {"id": "gold", "kind": "store", "label": "PROMOTED TO GOLD",
             "sublabel": "human", "state": "idle"},
        ],
        "edges": [
            {"from": "source", "to": "parse", "kind": "plain", "label": "raw"},
            {"from": "parse", "to": "evalgate", "kind": "active", "label": "typed"},
            {"from": "evalgate", "to": "gold", "kind": "drift", "label": "promote"},
        ],
        "series": [{"name": "sampled", "values": [6 + (i % 13) for i in range(SERIES_SAMPLE_COUNT)]}],
        "annotations": [{"target": "parse", "text": "agent per metric"}],
        "timeline": [
            {"at": 0.15, "target": "source", "effect": "enter"},
            {"at": 0.35, "target": "parse", "effect": "travel"},
            {"at": 0.55, "target": "evalgate", "effect": "gate"},
            {"at": 0.75, "target": "gold", "effect": "promote"},
        ],
        "layout": {"narrow": {"flow": "column", "gap": 3},
                   "wide": {"flow": "row", "gap": 3}},
    }


def make_diagram(client: httpx.Client, token: str, title: str,
                 structure: dict | None = None) -> dict:
    payload = {"title": title,
               "structure": structure or sample_structure(title),
               "alt_text": ("A source feeds a parse stage, the parse stage feeds "
                            "an eval gate, and the gate promotes to a gold store "
                            "only after a human confirms.")}
    r = client.post("/diagrams", json=payload, headers=bearer(token))
    assert r.status_code in (200, 201), anchor(f"create diagram {title}", r)
    return r.json()


def make_post(client: httpx.Client, token: str, title: str,
              diagram_slug: str | None = None, series: str = "ENG") -> dict:
    payload = {"series": series, "title": title,
               "summary": "A seeded summary for the drafted piece.",
               "body": "A seeded body for the drafted piece, long enough to read."}
    if diagram_slug:
        payload["diagram_slug"] = diagram_slug
    r = client.post("/posts", json=payload, headers=bearer(token))
    assert r.status_code in (200, 201), anchor(f"create piece {title}", r)
    return r.json()


def export_still(client: httpx.Client, token: str, slug: str) -> httpx.Response:
    return client.post(f"/diagrams/{slug}/export", headers=bearer(token))


def slug_of(record: dict) -> str:
    slug = record.get("slug")
    assert slug, f"the created record carries no slug: {record!r}"
    return slug


def long_message(words: int = 40) -> str:
    return " ".join(["retrieval"] * words)


def note_payload(**overrides) -> dict:
    payload = {"name": "Ada Ferreira", "email": probe_email(),
               "intent": "Collaboration",
               "message": ("I read the systems band and I would like to talk "
                           "about an extraction pipeline."),
               "band": "systems"}
    payload.update(overrides)
    return payload
