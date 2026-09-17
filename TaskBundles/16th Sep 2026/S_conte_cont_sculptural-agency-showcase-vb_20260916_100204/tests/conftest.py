from __future__ import annotations

import hashlib
import html
import os
import re
import struct
import time
import zlib
from html.parser import HTMLParser

import httpx
import pytest

import appclient
import capabilities

TIMEOUT = 30.0
SETTLE_STEP = 0.25
SETTLE_LIMIT = 20.0

CORPUS_PASSWORD = "deku-demo-pw-2026"
EDITOR_EMAIL = "editor@example.com"
SECOND_EDITOR_EMAIL = "editor2@example.com"
CLIENT_EMAIL = "client@example.com"
ANONYMOUS_ENQUIRER_EMAIL = "ada.quinn@example.com"
CONTACT_MAILBOX = "hello@example.com"
CAREERS_MAILBOX = "hr@example.com"

SEEDED_ACCOUNTS = (
    (EDITOR_EMAIL, "editor", "Nadia Brooks"),
    (SECOND_EDITOR_EMAIL, "editor", "Owen Pike"),
    (CLIENT_EMAIL, "client", "Leo Marsh"),
)

CONTENT_ROUTES = (
    "/",
    "/services",
    "/works",
    "/works/lumen-pay",
    "/about-us",
    "/blog",
    "/blog/shipping-an-mvp-in-eight-weeks",
    "/blog-categories/engineering",
    "/contact",
    "/privacy-policy",
    "/terms",
)
PUBLIC_ROUTES = CONTENT_ROUTES + ("/sign-in", "/sign-up")
PROTECTED_ROUTES = (
    "/account/enquiries",
    "/studio",
    "/studio/new/details",
    "/studio/new/media",
    "/studio/new/review",
    "/studio/entries/case-study/1",
    "/studio/enquiries",
)
FOOTERLESS_ROUTES = ("/contact",)

GROUND_VALUES = ("dark", "light", "tinted")
GROUND_SEQUENCES = (
    ("/", ("dark", "light", "dark", "tinted")),
    ("/services", ("dark", "light", "dark", "tinted")),
    ("/works", ("light", "dark")),
    ("/works/lumen-pay", ("dark", "light", "dark")),
    ("/about-us", ("dark", "light", "dark", "tinted")),
    ("/blog", ("dark", "tinted")),
    ("/blog-categories/engineering", ("dark", "tinted")),
    ("/blog/shipping-an-mvp-in-eight-weeks", ("dark", "light", "tinted")),
    ("/contact", ("dark", "light")),
    ("/privacy-policy", ("dark", "light")),
    ("/terms", ("dark", "light")),
)

SERVICES = (
    "Design thinking workshop",
    "UX/UI design",
    "Fractional CTO",
    "Website development",
    "Dedicated team",
    "Software development",
    "Branding design",
    "Website design",
)
BUDGETS = ("Under $10k", "$10k - $30k", "$30k - $60k", "$60k - $100k", "Over $100k")

SEEDED_CASE_STUDIES = (
    ("lumen-pay", "Lumen Pay", "Fintech", "A payments app that settles an invoice in one tap", "2026"),
    ("haven-health", "Haven Health", "Healthcare", "A patient portal that makes a clinic visit feel shorter", "2025"),
    ("kitefolio", "Kitefolio", "SaaS", "A portfolio builder for designers who hate building portfolios", "2025"),
    ("orchard-market", "Orchard Market", "E-commerce", "A grocery storefront that restocks before the shelf is empty", "2025"),
    ("tidewater", "Tidewater", "Travel", "A booking flow that fits a whole trip on one screen", "2024"),
    ("northstar-learning", "Northstar Learning", "Education", "A course platform where every lesson ends with something built", "2024"),
    ("quill-and-ink", "Quill and Ink", "Publishing", "An editorial system for a newsroom that never sleeps", "2024"),
    ("parcelio", "Parcelio", "Logistics", "A courier dashboard that shows every parcel at once", "2023"),
    ("verde-energy", "Verde Energy", "Energy", "A home energy app that turns a bill into a plan", "2023"),
    ("atlas-freight", "Atlas Freight", "Supply chain", "A freight marketplace that quotes in seconds", "2023"),
)
LUMEN_PAY_SERVICES = ("UX/UI design", "Software development", "Branding design")
DRAFT_CASE_STUDY_SLUG = "nightjar"
DRAFT_CASE_STUDY_NAME = "Nightjar"

