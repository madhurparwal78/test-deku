"""Task fixtures for deku/yard-operating-system-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout or
module names. The assumptions are the App Contract (the app answers at APP_PUBLIC_URL
with its HTTP API under /api), the HTTP contract and seeded fixtures instruction.md
pins, and the verifier-side services the task declares: the datastore at DB_ADMIN_URL
and DATABASE_URL, and the Mailpit inbox.

Every scenario that writes provisions its own assets, visits, bookings and windows on a
day of its own, so nothing asserted here depends on what the browser workflows did to
the seeded Oakridge visit or to the seeded trailers before pytest ran.
"""

from __future__ import annotations

import os
import threading
import time
from datetime import datetime, timedelta, timezone

import httpx
from appclient import api_base, app_url
from capabilities import PostgresBackend, make_inbox

PASSWORD = "deku-demo-pw-2026"

ORGADMIN = "orgadmin@tidewater.example.com"
MANAGER = "manager.dal@tidewater.example.com"
MANAGER2 = "manager2.dal@tidewater.example.com"
DISPATCH = "dispatch.dal@tidewater.example.com"
GATE = "gate.dal@tidewater.example.com"
DOCK = "dock.dal@tidewater.example.com"
SPOTTER = "spotter.dal@tidewater.example.com"
SPOTTER2 = "spotter2.dal@tidewater.example.com"
DUAL = "dual@tidewater.example.com"
ANALYST = "analyst@tidewater.example.com"
SECURITY = "security@tidewater.example.com"
MANAGER_ATL = "manager.atl@northfield.example.com"
PUBLISHER = "publisher@junction.example.com"

REDLINE = "bookings@redline.example.com"
BLUECREST = "desk@bluecrest.example.com"
OAKRIDGE = "team@oakridge.example.com"
EVERWEAR = "reports@everwear.example.com"
PRAXIS = "reports@praxis.example.com"

DAL1 = "DAL1"
RNO2 = "RNO2"
DALLAS_NAME = "Dallas Crossdock"
REG_REDLINE = "MC-100245"
REG_BLUECREST = "MC-200318"
REG_HALVARD = "MC-400932"
PLATE_ACTIVE = "TX-9KR-221"
PLATE_EXPIRED = "TX-4LM-870"
SEEDED_STALE_ASSET = "TRL-4471"
EVERWEAR_LOADS = {"EW-0901", "EW-0902", "EW-0903", "EW-0904", "EW-0905", "EW-0906"}
DRY_DOORS = {"D01", "D02", "D03", "D04"}
HELP_OPTION = "Schedule a 30-minute meeting with a yard expert"
ZERO_HASH = "0" * 64

SETTLE_SECONDS = 2.0
TIMEOUT = 30.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    time.sleep(seconds)


def uid(prefix: str) -> str:
    return f"{prefix}-{os.urandom(5).hex()}"


def upper_uid(prefix: str) -> str:
    return f"{prefix}-{os.urandom(3).hex().upper()}"


def absent_id(prefix: str) -> str:
    return f"{prefix}_{os.urandom(12).hex()}"


def future_day(days_ahead: int) -> str:
    return (datetime.now(timezone.utc).date() + timedelta(days=days_ahead)).isoformat()


def covering_shift_bounds() -> tuple[str, str]:
    today = datetime.now(timezone.utc).date()
    return (f"{(today - timedelta(days=1)).isoformat()}T00:00",
            f"{(today + timedelta(days=2)).isoformat()}T00:00")


def body(response: httpx.Response):
    try:
        return response.json()
    except ValueError as exc:
        raise AssertionError(
            f"{response.request.method} {response.request.url.path} answered "
            f"{response.status_code} with a non-JSON body: {response.text[:300]}") from exc


def code_of(response: httpx.Response):
    if "json" not in response.headers.get("content-type", ""):
        return None
    payload = response.json()
    return payload.get("code") if isinstance(payload, dict) else None


def expect(response: httpx.Response, *statuses: int):
    assert response.status_code in statuses, (
        f"{response.request.method} {response.request.url.path} answered "
        f"{response.status_code}, expected {statuses}: {response.text[:400]}")
    return body(response) if response.content else {}


