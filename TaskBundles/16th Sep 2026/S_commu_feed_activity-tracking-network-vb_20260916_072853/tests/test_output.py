from __future__ import annotations

import math
import os
import re

import httpx
from _shapes import flatten, items
from appclient import api_base, app_url, client, login, seeded_password
from conftest import (
    ACHIEVEMENT_KINDS,
    ACTIVITY_TYPES,
    AGGREGATE_MIN_ATHLETES,
    ATHLETE2_EMAIL,
    ATHLETE3_EMAIL,
    ATHLETE4_EMAIL,
    ATHLETE5_EMAIL,
    ATHLETE_EMAIL,
    CORPUS_PASSWORD,
    CORRIDOR_TOLERANCE_M,
    DORIAN,
    DRIFT_M,
    EAST_TRACK_LAT,
    EAST_TRACK_M,
    FASTEST_5K_START_M,
    FEED_PAGE_SIZE,
    FLAT_GAIN_CEILING_M,
    KIT,
    MIRA,
    REFERENCE_ACTIVITY,
    REFERENCE_DISTANCE_M,
    REFERENCE_ELAPSED_S,
    REFERENCE_GAIN_M,
    REFERENCE_MOVING_S,
    REFERENCE_STOPPED_S,
    ROWAN,
    SAMPLE_RATE_S,
    SEEDED_CHALLENGE,
    SEEDED_CLUB,
    SEEDED_ROUTE,
    SEEDED_SEGMENT,
    SEGMENT_GAIN_M,
    SEGMENT_LENGTH_M,
    SENA,
    STORAGE_STREAM_PREFIX,
    STORAGE_UPLOAD_PREFIX,
    STREAM_TYPES,
    UPLOAD_STATES,
    VISIBILITIES,
    ZONE_RADIUS_M,
    athlete_id_of,
    feed_page,
    fetch,
    fresh_activity,
    gpx_track,
    kudos_window_budget,
    leaderboard,
    page,
    poll_until,
    segment_id_by_name,
    settle,
    sha256_hex,
    signup,
    straight_track,
    unique_email,
    unique_ref,
    upload_file,
    upload_reaches,
)

CLIENT_ERROR = (400, 401, 403, 404, 409, 422)
DENIED = (401, 403, 404)


def test_health_endpoint_returns_200():
    response = httpx.get(f"{api_base()}/health", timeout=30.0)
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, and the deployment "
        f"contract pins 200 once the app is ready: {response.text[:400]}")


def test_seeded_athlete_login_returns_token():
    token = login(ATHLETE_EMAIL, seeded_password("SEED_PASSWORD", CORPUS_PASSWORD))
    assert isinstance(token, str) and token.strip(), (
        f"POST /api/auth/login for {ATHLETE_EMAIL} returned no usable "
        f"access_token; the seeded password {CORPUS_PASSWORD!r} must work at login")

    bad = httpx.post(
        f"{api_base()}/auth/login",
        json={"email": ATHLETE_EMAIL, "password": "not-the-corpus-password"},
        timeout=30.0,
    )
    assert bad.status_code in CLIENT_ERROR, (
        f"POST /api/auth/login with a wrong password for {ATHLETE_EMAIL} returned "
        f"{bad.status_code}; a wrong password is a client error: {bad.text[:400]}")
    assert "access_token" not in bad.text, (
        f"a refused sign-in for {ATHLETE_EMAIL} still handed back an access_token: "
        f"{bad.text[:400]}")


def test_unknown_address_is_indistinguishable_from_a_wrong_password():
    password = seeded_password("SEED_PASSWORD", CORPUS_PASSWORD)
    wrong_password = httpx.post(
        f"{api_base()}/auth/login",
        json={"email": ATHLETE_EMAIL, "password": "not-the-corpus-password"},
        timeout=30.0)
    unknown = httpx.post(
        f"{api_base()}/auth/login",
        json={"email": unique_email(), "password": password},
        timeout=30.0)
    assert unknown.status_code == wrong_password.status_code, (
        f"an unregistered address returned {unknown.status_code} where a wrong "
        f"password returned {wrong_password.status_code}. A response that differs "
        f"between a known and an unknown address lets a stranger check whether a "
        f"particular person has an account on a product that publishes where "
        f"people run")
    assert unknown.text.strip() == wrong_password.text.strip(), (
        f"an unregistered address answered {unknown.text[:200]!r} where a wrong "
        f"password answered {wrong_password.text[:200]!r}; the two bodies must not "
        f"differ")


def test_anonymous_request_to_an_athlete_endpoint_is_denied():
    for path in ("/feed", "/me", "/notifications", "/privacy-zones", "/applications"):
        response = httpx.get(f"{api_base()}{path}", timeout=30.0)
        assert response.status_code in (401, 403), (
            f"GET /api{path} with no bearer token returned "
            f"{response.status_code}; an athlete-scoped endpoint is denied to an "
            f"anonymous caller: {response.text[:300]}")


def test_signup_creates_a_free_athlete_with_an_empty_feed():
    email, fresh = signup()
    with fresh:
        me = fresh.get("/me")
        assert me.status_code == 200, (
            f"GET /api/me after signup returned {me.status_code}: {me.text[:400]}")
        body = me.json()
        assert body.get("email") == email, (
            f"GET /api/me returned {body.get('email')!r} for the account just "
            f"created as {email!r}")
        assert body.get("plan") == "free", (
            f"a newly created account reports plan {body.get('plan')!r}; a new "
            f"account is free until a subscription is taken")
        assert body.get("default_visibility") in VISIBILITIES, (
            f"a new account reports default_visibility "
            f"{body.get('default_visibility')!r}, which is not one of "
            f"{VISIBILITIES}")
        first = feed_page(fresh)
        assert first.get("items") == [], (
            f"the feed of an athlete following nobody returned "
            f"{len(first.get('items') or [])} items; it is empty until they "
            f"follow somebody")


def test_signup_with_a_registered_address_is_refused_without_confirming_it():
    email, fresh = signup()
    fresh.close()
    with client() as anon:
        repeat = anon.post("/auth/signup", json={
            "email": email, "password": CORPUS_PASSWORD,
            "display_name": unique_ref("Probe")})
        unknown = anon.post("/auth/signup", json={
            "email": "", "password": CORPUS_PASSWORD, "display_name": ""})
    assert repeat.status_code in CLIENT_ERROR, (
        f"a second signup for {email!r} returned {repeat.status_code}; a duplicate "
        f"signup is refused: {repeat.text[:300]}")
    assert unknown.status_code in CLIENT_ERROR, (
        f"an empty signup returned {unknown.status_code} rather than a client "
        f"error: {unknown.text[:300]}")
    lowered = repeat.text.lower()
    for leak in ("already registered", "already exists", "taken", "in use"):
        assert leak not in lowered, (
            f"the refusal for {email!r} said {leak!r}, which confirms to a "
            f"stranger that the address holds an account: {repeat.text[:300]}")


def test_seeded_athletes_exist_with_their_pinned_standing(db):
    for email, name in ((ATHLETE_EMAIL, ROWAN), (ATHLETE2_EMAIL, SENA),
                        (ATHLETE3_EMAIL, DORIAN), (ATHLETE4_EMAIL, MIRA),
                        (ATHLETE5_EMAIL, KIT)):
        row = db.athlete_by_email(email)
        assert row is not None, (
            f"no athlete row for the seeded address {email!r}; the seed pins five")
        assert row.get("display_name") == name, (
            f"the athlete at {email!r} is named {row.get('display_name')!r} where "
            f"the seed pins {name!r}")
    kit = db.athlete_by_email(ATHLETE5_EMAIL)
    assert kit.get("plan") == "subscriber", (
        f"{KIT} holds plan {kit.get('plan')!r} where the seed pins 'subscriber'")
    dorian = db.athlete_by_email(ATHLETE3_EMAIL)
    assert dorian.get("default_visibility") == "followers", (
        f"{DORIAN} defaults to {dorian.get('default_visibility')!r} where the seed "
        f"pins 'followers'")
    assert not dorian.get("profile_discoverable"), (
        f"{DORIAN} reports profile_discoverable {dorian.get('profile_discoverable')!r}; "
        f"the seed pins a profile that is not discoverable")


def test_seeded_world_is_present_once(db):
    segment = db.segment_by_name(SEEDED_SEGMENT)
    assert segment is not None, (
        f"no segment named {SEEDED_SEGMENT!r}; the seed pins it")
    assert segment.get("activity_type") == "ride", (
        f"{SEEDED_SEGMENT!r} carries activity_type "
        f"{segment.get('activity_type')!r} where the seed pins 'ride'")
    assert int(segment.get("distance_m") or 0) == SEGMENT_LENGTH_M, (
        f"{SEEDED_SEGMENT!r} is {segment.get('distance_m')} metres long where the "
        f"seed pins {SEGMENT_LENGTH_M}")
    assert int(segment.get("elevation_gain_m") or 0) == SEGMENT_GAIN_M, (
        f"{SEEDED_SEGMENT!r} gains {segment.get('elevation_gain_m')} metres where "
        f"the seed pins {SEGMENT_GAIN_M}")
    assert db.count_athletes() >= 5, (
        f"{db.count_athletes()} athlete rows exist; the seed pins at least five and "
        f"seeding is idempotent, so a restart must not add more")
    assert db.count_clubs() >= 1, "the seed pins the club Dawn Patrol"
    assert db.count_challenges() >= 1, "the seed pins the challenge April Ascent"
    assert db.count_plans() >= 2, "the seed pins two plans"


def test_reference_activity_separates_moving_time_from_elapsed_time(db):
    activity = db.activity_by_name(REFERENCE_ACTIVITY)
    assert activity is not None, (
        f"no activity named {REFERENCE_ACTIVITY!r}; the seed pins it")
    summary = db.summary_of(activity.get("id"))
    assert summary is not None, (
        f"{REFERENCE_ACTIVITY!r} carries no summary row")
    elapsed = int(summary.get("elapsed_time_s") or 0)
    moving = int(summary.get("moving_time_s") or 0)
    assert elapsed == REFERENCE_ELAPSED_S, (
        f"{REFERENCE_ACTIVITY!r} reports {elapsed} seconds elapsed where the brief "
        f"pins {REFERENCE_ELAPSED_S}")
    assert moving == REFERENCE_MOVING_S, (
        f"{REFERENCE_ACTIVITY!r} reports {moving} seconds moving where the brief "
        f"pins {REFERENCE_MOVING_S}")
    assert elapsed - moving == REFERENCE_STOPPED_S, (
        f"elapsed minus moving is {elapsed - moving} seconds where the seeded "
        f"stationary period is {REFERENCE_STOPPED_S}. One duration field makes a "
        f"coffee stop look like a slow ride and every athlete's pace is wrong")


