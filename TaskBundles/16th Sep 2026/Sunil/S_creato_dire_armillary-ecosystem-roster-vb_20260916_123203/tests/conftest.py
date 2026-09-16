from __future__ import annotations

import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"
CURATOR = "curator@example.com"
CREATOR = "creator@example.com"
CREATOR_SECOND = "creator2@example.com"
SEEDED_ACCOUNTS = ((CURATOR, "curator", "Ines Marlow"), (CREATOR, "creator", "Juno Okafor"),
                   (CREATOR_SECOND, "creator", "Ada Moreau"))

HEADLINE = "The Operating System for the Creator Economy"
MISSION_LINE = "Our purpose is to shorten the road back to human."
WORDMARK_NAME = "Halden"

DIVISIONS = (
    ("creator-media", "Creator Media", "red", "The new media empires will start with a person.",
     "PEOPLE ARE THE PLATFORM", "The people behind the platform", "disc-stack"),
    ("creator-communities", "Creator Communities", "green",
     "Audiences become communities when somebody gives them a home.", "BELONGING AT SCALE",
     "The people who host them", "sphere-ring"),
    ("creator-products", "Creator Products", "blue",
     "The best products start with the people who already use them.", "MADE WITH CREATORS",
     "The people who make them", "nested-boxes"),
    ("creator-tech", "Creator Tech", "yellow", "We build the engine that powers the person.",
     "ENGINEERING THE ECOSYSTEM", "The people who build it", "rippled-sphere"),
)
DIVISION_SLUGS = tuple(d[0] for d in DIVISIONS)
DISCIPLINES = (
    ("analytics", "Analytics"), ("discovery", "Discovery"), ("audience-insights", "Audience Insights"),
    ("presenting", "Presenting"), ("producing", "Producing"), ("writing", "Writing"),
    ("directing", "Directing"), ("design", "Design"), ("community", "Community"),
    ("commerce", "Commerce"), ("partnerships", "Partnerships"), ("engineering", "Engineering"),
)
UNUSED_DISCIPLINE = "partnerships"
TECH_PRODUCTS = (
    ("Signal Desk", "Less Noise, Better Work."),
    ("Roster Graph", "See who your audience already follows."),
    ("Brief Engine", "One message in, one brief out."),
    ("Payline", "Paid the day the work is approved."),
)

SEEDED_LIVE = (
    ("juno-okafor", "Juno Okafor", "creator-media"),
    ("amara-voss", "Amara Voss", "creator-media"),
    ("theo-lindqvist", "Theo Lindqvist", "creator-media"),
    ("priya-castellano", "Priya Castellano", "creator-media"),
    ("sol-ferreira", "Sol Ferreira", "creator-communities"),
    ("hana-petrova", "Hana Petrova", "creator-communities"),
    ("remy-achebe", "Remy Achebe", "creator-products"),
    ("kenji-aldana", "Kenji Aldana", "creator-tech"),
    ("mara-oyelaran", "Mara Oyelaran", "creator-tech"),
    ("felix-brandt", "Felix Brandt", "creator-tech"),
)
SEEDED_LIVE_SLUGS = tuple(s[0] for s in SEEDED_LIVE)
JUNO_STATEMENT = ("Juno hosts Backstage Hours, a weekly long-form interview show about the working "
                  "lives of independent musicians, and writes the letter that follows every episode.")
DRAFT_SLUG = "ada-moreau"
PORTRAIT_ORIGIN = "https://media.example.com/portraits/"
STATES = ("applying", "draft", "submitted", "changes_requested", "published", "unpublished")
LINK_KINDS = ("site", "photo", "network", "social", "audio", "document")
EVENT_NAMES = ("site_opened", "division_entered", "roster_filtered", "profile_opened", "apply_submitted",
               "profile_submitted", "profile_published", "profile_moved", "mode_toggled", "sketch_toggled")
PAGE_SIZE = 24

