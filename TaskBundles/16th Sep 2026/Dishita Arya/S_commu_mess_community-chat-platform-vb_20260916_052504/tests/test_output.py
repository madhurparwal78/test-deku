"""The one Rookery pytest module. Every assertion is black box: HTTP, the declared
datastore and the declared inbox. Nothing here reads the application's source."""

from __future__ import annotations

import concurrent.futures

import conftest
from conftest import (
    CHANNEL_BUILD_LOG,
    CHANNEL_GENERAL,
    CHANNEL_MODS_ONLY,
    CONFLICT_STATUSES,
    DENIAL_STATUSES,
    GIFT_CODE,
    HERO_HEADLINE,
    INVITE_CODE,
    MAIL_SUBJECT_PREFIX,
    MEMBER2_EMAIL,
    MEMBER_EMAIL,
    MODERATOR_EMAIL,
    MSG_INVITE_SPENT,
    NOT_FOUND_HEADLINE,
    NOT_FOUND_STATUSES,
    OWNER_EMAIL,
    PAGE_SIZE_MAX,
    PAGE_SIZE_PARAM,
    PASSWORD,
    PERM_ADD_REACTIONS,
    PERM_SEND_MESSAGES,
    PERM_VIEW_CHANNEL,
    REFUSAL_STATUSES,
    ROLE_ARCHIVISTS,
    ROLE_REGULARS,
    SECOND_SPACE_CHANNEL,
    SPACE_MEMBER_CAP,
    SPACE_NAME,
    SPACE_SLUG,
    SUCCESS_STATUSES,
    TERMS_PATH,
    Session,
    describe,
    field,
    poll_until,
    probe_email,
    probe_handle,
    probe_nonce,
    rows_of,
    settle,
)

import appclient
import httpx


def _site(path: str) -> httpx.Response:
    """A plain GET against the public origin rather than the API prefix."""
    base = appclient.api_base().rsplit("/api", 1)[0]
    with httpx.Client(base_url=base, timeout=30.0,
                      follow_redirects=True) as client:
        return client.get(path)


def _channel_id(session: Session, name: str, space: str = SPACE_SLUG) -> str:
    response = session.channels(space)
    assert response.status_code in SUCCESS_STATUSES, (
        f"channel list for {space!r}: expected a success, got {describe(response)}")
    for row in rows_of(response.json()):
        if str(field(row, "name", default="")).lstrip("#") == name.lstrip("#"):
            return str(field(row, "id", "slug", "name"))
    raise AssertionError(
        f"channel {name!r} is not in the channel list for {space!r}: "
        f"{describe(response)}")


def _newest_message(session: Session, channel: str) -> dict:
    response = session.messages(channel, limit=1)
    assert response.status_code in SUCCESS_STATUSES, (
        f"newest message in {channel!r}: expected a success, got {describe(response)}")
    rows = rows_of(response.json())
    assert rows, f"newest message in {channel!r}: the page is empty, {describe(response)}"
    return rows[0]


def _join_new_member(email: str) -> tuple[Session, httpx.Response]:
    """Sign a fresh account up, then redeem the seeded invite with that account."""
    fresh = Session()
    created = fresh.signup(email, probe_handle(), "Probe Member")
    assert created.status_code in SUCCESS_STATUSES, (
        f"signup for {email!r}: expected a success, got {describe(created)}")
    joined = Session(appclient.login(email, PASSWORD), email)
    return joined, joined.redeem_invite(INVITE_CODE)


