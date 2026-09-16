from __future__ import annotations

import os
import time

import httpx
import pytest
from appclient import api_base, app_url, client, login, seeded_password
from capabilities import Backend, make_backend

OWNER_EMAIL = "owner@example.com"
APPROVER_EMAIL = "approver@example.com"
APPROVER2_EMAIL = "approver2@example.com"
OPERATOR_EMAIL = "operator@example.com"
OPERATOR2_EMAIL = "operator2@example.com"

CORPUS_PASSWORD = "deku-demo-pw-2026"

PLATFORM_OPS = "platform-ops"
REVENUE_OPS = "revenue-ops"

INCIDENT_TRIAGE = "Incident triage"
NIGHTLY_BACKUP = "Nightly backup sweep"
LEAD_HANDOFF = "Lead handoff"

APPROVAL_STEP = "Wait for approval"
SEEDED_STEPS = ("Webhook trigger", "Fetch incident", "Classify impact",
                "Wait for approval", "Post to channel")

RUN_STATUSES = ("new", "running", "waiting", "succeeded", "failed",
                "cancelled", "crashed")

SETTLE_SECONDS = 1.0
POLL_BUDGET_SECONDS = 45.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    time.sleep(seconds)


def deadline_budget() -> float:
    configured = float(os.environ.get("APPROVAL_DEADLINE_SEC", "6"))
    return (2 * configured) + SETTLE_SECONDS + 5.0


def poll_until(predicate, budget: float = POLL_BUDGET_SECONDS):
    end = time.monotonic() + budget
    last = None
    while time.monotonic() < end:
        last = predicate()
        if last:
            return last
        settle(0.5)
    return last


def unique_ref(prefix: str = "probe") -> str:
    return f"{prefix}-{os.urandom(6).hex()}"


def unique_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


def authed(email: str) -> httpx.Client:
    token = login(email, seeded_password("SEED_PASSWORD", CORPUS_PASSWORD))
    return client(token)


@pytest.fixture
def anon_client():
    with client() as c:
        yield c


@pytest.fixture
def owner_client():
    with authed(OWNER_EMAIL) as c:
        yield c


@pytest.fixture
def approver_client():
    with authed(APPROVER_EMAIL) as c:
        yield c


@pytest.fixture
def approver2_client():
    with authed(APPROVER2_EMAIL) as c:
        yield c


@pytest.fixture
def operator_client():
    with authed(OPERATOR_EMAIL) as c:
        yield c


@pytest.fixture
def operator2_client():
    with authed(OPERATOR2_EMAIL) as c:
        yield c


class FlowmarkStore:
    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def user_by_email(self, email: str) -> dict | None:
        return self._b.one("users", email=email)

    def project_by_slug(self, slug: str) -> dict | None:
        return self._b.one("projects", slug=slug)

    def workflow_by_name(self, name: str) -> dict | None:
        return self._b.one("workflows", name=name)

    def count_workflows(self, **where) -> int:
        return self._b.count("workflows", **where)

    def versions_of(self, workflow_id) -> list[dict]:
        return self._b.rows("workflow_versions", workflow_id=workflow_id)

    def run_by_id(self, run_id) -> dict | None:
        return self._b.one("runs", id=run_id)

    def count_runs(self, **where) -> int:
        return self._b.count("runs", **where)

    def runs_with_status(self, status: str) -> list[dict]:
        return self._b.rows("runs", status=status)

    def steps_of_run(self, run_id) -> list[dict]:
        return self._b.rows("run_steps", run_id=run_id)

    def approvals_of_run(self, run_id) -> list[dict]:
        return self._b.rows("approvals", run_id=run_id)

    def annotations_of_run(self, run_id) -> list[dict]:
        return self._b.rows("run_annotations", run_id=run_id)

    def logs_of_run(self, run_id) -> list[dict]:
        return self._b.rows("run_logs", run_id=run_id)

    def count_audit(self, **where) -> int:
        return self._b.count("audit_events", **where)

    def count_connectors(self, **where) -> int:
        return self._b.count("connectors", **where)

    def count_contact_requests(self, **where) -> int:
        return self._b.count("contact_requests", **where)

    def contact_request_by_email(self, email: str) -> dict | None:
        return self._b.one("contact_requests", email=email)

    def count_plans(self) -> int:
        return self._b.count("plans")


@pytest.fixture
def db() -> FlowmarkStore:
    return FlowmarkStore(make_backend())


def api(path: str) -> str:
    return f"{api_base()}{path}"


def page(path: str) -> str:
    return f"{app_url()}{path}"


def fetch(path: str, **kwargs) -> httpx.Response:
    return httpx.get(page(path), timeout=30.0, follow_redirects=True, **kwargs)


