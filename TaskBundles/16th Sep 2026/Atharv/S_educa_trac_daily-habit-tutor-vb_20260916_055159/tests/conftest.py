from __future__ import annotations

import datetime as _dt
import os
import time
import urllib.parse

import httpx
import pytest

import appclient
import capabilities

APP_URL = None
API = None

PASSWORD = "deku-demo-pw-2026"

LEARNER_1 = "learner@example.com"
LEARNER_2 = "learner2@example.com"
LEARNER_3 = "learner3@example.com"

DISPLAY_NAMES = {
    LEARNER_1: "Nadia Fenn",
    LEARNER_2: "Bram Oduya",
    LEARNER_3: "Ines Caro",
}
TIMEZONES = {
    LEARNER_1: "Europe/Lisbon",
    LEARNER_2: "Africa/Nairobi",
    LEARNER_3: "America/Bogota",
}
COHORT_EMAILS = [f"learner{n}@example.com" for n in range(4, 14)]

OPEN_SUBJECTS = ["english", "chess", "math"]
PICKER_ORDER = [
    "English", "Chess", "Math", "Spanish", "French", "German", "Italian",
    "Portuguese", "Dutch", "Japanese", "Arabic", "Czech", "Welsh", "Danish",
    "Greek", "Esperanto", "Finnish", "Irish", "Scottish Gaelic", "Hebrew",
    "Hindi", "Haitian Creole", "Hungarian", "High Valyrian", "Hawaiian",
    "Indonesian", "Korean", "Latin", "Norwegian (Bokmal)", "Navajo", "Polish",
    "Romanian", "Russian", "Swedish", "Swahili", "Klingon", "Turkish",
    "Ukrainian", "Vietnamese", "Yiddish", "Chinese (Simplified)", "Zulu",
]
PICKER_COUNT = 42

ATTEMPT_STATES = ["correct", "correct_with_note", "incorrect", "skipped"]
TRACE_STATES = ["new", "learning", "review", "lapsed", "burned_in"]

LESSON_EXERCISES = 12
MAX_HEARTS = 5
REFILL_INTERVAL_SECONDS = 14400
RESUMABLE_SECONDS = 86400
REPAIR_WINDOW_SECONDS = 172800
REGRADE_WINDOW_SECONDS = 2592000
HALF_LIFE_MIN_SECONDS = 60
HALF_LIFE_MAX_SECONDS = 15768000
TARGET_RETENTION = 0.90
GRAMMAR_FORM_CEILING = 10000
DIFFICULTY_FREEZE_ATTEMPTS = 200
CLOCK_SKEW_SECONDS = 300
STALE_BOARD_SECONDS = 10
DAY_SHIFT_MAX_HOURS = 6
MAX_FREEZES = 2
COHORT_CAPACITY = 30
SEEDED_COHORT_SIZE = 12
PROMOTED = 7
DEMOTED = 5
TIED_POINTS = 150
COHORT_TIER = "Bronze"
TIERS = ["Copper", "Bronze", "Silver", "Gold", "Sapphire", "Ruby", "Emerald",
         "Amethyst", "Pearl", "Diamond"]

AWARD_LESSON = 10
AWARD_REVIEW = 6
AWARD_PRACTICE = 4
AWARD_PERFECT_BONUS = 5
AWARD_FIRST_OF_DAY_BONUS = 5

NADIA_STREAK = 4
NADIA_POINTS = 120
BRAM_POINTS = 180

UNITS_PER_SUBJECT = 3
LESSONS_PER_UNIT = 2
EXERCISES_PER_SUBJECT = 24

NOT_FOUND_TITLE = "Error 404"
HERO_PRIMARY = "GET STARTED"
HERO_SECONDARY = "I ALREADY HAVE AN ACCOUNT"
CLAIM_HEADINGS = ["free, fun, effective", "backed by science", "stay motivated",
                  "personalized learning"]
PLATFORM_HEADING = "learn anytime, anywhere"
STORE_SUBLABELS = ["Download on the", "Get it on"]
FOOTER_GROUPS = ["About us", "Products", "Apps", "Help and support",
                 "Privacy and terms", "Social"]
