"""Graders for deku/yard-operating-system-vb, one merged module.

Every assertion reads the running app over HTTP, the declared datastore or the Mailpit
inbox, and asserts only what instruction.md pins.
"""

from __future__ import annotations

from datetime import datetime

import pytest

from conftest import (
    ANALYST, BLUECREST, DAL1, DISPATCH, DOCK, DRY_DOORS, DUAL, EVERWEAR, EVERWEAR_LOADS,
    GATE, MANAGER, MANAGER2, MANAGER_ATL, OAKRIDGE, ORGADMIN, PASSWORD, PLATE_ACTIVE,
    PLATE_EXPIRED, PRAXIS, PUBLISHER, REDLINE, REG_REDLINE, RNO2, SECURITY, SEEDED_STALE_ASSET, SPOTTER,
    SPOTTER2, ZERO_HASH, absent_id, admin_db, app_db, body, cancel_move, code_of, contact_body,
    custody_event, decide, ensure_spotter_on_shift, expect, future_day, held_visit, http,
    member_booking_body, member_id, member_token, messages_matching, new_asset, observe,
    open_move, poll, portal_booking_body, portal_site_id, portal_token, read_json, read_move,
    record_visit, refusal, request_release, run_together, settle, site_client, site_id,
    tamper_seal_number, transition, uid, upper_uid, wait_for_mail, walk_to_placed,
)


def test_concurrent_portal_bookings_confirm_only_free_doors():
    red, blue = portal_token(REDLINE), portal_token(BLUECREST)
    site = portal_site_id(red)
    payload = portal_booking_body(future_day(11), "10:00", "10:30")
    requests = [(tok, {"Idempotency-Key": uid("idem")},
                 lambda c: c.post(f"/portal/sites/{site}/bookings", json=payload))
                for tok in (red, blue, red, blue, red)]
    responses = run_together(requests)
    confirmed = [r for r in responses if r.status_code == 201]
    refused = [r for r in responses if r.status_code != 201]
    assert len(confirmed) == 4, (
        f"five simultaneous dry van bookings for one half hour confirmed {len(confirmed)}, "
        f"expected 4: {[(r.status_code, r.text[:120]) for r in responses]}")
    assert len(refused) == 1 and refused[0].status_code == 409 and code_of(refused[0]) == "no_capacity", (
        f"the fifth booking was not refused no_capacity: {[(r.status_code, r.text[:160]) for r in refused]}")
    mgr = member_token(MANAGER)
    doors = [read_json(mgr, f"/appointments/{body(r)['id']}")["door"] for r in confirmed]
    assert len(set(doors)) == 4 and set(doors) <= DRY_DOORS, (
        f"the four confirmed bookings do not hold four distinct dry van doors: {doors}")


def test_concurrent_reefer_bookings_single_door_one_confirmed():
    red, blue = portal_token(REDLINE), portal_token(BLUECREST)
    site = portal_site_id(red)
    payload = portal_booking_body(future_day(12), "10:00", "10:30", asset_type="reefer")
    responses = run_together([(tok, {"Idempotency-Key": uid("idem")},
                               lambda c: c.post(f"/portal/sites/{site}/bookings", json=payload))
                              for tok in (red, blue)])
    confirmed = [r for r in responses if r.status_code == 201]
    assert len(confirmed) == 1, (
        f"two simultaneous reefer bookings for the one reefer door confirmed {len(confirmed)}: "
        f"{[(r.status_code, r.text[:160]) for r in responses]}")
    other = [r for r in responses if r.status_code != 201][0]
    refusal(other, 409, "no_capacity")
    door = read_json(member_token(MANAGER), f"/appointments/{body(confirmed[0])['id']}")["door"]
    assert door == "D05", f"the reefer booking holds door {door}, expected D05"


def test_no_capacity_refusal_offers_alternative_windows():
    red = portal_token(REDLINE)
    site = portal_site_id(red)
    day = future_day(13)
    with http(red) as c:
        for _ in range(4):
            expect(c.post(f"/portal/sites/{site}/bookings",
                          json=portal_booking_body(day, "10:00", "10:30"),
                          headers={"Idempotency-Key": uid("idem")}), 201)
        refused = c.post(f"/portal/sites/{site}/bookings",
                         json=portal_booking_body(day, "10:00", "10:30"),
                         headers={"Idempotency-Key": uid("idem")})
    payload = refusal(refused, 409, "no_capacity")
    alternatives = payload.get("alternatives")
    assert isinstance(alternatives, list) and alternatives, (
        f"a no_capacity refusal carried no alternatives: {payload}")
    first = alternatives[0]
    assert set(first) >= {"starts_at", "ends_at"}, f"an alternative lacks starts_at or ends_at: {first}"
    start = datetime.fromisoformat(first["starts_at"])
    end = datetime.fromisoformat(first["ends_at"])
    with http(red) as c:
        accepted = c.post(f"/portal/sites/{site}/bookings",
                          json=portal_booking_body(start.date().isoformat(), start.strftime("%H:%M"),
                                                   end.strftime("%H:%M")),
                          headers={"Idempotency-Key": uid("idem")})
    expect(accepted, 201)


def test_overlapping_window_same_door_conflict_door_unavailable():
    mgr = member_token(MANAGER)
    site = site_id(mgr, DAL1)
    day = future_day(14)
    with http(mgr) as c:
        expect(c.post(f"/sites/{site}/appointments", json=member_booking_body(day, "10:00", "10:30", "D01")), 201)
        overlap = c.post(f"/sites/{site}/appointments", json=member_booking_body(day, "10:15", "10:45", "D01"))
    refusal(overlap, 409, "door_unavailable")