def fresh_waiting_run(starter_client, reader_client, project_slug: str = PLATFORM_OPS):
    """Start a run, park it at the approval step, and return its approval row.

    Every test that needs a run at `waiting` makes its own. The browser pass runs
    before the pytest pass and approves the seeded waiting run, so a test that
    reads the seeded queue is asserting a pre-state another channel has already
    consumed (reference/E E.6, reference/J J.12).
    """
    workflow_id = workflow_id_by_name(starter_client, project_slug, INCIDENT_TRIAGE)
    run_id = start_run(starter_client, workflow_id).get("id")

    def parked():
        response = reader_client.get(f"/projects/{project_slug}/approvals")
        if response.status_code != 200:
            return None
        for row in response.json():
            if row.get("run_id") == run_id and row.get("decision") == "pending":
                return row
        return None

    row = poll_until(parked)
    assert row is not None, (
        f"run {run_id} of {INCIDENT_TRIAGE!r} never appeared in the "
        f"{project_slug} approvals queue at decision 'pending'; the step "
        f"{APPROVAL_STEP!r} parks a run for a person to decide")
    return row


def start_run(client_, workflow_id, mode: str = "manual") -> dict:
    response = client_.post(f"/workflows/{workflow_id}/runs", json={"mode": mode})
    assert response.status_code in (200, 201), (
        f"POST /api/workflows/{workflow_id}/runs returned {response.status_code}: "
        f"{response.text[:400]}")
    return response.json()


def workflow_id_by_name(client_, project_slug: str, name: str):
    response = client_.get(f"/projects/{project_slug}/workflows")
    assert response.status_code == 200, (
        f"GET /api/projects/{project_slug}/workflows returned "
        f"{response.status_code}: {response.text[:400]}")
    rows = response.json()
    assert isinstance(rows, list), (
        f"GET /api/projects/{project_slug}/workflows must return a top-level JSON "
        f"array, got {type(rows).__name__}: {response.text[:400]}")
    for row in rows:
        if row.get("name") == name:
            return row.get("id")
    raise AssertionError(
        f"no workflow named {name!r} in project {project_slug!r}; the seed data "
        f"pins it. Saw: {[r.get('name') for r in rows]}")


def contact_payload(email: str, **overrides) -> dict:
    body = {
        "email": email,
        "first_name": "Probe",
        "company": "Probe Industries",
        "message": "A verifier probe.",
        "consent": True,
        "campaign_source": "probe-source",
        "campaign_medium": "probe-medium",
        "campaign_name": "probe-campaign",
        "referrer": "https://example.com/probe",
    }
    body.update(overrides)
    return body


CODE_STEP_REACH_HOST = "return [{'json': {'leak': str(process.env)}}]"
CODE_STEP_SPIN = "while (true) { }"
CODE_STEP_MUTATE = "items[0].json.touched = true; return items;"
INTERNAL_URLS = ("http://127.0.0.1:9/", "http://localhost:9/", "http://169.254.169.254/")


def save_probe_workflow(owner_or_operator_client, project_slug, name, steps,
                        connections=None):
    """Create a workflow and save one version of it, returning its id.

    Each probe builds its own workflow rather than editing a seeded one, so no
    probe can leave another probe a graph it did not expect.
    """
    created = owner_or_operator_client.post(
        f"/projects/{project_slug}/workflows", json={"name": name})
    assert created.status_code in (200, 201), (
        f"POST /api/projects/{project_slug}/workflows returned "
        f"{created.status_code}: {created.text[:400]}")
    workflow_id = created.json().get("id")
    assert workflow_id is not None, (
        f"the created workflow carries no id: {created.text[:400]}")

    saved = owner_or_operator_client.post(
        f"/workflows/{workflow_id}/versions",
        json={"message": "verifier probe", "steps": steps,
              "connections": connections or []})
    assert saved.status_code in (200, 201), (
        f"POST /api/workflows/{workflow_id}/versions returned "
        f"{saved.status_code}: {saved.text[:400]}")
    return workflow_id


def step_row(name, step_type="regular", parameters=None, on_error="continue",
             position_x=100, position_y=100):
    return {"name": name, "step_type": step_type, "parameters": parameters or {},
            "position_x": position_x, "position_y": position_y,
            "on_error": on_error, "disabled": False}


def run_to_rest(db, run_id, budget=POLL_BUDGET_SECONDS):
    """Poll until the run stops moving, then return it."""
    def settled():
        row = db.run_by_id(run_id)
        if row and row.get("status") in ("succeeded", "failed", "cancelled",
                                         "crashed", "waiting"):
            return row
        return None
    return poll_until(settled, budget=budget)


def failed_step(db, run_id, step_name):
    for row in db.steps_of_run(run_id):
        if row.get("step_name") == step_name and row.get("status") == "failed":
            return row
    return None