MSG_NAME = "Give us your name."
MSG_STATEMENT = "Eighty characters at least. Tell us what you do."
MSG_PASSWORD = "Passwords are at least twelve characters."
MSG_EMAIL = "That address does not look right."
MSG_LINKS = "Give us one place to see your work."
MSG_DIVISION = "Pick a part of the ecosystem."
MSG_DISCIPLINES = "Pick between one and four."
MSG_DUPLICATE = "That address already has an account."
MSG_UNCONFIRMED = "Confirm your address first."
MSG_PICTURE = "We need a picture."
MSG_LINK_URL = "That link does not look right."
MSG_PLACEHOLDER = "Something in there is still a placeholder."
MSG_NOTE = "Say what needs changing."

SUBJECT_CONFIRM = "Confirm your address"
SUBJECT_RETURNED = "Your entry needs a change"
SUBJECT_PUBLISHED = "You are on the roster"
SUBJECT_TAKEN_DOWN = "Your entry has been taken down"

NOTICES = (("terms", "Terms & Conditions"), ("privacy", "Privacy Policy"), ("cookies", "Cookies"))

NARROW_VIEWPORT = {"width": 390, "height": 844}
WIDE_VIEWPORT = {"width": 1440, "height": 900}
TABLET_VIEWPORT = {"width": 820, "height": 1180}

