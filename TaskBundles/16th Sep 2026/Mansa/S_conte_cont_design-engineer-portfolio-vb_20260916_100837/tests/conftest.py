from __future__ import annotations

import hashlib
import html
import os
import re
import struct
import time
import zlib
from html.parser import HTMLParser
from http.cookies import SimpleCookie

import httpx
import pytest

import appclient
import capabilities

TIMEOUT = 30.0
SETTLE_STEP = 0.25
SETTLE_LIMIT = 20.0

STUDIO_PATH = "/studio"
STUDIO_CODE = "5093"
GATED_PATH = "/field-notes"
GATED_CODE = "2718"
WRONG_CODE = "1379"
RATE_LIMITED = "rate_limited"
POSITION_TAKEN = "position_taken"
INVALID_PLACEMENT = "invalid_placement"
INVALID_SLUG = "invalid_slug"
SLUG_RESERVED = "slug_reserved"
SLUG_TAKEN = "slug_taken"
INCOMPLETE = "incomplete"
ALT_TEXT_REQUIRED = "alt_text_required"
INVALID_DIMENSIONS = "invalid_dimensions"
UNSUPPORTED_TYPE = "unsupported_type"
FILE_TOO_LARGE = "file_too_large"
INVALID_MEDIA_ALT = "invalid_media_alt"
INVALID_FIELD = "invalid_field"
INVALID_HEADING_LEVELS = "invalid_heading_levels"

STATUSES = ("draft", "stub", "published")
ASPECT_RATIOS = ("16:9", "1.54:1", "0.71:1", "1:1")
DRAFT_SLUG = "tidewater"
DRAFT_TITLE = "Tidewater Sketchbook"
STUB_SLUG = "teamharbor"
STUB_NOTICE = "Work in progress - this page is not finished yet."
STUB_OUTBOUND = "https://www.example.com/teamharbor"
FIELD_NOTES_SLUG = "field-notes"
FIELD_NOTES_LEAD = "Notes I keep for myself, shared with the people who ask."
GATE_PROMPT = "Please enter passcode"
GATE_LABEL = "Passcode for"
WRONG_CODE_MESSAGE = "That code is not right. Try again."
RATE_LIMIT_MESSAGE = "Too many attempts. Wait a minute and try again."
NOT_FOUND_LINE = "Nothing is filed at this address."
NOT_FOUND_ACTION = "Back to the index"
DOWNLOAD_LABEL = "Download Almanac Mono"
DOWNLOAD_URL = "https://www.example.com/almanac-mono/download"
CONTACT_EMAIL = "studio.rin@example.com"
COPY_LABEL = "COPY"
COPIED_LABEL = "COPIED"
THEME_LABEL = "THEME[A]"
SOUND_LABEL_OPEN = "SOUND["
FOOTER_TERMS = ("Metadata", "Last Updated", "Dimensions", "Characters")
STUDIO_SIDEBAR = ("Case studies", "Index preview", "Page views", "Lock studio")
NEW_CASE_STUDY = "New case study"
SOCIAL_LABELS = ("Twitter/X", "Community", "GitHub")
HEADLINE_LINES = ("I bring", "craft & taste", "to digital work")
HELD_WORDS = ("Innovate", "with", "purpose")
CONTACT_WORDS = ("Let's", "Create", "Something", "Extraordinary")
PRIMARY_STATEMENT = "I explore how to shape AI-era workflows"
DISCIPLINE_LINES = ("Design &", "Engineering")
TAGLINE_LINES = ("Thinking in systems.", "Designing with care.")
SELECTED_WORK = "Selected work"

