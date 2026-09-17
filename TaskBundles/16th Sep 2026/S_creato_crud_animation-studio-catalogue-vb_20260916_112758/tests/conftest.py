from __future__ import annotations

import os
import time
import uuid

import pytest

import appclient
import capabilities

SETTLE_SECONDS = float(os.environ.get("DEKU_SETTLE_SECONDS", "2.0"))
POLL_DEADLINE_SECONDS = 30.0

PASSWORD = appclient.seeded_password("DEKU_SEED_PASSWORD", "deku-demo-pw-2026")

EDITOR = "editor@example.com"
PUBLISHER = "publisher@example.com"
PRODUCER = "producer@example.com"
SHOPKEEPER = "shopkeeper@example.com"
OWNER = "owner@example.com"
CUSTOMER = "customer@example.com"
CUSTOMER_TWO = "customer2@example.com"

CATALOGUE_TOTAL = 6
BRANDED_COUNT = 3
ENTERTAINMENT_COUNT = 3

READABLE_TITLES = (
    "Constellations",
    "The Summit",
    "Jungle All Stars",
    "A Hundred Years of Sweet",
    "Mistfall",
    "Kerb Kings",
)
EMBARGOED_TITLE = "Nightjar"
EXPIRED_TITLE = "Paper Lantern"
DRAFT_TITLE = "Low Tide"
WITHHELD_CLIENT = "Kessel"
NAMEABLE_CLIENT = "Verano"
DEPARTED_CREDIT = "Halle Brandt"
CONFIDENTIAL_SLATE_TITLE = "The Ends of Peck"

BRANDED = "Branded"
ENTERTAINMENT = "Entertainment"

DIGITAL_PRODUCT = "Beatboard Templates"
UPDATED_PRODUCT = "Rostrum Brush Pack"
LAST_EDITION = "Studio Tee"
SOLD_OUT_EDITION = "Crop Mark Print"

INDUSTRY_ORDER = (
    "Director",
    "Producer",
    "Production Manager",
    "Art Director",
    "Animation Lead",
    "Clean-up Lead",
    "Compositing Lead",
)

RESTRICTED_SUBJECTS = ("Head of Development / IP", "Games")
OPEN_SUBJECT = "Commercials and Branded Content"

DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
CREATED = (200, 201)
REFUSED = (400, 409, 422)


def settle() -> None:
    """The one sanctioned sleep: a bounded wait before asserting a non-event."""
    time.sleep(SETTLE_SECONDS)


def probe_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


def probe_key() -> str:
    return f"probe-{uuid.uuid4().hex}"


def poll_until(predicate, timeout: float = POLL_DEADLINE_SECONDS):
    """Poll a predicate to a monotonic deadline; return its last truthy value."""
    deadline = time.monotonic() + timeout
    outcome = None
    while time.monotonic() < deadline:
        outcome = predicate()
        if outcome:
            return outcome
        settle()
    return outcome


def _titles(records) -> list[str]:
    return [str(record.get("title", "")) for record in records]


def _flat(payload) -> str:
    import _shapes

    return _shapes.flatten(payload)


@pytest.fixture()
def anon():
    with appclient.client() as http:
        yield http


@pytest.fixture()
def backend():
    return capabilities.make_backend()


def _session(email: str):
    token = appclient.login(email, PASSWORD)
    return appclient.client(token)


@pytest.fixture()
def editor():
    with _session(EDITOR) as http:
        yield http


@pytest.fixture()
def publisher():
    with _session(PUBLISHER) as http:
        yield http


@pytest.fixture()
def producer():
    with _session(PRODUCER) as http:
        yield http


@pytest.fixture()
def shopkeeper():
    with _session(SHOPKEEPER) as http:
        yield http


@pytest.fixture()
def owner():
    with _session(OWNER) as http:
        yield http


@pytest.fixture()
def customer():
    with _session(CUSTOMER) as http:
        yield http


@pytest.fixture()
def customer_two():
    with _session(CUSTOMER_TWO) as http:
        yield http


