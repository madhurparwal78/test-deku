"""Fixtures, pinned literals and the one sanctioned sleep for the Havenn task.

Every value here appears verbatim in instruction.md. Nothing in this file
inspects the application's source: the observations are HTTP responses and rows
in the declared datastore.
"""

from __future__ import annotations

import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"
GUEST_EMAIL = "guest@example.com"
GUEST2_EMAIL = "guest2@example.com"
HOST_EMAIL = "host@example.com"
HOST2_EMAIL = "host2@example.com"

CEDAR_LOFT = "Cedar Loft"
HARBOUR_COTTAGE = "Harbour Cottage"
KITE_HOUSE = "Kite House"
SALT_MARSH_CABIN = "Salt Marsh Cabin"

PM_OK = "pm-ok-4242"
PM_DECLINE = "pm-decline-0002"
PM_CHALLENGE = "pm-challenge-3184"
PM_CAPTURE_FAIL = "pm-capture-fail-0005"

LINE_NIGHTLY = "nightly_subtotal"
LINE_DISCOUNT = "length_of_stay_discount"
LINE_CLEANING = "cleaning_fee"
LINE_EXTRA_GUEST = "extra_guest_fee"
LINE_PET = "pet_fee"
LINE_SERVICE = "guest_service_fee"
LINE_TAXES = "taxes"

SETTLE_SECONDS = 2.0
POLL_CEILING_SECONDS = 90.0
CONTENDERS = 12
OK = (200, 201)
REFUSED = (400, 403, 409, 422)
DENIED = (401, 403)
MISSING = (401, 403, 404)


def settle() -> None:
    """The only sanctioned sleep. A bounded wait before asserting an absence."""
    time.sleep(SETTLE_SECONDS)


def hold_ttl_seconds() -> float:
    """The pending-hold lifetime the application runs against, read from its own
    environment variable so a shorter verifier-side value shrinks the wait."""
    raw = os.environ.get("PENDING_HOLD_TTL_SEC")
    assert raw, "PENDING_HOLD_TTL_SEC is unset in this environment"
    return float(raw)


def quote_ttl_seconds() -> float:
    raw = os.environ.get("QUOTE_TTL_SEC")
    assert raw, "QUOTE_TTL_SEC is unset in this environment"
    return float(raw)


def unique_key() -> str:
    return f"probe-{uuid.uuid4().hex}"


def unique_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


def poll_until(predicate, deadline_seconds: float):
    """Poll to a monotonic deadline. Returns the first truthy result, else None."""
    limit = min(float(deadline_seconds), POLL_CEILING_SECONDS)
    started = time.monotonic()
    result = predicate()
    while not result and (time.monotonic() - started) < limit:
        settle()
        result = predicate()
    return result


def body_excerpt(response) -> str:
    return response.text[:400]


def as_list(payload):
    if isinstance(payload, dict):
        for key in ("results", "items", "data"):
            if isinstance(payload.get(key), list):
                return payload[key]
        return []
    return payload if isinstance(payload, list) else []


def listings(client):
    response = client.get("/listings")
    assert response.status_code == 200, (
        f"GET /api/listings returned {response.status_code}: {body_excerpt(response)}"
    )
    rows = as_list(response.json())
    assert rows, f"GET /api/listings returned no listing: {body_excerpt(response)}"
    return rows


def listing_id(client, title: str):
    for row in listings(client):
        if row.get("title") == title:
            found = row.get("listing_id", row.get("id"))
            assert found is not None, (
                f"the listing named {title!r} carries no listing_id: {row!r}"
            )
            return found
    raise AssertionError(
        f"no seeded listing titled {title!r} in GET /api/listings; the four seeded "
        f"titles are {CEDAR_LOFT}, {HARBOUR_COTTAGE}, {KITE_HOUSE}, {SALT_MARSH_CABIN}"
    )


