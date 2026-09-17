"""Task fixtures for deku/consumer-device-catalogue-vb.

Nothing here assumes the agent's framework, file layout, ORM or module names.
The only assumptions are the App Contract and whatever instruction.md pinned
literally: the route set, the field names, the seeded accounts and password,
the seeded catalogue matrix, the four serials, the reference and subject
schemes, and the fifteen table names.
"""

from __future__ import annotations

import os
import time

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, Inbox, make_backend, make_inbox

SETTLE_SECONDS = 2.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give an unwanted async side effect time to land before asserting absence."""
    time.sleep(seconds)


OWNER_EMAIL = "owner@example.com"
OWNER2_EMAIL = "owner2@example.com"

FAMILIES = ("phones", "audio", "wearables", "arc")
EMPTY_FAMILY = "wearables"

FLAGSHIP_SLUG = "phone-5a-pro"
SECOND_PHONE_SLUG = "phone-5a"
HEADPHONE_SLUG = "headphone-2"
EARBUD_SLUG = "earbud-3a"
ARC_BUDS_SLUG = "arc-buds-1"
ARC_WATCH_SLUG = "arc-watch-2"

PRODUCT_SLUGS = (FLAGSHIP_SLUG, SECOND_PHONE_SLUG, HEADPHONE_SLUG, EARBUD_SLUG,
                 ARC_BUDS_SLUG, ARC_WATCH_SLUG)

SMALL_CAPACITY = "8 GB / 128 GB"
LARGE_CAPACITY = "12 GB / 256 GB"

DIRECT_VARIANTS = {
    "phone-5a-pro--chalk--8-128": 79900,
    "phone-5a-pro--midnight--12-256": 99900,
    "headphone-2--black": 29900,
    "earbud-3a--white": 14900,
    "arc-watch-2--grey": 6900,
}
HANDOFF_VARIANTS = (
    "phone-5a-pro--chalk--12-256",
    "phone-5a-pro--slate--8-128",
    "phone-5a--chalk--8-128",
    "phone-5a--slate--8-128",
    "headphone-2--white",
    "arc-buds-1--orange",
    "arc-buds-1--grey",
)
UNAVAILABLE_VARIANTS = ("phone-5a-pro--slate--12-256", "earbud-3a--black")

RESOLVED_VARIANT = "phone-5a-pro--midnight--12-256"
MISSING_PAIR = (FLAGSHIP_SLUG, "Midnight", SMALL_CAPACITY)

RELEASE_DATES = {
    FLAGSHIP_SLUG: "2026-08-12",
    ARC_WATCH_SLUG: "2026-06-03",
    HEADPHONE_SLUG: "2026-04-21",
    SECOND_PHONE_SLUG: "2026-02-17",
    EARBUD_SLUG: "2025-11-05",
    ARC_BUDS_SLUG: "2025-09-30",
}

SERIAL_OWNED_BY_FIRST = "HLC-7K42QD19"
SERIAL_UNREGISTERED = "HLC-3M08XT55"
SERIAL_OWNED_BY_SECOND = "HLC-9P61BW73"
SERIAL_UNKNOWN_PRODUCT = "HLC-0000ZZZZ"
SERIAL_MALFORMED = "HLC-3M08"

SUPPORT_CATEGORIES = ("Setup", "Battery", "Connectivity", "Software", "Physical damage")
SUPPORT_CATEGORY = "Battery"
REFERENCE_PREFIX = "SR-"
SUBJECT_PREFIX = "Support request "
LOGIN_FAILURE_WORDING = "Incorrect email or password"

PUBLIC_ROUTES = (
    "/",
    "/collections/phones",
    "/collections/audio",
    "/collections/wearables",
    "/collections/arc",
    "/products/phone-5a-pro",
    "/products/phone-5a",
    "/products/headphone-2",
    "/products/earbud-3a",
    "/products/arc-buds-1",
    "/products/arc-watch-2",
    "/cart",
    "/about",
    "/halcyonos-4-1",
    "/lower-ground",
    "/pages/support-centre",
    "/pages/privacy-policy",
    "/pages/warranty-policy",
    "/pages/user-agreement",
    "/pages/acceptable-use",
    "/pages/terms-of-sale",
)

CREDENTIAL_MARKERS = (
    "deku-local-dev",
    "postgresql://",
    "DB_ADMIN_URL",
    "EMAIL_INBOX_API_URL",
)


def app_origin() -> str:
    return os.environ["APP_PUBLIC_URL"].rstrip("/")


def owner_password() -> str:
    return seeded_password("SEED_OWNER_PASSWORD", "deku-demo-pw-2026")


@pytest.fixture
def anon_client():
    with client() as c:
        yield c


@pytest.fixture
def owner_client():
    token = login(OWNER_EMAIL, owner_password())
    with client(token) as c:
        yield c


@pytest.fixture
def second_owner_client():
    token = login(OWNER2_EMAIL, owner_password())
    with client(token) as c:
        yield c


class CatalogueStore:
    """Domain queries composed from the generic capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def count_families(self) -> int:
        return self._b.count("families")

    def count_products(self) -> int:
        return self._b.count("products")

    def count_variants(self) -> int:
        return self._b.count("variants")

    def variant(self, variant_id: str) -> dict | None:
        return self._b.one("variants", variant_id=variant_id)

    def variants_for(self, product_slug: str) -> list[dict]:
        return self._b.rows("variants", product_slug=product_slug)

    def registration(self, serial: str) -> dict | None:
        return self._b.one("registrations", serial=serial)

    def count_registrations(self, serial: str) -> int:
        return self._b.count("registrations", serial=serial)

    def count_support_requests(self) -> int:
        return self._b.count("support_requests")

    def support_request(self, reference: str) -> dict | None:
        return self._b.one("support_requests", reference=reference)

    def count_requests_for_key(self, idempotency_key: str) -> int:
        return self._b.count("support_requests", idempotency_key=idempotency_key)

    def count_outbound_clicks(self, variant_id: str) -> int:
        return self._b.count("outbound_clicks", variant_id=variant_id)

    def count_article_votes(self, article_slug: str, anonymous_id: str) -> int:
        return self._b.count("article_votes", article_slug=article_slug,
                             anonymous_id=anonymous_id)

    def article_vote(self, article_slug: str, anonymous_id: str) -> dict | None:
        return self._b.one("article_votes", article_slug=article_slug,
                           anonymous_id=anonymous_id)

    def count_cart_lines(self, variant_id: str) -> int:
        return self._b.count("cart_lines", variant_id=variant_id)

    def account(self, email: str) -> dict | None:
        return self._b.one("accounts", email=email)


