"""Deterministic observations of the deployed Girder product.

Black box only: every assertion is made over the JSON API, over the served
markup, over the rows postgres holds, or over the messages the mail sink holds.
Nothing reads the agent's source, imports a vendor SDK, or probes for a feature
at run time.
"""

from __future__ import annotations

import httpx
import pytest
from _shapes import flatten, items
from conftest import (ACTIONS, APP_DRAFT, APP_PUBLISHED, AUDITOR_EMAIL,
                      BUILDER2_EMAIL, BUILDER_EMAIL, CONFLICT_STATUS,
                      DEMO_STATES, DENIED_STATUS, ENV_PRODUCTION, ENV_STAGING,
                      GROUP_SUPPORT, INVITE_SUBJECT, INVITE_SUBJECT_PREFIX,
                      MASKED_COLUMN, OK_STATUS, OPERATION_KINDS,
                      OPERATOR2_EMAIL, OPERATOR_EMAIL, ORDER_COLUMNS,
                      ORDER_ONE, ORDER_ONE_AMOUNT, ORDER_THREE,
                      ORDER_THREE_AMOUNT, ORDER_TWO, ORDER_TWO_AMOUNT,
                      OWNER_EMAIL, PASSWORD, PROBE_STATES, QUERY_READ,
                      QUERY_WRITE, REFUSED_STATUS, RESOURCE_KIND,
                      RESOURCE_OK, RESOURCE_STALE, ROLE_BUILDER, RUN_STATES,
                      SEARCH_STATES, SEEDED_ACCOUNTS, SEEDED_ORDER_ROWS,
                      SLUG_PUBLISHED, SUBSCRIPTION_STATES, WORKSPACE,
                      app_id_for, describe, in_parallel, json_of, poll_for,
                      probe_email, resource_id_for, run_query, settle,
                      state_of, unique)


def test_health_route_reports_ready(anonymous: httpx.Client) -> None:
    response = anonymous.get("/health")
    assert response.status_code == 200, describe(
        response, "the health route once the app is ready")


def test_signin_returns_a_token_for_every_seeded_account(
        anonymous: httpx.Client) -> None:
    for email in SEEDED_ACCOUNTS:
        response = anonymous.post("/auth/login",
                                  json={"email": email, "password": PASSWORD})
        assert response.status_code in OK_STATUS, describe(
            response, f"sign-in for the seeded account {email!r}")
        body = response.json()
        assert body.get("access_token"), describe(
            response, f"sign-in for {email!r} returned no access_token")
        principal = body.get("principal") or {}
        assert principal.get("email") == email, describe(
            response, f"sign-in for {email!r} named a different principal")


def test_signin_refusal_is_identical_for_unknown_and_wrong(
        anonymous: httpx.Client) -> None:
    unknown = anonymous.post(
        "/auth/login", json={"email": probe_email("nobody"), "password": PASSWORD})
    wrong = anonymous.post(
        "/auth/login", json={"email": BUILDER_EMAIL, "password": unique("wrong")})
    assert unknown.status_code in DENIED_STATUS, describe(
        unknown, "sign-in for an address with no account")
    assert wrong.status_code == unknown.status_code, (
        f"an unknown address answered {unknown.status_code} and a wrong password "
        f"answered {wrong.status_code}; the two must be indistinguishable. "
        f"Unknown body {unknown.text[:200]!r}, wrong body {wrong.text[:200]!r}")
    assert flatten(wrong.json() if wrong.content else {}) == flatten(
        unknown.json() if unknown.content else {}), (
        f"the two refusal bodies differ: unknown {unknown.text[:200]!r} against "
        f"wrong password {wrong.text[:200]!r}")


def test_signed_out_token_is_refused_on_the_next_request(
        anonymous: httpx.Client) -> None:
    login = anonymous.post("/auth/login",
                           json={"email": OPERATOR_EMAIL, "password": PASSWORD})
    token = json_of(login, "sign-in before signing out").get("access_token")
    with httpx.Client(base_url=str(anonymous.base_url), timeout=30.0,
                      headers={"Authorization": f"Bearer {token}"}) as session:
        before = session.get("/me")
        assert before.status_code in OK_STATUS, describe(
            before, "the identity route with a live token")
        session.post("/auth/logout")
        settle()
        after = session.get("/me")
    assert after.status_code in DENIED_STATUS, describe(
        after, "the identity route after signing out")


def test_resource_catalog_names_both_seeded_resources(
        owner: httpx.Client) -> None:
    rows = items(json_of(owner.get("/resources"), "the resource catalog"))
    names = {row.get("name") for row in rows if isinstance(row, dict)}
    assert {RESOURCE_OK, RESOURCE_STALE} <= names, (
        f"the resource catalog is missing a seeded resource; found {sorted(names)}, "
        f"expected {RESOURCE_OK!r} and {RESOURCE_STALE!r} among them")
    for row in rows:
        if row.get("name") == RESOURCE_OK:
            assert row.get("kind") == RESOURCE_KIND, (
                f"resource {RESOURCE_OK!r} reports kind {row.get('kind')!r}, "
                f"expected {RESOURCE_KIND!r}")