CATEGORIES = (
    ("product-design", "Product design"),
    ("engineering", "Engineering"),
    ("studio-life", "Studio life"),
)
SEEDED_ARTICLES = (
    ("shipping-an-mvp-in-eight-weeks", "Shipping an MVP in eight weeks", "engineering", "7 min read", "Sep 2, 2026"),
    ("design-thinking-workshop-field-notes", "Field notes from a design thinking workshop", "product-design", "5 min read", "Aug 26, 2026"),
    ("five-questions-before-you-hire-a-studio", "Five questions to ask before you hire a studio", "studio-life", "6 min read", "Aug 19, 2026"),
    ("when-to-bring-in-a-fractional-cto", "When to bring in a fractional CTO", "engineering", "8 min read", "Aug 5, 2026"),
    ("designing-onboarding-that-converts", "Designing onboarding that converts", "product-design", "4 min read", "Jul 22, 2026"),
    ("a-week-inside-the-studio", "A week inside the studio", "studio-life", "3 min read", "Jul 8, 2026"),
)
DRAFT_ARTICLE_SLUG = "hiring-a-design-partner"
DRAFT_ARTICLE_TITLE = "Hiring a design partner in 2027"
PAGE_SIZE = 4

CULTURE_OBJECTS = ("rocket", "wand", "arrow", "bomb", "thumb", "bond", "flame")
CULTURE_TITLES = (
    "Lift-off ready",
    "Technomagicians",
    "Aim for the point",
    "Go wow or go home",
    "Win-Win partnership",
    "Bonding together",
    "Keep the fire",
)
PROCESS_WORDS = ("Empathize", "Define", "Ideate", "Prototype", "Test", "Repeat")
TESTIMONIAL_NAMES = ("Mara Lindqvist", "Tomas Reyes", "Priya Anand")
TESTIMONIAL_QUOTES = (
    "The items were delivered on time and in great quality.",
    "They were a professional, experienced team with outstanding ideas.",
    "The team was always accommodating and supportive.",
)
AWARD_NAMES = (
    "Pixel Guild Site of the Day",
    "Studio Honors Gold",
    "Product Craft Award",
    "Design Circle Pick",
    "Web Makers Top Studio",
)
TEAM_MEMBERS = ("Hana Ito", "Marco Silva", "Ruth Okafor", "Dev Patel", "Ingrid Moe", "Sam Carter")
OFFICE_LABELS = ("First Office", "Second Office")
OFFICE_STREETS = ("85 Example St, District 4,", "60 Example Pl, Example NSW 2000")

