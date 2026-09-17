"""Task fixtures for deku/editorial-photography-exhibition-vb.

Implementation agnostic: nothing here assumes the framework, the file layout, an ORM
or a module name. What it assumes is the App Contract and what instruction.md pinned:
the routes, the camelCase API fields, the access_token login key, the seeded visitors,
the table and column names, the entry times, the capacity, the reservation code shape
and the confirmation subject prefix.

Provider agnostic where the capability layer allows: rows are read through the backend
capability and mail through the inbox capability, never through a provider SDK. The
full message detail (recipients, cc, bcc, text) comes from the inbox API the email slot
exposes to the verifier.
"""

from __future__ import annotations

import datetime
import os
import threading
import time

import httpx
import pytest
from appclient import api_base, app_url, client, login, seeded_password
from capabilities import Backend, Inbox, make_backend, make_inbox

SETTLE_SECONDS = 2.0
POLL_INTERVAL = 0.5
POLL_CEILING = 30.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned sleep: give an unwanted side effect time to land."""
    time.sleep(seconds)


SEEDED_PASSWORD = "deku-demo-pw-2026"
VISITOR_EMAIL = "visitor@example.com"
VISITOR2_EMAIL = "visitor2@example.com"
VISITOR3_EMAIL = "visitor3@example.com"
SEEDED_NAMES = (
    (VISITOR_EMAIL, "Nadia Rowe"),
    (VISITOR2_EMAIL, "Omar Lindgren"),
    (VISITOR3_EMAIL, "Hana Petrov"),
)

EXHIBITION_TITLE = "The New Hollywood Photography Exhibition"
VENUE = "Beacon Tower"
CITY = "New York City"
AURA_TITLE = "AURA: The New Hollywood"
GAZETTE_TITLE = "Gazette Goes to Hollywood"

PAGE_TITLES = (
    ("/", EXHIBITION_TITLE),
    ("/aura-intro", AURA_TITLE),
    ("/aura", AURA_TITLE),
    ("/gazette-intro", GAZETTE_TITLE),
    ("/gazette", GAZETTE_TITLE),
)
PUBLIC_ROUTES = ("/", "/aura-intro", "/aura", "/gazette-intro", "/gazette", "/visit",
                 "/signup", "/login", "/privacy", "/terms")

LOCKUP_WORDS = ("THE", "AURA", "Gazette", "HOLLYWOOD")
SUBTITLE_LINE_ONE = "As seen in the Beacon Tower, located in"
CHOOSER_PROMPT = "Choose which gallery you want to explore"
SCROLL_PROMPT = "Scroll to explore"

AURA_MANIFESTO = (
    "AURA has long been a partner for women in Hollywood, to connect, to provoke, to move the "
    "cultural needle. In these photographs, taken from 2018 to 2025, their growing power "
    "dominates every frame.",
    "The old binary, serious actress or brand-builder, artistic or commercial, has collapsed. "
    "In its place stands a new kind of force: the multihyphenate woman who shapes her own image "
    "and owns the infrastructure behind it.",
    "Performers like Odessa Vane, Lilou Marchetti and Priya Castellane no longer merely take "
    "roles: they choose them, develop them and use their visibility to elevate passion projects. "
    "Their legacy is built on craft, but also on never surrendering the narrative.",
)
GAZETTE_MANIFESTO = (
    "Gazette has spent decades writing about the men of Hollywood, to question them, to "
    "celebrate them, to take their measure. In these photographs, taken from 2018 to 2025, a "
    "different kind of leading man steps into the light.",
    "The old script, the tough guy or the heartthrob, the star or the character actor, has been "
    "torn up. In its place stands a performer who is allowed to be tender, strange and funny in "
    "the same frame, and who chooses which of those the camera sees.",
    "Actors like Rafe Okonkwo, Teodor Lindqvist and Marcus Delacroix-Bell no longer wait for the "
    "part to find them: they write it, produce it and carry it to the screen. Their legacy is "
    "built on range, and on the nerve to let an audience see them change.",
)

GALLERIES = (
    ("aura", "AURA", "serif", "dark", "white", 1, "Celine Armand"),
    ("gazette", "Gazette", "swash", "pale", "pink", 2, "Tomas Ekwueme"),
)

FRAMES = (
    ("aura", 1, "Odessa Vane", "Celine Armand", 2025, "portrait", "240x320"),
    ("aura", 2, "Lilou Marchetti", "Celine Armand", 2023, "landscape", "320x240"),
    ("aura", 3, "Priya Castellane", "Noor Haddad", 2021, "portrait", "280x320"),
    ("aura", 4, "Wren Adebayo", "Noor Haddad", 2019, "landscape", "320x200"),
    ("aura", 5, "Saskia Moreau", "Celine Armand", 2020, "portrait", "200x320"),
    ("aura", 6, "Ines Valcourt", "Jun Takeda", 2018, "landscape", "320x160"),
    ("gazette", 1, "Rafe Okonkwo", "Tomas Ekwueme", 2024, "portrait", "240x320"),
    ("gazette", 2, "Teodor Lindqvist", "Tomas Ekwueme", 2022, "landscape", "320x240"),
    ("gazette", 3, "Marcus Delacroix-Bell", "Ansel Varga", 2025, "portrait", "280x320"),
    ("gazette", 4, "Dario Fontaine", "Ansel Varga", 2019, "landscape", "320x200"),
    ("gazette", 5, "Kofi Brandt", "Tomas Ekwueme", 2021, "portrait", "200x320"),
    ("gazette", 6, "Elias Navarro", "Jun Takeda", 2018, "landscape", "320x160"),
)
CROPS = ("240x320", "320x240", "280x320", "320x200", "200x320", "320x160")

ENTRY_TIMES = ("10:00", "12:00", "14:00", "16:00", "18:00")
CAPACITY = 8
RUN_DAYS = 30
SLOT_COUNT = RUN_DAYS * len(ENTRY_TIMES)

SEED_RESERVATIONS = (
    ("SEEDA14B", VISITOR2_EMAIL, "14:00", 4, "Omar Lindgren"),
    ("SEEDC14D", VISITOR3_EMAIL, "14:00", 3, "Hana Petrov"),
    ("SEEDE16F", VISITOR2_EMAIL, "16:00", 4, "Omar Lindgren"),
    ("SEEDG16H", VISITOR3_EMAIL, "16:00", 4, "Hana Petrov"),
)
SEED_STARTED = ("SEEDP10Q", VISITOR3_EMAIL, "10:00", 2, "Hana Petrov")

SUBJECT_PREFIX = "Visit reserved:"
CONFIRMED = "confirmed"
CANCELLED = "cancelled"
PROBE_PASSWORD = "exhibit-probe-pw-2026"

MENU_LINKS = (
    ("AURA gallery", "/aura"),
    ("AURA introduction", "/aura-intro"),
    ("Gazette gallery", "/gazette"),
    ("Gazette introduction", "/gazette-intro"),
    ("Reserve a visit", "/visit"),
    ("Your selection", "/selection"),
    ("Privacy", "/privacy"),
    ("Terms", "/terms"),
)

GALLERY_FIELDS = {"id", "slug", "title", "wordmarkFace", "ground", "mastheadColour", "order"}
FRAME_FIELDS = {"id", "galleryId", "subject", "photographer", "publication", "year", "aspect", "crop", "order"}
SELECTION_FIELDS = {"frameId", "galleryId", "savedAt"}
SLOT_FIELDS = {"id", "startsAt", "capacity", "placesLeft", "status"}
RESERVATION_FIELDS = {"id", "slotId", "code", "status", "name", "email", "partySize", "startsAt"}
TABLES = ("visitors", "exhibitions", "galleries", "introductions", "frames", "slots", "reservations",
          "selections")
MENU_ROUTES = ("/aura", "/gazette", "/aura-intro", "/gazette-intro", "/visit", "/privacy", "/terms")
NARROW_WIDTH = 320
WIDE_WIDTH = 2560
NOT_FOUND_COPY = ("404", "Page Not Found", "You may have made a mistake.", "This page does not exist.")
PRIVACY_NOUNS = ("email address", "display name", "saved frames", "reservations")
TERMS_SENTENCE = "By creating an account you accept the Terms"
SOUND_OFF = "Sound: off"
SECRET_MARKERS = ("postgresql://", "deku-local-dev", "deku_admin", "SMTP_PASS", "pbkdf2_sha256$",
                  "$argon2", "$2b$")
DEBUG_MARKERS = ("Django tried these URL patterns", "Traceback (most recent call last)",
                 "DEBUG = True", "Using the URLconf")
ASSET_TYPES = ("image/", "font/", "audio/", "video/")
STYLE_FIELDS_JS = (
    "const st = getComputedStyle(best); "
    "return {size: parseFloat(st.fontSize), family: st.fontFamily, style: st.fontStyle, "
    "weight: String(st.fontWeight), numeric: st.fontVariantNumeric, features: st.fontFeatureSettings};"
)
LARGEST_EXACT_TEXT_JS = (
    "text => { let best = null, size = 0; for (const e of document.body.querySelectorAll('*')) { "
    "if (e.textContent.split(/[\\s\\u00a0]+/).join('') !== text) continue; "
    "const s = parseFloat(getComputedStyle(e).fontSize); if (s > size) { size = s; best = e; } } "
    "if (!best) return null; " + STYLE_FIELDS_JS + " }"
)
LARGEST_CONTAINING_TEXT_JS = (
    "text => { let best = null, size = 0; for (const e of document.body.querySelectorAll('*')) { "
    "if (!e.textContent.includes(text)) continue; "
    "const s = parseFloat(getComputedStyle(e).fontSize); if (s > size) { size = s; best = e; } } "
    "if (!best) return null; " + STYLE_FIELDS_JS + " }"
)
DEEPEST_TEXT_JS = (
    "text => { let best = null; for (const e of document.body.querySelectorAll('*')) { "
    "if (!e.textContent.split(/[\\s\\u00a0]+/).join(' ').includes(text)) continue; "
    "if (!best || best.contains(e)) best = e; } "
    "if (!best) return null; " + STYLE_FIELDS_JS + " }"
)
LOOPING_ANIMATIONS_JS = (
    "() => document.getAnimations().filter(a => a.playState === 'running' && a.effect "
    "&& a.effect.getTiming && a.effect.getTiming().iterations === Infinity).length"
)


def poll_until(predicate, ceiling: float = POLL_CEILING):
    """Bounded poll for an asynchronous side effect. Returns the last value seen."""
    deadline = time.monotonic() + ceiling
    value = predicate()
    while not value and time.monotonic() < deadline:
        settle(POLL_INTERVAL)
        value = predicate()
    return value


def unique_local() -> str:
    return f"probe-{os.urandom(6).hex()}"


def unique_email() -> str:
    return f"{unique_local()}@example.com"


def base_url() -> str:
    return app_url()


def page_url(route: str) -> str:
    return f"{app_url()}{route}"


def fetch_page(route: str) -> httpx.Response:
    return httpx.get(page_url(route), timeout=30.0, follow_redirects=True)


def signup(email: str | None = None, display_name: str | None = None,
           password: str = PROBE_PASSWORD) -> tuple[str, str]:
    """Create a fresh visitor through the public API and return (email, access_token)."""
    address = email or unique_email()
    name = display_name or f"Probe {os.urandom(3).hex()}"
    with client() as anon:
        response = anon.post("/auth/signup", json={
            "email": address, "password": password, "displayName": name})
    assert response.status_code in (200, 201), (
        f"POST /api/auth/signup for {address} returned {response.status_code}: "
        f"{response.text[:400]}")
    return address.lower(), login(address, password)


def me(token: str) -> dict:
    with client(token) as visitor:
        response = visitor.get("/me")
    assert response.status_code == 200, (
        f"GET /api/me returned {response.status_code}: {response.text[:400]}")
    return response.json()


def exhibition() -> dict:
    with client() as anon:
        response = anon.get("/exhibition")
    assert response.status_code == 200, (
        f"GET /api/exhibition returned {response.status_code}: {response.text[:400]}")
    return response.json()


def run_start() -> datetime.date:
    return datetime.date.fromisoformat(str(exhibition()["runStart"])[:10])


def tomorrow() -> datetime.date:
    """The UTC date after the app first started: the run starts the day before first start."""
    return run_start() + datetime.timedelta(days=2)


def all_slots() -> list[dict]:
    with client() as anon:
        response = anon.get("/slots")
    assert response.status_code == 200, (
        f"GET /api/slots returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    assert isinstance(body, list), f"GET /api/slots is not a top-level array: {response.text[:300]}"
    return body


def slot_date(slot: dict) -> str:
    return str(slot["startsAt"])[:10]


def slot_time(slot: dict) -> str:
    return str(slot["startsAt"])[11:16]


def slot_on(day: datetime.date, hhmm: str) -> dict:
    for slot in all_slots():
        if slot_date(slot) == day.isoformat() and slot_time(slot) == hhmm:
            return slot
    raise AssertionError(f"no entry time on {day.isoformat()} at {hhmm} in GET /api/slots")


def slot_by_id(slot_id) -> dict:
    for slot in all_slots():
        if str(slot["id"]) == str(slot_id):
            return slot
    raise AssertionError(f"entry time {slot_id} is missing from GET /api/slots")


def untouched_slot(skip: int = 0) -> dict:
    """An open entry time at least five days into the run with every place still free."""
    first_safe = (run_start() + datetime.timedelta(days=5)).isoformat()
    candidates = [s for s in all_slots()
                  if s.get("status") == "open" and int(s.get("placesLeft", -1)) == CAPACITY
                  and slot_date(s) >= first_safe]
    assert len(candidates) > skip, (
        "no untouched open entry time remains five days or more into the run")
    return candidates[skip]


def reservation_body(slot_id, party: int = 1, name: str = "Probe Guest",
                     email: str | None = None) -> dict:
    return {"name": name, "email": email or unique_email(), "partySize": party, "slotId": slot_id}


def reserve(token: str, body: dict) -> httpx.Response:
    with client(token) as visitor:
        return visitor.post("/reservations", json=body)


def confirmed_code(response: httpx.Response) -> dict:
    assert response.status_code in (200, 201), (
        f"POST /api/reservations returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    assert body.get("ok") is True, f"reservation response is not ok: {response.text[:400]}"
    reservation = body.get("reservation") or {}
    assert reservation.get("code"), f"reservation response carries no code: {response.text[:400]}"
    return reservation


def reserve_fresh(slot_id, party: int = 1, email: str | None = None) -> tuple[str, dict]:
    """Sign up a fresh visitor and confirm one reservation; returns (token, reservation)."""
    _, token = signup()
    return token, confirmed_code(reserve(token, reservation_body(slot_id, party, email=email)))


def fill_slot(slot_id, leave: int) -> None:
    """Confirm reservations from fresh visitors until exactly `leave` places remain."""
    remaining = int(slot_by_id(slot_id)["placesLeft"])
    while remaining > leave:
        party = min(4, remaining - leave)
        reserve_fresh(slot_id, party)
        remaining -= party
    assert int(slot_by_id(slot_id)["placesLeft"]) == leave, (
        f"entry time {slot_id} should have {leave} places left after filling")


def refusal(response: httpx.Response) -> dict:
    assert 400 <= response.status_code < 500, (
        f"expected a client-error refusal, got {response.status_code}: {response.text[:400]}")
    body = response.json()
    assert body.get("ok") is False, f"refusal body does not carry ok false: {response.text[:400]}"
    assert isinstance(body.get("message"), str) and body["message"].strip(), (
        f"refusal body carries no message: {response.text[:400]}")
    return body


def race(calls) -> list:
    """Run callables at the same instant behind a barrier and return their results."""
    barrier = threading.Barrier(len(calls))
    results = [None] * len(calls)

    def runner(index, call):
        barrier.wait()
        results[index] = call()

    threads = [threading.Thread(target=runner, args=(i, c)) for i, c in enumerate(calls)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=60)
    return results


def gallery(slug: str) -> dict:
    with client() as anon:
        response = anon.get(f"/galleries/{slug}")
    assert response.status_code == 200, (
        f"GET /api/galleries/{slug} returned {response.status_code}: {response.text[:400]}")
    return response.json()


def frame_id(subject: str) -> tuple:
    for slug in ("aura", "gazette"):
        for frame in gallery(slug).get("frames", []):
            if frame.get("subject") == subject:
                return frame["id"], slug
    raise AssertionError(f"seeded frame {subject} is missing from both galleries")


def save(token: str, frame, gallery_id: str, action: str = "add") -> httpx.Response:
    with client(token) as visitor:
        return visitor.post("/selection", json={
            "frameId": frame, "galleryId": gallery_id, "action": action})


def selection(token: str) -> list[dict]:
    with client(token) as visitor:
        response = visitor.get("/selection")
    assert response.status_code == 200, (
        f"GET /api/selection returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    assert isinstance(body, list), f"GET /api/selection is not a top-level array: {response.text[:300]}"
    return body


class ExhibitionStore:
    """Domain queries for this task, composed from the backend capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def visitor(self, email: str) -> dict | None:
        return self._b.one("visitors", email=email)

    def count_visitors(self, **where) -> int:
        return self._b.count("visitors", **where)

    def count(self, table: str, **where) -> int:
        return self._b.count(table, **where)

    def rows(self, table: str, limit: int | None = None, **where) -> list[dict]:
        return self._b.rows(table, limit=limit, **where)

    def reservation(self, code: str) -> dict | None:
        return self._b.one("reservations", code=code)

    def confirmed_places(self, slot_id) -> int:
        return sum(int(r.get("party_size") or 0)
                   for r in self._b.rows("reservations", slot_id=slot_id, status=CONFIRMED))