def test_visitor_joins_space_and_message_is_persisted(store):
    email = probe_email()
    joined, redeemed = _join_new_member(email)
    assert redeemed.status_code in SUCCESS_STATUSES, (
        f"redeeming {INVITE_CODE!r} as a new account: expected a success, "
        f"got {describe(redeemed)}")
    assert SPACE_NAME in redeemed.text, (
        f"the join confirmation must name {SPACE_NAME!r}: {describe(redeemed)}")

    channel = _channel_id(joined, CHANNEL_GENERAL)
    body = f"first word from {email}"
    sent = joined.send(channel, body)
    assert sent.status_code in SUCCESS_STATUSES, (
        f"sending into {CHANNEL_GENERAL!r} as a new member: expected a success, "
        f"got {describe(sent)}")

    settle()
    stored = poll_until(lambda: [row for row in store.rows("message", limit=2000)
                                 if field(row, "content") == body])
    assert len(stored) == 1, (
        f"exactly one message row must carry the sent content, found {len(stored)}; "
        f"send was {describe(sent)}")


def test_role_deny_and_allow_resolve_to_allow(member):
    channel = _channel_id(member, CHANNEL_BUILD_LOG)
    resolved = member.permissions(channel, MEMBER_EMAIL)
    assert resolved.status_code in SUCCESS_STATUSES, (
        f"resolving permissions in {CHANNEL_BUILD_LOG!r}: expected a success, "
        f"got {describe(resolved)}")
    granted = resolved.text
    assert PERM_SEND_MESSAGES in granted, (
        f"{MEMBER_EMAIL!r} holds {ROLE_REGULARS!r}, denied {PERM_SEND_MESSAGES} in "
        f"{CHANNEL_BUILD_LOG!r}, and {ROLE_ARCHIVISTS!r}, allowed it. Every role deny "
        f"is applied before every role allow, so the allow wins and "
        f"{PERM_SEND_MESSAGES} must be in the resolved set: {describe(resolved)}")

    sent = member.send(channel, f"build note {probe_nonce()}")
    assert sent.status_code in SUCCESS_STATUSES, (
        f"posting into {CHANNEL_BUILD_LOG!r} as {MEMBER_EMAIL!r}: the resolved set "
        f"allows it, so the send must succeed, got {describe(sent)}")


def test_invisible_channel_resolves_to_an_empty_permission_set(member, owner):
    channel = _channel_id(owner, CHANNEL_MODS_ONLY)
    resolved = member.permissions(channel, MEMBER_EMAIL)
    assert resolved.status_code in SUCCESS_STATUSES + NOT_FOUND_STATUSES, (
        f"resolving permissions in {CHANNEL_MODS_ONLY!r} for a member who cannot see "
        f"it: expected a success carrying an empty set or a not-found, "
        f"got {describe(resolved)}")
    if resolved.status_code in SUCCESS_STATUSES:
        assert PERM_SEND_MESSAGES not in resolved.text, (
            f"{CHANNEL_MODS_ONLY!r} denies {PERM_VIEW_CHANNEL} to everyone, which "
            f"voids the whole set, so {PERM_SEND_MESSAGES} must not be reported: "
            f"{describe(resolved)}")


def test_history_pages_return_newest_first_in_both_directions(member):
    channel = _channel_id(member, CHANNEL_GENERAL)
    marker = probe_nonce()
    for index in range(3):
        sent = member.send(channel, f"page probe {marker} {index}")
        assert sent.status_code in SUCCESS_STATUSES, (
            f"seeding a page probe into {CHANNEL_GENERAL!r}: expected a success, "
            f"got {describe(sent)}")
    settle()

    newest = member.messages(channel, limit=3)
    assert newest.status_code in SUCCESS_STATUSES, (
        f"reading the newest page: expected a success, got {describe(newest)}")
    rows = rows_of(newest.json())
    assert len(rows) >= 2, (
        f"the newest page must carry the probes just sent: {describe(newest)}")
    ids = [str(field(row, "id")) for row in rows]
    assert ids == sorted(ids, reverse=True), (
        f"a page is returned newest first, so the identifiers must descend, "
        f"got {ids}: {describe(newest)}")

    oldest_here = ids[-1]
    after = member.messages(channel, limit=3, after=oldest_here)
    assert after.status_code in SUCCESS_STATUSES, (
        f"reading a page of newer messages: expected a success, got {describe(after)}")
    after_ids = [str(field(row, "id")) for row in rows_of(after.json())]
    assert after_ids == sorted(after_ids, reverse=True), (
        f"a page of NEWER messages is returned newest first as well, which is the "
        f"trap: identifiers must descend, got {after_ids}: {describe(after)}")


