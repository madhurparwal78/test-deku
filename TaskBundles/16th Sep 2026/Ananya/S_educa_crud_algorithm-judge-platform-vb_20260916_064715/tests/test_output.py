from __future__ import annotations

import concurrent.futures
import json
import os
import re
import socket
import urllib.parse

import httpx

import appclient
from conftest import (
    BASE_MEMORY_LIMIT_KB,
    BASE_TIME_LIMIT_MS,
    CATALOGUE_TOTAL,
    CATEGORIES,
    CATEGORY_PILLS,
    COIN_REASONS,
    COMPARATORS,
    CONTEST_PENALTY_SECONDS,
    CUSTOM_CASE_CAP,
    DAILY_PROBLEM_TITLE,
    DISCUSSION_ORDERS,
    DUPLICATE_WINDOW_SECONDS,
    EU_CURRENCY,
    EU_MONTHLY_MINOR,
    EU_REGION,
    EU_YEARLY_MINOR,
    EXPLORE_CARD_SLUGS,
    FAILURE_TYPES,
    FEATURED_PLAN_SLUG,
    FINISHED_CONTEST,
    FOOTER_LABELS,
    FOOTER_ROUTES,
    INTAKE_BUDGET_SECONDS,
    INTERVIEW_ROUTES,
    LANGUAGES,
    LOCKOUT_ATTEMPTS,
    MEMBER2_EMAIL,
    MEMBER2_USERNAME,
    MEMBER_EMAIL,
    MEMBER_ONLY_ROUTES,
    MEMBER_STATES,
    MEMBER_USERNAME,
    MULTIPLIERS,
    NARROW_VIEWPORT,
    NON_TERMINATING_SOURCE,
    OUTPUT_LIMIT_BYTES,
    OVERSIZED_OUTPUT_SOURCE,
    PAGE_SIZE,
    PASSWORD_MAXIMUM_FLOOR,
    PREMIUM_PLAN_SLUG,
    PRICE_CURRENCY,
    PRICE_DISPLAY,
    PRICE_MONTHLY_MINOR,
    PRICE_REGION,
    PRICE_YEARLY_LIST_MINOR,
    PRICE_YEARLY_MINOR,
    PUBLIC_ROUTES,
    RAIL_LABELS,
    REVEAL_TRUNCATION,
    RUNNING_CONTEST,
    RUNNING_CONTEST_SCORES,
    RUNTIME_ERROR_SOURCE,
    SCHEDULED_CONTEST,
    SEEDED_ACCEPTANCE,
    SEEDED_POST_MINIMUM,
    SEED_PASSWORD,
    SIGNAL_IGNORING_SOURCE,
    SILENT_SOURCE,
    SLEEPING_SOURCE,
    STDERR_CAP_BYTES,
    STUDY_PLAN_GROUPS,
    STUDY_PLAN_NAMES,
    STUDY_PLAN_SUBTITLES,
    SUBMISSION_STATES,
    SUBSCRIBER_EMAIL,
    SUBSCRIBER_USERNAME,
    SYNTAX_ERROR_SOURCE,
    TOPIC_TAG_COUNT,
    TOPIC_TAG_NAMES,
    UNBOUNDED_ALLOCATION_SOURCE,
    VERDICTS,
    WIDE_VIEWPORT,
    WRONG_SOURCE,
    accepted_source,
    await_verdict,
    catalogue,
    columns_of,
    counters,
    cursor_of,
    describe,
    distinct_values,
    drain,
    entry_point,
    facet_count,
    facets,
    field,
    first_post_id,
    idempotency_key,
    judge,
    judge_in,
    median_source,
    member_id_for,
    open_route,
    permutations_source,
    premium_slug,
    probe_email,
    probe_token,
    problem_detail,
    problem_id_for,
    program,
    register_probe,
    rows_of,
    save_draft,
    seconds_to_utc_midnight,
    settle,
    signature,
    submission_id_of,
    submit,
    submit_in,
    two_sum_slug,
    two_sum_with,
    utc_today,
)

CLIENT_ERROR = range(400, 500)
FILE_INPUT = re.compile(r"""type=["']?file""", re.I)


def _titles(rows):
    return [str(field(row, "title")) for row in rows]


def _numbers(rows):
    return [int(field(row, "number")) for row in rows]


def _slugs(rows):
    return [str(field(row, "slug")) for row in rows]


def _percent(value) -> float:
    return float(str(value).strip().rstrip("%"))


def _walk_pages(session, limit=PAGE_SIZE, **params):
    seen, cursor, pages, last = [], None, 0, None
    while pages < 40:
        query = dict(params)
        query["limit"] = limit
        if cursor:
            query["after"] = cursor
        last = catalogue(session, **query)
        rows = rows_of(last)
        seen.extend(_slugs(rows))
        cursor = cursor_of(last)
        pages += 1
        if not cursor or not rows:
            break
    return seen, last


def _entries(payload):
    return payload if isinstance(payload, list) else rows_of(payload)


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def test_catalogue_lists_seeded_problems_in_number_order(anon):
    """The catalogue answers with the seeded problem set, numbered ascending by default.
    cov: C-OV-01, C-RL-01, C-CF-30, C-CF-52, C-CF-55, C-TR-12, C-DM-30, C-DC-21
    """
    payload = catalogue(anon, limit=PAGE_SIZE)
    rows = rows_of(payload)
    assert len(rows) == PAGE_SIZE, (
        f"catalogue page one carried {len(rows)} rows, not the pinned {PAGE_SIZE}"
    )
    numbers = _numbers(rows)
    assert numbers == sorted(numbers), (
        f"catalogue default order is not problem number ascending; the page opened {numbers[:8]}"
    )
    assert int(field(payload, "count")) == CATALOGUE_TOTAL, (
        f"catalogue reports {field(payload, 'count')} published problems, not the seeded {CATALOGUE_TOTAL}"
    )
    for key in ("limit", "next_cursor", "pinned"):
        assert key in payload, f"the catalogue payload omits {key!r}: {sorted(payload)[:12]}"
    for row in rows:
        for key in ("id", "number", "slug", "title", "difficulty", "acceptance_rate", "is_premium"):
            assert key in row, f"a catalogue row omits {key!r}: {sorted(row)}"
    titles = _titles(rows)
    assert "Two Sum" in titles, (
        f"the seeded row `1. Two Sum` is absent from page one; it opened {titles[:6]}"
    )


def test_catalogue_row_payload_is_identical_for_every_caller_with_no_member_status(anon, member):
    """The catalogue row payload is the same for a signed-out caller and a member, carrying no member status.
    cov: C-CF-68, C-TR-11
    """
    public = rows_of(catalogue(anon, limit=PAGE_SIZE))
    private = rows_of(catalogue(member, limit=PAGE_SIZE))
    assert public == private, "the catalogue rows served to a member differ from the rows served signed out"
    for row in private:
        for leaked in ("status", "solved", "is_solved", "attempted", "member_status"):
            assert leaked not in row, f"the catalogue row for {field(row, 'slug')} carries {leaked!r}"


def test_seeded_rows_carry_their_pinned_acceptance_and_authored_difficulty(anon):
    """Seeded rows read their pinned acceptance and difficulty, which disagree by design.
    cov: C-DM-08, C-DM-32
    """
    found = {}
    cursor = None
    for _ in range(10):
        query = {"limit": PAGE_SIZE}
        if cursor:
            query["after"] = cursor
        payload = catalogue(anon, **query)
        for row in rows_of(payload):
            number = int(field(row, "number"))
            if number in SEEDED_ACCEPTANCE:
                found[number] = row
        cursor = cursor_of(payload)
        if not cursor:
            break
    for number, (title, acceptance, word) in SEEDED_ACCEPTANCE.items():
        assert number in found, f"the seeded problem {number}. {title} is not in the catalogue"
        row = found[number]
        assert str(field(row, "title")) == title, (
            f"problem {number} is titled {field(row, 'title')!r}, not {title!r}"
        )
        assert abs(_percent(field(row, "acceptance_rate")) - _percent(acceptance)) < 0.05, (
            f"{number}. {title} reads an acceptance of {field(row, 'acceptance_rate')}, not {acceptance}"
        )
        expected_band = {"Easy": "easy", "Med.": "medium", "Hard": "hard"}[word]
        stored = str(field(row, "difficulty")).lower().rstrip(".")
        assert stored in (expected_band, "med" if expected_band == "medium" else expected_band), (
            f"{number}. {title} carries difficulty {field(row, 'difficulty')!r}, not {word}; "
            f"difficulty is authored and never derived from the acceptance rate"
        )


def test_exactly_one_premium_problem_per_difficulty_band(anon):
    """Walking the catalogue finds exactly one premium problem in each difficulty band.
    cov: C-CF-254
    """
    premium = {}
    cursor = None
    for _ in range(10):
        query = {"limit": PAGE_SIZE}
        if cursor:
            query["after"] = cursor
        payload = catalogue(anon, **query)
        for row in rows_of(payload):
            if field(row, "is_premium", required=False):
                band = str(field(row, "difficulty")).lower().rstrip(".")
                band = "medium" if band == "med" else band
                premium.setdefault(band, []).append(str(field(row, "slug")))
        cursor = cursor_of(payload)
        if not cursor:
            break
    for band in ("easy", "medium", "hard"):
        assert len(premium.get(band, [])) == 1, (
            f"the {band} band carries {len(premium.get(band, []))} premium problems, not exactly one: "
            f"{premium}"
        )


def test_catalogue_topic_filter_intersects_tags(anon):
    """Two selected topics return only problems carrying both tags, never either.
    cov: C-CF-36, C-CF-42
    """
    pair = ["array", "two-pointers"]
    both, _ = _walk_pages(anon, topics=",".join(pair))
    first, _ = _walk_pages(anon, topics=pair[0])
    second, _ = _walk_pages(anon, topics=pair[1])
    assert first and second, "a seeded topic returned no problems"
    assert set(both) == set(first) & set(second), (
        f"topics={pair} returned {len(both)} problems but {len(set(first) & set(second))} carry both "
        f"tags, so the topic axis is not an intersection"
    )


def test_catalogue_difficulty_filter_unions_values(anon):
    """Two selected difficulties return problems of either difficulty.
    cov: C-CF-37, C-CF-43
    """
    easy, _ = _walk_pages(anon, difficulty="Easy")
    hard, _ = _walk_pages(anon, difficulty="Hard")
    both, _ = _walk_pages(anon, difficulty="Easy,Hard")
    assert easy and hard, "the seeded catalogue carries no Easy or no Hard rows"
    assert set(both) == set(easy) | set(hard), (
        f"difficulty=Easy,Hard returned {len(both)} rows against {len(set(easy) | set(hard))} in "
        f"either band, so the difficulty axis is not a union"
    )


def test_category_axis_selects_exactly_one_category_with_the_fields_parameter(anon):
    """A category filter returns only that category, and `fields=+category` exposes it.
    cov: C-CF-33, C-TR-13
    """
    for category in CATEGORIES:
        rows = rows_of(catalogue(anon, category=category, fields="+category", limit=PAGE_SIZE))
        assert rows, f"the seeded category {category} carries no problem"
        for row in rows:
            assert str(field(row, "category")) == category, (
                f"category={category} returned {field(row, 'slug')} in {field(row, 'category')!r}"
            )
            assert "slug" in row and "title" in row, (
                f"a leading plus replaced the default row fields instead of adding to them: {sorted(row)}"
            )
    narrow = rows_of(catalogue(anon, fields="number,slug", limit=PAGE_SIZE))
    assert narrow and all(set(row) == {"number", "slug"} for row in narrow), (
        f"fields=number,slug did not replace the default set; a row reads {sorted(narrow[0]) if narrow else narrow}"
    )


def test_every_category_and_all_forty_seven_topic_tags_carry_a_problem(anon):
    """Every category and every seeded topic tag counts at least one problem.
    cov: C-CF-36, C-CF-47, C-DM-34, C-DM-35, C-DM-36, C-DC-22
    """
    axes = facets(anon)
    for category in CATEGORIES:
        assert facet_count(axes, "categories", category) >= 1, (
            f"the category {category} carries no problem"
        )
    topics = axes.get("topics") if isinstance(axes, dict) else None
    assert isinstance(topics, list) and len(topics) == TOPIC_TAG_COUNT, (
        f"the topic facet lists {len(topics) if isinstance(topics, list) else topics!r} tags, not {TOPIC_TAG_COUNT}"
    )
    listed = {_slugify(str(field(entry, "value", "name", "slug"))) for entry in topics}
    for name in TOPIC_TAG_NAMES:
        assert _slugify(name) in listed, f"the seeded topic tag {name!r} is absent from the facet"
    for entry in topics:
        assert int(field(entry, "count")) >= 1, f"the topic tag {entry!r} carries no problem"
    hash_table, _ = _walk_pages(anon, topics="hash-table")
    assert facet_count(axes, "topics", "hash-table") == len(hash_table), (
        "the Hash Table count disagrees with the problems the catalogue returns for it, so tag "
        "counts are authored rather than derived"
    )


def test_search_matches_the_title_and_an_all_digit_query_matches_the_number_first(anon):
    """Search matches titles, and a query of only digits puts the exact number first.
    cov: C-CF-40, C-CF-74, C-CF-75
    """
    by_title = rows_of(catalogue(anon, search="Two Sum", limit=PAGE_SIZE))
    assert by_title and str(field(by_title[0], "title")) == "Two Sum", (
        f"searching Two Sum did not return 1. Two Sum first: {_titles(by_title)[:5]}"
    )
    by_number = rows_of(catalogue(anon, search="1", limit=PAGE_SIZE))
    assert by_number and int(field(by_number[0], "number")) == 1, (
        f"searching 1 did not open on problem number 1: {_numbers(by_number)[:5]}"
    )


def test_catalogue_filter_state_round_trips_through_the_query_string(page, anon):
    """A filtered catalogue address reproduces the same rows in a fresh session.
    cov: C-CF-72, C-CF-73
    """
    query = "?difficulty=Medium&topics=dynamic-programming&status=all&sort=number&page=1"
    first = page.get("/problemset/" + query)
    assert first.status_code == 200, f"a filtered catalogue address is not servable. {describe(first)}"
    with httpx.Client(base_url=appclient.app_url(), timeout=appclient.TIMEOUT,
                      follow_redirects=True) as fresh:
        second = fresh.get("/problemset/" + query)
    assert second.status_code == 200, f"the filtered address failed in a fresh session. {describe(second)}"
    api_rows = _titles(rows_of(catalogue(anon, difficulty="Medium", topics="dynamic-programming",
                                         limit=PAGE_SIZE)))
    assert api_rows, "the same filter through the API returned nothing, so the link is not a view"
    positions = [second.text.find(title) for title in api_rows[:5]]
    assert all(p >= 0 for p in positions), (
        f"the filtered address in a fresh session does not render the filtered rows {api_rows[:5]}"
    )
    assert positions == sorted(positions), (
        f"the filtered address rendered the rows in a different order: {api_rows[:5]}"
    )


def test_topic_tag_order_is_count_then_name(anon):
    """Topic chips order by problem count descending, then by name ascending.
    cov: C-CF-51
    """
    axes = facets(anon)
    entries = axes.get("topics") if isinstance(axes, dict) else None
    assert isinstance(entries, list) and entries, "the facet payload carries no topics list"
    keyed = [(-int(field(e, "count")), str(field(e, "value", "name")).lower()) for e in entries]
    assert keyed == sorted(keyed), (
        f"topic chips are not ordered by count descending then name ascending; the first six read {keyed[:6]}"
    )
    again = facets(anon).get("topics")
    assert [field(e, "value", "name") for e in again] == [field(e, "value", "name") for e in entries], (
        "two identical facet reads ordered the topic chips differently"
    )


def test_facet_count_excludes_its_own_multi_select_axis(anon):
    """A facet count is what the list would return if that value were added, with its own
    multi-select axis excluded.
    cov: C-CF-41, C-CF-48, C-CF-49, C-DC-22
    """
    axes = facets(anon, difficulty="Medium")
    hard_count = facet_count(axes, "difficulty", "Hard")
    hard_rows, _ = _walk_pages(anon, difficulty="Hard")
    assert hard_count == len(hard_rows) and hard_count > 0, (
        f"with Medium selected the count beside Hard reads {hard_count}, but Hard alone returns "
        f"{len(hard_rows)}; the difficulty axis must be excluded from its own count"
    )
    array_count = facet_count(axes, "topics", "array")
    narrowed = catalogue(anon, difficulty="Medium", topics="array", limit=PAGE_SIZE)
    assert int(field(narrowed, "count")) == array_count, (
        f"the count beside the array topic was {array_count} but adding it returned "
        f"{field(narrowed, 'count')} problems, so the facet count is not the conditional one"
    )


def test_facet_counts_move_when_the_filter_set_moves(anon):
    """Facet counts are recomputed against the current filter, never frozen.
    cov: C-CF-50
    """
    unfiltered = facet_count(facets(anon), "topics", "array")
    filtered = facet_count(facets(anon, difficulty="Easy"), "topics", "array")
    easy_array, _ = _walk_pages(anon, difficulty="Easy", topics="array")
    assert filtered == len(easy_array), (
        f"with Easy selected the array count reads {filtered} but Easy array problems number {len(easy_array)}"
    )
    assert filtered < unfiltered, (
        f"the array topic count stayed at {unfiltered} with and without a difficulty filter, which is "
        f"what a build that computes every facet against no filter reports"
    )


