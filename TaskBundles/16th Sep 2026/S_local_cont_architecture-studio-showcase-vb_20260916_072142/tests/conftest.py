from __future__ import annotations

import datetime as _dt
import os
import time
import urllib.parse

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"

EDITOR_1 = "editor@example.com"
EDITOR_2 = "editor2@example.com"
READER = "reader@example.com"

DISPLAY_NAMES = {
    EDITOR_1: "Anton Norrgaard",
    EDITOR_2: "Marta Eklund",
    READER: "Petra Lindqvist",
}
ROLES = {EDITOR_1: "editor", EDITOR_2: "editor", READER: "reader"}

PUBLISHED_PROJECTS = [
    ("Pokrovskoe Private House", 611, "611 m2"),
    ("Millenium Private Park", 1360, "1,360 m2"),
    ("Bolshevik Residential", 8200, "8,200 m2"),
    ("KNS Stolbovo", 3345, "3,345 m2"),
    ("Kotelnaya Kinetics", 16488, "16,488 m2"),
    ("Vision Mansion", 991, "991 m2"),
    ("Almaty Hotel Ornament Stone", 58079, "58,079 m2"),
    ("Eli House Corner Plot", 435, "435 m2"),
    ("Riverside Restaurant", 1226, "1,226 m2"),
    ("Peredelki Mansion", 334, "334 m2"),
]
DRAFT_PROJECTS = [("Vantaa Timber Pavilion", 2140), ("Ostuni Cliff House", 780)]
PROJECT_COUNT = 12
PUBLISHED_COUNT = 10
DRAFT_COUNT = 2

TEAM_COUNT = 20
OFFICE_COUNT = 15
GALLERY_COUNT = 9
LEGAL_COUNT = 8
GALLERY_PER_PROJECT = 3

FOUNDER = "Anton Norrgaard"
FIRST_TEAM_ROLE = "Art director"
LAST_TEAM_MEMBER = "Livia Novak"
FIRST_OFFICE = ("Head office", "Italy", "Rome", "45 Casa di Maydwell Via Thomas")

LEGAL_CHAPTERS = [
    ("01", "Founding & Vision"), ("02", "Scope of Work"), ("03", "Design Philosophy"),
    ("04", "Sustainability"), ("05", "From Sketch to Strategy"),
    ("06", "Recognition & Reach"), ("07", "Global Presence"), ("08", "About This Site"),
]

VIEW_MODES = ["Grid", "List", "Gallery"]
DEFAULT_VIEW_MODE = "List"

REFERENCE_LENGTH = 12
ENQUIRY_RATE_LIMIT = 3
ENQUIRY_RATE_WINDOW_SECONDS = 3600
TOKEN_LIFETIME_SECONDS = 86400

ARC_FRAME_COUNT = 9
ARC_SWEEP_DEGREES = 120
ARC_RADIUS_RATIO = 1.4
ARC_TILT_STEP_DEGREES = 7

NAV_LINKS = ["Index", "Work", "About", "Contact"]
FOOTER_NAV = ["Index", "About", "Work", "Team", "Contact", "Order design"]
FOOTER_MEDIA = ["Behance", "Pinterest", "Telegram", "WhatsApp", "Phone", "Email", "Channel"]
FOOTER_IDENTITY = "Norrgaard Architectural Bureau"
FOOTER_HOURS = ["Mon to Fri 10:00 AM, 7:00 PM", "Sat to Sun 12:00 PM, 5:00 PM"]
LICENCES = ["IT-AR-2023-15847", "NL-BA-08576321"]
CREDITS = ["Luca Serrano", "Kai Andersen"]
ADDRESSES = ["Via Giacomo Leopardi 14, 20123, Milano Italia",
             "Keizersgracht 421, 1016, Amsterdam Netherlands"]
CONTACT_EMAILS = ["support@norrgaard.com", "info@norrgaard.com", "sales@norrgaard.com"]

HERO_WORDS = ["Norrgaard", "Architectural", "Bureau", "Systematic", "Clarity", "&",
              "Creativity"]
HOME_STATEMENTS = ["Refined & Bold Essential", "From Sketch to Strategy",
                   "15+ Years of experience"]
STATISTICS = ["490+ Completed projects", "45+ Professionals on the team"]
AWARD_SUMMARY = "Over 80+ awards in global competitions"
PUBLICATION_SUMMARY = "Over 20+ publications in the last year"
CARD_ACTION = "Visit"
NOT_FOUND_HEADING = "Page doesn't exist"
NOT_FOUND_LINE = "please return to the home page"

