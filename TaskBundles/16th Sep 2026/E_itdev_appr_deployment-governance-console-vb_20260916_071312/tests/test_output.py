"""The one pytest module for the Meridian deployment governance console.

Every assertion is black-box: HTTP against the running app, plus reads of the
relational store through the capability adapter to prove a fact really landed
there rather than only in a response body.
"""

from __future__ import annotations

import concurrent.futures
import json
import os

import httpx

from _shapes import flatten, items
from conftest import (ACCEPTED, DENIED, DEPLOYMENT_STATES, DEVELOPER_EMAIL,
                      ELIGIBLE_GROUP, FIREWALL_ACTIONS, FOREIGN_DEVELOPER_EMAIL,
                      FOREIGN_PROJECT_SLUG, FOREIGN_TEAM_SLUG, HOBBY_PRICE_CENTS,
                      LIVE_COMMIT, PLAN_CUSTOM_RULE_CAPS, POLICY_NAME,
                      POLICY_VERSION, PRODUCTION_ALIAS_HOST, PROJECT_SLUG,
                      PRO_PRICE_CENTS, PUBLIC_ROUTES, READY_COMMIT, REFUSED,
                      REQUEST_STATES, REQUIRED_APPROVALS, RESERVED_SLUGS,
                      REVIEWER2_EMAIL, REVIEWER_EMAIL, SEEDED_FIREWALL_RULES,
                      SPEND_CAP_ACTIONS, SUPERSEDED_COMMIT, TEAM_SLUG,
                      settle, unique_suffix)

TIMEOUT = 30.0


def _why(response, note: str) -> str:
    return (f"{note}: {response.request.method} {response.request.url} returned "
            f"{response.status_code}; body starts {response.text[:300]!r}")


def _open_request(client, commit: str, justification: str):
    deployments = items(_ok(client.get("/deployments", params={"project": PROJECT_SLUG}),
                            "deployment list").json())
    target = [d for d in deployments if str(d.get("git_commit_sha", "")).startswith(commit)]
    assert target, (f"no deployment for commit {commit!r} in "
                    f"{[d.get('git_commit_sha') for d in deployments]}")
    created = client.post("/promotions", json={"deployment_id": target[0]["id"],
                                               "environment": "production",
                                               "justification": justification})
    assert created.status_code in ACCEPTED, _why(created, "opening a promotion request")
    return created.json()


def _ok(response, note: str):
    assert response.status_code in ACCEPTED, _why(response, note)
    return response


def _request_row(client, request_id):
    listed = items(_ok(client.get("/promotions", params={"project": PROJECT_SLUG}),
                       "promotion list").json())
    matching = [r for r in listed if str(r.get("id")) == str(request_id)]
    assert matching, f"promotion request {request_id!r} is absent from the list"
    return matching[0]


def test_health_endpoint_answers_before_any_credential(anon, app_base):
    response = anon.get("/health")
    assert response.status_code == 200, _why(response, "unauthenticated health probe")
    assert response.json(), "health returned an empty body"
    root = httpx.get(app_base + "/", timeout=TIMEOUT, follow_redirects=True)
    assert root.status_code == 200, _why(root, "the application shell at the app root")


def test_seeded_accounts_sign_in_with_the_corpus_password(developer, reviewer,
                                                          reviewer_two, finance,
                                                          viewer, foreign_developer):
    for name, client in (("developer", developer), ("reviewer", reviewer),
                         ("reviewer2", reviewer_two), ("finance", finance),
                         ("viewer", viewer), ("developer2", foreign_developer)):
        response = client.get("/teams")
        assert response.status_code in ACCEPTED, _why(response, f"{name} reading its own teams")


def test_login_with_a_wrong_password_is_refused_like_an_unknown_address(app_base):
    api = app_base + "/api/auth/login"
    wrong = httpx.post(api, json={"email": DEVELOPER_EMAIL, "password": "not-the-seeded-one"},
                       timeout=TIMEOUT)
    unknown = httpx.post(api, json={"email": f"nobody-{unique_suffix()}@example.com",
                                    "password": "not-the-seeded-one"}, timeout=TIMEOUT)
    assert wrong.status_code in DENIED + REFUSED, _why(wrong, "login with a wrong password")
    assert unknown.status_code == wrong.status_code, (
        f"an unknown address returned {unknown.status_code} while a wrong password "
        f"returned {wrong.status_code}; the two refusals must be indistinguishable")
    assert set(wrong.json().keys()) == set(unknown.json().keys()), (
        f"refusal bodies differ in shape: {sorted(wrong.json())} against "
        f"{sorted(unknown.json())}")


