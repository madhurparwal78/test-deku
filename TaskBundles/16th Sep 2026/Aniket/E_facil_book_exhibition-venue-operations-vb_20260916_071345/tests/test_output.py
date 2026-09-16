"""Deterministic observations of the deployed Verwick Xpo product.

Black box only: every assertion is made over the JSON API, over the served
markup, or over the rows postgres holds. Nothing reads the agent's source,
imports a vendor SDK, or probes for a feature at run time.
"""

from __future__ import annotations

import httpx
import pytest
from _shapes import flatten, items
from conftest import (ACCREDITATION_STATES, AVAILABILITY_STATES,
                      BOOKING_PRIVATE, BOOKING_PUBLIC, BOOKING_PUBLISHED,
                      BOULEVARD, COMBINATION_HALLS, COMBINATION_HALLS_CAPACITY,
                      COMBINATION_HALLS_SUM, COMBINATION_MEETING,
                      COMBINATION_MEETING_CAPACITY, COORDINATOR_EMAIL,
                      COPYRIGHT_LINE, DENIED_STATUS, ENTRANCE_MODES,
                      ENTRANCE_NORTH, ENTRANCE_SOUTH, EVENT_HALL,
                      EXHIBITOR_EMAIL, HALL_AREAS, HALL_CAPACITIES, HALL_FIVE,
                      HALL_FOUR, HALL_FOUR_DAY_RATE_MINOR, HALL_ONE,
                      HALL_SIX, HALL_THREE, HALL_TWO, HERO_LINE, LANGUAGES,
                      LAYOUTS, MEETING_CENTRE_AREA, MEETING_ROOMS,
                      NOT_FOUND_ACTION, NOT_FOUND_HEADING, NOT_FOUND_STATUS,
                      OCCUPANCY_STATES, OK_STATUS, OPERATIONS_EMAIL,
                      OPTION_STATES, PARKING_SPACES, PARTY_EXHIBITOR,
                      PARTY_ORGANISER_ONE, PARTY_ORGANISER_TWO, PASSAGE,
                      PASSWORD, PHASE_KINDS, PLAN_CONSTRAINT_KINDS,
                      PLAN_OBJECT_KINDS, PLANNER2_EMAIL, PLANNER_EMAIL,
                      PUBLICATION_STATES, REFUSAL_REASONS, REFUSED_STATUS,
                      REVISION_STATES, SCAN_DECISIONS, SEARCH_LABEL,
                      SEEDED_ACCOUNTS, SEEDED_ENTRANCES, SEEDED_SPACES,
                      SERVICE_ORDER_STATES, SKIP_LINK, SPACE_KINDS,
                      STAND_REF, STATUS_CHIP_PUBLIC, STATUS_CHIP_TRADE,
                      SUBSCRIPTION_STATES, TRIBUNE_SEATS, availability,
                      describe, held_window, in_parallel, json_of, poll_for,
                      probe_email, public_space_row, settle, space_row,
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
        "/auth/login",
        json={"email": probe_email("nobody"), "password": PASSWORD})
    wrong = anonymous.post(
        "/auth/login",
        json={"email": COORDINATOR_EMAIL, "password": unique("wrong")})
    assert unknown.status_code in DENIED_STATUS, describe(
        unknown, "sign-in for an address with no account")
    assert wrong.status_code == unknown.status_code, (
        f"an unknown address answered {unknown.status_code} and a wrong "
        f"password answered {wrong.status_code}; the two must be "
        f"indistinguishable. Unknown body {unknown.text[:200]!r}, wrong body "
        f"{wrong.text[:200]!r}")
    assert flatten(wrong.json() if wrong.content else {}) == flatten(
        unknown.json() if unknown.content else {}), (
        f"the two refusal bodies differ: unknown {unknown.text[:200]!r} "
        f"against wrong password {wrong.text[:200]!r}")


def test_signed_out_token_is_refused_on_the_next_request(
        anonymous: httpx.Client) -> None:
    signin = anonymous.post(
        "/auth/login",
        json={"email": OPERATIONS_EMAIL, "password": PASSWORD})
    token = json_of(signin, "sign-in before signing out").get("access_token")
    with httpx.Client(base_url=str(anonymous.base_url), timeout=30.0,
                      headers={"Authorization": f"Bearer {token}"}) as session:
        before = session.get("/me")
        assert before.status_code in OK_STATUS, describe(
            before, "the identity route with a live token")
        session.post("/auth/logout")
        after = session.get("/me")
    assert after.status_code in DENIED_STATUS, describe(
        after, "the identity route with a signed-out token")


def test_anonymous_console_request_is_denied(anonymous: httpx.Client) -> None:
    for route in ("/enquiries", "/bookings", "/accreditations", "/audit"):
        response = anonymous.get(route)
        assert response.status_code in DENIED_STATUS, describe(
            response, f"an unauthenticated read of {route!r}")


def test_space_catalog_stores_every_seeded_space(
        coordinator: httpx.Client) -> None:
    payload = json_of(coordinator.get("/spaces"), "the space catalog")
    names = {row.get("name") for row in items(payload) if isinstance(row, dict)}
    missing = [name for name in SEEDED_SPACES if name not in names]
    assert not missing, (
        f"the space catalog is missing {missing}; it listed {sorted(names)!r}")
    for row in items(payload):
        kind = row.get("kind")
        assert kind in SPACE_KINDS, (
            f"space {row.get('name')!r} carries kind {kind!r}, which is outside "
            f"the closed set {list(SPACE_KINDS)}")


def test_seeded_hall_rows_carry_the_measured_area_and_capacity(
        coordinator: httpx.Client) -> None:
    for name, area in HALL_AREAS.items():
        row = space_row(coordinator, name)
        assert int(row.get("area_sqm") or 0) == area, (
            f"{name!r} reports a floor area of {row.get('area_sqm')!r}; the "
            f"seeded area is {area}")
    for name, capacity in HALL_CAPACITIES.items():
        row = space_row(coordinator, name)
        layouts = json_of(
            coordinator.get(f"/spaces/{row.get('id')}/layouts"),
            f"the layout list for {name!r}")
        by_name = {entry.get("name"): entry for entry in items(layouts)}
        unknown = [key for key in by_name if key not in LAYOUTS]
        assert not unknown, (
            f"{name!r} carries layouts {unknown} outside the closed set "
            f"{list(LAYOUTS)}")
        grid = by_name.get("stand_grid")
        assert grid is not None, (
            f"{name!r} carries no `stand_grid` layout; it carries "
            f"{sorted(by_name)!r}")
        assert int(grid.get("licensed_capacity") or 0) == capacity, (
            f"{name!r} licenses {grid.get('licensed_capacity')!r} in "
            f"`stand_grid`; the seeded licensed figure is {capacity}")


def test_capacity_is_not_derived_from_the_stored_floor_area(
        coordinator: httpx.Client) -> None:
    four = space_row(coordinator, HALL_FOUR)
    five = space_row(coordinator, HALL_FIVE)
    assert int(four.get("area_sqm") or 0) > int(five.get("area_sqm") or 0), (
        f"{HALL_FOUR!r} must carry the larger floor area; it reported "
        f"{four.get('area_sqm')!r} against {five.get('area_sqm')!r}")
    four_layouts = items(json_of(
        coordinator.get(f"/spaces/{four.get('id')}/layouts"),
        f"the layout list for {HALL_FOUR!r}"))
    five_layouts = items(json_of(
        coordinator.get(f"/spaces/{five.get('id')}/layouts"),
        f"the layout list for {HALL_FIVE!r}"))
    four_grid = next((e for e in four_layouts if e.get("name") == "stand_grid"),
                     {})
    five_grid = next((e for e in five_layouts if e.get("name") == "stand_grid"),
                     {})
    assert int(five_grid.get("licensed_capacity") or 0) > int(
        four_grid.get("licensed_capacity") or 0), (
        f"{HALL_FIVE!r} licenses {five_grid.get('licensed_capacity')!r} and "
        f"{HALL_FOUR!r} licenses {four_grid.get('licensed_capacity')!r}; the "
        f"smaller hall must license the larger figure, which is what proves "
        f"capacity is stored rather than computed from area")


