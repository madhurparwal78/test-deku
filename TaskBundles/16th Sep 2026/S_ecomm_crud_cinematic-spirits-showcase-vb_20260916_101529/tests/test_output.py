from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor

import httpx
from _shapes import items
from appclient import client
from conftest import (
    ABV_LABEL,
    ACCEPTED,
    ADDITION_ROUTES,
    AGE_QUESTION,
    ALERT_CANCEL_ROUTE,
    ALERT_FIRED_SUBJECT,
    ALERT_OFF_LINE,
    ALERT_SET_SUBJECT,
    BERGEN_LAT,
    BERGEN_LNG,
    BOOKED_SUBJECT,
    CANCELLED_SUBJECT,
    CANCEL_LINK_PREFIX,
    CHAPEL_CAPACITY,
    CHAPTER_KEYS,
    COLLECTION_LABEL,
    CONFLICT,
    CONTROL_NAMES,
    CREATED,
    CURRENCY,
    DENIED,
    DENIED_OR_MISSING,
    FAVICON_ROUTE,
    FLAVOUR_IDS,
    FLAVOUR_MARSHMALLOW,
    FLAVOUR_MINT,
    FLAVOUR_NAMES,
    FLAVOUR_ORANGE,
    GARNISH_IDS,
    GILDED_DISTANCE,
    HOLD_HOURS,
    HOST2_EMAIL,
    HOST_EMAIL,
    ICE_IDS,
    IDEMPOTENCY_HEADER,
    LEITH_LAT,
    LEITH_LNG,
    MAIN_REMAINING_AT_SEED,
    MAIN_TOTAL,
    MIXER_IDS,
    NARRATION_EMPHASIS,
    NARRATION_OPENING,
    NEWPORT_DETAILS,
    NIGHT_PRICE,
    NO_CONTENT,
    OFFER_SUBJECT,
    PARTY_MAX,
    PARTY_MIN,
    PLACE_BERGEN,
    PLACE_LEITH,
    RELEASE_EMBER,
    SESSION_EARLY,
    PLACE_NEWPORT,
    PLACE_SHOREDITCH,
    PLACE_SOHO,
    PORTAL_PROMPT,
    POSTER_PROSE,
    POUR_PROMPT,
    PROMISE_LINE,
    PROMISE_SECOND,
    TITLE_LOCKUP,
    RETAIL_LINE,
    CONTENT_KEYS,
    SESSION_DAYS,
    SEEDED_RELEASES,
    SEEDED_PLACES,
    REASON_INVALID_NAME,
    PUBLIC_ROUTES,
    RADIUS_MAX,
    RADIUS_MIN,
    RATE_LIMITED_STATUS,
    REASON_ALREADY_HELD,
    REASON_ALREADY_RESCHEDULED,
    REASON_CLOSED,
    REASON_EXHAUSTED,
    REASON_HOLD_ELSEWHERE,
    REASON_INSUFFICIENT,
    REASON_INVALID_FLAVOUR,
    REASON_INVALID_INGREDIENT,
    REASON_INVALID_PARTY,
    REASON_INVALID_RADIUS,
    REASON_INVALID_TOKEN,
    REASON_LATE,
    REASON_NAME_REFUSED,
    REASON_NOT_OFFERED,
    REASON_RATE_LIMITED,
    REASON_RESTRICTED,
    REASON_TOO_MANY_MIXERS,
    REFUSED,
    REGION_RESTRICTED,
    RELEASE_CASK,
    RELEASE_CLOSED,
    RELEASE_MAIN,
    RELEASE_SALON,
    RELEASE_SALON_NAME,
    RELEASE_UPCOMING,
    RESTRICTED_NOTICE,
    RITUAL_GONE_LINE,
    RITUAL_SAVES_PER_HOUR,
    RITUAL_SHARED_LINE,
    ROBOTS_ROUTE,
    ROTATE_LINE,
    SALT_DISTANCE,
    SEEDED_PASSWORD_DEFAULT,
    SEEDED_RITUAL_NAME,
    SEEDED_RITUAL_SLUG,
    SESSION_CHAPEL,
    SESSION_LAST_CALL,
    SESSION_LATE_POUR,
    SESSION_NIGHT,
    SESSION_PARIS,
    SESSION_SOLD_OUT,
    SIGN_IN_CODE_PREFIX,
    SIGN_IN_ROUTE,
    SIGN_IN_SUBJECT,
    SITEMAP_ROUTE,
    SLUG_PATTERN,
    SOCIAL_IMAGE_ROUTE,
    SOHO_LAT,
    SOHO_LNG,
    STILL_ROUTE,
    STOCK_READINGS,
    TASTING_NOTES,
    TERMS_ROUTE,
    TINT_TOKENS,
    UNSUPPORTED_LINE,
    UNSUPPORTED_ROUTE,
    VENUE_GILDED,
    VENUE_SALT,
    VISITOR2_EMAIL,
    VISITOR_EMAIL,
    VOLUME_LABEL,
    WITHDRAWN_GARNISH,
    ZONE_LONDON,
    ZONE_PARIS,
    allocation_id_of,
    api,
    body_of,
    book,
    booking_id_of,
    cellar_items,
    claim,
    exchange,
    flat,
    fresh_visitor,
    get_page,
    has_text,
    hold_id_of,
    hold_seats,
    hours_until,
    item_for,
    place_by_name,
    poll_until,
    probe_email,
    probe_suffix,
    reason_of,
    request_link,
    ritual_body,
    session_by_title,
    session_token_of,
    set_alert,
    settle,
    sign_in_code,
    slug_of,
    token_for,
    unescape,
    user_id_of,
    venue_list,
    venues_near,
    wait_for_mail,
)


def test_health_endpoint_reports_ready():
    response = httpx.get(api("/health"), timeout=30.0)
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:400]}"
    )
    assert response.headers.get("x-content-type-options", "").lower() == "nosniff", (
        "GET /api/health carries no nosniff content-type policy header"
    )
    health = body_of(response)
    assert "status" in health and "checks" in health, f"GET /api/health body lacks status or checks: {response.text[:300]}"


def test_seeded_visitor_login_returns_access_token(visitor_token, db):
    assert isinstance(visitor_token, str) and visitor_token.strip(), (
        f"login for {VISITOR_EMAIL} returned no usable access_token: {visitor_token!r}"
    )
    response = httpx.post(api("/auth/login"), timeout=30.0,
                          json={"email": VISITOR_EMAIL, "password": SEEDED_PASSWORD_DEFAULT})
    lifetime = hours_until(body_of(response).get("expiresAt")) / 24.0
    assert SESSION_DAYS - 0.1 < lifetime <= SESSION_DAYS + 0.01, (
        f"a new session lasts {lifetime:.2f} days, expected {SESSION_DAYS}"
    )
    row = db.user_row(VISITOR_EMAIL)
    assert row is not None, (
        f"app_user has no row for {VISITOR_EMAIL}, so the seed never ran"
    )
    assert str(row.get("role")) == "visitor", (
        f"app_user row for {VISITOR_EMAIL} carries role {row.get('role')!r}, expected 'visitor'"
    )
    assert SEEDED_PASSWORD_DEFAULT not in str(row.get("password_hash")), (
        f"app_user.password_hash for {VISITOR_EMAIL} holds the readable password"
    )


def test_login_with_wrong_password_is_denied():
    response = httpx.post(
        api("/auth/login"),
        json={"email": VISITOR_EMAIL, "password": "not-the-seeded-password"},
        timeout=30.0,
    )
    assert response.status_code in DENIED, (
        f"POST /api/auth/login with a wrong password returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}"
    )
    assert "access_token" not in response.text, (
        f"a refused sign-in returned a token: {response.text[:400]}"
    )
    assert reason_of(response) == "invalid_credentials", (
        f"a wrong password was refused with reason {reason_of(response)!r}"
    )


def test_request_without_token_is_denied(db):
    before = db.live_allocations(RELEASE_MAIN)
    with client() as anon:
        me = anon.get("/v1/me")
        shelf = anon.get("/v1/cellar")
        hold = anon.post("/v1/cellar/holds",
                         json={"releaseId": RELEASE_MAIN, "flavour": FLAVOUR_MINT})
    for label, response in (("GET /api/v1/me", me), ("GET /api/v1/cellar", shelf),
                            ("POST /api/v1/cellar/holds", hold)):
        assert response.status_code in DENIED, (
            f"{label} without a token returned {response.status_code}, expected a denial: "
            f"{response.text[:300]}"
        )
    assert db.live_allocations(RELEASE_MAIN) == before, (
        f"an anonymous hold request changed the live allocations of {RELEASE_MAIN}"
    )
    assert me.status_code == 401 and reason_of(me) == "unauthenticated", (
        f"GET /api/v1/me without a token answered {me.status_code} {reason_of(me)!r}"
    )


def test_malformed_token_is_denied():
    with client("not-a-real-session-token") as bad:
        response = bad.get("/v1/me")
    assert response.status_code in DENIED, (
        f"GET /api/v1/me with a malformed token returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}"
    )


def test_logout_revokes_the_session():
    token = token_for(VISITOR_EMAIL)
    with client(token) as signed_in:
        before = signed_in.get("/v1/me")
        assert before.status_code == 200, (
            f"GET /api/v1/me with a fresh token returned {before.status_code}: {before.text[:300]}"
        )
        out = signed_in.post("/auth/logout")
        assert out.status_code in NO_CONTENT, (
            f"POST /api/auth/logout returned {out.status_code}: {out.text[:300]}"
        )
        after = signed_in.get("/v1/me")
    assert after.status_code in DENIED, (
        f"GET /api/v1/me after sign-out returned {after.status_code}, expected a denial"
    )


def test_sign_in_link_email_is_delivered(inbox):
    email = probe_email("link")
    response = request_link(email)
    assert response.status_code in ACCEPTED, (
        f"POST /api/v1/auth/link returned {response.status_code}: {response.text[:300]}"
    )
    message = wait_for_mail(inbox, email, SIGN_IN_SUBJECT)
    assert message is not None, (
        f"no message titled {SIGN_IN_SUBJECT!r} reached {email} through Mailpit"
    )
    assert SIGN_IN_CODE_PREFIX.lower() in message.body.lower(), (
        f"the sign-in message body does not carry {SIGN_IN_CODE_PREFIX!r}: {message.body[:300]!r}"
    )
    assert "/sign-in/verify?token=" in message.body, (
        f"the sign-in message carries no /sign-in/verify?token= link: {message.body[:300]!r}"
    )
    assert len(message.to) == 1 and email.lower() in message.to[0].lower(), (
        f"the sign-in message is addressed to {message.to}, expected {email} alone"
    )


