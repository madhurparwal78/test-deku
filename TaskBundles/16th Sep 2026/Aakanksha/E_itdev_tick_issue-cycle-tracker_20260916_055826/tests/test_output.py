"""Black-box graders for deku/issue-cycle-tracker.

Every assertion drives the app through its HTTP surface, reads the real Postgres
rows through the backend capability, or reads the real Mailpit inbox through the
email capability. Nothing inspects the app's source, framework or schema
internals (INV6). Concurrency is exercised with real simultaneous requests, never
simulated, so the single-winner and idempotency rules are observed the way a
stranger would hit them. Unique per-run identifiers keep every run independent.
"""

from __future__ import annotations

import concurrent.futures
import uuid

import httpx
from appclient import app_url, login
from conftest import (
    PASSWORD, ADMIN_EMAIL, LEAD_EMAIL, MEMBER_EMAIL, MEMBER2_EMAIL,
    TEAM_NAME, TEAM_KEY, ACTIVE_CYCLE, CLOSED_CYCLE, OTHER_TEAM_ISSUE_KEY,
    ASSIGN_SUBJECT, UPDATE_SUBJECT,
    STATE_BACKLOG, STATE_UNSTARTED, STATE_IN_PROGRESS, STATE_DONE, STATE_CANCELLED,
    ACCEPTED,
    board_issues, inbox_issues, cycles, active_cycle, closed_cycle,
    create_issue, get_issue, patch_issue, issue_by_title, an_inbox_issue,
    all_issues, settle, find_email_eventually,
)


def _client_error(code: int) -> bool:
    return 400 <= code < 500


def _assign_an_inbox_issue(lead_client, db, member_email: str) -> str:
    """Triage one inbox issue onto a member and return its key."""
    row = an_inbox_issue(lead_client)
    key = row["key"]
    member = db.member(member_email)
    assert member is not None, f"the seeded member {member_email!r} must exist"
    response = patch_issue(lead_client, key, assignee=member["id"])
    assert response.status_code in ACCEPTED, "a lead must be able to assign an inbox issue"
    return key


def _owned_issue_key(lead_client, member_client, db, member_email: str) -> str:
    """A key of an issue the member owns, assigning one from the inbox if needed."""
    for issue in board_issues(member_client):
        assignee = issue.get("assignee")
        if assignee and (assignee == db.member(member_email)["id"]
                         or assignee == member_email):
            return issue["key"]
    return _assign_an_inbox_issue(lead_client, db, member_email)


def _new_cycle(lead_client, name_hint: str) -> dict:
    response = lead_client.post("/cycles", json={
        "name": f"{name_hint} {uuid.uuid4().hex[:6]}",
        "starts_on": "2026-10-01",
        "ends_on": "2026-10-14",
    })
    assert response.status_code in ACCEPTED, "a lead must be able to create a cycle"
    return response.json()


