"""The pytest layer for the broadcast reel index task.

Black box throughout. Every assertion is an HTTP call against the running app, an
out-of-band read of the same PostgreSQL, or an out-of-band read of the same
mailbox. No test reads the app's source, and no test depends on another test's
ordering.
"""

from __future__ import annotations

import concurrent.futures
import os
import re

import httpx

import appclient
from conftest import (
    ABSENT_FROM_HOME,
    FIRST_IN_INDEX,
    LAST_IN_INDEX,
    PRINCIPAL_EMAIL,
    PRINCIPAL_NAME,
    SECOND_IN_HOME,
    SECOND_PRINCIPAL_EMAIL,
    SEEDED_ATTENDEE,
    SUBJECT_PREFIX,
    VISITOR_EMAIL,
    WORKED_SUBJECT,
    booked_slot_ids,
    confirm,
    details,
    expire_holds,
    free_slot_ids,
    fresh_attendee,
    held_slot,
    place_hold,
    slot_rows,
    unique_suffix,
)

PUBLIC_ROUTES = ["/", "/work", "/about", "/contact", "/privacy", "/legal"]

ABSENT_ROUTES = [
    "/auth/signup", "/auth/register", "/auth/password-reset",
    "/auth/forgot-password", "/auth/invitations", "/accounts/delete",
    "/cart", "/checkout", "/payments", "/pricing",
    "/search", "/tags", "/newsletter", "/comments", "/likes", "/reactions",
    "/uploads", "/analytics", "/audit", "/outbox",
    "/bookings/reschedule", "/bookings/cancel",
    "/crew", "/day-rates", "/awards", "/clients",
]


def _slugs(payload):
    return [row.get("slug") for row in payload]


def _page_client():
    """A client speaking to the document origin rather than to the API prefix."""
    return httpx.Client(base_url=appclient.app_url(), timeout=30.0,
                        follow_redirects=True)


def test_seeded_productions_are_listed_in_index_order(anonymous, backend):
    stored = sorted(backend.rows("productions"), key=lambda r: r["sort_index"])
    assert len(stored) == 17, f"the seed carries {len(stored)} productions, expected 17"

    response = anonymous.get("/productions")
    assert response.status_code == 200, response.text[:300]
    served = _slugs(response.json())

    assert served == [r["slug"] for r in stored], (
        "the index is not served in stored sort order: "
        f"served {served[:4]}..., stored {[r['slug'] for r in stored][:4]}..."
    )
    assert served[0] == FIRST_IN_INDEX, (
        f"the index opens on {served[0]!r}, expected {FIRST_IN_INDEX!r}"
    )
    assert served[-1] == LAST_IN_INDEX, (
        f"the index closes on {served[-1]!r}, expected {LAST_IN_INDEX!r}"
    )


def test_home_feed_returns_eleven_in_its_own_order(anonymous, backend):
    featured = [r for r in backend.rows("productions") if r["featured_on_home"]]
    stored = [r["slug"] for r in sorted(featured, key=lambda r: r["home_sort_index"])]
    assert len(stored) == 11, f"the seed features {len(stored)} productions, expected 11"

    response = anonymous.get("/home-feed")
    assert response.status_code == 200, response.text[:300]
    served = _slugs(response.json())

    assert served == stored, (
        f"the home feed is not served in stored home order: {served[:4]}..."
    )
    assert served[1] == SECOND_IN_HOME, (
        f"the second production on the home feed is {served[1]!r}, "
        f"expected {SECOND_IN_HOME!r}"
    )


def test_home_ordering_is_not_derived_from_index_ordering(anonymous, backend):
    index = _slugs(anonymous.get("/productions").json())
    home = _slugs(anonymous.get("/home-feed").json())

    assert home != index[: len(home)], (
        "the home feed is the first eleven of the index, so the two orderings are "
        "not independent"
    )
    kept = [s for s in index if s in set(home)]
    assert home != kept, (
        "the home feed is the index order with the unfeatured rows removed, so the "
        "home ordering is derived rather than stored"
    )
    assert ABSENT_FROM_HOME not in home, (
        f"{ABSENT_FROM_HOME!r} carries no home ordinal but appears on the home feed"
    )


