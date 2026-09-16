"""Task fixtures for deku/immersive-experience-showcase-vb.

Nothing here assumes the agent's framework, file layout, ORM or module names.
The only assumptions are the App Contract and whatever instruction.md pinned
literally: the route set, the field names, the seeded accounts and password,
the seeded catalogue, the four record states, the preview token shape, the
content addressed key shape and the nineteen table names.
"""

from __future__ import annotations

import io
import os
import time

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

SETTLE_SECONDS = 2.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give an unwanted async side effect time to land before asserting absence."""
    time.sleep(seconds)


PRODUCER_EMAIL = "producer@example.com"
PRODUCER2_EMAIL = "producer2@example.com"
EDITOR_EMAIL = "editor@example.com"

STATE_DRAFT = "draft"
STATE_IN_REVIEW = "in_review"
STATE_PUBLISHED = "published"
STATE_UNPUBLISHED = "unpublished"
RECORD_STATES = (STATE_DRAFT, STATE_IN_REVIEW, STATE_PUBLISHED, STATE_UNPUBLISHED)

PROJECT_TYPES = ("Web Experience", "Corporate", "E-Shop")

DISCIPLINE_KEYS = ("Design", "Experience", "3D", "Tech", "Strategy",
                   "Branding", "E-shop", "Web3", "NFT", "Film")

REEL_PROJECT = "lambert-vitrine"
SECOND_REEL_PROJECT = "grale"
THIRD_REEL_PROJECT = "verrine-end-of-year-23"
HOME_REEL_ORDER = (REEL_PROJECT, SECOND_REEL_PROJECT, THIRD_REEL_PROJECT)
OFF_REEL_PROJECT = "aurel-vance-experience"

DRAFT_PROJECT = "marivella"
GATED_PROJECT = "oryx7"
UNPUBLISHED_SLUGS = (DRAFT_PROJECT, GATED_PROJECT)

SEEDED_PROJECT_ROWS = 18
SEEDED_PUBLISHED_PROJECTS = 16
SEEDED_DISCIPLINE_ROWS = 10
SEEDED_CHAPTER_ROWS = 6
SEEDED_ACCOUNT_ROWS = 3
SEEDED_MEDIA_ROWS = 4
SEEDED_REEL_SECTION_ROWS = 3
SEEDED_HOME_REEL_ROWS = 3
SEEDED_RETIRED_PATH_ROWS = 3

INDEX_OPENS = ("Arven", "Aurel Vance Experience", "Chastenay Belfort",
               "Faiseurs d'Ourcq", "Grale", "Halom")
INDEX_CLOSES = "Verrine Watchmaking Salon 24"

CHAPTER_SLUGS = ("where-we-started", "how-we-work", "what-we-refuse",
                 "the-people", "the-craft", "the-studio")

RETIRED_PATHS = {
    "/cases/lambert-vitrine": REEL_PROJECT,
    "/cases/vitrine": REEL_PROJECT,
    "/cases/grale": SECOND_REEL_PROJECT,
}

TOKEN_PREFIX = "prv_"
TOKEN_HEX_LENGTH = 32
WORKED_TOKEN = "prv_6d1f4a08c39b27e5d0a4f81c6b3e97d2"

MEDIA_STATES = ("uploaded", "deriving", "ready", "failed")
RENDITION_VARIANTS = ("placeholder", "xs", "sm", "md", "lg", "xl")
WORKED_RENDITION_KEY = "media/9f2ad0c4/medium.avif"
MASTER_KEY_TEMPLATE = "media/{content_hash}/master.{ext}"
RENDITION_KEY_TEMPLATE = "media/{content_hash}/{variant}.{ext}"

BLOCK_KINDS = ("hero", "text", "media", "split_media", "image_push")
SUBSCRIBER_STATES = ("pending", "confirmed", "unsubscribed", "bounced")
PUBLISH_OUTCOMES = ("succeeded", "failed", "partially applied")

STUDIO_MAILBOX = "studio@example.com"
LOGIN_FAILURE_WORDING = "Incorrect email or password"
MALFORMED_ADDRESS_WORDING = "Invalid email format"
EMPTY_INDEX_LINE = "Nothing published yet. Write to the studio."
NOT_FOUND_HEADLINE = "That page has moved on."

PUBLIC_ROUTES = (
    "/",
    "/projects",
    "/projects/lambert-vitrine",
    "/projects/aurel-vance-experience",
    "/projects/verrine-end-of-year-23",
    "/projects/grale",
    "/about-us",
    "/about-us/where-we-started",
    "/about-us/how-we-work",
    "/about-us/what-we-refuse",
    "/about-us/the-people",
    "/about-us/the-craft",
    "/about-us/the-studio",
    "/privacy",
)

CONSOLE_ROUTES = (
    "/console",
    "/console/projects/marivella",
    "/console/media",
    "/console/reel",
    "/console/publish-log",
)

SECURITY_HEADERS = (
    "strict-transport-security",
    "x-content-type-options",
    "referrer-policy",
    "cross-origin-opener-policy",
    "permissions-policy",
)

CREDENTIAL_MARKERS = (
    "deku-local-dev",
    "minio-root-3d81f7a2",
    "postgresql://",
    "DB_ADMIN_URL",
    "STORAGE_SECRET_KEY",
)


def app_origin() -> str:
    return os.environ["APP_PUBLIC_URL"].rstrip("/")


def console_password() -> str:
    return seeded_password("SEED_CONSOLE_PASSWORD", "deku-demo-pw-2026")


@pytest.fixture
def anon_client():
    with client() as c:
        yield c


@pytest.fixture
def producer_client():
    token = login(PRODUCER_EMAIL, console_password())
    with client(token) as c:
        yield c


@pytest.fixture
def second_producer_client():
    token = login(PRODUCER2_EMAIL, console_password())
    with client(token) as c:
        yield c


@pytest.fixture
def editor_client():
    token = login(EDITOR_EMAIL, console_password())
    with client(token) as c:
        yield c


class StudioStore:
    """Domain queries composed from the generic capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def count_projects(self, **where) -> int:
        return self._b.count("projects", **where)

    def project(self, slug: str) -> dict | None:
        return self._b.one("projects", slug=slug)

    def count_disciplines(self) -> int:
        return self._b.count("disciplines")

    def count_chapters(self) -> int:
        return self._b.count("chapters")

    def count_accounts(self) -> int:
        return self._b.count("accounts")

    def account(self, email: str) -> dict | None:
        return self._b.one("accounts", email=email)

    def count_media(self, **where) -> int:
        return self._b.count("media", **where)

    def media(self, content_hash: str) -> dict | None:
        return self._b.one("media", content_hash=content_hash)

    def renditions(self, media_id) -> list[dict]:
        return self._b.rows("media_renditions", media_id=media_id)

    def count_home_reel_entries(self) -> int:
        return self._b.count("home_reel_entries")

    def home_reel_entries(self) -> list[dict]:
        return self._b.rows("home_reel_entries")

    def count_reel_sections(self) -> int:
        return self._b.count("reel_sections")

    def count_retired_paths(self) -> int:
        return self._b.count("project_retired_paths")

    def preview_tokens(self, record_slug: str) -> list[dict]:
        return self._b.rows("preview_tokens", record_slug=record_slug)

    def count_publish_log(self, **where) -> int:
        return self._b.count("publish_log", **where)

    def publish_log_rows(self, **where) -> list[dict]:
        return self._b.rows("publish_log", **where)

    def subscriber(self, email_normalised: str) -> dict | None:
        return self._b.one("subscribers", email_normalised=email_normalised)

    def count_subscribers(self, **where) -> int:
        return self._b.count("subscribers", **where)

    def count_outbound_clicks(self, project_slug: str) -> int:
        return self._b.count("outbound_clicks", project_slug=project_slug)


