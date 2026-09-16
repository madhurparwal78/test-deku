"""Task fixtures for deku/constellation-drawing-canvas-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout
or module names. The only assumptions are the App Contract and the literals
instruction.md pins explicitly.

Provider agnostic: domain helpers are composed from the generic primitives in
capabilities.py, never from a provider SDK.
"""

from __future__ import annotations

import os
import time

import pytest
from appclient import api_base, client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

STARGAZER_EMAIL = "stargazer@example.com"
OTHER_STARGAZER_EMAIL = "stargazer2@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"

CATALOGUE_ROWS = 10000
BRIGHT_BOUND = 2.00
BRIGHT_BOUND_ROWS = 4412
WALK_BOUND = -1.00
WALK_BOUND_ROWS = 641
FAINTEST_MAGNITUDE = 6.49
BRIGHTEST_MAGNITUDE = -1.50

WORKED_STAR_ID = "HD00800"
WORKED_STAR_RA = 206.400
WORKED_STAR_DEC = -10.000
WORKED_STAR_MAGNITUDE = -1.50

PICK_RA = 257.448
PICK_DEC = -16.600
PICK_RADIUS = 2.0
PICK_BRIGHTEST = "HD08034"
PICK_NEAREST = "HD05306"

TIE_RA = 243.708
TIE_DEC = 88.900
TIE_RADIUS = 1.5
TIE_WINNER = "HD02633"
TIE_RUNNER_UP = "HD09833"

EMPTY_RA = 258.000
EMPTY_DEC = 15.000
EMPTY_RADIUS = 1.0

SEAM_RA = 359.000
SEAM_DEC = -60.000
SEAM_RADIUS = 2.0
SEAM_WINNER = "HD09205"

POLE_RA = 240.000
POLE_DEC = -85.000
POLE_RADIUS = 2.0
POLE_WINNER = "HD00117"

SEGMENT_FROM = "HD00042"
SEGMENT_TO = "HD01600"
UNKNOWN_STAR_ID = "HD99999"
BURST_PAIRS = [(f"HD{i:05d}", f"HD{i + 1:05d}") for i in range(1, 13)]

SKY_MONOCEROS = "Monoceros Arch"
SKY_LANTERN = "Lepus Lantern"
SKY_KITE = "The Kite"
SKY_HEXAGON = "Winter Hexagon"
SKY_CORVUS = "Corvus Sketch"
SEEDED_SKY_COUNT = 4
LANTERN_SEGMENTS = 3
LANTERN_COLOUR = "y"
SEEDED_SHARE_TOKEN = "lantern-7f3a91"

MAX_NAME_LENGTH = 80
PAGE_LIMIT_MAX = 500
DECOY_FIELD = "observer_note"
RENDER_CONTENT_TYPE = "image/svg+xml"

CLIENT_ERRORS = (400, 401, 403, 404, 409, 410, 422)
DENIALS = (401, 403, 404)


def unique(prefix: str) -> str:
    return f"{prefix}-{os.urandom(6).hex()}"


def settle(seconds: float = 1.0) -> None:
    """The one sanctioned pause, for a side effect that lands out of band."""
    time.sleep(seconds)


def _password(var: str) -> str:
    return seeded_password(var, SEEDED_PASSWORD)


def _signed_in(email: str, var: str):
    return client(login(email, _password(var)))


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def owner_client():
    with _signed_in(STARGAZER_EMAIL, "SEED_STARGAZER_PASSWORD") as c:
        yield c


@pytest.fixture(scope="session")
def other_client():
    with _signed_in(OTHER_STARGAZER_EMAIL, "SEED_STARGAZER2_PASSWORD") as c:
        yield c


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def store() -> ObjectStore:
    return make_store()


@pytest.fixture(scope="session")
def api() -> str:
    return api_base()


def rows_of(payload):
    """The list envelope instruction.md pins: rows live under `items`."""
    if isinstance(payload, dict) and "items" in payload:
        return payload["items"]
    return payload


def collection_page(c, limit: int, cursor: str | None = None) -> dict:
    params = {"limit": limit}
    if cursor is not None:
        params["cursor"] = cursor
    response = c.get("/skies", params=params)
    assert response.status_code == 200, (
        f"GET /api/skies limit={limit} cursor={cursor!r} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    return response.json()


def stars_page(c, limit: int, cursor: str | None = None,
               max_magnitude: float | None = None) -> dict:
    params = {"limit": limit}
    if cursor is not None:
        params["cursor"] = cursor
    if max_magnitude is not None:
        params["max_magnitude"] = max_magnitude
    response = c.get("/stars", params=params)
    assert response.status_code == 200, (
        f"GET /api/stars limit={limit} max_magnitude={max_magnitude} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    return response.json()


def sky_named(c, name: str) -> dict | None:
    cursor, seen = None, []
    for _ in range(50):
        page = collection_page(c, PAGE_LIMIT_MAX, cursor)
        seen.extend(rows_of(page))
        if not page.get("has_more"):
            break
        cursor = page.get("next_cursor")
        if cursor is None:
            break
    for row in seen:
        if row.get("name") == name:
            return row
    return None


def require_sky(c, name: str) -> dict:
    found = sky_named(c, name)
    assert found is not None, (
        f"the seeded sky {name!r} is not reachable in this stargazer's collection"
    )
    return found


def create_sky(c, name: str, colour: str = "g") -> dict:
    response = c.post("/skies", json={"name": name, "line_colour": colour})
    assert response.status_code in (200, 201), (
        f"POST /api/skies {name!r} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    return response.json()


def add_segment(c, sky_id, from_star: str, to_star: str):
    return c.post(
        f"/skies/{sky_id}/segments",
        json={"from_star_id": from_star, "to_star_id": to_star},
    )


def read_sky(c, sky_id) -> dict:
    response = c.get(f"/skies/{sky_id}")
    assert response.status_code == 200, (
        f"GET /api/skies/{sky_id} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    return response.json()


def publish(c, sky_id, share_key: str, **extra):
    body = {
        "share_key": share_key,
        "view_ra_deg": 90.000,
        "view_dec_deg": 0.000,
        "view_zoom": 1.0,
    }
    body.update(extra)
    return c.post(f"/skies/{sky_id}/publish", json=body)


def render(c, sky_id):
    return c.post(f"/skies/{sky_id}/renders")
