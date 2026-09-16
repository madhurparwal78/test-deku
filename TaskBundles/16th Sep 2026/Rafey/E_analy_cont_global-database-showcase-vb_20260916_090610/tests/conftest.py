from __future__ import annotations

import time
import uuid

import pytest

import appclient
import capabilities

SETTLE_SECONDS = 2.0
POLL_SECONDS = 0.5
POLL_BUDGET = 20.0

EDITOR_EMAIL = "editor@example.com"
PUBLISHER_EMAIL = "publisher@example.com"
ADMIN_EMAIL = "administrator@example.com"
EDITOR_PASSWORD = "deku-demo-pw-2026"
PASSWORD = EDITOR_PASSWORD

PUBLISHED_SLUGS = (
    "tessera", "slipstream", "beacon-enterprise", "quarry",
    "bastion", "anvil", "lattice", "foundry",
)
PUBLISHED_NAMES = (
    "Tessera", "Slipstream", "Beacon Enterprise", "Quarry",
    "Bastion", "Anvil", "Lattice", "Foundry",
)
PUBLISHED_COUNT = 8
FLAGSHIP_SLUG = "tessera"
FLAGSHIP_NAME = "Tessera"
FLAGSHIP_SERVICE_LEVEL = "99.999%"
FLAGSHIP_REGIONS = 5
FLAGSHIP_HIGHLIGHTS = 8

DRAFT_SLUG = "halyard"
DRAFT_NAME = "Halyard"
DRAFT_DATASHEET_TITLE = "Halyard Technical Overview"
DRAFT_ART = 3
FLAGSHIP_DATASHEET_TITLE = "Tessera Technical Overview"
PLATFORM_DATASHEETS = ("Meridian Platform Overview", "The Global Network",
                       "Consistency Explained")
DATASHEET_FILENAMES = {
    "Meridian Platform Overview": "meridian-platform-overview.pdf",
    "The Global Network": "the-global-network.pdf",
}

FAMILY_SLUGS = ("databases", "networking", "analytics")
FAMILY_NAMES = ("Databases", "Networking", "Analytics")
FAMILY_COUNTS = {"databases": 4, "networking": 3, "analytics": 3}
FAMILY_STANDFIRSTS = {
    "databases": "Relational and analytical stores that keep one answer everywhere.",
    "networking": "The paths your data travels, kept short and private.",
    "analytics": "Questions asked of data where it already lives.",
}
FAMILY_INTROS = {
    "databases": "Every database here is managed, replicated across regions and read through the same consistency guarantees.",
    "networking": "Traffic stays on the platform's own network from the edge to the region that serves it.",
    "analytics": "Analysis runs beside the data, so a report reads the same rows the application just wrote.",
}
FLAGSHIP_ART = 3
FLAGSHIP_ART_ALT = "Tessera card art, generated field {index} of {total}"
FLAGSHIP_HIGHLIGHT_FIRST = "Reads always reflect the latest write"
FLAGSHIP_SUBNAV_ITEM = "Synchronized clock"
CONSOLE_TIMESTAMP = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$"
COVER_RATIO = 4 / 3
PROBE_PDF_PAGES = 2
DATABASES_SLUGS = ("tessera", "quarry", "anvil", "foundry")
NETWORKING_SLUGS = ("slipstream", "bastion", "anvil", "halyard")
ANALYTICS_SLUGS = ("beacon-enterprise", "quarry", "lattice")

INDUSTRY_NAMES = ("Retail", "Financial services", "Healthcare",
                  "Telecommunications", "Government", "Manufacturing")
CUSTOMER_NAMES = ("Harrowgate", "Vessel Foods", "Cobalt Bank", "Truenorth",
                  "Stonecraft", "Threadly", "Marea Global", "The Gazette")
TESTIMONIAL_NAME = "Anjali Rao"

REGIONS = ("us-central", "eu-west", "asia-south", "sa-east", "au-southeast")
READ_MODES = ("strong", "bounded", "exact")
CONSOLE_VALUE = "amber"

RESERVED_SEGMENTS = (
    "desk", "api", "media", "product", "family", "solution", "datasheet",
    "gallery", "console", "ask", "contact", "privacy", "terms", "404",
)

ART_PAGE_SIZE = 24
NAME_MIN = 3
SUMMARY_MAX = 240
ASSISTANT_CAP = 500
CONTACT_NAME_MIN = 2
CONTACT_MESSAGE_MAX = 1000
SCRIPT_BUDGET_BYTES = 180 * 1024
BLOCKING_REQUEST_MAX = 3

