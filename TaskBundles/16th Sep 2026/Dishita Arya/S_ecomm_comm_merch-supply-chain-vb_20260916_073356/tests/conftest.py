"""Fixtures, stores and pinned literals for the Kilnly verifier.

Every value here is pinned in instruction.md. Nothing in this file asserts;
assertions live in test_output.py.
"""

from __future__ import annotations

import os
import time
import uuid

import httpx
import pytest

import capabilities

TIMEOUT = 30.0
SETTLE_STEP = 0.25
SETTLE_LIMIT = 20.0

SEED_PASSWORD = "deku-demo-pw-2026"

OWNER_EMAIL = "owner@example.com"
OPERATOR_EMAIL = "operator@example.com"
FINANCE_EMAIL = "finance@example.com"
VIEWER_EMAIL = "viewer@example.com"
OWNER2_EMAIL = "owner2@example.com"
BUYER_EMAIL = "buyer@example.com"
BUYER2_EMAIL = "buyer2@example.com"
BUYER3_EMAIL = "buyer3@example.com"

SEEDED_ACCOUNTS = [
    OWNER_EMAIL, OPERATOR_EMAIL, FINANCE_EMAIL, VIEWER_EMAIL,
    OWNER2_EMAIL, BUYER_EMAIL, BUYER2_EMAIL, BUYER3_EMAIL,
]

WORKSPACE_ONE = "Tidewater Goods"
WORKSPACE_TWO = "Copperline Club"
ROLES = ["owner", "operator", "finance", "viewer"]

CATEGORIES = ["apparel", "outerwear", "headwear", "accessories"]
CHIPS = ["All", "Apparel", "Outerwear", "Headwear", "Accessories"]

CATALOGUE = [
    ("acid-wash-patch-tee", "Acid-Wash Patch Tee", 3400, 100, "apparel"),
    ("embroidered-logo-tee", "Embroidered Logo Tee", 3000, 100, "apparel"),
    ("acid-wash-embroidered-hoodie", "Acid-Wash Embroidered Hoodie", 4800, 50, "apparel"),
    ("embroidered-quarter-zip", "Embroidered Quarter-Zip", 4800, 50, "apparel"),
    ("embroidered-dad-cap", "Embroidered Dad Cap", 1900, 100, "headwear"),
    ("washed-work-jacket", "Washed Work Jacket", 6800, 50, "outerwear"),
    ("canvas-duffel-bag", "Canvas Duffel Bag", 4200, 50, "accessories"),
    ("canvas-tote", "Canvas Tote", 2200, 100, "accessories"),
]

JACKET_SLUG = "washed-work-jacket"
TOTE_SLUG = "canvas-tote"
JACKET_SKU = "KJ-WORK-M"
TOTE_SKU = "CT-NAT-OS"
LOCATIONS = ["rotterdam", "newark"]
TRANSFER_UNITS = 6

PUBLIC_ROUTES = [
    "/", "/catalogue", "/merch-fulfillment", "/custom-merch-no-minimum",
    "/about", "/blog", "/brand", "/legal/website-terms-of-use", "/legal/privacy",
]
TERMS_ROUTE = "/legal/website-terms-of-use"
PRIVACY_ROUTE = "/legal/privacy"
SITEMAP_ROUTE = "/sitemap.xml"
ROBOTS_ROUTE = "/robots.txt"
NOT_FOUND_LINE = "Page not found"
FULFILLMENT_THESIS = "Nobody owns the delivery date."
FULFILLMENT_CLOSING = "One chain, one place to watch it."
OPS_SURFACE_FIGURE = "11"
MINIMUM_ORDER_FIGURE = "1"
NOTE_CATEGORIES = ["Supply chain", "Commerce", "Industry"]

DECORATION_METHODS = ["screen_print", "embroidery", "patch", "wash"]
MIN_PPI = 150
SCREEN_PRINT_COLOURS = 6
EMBROIDERY_COLOURS = 12
BLEED_MM = 3
ARTWORK_PIXEL_WIDTH = 900
ARTWORK_PRINT_CM = 30
ARTWORK_EFFECTIVE_PPI = 76