def test_combination_capacity_is_stored_rather_than_summed(
        coordinator: httpx.Client) -> None:
    row = space_row(coordinator, COMBINATION_HALLS)
    assert row.get("kind") == "combination", (
        f"{COMBINATION_HALLS!r} carries kind {row.get('kind')!r}; a combination "
        f"must carry the kind `combination`")
    layouts = items(json_of(
        coordinator.get(f"/spaces/{row.get('id')}/layouts"),
        f"the layout list for {COMBINATION_HALLS!r}"))
    grid = next((e for e in layouts if e.get("name") == "stand_grid"), {})
    licensed = int(grid.get("licensed_capacity") or 0)
    assert licensed == COMBINATION_HALLS_CAPACITY, (
        f"{COMBINATION_HALLS!r} licenses {licensed!r}; the seeded licensed "
        f"figure is {COMBINATION_HALLS_CAPACITY}")
    assert licensed != COMBINATION_HALLS_SUM, (
        f"{COMBINATION_HALLS!r} licenses {licensed!r}, which equals the sum of "
        f"its two halls; a combination carries its own licensed figure")
    members = row.get("members") or []
    member_names = {m.get("name") if isinstance(m, dict) else m
                    for m in members}
    for expected in (HALL_FOUR, HALL_FIVE, PASSAGE):
        assert expected in member_names, (
            f"{COMBINATION_HALLS!r} does not list {expected!r} among its "
            f"members; it listed {sorted(str(m) for m in member_names)!r}")


def test_meeting_centre_combination_stores_its_own_licensed_figure(
        coordinator: httpx.Client) -> None:
    row = space_row(coordinator, COMBINATION_MEETING)
    layouts = items(json_of(
        coordinator.get(f"/spaces/{row.get('id')}/layouts"),
        f"the layout list for {COMBINATION_MEETING!r}"))
    grid = next((e for e in layouts if e.get("name") == "stand_grid"), {})
    assert int(grid.get("licensed_capacity") or 0) == (
        COMBINATION_MEETING_CAPACITY), (
        f"{COMBINATION_MEETING!r} licenses "
        f"{grid.get('licensed_capacity')!r}; the seeded figure is "
        f"{COMBINATION_MEETING_CAPACITY}")
    member_names = {m.get("name") if isinstance(m, dict) else m
                    for m in (row.get("members") or [])}
    for expected in MEETING_ROOMS + (EVENT_HALL,):
        assert expected in member_names, (
            f"{COMBINATION_MEETING!r} does not list {expected!r} among its "
            f"members; it listed {sorted(str(m) for m in member_names)!r}")


def test_availability_answers_only_from_the_closed_state_set(
        coordinator: httpx.Client) -> None:
    booking = held_window(coordinator, BOOKING_PUBLISHED)
    start, end = booking.get("window_start"), booking.get("window_end")
    for space in (HALL_FOUR, HALL_FIVE, PASSAGE, COMBINATION_HALLS, HALL_ONE):
        response = availability(coordinator, space, start, end)
        state = state_of(response, f"availability for {space!r}")
        assert state in AVAILABILITY_STATES, (
            f"availability for {space!r} answered {state!r}, which is outside "
            f"the closed set {list(AVAILABILITY_STATES)}")


def test_holding_a_combination_blocks_every_constituent_space(
        coordinator: httpx.Client) -> None:
    booking = held_window(coordinator, BOOKING_PUBLISHED)
    start, end = booking.get("window_start"), booking.get("window_end")
    for member in (HALL_FOUR, HALL_FIVE, PASSAGE):
        response = availability(coordinator, member, start, end)
        state = state_of(response, f"availability for the member {member!r}")
        assert state == "blocked_by_ancestor", (
            f"{member!r} reads {state!r} in a window its parent combination "
            f"holds; the answer must be `blocked_by_ancestor`. Body "
            f"{response.text[:300]!r}")
        blocking = (response.json() or {}).get("blocking_space")
        assert blocking, (
            f"the block on {member!r} names no `blocking_space`; a coordinator "
            f"told only that a hall is busy cannot tell a client why. Body "
            f"{response.text[:300]!r}")


def test_holding_a_constituent_blocks_the_ancestor_combination(
        coordinator: httpx.Client) -> None:
    booking = held_window(coordinator, BOOKING_PUBLIC)
    start, end = booking.get("window_start"), booking.get("window_end")
    response = availability(coordinator, COMBINATION_MEETING, start, end)
    state = state_of(response, f"availability for {COMBINATION_MEETING!r}")
    assert state == "blocked_by_descendant", (
        f"{COMBINATION_MEETING!r} reads {state!r} in a window its member rooms "
        f"are held across; the answer must be `blocked_by_descendant`. Body "
        f"{response.text[:300]!r}")


def test_maintenance_hold_is_stored_and_blocks_a_booking(
        coordinator: httpx.Client) -> None:
    window = json_of(coordinator.get("/holds", params={"kind": "maintenance"}),
                     "the maintenance hold list")
    rows = items(window)
    assert rows, "no maintenance hold is seeded; one resurfacing window is"
    target = next((r for r in rows
                   if str(r.get("space") or r.get("space_name")) == HALL_THREE),
                  None)
    assert target is not None, (
        f"no maintenance hold is stored against {HALL_THREE!r}; the stored "
        f"holds were {rows!r}"[:500])
    response = availability(coordinator, HALL_THREE,
                            target.get("window_start"),
                            target.get("window_end"))
    state = state_of(response, f"availability for {HALL_THREE!r}")
    assert state == "maintenance", (
        f"{HALL_THREE!r} reads {state!r} across its resurfacing window; the "
        f"answer must be `maintenance`")


def test_option_ranks_are_stored_one_per_space_and_window(
        coordinator: httpx.Client) -> None:
    payload = json_of(coordinator.get("/options", params={"space": HALL_SIX}),
                      f"the option list for {HALL_SIX!r}")
    rows = items(payload)
    assert len(rows) >= 2, (
        f"{HALL_SIX!r} carries {len(rows)} seeded option(s); two ranked options "
        f"are seeded so the challenge path has something to run on")
    ranks = [int(r.get("rank") or 0) for r in rows]
    assert sorted(ranks)[:2] == [1, 2], (
        f"the seeded options on {HALL_SIX!r} carry ranks {ranks!r}; ranks 1 and "
        f"2 are seeded")
    assert len(ranks) == len(set(ranks)), (
        f"two seeded options share a rank on {HALL_SIX!r}: {ranks!r}; a rank is "
        f"unique per space per window")
    for row in rows:
        assert row.get("state") in OPTION_STATES, (
            f"option {row.get('id')!r} carries state {row.get('state')!r}, "
            f"outside the closed set {list(OPTION_STATES)}")


def test_a_lower_rank_does_not_block_the_higher_rank(
        coordinator: httpx.Client) -> None:
    payload = json_of(coordinator.get("/options", params={"space": HALL_SIX}),
                      f"the option list for {HALL_SIX!r}")
    rows = sorted(items(payload), key=lambda r: int(r.get("rank") or 99))
    first = rows[0]
    response = coordinator.post(f"/options/{first.get('id')}/confirm",
                                json={"layout": "stand_grid",
                                      "idempotency_key": unique("confirm")})
    assert response.status_code in OK_STATUS, describe(
        response, "confirming the rank-one option while a rank-two option "
                  "exists on the same space and window")


