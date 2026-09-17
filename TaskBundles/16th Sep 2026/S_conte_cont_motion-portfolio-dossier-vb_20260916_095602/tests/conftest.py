from __future__ import annotations

import datetime
import email.utils
import hashlib
import html
import json
import mimetypes
import os
import re
import time

import httpx
import pytest

import _shapes
import appclient
import capabilities

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 30.0

APP_PASSWORD = "deku-demo-pw-2026"
DESIGNER_EMAIL = "designer@example.com"
READER_EMAIL = "reader@example.com"
READER2_EMAIL = "reader2@example.com"

DRAFT_SLUG = "kestra-band"
DRAFT_TITLE = "A Wearable That Knew When to Stay Quiet"

FEATURED_SLUGS = (
    "verity-biotics-product",
    "kestra-care",
    "kestra-home",
    "mirror-lab",
)
LIST_SLUGS = (
    "verity-biotics-brand",
    "aging-model",
    "foundry-campaign",
    "foundry-dashboard",
    "vitality-score",
    "dusk-ritual",
    "quitkit",
)
PUBLISHED_SLUGS = FEATURED_SLUGS + LIST_SLUGS

INDEX_TITLES = {
    "verity-biotics-product": "Designing Trust in Preventive Health",
    "kestra-care": "Turning Disconnected Health Data Into Daily Decisions",
    "kestra-home": "The Smart Home Built For Placeland",
    "mirror-lab": "A Retail Experience That Turns Health Into Action",
    "verity-biotics-brand": "Where Art Meets Science",
    "aging-model": "Beyond Biological Age",
    "foundry-campaign": "Using AI to Build a Creative System",
    "foundry-dashboard": "Using AI to Rethink the Way We Build",
    "vitality-score": "Making Health Scores Work",
    "dusk-ritual": "Designing a Brand for Better Sleep",
    "quitkit": "Quit Like a Badass. Not a Patient.",
}

CATALOGUE = {
    "verity-biotics-product": ("verity-biotics", ("strategy", "product"), 2022),
    "kestra-care": ("kestra", ("strategy", "product"), 2020),
    "kestra-home": ("kestra", ("strategy", "product"), 2015),
    "mirror-lab": ("mirror-lab", ("brand-creative", "spatial-experience"), 2025),
    "verity-biotics-brand": ("verity-biotics", ("brand-creative",), 2022),
    "aging-model": ("verity-biotics", ("product",), 2023),
    "foundry-campaign": ("verity-biotics", ("brand-creative", "systems"), 2024),
    "foundry-dashboard": ("verity-biotics", ("product", "systems"), 2025),
    "vitality-score": ("kestra", ("product",), 2021),
    "dusk-ritual": ("dusk-ritual", ("brand-creative",), 2024),
    "quitkit": ("quitkit", ("brand-creative",), 2023),
}

CLIENT_TOKENS = ("verity-biotics", "kestra", "mirror-lab", "dusk-ritual", "quitkit")
DISCIPLINE_TOKENS = ("strategy", "product", "brand-creative", "systems",
                     "spatial-experience")

YEAR_DESC_ORDER = (
    "mirror-lab", "foundry-dashboard", "dusk-ritual", "foundry-campaign",
    "aging-model", "quitkit", "verity-biotics-product", "verity-biotics-brand",
    "vitality-score", "kestra-care", "kestra-home",
)
YEAR_ASC_ORDER = (
    "kestra-home", "kestra-care", "vitality-score", "verity-biotics-product",
    "verity-biotics-brand", "aging-model", "quitkit", "dusk-ritual",
    "foundry-campaign", "mirror-lab", "foundry-dashboard",
)
TITLE_ASC_ORDER = (
    "mirror-lab", "aging-model", "dusk-ritual", "verity-biotics-product",
    "vitality-score", "quitkit", "kestra-home", "kestra-care",
    "foundry-campaign", "foundry-dashboard", "verity-biotics-brand",
)
SYSTEMS_SLUGS = ("foundry-campaign", "foundry-dashboard")
VERITY_PRODUCT_SLUGS = ("verity-biotics-product", "aging-model", "foundry-dashboard")

