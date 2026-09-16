"""Black-box grading for deku/multiplayer-room-infrastructure-vb.

Every assertion reads the running application over HTTP, reads the Mailpit
inbox the app sends to, or reads the datastore through the verifier-only
credential. Nothing imports the agent's code or names a mechanism it was free to
choose. The two places the datastore is touched directly are both pinned by the
brief: the audit_event column names, and the claim that the application's own
credential cannot rewrite the record.
"""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import httpx
from playwright.sync_api import sync_playwright

from conftest import (
    ADMIN, ADMIN2, ANALYST, ATLAS, CHAIN_KEYS, COMMENT_WRITE, CONSUMER_HOST, CONTRACTOR,
    DEVELOPER, DEVELOPER2, ENTERPRISE_CONNECTIONS, NOT_FOUND_HEADING, ORG, OTHER_ORG,
    OWNER, OWNER2, RATE_MINOR_PER_MILLION, READ, REVIEWERS_GROUP, SEAT_OVERAGE_MINOR,
    SECRET_LITERALS, SEED_APPROVAL_GROUP, SEED_CREDIT, SEED_HOLD, SEED_METER_AMOUNTS, HELD_ROOM,
    SEED_INVOICE_WITHOUT_SEATS, SEED_PERIOD, SEED_PLAN_FEE, TETRAD, WRITE, ZERO_HASH,
    app_backend, argument_hash, audit_events, ceil_eight_tenths, chain_hash, code_of, connect,
    connection_record, decide, directory_token, disconnect, entitlement_cells,
    environment_id, execute,
    expect, find_event, get_request, hmac_hex, http, identity_token, in_parallel, login_token,
    new_project, new_room, new_secret, operate, parse_instant, poll, put_group,
    raise_request, request_fields, rewrite_audit_reason, room_record, set_entitlement,
    settle, site, uid,
    wait_for_mail, walk,
)
from appclient import app_url



def test_analyst_role_denied_approval_row_untouched(clients):
    admin = clients.member(ADMIN)
    developer = clients.member(DEVELOPER)
    analyst = clients.member(ANALYST)
    env = environment_id(admin, ORG, ATLAS, "production")
    room = new_room(admin, env, [READ])
    arguments = {"environment_id": env, "room_id": room}
    request = raise_request(admin, "room.delete_production", arguments,
                            "lower role denial probe")
    before = request_fields(get_request(admin, request["id"]))

    by_developer = decide(developer, request["id"])
    assert by_developer.status_code == 403 and code_of(by_developer) == "approver_not_eligible", (
        f"a developer approving someone else's request answered {by_developer.status_code}")
    refused = decide(analyst, request["id"])
    assert refused.status_code == 403, (
        f"an analyst approving a request answered {refused.status_code}: {refused.text[:300]}")
    assert code_of(refused) == "approver_not_eligible", refused.text[:300]
    refused_run = execute(analyst, request["id"], arguments)
    assert refused_run.status_code == 403, (
        f"an analyst executing a request answered {refused_run.status_code}")

    after = request_fields(get_request(admin, request["id"]))
    assert after == before, (
        f"a refused analyst decision changed the request.\nbefore={before}\nafter={after}")
    assert room_record(admin, env, room)["room_id"] == room


def test_analyst_denied_every_write_nothing_stored(clients):
    admin = clients.member(ADMIN)
    analyst = clients.member(ANALYST)
    prod = environment_id(admin, ORG, ATLAS, "production")
    dev = environment_id(admin, ORG, ATLAS, "development")
    slug = uid("analyst-project")
    room_id = uid("doc-analyst")
    reason = uid("analyst-request")
    projects_before = {p["slug"] for p in walk(admin, f"/organisations/{ORG}/projects")}

    attempts = [
        analyst.post(f"/organisations/{ORG}/projects", json={"name": slug, "slug": slug}),
        analyst.post(f"/environments/{dev}/keys", json={"kind": "secret", "label": slug}),
        analyst.post(f"/organisations/{ORG}/approvals", json={
            "action": "room.delete_production",
            "arguments": {"environment_id": prod, "room_id": "doc-almanac-brief"},
            "reason": reason}),
        analyst.post(f"/environments/{prod}/rooms", json={"room_id": room_id}),
        analyst.put(f"/environments/{prod}/rooms/doc-almanac-brief/default-accesses",
                    json={"accesses": []}),
        analyst.post(f"/organisations/{ORG}/directory-tokens"),
        analyst.patch("/entitlements/enterprise/connections_per_room", json={"value": 1}),
    ]
    for attempt in attempts:
        assert attempt.status_code == 403, (
            f"analyst {attempt.request.method} {attempt.request.url.path} answered "
            f"{attempt.status_code}, expected 403: {attempt.text[:200]}")
        assert code_of(attempt) == "forbidden", attempt.text[:200]

    listed = [p["slug"] for p in walk(admin, f"/organisations/{ORG}/projects")]
    for seeded in ("atlas-editor", "fieldnote-boards"):
        assert listed.count(seeded) == 1, f"the seeded project {seeded} is listed {listed.count(seeded)} times"
    addresses = [m.get("email") for m in walk(admin, f"/organisations/{ORG}/members")]
    for seeded in (OWNER, ADMIN, ADMIN2, DEVELOPER, CONTRACTOR, ANALYST):
        assert addresses.count(seeded) == 1, f"the seeded member {seeded} appears {addresses.count(seeded)} times"
    projects_after = set(listed)
    assert slug not in projects_after and projects_after == projects_before
    assert admin.get(f"/environments/{prod}/rooms/{room_id}/inspector").status_code == 404
    pending = walk(admin, f"/organisations/{ORG}/approvals", {"status": "pending"})
    assert not [r for r in pending if r.get("reason") == reason]
    assert room_record(admin, prod, "doc-almanac-brief")["default_accesses"] == [READ, WRITE]
    ceiling = [e for e in expect(clients.anon().get("/entitlements"), 200)["items"]
               if e["plan"] == "enterprise" and e["key"] == "connections_per_room"]
    assert ceiling and ceiling[0]["value"] == ENTERPRISE_CONNECTIONS


def test_end_user_token_cannot_reach_console_routes_denied(clients):
    admin = clients.member(ADMIN)
    prod = environment_id(admin, ORG, ATLAS, "production")
    secret = new_secret(admin, prod)["secret"]
    token = identity_token(secret, "eu-jonathan")
    end_user = clients.bearer(token)
    for path in ("/auth/me", f"/organisations/{ORG}/approvals", f"/organisations/{ORG}/audit"):
        r = end_user.get(path)
        assert r.status_code == 401, (
            f"an end user identity token on {path} answered {r.status_code}; the two "
            f"principal stores are joined somewhere: {r.text[:200]}")
        assert code_of(r) == "principal_kind_mismatch", r.text[:200]
    anonymous = clients.anon().get(f"/organisations/{ORG}/approvals")
    assert anonymous.status_code == 401 and code_of(anonymous) == "unauthenticated"


def test_cross_tenant_resource_denied_same_as_nonexistent(clients):
    admin = clients.member(ADMIN)
    stranger = clients.member(OWNER2)
    prod = environment_id(admin, ORG, ATLAS, "production")
    developer = clients.member(DEVELOPER)
    request = raise_request(developer, "room.delete_production",
                            {"environment_id": prod, "room_id": "doc-bramble-notes"},
                            "cross tenant probe")
    pairs = [
        (f"/organisations/{ORG}", f"/organisations/{uid('no-such-org')}"),
        (f"/approvals/{request['id']}", f"/approvals/{uid('req')}"),
        (f"/environments/{prod}/rooms", f"/environments/{uid('env')}/rooms"),
    ]
    for real, fake in pairs:
        a, b = stranger.get(real), stranger.get(fake)
        assert a.status_code == b.status_code == 404, (
            f"another tenant's {real} answered {a.status_code} while a missing one answered "
            f"{b.status_code}; the difference tells a stranger it exists")
        assert code_of(a) == code_of(b) == "not_found"


def test_requester_cannot_approve_own_request_denied(clients):
    admin = clients.member(ADMIN)
    admin2 = clients.member(ADMIN2)
    env = environment_id(admin, ORG, ATLAS, "production")
    room = new_room(admin, env, [])
    request = raise_request(admin, "room.default_access_public",
                            {"environment_id": env, "room_id": room}, "self approval probe")
    own = decide(admin, request["id"])
    assert own.status_code == 403, (
        f"an eligible admin approving their own request answered {own.status_code}; self "
        f"approval must be refused in the policy layer: {own.text[:300]}")
    assert code_of(own) == "self_approval_refused", own.text[:300]
    unchanged = get_request(admin, request["id"])
    assert unchanged["status"] == "pending" and not unchanged.get("decisions")

    other = expect(decide(admin2, request["id"]), 201)
    assert other["status"] == "approved", other


def test_break_glass_without_fresh_second_factor_denied(break_glass_scenario, clients):
    s = break_glass_scenario
    assert s["refused_owner"].status_code == 403, (
        f"break glass without a mailed second factor answered {s['refused_owner'].status_code}")
    assert code_of(s["refused_owner"]) == "second_factor_required"
    assert s["refused_admin"].status_code == 403
    assert code_of(s["refused_admin"]) == "approver_not_eligible"
    assert s["room_after_refusals"]["default_accesses"] == [], (
        "a refused break glass still changed the room's default access")


def test_production_secret_shown_once_never_stored_in_clear(clients, db):
    admin = clients.member(ADMIN)
    prod = environment_id(admin, ORG, ATLAS, "production")
    developer_try = clients.member(DEVELOPER).post(f"/environments/{prod}/keys",
                                                  json={"kind": "secret", "label": uid("dev-prod")})
    assert developer_try.status_code == 403 and code_of(developer_try) == "forbidden", (
        f"a developer issued a production key ({developer_try.status_code})")
    created = new_secret(admin, prod)
    secret = created.get("secret")
    assert secret and len(secret) >= 16, f"production key creation returned {created}"
    read = admin.get(f"/keys/{created['id']}")
    expect(read, 200)
    assert secret not in read.text, "reading a production key returned its secret"
    reveal = admin.post(f"/keys/{created['id']}/reveal")
    assert reveal.status_code == 409 and code_of(reveal) == "secret_not_revealable", (
        f"revealing a production secret answered {reveal.status_code}: {reveal.text[:200]}")
    assert secret not in reveal.text

    columns = db.query(
        "SELECT table_schema, table_name, column_name FROM information_schema.columns "
        "WHERE table_schema NOT IN ('pg_catalog', 'information_schema') "
        "AND data_type IN ('text', 'character varying', 'jsonb', 'json', 'bytea', 'character')")
    holders = []
    for c in columns:
        sql = (f'SELECT 1 AS hit FROM "{c["table_schema"]}"."{c["table_name"]}" '
               f'WHERE position(%s in "{c["column_name"]}"::text) > 0 LIMIT 1')
        if db.query(sql, (secret,)):
            holders.append(f'{c["table_name"]}.{c["column_name"]}')
    assert not holders, (
        f"the production secret is stored in the clear in {holders}; only a hash may be kept")


