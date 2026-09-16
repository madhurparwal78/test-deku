"""Black-box grading for deku/birthday-keyed-arcade-vb.

Every assertion reads the running application over HTTP, reads the datastore
the application seeds, or drives the rendered product in Chromium through the
roles, names and copy the brief pins. Nothing imports the agent's code, inspects
its schema, or names a mechanism it was free to choose.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlparse

from conftest import (
    CLOCK_BACKWARDS,
    COLLECTION_TOTAL,
    CYCLE_DAYS,
    DAILY_GRANT,
    DATE_REFUSAL,
    EMPTY_COLLECTION,
    EVERYTHING_DELETED,
    GAME_ROUTES,
    HONOLULU,
    HUB_ORDER,
    KEPT_COPY,
    KIRITIMATI,
    LAST_ORDINAL,
    LEAP_DAY_ORDINAL,
    LINK_NOT_DESCRIBED,
    LINK_TOO_OLD,
    LINK_VERSION,
    MAX_PAGE_SIZE,
    MERGED,
    NO_STORAGE,
    ORACLE_DECK_COUNT,
    PHASES,
    PRIZE_TIERS,
    PROMPT_AGAIN,
    PUBLIC_ROUTES,
    PURSE_CONFLICT,
    REFUSE_STORAGE,
    SERIES_COUNT,
    SERIES_LABELS,
    SHARE_WARNING,
    SHARED_BOARD,
    UNREADABLE_FILE,
    WELCOME_GRANT,
    WHEEL_CATEGORY_COUNT,
    at_local,
    blank_of,
    board_is_solvable,
    choose,
    collection_entries,
    credit,
    debit,
    decode_link,
    encode_link,
    enter_machine,
    exchange,
    expect,
    expect_balance,
    find_birthday,
    import_store,
    items_of,
    kept,
    member_label,
    member_number,
    member_pattern,
    move_blank,
    prompt_shown,
    raw_file,
    read_board,
    resolve,
    sixteen,
    store_file,
)


def test_leap_day_resolves_to_ordinal_sixty(anon_client):
    """The twenty-ninth of February is an ordinary day on a 366-day cycle."""
    r = resolve(anon_client, 29, 2)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("valid") is True, body
    assert body.get("ordinal") == LEAP_DAY_ORDINAL, (
        f"29 February resolved to ordinal {body.get('ordinal')}, expected "
        f"{LEAP_DAY_ORDINAL}. A cycle counted in a common year is wrong here "
        f"and wrong for every day after it")
    members = body.get("members")
    assert isinstance(members, list) and len(members) == SERIES_COUNT, (
        f"expected {SERIES_COUNT} members, one per series, got {len(members or [])}")
    assert sorted(m["series"] for m in members) == list(range(1, SERIES_COUNT + 1))
    for m in members:
        expected = (m["series"] - 1) * CYCLE_DAYS + LEAP_DAY_ORDINAL
        assert m["number"] == expected, (
            f"series {m['series']} gave number {m['number']}, expected {expected}")

    after = resolve(anon_client, 1, 3)
    assert after.json()["ordinal"] == LEAP_DAY_ORDINAL + 1, (
        "the first of March must follow the twenty-ninth of February")


def test_resolution_is_pure_and_repeatable(anon_client):
    """The same pair resolves identically every time, with no clock involved."""
    first = resolve(anon_client, 29, 2).json()
    second = resolve(anon_client, 29, 2).json()
    assert first == second, "the same pair resolved differently on two calls"
    for day, month in ((1, 1), (15, 6), (31, 12)):
        a = resolve(anon_client, day, month).json()
        b = resolve(anon_client, day, month).json()
        assert a == b, f"{day}/{month} resolved differently on two calls"
        assert a["ordinal"] >= 1 and a["ordinal"] <= LAST_ORDINAL
    starts = [1, 32, 61, 92, 122, 153, 183, 214, 245, 275, 306, 336]
    got = [resolve(anon_client, 1, m).json()["ordinal"] for m in range(1, 13)]
    assert got == starts, (
        f"the first of each month resolved to {got}, expected {starts}. A cycle "
        f"counted in a common year is short by one from March onward")
    for key in first:
        assert key not in ("today", "year", "now", "date", "timestamp"), (
            f"a resolution carries {key!r}, so it depends on when it was asked")


def test_last_day_of_cycle_resolves_and_carries_a_colour(anon_client):
    """The thirty-first of December is ordinal 366 and carries its colour."""
    r = resolve(anon_client, 31, 12)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ordinal"] == LAST_ORDINAL, (
        f"31 December resolved to {body['ordinal']}, expected {LAST_ORDINAL}")
    colour = body.get("colour")
    assert isinstance(colour, dict) and colour.get("phase") in PHASES, (
        f"the last day of the cycle carries {colour!r} rather than one of the five "
        f"phases, which is where a scheme that truncates on the remainder goes wrong")


def test_thirty_first_of_april_refused_january_accepted(anon_client):
    """Validity is a property of the pair, never of either field alone."""
    bad = resolve(anon_client, 31, 4)
    assert bad.status_code == 400, (
        f"the thirty-first of April answered {bad.status_code}, expected a refusal")
    body = bad.json()
    assert body.get("valid") is False
    assert body.get("error") == DATE_REFUSAL, body
    assert str(body.get("impossible", "")).strip(), (
        "the refusal does not name which part is impossible")
    good = resolve(anon_client, 31, 1)
    assert good.status_code == 200, (
        "the same day 31 beside January must resolve; neither field is wrong alone")


def test_out_of_range_day_and_month_refused(anon_client):
    """Impossible pairs are refused with the product's own words."""
    for day, month in ((30, 2), (0, 5), (12, 13), (12, 0), (32, 1)):
        r = resolve(anon_client, day, month)
        assert r.status_code == 400, (
            f"{day}/{month} answered {r.status_code}, expected a refusal")
        assert r.json().get("error") == DATE_REFUSAL


def test_the_finder_resolves_the_leap_day_whatever_year_the_device_believes(devices):
    """The finder gives the same sixteen in a common year, a leap year and later."""
    for year in (2027, 2028, 2031):
        context = devices(at=datetime(year, 3, 15, 12, 0, tzinfo=timezone.utc))
        page = context.new_page()
        page.goto("/")
        find_birthday(page, 29, 2)
        members = sixteen(page)
        expect(members).to_have_count(SERIES_COUNT)
        expect(members.first.get_by_text(member_label(LEAP_DAY_ORDINAL),
                                         exact=True)).to_be_visible()
        expect(members.last.get_by_text(
            member_label(member_number(SERIES_COUNT, LEAP_DAY_ORDINAL)),
            exact=True)).to_be_visible()
        find_birthday(page, 1, 3)
        expect(members.first.get_by_text(member_label(LEAP_DAY_ORDINAL + 1),
                                         exact=True)).to_be_visible()
        find_birthday(page, 31, 12)
        expect(members.first.get_by_text(member_label(LAST_ORDINAL),
                                         exact=True)).to_be_visible()
        find_birthday(page, 31, 4)
        expect(page.get_by_text(DATE_REFUSAL, exact=True)).to_be_visible()