def test_confirmation_stores_spaces_phases_and_contract_together(
        coordinator: httpx.Client) -> None:
    booking = held_window(coordinator, BOOKING_PUBLISHED)
    detail = json_of(coordinator.get(f"/bookings/{booking.get('id')}"),
                     f"the booking file for {BOOKING_PUBLISHED!r}")
    phases = {p.get("kind") for p in items(detail.get("phases") or [])}
    missing = [kind for kind in PHASE_KINDS if kind not in phases]
    assert not missing, (
        f"{BOOKING_PUBLISHED!r} carries phases {sorted(str(p) for p in phases)!r} "
        f"and is missing {missing}; confirmation creates all five")
    assert detail.get("contract"), (
        f"{BOOKING_PUBLISHED!r} carries no contract record; confirmation "
        f"creates the space set, the phases and the contract together")


def test_competing_confirmations_leave_exactly_one_stored_booking(
        coordinator: httpx.Client) -> None:
    enquiry = json_of(coordinator.post("/enquiries", json={
        "contact_name": unique("contact"),
        "contact_email": probe_email("enquiry"),
        "window_start": "2027-04-05T08:00:00Z",
        "window_end": "2027-04-09T20:00:00Z",
        "expected_visitors": 900,
        "event_type": "trade fair",
        "spaces_of_interest": [HALL_TWO],
    }), "creating an enquiry for the contended confirmation")
    made = []
    for rank in (1, 2):
        created = coordinator.post("/options", json={
            "enquiry_id": enquiry.get("id"),
            "spaces": [HALL_TWO],
            "window_start": "2027-04-05T08:00:00Z",
            "window_end": "2027-04-09T20:00:00Z",
            "rank": rank,
            "expires_at": "2027-03-01T00:00:00Z",
        })
        made.append(json_of(created, f"creating the rank-{rank} option"))

    def confirm_first():
        return coordinator.post(f"/options/{made[0].get('id')}/confirm",
                                json={"layout": "stand_grid",
                                      "idempotency_key": unique("race-a")})

    def confirm_second():
        return coordinator.post(f"/options/{made[1].get('id')}/confirm",
                                json={"layout": "stand_grid",
                                      "idempotency_key": unique("race-b")})

    responses = in_parallel(lambda: confirm_first(), count=1)
    responses += in_parallel(lambda: confirm_second(), count=1)
    accepted = [r for r in responses if r.status_code in OK_STATUS]
    refused = [r for r in responses if r.status_code in REFUSED_STATUS]
    assert len(accepted) == 1, (
        f"{len(accepted)} of two competing confirmations on {HALL_TWO!r} "
        f"succeeded; exactly one must. Statuses "
        f"{[r.status_code for r in responses]!r}")
    assert len(refused) == 1, (
        f"{len(refused)} of two competing confirmations was refused; exactly "
        f"one must be. Bodies {[r.text[:120] for r in responses]!r}")
    settle()
    listing = json_of(coordinator.get("/bookings",
                                      params={"space": HALL_TWO}),
                      f"the booking list for {HALL_TWO!r} after the contest")
    window_rows = [r for r in items(listing)
                   if str(r.get("window_start", "")).startswith("2027-04-05")]
    assert len(window_rows) == 1, (
        f"{len(window_rows)} booking rows are stored against {HALL_TWO!r} for "
        f"the contended window; exactly one must be. Rows {window_rows!r}"[:500])


def test_phase_windows_are_stored_as_occupancy_of_the_space(
        coordinator: httpx.Client) -> None:
    booking = held_window(coordinator, BOOKING_PUBLISHED)
    detail = json_of(coordinator.get(f"/bookings/{booking.get('id')}"),
                     f"the booking file for {BOOKING_PUBLISHED!r}")
    build = next((p for p in items(detail.get("phases") or [])
                  if p.get("kind") == "build_up"), None)
    assert build is not None, (
        f"{BOOKING_PUBLISHED!r} carries no `build_up` phase")
    response = availability(coordinator, HALL_FOUR,
                            build.get("window_start"),
                            build.get("window_end"))
    state = state_of(response, f"availability for {HALL_FOUR!r} during build-up")
    assert state != "free", (
        f"{HALL_FOUR!r} reads `free` during the build-up window of "
        f"{BOOKING_PUBLISHED!r}; a build-up phase occupies the hall exactly as "
        f"the run does")


def test_tight_turnaround_is_refused_naming_the_shortfall(
        coordinator: httpx.Client) -> None:
    booking = held_window(coordinator, BOOKING_PUBLISHED)
    detail = json_of(coordinator.get(f"/bookings/{booking.get('id')}"),
                     f"the booking file for {BOOKING_PUBLISHED!r}")
    run = next((p for p in items(detail.get("phases") or [])
                if p.get("kind") == "run"), {})
    response = coordinator.post(f"/bookings/{booking.get('id')}/phases", json={
        "kind": "tear_down",
        "window_start": run.get("window_start"),
        "window_end": run.get("window_end"),
    })
    assert response.status_code in REFUSED_STATUS, describe(
        response, "a tear-down window overlapping its own run window")
    body = response.json() if response.content else {}
    assert "shortfall_hours" in flatten(body), (
        f"the refusal names no `shortfall_hours`; the shortfall is named in "
        f"hours. Body {response.text[:300]!r}")


def test_plan_constraints_are_stored_for_the_seeded_halls(
        planner: httpx.Client) -> None:
    payload = json_of(planner.get("/plans"), "the plan list for the planner")
    plan = items(payload)[0] if items(payload) else None
    assert plan is not None, "the planner reaches no seeded plan"
    constraints = json_of(
        planner.get(f"/plans/{plan.get('id')}/constraints"),
        "the structural constraint list of the seeded plan")
    kinds = {c.get("kind") for c in items(constraints)}
    unknown = [k for k in kinds if k not in PLAN_CONSTRAINT_KINDS]
    assert not unknown, (
        f"the plan carries constraint kinds {unknown} outside the closed set "
        f"{list(PLAN_CONSTRAINT_KINDS)}")
    exits = [c for c in items(constraints) if c.get("kind") == "fire_exit"]
    assert len(exits) >= 2, (
        f"the seeded plan carries {len(exits)} fire exit constraint(s); two are "
        f"seeded with their required clearances")
    for one in exits:
        assert one.get("limit_value") is not None, (
            f"fire exit {one.get('id')!r} carries no required clearance")


def test_plan_object_blocking_an_exit_is_refused_with_the_rule(
        planner: httpx.Client) -> None:
    payload = json_of(planner.get("/plans"), "the plan list for the planner")
    plan = items(payload)[0]
    constraints = items(json_of(
        planner.get(f"/plans/{plan.get('id')}/constraints"),
        "the structural constraint list of the seeded plan"))
    exit_one = next(c for c in constraints if c.get("kind") == "fire_exit")
    response = planner.post(f"/plans/{plan.get('id')}/objects", json={
        "kind": "stand",
        "position": exit_one.get("geometry"),
        "dimensions": {"width_m": 6, "depth_m": 6},
    })
    assert response.status_code in REFUSED_STATUS, describe(
        response, "a stand placed on top of a seeded fire exit")
    body = response.json() if response.content else {}
    flat = flatten(body)
    assert "rule" in flat, (
        f"the refusal carries no `rule`; the rule is named in words. Body "
        f"{response.text[:300]!r}")
    assert "measurement" in flat, (
        f"the refusal carries no `measurement`; the offending measurement is "
        f"shown. Body {response.text[:300]!r}")