def test_acknowledgement_never_moves_the_read_mark_backwards(member):
    channel = _channel_id(member, CHANNEL_GENERAL)
    first = member.send(channel, f"ack probe one {probe_nonce()}")
    assert first.status_code in SUCCESS_STATUSES, (
        f"seeding the first ack probe: expected a success, got {describe(first)}")
    older_id = str(field(first.json(), "id"))

    second = member.send(channel, f"ack probe two {probe_nonce()}")
    assert second.status_code in SUCCESS_STATUSES, (
        f"seeding the second ack probe: expected a success, got {describe(second)}")
    newer_id = str(field(second.json(), "id"))

    forward = member.ack(channel, newer_id)
    assert forward.status_code in SUCCESS_STATUSES, (
        f"acknowledging the newer message: expected a success, got {describe(forward)}")
    settle()

    backward = member.ack(channel, older_id)
    assert backward.status_code in SUCCESS_STATUSES, (
        f"acknowledging an older message is accepted and does nothing, so it must not "
        f"be refused: {describe(backward)}")
    settle()

    states = member.read_states()
    assert states.status_code in SUCCESS_STATUSES, (
        f"reading the read states: expected a success, got {describe(states)}")
    mark = None
    for row in rows_of(states.json()):
        if str(field(row, "channel_id", "channel")) == str(channel):
            mark = str(field(row, "last_read_id"))
    assert mark == newer_id, (
        f"the read mark is monotonic: after acknowledging {newer_id} then {older_id} "
        f"it must still stand at {newer_id}, found {mark}: {describe(states)}")


def test_concurrent_invite_redemption_stores_one_membership_row(store):
    before = len(store.memberships_in(SPACE_SLUG))
    assert before == SPACE_MEMBER_CAP - 1, (
        f"{SPACE_NAME!r} seeds {SPACE_MEMBER_CAP - 1} members against a cap of "
        f"{SPACE_MEMBER_CAP}, leaving exactly one seat, found {before} membership rows")

    contenders = []
    for _ in range(2):
        email = probe_email()
        fresh = Session()
        created = fresh.signup(email, probe_handle(), "Race Member")
        assert created.status_code in SUCCESS_STATUSES, (
            f"signup for a racing account: expected a success, got {describe(created)}")
        contenders.append(Session(appclient.login(email, PASSWORD), email))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda s: s.redeem_invite(INVITE_CODE), contenders))

    wins = [r for r in results if r.status_code in SUCCESS_STATUSES]
    losses = [r for r in results if r.status_code in CONFLICT_STATUSES + REFUSAL_STATUSES]
    assert len(wins) == 1, (
        f"{INVITE_CODE!r} carries a use limit of 1 and one seat remains, so exactly "
        f"one of two simultaneous redemptions succeeds, got "
        f"{[describe(r) for r in results]}")
    assert len(losses) == 1, (
        f"the losing redemption is refused rather than silently succeeding, got "
        f"{[describe(r) for r in results]}")
    assert MSG_INVITE_SPENT in losses[0].text, (
        f"the refusal reports {MSG_INVITE_SPENT!r}: {describe(losses[0])}")

    settle()
    after = len(store.memberships_in(SPACE_SLUG))
    assert after == SPACE_MEMBER_CAP, (
        f"the space holds at most {SPACE_MEMBER_CAP} members, and one seat was free, "
        f"so exactly one membership row is added: found {after} rows after the race")


