from __future__ import annotations

import pathlib
import threading
from concurrent.futures import ThreadPoolExecutor

import httpx

import appclient
from conftest import (
    ALTERNATIVE_SAVING_MINUTES, BUFFER_MINUTES, DRIVER_A, DRIVER_B, DRIVER_C,
    FRESHNESS_CAP_MINUTES, FRESHNESS_MINUTES, PASSWORD, PLACE_DESTINATION,
    PLACE_HAUZ, PLACE_ORIGIN, PUBLIC_ROUTES, REMINDER_LEAD_MINUTES,
    SEEDED_CONDITIONS, SEEDED_PLACES, SEEDED_SEGMENTS, SEGMENT_DND,
    SEGMENT_OUTER_RING, SEGMENT_RING_NORTH, describe, expected_travel_minutes,
    file_report, future_arrival, iso, parse_iso, past_arrival, place_id,
    poll_until, probe_email, save_drive, segments_by_name, settle, solve_route,
)


def test_signup_returns_access_token(anon):
    email = probe_email()
    response = anon.post("/auth/signup", json={
        "email": email, "password": PASSWORD, "display_name": "New Driver"})
    assert response.status_code in (200, 201), (
        f"signup with the unregistered email {email} did not succeed: {describe(response)}")
    token = response.json().get("access_token")
    assert token, (
        f"signup for {email} returned no access_token; body was {response.text[:400]}")


def test_signup_with_existing_email_is_refused(anon, backend):
    before = backend.count("drivers", email=DRIVER_A)
    response = anon.post("/auth/signup", json={
        "email": DRIVER_A, "password": PASSWORD, "display_name": "Impostor"})
    assert 400 <= response.status_code < 500, (
        f"signup with the already registered {DRIVER_A} was not refused as a client "
        f"error: {describe(response)}")
    assert DRIVER_A in response.text, (
        f"the refusal does not name {DRIVER_A} as the reason: {response.text[:400]}")
    assert backend.count("drivers", email=DRIVER_A) == before, (
        f"a second drivers row exists for {DRIVER_A} after a refused signup")


def test_place_search_ranks_seeded_places(anon, driver_a):
    response = anon.get("/places", params={"q": "connaught"})
    assert response.status_code == 200, (
        f"a lower-case place search did not answer 200: {describe(response)}")
    rows = response.json()
    assert isinstance(rows, list), (
        f"GET /api/places must return a top-level JSON array, got "
        f"{type(rows).__name__}: {response.text[:400]}")
    names = [row.get("name") for row in rows]
    assert PLACE_ORIGIN in names, (
        f"a case insensitive substring search for 'connaught' did not match "
        f"{PLACE_ORIGIN!r}; it returned {names}")

    everything = anon.get("/places", params={"q": ""})
    assert everything.status_code == 200, (
        f"an empty place query did not answer 200: {describe(everything)}")
    seeded = [row.get("name") for row in everything.json()]
    for name in SEEDED_PLACES:
        assert name in seeded, (
            f"the seeded place {name!r} is missing from the place index; "
            f"the index holds {seeded}")
    assert seeded == sorted(seeded), (
        f"the place index is not ordered by name ascending: {seeded}")

    row = rows[0]
    reverse = anon.get("/places/reverse", params={
        "latitude": row["latitude"], "longitude": row["longitude"]})
    assert reverse.status_code == 200, (
        f"a reverse lookup on the coordinate of {row.get('name')!r} did not answer "
        f"200: {describe(reverse)}")
    assert reverse.json().get("name") == row.get("name"), (
        f"a reverse lookup on {row.get('name')!r}'s own coordinate returned "
        f"{reverse.json().get('name')!r}")

    signed_in = driver_a.get("/places", params={"q": ""})
    assert signed_in.status_code == 200, (
        f"a signed in driver could not read the place index: {describe(signed_in)}")
    assert [row.get("name") for row in signed_in.json()] == seeded, (
        f"{DRIVER_A} sees a different place index from an anonymous visitor; every "
        f"driver reads the same places")