def test_sign_in_link_request_creates_no_account(db):
    email = probe_email("noacct")
    response = request_link(email)
    assert response.status_code == 202, (
        f"POST /api/v1/auth/link returned {response.status_code}, expected 202: {response.text[:300]}"
    )
    settle()
    assert db.count_users(email) == 0, (
        f"asking for a sign-in link created an app_user row for {email} before any exchange"
    )


def test_sign_in_code_exchange_opens_a_visitor_account(inbox, db):
    email, token = fresh_visitor(inbox, "open")
    with client(token) as fresh:
        me = fresh.get("/v1/me")
    assert me.status_code == 200, f"GET /api/v1/me returned {me.status_code}: {me.text[:300]}"
    body = body_of(me)
    assert str(body.get("email")).lower() == email.lower(), (
        f"GET /api/v1/me returned email {body.get('email')!r}, expected {email!r}"
    )
    assert str(body.get("role")) == "visitor", (
        f"a link-opened account has role {body.get('role')!r}, expected 'visitor'"
    )
    row = db.user_row(email.lower())
    assert row is not None, f"app_user has no row for {email} after the exchange"
    assert not row.get("password_hash"), (
        f"the link-opened account {email} carries a password_hash"
    )


def test_sign_in_code_works_only_once(inbox):
    email = probe_email("once")
    request_link(email)
    code = sign_in_code(inbox, email)
    first = exchange(code)
    assert first.status_code in CREATED, (
        f"the first exchange returned {first.status_code}: {first.text[:300]}"
    )
    session_token_of(first)
    second = exchange(code)
    assert second.status_code in DENIED + REFUSED, (
        f"a second exchange of one code returned {second.status_code}, expected a denial: "
        f"{second.text[:300]}"
    )
    assert '"session"' not in second.text, (
        f"a second exchange of one code returned a session: {second.text[:300]}"
    )


def test_unknown_sign_in_code_is_denied():
    response = exchange(f"unknown{probe_suffix()}{probe_suffix()}")
    assert response.status_code in DENIED + REFUSED, (
        f"an unknown code returned {response.status_code}: {response.text[:300]}"
    )
    assert reason_of(response) == REASON_INVALID_TOKEN, (
        f"an unknown code was refused with reason {reason_of(response)!r}, expected "
        f"{REASON_INVALID_TOKEN!r}"
    )


def test_content_document_lists_three_flavours_with_tasting_notes():
    response = httpx.get(api("/v1/content"), timeout=30.0)
    assert response.status_code == 200, (
        f"GET /api/v1/content returned {response.status_code}: {response.text[:300]}"
    )
    body = response.json()
    flavours = {str(f.get("id")): f for f in body.get("flavours", [])}
    assert set(flavours) == set(FLAVOUR_IDS), (
        f"GET /api/v1/content lists flavour ids {sorted(flavours)}, expected {sorted(FLAVOUR_IDS)}"
    )
    names = {str(f.get("name")) for f in flavours.values()}
    assert names == set(FLAVOUR_NAMES), f"flavour names are {sorted(names)}"
    for flavour_id, notes in TASTING_NOTES.items():
        assert str(flavours[flavour_id].get("tastingNotes")) == notes, (
            f"{flavour_id} carries tastingNotes {flavours[flavour_id].get('tastingNotes')!r}"
        )
    tints = {str(f.get("tintToken")) for f in flavours.values()}
    assert tints == set(TINT_TOKENS), f"flavour tint tokens are {sorted(tints)}"
    assert str(flavours[FLAVOUR_MARSHMALLOW].get("tintToken")) == "flavour-a", (
        "the marshmallow flavour does not carry the flavour-a tint"
    )
    assert str(flavours[FLAVOUR_ORANGE].get("tintToken")) == "flavour-c", "the orange flavour does not carry the flavour-c tint"
    assert str(flavours[FLAVOUR_MINT].get("tintToken")) == "flavour-b", "the mint flavour does not carry the flavour-b tint"


def test_content_document_lists_eighteen_chapters_in_order():
    body = httpx.get(api("/v1/content"), timeout=30.0).json()
    for key in CONTENT_KEYS:
        assert key in body, f"GET /api/v1/content carries no {key!r} field"
    chapters = sorted(body.get("chapters", []), key=lambda c: int(c.get("position")))
    keys = tuple(str(c.get("key")) for c in chapters)
    assert keys == CHAPTER_KEYS, f"chapters in position order are {keys}"
    assert [int(c.get("position")) for c in chapters] == list(range(18)), (
        "chapter positions are not 0 to 17"
    )
    lines = " ".join(str(line.get("text")) for c in chapters for line in c.get("lines", []))
    assert NARRATION_OPENING in lines, f"no chapter line carries {NARRATION_OPENING!r}"
    assert NARRATION_EMPHASIS in flat(body).upper(), (
        f"no narration line carries the emphasis {NARRATION_EMPHASIS!r}"
    )


def test_content_document_carries_no_colour_values():
    response = httpx.get(api("/v1/content"), timeout=30.0)
    assert response.status_code == 200, f"GET /api/v1/content returned {response.status_code}"
    assert not re.search(r"#[0-9a-fA-F]{6}\b", response.text), (
        "GET /api/v1/content carries a literal colour value"
    )
    assert not re.search(r"rgba?\(", response.text), (
        "GET /api/v1/content carries a literal rgb colour value"
    )


def test_home_page_html_carries_the_story_text():
    response = get_page("/")
    assert response.status_code == 200, f"GET / returned {response.status_code}"
    html = response.text
    for needle in (TITLE_LOCKUP, NARRATION_OPENING, POSTER_PROSE, PROMISE_LINE, PROMISE_SECOND,
                   RETAIL_LINE, ABV_LABEL, VOLUME_LABEL, COLLECTION_LABEL) + FLAVOUR_NAMES:
        assert has_text(html, needle), (
            f"the HTML of / as sent by the server does not contain {needle!r}"
        )
    for notes in TASTING_NOTES.values():
        assert has_text(html, notes), f"the HTML of / lacks the tasting notes {notes!r}"
    for needle in ("VESPERI", "SPIRITS", "NOCTURNE", "COLLECTION", "WHAT HAPPENS",
                   "NEXT IS UP TO YOU", "AN ODE TO THE NIGHT, YOUR NIGHT"):
        assert has_text(html, needle), f"the HTML of / lacks the collection copy {needle!r}"
    for secret in ("deku-local-dev", "postgresql://", "SMTP_PASS"):
        assert secret not in html, f"the HTML of / carries {secret!r}"


def test_home_page_html_names_every_control():
    html = get_page("/").text
    for needle in CONTROL_NAMES + (AGE_QUESTION, ROTATE_LINE, PORTAL_PROMPT, POUR_PROMPT):
        assert has_text(html, needle), (
            f"the HTML of / as sent by the server does not contain {needle!r}"
        )


def test_still_page_lists_product_data():
    response = get_page(STILL_ROUTE)
    assert response.status_code == 200, f"GET {STILL_ROUTE} returned {response.status_code}"
    html = unescape(response.text)
    assert "<dl" in html.lower(), f"{STILL_ROUTE} carries no description list"
    for needle in (ABV_LABEL, VOLUME_LABEL, NARRATION_OPENING) + FLAVOUR_NAMES:
        assert has_text(html, needle), f"{STILL_ROUTE} does not contain {needle!r}"


def test_unsupported_route_states_the_refusal():
    response = get_page(UNSUPPORTED_ROUTE)
    assert response.status_code == 200, f"GET {UNSUPPORTED_ROUTE} returned {response.status_code}"
    assert has_text(response.text, UNSUPPORTED_LINE), (
        f"{UNSUPPORTED_ROUTE} does not say {UNSUPPORTED_LINE!r}"
    )
    assert "mode=still" in response.text, f"{UNSUPPORTED_ROUTE} carries no link to the still page"


def test_seeded_releases_report_stock(db):
    main = httpx.get(api(f"/v1/releases/{RELEASE_MAIN}"), timeout=30.0)
    assert main.status_code == 200, (
        f"GET /api/v1/releases/{RELEASE_MAIN} returned {main.status_code}: {main.text[:300]}"
    )
    body = body_of(main)
    assert int(body.get("total")) == MAIN_TOTAL, f"{RELEASE_MAIN} total is {body.get('total')}"
    assert int(body.get("claimed")) + int(body.get("remaining")) == MAIN_TOTAL, (
        f"{RELEASE_MAIN} claimed {body.get('claimed')} plus remaining {body.get('remaining')} "
        f"does not equal its total"
    )
    assert int(body.get("claimed")) == db.live_allocations(RELEASE_MAIN), (
        f"{RELEASE_MAIN} reports claimed {body.get('claimed')} but the allocation table holds "
        f"{db.live_allocations(RELEASE_MAIN)} live rows"
    )
    assert int(body.get("remaining")) <= MAIN_REMAINING_AT_SEED, (
        f"{RELEASE_MAIN} reports remaining {body.get('remaining')}, above the seeded "
        f"{MAIN_REMAINING_AT_SEED}"
    )
    listed = httpx.get(api("/v1/releases"), timeout=30.0)
    assert listed.status_code == 200 and RELEASE_MAIN in {str(r.get("id")) for r in items(listed.json())}, (
        f"GET /api/v1/releases does not list {RELEASE_MAIN}: {listed.text[:300]}"
    )
    row = db.release_row(RELEASE_CASK)
    assert row is not None and int(row.get("total")) == 1, (
        f"release {RELEASE_CASK} is not seeded with a total of 1"
    )


def test_cellar_hold_is_persisted_with_a_72_hour_expiry(inbox, db):
    email, token = fresh_visitor(inbox, "hold")
    with client(token) as fresh:
        response = claim(fresh, RELEASE_MAIN, FLAVOUR_MINT)
        assert response.status_code in CREATED, (
            f"POST /api/v1/cellar/holds returned {response.status_code}: {response.text[:300]}"
        )
        allocation_id = allocation_id_of(response)
        entry = item_for(fresh, allocation_id)
    assert str(entry.get("state")) == "held", f"the new item reads state {entry.get('state')!r}"
    assert str(entry.get("flavour")) == FLAVOUR_MINT, f"the item carries flavour {entry.get('flavour')!r}"
    hours = hours_until(entry.get("expiresAt"))
    assert HOLD_HOURS - 0.5 < hours <= HOLD_HOURS + 0.1, (
        f"the hold expires {hours:.2f} hours from now, expected {HOLD_HOURS}"
    )
    row = db.allocation_row(allocation_id)
    assert row is not None, f"allocation has no row with id {allocation_id}"
    assert str(row.get("state")) == "held", f"the stored allocation reads {row.get('state')!r}"
    assert str(row.get("release_id")) == RELEASE_MAIN, "the stored allocation names another release"
    assert row.get("user_id") == user_id_of(db, email.lower()), (
        "the stored allocation belongs to a different account"
    )