def test_featured_flag_and_home_sort_index_agree(backend):
    wrong = []
    for row in backend.rows("productions"):
        flagged = bool(row["featured_on_home"])
        ordinal = row["home_sort_index"]
        if flagged != (ordinal is not None):
            wrong.append((row["slug"], flagged, ordinal))
    assert not wrong, (
        "these rows carry the featured flag and the home ordinal inconsistently: "
        f"{wrong[:5]}"
    )


def test_case_study_returns_credits_in_stored_order(anonymous, backend):
    production = backend.one("productions", slug=ABSENT_FROM_HOME)
    assert production is not None, f"{ABSENT_FROM_HOME} is not seeded"
    stored = [r["person_name"] for r in
              sorted(backend.rows("production_credits", production_id=production["id"]),
                     key=lambda r: r["sort_index"])]
    assert stored, "the seeded production carries no credits"

    response = anonymous.get(f"/productions/{ABSENT_FROM_HOME}")
    assert response.status_code == 200, response.text[:300]
    served = [c.get("person_name") for c in response.json().get("credits", [])]

    assert served == stored, f"credits served as {served}, stored as {stored}"


def test_every_gallery_still_carries_a_caption(backend):
    missing = [r["id"] for r in backend.rows("gallery_images")
               if not str(r.get("caption") or "").strip()]
    assert not missing, (
        f"{len(missing)} gallery stills carry no caption, first few {missing[:5]}"
    )


def test_gallery_image_without_caption_cannot_be_stored(backend):
    gallery = backend.rows("production_galleries", limit=1)
    assert gallery, "no gallery is seeded"
    gallery_id = gallery[0]["id"]
    before = backend.count("gallery_images")

    try:
        backend.query(
            "INSERT INTO gallery_images (gallery_id, caption, sort_index) "
            "VALUES (%s, NULL, 999)", (gallery_id,))
    except Exception:
        assert backend.count("gallery_images") == before, (
            "the caption-less gallery still was refused and a row was written anyway"
        )
        return

    raise AssertionError(
        "a gallery still with no caption was written, so the requirement lives only "
        "in the interface rather than in storage"
    )


def test_unknown_production_slug_is_not_found(anonymous):
    response = anonymous.get(f"/productions/no-such-production-{unique_suffix()}")
    assert response.status_code == 404, (
        f"an unknown production slug returned {response.status_code}, expected 404"
    )


def test_availability_offers_only_free_published_slots(anonymous, backend):
    response = anonymous.get("/availability")
    assert response.status_code == 200, response.text[:300]
    offered = {str(s.get("id")) for s in response.json()}

    published = {str(r["id"]) for r in slot_rows(backend, state="published")}
    withdrawn = {str(r["id"]) for r in slot_rows(backend, state="withdrawn")}
    taken = {str(i) for i in booked_slot_ids(backend)}

    assert offered <= published, (
        "availability offers slots that are not published: "
        f"{sorted(offered - published)[:5]}"
    )
    assert not (offered & withdrawn), (
        f"availability offers withdrawn slots: {sorted(offered & withdrawn)[:5]}"
    )
    assert not (offered & taken), (
        f"availability offers slots already booked: {sorted(offered & taken)[:5]}"
    )

    seeded = [r for r in slot_rows(backend) if str(r["starts_at"])[:10] in SEED_DAYS]
    assert len(seeded) == 16, (
        f"the seed carries {len(seeded)} availability slots, expected 16"
    )
    for row in slot_rows(backend):
        span = (row["ends_at"] - row["starts_at"]).total_seconds()
        assert span == 900, (
            f"slot {row['id']} runs {span} seconds, expected a fifteen minute slot"
        )
    starts = sorted({str(r["starts_at"])[11:16] for r in seeded})
    assert starts == SEED_SLOT_STARTS, (
        f"the seeded slots begin at {starts}, expected {SEED_SLOT_STARTS}"
    )


def test_taken_slot_is_absent_from_availability(anonymous, backend):
    taken = booked_slot_ids(backend)
    assert taken, "the seed carries no confirmed booking"
    offered = {str(s.get("id")) for s in anonymous.get("/availability").json()}
    for slot_id in taken:
        assert str(slot_id) not in offered, (
            f"slot {slot_id} carries a confirmed booking and is still offered"
        )


