from __future__ import annotations

import datetime as dt
import hashlib
import os
import re
import time

import httpx
import pytest

import appclient
import capabilities

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 30.0

APP_PASSWORD = "deku-demo-pw-2026"
FOUNDER_EMAIL = "founder@example.com"
CLIENT_EMAIL = "client@example.com"
CLIENT2_EMAIL = "client2@example.com"

SEEDED_REQUEST = "VS-2026-0001"
SECOND_SEEDED_REQUEST = "VS-2026-0002"
REFERENCE_RE = re.compile(r"^VS-(\d{4})-(\d{4})$")
REFERENCE_IN_TEXT_RE = re.compile(r"VS-\d{4}-\d{4}")
CURRENT_RULES = "2026-09"
RETIRED_RULES = "2026-03"
CURRENCY = "eur"
MAX_ATTACHMENT_BYTES = 5242880
ATTACHMENT_PREFIX = "requests/"
ATTACHMENT_KEY_TEMPLATE = "requests/{reference}/{digest}.{ext}"
PORTRAIT_KEY_TEMPLATE = "portrait/{digest}.{ext}"
SEEDED_ATTACHMENT_NAME = "billing-brief.pdf"

CAPABILITY_ORDER = ("software", "website", "hosting")
RULE_TABLES = {
    "2026-09": {"software": 1200000, "website": 600000, "hosting": 300000},
    "2026-03": {"software": 1000000, "website": 500000, "hosting": 250000},
}
HANDOVER_MINOR = 150000
RESIDENCY_DE_PERCENT = 10
TIMELINE_PERCENT = {"flexible": 90, "standard": 100, "accelerated": 125}
ROUNDING_MINOR = 50000
POSTURES = ("managed", "handover")
RESIDENCIES = ("eu", "de")
BUDGET_BANDS = ("under-10k", "10k-25k", "25k-60k", "over-60k")
DESCRIPTION_MIN = 20
DESCRIPTION_MAX = 4000

WORKED_EXAMPLES = (
    (("software",), "managed", "eu", "standard", 1200000),
    (("website",), "managed", "eu", "flexible", 550000),
    (("hosting",), "managed", "de", "standard", 350000),
    (("website",), "managed", "de", "accelerated", 850000),
    (("software", "website"), "handover", "de", "accelerated", 2650000),
)
SEEDED_FIRST_REQUEST_FIGURE = 1450000
SEEDED_SECOND_REQUEST_FIGURE = 550000

REQUEST_STATUSES = ("new", "reviewing", "quoted", "accepted", "declined")

SEEDED_SYSTEM_NAMES = (
    "Vela Studio",
    "Vela Studio Finance",
    "Vela Studio Analytics",
    "Vela Studio Console",
    "Vela Studio DB Controller",
    "Vela Studio Tickets",
    "Anton Ferber Portfolio",
)
SEEDED_SYSTEM_SLUGS = (
    "vela-studio",
    "vela-studio-finance",
    "vela-studio-analytics",
    "vela-studio-console",
    "vela-studio-db-controller",
    "vela-studio-tickets",
    "anton-ferber-portfolio",
)
PORTFOLIO_SLUG = "anton-ferber-portfolio"
TICKETS_SLUG = "vela-studio-tickets"
CONSOLE_SLUG = "vela-studio-console"
SEEDED_CHECK_RESPONSE_MS = 48
DEFAULT_INTERVAL = 300
DEFAULT_OPEN_AFTER = 3
DEFAULT_CLOSE_AFTER = 2
MINIMUM_INTERVAL = 60
BAR_WINDOW = 90
CHECK_STATUSES = ("up", "slow", "degraded", "down")
FEED_STATUSES = ("up", "slow", "degraded", "down", "unknown")
FEED_PROJECT_FIELDS = (
    "id", "slug", "name", "position", "currentStatus", "uptimePercent",
    "latestResponseMs", "latestCheckedAt", "lastStatusChangeAt", "bars",
)
SEEDED_INCIDENT = "vela-studio-console-20260901-1420"
SEEDED_INCIDENT_OPENED = "2026-09-01T14:20:00Z"
SEEDED_INCIDENT_RESOLVED = "2026-09-01T14:40:00Z"
SEEDED_NOTE_PREFIX = "Disk pressure on the Frankfurt node"
ENTRY_KINDS = ("opened", "note", "resolved")

