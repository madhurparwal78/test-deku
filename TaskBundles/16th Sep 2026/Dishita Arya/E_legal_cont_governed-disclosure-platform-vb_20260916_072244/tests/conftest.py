from __future__ import annotations

import os
import time
import uuid

import httpx
import pytest

import appclient
import capabilities

APP_URL = os.environ.get("APP_PUBLIC_URL", "http://localhost:4173")
API = APP_URL.rstrip("/") + "/api"

CORPUS_PASSWORD = "deku-demo-pw-2026"

AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
LEGAL_EMAIL = "legal_reviewer@example.com"
COMPLIANCE_EMAIL = "compliance_officer@example.com"
PUBLISHER_EMAIL = "publisher@example.com"
GROUP_ADMIN_EMAIL = "group_admin@example.com"

AUTHOR_NAME = "Ines Marchetti"
AUTHOR2_NAME = "Tobias Renner"
LEGAL_NAME = "Priya Raman"
COMPLIANCE_NAME = "Yusuf Adeyemi"
PUBLISHER_NAME = "Hana Lindqvist"
GROUP_ADMIN_NAME = "Elena Duarte"

SEEDED_EMAILS = (
    AUTHOR_EMAIL,
    AUTHOR2_EMAIL,
    LEGAL_EMAIL,
    COMPLIANCE_EMAIL,
    PUBLISHER_EMAIL,
    GROUP_ADMIN_EMAIL,
)

DIVISION_GROUP = "group"
DIVISION_TRADING = "trading"
DIVISION_CAPITAL = "capital"
DIVISION_MARITIME = "maritime"
DIVISION_VENTURE = "kite-energy"
DIVISION_KEYS = (
    DIVISION_GROUP,
    DIVISION_TRADING,
    DIVISION_CAPITAL,
    DIVISION_MARITIME,
    DIVISION_VENTURE,
)
DIVISION_NAMES = {
    DIVISION_GROUP: "Calder Group",
    DIVISION_TRADING: "Calder Trading",
    DIVISION_CAPITAL: "Calder Capital",
    DIVISION_MARITIME: "Calder Maritime",
    DIVISION_VENTURE: "Kite Energy",
}

ROLES = (
    "author",
    "legal_reviewer",
    "compliance_officer",
    "publisher",
    "group_admin",
)

STATES = (
    "draft",
    "in_review",
    "legal_review",
    "compliance_review",
    "changes_requested",
    "approved",
    "embargoed",
    "published",
    "unpublished",
    "archived",
)

DISCLOSURE_CLASSES = ("general", "regulated", "market_sensitive", "restricted")

RECORD_TYPES = (
    "page",
    "release",
    "product",
    "vessel",
    "investment",
    "person",
    "figures",
    "policy",
    "redirect",
)

BLOCK_TYPES = (
    "paragraph",
    "subheading_2",
    "subheading_3",
    "list_unordered",
    "list_ordered",
    "quote",
    "image",
    "table",
)

JURISDICTIONS = ("CH", "AE-DIFC", "SG")

OFFICE_CITIES = ("Geneva", "Dubai", "Singapore")
GENEVA_ADDRESS = "12 Quai des Bergues, 1201 Geneva"
DUBAI_ADDRESS = "Level 14, Gate Village 7, DIFC, Dubai"
SINGAPORE_ADDRESS = "8 Marina View, Asia Square Tower 1, Singapore"
GENEVA_PHONE = "+41225550118"
DUBAI_PHONE = "+97145550142"
SINGAPORE_PHONE = "+6562550173"
GENEVA_EMAIL = "gva@calder.example.com"
DUBAI_EMAIL = "dxb@calder.example.com"
SINGAPORE_EMAIL = "sgp@calder.example.com"
MEDIA_EMAIL = "media@calder.example.com"
MARKER_LABELS = ("SWITZERLAND", "UAE", "SINGAPORE")

PUBLISHED_RELEASE_COUNT = 9
ARCHIVE_PAGE_SIZE = 6

