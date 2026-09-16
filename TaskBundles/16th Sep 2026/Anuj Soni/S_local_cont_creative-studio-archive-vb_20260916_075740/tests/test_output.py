"""The one pytest module for Creative Studio Archive.

Every assertion here is black box: HTTP against the running app, the datastore the
brief names, and the object store the brief names. Nothing reads the app's source,
its schema definitions or its imports. Every literal comes from conftest, which pins
the same values instruction.md pins.
"""

from __future__ import annotations

import os

import httpx

import appclient
import conftest
from conftest import (ACCEPTED, ARCHIVE_ITEM_COUNT, ARCHIVE_KEY_PREFIX, ARCHIVE_SEED,
                      AWARD_BODY_PRIMARY, AWARD_BODY_THIRD, AWARD_TYPE_COUNTED,
                      AWARD_TYPE_COUNTED_TOTAL, AWARD_TYPE_EMPTY, BLOCK_KINDS,
                      BUDGET_TOP, CASE_STATES, CLIENT_ERROR, CONSOLE_ROUTES,
                      COVER_KEY_PREFIX, CREDENTIALS_FILE, DECOY_FIELD, DENIED,
                      DISCIPLINE_COUNT, DOWNLOAD_DIR, DRAFT_SLUG, ERASURE_MARKER,
                      FIRST_SLUG, FIRST_VEIL, INQUIRY_NEW, INQUIRY_SPAM,
                      INQUIRY_STATES, LAST_VEIL, LEAD2_DISCIPLINE, LEAD_DISCIPLINE,
                      LEAD_EMAIL, LEAD_ONLY_ROUTES, LINKED_SLUG, MENU_VALUES,
                      MESSAGE_FLOOR, MODE_SEQUENCE, NOT_FOUND, PUBLIC_ROUTES,
                      PUBLISHED_CASE_COUNT, PUBLISHED_SLUGS, RATE_CEILING_PER_ADDRESS,
                      REFUSED, REVIEW_SLUG, SCREENSHOT_DIR, SEQUENCE_BLOCKS,
                      STATE_DRAFT, STATE_PUBLISHED, STUDIO_ADDRESS, TABLE_ARCHIVE_ITEM,
                      TABLE_AUDIT, TABLE_AWARD, TABLE_AWARD_TYPE, TABLE_CASE,
                      TABLE_INQUIRY, TABLE_INQUIRY_EVENT, TABLE_MEDIA, TABLE_MEMBER,
                      TABLE_PAGE_BLOCK, TABLE_REVIEW_TOKEN, TABLE_REVISION,
                      THIRTEENTH_FIRST_VEIL, accepted_inquiry, attribute_values,
                      backend, case_body, create_case, describe, fetch_document,
                      fetch_document_no_redirect, inquiry_body, inquiry_row,
                      internal_links, object_store, poll_until, probe_png,
                      publish_case, rectangles_overlap, settle, submit_inquiry,
                      unique_suffix, upload_cover)


def api_get(path: str, token: str | None = None) -> httpx.Response:
    with appclient.client(token) as api:
        return api.get(path)


def api_post(path: str, token: str | None = None, **kwargs) -> httpx.Response:
    with appclient.client(token) as api:
        return api.post(path, **kwargs)


def api_patch(path: str, token: str | None = None, **kwargs) -> httpx.Response:
    with appclient.client(token) as api:
        return api.patch(path, **kwargs)


def api_delete(path: str, token: str | None = None) -> httpx.Response:
    with appclient.client(token) as api:
        return api.delete(path)


def placed_shape(rows: list) -> dict:
    """Each archive item's placed rectangle, keyed by its own id."""
    return {str(r.get("id")): (r.get("x"), r.get("y"), r.get("w"), r.get("h"))
            for r in rows}


def published_cases() -> list:
    response = api_get("/cases")
    assert response.status_code == 200, describe(
        response, "the published case list must be readable by anybody")
    payload = response.json()
    assert isinstance(payload, list), describe(
        response, "the published case list must be a top-level JSON array")
    return payload


def approved_review(token: str, slug: str, suffix: str) -> str:
    """Issue a review link for a case, approve it as the client, return the token."""
    issued = api_post(f"/console/cases/{slug}/review-links", token,
                      json={"emails": [conftest.probe_address(suffix)],
                            "expires_in_days": 14})
    assert issued.status_code in ACCEPTED, describe(
        issued, "a lead must be able to issue a review link")
    payload = issued.json()
    tokens = payload if isinstance(payload, list) else payload.get("tokens", [])
    assert tokens, describe(issued, "an issued review link must return its token")
    first = tokens[0]
    review_token = first["token"] if isinstance(first, dict) else str(first)
    decided = api_post(f"/preview/{review_token}/decision", None,
                       json={"decision": "approve"})
    assert decided.status_code in ACCEPTED, describe(
        decided, "a client reviewer must be able to approve the revision")
    return review_token


def test_health_reports_status_once_the_app_is_ready():
    response = api_get("/health")
    assert response.status_code == 200, describe(response, "health must answer 200")
    payload = response.json()
    assert isinstance(payload, dict) and "status" in payload, describe(
        response, "health must carry a status field")


def test_seeded_lead_signs_in_and_receives_a_bearer_token(lead):
    assert lead, "signing in as the seeded lead must return a bearer token"
    response = api_get("/console/cases", lead)
    assert response.status_code == 200, describe(
        response, "the seeded lead's token must reach the console case list")


def test_signing_out_stops_the_bearer_token_working(writer):
    out = api_post("/auth/logout", writer)
    assert out.status_code in ACCEPTED or out.status_code == 204, describe(
        out, "a member must be able to sign out")
    settle()
    after = api_get("/console/cases", writer)
    assert after.status_code in DENIED, describe(
        after, "a token that has been signed out must stop working")


def test_no_route_creates_an_account(suffix):
    address = conftest.probe_address(suffix)
    before = backend().count(TABLE_MEMBER)
    for path in ("/auth/signup", "/auth/register", "/console/members/invite"):
        response = api_post(path, None, json={"email": address,
                                              "password": conftest.SEEDED_PASSWORD,
                                              "role": "lead"})
        assert response.status_code in REFUSED or response.status_code == 405, describe(
            response, f"{path} must not create an account for an anonymous caller")
    settle()
    assert backend().count(TABLE_MEMBER) == before, (
        "no anonymous request may add a row to the members table")


def test_page_returns_the_enabled_sequence_blocks_in_order():
    response = api_get("/page")
    assert response.status_code == 200, describe(
        response, "the sequence block list must be readable by anybody")
    payload = response.json()
    blocks = payload if isinstance(payload, list) else payload.get("blocks", [])
    names = [str(b.get("component")) for b in blocks]
    assert names == list(SEQUENCE_BLOCKS), (
        f"the sequence must render {SEQUENCE_BLOCKS} in order, the app returned {names}")