PUBLISHED_RECORDS = {
    "software": "harbour-ledger",
    "website": "kestrel-storefront",
    "hosting": "lahn-clinic-hosting",
}
DRAFT_RECORD = "aurora-payroll-portal"
HARBOUR_CLIENT = "Lahnhafen Logistik"
KESTREL_CLIENT = "Kestrel Outdoor"
RECORD_TITLES = {
    "harbour-ledger": "Harbour Ledger",
    "kestrel-storefront": "Kestrel Storefront",
    "lahn-clinic-hosting": "Lahn Clinic Hosting",
}
DELIVERED_ON = {
    "harbour-ledger": "2026-06-30",
    "kestrel-storefront": "2026-08-12",
    "lahn-clinic-hosting": "2026-05-02",
}
STARTED_ON = {
    "harbour-ledger": "2026-02-02",
    "kestrel-storefront": "2026-05-11",
    "lahn-clinic-hosting": "2026-03-16",
}
MEASUREMENT_METRICS = ("lcp_ms", "cls", "p95_api_ms", "uptime_percent")
PRIMITIVE_KINDS = ("rect", "path", "circle")
PRIMITIVE_ROLES = ("accent", "structure", "faint")
CAPABILITY_LINKS = {
    "Scope a build": "software",
    "See a build": "website",
    "See the stack": "hosting",
}

PUBLIC_ROUTES = ("/", "/about", "/uptime", "/impressum", "/agb", "/builds",
                 "/build-request")
FOOTER_ROUTES = ("/", "/about", "/impressum", "/agb", "/uptime")
LEGAL_ROUTES = ("/impressum", "/agb")
SCRIPTED_ROUTES = ("/", "/about", "/uptime", "/builds", "/build-request")
FOOTER_LINKS = {
    "Home": "/",
    "About": "/about",
    "Legal Notice": "/impressum",
    "Terms": "/agb",
    "Status/Uptime": "/uptime",
}
ROUTE_TITLES = {
    "/": "Vela Studio | Software Made in Germany, Hosted in Europe",
    "/about": "About | Vela Studio",
    "/uptime": "System Status | Vela Studio",
    "/impressum": "Legal Notice | Vela Studio",
    "/agb": "Terms & Conditions | Vela Studio",
    "/builds": "Builds | Vela Studio",
    "/build-request": "Build request | Vela Studio",
}
HOME_DESCRIPTION_PHRASE = "hosted in Europe on privacy-first infrastructure"
DIAGRAM_LABELS = (
    "Diagram: interface, API and workers over a Postgres database",
    "Diagram: a browser window with Core Web Vitals scores",
    "Diagram: a server rack with encrypted uplinks",
    "Diagram: four interconnected nodes across Falkenstein, Frankfurt and Eygelshoven",
)
DIAGRAM_WORDS = ("interface", "api", "workers", "postgres", "LCP 0.6s",
                 "CLS 0.00", "100 / 100", "uplink", "encrypted", "FSN", "FRA",
                 "EYG-1", "EYG-2")