def test_adjacent_half_open_windows_both_confirmed():
    mgr = member_token(MANAGER)
    site = site_id(mgr, DAL1)
    day = future_day(15)
    with http(mgr) as c:
        first = expect(c.post(f"/sites/{site}/appointments", json=member_booking_body(day, "10:00", "10:30", "D02")), 201)
        second = c.post(f"/sites/{site}/appointments", json=member_booking_body(day, "10:30", "11:00", "D02"))
    confirmed = expect(second, 201)
    assert first.get("state") == "confirmed" and confirmed.get("state") == "confirmed", (
        f"adjacent windows on one door did not both confirm: {first} {confirmed}")


def test_out_of_service_door_booking_refused():
    mgr = member_token(MANAGER)
    site = site_id(mgr, DAL1)
    with http(mgr) as c:
        response = c.post(f"/sites/{site}/appointments",
                          json=member_booking_body(future_day(16), "10:00", "10:30", "D06"))
    refusal(response, 409, "door_out_of_service")


def test_incapable_door_asset_type_refused():
    mgr = member_token(MANAGER)
    site = site_id(mgr, DAL1)
    with http(mgr) as c:
        response = c.post(f"/sites/{site}/appointments",
                          json=member_booking_body(future_day(17), "10:00", "10:30", "D05"))
    refusal(response, 422, "door_incapable")


def test_stale_version_appointment_update_version_conflict():
    mgr = member_token(MANAGER)
    site = site_id(mgr, DAL1)
    day = future_day(18)
    with http(mgr) as c:
        created = expect(c.post(f"/sites/{site}/appointments", json=member_booking_body(day, "10:00", "10:30", "D03")), 201)
        updated = expect(c.patch(f"/appointments/{created['id']}",
                                 json={"version": created["version"], "reason": "carrier asked later",
                                       "starts_local": f"{day}T11:00", "ends_local": f"{day}T11:30"}), 200)
        stale = c.patch(f"/appointments/{created['id']}",
                        json={"version": created["version"], "reason": "second planner",
                              "starts_local": f"{day}T12:00", "ends_local": f"{day}T12:30"})
    payload = refusal(stale, 409, "version_conflict")
    assert payload.get("current_version") == updated["version"], (
        f"version_conflict names {payload.get('current_version')!r}, current is {updated['version']!r}")
    after = read_json(mgr, f"/appointments/{created['id']}")
    assert after["starts_at"] == updated["starts_at"], f"the stale update overwrote the booking: {after}"


def test_unentitled_module_booking_module_not_entitled():
    dual = member_token(DUAL)
    reno = site_id(dual, RNO2)
    with http(dual) as c:
        response = c.post(f"/sites/{reno}/appointments",
                          json=member_booking_body(future_day(19), "10:00", "10:30", "D01"))
    refusal(response, 403, "module_not_entitled")


def test_concurrent_moves_same_asset_single_open_move():
    mgr, disp = member_token(MANAGER), member_token(DISPATCH)
    site = site_id(disp, DAL1)
    asset = new_asset(mgr, site)
    observe(disp, site, asset, "S-01")
    responses = run_together([
        (disp, {}, lambda c: c.post(f"/sites/{site}/moves", json={"asset_number": asset, "to_spot": "A-01", "reason": "repositioning"})),
        (disp, {}, lambda c: c.post(f"/sites/{site}/moves", json={"asset_number": asset, "to_spot": "A-02", "reason": "repositioning"})),
    ])
    created = [r for r in responses if r.status_code == 201]
    assert len(created) == 1, (
        f"two simultaneous moves for one asset created {len(created)}: "
        f"{[(r.status_code, r.text[:160]) for r in responses]}")
    other = [r for r in responses if r.status_code != 201][0]
    payload = refusal(other, 409, "asset_has_open_move")
    assert payload.get("move_id") == body(created[0])["id"], (
        f"asset_has_open_move names {payload.get('move_id')!r}, the open move is {body(created[0])['id']!r}")
    cancel_move(disp, body(created[0])["id"])


def test_concurrent_moves_same_destination_single_reservation():
    mgr, disp = member_token(MANAGER), member_token(DISPATCH)
    site = site_id(disp, DAL1)
    first, second = new_asset(mgr, site), new_asset(mgr, site)
    observe(disp, site, first, "S-01")
    observe(disp, site, second, "S-03")
    responses = run_together([
        (disp, {}, lambda c: c.post(f"/sites/{site}/moves", json={"asset_number": first, "to_spot": "A-04", "reason": "door_feed"})),
        (disp, {}, lambda c: c.post(f"/sites/{site}/moves", json={"asset_number": second, "to_spot": "A-04", "reason": "door_feed"})),
    ])
    created = [r for r in responses if r.status_code == 201]
    assert len(created) == 1, (
        f"two simultaneous moves into one free spot created {len(created)}: "
        f"{[(r.status_code, r.text[:160]) for r in responses]}")
    refusal([r for r in responses if r.status_code != 201][0], 409, "destination_reserved")
    cancel_move(disp, body(created[0])["id"])


def test_cancelled_move_frees_destination_reservation():
    mgr, disp = member_token(MANAGER), member_token(DISPATCH)
    site = site_id(disp, DAL1)
    first, second = new_asset(mgr, site), new_asset(mgr, site)
    observe(disp, site, first, "S-04")
    observe(disp, site, second, "S-05")
    move = open_move(disp, site, first, "A-05")
    with http(disp) as c:
        blocked = c.post(f"/sites/{site}/moves", json={"asset_number": second, "to_spot": "A-05", "reason": "repositioning"})
    refusal(blocked, 409, "destination_reserved")
    cancelled = cancel_move(disp, move["id"])
    assert cancelled.get("state") == "cancelled", f"cancel did not cancel: {cancelled}"
    freed = open_move(disp, site, second, "A-05")
    assert freed.get("state") == "open", f"the freed destination refused a new move: {freed}"
    cancel_move(disp, freed["id"])


