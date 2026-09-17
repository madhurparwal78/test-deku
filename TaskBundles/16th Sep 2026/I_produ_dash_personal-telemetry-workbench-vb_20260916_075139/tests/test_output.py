"""The one pytest module for Personal Telemetry Workbench.

Every section (core features, data integrity, authorization, edge cases) and the one
declared slot (backend) are merged here. Fixtures, pinned literals and helpers live in
conftest.py; the shared grader (appclient, capabilities, _shapes) is on
PYTHONPATH=/tests from the deku-verifier-base image.

The checklist obligations each function discharges live in the pytest-provenance-v1
sidecar beside the bundle, not in a comment.

Channel disjointness, per reference/J J.12: the browser pass drives the field and its
neighbouring surfaces through their own journeys, so every check here either reads a
seeded fact no journey mutates, or works inside a per-run probe the check created
itself.
"""

from __future__ import annotations

import json
import os
import re

import httpx

import appclient
import conftest as cf


def test_health_route_answers_two_hundred() -> None:
    """The app answers its health route once it is ready."""
    with appclient.client(None) as client:
        response = client.get("/health")
    assert response.status_code == 200, cf.describe(
        response, "the health route must answer 200 once the app is ready")


def test_owner_signs_in_and_receives_a_bearer_token() -> None:
    """The seeded owner signs in and the token reaches the project list."""
    token = appclient.login(cf.OWNER_EMAIL, cf.SEEDED_PASSWORD)
    assert isinstance(token, str) and token, (
        f"login for {cf.OWNER_EMAIL} must return a non-empty access token")
    with appclient.client(token) as client:
        response = client.get(cf.projects_path())
        assert response.status_code == 200, cf.describe(
            response, "the token returned by login must reach the project list")


def test_both_seeded_accounts_sign_in_with_the_pinned_password() -> None:
    """Both seeded accounts use the one corpus password."""
    for email in (cf.OWNER_EMAIL, cf.OTHER_EMAIL):
        token = appclient.login(email, cf.SEEDED_PASSWORD)
        assert token, f"{email} must sign in with the seeded password"


def test_credentials_file_is_written_at_the_app_root() -> None:
    """The seeded credentials are readable at the documented path."""
    assert os.path.isfile(cf.CREDENTIALS_FILE), (
        f"{cf.CREDENTIALS_FILE} must exist so a signed-in account can be found")
    with open(cf.CREDENTIALS_FILE, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    assert cf.OWNER_EMAIL in text, (
        f"{cf.CREDENTIALS_FILE} must name {cf.OWNER_EMAIL}, read {text[:400]}")
    assert cf.SEEDED_PASSWORD in text, (
        f"{cf.CREDENTIALS_FILE} must carry the seeded password, read {text[:400]}")


def test_reserved_directories_exist_and_are_empty() -> None:
    """The two reserved directories exist at the app root and hold nothing."""
    for path in (cf.SCREENSHOT_DIR, cf.DOWNLOAD_DIR):
        assert os.path.isdir(path), f"{path} must exist at the app root"
        assert os.listdir(path) == [], f"{path} must start empty, held {os.listdir(path)}"


def test_project_list_holds_only_the_projects_of_the_signed_in_owner(owner) -> None:
    """The project list is scoped to the workspace the caller owns."""
    slugs = [row.get("slug") for row in cf.read_all_rows(owner, cf.projects_path())]
    for slug in cf.OWNER_PROJECTS:
        assert slug in slugs, f"the project {slug} must be listed for the owner, saw {slugs}"
    assert cf.PROJECT_OUTSIDE not in slugs, (
        f"{cf.PROJECT_OUTSIDE} belongs to another workspace and must not be listed, "
        f"saw {slugs}")


def test_project_document_declares_every_structural_limit(owner) -> None:
    """Limits are declared by the product rather than discovered by hitting one."""
    limits = cf.project_document(owner, cf.PROJECT_ARCHIVE).get("limits")
    assert isinstance(limits, dict), (
        "the project document must carry a `limits` object naming every structural limit")
    for key in cf.LIMIT_KEYS:
        assert key in limits, f"the limits object must name {key}, saw {sorted(limits)}"
    assert int(limits["eventsPerRequest"]) == cf.LIMIT_EVENTS_PER_REQUEST, (
        f"eventsPerRequest must be {cf.LIMIT_EVENTS_PER_REQUEST}, "
        f"read {limits['eventsPerRequest']}")
    assert int(limits["stepsPerFunnel"]) == cf.LIMIT_STEPS_PER_FUNNEL, (
        f"stepsPerFunnel must be {cf.LIMIT_STEPS_PER_FUNNEL}, read {limits['stepsPerFunnel']}")
    assert int(limits["rowsPerQuery"]) == cf.LIMIT_ROWS_PER_QUERY, (
        f"rowsPerQuery must be {cf.LIMIT_ROWS_PER_QUERY}, read {limits['rowsPerQuery']}")


def test_privacy_page_is_readable_without_signing_in() -> None:
    """The privacy page answers to a visitor with no session."""
    response = cf.fetch_document(cf.ROUTE_PRIVACY)
    assert response.status_code == 200, cf.describe(
        response, "the privacy page must be readable without signing in")
    assert len(response.text) > 200, (
        "the privacy page must state what the workbench stores, "
        f"read {len(response.text)} characters")


def test_public_routes_declare_distinct_titles_and_descriptions() -> None:
    """Every public route carries its own title and its own description."""
    titles, descriptions = {}, {}
    for route in cf.PUBLIC_ROUTES:
        response = cf.fetch_document(route)
        assert response.status_code == 200, cf.describe(
            response, f"the public route {route} must answer")
        head = response.text
        title = re.search(r"<title[^>]*>(.*?)</title>", head, re.I | re.S)
        assert title and title.group(1).strip(), (
            f"{route} must declare a non-empty title in the document head")
        meta = re.search(
            r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"']([^\"']+)", head, re.I)
        assert meta and meta.group(1).strip(), (
            f"{route} must declare a non-empty description in the document head")
        titles[route] = title.group(1).strip()
        descriptions[route] = meta.group(1).strip()
    assert len(set(titles.values())) == len(titles), (
        f"no two public routes may share a title, read {titles}")
    assert len(set(descriptions.values())) == len(descriptions), (
        f"no two public routes may share a description, read {descriptions}")


def test_every_response_carries_the_security_headers() -> None:
    """A strict transport policy and a nosniff content-type policy on every answer."""
    response = cf.fetch_document(cf.ROUTE_LOGIN)
    for header in cf.SECURITY_HEADERS:
        assert header.lower() in {k.lower() for k in response.headers}, (
            f"{header} must be present on every response, saw {sorted(response.headers)}")
    assert response.headers.get("X-Content-Type-Options", "").lower() == "nosniff", (
        f"X-Content-Type-Options must be nosniff, read "
        f"{response.headers.get('X-Content-Type-Options')!r}")


def test_every_api_response_carries_the_rate_limit_headers(owner) -> None:
    """Three rate-limit headers travel on every API answer."""
    response = owner.get(cf.projects_path())
    assert response.status_code == 200, cf.describe(response, "the project list must answer")
    present = {k.lower() for k in response.headers}
    for header in cf.RATE_LIMIT_HEADERS:
        assert header.lower() in present, (
            f"{header} must travel on every API response, saw {sorted(response.headers)}")


def test_unknown_address_answers_not_found_with_a_way_back() -> None:
    """An address the workbench does not recognise renders its own not-found page."""
    response = httpx.get(appclient.app_url() + "/no-such-surface-here",
                         timeout=30.0, follow_redirects=False)
    assert response.status_code == 404, cf.describe(
        response, "an unknown address must answer as not found")
    body = response.text.lower()
    assert "grain" in body or "field" in body or "href" in body, (
        f"the not-found page must carry a way back to the field, read {response.text[:300]}")


def test_every_internal_link_on_a_public_route_resolves() -> None:
    """No internal link the workbench draws answers not-found."""
    seen = set()
    for route in cf.PUBLIC_ROUTES:
        page = cf.fetch_document(route)
        assert page.status_code == 200, cf.describe(page, f"{route} must answer")
        for href in re.findall(r'href=["\'](/[^"\'#?]*)', page.text):
            if href in seen or href.startswith("//"):
                continue
            seen.add(href)
            target = httpx.get(appclient.app_url() + href, timeout=30.0,
                               follow_redirects=True)
            assert target.status_code < 400, cf.describe(
                target, f"the internal link {href} drawn on {route} must resolve")
    assert seen, "a public route must draw at least one internal link"


def test_no_credential_appears_in_anything_the_browser_downloads() -> None:
    """The seeded password and the database address stay out of the client."""
    secrets = [cf.SEEDED_PASSWORD, "postgresql://", "deku-local-dev"]
    for route in cf.PUBLIC_ROUTES:
        page = cf.fetch_document(route)
        for secret in secrets:
            assert secret not in page.text, (
                f"{route} must not ship {secret!r} to the browser")
        for src in set(re.findall(r'src=["\'](/[^"\']+\.js)', page.text)):
            asset = httpx.get(appclient.app_url() + src, timeout=30.0)
            for secret in secrets:
                assert secret not in asset.text, (
                    f"the script {src} must not ship {secret!r} to the browser")


def test_an_address_under_the_api_prefix_that_is_unnamed_answers_not_found(owner) -> None:
    """The product has no surface the brief does not name."""
    response = owner.get("/no-such-resource-here")
    assert response.status_code == 404, cf.describe(
        response, "an unnamed address under the API prefix must answer as not found")


def test_signup_creates_an_account_with_an_empty_workspace() -> None:
    """A new account owns a new workspace holding no project."""
    suffix = cf.unique_suffix()
    email = cf.probe_address(suffix)
    with appclient.client(None) as anon:
        created = anon.post("/auth/signup", json={
            "email": email, "password": cf.SEEDED_PASSWORD,
            "displayName": cf.probe_name(suffix)})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "signup must create an account")
    token = appclient.login(email, cf.SEEDED_PASSWORD)
    with appclient.client(token) as fresh:
        rows = cf.read_all_rows(fresh, cf.projects_path())
    assert rows == [], (
        f"a new account must own an empty workspace, saw {[r.get('slug') for r in rows]}")


def test_a_request_with_no_token_is_denied_at_the_api(anonymous) -> None:
    """An absent token reads as not signed in."""
    response = anonymous.get(cf.projects_path())
    assert response.status_code in cf.DENIED, cf.describe(
        response, "a request with no bearer token must be denied at the API")


def test_span_total_is_identical_at_every_band(owner) -> None:
    """One span, one total, whatever magnification drew it."""
    lo, hi = cf.archive_bounds(owner)
    totals = {}
    for band in cf.BANDS:
        answer = cf.field_answer(owner, cf.PROJECT_ARCHIVE, band, lo, hi)
        assert "total" in answer, (
            f"the field answer at band {band} must carry a total, saw {sorted(answer)}")
        totals[band] = int(answer["total"])
    assert len(set(totals.values())) == 1, (
        f"one span must report one total at every band, read {totals}")


def test_field_answer_names_the_band_it_drew(owner) -> None:
    """The answer says which of the five representations it is."""
    lo, hi = cf.archive_bounds(owner)
    for band in cf.BANDS:
        answer = cf.field_answer(owner, cf.PROJECT_ARCHIVE, band, lo, hi)
        assert answer.get("band") == band, (
            f"the field answer must name the band it drew, asked {band} read "
            f"{answer.get('band')!r}")