def test_catalogue_walks_every_member_exactly_once(anon_client):
    """Paging the whole catalogue yields 5856 members, 366 in each series."""
    seen: set[int] = set()
    per_series: dict[int, int] = {}
    cursor = None
    for _ in range(80):
        params = {"page_size": 500}
        if cursor:
            params["cursor"] = cursor
        r = anon_client.get("/api/characters", params=params)
        assert r.status_code == 200, r.text
        body = r.json()
        assert isinstance(body, dict), "a paginated read must return an object"
        rows = items_of(body)
        numbers = [row["number"] for row in rows]
        assert len(numbers) == len(set(numbers)), "a page repeated a member"
        overlap = seen & set(numbers)
        assert not overlap, (
            f"paging repeated {len(overlap)} member(s) already seen; an unstable "
            f"ordering skips and repeats rows")
        seen |= set(numbers)
        for row in rows:
            per_series[row["series"]] = per_series.get(row["series"], 0) + 1
        cursor = body.get("next_cursor")
        if not cursor:
            break
    assert len(seen) == COLLECTION_TOTAL, (
        f"the catalogue walked to {len(seen)} members, expected {COLLECTION_TOTAL}")
    assert sorted(per_series) == list(range(1, SERIES_COUNT + 1))
    for series, count in per_series.items():
        assert count == CYCLE_DAYS, (
            f"series {series} holds {count} members, expected {CYCLE_DAYS}")


def test_paginated_response_carries_cursor_metadata(anon_client):
    """A paginated response declares whether more rows remain."""
    r = anon_client.get("/api/characters", params={"page_size": 10})
    assert r.status_code == 200, r.text
    body = r.json()
    assert isinstance(body, dict), "a paginated read must return an object"
    assert len(items_of(body)) <= 10, "page_size was ignored"
    assert "has_more" in body or "next_cursor" in body, (
        "the response carries neither has_more nor next_cursor")
    assert body.get("has_more") is True or body.get("next_cursor"), (
        f"a page of 10 over {COLLECTION_TOTAL} members reported no further rows")
    assert body.get("total_count") == COLLECTION_TOTAL, (
        f"total_count is {body.get('total_count')}, expected {COLLECTION_TOTAL}")


def test_series_labels_are_multiples_of_three_hundred_and_sixty_six(anon_client):
    """Sixteen series, each labelled by its own upper bound."""
    r = anon_client.get("/api/series")
    assert r.status_code == 200, r.text
    rows = items_of(r.json())
    assert len(rows) == SERIES_COUNT, f"expected {SERIES_COUNT} series"
    labels = [row["label"] for row in rows]
    assert labels == SERIES_LABELS, f"labels are {labels}"


def test_every_ordinal_carries_a_phase_and_the_rule_is_stated(anon_client):
    """All 366 days carry one of the five phases, and the remainder rule is published."""
    r = anon_client.get("/api/colours")
    assert r.status_code == 200, r.text
    body = r.json()
    rows = items_of(body)
    assert len(rows) == CYCLE_DAYS, (
        f"{len(rows)} day colours published, expected {CYCLE_DAYS}")
    ordinals = sorted(row["ordinal"] for row in rows)
    assert ordinals == list(range(1, CYCLE_DAYS + 1)), "an ordinal is missing"
    for row in rows:
        assert row.get("phase") in PHASES, (
            f"ordinal {row['ordinal']} carries {row.get('phase')!r}, not one of "
            f"the five phases")
    rule = body.get("rule") if isinstance(body, dict) else None
    assert isinstance(rule, str) and rule.strip(), (
        "no remainder rule is stated, and 366 does not divide by five")


def test_catalogue_walks_by_phase_in_a_stable_order(anon_client):
    """Ordered by phase, a walk repeats nothing, skips nothing, and breaks ties by number."""
    colours = anon_client.get("/api/colours")
    assert colours.status_code == 200, colours.text
    phase_of = {row["ordinal"]: row["phase"] for row in items_of(colours.json())}
    assert set(phase_of.values()) <= set(PHASES), set(phase_of.values())
    expected = sorted(
        range(1, COLLECTION_TOTAL + 1),
        key=lambda n: (PHASES.index(phase_of[(n - 1) % CYCLE_DAYS + 1]), n))
    walked: list[int] = []
    cursor = None
    for _ in range(80):
        params = {"order": "phase", "page_size": 97}
        if cursor:
            params["cursor"] = cursor
        r = anon_client.get("/api/characters", params=params)
        assert r.status_code == 200, r.text
        body = r.json()
        for row in items_of(body):
            ordinal = (row["number"] - 1) % CYCLE_DAYS + 1
            assert row.get("ordinal") == ordinal, (
                f"member {row['number']} reports ordinal {row.get('ordinal')}, "
                f"expected {ordinal}")
            assert row.get("phase") == phase_of[ordinal], (
                f"member {row['number']} reports phase {row.get('phase')!r} while "
                f"/api/colours assigns {phase_of[ordinal]!r} to ordinal {ordinal}")
            walked.append(row["number"])
        if not body.get("has_more"):
            break
        cursor = body.get("next_cursor")
        assert cursor, "has_more is true but no next_cursor was issued"
    assert len(walked) == COLLECTION_TOTAL and len(set(walked)) == COLLECTION_TOTAL, (
        f"the phase walk returned {len(walked)} rows, {len(set(walked))} distinct; "
        f"expected {COLLECTION_TOTAL} each exactly once. Paging a non-unique ordering "
        f"without a tiebreak repeats and skips")
    first_wrong = next((i for i, (a, b) in enumerate(zip(walked, expected)) if a != b), None)
    assert first_wrong is None, (
        f"the phase walk departs from phase order then number at position "
        f"{first_wrong}: got {walked[first_wrong]}, expected {expected[first_wrong]}")


