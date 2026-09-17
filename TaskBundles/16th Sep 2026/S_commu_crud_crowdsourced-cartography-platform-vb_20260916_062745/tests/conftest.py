"""Task fixtures for deku/crowdsourced-cartography-platform-vb.

Two rules govern this file. It is implementation agnostic: nothing here assumes
the agent's framework, file layout, ORM or module names, only the App Contract
and what instruction.md pinned. It is provider agnostic: every domain helper is
composed from the generic Backend primitives in capabilities.py, never from a
provider SDK.
"""

from __future__ import annotations

import os
import time
from typing import Any

import pytest
from appclient import api_base, client, login, seeded_password
from capabilities import Backend, make_backend

SEEDED_PASSWORD = "deku-demo-pw-2026"

MAPPER_EMAIL = "mapper@example.com"
MAPPER2_EMAIL = "mapper2@example.com"
MAPPER3_EMAIL = "mapper3@example.com"

MAPPER_NAME = "Ada Fenwick"
MAPPER2_NAME = "Bo Larsen"
MAPPER3_NAME = "Cleo Nkemdirim"

SEEDED_CAFE_NAME = "Riverside Cafe"
SEEDED_CAFE_TAG = "amenity=cafe"
SEEDED_MILL_NAME = "Old Mill"
SEEDED_MILL_TAG = "historic=mill"
SEEDED_ROAD_NAME = "Kingsway"
SEEDED_ROAD_TAG = "highway=residential"
SEEDED_BUILDING_NAME = "Market Hall"
SEEDED_BUILDING_TAG = "building=yes"
SEEDED_BUS_ROUTE_NAME = "Route 12"
SEEDED_BUS_ROUTE_TAG = "route=bus"
SEEDED_CYCLE_ROUTE_NAME = "Thames Cycle Way"
SEEDED_CYCLE_ROUTE_TAG = "route=bicycle"

SEEDED_CHANGESET_COMMENTS = (
    "Initial survey of the town centre",
    "Added Market Hall outline",
    "Tagged the cycle route",
)
SEEDED_DIARY_TITLES = (
    "Mapping the towpath after the flood",
    "Three weeks of building outlines",
    "Why I started mapping",
)

CAFE_NODE_ID = 1
MILL_NODE_ID = 2
ROAD_VERTEX_NODE_ID = 3
ROAD_WAY_ID = 1
BUILDING_WAY_ID = 2
BUS_ROUTE_RELATION_ID = 1
CYCLE_ROUTE_RELATION_ID = 2

CHANGESET_ELEMENT_CEILING = 500
BBOX_AREA_CAP = 0.25
BBOX_ELEMENT_CAP = 5000
TILE_EDGE_PX = 256
DEEPEST_ZOOM = 19
DIARY_PAGE_SIZE = 10

SEED_BBOX = "-0.1300,51.4980,-0.1200,51.5020"
OVERSIZED_BBOX = "-1.0000,50.0000,1.0000,52.0000"

SETTLE_SECONDS = 0.25
POLL_DEADLINE_SECONDS = 20.0

OK = (200, 201)
DENIED = (401, 403)
REFUSED = (400, 409, 422)
CONFLICT = (409,)


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned sleep. Every bounded poll routes its wait through here."""
    time.sleep(seconds)


def unique_suffix() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def poll_until(predicate, deadline_seconds: float = POLL_DEADLINE_SECONDS):
    """Poll a predicate to a monotonic deadline, returning its last truthy value."""
    deadline = time.monotonic() + deadline_seconds
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    return last


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def mapper_token() -> str:
    return login(MAPPER_EMAIL, seeded_password("SEED_MAPPER_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def mapper_client(mapper_token: str):
    with client(mapper_token) as c:
        yield c


@pytest.fixture(scope="session")
def mapper2_token() -> str:
    return login(MAPPER2_EMAIL, seeded_password("SEED_MAPPER2_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def mapper2_client(mapper2_token: str):
    with client(mapper2_token) as c:
        yield c


@pytest.fixture(scope="session")
def mapper3_client():
    token = login(MAPPER3_EMAIL, seeded_password("SEED_MAPPER3_PASSWORD", SEEDED_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


class MapStore:
    """Domain queries for this task, composed from the capability primitives."""

    def __init__(self, b: Backend) -> None:
        self._b = b

    def element_versions(self, table: str, element_id: int) -> list[dict]:
        return self._b.rows(table, id=element_id)

    def version_count(self, table: str, element_id: int) -> int:
        return self._b.count(table, id=element_id)

    def latest_version(self, table: str, element_id: int) -> int:
        versions = [int(r["version"]) for r in self.element_versions(table, element_id)]
        return max(versions) if versions else 0

    def row_at_version(self, table: str, element_id: int, version: int) -> dict | None:
        return self._b.one(table, id=element_id, version=version)

    def is_visible(self, table: str, element_id: int) -> bool:
        version = self.latest_version(table, element_id)
        row = self.row_at_version(table, element_id, version)
        return bool(row and row.get("visible"))

    def tags_at(self, element_type: str, element_id: int, version: int) -> dict:
        rows = self._b.rows(
            "tags",
            element_type=element_type,
            element_id=element_id,
            element_version=version,
        )
        return {r["key"]: r["value"] for r in rows}

    def relations_referencing(self, member_type: str, member_id: int) -> list[int]:
        rows = self._b.rows(
            "relation_members", member_type=member_type, member_id=member_id
        )
        return sorted({int(r["relation_id"]) for r in rows})

    def changeset_count(self) -> int:
        return self._b.count("changesets")

    def changeset(self, changeset_id: int) -> dict | None:
        return self._b.one("changesets", id=changeset_id)

    def mapper_by_email(self, email: str) -> dict | None:
        return self._b.one("mappers", email=email)

    def count_rows(self, table: str, **where: Any) -> int:
        return self._b.count(table, **where)


@pytest.fixture(scope="session")
def store(backend: Backend) -> MapStore:
    return MapStore(backend)


def open_changeset(c, comment: str) -> int:
    response = c.put("/changeset/create", json={"comment": comment})
    assert response.status_code in OK, (
        f"opening a changeset returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    changeset_id = body.get("id") if isinstance(body, dict) else None
    assert changeset_id is not None, (
        f"changeset create response carries no id: {response.text[:400]}"
    )
    return changeset_id


def upload(c, changeset_id: int, payload: dict):
    return c.post(f"/changeset/{changeset_id}/upload", json=payload)


def close_changeset(c, changeset_id: int):
    return c.put(f"/changeset/{changeset_id}/close")


def modify_node(node_id: int, version: int, **fields: Any) -> dict:
    element = {"id": node_id, "version": version}
    element.update(fields)
    return {"modify": {"nodes": [element]}}


def read_node(c, node_id: int) -> dict:
    response = c.get(f"/node/{node_id}")
    assert response.status_code in OK, (
        f"reading node {node_id} returned {response.status_code}: {response.text[:400]}"
    )
    return response.json()


def app_page_url(path: str) -> str:
    return f"{api_base().rsplit('/api', 1)[0]}{path}"
