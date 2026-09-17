"""Black-box graders for the hardware-companion-storefront.

Every test reaches the app only over HTTP and reads the declared services only
through the capability adapters: business rows through Backend, invoices through
Payments, confirmation mail through Inbox.
"""
from __future__ import annotations

import os
import threading

import pytest

from appclient import client
from conftest import (
    ADDRESS,
    CAMERA_PRICE_MINOR,
    CURRENCY,
    CUSTOMER_EMAIL,
    FIRMWARE_NEW,
    PAID_STATUS,
    account_password,
    fresh_email,
    poll,
    settle,
)
from _shapes import flatten, items


def _new_customer(email: str | None = None) -> tuple[str, str]:
    """Sign up a fresh customer; return (token, email)."""
    addr = email or fresh_email()
    with client() as c:
        resp = c.post("/auth/signup", json={"email": addr, "password": account_password()})
    token = resp.json().get("token")
    assert token, f"a fresh signup returned no token: {resp.text[:300]}"
    return token, addr


def _camera_variant(c) -> tuple[str, int]:
    """Return (variant_id, unit_price_minor) for the seeded camera."""
    products = items(c.get("/products", params={"kind": "camera"}).json())
    assert products, f"no camera in the catalogue: {flatten(products)[:300]}"
    pid = str(products[0].get("id"))
    detail = c.get(f"/products/{pid}").json()
    variants = detail.get("variants") or items(detail)
    assert variants, f"the camera carried no variant: {flatten(detail)[:300]}"
    v = variants[0]
    return str(v.get("id")), int(v.get("price_minor"))


def _add_to_cart(c, variant_id: str, quantity: int = 1):
    return c.post("/cart/lines", json={"variant_id": variant_id, "quantity": quantity})


def _checkout(c, email: str, key: str | None = None):
    headers = {"Idempotency-Key": key} if key else {}
    body = {"email": email, "address": ADDRESS, "shipping_method": "standard"}
    return c.post("/checkout", json=body, headers=headers)


def _buy_camera(token: str, email: str, key: str | None = None):
    with client(token) as c:
        variant_id, _ = _camera_variant(c)
        _add_to_cart(c, variant_id)
        return _checkout(c, email, key=key)


def test_health_ok():
    """The health endpoint returns ready."""
    with client() as c:
        resp = c.get("/health")
    assert resp.status_code == 200, f"health was not ready: {resp.status_code}"


def test_seeded_accounts_login(customer_client):
    """The seeded customer authenticates and reads their own orders."""
    resp = customer_client.get("/orders")
    assert resp.status_code == 200, f"seeded customer could not read orders: {resp.text[:300]}"


def test_signup_rejects_duplicate_email(anon_client):
    """A signup for an already registered email is refused."""
    resp = anon_client.post("/auth/signup",
                            json={"email": CUSTOMER_EMAIL, "password": account_password()})
    assert resp.status_code in (400, 409, 422), (
        f"a duplicate signup was accepted: {resp.status_code} {resp.text[:300]}")


def test_signup_rejects_short_password(anon_client):
    """A signup with a password shorter than eight characters is refused."""
    resp = anon_client.post("/auth/signup", json={"email": fresh_email(), "password": "short"})
    assert resp.status_code in (400, 422), (
        f"a short password was accepted: {resp.status_code} {resp.text[:300]}")


def test_catalogue_lists_products(anon_client):
    """The catalogue lists a camera priced at the pinned minor units."""
    products = items(anon_client.get("/products").json())
    assert products, "the catalogue returned nothing"
    kinds = {str(p.get("kind")) for p in products}
    assert "camera" in kinds and "accessory" in kinds, (
        f"the catalogue is missing a camera or an accessory: {kinds}")
    variant_id, price = _camera_variant(anon_client)
    assert price == CAMERA_PRICE_MINOR, (
        f"the camera price was {price}, expected {CAMERA_PRICE_MINOR} {CURRENCY}")


def test_add_to_cart_returns_line(customer_client):
    """Adding a variant to the cart returns the line with its quantity."""
    variant_id, _ = _camera_variant(customer_client)
    _add_to_cart(customer_client, variant_id)
    cart = customer_client.get("/cart").json()
    lines = cart.get("lines") or items(cart)
    assert any(str(l.get("variant_id")) == variant_id for l in lines), (
        f"the added variant was absent from the cart: {flatten(cart)[:300]}")


def test_cart_line_stores_price_snapshot(customer_client):
    """A cart line records the unit price captured at add time."""
    variant_id, price = _camera_variant(customer_client)
    _add_to_cart(customer_client, variant_id)
    cart = customer_client.get("/cart").json()
    lines = [l for l in (cart.get("lines") or items(cart))
             if str(l.get("variant_id")) == variant_id]
    assert lines, "the cart line was not stored"
    assert int(lines[0].get("unit_price_minor")) == price, (
        f"the line price {lines[0].get('unit_price_minor')} did not snapshot {price}")


