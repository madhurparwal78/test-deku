"""Fixtures, pinned literals and helpers for the Sounding task.

Black-box only: HTTP against the running app, the rendered page through
Playwright, PostgreSQL through the shared backend adapter and the mail inbox
through the shared email adapter. Nothing here reads the agent's source.
"""

from __future__ import annotations

import concurrent.futures
import json
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
MAIL_TIMEOUT = 20.0

PASSWORD = "deku-demo-pw-2026"
HOST_EMAIL = "host@example.com"
DIVER_EMAIL = "diver@example.com"
DIVER2_EMAIL = "diver2@example.com"

HOST_NAME = "Ines Marlow"
DIVER_NAME = "Coral Bevan"
DIVER2_NAME = "Toma Oyelaran"

DEFAULT_TITLE = "Untitled dive"
PUBLISHED_TITLE = "Reef pitch"

SCENE_SLUGS = ("surface", "introduction", "about", "works", "message", "contact")
SCENE_COUNT = 6
PROJECT_SLUGS = ("tidal-atlas", "kelp-forest", "sonar-room", "drift-table")
PROJECT_TITLES = ("Tidal Atlas", "Kelp Forest", "Sonar Room", "Drift Table")
PROJECT_SKILLS = {
    "tidal-atlas": "HTML / CSS / JS / WEBGL",
    "kelp-forest": "HTML / CSS / JS / SHADERS",
    "sonar-room": "HTML / CSS / JS / WEB AUDIO",
    "drift-table": "HTML / CSS / JS / CANVAS",
}
WORKS_SCENE_INDEX = 3

ENTRY_CEILING = 12
NOTE_MAX = 280
TITLE_MIN = 1
TITLE_MAX = 80
DISPLAY_NAME_MAX = 60
EMAIL_MAX = 254
PASSWORD_MIN = 8
PASSWORD_MAX = 200
PUBLIC_ID_MIN_BITS = 128
PUBLIC_ID_MIN_CHARS = 22
SESSION_DAYS = 30
RESET_MINUTES = 60

SEEDED_PUBLISHED = (
    {"scene_index": 3, "progress": 0.62, "note": "The works arc is the whole argument"},
    {"scene_index": 1, "progress": 0.24, "note": "Read this line against the bright water"},
    {"scene_index": 5, "progress": 0.94, "note": "Ends on an address, not a loop"},
    {"scene_index": 2, "progress": 0.41, "note": "Thin on purpose"},
)
SEEDED_DRAFT = (
    {"scene_index": 0, "progress": 0.05},
    {"scene_index": 4, "progress": 0.78},
)

STATES = ("empty", "draft", "published", "answered")

SUBJECT_WELCOME = "Sounding: your logbook"
SUBJECT_RESET = "Sounding: reset your password"
SUBJECT_LIVE = "Sounding: your logbook is live"
SUBJECT_WAITING = "New logbook from "

COPY_NO_MOMENT = "Log at least one moment"
COPY_TOO_MANY = "A logbook holds twelve moments at most"
COPY_NO_TITLE = "Give the logbook a name"
COPY_NOTE_LONG = "A note is too long"
COPY_SCENE_GONE = "One of your moments is no longer in the dive"
COPY_ALREADY = "This logbook is already published"
COPY_BAD_LOGIN = "That email and password do not match"
COPY_TAKEN = "That email is already registered"
COPY_NOT_FOUND = "That address does not exist"
COPY_FORBIDDEN = "This logbook belongs to someone else"
COPY_FAILED = "Something went wrong down here"
COPY_SIGNED_OUT = "Sign in to keep a logbook"
COPY_EMPTY_LOG = "Nothing logged yet"
COPY_QUIET = "No logbooks published yet"
COPY_LOAD_FAILED = "Could not load this"

LABEL_WAIT = "[Please wait]"
LABEL_WELCOME = "[Welcome aboard]"
LABEL_SURFACE_LOG = "[Surface log]"
LABEL_RECEIVED = "[Received]"
LABEL_NO_DEPTH = "[No such depth]"
LABEL_NOT_YOURS = "[Not your logbook]"
LABEL_SIGNAL_LOST = "[Signal lost]"
LABEL_NO_LOG = "[No log]"
LABEL_EMPTY_LOG = "[Empty log]"
LABEL_QUIET = "[Quiet]"
LABEL_LOGGED = "[Logged]"
LABEL_FULL = "[Logbook full]"
LABEL_OFFLINE = "[Offline]"
LABEL_COPIED = "[Link copied]"
LABEL_REORDER_FAILED = "[Could not reorder]"
LABEL_DEAD_LINK = "[Unpublished. The link is dead]"
LABEL_PRESS_AGAIN = "[Press again]"
DESCEND_PROMPT = "[Scroll to descend]"