SESSION_COPY = ["Continue", "Skip", "Check"]
FEEDBACK_COPY = ["Nice!", "Correct solution:", "You have a typo",
                 "Pay attention to the accents"]
HEART_COPY = ["Full hearts", "Practice to earn hearts"]
STREAK_COPY = ["Streak freeze used", "Extend your streak"]
LEAGUE_COPY = ["Promotion zone", "Demotion zone"]

PUBLIC_ROUTES = ["/", "/feed", "/courses", "/terms", "/privacy",
                 "/community-guidelines", "/status", "/blog", "/preferences",
                 "/signup", "/login"]
LEARNER_ROUTES = ["/learn", "/history", "/profile", "/league", "/settings"]

CONTRAST_AA = 4.5
NARROW_VIEWPORT = {"width": 390, "height": 844}

MARKETING_FIRST_VIEW_BYTES = 1048576
BINARY_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".ico",
                   ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp3", ".wav",
                   ".ogg", ".mp4", ".webm", ".pdf", ".zip")

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


def today_utc() -> _dt.date:
    return _dt.datetime.now(_dt.timezone.utc).date()


def now_utc() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


def unique_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


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


def first_open_subject(client) -> dict:
    response = client.get("/courses", params={"open": "true"})
    assert response.status_code == 200, describe(response)
    body = json_of(response)
    assert isinstance(body, list), f"/api/courses must return a top-level array: {body!r}"
    opened = [c for c in body if c.get("is_open")]
    assert opened, f"no open subject in /api/courses: {body!r}"
    return opened[0]


def enrol(client, course_id: str, goal: int = 1):
    return client.post("/enrolments",
                       json={"course_id": course_id, "daily_goal_lessons": goal})


def first_lesson(client, course_id: str) -> tuple[str, str]:
    response = client.get(f"/path/{course_id}")
    assert response.status_code == 200, describe(response)
    units = json_of(response)
    assert isinstance(units, list) and units, f"empty path for {course_id}: {units!r}"
    unit = units[0]
    lessons = unit.get("lessons") or []
    assert lessons, f"unit {unit.get('id')!r} declares no lessons: {unit!r}"
    return unit["id"], lessons[0]["id"]


def start_session(client, course_id: str, kind: str = "lesson"):
    unit_id, lesson_id = first_lesson(client, course_id)
    return client.post("/sessions", json={"course_id": course_id, "unit_id": unit_id,
                                          "lesson_id": lesson_id, "kind": kind})


def attempts_for(session: dict, answer=lambda ex: ex.get("solution_canonical", "")):
    exercises = session.get("exercises") or []
    return [{"exercise_id": ex["id"], "presented_index": n,
             "answer_raw": answer(ex), "elapsed_ms": 4200}
            for n, ex in enumerate(exercises)]


def reconcile(client, session_id: str, attempts, offset_ms: int = 0):
    return client.post(f"/sessions/{session_id}/reconcile",
                       json={"attempts": attempts, "device_clock_offset_ms": offset_ms})


def signup(client, email: str, birth_year: int = 1994, timezone: str = "Europe/Lisbon"):
    return client.post("/auth/signup", json={"email": email, "password": PASSWORD,
                                             "display_name": "Probe Learner",
                                             "birth_year": birth_year,
                                             "timezone": timezone})


@pytest.fixture(scope="session")
def db():
    return capabilities.make_backend()


@pytest.fixture()
def anon():
    with appclient.client() as client:
        yield client


@pytest.fixture()
def learner():
    with appclient.client(token_for(LEARNER_1)) as client:
        yield client


@pytest.fixture()
def learner2():
    with appclient.client(token_for(LEARNER_2)) as client:
        yield client


@pytest.fixture()
def learner3():
    with appclient.client(token_for(LEARNER_3)) as client:
        yield client


@pytest.fixture()
def fresh():
    """A brand-new account, so a test never depends on another test's leftovers."""
    email = unique_email()
    with appclient.client() as client:
        created = signup(client, email)
        assert created.status_code in (200, 201), describe(created)
        token = json_of(created).get("access_token") or token_for(email)
    with appclient.client(token) as client:
        client.probe_email = email
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