@pytest.fixture(scope="session")
def db() -> ExhibitionStore:
    return ExhibitionStore(make_backend())


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    return make_inbox()


INBOX_LIST_PATH = ("api", "v1", "messages")
INBOX_MESSAGE_PATH = ("api", "v1", "message")


class MailDetail:
    """Full message detail from the email slot's inbox API: recipients, cc, bcc, text."""

    def __init__(self) -> None:
        self._base = os.environ["EMAIL_INBOX_API_URL"].rstrip("/")

    def messages_to(self, address: str) -> list[dict]:
        response = httpx.get("/".join((self._base, *INBOX_LIST_PATH)), params={"limit": 500}, timeout=30.0)
        assert response.status_code == 200, (
            f"inbox listing returned {response.status_code}: {response.text[:300]}")
        found = []
        for item in response.json().get("messages", []):
            recipients = [str(a.get("Address", "")).lower() for a in item.get("To") or []]
            if address.lower() in recipients:
                found.append(item)
        return found

    def detail(self, message_id: str) -> dict:
        response = httpx.get("/".join((self._base, *INBOX_MESSAGE_PATH, str(message_id))), timeout=30.0)
        assert response.status_code == 200, (
            f"inbox message {message_id} returned {response.status_code}: {response.text[:300]}")
        return response.json()


