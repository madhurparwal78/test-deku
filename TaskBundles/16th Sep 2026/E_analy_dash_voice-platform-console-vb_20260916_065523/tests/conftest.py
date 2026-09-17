"""Fixtures, pinned literals and the one sanctioned sleep for the Vocalis Console.

Every literal here appears verbatim in instruction.md and on the Literals Ledger.
No test function lives in this file.
"""
from __future__ import annotations

import os
import time
import uuid

import pytest

import appclient
import capabilities

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 30.0

CORPUS_PASSWORD = "deku-demo-pw-2026"

OWNER_EMAIL = "owner@example.com"
SECOND_OWNER_EMAIL = "owner2@example.com"
ADMIN_EMAIL = "admin@example.com"
MEMBER_EMAIL = "member@example.com"
DENIED_MEMBER_EMAIL = "member2@example.com"
AUDITOR_EMAIL = "auditor@example.com"

PRIMARY_ORG_SLUG = "northwind-audio"
SECOND_ORG_SLUG = "halyard-labs"

METERED_PROJECT_SLUG = "contact-centre"
EMPTY_PROJECT_SLUG = "voice-notes"
ARCHIVED_PROJECT_SLUG = "meeting-capture"

SEEDED_PREFIX = "vclk2f8a"
REVOKED_PREFIX = "vclk6b1d"
SECRET_STEM = "vclk"
NEW_CREDENTIAL_LABEL = "Notes Ingest"

FIRST_CLIP = "Quarterly Review Call"
FIRST_CLIP_SECONDS = 180
FIRST_CLIP_ACCURACY = "97.4"

PERIOD_START = "2026-08-01"
PERIOD_END = "2026-08-31"

METERED_PROJECT_SECONDS = 5400
METERED_PROJECT_CHARACTERS = 6500
EMPTY_PROJECT_SECONDS = 1500
ORGANISATION_SECONDS = 7200
DENIED_VIEW_SECONDS = 5700

INVOICE_NUMBER = "NW-2026-0001"
INVOICE_TOTAL_MINOR = 19100
BALANCE_MINOR = 900

AUDIO_SECOND = "audio_second"
BATCH_LINE = "recognize.batch"

DENIED_STATUSES = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
OK_STATUSES = (200, 201)


def settle() -> None:
    """The only sanctioned sleep. Gives an absent side effect a fair chance to land."""
    time.sleep(SETTLE_SECONDS)


def run_tag() -> str:
    """A unique per-run identifier, so two identical runs never collide."""
    return uuid.uuid4().hex[:12]


def idempotency_key() -> str:
    return "probe-" + run_tag()


@pytest.fixture(scope="session")
def api() -> str:
    return appclient.api_base()


@pytest.fixture(scope="session")
def backend() -> capabilities.Backend:
    return capabilities.make_backend()


def _session(email: str):
    token = appclient.login(email, CORPUS_PASSWORD)
    return appclient.client(token)


@pytest.fixture()
def owner():
    with _session(OWNER_EMAIL) as c:
        yield c


@pytest.fixture()
def second_owner():
    with _session(SECOND_OWNER_EMAIL) as c:
        yield c


@pytest.fixture()
def administrator():
    with _session(ADMIN_EMAIL) as c:
        yield c


@pytest.fixture()
def member():
    with _session(MEMBER_EMAIL) as c:
        yield c


@pytest.fixture()
def denied_member():
    with _session(DENIED_MEMBER_EMAIL) as c:
        yield c


@pytest.fixture()
def auditor():
    with _session(AUDITOR_EMAIL) as c:
        yield c


@pytest.fixture()
def anonymous():
    with appclient.client(None) as c:
        yield c


def issue_credential(client, api: str, project_slug: str, label: str,
                     scopes: list[str]) -> dict:
    """Issue a credential and return the decoded issue response."""
    response = client.post(
        f"{api}/projects/{project_slug}/keys",
        json={"label": label, "scopes": scopes, "expires_at": None},
    )
    assert response.status_code in OK_STATUSES, (
        f"issuing credential {label!r} on project {project_slug!r} returned "
        f"{response.status_code}, expected one of {OK_STATUSES}; body={response.text[:400]}"
    )
    return response.json()


def credential_client(secret: str):
    """A client presenting a project credential secret to the usage intake."""
    return appclient.client(secret)


def submit_usage(client, api: str, key: str, line: str, quantity: int,
                 occurred_at: str) -> object:
    return client.post(
        f"{api}/usage/events",
        json={
            "idempotency_key": key,
            "line": line,
            "quantity": quantity,
            "unit": AUDIO_SECOND,
            "occurred_at": occurred_at,
        },
    )


def read_usage(client, api: str, scope_path: str, start: str, end: str) -> dict:
    response = client.get(
        f"{api}/{scope_path}/usage",
        params={"from": start, "to": end, "group_by": "line"},
    )
    assert response.status_code in OK_STATUSES, (
        f"reading usage at {scope_path!r} for {start}..{end} returned "
        f"{response.status_code}; body={response.text[:400]}"
    )
    return response.json()


def total_for_unit(payload: dict, unit: str) -> int:
    """The reported total for one unit, however the app spells its total block."""
    totals = payload.get("total_quantity")
    if isinstance(totals, dict):
        assert unit in totals, (
            f"usage response total_quantity {sorted(totals)} carries no entry for "
            f"unit {unit!r}"
        )
        return int(totals[unit])
    assert isinstance(totals, (int, float)), (
        f"usage response carries no usable total_quantity, found {totals!r}"
    )
    return int(totals)


def rows_sum(payload: dict, unit: str) -> int:
    rows = payload.get("rows")
    assert isinstance(rows, list), (
        f"usage response carries no rows list, found {type(rows).__name__}"
    )
    return sum(int(r.get("quantity", 0)) for r in rows
               if r.get("unit", unit) == unit)


def series_sum(payload: dict, unit: str) -> int:
    series = payload.get("series")
    assert isinstance(series, list), (
        f"usage response carries no series list, found {type(series).__name__}"
    )
    running = 0
    for band in series:
        if isinstance(band, dict) and band.get("unit", unit) != unit:
            continue
        points = band.get("points") if isinstance(band, dict) else None
        if isinstance(points, list):
            running += sum(int(p.get("quantity", 0)) for p in points)
        elif isinstance(band, dict) and "quantity" in band:
            running += int(band["quantity"])
    return running


def poll_until(predicate, message: str):
    """Bounded polling to a monotonic deadline. Never a bare sleep before a positive."""
    deadline = time.monotonic() + POLL_DEADLINE_SECONDS
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    raise AssertionError(f"{message}; last observation was {last!r}")


def public_routes() -> tuple:
    return ("/sign-in", "/terms")


def console_routes() -> tuple:
    return ("/overview", "/projects", "/usage", "/billing", "/members",
            "/approvals", "/audit", "/account")