def test_route_returns_ordered_segments_with_travel_time(anon):
    origin = place_id(anon, PLACE_ORIGIN)
    destination = place_id(anon, PLACE_DESTINATION)
    response = solve_route(anon, origin, destination, future_arrival())
    assert response.status_code == 200, (
        f"a route between two resolved endpoints did not answer 200: {describe(response)}")
    body = response.json()
    legs = body.get("segments")
    assert isinstance(legs, list) and legs, (
        f"the route carries no ordered segments: {response.text[:400]}")
    for leg in legs:
        assert leg.get("severity") in SEEDED_CONDITIONS.values(), (
            f"segment {leg.get('name')!r} carries the road condition "
            f"{leg.get('severity')!r}, which is not clear, slowing or heavy")
        assert int(leg["base_minutes"]) == SEEDED_SEGMENTS[leg["name"]], (
            f"segment {leg['name']!r} reports a free flow time of "
            f"{leg['base_minutes']} rather than {SEEDED_SEGMENTS[leg['name']]}")
    assert int(body["travel_minutes"]) == expected_travel_minutes(legs), (
        f"travel_minutes is {body['travel_minutes']} but scaling each segment "
        f"({[(leg['name'], leg['severity'], leg['base_minutes']) for leg in legs]}) "
        f"and rounding each up gives {expected_travel_minutes(legs)}")

    missing = solve_route(anon, origin, 10 ** 9, future_arrival())
    assert 400 <= missing.status_code < 500, (
        f"a route naming a destination that does not resolve was not refused as a "
        f"client error: {describe(missing)}")


def test_arrival_time_solves_to_leave_time_and_reminder(anon):
    origin = place_id(anon, PLACE_ORIGIN)
    destination = place_id(anon, PLACE_DESTINATION)
    arrival = future_arrival()
    response = solve_route(anon, origin, destination, arrival)
    assert response.status_code == 200, (
        f"the scheduler refused a visitor with no bearer token: {describe(response)}")
    body = response.json()
    travel = int(body["travel_minutes"])
    gap = (parse_iso(body["arrival_at"]) - parse_iso(body["leave_at"])).total_seconds() / 60
    assert gap == travel + BUFFER_MINUTES, (
        f"leave_at is {body['leave_at']} for an arrival_at of {body['arrival_at']}, "
        f"a gap of {gap} minutes; the travel time is {travel} so the gap must be "
        f"{travel + BUFFER_MINUTES} minutes")

    origin_b = place_id(anon, PLACE_HAUZ)
    second = solve_route(anon, origin_b, destination, arrival)
    assert second.status_code == 200, (
        f"a second route from {PLACE_HAUZ!r} did not answer 200: {describe(second)}")
    assert parse_iso(second.json()["arrival_at"]) == parse_iso(arrival), (
        f"the solved route moved the requested arrival time from {arrival} to "
        f"{second.json()['arrival_at']}")


def test_report_recolours_its_segment_at_once(driver_a, anon):
    seeded = segments_by_name(anon)
    for name, condition in SEEDED_CONDITIONS.items():
        assert seeded[name]["severity"] == condition, (
            f"the seeded road condition of {name!r} reads "
            f"{seeded[name]['severity']!r} rather than {condition!r}")

    target = seeded[SEGMENT_DND]
    created = file_report(driver_a, target, "jam")
    assert created.status_code in (200, 201), (
        f"a signed in driver could not file a jam report on {SEGMENT_DND!r}: "
        f"{describe(created)}")
    after = segments_by_name(anon)[SEGMENT_DND]
    assert after["severity"] == "slowing", (
        f"{SEGMENT_DND!r} carried no active report and now carries exactly one jam, "
        f"so it must read slowing; it reads {after['severity']!r}")

    second = file_report(driver_a, target, "jam")
    assert second.status_code in (200, 201), (
        f"a second jam report on {SEGMENT_DND!r} was refused: {describe(second)}")
    heavy = segments_by_name(anon)[SEGMENT_DND]
    assert heavy["severity"] == "heavy", (
        f"{SEGMENT_DND!r} now carries two active jam reports, so it must read heavy; "
        f"it reads {heavy['severity']!r}")


def test_confirm_vote_extends_report_freshness(driver_a, driver_b, anon):
    target = segments_by_name(anon)[SEGMENT_OUTER_RING]
    created = file_report(driver_a, target, "hazard")
    assert created.status_code in (200, 201), (
        f"filing a hazard report on {SEGMENT_OUTER_RING!r} failed: {describe(created)}")
    report = created.json()
    before = parse_iso(report["expires_at"])
    filed = parse_iso(report["created_at"])
    minutes = (before - filed).total_seconds() / 60
    assert minutes == FRESHNESS_MINUTES, (
        f"a new report expires {minutes} minutes after it was filed; the brief pins "
        f"{FRESHNESS_MINUTES} minutes")

    voted = driver_b.post(f"/reports/{report['id']}/votes", json={"vote": "confirm"})
    assert voted.status_code in (200, 201), (
        f"a confirming vote from {DRIVER_B} was refused: {describe(voted)}")
    extended = parse_iso(voted.json()["expires_at"])
    assert extended > before, (
        f"a confirming vote left expires_at at {iso(extended)}; it must move past "
        f"{iso(before)}")
    ceiling = (extended - filed).total_seconds() / 60
    assert ceiling <= FRESHNESS_CAP_MINUTES, (
        f"a confirming vote pushed freshness to {ceiling} minutes after filing; the "
        f"ceiling is {FRESHNESS_CAP_MINUTES} minutes")


