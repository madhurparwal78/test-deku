"""Fixtures, pinned literals and domain helpers for Doodlerush.

Every literal below is pinned in instruction.md. Nothing here defines a test.
"""

from __future__ import annotations

import contextlib
import os
import time
import uuid
from typing import Any

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"

PLAYER_EMAIL = "player@example.com"
PLAYER2_EMAIL = "player2@example.com"
PLAYER3_EMAIL = "player3@example.com"
MODERATOR_EMAIL = "moderator@example.com"

PLAYER_NAME = "Ivy"
PLAYER2_NAME = "Bo"
PLAYER3_NAME = "Ren"
MODERATOR_NAME = "Wren"

ROLE_PLAYER = "player"
ROLE_MODERATOR = "moderator"

ROOM_NAME = "Friday Night Doodles"
ROOM_CODE = "PARROT42"
ROOM_CAP = 4
ROOM_SEEDED_PLAYERS = 3
PUBLIC_ROOM_NAME = "Open Table"
LANGUAGE = "English"

ROOM_CODE_LENGTH = 8

STATE_LOBBY = "lobby"
STATE_CHOOSING = "choosing"
STATE_DRAWING = "drawing"
STATE_TURN_END = "turn_end"
STATE_ROUND_END = "round_end"
STATE_GAME_END = "game_end"

KIND_PUBLIC = "public"
KIND_PRIVATE = "private"

OUTCOME_CORRECT = "correct"
OUTCOME_CLOSE = "close"
OUTCOME_CHAT = "chat"

OP_UNDO = "undo"
OP_CLEAR = "clear"
OP_FILL = "fill"

MODE_NORMAL = "normal"
MODE_HIDDEN = "hidden"
MODE_COMBINATION = "combination"

DIFFICULTY_EASY = "easy"
DIFFICULTY_MEDIUM = "medium"
DIFFICULTY_HARD = "hard"

SEAT_HEADER = "X-Seat-Token"
SEAT_FIELD = "seat_token"
MASK_FIELD = "word_mask"
INVITE_FIELD = "invite_url"
OUTCOME_FIELD = "outcome"

NAME_MIN = 1
NAME_MAX = 16
GUESS_MAX_CHARS = 100
GUESS_RATE = 4
GUESS_WINDOW_SECONDS = 2

PLAYERS_MIN = 2
PLAYERS_MAX = 20
PLAYERS_DEFAULT = 8
ROUNDS_DEFAULT = 3
TURN_SECONDS_MIN = 30
TURN_SECONDS_MAX = 180
TURN_SECONDS_DEFAULT = 80
WORD_CHOICES_DEFAULT = 3
HINTS_DEFAULT = 2

AWARD_MAX = 500
AWARD_MIN = 50
LATE_GRACE_MS = 250
SEAT_GRACE_SECONDS = 45
ROOM_RETENTION_SECONDS = 60
STROKES_PER_TURN = 4000
STROKE_BATCHES_PER_SECOND = 60
CANVAS_OPS_PER_TURN = 20
FILL_COVERAGE_CAP = 95
WORDLIST_MIN = 2000
CUSTOM_WORD_MAX_CHARS = 100
CUSTOM_WORDS_MAX = 500
REPORTS_PER_HOUR = 3
REPORT_RETENTION_DAYS = 30
TOKEN_LIFETIME_HOURS = 24

PRIVACY_PATH = "/privacy"
TERMS_PATH = "/terms"
CREATE_PATH = "/create"
LOGIN_PATH = "/login"
SIGNUP_PATH = "/signup"
ACCOUNT_PATH = "/account"
REPORTS_PATH = "/reports"
ROOM_PATH = "/room/PARROT42"

PUBLIC_ROUTES = ("/", CREATE_PATH, PRIVACY_PATH, TERMS_PATH, LOGIN_PATH, SIGNUP_PATH)

FOOTER_LINKS = ("Contact", "Terms of Service", "Credits", "Privacy")
PRIMARY_ACTION = "Play!"
SECONDARY_ACTION = "Create Private Room"
LANDING_TITLE = "Doodlerush - Free Multiplayer Drawing & Guessing Game"
REVEAL_LINE = "The word was"