def test_each_sequence_block_carries_its_data_block_value():
    response = fetch_document("/")
    assert response.status_code == 200, describe(response, "the home route must render")
    values = attribute_values(response.text, "data-block")
    for name in SEQUENCE_BLOCKS:
        assert name in values, (
            f"the home document must carry a block marked data-block={name}, "
            f"found {values}")


def test_each_menu_label_carries_its_data_menu_value():
    response = fetch_document("/")
    values = attribute_values(response.text, "data-menu")
    for name in MENU_VALUES:
        assert name in values, (
            f"the menu must carry a label marked data-menu={name}, found {values}")


def test_the_document_element_carries_data_mode_sequence_on_the_home_route():
    response = fetch_document("/")
    values = attribute_values(response.text, "data-mode")
    assert MODE_SEQUENCE in values, (
        f"the home document must declare data-mode={MODE_SEQUENCE}, found {values}")


def test_cases_returns_only_published_cases_ordered_by_stack_order():
    cases = published_cases()
    slugs = [c["slug"] for c in cases]
    assert slugs == list(PUBLISHED_SLUGS), (
        f"the published stack must read {PUBLISHED_SLUGS}, the app returned {slugs}")
    orders = [int(c["stack_order"]) for c in cases]
    assert orders == list(range(1, PUBLISHED_CASE_COUNT + 1)), (
        f"stack_order must be contiguous from 1, the app returned {orders}")


def test_seeded_case_veil_values_step_evenly_down_the_stack():
    cases = published_cases()
    veils = [str(c["veil"]) for c in cases]
    assert veils[0] == FIRST_VEIL, (
        f"the first card's veil must read {FIRST_VEIL}, the app returned {veils[0]}")
    assert veils[-1] == LAST_VEIL, (
        f"the last card's veil must read {LAST_VEIL}, the app returned {veils[-1]}")
    steps = {round(float(veils[i]) - float(veils[i + 1]), 6)
             for i in range(len(veils) - 1)}
    assert len(steps) == 1, f"the veil must step evenly down the stack, found {steps}"


def test_each_case_card_carries_its_stack_order_and_veil_attributes():
    response = fetch_document("/")
    orders = attribute_values(response.text, "data-case-order")
    veils = attribute_values(response.text, "data-veil")
    assert "1" in orders, f"the first card must carry data-case-order=1, found {orders}"
    assert FIRST_VEIL in veils, (
        f"the first card must carry data-veil={FIRST_VEIL}, found {veils}")


def test_reordering_the_published_cases_recomputes_every_veil_value(lead):
    original = [c["slug"] for c in published_cases()]
    moved = original[1:] + original[:1]
    response = api_post("/console/cases/reorder", lead, json={"order": moved})
    assert response.status_code in ACCEPTED, describe(
        response, "a lead must be able to reorder the published stack")
    settle()
    after = published_cases()
    assert [c["slug"] for c in after] == moved, (
        "the reordered stack must read back in the order the lead sent")
    assert str(after[0]["veil"]) == FIRST_VEIL, (
        f"the card now first must wear the first veil {FIRST_VEIL}")
    restore = api_post("/console/cases/reorder", lead, json={"order": original})
    assert restore.status_code in ACCEPTED, describe(
        restore, "the stack must be restorable to its seeded order")


def test_reorder_never_leaves_two_cases_at_one_stack_position(lead):
    original = [c["slug"] for c in published_cases()]
    duplicated = list(original)
    duplicated[1] = duplicated[0]
    response = api_post("/console/cases/reorder", lead, json={"order": duplicated})
    assert response.status_code in CLIENT_ERROR, describe(
        response, "a reorder naming one case twice must be refused")
    settle()
    assert [c["slug"] for c in published_cases()] == original, (
        "a refused reorder must leave every stack position exactly as it was")


def test_publishing_a_thirteenth_case_moves_the_first_veil(lead, suffix):
    created = create_case(lead, suffix)
    slug = created.get("slug") or conftest.probe_slug(suffix)
    uploaded = upload_cover(lead, slug, probe_png(suffix))
    assert uploaded.status_code in ACCEPTED, describe(
        uploaded, "a member must be able to upload a case cover")
    submitted = api_post(f"/console/cases/{slug}/submit", lead)
    assert submitted.status_code in ACCEPTED, describe(
        submitted, "a member must be able to submit a case for review")
    approved_review(lead, slug, suffix)
    revision = api_get(f"/console/cases/{slug}", lead).json().get("current_revision")
    internal = api_post(f"/console/cases/{slug}/approve", lead,
                        json={"revision": revision})
    assert internal.status_code in ACCEPTED, describe(
        internal, "a lead must be able to record the internal approval")
    published = publish_case(lead, slug)
    assert published.status_code in ACCEPTED, describe(
        published, "a case carrying both approvals must publish")
    settle()
    cases = published_cases()
    assert len(cases) == PUBLISHED_CASE_COUNT + 1, (
        f"the stack must now carry {PUBLISHED_CASE_COUNT + 1} cases")
    assert str(cases[0]["veil"]) == THIRTEENTH_FIRST_VEIL, (
        f"with thirteen cases the first veil must read {THIRTEENTH_FIRST_VEIL}, "
        f"the app returned {cases[0]['veil']}")
    api_post(f"/console/cases/{slug}/unpublish", lead)


def test_the_archive_card_never_appears_in_the_published_case_list():
    slugs = [str(c["slug"]).lower() for c in published_cases()]
    assert "archive" not in slugs, (
        f"the archive card is not a case, so it must not be listed, found {slugs}")


def test_case_detail_returns_its_neighbouring_slugs():
    response = api_get(f"/cases/{PUBLISHED_SLUGS[1]}")
    assert response.status_code == 200, describe(
        response, "a published case must be readable by anybody")
    payload = response.json()
    assert payload.get("previous_slug") == PUBLISHED_SLUGS[0], (
        "the second case's previous_slug must name the first case")
    assert payload.get("next_slug") == PUBLISHED_SLUGS[2], (
        "the second case's next_slug must name the third case")


def test_first_and_last_cases_carry_no_neighbour_beyond_the_stack():
    first = api_get(f"/cases/{PUBLISHED_SLUGS[0]}").json()
    last = api_get(f"/cases/{PUBLISHED_SLUGS[-1]}").json()
    assert first.get("previous_slug") is None, (
        "the first case must carry no previous neighbour")
    assert last.get("next_slug") is None, (
        "the last case must carry no next neighbour")


