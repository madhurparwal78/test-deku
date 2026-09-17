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

ADMIN_EMAIL = "admin@example.com"
MEMBER_EMAIL = "member@example.com"
MEMBER2_EMAIL = "member2@example.com"
GUEST_EMAIL = "guest@example.com"

ADMIN_NAME = "Priya Raman"
MEMBER_NAME = "Tomas Vidal"
MEMBER2_NAME = "Nadia Okafor"
GUEST_NAME = "Ellis Byrne"

GROUP_NAME = "Editors"

OPEN_TEAMSPACE = "Engineering"
CLOSED_TEAMSPACE = "People Ops"
PRIVATE_TEAMSPACE = "Board Papers"
OPEN_SLUG = "engineering"
CLOSED_SLUG = "people-ops"
PRIVATE_SLUG = "board-papers"

HANDBOOK = "Engineering Handbook"
RELEASE_NOTES = "Release Notes"
RELEASE_NOTES_SLUG = "release-notes"
HANDBOOK_SLUG = "engineering-handbook"
ONBOARDING = "Onboarding Checklist"
COMPENSATION = "Compensation Bands"
BOARD_MINUTES = "Board Minutes"

DATABASE_NAME = "Company Tasks"
TABLE_VIEW = "Company tasks"
BOARD_VIEW = "Current sprint"
HIDDEN_PROPERTY = "Key notes"
TITLE_PROPERTY = "Project"
SELECT_PROPERTY = "Team"
DATE_PROPERTY = "Date"
CREATED_BY_PROPERTY = "Created by"
STATUS_PROPERTY = "Status"
STATUS_OPTIONS = ["To-do", "In progress", "In review", "Complete"]
UNIQUE_ID_PREFIX = "ZEN"

SEEDED_ATTACHMENT = "handbook-cover.png"
WORKSPACE_SLUG = "meridian"
KEY_SCHEME_PREFIX = "workspaces/" + WORKSPACE_SLUG + "/pages/"

LOGIN_ROUTE = "/login"
WORKSPACE_HOME_ROUTE = "/w"
SEARCH_ROUTE = "/w/search"
PAGE_ROUTE = "/w/p/{pageId}"
VIEW_ROUTE = "/w/db/{dbId}/{viewId}"
ADMIN_MEMBERS_ROUTE = "/w/admin/members"
ADMIN_TEAMSPACES_ROUTE = "/w/admin/teamspaces"
ADMIN_ACTIVITY_ROUTE = "/w/admin/activity"
PUBLISHED_ROUTE = "/site/{slug}"
CREDENTIAL_FILE = "/app/USER_README.md"
CONTAINER_PORT = "4173"
BLOCK_VOLUME_FLOOR = "10000"
ROW_VOLUME_FLOOR = "5000"

PRODUCT_NAME = "Meridian Workspace"

ACCESS_MODES = ("open", "closed", "private")
GRANT_LEVELS = ("full_access", "edit", "comment", "read")
GRANT_EFFECTS = ("allow", "deny")
VIEW_KINDS = ("table", "board")
UNIQUE_ID_KEYS = ("ZEN-1", "ZEN-2", "ZEN-3")
COPY_STRINGS = ("Teamspaces", "Private", "More", "Share", "New", "New page", "Syncing")

API_SURFACE = (
    "/api/admin/activity",
    "/api/admin/groups",
    "/api/admin/groups/{id}/members",
    "/api/admin/groups/{id}/members/{principalId}",
    "/api/admin/members",
    "/api/admin/members/{id}/deactivate",
    "/api/attachments/{attachmentId}",
    "/api/auth/identify",
    "/api/auth/login",
    "/api/auth/logout",
    "/api/blocks/{blockId}",
    "/api/blocks/{blockId}/move",
    "/api/blocks/{blockId}/restore",
    "/api/databases/{dbId}",
    "/api/databases/{dbId}/views/{viewId}/rows",
    "/api/grants",
    "/api/grants/{grantId}",
    "/api/health",
    "/api/me",
    "/api/pages",
    "/api/pages/{pageId}",
    "/api/pages/{pageId}/access",
    "/api/pages/{pageId}/attachments",
    "/api/pages/{pageId}/blocks",
    "/api/pages/{pageId}/publish",
    "/api/public/attachments/{attachmentId}",
    "/api/public/pages/{slug}",
    "/api/rows/{rowPageId}",
    "/api/search",
    "/api/teamspaces",
    "/api/teamspaces/{id}",
    "/api/views/{viewId}",
)

ERROR_CODES = [
    "unauthorized",
    "forbidden_permission",
    "not_found",
    "conflict_version",
    "conflict_state",
    "validation_failed",
    "rate_limited",
    "dependency_unavailable",
]

SECURITY_HEADER_NAMES = ["strict-transport-security", "x-content-type-options"]

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
    """A unique identifier per run, so a test never collides with its own history."""
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
        return str(body.get("code") or "")
    return ""


def page_named(client: httpx.Client, title: str) -> dict | None:
    response = client.get("/search", params={"q": title})
    if response.status_code != 200:
        return None
    body = response.json()
    if not isinstance(body, list):
        return None
    for row in body:
        if row.get("title") == title:
            return row
    return None


def teamspace_named(client: httpx.Client, name: str) -> dict | None:
    response = client.get("/teamspaces")
    assert response.status_code == 200, describe(response)
    body = response.json()
    assert isinstance(body, list), describe(response)
    for row in body:
        if row.get("name") == name:
            return row
    return None


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def admin_token():
    return token_for(ADMIN_EMAIL)


@pytest.fixture(scope="session")
def member_token():
    return token_for(MEMBER_EMAIL)


@pytest.fixture(scope="session")
def member2_token():
    return token_for(MEMBER2_EMAIL)


@pytest.fixture(scope="session")
def guest_token():
    return token_for(GUEST_EMAIL)


@pytest.fixture()
def admin(admin_token):
    with appclient.client(admin_token) as handle:
        yield handle


@pytest.fixture()
def member(member_token):
    with appclient.client(member_token) as handle:
        yield handle


@pytest.fixture()
def member2(member2_token):
    with appclient.client(member2_token) as handle:
        yield handle


@pytest.fixture()
def guest(guest_token):
    with appclient.client(guest_token) as handle:
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
def handbook(member):
    row = page_named(member, HANDBOOK)
    assert row is not None, f"seeded page {HANDBOOK!r} was not found through search"
    return row
