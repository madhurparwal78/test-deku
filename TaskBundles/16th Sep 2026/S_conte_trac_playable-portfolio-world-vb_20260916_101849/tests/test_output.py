"""The one pytest module for deku/playable-portfolio-world-vb.

Three kinds of assertion live here, and each is here for a reason the browser
channel cannot cover. HTTP assertions settle the leaderboard rules, the run
tokens and the denial matrix, because a screen that says a result was sent
cannot tell a stored row from a drawn one. Database assertions through the
`db` capability settle persistence, the seeded boards and the fact that a
refusal wrote nothing. Playwright assertions settle the exact strings, faces,
sizes and layer rules the brief pins for the front end, which an HTTP client
never sees. Nothing here imports the agent's code or assumes its framework.
"""

from __future__ import annotations

import json
import os
import re
import struct
import threading
import time

import httpx

import appclient
import conftest


def test_games_catalogue_lists_the_four_boards_in_order(anon):
    """The games index lists the four minigames in their fixed order."""
    response = anon.get("/games")
    assert response.status_code == 200, (
        f"GET /api/games returned {response.status_code}: {conftest.body_text(response)}")
    rows = response.json()
    assert isinstance(rows, list), f"GET /api/games is not a top-level array: {rows!r}"
    ids = [row.get("id") for row in rows]
    assert ids == list(conftest.GAMES), (
        f"the games index reads {ids}, expected {list(conftest.GAMES)} in that order")
    for row in rows:
        game = row["id"]
        assert row.get("label") == conftest.GAME_LABELS[game], (
            f"game {game!r} carries label {row.get('label')!r}, expected "
            f"{conftest.GAME_LABELS[game]!r}")
        assert row.get("zone") == conftest.GAME_ZONES[game], (
            f"game {game!r} carries zone {row.get('zone')!r}, expected "
            f"{conftest.GAME_ZONES[game]!r}")
        assert int(row.get("max_total")) == conftest.MAX_TOTALS[game], (
            f"game {game!r} reports max_total {row.get('max_total')!r}, expected "
            f"{conftest.MAX_TOTALS[game]}")


def test_games_catalogue_carries_every_item_worth_and_maximum(anon):
    """Each game lists its items with the tabled key, label, worth and maximum."""
    rows = {row["id"]: row for row in anon.get("/games").json()}
    for game, items in conftest.ITEMS.items():
        served = rows[game].get("items")
        assert isinstance(served, list), f"game {game!r} serves no items array: {served!r}"
        assert [item.get("key") for item in served] == [key for key, _l, _w, _m in items], (
            f"game {game!r} lists item keys {[i.get('key') for i in served]}, expected "
            f"{[key for key, _l, _w, _m in items]}")
        for served_item, (key, label, worth, maximum) in zip(served, items):
            assert served_item.get("label") == label, (
                f"item {key!r} of {game!r} carries label {served_item.get('label')!r}, "
                f"expected {label!r}")
            assert int(served_item.get("worth")) == worth, (
                f"item {key!r} of {game!r} is worth {served_item.get('worth')!r}, "
                f"expected {worth}")
            assert int(served_item.get("max")) == maximum, (
                f"item {key!r} of {game!r} caps at {served_item.get('max')!r}, "
                f"expected {maximum}")
        computed = sum(worth * maximum for _k, _l, worth, maximum in items)
        assert computed == conftest.MAX_TOTALS[game], (
            f"the tabled items of {game!r} sum to {computed}, and the brief pins "
            f"{conftest.MAX_TOTALS[game]} as the game maximum")


def test_run_start_returns_a_token_bound_to_its_game(anon, db):
    """Starting a run stores an unused run bound to the game and the player."""
    player = conftest.new_player()
    response = conftest.start_run(anon, "orchard", player)
    assert conftest.is_success(response.status_code), (
        f"POST /api/runs returned {response.status_code}: {conftest.body_text(response)}")
    body = response.json()
    token = body.get("run_token")
    assert isinstance(token, str) and token, f"no run_token in {body!r}"
    assert body.get("game") == "orchard", f"the run reports game {body.get('game')!r}"
    assert body.get("started_at"), f"the run carries no started_at: {body!r}"
    row = db.one("run", run_token=token)
    assert row is not None, f"no run row was stored for run_token {token!r}"
    assert row["game_id"] == "orchard", f"the stored run names game {row['game_id']!r}"
    assert row["player_id"] == player, (
        f"the stored run names player {row['player_id']!r}, expected {player!r}")
    assert row["started_at"] is not None, "the stored run carries no started_at"
    assert row["used_at"] is None, (
        f"a freshly started run already carries used_at {row['used_at']!r}")
    assert player not in token, (
        f"the run_token {token!r} carries the player_id inside it, so it is derived "
        f"from the player rather than opaque")


def test_run_start_for_unknown_or_missing_game_is_refused(anon, db):
    """A run start naming no game or an unknown game creates nothing."""
    player = conftest.new_player()
    for game in (None, "jardin"):
        response = conftest.start_run(anon, game, player)
        assert conftest.is_client_error(response.status_code), (
            f"POST /api/runs with game={game!r} returned {response.status_code}, "
            f"expected a client error: {conftest.body_text(response)}")
        assert response.text.strip(), (
            f"the refusal for game={game!r} carries no reason at all")
    assert db.count("run", player_id=player) == 0, (
        f"a refused run start still wrote a run row for player {player!r}")


def test_run_start_with_a_bad_player_id_is_refused(anon, db):
    """A player_id outside the character rule cannot start a run."""
    bad = {"missing": None, "short": "abc1234", "long": "z" * 65,
           "punctuated": "joueur_!" + "x" * 8}
    for label, player in bad.items():
        response = conftest.start_run(anon, "orchard", player)
        assert conftest.is_client_error(response.status_code), (
            f"POST /api/runs with a {label} player_id returned "
            f"{response.status_code}: {conftest.body_text(response)}")
        if player:
            assert db.count("run", player_id=player) == 0, (
                f"the {label} player_id {player!r} still wrote a run row")
    good = conftest.new_player()
    assert conftest.is_success(conftest.start_run(anon, "orchard", good).status_code), (
        f"a player_id of {len(good)} legal characters was refused")


def test_fourth_run_within_a_minute_hits_the_limit(anon, db):
    """One player starts three runs in the window and the fourth is refused."""
    player = conftest.new_player()
    for number in range(conftest.RUNS_PER_WINDOW):
        response = conftest.start_run(anon, "orchard", player)
        assert conftest.is_success(response.status_code), (
            f"run {number + 1} of {conftest.RUNS_PER_WINDOW} for one player returned "
            f"{response.status_code}: {conftest.body_text(response)}")
    fourth = conftest.start_run(anon, "orchard", player)
    assert conftest.is_client_error(fourth.status_code), (
        f"the fourth run start inside {conftest.RUNS_PER_WINDOW} per 60 seconds "
        f"returned {fourth.status_code}: {conftest.body_text(fourth)}")
    assert fourth.text.strip(), "the rate refusal carries no reason"
    assert db.count("run", player_id=player) == conftest.RUNS_PER_WINDOW, (
        f"player {player!r} holds {db.count('run', player_id=player)} run rows, "
        f"expected exactly {conftest.RUNS_PER_WINDOW}")


def test_accepted_entry_is_persisted_with_its_counts(anon, db):
    """An accepted entry is stored with its counts, total and run, and the run is spent."""
    name = conftest.unique_name("Alba")
    counts = {"pommes": 12, "bananes": 3, "bonus": 1}
    token = conftest.run_token(anon, "orchard")
    response = conftest.send_entry(anon, token, "orchard", name, counts, 245)
    assert conftest.is_success(response.status_code), (
        f"POST /api/entries returned {response.status_code}: {conftest.body_text(response)}")
    body = response.json()
    for field in ("entry_id", "game", "name", "total", "rank"):
        assert field in body, f"the accepted entry answer is missing {field!r}: {body!r}"
    assert body["game"] == "orchard" and body["name"] == name and body["total"] == 245, (
        f"the accepted entry answers {body!r}, which disagrees with what was sent")
    row = db.one("leaderboard_entry", id=body["entry_id"])
    assert row is not None, f"entry {body['entry_id']!r} was answered but never stored"
    assert row["total"] == 245, f"the stored total is {row['total']!r}, expected 245"
    assert row["name"] == name, f"the stored name is {row['name']!r}, expected {name!r}"
    assert not row["name_removed"], "a fresh entry is already marked name_removed"
    assert row["game_id"] == "orchard", f"the stored entry names game {row['game_id']!r}"
    assert row["created_at"] is not None, "the stored entry carries no created_at"
    assert conftest.counts_equal("orchard", row["counts"], counts), (
        f"the stored counts read {row['counts']!r}, expected {counts!r}")
    run = db.one("run", run_token=token)
    assert row["run_id"] == run["id"], (
        f"the entry names run {row['run_id']!r}, expected the run it was sent with")
    assert run["used_at"] is not None, "the spent run still carries an empty used_at"


def test_duplicate_submission_for_one_run_is_refused(anon, db):
    """A second send carrying one run token is refused and writes nothing."""
    token = conftest.run_token(anon, "orchard")
    first = conftest.send_entry(anon, token, "orchard", conftest.unique_name("Elio"),
                                {"pommes": 2}, 20)
    assert conftest.is_success(first.status_code), (
        f"the first send was refused with {first.status_code}: {conftest.body_text(first)}")
    second = conftest.send_entry(anon, token, "orchard", conftest.unique_name("Elio"),
                                 {"pommes": 3}, 30)
    assert conftest.is_client_error(second.status_code), (
        f"a second send with the same run_token returned {second.status_code}, "
        f"expected a client error: {conftest.body_text(second)}")
    assert second.text.strip(), "the duplicate refusal carries no reason"
    run = db.one("run", run_token=token)
    stored = db.count("leaderboard_entry", run_id=run["id"])
    assert stored == 1, (
        f"the run holds {stored} entries after one accepted send and one refused send")


def test_concurrent_submissions_for_one_run_store_exactly_one_entry(anon, db):
    """Two simultaneous sends with one run token leave exactly one entry."""
    token = conftest.run_token(anon, "orchard")
    barrier = threading.Barrier(2, timeout=60)
    lock = threading.Lock()
    seen = []

    def send(suffix: str) -> None:
        with conftest.api() as client:
            barrier.wait()
            response = conftest.send_entry(client, token, "orchard",
                                           conftest.unique_name("Nael"),
                                           {"pommes": 5}, 50)
        with lock:
            seen.append((suffix, response.status_code))

    threads = [threading.Thread(target=send, args=(side,)) for side in ("a", "b")]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=90)
    assert len(seen) == 2, f"only {len(seen)} of the two simultaneous sends returned"
    statuses = sorted(status for _side, status in seen)
    accepted = [s for s in statuses if conftest.is_success(s)]
    refused = [s for s in statuses if conftest.is_client_error(s)]
    run = db.one("run", run_token=token)
    stored = db.count("leaderboard_entry", run_id=run["id"])
    assert stored == 1, (
        f"the run holds {stored} entries after two simultaneous sends, expected one. "
        f"The two calls answered {statuses}")
    assert len(accepted) == 1 and len(refused) == 1, (
        f"the two simultaneous sends answered {statuses}, expected one success and "
        f"one client error")


def test_entry_without_or_with_an_unknown_game_is_refused(anon, db):
    """An entry naming no game or an unknown game is refused and writes nothing."""
    for game in (None, "jardin"):
        name = conftest.unique_name("Sacha")
        token = conftest.run_token(anon, "orchard")
        response = conftest.send_entry(anon, token, game, name, {"pommes": 1}, 10)
        assert conftest.is_client_error(response.status_code), (
            f"an entry naming game={game!r} returned {response.status_code}: "
            f"{conftest.body_text(response)}")
        assert db.count("leaderboard_entry", name=name) == 0, (
            f"the refused entry naming game={game!r} still stored a row")


def test_run_token_from_another_game_is_refused(anon, db):
    """An entry whose game differs from the run's game is refused and writes nothing."""
    name = conftest.unique_name("Nine")
    token = conftest.run_token(anon, "orchard")
    response = conftest.send_entry(anon, token, "ski", name, {"portes": 1}, 30)
    assert conftest.is_client_error(response.status_code), (
        f"a ski entry sent with an orchard run_token returned {response.status_code}: "
        f"{conftest.body_text(response)}")
    run = db.one("run", run_token=token)
    assert db.count("leaderboard_entry", run_id=run["id"]) == 0, (
        "the mismatched entry was stored against the orchard run")
    assert db.count("leaderboard_entry", name=name) == 0, (
        f"a row named {name!r} was stored despite the refusal")


def test_count_above_its_maximum_is_refused(anon, db):
    """An item count above the tabled maximum is refused and writes nothing."""
    name = conftest.unique_name("Orso")
    token = conftest.run_token(anon, "orchard")
    response = conftest.send_entry(anon, token, "orchard", name, {"pommes": 61}, 610)
    assert conftest.is_client_error(response.status_code), (
        f"orchard pommes 61 with total 610 returned {response.status_code}, and the "
        f"apple maximum is 60: {conftest.body_text(response)}")
    assert db.count("leaderboard_entry", name=name) == 0, (
        "the over-maximum entry was stored")
    allowed = conftest.unique_name("Orso")
    edge = conftest.run_token(anon, "orchard")
    accepted = conftest.send_entry(anon, edge, "orchard", allowed, {"pommes": 60}, 600)
    assert conftest.is_success(accepted.status_code), (
        f"orchard pommes 60, exactly the maximum, was refused with "
        f"{accepted.status_code}: {conftest.body_text(accepted)}")


