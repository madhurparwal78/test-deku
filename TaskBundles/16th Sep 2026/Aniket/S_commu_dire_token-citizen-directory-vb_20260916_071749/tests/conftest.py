from __future__ import annotations

import os
import time
import uuid

import httpx
import pytest
from playwright.sync_api import sync_playwright

from capabilities import make_backend, make_store

APP_URL = os.environ.get("APP_PUBLIC_URL", "http://localhost:4173").rstrip("/")
API = f"{APP_URL}/api"

CORPUS_PASSWORD = "deku-demo-pw-2026"
MEMBER_EMAIL = "member@example.com"
SECOND_MEMBER_EMAIL = "member2@example.com"
THIRD_MEMBER_EMAIL = "member3@example.com"

MEMBER_ADDRESS = "0xA7d3F1b2C4e5D6a7B8c9D0e1F2a3B4c5D6e7F801"
SECOND_MEMBER_ADDRESS = "0xB2c4E5d6F7a8B9c0D1e2F3a4B5c6D7e8F9a0B102"
EMPTY_MEMBER_ADDRESS = "0xC3d5F6a7B8c9D0e1F2a3B4c5D6e7F8a9B0c1D203"

TOKEN_COUNT = 10000
TRAIT_COUNT = 13
TOKEN_ID_SHIFT = 5022
IDENTIFIER_EXAMPLES = ((0, 4978), (5022, 0), (5021, 9999), (9999, 4977))

TRAIT_NAMES = ("Ear", "Entity", "Eyes", "Face", "Hair", "Headgear", "Hand",
               "Innerwear", "Mouth", "Neck", "Outerwear", "Special", "Tattoo")
TRAIT_VALUE_COUNTS = {"Ear": 12, "Entity": 2, "Eyes": 35, "Face": 38,
                      "Hair": 51, "Headgear": 34, "Hand": 12, "Innerwear": 41,
                      "Mouth": 27, "Neck": 11, "Outerwear": 56, "Special": 47,
                      "Tattoo": 7}

PASSPORT_FACES = ("document_front", "document_back", "share_image")
RENDER_STATES = ("pending", "ready", "failed")
ACHIEVEMENT_KINDS = ("mark", "badge")
ACHIEVEMENT_DIFFICULTIES = ("standard", "rare", "elite")
CITIZEN_STATUSES = ("active", "suspended", "deleted")

NICKNAME_MAX = 24
BIO_MAX = 280

MEDIA_TOTAL = 71
MEDIA_IMAGE = 31
MEDIA_VIDEO = 34
MEDIA_AUDIO = 6
MEDIA_KINDS = ("image", "video", "audio")

JOURNAL_CATEGORIES = ("updates", "community", "finders_lab")
JOURNAL_TABS = ("ALL", "UPDATES", "COMMUNITY", "FINDERS LAB")

CONSOLE_INTERNAL_COMMAND = "connect_citizens"
COLLECTION_TAB = "KEEPERS COLLECTION"
HOLDINGS_TAB = "MY COLLECTION"
COLLECTION_COUNT_LABEL = "10000 KEEPERS"
SEARCH_PLACEHOLDER = "SEARCH BY ID..."
CLEAR_ALL_LABEL = "CLEAR ALL"
SIGN_IN_LABEL = "SIGN IN"
CONNECT_LABEL = "CONNECT WALLET"
DISCONNECT_LABEL = "DISCONNECT"
AUDIO_ENABLE_LABEL = "CLICK TO ENABLE SOUND"
AUDIO_MUTE_LABEL = "CLICK TO MUTE SOUND"
FOOTER_CONNECT_LABEL = "CONNECT ON"
FOOTER_STUDIO = "SITE BY Studio North"
FOOTER_RIGHTS = "KEEPERS OF THE REACH. ALL RIGHTS RESERVED."
REGISTRATION_TITLE = "THE HOLD CITIZEN BUREAU"
REGENERATING_LABEL = "UPDATING YOUR DOCUMENTS."
NO_HOLDINGS_LABEL = "THIS WALLET HOLDS NONE OF THE COLLECTION YET."
FORBIDDEN_MESSAGE = "You can only change your own page."
NOT_FOUND_MESSAGE = "Nothing here. Check the address and try again."
STORY_SUBMENU = ("Project", "The Hold", "Factions", "The World")
PROTOCOL_SUBMENU = ("VISION", "WORLD", "CHARACTERS", "PORTAL", "UNION")

