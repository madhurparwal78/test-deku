"""Task fixtures for deku/time-literacy-storefront-vb.

Implementation agnostic: nothing here assumes the framework, the file layout, an
ORM or a module name. What it assumes is the App Contract and whatever
instruction.md pinned: the route shapes, the access_token login key, the seeded
accounts, the table and column names, the skus, the subject prefixes, the dial
hooks and the copy strings.

Provider agnostic: the store helpers are composed from the generic primitives in
capabilities.py, never from a provider SDK. Kill Bill is read through the payments
adapter, Mailpit through the inbox adapter.
"""

from __future__ import annotations

import html
import os
import re
import threading
import time
from datetime import datetime, timezone
from urllib.parse import unquote, urlparse

import httpx
import pytest
from appclient import api_base, app_url, client, login, seeded_password
from capabilities import Backend, Inbox, Payments, make_backend, make_inbox, make_payments
from playwright.sync_api import expect, sync_playwright

SETTLE_SECONDS = 2.0
POLL_INTERVAL = 0.5
POLL_CEILING = 30.0
UI_TIMEOUT_MS = 15000


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give an unwanted side effect time to land before asserting it did not."""
    time.sleep(seconds)


def poll_until(predicate, ceiling: float = POLL_CEILING):
    """Bounded poll for an asynchronous side effect. Returns the last value seen."""
    deadline = time.monotonic() + ceiling
    value = predicate()
    while not value and time.monotonic() < deadline:
        settle(POLL_INTERVAL)
        value = predicate()
    return value


SEEDED_PASSWORD = "deku-demo-pw-2026"
CUSTOMER_EMAIL = "customer@example.com"
CUSTOMER2_EMAIL = "customer2@example.com"
OWNER_EMAIL = "owner@example.com"
CUSTOMER_NAME = "Casey Rivera"
CUSTOMER2_NAME = "Jordan Lee"
OWNER_NAME = "Mara Ellison"

SIGN_IN_SUBJECT = "Your Tock sign-in link"
CONFIRMATION_PREFIX = "Tock order confirmed:"
ADDRESS_NEEDED_PREFIX = "Address needed:"
RESTOCK_PREFIX = "Back in stock:"
SPENT_LINK_COPY = "This sign-in link is no longer valid."
SEND_NEW_LINK = "Send a new link"
LINK_MARKER = "/account/link/"

AQUA = "tock-33-aqua"
NAVY = "tock-33-navy"
FUCHSIA = "tock-33-fuchsia"
GLOW33 = "tock-33-glow"
GREY38 = "tock-38-grey"
BLACK38 = "tock-38-black"
GLOW38 = "tock-38-glow"
SHARK38 = "tock-38-shark"
MINT31 = "tock-31-mint"
LILAC_DRAFT = "tock-33-lilac"
BUNDLE_BLACK_NAVY = "bundle-black-navy"
BUNDLE_GREY_AQUA = "bundle-grey-aqua"
BUNDLE_GLOW_GLOW = "bundle-glow-glow"
BUNDLE_SHARK_FUCHSIA = "bundle-shark-fuchsia"
WOVEN_SAND = "strap-woven-sand"
RUBBER_NAVY = "strap-rubber-navy"
RUBBER_FUCHSIA = "strap-rubber-fuchsia"
NATO_AQUA = "strap-nato-aqua"
NATO_NAVY = "strap-nato-navy"
TOTE = "tote-bone"
BEANIE = "beanie-navy"

SKU_AQUA = "TK33-AQUA"
SKU_NAVY = "TK33-NAVY"
SKU_FUCHSIA = "TK33-FUCHSIA"
SKU_GLOW33 = "TK33-GLOW"
SKU_GREY38 = "TK38-GREY"
SKU_BLACK38 = "TK38-BLACK"
SKU_GLOW38 = "TK38-GLOW"
SKU_SHARK38 = "TK38-SHARK"
SKU_LILAC = "TK33-LILAC"
SKU_BUNDLE_BLACK_NAVY = "BNDL-BLACK-NAVY"
SKU_BUNDLE_GREY_AQUA = "BNDL-GREY-AQUA"
SKU_BUNDLE_GLOW_GLOW = "BNDL-GLOW-GLOW"
SKU_WOVEN_SAND_S = "STRAP-WOVEN-SAND-S"
SKU_WOVEN_SAND_L = "STRAP-WOVEN-SAND-L"
SKU_RUBBER_NAVY_S = "STRAP-RUBBER-NAVY-S"
SKU_RUBBER_NAVY_L = "STRAP-RUBBER-NAVY-L"
SKU_RUBBER_FUCHSIA_S = "STRAP-RUBBER-FUCHSIA-S"
SKU_RUBBER_FUCHSIA_L = "STRAP-RUBBER-FUCHSIA-L"
SKU_NATO_AQUA = "STRAP-NATO-AQUA"
SKU_NATO_NAVY = "STRAP-NATO-NAVY"
SKU_TOTE = "TOTE-BONE"
SKU_BEANIE = "BEANIE-NAVY"

PRICE_AQUA = 18900
PRICE_NATO = 2200
PRICE_TOTE = 2000
FLAT_SHIPPING = 1500
GIFT_PROMOTION = "Gift with purchase"
PROMOTION_REMOVED_MESSAGE = ("The free tote and beanie were removed because your cart no "
                             "longer holds a watch.")
TOTE_UNAVAILABLE_MESSAGE = "The free Tock Tote is out of stock."
TOCK31_NOTICE = "TOCK 31 is discontinued. Every watch in this family has sold out."
ANNOUNCEMENT = "BUY ANY TOCK, GET A TOTE AND BEANIE FOR FREE"
COMPLETE_SET_NOTICE = ("This is a two-watch set and can only be returned complete. Individual "
                       "watches from a set cannot be returned separately.")
PO_BOX_RULE = ("We do not ship to PO Boxes. If an order is placed to a PO Box, a customer "
               "service liaison will reach out to receive an alternative address. If we "
               "cannot confirm a new address within 5 business days, your order will be "
               "canceled and fully refunded.")
ABOUT_CLOSE = ("We trust that you will find our products to be accurate, handsome, useful "
               "and, most importantly, indestructible.")
SPEC_KEYS = ["Case", "Bezel", "Movement", "Bezel Marquetry", "Dial", "Hands", "Lens",
             "Crown", "Band", "Buckle", "Water Resistance", "Theoretical Battery life",
             "Accuracy", "Warranty"]
EDITORIAL_HEADINGS = ["Innovative Time System", "Strap In", "Lume Say What?",
                      "Case in Point", "Dive! Dive! Dive!", "The Swissness", "Scratch That"]
TOCK_STARTS = {5: 0, 10: 5, 15: 15, 30: 30}
POLICY_CLAUSES = ("profanity", "personal-data", "off-topic", "spam")
COLLECTIONS = ["tock-33", "tock-38", "tock-31", "bundles", "straps", "all"]
CONTENT_PAGES = ["/pages/about", "/pages/faq", "/pages/user-guide",
                 "/pages/shipping-and-returns", "/pages/contact-us", "/pages/privacy",
                 "/pages/terms"]
PUBLIC_ROUTES = (["/"] + [f"/collections/{c}" for c in COLLECTIONS] + ["/search"]
                 + CONTENT_PAGES + [f"/products/{AQUA}", f"/products/{BUNDLE_BLACK_NAVY}",
                                    f"/products/{WOVEN_SAND}"])
PUBLISHED_HANDLES = [AQUA, NAVY, FUCHSIA, GLOW33, GREY38, BLACK38, GLOW38, SHARK38, MINT31,
                     BUNDLE_BLACK_NAVY, BUNDLE_GREY_AQUA, BUNDLE_GLOW_GLOW,
                     BUNDLE_SHARK_FUCHSIA, WOVEN_SAND, RUBBER_NAVY, RUBBER_FUCHSIA,
                     NATO_AQUA, NATO_NAVY, TOTE, BEANIE]
COMPARISON_TIMES = [(158, "2:38", "79", "2", "Somewhere between 2 and 3?", "It's in the 2. 2:38."),
                    (544, "9:04", "272", "9", "Somewhere between 9 and 10?", "It's in the 9. 9:04."),
                    (15, "12:15", "7.5", "12", "Somewhere between 12 and 1?", "It's in the 12. 12:15."),
                    (719, "11:59", "359.5", "11", "Somewhere between 11 and 12?", "It's in the 11. 11:59."),
                    (180, "3:00", "90", "3", "Somewhere between 3 and 4?", "It's in the 3. 3:00.")]
QUOTE_FOLDS = ((chr(0x2019), "'"), (chr(0x2018), "'"), (chr(0x201C), '"'), (chr(0x201D), '"'),
               (chr(0x2013), "-"), (chr(0x2014), "-"), (chr(0x00A0), " "))
HEAD_RE = re.compile(r"<head\b.*?</head>", re.S | re.I)
SCRIPT_RE = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")
HREF_RE = re.compile(r"""href\s*=\s*["']([^"']*)["']""", re.I)
ORDER_NUMBER_RE = re.compile(r"^TK-[A-Z0-9]{8}$")
REFERENCE_RE = re.compile(r"^SR-[A-Z0-9]{8}$")


def unique_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


def unique_key() -> str:
    return f"key-{os.urandom(8).hex()}"


def unique_title(prefix: str = "Probe review") -> str:
    return f"{prefix} {os.urandom(4).hex()}"


def base_url() -> str:
    return app_url()


def api_url() -> str:
    return api_base()


def us_address(line1: str = "12 Harbor Street", line2: str = "") -> dict:
    return {"name": "Probe Buyer", "line1": line1, "line2": line2, "city": "Portland",
            "region": "OR", "postcode": "97201", "country": "US"}


def expect_client_error(response: httpx.Response, what: str) -> None:
    assert 400 <= response.status_code < 500, (
        f"{what} returned {response.status_code}, expected a 4xx client error: "
        f"{response.text[:400]}")


def safe_json(response: httpx.Response):
    """The JSON body, or None when the response does not declare JSON."""
    if "json" not in response.headers.get("content-type", "").lower():
        return None
    return response.json()


def ok_json(response: httpx.Response, what: str):
    assert response.status_code in (200, 201), (
        f"{what} returned {response.status_code}: {response.text[:400]}")
    return response.json()


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture
def customer_client():
    token = login(CUSTOMER_EMAIL, seeded_password("SEED_CUSTOMER_PASSWORD", SEEDED_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture
def customer2_client():
    token = login(CUSTOMER2_EMAIL, seeded_password("SEED_CUSTOMER2_PASSWORD", SEEDED_PASSWORD))
    with client(token) as c:
        yield c


@pytest.fixture
def owner_client():
    token = login(OWNER_EMAIL, seeded_password("SEED_OWNER_PASSWORD", SEEDED_PASSWORD))
    with client(token) as c:
        yield c


def signup(email: str | None = None, password: str = "probe-pass-2026x",
           name: str = "Probe Buyer") -> tuple[str, str]:
    email = email or unique_email()
    with client() as c:
        response = c.post("/auth/signup",
                          json={"email": email, "password": password, "name": name})
    assert response.status_code in (200, 201), (
        f"POST /api/auth/signup for {email} returned {response.status_code}: "
        f"{response.text[:400]}")
    token = response.json().get("access_token")
    assert token, f"signup for {email} returned no access_token: {response.text[:400]}"
    return email, token


@pytest.fixture
def fresh_customer():
    email, token = signup()
    with client(token) as c:
        yield email, c


@pytest.fixture
def second_fresh_customer():
    email, token = signup()
    with client(token) as c:
        yield email, c


class StoreDb:
    """Domain queries for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def account(self, email: str) -> dict | None:
        return self._b.one("accounts", email=email)

    def count_accounts(self, email: str) -> int:
        return self._b.count("accounts", email=email)

    def product(self, handle: str) -> dict | None:
        return self._b.one("products", handle=handle)

    def count_products(self, handle: str) -> int:
        return self._b.count("products", handle=handle)

    def variant(self, sku: str) -> dict | None:
        return self._b.one("variants", sku=sku)

    def count_variants(self, sku: str) -> int:
        return self._b.count("variants", sku=sku)

    def inventory(self, sku: str) -> dict | None:
        variant = self.variant(sku)
        assert variant is not None, f"no variants row carries sku {sku!r}"
        return self._b.one("inventory_items", variant_id=variant["id"])

    def count_inventory_for_variant(self, variant_id) -> int:
        return self._b.count("inventory_items", variant_id=variant_id)

    def inventory_rows(self) -> list[dict]:
        return self._b.rows("inventory_items")

    def ledger_rows(self, inventory_item_id) -> list[dict]:
        return self._b.rows("stock_ledger", inventory_item_id=inventory_item_id)

    def all_ledger_rows(self) -> list[dict]:
        return self._b.rows("stock_ledger")

    def held_reservations(self, inventory_item_id) -> list[dict]:
        return self._b.rows("reservations", inventory_item_id=inventory_item_id,
                            status="held")

    def all_held_reservations(self) -> list[dict]:
        return self._b.rows("reservations", status="held")

    def cart(self, token: str) -> dict | None:
        return self._b.one("carts", token=token)

    def cart_line_rows(self, cart_id) -> list[dict]:
        return self._b.rows("cart_lines", cart_id=cart_id)

    def cart_reservations(self, cart_id) -> list[dict]:
        return self._b.rows("reservations", cart_id=cart_id)

    def order(self, number: str) -> dict | None:
        return self._b.one("orders", number=number)

    def count_order_numbers(self, number: str) -> int:
        return self._b.count("orders", number=number)

    def count_orders(self, account_id, idempotency_key: str) -> int:
        return self._b.count("orders", account_id=account_id,
                             idempotency_key=idempotency_key)

    def count_account_orders(self, account_id) -> int:
        return self._b.count("orders", account_id=account_id)

    def order_lines(self, order_id) -> list[dict]:
        return self._b.rows("order_lines", order_id=order_id)

    def review(self, review_id) -> dict | None:
        return self._b.one("reviews", id=review_id)

    def count_reviews(self, product_id, account_id) -> int:
        return self._b.count("reviews", product_id=product_id, account_id=account_id)

    def count_seeded_reviews(self, product_id, author_name: str) -> int:
        return self._b.count("reviews", product_id=product_id, author_name=author_name)

    def accounts(self) -> list[dict]:
        return self._b.rows("accounts")

    def columns_of(self, table: str) -> list[str]:
        """Column names of one table, read through the backend's own query seam."""
        rows = self._b.query("SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table,))
        return [row["column_name"] for row in rows]

    def rows_of(self, table: str) -> list[dict]:
        return self._b.rows(table)

    def reply_for(self, review_id) -> dict | None:
        return self._b.one("review_replies", review_id=review_id)

    def seeded_review(self, product_id, author_name: str) -> dict | None:
        return self._b.one("reviews", product_id=product_id, author_name=author_name)

    def count_replies(self, review_id) -> int:
        return self._b.count("review_replies", review_id=review_id)

    def count_waiting_subscriptions(self, product_id, email: str) -> int:
        return self._b.count("restock_subscriptions", product_id=product_id, email=email,
                             status="waiting")

    def subscriptions(self, product_id, email: str) -> list[dict]:
        return self._b.rows("restock_subscriptions", product_id=product_id, email=email)

    def waiting_subscriptions(self) -> list[dict]:
        return self._b.rows("restock_subscriptions", status="waiting")

    def count_support_requests(self, email: str) -> int:
        return self._b.count("support_requests", email=email)

    def support_request(self, reference: str) -> dict | None:
        return self._b.one("support_requests", reference=reference)


@pytest.fixture(scope="session")
def db() -> StoreDb:
    return StoreDb(make_backend())


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    """The mail-server inbox, read out of band. Never smtplib here."""
    return make_inbox()


@pytest.fixture(scope="session")
def payments() -> Payments:
    """Kill Bill, read through the payments adapter."""
    return make_payments()


def killbill_account(payments: Payments, external_key: str) -> dict | None:
    for account in payments.accounts():
        if str(account.get("externalKey", "")) == external_key:
            return account
    return None


def killbill_accounts_keyed(payments: Payments, external_key: str) -> list[dict]:
    return [account for account in payments.accounts()
            if str(account.get("externalKey", "")).lower() == external_key.lower()]


def killbill_invoices(payments: Payments, account_id) -> list:
    return [charge for charge in payments.charges()
            if str(charge.metadata.get("accountId", "")) == str(account_id)]


def killbill_invoices_for_key(payments: Payments, external_key: str, at_least: int = 1):
    """Poll until the account keyed external_key carries at_least invoices.

    Returns (account or None, invoices seen)."""
    def seen():
        account = killbill_account(payments, external_key)
        if account is None:
            return None
        invoices = killbill_invoices(payments, account.get("accountId"))
        return (account, invoices) if len(invoices) >= at_least else None

    found = poll_until(seen)
    if found:
        return found
    account = killbill_account(payments, external_key)
    invoices = killbill_invoices(payments, account.get("accountId")) if account else []
    return account, invoices


def mail_subjects(inbox: Inbox, to: str) -> list[str]:
    """Every subject addressed to `to`, read through the inbox adapter."""
    return [message.subject for message in inbox._messages()
            if any(address.lower() == to.lower() for address in message.to)]


def messages_with_subject(inbox: Inbox, subject_contains: str) -> list:
    return [message for message in inbox._messages()
            if subject_contains.lower() in message.subject.lower()]


def stock_rows(owner) -> list[dict]:
    response = owner.get("/owner/stock")
    assert response.status_code == 200, (
        f"GET /api/owner/stock returned {response.status_code}: {response.text[:400]}")
    payload = response.json()
    assert isinstance(payload, list), (
        f"GET /api/owner/stock must be a top-level JSON array: {response.text[:400]}")
    return payload


def stock_row(owner, sku: str) -> dict:
    for row in stock_rows(owner):
        if row.get("sku") == sku:
            return row
    raise AssertionError(f"GET /api/owner/stock carries no row for sku {sku!r}")


def adjust(owner, sku: str, delta: int, reason: str = "probe adjustment"):
    return owner.post("/owner/stock-adjustments",
                      json={"sku": sku, "delta": delta, "reason": reason})


def set_available(owner, sku: str, target: int) -> dict:
    """Move on_hand so that available equals target. Returns the stock row after."""
    row = stock_row(owner, sku)
    delta = target - int(row["available"])
    if delta == 0:
        return row
    response = adjust(owner, sku, delta, "probe sets availability")
    assert response.status_code in (200, 201), (
        f"POST /api/owner/stock-adjustments {sku} delta {delta} returned "
        f"{response.status_code}: {response.text[:400]}")
    after = stock_row(owner, sku)
    assert int(after["available"]) == target, (
        f"after adjusting {sku} by {delta} available reads {after['available']}, "
        f"expected {target}")
    return after


def ensure_available(owner, sku: str, minimum: int) -> dict:
    row = stock_row(owner, sku)
    if int(row["available"]) >= minimum:
        return row
    return set_available(owner, sku, minimum)


def new_cart(anon) -> str:
    response = anon.post("/cart")
    assert response.status_code in (200, 201), (
        f"POST /api/cart returned {response.status_code}: {response.text[:400]}")
    token = response.json().get("token")
    assert token, f"POST /api/cart returned no token: {response.text[:400]}"
    return token


def cart_get(anon, token: str) -> httpx.Response:
    return anon.get("/cart", headers={"X-Cart-Token": token})


def cart_add(anon, token: str, sku: str, quantity: int = 1) -> httpx.Response:
    return anon.post("/cart/lines", json={"sku": sku, "quantity": quantity},
                     headers={"X-Cart-Token": token})


def cart_patch(anon, token: str, line_id, quantity: int) -> httpx.Response:
    return anon.patch(f"/cart/lines/{line_id}", json={"quantity": quantity},
                      headers={"X-Cart-Token": token})


def cart_delete(anon, token: str, line_id) -> httpx.Response:
    return anon.delete(f"/cart/lines/{line_id}", headers={"X-Cart-Token": token})


def added_cart(anon, token: str, sku: str, quantity: int = 1) -> dict:
    return ok_json(cart_add(anon, token, sku, quantity), f"adding {quantity} x {sku}")


def lines_of(cart: dict) -> list[dict]:
    return list(cart.get("lines") or [])


def line_for(cart: dict, sku: str, gift: bool = False) -> dict | None:
    for line in lines_of(cart):
        if line.get("sku") == sku and bool(line.get("is_gift")) == gift:
            return line
    return None


def gift_lines(cart: dict, sku: str) -> list[dict]:
    return [line for line in lines_of(cart) if line.get("sku") == sku and line.get("is_gift")]


@pytest.fixture
def carts(anon_client):
    """Opens carts for one test and releases every non-gift hold they took afterwards."""
    opened: list[str] = []

    def open_cart() -> str:
        token = new_cart(anon_client)
        opened.append(token)
        return token

    yield open_cart
    for token in opened:
        response = cart_get(anon_client, token)
        if response.status_code != 200:
            continue
        for line in lines_of(response.json()):
            if not line.get("is_gift"):
                cart_delete(anon_client, token, line["id"])


def race(requests: list[dict]) -> list:
    """Send every request at one instant from its own client behind a shared barrier."""
    gate = threading.Barrier(len(requests))
    results: list = [None] * len(requests)

    def run(index: int, spec: dict) -> None:
        with client(spec.get("token")) as c:
            gate.wait()
            results[index] = c.request(spec["method"], spec["path"], json=spec.get("json"),
                                       headers=spec.get("headers"))

    threads = [threading.Thread(target=run, args=(i, spec)) for i, spec in enumerate(requests)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=60)
    return results


def checkout(buyer, cart_token: str, key: str | None = None,
             address: dict | None = None) -> httpx.Response:
    headers = {"X-Cart-Token": cart_token}
    if key is not None:
        headers["Idempotency-Key"] = key
    return buyer.post("/checkout", json={"shipping_address": address or us_address()},
                      headers=headers)


def place_order(anon, buyer, skus: list[str], address: dict | None = None) -> dict:
    token = new_cart(anon)
    for sku in skus:
        response = cart_add(anon, token, sku, 1)
        assert response.status_code in (200, 201), (
            f"adding {sku} before checkout returned {response.status_code}: "
            f"{response.text[:400]}")
    response = checkout(buyer, token, unique_key(), address)
    assert response.status_code in (200, 201), (
        f"POST /api/checkout returned {response.status_code}: {response.text[:400]}")
    order = response.json()
    assert order.get("number"), f"checkout returned no order number: {response.text[:400]}"
    return order


def own_orders(buyer) -> list[dict]:
    response = buyer.get("/orders")
    payload = ok_json(response, "GET /api/orders")
    assert isinstance(payload, list), (
        f"GET /api/orders must be a top-level JSON array: {response.text[:400]}")
    return payload


def request_link(email: str, return_to: str = "/account") -> httpx.Response:
    with client() as c:
        return c.post("/auth/link", json={"email": email, "return_to": return_to})


def token_in_body(body: str) -> str | None:
    if LINK_MARKER not in body:
        return None
    token = ""
    for ch in body.split(LINK_MARKER, 1)[1]:
        if ch.isalnum() or ch in "-_.~":
            token += ch
        else:
            break
    return token.rstrip(".") or None


def link_token_from_mail(inbox: Inbox, email: str) -> str | None:
    message = poll_until(lambda: inbox.find(to=email, subject_contains=SIGN_IN_SUBJECT))
    if message is None:
        return None
    return token_in_body(message.body)


def latest_link_token(inbox: Inbox, email: str) -> str | None:
    message = inbox.find(to=email, subject_contains=SIGN_IN_SUBJECT)
    return token_in_body(message.body) if message is not None else None


def consume_link(token: str) -> httpx.Response:
    with client() as c:
        return c.post("/auth/link/consume", json={"token": token})


def write_review(author, handle: str, title: str, rating: int = 4,
                 body: str = "Probe review body for moderation.",
                 mentions_minor: bool = False) -> httpx.Response:
    return author.post(f"/products/{handle}/reviews",
                       json={"rating": rating, "title": title, "body": body,
                             "mentions_minor": mentions_minor})


def pending_review(author, handle: str, **fields) -> dict:
    title = fields.pop("title", None) or unique_title()
    review = ok_json(write_review(author, handle, title, **fields),
                     f"POST /api/products/<handle> {handle}/reviews")
    assert review.get("id") is not None, f"the created review carries no id: {review}"
    return review


def public_reviews(anon, handle: str, rating: int | None = None) -> list[dict]:
    params = {"rating": rating} if rating is not None else None
    response = anon.get(f"/products/{handle}/reviews", params=params)
    payload = ok_json(response, f"GET /api/products/<handle> {handle}/reviews")
    assert isinstance(payload, list), (
        f"GET /api/products/<handle> {handle}/reviews must be a top-level JSON array: "
        f"{response.text[:400]}")
    return payload


def product_json(anon, handle: str) -> dict:
    return ok_json(anon.get(f"/products/{handle}"), f"GET /api/products/<handle> {handle}")


def collection_json(anon, handle: str, params: dict | None = None) -> dict:
    return ok_json(anon.get(f"/collections/{handle}", params=params),
                   f"GET /api/collections/<handle> {handle} {params or ''}")


def handles_of(items: list[dict]) -> list[str]:
    return [item.get("handle") for item in items]


def page_html(path: str) -> httpx.Response:
    return httpx.get(f"{app_url()}{path}", timeout=30.0, follow_redirects=False)


def normalise_text(text: str) -> str:
    text = html.unescape(text)
    for fancy, plain in QUOTE_FOLDS:
        text = text.replace(fancy, plain)
    return " ".join(text.split())


def html_text(path: str) -> tuple[int, str]:
    """The server-rendered text of a page: head, scripts and tags removed, entities decoded."""
    response = page_html(path)
    body = HEAD_RE.sub(" ", response.text)
    body = SCRIPT_RE.sub(" ", body)
    body = TAG_RE.sub(" ", body)
    return response.status_code, normalise_text(body)


def redirect_target(path: str) -> tuple[int, str]:
    """Status and decoded same-origin Location of a page request that is not followed."""
    response = page_html(path)
    location = unquote(response.headers.get("location", ""))
    if location.startswith(base_url()):
        location = location[len(base_url()):]
    return response.status_code, location


def internal_hrefs(markup: str) -> list[str]:
    out = []
    for href in HREF_RE.findall(markup):
        href = html.unescape(href).split("#", 1)[0]
        if not href or href.startswith(("mailto:", "tel:", "javascript:", "data:")):
            continue
        if href.startswith(base_url()):
            href = href[len(base_url()):] or "/"
        if href.startswith("/") and not href.startswith("//"):
            out.append(href)
    return out


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as driver:
        launched = driver.chromium.launch()
        yield launched
        launched.close()


def _surface(browser, **options):
    context = browser.new_context(**options)
    context.set_default_timeout(UI_TIMEOUT_MS)
    return context, context.new_page()


@pytest.fixture
def page(browser):
    context, surface = _surface(browser, viewport={"width": 1280, "height": 900})
    yield surface
    context.close()


@pytest.fixture
def narrow_page(browser):
    context, surface = _surface(browser, viewport={"width": 390, "height": 844})
    yield surface
    context.close()


@pytest.fixture
def reduced_page(browser):
    context, surface = _surface(browser, viewport={"width": 1280, "height": 900},
                                reduced_motion="reduce")
    yield surface
    context.close()


@pytest.fixture
def noscript_page(browser):
    context, surface = _surface(browser, viewport={"width": 1280, "height": 900},
                                java_script_enabled=False)
    yield surface
    context.close()


@pytest.fixture
def dark_page(browser):
    context, surface = _surface(browser, viewport={"width": 1280, "height": 900},
                                color_scheme="dark")
    yield surface
    context.close()


def visit(surface, path: str):
    return surface.goto(f"{base_url()}{path}", wait_until="load")


def dial(surface, role: str):
    return surface.locator(f"[data-dial='{role}']").first


def dial_attr(surface, role: str, name: str) -> str | None:
    return dial(surface, role).get_attribute(name)


def dial_state(surface, role: str) -> dict:
    """One consistent read of every hook on a dial root."""
    return dial(surface, role).evaluate(
        "e => ({segment: e.getAttribute('data-segment-minutes'),"
        " start: e.getAttribute('data-start-minute'),"
        " rotation: e.getAttribute('data-bezel-rotation'),"
        " elapsed: e.getAttribute('data-elapsed-minutes'),"
        " colourway: e.getAttribute('data-colourway'),"
        " hour: e.getAttribute('data-hour-rotation'),"
        " lit: e.getAttribute('data-lit-hour')})")


def setter_option(surface, label: str):
    return surface.get_by_role("radio", name=label, exact=True)


def run_control(surface):
    return surface.get_by_role("button", name=re.compile(r"Run a tock")).first


def swatch(surface, name: str):
    return surface.get_by_role("button", name=name, exact=True).first


def comparison_slider(surface):
    return surface.get_by_role("slider", name="Move the time").first


def slider_value(slider) -> int:
    raw = slider.evaluate(
        "e => (e.value !== undefined && e.value !== '') ? e.value : e.getAttribute('aria-valuenow')")
    return int(float(raw))


def slide_to(slider, target: int) -> None:
    slider.focus()
    current = slider_value(slider)
    hours, minutes = divmod(abs(target - current), 60)
    upward = target > current
    for _ in range(hours):
        slider.press("PageUp" if upward else "PageDown")
    for _ in range(minutes):
        slider.press("ArrowRight" if upward else "ArrowLeft")
    assert slider_value(slider) == target, (
        f"moving the slider from {current} to {target} by keyboard left it at "
        f"{slider_value(slider)}")


VISIBLE_NAMED_JS = """([selector, pattern]) => {
  const re = new RegExp(pattern);
  return Array.from(document.querySelectorAll(selector)).filter(e => {
    const name = ((e.getAttribute('aria-label') || '') + ' ' + (e.innerText || '')).trim();
    const style = getComputedStyle(e);
    return re.test(name) && e.getClientRects().length > 0 && style.visibility !== 'hidden'
      && style.display !== 'none';
  }).length;
}"""


def visible_named(surface, selector: str, pattern: str) -> int:
    return surface.evaluate(VISIBLE_NAMED_JS, [selector, pattern])


SMALLEST_CONTAINER_JS = """([needles]) => {
  const all = Array.from(document.querySelectorAll('body *'));
  const holders = all.filter(e => needles.every(n => (e.textContent || '').toLowerCase().includes(n.toLowerCase())));
  if (!holders.length) return null;
  holders.sort((a, b) => (a.textContent || '').length - (b.textContent || '').length);
  return holders[0];
}"""


def smallest_container(surface, needles: list[str]):
    """The element with the least text that still contains every needle."""
    handle = surface.evaluate_handle(SMALLEST_CONTAINER_JS, [needles])
    return handle.as_element()


def ui_sign_in(surface, email: str, password: str = SEEDED_PASSWORD,
               return_to: str | None = None) -> None:
    target = "/account/login" + (f"?return_to={return_to}" if return_to else "")
    visit(surface, target)
    form = surface.locator("form").filter(has=surface.get_by_label("Password", exact=True)).first
    form.get_by_label("Email", exact=True).fill(email)
    form.get_by_label("Password", exact=True).fill(password)
    with surface.expect_navigation():
        form.get_by_role("button", name="Sign in", exact=True).click()


def ui_add_to_cart(surface, handle: str) -> None:
    visit(surface, f"/products/{handle}")
    surface.get_by_role("button", name="Add to Cart", exact=True).first.click()
    expect(surface.get_by_role("button", name="Added to Cart").first).to_be_visible(
        timeout=UI_TIMEOUT_MS)


def main_text(surface) -> str:
    return normalise_text(surface.evaluate("() => document.body.innerText"))


CONTENTION_WRITERS = 8
CONTENTION_ROUNDS = 15
UNIT_COUNT_KEYS = {"available", "on_hand", "reserved", "stock", "inventory", "units", "units_available",
                   "quantity_available", "inventory_quantity", "units_left"}
NAV_LINKS = ["TOCK 33", "TOCK 38", "Bundles", "Straps", "About"]
FAQ_QUESTIONS = [("service", "When will I need to service my Tock timepiece?"),
                 ("waterproof", "How waterproof is a Tock watch?"),
                 ("battery", "How long does my battery last?"),
                 ("cleaning", "What is the best way to clean my watch + band?"),
                 ("warranty", "How long is my Tock watch warranty?"),
                 ("materials", "Are the materials safe?")]
GUIDE_HEADINGS = ["How do I set the time on my Tock?", "How do I change the band on my Tock?",
                  "How do I use the timing bezel on my Tock watch?"]
HOME_SECTION_MARKERS = ["Nobody is born knowing", "TOCK 33. 33mm, a first watch for a small wrist.",
                        "TOCK 38 GMT: For older wrists featuring two time zones",
                        "Most of a clock's day is spent between the numbers.",
                        "The co-founders first test with the prototype",
                        "Thirty minutes out. Fifteen gone. Half the tock still to run.",
                        "TIME CONFIDENCE - knowing how much longer.",
                        "Kids' watches usually fail at the bit you look through.",
                        "ONE FOR YOU, ONE FOR MINI-YOU"]

ELAPSED_WATCH_JS = """() => {
  window.__probePeakElapsed = 0;
  const root = document.querySelector("[data-dial='hero']");
  const read = () => {
    const value = parseFloat(root.getAttribute('data-elapsed-minutes') || '0');
    if (!Number.isNaN(value) && value > window.__probePeakElapsed) window.__probePeakElapsed = value;
  };
  new MutationObserver(read).observe(root, {attributes: true, attributeFilter: ['data-elapsed-minutes']});
  read();
}"""

SOUND_WATCH_JS = """window.__probeSounds = 0;
(() => {
  const bump = () => { window.__probeSounds += 1; };
  const play = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function () { bump(); return play.apply(this, arguments); };
  if (window.AudioScheduledSourceNode) {
    const start = AudioScheduledSourceNode.prototype.start;
    AudioScheduledSourceNode.prototype.start = function () { bump(); return start.apply(this, arguments); };
  }
  if (window.speechSynthesis) {
    const speak = window.speechSynthesis.speak.bind(window.speechSynthesis);
    window.speechSynthesis.speak = function (utterance) { bump(); return speak(utterance); };
  }
})();"""

NOTIFICATION_WATCH_JS = """window.__probeNotificationAsks = 0;
(() => {
  if (window.Notification && Notification.requestPermission) {
    const ask = Notification.requestPermission.bind(Notification);
    Notification.requestPermission = function () {
      window.__probeNotificationAsks += 1;
      return ask.apply(null, arguments);
    };
  }
})();"""

DISCLAIMER_PLACEMENT_JS = """() => {
  const needle = 'Quotes are reproduced from verified reviews';
  const holders = Array.from(document.querySelectorAll('body *')).filter(e => (e.textContent || '').includes(needle));
  if (!holders.length) return 'missing';
  holders.sort((a, b) => a.textContent.length - b.textContent.length);
  const own = holders[0];
  if (own.closest('footer')) return 'footer';
  let node = own;
  while (node && node !== document.body) {
    const text = (node.textContent || '').toLowerCase();
    if (text.includes('knowing how much longer')) {
      const foreign = ['usually fail at the bit you look through', 'fifteen gone. half the tock'];
      return foreign.some(f => text.includes(f)) ? 'outside' : 'inside';
    }
    node = node.parentElement;
  }
  return 'outside';
}"""

GRID_COLUMNS_JS = """([titles, columns]) => {
  const lefts = new Set();
  for (const e of document.querySelectorAll('body *')) {
    const text = (e.innerText || '').trim();
    if (!titles.includes(text)) continue;
    if (Array.from(e.children).some(c => (c.innerText || '').trim() === text)) continue;
    const r = e.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    lefts.add(Math.round(r.left / 8));
  }
  return lefts.size === columns;
}"""

DOT_LINKS_JS = """() => {
  const out = [];
  for (const a of document.querySelectorAll('a[href*="/products/tock-33-"]')) {
    const img = a.querySelector('img');
    const name = (a.getAttribute('aria-label') || a.getAttribute('title') || a.innerText || (img && img.alt) || '').trim();
    if (!name || /TOCK 33/i.test(name) || !/(aqua|navy|fuchsia|glow)/i.test(name)) continue;
    if (a.getClientRects().length === 0) continue;
    const path = new URL(a.href, location.href).pathname;
    a.setAttribute('data-probe-dot', path.split('/').pop());
    out.push(path);
  }
  return out;
}"""

LABEL_WATCH_JS = """() => {
  window.__probeLabels = [];
  const record = () => {
    for (const b of document.querySelectorAll('button, [role=button], input[type=submit]')) {
      const label = String(b.innerText || b.value || '').trim();
      for (const wanted of ['Adding to Cart', 'Added to Cart']) {
        const last = window.__probeLabels[window.__probeLabels.length - 1];
        if (label.includes(wanted) && last !== wanted) window.__probeLabels.push(wanted);
      }
    }
  };
  new MutationObserver(record).observe(document.body, {subtree: true, childList: true, characterData: true, attributes: true});
}"""

SIZE_STATE_JS = """(label) => {
  const candidates = Array.from(document.querySelectorAll('input, button, option, [role=radio], [role=option], label'))
    .filter(e => ((e.getAttribute('aria-label') || '') + ' ' + (e.innerText || e.textContent || e.value || '')).includes(label));
  if (!candidates.length) return 'removed';
  const unavailable = candidates.some(e => {
    const control = e.tagName === 'LABEL' ? (e.control || e.querySelector('input')) : e;
    const text = ((e.getAttribute('aria-label') || '') + ' ' + (e.innerText || e.textContent || '')).toLowerCase();
    return (control && (control.disabled || control.getAttribute('aria-disabled') === 'true'))
      || /unavailable|sold out|out of stock/.test(text);
  });
  return unavailable ? 'unavailable' : 'available';
}"""

STRUCK_PRICE_JS = """(price) => Array.from(document.querySelectorAll('body *')).some(e => {
  if (!(e.innerText || '').includes(price)) return false;
  for (let node = e; node && node !== document.body; node = node.parentElement) {
    if (['S', 'DEL', 'STRIKE'].includes(node.tagName)
        || getComputedStyle(node).textDecorationLine.includes('line-through')) return true;
  }
  return false;
})"""

ANIMATION_WATCH_JS = """window.__probeAnimations = [];
(() => {
  const seen = new Set();
  const sample = () => {
    if (!document.getAnimations) return;
    for (const a of document.getAnimations()) {
      const timing = a.effect && a.effect.getComputedTiming ? a.effect.getComputedTiming() : {};
      const duration = Number(timing.duration) || 0;
      if (a.playState === 'running' && (duration > 250 || timing.iterations === Infinity)) {
        const target = a.effect && a.effect.target;
        const label = (a.animationName || a.transitionProperty || 'animation') + ' on ' + (target ? target.tagName : '?');
        if (!seen.has(label)) { seen.add(label); window.__probeAnimations.push(label); }
      }
    }
  };
  const loop = (start) => (now) => { sample(); if (now - start < 1500) requestAnimationFrame(loop(start)); };
  document.addEventListener('DOMContentLoaded', () => requestAnimationFrame(loop(performance.now())));
})();"""

CONTRAST_JS = """() => {
  const parse = (c) => {
    const m = c.match(/^rgba?[(]([^)]+)[)]$/);
    if (!m) return null;
    const p = m[1].split(',').map(Number);
    return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1};
  };
  const channel = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lum = (c) => 0.2126 * channel(c.r) + 0.7152 * channel(c.g) + 0.0722 * channel(c.b);
  const ground = (e) => {
    for (let n = e; n; n = n.parentElement) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && c.a > 0.5) return c;
    }
    return {r: 255, g: 255, b: 255, a: 1};
  };
  const out = [];
  const nodes = Array.from(document.querySelectorAll('p'))
    .filter(p => (p.innerText || '').trim().length > 20 && p.getClientRects().length > 0).slice(0, 40);
  for (const p of nodes) {
    const fg = parse(getComputedStyle(p).color);
    if (!fg) continue;
    const a = lum(fg), b = lum(ground(p));
    const ratio = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
    if (ratio < 4.5) out.push([(p.innerText || '').slice(0, 40), Number(ratio.toFixed(2))]);
  }
  return out;
}"""


def sitemap_locations() -> list[str]:
    response = page_html("/sitemap.xml")
    assert response.status_code == 200, f"GET /sitemap.xml returned {response.status_code}"
    return [html.unescape(loc.strip()) for loc in re.findall(r"<loc>(.*?)</loc>", response.text, re.S)]


HOME_H2_HEADINGS = ["TOCK 33. 33mm, a first watch for a small wrist.",
                    "TOCK 38 GMT: For older wrists featuring two time zones",
                    "Most of a clock's day is spent between the numbers.",
                    "TIME CONFIDENCE - knowing how much longer.",
                    "Kids' watches usually fail at the bit you look through.",
                    "ONE FOR YOU, ONE FOR MINI-YOU"]
SEED_SKUS = {
    "TK33-AQUA": (18900, 12), "TK33-NAVY": (18900, 0), "TK33-FUCHSIA": (18900, 0), "TK33-GLOW": (22900, 6),
    "TK38-GREY": (37900, 5), "TK38-BLACK": (37900, 5), "TK38-GLOW": (42900, 3), "TK38-SHARK": (39900, 4),
    "TK31-MINT": (5900, 0), "BNDL-BLACK-NAVY": (49900, None), "BNDL-GREY-AQUA": (46900, None),
    "BNDL-GLOW-GLOW": (54900, None), "BNDL-SHARK-FUCHSIA": (51900, None),
    "STRAP-WOVEN-SAND-S": (2400, 20), "STRAP-WOVEN-SAND-L": (2400, 0),
    "STRAP-RUBBER-NAVY-S": (2900, 15), "STRAP-RUBBER-NAVY-L": (2900, 15),
    "STRAP-RUBBER-FUCHSIA-S": (2900, 10), "STRAP-RUBBER-FUCHSIA-L": (2900, 1),
    "STRAP-NATO-AQUA": (2200, 30), "STRAP-NATO-NAVY": (2200, 0), "TOTE-BONE": (2000, 5000),
    "BEANIE-NAVY": (2200, 5000), "TK33-LILAC": (18900, 8),
}
SEED_BUNDLES = {"BNDL-BLACK-NAVY": ("TK38-BLACK", "TK33-NAVY", "unavailable"),
                "BNDL-SHARK-FUCHSIA": ("TK38-SHARK", "TK33-FUCHSIA", "unavailable"),
                "BNDL-GLOW-GLOW": ("TK38-GLOW", "TK33-GLOW", "low_stock"),
                "BNDL-GREY-AQUA": ("TK38-GREY", "TK33-AQUA", "in_stock")}
SEED_REVIEWS = [
    ("tock-33-aqua", "Priya", 5, "Fewer questions in the car", True),
    ("tock-33-aqua", "Tom", 5, "Survived the playground", True),
    ("tock-33-aqua", "Lena", 5, "She reads the hour now", True),
    ("tock-33-aqua", "Marco", 5, "A proper first watch", True),
    ("tock-33-aqua", "Ada", 4, "Bezel is stiff at first", True),
    ("tock-33-aqua", "Sam", 4, "Lovely, not cheap", False),
    ("tock-33-aqua", "Dana", 1, "Strap tore at the buckle holes", True),
    ("tock-33-glow", "Iris", 5, "Glows all night", True),
    ("tock-33-glow", "Ben", 5, "Our second Tock", True),
    ("tock-33-glow", "Kofi", 4, "Pale in daylight", True),
    ("tock-38-grey", "Hana", 5, "Matching watches", True),
    ("tock-38-grey", "Luis", 4, "Handy second time zone", False),
    ("tock-38-black", "Ravi", 3, "Good but heavy", False),
    ("tock-33-glow", "Nora", 5, "My daughter wrote this one", False),
]
HOME_COPY = {
    "setter": ["Try it. Set a tock and watch closely",
               "No gimmicks, no alarms, just a simple visual timer to help with the passage of time",
               "Run a tock", "fast demo"],
    "hero": ["Exceptional wristwatches for kids to learn time",
             "Rotate the bezel and align the start of a tock with the minute hand to learn the fundamentals of time management",
             "2mm sapphire crystal", "100m water resistance", "Japanese LumiNova", "Swiss ETA quartz movement"],
    "ranges": ["TOCK 33. 33mm, a first watch for a small wrist.",
               "Four colourways, one size. The run-thru strap fits any wrist.",
               "TOCK 38 GMT: For older wrists featuring two time zones",
               "Swiss nylon polymer over a steel core. Swiss Made Ronda GMT movement. 2mm sapphire crystal. Rotating timer bezel with lume. Screw-down crown and case back, 100m water resistance."],
    "comparison": ["The dial innovation",
                   "Normal dials have the hour hand between two numerals for most of the hour. An adult reads through that without noticing. A child asked what it says will often tell you \"somewhere between two and three.\" We call that gap no man's land - we solved that design flaw.",
                   "Conventional Dial",
                   "The hour hand spends almost all of its time between two numerals, not clearly indicating which hour it currently is.",
                   "Tock Dial",
                   "We moved every hour off a point and into a tock. The hand sits inside the hour's own zone rather than between two numerals."],
    "founder": ["The co-founders first test with the prototype", "\"We're like...halfway there.\"",
                "Thirty minutes from their grandparents' house, my kids set a thirty minute tock on an early prototype. Fifteen minutes in, the youngest said that ^ out loud to nobody in particular. No \"are we there yet\" just confidence - the moment we knew that tocks were a thing - Mara.",
                "You say a number, your child turns the ring to the start of that tock, and from then on the watch is the one being asked how much longer. It is a simple concept, but infinitely empowering."],
    "walkthrough": ["Thirty minutes out. Fifteen gone. Half the tock still to run.",
                    "The bezel is turned to the start of the 30 minute tock",
                    "15 minutes have passed, the hand is half way through the tock",
                    "The 30 minute tock has elapsed, time to...build a dinosaur fort?",
                    "The bezel is marked in 5, 10, 15 and 30 minute \"tocks\". Each number is the length of time for the minute hand to pass."],
    "testimonials": ["What owners tell us", "TIME CONFIDENCE - knowing how much longer.",
                     "We built Tock for the car, the countdown and the bedtime negotiation. Owners keep putting it to new uses - we've been shocked but the number of ADHD messages we get...",
                     "The car ride question stopped. She just looks at her wrist now.", "Verified owner",
                     "Fifteen minutes finally means something to my son.", "Public forum post",
                     "Bedtime negotiations went from ten rounds to one.", "Verified review",
                     "Our ADHD kiddo uses the bezel to pace homework breaks.",
                     "My teacher asked how I knew there were five minutes left.", "Owner, age 8",
                     "It helps our autistic son see transitions coming."],
    "construction": ["How it's built", "Kids' watches usually fail at the bit you look through.",
                     "Read the reviews under any children's watch and the same complaint comes back: the crystal scratches until the dial can't be read. So that is the part we spent the money on.",
                     "Mohs 9 on the hardness scale. Chosen because a scratched crystal is the most common complaint in this category.",
                     "Rated to 100m. Showers, baths and swimming are fine. Care guidance ships with the watch.",
                     "The crown threads shut rather than pushing in, so it stays secured when it is closed.",
                     "The same movement family used across Swiss quartz watches. Battery, not charging."],
    "footer_groups": ["Main menu", "Home", "Shop All", "Contact", "More Links", "Search", "Terms of Use", "Privacy",
                      "Shipping and Returns", "User Guide", "Watch FAQs"],
    "footer_cards": ["Watch FAQs", "Your questions, answered.", "Need Help?", "Email us at care@example.com"],
}
PRODUCT_COPY = ["Materials & Care", "Size & Fit", "Shipping & Returns", "Customer Reviews",
                "Our straps have infinite size adjustability with a reliable steel buckle designed to fit a wide range of ages and sizes."]
CART_COPY = ["Your Cart", "Price", "Quantity", "Total", "Subtotal", "Shipping & taxes calculated at checkout", "Check Out",
             "Parent approved", "Founded and designed by real parents for real kids.", "Easy 30-Day Returns",
             "Not the right fit? No problem. See our return information below.", "Secure Checkout",
             "Your payment information is encrypted and secure."]
CHECKOUT_FIELDS = ["Full name", "Address line 1", "Address line 2", "City", "State", "ZIP code", "Country"]
FAQ_BATTERY_ANSWER = ("Up to 10 years..... Why isn't this exact? Batteries are weird. Temperature changes, the amount of "
                      "aggressive jiggling and indeed, interplanetary travel can affect this as well.")
GUIDE_CLOSING_STEP = ("The most important part! Screw the crown clockwise back into the case until it's a snug tight "
                      "fit, this means it's fully sealed and back up to dive grade water resistance.")

KEYFRAME_WATCH_JS = """window.__probeKeyframes = [];
document.addEventListener('animationstart', (e) => { window.__probeKeyframes.push(e.animationName); }, true);"""

ANIMATION_SAMPLE_JS = """() => {
  window.__probeAnimations = [];
  const seen = new Set();
  const start = performance.now();
  const tick = (now) => {
    for (const a of document.getAnimations()) {
      const t = a.effect && a.effect.getComputedTiming ? a.effect.getComputedTiming() : {};
      if (a.playState === 'running' && Number(t.duration) > 250) {
        const target = a.effect && a.effect.target;
        const label = (a.animationName || a.transitionProperty || 'animation') + ' on ' + (target ? target.tagName : '?');
        if (!seen.has(label)) { seen.add(label); window.__probeAnimations.push(label); }
      }
    }
    if (now - start < 1200) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}"""

PROGRESS_WATCH_JS = """() => {
  window.__probeProgress = null;
  const add = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'Add to Cart');
  window.__probePrimary = add ? getComputedStyle(add).backgroundColor : null;
  const sample = () => {
    const colours = [];
    for (const a of document.getAnimations()) {
      const t = a.effect && a.effect.getComputedTiming ? a.effect.getComputedTiming() : {};
      const target = a.effect && a.effect.target;
      if (a.playState !== 'running' || t.iterations !== Infinity || !(target instanceof Element)) continue;
      for (const n of [target, ...target.querySelectorAll('*')]) {
        const cs = getComputedStyle(n);
        colours.push(cs.color, cs.backgroundColor, cs.borderTopColor, cs.borderLeftColor, cs.fill, cs.stroke);
      }
    }
    const busyButton = Array.from(document.querySelectorAll('button, [role=button]')).find(b => (b.innerText || '').includes('Adding to Cart'));
    const busy = busyButton ? getComputedStyle(busyButton).backgroundColor : null;
    window.__probeProgress = {pending: false, moving: colours.length > 0, colours, busy};
  };
  new MutationObserver(() => {
    if (window.__probeProgress) return;
    const busy = Array.from(document.querySelectorAll('button, [role=button]')).some(b => (b.innerText || '').includes('Adding to Cart'));
    if (busy) {
      window.__probeProgress = {pending: true};
      requestAnimationFrame(() => requestAnimationFrame(sample));
    }
  }).observe(document.body, {subtree: true, childList: true, characterData: true, attributes: true});
}"""

GRID_COLUMN_COUNT_JS = """([titles]) => {
  const lefts = new Set();
  for (const e of document.querySelectorAll('body *')) {
    const text = (e.innerText || '').trim();
    if (!titles.includes(text)) continue;
    if (Array.from(e.children).some(c => (c.innerText || '').trim() === text)) continue;
    const r = e.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    lefts.add(Math.round(r.left / 8));
  }
  return lefts.size;
}"""

RAIL_REGION_JS = """([titles]) => {
  const holders = Array.from(document.querySelectorAll('body *')).filter(e => titles.every(t => (e.textContent || '').includes(t)));
  if (!holders.length) return 'missing';
  holders.sort((a, b) => a.textContent.length - b.textContent.length);
  for (let n = holders[0], depth = 0; n && depth < 5; n = n.parentElement, depth++) {
    const cs = getComputedStyle(n);
    if (['auto', 'scroll'].includes(cs.overflowX) && n.hasAttribute('tabindex') && n.tabIndex >= 0) return 'ok';
  }
  return 'no keyboard-focusable scroll region';
}"""

STICKY_BAR_JS = """() => new Promise(resolve => {
  window.scrollTo(0, document.documentElement.scrollHeight);
  requestAnimationFrame(() => requestAnimationFrame(() => {
    const vh = window.innerHeight;
    const bars = Array.from(document.querySelectorAll('body *')).filter(e => {
      const cs = getComputedStyle(e);
      if (!['fixed', 'sticky'].includes(cs.position)) return false;
      const r = e.getBoundingClientRect();
      return r.height > 0 && r.bottom >= vh - 2 && r.top > vh / 2;
    });
    if (!bars.length) return resolve('clear');
    const barTop = Math.min(...bars.map(b => b.getBoundingClientRect().top));
    const leaves = Array.from(document.querySelectorAll('body *')).filter(e => !bars.some(b => b.contains(e))
      && e.children.length === 0 && (e.innerText || '').trim() && e.getClientRects().length > 0
      && getComputedStyle(e).visibility !== 'hidden');
    const lowest = Math.max(...leaves.map(e => e.getBoundingClientRect().bottom));
    resolve(lowest <= barTop + 1 ? 'clear' : 'covered: content ends at ' + lowest + ' under a bar starting at ' + barTop);
  }));
})"""

SETTER_ROWS_JS = """() => new Set(Array.from(document.querySelectorAll('[role=radio], input[type=radio]'))
  .map(e => (e.closest('label') || e).getBoundingClientRect())
  .filter(r => r.height > 0).map(r => Math.round(r.top / 10))).size"""

WORDMARK_OFFSET_JS = """() => {
  const links = Array.from(document.querySelectorAll('a')).filter(a => {
    const href = a.getAttribute('href') || '';
    const r = a.getBoundingClientRect();
    return (href === '/' || href === location.origin + '/') && r.top < 120 && r.width > 0;
  });
  if (!links.length) return null;
  const r = links[0].getBoundingClientRect();
  return Math.abs((r.left + r.right) / 2 - window.innerWidth / 2);
}"""


def utc_now():
    """The single sanctioned clock read, taken inside a helper at call time."""
    return datetime.now(timezone.utc)


def cart_control(surface):
    return surface.get_by_role("button", name=re.compile(r"^(?!Add).*\bCart\b")).first


def all_titles(anon) -> list[str]:
    return [p["title"] for p in collection_json(anon, "all").get("products", [])]


def lowered_text(path: str) -> str:
    return html_text(path)[1].lower()


TABLET_VIEWPORT = {"width": 900, "height": 1000}
MARKETING_SUBJECT_RE = re.compile(r"newsletter|% off|discount|\bdeal|\bpromo|\bsale\b|special offer", re.I)

STYLE_SNAPSHOT_JS = """(root) => {
  const out = [];
  for (const n of [root, ...root.querySelectorAll('*')]) {
    for (const pseudo of [null, '::before', '::after']) {
      const cs = getComputedStyle(n, pseudo);
      out.push([cs.backgroundColor, cs.color, cs.borderTopColor, cs.boxShadow, cs.transform, cs.opacity, cs.outlineColor].join('|'));
    }
  }
  return out;
}"""

TAB_STOPS_JS = """() => { const e = document.activeElement; if (!e || e === document.body) return null;
  const r = e.getBoundingClientRect(); return {x: r.left + r.width / 2, top: r.top, text: (e.innerText || e.getAttribute('aria-label') || '').trim()}; }"""

TARGET_SIZES_JS = """(names) => names.map(name => {
  const candidates = Array.from(document.querySelectorAll('button, [role=radio], input[type=radio], label'))
    .filter(e => ((e.getAttribute('aria-label') || '') + ' ' + (e.innerText || '')).trim() === name || (e.innerText || '').trim() === name);
  const boxes = candidates.map(e => (e.closest('label') || e).getBoundingClientRect()).filter(r => r.width > 0);
  if (!boxes.length) return [name, 0, 0];
  const r = boxes.sort((a, b) => b.width * b.height - a.width * a.height)[0];
  return [name, r.width, r.height];
})"""

RAIL_CARDS_JS = """([titles]) => {
  const holders = Array.from(document.querySelectorAll('body *')).filter(e => titles.every(t => (e.textContent || '').includes(t)));
  if (!holders.length) return null;
  holders.sort((a, b) => a.textContent.length - b.textContent.length);
  const list = holders[0];
  const cards = Array.from(list.children).filter(c => titles.some(t => (c.textContent || '').includes(t)));
  if (cards.length < 2) return null;
  const pitch = cards[1].getBoundingClientRect().left - cards[0].getBoundingClientRect().left;
  let scroller = list;
  for (let n = list; n && n !== document.body; n = n.parentElement) {
    if (['auto', 'scroll', 'hidden'].includes(getComputedStyle(n).overflowX)) { scroller = n; break; }
  }
  return pitch > 0 ? scroller.clientWidth / pitch : null;
}"""


def product_image_markup(path: str) -> list[str]:
    """Image sources and inline drawings on a page, leaving out live dials whose hands show the time."""
    markup = page_html(path).text
    sources = re.findall(r"<img\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']", markup, re.I)
    drawings = [svg for svg in re.findall(r"<svg\b.*?</svg>", markup, re.S | re.I) if "data-dial" not in svg]
    return sources + drawings


def wide_surface(browser, viewport: dict):
    return _surface(browser, viewport=viewport)


TOCK33_SPECS = {"Case": "33mm Swiss nylon polymer",
                "Bezel": "Bidirectional rotating bezel with timer function and lume",
                "Movement": "Swiss Made 3-jewel quartz with anti-shock", "Bezel Marquetry": "Contrast lume fill",
                "Dial": "Embossed brass with pad-printed indexes and appliques", "Hands": "Brass dauphine hands with lume",
                "Lens": "Scratch-resistant sapphire crystal", "Crown": "Screw-down 316L stainless steel",
                "Band": "17mm recycled woven polyester", "Buckle": "316L stainless steel", "Water Resistance": "10 ATM",
                "Theoretical Battery life": "10 years", "Accuracy": "Plus or minus 10 seconds per month",
                "Warranty": "2 years"}
TOCK38_CHANGES = {"Case": "38mm Swiss nylon polymer over a steel core", "Movement": "Swiss Made Ronda GMT quartz",
                  "Dial": "Brass with a second time zone hand"}
TOCK31_CHANGES = {"Case": "31mm Swiss nylon polymer"}
DANA_BODY = ("The strap tore at the buckle holes within two months, the dial is hard to read in low light, the lume "
             "only covers the bezel, and we paid import charges nobody warned us about.")
DANA_REPLY = ("Sorry, Dana. A replacement strap is on its way under the warranty, and our shipping page now explains "
              "import charges.")


DISCLAIMER = ("Quotes are reproduced from verified reviews and public forum posts, attributed to their source. They "
              "are individual experiences, not results we have tested for.")
COLLECTION_TITLES = {"tock-33": "TOCK 33", "tock-38": "TOCK 38", "tock-31": "TOCK 31", "bundles": "Bundles",
                     "straps": "Straps", "all": "Shop All"}
LINE_FIELDS = {"id", "sku", "title", "quantity", "unit_price", "line_total", "is_gift", "promotion"}
ORDER_FIELDS = {"number", "status", "hold_reason", "subtotal", "shipping", "total", "currency", "lines"}
ORDER_LINE_FIELDS = {"sku", "title", "quantity", "unit_price", "is_gift", "parent_sku"}
PRODUCT_ELEMENT_FIELDS = {"handle", "title", "family", "colourway", "case_size", "price", "compare_at_price", "currency",
                          "availability", "rating_average", "review_count", "siblings"}
TABLE_COLUMNS = {
    "accounts": ["id", "email", "name", "password_hash", "role", "created_at"],
    "sign_in_links": ["id", "email", "token_hash", "return_to", "used_at", "expires_at", "created_at"],
    "products": ["id", "handle", "title", "kind", "family", "colourway", "case_size", "status", "description", "position",
                 "published_at"],
    "product_handle_aliases": ["alias", "product_id", "reason"],
    "variants": ["id", "product_id", "sku", "option", "price", "compare_at_price", "grams"],
    "product_specifications": ["product_id", "position", "key", "value"],
    "inventory_items": ["id", "variant_id", "on_hand", "reserved"],
    "bundle_components": ["bundle_variant_id", "component_variant_id", "quantity"],
    "stock_ledger": ["id", "inventory_item_id", "delta", "reason", "note", "created_at"],
    "carts": ["id", "token", "account_id", "status", "last_activity_at", "created_at"],
    "cart_lines": ["id", "cart_id", "variant_id", "quantity", "unit_price", "is_gift", "promotion"],
    "reservations": ["id", "cart_id", "cart_line_id", "inventory_item_id", "quantity", "status", "expires_at", "created_at"],
    "orders": ["id", "number", "account_id", "status", "hold_reason", "subtotal", "shipping", "total", "currency",
               "shipping_name", "shipping_line1", "shipping_line2", "shipping_city", "shipping_region", "shipping_postcode",
               "shipping_country", "idempotency_key", "billing_external_key", "placed_at"],
    "order_lines": ["id", "order_id", "variant_id", "parent_line_id", "quantity", "unit_price", "is_gift", "title_snapshot",
                    "sku_snapshot"],
    "reviews": ["id", "product_id", "account_id", "author_name", "rating", "title", "body", "status", "verified_purchase",
                "mentions_minor", "minor_basis", "rejection_clause", "created_at", "published_at"],
    "review_replies": ["id", "review_id", "body", "created_at"],
    "restock_subscriptions": ["id", "product_id", "email", "status", "created_at", "notified_at"],
    "support_requests": ["id", "reference", "name", "email", "subject", "queue", "message", "created_at"],
}
DERIVED_COLUMNS = {"products": ["availability", "rating_average", "review_count", "rating_histogram", "saving"],
                   "variants": ["availability", "saving"],
                   "carts": ["subtotal", "item_count", "hold_seconds_remaining"]}