def test_a_forged_or_foreign_cursor_is_rejected(anon_client):
    """A cursor the server did not issue for this ordering, or a bad page size, answers 400."""
    first = anon_client.get("/api/characters", params={"page_size": 5})
    assert first.status_code == 200, first.text
    foreign = first.json().get("next_cursor")
    assert foreign, "a page of five issued no next_cursor"
    cases = [
        ({"cursor": "not-a-cursor"}, "a cursor this server never issued"),
        ({"order": "phase", "cursor": foreign}, "a cursor issued for another ordering"),
        ({"page_size": MAX_PAGE_SIZE + 1}, "a page size above the stated maximum"),
        ({"page_size": 0}, "a page size of zero"),
        ({"order": "birthday"}, "an ordering the catalogue does not offer"),
    ]
    for params, what in cases:
        r = anon_client.get("/api/characters", params=params)
        assert r.status_code == 400, (
            f"{what} answered {r.status_code}; the catalogue refuses it with 400 "
            f"rather than guessing or failing")
        body = r.json()
        assert isinstance(body.get("error"), str) and body["error"].strip(), (
            f"{what} was refused without an error field: {body}")
    largest = anon_client.get("/api/characters", params={"page_size": MAX_PAGE_SIZE})
    assert largest.status_code == 200, largest.text
    assert len(items_of(largest.json())) == MAX_PAGE_SIZE, (
        f"a page size of exactly {MAX_PAGE_SIZE} is the stated maximum and is served whole")


def test_awards_and_roadmap_read_one_record(anon_client):
    """Both award surfaces agree because they read one record."""
    awards = anon_client.get("/api/awards")
    roadmap = anon_client.get("/api/roadmap")
    assert awards.status_code == 200, awards.text
    assert roadmap.status_code == 200, roadmap.text
    a_rows = items_of(awards.json())
    r_rows = items_of(roadmap.json())
    assert a_rows, "the award record is empty"
    a_subjects = sorted(str(row["subject"]) for row in a_rows)
    r_subjects = sorted(str(row["subject"]) for row in r_rows if "subject" in row)
    assert a_subjects == r_subjects, (
        "the awards scene and the timeline disagree about what was awarded")
    fmts = {bool(re.fullmatch(r"\d{4}[-/]\d{2}[-/]\d{2}", str(row.get("date", ""))))
            for row in a_rows + r_rows}
    assert len(fmts) == 1, "two date formats are published for one record"


def test_hub_order_is_data_and_every_game_route_answers(anon_client):
    """Ten games in hub order, and each route serves."""
    r = anon_client.get("/api/games")
    assert r.status_code == 200, r.text
    rows = items_of(r.json())
    assert len(rows) == len(HUB_ORDER), f"expected {len(HUB_ORDER)} games"
    ordered = [row["title"] for row in sorted(rows, key=lambda x: x["position"])]
    assert ordered == HUB_ORDER, f"hub order is {ordered}"
    for route in GAME_ROUTES:
        page = anon_client.get(route)
        assert page.status_code == 200, f"{route} answered {page.status_code}"


def test_wheel_categories_and_oracle_decks_are_served_as_data(anon_client):
    """Content a reader cannot use is content, not markup."""
    wheel = anon_client.get("/api/wheel-categories")
    assert wheel.status_code == 200, wheel.text
    w_rows = items_of(wheel.json())
    assert len(w_rows) == WHEEL_CATEGORY_COUNT, (
        f"{len(w_rows)} wheel categories, expected {WHEEL_CATEGORY_COUNT}")
    decks = anon_client.get("/api/oracle-decks")
    assert decks.status_code == 200, decks.text
    d_rows = items_of(decks.json())
    assert len(d_rows) == ORACLE_DECK_COUNT, (
        f"{len(d_rows)} oracle decks, expected {ORACLE_DECK_COUNT}")
    sizes = {len(row["cards"]) for row in d_rows}
    assert len(sizes) > 1, (
        "every deck is the same size, so the shell is assuming a uniform deck")
    assert min(sizes) >= 2


def test_the_menu_takes_focus_holds_it_and_gives_it_back(page):
    """The menu is a modal surface: focus goes in, stays in, and returns to its opener."""
    page.goto("/")
    opener = page.get_by_role("button", name="Menu")
    opener.click()
    panel = page.get_by_role("dialog", name="Menu")
    expect(panel).to_be_visible()
    inside = ("() => !!document.activeElement && "
              "!!document.activeElement.closest('[role=dialog], dialog')")
    not_behind = ("() => { const a = document.activeElement; return !a || "
                  "a === document.body || !!a.closest('[role=dialog], dialog'); }")
    page.wait_for_function(inside)
    for key in ["Tab"] * 12 + ["Shift+Tab"] * 4:
        page.keyboard.press(key)
        assert page.evaluate(not_behind), (
            f"pressing {key} moved focus out of the open menu, so the page behind "
            f"it is not inert to the keyboard")
    page.keyboard.press("Escape")
    expect(panel).to_be_hidden()
    expect(opener).to_be_focused()


def test_the_daily_prompt_turns_over_at_the_readers_local_midnight(anon_client, devices):
    """One minute before and one minute after local midnight are two days, in any timezone."""
    published = anon_client.get("/api/prompts")
    assert published.status_code == 200, published.text
    prompts = {str(row["key"]): str(row["text"]) for row in items_of(published.json())}
    assert prompts, "no daily prompt is published"
    context = devices(timezone_id="Pacific/Kiritimati",
                      at=at_local(KIRITIMATI, 2026, 10, 14, 23, 59))
    page = context.new_page()
    page.goto("/challenge")
    expect(page.get_by_text("Today is 2026-10-14", exact=True)).to_be_visible()
    page.get_by_role("button", name="challenge").click()
    region = page.get_by_role("region", name="Today's challenge")
    expect(region).to_be_visible()
    first = prompt_shown(region.inner_text(), prompts)

    page.reload()
    page.get_by_role("button", name="challenge").click()
    expect(page.get_by_text(PROMPT_AGAIN, exact=True)).to_be_visible()
    assert prompt_shown(region.inner_text(), prompts) == first, (
        "the same local day showed a different prompt on the second opening")

    context.clock.set_system_time(at_local(KIRITIMATI, 2026, 10, 15, 0, 1))
    page.reload()
    expect(page.get_by_text("Today is 2026-10-15", exact=True)).to_be_visible()
    page.get_by_role("button", name="challenge").click()
    expect(region).to_be_visible()
    expect(page.get_by_text(PROMPT_AGAIN, exact=True)).to_have_count(0)
    history = page.get_by_role("list", name="Previous days")
    yesterday = history.get_by_role("listitem").filter(has_text="2026-10-14")
    expect(yesterday).to_have_count(1)
    expect(yesterday).to_contain_text(prompts[first])