BRIEF_QUANTITY = 500
AVEIRO = "aveiro-knitworks"
TIRUPUR = "tirupur-mills"
DOZEN_QUOTE_MINOR = 46800
PIECE_QUOTE_MINOR = 3900
EUR_RATE = "1.08"
EUR_RATE_DATE = "2026-09-01"
UNIT_IN_USD_MINOR = 4212
SETUP_TOTAL_MINOR = 85000
SETUP_PER_UNIT_MINOR = 170
FREIGHT_TOTAL_MINOR = 120000
FREIGHT_PER_UNIT_MINOR = 240
DUTY_PERCENT = 12
DUTY_PER_UNIT_MINOR = 505
INSURANCE_PER_UNIT_MINOR = 17
AVEIRO_LANDED_MINOR = 5144
TIRUPUR_HEADLINE_MINOR = 2900
TIRUPUR_LANDED_MINOR = 6010
PRICE_BREAKS = [250, 500, 1000]
OFFER_VALID_DAYS = 14

SAMPLE_DECISIONS = ["accept", "rework", "reject"]
INSPECTION_SAMPLE_SIZE = 80
MAX_MAJOR = 2
MAX_MINOR = 5
BATCH_DECISIONS = ["rework", "partial_accept", "reject"]

RUN_STAGES = ["purchase_order", "deposit", "materials", "production",
              "quality", "packing", "freight_handover"]
LEDGER_KINDS = ["receipt", "reservation", "allocation", "pick", "shipment",
                "return", "write_off", "transfer_out", "transfer_in"]
ORDER_STATES = ["placed", "reserved", "picked", "packed", "handed_over",
                "in_transit", "delivered", "cancelled", "returned"]
OPS_SURFACES = ["receiving", "put_away", "storage", "replenishment", "pick",
                "pack", "carrier_handoff", "customs", "sales_tax", "tracking",
                "returns"]
MONEY_LEDGER_KINDS = ["settlement", "refund", "reversal", "presale_held",
                      "payout", "fee"]

GATED_LISTING = "holder-work-jacket"
HOLDER_PRICE_MINOR = 5900
PUBLIC_PRICE_MINOR = 8900
COLLECTION = "kilnfolk-genesis"

ORDER_REFERENCE_PREFIX = "KLN-"
SEEDED_ORDER_REFERENCE = "KLN-000412"
TOKEN_QUOTE_MINUTES = 15
CONFIRMATION_DEPTH = 12

TAX_JURISDICTIONS = {"NL": ("21", "per_invoice"), "GB": ("20", "per_invoice"),
                     "US-CA": ("8.5", "per_line")}
NL_LINES = [3333, 3333, 3334]
NL_INVOICE_TAX = 2100
NL_ALLOCATION = [700, 700, 700]
NEXUS_THRESHOLD_MINOR = 10000000

RETURN_WINDOW_DAYS = 30
RETURN_DISPOSITIONS = ["restock", "refurbish", "write_off"]

DROP_SLUG = "kilnfolk-winter"
DROP_SUPPLY = 40
DROP_ALLOWANCE = 2
GACHA_ODDS = {"common": "0.70", "rare": "0.25", "grail": "0.05"}
PRESALE_THRESHOLD_MINOR = 5000000

PROCEDURE_VERSIONS = 3
ANNOUNCEMENT_SUBJECT = "Kilnfolk winter drop opens Friday"
ORDER_SUBJECT_PREFIX = "Kilnly order confirmed: "
PROMISE_SUBJECT_PREFIX = "Kilnly delivery update: "
RETURN_SUBJECT_PREFIX = "Kilnly return authorised: "

LOT_COSTS = [5144, 6010]

BILLING_BASIC_USER = "admin"
BILLING_BASIC_PASSWORD = "password"
BILLING_HEADER_KEY = "X-Killbill-ApiKey"
BILLING_HEADER_SECRET = "X-Killbill-ApiSecret"

