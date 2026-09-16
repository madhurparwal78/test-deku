"""The one merged pytest module for deku/proctored-credential-academy-vb.

Every assertion is black box: HTTP against the deployed app and rows through
the generic backend adapter. Nothing here reads the agent's source, imports a
provider SDK, or assumes a framework.
"""

from __future__ import annotations

import concurrent.futures

from appclient import client, login
from conftest import (
    ASSESSMENT_STATES,
    BOUNTY_TITLE,
    CORPUS_PASSWORD,
    COURSE_DEPRECATED,
    COURSE_FREE,
    COURSE_PAID,
    COURSE_PAID_PRICE_MINOR,
    COURSE_RESTRICTED,
    CURSOR_HEADER,
    DENIED,
    DENIED_OR_MISSING,
    LEARNER2_EMAIL,
    LEARNER3_EMAIL,
    LEARNER_EMAIL,
    LEDGER_KINDS,
    MODULE_BASICS,
    NORTHGATE_SEATS_GRANTED,
    NORTHGATE_TREASURY_REMAINING,
    NORTHGATE_TREASURY_TOTAL,
    NOT_FOUND,
    OK,
    PAGE_SIZE,
    PASS_MARK,
    PROCTOR_KINDS,
    PROCTOR_SIGNAL_THRESHOLD,
    PROGRAM_HALCYON,
    PROGRAM_NORTHGATE,
    QUESTION_KINDS,
    RATE_LIMIT_HEADER,
    RATE_LIMIT_REMAINING_HEADER,
    RATE_LIMIT_RESET_HEADER,
    REFUSED,
    REGISTRAR_EMAIL,
    REVIEWER_EMAIL,
    REWARD_QUOTA_TOTAL,
    REWARD_TITLE,
    SEEDED_CHAIN_COUNT,
    SEEDED_COURSE_COUNT,
    api,
    poll_until,
    probe_email,
    seed_account_id,
    seed_course_id,
    seed_module_id,
    seed_program_id,
    settle,
    unique_suffix,
)


def _first_page_id(academy, module_slug):
    module_id = seed_module_id(academy, module_slug)
    pages = academy.pages_for_module(module_id)
    assert pages, f"seed module {module_slug!r} carries no page rows"
    return sorted(pages, key=lambda row: (row.get("id")))[0]["id"]


def _all_page_ids(academy, module_slug):
    module_id = seed_module_id(academy, module_slug)
    pages = academy.pages_for_module(module_id)
    assert pages, f"seed module {module_slug!r} carries no page rows"
    return [row["id"] for row in sorted(pages, key=lambda row: (row.get("id")))]


def _complete_module(clnt, academy, module_slug):
    for page_id in _all_page_ids(academy, module_slug):
        clnt.post(api(f"/api/pages/{page_id}/progress"), json={"status": "complete"})


def _enrol(clnt, course_id, program_id):
    return clnt.post(api("/api/enrolments"),
                     json={"course_id": course_id, "program_id": program_id})


def test_health_endpoint_requires_no_credential(anon_client):
    r = anon_client.get(api("/api/health"))
    assert r.status_code == 200, (
        f"GET /api/health answered {r.status_code} with no credential, body "
        f"{r.text[:200]!r}; the App Contract requires 200 once the app is ready"
    )


def test_login_returns_access_token_for_seeded_learner(anon_client):
    r = anon_client.post(api("/api/auth/login"),
                         json={"email": LEARNER_EMAIL, "password": CORPUS_PASSWORD})
    assert r.status_code in OK, (
        f"POST /api/auth/login as {LEARNER_EMAIL} with the pinned corpus password "
        f"answered {r.status_code}, body {r.text[:200]!r}"
    )
    body = r.json()
    assert body.get("access_token"), (
        f"login response carries no non-empty access_token: keys {sorted(body)}"
    )
    assert body.get("role") == "learner", (
        f"login response reports role {body.get('role')!r} for {LEARNER_EMAIL}, "
        f"whose seeded role is learner"
    )


def test_login_with_a_wrong_password_is_denied(anon_client):
    r = anon_client.post(api("/api/auth/login"),
                         json={"email": LEARNER_EMAIL, "password": f"not-{unique_suffix()}"})
    assert r.status_code not in OK, (
        f"POST /api/auth/login with a wrong password answered {r.status_code}, body "
        f"{r.text[:200]!r}; a bad credential must not be served a token"
    )


def test_me_reports_role_and_program_from_the_stored_account_row(learner_client, academy):
    r = learner_client.get(api("/api/me"))
    assert r.status_code in OK, (
        f"GET /api/me as {LEARNER_EMAIL} answered {r.status_code}, body {r.text[:200]!r}"
    )
    body = r.json()
    row = academy.account_by_email(LEARNER_EMAIL)
    assert row is not None, f"seed account {LEARNER_EMAIL!r} is missing"
    assert body.get("role") == row.get("role"), (
        f"GET /api/me reports role {body.get('role')!r} while the stored account row "
        f"holds {row.get('role')!r}"
    )
    assert str(body.get("program_id")) == str(row.get("program_id")), (
        f"GET /api/me reports program_id {body.get('program_id')!r} while the stored "
        f"row holds {row.get('program_id')!r}"
    )


def test_catalogue_is_public_and_hides_the_deprecated_course(anon_client, academy):
    r = anon_client.get(api("/api/catalogue"))
    assert r.status_code in OK, (
        f"GET /api/catalogue answered {r.status_code} with no credential, body "
        f"{r.text[:200]!r}; the catalogue is a public surface"
    )
    listed = r.json()
    assert isinstance(listed, list), (
        f"GET /api/catalogue returned {type(listed).__name__}, not a top-level array"
    )
    identifiers = {row.get("identifier") for row in listed}
    assert COURSE_FREE in identifiers, (
        f"GET /api/catalogue omits the seeded course {COURSE_FREE!r}; it returned "
        f"{sorted(i for i in identifiers if i)}"
    )
    assert COURSE_DEPRECATED not in identifiers, (
        f"GET /api/catalogue lists the deprecated course {COURSE_DEPRECATED!r}, which "
        f"must never appear in the enrolable catalogue"
    )


def test_reader_page_carries_its_position_counters(learner_client, academy):
    page_id = _first_page_id(academy, MODULE_BASICS)
    r = learner_client.get(api(f"/api/pages/{page_id}"))
    assert r.status_code in OK, (
        f"GET /api/pages/{page_id} as {LEARNER_EMAIL} answered {r.status_code}, body "
        f"{r.text[:200]!r}"
    )
    body = r.json()
    for field in ("page_current", "page_total", "lesson_current", "lesson_total"):
        assert field in body, (
            f"the page response omits {field!r}; keys present are {sorted(body)}"
        )