def test_the_shared_board_is_the_readers_local_day_in_any_timezone(devices):
    """Two readers on the same local date meet one board, whatever the UTC date is."""
    east = devices("Pacific/Kiritimati",
                   at_local(KIRITIMATI, 2026, 10, 14, 9)).new_page()
    west = devices("Pacific/Honolulu", at_local(HONOLULU, 2026, 10, 14, 9)).new_page()
    later = devices("Pacific/Kiritimati",
                    at_local(KIRITIMATI, 2026, 10, 15, 9)).new_page()
    boards = {}
    for name, reader in (("east", east), ("west", west), ("later", later)):
        reader.goto("/puzzle")
        boards[name] = read_board(reader)
    assert boards["east"] == boards["west"], (
        "two readers whose local date is 14 October met different boards; the day "
        "seed followed the UTC date rather than the reader's own day")
    expect(east.get_by_text(SHARED_BOARD, exact=True)).to_be_visible()
    east.reload()
    assert read_board(east) == boards["east"], (
        "reloading on the same day dealt a different board")
    assert boards["later"] != boards["east"], (
        "the next local day dealt the same board, so the seed ignores the date")


def test_each_game_draws_chance_from_its_own_day_stream(devices):
    """Spinning the wheel first changes neither the wheel's day nor the puzzle's board."""
    at = datetime(2026, 10, 14, 9, 0, tzinfo=timezone.utc)
    untouched = devices(at=at).new_page()
    untouched.goto("/puzzle")
    board = read_board(untouched)
    landings = []
    for _ in range(2):
        reader = devices(at=at).new_page()
        reader.goto("/wheel")
        spin = reader.get_by_role("button", name="GO")
        result = reader.get_by_role("status", name="Wheel result")
        for _ in range(3):
            expect(spin).to_be_enabled()
            spin.click()
        expect(spin).to_be_enabled()
        landings.append(result.inner_text().strip())
        reader.goto("/puzzle")
        assert read_board(reader) == board, (
            "spinning the wheel first changed the puzzle's board, so the games "
            "share one sequence of chance")
    assert landings[0] == landings[1], (
        f"two readers on the same day landed on {landings[0]!r} and {landings[1]!r} "
        f"after three spins; the wheel's landings are not derived from the day seed")


def test_daily_shards_are_claimed_once_per_day_however_the_clock_moves(devices):
    """Forward, back and forward again yields one claim per day, never one per adjustment."""
    day = datetime(2026, 10, 14, 10, 0, tzinfo=timezone.utc)
    context = devices(at=day)
    page = context.new_page()
    enter_machine(page)
    expect_balance(page, WELCOME_GRANT)
    claim = page.get_by_role("button", name="Claim daily shards")
    claim.click()
    expect_balance(page, WELCOME_GRANT + DAILY_GRANT)
    expect(page.get_by_text("Claimed for 2026-10-14", exact=True)).to_be_visible()
    expect(claim).to_be_disabled()

    context.clock.set_system_time(day + timedelta(days=1))
    enter_machine(page)
    expect(claim).to_be_enabled()
    claim.click()
    expect_balance(page, WELCOME_GRANT + 2 * DAILY_GRANT)

    context.clock.set_system_time(day)
    enter_machine(page)
    expect(page.get_by_text(CLOCK_BACKWARDS, exact=True)).to_be_visible()
    expect(claim).to_be_disabled()
    expect_balance(page, WELCOME_GRANT + 2 * DAILY_GRANT)

    context.clock.set_system_time(day + timedelta(days=1))
    enter_machine(page)
    expect(claim).to_be_disabled()
    expect_balance(page, WELCOME_GRANT + 2 * DAILY_GRANT)

    context.clock.set_system_time(day + timedelta(days=2))
    enter_machine(page)
    expect(claim).to_be_enabled()
    claim.click()
    expect_balance(page, WELCOME_GRANT + 3 * DAILY_GRANT)


def test_a_backwards_clock_is_announced_and_destroys_nothing(devices, tmp_path):
    """A device date moved back leaves the collection and the purse exactly as they were."""
    day = datetime(2026, 10, 14, 10, 0, tzinfo=timezone.utc)
    context = devices(at=day + timedelta(days=1))
    page = context.new_page()
    import_store(page, store_file(
        tmp_path, "earned",
        collection=[kept(3, 29, 2, "stripes", "Fire", "2026-10-01T12:00:00Z"),
                    kept(1, 1, 1, "plain", "Wood", "2026-10-02T12:00:00Z")],
        shardLedger=[credit("welcome", WELCOME_GRANT, "2026-10-01T09:00:00Z"),
                     debit("spent-common", 10, "2026-10-02T09:00:00Z")]))
    enter_machine(page)
    expect_balance(page, WELCOME_GRANT - 10)

    context.clock.set_system_time(day)
    enter_machine(page)
    expect(page.get_by_text(CLOCK_BACKWARDS, exact=True)).to_be_visible()
    expect_balance(page, WELCOME_GRANT - 10)
    page.goto("/collection")
    entries = collection_entries(page)
    expect(entries).to_have_count(2)
    expect(entries.filter(has_text=member_pattern(member_number(3, 60)))).to_have_count(1)
    expect(entries.filter(has_text=member_pattern(1))).to_have_count(1)


def test_prize_tiers_carry_prices_and_odds_that_sum_to_one(anon_client):
    """Three tiers are prices, and the odds behind them are published."""
    r = anon_client.get("/api/odds")
    assert r.status_code == 200, r.text
    rows = items_of(r.json())
    prices = {str(row["key"]): row["price"] for row in rows}
    assert prices == PRIZE_TIERS, f"tiers are {prices}, expected {PRIZE_TIERS}"
    for row in rows:
        odds = row.get("odds")
        assert isinstance(odds, list) and odds, f"{row['key']} publishes no odds"
        total = sum(float(o["chance"]) for o in odds)
        assert abs(total - 1.0) < 1e-6, (
            f"{row['key']} odds sum to {total}, which is not a distribution")


def test_two_tabs_spend_from_one_ledger(devices):
    """A spend in one tab is the balance in the other, and neither overwrites the other."""
    context = devices()
    left = context.new_page()
    enter_machine(left)
    expect_balance(left, WELCOME_GRANT)
    right = context.new_page()
    enter_machine(right)
    expect_balance(right, WELCOME_GRANT)

    exchange(left, "COMMON")
    expect_balance(left, WELCOME_GRANT - PRIZE_TIERS["COMMON"])
    expect_balance(right, WELCOME_GRANT - PRIZE_TIERS["COMMON"])

    exchange(right, "RARE")
    after = WELCOME_GRANT - PRIZE_TIERS["COMMON"] - PRIZE_TIERS["RARE"]
    expect_balance(right, after)
    expect_balance(left, after)
    left.reload()
    left.get_by_role("button", name="ENTER").click()
    expect_balance(left, after)