def test_holding_a_slot_blocks_a_second_hold(anonymous, backend):
    slot_id, _hold_id = held_slot(anonymous, backend)
    try:
        with appclient.client() as other:
            second = place_hold(other, slot_id)
        assert second.status_code == 409, (
            f"a second hold on a held slot returned {second.status_code}, "
            f"expected a conflict"
        )
    finally:
        expire_holds(backend, slot_id)


def test_holding_a_slot_blocks_a_booking_by_another_caller(anonymous, backend):
    slot_id, _hold_id = held_slot(anonymous, backend)
    try:
        with appclient.client() as other:
            taken = place_hold(other, slot_id)
            assert taken.status_code == 409, (
                f"the slot was not held against the second caller: {taken.status_code}"
            )
            attempt = confirm(other, slot_id, "not-the-live-hold")
        assert attempt.status_code in (403, 409, 410), (
            f"booking a slot held by somebody else returned {attempt.status_code}"
        )
    finally:
        expire_holds(backend, slot_id)


def test_lapsed_hold_releases_the_slot(anonymous, backend):
    slot_id, _hold_id = held_slot(anonymous, backend)
    expire_holds(backend, slot_id)

    offered = {str(s.get("id")) for s in anonymous.get("/availability").json()}
    assert str(slot_id) in offered, (
        "a slot whose hold has lapsed is still withheld from availability"
    )


def test_confirming_against_a_lapsed_hold_is_refused(anonymous, backend):
    slot_id, hold_id = held_slot(anonymous, backend)
    expire_holds(backend, slot_id)

    response = confirm(anonymous, slot_id, hold_id)
    assert response.status_code in (409, 410), (
        f"confirming against a lapsed hold returned {response.status_code}, "
        f"expected a refusal"
    )
    assert backend.one("bookings", slot_id=slot_id) is None, (
        "a confirmation against a lapsed hold still wrote a booking"
    )


def test_confirmed_booking_is_stored_with_its_attendee(anonymous, backend):
    slot_id, hold_id = held_slot(anonymous, backend)
    attendee = fresh_attendee()
    response = confirm(anonymous, slot_id, hold_id, details(attendee))
    assert response.status_code in (200, 201), response.text[:400]

    row = backend.one("bookings", slot_id=slot_id)
    assert row is not None, "confirming stored no booking row"
    assert row["status"] == "confirmed", f"the booking status is {row['status']!r}"
    assert row["attendee_email"] == attendee, (
        f"the booking stores {row['attendee_email']!r} rather than {attendee!r}"
    )


def _contended_confirmations(slot_id):
    """Two callers reach for one slot at the same moment."""

    def attempt():
        with appclient.client() as caller:
            held = place_hold(caller, slot_id)
            hold_id = (held.json().get("id") if held.status_code in (200, 201)
                       else "contended")
            return confirm(caller, slot_id, hold_id, details(fresh_attendee()))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(attempt) for _ in range(2)]
        return [f.result() for f in futures]


def test_concurrent_confirmations_leave_exactly_one_booking(backend):
    free = free_slot_ids(backend)
    assert free, "no free slot is available for the contention check"
    slot_id = free[0]

    _contended_confirmations(slot_id)

    confirmed = [r for r in backend.rows("bookings", slot_id=slot_id)
                 if r["status"] == "confirmed"]
    assert len(confirmed) == 1, (
        f"{len(confirmed)} confirmed bookings exist for one slot after two "
        f"simultaneous confirmations"
    )


def test_concurrent_confirmations_refuse_the_loser(backend):
    free = free_slot_ids(backend)
    assert free, "no free slot is available for the contention check"
    slot_id = free[0]

    responses = _contended_confirmations(slot_id)

    won = [r for r in responses if r.status_code in (200, 201)]
    lost = [r for r in responses if r.status_code not in (200, 201)]
    assert len(won) == 1, (
        "both simultaneous confirmations were accepted: "
        + ", ".join(str(r.status_code) for r in responses)
    )
    assert lost, "one caller received no answer at all"
    assert lost[0].status_code in (409, 410), (
        f"the losing caller received {lost[0].status_code}, expected a conflict"
    )