CASE_STUDY_ROUTES = (
    "/kindling",
    "/almanac-mono",
    "/wasm-design-utils",
    "/ndrive",
    "/coast-icon",
    "/teamharbor",
)
SEEDED_SLUGS = (
    "kindling",
    "almanac-mono",
    "wasm-design-utils",
    "ndrive",
    "coast-icon",
    "teamharbor",
    "field-notes",
    "tidewater",
)
NDRIVE_HEADINGS = (
    (2, "Why another drive", "why-another-drive"),
    (3, "Files as a timeline", "files-as-a-timeline"),
    (3, "Sharing without accounts", "sharing-without-accounts"),
    (2, "Sync, conflicts & recovery", "sync-conflicts-recovery"),
    (3, "Offline, then online", "offline-then-online"),
    (4, "The merge sheet", "the-merge-sheet"),
    (2, "Designing the empty states", "designing-the-empty-states"),
    (3, "What we measured", "what-we-measured"),
    (2, "What I would change", "what-i-would-change"),
)
SEEDED_CARDS = (
    {"sort_order": 1, "title": "Kindling", "slug": "kindling", "external_url": None,
     "eyebrow": "Coding Project", "year_label": "2024-2026", "kind": None,
     "aspect_ratio": "16:9", "column_start": 5, "column_span": 8,
     "column_start_lg": 5, "column_span_lg": 8},
    {"sort_order": 2, "title": "Almanac Mono", "slug": "almanac-mono", "external_url": None,
     "eyebrow": "Coding Project", "year_label": "2025", "kind": None,
     "aspect_ratio": "16:9", "column_start": 1, "column_span": 5,
     "column_start_lg": 1, "column_span_lg": 6},
    {"sort_order": 3, "title": "Wasm design utils", "slug": "wasm-design-utils",
     "external_url": None, "eyebrow": "Coding Project", "year_label": "2025", "kind": None,
     "aspect_ratio": "16:9", "column_start": 7, "column_span": 5,
     "column_start_lg": 7, "column_span_lg": 6},
    {"sort_order": 4, "title": "GlyphSymbols", "slug": None,
     "external_url": "https://www.example.com/plugins/glyphsymbols",
     "eyebrow": "Coding Project", "year_label": "2023", "kind": "tools",
     "aspect_ratio": "1.54:1", "column_start": 6, "column_span": 3,
     "column_start_lg": 5, "column_span_lg": 4},
    {"sort_order": 5, "title": "DuskMode", "slug": None,
     "external_url": "https://www.example.com/plugins/duskmode",
     "eyebrow": "Coding Project", "year_label": "2021", "kind": "tools",
     "aspect_ratio": "1.54:1", "column_start": 10, "column_span": 3,
     "column_start_lg": 9, "column_span_lg": 4},
    {"sort_order": 6, "title": "nDrive", "slug": "ndrive", "external_url": None,
     "eyebrow": None, "year_label": "2020-2022", "kind": None,
     "aspect_ratio": "0.71:1", "column_start": 1, "column_span": 3,
     "column_start_lg": 1, "column_span_lg": 3},
    {"sort_order": 7, "title": "Coast Icon", "slug": "coast-icon", "external_url": None,
     "eyebrow": None, "year_label": "2022", "kind": None,
     "aspect_ratio": "1:1", "column_start": 5, "column_span": 3,
     "column_start_lg": 5, "column_span_lg": 3},
    {"sort_order": 8, "title": "Teamharbor", "slug": "teamharbor", "external_url": None,
     "eyebrow": None, "year_label": "2018-2020", "kind": None,
     "aspect_ratio": "1:1", "column_start": 9, "column_span": 3,
     "column_start_lg": 9, "column_span_lg": 3},
    {"sort_order": 9, "title": "Loop: See Hear Touch", "slug": None,
     "external_url": "https://www.example.com/events/see-hear-touch",
     "eyebrow": None, "year_label": "2022", "kind": "event",
     "aspect_ratio": "1:1", "column_start": 6, "column_span": 3,
     "column_start_lg": 5, "column_span_lg": 4},
    {"sort_order": 10, "title": "Loop: System Design", "slug": None,
     "external_url": "https://www.example.com/events/system-design",
     "eyebrow": None, "year_label": "2021", "kind": "event",
     "aspect_ratio": "1:1", "column_start": 10, "column_span": 3,
     "column_start_lg": 9, "column_span_lg": 4},
)
WIDEST_COLUMN_STARTS = (5, 1, 7, 6, 10, 1, 5, 9, 6, 10)
CARD_FIELDS = (
    "id", "title", "slug", "external_url", "kind", "eyebrow", "year_from", "year_to",
    "year_label", "aspect_ratio", "column_start", "column_span", "column_start_lg",
    "column_span_lg", "sort_order", "media_alt",
)
OBJECT_KEY_TEMPLATE = "case-studies/{case_study_id}/figures/{digest}.png"
BINARY_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".bmp", ".mp3", ".ogg", ".wav",
    ".m4a", ".flac", ".glb", ".gltf", ".ttf", ".otf", ".eot", ".mp4", ".webm", ".mov",
)
WEB_FONT_EXTENSIONS = (".woff2", ".woff")
ANALYTICS_HOSTS = (
    "google-analytics.com", "googletagmanager.com", "plausible.io", "segment.com",
    "hotjar.com", "mixpanel.com", "clarity.ms",
)
WIDE_VIEWPORT = {"width": 1440, "height": 900}
WIDEST_VIEWPORT = {"width": 2560, "height": 1440}
NARROW_VIEWPORT = {"width": 390, "height": 844}
FIVE_MEGABYTES = 5 * 1024 * 1024
MENU_NAME = "Menu"
REFUSED_WORD = "Refused"
FIRST_SOCIAL_URL = "https://www.example.com/rin/x"
SOCIAL_URLS = ("https://www.example.com/rin/x", "https://www.example.com/rin/community",
               "https://www.example.com/rin/github")
