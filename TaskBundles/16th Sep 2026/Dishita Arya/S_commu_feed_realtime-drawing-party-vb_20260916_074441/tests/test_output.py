"""The one Doodlerush pytest module. Every assertion is black box: HTTP, the
declared datastore and a real rendered page. Nothing here reads the application's
source."""

from __future__ import annotations

import concurrent.futures
import contextlib

from conftest import (
    CONFLICT_STATUSES,
    CONTRAST_RATIO,
    DENIAL_STATUSES,
    FOOTER_LINKS,
    GUESS_MAX_CHARS,
    LANGUAGE,
    MODE_NORMAL,
    MODERATOR_EMAIL,
    NARROW_VIEWPORT,
    NOSNIFF_HEADER,
    NOT_FOUND_STATUSES,
    OUTCOME_CHAT,
    OUTCOME_CLOSE,
    OUTCOME_CORRECT,
    OUTCOME_FIELD,
    PASSWORD,
    PLAYER2_EMAIL,
    PLAYER3_EMAIL,
    PLAYER_EMAIL,
    PLAYER_NAME,
    PLAYERS_MAX,
    PRIVACY_PATH,
    PUBLIC_ROUTES,
    REFUSAL_STATUSES,
    ROOM_CAP,
    ROOM_CODE,
    ROOM_CODE_LENGTH,
    ROOM_NAME,
    ROUNDS_DEFAULT,
    SEAT_FIELD,
    SEAT_HEADER,
    STATE_CHOOSING,
    STATE_DRAWING,
    SUCCESS_STATUSES,
    TERMS_PATH,
    TRANSPORT_HEADER,
    TURN_SECONDS_MAX,
    WORD_CHOICES_DEFAULT,
    Session,
    body_of,
    describe,
    field,
    flatten,
    poll_until,
    probe_name,
    rows_of,
    seat_in,
    settle,
    site_base,
    stroke,
    unique_suffix,
)

import appclient
import httpx


def _site(path: str) -> httpx.Response:
    """A plain GET against the public origin rather than the API prefix."""
    with httpx.Client(base_url=site_base(), timeout=30.0,
                      follow_redirects=True) as client:
        return client.get(path)


def _state(session: Session, code: str) -> dict:
    response = session.state(code)
    assert response.status_code in SUCCESS_STATUSES, (
        f"room state for {code!r}: expected a success, got {describe(response)}")
    return body_of(response) or {}


def _open_room(host: Session, cap: int = 4, guests: int = 2,
               rounds: int = ROUNDS_DEFAULT) -> tuple[str, list[Session]]:
    """Create a private room, seat the creator, then seat `guests` strangers."""
    created = host.create_room(f"Probe Room {unique_suffix()[:6]}", {
        "max_players": cap,
        "rounds": rounds,
        "turn_seconds": TURN_SECONDS_MAX,
        "word_choices": WORD_CHOICES_DEFAULT,
        "hints": 0,
        "word_mode": MODE_NORMAL,
    })
    assert created.status_code in SUCCESS_STATUSES, (
        f"room creation: expected a success, got {describe(created)}")
    payload = body_of(created) or {}
    code = str(field(payload, "code", default=""))
    assert len(code) == ROOM_CODE_LENGTH, (
        f"a created room code is {ROOM_CODE_LENGTH} characters, got {code!r}: "
        f"{describe(created)}")

    joined = host.join(code, PLAYER_NAME)
    assert joined.status_code in SUCCESS_STATUSES, (
        f"the creator joining {code!r}: expected a success, got {describe(joined)}")
    host_body = body_of(joined) or {}
    host.seat = str(field(host_body, SEAT_FIELD, "seat", "token", default=""))
    host.player_id = field(host_body, "player_id", "id", "seat_id")

    sessions = [host]
    for _ in range(guests):
        sessions.append(seat_in(code, probe_name()))
    return code, sessions