def refusal(response: httpx.Response, status: int, code: str) -> dict:
    assert response.status_code == status and code_of(response) == code, (
        f"{response.request.method} {response.request.url.path} answered "
        f"{response.status_code} code {code_of(response)!r}, expected {status} "
        f"{code!r}: {response.text[:400]}")
    return body(response)


def http(token: str | None = None, headers: dict | None = None) -> httpx.Client:
    merged = dict(headers or {})
    if token:
        merged["Authorization"] = f"Bearer {token}"
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=merged)


def site_client() -> httpx.Client:
    return httpx.Client(base_url=app_url(), timeout=TIMEOUT, follow_redirects=False)


def member_token(email: str) -> str:
    with http() as c:
        payload = expect(c.post("/auth/login", json={"email": email, "password": PASSWORD}), 200)
    token = payload.get("access_token")
    assert token, f"member login for {email} returned no access_token: {payload}"
    return token


def portal_token(email: str) -> str:
    with http() as c:
        payload = expect(c.post("/portal/auth/login",
                                json={"email": email, "password": PASSWORD}), 200)
    token = payload.get("access_token")
    assert token, f"portal login for {email} returned no access_token: {payload}"
    return token


def site_id(token: str, code: str) -> str:
    with http(token) as c:
        sites = expect(c.get("/sites"), 200)
    for s in sites:
        if s.get("code") == code:
            return s["id"]
    raise AssertionError(f"GET /api/sites lists no site with code {code}: {sites}")


def portal_site_id(token: str, name: str = DALLAS_NAME) -> str:
    with http(token) as c:
        sites = expect(c.get("/portal/sites"), 200)
    for s in sites:
        if s.get("name") == name:
            return s["id"]
    raise AssertionError(f"GET /api/portal/sites lists no site named {name}: {sites}")


def member_id(admin_token: str, email: str) -> str:
    with http(admin_token) as c:
        members = expect(c.get("/members"), 200)
    for m in members:
        if m.get("email") == email:
            return m["member_id"]
    raise AssertionError(f"GET /api/members lists no member {email}")