DISPLAY_FAMILY = "Manrope"
BODY_FAMILY = "Inter"
NARROW_VIEWPORT = {"width": 390, "height": 844}
WIDE_VIEWPORT = {"width": 1440, "height": 900}
CONTRAST_FLOOR = 4.5
TOUCH_TARGET_MIN = 44
TIERS = ("sm", "md", "lg", "xl", "xxl")

PUBLIC_ROUTES = (
    "/", "/product", "/product/tessera", "/family", "/family/databases",
    "/solution", "/datasheet", "/gallery", "/console", "/ask", "/contact",
    "/privacy", "/terms",
)

COOKIE_CHOICE_CONTROLS = ("Accept", "Decline")

FEATURED_SLUGS = ("tessera", "slipstream", "beacon-enterprise", "quarry", "bastion", "anvil")
RAIL_HEADING = "Products that hold their promises"
CONTACT_REGIONS = ("Americas", "Europe", "Asia Pacific")
CONTACT_INTERESTS = ("Evaluation", "Migration", "Pricing")
MESSAGE_STACK_MAX = 3

TYPE_STEPS = {
    "body": ("16px", "24px"), "body-medium": ("16px", "24px"), "body-tall": ("16px", "26px"),
    "small": ("14px", "24px"), "dense": ("13px", "24px"), "lead": ("18px", "28px"),
    "title": ("20px", "28px"), "heading": ("24px", "32px"), "display": ("28px", "36px"),
    "micro": ("12px", "16px"), "button": ("14px", "36px"),
}
ALLOWED_FONT_SIZES = {"12px", "13px", "14px", "16px", "18px", "20px", "24px", "28px"}
RHYTHM_STEP = 8

PAGE_TYPES = {
    "/": "landing", "/product/tessera": "product", "/console": "tool", "/ask": "tool",
    "/product": "index", "/family": "index", "/solution": "index", "/datasheet": "index",
    "/gallery": "index",
}

COPY_STRINGS = {
    "/": ("The new way to cloud with Meridian", "Get started for free", "Contact sales",
          "Products that hold their promises", "Solutions for your industry",
          "Teams that build here", "Start your evaluation", "Start free", "Skip to content",
          "Meridian Cloud. All rights reserved.", "Privacy", "Site terms",
          "Why Meridian Cloud", "Products and pricing", "Resources", "Engage"),
    "/product": ("Every product on the platform", "8 products", "Filter by name",
                 "Name, A to Z", "Recently added"),
    "/product/tessera": ("Tessera database", "One database, every region, one truth",
                         "Try it in the console", "Related products"),
    "/family": ("Three ways into the platform",),
    "/solution": ("Solutions by industry", "All"),
    "/datasheet": ("Datasheets to download",),
    "/gallery": ("Every product, drawn", "Show more"),
    "/ask": ("Hello, how can I help?", "0 of 500 characters entered", "Built with Beacon Enterprise",
             "How can I try Meridian Cloud products for free?", "How do I evaluate Tessera?",
             "Discover solutions for my industry", "Summarize what is new"),
    "/privacy": ("What we record",),
    "/terms": ("Using the platform",),
    "/nothing-here": ("We cannot find that page",),
    "/desk/login": ("Sign in to the desk", "Sign in"),
}


def settle() -> None:
    time.sleep(SETTLE_SECONDS)


def probe_token() -> str:
    return uuid.uuid4().hex[:10]


def product_payload(**over) -> dict:
    token = probe_token()
    body = {
        "name": f"Probe Engine {token}",
        "slug": f"probe-engine-{token}",
        "eyebrow": "Probe database",
        "summary": "A probe product written by the checking suite.",
        "claim_body": "A probe product written by the checking suite, three sentences long. "
                      "It carries a claim body so the required fields are populated. "
                      "Nothing about it is drawn from the seed.",
        "families": ["databases"],
        "featured": False,
        "sort_index": 90,
        "service_level": "99.9%",
        "regions_available": 3,
    }
    body.update(over)
    return body


def describe(response) -> str:
    return f"status {response.status_code}, body {response.text[:400]!r}"


def create_draft(client, **over) -> dict:
    payload = product_payload(**over)
    r = client.post("/desk/products", json=payload)
    assert r.status_code in (200, 201), (
        f"POST /api/desk/products for slug {payload['slug']!r} should create a draft: "
        f"{describe(r)}"
    )
    body = r.json()
    assert isinstance(body, dict), (
        f"POST /api/desk/products should answer one entry object: {describe(r)}"
    )
    return body


def product_id(product: dict) -> str:
    assert "id" in product, f"a product object carries an id: {product!r}"
    return str(product["id"])


