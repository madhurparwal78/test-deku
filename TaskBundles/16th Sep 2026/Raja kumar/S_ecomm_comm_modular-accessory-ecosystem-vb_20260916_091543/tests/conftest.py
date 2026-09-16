"""Task fixtures for deku/modular-accessory-ecosystem-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout
or module names. The only assumptions are the App Contract and the literals
instruction.md pins explicitly.

Provider agnostic: Kill Bill and Mailpit are read over their own HTTP APIs and
PostgreSQL through capabilities.py, never through a provider SDK.
"""

from __future__ import annotations

import os
import re
import time

import httpx
import pytest
from appclient import api_base, app_url
from capabilities import Backend, make_backend

TIMEOUT = 30.0

SHOPPER_PHONE = "9876500001"
SHOPPER_EMAIL = "shopper@example.com"
SHOPPER_NAME = "Asha Rao"
SECOND_PHONE = "9876500002"
SECOND_EMAIL = "shopper2@example.com"
SECOND_NAME = "Bikram Sen"

CODE_SUBJECT = "Your LatticeGoods sign in code"
ORDER_SUBJECT = "Order confirmed:"
TWO_ATTEMPTS_LEFT = "That code did not match. Two attempts left."
COMPATIBILITY_WARNING = "This attaches to a Latch case. You may already have one."
NEWSLETTER_MESSAGE = "You are on the list. Watch your inbox."
STANDARD_WINDOW = "Delivers in 3 to 5 days"
EXPRESS_WINDOW = "Delivers in 1 to 2 days"
NOT_SERVED = "We do not deliver to this pincode yet"

SERVED_PINCODE = "400050"
STANDARD_ONLY_PINCODE = "411014"
UNSERVED_PINCODE = "999999"
EXPRESS_PRICE = 19900
PAGE_SIZE = 24

MODEL = "arbone-16-pro"
RETIRED_MODEL = "arbone-15"
CASES = "phone-cases"
HEADING_WITH_MODEL = "ARBOR ARBONE 16 PRO PHONE CASES"
HEADING_WITHOUT_MODEL = "PHONE CASES"
MODEL_LISTING_TOTAL = 60
CASES_TOTAL = 399
PUBLISHED_TOTAL = 404
CATEGORIES = ("phone-cases", "phone-grips", "phone-stands", "phone-wallets",
              "phone-lanyards", "colour-plates")
UNPUBLISHED_BASICS = ("basics-clear-case-13-arbone-16-pro",
                      "basics-clear-case-26-arbone-16-pro",
                      "basics-clear-case-39-arbone-16-pro",
                      "basics-clear-case-52-arbone-16-pro")

LATCH_CASE = "latch-phone-case-arbone-16-pro"
LATCH_CLEAR = "latch-clear-phone-case-arbone-16-pro"
LATCH_SIGNATURE = "latch-signature-phone-case-arbone-16-pro"
CLARITY_CASE = "clarity-maglock-case-arbone-16-pro"
BASICS_CASE = "basics-clear-case-01-arbone-16-pro"
MAGNETIC_CASES = [LATCH_CASE, LATCH_CLEAR, LATCH_SIGNATURE, CLARITY_CASE]
NEWEST_FIRST_FOUR = [LATCH_CASE, LATCH_CLEAR, LATCH_SIGNATURE, CLARITY_CASE]
PRICE_LOW_HIGH = [CLARITY_CASE, LATCH_CLEAR, LATCH_CASE, LATCH_SIGNATURE]
PRICE_HIGH_LOW = [LATCH_SIGNATURE, LATCH_CLEAR, LATCH_CASE, CLARITY_CASE]
DISCOUNT_ORDER = [CLARITY_CASE, LATCH_CLEAR, LATCH_CASE, LATCH_SIGNATURE]
UMBER_TOTAL = 8
UMBER_OR_CINNABAR_TOTAL = 13
UNDER_1000_TOTAL = 19

GRIP = "latch-phone-grip-stand"
FLEX = "latch-flex-stand"
WALLET = "latch-phone-wallet-stand"
LANYARD = "latch-phone-lanyard"
PLATE = "latch-colour-plate"
RING_MOUNT = "latch-ring-mount"
RING_MOUNT_SKU = "latch-ring-mount-basalt"
LATCH_CASE_PANEL = [GRIP, FLEX, WALLET, LANYARD]
LATCH_CASE_PANEL_TITLES = ["Marigold Latch Phone Grip & Stand", "Sage Latch Flex Stand",
                           "Cypress Latch Phone Wallet Stand", "Amber Latch Phone Lanyard"]