SLOT_ONE_EXAMPLES = (
    ("kestra-care", "kestra-home"),
    ("verity-biotics-product", "aging-model"),
    ("mirror-lab", "dusk-ritual"),
    ("quitkit", "dusk-ritual"),
)

CHAPTERS = {
    "verity-biotics-product": (
        ("s1", "The belief", "The belief we started with"),
        ("s2", "What we built", "What we were building"),
        ("s3", "Design as strategy", "Design as a strategic decision"),
        ("s4", "When people held it", "What happened when people held it"),
        ("s5", "What we learned", "What this taught us about trust"),
    ),
    "kestra-care": (
        ("s1", "The pivot", "The pivot that set the direction"),
        ("s2", "The platform", "A platform, not a feature"),
        ("s3", "Track trace act", "Track, trace and act"),
        ("s4", "The AI coach", "An AI coach in the pocket"),
        ("s5", "One designer", "One designer across the whole stack"),
        ("s6", "What it became", "What it became in the end"),
    ),
    "mirror-lab": (
        ("s1", "The concept", "A shop that starts with a question"),
        ("s2", "The experience", "Ten minutes, start to finish"),
        ("s3", "The diagnostics", "Diagnostics without a clinic"),
        ("s4", "What this proved", "What the pilot proved"),
        ("s5", "The model", "A model other stores can run"),
    ),
    "aging-model": (
        ("s1", "The question", "The question prevention cannot answer"),
        ("s2", "The model", "Building a model that looks ahead"),
        ("s3", "What it showed", "What the model showed people"),
    ),
    "vitality-score": (
        ("s1", "The noise", "Too many signals, not enough sense"),
        ("s2", "One number", "Designing one number worth checking"),
        ("s3", "Earning trust", "Earning trust in a score"),
        ("s4", "What moved", "What moved when people used it"),
    ),
    "kestra-home": (
        ("s1", "The house", "A house that had never been wired"),
        ("s2", "The hub", "One hub for every room"),
        ("s3", "The installers", "Designing for the installers first"),
        ("s4", "The app", "An app for the whole household"),
        ("s5", "The families", "What families actually asked for"),
        ("s6", "The scale", "Growing to thousands of homes"),
        ("s7", "What it left", "What it left behind"),
    ),
    "foundry-campaign": (
        ("s4", "Three audiences", "Three audiences, three anxieties"),
        ("s5", "The engine", "A lightweight creative engine"),
        ("s6", "The reel", "One reel for every channel"),
        ("s7", "The trio", "Three films, one system"),
        ("s8", "What it made", "What the engine made"),
    ),
    "foundry-dashboard": (
        ("s1", "The brief", "Six weeks and a blank page"),
        ("s2", "The workflow", "An AI-assisted workflow"),
        ("s3", "The guardrails", "Guardrails that kept the quality"),
        ("s4", "The build", "Building in the open"),
        ("s5", "The review", "Review as a daily habit"),
        ("s6", "The launch", "Launching on schedule"),
        ("s7", "What it changed", "What it changed about how we build"),
    ),
}
VBP_CHAPTERS = CHAPTERS["verity-biotics-product"]
DRAFT_CHAPTERS = ("s1", "s2", "s3")

CATALOGUE_DETAIL = {
    "verity-biotics-product": ("The Body Ledger", None, True, "product", "featured"),
    "kestra-care": ("Kestra Care", 2023, False, "product", "featured"),
    "kestra-home": ("Kestra Home", 2021, False, "product", "featured"),
    "mirror-lab": (None, None, True, "product", "featured"),
    "verity-biotics-brand": (None, None, False, "brand", "list"),
    "aging-model": ("The Body Ledger", None, False, "product", "list"),
    "foundry-campaign": ("Foundry", None, False, "product", "list"),
    "foundry-dashboard": ("Foundry", None, False, "product", "list"),
    "vitality-score": ("Vitality Score", None, False, "product", "list"),
    "dusk-ritual": (None, None, False, "brand", "list"),
    "quitkit": (None, None, False, "brand", "list"),
}