def test_field_total_reconciles_with_the_raw_event_rows(owner) -> None:
    """The headline number is reachable back to the rows it came from."""
    lo, hi = cf.archive_bounds(owner)
    answer = cf.field_answer(owner, cf.PROJECT_ARCHIVE, cf.BAND_WEEK, lo, hi)
    rows = cf.read_all_rows(owner, cf.events_path(cf.PROJECT_ARCHIVE),
                            **{"from": lo, "to": hi})
    assert int(answer["total"]) == len(rows), (
        f"the field total {answer['total']} must equal the {len(rows)} raw event rows "
        f"in the same span")


def test_field_person_count_reconciles_with_the_raw_event_rows(owner) -> None:
    """The person count is the distinct persons of the same rows."""
    lo, hi = cf.archive_bounds(owner)
    answer = cf.field_answer(owner, cf.PROJECT_ARCHIVE, cf.BAND_SESSION, lo, hi)
    rows = cf.read_all_rows(owner, cf.events_path(cf.PROJECT_ARCHIVE),
                            **{"from": lo, "to": hi})
    distinct = {row.get("personId") for row in rows}
    assert int(answer["persons"]) == len(distinct), (
        f"the field person count {answer['persons']} must equal the {len(distinct)} "
        f"distinct persons in the same rows")


def test_field_accepts_every_bound_dimension(owner) -> None:
    """The vertical axis binds to a person, a session or a release."""
    lo, hi = cf.archive_bounds(owner)
    for dim in cf.DIMENSIONS:
        answer = cf.field_answer(owner, cf.PROJECT_ARCHIVE, cf.BAND_WEEK, lo, hi, dim=dim)
        assert "total" in answer, (
            f"the field must answer for the bound dimension {dim}, saw {sorted(answer)}")


def test_seeded_archive_holds_the_pinned_event_total(owner) -> None:
    """The archive is seeded at the size the brief pins."""
    lo, hi = cf.archive_bounds(owner)
    answer = cf.field_answer(owner, cf.PROJECT_ARCHIVE, cf.BAND_EPOCH, lo, hi)
    assert int(answer["total"]) >= cf.ARCHIVE_EVENTS, (
        f"the seeded archive must hold at least {cf.ARCHIVE_EVENTS} events, "
        f"read {answer['total']}")
    assert int(answer["persons"]) >= cf.ARCHIVE_PERSONS, (
        f"the seeded archive must hold at least {cf.ARCHIVE_PERSONS} persons, "
        f"read {answer['persons']}")


def test_seeded_event_types_carry_the_pinned_counts(owner) -> None:
    """Each of the six seeded types is present at its pinned size."""
    lo, hi = cf.archive_bounds(owner)
    for event_type, expected in cf.SEEDED_TYPE_EVENTS.items():
        answer = cf.field_answer(owner, cf.PROJECT_ARCHIVE, cf.BAND_WEEK, lo, hi,
                                 types=event_type)
        assert int(answer["total"]) >= expected, (
            f"the seeded type {event_type} must hold at least {expected} events, "
            f"read {answer['total']}")


def test_seeded_event_rows_are_stored_in_the_database(owner, backend) -> None:
    """The archive lives in the declared provider rather than in the app."""
    stored = backend.count(cf.TABLE_EVENTS)
    assert stored >= cf.ARCHIVE_EVENTS, (
        f"the declared backend must hold at least {cf.ARCHIVE_EVENTS} event rows, "
        f"counted {stored}")


def test_empty_project_reports_no_events(owner) -> None:
    """A project with no events says so rather than showing fabricated ones."""
    doc = cf.project_document(owner, cf.PROJECT_EMPTY)
    assert doc.get("slug") == cf.PROJECT_EMPTY, (
        f"the empty project must answer its own slug, read {doc.get('slug')!r}")
    rows = cf.read_rows(owner, cf.events_path(cf.PROJECT_EMPTY))
    assert rows == [], (
        f"the seeded empty project must hold no event, saw {len(rows)} rows")


def test_brushing_the_whole_archive_resolves_the_pinned_cohort(owner) -> None:
    """The signature gesture returns the number the brief pins."""
    lo, hi = cf.archive_bounds(owner)
    cohort = cf.resolve_cohort(owner, cf.PROJECT_ARCHIVE, lo, hi)
    assert int(cohort["cardinality"]) >= cf.ARCHIVE_PERSONS, (
        f"brushing the whole archive must resolve at least {cf.ARCHIVE_PERSONS} persons, "
        f"read {cohort['cardinality']}")
    assert int(cohort["eventCount"]) >= cf.ARCHIVE_EVENTS, (
        f"brushing the whole archive must count at least {cf.ARCHIVE_EVENTS} events, "
        f"read {cohort['eventCount']}")


def test_cohort_cardinality_equals_the_returned_person_list(owner) -> None:
    """The reported size is the size of the list it reports."""
    lo, hi = cf.archive_bounds(owner)
    cohort = cf.resolve_cohort(owner, cf.PROJECT_ARCHIVE, lo, hi)
    people = cohort.get("personIds")
    assert isinstance(people, list), (
        f"a resolved cohort must carry personIds, saw {sorted(cohort)}")
    assert int(cohort["cardinality"]) == len(set(people)), (
        f"the cardinality {cohort['cardinality']} must equal the {len(set(people))} "
        f"distinct persons the cohort lists")


def test_cohort_persons_equal_the_distinct_persons_in_the_raw_events(owner) -> None:
    """A cohort is a reading of the rows beneath the brushed region."""
    lo, hi = cf.archive_bounds(owner)
    cohort = cf.resolve_cohort(owner, cf.PROJECT_ARCHIVE, lo, hi,
                               types=[cf.TYPE_REPORT_EXPORTED])
    rows = cf.read_all_rows(owner, cf.events_path(cf.PROJECT_ARCHIVE),
                            **{"from": lo, "to": hi, "types": cf.TYPE_REPORT_EXPORTED})
    raw = {row.get("personId") for row in rows}
    assert set(cohort["personIds"]) == raw, (
        f"the cohort persons must equal the distinct persons in the raw rows; cohort "
        f"held {len(set(cohort['personIds']))}, rows held {len(raw)}")


def test_resolving_one_region_twice_returns_identical_numbers(owner) -> None:
    """Nothing about a resolution depends on when it was asked."""
    lo, hi = cf.archive_bounds(owner)
    first = cf.resolve_cohort(owner, cf.PROJECT_ARCHIVE, lo, hi,
                              types=[cf.TYPE_SEARCH_RUN])
    second = cf.resolve_cohort(owner, cf.PROJECT_ARCHIVE, lo, hi,
                               types=[cf.TYPE_SEARCH_RUN])
    assert int(first["cardinality"]) == int(second["cardinality"]), (
        f"one region must resolve to one cardinality, read {first['cardinality']} then "
        f"{second['cardinality']}")
    assert int(first["eventCount"]) == int(second["eventCount"]), (
        f"one region must resolve to one event count, read {first['eventCount']} then "
        f"{second['eventCount']}")


def test_cohort_narrowed_by_type_matches_the_pinned_person_count(owner) -> None:
    """Narrowing the brush by event type narrows the cohort to the pinned figure."""
    lo, hi = cf.archive_bounds(owner)
    for event_type, expected in cf.SEEDED_TYPE_PERSONS.items():
        cohort = cf.resolve_cohort(owner, cf.PROJECT_ARCHIVE, lo, hi, types=[event_type])
        assert int(cohort["cardinality"]) >= expected, (
            f"the seeded type {event_type} must reach at least {expected} persons, "
            f"read {cohort['cardinality']}")


def test_saved_cohort_states_its_recomputation_and_its_last_computation(owner) -> None:
    """A saved cohort is honest about how fresh it is."""
    lo, hi = cf.archive_bounds(owner)
    suffix = cf.unique_suffix()
    created = owner.post(cf.cohorts_path(cf.PROJECT_ARCHIVE), json={
        "name": cf.probe_name(suffix),
        "definition": {"from": lo, "to": hi, "types": [cf.TYPE_PLAN_UPGRADED]}})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a resolved cohort must be savable by name")
    body = created.json()
    assert body.get("kind") in ("static", "dynamic"), (
        f"a saved cohort must state whether the membership recomputes, read "
        f"{body.get('kind')!r}")
    assert body.get("computedAt"), (
        f"a saved cohort must state when the membership was last computed, saw "
        f"{sorted(body)}")


def test_saved_cohort_survives_a_re_read(owner) -> None:
    """A cohort saved by name is found again with the same size."""
    lo, hi = cf.archive_bounds(owner)
    suffix = cf.unique_suffix()
    name = cf.probe_name(suffix)
    created = owner.post(cf.cohorts_path(cf.PROJECT_ARCHIVE), json={
        "name": name,
        "definition": {"from": lo, "to": hi, "types": [cf.TYPE_INVITE_SENT]}})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a cohort must be savable")
    first = int(created.json().get("memberCount", -1))
    rows = cf.read_all_rows(owner, cf.cohorts_path(cf.PROJECT_ARCHIVE))
    found = cf.find_by(rows, "name", name)
    assert found is not None, (
        f"the saved cohort {name} must be listed, saw {[r.get('name') for r in rows]}")
    assert int(found.get("memberCount", -2)) == first, (
        f"a saved cohort must re-read at the size it was saved with, read "
        f"{found.get('memberCount')} against {first}")


def test_seeded_funnel_reports_the_pinned_step_counts(owner) -> None:
    """The worked funnel the brief pins is the funnel the product computes."""
    lo, hi = cf.archive_bounds(owner)
    result = cf.run_query(owner, cf.PROJECT_ARCHIVE, {
        "kind": "funnel", "steps": list(cf.FUNNEL_STEPS), "from": lo, "to": hi})
    rows = result.get("rows")
    assert isinstance(rows, list) and len(rows) == len(cf.FUNNEL_STEPS), (
        f"a three-step funnel must answer three rows, read {rows}")
    counts = [int(row.get("count", -1)) for row in rows]
    assert counts == list(cf.FUNNEL_COUNTS), (
        f"the seeded funnel must report {list(cf.FUNNEL_COUNTS)}, read {counts}")


def test_funnel_steps_never_grow_along_the_sequence(owner) -> None:
    """A funnel is ordered, so a later step can never hold more persons."""
    lo, hi = cf.archive_bounds(owner)
    result = cf.run_query(owner, cf.PROJECT_ARCHIVE, {
        "kind": "funnel", "steps": list(cf.FUNNEL_STEPS), "from": lo, "to": hi})
    counts = [int(row.get("count", -1)) for row in result["rows"]]
    for earlier, later in zip(counts, counts[1:]):
        assert later <= earlier, (
            f"an ordered funnel must never grow along the sequence, read {counts}")


def test_funnel_step_counts_reconcile_with_the_raw_events(owner) -> None:
    """Every funnel step count is reachable back to the rows beneath it."""
    lo, hi = cf.archive_bounds(owner)
    result = cf.run_query(owner, cf.PROJECT_ARCHIVE, {
        "kind": "funnel", "steps": list(cf.FUNNEL_STEPS), "from": lo, "to": hi})
    first = int(result["rows"][0].get("count", -1))
    rows = cf.read_all_rows(owner, cf.events_path(cf.PROJECT_ARCHIVE),
                            **{"from": lo, "to": hi, "types": cf.FUNNEL_STEPS[0]})
    distinct = {row.get("personId") for row in rows}
    assert first == len(distinct), (
        f"the first funnel step must equal the {len(distinct)} distinct persons holding "
        f"{cf.FUNNEL_STEPS[0]}, read {first}")