GATE_PRIMARY = "Dive into the experience"
GATE_SECONDARY = "Enter without audio"
INTRO_SENTENCE = "Ines Marlow is a Software Engineer"
SIGN_OFF = "Thanks for visiting"
CREDIT = "Development & 3D Design by Ines Marlow"
HEADER_WORDS = ("Works", "Message", "Contact")
REPLAY_LABEL = "Dive to this"

TITLES = {
    "/": "Ines Marlow // Creative Software Engineer & UI/UX Designer",
    "/works": "Works // Ines Marlow",
    "/sign-in": "Sign in - Ines Marlow",
    "/logbook": "Your logbook - Ines Marlow",
    "/dock": "Dock - Ines Marlow",
}
NOT_FOUND_TITLE = "Not found - Ines Marlow"

PUBLIC_ROUTES = ("/", "/works", "/sign-in")

ERROR_CODES = {
    "unauthenticated": 401,
    "forbidden": 403,
    "not_found": 404,
    "wrong_state": 409,
    "already_published": 409,
    "logbook_full": 422,
    "scene_missing": 422,
    "invalid": 422,
    "rate_limited": 429,
}

HOSTILE = "<img src=x onerror=alert(1)>"

OK = (200, 201, 202, 204)
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


def probe_email() -> str:
    return f"{unique('diver')}@example.com"


def body(response: httpx.Response):
    """The decoded body, or an empty mapping when the response carried none."""
    if "json" not in response.headers.get("content-type", ""):
        return {}
    text = response.text.strip()
    if not text:
        return {}
    return json.loads(text)


def error_code(response: httpx.Response) -> str:
    data = body(response)
    return str(data.get("code", "")) if isinstance(data, dict) else ""


def error_message(response: httpx.Response) -> str:
    data = body(response)
    return str(data.get("error", "")) if isinstance(data, dict) else ""


def ok(response: httpx.Response, what: str):
    assert response.status_code in OK, f"{what} failed: {describe(response)}"
    return body(response)


def refused_as(response: httpx.Response, code: str) -> None:
    expected = ERROR_CODES[code]
    assert response.status_code == expected, \
        f"expected {expected} refused as {code}: {describe(response)}"
    assert error_code(response) == code, \
        f"expected the error code {code!r}: {describe(response)}"


def new_client() -> httpx.Client:
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, follow_redirects=False)


def sign_in(email: str, password: str = PASSWORD) -> httpx.Client:
    """A cookie session, which is the only credential the brief pins."""
    client = new_client()
    response = client.post("/auth/sign-in", json={"email": email, "password": password})
    assert response.status_code in OK, f"sign in for {email} failed: {describe(response)}"
    return client


def sign_up(email: str | None = None, display_name: str | None = None,
            password: str = PASSWORD) -> tuple[httpx.Client, str]:
    client = new_client()
    address = email or probe_email()
    response = client.post("/auth/sign-up", json={
        "displayName": display_name or unique("Diver"),
        "email": address,
        "password": password,
    })
    assert response.status_code in OK, f"sign up for {address} failed: {describe(response)}"
    return client, address


def reopen(session: httpx.Client) -> httpx.Client:
    """A second client carrying the same session cookie, as a new tab would."""
    client = new_client()
    client.cookies.update(session.cookies)
    return client


def logbook_of(session: httpx.Client) -> dict:
    return ok(session.get("/logbook"), "logbook read")


def entries_of(session: httpx.Client) -> list:
    payload = logbook_of(session)
    rows = payload.get("entries")
    assert isinstance(rows, list), f"the logbook carries no entries array: {payload}"
    return rows


def entry_ids(session: httpx.Client) -> list:
    return [str(row.get("id")) for row in entries_of(session)]


def save_moment(session: httpx.Client, scene_index: int = WORKS_SCENE_INDEX,
                progress: float = 0.5, note: str | None = None) -> httpx.Response:
    doc = {"sceneIndex": scene_index, "progress": progress}
    if note is not None:
        doc["note"] = note
    return session.post("/logbook/entries", json=doc)


def fill(session: httpx.Client, count: int) -> list:
    """Save `count` moments, spread across scenes and depths, and return the ids."""
    made = []
    for index in range(count):
        created = ok(save_moment(session, index % SCENE_COUNT, round(0.05 + index * 0.07, 2)),
                     f"save moment {index}")
        made.append(str(created.get("entry", {}).get("id") or created.get("id") or ""))
    return made


def reorder(session: httpx.Client, order: list) -> httpx.Response:
    return session.put("/logbook/order", json={"order": order})