def test_incompatible_destination_move_refused():
    mgr, disp = member_token(MANAGER), member_token(DISPATCH)
    site = site_id(disp, DAL1)
    asset = new_asset(mgr, site)
    observe(disp, site, asset, "S-06")
    with http(disp) as c:
        response = c.post(f"/sites/{site}/moves", json={"asset_number": asset, "to_spot": "R-02", "reason": "repositioning"})
    refusal(response, 422, "destination_incompatible")


def test_stale_position_move_refused_position_confirmation_task():
    disp = member_token(DISPATCH)
    site = site_id(disp, DAL1)
    reading = read_json(disp, f"/sites/{site}/assets/{SEEDED_STALE_ASSET}")
    assert reading.get("staleness") == "stale", f"the seeded trailer does not read stale: {reading}"
    with http(disp) as c:
        response = c.post(f"/sites/{site}/moves",
                          json={"asset_number": SEEDED_STALE_ASSET, "to_spot": "A-06", "reason": "repositioning"})
    refusal(response, 409, "position_stale")
    tasks = read_json(disp, f"/sites/{site}/tasks?kind=position_confirmation")
    assert any(t.get("asset_number") == SEEDED_STALE_ASSET and t.get("kind") == "position_confirmation"
               for t in tasks), f"no position_confirmation task names {SEEDED_STALE_ASSET}: {tasks}"


def test_fresh_position_move_accepted_open_state():
    mgr, disp = member_token(MANAGER), member_token(DISPATCH)
    site = site_id(disp, DAL1)
    asset = new_asset(mgr, site)
    reading = observe(disp, site, asset, "S-02")
    assert reading.get("staleness") == "fresh", f"a new observation does not read fresh: {reading}"
    move = open_move(disp, site, asset, "A-08")
    assert move.get("state") == "open" and move.get("from_spot") == "S-02", f"unexpected move: {move}"
    cancel_move(disp, move["id"])


def test_move_transition_to_verified_illegal_transition():
    mgr, disp = member_token(MANAGER), member_token(DISPATCH)
    site = site_id(disp, DAL1)
    ensure_spotter_on_shift(mgr, site)
    asset = new_asset(mgr, site)
    observe(disp, site, asset, "S-04")
    placed = walk_to_placed(disp, open_move(disp, site, asset, "A-09"))
    refusal(transition(disp, placed, "verified"), 409, "illegal_transition")
    assert read_move(disp, placed["id"]).get("state") == "placed", "a refused verified request changed the move"


def test_observation_at_destination_verifies_placed_move():
    mgr, disp = member_token(MANAGER), member_token(DISPATCH)
    site = site_id(disp, DAL1)
    ensure_spotter_on_shift(mgr, site)
    asset = new_asset(mgr, site)
    observe(disp, site, asset, "S-05")
    placed = walk_to_placed(disp, open_move(disp, site, asset, "A-10"))
    observe(disp, site, asset, "A-10")
    final = poll(lambda: read_move(disp, placed["id"]), lambda m: m.get("state") == "verified", 15.0)
    assert final.get("state") == "verified", f"an observation at the destination left the move {final.get('state')}"


def test_observation_elsewhere_leaves_move_placed():
    mgr, disp = member_token(MANAGER), member_token(DISPATCH)
    site = site_id(disp, DAL1)
    ensure_spotter_on_shift(mgr, site)
    asset = new_asset(mgr, site)
    observe(disp, site, asset, "S-06")
    placed = walk_to_placed(disp, open_move(disp, site, asset, "A-11"))
    observe(disp, site, asset, "S-01")
    settle()
    assert read_move(disp, placed["id"]).get("state") == "placed", "an observation elsewhere verified the move"


def test_assignment_needs_spotter_on_shift():
    mgr, disp = member_token(MANAGER), member_token(DISPATCH)
    site = site_id(disp, DAL1)
    asset = new_asset(mgr, site)
    observe(disp, site, asset, "S-03")
    move = open_move(disp, site, asset, "A-12")
    refusal(transition(disp, move, "assigned", assignee_email=SPOTTER2), 409, "spotter_not_on_shift")
    cancel_move(disp, move["id"])


def test_manually_completed_move_frees_destination():
    mgr, disp = member_token(MANAGER), member_token(DISPATCH)
    site = site_id(disp, DAL1)
    ensure_spotter_on_shift(mgr, site)
    first, second = new_asset(mgr, site, "reefer"), new_asset(mgr, site, "reefer")
    observe(disp, site, first, "R-03")
    observe(disp, site, second, "R-02")
    placed = walk_to_placed(disp, open_move(disp, site, first, "R-04"))
    completed = expect(transition(disp, placed, "completed", reason="no camera covers the reefer row"), 200)
    assert completed.get("state") == "completed", f"a manual completion left the move {completed.get('state')}"
    freed = open_move(disp, site, second, "R-04")
    assert freed.get("state") == "open", f"the completed move still holds its destination: {freed}"
    cancel_move(disp, freed["id"])


def test_spotter_cannot_accept_move_assigned_to_another_spotter():
    mgr, disp = member_token(MANAGER), member_token(DISPATCH)
    site = site_id(disp, DAL1)
    ensure_spotter_on_shift(mgr, site)
    asset = new_asset(mgr, site)
    observe(disp, site, asset, "S-03")
    assigned = expect(transition(disp, open_move(disp, site, asset, "A-06"), "assigned", assignee_email=SPOTTER), 200)
    refusal(transition(member_token(SPOTTER2), assigned, "accepted"), 403, "forbidden")
    assert read_move(disp, assigned["id"]).get("state") == "assigned", "another spotter accepted the move"
    cancel_move(disp, assigned["id"])


