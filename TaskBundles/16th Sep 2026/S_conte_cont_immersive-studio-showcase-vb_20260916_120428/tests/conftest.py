from __future__ import annotations

import hashlib
import os
import time
import uuid

import httpx
import pytest

import appclient
import capabilities

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 20.0

PASSWORD = appclient.seeded_password("SEEDED_PASSWORD", "deku-demo-pw-2026")

AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"

STUDIO_NAME = "Northform"
CONTACT_ADDRESS = "hello@northform.co"
FOOTER_CONTACT_LINE = "We'd love to hear from you"

DRAFT_CASE_SLUG = "harbour-line-rebrand"
PUBLISHED_CASE_SLUG = "grand-opera-of-verdal"
FILTER_CASE_SLUG = "lumenfest"
DRAFT_POST_SLUG = "the-quiet-rebrand"
PUBLISHED_POST_SLUG = "studio-turns-ten"

NOT_FOUND_HEADING = "Ooh shit!"
NOT_FOUND_LINE = "You're lost..."
NOT_FOUND_LINK = "Back to homepage"

DISCIPLINES = ("Web", "Strategy", "Design")
OFFICES = ("Detroit", "Rotterdam", "Lyon")
SOCIAL_NETWORKS = ("Facebook", "Instagram", "Dribbble", "Twitter")
PUBLISHED_CASE_SLUGS = (
    "lumenfest",
    "tidewater-hall",
    "grand-museum-of-science",
    "this-was-mias-phone",
    "prism-festival-2018",
    "the-whitfield-center",
    "grand-opera-of-verdal",
)
PUBLIC_ROUTES = (
    "/",
    "/studio",
    "/cases",
    "/values",
    "/careers",
    "/news",
    "/contact",
    "/privacy",
    "/terms",
)
CREDENTIAL_NEEDLES = (
    "deku-local-dev",
    "minio-root-3d81f7a2",
    "STORAGE_SECRET_KEY",
    "password_hash",
)

ONE_PIXEL_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
    "890000000a49444154789c6360000002000100ffff0300000600055773d5d600"
    "00000049454e44ae426082"
)


def settle() -> None:
    time.sleep(SETTLE_SECONDS)


def unique_token() -> str:
    return uuid.uuid4().hex[:12]


def unique_email() -> str:
    return f"probe-{unique_token()}@example.com"


def unique_slug(stem: str) -> str:
    return f"{stem}-{unique_token()}"


def image_bytes(seed: str) -> bytes:
    return ONE_PIXEL_PNG + seed.encode("utf-8")


def digest_of(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def poll_until(predicate, deadline_seconds: float = POLL_DEADLINE_SECONDS):
    deadline = time.monotonic() + deadline_seconds
    outcome = predicate()
    while not outcome and time.monotonic() < deadline:
        settle()
        outcome = predicate()
    return outcome


def page(path: str, token: str | None = None) -> httpx.Response:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.get(
        f"{appclient.app_url()}{path}",
        headers=headers,
        timeout=appclient.TIMEOUT,
        follow_redirects=True,
    )


def raw_page(path: str, token: str | None = None) -> httpx.Response:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.get(
        f"{appclient.app_url()}{path}",
        headers=headers,
        timeout=appclient.TIMEOUT,
        follow_redirects=False,
    )


def looks_absent(response: httpx.Response) -> bool:
    return response.status_code in (401, 403, 404)


def refusal_fingerprint(response: httpx.Response) -> tuple:
    body = response.text
    return (response.status_code, len(body), NOT_FOUND_HEADING in body)


def create_case(client: httpx.Client, slug: str, discipline: str = "Design") -> httpx.Response:
    return client.post(
        "/cases",
        json={
            "slug": slug,
            "title": slug.replace("-", " ").title(),
            "client": "Probe Client",
            "year_range": "2026",
            "discipline": discipline,
            "headline": "A probe case study written by the grader.",
            "accent": "violet",
        },
    )


def upload_asset(client: httpx.Client, slug: str, payload: bytes,
                 alt_text: str = "A probe hero image.") -> httpx.Response:
    return client.post(
        f"/cases/{slug}/assets",
        files={"file": ("hero.png", payload, "image/png")},
        data={"alt_text": alt_text},
    )


def publish(client: httpx.Client, slug: str, state: str = "published") -> httpx.Response:
    return client.post(f"/cases/{slug}/publish", json={"state": state})


@pytest.fixture(scope="session")
def author_token() -> str:
    return appclient.login(AUTHOR_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def author2_token() -> str:
    return appclient.login(AUTHOR2_EMAIL, PASSWORD)


@pytest.fixture(scope="session")
def reader_token() -> str:
    return appclient.login(READER_EMAIL, PASSWORD)


@pytest.fixture()
def author_client(author_token):
    with appclient.client(author_token) as c:
        yield c


@pytest.fixture()
def author2_client(author2_token):
    with appclient.client(author2_token) as c:
        yield c


@pytest.fixture()
def reader_client(reader_token):
    with appclient.client(reader_token) as c:
        yield c


@pytest.fixture()
def anon_client():
    with appclient.client() as c:
        yield c


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def probe_case(author_client):
    slug = unique_slug("probe-case")
    response = create_case(author_client, slug)
    assert response.status_code in (200, 201), (
        f"creating the probe case {slug!r} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    return slug


@pytest.fixture(scope="session")
def public_url() -> str:
    return appclient.app_url()


@pytest.fixture(scope="session")
def bucket_name() -> str:
    return os.environ["STORAGE_BUCKET"]