ERROR_CODES = ("session_required", "session_address_mismatch",
               "citizen_not_found", "nickname_taken", "nickname_invalid",
               "bio_too_long", "token_not_owned", "address_already_bound",
               "challenge_expired", "rate_limited", "ledger_unavailable",
               "render_in_flight")

PUBLIC_ROUTES = ("/", "/protocol", "/gallery", "/filters", "/journal", "/media",
                 "/about", "/mint", "/legal/terms-of-service",
                 "/legal/privacy-policy", "/legal/legal-license")
PRIVACY_ROUTE = "/legal/privacy-policy"
HARNESS_ROUTE = "/render-asset"

PASSPORT_KEY_PREFIX = "citizens/"
CATALOGUE_KEY_PREFIX = "catalogue/"

NARROW_VIEWPORT = {"width": 390, "height": 844}
SETTLE_SECONDS = 0.5
SETTLE_ATTEMPTS = 40


def settle(seconds: float = SETTLE_SECONDS) -> None:
    time.sleep(seconds)


def poll(predicate, attempts: int = SETTLE_ATTEMPTS):
    last = None
    for _ in range(attempts):
        last = predicate()
        if last:
            return last
        settle()
    return last


def probe_email() -> str:
    return f"probe-{uuid.uuid4().hex[:10]}@example.com"


def probe_nickname() -> str:
    return f"probe {uuid.uuid4().hex[:8]}"


def probe_address() -> str:
    return "0x" + uuid.uuid4().hex + uuid.uuid4().hex[:8]


def anchor(label: str, response: httpx.Response) -> str:
    body = response.text[:400] if response.text else ""
    return (f"{label}: {response.request.method} {response.request.url} "
            f"answered {response.status_code} with body {body!r}")


def on_chain_id(display_id: int) -> int:
    return ((display_id - TOKEN_ID_SHIFT) % TOKEN_COUNT + TOKEN_COUNT) % TOKEN_COUNT


@pytest.fixture(scope="session")
def api_base() -> str:
    return API


@pytest.fixture(scope="session")
def app_url() -> str:
    return APP_URL


@pytest.fixture()
def client():
    with httpx.Client(base_url=API, timeout=30.0, follow_redirects=False) as c:
        yield c


@pytest.fixture()
def site():
    with httpx.Client(base_url=APP_URL, timeout=30.0, follow_redirects=True) as c:
        yield c


def sign_in(client: httpx.Client, email: str, password: str = CORPUS_PASSWORD) -> str:
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code in (200, 201), anchor(f"sign in for {email}", r)
    token = r.json().get("token")
    assert token, anchor(f"sign in for {email} returned no token", r)
    return token


def bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def sign_up(client: httpx.Client, email: str) -> str:
    r = client.post("/auth/signup", json={"email": email,
                                          "password": CORPUS_PASSWORD})
    assert r.status_code in (200, 201), anchor(f"signup for {email}", r)
    token = r.json().get("token")
    assert token, anchor(f"signup for {email} returned no token", r)
    return token


@pytest.fixture()
def member_token(client) -> str:
    return sign_in(client, MEMBER_EMAIL)


@pytest.fixture()
def second_member_token(client) -> str:
    return sign_in(client, SECOND_MEMBER_EMAIL)


@pytest.fixture()
def third_member_token(client) -> str:
    return sign_in(client, THIRD_MEMBER_EMAIL)


@pytest.fixture()
def fresh_token(client) -> str:
    return sign_up(client, probe_email())


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as driver:
        engine = driver.chromium.launch()
        yield engine
        engine.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context()
    sheet = context.new_page()
    yield sheet
    context.close()


@pytest.fixture(scope="session")
def db():
    return make_backend()


@pytest.fixture(scope="session")
def storage():
    return make_store()


def request_challenge(client: httpx.Client, token: str, address: str) -> dict:
    r = client.post("/session/challenge", json={"address": address},
                    headers=bearer(token))
    assert r.status_code in (200, 201), anchor(f"challenge for {address}", r)
    return r.json()


def verify_challenge(client: httpx.Client, token: str, address: str,
                     nonce: str) -> httpx.Response:
    return client.post("/session/verify",
                       json={"address": address, "nonce": nonce},
                       headers=bearer(token))


def patch_profile(client: httpx.Client, token: str, address: str,
                  payload: dict) -> httpx.Response:
    return client.patch(f"/citizens/{address}/profile", json=payload,
                        headers=bearer(token))


def read_citizen(client: httpx.Client, address: str,
                 token: str | None = None) -> httpx.Response:
    headers = bearer(token) if token else {}
    return client.get(f"/citizens/{address}", headers=headers)