def _drawer_of(sessions: list[Session], code: str) -> tuple[Session, dict]:
    snapshot = _state(sessions[0], code)
    drawer_id = field(snapshot, "drawer", "drawer_id")
    for session in sessions:
        if drawer_id is not None and str(session.player_id) == str(drawer_id):
            return session, snapshot
    raise AssertionError(
        f"the room names drawer {drawer_id!r}, which is none of the seated "
        f"players {[s.player_id for s in sessions]!r}")


def _start_turn(sessions: list[Session], code: str) -> tuple[Session, str]:
    """Take the room from its current state into a live turn, and read the word."""
    poll_until(lambda: field(_state(sessions[0], code), "state")
               in (STATE_CHOOSING, STATE_DRAWING))
    drawer, snapshot = _drawer_of(sessions, code)
    if field(snapshot, "state") == STATE_CHOOSING:
        chosen = drawer.choose_word(0, code)
        assert chosen.status_code in SUCCESS_STATUSES, (
            f"the drawer choosing a word: expected a success, got {describe(chosen)}")
    poll_until(lambda: field(_state(drawer, code), "state") == STATE_DRAWING)
    live = _state(drawer, code)
    assert field(live, "state") == STATE_DRAWING, (
        f"the room should be {STATE_DRAWING!r} once a word is chosen, it is "
        f"{field(live, 'state')!r}")
    word = field(live, "word")
    assert word, ("the drawer's own snapshot must carry the word it is drawing, "
                  f"and carries {live!r}")
    return drawer, str(word)


def _run_game(host: Session, cap: int = 4, guests: int = 2) -> tuple[str, list[Session]]:
    code, sessions = _open_room(host, cap=cap, guests=guests)
    started = host.start(code)
    assert started.status_code in SUCCESS_STATUSES, (
        f"the host starting the game: expected a success, got {describe(started)}")
    return code, sessions


def _everybody_guesses(sessions: list[Session], drawer: Session, word: str,
                       code: str) -> list[httpx.Response]:
    return [s.guess(word, code) for s in sessions if s is not drawer]


def test_health_endpoint_reports_ready(visitor):
    """The app answers its health route once it is ready to serve."""
    response = visitor.get("/health")
    assert response.status_code == 200, (
        f"the health route must answer 200 once the app is ready, got "
        f"{describe(response)}")


def test_seeded_rows_are_present_for_every_account(store):
    """Every seeded account, the seeded private room and its cap are real rows."""
    for email in (PLAYER_EMAIL, PLAYER2_EMAIL, PLAYER3_EMAIL, MODERATOR_EMAIL):
        assert store.account(email) is not None, (
            f"the seeded account {email!r} is not a row in the declared datastore")
    room = store.room(ROOM_CODE)
    assert room is not None, (
        f"the seeded room {ROOM_NAME!r} with code {ROOM_CODE!r} is not a row in "
        f"the declared datastore")
    cap = field(room, "cap", "max_players", "player_cap")
    assert int(cap) == ROOM_CAP, (
        f"{ROOM_NAME!r} carries a cap of {ROOM_CAP}, the stored row says {cap!r}")


def test_private_room_is_created_and_joined_by_its_code(owner):
    """A created private room is reachable by its code and seats a stranger."""
    code, sessions = _open_room(owner, cap=4, guests=1)
    summary = sessions[0].room(code)
    assert summary.status_code in SUCCESS_STATUSES, (
        f"a room summary read with its own code: expected a success, got "
        f"{describe(summary)}")
    body = body_of(summary) or {}
    assert str(field(body, "code")) == code, (
        f"the summary for {code!r} names a different room: {describe(summary)}")
    snapshot = _state(sessions[1], code)
    players = rows_of(field(snapshot, "players", default=[]))
    assert len(players) == 2, (
        f"a room joined by its creator and one stranger holds two players, the "
        f"snapshot holds {len(players)}: {snapshot!r}")


