from __future__ import annotations

import hashlib
import os
import time

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"
SEED_PASSWORD = "deku-demo-pw-2026"

LOGIN_ROUTE = "/api/auth/login"
SIGNUP_ROUTE = "/api/auth/signup"

PUBLISHED_SLUGS = ("home", "ai", "top")
DRAFT_SLUG = "field-guide"

STATE_DRAFT = "draft"
STATE_PUBLISHED = "published"

BLOCK_KINDS = (
    "hero",
    "value_line",
    "feature_card",
    "color_panel",
    "community",
    "testimonial",
    "use_cases",
    "cta",
)

TOP_NINE = (
    ("d3-gallery", 1000),
    ("inputs", 991),
    ("learn-d3-introduction", 755),
    ("datalume-and-creative-coding", 603),
    ("zoomable-sunburst", 511),
    ("datalume-plot", 450),
    ("force-directed-graph-component", 418),
    ("enigma-machine", 417),
    ("collapsible-tree", 399),
)
FORKED_SLUG = "zoomable-sunburst"
PAGE_SIZE = 30
SEEDED_NOTEBOOK_COUNT = 33

PUBLIC_ROUTES = ("/", "/ai", "/top", "/new", "/terms-of-service")


def settle(seconds: float = 2.0) -> None:
    time.sleep(seconds)


def digest_of(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


def _authed(email: str, env_var: str):
    token = login(email, seeded_password(env_var, SEED_PASSWORD))
    return client(token)


@pytest.fixture(scope="session")
def author_client():
    with _authed(AUTHOR_EMAIL, "SEED_AUTHOR_PASSWORD") as c:
        yield c


@pytest.fixture(scope="session")
def author2_client():
    with _authed(AUTHOR2_EMAIL, "SEED_AUTHOR2_PASSWORD") as c:
        yield c


@pytest.fixture(scope="session")
def reader_client():
    with _authed(READER_EMAIL, "SEED_READER_PASSWORD") as c:
        yield c


class ShowcaseStore:
    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def author_by_email(self, email: str) -> dict | None:
        return self._b.one("authors", email=email)

    def reader_by_email(self, email: str) -> dict | None:
        return self._b.one("readers", email=email)

    def count_readers(self, **where) -> int:
        return self._b.count("readers", **where)

    def page_by_slug(self, slug: str) -> dict | None:
        return self._b.one("pages", slug=slug)

    def count_pages(self, **where) -> int:
        return self._b.count("pages", **where)

    def blocks_of(self, page_id) -> list[dict]:
        return self._b.rows("blocks", page_id=page_id)

    def count_blocks(self, **where) -> int:
        return self._b.count("blocks", **where)

    def media_by_key(self, object_key: str) -> dict | None:
        return self._b.one("media", object_key=object_key)

    def count_media(self, **where) -> int:
        return self._b.count("media", **where)

    def notebook_by_slug(self, slug: str) -> dict | None:
        return self._b.one("notebooks", slug=slug)

    def notebooks(self, limit: int | None = None, **where) -> list[dict]:
        return self._b.rows("notebooks", limit=limit, **where)

    def count_notebooks(self, **where) -> int:
        return self._b.count("notebooks", **where)

    def count_testimonials(self, **where) -> int:
        return self._b.count("testimonials", **where)

    def count_use_cases(self, **where) -> int:
        return self._b.count("use_cases", **where)

    def count_footer_links(self, **where) -> int:
        return self._b.count("footer_links", **where)

    def count_subscribers(self, **where) -> int:
        return self._b.count("newsletter_subscribers", **where)


@pytest.fixture(scope="session")
def db() -> ShowcaseStore:
    return ShowcaseStore(make_backend())


@pytest.fixture(scope="session")
def store() -> ObjectStore:
    return make_store()


@pytest.fixture
def probe_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


@pytest.fixture
def probe_bytes() -> bytes:
    marker = os.urandom(12).hex().encode("ascii")
    return b"\x89PNG\r\n\x1a\n" + marker + b"probe-media-payload"


def signup_payload(email: str) -> dict:
    return {"email": email, "password": SEED_PASSWORD}


def upload_media(client_, page_slug: str, payload: bytes):
    return client_.post(
        "/media",
        files={"file": ("probe.png", payload, "image/png")},
        data={"page_slug": page_slug},
    )


def key_for(page_slug: str, payload: bytes, ext: str = "png") -> str:
    return f"media/{page_slug}/{digest_of(payload)}.{ext}"


def create_page(client_, slug: str, title: str):
    return client_.post("/pages", json={"slug": slug, "title": title, "meta_title": title})


def add_block(client_, page_id, position: int, kind: str = "value_line", **fields):
    body = {"page_id": page_id, "position": position, "kind": kind}
    body.update(fields)
    return client_.post("/blocks", json=body)


def publish(client_, slug: str):
    return client_.post(f"/pages/{slug}/publish", json={})