def test_requester_self_approval_denied_visit_stays_held():
    mgr = member_token(MANAGER)
    site = site_id(mgr, DAL1)
    visit = held_visit(mgr, site)
    approval = request_release(mgr, visit["id"])
    refusal(decide(mgr, approval["id"]), 403, "self_approval_forbidden")
    assert read_json(mgr, f"/approvals/{approval['id']}").get("state") == "pending", "a refused self decision changed the request"
    assert read_json(mgr, f"/visits/{visit['id']}").get("state") == "held", "a refused self decision released the visit"


def test_eligible_site_manager_approval_admits_visit():
    gate, mgr2 = member_token(GATE), member_token(MANAGER2)
    site = site_id(gate, DAL1)
    visit = held_visit(gate, site)
    approval = request_release(gate, visit["id"])
    assert approval.get("action") == "gate.release_override" and approval.get("state") == "pending", approval
    expect(decide(mgr2, approval["id"]), 200)
    final = poll(lambda: read_json(mgr2, f"/visits/{visit['id']}"), lambda v: v.get("state") == "admitted", 15.0)
    assert final.get("state") == "admitted", f"an approved release left the visit {final.get('state')}"


def test_decided_approval_second_decision_already_decided():
    gate, mgr, mgr2 = member_token(GATE), member_token(MANAGER), member_token(MANAGER2)
    site = site_id(gate, DAL1)
    approval = request_release(gate, held_visit(gate, site)["id"])
    expect(decide(mgr, approval["id"]), 200)
    refusal(decide(mgr2, approval["id"], "rejected"), 409, "already_decided")


def test_denied_decision_recorded_in_audit():
    mgr, admin = member_token(MANAGER), member_token(ORGADMIN)
    site = site_id(mgr, DAL1)
    approval = request_release(mgr, held_visit(mgr, site)["id"])
    refusal(decide(mgr, approval["id"]), 403, "self_approval_forbidden")
    entries = poll(lambda: read_json(admin, "/audit?action=approval.decide&outcome=denied"),
                   lambda rows: any(r.get("resource_id") == approval["id"] for r in rows), 15.0)
    assert any(r.get("resource_id") == approval["id"] and r.get("outcome") == "denied" for r in entries), (
        f"the refused decision on {approval['id']} is absent from the audit record")


def test_dual_role_gate_operator_scope_approval_forbidden():
    gate, dual = member_token(GATE), member_token(DUAL)
    site = site_id(gate, DAL1)
    visit = held_visit(gate, site)
    approval = request_release(gate, visit["id"])
    refusal(decide(dual, approval["id"]), 403, "forbidden")
    assert read_json(gate, f"/approvals/{approval['id']}").get("state") == "pending", "a Reno manager decided a Dallas request"
    assert read_json(gate, f"/visits/{visit['id']}").get("state") == "held", "a Reno manager released a Dallas visit"


def test_gate_operator_approval_forbidden_request_pending():
    mgr, gate = member_token(MANAGER), member_token(GATE)
    site = site_id(mgr, DAL1)
    approval = request_release(mgr, held_visit(mgr, site)["id"])
    refusal(decide(gate, approval["id"]), 403, "forbidden")
    assert read_json(mgr, f"/approvals/{approval['id']}").get("state") == "pending", "a gate operator decided a request"


def test_dispatcher_approval_forbidden_request_pending():
    gate, disp = member_token(GATE), member_token(DISPATCH)
    site = site_id(gate, DAL1)
    approval = request_release(gate, held_visit(gate, site)["id"])
    refusal(decide(disp, approval["id"]), 403, "forbidden")
    assert read_json(gate, f"/approvals/{approval['id']}").get("state") == "pending", "a dispatcher decided a request"


def test_security_administrator_and_analyst_operational_write_forbidden():
    mgr = member_token(MANAGER)
    site = site_id(mgr, DAL1)
    asset = new_asset(mgr, site)
    observe(member_token(DISPATCH), site, asset, "S-05")
    for email in (SECURITY, ANALYST):
        with http(member_token(email)) as c:
            response = c.post(f"/sites/{site}/moves",
                              json={"asset_number": asset, "to_spot": "S-06", "reason": "repositioning"})
        refusal(response, 403, "forbidden")
    reading = read_json(mgr, f"/sites/{site}/assets/{asset}")
    assert reading.get("open_move_id") is None, f"a refused operational write opened a move: {reading}"


def test_approver_eligibility_read_at_decision_time():
    admin, gate = member_token(ORGADMIN), member_token(GATE)
    site = site_id(gate, DAL1)
    with http(admin) as c:
        grant = expect(c.post(f"/members/{member_id(admin, ANALYST)}/grants",
                              json={"role": "site_manager", "site_id": site, "reason": "holiday cover",
                                    "expires_at": "2027-12-31T23:59:59Z"}), 201)
    approval = request_release(gate, held_visit(gate, site)["id"])
    analyst = member_token(ANALYST)
    with http(admin) as c:
        expect(c.delete(f"/grants/{grant['id']}"), 204)
    refusal(decide(analyst, approval["id"]), 403, "forbidden")
    assert read_json(gate, f"/approvals/{approval['id']}").get("state") == "pending", (
        "a decision by a member whose grant was revoked changed the request")


def test_revoked_grant_denied_same_token_next_request():
    admin, mgr = member_token(ORGADMIN), member_token(MANAGER)
    site = site_id(mgr, DAL1)
    asset = new_asset(mgr, site)
    analyst_id = member_id(admin, ANALYST)
    with http(admin) as c:
        grant = expect(c.post(f"/members/{analyst_id}/grants",
                              json={"role": "dispatcher", "site_id": site, "reason": "cover a shift"}), 201)
    analyst = member_token(ANALYST)
    observe(analyst, site, asset, "S-02")
    with http(admin) as c:
        expect(c.delete(f"/grants/{grant['id']}"), 204)
    with http(analyst) as c:
        after = c.post(f"/sites/{site}/positions", json={"asset_number": asset, "spot": "S-03"})
    refusal(after, 403, "forbidden")
    reading = read_json(mgr, f"/sites/{site}/assets/{asset}")
    assert reading.get("spot") == "S-02", f"a revoked grant still moved the asset: {reading}"


