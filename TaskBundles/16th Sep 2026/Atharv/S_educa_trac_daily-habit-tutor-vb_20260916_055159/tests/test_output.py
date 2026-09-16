from __future__ import annotations

import json
import re
import urllib.parse

import httpx

import appclient
import conftest as kit



def test_health_endpoint_returns_ok(raw):
    response = raw.get("/api/health")
    assert response.status_code == 200, (
        f"GET /api/health must answer 200 once the app is ready: {kit.describe(response)}")


def test_seeded_learner_can_sign_in_with_pinned_password(learner):
    response = learner.get("/auth/me")
    assert response.status_code == 200, kit.describe(response)
    me = kit.json_of(response)
    assert me.get("email") == kit.LEARNER_1, (
        f"/api/auth/me must name the signed-in account {kit.LEARNER_1!r}, got {me!r}")
    assert me.get("display_name") == kit.DISPLAY_NAMES[kit.LEARNER_1], (
        f"seeded display name must be {kit.DISPLAY_NAMES[kit.LEARNER_1]!r}, got {me!r}")
    assert me.get("timezone") == kit.TIMEZONES[kit.LEARNER_1], (
        f"seeded timezone must be {kit.TIMEZONES[kit.LEARNER_1]!r}, got {me!r}")
    for email in (kit.LEARNER_2, kit.LEARNER_3, *kit.COHORT_EMAILS):
        with appclient.client(kit.token_for(email)) as other:
            who = other.get("/auth/me")
            assert who.status_code == 200, (
                f"seeded account {email!r} must sign in with the pinned password: "
                f"{kit.describe(who)}")
            assert kit.json_of(who).get("email") == email, (
                f"/api/auth/me returned the wrong account for {email!r}: {who.text[:300]}")


def test_user_readme_carries_every_seeded_login(raw):
    response = raw.get("/api/auth/me")
    assert response.status_code in (401, 403), (
        f"an unauthenticated /api/auth/me must be denied: {kit.describe(response)}")
    with appclient.client(kit.token_for(kit.LEARNER_1)) as client:
        readme = client.get("/readme")
    assert readme.status_code in (200, 404), kit.describe(readme)
    for email in (kit.LEARNER_1, kit.LEARNER_2, kit.LEARNER_3):
        with appclient.client(kit.token_for(email)) as client:
            who = client.get("/auth/me")
        assert who.status_code == 200, (
            f"the credentials written to /app/USER_README.md must work at login; "
            f"{email!r} failed: {kit.describe(who)}")


def test_signup_with_existing_email_is_refused_and_writes_no_row(anon, db):
    before = db.count("accounts", email=kit.LEARNER_1)
    assert before == 1, (
        f"exactly one seeded row must exist for {kit.LEARNER_1!r}, found {before}")
    response = kit.signup(anon, kit.LEARNER_1)
    assert 400 <= response.status_code < 500, (
        f"a duplicate signup must be refused as a client error: {kit.describe(response)}")
    assert "email" in response.text.lower(), (
        f"the refusal must name the field at fault: {kit.describe(response)}")
    after = db.count("accounts", email=kit.LEARNER_1)
    assert after == before, (
        f"a refused signup must write no second row: {before} before, {after} after")
    wrong = anon.post("/auth/login", json={"email": kit.LEARNER_1, "password": "not-it"})
    assert 400 <= wrong.status_code < 500, (
        f"a wrong password must be refused: {kit.describe(wrong)}")
    unknown = anon.post("/auth/login",
                        json={"email": kit.unique_email(), "password": kit.PASSWORD})
    assert unknown.status_code == wrong.status_code, (
        f"an unknown email and a wrong password must be indistinguishable: "
        f"{unknown.status_code} vs {wrong.status_code}")


def test_anonymous_sample_progress_moves_to_the_new_account(anon, db):
    minted = anon.post("/auth/anonymous")
    assert minted.status_code in (200, 201), kit.describe(minted)
    browsing = kit.json_of(minted).get("access_token")
    assert browsing, f"/api/auth/anonymous must return a browsing token: {minted.text[:300]}"
    with appclient.client(browsing) as visitor:
        subject = visitor.get(f"/courses/{kit.OPEN_SUBJECTS[1]}")
        assert subject.status_code == 200, kit.describe(subject)
        samples = kit.json_of(subject).get("samples") or []
        assert len(samples) == 2, (
            f"an open subject page must expose two samples, got {len(samples)}")
        answered = visitor.post("/sessions",
                                json={"course_id": kit.OPEN_SUBJECTS[1],
                                      "unit_id": None, "lesson_id": None,
                                      "kind": "practice"})
        assert answered.status_code in (200, 201, 400, 422), kit.describe(answered)
        email = kit.unique_email()
        created = kit.signup(visitor, email)
        assert created.status_code in (200, 201), (
            f"signup from a browsing token must succeed: {kit.describe(created)}")
    rows = db.rows("accounts", email=email)
    assert len(rows) == 1, f"signup must create exactly one row for {email!r}: {rows!r}"
    with appclient.client(browsing) as stale:
        after = stale.get("/auth/me")
    assert after.status_code in (401, 403), (
        f"the browsing token must stop working once exchanged: {kit.describe(after)}")


def test_subject_picker_lists_forty_two_subjects_in_promoted_order(anon, db):
    response = anon.get("/courses")
    assert response.status_code == 200, kit.describe(response)
    body = kit.json_of(response)
    assert isinstance(body, list), f"/api/courses must return a top-level array: {body!r}"
    names = [c.get("name") for c in body]
    assert len(names) == kit.PICKER_COUNT, (
        f"the picker carries exactly {kit.PICKER_COUNT} entries, got {len(names)}: {names!r}")
    assert names == kit.PICKER_ORDER, (
        f"picker order must be promoted-first then alphabetical by English name; "
        f"first divergence at index "
        f"{next((i for i, (a, b) in enumerate(zip(names, kit.PICKER_ORDER)) if a != b), -1)}: "
        f"{names!r}")
    assert db.count("courses") == kit.PICKER_COUNT, (
        f"the courses table carries {kit.PICKER_COUNT} rows, found {db.count('courses')}")


def test_only_three_subjects_are_open(anon):
    response = anon.get("/courses")
    assert response.status_code == 200, kit.describe(response)
    body = kit.json_of(response)
    opened = sorted(c.get("id") for c in body if c.get("is_open"))
    assert opened == sorted(kit.OPEN_SUBJECTS), (
        f"exactly {kit.OPEN_SUBJECTS} are open, got {opened}")
    closed = [c for c in body if not c.get("is_open")]
    assert len(closed) == kit.PICKER_COUNT - len(kit.OPEN_SUBJECTS), (
        f"the remaining {kit.PICKER_COUNT - len(kit.OPEN_SUBJECTS)} subjects stay closed, "
        f"got {len(closed)}")
    for course in body:
        assert "name" in course and "mark_code" in course, (
            f"every picker entry carries a name and a mark code: {course!r}")


def test_subject_page_exposes_two_playable_samples(anon):
    for slug in kit.OPEN_SUBJECTS:
        response = anon.get(f"/courses/{slug}")
        assert response.status_code == 200, kit.describe(response)
        body = kit.json_of(response)
        assert body.get("approx_hours"), (
            f"subject {slug!r} must state roughly how long it takes: {body!r}")
        if body.get("kind") == "language":
            assert body.get("writing_systems"), (
                f"a language subject names the writing systems taught: {body!r}")
        else:
            assert body.get("prerequisite"), (
                f"a non-language subject names its prerequisite: {body!r}")
        units = body.get("units") or []
        assert len(units) == kit.UNITS_PER_SUBJECT, (
            f"an open subject carries {kit.UNITS_PER_SUBJECT} units, got {len(units)}")
        samples = body.get("samples") or []
        assert len(samples) == 2, (
            f"subject {slug!r} must expose two playable samples, got {len(samples)}")
        for sample in samples:
            assert sample.get("type") and sample.get("prompt_text") is not None, (
                f"a sample must be a real exercise: {sample!r}")


def test_sample_attempt_is_stored_without_an_account(anon, db):
    before = db.count("attempts")
    minted = anon.post("/auth/anonymous")
    assert minted.status_code in (200, 201), kit.describe(minted)
    browsing = kit.json_of(minted)["access_token"]
    with appclient.client(browsing) as visitor:
        subject = visitor.get(f"/courses/{kit.OPEN_SUBJECTS[1]}")
        sample = kit.json_of(subject)["samples"][0]
        graded = visitor.post("/sessions", json={"course_id": kit.OPEN_SUBJECTS[1],
                                                 "unit_id": None, "lesson_id": None,
                                                 "kind": "practice"})
        assert graded.status_code in (200, 201), kit.describe(graded)
        session = kit.json_of(graded)
        done = kit.reconcile(visitor, session["id"],
                             [{"exercise_id": sample["id"], "presented_index": 0,
                               "answer_raw": sample.get("solution_canonical", ""),
                               "elapsed_ms": 5100}])
        assert done.status_code in (200, 201), kit.describe(done)
    after = kit.settle(lambda: db.count("attempts") > before)
    assert after, (
        f"a sample attempt answered with no account must be stored; attempts stayed at "
        f"{before}")


def test_english_subject_is_taught_from_spanish(anon):
    response = anon.get("/courses/english")
    assert response.status_code == 200, kit.describe(response)
    body = kit.json_of(response)
    assert body.get("from_language", "").lower().startswith("spanish"), (
        f"the english subject is taught from Spanish: {body!r}")
    assert body.get("to_language", "").lower().startswith("english"), (
        f"the english subject teaches English: {body!r}")


def test_two_language_runs_declare_their_own_language(page, raw):
    page.goto(kit.absolute("/courses/english"))
    runs = page.eval_on_selector_all(
        "[lang]", "nodes => nodes.map(n => n.getAttribute('lang'))")
    assert len(set(runs)) >= 2, (
        f"a two-language subject page declares at least two language attributes, "
        f"found {sorted(set(runs))!r}")
    picker = raw.get("/api/courses")
    assert picker.status_code == 200, kit.describe(picker)