def test_dispute_from_reputable_driver_dismisses_report(driver_a, driver_c, anon):
    target = segments_by_name(anon)[SEGMENT_OUTER_RING]
    created = file_report(driver_c, target, "crash")
    assert created.status_code in (200, 201), (
        f"filing a crash report failed: {describe(created)}")
    report = created.json()

    voted = driver_a.post(f"/reports/{report['id']}/votes", json={"vote": "dispute"})
    assert voted.status_code in (200, 201), (
        f"a disputing vote from the reputable {DRIVER_A} was refused: {describe(voted)}")
    assert voted.json().get("status") == "dismissed", (
        f"{DRIVER_A} has a reputation of 3, so one dispute reaches strength 2 and the "
        f"report must read dismissed; it reads {voted.json().get('status')!r}")

    listed = anon.get("/reports", params={"segment_id": target["id"]})
    assert listed.status_code == 200, (
        f"listing reports for {SEGMENT_OUTER_RING!r} failed: {describe(listed)}")
    still_active = [row for row in listed.json()
                    if row["id"] == report["id"] and row.get("status") == "active"]
    assert not still_active, (
        f"the dismissed report {report['id']} is still listed active on "
        f"{SEGMENT_OUTER_RING!r}")


def test_route_recalculates_after_a_report_changes_the_road(driver_a, anon):
    origin = place_id(anon, PLACE_ORIGIN)
    destination = place_id(anon, PLACE_DESTINATION)
    arrival = future_arrival()
    before = solve_route(anon, origin, destination, arrival)
    assert before.status_code == 200, (
        f"the first route calculation failed: {describe(before)}")
    first = before.json()
    leg = first["segments"][0]

    created = file_report(driver_a, leg, "closure")
    assert created.status_code in (200, 201), (
        f"filing a closure report on {leg.get('name')!r} failed: {describe(created)}")

    after = solve_route(anon, origin, destination, arrival)
    assert after.status_code == 200, (
        f"the route calculation after the road changed failed: {describe(after)}")
    second = after.json()
    assert int(second["travel_minutes"]) == expected_travel_minutes(second["segments"]), (
        f"after a closure landed on {leg.get('name')!r} the travel time is "
        f"{second['travel_minutes']} but scaling the returned segments gives "
        f"{expected_travel_minutes(second['segments'])}")
    saving = int(first["travel_minutes"]) - int(second["travel_minutes"])
    if second["segments"] != first["segments"]:
        assert saving >= ALTERNATIVE_SAVING_MINUTES, (
            f"the drawn path changed while saving only {saving} minutes; an "
            f"alternative is offered only when it saves at least "
            f"{ALTERNATIVE_SAVING_MINUTES} minutes")


def test_not_found_address_answers_not_found(anon):
    url = f"{appclient.app_url()}/no-such-road-{probe_email().split('@')[0]}"
    response = httpx.get(url, timeout=appclient.TIMEOUT)
    assert response.status_code == 404, (
        f"an unknown address answered {response.status_code} rather than not found: "
        f"GET {url} -> {response.text[:400]}")
    assert "Page not found" in response.text, (
        f"the not found page does not carry the heading 'Page not found': "
        f"{response.text[:400]}")


def test_privacy_and_terms_reachable_from_every_footer(anon):
    for route in ("/", "/ul", "/412"):
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=appclient.TIMEOUT)
        assert page.status_code == 200, (
            f"the public route {route} did not answer 200: GET {route} -> "
            f"{page.status_code}: {page.text[:200]}")
        assert "/privacy" in page.text, (
            f"the footer of {route} carries no link to /privacy: {page.text[:400]}")
        assert "/terms" in page.text, (
            f"the footer of {route} carries no link to /terms: {page.text[:400]}")


def test_seeded_rows_persisted_and_idempotent_after_restart(backend, anon):
    for email in (DRIVER_A, DRIVER_B, DRIVER_C):
        assert backend.count("drivers", email=email) == 1, (
            f"the seeded account {email} appears "
            f"{backend.count('drivers', email=email)} times in drivers; seeding must "
            f"leave exactly one row per account")
        token = appclient.login(email, PASSWORD)
        assert token, f"the seeded password does not sign {email} in"

    for name in SEEDED_PLACES:
        assert backend.count("places", name=name) == 1, (
            f"the seeded place {name!r} appears "
            f"{backend.count('places', name=name)} times in places")
    for name in SEEDED_SEGMENTS:
        assert backend.count("segments", name=name) == 1, (
            f"the seeded segment {name!r} appears "
            f"{backend.count('segments', name=name)} times in segments")

    scheduled = backend.rows("planned_drives", status="scheduled")
    assert scheduled, "the seeded planned drive is missing from planned_drives"