def test_elevated_role_grant_without_expiry_expiry_required():
    admin = member_token(ORGADMIN)
    site = site_id(admin, DAL1)
    with http(admin) as c:
        response = c.post(f"/members/{member_id(admin, ANALYST)}/grants",
                          json={"role": "site_manager", "site_id": site, "reason": "holiday cover"})
    refusal(response, 422, "expiry_required")


def test_cross_organisation_site_not_found_for_member():
    dallas = site_id(member_token(MANAGER), DAL1)
    with http(member_token(MANAGER_ATL)) as c:
        response = c.get(f"/sites/{dallas}")
    refusal(response, 404, "not_found")


def test_ungranted_site_same_organisation_not_found():
    reno = site_id(member_token(ORGADMIN), RNO2)
    with http(member_token(GATE)) as c:
        response = c.get(f"/sites/{reno}")
    refusal(response, 404, "not_found")


def test_member_session_login_access_token():
    with http() as c:
        good = expect(c.post("/auth/login", json={"email": MANAGER, "password": PASSWORD}), 200)
        bad = c.post("/auth/login", json={"email": MANAGER, "password": "wrong-pass-9"})
    assert good.get("access_token") and good.get("expires_at"), f"login lacks access_token or expires_at: {good}"
    refusal(bad, 401, "invalid_credentials")


def test_unauthenticated_console_call_unauthenticated():
    with http() as c:
        sites = c.get("/sites")
        members = c.get("/members")
    refusal(sites, 401, "unauthenticated")
    refusal(members, 401, "unauthenticated")


def test_signup_closed_in_both_spaces_no_account_created():
    body = {"email": f"{uid('newcomer')}@tidewater.example.com", "password": PASSWORD}
    with http() as c:
        member = c.post("/auth/signup", json=body)
        portal = c.post("/portal/auth/signup", json=body)
        member_login = c.post("/auth/login", json=body)
        portal_login = c.post("/portal/auth/login", json=body)
    refusal(member, 404, "not_found")
    refusal(portal, 404, "not_found")
    refusal(member_login, 401, "invalid_credentials")
    refusal(portal_login, 401, "invalid_credentials")


def test_other_company_booking_not_found_same_as_nonexistent():
    red, blue = portal_token(REDLINE), portal_token(BLUECREST)
    site = portal_site_id(blue)
    with http(blue, {"Idempotency-Key": uid("idem")}) as c:
        booking = expect(c.post(f"/portal/sites/{site}/bookings",
                                json=portal_booking_body(future_day(20), "13:00", "13:30")), 201)
    with http(red) as c:
        foreign = c.get(f"/portal/bookings/{booking['id']}")
        missing = c.get(f"/portal/bookings/{absent_id('apt')}")
    refusal(foreign, 404, "not_found")
    refusal(missing, 404, "not_found")
    assert body(foreign).get("message") == body(missing).get("message"), (
        f"another company's booking answers differently from a missing one: {foreign.text[:200]} | {missing.text[:200]}")


def test_unauthorised_site_booking_not_found_same_as_nonexistent():
    dallas = portal_site_id(portal_token(REDLINE))
    oak = portal_token(OAKRIDGE)
    payload = portal_booking_body(future_day(21), "13:00", "13:30")
    with http(oak, {"Idempotency-Key": uid("idem")}) as c:
        unauthorised = c.post(f"/portal/sites/{dallas}/bookings", json=payload)
    with http(oak, {"Idempotency-Key": uid("idem")}) as c:
        missing = c.post(f"/portal/sites/{absent_id('site')}/bookings", json=payload)
    refusal(unauthorised, 404, "not_found")
    refusal(missing, 404, "not_found")
    assert body(unauthorised).get("message") == body(missing).get("message"), (
        "a site the haulier is not authorised at answers differently from a missing site")


def test_availability_windows_expose_only_start_end():
    red = portal_token(REDLINE)
    site = portal_site_id(red)
    windows = read_json(red, f"/portal/sites/{site}/availability?date={future_day(22)}&direction=inbound&asset_type=dry_van")
    assert isinstance(windows, list) and windows, f"availability returned no windows: {windows}"
    leaked = [w for w in windows if set(w) != {"starts_at", "ends_at"}]
    assert not leaked, f"availability windows carry more than starts_at and ends_at: {leaked[:3]}"


def test_member_token_on_portal_principal_kind_mismatch():
    with http(member_token(MANAGER)) as c:
        member_on_portal = c.get("/portal/sites")
    with http(portal_token(REDLINE)) as c:
        portal_on_console = c.get("/sites")
    refusal(member_on_portal, 401, "principal_kind_mismatch")
    refusal(portal_on_console, 401, "principal_kind_mismatch")


def test_customer_fewer_than_five_loads_report_suppressed():
    praxis = portal_token(PRAXIS)
    site = portal_site_id(praxis)
    report = read_json(praxis, f"/portal/customer/report?site_id={site}&period=2026-09")
    assert report.get("suppressed") is True and report.get("loads") is None and report.get("median_dwell_seconds") is None, (
        f"a customer with three loads received an unsuppressed report: {report}")


def test_customer_six_loads_report_counts_loads():
    everwear = portal_token(EVERWEAR)
    site = portal_site_id(everwear)
    report = read_json(everwear, f"/portal/customer/report?site_id={site}&period=2026-09")
    assert report.get("suppressed") is False and report.get("loads") == 6, (
        f"a customer with six loads did not see its count: {report}")