def test_unknown_negative_or_fractional_counts_are_refused(anon, db):
    """An unknown item key, a negative count and a fractional count are all refused."""
    cases = {"unknown key": ({"cerises": 2}, 20), "negative": ({"pommes": -1}, -10),
             "fractional": ({"pommes": 1.5}, 15)}
    for label, (counts, total) in cases.items():
        name = conftest.unique_name("Vero")
        token = conftest.run_token(anon, "orchard")
        response = conftest.send_entry(anon, token, "orchard", name, counts, total)
        assert conftest.is_client_error(response.status_code), (
            f"the {label} count {counts!r} returned {response.status_code}, expected "
            f"a client error: {conftest.body_text(response)}")
        assert db.count("leaderboard_entry", name=name) == 0, (
            f"the {label} count {counts!r} still stored a row")


def test_total_that_disagrees_with_the_counts_is_refused(anon, db):
    """The pinned worked pair: 245 is accepted for those counts and 250 is refused."""
    counts = {"pommes": 12, "bananes": 3, "bonus": 1}
    refused_name = conftest.unique_name("Livia")
    token = conftest.run_token(anon, "orchard")
    refused = conftest.send_entry(anon, token, "orchard", refused_name, counts, 250)
    assert conftest.is_client_error(refused.status_code), (
        f"counts {counts!r} sent with total 250 returned {refused.status_code}, and "
        f"those counts are worth 245: {conftest.body_text(refused)}")
    assert db.count("leaderboard_entry", name=refused_name) == 0, (
        "the mismatched total was stored anyway")
    accepted_name = conftest.unique_name("Livia")
    good = conftest.run_token(anon, "orchard")
    accepted = conftest.send_entry(anon, good, "orchard", accepted_name, counts, 245)
    assert conftest.is_success(accepted.status_code), (
        f"counts {counts!r} sent with their own sum 245 were refused with "
        f"{accepted.status_code}: {conftest.body_text(accepted)}")


def test_orchard_maximum_is_accepted_and_nothing_above_it(anon, db):
    """The full orchard basket at 1350 is accepted and a total above it is refused."""
    counts = {"pommes": 60, "bananes": 20, "bonus": 5}
    top_name = conftest.unique_name("Maud")
    token = conftest.run_token(anon, "orchard")
    accepted = conftest.send_entry(anon, token, "orchard", top_name, counts, 1350)
    assert conftest.is_success(accepted.status_code), (
        f"the full orchard basket at the game maximum 1350 was refused with "
        f"{accepted.status_code}: {conftest.body_text(accepted)}")
    row = db.one("leaderboard_entry", id=accepted.json()["entry_id"])
    assert row["total"] == conftest.MAX_TOTALS["orchard"], (
        f"the stored total is {row['total']!r}, expected 1350")
    over_name = conftest.unique_name("Maud")
    over = conftest.run_token(anon, "orchard")
    refused = conftest.send_entry(anon, over, "orchard", over_name, counts, 1400)
    assert conftest.is_client_error(refused.status_code), (
        f"a total of 1400 above the orchard maximum returned {refused.status_code}: "
        f"{conftest.body_text(refused)}")
    assert db.count("leaderboard_entry", name=over_name) == 0, (
        "the above-maximum entry was stored")


def test_missing_item_key_counts_as_zero(anon, db):
    """An entry naming only one item key stores the other keys as zero."""
    name = conftest.unique_name("Tiago")
    token = conftest.run_token(anon, "orchard")
    response = conftest.send_entry(anon, token, "orchard", name, {"pommes": 3}, 30)
    assert conftest.is_success(response.status_code), (
        f"an entry naming only pommes was refused with {response.status_code}: "
        f"{conftest.body_text(response)}")
    row = db.one("leaderboard_entry", id=response.json()["entry_id"])
    assert conftest.counts_equal("orchard", row["counts"],
                                 {"pommes": 3, "bananes": 0, "bonus": 0}), (
        f"the stored counts read {row['counts']!r}; the keys left out of the send "
        f"must count as zero")


def test_board_lists_at_most_ten_rows_best_first(anon):
    """Every board is at most ten rows, highest total first, with consecutive ranks."""
    for game in conftest.GAMES:
        rows = conftest.board(anon, game)
        assert len(rows) <= conftest.BOARD_ROWS, (
            f"the {game} board serves {len(rows)} rows, and a board lists at most "
            f"{conftest.BOARD_ROWS}")
        totals = [row["total"] for row in rows]
        assert totals == sorted(totals, reverse=True), (
            f"the {game} board totals read {totals}, which is not highest first")
        assert [row["rank"] for row in rows] == list(range(1, len(rows) + 1)), (
            f"the {game} board ranks read {[row['rank'] for row in rows]}, expected "
            f"{list(range(1, len(rows) + 1))} with no gap and no shared rank")
        for row in rows:
            for field in ("rank", "entry_id", "name", "total"):
                assert field in row, f"a {game} board row is missing {field!r}: {row!r}"


def test_equal_totals_rank_the_earlier_entry_first(anon, db):
    """The two seeded orchard entries on 640 keep the earlier one ahead."""
    rows = conftest.board(anon, "orchard")
    names = [row["name"] for row in rows]
    assert "Nour" in names and "Hugo" in names, (
        f"the orchard board reads {names}, and both seeded entries on 640 belong on it")
    nour = rows[names.index("Nour")]
    hugo = rows[names.index("Hugo")]
    assert nour["total"] == 640 and hugo["total"] == 640, (
        f"the two seeded entries read {nour['total']} and {hugo['total']}, expected "
        f"640 apiece")
    assert hugo["rank"] == nour["rank"] + 1, (
        f"Nour ranks {nour['rank']} and Hugo ranks {hugo['rank']}; the earlier of two "
        f"equal totals comes first, so they must be consecutive")
    entries = conftest.game_entries(db, "orchard")
    above = len([row for row in entries if row["total"] > 640])
    assert nour["rank"] == above + 1, (
        f"Nour ranks {nour['rank']} while the store holds {above} orchard entries "
        f"above 640")


def test_entry_outside_the_top_ten_is_stored_and_ranked(anon, db):
    """An empty-handed run is stored, ranked past the tenth place and left off the board."""
    name = conftest.unique_name("Ilan")
    entry = conftest.accepted_entry(anon, "orchard", name,
                                    {"pommes": 0, "bananes": 0, "bonus": 0})
    assert entry["total"] == 0, f"the empty run answered total {entry['total']!r}"
    entries = conftest.game_entries(db, "orchard")
    row = db.one("leaderboard_entry", id=entry["entry_id"])
    assert row is not None, "the entry outside the top ten was never stored"
    expected = conftest.expected_rank(entries, row)
    assert int(entry["rank"]) == expected, (
        f"the entry answered rank {entry['rank']!r} while the store places it at "
        f"{expected} over the whole game")
    assert int(entry["rank"]) > conftest.BOARD_ROWS, (
        f"a total of 0 answered rank {entry['rank']!r}, which is inside the top ten "
        f"of a board holding {len(entries)} entries")
    assert conftest.row_for(conftest.board(anon, "orchard"), entry["entry_id"]) is None, (
        "an entry below the tenth place is being served on the board")


def test_seeded_boards_hold_the_tabled_entries(anon, db):
    """Every tabled seed exists once, with its counts and its own spent run."""
    seeds = {"orchard": conftest.ORCHARD_SEEDS, "lighthouse": conftest.LIGHTHOUSE_SEEDS,
             "ski": conftest.SKI_SEEDS}
    for game, table in seeds.items():
        for name, total, counts in table:
            rows = [row for row in conftest.game_entries(db, game)
                    if row["name"] == name and row["total"] == total]
            assert len(rows) == 1, (
                f"the {game} store holds {len(rows)} rows for the seed {name!r} on "
                f"{total}, expected exactly one; seeding must be idempotent")
            row = rows[0]
            assert conftest.counts_equal(game, row["counts"], counts), (
                f"the seed {name!r} stores counts {row['counts']!r}, expected {counts!r}")
            run = db.one("run", id=row["run_id"])
            assert run is not None, f"the seed {name!r} has no run of its own"
            assert run["used_at"] is not None, (
                f"the run behind the seed {name!r} is not marked used")
    ordered = [row["name"] for row in conftest.game_entries(db, "orchard")]
    tabled = [name for name, _t, _c in conftest.ORCHARD_SEEDS]
    assert ordered[:len(tabled)] == tabled, (
        f"the orchard seeds were created in the order {ordered[:len(tabled)]}, "
        f"expected {tabled}")
    assert db.count("leaderboard_entry", game_id="flight") == 0, (
        "the flight board is seeded with entries and the brief leaves it empty")


def test_store_totals_reconcile_with_the_counts_and_worths(anon, db):
    """Every stored entry reconciles against the item worths and the game maximum."""
    worths = {game: {key: worth for key, _l, worth, _m in items}
              for game, items in conftest.ITEMS.items()}
    for game in conftest.GAMES:
        for row in conftest.game_entries(db, game):
            counts = row["counts"]
            if isinstance(counts, str):
                counts = json.loads(counts)
            computed = sum(worths[game][key] * int(value)
                           for key, value in (counts or {}).items())
            assert computed == row["total"], (
                f"{game} entry {row['id']} stores total {row['total']} while its "
                f"counts {counts!r} are worth {computed}")
            assert row["total"] <= conftest.MAX_TOTALS[game], (
                f"{game} entry {row['id']} stores {row['total']}, above the game "
                f"maximum {conftest.MAX_TOTALS[game]}")


def test_empty_flight_board_answers_an_empty_array(anon):
    """The flight board answers a top-level empty array."""
    rows = conftest.board(anon, "flight")
    assert rows == [], f"the flight board serves {rows!r}, expected an empty array"


def test_legacy_reserved_name_is_served_as_anonymous(anon, owner, db):
    """The seeded reserved name is stored as written and served anonymously."""
    stored = db.one("leaderboard_entry", game_id="lighthouse", name="Admin Vireo")
    assert stored is not None, (
        "the lighthouse seed holding the reserved name is missing from the store")
    assert stored["total"] == 2080, (
        f"the reserved seed stores {stored['total']}, expected 2080")
    rows = conftest.board(anon, "lighthouse")
    top = rows[0]
    assert top["total"] == 2080 and top["rank"] == 1, (
        f"the lighthouse board opens with {top!r}, expected the 2080 entry at rank 1")
    assert top["name"] == conftest.ANONYMOUS, (
        f"the lighthouse board serves {top['name']!r} at rank 1; a stored name failing "
        f"the reserved-word rule is served as {conftest.ANONYMOUS!r}")
    listed = owner.get("/moderation/entries", params={"game": "lighthouse"})
    assert listed.status_code == 200, (
        f"the owner listing returned {listed.status_code}: {conftest.body_text(listed)}")
    names = [row.get("name") for row in listed.json()]
    assert "Admin Vireo" in names, (
        f"the owner listing reads {names}, and the owner sees the stored name")


def test_invalid_display_names_are_refused_and_nothing_is_written(anon, db):
    """A name outside the length, character or letter rule is refused."""
    cases = {"one character": "A", "seventeen characters": "Abcdefghijklmnopq",
             "symbols": "Nom<script>", "digits alone": "12345", "blank": "   "}
    for label, name in cases.items():
        token = conftest.run_token(anon, "orchard")
        response = conftest.send_entry(anon, token, "orchard", name, {"pommes": 1}, 10)
        assert conftest.is_client_error(response.status_code), (
            f"the {label} name {name!r} returned {response.status_code}, expected a "
            f"client error: {conftest.body_text(response)}")
        assert response.text.strip(), f"the refusal of the {label} name carries no reason"
        assert db.count("leaderboard_entry", name=name) == 0, (
            f"the {label} name {name!r} was stored anyway")
    good = conftest.run_token(anon, "orchard")
    edge = "Ab"
    response = conftest.send_entry(anon, good, "orchard", edge, {"pommes": 1}, 10)
    assert conftest.is_success(response.status_code), (
        f"the two-character name {edge!r} was refused with {response.status_code}, and "
        f"two characters is the pinned floor: {conftest.body_text(response)}")


def test_reserved_names_are_refused_regardless_of_case_or_accent(anon, db):
    """The reserved words are refused whatever their case or accents."""
    for name in ("ADMIN Nova", "moderateur x", "Modérateur X", "Vireo fan",
                 "Voyageur Anonyme"):
        token = conftest.run_token(anon, "orchard")
        response = conftest.send_entry(anon, token, "orchard", name, {"pommes": 1}, 10)
        assert conftest.is_client_error(response.status_code), (
            f"the reserved name {name!r} returned {response.status_code}, expected a "
            f"client error: {conftest.body_text(response)}")
        assert db.count("leaderboard_entry", name=name) == 0, (
            f"the reserved name {name!r} was stored anyway")
    folded = [conftest.fold(word) for word in conftest.RESERVED_NAMES]
    assert conftest.fold("Modérateur") in " ".join(folded), (
        "the reserved-word list in the brief does not cover the accented spelling")


def test_display_name_is_trimmed_and_spaces_collapsed(anon, db):
    """A name is trimmed and its inner space runs collapsed before it is stored."""
    tail = conftest.unique_suffix()
    entry = conftest.accepted_entry(anon, "orchard", f"  Lune   {tail}  ", {"pommes": 2})
    expected = f"Lune {tail}"
    assert entry["name"] == expected, (
        f"the accepted entry answers {entry['name']!r}, expected {expected!r}")
    row = db.one("leaderboard_entry", id=entry["entry_id"])
    assert row["name"] == expected, (
        f"the stored name reads {row['name']!r}, expected {expected!r}")


def test_board_stream_opens_with_the_current_board(anon, stream_factory):
    """The event stream opens with the board the plain request serves."""
    stream = stream_factory("orchard")
    status = conftest.poll(stream.status, "the event stream to answer", 30.0)
    assert status[1] == 200, f"the event stream answered {status[1]}"
    assert "text/event-stream" in status[2], (
        f"the event stream answers content-type {status[2]!r}, expected text/event-stream")
    opened = conftest.poll(lambda: stream.named("leaderboard"),
                           "a leaderboard event to arrive", 30.0)
    served = [row["entry_id"] for row in conftest.board(anon, "orchard")]
    assert [row["entry_id"] for row in opened[0]] == served, (
        f"the stream opened with {[r['entry_id'] for r in opened[0]]} while the board "
        f"serves {served}")