FLEX_PANEL = [CLARITY_CASE, LATCH_CLEAR, "latch-phone-case-arbone-15", LATCH_CASE]

UMBER_SKU = "latch-clear-phone-case-arbone-16-pro-umber"
CINNABAR_SKU = "latch-clear-phone-case-arbone-16-pro-cinnabar"
OCHRE_SKU = "latch-signature-phone-case-arbone-16-pro-ochre"
CERISE_SKU = "latch-signature-phone-case-arbone-16-pro-cerise"
BASALT_CASE_SKU = "latch-phone-case-arbone-16-pro-basalt"
FLEX_SAGE_SKU = "latch-flex-stand-sage"
GRIP_MARIGOLD_SKU = "latch-phone-grip-stand-marigold"
PLATE_VIOLET_SKU = "latch-colour-plate-violet"
WALLET_CYPRESS_SKU = "latch-phone-wallet-stand-cypress"
LANYARD_AMBER_SKU = "latch-phone-lanyard-amber"
LANYARD_SAGE_SKU = "latch-phone-lanyard-sage"
PLATE_CYPRESS_SKU = "latch-colour-plate-cypress"
PLATE_FERN_SKU = "latch-colour-plate-fern"
WALLET_UMBER_SKU = "latch-phone-wallet-stand-umber"
WALLET_UMBER_TITLE = "Umber Latch Phone Wallet Stand"
ATOMIC_KEEP = "basics-clear-case-16-arbone-17"
ATOMIC_KEEP_SKU = "basics-clear-case-16-arbone-17-sage"
ATOMIC_LAST = "basics-clear-case-56-arbone-17"
ATOMIC_LAST_SKU = "basics-clear-case-56-arbone-17-cerise"
UMBER_LIVE, UMBER_LIST = 179900, 229900
CINNABAR_LIVE, CINNABAR_LIST = 159900, 229900
FLEX_LIVE, FLEX_LIST = 99900, 129900
PLATE_LIVE = 79900
WALLET_LIVE, WALLET_LIST = 299900, 349900
LANYARD_LIVE = 249900

CLIENT_ERRORS = (400, 401, 403, 404, 409, 410, 422, 423, 429)
DENIALS = (401, 403, 404)


def unique(prefix: str) -> str:
    return f"{prefix}-{os.urandom(5).hex()}"


def unique_email() -> str:
    return f"{unique('probe')}@example.com"


def unique_phone() -> str:
    return "7" + str(int.from_bytes(os.urandom(5), "big") % 10**9).zfill(9)


def settle(seconds: float = 2.0) -> None:
    """The one sanctioned pause, for mail and invoices that land out of band."""
    time.sleep(seconds)


def client(token: str | None = None) -> httpx.Client:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=headers)


def rows_of(payload):
    if isinstance(payload, dict) and "items" in payload:
        return payload["items"]
    return payload


def _inbox_base() -> str:
    return os.environ["EMAIL_INBOX_API_URL"].rstrip("/")


def mails_to(address: str, subject_prefix: str = "") -> list[dict]:
    """Every message to one address, newest first, with its full text."""
    listing = httpx.get(f"{_inbox_base()}/messages", params={"limit": 1000},
                        timeout=TIMEOUT).json()
    found = []
    for item in listing.get("messages", []):
        recipients = [a.get("Address", "").lower() for a in item.get("To", [])]
        subject = item.get("Subject", "")
        if address.lower() in recipients and subject.startswith(subject_prefix):
            body = httpx.get(f"{_inbox_base()}/message/{item['ID']}",
                             timeout=TIMEOUT).json()
            found.append({"subject": subject, "text": body.get("Text", ""),
                          "to": recipients, "cc": body.get("Cc") or [],
                          "bcc": body.get("Bcc") or []})
    return found


def codes_for(address: str) -> list[str]:
    """Sign in codes sent to one address, newest first."""
    codes = []
    for mail in mails_to(address, CODE_SUBJECT):
        match = re.match(r"\s*(\d{6})", mail["text"])
        if match:
            codes.append(match.group(1))
    return codes


def request_code(phone: str, email: str) -> httpx.Response:
    return httpx.post(f"{api_base()}/auth/request-code",
                      json={"phone": phone, "email": email}, timeout=TIMEOUT)


def verify_code(phone: str, code: str) -> httpx.Response:
    return httpx.post(f"{api_base()}/auth/verify-code",
                      json={"phone": phone, "code": code}, timeout=TIMEOUT)


