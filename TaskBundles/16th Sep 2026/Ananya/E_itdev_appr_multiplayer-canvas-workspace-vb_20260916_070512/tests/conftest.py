from __future__ import annotations

import os
import time
from typing import Any

import httpx
import pytest

import appclient
import capabilities

PASSWORD = appclient.seeded_password("DEKU_SEEDED_PASSWORD", "deku-demo-pw-2026")

EDITOR = "editor@example.com"
SECOND_EDITOR = "editor2@example.com"
IN_TEAM_REVIEWER = "reviewer@example.com"
PEER_TEAM_REVIEWER = "reviewer2@example.com"
ADMINISTRATOR = "org_admin@example.com"

ORGANIZATION = "Harborlight"
FIRST_TEAM = "Atlas"
SECOND_TEAM = "Beacon"
FIRST_PROJECT = "Atlas Mobile"
SECOND_PROJECT = "Beacon Web"
DESIGN_FILE = "Checkout Redesign"
LIBRARY_FILE = "Atlas Core Kit"
PEER_TEAM_FILE = "Beacon Landing"
FIRST_FRAME = "Payment Step"
SECOND_FRAME = "Confirmation"
LIBRARY_NAME = "Atlas Core"
FIRST_COMPONENT = "Primary Action"
SECOND_COMPONENT = "Field Label"
BRANCH_NAME = "Compact Payment Step"

REVIEW_REQUESTED_SUBJECT = "Review requested: "
REVIEW_APPROVED_SUBJECT = "Review approved: "
BRANCH_MERGED_SUBJECT = "Branch merged: "

DECOY_FIELD = "company_website"
AUDIT_ACTIONS = frozenset({
    "sign_in", "sign_in_failed", "member_invited", "member_role_changed",
    "member_seat_changed", "member_deactivated", "grant_granted", "grant_revoked",
    "file_created", "file_opened", "file_renamed", "file_trashed",
    "admin_content_access", "library_published", "library_subscription_changed",
    "review_requested", "review_approved", "review_changes_requested",
    "approval_invalidated", "review_withdrawn", "branch_merged",
    "identity_policy_changed", "audit_exported",
})
AUTH_REALM = "deku"
AUTH_CLIENT = "kanvo-app"

DENIED = (401, 403, 404)
REFUSED = (400, 409, 422)
CREATED = (200, 201)