def test_rejected_confirmation_leaves_no_partial_state(anonymous, backend, inbox):
    slot_id, hold_id = held_slot(anonymous, backend)
    try:
        body = dict(details())
        body["agenda"] = ""
        before = backend.count("bookings")
        mail_before = inbox.count()

        response = confirm(anonymous, slot_id, hold_id, body)
        assert response.status_code in (400, 422), (
            f"an empty agenda returned {response.status_code}, expected a rejection"
        )
        assert backend.count("bookings") == before, (
            "a rejected confirmation still wrote a booking row"
        )
        assert inbox.count() == mail_before, (
            "a refused booking sent mail, and a refused booking sends none"
        )
    finally:
        expire_holds(backend, slot_id)


def test_repeated_idempotency_key_creates_no_second_booking(anonymous, backend):
    slot_id, hold_id = held_slot(anonymous, backend)
    key = f"key-{unique_suffix()}"
    body = details()

    first = confirm(anonymous, slot_id, hold_id, body, key=key)
    assert first.status_code in (200, 201), first.text[:400]
    after_first = backend.count("bookings")

    second = confirm(anonymous, slot_id, hold_id, body, key=key)
    assert second.status_code in (200, 201, 409), second.text[:300]
    assert backend.count("bookings") == after_first, (
        "replaying one idempotency key created a second booking"
    )


def test_agenda_outside_its_range_is_rejected(anonymous, backend):
    slot_id, hold_id = held_slot(anonymous, backend)
    try:
        before = backend.count("bookings")
        body = dict(details())
        body["agenda"] = "x" * 2100

        response = confirm(anonymous, slot_id, hold_id, body)
        assert response.status_code in (400, 422), (
            f"an over-long agenda returned {response.status_code}, expected a rejection"
        )
        assert backend.count("bookings") == before, (
            "an over-long agenda still wrote a booking row"
        )
    finally:
        expire_holds(backend, slot_id)


def test_attendee_name_outside_its_range_is_rejected(anonymous, backend):
    slot_id, hold_id = held_slot(anonymous, backend)
    try:
        before = backend.count("bookings")
        body = dict(details())
        body["attendee_name"] = "x"

        response = confirm(anonymous, slot_id, hold_id, body)
        assert response.status_code in (400, 422), (
            f"a one-character attendee name returned {response.status_code}"
        )
        assert backend.count("bookings") == before, (
            "a one-character attendee name still wrote a booking row"
        )
    finally:
        expire_holds(backend, slot_id)


def test_booking_requires_no_account(backend):
    with appclient.client() as anon:
        slot_id, hold_id = held_slot(anon, backend)
        response = confirm(anon, slot_id, hold_id, details(fresh_attendee()))
    assert response.status_code in (200, 201), (
        f"a signed-out visitor could not complete a booking: {response.status_code}"
    )
    assert backend.one("bookings", slot_id=slot_id) is not None, (
        "the signed-out booking stored no row"
    )


def test_confirmation_message_is_delivered_to_the_attendee(anonymous, backend, inbox):
    slot_id, hold_id = held_slot(anonymous, backend)
    attendee = fresh_attendee()
    sent = confirm(anonymous, slot_id, hold_id, details(attendee))
    assert sent.status_code in (200, 201), sent.text[:400]

    found = inbox.find(to=attendee, subject_contains=SUBJECT_PREFIX)
    assert found is not None, (
        f"no message carrying {SUBJECT_PREFIX!r} reached {attendee}"
    )
    assert inbox.count(to=attendee) == 1, (
        f"{inbox.count(to=attendee)} messages reached {attendee}, expected one"
    )


def test_confirmation_subject_carries_the_pinned_prefix(anonymous, backend, inbox):
    slot_id, hold_id = held_slot(anonymous, backend)
    attendee = fresh_attendee()
    sent = confirm(anonymous, slot_id, hold_id, details(attendee))
    assert sent.status_code in (200, 201), sent.text[:400]

    message = inbox.find(to=attendee, subject_contains=SUBJECT_PREFIX)
    assert message is not None, "the confirmation message never arrived"
    assert message.subject.startswith(SUBJECT_PREFIX), (
        f"the subject is {message.subject!r}, which does not begin {SUBJECT_PREFIX!r}"
    )

    booking = backend.one("bookings", slot_id=slot_id)
    owner = backend.one("accounts", id=booking["principal_id"])
    assert owner["display_name"] in message.subject, (
        f"the subject {message.subject!r} does not name {owner['display_name']!r}"
    )
    if owner["display_name"] == PRINCIPAL_NAME:
        assert message.subject == WORKED_SUBJECT, (
            f"the subject is {message.subject!r}, expected {WORKED_SUBJECT!r}"
        )