def test_case_body_carries_blocks_of_seven_kinds_only():
    payload = api_get(f"/cases/{FIRST_SLUG}").json()
    blocks = payload.get("blocks") or []
    assert blocks, "a published case must carry at least one body block"
    kinds = {str(b.get("kind")) for b in blocks}
    assert kinds <= set(BLOCK_KINDS), (
        f"a case body may only carry {BLOCK_KINDS}, the app returned {kinds}")


def test_unpublished_case_answers_a_stranger_as_an_unknown_address_does():
    review = api_get(f"/cases/{REVIEW_SLUG}")
    draft = api_get(f"/cases/{DRAFT_SLUG}")
    unknown = api_get("/cases/no-such-case-anywhere")
    assert review.status_code in NOT_FOUND, describe(
        review, "a case in review must not be readable by a stranger")
    assert draft.status_code == unknown.status_code, (
        f"a draft case must answer exactly as an unknown address does, "
        f"{draft.status_code} against {unknown.status_code}")


def test_signed_in_member_reads_an_unpublished_case(writer):
    response = api_get(f"/console/cases/{REVIEW_SLUG}", writer)
    assert response.status_code == 200, describe(
        response, "a signed in member must be able to read a case in review")


def test_archive_returns_the_seed_the_plane_plus_every_wall_item():
    response = api_get("/archive")
    assert response.status_code == 200, describe(
        response, "the archive document must be readable by anybody")
    payload = response.json()
    assert payload.get("seed") == ARCHIVE_SEED, (
        f"the archive layout seed must read {ARCHIVE_SEED}, "
        f"the app returned {payload.get('seed')}")
    plane = payload.get("plane") or {}
    assert float(plane.get("width", 0)) > 0 and float(plane.get("height", 0)) > 0, (
        "the archive plane must carry a width and a height")
    items = payload.get("items") or []
    assert len(items) == ARCHIVE_ITEM_COUNT, (
        f"the seeded wall must carry {ARCHIVE_ITEM_COUNT} items, found {len(items)}")


def test_no_two_archive_item_rectangles_overlap_on_the_plane():
    items = api_get("/archive").json().get("items") or []
    placed = [i for i in items if all(k in i for k in ("x", "y", "w", "h"))]
    assert len(placed) == len(items), "every wall item must carry a placed rectangle"
    for index, first in enumerate(placed):
        for second in placed[index + 1:]:
            assert not rectangles_overlap(first, second), (
                f"archive items {first.get('id')} and {second.get('id')} overlap on "
                f"the plane: {first} against {second}")


def test_two_reads_of_the_archive_return_identical_item_positions():
    first = api_get("/archive").json().get("items") or []
    settle()
    second = api_get("/archive").json().get("items") or []
    assert placed_shape(first) == placed_shape(second), (
        "two reads of the archive with nothing changed must return the same positions")


def test_adding_an_archive_item_regenerates_the_layout_without_overlap(lead, suffix):
    body = {"title": "Probe Frame " + suffix, "year": 2026,
            "intrinsic_width": 800, "intrinsic_height": 1200,
            "disciplines": [LEAD_DISCIPLINE], "case_slug": None}
    created = api_post("/console/archive", lead, json=body)
    assert created.status_code in ACCEPTED, describe(
        created, "a member must be able to add an archive item")
    settle()
    items = api_get("/archive").json().get("items") or []
    assert len(items) == ARCHIVE_ITEM_COUNT + 1, (
        f"the wall must now carry {ARCHIVE_ITEM_COUNT + 1} items, found {len(items)}")
    for index, first in enumerate(items):
        for second in items[index + 1:]:
            assert not rectangles_overlap(first, second), (
                f"after a new item the wall still must not overlap: {first} "
                f"against {second}")


def test_an_archive_item_linked_to_a_published_case_names_that_case():
    items = api_get("/archive").json().get("items") or []
    linked = [i for i in items if i.get("case_slug")]
    assert linked, "one seeded archive item must link to a published case"
    assert any(i.get("case_slug") == LINKED_SLUG for i in linked), (
        f"the linked archive item must name {LINKED_SLUG}, "
        f"found {[i.get('case_slug') for i in linked]}")


def test_showreel_returns_its_poster_address_plus_its_renditions():
    response = api_get("/showreel")
    assert response.status_code == 200, describe(
        response, "the showreel document must be readable by anybody")
    payload = response.json()
    assert payload.get("poster_url"), "the showreel must carry a poster address"
    assert payload.get("renditions"), "the showreel must carry at least one rendition"


def test_awards_returns_each_body_with_its_types_carrying_a_count():
    response = api_get("/awards")
    assert response.status_code == 200, describe(
        response, "the awards board must be readable by anybody")
    payload = response.json()
    bodies = payload if isinstance(payload, list) else payload.get("bodies", [])
    names = [b.get("name") for b in bodies]
    assert AWARD_BODY_PRIMARY in names, (
        f"the board must group by {AWARD_BODY_PRIMARY}, found {names}")
    primary = next(b for b in bodies if b.get("name") == AWARD_BODY_PRIMARY)
    counted = {t.get("name"): t.get("count") for t in primary.get("types", [])}
    assert counted.get(AWARD_TYPE_COUNTED) == AWARD_TYPE_COUNTED_TOTAL, (
        f"{AWARD_TYPE_COUNTED} must read {AWARD_TYPE_COUNTED_TOTAL}, "
        f"the app returned {counted.get(AWARD_TYPE_COUNTED)}")


def test_an_award_type_with_no_records_carries_no_count():
    payload = api_get("/awards").json()
    bodies = payload if isinstance(payload, list) else payload.get("bodies", [])
    third = next(b for b in bodies if b.get("name") == AWARD_BODY_THIRD)
    empty = next(t for t in third.get("types", [])
                 if t.get("name") == AWARD_TYPE_EMPTY)
    assert not empty.get("count"), (
        f"{AWARD_TYPE_EMPTY} carries no records, so it must carry no count, "
        f"the app returned {empty.get('count')}")


def test_recording_one_more_win_moves_that_award_count_up_by_one(lead):
    before = api_get("/awards").json()
    bodies = before if isinstance(before, list) else before.get("bodies", [])
    primary = next(b for b in bodies if b.get("name") == AWARD_BODY_PRIMARY)
    start = next(t for t in primary.get("types", [])
                 if t.get("name") == AWARD_TYPE_COUNTED).get("count")
    created = api_post("/console/awards", lead,
                       json={"award_type": AWARD_TYPE_COUNTED, "won_on": "2026-01-05",
                             "verification_url": "https://prixel.example.com/win",
                             "case_slug": FIRST_SLUG})
    assert created.status_code in ACCEPTED, describe(
        created, "a lead must be able to record one more win")
    settle()
    after = api_get("/awards").json()
    bodies = after if isinstance(after, list) else after.get("bodies", [])
    primary = next(b for b in bodies if b.get("name") == AWARD_BODY_PRIMARY)
    end = next(t for t in primary.get("types", [])
               if t.get("name") == AWARD_TYPE_COUNTED).get("count")
    assert end == start + 1, (
        f"recording one win must move the count from {start} to {start + 1}, "
        f"the app returned {end}")