HOME_COPY = (
    "Software built in Germany.",
    "Hosted in Europe.",
    "We write production software and run it on our own machines.",
    "Talk to an engineer",
    "See what we build",
    "01 - Philosophy",
    "We build privacy-first software and infrastructure that stays honest",
    "What we build",
    "Capabilities",
    "Software & Platforms",
    "High-performing websites",
    "Managed hosting, privacy-first",
    "Four nodes. One jurisdiction.",
    "Capability",
    "Infrastructure",
    "SaaS products, internal tools",
    "Marketing sites and web apps",
    "Your workload runs on our own hardware",
    "Our racks, our keys",
    "06 - Contact",
    "talk to an engineer_",
    "Reply within one working day, from the person who would write the code.",
    "hello@vela.example.com",
    "Curious who's actually behind the racks?",
    "(a real human)",
    "Marburg, DE",
)
ABOUT_COPY = (
    "Why I build",
    "I'm Anton.",
    "01 - The craft",
    "I build software the way",
    "02 - The principle",
    "Privacy isn't a feature",
    "03 - Elsewhere",
    "about me_",
    "anton-ferber.example.com",
    "Anton Ferber",
    "More of what I make, write and tinker with lives on my personal site.",
    "Marburg",
    "Germany",
    "Scroll",
)
UPTIME_COPY = (
    "System status",
    "Live reliability, shown in public.",
    "Live status needs JavaScript to load.",
    "Every Vela Studio system, monitored continuously.",
    "Looking for incident history, deeper diagnostics, or want to open a ticket? Full detail lives in the customer portal.",
    "Incident history",
    "Open customer portal",
    "portal.vela.example.com",
)
IMPRESSUM_COPY = (
    "Back to Vela Studio",
    "Information pursuant to",
    "Provider",
    "Contact",
    "Registered office",
    "VAT identification number: DE123456789",
    "Phone:",
    "Email:",
    "WhatsApp Business:",
    "Responsible for content",
    "Liability for content",
    "Liability for links",
    "Copyright",
    "Ketzerbach 21",
    "35037 Marburg",
    "+49 6421 555 0142",
)
AGB_COPY = (
    "Back to Vela Studio",
    "General Terms and Conditions",
    "1. Scope",
    "2. Services",
    "3. Client cooperation",
    "4. Fees and payment",
    "5. Operations and availability",
    "6. Rights of use",
    "7. Liability",
    "8. Final provisions",
)
COMPOSER_CONTROL_NAMES = (
    "capabilities", "posture", "residency", "timeline", "budget_band",
    "description", "contact_name", "contact_email", "contact_fax",
    "rules_version", "indicative_minor", "attachment",
)
COMPOSER_COPY = (
    "Describe the build",
    "Indicative figure",
    "Send build request",
    "We run it on our racks",
    "Hand it over to run yourself",
    "Software & Platforms",
    "High-performing websites",
    "Managed hosting, privacy-first",
    "Anywhere in the EU",
    "Germany only",
    "Flexible",
    "Standard",
    "Accelerated",
    "Under EUR 10,000",
    "EUR 10,000 to 25,000",
    "EUR 25,000 to 60,000",
    "Over EUR 60,000",
)
BUILDS_COPY = ("Builds", "All", "Software & Platforms",
               "High-performing websites", "Managed hosting, privacy-first")
UPTIME_TILE_LABELS = ("Systems", "Operational", "Average uptime", "Next check")
UPTIME_CARD_LABELS = ("Uptime", "Response time", "Last checked",
                      "Last status change")
STATUS_WORDS = ("Operational", "Slow", "Degraded", "Down", "Unknown")
PORTRAIT_ALT = "Anton Ferber, founder of Vela Studio"
PORTRAIT_PLACEHOLDER = "Portrait placeholder"
PREVIEW_ALT = "Vela Studio - Software that scales"
POSITION_HEADING = "Managed hosting, privacy-first"
POSITION_ADDRESS = "/?at=managed-hosting-80"
CONTRAST_FLOOR = 4.5
NARROW_VIEWPORT = {"width": 320, "height": 640}
WIDE_VIEWPORT = {"width": 1440, "height": 900}
IDENTIFYING_COLUMN_WORDS = ("ip", "addr", "agent", "cookie", "fingerprint",
                            "session")
PAGE_VIEW_COLUMNS = ("id", "route", "viewed_at")
PROBE_EPOCH = "2026-03-02T10:00:00Z"

