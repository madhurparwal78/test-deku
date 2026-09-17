from __future__ import annotations

import concurrent.futures

import httpx
import re as _re
from _shapes import flatten, items
from appclient import app_url
from appclient import client as make_client

from conftest import (
    BACKLIST_SLUGS,
    CAD,
    CA_BASE_MINOR,
    CA_EXTRA_MINOR,
    CURRENT_SLUGS,
    MEMBER2_EMAIL,
    MEMBER3_EMAIL,
    MEMBER_EMAIL,
    PREVIOUS_SLUGS,
    PROMOTION_BASE_MINOR,
    PROMOTION_CODE,
    SEEDED_GIFT_CODE,
    SEED_PASSWORD,
    USD,
    US_BASE_MINOR,
    US_EXTRA_MINOR,
    add_to_box,
    box_items_of,
    build_box,
    current_utc_year,
    empty_box,
    place_box,
    settle,
    signup_payload,
)

US_TWO_BOOK_TOTAL = 2898
US_THREE_BOOK_TOTAL = 3997
CA_TWO_BOOK_TOTAL = 4198
CA_THREE_BOOK_TOTAL = 5797
PROMOTION_THREE_BOOK_TOTAL = 2598
CREDIT_THREE_BOOK_TOTAL = 2198
US_INVOICE_DECIMAL = "39.97"
US_INVOICE_CURRENCY = "USD"

CONFIRMATION_SUBJECT_PREFIX = "Box confirmed: "
GIFT_SUBJECT_PREFIX = "Your e-gift card: "
INVALID_BOX_COPY = "Add at least one book from this month to complete your box."
FULL_BOX_COPY = "Three books is the limit. Remove one to add another."
WRONG_COUNTRY_COPY = "That code is for USA orders only."
CREDIT_APPLIED_COPY = "One free credit applied. You have"
SPECIAL_ADDRESS_COPY = "We ship there, but we'll need to set it up by hand."

FLAT_TAGS = ("Includes a Dog", "Includes a Cat", "Award Worthy", "LGBTQIA+", "Pangolin Original")


def _total_of(payload) -> int:
    for key in ("total_minor", "total"):
        if isinstance(payload, dict) and isinstance(payload.get(key), int):
            return payload[key]
    if isinstance(payload, dict):
        box = payload.get("box")
        if isinstance(box, dict):
            return _total_of(box)
    raise AssertionError(
        f"no integer total_minor in the response: {str(payload)[:400]}"
    )


def _instant_of(payload, key: str) -> str:
    value = payload.get(key) if isinstance(payload, dict) else None
    if value is None and isinstance(payload, dict):
        cycle = payload.get("cycle")
        if isinstance(cycle, dict):
            value = cycle.get(key)
    assert value, f"no {key} in the cycle response: {str(payload)[:400]}"
    return str(value).replace("T", " ").replace("Z", "").strip()


def _slugs_of(payload) -> list:
    out = []
    for item in box_items_of(payload):
        if isinstance(item, dict):
            out.append(item.get("slug") or item.get("edition_slug"))
        else:
            out.append(item)
    return [s for s in out if s]




def test_health_returns_ok(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:400]}"
    )


def test_current_cycle_reveals_the_seeded_selection(anon_client, db):
    response = anon_client.get("/cycles/current")
    assert response.status_code == 200, (
        f"GET /api/cycles/current returned {response.status_code}: {response.text[:400]}"
    )
    payload = response.json()
    blob = flatten(payload)
    missing = [slug for slug in CURRENT_SLUGS if slug not in blob]
    assert not missing, (
        f"GET /api/cycles/current omitted {len(missing)} of the seven current "
        f"editions {missing}: {response.text[:400]}"
    )
    stale = [slug for slug in PREVIOUS_SLUGS if slug in blob]
    assert not stale, (
        f"GET /api/cycles/current carries previous-cycle editions {stale}, so the "
        f"reveal is partial: {response.text[:400]}"
    )
    opens = _instant_of(payload, "opens_at")
    closes = _instant_of(payload, "closes_at")
    assert opens.endswith("00:00:00"), (
        f"the current cycle opens at {opens!r} rather than at 00:00:00 UTC on the "
        f"first of its month: {response.text[:400]}"
    )
    assert opens[8:10] == "01", (
        f"the current cycle opens on day {opens[8:10]!r} rather than the first: "
        f"{response.text[:400]}"
    )
    assert closes.endswith("00:00:00") and closes[8:10] == "01", (
        f"the current cycle closes at {closes!r} rather than at 00:00:00 UTC on the "
        f"first of the next month: {response.text[:400]}"
    )
    assert closes > opens, (
        f"the current cycle closes at {closes!r}, which is not after its open at "
        f"{opens!r}"
    )
    current_ids = {db.edition_by_slug(s)["cycle_id"] for s in CURRENT_SLUGS}
    assert len(current_ids) == 1 and None not in current_ids, (
        f"the seven current editions carry cycle ids {current_ids}; one cycle is "
        f"current at any instant and all seven belong to it"
    )
    previous_ids = {db.edition_by_slug(s)["cycle_id"] for s in PREVIOUS_SLUGS}
    assert len(previous_ids) == 1 and previous_ids.isdisjoint(current_ids), (
        f"the two previous-cycle editions carry cycle ids {previous_ids}, which is "
        f"not one cycle distinct from the current one {current_ids}"
    )


def test_editions_list_returns_every_orderable_slug(anon_client):
    response = anon_client.get("/editions")
    assert response.status_code == 200, (
        f"GET /api/editions returned {response.status_code}: {response.text[:400]}"
    )
    blob = flatten(items(response.json()))
    expected = list(CURRENT_SLUGS) + list(PREVIOUS_SLUGS) + list(BACKLIST_SLUGS)
    missing = [slug for slug in expected if slug not in blob]
    assert not missing, (
        f"GET /api/editions omitted {missing} of the thirteen seeded editions: "
        f"{response.text[:400]}"
    )


def test_edition_detail_carries_the_flat_tag_vocabulary(anon_client):
    seen = set()
    for slug in ("the-orrery-thief", "salt-and-static", "a-quiet-inventory",
                 "the-pangolin-anthology", "the-lamplighters-daughter"):
        response = anon_client.get(f"/editions/{slug}")
        assert response.status_code == 200, (
            f"GET /api/editions/{slug} returned {response.status_code}: "
            f"{response.text[:400]}"
        )
        blob = flatten(response.json())
        for tag in FLAT_TAGS:
            if tag.lower() in blob:
                seen.add(tag)
    missing = [tag for tag in FLAT_TAGS if tag not in seen]
    assert not missing, (
        f"the seeded editions carry none of the flat tags {missing}; the tag list "
        f"is one flat vocabulary and every one of these is in it"
    )


