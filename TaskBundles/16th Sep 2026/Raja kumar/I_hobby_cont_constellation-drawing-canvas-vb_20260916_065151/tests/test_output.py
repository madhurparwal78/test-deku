from __future__ import annotations

import concurrent.futures
import threading

import httpx
from appclient import api_base, client, login
from conftest import (
    BURST_PAIRS,
    POLE_DEC,
    POLE_RA,
    POLE_RADIUS,
    POLE_WINNER,
    SEAM_DEC,
    SEAM_RA,
    SEAM_RADIUS,
    SEAM_WINNER,
    BRIGHT_BOUND,
    BRIGHT_BOUND_ROWS,
    WALK_BOUND,
    WALK_BOUND_ROWS,
    CATALOGUE_ROWS,
    CLIENT_ERRORS,
    DECOY_FIELD,
    DENIALS,
    LANTERN_SEGMENTS,
    MAX_NAME_LENGTH,
    OTHER_STARGAZER_EMAIL,
    PAGE_LIMIT_MAX,
    PICK_BRIGHTEST,
    PICK_DEC,
    PICK_NEAREST,
    PICK_RA,
    PICK_RADIUS,
    TIE_RA,
    TIE_DEC,
    TIE_RADIUS,
    TIE_WINNER,
    TIE_RUNNER_UP,
    EMPTY_RA,
    EMPTY_DEC,
    EMPTY_RADIUS,
    RENDER_CONTENT_TYPE,
    SEEDED_PASSWORD,
    SEEDED_SHARE_TOKEN,
    SEEDED_SKY_COUNT,
    SEGMENT_FROM,
    SEGMENT_TO,
    SKY_CORVUS,
    SKY_HEXAGON,
    SKY_KITE,
    SKY_LANTERN,
    SKY_MONOCEROS,
    STARGAZER_EMAIL,
    UNKNOWN_STAR_ID,
    WORKED_STAR_DEC,
    WORKED_STAR_ID,
    WORKED_STAR_MAGNITUDE,
    WORKED_STAR_RA,
    add_segment,
    collection_page,
    create_sky,
    publish,
    read_sky,
    render,
    require_sky,
    rows_of,
    settle,
    stars_page,
    unique,
)


def _at_once(calls):
    gate = threading.Barrier(len(calls))

    def fire(call):
        gate.wait()
        return call()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(calls)) as pool:
        return list(pool.map(fire, calls))


def _warm(count):
    token = login(STARGAZER_EMAIL, SEEDED_PASSWORD)
    clients = [client(token) for _ in range(count)]
    for c in clients:
        c.get("/health")
    return clients


def _close(clients):
    for c in clients:
        c.close()


def test_health_route_answers_ready(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, so the app never "
        f"reported ready: {response.text[:400]}"
    )


def test_seeded_stargazer_signs_in_and_receives_token(api):
    token = login(STARGAZER_EMAIL, SEEDED_PASSWORD)
    assert token, f"sign-in as {STARGAZER_EMAIL} returned no bearer token"
    with client(token) as c:
        response = c.get("/skies", params={"limit": 1})
        assert response.status_code == 200, (
            f"the token issued to {STARGAZER_EMAIL} was refused at GET /api/skies "
            f"with {response.status_code}: {response.text[:400]}"
        )


def test_a_denied_call_is_a_client_error_not_a_server_fault(anon_client, other_client,
                                                            owner_client):
    target = require_sky(owner_client, SKY_HEXAGON)
    probes = [
        ("anonymous collection read", anon_client.get("/skies", params={"limit": 1})),
        ("anonymous catalogue read", anon_client.get("/stars", params={"limit": 1})),
        ("cross-owner sky read", other_client.get(f"/skies/{target['id']}")),
        ("unknown share token", anon_client.get(f"/shares/{unique('absent')}")),
    ]
    for label, response in probes:
        assert response.status_code < 500, (
            f"the {label} answered {response.status_code}; a refused call is a "
            f"client error, never a server fault: {response.text[:300]}"
        )
        assert response.status_code in CLIENT_ERRORS, (
            f"the {label} answered {response.status_code}, which is neither a "
            f"refusal nor a legitimate success"
        )


def test_stored_password_is_never_readable(backend):
    rows = backend.rows("stargazers", limit=50)
    assert rows, "the stargazers table carries no seeded row"
    for row in rows:
        blob = " ".join(str(v) for v in row.values())
        assert SEEDED_PASSWORD not in blob, (
            f"the stargazers row for {row.get('email')!r} carries the seeded "
            f"password in readable form"
        )


def test_catalogue_reports_full_row_count(owner_client):
    page = stars_page(owner_client, limit=1)
    assert page["total_count"] == CATALOGUE_ROWS, (
        f"GET /api/stars reports total_count {page.get('total_count')!r}, "
        f"but the catalogue holds {CATALOGUE_ROWS} stars"
    )
    assert len(rows_of(page)) == 1, (
        f"GET /api/stars limit=1 returned {len(rows_of(page))} rows under items"
    )