def test_funnel_conversions_keep_the_decimal_places_that_carry_a_boundary(owner) -> None:
    """A conversion is never rounded to a figure that hides a decision boundary."""
    lo, hi = cf.archive_bounds(owner)
    result = cf.run_query(owner, cf.PROJECT_ARCHIVE, {
        "kind": "funnel", "steps": list(cf.FUNNEL_STEPS), "from": lo, "to": hi})
    rendered = json.dumps(result)
    for figure in (cf.FUNNEL_SECOND_CONVERSION, cf.FUNNEL_THIRD_CONVERSION,
                   cf.FUNNEL_WHOLE_CONVERSION):
        bare = figure.rstrip("%")
        assert bare in rendered, (
            f"the funnel answer must carry the conversion {figure}, read {rendered[:400]}")


def test_every_result_carries_its_execution_provenance(owner) -> None:
    """A result with no provenance is not displayable."""
    lo, hi = cf.archive_bounds(owner)
    result = cf.run_query(owner, cf.PROJECT_ARCHIVE, {
        "kind": "trend", "series": [{"type": cf.TYPE_APP_OPENED}], "from": lo, "to": hi})
    execution = cf.execution_of(result)
    for key in cf.EXECUTION_KEYS:
        assert key in execution, (
            f"the execution object must carry {key}, saw {sorted(execution)}")


def test_execution_source_names_the_store_or_the_rollups(owner) -> None:
    """Provenance says which of the two surfaces answered."""
    lo, hi = cf.archive_bounds(owner)
    result = cf.run_query(owner, cf.PROJECT_ARCHIVE, {
        "kind": "trend", "series": [{"type": cf.TYPE_SEARCH_RUN}], "from": lo, "to": hi})
    source = cf.execution_of(result).get("source")
    assert source in cf.EXECUTION_SOURCES, (
        f"the execution source must be one of {list(cf.EXECUTION_SOURCES)}, read "
        f"{source!r}")


def test_execution_states_the_rows_it_read(owner) -> None:
    """The rows scanned is a real figure rather than a placeholder."""
    lo, hi = cf.archive_bounds(owner)
    result = cf.run_query(owner, cf.PROJECT_ARCHIVE, {
        "kind": "trend", "series": [{"type": cf.TYPE_APP_OPENED}], "from": lo, "to": hi})
    execution = cf.execution_of(result)
    assert int(execution["rowsScanned"]) > 0, (
        f"a result over a seeded archive must report the rows it read, read "
        f"{execution['rowsScanned']}")
    assert bool(execution["sampled"]) is False, (
        "a query this small must not report itself as sampled")


def test_saved_insight_result_carries_the_same_execution_shape(owner) -> None:
    """A saved analysis reports its provenance exactly as an ad hoc one does."""
    rows = cf.read_all_rows(owner, cf.insights_path(cf.PROJECT_ARCHIVE))
    found = cf.find_by(rows, "name", cf.SEEDED_INSIGHT)
    assert found is not None, (
        f"the seeded insight {cf.SEEDED_INSIGHT} must be listed, saw "
        f"{[r.get('name') for r in rows]}")
    response = owner.get(cf.insight_result_path(cf.PROJECT_ARCHIVE, found["id"]))
    assert response.status_code == 200, cf.describe(
        response, "a saved insight must answer its result")
    for key in cf.EXECUTION_KEYS:
        assert key in cf.execution_of(response.json()), (
            f"a saved insight result must carry {key} in its execution object")


def test_saved_insight_states_whether_its_range_is_frozen(owner) -> None:
    """A relative range re-evaluates, an absolute range is frozen, and both say so."""
    rows = cf.read_all_rows(owner, cf.insights_path(cf.PROJECT_ARCHIVE))
    found = cf.find_by(rows, "name", cf.SEEDED_INSIGHT)
    assert found is not None, f"the seeded insight {cf.SEEDED_INSIGHT} must be listed"
    time_range = found.get("timeRange")
    assert isinstance(time_range, dict), (
        f"a saved insight must carry a timeRange object, saw {sorted(found)}")
    assert time_range.get("kind") in ("relative", "absolute"), (
        f"a saved time range must state whether it is relative or absolute, read "
        f"{time_range.get('kind')!r}")


def test_funnel_beyond_the_step_ceiling_is_refused(owner) -> None:
    """A structural limit refuses with the limit it enforces."""
    lo, hi = cf.archive_bounds(owner)
    steps = [cf.TYPE_APP_OPENED] * (cf.LIMIT_STEPS_PER_FUNNEL + 1)
    response = owner.post(cf.query_path(cf.PROJECT_ARCHIVE), json={
        "kind": "funnel", "steps": steps, "from": lo, "to": hi})
    assert cf.is_client_error(response), cf.describe(
        response, f"a funnel beyond {cf.LIMIT_STEPS_PER_FUNNEL} steps must be refused")
    assert str(cf.LIMIT_STEPS_PER_FUNNEL) in response.text, (
        f"the refusal must name the limit {cf.LIMIT_STEPS_PER_FUNNEL}, read "
        f"{response.text[:300]}")


def test_breakdown_above_the_cardinality_ceiling_is_refused(owner) -> None:
    """A breakdown that would explode is refused with the measured count."""
    lo, hi = cf.archive_bounds(owner)
    response = owner.post(cf.query_path(cf.PROJECT_ARCHIVE), json={
        "kind": "trend", "series": [{"type": cf.TYPE_APP_OPENED}],
        "breakdown": "session_id", "from": lo, "to": hi,
        "breakdownCardinalityOverride": cf.LIMIT_BREAKDOWN_CARDINALITY + 1})
    assert cf.is_client_error(response), cf.describe(
        response, "a breakdown above the cardinality ceiling must be refused")


def test_query_above_the_projected_row_ceiling_is_refused(owner) -> None:
    """A query is refused before it runs rather than after it has read too much."""
    lo, hi = cf.archive_bounds(owner)
    response = owner.post(cf.query_path(cf.PROJECT_ARCHIVE), json={
        "kind": "trend", "series": [{"type": cf.TYPE_APP_OPENED}], "from": lo, "to": hi,
        "maxRowsScanned": 1})
    assert cf.is_client_error(response), cf.describe(
        response, "a query projected past its row budget must be refused before running")


def test_seeded_dashboard_carries_its_tiles(owner) -> None:
    """The seeded dashboard is an arrangement of real tiles."""
    rows = cf.read_all_rows(owner, cf.dashboards_path(cf.PROJECT_ARCHIVE))
    found = cf.find_by(rows, "name", cf.SEEDED_DASHBOARD)
    assert found is not None, (
        f"the seeded dashboard {cf.SEEDED_DASHBOARD} must be listed, saw "
        f"{[r.get('name') for r in rows]}")
    tiles = found.get("tiles")
    assert isinstance(tiles, list) and len(tiles) == cf.SEEDED_DASHBOARD_TILES, (
        f"the seeded dashboard must carry {cf.SEEDED_DASHBOARD_TILES} tiles, read {tiles}")


def test_list_endpoints_page_by_cursor(owner) -> None:
    """Paging is by cursor, and the envelope says whether more remains."""
    page = cf.read_envelope(owner, cf.events_path(cf.PROJECT_ARCHIVE), limit=50)
    assert len(page["data"]) <= 50, (
        f"a page must honour its limit, read {len(page['data'])} rows")
    meta = page["page"]
    assert "hasMore" in meta, f"the page object must carry hasMore, saw {sorted(meta)}"
    assert "nextCursor" in meta, (
        f"the page object must carry nextCursor, saw {sorted(meta)}")
    if meta.get("hasMore"):
        second = cf.read_envelope(owner, cf.events_path(cf.PROJECT_ARCHIVE),
                                  limit=50, cursor=meta["nextCursor"])
        first_ids = {row.get("id") for row in page["data"]}
        second_ids = {row.get("id") for row in second["data"]}
        assert not (first_ids & second_ids), (
            "a cursor must advance rather than repeat rows already returned")


def test_cursor_presented_against_another_sort_order_is_refused(owner) -> None:
    """A cursor carries its sort, so a mismatched one is refused rather than re-sorted."""
    page = cf.read_envelope(owner, cf.events_path(cf.PROJECT_ARCHIVE), limit=10,
                            sort="timestamp")
    cursor = page["page"].get("nextCursor")
    assert cursor, "a paged collection over the seeded archive must offer a cursor"
    response = owner.get(cf.events_path(cf.PROJECT_ARCHIVE),
                         params={"limit": 10, "cursor": cursor, "sort": "-timestamp"})
    assert cf.is_client_error(response), cf.describe(
        response, "a cursor against another sort order must be refused")
    assert cf.error_code(response) == "cursor_sort_mismatch", (
        f"the refusal code must be cursor_sort_mismatch, read {cf.error_code(response)!r}")


def test_ingest_accepts_the_valid_entries_and_names_every_rejection(owner) -> None:
    """One malformed entry never discards a valid entry beside it."""
    key = cf.project_document(owner, cf.PROJECT_ARCHIVE).get("ingestKey")
    assert key, "the project document must carry the ingest key of that project"
    suffix = cf.unique_suffix()
    batch = [
        {"type": cf.TYPE_APP_OPENED, "distinctId": cf.probe_distinct_id(suffix),
         "timestamp": "2026-03-14T04:12:00Z"},
        {"distinctId": cf.probe_distinct_id(suffix), "timestamp": "2026-03-14T04:13:00Z"},
        {"type": cf.TYPE_SEARCH_RUN, "distinctId": cf.probe_distinct_id(suffix),
         "timestamp": "2026-03-14T04:14:00Z"},
    ]
    response = httpx.post(cf.ingest_url(), json=batch,
                          headers={"X-Ingest-Key": str(key)}, timeout=30.0)
    assert response.status_code in cf.OK, cf.describe(
        response, "an ingest batch must answer what happened to every entry")
    body = response.json()
    assert int(body.get("accepted", -1)) == 2, (
        f"two valid entries must be accepted beside one malformed entry, read "
        f"{body.get('accepted')}")
    rejected = body.get("rejected")
    assert isinstance(rejected, list) and len(rejected) == 1, (
        f"the answer must name the one rejection, read {rejected}")


def test_ingest_rejection_carries_an_index_and_a_code(owner) -> None:
    """A rejection names which entry failed and why."""
    key = cf.project_document(owner, cf.PROJECT_ARCHIVE).get("ingestKey")
    suffix = cf.unique_suffix()
    batch = [
        {"type": cf.TYPE_APP_OPENED, "distinctId": cf.probe_distinct_id(suffix),
         "timestamp": "2026-03-14T05:00:00Z"},
        {"type": "", "distinctId": "", "timestamp": "not-a-moment"},
    ]
    response = httpx.post(cf.ingest_url(), json=batch,
                          headers={"X-Ingest-Key": str(key)}, timeout=30.0)
    assert response.status_code in cf.OK, cf.describe(
        response, "an ingest batch must answer rather than fail whole")
    rejected = response.json().get("rejected") or []
    assert rejected, "the malformed entry must be reported as a rejection"
    first = rejected[0]
    assert int(first.get("index", -1)) == 1, (
        f"the rejection must name the index of the entry that failed, read {first}")
    assert first.get("code"), f"the rejection must name a code, read {first}"


def test_ingest_batch_beyond_the_request_ceiling_is_refused(owner) -> None:
    """The batch ceiling is a declared limit rather than a discovered one."""
    key = cf.project_document(owner, cf.PROJECT_ARCHIVE).get("ingestKey")
    suffix = cf.unique_suffix()
    entry = {"type": cf.TYPE_APP_OPENED, "distinctId": cf.probe_distinct_id(suffix),
             "timestamp": "2026-03-14T06:00:00Z"}
    batch = [dict(entry) for _ in range(cf.LIMIT_EVENTS_PER_REQUEST + 1)]
    response = httpx.post(cf.ingest_url(), json=batch,
                          headers={"X-Ingest-Key": str(key)}, timeout=60.0)
    assert cf.is_client_error(response), cf.describe(
        response, f"a batch beyond {cf.LIMIT_EVENTS_PER_REQUEST} entries must be refused")