VISITOR_IDENTIFIER_WORDS = ("address", "cookie", "agent", "session", "token", "visitor")
SECONDARY_STATEMENT = "I'm building Kindling, and previously worked on Orchard nDrive, Teamharbor, and Hirebase."
INTRO_HEAD = "leading Design Engineering and AI exploration at"
INTRO_TAIL = "Outside work, I build design tools for team efficiency."
HOME_BANDS = ("first-screen", "statement", "index", "held", "contact")
PAGE_VIEW_COLUMNS = ("id", "route", "viewed_at")


def settle(seconds: float = SETTLE_STEP) -> None:
    """The one sanctioned pause. A raw sleep in a test module is a finding."""
    time.sleep(seconds)


def unique_suffix() -> str:
    return os.urandom(6).hex()


def probe_slug(stem: str = "probe") -> str:
    return f"{stem}-{unique_suffix()}"


def free_position() -> int:
    return 1000 + int.from_bytes(os.urandom(3), "big")


def digest_of(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def app_url() -> str:
    return appclient.app_url()


def api_base() -> str:
    return appclient.api_base()


def fetch(path: str, cookie: str | None = None, follow: bool = False) -> httpx.Response:
    headers = {"Cookie": cookie} if cookie else {}
    return httpx.get(f"{app_url()}{path}", timeout=TIMEOUT, headers=headers,
                     follow_redirects=follow)


def api(path: str, cookie: str | None = None) -> httpx.Response:
    headers = {"Cookie": cookie} if cookie else {}
    return httpx.get(f"{api_base()}{path}", timeout=TIMEOUT, headers=headers)


def page_text(markup: str) -> str:
    """Visible-ish text of a page with entities decoded and apostrophes folded."""
    without_scripts = re.sub(r"<(script|style)\b.*?</\1>", " ", markup, flags=re.S | re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", without_scripts))
    text = text.replace("’", "'").replace(" ", " ")
    return re.sub(r"\s+", " ", text)


def squash(text: str) -> str:
    return re.sub(r"\s+", "", text).lower()


def contains(markup: str, phrase: str) -> bool:
    """True when the phrase appears in the page text, ignoring whitespace and case.

    Per-character markup for the scramble effect splits words into many elements,
    so the comparison is made with every run of whitespace removed on both sides.
    """
    return squash(phrase) in squash(page_text(markup))


def local_hrefs(markup: str) -> list[tuple[str, str]]:
    """(href, text) anchors with this app's own origin stripped to a root path."""
    base = app_url()
    out = []
    for href, text in parse(markup).anchors:
        if href.startswith(base):
            href = href[len(base):] or "/"
        out.append((href, text))
    return out


def named_navigation(markup: str, name: str) -> bool:
    """A navigation landmark whose accessible name is `name`, by label or labelledby."""
    for tag, attrs in parse(markup).tags:
        if tag != "nav" and attrs.get("role") != "navigation":
            continue
        if attrs.get("aria-label", "").strip() == name:
            return True
        ref = attrs.get("aria-labelledby", "").strip()
        if ref:
            found = re.search(rf"id=[\"']{re.escape(ref)}[\"'][^>]*>(.*?)<", markup, re.S)
            if found and squash(found.group(1)) == squash(name):
                return True
    return False


def has_named_button(markup: str, name: str) -> bool:
    """A button whose visible text or aria-label is `name`."""
    target = squash(name)
    if any(squash(text) == target for text in parse(markup).buttons):
        return True
    return any(tag == "button" and squash(attrs.get("aria-label", "")) == target
               for tag, attrs in parse(markup).tags)


def submit_passcode(path: str, code, cookie: str | None = None) -> httpx.Response:
    headers = {"Cookie": cookie} if cookie else {}
    return httpx.post(f"{api_base()}/passcode", json={"path": path, "code": code},
                      timeout=TIMEOUT, headers=headers)


def set_cookies(response: httpx.Response) -> list[str]:
    return response.headers.get_list("set-cookie")


def cookie_header(response: httpx.Response) -> str:
    """name=value pairs from every Set-Cookie on a response, ready to send back."""
    pairs = []
    for raw in set_cookies(response):
        jar = SimpleCookie()
        jar.load(raw)
        for name, morsel in jar.items():
            pairs.append(f"{name}={morsel.value}")
    return "; ".join(pairs)


def grant(path: str, code: str) -> str:
    response = submit_passcode(path, code)
    assert response.status_code == 200, (
        f"POST /api/passcode for {path} returned {response.status_code}: {response.text[:300]}"
    )
    assert response.json() == {path: True}, (
        f"POST /api/passcode for {path} with its seeded code answered {response.text[:300]}"
    )
    header = cookie_header(response)
    assert header, f"POST /api/passcode for {path} succeeded but set no grant cookie"
    return header


def studio_cookie() -> str:
    return grant(STUDIO_PATH, STUDIO_CODE)


def field_notes_cookie() -> str:
    return grant(GATED_PATH, GATED_CODE)


def client_with(cookie: str | None) -> httpx.Client:
    headers = {"Cookie": cookie} if cookie else {}
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=headers)


def error_code(response: httpx.Response) -> str | None:
    if "json" not in response.headers.get("content-type", "") or not response.content:
        return None
    body = response.json()
    return body.get("error") if isinstance(body, dict) else None


def card_payload(position: int, **overrides) -> dict:
    card = {
        "eyebrow": None,
        "kind": None,
        "aspect_ratio": "1:1",
        "media_alt": "A soft two-colour gradient standing in for a probe sketch.",
        "column_start": 1,
        "column_span": 4,
        "column_start_lg": 1,
        "column_span_lg": 4,
        "sort_order": position,
    }
    card.update(overrides)
    return card


def case_study_payload(**overrides) -> dict:
    suffix = unique_suffix()
    payload = {
        "title": f"Probe Study {suffix}",
        "slug": f"probe-{suffix}",
        "last_updated": "2026-03-02",
        "year_from": 2026,
        "year_to": None,
        "lead": f"A probe lead {suffix} written for a single run.",
        "body": "## Probe heading\n\nA short probe paragraph.",
        "composed_width": 1440,
        "composed_height": 900,
        "outbound_url": None,
        "gated_path": None,
        "card": card_payload(free_position()),
    }
    payload.update(overrides)
    return payload


def create_case_study(client: httpx.Client, **overrides) -> dict:
    response = client.post("/studio/case-studies", json=case_study_payload(**overrides))
    assert response.status_code in (200, 201), (
        f"POST /api/studio/case-studies returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    assert body.get("status") == "draft", (
        f"a new case study reported status {body.get('status')!r} rather than 'draft': "
        f"{response.text[:300]}"
    )
    return body


def transition(client: httpx.Client, case_study_id, action: str) -> httpx.Response:
    return client.post(f"/studio/case-studies/{case_study_id}/{action}")


def studio_list(client: httpx.Client) -> list[dict]:
    response = client.get("/studio/case-studies")
    assert response.status_code == 200, (
        f"GET /api/studio/case-studies returned {response.status_code}: {response.text[:300]}"
    )
    body = response.json()
    assert isinstance(body, list), f"GET /api/studio/case-studies is not an array: {body!r:.200}"
    return body


def studio_find(client: httpx.Client, slug: str) -> dict | None:
    return next((row for row in studio_list(client) if row.get("slug") == slug), None)


def listed_cards() -> list[dict]:
    response = api("/projects")
    assert response.status_code == 200, (
        f"GET /api/projects returned {response.status_code}: {response.text[:300]}"
    )
    body = response.json()
    assert isinstance(body, list), f"GET /api/projects is not a top-level array: {body!r:.200}"
    return body


def holders_of(position: int) -> list[dict]:
    return [card for card in listed_cards() if card.get("sort_order") == position]


def png_bytes(red: int = 12, green: int = 34, blue: int = 56, width: int = 2,
              height: int = 1) -> bytes:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))

    row = b"\x00" + bytes((red, green, blue)) * width
    raw = row * height
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def random_png() -> bytes:
    shade = os.urandom(3)
    return png_bytes(shade[0], shade[1], shade[2])