@pytest.fixture(scope="session")
def db() -> CatalogueStore:
    return CatalogueStore(make_backend())


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    """The mail server inbox, inspected out of band. Never smtplib."""
    return make_inbox()


@pytest.fixture
def probe_token() -> str:
    return os.urandom(6).hex()


def wait_for_message(inbox: Inbox, to: str, subject_contains: str,
                     timeout: float = 20.0):
    """Poll to a monotonic deadline for a message the app was asked to send."""
    deadline = time.monotonic() + timeout
    found = inbox.find(to=to, subject_contains=subject_contains)
    while found is None and time.monotonic() < deadline:
        settle(0.5)
        found = inbox.find(to=to, subject_contains=subject_contains)
    return found


def signup(email: str, password: str) -> str:
    """Create a fresh owner and return the bearer token for that account."""
    with client() as c:
        response = c.post("/auth/signup", json={"email": email, "password": password})
    assert response.status_code in (200, 201), (
        f"POST /api/auth/signup for {email} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    return login(email, password)


def open_request_form(c) -> dict:
    """Read the registrations the signed in owner holds, for a request body."""
    response = c.get("/registrations")
    assert response.status_code == 200, (
        f"GET /api/registrations returned {response.status_code}: {response.text[:400]}"
    )
    return response.json()