def test_protected_collections_require_a_bearer_token(anon):
    for path, params in (("/deployments", {"project": PROJECT_SLUG}),
                         ("/promotions", {"project": PROJECT_SLUG}),
                         ("/audit", {"team": TEAM_SLUG}),
                         ("/spend", {"team": TEAM_SLUG})):
        response = anon.get(path, params=params)
        assert response.status_code in DENIED, _why(
            response, f"anonymous read of {path} must be refused")


def test_no_state_change_is_reachable_by_get(anon, developer):
    probe = developer.get("/promotions/1/approve")
    assert probe.status_code not in ACCEPTED, _why(
        probe, "a GET against the approve address must never act")
    unknown_field = developer.post("/promotions", json={
        "deployment_id": "0", "environment": "production",
        "justification": "field-probe", "not_a_real_field": unique_suffix()})
    assert unknown_field.status_code not in ACCEPTED, _why(
        unknown_field, "a write carrying an unknown field must be refused")


def test_seeded_deployment_rows_are_persisted_with_pinned_states(developer, db):
    listed = items(_ok(developer.get("/deployments", params={"project": PROJECT_SLUG}),
                       "deployment list").json())
    assert isinstance(listed, list) and listed, "the deployment list is empty"
    by_commit = {str(d.get("git_commit_sha", ""))[:7]: d for d in listed}
    for commit, expected in ((READY_COMMIT, "READY"), (LIVE_COMMIT, "LIVE"),
                             (SUPERSEDED_COMMIT, "SUPERSEDED")):
        assert commit in by_commit, f"seeded commit {commit!r} is absent from {sorted(by_commit)}"
        state = by_commit[commit].get("state")
        assert state in DEPLOYMENT_STATES, f"{commit} carries state {state!r}, outside the pinned set"
    stored = db.count("deployments")
    assert stored >= 3, f"the store holds {stored} deployment row(s); the seed declares three"


def test_a_replayed_webhook_delivery_stores_one_deployment_row(developer, db, app_base):
    delivery = f"d-{unique_suffix()}"
    commit = unique_suffix()
    payload = {"delivery_id": delivery, "project": PROJECT_SLUG, "commit": commit,
               "ref": "refs/heads/main", "author": "dana"}
    before = db.count("deployments")
    endpoint = app_base + "/api/webhooks/git"
    first = httpx.post(endpoint, json=payload, timeout=TIMEOUT,
                       headers={"X-Meridian-Signature": os.environ.get("WEBHOOK_SIGNATURE", "seeded"),
                                "X-Meridian-Timestamp": "now"})
    second = httpx.post(endpoint, json=payload, timeout=TIMEOUT,
                        headers={"X-Meridian-Signature": os.environ.get("WEBHOOK_SIGNATURE", "seeded"),
                                 "X-Meridian-Timestamp": "now"})
    assert first.status_code in ACCEPTED + DENIED + REFUSED, _why(first, "first webhook delivery")
    assert second.status_code == first.status_code or second.status_code in ACCEPTED, _why(
        second, "replayed webhook delivery")
    settle(lambda: db.count("deployments") >= before)
    after = db.count("deployments")
    assert after - before <= 1, (
        f"the replayed delivery {delivery!r} added {after - before} deployment rows; "
        f"one delivery identifier must produce exactly one deployment")


def test_a_webhook_without_a_signature_is_refused(app_base, db):
    before = db.count("deployments")
    unsigned = httpx.post(app_base + "/api/webhooks/git", timeout=TIMEOUT,
                          json={"delivery_id": f"d-{unique_suffix()}",
                                "project": PROJECT_SLUG, "commit": unique_suffix(),
                                "ref": "refs/heads/main", "author": "dana"})
    assert unsigned.status_code in DENIED + REFUSED, _why(
        unsigned, "an unsigned webhook delivery must be refused")
    assert db.count("deployments") == before, (
        "an unsigned webhook delivery wrote a deployment row")


def test_the_deployment_list_is_keyset_paginated_newest_first(developer):
    first = _ok(developer.get("/deployments", params={"project": PROJECT_SLUG, "limit": 2}),
                "first deployment page")
    rows = items(first.json())
    assert len(rows) <= 2, f"a limit of two returned {len(rows)} rows"
    body = first.json()
    if isinstance(body, dict):
        assert "nextCursor" in body or "next_cursor" in body, (
            f"a paginated list must return a cursor; keys were {sorted(body)}")
    created = [r.get("created_at") for r in rows if r.get("created_at")]
    assert created == sorted(created, reverse=True), (
        f"the deployment list is not newest first: {created}")