def test_customer_loads_list_only_own_references():
    everwear = portal_token(EVERWEAR)
    site = portal_site_id(everwear)
    loads = read_json(everwear, f"/portal/customer/loads?site_id={site}&period=2026-09")
    references = {row.get("reference") for row in loads}
    assert references == EVERWEAR_LOADS, f"Everwear's load list is {sorted(references)}"


def test_custody_chain_tamper_detected_broken_at_sequence():
    mgr, dock = member_token(MANAGER), member_token(DOCK)
    site = site_id(dock, DAL1)
    asset = new_asset(mgr, site)
    custody_event(dock, site, asset, "arrived")
    second = custody_event(dock, site, asset, "sealed", upper_uid("SL"))
    custody_event(dock, site, asset, "released")
    with http(dock) as c:
        clean = expect(c.post(f"/sites/{site}/assets/{asset}/custody/verify"), 200)
    assert clean.get("valid") is True, f"an untouched chain does not verify: {clean}"
    tamper_seal_number(second["id"], upper_uid("FORGED"))
    with http(dock) as c:
        broken = expect(c.post(f"/sites/{site}/assets/{asset}/custody/verify"), 200)
    assert broken.get("valid") is False and broken.get("broken_at") == second["sequence"], (
        f"a rewritten seal number at sequence {second['sequence']} verified as {broken}")


def test_custody_correction_new_event_original_unchanged():
    mgr, dock = member_token(MANAGER), member_token(DOCK)
    site = site_id(dock, DAL1)
    asset = new_asset(mgr, site)
    original_seal = upper_uid("SL")
    original = custody_event(dock, site, asset, "sealed", original_seal)
    with http(dock) as c:
        correction = expect(c.post(f"/custody-events/{original['id']}/corrections",
                                   json={"reason": "seal misread", "seal_number": upper_uid("SL")}), 201)
    assert correction.get("kind") == "corrected" and correction.get("corrects") == original["id"], correction
    chain = read_json(dock, f"/sites/{site}/assets/{asset}/custody")
    events = chain.get("events", [])
    kept = [e for e in events if e.get("id") == original["id"]]
    assert len(events) == 2 and kept and kept[0].get("seal_number") == original_seal, (
        f"the correction rewrote the original event: {events}")


def test_app_credential_cannot_rewrite_custody_event_row():
    mgr, dock = member_token(MANAGER), member_token(DOCK)
    site = site_id(dock, DAL1)
    asset = new_asset(mgr, site)
    seal = upper_uid("SL")
    event = custody_event(dock, site, asset, "sealed", seal)
    with pytest.raises(Exception):
        app_db().query("UPDATE custody_event SET seal_number = %s WHERE id = %s", (upper_uid("FORGED"), event["id"]))
    rows = admin_db().query("SELECT seal_number FROM custody_event WHERE id = %s", (event["id"],))
    assert rows and rows[0]["seal_number"] == seal, f"the application credential changed a custody row: {rows}"


def test_custody_chain_hashes_link_prior_event():
    mgr, dock = member_token(MANAGER), member_token(DOCK)
    site = site_id(dock, DAL1)
    asset = new_asset(mgr, site)
    first = custody_event(dock, site, asset, "arrived")
    second = custody_event(dock, site, asset, "docked")
    assert first.get("sequence") == 1 and first.get("prior_hash") == ZERO_HASH, f"the first event is not anchored: {first}"
    assert second.get("prior_hash") == first.get("hash") and second.get("hash") != first.get("hash"), (
        f"the second event does not link to the first: {first} {second}")
    assert len(str(second.get("hash"))) == 64, f"a custody hash is not sixty four characters: {second}"


def test_booking_confirmation_email_once_on_idempotent_replay():
    red = portal_token(REDLINE)
    site = portal_site_id(red)
    key = uid("idem")
    payload = portal_booking_body(future_day(23), "14:00", "14:30")
    with http(red, {"Idempotency-Key": key}) as c:
        first = expect(c.post(f"/portal/sites/{site}/bookings", json=payload), 201)
        replay = expect(c.post(f"/portal/sites/{site}/bookings", json=payload), 201)
    assert replay.get("id") == first.get("id"), f"a replay created a second booking: {first} {replay}"
    reference = first["reference"]
    found = wait_for_mail(REDLINE, reference)
    assert found, f"no confirmation mail for {reference} reached {REDLINE}"
    settle(3.0)
    matching = messages_matching(REDLINE, reference)
    assert len(matching) == 1, f"{len(matching)} confirmation mails for {reference}, expected 1"
    assert matching[0].subject.startswith("Junction booking confirmed: "), matching[0].subject


def test_booking_confirmation_email_names_no_load_reference():
    red = portal_token(REDLINE)
    site = portal_site_id(red)
    load_reference = upper_uid("PXHIDDEN")
    with http(red, {"Idempotency-Key": uid("idem")}) as c:
        booking = expect(c.post(f"/portal/sites/{site}/bookings",
                                json=portal_booking_body(future_day(24), "14:00", "14:30",
                                                         load_reference=load_reference)), 201)
    found = wait_for_mail(REDLINE, booking["reference"])
    assert found, f"no confirmation mail for {booking['reference']}"
    message = found[0]
    assert load_reference not in message.subject and load_reference not in message.body, (
        f"the confirmation mail names the load reference {load_reference}")
    assert message.body.strip().startswith(booking["reference"]), (
        f"the confirmation mail body does not open with the booking reference: {message.body[:120]}")


def test_idempotency_key_reused_different_body_conflict():
    red = portal_token(REDLINE)
    site = portal_site_id(red)
    day = future_day(25)
    with http(red, {"Idempotency-Key": uid("idem")}) as c:
        expect(c.post(f"/portal/sites/{site}/bookings", json=portal_booking_body(day, "14:00", "14:30")), 201)
        reused = c.post(f"/portal/sites/{site}/bookings", json=portal_booking_body(day, "15:00", "15:30"))
    refusal(reused, 409, "idempotency_key_reused")


