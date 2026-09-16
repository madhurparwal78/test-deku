"""Fixtures, pinned literals and helpers for the Modelport task.

Black-box only: HTTP against the running app, the rendered page through
Playwright, and PostgreSQL through the shared backend adapter. Nothing here reads
the agent's source.
"""

from __future__ import annotations

import concurrent.futures
import json
import math
import os
import re
import threading
import time
import uuid

import httpx
import pytest

import capabilities

TIMEOUT = 40.0
SETTLE_SECONDS = 0.5
TERMINAL_TIMEOUT = 45.0

PASSWORD = "deku-demo-pw-2026"
OWNER_EMAIL = "owner@example.com"
DEV_EMAIL = "member@example.com"
DEV2_EMAIL = "member2@example.com"

OWNER_HANDLE = "maren-vos"
DEV_HANDLE = "arden-hale"
DEV2_HANDLE = "vela-research"
ORG_HANDLE = "northlight"

SCRIBE = "northlight/scribe-2"
QUICKDRAW = "orchard/quickdraw-2"
PRISM = "blackpine-labs/prism-2-flex"
NOTES = "arden-hale/notes-tidy"

SCRIBE_VERSION = "8f1c0a4d"
SCRIBE_WITHDRAWN = "3b71e0c9"
QUICKDRAW_VERSION = "c41d7b20"
PRISM_VERSION = "5e09a3f6"
NOTES_VERSION = "9a2b61de"

WITHDRAWN_REASON = "Replaced by 8f1c0a4d, which fixes truncated summaries."

CPU_SMALL = "cpu-small"
CPU_LARGE = "cpu-large"
GPU = "gpu-a40"
RATES = {CPU_SMALL: 25, CPU_LARGE: 100, GPU: 1200}
DISPLAY_NAMES = {CPU_SMALL: "CPU (Small)", CPU_LARGE: "CPU (Large)", GPU: "GPU A40"}

SCRIBE_RUN_SECONDS = 4
NOTES_RUN_SECONDS = 2
QUICKDRAW_RATE_MICROS = 40000
PRISM_RATE_MICROS = 3750
PRISM_DIVISOR = 1000
PRISM_LOAD_SECONDS = 12
NOTES_LOAD_SECONDS = 2

FREE_ALLOWANCE_MICROS = 500000
DEFAULT_CAP_MICROS = 2000000
WARM_DAY_MICROS = 2160000
TOKEN_LIMIT = 20
ROTATION_GRACE_HOURS = 24
WAIT_CEILING_SECONDS = 60
RATE_LIMIT_PER_MINUTE = 60
LIST_LIMIT_DEFAULT = 25
LIST_LIMIT_MAX = 100
TOKEN_PREFIX = "mp_"
TOKEN_BODY_LENGTH = 40
PREDICTION_ID_LENGTH = 14
TOKEN_ENV_NAME = "MODELPORT_API_TOKEN"
COOKIE_CHOICE_NAME = "mp_cookie_choice"
PROMOTION_ID = "promo-autumn-2026"

STATUSES = ("starting", "processing", "succeeded", "failed", "canceled")
TERMINAL = ("succeeded", "failed", "canceled")

RESERVED_HANDLES = (
    "explore", "pricing", "enterprise", "docs", "blog", "changelog", "about",
    "terms", "privacy", "support", "status", "signin", "signup", "playground",
    "account", "settings", "dashboard", "predictions", "trainings",
    "deployments", "collections", "search", "api", "static", "assets", "home",
)

PUBLIC_ROUTES = (
    "/", "/explore", "/pricing", "/privacy", "/terms", "/signin", "/signup",
    "/search", "/collections/summarise-text", "/collections/structure-any-text",
    "/northlight", "/northlight/scribe-2", "/northlight/scribe-2/api",
    "/northlight/scribe-2/examples", "/northlight/scribe-2/readme",
    "/northlight/scribe-2/versions", "/orchard/quickdraw-2",
    "/blackpine-labs/prism-2-flex",
)

OK = (200, 201, 202)
REFUSED = tuple(range(400, 500))


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned pause, for a side effect the app applies asynchronously."""
    time.sleep(seconds)


def base_url() -> str:
    return os.environ["APP_PUBLIC_URL"].rstrip("/")


def api_base() -> str:
    return f"{base_url()}/api"


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}: {response.text[:400]}")


def unique(prefix: str = "probe") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


def body(response: httpx.Response):
    """The decoded body, or an empty mapping when the response carried none."""
    if "json" not in response.headers.get("content-type", ""):
        return {}
    text = response.text.strip()
    if not text:
        return {}
    return json.loads(text)


def error_type(response: httpx.Response) -> str:
    data = body(response)
    return str(data.get("type", "")) if isinstance(data, dict) else ""


def ok(response: httpx.Response, what: str):
    assert response.status_code in OK, f"{what} failed: {describe(response)}"
    return body(response)


def refused_as(response: httpx.Response, kind: str) -> None:
    assert response.status_code in REFUSED, \
        f"expected a client error refused as {kind}: {describe(response)}"
    assert error_type(response) == kind, \
        f"expected the error type {kind!r}: {describe(response)}"


def sign_in(email: str, password: str = PASSWORD) -> tuple[httpx.Client, str]:
    """A cookie session plus that session's CSRF value, as the brief pins them."""
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT, follow_redirects=False)
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code in OK, f"sign in for {email} failed: {describe(response)}"
    csrf = str(body(response).get("csrf_token") or "")
    assert csrf, f"sign in for {email} returned no csrf_token: {describe(response)}"
    client.headers["X-CSRF-Token"] = csrf
    return client, csrf