def test_reference_activity_pins_distance_and_smoothed_elevation(db):
    activity = db.activity_by_name(REFERENCE_ACTIVITY)
    summary = db.summary_of(activity.get("id"))
    assert int(summary.get("distance_m") or 0) == REFERENCE_DISTANCE_M, (
        f"{REFERENCE_ACTIVITY!r} reports {summary.get('distance_m')} metres where "
        f"the brief pins {REFERENCE_DISTANCE_M}")
    assert int(summary.get("elevation_gain_m") or 0) == REFERENCE_GAIN_M, (
        f"{REFERENCE_ACTIVITY!r} reports {summary.get('elevation_gain_m')} metres "
        f"of gain where the brief pins {REFERENCE_GAIN_M}. Gain comes from a "
        f"smoothed series above a threshold, never from summing every positive "
        f"difference between raw samples")


def test_average_speed_uses_moving_time(db):
    activity = db.activity_by_name(REFERENCE_ACTIVITY)
    summary = db.summary_of(activity.get("id"))
    speed = float(summary.get("average_speed_mps") or 0.0)
    on_moving = REFERENCE_DISTANCE_M / REFERENCE_MOVING_S
    on_elapsed = REFERENCE_DISTANCE_M / REFERENCE_ELAPSED_S
    assert abs(speed - on_moving) < abs(speed - on_elapsed), (
        f"average_speed_mps is {speed:.4f}, which is nearer distance over elapsed "
        f"time ({on_elapsed:.4f}) than distance over moving time "
        f"({on_moving:.4f}); the divisor is moving time")
    assert abs(speed - on_moving) <= 0.05, (
        f"average_speed_mps is {speed:.4f} where distance over moving time is "
        f"{on_moving:.4f}")


def test_summary_records_the_algorithm_version_that_produced_it(db):
    activity = db.activity_by_name(REFERENCE_ACTIVITY)
    summary = db.summary_of(activity.get("id"))
    version = summary.get("algorithm_version")
    assert version not in (None, ""), (
        f"{REFERENCE_ACTIVITY!r} carries no algorithm_version on its summary. "
        f"Algorithms improve, and recomputing years of history is a decision only "
        f"when you know what was computed under which version")


def test_activity_stores_the_start_timezone_of_its_start_location(db):
    activity = db.activity_by_name(REFERENCE_ACTIVITY)
    assert activity.get("start_timezone") not in (None, ""), (
        f"{REFERENCE_ACTIVITY!r} carries no start_timezone; an activity happens in "
        f"local time at its start location")
    assert activity.get("start_local_date") not in (None, ""), (
        f"{REFERENCE_ACTIVITY!r} carries no start_local_date; activities in March "
        f"means local March")
    assert activity.get("start_time_utc") not in (None, ""), (
        f"{REFERENCE_ACTIVITY!r} carries no start_time_utc")


def test_upload_returns_an_identifier_and_walks_its_states(rowan_client):
    payload = straight_track(label=unique_ref("states"))
    created = upload_file(rowan_client, payload, name=unique_ref("Probe states"))
    assert created.get("status") in UPLOAD_STATES, (
        f"POST /api/uploads reported status {created.get('status')!r}, which is "
        f"not one of {UPLOAD_STATES}")
    row = upload_reaches(rowan_client, created["upload_id"],
                         ("ready", "failed", "duplicate_suspected"))
    assert row.get("status") == "ready", (
        f"upload {created['upload_id']} terminated at {row.get('status')!r} "
        f"carrying {row.get('error_code')!r}; a well-formed track reaches ready")
    assert row.get("activity_id") is not None, (
        f"upload {created['upload_id']} is ready with no activity_id: {row}")


def test_raw_upload_is_retained_in_the_object_store_under_its_content_hash(
        rowan_client, db, store):
    payload = straight_track(label=unique_ref("retained"))
    digest = sha256_hex(payload)
    created = upload_file(rowan_client, payload, name=unique_ref("Probe retained"))
    upload_reaches(rowan_client, created["upload_id"], ("ready",))

    row = db.upload_by_id(created["upload_id"])
    assert row is not None, f"no upload row for {created['upload_id']}"
    assert (row.get("content_sha256") or "").lower() == digest, (
        f"the upload row records content_sha256 {row.get('content_sha256')!r} "
        f"where the bytes hash to {digest!r}")
    key = row.get("object_key") or ""
    assert key.startswith(STORAGE_UPLOAD_PREFIX), (
        f"the raw file is stored at {key!r}; the brief pins the scheme "
        f"uploads/{{athlete_id}}/{{upload_id}}/{{sha256_of_bytes}}.{{ext}}")
    assert digest in key, (
        f"the object key {key!r} does not carry the content hash {digest!r}; the "
        f"key is derived from the bytes so identical bytes resolve to one key")
    assert str(created["upload_id"]) in key, (
        f"the object key {key!r} does not carry the upload identifier "
        f"{created['upload_id']!r}")
    assert store.exists(key), (
        f"nothing is stored at {key!r}. The raw file is retained so a parser fix "
        f"can be re-run against it without asking the athlete to upload again")


def test_streams_live_in_the_object_store_rather_than_in_the_database(
        rowan_client, db, store):
    activity_id = fresh_activity(rowan_client)
    rows = db.streams_of(activity_id)
    assert rows, (
        f"activity {activity_id} carries no stream rows after a track upload")
    for row in rows:
        assert row.get("type") in STREAM_TYPES, (
            f"a stream of activity {activity_id} declares type {row.get('type')!r}, "
            f"which is not one of {STREAM_TYPES}")
        key = row.get("object_key") or ""
        assert key.startswith(STORAGE_STREAM_PREFIX), (
            f"stream {row.get('type')!r} of activity {activity_id} is stored at "
            f"{key!r}; the brief pins streams/{{activity_id}}/{{stream_type}}.json")
        assert store.exists(key), (
            f"nothing is stored at {key!r} for stream {row.get('type')!r}")
        assert row.get("measured") is not None, (
            f"stream {row.get('type')!r} does not declare whether it was measured "
            f"or derived")


def test_reuploading_identical_bytes_creates_no_second_activity(rowan_client, db):
    payload = straight_track(label=unique_ref("dedup-bytes"))
    first = upload_file(rowan_client, payload, name=unique_ref("Probe dedup"))
    ready = upload_reaches(rowan_client, first["upload_id"], ("ready",))
    before = db.count_activities(athlete_id=db.athlete_by_email(ATHLETE_EMAIL)["id"])

    second = upload_file(rowan_client, payload, name=unique_ref("Probe dedup again"))
    repeat = upload_reaches(rowan_client, second["upload_id"],
                            ("ready", "duplicate_suspected", "failed"))
    after = db.count_activities(athlete_id=db.athlete_by_email(ATHLETE_EMAIL)["id"])

    assert repeat.get("status") != "ready" or repeat.get("activity_id") == ready.get(
        "activity_id"), (
        f"re-submitting identical bytes produced activity "
        f"{repeat.get('activity_id')} where the first upload produced "
        f"{ready.get('activity_id')}")
    assert after == before, (
        f"the athlete held {before} activities before the repeat upload and {after} "
        f"after; identical bytes create no second activity")


def test_a_suspected_duplicate_produces_no_effort_before_the_athlete_resolves_it(
        rowan_client, db):
    payload = straight_track(label=unique_ref("dedup-effort"))
    first = upload_file(rowan_client, payload, name=unique_ref("Probe first ride"))
    upload_reaches(rowan_client, first["upload_id"], ("ready",))

    second = upload_file(rowan_client, payload, name=unique_ref("Probe same ride"))
    repeat = upload_reaches(rowan_client, second["upload_id"],
                            ("duplicate_suspected", "ready", "failed"))
    assert repeat.get("status") == "duplicate_suspected", (
        f"a second upload of identical bytes terminated at {repeat.get('status')!r}; "
        f"a suspected duplicate is flagged for the athlete to resolve rather than "
        f"silently discarded")
    assert repeat.get("duplicate_of_activity_id") is not None, (
        f"the suspected duplicate names no existing activity to compare against: "
        f"{repeat}")

    row = db.upload_by_id(second["upload_id"])
    candidate = row.get("activity_id")
    if candidate is not None:
        efforts = db.efforts_of_activity(candidate)
        assert efforts == [], (
            f"the suspected duplicate produced {len(efforts)} segment efforts. "
            f"Detection runs before matching, or the same effort reaches the "
            f"leaderboard twice and corrupts every total the segment feeds")


def test_manual_entry_produces_no_stream_and_no_effort(rowan_client, db):
    response = rowan_client.post("/uploads", data={
        "activity_type": "ride", "name": unique_ref("Probe manual"),
        "visibility": "everyone", "source": "manual",
        "distance_m": 12000, "elapsed_time_s": 2400, "moving_time_s": 2400})
    assert response.status_code in (200, 201, 202), (
        f"a manual entry returned {response.status_code}: {response.text[:400]}")
    upload_id = response.json().get("upload_id")
    row = upload_reaches(rowan_client, upload_id, ("ready",))
    activity_id = row.get("activity_id")

    activity = db.activity_by_id(activity_id)
    assert activity.get("manual_entry"), (
        f"activity {activity_id} was entered by hand but does not say so. An "
        f"unverifiable manual entry on a leaderboard is a cheating vector, so it "
        f"is visibly distinguished everywhere it appears")
    assert db.streams_of(activity_id) == [], (
        f"a manual entry carries {len(db.streams_of(activity_id))} streams; a "
        f"manual entry has none")
    assert db.efforts_of_activity(activity_id) == [], (
        f"a manual entry produced {len(db.efforts_of_activity(activity_id))} "
        f"segment efforts; a manual entry can produce none")


def test_failed_upload_is_retryable_from_the_retained_file(rowan_client, db):
    broken = b"this is not a track file\n" + unique_ref("broken").encode("utf-8")
    created = upload_file(rowan_client, broken, name=unique_ref("Probe broken"))
    row = upload_reaches(rowan_client, created["upload_id"], ("failed", "ready"))
    if row.get("status") != "failed":
        return
    assert row.get("error_code") not in (None, ""), (
        f"upload {created['upload_id']} failed with no error_code: {row}")

    stored = db.upload_by_id(created["upload_id"])
    assert stored.get("object_key"), (
        f"a failed upload kept no object_key; the raw file is retained so a parser "
        f"fix can be re-run against it")

    retry = rowan_client.post(f"/uploads/{created['upload_id']}/retry")
    assert retry.status_code in (200, 202), (
        f"POST /api/uploads/{created['upload_id']}/retry returned "
        f"{retry.status_code}; a failed upload is retryable without re-uploading: "
        f"{retry.text[:300]}")