def test_development_secret_reveal_repeatable_each_audited(clients):
    developer = clients.member(DEVELOPER)
    owner = clients.member(OWNER)
    dev = environment_id(developer, ORG, ATLAS, "development")
    created = new_secret(developer, dev)
    rids = [uid("rid-reveal"), uid("rid-reveal")]
    secrets = []
    for rid in rids:
        r = developer.post(f"/keys/{created['id']}/reveal", headers={"X-Request-Id": rid})
        secrets.append(expect(r, 200).get("secret"))
    assert secrets[0] == secrets[1] == created["secret"], "a development reveal changed the secret"
    for rid in rids:
        events = find_event(owner, rid)
        assert [e for e in events if e.get("action") == "key.revealed"
                and e.get("resource_id") == created["id"]], (
            f"the reveal carrying request {rid} wrote no key.revealed audit event")


def test_rotation_keeps_two_valid_keys_then_retire_closes_its_connections_token(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    first = new_secret(admin, env)
    second = new_secret(admin, env)
    room = new_room(admin, env, [READ])
    old = connect(first["secret"], uid("eu-rot"), room)
    new = connect(second["secret"], uid("eu-rot"), room)
    assert old.status == 201 and new.status == 201, "both keys must authenticate during rotation"

    expect(admin.post(f"/keys/{first['id']}/retire"), 200)
    with httpx.Client(base_url=app_url() + "/api", timeout=30.0,
                      headers={"Authorization": f"Bearer {first['secret']}"}) as c:
        refused = c.post("/identity-tokens", json={"user_id": uid("eu-rot")})
    assert refused.status_code == 401 and code_of(refused) == "key_retired", refused.text[:200]
    identity_token(second["secret"], uid("eu-rot"))

    closed = poll(lambda: connection_record(admin, old.id),
                  lambda rec: rec.get("closed_at") is not None, 35.0, 1.0)
    assert closed.get("closed_at") is not None, (
        "a connection authenticated by a retired key was still open 35 seconds later")
    assert connection_record(admin, new.id).get("closed_at") is None, (
        "retiring one key closed a connection authenticated by the other")


def test_jit_grant_opens_regulated_inspector_then_access_expires(clients):
    owner = clients.member(OWNER)
    admin = clients.member(ADMIN)
    developer = clients.member(DEVELOPER)
    env = environment_id(owner, ORG, ATLAS, "production")
    path = f"/environments/{env}/rooms/doc-sundial-intake/inspector"
    standing = owner.get(path)
    assert standing.status_code == 403 and code_of(standing) == "access_not_granted", (
        f"an owner opened a regulated room with no grant: {standing.status_code}")

    access = expect(developer.post("/access-requests", json={
        "environment_id": env, "room_id": "doc-sundial-intake",
        "reason": "verifier just in time probe"}), 201)
    too_long = admin.post(f"/access-requests/{access['id']}/grant",
                          json={"duration_seconds": 14401})
    assert too_long.status_code == 422, "a grant longer than four hours was accepted"
    expect(admin.post(f"/access-requests/{access['id']}/grant",
                      json={"duration_seconds": 6}), 200)
    rid = uid("rid-jit")
    opened = developer.get(path, headers={"X-Request-Id": rid})
    assert opened.status_code == 200, f"a granted inspector read answered {opened.status_code}"
    attributed = [e for e in find_event(owner, rid) if e.get("action") == "room.inspected"]
    assert attributed and attributed[0].get("reason") == access["id"], (
        f"the read inside the grant is not attributed to it: {attributed}")
    expired = poll(lambda: developer.get(path), lambda r: r.status_code == 403, 25.0, 1.0)
    assert expired.status_code == 403 and code_of(expired) == "access_not_granted", (
        "the just in time grant did not expire on its own")


def test_user_grant_narrows_group_grant_write_denied(clients):
    admin = clients.member(ADMIN)
    env = environment_id(admin, ORG, ATLAS, "production")
    secret = new_secret(admin, env)["secret"]
    olivier = connect(secret, "eu-olivier", "doc-cadence-roadmap")
    alicia = connect(secret, "eu-alicia", "doc-cadence-roadmap")
    assert olivier.status == 201 and alicia.status == 201
    assert operate(olivier.token, olivier.id, "storage.read").status_code == 202
    narrowed = operate(olivier.token, olivier.id, "storage.write")
    assert narrowed.status_code == 403, (
        f"eu-olivier holds a user grant of read under a group grant of write and wrote "
        f"anyway ({narrowed.status_code}); the layers were unioned, not replaced")
    assert code_of(narrowed) == "operation_not_permitted"
    assert operate(alicia.token, alicia.id, "storage.write").status_code == 202


def test_grant_layers_resolve_by_replacement_across_every_combination(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    group = uid("grp-combo")
    user = uid("eu-combo")
    put_group(directory_token(admin), group, [], [{"environment_id": env, "user_id": user}])
    room = new_room(admin, env, [])
    base = f"/environments/{env}/rooms/{room}"
    layers = [None, [], [READ], [READ, WRITE]]
    wrong = []
    for default in ([], [READ], [READ, WRITE]):
        expect(admin.put(f"{base}/default-accesses", json={"accesses": default}), 200)
        for group_layer in layers:
            if group_layer is None:
                expect(admin.delete(f"{base}/group-accesses/{group}"), 200, 204, 404)
            else:
                expect(admin.put(f"{base}/group-accesses/{group}",
                                 json={"accesses": group_layer}), 200, 201)
            for user_layer in layers:
                if user_layer is None:
                    expect(admin.delete(f"{base}/user-accesses/{user}"), 200, 204, 404)
                else:
                    expect(admin.put(f"{base}/user-accesses/{user}",
                                     json={"accesses": user_layer}), 200, 201)
                effective = (user_layer if user_layer is not None
                             else group_layer if group_layer is not None else default)
                c = connect(secret, user, room)
                can_read = READ in effective
                if c.status != (201 if can_read else 403):
                    wrong.append((default, group_layer, user_layer, "admission", c.status))
                    continue
                if can_read:
                    w = operate(c.token, c.id, "storage.write").status_code
                    if w != (202 if WRITE in effective else 403):
                        wrong.append((default, group_layer, user_layer, "write", w))
                    disconnect(c.token, c.id)
    assert not wrong, (
        f"{len(wrong)} of 48 grant combinations resolved wrongly (default, group, user, "
        f"check, status): {wrong[:8]}")


def test_removed_write_access_denied_on_next_operation_connection_stays_open(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    group, user = uid("grp-live"), uid("eu-live")
    put_group(directory_token(admin), group, [], [{"environment_id": env, "user_id": user}])
    room = new_room(admin, env, [])
    grant = f"/environments/{env}/rooms/{room}/group-accesses/{group}"
    expect(admin.put(grant, json={"accesses": [READ, WRITE]}), 200, 201)
    c = connect(secret, user, room)
    assert c.status == 201 and operate(c.token, c.id, "storage.write").status_code == 202

    expect(admin.put(grant, json={"accesses": [READ]}), 200, 201)
    refused = poll(lambda: operate(c.token, c.id, "storage.write"),
                   lambda r: r.status_code == 403, 6.0, 0.5)
    assert refused.status_code == 403 and code_of(refused) == "operation_not_permitted", (
        f"five seconds after write was withdrawn the open connection still wrote "
        f"({refused.status_code}); permission was captured at admission")
    assert operate(c.token, c.id, "storage.read").status_code == 202
    assert connection_record(admin, c.id).get("closed_at") is None, (
        "withdrawing write closed the connection instead of refusing the operation")


def test_removed_read_access_closes_the_connection(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    group, user = uid("grp-close"), uid("eu-close")
    put_group(directory_token(admin), group, [], [{"environment_id": env, "user_id": user}])
    room = new_room(admin, env, [])
    grant = f"/environments/{env}/rooms/{room}/group-accesses/{group}"
    expect(admin.put(grant, json={"accesses": [READ]}), 200, 201)
    c = connect(secret, user, room)
    assert c.status == 201 and operate(c.token, c.id, "storage.read").status_code == 202

    expect(admin.delete(grant), 200, 204)
    gone = poll(lambda: operate(c.token, c.id, "storage.read"),
                lambda r: r.status_code == 410, 6.0, 0.5)
    assert gone.status_code == 410 and code_of(gone) == "connection_closed", (
        f"five seconds after read was withdrawn the connection still answered {gone.status_code}")
    record = connection_record(admin, c.id)
    assert record.get("closed_at") is not None and record.get("close_reason"), record


def test_group_membership_change_denied_within_five_seconds(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    token = directory_token(admin)
    group, user = uid("grp-member"), uid("eu-member")
    put_group(token, group, [], [{"environment_id": env, "user_id": user}])
    room = new_room(admin, env, [])
    expect(admin.put(f"/environments/{env}/rooms/{room}/group-accesses/{group}",
                     json={"accesses": [READ, WRITE]}), 200, 201)
    c = connect(secret, user, room)
    assert c.status == 201 and operate(c.token, c.id, "storage.write").status_code == 202

    put_group(token, group, [], [])
    gone = poll(lambda: operate(c.token, c.id, "storage.write"),
                lambda r: r.status_code == 410, 6.0, 0.5)
    assert gone.status_code == 410, (
        f"five seconds after the directory removed the end user from the group, their "
        f"connection answered {gone.status_code}; group claims were read once")


def test_comment_write_separable_from_room_write_permission(clients):
    admin = clients.member(ADMIN)
    env = environment_id(admin, ORG, ATLAS, "production")
    secret = new_secret(admin, env)["secret"]
    reviewer = connect(secret, "eu-alicia", "doc-bramble-notes")
    assert reviewer.status == 201
    assert reviewer.payload.get("accesses") and COMMENT_WRITE in reviewer.payload["accesses"]
    assert operate(reviewer.token, reviewer.id, "comment.write").status_code == 202
    blocked = operate(reviewer.token, reviewer.id, "storage.write")
    assert blocked.status_code == 403 and code_of(blocked) == "operation_not_permitted", (
        "a reviewer granted comment write but not document write changed the document")
    room = new_room(admin, env, [READ, WRITE])
    editor = connect(secret, uid("eu-editor"), room)
    assert operate(editor.token, editor.id, "storage.write").status_code == 202
    no_comment = operate(editor.token, editor.id, "comment.write")
    assert no_comment.status_code == 403, (
        "document write was treated as implying comment write")


def test_analyst_and_stranger_cannot_open_page_view_log_owner_only(clients):
    probe = f"/{uid('page-view-probe')}"
    with site() as s:
        s.get(probe)
    owner = clients.member(OWNER)
    views = poll(lambda: walk(owner, "/page-views", max_pages=3),
                 lambda items: any(v.get("route") == probe for v in items), 15.0, 1.0)
    recorded = [v for v in views if v.get("route") == probe]
    assert recorded, f"a view of {probe} was not recorded"
    assert recorded[0].get("status") == 404 and recorded[0].get("occurred_at")
    assert clients.member(ANALYST).get("/page-views").status_code == 403
    assert clients.anon().get("/page-views").status_code == 401


def test_revocation_revokes_member_sessions_token_denied(revocation_scenario):
    s = revocation_scenario
    with httpx.Client(base_url=app_url() + "/api", timeout=30.0,
                      headers={"Authorization": f"Bearer {s['contractor_token']}"}) as c:
        me = c.get("/auth/me")
    assert me.status_code == 401 and code_of(me) == "session_revoked", (
        f"a session held by a member of the revoked group still answered {me.status_code}: "
        f"{me.text[:200]}")




def test_revocation_terminates_every_live_connection_of_the_group(revocation_scenario, clients):
    s = revocation_scenario
    executed = expect(s["executed"], 200)
    assert executed.get("status") == "executed", executed
    admin = clients.member(ADMIN)
    for member in s["member_connections"]:
        assert member.status == 201, "the scenario could not open a group member's connection"
        record = poll(lambda m=member: connection_record(admin, m.id),
                      lambda rec: rec.get("closed_at") is not None, 5.0, 0.5)
        assert record.get("closed_at") is not None and record.get("close_reason"), (
            f"a live connection held by a revoked group's end user is still open: {record}")
        after = operate(member.token, member.id, "storage.read")
        assert after.status_code == 410 and code_of(after) == "connection_closed", after.text[:200]


def test_seeded_revocation_executed_in_console_record(clients):
    admin = clients.member(ADMIN)
    seeded = [r for r in walk(admin, f"/organisations/{ORG}/approvals")
              if r.get("action") == "group.revoke_access"
              and (r.get("arguments") or {}).get("group_external_id") == SEED_APPROVAL_GROUP
              and r.get("requested_by") == DEVELOPER]
    assert seeded, "the seeded revocation request is not listed"
    assert any(r.get("status") == "executed" for r in seeded), (
        f"the seeded revocation of {SEED_APPROVAL_GROUP} was not executed through the console: "
        f"{[r.get('status') for r in seeded]}")
    group = expect(admin.get(f"/organisations/{ORG}/groups/{SEED_APPROVAL_GROUP}"), 200)
    statuses = {m.get("email"): m.get("status") for m in group.get("members", [])}
    assert statuses.get(DEVELOPER2) == "deprovisioned", statuses
    env = environment_id(admin, ORG, ATLAS, "production")
    grants = expect(admin.get(f"/environments/{env}/rooms/doc-foundry-handoff/group-accesses"), 200)
    assert SEED_APPROVAL_GROUP not in {g.get("group_external_id") for g in grants.get("items", [])}
    dev = environment_id(admin, ORG, ATLAS, "development")
    sandbox = [k for k in walk(admin, f"/environments/{dev}/keys")
               if k.get("label") == "Contractor sandbox"]
    assert sandbox and sandbox[0].get("status") == "retired", sandbox


def test_impact_growth_returns_request_to_pending(impact_growth_scenario):
    s = impact_growth_scenario
    assert expect(s["approved"], 201).get("status") == "approved"
    assert s["joined"].status == 201
    grown = s["grown"]
    assert grown.status_code == 409 and code_of(grown) == "impact_changed", (
        f"a request whose impact grew after approval executed anyway: {grown.status_code} "
        f"{grown.text[:300]}")
    payload = grown.json()
    assert payload["approved_impact"]["connections"] == 0
    assert payload["current_impact"]["connections"] == 1
    assert s["after_growth"]["status"] == "pending"
    stale = s["stale_execute"]
    assert stale.status_code == 409 and code_of(stale) == "request_not_approved", (
        "the approval given before the impact grew still counted")
    assert expect(s["reapproved"], 201).get("status") == "approved"
    assert expect(s["final_execute"], 200).get("status") == "executed", (
        "a freshly re-approved request could not execute, so the guard blocks everything")
    assert s["room_after"]["default_accesses"] == [READ]


def test_expired_request_reads_expired_and_execution_conflict(expiry_scenario, clients):
    s = expiry_scenario
    admin = clients.member(ADMIN)
    read = poll(lambda: get_request(admin, s["probed"]["id"]),
                lambda r: r.get("status") == "expired", 20.0, 1.0)
    assert read.get("status") == "expired", (
        f"a request past its expiry still reads {read.get('status')!r}")
    listed = walk(admin, f"/organisations/{ORG}/approvals", {"status": "expired"})
    assert s["probed"]["id"] in {r.get("id") for r in listed}
    run = execute(admin, s["probed"]["id"], s["probed"]["arguments"])
    assert run.status_code == 409 and code_of(run) == "request_expired", run.text[:200]
    assert room_record(admin, s["env"], s["probed_room"])["room_id"] == s["probed_room"]


def test_break_glass_review_item_stays_outstanding_until_justified(break_glass_scenario, clients):
    used = expect(break_glass_scenario["used"], 200)
    item_id = used.get("review_item_id")
    assert item_id, used
    owner = clients.member(OWNER)

    def item():
        for i in walk(owner, f"/organisations/{ORG}/review-items"):
            if i.get("id") == item_id:
                return i
        return {}

    assert item().get("status") == "outstanding"
    short = owner.post(f"/review-items/{item_id}/close", json={"justification": "done"})
    assert short.status_code == 422 and item().get("status") == "outstanding"
    expect(owner.post(f"/review-items/{item_id}/close", json={
        "justification": "Declared incident: production room exposure fixed and verified."}), 200)
    assert item().get("status") == "closed"


def test_two_approver_action_needs_two_distinct_admins(clients):
    admin = clients.member(ADMIN)
    admin2 = clients.member(ADMIN2)
    developer = clients.member(DEVELOPER)
    space = new_project(admin)
    request = raise_request(developer, "project.delete", {"project_id": space["project"]},
                            "two approver probe")
    first = expect(decide(admin, request["id"]), 201)
    assert first["status"] == "pending", "one approval approved a two approver action"
    again = decide(admin, request["id"])
    assert again.status_code == 409 and code_of(again) == "already_decided"
    assert get_request(admin, request["id"])["status"] == "pending"
    assert expect(decide(admin2, request["id"]), 201)["status"] == "approved"


def test_downgrade_breaching_entitlement_accepted_and_scheduled(clients):
    owner = clients.member(OWNER)
    before = sorted((e["plan"], e["key"], json.dumps(e["value"]))
                    for e in expect(clients.anon().get("/entitlements"), 200)["items"])
    change = owner.post(f"/organisations/{ORG}/plan-changes", json={"plan": "team"})
    payload = expect(change, 202)
    try:
        assert payload.get("status") == "scheduled" and payload.get("effective_at"), payload
        named = {(e.get("entitlement"), e.get("resource_type"), e.get("resource_id"))
                 for e in payload.get("exceeding", [])}
        assert ("directory_sync", "group", REVIEWERS_GROUP) in named, (
            f"a downgrade that loses directory sync did not name the directory groups: {named}")
        assert expect(owner.get(f"/organisations/{ORG}"), 200).get("plan") == "enterprise"
        after = sorted((e["plan"], e["key"], json.dumps(e["value"]))
                       for e in expect(clients.anon().get("/entitlements"), 200)["items"])
        assert after == before, "scheduling a downgrade changed entitlements before period end"
    finally:
        expect(owner.delete(f"/organisations/{ORG}/plan-changes/{payload.get('id')}"), 204)



def test_revocation_retires_member_credentials_and_group_grants_stored(revocation_scenario, clients):
    s = revocation_scenario
    admin = clients.member(ADMIN)
    key = expect(admin.get(f"/keys/{s['contractor_key']['id']}"), 200)
    assert key.get("status") == "retired", f"a revoked member's key reads {key.get('status')!r}"
    with httpx.Client(base_url=app_url() + "/api", timeout=30.0,
                      headers={"Authorization": f"Bearer {s['contractor_key']['secret']}"}) as c:
        refused = c.post("/identity-tokens", json={"user_id": uid("eu-after")})
    assert refused.status_code == 401 and code_of(refused) == "key_retired"
    for room in s["rooms"]:
        grants = expect(admin.get(f"/environments/{s['env']}/rooms/{room}/group-accesses"), 200)
        assert s["group"] not in {g.get("group_external_id") for g in grants.get("items", [])}, (
            f"the revoked group still holds a grant on {room}")
    group = expect(admin.get(f"/organisations/{ORG}/groups/{s['group']}"), 200)
    assert {m.get("email"): m.get("status") for m in group["members"]}.get(CONTRACTOR) == "deprovisioned"


def test_revocation_impact_counts_and_outsider_connection_untouched(revocation_scenario, clients):
    s = revocation_scenario
    assert s["request"]["impact"] == {"rooms": 2, "connections": 2, "end_users": 2,
                                      "members": 1, "credentials": 1}, s["request"]["impact"]
    outsider = s["outsider_connection"]
    admin = clients.member(ADMIN)
    assert outsider.status == 201
    assert connection_record(admin, outsider.id).get("closed_at") is None, (
        "revoking a group closed a connection held by someone outside it")
    assert operate(outsider.token, outsider.id, "storage.read").status_code == 202


def test_execute_with_unapproved_arguments_conflict_nothing_stored(clients):
    admin = clients.member(ADMIN)
    developer = clients.member(DEVELOPER)
    env = environment_id(admin, ORG, ATLAS, "production")
    approved_room, other_room = new_room(admin, env, []), new_room(admin, env, [])
    approved_args = {"environment_id": env, "room_id": approved_room}
    request = raise_request(developer, "room.default_access_public", approved_args,
                            "argument drift probe")
    expect(decide(admin, request["id"]), 201)
    drift = execute(admin, request["id"], {"environment_id": env, "room_id": other_room})
    assert drift.status_code == 409 and code_of(drift) == "arguments_not_approved", (
        f"executing arguments nobody approved answered {drift.status_code}: {drift.text[:300]}")
    assert get_request(admin, request["id"])["status"] == "approved"
    assert room_record(admin, env, other_room)["default_accesses"] == []
    assert room_record(admin, env, approved_room)["default_accesses"] == []

    done = expect(execute(admin, request["id"], approved_args), 200)
    assert done["status"] == "executed"
    assert room_record(admin, env, approved_room)["default_accesses"] == [READ]


def test_approval_records_canonical_argument_hash_stored(clients):
    admin = clients.member(ADMIN)
    admin2 = clients.member(ADMIN2)
    env = environment_id(admin, ORG, ATLAS, "production")
    room = new_room(admin, env, [])
    arguments = {"room_id": room, "environment_id": env}
    expected = argument_hash(arguments)
    request = raise_request(admin, "room.default_access_public", arguments, "hash probe")
    sibling = raise_request(admin, "room.default_access_public", arguments, "hash probe twin")
    for rid in (request["id"], sibling["id"]):
        assert re.fullmatch(r"req_[A-Za-z0-9_-]{6,}", rid), f"request identifier {rid!r} is not opaque and typed"
    tails = [r["id"][4:] for r in (request, sibling)]
    assert not (all(x.isdigit() for x in tails) and abs(int(tails[0]) - int(tails[1])) == 1), (
        f"request identifiers {tails} are sequential")
    assert request["argument_hash"] == expected, (
        f"argument_hash {request['argument_hash']} is not the SHA-256 of the sorted, "
        f"whitespace-free arguments ({expected})")
    decided = expect(decide(admin2, request["id"]), 201)
    assert [d.get("argument_hash") for d in decided["decisions"]] == [expected]


def test_connection_past_ceiling_refused_others_undisturbed_count(clients):
    owner = clients.member(OWNER)
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    room = new_room(admin, env, [READ, WRITE])
    set_entitlement(owner, "enterprise", "connections_per_room", 2)
    try:
        table = expect(clients.anon().get("/entitlements"), 200)["items"]
        assert [e["value"] for e in table if e["plan"] == "enterprise"
                and e["key"] == "connections_per_room"] == [2]
        held = [connect(secret, uid("eu-cap"), room) for _ in range(2)]
        assert [c.status for c in held] == [201, 201]
        extra = connect(secret, uid("eu-cap"), room)
        assert extra.status == 409 and extra.payload.get("code") == "room_full", (
            f"the connection past a ceiling of 2 answered {extra.status}; the admission check "
            f"is not reading the entitlement table")
        assert extra.payload.get("entitlement") == "connections_per_room"
        assert extra.payload.get("ceiling") == 2
        for c in held:
            assert operate(c.token, c.id, "storage.read").status_code == 202, (
                "refusing the newest connection disturbed one already present")
        capacity = expect(admin.get(f"/environments/{env}/rooms/{room}/capacity"), 200)
        assert (capacity.get("open_connections"), capacity.get("ceiling"),
                capacity.get("warning_at")) == (2, 2, 2), capacity
        disconnect(held[0].token, held[0].id)
        assert connect(secret, uid("eu-cap"), room).status == 201
    finally:
        set_entitlement(owner, "enterprise", "connections_per_room", ENTERPRISE_CONNECTIONS)


def test_entitlement_change_moves_capacity_warning_threshold(clients):
    owner = clients.member(OWNER)
    admin = clients.member(ADMIN)
    env = environment_id(admin, ORG, ATLAS, "production")
    try:
        for ceiling in (5, 7, 13):
            set_entitlement(owner, "enterprise", "connections_per_room", ceiling)
            capacity = expect(admin.get(
                f"/environments/{env}/rooms/doc-almanac-brief/capacity"), 200)
            assert capacity.get("ceiling") == ceiling, capacity
            assert capacity.get("warning_at") == ceil_eight_tenths(ceiling), capacity
    finally:
        set_entitlement(owner, "enterprise", "connections_per_room", ENTERPRISE_CONNECTIONS)


def test_entitlement_change_moves_invoice_seat_line_record(clients):
    owner = clients.member(OWNER)
    try:
        set_entitlement(owner, "enterprise", "seats_included", 2)
        seats = sum(1 for m in walk(owner, f"/organisations/{ORG}/members")
                    if m.get("status") in ("active", "invited"))
        invoice = expect(owner.get(f"/organisations/{ORG}/invoices/{SEED_PERIOD}"), 200)
        seat_lines = [l for l in invoice["lines"] if l.get("kind") == "seats"]
        assert len(seat_lines) == 1
        assert seat_lines[0]["amount_minor"] == max(0, seats - 2) * SEAT_OVERAGE_MINOR, (
            f"with {seats} seats and 2 included the seat line reads "
            f"{seat_lines[0]['amount_minor']}; the invoice is not reading the entitlement")
        assert invoice["total_minor"] == sum(l["amount_minor"] for l in invoice["lines"])
    finally:
        set_entitlement(owner, "enterprise", "seats_included", "unlimited")
    restored = expect(owner.get(f"/organisations/{ORG}/invoices/{SEED_PERIOD}"), 200)
    assert [l["amount_minor"] for l in restored["lines"] if l["kind"] == "seats"] == [0]


def test_collaboration_minutes_accrue_per_room_only_with_two_connections(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    shared, lonely = new_room(admin, env, [READ]), new_room(admin, env, [READ])

    first = connect(secret, uid("eu-meter"), shared)
    alone = connect(secret, uid("eu-meter"), lonely)
    settle(3)
    second = connect(secret, uid("eu-meter"), shared)
    settle(6)
    disconnect(second.token, second.id)
    settle(3)
    disconnect(first.token, first.id)
    disconnect(alone.token, alone.id)

    together = expect(admin.get(f"/environments/{env}/rooms/{shared}/accrual"), 200)
    seconds = together.get("collaboration_seconds")
    assert isinstance(seconds, int) and 4 <= seconds <= 9, (
        f"two connections overlapped for about six seconds and the room accrued {seconds}; "
        f"about twelve means it accrued with one connection, more means per participant")
    single = expect(admin.get(f"/environments/{env}/rooms/{lonely}/accrual"), 200)
    assert single.get("collaboration_seconds") == 0, (
        f"a room that only ever held one connection accrued {single}")


def test_six_participants_bill_one_room_window_record(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    room = new_room(admin, env, [READ])
    tokens = [identity_token(secret, uid("eu-six")) for _ in range(6)]

    def join(i):
        with httpx.Client(base_url=app_url() + "/api", timeout=30.0,
                          headers={"Authorization": f"Bearer {tokens[i]}"}) as c:
            return c.post("/rt/connections", json={"room_id": room})

    opened = in_parallel(6, join)
    assert [r.status_code for r in opened] == [201] * 6
    settle(5)
    for token, r in zip(tokens, opened):
        disconnect(token, r.json()["connection_id"])
    seconds = expect(admin.get(f"/environments/{env}/rooms/{room}/accrual"), 200).get(
        "collaboration_seconds")
    assert isinstance(seconds, int) and 3 <= seconds <= 9, (
        f"six people for about five seconds accrued {seconds}; about thirty means the room "
        f"is billed per participant")


def test_level_meter_bills_highest_sample_not_sum_stored(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    room = new_room(admin, env, [READ])
    rows = [("data_stored_gb", "00", "01", 10), ("data_stored_gb", "01", "02", 10),
            ("data_stored_gb", "02", "03", 10), ("file_storage_gb", "00", "01", 4),
            ("file_storage_gb", "01", "02", 4), ("collaboration_minutes", "00", "01", 30),
            ("collaboration_minutes", "01", "02", 45)]
    with httpx.Client(base_url=app_url() + "/api", timeout=30.0,
                      headers={"Authorization": f"Bearer {secret}"}) as c:
        for meter, start, end, quantity in rows:
            expect(c.post("/usage/intervals", json={
                "room_id": room, "meter": meter,
                "interval_start": f"2026-10-01T{start}:00:00Z",
                "interval_end": f"2026-10-01T{end}:00:00Z", "quantity": quantity}), 201)
    usage = expect(admin.get(f"/environments/{env}/usage", params={"period": "2026-10"}), 200)
    meters = {m["meter"]: m for m in usage["meters"]}
    assert meters["data_stored_gb"]["quantity"] == 10, (
        f"a steady ten gigabyte store sampled three times billed "
        f"{meters['data_stored_gb']['quantity']}; a level was accumulated")
    assert meters["data_stored_gb"]["amount_minor"] == 150
    assert meters["file_storage_gb"]["quantity"] == 4 and meters["file_storage_gb"]["amount_minor"] == 60
    assert meters["collaboration_minutes"]["quantity"] == 75
    assert meters["collaboration_minutes"]["amount_minor"] == 15
    for meter, rate in RATE_MINOR_PER_MILLION.items():
        if meter in meters:
            assert meters[meter]["rate_minor_per_million"] == rate


def test_invoice_total_equals_sum_of_visible_lines_record(clients):
    owner = clients.member(OWNER)
    invoice = expect(owner.get(f"/organisations/{ORG}/invoices/{SEED_PERIOD}"), 200)
    assert invoice.get("currency") == "usd"
    lines = invoice["lines"]
    amounts = [l["amount_minor"] for l in lines]
    assert all(isinstance(a, int) and not isinstance(a, bool) for a in amounts), amounts
    assert invoice["total_minor"] == sum(amounts), (
        f"the invoice total {invoice['total_minor']} is not the sum of its own lines "
        f"{sum(amounts)}")
    by_kind = {}
    for l in lines:
        by_kind.setdefault(l["kind"], []).append(l)
    assert [l["amount_minor"] for l in by_kind["plan_fee"]] == [SEED_PLAN_FEE]
    assert [l["amount_minor"] for l in by_kind["credit"]] == [SEED_CREDIT]
    meters = {l["meter"]: l["amount_minor"] for l in by_kind["meter"]}
    for fixed in ("data_stored_gb", "file_storage_gb", "custom_notifications"):
        assert meters.get(fixed) == SEED_METER_AMOUNTS[fixed], (fixed, meters)
    for grows in ("collaboration_minutes", "comments_created", "storage_updates"):
        assert SEED_METER_AMOUNTS[grows] <= meters.get(grows, -1) <= SEED_METER_AMOUNTS[grows] + 100
    seats = sum(l["amount_minor"] for l in by_kind["seats"])
    drift = sum(meters[m] - SEED_METER_AMOUNTS[m] for m in SEED_METER_AMOUNTS)
    assert invoice["total_minor"] == SEED_INVOICE_WITHOUT_SEATS + seats + drift, (
        "the invoice total does not reconcile with the seeded plan fee, meters and credit")


def test_money_amounts_are_integer_minor_units(clients):
    owner = clients.member(OWNER)
    raw = owner.get(f"/organisations/{ORG}/invoices/{SEED_PERIOD}").text
    assert not re.search(r'"(amount_minor|total_minor|rate_minor_per_million)"\s*:\s*-?\d+\.\d',
                         raw), f"a money field is not an integer: {raw[:400]}"
    env = environment_id(owner, ORG, ATLAS, "production")
    usage = owner.get(f"/environments/{env}/usage", params={"period": SEED_PERIOD}).text
    assert not re.search(r'"(amount_minor|rate_minor_per_million)"\s*:\s*-?\d+\.\d', usage)
    table = expect(clients.anon().get("/entitlements"), 200)["items"]
    fees = [e["value"] for e in table if e["key"] == "seat_overage_minor"]
    assert fees and all(isinstance(v, int) for v in fees), fees


def test_concurrent_identical_usage_intervals_store_one_row(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    room = new_room(admin, env, [READ])
    payload = {"room_id": room, "meter": "storage_updates",
               "interval_start": "2026-10-02T00:00:00Z",
               "interval_end": "2026-10-02T01:00:00Z", "quantity": 1234}

    def post(_):
        with httpx.Client(base_url=app_url() + "/api", timeout=30.0,
                          headers={"Authorization": f"Bearer {secret}"}) as c:
            return c.post("/usage/intervals", json=payload)

    results = in_parallel(8, post)
    assert all(r.status_code in (200, 201) for r in results), [r.status_code for r in results]
    ids = {r.json().get("id") for r in results}
    assert len(ids) == 1, f"eight identical interval writes returned {len(ids)} identifiers"
    stored = walk(admin, f"/environments/{env}/usage/intervals",
                  {"room_id": room, "meter": "storage_updates"})
    assert len([i for i in stored if i.get("interval_start", "").startswith("2026-10-02T00:00")]) == 1, (
        f"a retried usage interval was stored {len(stored)} times; the customer is double billed")


def test_duplicate_usage_interval_with_different_quantity_conflict(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    room = new_room(admin, env, [READ])
    base = {"room_id": room, "meter": "comments_created",
            "interval_start": "2026-10-03T00:00:00Z", "interval_end": "2026-10-03T01:00:00Z"}
    with httpx.Client(base_url=app_url() + "/api", timeout=30.0,
                      headers={"Authorization": f"Bearer {secret}"}) as c:
        first = expect(c.post("/usage/intervals", json={**base, "quantity": 5}), 201)
        same = expect(c.post("/usage/intervals", json={**base, "quantity": 5}), 200)
        assert same.get("id") == first.get("id")
        clash = c.post("/usage/intervals", json={**base, "quantity": 6})
    assert clash.status_code == 409 and code_of(clash) == "usage_interval_conflict", clash.text[:200]
    stored = walk(admin, f"/environments/{env}/usage/intervals",
                  {"room_id": room, "meter": "comments_created"})
    assert [i.get("quantity") for i in stored] == [5]


def test_idempotent_room_creation_single_winner_one_event_stored(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    token = login_token(ADMIN)
    key = uid("idem")
    room_id = uid("doc-idem")

    def create(_):
        with httpx.Client(base_url=app_url() + "/api", timeout=30.0, headers={
                "Authorization": f"Bearer {token}", "Idempotency-Key": key}) as c:
            return c.post(f"/environments/{env}/rooms", json={"room_id": room_id})

    results = in_parallel(6, create)
    statuses = [r.status_code for r in results]
    assert all(s in (201, 409) for s in statuses) and 201 in statuses, statuses
    winners = {r.json().get("id") for r in results if r.status_code == 201}
    assert len(winners) == 1, f"one idempotency key created {len(winners)} rooms"
    replay = expect(admin.post(f"/environments/{env}/rooms", json={"room_id": room_id},
                               headers={"Idempotency-Key": key}), 201)
    assert replay.get("id") in winners, "a later repeat did not return the stored response"
    rooms = [r for r in walk(admin, f"/environments/{env}/rooms") if r.get("room_id") == room_id]
    assert len(rooms) == 1
    events = [e for e in walk(admin, f"/environments/{env}/events", {"type": "room.created"})
              if (e.get("data") or {}).get("room_id") == room_id]
    assert len(events) == 1, (
        f"a single room creation under one idempotency key produced {len(events)} "
        f"room.created events")


def test_idempotency_key_reused_with_different_body_conflict(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    key = uid("idem")
    first, second = uid("doc-first"), uid("doc-second")
    expect(admin.post(f"/environments/{env}/rooms", json={"room_id": first},
                      headers={"Idempotency-Key": key}), 201)
    clash = admin.post(f"/environments/{env}/rooms", json={"room_id": second},
                       headers={"Idempotency-Key": key})
    assert clash.status_code == 409 and code_of(clash) == "idempotency_key_reused", (
        f"reusing an idempotency key with a different body answered {clash.status_code}")
    assert admin.get(f"/environments/{env}/rooms/{second}/inspector").status_code == 404


def test_audit_chain_hashes_recompute_and_verify_record(clients):
    owner = clients.member(OWNER)
    events = audit_events(owner)
    assert len(events) >= 5, "the organisation's record is nearly empty"
    previous = ZERO_HASH
    for index, event in enumerate(events, start=1):
        for key in CHAIN_KEYS + ("prev_hash", "hash"):
            assert key in event, f"audit event {index} has no {key!r}"
        assert event["sequence"] == index, (
            f"event {index} carries sequence {event['sequence']}; the sequence has a gap or a "
            f"duplicate")
        assert event["prev_hash"] == previous, f"event {index} does not chain to its predecessor"
        assert event["hash"] == chain_hash(previous, event), (
            f"event {index}'s hash is not SHA-256 over its predecessor and its canonical payload")
        previous = event["hash"]
    assert expect(owner.get(f"/organisations/{ORG}/audit/verify"), 200).get("ok") is True


def test_tampered_audit_row_reported_at_its_sequence(clients, db):
    owner = clients.member(OWNER)
    events = audit_events(owner)
    target = events[len(events) // 2]
    original = target.get("reason")
    rows = rewrite_audit_reason(db, target["hash"], "tampered by the verifier")
    assert rows and rows[0]["reason"] == "tampered by the verifier", (
        "no audit_event row carries the hash the API returned; the record is not where the "
        "brief says it is")
    try:
        verdict = expect(owner.get(f"/organisations/{ORG}/audit/verify"), 200)
        assert verdict.get("ok") is False and verdict.get("first_break") == target["sequence"], (
            f"an event edited in the store at sequence {target['sequence']} was reported as "
            f"{verdict}")
    finally:
        rewrite_audit_reason(db, target["hash"], original)
    assert expect(owner.get(f"/organisations/{ORG}/audit/verify"), 200).get("ok") is True


def test_audit_sequence_gapless_under_concurrent_writes_count(clients):
    admin = clients.member(ADMIN)
    owner = clients.member(OWNER)
    space = new_project(admin)
    token = login_token(ADMIN)

    def create(_):
        with httpx.Client(base_url=app_url() + "/api", timeout=30.0,
                          headers={"Authorization": f"Bearer {token}"}) as c:
            return c.post(f"/environments/{space['development']}/keys",
                          json={"kind": "secret", "label": uid("burst")})

    made = in_parallel(12, create)
    assert [r.status_code for r in made] == [201] * 12
    key_ids = {r.json()["id"] for r in made}
    events = audit_events(owner)
    sequences = [e["sequence"] for e in events]
    assert sequences == list(range(1, len(events) + 1)), (
        "after twelve concurrent audited writes the sequence is not gapless and unique: "
        f"{[s for s in sequences if sequences.count(s) > 1][:5]}")
    audited = {e["resource_id"] for e in events if e.get("action") == "key.created"}
    assert key_ids <= audited, f"{len(key_ids - audited)} key creations were not audited"


def test_application_credential_cannot_update_audit_rows(clients):
    owner = clients.member(OWNER)
    target = audit_events(owner)[-1]
    app_db = app_backend()
    assert app_db.query("SELECT 1 AS ok") == [{"ok": 1}], "the application credential cannot connect"
    try:
        touched = app_db.query(
            "UPDATE audit_event SET reason = reason WHERE hash = %s RETURNING hash",
            (target["hash"],))
    except Exception as exc:
        touched = []
        assert str(exc), "the refusal carried no reason"
    assert touched == [], (
        "the credential the application holds at DATABASE_URL updated an audit_event row; the "
        "tamper evidence is decorative")
    assert expect(owner.get(f"/organisations/{ORG}/audit/verify"), 200).get("ok") is True


def test_legal_hold_refuses_owner_deletion_everywhere(clients):
    owner = clients.member(OWNER)
    admin = clients.member(ADMIN)
    env = environment_id(owner, ORG, ATLAS, "production")
    secret = new_secret(admin, env)["secret"]
    by_owner = owner.delete(f"/environments/{env}/rooms/doc-hollow-dispute")
    with httpx.Client(base_url=app_url() + "/api", timeout=30.0,
                      headers={"Authorization": f"Bearer {secret}"}) as c:
        by_service = c.delete(f"/environments/{env}/rooms/doc-hollow-dispute")
    for label, r in (("owner", by_owner), ("service credential", by_service)):
        assert r.status_code == 409 and code_of(r) == "legal_hold", (
            f"deleting a held room as {label} answered {r.status_code}: {r.text[:200]}")
        assert r.json().get("hold") == SEED_HOLD
    assert room_record(owner, env, "doc-hollow-dispute")["room_id"] == "doc-hollow-dispute"


def test_retry_ladder_and_replay_keep_event_identifier(clients):
    owner = clients.member(OWNER2)
    env = environment_id(owner, OTHER_ORG, TETRAD, "production")
    endpoint = expect(owner.post(f"/environments/{env}/webhook-endpoints", json={
        "url": f"https://{CONSUMER_HOST}/{uid('ladder')}", "events": ["room.created"]}), 201)
    room = new_room(owner, env, [])
    path = f"/webhook-endpoints/{endpoint['id']}/deliveries"

    def mine(items):
        return [d for d in items if json.loads(d["body"]).get("data", {}).get("room_id") == room]

    two = poll(lambda: mine(walk(owner, path)),
               lambda ds: {d.get("attempt") for d in ds} >= {1, 2}, 30.0, 1.0)
    attempts = {d["attempt"]: d for d in two}
    assert {1, 2} <= set(attempts), f"the failing delivery was not retried: {attempts.keys()}"
    first, second = attempts[1], attempts[2]
    assert first["event_id"] == second["event_id"], "a retry changed the event identifier"
    gap1 = (parse_instant(first["next_attempt_at"]) - parse_instant(first["attempted_at"])).total_seconds()
    gap2 = (parse_instant(second["next_attempt_at"]) - parse_instant(second["attempted_at"])).total_seconds()
    assert 4 <= gap1 <= 7, f"the second attempt was scheduled {gap1}s after the first, not 5s"
    assert 290 <= gap2 <= 310, f"the third attempt was scheduled {gap2}s after the second, not 5m"
    replay = expect(owner.post(f"/webhook-deliveries/{first['id']}/replay"), 201)
    assert replay.get("event_id") == first["event_id"], "a replay minted a new event identifier"



def test_cursor_walk_returns_every_room_once_during_concurrent_inserts(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    originals = {new_room(admin, env, []) for _ in range(40)}
    token = login_token(ADMIN)
    seen: list[str] = []
    pages: list[dict] = []

    def walker(_):
        with httpx.Client(base_url=app_url() + "/api", timeout=30.0,
                          headers={"Authorization": f"Bearer {token}"}) as c:
            cursor = None
            for _ in range(60):
                params = {"limit": 7, **({"cursor": cursor} if cursor else {})}
                page = c.get(f"/environments/{env}/rooms", params=params).json()
                pages.append(page)
                seen.extend(r["room_id"] for r in page.get("items", []))
                cursor = page.get("next_cursor")
                if not cursor:
                    return "done"
            return "unfinished"

    def writer(_):
        with httpx.Client(base_url=app_url() + "/api", timeout=30.0,
                          headers={"Authorization": f"Bearer {token}"}) as c:
            for _ in range(25):
                c.post(f"/environments/{env}/rooms", json={"room_id": uid("doc-late")})
        return "written"

    outcome = in_parallel(2, lambda i: walker(i) if i == 0 else writer(i))
    assert outcome[0] == "done"
    repeated = sorted({r for r in seen if seen.count(r) > 1})
    missing = sorted(originals - set(seen))
    assert not repeated and not missing, (
        f"walking by cursor while rooms were inserted repeated {len(repeated)} and skipped "
        f"{len(missing)} rooms")
    assert pages[-1].get("has_more") is False
    assert all(p.get("page_size") == 7 for p in pages)


def test_paginated_response_shape_and_limit_bounds(clients):
    admin = clients.member(ADMIN)
    env = environment_id(admin, ORG, ATLAS, "production")
    page = expect(admin.get(f"/environments/{env}/rooms", params={"limit": 2}), 200)
    assert page.get("page_size") == 2 and len(page.get("items", [])) == 2
    assert page.get("has_more") is True and isinstance(page.get("next_cursor"), str)
    assert "total_count" not in page, "a large collection returned a total count"
    default = expect(admin.get(f"/environments/{env}/usage/intervals"), 200)
    assert default.get("page_size") == 20
    for bad in (0, 101):
        r = admin.get(f"/environments/{env}/rooms", params={"limit": bad})
        assert r.status_code == 422, f"limit={bad} answered {r.status_code}"


def test_request_id_echoed_in_header_and_error_body(clients):
    rid = uid("rid-echo")
    anon = clients.anon()
    health = anon.get("/health", headers={"X-Request-Id": rid})
    assert health.status_code == 200
    assert health.headers.get("X-Request-Id") == rid, "a supplied request identifier was replaced"
    assert anon.get("/health").headers.get("X-Request-Id"), "a response carries no X-Request-Id"
    admin = clients.member(ADMIN)
    missing = admin.get(f"/approvals/{uid('req')}", headers={"X-Request-Id": rid})
    assert missing.status_code == 404
    assert missing.json().get("request_id") == rid, "the error body does not carry the request_id"
    assert missing.headers.get("X-Request-Id") == rid


def test_denials_and_inspector_reads_audited_with_request_id(clients):
    owner = clients.member(OWNER)
    admin = clients.member(ADMIN)
    analyst = clients.member(ANALYST)
    env = environment_id(admin, ORG, ATLAS, "production")
    denied_rid, read_rid = uid("rid-deny"), uid("rid-read")
    refused = analyst.post(f"/organisations/{ORG}/approvals", headers={"X-Request-Id": denied_rid},
                           json={"action": "room.delete_production", "reason": "denied probe",
                                 "arguments": {"environment_id": env, "room_id": "doc-almanac-brief"}})
    assert refused.status_code == 403
    assert refused.headers.get("X-Request-Id") == denied_rid
    expect(admin.get(f"/environments/{env}/rooms/doc-almanac-brief/inspector",
                     headers={"X-Request-Id": read_rid}), 200)
    denial = find_event(owner, denied_rid)
    assert denial and denial[0].get("outcome") == "denied" and denial[0].get("reason") == "forbidden", (
        f"a refused request left no denied audit event with its rule: {denial}")
    read = [e for e in find_event(owner, read_rid) if e.get("action") == "room.inspected"]
    assert read and read[0].get("resource_id") == "doc-almanac-brief", (
        "opening the inspector, a read of customer content, was not audited")


def test_environment_kind_and_region_immutable_second_production_conflict(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    again = admin.post(f"/projects/{space['project']}/environments",
                       json={"kind": "production", "region": "us-east"})
    assert again.status_code == 409 and code_of(again) == "environment_exists"
    moved = admin.patch(f"/environments/{space['production']}", json={"region": "us-east"})
    assert moved.status_code == 409 and code_of(moved) == "environment_immutable", moved.text[:200]
    project = [p for p in walk(admin, f"/organisations/{ORG}/projects") if p["slug"] == space["slug"]][0]
    assert sorted((e["kind"], e["region"]) for e in project["environments"]) == [
        ("development", "eu-west"), ("production", "eu-west")]


def test_private_or_plaintext_destinations_refused_invalid(clients):
    owner = clients.member(OWNER2)
    env = environment_id(owner, OTHER_ORG, TETRAD, "production")
    for url in ("https://127.0.0.1/hook", "https://10.20.30.40/hook", "https://192.168.4.4/hook",
                "https://172.16.9.9/hook", "https://localhost/hook",
                f"http://{CONSUMER_HOST}/hook"):
        r = owner.post(f"/environments/{env}/webhook-endpoints",
                       json={"url": url, "events": ["room.created"]})
        assert r.status_code == 422, f"the destination {url} was accepted ({r.status_code})"
        assert "url" in (r.json().get("fields") or {}), r.text[:200]


def test_document_change_events_collapse_per_room_not_globally(clients):
    owner = clients.member(OWNER2)
    env = environment_id(owner, OTHER_ORG, TETRAD, "production")
    secret = new_secret(owner, env)["secret"]
    endpoint = expect(owner.post(f"/environments/{env}/webhook-endpoints", json={
        "url": f"https://{CONSUMER_HOST}/{uid('collapse')}", "events": ["storage.updated"]}), 201)
    busy, quiet = new_room(owner, env, [READ, WRITE]), new_room(owner, env, [READ, WRITE])
    b = connect(secret, uid("eu-busy"), busy)
    q = connect(secret, uid("eu-quiet"), quiet)
    for _ in range(5):
        assert operate(b.token, b.id, "storage.write").status_code == 202
    assert operate(q.token, q.id, "storage.write").status_code == 202

    def events_for(room):
        items = walk(owner, f"/webhook-endpoints/{endpoint['id']}/deliveries")
        return {d["event_id"] for d in items if d.get("event_type") == "storage.updated"
                and json.loads(d["body"]).get("data", {}).get("room_id") == room}

    poll(lambda: (events_for(busy), events_for(quiet)), lambda p: p[0] and p[1], 15.0, 1.0)
    settle(3)
    busy_events, quiet_events = events_for(busy), events_for(quiet)
    assert len(busy_events) == 1, (
        f"five changes inside one interval produced {len(busy_events)} events for the busy room")
    assert len(quiet_events) == 1, (
        f"the quiet room produced {len(quiet_events)} events; the collapse is global, not per room")


def test_webhook_signature_covers_timestamp_and_body_record(clients):
    owner = clients.member(OWNER2)
    env = environment_id(owner, OTHER_ORG, TETRAD, "production")
    endpoint = expect(owner.post(f"/environments/{env}/webhook-endpoints", json={
        "url": f"https://{CONSUMER_HOST}/{uid('sig')}", "events": ["room.created"]}), 201)
    assert endpoint.get("secret") and endpoint.get("verified") is False
    room = new_room(owner, env, [])
    deliveries = poll(lambda: [d for d in walk(owner, f"/webhook-endpoints/{endpoint['id']}/deliveries")
                               if json.loads(d["body"]).get("data", {}).get("room_id") == room],
                      lambda ds: bool(ds), 20.0, 1.0)
    assert deliveries, "creating a room produced no delivery within twenty seconds"
    d = deliveries[-1]
    parts = dict(p.split("=", 1) for p in d["signature"].split(","))
    assert parts.get("t") == str(d["signed_timestamp"])
    assert parts.get("v1") == hmac_hex(endpoint["secret"], f"{parts['t']}.{d['body']}"), (
        "the signature is not HMAC-SHA256 over the timestamp and the body")
    assert parts.get("v1") != hmac_hex(endpoint["secret"], d["body"])
    envelope = json.loads(d["body"])
    assert envelope.get("id") == d["event_id"] and envelope.get("type") == "room.created"


def test_unknown_address_renders_not_found_page_with_404():
    with site() as s:
        r = s.get(f"/{uid('no-such-page')}")
    assert r.status_code == 404, f"an unknown address answered {r.status_code}, not 404"
    assert "text/html" in r.headers.get("content-type", "")
    assert NOT_FOUND_HEADING in r.text
    assert re.search(r'href=["\']/["\']', r.text), "the not-found page offers no way back home"


def test_favicon_served_and_declared_in_every_head():
    with site() as s:
        icon = s.get("/favicon.ico")
        assert icon.status_code == 200 and icon.headers.get("content-type", "").startswith("image/")
        assert len(icon.content) > 0
        for route in ("/", "/pricing", "/privacy", "/terms", "/contact", "/auth/login"):
            r = s.get(route)
            assert r.status_code in (200, 401), f"{route} answered {r.status_code}"
            head = r.text.split("</head>")[0].lower()
            assert re.search(r'<link[^>]+rel=["\'][^"\']*icon', head), f"{route} declares no favicon"


def test_content_images_carry_alternative_text():
    class Images(HTMLParser):
        def __init__(self):
            super().__init__()
            self.imgs, self.svgs, self._open = [], [], []

        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            if tag == "img":
                self.imgs.append(a)
            if tag == "svg":
                self.svgs.append(a)
                self._open.append(a)
            if tag == "title" and self._open:
                self._open[-1]["aria-label"] = self._open[-1].get("aria-label") or "title"

        def handle_endtag(self, tag):
            if tag == "svg" and self._open:
                self._open.pop()

    graphics = 0
    with site() as s:
        for route in ("/", "/pricing", "/enterprise"):
            parser = Images()
            parser.feed(s.get(route).text)
            for img in parser.imgs:
                assert "alt" in img, f"an image on {route} has no alternative text: {img}"
            for svg in parser.svgs:
                named = (svg.get("aria-hidden") == "true" or svg.get("aria-label")
                         or svg.get("aria-labelledby") or svg.get("role") in ("presentation", "none"))
                assert named, f"a graphic on {route} is neither named nor declared decorative: {svg}"
            graphics += len(parser.imgs) + len(parser.svgs)
    assert graphics >= 3, "the public routes carry almost no graphics, so nothing was checked"


def test_body_text_contrast_and_narrow_viewport_hold():
    script = """() => {
      const parse = c => (c.match(/[\\d.]+/g) || []).map(Number);
      const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
      const ground = el => { for (let n = el; n; n = n.parentElement) { const p = parse(getComputedStyle(n).backgroundColor);
        if (p.length === 3 || (p.length === 4 && p[3] > 0.5)) return p.slice(0, 3); } return [255, 255, 255]; };
      return [...document.querySelectorAll('main p')].filter(p => p.innerText.trim().length > 20 && p.offsetParent)
        .map(p => { const a = lum(parse(getComputedStyle(p).color)), b = lum(ground(p));
          return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); });
    }"""
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            wide = browser.new_page(viewport={"width": 1440, "height": 900})
            wide.goto(app_url() + "/pricing", wait_until="networkidle")
            ratios = wide.evaluate(script)
            assert len(ratios) >= 3, "the pricing route has almost no body paragraphs to measure"
            low = [round(r, 2) for r in ratios if r < 4.5]
            assert not low, f"body paragraphs fall below the AA contrast bar: {low}"
            narrow = browser.new_page(viewport={"width": 390, "height": 844})
            for route in ("/", "/pricing"):
                narrow.goto(app_url() + route, wait_until="networkidle")
                overflow = narrow.evaluate(
                    "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                assert overflow <= 1, f"{route} scrolls sideways by {overflow}px at 390px"
        finally:
            browser.close()


def test_no_credential_in_anything_the_browser_downloads():
    fetched = 0
    with site() as s:
        for route in ("/", "/pricing", "/auth/login"):
            page = s.get(route)
            texts = [page.text]
            for src in re.findall(r'<script[^>]+src=["\']([^"\']+)', page.text):
                url = urljoin(app_url() + route, src)
                if urlparse(url).netloc == urlparse(app_url()).netloc:
                    texts.append(s.get(url).text)
                    fetched += 1
            for text in texts:
                for literal in SECRET_LITERALS + ("postgresql://",):
                    assert literal not in text, f"{literal!r} is shipped to the browser from {route}"


def test_entitlement_change_moves_pricing_matrix_cell(clients):
    owner = clients.member(OWNER)

    def cell(html, key):
        return entitlement_cells(html).get(key)

    try:
        set_entitlement(owner, "enterprise", "connections_per_room", 37)
        with site() as s:
            html = s.get("/pricing").text
        assert cell(html, "enterprise.connections_per_room") == "37", (
            f"after the entitlement moved to 37 the matrix reads "
            f"{cell(html, 'enterprise.connections_per_room')!r}; it is written by hand or cached")
        assert cell(html, "team.connections_per_room") == "50"
    finally:
        set_entitlement(owner, "enterprise", "connections_per_room", ENTERPRISE_CONNECTIONS)
    with site() as s:
        assert cell(s.get("/pricing").text, "enterprise.connections_per_room") == "100"


def test_enquiry_decoy_too_fast_and_rate_limit_nothing_stored(clients):
    anon = clients.anon()
    marker = uid("enquiry")
    tokens = [expect(anon.get("/enquiries/form"), 200)["form_token"] for _ in range(5)]

    def form(token, note, decoy=""):
        return {"form_token": token, "first_name": "Verifier", "last_name": "Probe",
                "work_email": f"{note}@example.com", "company_size": "51-200",
                "role": "Engineering", "interest": f"{marker} {note}", "website": "",
                "role_title": decoy}

    hasty = anon.post("/enquiries", json=form(tokens[0], "hasty"))
    assert hasty.status_code == 422 and code_of(hasty) == "submitted_too_fast", hasty.text[:200]
    settle(2.5)
    bot = anon.post("/enquiries", json=form(tokens[1], "bot", decoy="Head of automation"))
    assert bot.status_code == 422 and code_of(bot) == "spam_refused", bot.text[:200]
    for i, token in enumerate(tokens[2:5]):
        expect(anon.post("/enquiries", json=form(token, f"human{i}")), 201)
    late = expect(anon.get("/enquiries/form"), 200)["form_token"]
    settle(2.5)
    limited = anon.post("/enquiries", json=form(late, "fourth"))
    assert limited.status_code == 429 and code_of(limited) == "rate_limited", (
        f"a fourth accepted enquiry inside a minute answered {limited.status_code}")

    owner = clients.member(OWNER)
    stored = [e for e in walk(owner, "/enquiries", max_pages=5) if marker in json.dumps(e)]
    notes = sorted(e.get("interest", "").split()[-1] for e in stored)
    assert notes == ["human0", "human1", "human2"], (
        f"refused enquiries were recorded, or accepted ones were lost: {notes}")



def test_approval_requested_email_reaches_each_eligible_approver_except_requester(clients, mailbox):
    admin = clients.member(ADMIN)
    env = environment_id(admin, ORG, ATLAS, "production")
    room = new_room(admin, env, [])
    request = raise_request(admin, "room.default_access_public",
                            {"environment_id": env, "room_id": room}, "mail probe")
    subject = "Roomstack approval requested: room.default_access_public"
    found = wait_for_mail(mailbox, request["id"],
                          lambda m: ADMIN2 in m["to"] and m["subject"].startswith(subject))
    assert any(ADMIN2 in m["to"] and m["subject"].startswith(subject) for m in found), (
        "the other eligible approver was not mailed about a pending request")
    settle(5)
    messages = [m for m in mailbox.mentioning(request["id"]) if m["subject"].startswith(subject)]
    recipients = sorted(a for m in messages for a in m["to"])
    assert recipients == [ADMIN2], (
        f"the approval request went to {recipients}; exactly the eligible approvers other than "
        f"the requester should be told")
    assert all(m["text"].strip().startswith(request["id"]) for m in messages), (
        "an approval message does not open with the request identifier on its own line")


def test_impact_growth_renotifies_eligible_approvers_by_email(impact_growth_scenario, mailbox):
    request_id = impact_growth_scenario["request"]["id"]
    subject = "Roomstack approval requested: room.default_access_public"

    def twice(messages):
        return sum(1 for m in messages if ADMIN2 in m["to"] and m["subject"].startswith(subject)) >= 2

    found = poll(lambda: mailbox.mentioning(request_id), twice, 75.0, 2.0)
    for approver in (ADMIN, ADMIN2):
        count = sum(1 for m in found if approver in m["to"] and m["subject"].startswith(subject))
        assert count >= 2, (
            f"{approver} was told about the request {count} time(s); the return to pending after "
            f"the impact grew must reach every eligible approver again")


def test_expiry_email_reaches_requester_exactly_once(expiry_scenario, mailbox):
    silent_id = expiry_scenario["silent"]["id"]
    subject = "Roomstack approval expired: room.delete_production"
    found = wait_for_mail(mailbox, silent_id,
                          lambda m: OWNER2 in m["to"] and m["subject"].startswith(subject), 90.0)
    assert any(OWNER2 in m["to"] and m["subject"].startswith(subject) for m in found), (
        "a request nobody read after it expired never told its requester; expiry is silence")
    settle(35)
    count = sum(1 for m in mailbox.mentioning(silent_id)
                if OWNER2 in m["to"] and m["subject"].startswith(subject))
    assert count == 1, f"the requester was told about one expiry {count} times"


def test_executed_revocation_sends_no_transition_email(revocation_scenario, mailbox):
    request_id = revocation_scenario["request"]["id"]
    granted = wait_for_mail(mailbox, request_id,
                            lambda m: DEVELOPER in m["to"]
                            and m["subject"].startswith("Roomstack approval granted: group.revoke_access"))
    assert granted, "the requester was never told the revocation was approved"
    settle(5)
    messages = mailbox.mentioning(request_id)
    subjects = sorted((m["subject"].split(":")[0], tuple(m["to"])) for m in messages)
    expected = sorted([("Roomstack approval granted", (DEVELOPER,)),
                       ("Roomstack approval requested", (ADMIN,)),
                       ("Roomstack approval requested", (ADMIN2,))])
    assert subjects == expected, (
        f"executing an approved request sent mail it must not: {subjects}")


def test_break_glass_second_factor_code_arrives_by_email_and_executes(break_glass_scenario, clients):
    s = break_glass_scenario
    assert s["challenge"].status_code == 202
    assert s["code_message"], "no second factor code reached the owner's inbox"
    assert s["code"], "the second factor message carries no six digit code"
    used = expect(s["used"], 200)
    assert (used.get("approval") or {}).get("status") == "executed", used
    owner = clients.member(OWNER)
    assert room_record(owner, s["env"], s["room"])["default_accesses"] == [READ]


def test_break_glass_notifies_every_owner_and_approver_by_email(break_glass_scenario, mailbox):
    approval_id = (break_glass_scenario["used"].json().get("approval") or {}).get("id")
    assert approval_id
    subject = "Roomstack break glass used: room.default_access_public"
    wanted = {OWNER, ADMIN, ADMIN2}

    def everyone(messages):
        told = {a for m in messages if m["subject"].startswith(subject) for a in m["to"]}
        return wanted <= told

    found = poll(lambda: mailbox.mentioning(approval_id), everyone, 75.0, 2.0)
    told = {a for m in found if m["subject"].startswith(subject) for a in m["to"]}
    assert wanted <= told, f"break glass was announced to {sorted(told)}, not every owner and approver"


def test_two_executions_of_one_approved_request_arriving_together_run_it_once(clients):
    admin = clients.member(ADMIN)
    admin2 = clients.member(ADMIN2)
    developer = clients.member(DEVELOPER)
    env = new_project(admin)["production"]
    room = new_room(admin, env, [])
    arguments = {"environment_id": env, "room_id": room}
    request = raise_request(developer, "room.default_access_public", arguments,
                            "concurrent execution probe")
    expect(decide(admin, request["id"]), 201)
    marks = [uid("rq-exec"), uid("rq-exec")]
    executors = [admin, admin2]
    results = in_parallel(2, lambda i: executors[i].post(
        f"/approvals/{request['id']}/execute", json={"arguments": arguments},
        headers={"X-Request-Id": marks[i]}))
    statuses = sorted(r.status_code for r in results)
    assert statuses == [200, 409], (
        f"two executions of one approved request arriving together answered {statuses}; "
        f"exactly one may run and the other is refused because the request is no longer "
        f"approved")
    loser = next(r for r in results if r.status_code == 409)
    assert code_of(loser) == "request_not_approved", loser.text[:300]
    assert get_request(admin, request["id"])["status"] == "executed"
    assert room_record(admin, env, room)["default_accesses"] == [READ]
    owner = clients.member(OWNER)
    ran = [e for mark in marks for e in find_event(owner, mark)
           if e.get("action") == "approval.executed" and e.get("outcome") == "allowed"]
    assert len(ran) == 1, (
        f"the audit record shows {len(ran)} allowed approval.executed events for one "
        f"request; the change ran more than once")


def test_two_approvals_landing_together_are_both_recorded(clients):
    admin = clients.member(ADMIN)
    admin2 = clients.member(ADMIN2)
    developer = clients.member(DEVELOPER)
    space = new_project(admin)
    request = raise_request(developer, "project.delete", {"project_id": space["project"]},
                            "concurrent decision probe")
    deciders = [admin, admin2]
    results = in_parallel(2, lambda i: decide(deciders[i], request["id"]))
    assert [r.status_code for r in results] == [201, 201], (
        f"two distinct approvers deciding together answered "
        f"{[r.status_code for r in results]}: {[r.text[:120] for r in results]}")
    final = get_request(admin, request["id"])
    approvers = sorted(d.get("approver") for d in final.get("decisions") or []
                       if d.get("decision") == "approved")
    assert approvers == sorted([ADMIN, ADMIN2]), (
        f"two approvals landed together and the request records {approvers}; one "
        f"decision overwrote the other")
    assert final["status"] == "approved", final["status"]


def test_simultaneous_admissions_at_the_ceiling_admit_exactly_the_ceiling(clients):
    owner = clients.member(OWNER)
    admin = clients.member(ADMIN)
    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    room = new_room(admin, env, [READ, WRITE])
    set_entitlement(owner, "enterprise", "connections_per_room", 3)
    try:
        tokens = [identity_token(secret, uid("eu-race")) for _ in range(8)]

        def admit(index):
            with http(tokens[index]) as c:
                return c.post("/rt/connections", json={"room_id": room})

        results = in_parallel(8, admit)
        statuses = sorted(r.status_code for r in results)
        assert statuses.count(201) == 3 and statuses.count(409) == 5, (
            f"eight admissions arriving together at a ceiling of 3 answered {statuses}; "
            f"exactly three may be admitted")
        for r in results:
            if r.status_code == 409:
                assert code_of(r) == "room_full", r.text[:200]
        capacity = expect(admin.get(f"/environments/{env}/rooms/{room}/capacity"), 200)
        assert capacity.get("open_connections") == 3, capacity
        listed = walk(admin, "/rt/connections", {"room_id": room})
        assert len([c for c in listed if not c.get("closed_at")]) == 3, listed
    finally:
        set_entitlement(owner, "enterprise", "connections_per_room", ENTERPRISE_CONNECTIONS)


def test_admission_resolves_the_room_in_the_token_environment(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    room_id = uid("doc-twin")
    for kind, accesses in (("development", [READ, WRITE]), ("production", [])):
        expect(admin.post(f"/environments/{space[kind]}/rooms", json={
            "room_id": room_id, "classification": "standard",
            "default_accesses": accesses}), 201)
    dev_secret = new_secret(admin, space["development"])["secret"]
    prod_secret = new_secret(admin, space["production"])["secret"]
    dev = connect(dev_secret, uid("eu-twin"), room_id)
    assert dev.status == 201 and {READ, WRITE} <= set(dev.payload.get("accesses") or []), (
        f"a development token admitted to the development room answered {dev.status} "
        f"{dev.payload}")
    assert operate(dev.token, dev.id, "storage.write").status_code == 202
    prod = connect(prod_secret, uid("eu-twin"), room_id)
    assert prod.status == 403 and prod.payload.get("code") == "room_access_denied", (
        f"a production token for the private production room of the same identifier "
        f"answered {prod.status} {prod.payload}; the room was looked up outside the "
        f"token's environment")
    with http(dev_secret) as c:
        record = expect(c.get(f"/rt/connections/{dev.id}"), 200)
    assert record.get("room_id") == room_id and record.get("closed_at") is None, record


def test_one_interval_start_in_two_environments_is_two_intervals(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    room_id = uid("doc-meter")
    ids = {}
    for kind, quantity in (("development", 7), ("production", 9)):
        env = space[kind]
        expect(admin.post(f"/environments/{env}/rooms", json={
            "room_id": room_id, "classification": "standard", "default_accesses": []}), 201)
        secret = new_secret(admin, env)["secret"]
        with http(secret) as c:
            written = c.post("/usage/intervals", json={
                "room_id": room_id, "meter": "comments_created",
                "interval_start": "2026-07-01T00:00:00Z",
                "interval_end": "2026-07-01T00:01:00Z", "quantity": quantity})
        assert written.status_code == 201, (
            f"the {kind} interval answered {written.status_code}: {written.text[:200]}; the "
            f"natural key includes the key's environment, so the same room identifier and "
            f"start in another environment is a different interval")
        ids[kind] = written.json().get("id")
        usage = expect(admin.get(f"/environments/{env}/usage", params={"period": "2026-07"}), 200)
        meters = {m.get("meter"): m for m in usage.get("meters") or []}
        assert (meters.get("comments_created") or {}).get("quantity") == quantity, (
            f"the {kind} environment reads {meters.get('comments_created')} for its own "
            f"interval of {quantity}")
    assert ids["development"] and ids["development"] != ids["production"], ids


def test_meter_charges_round_half_up_once_per_line_in_minor_units(clients):
    admin = clients.member(ADMIN)
    env = new_project(admin)["production"]
    room = new_room(admin, env, [])
    secret = new_secret(admin, env)["secret"]
    writes = ([("custom_notifications", 1)] * 5
              + [("storage_updates", 2500), ("storage_updates", 2500),
                 ("collaboration_minutes", 13)])
    with http(secret) as c:
        for index, (meter, quantity) in enumerate(writes):
            expect(c.post("/usage/intervals", json={
                "room_id": room, "meter": meter,
                "interval_start": f"2026-08-01T00:{index:02d}:00Z",
                "interval_end": f"2026-08-01T00:{index:02d}:30Z",
                "quantity": quantity}), 201)
    usage = expect(admin.get(f"/environments/{env}/usage", params={"period": "2026-08"}), 200)
    meters = {m.get("meter"): m for m in usage.get("meters") or []}
    expected = {"custom_notifications": (5, 3), "storage_updates": (5000, 1),
                "collaboration_minutes": (13, 3)}
    for meter, (quantity, amount) in expected.items():
        line = meters.get(meter) or {}
        assert line.get("quantity") == quantity, (meter, line)
        assert line.get("amount_minor") == amount, (
            f"{meter} over a period quantity of {quantity} charges {line.get('amount_minor')}, "
            f"expected {amount}: the line is rounded half up once on the period quantity, "
            f"never per interval and never to the even neighbour")
        assert isinstance(line.get("amount_minor"), int)


def test_an_approved_deletion_of_a_held_room_is_refused_when_executed(clients):
    admin = clients.member(ADMIN)
    developer = clients.member(DEVELOPER)
    owner = clients.member(OWNER)
    env = environment_id(admin, ORG, ATLAS, "production")
    arguments = {"environment_id": env, "room_id": HELD_ROOM}
    request = raise_request(developer, "room.delete_production", arguments,
                            "held room deletion probe")
    expect(decide(admin, request["id"]), 201)
    ran = execute(admin, request["id"], arguments)
    assert ran.status_code == 409 and code_of(ran) == "legal_hold", (
        f"executing an approved deletion of a held room answered {ran.status_code}: "
        f"{ran.text[:300]}; an approval does not lift a hold")
    assert ran.json().get("hold") == SEED_HOLD
    assert get_request(admin, request["id"])["status"] == "approved"
    assert room_record(owner, env, HELD_ROOM)["room_id"] == HELD_ROOM


def test_break_glass_cannot_delete_a_held_room(break_glass_scenario):
    s = break_glass_scenario
    held = s["held"]
    assert held.status_code == 409 and code_of(held) == "legal_hold", (
        f"break glass deleting a held room answered {held.status_code}: {held.text[:300]}; "
        f"an emergency path is not a way around a legal hold")
    assert held.json().get("hold") == SEED_HOLD
    assert s["held_inspector"].status_code == 200, (
        f"the held room no longer reads after break glass: {s['held_inspector'].status_code}")


def test_a_second_factor_code_only_serves_the_member_it_was_mailed_to(clients, mailbox):
    owner = clients.member(OWNER)
    owner2 = clients.member(OWNER2)
    admin = clients.member(ADMIN)
    env = environment_id(owner, ORG, ATLAS, "production")
    room = new_room(admin, env, [])
    known = mailbox.snapshot()
    expect(owner2.post("/auth/second-factor/challenge"), 202)

    def code_for_other(messages):
        for m in messages:
            if OWNER2 in m["to"] and "roomstack second factor code" in m["subject"].lower():
                return m
        return None

    found = poll(lambda: mailbox.since(known), lambda ms: code_for_other(ms) is not None,
                 75.0, 2.0)
    message = code_for_other(found)
    assert message, "no second factor code reached owner2@example.com"
    match = re.search(r"\b(\d{6})\b", message["subject"] + " " + message["text"])
    assert match, message
    borrowed = owner.post(f"/organisations/{ORG}/break-glass", json={
        "action": "room.default_access_public",
        "arguments": {"environment_id": env, "room_id": room},
        "reason": "verifier incident with another member's code",
        "second_factor_code": match.group(1)})
    assert borrowed.status_code == 403 and code_of(borrowed) == "second_factor_required", (
        f"break glass with a code mailed to a different member answered "
        f"{borrowed.status_code}: {borrowed.text[:300]}")
    assert room_record(owner, env, room)["default_accesses"] == []


def test_a_stale_version_marker_is_refused_with_the_current_room(clients):
    admin = clients.member(ADMIN)
    env = new_project(admin)["production"]
    room = new_room(admin, env, [])
    version = room_record(admin, env, room).get("version")
    assert version not in (None, ""), "a room carries no version marker"
    path = f"/environments/{env}/rooms/{room}/default-accesses"
    fresh = admin.put(path, json={"accesses": [READ]}, headers={"If-Match": str(version)})
    assert fresh.status_code == 200, fresh.text[:300]
    stale = admin.put(path, json={"accesses": [READ, WRITE]},
                      headers={"If-Match": str(version)})
    assert stale.status_code == 409 and code_of(stale) == "version_conflict", (
        f"an update presenting a stale version answered {stale.status_code}: "
        f"{stale.text[:300]}; the later write silently replaced the earlier one")
    current = stale.json().get("current") or {}
    assert current.get("default_accesses") == [READ], current
    assert str(current.get("version")) != str(version), current
    assert room_record(admin, env, room)["default_accesses"] == [READ]
    blind = admin.put(path, json={"accesses": [READ, WRITE]})
    assert blind.status_code == 200, blind.text[:300]
    assert room_record(admin, env, room)["default_accesses"] == [READ, WRITE]


def test_a_cursor_reused_under_another_filter_or_order_is_rejected(clients):
    admin = clients.member(ADMIN)
    owner = clients.member(OWNER)
    developer = clients.member(DEVELOPER)
    env = new_project(admin)["production"]
    for _ in range(3):
        raise_request(developer, "room.default_access_public",
                      {"environment_id": env, "room_id": new_room(admin, env, [])},
                      "cursor probe")
    path = f"/organisations/{ORG}/approvals"
    page = expect(admin.get(path, params={"status": "pending", "limit": 1}), 200)
    cursor = page.get("next_cursor")
    assert cursor, page
    moved = admin.get(path, params={"status": "approved", "limit": 1, "cursor": cursor})
    assert moved.status_code == 422 and code_of(moved) == "cursor_invalid", (
        f"a pending-filter cursor presented under the approved filter answered "
        f"{moved.status_code}: {moved.text[:200]}")
    same = admin.get(path, params={"status": "pending", "limit": 1, "cursor": cursor})
    assert same.status_code == 200, same.text[:200]
    audit = f"/organisations/{ORG}/audit"
    ascending = expect(owner.get(audit, params={"order": "asc", "limit": 1}), 200)
    flipped = owner.get(audit, params={"order": "desc", "limit": 1,
                                       "cursor": ascending.get("next_cursor")})
    assert flipped.status_code == 422 and code_of(flipped) == "cursor_invalid", (
        f"an ascending audit cursor presented in descending order answered "
        f"{flipped.status_code}: {flipped.text[:200]}")


def test_a_deleted_room_identifier_is_not_reused_within_a_day(clients):
    admin = clients.member(ADMIN)
    space = new_project(admin)
    dev = space["development"]
    room = new_room(admin, dev, [])
    gone = admin.delete(f"/environments/{dev}/rooms/{room}")
    assert gone.status_code == 204, gone.text[:200]
    again = admin.post(f"/environments/{dev}/rooms", json={
        "room_id": room, "classification": "standard", "default_accesses": []})
    assert again.status_code == 409 and code_of(again) == "room_id_unavailable", (
        f"recreating a room identifier deleted moments ago answered {again.status_code}: "
        f"{again.text[:200]}")
    elsewhere = admin.post(f"/environments/{space['production']}/rooms", json={
        "room_id": room, "classification": "standard", "default_accesses": []})
    assert elsewhere.status_code == 201, (
        f"the same identifier in another environment answered {elsewhere.status_code}; "
        f"identifiers are unique per environment")


def test_one_idempotency_key_in_two_organisations_is_two_writes(clients):
    admin = clients.member(ADMIN)
    owner2 = clients.member(OWNER2)
    key = uid("idem-shared")
    north_env = new_project(admin)["development"]
    page_env = environment_id(owner2, OTHER_ORG, TETRAD, "development")
    north_room, page_room = uid("doc-idem"), uid("doc-idem")
    first = admin.post(f"/environments/{north_env}/rooms", headers={"Idempotency-Key": key},
                       json={"room_id": north_room, "classification": "standard",
                             "default_accesses": []})
    assert first.status_code == 201, first.text[:200]
    second = owner2.post(f"/environments/{page_env}/rooms", headers={"Idempotency-Key": key},
                         json={"room_id": page_room, "classification": "standard",
                               "default_accesses": []})
    assert second.status_code == 201, (
        f"another organisation's first use of the key answered {second.status_code}: "
        f"{second.text[:300]}; an idempotency key is scoped to the credential presenting it")
    assert second.json().get("room_id") == page_room, second.text[:300]
    assert room_record(owner2, page_env, page_room)["room_id"] == page_room
    assert room_record(admin, north_env, north_room)["room_id"] == north_room
    peek = admin.get(f"/environments/{page_env}/rooms/{page_room}/inspector")
    assert peek.status_code == 404, peek.status_code