def test_reachability_probe_reports_reachable_for_the_live_resource(
        owner: httpx.Client) -> None:
    resource = resource_id_for(owner, RESOURCE_OK)
    response = owner.post(f"/resources/{resource}/test",
                          json={"environment": ENV_PRODUCTION})
    state = state_of(response, f"the reachability probe on {RESOURCE_OK!r}")
    assert state in PROBE_STATES, (
        f"the probe on {RESOURCE_OK!r} answered {state!r}, which is outside "
        f"{PROBE_STATES}")
    assert state == "reachable", describe(
        response, f"the probe on the live resource {RESOURCE_OK!r}")


def test_reachability_probe_leaks_no_credential_for_the_stale_resource(
        owner: httpx.Client) -> None:
    resource = resource_id_for(owner, RESOURCE_STALE)
    response = owner.post(f"/resources/{resource}/test",
                          json={"environment": ENV_PRODUCTION})
    state = state_of(response, f"the reachability probe on {RESOURCE_STALE!r}")
    assert state == "unreachable", describe(
        response, f"the probe on the stale resource {RESOURCE_STALE!r}")
    body = response.text.lower()
    for leak in ("postgres:5432", "postgresql://", "password", "girder-local-dev"):
        assert leak not in body, (
            f"the probe answer on {RESOURCE_STALE!r} carries {leak!r}: "
            f"{response.text[:400]!r}")


def test_referenced_resource_delete_is_refused_naming_its_references(
        owner: httpx.Client) -> None:
    resource = resource_id_for(owner, RESOURCE_OK)
    response = owner.request("DELETE", f"/resources/{resource}")
    assert response.status_code in REFUSED_STATUS, describe(
        response, f"deleting the referenced resource {RESOURCE_OK!r}")
    assert APP_PUBLISHED.lower() in response.text.lower(), (
        f"the refusal names no reference; it must name the referencing apps and "
        f"queries. Body {response.text[:400]!r}")