def sign_in(phone: str, email: str) -> str:
    before = len(codes_for(email))
    response = request_code(phone, email)
    assert response.status_code in (200, 201, 202), (
        f"requesting a sign in code for {phone} returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    codes = []
    for _ in range(15):
        codes = codes_for(email)
        if len(codes) > before:
            break
        settle(1.0)
    assert len(codes) > before, (
        f"no email with subject beginning {CODE_SUBJECT!r} reached {email}"
    )
    verified = verify_code(phone, codes[0])
    assert verified.status_code == 200, (
        f"verifying the newest code for {phone} returned {verified.status_code}: "
        f"{verified.text[:300]}"
    )
    token = verified.json().get("access_token")
    assert token, f"verify-code for {phone} returned no access_token"
    return token


@pytest.fixture(scope="session")
def shopper_token() -> str:
    return sign_in(SHOPPER_PHONE, SHOPPER_EMAIL)


@pytest.fixture(scope="session")
def second_token() -> str:
    return sign_in(SECOND_PHONE, SECOND_EMAIL)


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


def listing(c: httpx.Client, **params) -> dict:
    response = c.get("/products", params=params)
    assert response.status_code == 200, (
        f"GET /api/products {params} returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    return response.json()


def handles(payload: dict) -> list[str]:
    return [row["handle"] for row in rows_of(payload)]


def product(c: httpx.Client, handle: str) -> httpx.Response:
    return c.get(f"/products/{handle}")


def add_line(c: httpx.Client, sku: str, quantity: int = 1) -> httpx.Response:
    return c.post("/cart/lines", json={"sku": sku, "quantity": quantity})


def cart(c: httpx.Client) -> dict:
    response = c.get("/cart")
    assert response.status_code == 200, (
        f"GET /api/cart returned {response.status_code}: {response.text[:300]}"
    )
    return response.json()


def line_for(payload: dict, sku: str) -> dict | None:
    for line in payload.get("lines", []):
        if line.get("sku") == sku:
            return line
    return None


def order_body(email: str | None = None, pincode: str = SERVED_PINCODE,
               method: str = "standard") -> dict:
    return {
        "name": SHOPPER_NAME,
        "email": email or unique_email(),
        "address": {"line1": "12 Linking Road", "line2": "Bandra West",
                    "city": "Mumbai", "region": "Maharashtra", "pincode": pincode},
        "delivery_method": method,
    }


def place_order(c: httpx.Client, **kwargs) -> httpx.Response:
    return c.post("/orders", json=order_body(**kwargs))


def pay(c: httpx.Client, number: str) -> httpx.Response:
    return c.post(f"/orders/{number}/pay")


def _killbill() -> httpx.Client:
    return httpx.Client(
        base_url=os.environ["PAYMENTS_API_URL"].rstrip("/"),
        timeout=TIMEOUT,
        auth=(os.environ["PAYMENTS_ADMIN_USER"], os.environ["PAYMENTS_ADMIN_PASSWORD"]),
        headers={"X-Killbill-ApiKey": os.environ["PAYMENTS_API_KEY"],
                 "X-Killbill-ApiSecret": os.environ["PAYMENTS_API_SECRET"]},
    )


def killbill_account(phone: str) -> dict | None:
    with _killbill() as kb:
        response = kb.get("/1.0/kb/accounts", params={"externalKey": f"shopper-{phone}"})
        if response.status_code == 404:
            return None
        assert response.status_code == 200, (
            f"Kill Bill account lookup for shopper-{phone} returned "
            f"{response.status_code}: {response.text[:300]}"
        )
        return response.json()


def killbill_invoices_for_order(phone: str, number: str) -> list[dict]:
    """Invoices on the shopper's Kill Bill account whose items name this order.

    Amounts are read from each invoice by id: Kill Bill's list endpoints report
    an external charge invoice with amount 0.0, so a list read cannot see them.
    """
    account = killbill_account(phone)
    if account is None:
        return []
    matched = []
    with _killbill() as kb:
        listing_response = kb.get("/1.0/kb/invoices/pagination", params={"limit": 10000})
        assert listing_response.status_code == 200, listing_response.text[:300]
        payload = listing_response.json()
        rows = payload if isinstance(payload, list) else payload.get("items", [])
        for row in rows:
            if row.get("accountId") != account["accountId"]:
                continue
            full = kb.get(f"/1.0/kb/invoices/{row['invoiceId']}",
                          params={"withItems": "true"}).json()
            items = full.get("items") or []
            if any(str(i.get("description", "")).startswith(f"Order {number}")
                   for i in items):
                matched.append(full)
    return matched


def app_page(path: str = "/") -> httpx.Response:
    return httpx.get(f"{app_url()}{path}", timeout=TIMEOUT, follow_redirects=True)