def test_one_dedupe_key_twice_leaves_one_event(owner) -> None:
    """Deduplication is by key within the window, so a retry writes nothing new."""
    key = cf.project_document(owner, cf.PROJECT_ARCHIVE).get("ingestKey")
    suffix = cf.unique_suffix()
    distinct = cf.probe_distinct_id(suffix)
    entry = {"type": cf.TYPE_PLAN_UPGRADED, "distinctId": distinct,
             "timestamp": "2026-03-14T07:00:00Z", "dedupeKey": "probe-" + suffix}
    for _ in range(2):
        response = httpx.post(cf.ingest_url(), json=[entry],
                              headers={"X-Ingest-Key": str(key)}, timeout=30.0)
        assert response.status_code in cf.OK, cf.describe(
            response, "an ingest retry must answer rather than fail")
    cf.settle()
    rows = cf.poll_until(lambda: cf.read_all_rows(
        owner, cf.events_path(cf.PROJECT_ARCHIVE), distinctId=distinct))
    assert len(rows or []) == 1, (
        f"one dedupe key inside the window must leave exactly one event, read "
        f"{len(rows or [])}")


def test_a_far_future_timestamp_is_clamped_and_flagged(owner) -> None:
    """A clock fault is recorded as a clamp rather than trusted."""
    key = cf.project_document(owner, cf.PROJECT_ARCHIVE).get("ingestKey")
    suffix = cf.unique_suffix()
    distinct = cf.probe_distinct_id(suffix)
    response = httpx.post(cf.ingest_url(), json=[{
        "type": cf.TYPE_APP_OPENED, "distinctId": distinct,
        "timestamp": "2099-01-01T00:00:00Z"}],
        headers={"X-Ingest-Key": str(key)}, timeout=30.0)
    assert response.status_code in cf.OK, cf.describe(
        response, "a far-future timestamp must be admitted with a clamp")
    rows = cf.poll_until(lambda: cf.read_all_rows(
        owner, cf.events_path(cf.PROJECT_ARCHIVE), distinctId=distinct))
    assert rows, "the clamped event must be readable back"
    assert bool(rows[0].get("clamped")) is True, (
        f"a clamped event must be flagged as clamped, read {rows[0]}")


def test_an_ancient_live_timestamp_is_refused(owner) -> None:
    """A live event dated years ago is a clock fault rather than history."""
    key = cf.project_document(owner, cf.PROJECT_ARCHIVE).get("ingestKey")
    suffix = cf.unique_suffix()
    response = httpx.post(cf.ingest_url(), json=[{
        "type": cf.TYPE_APP_OPENED, "distinctId": cf.probe_distinct_id(suffix),
        "timestamp": "1999-01-01T00:00:00Z"}],
        headers={"X-Ingest-Key": str(key)}, timeout=30.0)
    if response.status_code in cf.OK:
        rejected = response.json().get("rejected") or []
        assert rejected, (
            f"a live event dated years ago must be refused, read {response.text[:300]}")
    else:
        assert cf.is_client_error(response), cf.describe(
            response, "a live event dated years ago must be refused")


def test_an_ingest_key_naming_another_project_is_refused(owner, outsider) -> None:
    """A key admits events only to the project that issued it."""
    foreign = cf.project_document(outsider, cf.PROJECT_OUTSIDE).get("ingestKey")
    assert foreign, "the outside project must carry its own ingest key"
    suffix = cf.unique_suffix()
    response = httpx.post(
        appclient.app_url() + f"/i/v1/events?project={cf.PROJECT_ARCHIVE}",
        json=[{"type": cf.TYPE_APP_OPENED,
               "distinctId": cf.probe_distinct_id(suffix),
               "timestamp": "2026-03-14T08:00:00Z"}],
        headers={"X-Ingest-Key": str(foreign)}, timeout=30.0)
    assert cf.is_client_error(response), cf.describe(
        response, "an ingest key naming another project must be refused")
    assert cf.CODE_PROJECT_MISMATCH in response.text, (
        f"the refusal must carry {cf.CODE_PROJECT_MISMATCH}, read {response.text[:300]}")


def test_an_ingested_event_reaches_the_stored_rows(owner, backend) -> None:
    """Acceptance means a durable row rather than a number in the answer."""
    key = cf.project_document(owner, cf.PROJECT_ARCHIVE).get("ingestKey")
    before = backend.count(cf.TABLE_EVENTS)
    suffix = cf.unique_suffix()
    response = httpx.post(cf.ingest_url(), json=[{
        "type": cf.TYPE_INVITE_SENT, "distinctId": cf.probe_distinct_id(suffix),
        "timestamp": "2026-03-14T09:00:00Z"}],
        headers={"X-Ingest-Key": str(key)}, timeout=30.0)
    assert response.status_code in cf.OK, cf.describe(
        response, "the probe event must be admitted")
    after = cf.poll_until(
        lambda: backend.count(cf.TABLE_EVENTS) > before and backend.count(cf.TABLE_EVENTS))
    assert after and after > before, (
        f"an admitted event must land in the declared backend, counted {before} then "
        f"{after}")


def test_flag_evaluation_is_deterministic_for_one_person(owner) -> None:
    """The same flag and the same person always resolve to the same variant."""
    answers = set()
    for _ in range(3):
        response = owner.post(cf.evaluate_path(cf.PROJECT_ARCHIVE), json={
            "flagKey": cf.FLAG_MULTIVARIATE, "distinctId": cf.SEEDED_PERSON_IDS[0]})
        assert response.status_code in cf.CREATED, cf.describe(
            response, "an evaluation must answer a variant")
        answers.add(response.json().get("variantKey"))
    assert len(answers) == 1, (
        f"one person must resolve to one variant, read {answers}")
    assert answers.pop() in cf.FLAG_VARIANTS, (
        "the resolved variant must be one the flag declares")


def test_flag_evaluation_reason_comes_from_the_closed_set(owner) -> None:
    """The reason is an enumeration rather than free prose."""
    response = owner.post(cf.evaluate_path(cf.PROJECT_ARCHIVE), json={
        "flagKey": cf.FLAG_BOOLEAN, "distinctId": cf.SEEDED_PERSON_IDS[1]})
    assert response.status_code in cf.CREATED, cf.describe(
        response, "an evaluation must answer a reason")
    reason = response.json().get("reason")
    assert reason in cf.EVALUATION_REASONS, (
        f"the reason must be one of {list(cf.EVALUATION_REASONS)}, read {reason!r}")


def test_variant_percentages_sum_to_one_hundred(owner) -> None:
    """A multivariate flag divides the whole rather than part of it."""
    response = owner.get(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_MULTIVARIATE))
    assert response.status_code == 200, cf.describe(
        response, f"the seeded flag {cf.FLAG_MULTIVARIATE} must answer")
    variants = response.json().get("variants") or []
    total = sum(float(v.get("rolloutPercentage", 0)) for v in variants)
    assert abs(total - 100.0) < 0.001, (
        f"variant percentages must total one hundred, read {total} across "
        f"{[v.get('key') for v in variants]}")


def test_seeded_flag_declares_its_kind_and_its_default_variant(owner) -> None:
    """A flag names the kind it is and the variant it falls back to."""
    response = owner.get(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_MULTIVARIATE))
    body = response.json()
    assert body.get("kind") == "multivariate", (
        f"{cf.FLAG_MULTIVARIATE} must be multivariate, read {body.get('kind')!r}")
    assert body.get("defaultVariantKey") == cf.FLAG_DEFAULT_VARIANT, (
        f"the default variant must be {cf.FLAG_DEFAULT_VARIANT}, read "
        f"{body.get('defaultVariantKey')!r}")
    other = owner.get(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_BOOLEAN))
    assert other.json().get("kind") == "boolean", (
        f"{cf.FLAG_BOOLEAN} must be boolean, read {other.json().get('kind')!r}")


def test_blast_radius_names_the_matched_persons_and_the_window(owner) -> None:
    """The exposure is computed against current data before anything is saved."""
    response = owner.post(cf.blast_radius_path(cf.PROJECT_ARCHIVE, cf.FLAG_MULTIVARIATE),
                          json={"rolloutPercentage": 60})
    assert response.status_code in cf.CREATED, cf.describe(
        response, "a blast radius must be computed before a rollout change")
    body = response.json()
    for key in ("matchedPersons", "sharePercent", "windowDays"):
        assert key in body, (
            f"the blast radius must name {key}, saw {sorted(body)}")


def test_a_large_rollout_jump_is_refused_without_a_confirmation(owner) -> None:
    """A jump past the confirmation threshold needs the projected exposure named."""
    current = owner.get(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_MULTIVARIATE)).json()
    version = current.get("version")
    response = owner.patch(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_MULTIVARIATE),
                           json={"rolloutPercentage":
                                 float(current.get("rolloutPercentage", 0))
                                 + cf.ROLLOUT_CONFIRMATION_JUMP + 5},
                           headers={"If-Match": str(version)})
    assert cf.is_client_error(response), cf.describe(
        response, f"a rollout jump beyond {cf.ROLLOUT_CONFIRMATION_JUMP} must be refused "
                  f"without a confirmation")


def test_a_change_naming_a_stale_version_is_refused(owner) -> None:
    """A change carries the version it read, so a stale one cannot overwrite."""
    current = owner.get(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_BOOLEAN)).json()
    stale = int(current.get("version", 1)) - 1
    response = owner.patch(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_BOOLEAN),
                           json={"name": "Probe " + cf.unique_suffix()},
                           headers={"If-Match": str(stale)})
    assert response.status_code in cf.CONFLICT or cf.is_client_error(response), (
        cf.describe(response, "a change naming a stale version must be refused"))
    assert cf.error_code(response) == cf.CODE_VERSION, (
        f"the refusal code must be {cf.CODE_VERSION}, read {cf.error_code(response)!r}")


def test_a_refused_change_returns_the_current_representation(owner) -> None:
    """The caller is given what it needs to merge rather than re-read blind."""
    current = owner.get(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_BOOLEAN)).json()
    stale = int(current.get("version", 1)) - 1
    response = owner.patch(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_BOOLEAN),
                           json={"name": "Probe " + cf.unique_suffix()},
                           headers={"If-Match": str(stale)})
    detail = cf.error_body(response).get("detail") or {}
    assert detail, (
        f"a version refusal must carry the current representation, read "
        f"{response.text[:300]}")
    assert "version" in json.dumps(detail), (
        f"the refusal detail must name the current version, read {detail}")


def test_a_flag_key_cannot_be_changed_after_creation(owner) -> None:
    """Renaming a key produces a new flag rather than moving the old one."""
    current = owner.get(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_BOOLEAN)).json()
    response = owner.patch(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_BOOLEAN),
                           json={"key": "renamed-" + cf.unique_suffix()},
                           headers={"If-Match": str(current.get("version"))})
    assert cf.is_client_error(response), cf.describe(
        response, "a flag key must be refused a change after creation")
    again = owner.get(cf.flag_path(cf.PROJECT_ARCHIVE, cf.FLAG_BOOLEAN))
    assert again.status_code == 200, cf.describe(
        again, "the flag must still answer under its original key")