def test_segment_condition_reconciles_with_stored_reports(backend, driver_a, anon):
    served = segments_by_name(anon)
    for name, base in SEEDED_SEGMENTS.items():
        row = backend.one("segments", name=name)
        assert row is not None, f"the segment {name!r} has no row in segments"
        assert int(row["base_minutes"]) == base, (
            f"the stored free flow time of {name!r} is {row['base_minutes']} rather "
            f"than {base}")
        assert "severity" not in row, (
            f"the segments row for {name!r} stores a severity column; the road "
            f"condition is computed on read")
        path = str(row["path"]).split()
        assert len(path) >= 2 and all("," in pair for pair in path), (
            f"the stored path of {name!r} is not latitude,longitude pairs separated "
            f"by spaces: {row['path']!r}")
        assert served[name]["severity"] == SEEDED_CONDITIONS[name], (
            f"the served road condition of {name!r} is "
            f"{served[name]['severity']!r} rather than {SEEDED_CONDITIONS[name]!r}")

    listed = anon.get("/reports")
    assert listed.status_code == 200, (
        f"the report list refused an unauthenticated caller: {describe(listed)}")
    for row in listed.json():
        assert row.get("status") == "active", (
            f"report {row.get('id')} reads {row.get('status')!r} and is still served "
            f"on the live layer; only active reports colour a road")


def test_travel_time_reconciles_with_segment_free_flow_times(backend, anon):
    origin = place_id(anon, PLACE_ORIGIN)
    destination = place_id(anon, PLACE_DESTINATION)
    response = solve_route(anon, origin, destination, future_arrival())
    assert response.status_code == 200, (
        f"the route calculation failed: {describe(response)}")
    legs = response.json()["segments"]
    for leg in legs:
        row = backend.one("segments", name=leg["name"])
        assert row is not None, (
            f"the route names the segment {leg['name']!r}, which has no row in the "
            f"database reached at DATABASE_URL")
        assert int(leg["base_minutes"]) == int(row["base_minutes"]), (
            f"the route reports {leg['base_minutes']} free flow minutes for "
            f"{leg['name']!r} while the stored row says {row['base_minutes']}")
    assert int(response.json()["travel_minutes"]) == expected_travel_minutes(legs), (
        f"the served travel time disagrees with the stored free flow times scaled by "
        f"road condition")


def test_planned_drive_is_persisted_with_solved_window(backend, driver_b, anon):
    origin = place_id(anon, PLACE_HAUZ)
    destination = place_id(anon, PLACE_DESTINATION)
    arrival = future_arrival(600)
    response = save_drive(driver_b, origin, destination, arrival)
    assert response.status_code in (200, 201), (
        f"{DRIVER_B} could not save a planned drive: {describe(response)}")
    drive = response.json()
    assert drive.get("status") == "scheduled", (
        f"a saved planned drive starts in {drive.get('status')!r} rather than "
        f"'scheduled'")

    row = backend.one("planned_drives", id=drive["id"])
    assert row is not None, (
        f"the planned drive {drive['id']} was returned by the API but has no row in "
        f"planned_drives")
    assert int(row["travel_minutes"]) == int(drive["travel_minutes"]), (
        f"the stored travel_minutes {row['travel_minutes']} disagrees with the served "
        f"{drive['travel_minutes']}")
    gap = (parse_iso(drive["arrival_at"]) - parse_iso(drive["leave_at"])).total_seconds() / 60
    assert gap == int(drive["travel_minutes"]) + BUFFER_MINUTES, (
        f"the stored departure window spans {gap} minutes; the travel time is "
        f"{drive['travel_minutes']} so it must span "
        f"{int(drive['travel_minutes']) + BUFFER_MINUTES}")
    lead = (parse_iso(drive["leave_at"]) - parse_iso(drive["reminder_at"])).total_seconds() / 60
    assert lead == REMINDER_LEAD_MINUTES, (
        f"the reminder falls due {lead} minutes before the leave time; the brief pins "
        f"{REMINDER_LEAD_MINUTES}")