def test_a_double_press_exchanges_once_and_an_unaffordable_one_is_refused(page):
    """Two quick presses are one exchange, and a price above the balance draws nothing."""
    enter_machine(page)
    expect_balance(page, WELCOME_GRANT)
    page.get_by_role("button", name="Exchange COMMON").dblclick()
    expect(page.get_by_role("region", name="Reward")).to_have_count(1)
    page.get_by_role("button", name="Continue").click()
    expect_balance(page, WELCOME_GRANT - PRIZE_TIERS["COMMON"])

    exchange(page, "LEGENDARY")
    left = WELCOME_GRANT - PRIZE_TIERS["COMMON"] - PRIZE_TIERS["LEGENDARY"]
    expect_balance(page, left)
    for tier in ("LEGENDARY", "RARE"):
        page.get_by_role("button", name=f"Exchange {tier}").click()
        expect(page.get_by_text(
            f"This costs {PRIZE_TIERS[tier]} SOUL SHARDS and your balance is {left}.",
            exact=True)).to_be_visible()
        expect(page.get_by_role("region", name="Reward")).to_have_count(0)
        expect_balance(page, left)
    page.reload()
    page.get_by_role("button", name="ENTER").click()
    expect_balance(page, left)


def test_index_html_redirects_permanently_to_root(anon_client):
    """The home document answers on one address."""
    r = anon_client.get("/index.html", follow_redirects=False)
    assert r.status_code == 301, (
        f"/index.html answered {r.status_code}, expected a permanent redirect")
    assert r.headers.get("location", "").endswith("/")


def test_a_share_link_rederives_the_character_and_ignores_a_forged_result(page):
    """A link names inputs; a result smuggled into it is not what the recipient sees."""
    token = encode_link({"v": LINK_VERSION, "kind": "character", "day": 29, "month": 2,
                         "series": 3, "background": "stripes", "colour": "Fire",
                         "number": 1, "label": 366, "name": "a forged result"})
    page.goto(f"/?share={token}")
    shared = page.get_by_role("region", name="Shared character")
    expect(shared).to_be_visible()
    expect(shared.get_by_text(member_label(member_number(3, LEAP_DAY_ORDINAL)),
                              exact=True)).to_be_visible()
    expect(shared.get_by_text(member_label(1), exact=True)).to_have_count(0)
    expect(shared).to_contain_text("Background: stripes")
    expect(shared).to_contain_text("Colour: Fire")


def test_the_share_warning_comes_before_a_link_that_carries_only_inputs(page):
    """The birthday warning precedes the link, and the link encodes inputs and nothing else."""
    page.goto("/")
    choose(page, "Background", "clouds")
    choose(page, "Colour", "Metal")
    find_birthday(page, 29, 2)
    number = member_number(3, LEAP_DAY_ORDINAL)
    page.get_by_role("button", name=f"Share {member_label(number)}").click()
    expect(page.get_by_text(SHARE_WARNING, exact=True)).to_be_visible()
    expect(page.get_by_role("textbox", name="Link")).to_have_count(0)
    page.get_by_role("button", name="Create link").click()
    link = page.get_by_role("textbox", name="Link")
    expect(link).to_be_visible()
    url = link.input_value()
    tokens = parse_qs(urlparse(url).query).get("share")
    assert tokens, f"the created link {url!r} carries no share parameter"
    payload = decode_link(tokens[0])
    assert payload == {"v": LINK_VERSION, "kind": "character", "day": 29, "month": 2,
                       "series": 3, "background": "clouds", "colour": "Metal"}, (
        f"the link encodes {payload}; it must carry exactly the inputs, and a "
        f"rendered result inside it lets a sender claim what the resolver never made")
    page.goto(f"{urlparse(url).path or '/'}?{urlparse(url).query}")
    expect(page.get_by_role("region", name="Shared character").get_by_text(
        member_label(number), exact=True)).to_be_visible()


def test_an_impossible_or_older_share_link_is_refused_with_its_reason(page):
    """A link is typed input from a stranger: impossible fields and old versions are refused."""
    good = {"v": LINK_VERSION, "kind": "character", "day": 29, "month": 2, "series": 3,
            "background": "plain", "colour": "Wood"}
    refused = [
        (encode_link({**good, "day": 30}), LINK_NOT_DESCRIBED),
        (encode_link({**good, "series": 17}), LINK_NOT_DESCRIBED),
        (encode_link({**good, "colour": "Purple"}), LINK_NOT_DESCRIBED),
        (encode_link({**good, "background": "neon"}), LINK_NOT_DESCRIBED),
        ("this-is-not-a-link", LINK_NOT_DESCRIBED),
        (encode_link({"v": 1, "d": "29-02", "s": 3}), LINK_TOO_OLD),
    ]
    for token, reason in refused:
        page.goto(f"/?share={token}")
        expect(page.get_by_text(reason, exact=True)).to_be_visible()
        expect(page.get_by_role("region", name="Shared character")).to_have_count(0)
        expect(page.get_by_role("group", name="Birthday")).to_be_visible()


def test_an_import_unions_the_collection_keeping_the_earlier_keeping_time(devices, tmp_path):
    """Both import orders leave the union, and a character on both sides keeps its earlier entry."""
    phone = [kept(3, 29, 2, "stripes", "Fire", "2026-03-05T12:00:00Z"),
             kept(1, 1, 1, "plain", "Wood", "2026-03-02T12:00:00Z")]
    laptop = [kept(3, 29, 2, "clouds", "Water", "2026-03-01T12:00:00Z"),
              kept(16, 31, 12, "confetti", "Earth", "2026-03-03T12:00:00Z")]
    for label, order in (("phone-then-laptop", (phone, laptop)),
                         ("laptop-then-phone", (laptop, phone))):
        page = devices().new_page()
        for index, collection in enumerate(order):
            import_store(page, store_file(tmp_path, f"{label}-{index}",
                                          collection=collection))
        page.goto("/collection")
        entries = collection_entries(page)
        expect(entries).to_have_count(3)
        shared = entries.filter(has_text=member_pattern(member_number(3, 60)))
        expect(shared).to_have_count(1)
        expect(shared).to_contain_text("Kept 2026-03-01")
        expect(shared).to_contain_text("Background: clouds")
        expect(entries.filter(has_text=member_pattern(1))).to_have_count(1)
        expect(entries.filter(has_text=member_pattern(COLLECTION_TOTAL))).to_have_count(1)