def test_word_reaches_the_drawer_and_no_other_seat(owner):
    """The word is in the drawer's snapshot and in nothing any other seat receives."""
    code, sessions = _run_game(owner, cap=4, guests=2)
    drawer, word = _start_turn(sessions, code)
    needle = word.lower()

    for session in sessions:
        if session is drawer:
            continue
        snapshot = _state(session, code)
        assert needle not in flatten(snapshot).lower(), (
            f"the snapshot sent to a player who is not the drawer carries the "
            f"word {word!r}: {snapshot!r}")
        assert field(snapshot, "word") is None, (
            f"a non-drawer snapshot must omit the word field entirely, it carries "
            f"{field(snapshot, 'word')!r}")
        assert field(snapshot, "word_mask") is not None, (
            f"a non-drawer snapshot must carry the mask, it carries {snapshot!r}")

        summary = session.room(code)
        assert needle not in summary.text.lower(), (
            f"the room summary carries the word {word!r}: {describe(summary)}")

        stream = _read_events(session, code)
        assert needle not in stream.lower(), (
            f"the event stream a non-drawer holds carries the word {word!r}: "
            f"{stream[:400]!r}")


def _read_events(session: Session, code: str, budget: float = 3.0) -> str:
    """A bounded read of the live stream, so a held-open connection cannot hang."""
    collected: list[str] = []
    headers = {SEAT_HEADER: session.seat} if session.seat else {}
    with contextlib.suppress(httpx.HTTPError, RuntimeError):
        with httpx.Client(base_url=appclient.api_base(), timeout=budget) as client:
            with client.stream("GET", f"/rooms/{code}/events",
                               headers=headers) as response:
                for chunk in response.iter_text():
                    collected.append(chunk)
                    if sum(len(c) for c in collected) > 16000:
                        break
    return "".join(collected)


def test_correct_guess_is_announced_without_the_text(owner):
    """A correct guess tells the room who guessed and never what was typed."""
    code, sessions = _run_game(owner, cap=4, guests=2)
    drawer, word = _start_turn(sessions, code)
    guesser = next(s for s in sessions if s is not drawer)

    answered = guesser.guess(word, code)
    assert answered.status_code in SUCCESS_STATUSES, (
        f"a correct guess: expected a success, got {describe(answered)}")
    outcome = field(body_of(answered) or {}, OUTCOME_FIELD)
    assert outcome == OUTCOME_CORRECT, (
        f"a guess equal to the word answers {OUTCOME_CORRECT!r}, it answered "
        f"{outcome!r}: {describe(answered)}")

    watcher = next(s for s in sessions if s is not drawer and s is not guesser)
    snapshot = _state(watcher, code)
    chat = flatten(field(snapshot, "chat", default=[])).lower()
    assert word.lower() not in chat, (
        f"the chat a still-guessing player reads repeats the word {word!r}: "
        f"{field(snapshot, 'chat')!r}")


def test_near_miss_reaches_the_guesser_alone(owner):
    """A near miss answers the guesser and leaves the rest of the room unaware."""
    code, sessions = _run_game(owner, cap=4, guests=2)
    drawer, word = _start_turn(sessions, code)
    if len(word) < 5:
        settle()
    guesser = next(s for s in sessions if s is not drawer)
    near = word[:-1] + ("x" if not word.endswith("x") else "y")

    answered = guesser.guess(near, code)
    assert answered.status_code in SUCCESS_STATUSES, (
        f"a near miss: expected a success, got {describe(answered)}")
    outcome = field(body_of(answered) or {}, OUTCOME_FIELD)
    assert outcome in (OUTCOME_CLOSE, OUTCOME_CHAT), (
        f"a guess one letter from the word answers {OUTCOME_CLOSE!r} or "
        f"{OUTCOME_CHAT!r}, it answered {outcome!r}: {describe(answered)}")
    assert near.lower() not in flatten(body_of(answered)).lower() or \
        outcome == OUTCOME_CHAT, (
        f"a near-miss reply must not repeat the guess back: {describe(answered)}")

    if outcome == OUTCOME_CLOSE:
        watcher = next(s for s in sessions if s is not drawer and s is not guesser)
        seen = flatten(_state(watcher, code)).lower()
        assert near.lower() not in seen, (
            f"a near miss reached a player other than the guesser: {seen[:400]!r}")


