"""Task fixtures for deku/accessible-watch-storefront-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout or
module names. The only assumptions are the App Contract (the app answers at
APP_PUBLIC_URL with REST under /api) and the literals instruction.md pinned: the
routes, the payload field names, the nine table names, the twelve home products,
the three colourway sets and the two display currencies.

Provider agnostic: the store, the inbox and the billing helpers are composed from the
generic primitives in capabilities.py, never from a provider SDK.
"""

from __future__ import annotations

import os
import time

import httpx
import pytest
from appclient import api_base, app_url, client
from capabilities import Backend, Inbox, Payments, make_backend, make_inbox, make_payments

HOME_ROUTE = "/"
CART_ROUTE = "/cart"
CHECKOUT_ROUTE = "/checkout"
CATCH_ALL_ROUTE = "/collections/all"
SITEMAP_ROUTE = "/sitemap.xml"
ROBOTS_ROUTE = "/robots.txt"
ACCOUNT_HANDOFF_ROUTE = "/customer_authentication/redirect"

CURATED_HANDLES = (
    "mens-watches",
    "womens-watches",
    "couple-watches",
    "car-watches",
    "quartz-watches",
    "mechanical-watches",
    "automatic-watch",
    "best-sellers",
    "2-watch-bundle-offer",
    "watch-accessories",
)
CATCH_ALL_HANDLE = "all"

AUTHORED_PAGE_ROUTES = (
    "/pages/about-us",
    "/pages/contact",
    "/pages/faq",
    "/pages/volari-warranty",
    "/pages/payment-delivery",
)
POLICY_ROUTES = (
    "/policies/refund-policy",
    "/policies/shipping-policy",
    "/policies/privacy-policy",
    "/policies/terms-of-service",
    "/policies/legal-notice",
    "/policies/contact-information",
)
BLOG_ROUTE = "/blogs/watch-guide"

PUBLIC_ROUTES = (
    (HOME_ROUTE, CART_ROUTE, CATCH_ALL_ROUTE)
    + tuple(f"/collections/{h}" for h in CURATED_HANDLES)
    + AUTHORED_PAGE_ROUTES
    + (BLOG_ROUTE,)
    + POLICY_ROUTES
)

CATALOGUE_TOTAL = 174
IN_STOCK_COUNT = 161
OUT_OF_STOCK_COUNT = 13
PAGE_SIZE = 16
PAGE_COUNT = 11

STORE_CURRENCY = "usd"
DISPLAY_CURRENCIES = ("USD", "INR")
INR_RATE = 88.0
USD_PREFIX = "$"
INR_PREFIX = "Rs."
WORKED_USD = "$ 124.00 USD"
WORKED_INR = "Rs. 10,912.00 INR"
WORKED_MINOR = 12400

UPSELL_HANDLE = "shipping-protection"
UPSELL_TITLE = "Shipping Protection"
UPSELL_PRICE_MINOR = 1000
UPSELL_COMPARE_MINOR = 2000
UPSELL_DESCRIPTION = (
    "Protect your order from damage, loss, or theft during shipping."
)

SALE_BADGE = "Sale"
BUNDLE_BADGE = "Buy 1 Get 1 Free"

HOME_PRODUCTS = (
    ("VOLARI 2628 - Timeless Luxury Quartz Watch", 37400, 18700, True, "4.6", 154),
    ("VOLARI 2653 Sport Silicone Watch", 29000, 14500, True, "5.0", 56),
    ("VOLARI 2632 - Waterproof Stainless Steel Watch", 16000, 8000, False, "4.9", 35),
    ("VOLARI 2627 - Diamond Scale Quartz Watch", 14400, 10400, False, "4.3", 142),
    ("VOLARI 2309 - Luxury Quartz Chronograph Waterproof Watch", 18600, 9300, False,
     "4.5", 176),
    ("VOLARI 2638 - Classic Fluted Men's Watch", 20400, 10200, False, "4.9", 8),
    ("VOLARI 2506 - Rebel Face Watch", 24800, 12400, False, "4.5", 197),
    ("VOLARI 2653 Steel - Classic Edition", 24800, 12400, True, "4.9", 11),
    ("VOLARI 2622 - Elegant Zircon Women's Quartz Watch", 20600, 9300, False,
     "4.9", 15),
    ("VOLARI 2697 - Women's Business Watch", 13000, 9200, False, "4.9", 22),
    ("VOLARI 2357 - Crystal Elegance Women's Watch", 12600, 10100, False, "5.0", 12),
    ("VOLARI 2675 - Dreamy Fish Tail Watch", 10500, 8400, False, "4.8", 12),
)