def test_an_import_from_a_device_that_also_spent_asks_which_purse_to_keep(devices, tmp_path):
    """Spending on both sides is a question; spending on one side merges by entry."""
    welcome = credit("welcome", WELCOME_GRANT, "2026-10-01T09:00:00Z")
    page = devices().new_page()
    import_store(page, store_file(tmp_path, "here", shardLedger=[
        welcome, debit("spent-here", 100, "2026-10-02T09:00:00Z")]))
    enter_machine(page)
    expect_balance(page, WELCOME_GRANT - 100)

    page.goto("/import")
    page.get_by_label("Store file").set_input_files(store_file(tmp_path, "there", shardLedger=[
        welcome, debit("spent-there", 250, "2026-10-03T09:00:00Z")]))
    expect(page.get_by_role("region", name="Import preview")).to_be_visible()
    expect(page.get_by_text(PURSE_CONFLICT, exact=True)).to_be_visible()
    apply = page.get_by_role("button", name="Apply import")
    expect(apply).to_be_disabled()
    page.get_by_role("radio", name="The imported purse").check()
    apply.click()
    expect(page.get_by_text(MERGED, exact=True)).to_be_visible()
    enter_machine(page)
    expect_balance(page, WELCOME_GRANT - 250)

    other = devices().new_page()
    import_store(other, store_file(tmp_path, "start", shardLedger=[welcome]))
    import_store(other, store_file(tmp_path, "one-sided", shardLedger=[
        welcome, credit("bonus", 40, "2026-10-02T09:00:00Z"),
        debit("spent-there", 250, "2026-10-03T09:00:00Z")]))
    enter_machine(other)
    expect_balance(other, WELCOME_GRANT + 40 - 250)


def test_an_invalid_import_file_changes_nothing(devices, tmp_path):
    """A file failing anywhere is refused whole, and the store is exactly as it was."""
    page = devices().new_page()
    import_store(page, store_file(
        tmp_path, "base",
        collection=[kept(3, 29, 2, "stripes", "Fire", "2026-03-05T12:00:00Z")],
        shardLedger=[credit("welcome", WELCOME_GRANT, "2026-10-01T09:00:00Z")]))
    fresh = kept(16, 31, 12, "confetti", "Earth", "2026-03-03T12:00:00Z")
    bad_files = [
        raw_file(tmp_path, "truncated",
                 '{"format": "daykin-store", "version": 2, "collection": [{"series": 1,'),
        store_file(tmp_path, "impossible-date",
                   collection=[fresh, kept(2, 30, 2, "plain", "Wood", "2026-03-04T12:00:00Z")]),
        store_file(tmp_path, "series-seventeen",
                   collection=[fresh, kept(17, 1, 1, "plain", "Wood", "2026-03-04T12:00:00Z")]),
        store_file(tmp_path, "below-zero", collection=[fresh], shardLedger=[
            debit("early-spend", 50, "2026-01-01T09:00:00Z"),
            credit("late-credit", 30, "2026-02-01T09:00:00Z")]),
        raw_file(tmp_path, "other-product",
                 '{"format": "someone-else", "version": 2, "collection": []}'),
        raw_file(tmp_path, "older-version",
                 '{"format": "daykin-store", "version": 1, "collection": []}'),
    ]
    for path in bad_files:
        page.goto("/import")
        page.get_by_label("Store file").set_input_files(path)
        expect(page.get_by_text(UNREADABLE_FILE, exact=True)).to_be_visible()
        expect(page.get_by_role("button", name="Apply import")).to_have_count(0)
    page.goto("/collection")
    entries = collection_entries(page)
    expect(entries).to_have_count(1)
    expect(entries.filter(has_text=member_pattern(member_number(3, 60)))).to_have_count(1)
    enter_machine(page)
    expect_balance(page, WELCOME_GRANT)


def test_an_applied_import_can_be_undone_and_a_previewed_one_declined(devices, tmp_path):
    """Decline leaves the store untouched; undo returns it to the state before the import."""
    page = devices().new_page()
    import_store(page, store_file(tmp_path, "base", collection=[
        kept(3, 29, 2, "stripes", "Fire", "2026-03-05T12:00:00Z")]))
    incoming = store_file(tmp_path, "incoming", collection=[
        kept(3, 29, 2, "clouds", "Water", "2026-03-01T12:00:00Z"),
        kept(1, 1, 1, "plain", "Wood", "2026-03-02T12:00:00Z")])

    page.goto("/import")
    page.get_by_label("Store file").set_input_files(incoming)
    preview = page.get_by_role("region", name="Import preview")
    expect(preview).to_be_visible()
    page.get_by_role("button", name="Decline import").click()
    expect(preview).to_have_count(0)
    page.goto("/collection")
    expect(collection_entries(page)).to_have_count(1)

    page.goto("/import")
    page.get_by_label("Store file").set_input_files(incoming)
    page.get_by_role("button", name="Apply import").click()
    expect(page.get_by_text(MERGED, exact=True)).to_be_visible()
    page.get_by_role("button", name="Undo import").click()
    page.goto("/collection")
    entries = collection_entries(page)
    expect(entries).to_have_count(1)
    expect(entries.first).to_contain_text("Kept 2026-03-05")
    expect(entries.first).to_contain_text("Background: stripes")


def test_every_puzzle_board_dealt_is_solvable(devices):
    """Thirty boards over six days are all permutations of the tiles, unsolved and solvable."""
    solved = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    start = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)
    context = devices(at=start)
    page = context.new_page()
    boards = []
    for offset in range(6):
        context.clock.set_system_time(start + timedelta(days=offset))
        page.goto("/puzzle")
        for attempt in range(5):
            if attempt:
                page.get_by_role("button", name="Shuffle").click()
                expect(page.get_by_text("Movements: 0", exact=True)).to_be_visible()
            board = read_board(page)
            flat = sorted(n for row in board for n in row)
            assert flat == list(range(16)), f"the board is not the fifteen tiles: {board}"
            assert board != solved, "a board was dealt already solved"
            assert board_is_solvable(board), (
                f"day {offset}, attempt {attempt + 1} dealt an unsolvable board {board}; "
                f"half of all random permutations cannot be solved")
            boards.append(tuple(map(tuple, board)))
    assert len(set(boards)) >= 20, (
        f"thirty deals produced only {len(set(boards))} distinct boards")