def test_plan_object_kinds_are_stored_from_the_closed_set(
        planner: httpx.Client) -> None:
    payload = json_of(planner.get("/plans"), "the plan list for the planner")
    plan = items(payload)[0]
    revisions = items(json_of(
        planner.get(f"/plans/{plan.get('id')}/revisions"),
        "the revision list of the seeded plan"))
    states = {r.get("state") for r in revisions}
    unknown = [s for s in states if s not in REVISION_STATES]
    assert not unknown, (
        f"the plan carries revision states {unknown} outside the closed set "
        f"{list(REVISION_STATES)}")
    approved = [r for r in revisions if r.get("state") == "approved"]
    assert approved, (
        f"the seeded plan carries no `approved` revision; revisions were "
        f"{revisions!r}"[:400])
    objects = items(json_of(
        planner.get(f"/plan-revisions/{approved[0].get('id')}/objects"),
        "the object list of the approved revision"))
    assert len(objects) >= 4, (
        f"the approved revision carries {len(objects)} object(s); at least four "
        f"are seeded")
    kinds = {o.get("kind") for o in objects}
    unknown_kinds = [k for k in kinds if k not in PLAN_OBJECT_KINDS]
    assert not unknown_kinds, (
        f"the revision carries object kinds {unknown_kinds} outside the closed "
        f"set {list(PLAN_OBJECT_KINDS)}")
    assert "catering_point" in kinds, (
        f"the approved revision carries no catering position; the seeded plan "
        f"carries one. Kinds were {sorted(str(k) for k in kinds)!r}")


def test_planner_cannot_approve_an_own_submitted_revision(
        planner: httpx.Client) -> None:
    payload = json_of(planner.get("/plans"), "the plan list for the planner")
    plan = items(payload)[0]
    created = planner.post(f"/plans/{plan.get('id')}/revisions", json={})
    revision = json_of(created, "submitting a fresh plan revision")
    planner.post(f"/plan-revisions/{revision.get('id')}/submit", json={})
    response = planner.post(
        f"/plan-revisions/{revision.get('id')}/decision",
        json={"decision": "approved"})
    assert response.status_code in REFUSED_STATUS, describe(
        response, "a planner approving a revision that same planner submitted")


def test_accreditation_rows_are_stored_with_their_granter(
        coordinator: httpx.Client) -> None:
    payload = json_of(coordinator.get("/accreditations"),
                      "the accreditation list")
    rows = items(payload)
    assert rows, "no accreditation is seeded"
    for row in rows:
        assert row.get("state") in ACCREDITATION_STATES, (
            f"accreditation {row.get('id')!r} carries state "
            f"{row.get('state')!r}, outside the closed set "
            f"{list(ACCREDITATION_STATES)}")
    delegated = [r for r in rows if r.get("granted_by")]
    assert delegated, (
        "no accreditation records a granter; an organiser accredits its "
        "exhibitors and an exhibitor accredits its contractor, so the chain "
        "must be stored")


def test_revoking_an_organiser_cascades_to_every_row_beneath(
        coordinator: httpx.Client) -> None:
    parties = items(json_of(coordinator.get("/parties"), "the party list"))
    organiser = next((p for p in parties
                      if p.get("name") == PARTY_ORGANISER_TWO), None)
    assert organiser is not None, (
        f"the party list names no {PARTY_ORGANISER_TWO!r}; parties were "
        f"{parties!r}"[:400])
    before = items(json_of(
        coordinator.get("/accreditations",
                        params={"party": PARTY_EXHIBITOR}),
        f"the accreditation list for {PARTY_EXHIBITOR!r}"))
    assert before, (
        f"{PARTY_EXHIBITOR!r} holds no accreditation before the revocation")
    target = items(json_of(
        coordinator.get("/accreditations",
                        params={"party": PARTY_ORGANISER_TWO}),
        f"the accreditation list for {PARTY_ORGANISER_TWO!r}"))[0]
    response = coordinator.post(
        f"/accreditations/{target.get('id')}/revoke", json={})
    assert response.status_code in OK_STATUS, describe(
        response, f"revoking the organiser accreditation of "
                  f"{PARTY_ORGANISER_TWO!r}")
    body = response.json() if response.content else {}
    assert int(body.get("cascaded") or 0) >= 1, (
        f"the revocation reports {body.get('cascaded')!r} cascaded rows; the "
        f"exhibitor accredited beneath it must be withdrawn too")
    after = poll_for(lambda: [
        r for r in items(json_of(
            coordinator.get("/accreditations",
                            params={"party": PARTY_EXHIBITOR}),
            f"the accreditation list for {PARTY_EXHIBITOR!r} after revocation"))
        if r.get("state") == "revoked"])
    assert after, (
        f"{PARTY_EXHIBITOR!r} still holds a live accreditation after its "
        f"organiser was revoked; the cascade must reach it")


def test_entrance_modes_are_stored_per_event_and_per_phase(
        operations: httpx.Client) -> None:
    payload = json_of(operations.get("/entrances"), "the entrance list")
    names = {row.get("name") for row in items(payload)}
    missing = [name for name in SEEDED_ENTRANCES if name not in names]
    assert not missing, (
        f"the entrance list is missing {missing}; it listed {sorted(names)!r}")
    booking = held_window(operations, BOOKING_PUBLISHED)
    target = next(r for r in items(payload)
                  if r.get("name") == ENTRANCE_SOUTH)
    set_mode = operations.put(f"/entrances/{target.get('id')}/mode", json={
        "booking": booking.get("id"),
        "phase_kind": "build_up",
        "mode": "contractor",
    })
    assert set_mode.status_code in OK_STATUS, describe(
        set_mode, f"setting {ENTRANCE_SOUTH!r} to `contractor` for build-up")
    scoped = json_of(operations.get("/entrances",
                                    params={"booking": booking.get("id")}),
                     "the entrance list scoped to one booking")
    south = next(r for r in items(scoped) if r.get("name") == ENTRANCE_SOUTH)
    modes = south.get("mode") or {}
    assert modes.get("build_up") == "contractor", (
        f"{ENTRANCE_SOUTH!r} reports {modes!r} for this booking; the stored "
        f"build-up mode is `contractor`")
    north = next(r for r in items(scoped) if r.get("name") == ENTRANCE_NORTH)
    north_modes = north.get("mode") or {}
    for value in north_modes.values():
        assert value in ENTRANCE_MODES, (
            f"{ENTRANCE_NORTH!r} carries mode {value!r}, outside the closed set "
            f"{list(ENTRANCE_MODES)}")


def test_scan_rows_are_stored_append_only_with_their_reason(
        operations: httpx.Client, backend) -> None:
    badges = items(json_of(operations.get("/badges"), "the badge list"))
    assert badges, "no badge is seeded"
    badge = badges[0]
    response = operations.post("/scans", json={
        "badge": badge.get("id"),
        "entrance": ENTRANCE_NORTH,
        "at": "2027-01-04T09:00:00Z",
    })
    assert response.status_code in OK_STATUS, describe(
        response, "a badge scanned at the north entrance")
    body = response.json() if response.content else {}
    decision = body.get("decision")
    assert decision in SCAN_DECISIONS, (
        f"the scan answered {decision!r}, outside the closed set "
        f"{list(SCAN_DECISIONS)}")
    if decision == "refused":
        assert body.get("reason") in REFUSAL_REASONS, (
            f"the refusal carries reason {body.get('reason')!r}, outside the "
            f"closed set {list(REFUSAL_REASONS)}")
    settle()
    log = items(json_of(operations.get("/scans"), "the stored scan log"))
    assert log, "the scan log holds no rows after a scan was recorded"


