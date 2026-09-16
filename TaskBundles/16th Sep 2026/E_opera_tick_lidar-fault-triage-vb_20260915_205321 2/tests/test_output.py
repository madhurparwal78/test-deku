"""Deterministic graders for deku/lidar-fault-triage-vb.

Black box: every assertion goes through the deployed HTTP surface, the `db`
capability fixture or the `inbox` capability fixture. Nothing here imports the
agent's code or assumes its framework.

Sections are grouped in this one module, the fixed pytest file for every task.
"""

from __future__ import annotations

import re
import threading

import httpx
from appclient import client, login
from conftest import (
    ADMIN_EMAIL,
    DENIED,
    ENGINEER2_EMAIL,
    ENGINEER_EMAIL,
    OK,
    PAST_FLOWN_AT,
    PILOT_EMAIL,
    REFUSED,
    SEED_PASSWORD,
    SEEDED_SITES,
    SUBJECT_PREFIX,
    as_list,
    create_site,
    fault_zone,
    log_survey,
    logged_faults,
    poll_until,
    probe,
    settle,
    token_for,
)


def _one_fault(admin_client, pilot_client, asset_class: str = "wind_turbines",
               severity: int = 3, deformation_mm: int = 10):
    site = create_site(admin_client, asset_class)
    faults = logged_faults(log_survey(pilot_client, site["id"],
                                      [fault_zone(severity, deformation_mm)]))
    assert len(faults) == 1, f"a one-zone survey returned {len(faults)} faults: {faults}"
    return site, faults[0]