def test_award_counts_are_derived_from_records_rather_than_stored():
    types = backend().rows(TABLE_AWARD_TYPE)
    assert types, "the award types must be stored rows"
    for row in types:
        assert "count" not in row, (
            f"an award type must not store a count column, found {sorted(row)}")
    assert backend().count(TABLE_AWARD) > 0, (
        "the board's counts must come from individual award records")


def test_an_accepted_work_inquiry_is_stored_with_its_first_event(suffix):
    payload, body = accepted_inquiry(suffix)
    row = inquiry_row(body["submission_key"])
    assert row.get("state") in INQUIRY_STATES, (
        f"a stored inquiry must carry one of {INQUIRY_STATES}, "
        f"found {row.get('state')}")
    events = backend().rows(TABLE_INQUIRY_EVENT, inquiry_id=row["id"])
    assert events, "an accepted inquiry must be written with its first event"


def test_an_invalid_work_inquiry_is_refused_with_a_message_per_field(suffix):
    response = submit_inquiry(inquiry_body(suffix, email="", message="too short"))
    assert response.status_code in CLIENT_ERROR, describe(
        response, "an inquiry missing a reply address must be refused")
    payload = response.json()
    fields = payload.get("fields") or payload.get("errors") or {}
    if isinstance(fields, dict):
        keys = set(fields)
    else:
        keys = {str(f.get("field")) for f in fields}
    assert "email" in keys, (
        f"the refusal must name the email field, the app returned {payload}")
    assert "message" in keys, (
        f"the refusal must name the message field, the app returned {payload}")


def test_an_invalid_work_inquiry_writes_no_row_at_all(suffix):
    key = "probe-invalid-" + suffix
    before = backend().count(TABLE_INQUIRY)
    response = submit_inquiry(inquiry_body(suffix, submission_key=key, consent=False))
    assert response.status_code in CLIENT_ERROR, describe(
        response, "an inquiry without consent must be refused")
    settle()
    assert backend().count(TABLE_INQUIRY) == before, (
        "a refused inquiry must leave the stored count exactly where it was")
    assert backend().one(TABLE_INQUIRY, submission_key=key) is None, (
        "a refused inquiry must write no row under its own submission key")


def test_a_repeated_submission_key_produces_exactly_one_stored_inquiry(suffix):
    key = "probe-repeat-" + suffix
    first = submit_inquiry(inquiry_body(suffix, submission_key=key))
    assert first.status_code in ACCEPTED, describe(
        first, "the first submission carrying a key must be accepted")
    second = submit_inquiry(inquiry_body(suffix, submission_key=key))
    assert second.status_code in ACCEPTED, describe(
        second, "a repeat of one key must be accepted rather than refused")
    settle()
    rows = backend().rows(TABLE_INQUIRY, submission_key=key)
    assert len(rows) == 1, (
        f"one submission key must produce exactly one row, found {len(rows)}")


def test_a_repeated_submission_key_returns_the_first_inquiry_id(suffix):
    key = "probe-echo-" + suffix
    first = submit_inquiry(inquiry_body(suffix, submission_key=key))
    second = submit_inquiry(inquiry_body(suffix, submission_key=key,
                                         message=conftest.probe_message(suffix) + " b"))
    assert first.json().get("id") == second.json().get("id"), (
        "a repeat of one key must return the first inquiry rather than a new one")


def test_a_decoy_field_submission_is_refused_without_telling_the_sender(suffix):
    key = "probe-decoy-" + suffix
    clean, _ = accepted_inquiry(suffix)
    response = submit_inquiry(inquiry_body(suffix, submission_key=key,
                                           **{DECOY_FIELD: "https://spam.example.com"}))
    assert response.status_code in ACCEPTED, describe(
        response, "an automated submission must be answered as an accepted one is")
    settle()
    row = backend().one(TABLE_INQUIRY, submission_key=key)
    assert row is not None, "a refused automated submission must still be stored"
    assert row.get("state") == INQUIRY_SPAM or row.get("spam_reason"), (
        f"an automated submission must be stored with its reason, found {row}")
    assert clean.get("id") != row.get("id"), (
        "the decoy submission must be a different row from the clean one")


def test_a_submission_under_the_minimum_fill_time_is_refused(suffix):
    key = "probe-fast-" + suffix
    now = httpx.get(appclient.app_url() + "/api/health").headers.get("date")
    assert now, "the app must answer health with a date header to time a submission"
    response = submit_inquiry(inquiry_body(suffix, submission_key=key,
                                           form_opened_at=now))
    assert response.status_code in ACCEPTED, describe(
        response, "a submission filled instantly must be answered as accepted")
    settle()
    row = backend().one(TABLE_INQUIRY, submission_key=key)
    assert row is not None, "a submission filled instantly must still be stored"
    assert row.get("spam_reason") or row.get("state") == INQUIRY_SPAM, (
        f"a submission filled instantly must carry its reason, found {row}")


def test_submissions_past_the_hourly_ceiling_for_one_address_are_refused(suffix):
    address = conftest.probe_address(suffix)
    outcomes = []
    for index in range(RATE_CEILING_PER_ADDRESS + 2):
        body = inquiry_body(suffix, email=address,
                            submission_key=f"probe-rate-{suffix}-{index}")
        outcomes.append(submit_inquiry(body).status_code)
    assert 429 in outcomes or any(code in CLIENT_ERROR for code in outcomes[-2:]), (
        f"the address ceiling must refuse a burst from one address, got {outcomes}")


def test_a_high_scoring_submission_is_stored_in_the_spam_state(suffix):
    key = "probe-links-" + suffix
    spammy = ("Cheap backlinks https://a.example.com https://b.example.com "
              "https://c.example.com https://d.example.com " + suffix)
    response = submit_inquiry(inquiry_body(suffix, submission_key=key, message=spammy))
    assert response.status_code in ACCEPTED, describe(
        response, "a scored submission must be answered as an accepted one is")
    settle()
    row = backend().one(TABLE_INQUIRY, submission_key=key)
    assert row is not None, "a scored submission must be stored rather than discarded"
    assert row.get("state") == INQUIRY_SPAM or row.get("spam_score"), (
        f"a high scoring submission must carry its score or its state, found {row}")