def test_turn_ends_once_every_non_drawer_has_guessed(owner):
    """The turn leaves the drawing state the moment the last guesser gets it."""
    code, sessions = _run_game(owner, cap=4, guests=2)
    drawer, word = _start_turn(sessions, code)
    for response in _everybody_guesses(sessions, drawer, word, code):
        assert response.status_code in SUCCESS_STATUSES, (
            f"a correct guess: expected a success, got {describe(response)}")
    ended = poll_until(
        lambda: field(_state(drawer, code), "state") != STATE_DRAWING, budget=10.0)
    assert ended, (
        "once every player who is not the drawer has guessed, the turn ends at "
        f"once; the room is still {field(_state(drawer, code), 'state')!r}")


def test_drawer_is_awarded_when_the_room_guesses(owner):
    """The drawer's standing rises when the room works the word out."""
    code, sessions = _run_game(owner, cap=4, guests=2)
    drawer, word = _start_turn(sessions, code)
    before = _award_of(_state(drawer, code), drawer)
    for response in _everybody_guesses(sessions, drawer, word, code):
        assert response.status_code in SUCCESS_STATUSES, (
            f"a correct guess: expected a success, got {describe(response)}")
    poll_until(lambda: field(_state(drawer, code), "state") != STATE_DRAWING,
               budget=10.0)
    settle()
    after = _award_of(_state(drawer, code), drawer)
    assert after > before, (
        f"the drawer is awarded in proportion to how many players guessed; the "
        f"drawer's standing moved from {before} to {after}")


def _award_of(snapshot: dict, session: Session) -> int:
    for row in rows_of(field(snapshot, "players", default=[])):
        if str(field(row, "id", "player_id")) == str(session.player_id):
            return int(field(row, "score", "award", "total", default=0) or 0)
    return 0


def test_every_player_draws_the_same_number_of_times(owner):
    """A round gives one turn to each player, in a fixed order."""
    code, sessions = _run_game(owner, cap=4, guests=2)
    drawers: list[str] = []
    for _ in range(len(sessions)):
        drawer, word = _start_turn(sessions, code)
        drawers.append(str(drawer.player_id))
        for response in _everybody_guesses(sessions, drawer, word, code):
            assert response.status_code in SUCCESS_STATUSES, (
                f"a correct guess: expected a success, got {describe(response)}")
        poll_until(lambda: field(_state(sessions[0], code), "state")
                   in (STATE_CHOOSING, STATE_DRAWING), budget=20.0)
    assert len(set(drawers)) == len(sessions), (
        f"a round is one turn per player, so {len(sessions)} turns must have "
        f"{len(sessions)} distinct drawers; they were {drawers!r}")


def test_repeated_guess_is_awarded_once(owner):
    """The same correct guess sent four times moves the standing once."""
    code, sessions = _run_game(owner, cap=4, guests=2)
    drawer, word = _start_turn(sessions, code)
    guesser = next(s for s in sessions if s is not drawer)

    first = guesser.guess(word, code)
    assert first.status_code in SUCCESS_STATUSES, (
        f"a correct guess: expected a success, got {describe(first)}")
    settle()
    awarded = _award_of(_state(guesser, code), guesser)

    for _ in range(3):
        again = guesser.guess(word, code)
        assert again.status_code in SUCCESS_STATUSES + REFUSAL_STATUSES, (
            f"a repeated guess is either a no-op or a refusal, got {describe(again)}")
    settle()
    assert _award_of(_state(guesser, code), guesser) == awarded, (
        "a guess repeated four times is awarded once per player per turn; the "
        "standing moved a second time")