def test_board_stream_pushes_the_board_when_the_top_ten_changes(anon, stream_factory, db):
    """A new entry reaching the top ten is pushed to an open stream."""
    stream = stream_factory("ski")
    conftest.poll(lambda: stream.named("leaderboard"), "the opening board", 30.0)
    name = conftest.unique_name("Sonia")
    entry = conftest.accepted_entry(anon, "ski", name,
                                    {"portes": 40, "sauts": 15, "drapeaux": 5})
    assert int(entry["rank"]) <= conftest.BOARD_ROWS, (
        f"the full ski run answered rank {entry['rank']!r}, so it never entered the "
        f"top ten and no push is owed")
    pushed = conftest.poll(
        lambda: [board for board in stream.named("leaderboardUpdated")
                 if any(str(row.get("entry_id")) == str(entry["entry_id"])
                        for row in board)],
        f"a leaderboardUpdated carrying entry {entry['entry_id']}", 45.0)
    row = conftest.row_for(pushed[0], entry["entry_id"])
    assert row["name"] == name and row["total"] == 2600, (
        f"the pushed board carries {row!r}, which disagrees with the accepted entry")


def test_board_stream_stays_quiet_for_entries_off_the_board_or_elsewhere(anon, stream_factory):
    """Neither an entry below the top ten nor an entry on another game pushes anything."""
    stream = stream_factory("orchard")
    conftest.poll(lambda: stream.named("leaderboard"), "the opening board", 30.0)
    before = len(stream.named("leaderboardUpdated"))
    low = conftest.accepted_entry(anon, "orchard", conftest.unique_name("Remi"),
                                 {"pommes": 0, "bananes": 0, "bonus": 0})
    assert int(low["rank"]) > conftest.BOARD_ROWS, (
        f"the empty-handed entry answered rank {low['rank']!r} and belongs on the board")
    conftest.accepted_entry(anon, "lighthouse", conftest.unique_name("Remi"),
                            {"navires": 1})
    conftest.hold(6.0)
    after = len(stream.named("leaderboardUpdated"))
    assert after == before, (
        f"the orchard stream pushed {after - before} update(s) for an entry below the "
        f"top ten and an entry on the lighthouse board")


def test_owner_login_returns_an_access_token(anon):
    """The seeded owner signs in against the app and receives a bearer token."""
    response = httpx.post(f"{appclient.api_base()}/auth/login",
                          json={"email": conftest.OWNER_EMAIL,
                                "password": conftest.PASSWORD},
                          timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"POST /api/auth/login for {conftest.OWNER_EMAIL} returned "
        f"{response.status_code}: {conftest.body_text(response)}")
    token = response.json().get("access_token")
    assert isinstance(token, str) and token, (
        f"the sign-in answer carries no access_token: {response.text[:300]}")
    with appclient.client(token) as client:
        listed = client.get("/moderation/entries", params={"game": "orchard"})
    assert listed.status_code == 200, (
        f"the token the app issued was refused on an owner endpoint with "
        f"{listed.status_code}: {conftest.body_text(listed)}")


def test_wrong_password_is_denied_and_passwords_are_hashed(db):
    """A wrong password is denied and no account row carries the literal password."""
    response = httpx.post(f"{appclient.api_base()}/auth/login",
                          json={"email": conftest.OWNER_EMAIL, "password": "mauvais-mot"},
                          timeout=appclient.TIMEOUT)
    assert conftest.is_client_error(response.status_code), (
        f"a wrong password returned {response.status_code}, expected a client error: "
        f"{conftest.body_text(response)}")
    accounts = db.rows("account", limit=50)
    assert accounts, "the account table holds no rows at all"
    owner_rows = [row for row in accounts if row["email"] == conftest.OWNER_EMAIL]
    assert len(owner_rows) == 1, (
        f"the store holds {len(owner_rows)} rows for {conftest.OWNER_EMAIL}, expected one")
    row = owner_rows[0]
    assert row["role"] == "owner", f"the seeded account carries role {row['role']!r}"
    assert row["password_hash"] and conftest.PASSWORD not in str(row["password_hash"]), (
        "the seeded account stores the password in the clear rather than hashed")


def test_owner_session_expires_thirty_days_after_issue(db):
    """The issued session carries an expiry thirty days out."""
    token = appclient.login(conftest.OWNER_EMAIL, conftest.PASSWORD)
    row = db.one("session", token=token)
    assert row is not None, "the issued bearer token has no session row"
    days = conftest.days_until(row["expires_at"])
    assert 29.0 <= days <= 30.5, (
        f"the session expires in {days:.2f} days, and the brief pins thirty days from "
        f"issue")
    account = db.one("account", id=row["account_id"])
    assert account is not None and account["email"] == conftest.OWNER_EMAIL, (
        "the session does not belong to the seeded owner account")


def test_expired_owner_token_is_denied(anon, db):
    """A session moved past its expiry no longer opens the owner endpoints."""
    entry = conftest.accepted_entry(anon, "lighthouse", conftest.unique_name("Alix"),
                                    {"navires": 1})
    token = appclient.login(conftest.OWNER_EMAIL, conftest.PASSWORD)
    db.query("UPDATE session SET expires_at = %s WHERE token = %s",
             (conftest.now_utc() - conftest.datetime.timedelta(days=1), token))
    with appclient.client(token) as client:
        response = client.delete(f"/entries/{entry['entry_id']}/name")
    assert response.status_code in (401, 403), (
        f"an expired bearer token returned {response.status_code} on a removal, "
        f"expected 401 or 403: {conftest.body_text(response)}")
    row = db.one("leaderboard_entry", id=entry["entry_id"])
    assert not row["name_removed"] and row["name"] == entry["name"], (
        f"the entry now reads {row['name']!r} with name_removed {row['name_removed']!r} "
        f"although the call was denied")


def test_forged_bearer_token_is_denied_on_owner_endpoints(anon, db):
    """A token the app never issued is denied and changes nothing."""
    entry = conftest.accepted_entry(anon, "lighthouse", conftest.unique_name("Bram"),
                                    {"navires": 1})
    with appclient.client("forged-" + conftest.unique_suffix()) as client:
        removal = client.delete(f"/entries/{entry['entry_id']}/name")
        listing = client.get("/moderation/entries", params={"game": "lighthouse"})
    assert removal.status_code in (401, 403), (
        f"a forged token returned {removal.status_code} on a removal: "
        f"{conftest.body_text(removal)}")
    assert listing.status_code in (401, 403), (
        f"a forged token returned {listing.status_code} on the owner listing: "
        f"{conftest.body_text(listing)}")
    row = db.one("leaderboard_entry", id=entry["entry_id"])
    assert row["name"] == entry["name"] and not row["name_removed"], (
        f"the stored entry reads {row['name']!r} after a denied removal")


def test_anonymous_name_removal_is_denied_and_the_entry_is_unchanged(anon, db):
    """A visitor with no bearer token cannot remove a name."""
    entry = conftest.accepted_entry(anon, "lighthouse", conftest.unique_name("Cela"),
                                    {"navires": 1})
    response = anon.delete(f"/entries/{entry['entry_id']}/name")
    assert response.status_code in (401, 403), (
        f"an unauthenticated removal returned {response.status_code}, expected 401 or "
        f"403: {conftest.body_text(response)}")
    row = db.one("leaderboard_entry", id=entry["entry_id"])
    assert row["name"] == entry["name"], (
        f"the stored name reads {row['name']!r} after a denied removal, expected "
        f"{entry['name']!r}")
    assert not row["name_removed"], "the denied removal still set name_removed"
    served = conftest.board(anon, "lighthouse")
    listed = conftest.row_for(served, entry["entry_id"])
    if listed is not None:
        assert listed["name"] == entry["name"], (
            f"the board now serves {listed['name']!r} after a denied removal")


def test_moderation_listing_is_owner_only_with_the_stored_names(anon, owner, db):
    """The listing behind a board is owner-only and carries the stored names."""
    denied = anon.get("/moderation/entries", params={"game": "orchard"})
    assert denied.status_code in (401, 403), (
        f"the unauthenticated listing returned {denied.status_code}, expected 401 or "
        f"403: {conftest.body_text(denied)}")
    listed = owner.get("/moderation/entries", params={"game": "orchard"})
    assert listed.status_code == 200, (
        f"the owner listing returned {listed.status_code}: {conftest.body_text(listed)}")
    rows = listed.json()
    assert isinstance(rows, list) and rows, f"the owner listing serves {rows!r}"
    for row in rows:
        for field in ("entry_id", "name", "name_removed", "total", "created_at"):
            assert field in row, f"an owner listing row is missing {field!r}: {row!r}"
    created = [str(row["created_at"]) for row in rows]
    assert created == sorted(created, reverse=True), (
        f"the owner listing reads {created}, expected newest first")
    stored = {row["id"]: row["name"] for row in conftest.game_entries(db, "orchard")}
    for row in rows:
        assert row["name"] == stored.get(row["entry_id"]), (
            f"the listing shows {row['name']!r} for entry {row['entry_id']} while the "
            f"store holds {stored.get(row['entry_id'])!r}")


def test_owner_removes_a_name_and_the_total_stays(anon, owner, db):
    """A removed name is served anonymously while the row, total and rank stay."""
    entry = conftest.accepted_entry(anon, "lighthouse", conftest.unique_name("Diane"),
                                    {"navires": 23})
    before = int(entry["rank"])
    assert before <= conftest.BOARD_ROWS, (
        f"the entry answered rank {before}, so the board cannot show the removal")
    response = owner.delete(f"/entries/{entry['entry_id']}/name")
    assert response.status_code == 200, (
        f"the owner removal returned {response.status_code}: "
        f"{conftest.body_text(response)}")
    body = response.json()
    for field in ("entry_id", "name", "name_removed", "total"):
        assert field in body, f"the removal answer is missing {field!r}: {body!r}"
    assert body["name"] == conftest.ANONYMOUS, (
        f"the removal answers name {body['name']!r}, expected {conftest.ANONYMOUS!r}")
    assert body["name_removed"] is True, f"the removal answers {body!r}"
    assert body["total"] == entry["total"], (
        f"the total moved from {entry['total']} to {body['total']} on a name removal")
    row = db.one("leaderboard_entry", id=entry["entry_id"])
    assert row is not None, "the removal deleted the row instead of hiding the name"
    assert row["name"] == entry["name"], (
        f"the stored name reads {row['name']!r}; a removal hides the name rather than "
        f"rewriting it")
    assert row["name_removed"], "the stored row does not carry name_removed"
    assert row["total"] == entry["total"], "the stored total moved on a name removal"
    served = conftest.row_for(conftest.board(anon, "lighthouse"), entry["entry_id"])
    assert served is not None, "the entry left the board when its name was removed"
    assert served["name"] == conftest.ANONYMOUS, (
        f"the board still serves {served['name']!r} after the removal")
    assert served["rank"] == before, (
        f"the entry moved from rank {before} to {served['rank']} on a name removal")


def test_removing_an_already_removed_name_changes_nothing(anon, owner, db):
    """A second removal succeeds and leaves the row as the first one left it."""
    entry = conftest.accepted_entry(anon, "lighthouse", conftest.unique_name("Enzo"),
                                    {"navires": 2})
    first = owner.delete(f"/entries/{entry['entry_id']}/name")
    assert first.status_code == 200, (
        f"the first removal returned {first.status_code}: {conftest.body_text(first)}")
    before = db.one("leaderboard_entry", id=entry["entry_id"])
    second = owner.delete(f"/entries/{entry['entry_id']}/name")
    assert second.status_code == 200, (
        f"removing an already removed name returned {second.status_code}: "
        f"{conftest.body_text(second)}")
    after = db.one("leaderboard_entry", id=entry["entry_id"])
    assert (after["name"], after["name_removed"], after["total"]) == (
        before["name"], before["name_removed"], before["total"]), (
        f"the second removal changed the row from {before!r} to {after!r}")


def test_owner_cannot_change_a_total_or_delete_an_entry(owner, anon, db):
    """No owner call rewrites a total or deletes an entry."""
    entry = conftest.accepted_entry(anon, "lighthouse", conftest.unique_name("Faye"),
                                    {"navires": 3})
    attempts = {
        "put": owner.put(f"/entries/{entry['entry_id']}", json={"total": 2200}),
        "patch": owner.patch(f"/entries/{entry['entry_id']}", json={"total": 2200}),
        "delete": owner.delete(f"/entries/{entry['entry_id']}"),
    }
    for label, response in attempts.items():
        assert conftest.is_client_error(response.status_code), (
            f"the owner {label} on an entry returned {response.status_code}, and the "
            f"owner may neither change a total nor delete a row: "
            f"{conftest.body_text(response)}")
    row = db.one("leaderboard_entry", id=entry["entry_id"])
    assert row is not None and row["total"] == entry["total"], (
        f"the entry now reads {row!r} after the refused owner calls")


def test_signup_for_a_second_account_is_refused(db):
    """No route creates a second account."""
    before = db.count("account")
    for path in ("/auth/signup", "/auth/register", "/accounts"):
        response = httpx.post(f"{appclient.api_base()}{path}",
                              json={"email": f"second-{conftest.unique_suffix()}@example.com",
                                    "password": conftest.PASSWORD},
                              timeout=appclient.TIMEOUT)
        assert conftest.is_client_error(response.status_code), (
            f"POST /api{path} returned {response.status_code}, and the product seeds "
            f"one account with no second one: {conftest.body_text(response)}")
    assert db.count("account") == before, (
        f"the account table grew from {before} to {db.count('account')} rows")