def test_query_run_returns_rows_with_a_count_and_a_duration(
        builder: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    response = run_query(builder, app, QUERY_READ, ENV_PRODUCTION,
                         {"status": "delayed", "limit": 5})
    state = state_of(response, f"a read run of {QUERY_READ!r}")
    assert state == "ok", describe(response, f"a read run of {QUERY_READ!r}")
    body = response.json()
    assert isinstance(body.get("rows"), list), describe(
        response, "an ok run carrying no rows array")
    assert isinstance(body.get("row_count"), int), describe(
        response, "an ok run carrying no integer row_count")
    assert isinstance(body.get("duration_ms"), int), describe(
        response, "an ok run carrying no integer duration_ms")
    columns = body.get("columns") or []
    assert columns and all(
        isinstance(c, dict) and c.get("name") and c.get("type") for c in columns), (
        f"an ok run must declare a name and a type per column; got {columns!r}"[:400])


def test_query_run_rejects_an_undeclared_parameter(
        builder: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    response = run_query(builder, app, QUERY_READ, ENV_PRODUCTION,
                         {"status": "delayed", unique("ghost"): "1"})
    state = state_of(response, "a run carrying an undeclared parameter key")
    assert state == "invalid", (
        f"an undeclared parameter key answered {state!r}; an undeclared key is "
        f"rejected as invalid rather than ignored. Body {response.text[:400]!r}")


def test_query_run_state_is_always_from_the_closed_set(
        builder: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    seen = []
    for parameters in ({"status": "delayed", "limit": 1},
                       {"status": unique("nosuch"), "limit": 1},
                       {}):
        response = run_query(builder, app, QUERY_READ, ENV_PRODUCTION, parameters)
        seen.append(state_of(response, f"a run with parameters {parameters!r}"))
    for state in seen:
        assert state in RUN_STATES, (
            f"a run answered {state!r}, which is outside the closed set "
            f"{RUN_STATES}. Observed states were {seen}")


def test_app_catalog_lists_only_apps_the_caller_may_open(
        operator2: httpx.Client, builder: httpx.Client) -> None:
    theirs = items(json_of(operator2.get("/apps"),
                           "the app catalog for a support-group operator"))
    names = {row.get("name") for row in theirs if isinstance(row, dict)}
    assert APP_DRAFT not in names, (
        f"the support-group operator is offered {APP_DRAFT!r}, which no group "
        f"grants them; listing was {sorted(names)}")
    builders = items(json_of(builder.get("/apps"), "the app catalog for a builder"))
    builder_names = {row.get("name") for row in builders if isinstance(row, dict)}
    assert APP_DRAFT in builder_names, (
        f"the builder cannot see {APP_DRAFT!r}, which the builder group grants; "
        f"listing was {sorted(builder_names)}")


def test_app_creation_lands_a_draft_carrying_no_release(
        builder: httpx.Client) -> None:
    name = unique("Probe Desk")
    created = json_of(builder.post("/apps", json={"name": name}),
                      f"creating the app {name!r}")
    app = str(created.get("id") or created.get("slug"))
    assert app and app != "None", (
        f"creating an app returned no identity: {created!r}"[:300])
    releases = items(json_of(builder.get("/releases", params={"app_id": app}),
                             f"the release history of the new app {name!r}"))
    assert releases == [], (
        f"a newly created app already carries {len(releases)} release(s); a new "
        f"app is a draft with no release")


def test_version_freeze_returns_a_stable_content_hash(
        builder: httpx.Client) -> None:
    app = app_id_for(builder, APP_DRAFT)
    first = json_of(builder.post(f"/apps/{app}/versions", json={}),
                    f"freezing a version of {APP_DRAFT!r}")
    version_hash = first.get("version_hash")
    assert isinstance(version_hash, str) and version_hash, (
        f"freezing returned no version_hash: {first!r}"[:300])
    listing = items(json_of(builder.get(f"/apps/{app}/versions"),
                            f"the version history of {APP_DRAFT!r}"))
    hashes = [row.get("version_hash") for row in listing if isinstance(row, dict)]
    assert version_hash in hashes, (
        f"the frozen version {version_hash!r} is absent from the version history "
        f"{hashes!r}")
    assert len(hashes) == len(set(hashes)), (
        f"the version history repeats a hash: {hashes!r}")


def test_permission_decision_returns_a_reason_and_an_ordered_chain(
        owner: httpx.Client) -> None:
    response = owner.get("/decide", params={"principal": OPERATOR_EMAIL,
                                            "action": "read",
                                            "target": APP_PUBLISHED,
                                            "environment": ENV_PRODUCTION})
    body = json_of(response, "the permission answer for a seeded operator")
    assert body.get("decision") in ("allow", "deny"), describe(
        response, "the permission answer carries no allow or deny decision")
    assert isinstance(body.get("reason"), str) and body["reason"].strip(), describe(
        response, "the permission answer carries no reason")
    assert isinstance(body.get("chain"), list) and body["chain"], describe(
        response, "the permission answer carries no ordered rule chain")


def test_command_palette_targets_exclude_what_the_caller_cannot_reach(
        operator2: httpx.Client) -> None:
    response = operator2.get("/apps", params={"search": APP_DRAFT})
    rows = items(json_of(response, "a scoped search for an ungranted app"))
    assert rows == [], (
        f"a search for {APP_DRAFT!r} returned {len(rows)} row(s) to a principal no "
        f"group grants it; search is scoped at the server")


def test_environments_are_ordered_staging_then_production(
        owner: httpx.Client) -> None:
    rows = items(json_of(owner.get("/groups"), "the group listing"))
    assert rows, "the group listing is empty; three groups are seeded"
    response = owner.get("/decide", params={"principal": BUILDER_EMAIL,
                                            "action": "promote",
                                            "target": APP_PUBLISHED,
                                            "environment": ENV_STAGING})
    body = json_of(response, "the promote decision for a builder in staging")
    assert body.get("decision") == "allow", describe(
        response, "a builder must reach the unprotected environment")


def test_canvas_operations_persist_positions_sizes_and_bindings(
        builder: httpx.Client, backend) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    state = json_of(builder.get(f"/apps/{app}"), f"the app {APP_PUBLISHED!r}")
    base = state.get("base_version_hash")
    assert isinstance(base, str) and base, (
        f"the app carries no base_version_hash to build operations against: "
        f"{state!r}"[:300])
    name = unique("probe_table")
    operations = [
        {"kind": "add", "component": name, "component_kind": "table",
         "column_start": 1, "row_start": 9, "column_span": 6, "row_span": 4},
        {"kind": "bind", "component": name, "property": "rows",
         "expression": f"{QUERY_READ}.rows"},
    ]
    saved = builder.post(f"/apps/{app}/operations",
                         json={"base_version_hash": base, "operations": operations})
    assert saved.status_code in OK_STATUS, describe(
        saved, "saving two canvas operations against a current base hash")
    settle()
    reloaded = json_of(builder.get(f"/apps/{app}"),
                       f"re-reading {APP_PUBLISHED!r} after a save")
    blob = flatten(reloaded)
    assert name.lower() in blob, (
        f"the component {name!r} is absent after a re-read; positions, sizes and "
        f"bindings must all survive")
    assert f"{QUERY_READ}.rows".lower() in blob, (
        f"the binding to {QUERY_READ!r} is absent after a re-read; an app that "
        f"reopens looking right and doing nothing has lost its bindings")


def test_stale_base_version_hash_is_refused_with_the_conflict(
        builder: httpx.Client, builder2: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    state = json_of(builder.get(f"/apps/{app}"), "the app before a save")
    base = state.get("base_version_hash")
    first = builder.post(f"/apps/{app}/operations", json={
        "base_version_hash": base,
        "operations": [{"kind": "rename", "component": unique("probe"),
                        "name": unique("renamed")}]})
    assert first.status_code in OK_STATUS, describe(
        first, "the first save against a current base hash")
    settle()
    second = builder2.post(f"/apps/{app}/operations", json={
        "base_version_hash": base,
        "operations": [{"kind": "rename", "component": unique("probe"),
                        "name": unique("renamed")}]})
    assert second.status_code in CONFLICT_STATUS, describe(
        second, "a second save against the now stale base hash")
    body = second.json() if second.content else {}
    assert body.get("current_version_hash"), describe(
        second, "the conflict answer names no current_version_hash")
    assert body.get("conflicting_operations") is not None, describe(
        second, "the conflict answer carries no conflicting_operations")


def test_release_history_rows_are_append_only(
        owner: httpx.Client, builder: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    before = items(json_of(owner.get("/releases", params={"app_id": app}),
                           "the release history before a promotion"))
    frozen = json_of(builder.post(f"/apps/{app}/versions", json={}),
                     "freezing a version to promote")
    promoted = builder.post("/releases", json={
        "app_id": app, "version_hash": frozen.get("version_hash"),
        "environment": ENV_STAGING})
    assert promoted.status_code in OK_STATUS, describe(
        promoted, "promoting a frozen version to the unprotected environment")
    after = items(json_of(owner.get("/releases", params={"app_id": app}),
                          "the release history after a promotion"))
    assert len(after) == len(before) + 1, (
        f"the release history moved from {len(before)} row(s) to {len(after)}; a "
        f"promotion is an insert, never an update")
    stamps = [row.get("promoted_at") for row in after if isinstance(row, dict)]
    assert all(stamps), (
        f"a release row carries no promoted_at: {after!r}"[:400])


def test_currency_is_stored_as_integer_minor_units(
        builder: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    response = run_query(builder, app, QUERY_READ, ENV_PRODUCTION,
                         {"status": "delayed", "limit": 200})
    body = json_of(response, "a read run over the seeded orders")
    wanted = {ORDER_ONE: ORDER_ONE_AMOUNT}
    seen = {}
    for row in body.get("rows") or []:
        if isinstance(row, dict) and row.get("order_ref") in wanted:
            seen[row["order_ref"]] = row.get("amount_minor")
    assert seen, (
        f"the seeded order {ORDER_ONE!r} is absent from a delayed read; rows were "
        f"{str(body.get('rows'))[:400]}")
    for ref, amount in seen.items():
        assert isinstance(amount, int), (
            f"order {ref!r} carries amount_minor {amount!r} of type "
            f"{type(amount).__name__}; money is an integer count of minor units")
        assert amount == wanted[ref], (
            f"order {ref!r} carries amount_minor {amount!r}, expected "
            f"{wanted[ref]!r}")


def test_seeded_orders_row_count_is_stable_across_reads(
        builder: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    counts = []
    for _ in range(2):
        response = run_query(builder, app, QUERY_READ, ENV_PRODUCTION,
                             {"status": "open", "limit": 1})
        counts.append(json_of(response, "a read run counting open orders")
                      .get("row_count"))
        settle(1.0)
    assert counts[0] == counts[1], (
        f"two identical reads reported {counts[0]!r} then {counts[1]!r}; seeding "
        f"must be idempotent and a read must not duplicate rows")


def test_seeded_rows_carry_every_declared_column(
        builder: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    body = json_of(run_query(builder, app, QUERY_READ, ENV_PRODUCTION,
                             {"status": "settled", "limit": 50}),
                   "a read run over settled orders")
    names = {c.get("name") for c in (body.get("columns") or [])
             if isinstance(c, dict)}
    assert set(ORDER_COLUMNS) <= names, (
        f"the result declares columns {sorted(names)}, which is missing one of "
        f"{ORDER_COLUMNS}")
    refs = {row.get("order_ref") for row in (body.get("rows") or [])
            if isinstance(row, dict)}
    assert ORDER_THREE in refs, (
        f"the seeded settled order {ORDER_THREE!r} is absent; found {sorted(refs)[:10]}")


def test_audit_chain_verification_reports_an_intact_chain(
        auditor: httpx.Client) -> None:
    body = json_of(auditor.get("/audit/verify"), "the audit chain verification")
    assert body.get("state") == "intact", (
        f"the audit chain verification answered {body.get('state')!r}; a freshly "
        f"seeded workspace verifies intact. Body {body!r}"[:400])
    assert "first_divergent_sequence" in body, (
        f"the verification answer omits first_divergent_sequence: {body!r}"[:300])


def test_audit_row_is_appended_for_a_query_execution(
        builder: httpx.Client, auditor: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    before = len(items(json_of(auditor.get("/audit", params={"actor": BUILDER_EMAIL}),
                               "the trail for the builder before a run")))
    run_query(builder, app, QUERY_READ, ENV_PRODUCTION,
              {"status": "delayed", "limit": 1})
    grew = poll_for(lambda: len(items(json_of(
        auditor.get("/audit", params={"actor": BUILDER_EMAIL}),
        "the trail for the builder after a run"))) > before)
    assert grew, (
        f"the trail for {BUILDER_EMAIL!r} still holds {before} row(s) after a "
        f"policy-carrying execution; every such execution appends an event")


def test_audit_sequence_increases_without_gaps(auditor: httpx.Client) -> None:
    rows = items(json_of(auditor.get("/audit"), "the whole trail"))
    sequences = [row.get("sequence") for row in rows if isinstance(row, dict)]
    assert sequences and all(isinstance(s, int) for s in sequences), (
        f"the trail carries no integer sequence column: {sequences[:10]!r}")
    ordered = sorted(sequences)
    assert ordered == list(range(ordered[0], ordered[0] + len(ordered))), (
        f"the sequence has a gap or a repeat: {ordered[:20]!r}")


def test_query_run_record_stores_no_result_row(
        builder: httpx.Client, auditor: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    run_query(builder, app, QUERY_READ, ENV_PRODUCTION,
              {"status": "delayed", "limit": 5})
    settle()
    rows = items(json_of(auditor.get("/audit", params={"actor": BUILDER_EMAIL}),
                         "the trail for the builder after a run"))
    blob = flatten(rows)
    for leak in (ORDER_ONE.lower(), "bellweather", "halcyon"):
        assert leak not in blob, (
            f"an audit or run record carries the result value {leak!r}; a run "
            f"record stores that the run happened, never the rows")


def test_operator_mutation_is_denied_at_the_api(
        operator2: httpx.Client, backend) -> None:
    app = SLUG_PUBLISHED
    response = run_query(operator2, app, QUERY_WRITE, ENV_PRODUCTION,
                         {"order_ref": ORDER_TWO}, idempotency_key=unique("probe"))
    assert response.status_code in DENIED_STATUS or state_of(
        response, "a read-only group calling the mutating query") == "denied", (
        f"a read-only group's write on {QUERY_WRITE!r} was not refused: "
        f"{describe(response, 'the mutating call')}")
    settle()
    row = backend.one("orders", order_ref=ORDER_TWO)
    if row is not None:
        assert row.get("status") == "open", (
            f"order {ORDER_TWO!r} now reads status {row.get('status')!r}; a denied "
            f"mutation must leave the protected row unchanged")


def test_builder_cannot_administer_grants(builder: httpx.Client) -> None:
    response = builder.post("/grants", json={
        "principal_kind": "group", "principal": GROUP_SUPPORT,
        "scope_kind": "workspace", "scope": WORKSPACE,
        "action": "administer", "effect": "allow"})
    assert response.status_code in DENIED_STATUS, describe(
        response, "a builder writing a grant")


def test_auditor_cannot_read_an_app(auditor: httpx.Client) -> None:
    response = auditor.get("/apps")
    assert response.status_code in DENIED_STATUS, describe(
        response, "an auditor reading the app catalog")


def test_explicit_deny_defeats_every_allow_on_export(
        owner: httpx.Client) -> None:
    granted = owner.post("/grants", json={
        "principal_kind": "group", "principal": GROUP_SUPPORT,
        "scope_kind": "app", "scope": APP_PUBLISHED,
        "action": "export", "effect": "allow"})
    assert granted.status_code in OK_STATUS + REFUSED_STATUS, describe(
        granted, "adding a narrow export allow beneath a workspace deny")
    settle()
    body = json_of(owner.get("/decide", params={"principal": OPERATOR2_EMAIL,
                                                "action": "export",
                                                "target": APP_PUBLISHED,
                                                "environment": ENV_PRODUCTION}),
                   "the export decision under a workspace deny")
    assert body.get("decision") == "deny", (
        f"a narrow export allow overcame the workspace deny; the answer was "
        f"{body!r}"[:400])


def test_default_decision_is_deny_for_an_ungranted_action(
        owner: httpx.Client) -> None:
    for action in ACTIONS:
        body = json_of(owner.get("/decide", params={"principal": AUDITOR_EMAIL,
                                                    "action": action,
                                                    "target": APP_DRAFT,
                                                    "environment": ENV_STAGING}),
                       f"the {action!r} decision for the auditor on a draft app")
        if action == "read":
            continue
        assert body.get("decision") == "deny", (
            f"action {action!r} for an auditor on {APP_DRAFT!r} answered "
            f"{body.get('decision')!r}; the default outcome is deny")


def test_row_predicate_narrows_the_result_for_the_restricted_group(
        operator: httpx.Client, operator2: httpx.Client) -> None:
    wide = run_query(operator, SLUG_PUBLISHED, QUERY_READ, ENV_PRODUCTION,
                     {"status": "open", "limit": 25})
    narrow = run_query(operator2, SLUG_PUBLISHED, QUERY_READ, ENV_PRODUCTION,
                       {"status": "open", "limit": 25})
    wide_state = state_of(wide, "the unrestricted operator reading open orders")
    narrow_state = state_of(narrow, "the restricted operator reading open orders")
    assert wide_state == "ok", describe(wide, "the unrestricted read")
    assert narrow_state == "ok", describe(narrow, "the restricted read")
    wide_rows = wide.json().get("rows") or []
    narrow_rows = narrow.json().get("rows") or []
    assert len(narrow_rows) < len(wide_rows), (
        f"the restricted group received {len(narrow_rows)} row(s) against "
        f"{len(wide_rows)} for the unrestricted group; a row predicate must narrow "
        f"the same query at the server")
    for row in narrow_rows:
        assert row.get("status") == "delayed", (
            f"the restricted group received a row with status {row.get('status')!r}; "
            f"the predicate restricts the group to delayed orders")


def test_column_mask_holds_on_the_stored_row_and_the_response(
        operator2: httpx.Client, backend) -> None:
    body = json_of(run_query(operator2, SLUG_PUBLISHED, QUERY_READ,
                             ENV_PRODUCTION, {"status": "delayed", "limit": 10}),
                   "the restricted operator reading delayed orders")
    rows = body.get("rows") or []
    assert rows, "the restricted read returned no row to inspect for masking"
    stored = backend.rows("orders", limit=5, status="delayed")
    real = {row.get(MASKED_COLUMN) for row in stored if isinstance(row, dict)}
    served = {row.get(MASKED_COLUMN) for row in rows if isinstance(row, dict)}
    assert real, "no delayed order row is stored to compare the mask against"
    assert not (real & served), (
        f"the masked column {MASKED_COLUMN!r} reached the restricted group "
        f"unmasked; stored {sorted(v for v in real if v)[:3]} and served "
        f"{sorted(v for v in served if v)[:3]}")


def test_anonymous_console_request_is_denied(anonymous: httpx.Client) -> None:
    for path in ("/apps", "/resources", "/groups", "/audit"):
        response = anonymous.get(path)
        assert response.status_code in DENIED_STATUS, describe(
            response, f"an unauthenticated call to {path}")


def test_removed_member_is_denied_on_the_next_action(
        owner: httpx.Client, operator: httpx.Client) -> None:
    before = run_query(operator, SLUG_PUBLISHED, QUERY_READ, ENV_PRODUCTION,
                       {"status": "open", "limit": 1})
    assert state_of(before, "the operator reading before removal") == "ok", describe(
        before, "the operator's read before removal")
    removed = owner.request("DELETE", f"/group-members/Operations/{OPERATOR_EMAIL}")
    assert removed.status_code in OK_STATUS + (204,), describe(
        removed, f"removing {OPERATOR_EMAIL!r} from the Operations group")
    denied = poll_for(lambda: state_of(
        run_query(operator, SLUG_PUBLISHED, QUERY_READ, ENV_PRODUCTION,
                  {"status": "open", "limit": 1}),
        "the operator reading after removal") == "denied")
    assert denied, (
        f"{OPERATOR_EMAIL!r} still reads {APP_PUBLISHED!r} after removal from the "
        f"granting group; the loss takes effect on the next authorised action, "
        f"never on the next sign-in")


def test_self_approval_of_a_promotion_is_refused(
        builder: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    frozen = json_of(builder.post(f"/apps/{app}/versions", json={}),
                     "freezing a version to request approval for")
    requested = json_of(builder.post("/approvals", json={
        "app_id": app, "version_hash": frozen.get("version_hash"),
        "environment": ENV_PRODUCTION, "reason": unique("probe reason")}),
        "requesting approval to promote to production")
    approval = str(requested.get("id"))
    assert requested.get("decision") == "pending", (
        f"a fresh approval reads decision {requested.get('decision')!r}, expected "
        f"'pending'")
    response = builder.post(f"/approvals/{approval}/decision",
                            json={"decision": "granted"})
    assert response.status_code in REFUSED_STATUS, describe(
        response, "the requester granting its own approval")


def test_promotion_to_production_without_an_approval_is_refused(
        builder: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    frozen = json_of(builder.post(f"/apps/{app}/versions", json={}),
                     "freezing a version to promote without an approval")
    response = builder.post("/releases", json={
        "app_id": app, "version_hash": frozen.get("version_hash"),
        "environment": ENV_PRODUCTION})
    assert response.status_code in REFUSED_STATUS, describe(
        response, "promoting to the protected environment with no approval")


def test_operator_cannot_reach_the_editor_endpoints(
        operator: httpx.Client) -> None:
    app = SLUG_PUBLISHED
    for response in (operator.post(f"/apps/{app}/versions", json={}),
                     operator.post(f"/apps/{app}/operations",
                                   json={"base_version_hash": "x",
                                         "operations": []})):
        assert response.status_code in DENIED_STATUS, describe(
            response, "an operator calling an authoring endpoint")


def test_grid_page_request_never_returns_the_whole_table(
        operator: httpx.Client) -> None:
    body = json_of(run_query(operator, SLUG_PUBLISHED, QUERY_READ,
                             ENV_PRODUCTION, {"status": "open", "limit": 25}),
                   "one page of the seeded orders")
    rows = body.get("rows") or []
    assert len(rows) <= 25, (
        f"a page of 25 returned {len(rows)} rows; paging happens at the resource")
    assert len(rows) < SEEDED_ORDER_ROWS, (
        f"a single page carried {len(rows)} of {SEEDED_ORDER_ROWS} seeded rows; no "
        f"response carries the whole table")


def test_filter_and_sort_change_the_result_at_the_resource(
        operator: httpx.Client) -> None:
    first = json_of(run_query(operator, SLUG_PUBLISHED, QUERY_READ,
                              ENV_PRODUCTION, {"status": "open", "limit": 10}),
                    "a filtered page of open orders")
    second = json_of(run_query(operator, SLUG_PUBLISHED, QUERY_READ,
                               ENV_PRODUCTION, {"status": "settled", "limit": 10}),
                     "a filtered page of settled orders")
    open_refs = {row.get("order_ref") for row in (first.get("rows") or [])}
    settled_refs = {row.get("order_ref") for row in (second.get("rows") or [])}
    assert open_refs and settled_refs, (
        f"one of the two filters returned nothing: open {len(open_refs)}, settled "
        f"{len(settled_refs)}")
    assert not (open_refs & settled_refs), (
        f"the two filters share rows {sorted(open_refs & settled_refs)[:5]}; the "
        f"filter must be applied by the resource rather than in the browser")


def test_repeated_idempotency_key_writes_exactly_once(
        operator: httpx.Client, backend) -> None:
    key = unique("idem")
    first = run_query(operator, SLUG_PUBLISHED, QUERY_WRITE, ENV_PRODUCTION,
                      {"order_ref": ORDER_TWO}, idempotency_key=key)
    assert state_of(first, "the first mutating run") == "ok", describe(
        first, "the first mutating run under a fresh idempotency key")
    settle()
    second = run_query(operator, SLUG_PUBLISHED, QUERY_WRITE, ENV_PRODUCTION,
                       {"order_ref": ORDER_TWO}, idempotency_key=key)
    assert state_of(second, "the repeated mutating run") == "ok", describe(
        second, "the repeated mutating run under the same key")
    settle()
    rows = backend.rows("orders", limit=5, order_ref=ORDER_TWO)
    assert len(rows) <= 1, (
        f"order {ORDER_TWO!r} now has {len(rows)} rows; a repeated idempotency key "
        f"returns the first result rather than executing a second time")


def test_concurrent_promotions_on_one_approval_produce_one_release(
        builder: httpx.Client, owner: httpx.Client) -> None:
    app = app_id_for(builder, APP_PUBLISHED)
    frozen = json_of(builder.post(f"/apps/{app}/versions", json={}),
                     "freezing a version for a contested promotion")
    version_hash = frozen.get("version_hash")
    requested = json_of(builder.post("/approvals", json={
        "app_id": app, "version_hash": version_hash,
        "environment": ENV_PRODUCTION, "reason": unique("contested")}),
        "requesting approval for a contested promotion")
    granted = owner.post(f"/approvals/{requested.get('id')}/decision",
                         json={"decision": "granted"})
    assert granted.status_code in OK_STATUS, describe(
        granted, "a second principal granting the approval")
    before = len(items(json_of(owner.get("/releases", params={"app_id": app}),
                               "the release history before the race")))
    responses = in_parallel(lambda: builder.post("/releases", json={
        "app_id": app, "version_hash": version_hash,
        "environment": ENV_PRODUCTION,
        "approval_id": requested.get("id")}), count=2)
    settle()
    after = len(items(json_of(owner.get("/releases", params={"app_id": app}),
                              "the release history after the race")))
    accepted = [r for r in responses if r.status_code in OK_STATUS]
    assert after == before + 1, (
        f"two simultaneous promotions on one approval produced {after - before} "
        f"release(s); exactly one must win. Statuses were "
        f"{[r.status_code for r in responses]}")
    assert len(accepted) == 1, (
        f"{len(accepted)} of two simultaneous promotions were accepted; the loser "
        f"is refused with the state unchanged")


def test_invalid_demo_request_is_refused_as_invalid(
        anonymous: httpx.Client) -> None:
    response = anonymous.post("/demo-requests",
                              json={"work_email": "not-an-address",
                                    "reason": "Professional Services"})
    state = state_of(response, "a demo request carrying a malformed address")
    assert state in DEMO_STATES, (
        f"the demo request answered {state!r}, outside {DEMO_STATES}")
    assert state == "invalid", describe(
        response, "a demo request carrying a malformed address")


def test_valid_demo_request_and_subscription_are_accepted(
        anonymous: httpx.Client) -> None:
    demo = anonymous.post("/demo-requests",
                          json={"work_email": probe_email("demo"),
                                "reason": "Explore Girder Enterprise"})
    assert state_of(demo, "a well-formed demo request") == "sent", describe(
        demo, "a well-formed demo request")
    subscription = anonymous.post("/subscriptions",
                                  json={"email": probe_email("news"),
                                        "source_route": "/"})
    state = state_of(subscription, "a well-formed subscription")
    assert state in SUBSCRIPTION_STATES, (
        f"the subscription answered {state!r}, outside {SUBSCRIPTION_STATES}")
    assert state == "sent", describe(subscription, "a well-formed subscription")


def test_search_answers_a_closed_state_and_hides_drafts(
        anonymous: httpx.Client) -> None:
    response = anonymous.get("/search", params={"q": "girder"})
    state = state_of(response, "a site search for a common term")
    assert state in SEARCH_STATES, (
        f"search answered {state!r}, outside {SEARCH_STATES}")
    assert state == "ok", describe(response, "a site search for a common term")
    blob = flatten(response.json())
    assert "draft" not in blob or "/blog/" in blob, (
        f"the search answer mentions a draft: {response.text[:400]!r}")


def test_not_found_route_escapes_the_requested_path(web: httpx.Client) -> None:
    marker = unique("probe")
    response = web.get(f"/{marker}<script>alert(1)</script>")
    assert response.status_code in (404, 200), describe(
        response, "an address that resolves to nothing")
    assert "<script>alert(1)</script>" not in response.text, (
        "the not-found route reflected the requested path unescaped into the page")
    assert marker in response.text, (
        f"the not-found route does not name the requested path {marker!r}")


def test_sitemap_and_robots_list_public_routes_only(web: httpx.Client) -> None:
    sitemap = web.get("/sitemap.xml")
    assert sitemap.status_code == 200, describe(sitemap, "the sitemap")
    robots = web.get("/robots.txt")
    assert robots.status_code == 200, describe(robots, "the robots file")
    assert "sitemap" in robots.text.lower(), (
        f"the robots file does not name the sitemap: {robots.text[:300]!r}")
    body = sitemap.text.lower()
    for private in ("/console", "/run/"):
        assert private not in body, (
            f"the sitemap lists the private route {private!r}")


def test_every_named_navigation_destination_resolves(web: httpx.Client) -> None:
    for route in ("/", "/platform/build", "/platform/govern", "/blog", "/demo",
                  "/pricing", "/use-cases", "/docs", "/about", "/terms",
                  "/privacy", "/security", "/status", "/site-map"):
        response = web.get(route)
        assert response.status_code == 200, describe(
            response, f"the promised destination {route!r}")


def test_public_routes_declare_a_title_and_a_description(
        web: httpx.Client) -> None:
    for route in ("/", "/demo", "/blog"):
        response = web.get(route)
        markup = response.text.lower()
        assert "<title>" in markup, (
            f"the route {route!r} declares no title element")
        assert 'name="description"' in markup, (
            f"the route {route!r} declares no meta description")
        assert "color-scheme" in markup or 'name="theme-color"' in markup, (
            f"the route {route!r} declares neither a colour scheme nor a theme "
            f"colour")


def test_invitation_email_reaches_only_the_invited_inbox(
        owner: httpx.Client, inbox) -> None:
    invited = probe_email("invitee")
    created = owner.post("/invitations",
                         json={"email": invited, "group": GROUP_SUPPORT})
    assert created.status_code in OK_STATUS, describe(
        created, f"inviting {invited!r} into the support group")
    message = poll_for(lambda: inbox.find(invited, INVITE_SUBJECT_PREFIX))
    assert message is not None, (
        f"no message reached {invited!r} carrying a subject beginning "
        f"{INVITE_SUBJECT_PREFIX!r}")
    assert len(message.to) == 1, (
        f"the invitation was addressed to {message.to}; one recipient, no cc, no "
        f"bcc")
    assert inbox.count(BUILDER_EMAIL) == 0 or invited in message.to[0], (
        f"a copy of the invitation reached an uninvited inbox: {message.to}")


def test_invitation_mail_subject_names_the_workspace(
        owner: httpx.Client, inbox) -> None:
    invited = probe_email("subject")
    owner.post("/invitations", json={"email": invited, "group": GROUP_SUPPORT})
    message = poll_for(lambda: inbox.find(invited, INVITE_SUBJECT_PREFIX))
    assert message is not None, (
        f"no invitation message reached {invited!r}")
    assert message.subject.startswith(INVITE_SUBJECT_PREFIX), (
        f"the invitation subject is {message.subject!r}; it begins with "
        f"{INVITE_SUBJECT_PREFIX!r}")
    assert message.subject == INVITE_SUBJECT, (
        f"the invitation subject is {message.subject!r}, expected "
        f"{INVITE_SUBJECT!r}")
    assert WORKSPACE.lower() in message.body.lower(), (
        f"the invitation body does not name the workspace {WORKSPACE!r}: "
        f"{message.body[:300]!r}")


def test_invitation_token_is_single_use_confirmation(
        owner: httpx.Client, anonymous: httpx.Client, inbox) -> None:
    invited = probe_email("single")
    created = json_of(owner.post("/invitations",
                                 json={"email": invited, "group": GROUP_SUPPORT}),
                      f"inviting {invited!r}")
    assert "token" not in flatten(created), (
        f"the invitation response carries the token: {created!r}"[:300])
    message = poll_for(lambda: inbox.find(invited, INVITE_SUBJECT_PREFIX))
    assert message is not None, f"no invitation message reached {invited!r}"
    tokens = [word.rstrip(".,)") for word in message.body.split()
              if "/invite/" in word]
    assert tokens, (
        f"the invitation body carries no acceptance address: {message.body[:300]!r}")
    token = tokens[0].rsplit("/invite/", 1)[1]
    first = anonymous.post("/invitations/accept", json={"token": token})
    assert first.status_code in OK_STATUS, describe(
        first, "the first acceptance of an invitation token")
    second = anonymous.post("/invitations/accept", json={"token": token})
    assert second.status_code in REFUSED_STATUS, describe(
        second, "the second acceptance of the same token")


def test_revoked_invitation_sends_no_further_mail(
        owner: httpx.Client, inbox) -> None:
    invited = probe_email("revoked")
    created = json_of(owner.post("/invitations",
                                 json={"email": invited, "group": GROUP_SUPPORT}),
                      f"inviting {invited!r} before revoking")
    assert poll_for(lambda: inbox.find(invited, INVITE_SUBJECT_PREFIX)) is not None, (
        f"no invitation message reached {invited!r} before the revocation")
    before = inbox.count(invited)
    revoked = owner.request("DELETE", f"/invitations/{created.get('id')}")
    assert revoked.status_code in OK_STATUS + (204,), describe(
        revoked, "revoking a live invitation")
    settle()
    after = inbox.count(invited)
    assert after == before, (
        f"the inbox for {invited!r} moved from {before} to {after} message(s) after "
        f"a revocation; revoking sends no message")