def test_reconnect_restores_the_seat_and_its_guessed_mark(owner):
    """Rejoining on a held seat token returns the same seat, still marked correct."""
    code, sessions = _run_game(owner, cap=4, guests=2)
    drawer, word = _start_turn(sessions, code)
    guesser = next(s for s in sessions if s is not drawer)
    answered = guesser.guess(word, code)
    assert answered.status_code in SUCCESS_STATUSES, (
        f"a correct guess: expected a success, got {describe(answered)}")
    settle()
    before = _award_of(_state(guesser, code), guesser)

    returning = Session(seat=guesser.seat)
    rejoined = returning.join(code, probe_name(), seat=guesser.seat)
    assert rejoined.status_code in SUCCESS_STATUSES, (
        f"rejoining on a held seat token: expected a success, got "
        f"{describe(rejoined)}")
    payload = body_of(rejoined) or {}
    returning.seat = str(field(payload, SEAT_FIELD, "seat", "token",
                               default=guesser.seat))
    returning.player_id = field(payload, "player_id", "id", "seat_id",
                                default=guesser.player_id)
    assert str(returning.player_id) == str(guesser.player_id), (
        "a reconnection restores the same seat rather than creating a second one; "
        f"the seat moved from {guesser.player_id!r} to {returning.player_id!r}")

    snapshot = _state(returning, code)
    players = rows_of(field(snapshot, "players", default=[]))
    assert len(players) == len(sessions), (
        f"a reconnection must not add a player; the room now holds "
        f"{len(players)} against {len(sessions)} seats")
    mine = next((row for row in players
                 if str(field(row, "id", "player_id")) == str(guesser.player_id)), {})
    assert field(mine, "guessed", "has_guessed", "guessed_this_turn") is True, (
        f"a returning player who had already guessed comes back still marked "
        f"correct, the row reads {mine!r}")
    assert _award_of(snapshot, returning) == before, (
        "a reconnection restores the standing the seat already held")

    repeat = returning.guess(word, code)
    if repeat.status_code in SUCCESS_STATUSES:
        settle()
        assert _award_of(_state(returning, code), returning) == before, (
            "a returning player who already guessed cannot be awarded a second time")


def test_late_joiner_receives_the_stroke_buffer(owner):
    """A player seated mid-turn is handed the drawing as it stands, in one go."""
    code, sessions = _run_game(owner, cap=4, guests=1)
    drawer, _word = _start_turn(sessions, code)
    sent = drawer.strokes([stroke(1), stroke(2), stroke(3)], code)
    assert sent.status_code in SUCCESS_STATUSES, (
        f"the drawer sending a stroke batch: expected a success, got {describe(sent)}")
    settle()

    latecomer = seat_in(code, probe_name())
    snapshot = _state(latecomer, code)
    canvas = rows_of(field(snapshot, "canvas", default=[]))
    assert len(canvas) >= 3, (
        f"a player joining mid-turn receives the ordered stroke list for the "
        f"current turn, the snapshot carries {len(canvas)} strokes: {snapshot!r}")


def test_no_table_stores_the_current_word(owner, store):
    """While a turn is live, the word is in memory and in no table."""
    code, sessions = _run_game(owner, cap=4, guests=2)
    _drawer, word = _start_turn(sessions, code)
    needle = word.lower()
    for table in store.table_names():
        if table == "words":
            continue
        for column in store.text_columns(table):
            found = store.query(
                f'SELECT 1 FROM "{table}" WHERE lower("{column}") = %s LIMIT 1',
                (needle,))
            assert not found, (
                f"the current word of a live room is held in memory and in no "
                f"table; {table}.{column} holds {word!r}")


def test_concurrent_join_fills_the_last_seat_at_most_once(owner, store):
    """Two strangers racing for one free seat produce one join and one redirect."""
    code, sessions = _open_room(owner, cap=3, guests=1)

    def take_seat() -> httpx.Response:
        return Session().join(code, probe_name())

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        first, second = [f.result() for f in
                         [pool.submit(take_seat), pool.submit(take_seat)]]

    seated = [r for r in (first, second) if r.status_code in SUCCESS_STATUSES
              and field(body_of(r) or {}, SEAT_FIELD, "seat", "token")]
    assert len(seated) == 1, (
        f"a room with one free seat admits exactly one of two simultaneous "
        f"joiners; {len(seated)} were seated. first={describe(first)} "
        f"second={describe(second)}")
    other = first if second in seated else second
    assert other.status_code in SUCCESS_STATUSES + CONFLICT_STATUSES, (
        f"the join that loses the race is offered another room or refused, never "
        f"a server error: {describe(other)}")

    snapshot = _state(sessions[0], code)
    players = rows_of(field(snapshot, "players", default=[]))
    assert len(players) <= 3, (
        f"the room cap is 3 and the room holds {len(players)} players: {snapshot!r}")