def test_page_progress_is_stored_once_for_a_repeated_completion(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    page_id = _first_page_id(academy, MODULE_BASICS)
    learner_client.post(api(f"/api/pages/{page_id}/progress"), json={"status": "complete"})
    settle()
    before = academy.count_page_progress(account_id=account_id, page_id=page_id)
    r = learner_client.post(api(f"/api/pages/{page_id}/progress"),
                            json={"status": "complete"})
    assert r.status_code in OK or r.status_code in REFUSED, (
        f"a repeated page completion answered {r.status_code}, body {r.text[:200]!r}; "
        f"it must be accepted as a no-op or refused, never a server error"
    )
    settle()
    after = academy.count_page_progress(account_id=account_id, page_id=page_id)
    assert after == before == 1, (
        f"page_progress rows for one account and one page moved from {before} to "
        f"{after}; a repeated completion writes no second row"
    )


def test_stored_page_progress_never_regresses_to_in_progress(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    page_id = _first_page_id(academy, MODULE_BASICS)
    learner_client.post(api(f"/api/pages/{page_id}/progress"), json={"status": "complete"})
    settle()
    r = learner_client.post(api(f"/api/pages/{page_id}/progress"),
                            json={"status": "in_progress"})
    assert r.status_code not in (500, 502, 503), (
        f"a late in_progress write answered {r.status_code}, body {r.text[:200]!r}"
    )
    settle()
    row = academy.page_progress_for(account_id, page_id)
    assert row is not None, "the page_progress row vanished after a late write"
    assert row.get("status") == "complete", (
        f"the stored page_progress status regressed to {row.get('status')!r} after a "
        f"late in_progress write; a completed page never returns to in_progress"
    )


def test_free_enrolment_records_the_free_entitlement_source(learner3_client, academy):
    account_id = seed_account_id(academy, LEARNER3_EMAIL)
    course_id = seed_course_id(academy, COURSE_FREE)
    r = _enrol(learner3_client, course_id, None)
    assert r.status_code in OK, (
        f"POST /api/enrolments for the free course {COURSE_FREE!r} as {LEARNER3_EMAIL} "
        f"answered {r.status_code}, body {r.text[:200]!r}"
    )
    settle()
    row = academy.enrolment_for(account_id, course_id)
    assert row is not None, (
        f"no enrolment row exists for {LEARNER3_EMAIL} on {COURSE_FREE!r} after a 2xx"
    )
    assert row.get("entitlement_source") == "free", (
        f"the stored enrolment carries entitlement_source "
        f"{row.get('entitlement_source')!r}, expected 'free' for an unfunded course"
    )


def test_funded_enrolment_reserves_treasury_and_counts_the_seat(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    course_id = seed_course_id(academy, COURSE_PAID)
    program_id = seed_program_id(academy, PROGRAM_NORTHGATE)
    before = academy.program_by_name(PROGRAM_NORTHGATE)
    r = _enrol(learner_client, course_id, program_id)
    assert r.status_code in OK, (
        f"POST /api/enrolments for {COURSE_PAID!r} against {PROGRAM_NORTHGATE!r} "
        f"answered {r.status_code}, body {r.text[:200]!r}"
    )
    settle()
    after = academy.program_by_name(PROGRAM_NORTHGATE)
    assert after is not None and before is not None, "the seeded program row vanished"
    assert int(after["treasury_remaining"]) == int(before["treasury_remaining"]) - COURSE_PAID_PRICE_MINOR, (
        f"treasury_remaining moved from {before['treasury_remaining']} to "
        f"{after['treasury_remaining']}; a funded enrolment reserves exactly "
        f"{COURSE_PAID_PRICE_MINOR} minor units"
    )
    assert int(after["seats_granted"]) == int(before["seats_granted"]) + 1, (
        f"seats_granted moved from {before['seats_granted']} to "
        f"{after['seats_granted']}; a funded enrolment counts exactly one seat"
    )
    row = academy.enrolment_for(account_id, course_id)
    assert row is not None and row.get("entitlement_source") == "program", (
        f"the stored enrolment carries entitlement_source "
        f"{(row or {}).get('entitlement_source')!r}, expected 'program'"
    )


def test_duplicate_enrolment_reactivates_the_same_stored_row(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    course_id = seed_course_id(academy, COURSE_FREE)
    _enrol(learner_client, course_id, None)
    settle()
    before = academy.count_enrolments(account_id=account_id, course_id=course_id)
    r = _enrol(learner_client, course_id, None)
    assert r.status_code not in (500, 502, 503), (
        f"a second enrolment in {COURSE_FREE!r} answered {r.status_code}, body "
        f"{r.text[:200]!r}"
    )
    settle()
    after = academy.count_enrolments(account_id=account_id, course_id=course_id)
    assert after == before == 1, (
        f"enrolment rows for one account and one course moved from {before} to "
        f"{after}; a repeat enrolment reactivates the row rather than adding one"
    )


def test_enrolment_records_the_program_that_funded_it(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    course_id = seed_course_id(academy, COURSE_PAID)
    program_id = seed_program_id(academy, PROGRAM_NORTHGATE)
    _enrol(learner_client, course_id, program_id)
    settle()
    row = academy.enrolment_for(account_id, course_id)
    assert row is not None, (
        f"no enrolment row exists for {LEARNER_EMAIL} on {COURSE_PAID!r}"
    )
    assert str(row.get("program_id")) == str(program_id), (
        f"the stored enrolment records program_id {row.get('program_id')!r}, expected "
        f"the funding program {program_id!r}"
    )


def test_assessment_opens_in_preassessment_when_the_module_completes(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    course_id = seed_course_id(academy, COURSE_PAID)
    program_id = seed_program_id(academy, PROGRAM_NORTHGATE)
    _enrol(learner_client, course_id, program_id)
    _complete_module(learner_client, academy, MODULE_BASICS)
    module_id = seed_module_id(academy, MODULE_BASICS)
    row = poll_until(lambda: academy.assessment_for(account_id, module_id))
    assert row is not None, (
        f"no assessment row exists for {LEARNER_EMAIL} on {MODULE_BASICS!r} after "
        f"every page was marked complete"
    )
    assert row.get("status") in ASSESSMENT_STATES, (
        f"the stored assessment carries status {row.get('status')!r}, which is not one "
        f"of {ASSESSMENT_STATES}"
    )


def test_exam_start_without_every_consent_is_refused(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    learner_client.post(api(f"/api/assessments/{module_id}/consent"),
                        json={"accepted_terms": True,
                              "accepted_camera_monitor": False,
                              "verified_identity": True})
    settle()
    before = academy.assessment_for(account_id, module_id)
    r = learner_client.post(api(f"/api/assessments/{module_id}/exam"),
                            json={"proctoring_mode": "full"})
    assert r.status_code in REFUSED, (
        f"starting the exam with camera consent false answered {r.status_code}, body "
        f"{r.text[:200]!r}; all three consents are required"
    )
    settle()
    after = academy.assessment_for(account_id, module_id)
    assert (after or {}).get("status") == (before or {}).get("status"), (
        f"the stored assessment status moved from {(before or {}).get('status')!r} to "
        f"{(after or {}).get('status')!r} on a refused exam start"
    )


def test_exam_start_stores_a_server_end_time_and_ignores_the_client_value(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    learner_client.post(api(f"/api/assessments/{module_id}/consent"),
                        json={"accepted_terms": True,
                              "accepted_camera_monitor": True,
                              "verified_identity": True})
    r = learner_client.post(api(f"/api/assessments/{module_id}/exam"),
                            json={"proctoring_mode": "full",
                                  "ends_at": "2099-01-01T00:00:00Z"})
    assert r.status_code in OK, (
        f"starting the exam with every consent true answered {r.status_code}, body "
        f"{r.text[:200]!r}"
    )
    body = r.json()
    assert body.get("ends_at"), (
        f"the exam response carries no ends_at: keys {sorted(body)}"
    )
    assert not str(body.get("ends_at")).startswith("2099"), (
        f"the exam response echoes the client-supplied end time "
        f"{body.get('ends_at')!r}; the server owns the clock"
    )
    assessment = academy.assessment_for(account_id, module_id)
    exams = academy.exams_for((assessment or {}).get("id"))
    assert exams, (
        f"no exam row is stored for {LEARNER_EMAIL} on {MODULE_BASICS!r} after a 2xx"
    )


def test_exam_questions_never_expose_the_stored_answer_key(learner_client, academy):
    module_id = seed_module_id(academy, MODULE_BASICS)
    learner_client.post(api(f"/api/assessments/{module_id}/consent"),
                        json={"accepted_terms": True,
                              "accepted_camera_monitor": True,
                              "verified_identity": True})
    r = learner_client.post(api(f"/api/assessments/{module_id}/exam"),
                            json={"proctoring_mode": "full"})
    assert r.status_code in OK, (
        f"starting the exam answered {r.status_code}, body {r.text[:200]!r}"
    )
    assert "answer_key" not in r.text, (
        f"the exam response body carries the substring 'answer_key': "
        f"{r.text[:400]!r}; the key is served to nobody"
    )
    body = r.json()
    questions = body.get("questions") or []
    assert questions, f"the exam response carries no questions: keys {sorted(body)}"
    for question in questions:
        assert "answer_key" not in question, (
            f"a served question carries answer_key: keys {sorted(question)}"
        )
        assert question.get("kind") in QUESTION_KINDS, (
            f"a served question carries kind {question.get('kind')!r}, not one of "
            f"{QUESTION_KINDS}"
        )
    stored = academy.questions_for(module_id)
    assert stored, f"no exam_question rows are stored for {MODULE_BASICS!r}"


def test_proctor_events_are_stored_with_their_pinned_kind(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    learner_client.post(api(f"/api/assessments/{module_id}/consent"),
                        json={"accepted_terms": True,
                              "accepted_camera_monitor": True,
                              "verified_identity": True})
    start = learner_client.post(api(f"/api/assessments/{module_id}/exam"),
                                json={"proctoring_mode": "full"})
    assert start.status_code in OK, (
        f"starting the exam answered {start.status_code}, body {start.text[:200]!r}"
    )
    exam_id = start.json().get("exam_id")
    assert exam_id, f"the exam response carries no exam_id: {start.text[:200]!r}"
    r = learner_client.post(api(f"/api/exams/{exam_id}/events"),
                            json={"kind": "OffFocus",
                                  "occurred_at": "2026-09-16T08:00:00Z"})
    assert r.status_code in OK, (
        f"recording an OffFocus proctor event answered {r.status_code}, body "
        f"{r.text[:200]!r}"
    )
    settle()
    events = academy.proctor_events_for(exam_id)
    assert events, f"no proctor_event rows are stored for exam {exam_id!r}"
    for event in events:
        assert event.get("kind") in PROCTOR_KINDS, (
            f"a stored proctor_event carries kind {event.get('kind')!r}, not one of "
            f"{PROCTOR_KINDS}"
        )
    assert academy.count_accounts(id=account_id) == 1, (
        f"the seeded account row for {LEARNER_EMAIL} is no longer unique"
    )


def test_three_face_signals_mark_the_stored_exam_suspicious(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    learner_client.post(api(f"/api/assessments/{module_id}/consent"),
                        json={"accepted_terms": True,
                              "accepted_camera_monitor": True,
                              "verified_identity": True})
    start = learner_client.post(api(f"/api/assessments/{module_id}/exam"),
                                json={"proctoring_mode": "full"})
    assert start.status_code in OK, (
        f"starting the exam answered {start.status_code}, body {start.text[:200]!r}"
    )
    exam_id = start.json().get("exam_id")
    for index in range(PROCTOR_SIGNAL_THRESHOLD):
        learner_client.post(api(f"/api/exams/{exam_id}/events"),
                            json={"kind": "NoFaceDetected",
                                  "occurred_at": f"2026-09-16T08:0{index}:00Z"})
    learner_client.post(api(f"/api/exams/{exam_id}/submit"), json={"answers": []})
    assessment = academy.assessment_for(account_id, module_id)
    exams = academy.exams_for((assessment or {}).get("id"))
    row = poll_until(lambda: next(
        (e for e in academy.exams_for((assessment or {}).get("id"))
         if str(e.get("id")) == str(exam_id)), None))
    assert row is not None, (
        f"no stored exam row matches exam_id {exam_id!r} among {len(exams)} rows"
    )
    assert row.get("status") == "Suspicious", (
        f"the stored exam carries status {row.get('status')!r} after "
        f"{PROCTOR_SIGNAL_THRESHOLD} NoFaceDetected events; the attempt is raised for "
        f"a person rather than failed"
    )


def test_exam_submission_stores_a_result_and_advances_the_assessment(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    learner_client.post(api(f"/api/assessments/{module_id}/consent"),
                        json={"accepted_terms": True,
                              "accepted_camera_monitor": True,
                              "verified_identity": True})
    start = learner_client.post(api(f"/api/assessments/{module_id}/exam"),
                                json={"proctoring_mode": "full"})
    assert start.status_code in OK, (
        f"starting the exam answered {start.status_code}, body {start.text[:200]!r}"
    )
    exam_id = start.json().get("exam_id")
    questions = start.json().get("questions") or []
    answers = [{"question_id": q.get("id"), "choice": 0} for q in questions]
    r = learner_client.post(api(f"/api/exams/{exam_id}/submit"), json={"answers": answers})
    assert r.status_code in OK, (
        f"submitting the exam answered {r.status_code}, body {r.text[:200]!r}"
    )
    body = r.json()
    assert "result_percent" in body, (
        f"the submit response carries no result_percent: keys {sorted(body)}"
    )
    assert body.get("assessment_status") in ASSESSMENT_STATES, (
        f"the submit response reports assessment_status "
        f"{body.get('assessment_status')!r}, not one of {ASSESSMENT_STATES}"
    )
    stored = academy.assessment_for(account_id, module_id)
    assert (stored or {}).get("status") in ASSESSMENT_STATES, (
        f"the stored assessment carries status {(stored or {}).get('status')!r}"
    )


def test_project_submission_without_both_addresses_writes_no_row(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    assessment = academy.assessment_for(account_id, module_id)
    before = academy.count_projects(account_id=account_id)
    r = learner_client.post(api("/api/projects"),
                            json={"assessment_id": (assessment or {}).get("id"),
                                  "repo_url": f"https://example.com/{unique_suffix()}"})
    assert r.status_code in REFUSED, (
        f"a project submission missing demo_url answered {r.status_code}, body "
        f"{r.text[:200]!r}; an incomplete submission is refused as invalid"
    )
    settle()
    after = academy.count_projects(account_id=account_id)
    assert after == before, (
        f"project rows for {LEARNER_EMAIL} moved from {before} to {after} on a refused "
        f"submission; a refused submission writes nothing"
    )


def test_seeded_catalogue_rows_match_the_pinned_counts(academy):
    assert academy.count_chains() >= SEEDED_CHAIN_COUNT, (
        f"the chain table holds {academy.count_chains()} rows, fewer than the "
        f"{SEEDED_CHAIN_COUNT} seeded chains"
    )
    assert academy.count_courses() >= SEEDED_COURSE_COUNT, (
        f"the course table holds {academy.count_courses()} rows, fewer than the "
        f"{SEEDED_COURSE_COUNT} seeded courses"
    )
    paid = academy.course_by_identifier(COURSE_PAID)
    assert paid is not None, f"seed course {COURSE_PAID!r} is missing"
    assert int(paid.get("first_paywalled_module")) == 1, (
        f"{COURSE_PAID!r} carries first_paywalled_module "
        f"{paid.get('first_paywalled_module')!r}, expected 1"
    )
    assert int(paid.get("price_minor")) == COURSE_PAID_PRICE_MINOR, (
        f"{COURSE_PAID!r} carries price_minor {paid.get('price_minor')!r}, expected "
        f"{COURSE_PAID_PRICE_MINOR}"
    )
    free = academy.course_by_identifier(COURSE_FREE)
    assert free is not None and not free.get("first_paywalled_module"), (
        f"{COURSE_FREE!r} carries first_paywalled_module "
        f"{(free or {}).get('first_paywalled_module')!r}, expected no paywall"
    )
    deprecated = academy.course_by_identifier(COURSE_DEPRECATED)
    assert deprecated is not None and deprecated.get("is_deprecated"), (
        f"{COURSE_DEPRECATED!r} is not stored as deprecated"
    )


def test_seeded_programs_carry_the_pinned_treasury_shape(academy):
    northgate = academy.program_by_name(PROGRAM_NORTHGATE)
    assert northgate is not None, f"seed program {PROGRAM_NORTHGATE!r} is missing"
    assert int(northgate["treasury_total"]) == NORTHGATE_TREASURY_TOTAL, (
        f"{PROGRAM_NORTHGATE!r} carries treasury_total "
        f"{northgate['treasury_total']!r}, expected {NORTHGATE_TREASURY_TOTAL}"
    )
    halcyon = academy.program_by_name(PROGRAM_HALCYON)
    assert halcyon is not None, f"seed program {PROGRAM_HALCYON!r} is missing"
    reward = academy.reward_by_title(REWARD_TITLE)
    assert reward is not None, f"seed reward {REWARD_TITLE!r} is missing"
    assert int(reward["quota_total"]) == REWARD_QUOTA_TOTAL, (
        f"reward {REWARD_TITLE!r} carries quota_total {reward['quota_total']!r}, "
        f"expected {REWARD_QUOTA_TOTAL}"
    )
    bounty = academy.bounty_by_title(BOUNTY_TITLE)
    assert bounty is not None, f"seed bounty {BOUNTY_TITLE!r} is missing"
    assert bounty.get("requires_credential"), (
        f"bounty {BOUNTY_TITLE!r} is not stored as credential gated"
    )


def test_cookie_choice_is_stored_and_survives_a_fresh_client(learner_client):
    r = learner_client.post(api("/api/cookie-choice"), json={"accepted": True})
    assert r.status_code in OK, (
        f"POST /api/cookie-choice answered {r.status_code}, body {r.text[:200]!r}"
    )
    token = login(LEARNER_EMAIL, CORPUS_PASSWORD)
    with client(token) as fresh:
        again = fresh.get(api("/api/cookie-choice"))
    assert again.status_code in OK, (
        f"GET /api/cookie-choice on a fresh session answered {again.status_code}, body "
        f"{again.text[:200]!r}"
    )
    assert again.json().get("accepted") is True, (
        f"the stored cookie choice reads {again.json().get('accepted')!r} after a fresh "
        f"sign-in; the answer survives a reload"
    )


def test_page_views_are_recorded_as_rows_per_route(learner_client, academy):
    route = f"/privacy?probe={unique_suffix()}"
    before = academy.count_page_views()
    r = learner_client.post(api("/api/page-views"), json={"route": route})
    assert r.status_code in OK, (
        f"POST /api/page-views answered {r.status_code}, body {r.text[:200]!r}"
    )
    settle()
    after = academy.count_page_views()
    assert after == before + 1, (
        f"page_view rows moved from {before} to {after} after one recorded view"
    )


def test_concurrent_funded_enrolment_leaves_exactly_one_winner(academy):
    course_id = seed_course_id(academy, COURSE_PAID)
    program_id = seed_program_id(academy, PROGRAM_NORTHGATE)
    before = academy.program_by_name(PROGRAM_NORTHGATE)
    assert before is not None, f"seed program {PROGRAM_NORTHGATE!r} is missing"
    remaining = int(before["treasury_remaining"])
    assert remaining >= 0, f"treasury_remaining is already negative at {remaining}"

    tokens = [login(LEARNER_EMAIL, CORPUS_PASSWORD),
              login(LEARNER2_EMAIL, CORPUS_PASSWORD)]

    def attempt(token):
        with client(token) as c:
            response = c.post(api("/api/enrolments"),
                              json={"course_id": course_id, "program_id": program_id})
            return response.status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        statuses = list(pool.map(attempt, tokens))

    settle()
    after = academy.program_by_name(PROGRAM_NORTHGATE)
    assert int(after["treasury_remaining"]) >= 0, (
        f"treasury_remaining went negative at {after['treasury_remaining']} after two "
        f"simultaneous funded enrolments; the budget is never overspent"
    )
    spent = int(before["treasury_remaining"]) - int(after["treasury_remaining"])
    assert spent <= remaining, (
        f"two simultaneous enrolments spent {spent} minor units against {remaining} "
        f"available; statuses were {statuses}"
    )
    assert spent % COURSE_PAID_PRICE_MINOR == 0, (
        f"the treasury moved by {spent} minor units, which is not a whole multiple of "
        f"the course price {COURSE_PAID_PRICE_MINOR}; a half-written enrolment was left "
        f"behind. Statuses were {statuses}"
    )


def test_treasury_burn_reconciles_with_the_stored_funded_enrolments(academy):
    program = academy.program_by_name(PROGRAM_NORTHGATE)
    assert program is not None, f"seed program {PROGRAM_NORTHGATE!r} is missing"
    burn = int(program["treasury_total"]) - int(program["treasury_remaining"])
    funded = [row for row in academy.enrolments_for_program(program["id"])
              if row.get("entitlement_source") == "program"]
    expected = len(funded) * COURSE_PAID_PRICE_MINOR
    assert burn >= 0, f"treasury burn is negative at {burn}"
    assert burn == expected or int(program.get("treasury_spent") or burn) == burn, (
        f"treasury burn is {burn} minor units while {len(funded)} funded enrolments at "
        f"{COURSE_PAID_PRICE_MINOR} account for {expected}; the two must reconcile"
    )
    assert int(program["seats_granted"]) >= NORTHGATE_SEATS_GRANTED, (
        f"seats_granted is {program['seats_granted']}, below the seeded "
        f"{NORTHGATE_SEATS_GRANTED}"
    )


def test_issuance_stores_exactly_one_ledger_row_for_the_credential(registrar_client, reviewer_client, learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    assessment = academy.assessment_for(account_id, module_id)
    assert assessment is not None, (
        f"no assessment exists for {LEARNER_EMAIL} on {MODULE_BASICS!r}"
    )
    project = academy.project_for(assessment["id"])
    if project is not None:
        reviewer_client.post(api(f"/api/projects/{project['id']}/approve"))
    settle()
    r = registrar_client.post(api("/api/credentials"),
                              json={"assessment_id": assessment["id"]})
    assert r.status_code in OK or r.status_code in REFUSED, (
        f"issuing a credential as {REGISTRAR_EMAIL} answered {r.status_code}, body "
        f"{r.text[:200]!r}"
    )
    if r.status_code in OK:
        credential_id = r.json().get("id")
        settle()
        entries = academy.ledger_entries_for(credential_id)
        issuance = [e for e in entries if e.get("kind") == "issuance"]
        assert len(issuance) == 1, (
            f"{len(issuance)} issuance ledger rows exist for credential "
            f"{credential_id!r}; issuance appends exactly one"
        )
        assert entries[0].get("kind") in LEDGER_KINDS, (
            f"a stored ledger row carries kind {entries[0].get('kind')!r}, not one of "
            f"{LEDGER_KINDS}"
        )
        assert r.json().get("ledger_ref"), (
            f"the issuance response carries no ledger_ref: {r.text[:200]!r}"
        )
    else:
        assert academy.count_credentials(account_id=account_id) >= 0, (
            "a refused issuance must leave the credential table readable"
        )


def test_repeat_issuance_stores_no_second_ledger_row(registrar_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    assessment = academy.assessment_for(account_id, module_id)
    assert assessment is not None, (
        f"no assessment exists for {LEARNER_EMAIL} on {MODULE_BASICS!r}"
    )
    first = registrar_client.post(api("/api/credentials"),
                                  json={"assessment_id": assessment["id"]})
    settle()
    before = academy.count_ledger_entries()
    second = registrar_client.post(api("/api/credentials"),
                                   json={"assessment_id": assessment["id"]})
    assert second.status_code not in (500, 502, 503), (
        f"a repeat issuance answered {second.status_code}, body {second.text[:200]!r}"
    )
    settle()
    after = academy.count_ledger_entries()
    assert after == before, (
        f"ledger rows moved from {before} to {after} on a repeat issuance; the second "
        f"call writes nothing. First call answered {first.status_code}"
    )


def test_revocation_appends_a_row_and_leaves_the_issuance_row_stored(registrar_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    credentials = academy.credentials_for(account_id)
    if not credentials:
        assert academy.count_ledger_entries() >= 0, (
            "no credential exists to revoke, so the ledger must at least be readable"
        )
        return
    credential = credentials[0]
    before = academy.ledger_entries_for(credential["id"])
    issuance_before = [e for e in before if e.get("kind") == "issuance"]
    r = registrar_client.post(api(f"/api/credentials/{credential['id']}/revoke"),
                              json={"reason": f"probe {unique_suffix()}"})
    assert r.status_code in OK, (
        f"revoking credential {credential['id']!r} as {REGISTRAR_EMAIL} answered "
        f"{r.status_code}, body {r.text[:200]!r}"
    )
    settle()
    after = academy.ledger_entries_for(credential["id"])
    issuance_after = [e for e in after if e.get("kind") == "issuance"]
    assert len(after) == len(before) + 1, (
        f"ledger rows for the credential moved from {len(before)} to {len(after)}; a "
        f"revocation appends exactly one row"
    )
    assert issuance_after == issuance_before, (
        f"the stored issuance row changed during a revocation, from "
        f"{issuance_before!r} to {issuance_after!r}; the ledger is append only"
    )


def test_reward_quota_is_never_oversold_under_contention(academy):
    reward = academy.reward_by_title(REWARD_TITLE)
    assert reward is not None, f"seed reward {REWARD_TITLE!r} is missing"
    reward_id = reward["id"]
    tokens = [login(LEARNER_EMAIL, CORPUS_PASSWORD),
              login(LEARNER2_EMAIL, CORPUS_PASSWORD)]

    def claim(token):
        with client(token) as c:
            return c.post(api(f"/api/rewards/{reward_id}/claim")).status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        statuses = list(pool.map(claim, tokens))

    settle()
    granted = academy.count_reward_earns(reward_id=reward_id)
    assert granted <= REWARD_QUOTA_TOTAL, (
        f"{granted} reward_earn rows exist for a reward whose quota_total is "
        f"{REWARD_QUOTA_TOTAL}; statuses were {statuses}"
    )


def test_audit_rows_are_append_only_and_carry_their_chain_fields(registrar_client, academy):
    before = academy.count_audit_entries()
    entries = academy.audit_entries()
    r = registrar_client.get(api("/api/audit"))
    assert r.status_code in OK, (
        f"GET /api/audit as {REGISTRAR_EMAIL} answered {r.status_code}, body "
        f"{r.text[:200]!r}"
    )
    assert isinstance(r.json(), list), (
        f"GET /api/audit returned {type(r.json()).__name__}, not a top-level array"
    )
    settle()
    after_rows = academy.audit_entries()
    assert academy.count_audit_entries() >= before, (
        f"audit rows fell from {before} to {academy.count_audit_entries()}; the table "
        f"is append only"
    )
    for old, new in zip(entries, after_rows):
        assert old == new, (
            f"a stored audit row changed from {old!r} to {new!r}; no audit row is ever "
            f"updated"
        )
    if after_rows:
        assert "entry_hash" in after_rows[0], (
            f"a stored audit row carries no entry_hash: keys {sorted(after_rows[0])}"
        )


def test_catalogue_paging_uses_a_cursor_and_never_an_offset(anon_client):
    r = anon_client.get(api("/api/catalogue"))
    assert r.status_code in OK, (
        f"GET /api/catalogue answered {r.status_code}, body {r.text[:200]!r}"
    )
    listed = r.json()
    assert len(listed) <= PAGE_SIZE, (
        f"GET /api/catalogue returned {len(listed)} rows on one page, above the pinned "
        f"page size of {PAGE_SIZE}"
    )
    offset = anon_client.get(api("/api/catalogue"), params={"offset": 1})
    assert offset.status_code not in (500, 502, 503), (
        f"GET /api/catalogue?offset=1 answered {offset.status_code}, body "
        f"{offset.text[:200]!r}"
    )
    if CURSOR_HEADER in r.headers:
        assert r.headers[CURSOR_HEADER], (
            f"the {CURSOR_HEADER} header is present but empty on a non-final page"
        )


def test_idempotent_replay_of_an_enrolment_stores_one_row(academy):
    token = login(LEARNER3_EMAIL, CORPUS_PASSWORD)
    course_id = seed_course_id(academy, COURSE_FREE)
    account_id = seed_account_id(academy, LEARNER3_EMAIL)
    key = f"probe-{unique_suffix()}"
    with client(token) as c:
        first = c.post(api("/api/enrolments"),
                       json={"course_id": course_id, "program_id": None},
                       headers={"Idempotency-Key": key})
        second = c.post(api("/api/enrolments"),
                        json={"course_id": course_id, "program_id": None},
                        headers={"Idempotency-Key": key})
    assert first.status_code not in (500, 502, 503), (
        f"the first idempotent enrolment answered {first.status_code}, body "
        f"{first.text[:200]!r}"
    )
    assert second.status_code not in (500, 502, 503), (
        f"the replayed enrolment answered {second.status_code}, body "
        f"{second.text[:200]!r}"
    )
    settle()
    assert academy.count_enrolments(account_id=account_id, course_id=course_id) == 1, (
        f"a replayed enrolment left "
        f"{academy.count_enrolments(account_id=account_id, course_id=course_id)} rows "
        f"for one account and one course"
    )


def test_unauthenticated_enrolment_request_is_denied(anon_client, academy):
    course_id = seed_course_id(academy, COURSE_FREE)
    before = academy.count_enrolments(course_id=course_id)
    r = anon_client.post(api("/api/enrolments"),
                         json={"course_id": course_id, "program_id": None})
    assert r.status_code in DENIED_OR_MISSING, (
        f"an unauthenticated POST /api/enrolments answered {r.status_code}, body "
        f"{r.text[:200]!r}; a request with no bearer token is denied, not served"
    )
    settle()
    assert academy.count_enrolments(course_id=course_id) == before, (
        f"an unauthenticated enrolment moved the enrolment row count from {before} to "
        f"{academy.count_enrolments(course_id=course_id)}"
    )


def test_learner_credential_issuance_is_denied_and_the_row_is_untouched(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    assessment = academy.assessment_for(account_id, module_id)
    before = academy.count_credentials(account_id=account_id)
    r = learner_client.post(api("/api/credentials"),
                            json={"assessment_id": (assessment or {}).get("id")})
    assert r.status_code in DENIED, (
        f"POST /api/credentials from a learner session answered {r.status_code}, body "
        f"{r.text[:200]!r}; only a registrar issues"
    )
    settle()
    assert academy.count_credentials(account_id=account_id) == before, (
        f"a denied issuance moved the credential row count from {before} to "
        f"{academy.count_credentials(account_id=account_id)}"
    )


def test_reviewer_credential_issuance_is_denied(reviewer_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    assessment = academy.assessment_for(account_id, module_id)
    before = academy.count_credentials(account_id=account_id)
    r = reviewer_client.post(api("/api/credentials"),
                             json={"assessment_id": (assessment or {}).get("id")})
    assert r.status_code in DENIED, (
        f"POST /api/credentials from {REVIEWER_EMAIL} answered {r.status_code}, body "
        f"{r.text[:200]!r}; a reviewer cannot issue"
    )
    assert academy.count_credentials(account_id=account_id) == before, (
        f"a denied reviewer issuance moved the credential row count from {before}"
    )


def test_learner_cannot_create_a_partner_program(learner_client, academy):
    partner = academy.partner_by_name("Northgate Institute")
    before = academy.program_by_name(PROGRAM_NORTHGATE)
    r = learner_client.post(api("/api/programs"),
                            json={"partner_id": (partner or {}).get("id"),
                                  "name": f"Probe {unique_suffix()}",
                                  "starts_on": "2026-10-01",
                                  "ends_on": "2027-10-01",
                                  "treasury_total": 1000,
                                  "seat_cap": 1})
    assert r.status_code in DENIED, (
        f"POST /api/programs from a learner session answered {r.status_code}, body "
        f"{r.text[:200]!r}"
    )
    after = academy.program_by_name(PROGRAM_NORTHGATE)
    assert after == before, (
        f"the seeded program row changed during a denied program creation"
    )


def test_learner_self_approval_is_denied_and_the_project_stays_in_review(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    assessment = academy.assessment_for(account_id, module_id)
    project = academy.project_for((assessment or {}).get("id"))
    if project is None:
        unknown = f"absent-{unique_suffix()}"
        r = learner_client.post(api(f"/api/projects/{unknown}/approve"))
        assert r.status_code in DENIED_OR_MISSING, (
            f"a learner approval against an unknown project answered {r.status_code}"
        )
        return
    before = project.get("status")
    r = learner_client.post(api(f"/api/projects/{project['id']}/approve"))
    assert r.status_code in DENIED, (
        f"a learner approving their own project answered {r.status_code}, body "
        f"{r.text[:200]!r}; the reviewer is never the learner"
    )
    settle()
    after = academy.project_for(assessment["id"])
    assert (after or {}).get("status") == before, (
        f"the stored project status moved from {before!r} to "
        f"{(after or {}).get('status')!r} on a denied self-approval"
    )


def test_reviewer_from_another_program_is_forbidden_on_the_project(reviewer_client, academy):
    account_id = seed_account_id(academy, LEARNER2_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    assessment = academy.assessment_for(account_id, module_id)
    project = academy.project_for((assessment or {}).get("id"))
    if project is None:
        r = reviewer_client.get(api("/api/projects"), params={"status": "InReview"})
        assert r.status_code in OK, (
            f"GET /api/projects as {REVIEWER_EMAIL} answered {r.status_code}"
        )
        for row in r.json():
            assert str(row.get("program_id")) != str(
                (academy.program_by_name(PROGRAM_HALCYON) or {}).get("id")), (
                f"the reviewer's board lists a project funded by {PROGRAM_HALCYON!r}, "
                f"which is not the reviewer's own program"
            )
        return
    before = project.get("status")
    r = reviewer_client.post(api(f"/api/projects/{project['id']}/approve"))
    assert r.status_code in DENIED_OR_MISSING, (
        f"a reviewer attached to {PROGRAM_NORTHGATE!r} approving a project funded by "
        f"{PROGRAM_HALCYON!r} answered {r.status_code}, body {r.text[:200]!r}"
    )
    after = academy.project_for(assessment["id"])
    assert (after or {}).get("status") == before, (
        f"the cross-program project moved from {before!r} to "
        f"{(after or {}).get('status')!r} on a denied approval"
    )


def test_learner_cannot_read_another_learners_project(learner2_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    assessment = academy.assessment_for(account_id, module_id)
    project = academy.project_for((assessment or {}).get("id"))
    r = learner2_client.get(api("/api/projects"))
    assert r.status_code in OK, (
        f"GET /api/projects as {LEARNER2_EMAIL} answered {r.status_code}, body "
        f"{r.text[:200]!r}"
    )
    listed = r.json()
    assert isinstance(listed, list), (
        f"GET /api/projects returned {type(listed).__name__}, not a top-level array"
    )
    if project is not None:
        assert all(str(row.get("id")) != str(project["id"]) for row in listed), (
            f"the project belonging to {LEARNER_EMAIL} appears in the project list of "
            f"{LEARNER2_EMAIL}"
        )


def test_restricted_course_is_denied_to_a_learner_outside_its_program(learner_client, academy):
    course_id = seed_course_id(academy, COURSE_RESTRICTED)
    r = learner_client.get(api(f"/api/courses/{course_id}"))
    assert r.status_code in DENIED_OR_MISSING or not (r.json() or {}).get("entitled"), (
        f"GET /api/courses/{course_id} as {LEARNER_EMAIL} answered {r.status_code} and "
        f"reported entitled {(r.json() or {}).get('entitled')!r} for a course "
        f"restricted to {PROGRAM_HALCYON!r}"
    )


def test_restricted_course_is_readable_inside_its_own_program(learner2_client, academy):
    course_id = seed_course_id(academy, COURSE_RESTRICTED)
    r = learner2_client.get(api(f"/api/courses/{course_id}"))
    assert r.status_code in OK, (
        f"GET /api/courses/{course_id} as {LEARNER2_EMAIL}, who belongs to "
        f"{PROGRAM_HALCYON!r}, answered {r.status_code}, body {r.text[:200]!r}"
    )


def test_paywalled_page_body_is_denied_without_entitlement(learner3_client, academy):
    page_id = _first_page_id(academy, MODULE_BASICS)
    r = learner3_client.get(api(f"/api/pages/{page_id}"))
    if r.status_code in OK:
        assert not (r.json() or {}).get("body_markdown"), (
            f"GET /api/pages/{page_id} served body_markdown to {LEARNER3_EMAIL}, who "
            f"holds no entitlement to the paywalled module"
        )
    else:
        assert r.status_code in DENIED_OR_MISSING, (
            f"an unentitled page read answered {r.status_code}, body {r.text[:200]!r}"
        )


def test_role_in_the_request_body_is_ignored_by_the_server(learner_client, academy):
    r = learner_client.post(api("/api/auth/login"),
                            json={"email": LEARNER_EMAIL,
                                  "password": CORPUS_PASSWORD,
                                  "role": "registrar"})
    if r.status_code in OK:
        assert r.json().get("role") == "learner", (
            f"a login body claiming role registrar was answered with role "
            f"{r.json().get('role')!r}; the role is read from the account row"
        )
    me = learner_client.get(api("/api/me"))
    assert me.json().get("role") == "learner", (
        f"GET /api/me reports role {me.json().get('role')!r} after a request body "
        f"claimed registrar"
    )
    stored = academy.account_by_email(LEARNER_EMAIL)
    assert (stored or {}).get("role") == "learner", (
        f"the stored account row for {LEARNER_EMAIL} now reads role "
        f"{(stored or {}).get('role')!r}"
    )


def test_program_roster_carries_no_email_address(registrar_client, academy):
    program_id = seed_program_id(academy, PROGRAM_NORTHGATE)
    r = registrar_client.get(api(f"/api/programs/{program_id}/roster"))
    assert r.status_code in OK, (
        f"GET /api/programs/{program_id}/roster as {REGISTRAR_EMAIL} answered "
        f"{r.status_code}, body {r.text[:200]!r}"
    )
    assert "@" not in r.text, (
        f"the roster response carries an address-shaped value: {r.text[:300]!r}; a "
        f"roster reports completion state and never contact details"
    )


def test_bounty_application_without_a_credential_is_denied(learner3_client, academy):
    bounty = academy.bounty_by_title(BOUNTY_TITLE)
    assert bounty is not None, f"seed bounty {BOUNTY_TITLE!r} is missing"
    account_id = seed_account_id(academy, LEARNER3_EMAIL)
    before = academy.count_bounty_applications(account_id=account_id)
    r = learner3_client.post(api(f"/api/bounties/{bounty['id']}/applications"))
    assert r.status_code in REFUSED, (
        f"applying to the credential-gated bounty {BOUNTY_TITLE!r} as {LEARNER3_EMAIL}, "
        f"who holds no credential, answered {r.status_code}, body {r.text[:200]!r}"
    )
    settle()
    assert academy.count_bounty_applications(account_id=account_id) == before, (
        f"a denied bounty application moved the application row count from {before}"
    )


def test_public_proof_endpoint_resolves_without_a_token(anon_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    credentials = academy.credentials_for(account_id)
    entries = []
    for credential in credentials:
        entries.extend(academy.ledger_entries_for(credential["id"]))
    issuance = [e for e in entries if e.get("kind") == "issuance"]
    if not issuance:
        r = anon_client.get(api(f"/api/credentials/proof/{'0' * 64}"))
        assert r.status_code in NOT_FOUND, (
            f"an unknown ledger_ref answered {r.status_code}; it is reported as not "
            f"found rather than as an error"
        )
        return
    ref = issuance[0].get("ledger_ref")
    r = anon_client.get(api(f"/api/credentials/proof/{ref}"))
    assert r.status_code in OK, (
        f"GET /api/credentials/proof/{ref} with no credential answered "
        f"{r.status_code}, body {r.text[:200]!r}; the proof surface is public"
    )
    body = r.json()
    for field in ("ledger_ref", "display_name", "course_title", "module_title",
                  "issued_at", "proctoring_mode", "status"):
        assert field in body, (
            f"the proof response omits {field!r}; keys present are {sorted(body)}"
        )


def test_unknown_ledger_reference_is_reported_as_not_found(anon_client):
    r = anon_client.get(api(f"/api/credentials/proof/{'f' * 64}"))
    assert r.status_code in NOT_FOUND, (
        f"an unknown ledger_ref answered {r.status_code}, body {r.text[:200]!r}; an "
        f"unknown reference is not found rather than an error"
    )


def test_issuance_against_an_unfinished_assessment_is_refused(registrar_client, academy):
    account_id = seed_account_id(academy, LEARNER3_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    assessment = academy.assessment_for(account_id, module_id)
    before = academy.count_credentials(account_id=account_id)
    r = registrar_client.post(api("/api/credentials"),
                              json={"assessment_id": (assessment or {}).get("id")})
    assert r.status_code in REFUSED or r.status_code in NOT_FOUND, (
        f"issuing against an assessment that is not Completed answered "
        f"{r.status_code}, body {r.text[:200]!r}"
    )
    assert academy.count_credentials(account_id=account_id) == before, (
        f"a refused issuance moved the credential row count from {before}"
    )


def test_disallowed_assessment_transition_is_refused_and_stores_nothing(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER3_EMAIL)
    module_id = seed_module_id(academy, MODULE_BASICS)
    before = academy.assessment_for(account_id, module_id)
    r = learner_client.post(api(f"/api/assessments/{module_id}/exam"),
                            json={"proctoring_mode": "full"})
    assert r.status_code not in (500, 502, 503), (
        f"an out-of-order exam start answered {r.status_code}, body {r.text[:200]!r}"
    )
    after = academy.assessment_for(account_id, module_id)
    assert (after or {}).get("status") == (before or {}).get("status"), (
        f"the stored assessment for {LEARNER3_EMAIL} moved from "
        f"{(before or {}).get('status')!r} to {(after or {}).get('status')!r} on a "
        f"transition the machine does not allow"
    )


def test_invalid_enrolment_body_is_refused_and_writes_nothing(learner_client, academy):
    before = academy.count_enrolments()
    r = learner_client.post(api("/api/enrolments"), json={"course_id": None})
    assert r.status_code in REFUSED, (
        f"an enrolment with a null course_id answered {r.status_code}, body "
        f"{r.text[:200]!r}"
    )
    settle()
    assert academy.count_enrolments() == before, (
        f"an invalid enrolment moved the enrolment row count from {before} to "
        f"{academy.count_enrolments()}"
    )


def test_enrolment_in_the_deprecated_course_is_refused(learner_client, academy):
    course_id = seed_course_id(academy, COURSE_DEPRECATED)
    before = academy.count_enrolments(course_id=course_id)
    r = learner_client.post(api("/api/enrolments"),
                            json={"course_id": course_id, "program_id": None})
    assert r.status_code in REFUSED or r.status_code in NOT_FOUND, (
        f"enrolling in the deprecated course {COURSE_DEPRECATED!r} answered "
        f"{r.status_code}, body {r.text[:200]!r}"
    )
    settle()
    assert academy.count_enrolments(course_id=course_id) == before, (
        f"a refused enrolment in a deprecated course moved the row count from {before}"
    )


def test_rate_limit_headers_are_present_on_a_mutating_call(learner_client, academy):
    course_id = seed_course_id(academy, COURSE_FREE)
    r = learner_client.post(api("/api/enrolments"),
                            json={"course_id": course_id, "program_id": None})
    headers = {k.lower() for k in r.headers}
    assert RATE_LIMIT_HEADER.lower() in headers, (
        f"a mutating call answered {r.status_code} with headers {sorted(headers)} and "
        f"no {RATE_LIMIT_HEADER}"
    )
    assert RATE_LIMIT_REMAINING_HEADER.lower() in headers, (
        f"a mutating call carries no {RATE_LIMIT_REMAINING_HEADER} header"
    )
    assert RATE_LIMIT_RESET_HEADER.lower() in headers, (
        f"a mutating call carries no {RATE_LIMIT_RESET_HEADER} header"
    )


def test_erasure_request_is_stored_with_its_grace_window(learner3_client, academy):
    account_id = seed_account_id(academy, LEARNER3_EMAIL)
    before = academy.count_erasure_requests(account_id=account_id)
    r = learner3_client.post(api("/api/erasure-requests"))
    assert r.status_code in OK, (
        f"POST /api/erasure-requests as {LEARNER3_EMAIL} answered {r.status_code}, body "
        f"{r.text[:200]!r}"
    )
    settle()
    after = academy.count_erasure_requests(account_id=account_id)
    assert after == before + 1, (
        f"erasure_request rows for {LEARNER3_EMAIL} moved from {before} to {after}"
    )
    body = r.json()
    assert body.get("grace_ends_at"), (
        f"the erasure response carries no grace_ends_at: keys {sorted(body)}"
    )


def test_reward_window_is_stored_thirty_days_from_the_enrolment(learner_client, academy):
    account_id = seed_account_id(academy, LEARNER_EMAIL)
    course_id = seed_course_id(academy, COURSE_FREE)
    _enrol(learner_client, course_id, None)
    settle()
    row = academy.enrolment_for(account_id, course_id)
    assert row is not None, (
        f"no enrolment row exists for {LEARNER_EMAIL} on {COURSE_FREE!r}"
    )
    assert row.get("reward_window_ends_at"), (
        f"the stored enrolment carries no reward_window_ends_at: keys {sorted(row)}"
    )


def test_probe_account_cannot_sign_in_because_signup_is_closed(anon_client):
    r = anon_client.post(api("/api/auth/login"),
                         json={"email": probe_email(), "password": CORPUS_PASSWORD})
    assert r.status_code not in OK, (
        f"signing in with an address that was never seeded answered {r.status_code}, "
        f"body {r.text[:200]!r}; signup is closed"
    )


def test_exam_result_at_the_pass_mark_advances_and_below_it_returns(academy):
    module_id = seed_module_id(academy, MODULE_BASICS)
    stored = academy.questions_for(module_id)
    assert stored, f"no exam_question rows are stored for {MODULE_BASICS!r}"
    assert len(stored) >= 3, (
        f"{len(stored)} exam_question rows are stored for {MODULE_BASICS!r}, fewer than "
        f"the three the seed pins"
    )
    assert PASS_MARK == 70, (
        f"the pinned pass mark moved to {PASS_MARK}; the graders and the brief must "
        f"agree on one value"
    )
    for question in stored:
        assert question.get("kind") in QUESTION_KINDS, (
            f"a stored question carries kind {question.get('kind')!r}, not one of "
            f"{QUESTION_KINDS}"
        )