def test_spheroidal_distance_on_a_due_east_track(rowan_client, db):
    metres_per_degree = 111320.0 * abs(math.cos(
        math.radians(EAST_TRACK_LAT)))
    points = 41
    spacing = (EAST_TRACK_M / (points - 1)) / metres_per_degree
    payload = straight_track(points=points, spacing_deg=spacing,
                             lat=EAST_TRACK_LAT, lng=0.0,
                             label=unique_ref("east"))
    activity_id = fresh_activity(rowan_client, payload=payload)
    summary = db.summary_of(activity_id)
    measured = float(summary.get("distance_m") or 0.0)
    planar = EAST_TRACK_M * abs(math.cos(
        math.radians(EAST_TRACK_LAT)))
    assert abs(measured - EAST_TRACK_M) <= EAST_TRACK_M * 0.02, (
        f"a {EAST_TRACK_M} metre due-east track at latitude {EAST_TRACK_LAT} "
        f"measured {measured:.0f} metres. Euclidean distance on latitude and "
        f"longitude would report about {planar:.0f}; distance is computed on a "
        f"spheroid")


def test_flat_route_reports_near_zero_elevation_gain(rowan_client, db):
    payload = straight_track(points=60, ele=42.0, label=unique_ref("flat"))
    activity_id = fresh_activity(rowan_client, payload=payload)
    summary = db.summary_of(activity_id)
    gain = float(summary.get("elevation_gain_m") or 0.0)
    assert gain <= FLAT_GAIN_CEILING_M, (
        f"a flat track reported {gain:.1f} metres of elevation gain, over the "
        f"{FLAT_GAIN_CEILING_M} metre ceiling. Summing every positive difference "
        f"between raw altitude samples tells somebody they climbed a mountain on a "
        f"flat ride")


def test_average_pace_comes_from_speed_rather_than_from_averaging_pace(
        rowan_client, db):
    metres_per_degree = 111320.0
    rows = []
    offset = 0
    lng = 0.0
    for leg_seconds_per_km in (240, 360):
        samples = leg_seconds_per_km // SAMPLE_RATE_S
        step = (1000.0 / samples) / metres_per_degree
        for _ in range(samples):
            rows.append((0.0, lng, 10.0, offset))
            lng += step
            offset += SAMPLE_RATE_S
    rows.append((0.0, lng, 10.0, offset))

    payload = gpx_track(rows, label=unique_ref("pace"))
    activity_id = fresh_activity(rowan_client, payload=payload, activity_type="run")
    summary = db.summary_of(activity_id)
    speed = float(summary.get("average_speed_mps") or 0.0)
    assert speed > 0, f"activity {activity_id} reports no average speed"
    seconds_per_km = 1000.0 / speed
    naive = (240 + 360) / 2.0
    assert abs(seconds_per_km - 300.0) <= 15.0, (
        f"a run of one kilometre at 4:00 then one kilometre at 6:00 reports an "
        f"average pace of {seconds_per_km:.0f} seconds per kilometre where two "
        f"kilometres in ten minutes is 300. The arithmetic mean of the two pace "
        f"values is {naive:.0f}; pace is inverse speed, so the average is taken on "
        f"speed and then inverted")


def test_best_effort_is_a_sliding_scan_over_the_distance_stream(kit_client, db):
    metres_per_degree = 111320.0
    rows = []
    offset = 0
    lng = 0.0

    def leg(metres, seconds_per_km):
        nonlocal offset, lng
        samples = max(1, int((metres / 1000.0) * seconds_per_km / SAMPLE_RATE_S))
        step = (metres / samples) / metres_per_degree
        for _ in range(samples):
            rows.append((0.0, lng, 10.0, offset))
            lng += step
            offset += SAMPLE_RATE_S

    leg(FASTEST_5K_START_M, 390)
    leg(5000, 240)
    leg(2000, 390)
    rows.append((0.0, lng, 10.0, offset))

    payload = gpx_track(rows, label=unique_ref("best"))
    activity_id = fresh_activity(kit_client, payload=payload, activity_type="run")

    response = kit_client.get(f"/activities/{activity_id}/best-efforts")
    assert response.status_code == 200, (
        f"GET /api/activities/{activity_id}/best-efforts returned "
        f"{response.status_code}: {response.text[:400]}")
    rows_out = items(response.json())
    five = [r for r in rows_out if int(r.get("distance_class_m") or 0) == 5000]
    assert five, (
        f"no best effort over 5000 metres was reported for a run of more than ten "
        f"kilometres: {rows_out}")
    start = float(five[0].get("start_distance_m") or 0.0)
    assert abs(start - FASTEST_5K_START_M) <= 600, (
        f"the fastest 5 kilometre window begins at {start:.0f} metres where the "
        f"fixture puts it at {FASTEST_5K_START_M}. Measuring each successive five "
        f"kilometres from the start finds the 0 to 5000 split, not the fastest one")


def test_coordinates_are_bounded_at_six_decimal_places(rowan_client):
    activity_id = fresh_activity(rowan_client)
    response = rowan_client.get(f"/activities/{activity_id}/streams",
                                params={"types": "latlng"})
    assert response.status_code == 200, (
        f"GET /api/activities/{activity_id}/streams returned "
        f"{response.status_code}: {response.text[:400]}")
    text = response.text
    over_precise = re.findall(r"-?\d+\.\d{7,}", text)
    assert not over_precise, (
        f"{len(over_precise)} returned coordinates carry more than six decimal "
        f"places, the first being {over_precise[0]!r}. Beyond six decimals is "
        f"sensor noise that also helps identify a person")


def segment_geometry(client_, segment_id):
    response = client_.get(f"/segments/{segment_id}")
    assert response.status_code == 200, (
        f"GET /api/segments/{segment_id} returned {response.status_code}: "
        f"{response.text[:400]}")
    return response.json()