def test_private_room_state_is_denied_without_a_seat(owner, second_player):
    """A signed-in player with no seat learns nothing about a private room."""
    code, sessions = _open_room(owner, cap=4, guests=1)
    room_name = field(body_of(sessions[0].room(code)) or {}, "name")

    response = second_player.state(code)
    assert response.status_code in DENIAL_STATUSES, (
        f"a caller holding no seat token for {code!r} is denied its state, got "
        f"{describe(response)}")
    body = response.text.lower()
    assert "player" not in body or "seat" not in body, (
        f"a denied room-state response carries no player list: {describe(response)}")
    if room_name:
        assert str(room_name).lower() not in body, (
            f"a denied room-state response names the room {room_name!r}: "
            f"{describe(response)}")

    anonymous = Session().state(code)
    assert anonymous.status_code in DENIAL_STATUSES, (
        f"an anonymous caller is denied a private room's state, got "
        f"{describe(anonymous)}")


def test_stroke_from_a_non_drawer_is_rejected(owner):
    """Only the current drawer may put marks on the canvas."""
    code, sessions = _run_game(owner, cap=4, guests=2)
    drawer, _word = _start_turn(sessions, code)
    intruder = next(s for s in sessions if s is not drawer)

    before = len(rows_of(field(_state(drawer, code), "canvas", default=[])))
    response = intruder.strokes([stroke(900)], code)
    assert response.status_code in SUCCESS_STATUSES + REFUSAL_STATUSES, (
        f"a stroke from a player who is not the drawer is refused, never a "
        f"server error: {describe(response)}")
    settle()
    after = rows_of(field(_state(drawer, code), "canvas", default=[]))
    assert len(after) == before, (
        f"a stroke from a player who is not the drawer changes nothing; the "
        f"canvas moved from {before} strokes to {len(after)}")

    operation = intruder.canvas_op("clear", 901, code)
    assert operation.status_code in SUCCESS_STATUSES + REFUSAL_STATUSES, (
        f"a canvas operation from a non-drawer is refused: {describe(operation)}")
    settle()
    assert len(rows_of(field(_state(drawer, code), "canvas", default=[]))) == before, (
        "a canvas operation from a player who is not the drawer changes nothing")


def test_report_queue_is_denied_to_a_player(second_player, moderator):
    """The report queue answers a moderator and refuses everybody else."""
    refused = second_player.reports()
    assert refused.status_code in DENIAL_STATUSES, (
        f"a signed-in player is denied the report queue, got {describe(refused)}")
    assert "report" not in refused.text.lower() or refused.status_code != 200, (
        f"a refused report-queue request carries no queue: {describe(refused)}")

    allowed = moderator.reports()
    assert allowed.status_code in SUCCESS_STATUSES, (
        f"a moderator reads the report queue, got {describe(allowed)}")
    assert isinstance(body_of(allowed), list), (
        f"the report queue is a top-level JSON array, got {describe(allowed)}")

    anonymous = Session().reports()
    assert anonymous.status_code in DENIAL_STATUSES, (
        f"an anonymous caller is denied the report queue, got {describe(anonymous)}")


def test_unauthenticated_request_is_denied_at_the_api(visitor, store):
    """A call with no session is refused before anything is written."""
    before = len(store.rows("rooms", limit=2000))
    response = visitor.post("/rooms", {"name": "Uninvited", "language": LANGUAGE,
                                       "settings": {}})
    assert response.status_code in DENIAL_STATUSES + (400, 422), (
        f"creating a room with no session is refused, got {describe(response)}")
    settle()
    assert len(store.rows("rooms", limit=2000)) == before, (
        "a refused request writes nothing")

    me = visitor.get("/me")
    assert me.status_code in DENIAL_STATUSES, (
        f"the account route with no session is denied, got {describe(me)}")