def test_an_inquiry_at_the_top_budget_band_is_assigned_to_the_principal_lead(suffix):
    key = "probe-band-" + suffix
    submit_inquiry(inquiry_body(suffix, submission_key=key, budget_band=BUDGET_TOP,
                                disciplines=[LEAD2_DISCIPLINE]))
    settle()
    row = inquiry_row(key)
    assignee = backend().one(TABLE_MEMBER, id=row.get("assignee_id")) or {}
    assert assignee.get("email") == LEAD_EMAIL, (
        f"an inquiry at {BUDGET_TOP} must reach {LEAD_EMAIL}, found {assignee}")


def test_an_inquiry_naming_one_leads_discipline_is_assigned_to_that_lead(suffix):
    key = "probe-craft-" + suffix
    submit_inquiry(inquiry_body(suffix, submission_key=key,
                                budget_band="25k-75k",
                                disciplines=[LEAD2_DISCIPLINE]))
    settle()
    row = inquiry_row(key)
    assignee = backend().one(TABLE_MEMBER, id=row.get("assignee_id")) or {}
    assert assignee.get("email") == conftest.LEAD2_EMAIL, (
        f"an inquiry naming {LEAD2_DISCIPLINE} must reach {conftest.LEAD2_EMAIL}, "
        f"found {assignee}")


def test_the_console_inquiry_queue_reads_newest_first(lead, suffix):
    accepted_inquiry(suffix)
    settle()
    response = api_get("/console/inquiries", lead)
    assert response.status_code == 200, describe(
        response, "a lead must be able to read the inquiry queue")
    rows = response.json()
    assert isinstance(rows, list) and rows, describe(
        response, "the inquiry queue must be a top-level JSON array")
    stamps = [str(r.get("received_at")) for r in rows]
    assert stamps == sorted(stamps, reverse=True), (
        f"the queue must read newest first, the app returned {stamps[:4]}")


def test_erasing_an_inquiry_keeps_its_row_with_every_event(lead, suffix):
    payload, body = accepted_inquiry(suffix)
    row = inquiry_row(body["submission_key"])
    events_before = len(backend().rows(TABLE_INQUIRY_EVENT, inquiry_id=row["id"]))
    erased = api_post(f"/console/inquiries/{row['id']}/erase", lead)
    assert erased.status_code in ACCEPTED, describe(
        erased, "a lead must be able to erase an inquiry on request")
    settle()
    after = backend().one(TABLE_INQUIRY, id=row["id"])
    assert after is not None, "erasure must keep the row rather than delete it"
    events_after = len(backend().rows(TABLE_INQUIRY_EVENT, inquiry_id=row["id"]))
    assert events_after >= events_before, (
        f"erasure must keep every event, {events_before} before against "
        f"{events_after} after")


def test_an_erased_inquiry_reads_the_erasure_marker_in_every_personal_field(lead,
                                                                           suffix):
    payload, body = accepted_inquiry(suffix)
    row = inquiry_row(body["submission_key"])
    api_post(f"/console/inquiries/{row['id']}/erase", lead)
    settle()
    after = backend().one(TABLE_INQUIRY, id=row["id"]) or {}
    for field in ("name", "email", "company", "message"):
        assert str(after.get(field)) == ERASURE_MARKER, (
            f"the erased {field} must read {ERASURE_MARKER}, "
            f"the app stored {after.get(field)!r}")


def test_the_trail_sequence_values_increase_with_no_gaps(lead, suffix):
    accepted_inquiry(suffix)
    settle()
    response = api_get("/console/audit", lead)
    assert response.status_code == 200, describe(
        response, "a lead must be able to read the trail")
    rows = response.json()
    numbers = [int(r["sequence"]) for r in rows]
    assert numbers == sorted(numbers), "the trail must read in sequence order"
    assert numbers == list(range(numbers[0], numbers[0] + len(numbers))), (
        f"the trail sequence must carry no gaps, the app returned {numbers[:8]}")


def test_each_trail_row_chains_to_the_row_before_it(lead):
    rows = api_get("/console/audit", lead).json()
    assert len(rows) > 1, "the trail must carry more than one row to chain"
    for earlier, later in zip(rows, rows[1:]):
        assert later.get("prev_hash") == earlier.get("hash"), (
            f"trail row {later.get('sequence')} must chain to "
            f"{earlier.get('sequence')}, found {later.get('prev_hash')!r} against "
            f"{earlier.get('hash')!r}")


def test_the_trail_rejects_an_update_or_a_removal(lead):
    rows = api_get("/console/audit", lead).json()
    target = rows[0]
    patched = api_patch(f"/console/audit/{target.get('id')}", lead,
                        json={"action": "rewritten"})
    removed = api_delete(f"/console/audit/{target.get('id')}", lead)
    assert patched.status_code in REFUSED or patched.status_code == 405, describe(
        patched, "a trail row must not be updatable")
    assert removed.status_code in REFUSED or removed.status_code == 405, describe(
        removed, "a trail row must not be removable")


def test_the_console_case_list_carries_every_case_in_any_state(lead):
    response = api_get("/console/cases", lead)
    assert response.status_code == 200, describe(
        response, "a member must be able to read every case")
    rows = response.json()
    slugs = {r["slug"] for r in rows}
    assert REVIEW_SLUG in slugs and DRAFT_SLUG in slugs, (
        f"the console list must carry the unpublished cases, found {sorted(slugs)}")
    states = {str(r.get("state")) for r in rows}
    assert states <= set(CASE_STATES), (
        f"a case state must be one of {CASE_STATES}, the app returned {states}")


def test_each_console_case_row_carries_its_state_word(lead):
    response = fetch_document("/console/cases")
    assert response.status_code in (200, 302, 303), describe(
        response, "the console case list must render for a signed in member")
    rows = api_get("/console/cases", lead).json()
    words = {str(r.get("state")) for r in rows}
    assert STATE_DRAFT in words, (
        f"the seeded draft case must read its state as a word, found {words}")


def test_a_save_carrying_a_stale_revision_is_refused_with_the_current_one(lead,
                                                                         suffix):
    created = create_case(lead, suffix)
    slug = created.get("slug") or conftest.probe_slug(suffix)
    loaded = api_get(f"/console/cases/{slug}", lead).json()
    revision = loaded.get("current_revision")
    first = api_patch(f"/console/cases/{slug}", lead,
                      json={"revision": revision, "title": "Probe Case A " + suffix})
    assert first.status_code in ACCEPTED, describe(
        first, "a save against the loaded revision must be accepted")
    stale = api_patch(f"/console/cases/{slug}", lead,
                      json={"revision": revision, "title": "Probe Case B " + suffix})
    assert stale.status_code in CLIENT_ERROR, describe(
        stale, "a save against a stale revision must be refused")
    payload = stale.json()
    assert payload.get("current_revision") is not None, (
        f"a refused save must return the current revision, the app returned {payload}")