def test_a_failed_build_leaves_the_live_alias_untouched(developer, reviewer):
    before = items(_ok(reviewer.get("/aliases", params={"project": PROJECT_SLUG}),
                       "alias list").json())
    production = [a for a in before if a.get("host") == PRODUCTION_ALIAS_HOST]
    assert production, f"no alias for {PRODUCTION_ALIAS_HOST!r} in {[a.get('host') for a in before]}"
    pointed_at = production[0].get("deployment_id")
    errored = [d for d in items(_ok(developer.get("/deployments", params={"project": PROJECT_SLUG}),
                                    "deployment list").json())
               if d.get("state") == "ERROR"]
    after = items(_ok(reviewer.get("/aliases", params={"project": PROJECT_SLUG}),
                      "alias list after reading errors").json())
    still = [a for a in after if a.get("host") == PRODUCTION_ALIAS_HOST][0]
    assert still.get("deployment_id") == pointed_at, (
        f"the production alias moved from {pointed_at!r} to {still.get('deployment_id')!r} "
        f"with {len(errored)} failed build(s) present and no promotion in between")


def test_a_developer_is_denied_approving_their_own_request_and_the_row_is_untouched(developer, db):
    opened = _open_request(developer, READY_COMMIT, "self approval probe")
    request_id = opened["id"]
    before = _request_row(developer, request_id)
    assert before.get("state") == "OPEN", f"a new request opened in state {before.get('state')!r}"
    assert int(before.get("approvals_gathered", 0)) == 0, (
        f"a new request already carries {before.get('approvals_gathered')} approval(s)")
    assert int(before.get("required_approvals", 0)) == REQUIRED_APPROVALS, (
        f"the request requires {before.get('required_approvals')} approvals; "
        f"the {POLICY_NAME} policy at version {POLICY_VERSION} requires {REQUIRED_APPROVALS}")
    decisions_before = db.count("approval_decisions")

    refused = developer.post(f"/promotions/{request_id}/approve",
                             json={"comment": "approving my own change"})
    assert refused.status_code in DENIED, _why(
        refused, "a requester approving their own request must be denied by the server")

    after = _request_row(developer, request_id)
    assert int(after.get("approvals_gathered", 0)) == 0, (
        f"the denied self-approval moved the gathered count to "
        f"{after.get('approvals_gathered')}; the row must be untouched")
    assert after.get("state") == "OPEN", (
        f"the denied self-approval moved the state to {after.get('state')!r}")
    assert after.get("state") in REQUEST_STATES, f"state {after.get('state')!r} is outside the pinned set"
    assert db.count("approval_decisions") == decisions_before, (
        "the denied self-approval wrote an approval decision row")


def test_a_developer_role_is_denied_approving_any_request_at_the_api(developer, reviewer, db):
    opened = _open_request(developer, READY_COMMIT, "cross principal approval probe")
    request_id = opened["id"]
    decisions_before = db.count("approval_decisions")
    refused = developer.post(f"/promotions/{request_id}/approve", json={"comment": "let it through"})
    assert refused.status_code in DENIED, _why(
        refused, f"a developer approving a request must be denied; only the "
                 f"{ELIGIBLE_GROUP} group may approve")
    row = _request_row(reviewer, request_id)
    assert int(row.get("approvals_gathered", 0)) == 0, (
        f"the denied approval left {row.get('approvals_gathered')} approval(s) on the row")
    assert db.count("approval_decisions") == decisions_before, (
        "a denied approval wrote a decision row")


def test_finance_and_viewer_roles_are_forbidden_promoting_or_approving(developer, finance, viewer, db):
    opened = _open_request(developer, READY_COMMIT, "lower role probe")
    request_id = opened["id"]
    decisions_before = db.count("approval_decisions")
    for label, client in (("finance", finance), ("viewer", viewer)):
        refused = client.post(f"/promotions/{request_id}/approve", json={"comment": label})
        assert refused.status_code in DENIED, _why(
            refused, f"a {label} principal approving a promotion must be denied")
        raised = client.post("/promotions", json={"deployment_id": opened.get("deployment_id"),
                                                  "environment": "production",
                                                  "justification": label})
        assert raised.status_code in DENIED, _why(
            raised, f"a {label} principal opening a promotion request must be denied")
    assert db.count("approval_decisions") == decisions_before, (
        "a refused lower-role approval wrote a decision row")