def catalogue(http, **params) -> list[dict]:
    import _shapes

    response = http.get("/catalogue", params=params or None)
    assert response.status_code == 200, (
        f"GET /api/catalogue returned {response.status_code}: {response.text[:300]}"
    )
    return _shapes.items(response.json())


def counts(http) -> dict:
    response = http.get("/catalogue/counts")
    assert response.status_code == 200, (
        f"GET /api/catalogue/counts returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    return response.json()


def facet_count(payload: dict, label: str) -> int:
    facets = payload.get("facets") or []
    for facet in facets:
        name = str(facet.get("label") or facet.get("slug") or "")
        if name.strip().lower() == label.strip().lower():
            return int(facet.get("count"))
    raise AssertionError(
        f"no facet named {label!r} in the counts payload: {str(payload)[:300]}"
    )


def record_id(record: dict):
    for key in ("id", "record_id", "identity", "uuid"):
        if key in record and record[key] not in (None, ""):
            return record[key]
    raise AssertionError(f"record carries no identifier: {str(record)[:300]}")


def studio_records(http, **params) -> list[dict]:
    import _shapes

    response = http.get("/studio/records", params=params or None)
    assert response.status_code == 200, (
        f"GET /api/studio/records returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    return _shapes.items(response.json())


def find_record(http, title: str, **params) -> dict:
    for record in studio_records(http, **params):
        if str(record.get("title", "")).strip() == title:
            return record
    raise AssertionError(
        f"the back office lists no record titled {title!r}; the seed is incomplete"
    )


def transition(http, identifier, command: str, **body):
    payload = {"command": command}
    payload.update(body)
    return http.post(f"/studio/records/{identifier}/transition", json=payload)


def slug_of(record: dict) -> str:
    slug = record.get("slug")
    assert slug, f"record carries no slug: {str(record)[:300]}"
    return str(slug)


def case_study(http, slug: str):
    return http.get(f"/case-studies/{slug}")


def buy(http, product_slug: str, key: str | None = None):
    body = {"product_slug": product_slug, "idempotency_key": key or probe_key()}
    return http.post("/orders", json=body)


def product_slug(http, title: str) -> str:
    response = http.get("/shop")
    assert response.status_code == 200, (
        f"GET /api/shop returned {response.status_code}: {response.text[:300]}"
    )
    payload = response.json()
    for product in payload.get("products") or []:
        if str(product.get("title", "")).strip() == title:
            return str(product.get("slug"))
    raise AssertionError(
        f"the shop lists no product titled {title!r}: {str(payload)[:300]}"
    )


def rows_for_table(store, table: str, **where) -> int:
    return store.count(table, **where)


def page(http, route: str):
    """Fetch a public route's served markup through the app's own origin."""
    import httpx

    url = f"{appclient.app_url()}{route}"
    return httpx.get(url, timeout=appclient.TIMEOUT, follow_redirects=True)


def markup(route: str) -> str:
    import httpx

    response = httpx.get(f"{appclient.app_url()}{route}", timeout=appclient.TIMEOUT,
                         follow_redirects=True)
    assert response.status_code == 200, (
        f"GET {route} returned {response.status_code}: {response.text[:300]}"
    )
    return response.text


PUBLIC_ROUTES = ("/", "/work", "/entertainment", "/about", "/blog", "/podcast",
                 "/shop", "/contact", "/privacy", "/terms")

SECURITY_HEADERS = ("strict-transport-security", "x-content-type-options")
REQUEST_ID_HEADERS = ("x-request-id", "x-correlation-id", "request-id")
VENDOR_HEADERS = ("x-powered-by", "server")
CREDENTIAL_MARKERS = ("deku-local-dev", "postgresql://", "db_admin_url",
                      "authorization: bearer")


def stylesheets(html: str) -> str:
    """The document plus every same-origin stylesheet it links, as one string."""
    import re

    import httpx

    out = [html]
    for href in re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', html):
        if href.startswith("http") and appclient.app_url() not in href:
            continue
        url = href if href.startswith("http") else appclient.app_url() + href
        response = httpx.get(url, timeout=appclient.TIMEOUT)
        if response.status_code == 200:
            out.append(response.text)
    return chr(10).join(out)
