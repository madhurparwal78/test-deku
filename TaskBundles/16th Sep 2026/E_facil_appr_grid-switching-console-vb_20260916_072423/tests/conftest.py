from __future__ import annotations

import os
import time

import pytest
from _shapes import items
from appclient import api_base, app_url, client, login, seeded_password
from capabilities import Backend, make_backend

OPERATOR_EMAIL = "operator@example.com"
OPERATOR2_EMAIL = "operator2@example.com"
COORDINATOR_EMAIL = "coordinator@example.com"
CONTROLLER_EMAIL = "controller@example.com"
AUDITOR_EMAIL = "auditor@example.com"
SEEDED_PASSWORD_DEFAULT = "deku-demo-pw-2026"

AREA_ONE = "Northgate"
AREA_TWO = "Harbourside"

PUBLISHED_TRAIN = 418
READY_TRAIN = 419

INCIDENT_REFERENCE = "INC-4471"
ORDER_REFERENCE = "SWO-2026-014"
PERMIT_REFERENCE = "SD-2291"
CREW_ONE = "C-07"
CREW_TWO = "C-12"

RECLOSER_KEY = "4B-RCL-118"
SECTIONALIZER_KEY = "NG-SEC-142"
TIE_KEY = "NG-TIE-330"
ISOLATED_CONDUCTOR_KEY = "NG-OHL-2202"
FAR_CONDUCTOR_KEY = "NG-OHL-2203"
HARBOURSIDE_CONDUCTOR_KEY = "HS-OHL-3301"
SUBSTATION_KEY = "NG-SUB-01"

SEEDED_ALARM_PRIORITY = 34412
SEEDED_CUSTOMERS_AT_RISK = 4412
IMPACT_MIN = 4100
IMPACT_MAX = 4700
SENSITIVE_COUNT = 61
ESTIMATED_COST_MINOR = 182400
CURRENCY = "usd"

OVERLOADED_LOADING = "1.070"
CLEAN_LOADING = "0.780"
VIOLATION_KIND = "thermal"

CONFIRM_TOKEN_SECONDS = 120
SUPPRESSION_MIN_SECONDS = 60
SUPPRESSION_MAX_SECONDS = 86400
RELEASE_DWELL_MS = 800
VERIFY_WINDOW_DAYS = 366

CODE_ALARM_ALREADY_ACKNOWLEDGED = "ALARM_ALREADY_ACKNOWLEDGED"
CODE_SUPPRESSION_BLOCKED = "SUPPRESSION_BLOCKED_BY_PERMIT"
CODE_OUT_OF_AREA = "OUT_OF_AREA"
CODE_COMMAND_VERSION_CONFLICT = "COMMAND_VERSION_CONFLICT"
CODE_SELF_APPROVAL_DENIED = "SELF_APPROVAL_DENIED"
CODE_VERSION_CONFLICT = "VERSION_CONFLICT"
CODE_CONFIRMATION_REQUIRED = "CONFIRMATION_REQUIRED"
CODE_APPROVAL_HASH_MISMATCH = "APPROVAL_HASH_MISMATCH"
CODE_STEP_OUT_OF_ORDER = "STEP_OUT_OF_ORDER"
CODE_MODEL_VERSION_ELEMENT_MISSING = "MODEL_VERSION_ELEMENT_MISSING"
CODE_SAFETY_DOCUMENT_CONFLICT = "SAFETY_DOCUMENT_CONFLICT"
CODE_SAFETY_VALIDATION_FAILED = "SAFETY_VALIDATION_FAILED"
CODE_LEASE_HELD = "LEASE_HELD"
CODE_UNDISPOSITIONED_ITEMS = "UNDISPOSITIONED_ITEMS"

DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
CREATED = (200, 201, 202)
REFUSED = (400, 409, 410, 422, 423)

SETTLE_SECONDS = 2.0
POLL_BUDGET_SECONDS = 30.0


def settle() -> None:
    """The only sanctioned sleep in this suite."""
    time.sleep(SETTLE_SECONDS)