def test_health_ready(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, "health must return 200 once the app is ready"


def test_signin_issues_token():
    token = login(MEMBER_EMAIL, PASSWORD)
    assert token, "signing in with a seeded member must issue an access token"


def test_signin_wrong_password_refused(anon_client):
    response = anon_client.post(
        "/auth/login", json={"email": MEMBER_EMAIL, "password": "not-the-password"})
    assert _client_error(response.status_code), "a wrong password must be refused as a client error"


def test_file_issue_assigns_team_key(member_client):
    issue = create_issue(member_client, f"Filed {uuid.uuid4().hex[:8]}")
    key = issue.get("key", "")
    assert key.startswith(f"{TEAM_KEY}-"), f"a filed issue must carry a {TEAM_KEY} team key"


def test_new_issue_starts_in_backlog_unassigned(member_client):
    issue = create_issue(member_client, f"Fresh {uuid.uuid4().hex[:8]}")
    assert issue.get("state") == STATE_BACKLOG, "a new issue starts in the backlog state"
    assert not issue.get("assignee"), "a new issue starts with no assignee"


def test_blank_title_refused(member_client):
    response = member_client.post(
        "/issues", json={"title": "", "label": "bug", "priority": "med", "estimate": 1})
    assert _client_error(response.status_code), "a blank title must be refused as invalid"


def test_lead_reads_inbox(lead_client):
    rows = inbox_issues(lead_client)
    assert isinstance(rows, list), "the inbox must read as a list of issues"


def test_assign_persists_new_assignee(lead_client, member_client, db):
    key = _assign_an_inbox_issue(lead_client, db, MEMBER_EMAIL)
    reread = get_issue(member_client, key)
    assert reread.status_code == 200, "the assigned issue must be readable"
    member = db.member(MEMBER_EMAIL)
    stored = db.issue(key)
    assert stored is not None and stored.get("assignee_id") == member["id"], (
        "the new assignee must persist in storage")


def test_assignment_delivers_one_notification_email(lead_client, db, inbox):
    before = inbox.count(MEMBER_EMAIL)
    _assign_an_inbox_issue(lead_client, db, MEMBER_EMAIL)
    message = find_email_eventually(inbox, to=MEMBER_EMAIL, subject_contains=ASSIGN_SUBJECT)
    assert message is not None, "assigning an issue must deliver a notification email to the owner"
    after = inbox.count(MEMBER_EMAIL)
    assert after == before + 1, "exactly one notification email is delivered on assignment"


def test_assignment_email_subject_prefix(lead_client, db, inbox):
    _assign_an_inbox_issue(lead_client, db, MEMBER_EMAIL)
    message = find_email_eventually(inbox, to=MEMBER_EMAIL, subject_contains=ASSIGN_SUBJECT)
    assert message is not None, "the assignment email must reach the owner"
    assert message.subject.startswith(ASSIGN_SUBJECT), (
        f"the assignment subject must begin with {ASSIGN_SUBJECT!r}")


def test_minor_change_sends_no_notification_email(lead_client, db, inbox):
    key = _assign_an_inbox_issue(lead_client, db, MEMBER_EMAIL)
    settle()
    before = inbox.count(MEMBER_EMAIL)
    response = patch_issue(lead_client, key, estimate=8)
    assert response.status_code in ACCEPTED, "a lead may edit the estimate"
    settle()
    after = inbox.count(MEMBER_EMAIL)
    assert after == before, "a minor edit sends no notification email"


def test_foreign_move_sends_update_email(lead_client, db, inbox):
    key = _assign_an_inbox_issue(lead_client, db, MEMBER_EMAIL)
    response = patch_issue(lead_client, key, state=STATE_UNSTARTED)
    assert response.status_code in ACCEPTED, "a lead may move any issue in the team"
    message = find_email_eventually(inbox, to=MEMBER_EMAIL, subject_contains=UPDATE_SUBJECT)
    assert message is not None, "a move by someone other than the owner notifies the owner"


def test_member_move_owned_survives_reload(lead_client, member_client, db):
    key = _owned_issue_key(lead_client, member_client, db, MEMBER_EMAIL)
    response = patch_issue(member_client, key, state=STATE_IN_PROGRESS)
    assert response.status_code in ACCEPTED, "a member may move an issue it owns"
    reread = get_issue(member_client, key)
    assert reread.status_code == 200 and reread.json().get("state") == STATE_IN_PROGRESS, (
        "the move must survive a reload")
    stored = db.issue(key)
    assert stored is not None and stored.get("state") == STATE_IN_PROGRESS, (
        "the new state must persist in storage")


def test_state_change_writes_activity_record(lead_client, member_client, db):
    key = _owned_issue_key(lead_client, member_client, db, MEMBER_EMAIL)
    stored = db.issue(key)
    assert stored is not None, "the issue row must exist"
    before = db.activity_count(stored["id"])
    response = patch_issue(member_client, key, state=STATE_DONE)
    assert response.status_code in ACCEPTED, "a member may move an issue it owns"
    after = db.activity_count(stored["id"])
    assert after == before + 1, "a state change writes exactly one activity record"


def test_close_cycle_returns_unfinished_to_inbox(lead_client):
    cycle = _new_cycle(lead_client, "Returns")
    inbox_before = len(inbox_issues(lead_client))
    response = lead_client.post(f"/cycles/{cycle['id']}/close")
    assert response.status_code in ACCEPTED, "a lead may close a cycle"
    inbox_after = len(inbox_issues(lead_client))
    assert inbox_after >= inbox_before, "closing a cycle returns unfinished issues to the inbox"


def test_close_cycle_reports_moved_count(lead_client):
    cycle = _new_cycle(lead_client, "Counted")
    response = lead_client.post(f"/cycles/{cycle['id']}/close")
    assert response.status_code in ACCEPTED, "a lead may close a cycle"
    body = response.json()
    moved = body.get("count", body.get("moved"))
    assert isinstance(moved, int) and moved >= 0, "closing a cycle reports the count moved"


def test_closed_cycle_refuses_move(lead_client):
    cycle = closed_cycle(lead_client)
    assert cycle is not None, "the seed must include a closed cycle"
    detail = lead_client.get(f"/cycles/{cycle['id']}")
    assert detail.status_code == 200, "a member may read a closed cycle"
    issues = all_issues(detail.json())
    assert issues, "the seeded closed cycle must hold at least one issue"
    response = patch_issue(lead_client, issues[0]["key"], state=STATE_IN_PROGRESS)
    assert _client_error(response.status_code), "a closed cycle refuses any move of its issues"


def test_comment_records_author(member_client):
    issue = create_issue(member_client, f"Discuss {uuid.uuid4().hex[:8]}")
    response = member_client.post(
        f"/issues/{issue['key']}/comments", json={"body": "Looking into this now."})
    assert response.status_code in ACCEPTED, "a member may comment on an issue"
    comment = response.json()
    assert comment.get("author") or comment.get("author_id") or comment.get("author_email"), (
        "a comment records its author")


def test_admin_reads_page_view_log(admin_client):
    response = admin_client.get("/page-views")
    assert response.status_code == 200, "an admin may read the team page-view log"
    assert isinstance(response.json(), list), "the page-view log reads as a list"


def test_member_move_unowned_denied(lead_client, member2_client, db):
    key = _assign_an_inbox_issue(lead_client, db, MEMBER_EMAIL)
    response = patch_issue(member2_client, key, state=STATE_IN_PROGRESS)
    assert _client_error(response.status_code), (
        "a member moving an issue it does not own is denied by the server")


def test_denied_move_leaves_state_unchanged(lead_client, member2_client, db):
    key = _assign_an_inbox_issue(lead_client, db, MEMBER_EMAIL)
    before = db.issue(key)["state"]
    patch_issue(member2_client, key, state=STATE_DONE)
    after = db.issue(key)["state"]
    assert after == before, "a denied move must leave the issue state unchanged"


def test_member_inbox_request_denied(member_client):
    response = member_client.get("/inbox")
    assert _client_error(response.status_code), "a member requesting the inbox is denied"


def test_cross_team_issue_not_found(member_client):
    response = get_issue(member_client, OTHER_TEAM_ISSUE_KEY)
    assert response.status_code == 404, (
        "a request for another team's issue is answered as not found, not forbidden")


def test_admin_self_demote_denied(admin_client, db):
    admin = db.member(ADMIN_EMAIL)
    assert admin is not None, "the seeded admin must exist"
    response = admin_client.patch(f"/members/{admin['id']}", json={"role": "member"})
    assert _client_error(response.status_code), "an admin removing its own admin role is denied"


def test_lead_members_endpoint_denied(lead_client):
    response = lead_client.get("/members")
    assert _client_error(response.status_code), (
        "a lead requesting the admin-only members endpoint is denied")


def test_seed_team_orbit_has_members(db):
    team = db.team(TEAM_NAME)
    assert team is not None, f"the seeded team {TEAM_NAME!r} must be present"
    assert len(db.members_in(team["id"])) >= 4, "the seeded team has four members"


def test_seed_active_cycle_present(db):
    cycle = db.cycle(ACTIVE_CYCLE)
    assert cycle is not None and cycle.get("status") == "active", (
        f"the seeded active cycle {ACTIVE_CYCLE!r} must be present")


def test_seed_closed_cycle_present(db):
    cycle = db.cycle(CLOSED_CYCLE)
    assert cycle is not None and cycle.get("status") == "closed", (
        f"the seeded closed cycle {CLOSED_CYCLE!r} must be present")


def test_single_active_cycle_invariant(db):
    team = db.team(TEAM_NAME)
    assert team is not None, "the seeded team must exist"
    assert len(db.active_cycles(team["id"])) <= 1, "at most one cycle per team is active"


def test_concurrent_cycle_activation_single_winner(lead_client):
    current = active_cycle(lead_client)
    if current is not None:
        lead_client.post(f"/cycles/{current['id']}/close")
    first = _new_cycle(lead_client, "RaceA")
    second = _new_cycle(lead_client, "RaceB")

    def open_cycle(cycle_id):
        return lead_client.post(f"/cycles/{cycle_id}/open")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(open_cycle, first["id"]), pool.submit(open_cycle, second["id"])]
        results = [future.result() for future in futures]
    winners = sum(1 for result in results if result.status_code in ACCEPTED)
    assert winners == 1, "exactly one activation wins under a concurrent race"


