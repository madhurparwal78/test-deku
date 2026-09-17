"""Fixtures, pinned literals and helpers for the Studio AVX portfolio task.

Black-box only: HTTP against the running app, the rendered page through
Playwright, PostgreSQL through the shared backend adapter and Mailpit through the
shared inbox adapter. Nothing here reads the agent's source.
"""

from __future__ import annotations

import os
import re
import time
import uuid

import httpx
import pytest

import capabilities

TIMEOUT = 30.0
SETTLE_SECONDS = 0.5
OK = (200, 201)

PASSWORD = "deku-demo-pw-2026"
STUDIO_EMAIL = "studio@example.com"
STUDIO2_EMAIL = "studio2@example.com"
STUDIO_NAME = "Giulia Ferro"
STUDIO2_NAME = "Marco Lentini"
STUDIO_ROLE = "studio"
STUDIO_ADDRESS = "hello@avx-studio.example.com"
SUBJECT_PREFIX = "Enquiry from "

LOCALES = ("it", "en")
DISCIPLINES = (
    ("branding", "Branding", "Branding"),
    ("editorial", "Editorial", "Editoria"),
    ("type-design", "Type Design", "Type Design"),
    ("web-design", "Web Design", "Web Design"),
    ("packaging", "Packaging", "Packaging"),
)
ALL_LABEL = {"en": "All", "it": "Tutti"}
FACET_COUNTS = {"all": 20, "branding": 11, "editorial": 5, "type-design": 3,
                "web-design": 3, "packaging": 2}

PROJECTS = (
    ("amts-card", "AMTS Card", ("branding",), 2024, "AMTS Catania", True),
    ("infectious-diseases", "Infectious Diseases", ("editorial",), 2023, "SIMIT Sicilia", True),
    ("avx-alphabet", "AVX Alphabet", ("type-design",), 2022, "Studio AVX", True),
    ("herbert", "Herbert", ("type-design",), 2021, "Studio AVX", True),
    ("stelvio-grotesk", "Stelvio Grotesk", ("type-design", "branding"), 2025, "Stelvio Tessuti", True),
    ("etna-wine-cellars", "Etna Wine Cellars", ("branding", "packaging"), 2024, "Cantine Etna Nord", True),
    ("sale-marino", "Sale Marino", ("packaging", "branding"), 2023, "Saline di Trapani", True),
    ("teatro-bellini", "Teatro Bellini", ("branding", "web-design"), 2025, "Teatro Massimo Bellini", True),
    ("ortigia-journal", "Ortigia Journal", ("editorial",), 2022, "Ortigia Edizioni", True),
    ("lava-coffee", "Lava Coffee", ("branding",), 2021, "Lava Coffee Roasters", True),
    ("porto-digitale", "Porto Digitale", ("web-design",), 2026, "Porto di Catania", True),
    ("museo-diffuso", "Museo Diffuso", ("editorial",), 2020, "Comune di Noto", True),
    ("fiera-del-libro", "Fiera del Libro", ("editorial",), 2019, "Fiera del Libro Siciliana", False),
    ("agrumi-bio", "Agrumi Bio", ("branding",), 2020, "Agrumi Bio Paterno", False),
    ("cinema-lumiere", "Cinema Lumiere", ("branding",), 2018, "Cinema Lumiere", False),
    ("atlante-verde", "Atlante Verde", ("editorial",), 2019, "Legambiente Sicilia", False),
    ("kiosk-app", "Kiosk App", ("web-design",), 2024, "Kiosk Mobility", False),
    ("scirocco-festival", "Scirocco Festival", ("branding",), 2022, "Scirocco APS", False),
    ("bottega-ceramica", "Bottega Ceramica", ("branding",), 2018, "Bottega Ceramica Caltagirone", False),
    ("marea-hotel", "Marea Hotel", ("branding",), 2017, "Marea Hotel Taormina", False),
)
SLUGS = tuple(row[0] for row in PROJECTS)
FEATURED = sum(1 for row in PROJECTS if row[5])
DETAIL_SLUG = "sale-marino"
MEDIA_PER_PROJECT = 3

EYEBROWS = ("BASED IN CATANIA / SICILY", "SINCE 2017", "BRANDING / DIGITAL / TYPE / PACKAGING")
STATEMENT = "WE DON'T JUST DESIGN WE DEFINE ATTITUDES"
SERVICES = {
    "it": ("DESIGN EDITORIALE", "TYPE DESIGN", "SOCIAL MEDIA DESIGN",
           "COPYWRITING E NAMING", "BRANDING", "WEB DESIGN"),
    "en": ("EDITORIAL DESIGN", "TYPE DESIGN", "SOCIAL MEDIA DESIGN",
           "COPYWRITING AND NAMING", "BRANDING", "WEB DESIGN"),
}
NAV = {"en": ("All Works", "Studio", "Contact"), "it": ("Tutti i progetti", "Studio", "Contatti")}
FOOTER_TAGLINE = "BRAND & DIGITAL DESIGN STUDIO"
HOME_TITLE_EN = "Studio AVX | Brand & Digital Design Studio based in Italy"
STUDIO_TITLE_IT = "Studio grafico e di comunicazione a Catania"

