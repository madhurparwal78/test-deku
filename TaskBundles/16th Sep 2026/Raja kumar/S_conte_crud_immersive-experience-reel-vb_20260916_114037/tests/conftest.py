"""Task fixtures for deku/immersive-experience-reel-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout
or module names. The only assumptions are the App Contract and the literals
instruction.md pins explicitly.

Provider agnostic: Mailpit is read over its own HTTP API and PostgreSQL through
capabilities.py, never through a provider SDK.
"""

from __future__ import annotations

import concurrent.futures
import os
import re
import threading
import time

import httpx
import pytest
from appclient import api_base, app_url
from capabilities import Backend, make_backend

TIMEOUT = 30.0
PASSWORD = "deku-demo-pw-2026"
ADMIN_EMAIL = "admin@example.com"
EDITOR_EMAIL = "editor@example.com"
PRODUCER_EMAIL = "producer@example.com"
PRODUCER2_EMAIL = "producer2@example.com"
STUDIO_QUEUE = "studio@example.com"
PRODUCER_ORGANISATION = "Northlight Agency"

INTENT_LINKS = [("-> games", "/work?category=games"),
                ("-> multiplayer", "/work?category=multiplayer"),
                ("-> XR / VR / AI", "/work?category=xr"),
                ("-> installations", "/work?category=installation"),
                ("-> websites", "/work?category=web")]
QUESTION = "What are you looking for?"
RECENT_ORDER = ["Secret Tide", "Tidal Cartography", "Harmonic Drift", "Frontier Beyond",
                "Renewable Frontiers", "Welcome to Stonehall", "E.D.E.N.",
                "20 Years of Nexus", "Discover your Familiar", "Million Tile Mission",
                "Andes 20", "Archimedes", "Chromatik", "Glass Planes", "Rally"]
TITLE_ORDER = ["20 Years of Nexus", "Andes 20", "Archimedes", "Chromatik",
               "Discover your Familiar", "E.D.E.N.", "Frontier Beyond", "Glass Planes",
               "Harmonic Drift", "Million Tile Mission", "Rally", "Renewable Frontiers",
               "Secret Tide", "Tidal Cartography", "Welcome to Stonehall"]
DRAFT_SLUG = "lantern-protocol"
DRAFT_TITLE = "Lantern Protocol"
SEEDED_REEL_TITLE = "Launch shortlist"
SEEDED_PITCH_REFERENCE = "PT-000001"
TRACK_TITLES = ["Slow Current", "Glass Harbour", "Night Relay", "Amber Field"]

NOT_FOUND_COPY = "We cannot find that."
NO_SCENE_BANNER = "Running without the full scene."
SIGNIN_FAILURE = "That email and password do not match."
RESET_MESSAGE = "If that address has an account, a reset link is on its way."
EXPIRED_LINK = "That link has expired. Ask for a new one."
EMAIL_TAKEN = "That email already has an account."
OWN_ROLE = "You cannot change your own role."
LAST_OWNER = "The last owner cannot be demoted."
ALREADY_ON_REEL = "That project is already on this reel."
REEL_ITEM_LIMIT = "A reel holds every project there is. Remove one to add another."
REEL_LIMIT = "You have ten reels. Rename or delete one."
REEL_SENT = "This reel has been sent. Withdraw the pitch to change it."
ORDER_INVALID = "The order must list every project on this reel exactly once."
NOTE_TOO_LONG = "A note holds up to five hundred characters."
CONFIRM_TITLE = "Type the reel title to delete it."
OPEN_PITCH_DELETE = "Withdraw the pitch before deleting this reel."
CHOOSE_BUDGET = "Choose a budget band."
CHOOSE_TIMEFRAME = "Choose a timeframe."
SUMMARY_SHORT = "Tell us a little more, at least twenty characters."
SUMMARY_LONG = "That is over two thousand characters."
CHOOSE_REPLY = "Choose how we should reply."
NOT_VERIFIED = "Confirm your email to send a pitch."
NO_ITEMS = "Add a project before sending this reel."
OPEN_PITCH_LIMIT = "You have five open pitches. We will get to them."
PITCH_CLOSED = "This pitch is closed to new messages."
PITCH_CHANGE = "That change is not allowed for this pitch."
MESSAGE_LIMIT = "That is a lot of messages. Try again shortly."
QUESTION_LIMIT = "That is a lot of questions. Try again shortly."
QUESTION_TOO_LONG = "Keep your question under five hundred characters."
ENQUIRY_LIMIT = "That is a lot of enquiries. Try again in an hour."
LINK_INVALID = "A project link starts with http or https and names a host."
EVENT_PROPERTY = "That event does not carry that property."

