"""Task fixtures for deku/instrument-portfolio-console-vb.

Two rules govern this file. Nothing here assumes the agent's framework, file
layout, ORM or module names: the only assumptions are the App Contract and what
instruction.md pinned literally. And nothing here reaches a provider SDK; the
domain helpers are composed from the generic primitives in capabilities.py, so
swapping a slot's provider replaces the adapter rather than this file.
"""

from __future__ import annotations

import os
import time
import uuid

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

OWNER_EMAIL = "owner@example.com"
EDITOR_EMAIL = "editor@example.com"
CORPUS_PASSWORD = "deku-demo-pw-2026"

OWNER_DISPLAY_NAME = "Marlow Hendriks"
EDITOR_DISPLAY_NAME = "Rowan Vale"
PROFILE_FULL_NAME = "MARLOW HENDRIKS"
PROFILE_ROLE_LINE = "Product Engineer and Design Engineer"
FOOTER_LINE = "COPYRIGHT 2026 MARLOW HENDRIKS. ALL RIGHTS RESERVED."

STUDY_FIRST = "Ridge Survey"
STUDY_SECOND = "Tide Table"
STUDY_THIRD = "Lantern Field"

RECOGNITION_FIRST = "Northlight Prize"
RECOGNITION_SECOND = "Meridian Review"
RECOGNITION_THIRD = "Halden Biennale"

CITY_FIRST = "Oslo"
CITY_SECOND = "Lisbon"
CITY_THIRD = "Kyoto"

PALETTE_NEUTRAL = "neutral"
PALETTE_BLUE = "blue"
PALETTE_CORAL = "coral"

STATE_UNREAD = "unread"
STATE_READ = "read"
STATE_ARCHIVED = "archived"

PREVIEW_KEY_PREFIX = "previews/"
PREVIEW_KEY_SUFFIX = ".png"

TITLE_MAX = 120
KIND_MAX = 60
SUMMARY_MAX = 280
BODY_MAX = 8000
SEED_MAX = 999999
YEAR_MIN = 1970
YEAR_MAX = 2026
LINK_LABEL_MAX = 40
SENDER_NAME_MAX = 80
SENDER_EMAIL_MAX = 254
MESSAGE_BODY_MIN = 10
MESSAGE_BODY_MAX = 4000
MESSAGE_RATE_LIMIT = 3
LOCKOUT_ATTEMPTS = 5

ERROR_TITLE = "Give the entry a title."
ERROR_KIND = "Keep this under 60 characters."
ERROR_YEAR = "Use a four digit year up to 2026."
ERROR_SUMMARY = "Keep the summary under 280 characters."
ERROR_BODY = "This is longer than the editor will keep."
ERROR_SEED = "Use a whole number up to 999999."
ERROR_LINK = "Give this link a label and a secure address."
ERROR_SENDER_NAME = "Tell me what to call you."
ERROR_SENDER_EMAIL = "That address will not reach you."
ERROR_MESSAGE_BODY = "A few more words, please."
SIGN_IN_FAILURE = "That did not match. Check both fields and try again."
REFUSAL_EXPLANATION = "Messages are visible to the owner only."

PUBLIC_ROUTES = ("/", "/product", "/sketch", "/award", "/contact")

SECURITY_HEADERS = (
    "strict-transport-security",
    "x-content-type-options",
    "x-frame-options",
    "referrer-policy",
)

OK = (200, 201)
ACCEPTED = (200, 201, 202, 204)
DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
GONE_OR_MISSING = (404, 410)
REFUSED = (400, 403, 409, 422, 429)
CONFLICT = (409, 422)

SETTLE_SECONDS = 3.0
POLL_SECONDS = 20.0


def settle() -> None:
    """The one sanctioned sleep: a bounded wait before asserting a non-event."""
    time.sleep(SETTLE_SECONDS)


def unique_suffix() -> str:
    return uuid.uuid4().hex[:10]


def probe_title() -> str:
    return f"Probe Entry {unique_suffix()}"


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def poll_until(predicate, timeout: float = POLL_SECONDS):
    """Poll a predicate to a monotonic deadline. Returns the truthy value or None."""
    deadline = time.monotonic() + timeout
    while True:
        value = predicate()
        if value:
            return value
        if time.monotonic() >= deadline:
            return None
        settle()


def api(path: str) -> str:
    return f"/api{path}"


def body_text(response) -> str:
    return response.text