def test_planned_drive_row_matches_the_confirmation_page(backend, driver_b, anon):
    origin = place_id(anon, PLACE_ORIGIN)
    destination = place_id(anon, PLACE_HAUZ)
    created = save_drive(driver_b, origin, destination, future_arrival(900))
    assert created.status_code in (200, 201), (
        f"saving a planned drive failed: {describe(created)}")
    drive = created.json()

    cancelled = driver_b.delete(f"/drives/{drive['id']}")
    assert cancelled.status_code in (200, 202, 204), (
        f"{DRIVER_B} could not cancel their own planned drive: {describe(cancelled)}")
    row = backend.one("planned_drives", id=drive["id"])
    assert row is not None and row["status"] == "canceled", (
        f"the cancelled drive {drive['id']} reads "
        f"{(row or {}).get('status')!r} rather than 'canceled'")

    again = save_drive(driver_b, origin, destination, drive["arrival_at"])
    assert again.status_code in (200, 201), (
        f"a cancelled drive still holds its departure window: a fresh request for the "
        f"same window was refused with {describe(again)}")


def test_page_view_row_stored_for_each_public_route(backend, fresh_driver):
    email, session = fresh_driver
    before = len(session.get("/page-views").json())
    recorded = session.post("/page-views", json={"route": "/privacy"})
    assert recorded.status_code in (200, 201), (
        f"recording a page view for /privacy failed: {describe(recorded)}")
    mine = session.get("/page-views")
    assert mine.status_code == 200, (
        f"a driver could not read their own page views: {describe(mine)}")
    rows = mine.json()
    assert isinstance(rows, list) and len(rows) == before + 1, (
        f"recording one page view changed the caller's own record count from {before} "
        f"to {len(rows)}")
    assert any(row.get("route") == "/privacy" for row in rows), (
        f"the recorded view does not carry the route /privacy: {rows}")

    anonymous = httpx.get(f"{appclient.app_url()}/privacy", timeout=appclient.TIMEOUT)
    assert anonymous.status_code == 200, (
        f"/privacy did not answer 200 to an anonymous visitor: "
        f"{anonymous.status_code}")
    orphaned = backend.count("page_views", driver_id=None)
    assert orphaned >= 1, (
        "a view taken without an account records no row against a null driver_id; "
        f"page_views holds {orphaned} such rows")


def test_visitor_cannot_file_a_report_denied(anon, backend):
    before = backend.count("reports")
    segment = segments_by_name(anon)[SEGMENT_RING_NORTH]
    response = anon.post("/reports", json={
        "segment_id": segment["id"], "type": "police",
        "latitude": 28.459, "longitude": 77.025})
    assert response.status_code in (401, 403), (
        f"an unauthenticated caller filed a report: {describe(response)}")
    assert backend.count("reports") == before, (
        f"the reports table grew from {before} to {backend.count('reports')} after a "
        f"denied unauthenticated write")


def test_visitor_cannot_save_a_planned_drive_denied(anon, backend):
    before = backend.count("planned_drives")
    origin = place_id(anon, PLACE_ORIGIN)
    destination = place_id(anon, PLACE_DESTINATION)
    response = save_drive(anon, origin, destination, future_arrival())
    assert response.status_code in (401, 403), (
        f"an unauthenticated caller saved a planned drive: {describe(response)}")
    assert backend.count("planned_drives") == before, (
        f"planned_drives grew from {before} to {backend.count('planned_drives')} after "
        f"a denied unauthenticated write")


def test_driver_cannot_read_another_drivers_planned_drive_denied(driver_a, driver_b, anon, backend):
    origin = place_id(anon, PLACE_ORIGIN)
    destination = place_id(anon, PLACE_DESTINATION)
    created = save_drive(driver_b, origin, destination, future_arrival(1500))
    assert created.status_code in (200, 201), (
        f"{DRIVER_B} could not save the drive this check reads back: {describe(created)}")
    drive = created.json()
    before = backend.one("planned_drives", id=drive["id"])

    read = driver_a.get(f"/drives/{drive['id']}")
    assert read.status_code in (401, 403, 404), (
        f"{DRIVER_A} read {DRIVER_B}'s planned drive {drive['id']}: {describe(read)}")
    cancel = driver_a.delete(f"/drives/{drive['id']}")
    assert cancel.status_code in (401, 403, 404), (
        f"{DRIVER_A} cancelled {DRIVER_B}'s planned drive {drive['id']}: "
        f"{describe(cancel)}")
    after = backend.one("planned_drives", id=drive["id"])
    assert after == before, (
        f"the planned_drives row for {drive['id']} changed after a denied cross-driver "
        f"request: {before} became {after}")

    listed = driver_a.get("/drives")
    assert listed.status_code == 200, (
        f"{DRIVER_A} could not list their own drives: {describe(listed)}")
    assert all(row["id"] != drive["id"] for row in listed.json()), (
        f"{DRIVER_B}'s drive {drive['id']} appears in {DRIVER_A}'s own list")