PDF_HEAD = b"%PDF-1.4\n1 0 obj << /Type /Catalog >> endobj\n"
PDF_TAIL = b"\ntrailer << /Root 1 0 R >>\n%%EOF\n"
PNG_BYTES = bytes.fromhex(
    "89504e470d0a1a0a0000000d494844520000000100000001080600000"
    "01f15c4890000000a49444154789c6360000002000100ffff03000006"
    "0005570bf7050000000049454e44ae426082")


def settle() -> None:
    time.sleep(SETTLE_SECONDS)


def unique_token() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{unique_token()}@example.com"


def probe_slug(stem: str) -> str:
    return f"{stem}-{unique_token()}"


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def pdf_payload() -> bytes:
    return PDF_HEAD + unique_token().encode("ascii") + PDF_TAIL


def png_payload() -> bytes:
    return PNG_BYTES + unique_token().encode("ascii")


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


def is_client_error(response) -> bool:
    return 400 <= response.status_code < 500


def is_denied(response) -> bool:
    return response.status_code in (401, 403, 404)


def figure(caps, posture, residency, timeline, version=CURRENT_RULES) -> int:
    table = RULE_TABLES[version]
    base = sum(table[c] for c in set(caps))
    subtotal = base
    if posture == "handover":
        subtotal += HANDOVER_MINOR
    if residency == "de":
        subtotal += base * RESIDENCY_DE_PERCENT // 100
    scaled = subtotal * TIMELINE_PERCENT[timeline] // 100
    units, remainder = divmod(scaled, ROUNDING_MINOR)
    if remainder * 2 >= ROUNDING_MINOR:
        units += 1
    return units * ROUNDING_MINOR


def euros(minor: int) -> str:
    return f"EUR {minor // 100:,}"


def canonical_caps(caps) -> list[str]:
    return [c for c in CAPABILITY_ORDER if c in set(caps)]


def request_body(caps=("software",), posture="managed", residency="eu",
                 timeline="standard", budget="10k-25k", **overrides) -> dict:
    body = {
        "capabilities": list(caps),
        "posture": posture,
        "residency": residency,
        "timeline": timeline,
        "budget_band": budget,
        "description": f"Probe enquiry {unique_token()} about replacing a "
                       f"spreadsheet with a small internal tool.",
        "contact_name": "Probe Buyer",
        "contact_email": probe_email(),
        "rules_version": CURRENT_RULES,
        "indicative_minor": figure(caps, posture, residency, timeline),
        "contact_fax": "",
    }
    body.update(overrides)
    return body


def form_fields(body: dict) -> dict:
    fields = {}
    for key, value in body.items():
        if key == "capabilities":
            fields[key] = ",".join(value)
        elif value is None:
            continue
        else:
            fields[key] = str(value)
    return fields


def reference_of(payload) -> str:
    if isinstance(payload, dict):
        for key in ("reference", "ref"):
            if payload.get(key):
                return str(payload[key])
        for value in payload.values():
            if isinstance(value, dict) and value.get("reference"):
                return str(value["reference"])
    raise AssertionError(f"response carries no reference: {str(payload)[:300]}")


def field(payload, *names):
    if isinstance(payload, dict):
        for name in names:
            if name in payload:
                return payload[name]
        for value in payload.values():
            if isinstance(value, dict):
                for name in names:
                    if name in value:
                        return value[name]
    return None


def requests_for(backend, email: str) -> list[dict]:
    return backend.rows("build_requests", limit=50, contact_email=email)


def parse_time(value) -> dt.datetime:
    if isinstance(value, dt.datetime):
        stamp = value
    else:
        stamp = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=dt.timezone.utc)
    return stamp.astimezone(dt.timezone.utc)


def probe_times(count: int, start: str = PROBE_EPOCH, step: int = DEFAULT_INTERVAL,
                gaps: tuple = ()) -> list[str]:
    base = parse_time(start)
    out = []
    offset = 0
    for index in range(count):
        if index in gaps:
            offset += 1
        moment = base + dt.timedelta(seconds=step * (index + offset))
        out.append(moment.strftime("%Y-%m-%dT%H:%M:%SZ"))
    return out


def at_minutes(hour: int, minute: int, day: str = "2026-03-02") -> str:
    return f"{day}T{hour:02d}:{minute:02d}:00Z"