def test_catalogue_filters_by_genre(anon_client):
    response = anon_client.get("/editions", params={"genre": "Horror"})
    assert response.status_code == 200, (
        f"GET /api/editions?genre=Horror returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    rows = items(response.json())
    blob = flatten(rows)
    assert "salt-and-static" in blob, (
        f"GET /api/editions?genre=Horror omitted salt-and-static, which is tagged "
        f"Horror: {response.text[:400]}"
    )
    assert "every-third-tuesday" not in blob, (
        f"GET /api/editions?genre=Horror returned every-third-tuesday, which is "
        f"tagged Romance: {response.text[:400]}"
    )


def test_box_of_three_places_and_totals_correctly(member_client):
    build_box(member_client, ("the-orrery-thief", "salt-and-static", "a-quiet-inventory"))
    response = member_client.get("/box")
    assert response.status_code == 200, (
        f"GET /api/box returned {response.status_code}: {response.text[:400]}"
    )
    assert _total_of(response.json()) == US_THREE_BOOK_TOTAL, (
        f"GET /api/box for a three-book US box totalled "
        f"{_total_of(response.json())} rather than {US_THREE_BOOK_TOTAL}: "
        f"{response.text[:400]}"
    )
    placed = place_box(member_client)
    assert placed.status_code in (200, 201), (
        f"POST /api/box/place returned {placed.status_code}: {placed.text[:400]}"
    )
    assert _total_of(placed.json()) == US_THREE_BOOK_TOTAL, (
        f"POST /api/box/place recorded a total other than {US_THREE_BOOK_TOTAL}: "
        f"{placed.text[:400]}"
    )


def test_two_book_total_matches_the_worked_example(member_client):
    build_box(member_client, ("the-orrery-thief", "salt-and-static"))
    response = member_client.get("/box")
    assert response.status_code == 200, (
        f"GET /api/box returned {response.status_code}: {response.text[:400]}"
    )
    assert _total_of(response.json()) == US_TWO_BOOK_TOTAL, (
        f"a two-book US box totalled {_total_of(response.json())} rather than "
        f"{US_BASE_MINOR} plus {US_EXTRA_MINOR} = {US_TWO_BOOK_TOTAL}: "
        f"{response.text[:400]}"
    )


def test_canada_totals_match_the_worked_examples(member2_client):
    build_box(member2_client, ("the-orrery-thief", "salt-and-static"))
    two = member2_client.get("/box")
    assert two.status_code == 200, (
        f"GET /api/box returned {two.status_code}: {two.text[:400]}"
    )
    assert _total_of(two.json()) == CA_TWO_BOOK_TOTAL, (
        f"a two-book CA box totalled {_total_of(two.json())} rather than "
        f"{CA_BASE_MINOR} plus {CA_EXTRA_MINOR} = {CA_TWO_BOOK_TOTAL}: {two.text[:400]}"
    )
    added = add_to_box(member2_client, "a-quiet-inventory")
    assert added.status_code in (200, 201), (
        f"POST /api/box/items returned {added.status_code}: {added.text[:400]}"
    )
    three = member2_client.get("/box")
    assert _total_of(three.json()) == CA_THREE_BOOK_TOTAL, (
        f"a three-book CA box totalled {_total_of(three.json())} rather than "
        f"{CA_THREE_BOOK_TOTAL}: {three.text[:400]}"
    )


def test_box_without_a_current_title_is_refused(member_client):
    build_box(member_client, ("the-glass-cartographer",))
    response = place_box(member_client)
    assert 400 <= response.status_code < 500, (
        f"POST /api/box/place on a box with no current-cycle edition returned "
        f"{response.status_code} rather than a client error: {response.text[:400]}"
    )
    assert INVALID_BOX_COPY.lower() in flatten(response.json()), (
        f"POST /api/box/place refused the box without stating "
        f"{INVALID_BOX_COPY!r}: {response.text[:400]}"
    )


def test_reprint_alone_does_not_satisfy_the_composition_rule(member_client):
    build_box(member_client, ("salt-and-static-reprint", "the-glass-cartographer"))
    response = place_box(member_client)
    assert 400 <= response.status_code < 500, (
        f"POST /api/box/place on a box holding only salt-and-static-reprint and a "
        f"previous-cycle edition returned {response.status_code} rather than a "
        f"client error: {response.text[:400]}"
    )
    assert INVALID_BOX_COPY.lower() in flatten(response.json()), (
        f"the reprint was treated as this month's salt-and-static: "
        f"{response.text[:400]}"
    )


def test_every_edition_stays_addable_while_the_box_is_invalid(member_client):
    build_box(member_client, ("the-glass-cartographer",))
    response = add_to_box(member_client, "feral-arithmetic")
    assert response.status_code in (200, 201), (
        f"POST /api/box/items {{'slug': 'feral-arithmetic'}} returned "
        f"{response.status_code} on a box that is not yet valid; every edition "
        f"stays addable and only placement is refused: {response.text[:400]}"
    )
    assert "feral-arithmetic" in _slugs_of(response.json()), (
        f"the second edition was not added to the box: {response.text[:400]}"
    )


def test_fourth_edition_is_refused_at_the_limit(member_client):
    build_box(member_client, ("the-orrery-thief", "salt-and-static", "nine-yards-of-night"))
    response = add_to_box(member_client, "every-third-tuesday")
    assert 400 <= response.status_code < 500, (
        f"POST /api/box/items for a fourth edition returned {response.status_code} "
        f"rather than a client error: {response.text[:400]}"
    )
    assert FULL_BOX_COPY.lower() in flatten(response.json()), (
        f"the fourth addition was refused without stating {FULL_BOX_COPY!r}: "
        f"{response.text[:400]}"
    )
    after = member_client.get("/box")
    assert len(box_items_of(after.json())) == 3, (
        f"the box changed after a refused fourth addition: {after.text[:400]}"
    )


def test_empty_box_placement_is_refused(member_client):
    empty_box(member_client)
    response = place_box(member_client)
    assert 400 <= response.status_code < 500, (
        f"POST /api/box/place on an empty box returned {response.status_code} "
        f"rather than a client error: {response.text[:400]}"
    )


def test_preseeded_link_keeps_only_the_first_three_ids(member_client):
    empty_box(member_client)
    ids = "the-orrery-thief,salt-and-static,every-third-tuesday,a-quiet-inventory"
    response = member_client.get("/box", params={"ids": ids})
    assert response.status_code == 200, (
        f"GET /api/box?ids={ids} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    slugs = _slugs_of(response.json())
    assert len(slugs) == 3, (
        f"a pre-seeded link carrying four ids produced {len(slugs)} items rather "
        f"than three: {response.text[:400]}"
    )
    assert "a-quiet-inventory" not in slugs, (
        f"the fourth id in the link survived rather than being dropped: "
        f"{response.text[:400]}"
    )


def test_preseeded_link_drops_an_unknown_id(member_client):
    empty_box(member_client)
    ids = "the-orrery-thief,no-such-edition-at-all"
    response = member_client.get("/box", params={"ids": ids})
    assert response.status_code == 200, (
        f"GET /api/box?ids={ids} returned {response.status_code} rather than "
        f"rebuilding the box from what survives: {response.text[:400]}"
    )
    slugs = _slugs_of(response.json())
    assert slugs == ["the-orrery-thief"], (
        f"an id naming no orderable edition was not dropped; the box holds "
        f"{slugs}: {response.text[:400]}"
    )


def test_promotion_replaces_the_base_charge(member3_client):
    build_box(member3_client, ("the-orrery-thief", "salt-and-static", "a-quiet-inventory"))
    response = member3_client.post("/box/place", json={"promotion_code": PROMOTION_CODE})
    assert response.status_code in (200, 201), (
        f"POST /api/box/place with promotion_code {PROMOTION_CODE!r} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    assert _total_of(response.json()) == PROMOTION_THREE_BOOK_TOTAL, (
        f"a first three-book US order under {PROMOTION_CODE} totalled "
        f"{_total_of(response.json())} rather than {PROMOTION_BASE_MINOR} plus two "
        f"extras = {PROMOTION_THREE_BOOK_TOTAL}: {response.text[:400]}"
    )


def test_promotion_is_refused_for_a_canada_member(member2_client):
    build_box(member2_client, ("the-orrery-thief",))
    response = member2_client.post("/box/place", json={"promotion_code": PROMOTION_CODE})
    assert 400 <= response.status_code < 500, (
        f"POST /api/box/place with {PROMOTION_CODE!r} from a CA member returned "
        f"{response.status_code} rather than a client error: {response.text[:400]}"
    )
    assert WRONG_COUNTRY_COPY.lower() in flatten(response.json()), (
        f"the code was refused without stating {WRONG_COUNTRY_COPY!r}: "
        f"{response.text[:400]}"
    )


def test_credit_is_applied_to_the_base_charge_first(member2_client, db):
    member = db.member_by_email(MEMBER2_EMAIL)
    assert member, f"no seeded member row for {MEMBER2_EMAIL}"
    build_box(member2_client, ("the-orrery-thief", "salt-and-static", "a-quiet-inventory"))
    response = member2_client.post("/box/place", json={"use_credits": True})
    assert response.status_code in (200, 201), (
        f"POST /api/box/place with use_credits returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    expected = CA_EXTRA_MINOR * 2
    assert _total_of(response.json()) == expected, (
        f"a three-book CA box with one credit totalled {_total_of(response.json())} "
        f"rather than the two extra charges alone ({expected}); the credit is "
        f"applied to the base charge first: {response.text[:400]}"
    )


def test_credit_and_promotion_are_never_combined(member3_client):
    build_box(member3_client, ("the-orrery-thief", "salt-and-static"))
    response = member3_client.post(
        "/box/place", json={"promotion_code": PROMOTION_CODE, "use_credits": True})
    assert 400 <= response.status_code < 500, (
        f"POST /api/box/place carrying both {PROMOTION_CODE!r} and use_credits "
        f"returned {response.status_code} rather than a client error: "
        f"{response.text[:400]}"
    )


def test_ballot_is_recorded_for_a_member(member3_client):
    response = member3_client.post("/vote", json={"slug": "a-quiet-inventory"})
    assert response.status_code in (200, 201, 409), (
        f"POST /api/vote returned {response.status_code}: {response.text[:400]}"
    )
    read_back = member3_client.get("/vote")
    assert read_back.status_code == 200, (
        f"GET /api/vote returned {read_back.status_code}: {read_back.text[:400]}"
    )
    assert "a-quiet-inventory" in flatten(read_back.json()), (
        f"GET /api/vote does not show the ballot that was cast: "
        f"{read_back.text[:400]}"
    )
    year = current_utc_year()
    assert year in flatten(read_back.json()), (
        f"GET /api/vote names no round for the current UTC year {year}: "
        f"{read_back.text[:400]}"
    )


def test_second_ballot_in_one_round_is_refused(member3_client, db):
    member3_client.post("/vote", json={"slug": "a-quiet-inventory"})
    member = db.member_by_email(MEMBER3_EMAIL)
    assert member, f"no seeded member row for {MEMBER3_EMAIL}"
    response = member3_client.post("/vote", json={"slug": "every-third-tuesday"})
    assert 400 <= response.status_code < 500, (
        f"a second POST /api/vote in one round returned {response.status_code} "
        f"rather than a client error: {response.text[:400]}"
    )
    assert db.count_ballots(member_id=member["id"]) == 1, (
        f"member {MEMBER3_EMAIL} holds more than one ballot in the open round"
    )


def test_address_check_names_a_po_box_as_unservable(anon_client):
    response = anon_client.post("/addresses/check", json={
        "line1": "PO Box 4417", "city": "Boise", "region": "ID",
        "postal_code": "83701", "country": "US"})
    assert response.status_code == 200, (
        f"POST /api/addresses/check returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    assert SPECIAL_ADDRESS_COPY.lower() in flatten(response.json()), (
        f"a PO box address was not named as one the ordinary flow cannot serve: "
        f"{response.text[:400]}"
    )




def test_placed_box_is_persisted_with_its_pricing_snapshot(member_client, db):
    member = db.member_by_email(MEMBER_EMAIL)
    assert member, f"no seeded member row for {MEMBER_EMAIL}"
    build_box(member_client, ("the-orrery-thief", "salt-and-static"))
    response = place_box(member_client)
    assert response.status_code in (200, 201), (
        f"POST /api/box/place returned {response.status_code}: {response.text[:400]}"
    )
    settle()
    placed = db.boxes_for(member["id"], state="placed")
    assert placed, (
        f"no box row in state placed for {MEMBER_EMAIL} after a successful placement"
    )
    wrong_base = [b for b in placed if b.get("base_minor") != US_BASE_MINOR]
    assert not wrong_base, (
        f"{len(wrong_base)} placed box(es) for {MEMBER_EMAIL} stored a base_minor "
        f"other than the {US_BASE_MINOR} that applied when they were placed: "
        f"{[b.get('base_minor') for b in wrong_base][:3]}"
    )
    wrong_extra = [b for b in placed if b.get("extra_minor") != US_EXTRA_MINOR]
    assert not wrong_extra, (
        f"{len(wrong_extra)} placed box(es) for {MEMBER_EMAIL} stored an "
        f"extra_minor other than {US_EXTRA_MINOR}: "
        f"{[b.get('extra_minor') for b in wrong_extra][:3]}"
    )


def test_repeat_placement_stores_no_second_order_row(member_client, db):
    member = db.member_by_email(MEMBER_EMAIL)
    assert member, f"no seeded member row for {MEMBER_EMAIL}"
    build_box(member_client, ("the-orrery-thief",))
    first = place_box(member_client)
    assert first.status_code in (200, 201), (
        f"POST /api/box/place returned {first.status_code}: {first.text[:400]}"
    )
    settle()
    before = db.count_orders(member_id=member["id"])
    second = place_box(member_client)
    assert second.status_code in (200, 201, 409), (
        f"a repeated POST /api/box/place returned {second.status_code}: "
        f"{second.text[:400]}"
    )
    settle()
    after = db.count_orders(member_id=member["id"])
    assert after == before, (
        f"a repeated placement created a second order row for {MEMBER_EMAIL}: "
        f"{before} before, {after} after"
    )


def test_credit_ledger_row_is_stored_for_a_spend(member2_client, db):
    member = db.member_by_email(MEMBER2_EMAIL)
    assert member, f"no seeded member row for {MEMBER2_EMAIL}"
    build_box(member2_client, ("the-orrery-thief",))
    response = member2_client.post("/box/place", json={"use_credits": True})
    assert response.status_code in (200, 201), (
        f"POST /api/box/place with use_credits returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    settle()
    spends = db.ledger_for(member["id"], reason="spent_on_order")
    assert spends, (
        f"no credit_ledger row with reason spent_on_order for {MEMBER2_EMAIL} "
        f"after a placement that applied a credit"
    )
    assert all(row.get("delta", 0) < 0 for row in spends), (
        f"a spent_on_order ledger row carries a non-negative delta: {spends[:2]}"
    )


def test_unchosen_cycle_credit_is_seeded_once(db):
    member = db.member_by_email(MEMBER3_EMAIL)
    assert member, f"no seeded member row for {MEMBER3_EMAIL}"
    banked = db.ledger_for(member["id"], reason="unchosen_cycle")
    assert len(banked) == 1, (
        f"{MEMBER3_EMAIL} carries {len(banked)} unchosen_cycle ledger rows rather "
        f"than exactly one; the grant is once per member per cycle"
    )


def test_postcard_credit_is_seeded_for_the_canada_member(db):
    member = db.member_by_email(MEMBER2_EMAIL)
    assert member, f"no seeded member row for {MEMBER2_EMAIL}"
    earned = db.ledger_for(member["id"], reason="postcard_challenge")
    assert earned, (
        f"no credit_ledger row with reason postcard_challenge for {MEMBER2_EMAIL}"
    )


def test_seeded_editions_are_stored_exactly_once(db):
    for slug in list(CURRENT_SLUGS) + list(PREVIOUS_SLUGS) + list(BACKLIST_SLUGS):
        found = db.count_editions(slug=slug)
        assert found == 1, (
            f"the editions table holds {found} rows for slug {slug!r}; seeding is "
            f"idempotent and a restart must not duplicate a row"
        )


def test_reprint_and_original_are_separate_rows(db):
    original = db.edition_by_slug("salt-and-static")
    reprint = db.edition_by_slug("salt-and-static-reprint")
    assert original, "no editions row for slug 'salt-and-static'"
    assert reprint, "no editions row for slug 'salt-and-static-reprint'"
    assert original["id"] != reprint["id"], (
        "salt-and-static and salt-and-static-reprint resolve to one editions row; "
        "they are two editions of one work"
    )
    assert original.get("work_id") == reprint.get("work_id"), (
        f"salt-and-static and salt-and-static-reprint carry different work_id "
        f"values ({original.get('work_id')!r} and {reprint.get('work_id')!r}); "
        f"they are the same work"
    )


def test_cover_hue_is_stored_and_does_not_move_between_reads(anon_client, db):
    row = db.edition_by_slug("the-orrery-thief")
    assert row, "no editions row for slug 'the-orrery-thief'"
    stored = row.get("cover_hue")
    assert stored, (
        "the editions row for the-orrery-thief carries no cover_hue; the hue is "
        "derived once when the edition is created and stored"
    )
    first = anon_client.get("/editions/the-orrery-thief")
    second = anon_client.get("/editions/the-orrery-thief")
    assert first.status_code == 200 and second.status_code == 200, (
        f"GET /api/editions/the-orrery-thief returned {first.status_code} then "
        f"{second.status_code}: {first.text[:200]}"
    )
    assert str(stored).lower() in flatten(first.json()), (
        f"the edition response does not carry the stored cover_hue {stored!r}: "
        f"{first.text[:400]}"
    )
    assert flatten(first.json()) == flatten(second.json()), (
        "two reads of one edition returned different payloads, so the cover hue is "
        "being recomputed per render rather than stored"
    )


def test_country_pricing_is_stored_once_per_country(db):
    us = db.pricing_for("US")
    ca = db.pricing_for("CA")
    assert us, "no country_pricing row for US"
    assert ca, "no country_pricing row for CA"
    assert us.get("base_minor") == US_BASE_MINOR, (
        f"country_pricing US base_minor is {us.get('base_minor')!r} rather than "
        f"{US_BASE_MINOR}"
    )
    assert us.get("extra_minor") == US_EXTRA_MINOR, (
        f"country_pricing US extra_minor is {us.get('extra_minor')!r} rather than "
        f"{US_EXTRA_MINOR}"
    )
    assert ca.get("base_minor") == CA_BASE_MINOR, (
        f"country_pricing CA base_minor is {ca.get('base_minor')!r} rather than "
        f"{CA_BASE_MINOR}"
    )
    assert str(us.get("currency", "")).lower() == USD, (
        f"country_pricing US currency is {us.get('currency')!r} rather than {USD!r}"
    )
    assert str(ca.get("currency", "")).lower() == CAD, (
        f"country_pricing CA currency is {ca.get('currency')!r} rather than {CAD!r}"
    )


def test_concurrent_placement_yields_exactly_one_order_row(member_client, db):
    member = db.member_by_email(MEMBER_EMAIL)
    assert member, f"no seeded member row for {MEMBER_EMAIL}"
    build_box(member_client, ("nine-yards-of-night",))
    before = db.count_orders(member_id=member["id"])
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(place_box, member_client) for _ in range(2)]
        codes = [f.result().status_code for f in futures]
    settle()
    after = db.count_orders(member_id=member["id"])
    assert after - before == 1, (
        f"two simultaneous placements of one box created {after - before} order "
        f"rows rather than exactly one; the responses were {codes}"
    )


def test_gift_code_is_redeemed_at_most_once(anon_client, db, probe_email):
    created = anon_client.post("/auth/signup", json=signup_payload(probe_email))
    assert created.status_code in (200, 201), (
        f"POST /api/auth/signup for {probe_email} returned {created.status_code}: "
        f"{created.text[:400]}"
    )
    token = created.json().get("access_token") or created.json().get("token")
    assert token, (
        f"POST /api/auth/signup returned no bearer token: {created.text[:400]}"
    )
    with make_client(token) as redeemer:
        first = redeemer.post("/gifts/redeem", json={"code": SEEDED_GIFT_CODE})
        assert first.status_code in (200, 201), (
            f"the first POST /api/gifts/redeem of {SEEDED_GIFT_CODE} returned "
            f"{first.status_code}: {first.text[:400]}"
        )
        second = redeemer.post("/gifts/redeem", json={"code": SEEDED_GIFT_CODE})
        assert 400 <= second.status_code < 500, (
            f"a second POST /api/gifts/redeem of {SEEDED_GIFT_CODE} returned "
            f"{second.status_code} rather than a client error: {second.text[:400]}"
        )
    settle()
    gift = db.gift_by_code(SEEDED_GIFT_CODE)
    assert gift and gift.get("redeemed_by_member_id"), (
        f"the gifts row for {SEEDED_GIFT_CODE} records no redeemer after a "
        f"successful redemption: {gift}"
    )




def test_anonymous_box_request_is_denied(anon_client):
    response = anon_client.get("/box")
    assert response.status_code in (401, 403), (
        f"GET /api/box without a token returned {response.status_code} rather "
        f"than a denial: {response.text[:400]}"
    )


def test_anonymous_placement_is_denied_and_writes_nothing(anon_client, db):
    member = db.member_by_email(MEMBER_EMAIL)
    assert member, f"no seeded member row for {MEMBER_EMAIL}"
    before = db.count_orders(member_id=member["id"])
    response = anon_client.post("/box/place", json={})
    assert response.status_code in (401, 403), (
        f"POST /api/box/place without a token returned {response.status_code} "
        f"rather than a denial: {response.text[:400]}"
    )
    settle()
    assert db.count_orders(member_id=member["id"]) == before, (
        "a denied anonymous placement changed the order rows"
    )


def test_member_cannot_read_another_members_orders(member_client, member2_client, db):
    owner = db.member_by_email(MEMBER_EMAIL)
    assert owner, f"no seeded member row for {MEMBER_EMAIL}"
    build_box(member_client, ("the-orrery-thief",))
    placed = place_box(member_client)
    assert placed.status_code in (200, 201), (
        f"POST /api/box/place returned {placed.status_code}: {placed.text[:400]}"
    )
    settle()
    response = member2_client.get("/orders")
    assert response.status_code == 200, (
        f"GET /api/orders returned {response.status_code}: {response.text[:400]}"
    )
    blob = flatten(items(response.json()))
    assert MEMBER_EMAIL not in blob, (
        f"GET /api/orders for {MEMBER2_EMAIL} carries rows belonging to "
        f"{MEMBER_EMAIL}: {response.text[:400]}"
    )


def test_member_cannot_read_another_members_credit_ledger(member2_client, db):
    other = db.member_by_email(MEMBER3_EMAIL)
    assert other, f"no seeded member row for {MEMBER3_EMAIL}"
    response = member2_client.get("/credits")
    assert response.status_code == 200, (
        f"GET /api/credits returned {response.status_code}: {response.text[:400]}"
    )
    assert MEMBER3_EMAIL not in flatten(response.json()), (
        f"GET /api/credits for {MEMBER2_EMAIL} exposes {MEMBER3_EMAIL}: "
        f"{response.text[:400]}"
    )


def test_gift_buyer_cannot_read_the_recipients_box(member_client, anon_client, probe_email):
    issued = member_client.post("/gifts", json={"recipient_email": probe_email})
    assert issued.status_code in (200, 201), (
        f"POST /api/gifts returned {issued.status_code}: {issued.text[:400]}"
    )
    code = issued.json().get("code")
    assert code, f"POST /api/gifts returned no code: {issued.text[:400]}"
    created = anon_client.post("/auth/signup", json=signup_payload(probe_email))
    assert created.status_code in (200, 201), (
        f"POST /api/auth/signup for {probe_email} returned {created.status_code}: "
        f"{created.text[:400]}"
    )
    token = created.json().get("access_token") or created.json().get("token")
    assert token, f"POST /api/auth/signup returned no bearer token: {created.text[:400]}"
    with make_client(token) as recipient:
        redeemed = recipient.post("/gifts/redeem", json={"code": code})
        assert redeemed.status_code in (200, 201), (
            f"POST /api/gifts/redeem returned {redeemed.status_code}: "
            f"{redeemed.text[:400]}"
        )
        build_box(recipient, ("the-marmalade-conspiracy",))
    buyer_view = member_client.get("/box", params={"member": probe_email})
    assert "the-marmalade-conspiracy" not in flatten(buyer_view.json()), (
        f"the gift buyer can read the recipient's box: {buyer_view.text[:400]}"
    )




def test_signup_with_an_unsupported_country_is_refused(anon_client, db, probe_email):
    before = db.count_members(email=probe_email)
    response = anon_client.post("/auth/signup", json={
        "email": probe_email, "password": SEED_PASSWORD, "country": "FR"})
    assert 400 <= response.status_code < 500, (
        f"POST /api/auth/signup with country FR returned {response.status_code} "
        f"rather than a client error: {response.text[:400]}"
    )
    settle()
    assert db.count_members(email=probe_email) == before, (
        f"a refused signup wrote a members row for {probe_email}"
    )


def test_signup_with_a_malformed_email_writes_nothing(anon_client, db, probe_token):
    bad = f"not-an-address-{probe_token}"
    response = anon_client.post("/auth/signup", json={
        "email": bad, "password": SEED_PASSWORD, "country": "US"})
    assert 400 <= response.status_code < 500, (
        f"POST /api/auth/signup with a malformed email returned "
        f"{response.status_code} rather than a client error: {response.text[:400]}"
    )
    settle()
    assert db.count_members(email=bad) == 0, (
        f"a refused signup wrote a members row for {bad!r}"
    )


def test_unknown_edition_slug_is_not_found(anon_client):
    response = anon_client.get("/editions/no-such-edition-at-all")
    assert response.status_code == 404, (
        f"GET /api/editions/no-such-edition-at-all returned "
        f"{response.status_code} rather than 404: {response.text[:400]}"
    )


def test_duplicate_edition_in_one_box_is_refused(member_client):
    build_box(member_client, ("the-orrery-thief",))
    response = add_to_box(member_client, "the-orrery-thief")
    assert response.status_code in (200, 400, 409, 422), (
        f"a repeated POST /api/box/items for the-orrery-thief returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    after = member_client.get("/box")
    slugs = _slugs_of(after.json())
    assert slugs.count("the-orrery-thief") == 1, (
        f"the-orrery-thief appears {slugs.count('the-orrery-thief')} times in one "
        f"box: {after.text[:400]}"
    )




def test_placed_box_delivers_a_confirmation_email(member_client, inbox):
    build_box(member_client, ("every-third-tuesday",))
    response = place_box(member_client)
    assert response.status_code in (200, 201), (
        f"POST /api/box/place returned {response.status_code}: {response.text[:400]}"
    )
    settle(5.0)
    message = inbox.find(MEMBER_EMAIL, subject_contains=CONFIRMATION_SUBJECT_PREFIX)
    assert message is not None, (
        f"no message whose subject begins {CONFIRMATION_SUBJECT_PREFIX!r} reached "
        f"{MEMBER_EMAIL} after a successful placement"
    )
    assert message.subject.startswith(CONFIRMATION_SUBJECT_PREFIX), (
        f"the confirmation subject is {message.subject!r} and does not begin "
        f"{CONFIRMATION_SUBJECT_PREFIX!r}"
    )
    assert message.body.strip(), (
        f"the confirmation message to {MEMBER_EMAIL} carries an empty body"
    )
    for other in (MEMBER2_EMAIL, MEMBER3_EMAIL):
        stray = inbox.find(other, subject_contains=CONFIRMATION_SUBJECT_PREFIX)
        assert stray is None or stray.subject != message.subject, (
            f"the confirmation addressed to {MEMBER_EMAIL} also reached {other}; "
            f"the message carries no cc and no bcc"
        )


def test_refused_placement_delivers_no_confirmation_email(member2_client, inbox):
    before = inbox.count(MEMBER2_EMAIL)
    build_box(member2_client, ("the-glass-cartographer",))
    response = place_box(member2_client)
    assert 400 <= response.status_code < 500, (
        f"POST /api/box/place on an invalid box returned {response.status_code} "
        f"rather than a client error: {response.text[:400]}"
    )
    settle(5.0)
    assert inbox.count(MEMBER2_EMAIL) == before, (
        f"a refused placement sent mail to {MEMBER2_EMAIL}: {before} messages "
        f"before, {inbox.count(MEMBER2_EMAIL)} after"
    )


def test_gift_purchase_delivers_an_e_gift_card_email(member_client, inbox, probe_email):
    response = member_client.post("/gifts", json={"recipient_email": probe_email})
    assert response.status_code in (200, 201), (
        f"POST /api/gifts returned {response.status_code}: {response.text[:400]}"
    )
    code = response.json().get("code")
    assert code, f"POST /api/gifts returned no code: {response.text[:400]}"
    settle(5.0)
    message = inbox.find(MEMBER_EMAIL, subject_contains=GIFT_SUBJECT_PREFIX)
    assert message is not None, (
        f"no message whose subject begins {GIFT_SUBJECT_PREFIX!r} reached the "
        f"buyer {MEMBER_EMAIL} after a gift purchase"
    )
    assert code in message.body or code in message.subject, (
        f"the e-gift card message names no code; subject {message.subject!r}"
    )




def test_placed_box_creates_a_billing_charge_for_the_total(member_client, payments):
    build_box(member_client, ("the-orrery-thief", "salt-and-static", "a-quiet-inventory"))
    response = place_box(member_client)
    assert response.status_code in (200, 201), (
        f"POST /api/box/place returned {response.status_code}: {response.text[:400]}"
    )
    settle(5.0)
    charge = payments.find_charge(US_THREE_BOOK_TOTAL, currency=USD)
    assert charge is not None, (
        f"no invoice for {US_THREE_BOOK_TOTAL} minor units ({US_INVOICE_DECIMAL} "
        f"{US_INVOICE_CURRENCY}) exists in killbill after a three-book US order; "
        f"the app's own tables cannot substitute for the billing platform"
    )


def test_repeat_checkout_creates_no_second_billing_charge(member_client, payments):
    build_box(member_client, ("the-marmalade-conspiracy", "salt-and-static"))
    first = place_box(member_client)
    assert first.status_code in (200, 201), (
        f"POST /api/box/place returned {first.status_code}: {first.text[:400]}"
    )
    settle(5.0)
    before = len([c for c in payments.charges() if c.amount == US_TWO_BOOK_TOTAL])
    second = place_box(member_client)
    assert second.status_code in (200, 201, 409), (
        f"a repeated POST /api/box/place returned {second.status_code}: "
        f"{second.text[:400]}"
    )
    settle(5.0)
    after = len([c for c in payments.charges() if c.amount == US_TWO_BOOK_TOTAL])
    assert after == before, (
        f"a repeated checkout created a second invoice for {US_TWO_BOOK_TOTAL} "
        f"minor units: {before} before, {after} after"
    )


def test_member_has_exactly_one_billing_account(member_client, payments, anon_client):
    anon_client.post("/auth/signup", json=signup_payload(MEMBER_EMAIL))
    settle()
    accounts = payments.accounts()
    keys = [str(a.get("externalKey", "")) for a in accounts]
    duplicated = [k for k in set(keys) if k and keys.count(k) > 1]
    assert not duplicated, (
        f"killbill holds more than one account for externalKey(s) {duplicated}; "
        f"the external key is unique per tenant and a re-submit creates no second "
        f"account"
    )




def test_privacy_page_is_served_and_linked_from_the_footer(anon_client):
    with httpx.Client(base_url=app_url(), timeout=30.0, follow_redirects=True) as web:
        page = web.get("/privacy-policy")
        assert page.status_code == 200, (
            f"GET /privacy-policy returned {page.status_code}: {page.text[:400]}"
        )
        home = web.get("/")
        assert home.status_code == 200, (
            f"GET / returned {home.status_code}: {home.text[:400]}"
        )
        assert "/privacy-policy" in home.text, (
            "the home page does not link to /privacy-policy from its footer"
        )


def test_terms_page_is_served_and_linked_from_the_footer(anon_client):
    with httpx.Client(base_url=app_url(), timeout=30.0, follow_redirects=True) as web:
        page = web.get("/terms-of-service")
        assert page.status_code == 200, (
            f"GET /terms-of-service returned {page.status_code}: {page.text[:400]}"
        )
        home = web.get("/")
        assert "/terms-of-service" in home.text, (
            "the home page does not link to /terms-of-service from its footer"
        )


def test_public_routes_declare_distinct_social_preview_titles(anon_client):
    titles = {}
    with httpx.Client(base_url=app_url(), timeout=30.0, follow_redirects=True) as web:
        for route in ("/", "/allbooks", "/gifting", "/faq"):
            page = web.get(route)
            assert page.status_code == 200, (
                f"GET {route} returned {page.status_code}: {page.text[:200]}"
            )
            found = _re.search(
                r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)',
                page.text, re.IGNORECASE)
            assert found, (
                f"GET {route} declares no social preview title in its head"
            )
            titles[route] = found.group(1).strip()
    duplicates = [t for t in set(titles.values()) if list(titles.values()).count(t) > 1]
    assert not duplicates, (
        f"two public routes share the social preview title(s) {duplicates}: {titles}"
    )


def test_catalogue_copy_states_the_open_genre_list(anon_client):
    with httpx.Client(base_url=app_url(), timeout=30.0, follow_redirects=True) as web:
        page = web.get("/allbooks")
        assert page.status_code == 200, (
            f"GET /allbooks returned {page.status_code}: {page.text[:400]}"
        )
        assert "and more!" in page.text, (
            "the catalogue does not carry the copy 'and more!' that closes its "
            "genre list"
        )
    response = anon_client.get("/editions", params={"genre": "and more!"})
    assert response.status_code != 200 or not items(response.json()), (
        "'and more!' is copy and must not behave as a genre a member can filter by"
    )


def test_seeded_accounts_sign_in_with_the_corpus_password(anon_client):
    for email in (MEMBER_EMAIL, MEMBER2_EMAIL, MEMBER3_EMAIL):
        response = anon_client.post(
            "/auth/login", json={"email": email, "password": SEED_PASSWORD})
        assert response.status_code == 200, (
            f"POST /api/auth/login for {email} returned {response.status_code}: "
            f"{response.text[:400]}"
        )
        token = response.json().get("access_token") or response.json().get("token")
        assert token, (
            f"POST /api/auth/login for {email} returned no bearer token: "
            f"{response.text[:400]}"
        )


def test_gift_purchaser_cannot_redeem_their_own_code(member_client, probe_email):
    issued = member_client.post("/gifts", json={"recipient_email": probe_email})
    assert issued.status_code in (200, 201), (
        f"POST /api/gifts returned {issued.status_code}: {issued.text[:400]}"
    )
    code = issued.json().get("code")
    assert code, f"POST /api/gifts returned no code: {issued.text[:400]}"
    response = member_client.post("/gifts/redeem", json={"code": code})
    assert 400 <= response.status_code < 500, (
        f"the purchaser's own POST /api/gifts/redeem returned "
        f"{response.status_code} rather than a client error: {response.text[:400]}"
    )


def test_gift_redeemed_by_a_member_creates_no_second_subscription(
        member_client, anon_client, db, probe_email):
    issued = member_client.post("/gifts", json={"recipient_email": probe_email})
    assert issued.status_code in (200, 201), (
        f"POST /api/gifts returned {issued.status_code}: {issued.text[:400]}"
    )
    code = issued.json().get("code")
    assert code, f"POST /api/gifts returned no code: {issued.text[:400]}"
    created = anon_client.post("/auth/signup", json=signup_payload(probe_email))
    assert created.status_code in (200, 201), (
        f"POST /api/auth/signup for {probe_email} returned {created.status_code}: "
        f"{created.text[:400]}"
    )
    token = created.json().get("access_token") or created.json().get("token")
    assert token, f"POST /api/auth/signup returned no bearer token: {created.text[:400]}"
    with make_client(token) as recipient:
        redeemed = recipient.post("/gifts/redeem", json={"code": code})
        assert redeemed.status_code in (200, 201), (
            f"POST /api/gifts/redeem returned {redeemed.status_code}: "
            f"{redeemed.text[:400]}"
        )
    settle()
    member = db.member_by_email(probe_email)
    assert member, f"no members row for {probe_email} after redemption"
    assert db.count_subscriptions(member_id=member["id"]) == 1, (
        f"{probe_email} holds more than one subscription row after redeeming a "
        f"gift as an existing member"
    )


def test_seeded_subscriptions_survive_a_failed_payment(db):
    for email in (MEMBER_EMAIL, MEMBER2_EMAIL, MEMBER3_EMAIL):
        member = db.member_by_email(email)
        assert member, f"no seeded members row for {email}"
        subscription = db.subscription_of(member["id"])
        assert subscription, f"no subscriptions row for {email}"
        assert subscription.get("state") in ("active", "paused"), (
            f"the subscription for {email} is in state "
            f"{subscription.get('state')!r}; a failed payment pauses a membership "
            f"rather than deleting the account"
        )
        assert db.count_members(email=email) == 1, (
            f"the members row for {email} was removed"
        )


def test_cancelled_membership_ends_at_the_close_of_the_paid_cycle(member3_client, db):
    member = db.member_by_email(MEMBER3_EMAIL)
    assert member, f"no seeded members row for {MEMBER3_EMAIL}"
    build_box(member3_client, ("nine-yards-of-night",))
    placed = place_box(member3_client)
    assert placed.status_code in (200, 201), (
        f"POST /api/box/place returned {placed.status_code}: {placed.text[:400]}"
    )
    settle()
    response = member3_client.post("/account/cancel", json={})
    assert response.status_code in (200, 202, 204), (
        f"POST /api/account/cancel returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    settle()
    subscription = db.subscription_of(member["id"])
    assert subscription and subscription.get("ends_at"), (
        f"cancelling set no ends_at on the subscription for {MEMBER3_EMAIL}: "
        f"{subscription}"
    )
    assert subscription.get("state") != "canceled", (
        f"the subscription for {MEMBER3_EMAIL} is already canceled; cancellation "
        f"takes effect at the close of the paid cycle"
    )
    boxes = db.boxes_for(member["id"], state="placed")
    assert boxes, (
        f"the box placed by {MEMBER3_EMAIL} before cancelling is no longer in "
        f"state placed; a box already placed still ships"
    )


def test_credit_spend_beyond_the_balance_is_refused(member_client, db):
    member = db.member_by_email(MEMBER_EMAIL)
    assert member, f"no seeded members row for {MEMBER_EMAIL}"
    build_box(member_client, ("the-orrery-thief", "salt-and-static"))
    response = member_client.post("/box/place", json={"use_credits": True})
    assert response.status_code in (200, 201, 400, 409, 422), (
        f"POST /api/box/place with use_credits from a member holding no credits "
        f"returned {response.status_code}: {response.text[:400]}"
    )
    settle()
    balance = sum(row.get("delta", 0) for row in db.ledger_for(member["id"]))
    assert balance >= 0, (
        f"the credit balance for {MEMBER_EMAIL} is {balance}, which is below zero"
    )


def test_failed_placement_leaves_no_order_and_no_credit_row(member2_client, db):
    member = db.member_by_email(MEMBER2_EMAIL)
    assert member, f"no seeded members row for {MEMBER2_EMAIL}"
    orders_before = db.count_orders(member_id=member["id"])
    ledger_before = db.count_ledger(member_id=member["id"])
    boxes_before = db.count_boxes(member_id=member["id"], state="placed")
    build_box(member2_client, ("the-glass-cartographer",))
    response = member2_client.post("/box/place", json={"use_credits": True})
    assert 400 <= response.status_code < 500, (
        f"POST /api/box/place on an invalid box returned {response.status_code} "
        f"rather than a client error: {response.text[:400]}"
    )
    settle()
    assert db.count_orders(member_id=member["id"]) == orders_before, (
        "a refused placement created an order row"
    )
    assert db.count_ledger(member_id=member["id"]) == ledger_before, (
        "a refused placement wrote a credit ledger row"
    )
    assert db.count_boxes(member_id=member["id"], state="placed") == boxes_before, (
        "a refused placement moved a box into state placed"
    )


def test_member_keeps_at_most_one_building_box_per_cycle(member_client, db):
    member = db.member_by_email(MEMBER_EMAIL)
    assert member, f"no seeded members row for {MEMBER_EMAIL}"
    build_box(member_client, ("the-orrery-thief",))
    add_to_box(member_client, "salt-and-static")
    settle()
    building = db.boxes_for(member["id"], state="building")
    assert len(building) <= 1, (
        f"{MEMBER_EMAIL} holds {len(building)} boxes in state building; at most "
        f"one box is open per member per cycle"
    )


def test_concurrent_fourth_addition_is_refused_twice(member_client, db):
    build_box(member_client, ("the-orrery-thief", "salt-and-static", "nine-yards-of-night"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(add_to_box, member_client, slug)
                   for slug in ("every-third-tuesday", "a-quiet-inventory")]
        codes = [f.result().status_code for f in futures]
    settle()
    after = member_client.get("/box")
    slugs = _slugs_of(after.json())
    assert len(slugs) == 3, (
        f"two simultaneous fourth additions left {len(slugs)} items in the box "
        f"rather than three; the responses were {codes}: {after.text[:400]}"
    )


def test_concurrent_ballots_record_exactly_one(member2_client, db):
    member = db.member_by_email(MEMBER2_EMAIL)
    assert member, f"no seeded members row for {MEMBER2_EMAIL}"
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(member2_client.post, "/vote", json={"slug": slug})
                   for slug in ("a-quiet-inventory", "every-third-tuesday")]
        codes = [f.result().status_code for f in futures]
    settle()
    assert db.count_ballots(member_id=member["id"]) == 1, (
        f"two simultaneous ballots by {MEMBER2_EMAIL} left "
        f"{db.count_ballots(member_id=member['id'])} rows rather than one; the "
        f"responses were {codes}"
    )


def test_concurrent_gift_redemptions_succeed_at_most_once(anon_client, db, probe_email):
    created = anon_client.post("/auth/signup", json=signup_payload(probe_email))
    assert created.status_code in (200, 201), (
        f"POST /api/auth/signup for {probe_email} returned {created.status_code}: "
        f"{created.text[:400]}"
    )
    token = created.json().get("access_token") or created.json().get("token")
    assert token, f"POST /api/auth/signup returned no bearer token: {created.text[:400]}"
    issuer = anon_client.post("/auth/login", json={
        "email": MEMBER_EMAIL, "password": SEED_PASSWORD})
    assert issuer.status_code == 200, (
        f"POST /api/auth/login returned {issuer.status_code}: {issuer.text[:400]}"
    )
    buyer_token = issuer.json().get("access_token") or issuer.json().get("token")
    with make_client(buyer_token) as buyer:
        issued = buyer.post("/gifts", json={"recipient_email": probe_email})
        assert issued.status_code in (200, 201), (
            f"POST /api/gifts returned {issued.status_code}: {issued.text[:400]}"
        )
        code = issued.json().get("code")
    assert code, "POST /api/gifts returned no code"
    with make_client(token) as redeemer:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(redeemer.post, "/gifts/redeem", json={"code": code})
                       for _ in range(2)]
            codes = [f.result().status_code for f in futures]
    accepted = [c for c in codes if c in (200, 201)]
    assert len(accepted) <= 1, (
        f"two simultaneous redemptions of one gift code both succeeded: {codes}"
    )


def test_home_page_arrives_as_complete_html(anon_client):
    with httpx.Client(base_url=app_url(), timeout=30.0, follow_redirects=True) as web:
        page = web.get("/")
        assert page.status_code == 200, (
            f"GET / returned {page.status_code}: {page.text[:400]}"
        )
        body = page.text.lower()
        found = [slug for slug in CURRENT_SLUGS if slug in body]
        assert found, (
            f"GET / returned no current edition in its HTML, so the first paint is "
            f"an empty shell the browser has to fill: {page.text[:400]}"
        )
        catalogue = web.get("/allbooks")
        assert catalogue.status_code == 200, (
            f"GET /allbooks returned {catalogue.status_code}: {catalogue.text[:400]}"
        )
        assert any(slug in catalogue.text.lower() for slug in CURRENT_SLUGS), (
            f"GET /allbooks returned no edition in its HTML: {catalogue.text[:400]}"
        )


def test_placed_order_timestamp_is_recorded_in_utc(member_client, db):
    member = db.member_by_email(MEMBER_EMAIL)
    assert member, f"no seeded members row for {MEMBER_EMAIL}"
    build_box(member_client, ("the-marmalade-conspiracy",))
    placed = place_box(member_client)
    assert placed.status_code in (200, 201), (
        f"POST /api/box/place returned {placed.status_code}: {placed.text[:400]}"
    )
    settle()
    orders = db.orders_for(member["id"])
    assert orders, f"no orders row for {MEMBER_EMAIL} after a successful placement"
    bad = []
    for row in orders:
        stamp = row.get("placed_at")
        if stamp is None:
            bad.append(row)
            continue
        offset = getattr(stamp, "utcoffset", lambda: None)()
        text = str(stamp)
        utc = (offset is not None and offset.total_seconds() == 0) or text.endswith("+00:00") or text.endswith("Z")
        if not utc:
            bad.append(row)
    assert not bad, (
        f"{len(bad)} of {len(orders)} orders rows for {MEMBER_EMAIL} carry a "
        f"placed_at with no UTC offset, first {str(bad[0].get('placed_at'))!r}; "
        f"every timestamp is stored in UTC"
    )