def test_driver_cannot_read_another_drivers_page_views_denied(driver_a, fresh_driver):
    email, session = fresh_driver
    session.post("/page-views", json={"route": "/terms"})
    mine = driver_a.get("/page-views")
    assert mine.status_code == 200, (
        f"{DRIVER_A} could not read their own page views: {describe(mine)}")
    routes = [row.get("route") for row in mine.json()]
    theirs = session.get("/page-views").json()
    ids = {row.get("id") for row in theirs}
    assert not ids & {row.get("id") for row in mine.json()}, (
        f"{DRIVER_A}'s page view list carries rows belonging to {email}: {routes}")


def test_driver_cannot_vote_on_own_report_denied(driver_c, anon, backend):
    segment = segments_by_name(anon)[SEGMENT_RING_NORTH]
    created = file_report(driver_c, segment, "police")
    assert created.status_code in (200, 201), (
        f"{DRIVER_C} could not file the report this check votes on: {describe(created)}")
    report = created.json()
    before = backend.count("report_votes", report_id=report["id"])

    response = driver_c.post(f"/reports/{report['id']}/votes", json={"vote": "confirm"})
    assert 400 <= response.status_code < 500, (
        f"{DRIVER_C} voted on their own report {report['id']}: {describe(response)}")
    assert backend.count("report_votes", report_id=report["id"]) == before, (
        f"a vote row was written for a driver voting on their own report "
        f"{report['id']}")


def test_expired_token_denied_and_row_unchanged(driver_b, anon, backend):
    origin = place_id(anon, PLACE_ORIGIN)
    destination = place_id(anon, PLACE_DESTINATION)
    created = save_drive(driver_b, origin, destination, future_arrival(2100))
    assert created.status_code in (200, 201), (
        f"{DRIVER_B} could not save the drive this check reads back: {describe(created)}")
    drive = created.json()
    before = backend.one("planned_drives", id=drive["id"])

    with appclient.client("expired.bearer.credential") as stale:
        read = stale.get(f"/drives/{drive['id']}")
        assert read.status_code in (401, 403), (
            f"an unparseable bearer credential was served rather than denied: "
            f"{describe(read)}")
        cancel = stale.delete(f"/drives/{drive['id']}")
        assert cancel.status_code in (401, 403), (
            f"an unparseable bearer credential cancelled a planned drive: "
            f"{describe(cancel)}")
    assert backend.one("planned_drives", id=drive["id"]) == before, (
        f"the planned_drives row for {drive['id']} changed after a denied request "
        f"carrying an unusable credential")


def test_concurrent_overlapping_windows_admit_exactly_one(driver_b, anon, backend):
    origin = place_id(anon, PLACE_ORIGIN)
    destination = place_id(anon, PLACE_DESTINATION)
    arrival = future_arrival(3000)
    before = backend.count("planned_drives", driver_id=None)
    del before

    barrier = threading.Barrier(2)
    token = appclient.login(DRIVER_B, PASSWORD)

    def attempt() -> int:
        with appclient.client(token) as session:
            barrier.wait(timeout=30)
            return save_drive(session, origin, destination, arrival).status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        statuses = sorted(future.result() for future in
                          [pool.submit(attempt), pool.submit(attempt)])

    accepted = [code for code in statuses if code in (200, 201)]
    refused = [code for code in statuses if 400 <= code < 500]
    assert len(accepted) == 1 and len(refused) == 1, (
        f"two simultaneous requests for the same departure window returned "
        f"{statuses}; exactly one must be accepted and one refused as a client error")

    rows = [row for row in backend.rows("planned_drives")
            if row.get("status") == "scheduled"
            and parse_iso(iso(row["arrival_at"])) == parse_iso(arrival)]
    assert len(rows) == 1, (
        f"{len(rows)} planned_drives rows exist for the contested arrival time "
        f"{arrival}; exactly one request won, so exactly one row may survive")


def test_touching_windows_are_both_accepted(driver_c, anon):
    origin = place_id(anon, PLACE_ORIGIN)
    destination = place_id(anon, PLACE_DESTINATION)
    first = save_drive(driver_c, origin, destination, future_arrival(4000))
    assert first.status_code in (200, 201), (
        f"the first planned drive was refused: {describe(first)}")
    earlier = first.json()

    adjacent = iso(parse_iso(earlier["leave_at"]))
    second = save_drive(driver_c, origin, destination, adjacent)
    assert second.status_code in (200, 201), (
        f"a drive arriving exactly when the held window opens, at {adjacent}, was "
        f"refused; windows that touch end to start do not overlap: {describe(second)}")