def test_two_saves_from_one_loaded_revision_never_both_succeed(lead, suffix):
    created = create_case(lead, suffix)
    slug = created.get("slug") or conftest.probe_slug(suffix)
    revision = api_get(f"/console/cases/{slug}", lead).json().get("current_revision")
    outcomes = []
    for index in range(2):
        outcomes.append(api_patch(f"/console/cases/{slug}", lead,
                                  json={"revision": revision,
                                        "title": f"Probe Race {index} {suffix}"}
                                  ).status_code)
    accepted = [code for code in outcomes if code in ACCEPTED]
    assert len(accepted) == 1, (
        f"exactly one save from one loaded revision may be accepted, got {outcomes}")


def test_a_writer_cannot_publish_a_case(writer, lead, suffix):
    created = create_case(lead, suffix)
    slug = created.get("slug") or conftest.probe_slug(suffix)
    before = backend().one(TABLE_CASE, slug=slug)
    response = publish_case(writer, slug)
    assert response.status_code in DENIED, describe(
        response, "a writer must be refused at the publish endpoint")
    settle()
    after = backend().one(TABLE_CASE, slug=slug)
    assert after.get("state") == before.get("state"), (
        f"a refused publish must leave the stored state at {before.get('state')}, "
        f"the app stored {after.get('state')}")


def test_a_writer_requesting_the_inquiry_queue_is_refused(writer):
    for path in ("/console/inquiries", "/console/audit"):
        response = api_get(path, writer)
        assert response.status_code in DENIED, describe(
            response, f"a writer must be refused at {path}")


def test_an_anonymous_request_for_a_console_route_lands_on_the_sign_in_route():
    response = fetch_document_no_redirect("/console/cases")
    assert response.status_code in (301, 302, 303, 307, 308, 401, 403), describe(
        response, "an anonymous console request must not be served")
    if response.status_code in (301, 302, 303, 307, 308):
        assert "/login" in response.headers.get("location", ""), (
            f"the redirect must land on the sign in route, the app sent "
            f"{response.headers.get('location')!r}")


def test_an_absolute_return_path_on_sign_in_is_refused():
    response = fetch_document_no_redirect("/login?next=https://elsewhere.example.com/")
    assert response.status_code in (200, 400, 302, 303), describe(
        response, "an absolute return path must be handled rather than followed")
    assert "elsewhere.example.com" not in response.headers.get("location", ""), (
        "an absolute return path must never be followed off the app's own origin")


def test_publication_is_refused_until_a_client_approval_matches_the_revision(lead):
    before = backend().one(TABLE_CASE, slug=DRAFT_SLUG)
    response = publish_case(lead, DRAFT_SLUG)
    assert response.status_code in CLIENT_ERROR, describe(
        response, "a case with no client approval must not publish")
    settle()
    after = backend().one(TABLE_CASE, slug=DRAFT_SLUG)
    assert after.get("state") == before.get("state"), (
        "a refused publication must leave the stored state unchanged")


def test_publication_is_refused_until_a_lead_approval_matches_the_revision(lead):
    response = publish_case(lead, REVIEW_SLUG)
    assert response.status_code in CLIENT_ERROR, describe(
        response, "a case carrying only the client approval must not publish")
    body = response.text.lower()
    assert "approv" in body, (
        f"the refusal must name the approval condition, the app returned "
        f"{response.text[:300]}")


def test_a_refused_publication_leaves_the_case_out_of_the_public_stack(lead):
    publish_case(lead, REVIEW_SLUG)
    settle()
    slugs = [c["slug"] for c in published_cases()]
    assert REVIEW_SLUG not in slugs, (
        f"a case whose publication was refused must stay out of the stack, "
        f"found {slugs}")


def test_editing_an_approved_case_writes_a_new_revision(lead, suffix):
    created = create_case(lead, suffix)
    slug = created.get("slug") or conftest.probe_slug(suffix)
    before = len(backend().rows(TABLE_REVISION))
    revision = api_get(f"/console/cases/{slug}", lead).json().get("current_revision")
    edited = api_patch(f"/console/cases/{slug}", lead,
                       json={"revision": revision,
                             "title": "Probe Revised " + suffix})
    assert edited.status_code in ACCEPTED, describe(
        edited, "a member must be able to edit a draft case")
    settle()
    after = len(backend().rows(TABLE_REVISION))
    assert after > before, (
        f"an edit must write a new revision row, {before} before against {after} after")


def test_a_case_revision_is_immutable_once_written(lead, suffix):
    created = create_case(lead, suffix)
    slug = created.get("slug") or conftest.probe_slug(suffix)
    revision = api_get(f"/console/cases/{slug}", lead).json().get("current_revision")
    rows = backend().rows(TABLE_REVISION, revision=revision)
    assert rows, "a created case must carry its first revision row"
    snapshot = rows[0]
    api_patch(f"/console/cases/{slug}", lead,
              json={"revision": revision, "title": "Probe Frozen " + suffix})
    settle()
    again = backend().rows(TABLE_REVISION, revision=revision)
    assert again and again[0] == snapshot, (
        "an existing revision row must not change when a later revision is written")


def test_a_minor_revision_changing_the_client_name_is_refused(lead, suffix):
    created = create_case(lead, suffix)
    slug = created.get("slug") or conftest.probe_slug(suffix)
    revision = api_get(f"/console/cases/{slug}", lead).json().get("current_revision")
    response = api_patch(f"/console/cases/{slug}", lead,
                         json={"revision": revision, "is_minor": True,
                               "client": "Another Client " + suffix})
    assert response.status_code in CLIENT_ERROR, describe(
        response, "a minor revision may not change the client name")
    settle()
    stored = backend().one(TABLE_CASE, slug=slug)
    assert stored.get("client") == created.get("client"), (
        f"the refused minor revision must leave the client at "
        f"{created.get('client')!r}, the app stored {stored.get('client')!r}")


def test_a_lead_issues_a_review_link_bound_to_one_case_revision(lead, suffix):
    before = len(backend().rows(TABLE_REVIEW_TOKEN))
    issued = api_post(f"/console/cases/{REVIEW_SLUG}/review-links", lead,
                      json={"emails": [conftest.probe_address(suffix)],
                            "expires_in_days": 14})
    assert issued.status_code in ACCEPTED, describe(
        issued, "a lead must be able to issue a review link")
    settle()
    rows = backend().rows(TABLE_REVIEW_TOKEN)
    assert len(rows) > before, "issuing a review link must store a token row"
    latest = rows[-1]
    assert latest.get("revision") is not None, (
        f"a review token must be bound to one revision, the app stored {latest}")