def test_catalogue_row_matches_the_generated_rule(owner_client):
    page = stars_page(owner_client, limit=PAGE_LIMIT_MAX, max_magnitude=WORKED_STAR_MAGNITUDE)
    found = [r for r in rows_of(page) if r.get("star_id") == WORKED_STAR_ID]
    assert found, (
        f"{WORKED_STAR_ID} is absent from the catalogue at or below magnitude "
        f"{WORKED_STAR_MAGNITUDE}, so the generation rule was not followed"
    )
    row = found[0]
    assert abs(float(row["ra_deg"]) - WORKED_STAR_RA) < 0.0005, (
        f"{WORKED_STAR_ID} carries ra_deg {row['ra_deg']!r}, expected {WORKED_STAR_RA}"
    )
    assert abs(float(row["dec_deg"]) - WORKED_STAR_DEC) < 0.0005, (
        f"{WORKED_STAR_ID} carries dec_deg {row['dec_deg']!r}, expected {WORKED_STAR_DEC}"
    )
    assert abs(float(row["magnitude"]) - WORKED_STAR_MAGNITUDE) < 0.005, (
        f"{WORKED_STAR_ID} carries magnitude {row['magnitude']!r}, expected "
        f"{WORKED_STAR_MAGNITUDE}"
    )