LIST_FIELDS = ("slug", "title", "index_title", "client", "product", "disciplines",
               "year", "year_end", "ongoing", "template", "home_placement")
DETAIL_FIELDS = ("summary", "opening_quote", "chapters", "media")
MEDIA_FIELDS = ("id", "role", "alt_text", "width", "height")
ENTRY_FIELDS = ("slug", "title", "saved_at", "max_fraction", "last_fraction",
                "chapters_read", "completed", "last_seen")
PUBLISH_REFUSAL_FIELDS = {"hero": "hero", "alt_text": "alt_text", "chapters": "chapters"}
RESUME_AWAY_SECONDS = 10 * 60
CAMPAIGN_ANCHORS = ("s4", "s5", "s6", "s7", "s8")

NAV_LABELS = ("Intro", "Work", "About", "Contact")
HOME_ANCHORS = ("hero", "featured", "about", "contact")
PHILOSOPHY_PASSAGE = (
    "I believe great products are not just engineered or designed, they are "
    "carefully crafted experiences. My work lives at the intersection of art, "
    "science, and technology, where art shapes form and emotion, science guides "
    "understanding, and technology quietly enables experiences that feel natural "
    "and alive.")
PUNCHLINE = ("Art taught me to see. Science taught me to question. Technology gave "
             "me a way to build. I have not stopped since.")
MECHANISM_LINE = "startY(i) = -40 * curve(t)"

EMPTY_STATE_LINE = ("Nothing matches those two together. Clear the filters and "
                    "start again.")
IGNORED_LINE = "One filter in that link was not recognised and has been dropped."
COOKIE_QUESTION = "May this browser remember your place?"
COOKIE_NAME = "reading_memory"
COOKIE_MIN_SECONDS = 180 * 24 * 3600
PRIVACY_ROUTE = "/privacy"
PRIVACY_SENTENCE = "This site keeps no analytics and sends nothing to anyone else."
LONG_QUERY_LIMIT = 512

MOTION_LEVELS = ("full", "reduced", "still")
COMPLETED_AT = 0.95
RESET_CAP = 0.5
SEEDED_ENTRY_SLUG = "kestra-care"
SEEDED_MAX_FRACTION = 0.4
SEEDED_CHAPTERS = ("s1", "s2")

RESERVED_SLUG = "work"
PROBE_CLIENT = "quitkit"
PROBE_DISCIPLINE = "spatial-experience"
PROBE_YEAR = 2019

SEVEN_TABLES = ("accounts", "case_studies", "case_study_disciplines", "chapters",
                "media", "reading_list", "preferences")

PUBLIC_PAGES = ("/", "/work", "/verity-biotics-product", "/privacy")
HEADER_ROUTES = ("/", "/work", "/privacy", "/api/health", "/api/case-studies")

OBJECT_KEY_TEMPLATE = "case-studies/{case_study_id}/{digest}{ext}"

PNG_BYTES = bytes.fromhex(
    "89504e470d0a1a0a0000000d494844520000000100000001080600000"
    "01f15c4890000000a49444154789c6360000002000100ffff03000006"
    "0005570bf7050000000049454e44ae426082")

TAG_RE = re.compile(r"<[^>]+>")
SCRIPT_RE = re.compile(r"<(script|style|template)\b.*?</\1\s*>", re.I | re.S)
SPACE_RE = re.compile(r"\s+")
HREF_RE = re.compile(r"""href\s*=\s*["']([^"']+)["']""", re.I)
ID_RE_TEMPLATE = r"""id\s*=\s*["']{anchor}["']"""
SCRIPT_SRC_RE = re.compile(r"""<script[^>]+src\s*=\s*["']([^"']+)["']""", re.I)
STYLE_HREF_RE = re.compile(r"""<link[^>]+rel\s*=\s*["']stylesheet["'][^>]*href\s*=\s*["']([^"']+)["']""", re.I)
HOME_SCRIPT_BUDGET = 805638
SECRET_ENV_VARS = ("STORAGE_SECRET_KEY", "STORAGE_ACCESS_KEY")