def run_together(requests: list) -> list[httpx.Response]:
    clients = [http(token, headers) for token, headers, _ in requests]
    for c in clients:
        c.get("/health")
    barrier = threading.Barrier(len(requests))
    results: list = [None] * len(requests)

    def fire(index: int) -> None:
        _, _, call = requests[index]
        barrier.wait()
        results[index] = call(clients[index])

    threads = [threading.Thread(target=fire, args=(i,)) for i in range(len(requests))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    for c in clients:
        c.close()
    assert all(r is not None for r in results), "a simultaneous request never completed"
    return results


def portal_booking_body(day: str, start: str, end: str, asset_type: str = "dry_van",
                        load_reference: str | None = None) -> dict:
    payload = {"direction": "inbound", "asset_type": asset_type,
               "starts_local": f"{day}T{start}", "ends_local": f"{day}T{end}",
               "driver": {"name": "Rosa Delgado", "telephone": "+15550100177", "language": "en"}}
    if load_reference:
        payload["load_reference"] = load_reference
    return payload


def member_booking_body(day: str, start: str, end: str, door: str,
                        asset_type: str = "dry_van") -> dict:
    return {"haulier_registration": REG_REDLINE, "direction": "inbound", "door": door,
            "asset_type": asset_type, "starts_local": f"{day}T{start}",
            "ends_local": f"{day}T{end}"}


def new_asset(token: str, site: str, asset_type: str = "dry_van") -> str:
    number = upper_uid("TST")
    with http(token) as c:
        expect(c.post(f"/sites/{site}/assets",
                      json={"asset_number": number, "asset_type": asset_type,
                            "haulier_registration": REG_REDLINE}), 201)
    return number


def observe(token: str, site: str, asset_number: str, spot: str) -> dict:
    with http(token) as c:
        return expect(c.post(f"/sites/{site}/positions",
                             json={"asset_number": asset_number, "spot": spot}), 201)


def open_move(token: str, site: str, asset_number: str, to_spot: str) -> dict:
    with http(token) as c:
        return expect(c.post(f"/sites/{site}/moves",
                             json={"asset_number": asset_number, "to_spot": to_spot,
                                   "reason": "repositioning"}), 201)


def cancel_move(token: str, move_id: str) -> dict:
    with http(token) as c:
        return expect(c.post(f"/moves/{move_id}/cancel", json={"reason": "scenario complete"}), 200)


def ensure_spotter_on_shift(manager_token: str, site: str) -> None:
    start, end = covering_shift_bounds()
    with http(manager_token) as c:
        expect(c.post(f"/sites/{site}/shifts",
                      json={"member_email": SPOTTER, "starts_local": start,
                            "ends_local": end}), 201)


def transition(token: str, move: dict, to: str, **extra) -> httpx.Response:
    with http(token) as c:
        return c.post(f"/moves/{move['id']}/transitions",
                      json={"to": to, "version": move["version"], **extra})


def walk_to_placed(token: str, move: dict) -> dict:
    current = expect(transition(token, move, "assigned", assignee_email=SPOTTER), 200)
    for step in ("accepted", "travelling", "hooked", "moving", "placed"):
        current = expect(transition(token, current, step), 200)
    assert current.get("state") == "placed", f"move did not reach placed: {current}"
    return current


def read_move(token: str, move_id: str) -> dict:
    with http(token) as c:
        return expect(c.get(f"/moves/{move_id}"), 200)


def record_visit(token: str, site: str, plate: str, registration: str) -> dict:
    with http(token) as c:
        return expect(c.post(f"/sites/{site}/visits",
                             json={"lane": "G1-IN", "direction": "inbound", "plate": plate,
                                   "asset_number": upper_uid("TRL"),
                                   "haulier_registration": registration}), 201)


def held_visit(token: str, site: str) -> dict:
    visit = record_visit(token, site, upper_uid("HV"), REG_HALVARD)
    assert visit.get("state") == "held", f"a suspended haulier's arrival was not held: {visit}"
    return visit


def request_release(token: str, visit_id: str) -> dict:
    with http(token) as c:
        return expect(c.post(f"/visits/{visit_id}/release-requests",
                             json={"reason": "Driver presented a retrospective booking"}), 201)


def decide(token: str, approval_id: str, decision: str = "approved") -> httpx.Response:
    with http(token) as c:
        return c.post(f"/approvals/{approval_id}/decisions",
                      json={"decision": decision, "reason": "Reviewed at the gate"})


def read_json(token: str, path: str):
    with http(token) as c:
        return expect(c.get(path), 200)


def custody_event(token: str, site: str, asset_number: str, kind: str,
                  seal_number: str | None = None) -> dict:
    payload = {"asset_number": asset_number, "kind": kind}
    if seal_number:
        payload["seal_number"] = seal_number
    with http(token) as c:
        return expect(c.post(f"/sites/{site}/custody-events", json=payload), 201)


def admin_db() -> PostgresBackend:
    return PostgresBackend(os.environ["DB_ADMIN_URL"])


def app_db() -> PostgresBackend:
    return PostgresBackend(os.environ["DATABASE_URL"])


def tamper_seal_number(event_id: str, seal_number: str) -> None:
    assert event_id.replace("_", "").replace("-", "").isalnum(), event_id
    admin_db().query(
        "DO $tamper$ BEGIN "
        "PERFORM set_config('session_replication_role', 'replica', true); "
        f"UPDATE custody_event SET seal_number = '{seal_number}' WHERE id = '{event_id}'; "
        "END $tamper$")


def contact_body(email: str, decoy: str = "") -> dict:
    return {"full_name": "Morgan Reyes", "role": "Yard operations lead", "phone": "",
            "email": email, "company": "Reyes Freight", "help": [HELP_OPTION],
            "company_website": decoy, "submission_id": uid("sub")}


def inbox():
    return make_inbox()


def messages_matching(to: str, needle: str) -> list:
    box = inbox()
    return [m for m in box._messages()
            if any(to.lower() in addr.lower() for addr in m.to) and needle in m.subject]


def poll(fetch, done, deadline_seconds: float, interval: float = 0.5):
    deadline = time.monotonic() + deadline_seconds
    last = fetch()
    while not done(last):
        if time.monotonic() >= deadline:
            return last
        settle(interval)
        last = fetch()
    return last


def wait_for_mail(to: str, needle: str, deadline_seconds: float = 30.0) -> list:
    return poll(lambda: messages_matching(to, needle), lambda found: len(found) > 0,
                deadline_seconds)