HOME_HEADINGS = (
    "Our culture, mantra, and beliefs",
    "We've been doing brilliant work with brilliant brands",
    "What our clients talk about us",
)
HEADER_LINKS = ("Services.", "Works.", "About.", "Blog.")
HEADER_BUTTON = "Contact"
DRAWER_LINKS = ("Home.", "Services.", "Works.", "About.", "Blog.", "Hire us.")
DRAWER_SOCIALS = ("facebook", "behance", "instagram", "dribbble", "clutch", "linkedin", "awwwards")
FOOTER_SOCIALS = ("facebook", "instagram", "dribbble", "clutch", "linkedin", "awwwards")
FOOTER_LEAD_IN = "Have a product in mind?"
FOOTER_LINK = "Let's build it"
COPYRIGHT_LINE = "© 2026 Iron Wood - UX UI Design Agency"
PRIVACY_LABEL = "Privacy Policy"
TERMS_LABEL = "Terms"
TERMS_SENTENCE = "By creating an account you agree to the Terms of Service."
NOT_FOUND_LINE = "Sorry! The page you're looking for was not found"
NOT_FOUND_CODE = "404"
NOT_FOUND_ACTION = "Back to home"
SUCCESS_HEADING = "Thank you. Your enquiry is with us."
SUCCESS_LINE = "We read every message and reply within two working days."
FAILURE_LINE = "Something went wrong and your enquiry was not sent. Everything you typed is still here."
SERVICES_HERO = (
    "We build business-savvy products from the hive of creativity blended with the "
    "latest technology trends."
)
CONTACT_HERO = "Be our client. Get that buzz"
WORKS_HERO_LINES = ("We build", "award-winning products", "that everyone loves.")

MEDIA_KEY_RE = re.compile(r"^media/(case-study|article)/(\d+)/([0-9a-f]{64})\.([A-Za-z0-9]+)$")
BINARY_REFERENCE_RE = re.compile(
    r"""(?:src|href|poster|srcset)\s*=\s*["'][^"']*\.(?:png|jpe?g|gif|webp|avif|bmp|svg|ico|mp4|webm|mov|m4v|glb|gltf|drc)(?:[?#][^"']*)?["']"""
    r"""|url\(\s*["']?[^)"']*\.(?:png|jpe?g|gif|webp|avif|bmp|svg|ico|mp4|webm|mov|m4v|glb|gltf|drc)""",
    re.IGNORECASE,
)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
ASSET_TAGS = ("script", "link", "img", "iframe", "source", "video", "audio", "embed")
MAX_UPLOAD_BYTES = 5 * 1024 * 1024
BOT_TOKEN_LIFETIME_MINUTES = 10
RATE_WINDOW_SECONDS = 60