def test_cursor_pages_cover_every_stored_problem_exactly_once(anon):
    """Walking every page yields each seeded problem once, with no repeat and no omission.
    cov: C-CF-55, C-CF-56, C-CN-11
    """
    for order in (None, "acceptance", "title"):
        params = {"order": order} if order else {}
        seen, _ = _walk_pages(anon, **params)
        assert len(seen) == len(set(seen)), (
            f"paging the {order or 'default'} order returned {len(seen)} rows but only "
            f"{len(set(seen))} distinct problems, so a row was served twice across a page boundary"
        )
        assert len(seen) == CATALOGUE_TOTAL, (
            f"paging the {order or 'default'} order yielded {len(seen)} problems, not {CATALOGUE_TOTAL}"
        )


def test_catalogue_page_past_the_end_is_empty_and_successful(page, anon):
    """A page past the end answers successfully with an empty list, a null cursor and the total.
    cov: C-CF-57
    """
    seen, last = _walk_pages(anon, limit=40)
    assert len(seen) == CATALOGUE_TOTAL, f"paging by forty yielded {len(seen)} problems"
    cursor = cursor_of(last)
    if cursor:
        response = anon.get("/problems", params={"limit": 40, "after": cursor})
        assert response.status_code == 200, (
            f"the page after the last full page did not answer successfully. {describe(response)}"
        )
        payload = response.json()
        assert rows_of(payload) == [] and cursor_of(payload) in (None, ""), (
            f"the page past the end carried rows or a cursor: {payload!r}"
        )
        assert int(field(payload, "count")) == CATALOGUE_TOTAL, (
            f"the page past the end reports a total of {field(payload, 'count')}"
        )
    html = page.get("/problemset/?page=99")
    assert html.status_code == 200, (
        f"a catalogue address past the last page answered {html.status_code} rather than an empty "
        f"successful page. {describe(html)}"
    )


def test_every_catalogue_order_sorts_by_its_key_then_breaks_ties_on_the_problem_number(anon):
    """Each ordering sorts by its own key and breaks every tie on the problem number ascending.
    cov: C-CF-53, C-CF-54
    """
    rank = {"easy": 0, "medium": 1, "med": 1, "hard": 2}
    keys = {
        "acceptance": lambda r: -_percent(field(r, "acceptance_rate")),
        "difficulty": lambda r: rank[str(field(r, "difficulty")).lower().rstrip(".")],
        "title": lambda r: str(field(r, "title")).casefold(),
        "frequency": lambda r: -(field(r, "frequency_bucket", required=False) or 0),
    }
    for order, key in keys.items():
        rows = rows_of(catalogue(anon, order=order, limit=PAGE_SIZE))
        assert rows, f"the {order} ordering returned no rows"
        pairs = [(key(r), int(field(r, "number"))) for r in rows]
        assert pairs == sorted(pairs), (
            f"the {order} ordering is not sorted by its key then the problem number: {pairs[:6]}"
        )
        again = _slugs(rows_of(catalogue(anon, order=order, limit=PAGE_SIZE)))
        assert again == _slugs(rows), f"the {order} ordering changed between two identical reads"


def test_pinned_daily_row_is_not_part_of_the_result_set(anon):
    """The day's featured problem is pinned above the list without consuming a row of page one.
    cov: C-CF-58, C-CF-59, C-DM-31
    """
    payload = catalogue(anon, limit=PAGE_SIZE)
    pinned = field(payload, "pinned")
    assert isinstance(pinned, dict) and pinned, "the catalogue payload carries no pinned daily row"
    rows = rows_of(payload)
    assert len(rows) == PAGE_SIZE, f"page one carried {len(rows)} rows beside the pinned row, not {PAGE_SIZE}"
    assert str(field(pinned, "slug")) not in _slugs(rows), (
        "the pinned daily row is also inside the page-one result set, which loses a problem at the "
        "boundary with page two"
    )
    assert DAILY_PROBLEM_TITLE.split(". ", 1)[1] == str(field(pinned, "title")), (
        f"the pinned daily row is not the seeded featured problem: {pinned!r}"
    )
    second = rows_of(catalogue(anon, limit=PAGE_SIZE, after=cursor_of(payload)))
    assert _numbers(second) and _numbers(second)[0] > _numbers(rows)[-1], (
        "page two does not begin after the fiftieth row of page one"
    )


def _two_sum_id(session) -> str:
    for row in rows_of(catalogue(session, search="1", limit=PAGE_SIZE)):
        if int(field(row, "number")) == 1:
            return str(field(row, "id"))
    raise AssertionError("the catalogue search for 1 did not return 1. Two Sum")


def _status_of(session, problem_id: str) -> list:
    response = session.get("/problems/status", params={"ids": problem_id})
    assert response.status_code == 200, f"the per-member status overlay is unreadable. {describe(response)}"
    return [e for e in _entries(response.json()) if str(field(e, "problem_id")) == problem_id]


def test_submission_intake_answers_pending_before_the_program_runs(member):
    """Intake records the submission and answers promptly, carrying the state `pending`.
    cov: C-CF-142, C-CF-143, C-CF-144, C-TR-10, C-DC-28
    """
    slug = two_sum_slug(member)
    response = submit(member, slug, "python3", program(member, slug, SLEEPING_SOURCE))
    assert response.status_code in (200, 201, 202), f"intake refused a valid submission. {describe(response)}"
    body = response.json()
    assert str(field(body, "state")) == "pending", (
        f"intake answered with state {field(body, 'state')!r} rather than 'pending', so the request "
        f"blocked on judging. {describe(response)}"
    )
    assert field(body, "submission_id"), f"intake answered without a submission identifier. {describe(response)}"
    elapsed = response.elapsed.total_seconds()
    assert elapsed < INTAKE_BUDGET_SECONDS, (
        f"intake took {elapsed:.1f}s for a program that sleeps thirty seconds; the python3 wall-clock "
        f"stop lands at eighteen seconds, so the request is waiting on the program"
    )
    settled = await_verdict(member, str(field(body, "submission_id")))
    assert str(field(settled, "state")) == "done", f"the submission never settled: {settled!r}"


def test_accepted_submission_stores_a_runtime_and_a_percentile_row(member):
    """An accepted submission records a runtime, a memory figure and a percentile.
    cov: C-OV-05, C-CF-148, C-CF-199, C-TR-28, C-DC-29
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "python3", accepted_source(member, slug, "python3"))
    assert str(field(settled, "verdict")) == "Accepted", (
        f"a correct Two Sum solution settled as {field(settled, 'verdict')!r}: {settled!r}"
    )
    for key in ("submission_id", "problem_slug", "language", "state", "verdict", "failed_case_index",
                "runtime_ms", "memory_kb", "runtime_percentile", "memory_percentile", "created_at",
                "judged_at"):
        assert key in settled, f"the settled submission omits {key!r}: {sorted(settled)}"
    assert isinstance(settled["runtime_ms"], int) and settled["runtime_ms"] >= 0, (
        f"an accepted submission carries no integer runtime in milliseconds: {settled!r}"
    )
    assert isinstance(settled["memory_kb"], int) and settled["memory_kb"] > 0, (
        f"an accepted submission carries no integer memory figure: {settled!r}"
    )
    for key in ("runtime_percentile", "memory_percentile"):
        assert isinstance(settled[key], (int, float)) and 0 <= settled[key] <= 100, (
            f"an accepted submission carries no usable {key}: {settled!r}"
        )
    assert settled["verdict"] in VERDICTS and settled["state"] in SUBMISSION_STATES


def test_accepted_submission_persists_a_solved_row_for_that_member(member, backend):
    """An accepted submission leaves a stored solved row the status overlay and the status filter read back.
    cov: C-RL-05, C-CF-38, C-CF-45, C-CF-69, C-CF-70, C-CF-181, C-DM-20, C-DC-23
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "python3", accepted_source(member, slug, "python3"))
    assert str(field(settled, "verdict")) == "Accepted", f"the setup solve did not settle Accepted: {settled!r}"
    rows = backend.query(
        "SELECT first_accepted_at FROM solved_set WHERE member_id = %s AND problem_id = %s",
        (member_id_for(backend, MEMBER_EMAIL), problem_id_for(backend, slug)),
    )
    assert len(rows) == 1 and rows[0]["first_accepted_at"] is not None, (
        f"solved_set holds {len(rows)} rows for member@example.com on {slug} after an accepted submission"
    )
    marks = _status_of(member, _two_sum_id(member))
    assert marks and str(field(marks[0], "status")) == "solved", (
        f"the status overlay does not read back the stored solved row: {marks!r}"
    )
    solved, _ = _walk_pages(member, status="solved")
    unsolved, _ = _walk_pages(member, status="unsolved")
    assert slug in solved and slug not in unsolved, (
        "the status filter is not evaluated against the caller's own solved set"
    )


def test_wrong_answer_leaves_an_attempted_row_rather_than_a_solved_one(backend):
    """A submission that is not accepted adds nothing to the solved set, and the problem reads attempted.
    cov: C-CF-69, C-CF-182, C-DC-46
    """
    probe = register_probe()
    with appclient.client(probe["token"]) as session:
        slug = two_sum_slug(session)
        settled = judge(session, slug, "python3", program(session, slug, WRONG_SOURCE))
        assert str(field(settled, "verdict")) == "Wrong Answer", f"the wrong program settled {settled!r}"
        marks = _status_of(session, _two_sum_id(session))
        assert marks and str(field(marks[0], "status")) == "attempted", (
            f"a wrong answer did not leave the problem reading attempted: {marks!r}"
        )
    member = member_id_for(backend, probe["email"])
    problem = problem_id_for(backend, slug)
    assert backend.query("SELECT 1 FROM solved_set WHERE member_id = %s AND problem_id = %s",
                         (member, problem)) == [], "a wrong answer wrote a solved-set row"
    assert len(backend.query("SELECT 1 FROM attempted_set WHERE member_id = %s AND problem_id = %s",
                             (member, problem))) == 1, "a wrong answer wrote no attempted-set row"


def test_acceptance_counters_reconcile_with_the_submission_rows(member, anon):
    """The acceptance figure is the accepted count over the submission count at one decimal.
    cov: C-CF-183
    """
    slug = two_sum_slug(member)
    submitted, accepted = counters(member, slug)
    assert submitted >= accepted >= 0, f"{slug} reports {accepted} accepted against {submitted} submissions"
    row = next(r for r in rows_of(catalogue(anon, search="Two Sum", limit=PAGE_SIZE))
               if str(field(r, "slug")) == slug)
    expected = round(accepted * 100.0 / submitted, 1) if submitted else 0.0
    assert abs(_percent(field(row, "acceptance_rate")) - expected) < 0.051, (
        f"{slug} shows an acceptance of {field(row, 'acceptance_rate')} but its counters give {expected}%"
    )


def test_practice_submission_moves_counters_by_one_while_a_run_moves_neither(member, member2, subscriber):
    """A practice submission moves the submission count by one, an accepted one the accepted count, a run neither.
    cov: C-CF-132, C-CF-133, C-CF-134
    """
    probe = register_probe()
    with appclient.client(probe["token"]) as session:
        slug = two_sum_slug(session)
        drain((member, member2, subscriber, session), slug)
        before = counters(session, slug)
        ran = session.post(f"/problems/{slug}/run",
                           json={"language": "python3", "source": accepted_source(session, slug, "python3"),
                                 "cases": []})
        assert ran.status_code == 200, f"a run was refused. {describe(ran)}"
        assert counters(session, slug) == before, "a run moved the problem's counters"
        judge(session, slug, "python3", program(session, slug, WRONG_SOURCE))
        after_wrong = counters(session, slug)
        assert after_wrong == (before[0] + 1, before[1]), (
            f"a wrong practice submission moved the counters from {before} to {after_wrong}"
        )
        judge(session, slug, "python3", accepted_source(session, slug, "python3"))
        after_right = counters(session, slug)
        assert after_right == (before[0] + 2, before[1] + 1), (
            f"an accepted practice submission moved the counters from {after_wrong} to {after_right}"
        )


def test_simultaneous_accepted_submissions_move_both_counters_by_exactly_their_number(member, member2, subscriber):
    """Accepted submissions arriving together each move both counters once, with no lost update.
    cov: C-CF-184, C-DM-20
    """
    probes = [register_probe() for _ in range(4)]
    sessions = [appclient.client(p["token"]) for p in probes]
    try:
        slug = two_sum_slug(sessions[0])
        drain([member, member2, subscriber] + sessions, slug)
        before = counters(sessions[0], slug)
        sources = [accepted_source(s, slug, "python3") for s in sessions]
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(sessions)) as pool:
            responses = list(pool.map(lambda pair: submit(pair[0], slug, "python3", pair[1]),
                                      zip(sessions, sources)))
        for session, response in zip(sessions, responses):
            settled = await_verdict(session, submission_id_of(response))
            assert str(field(settled, "verdict")) == "Accepted", f"a concurrent solve settled {settled!r}"
        after = counters(sessions[0], slug)
        assert after == (before[0] + 4, before[1] + 4), (
            f"four simultaneous accepted submissions moved the counters from {before} to {after}; the "
            f"accepted count must never lose an update or exceed the submission count"
        )
    finally:
        for session in sessions:
            session.close()


def test_non_terminating_solution_settles_time_limit_exceeded(member):
    """A solution that never returns is stopped from outside and settles as a time limit, naming the limit.
    cov: C-OV-04, C-CF-151, C-CF-157, C-CF-173, C-DC-43
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "python3", program(member, slug, NON_TERMINATING_SOURCE))
    assert str(field(settled, "verdict")) == "Time Limit Exceeded", (
        f"a solution that loops forever settled as {field(settled, 'verdict')!r}: {settled!r}"
    )
    assert field(settled, "failed_case_index") is not None, f"a time limit verdict names no case index: {settled!r}"
    reveal = field(settled, "reveal")
    assert isinstance(reveal, dict), f"a time limit verdict carries no reveal object: {settled!r}"
    assert float(field(reveal, "multiplier")) == float(MULTIPLIERS["python3"]), (
        f"a time limit verdict does not reveal the python3 multiplier: {reveal!r}"
    )
    assert field(reveal, "limit") is not None, f"a time limit verdict does not reveal the limit: {reveal!r}"
    assert reveal.get("input") is None, f"a time limit verdict revealed the case input: {reveal!r}"



def test_signal_ignoring_loop_is_still_stopped_from_outside_as_time_limit_exceeded(member):
    """A loop that ignores every catchable signal is still stopped, because the limit lives outside it.
    cov: C-CF-156
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "python3", program(member, slug, SIGNAL_IGNORING_SOURCE))
    assert str(field(settled, "verdict")) == "Time Limit Exceeded", (
        f"a loop ignoring alarm and termination signals settled as {field(settled, 'verdict')!r}; an "
        f"in-process timer cannot stop it: {settled!r}"
    )


def test_sleeping_solution_settles_time_limit_exceeded_by_the_wall_clock_limit(member):
    """A program that sleeps rather than computes is stopped by the wall-clock limit.
    cov: C-CF-158, C-DC-45
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "python3", program(member, slug, SLEEPING_SOURCE))
    assert str(field(settled, "verdict")) == "Time Limit Exceeded", (
        f"a solution sleeping thirty seconds settled as {field(settled, 'verdict')!r}: {settled!r}"
    )


def test_unbounded_allocation_settles_memory_limit_exceeded(member):
    """A solution that allocates without bound settles as a memory limit, never a crash, without its input.
    cov: C-OV-04, C-CF-152, C-CF-174
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "python3", program(member, slug, UNBOUNDED_ALLOCATION_SOURCE))
    assert str(field(settled, "verdict")) == "Memory Limit Exceeded", (
        f"a solution that allocates without bound settled as {field(settled, 'verdict')!r}: {settled!r}"
    )
    reveal = field(settled, "reveal")
    assert not (isinstance(reveal, dict) and reveal.get("input")), (
        f"a memory limit verdict revealed the case input: {reveal!r}"
    )


def test_silent_solution_is_wrong_answer_recording_no_runtime_or_memory(member):
    """A solution that exits cleanly having produced nothing is a wrong answer, recording neither figure.
    cov: C-CF-150, C-CF-200
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "python3", program(member, slug, SILENT_SOURCE))
    assert str(field(settled, "verdict")) == "Wrong Answer", (
        f"a solution that returned nothing settled as {field(settled, 'verdict')!r}: {settled!r}"
    )
    assert settled.get("runtime_ms") is None and settled.get("memory_kb") is None, (
        f"a wrong answer recorded a runtime or a memory figure: {settled!r}"
    )


def test_python3_syntax_error_settles_compile_error_with_the_diagnostic(member):
    """A source the interpreter refuses to load is a compile error carrying the diagnostic.
    cov: C-CF-155
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "python3", program(member, slug, SYNTAX_ERROR_SOURCE))
    assert str(field(settled, "verdict")) == "Compile Error", (
        f"a python3 syntax error settled as {field(settled, 'verdict')!r}: {settled!r}"
    )
    diagnostic = str(field(field(settled, "reveal"), "diagnostic"))
    assert "SyntaxError" in diagnostic or "never closed" in diagnostic, (
        f"the compile error does not reproduce the interpreter's diagnostic: {settled!r}"
    )