def json_body(response) -> dict:
    """The response body as a mapping, or an empty mapping when it is not JSON.

    Guarded on the content type rather than on an exception: a handler that
    swallowed a decode error would turn a malformed body into a non-event.
    """
    if "json" not in response.headers.get("content-type", "").lower():
        return {}
    value = response.json()
    return value if isinstance(value, dict) else {}


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture()
def owner_client():
    token = login(OWNER_EMAIL, seeded_password("SEED_OWNER_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture()
def editor_client():
    token = login(EDITOR_EMAIL, seeded_password("SEED_EDITOR_PASSWORD", CORPUS_PASSWORD))
    with client(token) as c:
        yield c


class ConsoleStore:
    """Domain queries for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def account_by_email(self, email: str) -> dict | None:
        return self._b.one("account", email=email)

    def count_accounts(self, **where) -> int:
        return self._b.count("account", **where)

    def entry_by_title(self, title: str) -> dict | None:
        return self._b.one("work_entry", title=title)

    def entry_by_id(self, entry_id) -> dict | None:
        return self._b.one("work_entry", id=entry_id)

    def entries(self, **where) -> list[dict]:
        return self._b.rows("work_entry", **where)

    def count_entries(self, **where) -> int:
        return self._b.count("work_entry", **where)

    def links_for(self, entry_id) -> list[dict]:
        return self._b.rows("entry_link", entry_id=entry_id)

    def study_by_title(self, title: str) -> dict | None:
        return self._b.one("study", title=title)

    def count_studies(self, **where) -> int:
        return self._b.count("study", **where)

    def recognition_by_body(self, body: str) -> dict | None:
        return self._b.one("recognition", body=body)

    def count_recognitions(self, **where) -> int:
        return self._b.count("recognition", **where)

    def city_by_name(self, name: str) -> dict | None:
        return self._b.one("city", name=name)

    def message_by_email(self, email: str) -> dict | None:
        return self._b.one("message", sender_email=email)

    def count_messages(self, **where) -> int:
        return self._b.count("message", **where)

    def page_views(self, **where) -> list[dict]:
        return self._b.rows("page_view", **where)

    def count_page_views(self, **where) -> int:
        return self._b.count("page_view", **where)


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def console(backend: Backend) -> ConsoleStore:
    return ConsoleStore(backend)


@pytest.fixture(scope="session")
def store() -> ObjectStore:
    return make_store()


def preview_keys(store: ObjectStore, entry_id) -> list[str]:
    return [k for k in store.list(f"{PREVIEW_KEY_PREFIX}{entry_id}/")
            if k.endswith(PREVIEW_KEY_SUFFIX)]


def new_entry_payload(**overrides) -> dict:
    payload = {
        "title": probe_title(),
        "kind": "Web",
        "year": 2024,
        "summary": "A short summary.",
        "body": "A longer description of the work.",
        "grid_seed": 4096,
        "grid_palette": PALETTE_NEUTRAL,
        "links": [],
    }
    payload.update(overrides)
    return payload


def new_message_payload(**overrides) -> dict:
    payload = {
        "name": "Probe Visitor",
        "email": probe_email(),
        "body": "A message long enough to be accepted by the form.",
        "decoy": "",
        "built_at": "2026-01-01T00:00:00Z",
        "source_path": "/contact",
    }
    payload.update(overrides)
    return payload


def create_entry(owner, **overrides):
    return owner.post(api("/studio/work"), json=new_entry_payload(**overrides))


def entry_id_of(response, console_store, title: str):
    data = json_body(response)
    item = data.get("item")
    if isinstance(item, dict) and item.get("id") is not None:
        return item["id"]
    if data.get("id") is not None:
        return data["id"]
    row = console_store.entry_by_title(title)
    return row.get("id") if row else None


def version_of(response, console_store, entry_id):
    data = json_body(response)
    item = data.get("item")
    if isinstance(item, dict) and item.get("version") is not None:
        return item["version"]
    row = console_store.entry_by_id(entry_id)
    return row.get("version") if row else None


def console_payload(anon):
    response = anon.get(api("/console"))
    assert response.status_code == 200, (
        f"GET /api/console answered {response.status_code} with no credential; the "
        f"public console read requires no session. Body: {body_text(response)[:400]}"
    )
    return response.json()


def work_titles(payload) -> list[str]:
    work = payload.get("work") or []
    return [item.get("title") for item in work if isinstance(item, dict)]


def app_origin() -> str:
    return os.environ.get("APP_PUBLIC_URL", "http://localhost:4173").rstrip("/")
