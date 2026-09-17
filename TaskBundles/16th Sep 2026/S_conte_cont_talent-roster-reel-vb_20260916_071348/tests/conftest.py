from __future__ import annotations

import hashlib
import mimetypes
import os
import time

import httpx
import pytest

import appclient
import capabilities

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 30.0

APP_PASSWORD = "deku-demo-pw-2026"
PRODUCER_EMAIL = "producer@example.com"
PRODUCER2_EMAIL = "producer2@example.com"
VISITOR_EMAIL = "visitor@example.com"

UNPUBLISHED_TALENT_SLUG = "odile-marchand"
UNPUBLISHED_TALENT_NAME = "Odile Marchand"
UNPUBLISHED_WORK_SLUG = "the-quiet-room"
UNPUBLISHED_WORK_TITLE = "The Quiet Room"

WORK_SLUGS = (
    "the-halo",
    "sonder",
    "binary",
    "common-ground",
    "nve",
    "the-absolute-shelter",
    "maison-de-lumiere",
    "loris",
    "mdl-serie-extreme",
    "ak",
    "loris-shoot-studio",
    "the-radiant",
)
WORK_TITLES = (
    "The Halo",
    "Sonder",
    "BINARY",
    "Common Ground",
    "NVE",
    "The Absolute Shelter",
    "MAISON DE LUMIERE",
    "LORIS",
    "MDL Serie Extreme",
    "AK",
    "Loris Shoot Studio",
    "The Radiant",
)
SEEDED_ORDINALS = tuple(f"{n:03d}" for n in range(1, 13))

TALENT_SLUGS = ("rives", "halcyon", "camille-ferrand")
TALENT_NAMES = ("Rives", "Halcyon", "Camille Ferrand")
SEEDED_DISCIPLINES = ("director", "photographer")

PUBLIC_ROUTES = ("/", "/works", "/talents", "/about")
SLASHED_ROUTES = (("/works", "/works/"), ("/talents", "/talents/"))
STUDIO_ROUTES = (
    "/studio",
    "/studio/talents",
    "/studio/talents/new",
    "/studio/works",
    "/studio/works/new",
    "/studio/page-views",
)
STUDIO_API_ROUTES = ("/items", "/page-views")

OBJECT_KEY_PREFIX = "items/"
OBJECT_KEY_TEMPLATE = "items/{item_id}/{digest}{ext}"

SECURITY_HEADERS = ("x-content-type-options", "referrer-policy",
                    "content-security-policy")

PNG_BYTES = bytes.fromhex(
    "89504e470d0a1a0a0000000d494844520000000100000001080600000"
    "01f15c4890000000a49444154789c6360000002000100ffff03000006"
    "0005570bf7050000000049454e44ae426082")


def settle() -> None:
    time.sleep(SETTLE_SECONDS)


def unique_token() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{unique_token()}@example.com"


def probe_slug(stem: str) -> str:
    return f"{stem}-{unique_token()}"


def probe_bytes() -> bytes:
    return PNG_BYTES + unique_token().encode("ascii")


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def expected_object_key(item_id, payload: bytes, content_type: str) -> str:
    ext = mimetypes.guess_extension(content_type) or ""
    return OBJECT_KEY_TEMPLATE.format(
        item_id=item_id, digest=sha256_hex(payload), ext=ext)


def describe(response) -> str:
    body = response.text[:400]
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}; body: {body}")


def poll_until(predicate, deadline_seconds: float = POLL_DEADLINE_SECONDS):
    deadline = time.monotonic() + deadline_seconds
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    return last


def item_id(item) -> str:
    for key in ("id", "item_id", "itemId"):
        if key in item:
            return item[key]
    raise AssertionError(f"created item carries no id field: {item}")


@pytest.fixture(scope="session")
def api_base() -> str:
    return appclient.api_base()


@pytest.fixture(scope="session")
def app_base() -> str:
    return appclient.app_url()


@pytest.fixture()
def anon():
    with appclient.client() as c:
        yield c


@pytest.fixture()
def producer_token() -> str:
    return appclient.login(PRODUCER_EMAIL, APP_PASSWORD)


@pytest.fixture()
def second_producer_token() -> str:
    return appclient.login(PRODUCER2_EMAIL, APP_PASSWORD)


@pytest.fixture()
def visitor_token() -> str:
    return appclient.login(VISITOR_EMAIL, APP_PASSWORD)


@pytest.fixture()
def producer(producer_token):
    with appclient.client(producer_token) as c:
        yield c


@pytest.fixture()
def second_producer(second_producer_token):
    with appclient.client(second_producer_token) as c:
        yield c


@pytest.fixture()
def visitor(visitor_token):
    with appclient.client(visitor_token) as c:
        yield c


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def site():
    with httpx.Client(base_url=appclient.app_url(), timeout=30.0,
                      follow_redirects=True) as c:
        yield c


@pytest.fixture()
def site_direct():
    with httpx.Client(base_url=appclient.app_url(), timeout=30.0) as c:
        yield c