def test_killing_a_flag_records_the_state_it_was_killed_from(owner) -> None:
    """A kill is reversible because it remembers what it replaced."""
    suffix = cf.unique_suffix()
    created = owner.post(cf.flags_path(cf.PROJECT_ARCHIVE), json={
        "key": "probe-" + suffix, "name": cf.probe_name(suffix), "kind": "boolean",
        "rolloutPercentage": 40})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a probe flag must be creatable")
    key = created.json().get("key")
    response = owner.post(cf.kill_path(cf.PROJECT_ARCHIVE, key), json={})
    assert response.status_code in cf.CREATED, cf.describe(
        response, "a kill must answer the killed flag")
    body = response.json()
    assert body.get("state") == "killed", (
        f"a killed flag must report the killed state, read {body.get('state')!r}")
    assert body.get("killedFromState"), (
        f"a kill must record the state it killed from, saw {sorted(body)}")


def test_a_second_kill_returns_the_same_terminal_state(owner) -> None:
    """A kill is safe to repeat because a retry must never be dangerous."""
    suffix = cf.unique_suffix()
    created = owner.post(cf.flags_path(cf.PROJECT_ARCHIVE), json={
        "key": "probe-" + suffix, "name": cf.probe_name(suffix), "kind": "boolean",
        "rolloutPercentage": 20})
    key = created.json().get("key")
    first = owner.post(cf.kill_path(cf.PROJECT_ARCHIVE, key), json={})
    second = owner.post(cf.kill_path(cf.PROJECT_ARCHIVE, key), json={})
    assert second.status_code in cf.CREATED, cf.describe(
        second, "a second kill must answer rather than fail")
    assert second.json().get("state") == first.json().get("state"), (
        f"a second kill must return the same terminal state, read "
        f"{first.json().get('state')!r} then {second.json().get('state')!r}")


def test_a_kill_appends_an_audit_entry_naming_the_actor(owner) -> None:
    """Every kill leaves a record of who did it."""
    before = cf.read_rows(owner, cf.operations_path(), limit=1)
    highest = int(before[0]["sequence"]) if before else 0
    suffix = cf.unique_suffix()
    created = owner.post(cf.flags_path(cf.PROJECT_ARCHIVE), json={
        "key": "probe-" + suffix, "name": cf.probe_name(suffix), "kind": "boolean",
        "rolloutPercentage": 10})
    key = created.json().get("key")
    owner.post(cf.kill_path(cf.PROJECT_ARCHIVE, key), json={})
    cf.settle()
    fresh = cf.read_all_rows(owner, cf.operations_path(), since=highest)
    kinds = [row.get("kind") for row in fresh]
    actors = {row.get("actor") for row in fresh}
    assert fresh, f"a kill must append to the operation log, read {kinds}"
    assert any(actor for actor in actors), (
        f"an appended operation must name the actor that caused it, read {actors}")


def test_a_scheduled_change_loses_to_a_manual_edit(owner) -> None:
    """A human edit beats a machine edit whatever the order of arrival."""
    suffix = cf.unique_suffix()
    created = owner.post(cf.flags_path(cf.PROJECT_ARCHIVE), json={
        "key": "probe-" + suffix, "name": cf.probe_name(suffix), "kind": "boolean",
        "rolloutPercentage": 5})
    key = created.json().get("key")
    version = created.json().get("version")
    queued = owner.post(cf.scheduled_changes_path(cf.PROJECT_ARCHIVE, key), json={
        "applyAt": "2026-12-01T00:00:00Z", "change": {"rolloutPercentage": 30},
        "guard": {"maxErrorRate": 0.5}})
    assert queued.status_code in cf.CREATED, cf.describe(
        queued, "a scheduled change must be queueable")
    edited = owner.patch(cf.flag_path(cf.PROJECT_ARCHIVE, key),
                         json={"rolloutPercentage": 12},
                         headers={"If-Match": str(version)})
    assert edited.status_code in cf.CREATED, cf.describe(
        edited, "a manual edit must be accepted beside a queued change")
    current = owner.get(cf.flag_path(cf.PROJECT_ARCHIVE, key)).json()
    assert float(current.get("rolloutPercentage")) == 12.0, (
        f"the manual edit must hold, read {current.get('rolloutPercentage')}")


def test_the_evaluation_log_lists_the_evaluations_served(owner) -> None:
    """Evaluation is observable rather than invisible."""
    owner.post(cf.evaluate_path(cf.PROJECT_ARCHIVE), json={
        "flagKey": cf.FLAG_MULTIVARIATE, "distinctId": cf.SEEDED_PERSON_IDS[2]})
    cf.settle()
    rows = cf.read_rows(owner, cf.evaluations_path(cf.PROJECT_ARCHIVE,
                                                   cf.FLAG_MULTIVARIATE))
    assert rows, "the evaluation log must list the evaluations served"
    assert rows[0].get("variantKey"), (
        f"an evaluation row must name the variant served, read {rows[0]}")


def test_assignment_is_deterministic_from_the_salt_and_the_person(owner) -> None:
    """One person resolves to one variant everywhere the question is asked."""
    experiment = owner.get(cf.experiment_path(cf.PROJECT_ARCHIVE, cf.EXPERIMENT_KEY))
    assert experiment.status_code == 200, cf.describe(
        experiment, f"the seeded experiment {cf.EXPERIMENT_KEY} must answer")
    assert experiment.json().get("assignmentSalt") == cf.EXPERIMENT_SALT, (
        f"the assignment salt must be {cf.EXPERIMENT_SALT}, read "
        f"{experiment.json().get('assignmentSalt')!r}")
    seen = set()
    for _ in range(3):
        answer = owner.post(cf.evaluate_path(cf.PROJECT_ARCHIVE), json={
            "flagKey": cf.FLAG_MULTIVARIATE, "distinctId": cf.SEEDED_PERSON_IDS[3]})
        seen.add(answer.json().get("variantKey"))
    assert len(seen) == 1, (
        f"the assignment for one person must not move between reads, read {seen}")


def test_the_power_answer_names_the_sample_and_the_projected_days(owner) -> None:
    """The cost of a decision is stated before the experiment runs."""
    response = owner.post(cf.power_path(cf.PROJECT_ARCHIVE, cf.EXPERIMENT_KEY), json={})
    assert response.status_code in cf.CREATED, cf.describe(
        response, "a power calculation must answer before launch")
    body = response.json()
    for key in ("samplePerVariant", "projectedDays", "projectedPower"):
        assert key in body, f"the power answer must name {key}, saw {sorted(body)}"


def test_results_name_the_statistical_method_in_force(owner) -> None:
    """A result read every day says which statistic survives that."""
    response = owner.get(cf.results_path(cf.PROJECT_ARCHIVE, cf.EXPERIMENT_KEY))
    assert response.status_code == 200, cf.describe(
        response, "an experiment must answer its results")
    body = response.json()
    assert body.get("statisticalMethod"), (
        f"the results must name the method in force, saw {sorted(body)}")
    assert isinstance(body.get("variants"), list), (
        f"the results must carry a per-variant breakdown, saw {sorted(body)}")


def test_missing_exposure_refuses_a_conclusion(owner) -> None:
    """An absence is never read as a zero."""
    suffix = cf.unique_suffix()
    created = owner.post(cf.experiments_path(cf.PROJECT_ARCHIVE), json={
        "key": "probe-" + suffix, "name": cf.probe_name(suffix),
        "flagKey": cf.FLAG_MULTIVARIATE, "hypothesis": "probe",
        "primaryMetric": cf.EXPERIMENT_PRIMARY_METRIC,
        "guardrailMetrics": [cf.EXPERIMENT_GUARDRAIL_METRIC],
        "exposureEvent": "probe_exposure_" + suffix,
        "minimumDetectableEffect": 0.05})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a probe experiment must be creatable")
    response = owner.get(cf.results_path(cf.PROJECT_ARCHIVE, created.json()["key"]))
    body = response.json() if response.status_code == 200 else cf.error_body(response)
    rendered = json.dumps(body)
    assert "exposure" in rendered.lower(), (
        f"an experiment with no exposure must name the missing exposure rather than "
        f"reading absence as a zero, read {rendered[:400]}")


def test_a_repeated_ship_under_one_idempotency_key_ships_once(owner) -> None:
    """A retry of a dangerous operation is the same operation."""
    suffix = cf.unique_suffix()
    created = owner.post(cf.experiments_path(cf.PROJECT_ARCHIVE), json={
        "key": "probe-" + suffix, "name": cf.probe_name(suffix),
        "flagKey": cf.FLAG_MULTIVARIATE, "hypothesis": "probe",
        "primaryMetric": cf.EXPERIMENT_PRIMARY_METRIC,
        "guardrailMetrics": [cf.EXPERIMENT_GUARDRAIL_METRIC],
        "exposureEvent": cf.EXPERIMENT_EXPOSURE_EVENT,
        "minimumDetectableEffect": 0.05, "confirmPower": True})
    key = created.json()["key"]
    idem = "probe-" + cf.unique_suffix()
    first = owner.post(cf.ship_path(cf.PROJECT_ARCHIVE, key),
                       json={"variantKey": cf.FLAG_DEFAULT_VARIANT},
                       headers={"Idempotency-Key": idem})
    assert first.status_code in cf.CREATED, cf.describe(
        first, "shipping must answer the shipped experiment")
    second = owner.post(cf.ship_path(cf.PROJECT_ARCHIVE, key),
                        json={"variantKey": cf.FLAG_DEFAULT_VARIANT},
                        headers={"Idempotency-Key": idem})
    assert second.status_code in cf.CREATED, cf.describe(
        second, "a repeat under one idempotency key must answer the first answer")
    assert second.headers.get("Idempotency-Replayed", "").lower() == "true", (
        f"a replayed request must say so in its headers, saw {dict(second.headers)}")


def test_a_shipped_experiment_freezes_its_definition(owner) -> None:
    """A concluded result is reproducible because its inputs are frozen."""
    suffix = cf.unique_suffix()
    created = owner.post(cf.experiments_path(cf.PROJECT_ARCHIVE), json={
        "key": "probe-" + suffix, "name": cf.probe_name(suffix),
        "flagKey": cf.FLAG_MULTIVARIATE, "hypothesis": "probe",
        "primaryMetric": cf.EXPERIMENT_PRIMARY_METRIC,
        "guardrailMetrics": [cf.EXPERIMENT_GUARDRAIL_METRIC],
        "exposureEvent": cf.EXPERIMENT_EXPOSURE_EVENT,
        "minimumDetectableEffect": 0.05, "confirmPower": True})
    key = created.json()["key"]
    owner.post(cf.ship_path(cf.PROJECT_ARCHIVE, key),
               json={"variantKey": cf.FLAG_DEFAULT_VARIANT},
               headers={"Idempotency-Key": "probe-" + cf.unique_suffix()})
    cf.settle()
    body = owner.get(cf.experiment_path(cf.PROJECT_ARCHIVE, key)).json()
    assert body.get("frozenDefinition"), (
        f"a shipped experiment must freeze its definition, saw {sorted(body)}")


def test_a_launch_below_the_power_floor_is_refused(owner) -> None:
    """An underpowered launch needs the projected power acknowledged."""
    suffix = cf.unique_suffix()
    response = owner.post(cf.experiments_path(cf.PROJECT_ARCHIVE), json={
        "key": "probe-" + suffix, "name": cf.probe_name(suffix),
        "flagKey": cf.FLAG_MULTIVARIATE, "hypothesis": "probe",
        "primaryMetric": cf.EXPERIMENT_PRIMARY_METRIC,
        "guardrailMetrics": [cf.EXPERIMENT_GUARDRAIL_METRIC],
        "exposureEvent": cf.EXPERIMENT_EXPOSURE_EVENT,
        "minimumDetectableEffect": 0.0001, "launch": True})
    assert cf.is_client_error(response), cf.describe(
        response, "an underpowered launch must be refused without a confirmation")


