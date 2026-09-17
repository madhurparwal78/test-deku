"""Task fixtures for deku/exhibition-venue-operations-vb.

Implementation-agnostic (reference/J J.2): assume only the App Contract, the
literals pinned in instruction.md, and the capability fixture the declared `db`
slot earns. Observations are made over the JSON API, over the served markup of
the public routes and over the rows in postgres. Nothing here imports a vendor
SDK, reads the agent's source, or probes for a feature at run time. No test
function lives in this file.
"""

from __future__ import annotations

import os
import time
from concurrent.futures import ThreadPoolExecutor

import httpx
import pytest
from appclient import api_base, app_url, client, login
from capabilities import Backend, make_backend

TIMEOUT = 30.0
SETTLE_SECONDS = 2.0
POLL_ATTEMPTS = 15


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give a side effect time to land before asserting on it."""
    time.sleep(seconds)


def unique(prefix: str) -> str:
    """A per-run identifier, so a re-run never collides with its predecessor."""
    return f"{prefix}-{os.urandom(6).hex()}"


def probe_email(prefix: str = "probe") -> str:
    return f"{unique(prefix)}@example.com"


PASSWORD = "deku-demo-pw-2026"

COORDINATOR_EMAIL = "coordinator@example.com"
OPERATIONS_EMAIL = "operations@example.com"
PLANNER_EMAIL = "planner@example.com"
PLANNER2_EMAIL = "planner2@example.com"
EXHIBITOR_EMAIL = "exhibitor@example.com"
FINANCE_EMAIL = "finance@example.com"
AUDITOR_EMAIL = "auditor@example.com"

SEEDED_ACCOUNTS = (COORDINATOR_EMAIL, OPERATIONS_EMAIL, PLANNER_EMAIL,
                   PLANNER2_EMAIL, EXHIBITOR_EMAIL, FINANCE_EMAIL,
                   AUDITOR_EMAIL)

ROLE_COORDINATOR = "coordinator"
ROLE_OPERATIONS = "operations"
ROLE_PLANNER = "planner"
ROLE_EXHIBITOR = "exhibitor"
ROLE_FINANCE = "finance"
ROLE_AUDITOR = "auditor"
ROLES = (ROLE_COORDINATOR, ROLE_OPERATIONS, ROLE_PLANNER, ROLE_EXHIBITOR,
         ROLE_FINANCE, ROLE_AUDITOR)

LANGUAGES = ("nl", "fr", "en")

HALL_ONE = "Hall 1"
HALL_TWO = "Hall 2"
HALL_THREE = "Hall 3"
HALL_FOUR = "Hall 4"
HALL_FIVE = "Hall 5"
HALL_SIX = "Hall 6"
EVENT_HALL = "The Event Hall"
MEETING_ROOMS = ("MC 1", "MC 2", "MC 3", "MC 4")
BOULEVARD = "The Concourse"
PASSAGE = "The Transit"

SEEDED_SPACES = (HALL_ONE, HALL_TWO, HALL_THREE, HALL_FOUR, HALL_FIVE,
                 HALL_SIX, EVENT_HALL) + MEETING_ROOMS + (BOULEVARD, PASSAGE)

SPACE_KINDS = ("hall", "event_hall", "meeting_room", "boulevard", "passage",
               "combination")

HALL_AREAS = {
    HALL_ONE: 6090,
    HALL_TWO: 4058,
    HALL_THREE: 3601,
    HALL_FOUR: 7685,
    HALL_FIVE: 4723,
    HALL_SIX: 5055,
    EVENT_HALL: 2000,
}
HALL_CAPACITIES = {
    HALL_ONE: 1620,
    HALL_TWO: 1740,
    HALL_THREE: 1680,
    HALL_FOUR: 3660,
    HALL_FIVE: 5160,
    HALL_SIX: 1860,
    EVENT_HALL: 2000,
}
MEETING_CENTRE_AREA = 1679
TRIBUNE_SEATS = 550

COMBINATION_HALLS = "Halls 4 and 5 with the Transit"
COMBINATION_HALLS_CAPACITY = 7400
COMBINATION_HALLS_SUM = 8820
COMBINATION_MEETING = "The Meeting Centre with the Event Hall"
COMBINATION_MEETING_CAPACITY = 2600

LAYOUTS = ("theatre", "cabaret", "banquet", "stand_grid", "standing")

ENTRANCE_NORTH = "North Entrance"
ENTRANCE_SOUTH = "South Entrance"
ENTRANCE_CONCOURSE_EAST = "Concourse East"
ENTRANCE_CONCOURSE_WEST = "Concourse West"
ENTRANCE_DOCK = "Dock Gate"
SEEDED_ENTRANCES = (ENTRANCE_NORTH, ENTRANCE_SOUTH, ENTRANCE_CONCOURSE_EAST,
                    ENTRANCE_CONCOURSE_WEST, ENTRANCE_DOCK)
ENTRANCE_MODES = ("staff", "contractor", "exhibitor", "trade", "public",
                  "closed")

PARKING_SPACES = 2500

PARTY_ORGANISER_ONE = "Palmarosa"
PARTY_ORGANISER_TWO = "Bookmark Fair"
PARTY_EXHIBITOR = "Ironwood Interiors"
PARTY_KINDS = ("organiser", "exhibitor", "contractor", "venue_staff",
               "caterer", "security", "cleaner", "visitor")
STAND_REF = "S-118"

BOOKING_PUBLISHED = "Verwick Design Days"
BOOKING_PUBLIC = "Bookmark Fair"
BOOKING_PRIVATE = "Ironwood Night"

PHASE_KINDS = ("access", "build_up", "run", "tear_down", "clearance")

AVAILABILITY_STATES = ("free", "held", "booked", "blocked_by_ancestor",
                       "blocked_by_descendant", "maintenance")
HOLD_KINDS = ("option", "booking", "maintenance")
OPTION_STATES = ("held", "challenged", "released", "confirmed", "lapsed")
REVISION_STATES = ("draft", "submitted", "approved", "withdrawn")
PLAN_OBJECT_KINDS = ("stand", "catering_point", "stage", "seating_block",
                     "entrance_point")
PLAN_CONSTRAINT_KINDS = ("column", "truss", "door", "fire_exit",
                         "rigging_point", "power_point", "water_point")
ACCREDITATION_STATES = ("pending_evidence", "valid", "expired", "revoked")
EVIDENCE_KINDS = ("insurance", "risk_assessment", "competence", "identity")
SCAN_DECISIONS = ("admitted", "refused")
REFUSAL_REASONS = ("no_accreditation", "wrong_phase", "wrong_space",
                   "expired_evidence", "revoked", "at_capacity",
                   "anti_passback")
OCCUPANCY_STATES = ("clear", "approaching", "at_limit")
SERVICE_ORDER_STATES = ("draft", "ordered", "late_ordered", "cancelled",
                        "delivered")
SERVICE_CATEGORIES = ("catering", "technical", "furniture", "cleaning",
                      "waste", "signage", "parking")
PAYMENT_KINDS = ("deposit", "stage", "final", "credit")
PUBLICATION_STATES = ("private", "announced", "published")
TRANSLATION_STATES = ("missing", "draft", "published")
SUBSCRIPTION_STATES = ("sent", "invalid", "already")
SEARCH_STATES = ("ok", "invalid", "failed")
RESOURCE_KINDS = ("dock", "lift", "forklift", "crew", "power_drop")
CAMPUS_STATES = ("normal", "evacuation")

HALL_FOUR_DAY_RATE_MINOR = 1450000

STATUS_CHIP_PUBLIC = "Open to the public"
STATUS_CHIP_TRADE = "Trade fair - registration required"
SECTOR_DESIGN = "Architecture & Design"
SECTOR_LIFESTYLE = "Lifestyle & Sports"
SECTOR_SUSTAINABILITY = "Sustainability"

HERO_LINE = "when ideas need space"
SEARCH_LABEL = "Search entire website"
SKIP_LINK = "Skip to main content"
COPYRIGHT_LINE = "(C) 2026 Verwick Xpo"
NOT_FOUND_HEADING = "Page not found"
NOT_FOUND_ACTION = "Go to homepage"
NEWS_CORPORATE = ("Calderhook Group completes acquisition of "
                  "Northtide Venues Group")
NEWS_SUSTAINABILITY = ("Verwick Xpo achieves the Westmark sustainability "
                       "charter for the 10th consecutive year")

OK_STATUS = (200, 201)
DENIED_STATUS = (401, 403)
NOT_FOUND_STATUS = (404,)
REFUSED_STATUS = (400, 401, 403, 404, 409, 422)
CONFLICT_STATUS = (409, 412, 422)


def describe(response: httpx.Response, what: str) -> str:
    """Failure prose naming the anchor, the request, the status and the body."""
    return (f"{what}: {response.request.method} {response.request.url} "
            f"returned {response.status_code}, body {response.text[:400]!r}")


@pytest.fixture(scope="session")
def base_url() -> str:
    return app_url()


@pytest.fixture(scope="session")
def api() -> str:
    return api_base()


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def coordinator_token() -> str:
    return login(COORDINATOR_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def operations_token() -> str:
    return login(OPERATIONS_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def planner_token() -> str:
    return login(PLANNER_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def planner2_token() -> str:
    return login(PLANNER2_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def exhibitor_token() -> str:
    return login(EXHIBITOR_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def finance_token() -> str:
    return login(FINANCE_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def auditor_token() -> str:
    return login(AUDITOR_EMAIL, PASSWORD)


@pytest.fixture()
def coordinator(coordinator_token: str):
    with client(coordinator_token) as c:
        yield c


@pytest.fixture()
def operations(operations_token: str):
    with client(operations_token) as c:
        yield c


@pytest.fixture()
def planner(planner_token: str):
    with client(planner_token) as c:
        yield c


@pytest.fixture()
def planner2(planner2_token: str):
    with client(planner2_token) as c:
        yield c


@pytest.fixture()
def exhibitor(exhibitor_token: str):
    with client(exhibitor_token) as c:
        yield c


@pytest.fixture()
def finance(finance_token: str):
    with client(finance_token) as c:
        yield c


@pytest.fixture()
def auditor(auditor_token: str):
    with client(auditor_token) as c:
        yield c


@pytest.fixture()
def anonymous():
    with client(None) as c:
        yield c


@pytest.fixture()
def web():
    """An unauthenticated client against the served routes, not the API."""
    with httpx.Client(base_url=app_url(), timeout=TIMEOUT,
                      follow_redirects=True) as c:
        yield c


def json_of(response: httpx.Response, what: str):
    assert response.status_code in OK_STATUS, describe(response, what)
    return response.json()


def find_named(rows, name: str):
    """The row whose `name` field equals `name`, or None."""
    for row in rows:
        if isinstance(row, dict) and row.get("name") == name:
            return row
    return None


def space_row(session: httpx.Client, name: str):
    from _shapes import items
    payload = json_of(session.get("/spaces"),
                      f"the space catalog listing {name!r}")
    row = find_named(items(payload), name)
    assert row is not None, (
        f"the space catalog names no space {name!r}; the seeded spaces are "
        f"{list(SEEDED_SPACES)}. Listing was {payload!r}"[:600])
    return row


def public_space_row(session: httpx.Client, name: str):
    from _shapes import items
    payload = json_of(session.get("/public/spaces"),
                      f"the public space list naming {name!r}")
    row = find_named(items(payload), name)
    assert row is not None, (
        f"the public space list names no space {name!r}; the seeded spaces are "
        f"{list(SEEDED_SPACES)}. Listing was {payload!r}"[:600])
    return row


def availability(session: httpx.Client, space: str, start: str, end: str):
    return session.get("/availability",
                       params={"space": space, "from": start, "to": end})


def state_of(response: httpx.Response, what: str) -> str:
    payload = response.json() if response.content else {}
    assert isinstance(payload, dict), describe(response, what)
    state = payload.get("state")
    assert isinstance(state, str), (
        f"{what}: the answer carries no string `state`; body "
        f"{response.text[:400]!r}")
    return state


def held_window(session: httpx.Client, booking_name: str):
    """The window of a seeded booking, read back from its own record."""
    from _shapes import items
    payload = json_of(session.get("/bookings"),
                      f"the booking list naming {booking_name!r}")
    row = find_named(items(payload), booking_name)
    assert row is not None, (
        f"the booking list names no booking {booking_name!r}; the seeded "
        f"bookings are {BOOKING_PUBLISHED!r}, {BOOKING_PUBLIC!r} and "
        f"{BOOKING_PRIVATE!r}. Listing was {payload!r}"[:600])
    return row


def poll_for(predicate, attempts: int = POLL_ATTEMPTS):
    """Bounded polling for an asynchronous side effect. Never an unbounded loop
    and never a retry that hides a failure: the last observation is returned and
    the caller asserts on it."""
    observed = None
    for _ in range(attempts):
        observed = predicate()
        if observed:
            return observed
        settle(1.0)
    return observed


def in_parallel(call, count: int = 2):
    """Fire `count` identical calls at once and return every response."""
    with ThreadPoolExecutor(max_workers=count) as pool:
        futures = [pool.submit(call) for _ in range(count)]
        return [f.result() for f in futures]
