from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"
EMPLOYEE = "employee@example.com"
PARTNER = "partner@example.com"
PARTNER_SECOND = "partner2@example.com"
REVIEWER = "reviewer@example.com"
REVIEWER_SECOND = "reviewer2@example.com"
SEEDED_PRINCIPALS = (EMPLOYEE, PARTNER, PARTNER_SECOND, REVIEWER, REVIEWER_SECOND)

PARTNER_ENGAGEMENT_END = "2026-11-30"
PARTNER_SECOND_ENGAGEMENT_END = "2027-03-31"
WORKED_CAMPAIGN_END = "2027-01-31"
PARTNER_GRANTED_CLASSES = ("spot_icon", "pictogram")
PARTNER_SECOND_GRANTED_CLASSES = ("photograph",)

CHAPTER_SLUGS = ("framework", "voice-and-tone", "logo", "typography",
                 "iconography", "color", "imagery", "motion")
CHAPTER_TITLES = {
    "framework": "Framework",
    "voice-and-tone": "Voice & Tone",
    "logo": "Logo",
    "typography": "Typography",
    "iconography": "Iconography",
    "color": "Colour",
    "imagery": "Imagery",
    "motion": "Motion",
}
FRAMEWORK_PRINCIPLES = ("Prioritize Simplicity", "Deepen Understanding",
                        "Instant Feedback", "Subtle Playfulness")
MARK_EXPRESSIONS = ("Version A", "Version B")
STATEMENT_IDENTIFIER = "logo.expressions.2"

ASSET_CLASSES = ("mark", "spot_icon", "pictogram", "ui_icon", "photograph",
                 "typeface", "motion_clip")
APPLICATION_CLASSES = ("internal", "advertising", "co_brand", "merchandise",
                       "partnership", "press")
LEGAL_STAGE_CLASSES = ("co_brand", "merchandise", "partnership")
REQUEST_STATES = ("draft", "routed", "under_review", "changes_requested",
                  "approved", "granted", "rejected", "withdrawn", "expired")
CONDITION_KINDS = ("clear_space", "no_recolour", "attribution", "proof_required",
                   "territory", "expiry_override")
AVAILABILITY_BADGES = ("Available", "Request required", "Restricted", "Retired")
SCAN_STATES = ("pending", "clean", "quarantined")
ICON_DIMENSIONS = {"spot_icon": 120, "pictogram": 64, "ui_icon": 24}

OUTRO_DESTINATIONS = ("Brand Partner Toolkit", "Legal Branding Resources",
                      "Tessera Design")
FOOTER_DESTINATIONS = ("Modern Slavery Statement", "Impressum", "Cancel Contract",
                       "Cookies & CCPA preferences")
CONSENT_CONTROL = "Do not sell or share my personal data to third parties"
OWNING_STUDIO = "Tessera Brand Studio"
PARTNER_STUDIO = "Meridian Studio"
TYPE_FACES = ("Ridge Grotesk", "TS Ridge Grotesk", "Basis Grotesk", "Ridge Type")

PUBLIC_ROUTES = ("/", "/framework", "/voice-and-tone", "/logo", "/typography",
                 "/iconography", "/color", "/imagery", "/motion")
RESERVED_ROUTES = ("/2/", "/as", "/gs")
GOVERNED_ROUTES = ("/library", "/requests", "/queue", "/admin/audit")

SECURITY_HEADERS = ("strict-transport-security", "x-content-type-options",
                    "referrer-policy")
FRAME_HEADERS = ("content-security-policy", "x-frame-options")

PRINCIPAL_TABLES = ("principals", "principal", "users", "accounts")
ASSET_TABLES = ("assets", "asset")
CHAPTER_TABLES = ("chapters", "chapter")
REQUEST_TABLES = ("usage_requests", "usage_request", "requests", "request")
STAGE_TABLES = ("request_stages", "request_stage", "stages", "stage")
GRANT_TABLES = ("grants", "grant")
AUDIT_TABLES = ("audit_records", "audit_record", "audit_log", "audit")
DOWNLOAD_TABLES = ("downloads", "download")
CONSENT_TABLES = ("consent_choices", "consent_choice", "consents", "consent")