def test_confirmation_body_names_the_principal_and_the_time(anonymous, backend, inbox):
    slot_id, hold_id = held_slot(anonymous, backend)
    attendee = fresh_attendee()
    sent = confirm(anonymous, slot_id, hold_id, details(attendee))
    assert sent.status_code in (200, 201), sent.text[:400]

    message = inbox.find(to=attendee, subject_contains=SUBJECT_PREFIX)
    assert message is not None, "the confirmation message never arrived"
    assert message.body.strip(), "the confirmation body is empty"

    booking = backend.one("bookings", slot_id=slot_id)
    owner = backend.one("accounts", id=booking["principal_id"])
    assert owner["display_name"] in message.body, (
        f"the confirmation body does not name {owner['display_name']!r}"
    )

    slot = backend.one("availability_slots", id=slot_id)
    minute = str(slot["starts_at"])[11:16]
    assert minute in message.body, (
        f"the confirmation body does not carry the start time {minute}"
    )


def test_no_mail_is_sent_by_a_hold_or_a_withdrawal(anonymous, principal, backend, inbox):
    before = inbox.count()

    slot_id, _hold_id = held_slot(anonymous, backend)
    expire_holds(backend, slot_id)

    taken = booked_slot_ids(backend)
    account = backend.one("accounts", email=PRINCIPAL_EMAIL)
    free = [r for r in slot_rows(backend, state="published",
                                 principal_id=account["id"])
            if r["id"] not in taken]
    if free:
        principal.post(f"/principal/availability/{free[-1]['id']}/withdraw")

    assert inbox.count() == before, (
        f"the mailbox moved from {before} to {inbox.count()} messages, and neither "
        f"placing a hold nor withdrawing a slot sends mail"
    )


def test_principal_reads_their_own_booking_list(principal, backend):
    response = principal.get("/principal/bookings")
    assert response.status_code == 200, response.text[:300]

    account = backend.one("accounts", email=PRINCIPAL_EMAIL)
    stored = {str(r["id"]) for r in backend.rows("bookings",
                                                 principal_id=account["id"])}
    served = {str(b.get("id")) for b in response.json()}
    assert served <= stored, (
        "the booking list carries bookings belonging to another principal: "
        f"{sorted(served - stored)[:5]}"
    )
    seeded = backend.one("bookings", attendee_email=SEEDED_ATTENDEE)
    if seeded is not None and seeded["principal_id"] == account["id"]:
        assert str(seeded["id"]) in served, (
            f"the seeded booking for {SEEDED_ATTENDEE} is missing from the list"
        )


def test_principal_publishes_availability(principal, backend):
    before = backend.count("availability_slots")
    response = principal.post("/principal/availability", json={
        "starts_at": "2026-11-02T15:00:00Z",
        "ends_at": "2026-11-02T15:15:00Z",
    })
    assert response.status_code in (200, 201), response.text[:400]
    assert backend.count("availability_slots") == before + 1, (
        "publishing availability stored no new slot"
    )


def test_principal_withdraws_an_untaken_slot(principal, backend):
    taken = booked_slot_ids(backend)
    account = backend.one("accounts", email=PRINCIPAL_EMAIL)
    mine = [r for r in slot_rows(backend, state="published",
                                 principal_id=account["id"])
            if r["id"] not in taken]
    assert mine, "the principal holds no untaken published slot"
    slot_id = mine[-1]["id"]

    response = principal.post(f"/principal/availability/{slot_id}/withdraw")
    assert response.status_code in (200, 204), response.text[:300]
    assert backend.one("availability_slots", id=slot_id)["state"] == "withdrawn", (
        "the withdrawn slot did not move to the withdrawn state"
    )


def test_withdrawing_a_booked_slot_is_refused(principal, backend):
    taken = sorted(booked_slot_ids(backend), key=str)
    assert taken, "the seed carries no confirmed booking"
    slot_id = taken[0]

    response = principal.post(f"/principal/availability/{slot_id}/withdraw")
    assert response.status_code in (403, 409), (
        f"withdrawing a booked slot returned {response.status_code}, "
        f"expected a refusal"
    )