def test_a_cross_entity_team_read_is_denied_with_an_identical_shape(foreign_developer, developer):
    missing = foreign_developer.get("/deployments", params={"project": f"no-such-{unique_suffix()}"})
    foreign = foreign_developer.get("/deployments", params={"project": PROJECT_SLUG})
    assert foreign.status_code in DENIED, _why(
        foreign, f"{FOREIGN_DEVELOPER_EMAIL} reading {TEAM_SLUG} deployments must be refused")
    assert foreign.status_code == missing.status_code, (
        f"an invisible project answered {foreign.status_code} while a missing one "
        f"answered {missing.status_code}; the two must be indistinguishable")
    own = foreign_developer.get("/deployments", params={"project": FOREIGN_PROJECT_SLUG})
    assert own.status_code in ACCEPTED, _why(
        own, f"{FOREIGN_DEVELOPER_EMAIL} reading its own {FOREIGN_TEAM_SLUG} project")
    body = flatten(items(_ok(developer.get("/deployments", params={"project": PROJECT_SLUG}),
                             "own team deployments").json()))
    assert FOREIGN_PROJECT_SLUG not in body, (
        f"{TEAM_SLUG} deployment data mentions {FOREIGN_PROJECT_SLUG}")


def test_a_role_change_is_forbidden_to_a_developer(developer, reviewer):
    attempt = developer.post("/firewall/rules", json={
        "project": PROJECT_SLUG, "name": f"probe-{unique_suffix()}",
        "action": "deny", "priority": 900, "condition_groups": []})
    assert attempt.status_code in DENIED, _why(
        attempt, "a developer creating a firewall rule must be denied")
    allowed = reviewer.get("/firewall/rules", params={"project": PROJECT_SLUG})
    assert allowed.status_code in ACCEPTED, _why(allowed, "a reviewer reading firewall rules")


def test_a_reserved_team_slug_is_refused_and_no_row_is_stored(reviewer, db):
    before = db.count("teams")
    for slug in ("docs", "api", "login"):
        assert slug in RESERVED_SLUGS, f"{slug!r} is not in the reserved list under audit"
        refused = reviewer.post("/teams", json={"slug": slug, "name": f"Probe {slug}"})
        assert refused.status_code in DENIED + REFUSED, _why(
            refused, f"a team slug of {slug!r} collides with a public route and must be refused")
    duplicate = reviewer.post("/teams", json={"slug": TEAM_SLUG, "name": "Duplicate"})
    assert duplicate.status_code in DENIED + REFUSED, _why(
        duplicate, f"a second team claiming {TEAM_SLUG!r} must be refused")
    assert db.count("teams") == before, "a refused team slug still wrote a team row"


def test_two_distinct_reviewers_approve_and_the_promotion_is_executed(developer, reviewer,
                                                                      reviewer_two, db):
    opened = _open_request(developer, READY_COMMIT, "two eyes happy path")
    request_id = opened["id"]
    first = reviewer.post(f"/promotions/{request_id}/approve", json={"comment": "looks right"})
    assert first.status_code in ACCEPTED, _why(first, "the first eligible approval")
    assert int(first.json().get("approvals_gathered", 0)) == 1, (
        f"after one approval the count reads {first.json().get('approvals_gathered')}")
    second = reviewer_two.post(f"/promotions/{request_id}/approve", json={"comment": "agreed"})
    assert second.status_code in ACCEPTED, _why(second, "the second eligible approval")
    row = settle(lambda: (lambda r: r if r.get("state") in ("APPROVED", "EXECUTED") else None)(
        _request_row(reviewer, request_id)))
    assert row and row.get("state") in ("APPROVED", "EXECUTED"), (
        f"after {REQUIRED_APPROVALS} approvals the request reads "
        f"{row.get('state') if row else 'nothing'}")
    aliases = items(_ok(reviewer.get("/aliases", params={"project": PROJECT_SLUG}),
                        "alias list after promotion").json())
    production = [a for a in aliases if a.get("host") == PRODUCTION_ALIAS_HOST]
    assert production, f"the production alias {PRODUCTION_ALIAS_HOST!r} is absent after promotion"
    assert db.count("approval_decisions") >= 2, (
        f"only {db.count('approval_decisions')} approval decision row(s) exist after two approvals")