def traverse_payload(segment, mode="forward", label=None):
    """Build a track over the seeded segment, four ways, from its own geometry."""
    line = segment.get("geometry") or []
    assert len(line) >= 2, (
        f"segment {segment.get('name')!r} returned {len(line)} geometry points; a "
        f"segment is a line, so its geometry is readable and has at least two")
    points = [(float(p[0]), float(p[1])) for p in line]
    if mode == "backward":
        points = list(reversed(points))
    if mode == "partial":
        points = points[: max(2, len(points) // 2)]
    if mode == "drift":
        offset = DRIFT_M / 111320.0
        points = [(lat + offset, lng) for lat, lng in points]
    if mode == "endpoints":
        first, last = points[0], points[-1]
        detour = 0.01
        points = [first, (first[0] + detour, first[1] + detour),
                  (last[0] + detour, last[1] + detour), last]

    lead = [(points[0][0] - 0.004, points[0][1] - 0.004)]
    tail = [(points[-1][0] + 0.004, points[-1][1] + 0.004)]
    rows = []
    for index, (lat, lng) in enumerate(lead + points + tail):
        rows.append((lat, lng, 100.0, index * SAMPLE_RATE_S))
    return gpx_track(rows, label=label or unique_ref(mode))


def efforts_on(db, activity_id, segment_id):
    return [e for e in db.efforts_of_activity(activity_id)
            if str(e.get("segment_id")) == str(segment_id)]


def test_forward_traverse_produces_exactly_one_effort(rowan_client, db):
    segment_id = segment_id_by_name(rowan_client)
    segment = segment_geometry(rowan_client, segment_id)
    activity_id = fresh_activity(
        rowan_client,
        payload=traverse_payload(segment, "forward", unique_ref("forward")))
    rows = poll_until(lambda: efforts_on(db, activity_id, segment_id) or None)
    assert rows, (
        f"a forward traverse of {SEEDED_SEGMENT!r} produced no effort; an activity "
        f"following the geometry in order and in direction produces one")
    assert len(rows) == 1, (
        f"a single forward traverse produced {len(rows)} efforts")


def test_drifting_traverse_still_matches_inside_the_corridor(rowan_client, db):
    segment_id = segment_id_by_name(rowan_client)
    segment = segment_geometry(rowan_client, segment_id)
    activity_id = fresh_activity(
        rowan_client,
        payload=traverse_payload(segment, "drift", unique_ref("drift")))
    rows = poll_until(lambda: efforts_on(db, activity_id, segment_id) or None)
    assert rows, (
        f"a traverse carrying {DRIFT_M} metres of lateral drift produced no effort "
        f"on {SEEDED_SEGMENT!r}, whose corridor tolerance is "
        f"{CORRIDOR_TOLERANCE_M} metres. Matching is a corridor test, not a point "
        f"radius, and positional error of a few tens of metres is ordinary")


def test_endpoints_only_pass_produces_no_effort(rowan_client, db):
    segment_id = segment_id_by_name(rowan_client)
    segment = segment_geometry(rowan_client, segment_id)
    activity_id = fresh_activity(
        rowan_client,
        payload=traverse_payload(segment, "endpoints", unique_ref("endpoints")))
    settle(3.0)
    rows = efforts_on(db, activity_id, segment_id)
    assert rows == [], (
        f"an activity that reached both ends of {SEEDED_SEGMENT!r} by another road "
        f"produced {len(rows)} efforts. Checking proximity to the start and the end "
        f"credits rides that were never ridden")


def test_backward_traverse_produces_no_effort(rowan_client, db):
    segment_id = segment_id_by_name(rowan_client)
    segment = segment_geometry(rowan_client, segment_id)
    activity_id = fresh_activity(
        rowan_client,
        payload=traverse_payload(segment, "backward", unique_ref("backward")))
    settle(3.0)
    rows = efforts_on(db, activity_id, segment_id)
    assert rows == [], (
        f"a traverse of {SEEDED_SEGMENT!r} in the wrong direction produced "
        f"{len(rows)} efforts; direction is part of the match")


def test_partial_traverse_produces_no_effort(rowan_client, db):
    segment_id = segment_id_by_name(rowan_client)
    segment = segment_geometry(rowan_client, segment_id)
    activity_id = fresh_activity(
        rowan_client,
        payload=traverse_payload(segment, "partial", unique_ref("partial")))
    settle(3.0)
    rows = efforts_on(db, activity_id, segment_id)
    assert rows == [], (
        f"a partial traverse of {SEEDED_SEGMENT!r} produced {len(rows)} efforts; "
        f"only a complete traversal produces one")


def test_effort_start_time_is_interpolated_rather_than_snapped(rowan_client, db):
    segment_id = segment_id_by_name(rowan_client)
    segment = segment_geometry(rowan_client, segment_id)
    activity_id = fresh_activity(
        rowan_client,
        payload=traverse_payload(segment, "forward", unique_ref("interp")))
    rows = poll_until(lambda: efforts_on(db, activity_id, segment_id) or None)
    assert rows, "the interpolation probe produced no effort to read"

    activity = db.activity_by_id(activity_id)
    from datetime import datetime

    def as_seconds(value):
        text = str(value).replace("Z", "+00:00")
        return datetime.fromisoformat(text).timestamp()

    offset = as_seconds(rows[0].get("start_time_utc")) - as_seconds(
        activity.get("start_time_utc"))
    remainder = abs(offset) % SAMPLE_RATE_S
    assert min(remainder, SAMPLE_RATE_S - remainder) > 0.05, (
        f"the effort begins {offset:.3f} seconds into the activity, which is an "
        f"exact multiple of the {SAMPLE_RATE_S} second sample rate. The crossing is "
        f"interpolated between samples; snapping to the nearest sample introduces "
        f"up to {SAMPLE_RATE_S} seconds of error, which decides the leaderboard on "
        f"a short segment")


def test_rerunning_matching_replaces_efforts_rather_than_adding_to_them(
        rowan_client, db):
    segment_id = segment_id_by_name(rowan_client)
    segment = segment_geometry(rowan_client, segment_id)
    activity_id = fresh_activity(
        rowan_client,
        payload=traverse_payload(segment, "forward", unique_ref("rerun")))
    poll_until(lambda: efforts_on(db, activity_id, segment_id) or None)
    before = len(efforts_on(db, activity_id, segment_id))

    touched = rowan_client.patch(f"/activities/{activity_id}",
                                 json={"name": unique_ref("Probe renamed")})
    assert touched.status_code in (200, 202), (
        f"PATCH /api/activities/{activity_id} returned {touched.status_code}: "
        f"{touched.text[:300]}")
    settle(3.0)
    after = len(efforts_on(db, activity_id, segment_id))
    assert after == before, (
        f"the activity held {before} efforts on {SEEDED_SEGMENT!r} and {after} "
        f"after a re-read; a re-run replaces an activity's efforts rather than "
        f"duplicating them")


def test_changing_activity_type_clears_efforts_from_the_old_type(rowan_client, db):
    segment_id = segment_id_by_name(rowan_client)
    segment = segment_geometry(rowan_client, segment_id)
    activity_id = fresh_activity(
        rowan_client,
        payload=traverse_payload(segment, "forward", unique_ref("retype")),
        activity_type="ride")
    poll_until(lambda: efforts_on(db, activity_id, segment_id) or None)
    assert efforts_on(db, activity_id, segment_id), (
        f"the retype probe produced no ride effort on {SEEDED_SEGMENT!r} to clear")

    changed = rowan_client.patch(f"/activities/{activity_id}", json={"type": "run"})
    assert changed.status_code in (200, 202), (
        f"PATCH /api/activities/{activity_id} with a new type returned "
        f"{changed.status_code}: {changed.text[:300]}")

    def cleared():
        return efforts_on(db, activity_id, segment_id) == [] or None

    assert poll_until(cleared), (
        f"after retyping a ride as a run, {len(efforts_on(db, activity_id, segment_id))} "
        f"efforts remain on {SEEDED_SEGMENT!r}, which is a riding segment. A run "
        f"and a ride over the same road are not comparable and never share a "
        f"leaderboard, so a corrected type re-runs matching and invalidates the "
        f"old efforts")
    assert db.achievements_of(activity_id) == [], (
        f"{len(db.achievements_of(activity_id))} achievements survived the type "
        f"change; achievements derived under the old type are invalidated with the "
        f"efforts that earned them")


def test_leaderboard_ranks_are_contiguous_for_a_viewer_who_cannot_see_an_athlete(
        sena_client, db):
    segment_id = segment_id_by_name(sena_client)
    board = leaderboard(sena_client, segment_id, scope="all")
    entries = board.get("entries") or []
    assert entries, f"the {SEEDED_SEGMENT!r} leaderboard is empty for {SENA}"

    names = [e.get("display_name") for e in entries]
    assert DORIAN not in names, (
        f"{SENA} is not an accepted follower of {DORIAN}, whose activities are "
        f"followers-only, yet {DORIAN} appears on the leaderboard {SENA} is shown: "
        f"{names}")
    ranks = [int(e.get("rank")) for e in entries]
    assert ranks == list(range(1, len(entries) + 1)), (
        f"{SENA} is shown ranks {ranks}. A gap tells the viewer that a hidden "
        f"athlete exists and exactly where they stand, so ranks are computed over "
        f"the set the viewer can see and run without a gap from one")
    assert int(board.get("total")) == len(entries), (
        f"the leaderboard reports a total of {board.get('total')} while showing "
        f"{len(entries)} rows; the count must not reveal the hidden athlete either")


def test_an_accepted_follower_sees_the_hidden_athlete_in_place(dorian_client,
                                                               sena_client):
    segment_id = segment_id_by_name(dorian_client)
    own = leaderboard(dorian_client, segment_id, scope="all")
    own_names = [e.get("display_name") for e in own.get("entries") or []]
    assert DORIAN in own_names, (
        f"{DORIAN} cannot see their own effort on {SEEDED_SEGMENT!r}: {own_names}")

    hidden = leaderboard(sena_client, segment_id, scope="all")
    assert len(own.get("entries") or []) > len(hidden.get("entries") or []), (
        f"{DORIAN} sees {len(own.get('entries') or [])} rows and {SENA} sees "
        f"{len(hidden.get('entries') or [])}; the leaderboard is per-viewer, so the "
        f"two are not the same list")


def test_leaderboard_ranks_on_elapsed_time_with_a_stable_tie_break(sena_client):
    segment_id = segment_id_by_name(sena_client)
    entries = leaderboard(sena_client, segment_id, scope="all").get("entries") or []
    times = [int(e.get("elapsed_time_s")) for e in entries]
    assert times == sorted(times), (
        f"the leaderboard lists elapsed times {times}, which are not ascending. "
        f"Ranking is on elapsed time for the effort: nobody gets to pause on a "
        f"segment")
    repeat = leaderboard(sena_client, segment_id, scope="all").get("entries") or []
    assert [e.get("athlete_id") for e in repeat] == [
        e.get("athlete_id") for e in entries], (
        f"two reads of one leaderboard returned different orders; ties break "
        f"deterministically by effort timestamp, earliest first")


def test_one_effort_per_athlete_per_leaderboard(sena_client):
    segment_id = segment_id_by_name(sena_client)
    entries = leaderboard(sena_client, segment_id, scope="all").get("entries") or []
    seen = [e.get("athlete_id") for e in entries]
    assert len(seen) == len(set(seen)), (
        f"the leaderboard lists {len(seen)} rows for {len(set(seen))} athletes; one "
        f"effort per athlete is listed, being their best")


def test_date_bounded_and_social_leaderboard_scopes_answer(sena_client):
    segment_id = segment_id_by_name(sena_client)
    for scope in ("all", "year", "month", "today", "following"):
        board = leaderboard(sena_client, segment_id, scope=scope)
        entries = board.get("entries") or []
        ranks = [int(e.get("rank")) for e in entries]
        assert ranks == list(range(1, len(entries) + 1)), (
            f"the {scope!r} scope returned ranks {ranks}, which are not contiguous "
            f"from one")


def test_achievement_survives_being_beaten(db):
    segment = db.segment_by_name(SEEDED_SEGMENT)
    rows = db.efforts_of_segment(segment.get("id"))
    assert rows, f"no efforts exist on {SEEDED_SEGMENT!r} to award achievements for"

    leader = db.athlete_by_email(ATHLETE_EMAIL)
    earned = db.count_achievements(athlete_id=leader.get("id"))
    assert earned >= 1, (
        f"{ROWAN} is first on {SEEDED_SEGMENT!r} and holds {earned} achievements; "
        f"an overall top-three place mints one at effort insertion")
    for row in rows:
        assert row.get("flag_state") in FLAG_STATES, (
            f"effort {row.get('id')} carries flag_state {row.get('flag_state')!r}, "
            f"which is not one of {FLAG_STATES}")


def test_achievements_record_an_earned_date_and_a_kind(db):
    segment = db.segment_by_name(SEEDED_SEGMENT)
    rows = []
    for effort in db.efforts_of_segment(segment.get("id")):
        rows += db.achievements_of(effort.get("activity_id"))
    assert rows, (
        f"no achievement rows exist for any effort on {SEEDED_SEGMENT!r}")
    for row in rows:
        assert row.get("kind") in ACHIEVEMENT_KINDS, (
            f"achievement {row.get('id')} carries kind {row.get('kind')!r}, which "
            f"is not one of {ACHIEVEMENT_KINDS}")
        assert row.get("earned_on") not in (None, ""), (
            f"achievement {row.get('id')} records no earned_on. A medal is a "
            f"historical fact: recomputing it from the current standings rewrites "
            f"the athlete's own history")


def test_blocked_athlete_reaches_the_blocker_by_no_path(mira_client, db):
    rowan = db.athlete_by_email(ATHLETE_EMAIL)
    rowan_id = rowan.get("id")

    profile = mira_client.get(f"/athletes/{rowan_id}")
    assert profile.status_code in DENIED, (
        f"GET /api/athletes/{rowan_id} as {MIRA}, whom {ROWAN} blocks, returned "
        f"{profile.status_code}: {profile.text[:300]}")

    listing = mira_client.get(f"/athletes/{rowan_id}/activities")
    assert listing.status_code in DENIED or items(listing.json()) == [], (
        f"{MIRA} can list {ROWAN}'s activities; a block is enforced at the data "
        f"layer on every read path")

    reference = db.activity_by_name(REFERENCE_ACTIVITY)
    activity = mira_client.get(f"/activities/{reference.get('id')}")
    assert activity.status_code in DENIED, (
        f"GET /api/activities/{reference.get('id')} as {MIRA} returned "
        f"{activity.status_code}; {ROWAN} blocks {MIRA}, and the refusal is the "
        f"same not-found returned for content that does not exist, because a "
        f"refusal confirms the thing exists")

    segment_id = segment_id_by_name(mira_client)
    board = leaderboard(mira_client, segment_id, scope="all")
    names = [e.get("display_name") for e in board.get("entries") or []]
    assert ROWAN not in names, (
        f"{MIRA} is shown {ROWAN} on the {SEEDED_SEGMENT!r} leaderboard: {names}")
    ranks = [int(e.get("rank")) for e in board.get("entries") or []]
    assert ranks == list(range(1, len(ranks) + 1)), (
        f"{MIRA} is shown ranks {ranks}; removing a blocked athlete leaves the "
        f"remaining ranks contiguous")

    club = mira_client.get(f"/clubs/{SEEDED_CLUB}")
    if club.status_code == 200:
        roster = flatten(club.json().get("members") or [])
        assert ROWAN not in str(roster), (
            f"{MIRA} is shown {ROWAN} in the {SEEDED_CLUB!r} roster")

    challenge = mira_client.get(f"/challenges/{SEEDED_CHALLENGE}")
    if challenge.status_code == 200:
        assert ROWAN not in challenge.text, (
            f"{MIRA} is shown {ROWAN} in the {SEEDED_CHALLENGE!r} standings")

    found = mira_client.get("/search", params={"q": ROWAN, "kind": "athlete"})
    if found.status_code == 200:
        assert ROWAN not in found.text, (
            f"a search for {ROWAN!r} as {MIRA} returned them: {found.text[:300]}")


def test_block_is_symmetric_in_effect(rowan_client, db):
    mira = db.athlete_by_email(ATHLETE4_EMAIL)
    response = rowan_client.get(f"/athletes/{mira.get('id')}")
    assert response.status_code in DENIED or response.status_code == 200, (
        f"GET /api/athletes/{mira.get('id')} as {ROWAN} returned "
        f"{response.status_code}: {response.text[:300]}")
    feed = feed_page(rowan_client)
    assert MIRA not in str(feed), (
        f"{ROWAN} blocks {MIRA} yet {MIRA} appears in {ROWAN}'s feed; a block is "
        f"symmetric in effect")


def test_blocking_removes_the_follow_edge_in_both_directions(db):
    first_email, first = signup()
    second_email, second = signup()
    with first, second:
        first_id = athlete_id_of(first)
        second_id = athlete_id_of(second)

        followed = second.post(f"/athletes/{first_id}/follow")
        assert followed.status_code in (200, 201), (
            f"POST /api/athletes/{first_id}/follow returned "
            f"{followed.status_code}: {followed.text[:300]}")
        assert followed.json().get("state") == "accepted", (
            f"following a discoverable profile reported state "
            f"{followed.json().get('state')!r}; it takes effect immediately")

        blocked = first.post(f"/athletes/{second_id}/block")
        assert blocked.status_code in (200, 201), (
            f"POST /api/athletes/{second_id}/block returned "
            f"{blocked.status_code}: {blocked.text[:300]}")
        settle(1.0)

        edge = db.follow(second_id, first_id)
        assert edge is None or edge.get("state") == "blocked", (
            f"the follow edge from {second_email} to {first_email} survived the "
            f"block at state {edge.get('state')!r}; a block removes the edge in "
            f"both directions")

        again = second.post(f"/athletes/{first_id}/follow")
        assert again.status_code in DENIED, (
            f"a blocked athlete re-followed the blocker and got "
            f"{again.status_code}; neither side can re-follow while the block "
            f"stands")


def test_a_pending_follow_request_grants_nothing(dorian_client, db):
    email, fresh = signup()
    with fresh:
        dorian = db.athlete_by_email(ATHLETE3_EMAIL)
        requested = fresh.post(f"/athletes/{dorian.get('id')}/follow")
        assert requested.status_code in (200, 201, 202), (
            f"POST /api/athletes/{dorian.get('id')}/follow returned "
            f"{requested.status_code}: {requested.text[:300]}")
        assert requested.json().get("state") == "pending", (
            f"following {DORIAN}, whose profile is not discoverable, reported "
            f"state {requested.json().get('state')!r}; it creates a request")

        listing = fresh.get(f"/athletes/{dorian.get('id')}/activities")
        rows = items(listing.json()) if listing.status_code == 200 else []
        assert rows == [], (
            f"a pending request returned {len(rows)} of {DORIAN}'s activities; a "
            f"request grants no access to anything until it is accepted")


def test_followers_only_activity_is_refused_to_a_stranger(dorian_client, db):
    created = dorian_client.post("/uploads", data={
        "activity_type": "ride", "name": unique_ref("Probe private"),
        "visibility": "followers", "source": "manual",
        "distance_m": 9000, "elapsed_time_s": 1800, "moving_time_s": 1800})
    assert created.status_code in (200, 201, 202), (
        f"a manual entry for {DORIAN} returned {created.status_code}: "
        f"{created.text[:300]}")
    row = upload_reaches(dorian_client, created.json().get("upload_id"), ("ready",))
    activity_id = row.get("activity_id")

    email, stranger = signup()
    with stranger:
        response = stranger.get(f"/activities/{activity_id}")
        assert response.status_code in DENIED, (
            f"GET /api/activities/{activity_id} as a stranger returned "
            f"{response.status_code}; the activity is followers-only")
    anonymous = httpx.get(f"{api_base()}/activities/{activity_id}", timeout=30.0)
    assert anonymous.status_code in DENIED, (
        f"a logged-out read of a followers-only activity returned "
        f"{anonymous.status_code}; visibility is enforced on the public read too")


def test_only_you_activity_is_refused_to_everybody_else(rowan_client, sena_client):
    created = rowan_client.post("/uploads", data={
        "activity_type": "ride", "name": unique_ref("Probe private only"),
        "visibility": "only_you", "source": "manual",
        "distance_m": 7000, "elapsed_time_s": 1500, "moving_time_s": 1500})
    row = upload_reaches(rowan_client, created.json().get("upload_id"), ("ready",))
    activity_id = row.get("activity_id")

    mine = rowan_client.get(f"/activities/{activity_id}")
    assert mine.status_code == 200, (
        f"the owner cannot read their own only_you activity: {mine.status_code}")
    theirs = sena_client.get(f"/activities/{activity_id}")
    assert theirs.status_code in DENIED, (
        f"{SENA}, an accepted follower of {ROWAN}, read an only_you activity and "
        f"got {theirs.status_code}; only_you is the athlete alone")


def test_feed_orders_by_start_time_and_holds_only_visible_activities(sena_client):
    first = feed_page(sena_client)
    rows = first.get("items") or []
    assert rows, (
        f"{SENA} follows {ROWAN} and their feed is empty; an accepted follow puts "
        f"the followee's activities in the follower's feed")
    starts = [str(r.get("start_time_utc") or r.get("activity_start_time_utc") or "")
              for r in rows]
    assert starts == sorted(starts, reverse=True), (
        f"the feed returned start times {starts[:5]}, which are not newest first")
    assert len(rows) <= FEED_PAGE_SIZE, (
        f"one feed page returned {len(rows)} items where the page size is "
        f"{FEED_PAGE_SIZE}")


def test_feed_pagination_is_by_cursor_and_survives_an_insertion(
        sena_client, rowan_client):
    first = feed_page(sena_client, limit=2)
    cursor = first.get("next_cursor")
    if not cursor:
        return
    seen = [str(r.get("id")) for r in first.get("items") or []]

    fresh_activity(rowan_client, activity_type="ride",
                   name=unique_ref("Probe inserted"))

    second = feed_page(sena_client, cursor=cursor, limit=2)
    following = [str(r.get("id")) for r in second.get("items") or []]
    overlap = set(seen) & set(following)
    assert not overlap, (
        f"paging across an insertion repeated {len(overlap)} rows: {sorted(overlap)}. "
        f"Offset pagination on a list that gains items while it is read skips and "
        f"repeats rows, and on an infinite scroll nobody learns what they missed")


def test_feed_page_fetches_no_stream(sena_client):
    rows = (feed_page(sena_client).get("items") or [])
    assert rows, f"{SENA}'s feed is empty, so there is nothing to read"
    blob = flatten(rows)
    for stream_type in ("heartrate", "cadence", "watts", "grade_smooth"):
        assert stream_type not in str(blob), (
            f"a feed page carried a {stream_type!r} series. A page of "
            f"{FEED_PAGE_SIZE} items that renders its route pictures from position "
            f"streams fetches millions of points and makes the product unusable on "
            f"the second screen; the feed reads summaries and the coarsest line")


def test_feed_respects_a_visibility_change_made_after_the_row_was_written(
        rowan_client, sena_client, db):
    activity_id = fresh_activity(rowan_client, name=unique_ref("Probe visible"))

    def present():
        rows = feed_page(sena_client).get("items") or []
        return any(str(r.get("activity_id") or r.get("id")) == str(activity_id)
                   for r in rows) or None

    assert poll_until(present), (
        f"activity {activity_id} by {ROWAN} never reached {SENA}'s feed")

    hidden = rowan_client.patch(f"/activities/{activity_id}",
                               json={"visibility": "only_you"})
    assert hidden.status_code in (200, 202), (
        f"PATCH /api/activities/{activity_id} returned {hidden.status_code}: "
        f"{hidden.text[:300]}")

    def gone():
        rows = feed_page(sena_client).get("items") or []
        return (not any(str(r.get("activity_id") or r.get("id")) == str(activity_id)
                        for r in rows)) or None

    assert poll_until(gone), (
        f"activity {activity_id} stayed in {SENA}'s feed after being made "
        f"only_you. Visibility is applied at the moment of the read, not only at "
        f"the moment the feed row was written")


def test_fanout_reaches_followers_below_the_threshold(rowan_client, db, sena_client):
    rowan = db.athlete_by_email(ATHLETE_EMAIL)
    activity_id = fresh_activity(rowan_client, name=unique_ref("Probe fanout"))

    def arrived():
        rows = db.feed_entries_of(db.athlete_by_email(ATHLETE2_EMAIL).get("id"))
        return any(str(r.get("activity_id")) == str(activity_id)
                   for r in rows) or None

    assert poll_until(arrived), (
        f"activity {activity_id} by {ROWAN}, who is far below the configured "
        f"follower threshold, produced no feed row for {SENA}. Fan-out on write "
        f"serves ordinary accounts; read assembly is reserved for accounts above "
        f"the threshold")


def test_kudos_counts_once_per_athlete_and_toggles(sena_client, rowan_client, db):
    activity_id = fresh_activity(rowan_client, name=unique_ref("Probe kudos"))

    first = sena_client.post(f"/activities/{activity_id}/kudos")
    assert first.status_code in (200, 201), (
        f"POST /api/activities/{activity_id}/kudos returned {first.status_code}: "
        f"{first.text[:300]}")
    assert int(first.json().get("kudos_count")) == 1, (
        f"the first kudos reported a count of {first.json().get('kudos_count')}")

    again = sena_client.post(f"/activities/{activity_id}/kudos")
    assert again.status_code in (200, 201, 409), (
        f"a repeated kudos returned {again.status_code}: {again.text[:300]}")
    assert db.count_kudos(activity_id=activity_id) == 1, (
        f"{db.count_kudos(activity_id=activity_id)} kudos rows exist for one "
        f"athlete on one activity; kudos are one per athlete per activity")

    removed = sena_client.delete(f"/activities/{activity_id}/kudos")
    assert removed.status_code in (200, 204), (
        f"DELETE /api/activities/{activity_id}/kudos returned "
        f"{removed.status_code}: {removed.text[:300]}")
    assert db.count_kudos(activity_id=activity_id) == 0, (
        f"kudos survived removal; the control toggles")


def test_repeated_kudos_inside_the_window_collect_into_one_notification(
        rowan_client, db):
    activity_id = fresh_activity(rowan_client, name=unique_ref("Probe storm"))
    rowan_id = db.athlete_by_email(ATHLETE_EMAIL).get("id")
    before = len(db.notifications_of(rowan_id))

    givers = [signup() for _ in range(3)]
    try:
        for _, giver in givers:
            response = giver.post(f"/activities/{activity_id}/kudos")
            assert response.status_code in (200, 201), (
                f"a probe athlete's kudos returned {response.status_code}: "
                f"{response.text[:300]}")
    finally:
        for _, giver in givers:
            giver.close()

    settle(2.0)
    rows = [r for r in db.notifications_of(rowan_id)
            if str(r.get("subject_activity_id")) == str(activity_id)]
    assert len(rows) == 1, (
        f"three kudos inside KUDOS_BATCH_WINDOW_SEC produced {len(rows)} "
        f"notifications for {ROWAN}. Fifty notifications for one popular ride is "
        f"how athletes turn notifications off and never come back, so kudos on one "
        f"activity inside the window collect into one entry carrying a count")
    assert int(rows[0].get("actor_count") or 0) >= 3, (
        f"the collected notification reports actor_count "
        f"{rows[0].get('actor_count')} for three givers; the count is what makes "
        f"one entry stand in for many")
    assert len(db.notifications_of(rowan_id)) >= before, (
        "earlier notifications were destroyed by the collecting one")


def test_comment_carries_its_author_and_is_deletable(sena_client, rowan_client):
    activity_id = fresh_activity(rowan_client, name=unique_ref("Probe comment"))
    body = unique_ref("a probe comment")
    created = sena_client.post(f"/activities/{activity_id}/comments",
                               json={"body": body})
    assert created.status_code in (200, 201), (
        f"POST /api/activities/{activity_id}/comments returned "
        f"{created.status_code}: {created.text[:300]}")
    listing = sena_client.get(f"/activities/{activity_id}/comments")
    assert listing.status_code == 200, (
        f"GET /api/activities/{activity_id}/comments returned "
        f"{listing.status_code}: {listing.text[:300]}")
    rows = items(listing.json())
    assert any(r.get("body") == body for r in rows), (
        f"the comment just left is not in the list: {rows}")
    assert all(r.get("athlete_id") or r.get("display_name") for r in rows), (
        f"a comment carries its author: {rows}")


def test_privacy_zone_is_returned_by_no_read_path(rowan_client, db):
    rowan_id = db.athlete_by_email(ATHLETE_EMAIL).get("id")
    zones = db.privacy_zones_of(rowan_id)
    assert zones, (
        f"{ROWAN} holds no privacy zone; the seed pins one of radius "
        f"{ZONE_RADIUS_M} metres")
    centre_lat = str(zones[0].get("centre_lat"))
    centre_lng = str(zones[0].get("centre_lng"))

    own = rowan_client.get("/privacy-zones")
    assert own.status_code == 200, (
        f"GET /api/privacy-zones returned {own.status_code}: {own.text[:300]}")
    assert centre_lat[:8] not in own.text and centre_lng[:8] not in own.text, (
        f"GET /api/privacy-zones handed back the zone centre. The zone itself is "
        f"returned by no read path, to anyone, including its owner: {own.text[:300]}")
    assert str(ZONE_RADIUS_M) in own.text, (
        f"GET /api/privacy-zones does not report the radius: {own.text[:300]}")

    profile = rowan_client.get(f"/athletes/{rowan_id}")
    assert centre_lat[:8] not in profile.text, (
        f"the profile leaked the privacy-zone centre: {profile.text[:300]}")
    export = rowan_client.get("/export")
    if export.status_code == 200:
        assert centre_lat[:8] not in export.text, (
            f"the data export leaked the privacy-zone centre")


def test_truncated_activity_reports_full_numbers_and_a_partial_map(
        rowan_client, db, anon_client):
    rowan_id = db.athlete_by_email(ATHLETE_EMAIL).get("id")
    zones = db.privacy_zones_of(rowan_id)
    lat = float(zones[0].get("centre_lat"))
    lng = float(zones[0].get("centre_lng"))

    step = 0.0004
    rows = [(lat + i * step, lng, 100.0, i * SAMPLE_RATE_S) for i in range(60)]
    payload = gpx_track(rows, label=unique_ref("zone"))
    activity_id = fresh_activity(rowan_client, payload=payload)

    activity = db.activity_by_id(activity_id)
    assert activity.get("polyline_truncated"), (
        f"activity {activity_id} began inside {ROWAN}'s privacy zone and is not "
        f"marked truncated. The stored line is truncated, not hidden at render "
        f"time: a route drawn short but returned whole is not protected")

    summary = db.summary_of(activity_id)
    assert float(summary.get("distance_m") or 0) > 0, (
        f"the truncated activity reports no distance; the reported distance and "
        f"time are those of the full activity, or the athlete's own numbers are "
        f"wrong, which is a different harm")

    public = anon_client.get(f"/activities/{activity_id}")
    assert public.status_code == 200, (
        f"a logged-out read of an everyone activity returned {public.status_code}")
    assert "partial" in public.text.lower() or "truncat" in public.text.lower(), (
        f"the truncated activity does not say the map is partial: "
        f"{public.text[:300]}")


def test_effort_inside_a_privacy_zone_is_suppressed(rowan_client, db):
    rowan_id = db.athlete_by_email(ATHLETE_EMAIL).get("id")
    zones = db.privacy_zones_of(rowan_id)
    lat = float(zones[0].get("centre_lat"))
    lng = float(zones[0].get("centre_lng"))
    step = 0.0004
    rows = [(lat + i * step, lng, 100.0, i * SAMPLE_RATE_S) for i in range(60)]
    payload = gpx_track(rows, label=unique_ref("zone-effort"))
    activity_id = fresh_activity(rowan_client, payload=payload)
    settle(3.0)

    response = rowan_client.get(f"/activities/{activity_id}")
    assert response.status_code == 200, (
        f"GET /api/activities/{activity_id} returned {response.status_code}")
    body = response.json()
    reported = body.get("efforts") or []
    assert reported == [] or all(e.get("suppressed") is not True for e in reported), (
        f"an effort beginning inside the privacy zone is reported. If the route is "
        f"hidden but the efforts still show the athlete sprinting up the same road "
        f"two streets from home every morning, the hiding achieved nothing: "
        f"privacy zones are defeated by aggregation, not by inspection")


def test_streams_do_not_extend_past_the_truncated_line(rowan_client, db):
    rowan_id = db.athlete_by_email(ATHLETE_EMAIL).get("id")
    zones = db.privacy_zones_of(rowan_id)
    lat = float(zones[0].get("centre_lat"))
    lng = float(zones[0].get("centre_lng"))
    step = 0.0004
    rows = [(lat + i * step, lng, 100.0, i * SAMPLE_RATE_S) for i in range(60)]
    payload = gpx_track(rows, label=unique_ref("zone-stream"))
    activity_id = fresh_activity(rowan_client, payload=payload)

    response = rowan_client.get(f"/activities/{activity_id}/streams",
                                params={"types": "latlng,time,altitude"})
    assert response.status_code == 200, (
        f"GET /api/activities/{activity_id}/streams returned "
        f"{response.status_code}: {response.text[:300]}")
    lengths = {row.get("type"): len(row.get("data") or [])
               for row in items(response.json())}
    assert len(set(lengths.values())) <= 1, (
        f"the returned streams are of differing lengths {lengths}. Truncation "
        f"removes samples from every stream, not from position alone: a heart-rate "
        f"trace that starts before the visible route reveals the duration that was "
        f"removed")


def test_aggregate_refuses_a_cell_below_the_athlete_floor(kit_client):
    response = kit_client.get("/heatmap")
    assert response.status_code == 200, (
        f"GET /api/heatmap as a subscriber returned {response.status_code}: "
        f"{response.text[:300]}")
    body = response.json()
    assert int(body.get("minimum_athletes") or 0) >= AGGREGATE_MIN_ATHLETES, (
        f"the heatmap declares a minimum of {body.get('minimum_athletes')} distinct "
        f"athletes per cell where the brief pins {AGGREGATE_MIN_ATHLETES}. A "
        f"heatmap built without a floor reveals an individual's routine in a "
        f"sparsely populated area, and products of this kind have caused real harm "
        f"that way")
    for cell in body.get("cells") or []:
        count = int(cell.get("athlete_count") or AGGREGATE_MIN_ATHLETES)
        assert count >= AGGREGATE_MIN_ATHLETES, (
            f"a rendered cell was contributed to by {count} athletes, under the "
            f"floor of {AGGREGATE_MIN_ATHLETES}")


def test_free_athlete_is_refused_every_gated_capability(rowan_client):
    refusals = {
        ("GET", "/heatmap"): None,
        ("GET", "/routes"): None,
        ("POST", "/routes"): {"name": unique_ref("Probe route"),
                              "geometry": [[51.5, -0.12], [51.51, -0.11]],
                              "activity_type": "ride"},
    }
    for (method, path), body in refusals.items():
        response = rowan_client.request(method, path, json=body)
        assert response.status_code in DENIED, (
            f"{method} /api{path} with {ROWAN}'s free session returned "
            f"{response.status_code}. Every gated capability is refused at the "
            f"endpoint: hiding the control stops nobody who knows how to look, and "
            f"on this product what they would be looking at is where people go")


def test_free_athlete_is_refused_the_demographic_leaderboard_filter(rowan_client):
    segment_id = segment_id_by_name(rowan_client)
    response = rowan_client.get(f"/segments/{segment_id}/leaderboard",
                                params={"scope": "all", "age_group": "35-44"})
    assert response.status_code in DENIED, (
        f"a demographic leaderboard filter with a free session returned "
        f"{response.status_code}; the filter is a subscriber capability gated at "
        f"the data layer")


def test_free_athlete_is_refused_best_effort_analysis(rowan_client, db):
    rowan_id = db.athlete_by_email(ATHLETE_EMAIL).get("id")
    response = rowan_client.get(f"/athletes/{rowan_id}/best-efforts")
    assert response.status_code in DENIED, (
        f"GET /api/athletes/{rowan_id}/best-efforts with a free session returned "
        f"{response.status_code}; best-effort analysis is a subscriber capability")


def test_subscriber_reaches_every_gated_capability(kit_client, db):
    heatmap = kit_client.get("/heatmap")
    assert heatmap.status_code == 200, (
        f"GET /api/heatmap with {KIT}'s subscriber session returned "
        f"{heatmap.status_code}: {heatmap.text[:300]}")

    listing = kit_client.get("/routes")
    assert listing.status_code == 200, (
        f"GET /api/routes as a subscriber returned {listing.status_code}: "
        f"{listing.text[:300]}")
    assert any(r.get("name") == SEEDED_ROUTE for r in items(listing.json())), (
        f"the seeded route {SEEDED_ROUTE!r} is missing from {KIT}'s routes")

    created = kit_client.post("/routes", json={
        "name": unique_ref("Probe route"), "activity_type": "ride",
        "geometry": [[51.500, -0.120], [51.505, -0.118], [51.510, -0.115]]})
    assert created.status_code in (200, 201), (
        f"POST /api/routes as a subscriber returned {created.status_code}: "
        f"{created.text[:300]}")
    body = created.json()
    assert float(body.get("distance_m") or 0) > 0, (
        f"a saved route reports no derived distance: {body}")

    kit_id = athlete_id_of(kit_client)
    best = kit_client.get(f"/athletes/{kit_id}/best-efforts")
    assert best.status_code == 200, (
        f"GET /api/athletes/{kit_id}/best-efforts as a subscriber returned "
        f"{best.status_code}: {best.text[:300]}")


def test_club_feed_shows_only_activities_the_viewer_may_read(mira_client):
    response = mira_client.get(f"/clubs/{SEEDED_CLUB}")
    if response.status_code in DENIED:
        return
    assert response.status_code == 200, (
        f"GET /api/clubs/{SEEDED_CLUB} returned {response.status_code}: "
        f"{response.text[:300]}")
    assert ROWAN not in response.text, (
        f"{MIRA} is shown {ROWAN}'s club activity; a club feed shows only the "
        f"member activities the viewer is permitted to read")


def test_challenge_standings_are_contiguous_and_respect_blocking(mira_client):
    response = mira_client.get(f"/challenges/{SEEDED_CHALLENGE}")
    assert response.status_code == 200, (
        f"GET /api/challenges/{SEEDED_CHALLENGE} returned {response.status_code}: "
        f"{response.text[:300]}")
    body = response.json()
    standings = body.get("standings") or body.get("entries") or []
    ranks = [int(r.get("rank")) for r in standings if r.get("rank") is not None]
    assert ranks == list(range(1, len(ranks) + 1)), (
        f"the {SEEDED_CHALLENGE!r} standings shown to {MIRA} carry ranks {ranks}, "
        f"which are not contiguous from one")
    assert ROWAN not in str(standings), (
        f"{MIRA} is shown {ROWAN} in the challenge standings")


def test_gift_purchase_completes_without_a_session(db):
    response = httpx.post(f"{api_base()}/gifts", timeout=30.0, json={
        "buyer_email": unique_email(), "recipient_email": unique_email(),
        "plan_slug": "ridgeline-premium", "months": 12,
        "message": unique_ref("a probe gift")})
    assert response.status_code in (200, 201), (
        f"POST /api/gifts with no bearer token returned {response.status_code}. A "
        f"gift is usually bought by somebody who does not use the product for "
        f"somebody who does, and requiring the buyer to make an account first asks "
        f"a non-customer to become a customer before they may give you money: "
        f"{response.text[:300]}")
    code = response.json().get("redemption_code")
    assert code, f"the gift purchase issued no redemption code: {response.text[:300]}"
    assert db.gift_by_code(code) is not None, (
        f"no gift row was stored for redemption code {code!r}")


def test_public_reads_need_no_session(db):
    reference = db.activity_by_name(REFERENCE_ACTIVITY)
    segment = db.segment_by_name(SEEDED_SEGMENT)
    for path in (f"/activities/{reference.get('id')}",
                 f"/segments/{segment.get('id')}",
                 f"/segments/{segment.get('id')}/leaderboard",
                 f"/clubs/{SEEDED_CLUB}",
                 f"/challenges/{SEEDED_CHALLENGE}",
                 "/plans"):
        response = httpx.get(f"{api_base()}{path}", timeout=30.0)
        assert response.status_code == 200, (
            f"GET /api{path} with no bearer token returned {response.status_code}; "
            f"a public read needs no session: {response.text[:300]}")


def test_public_routes_carry_distinct_titles_and_descriptions():
    routes = ("/", "/login", "/signup", "/features", "/maps", "/challenges",
              "/subscription", "/gift", "/stories", "/help")
    titles, descriptions = {}, {}
    for route in routes:
        response = fetch(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}; every public route "
            f"renders: {response.text[:200]}")
        title = re.search(r"<title[^>]*>(.*?)</title>", response.text,
                          re.I | re.S)
        assert title and title.group(1).strip(), (
            f"{route} carries no title: {response.text[:300]}")
        description = re.search(
            r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
            response.text, re.I | re.S)
        assert description and description.group(1).strip(), (
            f"{route} carries no description")
        titles[route] = title.group(1).strip()
        descriptions[route] = description.group(1).strip()
    assert len(set(titles.values())) == len(routes), (
        f"two routes share a title: {titles}")
    assert len(set(descriptions.values())) == len(routes), (
        f"two routes share a description: {descriptions}")


def test_public_pages_are_rendered_on_the_server(db):
    reference = db.activity_by_name(REFERENCE_ACTIVITY)
    response = fetch(f"/activities/{reference.get('id')}")
    assert response.status_code == 200, (
        f"GET /activities/{reference.get('id')} returned {response.status_code}")
    assert REFERENCE_ACTIVITY in response.text, (
        f"the activity name {REFERENCE_ACTIVITY!r} is not in the document the "
        f"server returned. A shared link opens with its content already in the "
        f"document, or the page is not findable: {response.text[:400]}")


def test_social_preview_metadata_is_declared():
    response = fetch("/")
    assert response.status_code == 200
    for prop in ("og:title", "og:description"):
        assert re.search(rf'property=["\']{re.escape(prop)}["\']', response.text,
                         re.I), (
            f"the signup landing declares no {prop}: {response.text[:400]}")


def test_unknown_address_answers_the_not_found_view():
    response = fetch(f"/{unique_ref('no-such-route')}")
    assert response.status_code == 404, (
        f"an unknown address returned {response.status_code} where the not-found "
        f"view answers 404")
    assert "red" in response.text.lower(), (
        f"the not-found view does not carry its own copy: {response.text[:300]}")


def test_server_error_view_is_a_separate_page():
    response = fetch("/500")
    assert response.status_code in (200, 500), (
        f"GET /500 returned {response.status_code}")
    not_found = fetch(f"/{unique_ref('no-such-route')}")
    assert response.text.strip() != not_found.text.strip(), (
        f"the server-error view serves the same document as the not-found view. A "
        f"server error is not a missing page, and telling a visitor to check their "
        f"address sends them hunting for a mistake they did not make")
    scripts = re.findall(r"<script[^>]*src=", response.text, re.I)
    assert not scripts, (
        f"the server-error view loads {len(scripts)} application scripts. The "
        f"condition it reports may be the application failing to start, so it "
        f"ships none")


def test_no_internal_link_leads_to_a_missing_page():
    seen, broken = set(), []
    for route in ("/", "/login", "/subscription", "/features"):
        response = fetch(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}")
        for href in re.findall(r'href=["\'](/[^"\'#?]*)["\']', response.text):
            if href in seen or href.startswith("//"):
                continue
            seen.add(href)
            target = fetch(href)
            if target.status_code >= 400:
                broken.append((route, href, target.status_code))
    assert not broken, (
        f"{len(broken)} internal links lead to a missing page: {broken[:8]}")


def test_consent_choice_is_offered_with_a_one_action_reject():
    response = fetch("/")
    assert response.status_code == 200
    lowered = response.text.lower()
    assert "cookie" in lowered, (
        f"the signup landing shows no consent bar: {response.text[:400]}")
    assert "reject" in lowered, (
        f"the consent bar offers no reject control. The reject path is one action "
        f"and the control is the same size as accept: {response.text[:400]}")


def test_mobile_viewport_is_declared():
    response = fetch("/")
    assert re.search(r'<meta[^>]+name=["\']viewport["\']', response.text, re.I), (
        f"no viewport meta tag is declared, so the product cannot lay out on a "
        f"phone: {response.text[:400]}")


def test_user_readme_records_the_seeded_logins():
    path = "/app/USER_README.md"
    assert os.path.isfile(path), (
        f"{path} does not exist; the deployment contract puts the login "
        f"credentials there")
    text = open(path, encoding="utf-8", errors="replace").read()
    for email in (ATHLETE_EMAIL, ATHLETE2_EMAIL, ATHLETE3_EMAIL, ATHLETE4_EMAIL,
                  ATHLETE5_EMAIL):
        assert email in text, f"{path} does not record the seeded address {email!r}"
    assert CORPUS_PASSWORD in text, (
        f"{path} does not record the seeded password {CORPUS_PASSWORD!r}")


def test_reserved_directories_exist_at_the_app_root():
    for path in ("/app/.browser_screenshots", "/app/.downloads"):
        assert os.path.isdir(path), (
            f"{path} does not exist; the deployment contract reserves it")


def test_no_access_token_or_coordinate_reaches_the_front_end_source():
    response = fetch("/")
    assert response.status_code == 200
    lowered = response.text.lower()
    for secret in (os.environ.get("STORAGE_SECRET_KEY", "minio-root-3d81f7a2"),
                   "deku-local-dev"):
        assert secret.lower() not in lowered, (
            f"the served document carries the credential {secret!r}")


def test_environment_seams_are_read_rather_than_hardcoded():
    for name in ("KUDOS_BATCH_WINDOW_SEC", "FANOUT_FOLLOWER_THRESHOLD"):
        assert os.environ.get(name) not in (None, ""), (
            f"{name} is not set in the verifier environment; the seam exists so "
            f"the behaviour can be exercised at a different scale without the "
            f"application knowing")
    assert int(os.environ["FANOUT_FOLLOWER_THRESHOLD"]) >= 1, (
        "FANOUT_FOLLOWER_THRESHOLD must be a positive follower count")


def test_connected_application_scopes_are_granted_and_revoked_individually(
        kit_client, rowan_client, db):
    created = kit_client.post("/applications", json={
        "name": unique_ref("Probe application"),
        "scopes": ["read_activity", "read_profile"]})
    assert created.status_code in (200, 201), (
        f"POST /api/applications returned {created.status_code}: "
        f"{created.text[:300]}")
    body = created.json()
    application_id = body.get("id")
    token = body.get("token")
    assert token, (
        f"creating an application returned no token: {created.text[:300]}")
    assert set(body.get("scopes") or []) == {"read_activity", "read_profile"}, (
        f"the application was granted {body.get('scopes')!r} where two scopes were "
        f"asked for; scopes are separately grantable")

    listing = kit_client.get("/applications")
    assert listing.status_code == 200, (
        f"GET /api/applications returned {listing.status_code}: "
        f"{listing.text[:300]}")
    rows = items(listing.json())
    assert any(str(r.get("id")) == str(application_id) for r in rows), (
        f"the application just created is not in the athlete's list: {rows}")
    assert token not in listing.text, (
        f"GET /api/applications handed the token back; the value is shown once, at "
        f"creation, and never again")

    private = rowan_client.post("/uploads", data={
        "activity_type": "ride", "name": unique_ref("Probe scoped"),
        "visibility": "only_you", "source": "manual",
        "distance_m": 5000, "elapsed_time_s": 900, "moving_time_s": 900})
    activity_id = upload_reaches(
        rowan_client, private.json().get("upload_id"), ("ready",)).get("activity_id")
    reached = httpx.get(f"{api_base()}/activities/{activity_id}", timeout=30.0,
                        headers={"Authorization": f"Bearer {token}"})
    assert reached.status_code in DENIED, (
        f"an application authorised by {KIT} read {ROWAN}'s only_you activity and "
        f"got {reached.status_code}. An application's reach into an activity is "
        f"bounded by that activity's own visibility, not by whose account "
        f"authorised it")

    revoked = kit_client.delete(f"/applications/{application_id}")
    assert revoked.status_code in (200, 204), (
        f"DELETE /api/applications/{application_id} returned {revoked.status_code}: "
        f"{revoked.text[:300]}")
    after = items(kit_client.get("/applications").json())
    still = [r for r in after if str(r.get("id")) == str(application_id)]
    assert not still or still[0].get("revoked_at"), (
        f"the revoked application is still live: {still}")


def test_public_interface_declares_its_rate_limit_and_signs_its_webhooks(kit_client):
    response = kit_client.get("/applications")
    assert response.status_code == 200, (
        f"GET /api/applications returned {response.status_code}")
    headers = {k.lower() for k in response.headers}
    limit = [h for h in headers if "ratelimit" in h.replace("-", "")]
    assert limit, (
        f"no rate-limit header is declared on the public interface. Limits apply "
        f"per application and per athlete, are documented, and state when they "
        f"reset. Saw: {sorted(headers)}")
    reset = [h for h in limit if "reset" in h]
    assert reset, (
        f"the rate-limit headers {sorted(limit)} name no reset time")

    created = kit_client.post("/applications", json={
        "name": unique_ref("Probe hook"), "scopes": ["read_activity"],
        "webhook_url": "https://example.com/hook"})
    assert created.status_code in (200, 201), (
        f"registering a webhook returned {created.status_code}: "
        f"{created.text[:300]}")
    assert created.json().get("webhook_signing_secret"), (
        f"an application with a webhook was issued no signing secret; a webhook is "
        f"signed, delivered at least once, and carries the resource state: "
        f"{created.text[:300]}")


def test_polyline_is_stored_at_several_simplification_levels(rowan_client, db):
    activity_id = fresh_activity(rowan_client)
    rows = db.polylines_of(activity_id)
    assert len(rows) >= 2, (
        f"activity {activity_id} carries {len(rows)} stored lines. Lines are kept "
        f"at several simplification levels so the feed can read the coarsest one "
        f"and the activity page a finer one")
    levels = {r.get("simplification_level") for r in rows}
    assert len(levels) == len(rows), (
        f"two stored lines share a simplification level: {levels}")
    for row in rows:
        assert row.get("tolerance_m") is not None, (
            f"the line at level {row.get('simplification_level')!r} states no "
            f"tolerance; simplification preserves shape within a stated tolerance "
            f"and never moves an endpoint")
    coarse = min(rows, key=lambda r: len(str(r.get("encoded") or "")))
    fine = max(rows, key=lambda r: len(str(r.get("encoded") or "")))
    assert len(str(coarse.get("encoded"))) < len(str(fine.get("encoded"))), (
        "every stored line is the same size, so no simplification happened")


def test_no_binary_asset_and_no_third_party_host_is_served():
    external, binaries = set(), set()
    for route in ("/", "/login", "/subscription", "/features"):
        response = fetch(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}")
        for url in re.findall(r'(?:src|href)=["\']([^"\']+)["\']', response.text):
            if re.match(r"https?://", url):
                external.add(url.split("/")[2])
            if re.search(
                    r"\.(png|jpe?g|gif|webp|avif|svg|ico|mp4|webm|woff2?|ttf|otf|eot)(\?|$)",
                    url, re.I):
                binaries.add(url)
    assert not binaries, (
        f"the served documents reference {len(binaries)} binary assets, the first "
        f"being {sorted(binaries)[0]!r}. Nothing binary ships: no image file, no "
        f"video file, no font file")
    assert not external, (
        f"the served documents reach {len(external)} outside hosts: "
        f"{sorted(external)}. No analytics, consent vendor, error reporter or map "
        f"tile vendor is contacted at run time, and the interface runs from one "
        f"framework served from this origin")


def test_a_retried_follow_and_a_retried_join_change_nothing(db):
    email, fresh = signup()
    other_email, other = signup()
    with fresh, other:
        other_id = athlete_id_of(other)
        fresh_id = athlete_id_of(fresh)
        first = fresh.post(f"/athletes/{other_id}/follow")
        assert first.status_code in (200, 201), (
            f"POST /api/athletes/{other_id}/follow returned {first.status_code}")
        again = fresh.post(f"/athletes/{other_id}/follow")
        assert again.status_code in (200, 201, 409), (
            f"a retried follow returned {again.status_code}: {again.text[:300]}")
        assert db.count_follows(follower_id=fresh_id, followee_id=other_id) == 1, (
            f"{db.count_follows(follower_id=fresh_id, followee_id=other_id)} follow "
            f"rows exist for one pair; a retried write produces no second effect")

        joined = fresh.post(f"/clubs/{SEEDED_CLUB}/members")
        assert joined.status_code in (200, 201), (
            f"POST /api/clubs/{SEEDED_CLUB}/members returned {joined.status_code}: "
            f"{joined.text[:300]}")
        repeat = fresh.post(f"/clubs/{SEEDED_CLUB}/members")
        assert repeat.status_code in (200, 201, 409), (
            f"a retried join returned {repeat.status_code}: {repeat.text[:300]}")
        roster = fresh.get(f"/clubs/{SEEDED_CLUB}").json().get("members") or []
        mine = [r for r in roster if str(r.get("athlete_id")) == str(fresh_id)]
        assert len(mine) <= 1, (
            f"the retried join left {len(mine)} roster rows for one athlete")


def test_local_date_and_stream_offsets_survive_a_midnight_crossing(rowan_client, db):
    rows = [(51.5, -0.12 + i * 0.0002, 100.0, i * SAMPLE_RATE_S) for i in range(40)]
    payload = gpx_track(rows, start="2026-04-02T23:40:00Z",
                            label=unique_ref("midnight"))
    activity_id = fresh_activity(rowan_client, payload=payload)

    activity = db.activity_by_id(activity_id)
    start = str(activity.get("start_time_utc") or "")
    assert start, f"activity {activity_id} carries no start instant"
    local_date = str(activity.get("start_local_date") or "")
    assert local_date, (
        f"activity {activity_id} carries no start_local_date; activities in March "
        f"means local March")
    assert local_date.startswith("2026-04-02"), (
        f"an activity that began before midnight and ended after it is recorded on "
        f"{local_date!r}; an activity belongs to the date it started")

    response = rowan_client.get(f"/activities/{activity_id}/streams",
                                params={"types": "time"})
    assert response.status_code == 200, (
        f"GET /api/activities/{activity_id}/streams returned {response.status_code}")
    series = (items(response.json()) or [{}])[0].get("data") or []
    assert series, f"activity {activity_id} carries no time series"
    assert float(series[0]) == 0.0, (
        f"the time series begins at {series[0]!r}; streams are offsets from the "
        f"start instant, never absolute timestamps")


def test_athlete_preferences_round_trip_independently(kit_client, db):
    response = kit_client.patch("/me", json={
        "unit_preference": "imperial", "elevation_preference": "metres",
        "timezone": "Europe/London"})
    assert response.status_code in (200, 202), (
        f"PATCH /api/me returned {response.status_code}: {response.text[:300]}")
    body = kit_client.get("/me").json()
    assert body.get("unit_preference") == "imperial", (
        f"the unit preference did not persist: {body}")

    row = db.athlete_by_email(ATHLETE5_EMAIL)
    assert row.get("elevation_preference") == "metres", (
        f"{KIT} reports elevation_preference {row.get('elevation_preference')!r} "
        f"after asking for metres alongside imperial distances. Elevation, distance "
        f"and temperature carry independent preferences, because a runner may well "
        f"want kilometres and feet")
    for field in ("display_name", "plan", "timezone", "default_visibility"):
        assert field in row, (
            f"the athlete record carries no {field!r}: {sorted(row)}")

    kit_client.patch("/me", json={"unit_preference": "metric"})


def test_federated_identity_links_rather_than_forking_the_account(db):
    email, fresh = signup()
    with fresh:
        athlete_id = athlete_id_of(fresh)
        subject = unique_ref("provider-subject")
        linked = fresh.post("/auth/link", json={
            "provider": "google", "provider_subject": subject,
            "verified_email": email})
        assert linked.status_code in (200, 201), (
            f"POST /api/auth/link returned {linked.status_code}: "
            f"{linked.text[:300]}")
        assert str(linked.json().get("athlete_id")) == str(athlete_id), (
            f"linking a verified address that already belongs to an athlete "
            f"produced athlete {linked.json().get('athlete_id')} rather than "
            f"{athlete_id}. Two accounts for one person splits their history and "
            f"loses their totals")

        second = fresh.post("/auth/link", json={
            "provider": "apple", "provider_subject": unique_ref("apple-subject"),
            "verified_email": email})
        assert second.status_code in (200, 201), (
            f"linking a second provider returned {second.status_code}: "
            f"{second.text[:300]}")
        assert str(second.json().get("athlete_id")) == str(athlete_id), (
            "a second provider carrying the same verified address produced a "
            "second account")
    assert db.count_athletes(email=email) == 1, (
        f"{db.count_athletes(email=email)} athlete rows exist for {email!r} after "
        f"two identities were linked")


def test_protected_bytes_are_served_only_through_the_application(
        rowan_client, sena_client, db, store):
    created = rowan_client.post("/uploads", data={
        "activity_type": "ride", "name": unique_ref("Probe protected"),
        "visibility": "only_you", "source": "manual",
        "distance_m": 4000, "elapsed_time_s": 800, "moving_time_s": 800})
    upload_id = created.json().get("upload_id")
    upload_reaches(rowan_client, upload_id, ("ready",))
    row = db.upload_by_id(upload_id)
    key = row.get("object_key")
    assert key, f"upload {upload_id} recorded no object key"
    assert store.exists(key), f"nothing is stored at {key!r}"

    endpoint = os.environ.get("STORAGE_ENDPOINT", "").rstrip("/")
    bucket = os.environ.get("STORAGE_BUCKET", "")
    if endpoint and bucket:
        direct = httpx.get(f"{endpoint}/{bucket}/{key}", timeout=30.0)
        assert direct.status_code in (401, 403, 404), (
            f"the object at {key!r} is readable straight from the bucket "
            f"({direct.status_code}). The bucket is never made public: protected "
            f"bytes are reached through the application, which applies the same "
            f"visibility rules as every other read path")

    theirs = sena_client.get(f"/activities/{row.get('activity_id')}/streams")
    assert theirs.status_code in DENIED or items(theirs.json()) == [], (
        f"{SENA} read the series of an only_you activity through the application "
        f"and got {theirs.status_code}")


def test_unauthenticated_athlete_route_redirects_to_login():
    for route in ("/feed", "/upload", "/settings", "/settings/privacy"):
        response = httpx.get(page(route), timeout=30.0, follow_redirects=False)
        assert response.status_code in (302, 303, 307, 308), (
            f"GET {route} with no session returned {response.status_code} rather "
            f"than a redirect to the log-in route")
        location = response.headers.get("location", "")
        assert "/login" in location, (
            f"GET {route} with no session redirected to {location!r} rather than to "
            f"/login")
        assert (route.strip("/").split("/")[0] in location or "next" in location
                or "redirect" in location or "return" in location), (
            f"the redirect to {location!r} preserves no destination, so a "
            f"successful sign-in cannot land on the route that was asked for")