def create_system(founder, stem="probe-system", **extra) -> str:
    slug = probe_slug(stem)
    body = {"slug": slug, "name": f"Probe {slug}"}
    body.update(extra)
    response = founder.post("/systems", json=body)
    assert response.status_code in (200, 201), (
        "the founder must be able to create a system: " + describe(response))
    return slug


def post_check(founder, slug, checked_at, status, response_ms=40):
    return founder.post(f"/systems/{slug}/checks", json={
        "checked_at": checked_at, "status": status, "response_ms": response_ms})


def record_checks(founder, slug, rows) -> None:
    for checked_at, status, response_ms in rows:
        response = post_check(founder, slug, checked_at, status, response_ms)
        assert response.status_code in (200, 201), (
            f"recording a {status} check at {checked_at} for {slug} must "
            "succeed: " + describe(response))


def feed(client) -> dict:
    response = client.get("/uptime/projects")
    assert response.status_code == 200, (
        "the status feed must answer without a session: " + describe(response))
    body = response.json()
    assert isinstance(body, dict) and isinstance(body.get("data"), dict), (
        f"the status feed must return the pinned data envelope: {str(body)[:300]}")
    return body["data"]


def feed_project(client, slug) -> dict:
    data = feed(client)
    for project in data.get("projects") or []:
        if project.get("slug") == slug:
            return project
    raise AssertionError(f"the status feed lists no project with slug {slug}")


def bar_statuses(project) -> list[str]:
    return [str(bar.get("status")) for bar in project.get("bars") or []]


def incidents_for(client, system_slug) -> list[dict]:
    response = client.get("/uptime/incidents")
    assert response.status_code == 200, (
        "the incident list must be public: " + describe(response))
    rows = response.json()
    assert isinstance(rows, list), (
        f"the incident list must be a top-level array: {str(rows)[:300]}")
    return [row for row in rows if str(row.get("system")) == system_slug]


def incident_entries(client, ref) -> list[dict]:
    response = client.get(f"/uptime/incidents/{ref}")
    assert response.status_code == 200, (
        f"incident {ref} must be publicly readable: " + describe(response))
    entries = response.json().get("entries")
    assert isinstance(entries, list), (
        f"incident {ref} must carry an entries list: {response.text[:300]}")
    return sorted(entries, key=lambda e: int(e.get("seq")))


def flapping_rows() -> list[tuple]:
    statuses = ("down", "down", "up", "down", "up", "down", "up", "up", "up",
                "up")
    times = probe_times(len(statuses), start=at_minutes(11, 0))
    return [(t, s, None if s == "down" else 40) for t, s in zip(times, statuses)]


def build_record_body(capability="website", delivered_on="2026-01-15", **extra):
    slug = probe_slug("probe-record")
    body = {
        "slug": slug,
        "title": f"Probe Record {slug[-6:]}",
        "capability": capability,
        "summary": "A probe record written to exercise the build library.",
        "body": "The probe record carries a short body and a small diagram.",
        "stack": ["Python", "PostgreSQL"],
        "started_on": "2026-01-02",
        "delivered_on": delivered_on,
        "client_name": "Probe Client",
        "client_visible": True,
        "diagram": [
            {"kind": "rect", "role": "accent", "x": 60, "y": 30,
             "width": 300, "height": 62, "rx": 8},
            {"kind": "rect", "role": "structure", "x": 20, "y": 140,
             "width": 170, "height": 62, "rx": 8},
            {"kind": "path", "role": "faint", "d": "M150 92 V116 H105 V140"},
            {"kind": "circle", "role": "accent", "cx": 210, "cy": 61, "r": 3},
        ],
    }
    body.update(extra)
    return body


def anchors(html: str) -> list[tuple[str, str]]:
    out = []
    for match in re.finditer(r"<a\b([^>]*)>(.*?)</a>", html, re.S | re.I):
        href = re.search(r"href\s*=\s*[\"']([^\"']*)[\"']", match.group(1), re.I)
        text = re.sub(r"<[^>]+>", " ", match.group(2))
        text = re.sub(r"\s+", " ", text).strip()
        if href:
            out.append((href.group(1), text))
    return out