def server_secrets() -> list:
    out = []
    for name in SECRET_ENV_VARS:
        value = os.environ.get(name, "")
        if len(value) >= 8:
            out.append((name, value))
    return out


def settle() -> None:
    time.sleep(SETTLE_SECONDS)


def unique_token() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{unique_token()}@example.com"


def probe_slug(stem: str) -> str:
    return f"{stem}-{unique_token()}"


def probe_bytes() -> bytes:
    return PNG_BYTES + unique_token().encode("ascii")


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def expected_object_key(case_study_id, payload: bytes, content_type: str) -> str:
    ext = mimetypes.guess_extension(content_type) or ""
    return OBJECT_KEY_TEMPLATE.format(
        case_study_id=case_study_id, digest=sha256_hex(payload), ext=ext)


def describe(response) -> str:
    body = response.text[:400]
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}; body: {body}")


def poll_until(predicate, deadline_seconds: float = POLL_DEADLINE_SECONDS):
    deadline = time.monotonic() + deadline_seconds
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    return last


def visible_markup(markup: str) -> str:
    return SCRIPT_RE.sub(" ", markup)


def visible_text(markup: str, drop: str = "") -> str:
    text = SPACE_RE.sub(" ", TAG_RE.sub(" ", html.unescape(visible_markup(markup))))
    return text.replace(drop, " ").strip() if drop else text.strip()


def seconds_ago(value) -> float:
    if isinstance(value, str):
        value = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.timezone.utc)
    return time.time() - value.timestamp()


def page_text(markup: str) -> str:
    raw = html.unescape(markup)
    stripped = SPACE_RE.sub(" ", TAG_RE.sub(" ", raw))
    joined = SPACE_RE.sub(" ", TAG_RE.sub("", raw))
    return f"{SPACE_RE.sub(' ', raw)}\n{stripped}\n{joined}"


def set_cookie_headers(response) -> list:
    return [v for k, v in response.headers.multi_items() if k.lower() == "set-cookie"]


def cookie_lifetime_seconds(header_value: str) -> int:
    match = re.search(r"max-age\s*=\s*(\d+)", header_value, re.I)
    if match:
        return int(match.group(1))
    match = re.search(r"expires\s*=\s*([^;]+)", header_value, re.I)
    if match:
        parsed = email.utils.parsedate_to_datetime(match.group(1).strip())
        return int(parsed.timestamp() - time.time())
    return 0


def has_anchor(markup: str, anchor: str) -> bool:
    return re.search(ID_RE_TEMPLATE.format(anchor=re.escape(anchor)), markup) is not None


def ident(record) -> str:
    for key in ("id", "case_study_id", "caseStudyId"):
        if isinstance(record, dict) and key in record:
            return record[key]
    raise AssertionError(f"the record carries no id field: {record}")


def slugs_of(payload) -> list:
    out = []
    for row in _shapes.items(payload):
        if isinstance(row, dict) and row.get("slug") is not None:
            out.append(str(row["slug"]))
        elif isinstance(row, str):
            out.append(row)
    return out


def seeded_subsequence(slugs) -> list:
    return [s for s in slugs if s in PUBLISHED_SLUGS]


def as_float(value):
    if value is None or value == "":
        return None
    return float(value)


def as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        if text.startswith("["):
            return [str(v) for v in json.loads(text)]
        if text.startswith("{") and text.endswith("}"):
            return [v.strip().strip('"') for v in text[1:-1].split(",") if v.strip()]
        return [v.strip() for v in text.split(",") if v.strip()]
    return [str(v) for v in value]


def entry_for(payload, slug: str):
    for row in _shapes.items(payload):
        if isinstance(row, dict) and str(row.get("slug")) == slug:
            return row
    return None


