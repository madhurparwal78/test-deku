"""Task fixtures for deku/metered-mesh-generator-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout
or module names. The only assumptions are the App Contract and what
instruction.md pinned explicitly, which is the endpoint set, the seeded
accounts, the stored tier table, the three plans and the published figures.

Provider agnostic: the datastore and the object store are reached through the
generic Backend and ObjectStore primitives in capabilities.py, never through a
provider SDK, so swapping postgres or minio replaces an adapter rather than this
file.
"""

from __future__ import annotations

import os
import time
import uuid

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

CREATOR_EMAIL = "creator@example.com"
CREATOR2_EMAIL = "creator2@example.com"
CREATOR3_EMAIL = "creator3@example.com"
SEED_PASSWORD = "deku-demo-pw-2026"

TIERS = {
    "fast": {"octree": 196, "steps": 20, "polygons": 15000, "credits": 2},
    "standard": {"octree": 256, "steps": 30, "polygons": 30000, "credits": 5},
    "pro": {"octree": 384, "steps": 40, "polygons": 60000, "credits": 10},
    "ultra": {"octree": 512, "steps": 50, "polygons": 300000, "credits": 20},
}
POLYGON_CEILING = 300000
TEXTURE_SURCHARGE = 5
MULTI_IMAGE_SURCHARGE = 10

PLAN_KEYS = ("free", "pro", "max")
PLAN_MONTHLY_CREDITS = {"free": 10, "pro": 1000, "max": 4000}
PLAN_WELCOME_CREDITS = {"free": 5}
PLAN_RETENTION_DAYS = {"free": 7, "pro": 180}
PLAN_LICENCE = {"free": "CC-BY-4.0", "pro": "customer-owned", "max": "customer-owned"}
PLAN_QUEUE = {"free": "limited", "pro": "standard", "max": "higher"}
PROMOTION_START = "2026-09-01"
PROMOTION_END = "2026-12-31"

JOB_STATES = ("queued", "processing", "completed", "failed")
TERMINAL_STATES = {"completed", "failed"}
REPRESENTATION_KINDS = ("glb", "obj", "stl", "texture-map", "preview")
DOWNLOAD_KINDS = ("glb", "obj", "stl")
ACCEPTED_SOURCE_FORMATS = ("JPG", "PNG", "WEBP")

SAMPLE_KEYS = ("sneaker", "mug", "chair", "plant")
GALLERY_ITEMS = {
    "Brass Compass": "pro",
    "Woven Basket": "standard",
    "Carved Owl": "ultra",
    "Tin Robot": "fast",
}
PUBLISHED_CLAIM_KEYS = (
    "models_created",
    "average_rating",
    "success_rate",
    "countries_served",
    "average_cost_usd",
    "conversion_minutes",
)
SUCCESS_RATE_VALUE = "99.0"
CONVERTER_PAIR_COUNT = 128
VIEWER_FORMAT_COUNT = 15
ANONYMOUS_ALLOWANCE = 1
CLAIM_WINDOW_HOURS = 24

SETTLE_SECONDS = 2.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned sleep, for an absence that cannot be polled."""
    time.sleep(seconds)


def generation_seconds() -> float:
    """The verifier binds GENERATION_SECONDS low; the app reads the same variable
    at its production value from task.toml. Hardcoding the wait is a J.9 breach."""
    return float(os.getenv("GENERATION_SECONDS", "150"))


def job_deadline() -> float:
    return (3.0 * generation_seconds()) + (4.0 * SETTLE_SECONDS)


def wait_for_job_state(getter, target: set[str], timeout: float | None = None):
    """Poll one job until its state lands in target. Settlement is asynchronous,
    so asserting immediately after submission is a race the substep would lose.
    Returns rather than raises, so the caller reports what it actually saw."""
    limit = timeout if timeout is not None else job_deadline()
    deadline = time.monotonic() + limit
    latest = None
    while time.monotonic() < deadline:
        latest = getter()
        if latest is not None and latest.get("state") in target:
            return latest
        settle(0.5)
    return latest


def unique_key() -> str:
    return f"grader-{uuid.uuid4().hex}"


def submit_job(http, tier: str = "pro", textures: bool = False,
               input_mode: str = "single-image", source_mode: str = "image-to-3d",
               idempotency_key: str | None = None, sample: str | None = None):
    payload = {
        "source_mode": source_mode,
        "input_mode": input_mode,
        "tier": tier,
        "textures": textures,
        "idempotency_key": idempotency_key or unique_key(),
    }
    if sample is not None:
        payload["sample"] = sample
    return http.post("/jobs", json=payload)


def expected_cost(tier: str, textures: bool = False,
                  input_mode: str = "single-image") -> int:
    cost = TIERS[tier]["credits"]
    if textures:
        cost += TEXTURE_SURCHARGE
    if input_mode == "multiple-images":
        cost += MULTI_IMAGE_SURCHARGE
    return cost


def balance_of(http) -> int:
    response = http.get("/session")
    assert response.status_code == 200, (
        f"GET /api/session returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    for key in ("balance", "credits", "credit_balance"):
        if isinstance(body.get(key), int):
            return body[key]
        nested = body.get("account") or {}
        if isinstance(nested, dict) and isinstance(nested.get(key), int):
            return nested[key]
    raise AssertionError(
        f"GET /api/session carries no integer credit balance: {response.text[:400]}"
    )


def completed_asset(http, tier: str = "pro"):
    response = submit_job(http, tier=tier)
    assert response.status_code in (200, 201, 202), (
        f"POST /api/jobs returned {response.status_code}: {response.text[:400]}"
    )
    job_id = response.json().get("id") or response.json().get("job_id")
    assert job_id, f"POST /api/jobs returned no job id: {response.text[:400]}"

    def read():
        got = http.get(f"/jobs/{job_id}")
        return got.json() if got.status_code == 200 else None

    final = wait_for_job_state(read, {"completed"})
    assert final is not None and final.get("state") == "completed", (
        f"job {job_id} did not reach completed within {job_deadline():.0f}s, "
        f"last state was {final.get('state') if final else None!r}"
    )
    asset_id = final.get("asset_id") or (final.get("asset") or {}).get("id")
    assert asset_id, f"completed job {job_id} names no asset: {final}"
    return job_id, asset_id


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


def _authed(email: str, env_var: str):
    token = login(email, seeded_password(env_var, SEED_PASSWORD))
    return client(token)


@pytest.fixture(scope="session")
def creator_client():
    with _authed(CREATOR_EMAIL, "SEED_CREATOR_PASSWORD") as c:
        yield c


@pytest.fixture(scope="session")
def creator2_client():
    with _authed(CREATOR2_EMAIL, "SEED_CREATOR2_PASSWORD") as c:
        yield c


@pytest.fixture(scope="session")
def creator3_client():
    with _authed(CREATOR3_EMAIL, "SEED_CREATOR3_PASSWORD") as c:
        yield c


@pytest.fixture(scope="session")
def db() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def store() -> ObjectStore:
    return make_store()
