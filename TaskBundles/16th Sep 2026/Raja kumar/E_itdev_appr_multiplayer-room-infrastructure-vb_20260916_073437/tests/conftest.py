"""Task fixtures for deku/multiplayer-room-infrastructure-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout
or module names. The assumptions are the App Contract (the app answers at
APP_PUBLIC_URL with its HTTP API under /api), the HTTP contract and the seeded
fixtures instruction.md pins, and the two verifier-side services the task
declares: the datastore at DB_ADMIN_URL and the Mailpit inbox API.

Every scenario that mutates state provisions its own project, environment,
room, group and end users, so nothing asserted here depends on what the browser
workflows did to the seeded Northlake Contractors group before pytest ran.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import math
import os
import re
import threading
import time
from datetime import datetime
from html.parser import HTMLParser

import httpx
import pytest
from appclient import api_base, app_url
from capabilities import PostgresBackend, make_backend, make_inbox

PASSWORD = "deku-demo-pw-2026"
ORG = "northlake"
OTHER_ORG = "pagewise"

OWNER = "owner@example.com"
ADMIN = "admin@example.com"
ADMIN2 = "admin2@example.com"
DEVELOPER = "developer@example.com"
DEVELOPER2 = "developer2@example.com"
CONTRACTOR = "contractor@example.com"
ANALYST = "analyst@example.com"
OWNER2 = "owner2@example.com"

ATLAS = "atlas-editor"
TETRAD = "tetrad-canvas"

READ = "room:read"
WRITE = "room:write"
COMMENT_WRITE = "comment:write"

ZERO_HASH = "0" * 64
CHAIN_KEYS = ("sequence", "occurred_at", "actor_id", "actor_kind", "action",
              "resource_type", "resource_id", "resource_name_at_time", "outcome",
              "reason", "request_id")

SEED_APPROVAL_GROUP = "grp-northlake-contractors"
REVIEWERS_GROUP = "grp-northlake-reviewers"
SEED_HOLD = "hold-hollow-2026"
HELD_ROOM = "doc-hollow-dispute"
SEED_PERIOD = "2026-09"
SEED_PLAN_FEE = 50000
SEED_CREDIT = -60000
SEED_METER_AMOUNTS = {
    "collaboration_minutes": 72000,
    "comments_created": 15000,
    "storage_updates": 420,
    "data_stored_gb": 150,
    "custom_notifications": 120000,
    "file_storage_gb": 60,
}
SEED_INVOICE_WITHOUT_SEATS = 197630
SEAT_OVERAGE_MINOR = 2500
RATE_MINOR_PER_MILLION = {
    "collaboration_minutes": 200000,
    "comments_created": 1000000,
    "storage_updates": 100,
    "data_stored_gb": 15000000,
    "custom_notifications": 500000,
    "file_storage_gb": 15000000,
}
ENTERPRISE_CONNECTIONS = 100
POLICY_TIMEOUT_SECONDS = 86400

NOT_FOUND_HEADING = "That address does not exist"
CONSUMER_HOST = "hooks.roomstack-consumer.invalid"
SECRET_LITERALS = ("roomstack-client-secret-2026", "deku_app:deku-local-dev",
                   "deku_admin:deku-local-dev")

SETTLE_SECONDS = 2.0
TIMEOUT = 30.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    time.sleep(seconds)


def uid(prefix: str) -> str:
    return f"{prefix}-{os.urandom(5).hex()}"


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def argument_hash(arguments: dict) -> str:
    return sha256_hex(canonical(arguments))


def chain_hash(prev_hash: str, event: dict) -> str:
    payload = {key: event.get(key) for key in CHAIN_KEYS}
    return sha256_hex(prev_hash + "|" + canonical(payload))


def hmac_hex(secret: str, message: str) -> str:
    return hmac.new(secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()


def parse_instant(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def body(response: httpx.Response) -> dict:
    try:
        payload = response.json()
    except ValueError as exc:
        raise AssertionError(
            f"{response.request.method} {response.request.url} answered "
            f"{response.status_code} with a non-JSON body: {response.text[:300]}") from exc
    return payload if isinstance(payload, dict) else {"items": payload}


def code_of(response: httpx.Response):
    if "json" not in response.headers.get("content-type", ""):
        return None
    payload = response.json()
    return payload.get("code") if isinstance(payload, dict) else None


def app_backend():
    return PostgresBackend(os.environ["DATABASE_URL"])


def dollar(value: str | None) -> str:
    if value is None:
        return "NULL"
    tag = "v" + os.urandom(4).hex()
    return f"${tag}${value}${tag}$"


def rewrite_audit_reason(admin_db, event_hash: str, reason: str | None) -> list[dict]:
    assert re.fullmatch(r"[0-9a-f]{64}", event_hash), event_hash
    admin_db.query(
        "DO $body$ BEGIN "
        "PERFORM set_config('session_replication_role', 'replica', true); "
        f"UPDATE audit_event SET reason = {dollar(reason)} WHERE hash = '{event_hash}'; "
        "END $body$")
    return admin_db.query("SELECT reason FROM audit_event WHERE hash = %s", (event_hash,))


def expect(response: httpx.Response, *statuses: int) -> dict:
    assert response.status_code in statuses, (
        f"{response.request.method} {response.request.url.path} answered "
        f"{response.status_code}, expected {statuses}: {response.text[:400]}")
    return body(response) if response.content else {}


def poll(fetch, done, deadline_seconds: float, interval: float = 0.5):
    deadline = time.monotonic() + deadline_seconds
    last = fetch()
    while not done(last):
        if time.monotonic() >= deadline:
            return last
        settle(interval)
        last = fetch()
    return last


def http(token: str | None = None, headers: dict | None = None) -> httpx.Client:
    merged = dict(headers or {})
    if token:
        merged["Authorization"] = f"Bearer {token}"
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=merged)


def site() -> httpx.Client:
    return httpx.Client(base_url=app_url(), timeout=TIMEOUT, follow_redirects=False)


def login_token(email: str) -> str:
    with http() as c:
        r = c.post("/auth/login", json={"email": email, "password": PASSWORD})
    payload = expect(r, 200)
    token = payload.get("access_token")
    assert token, f"login for {email} returned no access_token: {r.text[:300]}"
    return token


class Clients:
    def __init__(self) -> None:
        self._open: list[httpx.Client] = []

    def member(self, email: str, headers: dict | None = None) -> httpx.Client:
        c = http(login_token(email), headers)
        self._open.append(c)
        return c

    def bearer(self, token: str) -> httpx.Client:
        c = http(token)
        self._open.append(c)
        return c

    def anon(self) -> httpx.Client:
        c = http()
        self._open.append(c)
        return c

    def close(self) -> None:
        for c in self._open:
            c.close()


@pytest.fixture
def clients():
    pool = Clients()
    yield pool
    pool.close()


@pytest.fixture(scope="session")
def db():
    return make_backend()


def walk(client: httpx.Client, path: str, params: dict | None = None,
         limit: int = 100, max_pages: int = 200) -> list[dict]:
    items: list[dict] = []
    query = dict(params or {})
    query["limit"] = limit
    cursor = None
    for _ in range(max_pages):
        if cursor:
            query["cursor"] = cursor
        page = expect(client.get(path, params=query), 200)
        items.extend(page.get("items", []))
        cursor = page.get("next_cursor")
        if not cursor or page.get("has_more") is False:
            break
    return items


def project_by_slug(client: httpx.Client, org: str, slug: str) -> dict:
    for project in walk(client, f"/organisations/{org}/projects"):
        if project.get("slug") == slug:
            return project
    raise AssertionError(f"project {slug!r} is not listed for {org}")


def environment_id(client: httpx.Client, org: str, slug: str, kind: str) -> str:
    project = project_by_slug(client, org, slug)
    for env in project.get("environments", []):
        if env.get("kind") == kind:
            return env["id"]
    raise AssertionError(f"project {slug!r} has no {kind} environment")


def new_project(admin: httpx.Client, org: str = ORG, region: str = "eu-west") -> dict:
    slug = uid("probe")
    project = expect(admin.post(f"/organisations/{org}/projects",
                                json={"name": slug, "slug": slug}), 201)
    dev = expect(admin.post(f"/projects/{project['id']}/environments",
                            json={"kind": "development", "region": region}), 201)
    prod = expect(admin.post(f"/projects/{project['id']}/environments",
                             json={"kind": "production", "region": region}), 201)
    return {"project": project["id"], "slug": slug, "development": dev["id"],
            "production": prod["id"]}


def new_secret(client: httpx.Client, env_id: str) -> dict:
    return expect(client.post(f"/environments/{env_id}/keys",
                              json={"kind": "secret", "label": uid("key")}), 201)


def new_room(client: httpx.Client, env_id: str, accesses=None,
             classification: str = "standard") -> str:
    room_id = uid("doc-probe")
    expect(client.post(f"/environments/{env_id}/rooms", json={
        "room_id": room_id, "classification": classification,
        "default_accesses": accesses if accesses is not None else []}), 201)
    return room_id


def identity_token(secret: str, user_id: str) -> str:
    with http(secret) as c:
        payload = expect(c.post("/identity-tokens", json={"user_id": user_id}), 201)
    assert payload.get("token"), f"identity token response carries no token: {payload}"
    return payload["token"]


class Connection:
    def __init__(self, response: httpx.Response, token: str) -> None:
        self.response = response
        self.token = token
        self.status = response.status_code
        self.payload = body(response) if response.content else {}
        self.id = self.payload.get("connection_id")


def connect(secret: str, user_id: str, room_id: str) -> Connection:
    token = identity_token(secret, user_id)
    with http(token) as c:
        response = c.post("/rt/connections", json={"room_id": room_id})
    return Connection(response, token)


def operate(token: str, connection_id: str, kind: str) -> httpx.Response:
    with http(token) as c:
        return c.post(f"/rt/connections/{connection_id}/operations", json={"kind": kind})


def disconnect(token: str, connection_id: str) -> httpx.Response:
    with http(token) as c:
        return c.delete(f"/rt/connections/{connection_id}")


def connection_record(client: httpx.Client, connection_id: str) -> dict:
    return expect(client.get(f"/rt/connections/{connection_id}"), 200)


def directory_token(admin: httpx.Client, org: str = ORG) -> str:
    payload = expect(admin.post(f"/organisations/{org}/directory-tokens"), 201)
    return payload["token"]


def put_group(token: str, external_id: str, members: list[str], end_users: list[dict]):
    with http(token) as c:
        return expect(c.put(f"/directory/groups/{external_id}", json={
            "name": external_id, "members": members, "end_users": end_users}), 200, 201)


def raise_request(client: httpx.Client, action: str, arguments: dict, reason: str,
                  org: str = ORG) -> dict:
    return expect(client.post(f"/organisations/{org}/approvals", json={
        "action": action, "arguments": arguments, "reason": reason}), 201)


def get_request(client: httpx.Client, approval_id: str) -> dict:
    return expect(client.get(f"/approvals/{approval_id}"), 200)


def decide(client: httpx.Client, approval_id: str, decision: str = "approved") -> httpx.Response:
    return client.post(f"/approvals/{approval_id}/decisions",
                       json={"decision": decision, "reason": "reviewed by the verifier"})


def execute(client: httpx.Client, approval_id: str, arguments: dict) -> httpx.Response:
    return client.post(f"/approvals/{approval_id}/execute", json={"arguments": arguments})


def room_record(client: httpx.Client, env_id: str, room_id: str) -> dict:
    inspector = expect(client.get(f"/environments/{env_id}/rooms/{room_id}/inspector"), 200)
    room = inspector.get("room") or {}
    assert room.get("room_id") == room_id, f"inspector room is {room!r}"
    return room


def request_fields(request: dict) -> dict:
    keys = ("id", "action", "arguments", "reason", "argument_hash", "impact", "status",
            "requested_by", "expires_at", "decisions")
    return {key: request.get(key) for key in keys}


def set_entitlement(owner: httpx.Client, plan: str, key: str, value):
    return expect(owner.patch(f"/entitlements/{plan}/{key}", json={"value": value}), 200)


def audit_events(client: httpx.Client, org: str = ORG, order: str = "asc") -> list[dict]:
    return walk(client, f"/organisations/{org}/audit", {"order": order})


def find_event(client: httpx.Client, request_id: str, org: str = ORG) -> list[dict]:
    newest = walk(client, f"/organisations/{org}/audit", {"order": "desc"}, max_pages=5)
    return [e for e in newest if e.get("request_id") == request_id]


def in_parallel(count: int, work) -> list:
    results: list = [None] * count
    barrier = threading.Barrier(count)

    def run(index: int) -> None:
        barrier.wait()
        results[index] = work(index)

    threads = [threading.Thread(target=run, args=(i,)) for i in range(count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results


class Mailbox:
    def __init__(self) -> None:
        self._inbox = make_inbox()

    def messages(self) -> list[dict]:
        return [{"to": [a.lower() for a in m.to], "subject": m.subject, "text": m.body}
                for m in self._inbox._messages()]

    def mentioning(self, needle: str) -> list[dict]:
        return [m for m in self.messages() if needle in m["text"] or needle in m["subject"]]

    def snapshot(self) -> list[tuple]:
        return [(tuple(m["to"]), m["subject"], m["text"]) for m in self.messages()]

    def since(self, known: list[tuple]) -> list[dict]:
        remaining = list(known)
        fresh = []
        for m in reversed(self.messages()):
            key = (tuple(m["to"]), m["subject"], m["text"])
            if key in remaining:
                remaining.remove(key)
            else:
                fresh.append(m)
        return fresh


@pytest.fixture
def mailbox():
    return Mailbox()


def wait_for_mail(box: Mailbox, needle: str, match, deadline_seconds: float = 75.0) -> list[dict]:
    return poll(lambda: box.mentioning(needle),
                lambda found: any(match(m) for m in found), deadline_seconds, 2.0)


def html_heads(client: httpx.Client, routes) -> dict[str, str]:
    out = {}
    for route in routes:
        r = client.get(route)
        assert r.status_code == 200, f"{route} answered {r.status_code}"
        out[route] = r.text
    return out


def ceil_eight_tenths(value: int) -> int:
    return math.ceil(value * 8 / 10)


class _Cells(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.cells: dict[str, str] = {}
        self._stack: list[tuple[str, str | None]] = []

    def handle_starttag(self, tag, attrs):
        key = dict(attrs).get("data-entitlement")
        if tag in ("br", "img", "input", "meta", "link", "hr"):
            return
        self._stack.append((tag, key))
        if key:
            self.cells.setdefault(key, "")

    def handle_endtag(self, tag):
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                return

    def handle_data(self, data):
        for _, key in self._stack:
            if key:
                self.cells[key] += data


def entitlement_cells(html: str) -> dict[str, str]:
    parser = _Cells()
    parser.feed(html)
    return {k: re.sub(r"\s+", " ", v).strip() for k, v in parser.cells.items()}


@pytest.fixture(scope="session")
def revocation_scenario():
    pool = Clients()
    admin = pool.member(ADMIN)
    developer = pool.member(DEVELOPER)
    contractor_token = login_token(CONTRACTOR)
    contractor = pool.bearer(contractor_token)

    space = new_project(admin)
    env = space["production"]
    secret = new_secret(admin, env)["secret"]
    group = uid("grp-revoke")
    member_users = [uid("eu-rv"), uid("eu-rv")]
    outsider = uid("eu-out")
    put_group(directory_token(admin), group, [CONTRACTOR],
              [{"environment_id": env, "user_id": u} for u in member_users])

    room_a = new_room(admin, env, [READ])
    room_b = new_room(admin, env, [])
    for room in (room_a, room_b):
        expect(admin.put(f"/environments/{env}/rooms/{room}/group-accesses/{group}",
                         json={"accesses": [READ, WRITE]}), 200, 201)

    contractor_key = expect(contractor.post(f"/environments/{space['development']}/keys",
                                            json={"kind": "secret", "label": uid("ck")}), 201)

    member_a = connect(secret, member_users[0], room_a)
    member_b = connect(secret, member_users[1], room_b)
    outside = connect(secret, outsider, room_a)
    arguments = {"group_external_id": group}
    request = raise_request(developer, "group.revoke_access", arguments,
                            "verifier revocation scenario")
    approval = decide(admin, request["id"])
    executed = execute(admin, request["id"], arguments)
    scenario = {
        "env": env, "secret": secret, "group": group, "rooms": (room_a, room_b),
        "contractor_token": contractor_token, "contractor_key": contractor_key,
        "member_connections": [member_a, member_b], "outsider_connection": outside,
        "request": request, "approval": approval, "executed": executed,
    }
    yield scenario
    pool.close()


@pytest.fixture(scope="session")
def impact_growth_scenario():
    pool = Clients()
    admin = pool.member(ADMIN)
    admin2 = pool.member(ADMIN2)
    developer = pool.member(DEVELOPER)
    atlas_prod = environment_id(admin, ORG, ATLAS, "production")
    secret = new_secret(admin, atlas_prod)["secret"]
    room = new_room(admin, atlas_prod, [READ, WRITE])
    arguments = {"environment_id": atlas_prod, "room_id": room}
    request = raise_request(developer, "room.default_access_public", arguments,
                            "verifier impact growth scenario")
    approved = decide(admin, request["id"])
    joined = connect(secret, uid("eu-grow"), room)
    grown = execute(admin, request["id"], arguments)
    after_growth = get_request(admin, request["id"])
    stale_execute = execute(admin, request["id"], arguments)
    reapproved = decide(admin2, request["id"])
    final_execute = execute(admin2, request["id"], arguments)
    scenario = {
        "env": atlas_prod, "room": room, "arguments": arguments, "request": request,
        "approved": approved, "joined": joined, "grown": grown,
        "after_growth": after_growth, "stale_execute": stale_execute,
        "reapproved": reapproved, "final_execute": final_execute,
        "room_after": room_record(admin, atlas_prod, room),
    }
    yield scenario
    pool.close()


@pytest.fixture(scope="session")
def expiry_scenario():
    pool = Clients()
    admin = pool.member(ADMIN)
    developer = pool.member(DEVELOPER)
    atlas_prod = environment_id(admin, ORG, ATLAS, "production")
    expect(admin.put(f"/organisations/{ORG}/approval-policies/room.delete_production", json={
        "requirement": "one_approver", "eligible_roles": ["admin"], "timeout_seconds": 3}),
        200, 201)
    probed_room = new_room(admin, atlas_prod, [READ])
    probed = raise_request(developer, "room.delete_production",
                           {"environment_id": atlas_prod, "room_id": probed_room},
                           "verifier expiry probe")
    expect(admin.put(f"/organisations/{ORG}/approval-policies/room.delete_production", json={
        "requirement": "one_approver", "eligible_roles": ["admin"],
        "timeout_seconds": POLICY_TIMEOUT_SECONDS}), 200, 201)

    stranger = pool.member(OWNER2)
    tetrad_prod = environment_id(stranger, OTHER_ORG, TETRAD, "production")
    expect(stranger.put(f"/organisations/{OTHER_ORG}/approval-policies/room.delete_production",
                        json={"requirement": "one_approver", "eligible_roles": ["admin"],
                              "timeout_seconds": 3}), 200, 201)
    silent_room = new_room(stranger, tetrad_prod, [READ])
    silent = raise_request(stranger, "room.delete_production",
                           {"environment_id": tetrad_prod, "room_id": silent_room},
                           "verifier expiry without reads", org=OTHER_ORG)
    expect(stranger.put(f"/organisations/{OTHER_ORG}/approval-policies/room.delete_production",
                        json={"requirement": "one_approver", "eligible_roles": ["admin"],
                              "timeout_seconds": POLICY_TIMEOUT_SECONDS}), 200, 201)
    scenario = {"env": atlas_prod, "probed": probed, "probed_room": probed_room,
                "silent": silent, "silent_room": silent_room}
    yield scenario
    pool.close()


@pytest.fixture(scope="session")
def break_glass_scenario():
    pool = Clients()
    owner = pool.member(OWNER)
    admin = pool.member(ADMIN)
    box = Mailbox()
    atlas_prod = environment_id(owner, ORG, ATLAS, "production")
    room = new_room(admin, atlas_prod, [])
    arguments = {"environment_id": atlas_prod, "room_id": room}

    refused_owner = owner.post(f"/organisations/{ORG}/break-glass", json={
        "action": "room.default_access_public", "arguments": arguments,
        "reason": "verifier incident without a factor", "second_factor_code": "000000"})
    refused_admin = admin.post(f"/organisations/{ORG}/break-glass", json={
        "action": "room.default_access_public", "arguments": arguments,
        "reason": "verifier incident by an admin", "second_factor_code": "000000"})
    room_after_refusals = room_record(owner, atlas_prod, room)

    known = box.snapshot()
    challenge = owner.post("/auth/second-factor/challenge")

    def code_message(messages):
        for m in messages:
            if OWNER in m["to"] and "roomstack second factor code" in m["subject"].lower():
                return m
        return None

    found = poll(lambda: box.since(known), lambda ms: code_message(ms) is not None, 75.0, 2.0)
    message = code_message(found)
    code = None
    if message:
        match = re.search(r"\b(\d{6})\b", message["subject"] + " " + message["text"])
        code = match.group(1) if match else None
    used = owner.post(f"/organisations/{ORG}/break-glass", json={
        "action": "room.default_access_public", "arguments": arguments,
        "reason": "verifier declared incident", "second_factor_code": code or "missing"})
    held = owner.post(f"/organisations/{ORG}/break-glass", json={
        "action": "room.delete_production",
        "arguments": {"environment_id": atlas_prod, "room_id": HELD_ROOM},
        "reason": "verifier declared incident against a held room",
        "second_factor_code": code or "missing"})
    held_inspector = owner.get(f"/environments/{atlas_prod}/rooms/{HELD_ROOM}/inspector")
    scenario = {
        "env": atlas_prod, "room": room, "arguments": arguments,
        "refused_owner": refused_owner, "refused_admin": refused_admin,
        "room_after_refusals": room_after_refusals, "challenge": challenge,
        "code_message": message, "code": code, "used": used,
        "held": held, "held_inspector": held_inspector,
    }
    yield scenario
    pool.close()