def mint_token(session: httpx.Client, scopes=("run",), name: str | None = None) -> str:
    created = ok(session.post("/tokens", json={"name": name or unique("probe-token"),
                                               "scopes": list(scopes)}),
                 "token creation")
    value = str(created.get("token") or "")
    assert value.startswith(TOKEN_PREFIX), \
        f"a minted token must begin {TOKEN_PREFIX!r}: {created}"
    return value


def client_for(token: str | None) -> httpx.Client:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=headers)


def bearer_for(email: str, scopes=("run", "read", "write", "admin")) -> str:
    session, _ = sign_in(email)
    with session:
        return mint_token(session, scopes)


def html_of(path: str, token: str | None = None) -> httpx.Response:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.get(f"{base_url()}{path}", timeout=TIMEOUT, headers=headers,
                     follow_redirects=True)


def create_prediction(client: httpx.Client, model: str, payload: dict,
                      headers: dict | None = None, **extra) -> httpx.Response:
    doc = {"model": model, "input": payload}
    doc.update(extra)
    return client.post("/predictions", json=doc, headers=headers or {})


def wait_terminal(client: httpx.Client, prediction_id: str,
                  timeout: float = TERMINAL_TIMEOUT) -> dict:
    deadline = time.monotonic() + timeout
    record = ok(client.get(f"/predictions/{prediction_id}"), "prediction read")
    while str(record.get("status")) not in TERMINAL and time.monotonic() < deadline:
        settle()
        record = ok(client.get(f"/predictions/{prediction_id}"), "prediction read")
    assert str(record.get("status")) in TERMINAL, \
        f"prediction {prediction_id} never reached a terminal status: {record}"
    return record


def run_now(client: httpx.Client, model: str, payload: dict) -> dict:
    created = ok(create_prediction(client, model, payload), f"create on {model}")
    identifier = str(created.get("id") or "")
    assert identifier, f"create on {model} returned no id: {created}"
    return wait_terminal(client, identifier)


def scribe_input(prompt: str | None = None, **over) -> dict:
    doc = {"prompt": prompt or "Summarise the quarterly report for a busy reader."}
    doc.update(over)
    return doc


def usage_rows(client: httpx.Client, **params) -> dict:
    return ok(client.get("/account/usage", params=params), "usage read")


def rows_of(report: dict) -> list:
    rows = report.get("rows")
    assert isinstance(rows, list), f"usage report carries no rows array: {report}"
    return rows


def row_for(report: dict, prediction_id: str) -> dict | None:
    for row in rows_of(report):
        if str(row.get("prediction_id")) == prediction_id:
            return row
    return None


def charge_for(quantity: int, rate_micros: int, divisor: int = 1) -> int:
    """The one billing formula the brief states, rounded up to a whole micro unit."""
    return math.ceil(quantity * rate_micros / divisor)


def run_together(*calls):
    """Start every call at the same instant and return their results in order."""
    gate = threading.Barrier(len(calls))

    def wrap(fn):
        gate.wait()
        return fn()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(calls)) as pool:
        futures = [pool.submit(wrap, fn) for fn in calls]
        return [f.result() for f in futures]


def head_of(path: str) -> str:
    response = html_of(path)
    assert response.status_code == 200, f"public route {path} is not served: {describe(response)}"
    text = response.text
    start = text.lower().find("<head")
    end = text.lower().find("</head>")
    return text[start:end] if start >= 0 and end > start else text


def meta_content(head: str, key: str, attribute: str = "name") -> str:
    pattern = re.compile(
        rf'<meta[^>]*{attribute}=["\']{re.escape(key)}["\'][^>]*content=["\']([^"\']*)["\']',
        re.I)
    other = re.compile(
        rf'<meta[^>]*content=["\']([^"\']*)["\'][^>]*{attribute}=["\']{re.escape(key)}["\']',
        re.I)
    found = pattern.search(head) or other.search(head)
    return found.group(1).strip() if found else ""


def table_rows(backend, table: str, **where) -> list:
    return backend.rows(table, **where)


def contrast(front: tuple, back: tuple) -> float:
    def channel(value):
        value = value / 255.0
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    def luminance(colour):
        r, g, b = (channel(c) for c in colour[:3])
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    light, dark = sorted((luminance(front), luminance(back)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def rgb_of(value: str) -> tuple:
    found = re.findall(r"[\d.]+", value or "")
    numbers = [float(n) for n in found[:3]]
    return tuple(int(round(n)) for n in numbers) if len(numbers) == 3 else (0, 0, 0)


@pytest.fixture(scope="session")
def app_url() -> str:
    return base_url()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture()
def dev() -> httpx.Client:
    with client_for(bearer_for(DEV_EMAIL)) as session:
        yield session


@pytest.fixture()
def dev2() -> httpx.Client:
    with client_for(bearer_for(DEV2_EMAIL)) as session:
        yield session


@pytest.fixture()
def owner() -> httpx.Client:
    with client_for(bearer_for(OWNER_EMAIL)) as session:
        yield session


@pytest.fixture()
def anon() -> httpx.Client:
    with client_for(None) as session:
        yield session


@pytest.fixture()
def dev_session():
    session, csrf = sign_in(DEV_EMAIL)
    with session:
        yield session


@pytest.fixture()
def owner_session():
    session, csrf = sign_in(OWNER_EMAIL)
    with session:
        yield session


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        chromium = pw.chromium.launch()
        yield chromium
        chromium.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    tab = context.new_page()
    yield tab
    context.close()


@pytest.fixture()
def narrow_page(browser):
    context = browser.new_context(viewport={"width": 390, "height": 844},
                                  has_touch=True, is_mobile=True)
    tab = context.new_page()
    yield tab
    context.close()