def test_cellar_hold_with_invalid_flavour_is_refused(inbox, db):
    email, token = fresh_visitor(inbox, "badflav")
    with client(token) as fresh:
        response = claim(fresh, RELEASE_MAIN, "banana-rum")
    assert response.status_code in REFUSED, (
        f"a hold for an unknown flavour returned {response.status_code}: {response.text[:300]}"
    )
    assert reason_of(response) == REASON_INVALID_FLAVOUR, (
        f"the refusal reason is {reason_of(response)!r}, expected {REASON_INVALID_FLAVOUR!r}"
    )
    assert db.allocations_for_user(user_id_of(db, email.lower())) == [], (
        "a refused hold wrote an allocation row"
    )


def test_cellar_hold_on_closed_release_is_refused(inbox, db):
    email, token = fresh_visitor(inbox, "closed")
    with client(token) as fresh:
        for release_id in (RELEASE_CLOSED, RELEASE_UPCOMING):
            response = claim(fresh, release_id, FLAVOUR_ORANGE)
            assert response.status_code in CONFLICT, (
                f"a hold on {release_id} returned {response.status_code}, expected 409: "
                f"{response.text[:300]}"
            )
            assert reason_of(response) == REASON_CLOSED, (
                f"the refusal on {release_id} carries reason {reason_of(response)!r}"
            )
    assert db.allocations_for_user(user_id_of(db, email.lower())) == [], (
        "a refused hold outside the release window wrote an allocation row"
    )


def test_second_live_hold_on_same_release_is_refused(inbox, db):
    email, token = fresh_visitor(inbox, "twice")
    with client(token) as fresh:
        first = claim(fresh, RELEASE_MAIN, FLAVOUR_ORANGE)
        assert first.status_code in CREATED, f"the first hold returned {first.status_code}"
        second = claim(fresh, RELEASE_MAIN, FLAVOUR_MINT)
    assert second.status_code in REFUSED, (
        f"a second hold on {RELEASE_MAIN} returned {second.status_code}: {second.text[:300]}"
    )
    assert reason_of(second) == REASON_ALREADY_HELD, (
        f"the second hold was refused with {reason_of(second)!r}, expected {REASON_ALREADY_HELD!r}"
    )
    rows = db.allocations_for_user(user_id_of(db, email.lower()))
    assert len(rows) == 1, f"the account holds {len(rows)} allocation rows, expected 1"


def test_idempotent_hold_retry_consumes_one_allocation(inbox, db):
    email, token = fresh_visitor(inbox, "idem")
    key = f"hold-{probe_suffix()}"
    with client(token) as fresh:
        first = claim(fresh, RELEASE_MAIN, FLAVOUR_MARSHMALLOW, key=key)
        again = claim(fresh, RELEASE_MAIN, FLAVOUR_MARSHMALLOW, key=key)
    assert first.status_code in CREATED, f"the first hold returned {first.status_code}"
    assert again.status_code in CREATED, (
        f"a retry with the same {IDEMPOTENCY_HEADER} returned {again.status_code}: {again.text[:300]}"
    )
    assert allocation_id_of(first) == allocation_id_of(again), (
        "a retry with the same key returned a different allocation"
    )
    rows = db.allocations_for_user(user_id_of(db, email.lower()))
    assert len(rows) == 1, f"a retried hold produced {len(rows)} allocation rows"


def test_concurrent_claims_on_last_allocation_leave_one_hold(inbox, db):
    first_email, first_token = fresh_visitor(inbox, "racea")
    second_email, second_token = fresh_visitor(inbox, "raceb")
    before = httpx.get(api(f"/v1/releases/{RELEASE_CASK}"), timeout=30.0)
    remaining_before = int(body_of(before).get("remaining"))

    def attempt(token):
        with client(token) as c:
            return claim(c, RELEASE_CASK, FLAVOUR_ORANGE)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(attempt, (first_token, second_token)))
    statuses = sorted(r.status_code for r in results)
    held = [r for r in results if r.status_code in CREATED]
    lost = [r for r in results if r.status_code in CONFLICT]
    assert len(held) + len(lost) == 2, f"the two simultaneous claims answered {statuses}"
    assert len(held) <= 1, f"two simultaneous claims on {RELEASE_CASK} both succeeded: {statuses}"
    if remaining_before == 1:
        assert len(held) == 1, f"the last bottle of {RELEASE_CASK} went to nobody: {statuses}"
    for response in lost:
        assert reason_of(response) == REASON_EXHAUSTED, (
            f"the losing claim carries reason {reason_of(response)!r}, expected {REASON_EXHAUSTED!r}"
        )
        assert int(body_of(response).get("position")) >= 1, (
            f"the losing claim carries no waitlist position: {response.text[:300]}"
        )
    assert db.live_allocations(RELEASE_CASK) <= 1, (
        f"{RELEASE_CASK} has {db.live_allocations(RELEASE_CASK)} live allocations against a total of 1"
    )


def test_released_hold_is_offered_to_the_waitlist_by_email(inbox, db):
    holder_email, holder_token = fresh_visitor(inbox, "salona")
    waiter_email, waiter_token = fresh_visitor(inbox, "salonb")
    third_email, third_token = fresh_visitor(inbox, "salonc")
    fourth_email, fourth_token = fresh_visitor(inbox, "salond")
    with client(holder_token) as holder, client(waiter_token) as waiter, \
            client(third_token) as third, client(fourth_token) as fourth:
        held = claim(holder, RELEASE_SALON, FLAVOUR_MINT)
        assert held.status_code in CREATED, (
            f"the first hold on {RELEASE_SALON} returned {held.status_code}: {held.text[:300]}"
        )
        queued = claim(waiter, RELEASE_SALON, FLAVOUR_MINT)
        assert queued.status_code in CONFLICT, (
            f"a hold on an exhausted release returned {queued.status_code}: {queued.text[:300]}"
        )
        assert reason_of(queued) == REASON_EXHAUSTED, f"reason was {reason_of(queued)!r}"
        assert int(body_of(queued).get("position")) == 1, (
            f"the first visitor in line was told position {body_of(queued).get('position')}"
        )
        behind = claim(third, RELEASE_SALON, FLAVOUR_MINT)
        assert reason_of(behind) == REASON_EXHAUSTED and int(body_of(behind).get("position")) == 2, (
            f"the second visitor in line was told {behind.status_code} {behind.text[:200]}"
        )
        assert int(body_of(claim(fourth, RELEASE_SALON, FLAVOUR_MINT)).get("position")) == 3, (
            "the third visitor in line was not told position 3"
        )
        settle()
        assert inbox.count(to=waiter_email) == 1, "joining a waitlist sent a message"
        waiting = [e for e in cellar_items(waiter) if str(e.get("releaseId")) == RELEASE_SALON]
        assert waiting and str(waiting[0].get("state")) == "waitlisted", (
            f"the waiting visitor's shelf item reads {waiting}"
        )
        released = holder.delete(f"/v1/cellar/holds/{allocation_id_of(held)}")
        assert released.status_code in NO_CONTENT, (
            f"releasing the hold returned {released.status_code}: {released.text[:300]}"
        )
        offered = poll_until(lambda: [e for e in cellar_items(waiter)
                                      if str(e.get("releaseId")) == RELEASE_SALON
                                      and str(e.get("state")) == "offered"])
        assert offered, "the first waitlisted visitor was not offered the released bottle"
        message = wait_for_mail(inbox, waiter_email, OFFER_SUBJECT)
        assert message is not None, f"no message titled {OFFER_SUBJECT!r} reached {waiter_email}"
        assert RELEASE_SALON_NAME.lower() in message.subject.lower(), (
            f"the offer subject {message.subject!r} does not name {RELEASE_SALON_NAME!r}"
        )
        moved_up = [e for e in cellar_items(third) if str(e.get("releaseId")) == RELEASE_SALON]
        assert moved_up and int(moved_up[0].get("position")) == 1, (
            f"the visitor behind did not close up to position 1: {moved_up}"
        )
        left = third.delete(f"/v1/cellar/holds/{moved_up[0]['allocationId']}")
        assert left.status_code in NO_CONTENT, f"leaving the waitlist returned {left.status_code}"
        last = [e for e in cellar_items(fourth) if str(e.get("releaseId")) == RELEASE_SALON]
        assert last and int(last[0].get("position")) == 1, (
            f"the visitor behind did not move up after someone ahead left: {last}"
        )
        declined = waiter.post(f"/v1/cellar/holds/{offered[0]['allocationId']}/decline")
        assert declined.status_code in CREATED and str(body_of(declined).get("state")) == "declined", (
            f"declining the offer returned {declined.status_code}: {declined.text[:300]}"
        )
        passed = poll_until(lambda: [e for e in cellar_items(fourth)
                                     if str(e.get("releaseId")) == RELEASE_SALON
                                     and str(e.get("state")) == "offered"])
        assert passed, "a declined offer did not pass to the next visitor in line"
        assert wait_for_mail(inbox, fourth_email, OFFER_SUBJECT) is not None, (
            f"no offer message reached {fourth_email} after the decline"
        )
        accepted = fourth.post(f"/v1/cellar/holds/{passed[0]['allocationId']}/accept")
        assert accepted.status_code in CREATED, (
            f"accepting the offer returned {accepted.status_code}: {accepted.text[:300]}"
        )
        assert str(body_of(accepted).get("state")) == "held", (
            f"an accepted offer reads {body_of(accepted).get('state')!r}"
        )
    assert inbox.find(to=holder_email, subject_contains=OFFER_SUBJECT) is None, (
        "the visitor who released the bottle was sent an offer message"
    )
    settle()
    assert inbox.count(to=holder_email) == 1, "releasing a hold sent its owner a message"
    assert inbox.count(to=waiter_email) == 2, "declining an offer sent a further message"
    assert inbox.count(to=third_email) == 1, "leaving a waitlist sent a message"


def test_confirm_is_idempotent(inbox):
    email, token = fresh_visitor(inbox, "confirm")
    with client(token) as fresh:
        held = claim(fresh, RELEASE_MAIN, FLAVOUR_ORANGE)
        allocation_id = allocation_id_of(held)
        first = fresh.post(f"/v1/cellar/holds/{allocation_id}/confirm")
        second = fresh.post(f"/v1/cellar/holds/{allocation_id}/confirm")
    for label, response in (("first", first), ("second", second)):
        assert response.status_code in CREATED, (
            f"the {label} confirm returned {response.status_code}: {response.text[:300]}"
        )
        assert str(body_of(response).get("state")) == "confirmed", (
            f"the {label} confirm returned state {body_of(response).get('state')!r}"
        )
    settle()
    assert inbox.count(to=email) == 1, "confirming a hold sent a message"


