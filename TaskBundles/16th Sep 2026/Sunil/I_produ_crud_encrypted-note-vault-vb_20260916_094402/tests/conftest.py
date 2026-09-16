"""Fixtures, pinned literals and the one sanctioned sleep for Lockleaf.

Every literal here appears verbatim in instruction.md and on the Literals Ledger.
No test function lives in this file. Signing in to a seeded account goes through the
real sign-in page, because the password never leaves the browser: the session token
is read from the app's own sign-in response rather than minted here.
"""
from __future__ import annotations

import base64
import os
import re
import time
import uuid

import pytest

import appclient
import capabilities

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 60.0
PAGE_TIMEOUT_MS = 120000

CORPUS_PASSWORD = "deku-demo-pw-2026"
OWNER_EMAIL = "user@example.com"
MEMBER_EMAIL = "user2@example.com"
LAPSED_EMAIL = "user3@example.com"
PROBE_DOMAIN = "@example.com"

CONTENT_TYPES = ("note", "tag", "items_key", "file", "revision", "saved_view",
                 "preferences")
ENVELOPE_LIMIT = 2000000
PAGE_LIMIT = 100
CANOPY = "Canopy"
LEAF = "Leaf"
ACTIVE = "active"
CANOPY_QUOTA_BYTES = 107374182400
LAPSED_REVISIONS = 2

VERSION_CONFLICT = "version_conflict"
UUID_CONFLICT = "uuid_conflict"
PLAN_LIMIT = "plan_limit"
INVALID_TYPE = "invalid_type"
TOO_LARGE = "too_large"
PENDING = "pending"
COMPLETE = "complete"

CONFIRMATION_PHRASE = "delete my notes forever"
START_OVER_LINK = "Start over with an empty vault"
START_OVER_BUTTON = "Delete my vault and start over"
SIGNUP_WARNING = "Nobody can recover your notes if you forget this password."
SAVED_STATUS = "All changes saved"
UNOPENABLE_HEADING = "This note cannot be opened"
NOT_FOUND_HEADING = "We can't find that page."
DEMO_NOTICE = "Nothing you write here is saved."
SEARCH_LABEL = "Search notes"
LOCK_PASSCODE = "482917"

PINNED_TITLE = "Grocery run"
PINNED_WORDS = "Oat milk, lemons, rye bread, coffee filters."
RENEWAL_TITLE = "Passport renewal"

PUBLIC_ROUTES = ("/", "/plans", "/privacy", "/longevity", "/signup", "/sign-in")
FORBIDDEN_ITEM_COLUMNS = ("title", "body", "name", "tag", "tags", "pinned", "archived",
                          "protected", "trashed", "file_name", "filename")

DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
OK = (200, 201)


def settle() -> None:
    """The only sanctioned sleep. Gives an absent side effect a fair chance to land."""
    time.sleep(SETTLE_SECONDS)


def run_tag() -> str:
    """A unique per-run identifier, so two identical runs never collide."""
    return uuid.uuid4().hex[:12]


def new_uuid() -> str:
    return str(uuid.uuid4())


def opaque_envelope() -> str:
    """Random bytes standing in for a sealed envelope. The server cannot tell."""
    return base64.b64encode(os.urandom(48)).decode("ascii")


def is_client_error(status: int) -> bool:
    return 400 <= status < 500


def poll_until(predicate, message: str):
    """Bounded polling to a monotonic deadline. Never a bare sleep before a positive."""
    deadline = time.monotonic() + POLL_DEADLINE_SECONDS
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    raise AssertionError(f"{message}; last observation was {last!r}")


def encodings(text: str) -> tuple:
    """The plain form of a marker and its common reversible encodings."""
    raw = text.encode("utf-8")
    return (text, base64.b64encode(raw).decode("ascii").rstrip("="),
            base64.urlsafe_b64encode(raw).decode("ascii").rstrip("="), raw.hex())


@pytest.fixture(scope="session")
def api() -> str:
    return appclient.api_base()


@pytest.fixture(scope="session")
def app_url() -> str:
    return appclient.app_url()


@pytest.fixture(scope="session")
def backend() -> capabilities.Backend:
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store() -> capabilities.ObjectStore:
    return capabilities.make_store()


@pytest.fixture()
def anonymous():
    with appclient.client(None) as c:
        yield c


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


def new_page(browser_handle):
    context = browser_handle.new_context()
    context.set_default_timeout(PAGE_TIMEOUT_MS)
    return context, context.new_page()


@pytest.fixture()
def page(browser):
    context, pg = new_page(browser)
    yield pg
    context.close()


def client_for(token: str):
    return appclient.client(token)


def record_requests(pg) -> list:
    """Every request the page sends from now on, as (method, url, body text)."""
    log: list = []
    pg.on("request", lambda req: log.append(
        (req.method, req.url, (req.post_data_buffer or b"").decode("utf-8", "replace"))))
    return log


def requests_carrying(log: list, needles: tuple) -> list:
    return [(m, u) for (m, u, body) in log
            if any(n and (n in u or n in body) for n in needles)]