def test_past_arrival_time_is_refused(driver_b, anon, backend):
    before = backend.count("planned_drives")
    origin = place_id(anon, PLACE_ORIGIN)
    destination = place_id(anon, PLACE_DESTINATION)
    stale = past_arrival()
    response = save_drive(driver_b, origin, destination, stale)
    assert 400 <= response.status_code < 500, (
        f"an arrival time already in the past, {stale}, was not refused as a client "
        f"error: {describe(response)}")
    assert backend.count("planned_drives") == before, (
        f"planned_drives grew from {before} to {backend.count('planned_drives')} after "
        f"a refused past arrival time")


def test_unknown_report_type_is_refused(driver_a, anon, backend):
    before = backend.count("reports")
    segment = segments_by_name(anon)[SEGMENT_RING_NORTH]
    bogus = file_report(driver_a, segment, "roadworks")
    assert 400 <= bogus.status_code < 500, (
        f"the report type 'roadworks' is outside the nine named types and was not "
        f"refused: {describe(bogus)}")
    missing = driver_a.post("/reports", json={
        "segment_id": 10 ** 9, "type": "jam",
        "latitude": 28.459, "longitude": 77.025})
    assert 400 <= missing.status_code < 500, (
        f"a report naming a segment that does not exist was not refused: "
        f"{describe(missing)}")
    assert backend.count("reports") == before, (
        f"the reports table grew from {before} to {backend.count('reports')} after two "
        f"refused writes")


def test_second_vote_from_one_driver_is_refused(driver_a, driver_b, anon, backend):
    segment = segments_by_name(anon)[SEGMENT_RING_NORTH]
    created = file_report(driver_a, segment, "hazard")
    assert created.status_code in (200, 201), (
        f"filing the report this check votes on failed: {describe(created)}")
    report = created.json()

    first = driver_b.post(f"/reports/{report['id']}/votes", json={"vote": "confirm"})
    assert first.status_code in (200, 201), (
        f"the first vote from {DRIVER_B} was refused: {describe(first)}")
    votes = backend.count("report_votes", report_id=report["id"])

    second = driver_b.post(f"/reports/{report['id']}/votes", json={"vote": "dispute"})
    assert 400 <= second.status_code < 500, (
        f"{DRIVER_B} voted twice on report {report['id']}: {describe(second)}")
    assert backend.count("report_votes", report_id=report["id"]) == votes, (
        f"a second vote row was written for {DRIVER_B} on report {report['id']}")


def test_empty_place_search_returns_empty_array(anon):
    response = anon.get("/places", params={"q": "zzzz-no-such-place"})
    assert response.status_code == 200, (
        f"a place search matching nothing answered {response.status_code} rather than "
        f"200: {describe(response)}")
    rows = response.json()
    assert isinstance(rows, list) and rows == [], (
        f"a place search matching nothing returned {rows!r}; it must be an empty "
        f"top-level array")


def test_drives_list_empty_for_a_fresh_driver(fresh_driver):
    email, session = fresh_driver
    drives = session.get("/drives")
    assert drives.status_code == 200, (
        f"a driver with nothing scheduled could not list their drives: "
        f"{describe(drives)}")
    assert drives.json() == [], (
        f"a freshly created driver {email} already holds planned drives: "
        f"{drives.json()}")
    reminders = session.get("/reminders")
    assert reminders.status_code == 200, (
        f"a driver with nothing scheduled could not read their reminders: "
        f"{describe(reminders)}")
    assert reminders.json() == [], (
        f"a freshly created driver {email} already has reminders: {reminders.json()}")


def test_decoy_field_submission_is_refused(anon, backend):
    before = backend.count("drivers")
    email = probe_email()
    response = anon.post("/auth/signup", json={
        "email": email, "password": PASSWORD, "display_name": "Bot",
        "website": "http://spam.example"})
    assert 400 <= response.status_code < 500, (
        f"a submission arriving with the decoy field filled was accepted: "
        f"{describe(response)}")
    assert backend.count("drivers") == before, (
        f"the drivers table grew from {before} to {backend.count('drivers')} after a "
        f"refused decoy submission")


def test_repeated_submissions_are_refused(anon, backend):
    before = backend.count("drivers")
    statuses = []
    for _ in range(6):
        statuses.append(anon.post("/auth/signup", json={
            "email": probe_email(), "password": PASSWORD,
            "display_name": "Rapid Driver"}).status_code)
    assert any(400 <= code < 500 for code in statuses), (
        f"six signups from one origin inside a minute all succeeded with {statuses}; a "
        f"form submitted more than three times inside one minute is refused")
    written = backend.count("drivers") - before
    assert written <= 3, (
        f"{written} drivers rows were written by six rapid submissions; at most three "
        f"may be")