def test_accept_without_offer_is_refused(inbox, db):
    email, token = fresh_visitor(inbox, "notoffer")
    with client(token) as fresh:
        held = claim(fresh, RELEASE_MAIN, FLAVOUR_MINT)
        allocation_id = allocation_id_of(held)
        response = fresh.post(f"/v1/cellar/holds/{allocation_id}/accept")
    assert response.status_code in REFUSED, (
        f"accepting a held item returned {response.status_code}: {response.text[:300]}"
    )
    assert reason_of(response) == REASON_NOT_OFFERED, f"reason was {reason_of(response)!r}"
    assert str(db.allocation_row(allocation_id).get("state")) == "held", (
        "a refused accept changed the allocation"
    )


def test_other_visitor_cannot_release_a_hold(inbox, db, visitor2_client):
    email, token = fresh_visitor(inbox, "owner")
    with client(token) as fresh:
        allocation_id = allocation_id_of(claim(fresh, RELEASE_MAIN, FLAVOUR_ORANGE))
    release = visitor2_client.delete(f"/v1/cellar/holds/{allocation_id}")
    confirm = visitor2_client.post(f"/v1/cellar/holds/{allocation_id}/confirm")
    for label, response in (("release", release), ("confirm", confirm)):
        assert response.status_code in DENIED_OR_MISSING, (
            f"another visitor's {label} returned {response.status_code}: {response.text[:300]}"
        )
    assert str(db.allocation_row(allocation_id).get("state")) == "held", (
        "another visitor changed an allocation that is not theirs"
    )


def test_empty_cellar_returns_an_empty_list(visitor_client):
    response = visitor_client.get("/v1/cellar")
    assert response.status_code == 200, f"GET /api/v1/cellar returned {response.status_code}"
    body = response.json()
    assert isinstance(body, dict) and body.get("items") == [], (
        f"the seeded empty shelf for {VISITOR_EMAIL} answered {response.text[:300]}"
    )


def test_no_email_is_sent_when_a_hold_is_granted(inbox):
    email, token = fresh_visitor(inbox, "quiet")
    with client(token) as fresh:
        response = claim(fresh, RELEASE_MAIN, FLAVOUR_MARSHMALLOW)
    assert response.status_code in CREATED, f"the hold returned {response.status_code}"
    settle()
    settle()
    assert inbox.count(to=email) == 1, (
        f"{email} received {inbox.count(to=email)} messages; only the sign-in link was expected"
    )


def test_places_search_lists_every_match():
    response = httpx.get(api("/v1/places"), params={"q": PLACE_NEWPORT}, timeout=30.0)
    assert response.status_code == 200, f"GET /api/v1/places returned {response.status_code}"
    assert isinstance(response.json(), list), "GET /api/v1/places does not return a top-level JSON array"
    matches = [p for p in items(response.json()) if str(p.get("name")) == PLACE_NEWPORT]
    assert len(matches) == 2, f"a search for {PLACE_NEWPORT} listed {len(matches)} places"
    details = " ".join(str(p.get("detail")) for p in matches)
    for detail in NEWPORT_DETAILS:
        assert detail in details, f"the two Newports do not carry the detail {detail!r}"
    lower = httpx.get(api("/v1/places"), params={"q": "sou"}, timeout=30.0)
    assert any(str(p.get("name")) == PLACE_SOHO for p in items(lower.json())), (
        "a lower-case prefix search does not find Soho"
    )


def test_venues_are_sorted_by_distance_within_radius():
    response = venues_near(SOHO_LAT, SOHO_LNG, 5)
    assert response.status_code == 200, (
        f"GET /api/v1/venues returned {response.status_code}: {response.text[:300]}"
    )
    venues = venue_list(response)
    names = [str(v.get("name")) for v in venues]
    assert names == [VENUE_GILDED, VENUE_SALT], f"venues within 5 km of Soho are {names}"
    distances = [f"{float(v.get('distance')):.1f}" for v in venues]
    assert distances == [GILDED_DISTANCE, SALT_DISTANCE], f"distances are {distances}"
    near = venue_list(venues_near(SOHO_LAT, SOHO_LNG, 3))
    assert [str(v.get("name")) for v in near] == [VENUE_GILDED], (
        f"venues within 3 km of Soho are {[v.get('name') for v in near]}"
    )
    for venue in venues:
        assert str(venue.get("stock")) in STOCK_READINGS, f"stock reads {venue.get('stock')!r}"


def test_radius_outside_bounds_is_refused():
    for radius in (RADIUS_MIN - 1, RADIUS_MAX + 1):
        response = venues_near(SOHO_LAT, SOHO_LNG, radius)
        assert response.status_code in REFUSED, (
            f"radius {radius} returned {response.status_code}: {response.text[:300]}"
        )
        assert reason_of(response) == REASON_INVALID_RADIUS, f"reason was {reason_of(response)!r}"


def test_stale_stock_reading_reports_unknown(db):
    venues = venue_list(venues_near(SOHO_LAT, SOHO_LNG, 5, flavour=FLAVOUR_MINT))
    gilded = [v for v in venues if str(v.get("name")) == VENUE_GILDED]
    assert gilded, "The Gilded Nave is missing from the mint listing near Soho"
    assert str(gilded[0].get("stock")) == "unknown", (
        f"a five-day-old mint reading at {VENUE_GILDED} reads {gilded[0].get('stock')!r}"
    )
    row = db.stock_row(VENUE_GILDED, FLAVOUR_MINT)
    assert row is not None and str(row.get("reading")) == "in", (
        "the seeded mint reading at The Gilded Nave is not stored as in"
    )
    detail = httpx.get(api(f"/v1/venues/{gilded[0]['id']}"), timeout=30.0)
    assert detail.status_code == 200, f"GET /api/v1/venues/{{id}} returned {detail.status_code}"
    stock = body_of(detail).get("stock", {})
    assert str(stock.get(FLAVOUR_MINT, {}).get("reading")) == "unknown", (
        f"the venue detail reports mint as {stock.get(FLAVOUR_MINT)!r}"
    )
    assert "17:00 to 01:00" in str(body_of(detail).get("hours")), (
        f"The Gilded Nave hours read {body_of(detail).get('hours')!r}"
    )
    salt = [v for v in venues if str(v.get("name")) == VENUE_SALT]
    assert salt and str(salt[0].get("stock")) == "unknown", (
        "Salt & Vesper has no mint reading and does not report mint as unknown"
    )
    marshmallow = [v for v in venue_list(venues_near(SOHO_LAT, SOHO_LNG, 5,
                                                     flavour=FLAVOUR_MARSHMALLOW))
                   if str(v.get("name")) == VENUE_GILDED]
    assert marshmallow and str(marshmallow[0].get("stock")) != "unknown", (
        "a one-day-old marshmallow reading at The Gilded Nave reads unknown"
    )


def test_restricted_region_lists_no_venues():
    response = venues_near(BERGEN_LAT, BERGEN_LNG, 10)
    assert response.status_code == 200, (
        f"GET /api/v1/venues near Bergen returned {response.status_code}: {response.text[:300]}"
    )
    body = response.json()
    assert venue_list(response) == [], f"a restricted region listed venues: {response.text[:300]}"
    region = body.get("region") or {}
    assert str(region.get("code")) == REGION_RESTRICTED, f"the region is {region!r}"
    assert region.get("listingAllowed") is False, f"listingAllowed is {region.get('listingAllowed')!r}"
    record = httpx.get(api(f"/v1/regions/{REGION_RESTRICTED}"), timeout=30.0)
    assert record.status_code == 200, f"GET /api/v1/regions/NO returned {record.status_code}"
    assert str(body_of(record).get("notice")) == RESTRICTED_NOTICE, (
        f"the NO region notice is {body_of(record).get('notice')!r}"
    )


def test_empty_radius_returns_no_venues():
    response = venues_near(LEITH_LAT, LEITH_LNG, RADIUS_MAX)
    assert response.status_code == 200, f"GET /api/v1/venues near Leith returned {response.status_code}"
    assert venue_list(response) == [], f"venues near Leith: {response.text[:300]}"


def test_alert_is_set_once_and_confirmed_by_email(inbox, db):
    email, token = fresh_visitor(inbox, "alert")
    soho = place_by_name(PLACE_SOHO)
    with client(token) as fresh:
        first = set_alert(fresh, soho["id"], 5, FLAVOUR_MINT)
        again = set_alert(fresh, soho["id"], 5, FLAVOUR_MINT)
    assert first.status_code in CREATED, f"POST /api/v1/alerts returned {first.status_code}: {first.text[:300]}"
    assert again.status_code in CREATED, f"repeating the alert returned {again.status_code}"
    assert str(body_of(first).get("id")) == str(body_of(again).get("id")), (
        "setting the same alert twice returned two different alerts"
    )
    rows = [r for r in db.alerts_for_user(user_id_of(db, email.lower())) if str(r.get("state")) == "active"]
    assert len(rows) == 1, f"the account holds {len(rows)} active alerts, expected 1"
    message = wait_for_mail(inbox, email, f"{ALERT_SET_SUBJECT} {PLACE_SOHO}")
    assert message is not None, f"no message titled {ALERT_SET_SUBJECT!r} {PLACE_SOHO!r} reached {email}"
    assert CANCEL_LINK_PREFIX.lower() in message.body.lower(), (
        f"the alert message carries no cancellation line: {message.body[:300]!r}"
    )
    alert_id = str(body_of(first).get("id"))
    with client(token) as fresh:
        listed = fresh.get("/v1/alerts")
        assert listed.status_code == 200, f"GET /api/v1/alerts returned {listed.status_code}"
        assert alert_id in [str(a.get("id")) for a in items(listed.json())], (
            "GET /api/v1/alerts does not list the new alert"
        )
        removed = fresh.delete(f"/v1/alerts/{alert_id}")
    assert removed.status_code in NO_CONTENT, f"deleting the alert returned {removed.status_code}"
    cancelled = [r for r in db.alerts_for_user(user_id_of(db, email.lower()))
                 if str(r.get("id")) == alert_id]
    assert cancelled and str(cancelled[0].get("state")) == "cancelled", (
        f"the deleted alert reads {cancelled}"
    )