def upload(client: httpx.Client, case_study_id, payload: bytes, *,
           content_type: str = "image/png", alt_text: str | None = "A probe figure.",
           width: str = "2", height: str = "1", filename: str = "figure.png") -> httpx.Response:
    data = {"width": width, "height": height}
    if alt_text is not None:
        data["alt_text"] = alt_text
    return client.post(
        f"/studio/case-studies/{case_study_id}/figures",
        files={"file": (filename, payload, content_type)},
        data=data,
    )


def wait_for(getter, predicate, limit: float = SETTLE_LIMIT):
    """Bounded polling toward a deadline; returns the last value seen."""
    deadline = time.monotonic() + limit
    latest = getter()
    while not predicate(latest) and time.monotonic() < deadline:
        settle()
        latest = getter()
    return latest


class _Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.buttons: list[str] = []
        self.anchors: list[tuple[str, str]] = []
        self.tags: list[tuple[str, dict]] = []
        self._button_depth = 0
        self._button_text: list[str] = []
        self._anchor: list[tuple[str, list[str]]] = []

    def handle_starttag(self, tag, attrs):
        attributes = {k: (v or "") for k, v in attrs}
        self.tags.append((tag, attributes))
        if tag == "button":
            self._button_depth += 1
            if self._button_depth == 1:
                self._button_text = []
        if tag == "a":
            self._anchor.append((attributes.get("href", ""), []))

    def handle_endtag(self, tag):
        if tag == "button" and self._button_depth:
            self._button_depth -= 1
            if self._button_depth == 0:
                self.buttons.append(" ".join("".join(self._button_text).split()))
        if tag == "a" and self._anchor:
            href, parts = self._anchor.pop()
            self.anchors.append((href, " ".join("".join(parts).split())))

    def handle_data(self, data):
        if self._button_depth:
            self._button_text.append(data)
        for _, parts in self._anchor:
            parts.append(data)