def test_only_the_owner_endpoints_require_a_bearer_token(anon, db):
    """Playing and reading need no token; the two owner endpoints need one."""
    open_calls = {
        "games": anon.get("/games"),
        "board": anon.get("/leaderboards/orchard"),
        "run": conftest.start_run(anon, "orchard", conftest.new_player()),
    }
    for label, response in open_calls.items():
        assert conftest.is_success(response.status_code), (
            f"the anonymous {label} call returned {response.status_code}, and a "
            f"visitor plays with no account: {conftest.body_text(response)}")
    entry = conftest.accepted_entry(anon, "lighthouse", conftest.unique_name("Gaia"),
                                   {"navires": 4})
    guarded = {
        "listing": anon.get("/moderation/entries", params={"game": "lighthouse"}),
        "removal": anon.delete(f"/entries/{entry['entry_id']}/name"),
    }
    for label, response in guarded.items():
        assert response.status_code in (401, 403), (
            f"the anonymous {label} returned {response.status_code}, expected 401 or "
            f"403: {conftest.body_text(response)}")
    assert db.count("account") == 1, (
        f"the store holds {db.count('account')} accounts, and the product has one role "
        f"holder beside the account-free visitor")


def test_health_answers_on_the_public_origin(anon):
    """GET /api/health answers 200 at the address the environment names."""
    response = anon.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {conftest.body_text(response)}")
    direct = conftest.fetch("/api/health")
    assert direct.status_code == 200, (
        f"GET {appclient.app_url()}/api/health returned {direct.status_code}, so the "
        f"app is not answering on its public origin")


def test_api_is_served_under_the_api_prefix_on_one_origin(anon):
    """The HTTP API answers under /api on the same origin as the page."""
    page = conftest.fetch("/")
    assert page.status_code == 200, (
        f"GET / returned {page.status_code}, so the page and the API are not one origin")
    assert "text/html" in page.headers.get("content-type", ""), (
        f"GET / answered content-type {page.headers.get('content-type')!r}")
    assert conftest.fetch("/api/games").status_code == 200, (
        "GET /api/games did not answer on the page's own origin")
    outside = conftest.fetch("/games")
    assert outside.status_code != 200 or "json" not in outside.headers.get("content-type", ""), (
        "the API answers outside the /api prefix as well as under it")


def test_unknown_game_in_a_path_answers_not_found(anon):
    """An unknown game in a board path answers not-found."""
    for path in ("/leaderboards/jardin", "/leaderboards/jardin/events"):
        response = anon.get(path)
        assert response.status_code == 404, (
            f"GET /api{path} returned {response.status_code}, expected 404: "
            f"{conftest.body_text(response)}")


def test_list_endpoints_return_top_level_arrays(anon, owner):
    """Every listing answers a bare JSON array rather than a wrapper object."""
    for label, response in (("games", anon.get("/games")),
                            ("board", anon.get("/leaderboards/ski")),
                            ("listing", owner.get("/moderation/entries",
                                                  params={"game": "ski"}))):
        assert response.status_code == 200, (
            f"the {label} call returned {response.status_code}")
        assert isinstance(response.json(), list), (
            f"the {label} call answers {type(response.json()).__name__}, expected a "
            f"top-level array: {response.text[:200]}")


def test_environment_variables_drive_every_connection(db):
    """The app and the store are reached at the addresses the environment names."""
    for name in ("DATABASE_URL", "APP_PUBLIC_URL", "APP_PUBLIC_PORT"):
        assert os.environ.get(name), f"{name} is unset in the environment"
    assert os.environ["APP_PUBLIC_URL"].rstrip("/") == appclient.app_url(), (
        "the app is not answering at APP_PUBLIC_URL")
    port = os.environ["APP_PUBLIC_PORT"].strip()
    assert port and port in os.environ["APP_PUBLIC_URL"], (
        f"APP_PUBLIC_URL {os.environ['APP_PUBLIC_URL']!r} does not carry the published "
        f"port {port!r}")
    assert db.count("game") == len(conftest.GAMES), (
        f"the store reached through the database URL holds {db.count('game')} games, "
        f"expected {len(conftest.GAMES)}")