def test_the_same_reviewer_approving_twice_is_refused_as_a_duplicate(developer, reviewer, db):
    opened = _open_request(developer, READY_COMMIT, "duplicate approval probe")
    request_id = opened["id"]
    first = reviewer.post(f"/promotions/{request_id}/approve", json={"comment": "first"})
    assert first.status_code in ACCEPTED, _why(first, "the first approval")
    decisions = db.count("approval_decisions")
    again = reviewer.post(f"/promotions/{request_id}/approve", json={"comment": "second"})
    assert again.status_code in DENIED + REFUSED, _why(
        again, "the same reviewer approving twice must be refused")
    assert db.count("approval_decisions") == decisions, (
        "a duplicate approval from one reviewer wrote a second decision row")


def test_a_rejection_closes_the_request_and_stores_its_comment(developer, reviewer):
    opened = _open_request(developer, READY_COMMIT, "rejection probe")
    request_id = opened["id"]
    bare = reviewer.post(f"/promotions/{request_id}/reject", json={})
    assert bare.status_code in REFUSED + DENIED, _why(
        bare, "a rejection without a comment must be refused")
    rejected = reviewer.post(f"/promotions/{request_id}/reject",
                             json={"comment": "waiting on the security review"})
    assert rejected.status_code in ACCEPTED, _why(rejected, "a rejection carrying a comment")
    row = _request_row(reviewer, request_id)
    assert row.get("state") == "REJECTED", (
        f"after a rejection the request reads {row.get('state')!r}")


def test_concurrent_approvals_are_both_persisted(developer, reviewer, reviewer_two, db):
    opened = _open_request(developer, READY_COMMIT, "concurrent approval probe")
    request_id = opened["id"]
    before = db.count("approval_decisions")

    def approve(client, comment):
        return client.post(f"/promotions/{request_id}/approve", json={"comment": comment})

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = [f.result() for f in (pool.submit(approve, reviewer, "simultaneous one"),
                                        pool.submit(approve, reviewer_two, "simultaneous two"))]
    accepted = [r for r in results if r.status_code in ACCEPTED]
    assert len(accepted) == 2, (
        f"two distinct reviewers approving at the same instant produced "
        f"{len(accepted)} acceptance(s): {[ (r.status_code, r.text[:120]) for r in results ]}")
    settle(lambda: db.count("approval_decisions") >= before + 2)
    assert db.count("approval_decisions") >= before + 2, (
        f"only {db.count('approval_decisions') - before} decision row(s) landed; "
        f"a simultaneous approval must never be dropped")


def test_concurrent_promotions_leave_one_winner_and_one_conflict(developer, reviewer,
                                                                 reviewer_two):
    first = _open_request(developer, READY_COMMIT, "race one")
    second = _open_request(developer, SUPERSEDED_COMMIT, "race two")
    for request in (first, second):
        for client in (reviewer, reviewer_two):
            client.post(f"/promotions/{request['id']}/approve", json={"comment": "race"})

    def execute(request_id):
        return developer.post(f"/promotions/{request_id}/execute", json={})

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = [f.result() for f in (pool.submit(execute, first["id"]),
                                         pool.submit(execute, second["id"]))]
    winners = [o for o in outcomes if o.status_code in ACCEPTED]
    assert len(winners) <= 1, (
        f"both promotions succeeded against one alias: "
        f"{[(o.status_code, o.text[:120]) for o in outcomes]}; exactly one must win")
    losers = [o for o in outcomes if o.status_code not in ACCEPTED]
    for loser in losers:
        assert loser.status_code in REFUSED + DENIED, _why(
            loser, "a losing promotion must be refused with a conflict, never dropped")


def test_rollback_moves_the_alias_back_to_a_superseded_deployment(developer, reviewer,
                                                                  reviewer_two):
    aliases = items(_ok(reviewer.get("/aliases", params={"project": PROJECT_SLUG}),
                        "alias list before rollback").json())
    production = [a for a in aliases if a.get("host") == PRODUCTION_ALIAS_HOST]
    assert production, f"no alias for {PRODUCTION_ALIAS_HOST!r}"
    previous = production[0].get("previous_deployment_id")
    assert "previous_deployment_id" in production[0], (
        f"the alias row carries no previous deployment; keys were {sorted(production[0])}")
    assert previous is None or isinstance(previous, (str, int)), (
        f"previous_deployment_id has type {type(previous).__name__}")