CONFIRM_SUBJECT = "Confirm your email"
RESET_SUBJECT = "Reset your password"
PITCH_RECEIPT = "We have your pitch"
PITCH_STUDIO = "New pitch from"
STUDIO_REPLIED = "The studio replied"
PITCH_WITHDRAWN = "Pitch withdrawn"
ENQUIRY_RECEIPT = "Your enquiry"
ENQUIRY_STUDIO = "Enquiry from"

CLIENT_ERRORS = (400, 401, 403, 404, 409, 422, 429)
LINK_RE = re.compile(r"https?://\S+")


def unique(prefix: str) -> str:
    return f"{prefix}-{os.urandom(5).hex()}"


def unique_email(prefix: str = "probe") -> str:
    return f"{unique(prefix)}@example.com"


def settle(seconds: float = 2.0) -> None:
    """The one sanctioned pause, for mail that lands out of band."""
    time.sleep(seconds)


def client(token: str | None = None) -> httpx.Client:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=headers)


def document(path: str) -> httpx.Response:
    return httpx.get(f"{app_url()}{path}", timeout=TIMEOUT, follow_redirects=False)


def rows_of(payload):
    if isinstance(payload, dict) and "items" in payload:
        return payload["items"]
    return payload


def error_of(response: httpx.Response) -> dict:
    body = response.json()
    assert isinstance(body, dict) and isinstance(body.get("error"), dict), (
        f"{response.request.method} {response.request.url} returned {response.status_code} "
        f"without the error body shape: {response.text[:300]}"
    )
    return body["error"]


def signin(email: str, password: str = PASSWORD) -> str:
    with client() as c:
        response = c.post("/auth/signin", json={"email": email, "password": password})
    assert response.status_code == 200, (
        f"signing in as {email} returned {response.status_code}: {response.text[:300]}"
    )
    token = response.json().get("access_token")
    assert token, f"signing in as {email} returned no access_token: {response.text[:300]}"
    return token


def signup(email: str, display_name: str = "Probe Person", organisation: str = "Probe Studio",
           password: str = "probe-password-2026") -> httpx.Response:
    with client() as c:
        return c.post("/auth/signup", json={"email": email, "display_name": display_name,
                                            "organisation": organisation, "password": password})


def _inbox() -> str:
    return os.environ["EMAIL_INBOX_API_URL"].rstrip("/")


def mails_to(address: str, subject_prefix: str = "") -> list[dict]:
    """Every message to one address whose subject starts with the prefix, newest first."""
    listing = httpx.get(f"{_inbox()}/messages", params={"limit": 2000}, timeout=TIMEOUT).json()
    found = []
    for item in listing.get("messages", []):
        recipients = [a.get("Address", "").lower() for a in item.get("To", [])]
        subject = item.get("Subject", "")
        if address.lower() in recipients and subject.startswith(subject_prefix):
            body = httpx.get(f"{_inbox()}/message/{item['ID']}", timeout=TIMEOUT).json()
            found.append({"subject": subject, "text": body.get("Text", "") or "",
                          "html": body.get("HTML", "") or "", "to": recipients,
                          "cc": body.get("Cc") or [], "bcc": body.get("Bcc") or []})
    return found


def wait_for_mails(address: str, subject_prefix: str, at_least: int = 1) -> list[dict]:
    found = []
    for _ in range(10):
        found = mails_to(address, subject_prefix)
        if len(found) >= at_least:
            break
        settle(1.0)
    return found


def token_from(mail: dict, route: str) -> str:
    match = re.search(re.escape(route) + r"\?token=([A-Za-z0-9._~%-]+)", mail["text"])
    assert match, f"the mail {mail['subject']!r} carries no {route}?token= link: {mail['text'][:300]}"
    return match.group(1)


def verified_producer(prefix: str) -> dict:
    email = unique_email(prefix)
    password = "probe-password-2026"
    created = signup(email, display_name="Probe Producer", organisation=unique("Probe Org"),
                     password=password)
    assert created.status_code == 201, f"sign up for {email} returned {created.status_code}: {created.text[:300]}"
    body = created.json()
    mails = wait_for_mails(email, CONFIRM_SUBJECT)
    assert mails, f"no {CONFIRM_SUBJECT!r} mail reached {email}"
    with client() as c:
        verified = c.post("/auth/verify", json={"token": token_from(mails[0], "/verify")})
    assert verified.status_code == 200, f"verifying {email} returned {verified.status_code}: {verified.text[:300]}"
    return {"email": email, "password": password, "token": body["access_token"],
            "organisation": body["account"]["organisation"]}


def projects(c: httpx.Client, **params) -> dict:
    response = c.get("/projects", params=params)
    assert response.status_code == 200, (
        f"GET /api/projects {params} returned {response.status_code}: {response.text[:300]}"
    )
    return response.json()


def titles(payload: dict) -> list[str]:
    return [row["title"] for row in rows_of(payload)]


