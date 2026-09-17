"""Task fixtures for deku/fitness-gear-storefront-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout
or module names. The assumptions are the App Contract, the HTTP contract, the
copy and the seeded fixtures instruction.md pins, and the verifier-side services
the task declares: the Mailpit inbox API and the Kill Bill tenant.

Every scenario that changes state provisions its own products, bags, phones and
orders, so nothing asserted here depends on what the browser workflows did to
the seeded catalogue before pytest ran.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import random
import re
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from appclient import app_url
from playwright.sync_api import sync_playwright

TIMEOUT = 30.0

MERCHANT_PHONE = "9000000001"
MERCHANT_EMAIL = "merchant@example.com"
CUSTOMER_PHONE = "9000000011"
CUSTOMER_EMAIL = "customer@example.com"
CUSTOMER2_PHONE = "9000000012"
CUSTOMER3_PHONE = "9000000013"
CUSTOMER4_PHONE = "9000000014"
CUSTOMER4_EMAIL = "customer4@example.com"
CUSTOMER5_PHONE = "9000000015"
CUSTOMER5_EMAIL = "customer5@example.com"

CODE_SUBJECT = "Your Peakfit code"
POSTAL_COD = "560001"
POSTAL_HIGH_REFUSAL = "400050"
POSTAL_PREPAID_ONLY = "110001"
POSTAL_UNSERVED = "799001"
COD_CAP = 999900
ADVANCE_ABOVE = 499900
GIFT_SKU = "PF-GIFT-SHAKER"
VIBRATION_PLATE_SKU = "KIN-VP-PRO"
MASSAGE_GUN = "kinetra-compact-mini-massage-gun"
MASSAGE_GUN_SKU = "KIN-MG-GRAPHITE"
PAGE_SIZE = 24
RETURN_REASONS = ("too_small", "too_large", "not_as_described", "damaged",
                  "changed_mind", "wrong_item")
TRACK_KEYS = {"number", "state", "timeline"}
APP_SECRETS = ("carrier-sig-5e8d2b7a41", "kb-store-7c41e9", "mail-relay-9a3f62",
               "postgresql://", "deku-local-dev")
PUBLIC_ROUTES = ("/", "/collections/bestsellers", "/products/kinetra-compact-mini-massage-gun",
                 "/track", "/pages/privacy", "/build")
NOT_FOUND_COPY = "That page does not exist."
PRICE_SENTENCE = "\u20b91,899, reduced from \u20b93,499, saving 45%"
CLIENT_ERRORS = (400, 401, 403, 404, 409, 410, 422, 429)


def settle(seconds: float = 1.0) -> None:
    time.sleep(seconds)


def unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


def unique_phone() -> str:
    return "7" + "".join(random.choice("0123456789") for _ in range(9))


def unique_email() -> str:
    return f"shopper-{uuid.uuid4().hex[:12]}@example.com"


def hold_seconds() -> int:
    return int(os.environ.get("CART_HOLD_SECONDS", "45"))


def carrier_secret() -> str:
    return os.environ["CARRIER_WEBHOOK_SECRET"]


def api(token: str | None = None, headers: dict | None = None) -> httpx.Client:
    merged = dict(headers or {})
    if token:
        merged["Authorization"] = f"Bearer {token}"
    return httpx.Client(base_url=app_url(), timeout=TIMEOUT, headers=merged)


def body(response: httpx.Response) -> dict:
    try:
        payload = response.json()
    except ValueError as exc:
        raise AssertionError(
            f"{response.request.method} {response.request.url.path} answered "
            f"{response.status_code} with a non-JSON body: {response.text[:300]}") from exc
    return payload if isinstance(payload, dict) else {"items": payload}


def expect(response: httpx.Response, *statuses: int) -> dict:
    assert response.status_code in statuses, (
        f"{response.request.method} {response.request.url.path} answered "
        f"{response.status_code}, expected {statuses}: {response.text[:400]}")
    return body(response) if response.content else {}


def error_code(response: httpx.Response):
    if "json" not in response.headers.get("content-type", ""):
        return None
    payload = response.json()
    if isinstance(payload, dict) and isinstance(payload.get("error"), dict):
        return payload["error"].get("code")
    return None


def error_of(response: httpx.Response) -> dict:
    payload = body(response)
    err = payload.get("error")
    assert isinstance(err, dict), f"refusal carries no error object: {response.text[:300]}"
    return err


def poll(fetch, done, deadline_seconds: float, interval: float = 1.0):
    deadline = time.monotonic() + deadline_seconds
    last = fetch()
    while not done(last):
        if time.monotonic() >= deadline:
            return last
        settle(interval)
        last = fetch()
    return last


def in_parallel(count: int, work) -> list:
    results: list = [None] * count
    barrier = threading.Barrier(count)

    def run(index: int) -> None:
        barrier.wait()
        results[index] = work(index)

    threads = [threading.Thread(target=run, args=(i,)) for i in range(count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results


def inbox_base() -> str:
    return os.environ["EMAIL_INBOX_API_URL"].rstrip("/")


def mails_to(address: str, subject_prefix: str = "") -> list[dict]:
    listing = httpx.get(f"{inbox_base()}/messages", params={"limit": 1000},
                        timeout=TIMEOUT).json()
    found = []
    for item in listing.get("messages", []):
        recipients = [a.get("Address", "").lower() for a in item.get("To", [])]
        subject = item.get("Subject", "")
        if address.lower() in recipients and subject.startswith(subject_prefix):
            full = httpx.get(f"{inbox_base()}/message/{item['ID']}", timeout=TIMEOUT).json()
            found.append({"id": item["ID"], "subject": subject,
                          "text": full.get("Text", ""), "to": recipients})
    return found


def first_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def wait_for_mail(address: str, subject_prefix: str, known: set[str],
                  deadline_seconds: float = 60.0) -> dict | None:
    def fresh():
        return [m for m in mails_to(address, subject_prefix) if m["id"] not in known]

    found = poll(fresh, lambda ms: bool(ms), deadline_seconds, 1.0)
    return found[0] if found else None


def mail_ids(address: str) -> set[str]:
    return {m["id"] for m in mails_to(address)}


def request_code(phone: str, email: str) -> httpx.Response:
    with api() as c:
        return c.post("/api/auth/code", json={"phone": phone, "email": email})


def code_from(address: str, known: set[str]) -> str:
    message = wait_for_mail(address, CODE_SUBJECT, known)
    assert message, f"no `{CODE_SUBJECT}` email reached {address}"
    line = first_line(message["text"])
    assert re.fullmatch(r"\d{6}", line), (
        f"the code email's first line is {line!r}, not the six digits alone")
    return line


def fresh_code(phone: str, email: str, inbox: str | None = None) -> str:
    target = inbox or email
    known = mail_ids(target)
    expect(request_code(phone, email), 202)
    return code_from(target, known)


def sign_in(phone: str, email: str, inbox: str | None = None) -> str:
    code = fresh_code(phone, email, inbox)
    with api() as c:
        payload = expect(c.post("/api/auth/verify", json={"phone": phone, "code": code}), 200)
    token = payload.get("token")
    assert token, f"verify answered no token: {payload}"
    return token


@pytest.fixture(scope="session")
def chromium():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(chromium):
    context = chromium.new_context(base_url=app_url(), viewport={"width": 1280, "height": 900})
    context.set_default_timeout(20000)
    yield context.new_page()
    context.close()


@pytest.fixture(scope="session")
def merchant_token() -> str:
    return sign_in(MERCHANT_PHONE, MERCHANT_EMAIL)


@pytest.fixture(scope="session")
def customer_token() -> str:
    return sign_in(CUSTOMER_PHONE, CUSTOMER_EMAIL)


@pytest.fixture(scope="session")
def customer5_token() -> str:
    return sign_in(CUSTOMER5_PHONE, CUSTOMER5_EMAIL)


def new_product(merchant_token: str, department: str = "EQUIPMENTS",
                sub_category: str = "massagers", prices=(129900,), on_hand: int = 20,
                low_threshold: int = 2, cod_eligible: bool = True,
                backorderable: bool = False) -> dict:
    handle = unique("probe")
    variants = []
    for index, price in enumerate(prices):
        variants.append({"sku": f"{handle}-{index}".upper(), "options": {"size": str(index + 7)},
                         "price_minor": price, "on_hand": on_hand,
                         "low_threshold": low_threshold, "backorderable": backorderable})
    with api(merchant_token) as c:
        expect(c.post("/api/merchant/products", json={
            "handle": handle, "title": handle.replace("-", " "), "department": department,
            "sub_category": sub_category, "cod_eligible": cod_eligible,
            "variants": variants}), 201)
    return {"handle": handle, "skus": [v["sku"] for v in variants]}


def merchant_variant(merchant_token: str, sku: str) -> dict:
    with api(merchant_token) as c:
        return expect(c.get(f"/api/merchant/variants/{sku}"), 200)


def set_variant(merchant_token: str, sku: str, **fields) -> dict:
    with api(merchant_token) as c:
        return expect(c.patch(f"/api/merchant/variants/{sku}", json=fields), 200)


def product(handle: str) -> dict:
    with api() as c:
        return expect(c.get(f"/api/products/{handle}"), 200)


def variant_of(handle: str, sku: str) -> dict:
    for variant in product(handle).get("variants", []):
        if variant.get("sku") == sku:
            return variant
    raise AssertionError(f"{handle} lists no variant {sku}")


def new_cart() -> str:
    with api() as c:
        payload = expect(c.post("/api/carts"), 201)
    assert payload.get("token"), payload
    return payload["token"]


def add_line(cart: str, sku: str, quantity: int = 1) -> httpx.Response:
    with api() as c:
        return c.post(f"/api/carts/{cart}/lines", json={"sku": sku, "quantity": quantity})


def get_cart(cart: str) -> dict:
    with api() as c:
        return expect(c.get(f"/api/carts/{cart}"), 200)


def cart_with(skus: dict[str, int]) -> dict:
    cart = new_cart()
    for sku, quantity in skus.items():
        expect(add_line(cart, sku, quantity), 200)
    return get_cart(cart)


def address(postal_code: str = POSTAL_COD) -> dict:
    return {"name": "Probe Shopper", "line1": f"{random.randint(1, 900)} {unique('lane')} Road",
            "landmark": "Opposite the park", "city": "Bengaluru", "postal_code": postal_code}


def contact(phone: str, email: str) -> dict:
    return {"name": "Probe Shopper", "phone": phone, "email": email}


def place(cart: dict, phone: str, email: str, payment_method: str,
          postal_code: str = POSTAL_COD, code: str | None = None, key: str | None = None,
          expected_total: int | None = None, token: str | None = None,
          ship_to: dict | None = None, address_id: str | None = None) -> httpx.Response:
    order = {"cart_token": cart["token"], "contact": contact(phone, email),
             "payment_method": payment_method,
             "expected_total_minor": cart["total_minor"] if expected_total is None else expected_total}
    if address_id is not None:
        order["address_id"] = address_id
    else:
        order["address"] = ship_to or address(postal_code)
    if code is not None:
        order["verification_code"] = code
    with api(token, {"Idempotency-Key": key or unique("order")}) as c:
        return c.post("/api/orders", json=order)


def guest_cod_order(skus: dict[str, int], postal_code: str = POSTAL_COD) -> dict:
    phone, email = unique_phone(), unique_email()
    cart = cart_with(skus)
    code = fresh_code(phone, email)
    order = expect(place(cart, phone, email, "on_delivery", postal_code, code=code), 201)
    return {"order": order, "phone": phone, "email": email, "cart": cart}


def prepaid_order(skus: dict[str, int], postal_code: str = POSTAL_COD) -> dict:
    phone, email = unique_phone(), unique_email()
    cart = cart_with(skus)
    order = expect(place(cart, phone, email, "prepaid", postal_code), 201)
    return {"order": order, "phone": phone, "email": email, "cart": cart}


def merchant_order(merchant_token: str, number: str) -> dict:
    with api(merchant_token) as c:
        return expect(c.get(f"/api/merchant/orders/{number}"), 200)


def transition(merchant_token: str, number: str, to: str, reason: str = "") -> httpx.Response:
    with api(merchant_token) as c:
        return c.post(f"/api/merchant/orders/{number}/transitions",
                      json={"to": to, "reason": reason or f"verifier moves the order to {to}"})


def pack(merchant_token: str, number: str) -> None:
    state = merchant_order(merchant_token, number)["state"]
    if state == "placed":
        expect(transition(merchant_token, number, "confirmed"), 200)
    expect(transition(merchant_token, number, "packed"), 200)


def iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def signed(raw: str, secret: str | None = None, at: int | None = None) -> str:
    stamp = int(time.time()) if at is None else at
    digest = hmac.new((secret or carrier_secret()).encode("utf-8"),
                      f"{stamp}.{raw}".encode("utf-8"), hashlib.sha256).hexdigest()
    return f"t={stamp},v1={digest}"


def carrier(number: str, status: str, occurred_at: datetime | None = None,
            event_id: str | None = None, window: str | None = None,
            signature: str | None = None) -> httpx.Response:
    event = {"event_id": event_id or unique("evt"), "order_number": number, "status": status,
             "occurred_at": iso(occurred_at or now_utc())}
    if status == "out_for_delivery":
        event["window"] = window or "11:00 and 14:00"
    raw = json.dumps(event, separators=(",", ":"))
    headers = {"Content-Type": "application/json",
               "X-Carrier-Signature": signature if signature is not None else signed(raw)}
    with api() as c:
        return c.post("/api/webhooks/carrier", content=raw.encode("utf-8"), headers=headers)


def deliver(merchant_token: str, number: str, delivered_at: datetime | None = None) -> None:
    moment = delivered_at or now_utc()
    pack(merchant_token, number)
    for offset, status in ((-3, "shipped"), (-2, "out_for_delivery"), (0, "delivered")):
        response = carrier(number, status, moment + timedelta(hours=offset))
        assert response.status_code == 204, (
            f"carrier {status} for {number} answered {response.status_code}: {response.text[:300]}")


def order_for(token: str, number: str) -> httpx.Response:
    with api(token) as c:
        return c.get(f"/api/orders/{number}")


def track(number: str, last4: str) -> httpx.Response:
    with api() as c:
        return c.get("/api/track", params={"number": number, "phone_last4": last4})


def rupees(minor: int) -> str:
    return f"{minor // 100}.{minor % 100:02d}"


def killbill() -> httpx.Client:
    return httpx.Client(
        base_url=os.environ["PAYMENTS_API_URL"].rstrip("/"), timeout=TIMEOUT,
        auth=(os.environ["PAYMENTS_ADMIN_USER"], os.environ["PAYMENTS_ADMIN_PASSWORD"]),
        headers={"X-Killbill-ApiKey": os.environ["PAYMENTS_API_KEY"],
                 "X-Killbill-ApiSecret": os.environ["PAYMENTS_API_SECRET"]})


def killbill_account(phone: str) -> dict | None:
    with killbill() as kb:
        response = kb.get("/1.0/kb/accounts", params={"externalKey": f"peakfit-{phone}"})
    if response.status_code == 404:
        return None
    assert response.status_code == 200, (
        f"Kill Bill account lookup for peakfit-{phone} answered {response.status_code}: "
        f"{response.text[:300]}")
    return response.json()


def invoices_for(phone: str, number: str) -> list[dict]:
    account = killbill_account(phone)
    if account is None:
        return []
    matched = []
    with killbill() as kb:
        listing = kb.get(f"/1.0/kb/accounts/{account['accountId']}/invoices")
        assert listing.status_code == 200, listing.text[:300]
        for row in listing.json():
            full = kb.get(f"/1.0/kb/invoices/{row['invoiceId']}",
                          params={"withItems": "true"}).json()
            items = full.get("items") or []
            if any(str(i.get("description", "")).startswith(f"Order {number}") for i in items):
                matched.append(full)
    return matched


def invoices_settled(phone: str, number: str, count: int, deadline: float = 30.0) -> list[dict]:
    return poll(lambda: invoices_for(phone, number), lambda found: len(found) >= count,
                deadline, 1.0)


def amount_of(invoice: dict) -> str:
    return f"{float(invoice.get('amount')):.2f}"


def allocate(discount: int, totals: list[int]) -> list[int]:
    whole = sum(totals)
    shares = [discount * t // whole for t in totals]
    fractions = [(discount * t % whole, -i) for i, t in enumerate(totals)]
    left = discount - sum(shares)
    for _, neg_index in sorted(fractions, reverse=True)[:left]:
        shares[-neg_index] += 1
    return shares


def advance_for(total: int) -> int:
    return -(-total * 20 // 10000) * 100


def walk_products(params: dict) -> tuple[list[dict], list[int], int]:
    items, sizes, count = [], [], None
    cursor = None
    with api() as c:
        for _ in range(40):
            query = dict(params)
            if cursor:
                query["cursor"] = cursor
            page = expect(c.get("/api/products", params=query), 200)
            count = page.get("count") if count is None else count
            rows = page.get("items") or []
            items.extend(rows)
            sizes.append(len(rows))
            cursor = page.get("next_cursor")
            if not cursor:
                break
    return items, sizes, count


def keys_named(value, name: str) -> list[str]:
    found = []
    if isinstance(value, dict):
        for key, inner in value.items():
            if key.lower() == name:
                found.append(key)
            found.extend(keys_named(inner, name))
    elif isinstance(value, list):
        for inner in value:
            found.extend(keys_named(inner, name))
    return found