def test_duplicate_send_with_one_nonce_stores_one_message_row(member, store):
    channel = _channel_id(member, CHANNEL_GENERAL)
    nonce = probe_nonce()
    body = f"retry probe {nonce}"

    first = member.send(channel, body, nonce=nonce)
    assert first.status_code in SUCCESS_STATUSES, (
        f"the first send: expected a success, got {describe(first)}")
    first_id = str(field(first.json(), "id"))

    for attempt in range(3):
        again = member.send(channel, body, nonce=nonce)
        assert again.status_code in SUCCESS_STATUSES, (
            f"retry {attempt} of a send carrying a stored nonce returns the original "
            f"message rather than refusing: {describe(again)}")
        assert str(field(again.json(), "id")) == first_id, (
            f"retry {attempt} must return the original message {first_id}, got "
            f"{describe(again)}")

    settle()
    stored = store.messages_with_nonce(nonce)
    assert len(stored) == 1, (
        f"a nonce is held for {conftest.NONCE_WINDOW_SECONDS} seconds per channel per "
        f"author, so four sends carrying one nonce leave exactly one message row, "
        f"found {len(stored)}")


def test_reaction_count_equals_stored_reaction_set(member, owner, moderator, store):
    channel = _channel_id(member, CHANNEL_GENERAL)
    seeded = member.send(channel, f"reaction probe {probe_nonce()}")
    assert seeded.status_code in SUCCESS_STATUSES, (
        f"seeding a message to react to: expected a success, got {describe(seeded)}")
    message_id = str(field(seeded.json(), "id"))
    emoji = "sparkles"

    sessions = [member, owner, moderator]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(lambda s: s.react(message_id, emoji), sessions))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda s: s.unreact(message_id, emoji), sessions[1:]))

    settle()
    stored = [row for row in store.reactions_for(message_id)
              if field(row, "emoji") == emoji]
    reported = member.messages(channel, limit=25)
    assert reported.status_code in SUCCESS_STATUSES, (
        f"reading the reacted message back: expected a success, got {describe(reported)}")
    shown = None
    for row in rows_of(reported.json()):
        if str(field(row, "id")) == message_id:
            for summary in rows_of(field(row, "reactions", default=[])):
                if field(summary, "emoji") == emoji:
                    shown = field(summary, "count")
    assert shown == len(stored), (
        f"a reaction count is the size of the set of members who reacted, never a "
        f"tally: the store holds {len(stored)} rows for {emoji!r} and the app reports "
        f"{shown}: {describe(reported)}")


def test_concurrent_gift_redemption_grants_one_entitlement_row(store):
    email = probe_email()
    joined, redeemed = _join_new_member(email)
    assert redeemed.status_code in SUCCESS_STATUSES + REFUSAL_STATUSES, (
        f"redeeming the seeded invite before a gift code: got {describe(redeemed)}")

    code_row = store.gift_code(GIFT_CODE)
    assert code_row is not None, (
        f"the gift code {GIFT_CODE!r} must be seeded as a row in the declared store")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: joined.redeem_gift(GIFT_CODE), range(2)))

    wins = [r for r in results if r.status_code in SUCCESS_STATUSES]
    assert len(wins) == 1, (
        f"{GIFT_CODE!r} is single use, so two simultaneous redemptions produce exactly "
        f"one grant and one clear refusal, got {[describe(r) for r in results]}")

    settle()
    granted = store.entitlements_for(email)
    assert len(granted) == 1, (
        f"exactly one entitlement row follows a single-use gift code, found "
        f"{len(granted)} for {email!r}")


def test_seeded_rows_are_present_for_every_account(store):
    for email in (OWNER_EMAIL, MODERATOR_EMAIL, MEMBER_EMAIL, MEMBER2_EMAIL):
        assert store.account(email) is not None, (
            f"the account {email!r} must be seeded as a row in the declared store")
    space = store.space(SPACE_SLUG)
    assert space is not None, (
        f"the space {SPACE_SLUG!r} must be seeded as a row in the declared store")
    assert int(field(space, "member_cap", default=0)) == SPACE_MEMBER_CAP, (
        f"{SPACE_NAME!r} carries a member cap of {SPACE_MEMBER_CAP}, found "
        f"{field(space, 'member_cap')}")
    invite = store.invite(INVITE_CODE)
    assert invite is not None, (
        f"the invite {INVITE_CODE!r} must be seeded as a row in the declared store")
    assert int(field(invite, "max_uses", default=0)) == 1, (
        f"{INVITE_CODE!r} carries a use limit of 1, found {field(invite, 'max_uses')}")