def add_art(client, pid: str, alt_text: str = "A probe field of drifting colour.") -> dict:
    token = probe_token()
    target = client.post("/desk/uploads", json={
        "product_id": pid, "kind": "art",
        "filename": f"probe-{token}.jpg", "content_type": "image/jpeg",
    })
    assert target.status_code in (200, 201), (
        f"POST /api/desk/uploads should issue an upload target for product {pid}: "
        f"{describe(target)}"
    )
    issued = target.json()
    assert "object_key" in issued, (
        f"POST /api/desk/uploads should name the object_key the bytes land at: "
        f"{describe(target)}"
    )
    put_upload(issued, b"probe-art-bytes")
    r = client.post("/desk/art", json={
        "product_id": pid, "object_key": issued["object_key"], "alt_text": alt_text,
        "width": 1200, "height": 800, "sort_index": 1,
    })
    assert r.status_code in (200, 201), (
        f"POST /api/desk/art should register the uploaded piece for product {pid}: "
        f"{describe(r)}"
    )
    registered = r.json()
    registered["object_key"] = issued["object_key"]
    return registered


def put_upload(issued: dict, payload: bytes) -> None:
    import httpx

    url = issued.get("url") or issued.get("upload_url") or issued.get("target")
    assert url, (
        f"the upload target should carry the address the bytes are sent to: {issued!r}"
    )
    method = (issued.get("method") or "PUT").upper()
    headers = issued.get("headers") or {}
    fields = issued.get("fields")
    with httpx.Client(timeout=appclient.TIMEOUT) as raw:
        if fields:
            r = raw.post(url, data=fields, files={"file": payload})
        else:
            r = raw.request(method, url, content=payload, headers=headers)
    assert r.status_code < 400, (
        f"sending the bytes to the issued upload target should succeed: {describe(r)}"
    )


def probe_pdf(pages: int) -> bytes:
    objects = ["<< /Type /Catalog /Pages 2 0 R >>"]
    kids = " ".join(f"{3 + n} 0 R" for n in range(pages))
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {pages} >>")
    for _ in range(pages):
        objects.append("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>")
    out = b"%PDF-1.4\n"
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{body}\nendobj\n".encode()
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n").encode()
    return out


def drop(client, pid: str) -> None:
    client.patch(f"/desk/products/{pid}", json={"sort_index": 99})


def publish(client, pid: str):
    return client.post(f"/desk/products/{pid}/publish")


def unpublish(client, pid: str):
    return client.post(f"/desk/products/{pid}/unpublish")


def slugs_of(rows) -> set:
    out = set()
    for row in rows:
        if isinstance(row, dict) and row.get("slug"):
            out.add(str(row["slug"]))
    return out


def names_of(rows, key: str = "name") -> set:
    out = set()
    for row in rows:
        if isinstance(row, dict) and row.get(key):
            out.add(str(row[key]))
    return out


def json_list(response, label: str) -> list:
    assert response.status_code == 200, f"{label} should answer 200: {describe(response)}"
    body = response.json()
    assert isinstance(body, list), (
        f"{label} should answer a top-level JSON array: {describe(response)}"
    )
    return body


def poll_until(predicate, label: str):
    deadline = time.monotonic() + POLL_BUDGET
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    raise AssertionError(f"{label} did not hold within {POLL_BUDGET} seconds; last saw {last!r}")


def relative_luminance(rgb) -> float:
    channels = []
    for raw in rgb:
        c = raw / 255.0
        channels.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg) -> float:
    a = relative_luminance(fg) + 0.05
    b = relative_luminance(bg) + 0.05
    return max(a, b) / min(a, b)


def parse_rgb(value: str):
    digits = []
    current = ""
    for ch in value:
        if ch.isdigit() or ch == ".":
            current += ch
        elif current:
            digits.append(current)
            current = ""
    if current:
        digits.append(current)
    assert len(digits) >= 3, f"a computed colour should carry three channels: {value!r}"
    return tuple(int(float(d)) for d in digits[:3])


@pytest.fixture()
def api():
    with appclient.client() as client:
        yield client


@pytest.fixture()
def desk():
    token = appclient.login(PUBLISHER_EMAIL, PASSWORD)
    with appclient.client(token) as client:
        yield client


@pytest.fixture()
def editor():
    token = appclient.login(EDITOR_EMAIL, PASSWORD)
    with appclient.client(token) as client:
        yield client


@pytest.fixture()
def admin():
    token = appclient.login(ADMIN_EMAIL, PASSWORD)
    with appclient.client(token) as client:
        yield client


def denied(response) -> bool:
    return response.status_code in (401, 403)


@pytest.fixture()
def anon():
    with appclient.client() as client:
        yield client


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture()
def page():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as driver:
        browser = driver.chromium.launch(args=["--no-sandbox"])
        context = browser.new_context(viewport=WIDE_VIEWPORT)
        opened = context.new_page()
        opened.set_default_timeout(20000)
        try:
            yield opened
        finally:
            context.close()
            browser.close()