def test_audit_rows_are_append_only_with_a_gapless_sequence(reviewer, db):
    rows = items(_ok(reviewer.get("/audit", params={"team": TEAM_SLUG, "limit": 50}),
                     "audit read").json())
    assert rows, "the audit log is empty after a promotion flow has run"
    for row in rows:
        for field in ("sequence", "occurred_at", "actor", "action", "outcome"):
            assert field in row, f"an audit row is missing {field!r}; keys were {sorted(row)}"
    sequences = sorted(int(r["sequence"]) for r in rows)
    assert len(sequences) == len(set(sequences)), f"audit sequence values repeat: {sequences}"
    assert sequences == list(range(sequences[0], sequences[0] + len(sequences))), (
        f"the audit sequence has gaps across the window read: {sequences}")
    stored = db.count("audit_records")
    assert stored >= len(rows), (
        f"the API returned {len(rows)} audit rows while the store holds {stored}")


def test_a_denied_approval_stores_an_audit_row_carrying_a_deny_outcome(developer, reviewer, db):
    opened = _open_request(developer, READY_COMMIT, "audit of a denial")
    refused = developer.post(f"/promotions/{opened['id']}/approve", json={"comment": "mine"})
    assert refused.status_code in DENIED, _why(refused, "a self-approval must be denied")
    body = refused.json()
    assert isinstance(body, dict) and body, "a refusal returned no structured body"
    denials = settle(lambda: [r for r in items(
        _ok(reviewer.get("/audit", params={"team": TEAM_SLUG, "limit": 50}),
            "audit read after a denial").json()) if r.get("outcome") == "deny"])
    assert denials, "a denied approval wrote no audit row whose outcome is deny"
    assert any(r.get("reason") for r in denials), (
        "a denial audit row carries no authorization reason")
    assert db.count("audit_records") > 0, "the audit store is empty"


def test_seeded_firewall_rules_are_stored_with_their_pinned_names(reviewer, db):
    rows = items(_ok(reviewer.get("/firewall/rules", params={"project": PROJECT_SLUG}),
                     "firewall rule list").json())
    names = [r.get("name") for r in rows]
    for seeded in SEEDED_FIREWALL_RULES:
        assert seeded in names, f"seeded rule {seeded!r} is absent from {names}"
    for row in rows:
        assert row.get("action") in FIREWALL_ACTIONS, (
            f"rule {row.get('name')!r} carries action {row.get('action')!r}, outside the pinned set")
    priorities = [r.get("priority") for r in rows if r.get("priority") is not None]
    assert priorities == sorted(priorities), f"the rule list is not in ordering-value order: {priorities}"
    assert db.count("firewall_rules") >= len(SEEDED_FIREWALL_RULES), (
        f"the store holds {db.count('firewall_rules')} firewall rule row(s)")


def test_a_firewall_rule_beyond_the_plan_cap_is_refused(reviewer, db):
    plans = items(_ok(reviewer.get("/plans"), "plan list").json())
    by_name = {str(p.get("name", "")).lower(): p for p in plans}
    for plan_name, cap in PLAN_CUSTOM_RULE_CAPS:
        assert plan_name in by_name, f"plan {plan_name!r} is absent from {sorted(by_name)}"
        limits = by_name[plan_name].get("limits") or {}
        assert flatten(limits), f"plan {plan_name!r} publishes no limits"
        assert str(cap) in flatten(limits), (
            f"plan {plan_name!r} does not publish the custom-rule cap {cap}; limits were {limits}")
    before = db.count("firewall_rules")
    overflow = None
    for _ in range(41):
        overflow = reviewer.post("/firewall/rules", json={
            "project": PROJECT_SLUG, "name": f"cap-probe-{unique_suffix()}",
            "action": "log", "priority": 5000, "condition_groups": []})
        if overflow.status_code not in ACCEPTED:
            break
    assert overflow is not None and overflow.status_code in REFUSED + DENIED, _why(
        overflow, "creating past the plan cap must be refused with the cap named")
    assert db.count("firewall_rules") <= before + 40, (
        f"the store holds {db.count('firewall_rules')} rules; the pro cap is 40")


def test_the_firewall_preview_returns_a_would_match_count(reviewer):
    preview = reviewer.post("/firewall/rules/preview", json={
        "project": PROJECT_SLUG,
        "condition_groups": [{"combinator": "and",
                              "conditions": [{"field": "path", "op": "starts_with", "value": "/"}]}]})
    assert preview.status_code in ACCEPTED, _why(preview, "a rule preview")
    body = preview.json()
    assert "would_match" in body, f"the preview returned {sorted(body)} with no would_match"
    assert isinstance(body["would_match"], int), (
        f"would_match is {type(body['would_match']).__name__}, not an integer count")


