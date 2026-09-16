"""Fixtures, pinned literals and domain stores for Rookery.

Every literal below is pinned in instruction.md. Nothing here defines a test.
"""

from __future__ import annotations

import os
import time
import uuid
from typing import Any

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"

OWNER_EMAIL = "owner@example.com"
MODERATOR_EMAIL = "moderator@example.com"
MEMBER_EMAIL = "member@example.com"
MEMBER2_EMAIL = "member2@example.com"

OWNER_NAME = "Wren"
MODERATOR_NAME = "Ember"
MEMBER_NAME = "Juniper"
MEMBER2_NAME = "Hazel"

SPACE_NAME = "Nightjar Collective"
SPACE_SLUG = "nightjar-collective"
SPACE_MEMBER_CAP = 4
SPACE_SEEDED_MEMBERS = 3

SECOND_SPACE_NAME = "Studio Loft"
SECOND_SPACE_SLUG = "studio-loft"
SECOND_SPACE_CHANNEL = "studio"

CHANNEL_WELCOME = "welcome"
CHANNEL_GENERAL = "general"
CHANNEL_BUILD_LOG = "build-log"
CHANNEL_MODS_ONLY = "mods-only"
CHANNEL_SHOWCASE = "showcase"
CHANNEL_VOICE = "Main Stage"
CHANNEL_STAGE = "Front Room"

ROLE_EVERYONE = "@everyone"
ROLE_REGULARS = "Regulars"
ROLE_ARCHIVISTS = "Archivists"
ROLE_MODERATORS = "Moderators"

PERM_VIEW_CHANNEL = "VIEW_CHANNEL"
PERM_READ_HISTORY = "READ_HISTORY"
PERM_SEND_MESSAGES = "SEND_MESSAGES"
PERM_ADD_REACTIONS = "ADD_REACTIONS"
PERM_MANAGE_MESSAGES = "MANAGE_MESSAGES"
PERM_VIEW_AUDIT_LOG = "VIEW_AUDIT_LOG"

INVITE_CODE = "NIGHTJAR-ONE"
INVITE_MAX_USES = 1
MSG_INVITE_SPENT = "That invite has already been used."

GIFT_CODE = "LOFT-ONE-SEAT"
PLAN_MONTHLY = "Loft Monthly"
PLAN_YEARLY = "Loft Yearly"
PLAN_MONTHLY_MINOR = 1000
PLAN_YEARLY_MINOR = 10000
CURRENCY = "usd"
TIER_NAME = "Loft"

MAIL_SUBJECT_PREFIX = "Rookery mention:"

MESSAGE_MAX_CLUSTERS = 4000
NONCE_WINDOW_SECONDS = 300
PAGE_SIZE_PARAM = "page_size"
PAGE_SIZE_DEFAULT = 50
PAGE_SIZE_MAX = 100
CURSOR_FIELD = "next_cursor"
MORE_FLAG = "has_more"
CORRELATION_FIELD = "request_id"

NOTIFY_ALL = "all"
NOTIFY_MENTIONS = "mentions"
NOTIFY_NOTHING = "nothing"
NOTIFY_INHERIT = "inherit"

STATUS_INCOMPLETE = "incomplete"
STATUS_ACTIVE = "active"
STATUS_PAST_DUE = "past_due"
STATUS_UNPAID = "unpaid"
STATUS_CANCELLED = "cancelled"

TERMS_PATH = "/legal/terms"
PRIVACY_PATH = "/legal/privacy"
HERO_HEADLINE = "A ROOM THAT IS ALWAYS OPEN"
NOT_FOUND_HEADLINE = "NOTHING LIVES HERE"
SKIP_LINK = "Skip to main content"

SUCCESS_STATUSES = (200, 201, 202, 204)
REFUSAL_STATUSES = (400, 401, 403, 404, 409, 422)
DENIAL_STATUSES = (401, 403)
NOT_FOUND_STATUSES = (404,)
CONFLICT_STATUSES = (400, 409, 410, 422)

