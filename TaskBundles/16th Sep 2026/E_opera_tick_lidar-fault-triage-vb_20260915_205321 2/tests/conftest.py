"""Task fixtures for deku/lidar-fault-triage-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout,
ORM or module names. The only assumptions are the App Contract (the app answers at
APP_PUBLIC_URL, REST under /api) and what instruction.md pinned: the endpoints in
the API shapes table, the table and field names in the Data model, the enum values
and the seeded accounts.

Provider agnostic: domain queries are composed from the generic Backend primitives
and the shared Inbox, never from a provider SDK.
"""

from __future__ import annotations

import time
import uuid

import pytest
from appclient import app_url as _app_url
from appclient import client, login, seeded_password
from capabilities import Backend, Inbox, make_backend, make_inbox

SETTLE_SECONDS = 3.0

ADMIN_EMAIL = "administrator@example.com"
PILOT_EMAIL = "pilot@example.com"
ENGINEER_EMAIL = "engineer@example.com"
ENGINEER2_EMAIL = "engineer2@example.com"
SEED_PASSWORD = "deku-demo-pw-2026"

ASSET_CLASSES = ("wind_turbines", "solar_farms", "power_lines", "substations")
FAULT_KINDS = ("crack", "deformation", "corrosion", "vegetation_encroachment")
SEEDED_SITES = ("Harrow Ridge Wind Farm", "Saltmarsh Solar Array",
                "Brackenfold Line", "Tollgate Substation")
SUBJECT_PREFIX = "Confirmed fault at"
PAST_FLOWN_AT = "2026-01-15T09:00:00Z"

OK = (200, 201)
DENIED = (401, 403)
REFUSED = (400, 409, 422)


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give an unwanted async side effect time to land before asserting it did not."""
    time.sleep(seconds)


def poll_until(predicate, timeout: float = 20.0, interval: float = 0.5):
    """Poll to a monotonic deadline; never a bare sleep before asserting presence."""
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle(interval)
    return last


def probe() -> str:
    """A unique per-run token, so two runs never collide on a created record."""
    return uuid.uuid4().hex[:10]


def as_list(payload) -> list:
    """A list endpoint returns a top-level array; tolerate a wrapped one."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "data", "faults", "sites"):
            if isinstance(payload.get(key), list):
                return payload[key]
    return []


def token_for(email: str) -> str:
    return login(email, seeded_password("SEED_PASSWORD", SEED_PASSWORD))


def create_site(admin_client, asset_class: str = "wind_turbines") -> dict:
    marker = probe()
    body = {
        "name": f"Probe Site {marker}",
        "asset_class": asset_class,
        "region": "North Probe",
        "owner_name": f"Owner {marker}",
        "owner_email": f"owner-{marker}@example.com",
    }
    r = admin_client.post("/sites", json=body)
    assert r.status_code in OK, (
        f"POST /api/sites as the administrator returned {r.status_code}: {r.text[:400]}"
    )
    site = r.json()
    site.setdefault("owner_email", body["owner_email"])
    site.setdefault("name", body["name"])
    return site


def fault_zone(severity: int = 3, deformation_mm: int = 10, kind: str = "crack",
               location: str | None = None) -> dict:
    return {
        "kind": kind,
        "location": location or f"Probe location {probe()}",
        "deformation_mm": deformation_mm,
        "severity": severity,
    }


def log_survey(pilot_client, site_id, zones: list[dict], notes: str | None = None):
    body = {
        "site_id": site_id,
        "flown_at": PAST_FLOWN_AT,
        "coverage_km2": 12.5,
        "notes": notes or f"probe survey {probe()}",
        "faults": zones,
    }
    return pilot_client.post("/surveys", json=body)


def logged_faults(response) -> list[dict]:
    assert response.status_code in OK, (
        f"POST /api/surveys returned {response.status_code}: {response.text[:400]}"
    )
    return as_list(response.json().get("faults"))


@pytest.fixture
def app_url() -> str:
    return _app_url()


@pytest.fixture
def anon_client():
    with client() as c:
        yield c


@pytest.fixture
def admin_client():
    with client(token_for(ADMIN_EMAIL)) as c:
        yield c


@pytest.fixture
def pilot_client():
    with client(token_for(PILOT_EMAIL)) as c:
        yield c


@pytest.fixture
def engineer_client():
    with client(token_for(ENGINEER_EMAIL)) as c:
        yield c


@pytest.fixture
def engineer2_client():
    with client(token_for(ENGINEER2_EMAIL)) as c:
        yield c


class TriageStore:
    """Domain queries for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def fault(self, fault_id) -> dict | None:
        return self._b.one("faults", id=fault_id)

    def faults_for_survey(self, survey_id) -> list[dict]:
        return self._b.rows("faults", survey_id=survey_id)

    def count_faults_at_location(self, location: str) -> int:
        return self._b.count("faults", location=location)

    def count_events(self, fault_id, kind: str) -> int:
        return self._b.count("fault_events", fault_id=fault_id, kind=kind)

    def events(self, fault_id, kind: str) -> list[dict]:
        return self._b.rows("fault_events", fault_id=fault_id, kind=kind)

    def count_surveys_with_notes(self, notes: str) -> int:
        return self._b.count("surveys", notes=notes)

    def count_sites_named(self, name: str) -> int:
        return self._b.count("sites", name=name)

    def count_staff_with_email(self, email: str) -> int:
        return self._b.count("staff", email=email)

    def staff_by_email(self, email: str) -> dict | None:
        return self._b.one("staff", email=email)

    def count_page_views(self, route: str) -> int:
        return self._b.count("page_views", route=route)


@pytest.fixture
def db() -> TriageStore:
    return TriageStore(make_backend())


@pytest.fixture
def inbox() -> Inbox:
    return make_inbox()