def test_visit_link_revoked_after_booking_cancelled():
    red = portal_token(REDLINE)
    site = portal_site_id(red)
    with http(red, {"Idempotency-Key": uid("idem")}) as c:
        booking = expect(c.post(f"/portal/sites/{site}/bookings",
                                json=portal_booking_body(future_day(26), "14:00", "14:30")), 201)
    token = booking["visit_link"].rstrip("/").rsplit("/", 1)[-1]
    with http() as c:
        expect(c.get(f"/visit-views/{token}"), 200)
    with http(red) as c:
        expect(c.post(f"/portal/bookings/{booking['id']}/cancel", json={"reason": "load moved"}), 200)
    with http() as c:
        refusal(c.get(f"/visit-views/{token}"), 410, "visit_link_revoked")


def test_visit_view_exposes_no_load_reference():
    red = portal_token(REDLINE)
    site = portal_site_id(red)
    load_reference = upper_uid("LOADREF")
    with http(red, {"Idempotency-Key": uid("idem")}) as c:
        booking = expect(c.post(f"/portal/sites/{site}/bookings",
                                json=portal_booking_body(future_day(27), "14:00", "14:30",
                                                         load_reference=load_reference)), 201)
    token = booking["visit_link"].rstrip("/").rsplit("/", 1)[-1]
    with http() as c:
        view = c.get(f"/visit-views/{token}")
    payload = expect(view, 200)
    assert payload.get("site_address") and payload.get("contact_number"), f"the visit view lacks the address or contact: {payload}"
    assert load_reference not in view.text, "the driver's visit view carries the load reference"


def test_approval_request_email_reaches_eligible_site_managers():
    gate = member_token(GATE)
    site = site_id(gate, DAL1)
    approval = request_release(gate, held_visit(gate, site)["id"])
    for recipient in (MANAGER, MANAGER2):
        found = wait_for_mail(recipient, approval["id"])
        assert found, f"{recipient} received no approval request mail for {approval['id']}"
        assert found[0].subject.startswith("Junction approval requested: "), found[0].subject


def test_approval_request_email_skips_requester_ineligible_member():
    gate = member_token(GATE)
    site = site_id(gate, DAL1)
    approval = request_release(gate, held_visit(gate, site)["id"])
    assert wait_for_mail(MANAGER, approval["id"]), f"no eligible approver was mailed for {approval['id']}"
    settle(3.0)
    assert not messages_matching(GATE, approval["id"]), "the requester was mailed their own approval request"
    assert not messages_matching(DUAL, approval["id"]), "a member ineligible at Dallas was mailed the approval request"


def test_active_watchlist_plate_visit_refused():
    gate = member_token(GATE)
    visit = record_visit(gate, site_id(gate, DAL1), PLATE_ACTIVE, REG_REDLINE)
    watch = [c for c in visit.get("checks", []) if c.get("kind") == "watchlist"]
    assert visit.get("state") == "refused" and watch and watch[0].get("result") == "fail", (
        f"an active watchlist plate was not refused: {visit}")


def test_expired_watchlist_plate_visit_not_refused():
    gate = member_token(GATE)
    visit = record_visit(gate, site_id(gate, DAL1), PLATE_EXPIRED, REG_REDLINE)
    watch = [c for c in visit.get("checks", []) if c.get("kind") == "watchlist"]
    assert visit.get("state") != "refused" and watch and watch[0].get("result") == "pass", (
        f"an expired watchlist entry still matched: {visit}")


def test_suspended_haulier_visit_held_authorisation_check():
    gate = member_token(GATE)
    visit = held_visit(gate, site_id(gate, DAL1))
    auth = [c for c in visit.get("checks", []) if c.get("kind") == "haulier_authorisation"]
    assert auth and auth[0].get("result") == "fail", f"the held visit does not fail haulier_authorisation: {visit}"


def test_shift_duration_across_fall_back_daylight_saving():
    mgr = member_token(MANAGER)
    with http(mgr) as c:
        shift = expect(c.post(f"/sites/{site_id(mgr, DAL1)}/shifts",
                              json={"member_email": SPOTTER, "starts_local": "2026-11-01T00:00",
                                    "ends_local": "2026-11-01T08:00"}), 201)
    assert shift.get("duration_seconds") == 32400, f"a Dallas shift across the fall back change lasts {shift.get('duration_seconds')}"


def test_shift_duration_across_spring_forward_daylight_saving():
    mgr = member_token(MANAGER)
    with http(mgr) as c:
        shift = expect(c.post(f"/sites/{site_id(mgr, DAL1)}/shifts",
                              json={"member_email": SPOTTER, "starts_local": "2027-03-14T00:00",
                                    "ends_local": "2027-03-14T08:00"}), 201)
    assert shift.get("duration_seconds") == 25200, f"a Dallas shift across the spring forward change lasts {shift.get('duration_seconds')}"


def test_shift_instants_carry_site_offset():
    mgr = member_token(MANAGER)
    with http(mgr) as c:
        shift = expect(c.post(f"/sites/{site_id(mgr, DAL1)}/shifts",
                              json={"member_email": SPOTTER, "starts_local": "2026-11-01T00:00",
                                    "ends_local": "2026-11-01T08:00"}), 201)
    start = datetime.fromisoformat(shift["starts_at"])
    end = datetime.fromisoformat(shift["ends_at"])
    assert start.utcoffset() is not None and start.utcoffset().total_seconds() == -18000, f"starts_at offset: {shift['starts_at']}"
    assert end.utcoffset() is not None and end.utcoffset().total_seconds() == -21600, f"ends_at offset: {shift['ends_at']}"