def test_settings_change_from_a_non_host_is_rejected(owner):
    """Only the host changes a room's settings, and only before it starts."""
    code, sessions = _open_room(owner, cap=4, guests=1)
    stranger = sessions[1]

    refused = stranger.settings({"rounds": 9}, code)
    assert refused.status_code in REFUSAL_STATUSES, (
        f"a settings change from a player who is not the host is rejected, got "
        f"{describe(refused)}")
    snapshot = _state(sessions[0], code)
    rounds = field(field(snapshot, "settings", default={}) or {}, "rounds")
    assert rounds != 9, (
        f"a rejected settings change leaves the settings untouched, rounds is "
        f"{rounds!r}")

    started = sessions[0].start(code)
    assert started.status_code in SUCCESS_STATUSES, (
        f"the host starting the game: expected a success, got {describe(started)}")
    late = sessions[0].settings({"rounds": 7}, code)
    assert late.status_code in REFUSAL_STATUSES, (
        f"a settings change after the game has started is rejected, got "
        f"{describe(late)}")


def test_out_of_range_settings_change_is_refused(owner):
    """Every setting is validated server-side against the range the brief pins."""
    code, sessions = _open_room(owner, cap=4, guests=0)
    for patch in ({"max_players": PLAYERS_MAX + 1}, {"max_players": 1},
                  {"turn_seconds": 999999}, {"turn_seconds": 5},
                  {"rounds": 99}, {"word_choices": 9}, {"hints": 9},
                  {"word_mode": "sideways"}):
        response = sessions[0].settings(patch, code)
        assert response.status_code in REFUSAL_STATUSES, (
            f"the out-of-range settings patch {patch!r} is refused, got "
            f"{describe(response)}")
    snapshot = _state(sessions[0], code)
    settings = field(snapshot, "settings", default={}) or {}
    assert int(field(settings, "max_players", "players", default=4)) <= PLAYERS_MAX, (
        f"a refused settings patch leaves the stored settings within range: "
        f"{settings!r}")


def test_guess_beyond_the_length_cap_is_refused(owner):
    """A guess longer than the cap is refused and never compared."""
    code, sessions = _run_game(owner, cap=4, guests=2)
    drawer, _word = _start_turn(sessions, code)
    guesser = next(s for s in sessions if s is not drawer)

    response = guesser.guess("d" * (GUESS_MAX_CHARS + 50), code)
    assert response.status_code in REFUSAL_STATUSES, (
        f"a guess beyond {GUESS_MAX_CHARS} characters is refused, got "
        f"{describe(response)}")

    empty_name = Session().join(code, "")
    assert empty_name.status_code in REFUSAL_STATUSES, (
        f"a display name outside the pinned length band is refused, got "
        f"{describe(empty_name)}")
    too_long = Session().join(code, "n" * 40)
    assert too_long.status_code in REFUSAL_STATUSES, (
        f"a display name beyond the pinned length band is refused, got "
        f"{describe(too_long)}")


def test_unknown_address_answers_not_found():
    """An address the product does not serve renders its own not-found page."""
    response = _site(f"/room/NOSUCH{unique_suffix()[:2].upper()}")
    assert response.status_code in NOT_FOUND_STATUSES, (
        f"a room code that is not live answers not-found, got {describe(response)}")
    body = response.text.lower()
    assert "cannot get" not in body, (
        "the not-found page is the product's own page, not a bare framework "
        f"string: {response.text[:300]!r}")
    assert "doodlerush" in body, (
        f"the not-found page carries the product's own chrome: {response.text[:300]!r}")


def test_security_headers_are_present_on_every_public_route():
    """Every response carries the strict transport and nosniff policies."""
    for path in PUBLIC_ROUTES:
        response = _site(path)
        headers = {k.lower(): v for k, v in response.headers.items()}
        assert TRANSPORT_HEADER in headers, (
            f"{path!r} answers without a strict transport policy header: "
            f"{sorted(headers)!r}")
        assert headers.get(NOSNIFF_HEADER, "").lower() == "nosniff", (
            f"{path!r} answers without a nosniff content-type policy: "
            f"{headers.get(NOSNIFF_HEADER)!r}")

    body = _site("/").text.lower()
    for secret in (PASSWORD.lower(), "database_url", "postgresql://"):
        assert secret not in body, (
            f"the landing document carries {secret!r}, which the browser must "
            f"never download")