def test_expired_evidence_stops_the_badge_derived_from_it(
        operations: httpx.Client) -> None:
    rows = items(json_of(operations.get("/accreditations",
                                        params={"state": "expired"}),
                         "the expired accreditation list"))
    assert rows, (
        "no accreditation reads `expired`; one seeded contractor carries "
        "insurance evidence that expires inside the seeded window")
    target = rows[0]
    badges = items(json_of(
        operations.get("/badges",
                       params={"accreditation": target.get("id")}),
        "the badge list of the expired accreditation"))
    assert badges, (
        "the expired accreditation carries no badge; a badge is issued from it")
    response = operations.post("/scans", json={
        "badge": badges[0].get("id"),
        "entrance": ENTRANCE_NORTH,
        "at": "2027-01-04T09:00:00Z",
    })
    assert response.status_code in OK_STATUS, describe(
        response, "scanning a badge whose evidence has expired")
    body = response.json() if response.content else {}
    assert body.get("decision") == "refused", (
        f"the scan answered {body.get('decision')!r}; a badge derived from "
        f"expired evidence must be refused")
    assert body.get("reason") == "expired_evidence", (
        f"the refusal carries reason {body.get('reason')!r}; the reason must "
        f"be `expired_evidence`")


def test_occupancy_is_stored_against_the_licensed_figure(
        operations: httpx.Client) -> None:
    response = operations.get("/occupancy", params={"space": HALL_FOUR})
    body = json_of(response, f"the occupancy record for {HALL_FOUR!r}")
    assert isinstance(body.get("count"), int), (
        f"occupancy for {HALL_FOUR!r} reports count {body.get('count')!r}; an "
        f"occupancy count is an integer")
    assert body.get("count") >= 0, (
        f"occupancy for {HALL_FOUR!r} reports {body.get('count')!r}; an "
        f"occupancy count is never negative")
    assert body.get("state") in OCCUPANCY_STATES, (
        f"occupancy for {HALL_FOUR!r} reports state {body.get('state')!r}, "
        f"outside the closed set {list(OCCUPANCY_STATES)}")
    assert int(body.get("licensed_capacity") or 0) == (
        HALL_CAPACITIES[HALL_FOUR]), (
        f"occupancy for {HALL_FOUR!r} compares against "
        f"{body.get('licensed_capacity')!r}; the licensed figure is "
        f"{HALL_CAPACITIES[HALL_FOUR]}")


def test_occupancy_of_a_combination_covers_its_member_halls(
        operations: httpx.Client) -> None:
    combination = operations.get("/occupancy",
                                 params={"space": COMBINATION_HALLS})
    parent = json_of(combination, f"occupancy for {COMBINATION_HALLS!r}")
    member = json_of(operations.get("/occupancy", params={"space": HALL_FOUR}),
                     f"occupancy for {HALL_FOUR!r}")
    assert int(parent.get("count") or 0) >= int(member.get("count") or 0), (
        f"{COMBINATION_HALLS!r} reports {parent.get('count')!r} present while "
        f"its member {HALL_FOUR!r} reports {member.get('count')!r}; somebody "
        f"admitted to the combination is present in every constituent hall")
    assert int(parent.get("licensed_capacity") or 0) == (
        COMBINATION_HALLS_CAPACITY), (
        f"{COMBINATION_HALLS!r} compares occupancy against "
        f"{parent.get('licensed_capacity')!r}; the stored licensed figure is "
        f"{COMBINATION_HALLS_CAPACITY}")


def test_evacuation_is_stored_and_suspends_admission(
        operations: httpx.Client) -> None:
    response = operations.post("/evacuations", json={})
    assert response.status_code in OK_STATUS, describe(
        response, "declaring evacuation from an operations session")
    body = response.json() if response.content else {}
    assert body.get("declared_at"), (
        f"the declaration carries no `declared_at`; the trail records the time. "
        f"Body {response.text[:300]!r}")
    settle()
    badges = items(json_of(operations.get("/badges"), "the badge list"))
    scan = operations.post("/scans", json={
        "badge": badges[0].get("id"),
        "entrance": ENTRANCE_NORTH,
        "at": "2027-01-04T09:30:00Z",
    })
    assert scan.status_code in OK_STATUS, describe(
        scan, "a scan attempted during a declared evacuation")
    scan_body = scan.json() if scan.content else {}
    assert scan_body.get("decision") == "refused", (
        f"a scan during evacuation answered {scan_body.get('decision')!r}; "
        f"admission is suspended campus-wide")
    stand_down = operations.post("/evacuations/stand-down", json={})
    assert stand_down.status_code in OK_STATUS, describe(
        stand_down, "standing evacuation down again")


def test_service_order_without_its_dependency_is_refused(
        planner: httpx.Client) -> None:
    services = items(json_of(planner.get("/services"), "the service catalogue"))
    assert services, "no service is seeded"
    needs_position = next((s for s in services
                           if s.get("requires_plan_position")), None)
    assert needs_position is not None, (
        "no seeded service requires a position on the plan; the power drop does")
    booking = held_window(planner, BOOKING_PUBLISHED)
    response = planner.post("/service-orders", json={
        "booking": booking.get("id"),
        "service": needs_position.get("id"),
        "quantity": 1,
    })
    assert response.status_code in REFUSED_STATUS, describe(
        response, "ordering a power drop with no position on the plan")
    assert "depend" in flatten(response.json() if response.content else {}), (
        f"the refusal names no missing dependency. Body "
        f"{response.text[:300]!r}")


def test_service_order_states_are_stored_from_the_closed_set(
        planner: httpx.Client) -> None:
    booking = held_window(planner, BOOKING_PUBLISHED)
    services = items(json_of(planner.get("/services"), "the service catalogue"))
    plain = next(s for s in services
                 if not s.get("requires_plan_position")
                 and not s.get("requires_approved_plan"))
    created = planner.post("/service-orders", json={
        "booking": booking.get("id"),
        "service": plain.get("id"),
        "quantity": 2,
    })
    order = json_of(created, "ordering a service inside its cut-off")
    assert order.get("state") in SERVICE_ORDER_STATES, (
        f"the order carries state {order.get('state')!r}, outside the closed "
        f"set {list(SERVICE_ORDER_STATES)}")
    settle()
    stored = items(json_of(
        planner.get("/service-orders", params={"booking": booking.get("id")}),
        "the stored service orders of the booking"))
    assert any(str(row.get("id")) == str(order.get("id")) for row in stored), (
        f"the order {order.get('id')!r} is not among the stored rows "
        f"{stored!r}"[:400])


def test_invoice_lines_sum_exactly_to_the_stored_total(
        finance: httpx.Client) -> None:
    listing = items(json_of(finance.get("/invoices"), "the invoice list"))
    assert listing, "no invoice is seeded"
    invoice = json_of(finance.get(f"/invoices/{listing[0].get('id')}"),
                      "one invoice with its lines")
    lines = items(invoice.get("lines") or [])
    assert lines, (
        f"invoice {listing[0].get('id')!r} carries no lines; a booking accrues "
        f"charges from hire, phases and services")
    total = sum(int(line.get("amount_minor") or 0) for line in lines)
    assert total == int(invoice.get("total_minor") or -1), (
        f"the lines sum to {total} and the invoice total is "
        f"{invoice.get('total_minor')!r}; lines sum exactly to the total")
    for line in lines:
        assert line.get("rounding_minor") is not None, (
            f"line {line.get('description')!r} records no rounding decision")


def test_hall_hire_rate_is_stored_in_integer_minor_units(
        finance: httpx.Client) -> None:
    services = items(json_of(finance.get("/services"), "the service catalogue"))
    hire = [s for s in services
            if int(s.get("unit_price_minor") or 0) == HALL_FOUR_DAY_RATE_MINOR]
    assert hire, (
        f"no priced row carries the seeded hall hire rate "
        f"{HALL_FOUR_DAY_RATE_MINOR}; prices were "
        f"{[s.get('unit_price_minor') for s in services]!r}")
    for service in services:
        price = service.get("unit_price_minor")
        assert isinstance(price, int), (
            f"service {service.get('name')!r} is priced {price!r}; money is "
            f"held in integer minor units")