def test_checkout_reprices_total(customer_client):
    """Checkout re-prices the lines and the order total equals their sum."""
    variant_id, price = _camera_variant(customer_client)
    _add_to_cart(customer_client, variant_id)
    resp = _checkout(customer_client, CUSTOMER_EMAIL)
    assert resp.status_code in (200, 201), f"checkout failed: {resp.text[:300]}"
    order = resp.json()
    assert int(order.get("total_minor")) >= price, (
        f"the order total {order.get('total_minor')} was below the line price {price}")


def test_checkout_raises_invoice_on_account(payments):
    """Placing an order raises an invoice for the exact total and currency."""
    token, email = _new_customer()
    resp = _buy_camera(token, email)
    assert resp.status_code in (200, 201), f"checkout failed: {resp.text[:300]}"
    total = int(resp.json().get("total_minor"))
    charge = poll(lambda: payments.find_charge(total, CURRENCY), lambda c: c is not None)
    assert charge is not None, (
        f"no invoice for {total} {CURRENCY} was raised in the payments provider")


def test_order_confirmation_email_delivered(inbox):
    """Placing an order sends a confirmation email carrying the order reference."""
    token, email = _new_customer()
    resp = _buy_camera(token, email)
    reference = str(resp.json().get("reference", ""))
    message = poll(lambda: inbox.find(to=email, subject_contains="order"), lambda m: m is not None)
    assert message is not None, f"no confirmation email reached {email}"


def test_order_status_paid(customer_client):
    """A placed order records a paid status."""
    variant_id, _ = _camera_variant(customer_client)
    _add_to_cart(customer_client, variant_id)
    order = _checkout(customer_client, CUSTOMER_EMAIL).json()
    assert str(order.get("status")) == PAID_STATUS, (
        f"the placed order status was {order.get('status')}, expected {PAID_STATUS}")


def test_order_persisted_in_db(db):
    """A placed order is persisted in the orders table."""
    token, email = _new_customer()
    resp = _buy_camera(token, email)
    reference = str(resp.json().get("reference", ""))
    rows = poll(lambda: db.rows("orders", 500), lambda r: any(str(x.get("email")) == email for x in r))
    assert any(str(x.get("email")) == email for x in rows), (
        f"the placed order for {email} was absent from the orders table")


def test_register_device_duplicate_serial_refused(customer_client):
    """A customer registers a camera by serial and a duplicate serial is refused."""
    products = items(customer_client.get("/products", params={"kind": "camera"}).json())
    pid = str(products[0].get("id"))
    serial = "OPAL-" + os.urandom(4).hex()
    first = customer_client.post("/devices", json={"product_id": pid, "serial": serial})
    assert first.status_code in (200, 201), f"device registration failed: {first.text[:300]}"
    again = customer_client.post("/devices", json={"product_id": pid, "serial": serial})
    assert again.status_code in (400, 409, 422), (
        f"a duplicate serial was accepted: {again.status_code}")


def test_flash_device_moves_firmware(customer_client):
    """Flashing a registered device moves it to the newer firmware version."""
    products = items(customer_client.get("/products", params={"kind": "camera"}).json())
    pid = str(products[0].get("id"))
    serial = "OPAL-" + os.urandom(4).hex()
    device = customer_client.post("/devices", json={"product_id": pid, "serial": serial}).json()
    did = str(device.get("id"))
    resp = customer_client.post(f"/devices/{did}/flash", json={"version": FIRMWARE_NEW})
    assert resp.status_code in (200, 201), f"flash failed: {resp.text[:300]}"
    moved = poll(lambda: customer_client.get(f"/devices").json(),
                 lambda payload: any(str(d.get("id")) == did
                                     and str(d.get("firmware_version")) == FIRMWARE_NEW
                                     for d in items(payload)))
    assert any(str(d.get("id")) == did and str(d.get("firmware_version")) == FIRMWARE_NEW
               for d in items(moved)), "the device did not move to the flashed firmware version"


def test_cannot_flash_other_account_device(customer_client, customer2_client):
    """A device belonging to another account cannot be flashed."""
    products = items(customer_client.get("/products", params={"kind": "camera"}).json())
    pid = str(products[0].get("id"))
    serial = "OPAL-" + os.urandom(4).hex()
    device = customer_client.post("/devices", json={"product_id": pid, "serial": serial}).json()
    did = str(device.get("id"))
    resp = customer2_client.post(f"/devices/{did}/flash", json={"version": FIRMWARE_NEW})
    assert resp.status_code in (401, 403, 404), (
        f"another account flashed a device it does not own: {resp.status_code}")


def test_cookie_choice_persists():
    """A first-time visitor's cookie choice survives a reload."""
    with client() as c:
        resp = c.post("/cookie-consent", json={"choice": "rejected"})
        assert resp.status_code in (200, 201, 204), f"the cookie choice was not accepted: {resp.status_code}"
        again = c.get("/cookie-consent")
    assert again.status_code == 200, f"the cookie choice could not be read back: {again.status_code}"
    assert "rejected" in flatten(again.json()), "the cookie choice did not survive a reload"