def test_only_the_named_backing_service_is_present(db):
    """PostgreSQL is the only backing service, with no second store beside it."""
    for name in ("REDIS_URL", "S3_ENDPOINT", "STORAGE_ENDPOINT", "SMTP_HOST",
                 "QUEUE_URL", "MEILI_URL", "OIDC_ISSUER"):
        assert not os.environ.get(name), (
            f"{name} is set in the environment, and the product introduces no second "
            f"database, cache, queue, object store, identity provider or mail vendor")
    tables = {"account", "session", "game", "game_item", "run", "leaderboard_entry"}
    for table in sorted(tables):
        assert db.count(table) >= 0, f"the store holds no table named {table!r}"
    stamps = db.query(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name = 'leaderboard_entry' AND data_type LIKE 'timestamp%'")
    assert stamps, "the entry table carries no timestamp column"


def test_user_readme_names_the_seeded_login(anon):
    """The credentials file names the seeded account beside its password."""
    path = os.path.join(conftest.APP_ROOT, "USER_README.md")
    assert os.path.isfile(path), f"{path} was not written"
    text = open(path, encoding="utf-8").read()
    assert conftest.OWNER_EMAIL in text, f"{path} does not name {conftest.OWNER_EMAIL}"
    assert conftest.PASSWORD in text, f"{path} does not carry the seeded password"


def test_reserved_directories_exist_and_are_empty(anon):
    """The two reserved directories exist at the app root and hold nothing."""
    for name in conftest.RESERVED_DIRS:
        path = os.path.join(conftest.APP_ROOT, name)
        assert os.path.isdir(path), f"{path} does not exist at the app root"
        assert os.listdir(path) == [], f"{path} is not empty: {os.listdir(path)}"


def test_absent_surfaces_answer_not_found(anon):
    """The pages the brief rules out are absent, and the document offers no form at all."""
    for path in ("/projects", "/about", "/work", "/blog", "/en", "/moderation"):
        response = conftest.fetch(path, follow_redirects=True)
        assert response.status_code == 404, (
            f"GET {path} returned {response.status_code}, and the product is one page "
            f"with no project index, no about page and no moderation page")
    served = conftest.fetch("/").text
    lowered = served.lower()
    for tag in ("<form", "<textarea", "type=\"file\"", "type=\"password\""):
        assert tag not in lowered, (
            f"the served document carries {tag!r}, and the product takes no payments, "
            f"accepts no uploads, carries no contact form and signs nobody in")
    for word in ("commentaire", "cookie", "newsletter"):
        assert word not in lowered, (
            f"the served document mentions {word!r}, and the product carries no "
            f"comments, no consent banner and no mailing list")


def test_unknown_address_serves_a_scriptless_not_found_page(anon):
    """An unknown address answers 404 with the pinned words and no script."""
    response = conftest.fetch(conftest.NOT_FOUND_PATH)
    assert response.status_code == 404, (
        f"GET {conftest.NOT_FOUND_PATH} returned {response.status_code}, expected 404")
    document = conftest.scan(response.text)
    assert document.title_text.strip() == conftest.NOT_FOUND_TITLE, (
        f"the not-found page is titled {document.title_text.strip()!r}, expected "
        f"{conftest.NOT_FOUND_TITLE!r}")
    description = document.meta("description")
    assert description and description.get("content") == conftest.NOT_FOUND_DESCRIPTION, (
        f"the not-found page describes itself as {description!r}")
    words = conftest.visible_words(response.text)
    assert conftest.NOT_FOUND_HEADING in words, (
        f"the not-found page is not headed {conftest.NOT_FOUND_HEADING!r}: {words[:200]!r}")
    back = [a for a in document.anchors if a["text"].strip() == conftest.NOT_FOUND_LINK]
    assert back and back[0]["href"] == "/", (
        f"the not-found page carries no {conftest.NOT_FOUND_LINK!r} link back to /: "
        f"{document.anchors!r}")
    assert not document.scripts, (
        f"the not-found page loads {len(document.scripts)} script(s), and it loads none")


def test_asset_directories_refuse_a_listing_and_assets_are_immutable(anon):
    """Hashed assets are immutable, fonts are WOFF2 and no directory lists itself."""
    document = conftest.scan(conftest.fetch("/").text)
    assets = conftest.same_origin_assets(document)
    assert assets, "the served document references no same-origin script or stylesheet"
    checked = 0
    for href in assets:
        path = href if href.startswith("/") else f"/{href}"
        response = conftest.fetch(path)
        if response.status_code != 200:
            continue
        checked += 1
        name = path.rsplit("/", 1)[-1]
        assert re.search(r"[-.][A-Za-z0-9_]{8,}\.(?:js|mjs|css|woff2)$", name), (
            f"the asset {name!r} carries no content hash in its file name")
        cache = response.headers.get("cache-control", "")
        assert "immutable" in cache, (
            f"the asset {name!r} answers Cache-Control {cache!r}, which lacks immutable")
        ages = re.findall(r"max-age=(\d+)", cache)
        assert ages and int(ages[0]) >= conftest.IMMUTABLE_MAX_AGE, (
            f"the asset {name!r} answers Cache-Control {cache!r}, below the pinned "
            f"max-age of {conftest.IMMUTABLE_MAX_AGE}")
        if name.endswith((".woff", ".ttf", ".otf", ".eot")):
            raise AssertionError(f"the font {name!r} is not served as WOFF2")
        directory = path.rsplit("/", 1)[0] + "/"
        listing = conftest.fetch(directory, follow_redirects=True)
        assert listing.status_code in (403, 404), (
            f"GET {directory} returned {listing.status_code}, so a static directory "
            f"lists itself")
    assert checked, "not one referenced asset answered 200"


def test_served_document_carries_the_opening_words(anon):
    """The first document already holds the loading layer, the word and all six tips."""
    response = conftest.fetch("/")
    assert response.status_code == 200, f"GET / returned {response.status_code}"
    words = conftest.plain_spaces(conftest.visible_words(response.text))
    assert conftest.LOADING_WORD in words, (
        f"the served document does not carry {conftest.LOADING_WORD!r}: {words[:300]!r}")
    for number, tip in enumerate(conftest.TIPS, start=1):
        assert conftest.plain_spaces(tip) in words, (
            f"tip {number} is missing from the served document: {tip!r}")
    assert conftest.HIDDEN_DESCRIPTION_SENTENCE in words, (
        "the served document carries no hidden description of the controls")
    assert conftest.SITE_TITLE in words, (
        "the served document carries no copy of the display title")


def test_document_declares_its_languages_title_and_description(anon):
    """The document is French while its title and description declare English."""
    response = conftest.fetch("/")
    document = conftest.scan(response.text)
    assert (document.html_lang or "").lower().startswith("fr"), (
        f"the document declares lang {document.html_lang!r}, expected French")
    assert document.title_text.strip() == conftest.PAGE_TITLE, (
        f"the page is titled {document.title_text.strip()!r}, expected "
        f"{conftest.PAGE_TITLE!r}")
    assert (document.title_attrs or {}).get("lang", "").lower().startswith("en"), (
        f"the title element declares lang {(document.title_attrs or {}).get('lang')!r}, "
        f"expected English")
    description = document.meta("description")
    assert description is not None, "the document declares no description"
    content = description.get("content", "")
    assert content == conftest.PAGE_DESCRIPTION, (
        f"the description reads {content!r}, expected {conftest.PAGE_DESCRIPTION!r}")
    assert description.get("lang", "").lower().startswith("en"), (
        f"the description element declares lang {description.get('lang')!r}, expected "
        f"English")
    assert re.search(r"<[^>]+lang=\"en\"[^>]*>\s*" + conftest.LOADING_WORD,
                     response.text), (
        f"the word {conftest.LOADING_WORD!r} does not declare English where it stands")
    assert re.search(r"<[^>]+lang=\"en\"[^>]*>[^<]*Creative Developer", response.text), (
        "the English words inside the French subtitle do not declare English")


def test_tips_use_no_break_spaces_and_typographic_apostrophes(anon):
    """French copy keeps the typographic apostrophe and the no-break space."""
    text = conftest.fetch("/").text
    assert " :" in text or " :" in text, (
        "no no-break space stands before a colon anywhere in the served document")
    for tip in conftest.TIPS[2:]:
        assert tip in text, f"the served tip does not match the pinned copy: {tip!r}"
    french = conftest.visible_words(text)
    for phrase in ("N'hésitez", "j'y explore", "l'instant"):
        assert phrase not in french, (
            f"French copy carries the straight quote in {phrase!r}")


def test_social_preview_is_declared_and_the_image_resolves(anon):
    """The social preview names the page, the site and an image of the pinned size."""
    document = conftest.scan(conftest.fetch("/").text)
    expected = {"og:title": conftest.PAGE_TITLE, "og:image": conftest.OG_IMAGE,
                "og:site_name": conftest.SITE_NAME, "og:locale": conftest.LOCALE,
                "og:locale:alternate": conftest.LOCALE_ALTERNATE,
                "twitter:card": "summary_large_image"}
    for key, value in expected.items():
        tag = document.meta(key)
        assert tag is not None, f"the document declares no {key}"
        content = tag.get("content", "")
        assert content.endswith(value) or content == value, (
            f"{key} reads {content!r}, expected {value!r}")
    image = conftest.fetch(conftest.OG_IMAGE)
    assert image.status_code == 200, (
        f"GET {conftest.OG_IMAGE} returned {image.status_code}")
    assert image.headers.get("content-type", "").startswith("image/png"), (
        f"the preview image answers content-type {image.headers.get('content-type')!r}")
    assert image.content[:8] == b"\x89PNG\r\n\x1a\n", (
        "the preview image is not a PNG by its own header")
    width, height = struct.unpack(">II", image.content[16:24])
    assert (width, height) == (conftest.SOCIAL_WIDTH, conftest.SOCIAL_HEIGHT), (
        f"the preview image is {width} by {height}, expected {conftest.SOCIAL_WIDTH} by "
        f"{conftest.SOCIAL_HEIGHT}")


def test_production_build_is_served_without_dev_tooling(anon):
    """The app serves a built bundle with no development client and no debug marks."""
    text = conftest.fetch("/").text
    lowered = text.lower()
    for marker in ("/@vite/client", "__vite_ping", "webpack-dev-server", "@solid-refresh",
                   "tweakpane", "lil-gui", "stats.js"):
        assert marker not in lowered, (
            f"the served document loads {marker!r}, which belongs to development only")
    body = re.search(r"<body[^>]*>", text)
    assert body is not None, "the served document has no body element"
    assert "debug" not in body.group(0).lower(), (
        f"the body element carries a debug class: {body.group(0)!r}")
    assert "<script" in lowered, (
        "the served document loads no script at all, so nothing can hydrate")


def test_home_screen_writes_its_title_before_offering_the_way_in(page):
    """The way in arrives four seconds after the title starts, never before."""
    conftest.open_site(page)
    conftest.wait_text(page, conftest.SITE_TITLE, conftest.WORLD_TIMEOUT)
    early = conftest.button(page, conftest.VOYAGER)
    if early.count():
        opacity = early.first.evaluate(conftest.EFFECTIVE_OPACITY_JS)
        assert opacity < 0.5, (
            f"the way in is already at opacity {opacity:.2f} as the title starts")
    started = time.monotonic()
    conftest.visible_button(page, conftest.VOYAGER, 30.0)
    waited = conftest.elapsed_since(started)
    assert waited >= 2.5, (
        f"the way in appeared {waited:.1f}s after the title started, and the brief "
        f"holds it back four seconds")
    subtitle = conftest.find_text(page, conftest.SUBTITLE)
    assert subtitle, "the home screen shows no subtitle"
    assert subtitle[0]["fontSize"] == conftest.SUBTITLE_SIZE, (
        f"the subtitle is set at {subtitle[0]['fontSize']}, expected "
        f"{conftest.SUBTITLE_SIZE}")


def test_instruction_screen_carries_its_three_lines_and_caption(page):
    """The first way in opens the welcome screen with its lines and its caption."""
    conftest.open_site(page)
    conftest.wait_home(page).click()
    conftest.wait_text(page, conftest.WELCOME, 60.0)
    assert not conftest.find_text(page, conftest.OPENING_ZONE), (
        "the first way in went straight to the world instead of the welcome screen")
    for line in conftest.WELCOME_LINES:
        assert conftest.find_text(page, line), (
            f"the welcome screen does not carry the line {line[:60]!r}")
    caption = conftest.find_text(page, conftest.INPUT_CAPTION)
    assert caption, f"the welcome screen carries no {conftest.INPUT_CAPTION!r} caption"
    assert caption[0]["fontStyle"] == "italic", (
        f"the caption is set {caption[0]['fontStyle']!r}, expected italic")
    body = conftest.find_text(page, conftest.WELCOME_LINES[0])[0]
    ratio = float(caption[0]["fontSize"][:-2]) / float(body["fontSize"][:-2])
    assert 0.71 <= ratio <= 0.79, (
        f"the caption sits at {ratio:.2f} of the text size, expected three quarters")
    heading = conftest.find_text(page, conftest.WELCOME)[0]
    assert heading["height"] <= float(heading["fontSize"][:-2]) * 1.8, (
        f"the welcome word wraps over more than one line: {heading!r}")
    started = time.monotonic()
    conftest.visible_button(page, conftest.VOYAGER, 30.0)
    assert conftest.elapsed_since(started) >= 1.2, (
        "the second way in appeared at once, and the brief drifts it up two seconds "
        "after the welcome screen")


def test_home_title_is_accessible_and_lets_the_pointer_through(page):
    """The whole sentence is readable to assistive technology and the pointer reaches the world."""
    conftest.open_site(page)
    conftest.wait_home(page)
    shown = conftest.find_text(page, conftest.SITE_TITLE)
    hidden = conftest.find_text(page, conftest.SITE_TITLE, False)
    assert len(hidden) > len(shown), (
        "the title is drawn per letter with no whole-sentence copy behind it")
    assert any(row["ariaHidden"] for row in hidden), (
        "the per-letter run is not hidden from assistive technology")
    assert any(not row["ariaHidden"] for row in hidden), (
        "no copy of the title is left for assistive technology to read")
    subtitle = conftest.find_text(page, conftest.SUBTITLE)[0]
    x, y = conftest.box_center(subtitle)
    assert conftest.hit_is_world(page, x, y), (
        "the subtitle intercepts the pointer instead of letting it reach the world")
    voyager = conftest.visible_button(page, conftest.VOYAGER, 30.0)
    box = voyager.bounding_box()
    assert conftest.hit_inside(page, voyager, *conftest.box_center(box)), (
        "the way in does not take the pointer at its own centre")
    assert page.evaluate(
        """() => { const el = [...document.querySelectorAll('*')].find(
        (n) => (n.textContent || '').trim() === 'Où sommeillent les Îles');
        const s = getComputedStyle(el);
        return s.overflowWrap !== 'break-word' && s.wordBreak !== 'break-all'; }"""), (
        "the title is allowed to break inside a word")


def test_contact_is_the_only_outbound_link(page):
    """Contact is the one link that leaves, and it says so to assistive technology."""
    conftest.open_site(page)
    conftest.wait_home(page)
    outbound = page.evaluate(
        """() => [...document.querySelectorAll('a[href]')]
        .map((a) => ({href: a.href, target: a.target, text: (a.innerText || '').trim(),
                      inner: a.textContent || ''}))
        .filter((a) => !a.href.startsWith(location.origin))""")
    assert len(outbound) == 1, (
        f"the home screen carries {len(outbound)} outbound links: {outbound!r}")
    link = outbound[0]
    assert link["href"].rstrip("/") == conftest.CONTACT_URL.rstrip("/"), (
        f"the outbound link points at {link['href']!r}, expected {conftest.CONTACT_URL!r}")
    assert link["target"] == "_blank", (
        f"the contact link opens with target {link['target']!r}, expected a new window")
    assert conftest.NEW_WINDOW_NOTE in link["inner"], (
        f"the contact link carries no hidden {conftest.NEW_WINDOW_NOTE!r} note")
    assert conftest.NEW_WINDOW_NOTE not in link["text"], (
        f"the {conftest.NEW_WINDOW_NOTE!r} note is drawn on screen rather than hidden")
    assert page.locator("form").count() == 0, (
        "the home screen carries a form, and the contact destination is a link")
    assert page.locator("input[type=password]").count() == 0, (
        "the home screen offers a sign-in field")


def test_type_scale_matches_the_pinned_faces_and_sizes(ui_page):
    """The two loaded faces carry the pinned sizes on the opening screens."""
    page = ui_page(*conftest.WIDE)
    conftest.open_site(page)
    conftest.wait_home(page)
    title = conftest.find_text(page, conftest.SITE_TITLE)[0]
    assert title["fontSize"] == conftest.TITLE_WIDE, (
        f"the home title is set at {title['fontSize']}, expected {conftest.TITLE_WIDE}")
    assert conftest.DISPLAY_FAMILY in title["fontFamily"], (
        f"the home title is set in {title['fontFamily']!r}, expected "
        f"{conftest.DISPLAY_FAMILY!r}")
    subtitle = conftest.find_text(page, conftest.SUBTITLE)[0]
    assert conftest.BODY_FAMILY in subtitle["fontFamily"], (
        f"the subtitle is set in {subtitle['fontFamily']!r}")
    assert subtitle["fontWeight"] in ("100", "200"), (
        f"the subtitle is set at weight {subtitle['fontWeight']}, expected 100")
    label = conftest.find_text(page, conftest.VOYAGER)
    assert label and label[0]["fontSize"] == conftest.BUTTON_LABEL_SIZE, (
        f"the button label is set at {label[0]['fontSize'] if label else None}, "
        f"expected {conftest.BUTTON_LABEL_SIZE}")
    conftest.visible_button(page, conftest.VOYAGER, 30.0).click()
    welcome = conftest.wait_text(page, conftest.WELCOME, 60.0)
    assert welcome["fontSize"] == conftest.WELCOME_WIDE, (
        f"the welcome word is set at {welcome['fontSize']}, expected "
        f"{conftest.WELCOME_WIDE}")
    line = conftest.find_text(page, conftest.WELCOME_LINES[0])[0]
    assert line["fontSize"] == conftest.ROOT_WIDE and line["fontWeight"] == "400", (
        f"body copy is set at {line['fontSize']} weight {line['fontWeight']}, expected "
        f"{conftest.ROOT_WIDE} weight 400")
    families = page.evaluate(
        "() => [...new Set([...document.fonts].map((f) => f.family.replace(/\"/g, '')))]")
    assert conftest.DISPLAY_FAMILY in " ".join(families), (
        f"the display face is not loaded: {families!r}")
    assert len(families) <= 3, (
        f"the page loads {len(families)} font families: {families!r}")


def test_loading_word_is_set_in_the_body_face_before_scripts_run(ui_page):
    """The first frame the server sends carries the word in the body face, bold."""
    page = ui_page(*conftest.WIDE, java_script_enabled=False)
    conftest.open_site(page)
    word = conftest.wait_text(page, conftest.LOADING_WORD, 30.0)
    assert word["fontSize"] == conftest.ROOT_WIDE, (
        f"the word is set at {word['fontSize']}, expected {conftest.ROOT_WIDE}")
    assert conftest.BODY_FAMILY in word["fontFamily"], (
        f"the word is set in {word['fontFamily']!r}, expected {conftest.BODY_FAMILY!r}")
    assert int(word["fontWeight"]) >= 700, (
        f"the word is set at weight {word['fontWeight']}, expected bold")


def test_root_type_scale_follows_the_single_breakpoint(ui_page):
    """One breakpoint governs the root size by width and by height."""
    page = ui_page(*conftest.WIDE)
    conftest.open_site(page)
    conftest.wait_home(page)
    assert conftest.root_font_size(page) == conftest.ROOT_WIDE, (
        f"the wide root reads {conftest.root_font_size(page)}, expected "
        f"{conftest.ROOT_WIDE}")
    wide_title = conftest.find_text(page, conftest.SITE_TITLE)[0]["fontSize"]
    assert wide_title == conftest.TITLE_WIDE, (
        f"the wide title reads {wide_title}, expected {conftest.TITLE_WIDE}")
    page.set_viewport_size({"width": conftest.NARROW[0], "height": conftest.NARROW[1]})
    conftest.hold(1.0)
    assert conftest.root_font_size(page) == conftest.ROOT_NARROW, (
        f"below the breakpoint the root reads {conftest.root_font_size(page)}, expected "
        f"{conftest.ROOT_NARROW}")
    narrow_title = conftest.find_text(page, conftest.SITE_TITLE)[0]["fontSize"]
    assert narrow_title == conftest.TITLE_NARROW, (
        f"the narrow title reads {narrow_title}, expected {conftest.TITLE_NARROW}")
    page.set_viewport_size({"width": conftest.SHORT[0], "height": conftest.SHORT[1]})
    conftest.hold(1.0)
    assert conftest.root_font_size(page) == conftest.ROOT_NARROW, (
        f"a short window reads root {conftest.root_font_size(page)}, and the breakpoint "
        f"applies by height as well as width")
    page.set_viewport_size({"width": conftest.NARROW[0], "height": conftest.NARROW[1]})
    conftest.visible_button(page, conftest.VOYAGER, 30.0).click()
    welcome = conftest.wait_text(page, conftest.WELCOME, 60.0)
    assert welcome["fontSize"] == conftest.WELCOME_NARROW, (
        f"the narrow welcome word reads {welcome['fontSize']}, expected "
        f"{conftest.WELCOME_NARROW}")


def test_changing_the_root_size_rescales_the_interface(page):
    """Every interface measure follows the one root size."""
    conftest.open_site(page)
    voyager = conftest.wait_home(page)
    before = voyager.bounding_box()
    page.evaluate("() => { document.documentElement.style.fontSize = '38px'; }")
    conftest.hold(1.0)
    after = voyager.bounding_box()
    ratio = after["height"] / before["height"]
    assert 1.8 <= ratio <= 2.2, (
        f"doubling the root size moved the button height by {ratio:.2f}, expected the "
        f"interface to grow with the root")
    width_ratio = after["width"] / before["width"]
    assert 1.6 <= width_ratio <= 2.4, (
        f"doubling the root size moved the button width by {width_ratio:.2f}")


def test_world_arrival_names_the_zone_and_shows_the_corner_controls(page):
    """The world arrives named, focusable and framed by its two corner controls."""
    conftest.open_site(page)
    conftest.wait_home(page)
    assert conftest.button(page, conftest.NOTEBOOK_CONTROL).count() == 0, (
        "the notebook control is offered on the home screen")
    conftest.visible_button(page, conftest.VOYAGER, 30.0).click()
    conftest.wait_text(page, conftest.WELCOME, 60.0)
    conftest.visible_button(page, conftest.VOYAGER, 60.0).click()
    notebook = conftest.visible_button(page, conftest.NOTEBOOK_CONTROL,
                                       conftest.WORLD_TIMEOUT)
    conftest.wait_text(page, conftest.OPENING_ZONE, 60.0)
    announced = conftest.poll(
        lambda: conftest.ARRIVAL_PREFIX + conftest.OPENING_ZONE in
        conftest.live_region_text(page), "the arrival announcement", 30.0)
    assert announced, "the opening zone was never announced in the live region"
    size = page.viewport_size
    menu = conftest.corner_control(page, conftest.MENU_NAME).bounding_box()
    assert menu["x"] < size["width"] * 0.25 and menu["y"] < size["height"] * 0.35, (
        f"the menu control sits at {menu!r}, expected the top-left corner")
    book = notebook.bounding_box()
    assert book["x"] > size["width"] * 0.6 and book["y"] > size["height"] * 0.55, (
        f"the notebook control sits at {book!r}, expected the bottom-right corner")
    for label, locator in ((conftest.MENU_NAME, conftest.corner_control(page, conftest.MENU_NAME)),
                           (conftest.NOTEBOOK_CONTROL, notebook)):
        assert locator.evaluate("(el) => !!el.querySelector('canvas')"), (
            f"the {label} control draws no canvas of its own")
    surface = page.locator("[role=application]")
    assert surface.count() >= 1, "the world surface is no application region"
    assert surface.first.get_attribute("tabindex") == "0", (
        "the world surface is not focusable")
    assert surface.first.evaluate(
        """(el) => { const c = el.matches('canvas') ? el : el.querySelector('canvas');
        return !!c && (c.dataset.engine || '').toLowerCase().includes('three'); }"""), (
        "the world surface holds no canvas drawn through three")
    assert conftest.button(page, "Interagir").count() == 0, (
        "the touch pad is drawn on a pointer machine")
    for teaching in ("flèches directionnelles", "manette de jeu"):
        assert not conftest.find_text(page, teaching), (
            f"an overlay still teaches the controls in the world: {teaching!r}")


def test_second_load_shows_the_loading_screen_again(page):
    """The loading screen carries a live figure, one tip at a time, and returns."""
    conftest.open_site(page)
    canvas_seen = conftest.poll(
        lambda: page.evaluate(
            """() => { const t = [...document.querySelectorAll('*')].find(
            (n) => (n.textContent || '').trim() === 'LOADING');
            return !!t && !!document.querySelector('canvas'); }"""),
        "a live figure beside the loading word", 60.0)
    assert canvas_seen, "the loading screen draws nothing live"
    assert page.locator("progress, [role=progressbar]").count() == 0, (
        "the loading screen shows a progress bar")
    samples = []
    for _ in range(8):
        samples.append(page.evaluate(
            """([tips]) => { const vis = (el) => { let o = 1;
            for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
              const s = getComputedStyle(n);
              if (s.display === 'none' || s.visibility === 'hidden') return 0;
              o *= parseFloat(s.opacity || '1'); }
            return o; };
            const out = [];
            for (const tip of tips) {
              for (const el of document.querySelectorAll('body *')) {
                if ((el.textContent || '').replace(/\\s+/g, ' ').trim() !== tip) continue;
                if (el.children.length) continue;
                if (vis(el) > 0.6) out.push(tip);
              } }
            return out; }""", [list(conftest.TIPS)]))
        conftest.hold(1.2)
    assert any(len(sample) == 1 for sample in samples), (
        f"no sample of the loading screen showed exactly one tip: {samples!r}")
    assert all(len(sample) <= 1 for sample in samples), (
        f"more than one tip stood at full strength at once: {samples!r}")
    shown = {tip for sample in samples for tip in sample}
    assert len(shown) >= 2, (
        f"the tip never changed over {len(samples)} samples: {shown!r}")
    conftest.wait_home(page).click()
    conftest.wait_text(page, conftest.WELCOME, 60.0)
    page.evaluate(
        """() => { window.__deku_loading = false;
        const check = () => { const t = [...document.querySelectorAll('*')].find(
          (n) => (n.textContent || '').trim() === 'LOADING');
        if (t) { const r = t.getBoundingClientRect();
          if (r.width > 2 && r.height > 2) window.__deku_loading = true; }
        requestAnimationFrame(check); };
        requestAnimationFrame(check); }""")
    conftest.visible_button(page, conftest.VOYAGER, 60.0).click()
    conftest.visible_button(page, conftest.NOTEBOOK_CONTROL, conftest.WORLD_TIMEOUT)
    assert page.evaluate("() => window.__deku_loading === true"), (
        "no loading screen stood between the second way in and the world")


def test_reload_returns_to_the_opening_screens_without_error(page):
    """A reload from the world returns through the opening screens with nothing kept."""
    conftest.enter_world(page)
    start = page.url
    page.reload(wait_until="domcontentloaded")
    conftest.wait_home(page)
    assert page.url == start, (
        f"the address moved from {start!r} to {page.url!r} across the journey")
    assert conftest.button(page, conftest.NOTEBOOK_CONTROL).count() == 0, (
        "the world survived the reload instead of returning to the home screen")
    assert not conftest.find_text(page, conftest.OPENING_ZONE), (
        "the zone the visitor stood in was kept across the reload")
    assert conftest.errors_of(page) == [], (
        f"the journey raised page errors: {conftest.errors_of(page)!r}")


def test_menu_opens_by_click_or_key_and_escape_returns_focus(page):
    """The menu opens either way, names its sections and hands focus back."""
    conftest.enter_world(page)
    control = conftest.corner_control(page, conftest.MENU_NAME)
    name = control.evaluate("(el) => el.getAttribute('aria-label') || el.innerText || ''")
    assert conftest.MENU_NAME in name and "M" in name, (
        f"the menu control is named {name!r}, and it keeps its key in the accessibility "
        f"tree")
    assert control.evaluate(
        """(el) => [...el.querySelectorAll('*')].concat([el]).every((n) =>
        ![...n.childNodes].some((c) => c.nodeType === 3 && c.textContent.trim()) ||
        n.getBoundingClientRect().width <= 2 || n.getBoundingClientRect().height <= 2 ||
        getComputedStyle(n).clipPath !== 'none' || getComputedStyle(n).clip !== 'auto')"""), (
        "the menu control draws its name on screen instead of keeping it for assistive "
        "technology")
    control.click()
    conftest.wait_text(page, conftest.CLASSEMENTS, 30.0)
    assert control.get_attribute("aria-expanded") == "true", (
        f"the menu control reports aria-expanded "
        f"{control.get_attribute('aria-expanded')!r} while the panel stands open")
    assert conftest.find_text(page, conftest.RESUME), (
        f"the panel does not carry {conftest.RESUME!r}")
    for label in conftest.GAME_LABELS.values():
        assert conftest.button(page, label).count() >= 1, (
            f"the boards section does not list {label!r}")
    assert conftest.button(page, conftest.END_RUN).count() == 0, (
        f"the panel offers {conftest.END_RUN!r} outside a run")
    page.keyboard.press("Escape")
    conftest.poll(lambda: not conftest.find_text(page, conftest.CLASSEMENTS),
                  "the panel to close", 20.0)
    assert control.get_attribute("aria-expanded") in ("false", None), (
        "the menu control still reports the panel open after Escape")
    assert control.evaluate(
        "(el) => el === document.activeElement || el.contains(document.activeElement)"), (
        "focus did not return to the menu control after Escape")
    page.keyboard.press("m")
    conftest.wait_text(page, conftest.CLASSEMENTS, 20.0)


def test_settings_are_real_radio_groups_with_legends(page):
    """Every setting is a named group of radios, operable from the keyboard."""
    conftest.enter_world(page)
    conftest.open_menu(page)
    for legend, options in conftest.SETTING_GROUPS.items():
        group = page.get_by_role("group", name=re.compile(re.escape(legend)))
        assert group.count() >= 1, f"no group is named {legend!r}"
        for option in options:
            radio = group.first.get_by_role("radio", name=re.compile(re.escape(option)))
            assert radio.count() == 1, (
                f"the group {legend!r} offers {radio.count()} radios named {option!r}")
    quality = page.get_by_role("group", name=re.compile("Qualité")).first
    default = quality.get_by_role("radio", name=re.compile("Moyenne"))
    assert default.is_checked(), (
        f"the quality group does not default to Moyenne")
    for switch in conftest.SETTING_SWITCHES:
        assert page.get_by_label(re.compile(re.escape(switch))).count() >= 1, (
            f"no switch is labelled {switch!r}")
    size = page.get_by_role("group", name=re.compile("Taille du texte")).first
    normal = size.get_by_role("radio", name=re.compile("Normale"))
    large = size.get_by_role("radio", name=re.compile("Grande"))
    normal.focus()
    page.keyboard.press("ArrowRight")
    conftest.hold(0.6)
    assert large.is_checked(), (
        "the arrow key does not move the choice inside the text size group")
    weights = page.evaluate(
        """([on, off]) => { const label = (text) => {
          const el = [...document.querySelectorAll('label, span, div')].find(
            (n) => (n.textContent || '').trim() === text && n.children.length === 0);
          return el ? parseInt(getComputedStyle(el).fontWeight, 10) : null; };
        return [label(on), label(off)]; }""", ["Grande", "Normale"])
    assert weights[0] and weights[1] and weights[0] > weights[1], (
        f"the chosen option is set at weight {weights[0]} beside {weights[1]} for the "
        f"one not chosen")


def test_text_size_choice_applies_at_once_and_persists(page):
    """The larger text size takes hold at once, follows the breakpoint and survives a reload."""
    conftest.enter_world(page)
    conftest.open_menu(page)
    page.get_by_role("group", name=re.compile("Taille du texte")).first.get_by_role(
        "radio", name=re.compile("Grande")).check()
    conftest.poll(lambda: conftest.root_font_size(page) == conftest.ROOT_WIDE_LARGE,
                  f"the root to reach {conftest.ROOT_WIDE_LARGE}", 20.0)
    page.set_viewport_size({"width": conftest.NARROW[0], "height": conftest.NARROW[1]})
    conftest.poll(lambda: conftest.root_font_size(page) == conftest.ROOT_NARROW_LARGE,
                  f"the narrow root to reach {conftest.ROOT_NARROW_LARGE}", 20.0)
    page.set_viewport_size({"width": conftest.WIDE[0], "height": conftest.WIDE[1]})
    conftest.enter_world(page)
    assert conftest.root_font_size(page) == conftest.ROOT_WIDE_LARGE, (
        f"after a reload the root reads {conftest.root_font_size(page)}, expected "
        f"{conftest.ROOT_WIDE_LARGE}")
    conftest.open_menu(page)
    assert page.get_by_role("group", name=re.compile("Taille du texte")).first.get_by_role(
        "radio", name=re.compile("Grande")).is_checked(), (
        "the chosen text size is no longer chosen after a reload")


def test_quality_choice_changes_the_world_pixel_density(ui_page):
    """The quality choice moves the drawing density of the world surface."""
    page = ui_page(1280, 800, device_scale_factor=2)
    conftest.enter_world(page)
    conftest.open_menu(page)
    quality = page.get_by_role("group", name=re.compile("Qualité")).first
    quality.get_by_role("radio", name=re.compile("Haute")).check()
    high = conftest.poll(lambda: conftest.world_density(page) >= 1.8,
                         "the high quality density", 30.0)
    assert high, f"the world draws at {conftest.world_density(page):.2f} device pixels"
    conftest.open_menu(page)
    quality.get_by_role("radio", name=re.compile("Basse")).check()
    low = conftest.poll(lambda: conftest.world_density(page) <= 1.05,
                        "the low quality density", 30.0)
    assert low, (
        f"at the low quality the world still draws at {conftest.world_density(page):.2f} "
        f"device pixels per interface pixel")


def test_reduced_motion_writes_the_title_at_once(ui_page):
    """A visitor who asks for less motion gets the whole title at once."""
    page = ui_page(*conftest.WIDE, reduced_motion="reduce")
    conftest.open_site(page)
    conftest.wait_text(page, conftest.SITE_TITLE, conftest.WORLD_TIMEOUT)
    running = page.evaluate(
        """([title]) => { const el = [...document.querySelectorAll('*')].find(
        (n) => (n.textContent || '').replace(/\\s+/g, ' ').trim() === title);
        if (!el) return -1;
        return document.getAnimations().filter((a) => a.playState === 'running' &&
          a.effect && a.effect.target && el.contains(a.effect.target) &&
          (a.effect.getComputedTiming().duration || 0) > 50).length; }""",
        [conftest.SITE_TITLE])
    assert running == 0, (
        f"{running} letter animations were still running under reduced motion")
    conftest.enter_world(page)
    conftest.open_menu(page)
    assert page.get_by_role("group", name=re.compile("Animations")).first.get_by_role(
        "radio", name=re.compile("Réduites")).is_checked(), (
        "the animations group does not default to the reduced choice when the system "
        "asks for less motion")


def test_every_board_departs_to_its_keeper(page):
    """Each board opens read-only, sends the character to its zone and its keeper speaks."""
    conftest.enter_world(page)
    for game in conftest.GAMES:
        conftest.open_board(page, game)
        assert page.get_by_label(conftest.NAME_LABEL).count() == 0, (
            f"the {game} board opened from the menu offers a name form")
        assert conftest.find_text(page, conftest.GAME_LABELS[game]), (
            f"the {game} board is not titled {conftest.GAME_LABELS[game]!r}")
        assert conftest.button(page, conftest.CLOSE_BOARD).count() >= 1, (
            f"the {game} board offers no {conftest.CLOSE_BOARD!r}")
        prompt = conftest.depart(page, game)
        zone = conftest.find_text(page, conftest.GAME_ZONES[game])[0]
        assert zone["fontWeight"] in ("200", "300"), (
            f"the zone card is set at weight {zone['fontWeight']}, expected 200")
        assert zone["width"] <= page.viewport_size["width"] * 0.5 + 2, (
            f"the zone card is {zone['width']:.0f} wide on a "
            f"{page.viewport_size['width']} screen")
        assert conftest.ARRIVAL_PREFIX + conftest.GAME_ZONES[game] in \
            conftest.live_region_text(page), (
            f"arriving in {conftest.GAME_ZONES[game]!r} was not announced")
        label = prompt.evaluate("(el) => el.getAttribute('aria-label') || el.innerText || ''")
        assert conftest.TALK in label and "E" in label, (
            f"the prompt reads {label!r}, and it names the action with its key")
        if game == "orchard":
            page.keyboard.press("e")
        else:
            prompt.click()
        conftest.wait_text(page, conftest.KEEPER_LINES[game], 30.0)
        assert conftest.find_text(page, conftest.KEEPERS[game]), (
            f"the {game} dialogue does not name {conftest.KEEPERS[game]!r} above the line")
        line = conftest.find_text(page, conftest.KEEPER_LINES[game])[0]
        assert line["width"] <= page.viewport_size["width"] * 0.85, (
            f"the dialogue line runs {line['width']:.0f} across a "
            f"{page.viewport_size['width']} screen")
        menu = conftest.corner_control(page, conftest.MENU_NAME)
        assert conftest.hit_inside(page, menu, *conftest.box_center(menu.bounding_box())), (
            "the dialogue covers the menu control")
        assert conftest.KEEPER_LINES[game] in conftest.live_region_text(page), (
            f"the {game} dialogue line was not announced in the live region")
        for choice in (conftest.START, conftest.LATER):
            assert conftest.button(page, choice).count() >= 1, (
                f"the {game} dialogue offers no {choice!r}")
        conftest.visible_button(page, conftest.LATER, 20.0).click()
        conftest.poll(lambda: not conftest.find_text(page, conftest.KEEPER_LINES[game]),
                      "the dialogue to close", 20.0)
    assert conftest.button(page, conftest.END_RUN).count() == 0, (
        f"{conftest.LATER!r} started a run all the same")


def test_prompt_darkens_where_the_world_is_bright(page):
    """The prompt is light at the orchard and dark at the lighthouse."""
    conftest.enter_world(page)
    orchard = conftest.depart(page, "orchard")
    light = conftest.luminance(orchard.evaluate(
        "(el) => getComputedStyle(el).color"))
    lighthouse = conftest.depart(page, "lighthouse")
    dark = conftest.luminance(lighthouse.evaluate(
        "(el) => getComputedStyle(el).color"))
    assert light > dark, (
        f"the prompt reads at luminance {light:.2f} at the orchard and {dark:.2f} at "
        f"the lighthouse, and it turns dark in the bright places")


def test_orchard_run_shows_its_display_and_can_end_early(page):
    """The orchard run starts at sixty, holds while the menu is open and ends on request."""
    starts = []
    page.on("request", lambda request: starts.append(request.url)
            if request.method == "POST" and request.url.endswith("/api/runs") else None)
    conftest.enter_world(page)
    conftest.begin_run(page, "orchard")
    clock = conftest.poll(
        lambda: [row for row in conftest.numeric_texts(page) if 50 <= row["value"] <= 60],
        "the orchard clock to appear", 30.0)
    assert starts, "the run began without the browser starting a run on the server"
    biggest = max(clock, key=lambda row: row["size"])
    root = float(conftest.root_font_size(page)[:-2])
    assert abs(biggest["size"] - root * 3) <= 2.0, (
        f"the clock is set at {biggest['size']:.1f}px beside a root of {root}px, "
        f"expected three root units")
    assert biggest["weight"] >= 700, (
        f"the clock is set at weight {biggest['weight']}, expected bold")
    assert not conftest.hit_inside(
        page, page.locator("body"), biggest["x"], biggest["y"]) or \
        conftest.hit_is_world(page, biggest["x"], biggest["y"]), (
        "the display takes the pointer instead of letting it reach the world")
    conftest.open_menu(page)
    assert conftest.button(page, conftest.END_RUN).count() >= 1, (
        f"the panel does not offer {conftest.END_RUN!r} during a run")
    held = conftest.poll(
        lambda: [row["value"] for row in conftest.numeric_texts(page)
                 if 1 <= row["value"] <= 60], "the clock while the panel is open", 20.0)
    conftest.hold(3.0)
    again = [row["value"] for row in conftest.numeric_texts(page) if 1 <= row["value"] <= 60]
    assert set(held) & set(again), (
        f"the clock moved from {held} to {again} while the menu stood open")
    conftest.visible_button(page, conftest.END_RUN, 20.0).click()
    conftest.wait_text(page, conftest.TOTAL_ROW, 30.0)
    for label in ("Pommes", "Bananes", "Bonus"):
        assert conftest.find_text(page, label), (
            f"the receipt carries no {label!r} row")
    total = conftest.find_text(page, conftest.TOTAL_ROW)[0]
    rows = conftest.find_text(page, "Pommes")[0]
    assert float(total["fontSize"][:-2]) > float(rows["fontSize"][:-2]), (
        f"the total row is set at {total['fontSize']} beside a run row at "
        f"{rows['fontSize']}, and the total is set apart")
    conftest.visible_button(page, conftest.CONTINUE, 20.0).click()
    conftest.poll(lambda: page.get_by_label(conftest.NAME_LABEL).count(),
                  "the name form to arrive", 30.0)


def test_orchard_run_ends_when_the_clock_runs_out(page):
    """An orchard run left alone ends itself at zero."""
    conftest.enter_world(page)
    conftest.begin_run(page, "orchard")
    started = time.monotonic()
    conftest.wait_text(page, conftest.TOTAL_ROW, 110.0)
    waited = conftest.elapsed_since(started)
    assert waited >= 45.0, (
        f"the orchard run ended by itself after {waited:.0f}s, and its clock starts at "
        f"60 seconds")


def test_lighthouse_run_starts_at_ninety(page):
    """The lighthouse run opens its display at ninety seconds."""
    conftest.enter_world(page)
    conftest.begin_run(page, "lighthouse")
    found = conftest.poll(
        lambda: [row for row in conftest.numeric_texts(page) if 80 <= row["value"] <= 90],
        "the lighthouse clock to appear", 30.0)
    assert found, "the lighthouse display shows no clock near ninety seconds"


def test_signing_the_board_from_a_run_writes_one_entry(page, db):
    """The name form sends once, says so and shows the visitor's own rank."""
    conftest.enter_world(page)
    conftest.begin_run(page, "orchard")
    conftest.end_run_now(page)
    field = conftest.reach_name_form(page)
    name = "Wwwwwwwww " + conftest.unique_suffix()
    field.fill(name)
    held = []
    page.route("**/api/entries", lambda route: held.append(route))
    send = conftest.visible_button(page, conftest.SEND, 20.0)
    send.click()
    conftest.poll(lambda: held and page.evaluate("() => 1"),
                  "the send to reach the network", 20.0)
    assert send.is_disabled() or send.get_attribute("aria-disabled") == "true", (
        "the send button stays available while a send is in flight")
    held[0].continue_()
    page.unroute("**/api/entries")
    conftest.wait_text(page, conftest.SENT_NOTE, 30.0)
    assert page.get_by_label(conftest.NAME_LABEL).count() == 0, (
        "the name form is offered again after an accepted send")
    assert conftest.SENT_PREFIX in conftest.live_region_text(page), (
        f"the send was not announced with {conftest.SENT_PREFIX!r}: "
        f"{conftest.live_region_text(page)[:200]!r}")
    assert conftest.find_text(page, name), (
        "the visitor's own entry is not shown above the board")
    rows = db.rows("leaderboard_entry", limit=5, name=name)
    assert len(rows) == 1, (
        f"the store holds {len(rows)} rows named {name!r} after one send")
    assert rows[0]["game_id"] == "orchard", (
        f"the sent entry landed on {rows[0]['game_id']!r}")


def test_invalid_name_is_refused_inline_and_names_the_field(page, db):
    """A one-letter name is refused in place, keeping the typed text and writing nothing."""
    conftest.enter_world(page)
    conftest.begin_run(page, "orchard")
    conftest.end_run_now(page)
    field = conftest.reach_name_form(page)
    field.fill("A")
    conftest.visible_button(page, conftest.SEND, 20.0).click()
    conftest.poll(lambda: conftest.find_text(page, conftest.NAME_LABEL, False),
                  "a refusal naming the field", 30.0)
    message = conftest.poll(
        lambda: [row for row in conftest.find_text(page, conftest.NAME_LABEL, False)],
        "the inline refusal", 20.0)
    assert message, "no message names the field after the refusal"
    assert page.get_by_label(conftest.NAME_LABEL).count() >= 1, (
        "the form was taken away instead of keeping the typed text")
    assert page.get_by_label(conftest.NAME_LABEL).first.input_value() == "A", (
        "the typed text was cleared by the refusal")
    assert conftest.REFUSED_PREFIX in conftest.live_region_text(page), (
        f"the refusal was not announced with {conftest.REFUSED_PREFIX!r}")
    assert db.count("leaderboard_entry", name="A") == 0, (
        "the refused name was stored anyway")


def test_board_rows_show_the_rank_the_name_and_the_total(page, anon, db):
    """A board carries its game label, italic names and totals held inside the panel."""
    long_name = "Wwwwwwwww " + conftest.unique_suffix()
    conftest.accepted_entry(anon, "orchard", long_name,
                            {"pommes": 60, "bananes": 20, "bonus": 5})
    conftest.enter_world(page)
    conftest.open_board(page, "orchard")
    rows = conftest.board(anon, "orchard")
    assert conftest.find_text(page, conftest.GAME_LABELS["orchard"]), (
        "the board is not titled with its game label")
    first = conftest.find_text(page, rows[0]["name"])
    second = conftest.find_text(page, rows[1]["name"])
    assert first and second, (
        f"the board does not show {rows[0]['name']!r} and {rows[1]['name']!r}")
    assert first[0]["fontStyle"] == "italic", (
        f"the name on the board is set {first[0]['fontStyle']!r}, expected italic")
    assert float(first[0]["fontSize"][:-2]) > float(second[0]["fontSize"][:-2]) * 1.15, (
        f"the first row is set at {first[0]['fontSize']} beside {second[0]['fontSize']} "
        f"for the second, and the first row is noticeably larger")
    totals = conftest.find_text(page, str(rows[0]["total"]))
    assert totals, f"the board shows no total {rows[0]['total']!r}"
    digits = totals[0]
    assert "tabular-nums" in (digits["numeric"] or "") or \
        "tnum" in (digits["features"] or ""), (
        f"the totals are set with numeric features {digits['numeric']!r} "
        f"{digits['features']!r}, and they line up on the digits")
    if long_name in [row["name"] for row in rows]:
        name_cell = conftest.find_text(page, long_name)[0]
        assert name_cell["x"] + name_cell["width"] <= page.viewport_size["width"], (
            "a long name pushes the row past the panel instead of shrinking")


def test_empty_flight_board_shows_its_empty_line(page):
    """The board with no entries says so in its own words."""
    conftest.enter_world(page)
    conftest.open_board(page, "flight")
    assert conftest.find_text(page, conftest.EMPTY_BOARD), (
        f"the flight board does not read {conftest.EMPTY_BOARD!r}")
    assert conftest.button(page, conftest.DEPART).count() >= 1, (
        f"the empty board offers no {conftest.DEPART!r}")
    conftest.visible_button(page, conftest.CLOSE_BOARD, 20.0).click()
    conftest.poll(lambda: not conftest.find_text(page, conftest.EMPTY_BOARD),
                  "the board to close", 20.0)


def test_notebook_opens_with_its_pages_and_handwriting(page):
    """The notebook opens on the key, turns its pages and closes on Escape."""
    conftest.enter_world(page)
    page.keyboard.press("i")
    title = conftest.wait_text(page, conftest.NOTEBOOK_TITLE, 30.0)
    body_face = conftest.find_text(page, conftest.OPENING_ZONE, False)
    assert conftest.BODY_FAMILY not in title["fontFamily"] and \
        conftest.DISPLAY_FAMILY not in title["fontFamily"], (
        f"the notebook is set in {title['fontFamily']!r}, and its face is the "
        f"handwriting one used nowhere else")
    size = page.viewport_size
    book = page.evaluate(
        """([title, next]) => { const has = (el, t) =>
        (el.textContent || '').includes(t);
        const all = [...document.querySelectorAll('body *')].filter(
          (el) => has(el, title) && has(el, next));
        if (!all.length) return null;
        const el = all[all.length - 1];
        const r = el.getBoundingClientRect();
        return {width: r.width, height: r.height}; }""",
        [conftest.NOTEBOOK_TITLE, conftest.NEXT_PAGE])
    assert book is not None, "the notebook and its page controls share no panel"
    assert book["width"] > book["height"], (
        f"the notebook stands {book['width']:.0f} by {book['height']:.0f}, and it stays "
        f"landscape")
    assert book["height"] <= size["height"] * 0.8 + 4, (
        f"the notebook is {book['height']:.0f} tall on a {size['height']} screen")
    assert book["width"] <= size["width"] * 0.75 + 4, (
        f"the notebook is {book['width']:.0f} wide on a {size['width']} screen")
    ratio = book["width"] / book["height"]
    assert 1.3 <= ratio <= 1.7, (
        f"the notebook spread is {ratio:.2f} times as wide as tall, expected about one "
        f"and a half")
    seen = []
    for _ in range(5):
        for label in conftest.NOTEBOOK_PAGES:
            if conftest.find_text(page, label) and label not in seen:
                seen.append(label)
        if conftest.EMPTY_PAGE not in seen and conftest.find_text(page, conftest.EMPTY_PAGE):
            seen.append(conftest.EMPTY_PAGE)
        conftest.visible_button(page, conftest.NEXT_PAGE, 20.0).click()
        conftest.hold(1.0)
    for label in conftest.NOTEBOOK_PAGES:
        assert label in seen, f"turning the pages never reached {label!r}: {seen!r}"
    assert conftest.EMPTY_PAGE in seen, (
        f"no page read {conftest.EMPTY_PAGE!r} on a fresh visit: {seen!r}")
    assert conftest.button(page, conftest.PREVIOUS_PAGE).count() >= 1, (
        f"the notebook carries no {conftest.PREVIOUS_PAGE!r}")
    for label in ("Pommes", "Bananes", "Bonus"):
        assert conftest.find_text(page, label, False), (
            f"the tallies page does not list {label!r}")
    assert conftest.hit_is_world(page, size["width"] * 0.04, size["height"] * 0.5), (
        "the space around the notebook takes the pointer")
    page.keyboard.press("Escape")
    conftest.poll(lambda: not conftest.find_text(page, conftest.NOTEBOOK_TITLE),
                  "the notebook to close", 20.0)
    assert body_face is not None, "the world was never reached"


def test_finished_run_writes_the_journal_and_keeps_it_across_a_reload(page):
    """The first finished orchard run leaves a journal line that survives a reload."""
    sent = []
    page.on("request", lambda request: sent.append((request.method, request.url))
            if request.method in ("POST", "PUT", "PATCH", "DELETE") else None)
    conftest.enter_world(page)
    conftest.begin_run(page, "orchard")
    conftest.end_run_now(page)
    conftest.open_notebook_page(page, conftest.BRIDGE_ENTRY)
    conftest.enter_world(page)
    conftest.open_notebook_page(page, conftest.BRIDGE_ENTRY)
    for method, url in sent:
        assert url.rstrip("/").endswith(("/api/runs", "/api/entries")), (
            f"the browser sent {method} {url}, and the notebook stays in the visitor's "
            f"own browser")


def test_keyboard_alone_reaches_a_moving_character(page):
    """Tab and Enter cross the opening screens and reach the world surface."""
    conftest.open_site(page)
    conftest.wait_home(page)
    focused = None
    for _ in range(15):
        page.keyboard.press("Tab")
        name = page.evaluate(
            """() => { const a = document.activeElement;
            return a ? (a.getAttribute('aria-label') || a.innerText || '').trim() : ''; }""")
        if conftest.VOYAGER in name:
            focused = name
            break
    assert focused, "fifteen presses of Tab never reached the way in"
    ring = page.evaluate(
        """() => { const s = getComputedStyle(document.activeElement);
        return {style: s.outlineStyle, width: parseFloat(s.outlineWidth) || 0,
                shadow: s.boxShadow}; }""")
    assert (ring["style"] != "none" and ring["width"] >= conftest.FOCUS_RING_MIN) or \
        (ring["shadow"] and ring["shadow"] != "none"), (
        f"the focused control draws no focus ring: {ring!r}")
    page.keyboard.press("Enter")
    conftest.wait_text(page, conftest.WELCOME, 60.0)
    for _ in range(15):
        page.keyboard.press("Tab")
        name = page.evaluate(
            """() => { const a = document.activeElement;
            return a ? (a.getAttribute('aria-label') || a.innerText || '').trim() : ''; }""")
        if conftest.VOYAGER in name:
            break
    page.keyboard.press("Enter")
    conftest.visible_button(page, conftest.NOTEBOOK_CONTROL, conftest.WORLD_TIMEOUT)
    for _ in range(20):
        page.keyboard.press("Tab")
        if page.evaluate(
                """() => { const a = document.activeElement;
                return !!a && !!a.closest('[role=application]'); }"""):
            break
    assert page.evaluate(
        """() => { const a = document.activeElement;
        return !!a && !!a.closest('[role=application]'); }"""), (
        "the world surface is never reached by Tab")
    page.keyboard.down("ArrowUp")
    conftest.hold(1.5)
    page.keyboard.up("ArrowUp")
    assert page.evaluate("() => window.scrollY") == 0, (
        "the arrow keys scroll the document instead of walking the character")
    assert conftest.errors_of(page) == [], (
        f"walking from the keyboard raised {conftest.errors_of(page)!r}")


def test_gamepad_buttons_commit_close_and_open_the_layers(ui_page):
    """The four face buttons and the start button reach the same actions as the keys."""
    page = ui_page(*conftest.WIDE)
    page.add_init_script(conftest.GAMEPAD_JS)
    conftest.open_site(page)
    conftest.wait_home(page)
    conftest.press_pad(page, 0)
    conftest.wait_text(page, conftest.WELCOME, 60.0)
    conftest.press_pad(page, 0)
    conftest.visible_button(page, conftest.NOTEBOOK_CONTROL, conftest.WORLD_TIMEOUT)
    conftest.press_pad(page, 9)
    conftest.wait_text(page, conftest.CLASSEMENTS, 30.0)
    conftest.press_pad(page, 1)
    conftest.poll(lambda: not conftest.find_text(page, conftest.CLASSEMENTS),
                  "the panel to close on the east button", 20.0)
    conftest.press_pad(page, 3)
    conftest.wait_text(page, conftest.NOTEBOOK_TITLE, 30.0)
    conftest.press_pad(page, 1)
    conftest.poll(lambda: not conftest.find_text(page, conftest.NOTEBOOK_TITLE),
                  "the notebook to close on the east button", 20.0)
    conftest.depart(page, "orchard")
    conftest.press_pad(page, 2)
    conftest.wait_text(page, conftest.KEEPER_LINES["orchard"], 30.0)


def test_touch_screen_shows_pass_through_controls(ui_page):
    """A sideways touch screen carries its own controls without covering the world."""
    page = ui_page(*conftest.LANDSCAPE_PHONE, has_touch=True, is_mobile=True)
    conftest.enter_world(page)
    size = page.viewport_size
    for label in conftest.TOUCH_BUTTONS:
        control = conftest.visible_button(page, label, 30.0)
        box = control.bounding_box()
        assert box["width"] >= conftest.TOUCH_MIN and box["height"] >= conftest.TOUCH_MIN, (
            f"the {label!r} control is {box['width']:.0f} by {box['height']:.0f}, below "
            f"the pinned {conftest.TOUCH_MIN} CSS pixels")
        assert box["x"] > size["width"] * 0.5, (
            f"the {label!r} control sits at x {box['x']:.0f} on a {size['width']} "
            f"screen, expected the lower right")
        assert conftest.hit_inside(page, control, *conftest.box_center(box)), (
            f"a touch on the glyph inside {label!r} does not count for the control")
    before = conftest.visible_button(page, conftest.TOUCH_BUTTONS[0], 20.0).bounding_box()
    page.evaluate("() => { document.documentElement.style.fontSize = '38px'; }")
    conftest.hold(1.0)
    after = conftest.visible_button(page, conftest.TOUCH_BUTTONS[0], 20.0).bounding_box()
    assert abs(after["width"] - before["width"]) <= 2, (
        f"the touch control grew from {before['width']:.0f} to {after['width']:.0f} with "
        f"the interface, and it never scales with the root")
    assert conftest.hit_is_world(page, size["width"] * 0.5, size["height"] * 0.3), (
        "the touch pad swallows touches meant for the world")


def test_rotate_prompt_covers_the_upright_phone(ui_page):
    """A phone held upright is asked to rotate, above every other layer."""
    upright = ui_page(*conftest.PORTRAIT)
    conftest.open_site(upright)
    prompt = conftest.wait_text(upright, conftest.ROTATE_PROMPT, 60.0)
    size = upright.viewport_size
    assert prompt["width"] >= size["width"] * 0.9 and prompt["height"] >= size["height"] * 0.5, (
        f"the rotate prompt covers {prompt['width']:.0f} by {prompt['height']:.0f} of a "
        f"{size['width']} by {size['height']} screen")
    assert not conftest.hit_is_world(upright, size["width"] / 2, size["height"] / 2), (
        "the rotate prompt sits under the world instead of above every layer")
    sideways = ui_page(*conftest.LANDSCAPE_PHONE)
    conftest.open_site(sideways)
    conftest.wait_home(sideways)
    assert not conftest.find_text(sideways, conftest.ROTATE_PROMPT), (
        "the same phone held sideways is still asked to rotate")


def test_narrow_screens_keep_every_control_reachable(ui_page):
    """Nothing overflows sideways and the contact link moves to the lower corner."""
    page = ui_page(*conftest.LANDSCAPE_PHONE)
    conftest.open_site(page)
    voyager = conftest.wait_home(page)
    overflow = page.evaluate(
        "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    assert overflow <= 1, f"the page overflows sideways by {overflow}px"
    size = page.viewport_size
    for locator in (voyager, page.get_by_role("link", name=re.compile(conftest.CONTACT_LABEL)).first):
        box = locator.bounding_box()
        assert box is not None, "a control on the home screen has no box at all"
        assert box["x"] >= -1 and box["x"] + box["width"] <= size["width"] + 1, (
            f"a control runs from {box['x']:.0f} to {box['x'] + box['width']:.0f} on a "
            f"{size['width']} screen")
    contact = page.get_by_role("link", name=re.compile(conftest.CONTACT_LABEL)).first.bounding_box()
    assert contact["x"] > size["width"] * 0.5 and contact["y"] > size["height"] * 0.55, (
        f"below the breakpoint the contact link sits at {contact!r}, expected the lower "
        f"right corner")
    tablet = ui_page(*conftest.TABLET_SIDEWAYS)
    conftest.open_site(tablet)
    conftest.wait_home(tablet)
    title = conftest.find_text(tablet, conftest.SITE_TITLE)[0]
    assert title["height"] <= float(title["fontSize"][:-2]) * 1.8, (
        f"the whole title does not fit on one line at "
        f"{conftest.TABLET_SIDEWAYS[0]} wide: {title!r}")


def test_document_holds_one_scheme_under_both_colour_preferences(ui_page):
    """The product keeps one scheme whatever the system asks for."""
    grounds = {}
    for scheme in ("dark", "light"):
        page = ui_page(*conftest.WIDE, color_scheme=scheme)
        conftest.open_site(page)
        conftest.wait_home(page)
        grounds[scheme] = page.evaluate(
            """() => { const body = getComputedStyle(document.body).backgroundColor;
            const root = getComputedStyle(document.documentElement).backgroundColor;
            const text = getComputedStyle(document.body).color;
            return [body, root, text]; }""")
    assert grounds["dark"] == grounds["light"], (
        f"the product answers a light preference with {grounds['light']!r} and a dark "
        f"one with {grounds['dark']!r}, and it has one scheme")


def test_world_load_fetches_no_media_no_other_host_and_sets_no_cookie(page):
    """The world is generated: no media file, no other host, no cookie, no analytics."""
    seen = []
    page.on("response", lambda response: seen.append(
        (response.url, response.headers.get("content-type", ""), response.status)))
    conftest.enter_world(page)
    conftest.open_menu(page)
    page.keyboard.press("Escape")
    origin = appclient.app_url()
    offsite = [url for url, _type, _status in seen
               if not url.startswith((origin, "data:", "blob:", "about:"))]
    assert offsite == [], f"the page fetched from another host: {offsite[:5]!r}"
    media = [(url, kind) for url, kind, status in seen
             if status == 200 and (kind.startswith(conftest.MEDIA_TYPES) or
                                   url.split("?")[0].lower().endswith(conftest.MEDIA_SUFFIXES))]
    assert media == [], f"the page downloaded media files: {media[:5]!r}"
    fonts = [url for url, kind, _status in seen
             if kind.startswith("font/") or url.split("?")[0].lower().endswith(conftest.FONT_SUFFIXES)]
    bad_fonts = [url for url in fonts if not url.split("?")[0].lower().endswith(".woff2")]
    assert bad_fonts == [], f"fonts arrived outside WOFF2: {bad_fonts!r}"
    wasm = [(url, kind) for url, kind, _status in seen
            if url.split("?")[0].lower().endswith(".wasm")]
    for url, kind in wasm:
        assert kind.startswith("application/wasm"), (
            f"{url} is served as {kind!r}, expected application/wasm")
    assert page.context.cookies() == [], (
        f"the page set cookies: {page.context.cookies()!r}")
    calls = {url.split("?")[0][len(origin):] for url, _kind, _status in seen
             if url.startswith(origin + "/api/")}
    for call in calls:
        assert call.startswith(("/api/games", "/api/runs", "/api/entries",
                                "/api/leaderboards", "/api/health")), (
            f"the world called {call!r}, and walking stays in the visitor's own browser")
    assert page.evaluate(
        "() => navigator.serviceWorker ? navigator.serviceWorker.controller === null : true"), (
        "a service worker took control, and the product has no offline build")


def test_open_board_never_polls_and_the_player_id_survives_a_reload(page):
    """One player identity is reused, and an open board waits for the stream."""
    starts = []
    reads = []
    page.on("request", lambda request: starts.append(request.post_data)
            if request.method == "POST" and request.url.endswith("/api/runs") else None)
    page.on("request", lambda request: reads.append(request.url)
            if "/api/leaderboards/" in request.url and request.method == "GET" else None)
    conftest.enter_world(page)
    conftest.begin_run(page, "orchard")
    first = conftest.poll(lambda: starts and starts[0], "the run start body", 30.0)
    player = json.loads(first).get("player_id")
    assert isinstance(player, str) and 8 <= len(player) <= 64, (
        f"the browser sent player_id {player!r}, outside 8 to 64 characters")
    assert re.fullmatch(r"[A-Za-z0-9-]+", player), (
        f"the player_id {player!r} carries characters outside letters, digits and hyphens")
    conftest.end_run_now(page)
    conftest.open_board(page, "orchard")
    before = len(reads)
    conftest.hold(12.0)
    assert len(reads) == before, (
        f"the open board asked the server {len(reads) - before} more times on a timer")
    conftest.enter_world(page)
    conftest.begin_run(page, "orchard")
    second = conftest.poll(lambda: len(starts) > 1 and starts[-1],
                           "the second run start body", 30.0)
    assert json.loads(second).get("player_id") == player, (
        f"the browser sent {json.loads(second).get('player_id')!r} after a reload, "
        f"expected the kept {player!r}")


def test_browser_without_3d_keeps_every_interface_layer(browser_page):
    """A browser that cannot draw the world still carries the whole interface."""
    page = browser_page(*conftest.WIDE)
    conftest.open_site(page)
    conftest.wait_text(page, conftest.NO_3D_NOTICE, conftest.WORLD_TIMEOUT)
    conftest.wait_home(page).click()
    conftest.wait_text(page, conftest.WELCOME, 60.0)
    conftest.visible_button(page, conftest.VOYAGER, 60.0).click()
    conftest.visible_button(page, conftest.MENU_NAME, conftest.WORLD_TIMEOUT).click()
    conftest.wait_text(page, conftest.CLASSEMENTS, 30.0)
    assert conftest.find_text(page, conftest.NO_3D_NOTICE), (
        "the notice went away although the world still cannot be drawn")


def test_layout_carries_no_menu_bar_header_or_footer(page):
    """The frame around the world is the interface, with no site furniture."""
    conftest.enter_world(page)
    furniture = page.evaluate(
        """() => ['header', 'footer', 'nav'].flatMap((tag) =>
        [...document.querySelectorAll(tag)].filter((el) => {
          const r = el.getBoundingClientRect();
          return r.width > 2 && r.height > 2;
        }).map((el) => tag))""")
    assert furniture == [], (
        f"the world carries site furniture: {furniture!r}")
    assert page.evaluate("() => document.body.scrollHeight <= window.innerHeight + 2"), (
        "the page scrolls like a document instead of holding one frame")