NEWEST_RELEASE_TITLE = "Calder joins Energy LEAP for Operational Excellence"
OLDEST_RELEASE_TITLE = "Calder Maritime acquires its first vessel"
EMBARGOED_RELEASE_TITLE = "Calder Trading agrees a multi-year naphtha supply arrangement"
WITHDRAWN_RELEASE_TITLE = "Calder restates its 2022 throughput figures"
WITHDRAWAL_REASON = "Superseded by a corrected statement"

OIL_FAMILY = "Oil"
METALS_FAMILY = "Metals"
OIL_PRODUCTS = (
    "Crude oil",
    "Marine Fuels",
    "Gasoline",
    "LPG (Liquefied Petroleum Gas)",
    "Power and Gas",
    "Fuel Oil",
    "Downstream",
    "Naphtha",
    "Renewables",
)
METALS_PRODUCTS = ("Ferroalloys", "Dry Bulk", "Base Metals")

FIGURES_OFFICE_COUNT = "15"
FIGURES_NATIONALITY_COUNT = "27"
FIGURES_FEMALE_GLOBAL = "35"
FIGURES_FEMALE_MANAGEMENT = "22"

POLICY_CODES = (
    "POL-CONDUCT",
    "POL-PRIVACY-CH",
    "POL-PRIVACY-AE",
    "POL-PRIVACY-SG",
    "POL-TERMS",
    "POL-DISC-REG",
)

KEY_SCHEME_PREFIX = "media/"

HOME_ROUTE = "/"
TRADING_ROUTE = "/trading/"
CAPITAL_ROUTE = "/capital/"
MARITIME_ROUTE = "/maritime/"
VENTURE_ROUTE = "/kite-energy/"
WHO_WE_ARE_ROUTE = "/who-we-are/"
ARCHIVE_ROUTE = "/news/"
RELEASE_ROUTE = "/news/{slug}/"
SUSTAINABILITY_ROUTE = "/sustainability/"
CONTACT_ROUTE = "/contact/"
PRIVACY_ROUTE = "/privacy-policy/"
TERMS_ROUTE = "/terms-of-use/"
SEARCH_ROUTE = "/search"
CONSOLE_LOGIN_ROUTE = "/console/login"
CONSOLE_ROUTE = "/console"
CONSOLE_NEW_ROUTE = "/console/releases/new"
CONSOLE_AUDIT_ROUTE = "/console/admin/audit"
CONSOLE_MEMBERS_ROUTE = "/console/admin/members"
CONSOLE_EXCEPTIONS_ROUTE = "/console/admin/exceptions"

PUBLIC_ROUTES = (
    HOME_ROUTE,
    TRADING_ROUTE,
    CAPITAL_ROUTE,
    MARITIME_ROUTE,
    VENTURE_ROUTE,
    WHO_WE_ARE_ROUTE,
    ARCHIVE_ROUTE,
    SUSTAINABILITY_ROUTE,
    CONTACT_ROUTE,
    PRIVACY_ROUTE,
    TERMS_ROUTE,
)

ANCHORS = ("#WhoWeAre", "#WhatWeDo", "#GlobalConnectivity", "#Sustainability")

COPY_STRINGS = (
    "Calder Group",
    "Calder Trading",
    "Calder Capital",
    "Calder Maritime",
    "Kite Energy",
    "News",
    "Menu",
    "Contact",
    "ESG",
    "Privacy policy",
    "Terms of use",
    "Scroll down to discover",
    "Swipe down",
    "Who we are",
    "Explore Our",
    "Products:",
    "Oil",
    "Metals",
    "Environmental",
    "Social",
    "Governance",
    "Contact us",
    "First",
    "Last",
    "Geneva, Switzerland",
    "Dubai, UAE",
    "Singapore",
)