def test_alert_cancellation_link_cancels_the_alert(inbox, db):
    email, token = fresh_visitor(inbox, "cancel")
    soho = place_by_name(PLACE_SOHO)
    with client(token) as fresh:
        created = set_alert(fresh, soho["id"], 10, None)
    assert created.status_code in CREATED, f"POST /api/v1/alerts returned {created.status_code}"
    message = wait_for_mail(inbox, email, ALERT_SET_SUBJECT)
    assert message is not None, f"no alert message reached {email}"
    found = re.search(r"/alerts/cancel\?token=([A-Za-z0-9_-]+)", message.body)
    assert found, f"the alert message carries no {ALERT_CANCEL_ROUTE}?token= link: {message.body[:300]!r}"
    opened = get_page(f"{ALERT_CANCEL_ROUTE}?token={found.group(1)}")
    assert opened.status_code == 200, f"opening the cancellation link returned {opened.status_code}"
    assert has_text(opened.text, ALERT_OFF_LINE), f"the cancellation page does not say {ALERT_OFF_LINE!r}"
    reopened = get_page(f"{ALERT_CANCEL_ROUTE}?token={found.group(1)}")
    assert reopened.status_code == 200 and has_text(reopened.text, ALERT_OFF_LINE), (
        "opening the cancellation link a second time does not show the same line"
    )
    alert_id = body_of(created).get("id")
    row = [r for r in db.alerts_for_user(user_id_of(db, email.lower())) if str(r.get("id")) == str(alert_id)]
    assert row and str(row[0].get("state")) == "cancelled", f"the alert row reads {row}"


def test_alert_in_restricted_region_is_refused(inbox, db):
    email, token = fresh_visitor(inbox, "restrict")
    bergen = place_by_name(PLACE_BERGEN)
    with client(token) as fresh:
        response = set_alert(fresh, bergen["id"], 10, None)
    assert response.status_code in CONFLICT, (
        f"an alert in a restricted region returned {response.status_code}: {response.text[:300]}"
    )
    assert reason_of(response) == REASON_RESTRICTED, f"reason was {reason_of(response)!r}"
    assert db.alerts_for_user(user_id_of(db, email.lower())) == [], "a refused alert wrote a row"
    with client(token) as fresh:
        unknown = set_alert(fresh, "no-such-place", 10, None)
    assert unknown.status_code in REFUSED and reason_of(unknown) == "invalid_place", (
        f"an alert on an unknown place answered {unknown.status_code} {reason_of(unknown)!r}"
    )


def test_host_stock_update_fires_matching_alert_email(inbox, db, host2_client):
    email, token = fresh_visitor(inbox, "landed")
    shoreditch = place_by_name(PLACE_SHOREDITCH)
    with client(token) as fresh:
        created = set_alert(fresh, shoreditch["id"], 2, FLAVOUR_MARSHMALLOW)
    assert created.status_code in CREATED, f"POST /api/v1/alerts returned {created.status_code}"
    far_email, far_token = fresh_visitor(inbox, "farwatch")
    with client(far_token) as far:
        assert set_alert(far, place_by_name(PLACE_LEITH)["id"], 2, None).status_code in CREATED, (
            "an any-flavour alert on Leith was not created"
        )
    salt = db.venue_row(VENUE_SALT)
    assert salt is not None, f"venue has no row named {VENUE_SALT!r}"
    updated = host2_client.put(f"/v1/venues/{salt['id']}/stock",
                               json={"flavour": FLAVOUR_MARSHMALLOW, "reading": "in"})
    assert updated.status_code in CREATED, (
        f"the host's stock update returned {updated.status_code}: {updated.text[:300]}"
    )
    assert str(db.stock_row(VENUE_SALT, FLAVOUR_MARSHMALLOW).get("reading")) == "in", (
        "the stock update did not persist"
    )
    assert str(body_of(updated).get("reading")) == "in", f"the update answered {updated.text[:200]}"
    bad = host2_client.put(f"/v1/venues/{salt['id']}/stock",
                           json={"flavour": FLAVOUR_ORANGE, "reading": "plenty"})
    assert bad.status_code in REFUSED and reason_of(bad) == "invalid_reading", (
        f"an unknown reading answered {bad.status_code} {bad.text[:200]}"
    )
    message = wait_for_mail(inbox, email, f"{ALERT_FIRED_SUBJECT} {VENUE_SALT}")
    assert message is not None, (
        f"no message titled {ALERT_FIRED_SUBJECT!r} {VENUE_SALT!r} reached {email}"
    )
    fired = poll_until(lambda: [r for r in db.alerts_for_user(user_id_of(db, email.lower()))
                                if str(r.get("state")) == "fired"])
    assert fired, "the matching alert did not move to fired"
    gone_email, gone_token = fresh_visitor(inbox, "goneflav")
    with client(gone_token) as gone:
        dropped = set_alert(gone, shoreditch["id"], 2, None)
        assert gone.delete(f"/v1/alerts/{body_of(dropped).get('id')}").status_code in NO_CONTENT, (
            "cancelling an alert did not answer 204"
        )
    any_email, any_token = fresh_visitor(inbox, "anyflav")
    with client(any_token) as anyone:
        assert set_alert(anyone, shoreditch["id"], 2, None).status_code in CREATED, (
            "an any-flavour alert on Shoreditch was not created"
        )
    again = host2_client.put(f"/v1/venues/{salt['id']}/stock",
                             json={"flavour": FLAVOUR_MARSHMALLOW, "reading": "in"})
    assert again.status_code in CREATED, f"the second stock update returned {again.status_code}"
    assert wait_for_mail(inbox, any_email, f"{ALERT_FIRED_SUBJECT} {VENUE_SALT}") is not None, (
        "an unchanged in reading did not fire the matching any-flavour alert"
    )
    assert inbox.find(to=gone_email, subject_contains=ALERT_FIRED_SUBJECT) is None, (
        "a cancelled alert still sent a landing message"
    )
    assert inbox.find(to=far_email, subject_contains=ALERT_FIRED_SUBJECT) is None, (
        "an alert on a place outside the radius fired"
    )
    settle()
    settle()
    sent = inbox.count(to=email)
    assert sent == 3, (
        f"{email} received {sent} messages; the sign-in link, the alert confirmation and one "
        f"landing message were expected, so a fired alert sent again"
    )


def test_visitor_cannot_change_a_stock_reading(db, visitor_client):
    gilded = db.venue_row(VENUE_GILDED)
    before = db.stock_row(VENUE_GILDED, FLAVOUR_ORANGE)
    response = visitor_client.put(f"/v1/venues/{gilded['id']}/stock",
                                  json={"flavour": FLAVOUR_ORANGE, "reading": "out"})
    assert response.status_code in DENIED, (
        f"a visitor changing a stock reading returned {response.status_code}: {response.text[:300]}"
    )
    assert reason_of(response) == "forbidden", f"a visitor changing a stock reading gave reason {reason_of(response)!r}"
    after = db.stock_row(VENUE_GILDED, FLAVOUR_ORANGE)
    assert after.get("reading") == before.get("reading") and after.get("updated_at") == before.get("updated_at"), (
        "a denied stock update changed the stored reading"
    )


def test_host_cannot_change_another_venues_reading(db, host_client):
    salt = db.venue_row(VENUE_SALT)
    before = db.stock_row(VENUE_SALT, FLAVOUR_ORANGE)
    response = host_client.put(f"/v1/venues/{salt['id']}/stock",
                               json={"flavour": FLAVOUR_ORANGE, "reading": "out"})
    assert response.status_code in DENIED, (
        f"{HOST_EMAIL} changing {VENUE_SALT} returned {response.status_code}: {response.text[:300]}"
    )
    after = db.stock_row(VENUE_SALT, FLAVOUR_ORANGE)
    assert after.get("reading") == before.get("reading") and after.get("updated_at") == before.get("updated_at"), (
        "another venue's host changed a reading"
    )


def test_host_venue_page_returns_own_venue(host2_client):
    response = host2_client.get("/v1/host/venue")
    assert response.status_code == 200, f"GET /api/v1/host/venue returned {response.status_code}"
    assert str(body_of(response).get("name")) == VENUE_SALT, (
        f"{HOST2_EMAIL} was given venue {body_of(response).get('name')!r}"
    )
    venue = body_of(response)
    assert "stock" in venue and isinstance(venue.get("sessions"), list), f"the host venue lacks stock or sessions: {response.text[:300]}"
    assert has_text(response.text, SESSION_LATE_POUR), f"the host venue sessions omit {SESSION_LATE_POUR!r}"


def test_visitor_cannot_read_the_host_venue(visitor_client):
    response = visitor_client.get("/v1/host/venue")
    assert response.status_code in DENIED, (
        f"a visitor reading the host venue returned {response.status_code}: {response.text[:300]}"
    )


def test_tastings_list_carries_zone_and_minor_unit_price():
    night = session_by_title(SESSION_NIGHT)
    assert int(night.get("price")) == NIGHT_PRICE, f"{SESSION_NIGHT} price is {night.get('price')!r}"
    assert str(night.get("currency")).lower() == CURRENCY, f"currency is {night.get('currency')!r}"
    assert str(night.get("timezone")) == ZONE_LONDON, f"timezone is {night.get('timezone')!r}"
    assert int(night.get("remaining")) <= int(night.get("capacity")), "remaining exceeds capacity"
    paris = session_by_title(SESSION_PARIS)
    assert str(paris.get("timezone")) == ZONE_PARIS, f"{SESSION_PARIS} timezone is {paris.get('timezone')!r}"
    assert re.search(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?Z$", str(night.get("startsAt"))), (
        f"startsAt {night.get('startsAt')!r} is not an ISO 8601 UTC instant ending in Z"
    )
    assert str(night.get("state")) == "scheduled", f"{SESSION_NIGHT} is in state {night.get('state')!r}"