def parse(markup: str) -> _Collector:
    collector = _Collector()
    collector.feed(markup)
    collector.close()
    return collector


@pytest.fixture(scope="session")
def store() -> capabilities.ObjectStore:
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend() -> capabilities.Backend:
    return capabilities.make_backend()


@pytest.fixture
def studio():
    with client_with(studio_cookie()) as client:
        yield client


@pytest.fixture
def anonymous():
    with client_with(None) as client:
        yield client


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as runner:
        launched = runner.chromium.launch()
        yield launched
        launched.close()


@pytest.fixture
def app_base() -> str:
    return app_url()


@pytest.fixture
def page(browser):
    context = browser.new_context(viewport=WIDE_VIEWPORT,
                                  permissions=["clipboard-read", "clipboard-write"])
    opened = context.new_page()
    opened.set_default_timeout(TIMEOUT * 1000)
    yield opened
    context.close()


@pytest.fixture
def narrow_page(browser):
    context = browser.new_context(viewport=NARROW_VIEWPORT)
    opened = context.new_page()
    opened.set_default_timeout(TIMEOUT * 1000)
    yield opened
    context.close()


@pytest.fixture
def reduced_page(browser):
    context = browser.new_context(viewport=WIDE_VIEWPORT, reduced_motion="reduce")
    opened = context.new_page()
    opened.set_default_timeout(TIMEOUT * 1000)
    yield opened
    context.close()