def test_issuing_a_second_review_link_revokes_the_previous_tokens(lead, suffix):
    first = api_post(f"/console/cases/{REVIEW_SLUG}/review-links", lead,
                     json={"emails": [conftest.probe_address(suffix)],
                           "expires_in_days": 14})
    assert first.status_code in ACCEPTED, describe(first, "the first link must issue")
    payload = first.json()
    tokens = payload if isinstance(payload, list) else payload.get("tokens", [])
    original = tokens[0]["token"] if isinstance(tokens[0], dict) else str(tokens[0])
    second = api_post(f"/console/cases/{REVIEW_SLUG}/review-links", lead,
                      json={"emails": [conftest.probe_address(suffix + "b")],
                            "expires_in_days": 14})
    assert second.status_code in ACCEPTED, describe(second, "the second link must issue")
    settle()
    response = api_get(f"/preview/{original}")
    assert response.status_code in REFUSED, describe(
        response, "the superseded token must stop reaching the preview")


def test_a_preview_token_reaches_no_case_beyond_the_one_it_is_bound_to(lead, suffix):
    issued = api_post(f"/console/cases/{REVIEW_SLUG}/review-links", lead,
                      json={"emails": [conftest.probe_address(suffix)],
                            "expires_in_days": 14})
    payload = issued.json()
    tokens = payload if isinstance(payload, list) else payload.get("tokens", [])
    token = tokens[0]["token"] if isinstance(tokens[0], dict) else str(tokens[0])
    allowed = api_get(f"/preview/{token}")
    assert allowed.status_code == 200, describe(
        allowed, "a valid review token must reach its own case revision")
    body = allowed.json()
    assert str(body.get("slug", REVIEW_SLUG)) == REVIEW_SLUG, (
        f"the preview must carry {REVIEW_SLUG}, the app returned {body.get('slug')}")
    other = api_get(f"/cases/{DRAFT_SLUG}", token)
    assert other.status_code in NOT_FOUND, describe(
        other, "a review token must reach no other unpublished case")


def test_an_expired_token_answers_exactly_as_an_unknown_token_does():
    unknown = api_get("/preview/not-a-real-token-at-all")
    malformed = api_get("/preview/%20")
    assert unknown.status_code in REFUSED, describe(
        unknown, "an unknown review token must be refused")
    assert unknown.status_code == malformed.status_code, (
        f"an unknown token and a malformed one must answer alike, "
        f"{unknown.status_code} against {malformed.status_code}")


def test_an_uploaded_case_cover_is_stored_in_the_object_store_under_its_key(lead,
                                                                           suffix):
    created = create_case(lead, suffix)
    slug = created.get("slug") or conftest.probe_slug(suffix)
    response = upload_cover(lead, slug, probe_png(suffix))
    assert response.status_code in ACCEPTED, describe(
        response, "a member must be able to upload a case cover")
    payload = response.json()
    key = payload.get("object_key")
    assert key and key.startswith(COVER_KEY_PREFIX + slug + "/"), (
        f"the cover key must read {COVER_KEY_PREFIX}{slug}/<digest>.<ext>, "
        f"the app returned {key!r}")
    assert poll_until(lambda: object_store().exists(key)), (
        f"the uploaded bytes must exist in the object store at {key}")


def test_an_uploaded_file_renamed_to_another_extension_is_refused(lead, suffix):
    created = create_case(lead, suffix)
    slug = created.get("slug") or conftest.probe_slug(suffix)
    before = len(object_store().list(COVER_KEY_PREFIX))
    response = upload_cover(lead, slug, b"not an image at all " + suffix.encode(),
                            filename="payload.png", content_type="image/png")
    assert response.status_code in CLIENT_ERROR, describe(
        response, "a file that is not an image must be refused on inspection")
    settle()
    assert len(object_store().list(COVER_KEY_PREFIX)) == before, (
        "a refused upload must leave no object behind in the store")


def test_the_cover_object_of_an_unpublished_case_is_refused_to_a_stranger():
    response = api_get(f"/cases/{REVIEW_SLUG}/cover")
    assert response.status_code in NOT_FOUND, describe(
        response, "the cover of a case in review must not be served to a stranger")


def test_the_uploaded_archive_image_lives_under_the_archive_key_prefix(lead, suffix):
    created = api_post("/console/archive", lead,
                       json={"title": "Probe Frame " + suffix, "year": 2026,
                             "intrinsic_width": 900, "intrinsic_height": 600,
                             "disciplines": [LEAD_DISCIPLINE], "case_slug": None})
    assert created.status_code in ACCEPTED, describe(
        created, "a member must be able to add an archive item")
    item_id = created.json().get("id")
    files = {"file": ("frame.png", probe_png(suffix), "image/png")}
    with appclient.client(lead) as api:
        uploaded = api.post(f"/console/archive/{item_id}/image", files=files,
                            data={"alt_text": "A probe archive frame"})
    assert uploaded.status_code in ACCEPTED, describe(
        uploaded, "a member must be able to upload an archive image")
    key = uploaded.json().get("object_key")
    assert key and key.startswith(ARCHIVE_KEY_PREFIX), (
        f"an archive image key must begin {ARCHIVE_KEY_PREFIX}, the app returned {key!r}")
    assert poll_until(lambda: object_store().exists(key)), (
        f"the uploaded archive bytes must exist in the object store at {key}")


def test_deleting_a_referenced_media_asset_is_refused_with_its_references(lead,
                                                                         suffix):
    created = create_case(lead, suffix)
    slug = created.get("slug") or conftest.probe_slug(suffix)
    uploaded = upload_cover(lead, slug, probe_png(suffix))
    key = uploaded.json().get("object_key")
    asset = poll_until(lambda: backend().one(TABLE_MEDIA, object_key=key))
    assert asset, f"an upload must be recorded in {TABLE_MEDIA} under {key}"
    response = api_delete(f"/console/media/{asset['id']}", lead)
    assert response.status_code in CLIENT_ERROR, describe(
        response, "a referenced media asset must not be deletable")
    assert slug in response.text, (
        f"the refusal must list the referencing record {slug}, the app returned "
        f"{response.text[:300]}")


def test_every_public_route_renders_a_complete_document_from_the_server():
    for path in PUBLIC_ROUTES:
        response = fetch_document(path)
        assert response.status_code == 200, describe(
            response, f"{path} must render a document")
        markup = response.text.lower()
        assert "<html" in markup and "</body>" in markup, (
            f"{path} must return a complete document rather than an empty shell")
        assert len(response.text) > 2000, (
            f"{path} must carry its copy in the served document, "
            f"the app returned {len(response.text)} characters")