def test_seat_hold_and_booking_send_one_confirmation_email(inbox, db):
    email, token = fresh_visitor(inbox, "book")
    night = session_by_title(SESSION_NIGHT)
    with client(token) as fresh:
        held = hold_seats(fresh, night["id"], 2)
        assert held.status_code in CREATED, f"holding seats returned {held.status_code}: {held.text[:300]}"
        assert 0.1 < hours_until(body_of(held).get("expiresAt")) * 60 <= 15.5, (
            "the seat hold does not expire about fifteen minutes from now"
        )
        booked = book(fresh, hold_id_of(held), email)
    assert booked.status_code in CREATED, f"POST /api/v1/bookings returned {booked.status_code}: {booked.text[:300]}"
    assert str(body_of(booked).get("state")) == "booked", f"booking state is {body_of(booked).get('state')!r}"
    message = wait_for_mail(inbox, email, f"{BOOKED_SUBJECT} {SESSION_NIGHT}")
    assert message is not None, f"no message titled {BOOKED_SUBJECT!r} {SESSION_NIGHT!r} reached {email}"
    assert has_text(message.body, VENUE_GILDED), "the booking message body does not name the venue"
    with client(token) as fresh:
        listed = fresh.get("/v1/bookings")
    assert listed.status_code == 200 and booking_id_of(booked) in [str(b.get("id")) for b in items(listed.json())], (
        "GET /api/v1/bookings does not list the new booking"
    )
    assert inbox.count(to=email) == 2, (
        f"{email} received {inbox.count(to=email)} messages; the sign-in link and one confirmation were expected"
    )
    rows = db.bookings_for_user(user_id_of(db, email.lower()))
    assert len(rows) == 1 and str(rows[0].get("state")) == "booked", f"booking rows: {rows}"
    with client(token) as fresh:
        cancelled = fresh.delete(f"/v1/bookings/{booking_id_of(booked)}")
    assert cancelled.status_code in NO_CONTENT, (
        f"cancelling ten days ahead returned {cancelled.status_code}: {cancelled.text[:300]}"
    )
    settle()
    assert inbox.count(to=email) == 2, "a visitor cancelling a booking was sent a message"


def test_party_size_outside_bounds_is_refused(inbox):
    email, token = fresh_visitor(inbox, "party")
    night = session_by_title(SESSION_NIGHT)
    with client(token) as fresh:
        for size in (PARTY_MIN - 1, PARTY_MAX + 1):
            response = hold_seats(fresh, night["id"], size)
            assert response.status_code in REFUSED, f"party size {size} returned {response.status_code}"
            assert reason_of(response) == REASON_INVALID_PARTY, f"reason was {reason_of(response)!r}"


def test_hold_larger_than_remaining_is_refused(inbox, db):
    email, token = fresh_visitor(inbox, "soldout")
    sold_out = session_by_title(SESSION_SOLD_OUT)
    assert int(sold_out.get("remaining")) == 0, f"{SESSION_SOLD_OUT} lists {sold_out.get('remaining')} remaining"
    with client(token) as fresh:
        response = hold_seats(fresh, sold_out["id"], 1)
    assert response.status_code in CONFLICT, f"holding a full session returned {response.status_code}"
    assert reason_of(response) == REASON_INSUFFICIENT, f"reason was {reason_of(response)!r}"
    assert int(body_of(response).get("remaining")) == 0, f"the refusal says remaining {response.text[:200]}"
    assert db.active_holds_for_session(sold_out["id"]) == [], "a refused hold left an active hold"
    early = session_by_title(SESSION_EARLY)
    with client(token) as fresh:
        started = hold_seats(fresh, early["id"], 1)
    assert started.status_code in REFUSED and reason_of(started) == "session_started", (
        f"a hold on a started session answered {started.status_code} {reason_of(started)!r}"
    )


def test_concurrent_holds_never_exceed_capacity(inbox, db):
    first_email, first_token = fresh_visitor(inbox, "seata")
    second_email, second_token = fresh_visitor(inbox, "seatb")
    chapel = session_by_title(SESSION_CHAPEL)
    assert int(chapel.get("capacity")) == CHAPEL_CAPACITY, f"{SESSION_CHAPEL} capacity is {chapel.get('capacity')}"

    def attempt(token):
        with client(token) as c:
            return hold_seats(c, chapel["id"], CHAPEL_CAPACITY)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(attempt, (first_token, second_token)))
    statuses = sorted(r.status_code for r in results)
    granted = [r for r in results if r.status_code in CREATED]
    assert len(granted) <= 1, f"two holds for the whole capacity both succeeded: {statuses}"
    held = sum(int(h.get("party_size")) for h in db.active_holds_for_session(chapel["id"]))
    booked = sum(int(b.get("party_size")) for b in db.bookings_for_session(chapel["id"])
                 if str(b.get("state")) == "booked")
    assert held + booked <= CHAPEL_CAPACITY, (
        f"{SESSION_CHAPEL} holds {held} and books {booked} seats against a capacity of {CHAPEL_CAPACITY}"
    )
    after = session_by_title(SESSION_CHAPEL)
    assert int(after.get("remaining")) >= 0, f"remaining went to {after.get('remaining')}"


def test_hold_at_a_second_session_is_refused(inbox):
    email, token = fresh_visitor(inbox, "elsewhere")
    night = session_by_title(SESSION_NIGHT)
    paris = session_by_title(SESSION_PARIS)
    with client(token) as fresh:
        first = hold_seats(fresh, night["id"], 1)
        assert first.status_code in CREATED, f"the first hold returned {first.status_code}"
        second = hold_seats(fresh, paris["id"], 1)
        assert second.status_code in REFUSED, f"a second concurrent hold returned {second.status_code}"
        assert reason_of(second) == REASON_HOLD_ELSEWHERE, f"reason was {reason_of(second)!r}"
        released = fresh.delete(f"/v1/tastings/holds/{hold_id_of(first)}")
        assert released.status_code in NO_CONTENT, f"giving seats back returned {released.status_code}"
        third = hold_seats(fresh, paris["id"], 1)
    assert third.status_code in CREATED, f"a hold after giving seats back returned {third.status_code}"


def test_repeated_booking_with_same_key_creates_one_booking(inbox, db):
    email, token = fresh_visitor(inbox, "rebook")
    paris = session_by_title(SESSION_PARIS)
    key = f"book-{probe_suffix()}"
    with client(token) as fresh:
        hold_id = hold_id_of(hold_seats(fresh, paris["id"], 1))
        first = book(fresh, hold_id, email, key=key)
        again = book(fresh, hold_id, email, key=key)
    assert first.status_code in CREATED, f"the booking returned {first.status_code}: {first.text[:300]}"
    assert again.status_code in CREATED, f"the retried booking returned {again.status_code}"
    assert booking_id_of(first) == booking_id_of(again), "the retry produced a second booking"
    rows = db.bookings_for_user(user_id_of(db, email.lower()))
    assert len(rows) == 1, f"a retried booking produced {len(rows)} rows"


def test_cancel_inside_48_hours_is_refused_as_late(inbox, db):
    email, token = fresh_visitor(inbox, "late")
    late = session_by_title(SESSION_LATE_POUR)
    assert 0 < hours_until(late.get("startsAt")) < 48, (
        f"{SESSION_LATE_POUR} is not inside the next forty-eight hours"
    )
    with client(token) as fresh:
        booking_id = booking_id_of(book(fresh, hold_id_of(hold_seats(fresh, late["id"], 1)), email))
        response = fresh.delete(f"/v1/bookings/{booking_id}")
    assert response.status_code in CONFLICT, (
        f"cancelling inside forty-eight hours returned {response.status_code}: {response.text[:300]}"
    )
    assert reason_of(response) == REASON_LATE, f"reason was {reason_of(response)!r}"
    rows = db.bookings_for_user(user_id_of(db, email.lower()))
    assert rows and str(rows[0].get("state")) == "booked", f"the refused cancel changed the booking: {rows}"


def test_second_reschedule_is_refused(inbox, db):
    email, token = fresh_visitor(inbox, "move")
    late = session_by_title(SESSION_LATE_POUR)
    paris = session_by_title(SESSION_PARIS)
    night = session_by_title(SESSION_NIGHT)
    with client(token) as fresh:
        booking_id = booking_id_of(book(fresh, hold_id_of(hold_seats(fresh, late["id"], 1)), email))
        full = session_by_title(SESSION_SOLD_OUT)
        no_room = fresh.post(f"/v1/bookings/{booking_id}/reschedule", json={"sessionId": full["id"]})
        assert no_room.status_code in REFUSED and reason_of(no_room) == REASON_INSUFFICIENT, (
            f"moving to a full session answered {no_room.status_code} {no_room.text[:200]}"
        )
        early = session_by_title(SESSION_EARLY)
        too_late = fresh.post(f"/v1/bookings/{booking_id}/reschedule", json={"sessionId": early["id"]})
        assert too_late.status_code in REFUSED and reason_of(too_late) == "session_started", (
            f"moving onto a started session answered {too_late.status_code} {too_late.text[:200]}"
        )
        moved = fresh.post(f"/v1/bookings/{booking_id}/reschedule", json={"sessionId": paris["id"]})
        assert moved.status_code in CREATED, f"the first move returned {moved.status_code}: {moved.text[:300]}"
        assert str(body_of(moved).get("sessionId")) == str(paris["id"]), "the moved booking names another session"
        again = fresh.post(f"/v1/bookings/{booking_id}/reschedule", json={"sessionId": night["id"]})
    assert again.status_code in REFUSED, f"a second move returned {again.status_code}"
    assert reason_of(again) == REASON_ALREADY_RESCHEDULED, f"reason was {reason_of(again)!r}"
    rows = db.bookings_for_user(user_id_of(db, email.lower()))
    assert rows and str(rows[0].get("session_id")) == str(paris["id"]), "the refused move changed the booking"
    settle()
    assert inbox.count(to=email) == 2, "rescheduling a booking sent a message beyond the one confirmation"


def test_full_session_waitlist_returns_a_position(inbox):
    email, token = fresh_visitor(inbox, "line")
    sold_out = session_by_title(SESSION_SOLD_OUT)
    with client(token) as fresh:
        response = fresh.post(f"/v1/tastings/{sold_out['id']}/waitlist", json={"partySize": 2})
    assert response.status_code in CREATED, f"joining the waitlist returned {response.status_code}: {response.text[:300]}"
    assert int(body_of(response).get("position")) >= 1, f"no position in {response.text[:200]}"
    settle()
    assert inbox.count(to=email) == 1, "joining a tasting waitlist sent a message"
    with client(token) as fresh:
        rejoined = fresh.post(f"/v1/tastings/{sold_out['id']}/waitlist", json={"partySize": 2})
    assert body_of(rejoined).get("position") == body_of(response).get("position"), (
        f"joining the same list twice answered {rejoined.text[:200]}"
    )
    paris = session_by_title(SESSION_PARIS)
    with client(token) as fresh:
        roomy = fresh.post(f"/v1/tastings/{paris['id']}/waitlist", json={"partySize": 1})
    assert roomy.status_code == 409 and reason_of(roomy) == "not_full", (
        f"joining the list of a session with room returned {roomy.status_code} {reason_of(roomy)!r}"
    )