SETTLE_SECONDS = 1.0
MAIL_BUDGET_SECONDS = 30.0
ARRIVAL_BUDGET_MS = 45000
MAILPIT_V1 = "api/v1"


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned sleep."""
    time.sleep(seconds)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def deadline_after(seconds: float) -> float:
    return time.monotonic() + seconds


def before(deadline: float) -> bool:
    return time.monotonic() < deadline


def parse_moment(value) -> datetime:
    text = str(value).strip().replace("Z", "+00:00")
    moment = datetime.fromisoformat(text)
    assert moment.tzinfo is not None, f"timestamp {value!r} carries no UTC offset"
    return moment.astimezone(timezone.utc)


def probe_token() -> str:
    return os.urandom(5).hex()


def probe_email(prefix: str) -> str:
    return f"{prefix}-{probe_token()}@example.com"


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url.path} -> "
            f"{response.status_code}: {response.text[:500]}")


def is_success(response: httpx.Response) -> bool:
    return 200 <= response.status_code < 300


def json_object(response: httpx.Response, label: str) -> dict:
    assert is_success(response), f"{label} did not succeed: {describe(response)}"
    body = response.json()
    assert isinstance(body, dict), f"{label} must answer a JSON object: {response.text[:300]}"
    return body


def error_body(response: httpx.Response, status: int, token: str, label: str) -> dict:
    assert response.status_code == status, f"{label} expected {status}: {describe(response)}"
    body = response.json()
    assert isinstance(body, dict), f"{label} error is not a JSON object: {response.text[:300]}"
    assert body.get("error") == token, f"{label} expected error token {token!r}: {response.text[:300]}"
    return body


def raw_get(route: str) -> httpx.Response:
    return httpx.get(f"{appclient.app_url()}{route}", timeout=appclient.TIMEOUT, follow_redirects=False)


def statement_for(token: str) -> str:
    return (f"Probe {token} records field sounds on long coastal walks and edits them into "
            f"quiet half-hour pieces for listeners who work late.")


def application_body(email: str, name: str, division: str = "creator-media", **overrides) -> dict:
    body = {
        "email": email,
        "password": "probe-pass-2026-long",
        "name": name,
        "division": division,
        "disciplines": ["producing", "writing"],
        "statement": statement_for(probe_token()),
        "links": [{"kind": "site", "label": "Work", "url": "https://www.example.com/probe"}],
        "consent": True,
    }
    body.update(overrides)
    return body


def apply(body: dict) -> httpx.Response:
    with appclient.client() as session:
        return session.post("/applications", json=body)


def run_together(calls) -> list:
    barrier = threading.Barrier(len(calls))

    def fire(call):
        barrier.wait()
        return call()

    with ThreadPoolExecutor(max_workers=len(calls)) as pool:
        futures = [pool.submit(fire, call) for call in calls]
        return [f.result() for f in futures]


def mailpit_base() -> str:
    return os.environ["EMAIL_INBOX_API_URL"].rstrip("/")


def mail_to(address: str) -> list[dict]:
    response = httpx.get(f"{mailpit_base()}/{MAILPIT_V1}/messages", params={"limit": 1000}, timeout=30.0)
    assert response.status_code == 200, f"mail inbox unreadable: {response.status_code}"
    found = []
    for item in response.json().get("messages", []):
        recipients = [a.get("Address", "").lower() for a in item.get("To") or []]
        if address.lower() in recipients:
            found.append(item)
    return found


def mail_text(message_id: str) -> str:
    response = httpx.get(f"{mailpit_base()}/{MAILPIT_V1}/message/{message_id}", timeout=30.0)
    assert response.status_code == 200, f"mail message {message_id} unreadable: {response.status_code}"
    body = response.json()
    return f"{body.get('Text') or ''}\n{body.get('HTML') or ''}"


def wait_for_mail(address: str, subject: str) -> dict:
    deadline = deadline_after(MAIL_BUDGET_SECONDS)
    matches = [m for m in mail_to(address) if m.get("Subject") == subject]
    while not matches and before(deadline):
        settle(0.5)
        matches = [m for m in mail_to(address) if m.get("Subject") == subject]
    assert matches, f"no mail with subject {subject!r} reached {address} within {MAIL_BUDGET_SECONDS}s"
    return matches[0]


def count_mail(address: str, subject: str | None = None) -> int:
    return sum(1 for m in mail_to(address) if subject is None or m.get("Subject") == subject)


def confirmation_token(address: str) -> str:
    message = wait_for_mail(address, SUBJECT_CONFIRM)
    text = mail_text(message["ID"])
    match = re.search(r"/verify\?token=([A-Za-z0-9_.~%-]+)", text)
    assert match, f"the confirmation mail to {address} carries no /verify?token= link: {text[:300]}"
    return match.group(1)


def login(email: str, password: str) -> httpx.Response:
    with appclient.client() as session:
        return session.post("/auth/login", json={"email": email, "password": password})


def token_for(email: str, password: str) -> str:
    return json_object(login(email, password), f"sign in for {email}")["access_token"]


def new_creator(division: str = "creator-media", confirm: bool = True, name: str | None = None) -> dict:
    token = probe_token()
    email = probe_email("creator")
    body = application_body(email, name or f"Probe Creator {token}", division)
    created = apply(body)
    assert created.status_code == 201, f"application failed: {describe(created)}"
    if confirm:
        with appclient.client() as session:
            verified = session.post("/accounts/verifications", json={"token": confirmation_token(email)})
        assert verified.status_code == 204, f"confirmation failed: {describe(verified)}"
    access = token_for(email, body["password"])
    profile = created.json().get("profile") or {}
    return {"email": email, "password": body["password"], "token": access, "name": body["name"],
            "slug": profile.get("slug"), "body": body}


def own_profile(session: httpx.Client) -> dict:
    return json_object(session.get("/me/profile"), "GET /api/me/profile")


def complete_profile(session: httpx.Client, slug: str) -> dict:
    profile = own_profile(session)
    patched = session.patch("/me/profile", json={"portrait_url": f"{PORTRAIT_ORIGIN}{slug}.jpg",
                                                  "version": profile["version"]})
    return json_object(patched, "PATCH /api/me/profile portrait")


def transition_own(session: httpx.Client, to: str) -> httpx.Response:
    profile = own_profile(session)
    return session.post("/me/profile/transitions", json={"to": to, "version": profile["version"]})


def studio_profile(curator: httpx.Client, slug: str, state: str = "submitted") -> dict:
    listed = json_object(curator.get("/profiles", params={"state": state}), "curator state list")
    for row in listed.get("items", []):
        if row.get("slug") == slug:
            return row
    raise AssertionError(f"{slug} is not in the curator list for state {state}: {str(listed)[:300]}")


def version_of(backend, slug: str) -> int:
    row = backend.one("profiles", slug=slug)
    assert row is not None, f"no profiles row for {slug}"
    return int(row["version"])


def studio_transition(curator: httpx.Client, backend, slug: str, to: str, **extra) -> httpx.Response:
    body = {"to": to, "version": version_of(backend, slug)}
    body.update(extra)
    return curator.post(f"/profiles/{slug}/transitions", json=body)


def published_creator(backend, curator: httpx.Client, division: str = "creator-media") -> dict:
    creator = new_creator(division)
    with appclient.client(creator["token"]) as session:
        complete_profile(session, creator["slug"])
        submitted = transition_own(session, "submitted")
        assert submitted.status_code == 200, f"submission failed: {describe(submitted)}"
    published = studio_transition(curator, backend, creator["slug"], "published")
    assert published.status_code == 200, f"publish failed: {describe(published)}"
    return creator


def live_slugs(session: httpx.Client, **params) -> list[str]:
    slugs, page = [], 1
    while True:
        body = json_object(session.get("/profiles", params={**params, "page": page}), "GET /api/profiles")
        items = body.get("items", [])
        slugs += [row.get("slug") for row in items]
        if len(slugs) >= int(body.get("total", 0)) or not items:
            return slugs
        page += 1


def division_roster(session: httpx.Client, slug: str, **params) -> list[str]:
    body = json_object(session.get(f"/divisions/{slug}", params=params), f"GET /api/divisions/{slug}")
    return [row.get("slug") for row in body.get("roster", [])]


def account_id(backend, email: str):
    row = backend.one("accounts", email=email.lower())
    assert row is not None, f"no accounts row for {email}"
    return row["id"]


def event_kinds(backend, slug: str) -> list[str]:
    profile = backend.one("profiles", slug=slug)
    assert profile is not None, f"no profiles row for {slug}"
    return [row["kind"] for row in backend.rows("profile_events", profile_id=profile["id"])]


def site_event_count(backend) -> int:
    return int(backend.query("SELECT count(*) AS n FROM site_events")[0]["n"])


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def inbox():
    return capabilities.make_inbox()


@pytest.fixture
def anon():
    with appclient.client() as session:
        yield session


@pytest.fixture
def curator():
    with appclient.client(appclient.login(CURATOR, PASSWORD)) as session:
        yield session


@pytest.fixture
def creator():
    with appclient.client(appclient.login(CREATOR, PASSWORD)) as session:
        yield session


@pytest.fixture
def creator_second():
    with appclient.client(appclient.login(CREATOR_SECOND, PASSWORD)) as session:
        yield session


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as driver:
        launched = driver.chromium.launch()
        yield launched
        launched.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(viewport=WIDE_VIEWPORT)
    tab = context.new_page()
    yield tab
    context.close()


@pytest.fixture
def narrow_page(browser):
    context = browser.new_context(viewport=NARROW_VIEWPORT)
    tab = context.new_page()
    yield tab
    context.close()


def open_route(tab, route: str):
    response = tab.goto(f"{appclient.app_url()}{route}", wait_until="domcontentloaded")
    assert response is not None, f"navigating to {route} produced no response"
    tab.wait_for_selector('html[data-arrival="done"]', state="attached", timeout=ARRIVAL_BUDGET_MS)
    return response


STORED_JS = "(key) => window.localStorage.getItem(key) ?? window.sessionStorage.getItem(key)"


def page_metrics(tab) -> dict:
    return tab.evaluate("""() => ({
        scrollHeight: document.documentElement.scrollHeight,
        innerHeight: window.innerHeight,
        scrollWidth: document.documentElement.scrollWidth,
        innerWidth: window.innerWidth,
    })""")