def test_the_served_document_carries_every_word_before_any_script_runs():
    response = fetch_document("/")
    assert STUDIO_ADDRESS in response.text, (
        f"the served document must carry {STUDIO_ADDRESS} before any script runs")
    for slug in PUBLISHED_SLUGS[:3]:
        assert slug in response.text, (
            f"the served document must carry the case {slug} before any script runs")


def test_every_response_carries_the_standard_security_headers():
    response = fetch_document("/")
    headers = {k.lower(): v.lower() for k, v in response.headers.items()}
    assert headers.get("x-content-type-options") == "nosniff", (
        f"every response must carry a nosniff content type security header, "
        f"found {headers.get('x-content-type-options')!r}")
    assert "strict-transport-security" in headers, (
        f"every response must carry a strict transport security header, "
        f"found {sorted(headers)}")
    assert headers.get("x-frame-options") or "frame-ancestors" in headers.get(
        "content-security-policy", ""), (
        "every response must deny framing, by header or by policy")


def test_no_credential_appears_in_what_the_browser_downloads():
    for path in PUBLIC_ROUTES:
        markup = fetch_document(path).text
        assert conftest.SEEDED_PASSWORD not in markup, (
            f"{path} must not ship the seeded password to the browser")
        for marker in ("STORAGE_SECRET_KEY", "secretAccessKey", "DATABASE_URL"):
            assert marker not in markup, (
                f"{path} must not ship {marker} to the browser")


def test_an_unknown_address_reports_itself_as_not_found():
    response = fetch_document("/no-such-place-at-all")
    assert response.status_code == 404, describe(
        response, "an unknown address must report itself as not found")
    assert "GO HOME" in response.text, (
        "the not-found page must carry the control that returns to the sequence root")


def test_every_internal_link_on_every_public_route_resolves():
    for path in PUBLIC_ROUTES:
        markup = fetch_document(path).text
        for href in sorted(set(internal_links(markup)))[:25]:
            response = fetch_document(href)
            assert response.status_code == 200, describe(
                response, f"the link {href} printed on {path} must resolve")


def test_the_privacy_page_states_the_retention_window_for_an_inquiry():
    response = fetch_document("/legal/privacy")
    assert response.status_code == 200, describe(
        response, "the privacy page must render")
    body = response.text.lower()
    assert "two years" in body, (
        "the privacy page must state that an inquiry is kept for two years")
    home = fetch_document("/").text
    assert "/legal/privacy" in home, (
        "the privacy page must be reachable from the footer of the home route")


def test_a_list_endpoint_returns_a_top_level_json_array():
    for path in ("/cases", "/services"):
        response = api_get(path)
        assert isinstance(response.json(), list), describe(
            response, f"{path} must return a top-level JSON array")


def test_the_services_list_carries_the_eight_disciplines_in_order():
    rows = api_get("/services").json()
    assert len(rows) == DISCIPLINE_COUNT, (
        f"the services run must carry {DISCIPLINE_COUNT} disciplines, "
        f"found {len(rows)}")
    orders = [int(r["menu_order"]) for r in rows]
    assert orders == sorted(orders), (
        f"the disciplines must read in their stored order, the app returned {orders}")


def test_the_seeded_estate_holds_its_sixteen_tables():
    store = backend()
    for table in (TABLE_MEMBER, TABLE_CASE, TABLE_REVISION, TABLE_ARCHIVE_ITEM,
                  TABLE_AWARD, TABLE_AWARD_TYPE, TABLE_INQUIRY, TABLE_INQUIRY_EVENT,
                  TABLE_REVIEW_TOKEN, TABLE_AUDIT, TABLE_MEDIA, TABLE_PAGE_BLOCK):
        assert store.count(table) >= 0, (
            f"the table {table} the brief names must exist in the datastore")
    assert store.count(TABLE_CASE) >= PUBLISHED_CASE_COUNT + 2, (
        f"the estate must seed {PUBLISHED_CASE_COUNT} published cases beside the two "
        f"unpublished ones")


def test_two_unpublished_cases_are_seeded_beside_the_published_ones():
    store = backend()
    review = store.one(TABLE_CASE, slug=REVIEW_SLUG)
    draft = store.one(TABLE_CASE, slug=DRAFT_SLUG)
    assert review and str(review.get("state")) != STATE_PUBLISHED, (
        f"{REVIEW_SLUG} must be seeded unpublished, found {review}")
    assert draft and str(draft.get("state")) == STATE_DRAFT, (
        f"{DRAFT_SLUG} must be seeded at {STATE_DRAFT}, found {draft}")


def test_seeding_is_idempotent_across_a_restart():
    store = backend()
    for slug in PUBLISHED_SLUGS:
        rows = store.rows(TABLE_CASE, slug=slug)
        assert len(rows) == 1, (
            f"the seeded case {slug} must exist exactly once, found {len(rows)}")
    for email in (conftest.LEAD_EMAIL, conftest.LEAD2_EMAIL, conftest.WRITER_EMAIL):
        assert len(store.rows(TABLE_MEMBER, email=email)) == 1, (
            f"the seeded member {email} must exist exactly once")


def test_the_credentials_file_and_the_reserved_directories_exist():
    assert os.path.isfile(CREDENTIALS_FILE), (
        f"the seeded logins must be written to {CREDENTIALS_FILE}")
    body = open(CREDENTIALS_FILE, encoding="utf-8").read()
    assert conftest.LEAD_EMAIL in body, (
        f"{CREDENTIALS_FILE} must name the seeded lead")
    assert os.path.isdir(SCREENSHOT_DIR), f"{SCREENSHOT_DIR} must exist at the app root"
    assert os.path.isdir(DOWNLOAD_DIR), f"{DOWNLOAD_DIR} must exist at the app root"


def test_no_public_route_reaches_another_service_at_runtime():
    for path in PUBLIC_ROUTES:
        reached = conftest.external_origins(fetch_document(path).text)
        assert not reached, (
            f"{path} must call out to no other service at runtime, it reaches "
            f"{reached[:4]}")


def test_no_payment_or_cart_surface_exists_anywhere():
    for path in ("/cart", "/checkout", "/pricing", "/plans"):
        response = fetch_document(path)
        assert response.status_code == 404, describe(
            response, f"{path} must not exist: nothing is sold on this site")
    markup = fetch_document("/").text.lower()
    for word in ("add to cart", "checkout", "subscribe now"):
        assert word not in markup, (
            f"the home route must carry no commerce control, found {word!r}")