def _race_claims(fault_id, writers: int = 6) -> list[httpx.Response]:
    tokens = (token_for(ENGINEER_EMAIL), token_for(ENGINEER2_EMAIL))
    gate = threading.Barrier(writers)
    lock = threading.Lock()
    results: list[httpx.Response] = []

    def claim(token: str) -> None:
        with client(token) as c:
            gate.wait()
            r = c.post(f"/faults/{fault_id}/claim")
        with lock:
            results.append(r)

    threads = [threading.Thread(target=claim, args=(tokens[i % 2],)) for i in range(writers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)
    return results


def test_wrong_password_sign_in_is_refused_with_no_token(anon_client):
    """cov: C-CF-03"""
    r = anon_client.post("/auth/login", json={"email": ENGINEER_EMAIL,
                                              "password": "not-the-password"})
    assert r.status_code in (400, 401, 403), (
        f"POST /api/auth/login with a wrong password returned {r.status_code}: {r.text[:300]}"
    )
    assert "access_token" not in r.text, (
        f"a refused sign in returned a token-shaped body: {r.text[:300]}"
    )


def test_each_seeded_account_signs_in_with_the_seeded_password_and_receives_an_access_token(db):
    """cov: C-RL-12, C-DM-01, C-TR-03"""
    for email in (ADMIN_EMAIL, PILOT_EMAIL, ENGINEER_EMAIL, ENGINEER2_EMAIL):
        token = login(email, SEED_PASSWORD)
        assert token, f"{email} received no access_token for the seeded password"
        assert db.count_staff_with_email(email) == 1, (
            f"{email} is stored {db.count_staff_with_email(email)} times in staff"
        )


def test_site_owner_email_cannot_sign_in(anon_client):
    """cov: C-OV-04, C-CN-01"""
    r = anon_client.post("/auth/login", json={"email": "harrow.owner@example.com",
                                              "password": SEED_PASSWORD})
    assert r.status_code in (400, 401, 403), (
        f"the site owner harrow.owner@example.com signed in with {r.status_code}: {r.text[:300]}"
    )
    assert "access_token" not in r.text, f"a site owner received a token: {r.text[:300]}"


def test_deactivated_staff_account_sign_in_is_refused(admin_client, anon_client):
    """cov: C-CF-04"""
    email = f"pilot-{probe()}@example.com"
    made = admin_client.post("/staff", json={"email": email, "name": "Probe Pilot",
                                             "role": "pilot", "password": SEED_PASSWORD})
    assert made.status_code in OK, f"POST /api/staff returned {made.status_code}: {made.text[:300]}"
    staff_id = made.json().get("id")
    off = admin_client.patch(f"/staff/{staff_id}", json={"active": False})
    assert off.status_code in OK, f"PATCH /api/staff/{staff_id} returned {off.status_code}"
    r = anon_client.post("/auth/login", json={"email": email, "password": SEED_PASSWORD})
    assert r.status_code in (400, 401, 403), (
        f"a deactivated account signed in with {r.status_code}: {r.text[:300]}"
    )


def test_administrator_creates_a_site_that_is_stored_as_a_row(admin_client, db):
    """cov: C-RL-01"""
    site = create_site(admin_client, "substations")
    assert db.count_sites_named(site["name"]) == 1, (
        f"the site {site['name']!r} created by the administrator is not stored once in sites"
    )


def test_administrator_creates_a_staff_account(admin_client, db):
    """cov: C-RL-02"""
    email = f"engineer-{probe()}@example.com"
    r = admin_client.post("/staff", json={"email": email, "name": "Probe Engineer",
                                          "role": "engineer", "password": SEED_PASSWORD})
    assert r.status_code in OK, f"POST /api/staff returned {r.status_code}: {r.text[:300]}"
    row = db.staff_by_email(email)
    assert row is not None, f"the staff account {email} is not stored"
    assert str(row.get("role")) == "engineer", f"{email} is stored with role {row.get('role')!r}"


def test_staff_account_with_an_existing_email_is_refused(admin_client, db):
    """cov: C-DM-03"""
    r = admin_client.post("/staff", json={"email": PILOT_EMAIL, "name": "Duplicate",
                                          "role": "pilot", "password": SEED_PASSWORD})
    assert r.status_code in REFUSED, (
        f"a second staff account for {PILOT_EMAIL} answered {r.status_code}: {r.text[:300]}"
    )
    assert db.count_staff_with_email(PILOT_EMAIL) == 1, f"{PILOT_EMAIL} is stored twice"


def test_pilot_logged_survey_faults_are_stored_as_open_rows(admin_client, pilot_client, db):
    """cov: C-RL-03, C-CF-17, C-TR-01 (earned: the fault rows are read back from the PostgreSQL database at DATABASE_URL)"""
    site = create_site(admin_client, "solar_farms")
    r = log_survey(pilot_client, site["id"], [fault_zone(2), fault_zone(3), fault_zone(4)])
    faults = logged_faults(r)
    survey_id = r.json().get("id")
    rows = db.faults_for_survey(survey_id)
    assert len(rows) == 3, f"survey {survey_id} stored {len(rows)} fault rows, expected 3"
    assert all(str(row.get("status")) == "open" for row in rows), (
        f"new faults are not all open: {[row.get('status') for row in rows]}"
    )
    assert all(str(f.get("status")) == "open" for f in faults), (
        f"POST /api/surveys returned faults not open: {faults}"
    )


def test_pilot_claiming_a_fault_is_denied_and_the_row_stays_open(admin_client, pilot_client, db):
    """cov: C-RL-04"""
    _, fault = _one_fault(admin_client, pilot_client)
    r = pilot_client.post(f"/faults/{fault['id']}/claim")
    assert r.status_code in DENIED, (
        f"a pilot claiming fault {fault['id']} answered {r.status_code}: {r.text[:300]}"
    )
    assert str(db.fault(fault["id"]).get("status")) == "open", "a denied pilot claim changed the fault"


def test_pilot_creating_a_site_is_denied(pilot_client, db):
    """cov: C-RL-05"""
    name = f"Pilot Site {probe()}"
    r = pilot_client.post("/sites", json={"name": name, "asset_class": "power_lines",
                                          "region": "West", "owner_name": "Nobody",
                                          "owner_email": f"nobody-{probe()}@example.com"})
    assert r.status_code in DENIED, f"a pilot creating a site answered {r.status_code}"
    assert db.count_sites_named(name) == 0, f"a denied pilot request stored the site {name!r}"


def test_engineer_creating_a_site_is_denied_with_no_row_written(engineer_client, db):
    """cov: C-RL-08"""
    name = f"Engineer Site {probe()}"
    r = engineer_client.post("/sites", json={"name": name, "asset_class": "power_lines",
                                             "region": "West", "owner_name": "Nobody",
                                             "owner_email": f"nobody-{probe()}@example.com"})
    assert r.status_code in DENIED, f"an engineer creating a site answered {r.status_code}"
    assert db.count_sites_named(name) == 0, f"a denied engineer request stored the site {name!r}"


def test_engineer_creating_a_staff_account_is_denied(engineer_client, db):
    """cov: C-RL-09"""
    email = f"sneaky-{probe()}@example.com"
    r = engineer_client.post("/staff", json={"email": email, "name": "Sneaky",
                                             "role": "administrator", "password": SEED_PASSWORD})
    assert r.status_code in DENIED, f"an engineer creating a staff account answered {r.status_code}"
    assert db.count_staff_with_email(email) == 0, f"a denied engineer request stored {email}"


def test_second_engineer_confirming_a_held_fault_is_denied_and_the_fault_stays_claimed(
        admin_client, pilot_client, engineer_client, engineer2_client, db):
    """cov: C-RL-07, C-CF-33 (earned: the holding engineer is the only one whose confirm is not denied)"""
    _, fault = _one_fault(admin_client, pilot_client)
    held = engineer_client.post(f"/faults/{fault['id']}/claim")
    assert held.status_code in OK, f"the first engineer's claim returned {held.status_code}"
    r = engineer2_client.post(f"/faults/{fault['id']}/confirm")
    assert r.status_code in DENIED, (
        f"a second engineer confirming a held fault answered {r.status_code}: {r.text[:300]}"
    )
    row = db.fault(fault["id"])
    assert str(row.get("status")) == "claimed", f"the held fault is now {row.get('status')!r}"


def test_anonymous_caller_is_denied_on_every_mutating_endpoint(anon_client):
    """cov: C-RL-10, C-TR-04 (earned: a caller with no bearer token is refused on every endpoint that needs one)"""
    calls = (
        ("/sites", {"name": "x", "asset_class": "wind_turbines"}),
        ("/surveys", {"site_id": 1, "faults": []}),
        ("/faults/1/claim", {}),
        ("/faults/1/release", {}),
        ("/faults/1/confirm", {}),
        ("/faults/1/dismiss", {"reason": "anonymous reason"}),
        ("/staff", {"email": f"anon-{probe()}@example.com"}),
        ("/page-views", {"route": "/console"}),
    )
    for path, body in calls:
        r = anon_client.post(path, json=body)
        assert r.status_code in DENIED, (
            f"an anonymous POST /api{path} answered {r.status_code}: {r.text[:200]}"
        )


def test_site_with_an_unknown_asset_class_is_refused(admin_client, db):
    """cov: C-CF-06"""
    name = f"Offshore Site {probe()}"
    r = admin_client.post("/sites", json={"name": name, "asset_class": "offshore_rigs",
                                          "region": "Sea", "owner_name": "Nobody",
                                          "owner_email": f"sea-{probe()}@example.com"})
    assert r.status_code in REFUSED, f"an unknown asset class answered {r.status_code}"
    assert db.count_sites_named(name) == 0, f"a refused site {name!r} was stored"


def test_duplicate_site_name_is_refused(admin_client, db):
    """cov: C-CF-07"""
    r = admin_client.post("/sites", json={"name": "Harrow Ridge Wind Farm",
                                          "asset_class": "wind_turbines", "region": "North",
                                          "owner_name": "Copy",
                                          "owner_email": f"copy-{probe()}@example.com"})
    assert r.status_code in REFUSED, f"a duplicate site name answered {r.status_code}"
    assert db.count_sites_named("Harrow Ridge Wind Farm") == 1, "the site name is stored twice"


def test_survey_on_an_inactive_site_is_refused(admin_client, pilot_client, db):
    """cov: C-CF-08"""
    site = create_site(admin_client, "power_lines")
    off = admin_client.patch(f"/sites/{site['id']}", json={"active": False})
    assert off.status_code in OK, f"PATCH /api/sites/{site['id']} returned {off.status_code}"
    notes = f"inactive probe {probe()}"
    r = log_survey(pilot_client, site["id"], [fault_zone()], notes=notes)
    assert r.status_code in REFUSED, f"a survey on an inactive site answered {r.status_code}"
    assert db.count_surveys_with_notes(notes) == 0, "a survey on an inactive site was stored"


def test_survey_with_no_fault_zone_is_refused_and_stores_no_row(admin_client, pilot_client, db):
    """cov: C-CF-09, C-CF-15, C-CF-16, C-DM-09 (earned: the survey with its faults is written together or not at all), C-DC-05 (earned: an invalid call answers a client error)"""
    site = create_site(admin_client, "wind_turbines")
    notes = f"empty probe {probe()}"
    r = log_survey(pilot_client, site["id"], [], notes=notes)
    assert r.status_code in REFUSED, (
        f"a survey with no fault zone answered {r.status_code}: {r.text[:300]}"
    )
    assert db.count_surveys_with_notes(notes) == 0, "a rejected survey left a survey row"


def test_survey_with_twenty_one_fault_zones_is_refused(admin_client, pilot_client, db):
    """cov: C-CF-10"""
    site = create_site(admin_client, "wind_turbines")
    marker = f"Overflow zone {probe()}"
    zones = [fault_zone(location=marker) for _ in range(21)]
    notes = f"overflow probe {probe()}"
    r = log_survey(pilot_client, site["id"], zones, notes=notes)
    assert r.status_code in REFUSED, f"a survey with 21 fault zones answered {r.status_code}"
    assert db.count_surveys_with_notes(notes) == 0, "a rejected survey left a survey row"
    assert db.count_faults_at_location(marker) == 0, "a rejected survey left fault rows"


def test_fault_zone_with_an_unknown_kind_is_refused(admin_client, pilot_client, db):
    """cov: C-CF-11"""
    site = create_site(admin_client, "wind_turbines")
    marker = f"Rust zone {probe()}"
    r = log_survey(pilot_client, site["id"], [fault_zone(kind="rust", location=marker)])
    assert r.status_code in REFUSED, f"an unknown fault kind answered {r.status_code}"
    assert db.count_faults_at_location(marker) == 0, "a fault of an unknown kind was stored"


def test_fault_zone_ranked_above_four_is_refused(admin_client, pilot_client, db):
    """cov: C-CF-12"""
    site = create_site(admin_client, "wind_turbines")
    marker = f"Rank five zone {probe()}"
    r = log_survey(pilot_client, site["id"], [fault_zone(severity=5, location=marker)])
    assert r.status_code in REFUSED, f"a fault with severity 5 answered {r.status_code}"
    assert db.count_faults_at_location(marker) == 0, "a fault with severity 5 was stored"


def test_survey_flown_in_the_future_is_refused(admin_client, pilot_client, db):
    """cov: C-CF-13"""
    site = create_site(admin_client, "wind_turbines")
    notes = f"future probe {probe()}"
    r = pilot_client.post("/surveys", json={"site_id": site["id"],
                                            "flown_at": "2099-01-01T09:00:00Z",
                                            "coverage_km2": 5, "notes": notes,
                                            "faults": [fault_zone()]})
    assert r.status_code in REFUSED, f"a survey flown in 2099 answered {r.status_code}"
    assert db.count_surveys_with_notes(notes) == 0, "a future survey was stored"


def test_survey_coverage_above_one_hundred_is_refused(admin_client, pilot_client, db):
    """cov: C-CF-14"""
    site = create_site(admin_client, "wind_turbines")
    notes = f"coverage probe {probe()}"
    r = pilot_client.post("/surveys", json={"site_id": site["id"], "flown_at": PAST_FLOWN_AT,
                                            "coverage_km2": 150, "notes": notes,
                                            "faults": [fault_zone()]})
    assert r.status_code in REFUSED, f"a coverage of 150 answered {r.status_code}"
    assert db.count_surveys_with_notes(notes) == 0, "a survey over 100 square kilometres was stored"


def test_queue_lists_open_faults_in_rank_deformation_flown_order(admin_client, pilot_client,
                                                                 engineer_client):
    """cov: C-CF-19, C-CF-20, C-CF-21, C-CF-22"""
    site = create_site(admin_client, "wind_turbines")
    newer = logged_faults(log_survey(pilot_client, site["id"], [
        fault_zone(2, 50), fault_zone(4, 10), fault_zone(4, 30), fault_zone(3, 99)]))
    older = pilot_client.post("/surveys", json={"site_id": site["id"],
                                                "flown_at": "2026-01-10T09:00:00Z",
                                                "coverage_km2": 3, "notes": f"older {probe()}",
                                                "faults": [fault_zone(4, 10)]})
    older_fault = logged_faults(older)[0]
    by_zone = {(f["severity"], f["deformation_mm"]): f["id"] for f in newer}
    expected = [by_zone[(4, 30)], older_fault["id"], by_zone[(4, 10)], by_zone[(3, 99)],
                by_zone[(2, 50)]]
    r = engineer_client.get("/faults")
    assert r.status_code in OK, f"GET /api/faults returned {r.status_code}"
    listed = [f["id"] for f in as_list(r.json()) if f.get("id") in set(expected)]
    assert listed == expected, (
        f"the queue order for severity, deformation, flown-at is {listed}, expected {expected}"
    )


def test_queue_narrowed_by_asset_class_returns_only_that_class(admin_client, pilot_client,
                                                                engineer_client):
    """cov: C-CF-24"""
    _, solar = _one_fault(admin_client, pilot_client, "solar_farms")
    sites = {s["id"]: s["asset_class"] for s in as_list(engineer_client.get("/sites").json())}
    r = engineer_client.get("/faults", params={"asset_class": "solar_farms"})
    assert r.status_code in OK, f"GET /api/faults?asset_class=solar_farms returned {r.status_code}"
    rows = as_list(r.json())
    assert solar["id"] in [f.get("id") for f in rows], "the new solar fault is not in the narrowed queue"
    assert all(sites.get(f.get("site_id")) == "solar_farms" for f in rows), (
        f"the queue narrowed to solar_farms lists faults of other classes: "
        f"{sorted({str(sites.get(f.get('site_id'))) for f in rows})}"
    )


def test_engineer_claims_an_open_fault_which_becomes_claimed_with_one_history_entry(
        admin_client, pilot_client, engineer_client, db):
    """cov: C-RL-06, C-CF-26, C-CF-27, C-DM-06"""
    _, fault = _one_fault(admin_client, pilot_client)
    r = engineer_client.post(f"/faults/{fault['id']}/claim")
    assert r.status_code in OK, f"claiming fault {fault['id']} returned {r.status_code}: {r.text[:300]}"
    row = db.fault(fault["id"])
    assert str(row.get("status")) == "claimed", f"a claimed fault is stored as {row.get('status')!r}"
    assert row.get("claimed_by") is not None, "a claimed fault records no claimed_by"
    assert db.count_events(fault["id"], "claimed") == 1, "a claim did not write exactly one claimed entry"


def test_concurrent_claims_on_one_fault_admit_exactly_one_claimant(admin_client, pilot_client, db):
    """cov: C-CF-28, C-DM-05"""
    for round_n in range(8):
        _, fault = _one_fault(admin_client, pilot_client)
        results = _race_claims(fault["id"])
        won = [r for r in results if r.status_code in OK]
        assert len(won) == 1, (
            f"round {round_n}: {len(won)} of {len(results)} simultaneous claims on fault "
            f"{fault['id']} were accepted; statuses={sorted(r.status_code for r in results)}"
        )
        row = db.fault(fault["id"])
        assert str(row.get("status")) == "claimed", f"round {round_n}: status is {row.get('status')!r}"


def test_losing_concurrent_claim_is_refused_as_a_conflict_naming_the_holder(admin_client,
                                                                             pilot_client):
    """cov: C-CF-29"""
    _, fault = _one_fault(admin_client, pilot_client)
    results = _race_claims(fault["id"], writers=2)
    lost = [r for r in results if r.status_code not in OK]
    assert len(lost) == 1, f"expected one losing claim, got {[r.status_code for r in results]}"
    loser = lost[0]
    assert loser.status_code in REFUSED, f"the losing claim answered {loser.status_code}"
    assert loser.json().get("claimed_by"), (
        f"the losing claim does not carry claimed_by: {loser.text[:300]}"
    )


def test_concurrent_claims_record_exactly_one_claimed_history_row(admin_client, pilot_client, db):
    """cov: C-CF-30"""
    _, fault = _one_fault(admin_client, pilot_client)
    _race_claims(fault["id"])
    assert db.count_events(fault["id"], "claimed") == 1, (
        f"simultaneous claims left {db.count_events(fault['id'], 'claimed')} claimed rows "
        f"in fault_events for fault {fault['id']}"
    )


def test_claiming_a_decided_fault_is_refused_as_a_conflict(admin_client, pilot_client,
                                                           engineer_client, engineer2_client, db):
    """cov: C-CF-31"""
    _, fault = _one_fault(admin_client, pilot_client)
    engineer_client.post(f"/faults/{fault['id']}/claim")
    done = engineer_client.post(f"/faults/{fault['id']}/confirm")
    assert done.status_code in OK, f"confirming returned {done.status_code}"
    r = engineer2_client.post(f"/faults/{fault['id']}/claim")
    assert r.status_code in REFUSED, f"claiming a confirmed fault answered {r.status_code}"
    assert str(db.fault(fault["id"]).get("status")) == "confirmed", "a refused claim changed the fault"


def test_released_fault_returns_to_open_with_no_claimant_and_sends_no_email(
        admin_client, pilot_client, engineer_client, db, inbox):
    """cov: C-CF-32, C-CF-42"""
    site, fault = _one_fault(admin_client, pilot_client)
    engineer_client.post(f"/faults/{fault['id']}/claim")
    r = engineer_client.post(f"/faults/{fault['id']}/release")
    assert r.status_code in OK, f"releasing returned {r.status_code}: {r.text[:300]}"
    row = db.fault(fault["id"])
    assert str(row.get("status")) == "open", f"a released fault is stored as {row.get('status')!r}"
    assert row.get("claimed_by") is None, "a released fault still records claimed_by"
    settle()
    assert inbox.count(to=site["owner_email"]) == 0, "releasing a fault sent the owner an email"


def test_confirmed_fault_is_stored_confirmed_with_a_history_entry_and_leaves_the_queue(
        admin_client, pilot_client, engineer_client, db):
    """cov: C-OV-03, C-CF-35, C-CF-38, C-CF-43, C-DM-07 (earned: confirming is a decision whose decided_by is read back), C-DM-04 (earned: the stored status is one of the four named values)"""
    _, fault = _one_fault(admin_client, pilot_client)
    engineer_client.post(f"/faults/{fault['id']}/claim")
    r = engineer_client.post(f"/faults/{fault['id']}/confirm")
    assert r.status_code in OK, f"confirming returned {r.status_code}: {r.text[:300]}"
    row = db.fault(fault["id"])
    assert str(row.get("status")) == "confirmed", f"a confirmed fault is stored as {row.get('status')!r}"
    assert row.get("decided_by") is not None, "a confirmed fault records no decided_by"
    assert db.count_events(fault["id"], "confirmed") == 1, "confirming wrote no single confirmed entry"
    queue = [f.get("id") for f in as_list(engineer_client.get("/faults").json())]
    assert fault["id"] not in queue, "a confirmed fault is still listed in the queue"


def test_dismissal_with_a_short_reason_is_refused(admin_client, pilot_client, engineer_client, db):
    """cov: C-CF-36"""
    _, fault = _one_fault(admin_client, pilot_client)
    engineer_client.post(f"/faults/{fault['id']}/claim")
    r = engineer_client.post(f"/faults/{fault['id']}/dismiss", json={"reason": "too short"})
    assert r.status_code in REFUSED, f"a nine-character reason answered {r.status_code}"
    assert str(db.fault(fault["id"]).get("status")) == "claimed", "a refused dismissal changed the fault"


def test_dismissed_fault_stores_the_reason_and_sends_no_email(admin_client, pilot_client,
                                                              engineer_client, db, inbox):
    """cov: C-CF-37, C-CF-41"""
    site, fault = _one_fault(admin_client, pilot_client)
    engineer_client.post(f"/faults/{fault['id']}/claim")
    reason = f"Scan artefact from a wet blade, probe {probe()}"
    r = engineer_client.post(f"/faults/{fault['id']}/dismiss", json={"reason": reason})
    assert r.status_code in OK, f"dismissing returned {r.status_code}: {r.text[:300]}"
    row = db.fault(fault["id"])
    assert str(row.get("status")) == "dismissed", f"a dismissed fault is stored as {row.get('status')!r}"
    assert str(row.get("dismiss_reason")) == reason, f"dismiss_reason stored {row.get('dismiss_reason')!r}"
    settle()
    assert inbox.count(to=site["owner_email"]) == 0, "dismissing a fault sent the owner an email"


def test_confirmed_fault_sends_one_email_to_the_site_owner(admin_client, pilot_client,
                                                           engineer_client, inbox):
    """cov: C-OV-02, C-CF-39, C-TR-02 (earned: the message is found at Mailpit), C-DC-06 (earned: delivery through Mailpit is what is read back)"""
    site, fault = _one_fault(admin_client, pilot_client)
    engineer_client.post(f"/faults/{fault['id']}/claim")
    r = engineer_client.post(f"/faults/{fault['id']}/confirm")
    assert r.status_code in OK, f"confirming returned {r.status_code}"
    found = poll_until(lambda: inbox.find(to=site["owner_email"]))
    assert found, f"no email reached the site owner {site['owner_email']} after confirming"
    settle()
    assert inbox.count(to=site["owner_email"]) == 1, (
        f"the site owner received {inbox.count(to=site['owner_email'])} emails, expected exactly one"
    )


def test_confirmation_email_subject_begins_with_confirmed_fault_at_the_site_name(
        admin_client, pilot_client, engineer_client, inbox):
    """cov: C-CF-40"""
    site, fault = _one_fault(admin_client, pilot_client, severity=4)
    engineer_client.post(f"/faults/{fault['id']}/claim")
    engineer_client.post(f"/faults/{fault['id']}/confirm")
    found = poll_until(lambda: inbox.find(to=site["owner_email"], subject_contains=SUBJECT_PREFIX))
    assert found, f"no email to {site['owner_email']} has a subject containing {SUBJECT_PREFIX!r}"
    assert found.subject.startswith(f"{SUBJECT_PREFIX} {site['name']}"), (
        f"the subject {found.subject!r} does not begin with {SUBJECT_PREFIX!r} and the site name"
    )


def test_fault_history_entries_are_unchanged_after_a_later_decision(admin_client, pilot_client,
                                                                    engineer_client, db):
    """cov: C-DM-08"""
    _, fault = _one_fault(admin_client, pilot_client)
    engineer_client.post(f"/faults/{fault['id']}/claim")
    before = db.events(fault["id"], "claimed")
    engineer_client.post(f"/faults/{fault['id']}/dismiss",
                         json={"reason": f"Duplicate of an earlier finding {probe()}"})
    after = db.events(fault["id"], "claimed")
    assert before == after, f"the claimed entry changed after a later decision: {before} -> {after}"


def test_overview_open_count_rises_by_the_logged_fault_count(admin_client, pilot_client,
                                                              engineer_client):
    """cov: C-CF-44"""
    before = engineer_client.get("/overview").json()["power_lines"]["open"]
    site = create_site(admin_client, "power_lines")
    logged_faults(log_survey(pilot_client, site["id"], [fault_zone(), fault_zone(), fault_zone()]))
    after = engineer_client.get("/overview").json()["power_lines"]["open"]
    assert int(after) == int(before) + 3, (
        f"the power_lines open count moved from {before} to {after} after logging three faults"
    )


def test_overview_all_sites_figure_equals_the_sum_of_the_classes(engineer_client):
    """cov: C-CF-45"""
    body = engineer_client.get("/overview").json()
    classes = ("wind_turbines", "solar_farms", "power_lines", "substations")
    for status in ("open", "claimed", "confirmed", "dismissed"):
        total = sum(int(body[c][status]) for c in classes)
        assert int(body["all"][status]) == total, (
            f"the all figure for {status} is {body['all'][status]}, the classes sum to {total}"
        )


def test_recorded_page_view_is_counted_per_route_for_the_administrator(admin_client, db):
    """cov: C-CF-50, C-CF-51"""
    route = f"/console/queue?probe={probe()}"
    r = admin_client.post("/page-views", json={"route": route})
    assert r.status_code in OK, f"POST /api/page-views returned {r.status_code}"
    assert poll_until(lambda: db.count_page_views(route) >= 1), f"no page_views row for {route}"
    counts = as_list(admin_client.get("/page-views").json())
    assert any(c.get("route") == route and int(c.get("count", 0)) >= 1 for c in counts), (
        f"GET /api/page-views carries no count for {route}"
    )


def test_seeded_sites_exist_once_each_after_restart(db):
    """cov: C-DM-10, C-DM-12"""
    for name in SEEDED_SITES:
        assert db.count_sites_named(name) == 1, (
            f"the seeded site {name!r} is stored {db.count_sites_named(name)} times"
        )


def test_fault_list_is_a_top_level_array(engineer_client):
    """cov: C-DC-04"""
    r = engineer_client.get("/faults")
    assert r.status_code in OK, f"GET /api/faults returned {r.status_code}"
    assert isinstance(r.json(), list), f"GET /api/faults is not a top-level array: {r.text[:200]}"


def test_favicon_link_declared_in_the_head_resolves(app_url):
    """cov: C-TR-05"""
    page = httpx.get(f"{app_url}/", timeout=30.0)
    match = re.search(r"<link[^>]*rel=[\"'](?:shortcut )?icon[\"'][^>]*>", page.text, re.I)
    assert match, "the document head declares no rel=\"icon\" link"
    href = re.search(r"href=[\"']([^\"']+)[\"']", match.group(0))
    assert href, f"the icon link carries no href: {match.group(0)}"
    target = href.group(1)
    url = target if target.startswith("http") else f"{app_url}/{target.lstrip('/')}"
    icon = httpx.get(url, timeout=30.0)
    assert icon.status_code == 200 and icon.content, f"the favicon at {url} answered {icon.status_code}"


def test_every_response_carries_the_security_headers(anon_client):
    """cov: C-TR-06, C-TR-07"""
    r = anon_client.get("/health")
    headers = {k.lower(): v for k, v in r.headers.items()}
    assert "strict-transport-security" in headers, f"no Strict-Transport-Security header: {sorted(headers)}"
    assert headers.get("x-content-type-options", "").lower() == "nosniff", (
        f"X-Content-Type-Options is {headers.get('x-content-type-options')!r}, expected nosniff"
    )


def test_no_credential_appears_in_downloaded_frontend_files(app_url):
    """cov: C-TR-08, C-TR-09"""
    shell = httpx.get(f"{app_url}/", timeout=30.0)
    assets = re.findall(r"(?:src|href)=[\"'](/[^\"']+\.(?:js|css))[\"']", shell.text)
    bodies = [shell.text] + [httpx.get(f"{app_url}{a}", timeout=30.0).text for a in assets]
    for text in bodies:
        assert SEED_PASSWORD not in text, "the seeded password appears in a file the browser downloads"
        assert "deku-local-dev" not in text, "the database password appears in a downloaded file"
        assert "postgresql://" not in text, "a database connection string appears in a downloaded file"


def test_health_endpoint_returns_two_hundred_under_the_api_prefix(anon_client):
    """cov: C-TR-10, C-DC-02, C-DC-03, C-DC-01 (earned: the health call is made against APP_PUBLIC_URL)"""
    r = anon_client.get("/health")
    assert r.status_code == 200, f"GET /api/health returned {r.status_code}: {r.text[:200]}"
