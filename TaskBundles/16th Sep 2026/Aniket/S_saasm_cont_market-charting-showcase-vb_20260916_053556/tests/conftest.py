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
AUTHOR_EMAIL = "author@example.com"
SECOND_AUTHOR_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"
AUTHOR_NAME = "Dana Holt"
SECOND_AUTHOR_NAME = "Priya Raman"
READER_NAME = "Sam Okafor"

PUBLISHED_IDEA = "Gold Breakout Watch"
SECOND_PUBLISHED_IDEA = "Yen Carry Unwind"
DRAFT_IDEA = "Copper Squeeze Setup"
PUBLISHED_IDEA_SYMBOL = "XAUUSD"
DRAFT_IDEA_SYMBOL = "HG1!"

IDEA_STATUSES = ("draft", "published")
IDEA_BIASES = ("long", "short")
TICK_DIRECTIONS = ("up", "down")
MARKET_SESSIONS = ("open", "closed", "holiday")

MARKET_SUMMARY_FIELDS = ("symbol", "value", "unit", "change", "direction",
                         "session", "timestamp")
PRIMARY_SYMBOL = "SPX"
PRIMARY_SYMBOL_NAME = "S&P 500"
PRIMARY_SYMBOL_UNIT = "POINT"
INDEX_SYMBOLS = ("NDX", "NI225", "000001", "UKX", "DAX", "PX1")
CRYPTO_SYMBOLS = ("TOTAL", "BTCUSD", "ETHUSD")
RATE_SYMBOLS = ("DXY", "CL1!", "NG1!")
SEEDED_SYMBOLS = (PRIMARY_SYMBOL,) + INDEX_SYMBOLS + CRYPTO_SYMBOLS + RATE_SYMBOLS

MARKET_SUMMARY_TITLE = "Market summary"
MATRIX_TITLE = "Track and trade all major asset classes"
ASSET_CLASS_TABS = ("Equity indices", "Metals", "Micro futures and options",
                    "Interest rates", "Energy", "Cryptocurrency", "FX",
                    "Agriculture", "ESG")
METRIC_LABELS = ("Average daily volume", "Average daily notional volume",
                 "Open Interest")
FUTURES_PRICE_DISPLAY = "591 INR per month"
FUTURES_PRICE_NOTE = "for non-professional subscribers only"
SUBSCRIBE_LABEL = "Subscribe"
FUTURES_HERO_SUBLINE = ("Highly liquid futures markets mean oh-so-many more "
                        "possibilities.")

HEADER_MENU = ("Products", "Community", "Markets", "Brokers", "More")
SEARCH_PLACEHOLDER = "Search"
OFFER_LABEL = "Get started"
HERO_ACTION = "Get started for free"
HERO_SUBHEADLINE = "The best trades require research, then commitment."
HERO_REASSURANCE = "$0 forever, no credit card needed"
SECTION_TITLE = "Where the world does markets"
SECTION_SUBTITLE = ("Join 100 million traders and investors taking the future "
                    "into their own hands.")
FEATURE_CHIPS = ("US stocks", "Crypto", "Futures", "Forex", "Economy", "Brokers")
FOOTER_BADGE = "Made by humans"
NOT_FOUND_WORD = "coordinates"
NOT_FOUND_ACTION = "Set course for home"

SCRIPTING_LANGUAGE = "Beamscript"
CHARTS_PRODUCT = "Powercharts"
EXCHANGE_PARTNER = "CXE Group"
DISPLAY_FONT = "Onest"
CAPABILITY_MARKERS = ("charting engine", SCRIPTING_LANGUAGE,
                      "real-time global market data", "backtesting engine",
                      "social", "sync")

PUBLIC_ROUTES = ("/", "/markets", "/futures", "/platform", "/ideas")
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


def anchor(label: str, response: httpx.Response) -> str:
    body = response.text[:400] if response.text else ""
    return (f"{label}: {response.request.method} {response.request.url} "
            f"answered {response.status_code} with body {body!r}")


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


@pytest.fixture()
def author_token(client) -> str:
    return sign_in(client, AUTHOR_EMAIL)


@pytest.fixture()
def second_author_token(client) -> str:
    return sign_in(client, SECOND_AUTHOR_EMAIL)


@pytest.fixture()
def reader_token(client) -> str:
    return sign_in(client, READER_EMAIL)


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


def make_draft(client: httpx.Client, token: str, title: str) -> dict:
    payload = {"title": title, "thesis": "A seeded thesis for the drafted idea.",
               "symbol": DRAFT_IDEA_SYMBOL, "bias": "long", "tags": ["probe"]}
    r = client.post("/ideas", json=payload, headers=bearer(token))
    assert r.status_code in (200, 201), anchor(f"draft {title}", r)
    return r.json()


def attach_snapshot(client: httpx.Client, token: str, slug: str,
                    payload: bytes) -> httpx.Response:
    return client.post(f"/ideas/{slug}/snapshot",
                       content=payload,
                       headers={**bearer(token), "Content-Type": "image/png"})


def png_bytes(marker: bytes) -> bytes:
    return b"\x89PNG\r\n\x1a\n" + marker + b"\x00" * 16