SETTLE_SECONDS = 2.0
POLL_BUDGET_SECONDS = 20.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned sleep. A bounded wait before asserting a non-event."""
    time.sleep(seconds)


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(value: str) -> datetime:
    text = str(value).strip().replace("Z", "+00:00")
    return datetime.fromisoformat(text).astimezone(timezone.utc)


def parse_date(value: str) -> datetime:
    text = str(value).strip()
    if "T" in text:
        return parse_iso(text)
    return datetime.fromisoformat(text).replace(tzinfo=timezone.utc)


def future_date(days_ahead: int = 60) -> str:
    return (now_utc() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url.path} -> "
            f"{response.status_code}: {response.text[:400]}")


def probe_token() -> str:
    return os.urandom(6).hex()


def poll_until(predicate, budget: float = POLL_BUDGET_SECONDS):
    """Bounded polling to a monotonic deadline. Returns the last value seen."""
    deadline = time.monotonic() + budget
    value = predicate()
    while not value and time.monotonic() < deadline:
        settle(1.0)
        value = predicate()
    return value


def resolve_table(backend, candidates: tuple, **where) -> str:
    """The first candidate table name the store actually answers for.

    Table naming is the agent's choice, so every store read goes through this
    rather than pinning one spelling. A miss on all candidates is a clear
    failure naming what was tried.
    """
    errors = []
    for name in candidates:
        try:
            backend.count(name, **where)
        except Exception as error:
            errors.append(f"{name}: {error}")
            if len(errors) == len(candidates):
                raise AssertionError(
                    f"none of the candidate tables {list(candidates)} could be "
                    f"read; the records this brief names must be queryable in the "
                    f"store. Errors: {errors}")
            continue
        return name
    raise AssertionError(
        f"none of the candidate tables {list(candidates)} could be read; the "
        f"records this brief names must be queryable in the store")


def count_rows(backend, candidates: tuple, **where) -> int:
    return backend.count(resolve_table(backend, candidates), **where)


def fetch_rows(backend, candidates: tuple, **where) -> list:
    return backend.rows(resolve_table(backend, candidates), **where)


def json_list(response: httpx.Response, label: str) -> list:
    assert response.status_code == 200, (
        f"{label} did not answer 200: {describe(response)}")
    rows = response.json()
    assert isinstance(rows, list), (
        f"{label} must return a top-level JSON array, got "
        f"{type(rows).__name__}: {response.text[:400]}")
    return rows


def page(route: str) -> httpx.Response:
    return httpx.get(f"{appclient.app_url()}{route}", timeout=appclient.TIMEOUT,
                     follow_redirects=True)


def raw_page(route: str) -> httpx.Response:
    return httpx.get(f"{appclient.app_url()}{route}", timeout=appclient.TIMEOUT,
                     follow_redirects=False)


def chapters(session: httpx.Client) -> list:
    return json_list(session.get("/chapters"), "GET /api/chapters")


def assets(session: httpx.Client, **params) -> list:
    return json_list(session.get("/assets", params=params or None),
                     "GET /api/assets")


def asset_of_class(session: httpx.Client, asset_class: str,
                   availability: str | None = None) -> dict:
    rows = [row for row in assets(session)
            if row.get("asset_class") == asset_class
            and (availability is None or row.get("availability") == availability)]
    assert rows, (
        f"no asset of class {asset_class!r} "
        f"{'with availability ' + repr(availability) if availability else ''} is "
        f"served from the library; the seed must carry one")
    return rows[0]


def asset_detail(session: httpx.Client, asset_id) -> httpx.Response:
    return session.get(f"/assets/{asset_id}")


def download(session: httpx.Client, asset_id) -> httpx.Response:
    return session.get(f"/assets/{asset_id}/download")


def submit_request(session: httpx.Client, asset_id, application_class: str,
                   campaign_end: str | None = None,
                   cited: list | None = None) -> httpx.Response:
    return session.post("/requests", json={
        "asset_id": asset_id,
        "application_class": application_class,
        "territory": "worldwide",
        "campaign_start": future_date(7),
        "campaign_end": campaign_end or future_date(120),
        "cited_statement_ids": cited if cited is not None else [STATEMENT_IDENTIFIER],
    })


def read_request(session: httpx.Client, request_id) -> httpx.Response:
    return session.get(f"/requests/{request_id}")


def withdraw_request(session: httpx.Client, request_id) -> httpx.Response:
    return session.post(f"/requests/{request_id}/withdraw")


def queue(session: httpx.Client) -> list:
    return json_list(session.get("/queue"), "GET /api/queue")


def decide(session: httpx.Client, stage_id, decision: str = "approve",
           conditions: list | None = None, reason: str | None = None) -> httpx.Response:
    body = {"decision": decision}
    if conditions is not None:
        body["conditions"] = conditions
    if reason is not None:
        body["reason"] = reason
    return session.post(f"/stages/{stage_id}/decision", json=body)


def grants(session: httpx.Client) -> list:
    return json_list(session.get("/grants"), "GET /api/grants")


def audit(session: httpx.Client, **params) -> httpx.Response:
    return session.get("/audit", params=params or None)


def stage_ids(payload: dict) -> list:
    """Every stage identifier a request payload names, however it is nested."""
    stages = payload.get("stages") or payload.get("request_stages") or []
    out = []
    for stage in stages:
        if isinstance(stage, dict) and stage.get("id") is not None:
            out.append(stage["id"])
    return out


def open_stage_ids(payload: dict) -> list:
    stages = payload.get("stages") or payload.get("request_stages") or []
    out = []
    for stage in stages:
        if not isinstance(stage, dict):
            continue
        outcome = stage.get("outcome") or stage.get("decision")
        if stage.get("id") is not None and not outcome:
            out.append(stage["id"])
    return out


def stage_holders(payload: dict) -> list:
    stages = payload.get("stages") or payload.get("request_stages") or []
    out = []
    for stage in stages:
        if not isinstance(stage, dict):
            continue
        holder = (stage.get("reviewer") or stage.get("holder")
                  or stage.get("assignee") or stage.get("reviewer_email"))
        if isinstance(holder, dict):
            holder = holder.get("email") or holder.get("id")
        if holder:
            out.append(str(holder))
    return out


def holder_of(payload: dict):
    holder = (payload.get("holder") or payload.get("current_holder")
              or payload.get("holder_email"))
    if isinstance(holder, dict):
        holder = holder.get("email") or holder.get("id")
    return holder


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture
def anon():
    with appclient.client() as session:
        yield session


@pytest.fixture
def employee():
    with appclient.client(appclient.login(EMPLOYEE, PASSWORD)) as session:
        yield session


@pytest.fixture
def partner():
    with appclient.client(appclient.login(PARTNER, PASSWORD)) as session:
        yield session


@pytest.fixture
def partner_second():
    with appclient.client(appclient.login(PARTNER_SECOND, PASSWORD)) as session:
        yield session


@pytest.fixture
def reviewer():
    with appclient.client(appclient.login(REVIEWER, PASSWORD)) as session:
        yield session


@pytest.fixture
def reviewer_second():
    with appclient.client(appclient.login(REVIEWER_SECOND, PASSWORD)) as session:
        yield session