def test_withdrawn_slot_keeps_its_confirmed_booking(principal, backend):
    taken = sorted(booked_slot_ids(backend), key=str)
    assert taken, "the seed carries no confirmed booking"
    slot_id = taken[0]
    before = backend.one("bookings", slot_id=slot_id)

    principal.post(f"/principal/availability/{slot_id}/withdraw")

    after = backend.one("bookings", slot_id=slot_id)
    assert after is not None, "a refused withdrawal removed the booking"
    assert after["status"] == "confirmed", (
        f"the booking status moved from {before['status']!r} to {after['status']!r}"
    )
    assert backend.one("availability_slots", id=slot_id)["state"] != "withdrawn", (
        "the slot was withdrawn despite carrying a confirmed booking"
    )


def test_principal_cannot_touch_the_other_principals_availability(
        second_principal, backend):
    owner = backend.one("accounts", email=PRINCIPAL_EMAIL)
    taken = booked_slot_ids(backend)
    theirs = [r for r in slot_rows(backend, state="published",
                                   principal_id=owner["id"])
              if r["id"] not in taken]
    assert theirs, "the first principal holds no untaken published slot"
    slot_id = theirs[0]["id"]

    response = second_principal.post(f"/principal/availability/{slot_id}/withdraw")
    assert response.status_code in (403, 404), (
        f"a withdrawal by {SECOND_PRINCIPAL_EMAIL} against another principal's slot "
        f"returned {response.status_code}"
    )
    assert backend.one("availability_slots", id=slot_id)["state"] == "published", (
        "a cross-principal withdrawal changed the slot"
    )


def test_visitor_is_denied_at_every_principal_endpoint(visitor, backend):
    free = free_slot_ids(backend)
    attempts = {
        "read the booking list": visitor.get("/principal/bookings"),
        "publish availability": visitor.post("/principal/availability", json={
            "starts_at": "2026-11-03T15:00:00Z",
            "ends_at": "2026-11-03T15:15:00Z"}),
    }
    if free:
        attempts["withdraw a slot"] = visitor.post(
            f"/principal/availability/{free[0]}/withdraw")

    for action, response in attempts.items():
        assert response.status_code in (401, 403), (
            f"the session for {VISITOR_EMAIL} was allowed to {action}: "
            f"{response.status_code}"
        )


def test_denied_visitor_write_changes_no_row(visitor, backend):
    before_slots = backend.count("availability_slots")
    before_bookings = backend.count("bookings")

    visitor.post("/principal/availability", json={
        "starts_at": "2026-11-04T15:00:00Z",
        "ends_at": "2026-11-04T15:15:00Z"})

    assert backend.count("availability_slots") == before_slots, (
        "a denied visitor write created an availability slot"
    )
    assert backend.count("bookings") == before_bookings, (
        "a denied visitor write created a booking"
    )


def test_seeded_accounts_carry_their_roles(backend):
    """The app seeds dara@tallow.agency as Dara Okonjo and otis@tallow.agency as
    Otis Vandermeer, both principals, and casey@tallow.agency as Casey Brandt, a
    visitor. Every seeded account accepts the corpus password, and no account
    stores that password in readable form."""
    expected = {
        PRINCIPAL_EMAIL: (PRINCIPAL_NAME, "principal"),
        SECOND_PRINCIPAL_EMAIL: ("Otis Vandermeer", "principal"),
        VISITOR_EMAIL: ("Casey Brandt", "visitor"),
    }
    for email, (name, role) in expected.items():
        row = backend.one("accounts", email=email)
        assert row is not None, f"{email} is not seeded"
        assert row["display_name"] == name, (
            f"{email} carries display name {row['display_name']!r}, expected {name!r}"
        )
        assert row["role"] == role, (
            f"{email} carries role {row['role']!r}, expected {role!r}"
        )
        assert "deku-studio-2026" not in str(row.get("password_hash", "")), (
            f"{email} stores its password rather than a hash of that password"
        )

        token = appclient.login(email, CORPUS_PASSWORD)
        assert token, f"signing in as {email} returned no bearer token"
        with appclient.client(token) as signed_in:
            session = signed_in.get("/session")
            assert session.status_code == 200, session.text[:300]
            body = session.json()
            assert body.get("email") == email, (
                f"the session read returned {body.get('email')!r} for {email}"
            )
            assert body.get("display_name") == name
            assert body.get("role") == role
            leaked = [k for k in body if "password" in k.lower()]
            assert not leaked, (
                f"the session read returned password material for {email}: {leaked}"
            )

    with appclient.client() as no_token:
        anonymous_read = no_token.get("/session")
    with appclient.client("not-a-real-token") as bad_token:
        malformed_read = bad_token.get("/session")
    assert anonymous_read.status_code == 401, (
        f"a session read with no token returned {anonymous_read.status_code}"
    )
    assert malformed_read.status_code == 401, (
        f"a session read with a malformed token returned "
        f"{malformed_read.status_code}, expected the same answer as a missing one"
    )

    with appclient.client() as anon:
        wrong = anon.post("/auth/login", json={"email": PRINCIPAL_EMAIL,
                                               "password": "not-the-password"})
        stranger = "unknown-{0}".format(unique_suffix()) + "@tallow.agency"
        unknown = anon.post("/auth/login", json={"email": stranger,
                                                "password": CORPUS_PASSWORD})
    assert wrong.status_code == unknown.status_code, (
        f"a wrong password answers {wrong.status_code} but an unknown address "
        f"answers {unknown.status_code}, which reveals whether the address exists"
    )
    assert wrong.text == unknown.text, (
        "the two denied sign-ins differ in body, which reveals whether the "
        "address exists"
    )