def test_privacy_page_is_reachable_from_the_footer(page):
    """The footer of the landing route reaches a privacy page that says what is kept."""
    page.goto(site_base() + "/", wait_until="domcontentloaded")
    for label in FOOTER_LINKS:
        assert page.get_by_text(label, exact=False).count() > 0, (
            f"the footer carries the link {label!r}, and the landing route shows "
            f"no such text")
    page.goto(site_base() + PRIVACY_PATH, wait_until="domcontentloaded")
    text = page.locator("body").inner_text().lower()
    assert "store" in text or "keep" in text or "retain" in text, (
        f"the privacy page states what the product stores and for how long, it "
        f"reads {text[:300]!r}")
    page.goto(site_base() + TERMS_PATH, wait_until="domcontentloaded")
    assert "@" in page.locator("body").inner_text(), (
        "the terms page carries a contact address at its head")


def test_every_internal_link_on_a_public_route_resolves(page):
    """Every internal link the product offers reaches a page the app serves."""
    seen: set[str] = set()
    for path in PUBLIC_ROUTES:
        page.goto(site_base() + path, wait_until="domcontentloaded")
        for handle in page.locator("a[href]").all():
            href = handle.get_attribute("href") or ""
            if href.startswith("http") or href.startswith("#") or \
                    href.startswith("mailto:"):
                continue
            seen.add(href if href.startswith("/") else "/" + href)
    assert seen, "the public routes offer no internal link at all"
    for href in sorted(seen):
        response = _site(href)
        assert response.status_code < 400, (
            f"the internal link {href!r} does not resolve: {describe(response)}")


def test_landing_body_text_meets_the_contrast_bar(page):
    """Body text on the landing route clears the contrast ratio the brief pins."""
    page.goto(site_base() + "/", wait_until="domcontentloaded")
    ratio = page.evaluate(
        """() => {
            const lum = (c) => {
                const v = c.map((x) => {
                    const s = x / 255;
                    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
                });
                return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
            };
            const parse = (s) => (s.match(/\\d+(\\.\\d+)?/g) || [0, 0, 0])
                .slice(0, 3).map(Number);
            const walk = (el) => {
                let node = el;
                while (node) {
                    const bg = getComputedStyle(node).backgroundColor;
                    const parts = parse(bg);
                    if (!/rgba\\(.*,\\s*0\\)/.test(bg)) return parts;
                    node = node.parentElement;
                }
                return [255, 255, 255];
            };
            let worst = 99;
            for (const el of document.querySelectorAll('p, li, span, td, label')) {
                const text = (el.textContent || '').trim();
                if (text.length < 12) continue;
                const style = getComputedStyle(el);
                if (style.visibility === 'hidden' || style.display === 'none') continue;
                const fg = lum(parse(style.color));
                const bg = lum(walk(el));
                const hi = Math.max(fg, bg), lo = Math.min(fg, bg);
                worst = Math.min(worst, (hi + 0.05) / (lo + 0.05));
            }
            return worst;
        }"""
    )
    assert ratio >= CONTRAST_RATIO, (
        f"body text and its background must reach a contrast ratio of "
        f"{CONTRAST_RATIO}; the worst pairing on the landing route reads {ratio}")


def test_narrow_viewport_does_not_overflow_sideways(page):
    """At a phone width nothing spills sideways and both actions stay reachable."""
    page.set_viewport_size(NARROW_VIEWPORT)
    page.goto(site_base() + "/", wait_until="domcontentloaded")
    overflow = page.evaluate(
        "() => document.documentElement.scrollWidth - "
        "document.documentElement.clientWidth")
    assert overflow <= 1, (
        f"at a viewport {NARROW_VIEWPORT['width']} wide the document scrolls "
        f"sideways by {overflow} pixels")
    for label in ("Play", "Create Private Room"):
        found = page.get_by_text(label, exact=False)
        assert found.count() > 0, (
            f"the action {label!r} is unreachable at a narrow viewport")