def test_host_cancelling_a_session_emails_every_booking(inbox, db, host2_client):
    email, token = fresh_visitor(inbox, "hostcancel")
    last_call = session_by_title(SESSION_LAST_CALL)
    with client(token) as fresh:
        booked = book(fresh, hold_id_of(hold_seats(fresh, last_call["id"], 1)), email)
    assert booked.status_code in CREATED, f"booking {SESSION_LAST_CALL} returned {booked.status_code}"
    response = host2_client.post(f"/v1/tastings/{last_call['id']}/cancel")
    assert response.status_code in CREATED, f"the host's cancel returned {response.status_code}: {response.text[:300]}"
    assert str(db.session_row(SESSION_LAST_CALL).get("state")) == "cancelled", "the session is not cancelled"
    rows = db.bookings_for_user(user_id_of(db, email.lower()))
    assert rows and str(rows[0].get("state")) == "session_cancelled", f"booking rows: {rows}"
    early = session_by_title(SESSION_EARLY)
    started = host2_client.post(f"/v1/tastings/{early['id']}/cancel")
    assert started.status_code in REFUSED and reason_of(started) == "session_started", (
        f"cancelling a started session answered {started.status_code} {reason_of(started)!r}"
    )
    assert str(db.session_row(SESSION_EARLY).get("state")) == "scheduled", "a refused cancel changed the session"
    message = wait_for_mail(inbox, email, f"{CANCELLED_SUBJECT} {SESSION_LAST_CALL}")
    assert message is not None, f"no message titled {CANCELLED_SUBJECT!r} {SESSION_LAST_CALL!r} reached {email}"
    late_email, late_token = fresh_visitor(inbox, "aftercancel")
    with client(late_token) as late:
        refused = hold_seats(late, last_call["id"], 1)
    assert refused.status_code in REFUSED, f"a hold on a cancelled session returned {refused.status_code}"
    assert reason_of(refused) == "closed", f"a hold on a cancelled session gave reason {reason_of(refused)!r}"
    paris = session_by_title(SESSION_PARIS)
    with client(late_token) as late:
        moving = book(late, hold_id_of(hold_seats(late, paris["id"], 1)), late_email)
        assert moving.status_code in CREATED, f"booking {SESSION_PARIS} returned {moving.status_code}"
        onto_cancelled = late.post(f"/v1/bookings/{booking_id_of(moving)}/reschedule",
                                   json={"sessionId": last_call["id"]})
    assert onto_cancelled.status_code == 409 and reason_of(onto_cancelled) == "closed", (
        f"moving a booking onto a cancelled session answered {onto_cancelled.status_code} {reason_of(onto_cancelled)!r}"
    )


def test_visitor_cannot_cancel_a_session(db, visitor_client):
    night = db.session_row(SESSION_NIGHT)
    response = visitor_client.post(f"/v1/tastings/{night['id']}/cancel")
    assert response.status_code in DENIED, f"a visitor cancelling a session returned {response.status_code}"
    assert str(db.session_row(SESSION_NIGHT).get("state")) == "scheduled", "a visitor cancelled a session"


def test_host_cannot_cancel_another_venues_session(db, host_client):
    late = db.session_row(SESSION_LATE_POUR)
    response = host_client.post(f"/v1/tastings/{late['id']}/cancel")
    assert response.status_code in DENIED, (
        f"{HOST_EMAIL} cancelling {SESSION_LATE_POUR} returned {response.status_code}"
    )
    assert str(db.session_row(SESSION_LATE_POUR).get("state")) == "scheduled", (
        "another venue's host cancelled a session"
    )
    visitor_only = host_client.post("/v1/cellar/holds", json={"releaseId": RELEASE_MAIN, "flavour": FLAVOUR_MINT})
    assert visitor_only.status_code == 403 and reason_of(visitor_only) == "forbidden", (
        f"{HOST_EMAIL} placing a hold answered {visitor_only.status_code} {reason_of(visitor_only)!r}"
    )


def test_ingredients_are_closed_sets_without_withdrawn_items():
    response = httpx.get(api("/v1/ingredients"), timeout=30.0)
    assert response.status_code == 200, f"GET /api/v1/ingredients returned {response.status_code}"
    body = response.json()
    for key, expected in (("mixers", MIXER_IDS), ("ices", ICE_IDS), ("garnishes", GARNISH_IDS)):
        got = {str(entry.get("id")) for entry in body.get(key, [])}
        assert got == set(expected), f"{key} are {sorted(got)}, expected {sorted(expected)}"
    assert WITHDRAWN_GARNISH not in response.text, "the withdrawn garnish is still offered"


def test_ritual_save_returns_a_slug_following_the_scheme(inbox, db):
    email, token = fresh_visitor(inbox, "ritual")
    with client(token) as fresh:
        response = fresh.post("/v1/rituals", json=ritual_body("Velvet Hour"))
    assert response.status_code == 201, f"POST /api/v1/rituals returned {response.status_code}: {response.text[:300]}"
    slug = slug_of(response)
    assert re.match(SLUG_PATTERN, slug), f"the slug {slug!r} does not follow the scheme"
    row = db.ritual_row(slug)
    assert row is not None and str(row.get("name")) == "Velvet Hour", f"ritual row: {row}"
    public = httpx.get(api(f"/v1/rituals/{slug}"), timeout=30.0)
    assert public.status_code == 200, f"GET /api/v1/rituals/{slug} returned {public.status_code}"
    shown = body_of(public)
    assert shown.get("mixers") == ["cold-brew", "oat-milk"], f"mixers are {shown.get('mixers')}"
    assert (str(shown.get("name")), str(shown.get("flavour")), str(shown.get("ice")), str(shown.get("garnish"))) == (
        "Velvet Hour", FLAVOUR_MARSHMALLOW, "crushed", "cocoa-dust"), f"the public ritual reads {shown}"


def test_same_ritual_saved_twice_returns_one_slug(inbox, db):
    email, token = fresh_visitor(inbox, "same")
    with client(token) as fresh:
        first = fresh.post("/v1/rituals", json=ritual_body("Quiet Hours"))
        again = fresh.post("/v1/rituals", json=ritual_body("Quiet Hours"))
    assert first.status_code in CREATED and again.status_code in CREATED, (
        f"the two saves returned {first.status_code} and {again.status_code}"
    )
    assert slug_of(first) == slug_of(again), "saving the same ritual twice issued two slugs"
    assert len(db.rituals_for_user(user_id_of(db, email.lower()))) == 1, "a repeat save wrote a second row"


def test_refused_ritual_name_writes_nothing(inbox, db):
    email, token = fresh_visitor(inbox, "refuse")
    with client(token) as fresh:
        for name in ("Big Casino Night", "Visit www.example.com"):
            response = fresh.post("/v1/rituals", json=ritual_body(name))
            assert response.status_code in REFUSED, f"the name {name!r} returned {response.status_code}"
            assert reason_of(response) == REASON_NAME_REFUSED, f"reason was {reason_of(response)!r}"
        short = fresh.post("/v1/rituals", json=ritual_body("Ab"))
        assert short.status_code in REFUSED, f"a two-character name returned {short.status_code}"
        assert reason_of(short) == REASON_INVALID_NAME, f"reason was {reason_of(short)!r}"
    assert db.rituals_for_user(user_id_of(db, email.lower())) == [], "a refused name wrote a ritual"


def test_ritual_with_withdrawn_or_unknown_ingredient_is_refused(inbox, db):
    email, token = fresh_visitor(inbox, "ingr")
    with client(token) as fresh:
        withdrawn = fresh.post("/v1/rituals", json=ritual_body("Gilded Edge", garnish=WITHDRAWN_GARNISH))
        too_many = fresh.post("/v1/rituals", json=ritual_body(
            "Crowded Glass", mixers=("cold-brew", "tonic", "oat-milk", "soda", "espresso")))
    assert withdrawn.status_code in REFUSED, f"a withdrawn garnish returned {withdrawn.status_code}"
    assert reason_of(withdrawn) == REASON_INVALID_INGREDIENT, f"reason was {reason_of(withdrawn)!r}"
    assert too_many.status_code in REFUSED, f"five mixers returned {too_many.status_code}"
    assert reason_of(too_many) == REASON_TOO_MANY_MIXERS, f"reason was {reason_of(too_many)!r}"
    assert db.rituals_for_user(user_id_of(db, email.lower())) == [], "a refused ritual wrote a row"


def test_sixth_ritual_save_in_an_hour_is_rate_limited(inbox, db):
    email, token = fresh_visitor(inbox, "limit")
    with client(token) as fresh:
        for n in range(RITUAL_SAVES_PER_HOUR):
            response = fresh.post("/v1/rituals", json=ritual_body(f"Night Number {n + 1}"))
            assert response.status_code in CREATED, (
                f"save {n + 1} of {RITUAL_SAVES_PER_HOUR} returned {response.status_code}: {response.text[:300]}"
            )
            if n == 1:
                repeat = fresh.post("/v1/rituals", json=ritual_body("Night Number 1"))
                assert repeat.status_code in CREATED, (
                    f"re-saving an existing ritual returned {repeat.status_code}, so it was counted"
                )
        sixth = fresh.post("/v1/rituals", json=ritual_body("Night Number Six"))
    assert sixth.status_code in RATE_LIMITED_STATUS, f"the sixth save returned {sixth.status_code}"
    assert reason_of(sixth) == REASON_RATE_LIMITED, f"reason was {reason_of(sixth)!r}"
    assert int(body_of(sixth).get("cooldownSeconds")) > 0, f"no cooldown in {sixth.text[:200]}"
    assert len(db.rituals_for_user(user_id_of(db, email.lower()))) == RITUAL_SAVES_PER_HOUR, (
        "the refused sixth save wrote a row"
    )


def test_public_ritual_read_carries_no_owner_identity(db):
    response = httpx.get(api(f"/v1/rituals/{SEEDED_RITUAL_SLUG}"), timeout=30.0)
    assert response.status_code == 200, f"GET /api/v1/rituals/{SEEDED_RITUAL_SLUG} returned {response.status_code}"
    body = body_of(response)
    assert str(body.get("name")) == SEEDED_RITUAL_NAME, f"the seeded ritual is named {body.get('name')!r}"
    assert str(body.get("garnish")) == WITHDRAWN_GARNISH, "the seeded ritual lost its withdrawn garnish"
    text = response.text.lower()
    owner = db.user_row(VISITOR2_EMAIL)
    for forbidden in ("userid", "ownerid", "user_id", "owner_id", "email", VISITOR2_EMAIL):
        assert forbidden.lower() not in text, f"the public ritual read carries {forbidden!r}"
    assert str(owner.get("display_name")).lower() not in text, "the public ritual read carries the owner's name"


