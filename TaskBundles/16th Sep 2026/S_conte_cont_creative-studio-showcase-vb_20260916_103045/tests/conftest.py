"""Fixtures, pinned literals and helpers for the Naught' task.

Black-box only: HTTP against the running app, the rendered page through
Playwright, PostgreSQL through the shared backend adapter and the object store
through the shared storage adapter. Nothing here reads the agent's source.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import struct
import time
import uuid
import zlib

import httpx
import pytest

import capabilities

TIMEOUT = 40.0
SETTLE_SECONDS = 0.5

PASSWORD = "deku-demo-pw-2026"
AUTHOR_EMAIL = "author@example.com"
READER_EMAIL = "reader@example.com"
READER2_EMAIL = "reader2@example.com"
AUTHOR_NAME = "Lena March"
READER_NAME = "Paolo Ferri"
READER2_NAME = "Ada Rinaldi"
CONTACT_EMAIL = "studio@example.com"

BRAND = "Naught'"
BYLINE = "Creative studio in Milan"
COPYRIGHT = "©24 . 26"
NOT_FOUND_TITLE = "Naught' to see here..."

PUBLISHED = ("solace", "urbana", "un-charted", "kwm", "tactify", "kine", "chemie-union")
FEATURED = ("solace", "urbana", "un-charted", "kwm", "tactify")
DRAFT_SLUG = "veloce"
DRAFT_ORDINAL = 8
TITLES = {
    "solace": "Solace", "urbana": "Urbana", "un-charted": "Un_Charted", "kwm": "Kwm",
    "tactify": "Tactify", "kine": "Kine", "chemie-union": "Chemie Union", "veloce": "Veloce",
}
TAGLINES = {
    "solace": "Where taste meets meaning.",
    "urbana": "A living instrument for reading territory.",
    "un-charted": "Seize the unexpected: the invisible, made visible.",
    "kwm": "Swiss clarity for French engineering.",
    "tactify": "Branding the forgotten sense.",
    "kine": "The movement, made conscious.",
    "chemie-union": "From toxic to tomorrow: chemistry, reframed.",
}
DISCIPLINES = {
    "solace": ["Branding", "Packaging", "Space design"],
    "urbana": ["Branding", "Webdesign", "Development"],
    "un-charted": ["Branding", "Webdesign"],
    "kwm": ["Branding", "Digital"],
}
SERVICES = ("Brand identities", "Campaigns", "Digital experiences", "Events", "Visual systems")
PEOPLE = (
    ("Lena March", "founders & management"), ("Marie-Line Vo", "founders & management"),
    ("Gabriel March", "founders & management"), ("Frederic Valmont", "founders & management"),
    ("Antoine Marlet", "creative partners"), ("Julien Mercer", "creative partners"),
    ("Frederic Delorme", "creative partners"),
)
DISCIPLINE_SET = ("Branding", "Webdesign", "Development", "Digital", "Packaging", "Space design")
KEY_RE = re.compile(r"^works/(?P<work>[^/]+)/(?P<digest>[0-9a-f]{64})\.(?P<ext>png|jpg|webp)$")

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
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def norm(text: str) -> str:
    """Rendered copy uses typographic apostrophes; the brief writes straight ones."""
    return (text or "").replace("’", "'").replace("‘", "'")


def body(response: httpx.Response):
    if "json" not in response.headers.get("content-type", ""):
        return {}
    text = response.text.strip()
    if not text:
        return {}
    return json.loads(text)


def ok(response: httpx.Response, what: str):
    assert response.status_code in OK, f"{what} failed: {describe(response)}"
    return body(response)


def refused(response: httpx.Response, what: str) -> None:
    assert response.status_code in REFUSED, f"{what} was not refused: {describe(response)}"


def missing(response: httpx.Response, what: str) -> None:
    assert response.status_code == 404, f"{what} did not answer as missing: {describe(response)}"


def client(token: str | None = None) -> httpx.Client:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.Client(base_url=base_url(), timeout=TIMEOUT, headers=headers,
                        follow_redirects=False)


def token_for(email: str, password: str = PASSWORD) -> str:
    with client() as anon:
        payload = ok(anon.post("/api/auth/sign-in", json={"email": email, "password": password}),
                     f"sign in for {email}")
    value = str(payload.get("token") or "")
    assert value, f"sign in for {email} returned no token: {payload}"
    return value


def sign_up(display_name: str | None = None, email: str | None = None) -> tuple[httpx.Client, str]:
    address = email or f"{unique('reader')}@example.com"
    with client() as anon:
        payload = ok(anon.post("/api/auth/sign-up", json={
            "display_name": display_name or "Probe Reader", "email": address,
            "password": PASSWORD}), "sign up")
    return client(str(payload["token"])), address


def png_bytes(seed: str) -> bytes:
    """A small valid PNG whose pixels depend on the seed, so its digest is unique."""
    digest = hashlib.sha256(seed.encode()).digest()
    width = height = 8
    rows = b"".join(b"\x00" + bytes(digest[(y * 3 + x) % 32] for x in range(width * 3))
                    for y in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def free_ordinal(author: httpx.Client) -> int:
    taken = {int(w["ordinal"]) for w in works(author)}
    return next(n for n in range(9, 100) if n not in taken)


def new_work(author: httpx.Client, **over) -> dict:
    slug = over.pop("slug", unique("probe"))
    ordinal = over.pop("ordinal", None) or free_ordinal(author)
    doc = {
        "slug": slug, "title": "Probe", "ordinal": ordinal, "year_from": 25, "year_to": 26,
        "disciplines": ["Branding"], "tagline": "A probe, made visible.",
        "brief": "A probe client. It was unusual. The problem was short.",
        "concept": "So we answered it. Short and done.", "credits": [],
    }
    doc.update(over)
    return ok(author.post("/api/works", json=doc), "create draft")


def upload(author: httpx.Client, work_id, data: bytes, kind: str = "cover",
           description: str = "A probe image", **fields) -> httpx.Response:
    form = {"kind": kind, "description": description}
    form.update({k: str(v) for k, v in fields.items()})
    return author.post(f"/api/works/{work_id}/media", data=form,
                       files={"file": ("probe.png", data, "image/png")})


def works(session: httpx.Client, **params) -> list:
    payload = ok(session.get("/api/works", params=params), "works read")
    assert isinstance(payload, list), f"the works read is not an array: {payload}"
    return payload


def html(path: str, session: httpx.Client | None = None) -> httpx.Response:
    with client() as anon:
        target = session or anon
        return target.get(path)


def title_of(markup: str) -> str:
    found = re.search(r"<title[^>]*>(.*?)</title>", markup, re.I | re.S)
    return norm(found.group(1).strip()) if found else ""


def meta_property(markup: str, key: str) -> str:
    for pattern in (rf'<meta[^>]*property=["\']{re.escape(key)}["\'][^>]*content=["\']([^"\']*)["\']',
                    rf'<meta[^>]*content=["\']([^"\']*)["\'][^>]*property=["\']{re.escape(key)}["\']'):
        found = re.search(pattern, markup, re.I)
        if found:
            return found.group(1).strip()
    return ""


def enquiry_doc(**over) -> dict:
    doc = {
        "name": "Probe Visitor", "email": f"{unique('visitor')}@example.com",
        "company": "Probe Co", "service": "Campaigns",
        "preferred_date": (datetime.date.today() + datetime.timedelta(days=7)).isoformat(),
        "time_window": "morning", "message": "We would like to talk about a campaign.",
    }
    doc.update(over)
    return doc


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
    numbers = [float(n) for n in re.findall(r"[\d.]+", value or "")[:3]]
    return tuple(int(round(n)) for n in numbers) if len(numbers) == 3 else (0, 0, 0)


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def anon() -> httpx.Client:
    with client() as session:
        yield session


@pytest.fixture()
def author() -> httpx.Client:
    with client(token_for(AUTHOR_EMAIL)) as session:
        yield session


@pytest.fixture()
def reader() -> httpx.Client:
    with client(token_for(READER_EMAIL)) as session:
        yield session


@pytest.fixture()
def reader2() -> httpx.Client:
    with client(token_for(READER2_EMAIL)) as session:
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
def tablet_page(browser):
    context = browser.new_context(viewport={"width": 990, "height": 800})
    tab = context.new_page()
    yield tab
    context.close()


@pytest.fixture()
def phone_page(browser):
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