CONTRAST_RATIO = 4.5
TOUCH_TARGET_PX = 44
NARROW_VIEWPORT = {"width": 390, "height": 844}
WIDE_VIEWPORT = {"width": 1440, "height": 900}

TRANSPORT_HEADER = "strict-transport-security"
NOSNIFF_HEADER = "x-content-type-options"

SUCCESS_STATUSES = (200, 201, 202, 204)
REFUSAL_STATUSES = (400, 401, 403, 404, 409, 422)
DENIAL_STATUSES = (401, 403, 404)
NOT_FOUND_STATUSES = (404,)
CONFLICT_STATUSES = (400, 403, 409, 410, 422)

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


def probe_name() -> str:
    return f"Probe{unique_suffix()[:6]}"


def site_base() -> str:
    return appclient.api_base().rsplit("/api", 1)[0]


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code} :: {response.text[:400]}")


def rows_of(payload: Any) -> list:
    """A list endpoint returns a top-level array; a paged one wraps it in `data`."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "items", "results", "rows", "reports", "players"):
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


def body_of(response: httpx.Response) -> Any:
    """The decoded body, or None when the response carries no JSON document."""
    import json
    text = response.text.strip()
    if not text.startswith(("{", "[")):
        return None
    return json.loads(text)


def flatten(value: Any) -> str:
    """Every scalar anywhere in a payload, joined, so a secret cannot hide in a corner."""
    import json
    return json.dumps(value, ensure_ascii=False, default=str)


class Session:
    """One Doodlerush caller: an optional bearer token, an optional seat token."""

    def __init__(self, token: str | None = None, email: str | None = None,
                 seat: str | None = None) -> None:
        self.token = token
        self.email = email
        self.seat = seat
        self.player_id: str | None = None

    def _headers(self, extra: dict | None = None) -> dict:
        headers: dict[str, str] = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if self.seat:
            headers[SEAT_HEADER] = self.seat
        headers.update(extra or {})
        return headers

    def request(self, method: str, path: str, body: dict | None = None,
                params: dict | None = None,
                headers: dict | None = None) -> httpx.Response:
        with httpx.Client(base_url=appclient.api_base(), timeout=30.0) as client:
            return client.request(method, path, json=body, params=params,
                                  headers=self._headers(headers))

    def get(self, path: str, **params: Any) -> httpx.Response:
        return self.request("GET", path,
                            params={k: v for k, v in params.items() if v is not None})

    def post(self, path: str, body: dict | None = None) -> httpx.Response:
        return self.request("POST", path, body=body)

    def patch(self, path: str, body: dict | None = None) -> httpx.Response:
        return self.request("PATCH", path, body=body)

    def signup(self, email: str, display_name: str,
               password: str = PASSWORD) -> httpx.Response:
        return self.post("/auth/signup", {"email": email, "password": password,
                                          "display_name": display_name})

    def create_room(self, name: str, settings: dict | None = None) -> httpx.Response:
        return self.post("/rooms", {"name": name, "language": LANGUAGE,
                                    "settings": settings or {}})

    def room(self, code: str = ROOM_CODE) -> httpx.Response:
        return self.get(f"/rooms/{code}")

    def join(self, code: str = ROOM_CODE, display_name: str | None = None,
             avatar: dict | None = None, seat: str | None = None) -> httpx.Response:
        body: dict[str, Any] = {"display_name": display_name or probe_name(),
                                "avatar": avatar or {"colour": 0, "eyes": 0,
                                                     "mouth": 0, "special": 0}}
        if seat:
            body[SEAT_FIELD] = seat
        return self.post(f"/rooms/{code}/join", body)

    def state(self, code: str = ROOM_CODE) -> httpx.Response:
        return self.get(f"/rooms/{code}/state")

    def start(self, code: str = ROOM_CODE) -> httpx.Response:
        return self.post(f"/rooms/{code}/start")

    def settings(self, patch: dict, code: str = ROOM_CODE) -> httpx.Response:
        return self.patch(f"/rooms/{code}/settings", patch)

    def choose_word(self, index: int = 0, code: str = ROOM_CODE) -> httpx.Response:
        return self.post(f"/rooms/{code}/word-choice", {"index": index})

    def guess(self, text: str, code: str = ROOM_CODE) -> httpx.Response:
        return self.post(f"/rooms/{code}/guess", {"text": text})

    def strokes(self, batch: list, code: str = ROOM_CODE) -> httpx.Response:
        return self.post(f"/rooms/{code}/strokes", {"batch": batch})

    def canvas_op(self, op: str, sid: int, code: str = ROOM_CODE) -> httpx.Response:
        return self.post(f"/rooms/{code}/canvas-op", {"sid": sid, "op": op})

    def leave(self, code: str = ROOM_CODE) -> httpx.Response:
        return self.post(f"/rooms/{code}/leave")

    def reports(self) -> httpx.Response:
        return self.get("/reports")

    def file_report(self, target: str, code: str = ROOM_CODE) -> httpx.Response:
        return self.post("/reports", {"code": code, "target": target})


def seat_in(code: str, display_name: str | None = None) -> Session:
    """Take a seat as a guest and return the session that holds the seat token."""
    session = Session()
    response = session.join(code, display_name)
    assert response.status_code in SUCCESS_STATUSES, (
        f"join {code!r}: expected a success, got {describe(response)}")
    payload = body_of(response) or {}
    session.seat = str(field(payload, SEAT_FIELD, "seat", "token", default=""))
    session.player_id = field(payload, "player_id", "id", "seat_id")
    assert session.seat, f"join {code!r} returned no seat token: {describe(response)}"
    return session


def stroke(sid: int, colour: int = 1, width: int = 1) -> dict:
    return {"sid": sid, "c": colour, "w": width,
            "p": [[0.1000, 0.1000], [0.5000, 0.5000], [0.9000, 0.9000]]}


class Store:
    """Read-only reach into the declared datastore, for what HTTP cannot show."""

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

    def account(self, email: str) -> dict | None:
        for row in self.backend.rows("accounts", limit=500):
            if str(field(row, "email", default="")).lower() == email.lower():
                return row
        return None

    def room(self, code: str) -> dict | None:
        for row in self.backend.rows("rooms", limit=500):
            if str(field(row, "code", default="")) == code:
                return row
        return None

    def table_names(self) -> list[str]:
        found = self.backend.query(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public'")
        return [str(field(row, "table_name", default="")) for row in found]

    def text_columns(self, table: str) -> list[str]:
        found = self.backend.query(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema = 'public' AND table_name = %s "
            "AND data_type IN ('text', 'character varying', 'character')",
            (table,))
        return [str(field(row, "column_name", default="")) for row in found]


@pytest.fixture(scope="session")
def store() -> Store:
    return Store(capabilities.make_backend())


@pytest.fixture(scope="session")
def app_base() -> str:
    return appclient.api_base()


@pytest.fixture()
def visitor() -> Session:
    return Session()


@pytest.fixture()
def owner() -> Session:
    return Session(appclient.login(PLAYER_EMAIL, PASSWORD), PLAYER_EMAIL)


@pytest.fixture()
def second_player() -> Session:
    return Session(appclient.login(PLAYER2_EMAIL, PASSWORD), PLAYER2_EMAIL)


@pytest.fixture()
def third_player() -> Session:
    return Session(appclient.login(PLAYER3_EMAIL, PASSWORD), PLAYER3_EMAIL)


@pytest.fixture()
def moderator() -> Session:
    return Session(appclient.login(MODERATOR_EMAIL, PASSWORD), MODERATOR_EMAIL)


@pytest.fixture(scope="session")
def browser_session():
    """Chromium, from the browsers the verifier image already carries."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as driver:
        browser = driver.chromium.launch()
        try:
            yield browser
        finally:
            with contextlib.suppress(Exception):
                browser.close()


@pytest.fixture()
def page(browser_session):
    """A real rendered page, so a surface can be observed rather than inferred."""
    context = browser_session.new_context(viewport=WIDE_VIEWPORT)
    opened = context.new_page()
    try:
        yield opened
    finally:
        with contextlib.suppress(Exception):
            context.close()