def test_unauthenticated_request_is_denied_at_the_api(visitor, member, store):
    channel = _channel_id(member, CHANNEL_GENERAL)
    before = store.table_row_count("message")

    read = visitor.messages(channel, limit=5)
    assert read.status_code in DENIAL_STATUSES, (
        f"an anonymous read of a channel is denied by the server, got {describe(read)}")

    sent = visitor.send(channel, f"anonymous probe {probe_nonce()}")
    assert sent.status_code in DENIAL_STATUSES, (
        f"an anonymous send is denied by the server, got {describe(sent)}")

    settle()
    after = store.table_row_count("message")
    assert after == before, (
        f"a denied request leaves the protected state unchanged: the message table "
        f"held {before} rows before the anonymous calls and {after} after")


def test_member_cannot_read_another_space(outsider, member, store):
    channel = _channel_id(member, CHANNEL_GENERAL)

    read = outsider.messages(channel, limit=5)
    assert read.status_code in NOT_FOUND_STATUSES + DENIAL_STATUSES, (
        f"{MEMBER2_EMAIL!r} belongs to the second space only, so a direct read of a "
        f"{SPACE_NAME!r} channel must not be served, got {describe(read)}")

    before = store.table_row_count("message")
    sent = outsider.send(channel, f"cross space probe {probe_nonce()}")
    assert sent.status_code in NOT_FOUND_STATUSES + DENIAL_STATUSES, (
        f"a send into a space the account has not joined must not be served, "
        f"got {describe(sent)}")

    settle()
    assert store.table_row_count("message") == before, (
        f"a refused cross-space send writes no message row: the table held {before} "
        f"rows before the attempt")

    listed = outsider.spaces()
    assert listed.status_code in SUCCESS_STATUSES, (
        f"listing the outsider's own spaces: expected a success, got {describe(listed)}")
    assert SPACE_NAME not in listed.text, (
        f"{SPACE_NAME!r} must not appear in the space list of an account that has not "
        f"joined it: {describe(listed)}")


def test_timed_out_member_is_denied_send_and_reaction(moderator, member, owner, store):
    channel = _channel_id(member, CHANNEL_GENERAL)
    seeded = owner.send(channel, f"timeout probe {probe_nonce()}")
    assert seeded.status_code in SUCCESS_STATUSES, (
        f"seeding a message to react to: expected a success, got {describe(seeded)}")
    message_id = str(field(seeded.json(), "id"))

    applied = moderator.timeout_member(MEMBER_EMAIL, "2099-01-01T00:00:00Z",
                                       "probe timeout")
    assert applied.status_code in SUCCESS_STATUSES, (
        f"a moderator applying a timeout within their authority: expected a success, "
        f"got {describe(applied)}")
    settle()

    try:
        read = member.messages(channel, limit=5)
        assert read.status_code in SUCCESS_STATUSES, (
            f"a timeout masks to viewing and reading, so the timed-out member must "
            f"still read the channel, got {describe(read)}")

        before = store.table_row_count("message")
        sent = member.send(channel, f"silenced probe {probe_nonce()}")
        assert sent.status_code in DENIAL_STATUSES, (
            f"a timed-out member is denied sending, got {describe(sent)}")

        reacted = member.react(message_id, "sparkles")
        assert reacted.status_code in DENIAL_STATUSES, (
            f"a timeout removes ADD_REACTIONS as well as sending, which is the half "
            f"usually missed: reacting must be denied, got {describe(reacted)}")

        settle()
        assert store.table_row_count("message") == before, (
            f"a denied send by a timed-out member writes no message row")
    finally:
        moderator.timeout_member(MEMBER_EMAIL, "1971-01-01T00:00:00Z", "probe cleared")