REBEL_HANDLE = "volari-2506-rebel-face-watch"
REBEL_TITLE = "VOLARI 2506 - Rebel Face Watch"
REBEL_COMPARE_MINOR = 24800
REBEL_OPTION_NAME = "Color"
REBEL_COLOURWAYS = (
    ("Green Black", 12400, True),
    ("Black Red", 12400, False),
    ("Green White", 12400, True),
    ("Red White", 12400, True),
    ("Red Black", 12400, True),
)
REBEL_OFFER_LINE = "Exclusive Online Offer - Save 50%"

DIAMOND_TITLE = "VOLARI 2627 - Diamond Scale Quartz Watch"
DIAMOND_COLOURWAYS = (
    ("Rose Gold", 9900, False),
    ("Steel Silver", 10400, True),
    ("Gold", 11900, True),
)
DIAMOND_CHEAPEST_AVAILABLE_MINOR = 10400

BUSINESS_TITLE = "VOLARI 2697 - Women's Business Watch"
BUSINESS_COLOURWAYS = (
    ("Silver", 9200, True),
    ("Gold", 10600, True),
)

SORT_OPTIONS = (
    "Featured",
    "Most relevant",
    "Best selling",
    "Alphabetically, A-Z",
    "Alphabetically, Z-A",
    "Price, low to high",
    "Price, high to low",
    "Date, old to new",
    "Date, new to old",
)

OTHER_MAKER_TITLES = (
    "ADDIESDIVE AD2503 Oceanmaster Automatic - Miyota 8215",
    "CRRJU 2165 Grace Minimalist Quartz",
    "LONGLUX 6269K2 Vanguard Skeleton Automatic",
    "LONGLUX 8020P Heritage Open Heart Mechanical",
    "LONGLUX 8057G Apex Skeleton Mechanical",
    "LUMINOUS MILITARY Heritage Automatic",
)

SIGNUP_SUBJECT_PREFIX = "Your 10% code: "
SIGNUP_CODE = "VOLARI10"
SIGNUP_SUBJECT = "Your 10% code: VOLARI10"
BRAND_FULL = "Volari Official"

APP_ROOT = "/app"
USER_README_PATH = "/app/USER_README.md"
REQUEST_LOG_PATH = "/app/logs/requests.log"
RESERVED_DIRECTORIES = ("/app/.browser_screenshots", "/app/.downloads")
REQUEST_LOG_KEYS = ("method", "path")

SECURITY_HEADER_NAMES = ("strict-transport-security", "x-content-type-options")
NOSNIFF_VALUE = "nosniff"

CART_FIELDS = ("token", "currency", "lines", "unit_count", "subtotal", "discount_code")
CART_LINE_FIELDS = ("key", "variant_id", "handle", "title", "maker", "option_name",
                    "option_value", "image", "unit_price", "compare_at", "quantity",
                    "line_total", "removable")
COLLECTION_FIELDS = ("title", "description", "count", "facets", "products", "page",
                     "pages")
CARD_FIELDS = ("handle", "title", "maker", "badges", "rating", "price", "compare_at")
PRICE_FIELDS = ("amount_minor", "formatted", "from")
PRODUCT_FIELDS = ("handle", "title", "maker", "model", "body", "features", "includes",
                  "rating", "badges", "media", "option_name", "variants")
VARIANT_FIELDS = ("id", "option_value", "price", "compare_at", "available",
                  "media_seed")
CHECKOUT_FIELDS = ("reference", "lines", "unit_count", "total", "currency")

CATALOGUE_TABLES = ("products", "variants", "collections", "collection_products")

WRITE_PROBES = (
    ("POST", "/products"),
    ("POST", "/variants"),
    ("PUT", "/products/volari-2506-rebel-face-watch"),
    ("PATCH", "/collections/all"),
    ("DELETE", "/products/volari-2506-rebel-face-watch"),
    ("POST", "/collections"),
)

SETTLE_SECONDS = 0.5
POLL_ATTEMPTS = 20


def settle() -> None:
    """The one sanctioned pause, used only between polls for an async side effect."""
    time.sleep(SETTLE_SECONDS)


def probe_email() -> str:
    """A unique address per run, so one inbox serves repeated runs."""
    return f"probe-{os.urandom(6).hex()}@example.com"