SETTLE_SECONDS = 0.4
POLL_BUDGET_SECONDS = 25.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned pause, for an effect the app writes just after replying."""
    time.sleep(seconds)


def poll_until(predicate, budget: float = POLL_BUDGET_SECONDS):
    """Bounded polling on a monotonic clock. Returns the last value the predicate saw."""
    deadline = time.monotonic() + budget
    value = predicate()
    while not value and time.monotonic() < deadline:
        settle()
        value = predicate()
    return value


def unique_suffix() -> str:
    return uuid.UUID(bytes=os.urandom(16), version=4).hex[:10]


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def probe_handle() -> str:
    return f"probe{unique_suffix()}"


def probe_nonce() -> str:
    return f"nonce-{unique_suffix()}"


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code} :: {response.text[:400]}")


def rows_of(payload: Any) -> list:
    """A list endpoint returns a top-level array; a paged one wraps it in `data`."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "items", "results", "messages", "rows"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def field(row: Any, *names: str, default: Any = None) -> Any:
    """Read the first present field name, so a spelling the brief left free still reads."""
    if not isinstance(row, dict):
        return default
    for name in names:
        if name in row and row[name] is not None:
            return row[name]
    return default


class Session:
    """One Rookery session: an optional bearer token and the calls a member makes."""

    def __init__(self, token: str | None = None, email: str | None = None) -> None:
        self.token = token
        self.email = email

    def _client(self) -> httpx.Client:
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        return httpx.Client(base_url=appclient.api_base(), timeout=30.0,
                            headers=headers)

    def request(self, method: str, path: str, body: dict | None = None,
                params: dict | None = None,
                headers: dict | None = None) -> httpx.Response:
        with self._client() as client:
            return client.request(method, path, json=body, params=params,
                                  headers=headers or {})

    def get(self, path: str, **params: Any) -> httpx.Response:
        return self.request("GET", path,
                            params={k: v for k, v in params.items() if v is not None})

    def post(self, path: str, body: dict | None = None) -> httpx.Response:
        return self.request("POST", path, body=body)

    def put(self, path: str, body: dict | None = None) -> httpx.Response:
        return self.request("PUT", path, body=body)

    def patch(self, path: str, body: dict | None = None) -> httpx.Response:
        return self.request("PATCH", path, body=body)

    def delete(self, path: str) -> httpx.Response:
        return self.request("DELETE", path)

    def signup(self, email: str, handle: str, display_name: str,
               password: str = PASSWORD) -> httpx.Response:
        return self.post("/auth/signup", {"email": email, "password": password,
                                          "handle": handle,
                                          "display_name": display_name})

    def spaces(self) -> httpx.Response:
        return self.get("/spaces")

    def channels(self, space: str = SPACE_SLUG) -> httpx.Response:
        return self.get(f"/spaces/{space}/channels")

    def redeem_invite(self, code: str = INVITE_CODE) -> httpx.Response:
        return self.post(f"/invites/{code}/redeem")

    def redeem_gift(self, code: str = GIFT_CODE) -> httpx.Response:
        return self.post(f"/gift-codes/{code}/redeem")

    def entitlements(self) -> httpx.Response:
        return self.get("/entitlements")

    def permissions(self, channel: str, account: str) -> httpx.Response:
        return self.get(f"/channels/{channel}/permissions/{account}")

    def messages(self, channel: str, **params: Any) -> httpx.Response:
        return self.get(f"/channels/{channel}/messages", **params)

    def send(self, channel: str, content: str, nonce: str | None = None,
             **extra: Any) -> httpx.Response:
        body: dict[str, Any] = {"content": content,
                                "nonce": nonce or probe_nonce()}
        body.update(extra)
        return self.post(f"/channels/{channel}/messages", body)

    def react(self, message_id: str, emoji: str) -> httpx.Response:
        return self.put(f"/messages/{message_id}/reactions/{emoji}/me")

    def unreact(self, message_id: str, emoji: str) -> httpx.Response:
        return self.delete(f"/messages/{message_id}/reactions/{emoji}/me")

    def ack(self, channel: str, message_id: str, manual: bool = False) -> httpx.Response:
        return self.post(f"/channels/{channel}/ack",
                         {"message_id": message_id, "manual": manual})

    def read_states(self) -> httpx.Response:
        return self.get("/read-states")

    def timeout_member(self, account: str, expires_at: str, reason: str,
                       space: str = SPACE_SLUG) -> httpx.Response:
        return self.post(f"/spaces/{space}/members/{account}/timeout",
                         {"expires_at": expires_at, "reason": reason})