PROJECT_IDS: dict = {}


def project_id(c: httpx.Client, slug: str) -> object:
    if slug not in PROJECT_IDS:
        response = c.get(f"/projects/{slug}")
        assert response.status_code == 200, f"GET /api/projects/{slug} returned {response.status_code}"
        PROJECT_IDS[slug] = response.json()["project"]["id"]
    return PROJECT_IDS[slug]


def new_reel(c: httpx.Client, title: str | None = None) -> dict:
    response = c.post("/reels", json={"title": title or unique("Probe reel")})
    assert response.status_code == 201, f"POST /api/reels returned {response.status_code}: {response.text[:300]}"
    return response.json()


def add_item(c: httpx.Client, reel: dict, slug: str) -> httpx.Response:
    return c.post(f"/reels/{reel['id']}/items",
                  json={"project_id": project_id(c, slug), "version": reel["version"]})


def reel_with(c: httpx.Client, slugs: list[str]) -> dict:
    reel = new_reel(c)
    for slug in slugs:
        response = add_item(c, reel, slug)
        assert response.status_code == 201, f"adding {slug} returned {response.status_code}: {response.text[:300]}"
        reel = response.json()
    return reel


def read_reel(c: httpx.Client, reel_id) -> dict:
    response = c.get(f"/reels/{reel_id}")
    assert response.status_code == 200, f"GET /api/reels/{reel_id} returned {response.status_code}: {response.text[:300]}"
    return response.json()


def pitch_body(reel: dict, **overrides) -> dict:
    body = {"reel_id": reel["id"], "budget_band": "50k-100k", "timing": "next-quarter",
            "summary": "A launch piece that feels like a place rather than a page",
            "contact_preference": "email"}
    body.update(overrides)
    return body


def set_project_state(slug: str, state: str) -> None:
    with client(signin(ADMIN_EMAIL)) as c:
        response = c.patch(f"/projects/{slug}", json={"state": state})
    assert response.status_code == 200, (
        f"the admin setting {slug} to {state} returned {response.status_code}: {response.text[:300]}"
    )


def at_once(calls):
    gate = threading.Barrier(len(calls))

    def fire(call):
        gate.wait()
        return call()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(calls)) as pool:
        return list(pool.map(fire, calls))


def warm(count: int, token: str | None = None) -> list[httpx.Client]:
    clients = [client(token) for _ in range(count)]
    for c in clients:
        c.get("/health")
    return clients


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


@pytest.fixture(scope="session")
def producer_token() -> str:
    return signin(PRODUCER_EMAIL)


@pytest.fixture(scope="session")
def producer2_token() -> str:
    return signin(PRODUCER2_EMAIL)


@pytest.fixture(scope="session")
def editor_token() -> str:
    return signin(EDITOR_EMAIL)


def plain_account(email: str, password: str = "probe-password-2026") -> dict:
    created = signup(email, display_name="Probe Producer", organisation=unique("Probe Org"),
                     password=password)
    assert created.status_code == 201, f"sign up for {email} returned {created.status_code}: {created.text[:300]}"
    body = created.json()
    return {"email": email, "folded": email.lower(), "password": password, "token": body["access_token"],
            "account": body["account"], "organisation": body["account"]["organisation"]}


@pytest.fixture(scope="session")
def reel_producer() -> dict:
    return verified_producer("reels")


@pytest.fixture(scope="session")
def pitch_producer() -> dict:
    return verified_producer("pitches")


@pytest.fixture(scope="session")
def fresh_account() -> dict:
    """Signed up with a mixed-case address and never verified by a fixture."""
    return plain_account(f"{unique('Probe-Case')}@Example.COM")


@pytest.fixture(scope="session")
def unverified_account() -> dict:
    return plain_account(unique_email("lock"), password="lock-password-2026")


@pytest.fixture(scope="session")
def role_account() -> dict:
    return plain_account(unique_email("role"))


@pytest.fixture(scope="session")
def _playwright():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as runtime:
        yield runtime


@pytest.fixture(scope="session")
def _chromium(_playwright):
    browser = _playwright.chromium.launch()
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def _chromium_without_render_context(_playwright):
    browser = _playwright.chromium.launch(args=["--disable-3d-apis", "--disable-webgl",
                                                "--disable-webgl2"])
    yield browser
    browser.close()


@pytest.fixture
def page(_chromium):
    context = _chromium.new_context(viewport={"width": 1440, "height": 900})
    tab = context.new_page()
    tab.set_default_timeout(15000)
    yield tab
    context.close()


@pytest.fixture
def browser_page(_chromium_without_render_context):
    context = _chromium_without_render_context.new_context(viewport={"width": 1440, "height": 900})
    tab = context.new_page()
    tab.set_default_timeout(15000)
    yield tab
    context.close()