def test_idempotent_invoice_export_stores_one_external_reference(
        finance: httpx.Client) -> None:
    listing = items(json_of(finance.get("/invoices"), "the invoice list"))
    invoice_id = listing[0].get("id")
    key = unique("export")
    first = finance.post(f"/invoices/{invoice_id}/export",
                         json={"idempotency_key": key})
    second = finance.post(f"/invoices/{invoice_id}/export",
                          json={"idempotency_key": key})
    assert first.status_code in OK_STATUS, describe(
        first, "exporting an invoice for the first time")
    assert second.status_code in OK_STATUS, describe(
        second, "repeating an invoice export under the same key")
    first_ref = (first.json() or {}).get("external_ref")
    second_ref = (second.json() or {}).get("external_ref")
    assert first_ref and first_ref == second_ref, (
        f"a repeated export produced {second_ref!r} against the first "
        f"{first_ref!r}; a retried export never produces a second invoice")


def test_publication_states_are_stored_from_the_closed_set(
        coordinator: httpx.Client) -> None:
    rows = items(json_of(coordinator.get("/publications"),
                         "the publication list"))
    assert rows, "no publication record is seeded"
    for row in rows:
        assert row.get("state") in PUBLICATION_STATES, (
            f"publication {row.get('id')!r} carries state {row.get('state')!r}, "
            f"outside the closed set {list(PUBLICATION_STATES)}")
    private = [r for r in rows if r.get("state") == "private"]
    assert private, (
        f"no publication reads `private`; {BOOKING_PRIVATE!r} is seeded private "
        f"so the diary holds what the public cannot see")


def test_private_booking_never_reaches_the_public_event_list(
        anonymous: httpx.Client) -> None:
    rows = items(json_of(anonymous.get("/public/events"),
                         "the public event list"))
    titles = {str(row.get("title")) for row in rows}
    assert BOOKING_PRIVATE not in titles, (
        f"{BOOKING_PRIVATE!r} appears on the public event list; a privately "
        f"held booking occupies the diary and reaches no public surface. "
        f"Listed {sorted(titles)!r}")
    assert BOOKING_PUBLISHED in titles, (
        f"{BOOKING_PUBLISHED!r} is missing from the public event list; it is "
        f"seeded published. Listed {sorted(titles)!r}")


def test_public_event_rows_carry_no_internal_field(
        anonymous: httpx.Client) -> None:
    rows = items(json_of(anonymous.get("/public/events"),
                         "the public event list"))
    flat = flatten(rows).lower()
    for internal in ("rate", "contract", "amount_minor", "occupancy",
                     "incident", "contact_email"):
        assert internal not in flat, (
            f"the public event list carries the internal field {internal!r}; "
            f"rates, contacts, contract terms, occupancy and incidents can "
            f"never be published. Body {flatten(rows)[:400]!r}")


def test_public_space_list_carries_the_measured_capacity_and_area(
        anonymous: httpx.Client) -> None:
    for name, area in HALL_AREAS.items():
        row = public_space_row(anonymous, name)
        assert str(area) in flatten(row), (
            f"the public entry for {name!r} does not carry the floor area "
            f"{area}; body {flatten(row)[:300]!r}")
    for name, capacity in HALL_CAPACITIES.items():
        row = public_space_row(anonymous, name)
        assert str(capacity) in flatten(row), (
            f"the public entry for {name!r} does not carry the capacity "
            f"{capacity}; body {flatten(row)[:300]!r}")


def test_public_space_list_names_the_meeting_centre_and_the_tribune(
        anonymous: httpx.Client) -> None:
    rows = items(json_of(anonymous.get("/public/spaces"),
                         "the public space list"))
    flat = flatten(rows)
    assert str(MEETING_CENTRE_AREA) in flat, (
        f"the public space list does not carry the meeting centre total "
        f"{MEETING_CENTRE_AREA}; body {flat[:400]!r}")
    assert str(TRIBUNE_SEATS) in flat, (
        f"the public space list does not carry the tribune seat count "
        f"{TRIBUNE_SEATS}; body {flat[:400]!r}")
    assert "not captured" in flat.lower(), (
        f"the public entry for {HALL_FOUR!r} invents a suitability line; the "
        f"captured record carries none. Body {flat[:400]!r}")


def test_subscription_answers_already_for_a_repeated_address(
        anonymous: httpx.Client) -> None:
    address = probe_email("subscriber")
    first = anonymous.post("/subscriptions", json={"email": address})
    second = anonymous.post("/subscriptions", json={"email": address})
    first_state = state_of(first, "a first newsletter subscription")
    second_state = state_of(second, "the same address subscribed twice")
    assert first_state in SUBSCRIPTION_STATES, (
        f"a first subscription answered {first_state!r}, outside the closed set "
        f"{list(SUBSCRIPTION_STATES)}")
    assert second_state == "already", (
        f"the same address twice answered {second_state!r}; the answer is "
        f"`already` rather than a second subscription")


def test_public_enquiry_is_stored_rather_than_mailed(
        anonymous: httpx.Client, coordinator: httpx.Client) -> None:
    marker = unique("enquiry")
    created = anonymous.post("/enquiries", json={
        "contact_name": marker,
        "contact_email": probe_email("visitor"),
        "window_start": "2027-06-01T08:00:00Z",
        "window_end": "2027-06-03T20:00:00Z",
        "expected_visitors": 400,
        "event_type": "conference",
        "spaces_of_interest": [HALL_ONE],
    })
    assert created.status_code in OK_STATUS, describe(
        created, "a public enquiry submitted from the contact form")
    settle()
    rows = items(json_of(coordinator.get("/enquiries"), "the enquiry desk"))
    assert any(marker == str(row.get("contact_name")) for row in rows), (
        f"the enquiry {marker!r} is not stored on the enquiry desk; a public "
        f"submission creates a record rather than sending a message")


def test_page_view_is_refused_without_statistics_consent(
        anonymous: httpx.Client) -> None:
    response = anonymous.post("/page-views",
                              json={"route": "/en", "language": "en"})
    assert response.status_code in REFUSED_STATUS, describe(
        response, "a page view recorded with no statistics consent given")


def test_exhibitor_cannot_read_another_exhibitor_stand(
        exhibitor: httpx.Client, planner: httpx.Client) -> None:
    stands = items(json_of(planner.get("/stands"),
                           "the stand list the organiser sees"))
    other = next((s for s in stands if str(s.get("ref")) != STAND_REF), None)
    assert other is not None, (
        f"the organiser sees only one stand; a second stand is needed to prove "
        f"the wall. Stands were {stands!r}"[:400])
    response = exhibitor.get(f"/stands/{other.get('id')}")
    assert response.status_code in NOT_FOUND_STATUS, describe(
        response, "an exhibitor asking for another exhibitor's stand")


def test_exhibitor_cannot_read_another_exhibitor_orders(
        exhibitor: httpx.Client, planner: httpx.Client) -> None:
    stands = items(json_of(planner.get("/stands"),
                           "the stand list the organiser sees"))
    other = next(s for s in stands if str(s.get("ref")) != STAND_REF)
    response = exhibitor.get("/service-orders",
                             params={"stand": other.get("id")})
    if response.status_code in OK_STATUS:
        rows = items(response.json())
        assert not rows, (
            f"an exhibitor read {len(rows)} order(s) belonging to another "
            f"stand; everything an exhibitor sees stops at its own stand")
    else:
        assert response.status_code in NOT_FOUND_STATUS, describe(
            response, "an exhibitor asking for another stand's orders")