PUBLIC_ROUTES = ["/", "/work", "/about", "/contact", "/legal", "/signup", "/login"]
EDITOR_ROUTES = ["/studio", "/studio/enquiries"]
READER_ROUTES = ["/account"]

OBJECT_PREFIXES = {"cover": "projects", "gallery": "projects", "team": "team",
                   "photo": "gallery"}

CONTRAST_AA = 4.5
NARROW_VIEWPORT = {"width": 390, "height": 844}

BINARY_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".ico", ".woff",
                   ".woff2", ".ttf", ".otf", ".eot", ".mp3", ".wav", ".ogg", ".mp4",
                   ".webm", ".ktx2", ".wasm", ".pdf", ".zip")

POLL_SECONDS = 10.0
POLL_INTERVAL = 0.25


def settle(predicate, seconds: float = POLL_SECONDS, interval: float = POLL_INTERVAL):
    """Bounded poll. The only sanctioned sleep in the suite."""
    deadline = time.monotonic() + seconds
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        time.sleep(interval)
    return last


def now_utc() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


def unique_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


def unique_slug() -> str:
    return f"probe-{os.urandom(6).hex()}"


def app_url() -> str:
    return appclient.app_url()


def api_base() -> str:
    return appclient.api_base()


def absolute(path: str) -> str:
    return urllib.parse.urljoin(app_url() + "/", path.lstrip("/"))


def describe(response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}: {response.text[:400]}")


def token_for(email: str) -> str:
    return appclient.login(email, PASSWORD)


def json_of(response):
    assert response.headers.get("content-type", "").startswith("application/json"), (
        f"expected a JSON body, got {response.headers.get('content-type')!r}: "
        f"{describe(response)}")
    return response.json()


def store_url(object_key: str) -> str:
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    bucket = os.environ["STORAGE_BUCKET"]
    return f"{endpoint}/{bucket}/{object_key}"


def fetch_object_anonymously(object_key: str):
    with httpx.Client(timeout=30.0) as client:
        return client.get(store_url(object_key))


def enquiry_body(**overrides):
    payload = {"name": "Probe Client", "email": unique_email(),
               "message": "We are planning a civic building and would like to talk.",
               "company": ""}
    payload.update(overrides)
    return payload


def published_projects(client):
    response = client.get("/projects")
    assert response.status_code == 200, describe(response)
    body = json_of(response)
    assert isinstance(body, list), f"/api/projects must return a top-level array: {body!r}"
    return body


def draft_projects(editor_client):
    response = editor_client.get("/projects", params={"include": "drafts"})
    assert response.status_code == 200, describe(response)
    body = json_of(response)
    return [p for p in body if not p.get("is_published")]


def create_project(editor_client, **overrides):
    payload = {"slug": unique_slug(), "title": "Probe Pavilion", "area_sqm": 1200,
               "category": "Civic", "body": "A probe project.", "order": 99}
    payload.update(overrides)
    return editor_client.post("/projects", json=payload)


def add_image(editor_client, project_id, **overrides):
    payload = {"kind": "cover", "ratio": 1.5, "alt_text": "A grey render placeholder.",
               "seed": os.urandom(4).hex(), "order": 0}
    payload.update(overrides)
    return editor_client.post(f"/projects/{project_id}/images", json=payload)


@pytest.fixture(scope="session")
def db():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def anon():
    with appclient.client() as client:
        yield client


@pytest.fixture()
def editor():
    with appclient.client(token_for(EDITOR_1)) as client:
        yield client


@pytest.fixture()
def editor2():
    with appclient.client(token_for(EDITOR_2)) as client:
        yield client


@pytest.fixture()
def reader():
    with appclient.client(token_for(READER)) as client:
        yield client


@pytest.fixture()
def fresh():
    """A brand-new reader account, so a test never depends on another test's leftovers."""
    email = unique_email()
    with appclient.client() as client:
        created = client.post("/auth/signup", json={"email": email, "password": PASSWORD,
                                                    "display_name": "Probe Reader"})
        assert created.status_code in (200, 201), describe(created)
        token = json_of(created).get("access_token") or token_for(email)
    with appclient.client(token) as client:
        yield client


@pytest.fixture()
def page():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as play:
        browser = play.chromium.launch()
        context = browser.new_context()
        sheet = context.new_page()
        yield sheet
        context.close()
        browser.close()


@pytest.fixture()
def raw():
    with httpx.Client(base_url=app_url(), timeout=30.0,
                      follow_redirects=False) as client:
        yield client