def test_pick_resolves_the_brightest_star_in_radius(owner_client):
    response = owner_client.get(
        "/sky/pick",
        params={"ra_deg": PICK_RA, "dec_deg": PICK_DEC, "radius_deg": PICK_RADIUS},
    )
    assert response.status_code == 200, (
        f"GET /api/sky/pick at ra {PICK_RA} dec {PICK_DEC} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    star = response.json().get("star")
    assert star, (
        f"GET /api/sky/pick resolved no star at ra {PICK_RA} dec {PICK_DEC} "
        f"radius {PICK_RADIUS}, where the catalogue holds several"
    )
    assert star.get("star_id") == PICK_BRIGHTEST, (
        f"pick resolved {star.get('star_id')!r} at ra {PICK_RA} dec {PICK_DEC} "
        f"radius {PICK_RADIUS}; the brightest star inside that radius is "
        f"{PICK_BRIGHTEST}, not the nearest one, {PICK_NEAREST}"
    )


def test_pick_ties_resolve_to_the_lower_catalogue_id(owner_client):
    response = owner_client.get(
        "/sky/pick",
        params={"ra_deg": TIE_RA, "dec_deg": TIE_DEC, "radius_deg": TIE_RADIUS},
    )
    assert response.status_code == 200, (
        f"GET /api/sky/pick at ra {TIE_RA} dec {TIE_DEC} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    star = response.json().get("star")
    assert star, (
        f"pick resolved no star at ra {TIE_RA} dec {TIE_DEC} radius {TIE_RADIUS}, "
        f"where {TIE_WINNER} and {TIE_RUNNER_UP} both sit at the winning magnitude"
    )
    assert star.get("star_id") == TIE_WINNER, (
        f"pick resolved {star.get('star_id')!r}; {TIE_WINNER} and {TIE_RUNNER_UP} "
        f"share the brightest magnitude inside this radius, so the lower "
        f"catalogue id wins and that is {TIE_WINNER}"
    )


def test_pick_outside_any_radius_resolves_no_star(owner_client):
    response = owner_client.get(
        "/sky/pick",
        params={"ra_deg": EMPTY_RA, "dec_deg": EMPTY_DEC,
                "radius_deg": EMPTY_RADIUS},
    )
    assert response.status_code == 200, (
        f"GET /api/sky/pick over an empty patch returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    assert response.json().get("star") is None, (
        f"pick resolved {response.json().get('star')!r} at ra {EMPTY_RA} dec "
        f"{EMPTY_DEC} radius {EMPTY_RADIUS}, where the catalogue holds no star"
    )


def test_pick_measures_great_circle_separation_across_the_seam_and_near_a_pole(owner_client):
    probes = [
        ("the right ascension seam", SEAM_RA, SEAM_DEC, SEAM_RADIUS, SEAM_WINNER),
        ("the south pole", POLE_RA, POLE_DEC, POLE_RADIUS, POLE_WINNER),
    ]
    for label, ra, dec, radius, winner in probes:
        response = owner_client.get("/sky/pick", params={"ra_deg": ra, "dec_deg": dec, "radius_deg": radius})
        assert response.status_code == 200, (
            f"GET /api/sky/pick near {label} returned {response.status_code}: {response.text[:400]}"
        )
        star = response.json().get("star") or {}
        assert star.get("star_id") == winner, (
            f"pick near {label} at ra {ra} dec {dec} radius {radius} resolved "
            f"{star.get('star_id')!r}; measured along the sphere the brightest star inside the "
            f"radius is {winner}"
        )


def test_segment_is_persisted_against_two_catalogue_ids(owner_client):
    sky = create_sky(owner_client, unique("Probe Figure"))
    response = add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    assert response.status_code in (200, 201), (
        f"POST segment {SEGMENT_FROM} to {SEGMENT_TO} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    stored = read_sky(owner_client, sky["id"])["segments"]
    assert len(stored) == 1, f"the sky stored {len(stored)} segments, expected 1"
    assert stored[0]["from_star_id"] == SEGMENT_FROM, (
        f"the stored segment starts at {stored[0]['from_star_id']!r}, expected "
        f"{SEGMENT_FROM}: the endpoints are catalogue ids, never screen positions"
    )
    assert stored[0]["to_star_id"] == SEGMENT_TO, (
        f"the stored segment ends at {stored[0]['to_star_id']!r}, expected {SEGMENT_TO}"
    )


def test_segment_order_survives_a_reread(owner_client):
    sky = create_sky(owner_client, unique("Probe Order"))
    pairs = [(SEGMENT_FROM, SEGMENT_TO), (SEGMENT_TO, WORKED_STAR_ID),
             (WORKED_STAR_ID, SEGMENT_FROM)]
    for a, b in pairs:
        response = add_segment(owner_client, sky["id"], a, b)
        assert response.status_code in (200, 201), (
            f"POST segment {a} to {b} returned {response.status_code}: "
            f"{response.text[:400]}"
        )
    stored = read_sky(owner_client, sky["id"])["segments"]
    order = [(s["from_star_id"], s["to_star_id"]) for s in stored]
    assert order == pairs, (
        f"the sky returned segments in the order {order}, expected the order "
        f"they were added in, {pairs}"
    )
    positions = [s["position"] for s in stored]
    assert positions == [1, 2, 3], (
        f"segment positions read {positions}, expected 1, 2, 3 in order"
    )


def test_undo_removes_only_the_last_segment(owner_client):
    sky = create_sky(owner_client, unique("Probe Undo"))
    for a, b in ((SEGMENT_FROM, SEGMENT_TO), (SEGMENT_TO, WORKED_STAR_ID)):
        add_segment(owner_client, sky["id"], a, b)
    response = owner_client.delete(f"/skies/{sky['id']}/segments/last")
    assert response.status_code in (200, 204), (
        f"undo returned {response.status_code}: {response.text[:400]}"
    )
    stored = read_sky(owner_client, sky["id"])["segments"]
    assert len(stored) == 1, f"undo left {len(stored)} segments, expected 1"
    assert stored[0]["from_star_id"] == SEGMENT_FROM, (
        f"undo removed the wrong segment: the survivor starts at "
        f"{stored[0]['from_star_id']!r}, expected {SEGMENT_FROM}"
    )


def test_simultaneous_segments_each_take_their_own_position(owner_client):
    sky = create_sky(owner_client, unique("Probe Burst"))
    clients = _warm(len(BURST_PAIRS))
    try:
        responses = _at_once([
            lambda c=c, pair=pair: add_segment(c, sky["id"], pair[0], pair[1])
            for c, pair in zip(clients, BURST_PAIRS)
        ])
    finally:
        _close(clients)
    statuses = sorted(r.status_code for r in responses)
    assert all(s in (200, 201) for s in statuses), (
        f"{len(BURST_PAIRS)} segments sent to one sky at the same instant returned {statuses}; "
        f"none is refused or fails because another arrived with it"
    )
    stored = read_sky(owner_client, sky["id"])["segments"]
    positions = sorted(s["position"] for s in stored)
    assert positions == list(range(1, len(BURST_PAIRS) + 1)), (
        f"the sky holds positions {positions} after {len(BURST_PAIRS)} simultaneous segments; "
        f"positions run from 1 to the segment count with no gap and no repeat"
    )
    assert sorted((s["from_star_id"], s["to_star_id"]) for s in stored) == sorted(BURST_PAIRS), (
        f"the stored segments differ from the {len(BURST_PAIRS)} that were sent"
    )


def test_simultaneous_undos_each_remove_a_segment_of_their_own(owner_client):
    sky = create_sky(owner_client, unique("Probe Undo Burst"))
    for a, b in BURST_PAIRS[:6]:
        added = add_segment(owner_client, sky["id"], a, b)
        assert added.status_code in (200, 201), added.text[:400]
    clients = _warm(4)
    try:
        responses = _at_once([lambda c=c: c.delete(f"/skies/{sky['id']}/segments/last") for c in clients])
    finally:
        _close(clients)
    statuses = sorted(r.status_code for r in responses)
    assert statuses == [200, 200, 200, 200], (
        f"four simultaneous undos on six segments returned {statuses}"
    )
    removed = sorted(r.json().get("removed_position") for r in responses)
    assert removed == [3, 4, 5, 6], (
        f"four simultaneous undos on six segments reported removing positions {removed}; each "
        f"removes a segment of its own, newest first, so 6, 5, 4 and 3 are each reported once"
    )
    left = [s["position"] for s in read_sky(owner_client, sky["id"])["segments"]]
    assert left == [1, 2], f"after four simultaneous undos the sky holds positions {left}, expected [1, 2]"


def test_seeded_collection_reads_newest_first(owner_client):
    page = collection_page(owner_client, limit=PAGE_LIMIT_MAX)
    names = [row["name"] for row in rows_of(page)]
    seeded = [n for n in names if n in
              (SKY_MONOCEROS, SKY_LANTERN, SKY_KITE, SKY_HEXAGON)]
    assert seeded == [SKY_MONOCEROS, SKY_LANTERN, SKY_KITE, SKY_HEXAGON], (
        f"the seeded skies read {seeded}, expected newest first: "
        f"{[SKY_MONOCEROS, SKY_LANTERN, SKY_KITE, SKY_HEXAGON]}"
    )
    assert SKY_CORVUS not in names, (
        f"the collection for {STARGAZER_EMAIL} lists {SKY_CORVUS}, which belongs "
        f"to {OTHER_STARGAZER_EMAIL}"
    )


def test_brightness_filter_fills_the_page_before_paging(owner_client):
    page = stars_page(owner_client, limit=100, max_magnitude=BRIGHT_BOUND)
    items = rows_of(page)
    assert len(items) == 100, (
        f"GET /api/stars limit=100 max_magnitude={BRIGHT_BOUND} returned "
        f"{len(items)} rows; {BRIGHT_BOUND_ROWS} stars match that bound, so a "
        f"full page exists. A page filtered after it was read is short"
    )
    for row in items:
        assert float(row["magnitude"]) <= BRIGHT_BOUND, (
            f"the filtered page carries {row['star_id']!r} at magnitude "
            f"{row['magnitude']!r}, above the requested bound {BRIGHT_BOUND}"
        )


def test_catalogue_total_count_reports_matching_rows_not_page(owner_client):
    page = stars_page(owner_client, limit=10, max_magnitude=BRIGHT_BOUND)
    assert page["total_count"] == BRIGHT_BOUND_ROWS, (
        f"GET /api/stars max_magnitude={BRIGHT_BOUND} reports total_count "
        f"{page.get('total_count')!r}; {BRIGHT_BOUND_ROWS} catalogue rows match "
        f"that bound, and total_count counts matches rather than the page or "
        f"the whole catalogue"
    )
    assert page["has_more"] is True, (
        f"has_more reads {page.get('has_more')!r} on a ten-row page of "
        f"{BRIGHT_BOUND_ROWS} matching stars"
    )


def test_catalogue_walk_yields_every_row_once(owner_client):
    seen, cursor, pages = [], None, 0
    while pages < 40:
        page = stars_page(owner_client, limit=100, cursor=cursor,
                          max_magnitude=WALK_BOUND)
        pages += 1
        seen.extend(r["star_id"] for r in rows_of(page))
        assert page["total_count"] == WALK_BOUND_ROWS, (
            f"page {pages} reports total_count {page.get('total_count')!r}, "
            f"expected {WALK_BOUND_ROWS} rows at or below magnitude {WALK_BOUND}"
        )
        if not page.get("has_more"):
            break
        cursor = page.get("next_cursor")
        assert cursor, (
            f"has_more is true on page {pages} but next_cursor is {cursor!r}, "
            f"so the walk cannot continue"
        )
    assert len(seen) == len(set(seen)), (
        f"the walk returned {len(seen) - len(set(seen))} duplicate star ids "
        f"across {pages} pages"
    )
    assert len(seen) == WALK_BOUND_ROWS, (
        f"the walk collected {len(seen)} rows across {pages} pages, expected "
        f"{WALK_BOUND_ROWS}; every matching row appears exactly once"
    )


def test_last_page_of_an_exact_multiple_reports_no_more(owner_client):
    first = collection_page(owner_client, limit=2)
    assert first["has_more"] is True, (
        f"the first page of {SEEDED_SKY_COUNT} seeded skies at limit 2 reports "
        f"has_more {first.get('has_more')!r}"
    )
    cursor = first["next_cursor"]
    assert cursor, "the first collection page carries no next_cursor"
    second = collection_page(owner_client, limit=2, cursor=cursor)
    assert len(rows_of(second)) == 2, (
        f"the second collection page carries {len(rows_of(second))} rows, expected 2"
    )
    assert second["has_more"] is False, (
        f"the last page of an exactly filled collection reports has_more "
        f"{second.get('has_more')!r}; {SEEDED_SKY_COUNT} skies at limit 2 fill "
        f"two pages with nothing after them"
    )
    assert second.get("next_cursor") is None, (
        f"the last page carries next_cursor {second.get('next_cursor')!r}, "
        f"expected null"
    )


def test_collection_paging_yields_each_sky_once_after_an_insert(owner_client):
    first = collection_page(owner_client, limit=2)
    first_ids = [str(row["id"]) for row in rows_of(first)]
    cursor = first["next_cursor"]
    assert cursor, "the first collection page carries no next_cursor"
    create_sky(owner_client, unique("Probe Insert"))
    second = collection_page(owner_client, limit=2, cursor=cursor)
    second_ids = [str(row["id"]) for row in rows_of(second)]
    repeated = sorted(set(first_ids) & set(second_ids))
    assert not repeated, (
        f"sky ids {repeated} appear on both pages after one sky was created "
        f"between the two requests; a cursor addresses a row, so an insertion "
        f"ahead of the cursor cannot shift the page after it"
    )


def test_collection_lists_only_the_owning_stargazer(other_client):
    page = collection_page(other_client, limit=PAGE_LIMIT_MAX)
    names = [row["name"] for row in rows_of(page)]
    assert SKY_CORVUS in names, (
        f"the collection for {OTHER_STARGAZER_EMAIL} is missing {SKY_CORVUS}"
    )
    for leaked in (SKY_MONOCEROS, SKY_LANTERN, SKY_KITE, SKY_HEXAGON):
        assert leaked not in names, (
            f"the collection for {OTHER_STARGAZER_EMAIL} lists {leaked!r}, which "
            f"belongs to {STARGAZER_EMAIL}"
        )


def test_seeding_twice_duplicates_no_row(backend):
    assert backend.count("stargazers") == 2, (
        f"the stargazers table holds {backend.count('stargazers')} rows, expected "
        f"the two seeded accounts; seeding must be idempotent across a restart"
    )
    assert backend.count("stars") == CATALOGUE_ROWS, (
        f"the stars table holds {backend.count('stars')} rows, expected "
        f"{CATALOGUE_ROWS}; re-seeding must not duplicate the catalogue"
    )


def test_published_payload_is_frozen_against_later_edits(owner_client, anon_client):
    sky = create_sky(owner_client, unique("Probe Frozen"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    published = publish(owner_client, sky["id"], unique("key"))
    assert published.status_code in (200, 201), (
        f"publish returned {published.status_code}: {published.text[:400]}"
    )
    token = published.json()["share_token"]
    before = anon_client.get(f"/shares/{token}")
    assert before.status_code == 200, (
        f"the published link returned {before.status_code}: {before.text[:400]}"
    )
    original = before.json()["segments"]
    assert len(original) == 1, (
        f"the frozen copy carries {len(original)} segments, expected 1"
    )
    add_segment(owner_client, sky["id"], SEGMENT_TO, WORKED_STAR_ID)
    settle()
    after = anon_client.get(f"/shares/{token}")
    assert after.status_code == 200, (
        f"the published link returned {after.status_code} after a later edit"
    )
    assert after.json()["segments"] == original, (
        f"the published link now returns {len(after.json()['segments'])} segments; "
        f"a frozen copy is stored at publish time, so drawing on the sky "
        f"afterwards cannot change what the link returns"
    )


def test_idempotent_publish_replay_creates_no_second_record(owner_client, backend):
    sky = create_sky(owner_client, unique("Probe Replay"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    key = unique("replay")
    first = publish(owner_client, sky["id"], key)
    assert first.status_code in (200, 201), (
        f"the first publish returned {first.status_code}: {first.text[:400]}"
    )
    token = first.json()["share_token"]
    for attempt in range(3):
        again = publish(owner_client, sky["id"], key)
        assert again.status_code in (200, 201, 409), (
            f"publish replay {attempt} returned {again.status_code}: "
            f"{again.text[:400]}"
        )
        if again.status_code in (200, 201):
            assert again.json()["share_token"] == token, (
                f"publish replay {attempt} returned a different share_token; a "
                f"replayed publish carrying share_key {key!r} returns the first one"
            )
    stored = backend.count("published_skies", share_key=key)
    assert stored == 1, (
        f"the published_skies table holds {stored} rows for share_key {key!r} "
        f"after three replays, expected exactly one"
    )


def test_concurrent_publish_on_one_share_key_has_a_single_winner(owner_client, backend):
    sky = create_sky(owner_client, unique("Probe Race"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    key = unique("race")
    clients = _warm(4)
    try:
        responses = _at_once([lambda c=c: publish(c, sky["id"], key) for c in clients])
    finally:
        _close(clients)
    codes = sorted(r.status_code for r in responses)
    assert all(c in (200, 201, 409) for c in codes), (
        f"four simultaneous publishes carrying share_key {key!r} returned {codes}; each is either "
        f"the winner, a replay of the winner or a 409 conflict"
    )
    tokens = {r.json()["share_token"] for r in responses if r.status_code in (200, 201)}
    assert len(tokens) == 1, (
        f"four simultaneous publishes carrying share_key {key!r} answered {len(tokens)} different "
        f"share tokens; exactly one publish wins and any replay carries its token"
    )
    stored = backend.count("published_skies", share_key=key)
    assert stored == 1, (
        f"the published_skies table holds {stored} rows for share_key {key!r} "
        f"after four simultaneous publishes, expected exactly one"
    )


def test_republishing_mints_a_new_share_token(owner_client, anon_client):
    sky = create_sky(owner_client, unique("Probe Republish"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    first = publish(owner_client, sky["id"], unique("first"))
    assert first.status_code in (200, 201), first.text[:400]
    first_token = first.json()["share_token"]
    add_segment(owner_client, sky["id"], SEGMENT_TO, WORKED_STAR_ID)
    second = publish(owner_client, sky["id"], unique("second"))
    assert second.status_code in (200, 201), second.text[:400]
    second_token = second.json()["share_token"]
    assert second_token != first_token, (
        "republishing returned the earlier share_token; a second publish mints "
        "a new one over the sky as it stands"
    )
    earlier = anon_client.get(f"/shares/{first_token}")
    assert earlier.status_code == 200, (
        f"the earlier link returned {earlier.status_code} after republishing; "
        f"it keeps working"
    )
    assert len(earlier.json()["segments"]) == 1, (
        f"the earlier link now returns {len(earlier.json()['segments'])} segments, "
        f"expected the single segment it froze"
    )


def test_client_supplied_manage_token_is_never_honoured(owner_client, anon_client):
    sky = create_sky(owner_client, unique("Probe Token"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    chosen_share = unique("chosen-share")
    chosen_manage = unique("chosen-manage")
    response = publish(
        owner_client, sky["id"], unique("mint"),
        share_token=chosen_share, manage_token=chosen_manage,
    )
    assert response.status_code in (200, 201), (
        f"publish returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    assert body["share_token"] != chosen_share, (
        f"publish returned the share_token the caller supplied, {chosen_share!r}; "
        f"both tokens are minted by the server"
    )
    assert body["manage_token"] != chosen_manage, (
        f"publish returned the manage_token the caller supplied, "
        f"{chosen_manage!r}; both tokens are minted by the server"
    )
    guessed = anon_client.get(f"/shares/{chosen_share}")
    assert guessed.status_code in CLIENT_ERRORS, (
        f"the share_token the caller invented, {chosen_share!r}, resolves with "
        f"{guessed.status_code}; a token the server never minted addresses nothing"
    )


def test_other_stargazer_is_denied_the_private_sky(owner_client, other_client):
    target = require_sky(owner_client, SKY_HEXAGON)
    response = other_client.get(f"/skies/{target['id']}")
    assert response.status_code in DENIALS, (
        f"{OTHER_STARGAZER_EMAIL} read {SKY_HEXAGON}, which belongs to "
        f"{STARGAZER_EMAIL}, with {response.status_code}: {response.text[:400]}"
    )
    written = add_segment(other_client, target["id"], SEGMENT_FROM, SEGMENT_TO)
    assert written.status_code in DENIALS, (
        f"{OTHER_STARGAZER_EMAIL} wrote a segment onto {SKY_HEXAGON} with "
        f"{written.status_code}"
    )
    still = read_sky(owner_client, target["id"])["segments"]
    assert len(still) == 1, (
        f"{SKY_HEXAGON} now carries {len(still)} segments; a refused write leaves "
        f"the protected state unchanged"
    )


def test_other_stargazer_is_denied_the_private_render(owner_client, other_client):
    target = require_sky(owner_client, SKY_HEXAGON)
    made = render(owner_client, target["id"])
    assert made.status_code in (200, 201), (
        f"the owner's render returned {made.status_code}: {made.text[:400]}"
    )
    response = other_client.get(f"/skies/{target['id']}/renders/latest")
    assert response.status_code in DENIALS, (
        f"{OTHER_STARGAZER_EMAIL} read the rendered image of {SKY_HEXAGON} with "
        f"{response.status_code}; a private sky's render is the owner's alone"
    )


def test_anonymous_request_to_the_collection_is_denied(anon_client, owner_client):
    response = anon_client.get("/skies", params={"limit": 1})
    assert response.status_code in DENIALS, (
        f"an unauthenticated GET /api/skies returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    catalogue = anon_client.get("/stars", params={"limit": 1})
    assert catalogue.status_code in DENIALS, (
        f"an unauthenticated GET /api/stars returned {catalogue.status_code}; "
        f"the catalogue is not open to a visitor"
    )
    target = require_sky(owner_client, SKY_KITE)
    written = add_segment(anon_client, target["id"], SEGMENT_FROM, SEGMENT_TO)
    assert written.status_code in DENIALS, (
        f"an unauthenticated segment write returned {written.status_code}"
    )


def test_published_share_reads_without_a_token(anon_client):
    response = anon_client.get(f"/shares/{SEEDED_SHARE_TOKEN}")
    assert response.status_code == 200, (
        f"the seeded published link {SEEDED_SHARE_TOKEN} returned "
        f"{response.status_code} to a visitor: {response.text[:400]}"
    )
    body = response.json()
    assert len(body["segments"]) == LANTERN_SEGMENTS, (
        f"the seeded published sky carries {len(body['segments'])} segments, "
        f"expected {LANTERN_SEGMENTS}"
    )
    assert body["sky_name"] == SKY_LANTERN, (
        f"the seeded published sky is named {body['sky_name']!r}, expected "
        f"{SKY_LANTERN}"
    )


def test_unknown_share_token_resolves_to_nothing(anon_client):
    response = anon_client.get(f"/shares/{unique('never-minted')}")
    assert response.status_code in CLIENT_ERRORS, (
        f"a share token the server never minted returned {response.status_code}: "
        f"{response.text[:400]}"
    )


def test_unseeded_email_cannot_sign_in():
    response = httpx.post(
        f"{api_base()}/auth/login",
        json={"email": unique("newcomer") + "@example.com",
              "password": SEEDED_PASSWORD},
        timeout=30.0,
    )
    assert response.status_code in CLIENT_ERRORS, (
        f"an address that was never seeded signed in with "
        f"{response.status_code}; signup is closed and accounts are seeded only"
    )


def test_unknown_star_id_in_a_segment_is_refused(owner_client):
    sky = create_sky(owner_client, unique("Probe Unknown"))
    response = add_segment(owner_client, sky["id"], SEGMENT_FROM, UNKNOWN_STAR_ID)
    assert response.status_code in CLIENT_ERRORS, (
        f"a segment naming {UNKNOWN_STAR_ID}, which is not a catalogue id, "
        f"returned {response.status_code}: {response.text[:400]}"
    )
    assert read_sky(owner_client, sky["id"])["segments"] == [], (
        "a refused segment was written anyway"
    )


def test_self_joining_segment_is_refused(owner_client):
    sky = create_sky(owner_client, unique("Probe Self"))
    response = add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_FROM)
    assert response.status_code in CLIENT_ERRORS, (
        f"a segment joining {SEGMENT_FROM} to itself returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    assert read_sky(owner_client, sky["id"])["segments"] == [], (
        "a refused self-joining segment was written anyway"
    )


def test_another_stargazer_is_refused_on_every_write_route(owner_client, other_client, store, backend):
    sky = create_sky(owner_client, unique("Probe Guard"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    key = unique("guard")
    attempts = [
        ("adding a segment", add_segment(other_client, sky["id"], SEGMENT_TO, WORKED_STAR_ID)),
        ("undoing a segment", other_client.delete(f"/skies/{sky['id']}/segments/last")),
        ("rendering", render(other_client, sky["id"])),
        ("publishing", publish(other_client, sky["id"], key)),
    ]
    for label, response in attempts:
        assert response.status_code in DENIALS, (
            f"{OTHER_STARGAZER_EMAIL} {label} on a sky owned by {STARGAZER_EMAIL} returned "
            f"{response.status_code}: {response.text[:300]}"
        )
    settle()
    kept = [(s["from_star_id"], s["to_star_id"]) for s in read_sky(owner_client, sky["id"])["segments"]]
    assert kept == [(SEGMENT_FROM, SEGMENT_TO)], (
        f"the owner's sky now holds {kept} after another stargazer's refused writes"
    )
    leftover = store.list(f"renders/{sky['id']}/")
    assert leftover == [], f"another stargazer's refused render still wrote {leftover}"
    assert backend.count("published_skies", share_key=key) == 0, (
        f"another stargazer's refused publish still stored a published row for share_key {key!r}"
    )


def test_empty_sky_name_is_refused_with_the_field_named(owner_client):
    before = collection_page(owner_client, limit=PAGE_LIMIT_MAX)["total_count"]
    response = owner_client.post("/skies", json={"name": "   ", "line_colour": "g"})
    assert response.status_code in CLIENT_ERRORS, (
        f"a whitespace-only sky name returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    assert "name" in response.text.lower(), (
        f"the refusal body does not name the offending field: "
        f"{response.text[:400]}"
    )
    after = collection_page(owner_client, limit=PAGE_LIMIT_MAX)["total_count"]
    assert after == before, (
        f"the collection grew from {before} to {after} after a refused create"
    )


def test_overlong_sky_name_is_refused(owner_client):
    response = owner_client.post(
        "/skies",
        json={"name": "N" * (MAX_NAME_LENGTH + 1), "line_colour": "g"},
    )
    assert response.status_code in CLIENT_ERRORS, (
        f"a name of {MAX_NAME_LENGTH + 1} characters returned "
        f"{response.status_code}: {response.text[:400]}"
    )


def test_undo_on_an_empty_sky_is_refused(owner_client):
    sky = create_sky(owner_client, unique("Probe Empty"))
    response = owner_client.delete(f"/skies/{sky['id']}/segments/last")
    assert response.status_code in CLIENT_ERRORS, (
        f"undo on a sky carrying no segments returned {response.status_code}: "
        f"{response.text[:400]}"
    )


def test_limit_outside_the_band_is_refused(owner_client):
    for bad in (0, PAGE_LIMIT_MAX + 1):
        response = owner_client.get("/stars", params={"limit": bad})
        assert response.status_code in CLIENT_ERRORS, (
            f"GET /api/stars limit={bad} returned {response.status_code}; the "
            f"band runs 1 to {PAGE_LIMIT_MAX}"
        )


def test_duplicate_rapid_publish_from_one_session_is_refused(owner_client):
    sky = create_sky(owner_client, unique("Probe Rapid"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    codes = [publish(owner_client, sky["id"], unique("rapid")).status_code
             for _ in range(6)]
    assert any(c in CLIENT_ERRORS for c in codes), (
        f"six publishes fired back to back from one session all succeeded "
        f"({codes}); a session publishes at most five times in a burst, so the "
        f"sixth is refused"
    )


def test_filled_decoy_field_refuses_the_publish(owner_client):
    sky = create_sky(owner_client, unique("Probe Decoy"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    response = publish(owner_client, sky["id"], unique("decoy"),
                       **{DECOY_FIELD: "an automated hand filled this in"})
    assert response.status_code in CLIENT_ERRORS, (
        f"a publish carrying a filled {DECOY_FIELD} returned "
        f"{response.status_code}: {response.text[:400]}"
    )


def test_internal_links_on_public_routes_resolve(anon_client):
    response = anon_client.get(f"/shares/{SEEDED_SHARE_TOKEN}")
    assert response.status_code == 200, (
        f"the seeded published link returned {response.status_code}"
    )
    payload = response.json()
    for field in ("sky_name", "line_colour", "segments", "view_ra_deg",
                  "view_dec_deg", "view_zoom", "published_at", "payload_version"):
        assert field in payload, (
            f"the published payload is missing {field!r}: "
            f"{sorted(payload)}"
        )


def test_render_upload_lands_in_the_object_store(owner_client, store):
    sky = create_sky(owner_client, unique("Probe Render"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    response = render(owner_client, sky["id"])
    assert response.status_code in (200, 201), (
        f"the render returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    expected = f"renders/{sky['id']}/{body['revision']}.svg"
    assert body["object_key"] == expected, (
        f"the render reports object_key {body['object_key']!r}, expected "
        f"{expected!r}"
    )
    settle()
    assert store.exists(expected), (
        f"no object exists in the bucket at {expected!r}; the rendered image "
        f"lives in the object store, never on the app's own filesystem"
    )


def test_render_upload_is_append_only_across_revisions(owner_client, store):
    sky = create_sky(owner_client, unique("Probe Append"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    first = render(owner_client, sky["id"])
    assert first.status_code in (200, 201), first.text[:400]
    assert first.json()["revision"] == 1, (
        f"the first render reports revision {first.json()['revision']!r}, "
        f"expected 1"
    )
    add_segment(owner_client, sky["id"], SEGMENT_TO, WORKED_STAR_ID)
    second = render(owner_client, sky["id"])
    assert second.status_code in (200, 201), second.text[:400]
    assert second.json()["revision"] == 2, (
        f"the second render reports revision {second.json()['revision']!r}, "
        f"expected 2"
    )
    settle()
    keys = sorted(store.list(f"renders/{sky['id']}/"))
    assert keys == [f"renders/{sky['id']}/1.svg", f"renders/{sky['id']}/2.svg"], (
        f"the bucket holds {keys} under this sky; a later render writes a new "
        f"key and leaves every earlier one in place"
    )


def test_simultaneous_renders_each_take_a_revision_of_their_own(owner_client, store):
    sky = create_sky(owner_client, unique("Probe Render Burst"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    clients = _warm(4)
    try:
        responses = _at_once([lambda c=c: render(c, sky["id"]) for c in clients])
    finally:
        _close(clients)
    statuses = sorted(r.status_code for r in responses)
    assert all(s in (200, 201) for s in statuses), (
        f"four simultaneous renders of one sky returned {statuses}"
    )
    revisions = sorted(r.json()["revision"] for r in responses)
    assert revisions == [1, 2, 3, 4], (
        f"four simultaneous renders of one sky reported revisions {revisions}; each takes a "
        f"revision of its own, so no two share a revision or a key"
    )
    settle()
    keys = sorted(store.list(f"renders/{sky['id']}/"))
    expected = sorted(f"renders/{sky['id']}/{n}.svg" for n in (1, 2, 3, 4))
    assert keys == expected, (
        f"the bucket holds {keys} under this sky after four simultaneous renders, expected {expected}"
    )


def test_render_svg_carries_one_line_per_segment(owner_client):
    sky = create_sky(owner_client, unique("Probe Lines"))
    pairs = [(SEGMENT_FROM, SEGMENT_TO), (SEGMENT_TO, WORKED_STAR_ID)]
    for a, b in pairs:
        add_segment(owner_client, sky["id"], a, b)
    made = render(owner_client, sky["id"])
    assert made.status_code in (200, 201), made.text[:400]
    response = owner_client.get(f"/skies/{sky['id']}/renders/latest")
    assert response.status_code == 200, (
        f"reading the latest render returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    assert RENDER_CONTENT_TYPE in response.headers.get("content-type", ""), (
        f"the render was served as {response.headers.get('content-type')!r}, "
        f"expected {RENDER_CONTENT_TYPE}"
    )
    drawn = response.text.count("<line")
    assert drawn == len(pairs), (
        f"the rendered image carries {drawn} line elements for {len(pairs)} "
        f"segments"
    )


def test_render_latest_is_refused_before_any_render(owner_client):
    sky = create_sky(owner_client, unique("Probe Norender"))
    add_segment(owner_client, sky["id"], SEGMENT_FROM, SEGMENT_TO)
    response = owner_client.get(f"/skies/{sky['id']}/renders/latest")
    assert response.status_code in CLIENT_ERRORS, (
        f"a sky that was never rendered served an image with "
        f"{response.status_code}; the stored object is the render, so there is "
        f"nothing to serve until one is written"
    )


def test_signing_out_ends_that_session_alone(owner_client):
    token = login(STARGAZER_EMAIL, SEEDED_PASSWORD)
    with client(token) as c:
        before = c.get("/skies", params={"limit": 1})
        out = c.post("/auth/logout")
        after = c.get("/skies", params={"limit": 1})
    assert before.status_code == 200, f"a fresh session was refused before signing out: {before.status_code}"
    assert out.status_code in (200, 204), (
        f"POST /api/auth/logout returned {out.status_code}: {out.text[:300]}"
    )
    assert after.status_code in DENIALS, (
        f"the token that signed out still reads the collection with {after.status_code}; signing "
        f"out ends that session and its token is refused from then on"
    )
    other_session = owner_client.get("/skies", params={"limit": 1})
    assert other_session.status_code == 200, (
        f"another session of {STARGAZER_EMAIL} was refused with {other_session.status_code} after "
        f"one session signed out; only the session that signed out ends"
    )