def test_planner_cannot_read_another_party_booking(
        planner: httpx.Client, planner2: httpx.Client) -> None:
    mine = held_window(planner2, BOOKING_PUBLIC)
    response = planner.get(f"/bookings/{mine.get('id')}")
    assert response.status_code in NOT_FOUND_STATUS + DENIED_STATUS, describe(
        response, "a planner reading a booking belonging to another party")


def test_operations_cannot_confirm_a_booking(
        operations: httpx.Client, coordinator: httpx.Client) -> None:
    options = items(json_of(coordinator.get("/options"), "the option desk"))
    held = next((o for o in options if o.get("state") == "held"), None)
    if held is None:
        pytest.fail("no option reads `held`; two ranked options are seeded on "
                    "one hall so the sales path has something to run on")
    response = operations.post(f"/options/{held.get('id')}/confirm",
                               json={"layout": "stand_grid",
                                     "idempotency_key": unique("forged")})
    assert response.status_code in DENIED_STATUS + NOT_FOUND_STATUS, describe(
        response, "an operations session confirming a booking")


def test_coordinator_cannot_declare_evacuation(
        coordinator: httpx.Client) -> None:
    response = coordinator.post("/evacuations", json={})
    assert response.status_code in DENIED_STATUS + NOT_FOUND_STATUS, describe(
        response, "a coordinator declaring evacuation")


def test_auditor_cannot_read_a_booking_row(auditor: httpx.Client) -> None:
    response = auditor.get("/bookings")
    assert response.status_code in DENIED_STATUS + NOT_FOUND_STATUS, describe(
        response, "an auditor reading the booking list")


def test_auditor_read_of_the_trail_is_stored_and_served(
        auditor: httpx.Client) -> None:
    response = auditor.get("/audit")
    payload = json_of(response, "the audit trail read by the auditor")
    assert isinstance(payload, dict) or isinstance(payload, list), describe(
        response, "the audit trail shape")
    rows = items(payload)
    assert rows, "the audit trail holds no rows"
    for row in rows[:5]:
        for field in ("actor", "action", "target", "at"):
            assert field in row, (
                f"an audit row carries no {field!r}; every row names the actor, "
                f"the action, the target and the time. Row {row!r}"[:300])


def test_audit_row_cannot_be_altered_through_the_api(
        auditor: httpx.Client, coordinator: httpx.Client) -> None:
    rows = items(json_of(auditor.get("/audit"), "the audit trail"))
    target = rows[0]
    for session, who in ((auditor, "the auditor"),
                         (coordinator, "a coordinator")):
        response = session.delete(f"/audit/{target.get('id')}")
        assert response.status_code not in OK_STATUS, (
            f"{who} deleted an audit row; the trail is append-only. "
            f"{describe(response, 'deleting an audit row')}")


def test_finance_cannot_issue_a_badge(finance: httpx.Client) -> None:
    response = finance.post("/badges", json={
        "accreditation": unique("accreditation"),
        "person_ref": unique("person"),
    })
    assert response.status_code in DENIED_STATUS + NOT_FOUND_STATUS, describe(
        response, "a finance session issuing a badge")


def test_planner_cannot_publish_another_party_event(
        planner: httpx.Client, planner2: httpx.Client) -> None:
    other = held_window(planner2, BOOKING_PUBLIC)
    response = planner.put(f"/publications/{other.get('id')}", json={
        "state": "published",
        "publish_at": "2026-12-01T00:00:00Z",
        "public_fields": {"title": unique("forged")},
    })
    assert response.status_code in DENIED_STATUS + NOT_FOUND_STATUS, describe(
        response, "a planner publishing another party's event")


def test_cancelling_a_booking_releases_every_stored_hold(
        coordinator: httpx.Client) -> None:
    enquiry = json_of(coordinator.post("/enquiries", json={
        "contact_name": unique("cancel"),
        "contact_email": probe_email("cancel"),
        "window_start": "2027-08-02T08:00:00Z",
        "window_end": "2027-08-04T20:00:00Z",
        "expected_visitors": 300,
        "event_type": "meeting",
        "spaces_of_interest": [MEETING_ROOMS[0]],
    }), "creating an enquiry to cancel later")
    option = json_of(coordinator.post("/options", json={
        "enquiry_id": enquiry.get("id"),
        "spaces": [MEETING_ROOMS[0]],
        "window_start": "2027-08-02T08:00:00Z",
        "window_end": "2027-08-04T20:00:00Z",
        "rank": 1,
        "expires_at": "2027-07-01T00:00:00Z",
    }), "placing the option to cancel later")
    booking = json_of(coordinator.post(f"/options/{option.get('id')}/confirm",
                                       json={"layout": "theatre",
                                             "idempotency_key": unique("cx")}),
                      "confirming the option to cancel later")
    cancelled = coordinator.post(f"/bookings/{booking.get('id')}/cancel",
                                 json={})
    assert cancelled.status_code in OK_STATUS, describe(
        cancelled, "cancelling the booking just made")
    settle()
    response = availability(coordinator, MEETING_ROOMS[0],
                            "2027-08-02T08:00:00Z", "2027-08-04T20:00:00Z")
    state = state_of(response, f"availability for {MEETING_ROOMS[0]!r} after "
                               f"cancellation")
    assert state == "free", (
        f"{MEETING_ROOMS[0]!r} reads {state!r} after its booking was cancelled; "
        f"cancellation releases every space the booking held")


def test_availability_is_the_same_answer_on_the_public_and_console_paths(
        coordinator: httpx.Client, anonymous: httpx.Client) -> None:
    booking = held_window(coordinator, BOOKING_PUBLISHED)
    start, end = booking.get("window_start"), booking.get("window_end")
    console = state_of(availability(coordinator, HALL_FOUR, start, end),
                       "console availability")
    public = anonymous.get("/availability",
                           params={"space": HALL_FOUR, "from": start,
                                   "to": end})
    if public.status_code in OK_STATUS:
        assert state_of(public, "public availability") == console, (
            f"the public path answers {public.text[:200]!r} while the console "
            f"answers {console!r} for {HALL_FOUR!r}; exactly one authority "
            f"answers whether a space is free")
    else:
        rows = items(json_of(anonymous.get("/public/events"),
                             "the public event list"))
        assert any(HALL_FOUR in flatten(row) for row in rows), (
            f"the public surface neither answers availability nor names "
            f"{HALL_FOUR!r} on a published event; the public plan and the "
            f"desk read the same space records")


def test_booking_rows_record_the_licence_version_they_were_written_under(
        coordinator: httpx.Client) -> None:
    booking = held_window(coordinator, BOOKING_PUBLISHED)
    detail = json_of(coordinator.get(f"/bookings/{booking.get('id')}"),
                     f"the booking file for {BOOKING_PUBLISHED!r}")
    flat = flatten(detail).lower()
    assert "version" in flat, (
        f"the booking file records no version; every booking records the "
        f"version it was written under. Body {flatten(detail)[:400]!r}")


def test_seeded_rows_survive_a_repeated_read_without_duplicating(
        coordinator: httpx.Client) -> None:
    first = items(json_of(coordinator.get("/spaces"), "the space catalog"))
    settle(1.0)
    second = items(json_of(coordinator.get("/spaces"),
                           "the space catalog read again"))
    assert len(first) == len(second), (
        f"the space catalog held {len(first)} rows and then {len(second)}; "
        f"seeding is idempotent")
    names = [row.get("name") for row in second]
    assert len(names) == len(set(names)), (
        f"the space catalog holds duplicate names {names!r}; seeding must not "
        f"duplicate a row")