def test_every_internal_link_on_every_public_route_resolves():
    seen, broken = set(), []
    with _page_client() as page:
        for route in PUBLIC_ROUTES:
            response = page.get(route)
            assert response.status_code == 200, (
                f"public route {route} returned {response.status_code}"
            )
            for href in re.findall(r'href="([^"#?]+)"', response.text):
                if href.startswith(("http://", "https://", "mailto:", "javascript:")):
                    continue
                if not href.startswith("/") or href in seen:
                    continue
                seen.add(href)
                target = page.get(href)
                if target.status_code >= 400:
                    broken.append(f"{href} -> {target.status_code} (from {route})")

    assert seen, "no internal links were found on any public route"
    assert not broken, "internal links that do not resolve: " + "; ".join(broken[:10])


def test_unknown_address_answers_not_found():
    with _page_client() as page:
        response = page.get(f"/no-such-route-{unique_suffix()}")
    assert response.status_code == 404, (
        f"an unknown address answered {response.status_code}, expected 404"
    )
    assert response.text.strip(), "the not-found page is empty"


def test_privacy_page_is_served():
    with _page_client() as page:
        response = page.get("/privacy")
    assert response.status_code == 200, (
        f"the privacy page returned {response.status_code}"
    )
    assert response.text.strip(), "the privacy page is empty"


def test_invalid_form_input_is_rejected_and_writes_nothing(anonymous, backend):
    before = backend.count("bookings")
    response = anonymous.post("/bookings", json={"slot_id": None, "agenda": ""},
                              headers={"Idempotency-Key": f"key-{unique_suffix()}"})
    assert response.status_code in (400, 422), (
        f"an invalid booking body returned {response.status_code}, expected a rejection"
    )
    assert backend.count("bookings") == before, (
        "a rejected booking still wrote a row"
    )

    over_long = anonymous.post(
        "/bookings", json=details(),
        headers={"Idempotency-Key": "k" * 240})
    assert over_long.status_code in (400, 422), (
        f"an idempotency key of 240 characters returned {over_long.status_code}, "
        f"expected a rejection past the ceiling of 200"
    )
    assert backend.count("bookings") == before, (
        "a booking carrying an over-long idempotency key still wrote a row"
    )


def test_declared_stack_and_environment_are_in_use(backend, inbox):
    """The app stores data in PostgreSQL reached through DATABASE_URL and sends
    over real SMTP reached through SMTP_HOST, SMTP_PORT, SMTP_USER and SMTP_PASS.
    Both backing services are already running and reachable."""
    assert os.environ.get("EMAIL_INBOX_API_URL"), (
        "EMAIL_INBOX_API_URL is not set for the verifier"
    )
    assert backend.count("accounts") >= 3, (
        "the declared PostgreSQL datastore holds fewer than the three seeded accounts"
    )
    assert inbox.count() >= 0, "the declared mailbox could not be read"