def listing_detail(client, ident):
    response = client.get(f"/listings/{ident}")
    assert response.status_code == 200, (
        f"GET /api/listings/{ident} returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    return response.json()


def calendar(client, ident):
    response = client.get(f"/listings/{ident}/availability")
    assert response.status_code == 200, (
        f"GET /api/listings/{ident}/availability returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    days = as_list(response.json())
    assert days, (
        f"the availability of listing {ident} is empty; a seeded listing opens its "
        f"calendar for the coming year"
    )
    return days


def _day_index(days):
    return {row["local_date"]: row for row in days if row.get("local_date")}


def bookable_range(client, ident, nights: int = 2):
    """The first run of `nights` consecutive open dates that may be arrived on.

    Read from the application rather than computed here, so the dates are the
    ones the listing's own timezone produced.
    """
    days = calendar(client, ident)
    index = _day_index(days)
    ordered = sorted(index)
    for start in ordered:
        row = index[start]
        if not row.get("is_available"):
            continue
        if row.get("bookable_as_checkin") is False:
            continue
        first = date.fromisoformat(start)
        span = [index.get((first + timedelta(days=offset)).isoformat())
                for offset in range(nights)]
        if any(entry is None or not entry.get("is_available") for entry in span):
            continue
        checkout = (first + timedelta(days=nights)).isoformat()
        return start, checkout
    raise AssertionError(
        f"listing {ident} offers no run of {nights} bookable nights; a seeded "
        f"listing other than {SALT_MARSH_CABIN} opens its calendar for the year"
    )


def party(adults: int = 2, children: int = 0, infants: int = 0, pets: int = 0):
    return {"adults": adults, "children": children, "infants": infants, "pets": pets}


def quote_for(client, ident, checkin, checkout, guests=None):
    payload = {"listing_id": ident, "checkin": checkin, "checkout": checkout}
    payload.update(guests or party())
    response = client.post("/quotes", json=payload)
    assert response.status_code in OK, (
        f"POST /api/quotes for listing {ident} {checkin}..{checkout} returned "
        f"{response.status_code}: {body_excerpt(response)}"
    )
    return response.json()


def quote_attempt(client, ident, checkin, checkout, guests=None):
    payload = {"listing_id": ident, "checkin": checkin, "checkout": checkout}
    payload.update(guests or party())
    return client.post("/quotes", json=payload)


def lines_of(quote):
    rows = quote.get("lines")
    assert isinstance(rows, list), f"the quote carries no lines array: {quote!r}"
    return {row.get("code"): row.get("amount_minor_units") for row in rows}


def confirm(client, quote, key=None, method=PM_OK):
    headers = {"Idempotency-Key": key or unique_key()}
    ident = quote.get("quote_id")
    assert ident, f"the quote carries no quote_id: {quote!r}"
    return client.post(
        "/reservations",
        json={"quote_id": ident, "payment_method_reference": method},
        headers=headers,
    )


def confirmed(client, quote, key=None, method=PM_OK):
    response = confirm(client, quote, key=key, method=method)
    assert response.status_code in OK, (
        f"POST /api/reservations returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    return response.json()


def reservation_id(payload):
    for key in ("reservation_id", "id"):
        if payload.get(key) is not None:
            return payload[key]
    nested = payload.get("reservation") or {}
    for key in ("reservation_id", "id"):
        if nested.get(key) is not None:
            return nested[key]
    raise AssertionError(f"the confirm response carries no reservation_id: {payload!r}")


def race(callables):
    with ThreadPoolExecutor(max_workers=len(callables)) as pool:
        return [future.result() for future in
                [pool.submit(fn) for fn in callables]]


def html(path: str):
    return httpx.get(f"{appclient.app_url()}{path}", timeout=30.0,
                     follow_redirects=True)


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture()
def anon():
    with httpx.Client(base_url=appclient.api_base(), timeout=30.0) as client:
        yield client


@pytest.fixture()
def guest():
    with appclient.client(appclient.login(GUEST_EMAIL, PASSWORD)) as client:
        yield client


@pytest.fixture()
def other_guest():
    with appclient.client(appclient.login(GUEST2_EMAIL, PASSWORD)) as client:
        yield client


@pytest.fixture()
def host():
    with appclient.client(appclient.login(HOST_EMAIL, PASSWORD)) as client:
        yield client


@pytest.fixture()
def other_host():
    with appclient.client(appclient.login(HOST2_EMAIL, PASSWORD)) as client:
        yield client


@pytest.fixture()
def fresh_guest():
    """A signed-up guest nobody else in this run shares."""
    email = unique_email()
    response = httpx.post(f"{appclient.api_base()}/auth/signup",
                          json={"email": email, "password": PASSWORD}, timeout=30.0)
    assert response.status_code in OK, (
        f"POST /api/auth/signup for {email} returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    with appclient.client(appclient.login(email, PASSWORD)) as client:
        yield client
