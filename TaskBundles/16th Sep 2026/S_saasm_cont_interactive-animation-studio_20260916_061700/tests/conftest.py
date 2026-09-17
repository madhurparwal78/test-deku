"""Task fixtures for deku/interactive-animation-studio.

Two rules govern this file. Nothing here assumes the agent's framework, file
layout, ORM or module names: the only assumptions are the App Contract and what
instruction.md pinned literally. And nothing here reaches a provider SDK; the
domain helpers are composed from the generic primitives in capabilities.py, so
swapping a slot's provider replaces the adapter rather than this file.
"""

from __future__ import annotations

import os
import time
import uuid

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

EDITOR_EMAIL = "editor@example.com"
EDITOR2_EMAIL = "editor2@example.com"
EDITOR3_EMAIL = "editor3@example.com"
VIEWER_EMAIL = "viewer@example.com"
CORPUS_PASSWORD = "deku-demo-pw-2026"

WORKSPACE_NAME = "Northlight Studio"
WORKSPACE_SLUG = "northlight"
SEAT_CAP = 3

FOLDER_PRODUCT_UI = "Product UI"
FOLDER_GAME_UI = "Game UI"
FOLDER_BROADCAST = "Broadcast"

DOC_PUBLISHED = "Loader Ring"
DOC_DRAFT = "Menu Transition"
DOC_SECOND = "Match Ticker"

CHANNEL_PUBLISHED = "loader-ring"
CHANNEL_SECOND = "match-ticker"

HANDLE_RAE = "rae"
HANDLE_TOMAS = "tomas"

LIKES_LOADER_RING = 23
LIKES_MATCH_TICKER = 623

PAGE_SIZE = 24
CURSOR_HEADER = "X-Next-Cursor"

REVISION_KEY_PREFIX = "documents/"
POSTER_KEY_PREFIX = "posters/"
DOCUMENT_KEY_SUFFIX = ".mot"
POSTER_KEY_SUFFIX = ".svg"

OK = (200, 201)
DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
REFUSED = (400, 403, 409, 422)

SETTLE_SECONDS = 3.0
POLL_SECONDS = 20.0
CACHE_INTERVAL_SECONDS = 10.0


def settle() -> None:
    """The one sanctioned sleep: a bounded wait before asserting a non-event."""
    time.sleep(SETTLE_SECONDS)


def unique_suffix() -> str:
    return uuid.uuid4().hex[:10]


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def probe_handle() -> str:
    return f"probe{unique_suffix()}"


def poll_until(predicate, timeout: float = POLL_SECONDS):
    """Poll a predicate to a monotonic deadline. Returns the truthy value or None."""
    deadline = time.monotonic() + timeout
    while True:
        value = predicate()
        if value:
            return value
        if time.monotonic() >= deadline:
            return None
        settle()


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture()
def editor_client():
    token = login(EDITOR_EMAIL, seeded_password("SEED_EDITOR_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def editor2_client():
    token = login(EDITOR2_EMAIL, seeded_password("SEED_EDITOR2_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def viewer_client():
    token = login(VIEWER_EMAIL, seeded_password("SEED_VIEWER_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


class StudioStore:
    """Domain queries for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def member_by_email(self, email: str) -> dict | None:
        return self._b.one("member", email=email)

    def count_members(self, **where) -> int:
        return self._b.count("member", **where)

    def count_grants(self, **where) -> int:
        return self._b.count("grant", **where)

    def seats_used(self) -> int:
        rows = self._b.rows("grant", role="editor")
        holders = set()
        for row in rows:
            if row.get("deny"):
                continue
            member = self._b.one("member", id=row.get("member_id"))
            if member and member.get("status") == "active":
                holders.add(member["id"])
        return len(holders)

    def invitation_by_email(self, email: str) -> dict | None:
        return self._b.one("invitation", email=email)

    def folder_by_name(self, name: str) -> dict | None:
        return self._b.one("folder", name=name)

    def document_by_name(self, name: str) -> dict | None:
        return self._b.one("document", name=name)

    def count_documents(self, **where) -> int:
        return self._b.count("document", **where)

    def revisions_for(self, document_id) -> list[dict]:
        return self._b.rows("revision", document_id=document_id)

    def count_revisions(self, document_id) -> int:
        return self._b.count("revision", document_id=document_id)

    def revision_parents(self, revision_id) -> list[dict]:
        return self._b.rows("revision_parent", revision_id=revision_id)

    def operations_for(self, document_id) -> list[dict]:
        return self._b.rows("operation", document_id=document_id)

    def count_operations(self, document_id, **where) -> int:
        return self._b.count("operation", document_id=document_id, **where)

    def builds_for(self, document_id) -> list[dict]:
        return self._b.rows("build", document_id=document_id)

    def count_builds(self, document_id) -> int:
        return self._b.count("build", document_id=document_id)

    def channel_by_slug(self, slug: str) -> dict | None:
        return self._b.one("channel", slug=slug)

    def listing_by_slug(self, slug: str) -> dict | None:
        return self._b.one("listing", slug=slug)

    def count_listings(self, **where) -> int:
        return self._b.count("listing", **where)

    def count_listing_likes(self, listing_id) -> int:
        return self._b.count("listing_like", listing_id=listing_id)


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def studio(backend: Backend) -> StudioStore:
    return StudioStore(backend)


@pytest.fixture(scope="session")
def store() -> ObjectStore:
    return make_store()


def revision_keys(store: ObjectStore, document_id) -> list[str]:
    return [k for k in store.list(f"{REVISION_KEY_PREFIX}{document_id}/")
            if k.endswith(DOCUMENT_KEY_SUFFIX)]


def poster_keys(store: ObjectStore, build_id) -> list[str]:
    return [k for k in store.list(f"{POSTER_KEY_PREFIX}{build_id}/")
            if k.endswith(POSTER_KEY_SUFFIX)]


def api(path: str) -> str:
    return f"/api{path}"


def json_body(response):
    return response.json()


def new_operation(target: str, prop: str, value):
    return {"op_id": str(uuid.uuid4()), "target": target, "property": prop, "value": value}


def seed_document_id(studio: StudioStore, name: str):
    row = studio.document_by_name(name)
    assert row is not None, f"seed document {name!r} is missing from the document table"
    return row["id"]