def test_puzzle_undo_returns_board_and_move_count_together(page):
    """Moves are counted only when legal, and undo rewinds the board and the count as one."""
    page.goto("/puzzle")
    grid = page.get_by_role("grid", name="Puzzle board")
    grid.focus()
    board = read_board(page)
    expect(page.get_by_text("Movements: 0", exact=True)).to_be_visible()
    row, col = blank_of(board)
    keys = ["ArrowUp"] * row
    if row == 0:
        keys = ["ArrowDown", "ArrowRight" if col < 3 else "ArrowLeft", "ArrowUp"]
    while len(keys) < 3:
        keys += ["ArrowDown", "ArrowUp"]
    history = [board]
    for count, key in enumerate(keys, start=1):
        page.keyboard.press(key)
        expect(page.get_by_text(f"Movements: {count}", exact=True)).to_be_visible()
        expected = move_blank(history[-1], key)
        assert read_board(page) == expected, (
            f"{key} should move the empty cell that way: expected {expected}")
        history.append(expected)
    page.keyboard.press("ArrowUp")
    expect(page.get_by_text(f"Movements: {len(keys)}", exact=True)).to_be_visible()
    assert read_board(page) == history[-1], "an arrow off the board changed the board"
    undo = page.get_by_role("button", name="Undo")
    for back in (1, 2):
        undo.click()
        expect(page.get_by_text(f"Movements: {len(keys) - back}", exact=True)).to_be_visible()
        assert read_board(page) == history[-1 - back], (
            f"after {back} undo(s) the board is not the board from {back} move(s) ago")


def test_nothing_a_reader_produces_reaches_the_server(anon_client):
    """The catalogue is read-only: the app accepts no reader write."""
    alive = anon_client.get("/api/series")
    assert alive.status_code == 200, (
        "the catalogue API must answer before a write probe means anything")
    probes = [
        ("/api/collection", {"character": 1}),
        ("/api/scores", {"game": "puzzle", "best": 1}),
        ("/api/shards", {"delta": 100}),
        ("/api/characters", {"number": 1}),
    ]
    for route, payload in probes:
        r = anon_client.post(route, json=payload)
        assert r.status_code in (403, 404, 405), (
            f"POST {route} answered {r.status_code}; the reader's state lives on "
            f"the device and the application accepts no write for it")


def test_a_kept_character_survives_a_reload_with_its_background_once(devices):
    """A character kept twice is one entry carrying its choices, and a reload keeps it."""
    page = devices(at=datetime(2026, 10, 14, 12, 0, tzinfo=timezone.utc)).new_page()
    page.goto("/")
    choose(page, "Background", "stripes")
    choose(page, "Colour", "Water")
    find_birthday(page, 29, 2)
    number = member_number(3, LEAP_DAY_ORDINAL)
    keep = page.get_by_role("button", name=f"Keep {member_label(number)}")
    keep.click()
    expect(page.get_by_text(KEPT_COPY, exact=True).first).to_be_visible()
    keep.click()
    page.goto("/collection")
    for _ in range(2):
        entries = collection_entries(page)
        expect(entries).to_have_count(1)
        expect(entries.first.get_by_text(member_label(number), exact=True)).to_be_visible()
        expect(entries.first).to_contain_text("Background: stripes")
        expect(entries.first).to_contain_text("Colour: Water")
        expect(entries.first).to_contain_text("Kept 2026-10-14")
        page.reload()


def test_refused_storage_still_opens_plays_and_says_so_once(devices):
    """With every browser store refused, the product opens, resolves, spends, and says so once."""
    context = devices()
    context.add_init_script(REFUSE_STORAGE)
    page = context.new_page()
    page.goto("/")
    expect(page.get_by_text(NO_STORAGE, exact=True)).to_have_count(1)
    find_birthday(page, 29, 2)
    expect(sixteen(page)).to_have_count(SERIES_COUNT)
    page.get_by_role("button", name=f"Keep {member_label(LEAP_DAY_ORDINAL)}").click()
    expect(page.get_by_text(NO_STORAGE, exact=True)).to_have_count(1)
    enter_machine(page)
    expect_balance(page, WELCOME_GRANT)
    exchange(page, "COMMON")
    expect_balance(page, WELCOME_GRANT - PRIZE_TIERS["COMMON"])
    expect(page.get_by_text(NO_STORAGE, exact=True)).to_have_count(1)


def test_removal_deletes_one_kind_and_leaves_the_rest(devices, tmp_path):
    """Deleting the collection asks first, and leaves the purse and its welcome entry alone."""
    page = devices().new_page()
    import_store(page, store_file(
        tmp_path, "profile",
        collection=[kept(3, 29, 2, "stripes", "Fire", "2026-03-05T12:00:00Z"),
                    kept(1, 1, 1, "plain", "Wood", "2026-03-02T12:00:00Z")],
        shardLedger=[credit("welcome", WELCOME_GRANT, "2026-10-01T09:00:00Z"),
                     debit("spent-common", 10, "2026-10-02T09:00:00Z")]))
    page.goto("/my-data")
    stored = page.get_by_role("list", name="Stored on this device").get_by_role("listitem")
    expect(stored.filter(has_text="collection:")).to_contain_text("collection: 2")
    expect(stored.filter(has_text="shardLedger:")).to_contain_text("shardLedger: 2")

    page.get_by_role("button", name="Delete collection").click()
    confirm = page.get_by_role("alertdialog")
    expect(confirm).to_be_visible()
    confirm.get_by_role("button", name="Cancel").click()
    expect(stored.filter(has_text="collection:")).to_contain_text("collection: 2")

    page.get_by_role("button", name="Delete collection").click()
    page.get_by_role("alertdialog").get_by_role("button", name="Delete").click()
    expect(stored.filter(has_text="collection:")).to_contain_text("collection: 0")
    expect(stored.filter(has_text="shardLedger:")).to_contain_text("shardLedger: 2")
    page.goto("/collection")
    expect(page.get_by_text(EMPTY_COLLECTION, exact=True)).to_be_visible()
    enter_machine(page)
    expect_balance(page, WELCOME_GRANT - 10)

    page.goto("/my-data")
    page.get_by_role("button", name="Delete everything").click()
    page.get_by_role("alertdialog").get_by_role("button", name="Delete").click()
    expect(page.get_by_text(EVERYTHING_DELETED, exact=True)).to_be_visible()


def test_privacy_and_terms_reachable_from_every_footer(anon_client):
    """A privacy page and a terms page are linked from every route's footer."""
    targets = {}
    home = anon_client.get("/")
    assert home.status_code == 200, home.text
    for word in ("privacy", "terms"):
        m = re.search(rf'href=["\']([^"\']*{word}[^"\']*)["\']', home.text, re.I)
        assert m, f"the home footer links to no {word} page"
        targets[word] = m.group(1)
        page = anon_client.get(m.group(1))
        assert page.status_code == 200, f"the {word} page answered {page.status_code}"
        assert len(page.text) > 400, f"the {word} page states nothing"
    for route in ("/games", "/roadmap"):
        body = anon_client.get(route).text
        for word, href in targets.items():
            assert href in body, f"{route} does not link the {word} page"


