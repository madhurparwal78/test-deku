from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"
DRIVER_A = "driver@example.com"
DRIVER_B = "driver2@example.com"
DRIVER_C = "driver3@example.com"

PLACE_ORIGIN = "Connaught Place"
PLACE_DESTINATION = "Cyber Hub Gurugram"
PLACE_AIRPORT = "Indira Gandhi Airport"
PLACE_NOIDA = "Noida Sector 18"
PLACE_HAUZ = "Hauz Khas Village"
PLACE_AKSHARDHAM = "Akshardham Temple"
SEEDED_PLACES = (PLACE_ORIGIN, PLACE_DESTINATION, PLACE_NOIDA, PLACE_AIRPORT,
                 PLACE_HAUZ, PLACE_AKSHARDHAM)

SEGMENT_RING_NORTH = "Ring Road North"
SEGMENT_OUTER_RING = "Outer Ring Road"
SEGMENT_NH48 = "NH48 Delhi Gurugram"
SEGMENT_BARAPULLAH = "Barapullah Elevated"
SEGMENT_DND = "DND Flyway"
SEEDED_SEGMENTS = {
    SEGMENT_RING_NORTH: 14,
    SEGMENT_OUTER_RING: 12,
    SEGMENT_NH48: 21,
    SEGMENT_BARAPULLAH: 7,
    SEGMENT_DND: 9,
}
SEEDED_CONDITIONS = {
    SEGMENT_RING_NORTH: "heavy",
    SEGMENT_OUTER_RING: "slowing",
    SEGMENT_NH48: "heavy",
    SEGMENT_BARAPULLAH: "slowing",
    SEGMENT_DND: "clear",
}

REPORT_TYPES = ("police", "jam", "hazard", "closure", "crash", "gas", "place",
                "chat", "carpool")
CONDITION_FACTOR = {"clear": 100, "slowing": 150, "heavy": 250}
BUFFER_MINUTES = 5
REMINDER_LEAD_MINUTES = 15
FRESHNESS_MINUTES = 60
FRESHNESS_CAP_MINUTES = 180
ALTERNATIVE_SAVING_MINUTES = 3

PUBLIC_ROUTES = ("/", "/as", "/gs", "/ul", "/412", "/416", "/417", "/419",
                 "/privacy", "/terms", "/login", "/signup")

SETTLE_SECONDS = 2.0
POLL_BUDGET_SECONDS = 20.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned sleep. A bounded wait before asserting a non-event."""
    time.sleep(seconds)


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def future_arrival(minutes_ahead: int = 240) -> str:
    return iso(now_utc() + timedelta(minutes=minutes_ahead))


def past_arrival(minutes_behind: int = 240) -> str:
    return iso(now_utc() - timedelta(minutes=minutes_behind))


def iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(value: str) -> datetime:
    text = str(value).strip().replace("Z", "+00:00")
    return datetime.fromisoformat(text).astimezone(timezone.utc)


def probe_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url.path} -> "
            f"{response.status_code}: {response.text[:400]}")


def poll_until(predicate, budget: float = POLL_BUDGET_SECONDS):
    """Bounded polling to a monotonic deadline. Returns the last value seen."""
    deadline = time.monotonic() + budget
    value = predicate()
    while not value and time.monotonic() < deadline:
        settle(1.0)
        value = predicate()
    return value


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture
def anon():
    with appclient.client() as session:
        yield session


@pytest.fixture
def driver_a():
    with appclient.client(appclient.login(DRIVER_A, PASSWORD)) as session:
        yield session


@pytest.fixture
def driver_b():
    with appclient.client(appclient.login(DRIVER_B, PASSWORD)) as session:
        yield session


@pytest.fixture
def driver_c():
    with appclient.client(appclient.login(DRIVER_C, PASSWORD)) as session:
        yield session


@pytest.fixture
def fresh_driver():
    """A self-seeded driver, so a test never depends on another test's state."""
    email = probe_email()
    response = httpx.post(
        f"{appclient.api_base()}/auth/signup",
        json={"email": email, "password": PASSWORD, "display_name": "Probe Driver"},
        timeout=appclient.TIMEOUT,
    )
    assert response.status_code in (200, 201), (
        f"signup for the probe driver {email} failed: {describe(response)}")
    token = response.json().get("access_token")
    assert token, f"signup for {email} returned no access_token: {response.text[:400]}"
    with appclient.client(token) as session:
        yield email, session


def place_id(session: httpx.Client, name: str) -> int:
    response = session.get("/places", params={"q": name})
    assert response.status_code == 200, (
        f"place search for {name!r} did not answer 200: {describe(response)}")
    rows = response.json()
    assert isinstance(rows, list), (
        f"GET /api/places must return a top-level JSON array, got "
        f"{type(rows).__name__}: {response.text[:400]}")
    match = [row for row in rows if row.get("name") == name]
    assert match, (
        f"the seeded place {name!r} is not in the place index; "
        f"search returned {[row.get('name') for row in rows]}")
    return match[0]["id"]


def segments_by_name(session: httpx.Client) -> dict:
    response = session.get("/segments")
    assert response.status_code == 200, (
        f"GET /api/segments did not answer 200: {describe(response)}")
    rows = response.json()
    assert isinstance(rows, list), (
        f"GET /api/segments must return a top-level JSON array, got "
        f"{type(rows).__name__}: {response.text[:400]}")
    return {row.get("name"): row for row in rows}


def solve_route(session: httpx.Client, origin: int, destination: int,
                arrival_at: str) -> httpx.Response:
    return session.post("/routes", json={
        "origin_place_id": origin,
        "destination_place_id": destination,
        "arrival_at": arrival_at,
    })


def save_drive(session: httpx.Client, origin: int, destination: int,
               arrival_at: str) -> httpx.Response:
    return session.post("/drives", json={
        "origin_place_id": origin,
        "destination_place_id": destination,
        "arrival_at": arrival_at,
    })


def file_report(session: httpx.Client, segment: dict, report_type: str) -> httpx.Response:
    return session.post("/reports", json={
        "segment_id": segment["id"],
        "type": report_type,
        "latitude": segment.get("latitude", 28.459),
        "longitude": segment.get("longitude", 77.025),
    })


def expected_travel_minutes(segments: list) -> int:
    """The brief's arithmetic: scale each free flow time, round each up, then sum."""
    total = 0
    for segment in segments:
        base = int(segment["base_minutes"])
        factor = CONDITION_FACTOR[segment["severity"]]
        total += -((-base * factor) // 100)
    return total
