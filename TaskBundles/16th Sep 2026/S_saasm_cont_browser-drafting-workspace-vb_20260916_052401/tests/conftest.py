from __future__ import annotations

import os
import time

import pytest

import appclient
import capabilities

SEEDED_PASSWORD = appclient.seeded_password("DEKU_SEED_PASSWORD", "deku-demo-pw-2026")

DRAFTER_EMAIL = "drafter@example.com"
SECOND_DRAFTER_EMAIL = "drafter2@example.com"
REVIEWER_EMAIL = "reviewer@example.com"

DRAFTER_NAME = "Mira Vance"
SECOND_DRAFTER_NAME = "Owen Blake"
REVIEWER_NAME = "Priya Raman"

UNSHARED_DRAWING = "Harbour Pavilion"
SHARED_DRAWING = "Rail Shed Section"
SECOND_OWNER_DRAWING = "Kiln House Elevation"
DENSE_DRAWING = "Site Survey Grid"
DENSE_ENTITIES = 20000
DENSE_LAYERS = 40

BASE_LAYER = "Base"
WALLS_LAYER = "Walls"
DIMENSIONS_LAYER = "Dimensions"
NOTES_LAYER = "Notes"
OUTLINE_LAYER = "Outline"
CENTERLINES_LAYER = "Centerlines"

ARCHITECTURAL_LAYERS = (BASE_LAYER, WALLS_LAYER, DIMENSIONS_LAYER, NOTES_LAYER)
MECHANICAL_LAYERS = (BASE_LAYER, OUTLINE_LAYER, CENTERLINES_LAYER, DIMENSIONS_LAYER)

DOCUMENT_TITLE = "Draftline Web App, Online CAD Editor and Viewer"
ASSISTANT_PANEL_TITLE = "Draft Assistant"

EXCHANGE_EXTENSION = ".dxe"
OBJECT_KEY_TEMPLATE = "drawings/{drawing_id}/v{version_number}/{byte_digest}.dxe"

PRIVACY_ROUTE = "/privacy"
TERMS_ROUTE = "/terms"
LOGIN_ROUTE = "/login"
SIGNUP_ROUTE = "/signup"
LIBRARY_ROUTE = "/drawings"
SITEMAP_ROUTE = "/sitemap.xml"
ROBOTS_ROUTE = "/robots.txt"
HEALTH_ENDPOINT = "/api/health"

PUBLIC_ROUTES = ("/", LOGIN_ROUTE, SIGNUP_ROUTE, PRIVACY_ROUTE, TERMS_ROUTE)

LINETYPES = ("continuous", "dashed", "center", "hidden")
UNITS = ("millimeters", "meters", "inches", "feet")
TEMPLATES = ("blank", "architectural", "mechanical")
ACCESS_LEVELS = ("view", "comment", "edit")
ROLE_DRAFTER = "drafter"
ROLE_REVIEWER = "reviewer"
LINEWEIGHT_BYLAYER = -1
COLOUR_BYLAYER = "BYLAYER"

OK = (200, 201)
DENIED = (401, 403, 404)
REFUSED = (400, 409, 422)

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


def page(path: str):
    import httpx

    return httpx.get(f"{app_url()}{path}", timeout=appclient.TIMEOUT,
                     follow_redirects=True)


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def drafter_token() -> str:
    return appclient.login(DRAFTER_EMAIL, SEEDED_PASSWORD)


@pytest.fixture(scope="session")
def second_drafter_token() -> str:
    return appclient.login(SECOND_DRAFTER_EMAIL, SEEDED_PASSWORD)


@pytest.fixture(scope="session")
def reviewer_token() -> str:
    return appclient.login(REVIEWER_EMAIL, SEEDED_PASSWORD)


@pytest.fixture
def drafter(drafter_token):
    with appclient.client(drafter_token) as c:
        yield c


@pytest.fixture
def second_drafter(second_drafter_token):
    with appclient.client(second_drafter_token) as c:
        yield c


@pytest.fixture
def reviewer(reviewer_token):
    with appclient.client(reviewer_token) as c:
        yield c


@pytest.fixture
def anonymous():
    with appclient.client() as c:
        yield c


def drawings_of(client) -> list[dict]:
    import _shapes

    response = client.get("/drawings")
    assert response.status_code in OK, (
        f"GET /api/drawings returned {response.status_code}: {body(response)}"
    )
    return _shapes.items(response.json())


def find_drawing(client, name: str) -> dict | None:
    for row in drawings_of(client):
        if str(row.get("name", "")).strip() == name:
            return row
    return None


def require_drawing(client, name: str) -> dict:
    found = find_drawing(client, name)
    assert found is not None, (
        f"seeded drawing {name!r} is not in GET /api/drawings for this account; "
        f"the library returned {[r.get('name') for r in drawings_of(client)]}"
    )
    return found


def layers_of(client, drawing_id) -> list[dict]:
    import _shapes

    response = client.get(f"/drawings/{drawing_id}/layers")
    assert response.status_code in OK, (
        f"GET /api/drawings/{drawing_id}/layers returned {response.status_code}: "
        f"{body(response)}"
    )
    return _shapes.items(response.json())


def entities_of(client, drawing_id) -> list[dict]:
    import _shapes

    response = client.get(f"/drawings/{drawing_id}/entities")
    assert response.status_code in OK, (
        f"GET /api/drawings/{drawing_id}/entities returned {response.status_code}: "
        f"{body(response)}"
    )
    return _shapes.items(response.json())


def versions_of(client, drawing_id) -> list[dict]:
    import _shapes

    response = client.get(f"/drawings/{drawing_id}/versions")
    assert response.status_code in OK, (
        f"GET /api/drawings/{drawing_id}/versions returned {response.status_code}: "
        f"{body(response)}"
    )
    return _shapes.items(response.json())


def layer_named(client, drawing_id, name: str) -> dict | None:
    for row in layers_of(client, drawing_id):
        if str(row.get("name", "")).strip().lower() == name.lower():
            return row
    return None


def new_layer(client, drawing_id, name: str, colour_index: int = 3):
    return client.post(
        f"/drawings/{drawing_id}/layers",
        json={"name": name, "color_index": colour_index,
              "linetype": "continuous", "lineweight": LINEWEIGHT_BYLAYER,
              "description": "probe layer"},
    )


def new_line(client, drawing_id, layer_id, start, end, colour_index=None):
    return client.post(
        f"/drawings/{drawing_id}/entities",
        json={"layer_id": layer_id, "kind": "line",
              "points": [{"x": start[0], "y": start[1]},
                         {"x": end[0], "y": end[1]}],
              "color_index": colour_index, "linetype": "continuous",
              "lineweight": LINEWEIGHT_BYLAYER, "properties": {}},
    )


def new_drawing(client, name: str, units: str = "millimeters",
                template: str = "architectural"):
    return client.post("/drawings",
                       json={"name": name, "units": units, "template": template})


def save_version(client, drawing_id, base_version, label=None):
    return client.post(f"/drawings/{drawing_id}/versions",
                       json={"base_version": base_version, "label": label})


def highest_version(client, drawing_id) -> int:
    rows = versions_of(client, drawing_id)
    numbers = [int(r["number"]) for r in rows if r.get("number") is not None]
    return max(numbers) if numbers else 0