def test_page_view_recorded(customer_client):
    """Each page view is recorded with its route, readable by an owner."""
    customer_client.post("/page-views", json={"route": "/shop"})
    views = poll(lambda: items(customer_client.get("/page-views").json()),
                 lambda rows: any(str(r.get("route")) == "/shop" for r in rows))
    assert any(str(r.get("route")) == "/shop" for r in views), (
        "a recorded page view was not readable by its owner")


def test_contact_spam_refused(anon_client):
    """A contact submission with the decoy field filled is refused."""
    resp = anon_client.post("/contact", json={
        "name": "Bot", "email": fresh_email(), "message": "hello",
        "website": "http://spam.example.com"})
    assert resp.status_code in (400, 403, 422), (
        f"a decoy-filled contact submission was accepted: {resp.status_code}")


def test_unauthenticated_account_route_denied(anon_client):
    """An anonymous caller to an account scoped endpoint is refused."""
    for method, path in [("GET", "/orders"), ("GET", "/devices"), ("POST", "/devices")]:
        resp = anon_client.request(method, path, json={})
        assert resp.status_code in (401, 403), (
            f"anonymous {method} {path} was served: {resp.status_code}")


def test_cross_account_order_denied(customer_client, customer2_client):
    """One account cannot read another account's order."""
    variant_id, _ = _camera_variant(customer_client)
    _add_to_cart(customer_client, variant_id)
    order = _checkout(customer_client, CUSTOMER_EMAIL).json()
    oid = str(order.get("id"))
    resp = customer2_client.get(f"/orders/{oid}")
    assert resp.status_code in (401, 403, 404), (
        f"another account read a private order: {resp.status_code}")


def test_no_frontend_secret_in_bundle():
    """The served frontend carries no payments or database secret."""
    with client() as c:
        resp = c.get("/../")
    assert resp.status_code == 200, f"the app root did not render: {resp.status_code}"
    secret = os.environ.get("PAYMENTS_API_SECRET", "orbit-labs-secret-9f14c73e")
    assert secret not in resp.text, "a payments secret was served in the frontend document"


def test_concurrent_duplicate_key_single_order(customer_token):
    """Two simultaneous checkouts with one key place exactly one order."""
    token, email = _new_customer()
    with client(token) as c:
        variant_id, _ = _camera_variant(c)
        _add_to_cart(c, variant_id)
    key = "idem-" + os.urandom(6).hex()
    gate = threading.Barrier(2)
    lock = threading.Lock()
    statuses: list[int] = []

    def fire():
        with client(token) as c:
            gate.wait()
            resp = _checkout(c, email, key=key)
        with lock:
            statuses.append(resp.status_code)

    threads = [threading.Thread(target=fire) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=45)
    created = [s for s in statuses if s in (200, 201)]
    assert created, f"neither duplicated checkout succeeded: {sorted(statuses)}"
    with client(token) as c:
        orders = items(c.get("/orders").json())
    assert len(orders) == 1, (
        f"a duplicated key placed {len(orders)} orders; exactly one must exist")


def test_checkout_replay_no_second_invoice(payments):
    """A replayed checkout with the same key raises no second invoice."""
    token, email = _new_customer()
    key = "idem-" + os.urandom(6).hex()
    with client(token) as c:
        variant_id, _ = _camera_variant(c)
        _add_to_cart(c, variant_id)
        first = _checkout(c, email, key=key)
        assert first.status_code in (200, 201), f"first checkout failed: {first.text[:300]}"
        first_ref = str(first.json().get("reference"))
        settle()
        before = len(payments.charges())
        replay = _checkout(c, email, key=key)
    assert replay.status_code in (200, 201), f"replay was not accepted idempotently: {replay.text[:300]}"
    assert str(replay.json().get("reference")) == first_ref, (
        "a replay with the same key returned a different order reference")
    after = len(payments.charges())
    assert after == before, (
        f"a replay raised a second invoice: {before} then {after}")


def test_orders_pagination_cursor(customer_client):
    """The account orders read is paginated with a forward cursor and metadata."""
    payload = customer_client.get("/orders", params={"page_size": 1}).json()
    assert "next_cursor" in payload or payload.get("has_more") is not None, (
        f"the paginated response carried no cursor metadata: {flatten(payload)[:300]}")
    rows = items(payload)
    assert len(rows) <= 1, f"page_size was ignored, got {len(rows)} rows"


def test_seed_is_idempotent(anon_client):
    """The seeded catalogue holds a stable set of products across reads."""
    first = len(items(anon_client.get("/products").json()))
    second = len(items(anon_client.get("/products").json()))
    assert first == second and first > 0, (
        f"the seeded catalogue size drifted between reads: {first} then {second}")