def test_other_visitor_cannot_edit_a_ritual(db, visitor_client, visitor2_client, inbox):
    before = db.ritual_row(SEEDED_RITUAL_SLUG)
    response = visitor_client.patch(f"/v1/rituals/{SEEDED_RITUAL_SLUG}", json={
        "flavour": FLAVOUR_ORANGE, "mixers": ["tonic"], "ice": "cubed",
        "garnish": "orange-twist", "name": "Taken Over"})
    deleted = visitor_client.delete(f"/v1/rituals/{SEEDED_RITUAL_SLUG}")
    for label, result in (("edit", response), ("delete", deleted)):
        assert result.status_code in DENIED_OR_MISSING, f"another visitor's {label} returned {result.status_code}"
    after = db.ritual_row(SEEDED_RITUAL_SLUG)
    assert after.get("name") == before.get("name") and after.get("deleted_at") == before.get("deleted_at"), (
        "another visitor changed the seeded ritual"
    )
    assert response.status_code == 403 and reason_of(response) == "forbidden", (
        f"another visitor's edit answered {response.status_code} {reason_of(response)!r}"
    )
    late_edit = visitor2_client.patch(f"/v1/rituals/{SEEDED_RITUAL_SLUG}", json=ritual_body("Too Late Now"))
    assert late_edit.status_code in REFUSED and reason_of(late_edit) == "edit_window_closed", (
        f"the owner's edit after twenty-four hours answered {late_edit.status_code} {reason_of(late_edit)!r}"
    )
    assert db.ritual_row(SEEDED_RITUAL_SLUG).get("name") == before.get("name"), "a refused late edit changed the ritual"
    email, token = fresh_visitor(inbox, "editor")
    with client(token) as owner:
        slug = slug_of(owner.post("/v1/rituals", json=ritual_body("Blue Lantern")))
        edited = owner.patch(f"/v1/rituals/{slug}", json=ritual_body("Blue Lantern Two"))
    assert edited.status_code == 200, f"the owner's edit returned {edited.status_code}: {edited.text[:300]}"
    assert str(db.ritual_row(slug).get("name")) == "Blue Lantern Two", "the owner's edit was not stored"


def test_deleted_ritual_link_offers_the_builder(inbox):
    email, token = fresh_visitor(inbox, "gone")
    with client(token) as fresh:
        slug = slug_of(fresh.post("/v1/rituals", json=ritual_body("Last Orders")))
        removed = fresh.delete(f"/v1/rituals/{slug}")
    assert removed.status_code in NO_CONTENT, f"deleting the ritual returned {removed.status_code}"
    public = httpx.get(api(f"/v1/rituals/{slug}"), timeout=30.0)
    assert public.status_code == 404, f"a deleted ritual answered {public.status_code}"
    assert reason_of(public) == "not_found", f"a deleted ritual gave reason {reason_of(public)!r}"
    opened = get_page(f"/ritual/{slug}")
    assert opened.status_code in (200, 404), f"the deleted ritual page answered {opened.status_code}"
    assert has_text(opened.text, RITUAL_GONE_LINE), f"the deleted ritual page does not say {RITUAL_GONE_LINE!r}"


def test_shared_ritual_page_renders_the_recipe_as_text():
    response = get_page(f"/ritual/{SEEDED_RITUAL_SLUG}")
    assert response.status_code == 200, f"GET /ritual/{SEEDED_RITUAL_SLUG} returned {response.status_code}"
    for needle in (SEEDED_RITUAL_NAME, RITUAL_SHARED_LINE, "Gold leaf", "Espresso", "Oat milk",
                   "MINT CHOCOLATE & CREAM"):
        assert has_text(response.text, needle), f"the shared ritual page HTML does not contain {needle!r}"


def test_terms_page_is_reachable_and_linked():
    terms = get_page(TERMS_ROUTE)
    assert terms.status_code == 200, f"GET {TERMS_ROUTE} returned {terms.status_code}"
    for route in ("/", SIGN_IN_ROUTE):
        html = get_page(route).text
        assert f'href="{TERMS_ROUTE}"' in html or f"href='{TERMS_ROUTE}'" in html, (
            f"{route} carries no link to {TERMS_ROUTE}"
        )


def test_cookie_choice_survives_a_reload():
    with httpx.Client(timeout=30.0, follow_redirects=True) as browser:
        browser.get(api("/health"))
        recorded = browser.post(api("/v1/cookie-choice"), json={"nonEssentialAccepted": False})
        assert recorded.status_code in CREATED, (
            f"recording the cookie choice returned {recorded.status_code}: {recorded.text[:300]}"
        )
        again = browser.get(api("/v1/cookie-choice"))
    assert again.status_code == 200, f"reading the cookie choice back returned {again.status_code}"
    assert body_of(again).get("nonEssentialAccepted") is False, (
        f"the recorded cookie choice did not survive a reload: {again.text[:300]}"
    )
    malformed = httpx.post(api("/v1/cookie-choice"), json={"nonEssentialAccepted": "maybe"}, timeout=30.0)
    assert malformed.status_code in REFUSED and reason_of(malformed) == "invalid_request", (
        f"a malformed cookie choice answered {malformed.status_code} {reason_of(malformed)!r}"
    )


def test_favicon_is_served_and_declared():
    icon = get_page(FAVICON_ROUTE)
    assert icon.status_code == 200 and icon.content, f"GET {FAVICON_ROUTE} returned {icon.status_code}"
    html = get_page("/").text.lower()
    assert 'rel="icon"' in html or "rel='icon'" in html or 'rel="shortcut icon"' in html, (
        "the document head of / declares no favicon"
    )


def test_sitemap_lists_public_routes_and_robots_points_to_it():
    sitemap = get_page(SITEMAP_ROUTE)
    assert sitemap.status_code == 200, f"GET {SITEMAP_ROUTE} returned {sitemap.status_code}"
    for route in PUBLIC_ROUTES:
        assert f"{route}<" in sitemap.text or f"{route}\"" in sitemap.text, (
            f"the sitemap does not list {route}"
        )
    assert re.search(r"<loc>https?://[^/<]+/?</loc>", sitemap.text), "the sitemap does not list the root route /"
    robots = get_page(ROBOTS_ROUTE)
    assert robots.status_code == 200, f"GET {ROBOTS_ROUTE} returned {robots.status_code}"
    assert "sitemap:" in robots.text.lower(), "robots.txt does not point at the sitemap"


def test_addition_pages_declare_a_responsive_viewport():
    for route in ADDITION_ROUTES:
        response = get_page(route)
        assert response.status_code in (200, 401, 403), f"GET {route} returned {response.status_code}"
        html = response.text.lower()
        assert 'name="viewport"' in html and "width=device-width" in html, (
            f"{route} declares no responsive viewport, so it cannot hold at a narrow viewport"
        )
    titles = set()
    for route in PUBLIC_ROUTES:
        html = get_page(route).text
        found = re.search(r"<title>([^<]+)</title>", html)
        assert found and 'name="description"' in html, f"{route} lacks its own title or description"
        titles.add(found.group(1).strip())
    assert len(titles) == len(PUBLIC_ROUTES), f"public routes share titles: {sorted(titles)}"


def test_social_preview_image_is_generated():
    response = get_page(SOCIAL_IMAGE_ROUTE)
    assert response.status_code == 200, f"GET {SOCIAL_IMAGE_ROUTE} returned {response.status_code}"
    assert response.content[:8] == b"\x89PNG\r\n\x1a\n", f"{SOCIAL_IMAGE_ROUTE} is not a PNG"
    html = get_page("/").text
    assert "og:image" in html and "og:title" in html, "the document head of / declares no social preview"
    ritual_image = get_page(f"/og/ritual/{SEEDED_RITUAL_SLUG}.png")
    assert ritual_image.status_code == 200 and ritual_image.content[:4] == b"\x89PNG", (
        f"the ritual preview image answered {ritual_image.status_code}"
    )


def test_seeding_is_idempotent(db):
    assert db.count_releases() == SEEDED_RELEASES, (
        f"release holds {db.count_releases()} rows, expected {SEEDED_RELEASES}"
    )
    assert db.count_places() == SEEDED_PLACES, f"place holds {db.count_places()} rows"
    assert db.count_flavours() == 3, f"flavour holds {db.count_flavours()} rows, expected 3"
    assert db.count_chapters() == 18, f"chapter holds {db.count_chapters()} rows, expected 18"
    assert db.count_venues() == 5, f"venue holds {db.count_venues()} rows, expected 5"
    assert db.count_sessions() == 7, f"tasting_session holds {db.count_sessions()} rows, expected 7"
    for email in (VISITOR_EMAIL, VISITOR2_EMAIL, HOST_EMAIL, HOST2_EMAIL):
        assert db.count_users(email) == 1, f"app_user holds {db.count_users(email)} rows for {email}"


def test_seeded_rows_survive_a_re_read(db, visitor2_client):
    owner = user_id_of(db, VISITOR2_EMAIL)
    confirmed = [r for r in db.allocations_for_user(owner)
                 if str(r.get("release_id")) == RELEASE_MAIN and str(r.get("state")) == "confirmed"]
    assert confirmed, f"{VISITOR2_EMAIL} has no confirmed allocation of {RELEASE_MAIN}"
    shelf = [e for e in cellar_items(visitor2_client)
             if str(e.get("releaseId")) == RELEASE_MAIN and str(e.get("state")) == "confirmed"]
    assert shelf, f"GET /api/v1/cellar for {VISITOR2_EMAIL} omits the confirmed bottle"
    expired = [e for e in cellar_items(visitor2_client)
               if str(e.get("releaseId")) == RELEASE_CLOSED and str(e.get("state")) == "expired"]
    assert expired, f"GET /api/v1/cellar for {VISITOR2_EMAIL} omits the expired {RELEASE_CLOSED} bottle"
    lapsed = [e for e in cellar_items(visitor2_client)
              if str(e.get("releaseId")) == RELEASE_EMBER and str(e.get("state")) == "lapsed"]
    assert lapsed, f"the offer seeded thirteen hours back on {RELEASE_EMBER} does not read lapsed"
    ember = httpx.get(api(f"/v1/releases/{RELEASE_EMBER}"), timeout=30.0)
    assert ember.status_code == 200 and int(body_of(ember).get("remaining")) >= 1, (
        f"the lapsed {RELEASE_EMBER} bottle did not return to remaining: {ember.text[:200]}"
    )
    sold_out = db.session_row(SESSION_SOLD_OUT)
    booked = [b for b in db.bookings_for_session(sold_out["id"]) if str(b.get("state")) == "booked"]
    assert sum(int(b.get("party_size")) for b in booked) == 4, "the seeded full booking is not four seats"