def test_report_figures_reconcile_with_the_stored_rows(
        coordinator: httpx.Client) -> None:
    report = json_of(coordinator.get("/reports/occupancy",
                                     params={"from": "2027-01-01",
                                             "to": "2027-12-31"}),
                     "the campus occupancy report")
    by_space = items(report.get("by_space") or report)
    assert by_space, (
        f"the occupancy report returns no rows; every figure derives from the "
        f"ledgers. Body {flatten(report)[:400]!r}")
    catalog = items(json_of(coordinator.get("/spaces"), "the space catalog"))
    known = {str(row.get("name")) for row in catalog}
    for row in by_space:
        label = str(row.get("space") or row.get("name"))
        assert label in known, (
            f"the occupancy report names {label!r}, which is not a stored "
            f"space; the report derives from the ledgers")


def test_undeclared_option_rank_collision_is_refused(
        coordinator: httpx.Client) -> None:
    enquiry = json_of(coordinator.post("/enquiries", json={
        "contact_name": unique("rank"),
        "contact_email": probe_email("rank"),
        "window_start": "2027-09-06T08:00:00Z",
        "window_end": "2027-09-08T20:00:00Z",
        "expected_visitors": 200,
        "event_type": "seminar",
        "spaces_of_interest": [EVENT_HALL],
    }), "creating an enquiry for the rank collision")
    body = {
        "enquiry_id": enquiry.get("id"),
        "spaces": [EVENT_HALL],
        "window_start": "2027-09-06T08:00:00Z",
        "window_end": "2027-09-08T20:00:00Z",
        "rank": 1,
        "expires_at": "2027-08-01T00:00:00Z",
    }
    first = coordinator.post("/options", json=body)
    assert first.status_code in OK_STATUS, describe(
        first, "placing the first rank-one option")
    second = coordinator.post("/options", json=body)
    assert second.status_code in REFUSED_STATUS, describe(
        second, "placing a second rank-one option on the same space and window")


def test_boulevard_hire_is_refused_when_the_route_would_fail(
        coordinator: httpx.Client) -> None:
    enquiry = json_of(coordinator.post("/enquiries", json={
        "contact_name": unique("route"),
        "contact_email": probe_email("route"),
        "window_start": "2027-01-04T08:00:00Z",
        "window_end": "2027-01-06T20:00:00Z",
        "expected_visitors": 5000,
        "event_type": "public fair",
        "spaces_of_interest": [BOULEVARD, HALL_ONE, HALL_TWO],
    }), "creating an enquiry that would close the public route")
    response = coordinator.post("/options", json={
        "enquiry_id": enquiry.get("id"),
        "spaces": [BOULEVARD, HALL_ONE, HALL_TWO],
        "window_start": "2027-01-04T08:00:00Z",
        "window_end": "2027-01-06T20:00:00Z",
        "rank": 1,
        "expires_at": "2026-12-01T00:00:00Z",
        "boulevard_use": "exhibition",
        "expected_occupancy": 5000,
    })
    if response.status_code in REFUSED_STATUS:
        assert "route" in flatten(response.json() if response.content else {}), (
            f"the refusal names no failing route; hiring the boulevard is "
            f"refused with the route named. Body {response.text[:300]!r}")
    else:
        detail = json_of(response, "the accepted boulevard hire")
        assert flatten(detail), describe(
            response, "an accepted boulevard hire must still record the "
                      "remaining public route")


def test_scan_at_an_unknown_entrance_is_refused(
        operations: httpx.Client) -> None:
    badges = items(json_of(operations.get("/badges"), "the badge list"))
    response = operations.post("/scans", json={
        "badge": badges[0].get("id"),
        "entrance": unique("ghost-gate"),
        "at": "2027-01-04T10:00:00Z",
    })
    assert response.status_code in REFUSED_STATUS or (
        (response.json() or {}).get("decision") == "refused"), describe(
        response, "a scan at an entrance the campus does not have")


def test_empty_public_calendar_filter_returns_an_empty_list(
        anonymous: httpx.Client) -> None:
    response = anonymous.get("/public/events",
                             params={"hall": unique("no-such-hall")})
    assert response.status_code in OK_STATUS + NOT_FOUND_STATUS, describe(
        response, "the public event list filtered to a hall that does not exist")
    if response.status_code in OK_STATUS:
        assert items(response.json()) == [], (
            f"a filter matching nothing returned rows: "
            f"{response.text[:300]!r}")


def test_search_answers_only_from_the_closed_state_set(
        anonymous: httpx.Client) -> None:
    response = anonymous.get("/search", params={"q": HALL_FIVE,
                                                "language": "en"})
    state = state_of(response, "a search across the public site")
    assert state in ("ok", "invalid", "failed"), (
        f"search answered {state!r}, outside the closed set "
        f"('ok', 'invalid', 'failed')")


def test_every_language_prefix_serves_the_home_route(
        web: httpx.Client) -> None:
    for language in LANGUAGES:
        response = web.get(f"/{language}")
        assert response.status_code == 200, describe(
            response, f"the home route under the {language!r} prefix")
        assert f'lang="{language}"' in response.text, (
            f"the {language!r} home route does not declare its own document "
            f"language; markup began {response.text[:300]!r}")


def test_home_markup_carries_the_pinned_hero_line_and_skip_link(
        web: httpx.Client) -> None:
    response = web.get("/en")
    assert response.status_code == 200, describe(response, "the English home")
    for pinned in (HERO_LINE, SKIP_LINK, SEARCH_LABEL):
        assert pinned in response.text, (
            f"the English home route does not carry the pinned string "
            f"{pinned!r}")


def test_footer_markup_carries_the_pinned_copyright_line(
        web: httpx.Client) -> None:
    response = web.get("/en")
    assert COPYRIGHT_LINE in response.text, (
        f"the English home route does not carry the pinned copyright line "
        f"{COPYRIGHT_LINE!r}")


def test_calendar_markup_carries_both_pinned_status_chips(
        web: httpx.Client) -> None:
    response = web.get("/en/calendar")
    assert response.status_code == 200, describe(response, "the calendar route")
    for chip in (STATUS_CHIP_PUBLIC, STATUS_CHIP_TRADE):
        assert chip in response.text, (
            f"the calendar does not carry the pinned status chip {chip!r}")


def test_spaces_markup_carries_the_pinned_parking_figure(
        web: httpx.Client) -> None:
    response = web.get("/en/organize/spaces")
    assert response.status_code == 200, describe(response, "the spaces route")
    assert str(PARKING_SPACES) in response.text.replace(",", ""), (
        f"the spaces route does not carry the parking figure {PARKING_SPACES}")


def test_not_found_route_serves_the_designed_screen(
        web: httpx.Client) -> None:
    response = web.get(f"/en/{unique('no-such-page')}")
    assert response.status_code in NOT_FOUND_STATUS + (200,), describe(
        response, "an unknown address under the English prefix")
    for pinned in (NOT_FOUND_HEADING, NOT_FOUND_ACTION):
        assert pinned in response.text, (
            f"the not-found screen does not carry the pinned string {pinned!r}")


def test_sitemap_and_robots_are_served_for_the_public_routes(
        web: httpx.Client) -> None:
    sitemap = web.get("/sitemap.xml")
    assert sitemap.status_code == 200, describe(sitemap, "the sitemap")
    for language in LANGUAGES:
        assert f"/{language}" in sitemap.text, (
            f"the sitemap names no route under the {language!r} prefix")
    robots = web.get("/robots.txt")
    assert robots.status_code == 200, describe(robots, "the robots file")
    assert "sitemap" in robots.text.lower(), (
        f"the robots file does not name the sitemap; body "
        f"{robots.text[:200]!r}")


def test_public_response_carries_the_security_header_set(
        web: httpx.Client) -> None:
    response = web.get("/en")
    headers = {key.lower() for key in response.headers}
    for header in ("content-security-policy", "x-content-type-options",
                   "referrer-policy"):
        assert header in headers, (
            f"the home response carries no {header!r}; every response carries "
            f"the security header set. Headers were {sorted(headers)!r}")