def publish(session: httpx.Client) -> httpx.Response:
    return session.post("/logbook/publish")


def unpublish(session: httpx.Client) -> httpx.Response:
    return session.post("/logbook/unpublish")


def rename(session: httpx.Client, title: str) -> httpx.Response:
    return session.patch("/logbook", json={"title": title})


def annotate(session: httpx.Client, entry_id: str, note: str) -> httpx.Response:
    return session.patch(f"/logbook/entries/{entry_id}", json={"note": note})


def published_logbook(session: httpx.Client, title: str | None = None,
                      moments: int = 3) -> str:
    """A freshly published logbook on a new account, returning its public address."""
    fill(session, moments)
    ok(rename(session, title or unique("Dive")), "rename")
    payload = ok(publish(session), "publish")
    public = str(payload.get("logbook", {}).get("publicId")
                 or payload.get("publicId") or "")
    assert public, f"publish returned no publicId: {payload}"
    return public


def read_public(public_id: str, session: httpx.Client | None = None) -> httpx.Response:
    client = session or httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    return client.get(f"/logbook/public/{public_id}")


def html_of(path: str, session: httpx.Client | None = None) -> httpx.Response:
    cookies = session.cookies if session is not None else None
    return httpx.get(f"{base_url()}{path}", timeout=TIMEOUT, cookies=cookies,
                     follow_redirects=True)


def raw_get(path: str, session: httpx.Client | None = None) -> httpx.Response:
    cookies = session.cookies if session is not None else None
    return httpx.get(f"{base_url()}{path}", timeout=TIMEOUT, cookies=cookies,
                     follow_redirects=False)


def head_of(path: str) -> str:
    response = html_of(path)
    assert response.status_code == 200, f"public route {path} is not served: {describe(response)}"
    text = response.text
    start = text.lower().find("<head")
    end = text.lower().find("</head>")
    return text[start:end] if start >= 0 and end > start else text


def title_of(path: str) -> str:
    found = re.search(r"<title[^>]*>(.*?)</title>", head_of(path), re.I | re.S)
    return found.group(1).strip() if found else ""


def meta_content(head: str, key: str, attribute: str = "name") -> str:
    pattern = re.compile(
        rf'<meta[^>]*{attribute}=["\']{re.escape(key)}["\'][^>]*content=["\']([^"\']*)["\']',
        re.I)
    other = re.compile(
        rf'<meta[^>]*content=["\']([^"\']*)["\'][^>]*{attribute}=["\']{re.escape(key)}["\']',
        re.I)
    found = pattern.search(head) or other.search(head)
    return found.group(1).strip() if found else ""


def wait_for_mail(inbox, to: str, subject: str, timeout: float = MAIL_TIMEOUT):
    deadline = time.monotonic() + timeout
    message = inbox.find(to=to, subject_contains=subject)
    while message is None and time.monotonic() < deadline:
        settle()
        message = inbox.find(to=to, subject_contains=subject)
    return message


def run_together(*calls):
    """Start every call at the same instant and return their results in order."""
    gate = threading.Barrier(len(calls))

    def wrap(fn):
        gate.wait()
        return fn()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(calls)) as pool:
        futures = [pool.submit(wrap, fn) for fn in calls]
        return [f.result() for f in futures]


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


def enter_dive(tab, path: str = "/", audio: bool = False) -> None:
    """Load the dive and pass the entry gate, which every dive surface sits behind."""
    tab.goto(f"{base_url()}{path}", wait_until="domcontentloaded")
    label = GATE_PRIMARY if audio else GATE_SECONDARY
    tab.get_by_text(label, exact=False).first.click(timeout=TIMEOUT * 1000)
    tab.wait_for_timeout(1200)


@pytest.fixture(scope="session")
def app_url() -> str:
    return base_url()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def inbox():
    return capabilities.make_inbox()


@pytest.fixture()
def anon() -> httpx.Client:
    with httpx.Client(base_url=api_base(), timeout=TIMEOUT) as session:
        yield session


@pytest.fixture()
def diver() -> httpx.Client:
    with sign_in(DIVER_EMAIL) as session:
        yield session


@pytest.fixture()
def diver2() -> httpx.Client:
    with sign_in(DIVER2_EMAIL) as session:
        yield session


@pytest.fixture()
def host() -> httpx.Client:
    with sign_in(HOST_EMAIL) as session:
        yield session


@pytest.fixture()
def fresh() -> httpx.Client:
    session, _ = sign_up()
    with session:
        yield session


@pytest.fixture()
def fresh2() -> httpx.Client:
    session, _ = sign_up()
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


@pytest.fixture()
def reduced_page(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900},
                                  reduced_motion="reduce")
    tab = context.new_page()
    yield tab
    context.close()