def test_spend_amounts_are_integer_minor_units(finance):
    spend = _ok(finance.get("/spend", params={"team": TEAM_SLUG}), "spend read").json()
    for field in ("hard_cap_cents", "used_cents", "on_hard_cap"):
        assert field in spend, f"the spend record is missing {field!r}; keys were {sorted(spend)}"
    for field in ("hard_cap_cents", "used_cents"):
        assert isinstance(spend[field], int), (
            f"{field} is {type(spend[field]).__name__} with value {spend[field]!r}; "
            f"money is integer minor units and never a decimal")
    assert spend["on_hard_cap"] in SPEND_CAP_ACTIONS, (
        f"on_hard_cap is {spend['on_hard_cap']!r}, outside the pinned set")
    plans = items(_ok(finance.get("/plans"), "plan list").json())
    prices = {str(p.get("name", "")).lower(): p.get("price_cents") for p in plans}
    assert prices.get("pro") == PRO_PRICE_CENTS, f"the pro price reads {prices.get('pro')!r}"
    assert prices.get("hobby") == HOBBY_PRICE_CENTS, f"the hobby price reads {prices.get('hobby')!r}"
    assert all(isinstance(v, int) for v in prices.values() if v is not None), (
        f"a plan price is not an integer: {prices}")


def test_a_repeated_metering_submission_charges_once(finance, db):
    key = f"usage-{unique_suffix()}"
    payload = {"team": TEAM_SLUG, "metric": "edge_requests", "quantity": 1000,
               "unit": "requests", "idempotency_key": key}
    before = db.count("usage_records")
    first = finance.post("/usage", json=payload)
    second = finance.post("/usage", json=payload)
    assert first.status_code in ACCEPTED + DENIED + REFUSED, _why(first, "first usage submission")
    assert second.status_code in ACCEPTED + DENIED + REFUSED, _why(second, "repeated usage submission")
    settle(lambda: db.count("usage_records") >= before)
    added = db.count("usage_records") - before
    assert added <= 1, (
        f"the repeated submission of idempotency key {key!r} added {added} usage rows")


def test_the_spend_hard_cap_pause_stops_builds_and_keeps_production_serving(finance, developer,
                                                                           reviewer, app_base):
    stored = finance.put("/spend", json={"team": TEAM_SLUG, "hard_cap_cents": 1,
                                         "on_hard_cap": "pause"})
    assert stored.status_code in ACCEPTED, _why(stored, "a finance principal setting the spend cap")
    assert stored.json().get("on_hard_cap") == "pause", (
        f"the stored cap action reads {stored.json().get('on_hard_cap')!r}")
    health = httpx.get(app_base + "/api/health", timeout=TIMEOUT)
    assert health.status_code == 200, _why(
        health, "production must keep serving while spending is paused")
    listed = reviewer.get("/deployments", params={"project": PROJECT_SLUG})
    assert listed.status_code in ACCEPTED, _why(
        listed, "reading deployments must keep working while spending is paused")
    restored = finance.put("/spend", json={"team": TEAM_SLUG, "hard_cap_cents": 100000,
                                           "on_hard_cap": "notify"})
    assert restored.status_code in ACCEPTED, _why(restored, "reversing a pause in one action")


def test_notifications_are_resolved_from_the_reader_role(reviewer, finance):
    for label, client in (("reviewer", reviewer), ("finance", finance)):
        response = client.get("/notifications")
        assert response.status_code in ACCEPTED, _why(response, f"{label} reading notifications")
        assert isinstance(items(response.json()), list), (
            f"{label} notifications did not return a list")


def test_an_observability_query_is_scoped_by_the_compiler(developer, foreign_developer):
    query = {"select": "count", "from": "requests", "group_by": ["source_path"],
             "since": "1h", "limit": 10, "project": PROJECT_SLUG}
    own = developer.post("/observability/query", json=query)
    assert own.status_code in ACCEPTED, _why(own, "a member running a scoped query")
    body = own.json()
    assert "scope" in body, f"the query response declares no scope; keys were {sorted(body)}"
    assert "estimated_cost" in body, (
        f"the query response carries no cost estimate; keys were {sorted(body)}")
    foreign = foreign_developer.post("/observability/query", json=query)
    assert foreign.status_code in DENIED, _why(
        foreign, f"{FOREIGN_DEVELOPER_EMAIL} querying {PROJECT_SLUG} traffic must be refused")