class Store:
    """Read-only reach into the declared datastore, for side effects HTTP cannot show."""

    def __init__(self, backend: Any) -> None:
        self.backend = backend

    def query(self, sql: str, params: tuple = ()) -> list[dict]:
        return self.backend.query(sql, params)

    def count(self, table: str, **where: Any) -> int:
        return self.backend.count(table, **where)

    def rows(self, table: str, limit: int | None = None, **where: Any) -> list[dict]:
        return self.backend.rows(table, limit=limit, **where)

    def one(self, table: str, **where: Any) -> dict | None:
        return self.backend.one(table, **where)

    def table_row_count(self, table: str) -> int:
        return self.backend.count(table)

    def account(self, email: str) -> dict | None:
        found = self.backend.rows("account", limit=200)
        for row in found:
            if str(field(row, "email", default="")).lower() == email.lower():
                return row
        return None

    def space(self, slug: str) -> dict | None:
        for row in self.backend.rows("space", limit=200):
            if field(row, "slug") == slug:
                return row
        return None

    def memberships_in(self, slug: str) -> list[dict]:
        space = self.space(slug)
        if space is None:
            return []
        space_id = field(space, "id")
        return [row for row in self.backend.rows("membership", limit=2000)
                if str(field(row, "space_id")) == str(space_id)]

    def messages_with_nonce(self, nonce: str) -> list[dict]:
        return [row for row in self.backend.rows("message", limit=2000)
                if field(row, "nonce") == nonce]

    def reactions_for(self, message_id: str) -> list[dict]:
        return [row for row in self.backend.rows("reaction", limit=2000)
                if str(field(row, "message_id")) == str(message_id)]

    def entitlements_for(self, email: str) -> list[dict]:
        account = self.account(email)
        if account is None:
            return []
        account_id = field(account, "id")
        return [row for row in self.backend.rows("entitlement", limit=2000)
                if str(field(row, "account_id")) == str(account_id)]

    def gift_code(self, code: str) -> dict | None:
        for row in self.backend.rows("gift_code", limit=200):
            if field(row, "code") == code:
                return row
        return None

    def invite(self, code: str) -> dict | None:
        for row in self.backend.rows("invite", limit=200):
            if field(row, "code") == code:
                return row
        return None


@pytest.fixture(scope="session")
def store() -> Store:
    return Store(capabilities.make_backend())


@pytest.fixture(scope="session")
def inbox():
    return capabilities.make_inbox()


@pytest.fixture(scope="session")
def app_base() -> str:
    return appclient.api_base()


@pytest.fixture()
def visitor() -> Session:
    return Session()


@pytest.fixture()
def owner() -> Session:
    return Session(appclient.login(OWNER_EMAIL, PASSWORD), OWNER_EMAIL)


@pytest.fixture()
def moderator() -> Session:
    return Session(appclient.login(MODERATOR_EMAIL, PASSWORD), MODERATOR_EMAIL)


@pytest.fixture()
def member() -> Session:
    return Session(appclient.login(MEMBER_EMAIL, PASSWORD), MEMBER_EMAIL)


@pytest.fixture()
def outsider() -> Session:
    return Session(appclient.login(MEMBER2_EMAIL, PASSWORD), MEMBER2_EMAIL)
