from __future__ import annotations

import hashlib
import os
import time

import pytest
from _shapes import items
from appclient import api_base, app_url, client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

OWNER_EMAIL = "owner@example.com"
SEEDED_PASSWORD_DEFAULT = "deku-demo-pw-2026"

PUBLISHED_SLUGS = ("lantern-run", "paper-tide", "copper-garden")
DRAFT_SLUG = "night-ferry"
DRAFT_TITLE = "Night Ferry"

CONFLICT_ERROR = "coordinates_occupied"
CONFLICT_MESSAGE = "Another published project already stands at those coordinates."
POSTER_ERROR = "poster_required"

OBJECT_KEY_PREFIX = "projects/"
OBJECT_KEY_MIDDLE = "/posters/"

DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
CREATED = (200, 201)
CONFLICT = (409, 422, 400)

SETTLE_SECONDS = 2.0
POLL_BUDGET_SECONDS = 30.0

PNG_HEADER = b"\x89PNG\r\n\x1a\n"


def settle() -> None:
    """The only sanctioned sleep in this suite."""
    time.sleep(SETTLE_SECONDS)


def deadline(seconds: float = POLL_BUDGET_SECONDS) -> float:
    return time.monotonic() + seconds


def png_bytes(marker: str) -> bytes:
    """A small deterministic-per-call byte string that reads as a PNG."""
    return PNG_HEADER + marker.encode("utf-8") + b"\x00" * 16


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def probe_suffix() -> str:
    return os.urandom(6).hex()


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture
def owner_token() -> str:
    return login(
        OWNER_EMAIL, seeded_password("SEED_OWNER_PASSWORD", SEEDED_PASSWORD_DEFAULT)
    )


@pytest.fixture
def owner_client(owner_token: str):
    with client(owner_token) as c:
        yield c


class PortfolioStore:
    """Domain queries for this task, composed from the generic primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def project_by_slug(self, slug: str) -> dict | None:
        return self._b.one("project", slug=slug)

    def count_projects_with_slug(self, slug: str) -> int:
        return self._b.count("project", slug=slug)

    def published_projects(self) -> list[dict]:
        return self._b.rows("project", limit=500, published=True)

    def count_published_at(self, x: int, y: int, z: int) -> int:
        return self._b.count("project", published=True, world_x=x, world_y=y, world_z=z)

    def images_for(self, project_id) -> list[dict]:
        return self._b.rows("project_image", limit=100, project_id=project_id)

    def count_whispers(self) -> int:
        return self._b.count("whisper")

    def count_laps(self) -> int:
        return self._b.count("lap")

    def count_page_views(self, route: str) -> int:
        return self._b.count("page_view", route=route)

    def owner_row(self) -> dict | None:
        return self._b.one("owner_account", email=OWNER_EMAIL)


@pytest.fixture(scope="session")
def db() -> PortfolioStore:
    return PortfolioStore(make_backend())


@pytest.fixture(scope="session")
def bucket() -> ObjectStore:
    return make_store()


def create_draft(owner_client, suffix: str, x: int, y: int, z: int) -> dict:
    """Write one project through the studio API and return the created body."""
    payload = {
        "slug": f"probe-{suffix}",
        "title": f"Probe {suffix}",
        "summary": "written by the verifier",
        "link": "https://example.com/probe",
        "world_x": x,
        "world_y": y,
        "world_z": z,
        "zone": "projects",
        "previous_slug": None,
        "next_slug": None,
    }
    response = owner_client.post("/studio/projects", json=payload)
    assert response.status_code in CREATED, (
        f"POST /api/studio/projects for {payload['slug']!r} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    assert isinstance(body, dict), (
        f"POST /api/studio/projects returned {type(body).__name__}, "
        f"expected the created project object: {response.text[:400]}"
    )
    return body


def project_id_of(body: dict):
    for key in ("id", "project_id"):
        if body.get(key) is not None:
            return body[key]
    raise AssertionError(f"created project carries no id field: {str(body)[:300]}")


def upload_poster(owner_client, project_id, payload: bytes) -> dict:
    response = owner_client.post(
        f"/studio/projects/{project_id}/images",
        files={"file": (f"poster-{sha256_hex(payload)[:8]}.png", payload, "image/png")},
        data={"alt_text": "a verifier poster"},
    )
    assert response.status_code in CREATED, (
        f"POST /api/studio/projects/{project_id}/images returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    assert isinstance(body, dict), (
        f"poster upload returned {type(body).__name__}, expected the created image "
        f"object: {response.text[:400]}"
    )
    return body


def publish(owner_client, project_id):
    return owner_client.post(f"/studio/projects/{project_id}/publish")


def unpublish(owner_client, project_id):
    return owner_client.post(f"/studio/projects/{project_id}/unpublish")


def world_manifest(anon_client) -> dict:
    response = anon_client.get("/world")
    assert response.status_code == 200, (
        f"GET /api/world returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    assert isinstance(body, dict), (
        f"GET /api/world returned {type(body).__name__}, expected an object carrying "
        f"projects and areas: {response.text[:400]}"
    )
    return body


def manifest_slugs(manifest: dict) -> set[str]:
    projects = manifest.get("projects")
    assert isinstance(projects, list), (
        f"GET /api/world carries no projects list: {str(manifest)[:300]}"
    )
    return {str(p.get("slug", "")) for p in projects}


def public_project_slugs(anon_client) -> list[str]:
    response = anon_client.get("/projects")
    assert response.status_code == 200, (
        f"GET /api/projects returned {response.status_code}: {response.text[:400]}"
    )
    return [str(p.get("slug", "")) for p in items(response.json())]


def poll_until(check, budget: float = POLL_BUDGET_SECONDS):
    """Bounded poll to a monotonic deadline. Returns the first truthy result."""
    stop = deadline(budget)
    last = None
    while time.monotonic() < stop:
        last = check()
        if last:
            return last
        settle()
    return last


def wait_for_object(store: ObjectStore, prefix: str, budget: float = POLL_BUDGET_SECONDS):
    return poll_until(lambda: store.list(prefix), budget)


def free_point(db: PortfolioStore, seed: int) -> tuple[int, int, int]:
    """A world point no published project holds."""
    x = 9000 + (seed % 900)
    y = 0
    z = 9000 + ((seed // 900) % 900)
    while db.count_published_at(x, y, z) > 0:
        x += 1
    return x, y, z


def occupied_point(db: PortfolioStore) -> tuple[int, int, int]:
    """The world point a seeded published project already holds."""
    rows = db.published_projects()
    assert rows, "no published project row exists, so the seed never ran"
    row = rows[0]
    return int(row["world_x"]), int(row["world_y"]), int(row["world_z"])


def page(path: str) -> str:
    return f"{app_url()}{path}"


def api(path: str) -> str:
    return f"{api_base()}{path}"