def test_an_outsider_cannot_read_the_owner_project(outsider) -> None:
    """A workspace another account owns is answered as absent."""
    response = outsider.get(cf.project_path(cf.PROJECT_ARCHIVE))
    assert response.status_code in cf.NOT_FOUND, cf.describe(
        response, "a project in another workspace must be answered as absent")


def test_an_outsider_cannot_read_an_owner_person_by_identifier(owner, outsider) -> None:
    """A direct request naming an identifier reaches nothing either."""
    rows = cf.read_rows(owner, cf.events_path(cf.PROJECT_ARCHIVE), limit=1)
    assert rows, "the seeded archive must hold at least one event"
    person_id = rows[0].get("personId")
    response = outsider.get(cf.person_path(cf.PROJECT_ARCHIVE, str(person_id)))
    assert response.status_code in cf.NOT_FOUND, cf.describe(
        response, "a person in another workspace must be answered as absent")


def test_an_outsider_project_list_excludes_the_owner_projects(outsider) -> None:
    """The list is a projection of what the caller owns."""
    slugs = [row.get("slug") for row in cf.read_all_rows(outsider, cf.projects_path())]
    assert cf.PROJECT_OUTSIDE in slugs, (
        f"the second account must see its own project, saw {slugs}")
    for slug in cf.OWNER_PROJECTS:
        assert slug not in slugs, (
            f"{slug} belongs to another workspace and must not be listed, saw {slugs}")


def test_an_anonymous_request_is_denied_at_the_field(anonymous) -> None:
    """The field is not readable without a session."""
    response = anonymous.get(cf.field_path(cf.PROJECT_ARCHIVE))
    assert response.status_code in cf.DENIED + (404,), cf.describe(
        response, "the field must be denied to an anonymous caller")


def test_a_forged_token_reads_as_not_signed_in() -> None:
    """A token the workbench did not issue reaches nothing."""
    with appclient.client("forged-" + cf.unique_suffix()) as client:
        response = client.get(cf.projects_path())
    assert response.status_code in cf.DENIED, cf.describe(
        response, "a forged token must read as not signed in")


def test_a_scoped_key_without_the_scope_is_denied_naming_the_scope(owner) -> None:
    """A refusal tells the owner which scope to add."""
    token = cf.step_up_token(owner)
    created = owner.post(cf.keys_path(),
                         json={"kind": "personal", "scopes": ["event:read"]},
                         headers={"X-Step-Up": token})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a scoped key must be creatable behind a step-up")
    secret = created.json().get("secret")
    assert secret, "a created key must return its secret exactly once"
    with appclient.client(str(secret)) as scoped:
        response = scoped.post(cf.kill_path(cf.PROJECT_ARCHIVE, cf.FLAG_BOOLEAN), json={})
    assert cf.is_client_error(response), cf.describe(
        response, "a key without flag:write must be denied the kill")
    assert cf.error_code(response) == cf.CODE_SCOPE, (
        f"the refusal code must be {cf.CODE_SCOPE}, read {cf.error_code(response)!r}")


def test_a_scoped_key_cannot_erase_a_person(owner) -> None:
    """Erasure is never reachable by a credential, whatever scopes it holds."""
    token = cf.step_up_token(owner)
    created = owner.post(cf.keys_path(),
                         json={"kind": "personal", "scopes": list(cf.KEY_SCOPES)},
                         headers={"X-Step-Up": token})
    secret = created.json().get("secret")
    rows = cf.read_rows(owner, cf.events_path(cf.PROJECT_ARCHIVE), limit=1)
    person_id = str(rows[0].get("personId"))
    with appclient.client(str(secret)) as scoped:
        response = scoped.post(cf.erase_path(cf.PROJECT_ARCHIVE, person_id),
                               json={"legalBasis": "probe"})
    assert cf.is_client_error(response), cf.describe(
        response, "a key must be denied erasing a person")


def test_a_scoped_key_cannot_create_another_key(owner) -> None:
    """A credential never mints a credential."""
    token = cf.step_up_token(owner)
    created = owner.post(cf.keys_path(),
                         json={"kind": "personal", "scopes": list(cf.KEY_SCOPES)},
                         headers={"X-Step-Up": token})
    secret = created.json().get("secret")
    with appclient.client(str(secret)) as scoped:
        response = scoped.post(cf.keys_path(),
                               json={"kind": "personal", "scopes": ["event:read"]})
    assert cf.is_client_error(response), cf.describe(
        response, "a key must be denied creating another key")


def test_an_erasure_without_a_step_up_is_denied(owner) -> None:
    """The most destructive action asks who is asking."""
    rows = cf.read_rows(owner, cf.events_path(cf.PROJECT_ARCHIVE), limit=1)
    person_id = str(rows[0].get("personId"))
    response = owner.post(cf.erase_path(cf.PROJECT_ARCHIVE, person_id),
                          json={"legalBasis": "probe"})
    assert cf.is_client_error(response), cf.describe(
        response, "an erasure without a step-up must be denied")


def test_a_held_workspace_refuses_a_kill_naming_the_held_state(owner) -> None:
    """A dangerous operation is refused rather than queued."""
    held = owner.put(cf.held_path(), json={"held": True})
    assert held.status_code in cf.OK, cf.describe(
        held, "the workspace must be holdable")
    try:
        response = owner.post(cf.kill_path(cf.PROJECT_ARCHIVE, cf.FLAG_BOOLEAN), json={})
        assert cf.is_client_error(response), cf.describe(
            response, "a kill must be refused while the workspace is held")
        assert cf.error_code(response) == cf.CODE_HELD, (
            f"the refusal code must be {cf.CODE_HELD}, read {cf.error_code(response)!r}")
        pending = cf.read_rows(owner, cf.pending_path())
        kinds = [row.get("kind") for row in pending]
        assert "flag_kill" not in kinds, (
            f"a kill must never be recorded as pending work, read {kinds}")
    finally:
        owner.put(cf.held_path(), json={"held": False})


def test_a_held_workspace_records_an_authoring_write_as_pending(owner) -> None:
    """Authoring continues while publishing does not."""
    lo, hi = cf.archive_bounds(owner)
    suffix = cf.unique_suffix()
    owner.put(cf.held_path(), json={"held": True})
    try:
        created = owner.post(cf.cohorts_path(cf.PROJECT_ARCHIVE), json={
            "name": cf.probe_name(suffix),
            "definition": {"from": lo, "to": hi, "types": [cf.TYPE_APP_OPENED]}})
        assert created.status_code in cf.OK, cf.describe(
            created, "authoring must continue while the workspace is held")
        pending = cf.read_rows(owner, cf.pending_path())
        assert pending, "an authoring write during a hold must appear as pending work"
    finally:
        owner.put(cf.held_path(), json={"held": False})


def test_releasing_the_hold_applies_the_pending_work(owner) -> None:
    """The pending ladder empties in order on release."""
    lo, hi = cf.archive_bounds(owner)
    suffix = cf.unique_suffix()
    name = cf.probe_name(suffix)
    owner.put(cf.held_path(), json={"held": True})
    owner.post(cf.cohorts_path(cf.PROJECT_ARCHIVE), json={
        "name": name, "definition": {"from": lo, "to": hi,
                                     "types": [cf.TYPE_SEARCH_RUN]}})
    released = owner.post(cf.release_hold_path(), json={})
    assert released.status_code in cf.OK, cf.describe(
        released, "releasing the hold must apply the pending work")
    owner.put(cf.held_path(), json={"held": False})
    remaining = cf.read_rows(owner, cf.pending_path())
    assert remaining == [], (
        f"released pending work must leave the pending list empty, read "
        f"{[r.get('kind') for r in remaining]}")
    rows = cf.read_all_rows(owner, cf.cohorts_path(cf.PROJECT_ARCHIVE))
    assert cf.find_by(rows, "name", name) is not None, (
        f"the cohort authored during the hold must exist after release, saw "
        f"{[r.get('name') for r in rows][:8]}")


def test_a_conflict_row_keeps_both_values_and_the_rule(owner) -> None:
    """Resolution is automatic, recorded and reversible."""
    response = owner.get(cf.conflicts_path())
    assert response.status_code == 200, cf.describe(
        response, "the conflict history must answer")
    payload = response.json()
    rows = payload.get("data") if isinstance(payload, dict) else payload
    assert isinstance(rows, list), (
        f"the conflict history must answer a list of resolutions, read {payload}")
    for row in rows:
        for key in ("winningValue", "losingValue", "ruleApplied", "restorableUntil"):
            assert key in row, (
                f"a conflict row must carry {key}, saw {sorted(row)}")


def test_the_processing_answer_names_the_capabilities_it_withdraws(owner) -> None:
    """The switch states the loss before it is enabled."""
    response = owner.get(cf.processing_path())
    assert response.status_code == 200, cf.describe(
        response, "the processing policy must answer")
    body = response.json()
    assert "localOnly" in body, (
        f"the processing answer must carry localOnly, saw {sorted(body)}")
    disabled = body.get("disabledCapabilities")
    assert isinstance(disabled, list), (
        f"the processing answer must name disabledCapabilities, saw {sorted(body)}")
    for capability in cf.DISABLED_CAPABILITIES:
        assert capability in disabled, (
            f"the switch must name {capability} among the capabilities it withdraws, "
            f"read {disabled}")


def test_a_disabled_capability_is_refused_naming_the_switch(owner) -> None:
    """With the switch on, a withdrawn capability is refused rather than weakened."""
    owner.put(cf.processing_path(), json={"localOnly": True})
    try:
        rows = cf.read_rows(owner, cf.destinations_path(cf.PROJECT_ARCHIVE))
        target = cf.find_by(rows, "name", cf.DESTINATION_HEALTHY) or (rows[0] if rows else None)
        assert target is not None, "the seeded destinations must be listed"
        response = owner.post(cf.replay_path(cf.PROJECT_ARCHIVE, str(target["id"])),
                              json={})
        assert cf.is_client_error(response), cf.describe(
            response, "a withdrawn capability must be refused while the switch is on")
        assert cf.error_code(response) == cf.CODE_LOCAL_ONLY, (
            f"the refusal code must be {cf.CODE_LOCAL_ONLY}, read "
            f"{cf.error_code(response)!r}")
    finally:
        owner.put(cf.processing_path(), json={"localOnly": False})


def test_a_share_token_is_returned_once_at_creation(owner) -> None:
    """The workbench stores a digest rather than the token."""
    rows = cf.read_all_rows(owner, cf.insights_path(cf.PROJECT_ARCHIVE))
    insight = cf.find_by(rows, "name", cf.SEEDED_INSIGHT)
    assert insight is not None, f"the seeded insight {cf.SEEDED_INSIGHT} must be listed"
    created = owner.post(cf.shares_path(cf.PROJECT_ARCHIVE), json={
        "resourceType": "insight", "resourceId": insight["id"]})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a share must be mintable on a saved insight")
    body = created.json()
    token = body.get("token")
    assert token, f"a minted share must return its token once, saw {sorted(body)}"
    again = owner.get(cf.share_path(cf.PROJECT_ARCHIVE, str(body["id"])))
    assert token not in again.text, (
        "a share re-read must never show the raw token a second time")