@pytest.fixture(scope="session")
def db() -> StudioStore:
    return StudioStore(make_backend())


@pytest.fixture(scope="session")
def store() -> ObjectStore:
    """The object bucket, inspected out of band. Never through the app."""
    return make_store()


@pytest.fixture
def probe() -> str:
    """A per-run suffix so a rerun never collides with its own earlier rows."""
    return os.urandom(6).hex()


def probe_address(probe: str) -> str:
    return f"list-{probe}@example.com"


def probe_slug(probe: str) -> str:
    return f"probe-{probe}"


def png_bytes(seed: int = 0) -> bytes:
    """A tiny valid still, generated rather than shipped, unique per seed."""
    import struct
    import zlib

    width = height = 4
    raw = b"".join(
        b"\x00" + bytes(((x * 7 + y * 11 + seed) % 256, (seed * 3) % 256,
                         (x + y + seed) % 256) for x in range(width))
        for y in range(height)
    )

    def chunk(tag: bytes, body: bytes) -> bytes:
        return (struct.pack(">I", len(body)) + tag + body
                + struct.pack(">I", zlib.crc32(tag + body) & 0xFFFFFFFF))

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def upload_master(c, probe: str, seed: int = 0) -> dict:
    """Upload one generated master through the console and return the record."""
    payload = png_bytes(seed)
    response = c.post(
        "/console/media",
        files={"file": (f"probe-{probe}-{seed}.png", io.BytesIO(payload), "image/png")},
    )
    assert response.status_code in (200, 201), (
        f"POST /api/console/media returned {response.status_code}: {response.text[:400]}"
    )
    return response.json()


def wait_for_media_state(c, media_id, wanted: str, timeout: float = 60.0) -> dict:
    """Poll the media library to a monotonic deadline for a derivation outcome."""
    deadline = time.monotonic() + timeout
    latest: dict = {}
    while time.monotonic() < deadline:
        response = c.get("/console/media")
        assert response.status_code == 200, (
            f"GET /api/console/media returned {response.status_code}: "
            f"{response.text[:400]}"
        )
        for row in response.json():
            if str(row.get("id")) == str(media_id):
                latest = row
                if row.get("state") == wanted:
                    return row
        settle(1.0)
    raise AssertionError(
        f"media {media_id} never reached {wanted!r}; last seen {latest.get('state')!r}"
    )


def create_draft_project(c, probe: str, seed: int = 0) -> dict:
    """Create one draft case study owned by the calling session."""
    slug = f"{probe_slug(probe)}-{seed}"
    response = c.post("/console/projects", json={
        "title": f"Probe {probe} {seed}",
        "slug": slug,
        "type": PROJECT_TYPES[0],
        "description": "A probe record written by the grader.",
        "disciplines": [DISCIPLINE_KEYS[0]],
    })
    assert response.status_code in (200, 201), (
        f"POST /api/console/projects returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    return response.json()


def transition(c, slug: str, to_state: str):
    return c.post(f"/console/projects/{slug}/transition", json={"to_state": to_state})


def mint_preview_token(c, slug: str) -> str:
    response = c.post(f"/console/projects/{slug}/preview-tokens")
    assert response.status_code in (200, 201), (
        f"POST /api/console/projects/{slug}/preview-tokens returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    token = body.get("token") or body.get("preview_token") or body.get("value")
    assert isinstance(token, str) and token.startswith(TOKEN_PREFIX), (
        f"the minted preview token is returned once, as a string opening "
        f"{TOKEN_PREFIX!r}; got {body!r}"
    )
    return token