CHAPTER_ONE_HEADLINE = "Calder is a global commodity trading and asset investment company."
CHAPTER_TWO_HEADING = "We provide energy solutions with integrity and efficiency"
TRADING_PROPOSITION = "Operating Efficiently, Leading with Innovation."
CAPITAL_PROPOSITION = "Identify and seize opportunities that maximise value"
VENTURE_PROPOSITION = "Energy investments"
SUSTAINABILITY_HEADING = "Delivering sustainable energy solutions"
PEOPLE_STATEMENT = (
    "We strive to create an environment where everyone can thrive and contribute to our success."
)
RESPONSIBILITY_HEADING = "Our pledge to corporate social responsibility"
NOT_FOUND_LINE = "We cannot find that page. It may have moved, or the address may be mistyped."

API_SURFACE = (
    "/api/admin/audit",
    "/api/admin/exceptions",
    "/api/admin/members",
    "/api/admin/memberships",
    "/api/admin/memberships/{id}",
    "/api/auth/login",
    "/api/auth/logout",
    "/api/content/records",
    "/api/content/records/{id}",
    "/api/content/records/{id}/classify",
    "/api/content/records/{id}/media",
    "/api/content/records/{id}/revisions",
    "/api/health",
    "/api/me",
    "/api/media/{mediaId}",
    "/api/policy/entries",
    "/api/public/counters",
    "/api/public/divisions",
    "/api/public/enquiries",
    "/api/public/figures",
    "/api/public/media/{mediaId}",
    "/api/public/offices",
    "/api/public/policies",
    "/api/public/releases",
    "/api/public/releases/{slug}",
    "/api/public/search",
    "/api/workflow/delegations",
    "/api/workflow/delegations/{id}",
    "/api/workflow/inbox",
    "/api/workflow/records/{id}/publish",
    "/api/workflow/records/{id}/schedule",
    "/api/workflow/records/{id}/submit",
    "/api/workflow/records/{id}/transition",
    "/api/workflow/records/{id}/unpublish",
)

ERROR_CODES = [
    "unauthorized",
    "forbidden_permission",
    "not_found",
    "gone",
    "conflict_version",
    "conflict_state",
    "validation_failed",
    "rate_limited",
    "dependency_unavailable",
]

SECURITY_HEADER_NAMES = ["strict-transport-security", "x-content-type-options"]

CREDENTIAL_FILE = "/app/USER_README.md"
CONTAINER_PORT = "4173"
RECORD_VOLUME_FLOOR = "20000"
AUDIT_VOLUME_FLOOR = "4000"
DELEGATION_DAY_CAP = "30"
FAST_PATH_CAP = "3"
IDEMPOTENCY_HOURS = "24"
FAILED_LOGIN_ALLOWANCE = "5"
ENQUIRY_HOURLY_LIMIT = "5"
FORM_TOKEN_MINUTES = "30"
FORM_MINIMUM_SECONDS = "3"
MEMBERSHIP_DAY_CAP = "90"
PUBLICATION_SECONDS = "30"
MEMBERSHIP_SECONDS = "60"
LATE_PUBLICATION_SECONDS = "60"
ESCALATION_HOURS = "48"
SECOND_ESCALATION_HOURS = "96"
CONTRAST_BODY = "4.5"
CONTRAST_LARGE = "3"
TOUCH_TARGET = "44"
CONSOLE_FLOOR = "1024"
TEXT_SCALE = "200"

PRODUCT_NAME = "Calder Disclosure Platform"

SETTLE_SECONDS = 0.5
SETTLE_ATTEMPTS = 20


def settle(predicate, attempts: int = SETTLE_ATTEMPTS, delay: float = SETTLE_SECONDS):
    """Poll a predicate with a bounded budget. The only sanctioned sleep."""
    last = None
    for _ in range(attempts):
        last = predicate()
        if last:
            return last
        time.sleep(delay)
    return last


def probe_id() -> str:
    """A unique identifier per run, so one run never collides with its own history."""
    return uuid.uuid4().hex[:12]


def token_for(email: str) -> str:
    return appclient.login(email, CORPUS_PASSWORD)


