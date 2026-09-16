from __future__ import annotations

import io
import os
import time

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"
STUDIO_EMAIL = "studio@example.com"
CLIENT_EMAIL = "client@example.com"
CLIENT2_EMAIL = "client2@example.com"
SEED_DOMAIN = "example.com"

PUBLISHED_CASE_SLUG = "northwind-aero"
SECOND_CASE_SLUG = "bridgeline-health"
UNPUBLISHED_CASE_SLUG = "token-market"
UNPUBLISHED_CASE_NAME = "Token Market"

BRIEF_KEY_PREFIX = "briefs/"
DELIVERABLE_KEY_PREFIX = "deliverables/"
ATTACHMENT_LIMIT_BYTES = 2 * 1024 * 1024

SECTORS = ("FINANCE", "TECHNOLOGY", "HEALTHCARE", "AGENCY", "ECOMMERCE")
KINDS = ("BRANDING", "WEB", "PRODUCT")
SHAPES = ("identity", "product", "build", "full-cycle")
DETAILS = ("overview", "standard", "deep")
SLOT_STATES = ("free", "held", "booked")
DIGESTS = ("Daily", "Weekly", "Off")
CHAPTER_TYPES = ("cover", "context", "figures", "still", "compare",
                 "sequence", "motion", "quote", "stack", "outcome")
SERVICE_NAMES = (
    "Logo Design", "Brand Identity Systems", "Corporate Identity",
    "User Experience Design", "UX Strategy", "User Interface Design",
    "UI Kits & Design Systems", "Product Design", "Custom Product Solutions",
    "Prototyping", "Graphic Design", "Marketing Graphics", "Illustrations",
    "Motion Design", "3D Modeling", "Frontend Development",
    "Backend Development", "DevOps & Architecture", "Product Analytics",
    "Creative Direction",
)
CAPABILITY_TITLES = ("Branding", "UX/UI Design", "Web & Development", "3D / Motion")
TONE_WORDS = ("Vision.", "Clarity.", "Flow.", "Execution.")
STUDIO_STRIP = ("FULL-CYCLE DIGITAL AGENCY", "EST. 2023", "Canada")
YEAR_MARK = "23-26"
DECK_CONTROL = "GET CAPABILITIES DECK"
ARCHIVE_HEADING = "Selected Cases"
WORK_HEADING = "The Archive"
LOADER_LABEL = "LOADING..."
TELEMETRY_NOTICE = "Whoever sent you this deck can see which pages were read."
NOT_PUBLISHED = "not published"
PUBLIC_ROUTES = ("/", "/contact/", "/privacy-policy/", "/terms/", "/work/",
                 "/brief/", "/deck/", "/login", "/signup")
PRIVACY_HEADINGS = ("Introduction", "What We Collect", "How We Use Your Information",
                    "File Uploads", "Cookies", "Data Storage", "Your Rights", "Contact")
NEW_COLLECTION_POINTS = ("brief", "slot", "deck", "tone", "portal")
SECRET_MARKERS = ("STORAGE_SECRET_KEY", "STORAGE_ACCESS_KEY", "DATABASE_URL",
                  "DB_ADMIN_URL", "postgres://", "postgresql://")
ABSENT_PHRASES = ("add to cart", "checkout", "start a chat", "new folder",
                  "connect your calendar", "follow this", "like this")
APP_ROOT = "/app"
SETTLE_DEADLINE = 20.0
SETTLE_INTERVAL = 0.25


def app_origin() -> str:
    return appclient.app_url()


def page(path: str, headers: dict | None = None) -> httpx.Response:
    """Fetch a route of the deployed app as a browser would."""
    return httpx.get(f"{app_origin()}{path}", timeout=appclient.TIMEOUT,
                     follow_redirects=False, headers=headers or {})


def page_body(path: str, headers: dict | None = None) -> str:
    response = page(path, headers=headers)
    assert response.status_code < 400, (
        f"GET {path} returned {response.status_code}: {response.text[:300]}")
    return response.text


def settle(predicate, what: str):
    """The one sanctioned bounded poll: poll to a deadline, never a bare sleep."""
    deadline = time.monotonic() + SETTLE_DEADLINE
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        time.sleep(SETTLE_INTERVAL)
    raise AssertionError(f"{what} did not settle within the deadline; last saw {last!r}")


def body(response: httpx.Response):
    if "json" in response.headers.get("content-type", "").lower():
        return response.json()
    return response.text


def is_client_error(status: int) -> bool:
    return 400 <= status < 500


def create_brief(api: httpx.Client, **fields) -> dict:
    payload = {
        "stage": 1,
        "contact": {"name": "Ada Reyes", "company": "Northwind Aero",
                    "email": CLIENT_EMAIL, "phone": "",
                    "current_site": ""},
        "disciplines": ["Brand Identity Systems", "Motion Design"],
    }
    payload.update(fields)
    response = api.post("/briefs", json=payload)
    assert response.status_code < 300, (
        f"POST /briefs returned {response.status_code}: {response.text[:300]}")
    record = response.json()
    assert record.get("token"), f"brief create returned no token: {record}"
    return record


def free_slots(api: httpx.Client) -> list[dict]:
    response = api.get("/availability")
    assert response.status_code == 200, (
        f"GET /availability returned {response.status_code}")
    payload = response.json()
    slots = payload.get("slots") if isinstance(payload, dict) else payload
    assert isinstance(slots, list), f"availability carried no slot list: {payload}"
    return [s for s in slots if s.get("state", "free") == "free"]


def attach(api: httpx.Client, token: str, size: int, name: str = "brief.pdf"):
    files = {"file": (name, io.BytesIO(b"x" * size), "application/pdf")}
    return api.post(f"/briefs/{token}/attachment", files=files)


def engagement_ids(api: httpx.Client) -> list[str]:
    response = api.get("/portal/engagements")
    assert response.status_code == 200, (
        f"GET /portal/engagements returned {response.status_code}")
    rows = response.json()
    assert isinstance(rows, list), f"engagement listing is not an array: {rows}"
    return [str(row["id"]) for row in rows]


def first_version_awaiting(api: httpx.Client, engagement: str) -> str:
    response = api.get(f"/portal/engagements/{engagement}")
    assert response.status_code == 200
    payload = response.json()
    for deliverable in payload.get("deliverables") or []:
        for version in deliverable.get("versions") or []:
            if not version.get("frozen"):
                return str(version["id"])
    raise AssertionError(f"engagement {engagement} carries no open version: {payload}")


@pytest.fixture(scope="session")
def db():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def anon():
    with appclient.client() as c:
        yield c


@pytest.fixture()
def studio():
    with appclient.client(appclient.login(STUDIO_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def client_a():
    with appclient.client(appclient.login(CLIENT_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def client_b():
    with appclient.client(appclient.login(CLIENT2_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def brief(anon):
    return create_brief(anon)