def test_role_reorder_does_not_change_resolved_permissions(owner, member):
    channel = _channel_id(member, CHANNEL_BUILD_LOG)
    first = member.permissions(channel, MEMBER_EMAIL)
    assert first.status_code in SUCCESS_STATUSES, (
        f"resolving permissions before the reorder: expected a success, "
        f"got {describe(first)}")
    assert PERM_SEND_MESSAGES in first.text, (
        f"the allow wins before any reorder, so {PERM_SEND_MESSAGES} must be present: "
        f"{describe(first)}")

    listed = owner.get(f"/spaces/{SPACE_SLUG}/roles")
    assert listed.status_code in SUCCESS_STATUSES, (
        f"listing the roles of {SPACE_SLUG!r}: expected a success, got {describe(listed)}")
    roles = {field(row, "name"): row for row in rows_of(listed.json())}
    for name in (ROLE_REGULARS, ROLE_ARCHIVISTS):
        assert name in roles, (
            f"the role {name!r} must be seeded in {SPACE_NAME!r}: {describe(listed)}")

    regulars = roles[ROLE_REGULARS]
    archivists = roles[ROLE_ARCHIVISTS]
    swap = owner.patch(f"/spaces/{SPACE_SLUG}/roles/{field(regulars, 'id')}",
                       {"position": field(archivists, "position")})
    assert swap.status_code in SUCCESS_STATUSES, (
        f"the owner reordering two roles below their own: expected a success, "
        f"got {describe(swap)}")
    settle()

    try:
        second = member.permissions(channel, MEMBER_EMAIL)
        assert second.status_code in SUCCESS_STATUSES, (
            f"resolving permissions after the reorder: expected a success, "
            f"got {describe(second)}")
        assert PERM_SEND_MESSAGES in second.text, (
            f"role position orders authority over other members, never a member's own "
            f"permissions, so reordering {ROLE_REGULARS!r} and {ROLE_ARCHIVISTS!r} "
            f"must leave {PERM_SEND_MESSAGES} granted: {describe(second)}")
    finally:
        owner.patch(f"/spaces/{SPACE_SLUG}/roles/{field(regulars, 'id')}",
                    {"position": field(regulars, "position")})


def test_invalid_signup_is_refused_and_writes_no_account(visitor, store):
    before = store.table_row_count("account")

    malformed = visitor.signup("not-an-address", probe_handle(), "Probe")
    assert malformed.status_code in REFUSAL_STATUSES, (
        f"a malformed address is refused inline, got {describe(malformed)}")
    assert "email" in malformed.text.lower(), (
        f"the refusal names the field at fault: {describe(malformed)}")

    short = visitor.request("POST", "/auth/signup",
                            {"email": probe_email(), "password": "abc",
                             "handle": probe_handle(), "display_name": "Probe"})
    assert short.status_code in REFUSAL_STATUSES, (
        f"a password below the minimum is refused, got {describe(short)}")
    assert "password" in short.text.lower(), (
        f"the refusal names the field at fault: {describe(short)}")

    settle()
    assert store.table_row_count("account") == before, (
        f"a rejected form writes nothing: the account table held {before} rows before "
        f"the two refused signups")


def test_page_size_above_the_cap_is_refused(member):
    channel = _channel_id(member, CHANNEL_GENERAL)
    over = member.get(f"/channels/{channel}/messages",
                      **{PAGE_SIZE_PARAM: PAGE_SIZE_MAX + 400})
    assert over.status_code in REFUSAL_STATUSES, (
        f"a page size above the cap of {PAGE_SIZE_MAX} is refused rather than quietly "
        f"served a smaller page, got {describe(over)}")
    assert str(PAGE_SIZE_MAX) in over.text, (
        f"the refusal names the cap {PAGE_SIZE_MAX}: {describe(over)}")


