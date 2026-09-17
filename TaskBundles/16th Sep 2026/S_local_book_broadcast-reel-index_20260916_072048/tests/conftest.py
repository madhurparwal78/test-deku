"""Fixtures for the broadcast reel index task.

Composed from the vendored capability adapters only. Nothing here reads the app's
source; every observation is either an HTTP call against the running app or an
out-of-band read of the same PostgreSQL and the same mailbox the app writes to.
"""

from __future__ import annotations

import itertools
import uuid

import pytest

import appclient
import capabilities

CORPUS_PASSWORD = appclient.seeded_password("DEKU_SEED_PASSWORD", "deku-studio-2026")

PRINCIPAL_EMAIL = "dara@tallow.agency"
SECOND_PRINCIPAL_EMAIL = "otis@tallow.agency"
VISITOR_EMAIL = "casey@tallow.agency"

PRINCIPAL_NAME = "Dara Okonjo"
SEEDED_ATTENDEE = "marta@example.com"

SUBJECT_PREFIX = "Call confirmed:"
WORKED_SUBJECT = "Call confirmed: Dara Okonjo"

SEED_DAYS = ["2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08"]
SEED_SLOT_STARTS = ["14:00", "14:15", "14:30", "14:45"]

CATEGORIES = ["Campaign", "Film", "Documentary", "Re-Brand", "Out-of-Home",
              "Collaboration", "Integrated"]

FIRST_IN_INDEX = "tanaka-vertical-mile"
LAST_IN_INDEX = "tanaka-steppe-space-shuttle"
SECOND_IN_HOME = "norvel-master-the-route"
ABSENT_FROM_HOME = "norvel-drift"

_counter = itertools.count(1)


@pytest.fixture(scope="session")
def backend() -> capabilities.Backend:
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def inbox() -> capabilities.Inbox:
    return capabilities.make_inbox()


@pytest.fixture(scope="session")
def principal_token() -> str:
    return appclient.login(PRINCIPAL_EMAIL, CORPUS_PASSWORD)


@pytest.fixture(scope="session")
def second_principal_token() -> str:
    return appclient.login(SECOND_PRINCIPAL_EMAIL, CORPUS_PASSWORD)


@pytest.fixture(scope="session")
def visitor_token() -> str:
    return appclient.login(VISITOR_EMAIL, CORPUS_PASSWORD)


@pytest.fixture
def principal(principal_token):
    with appclient.client(principal_token) as c:
        yield c


@pytest.fixture
def second_principal(second_principal_token):
    with appclient.client(second_principal_token) as c:
        yield c


@pytest.fixture
def visitor(visitor_token):
    with appclient.client(visitor_token) as c:
        yield c


@pytest.fixture
def anonymous():
    with appclient.client() as c:
        yield c


def unique_suffix() -> str:
    """A value nothing else in the run will produce."""
    return f"{next(_counter)}-{uuid.uuid4().hex[:8]}"


def fresh_attendee() -> str:
    return f"attendee-{unique_suffix()}@example.com"


def slot_rows(backend: capabilities.Backend, **where) -> list[dict]:
    return backend.rows("availability_slots", **where)


def booked_slot_ids(backend: capabilities.Backend) -> set:
    return {r["slot_id"] for r in backend.rows("bookings", status="confirmed")}


def free_slot_ids(backend: capabilities.Backend) -> list:
    """Published slots carrying no confirmed booking, read out of band."""
    taken = booked_slot_ids(backend)
    return [r["id"] for r in slot_rows(backend, state="published")
            if r["id"] not in taken]


@pytest.fixture
def free_slot_id(backend):
    free = free_slot_ids(backend)
    assert free, "the seed carries no published slot without a booking"
    return free[0]


def details(attendee: str | None = None) -> dict:
    return {
        "attendee_name": "Priya Raman",
        "attendee_email": attendee or fresh_attendee(),
        "attendee_timezone": "Europe/Lisbon",
        "agenda": "A fifteen minute introduction about a spring campaign.",
    }


def place_hold(client, slot_id):
    return client.post("/holds", json={"slot_id": slot_id})


def confirm(client, slot_id, hold_id, body=None, key=None):
    payload = dict(body or details())
    payload["slot_id"] = slot_id
    payload["hold_id"] = hold_id
    headers = {"Idempotency-Key": key or f"key-{unique_suffix()}"}
    return client.post("/bookings", json=payload, headers=headers)


def held_slot(client, backend):
    """Take a free slot and hold it. Returns (slot_id, hold_id)."""
    for slot_id in free_slot_ids(backend):
        response = place_hold(client, slot_id)
        if response.status_code in (200, 201):
            body = response.json()
            return slot_id, body.get("id") or body.get("hold_id")
    raise AssertionError("no published slot could be held")


def expire_holds(backend: capabilities.Backend, slot_id) -> None:
    """Age every live hold on a slot out of band, so expiry is observable
    without waiting out the configured lifetime."""
    backend.query(
        "UPDATE slot_holds SET expires_at = now() - interval '1 hour' "
        "WHERE slot_id = %s",
        (slot_id,),
    )