FRONTEND = "SolidJS"
BACKEND = "Litestar"
INTERFACE_FAMILY = "Inter"
DISPLAY_FAMILY = "Baloo 2"
BODY_SIZE_PX = "16px"
DENSE_SIZE_PX = "14px"

HERO_HEADLINE = "Create your dream merch on autopilot"
POSITIONING_LINE = "Grow your brand, not your ops."
FIRST_PANEL = "Find your ideal suppliers."
FIRST_PILL = "emailing 12 manufacturers"
FIRST_REEL_LINE = "Pondering manufacturers..."
REEL_LINE_COUNT = 12
MENU_LABELS = ["Past drops", "Kilnfolk"]
WHITELIST_LINK = "Whitelist"
COPYRIGHT_LINE = "(C) 2026 Kilnly"
FOOTER_COLUMNS = ["Past drops", "Resources", "Community", "Social"]
CATALOGUE_HEADING = "Latest productions"
FULFILLMENT_HEADING = "Merch fulfillment, end to end."
OPS_FIGURE_LINE = "11 Ops surfaces we run"
MINIMUM_FIGURE_LINE = "1 Minimum order"
DEMO_PILL = "Book a demo"

DATABASE_URL_VAR = "DATABASE_URL"
SMTP_HOST_VAR = "SMTP_HOST"
PAYMENTS_API_URL_VAR = "PAYMENTS_API_URL"
APP_PUBLIC_URL_VAR = "APP_PUBLIC_URL"
APP_PUBLIC_PORT_VAR = "APP_PUBLIC_PORT"
HEALTH_ROUTE = "/api/health"
CREDENTIALS_FILE = "/app/USER_README.md"
BIND_ADDRESS = "0.0.0.0"
SCREENSHOT_DIR = ".browser_screenshots/"
DOWNLOAD_DIR = ".downloads/"
CONTAINER_PORT = "4173"

OK_CREATED = (200, 201)
DENIED = (401, 403)
REFUSED = (400, 409, 422)
CONFLICT = 409
CLIENT_ERROR = range(400, 500)
LARGE_ROW_COUNT = 10000


def app_url() -> str:
    return os.environ[APP_PUBLIC_URL_VAR].rstrip("/")


def api_base() -> str:
    return f"{app_url()}/api"


def excerpt(response: httpx.Response) -> str:
    return response.text[:300]


def settle(predicate, limit: float = SETTLE_LIMIT):
    """Poll a predicate until it returns a truthy value, or give up.

    The only sanctioned sleep in this layer. Returns whatever the predicate
    last returned, so a caller asserts on the value rather than on the wait.
    """
    deadline = time.monotonic() + limit
    value = predicate()
    while not value and time.monotonic() < deadline:
        time.sleep(SETTLE_STEP)
        value = predicate()
    return value


def probe_email() -> str:
    return f"probe-{uuid.uuid4().hex[:12]}@example.com"


def probe_key() -> str:
    return f"probe-{uuid.uuid4().hex[:16]}"


def anon() -> httpx.Client:
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT)


def site() -> httpx.Client:
    return httpx.Client(base_url=app_url(), timeout=TIMEOUT,
                        follow_redirects=True)


def sign_in(email: str, password: str = SEED_PASSWORD) -> httpx.Response:
    with anon() as client:
        return client.post("/auth/sign-in",
                           json={"email": email, "password": password})


def token_for(email: str, password: str = SEED_PASSWORD) -> str:
    response = sign_in(email, password)
    assert response.status_code == 200, (
        f"POST /api/auth/sign-in for {email} returned {response.status_code}, "
        f"expected 200: {excerpt(response)}")
    token = response.json().get("access_token")
    assert token, (
        f"POST /api/auth/sign-in for {email} returned 200 with no access_token "
        f"field: {excerpt(response)}")
    return token


def bearer(token: str) -> httpx.Client:
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT,
                        headers={"Authorization": f"Bearer {token}"})