@pytest.fixture(scope="session")
def mail() -> MailDetail:
    return MailDetail()


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def visitor_token() -> str:
    return login(VISITOR_EMAIL, seeded_password("SEED_VISITOR_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def visitor2_token() -> str:
    return login(VISITOR2_EMAIL, seeded_password("SEED_VISITOR2_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def chromium():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as driver:
        browser = driver.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(chromium):
    context = chromium.new_context(viewport={"width": 1280, "height": 900})
    surface = context.new_page()
    yield surface
    context.close()


def families(value: str) -> list[str]:
    return [part.strip().strip("\"'").lower() for part in str(value).split(",")]


def rendered(surface, script: str, text: str) -> dict:
    found = surface.evaluate(script, text)
    assert found, f"{surface.url} renders no element carrying the text {text!r}"
    return found


def menu_control(surface):
    return surface.get_by_role("button", name="Menu", exact=True).or_(
        surface.get_by_role("link", name="Menu", exact=True))


def sign_in_page(surface, email: str, password: str) -> None:
    """Sign in through the pinned sign-in form labels and wait to leave the login route."""
    surface.goto(page_url("/login"))
    surface.get_by_label("Email", exact=True).fill(email)
    surface.get_by_label("Password", exact=True).fill(password)
    surface.get_by_role("button", name="Sign in", exact=True).click()
    surface.wait_for_url(lambda url: "/login" not in url, timeout=20000)
