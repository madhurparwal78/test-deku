from __future__ import annotations

import os
import time

import pytest

import appclient
import capabilities

SEEDED_PASSWORD = appclient.seeded_password("DEKU_SEED_PASSWORD", "deku-demo-pw-2026")

STUDIO_EMAIL = "studio@example.com"
CLIENT_EMAIL = "client@example.com"

STUDIO_NAME = "Elian Moreau"
CLIENT_NAME = "Alex Renard"
STUDIO_ORGANISATION = "Atelier Moreau"
CLIENT_ORGANISATION = "Northgate"

ROLE_CLIENT = "client"
ROLE_STUDIO = "studio"

HOLD_HOURS = 72
ENQUIRY_TOKEN_DAYS = 90
BEARER_TOKEN_HOURS = 24
OPEN_NOW_HORIZON_DAYS = 14
LAPSE_SILENCE_DAYS = 30
PROPOSAL_WARNING_HOURS = 48
LIVE_HOLD_CEILING = 3

MODE_OPEN_NOW = "open_now"
MODE_OPEN_FROM = "open_from"
MODE_BOOKED_UNTIL = "booked_until"
MODE_NOT_TAKING = "not_taking"

PILL_OPEN_NOW = "available now for work"
PILL_OPEN_FROM = "available from"
PILL_BOOKED_UNTIL = "booked until"
PILL_NOT_TAKING = "not taking new work"

WINDOW_OPEN = "open"
WINDOW_HELD = "held"
WINDOW_BOOKED = "booked"
WINDOW_CLOSED = "closed"

ENQUIRY_NEW = "new"
ENQUIRY_READING = "reading"
ENQUIRY_PROPOSED = "proposed"
ENQUIRY_BOOKED = "booked"
ENQUIRY_DECLINED = "declined"
ENQUIRY_WITHDRAWN = "withdrawn"
ENQUIRY_LAPSED = "lapsed"

PROPOSAL_LIVE = "live"
PROPOSAL_ACCEPTED = "accepted"
PROPOSAL_EXPIRED = "expired"
PROPOSAL_SUPERSEDED = "superseded"

BUDGET_BANDS = (
    "USD $20001 and up",
    "USD $10001-$20000",
    "USD $5001-$10000",
    "USD $2000-$5000",
)

FIELD_LABELS = (
    "My Name",
    "My Email",
    "I work at",
    "I am looking for",
    "My budget is",
    "My message",
)

ERROR_MISSING_NAME = "We need something to call you."
ERROR_MISSING_EMAIL = "We need an address to reply to."
ERROR_LONG_ORGANISATION = "That is longer than we can store."
ERROR_MISSING_SUBJECT = "A few words about what you need."
ERROR_MISSING_BAND = "Choose a range, even a rough one."
ERROR_SHORT_MESSAGE = "Tell us a little more, at least twenty characters."

FOURTH_HOLD_REFUSAL = "This window is nearly full. Send an enquiry without holding it."
BAND_FLOOR_LINE = (
    "Smaller than that? Say so in your message and we will point you somewhere good."
)
SUBMIT_COPY = "Send it now :)"
LAPSED_HOLD_BAND = "Your hold on that window ran out. You can still send this."
FILLED_WINDOW_REFUSAL = "That window filled up. Here is what is open."
EXPIRED_PROPOSAL_REFUSAL = "That proposal has expired. Ask for a new one."
SIGNIN_LINK_RESPONSE = (
    "If that address has an enquiry with us, a sign-in link is on its way."
)

SUBJECT_CONFIRMATION = "We have your enquiry"
SUBJECT_NOTIFICATION = "New enquiry"
SUBJECT_STUDIO_REPLY = "A reply to your enquiry"
SUBJECT_CLIENT_REPLY = "A reply from"
SUBJECT_PROPOSAL = "A start date for your project"
SUBJECT_BOOKED = "Booked"
SUBJECT_EXPIRING = "Your start date offer expires soon"
SUBJECT_DECLINED = "About your enquiry"
SUBJECT_SIGNIN_LINK = "Your sign-in link"

EMPTY_ACCOUNT_STATE = "An enquiry appears here once you send one."
EMPTY_PIPELINE_STATE = "The pipeline is clear."
EMPTY_WORK_STATE = "No projects listed."
FAILED_READ_STATE = "That did not load."
RETRY_CONTROL = "Try again"
DENIED_SURFACE_COPY = "That is not yours to open."
MISSING_SURFACE_COPY = "We cannot find that."
OFFLINE_STATE_COPY = "You are offline. Your draft is safe."

SOUND_ACCESSIBLE_NAME = "Turn sound on"
RAIL_LABEL = "Honors"
CURSOR_LABEL = "View"
HERO_EYEBROW = "Creative Developer"
HERO_LOCATION = "Located in France"
HERO_PROMPT = "Scroll down to explore"
ABOUT_FIGURE = "5+"
ABOUT_FIGURE_LABEL = "years of experience"
CONTACT_HEADLINE = "LET'S BUILD YOUR IDEA TOGETHER :)"
CONTACT_SIDE_HEAD = "Further Inquiries"
WORK_HEADLINE = (
    "Elevate user experience through cutting-edge technology and design"
)
WORK_INDEX_COUNT = "(09)"
NAVIGATION_TARGETS = ("Home", "About", "Work", "Contact")
FOOTER_HEADS = ("Local Time", "Version", "Resource", "Social Media")
SOCIAL_LABELS = ("Linkedin", "Postline", "Showcase")
SERVICE_TITLES = ("SEO", "UX Design", "Web & Mobile Development")