def test_a_share_read_returns_only_the_scoped_artefact(owner) -> None:
    """The recipient sees the one thing the token names."""
    rows = cf.read_all_rows(owner, cf.insights_path(cf.PROJECT_ARCHIVE))
    insight = cf.find_by(rows, "name", cf.SEEDED_INSIGHT)
    created = owner.post(cf.shares_path(cf.PROJECT_ARCHIVE), json={
        "resourceType": "insight", "resourceId": insight["id"]})
    token = created.json()["token"]
    with appclient.client(None) as anon:
        response = anon.get(cf.public_share_path(str(token)))
    assert response.status_code == 200, cf.describe(
        response, "a valid share token must answer its artefact")
    rendered = json.dumps(response.json())
    assert cf.WORKSPACE_OWNER not in rendered or "attribution" in rendered.lower(), (
        "a share answer must not leak workspace-level context beyond the attribution")


def test_a_share_defaults_to_the_most_restrictive_scope(owner) -> None:
    """The sheet opens closed and the owner widens deliberately."""
    rows = cf.read_all_rows(owner, cf.insights_path(cf.PROJECT_ARCHIVE))
    insight = cf.find_by(rows, "name", cf.SEEDED_INSIGHT)
    created = owner.post(cf.shares_path(cf.PROJECT_ARCHIVE), json={
        "resourceType": "insight", "resourceId": insight["id"]})
    scope = created.json().get("scope") or {}
    assert scope.get("allowDrillDown") in (False, None), (
        f"a default share must not allow drilling down, read {scope}")
    assert scope.get("allowPersonIdentifiers") in (False, None), (
        f"a default share must not expose person identifiers, read {scope}")


def test_a_request_outside_the_share_scope_is_forbidden(owner) -> None:
    """A bounded token stays bounded."""
    rows = cf.read_all_rows(owner, cf.insights_path(cf.PROJECT_ARCHIVE))
    insight = cf.find_by(rows, "name", cf.SEEDED_INSIGHT)
    created = owner.post(cf.shares_path(cf.PROJECT_ARCHIVE), json={
        "resourceType": "insight", "resourceId": insight["id"]})
    token = created.json()["token"]
    with appclient.client(None) as anon:
        response = anon.get(cf.public_share_path(str(token)) + "/persons/"
                            + cf.SEEDED_PERSON_IDS[0])
    assert response.status_code in cf.NOT_FOUND, cf.describe(
        response, "a request outside a share scope must be refused")


def test_a_revoked_token_and_an_unknown_token_answer_identically(owner) -> None:
    """Revoked, expired and never-existed are one answer."""
    rows = cf.read_all_rows(owner, cf.insights_path(cf.PROJECT_ARCHIVE))
    insight = cf.find_by(rows, "name", cf.SEEDED_INSIGHT)
    created = owner.post(cf.shares_path(cf.PROJECT_ARCHIVE), json={
        "resourceType": "insight", "resourceId": insight["id"]})
    token = created.json()["token"]
    revoked = owner.delete(cf.share_path(cf.PROJECT_ARCHIVE, str(created.json()["id"])))
    assert revoked.status_code in cf.OK, cf.describe(
        revoked, "a share must be revocable")
    with appclient.client(None) as anon:
        after = anon.get(cf.public_share_path(str(token)))
        unknown = anon.get(cf.public_share_path("unknown-" + cf.unique_suffix()))
    assert after.status_code == unknown.status_code, (
        f"a revoked token must answer exactly as an unknown one, read "
        f"{after.status_code} against {unknown.status_code}")
    assert cf.error_code(after) == cf.error_code(unknown), (
        f"a revoked token must carry the same code as an unknown one, read "
        f"{cf.error_code(after)!r} against {cf.error_code(unknown)!r}")


def test_a_share_row_records_its_access_count(owner) -> None:
    """The owner can see how often a link was opened."""
    rows = cf.read_all_rows(owner, cf.insights_path(cf.PROJECT_ARCHIVE))
    insight = cf.find_by(rows, "name", cf.SEEDED_INSIGHT)
    created = owner.post(cf.shares_path(cf.PROJECT_ARCHIVE), json={
        "resourceType": "insight", "resourceId": insight["id"]})
    token = created.json()["token"]
    share_id = str(created.json()["id"])
    with appclient.client(None) as anon:
        anon.get(cf.public_share_path(str(token)))
    cf.settle()
    row = owner.get(cf.share_path(cf.PROJECT_ARCHIVE, share_id)).json()
    assert int(row.get("accessCount", 0)) >= 1, (
        f"a share row must record how often the link was opened, read "
        f"{row.get('accessCount')}")


def test_the_operation_sequence_is_gapless_within_the_workspace(owner) -> None:
    """The log runs from one with no gap and no repeat."""
    rows = cf.read_all_rows(owner, cf.operations_path())
    assert rows, "the seeded workspace must already carry an operation log"
    sequences = sorted(int(row["sequence"]) for row in rows)
    assert sequences[0] == 1, (
        f"a workspace log must start at sequence 1, read {sequences[0]}")
    assert sequences == list(range(1, len(sequences) + 1)), (
        f"the log must hold no gap and no repeat, read {sequences[:12]} of "
        f"{len(sequences)}")


def test_four_simultaneous_writes_take_four_different_sequences(owner) -> None:
    """Contention issues one sequence value to each writer."""
    lo, hi = cf.archive_bounds(owner)
    suffixes = [cf.unique_suffix() for _ in range(4)]

    def make(suffix):
        return lambda: owner.post(cf.cohorts_path(cf.PROJECT_ARCHIVE), json={
            "name": cf.probe_name(suffix),
            "definition": {"from": lo, "to": hi, "types": [cf.TYPE_APP_OPENED]}})

    responses = cf.run_together([make(s) for s in suffixes])
    for response in responses:
        assert response.status_code in cf.CREATED, cf.describe(
            response, "each concurrent write must be accepted")
    cf.settle()
    rows = cf.read_all_rows(owner, cf.operations_path())
    sequences = [int(row["sequence"]) for row in rows]
    assert len(sequences) == len(set(sequences)), (
        f"no two operations may share a sequence, read {len(sequences)} rows with "
        f"{len(set(sequences))} distinct sequences")


def test_an_operation_row_is_never_updated_or_deleted(owner, backend) -> None:
    """The log is append-only in the store as well as in the answer."""
    before = backend.count(cf.TABLE_OPERATIONS)
    lo, hi = cf.archive_bounds(owner)
    suffix = cf.unique_suffix()
    owner.post(cf.cohorts_path(cf.PROJECT_ARCHIVE), json={
        "name": cf.probe_name(suffix),
        "definition": {"from": lo, "to": hi, "types": [cf.TYPE_INVITE_SENT]}})
    after = cf.poll_until(
        lambda: backend.count(cf.TABLE_OPERATIONS) > before
        and backend.count(cf.TABLE_OPERATIONS))
    assert after and after > before, (
        f"a write must append to the stored log, counted {before} then {after}")


def test_the_operations_endpoint_answers_newest_first_and_accepts_since(owner) -> None:
    """The log is readable forward from a chosen point."""
    rows = cf.read_rows(owner, cf.operations_path(), limit=20)
    assert rows, "the operation log must answer"
    sequences = [int(row["sequence"]) for row in rows]
    assert sequences == sorted(sequences, reverse=True), (
        f"the log must answer newest first, read {sequences[:8]}")
    highest = max(sequences)
    later = cf.read_rows(owner, cf.operations_path(), since=highest)
    assert all(int(row["sequence"]) > highest for row in later), (
        f"a since bound must return only operations after it, read "
        f"{[row['sequence'] for row in later][:8]}")


def test_the_audit_chain_answers_that_it_agrees(owner) -> None:
    """The digest chain is readable end to end."""
    response = owner.get(cf.audit_verify_path())
    assert response.status_code == 200, cf.describe(
        response, "the audit chain must answer whether it agrees")
    body = response.json()
    assert "agrees" in body, (
        f"the audit answer must carry agrees, saw {sorted(body)}")
    assert bool(body["agrees"]) is True, (
        f"the seeded chain must agree from the first entry to the last, read {body}")


def test_the_person_timeline_merges_every_correlated_record(owner) -> None:
    """Six kinds of record resolve to one person on one clock."""
    resolved = owner.post(cf.person_resolve_path(cf.PROJECT_ARCHIVE),
                          json={"identifier": cf.PERSON_WITH_RECORDING})
    assert resolved.status_code in cf.CREATED, cf.describe(
        resolved, f"the alias {cf.PERSON_WITH_RECORDING} must resolve to a person")
    person_id = str(resolved.json().get("id"))
    response = owner.get(cf.person_path(cf.PROJECT_ARCHIVE, person_id))
    assert response.status_code == 200, cf.describe(
        response, "a person must answer with the correlated timeline")
    timeline = response.json().get("timeline")
    assert isinstance(timeline, list) and timeline, (
        f"a person must carry a merged timeline, saw {sorted(response.json())}")
    kinds = {entry.get("kind") for entry in timeline}
    assert len(kinds) >= 2, (
        f"the timeline must merge more than one kind of record, read {kinds}")


def test_a_person_property_carries_its_previous_value_and_its_source(owner) -> None:
    """A property says where it came from and what it replaced."""
    resolved = owner.post(cf.person_resolve_path(cf.PROJECT_ARCHIVE),
                          json={"identifier": cf.PERSON_WITH_RECORDING})
    person_id = str(resolved.json().get("id"))
    body = owner.get(cf.person_path(cf.PROJECT_ARCHIVE, person_id)).json()
    properties = body.get("properties")
    assert isinstance(properties, dict) and properties, (
        f"a person must carry properties, saw {sorted(body)}")
    sources = body.get("propertySources")
    assert isinstance(sources, dict) and sources, (
        f"a person must carry the source of each property, saw {sorted(body)}")


def test_an_access_package_states_the_alias_count(owner) -> None:
    """The package reaches aliases the owner did not name."""
    resolved = owner.post(cf.person_resolve_path(cf.PROJECT_ARCHIVE),
                          json={"identifier": cf.SEEDED_PERSON_IDS[1]})
    person_id = str(resolved.json().get("id"))
    token = cf.step_up_token(owner)
    response = owner.post(cf.access_package_path(cf.PROJECT_ARCHIVE, person_id),
                          json={}, headers={"X-Step-Up": token})
    assert response.status_code in cf.CREATED, cf.describe(
        response, "an access package must be generated behind a step-up")
    body = response.json()
    assert "aliasCount" in body, (
        f"an access package must state how many aliases were found, saw {sorted(body)}")


def test_an_erasure_certificate_names_reached_and_unreached_stores(owner) -> None:
    """A certificate never claims a completeness it cannot support."""
    resolved = owner.post(cf.person_resolve_path(cf.PROJECT_ARCHIVE),
                          json={"identifier": cf.SEEDED_PERSON_IDS[7]})
    person_id = str(resolved.json().get("id"))
    token = cf.step_up_token(owner)
    erased = owner.post(cf.erase_path(cf.PROJECT_ARCHIVE, person_id),
                        json={"legalBasis": "subject request"},
                        headers={"X-Step-Up": token})
    assert erased.status_code in cf.CREATED, cf.describe(
        erased, "an erasure must be recorded behind a step-up")
    erasure_id = str(erased.json().get("id"))
    certificate = cf.poll_until(lambda: (
        lambda r: r.json() if r.status_code == 200 and r.json().get("certificate") else None
    )(owner.get(cf.erasure_path(cf.PROJECT_ARCHIVE, erasure_id))))
    assert certificate, "an erasure must reach a certificate"
    for key in ("storesCompleted", "storesUnreachable", "residualWindowDays"):
        assert key in certificate["certificate"] or key in certificate, (
            f"the certificate must name {key}, read {certificate}")