def test_security_headers_present_on_every_response(anon):
    for route in ("/", "/privacy", "/login"):
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=appclient.TIMEOUT)
        assert page.status_code == 200, (
            f"the public route {route} did not answer 200: {page.status_code}")
        headers = {key.lower(): value for key, value in page.headers.items()}
        assert "strict-transport-security" in headers, (
            f"{route} carries no strict transport policy header; it carries "
            f"{sorted(headers)}")
        assert headers.get("x-content-type-options", "").lower() == "nosniff", (
            f"{route} carries no nosniff content type policy header; it carries "
            f"{headers.get('x-content-type-options')!r}")
        assert PASSWORD not in page.text, (
            f"{route} serves the seeded password to the browser")
        assert "DB_ADMIN_URL" not in page.text, (
            f"{route} serves an admin credential name to the browser")


def test_social_preview_titles_are_unique_per_route(anon):
    seen = {}
    for route in PUBLIC_ROUTES:
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=appclient.TIMEOUT)
        assert page.status_code == 200, (
            f"the public route {route} did not answer 200: {page.status_code}")
        body = page.text
        assert "og:title" in body, (
            f"{route} declares no social preview title: {body[:300]}")
        assert "og:image" in body, (
            f"{route} declares no social preview image: {body[:300]}")
        marker = body.split("og:title", 1)[1][:200]
        assert marker not in seen.values(), (
            f"{route} shares its social preview title with "
            f"{[key for key, value in seen.items() if value == marker]}")
        seen[route] = marker

        source = body.split("og:image", 1)[1][:300]
        path = None
        for token in source.replace('"', " ").replace("'", " ").split():
            if token.startswith("/") or token.startswith("http"):
                path = token
                break
        assert path, f"{route} declares a social preview image with no address: {source[:200]}"
        url = path if path.startswith("http") else f"{appclient.app_url()}{path}"
        image = httpx.get(url, timeout=appclient.TIMEOUT)
        assert image.status_code == 200, (
            f"the social preview image {url} declared by {route} answered "
            f"{image.status_code}")


def test_health_endpoint_reports_ready(anon):
    ready = poll_until(lambda: anon.get("/health").status_code == 200)
    assert ready, (
        f"GET /api/health never answered 200 within the poll budget at "
        f"{appclient.api_base()}/health")
    response = anon.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health answered {response.status_code}: {response.text[:200]}")
    assert appclient.app_url().endswith(":4173") or "4173" not in appclient.app_url(), (
        f"APP_PUBLIC_URL is {appclient.app_url()!r}; the app is published through the "
        f"port mapping rather than a hardcoded container port")
    segments = anon.get("/segments")
    assert segments.status_code == 200, (
        f"the app reports ready but cannot serve its segments from the database: "
        f"{describe(segments)}")
    settle()
    still = anon.get("/health")
    assert still.status_code == 200, (
        f"GET /api/health stopped answering after a short wait: {still.status_code}")


def test_app_contract_artifacts_present():
    readme = pathlib.Path("/app/USER_README.md")
    assert readme.is_file(), (
        "the App Contract requires login credentials to be written to "
        "/app/USER_README.md; no such file exists at the app root")
    written = readme.read_text(encoding="utf-8", errors="replace")
    assert DRIVER_A in written, (
        f"/app/USER_README.md does not name the seeded account {DRIVER_A}; it reads "
        f"{written[:400]!r}")
    assert PASSWORD in written, (
        "/app/USER_README.md does not carry the seeded password beside the accounts")
    for reserved in ("/app/.browser_screenshots", "/app/.downloads"):
        folder = pathlib.Path(reserved)
        assert folder.is_dir(), (
            f"the App Contract reserves {reserved} at the app root; no such directory "
            f"exists")


def test_map_tiles_are_served_by_the_app(anon):
    origin = appclient.app_url()
    tile = httpx.get(f"{origin}/row-tiles/live/base/11/1/1", timeout=appclient.TIMEOUT)
    assert tile.status_code == 200, (
        f"the tile path /row-tiles/live/base/11/1/1 answered {tile.status_code}; the "
        f"app generates or proxies its own tiles rather than bundling one")
    assert tile.headers.get("content-type", "").startswith("image/"), (
        f"the tile path returned content-type "
        f"{tile.headers.get('content-type')!r} rather than an image")

    host = origin.split("//", 1)[-1].split("/", 1)[0]
    for route in ("/", "/ul"):
        page = httpx.get(f"{origin}{route}", timeout=appclient.TIMEOUT)
        assert page.status_code == 200, (
            f"the public route {route} did not answer 200: {page.status_code}")
        external = sorted({
            token.strip('"\'()<>,;')
            for token in page.text.replace(">", " ").replace("<", " ").split()
            if token.startswith(("http://", "https://", "//"))
            and host not in token
        })
        assert not external, (
            f"{route} references {len(external)} address(es) outside this app, so the "
            f"browser would reach a third party at run time: {external[:5]}")