def test_nonzero_exit_settles_runtime_error_with_standard_error_capped(member):
    """A program exiting non-zero is a runtime error whose standard error is truncated to the cap.
    cov: C-CF-153, C-CF-175
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "python3", program(member, slug, RUNTIME_ERROR_SOURCE))
    assert str(field(settled, "verdict")) == "Runtime Error", (
        f"a program raising an exception settled as {field(settled, 'verdict')!r}: {settled!r}"
    )
    reveal = field(settled, "reveal")
    stderr = str(field(reveal, "stderr"))
    assert "bytefold-stderr-marker" in stderr, f"the runtime error does not reveal the captured standard error: {reveal!r}"
    assert len(stderr.encode("utf-8")) <= STDERR_CAP_BYTES + 64, (
        f"the revealed standard error is {len(stderr)} characters, past the 4KB cap"
    )
    assert reveal.get("input") is None, f"a runtime error revealed the case input: {reveal!r}"
    assert field(settled, "failed_case_index") is not None, f"the runtime error names no case index: {settled!r}"


def test_output_past_the_byte_cap_settles_output_limit_exceeded(member):
    """An answer whose output passes the byte cap settles as an output limit.
    cov: C-CF-154
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "python3", program(member, slug, OVERSIZED_OUTPUT_SOURCE))
    assert str(field(settled, "verdict")) == "Output Limit Exceeded", (
        f"an answer of two hundred thousand values settled as {field(settled, 'verdict')!r}: {settled!r}"
    )


