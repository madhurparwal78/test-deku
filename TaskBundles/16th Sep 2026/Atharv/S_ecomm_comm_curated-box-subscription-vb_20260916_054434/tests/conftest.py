from __future__ import annotations

import os
import time
from datetime import datetime, timezone

import pytest
from appclient import client, login, seeded_password
from capabilities import Backend, Inbox, Payments, make_backend, make_inbox, make_payments

MEMBER_EMAIL = "member@example.com"
MEMBER2_EMAIL = "member2@example.com"
MEMBER3_EMAIL = "member3@example.com"
READER_EMAIL = "reader@example.com"
SEED_PASSWORD = "deku-demo-pw-2026"

US_BASE_MINOR = 1799
US_EXTRA_MINOR = 1099
CA_BASE_MINOR = 2599
CA_EXTRA_MINOR = 1599
PROMOTION_BASE_MINOR = 400
PROMOTION_CODE = "SUMMER"
SEEDED_GIFT_CODE = "PANGOLIN-GIFT-7K42"

USD = "usd"
CAD = "cad"

CURRENT_SLUGS = (
    "the-lamplighters-daughter",
    "salt-and-static",
    "nine-yards-of-night",
    "the-orrery-thief",
    "a-quiet-inventory",
    "the-marmalade-conspiracy",
    "every-third-tuesday",
)
PREVIOUS_SLUGS = ("the-glass-cartographer", "feral-arithmetic")
BACKLIST_SLUGS = (
    "salt-and-static-reprint",
    "saltmarsh-2024-members-choice-winner",
    "the-paper-wife-2025-members-choice-winner",
    "the-pangolin-anthology",
)

LOGIN_ROUTE = "/api/auth/login"


def settle(seconds: float = 2.0) -> None:
    time.sleep(seconds)


def current_utc_year() -> str:
    return str(datetime.now(timezone.utc).year)


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


def _authed(email: str, env_var: str):
    token = login(email, seeded_password(env_var, SEED_PASSWORD))
    return client(token)


@pytest.fixture(scope="session")
def member_client():
    with _authed(MEMBER_EMAIL, "SEED_MEMBER_PASSWORD") as c:
        yield c


@pytest.fixture(scope="session")
def member2_client():
    with _authed(MEMBER2_EMAIL, "SEED_MEMBER2_PASSWORD") as c:
        yield c


@pytest.fixture(scope="session")
def member3_client():
    with _authed(MEMBER3_EMAIL, "SEED_MEMBER3_PASSWORD") as c:
        yield c


class ClubStore:
    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def member_by_email(self, email: str) -> dict | None:
        return self._b.one("members", email=email)

    def count_members(self, **where) -> int:
        return self._b.count("members", **where)

    def subscription_of(self, member_id) -> dict | None:
        return self._b.one("subscriptions", member_id=member_id)

    def count_subscriptions(self, **where) -> int:
        return self._b.count("subscriptions", **where)

    def edition_by_slug(self, slug: str) -> dict | None:
        return self._b.one("editions", slug=slug)

    def count_editions(self, **where) -> int:
        return self._b.count("editions", **where)

    def editions(self, limit: int | None = None, **where) -> list[dict]:
        return self._b.rows("editions", limit=limit, **where)

    def boxes_for(self, member_id, state: str | None = None) -> list[dict]:
        where: dict = {"member_id": member_id}
        if state:
            where["state"] = state
        return self._b.rows("boxes", **where)

    def count_boxes(self, **where) -> int:
        return self._b.count("boxes", **where)

    def box_items(self, box_id) -> list[dict]:
        return self._b.rows("box_items", box_id=box_id)

    def orders_for(self, member_id) -> list[dict]:
        return self._b.rows("orders", member_id=member_id)

    def count_orders(self, **where) -> int:
        return self._b.count("orders", **where)

    def ledger_for(self, member_id, reason: str | None = None) -> list[dict]:
        where: dict = {"member_id": member_id}
        if reason:
            where["reason"] = reason
        return self._b.rows("credit_ledger", **where)

    def count_ledger(self, **where) -> int:
        return self._b.count("credit_ledger", **where)

    def gift_by_code(self, code: str) -> dict | None:
        return self._b.one("gifts", code=code)

    def count_gifts(self, **where) -> int:
        return self._b.count("gifts", **where)

    def promotion_by_code(self, code: str) -> dict | None:
        return self._b.one("promotions", code=code)

    def pricing_for(self, country: str) -> dict | None:
        return self._b.one("country_pricing", country=country)

    def count_ballots(self, **where) -> int:
        return self._b.count("ballots", **where)

    def count_tags(self, **where) -> int:
        return self._b.count("tags", **where)


@pytest.fixture(scope="session")
def db() -> ClubStore:
    return ClubStore(make_backend())


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    return make_inbox()


@pytest.fixture(scope="session")
def payments() -> Payments:
    return make_payments()


@pytest.fixture
def probe_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


@pytest.fixture
def probe_token() -> str:
    return f"probe-{os.urandom(6).hex()}"


def signup_payload(email: str, country: str = "US") -> dict:
    return {"email": email, "password": SEED_PASSWORD, "country": country}


def empty_box(client_) -> None:
    response = client_.get("/box")
    assert response.status_code == 200, (
        f"GET /api/box returned {response.status_code}: {response.text[:400]}"
    )
    for item in _box_items(response.json()):
        slug = item.get("slug") if isinstance(item, dict) else item
        if slug:
            client_.delete(f"/box/items/{slug}")


def _box_items(payload) -> list:
    if isinstance(payload, dict):
        for key in ("items", "box_items", "editions"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
        box = payload.get("box")
        if isinstance(box, dict):
            return _box_items(box)
    if isinstance(payload, list):
        return payload
    return []


def box_items_of(payload) -> list:
    return _box_items(payload)


def add_to_box(client_, slug: str):
    return client_.post("/box/items", json={"slug": slug})


def place_box(client_, **body):
    return client_.post("/box/place", json=dict(body))


def build_box(client_, slugs) -> None:
    empty_box(client_)
    for slug in slugs:
        response = add_to_box(client_, slug)
        assert response.status_code in (200, 201), (
            f"POST /api/box/items {{'slug': {slug!r}}} returned "
            f"{response.status_code}: {response.text[:400]}"
        )