SETTLE_SECONDS = 0.4
POLL_ATTEMPTS = 40


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned pause. Async side effects are polled, never slept over."""
    time.sleep(seconds)


def unique(prefix: str) -> str:
    return f"{prefix}-{os.urandom(6).hex()}"


def body(response: httpx.Response, limit: int = 300) -> str:
    return response.text[:limit]


def ok(response: httpx.Response, what: str) -> Any:
    assert response.status_code in CREATED, (
        f"{what}: {response.request.method} {response.request.url} returned "
        f"{response.status_code}, expected 200 or 201. Body: {body(response)}"
    )
    return response.json()


def token_for(email: str) -> str:
    return appclient.login(email, PASSWORD)


def api_for(email: str) -> httpx.Client:
    return appclient.client(token_for(email))


@pytest.fixture
def backend() -> capabilities.Backend:
    return capabilities.make_backend()


@pytest.fixture
def inbox() -> capabilities.Inbox:
    return capabilities.make_inbox()


@pytest.fixture
def editor() -> httpx.Client:
    with api_for(EDITOR) as cl:
        yield cl


@pytest.fixture
def second_editor() -> httpx.Client:
    with api_for(SECOND_EDITOR) as cl:
        yield cl


@pytest.fixture
def reviewer() -> httpx.Client:
    with api_for(IN_TEAM_REVIEWER) as cl:
        yield cl


@pytest.fixture
def peer_reviewer() -> httpx.Client:
    with api_for(PEER_TEAM_REVIEWER) as cl:
        yield cl


@pytest.fixture
def administrator() -> httpx.Client:
    with api_for(ADMINISTRATOR) as cl:
        yield cl


@pytest.fixture
def anonymous() -> httpx.Client:
    with appclient.client() as cl:
        yield cl


def teams(cl: httpx.Client) -> list[dict]:
    return ok(cl.get("/teams"), "reading the team list")


def team_id(cl: httpx.Client, name: str) -> Any:
    for row in teams(cl):
        if row.get("name") == name:
            return row["id"]
    raise AssertionError(
        f"the seeded team {name!r} is absent from GET /api/teams, which returned "
        f"{[r.get('name') for r in teams(cl)]!r}"
    )


def project_id(cl: httpx.Client, team: Any, name: str) -> Any:
    rows = ok(cl.get(f"/teams/{team}/projects"), "reading the project list")
    for row in rows:
        if row.get("name") == name:
            return row["id"]
    raise AssertionError(
        f"the seeded project {name!r} is absent from the project list for team "
        f"{team!r}, which returned {[r.get('name') for r in rows]!r}"
    )


def file_id(cl: httpx.Client, project: Any, name: str) -> Any:
    rows = ok(cl.get(f"/projects/{project}/files"), "reading the file list")
    for row in rows:
        if row.get("name") == name:
            return row["id"]
    raise AssertionError(
        f"the seeded file {name!r} is absent from GET /api/projects/{project}/files, "
        f"which returned {[r.get('name') for r in rows]!r}"
    )


def design_file_id(cl: httpx.Client) -> Any:
    return file_id(cl, project_id(cl, team_id(cl, FIRST_TEAM), FIRST_PROJECT), DESIGN_FILE)


def library_file_id(cl: httpx.Client) -> Any:
    return file_id(cl, project_id(cl, team_id(cl, FIRST_TEAM), FIRST_PROJECT), LIBRARY_FILE)


def frames(cl: httpx.Client, file: Any) -> list[dict]:
    return ok(cl.get(f"/files/{file}/frames"), f"reading the frames of file {file!r}")


def frame_named(cl: httpx.Client, file: Any, name: str) -> dict:
    for row in frames(cl, file):
        if row.get("name") == name:
            return row
    raise AssertionError(
        f"the frame {name!r} is absent from file {file!r}, whose frames are "
        f"{[r.get('name') for r in frames(cl, file)]!r}"
    )


def add_frame(cl: httpx.Client, file: Any, name: str, **extra: Any) -> dict:
    payload = {"name": name, "parent_id": None, "after_frame_id": None,
               "x": 0, "y": 0, "width": 200, "height": 120}
    payload.update(extra)
    return ok(cl.post(f"/files/{file}/frames", json=payload),
              f"adding the frame {name!r} to file {file!r}")


def open_branch(cl: httpx.Client, file: Any, name: str) -> dict:
    return ok(cl.post(f"/files/{file}/branches", json={"name": name}),
              f"opening a branch on file {file!r}")


def read_branch(cl: httpx.Client, branch: Any) -> dict:
    return ok(cl.get(f"/branches/{branch}"), f"reading branch {branch!r}")


def push_branch(cl: httpx.Client, branch: Any, label: str) -> dict:
    payload = {"frames": [{"name": label, "x": 40, "y": 40, "width": 200, "height": 120}]}
    return ok(cl.post(f"/branches/{branch}/versions", json=payload),
              f"storing a new version on branch {branch!r}")


def request_review(cl: httpx.Client, branch: Any, reviewer_email: str) -> dict:
    return ok(cl.post(f"/branches/{branch}/review-requests",
                      json={"reviewer_email": reviewer_email}),
              f"requesting review on branch {branch!r}")


def decide(cl: httpx.Client, branch: Any, decision: str, comment: str = "") -> httpx.Response:
    return cl.post(f"/branches/{branch}/decisions",
                   json={"decision": decision, "comment": comment})


def approve(cl: httpx.Client, branch: Any) -> dict:
    return ok(decide(cl, branch, "approved", "looks right"),
              f"approving branch {branch!r}")


def merge(cl: httpx.Client, branch: Any) -> httpx.Response:
    return cl.post(f"/branches/{branch}/merge")


def reviewed_branch(owner: httpx.Client, judge: httpx.Client, name: str) -> dict:
    """A branch on the seeded design file, pushed once and out for review."""
    source = design_file_id(owner)
    branch = open_branch(owner, source, name)
    push_branch(owner, branch["id"], unique("frame"))
    request_review(owner, branch["id"], IN_TEAM_REVIEWER)
    return {"source_file_id": source, "branch": branch}


def merge_versions(cl: httpx.Client, file: Any) -> list[dict]:
    rows = ok(cl.get(f"/files/{file}/versions"), f"reading the versions of file {file!r}")
    return [r for r in rows if r.get("kind") == "merge"]


def mails(inbox, to: str, needle: str) -> list:
    """Every delivered message to one recipient whose subject names `needle`.

    Counting by subject keeps a late message from an earlier check out of this one.
    """
    listing = getattr(inbox, "_messages", None)
    assert listing is not None, "the mail capability exposes no message listing"
    return [m for m in listing() if to in m.to and needle in m.subject]


def poll(read, predicate, what: str, attempts: int = POLL_ATTEMPTS):
    """Bounded polling for an async side effect. Never a retry loop that hides failure."""
    last = None
    for _ in range(attempts):
        last = read()
        if predicate(last):
            return last
        settle()
    raise AssertionError(
        f"{what}: the condition was still unmet after {attempts} bounded polls. "
        f"Last observation: {str(last)[:300]}"
    )