def test_the_privacy_and_terms_pages_are_reachable(app_base):
    for route in ("/privacy", "/terms"):
        page = httpx.get(app_base + route, timeout=TIMEOUT, follow_redirects=True)
        assert page.status_code == 200, _why(page, f"the public page at {route}")
        assert len(page.text) > 200, f"the page at {route} returned {len(page.text)} characters"


def test_the_sitemap_lists_every_public_route_and_robots_names_it(app_base):
    sitemap = httpx.get(app_base + "/sitemap.xml", timeout=TIMEOUT, follow_redirects=True)
    assert sitemap.status_code == 200, _why(sitemap, "the sitemap")
    for route in PUBLIC_ROUTES:
        if route == "/":
            continue
        assert route in sitemap.text, f"{route} is absent from the sitemap"
    robots = httpx.get(app_base + "/robots.txt", timeout=TIMEOUT, follow_redirects=True)
    assert robots.status_code == 200, _why(robots, "the robots file")
    assert "sitemap" in robots.text.lower(), (
        f"the robots file names no sitemap; body starts {robots.text[:200]!r}")


def test_an_unknown_address_answers_not_found(app_base):
    unknown = httpx.get(f"{app_base}/no-such-page-{unique_suffix()}", timeout=TIMEOUT)
    assert unknown.status_code == 404, _why(
        unknown, "an address matching no route must answer as not found")
    console = httpx.get(f"{app_base}/{TEAM_SLUG}/{PROJECT_SLUG}/approvals", timeout=TIMEOUT,
                        follow_redirects=False)
    assert console.status_code in (200, 302, 303, 307, 308), _why(
        console, "an unauthenticated console request must redirect or render the shell")


def test_every_public_route_answers_and_carries_its_own_title(app_base):
    for route in PUBLIC_ROUTES:
        page = httpx.get(app_base + route, timeout=TIMEOUT, follow_redirects=True)
        assert page.status_code == 200, _why(page, f"the public route {route}")


def test_a_repeated_lead_submission_returns_the_first_result(anon):
    key = f"lead-{unique_suffix()}"
    payload = {"full_name": "Ada Rivera", "work_email": f"ada-{key}@example.com",
               "company_size": "500-1000", "company_website": "northwind-demo.test",
               "country": "United States", "idempotency_key": key}
    first = anon.post("/leads", json=payload)
    second = anon.post("/leads", json=payload)
    assert first.status_code in ACCEPTED, _why(first, "the first lead submission")
    assert second.status_code in ACCEPTED, _why(second, "the repeated lead submission")
    assert first.json().get("id") == second.json().get("id"), (
        f"the repeated submission created a second lead: {first.json().get('id')!r} "
        f"against {second.json().get('id')!r}")


def test_security_headers_and_error_bodies_leak_nothing(app_base, developer):
    page = httpx.get(app_base + "/login", timeout=TIMEOUT, follow_redirects=True)
    lowered = {k.lower(): v for k, v in page.headers.items()}
    assert "x-content-type-options" in lowered, (
        f"no nosniff content-type policy on the identity route; headers were {sorted(lowered)}")
    assert "content-security-policy" in lowered, (
        f"no content security policy on the identity route; headers were {sorted(lowered)}")
    refused = developer.get("/deployments", params={"project": f"missing-{unique_suffix()}"})
    body = refused.text.lower()
    for leak in ("traceback", "select ", "postgresql://", "psycopg", "/usr/lib"):
        assert leak not in body, f"an error body leaked {leak!r}: {refused.text[:300]!r}"
    assert refused.status_code not in (500, 502, 503), _why(
        refused, "a refused read must be a client error rather than a server error")
    assert str(page.url).startswith(app_base), (
        f"the identity route redirected off the app origin to {page.url}")
    assert "secret" not in str(page.url).lower(), f"a secret reached an address: {page.url}"


def test_the_environment_declares_only_the_named_backing_services(app_base, developer):
    health = httpx.get(app_base + "/api/health", timeout=TIMEOUT)
    assert health.status_code == 200, _why(health, "health before reading the environment")
    payload = json.dumps(health.json()).lower()
    for foreign in ("redis", "mongodb", "rabbitmq", "elasticsearch", "s3.amazonaws"):
        assert foreign not in payload, f"health names an undeclared backing service: {foreign}"
    teams = items(_ok(developer.get("/teams"), "team list").json())
    slugs = {t.get("slug") for t in teams}
    assert TEAM_SLUG in slugs, f"{TEAM_SLUG!r} is absent from the caller's teams {sorted(slugs)}"