SEEDED_PROJECTS = (
    "Meridian",
    "Auriga Concept",
    "Portfolio 2.0",
    "Uplink Usability",
    "Tower Supervision",
    "Colisa",
    "UBX Roadmap",
    "Aera Unity",
    "Baba Quiz",
)

SEEDED_WINDOWS = (
    {"offset_days": 10, "weeks": 6, "capacity_days": 3, "state": WINDOW_OPEN,
     "committed_days": 0},
    {"offset_days": 40, "weeks": 8, "capacity_days": 2, "state": WINDOW_OPEN,
     "committed_days": 0},
    {"offset_days": 90, "weeks": 4, "capacity_days": 2, "state": WINDOW_BOOKED,
     "committed_days": 2},
)

BAR_PROJECTS = 9
BAR_WINDOWS = 40
BAR_ENQUIRIES = 500
BAR_MESSAGES = 2000

HOME_ROUTE = "/"
WORK_ROUTE = "/work"
CONTACT_ROUTE = "/contact"
AVAILABILITY_ROUTE = "/availability"
PRIVACY_ROUTE = "/legal/privacy"
TERMS_ROUTE = "/legal/terms"
SIGNIN_ROUTE = "/signin"
ACCOUNT_ROUTE = "/account"
STUDIO_ROUTE = "/studio"
PIPELINE_ROUTE = "/studio/pipeline"
SITEMAP_ROUTE = "/sitemap.xml"
ROBOTS_ROUTE = "/robots.txt"
HEALTH_ENDPOINT = "/api/health"
CONTAINER_PORT = "4173"
BIND_ADDRESS = "0.0.0.0"
CREDENTIALS_FILE = "/app/USER_README.md"
SCREENSHOT_DIR = "/app/.browser_screenshots"
DOWNLOAD_DIR = "/app/.downloads"
API_PREFIX = "/api"

PUBLIC_ROUTES = (
    HOME_ROUTE,
    WORK_ROUTE,
    CONTACT_ROUTE,
    AVAILABILITY_ROUTE,
    PRIVACY_ROUTE,
    TERMS_ROUTE,
    SIGNIN_ROUTE,
)

OK = (200, 201)
DENIED = (401, 403, 404)
REFUSED = (400, 409, 422)
RATE_LIMITED = (429,)

SETTLE_SECONDS = 0.5
SETTLE_ATTEMPTS = 20


def settle(predicate, attempts: int = SETTLE_ATTEMPTS, pause: float = SETTLE_SECONDS):
    """The only sanctioned wait. Polls a bounded number of times for an
    asynchronous side effect and returns the first truthy result, else None."""
    result = None
    for _ in range(attempts):
        result = predicate()
        if result:
            return result
        time.sleep(pause)
    return result


def probe_email(label: str) -> str:
    return f"probe-{label}-{os.urandom(6).hex()}@example.com"


def probe_name(label: str) -> str:
    return f"Probe {label.title()} {os.urandom(3).hex()}"


def body(response) -> str:
    """The failure-message excerpt. Byte content is decoded leniently so a
    binary download still produces a readable message."""
    return response.content[:400].decode("utf-8", errors="replace")


def app_url() -> str:
    return appclient.app_url()


def page(path: str, follow_redirects: bool = True):
    import httpx

    return httpx.get(
        f"{app_url()}{path}", timeout=appclient.TIMEOUT,
        follow_redirects=follow_redirects,
    )


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def inbox():
    return capabilities.make_inbox()


@pytest.fixture(scope="session")
def studio_token() -> str:
    return appclient.login(STUDIO_EMAIL, SEEDED_PASSWORD)


@pytest.fixture(scope="session")
def client_token() -> str:
    return appclient.login(CLIENT_EMAIL, SEEDED_PASSWORD)


@pytest.fixture
def studio(studio_token):
    with appclient.client(studio_token) as c:
        yield c


@pytest.fixture
def client(client_token):
    with appclient.client(client_token) as c:
        yield c


@pytest.fixture
def anonymous():
    with appclient.client() as c:
        yield c


def _items(payload):
    import _shapes

    return _shapes.items(payload)


def flat(payload) -> str:
    import _shapes

    return _shapes.flatten(payload)


def read(client, path: str, expect=OK) -> dict | list:
    response = client.get(path)
    assert response.status_code in expect, (
        f"GET {API_PREFIX}{path} returned {response.status_code}, expected one of "
        f"{expect}: {body(response)}"
    )
    return response.json()


def windows_of(client) -> list[dict]:
    payload = read(client, "/availability")
    rows = payload.get("windows") if isinstance(payload, dict) else payload
    return _items(rows)