def test_failing_hidden_case_reveal_is_truncated(member):
    """A failing case reveals its index with input, expected and produced values truncated.
    cov: C-CF-146, C-CF-149, C-CF-172, C-DC-44
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "python3", program(member, slug, WRONG_SOURCE))
    assert str(field(settled, "verdict")) == "Wrong Answer", f"the wrong solution did not settle WA: {settled!r}"
    assert field(settled, "failed_case_index") is not None, f"the wrong answer names no case index: {settled!r}"
    reveal = field(settled, "reveal")
    assert isinstance(reveal, dict) and reveal, f"a wrong answer verdict reveals nothing: {settled!r}"
    for key in ("input", "expected", "produced"):
        value = reveal.get(key)
        assert value is not None, f"the wrong answer reveal omits {key!r}: {reveal!r}"
        assert len(str(value)) <= REVEAL_TRUNCATION + 32, (
            f"the revealed {key} is {len(str(value))} characters, past the pinned {REVEAL_TRUNCATION}"
        )


def test_same_wrong_source_names_the_same_failing_case_index_twice(member):
    """Judging stops at the first failure, and the same wrong program names the same case every time.
    cov: C-CF-146, C-CF-147, C-CF-186
    """
    slug = two_sum_slug(member)
    base = program(member, slug, WRONG_SOURCE)
    first = judge(member, slug, "python3", f"# {probe_token()}\n" + base)
    second = judge(member, slug, "python3", f"# {probe_token()}\n" + base)
    assert str(field(first, "verdict")) == str(field(second, "verdict")) == "Wrong Answer"
    assert field(first, "failed_case_index") == field(second, "failed_case_index"), (
        f"the same wrong program failed case {field(first, 'failed_case_index')} then "
        f"{field(second, 'failed_case_index')}, so the case order is not deterministic"
    )


def test_javascript_solution_is_accepted_despite_reserving_a_large_address_space(member):
    """A javascript solution starts and is accepted, because memory is judged on what is held.
    cov: C-CF-162
    """
    slug = two_sum_slug(member)
    settled = judge(member, slug, "javascript", accepted_source(member, slug, "javascript"))
    assert str(field(settled, "verdict")) == "Accepted", (
        f"a correct javascript Two Sum settled as {field(settled, 'verdict')!r}; a runtime reserving "
        f"address space must still start: {settled!r}"
    )


def test_unordered_comparator_accepts_any_order_but_refuses_a_repeated_ordering(member):
    """`46. Permutations` accepts every ordering in any order and refuses one listed twice.
    cov: C-CF-169, C-DM-40
    """
    slug = "permutations"
    detail = problem_detail(member, slug)
    assert str(field(detail, "comparator")) == "unordered", f"{slug} does not declare unordered: {detail.get('comparator')!r}"
    entry = entry_point(member, slug)
    reordered = judge(member, slug, "python3", permutations_source(entry, repeat_one=False))
    assert str(field(reordered, "verdict")) == "Accepted", (
        f"every ordering listed in reverse was not accepted by the unordered comparator: {reordered!r}"
    )
    repeated = judge(member, slug, "python3", permutations_source(entry, repeat_one=True))
    assert str(field(repeated, "verdict")) == "Wrong Answer", (
        f"an answer listing one ordering twice settled {field(repeated, 'verdict')!r}; unordered is "
        f"multiset equality, not set equality"
    )


def test_numeric_tolerance_comparator_accepts_a_median_within_the_declared_tolerance(member):
    """`4. Median of Two Sorted Arrays` accepts a median off by 1e-7 and refuses one off by 0.1.
    cov: C-CF-168, C-CF-171, C-DM-41
    """
    slug = "median-of-two-sorted-arrays"
    detail = problem_detail(member, slug)
    assert str(field(detail, "comparator")) == "numeric-tolerance", (
        f"{slug} does not declare numeric-tolerance: {detail.get('comparator')!r}"
    )
    entry = entry_point(member, slug)
    close = judge(member, slug, "python3", median_source(entry, "1e-7"))
    assert str(field(close, "verdict")) == "Accepted", (
        f"a median off by 1e-7 was not accepted inside the declared tolerance: {close!r}"
    )
    far = judge(member, slug, "python3", median_source(entry, "0.1"))
    assert str(field(far, "verdict")) == "Wrong Answer", (
        f"a median off by 0.1 settled {field(far, 'verdict')!r} rather than a wrong answer"
    )


def test_isolated_program_reaches_no_network_database_or_app_surface(member):
    """A program opening sockets to the network, the database and the app still settles, and reaches none.
    cov: C-CF-163, C-CF-166, C-TR-09, C-CN-09
    """
    slug = two_sum_slug(member)
    app = urllib.parse.urlparse(appclient.app_url())
    database = urllib.parse.urlparse(os.environ.get("DB_ADMIN_URL", "postgresql://postgres:5432/deku"))
    targets = [("1.1.1.1", 53), ("8.8.8.8", 53), ("127.0.0.1", 4173), ("127.0.0.1", 5432)]
    for host, port in ((app.hostname, app.port or 80), (database.hostname, database.port or 5432)):
        targets.append((socket.gethostbyname(host), int(port)))
    preamble = (
        "import socket\n"
        f"TARGETS = {targets!r}\n"
        "def reached():\n"
        "    for host, port in TARGETS:\n"
        "        try:\n"
        "            conn = socket.create_connection((host, port), timeout=0.5)\n"
        "            conn.close()\n"
        "            return True\n"
        "        except Exception:\n"
        "            continue\n"
        "    return False\n"
    )
    settled = judge(member, slug, "python3", two_sum_with(member, slug, preamble, "reached()"))
    assert str(field(settled, "verdict")) in ("Accepted", "Runtime Error"), (
        f"a program that tried to open sockets settled {field(settled, 'verdict')!r}; a Wrong Answer here "
        f"means a connection to {targets} succeeded from inside the sandbox: {settled!r}"
    )


def test_isolated_program_environment_names_no_database_member_or_problem(member):
    """Nothing in the executing program's environment names a database, the member or the problem.
    cov: C-CF-164
    """
    slug = two_sum_slug(member)
    words = ["database", "postgres", "db_url", MEMBER_EMAIL, MEMBER_USERNAME, slug]
    preamble = (
        "import os\n"
        f"WORDS = {words!r}\n"
        "def leaked():\n"
        "    blob = ' '.join(k + '=' + v for k, v in os.environ.items()).lower()\n"
        "    return any(word in blob for word in WORDS)\n"
    )
    settled = judge(member, slug, "python3", two_sum_with(member, slug, preamble, "leaked()"))
    assert str(field(settled, "verdict")) == "Accepted", (
        f"the sandbox environment names one of {words}: the guarded solution settled "
        f"{field(settled, 'verdict')!r}"
    )


def test_isolated_program_working_directory_is_discarded_between_cases(member):
    """A file one case writes in its working directory is gone for the next case.
    cov: C-CF-165
    """
    slug = two_sum_slug(member)
    preamble = (
        "import os\n"
        "def carried_over():\n"
        "    marker = 'bytefold-case-marker'\n"
        "    if os.path.exists(marker):\n"
        "        return True\n"
        "    try:\n"
        "        with open(marker, 'w') as handle:\n"
        "            handle.write('seen')\n"
        "    except OSError:\n"
        "        pass\n"
        "    return False\n"
    )
    settled = judge(member, slug, "python3", two_sum_with(member, slug, preamble, "carried_over()"))
    assert str(field(settled, "verdict")) == "Accepted", (
        f"a file written by one case was still present for a later case: {settled!r}"
    )


def test_problem_detail_declares_comparator_limits_and_language_multipliers(member):
    """A problem's public metadata reports its comparator, its base limits and the language multipliers.
    cov: C-CF-159, C-CF-160, C-CF-167, C-DM-37, C-DC-24
    """
    detail = problem_detail(member, two_sum_slug(member))
    for key in ("id", "number", "slug", "title", "difficulty", "category", "statement", "constraints",
                "examples", "hints", "is_premium", "accepted_count", "submission_count", "like_count",
                "dislike_count", "comparator", "time_limit_ms", "memory_limit_kb", "multipliers"):
        assert key in detail, f"the problem detail omits {key!r}: {sorted(detail)}"
    assert detail["comparator"] == "exact", f"Two Sum declares {detail['comparator']!r}, not exact"
    assert int(detail["time_limit_ms"]) == BASE_TIME_LIMIT_MS, f"Two Sum's time limit is {detail['time_limit_ms']}"
    assert int(detail["memory_limit_kb"]) == BASE_MEMORY_LIMIT_KB, f"Two Sum's memory limit is {detail['memory_limit_kb']}"
    multipliers = {str(k): float(v) for k, v in dict(detail["multipliers"]).items()}
    assert multipliers.get("javascript") == 2.0 and multipliers.get("python3") == 3.0, (
        f"the language multipliers read {multipliers}, not javascript 2.0 and python3 3.0"
    )
    assert "topic_tags" not in detail, "topic_tags were served without being asked for"
    asked = problem_detail(member, two_sum_slug(member), fields="+topic_tags")
    names = {str(t.get("name", t) if isinstance(t, dict) else t) for t in asked.get("topic_tags", [])}
    assert {"Array", "Hash Table"} <= names, f"Two Sum's topic tags read {names}, not Array and Hash Table"


def test_two_sum_signature_declares_nums_and_target_in_both_languages(anon):
    """Two Sum's signature takes `nums` as `array<int>` and `target` as `int` in python3 and javascript.
    cov: C-DM-12, C-DC-25
    """
    slug = two_sum_slug(anon)
    for language in LANGUAGES:
        sig = signature(anon, slug, language)
        for key in ("language", "starter", "entry_point", "parameters", "returns", "mutates", "indent"):
            assert key in sig, f"the {language} signature omits {key!r}: {sorted(sig)}"
        params = [(str(p["name"]), str(p["type"])) for p in sig["parameters"]]
        assert params == [("nums", "array<int>"), ("target", "int")], (
            f"the {language} Two Sum parameters read {params}"
        )
        assert str(sig["returns"]) == "array<int>" and list(sig["mutates"]) == [], (
            f"the {language} Two Sum signature returns {sig['returns']!r} mutating {sig['mutates']!r}"
        )
        assert str(sig["starter"]).strip(), f"the {language} starter is empty"


def test_run_or_submission_in_an_unoffered_language_is_rejected_as_invalid_input(member, backend):
    """Only python3 and javascript are offered; any other language is refused and nothing is written.
    cov: C-CF-109, C-CF-110, C-CN-08
    """
    slug = two_sum_slug(member)
    before = backend.query("SELECT count(*) AS n FROM submissions WHERE member_id = %s",
                           (member_id_for(backend, MEMBER_EMAIL),))[0]["n"]
    ran = member.post(f"/problems/{slug}/run", json={"language": "cpp", "source": "int main(){}", "cases": []})
    assert ran.status_code == 400, f"a run in cpp answered {ran.status_code}. {describe(ran)}"
    sent = member.post("/submissions", json={"problem_slug": slug, "language": "java",
                                             "source": "class Solution {}", "context": "practice"},
                       headers={"Idempotency-Key": idempotency_key()})
    assert sent.status_code == 400, f"a submission in java answered {sent.status_code}. {describe(sent)}"
    after = backend.query("SELECT count(*) AS n FROM submissions WHERE member_id = %s",
                          (member_id_for(backend, MEMBER_EMAIL),))[0]["n"]
    assert after == before, "a refused submission still wrote a submission row"


def test_source_past_the_64kb_cap_is_rejected_at_intake_leaving_no_row(member, backend):
    """A source over 64KB is refused at intake and no submission row exists afterwards.
    cov: C-CF-137
    """
    slug = two_sum_slug(member)
    source = accepted_source(member, slug, "python3") + "\n" + ("# padding\n" * 7000)
    member_id = member_id_for(backend, MEMBER_EMAIL)
    before = backend.query("SELECT count(*) AS n FROM submissions WHERE member_id = %s", (member_id,))[0]["n"]
    response = submit(member, slug, "python3", source)
    assert response.status_code in (400, 413), f"a {len(source)}-byte source was admitted. {describe(response)}"
    after = backend.query("SELECT count(*) AS n FROM submissions WHERE member_id = %s", (member_id,))[0]["n"]
    assert after == before, "a source refused at intake still wrote a submission row"


def test_submission_without_an_idempotency_key_is_rejected_as_invalid_input(member):
    """A submission carrying no Idempotency-Key header is refused as invalid input.
    cov: C-CF-136
    """
    slug = two_sum_slug(member)
    response = member.post("/submissions", json={"problem_slug": slug, "language": "python3",
                                                 "source": accepted_source(member, slug, "python3"),
                                                 "context": "practice"})
    assert response.status_code == 400, (
        f"a submission without an Idempotency-Key answered {response.status_code}. {describe(response)}"
    )


def test_run_case_typed_from_the_signature_refuses_a_string_for_an_array_parameter(anon):
    """A run case giving a string where the signature declares an integer array is invalid input.
    cov: C-CF-124
    """
    slug = two_sum_slug(anon)
    response = anon.post(f"/problems/{slug}/run",
                         json={"language": "python3", "source": accepted_source(anon, slug, "python3"),
                               "cases": [{"nums": "not-an-array", "target": 9}]})
    assert response.status_code == 400, f"a string for nums answered {response.status_code}. {describe(response)}"


def test_run_carrying_more_than_ten_custom_cases_is_rejected(anon):
    """A run may carry at most ten custom cases; eleven are refused as invalid input.
    cov: C-CF-125
    """
    slug = two_sum_slug(anon)
    source = accepted_source(anon, slug, "python3")
    cases = [{"nums": [index, 100 - index], "target": 100} for index in range(CUSTOM_CASE_CAP + 1)]
    over = anon.post(f"/problems/{slug}/run", json={"language": "python3", "source": source, "cases": cases})
    assert over.status_code == 400, f"eleven custom cases answered {over.status_code}. {describe(over)}"
    at_cap = anon.post(f"/problems/{slug}/run",
                       json={"language": "python3", "source": source, "cases": cases[:CUSTOM_CASE_CAP]})
    assert at_cap.status_code == 200, f"ten custom cases were refused. {describe(at_cap)}"


def test_signed_out_run_shows_example_cases_and_a_custom_case_with_no_expected_value(anon):
    """A signed-out run executes the examples plus custom cases; a custom result carries no expected value.
    cov: C-RL-02, C-CF-126, C-CF-130, C-CF-131, C-CF-135, C-DC-27
    """
    slug = two_sum_slug(anon)
    response = anon.post(f"/problems/{slug}/run",
                         json={"language": "python3", "source": accepted_source(anon, slug, "python3"),
                               "cases": [{"nums": [4, 5, 6], "target": 11}]})
    assert response.status_code == 200, f"a signed-out run was refused. {describe(response)}"
    body = response.json()
    assert field(body, "run_id"), f"the run answered no run_id: {body!r}"
    results = list(field(body, "results"))
    examples = [r for r in results if str(field(r, "kind")) == "example"]
    customs = [r for r in results if str(field(r, "kind")) == "custom"]
    assert examples, f"the run executed no example case: {results!r}"
    for row in examples:
        for key in ("index", "input", "expected", "produced", "passed"):
            assert row.get(key) is not None, f"an example result omits {key!r}: {row!r}"
    assert len(customs) == 1, f"the run did not execute the one custom case: {results!r}"
    assert customs[0].get("expected") is None and customs[0].get("passed") is None, (
        f"a custom case was compared against an expected value: {customs[0]!r}"
    )
    assert customs[0].get("produced") is not None, f"the custom case shows no produced output: {customs[0]!r}"


def test_replayed_idempotency_key_returns_the_original_submission(member):
    """A repeat with the same key and the same body returns the first submission.
    cov: C-CF-177, C-TR-14
    """
    slug = two_sum_slug(member)
    source = accepted_source(member, slug, "python3")
    key = idempotency_key()
    original = submission_id_of(submit(member, slug, "python3", source, key=key))
    replay = submit(member, slug, "python3", source, key=key)
    assert submission_id_of(replay) == original, (
        f"replaying the key created {field(replay.json(), 'submission_id')} beside the original {original}"
    )


def test_replayed_idempotency_key_with_a_different_body_is_rejected_as_a_conflict(member):
    """A repeat with the same key and a different body is refused as a conflicting request.
    cov: C-CF-178
    """
    slug = two_sum_slug(member)
    key = idempotency_key()
    submission_id_of(submit(member, slug, "python3", accepted_source(member, slug, "python3"), key=key))
    clash = submit(member, slug, "python3", accepted_source(member, slug, "python3"), key=key)
    assert clash.status_code == 409, (
        f"reusing a key with a different body answered {clash.status_code}. {describe(clash)}"
    )


def test_duplicate_source_inside_the_window_is_refused(member):
    """An immediate resubmission of the same source, problem and language is refused as a conflict.
    cov: C-CF-179
    """
    slug = two_sum_slug(member)
    source = accepted_source(member, slug, "python3")
    submission_id_of(submit(member, slug, "python3", source))
    second = submit(member, slug, "python3", source)
    assert second.status_code == 409, (
        f"an immediate repeat of the same source answered {second.status_code} rather than a conflict. "
        f"{describe(second)}"
    )
    assert str(field(second.json(), "type")) == "conflict", f"the refusal type is not conflict. {describe(second)}"


def test_resubmission_after_the_window_is_accepted(member):
    """The duplicate rule catches a double press without catching a later resubmission.
    cov: C-CF-180
    """
    slug = two_sum_slug(member)
    source = accepted_source(member, slug, "python3")
    submission_id_of(submit(member, slug, "python3", source))
    settle(float(DUPLICATE_WINDOW_SECONDS + 2))
    later = submit(member, slug, "python3", source)
    assert later.status_code in (200, 201, 202), (
        f"a resubmission past the {DUPLICATE_WINDOW_SECONDS}s window was refused. {describe(later)}"
    )


def test_hidden_case_inputs_stored_in_the_database_never_appear_in_problem_responses(anon, member, backend):
    """Hidden case inputs read from storage appear in no problem, signature or run response.
    cov: C-RL-10, C-CF-176, C-DM-39
    """
    slug = two_sum_slug(anon)
    stored = backend.query(
        "SELECT tc.input AS input FROM test_cases tc JOIN test_sets ts ON tc.test_set_id = ts.id "
        "JOIN problems p ON ts.problem_id = p.id WHERE p.slug = %s AND tc.is_example = false",
        (slug,),
    )
    lists = []
    for row in stored:
        for match in re.findall(r"\[([-\d,\s]+)\]", json.dumps(row["input"]) if not isinstance(row["input"], str) else row["input"]):
            values = [v.strip() for v in match.split(",") if v.strip()]
            if len(values) > 4:
                lists.append(values)
    assert lists, "no hidden Two Sum case holds more than four values in nums"
    responses = [
        anon.get(f"/problems/{slug}").text,
        member.get(f"/problems/{slug}", params={"fields": "+topic_tags"}).text,
        anon.get(f"/problems/{slug}/signature", params={"language": "python3"}).text,
        anon.get(f"/problems/{slug}/signature", params={"language": "javascript"}).text,
        anon.post(f"/problems/{slug}/run", json={"language": "python3",
                                                 "source": accepted_source(anon, slug, "python3"),
                                                 "cases": []}).text,
    ]
    blob = re.sub(r"\s+", "", " ".join(responses))
    for values in lists:
        needle = ",".join(values)
        assert needle not in blob, f"a hidden case input [{needle[:60]}] appears in a problem response"


def test_every_published_problem_stores_two_signatures_ten_cases_an_example_and_a_comparator(backend):
    """Every published problem stores both signatures, at least ten cases, an example and a declared comparator.
    cov: C-OV-02, C-CF-170, C-DM-14, C-DM-38
    """
    offenders = backend.query(
        "SELECT p.slug FROM problems p WHERE p.state = 'published' AND ("
        " (SELECT count(DISTINCT s.language) FROM problem_signatures s WHERE s.problem_id = p.id"
        "   AND s.language IN ('python3', 'javascript')) < 2"
        " OR (SELECT count(*) FROM test_cases c JOIN test_sets t ON c.test_set_id = t.id"
        "   WHERE t.problem_id = p.id AND t.version = (SELECT max(version) FROM test_sets WHERE problem_id = p.id)) < 10"
        " OR NOT EXISTS (SELECT 1 FROM test_cases c JOIN test_sets t ON c.test_set_id = t.id"
        "   WHERE t.problem_id = p.id AND c.is_example)"
        " OR EXISTS (SELECT 1 FROM test_sets t WHERE t.problem_id = p.id AND coalesce(t.comparator, '') = '')"
        ")"
    )
    assert offenders == [], f"published problems missing a signature, cases, an example or a comparator: {offenders[:10]}"
    comparators = distinct_values(backend, "test_sets", "comparator")
    assert comparators <= set(COMPARATORS), f"test sets declare comparators outside the five: {comparators}"
    output_limits = backend.query(
        "SELECT t.output_limit_bytes AS b FROM test_sets t JOIN problems p ON t.problem_id = p.id WHERE p.slug = 'two-sum'"
    )
    assert output_limits and all(int(r["b"]) == OUTPUT_LIMIT_BYTES for r in output_limits), (
        f"Two Sum's output limit reads {output_limits}, not the default {OUTPUT_LIMIT_BYTES}"
    )


def test_draft_row_is_stored_per_member_problem_and_language(member, backend):
    """A draft is stored against the member, the problem and the language together.
    cov: C-RL-05, C-CF-70, C-CF-115, C-CF-118, C-DC-31
    """
    slug = two_sum_slug(member)
    marker = probe_token()
    response = save_draft(member, slug, "python3", f"# draft {marker}\n")
    assert response.status_code in (200, 201, 204), f"a member could not save a draft. {describe(response)}"
    read = member.get(f"/drafts/{slug}", params={"language": "python3"})
    assert read.status_code == 200 and marker in str(field(read.json(), "body")), (
        f"the stored draft does not carry what was written. {describe(read)}"
    )
    rows = backend.query(
        "SELECT body FROM drafts WHERE member_id = %s AND problem_id = %s AND language = 'python3'",
        (member_id_for(backend, MEMBER_EMAIL), problem_id_for(backend, slug)),
    )
    assert len(rows) == 1 and marker in str(rows[0]["body"]), (
        f"drafts holds {len(rows)} python3 rows for this member and problem"
    )


def test_draft_stored_row_survives_a_language_switch(member):
    """Writing a draft in one language leaves the other language's draft untouched.
    cov: C-CF-116
    """
    slug = two_sum_slug(member)
    python_marker, js_marker = probe_token(), probe_token()
    first = save_draft(member, slug, "python3", f"# {python_marker}\n")
    assert first.status_code in (200, 201, 204), f"the python3 draft was refused. {describe(first)}"
    second = save_draft(member, slug, "javascript", f"// {js_marker}\n")
    assert second.status_code in (200, 201, 204), f"the javascript draft was refused. {describe(second)}"
    back = member.get(f"/drafts/{slug}", params={"language": "python3"})
    body = str(field(back.json(), "body"))
    assert python_marker in body and js_marker not in body, (
        f"writing the javascript draft changed the python3 draft; it now reads {body[:120]!r}"
    )


def test_simultaneous_draft_writes_leave_one_stored_row_holding_one_of_the_two_bodies(backend):
    """Two draft writes arriving together leave one row whose body is one of the two writes.
    cov: C-DM-22
    """
    probe = register_probe()
    with appclient.client(probe["token"]) as a, appclient.client(probe["token"]) as b:
        slug = two_sum_slug(a)
        bodies = [f"# tab one {probe_token()}\n", f"# tab two {probe_token()}\n"]
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            responses = list(pool.map(
                lambda pair: pair[0].put(f"/drafts/{slug}", json={"language": "python3", "body": pair[1], "version": 0}),
                [(a, bodies[0]), (b, bodies[1])]))
    assert any(r.status_code in (200, 201, 204) for r in responses), (
        "neither simultaneous draft write was accepted: " + " | ".join(describe(r) for r in responses)
    )
    rows = backend.query(
        "SELECT body FROM drafts WHERE member_id = %s AND problem_id = %s AND language = 'python3'",
        (member_id_for(backend, probe["email"]), problem_id_for(backend, slug)),
    )
    assert len(rows) == 1, f"two simultaneous draft writes left {len(rows)} rows"
    assert str(rows[0]["body"]) in bodies, f"the stored draft is a blend of both writes: {rows[0]['body']!r}"


def test_cross_member_submission_read_is_denied(member, member2):
    """One member's submission answers not-found from another member's session.
    cov: C-RL-06, C-RL-17, C-CF-203
    """
    slug = two_sum_slug(member)
    other_id = submission_id_of(submit(member, slug, "python3", accepted_source(member, slug, "python3")))
    read = member2.get(f"/submissions/{other_id}")
    assert read.status_code == 404, (
        f"member2 reading another member's submission answered {read.status_code}; it must answer as if "
        f"the record does not exist. {describe(read)}"
    )


def test_cross_member_draft_read_is_denied(member, member2):
    """One member's draft is unreachable from another member's session.
    cov: C-RL-07
    """
    slug = two_sum_slug(member)
    marker = probe_token()
    saved = save_draft(member, slug, "python3", f"# {marker}\n")
    assert saved.status_code in (200, 201, 204), f"the setup draft was refused. {describe(saved)}"
    read = member2.get(f"/drafts/{slug}", params={"language": "python3"})
    assert read.status_code in (200, 404), f"reading a draft answered {read.status_code}. {describe(read)}"
    assert marker not in read.text, f"member2 read member@example.com's draft buffer. {describe(read)}"


def test_submission_list_returns_only_the_callers_own_rows_newest_first(member, member2):
    """A member's submission list carries that member's attempts, newest first, and nobody else's.
    cov: C-CF-201, C-DC-30
    """
    slug = two_sum_slug(member)
    mine = submission_id_of(submit(member, slug, "python3", accepted_source(member, slug, "python3")))
    theirs = member2.get("/submissions", params={"problem": slug, "limit": PAGE_SIZE})
    assert theirs.status_code == 200, f"the submission list is unreadable. {describe(theirs)}"
    assert mine not in [str(field(r, "submission_id", "id")) for r in rows_of(theirs.json())], (
        f"member2's submission list carries member@example.com's submission {mine}"
    )
    own = rows_of(member.get("/submissions", params={"problem": slug, "limit": PAGE_SIZE}).json())
    assert own and str(field(own[0], "submission_id", "id")) == mine, (
        "the caller's own list does not open on the newest submission"
    )
    stamps = [str(field(r, "created_at")) for r in own]
    assert stamps == sorted(stamps, reverse=True), "the submission list is not ordered newest first"


def test_gated_statement_without_an_entitlement_is_denied(member):
    """A premium problem's statement and signature are refused as payment-required without an entitlement.
    cov: C-RL-08, C-RL-13, C-RL-16, C-CF-252
    """
    slug = premium_slug(member)
    response = member.get(f"/problems/{slug}")
    assert response.status_code == 402, (
        f"a gated statement answered {response.status_code} to a member with no entitlement. {describe(response)}"
    )
    assert str(field(response.json(), "type")) == "payment_required", f"the refusal type is wrong. {describe(response)}"
    sig = member.get(f"/problems/{slug}/signature", params={"language": "python3"})
    assert sig.status_code == 402, f"a gated signature answered {sig.status_code}. {describe(sig)}"


def test_premium_row_stays_public_while_the_body_is_gated(anon, member, backend):
    """A premium problem's catalogue row is public; its statement body is not, and a gated submit writes nothing.
    cov: C-RL-14, C-CF-138, C-CF-253
    """
    rows = [r for r in rows_of(catalogue(anon, limit=PAGE_SIZE)) if field(r, "is_premium", required=False)]
    assert rows, "page one carries no row marked premium"
    for key in ("number", "title", "difficulty", "acceptance_rate", "is_premium"):
        assert field(rows[0], key, required=False) is not None, f"the premium row omits {key!r}: {rows[0]!r}"
    slug = str(field(rows[0], "slug"))
    assert anon.get(f"/problems/{slug}").status_code in (401, 402), "a premium body was served signed out"
    member_id = member_id_for(backend, MEMBER_EMAIL)
    before = backend.query("SELECT count(*) AS n FROM submissions WHERE member_id = %s", (member_id,))[0]["n"]
    refused = submit(member, slug, "python3", "def placeholder():\n    return 0\n")
    assert refused.status_code == 402, f"a gated submission answered {refused.status_code}. {describe(refused)}"
    after = backend.query("SELECT count(*) AS n FROM submissions WHERE member_id = %s", (member_id,))[0]["n"]
    assert after == before, "a submission refused as payment-required still wrote a row"


def test_employer_filter_without_an_entitlement_is_denied(member):
    """An employers filter is refused as payment-required without an entitlement.
    cov: C-RL-09, C-CF-67
    """
    response = member.get("/problems", params={"employers": "kestrel", "limit": PAGE_SIZE})
    assert response.status_code == 402, (
        f"the employer facet answered {response.status_code} to a member with no entitlement. {describe(response)}"
    )


def test_employer_tags_are_absent_from_the_public_payload(anon, member, subscriber):
    """Employer tags never appear in a problem payload served without an entitlement.
    cov: C-CF-102, C-CF-251
    """
    slug = two_sum_slug(anon)
    for session, who in ((anon, "a signed-out caller"), (member, "an unentitled member")):
        payload = problem_detail(session, slug, fields="+employer_tags")
        assert "employer_tags" not in payload, f"the problem payload served to {who} carries employer_tags"
    entitled = problem_detail(subscriber, slug, fields="+employer_tags")
    assert "employer_tags" in entitled, "an entitled subscriber asking for employer_tags received none"


def test_subscriber_employer_filter_with_two_employers_returns_either(subscriber):
    """An entitled subscriber filtering by two employers receives the problems of either.
    cov: C-RL-12, C-CF-39, C-CF-44
    """
    employers = facets(subscriber).get("employers")
    assert isinstance(employers, list) and len(employers) >= 2, f"the employer facet is empty: {employers!r}"
    first, second = (str(field(e, "value", "slug")) for e in employers[:2])
    one, _ = _walk_pages(subscriber, employers=first)
    two, _ = _walk_pages(subscriber, employers=second)
    both, _ = _walk_pages(subscriber, employers=f"{first},{second}")
    assert set(both) == set(one) | set(two), (
        f"employers={first},{second} returned {len(both)} problems against {len(set(one) | set(two))} of either"
    )


def test_subscriber_reads_the_gated_statement_holding_an_active_yearly_entitlement(subscriber, anon):
    """An entitled subscriber reads the statement a member is refused.
    cov: C-RL-11, C-DM-47, C-DC-20
    """
    slug = premium_slug(anon)
    payload = problem_detail(subscriber, slug)
    assert field(payload, "statement"), f"the gated statement came back empty for the subscriber: {payload!r}"
    me = subscriber.get("/me")
    assert me.status_code == 200, f"the subscriber's account is unreadable. {describe(me)}"
    entitlement = field(me.json(), "entitlement")
    text = str(entitlement)
    assert "yearly" in text and "US" in text and "active" in text, (
        f"subscriber@example.com does not hold an active yearly entitlement in region US: {entitlement!r}"
    )


def test_daily_endpoint_reports_the_utc_day_and_the_seconds_left_in_it(anon, backend):
    """The daily endpoint reports the current UTC day and the seconds remaining until UTC midnight.
    cov: C-CF-187, C-CF-188, C-TR-30, C-DC-26
    """
    pinned = field(catalogue(anon, limit=PAGE_SIZE), "pinned")
    slug = str(field(pinned, "slug"))
    response = anon.get(f"/problems/{slug}/daily")
    assert response.status_code == 200, f"the daily endpoint is unreadable. {describe(response)}"
    body = response.json()
    assert field(body, "is_daily") is True, f"the pinned problem does not report itself as the daily: {body!r}"
    assert str(field(body, "day")) == utc_today(backend), (
        f"the daily endpoint reports day {field(body, 'day')!r}, but the UTC day is {utc_today(backend)}"
    )
    remaining = float(field(body, "seconds_remaining"))
    expected = seconds_to_utc_midnight(backend)
    assert 0 <= remaining <= 86400 and abs(remaining - expected) < 120, (
        f"the daily countdown reads {remaining}s, but UTC midnight is {expected:.0f}s away"
    )


def test_streak_advances_once_for_two_solves_on_one_day(member):
    """The streak advances by at most one on a day, however many solves arrive.
    cov: C-CF-195
    """
    before = member.get("/streak")
    assert before.status_code == 200, f"the streak is unreadable. {describe(before)}"
    start = int(field(before.json(), "current"))
    slug = two_sum_slug(member)
    first = judge(member, slug, "python3", accepted_source(member, slug, "python3"))
    second = judge(member, slug, "python3", accepted_source(member, slug, "python3"))
    assert str(field(first, "verdict")) == str(field(second, "verdict")) == "Accepted"
    end = int(field(member.get("/streak").json(), "current"))
    assert end - start <= 1, f"the streak moved from {start} to {end} across two solves on one day"


def test_streak_starts_at_one_on_a_first_solve_of_any_problem_stored_as_a_utc_date(backend):
    """A first accepted solve of any problem starts the streak at one, with the UTC day stored.
    cov: C-RL-05, C-CF-191, C-DC-32
    """
    probe = register_probe()
    with appclient.client(probe["token"]) as session:
        slug = two_sum_slug(session)
        settled = judge(session, slug, "python3", accepted_source(session, slug, "python3"))
        assert str(field(settled, "verdict")) == "Accepted", f"the probe solve settled {settled!r}"
        streak = session.get("/streak").json()
    assert int(field(streak, "current")) == 1 and int(field(streak, "longest")) >= 1, (
        f"a first solve left the streak at {streak!r}"
    )
    assert str(field(streak, "last_qualifying_day")) == utc_today(backend), (
        f"the last qualifying day reads {field(streak, 'last_qualifying_day')!r}, not the UTC day"
    )
    stored = backend.query("SELECT current, longest, last_qualifying_day FROM streaks WHERE member_id = %s",
                           (member_id_for(backend, probe["email"]),))
    assert len(stored) == 1 and str(stored[0]["last_qualifying_day"]) == utc_today(backend), (
        f"the streaks table holds {stored!r} for the probe"
    )


def test_streak_increments_after_yesterday_and_resets_to_one_after_a_gap_keeping_the_longest_run(backend):
    """A solve the day after the last qualifying day adds one; a solve after a gap resets to one.
    cov: C-CF-192, C-CF-193, C-CF-194
    """
    probe = register_probe()
    with appclient.client(probe["token"]) as session:
        slug = two_sum_slug(session)
        judge(session, slug, "python3", accepted_source(session, slug, "python3"))
        member_id = member_id_for(backend, probe["email"])
        backend.query(
            "UPDATE streaks SET current = 4, longest = 4, "
            "last_qualifying_day = (now() AT TIME ZONE 'utc')::date - 1 WHERE member_id = %s", (member_id,))
        judge(session, slug, "python3", accepted_source(session, slug, "python3"))
        after_yesterday = session.get("/streak").json()
        assert (int(field(after_yesterday, "current")), int(field(after_yesterday, "longest"))) == (5, 5), (
            f"a solve the day after a qualifying day left the streak at {after_yesterday!r}, not 5 and 5"
        )
        backend.query(
            "UPDATE streaks SET current = 7, longest = 9, "
            "last_qualifying_day = (now() AT TIME ZONE 'utc')::date - 3 WHERE member_id = %s", (member_id,))
        judge(session, slug, "python3", accepted_source(session, slug, "python3"))
        after_gap = session.get("/streak").json()
    assert (int(field(after_gap, "current")), int(field(after_gap, "longest"))) == (1, 9), (
        f"a solve after a gap left the streak at {after_gap!r}, not a current run of 1 beside a longest of 9"
    )


def test_redeeming_more_coins_than_the_ledger_balance_is_refused_leaving_the_balance(member, backend):
    """A redemption larger than the balance is refused, the balance is the ledger sum and never negative.
    cov: C-CF-196, C-CF-197, C-CF-198, C-DM-29, C-DC-33
    """
    first = member.get("/coins")
    assert first.status_code == 200, f"the coin balance is unreadable. {describe(first)}"
    balance = int(field(first.json(), "balance"))
    stored = backend.query("SELECT coalesce(sum(delta), 0) AS s FROM coin_ledger WHERE member_id = %s",
                           (member_id_for(backend, MEMBER_EMAIL),))[0]["s"]
    assert int(stored) == balance and balance >= 0, (
        f"the coin balance reads {balance} but the ledger sums to {stored}"
    )
    refused = member.post("/coins/redeem", json={"amount": balance + 1000, "reference": f"probe-{probe_token()}"})
    assert refused.status_code in CLIENT_ERROR, f"an over-balance redemption was accepted. {describe(refused)}"
    after = int(field(member.get("/coins").json(), "balance"))
    assert after == balance, f"a refused redemption moved the balance from {balance} to {after}"
    reasons = distinct_values(backend, "coin_ledger", "reason")
    assert reasons <= set(COIN_REASONS), f"the coin ledger carries reasons outside the seven: {reasons}"
    zero = backend.query("SELECT count(*) AS n FROM coin_ledger WHERE delta = 0")[0]["n"]
    assert zero == 0, f"the coin ledger carries {zero} zero deltas"


def test_study_plan_listing_carries_the_four_seeded_plans_with_the_premium_one_gated(member, subscriber):
    """Four plans are seeded with item and solved counts, and the premium plan body is gated.
    cov: C-CF-206, C-DM-45, C-DC-34
    """
    listing = member.get("/studyplans")
    assert listing.status_code == 200, f"the study plans are unreadable. {describe(listing)}"
    plans = _entries(listing.json())
    titles = {str(field(p, "title")) for p in plans}
    for name in STUDY_PLAN_NAMES:
        assert name in titles, f"the seeded study plan {name!r} is missing: {sorted(titles)}"
    by_slug = {str(field(p, "slug")): p for p in plans}
    assert FEATURED_PLAN_SLUG in by_slug and PREMIUM_PLAN_SLUG in by_slug, f"plan slugs read {sorted(by_slug)}"
    assert by_slug[PREMIUM_PLAN_SLUG]["is_premium"] is True, "Top Interview 150 is not marked premium"
    for plan in plans:
        for key in ("group", "is_featured", "item_count", "solved_count"):
            assert key in plan, f"a study plan entry omits {key!r}: {plan!r}"
    gated = member.get(f"/studyplans/{PREMIUM_PLAN_SLUG}")
    assert gated.status_code == 402, f"the premium plan body answered {gated.status_code} to a member. {describe(gated)}"
    assert subscriber.get(f"/studyplans/{PREMIUM_PLAN_SLUG}").status_code == 200, "the subscriber was refused the premium plan"


def test_study_plan_progress_follows_the_stored_solved_set(backend):
    """Solving a plan's problem from the catalogue advances the plan, with progress derived from the solved set.
    cov: C-OV-08, C-CF-211, C-CF-212
    """
    probe = register_probe()
    with appclient.client(probe["token"]) as session:
        detail = session.get(f"/studyplans/{FEATURED_PLAN_SLUG}")
        assert detail.status_code == 200, f"the featured plan is unreadable. {describe(detail)}"
        items = [str(field(i, "slug", "problem_slug")) for i in field(detail.json(), "items")]
        assert "two-sum" in items, f"Bytefold 75 does not carry Two Sum: {items[:10]}"
        before = int(field(detail.json(), "solved_count"))
        slug = two_sum_slug(session)
        judge(session, slug, "python3", accepted_source(session, slug, "python3"))
        after = session.get(f"/studyplans/{FEATURED_PLAN_SLUG}").json()
    assert int(field(after, "solved_count")) == before + 1, (
        f"solving Two Sum from the catalogue moved Bytefold 75 from {before} to {field(after, 'solved_count')}"
    )
    columns = columns_of(backend, "study_plans") | columns_of(backend, "study_plan_items")
    assert not {"solved_count", "progress"} & columns, "plan progress is stored as a column rather than derived"


def test_study_plan_items_keep_the_authored_order(member, backend):
    """A plan detail lists its problems in the position order stored for the plan.
    cov: C-CF-210, C-DC-34
    """
    response = member.get(f"/studyplans/{FEATURED_PLAN_SLUG}")
    assert response.status_code == 200, f"the plan is unreadable. {describe(response)}"
    served = [str(field(i, "slug", "problem_slug")) for i in field(response.json(), "items")]
    stored = [r["slug"] for r in backend.query(
        "SELECT p.slug FROM study_plan_items i JOIN study_plans s ON i.plan_id = s.id "
        "JOIN problems p ON i.problem_id = p.id WHERE s.slug = %s ORDER BY i.position", (FEATURED_PLAN_SLUG,))]
    assert served == stored and served, f"the plan serves {served[:6]} against the stored order {stored[:6]}"
    for item in field(response.json(), "items"):
        assert "status" in item, f"a plan item carries no member status: {item!r}"


def test_vote_toggles_and_an_opposite_vote_moves_the_score_by_minus_two():
    """Voting again the same way removes the vote, and switching an up-vote to a down-vote moves the score by -2.
    cov: C-CF-219, C-CF-220, C-DC-42
    """
    probe = register_probe(verified=True)
    with appclient.client(probe["token"]) as member:
        _vote_sequence(member)


def _vote_sequence(member):
    post = first_post_id(member)

    def score():
        response = member.get(f"/posts/{post}")
        assert response.status_code == 200, f"the post is unreadable. {describe(response)}"
        return int(field(response.json(), "score"))

    def vote(value):
        response = member.post(f"/posts/{post}/vote", json={"value": value})
        assert response.status_code in (200, 201), f"a vote was refused. {describe(response)}"
        return response.json()

    base = score()
    current = vote(1)
    assert int(field(current, "score")) == base + 1, f"an up-vote read {current!r} from a base of {base}"
    down = vote(-1)
    assert int(field(down, "score")) == base - 1 and int(field(down, "my_vote")) == -1, (
        f"switching an up-vote to a down-vote read {down!r}; the score must move by -2"
    )
    cleared = vote(-1)
    assert int(field(cleared, "score")) == base and not field(cleared, "my_vote"), (
        f"voting down again did not remove the vote: {cleared!r}"
    )


def test_simultaneous_votes_from_one_member_leave_at_most_one_stored_vote(backend):
    """Two votes from one member on one post arriving together leave at most one stored vote row.
    cov: C-CF-221
    """
    probe = register_probe(verified=True)
    with appclient.client(probe["token"]) as a, appclient.client(probe["token"]) as b:
        post = first_post_id(a)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(lambda s: s.post(f"/posts/{post}/vote", json={"value": 1}), (a, b)))
    rows = backend.query("SELECT value FROM votes WHERE member_id = %s AND target_id::text = %s",
                         (member_id_for(backend, probe["email"]), post))
    assert len(rows) <= 1, f"two simultaneous votes left {len(rows)} vote rows for one member on one post"


def test_second_read_of_a_post_on_the_same_day_does_not_raise_its_view_count(member):
    """Reading a post a second time on the same day leaves its view count where the first read put it.
    cov: C-CF-222, C-DC-41
    """
    post = first_post_id(member)
    first = member.get(f"/posts/{post}")
    second = member.get(f"/posts/{post}")
    assert first.status_code == second.status_code == 200, f"the post is unreadable. {describe(second)}"
    assert int(field(second.json(), "view_count")) == int(field(first.json(), "view_count")), (
        f"a second read on the same day raised the view count from {field(first.json(), 'view_count')} "
        f"to {field(second.json(), 'view_count')}"
    )


def test_discussion_feed_carries_the_seeded_posts_with_a_solution_post_on_two_sum(anon, backend):
    """At least three posts are seeded, one a solution post on Two Sum, each carrying the feed fields.
    cov: C-OV-09, C-CF-216, C-DM-46, C-DC-41
    """
    response = anon.get("/posts", params={"limit": PAGE_SIZE})
    assert response.status_code == 200, f"the discussion feed is unreadable. {describe(response)}"
    posts = rows_of(response.json())
    assert len(posts) >= SEEDED_POST_MINIMUM, f"the feed carries {len(posts)} posts, fewer than {SEEDED_POST_MINIMUM}"
    for post in posts:
        for key in ("id", "title", "category", "author", "score", "view_count", "reply_count"):
            assert key in post, f"a feed entry omits {key!r}: {post!r}"
    solutions = backend.query(
        "SELECT count(*) AS n FROM posts x JOIN problems p ON x.problem_id = p.id "
        "WHERE x.kind = 'solution' AND p.slug = 'two-sum'")[0]["n"]
    assert solutions >= 1, "no solution post on 1. Two Sum is seeded"


def test_unverified_member_may_submit_but_is_forbidden_to_vote_or_register(anon):
    """A newly registered unverified member submits, and is refused as forbidden to vote or register.
    cov: C-CF-12, C-CF-13, C-CF-14, C-CF-15
    """
    probe = register_probe()
    with appclient.client(probe["token"]) as session:
        me = session.get("/me").json()
        assert str(field(me, "state")) == "unverified", f"a new account reads state {field(me, 'state')!r}"
        slug = two_sum_slug(session)
        sent = submit(session, slug, "python3", accepted_source(session, slug, "python3"))
        assert sent.status_code in (200, 201, 202), f"an unverified member could not submit. {describe(sent)}"
        voted = session.post(f"/posts/{first_post_id(session)}/vote", json={"value": 1})
        assert voted.status_code == 403, f"an unverified vote answered {voted.status_code}. {describe(voted)}"
        registered = session.post(f"/contests/{SCHEDULED_CONTEST}/register",
                                  headers={"Idempotency-Key": idempotency_key()})
        assert registered.status_code == 403, (
            f"an unverified contest registration answered {registered.status_code}. {describe(registered)}"
        )


def test_in_product_verification_moves_a_new_member_from_unverified_to_active(anon):
    """Verification completed inside the product moves the member from unverified to active.
    cov: C-CF-11, C-CF-12, C-CF-24, C-CN-04, C-DC-18, C-DC-20
    """
    probe = register_probe()
    with appclient.client(probe["token"]) as session:
        assert str(field(session.get("/me").json(), "state")) == "unverified"
        done = session.post("/auth/verify")
        assert done.status_code in (200, 201), f"verification was refused. {describe(done)}"
        me = session.get("/me").json()
    assert str(field(me, "state")) == "active", f"verification left the member in state {field(me, 'state')!r}"
    for key in ("member_id", "username", "state", "entitlement"):
        assert key in me, f"GET /api/me omits {key!r}: {sorted(me)}"
    assert str(field(me, "state")) in MEMBER_STATES


def test_contest_listing_carries_the_running_upcoming_and_past_seeded_contests(anon):
    """The contest listing places the running, scheduled and finished seeded contests in their groups.
    cov: C-CF-224, C-CF-225, C-TR-29, C-DM-42, C-DC-35
    """
    response = anon.get("/contests")
    assert response.status_code == 200, f"the contest listing is unreadable. {describe(response)}"
    body = response.json()
    groups = {name: [str(field(c, "slug")) for c in field(body, name)] for name in ("running", "upcoming", "past")}
    assert "ladder" in body, f"the contest listing carries no ladder: {sorted(body)}"
    assert RUNNING_CONTEST in groups["running"], f"{RUNNING_CONTEST} is not running: {groups}"
    assert SCHEDULED_CONTEST in groups["upcoming"], f"{SCHEDULED_CONTEST} is not upcoming: {groups}"
    assert FINISHED_CONTEST in groups["past"], f"{FINISHED_CONTEST} is not past: {groups}"
    for name in ("running", "upcoming", "past"):
        for entry in field(body, name):
            for key in ("slug", "title", "starts_at", "duration_seconds", "cadence", "state"):
                assert key in entry, f"a contest entry omits {key!r}: {entry!r}"
            assert entry["cadence"] in ("weekly", "biweekly") and entry["state"] in ("scheduled", "running", "finished")
    running = next(c for c in field(body, "running") if str(field(c, "slug")) == RUNNING_CONTEST)
    assert int(field(running, "duration_seconds")) == 14 * 86400 and running["cadence"] == "biweekly", (
        f"the running contest reads {running!r}, not a biweekly contest lasting fourteen days"
    )


def test_running_contest_problems_endpoint_serves_its_four_scored_problems(member):
    """The running contest serves its four problems with their pinned values.
    cov: C-CF-226, C-DM-43, C-DC-36
    """
    response = member.get(f"/contests/{RUNNING_CONTEST}/problems")
    assert response.status_code == 200, f"the running contest's problems are unreadable. {describe(response)}"
    served = {str(field(p, "slug")): int(field(p, "score")) for p in _entries(response.json())}
    assert served == RUNNING_CONTEST_SCORES, f"the running contest serves {served}"


def test_scheduled_contest_problems_are_not_found_and_absent_from_the_catalogue(member, anon, backend):
    """A scheduled contest's problem set answers not-found, and its problems are outside the catalogue.
    cov: C-CF-141, C-CF-230, C-DM-44
    """
    response = member.get(f"/contests/{SCHEDULED_CONTEST}/problems")
    assert response.status_code == 404, (
        f"the problem set of a contest that has not started answered {response.status_code}. {describe(response)}"
    )
    hidden = [r["slug"] for r in backend.query(
        "SELECT p.slug FROM contest_problems cp JOIN contests c ON cp.contest_id = c.id "
        "JOIN problems p ON cp.problem_id = p.id WHERE c.slug = %s", (SCHEDULED_CONTEST,))]
    assert len(hidden) == 4, f"{SCHEDULED_CONTEST} stores {len(hidden)} problems, not four"
    listed, _ = _walk_pages(anon)
    assert not set(hidden) & set(listed), f"scheduled contest problems appear in the catalogue: {set(hidden) & set(listed)}"
    for slug in hidden:
        assert anon.get(f"/problems/{slug}").status_code == 404, f"the scheduled problem {slug} is readable"


def test_submission_in_an_unregistered_contest_context_is_refused_as_forbidden(backend):
    """A submission in the context of a contest the member did not register for is forbidden and writes nothing.
    cov: C-CF-139, C-CF-140
    """
    probe = register_probe(verified=True)
    with appclient.client(probe["token"]) as session:
        slug = two_sum_slug(session)
        response = submit_in(session, slug, "python3", accepted_source(session, slug, "python3"),
                             f"contest:{RUNNING_CONTEST}")
        assert response.status_code == 403, f"an unregistered contest submission answered {response.status_code}. {describe(response)}"
    rows = backend.query("SELECT count(*) AS n FROM submissions WHERE member_id = %s",
                         (member_id_for(backend, probe["email"]),))[0]["n"]
    assert rows == 0, f"a refused contest submission left {rows} submission rows"


def test_running_contest_penalty_counts_an_earlier_compile_error_but_not_later_or_unsolved_wrong_submissions(member, member2, subscriber):
    """Penalty adds 300 seconds for a compile error before the accepted one, and nothing for later or unsolved wrong ones.
    cov: C-CF-185, C-CF-229, C-CF-231, C-CF-232, C-CF-233, C-CF-234
    """
    context = f"contest:{RUNNING_CONTEST}"
    early, late = register_probe(verified=True), register_probe(verified=True)
    with appclient.client(early["token"]) as fast, appclient.client(late["token"]) as slow:
        slug = two_sum_slug(fast)
        for session in (fast, slow):
            joined = session.post(f"/contests/{RUNNING_CONTEST}/register", headers={"Idempotency-Key": idempotency_key()})
            assert joined.status_code in (200, 201), f"registration for the running contest failed. {describe(joined)}"
        drain((member, member2, subscriber, fast, slow), slug)
        before = counters(fast, slug)
        compile_error = judge_in(slow, slug, "python3", program(slow, slug, SYNTAX_ERROR_SOURCE), context)
        assert str(field(compile_error, "verdict")) == "Compile Error"
        assert str(field(judge_in(fast, slug, "python3", accepted_source(fast, slug, "python3"), context), "verdict")) == "Accepted"
        assert str(field(judge_in(slow, slug, "python3", accepted_source(slow, slug, "python3"), context), "verdict")) == "Accepted"
        assert str(field(judge_in(slow, slug, "python3", program(slow, slug, WRONG_SOURCE), context), "verdict")) == "Wrong Answer"
        unsolved = judge_in(slow, "add-two-numbers", "python3", "def broken(:\n", context)
        assert str(field(unsolved, "verdict")) in ("Compile Error", "Wrong Answer", "Runtime Error")
        assert counters(fast, slug) == before, "contest submissions moved Two Sum's public counters before the contest ended"
        rows, cursor = [], None
        for _ in range(20):
            params = {"limit": PAGE_SIZE}
            if cursor is not None:
                params["after"] = cursor
            page_rows = _entries(fast.get(f"/contests/{RUNNING_CONTEST}/ranking", params=params).json())
            rows.extend(page_rows)
            if len(page_rows) < PAGE_SIZE:
                break
            cursor = field(page_rows[-1], "rank")
    by_name = {str(field(r, "username")): r for r in rows}
    assert early["username"] in by_name and late["username"] in by_name, "a probe participant is missing from the standings"
    fast_row, slow_row = by_name[early["username"]], by_name[late["username"]]
    assert int(field(fast_row, "score")) == int(field(slow_row, "score")) == RUNNING_CONTEST_SCORES["two-sum"]
    gap = int(field(slow_row, "penalty")) - int(field(fast_row, "penalty"))
    assert CONTEST_PENALTY_SECONDS <= gap < 2 * CONTEST_PENALTY_SECONDS, (
        f"the penalty gap is {gap}s; one earlier compile error adds exactly {CONTEST_PENALTY_SECONDS}s, and the "
        f"later wrong answer and the unsolved problem add nothing"
    )
    assert int(field(fast_row, "rank")) < int(field(slow_row, "rank")), "the lower penalty does not rank first on an equal total"


def test_contest_penalty_counts_only_prior_wrong_submissions(member):
    """In the finished contest a competitor who solved nothing carries no penalty.
    cov: C-CF-233, C-DC-38
    """
    response = member.get(f"/contests/{FINISHED_CONTEST}/ranking", params={"limit": PAGE_SIZE})
    assert response.status_code == 200, f"the finished contest standings are unreadable. {describe(response)}"
    rows = _entries(response.json())
    assert rows, "the finished contest has no standings"
    for row in rows:
        for key in ("rank", "username", "score", "penalty", "solved"):
            assert key in row, f"a standings row omits {key!r}: {row!r}"
        if int(field(row, "score")) == 0:
            assert int(field(row, "penalty")) == 0, f"a competitor who solved nothing carries a penalty: {row!r}"


def test_contest_standings_order_by_total_then_penalty(member):
    """Standings order by total descending, then penalty ascending, and repeated reads agree.
    cov: C-CF-235, C-CF-236
    """
    rows = _entries(member.get(f"/contests/{FINISHED_CONTEST}/ranking", params={"limit": PAGE_SIZE}).json())
    keyed = [(-int(field(r, "score")), int(field(r, "penalty"))) for r in rows]
    assert keyed == sorted(keyed), f"the standings are not ordered by total then penalty: {keyed[:6]}"
    again = _entries(member.get(f"/contests/{FINISHED_CONTEST}/ranking", params={"limit": PAGE_SIZE}).json())
    assert [str(field(r, "username")) for r in again] == [str(field(r, "username")) for r in rows], (
        "two identical reads of the standings returned a different order"
    )


def test_contest_registration_is_stored_once_per_member(backend):
    """Two simultaneous registrations for one contest leave exactly one stored participation.
    cov: C-CF-228, C-DM-25, C-DC-37
    """
    probe = register_probe(verified=True)
    with appclient.client(probe["token"]) as a, appclient.client(probe["token"]) as b:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            responses = list(pool.map(
                lambda s: s.post(f"/contests/{SCHEDULED_CONTEST}/register", headers={"Idempotency-Key": idempotency_key()}),
                (a, b)))
    assert any(r.status_code in (200, 201) for r in responses), (
        "neither registration for the scheduled contest was accepted: " + " | ".join(describe(r) for r in responses)
    )
    rows = backend.query(
        "SELECT count(*) AS n FROM participations pa JOIN contests c ON pa.contest_id = c.id "
        "WHERE c.slug = %s AND pa.member_id = %s", (SCHEDULED_CONTEST, member_id_for(backend, probe["email"])))[0]["n"]
    assert rows == 1, f"two simultaneous registrations left {rows} participations"


def test_eu_price_list_is_seeded_unavailable_and_subscribing_there_is_rejected(anon):
    """The EU list in eur is seeded at 3200 and 14900 but not available, and subscribing in EU is invalid input.
    cov: C-OV-10, C-CF-245, C-CF-246, C-CF-247
    """
    response = anon.get("/prices", params={"region": EU_REGION})
    assert response.status_code == 200, f"the EU price list is unreadable. {describe(response)}"
    rows = {str(field(r, "plan")): r for r in _entries(response.json())}
    assert int(field(rows["monthly"], "amount_minor")) == EU_MONTHLY_MINOR
    assert int(field(rows["yearly"], "amount_minor")) == EU_YEARLY_MINOR
    for row in rows.values():
        assert str(field(row, "currency")) == EU_CURRENCY and field(row, "available") is False, (
            f"the EU price reads {row!r}, not an unavailable eur price"
        )
        assert "effective_from" in row and "effective_to" in row, f"an EU price carries no effective window: {row!r}"
    probe = register_probe(verified=True)
    with appclient.client(probe["token"]) as session:
        refused = session.post("/subscribe", json={"plan": "yearly", "region": EU_REGION},
                               headers={"Idempotency-Key": idempotency_key()})
        assert refused.status_code == 400, f"subscribing in EU answered {refused.status_code}. {describe(refused)}"
        assert not field(session.get("/me").json(), "entitlement"), "a refused EU subscription granted an entitlement"


def test_price_list_rows_are_integer_minor_units(anon):
    """Every price is an integer of the currency's minor unit with its currency code and an effective window.
    cov: C-CF-240, C-CF-241, C-CF-245, C-DC-39
    """
    response = anon.get("/prices", params={"region": PRICE_REGION})
    assert response.status_code == 200, f"the price list is unreadable. {describe(response)}"
    by_plan = {str(field(r, "plan")): r for r in _entries(response.json())}
    for plan in ("monthly", "yearly"):
        row = by_plan[plan]
        for key in ("region", "currency", "amount_minor", "list_amount_minor", "available", "effective_from", "effective_to"):
            assert key in row, f"the {plan} price omits {key!r}: {row!r}"
        assert isinstance(row["amount_minor"], int), f"the {plan} amount {row['amount_minor']!r} is not an integer"
        assert str(row["currency"]).lower() == PRICE_CURRENCY and row["available"] is True
    assert by_plan["monthly"]["amount_minor"] == PRICE_MONTHLY_MINOR
    assert by_plan["yearly"]["amount_minor"] == PRICE_YEARLY_MINOR
    assert by_plan["yearly"]["list_amount_minor"] == PRICE_YEARLY_LIST_MINOR


def test_subscribing_serves_the_gated_statement_on_the_next_request(anon):
    """Subscribing in-product records the yearly US term, and the next read of a gated statement is served.
    cov: C-OV-12, C-CF-255, C-CN-03, C-DC-40
    """
    slug = premium_slug(anon)
    probe = register_probe(verified=True)
    with appclient.client(probe["token"]) as session:
        assert session.get(f"/problems/{slug}").status_code == 402, "the gated statement was served before subscribing"
        granted = session.post("/subscribe", json={"plan": "yearly", "region": PRICE_REGION},
                               headers={"Idempotency-Key": idempotency_key()})
        assert granted.status_code in (200, 201), f"subscribing was refused. {describe(granted)}"
        body = granted.json()
        for key in ("plan", "region", "currency", "amount_minor", "period_start", "period_end", "state"):
            assert key in body, f"the subscription answer omits {key!r}: {body!r}"
        assert (body["plan"], body["region"], body["currency"], body["amount_minor"], body["state"]) == (
            "yearly", PRICE_REGION, PRICE_CURRENCY, PRICE_YEARLY_MINOR, "active"), f"the subscription reads {body!r}"
        served = session.get(f"/problems/{slug}")
        assert served.status_code == 200, f"the next read after subscribing was refused. {describe(served)}"


def test_subscribing_twice_stores_one_active_entitlement(backend):
    """Pressing subscribe twice leaves exactly one active entitlement row for the member.
    cov: C-CF-256
    """
    probe = register_probe(verified=True)
    with appclient.client(probe["token"]) as session:
        for _ in range(2):
            response = session.post("/subscribe", json={"plan": "yearly", "region": PRICE_REGION},
                                    headers={"Idempotency-Key": idempotency_key()})
            assert response.status_code in (200, 201, 409), f"subscribing was refused. {describe(response)}"
    rows = backend.query("SELECT count(*) AS n FROM entitlements WHERE member_id = %s AND state = 'active'",
                         (member_id_for(backend, probe["email"]),))[0]["n"]
    assert rows == 1, f"subscribing twice left {rows} active entitlements"


def test_unauthenticated_submission_is_denied(anon):
    """A caller with no session cannot submit a solution.
    cov: C-RL-03, C-RL-15, C-DC-14
    """
    slug = two_sum_slug(anon)
    response = submit(anon, slug, "python3", accepted_source(anon, slug, "python3"))
    assert response.status_code == 401, f"an anonymous submission answered {response.status_code}. {describe(response)}"
    assert str(field(response.json(), "type")) == "unauthorized", f"the refusal type is wrong. {describe(response)}"


def test_unauthenticated_draft_write_vote_and_registration_are_denied(anon):
    """A caller with no session cannot write a service draft, vote or register for a contest.
    cov: C-RL-04, C-CF-119
    """
    slug = two_sum_slug(anon)
    draft = anon.put(f"/drafts/{slug}", json={"language": "python3", "body": "# anonymous\n", "version": 0})
    assert draft.status_code == 401, f"an anonymous draft write answered {draft.status_code}. {describe(draft)}"
    vote = anon.post(f"/posts/{first_post_id(anon)}/vote", json={"value": 1})
    assert vote.status_code == 401, f"an anonymous vote answered {vote.status_code}. {describe(vote)}"
    joined = anon.post(f"/contests/{SCHEDULED_CONTEST}/register", headers={"Idempotency-Key": idempotency_key()})
    assert joined.status_code == 401, f"an anonymous registration answered {joined.status_code}. {describe(joined)}"


def test_seeded_accounts_sign_in_with_the_corpus_password(anon):
    """Each seeded account signs in with the pinned password, answering its username and an access token.
    cov: C-RL-19, C-RL-20, C-RL-21, C-RL-22, C-CF-01, C-CF-02, C-CF-08, C-DC-16
    """
    for email, username in ((MEMBER_EMAIL, MEMBER_USERNAME), (MEMBER2_EMAIL, MEMBER2_USERNAME),
                            (SUBSCRIBER_EMAIL, SUBSCRIBER_USERNAME)):
        response = anon.post("/auth/login", json={"email": email, "password": SEED_PASSWORD})
        assert response.status_code == 200, f"the seeded account {email} could not sign in. {describe(response)}"
        body = response.json()
        for key in ("access_token", "member_id", "username", "state"):
            assert body.get(key), f"sign-in for {email} omits {key!r}. {describe(response)}"
        assert body["username"] == username, f"{email} signs in as {body['username']!r}, not {username!r}"
    bad = anon.post("/auth/login", json={"email": MEMBER_EMAIL, "password": "not-the-password"})
    assert bad.status_code == 401, f"a wrong password answered {bad.status_code}. {describe(bad)}"


def test_registration_answers_identically_for_a_known_address(anon, backend):
    """Registration answers the same for a known address, creates no second account, and keeps the original password.
    cov: C-RL-18, C-CF-22, C-CF-23, C-DC-15
    """
    fresh = anon.post("/auth/register", json={"email": probe_email(), "username": f"probe{probe_token()}",
                                              "password": SEED_PASSWORD})
    other_password = f"changed-{probe_token()}"
    repeat = anon.post("/auth/register", json={"email": MEMBER_EMAIL, "username": f"probe{probe_token()}",
                                               "password": other_password})
    assert repeat.status_code == fresh.status_code, (
        f"registering the seeded address answered {repeat.status_code} while a fresh one answered {fresh.status_code}"
    )
    assert sorted(repeat.json()) == sorted(fresh.json()), (
        f"the two registration answers differ in shape: {sorted(repeat.json())} against {sorted(fresh.json())}"
    )
    assert backend.query("SELECT count(*) AS n FROM members WHERE lower(email) = %s", (MEMBER_EMAIL,))[0]["n"] == 1
    assert anon.post("/auth/login", json={"email": MEMBER_EMAIL, "password": SEED_PASSWORD}).status_code == 200
    assert anon.post("/auth/login", json={"email": MEMBER_EMAIL, "password": other_password}).status_code == 401


def test_password_below_the_minimum_length_is_rejected_and_never_echoed(anon):
    """A seven-character password is invalid input, a 128-character one is accepted, and no response echoes either.
    cov: C-CF-06, C-CF-07, C-CF-09
    """
    short = "Sh0rt-7"
    refused = anon.post("/auth/register", json={"email": probe_email(), "username": f"probe{probe_token()}",
                                                "password": short})
    assert refused.status_code == 400, f"a {len(short)}-character password answered {refused.status_code}. {describe(refused)}"
    assert short not in refused.text, "the refused password was echoed in the error response"
    long_password = ("long-password-" * 10)[:PASSWORD_MAXIMUM_FLOOR]
    email = probe_email()
    accepted = anon.post("/auth/register", json={"email": email, "username": f"probe{probe_token()}",
                                                 "password": long_password})
    assert accepted.status_code in (200, 201), f"a 128-character password was refused. {describe(accepted)}"
    assert long_password not in accepted.text
    signed_in = anon.post("/auth/login", json={"email": email, "password": long_password})
    assert signed_in.status_code == 200 and long_password not in signed_in.text
    wrong = anon.post("/auth/login", json={"email": email, "password": long_password + "x"})
    assert wrong.status_code == 401 and long_password not in wrong.text


def test_five_failed_sign_ins_lock_the_account_with_the_wrong_password_message(anon, backend):
    """Five consecutive failed sign-ins lock the account, refused with exactly the wrong-password answer.
    cov: C-CF-08, C-CF-16, C-CF-17
    """
    probe = register_probe(verified=True)
    answers = [anon.post("/auth/login", json={"email": probe["email"], "password": f"wrong-{index}"})
               for index in range(LOCKOUT_ATTEMPTS)]
    assert all(a.status_code == 401 for a in answers), "a wrong password was not refused as unauthenticated"
    locked = anon.post("/auth/login", json={"email": probe["email"], "password": probe["password"]})
    assert locked.status_code == answers[0].status_code, (
        f"after {LOCKOUT_ATTEMPTS} failures the correct password answered {locked.status_code}. {describe(locked)}"
    )
    assert field(locked.json(), "message") == field(answers[0].json(), "message"), (
        "the locked refusal reads differently from a wrong password, so a caller can tell the two apart"
    )
    state = backend.query("SELECT state FROM members WHERE email = %s", (probe["email"],))[0]["state"]
    assert state == "locked", f"the account reads state {state!r} after {LOCKOUT_ATTEMPTS} failures"


def test_address_normalisation_lowercases_only_the_domain_for_sign_in(anon):
    """An address differing only in its domain case signs in to the same account; the local part is kept exactly.
    cov: C-CF-18, C-CF-19
    """
    token = probe_token()
    upper_domain = f"Probe-{token}@EXAMPLE.COM"
    created = anon.post("/auth/register", json={"email": upper_domain, "username": f"probe{token}",
                                                "password": SEED_PASSWORD})
    assert created.status_code in (200, 201), f"registration was refused. {describe(created)}"
    first = anon.post("/auth/login", json={"email": f"Probe-{token}@example.com", "password": SEED_PASSWORD})
    assert first.status_code == 200, f"the lowercased domain did not sign in to the account. {describe(first)}"
    lower_local = f"probe-{token}@example.com"
    anon.post("/auth/register", json={"email": lower_local, "username": f"probe{token}x", "password": SEED_PASSWORD})
    second = anon.post("/auth/login", json={"email": lower_local, "password": SEED_PASSWORD})
    assert second.status_code == 200, f"a different local part was not registered as its own account. {describe(second)}"
    assert field(second.json(), "member_id") != field(first.json(), "member_id"), (
        "a local part differing only in case signed in to the same account, so the local part was not preserved"
    )


def test_username_colliding_case_insensitively_or_by_confusable_is_rejected(anon):
    """A username matching an existing one by case or by confusable folding is invalid input.
    cov: C-CF-20, C-CF-21
    """
    for candidate in (MEMBER_USERNAME.upper(), "nаdia_roux"):
        response = anon.post("/auth/register", json={"email": probe_email(), "username": candidate,
                                                     "password": SEED_PASSWORD})
        assert response.status_code == 400, (
            f"the username {candidate!r} collides with {MEMBER_USERNAME} but answered {response.status_code}. "
            f"{describe(response)}"
        )


def test_sign_out_refuses_that_bearer_token_and_leaves_other_sessions_signed_in(anon):
    """Signing out ends that server-side session at once, leaves another device signed in, and answers the same either way.
    cov: C-CF-05, C-CF-28, C-CF-29, C-DC-17
    """
    probe = register_probe(verified=True)
    other = appclient.login(probe["email"], probe["password"])
    with appclient.client(probe["token"]) as first, appclient.client(other) as second:
        ended = first.post("/auth/logout")
        assert ended.status_code == 200, f"signing out failed. {describe(ended)}"
        assert first.get("/me").status_code == 401, "a bearer token still worked after its session was signed out"
        assert second.get("/me").status_code == 200, "signing out one session ended another device's session"
        repeat = first.post("/auth/logout")
    anonymous = anon.post("/auth/logout")
    assert repeat.status_code == anonymous.status_code == ended.status_code, (
        f"sign-out answered {ended.status_code}, then {repeat.status_code} without a session, then "
        f"{anonymous.status_code} anonymously; it must answer the same whether or not a session existed"
    )


def test_session_list_names_devices_and_ending_one_signs_that_device_out(anon):
    """The sessions list carries each device label and last-seen time, and ending one signs that device out.
    cov: C-CF-26, C-CF-27, C-DC-19
    """
    probe = register_probe(verified=True)
    other = appclient.login(probe["email"], probe["password"])
    with appclient.client(probe["token"]) as first, appclient.client(other) as second:
        listing = first.get("/sessions")
        assert listing.status_code == 200, f"the sessions list is unreadable. {describe(listing)}"
        sessions = _entries(listing.json())
        assert len(sessions) >= 2, f"two signed-in devices list {len(sessions)} sessions"
        for entry in sessions:
            for key in ("id", "device_label", "last_seen_at", "current"):
                assert key in entry, f"a session entry omits {key!r}: {entry!r}"
        foreign = next(s for s in sessions if not s["current"])
        ended = first.delete(f"/sessions/{foreign['id']}")
        assert ended.status_code in (200, 204), f"ending another session failed. {describe(ended)}"
        assert second.get("/me").status_code == 401, "the ended session still signs that device in"
        assert first.get("/me").status_code == 200, "ending another session signed out the current one"


def test_session_cookie_alone_is_refused_on_the_api(anon):
    """Sign-in sets a session cookie, and that cookie alone is never accepted on `/api`.
    cov: C-CF-03, C-CF-04
    """
    probe = register_probe(verified=True)
    response = anon.post("/auth/login", json={"email": probe["email"], "password": probe["password"]})
    assert response.status_code == 200 and response.cookies, (
        f"sign-in set no session cookie for browser use. {describe(response)}"
    )
    with httpx.Client(base_url=appclient.api_base(), timeout=appclient.TIMEOUT, cookies=response.cookies) as cookie_only:
        me = cookie_only.get("/me")
    assert me.status_code == 401, f"the session cookie alone was accepted on /api/me. {describe(me)}"


def test_failure_envelope_carries_type_message_code_and_a_trace_matching_the_correlation_header(anon, member):
    """Every failure answers one envelope whose trace equals the X-Correlation-Id header on the response.
    cov: C-CF-46, C-TR-08, C-TR-15, C-TR-16, C-TR-17, C-TR-18, C-DC-13
    """
    failures = [
        (anon.get("/problems", params={"status": "solved"}), 400, "invalid_data"),
        (anon.get("/me"), 401, "unauthorized"),
        (member.get(f"/problems/{premium_slug(anon)}"), 402, "payment_required"),
        (member.get(f"/problems/no-such-problem-{probe_token()}"), 404, "not_found"),
    ]
    for response, status, kind in failures:
        assert response.status_code == status, f"expected {status}. {describe(response)}"
        body = response.json()
        for key in ("type", "message", "code", "trace"):
            assert body.get(key), f"the failure omits {key!r}. {describe(response)}"
        assert body["type"] == kind and body["type"] in FAILURE_TYPES, f"the failure type reads {body['type']!r}"
        assert body["trace"] == response.headers.get("X-Correlation-Id"), (
            f"the failure trace {body['trace']!r} is not the X-Correlation-Id header "
            f"{response.headers.get('X-Correlation-Id')!r}"
        )
        assert "Traceback" not in body["message"] and "    at " not in body["message"], (
            f"a failure message carries a stack trace: {body['message'][:200]!r}"
        )
    for response in (anon.get("/health"), anon.get("/problems", params={"limit": 1})):
        assert response.headers.get("X-Correlation-Id"), f"a successful response carries no X-Correlation-Id. {describe(response)}"


def test_health_route_answers_two_hundred_at_verification_time_through_the_public_url_on_port_4173(anon):
    """At verification time the health route answers 200 at APP_PUBLIC_URL from outside the app container.
    cov: C-TR-05, C-TR-07, C-DC-01, C-DC-02, C-DC-03, C-DC-04, C-DC-05, C-DC-09, C-DC-10
    """
    response = anon.get("/health")
    assert response.status_code == 200, f"the health route did not answer 200. {describe(response)}"
    assert "status" in response.json(), f"the health answer carries no status. {describe(response)}"
    assert str(response.request.url).startswith(appclient.api_base()), "the API is not served under /api on the public origin"


def test_admin_address_answers_not_found(page):
    """No operator console ships: `/admin/` answers not-found.
    cov: C-CN-07
    """
    response = page.get("/admin/")
    assert response.status_code == 404, f"/admin/ answered {response.status_code}. {describe(response)}"


def test_member_only_route_redirects_to_sign_in_carrying_the_intended_path():
    """An unauthenticated request for a member-only route lands on sign-in carrying the intended path.
    cov: C-UF-05, C-UF-06
    """
    with httpx.Client(base_url=appclient.app_url(), timeout=appclient.TIMEOUT, follow_redirects=False) as raw:
        for route in MEMBER_ONLY_ROUTES:
            response = raw.get(route)
            assert response.status_code in (301, 302, 303, 307, 308), (
                f"a signed-out request for {route} answered {response.status_code} rather than a redirect"
            )
            location = urllib.parse.unquote(response.headers.get("location", ""))
            assert "/accounts/login/" in location and route in location, (
                f"{route} redirected to {location!r}, which does not carry the intended path to sign-in"
            )


def test_route_table_public_addresses_and_footer_pages_answer_with_a_page(page, anon):
    """Every public route in the route table answers with a page, including footer and interview pages.
    cov: C-OV-11, C-CF-209, C-CF-214, C-CF-237, C-UF-01, C-UF-02, C-UF-03, C-UF-04, C-CN-02, C-CN-05
    """
    post = first_post_id(anon)
    routes = list(PUBLIC_ROUTES) + list(FOOTER_ROUTES) + list(INTERVIEW_ROUTES) + [
        f"/contest/{FINISHED_CONTEST}/", f"/contest/{FINISHED_CONTEST}/ranking/",
        f"/studyplan/{FEATURED_PLAN_SLUG}/", f"/discuss/post/{post}/", f"/u/{MEMBER_USERNAME}/",
    ] + [f"/explore/{card}/" for card in EXPLORE_CARD_SLUGS]
    for route in routes:
        response = page.get(route)
        assert response.status_code == 200, f"the public route {route} answered {response.status_code}. {describe(response)}"
        assert "<html" in response.text.lower(), f"{route} answered without a page"
        assert not FILE_INPUT.search(response.text), f"{route} offers a file input"
    probe = register_probe()
    with httpx.Client(base_url=appclient.app_url(), timeout=appclient.TIMEOUT, follow_redirects=True) as browser_like:
        signed = browser_like.post("/api/auth/login", json={"email": probe["email"], "password": probe["password"]})
        assert signed.status_code == 200, f"the probe could not sign in for the member routes. {describe(signed)}"
        for route in MEMBER_ONLY_ROUTES:
            response = browser_like.get(route)
            assert response.status_code == 200, f"the member route {route} answered {response.status_code} with a session"
            assert not FILE_INPUT.search(response.text), f"the member route {route} offers a file input"


def test_workspace_tabs_are_real_addresses_under_the_problem_slug(page):
    """The four workspace tabs answer at their own addresses, and signed out the submissions tab prompts sign-in.
    cov: C-CF-88, C-CF-89, C-CF-90, C-CF-92
    """
    for tab in ("description", "editorial", "solutions", "submissions"):
        response = page.get(f"/problems/two-sum/{tab}/")
        assert response.status_code == 200, f"the {tab} tab answered {response.status_code}. {describe(response)}"
    submissions = page.get("/problems/two-sum/submissions/").text.lower()
    assert "sign in" in submissions or "log in" in submissions, (
        "signed out, the submissions tab shows no sign-in prompt"
    )
    unknown = page.get(f"/problems/no-such-problem-{probe_token()}/description/")
    assert unknown.status_code == 404 and "<html" in unknown.text.lower(), (
        f"an unknown problem slug answered {unknown.status_code} without the product's not-found page"
    )


def test_unsolved_description_markup_omits_topic_tag_names_and_image_elements(page):
    """The delivered description markup of an unsolved problem carries no topic tag name and no image element.
    cov: C-CF-94, C-CF-95, C-CF-98, C-CF-101
    """
    response = page.get("/problems/two-sum/description/")
    assert response.status_code == 200, f"the description tab is unreadable. {describe(response)}"
    assert "Hash Table" not in response.text, "the closed Topics disclosure delivered the Hash Table tag name in the markup"
    assert "<img" not in response.text.lower(), "the statement markup carries an image element"
    for label in ("Input", "Output", "Topics", "Discussion"):
        assert label in response.text, f"the description tab does not render {label!r}"


def test_catalogue_first_response_is_server_rendered_with_rows_copy_and_htmx_attributes(page):
    """The catalogue's first response already carries its rows, its control copy and hx- attributes.
    cov: C-CF-34, C-CF-64, C-CF-76, C-CF-78, C-CF-79, C-CF-80, C-CF-81, C-TR-02, C-TR-03
    """
    response = page.get("/problemset/")
    assert response.status_code == 200, f"the catalogue route is unreadable. {describe(response)}"
    html = response.text
    assert "Two Sum" in html and "Add Two Numbers" in html, "the first catalogue response carries no rows"
    assert re.search(r"\shx-(get|post|put|delete|trigger|target|swap)=", html), "the catalogue markup carries no hx- attribute"
    for text in ("Search questions", "0/240 Solved", "Weekly Premium", "W1", "W5", "Redeem", "Rules",
                 "Search for a company...", "Expand") + CATEGORY_PILLS:
        assert text in html, f"the catalogue does not render {text!r}"
    assert "Med." in html, "catalogue rows do not render the Med. difficulty word"


def test_workspace_markup_renders_console_tabs_and_toolbar_labels(page):
    """The workspace renders the console tabs and the toolbar controls by name.
    cov: C-CF-121, C-CF-128
    """
    html = page.get("/problems/two-sum/description/").text
    for label in ("Testcase", "Result", "Debugger", "Reset", "Format", "Copy", "Run", "Submit", "Notes", "Timer"):
        assert label in html, f"the workspace does not render {label!r}"


def test_learning_contest_and_discussion_pages_render_their_pinned_copy(page):
    """Study plans, explore cards, contests and discussion render their seeded names and labels.
    cov: C-CF-205, C-CF-207, C-CF-208, C-CF-217, C-CF-227
    """
    plans = page.get("/studyplan/").text
    for text in STUDY_PLAN_NAMES + STUDY_PLAN_GROUPS + STUDY_PLAN_SUBTITLES:
        assert text in plans, f"/studyplan/ does not render {text!r}"
    contests = page.get("/contest/").text
    assert "0 / 4" in contests, "/contest/ renders no past contest reading 0 / 4"
    discuss = page.get("/discuss/").text
    for text in DISCUSSION_ORDERS:
        assert text in discuss, f"/discuss/ does not offer the {text!r} order"
    explore = page.get("/explore/").text
    for card in EXPLORE_CARD_SLUGS:
        assert f"/explore/{card}/" in explore, f"/explore/ does not link the seeded card {card}"


def test_subscribe_page_renders_prices_saving_and_per_month_figure(page):
    """The pricing route renders both terms, the strike price, the computed saving and the per-month figure.
    cov: C-CF-242, C-CF-243, C-CF-244
    """
    html = page.get("/subscribe/").text
    for text in PRICE_DISPLAY:
        assert text in html, f"/subscribe/ does not render {text!r}"


def test_favicon_is_declared_and_resolves_as_a_vector_document(page):
    """The site declares a favicon in the document head and serves it as a vector document.
    cov: C-TR-21
    """
    home = page.get("/")
    assert home.status_code == 200, f"the marketing route is unreachable. {describe(home)}"
    declared = re.findall(r'<link[^>]+rel="[^"]*icon[^"]*"[^>]*>', home.text, re.I)
    assert declared, "the document head declares no favicon link"
    href = re.search(r'href="([^"]+)"', declared[0])
    served = page.get(href.group(1))
    assert served.status_code == 200, f"the declared favicon does not resolve. {describe(served)}"
    assert "svg" in served.headers.get("content-type", ""), (
        f"the favicon is served as {served.headers.get('content-type')!r}, not a vector document"
    )


def test_public_routes_carry_unique_titles_and_a_social_preview(page):
    """Every public route carries its own title and description, and a social preview image from this origin.
    cov: C-TR-19, C-TR-20
    """
    titles, descriptions = {}, {}
    for route in PUBLIC_ROUTES:
        response = page.get(route)
        assert response.status_code == 200, f"the public route {route} is unreachable. {describe(response)}"
        html = response.text
        title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        description = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', html, re.I)
        assert title and title.group(1).strip(), f"{route} carries no document title"
        assert description and description.group(1).strip(), f"{route} carries no meta description"
        assert re.search(r'<meta[^>]+property="og:title"', html, re.I), f"{route} declares no social preview title"
        image = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html, re.I)
        assert image, f"{route} declares no social preview image"
        target = urllib.parse.urlparse(image.group(1))
        assert not target.netloc or target.netloc == urllib.parse.urlparse(appclient.app_url()).netloc, (
            f"{route} points its social preview at another origin: {image.group(1)}"
        )
        assert page.get(target.path).status_code == 200, f"the social preview image of {route} does not resolve"
        assert title.group(1) not in titles, f"{route} shares its title with {titles.get(title.group(1))}"
        assert description.group(1) not in descriptions, f"{route} shares its description with {descriptions.get(description.group(1))}"
        titles[title.group(1)] = route
        descriptions[description.group(1)] = route


def test_internal_links_on_public_routes_resolve(page):
    """Every internal link on the public routes resolves rather than answering not-found.
    cov: C-CF-83, C-CF-84
    """
    checked = set()
    for route in PUBLIC_ROUTES:
        response = page.get(route)
        assert response.status_code == 200, f"{route} is unreachable. {describe(response)}"
        for href in re.findall(r'href="(/[^"#?]*)"', response.text):
            if href in checked:
                continue
            checked.add(href)
            target = page.get(href)
            assert target.status_code == 200, f"the internal link {href} on {route} answered {target.status_code}"
    for label in FOOTER_LABELS + RAIL_LABELS:
        assert any(label in page.get(route).text for route in ("/", "/problemset/")), f"no public route links {label!r}"
    assert checked, "no internal link was found on the public routes"


def test_unknown_address_renders_the_products_not_found_page(page):
    """An unknown address renders the product's own not-found page inside the shell and answers not-found.
    cov: C-CF-86
    """
    response = page.get(f"/no-such-route-{probe_token()}/")
    assert response.status_code == 404, f"an unknown address answered {response.status_code}. {describe(response)}"
    assert "<html" in response.text.lower(), "an unknown address answered with no page body"
    assert "/problemset/" in response.text, "the not-found page carries no way back to the catalogue"


def test_every_browser_request_stays_on_the_app_origin_with_no_binary_asset_or_dev_client(browser_page):
    """Loading the public routes fetches only same-origin, non-binary assets, with no dev client and no credential.
    cov: C-OV-13, C-TR-22, C-TR-23, C-TR-24, C-TR-25, C-CN-06, C-DC-08
    """
    origin = urllib.parse.urlparse(appclient.app_url()).netloc
    seen = []
    browser_page.on("response", lambda r: seen.append((r.url, r.headers.get("content-type", ""))))
    bodies = []
    for route in ("/", "/problemset/", "/problems/two-sum/description/", "/subscribe/"):
        open_route(browser_page, route)
        bodies.append(browser_page.content())
    for url, kind in seen:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme in ("data", "blob", "about"):
            continue
        assert parsed.netloc == origin, f"the browser fetched {url} from another origin"
        assert not re.match(r"(image/(png|jpe?g|gif|webp|avif|x-icon)|font/|application/font|video/)", kind), (
            f"the browser fetched a binary asset {url} ({kind})"
        )
        assert not re.search(r"(@vite/client|livereload|__webpack_hmr|browser-sync|hot-update)", url), (
            f"the served pages load a development client: {url}"
        )
    joined = " ".join(bodies)
    for secret in ("postgresql://", "DATABASE_URL", "deku-local-dev", "DB_ADMIN_URL"):
        assert secret not in joined, f"a served page carries the credential marker {secret!r}"


def test_body_text_is_fourteen_on_twenty_one_in_the_system_stack_with_monospace_code(browser_page):
    """Body text computes to 14px on 21px in the system stack, and the editor uses the monospace stack.
    cov: C-UX-18, C-UX-19
    """
    open_route(browser_page, "/problemset/")
    style = browser_page.evaluate(
        "() => { const s = getComputedStyle(document.body); return [s.fontSize, s.lineHeight, s.fontFamily]; }")
    assert style[0] == "14px" and style[1] == "21px", f"body text computes to {style[0]} on {style[1]}"
    assert style[2].replace('"', "").startswith("system-ui"), f"the interface stack reads {style[2]!r}"
    open_route(browser_page, "/problems/two-sum/description/")
    mono = browser_page.evaluate(
        "() => { const el = ['textarea[aria-describedby]', '[role=textbox][aria-multiline=true]', 'pre', 'code']"
        ".map(q => document.querySelector(q)).find(x => x);"
        " return el ? getComputedStyle(el).fontFamily : ''; }")
    assert "ui-monospace" in mono, f"the editor and code use {mono!r}, not the monospace stack"


def test_no_element_transitions_every_property(browser_page):
    """No rendered element asks the browser to transition `all` properties.
    cov: C-UX-27
    """
    for route in ("/", "/problemset/", "/problems/two-sum/description/"):
        open_route(browser_page, route)
        offenders = browser_page.evaluate(
            "() => Array.from(document.querySelectorAll('*')).filter(el => {"
            " const s = getComputedStyle(el);"
            " return s.transitionProperty.split(',').map(x => x.trim()).includes('all')"
            "  && s.transitionDuration.split(',').some(d => parseFloat(d) > 0); }).length")
        assert offenders == 0, f"{offenders} elements on {route} transition every property"


def test_reduced_motion_stops_every_endless_animation(chromium):
    """Under a reduced-motion preference no endless animation keeps running.
    cov: C-UX-33
    """
    context = chromium.new_context(viewport=WIDE_VIEWPORT, reduced_motion="reduce")
    tab = context.new_page()
    try:
        for route in ("/", "/problemset/"):
            open_route(tab, route)
            running = tab.evaluate(
                "() => document.getAnimations().filter(a => a.playState === 'running'"
                " && a.effect && a.effect.getComputedTiming().iterations === Infinity).length")
            assert running == 0, f"{running} endless animations keep running on {route} under reduced motion"
    finally:
        context.close()


def test_narrow_viewport_overflows_nothing_sideways(chromium):
    """At a narrow viewport no public route scrolls sideways.
    cov: C-UX-44
    """
    context = chromium.new_context(viewport=NARROW_VIEWPORT)
    tab = context.new_page()
    try:
        for route in ("/", "/problemset/", "/contest/", "/subscribe/", "/studyplan/", "/discuss/"):
            open_route(tab, route)
            widths = tab.evaluate("() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            assert widths[0] <= widths[1] + 1, f"{route} is {widths[0]}px wide inside a {widths[1]}px viewport"
    finally:
        context.close()


def test_dark_theme_follows_the_operating_system_preference(chromium):
    """With no member override the page ground follows the operating system colour scheme.
    cov: C-UX-14
    """
    grounds = {}
    for scheme in ("light", "dark"):
        context = chromium.new_context(viewport=WIDE_VIEWPORT, color_scheme=scheme)
        tab = context.new_page()
        try:
            open_route(tab, "/problemset/")
            grounds[scheme] = tab.evaluate("() => getComputedStyle(document.body).backgroundColor")
        finally:
            context.close()
    assert grounds["light"] != grounds["dark"], f"the page ground reads {grounds['light']} in both schemes"


def test_catalogue_markup_is_an_accessible_table_with_sort_state_pager_and_polite_region(browser_page):
    """The catalogue is a table with header cells, a sort state, a current page mark and a polite live region.
    cov: C-UX-47, C-UX-49
    """
    open_route(browser_page, "/problemset/")
    facts = browser_page.evaluate(
        "() => ({ headers: document.querySelectorAll('table th').length,"
        " sorted: document.querySelectorAll('th[aria-sort]').length,"
        " current: document.querySelectorAll('[aria-current=page]').length,"
        " polite: document.querySelectorAll('[aria-live=polite]').length })")
    assert facts["headers"] > 0, "the catalogue is not a table with a header row"
    assert facts["sorted"] > 0, "no catalogue header carries its sort state"
    assert facts["current"] > 0, "the pager marks no page as current"
    assert facts["polite"] > 0, "the catalogue carries no polite live region for the result count"


def test_workspace_markup_exposes_separator_tab_list_live_regions_and_a_described_editor(browser_page):
    """The workspace exposes a valued separator, a tab list, polite and assertive regions, and a described editor.
    cov: C-CF-106, C-CF-122, C-UX-50, C-UX-51
    """
    open_route(browser_page, "/problems/two-sum/description/")
    facts = browser_page.evaluate(
        "() => { const sep = document.querySelector('[role=separator]');"
        " const ed = document.querySelector('textarea[aria-describedby], textarea[aria-description], [role=textbox][aria-multiline=true]');"
        " const desc = ed ? (ed.getAttribute('aria-description') || '') + ' ' + (ed.getAttribute('aria-describedby') || '').split(' ').map(id => (document.getElementById(id) || {}).textContent || '').join(' ') : '';"
        " return { sep: !!sep && ['aria-valuenow','aria-valuemin','aria-valuemax'].every(a => sep.hasAttribute(a)),"
        " tablist: document.querySelectorAll('[role=tablist]').length,"
        " assertive: document.querySelectorAll('[aria-live=assertive]').length,"
        " polite: document.querySelectorAll('[aria-live=polite]').length,"
        " labelled: !!ed && !!(ed.getAttribute('aria-label') || ed.getAttribute('aria-labelledby')), desc: desc }; }")
    assert facts["sep"], "the workspace divider is not a separator carrying a value, a minimum and a maximum"
    assert facts["tablist"] > 0, "the console tabs are not a tab list"
    assert facts["assertive"] > 0 and facts["polite"] > 0, "the workspace lacks a polite or an assertive live region"
    assert facts["labelled"], "the editor is not a labelled multi-line text control"
    assert "Escape" in facts["desc"], f"the editor description does not state the Escape sequence: {facts['desc']!r}"


def test_contest_countdown_is_a_named_timer(browser_page):
    """The contest countdown is exposed as a named timer.
    cov: C-UX-52
    """
    open_route(browser_page, "/contest/")
    named = browser_page.evaluate(
        "() => Array.from(document.querySelectorAll('[role=timer]'))"
        ".filter(el => el.getAttribute('aria-label') || el.getAttribute('aria-labelledby')).length")
    assert named > 0, "the contest countdown is not a named timer"


def test_keyboard_shortcuts_focus_search_and_open_the_catalogue_and_contests(browser_page):
    """`/` focuses the global search, `g` then `p` opens the catalogue, `g` then `c` opens contests, `?` opens the sheet.
    cov: C-UX-53, C-UX-54
    """
    open_route(browser_page, "/contest/")
    browser_page.keyboard.press("/")
    focused = browser_page.evaluate("() => document.activeElement && document.activeElement.tagName")
    assert focused == "INPUT", f"pressing / focused {focused!r}, not the global search"
    browser_page.keyboard.press("Escape")
    browser_page.evaluate("() => document.activeElement && document.activeElement.blur()")
    browser_page.keyboard.press("g")
    browser_page.keyboard.press("p")
    browser_page.wait_for_url("**/problemset/**")
    browser_page.keyboard.press("g")
    browser_page.keyboard.press("c")
    browser_page.wait_for_url("**/contest/**")
    browser_page.keyboard.press("Shift+Slash")
    settle(0.5)
    visible = browser_page.evaluate(
        "() => Array.from(document.querySelectorAll('dialog[open], [role=dialog]'))"
        ".some(d => getComputedStyle(d).display !== 'none' && getComputedStyle(d).visibility !== 'hidden')")
    assert visible, "pressing ? opened no shortcut sheet"


def test_members_sessions_and_problem_tables_carry_the_pinned_columns_and_values(backend):
    """The members, sessions and problems tables carry their pinned columns and enumerated values.
    cov: C-CF-10, C-TR-04, C-DM-01, C-DM-03, C-DM-04, C-DM-05, C-DM-06, C-DM-07, C-DM-48, C-CN-01, C-DC-11
    """
    expected = {
        "members": {"id", "email", "username", "display_name", "password_hash", "state", "region", "theme", "created_at"},
        "sessions": {"id", "member_id", "created_at", "last_seen_at", "device_label", "revoked_at"},
        "problems": {"id", "number", "slug", "title", "difficulty", "category", "statement", "constraints", "examples",
                     "hints", "is_premium", "state", "published_at", "accepted_count", "submission_count",
                     "like_count", "dislike_count", "test_set_version"},
    }
    for table, columns in expected.items():
        missing = columns - columns_of(backend, table)
        assert not missing, f"{table} lacks the pinned columns {sorted(missing)}"
    tables = {r["table_name"] for r in backend.query(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = current_schema()")}
    above = tables & {"organisations", "organizations", "teams", "workspaces", "tenants"}
    assert not above, f"the data model carries a boundary above the member: {sorted(above)}"
    assert distinct_values(backend, "members", "state") <= set(MEMBER_STATES)
    assert distinct_values(backend, "problems", "difficulty") <= {"easy", "medium", "hard"}
    assert distinct_values(backend, "problems", "category") <= set(CATEGORIES)
    assert distinct_values(backend, "problems", "state") <= {"draft", "published", "withdrawn"}
    published = backend.query("SELECT count(*) AS n, count(DISTINCT number) AS u, count(DISTINCT slug) AS s "
                              "FROM problems WHERE state = 'published'")[0]
    assert published["n"] == published["u"] == published["s"] == CATALOGUE_TOTAL, (
        f"published problems read {published}, not {CATALOGUE_TOTAL} with unique numbers and slugs"
    )
    for email in (MEMBER_EMAIL, MEMBER2_EMAIL, SUBSCRIBER_EMAIL):
        assert backend.query("SELECT count(*) AS n FROM members WHERE email = %s", (email,))[0]["n"] == 1, (
            f"the seed stores {email} more than once"
        )


def test_tag_signature_and_test_set_tables_carry_the_pinned_columns_and_values(backend):
    """The tag, signature, test set and test case tables carry their pinned columns and enumerated values.
    cov: C-DM-01, C-DM-10, C-DM-11, C-DM-13, C-DM-15
    """
    expected = {
        "tags": {"id", "slug", "name", "kind", "problem_count"},
        "problem_tags": {"problem_id", "tag_id", "frequency"},
        "problem_signatures": {"problem_id", "language", "starter", "entry_point", "imports", "parameters",
                               "returns", "mutates", "indent"},
        "test_sets": {"problem_id", "version", "comparator", "time_limit_ms", "memory_limit_kb", "output_limit_bytes"},
        "test_cases": {"test_set_id", "index", "input", "expected", "is_example"},
    }
    for table, columns in expected.items():
        missing = columns - columns_of(backend, table)
        assert not missing, f"{table} lacks the pinned columns {sorted(missing)}"
    assert distinct_values(backend, "tags", "kind") <= {"topic", "employer"}
    assert backend.query("SELECT count(*) AS n FROM tags WHERE kind = 'topic'")[0]["n"] == TOPIC_TAG_COUNT
    buckets = distinct_values(backend, "problem_tags", "frequency")
    assert all(1 <= int(b) <= 5 for b in buckets), f"employer frequency buckets fall outside 1 to 5: {buckets}"


def test_submission_run_and_progress_tables_carry_the_pinned_columns_and_values(backend):
    """The submission, run, solved, attempted, streak and draft tables carry their pinned columns and values.
    cov: C-CF-145, C-DM-01, C-DM-09, C-DM-16, C-DM-17, C-DM-18, C-DM-19, C-DM-21
    """
    expected = {
        "submissions": {"id", "member_id", "problem_id", "language", "source", "source_hash", "test_set_version",
                        "context", "state", "verdict", "failed_case_index", "runtime_ms", "memory_kb",
                        "runtime_percentile", "memory_percentile", "attempt", "idempotency_key", "created_at",
                        "judged_at"},
        "run_requests": {"id", "member_id", "problem_id", "language", "source"},
        "solved_set": {"member_id", "problem_id", "first_accepted_at"},
        "attempted_set": {"member_id", "problem_id", "first_attempted_at"},
        "streaks": {"member_id", "current", "longest", "last_qualifying_day"},
        "drafts": {"member_id", "problem_id", "language", "body", "version", "updated_at"},
    }
    for table, columns in expected.items():
        missing = columns - columns_of(backend, table)
        assert not missing, f"{table} lacks the pinned columns {sorted(missing)}"
    assert "problem_number" not in columns_of(backend, "submissions"), "a submission references its problem by number"
    assert distinct_values(backend, "submissions", "state") <= {"pending", "judging", "done", "failed"}
    assert distinct_values(backend, "submissions", "verdict") <= set(VERDICTS)
    contexts = distinct_values(backend, "submissions", "context")
    assert all(c == "practice" or str(c).startswith("contest:") for c in contexts), f"submission contexts read {contexts}"
    kind = backend.query("SELECT data_type FROM information_schema.columns WHERE table_schema = current_schema() "
                         "AND table_name = 'streaks' AND column_name = 'last_qualifying_day'")[0]["data_type"]
    assert kind == "date", f"the last qualifying day is stored as {kind}, not a date"


def test_learning_contest_price_post_and_ledger_tables_carry_the_pinned_columns_and_values(backend):
    """The plan, contest, price, entitlement, post, vote and coin ledger tables carry their pinned columns and values.
    cov: C-DM-01, C-DM-23, C-DM-24, C-DM-26, C-DM-27, C-DM-28, C-DM-29, C-DM-48
    """
    expected = {
        "study_plans": {"slug", "title", "group", "is_featured", "is_premium", "position"},
        "study_plan_items": {"plan_id", "problem_id", "position"},
        "contests": {"slug", "title", "starts_at", "duration_seconds", "cadence", "state"},
        "contest_problems": {"contest_id", "problem_id", "position", "score"},
        "participations": {"contest_id", "member_id", "registered_at", "score", "penalty", "rank"},
        "prices": {"plan", "region", "currency", "amount_minor", "list_amount_minor", "available", "effective_from",
                   "effective_to"},
        "entitlements": {"member_id", "plan", "region", "currency", "amount_minor", "period_start", "period_end", "state"},
        "posts": {"id", "member_id", "problem_id", "kind", "language", "title", "body", "view_count", "state", "created_at"},
        "votes": {"member_id", "target_id", "value"},
        "coin_ledger": {"member_id", "sequence", "delta", "reason", "reference", "created_at"},
    }
    for table, columns in expected.items():
        missing = columns - columns_of(backend, table)
        assert not missing, f"{table} lacks the pinned columns {sorted(missing)}"
    assert "ends_at" not in columns_of(backend, "contests"), "a contest stores an end column beside its duration"
    assert distinct_values(backend, "contests", "cadence") <= {"weekly", "biweekly"}
    assert distinct_values(backend, "contests", "state") <= {"scheduled", "running", "finished"}
    assert distinct_values(backend, "entitlements", "state") <= {"active", "canceled", "expired"}
    assert distinct_values(backend, "prices", "plan") <= {"monthly", "yearly"}
    assert distinct_values(backend, "posts", "kind") <= {"discussion", "solution"}
    assert {int(v) for v in distinct_values(backend, "votes", "value")} <= {-1, 1}
    slugs = {r["slug"] for r in backend.query("SELECT slug FROM contests")}
    assert {FINISHED_CONTEST, SCHEDULED_CONTEST, RUNNING_CONTEST} <= slugs, f"seeded contests read {slugs}"
    duplicates = backend.query("SELECT slug FROM study_plans GROUP BY slug HAVING count(*) > 1")
    assert duplicates == [], f"study plans are seeded twice: {duplicates}"