class _TagCollector(HTMLParser):
    """Start tags in document order, with their attributes unescaped."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found: list[tuple[str, dict]] = []

    def handle_starttag(self, tag, attrs):
        self.found.append((tag, {k: (v if v is not None else "") for k, v in attrs}))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def settle(seconds: float = SETTLE_STEP) -> None:
    """The one sanctioned pause. A raw sleep in a test module is a finding."""
    time.sleep(seconds)


def unique_suffix() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def probe_slug(stem: str = "probe") -> str:
    return f"{stem}-{unique_suffix()}"


def digest_of(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def png_bytes() -> bytes:
    """A valid one-pixel PNG whose colour is unique to this call."""
    colour = os.urandom(3)

    def chunk(kind: bytes, data: bytes) -> bytes:
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    pixels = zlib.compress(b"\x00" + colour)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", pixels)
            + chunk(b"IEND", b""))


def app_url() -> str:
    return appclient.app_url()


def api_base() -> str:
    return appclient.api_base()


def page(path: str) -> httpx.Response:
    return httpx.get(f"{app_url()}{path}", timeout=TIMEOUT, follow_redirects=False)


def rendered(path: str) -> str:
    response = page(path)
    assert response.status_code == 200, (
        f"GET {path} returned {response.status_code} rather than a rendered page: "
        f"{response.text[:300]}"
    )
    return response.text


def tags_of(markup: str) -> list[tuple[str, dict]]:
    collector = _TagCollector()
    collector.feed(markup)
    collector.close()
    return collector.found


def tags_with(markup: str, attribute: str) -> list[tuple[str, dict]]:
    return [(tag, attrs) for tag, attrs in tags_of(markup) if attribute in attrs]


def visible_text(markup: str) -> str:
    stripped = re.sub(r"<(script|style)\b.*?</\1>", " ", markup, flags=re.IGNORECASE | re.DOTALL)
    return " ".join(html.unescape(TAG_RE.sub(" ", stripped)).split())


def page_text(path: str) -> str:
    return visible_text(rendered(path))


def head_meta(markup: str) -> dict:
    """name or property -> content, for every meta tag in the document."""
    found = {}
    for tag, attrs in tags_of(markup):
        if tag != "meta":
            continue
        key = (attrs.get("name") or attrs.get("property") or "").lower()
        if key and key not in found:
            found[key] = attrs.get("content", "")
    return found


def title_of(markup: str) -> str:
    match = TITLE_RE.search(markup)
    return " ".join(html.unescape(match.group(1)).split()) if match else ""


def token_for(email: str) -> str:
    return appclient.login(email, CORPUS_PASSWORD)


def as_editor() -> httpx.Client:
    return appclient.client(token_for(EDITOR_EMAIL))


def as_second_editor() -> httpx.Client:
    return appclient.client(token_for(SECOND_EDITOR_EMAIL))


def as_client() -> httpx.Client:
    return appclient.client(token_for(CLIENT_EMAIL))


def anonymous() -> httpx.Client:
    return appclient.client(None)


def login_body(email: str) -> dict:
    response = httpx.post(
        f"{api_base()}/auth/login",
        json={"email": email, "password": CORPUS_PASSWORD},
        timeout=TIMEOUT,
    )
    assert response.status_code == 200, (
        f"POST /api/auth/login for {email} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    return response.json()


def register(display_name: str = "Probe Founder") -> tuple[str, str, dict]:
    email = probe_email()
    response = httpx.post(
        f"{api_base()}/auth/sign-up",
        json={"email": email, "password": CORPUS_PASSWORD, "display_name": display_name},
        timeout=TIMEOUT,
    )
    assert response.status_code in (200, 201), (
        f"POST /api/auth/sign-up for {email} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    body = response.json()
    token = body.get("access_token")
    assert token, f"POST /api/auth/sign-up for {email} returned no access_token: {response.text[:400]}"
    return email, token, body


def case_study_payload(**overrides) -> dict:
    slug = probe_slug("case")
    payload = {
        "slug": slug,
        "name": f"Probe Client {unique_suffix()}",
        "label": "Probe",
        "title": f"A probe project {unique_suffix()}",
        "subtitle": "A probe subtitle",
        "summary": "A probe case study created for this run.",
        "body": f"Probe case study body {unique_suffix()}.",
        "year": 2026,
        "website_url": "https://probe.example.com",
        "services": ["UX/UI design", "Software development"],
    }
    payload.update(overrides)
    return payload


def article_payload(**overrides) -> dict:
    payload = {
        "slug": probe_slug("article"),
        "title": f"Probe article {unique_suffix()}",
        "summary": "A probe article created for this run.",
        "body": f"Probe article body {unique_suffix()}.",
        "category": "engineering",
        "read_minutes": 5,
    }
    payload.update(overrides)
    return payload


def create_case_study(client: httpx.Client, **overrides) -> dict:
    payload = case_study_payload(**overrides)
    response = client.post("/case-studies", json=payload)
    assert response.status_code in (200, 201), (
        f"POST /api/case-studies returned {response.status_code} rather than creating a "
        f"draft: {response.text[:400]}"
    )
    record = response.json()
    assert record.get("state") == "draft", (
        f"POST /api/case-studies returned state {record.get('state')!r} rather than 'draft': "
        f"{response.text[:400]}"
    )
    return record


def create_article(client: httpx.Client, **overrides) -> dict:
    payload = article_payload(**overrides)
    response = client.post("/articles", json=payload)
    assert response.status_code in (200, 201), (
        f"POST /api/articles returned {response.status_code} rather than creating a draft: "
        f"{response.text[:400]}"
    )
    record = response.json()
    assert record.get("state") == "draft", (
        f"POST /api/articles returned state {record.get('state')!r} rather than 'draft': "
        f"{response.text[:400]}"
    )
    return record


def publish(client: httpx.Client, kind: str, record_id) -> httpx.Response:
    return client.post(f"/{kind}/{record_id}/publish")


def unpublish(client: httpx.Client, kind: str, record_id) -> httpx.Response:
    return client.post(f"/{kind}/{record_id}/unpublish")


def published_case_study(client: httpx.Client, **overrides) -> dict:
    record = create_case_study(client, **overrides)
    result = publish(client, "case-studies", record["id"])
    assert result.status_code in (200, 201), (
        f"POST /api/case-studies/{record['id']}/publish returned {result.status_code}: "
        f"{result.text[:400]}"
    )
    return result.json()


def published_article(client: httpx.Client, **overrides) -> dict:
    record = create_article(client, **overrides)
    result = publish(client, "articles", record["id"])
    assert result.status_code in (200, 201), (
        f"POST /api/articles/{record['id']}/publish returned {result.status_code}: "
        f"{result.text[:400]}"
    )
    return result.json()


def upload(client: httpx.Client, kind: str, record_id, payload: bytes | None = None,
           content_type: str = "image/png", alt_text: str | None = "A probe image",
           filename: str | None = None) -> httpx.Response:
    data = {} if alt_text is None else {"alt_text": alt_text}
    body = png_bytes() if payload is None else payload
    name = filename or f"{unique_suffix()}.png"
    return client.post(f"/{kind}/{record_id}/media",
                       files={"file": (name, body, content_type)}, data=data)


def bot_token() -> str:
    response = httpx.get(f"{api_base()}/bot-check", timeout=TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/bot-check returned {response.status_code}: {response.text[:300]}"
    )
    token = response.json().get("token")
    assert token, f"GET /api/bot-check returned no token: {response.text[:300]}"
    return str(token)


def enquiry_payload(**overrides) -> dict:
    payload = {
        "Service": "UX/UI design",
        "Budget": "$30k - $60k",
        "Name": "Probe Founder",
        "Email": probe_email(),
        "Message": f"We would like to talk about a new product {unique_suffix()}.",
        "bpGCap": bot_token(),
        "Website": "",
    }
    payload.update(overrides)
    return payload


def send_enquiry(client: httpx.Client | None = None, **overrides) -> tuple[httpx.Response, dict]:
    payload = enquiry_payload(**overrides)
    if client is None:
        response = httpx.post(f"{api_base()}/enquiries", json=payload, timeout=TIMEOUT)
    else:
        response = client.post("/enquiries", json=payload)
    return response, payload


def enquiry_rows_for(backend, email: str) -> list[dict]:
    return backend.query("SELECT * FROM enquiry WHERE email = %s ORDER BY id", (email,))


def is_client_error(status: int) -> bool:
    return 400 <= status < 500


def sitemap_paths() -> set[str]:
    response = page("/sitemap.xml")
    assert response.status_code == 200, (
        f"GET /sitemap.xml returned {response.status_code}: {response.text[:300]}"
    )
    paths = set()
    for loc in LOC_RE.findall(response.text):
        path = httpx.URL(html.unescape(loc)).path or "/"
        paths.add(path.rstrip("/") or "/")
    return paths


def index_slugs() -> list[str]:
    markup = rendered("/works")
    return [attrs.get("data-slug", "") for _, attrs in tags_with(markup, "data-case-study-row")]


def listed_article_slugs(path: str) -> list[str]:
    markup = rendered(path)
    return [attrs.get("data-slug", "") for _, attrs in tags_with(markup, "data-article-row")]


@pytest.fixture(scope="session")
def store() -> capabilities.ObjectStore:
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend() -> capabilities.Backend:
    return capabilities.make_backend()


@pytest.fixture
def editor():
    with as_editor() as client:
        yield client


@pytest.fixture
def second_editor():
    with as_second_editor() as client:
        yield client


@pytest.fixture
def founder():
    with as_client() as client:
        yield client


@pytest.fixture
def guest():
    with anonymous() as client:
        yield client