SEEDED_ENQUIRIES = (
    ("ENQ-0001", "Anna Rizzo", "anna.rizzo@example.com", "it", "new"),
    ("ENQ-0002", "Luca Bianchi", "luca.bianchi@example.com", "it", "replied"),
    ("ENQ-0003", "Sofia Greco", "sofia.greco@example.com", "en", "archived"),
)
STATUSES = ("new", "replied", "archived")
REFERENCE_RE = re.compile(r"^ENQ-\d{4}$")
DECOY_FIELD = "company_website"
ENQUIRY_LIMIT = 10

PRIVACY_TITLE = "Privacy & Cookie Policy"
PRIVACY_CONTROLLER = "Grafiche Meridiane"
PRIVACY_SECTIONS = (
    "1. Titolare del trattamento", "2. Tipologie di dati e finalità",
    "3. Modalità del trattamento", "4. Destinatari dei dati",
    "5. Conservazione dei dati", "6. Diritti dell'interessato", "7. Cookie Policy",
)
CONSENT_COOKIE = "cc_cookie"

PUBLIC_ROUTES = ("/it", "/en", "/works", "/studio", "/contact", "/privacy")
NOT_FOUND_ROUTES = ("/test", "/gs", "/g/d")


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


def token_hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n]


def client_for(token: str | None) -> httpx.Client:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=headers)


def login(email: str, password: str = PASSWORD) -> httpx.Response:
    return httpx.post(f"{api_base()}/auth/login",
                      json={"email": email, "password": password}, timeout=TIMEOUT)


def token_for(email: str, password: str = PASSWORD) -> str:
    response = login(email, password)
    assert response.status_code in OK, f"login for {email} failed: {describe(response)}"
    token = response.json().get("token")
    assert token, f"login for {email} returned no `token`: {describe(response)}"
    return token


def body(response: httpx.Response):
    if "json" not in response.headers.get("content-type", ""):
        return {}
    return response.json()


def message(response: httpx.Response) -> str:
    data = body(response)
    if isinstance(data, dict):
        for key in ("message", "detail", "error"):
            if data.get(key):
                return str(data[key])
    return response.text[:400]


def refused(response: httpx.Response, what: str) -> None:
    assert 400 <= response.status_code < 500, \
        f"{what} must be refused as a client error: {describe(response)}"


def denied(response: httpx.Response, what: str) -> None:
    assert response.status_code in (401, 403, 404), \
        f"{what} must be denied or answered as absent: {describe(response)}"


def ok(response: httpx.Response, what: str):
    assert response.status_code in OK, f"{what} failed: {describe(response)}"
    return response.json()


def rows(response: httpx.Response, what: str) -> list:
    data = ok(response, what)
    assert isinstance(data, list), f"{what} must return a top-level array: {data!r}"
    return data


def wait_until(read, done, timeout: float = 25.0):
    """Poll `read` toward a deadline for a side effect applied asynchronously."""
    deadline = time.monotonic() + timeout
    value = read()
    while not done(value) and time.monotonic() < deadline:
        settle()
        value = read()
    return value


def raw_get(path: str, **kwargs) -> httpx.Response:
    return httpx.get(f"{base_url()}{path}", timeout=TIMEOUT, **kwargs)


def projects_of(client: httpx.Client, **params) -> list:
    return rows(client.get("/projects", params=params), f"project list {params}")


def project_of(client: httpx.Client, slug: str, locale: str = "en") -> httpx.Response:
    return client.get(f"/projects/{slug}", params={"locale": locale})


def facets_of(client: httpx.Client, locale: str = "en") -> list:
    return rows(client.get("/facets", params={"locale": locale}), f"facets {locale}")


def enquiry_payload(**extra) -> dict:
    stamp = token_hex(6)
    payload = {"name": f"Probe Visitor {stamp}",
               "email": f"probe-{stamp}@example.com",
               "message": f"We would like to talk about a new identity, ref {stamp}.\nThanks!",
               "locale": "en", DECOY_FIELD: ""}
    payload.update(extra)
    return payload


def send_enquiry(client: httpx.Client, **extra) -> httpx.Response:
    return client.post("/enquiries", json=enquiry_payload(**extra))


def enquiry_count(backend) -> int:
    return backend.count("enquiries")


def mail_subjects(inbox, to: str) -> list:
    return [m.subject for m in inbox._messages() if any(to.lower() in a.lower() for a in m.to)]


def sign_in_page(page, email: str, password: str = PASSWORD) -> None:
    page.goto(f"{base_url()}/login")
    page.wait_for_load_state("networkidle")
    page.get_by_label(re.compile(r"^\s*email\s*$", re.I)).fill(email)
    page.get_by_label(re.compile(r"^\s*password\s*$", re.I)).fill(password)
    page.get_by_role("button", name=re.compile("sign in|log in|login|accedi", re.I)).click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=20000)


def contrast_ratio(front: tuple, back: tuple) -> float:
    def channel(value):
        value = value / 255.0
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    def luminance(colour):
        r, g, b = (channel(c) for c in colour[:3])
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    first, second = luminance(front), luminance(back)
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def parse_colour(value: str) -> tuple:
    numbers = [float(n) for n in re.findall(r"[\d.]+", value or "")]
    if len(numbers) >= 3:
        return tuple(int(round(n)) for n in numbers[:3])
    return (0, 0, 0)


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def inbox():
    return capabilities.make_inbox()


@pytest.fixture()
def studio():
    with client_for(token_for(STUDIO_EMAIL)) as session:
        yield session


@pytest.fixture()
def anon():
    with client_for(None) as session:
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
    context = browser.new_context(viewport={"width": 390, "height": 844})
    tab = context.new_page()
    yield tab
    context.close()