def test_unknown_address_answers_not_found():
    response = _site(f"/no-such-place-{probe_nonce()}")
    assert response.status_code in NOT_FOUND_STATUSES, (
        f"an unknown address answers not-found rather than answering as though the "
        f"page were fine, got {describe(response)}")
    assert NOT_FOUND_HEADLINE in response.text, (
        f"the not-found page is the product's own designed page carrying "
        f"{NOT_FOUND_HEADLINE!r}: {describe(response)}")


def test_terms_page_is_reachable_from_the_footer():
    home = _site("/")
    assert home.status_code in SUCCESS_STATUSES, (
        f"the home page: expected a success, got {describe(home)}")
    assert HERO_HEADLINE in home.text, (
        f"the home page carries the pinned hero line {HERO_HEADLINE!r}: "
        f"{describe(home)}")
    assert TERMS_PATH in home.text, (
        f"the terms page is reachable from the footer of every page, so {TERMS_PATH!r} "
        f"must be linked from the home page: {describe(home)}")

    terms = _site(TERMS_PATH)
    assert terms.status_code in SUCCESS_STATUSES, (
        f"the terms page at {TERMS_PATH!r}: expected a success, got {describe(terms)}")


def test_health_endpoint_reports_ready(visitor):
    response = visitor.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returns 200 once the app is ready, got {describe(response)}")


def test_mention_email_reaches_only_the_mentioned_member(member, inbox):
    channel = _channel_id(member, CHANNEL_GENERAL)
    marker = probe_nonce()
    sent = member.send(channel, f"<@{OWNER_EMAIL}> please look at {marker}",
                       mentions=[OWNER_EMAIL])
    assert sent.status_code in SUCCESS_STATUSES, (
        f"sending a message that mentions {OWNER_EMAIL!r}: expected a success, "
        f"got {describe(sent)}")

    delivered = poll_until(
        lambda: inbox.find(OWNER_EMAIL, subject_contains=MAIL_SUBJECT_PREFIX))
    assert delivered is not None, (
        f"a mention of a member with no live session sends exactly one mail to that "
        f"member's address; nothing carrying the subject prefix "
        f"{MAIL_SUBJECT_PREFIX!r} reached {OWNER_EMAIL!r}")
    assert delivered.subject.startswith(MAIL_SUBJECT_PREFIX), (
        f"the subject begins {MAIL_SUBJECT_PREFIX!r} then a space then the channel "
        f"name, got {delivered.subject!r}")
    assert CHANNEL_GENERAL in delivered.subject, (
        f"the subject names the channel {CHANNEL_GENERAL!r}, got {delivered.subject!r}")

    for other in (MODERATOR_EMAIL, MEMBER2_EMAIL, MEMBER_EMAIL):
        stray = inbox.find(other, subject_contains=marker)
        assert stray is None, (
            f"the mention mail reaches the mentioned member alone, with no cc and no "
            f"bcc, so nothing carrying {marker!r} may reach {other!r}")


def test_reaction_sends_no_mail(member, owner, inbox):
    channel = _channel_id(member, CHANNEL_GENERAL)
    marker = probe_nonce()
    seeded = owner.send(channel, f"quiet probe {marker}")
    assert seeded.status_code in SUCCESS_STATUSES, (
        f"seeding a message to react to: expected a success, got {describe(seeded)}")
    message_id = str(field(seeded.json(), "id"))

    before = inbox.count(OWNER_EMAIL)
    reacted = member.react(message_id, "sparkles")
    assert reacted.status_code in SUCCESS_STATUSES, (
        f"reacting to a message: expected a success, got {describe(reacted)}")

    settle()
    after = inbox.count(OWNER_EMAIL)
    assert after == before, (
        f"a reaction is a non-transition and sends no mail: {OWNER_EMAIL!r} held "
        f"{before} messages before the reaction and {after} after")