def probe_reference() -> str:
    return f"probe-order-{os.urandom(6).hex()}"


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture()
def fresh_client():
    """A client with its own cart, so one workflow's cart never leaks into another."""
    with httpx.Client(base_url=api_base(), timeout=30.0) as c:
        yield c


@pytest.fixture(scope="session")
def site():
    with httpx.Client(base_url=app_url(), timeout=30.0,
                      follow_redirects=True) as c:
        yield c


class ShopStore:
    """Domain reads for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def count(self, table: str, **where) -> int:
        return self._b.count(table, **where)

    def rows(self, table: str, limit: int | None = None, **where) -> list[dict]:
        return self._b.rows(table, limit=limit, **where)

    def one(self, table: str, **where) -> dict | None:
        return self._b.one(table, **where)

    def product(self, handle: str) -> dict | None:
        return self._b.one("products", handle=handle)

    def variants_of(self, handle: str) -> list[dict]:
        return self._b.rows("variants", product_handle=handle)

    def order(self, reference: str) -> dict | None:
        return self._b.one("orders", reference=reference)


@pytest.fixture(scope="session")
def store() -> ShopStore:
    return ShopStore(make_backend())


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    return make_inbox()


@pytest.fixture(scope="session")
def payments() -> Payments:
    return make_payments()


def collection(http_client, handle: str = CATCH_ALL_HANDLE, **params) -> dict:
    response = http_client.get(f"/collections/{handle}", params=params or None)
    assert response.status_code == 200, (
        f"GET {api_base()}/collections/{handle} with {params!r} returned "
        f"{response.status_code}, expected 200: {response.text[:400]}"
    )
    body = response.json()
    assert isinstance(body, dict), (
        f"GET {api_base()}/collections/{handle} must return an object carrying "
        f"{list(COLLECTION_FIELDS)}, got {type(body).__name__}: {response.text[:400]}"
    )
    for field in COLLECTION_FIELDS:
        assert field in body, (
            f"the collection payload for {handle!r} carries no {field!r} key; it "
            f"carries {sorted(body)}"
        )
    return body


def product(http_client, handle: str, **params) -> dict:
    response = http_client.get(f"/products/{handle}", params=params or None)
    assert response.status_code == 200, (
        f"GET {api_base()}/products/{handle} returned {response.status_code}, "
        f"expected 200: {response.text[:400]}"
    )
    body = response.json()
    for field in PRODUCT_FIELDS:
        assert field in body, (
            f"the product payload for {handle!r} carries no {field!r} key; it "
            f"carries {sorted(body)}"
        )
    return body


def cart(http_client, **params) -> dict:
    response = http_client.get("/cart", params=params or None)
    assert response.status_code == 200, (
        f"GET {api_base()}/cart returned {response.status_code}, expected 200: "
        f"{response.text[:400]}"
    )
    body = response.json()
    for field in CART_FIELDS:
        assert field in body, (
            f"the cart payload carries no {field!r} key; it carries {sorted(body)}"
        )
    return body


def add_line(http_client, variant_id, quantity: int = 1) -> dict:
    response = http_client.post("/cart/lines",
                                json={"variant_id": variant_id,
                                      "quantity": quantity})
    assert response.status_code in (200, 201), (
        f"POST {api_base()}/cart/lines with variant {variant_id!r} returned "
        f"{response.status_code}, expected 200 or 201: {response.text[:400]}"
    )
    body = response.json()
    for field in CART_FIELDS:
        assert field in body, (
            f"a cart mutation must return the WHOLE cart; the response carries no "
            f"{field!r} key, only {sorted(body)}"
        )
    return body


def first_available_variant(payload: dict) -> dict:
    for variant in payload["variants"]:
        if variant.get("available"):
            return variant
    raise AssertionError(
        f"product {payload.get('handle')!r} carries no available variant: "
        f"{payload['variants']}"
    )


def find_message(inbox_handle, address: str, subject_part: str):
    """Bounded polling for an async side effect; never an unbounded retry."""
    for _ in range(POLL_ATTEMPTS):
        found = inbox_handle.find(address, subject_part)
        if found is not None:
            return found
        settle()
    return None


def find_account(payments_handle, external_key: str) -> dict | None:
    for account in payments_handle.accounts():
        if account.get("externalKey") == external_key:
            return account
    return None


def poll_account(payments_handle, external_key: str) -> dict | None:
    for _ in range(POLL_ATTEMPTS):
        found = find_account(payments_handle, external_key)
        if found is not None:
            return found
        settle()
    return None