def deadline(seconds: float = POLL_BUDGET_SECONDS) -> float:
    return time.monotonic() + seconds


def probe_suffix() -> str:
    return os.urandom(6).hex()


def token_for(email: str) -> str:
    return login(email, seeded_password("SEED_OPERATOR_PASSWORD", SEEDED_PASSWORD_DEFAULT))


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture
def operator_token() -> str:
    return token_for(OPERATOR_EMAIL)


@pytest.fixture
def operator_client(operator_token: str):
    with client(operator_token) as c:
        yield c


@pytest.fixture
def operator2_client():
    with client(token_for(OPERATOR2_EMAIL)) as c:
        yield c


@pytest.fixture
def coordinator_client():
    with client(token_for(COORDINATOR_EMAIL)) as c:
        yield c


@pytest.fixture
def controller_client():
    with client(token_for(CONTROLLER_EMAIL)) as c:
        yield c


@pytest.fixture
def auditor_client():
    with client(token_for(AUDITOR_EMAIL)) as c:
        yield c


class ConsoleStore:
    """Domain queries for this task, composed from the generic primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def user_row(self, email: str) -> dict | None:
        return self._b.one("app_user", email=email)

    def published_version(self) -> dict | None:
        return self._b.one("model_version", state="published")

    def version_by_train(self, train: int) -> dict | None:
        return self._b.one("model_version", train=train)

    def count_published_versions(self) -> int:
        return self._b.count("model_version", state="published")

    def element_by_key(self, key: str) -> dict | None:
        return self._b.one("network_element", stable_key=key)

    def count_elements(self) -> int:
        return self._b.count("network_element")

    def order_row(self, reference: str) -> dict | None:
        return self._b.one("switching_order", reference=reference)

    def steps_for(self, order_id) -> list[dict]:
        return self._b.rows("switching_step", limit=200, order_id=order_id)

    def approvals_for(self, order_id) -> list[dict]:
        return self._b.rows("approval_record", limit=200, order_id=order_id)

    def attempts_for(self, step_id) -> list[dict]:
        return self._b.rows("step_execution_attempt", limit=200, step_id=step_id)

    def count_attempts(self, step_id) -> int:
        return self._b.count("step_execution_attempt", step_id=step_id)

    def incident_row(self, reference: str) -> dict | None:
        return self._b.one("incident", reference=reference)

    def timeline_for(self, incident_id) -> list[dict]:
        return self._b.rows("incident_timeline_entry", limit=500, incident_id=incident_id)

    def alarm_rows(self) -> list[dict]:
        return self._b.rows("alarm", limit=500)

    def crew_row(self, call_sign: str) -> dict | None:
        return self._b.one("crew", call_sign=call_sign)

    def count_assignments(self, crew_id) -> int:
        return self._b.count("dispatch_assignment", crew_id=crew_id)

    def permit_rows(self) -> list[dict]:
        return self._b.rows("safety_document", limit=200)

    def audit_rows(self, limit: int = 2000) -> list[dict]:
        return self._b.rows("audit_event", limit=limit)

    def count_audit(self) -> int:
        return self._b.count("audit_event")

    def count_samples(self) -> int:
        return self._b.count("measurement_sample")

    def count_cookie_choices(self) -> int:
        return self._b.count("cookie_choice")


@pytest.fixture(scope="session")
def db() -> ConsoleStore:
    return ConsoleStore(make_backend())


def api(path: str) -> str:
    return f"{api_base()}{path}"


def page(path: str) -> str:
    return f"{app_url()}{path}"


def error_code(response) -> str:
    """The stable `code` string this brief pins on every refusal."""
    header = response.headers.get("content-type", "")
    if "json" not in header.lower():
        return ""
    body = response.json()
    error = body.get("error") if isinstance(body, dict) else None
    if isinstance(error, dict):
        return str(error.get("code", ""))
    return ""


def order_body(client_, reference: str = ORDER_REFERENCE) -> dict:
    response = client_.get(f"/v1/switching-orders/{reference}")
    assert response.status_code == 200, (
        f"GET /api/v1/switching-orders/{reference} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    body = response.json()
    assert isinstance(body, dict), (
        f"GET /api/v1/switching-orders/{reference} returned "
        f"{type(body).__name__}, expected the order object: {response.text[:400]}"
    )
    return body.get("data", body) if isinstance(body.get("data"), dict) else body


def new_order(client_, area: str = AREA_ONE) -> dict:
    response = client_.post(
        "/v1/switching-orders",
        json={"incident_reference": INCIDENT_REFERENCE, "area_name": area},
    )
    assert response.status_code in CREATED, (
        f"POST /api/v1/switching-orders for {area!r} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    body = response.json()
    return body.get("data", body) if isinstance(body.get("data"), dict) else body


def reference_of(body: dict) -> str:
    for key in ("reference", "order_reference", "id"):
        value = body.get(key)
        if value:
            return str(value)
    raise AssertionError(f"created order carries no reference field: {str(body)[:300]}")


def add_step(client_, reference: str, element_key: str, action: str):
    return client_.post(
        f"/v1/switching-orders/{reference}/steps",
        json={"element_stable_key": element_key, "action": action},
    )


def step_id_of(body: dict):
    for key in ("id", "step_id"):
        if body.get(key) is not None:
            return body[key]
    raise AssertionError(f"created step carries no id field: {str(body)[:300]}")


def run_study(client_, reference: str):
    return client_.post(f"/v1/switching-orders/{reference}/study", json={})


def submit(client_, reference: str):
    return client_.post(f"/v1/switching-orders/{reference}/submit", json={})


def approve(client_, reference: str, approved_hash: str | None = None):
    payload: dict = {"comment": "reviewed"}
    if approved_hash is not None:
        payload["approved_hash"] = approved_hash
    return client_.post(f"/v1/switching-orders/{reference}/approve", json=payload)


def confirm_token(client_, reference: str, step_id) -> str:
    response = client_.post(
        f"/v1/switching-orders/{reference}/steps/{step_id}/confirm-token", json={}
    )
    assert response.status_code in CREATED, (
        f"minting a confirmation token for step {step_id} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    body = body.get("data", body) if isinstance(body.get("data"), dict) else body
    value = body.get("confirm_token")
    assert value, f"no confirm_token in the mint response: {response.text[:400]}"
    return str(value)


def execute_step(client_, reference: str, step_id, token: str | None):
    payload = {"confirm_token": token} if token is not None else {}
    return client_.post(
        f"/v1/switching-orders/{reference}/steps/{step_id}/execute", json=payload
    )


def approved_hash_of(body: dict) -> str:
    for key in ("step_sequence_hash", "approved_hash"):
        value = body.get(key)
        if value:
            return str(value)
    raise AssertionError(f"order carries no step sequence digest: {str(body)[:300]}")


def alarm_list(client_) -> list[dict]:
    response = client_.get("/v1/alarms", params={"state": "active"})
    assert response.status_code == 200, (
        f"GET /api/v1/alarms returned {response.status_code}: {response.text[:400]}"
    )
    return items(response.json())


def seeded_alarm(client_) -> dict:
    for alarm in alarm_list(client_):
        if RECLOSER_KEY in str(alarm):
            return alarm
    raise AssertionError(
        f"no active alarm names {RECLOSER_KEY!r}, so the seed never ran or the alarm "
        f"is not listed"
    )


def alarm_id_of(body: dict):
    for key in ("id", "alarm_id"):
        if body.get(key) is not None:
            return body[key]
    raise AssertionError(f"alarm carries no id field: {str(body)[:300]}")


def poll_until(check, budget: float = POLL_BUDGET_SECONDS):
    """Bounded poll to a monotonic deadline. Returns the first truthy result."""
    stop = deadline(budget)
    last = None
    while time.monotonic() < stop:
        last = check()
        if last:
            return last
        settle()
    return last