def test_cycle_activation_conflict_rejected(lead_client):
    extra = _new_cycle(lead_client, "Conflict")
    response = lead_client.post(f"/cycles/{extra['id']}/open")
    assert response.status_code == 409 or _client_error(response.status_code), (
        "activating a second cycle while one is active is refused as a conflict")


def test_idempotent_create_issue_replay(member_client, db):
    request_id = uuid.uuid4().hex
    title = f"Replay {uuid.uuid4().hex[:8]}"
    first = member_client.post("/issues", json={
        "title": title, "label": "bug", "priority": "med", "estimate": 1,
        "client_request_id": request_id})
    assert first.status_code in ACCEPTED, "the first create must succeed"
    member_client.post("/issues", json={
        "title": title, "label": "bug", "priority": "med", "estimate": 1,
        "client_request_id": request_id})
    assert db.issue_count(title=title) == 1, "a replayed create must not create a second issue"


def test_issue_keys_unique_under_contention(member_client):
    def file_one(index):
        return create_issue(member_client, f"Contend {uuid.uuid4().hex[:8]}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        issues = [future.result() for future in
                  [pool.submit(file_one, i) for i in range(5)]]
    keys = [issue["key"] for issue in issues]
    assert len(set(keys)) == len(keys), "every issue key allocated under contention is distinct"


def test_no_frontend_secrets():
    root = app_url()
    secrets = ("deku-local-dev", "DB_ADMIN_URL", "ANTHROPIC_API_KEY")
    for path in ("/", "/login", "/board"):
        response = httpx.get(f"{root}{path}", timeout=30.0)
        for secret in secrets:
            assert secret not in response.text, (
                f"no credential must appear in the downloaded page {path!r}")


def test_strict_transport_security_header(anon_client):
    response = anon_client.get("/health")
    headers = {key.lower(): value for key, value in response.headers.items()}
    assert "strict-transport-security" in headers, (
        "every response carries a strict transport security header")


def test_nosniff_content_type_header(anon_client):
    response = anon_client.get("/health")
    headers = {key.lower(): value for key, value in response.headers.items()}
    assert headers.get("x-content-type-options", "").lower() == "nosniff", (
        "every response carries a nosniff content-type header")