def availability(client) -> dict:
    payload = read(client, "/availability")
    assert isinstance(payload, dict), (
        f"GET {API_PREFIX}/availability returned {type(payload).__name__}, expected an "
        f"object carrying mode, from_date, note and windows"
    )
    return payload


def open_windows(client) -> list[dict]:
    return [w for w in windows_of(client) if w.get("state") == WINDOW_OPEN]


def first_open_window(client) -> dict:
    found = open_windows(client)
    assert found, (
        f"no window in state {WINDOW_OPEN!r} is reachable at "
        f"{API_PREFIX}/availability; the seed must leave two open"
    )
    return found[0]


def remaining_days(window: dict) -> int:
    return int(window.get("capacity_days", 0)) - int(window.get("committed_days", 0))


def make_window(studio_client, *, offset_days: int = 21, weeks: int = 4,
                capacity_days: int = 2) -> dict:
    import datetime

    starts_on = (
        datetime.date.today() + datetime.timedelta(days=offset_days)
    ).isoformat()
    response = studio_client.post(
        "/windows",
        json={"starts_on": starts_on, "weeks": weeks, "capacity_days": capacity_days},
    )
    assert response.status_code in OK, (
        f"POST {API_PREFIX}/windows returned {response.status_code} for a window of "
        f"{weeks} weeks at {capacity_days} capacity days: {body(response)}"
    )
    return response.json()


def make_hold(client, window_id, days: int = 1):
    return client.post("/holds", json={"window_id": window_id, "days": days})


def enquiry_payload(**overrides) -> dict:
    payload = {
        "name": probe_name("sender"),
        "email": probe_email("sender"),
        "organisation": "Northgate",
        "looking_for": "A booking desk for a studio calendar",
        "budget_band": BUDGET_BANDS[1],
        "message": (
            "We need a small booking surface for a single operator, and would like "
            "to start within the quarter."
        ),
    }
    payload.update(overrides)
    return payload


def submit_enquiry(client, *, hold_id=None, **overrides):
    payload = enquiry_payload(**overrides)
    if hold_id is not None:
        payload["hold_id"] = hold_id
    return client.post("/enquiries", json=payload)


def require_enquiry(client, *, hold_id=None, **overrides) -> dict:
    response = submit_enquiry(client, hold_id=hold_id, **overrides)
    assert response.status_code in OK, (
        f"POST {API_PREFIX}/enquiries returned {response.status_code} for a valid "
        f"six-field brief: {body(response)}"
    )
    return response.json()


def enquiry_state(client, enquiry_id) -> str:
    payload = read(client, f"/enquiries/{enquiry_id}")
    row = payload.get("enquiry", payload) if isinstance(payload, dict) else payload
    return str(row.get("state", ""))


def propose(studio_client, enquiry_id, *, starts_on, weeks=4, days_per_week=1,
            note="A start we can hold"):
    return studio_client.post(
        f"/enquiries/{enquiry_id}/proposals",
        json={"starts_on": starts_on, "weeks": weeks,
              "days_per_week": days_per_week, "note": note},
    )


def accept(client, enquiry_id, proposal_id):
    return client.post(
        f"/enquiries/{enquiry_id}/accept", json={"proposal_id": proposal_id}
    )


def booked_enquiry(studio_client, acting_client, window: dict, *, days_per_week=1):
    """Drive one enquiry all the way to a booking against the given window."""
    hold = make_hold(acting_client, window["id"])
    assert hold.status_code in OK, (
        f"POST {API_PREFIX}/holds returned {hold.status_code} on an open window: "
        f"{body(hold)}"
    )
    enquiry = require_enquiry(acting_client, hold_id=hold.json().get("id"))
    read(studio_client, f"/enquiries/{enquiry['id']}")
    proposal = propose(
        studio_client, enquiry["id"], starts_on=window["starts_on"],
        weeks=int(window.get("weeks", 4)), days_per_week=days_per_week,
    )
    assert proposal.status_code in OK, (
        f"POST {API_PREFIX}/enquiries/{{id}}/proposals returned "
        f"{proposal.status_code} inside the window: {body(proposal)}"
    )
    confirmed = accept(acting_client, enquiry["id"], proposal.json().get("id"))
    assert confirmed.status_code in OK, (
        f"POST {API_PREFIX}/enquiries/{{id}}/accept returned {confirmed.status_code} "
        f"on a live proposal: {body(confirmed)}"
    )
    return enquiry, proposal.json(), confirmed.json()


def token_client(token: str):
    return appclient.client()


def bundle_assets(limit: int = 60) -> list[str]:
    """Every same-origin asset the served home document references."""
    import re

    document = page(HOME_ROUTE)
    hrefs = re.findall(r'(?:src|href)="([^"]+)"', document.text)
    out = []
    for href in hrefs:
        if href.startswith("http") or href.startswith("//") or href.startswith("data:"):
            continue
        if not href.startswith("/"):
            href = "/" + href.lstrip("./")
        if href not in out:
            out.append(href)
    return out[:limit]