def path_of(href: str, base: str) -> str:
    target = httpx.URL(base).join(href)
    return target.path or "/"


def storage_object_url(key: str) -> str:
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    bucket = os.environ["STORAGE_BUCKET"]
    return f"{endpoint}/{bucket}/{key}"


def relative_luminance(rgb) -> float:
    def channel(value):
        c = value / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def parse_rgb(text: str):
    numbers = re.findall(r"[\d.]+", text or "")
    if len(numbers) < 3:
        raise AssertionError(f"not a computed colour: {text!r}")
    return tuple(float(n) for n in numbers[:3])


def contrast(fore: str, back: str) -> float:
    a = relative_luminance(parse_rgb(fore))
    b = relative_luminance(parse_rgb(back))
    light, dark = max(a, b), min(a, b)
    return (light + 0.05) / (dark + 0.05)


class RenderedText(str):
    """Rendered page text whose `in` ignores letter case, since labels may be set in capitals."""

    def __contains__(self, other) -> bool:
        return str(other).casefold() in self.casefold()


def body_text(page) -> str:
    return RenderedText(re.sub(r"\s+", " ", page.inner_text("body")))


def in_viewport(page, text: str) -> bool:
    locator = page.get_by_text(text, exact=True).first
    box = locator.bounding_box()
    if not box:
        return False
    height = page.evaluate("window.innerHeight")
    return box["y"] < height and box["y"] + box["height"] > 0


def choose(page, name: str, value: str) -> None:
    selects = page.locator(f"select[name='{name}']")
    if selects.count():
        selects.first.select_option(value)
        return
    page.locator(f"input[name='{name}'][value='{value}']").first.check()


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
def founder():
    token = appclient.login(FOUNDER_EMAIL, APP_PASSWORD)
    with appclient.client(token) as c:
        yield c


@pytest.fixture()
def client_token() -> str:
    return appclient.login(CLIENT_EMAIL, APP_PASSWORD)


@pytest.fixture()
def client(client_token):
    with appclient.client(client_token) as c:
        yield c


@pytest.fixture()
def client2():
    token = appclient.login(CLIENT2_EMAIL, APP_PASSWORD)
    with appclient.client(token) as c:
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


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        engine = p.chromium.launch()
        yield engine
        engine.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context(viewport=WIDE_VIEWPORT)
    tab = context.new_page()
    yield tab
    context.close()


@pytest.fixture()
def ui_page(browser):
    context = browser.new_context(viewport=WIDE_VIEWPORT,
                                  java_script_enabled=False)
    tab = context.new_page()
    yield tab
    context.close()


@pytest.fixture()
def browser_page(browser):
    context = browser.new_context(viewport=WIDE_VIEWPORT,
                                  reduced_motion="reduce")
    tab = context.new_page()
    yield tab
    context.close()


TYPE_SCALE = {
    1440: {"hero": 100.8, "statement": 66.24, "card_heading": 48.0, "card_body": 23.04,
           "contact": 70.4},
    990: {"hero": 69.3, "statement": 45.54, "card_body": 16.8, "contact": 51.48},
    390: {"hero": 32.76, "statement": 32.0, "card_body": 16.8, "contact": 22.4},
}
TYPE_TOLERANCE = 0.6
BAR_TITLE_RE = r"^(Operational|Slow|Degraded|Down|Unknown) at \d{1,2} \w+ \d{4}, \d{2}:\d{2}$"
HOVER_CEILING_SECONDS = 0.2
LAYOUT_SHIFT_CEILING = 0.02
PHOTO_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif")


def font_px(page, locator) -> float:
    return float(locator.evaluate("e => parseFloat(getComputedStyle(e).fontSize)"))


def font_family(page, locator) -> str:
    return str(locator.evaluate("e => getComputedStyle(e).fontFamily"))