def as_role(email: str) -> httpx.Client:
    return bearer(token_for(email))


def create_account(email: str | None = None,
                   display_name: str = "Probe Buyer",
                   password: str = SEED_PASSWORD) -> tuple[str, str]:
    email = email or probe_email()
    with anon() as client:
        response = client.post("/auth/sign-up", json={
            "display_name": display_name, "email": email, "password": password})
    assert response.status_code in OK_CREATED, (
        f"POST /api/auth/sign-up for {email} returned {response.status_code}, "
        f"expected one of {OK_CREATED}: {excerpt(response)}")
    token = response.json().get("access_token") or token_for(email, password)
    return email, token


def json_array(response: httpx.Response, where: str) -> list:
    assert response.status_code == 200, (
        f"{where} returned {response.status_code}, expected 200: "
        f"{excerpt(response)}")
    rows = response.json()
    assert isinstance(rows, list), (
        f"{where} did not return a top-level JSON array: {str(rows)[:300]}")
    return rows


def products(category: str | None = None) -> list[dict]:
    params = {"category": category} if category else None
    with anon() as client:
        response = client.get("/products", params=params)
    return json_array(response, "GET /api/products")


def product_by_slug(slug: str) -> dict:
    for row in products():
        if row.get("slug") == slug:
            return row
    raise AssertionError(
        f"GET /api/products carries no product with slug {slug!r}; the eight "
        f"seeded slugs are pinned in the brief")


def inventory(sku: str | None = None, location: str | None = None) -> list[dict]:
    params = {}
    if sku:
        params["sku"] = sku
    if location:
        params["location"] = location
    with anon() as client:
        response = client.get("/inventory", params=params or None)
    return json_array(response, "GET /api/inventory")


def available(sku: str, location: str) -> int:
    for row in inventory(sku, location):
        if row.get("sku") == sku and row.get("location") == location:
            return int(row["available"])
    raise AssertionError(
        f"GET /api/inventory carries no row for sku {sku!r} at location "
        f"{location!r}; both are pinned in the brief")


def shop(client: httpx.Client) -> list[dict]:
    return json_array(client.get("/shop"), "GET /api/shop")


def place_order(client: httpx.Client, listing_slug: str, units: int = 1,
                buyer_email: str | None = None, destination: str = "NL",
                rail: str = "fiat", key: str | None = None) -> httpx.Response:
    headers = {"Idempotency-Key": key or probe_key()}
    body = {
        "lines": [{"listing_slug": listing_slug, "units": units}],
        "buyer_email": buyer_email or probe_email(),
        "destination": destination,
        "rail": rail,
    }
    return client.post("/orders", json=body, headers=headers)


def read_order(reference: str, access_token: str) -> httpx.Response:
    with anon() as client:
        return client.get(f"/orders/{reference}",
                          params={"access_token": access_token})


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def inbox():
    return capabilities.make_inbox()


@pytest.fixture(scope="session")
def payments():
    return capabilities.make_payments()


@pytest.fixture()
def anonymous():
    with anon() as client:
        yield client


@pytest.fixture()
def public():
    with site() as client:
        yield client


@pytest.fixture()
def owner():
    with as_role(OWNER_EMAIL) as client:
        yield client


@pytest.fixture()
def operator():
    with as_role(OPERATOR_EMAIL) as client:
        yield client


@pytest.fixture()
def finance():
    with as_role(FINANCE_EMAIL) as client:
        yield client


@pytest.fixture()
def viewer():
    with as_role(VIEWER_EMAIL) as client:
        yield client


@pytest.fixture()
def owner_two():
    with as_role(OWNER2_EMAIL) as client:
        yield client


@pytest.fixture()
def holder():
    with as_role(BUYER_EMAIL) as client:
        yield client


@pytest.fixture()
def plain_buyer():
    with as_role(BUYER2_EMAIL) as client:
        yield client


@pytest.fixture()
def fresh_buyer():
    email, token = create_account()
    with bearer(token) as client:
        client.probe_email = email
        yield client