def case_study_body(slug: str, **extra) -> dict:
    body = {
        "slug": slug,
        "title": f"Probe {slug}",
        "index_title": f"Probe Index {slug}",
        "summary": "A probe case study written for this check.",
        "template": "product",
        "client": PROBE_CLIENT,
        "disciplines": [PROBE_DISCIPLINE],
        "year": PROBE_YEAR,
        "home_placement": "list",
        "position": 90,
    }
    body.update(extra)
    return body


def create_case_study(designer, slug: str, **extra) -> dict:
    response = designer.post("/studio/case-studies", json=case_study_body(slug, **extra))
    assert response.status_code in (200, 201), (
        "creating a case study as the designer should succeed: " + describe(response))
    return response.json()


def add_chapter(designer, case_study_id, anchor: str, label: str = "Probe label",
                heading: str = "Probe heading"):
    response = designer.post(f"/studio/case-studies/{case_study_id}/chapters", json={
        "anchor": anchor, "rail_label": label, "heading": heading,
        "body": "A probe paragraph."})
    assert response.status_code in (200, 201), (
        f"adding chapter {anchor} as the designer should succeed: " + describe(response))
    return response.json()


def upload_media(designer, case_study_id, role: str = "hero", payload=None,
                 alt_text: str = "A probe image.", content_type: str = "image/png",
                 filename: str = "probe.png"):
    payload = payload if payload is not None else probe_bytes()
    response = designer.post(
        f"/studio/case-studies/{case_study_id}/media",
        files={"file": (filename, payload, content_type)},
        data={"role": role, "alt_text": alt_text, "width": "1600", "height": "900"})
    return payload, response


def publish(designer, case_study_id):
    return designer.post(f"/studio/case-studies/{case_study_id}/publish")


def unpublish(designer, case_study_id):
    return designer.post(f"/studio/case-studies/{case_study_id}/unpublish")


def publishable_case_study(designer, slug: str, **extra) -> dict:
    created = create_case_study(designer, slug, **extra)
    cid = ident(created)
    add_chapter(designer, cid, "s1")
    _, response = upload_media(designer, cid, alt_text=f"Probe hero for {slug}.")
    assert response.status_code in (200, 201), (
        "uploading a hero image as the designer should succeed: " + describe(response))
    return created


def signup(email: str, password: str = APP_PASSWORD, **extra):
    body = {"email": email, "password": password}
    body.update(extra)
    with httpx.Client(base_url=appclient.api_base(), timeout=30.0) as c:
        return c.post("/auth/signup", json=body)


@pytest.fixture(scope="session")
def api_base() -> str:
    return appclient.api_base()


@pytest.fixture(scope="session")
def app_base() -> str:
    return appclient.app_url()


@pytest.fixture()
def anon():
    with appclient.client() as c:
        yield c


@pytest.fixture()
def designer_token() -> str:
    return appclient.login(DESIGNER_EMAIL, APP_PASSWORD)


@pytest.fixture()
def reader_token() -> str:
    return appclient.login(READER_EMAIL, APP_PASSWORD)


@pytest.fixture()
def reader2_token() -> str:
    return appclient.login(READER2_EMAIL, APP_PASSWORD)


@pytest.fixture()
def designer(designer_token):
    with appclient.client(designer_token) as c:
        yield c


@pytest.fixture()
def reader(reader_token):
    with appclient.client(reader_token) as c:
        yield c


@pytest.fixture()
def reader2(reader2_token):
    with appclient.client(reader2_token) as c:
        yield c


@pytest.fixture()
def fresh_reader():
    email = probe_email()
    response = signup(email)
    assert response.status_code in (200, 201), (
        "signing up a fresh reader should succeed: " + describe(response))
    token = appclient.login(email, APP_PASSWORD)
    with appclient.client(token) as c:
        c.probe_email = email
        yield c


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def site():
    with httpx.Client(base_url=appclient.app_url(), timeout=30.0,
                      follow_redirects=True) as c:
        yield c


@pytest.fixture()
def site_direct():
    with httpx.Client(base_url=appclient.app_url(), timeout=30.0) as c:
        yield c