def test_content_images_carry_alt_text(anon_client):
    """Every content image carries alternative text."""
    for route in ("/", "/games"):
        body = anon_client.get(route).text
        imgs = re.findall(r"<img\b[^>]*>", body, re.I)
        missing = [tag for tag in imgs if not re.search(r"\balt=", tag, re.I)]
        assert not missing, f"{route} carries {len(missing)} image(s) with no alt"
        svgs = re.findall(r"<svg\b[^>]*>", body, re.I)
        unlabelled = [s for s in svgs
                      if not re.search(r"aria-hidden|aria-label|role=", s, re.I)]
        assert not unlabelled, (
            f"{route} carries {len(unlabelled)} inline vector(s) that are neither "
            f"labelled nor marked decorative")
        assert imgs or svgs, (
            f"{route} renders no image and no inline vector, so this route shows "
            f"no character at all")


def test_every_public_route_declares_a_social_preview(anon_client):
    """Each public route declares its own preview title and a resolving image."""
    seen_titles = set()
    for route in PUBLIC_ROUTES:
        body = anon_client.get(route).text
        title = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]*content=["\']([^"\']+)', body, re.I)
        image = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]*content=["\']([^"\']+)', body, re.I)
        assert title, f"{route} declares no social preview title"
        assert image, f"{route} declares no social preview image"
        seen_titles.add(title.group(1))
        src = image.group(1)
        assert src.startswith("/"), (
            f"{route} names a preview image at {src!r}; it is served by this app "
            f"and is addressed from its own origin")
        got = anon_client.get(src)
        assert got.status_code == 200, (
            f"{route} names a preview image that answers {got.status_code}")
    assert len(seen_titles) == len(PUBLIC_ROUTES), (
        "two routes share a social preview title")


def test_no_credential_in_anything_the_browser_downloads(anon_client):
    """No credential reaches the browser."""
    blob = anon_client.get("/").text
    assets = sorted(set(re.findall(r'src=["\']([^"\']+\.js)["\']', blob, re.I)))
    local = [a for a in assets if a.startswith("/")]
    assert local, "the home route loads no script of its own, so nothing was scanned"
    fetched = 0
    for asset in local[:10]:
        got = anon_client.get(asset)
        assert got.status_code == 200, f"{asset} answered {got.status_code}"
        blob += got.text
        fetched += 1
    assert fetched, "no script asset resolved"
    for secret in ("deku-local-dev-2026", "deku-admin-dev-2026",
                   "postgresql://", "DB_ADMIN_URL"):
        assert secret not in blob, f"{secret!r} reached the browser"


def test_no_source_map_is_published(anon_client):
    """Source maps are not served in production."""
    body = anon_client.get("/").text
    maps = re.findall(r"sourceMappingURL=(\S+)", body)
    for asset in sorted(set(re.findall(r'src=["\']([^"\']+\.js)["\']',
                                       body, re.I)))[:10]:
        if not asset.startswith("/"):
            continue
        got = anon_client.get(asset)
        if got.status_code == 200:
            maps += re.findall(r"sourceMappingURL=(\S+)", got.text)
    assert not maps, f"source maps are published: {maps[:3]}"


def test_structured_logs_carry_request_id(anon_client):
    """Every response carries the request identifier its log lines are keyed by."""
    first = anon_client.get("/api/series")
    assert first.status_code == 200, first.text
    one = first.headers.get("X-Request-Id")
    assert one, (
        "no X-Request-Id header, so a request cannot be joined to the log lines "
        "it produced from outside the process")
    second = anon_client.get("/api/games")
    two = second.headers.get("X-Request-Id")
    assert two, "a second response carried no X-Request-Id"
    assert one != two, (
        f"two requests shared the identifier {one!r}, so it identifies nothing")
    assert len(str(one)) >= 8, f"the request_id {one!r} is too short to be unique"


def test_page_views_are_recorded_with_route_and_time(anon_client):
    """Page views are recorded with their route and the time."""
    anon_client.get("/games")
    r = anon_client.get("/api/page-views")
    assert r.status_code == 200, r.text
    rows = items_of(r.json())
    assert rows, "no page view was recorded"
    latest = rows[-1]
    assert str(latest.get("route", "")).startswith("/"), latest
    assert str(latest.get("at", "")).strip(), latest


def test_catalogue_is_served_from_the_datastore(anon_client, backend):
    """The published catalogue reconciles with the rows the datastore holds."""
    rows = backend.query(
        "SELECT count(*) AS n FROM information_schema.tables "
        "WHERE table_schema NOT IN ('pg_catalog', 'information_schema')", ())
    assert rows and rows[0]["n"] > 0, (
        "the datastore holds no tables, so the catalogue is not stored in "
        "`postgres` as the brief requires")
    stored = backend.query(
        "SELECT relname, n_live_tup FROM pg_stat_user_tables "
        "WHERE n_live_tup >= %s ORDER BY n_live_tup DESC LIMIT 1", (COLLECTION_TOTAL,))
    assert stored, (
        f"no table in the datastore holds {COLLECTION_TOTAL} or more rows, so the "
        f"catalogue the API publishes is not the catalogue the datastore stores. "
        f"Serving it from a file in the image is not what the brief asks for")
    served = anon_client.get("/api/characters", params={"page_size": 1}).json()
    assert served.get("total_count") == COLLECTION_TOTAL, (
        f"the API reports {served.get('total_count')} members while the datastore "
        f"holds {stored[0]['n_live_tup']}; the two must reconcile")


def test_birthday_finder_refuses_a_bot_submission(anon_client):
    """A submission filling the unseen field is refused, and a flood of submissions is limited."""
    decoy = anon_client.get("/api/resolve",
                            params={"day": 1, "month": 1, "website": "x"})
    assert decoy.status_code in (400, 403), (
        f"a resolution carrying the decoy parameter answered "
        f"{decoy.status_code}; no person is shown that field")
    refused = 0
    for _ in range(45):
        rapid = anon_client.get("/api/resolve",
                                params={"day": 2, "month": 2, "website": ""})
        if rapid.status_code == 429:
            refused += 1
    assert refused > 0, (
        "45 finder submissions in quick succession were all served; more than 30 "
        "inside 10 seconds from one caller must answer 429")
