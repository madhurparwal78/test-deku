from __future__ import annotations

import re
from datetime import date, timedelta

import httpx

import appclient
import conftest as fixtures


def test_guest_confirms_a_reservation_that_holds_the_nights(guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    reservation = fixtures.confirmed(guest, quote)
    assert reservation.get("status") in ("confirmed", "pending"), (
        f"a confirm on {fixtures.CEDAR_LOFT} for {checkin}..{checkout} left status "
        f"{reservation.get('status')!r}: {reservation!r}"
    )
    days = {row["local_date"]: row for row in fixtures.calendar(guest, ident)}
    assert days[checkin]["is_available"] is False, (
        f"{checkin} is still available on {fixtures.CEDAR_LOFT} after a reservation "
        f"covering it: {days[checkin]!r}"
    )


def test_signup_refuses_a_duplicate_address(anon):
    response = anon.post("/auth/signup",
                         json={"email": fixtures.GUEST_EMAIL,
                               "password": fixtures.PASSWORD})
    assert response.status_code in fixtures.REFUSED, (
        f"POST /api/auth/signup reusing {fixtures.GUEST_EMAIL} returned "
        f"{response.status_code}, expected a client error: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_login_with_a_wrong_password_is_denied(anon):
    response = anon.post("/auth/login",
                         json={"email": fixtures.GUEST_EMAIL,
                               "password": "not-the-corpus-password"})
    assert response.status_code in (400, 401, 403, 422), (
        f"POST /api/auth/login with a wrong password returned {response.status_code}, "
        f"expected a refusal: {fixtures.body_excerpt(response)}"
    )
    assert "access_token" not in (response.text or ""), (
        f"a denied login still returned a token: {fixtures.body_excerpt(response)}"
    )


def test_search_query_round_trips_through_the_address(anon):
    ident = fixtures.listing_id(anon, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(anon, ident, nights=2)
    query = {"place": "Portland", "checkin": checkin, "checkout": checkout,
             "adults": 2, "children": 1, "infants": 1, "pets": 0}
    first = anon.get("/listings", params=query)
    assert first.status_code == 200, (
        f"a full search returned {first.status_code}: {fixtures.body_excerpt(first)}"
    )
    second = anon.get("/listings", params=query)
    assert second.status_code == 200, (
        f"the same search repeated returned {second.status_code}: "
        f"{fixtures.body_excerpt(second)}"
    )
    left = [row.get("listing_id", row.get("id")) for row in fixtures.as_list(first.json())]
    right = [row.get("listing_id", row.get("id")) for row in fixtures.as_list(second.json())]
    assert left == right, (
        f"one address produced two different result orders: {left!r} then {right!r}"
    )


def test_cursor_from_another_query_is_refused(anon):
    first = anon.get("/listings", params={"place": "Portland", "adults": 2})
    assert first.status_code == 200, (
        f"the first search returned {first.status_code}: {fixtures.body_excerpt(first)}"
    )
    cursor = first.json().get("next_cursor") if isinstance(first.json(), dict) else None
    borrowed = cursor or "not-a-cursor-issued-for-this-query"
    response = anon.get("/listings", params={"place": "Kyoto", "adults": 4,
                                             "cursor": borrowed})
    assert response.status_code in fixtures.REFUSED, (
        f"a cursor carried onto a different query returned {response.status_code}, "
        f"expected a refusal rather than a silent reinterpretation: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_a_dense_search_page_is_not_sparse(anon):
    response = anon.get("/listings", params={"adults": 2})
    assert response.status_code == 200, (
        f"GET /api/listings returned {response.status_code}: "
        f"{fixtures.body_excerpt(response)}"
    )
    rows = fixtures.as_list(response.json())
    for row in rows:
        assert row.get("listing_id", row.get("id")) is not None, (
            f"a search result carries no identifier: {row!r}"
        )
        assert row.get("title"), f"a search result carries no title: {row!r}"


def test_closed_to_arrival_date_is_not_offered_as_a_check_in(anon):
    ident = fixtures.listing_id(anon, fixtures.HARBOUR_COTTAGE)
    days = fixtures.calendar(anon, ident)
    closed = [row for row in days if row.get("closed_to_arrival")]
    assert closed, (
        f"{fixtures.HARBOUR_COTTAGE} carries no date closed to arrival, so the third "
        f"calendar state cannot be observed on the seeded data"
    )
    for row in closed:
        assert row.get("bookable_as_checkin") is False, (
            f"{row.get('local_date')} on {fixtures.HARBOUR_COTTAGE} is closed to "
            f"arrival yet is still offered as a check-in: {row!r}"
        )


def test_range_shorter_than_min_stay_is_refused(guest):
    ident = fixtures.listing_id(guest, fixtures.HARBOUR_COTTAGE)
    days = {row["local_date"]: row for row in fixtures.calendar(guest, ident)}
    long_stay = [row for row in days.values()
                 if (row.get("min_stay") or 1) > 1 and row.get("is_available")
                 and row.get("bookable_as_checkin") is not False]
    assert long_stay, (
        f"{fixtures.HARBOUR_COTTAGE} carries no date with a minimum stay above one "
        f"night, so the rule cannot be observed on the seeded data"
    )
    row = sorted(long_stay, key=lambda entry: entry["local_date"])[0]
    checkin = row["local_date"]
    checkout = (date.fromisoformat(checkin) + timedelta(days=1)).isoformat()
    response = fixtures.quote_attempt(guest, ident, checkin, checkout)
    assert response.status_code in fixtures.REFUSED, (
        f"a one-night range starting {checkin}, where the minimum stay is "
        f"{row.get('min_stay')}, returned {response.status_code}: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_request_to_book_authorises_without_capturing(guest):
    ident = fixtures.listing_id(guest, fixtures.HARBOUR_COTTAGE)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=3)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    reservation = fixtures.confirmed(guest, quote)
    assert reservation.get("status") == "pending", (
        f"a request-to-book confirm on {fixtures.HARBOUR_COTTAGE} left status "
        f"{reservation.get('status')!r}, expected 'pending': {reservation!r}"
    )
    payment = reservation.get("payment") or {}
    assert payment.get("status") == "authorised", (
        f"the payment on a pending reservation is {payment.get('status')!r}, "
        f"expected 'authorised': {reservation!r}"
    )
    assert not payment.get("captured_minor_units"), (
        f"a pending request captured {payment.get('captured_minor_units')!r} minor "
        f"units before the host accepted: {reservation!r}"
    )


def test_host_acceptance_captures_the_authorisation(guest, host):
    ident = fixtures.listing_id(guest, fixtures.HARBOUR_COTTAGE)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=3)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    reservation = fixtures.confirmed(guest, quote)
    booking = fixtures.reservation_id(reservation)
    accepted = host.post(f"/reservations/{booking}/accept")
    assert accepted.status_code in fixtures.OK, (
        f"POST /api/reservations/{booking}/accept returned {accepted.status_code}: "
        f"{fixtures.body_excerpt(accepted)}"
    )
    after = guest.get(f"/reservations/{booking}")
    assert after.status_code == 200, (
        f"reading the accepted reservation returned {after.status_code}: "
        f"{fixtures.body_excerpt(after)}"
    )
    state = after.json()
    payment = state.get("payment") or {}
    assert state.get("status") == "confirmed", (
        f"the accepted reservation is {state.get('status')!r}, expected 'confirmed': "
        f"{state!r}"
    )
    assert payment.get("status") == "captured", (
        f"acceptance left the payment {payment.get('status')!r}, expected 'captured': "
        f"{state!r}"
    )


def test_declined_instrument_creates_no_reservation(guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    response = fixtures.confirm(guest, quote, method=fixtures.PM_DECLINE)
    assert response.status_code in fixtures.REFUSED, (
        f"a confirm with {fixtures.PM_DECLINE} returned {response.status_code}, "
        f"expected a refusal: {fixtures.body_excerpt(response)}"
    )
    days = {row["local_date"]: row for row in fixtures.calendar(guest, ident)}
    assert days[checkin]["is_available"] is True, (
        f"{checkin} is held after a declined authorisation: {days[checkin]!r}"
    )


def test_challenge_instrument_answers_requires_action(guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    response = fixtures.confirm(guest, quote, method=fixtures.PM_CHALLENGE)
    assert response.status_code in fixtures.OK, (
        f"a confirm with {fixtures.PM_CHALLENGE} returned {response.status_code}: "
        f"{fixtures.body_excerpt(response)}"
    )
    payload = response.json()
    payment = payload.get("payment") or {}
    assert "requires_action" in (str(payload.get("status")), str(payment.get("status"))), (
        f"a confirm needing an interactive challenge answered "
        f"{payload.get('status')!r} / {payment.get('status')!r}, expected "
        f"'requires_action': {payload!r}"
    )
    days = {row["local_date"]: row for row in fixtures.calendar(guest, ident)}
    assert days[checkin]["is_available"] is False, (
        f"{checkin} is not held while the challenge is outstanding: {days[checkin]!r}"
    )


def test_unpublishing_a_listing_keeps_its_reservations(guest, other_host):
    ident = fixtures.listing_id(guest, fixtures.KITE_HOUSE)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    booking = fixtures.reservation_id(fixtures.confirmed(guest, quote))
    changed = other_host.patch(f"/host/listings/{ident}", json={"status": "unlisted"})
    assert changed.status_code in fixtures.OK, (
        f"unlisting {fixtures.KITE_HOUSE} returned {changed.status_code}: "
        f"{fixtures.body_excerpt(changed)}"
    )
    after = guest.get(f"/reservations/{booking}")
    assert after.status_code == 200, (
        f"the reservation on an unlisted listing returned {after.status_code}: "
        f"{fixtures.body_excerpt(after)}"
    )
    assert after.json().get("status") in ("confirmed", "pending"), (
        f"unlisting {fixtures.KITE_HOUSE} changed its reservation to "
        f"{after.json().get('status')!r}: {after.json()!r}"
    )
    other_host.patch(f"/host/listings/{ident}", json={"status": "listed"})


def test_refund_quote_precedes_the_cancellation(guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    booking = fixtures.reservation_id(fixtures.confirmed(guest, quote))
    preview = guest.get(f"/reservations/{booking}/refund-quote")
    assert preview.status_code == 200, (
        f"GET /api/reservations/{booking}/refund-quote returned "
        f"{preview.status_code}: {fixtures.body_excerpt(preview)}"
    )
    quoted = preview.json()
    assert isinstance(fixtures.as_list(quoted.get("lines")) or quoted.get("lines"), list), (
        f"the refund quote carries no itemised lines: {quoted!r}"
    )
    cancelled = guest.post(f"/reservations/{booking}/cancel",
                           json={"reason": "plans changed"})
    assert cancelled.status_code in fixtures.OK, (
        f"cancelling {booking} returned {cancelled.status_code}: "
        f"{fixtures.body_excerpt(cancelled)}"
    )
    assert cancelled.json().get("status") == "cancelled", (
        f"the cancelled reservation is {cancelled.json().get('status')!r}: "
        f"{cancelled.json()!r}"
    )


def test_seeded_listing_rows_are_persisted_and_not_duplicated(backend):
    for title in (fixtures.CEDAR_LOFT, fixtures.HARBOUR_COTTAGE,
                  fixtures.KITE_HOUSE, fixtures.SALT_MARSH_CABIN):
        stored = backend.count("listing", title=title)
        assert stored == 1, (
            f"the listing table holds {stored} row(s) titled {title!r}; seeding is "
            f"idempotent, so exactly one is expected"
        )
    days = backend.count("calendar_day")
    assert days > 0, (
        "the calendar_day table is empty; availability is stored as one row per "
        "listing per open local date"
    )


def test_quote_lines_sum_exactly_to_the_quote_total(guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    lines = fixtures.lines_of(quote)
    total = quote.get("total_minor_units")
    assert isinstance(total, int), (
        f"total_minor_units is {total!r}, expected an integer in minor units: {quote!r}"
    )
    summed = sum(int(value) for value in lines.values())
    assert summed == total, (
        f"the displayed lines sum to {summed} while the displayed total is {total}: "
        f"{lines!r}"
    )


def test_authorised_amount_equals_the_quote_total(guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    reservation = fixtures.confirmed(guest, quote)
    payment = reservation.get("payment") or {}
    assert payment.get("authorised_minor_units") == quote.get("total_minor_units"), (
        f"the amount authorised is {payment.get('authorised_minor_units')!r} while "
        f"the quote total was {quote.get('total_minor_units')!r}: {reservation!r}"
    )
    assert payment.get("currency") == quote.get("currency"), (
        f"the authorisation currency is {payment.get('currency')!r} while the quote "
        f"was priced in {quote.get('currency')!r}"
    )


def test_cleaning_fee_is_identical_on_a_long_stay(guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    short_in, short_out = fixtures.bookable_range(guest, ident, nights=2)
    long_in, long_out = fixtures.bookable_range(guest, ident, nights=30)
    short_lines = fixtures.lines_of(fixtures.quote_for(guest, ident, short_in, short_out))
    long_lines = fixtures.lines_of(fixtures.quote_for(guest, ident, long_in, long_out))
    assert short_lines.get(fixtures.LINE_CLEANING) == long_lines.get(fixtures.LINE_CLEANING), (
        f"the cleaning fee is {short_lines.get(fixtures.LINE_CLEANING)!r} on a "
        f"two-night stay and {long_lines.get(fixtures.LINE_CLEANING)!r} on a "
        f"thirty-night one; a per-stay fee does not scale with length"
    )


def test_discount_reduces_the_nightly_subtotal_only(guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=30)
    lines = fixtures.lines_of(fixtures.quote_for(guest, ident, checkin, checkout))
    discount = lines.get(fixtures.LINE_DISCOUNT)
    nightly = lines.get(fixtures.LINE_NIGHTLY)
    assert discount is not None and int(discount) != 0, (
        f"a thirty-night stay on {fixtures.CEDAR_LOFT} carries no length-of-stay "
        f"discount line: {lines!r}"
    )
    assert abs(int(discount)) < int(nightly), (
        f"the discount {discount!r} is not smaller than the nightly subtotal "
        f"{nightly!r}, so it is reaching past the room cost: {lines!r}"
    )


def test_extra_guest_fee_excludes_infants(guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    without = fixtures.lines_of(fixtures.quote_for(
        guest, ident, checkin, checkout, fixtures.party(adults=2, children=2)))
    with_infant = fixtures.lines_of(fixtures.quote_for(
        guest, ident, checkin, checkout,
        fixtures.party(adults=2, children=2, infants=1)))
    assert without.get(fixtures.LINE_EXTRA_GUEST) == with_infant.get(fixtures.LINE_EXTRA_GUEST), (
        f"adding an infant moved the extra-guest fee from "
        f"{without.get(fixtures.LINE_EXTRA_GUEST)!r} to "
        f"{with_infant.get(fixtures.LINE_EXTRA_GUEST)!r}; an infant is not an extra guest"
    )


def test_pet_fee_is_charged_once_per_stay(guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    short_in, short_out = fixtures.bookable_range(guest, ident, nights=2)
    long_in, long_out = fixtures.bookable_range(guest, ident, nights=30)
    short_lines = fixtures.lines_of(fixtures.quote_for(
        guest, ident, short_in, short_out, fixtures.party(adults=2, pets=1)))
    long_lines = fixtures.lines_of(fixtures.quote_for(
        guest, ident, long_in, long_out, fixtures.party(adults=2, pets=1)))
    assert int(short_lines.get(fixtures.LINE_PET) or 0) > 0, (
        f"a party carrying a pet is charged no pet fee: {short_lines!r}"
    )
    assert short_lines.get(fixtures.LINE_PET) == long_lines.get(fixtures.LINE_PET), (
        f"the pet fee is {short_lines.get(fixtures.LINE_PET)!r} on two nights and "
        f"{long_lines.get(fixtures.LINE_PET)!r} on thirty; a per-stay fee is charged once"
    )


def test_per_date_prices_are_summed_across_the_range(guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    lines = fixtures.lines_of(fixtures.quote_for(guest, ident, checkin, checkout))
    days = {row["local_date"]: row for row in fixtures.calendar(guest, ident)}
    spanned = [days[key]["price_minor"] for key in
               [(date.fromisoformat(checkin) + timedelta(days=offset)).isoformat()
                for offset in range(2)]]
    assert int(lines.get(fixtures.LINE_NIGHTLY)) == sum(int(value) for value in spanned), (
        f"the nightly subtotal is {lines.get(fixtures.LINE_NIGHTLY)!r} while the two "
        f"covered dates are priced {spanned!r}; the subtotal sums each date"
    )


def test_tax_drops_to_zero_at_the_exemption_threshold(guest):
    ident = fixtures.listing_id(guest, fixtures.HARBOUR_COTTAGE)
    under_in, under_out = fixtures.bookable_range(guest, ident, nights=29)
    over_in, over_out = fixtures.bookable_range(guest, ident, nights=30)
    under = fixtures.lines_of(fixtures.quote_for(guest, ident, under_in, under_out))
    over = fixtures.lines_of(fixtures.quote_for(guest, ident, over_in, over_out))
    assert int(under.get(fixtures.LINE_TAXES) or 0) > 0, (
        f"a twenty-nine-night stay in Amsterdam carries no tax line: {under!r}"
    )
    assert int(over.get(fixtures.LINE_TAXES) or 0) == 0, (
        f"a thirty-night stay in Amsterdam is exempt yet carries a tax of "
        f"{over.get(fixtures.LINE_TAXES)!r}: {over!r}"
    )


def test_zero_minor_digit_currency_totals_are_whole_units(guest):
    ident = fixtures.listing_id(guest, fixtures.KITE_HOUSE)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    assert (quote.get("currency") or "").lower() == "jpy", (
        f"{fixtures.KITE_HOUSE} priced in {quote.get('currency')!r}, expected 'jpy'"
    )
    total = quote.get("total_minor_units")
    assert isinstance(total, int) and total > 0, (
        f"a yen total is {total!r}; a currency with no minor digits still carries an "
        f"integer amount in its own unit"
    )
    lines = fixtures.lines_of(quote)
    assert sum(int(value) for value in lines.values()) == total, (
        f"the yen lines {lines!r} do not sum to {total}"
    )


def test_policy_snapshot_survives_a_later_policy_edit(guest, host):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    booked = fixtures.confirmed(guest, quote)
    booking = fixtures.reservation_id(booked)
    sold_under = booked.get("policy_snapshot") or quote.get("policy_snapshot")
    assert sold_under, f"the reservation carries no policy_snapshot: {booked!r}"
    host.patch(f"/host/listings/{ident}", json={"cancellation_policy": "strict"})
    after = guest.get(f"/reservations/{booking}")
    assert after.status_code == 200, (
        f"re-reading {booking} returned {after.status_code}: "
        f"{fixtures.body_excerpt(after)}"
    )
    assert after.json().get("policy_snapshot") == sold_under, (
        f"the reservation's stored policy became "
        f"{after.json().get('policy_snapshot')!r} after the host edited the listing; "
        f"it was sold under {sold_under!r}"
    )


def test_approximate_circle_is_stable_across_requests(anon):
    ident = fixtures.listing_id(anon, fixtures.CEDAR_LOFT)
    first = fixtures.listing_detail(anon, ident)
    second = fixtures.listing_detail(anon, ident)
    keys = ("approximate_latitude", "approximate_longitude",
            "approximate_coordinates", "approximate_location")
    present = [key for key in keys if first.get(key) is not None]
    assert present, (
        f"the public listing carries no approximate location field; the keys looked "
        f"for are {keys!r}: {first!r}"
    )
    for key in present:
        assert first[key] == second[key], (
            f"the approximate location {key!r} moved between two reads, from "
            f"{first[key]!r} to {second[key]!r}; sampling a moving circle recovers "
            f"the true point"
        )


def test_duplicate_payment_event_changes_no_stored_row(guest, backend):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    booked = fixtures.confirmed(guest, quote)
    booking = fixtures.reservation_id(booked)
    event = {"event_id": fixtures.unique_key(), "type": "payment.captured",
             "reservation_id": booking, "occurred_at": "2026-01-01T00:00:00Z"}
    with httpx.Client(base_url=appclient.api_base(), timeout=30.0) as hook:
        first = hook.post("/payments/webhook", json=event)
        assert first.status_code in fixtures.OK, (
            f"the first delivery of a payment event returned {first.status_code}: "
            f"{fixtures.body_excerpt(first)}"
        )
        before = backend.count("payment_event")
        second = hook.post("/payments/webhook", json=event)
        assert second.status_code in fixtures.OK, (
            f"a repeated delivery of the same event returned {second.status_code}, "
            f"expected the same acknowledgement: {fixtures.body_excerpt(second)}"
        )
    after = backend.count("payment_event")
    assert after == before, (
        f"re-delivering one event moved the payment_event count from {before} to "
        f"{after}; a handler keyed on the event id applies it once"
    )


def test_guest_cannot_read_another_guests_reservation(guest, other_guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    booking = fixtures.reservation_id(fixtures.confirmed(guest, quote))
    response = other_guest.get(f"/reservations/{booking}")
    assert response.status_code in fixtures.MISSING, (
        f"{fixtures.GUEST2_EMAIL} read reservation {booking}, which belongs to "
        f"{fixtures.GUEST_EMAIL}, with {response.status_code}: "
        f"{fixtures.body_excerpt(response)}"
    )
    mine = guest.get(f"/reservations/{booking}")
    assert mine.status_code == 200, (
        f"the owning guest can no longer read {booking}: "
        f"{fixtures.body_excerpt(mine)}"
    )


def test_host_cannot_read_another_hosts_reservations(guest, other_host):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    booking = fixtures.reservation_id(fixtures.confirmed(guest, quote))
    response = other_host.get(f"/reservations/{booking}")
    assert response.status_code in fixtures.MISSING, (
        f"{fixtures.HOST2_EMAIL} read a reservation on a listing owned by "
        f"{fixtures.HOST_EMAIL} with {response.status_code}: "
        f"{fixtures.body_excerpt(response)}"
    )
    listed = other_host.get("/host/reservations")
    assert listed.status_code == 200, (
        f"a host reading their own reservations got {listed.status_code}: "
        f"{fixtures.body_excerpt(listed)}"
    )
    ids = [str(row.get("reservation_id", row.get("id")))
           for row in fixtures.as_list(listed.json())]
    assert str(booking) not in ids, (
        f"another host's reservation {booking} appears in "
        f"{fixtures.HOST2_EMAIL}'s own list: {ids!r}"
    )


def test_anonymous_mutation_is_denied(anon, guest):
    ident = fixtures.listing_id(anon, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(anon, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    response = anon.post("/reservations",
                         json={"quote_id": quote.get("quote_id"),
                               "payment_method_reference": fixtures.PM_OK},
                         headers={"Idempotency-Key": fixtures.unique_key()})
    assert response.status_code in fixtures.DENIED, (
        f"an unauthenticated confirm returned {response.status_code}, expected a "
        f"denial: {fixtures.body_excerpt(response)}"
    )
    days = {row["local_date"]: row for row in fixtures.calendar(anon, ident)}
    assert days[checkin]["is_available"] is True, (
        f"{checkin} was held by a request carrying no token: {days[checkin]!r}"
    )


def test_unpublished_review_is_absent_from_the_response_body(guest, host):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    booking = fixtures.reservation_id(fixtures.confirmed(guest, quote))
    marker = f"probe-review-{fixtures.unique_key()}"
    submitted = guest.post("/reviews", json={
        "reservation_id": booking, "direction": "guest_to_host", "rating": 5,
        "subratings": {"cleanliness": 5, "accuracy": 5, "checkin": 5,
                       "communication": 5, "location": 5, "value": 5},
        "body": marker})
    assert submitted.status_code in fixtures.OK, (
        f"POST /api/reviews returned {submitted.status_code}: "
        f"{fixtures.body_excerpt(submitted)}"
    )
    public = host.get(f"/listings/{ident}/reviews")
    assert public.status_code == 200, (
        f"reading the listing's reviews returned {public.status_code}: "
        f"{fixtures.body_excerpt(public)}"
    )
    assert marker not in public.text, (
        f"the unpublished review body {marker!r} reached the host before the host "
        f"had written their own: {fixtures.body_excerpt(public)}"
    )


def test_contact_details_are_redacted_before_confirmation(guest):
    threads = guest.get("/threads")
    assert threads.status_code == 200, (
        f"GET /api/threads returned {threads.status_code}: "
        f"{fixtures.body_excerpt(threads)}"
    )
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    opened = guest.post("/threads", json={"listing_id": ident,
                                          "body": "Is the loft free in May?"})
    assert opened.status_code in fixtures.OK, (
        f"opening an inquiry thread returned {opened.status_code}: "
        f"{fixtures.body_excerpt(opened)}"
    )
    thread = opened.json().get("thread_id", opened.json().get("id"))
    reachable = fixtures.unique_email()
    leak = f"reach me on 555-0134 or at {reachable}"
    posted = guest.post(f"/threads/{thread}/messages", json={"body": leak})
    assert posted.status_code in fixtures.OK, (
        f"posting a message returned {posted.status_code}: "
        f"{fixtures.body_excerpt(posted)}"
    )
    read_back = guest.get(f"/threads/{thread}")
    assert read_back.status_code == 200, (
        f"reading the thread returned {read_back.status_code}: "
        f"{fixtures.body_excerpt(read_back)}"
    )
    assert "555-0134" not in read_back.text, (
        f"a phone number survived redaction before confirmation: "
        f"{fixtures.body_excerpt(read_back)}"
    )
    assert reachable not in read_back.text, (
        f"an email address survived redaction before confirmation: "
        f"{fixtures.body_excerpt(read_back)}"
    )


def test_exact_coordinates_are_withheld_before_confirmation(anon):
    ident = fixtures.listing_id(anon, fixtures.CEDAR_LOFT)
    detail = fixtures.listing_detail(anon, ident)
    for key in ("latitude", "longitude", "exact_latitude", "exact_longitude",
                "coordinates", "address"):
        assert detail.get(key) is None, (
            f"the public listing exposes {key!r} to a caller who has not booked: "
            f"{detail!r}"
        )


def test_concurrent_confirms_leave_exactly_one_reservation(guest, backend):
    ident = fixtures.listing_id(guest, fixtures.SALT_MARSH_CABIN)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quotes = [fixtures.quote_for(guest, ident, checkin, checkout)
              for _ in range(fixtures.CONTENDERS)]
    attempts = fixtures.race([
        (lambda held=held: fixtures.confirm(guest, held)) for held in quotes])
    accepted = [r for r in attempts if r.status_code in fixtures.OK]
    refused = [r for r in attempts if r.status_code in fixtures.REFUSED]
    assert len(accepted) == 1, (
        f"{len(accepted)} of {fixtures.CONTENDERS} simultaneous confirms for "
        f"{fixtures.SALT_MARSH_CABIN} {checkin}..{checkout} succeeded, expected "
        f"exactly one; statuses were {[r.status_code for r in attempts]!r}"
    )
    assert len(refused) == fixtures.CONTENDERS - 1, (
        f"{len(refused)} confirms were refused as a conflict, expected "
        f"{fixtures.CONTENDERS - 1}; statuses were "
        f"{[r.status_code for r in attempts]!r}"
    )
    held = backend.count("reservation", listing_id=ident, checkin=checkin)
    assert held == 1, (
        f"the reservation table holds {held} rows for {fixtures.SALT_MARSH_CABIN} "
        f"starting {checkin}; exactly one wins"
    )


def test_adjacent_stays_are_accepted_and_overlaps_refused(guest, other_guest):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    first_in, first_out = fixtures.bookable_range(guest, ident, nights=2)
    fixtures.confirmed(guest, fixtures.quote_for(guest, ident, first_in, first_out))
    adjacent_out = (date.fromisoformat(first_out) + timedelta(days=2)).isoformat()
    adjacent = fixtures.quote_attempt(other_guest, ident, first_out, adjacent_out)
    assert adjacent.status_code in fixtures.OK, (
        f"a stay starting on the previous guest's departure date {first_out} was "
        f"refused with {adjacent.status_code}; ranges may touch: "
        f"{fixtures.body_excerpt(adjacent)}"
    )
    overlap_in = (date.fromisoformat(first_in) + timedelta(days=1)).isoformat()
    overlap_out = (date.fromisoformat(first_out) + timedelta(days=1)).isoformat()
    overlapping = fixtures.quote_attempt(other_guest, ident, overlap_in, overlap_out)
    if overlapping.status_code in fixtures.OK:
        clash = fixtures.confirm(other_guest, overlapping.json())
        assert clash.status_code in fixtures.REFUSED, (
            f"a range {overlap_in}..{overlap_out} overlapping a held reservation was "
            f"confirmed with {clash.status_code}: {fixtures.body_excerpt(clash)}"
        )
    else:
        assert overlapping.status_code in fixtures.REFUSED, (
            f"an overlapping range returned {overlapping.status_code}, expected "
            f"either a quote or a refusal: {fixtures.body_excerpt(overlapping)}"
        )


def test_replayed_idempotency_key_creates_one_reservation(guest, backend):
    ident = fixtures.listing_id(guest, fixtures.CEDAR_LOFT)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=2)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    key = fixtures.unique_key()
    first = fixtures.confirm(guest, quote, key=key)
    assert first.status_code in fixtures.OK, (
        f"the first confirm returned {first.status_code}: "
        f"{fixtures.body_excerpt(first)}"
    )
    second = fixtures.confirm(guest, quote, key=key)
    assert second.status_code in fixtures.OK, (
        f"replaying the same Idempotency-Key returned {second.status_code}, expected "
        f"the original result: {fixtures.body_excerpt(second)}"
    )
    assert fixtures.reservation_id(first.json()) == fixtures.reservation_id(second.json()), (
        f"one key produced two reservations: {fixtures.reservation_id(first.json())!r} "
        f"then {fixtures.reservation_id(second.json())!r}"
    )
    rows = backend.count("reservation", listing_id=ident, checkin=checkin)
    assert rows == 1, (
        f"the reservation table holds {rows} rows for {checkin} after one key was "
        f"replayed; a replay creates no second row"
    )


def test_expired_pending_hold_frees_the_nights(guest, anon):
    ident = fixtures.listing_id(guest, fixtures.HARBOUR_COTTAGE)
    checkin, checkout = fixtures.bookable_range(guest, ident, nights=3)
    quote = fixtures.quote_for(guest, ident, checkin, checkout)
    fixtures.confirmed(guest, quote)
    ttl = fixtures.hold_ttl_seconds()

    def freed():
        days = {row["local_date"]: row for row in fixtures.calendar(anon, ident)}
        return days.get(checkin, {}).get("is_available") is True

    released = fixtures.poll_until(freed, ttl * 2 + fixtures.SETTLE_SECONDS)
    assert released, (
        f"{checkin} on {fixtures.HARBOUR_COTTAGE} is still held more than twice the "
        f"pending-hold lifetime of {ttl} seconds after an abandoned request, with "
        f"nothing having read the reservation"
    )


def test_maintenance_sweep_is_idempotent(anon):
    first = anon.post("/maintenance/release-expired-holds")
    assert first.status_code in fixtures.OK, (
        f"POST /api/maintenance/release-expired-holds returned {first.status_code}: "
        f"{fixtures.body_excerpt(first)}"
    )
    second = anon.post("/maintenance/release-expired-holds")
    assert second.status_code in fixtures.OK, (
        f"a second sweep returned {second.status_code}, expected the same "
        f"acknowledgement: {fixtures.body_excerpt(second)}"
    )


def test_empty_trips_list_is_an_empty_array(fresh_guest):
    response = fresh_guest.get("/trips")
    assert response.status_code == 200, (
        f"a brand-new guest reading /api/trips got {response.status_code}, expected "
        f"an empty result rather than an error: {fixtures.body_excerpt(response)}"
    )
    assert fixtures.as_list(response.json()) == [], (
        f"a guest with no reservations has trips: {fixtures.body_excerpt(response)}"
    )


def test_health_endpoint_returns_two_hundred(anon):
    response = anon.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: "
        f"{fixtures.body_excerpt(response)}"
    )


def test_unknown_route_answers_not_found_with_named_links(anon):
    response = fixtures.html(f"/no-such-place-{fixtures.unique_key()}")
    assert response.status_code == 404, (
        f"an unknown address answered {response.status_code}, expected 404: "
        f"{fixtures.body_excerpt(response)}"
    )
    page = response.text
    for phrase in ("Oops!", "Error code: 404",
                   "Here are some helpful links instead:", "Trust &amp; Safety"):
        needle = phrase.replace("&amp;", "&")
        assert needle in page or phrase in page, (
            f"the not-found view is missing the pinned copy {needle!r}: {page[:400]}"
        )


def test_terms_page_is_reachable(anon):
    response = fixtures.html("/terms")
    assert response.status_code == 200, (
        f"GET /terms returned {response.status_code}: "
        f"{fixtures.body_excerpt(response)}"
    )
    home = fixtures.html("/")
    assert "/terms" in home.text, (
        f"the home route's footer carries no link to /terms: {home.text[:400]}"
    )


def test_public_routes_carry_distinct_titles_and_descriptions(anon):
    seen_titles = []
    seen_descriptions = []
    for path in ("/", "/terms", "/help"):
        page = fixtures.html(path)
        assert page.status_code == 200, (
            f"GET {path} returned {page.status_code}: {page.text[:200]}"
        )
        title = re.search(r"<title[^>]*>(.*?)</title>", page.text, re.S)
        description = re.search(
            r'<meta[^>]+name=["\']description["\'][^>]*content=["\'](.*?)["\']',
            page.text, re.S)
        assert title and title.group(1).strip(), f"{path} carries no title"
        assert description and description.group(1).strip(), (
            f"{path} carries no meta description"
        )
        seen_titles.append(title.group(1).strip())
        seen_descriptions.append(description.group(1).strip())
    assert len(set(seen_titles)) == len(seen_titles), (
        f"two public routes share a title: {seen_titles!r}"
    )
    assert len(set(seen_descriptions)) == len(seen_descriptions), (
        f"two public routes share a description: {seen_descriptions!r}"
    )


def test_link_grid_is_present_in_the_server_markup(anon):
    page = fixtures.html("/")
    assert page.status_code == 200, (
        f"GET / returned {page.status_code}: {page.text[:200]}"
    )
    assert "Inspiration for future getaways" in page.text, (
        f"the link grid heading is absent from the markup the server sent: "
        f"{page.text[:400]}"
    )
    for place in ("Portland", "Kyoto", "Amsterdam"):
        assert place in page.text, (
            f"the link grid in the server markup names no {place} cell: "
            f"{page.text[:400]}"
        )