def test_an_event_for_an_erased_person_is_refused(owner) -> None:
    """A tombstone is not resurrected by a later arrival."""
    resolved = owner.post(cf.person_resolve_path(cf.PROJECT_ARCHIVE),
                          json={"identifier": cf.SEEDED_PERSON_IDS[6]})
    person_id = str(resolved.json().get("id"))
    token = cf.step_up_token(owner)
    owner.post(cf.erase_path(cf.PROJECT_ARCHIVE, person_id),
               json={"legalBasis": "subject request"},
               headers={"X-Step-Up": token})
    cf.settle()
    key = cf.project_document(owner, cf.PROJECT_ARCHIVE).get("ingestKey")
    response = httpx.post(cf.ingest_url(), json=[{
        "type": cf.TYPE_APP_OPENED, "distinctId": cf.SEEDED_PERSON_IDS[6],
        "timestamp": "2026-03-14T10:00:00Z"}],
        headers={"X-Ingest-Key": str(key)}, timeout=30.0)
    rendered = response.text
    assert cf.CODE_ERASED in rendered, (
        f"an event for an erased person must be refused as {cf.CODE_ERASED}, read "
        f"{rendered[:300]}")


def test_an_issue_carries_its_counts_and_the_releases_it_spans(owner) -> None:
    """A group is the whole picture of one error."""
    rows = cf.read_all_rows(owner, cf.issues_path(cf.PROJECT_ARCHIVE))
    found = cf.find_by(rows, "title", cf.ISSUE_RESOLVED_TITLE)
    assert found is not None, (
        f"the seeded issue must be listed, saw {[r.get('title') for r in rows]}")
    body = owner.get(cf.issue_path(cf.PROJECT_ARCHIVE, str(found["id"]))).json()
    for key in ("firstSeenAt", "lastSeenAt", "occurrenceCount", "personCount", "status"):
        assert key in body, f"an issue must carry {key}, saw {sorted(body)}"
    assert int(body["occurrenceCount"]) == cf.ISSUE_RESOLVED_OCCURRENCES, (
        f"the seeded issue must hold {cf.ISSUE_RESOLVED_OCCURRENCES} occurrences, read "
        f"{body['occurrenceCount']}")


def test_an_unresolved_frame_names_the_artefact_that_is_missing(owner) -> None:
    """An unresolved frame is never presented as source."""
    rows = cf.read_all_rows(owner, cf.issues_path(cf.PROJECT_ARCHIVE))
    found = cf.find_by(rows, "title", cf.ISSUE_UNRESOLVED_TITLE)
    assert found is not None, (
        f"the unresolved seeded issue must be listed, saw "
        f"{[r.get('title') for r in rows]}")
    body = owner.get(cf.issue_path(cf.PROJECT_ARCHIVE, str(found["id"]))).json()
    frames = body.get("frames") or []
    assert frames, f"an issue must carry its frames, saw {sorted(body)}"
    unresolved = [f for f in frames if not f.get("resolved")]
    assert unresolved, (
        f"the seeded unresolved issue must carry an unresolved frame, read {frames[:3]}")
    assert unresolved[0].get("missingArtefact"), (
        f"an unresolved frame must name the artefact that is missing, read "
        f"{unresolved[0]}")


def test_an_issue_status_comes_from_the_closed_set(owner) -> None:
    """A status is an enumeration rather than free prose."""
    rows = cf.read_all_rows(owner, cf.issues_path(cf.PROJECT_ARCHIVE))
    assert rows, "the seeded project must carry error groups"
    for row in rows:
        assert row.get("status") in cf.ISSUE_STATUSES, (
            f"an issue status must be one of {list(cf.ISSUE_STATUSES)}, read "
            f"{row.get('status')!r}")


def test_a_recording_manifest_marks_its_gaps(owner) -> None:
    """A dropped stretch is visible rather than interpolated across."""
    rows = cf.read_all_rows(owner, cf.recordings_path(cf.PROJECT_ARCHIVE))
    assert rows, "the seeded project must carry recordings"
    with_gaps = [row for row in rows if row.get("hasGaps")]
    assert with_gaps, (
        f"one seeded recording must carry a dropped stretch, read "
        f"{[r.get('hasGaps') for r in rows]}")
    body = owner.get(cf.recording_path(cf.PROJECT_ARCHIVE,
                                       str(with_gaps[0]["id"]))).json()
    assert body.get("maskingPolicySnapshot") is not None, (
        f"a recording must state the masking in force at capture, saw {sorted(body)}")


def test_a_small_survey_theme_is_never_shown_as_a_percentage(owner) -> None:
    """A theme from too few answers is labelled rather than quantified."""
    rows = cf.read_all_rows(owner, cf.surveys_path(cf.PROJECT_ARCHIVE))
    found = cf.find_by(rows, "key", cf.SURVEY_KEY) or cf.find_by(rows, "name",
                                                                 cf.SURVEY_KEY)
    assert found is not None, (
        f"the seeded survey {cf.SURVEY_KEY} must be listed, saw "
        f"{[r.get('key') or r.get('name') for r in rows]}")
    themes = found.get("themes") or []
    for theme in themes:
        if int(theme.get("size", 0)) < cf.SURVEY_SMALL_THEME:
            assert theme.get("small") is True or theme.get("percentage") in (None, ""), (
                f"a theme under {cf.SURVEY_SMALL_THEME} answers must not carry a "
                f"percentage, read {theme}")


def test_a_destination_reports_its_breaker_state_and_its_backlog(owner) -> None:
    """A failing sink holds its backlog rather than dropping it."""
    rows = cf.read_all_rows(owner, cf.destinations_path(cf.PROJECT_ARCHIVE))
    found = cf.find_by(rows, "name", cf.DESTINATION_OPEN)
    assert found is not None, (
        f"the seeded destination {cf.DESTINATION_OPEN} must be listed, saw "
        f"{[r.get('name') for r in rows]}")
    for key in ("state", "breakerState", "backlogDepth", "lastSuccessAt"):
        assert key in found, f"a destination must report {key}, saw {sorted(found)}"
    assert int(found["backlogDepth"]) == cf.DESTINATION_BACKLOG, (
        f"the seeded held backlog must be {cf.DESTINATION_BACKLOG}, read "
        f"{found['backlogDepth']}")


def test_activation_without_a_passing_dry_run_is_refused(owner) -> None:
    """A transformation is proven before it is allowed to run."""
    suffix = cf.unique_suffix()
    created = owner.post(cf.destinations_path(cf.PROJECT_ARCHIVE), json={
        "name": cf.probe_name(suffix), "kind": "log",
        "transformations": [{"sequence": 1, "drop": ["ip"]}]})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a probe destination must be creatable")
    destination_id = str(created.json()["id"])
    response = owner.patch(
        cf.destinations_path(cf.PROJECT_ARCHIVE) + "/" + destination_id,
        json={"state": "active"})
    assert cf.is_client_error(response), cf.describe(
        response, "activation without a dry run must be refused")
    assert cf.error_code(response) == cf.CODE_DRY_RUN, (
        f"the refusal code must be {cf.CODE_DRY_RUN}, read {cf.error_code(response)!r}")


def test_a_dry_run_returns_the_before_beside_the_after(owner) -> None:
    """The owner sees exactly what would leave."""
    rows = cf.read_all_rows(owner, cf.destinations_path(cf.PROJECT_ARCHIVE))
    found = cf.find_by(rows, "name", cf.DESTINATION_OPEN)
    response = owner.post(cf.dry_run_path(cf.PROJECT_ARCHIVE, str(found["id"])), json={})
    assert response.status_code in cf.CREATED, cf.describe(
        response, "a dry run must answer before and after for recent events")
    payload = response.json()
    samples = payload.get("samples") or payload.get("data") or []
    assert samples, f"a dry run must return sampled events, saw {sorted(payload)}"
    assert len(samples) <= cf.LIMIT_DRY_RUN_EVENTS, (
        f"a dry run must read at most {cf.LIMIT_DRY_RUN_EVENTS} events, read "
        f"{len(samples)}")
    first = samples[0]
    assert "before" in first, f"a dry-run sample must carry before, saw {sorted(first)}"
    assert "after" in first, f"a dry-run sample must carry after, saw {sorted(first)}"


def test_a_replay_delivers_no_event_twice(owner) -> None:
    """A replay resumes from its own cursor rather than redelivering."""
    rows = cf.read_all_rows(owner, cf.destinations_path(cf.PROJECT_ARCHIVE))
    found = cf.find_by(rows, "name", cf.DESTINATION_OPEN)
    response = owner.post(cf.replay_path(cf.PROJECT_ARCHIVE, str(found["id"])), json={})
    assert response.status_code in cf.CREATED, cf.describe(
        response, "a held backlog must be replayable")
    body = response.json()
    assert "delivered" in body or "replayed" in body, (
        f"a replay must report what it delivered, saw {sorted(body)}")
    assert int(body.get("duplicates", 0)) == 0, (
        f"a replay must deliver no event twice, read {body.get('duplicates')}")


def test_workspace_health_enumerates_every_refusal_reason(owner) -> None:
    """Refusals are enumerated rather than totalled into one number."""
    response = owner.get(cf.workspace_health_path())
    assert response.status_code == 200, cf.describe(
        response, "the health surface must answer")
    body = response.json()
    ingest = body.get("ingest") or {}
    assert isinstance(ingest.get("rejectedByReason"), dict), (
        f"health must enumerate ingest refusals by reason, saw {sorted(ingest)}")
    for key in ("storage", "materialisation", "cost"):
        assert key in body, f"health must answer the {key} group, saw {sorted(body)}"


def test_the_metered_dimensions_are_the_five_named(owner) -> None:
    """Metering is a closed set rather than an open one."""
    body = owner.get(cf.workspace_health_path()).json()
    cost = body.get("cost") or {}
    dimensions = cost.get("dimensions") or {}
    for dimension in cf.METERED_DIMENSIONS:
        assert dimension in dimensions, (
            f"the cost group must meter {dimension}, saw {sorted(dimensions)}")


def test_a_cost_projection_states_its_assumption_and_a_range(owner) -> None:
    """A projection is a range with a stated basis rather than one number."""
    body = owner.get(cf.workspace_health_path()).json()
    projection = (body.get("cost") or {}).get("projection") or {}
    assert projection.get("assumption"), (
        f"a projection must state the assumption it rests on, saw {sorted(projection)}")
    assert "low" in projection, (
        f"a projection must show a low figure, saw {sorted(projection)}")
    assert "high" in projection, (
        f"a projection must show a high figure, saw {sorted(projection)}")
    assert int(projection.get("windowDays", 0)) == cf.PROJECTION_WINDOW_DAYS, (
        f"a projection must rest on the trailing {cf.PROJECTION_WINDOW_DAYS} days, read "
        f"{projection.get('windowDays')}")


def test_absent_surfaces_answer_as_not_found(owner) -> None:
    """The product is only what the brief names, so an excluded surface is absent."""
    for path in ("/uploads", "/billing", "/emails", "/organisations", "/members",
                 "/warehouse", "/ads", "/presence", "/assistant"):
        response = owner.get(path)
        assert response.status_code == 404, cf.describe(
            response, f"the excluded surface {path} must answer as not found")


def test_first_paint_delivers_a_static_shell_the_browser_fills(owner) -> None:
    """The rendering model is a shell served once with every surface drawn in the browser."""
    page = cf.fetch_document(cf.ROUTE_LOGIN)
    assert page.status_code == 200, cf.describe(page, "the shell must be served")
    assert "<script" in page.text.lower(), (
        "a client-rendered shell must reference the script that draws the surfaces")
    api = owner.get(cf.projects_path())
    assert api.headers.get("content-type", "").startswith("application/json"), (
        f"the API behind the shell must answer JSON, read "
        f"{api.headers.get('content-type')!r}")