def test_data_model_tables_and_columns_exist(backend):
    """The app defines eight tables, gives every table its own id, and stores every
    timestamp in UTC. accounts carries email, display_name, role and password_hash.
    productions carries slug, title, client_name, category, duration_seconds,
    sort_index, featured_on_home and home_sort_index. production_galleries carries
    label and sort_index. gallery_images carries caption and sort_index.
    production_credits carries role, person_name and sort_index. availability_slots
    carries principal_id, starts_at, ends_at and state. slot_holds carries slot_id
    and expires_at. bookings carries slot_id, attendee_name, attendee_email,
    attendee_timezone, agenda, status and idempotency_key."""
    expected = {
        "accounts": ["email", "display_name", "role", "password_hash"],
        "productions": ["slug", "title", "client_name", "category",
                        "duration_seconds", "sort_index", "featured_on_home",
                        "home_sort_index"],
        "production_galleries": ["label", "sort_index"],
        "gallery_images": ["caption", "sort_index"],
        "production_credits": ["role", "person_name", "sort_index"],
        "availability_slots": ["principal_id", "starts_at", "ends_at", "state"],
        "slot_holds": ["slot_id", "expires_at"],
        "bookings": ["slot_id", "attendee_name", "attendee_email",
                     "attendee_timezone", "agenda", "status", "idempotency_key"],
    }
    for table, columns in expected.items():
        rows = backend.rows(table, limit=1)
        assert rows, f"table {table} could not be read in id order, or holds no row"
        present = set(rows[0])
        assert "id" in present, f"table {table} carries no id of its own"
        missing = [c for c in columns if c not in present]
        assert not missing, f"table {table} is missing columns {missing}"

    stray = sorted({r["category"] for r in backend.rows("productions")}
                   - set(CATEGORIES))
    assert not stray, (
        f"the seeded productions carry categories outside the closed set of seven: "
        f"{stray}"
    )

    naive = []
    for table, column in (("availability_slots", "starts_at"),
                          ("availability_slots", "ends_at"),
                          ("bookings", "created_at"),
                          ("accounts", "created_at")):
        for row in backend.rows(table, limit=5):
            stamp = row.get(column)
            if stamp is not None and getattr(stamp, "utcoffset", None) is not None:
                offset = stamp.utcoffset()
                if offset is not None and offset.total_seconds() != 0:
                    naive.append(f"{table}.{column} carries offset {offset}")
    assert not naive, "these timestamps are not stored in UTC: " + "; ".join(naive[:5])


def test_deployment_contract_holds(anonymous):
    """The app is reachable at APP_PUBLIC_URL, serves its HTTP API under the /api
    prefix on the same origin, returns 200 from GET /api/health once ready, listens
    on container-internal port 4173 and binds 0.0.0.0 rather than 127.0.0.1 or
    localhost, reading both port values from the environment, and keeps the reserved
    .browser_screenshots/ and .downloads/ directories at the app root."""
    health = anonymous.get("/health")
    assert health.status_code == 200, (
        f"GET /api/health returned {health.status_code} once the app was ready"
    )
    assert os.environ.get("APP_PUBLIC_URL"), "APP_PUBLIC_URL is not set"
    assert appclient.api_base().endswith("/api"), (
        f"the API base is {appclient.api_base()}, which does not end in the /api prefix"
    )
    assert appclient.api_base().startswith(appclient.app_url()), (
        "the API is not served on the same origin as the documents"
    )


def test_every_route_in_the_brief_resolves(anonymous):
    """Every route the brief names resolves: the home page at /, the work index at
    /work, one case study at /work/{slug}, the about page, the contact page, the
    privacy page, the legal page and sign-in."""
    listed = anonymous.get("/productions")
    assert listed.status_code == 200, listed.text[:300]
    slugs = _slugs(listed.json())
    assert slugs, "the catalogue serves no production"

    routes = list(PUBLIC_ROUTES) + ["/sign-in", f"/work/{slugs[0]}"]
    with _page_client() as page:
        for route in routes:
            response = page.get(route)
            assert response.status_code == 200, (
                f"the route {route} returned {response.status_code}"
            )

    present = []
    for route in ABSENT_ROUTES:
        if anonymous.post(route, json={}).status_code not in (404, 405):
            present.append(route)
        if anonymous.get(route).status_code == 200:
            present.append(route)
    assert not present, (
        "the brief names no such surface, yet these answer as though the product "
        f"carries one: {sorted(set(present))}"
    )