def anon() -> httpx.Client:
    return httpx.Client(base_url=API, timeout=30.0)


def raw_anon() -> httpx.Client:
    return httpx.Client(base_url=APP_URL.rstrip("/"), timeout=30.0)


def describe(response: httpx.Response) -> str:
    return (
        f"{response.request.method} {response.request.url} -> "
        f"{response.status_code}: {response.text[:400]}"
    )


def code_of(response: httpx.Response) -> str:
    """The machine-readable `code` a rejection carries, or the empty string."""
    content_type = response.headers.get("content-type", "")
    if "json" not in content_type.lower():
        return ""
    body = response.json()
    if isinstance(body, dict):
        error = body.get("error")
        if isinstance(error, dict):
            return str(error.get("code") or "")
        return str(body.get("code") or "")
    return ""


def records_for(client: httpx.Client, **params) -> list:
    response = client.get("/content/records", params=params)
    assert response.status_code == 200, describe(response)
    body = response.json()
    assert isinstance(body, list), describe(response)
    return body


def record_titled(client: httpx.Client, title: str, **params) -> dict | None:
    for row in records_for(client, **params):
        if row.get("title") == title:
            return row
    return None


def public_releases(client: httpx.Client, **params) -> dict:
    response = client.get("/public/releases", params=params)
    assert response.status_code == 200, describe(response)
    body = response.json()
    assert isinstance(body, dict), describe(response)
    return body


def counter_value(client: httpx.Client) -> int:
    response = client.get("/public/counters")
    assert response.status_code == 200, describe(response)
    return int(response.json()["published_releases"])


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def author_token():
    return token_for(AUTHOR_EMAIL)


@pytest.fixture(scope="session")
def author2_token():
    return token_for(AUTHOR2_EMAIL)


@pytest.fixture(scope="session")
def legal_token():
    return token_for(LEGAL_EMAIL)


@pytest.fixture(scope="session")
def compliance_token():
    return token_for(COMPLIANCE_EMAIL)


@pytest.fixture(scope="session")
def publisher_token():
    return token_for(PUBLISHER_EMAIL)


@pytest.fixture(scope="session")
def group_admin_token():
    return token_for(GROUP_ADMIN_EMAIL)


@pytest.fixture()
def author(author_token):
    with appclient.client(author_token) as handle:
        yield handle


@pytest.fixture()
def author2(author2_token):
    with appclient.client(author2_token) as handle:
        yield handle


@pytest.fixture()
def legal(legal_token):
    with appclient.client(legal_token) as handle:
        yield handle


@pytest.fixture()
def compliance(compliance_token):
    with appclient.client(compliance_token) as handle:
        yield handle


@pytest.fixture()
def publisher(publisher_token):
    with appclient.client(publisher_token) as handle:
        yield handle


@pytest.fixture()
def group_admin(group_admin_token):
    with appclient.client(group_admin_token) as handle:
        yield handle


@pytest.fixture()
def stranger():
    with anon() as handle:
        yield handle


@pytest.fixture()
def site():
    with raw_anon() as handle:
        yield handle


@pytest.fixture()
def embargoed_release(publisher):
    row = record_titled(publisher, EMBARGOED_RELEASE_TITLE, division=DIVISION_TRADING)
    assert row is not None, (
        f"seeded embargoed release {EMBARGOED_RELEASE_TITLE!r} was not found"
    )
    return row


@pytest.fixture()
def withdrawn_release(publisher):
    row = record_titled(publisher, WITHDRAWN_RELEASE_TITLE, division=DIVISION_GROUP)
    assert row is not None, (
        f"seeded withdrawn release {WITHDRAWN_RELEASE_TITLE!r} was not found"
    )
    return row


@pytest.fixture()
def capital_in_compliance(compliance):
    rows = records_for(compliance, division=DIVISION_CAPITAL, state="compliance_review")
    assert rows, "no seeded capital record sits in compliance_review"
    return rows[0]