def sign_in_through_page(pg, app_url: str, identifier: str, password: str) -> str:
    """Sign in on /sign-in and return the token the app's own sign-in reply carries."""
    pg.goto(f"{app_url}/sign-in")
    pg.get_by_label("Email").fill(identifier)
    pg.get_by_label("Password", exact=True).fill(password)
    with pg.expect_response(
            lambda r: r.request.method == "POST"
            and r.url.split("?")[0].rstrip("/").endswith("/api/sessions"),
            timeout=PAGE_TIMEOUT_MS) as info:
        pg.get_by_role("button", name="Sign in").click()
    reply = info.value
    assert reply.status in OK, (
        f"signing in {identifier} through /sign-in answered {reply.status}; "
        f"body={reply.text()[:300]}")
    token = reply.json().get("token")
    assert token, f"the sign-in reply for {identifier} carries no token: {reply.text()[:300]}"
    pg.wait_for_url(re.compile(r".*/notes.*"), timeout=PAGE_TIMEOUT_MS)
    return token


def token_for(browser_handle, app_url: str, identifier: str) -> str:
    """A bearer token for a seeded account, signed in from a throwaway browser context."""
    context, pg = new_page(browser_handle)
    token = sign_in_through_page(pg, app_url, identifier, CORPUS_PASSWORD)
    context.close()
    return token


def create_note_through_page(pg, app_url: str, title: str, words: str) -> str:
    """Create a note on /notes/new, wait for the sealed save, return its uuid."""
    pg.goto(f"{app_url}/notes/new")
    pg.get_by_label("Title").fill(title)
    pg.get_by_label("Note body").fill(words)
    pg.get_by_role("button", name="Create note").click()
    pg.wait_for_url(re.compile(r".*/notes/[0-9A-Za-z-]{8,}$"), timeout=PAGE_TIMEOUT_MS)
    pg.get_by_text(SAVED_STATUS).first.wait_for(timeout=PAGE_TIMEOUT_MS)
    return pg.url.rstrip("/").rsplit("/", 1)[1]


def register_probe(api: str) -> dict:
    """A fresh account created straight through the API with opaque key material."""
    identifier = "probe-" + run_tag() + PROBE_DOMAIN
    secret = os.urandom(32).hex()
    params = {"version": "probe", "salt": os.urandom(16).hex(), "identifier": identifier}
    with appclient.client(None) as c:
        response = c.post(f"{api}/accounts", json={
            "identifier": identifier, "auth_secret": secret, "key_params": params})
    assert response.status_code in OK, (
        f"POST {api}/accounts for a fresh identifier answered {response.status_code}; "
        f"body={response.text[:300]}")
    body = response.json()
    assert body.get("token") and body.get("refresh_token"), (
        f"account creation returned no token pair: {response.text[:300]}")
    return {"identifier": identifier, "auth_secret": secret, "key_params": params,
            "token": body["token"], "refresh_token": body["refresh_token"]}


def sign_in_api(api: str, identifier: str, secret: str, device: str = "probe device"):
    with appclient.client(None) as c:
        return c.post(f"{api}/sessions", json={
            "identifier": identifier, "auth_secret": secret, "device": device})


def note_item(uid: str | None = None, version=None, envelope: str | None = None,
              content_type: str = "note", deleted: bool = False) -> dict:
    return {"uuid": uid or new_uuid(), "content_type": content_type,
            "envelope": opaque_envelope() if envelope is None else envelope,
            "version": version, "deleted": deleted}


def sync(client, api: str, items=(), cursor=None, limit: int = 150,
         request_id: str | None = None) -> dict:
    response = client.post(f"{api}/items/sync", json={
        "cursor": cursor, "limit": limit, "request_id": request_id or run_tag(),
        "items": list(items)})
    assert response.status_code in OK, (
        f"POST {api}/items/sync answered {response.status_code}; body={response.text[:400]}")
    return response.json()


def saved_version(reply: dict, uid: str):
    for entry in reply.get("saved_items") or []:
        if entry.get("uuid") == uid:
            return entry.get("version")
    return None


def conflict_for(reply: dict, uid: str) -> dict | None:
    for entry in reply.get("conflicts") or []:
        if entry.get("uuid") == uid:
            return entry
    return None


def pull_all(client, api: str, cursor=None, limit: int = PAGE_LIMIT) -> tuple:
    """Follow `more` from a cursor. Returns (every retrieved item, the final cursor)."""
    delivered: list = []
    for _ in range(1000):
        reply = sync(client, api, cursor=cursor, limit=limit)
        delivered.extend(reply.get("retrieved_items") or [])
        cursor = reply.get("cursor")
        if not reply.get("more"):
            return delivered, cursor
    raise AssertionError("sync kept reporting more after a thousand pages")


def get_item(client, api: str, uid: str):
    return client.get(f"{api}/items/{uid}")


def start_upload(client, api: str, uid: str, chunk_count: int):
    return client.post(f"{api}/files", json={"uuid": uid, "chunk_count": chunk_count})


def put_chunk(client, api: str, uid: str, index: int, data: bytes):
    return client.put(f"{api}/files/{uid}/chunks/{index}", content=data,
                      headers={"Content-Type": "application/octet-stream"})


def text_columns(backend) -> list:
    return backend.query(
        "SELECT table_name, column_name FROM information_schema.columns "
        "WHERE table_schema = 'public' AND data_type IN "
        "('text', 'character varying', 'character', 'json', 'jsonb')")


def rows_containing(backend, needle: str) -> list:
    """Every (table, column) in which some stored value contains the needle."""
    hits = []
    for row in text_columns(backend):
        table, column = row["table_name"], row["column_name"]
        found = backend.query(
            f'SELECT count(*) AS n FROM "{table}" WHERE CAST("{column}" AS text) LIKE %s',
            (f"%{needle}%",))
        if found and int(found[0]["n"]) > 0:
            hits.append((table, column))
    return hits