def test_unknown_path_answers_404_not_found_document():
    with site_client() as c:
        response = c.get(f"/no-such-yard-route-{uid('x')}")
    assert response.status_code == 404, f"an unknown address answered {response.status_code}"
    assert "Page not found" in response.text and 'href="/"' in response.text, (
        f"the not-found document lacks its heading or a link home: {response.text[:300]}")


def test_terms_page_answered_with_footer_terms_link():
    with site_client() as c:
        terms = c.get("/terms")
        home = c.get("/")
    assert terms.status_code == 200 and "Terms of use" in terms.text, f"the terms page answered {terms.status_code}"
    assert 'href="/terms"' in home.text, "the home document carries no footer link to the terms page"


def test_security_headers_on_every_response():
    with site_client() as c:
        responses = [c.get("/"), c.get("/terms"), c.get("/api/health"), c.get("/api/sites")]
    for r in responses:
        assert r.headers.get("x-content-type-options", "").lower() == "nosniff", (
            f"{r.request.url.path} lacks nosniff: {dict(r.headers)}")
        hsts = r.headers.get("strict-transport-security", "")
        max_age = [int(part.split("=", 1)[1]) for part in hsts.replace(" ", "").split(";")
                   if part.lower().startswith("max-age=") and part.split("=", 1)[1].isdigit()]
        assert max_age and max_age[0] > 0, f"{r.request.url.path} lacks a Strict-Transport-Security max-age: {hsts!r}"


def test_console_api_responses_cache_control_no_store():
    with http(member_token(MANAGER)) as c:
        console = c.get("/sites")
    with http(portal_token(REDLINE)) as c:
        portal = c.get("/portal/sites")
    for r in (console, portal):
        expect(r, 200)
        assert "no-store" in r.headers.get("cache-control", "").lower(), (
            f"{r.request.url.path} is storable: {r.headers.get('cache-control')!r}")


def test_unknown_api_path_not_found_code():
    with http(member_token(MANAGER)) as c:
        response = c.get(f"/no-such-endpoint-{uid('x')}")
    refusal(response, 404, "not_found")


def test_health_route_returns_200():
    with http() as c:
        response = c.get("/health")
    assert response.status_code == 200, f"GET /api/health answered {response.status_code}"


def test_contact_decoy_field_rejected_submission_nothing_stored():
    email = f"{uid('decoy')}@reyesfreight.example.com"
    with http() as c:
        response = c.post("/forms/contact", json=contact_body(email, decoy="https://reyes.example.com"))
    refusal(response, 422, "rejected_submission")
    assert admin_db().count("form_submission", email=email) == 0, "a decoy submission was stored"


def test_contact_fourth_submission_rate_limited_nothing_stored():
    email = f"{uid('burst')}@reyesfreight.example.com"
    with http() as c:
        for _ in range(3):
            expect(c.post("/forms/contact", json=contact_body(email)), 201)
        fourth = c.post("/forms/contact", json=contact_body(email))
    refusal(fourth, 429, "rate_limited")
    assert admin_db().count("form_submission", email=email) == 3, "the refused fourth submission was stored"


def test_contact_valid_submission_stored_form_submission_row():
    email = f"{uid('valid')}@reyesfreight.example.com"
    with http() as c:
        payload = expect(c.post("/forms/contact", json=contact_body(email)), 201)
    assert payload.get("id"), f"a valid contact submission returned no id: {payload}"
    assert admin_db().count("form_submission", email=email) == 1, "a valid contact submission was not stored"


def test_contact_replayed_submission_id_stored_once_single_row():
    email = f"{uid('replay')}@reyesfreight.example.com"
    payload = contact_body(email)
    with http() as c:
        first = expect(c.post("/forms/contact", json=payload), 201)
        second = expect(c.post("/forms/contact", json=payload), 201)
    assert second.get("id") == first.get("id"), f"a replayed submission answered a new id: {first} {second}"
    assert admin_db().count("form_submission", email=email) == 1, "a replayed submission stored a second row"


def test_page_view_log_denied_to_analyst():
    with http(member_token(ANALYST)) as c:
        response = c.get("/page-views")
    refusal(response, 403, "forbidden")


def test_page_view_recorded_for_public_route_read_by_publisher():
    with site_client() as c:
        about = c.get("/about")
    assert about.status_code == 200, f"GET /about answered {about.status_code}"
    publisher = member_token(PUBLISHER)
    views = poll(lambda: read_json(publisher, "/page-views"),
                 lambda rows: any(r.get("route") == "/about" for r in rows), 15.0)
    assert any(r.get("route") == "/about" and r.get("viewed_at") for r in views), (
        f"no page view for /about was recorded: {views[:5]}")


def test_grader_report_recomputes_score_ignoring_claimed_score():
    answers = [3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1, 0, 3, 2, 3]
    with http() as c:
        report = expect(c.post("/grader/reports",
                               json={"answers": answers, "score": 12,
                                     "email": f"{uid('grade')}@reyesfreight.example.com",
                                     "consent": True}), 202)
    layers = {row.get("id"): row for row in report.get("layers", [])}
    assert report.get("score") == 80 and report.get("band") == "Sealed yard", f"the report was not recomputed: {report}"
    assert layers.get("L03", {}).get("percent") == 11 and layers["L03"].get("status") == "Exposed", layers
    assert report.get("fix_route") == "/modules/load-verification", report.get("fix_route")


def test_grader_full_marks_fix_route_yard_security():
    with http() as c:
        report = expect(c.post("/grader/reports",
                               json={"answers": [3] * 15, "score": 0,
                                     "email": f"{uid('grade')}@reyesfreight.example.com",
                                     "consent": True}), 202)
    assert report.get("score") == 100 and report.get("fix_route") == "/yard-security", report
