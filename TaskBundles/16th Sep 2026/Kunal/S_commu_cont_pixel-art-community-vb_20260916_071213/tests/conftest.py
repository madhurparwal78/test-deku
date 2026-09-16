"""Task fixtures for deku/pixel-art-community-vb.

Two rules govern this file.

1. Implementation agnostic. Nothing here assumes the agent's framework, file
   layout, ORM or module names. The only assumptions are the App Contract (the
   app answers at APP_PUBLIC_URL, REST under /api) and whatever instruction.md
   pinned explicitly: the endpoint paths and bodies, the `access_token` login
   key, the seeded accounts and their password, the seeded pieces, the topic
   set, the table names and the object-key scheme.

2. Provider agnostic. The domain helpers are composed from the generic `Backend`
   and `ObjectStore` primitives in capabilities.py, never from a provider SDK.
   Swapping the storage slug replaces the adapter, not this file.
"""

from __future__ import annotations

import os
import time

import pytest
from _shapes import items
from appclient import client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"

AUTHOR_HANDLE = "nova"
AUTHOR2_HANDLE = "bram"
READER_HANDLE = "pilot"

PUBLIC_ANIMATED_PIECE = "Harbour Lights"
PUBLIC_STILL_PIECE = "Cat In A Window"
PRIVATE_PIECE = "Night Market Draft"
SECOND_AUTHOR_PIECE = "Valentine Robot"
UNLISTED_PIECE = "Ocean Study"

SEEDED_TOPICS = ("Cats", "Christmas", "People", "Technology", "Valentine", "Ocean")
SEEDED_PALETTES = ("Harbour Eight", "Night Sixteen")

MAX_TAGS = 10
MAX_COMMENT_CLUSTERS = 1000
THUMBNAIL_SIZES = (64, 128, 256, 512)

RESERVED_HANDLES = ("privacy", "terms", "search", "admin", "api", "draw")

SETTLE_SECONDS = 2.0
DEADLINE_SECONDS = 30.0


def settle() -> None:
    """The only sanctioned sleep in this bundle.

    A bounded wait before asserting a thing did NOT happen. Polling cannot prove
    absence: a poll that never finds the event cannot tell "did not happen" from
    "has not happened yet".
    """
    time.sleep(SETTLE_SECONDS)


def poll_until(predicate, what: str, deadline_seconds: float = DEADLINE_SECONDS):
    """Poll to a monotonic deadline, never a wall clock, and never a bare sleep."""
    end = time.monotonic() + deadline_seconds
    last = None
    while time.monotonic() < end:
        last = predicate()
        if last:
            return last
        settle()
    raise AssertionError(
        f"{what} was still not observed after {deadline_seconds:.0f}s; "
        f"last observation was {last!r}"
    )


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture
def author_token() -> str:
    return login(AUTHOR_EMAIL, seeded_password("SEED_AUTHOR_PASSWORD", "deku-demo-pw-2026"))


@pytest.fixture
def author_client(author_token: str):
    with client(author_token) as c:
        yield c


@pytest.fixture
def author2_client():
    token = login(AUTHOR2_EMAIL, seeded_password("SEED_AUTHOR2_PASSWORD", "deku-demo-pw-2026"))
    with client(token) as c:
        yield c


@pytest.fixture
def reader_client():
    token = login(READER_EMAIL, seeded_password("SEED_READER_PASSWORD", "deku-demo-pw-2026"))
    with client(token) as c:
        yield c


class GalleryStore:
    """Domain queries for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend


    def account_by_email(self, email: str) -> dict | None:
        return self._b.one("accounts", email=email)

    def account_by_handle(self, handle: str) -> dict | None:
        return self._b.one("accounts", handle=handle)

    def count_accounts(self, **where) -> int:
        return self._b.count("accounts", **where)


    def piece_by_title(self, title: str) -> dict | None:
        return self._b.one("pieces", title=title)

    def count_pieces(self, **where) -> int:
        return self._b.count("pieces", **where)

    def pieces_for_account(self, account_id) -> list[dict]:
        return self._b.rows("pieces", limit=200, account_id=account_id)

    def piece_columns(self) -> set[str]:
        rows = self._b.rows("pieces", limit=1)
        return set(rows[0].keys()) if rows else set()


    def count_likes(self, piece_id) -> int:
        return self._b.count("likes", piece_id=piece_id)

    def count_comments(self, piece_id) -> int:
        return self._b.count("comments", piece_id=piece_id)

    def count_follows(self, follower_id, followee_id) -> int:
        return self._b.count("follows", follower_id=follower_id, followee_id=followee_id)

    def notifications_for(self, recipient_id) -> list[dict]:
        return self._b.rows("notifications", limit=200, recipient_id=recipient_id)


@pytest.fixture(scope="session")
def db() -> GalleryStore:
    return GalleryStore(make_backend())


@pytest.fixture(scope="session")
def store() -> ObjectStore:
    return make_store()


@pytest.fixture
def probe_suffix() -> str:
    """A per-run identifier, so two identical runs never collide on a title."""
    return os.urandom(6).hex()


def tiny_artwork(seed: str) -> dict:
    """A deterministic one-frame document payload the publish endpoint accepts.

    The brief pins the document's own shape: whole-pixel dimensions, an indexed
    mode, a palette and a frame list. Nothing here names a file format, because
    the app owns the rendition it writes to the object store.
    """
    return {
        "width": 8,
        "height": 8,
        "mode": "indexed",
        "palette": [
            {"index": 0, "r": 0, "g": 0, "b": 0, "a": 0},
            {"index": 1, "r": 0, "g": 94, "b": 255, "a": 255},
            {"index": 2, "r": 56, "g": 193, "b": 114, "a": 255},
        ],
        "frames": [
            {
                "duration_ms": 200,
                "pixels": [(i + len(seed)) % 3 for i in range(64)],
            }
        ],
    }


def publish_payload(title: str, seed: str, **overrides) -> dict:
    body = {
        "title": title,
        "description": f"A probe piece published by the checks, run {seed}.",
        "tags": ["ocean"],
        "visibility": "public",
        "artwork": tiny_artwork(seed),
    }
    body.update(overrides)
    return body


def publish(http_client, title: str, seed: str, **overrides):
    """POST /api/pieces with an idempotency key, returning the response."""
    key = overrides.pop("idempotency_key", f"probe-{seed}")
    return http_client.post(
        "/pieces",
        json=publish_payload(title, seed, **overrides),
        headers={"Idempotency-Key": key},
    )


def created_piece(response) -> dict:
    assert response.status_code in (200, 201), (
        f"POST /api/pieces returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    piece = body.get("piece", body)
    assert isinstance(piece, dict) and piece.get("id") is not None, (
        f"POST /api/pieces returned no piece with an id: {response.text[:400]}"
    )
    return piece


def feed_titles(http_client, **params) -> list[str]:
    response = http_client.get("/pieces", params=params)
    assert response.status_code == 200, (
        f"GET /api/pieces {params} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    return [row.get("title") for row in items(response.json())]


def feed_page(http_client, **params) -> dict:
    response = http_client.get("/pieces", params=params)
    assert response.status_code == 200, (
        f"GET /api/pieces {params} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    payload = response.json()
    return payload if isinstance(payload, dict) else {"pieces": payload}