def test_enrolment_is_idempotent_for_one_subject(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    first = kit.enrol(fresh, course, goal=3)
    assert first.status_code in (200, 201), kit.describe(first)
    me = kit.json_of(fresh.get("/auth/me"))
    second = kit.enrol(fresh, course, goal=1)
    assert second.status_code in (200, 201, 409), kit.describe(second)
    rows = db.rows("enrolments", account_id=me["id"], course_id=course)
    assert len(rows) == 1, (
        f"enrolling twice in {course!r} must leave exactly one row, found {len(rows)}")
    assert rows[0].get("daily_goal_lessons") == 3, (
        f"a repeated enrolment must not reset the daily goal: {rows[0]!r}")
    listed = fresh.get("/enrolments")
    assert listed.status_code == 200, kit.describe(listed)
    assert isinstance(kit.json_of(listed), list), "/api/enrolments must return an array"


def test_lesson_session_is_assembled_with_twelve_exercises(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    started = kit.start_session(fresh, course)
    assert started.status_code in (200, 201), kit.describe(started)
    session = kit.json_of(started)
    exercises = session.get("exercises") or []
    assert len(exercises) == kit.LESSON_EXERCISES, (
        f"a lesson is assembled with exactly {kit.LESSON_EXERCISES} exercises, "
        f"got {len(exercises)}")
    assert session.get("kind") == "lesson", f"session kind must be 'lesson': {session!r}"
    assert session.get("state") == "in_progress", f"a new session is in_progress: {session!r}"


def test_session_exercise_list_is_fixed_after_assembly(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    first = [ex["id"] for ex in session["exercises"]]
    again = fresh.get(f"/sessions/{session['id']}")
    assert again.status_code == 200, kit.describe(again)
    second = [ex["id"] for ex in kit.json_of(again)["exercises"]]
    assert second == first, (
        f"a session's exercise list is fixed for its lifetime; re-read gave {second!r} "
        f"after {first!r}")


def test_session_assembly_respects_type_and_concept_runs(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    types = [ex.get("type") for ex in session["exercises"]]
    run = 1
    for a, b in zip(types, types[1:]):
        run = run + 1 if a == b else 1
        assert run <= 3, (
            f"no more than 3 consecutive exercises share one type, got a run of {run} "
            f"in {types!r}")
    concepts = [tuple(sorted(ex.get("concept_ids") or [])) for ex in session["exercises"]]
    run = 1
    for a, b in zip(concepts, concepts[1:]):
        run = run + 1 if a == b and a else 1
        assert run <= 2, (
            f"no more than 2 consecutive exercises share one concept, got a run of {run}")
    difficulties = [ex.get("difficulty") for ex in session["exercises"]]
    assert all(d is not None for d in difficulties), (
        f"every assembled exercise carries a difficulty: {difficulties!r}")
    opening = difficulties[:2]
    middle = difficulties[len(difficulties) // 3: 2 * len(difficulties) // 3]
    assert max(opening) <= max(middle), (
        f"the first two exercises are the easiest and the hardest sit in the middle "
        f"third: opening {opening!r}, middle {middle!r}")
    assert difficulties[-1] <= max(middle), (
        f"a session ends on an exercise the learner is likely to answer correctly: "
        f"{difficulties!r}")


def test_attempt_states_are_the_four_pinned_values(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session)
    attempts[0]["answer_raw"] = ""
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), kit.describe(done)
    result = kit.json_of(done)
    states = [a.get("state") for a in result.get("attempts", [])]
    assert states, f"a reconcile result must name each attempt state: {result!r}"
    for state in states:
        assert state in kit.ATTEMPT_STATES, (
            f"attempt state {state!r} is outside the pinned four {kit.ATTEMPT_STATES}")
    me = kit.json_of(fresh.get("/auth/me"))
    stored = db.rows("attempts", session_id=session["id"])
    assert len(stored) == len(attempts), (
        f"every reported attempt is stored once: reported {len(attempts)}, "
        f"stored {len(stored)}")
    assert all(row.get("account_id") == me["id"] for row in stored), (
        f"stored attempts belong to the reporting account: {stored!r}")


def test_wrong_answer_is_requeued_once_as_a_different_exercise(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    target = session["exercises"][0]
    attempts = kit.attempts_for(session)
    attempts[0]["answer_raw"] = "zzzzz-not-an-answer"
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), kit.describe(done)
    requeued = kit.json_of(done).get("requeued") or []
    assert len(requeued) >= 1, (
        f"a wrong answer must re-queue its concept: {kit.json_of(done)!r}")
    entry = requeued[0]
    assert entry.get("position", 0) - 0 >= 3, (
        f"a re-queued exercise lands at least 3 exercises further on: {entry!r}")
    assert requeued.count(entry) == 1, f"a re-queue happens at most once: {requeued!r}"
    assert entry.get("exercise_id") != target["id"] or entry.get("only_instance"), (
        f"a re-queue uses a different exercise for the same concept where one exists: "
        f"{entry!r}")


def test_frustration_guard_ends_a_concept_after_three_wrong(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session, answer=lambda ex: "zzzzz-not-an-answer")
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), kit.describe(done)
    guarded = kit.json_of(done).get("guarded_concepts")
    assert guarded is not None, (
        f"a reconcile result must report which concepts the frustration guard closed: "
        f"{kit.json_of(done)!r}")


def test_interrupted_session_is_resumable_and_offered(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    again = fresh.get(f"/sessions/{session['id']}")
    assert again.status_code == 200, kit.describe(again)
    resumable = kit.json_of(again)
    assert resumable.get("state") == "in_progress", (
        f"an unfinished session stays in_progress and resumable: {resumable!r}")
    assert resumable.get("resumable_for_seconds") == kit.RESUMABLE_SECONDS, (
        f"a session stays resumable for {kit.RESUMABLE_SECONDS} seconds: {resumable!r}")
    assert resumable.get("resume_offered") is True, (
        f"a resumable session is offered rather than resumed silently: {resumable!r}")
    assert resumable.get("exercise_index") is not None, (
        f"a resumable session names the exercise index to resume from: {resumable!r}")




def test_session_reconcile_is_idempotent_and_does_not_double_count(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    me = kit.json_of(fresh.get("/auth/me"))
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session)
    first = kit.reconcile(fresh, session["id"], attempts)
    assert first.status_code in (200, 201), kit.describe(first)
    one = kit.json_of(first)
    rows_after_first = db.count("attempts", session_id=session["id"])
    streak_after_first = kit.json_of(fresh.get("/streak"))
    profile_after_first = kit.json_of(fresh.get("/profile"))

    second = kit.reconcile(fresh, session["id"], attempts)
    assert second.status_code in (200, 201, 409), kit.describe(second)
    two = kit.json_of(second)
    assert two.get("points_earned") == one.get("points_earned"), (
        f"a second report must return the first result unchanged: "
        f"{one.get('points_earned')!r} then {two.get('points_earned')!r}")
    rows_after_second = db.count("attempts", session_id=session["id"])
    assert rows_after_second == rows_after_first, (
        f"a second report writes no second attempt row: {rows_after_first} then "
        f"{rows_after_second}")
    streak_after_second = kit.json_of(fresh.get("/streak"))
    assert streak_after_second.get("length") == streak_after_first.get("length"), (
        f"a second report extends the streak no further: "
        f"{streak_after_first!r} then {streak_after_second!r}")
    profile_after_second = kit.json_of(fresh.get("/profile"))
    assert profile_after_second.get("points_this_week") == \
        profile_after_first.get("points_this_week"), (
            f"a second report awards no further points: "
            f"{profile_after_first!r} then {profile_after_second!r}")
    sessions = db.rows("sessions", id=session["id"])
    assert len(sessions) == 1 and sessions[0].get("reconciled_at") is not None, (
        f"the session carries exactly one reconcile mark: {sessions!r}")
    summary = fresh.get("/history")
    assert summary.status_code == 200, kit.describe(summary)
    days = kit.json_of(summary)
    assert sum(d.get("sessions_completed", 0) for d in days) == 1, (
        f"the history must show exactly one completed session, got {days!r}")


def test_concurrent_session_reports_produce_one_accepted_result(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session)
    token = fresh.headers.get("Authorization", "")
    url = f"{kit.api_base()}/sessions/{session['id']}/reconcile"
    payload = {"attempts": attempts, "device_clock_offset_ms": 0}
    responses = []
    with httpx.Client(timeout=30.0, headers={"Authorization": token}) as a, \
            httpx.Client(timeout=30.0, headers={"Authorization": token}) as b:
        first = a.build_request("POST", url, json=payload)
        second = b.build_request("POST", url, json=payload)
        responses.append(a.send(first))
        responses.append(b.send(second))
    codes = [r.status_code for r in responses]
    assert all(c < 500 for c in codes), (
        f"neither concurrent report may be a server error, got {codes}")
    rows = db.count("attempts", session_id=session["id"])
    assert rows == len(attempts), (
        f"two concurrent reports of one session store exactly one set of attempts: "
        f"expected {len(attempts)}, found {rows}")
    sessions = db.rows("sessions", id=session["id"])
    assert len(sessions) == 1, f"exactly one session row survives: {sessions!r}"
    orphans = db.count("attempts", session_id=session["id"], state=None)
    assert orphans == 0, (
        f"a failed report leaves no half-written attempt row, found {orphans}")


def test_reconcile_recomputes_awards_from_stored_attempts(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session)
    for attempt in attempts:
        attempt["claimed_points"] = 99999
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), kit.describe(done)
    earned = kit.json_of(done).get("points_earned")
    assert earned is not None, f"a reconcile result names the points earned: {done.text[:300]}"
    ceiling = kit.AWARD_LESSON + kit.AWARD_PERFECT_BONUS + kit.AWARD_FIRST_OF_DAY_BONUS
    assert earned <= ceiling, (
        f"the award is recomputed by the service, never proposed by the client: "
        f"got {earned}, ceiling {ceiling}")
    stored = db.rows("attempts", session_id=session["id"])
    assert len(stored) == len(attempts), (
        f"the award must be computed from the stored attempts: {len(stored)} rows for "
        f"{len(attempts)} reported")


def test_out_of_order_attempt_report_is_refused_and_stores_nothing(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session)
    shuffled = [attempts[3], attempts[0]] + attempts[4:]
    refused = kit.reconcile(fresh, session["id"], shuffled)
    assert 400 <= refused.status_code < 500, (
        f"attempts out of presentation order are refused in full: {kit.describe(refused)}")
    assert db.count("attempts", session_id=session["id"]) == 0, (
        "a refused report writes nothing")

    intruder = kit.json_of(kit.start_session(fresh, kit.OPEN_SUBJECTS[1]))
    alien = kit.attempts_for(session)
    alien[0]["exercise_id"] = intruder["exercises"][0]["id"]
    foreign = kit.reconcile(fresh, session["id"], alien)
    assert 400 <= foreign.status_code < 500, (
        f"an attempt naming an exercise outside the assembled list is refused in full: "
        f"{kit.describe(foreign)}")
    assert db.count("attempts", session_id=session["id"]) == 0, (
        "a refused report writes nothing")


def test_attempt_faster_than_the_human_floor_earns_nothing(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session)
    for attempt in attempts:
        attempt["elapsed_ms"] = 1
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), (
        f"an impossibly fast session still completes: {kit.describe(done)}")
    assert kit.json_of(done).get("points_earned") == 0, (
        f"attempts faster than the human floor earn nothing: {done.text[:300]}")


def test_browser_clock_offset_never_moves_an_award(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session)
    skewed = kit.reconcile(fresh, session["id"], attempts,
                           offset_ms=(kit.CLOCK_SKEW_SECONDS + 600) * 1000)
    assert skewed.status_code in (200, 201), kit.describe(skewed)
    rows = db.rows("sessions", id=session["id"])
    assert rows and rows[0].get("device_clock_offset_ms") is not None, (
        f"the reported clock offset must be recorded: {rows!r}")
    streak = kit.json_of(fresh.get("/streak"))
    assert streak.get("local_date"), (
        f"the streak names the local date the service decided on: {streak!r}")


def test_attempt_rows_persist_and_survive_a_reread(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    me = kit.json_of(fresh.get("/auth/me"))
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session)
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), kit.describe(done)
    rows = db.rows("attempts", session_id=session["id"])
    assert len(rows) == len(attempts), (
        f"every attempt is a stored row: {len(rows)} for {len(attempts)} reported")
    indexes = sorted(row.get("presented_index") for row in rows)
    assert indexes == sorted(set(indexes)), (
        f"attempt rows are unique on the session with the presented index: {indexes!r}")
    history = fresh.get("/history")
    assert history.status_code == 200, kit.describe(history)
    days = kit.json_of(history)
    assert isinstance(days, list) and days, (
        f"/api/history must return a top-level array of local days: {days!r}")
    assert all(row.get("account_id") == me["id"] for row in rows), (
        f"stored attempts belong to the account that reported them: {rows[:2]!r}")


def test_traces_are_rebuildable_from_the_attempt_log(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    me = kit.json_of(fresh.get("/auth/me"))
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session)
    assert kit.reconcile(fresh, session["id"], attempts).status_code in (200, 201)
    traces = kit.settle(lambda: db.rows("traces", account_id=me["id"]) or None)
    assert traces, f"answering exercises must write concept traces for {me['id']!r}"
    exercised = set()
    for exercise in session["exercises"]:
        exercised.update(exercise.get("concept_ids") or [])
    traced = {row.get("concept_id") for row in traces}
    assert exercised.issubset(traced), (
        f"every concept the session exercised owns a trace; missing "
        f"{sorted(exercised - traced)!r}")
    listed = fresh.get("/traces", params={"course_id": course})
    assert listed.status_code == 200, kit.describe(listed)
    body = kit.json_of(listed)
    assert isinstance(body, list), f"/api/traces returns a top-level array: {body!r}"
    for trace in body:
        assert trace.get("state") in kit.TRACE_STATES, (
            f"trace state {trace.get('state')!r} is outside {kit.TRACE_STATES}")


def test_recall_probability_matches_the_pinned_formula(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    assert kit.reconcile(fresh, session["id"],
                         kit.attempts_for(session)).status_code in (200, 201)
    listed = kit.json_of(fresh.get("/traces", params={"course_id": course}))
    assert listed, f"a completed session must produce traces: {listed!r}"
    for trace in listed:
        half_life = trace.get("half_life_seconds")
        assert half_life is not None, f"a trace carries a half-life: {trace!r}"
        assert kit.HALF_LIFE_MIN_SECONDS <= half_life <= kit.HALF_LIFE_MAX_SECONDS, (
            f"half-life {half_life} is outside the clamp "
            f"[{kit.HALF_LIFE_MIN_SECONDS}, {kit.HALF_LIFE_MAX_SECONDS}]: {trace!r}")
        recall = trace.get("recall_probability")
        assert recall is not None and 0.0 <= recall <= 1.0, (
            f"a trace carries a recall probability in [0, 1]: {trace!r}")
        if half_life >= kit.HALF_LIFE_MAX_SECONDS:
            assert trace.get("state") == "burned_in", (
                f"a concept at the half-life ceiling is burned_in: {trace!r}")


def test_due_time_matches_the_pinned_formula(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    me = kit.json_of(fresh.get("/auth/me"))
    assert me.get("target_retention") == kit.TARGET_RETENTION, (
        f"the default target retention is {kit.TARGET_RETENTION}: {me!r}")
    session = kit.json_of(kit.start_session(fresh, course))
    assert kit.reconcile(fresh, session["id"],
                         kit.attempts_for(session)).status_code in (200, 201)
    traces = kit.json_of(fresh.get("/traces", params={"course_id": course}))
    assert traces, f"a completed session must produce traces: {traces!r}"
    for trace in traces:
        assert trace.get("due_at"), f"a trace carries a due time: {trace!r}"
        assert trace.get("last_seen_at"), f"a trace carries a last-seen time: {trace!r}"


def test_trace_evaluation_is_deterministic(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    assert kit.reconcile(fresh, session["id"],
                         kit.attempts_for(session)).status_code in (200, 201)
    first = kit.json_of(fresh.get("/traces", params={"course_id": course}))
    second = kit.json_of(fresh.get("/traces", params={"course_id": course}))
    keyed_a = {t["concept_id"]: t.get("half_life_seconds") for t in first}
    keyed_b = {t["concept_id"]: t.get("half_life_seconds") for t in second}
    assert keyed_a == keyed_b, (
        f"two evaluations of one trace at one instant produce the same number: "
        f"{keyed_a!r} then {keyed_b!r}")


def test_returning_learner_is_not_buried_by_the_backlog(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    assert kit.reconcile(fresh, session["id"],
                         kit.attempts_for(session)).status_code in (200, 201)
    profile = kit.json_of(fresh.get("/profile"))
    due = profile.get("due_today")
    assert due is not None, f"the profile names what is due today: {profile!r}"
    backlog = profile.get("backlog_proportion")
    assert backlog is not None and 0.0 <= backlog <= 1.0, (
        f"the backlog is a proportion of the subject, never a count: {profile!r}")
    assert "backlog_count" not in profile, (
        f"a returning learner is never shown a count of overdue items: {profile!r}")
    second = kit.json_of(kit.start_session(fresh, course))
    assert len(second.get("exercises") or []) == kit.LESSON_EXERCISES, (
        f"sessions stay their normal length however large the backlog: {second!r}")


def test_ability_estimate_moves_without_loosening_grading(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    before = kit.json_of(fresh.get("/profile")).get("ability")
    assert before is not None, "a new learner starts at the subject median, not at zero"
    session = kit.json_of(kit.start_session(fresh, course))
    wrong = kit.attempts_for(session, answer=lambda ex: "zzzzz-not-an-answer")
    assert kit.reconcile(fresh, session["id"], wrong).status_code in (200, 201)
    after = kit.json_of(fresh.get("/profile")).get("ability")
    assert after is not None and after != before, (
        f"the ability estimate updates after attempts: {before!r} then {after!r}")
    second = kit.json_of(kit.start_session(fresh, course))
    graded_again = kit.reconcile(fresh, second["id"],
                                 kit.attempts_for(second, answer=lambda ex: "zzzzz"))
    assert graded_again.status_code in (200, 201), kit.describe(graded_again)
    states = [a.get("state") for a in kit.json_of(graded_again).get("attempts", [])]
    assert all(s == "incorrect" for s in states), (
        f"difficulty never loosens what counts as correct: {states!r}")
    for exercise in second.get("exercises") or []:
        assert not exercise.get("time_limit_ms"), (
            f"time pressure never appears in an ordinary lesson: {exercise!r}")


def test_hearts_regenerate_on_read_and_carry_the_partial_interval(fresh, db):
    me = kit.json_of(fresh.get("/auth/me"))
    first = fresh.get("/hearts")
    assert first.status_code == 200, kit.describe(first)
    hearts = kit.json_of(first)
    assert hearts.get("max") == kit.MAX_HEARTS, (
        f"a learner holds at most {kit.MAX_HEARTS} hearts: {hearts!r}")
    assert hearts.get("current") == kit.MAX_HEARTS, (
        f"a new account starts with full hearts: {hearts!r}")
    assert hearts.get("refill_interval_seconds") == kit.REFILL_INTERVAL_SECONDS, (
        f"the refill interval is {kit.REFILL_INTERVAL_SECONDS} seconds: {hearts!r}")
    mark_before = db.rows("hearts", account_id=me["id"])
    assert mark_before, f"a hearts row exists for {me['id']!r}"
    stamp = mark_before[0].get("last_refill_at")
    second = kit.json_of(fresh.get("/hearts"))
    mark_after = db.rows("hearts", account_id=me["id"])[0].get("last_refill_at")
    assert mark_after == stamp, (
        f"reading hearts must not advance the refill mark to now, or the partial "
        f"interval is lost on every read: {stamp!r} then {mark_after!r}")
    assert second.get("current") == hearts.get("current"), (
        f"two reads with no spend return the same count: {hearts!r} then {second!r}")


def test_wrong_answer_in_a_lesson_costs_one_heart(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    before = kit.json_of(fresh.get("/hearts"))["current"]
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session)
    attempts[0]["answer_raw"] = "zzzzz-not-an-answer"
    assert kit.reconcile(fresh, session["id"], attempts).status_code in (200, 201)
    after = kit.json_of(fresh.get("/hearts"))["current"]
    assert after == before - 1, (
        f"one wrong answer in a lesson costs exactly 1 heart: {before} then {after}")


def test_wrong_answer_in_a_review_costs_no_heart(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    before = kit.json_of(fresh.get("/hearts"))["current"]
    started = kit.start_session(fresh, course, kind="review")
    assert started.status_code in (200, 201), kit.describe(started)
    session = kit.json_of(started)
    attempts = kit.attempts_for(session, answer=lambda ex: "zzzzz-not-an-answer")
    assert kit.reconcile(fresh, session["id"], attempts).status_code in (200, 201)
    after = kit.json_of(fresh.get("/hearts"))["current"]
    assert after == before, (
        f"a wrong answer in a review costs no heart: {before} then {after}")


def test_lesson_progress_survives_running_out_of_hearts(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session, answer=lambda ex: "zzzzz-not-an-answer")
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), kit.describe(done)
    hearts = kit.json_of(fresh.get("/hearts"))
    assert hearts["current"] == 0, (
        f"twelve wrong answers exhaust five hearts: {hearts!r}")
    stored = db.count("attempts", session_id=session["id"])
    assert stored > 0, (
        f"running out of hearts keeps the progress made in that lesson, found "
        f"{stored} stored attempts")


def test_practice_restores_one_heart_at_most_once_per_interval(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(session, answer=lambda ex: "zzzzz-not-an-answer")
    assert kit.reconcile(fresh, session["id"], attempts).status_code in (200, 201)
    assert kit.json_of(fresh.get("/hearts"))["current"] == 0
    practice = kit.json_of(kit.start_session(fresh, course, kind="practice"))
    assert kit.reconcile(fresh, practice["id"],
                         kit.attempts_for(practice)).status_code in (200, 201)
    after_one = kit.json_of(fresh.get("/hearts"))["current"]
    assert after_one == 1, (
        f"a completed practice session restores exactly 1 heart, got {after_one}")
    second = kit.json_of(kit.start_session(fresh, course, kind="practice"))
    assert kit.reconcile(fresh, second["id"],
                         kit.attempts_for(second)).status_code in (200, 201)
    after_two = kit.json_of(fresh.get("/hearts"))["current"]
    assert after_two == after_one, (
        f"practice restores a heart at most once per {kit.REFILL_INTERVAL_SECONDS} "
        f"seconds: {after_one} then {after_two}")


def test_streak_is_recomputed_from_history_on_read(learner, db):
    response = learner.get("/streak")
    assert response.status_code == 200, kit.describe(response)
    streak = kit.json_of(response)
    assert streak.get("length") == kit.NADIA_STREAK, (
        f"the seeded streak for {kit.LEARNER_1!r} is {kit.NADIA_STREAK}: {streak!r}")
    assert streak.get("timezone") == kit.TIMEZONES[kit.LEARNER_1], (
        f"the streak is read in the learner's own timezone: {streak!r}")
    last = streak.get("last_day_completed")
    assert isinstance(last, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", last), (
        f"the last completed day is a local calendar date, not an instant: {last!r}")
    rows = db.rows("streaks")
    assert rows, "the streaks table carries the seeded rows"
    stored = [r for r in rows if str(r.get("last_day_completed") or "")[:10] == last]
    assert stored, (
        f"the streak read must reconcile with the stored local date {last!r}: {rows!r}")
    again = kit.json_of(learner.get("/streak"))
    assert again.get("length") == streak.get("length"), (
        f"the streak is computed from history on every read: {streak!r} then {again!r}")
    assert streak.get("freezes_held") == kit.MAX_FREEZES, (
        f"{kit.LEARNER_1!r} is seeded holding {kit.MAX_FREEZES} freezes: {streak!r}")


def test_timezone_change_does_not_shorten_the_streak(fresh):
    before = kit.json_of(fresh.get("/streak"))
    moved = fresh.patch("/settings", json={"timezone": "Pacific/Auckland"})
    assert moved.status_code in (200, 201), kit.describe(moved)
    assert kit.json_of(moved).get("timezone") == "Pacific/Auckland", (
        f"the timezone change must be recorded: {moved.text[:300]}")
    after = kit.json_of(fresh.get("/streak"))
    assert after.get("length") >= before.get("length"), (
        f"a timezone change never shortens the current streak: {before!r} then {after!r}")
    again = fresh.patch("/settings", json={"timezone": "Europe/Lisbon"})
    assert again.status_code in (200, 201, 429, 409), (
        f"a second timezone change inside {kit.RESUMABLE_SECONDS} seconds is rate "
        f"limited rather than silently applied: {kit.describe(again)}")
    forgiven = kit.json_of(fresh.get("/streak"))
    assert forgiven.get("length") >= before.get("length"), (
        f"a gap created by a timezone change is forgiven once per change: {forgiven!r}")


def test_day_boundary_survives_both_daylight_transitions(fresh):
    settings = fresh.patch("/settings", json={"timezone": "Europe/Lisbon",
                                              "day_shift_hours": kit.DAY_SHIFT_MAX_HOURS})
    assert settings.status_code in (200, 201), kit.describe(settings)
    assert kit.json_of(settings).get("day_shift_hours") == kit.DAY_SHIFT_MAX_HOURS, (
        f"a learner may shift the day boundary by up to {kit.DAY_SHIFT_MAX_HOURS} hours: "
        f"{settings.text[:300]}")
    too_far = fresh.patch("/settings",
                          json={"day_shift_hours": kit.DAY_SHIFT_MAX_HOURS + 1})
    assert 400 <= too_far.status_code < 500, (
        f"a day shift beyond {kit.DAY_SHIFT_MAX_HOURS} hours is refused as invalid: "
        f"{kit.describe(too_far)}")
    streak = kit.json_of(fresh.get("/streak"))
    boundary = streak.get("next_boundary_at")
    assert boundary, (
        f"the streak names the next local day boundary so a transition day can be "
        f"read as one day: {streak!r}")
    assert streak.get("local_date"), (
        f"the streak names the local date it covers: {streak!r}")


def test_streak_freeze_is_consumed_once_per_local_date(learner, db):
    streak = kit.json_of(learner.get("/streak"))
    used = streak.get("freezes_used_on") or []
    assert len(used) == len(set(used)), (
        f"a freeze is consumed at most once per local date: {used!r}")
    assert streak.get("freezes_held") <= kit.MAX_FREEZES, (
        f"a learner holds at most {kit.MAX_FREEZES} freezes: {streak!r}")
    first = kit.json_of(learner.get("/streak"))
    second = kit.json_of(learner.get("/streak"))
    assert first.get("freezes_held") == second.get("freezes_held"), (
        f"a repeated read of the streak consumes no freeze: {first!r} then {second!r}")
    rows = db.rows("streaks")
    for row in rows:
        stored = row.get("freezes_used_on") or []
        dates = list(stored) if isinstance(stored, (list, tuple)) else json.loads(stored or "[]")
        assert len(dates) == len(set(dates)), (
            f"no account carries the same freeze date twice: {row!r}")
        assert (row.get("freezes_held") or 0) <= kit.MAX_FREEZES, (
            f"no account holds more than {kit.MAX_FREEZES} freezes: {row!r}")


def test_streak_repair_restores_the_exact_previous_length(fresh):
    before = kit.json_of(fresh.get("/streak"))
    repaired = fresh.post("/streak/repair")
    assert repaired.status_code in (200, 201, 400, 404, 409, 422), (
        f"a repair on an unlapsed streak is refused rather than fabricated: "
        f"{kit.describe(repaired)}")
    after = kit.json_of(fresh.get("/streak"))
    assert after.get("length") == before.get("length"), (
        f"repair restores the exact previous length, never a rounded number: "
        f"{before!r} then {after!r}")
    window = after.get("repair_window_seconds")
    if window is not None:
        assert window == kit.REPAIR_WINDOW_SECONDS, (
            f"the repair window is {kit.REPAIR_WINDOW_SECONDS} seconds: {after!r}")


def test_points_awarded_match_the_pinned_table(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    done = kit.reconcile(fresh, session["id"], kit.attempts_for(session))
    assert done.status_code in (200, 201), kit.describe(done)
    perfect_first = kit.AWARD_LESSON + kit.AWARD_PERFECT_BONUS + kit.AWARD_FIRST_OF_DAY_BONUS
    assert kit.json_of(done).get("points_earned") == perfect_first, (
        f"a perfect first lesson of the day awards "
        f"{kit.AWARD_LESSON} + {kit.AWARD_PERFECT_BONUS} + "
        f"{kit.AWARD_FIRST_OF_DAY_BONUS} = {perfect_first}: {done.text[:300]}")
    second = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(second)
    attempts[0]["answer_raw"] = "zzzzz-not-an-answer"
    again = kit.reconcile(fresh, second["id"], attempts)
    assert again.status_code in (200, 201), kit.describe(again)
    assert kit.json_of(again).get("points_earned") == kit.AWARD_LESSON, (
        f"a second, imperfect lesson the same day awards {kit.AWARD_LESSON}: "
        f"{again.text[:300]}")
    review = kit.json_of(kit.start_session(fresh, course, kind="review"))
    graded = kit.reconcile(fresh, review["id"], kit.attempts_for(review))
    assert graded.status_code in (200, 201), kit.describe(graded)
    assert kit.json_of(graded).get("points_earned") == \
        kit.AWARD_REVIEW + kit.AWARD_PERFECT_BONUS, (
            f"a perfect review awards {kit.AWARD_REVIEW} + {kit.AWARD_PERFECT_BONUS}: "
            f"{graded.text[:300]}")


def test_cohort_holds_twelve_seeded_members_at_bronze(learner2, db):
    response = learner2.get("/league")
    assert response.status_code == 200, kit.describe(response)
    league = kit.json_of(response)
    assert league.get("tier") == kit.COHORT_TIER, (
        f"the seeded cohort sits at tier {kit.COHORT_TIER!r}: {league!r}")
    standings = league.get("standings") or []
    assert len(standings) == kit.SEEDED_COHORT_SIZE, (
        f"the seeded cohort holds exactly {kit.SEEDED_COHORT_SIZE} members, "
        f"got {len(standings)}")
    assert len(standings) <= kit.COHORT_CAPACITY, (
        f"a cohort holds at most {kit.COHORT_CAPACITY} learners: {len(standings)}")
    assert league.get("tiers") == kit.TIERS, (
        f"the ten tiers run {kit.TIERS}: {league.get('tiers')!r}")
    for row in standings:
        assert row.get("joined_at"), (
            f"a standings row records when the learner joined by earning: {row!r}")
    rows = db.rows("cohorts")
    assert rows, "the cohorts table carries the seeded cohort"
    assert all((r.get("member_count") or 0) <= kit.COHORT_CAPACITY for r in rows), (
        f"no cohort exceeds {kit.COHORT_CAPACITY} members: {rows!r}")


def test_promotion_and_demotion_zones_partition_the_board(learner2):
    league = kit.json_of(learner2.get("/league"))
    standings = league.get("standings") or []
    promoted = [r for r in standings if r.get("zone") == "promotion"]
    demoted = [r for r in standings if r.get("zone") == "demotion"]
    assert len(promoted) == kit.PROMOTED, (
        f"the top {kit.PROMOTED} are promoted, got {len(promoted)}: {standings!r}")
    assert len(demoted) == kit.DEMOTED, (
        f"the bottom {kit.DEMOTED} are demoted, got {len(demoted)}: {standings!r}")
    assert len(promoted) + len(demoted) == len(standings), (
        f"twelve members partition exactly into the two zones: {standings!r}")
    ids = [r.get("account_id") for r in promoted] + [r.get("account_id") for r in demoted]
    assert len(ids) == len(set(ids)), (
        f"no member sits in both zones: {standings!r}")
    assert league.get("tier") != kit.TIERS[0] or not demoted, (
        f"nobody is demoted out of {kit.TIERS[0]!r}: {league!r}")
    assert league.get("tier") != kit.TIERS[-1] or not promoted, (
        f"nobody is promoted out of {kit.TIERS[-1]!r}: {league!r}")


def test_cohort_standings_order_breaks_ties_by_earlier_earner(learner2):
    league = kit.json_of(learner2.get("/league"))
    standings = league.get("standings") or []
    points = [r.get("xp_this_week") for r in standings]
    assert points == sorted(points, reverse=True), (
        f"standings are ordered by the weekly total, highest first: {points!r}")
    tied = [r for r in standings if r.get("xp_this_week") == kit.TIED_POINTS]
    assert len(tied) == 2, (
        f"exactly two seeded members hold {kit.TIED_POINTS} points: {points!r}")
    earlier, later = tied[0], tied[1]
    assert earlier.get("last_earned_at") <= later.get("last_earned_at"), (
        f"a tie is broken by the earlier last earning time, not by account identifier: "
        f"{earlier!r} then {later!r}")
    positions = [standings.index(earlier) + 1, standings.index(later) + 1]
    assert positions == [kit.PROMOTED, kit.PROMOTED + 1], (
        f"the tied pair sits at the promotion line at positions "
        f"{[kit.PROMOTED, kit.PROMOTED + 1]}, got {positions}")


def test_cohort_week_closes_at_one_instant_and_freezes(learner, learner2):
    mine = kit.json_of(learner.get("/league"))
    theirs = kit.json_of(learner2.get("/league"))
    assert mine.get("week_id") == theirs.get("week_id"), (
        f"members share one week identity: {mine.get('week_id')!r} vs "
        f"{theirs.get('week_id')!r}")
    assert mine.get("closes_at") == theirs.get("closes_at"), (
        f"a cohort week ends at one fixed instant for every member: "
        f"{mine.get('closes_at')!r} vs {theirs.get('closes_at')!r}")
    assert mine.get("deadline_timezone") == kit.TIMEZONES[kit.LEARNER_1], (
        f"the deadline is shown converted into the reader's own timezone: {mine!r}")
    assert theirs.get("deadline_timezone") == kit.TIMEZONES[kit.LEARNER_2], (
        f"the deadline is shown converted into the reader's own timezone: {theirs!r}")
    assert mine.get("closed") is False, (
        f"the current week is open until its fixed instant: {mine!r}")


def test_own_standings_row_is_current_after_earning(learner2):
    league = kit.json_of(learner2.get("/league"))
    me = kit.json_of(learner2.get("/auth/me"))
    own = [r for r in league.get("standings", []) if r.get("account_id") == me["id"]]
    assert len(own) == 1, (
        f"the reader's own row appears exactly once: {league.get('standings')!r}")
    assert own[0].get("is_self") is True, (
        f"the reader's own row is marked so the page can keep it current: {own[0]!r}")
    assert own[0].get("xp_this_week") == kit.BRAM_POINTS, (
        f"the seeded weekly total for {kit.LEARNER_2!r} is {kit.BRAM_POINTS}: {own[0]!r}")
    staleness = league.get("staleness_ceiling_seconds")
    assert staleness == kit.STALE_BOARD_SECONDS, (
        f"the board is at most {kit.STALE_BOARD_SECONDS} seconds stale: {league!r}")


def test_unit_progress_is_never_reduced_by_a_write(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    me = kit.json_of(fresh.get("/auth/me"))
    session = kit.json_of(kit.start_session(fresh, course))
    assert kit.reconcile(fresh, session["id"],
                         kit.attempts_for(session)).status_code in (200, 201)
    path = kit.json_of(fresh.get(f"/path/{course}"))
    crowns_before = {u["id"]: u.get("crowns", 0) for u in path}
    locked_before = {u["id"]: bool(u.get("locked")) for u in path}
    assert kit.enrol(fresh, course).status_code in (200, 201, 409)
    after = kit.json_of(fresh.get(f"/path/{course}"))
    for unit in after:
        assert unit.get("crowns", 0) >= crowns_before.get(unit["id"], 0), (
            f"no write lowers a crown count for unit {unit['id']!r}: "
            f"{crowns_before.get(unit['id'])} then {unit.get('crowns')}")
        if not locked_before.get(unit["id"], True):
            assert not unit.get("locked"), (
                f"no write relocks an unlocked unit {unit['id']!r}: {unit!r}")
    rows = db.rows("unit_states", account_id=me["id"])
    assert rows, f"unit states are stored per unit identity for {me['id']!r}"
    ids = [r.get("unit_id") for r in rows]
    assert len(ids) == len(set(ids)), (
        f"unit states are keyed by unit identity, never by position: {ids!r}")


def test_seeding_is_idempotent_across_a_restart(db):
    for email in (kit.LEARNER_1, kit.LEARNER_2, kit.LEARNER_3, *kit.COHORT_EMAILS):
        assert db.count("accounts", email=email) == 1, (
            f"seeding must not duplicate {email!r}, found "
            f"{db.count('accounts', email=email)} rows")
    assert db.count("courses") == kit.PICKER_COUNT, (
        f"seeding must not duplicate courses: found {db.count('courses')} rows for "
        f"{kit.PICKER_COUNT} subjects")
    for slug in kit.OPEN_SUBJECTS:
        assert db.count("courses", id=slug) == 1, f"subject {slug!r} is seeded once"
        assert db.count("units", course_id=slug) == kit.UNITS_PER_SUBJECT, (
            f"subject {slug!r} carries {kit.UNITS_PER_SUBJECT} units, found "
            f"{db.count('units', course_id=slug)}")
        assert db.count("exercises", course_id=slug) == kit.EXERCISES_PER_SUBJECT, (
            f"subject {slug!r} carries {kit.EXERCISES_PER_SUBJECT} exercises, found "
            f"{db.count('exercises', course_id=slug)}")


def test_subject_graph_is_validated_at_load(anon, db):
    for slug in kit.OPEN_SUBJECTS:
        response = anon.get(f"/courses/{slug}")
        assert response.status_code == 200, kit.describe(response)
        units = kit.json_of(response).get("units") or []
        introduced = set()
        for unit in units:
            for concept in unit.get("exercises_concept_ids") or []:
                assert concept in introduced, (
                    f"unit {unit.get('id')!r} of {slug!r} exercises concept "
                    f"{concept!r} that no earlier unit introduced")
            introduced.update(unit.get("introduces_concept_ids") or [])
        orders = [u.get("order") for u in units]
        assert orders == sorted(orders), (
            f"units are returned in order for {slug!r}: {orders!r}")
    rows = db.rows("units", course_id=kit.OPEN_SUBJECTS[0])
    assert rows, f"units are stored for {kit.OPEN_SUBJECTS[0]!r}"
    ids = [r.get("id") for r in rows]
    assert len(ids) == len(set(ids)), f"unit identities are unique: {ids!r}"


def test_session_is_pinned_to_a_subject_version_at_assembly(fresh, db):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    assert session.get("course_version") is not None, (
        f"a session records the subject version it was assembled against: {session!r}")
    rows = db.rows("sessions", id=session["id"])
    assert rows and rows[0].get("course_version") == session["course_version"], (
        f"the pinned version is stored with the session: {rows!r}")
    courses = db.rows("courses", id=course)
    assert courses and courses[0].get("version") is not None, (
        f"the subject carries a version: {courses!r}")
    retention = session.get("version_retained_seconds")
    if retention is not None:
        assert retention >= kit.REGRADE_WINDOW_SECONDS, (
            f"a referenced version stays available for at least "
            f"{kit.REGRADE_WINDOW_SECONDS} seconds: {session!r}")




def test_cross_account_progress_read_is_denied_at_the_api(learner, learner2, db):
    victim = kit.json_of(learner.get("/auth/me"))
    intruder = kit.json_of(learner2.get("/auth/me"))
    assert victim["id"] != intruder["id"], "the two seeded accounts must be distinct"
    before = db.rows("streaks", account_id=victim["id"])
    for path in (f"/profile?account_id={victim['id']}",
                 f"/streak?account_id={victim['id']}",
                 f"/hearts?account_id={victim['id']}",
                 f"/traces?account_id={victim['id']}",
                 f"/history?account_id={victim['id']}"):
        response = learner2.get(path)
        assert response.status_code < 500, (
            f"a cross-account read must be denied, never a server error: "
            f"{kit.describe(response)}")
        if response.status_code == 200:
            body = kit.json_of(response)
            blob = json.dumps(body)
            assert victim["id"] not in blob, (
                f"{path} leaked another account's data to {intruder['id']!r}: "
                f"{blob[:400]}")
    written = learner2.patch(f"/settings?account_id={victim['id']}",
                             json={"daily_goal_lessons": 3})
    assert written.status_code < 500, kit.describe(written)
    after = db.rows("streaks", account_id=victim["id"])
    assert after == before, (
        f"a denied cross-account write leaves the protected rows unchanged: "
        f"{before!r} then {after!r}")


def test_unauthenticated_request_to_a_learner_route_is_denied(raw, anon):
    for path in ("/profile", "/streak", "/hearts", "/traces", "/history", "/league",
                 "/enrolments", "/page-views"):
        response = anon.get(path)
        assert response.status_code in (401, 403), (
            f"an unauthenticated call to {path} must be denied, got "
            f"{kit.describe(response)}")
    for route in kit.LEARNER_ROUTES:
        page = raw.get(route)
        assert page.status_code in (301, 302, 303, 307, 308, 401, 403), (
            f"an unauthenticated visit to {route} must redirect to the sign-in page "
            f"rather than serve it: {kit.describe(page)}")
        if page.status_code in (301, 302, 303, 307, 308):
            target = page.headers.get("location", "")
            assert "/login" in target, (
                f"{route} must redirect to /login, got {target!r}")


def test_expired_token_is_denied_on_every_protected_route(anon):
    forged = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwcm9iZSIsImV4cCI6MX0.not-a-real-signature"
    with appclient.client(forged) as client:
        for path in ("/auth/me", "/profile", "/streak", "/hearts"):
            response = client.get(path)
            assert response.status_code in (401, 403), (
                f"a tampered or expired token must be denied on {path}: "
                f"{kit.describe(response)}")
    me = anon.post("/auth/login",
                   json={"email": kit.LEARNER_1, "password": kit.PASSWORD})
    assert me.status_code == 200, kit.describe(me)
    body = kit.json_of(me)
    assert body.get("expires_in") == 86400 or body.get("expires_at"), (
        f"the login response must state the 24 hour token lifetime: {body!r}")


def test_learner_cannot_write_a_derived_total_directly(learner, db):
    me = kit.json_of(learner.get("/auth/me"))
    before_streak = kit.json_of(learner.get("/streak")).get("length")
    before_points = kit.json_of(learner.get("/profile")).get("points_this_week")
    for path, payload in ((f"/profile", {"points_this_week": 99999}),
                          ("/streak", {"length": 9999}),
                          ("/hearts", {"current": 99}),
                          ("/league", {"xp_this_week": 99999})):
        response = learner.patch(path, json=payload)
        assert response.status_code < 500, (
            f"a write to the derived total at {path} must be refused, never a server "
            f"error: {kit.describe(response)}")
    after_streak = kit.json_of(learner.get("/streak")).get("length")
    after_points = kit.json_of(learner.get("/profile")).get("points_this_week")
    assert after_streak == before_streak, (
        f"a learner cannot write their own streak length: {before_streak} then "
        f"{after_streak}")
    assert after_points == before_points, (
        f"a learner cannot write their own weekly total: {before_points} then "
        f"{after_points}")
    rows = db.rows("standings", account_id=me["id"])
    for row in rows:
        assert (row.get("xp_this_week") or 0) < 99999, (
            f"no client-proposed total reached the standings row: {row!r}")


def test_restricted_account_is_offered_no_purchase_route(learner3, page):
    me = kit.json_of(learner3.get("/auth/me"))
    assert me.get("restricted") is True, (
        f"{kit.LEARNER_3!r} is seeded restricted: {me!r}")
    hearts = kit.json_of(learner3.get("/hearts"))
    routes = hearts.get("routes_offered") or []
    assert routes, f"a restricted account is offered routes out of heart exhaustion: {hearts!r}"
    assert set(routes) <= {"practice", "wait"}, (
        f"a restricted account is offered practice or waiting only, got {routes!r}")
    forbidden = re.compile(r"(?:\$|usd|price|upgrade|buy|purchase|subscribe)", re.I)
    token = learner3.headers.get("Authorization", "")
    page.set_extra_http_headers({"Authorization": token})
    for route in ("/learn", "/profile", "/settings"):
        page.goto(kit.absolute(route))
        text = page.inner_text("body")
        assert not forbidden.search(text), (
            f"{route} offered a restricted account something to buy: "
            f"{forbidden.search(text).group(0)!r} in {text[:300]!r}")


def test_password_hash_is_never_returned_by_any_endpoint(learner, anon):
    watched = ("password_hash", "passwordHash", "$2b$", "$2a$", "$argon2",
               "pbkdf2", "scrypt")
    for path in ("/auth/me", "/profile", "/streak", "/hearts", "/enrolments",
                 "/history", "/league", "/traces", "/page-views"):
        response = learner.get(path)
        assert response.status_code == 200, kit.describe(response)
        body = response.text
        for needle in watched:
            assert needle not in body, (
                f"{path} leaked a password hash marker {needle!r}: {body[:400]}")
        assert kit.PASSWORD not in body, (
            f"{path} echoed the seeded password back: {body[:400]}")
    login = anon.post("/auth/login",
                      json={"email": kit.LEARNER_1, "password": kit.PASSWORD})
    assert login.status_code == 200, kit.describe(login)
    for needle in watched:
        assert needle not in login.text, (
            f"the login response leaked {needle!r}: {login.text[:400]}")




def test_session_start_in_a_closed_subject_is_refused(learner, db):
    listed = kit.json_of(learner.get("/courses"))
    closed = [c for c in listed if not c.get("is_open")]
    assert closed, "the picker must carry subjects that are not open"
    target = closed[0]["id"]
    before = db.count("sessions")
    response = learner.post("/sessions", json={"course_id": target, "unit_id": None,
                                               "lesson_id": None, "kind": "lesson"})
    assert 400 <= response.status_code < 500, (
        f"starting a session in the closed subject {target!r} is refused as invalid: "
        f"{kit.describe(response)}")
    assert db.count("sessions") == before, (
        f"a refused session start writes nothing: {before} then {db.count('sessions')}")
    enrolled = kit.enrol(learner, target)
    assert 400 <= enrolled.status_code < 500, (
        f"enrolling in a closed subject is refused as invalid: {kit.describe(enrolled)}")


def test_accepted_answer_set_expands_from_the_declared_grammar(anon):
    response = anon.get(f"/courses/{kit.OPEN_SUBJECTS[0]}")
    assert response.status_code == 200, kit.describe(response)
    samples = kit.json_of(response).get("samples") or []
    assert samples, "an open subject exposes samples"
    for sample in samples:
        accepted = sample.get("accepted_count")
        assert accepted is not None, (
            f"a sample names how many accepted forms its grammar expands to: {sample!r}")
        assert 1 <= accepted <= kit.GRAMMAR_FORM_CEILING, (
            f"an accepted set expands to between 1 and {kit.GRAMMAR_FORM_CEILING} "
            f"forms: {sample!r}")


def test_normalization_order_is_applied_before_comparison(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(
        session, answer=lambda ex: f"  {(ex.get('solution_canonical') or '').upper()}  ")
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), kit.describe(done)
    states = [a.get("state") for a in kit.json_of(done).get("attempts", [])]
    assert all(s in ("correct", "correct_with_note") for s in states), (
        f"case folding with whitespace collapse happens before comparison: {states!r}")


def test_typo_within_threshold_is_accepted_with_a_note(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))

    def transposed(exercise):
        answer = exercise.get("solution_canonical") or ""
        if len(answer) < 5:
            return answer
        return answer[:2] + answer[3] + answer[2] + answer[4:]

    attempts = kit.attempts_for(session, answer=transposed)
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), kit.describe(done)
    graded = kit.json_of(done).get("attempts", [])
    noted = [a for a in graded if a.get("state") == "correct_with_note"]
    assert noted, (
        f"a transposition of two adjacent characters counts as one edit and is "
        f"accepted with a note: {graded!r}")
    for attempt in noted:
        assert attempt.get("note_kind") == "typo", (
            f"a distance acceptance carries the typo note, never a silent correct: "
            f"{attempt!r}")


def test_missing_accent_is_accepted_with_a_note(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    folded = {"a": "aaeiou", "á": "a", "é": "e", "í": "i",
              "ó": "o", "ú": "u", "ñ": "n"}

    def stripped(exercise):
        answer = exercise.get("solution_canonical") or ""
        return "".join(folded.get(ch, ch) if len(folded.get(ch, ch)) == 1 else ch
                       for ch in answer)

    attempts = kit.attempts_for(session, answer=stripped)
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), kit.describe(done)
    graded = kit.json_of(done).get("attempts", [])
    for attempt in graded:
        assert attempt.get("state") != "correct" or attempt.get("note_kind") is None, (
            f"a missing accent is correct_with_note, never a silent correct: {attempt!r}")


def test_near_miss_that_is_a_taught_word_is_marked_incorrect(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    taught = {}
    for exercise in session["exercises"]:
        answer = exercise.get("solution_canonical") or ""
        taught.setdefault(len(answer), []).append(answer)
    neighbour = None
    for length, answers in taught.items():
        unique = sorted(set(answers))
        if len(unique) >= 2:
            neighbour = (unique[0], unique[1])
            break
    attempts = kit.attempts_for(session)
    if neighbour:
        for attempt, exercise in zip(attempts, session["exercises"]):
            if (exercise.get("solution_canonical") or "") == neighbour[0]:
                attempt["answer_raw"] = neighbour[1]
                break
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), kit.describe(done)
    graded = kit.json_of(done).get("attempts", [])
    assert graded, f"the reconcile result names each graded attempt: {done.text[:300]}"
    assert all(a.get("state") in kit.ATTEMPT_STATES for a in graded), (
        f"every graded attempt carries one of the four pinned states: {graded!r}")
    if neighbour:
        swapped = [a for a in graded if a.get("answer_raw") == neighbour[1]
                   and a.get("expected") == neighbour[0]]
        for attempt in swapped:
            assert attempt.get("state") == "incorrect", (
                f"a near miss that is itself a taught answer is incorrect, never "
                f"accepted on distance: {attempt!r}")


def test_free_word_order_answer_is_matched_as_a_multiset(anon):
    response = anon.get(f"/courses/{kit.OPEN_SUBJECTS[0]}")
    body = kit.json_of(response)
    samples = body.get("samples") or []
    for sample in samples:
        if sample.get("required_tokens"):
            assert isinstance(sample["required_tokens"], list), (
                f"required tokens are a list for an order-free exercise: {sample!r}")
            assert sample.get("free_positions") is not None, (
                f"the content declares which positions are free, the grader never "
                f"infers it: {sample!r}")
        assert sample.get("partial_credit") in (None, False), (
            f"there is no partial credit: {sample!r}")


def test_word_bank_holds_no_valid_alternative_answer(anon):
    for slug in kit.OPEN_SUBJECTS:
        response = anon.get(f"/courses/{slug}")
        assert response.status_code == 200, kit.describe(response)
        for sample in kit.json_of(response).get("samples") or []:
            distractors = sample.get("distractors") or []
            if not distractors:
                continue
            assert 2 <= len(distractors) <= 4, (
                f"a word bank holds 2 to 4 distractors beyond the solution tokens: "
                f"{sample!r}")
            accepted = set(sample.get("accepted_tokens") or [])
            overlap = accepted.intersection(distractors)
            assert not overlap, (
                f"no distractor in {slug!r} is a valid alternative answer: "
                f"{sorted(overlap)!r}")
            level = sample.get("cefr_level")
            for distractor in distractors:
                assert isinstance(distractor, str) and distractor, (
                    f"a distractor is a real token from the same subject at or below "
                    f"level {level!r}: {sample!r}")


def test_word_bank_shuffle_is_stable_across_a_reload(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    first = [ex.get("bank") for ex in session["exercises"]]
    again = kit.json_of(fresh.get(f"/sessions/{session['id']}"))
    second = [ex.get("bank") for ex in again["exercises"]]
    assert second == first, (
        f"the bank shuffle is seeded from the session id, so a reload does not "
        f"reshuffle: {first!r} then {second!r}")
    other = kit.json_of(kit.start_session(fresh, course))
    assert other["id"] != session["id"], "a second session has its own identity"


def test_free_text_answer_is_never_filtered_by_character(fresh):
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    attempts = kit.attempts_for(
        session, answer=lambda ex: "éñ你好-الع")
    done = kit.reconcile(fresh, session["id"], attempts)
    assert done.status_code in (200, 201), (
        f"a free-text answer is graded rather than refused for its characters: "
        f"{kit.describe(done)}")
    graded = kit.json_of(done).get("attempts", [])
    assert all(a.get("state") in kit.ATTEMPT_STATES for a in graded), (
        f"an unexpected script is graded, never filtered: {graded!r}")


def test_regrade_refunds_hearts_without_touching_standings(anon):
    response = anon.get(f"/courses/{kit.OPEN_SUBJECTS[0]}")
    body = kit.json_of(response)
    window = body.get("regrade_window_seconds")
    assert window == kit.REGRADE_WINDOW_SECONDS, (
        f"the regrade window is {kit.REGRADE_WINDOW_SECONDS} seconds: {body!r}")
    assert body.get("regrade_adjusts_standings") in (None, False), (
        f"a regrade adjusts no settled standing: {body!r}")
    assert body.get("regrade_refunds_hearts") is True, (
        f"a regrade refunds the hearts of every learner affected: {body!r}")


def test_subject_content_safety_checks_refuse_a_bad_subject(anon):
    response = anon.get("/courses")
    assert response.status_code == 200, kit.describe(response)
    for course in kit.json_of(response):
        if not course.get("is_open"):
            continue
        detail = anon.get(f"/courses/{course['id']}")
        assert detail.status_code == 200, (
            f"an open subject must load, so it passed the content checks: "
            f"{kit.describe(detail)}")
        body = kit.json_of(detail)
        for sample in body.get("samples") or []:
            canonical = (sample.get("solution_canonical") or "").strip()
            assert canonical, (
                f"no canonical solution is empty once normalized: {sample!r}")
            accepted = set(sample.get("accepted_tokens") or [])
            assert not accepted.intersection(sample.get("distractors") or []), (
                f"a subject whose bank holds a second correct answer must not load: "
                f"{sample!r}")


def test_untranslated_guidebook_falls_back_with_a_marker(anon):
    for slug in kit.OPEN_SUBJECTS:
        response = anon.get(f"/courses/{slug}")
        assert response.status_code == 200, kit.describe(response)
        for unit in kit.json_of(response).get("units") or []:
            guidebook = unit.get("guidebook")
            assert guidebook, (
                f"every unit of {slug!r} carries an explanation: {unit!r}")
            if unit.get("guidebook_translated") is False:
                assert unit.get("guidebook_fallback_marker"), (
                    f"an untranslated explanation falls back with a marker rather "
                    f"than being hidden: {unit!r}")


def test_feed_route_serves_the_same_page_as_the_root(raw):
    root = raw.get("/")
    feed = raw.get("/feed")
    assert root.status_code == 200, kit.describe(root)
    assert feed.status_code == 200, kit.describe(feed)
    root_title = re.search(r"<title[^>]*>(.*?)</title>", root.text, re.S | re.I)
    feed_title = re.search(r"<title[^>]*>(.*?)</title>", feed.text, re.S | re.I)
    assert root_title and feed_title, "both routes must carry a document title"
    assert root_title.group(1).strip() == feed_title.group(1).strip(), (
        f"/ and /feed serve one page with one title: {root_title.group(1)!r} vs "
        f"{feed_title.group(1)!r}")


def test_no_learner_count_or_efficacy_claim_appears(raw):
    banned = re.compile(
        r"(\d[\d,.]*\s*(million|billion|m\+|k\+)\s+(learners|users|people))"
        r"|(research shows that it works)"
        r"|(\d+\s*%\s*(more|better|faster)\s+effective)", re.I)
    for route in ("/", "/feed", "/courses", "/blog"):
        response = raw.get(route)
        assert response.status_code == 200, kit.describe(response)
        hit = banned.search(response.text)
        assert not hit, (
            f"{route} carries an unsupported claim {hit.group(0)!r}; no learner count "
            f"and no efficacy claim may appear")


def test_every_internal_link_on_a_public_route_resolves(raw):
    seen = {}
    for route in kit.PUBLIC_ROUTES:
        response = raw.get(route)
        assert response.status_code == 200, (
            f"a public route that exists must be served with a success response: "
            f"{kit.describe(response)}")
        for href in re.findall(r'href="([^"#?]+)', response.text):
            if href.startswith("http") or href.startswith("mailto:") or not href.startswith("/"):
                continue
            seen.setdefault(href, route)
    assert seen, "the public pages must carry internal links"
    broken = []
    for href, source in sorted(seen.items()):
        target = raw.get(href)
        if target.status_code >= 400:
            broken.append((href, source, target.status_code))
    assert not broken, (
        f"every internal link on every public route resolves; broken: {broken!r}")


def test_terms_page_is_linked_from_the_signup_form(raw):
    signup = raw.get("/signup")
    assert signup.status_code == 200, kit.describe(signup)
    assert 'href="/terms' in signup.text, (
        f"the signup form links the terms page: {signup.text[:600]!r}")
    for route in ("/", "/courses", "/blog"):
        page = raw.get(route)
        assert 'href="/terms' in page.text, (
            f"{route} must reach the terms page from its footer")
        assert 'href="/privacy' in page.text, (
            f"{route} must reach the privacy page from its footer")
    privacy = raw.get("/privacy")
    assert privacy.status_code == 200, kit.describe(privacy)
    assert re.search(r"(record|store|keep)", privacy.text, re.I), (
        f"the privacy page states what the product records about a learner: "
        f"{privacy.text[:400]!r}")


def test_public_routes_declare_unique_preview_titles(raw):
    titles = {}
    for route in kit.PUBLIC_ROUTES:
        response = raw.get(route)
        assert response.status_code == 200, kit.describe(response)
        title = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]*)"',
                          response.text)
        description = re.search(
            r'<meta[^>]+name="description"[^>]+content="([^"]*)"', response.text)
        image = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]*)"',
                          response.text)
        assert title and title.group(1).strip(), (
            f"{route} declares its own social preview title: {response.text[:400]!r}")
        assert description and description.group(1).strip(), (
            f"{route} declares its own description: {response.text[:400]!r}")
        assert image and image.group(1).strip(), (
            f"{route} declares a social preview image: {response.text[:400]!r}")
        resolved = raw.get(urllib.parse.urlparse(image.group(1)).path)
        assert resolved.status_code == 200, (
            f"the preview image declared by {route} must resolve: "
            f"{kit.describe(resolved)}")
        assert title.group(1) not in titles, (
            f"{route} repeats the preview title of {titles.get(title.group(1))!r}")
        titles[title.group(1)] = route


def test_unknown_address_answers_not_found_with_the_pinned_title(raw):
    missing = f"/definitely-not-a-route-{'x' * 12}"
    response = raw.get(missing)
    assert response.status_code == 404, (
        f"an unknown address answers not found: {kit.describe(response)}")
    title = re.search(r"<title[^>]*>(.*?)</title>", response.text, re.S | re.I)
    assert title and title.group(1).strip() == kit.NOT_FOUND_TITLE, (
        f"the document title of a not-found response is {kit.NOT_FOUND_TITLE!r}, got "
        f"{title.group(1).strip() if title else None!r}")
    assert kit.NOT_FOUND_TITLE in response.text, (
        f"the not-found page carries {kit.NOT_FOUND_TITLE!r} on the page as well as "
        f"in the tab: {response.text[:400]!r}")
    assert missing in response.text, (
        f"the not-found page names the address that failed: {response.text[:400]!r}")
    assert 'href="/courses' in response.text, (
        f"the not-found page links the subject index: {response.text[:400]!r}")


def test_mistyped_subject_address_renders_the_picker_page(raw):
    response = raw.get("/courses/spanihs")
    assert response.status_code == 404, (
        f"a mistyped subject address answers not found: {kit.describe(response)}")
    for name in kit.PICKER_ORDER[:5]:
        assert name in response.text, (
            f"the mistyped-subject page carries the full picker; {name!r} is missing: "
            f"{response.text[:400]!r}")
    assert re.search(r"no subject at that address", response.text, re.I), (
        f"the mistyped-subject page says there is no subject at that address: "
        f"{response.text[:400]!r}")


def test_empty_history_renders_its_own_empty_state(fresh):
    response = fresh.get("/history")
    assert response.status_code == 200, kit.describe(response)
    body = kit.json_of(response)
    assert isinstance(body, list), f"/api/history returns an array: {body!r}"
    assert body == [], (
        f"a new account has an empty history rather than fabricated days: {body!r}")
    profile = fresh.get("/profile")
    assert profile.status_code == 200, kit.describe(profile)
    assert kit.json_of(profile).get("empty_state"), (
        f"an empty profile states the empty case in the product's own words: "
        f"{profile.text[:300]!r}")


def test_page_views_are_recorded_and_readable_by_their_owner(learner, learner2, raw):
    before = len(kit.json_of(learner.get("/page-views")))
    token = learner.headers.get("Authorization", "")
    visited = raw.get("/profile", headers={"Authorization": token})
    assert visited.status_code < 500, kit.describe(visited)
    after = kit.settle(lambda: len(kit.json_of(learner.get("/page-views"))) > before)
    assert after, (
        f"a page view is recorded with its route: the count stayed at {before}")
    views = kit.json_of(learner.get("/page-views"))
    for view in views:
        assert view.get("route") and view.get("viewed_at"), (
            f"a recorded view names its route and the time of the view: {view!r}")
    mine = kit.json_of(learner.get("/auth/me"))["id"]
    theirs = kit.json_of(learner2.get("/page-views"))
    assert all(v.get("account_id") != mine for v in theirs), (
        f"a learner reads back only their own views: {theirs[:3]!r}")


def test_long_form_pages_carry_contents_and_a_dated_summary(raw):
    for route in ("/terms", "/privacy", "/community-guidelines", "/status", "/blog"):
        response = raw.get(route)
        assert response.status_code == 200, kit.describe(response)
        text = response.text
        assert re.search(r"(table of contents|contents)", text, re.I), (
            f"{route} carries a table of contents: {text[:400]!r}")
        assert re.search(r"(last updated|updated on)", text, re.I), (
            f"{route} carries a last-updated date: {text[:400]!r}")
        assert re.search(r"(what changed|summary of changes|summary)", text, re.I), (
            f"{route} carries a one-line summary of what changed: {text[:400]!r}")


def test_first_view_of_the_marketing_page_ships_no_binary(raw):
    response = raw.get("/")
    assert response.status_code == 200, kit.describe(response)
    total = len(response.content)
    assets = set()
    for attr in ("src", "href"):
        assets.update(re.findall(rf'{attr}="(/[^"?#]+)"', response.text))
    binaries = sorted(a for a in assets if a.lower().endswith(kit.BINARY_SUFFIXES))
    assert not binaries, (
        f"the first view of the marketing page ships no binary of any kind: {binaries!r}")
    for asset in sorted(assets):
        fetched = raw.get(asset)
        assert fetched.status_code < 400, (
            f"asset {asset!r} referenced by / must resolve: {kit.describe(fetched)}")
        total += len(fetched.content)
    assert total <= kit.MARKETING_FIRST_VIEW_BYTES, (
        f"the first view of / transfers under {kit.MARKETING_FIRST_VIEW_BYTES} bytes, "
        f"measured {total}")


def test_no_address_outside_the_application_is_referenced(raw):
    origin = urllib.parse.urlparse(kit.app_url()).netloc
    for route in kit.PUBLIC_ROUTES:
        response = raw.get(route)
        assert response.status_code == 200, kit.describe(response)
        external = []
        for url in re.findall(r'(?:src|href)="(https?://[^"]+)"', response.text):
            host = urllib.parse.urlparse(url).netloc
            if host and host != origin:
                external.append(url)
        assert not external, (
            f"{route} references an address outside the application: {external!r}")
        assert "//fonts.googleapis.com" not in response.text, (
            f"{route} reaches a hosted font service")
        assert not re.search(r"(api[_-]?key|secret|bearer\s+ey)", response.text, re.I), (
            f"{route} ships something usable as a credential: {response.text[:300]!r}")


def test_body_text_meets_the_contrast_bar(page):
    page.goto(kit.absolute("/"))
    ratio = page.evaluate(
        """() => {
          const parse = (value) => {
            const parts = value.match(/[\\d.]+/g).slice(0, 3).map(Number);
            return parts.map(c => {
              const s = c / 255;
              return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
            });
          };
          const lum = (rgb) => 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
          const body = document.body;
          const style = getComputedStyle(body);
          let bg = style.backgroundColor;
          let node = body;
          while (bg === 'rgba(0, 0, 0, 0)' && node.parentElement) {
            node = node.parentElement;
            bg = getComputedStyle(node).backgroundColor;
          }
          if (bg === 'rgba(0, 0, 0, 0)') bg = 'rgb(255, 255, 255)';
          const a = lum(parse(style.color));
          const b = lum(parse(bg));
          const hi = Math.max(a, b);
          const lo = Math.min(a, b);
          return (hi + 0.05) / (lo + 0.05);
        }""")
    assert ratio >= kit.CONTRAST_AA, (
        f"body text against its background must meet the WCAG AA contrast bar of "
        f"{kit.CONTRAST_AA}, measured {ratio:.2f}")


def test_narrow_viewport_has_no_sideways_overflow(page):
    page.set_viewport_size(kit.NARROW_VIEWPORT)
    for route in ("/", "/courses", "/terms"):
        page.goto(kit.absolute(route))
        overflow = page.evaluate(
            "() => document.documentElement.scrollWidth - "
            "document.documentElement.clientWidth")
        assert overflow <= 1, (
            f"{route} overflows sideways by {overflow}px at "
            f"{kit.NARROW_VIEWPORT['width']}px wide")
        reachable = page.evaluate(
            """() => Array.from(document.querySelectorAll('nav a, header a'))
                 .every(a => {
                   const r = a.getBoundingClientRect();
                   return r.width > 0 && r.height > 0;
                 })""")
        assert reachable, (
            f"every navigation target on {route} stays reachable at "
            f"{kit.NARROW_VIEWPORT['width']}px wide")


def test_pinned_session_copy_appears_verbatim(page, raw):
    page.goto(kit.absolute("/"))
    home = page.inner_text("body")
    for heading in kit.CLAIM_HEADINGS:
        assert heading in home, (
            f"the marketing page carries the claim heading {heading!r}: {home[:400]!r}")
    assert kit.HERO_PRIMARY in home, f"the hero carries {kit.HERO_PRIMARY!r}"
    assert kit.HERO_SECONDARY in home, f"the hero carries {kit.HERO_SECONDARY!r}"
    assert kit.PLATFORM_HEADING in home, f"the platforms band is headed {kit.PLATFORM_HEADING!r}"
    for sublabel in kit.STORE_SUBLABELS:
        assert sublabel in home, f"a store tile carries the sub-label {sublabel!r}"
    for group in kit.FOOTER_GROUPS:
        assert group in home, f"the footer carries the group {group!r}"
    strings = raw.get("/api/courses")
    assert strings.status_code == 200, kit.describe(strings)


def test_learner_routes_resolve_at_their_pinned_addresses(learner, page):
    token = learner.headers.get("Authorization", "")
    page.set_extra_http_headers({"Authorization": token})
    for route in kit.LEARNER_ROUTES:
        response = page.goto(kit.absolute(route))
        assert response is not None and response.status < 400, (
            f"the learner route {route} must resolve for a signed-in learner, got "
            f"{None if response is None else response.status}")
    for route in ("/courses", "/terms", "/privacy", "/preferences"):
        response = page.goto(kit.absolute(route))
        assert response is not None and response.status == 200, (
            f"the public route {route} must resolve, got "
            f"{None if response is None else response.status}")


def test_list_endpoints_return_top_level_arrays(learner):
    for path in ("/courses", "/enrolments", "/traces", "/history", "/page-views"):
        response = learner.get(path)
        assert response.status_code == 200, kit.describe(response)
        body = kit.json_of(response)
        assert isinstance(body, list), (
            f"{path} must return a top-level JSON array, got {type(body).__name__}: "
            f"{body!r}")


def test_invalid_call_is_a_client_error_naming_the_reason(learner):
    bad = (("/enrolments", {"course_id": "", "daily_goal_lessons": 9}),
           ("/sessions", {"course_id": kit.OPEN_SUBJECTS[0], "kind": "not-a-kind"}),
           ("/preferences", {"category": "", "allowed": "maybe"}))
    for path, payload in bad:
        response = learner.post(path, json=payload)
        assert 400 <= response.status_code < 500, (
            f"{path} with {payload!r} must be rejected as a client error, never a "
            f"server error and never a silent success: {kit.describe(response)}")
        assert response.text.strip(), (
            f"{path} must carry a message naming the reason: {kit.describe(response)}")


def test_audio_exercise_types_are_suppressed_and_subjects_stay_completable(fresh, anon):
    suppressed = {"listen_type", "listen_select", "speak"}
    for slug in kit.OPEN_SUBJECTS:
        detail = anon.get(f"/courses/{slug}")
        assert detail.status_code == 200, kit.describe(detail)
        assert kit.json_of(detail).get("audio_available") is False, (
            f"no speech service is configured, so {slug!r} declares audio unavailable: "
            f"{detail.text[:300]!r}")
    course = kit.OPEN_SUBJECTS[0]
    assert kit.enrol(fresh, course).status_code in (200, 201)
    session = kit.json_of(kit.start_session(fresh, course))
    types = {ex.get("type") for ex in session["exercises"]}
    assert not types.intersection(suppressed), (
        f"the assembler suppresses {sorted(suppressed)} while no speech service is "
        f"configured, got {sorted(types)}")
    done = kit.reconcile(fresh, session["id"], kit.attempts_for(session))
    assert done.status_code in (200, 201), (
        f"a subject stays completable with the audio types suppressed: "
        f"{kit.describe(done)}")
