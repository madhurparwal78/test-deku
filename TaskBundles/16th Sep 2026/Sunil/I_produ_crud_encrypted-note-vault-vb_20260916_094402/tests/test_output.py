"""The one pytest module for Lockleaf.

Every observation here is black box: HTTP against the running app, the rendered page in a
real browser, reads of the declared database and object store through the capability
fixtures. Nothing inspects the agent's source.
"""
from __future__ import annotations

import base64
import json
import os
import re

import conftest
from conftest import (
    CANOPY,
    CANOPY_QUOTA_BYTES,
    COMPLETE,
    CONFIRMATION_PHRASE,
    CORPUS_PASSWORD,
    DEMO_NOTICE,
    DENIED,
    DENIED_OR_MISSING,
    ENVELOPE_LIMIT,
    FORBIDDEN_ITEM_COLUMNS,
    INVALID_TYPE,
    LAPSED_EMAIL,
    LAPSED_REVISIONS,
    LEAF,
    LOCK_PASSCODE,
    MEMBER_EMAIL,
    NOT_FOUND_HEADING,
    OK,
    OWNER_EMAIL,
    PENDING,
    PINNED_TITLE,
    PINNED_WORDS,
    PLAN_LIMIT,
    PUBLIC_ROUTES,
    RENEWAL_TITLE,
    SAVED_STATUS,
    SEARCH_LABEL,
    SIGNUP_WARNING,
    START_OVER_BUTTON,
    START_OVER_LINK,
    TOO_LARGE,
    UNOPENABLE_HEADING,
    UUID_CONFLICT,
    VERSION_CONFLICT,
    ACTIVE,
)


def test_note_written_in_browser_leaves_no_plaintext_on_server(page, app_url, backend):
    """A note written in the browser reaches the server sealed: no readable trace anywhere."""
    tag = conftest.run_tag()
    title, words = f"Tidewater {tag}", f"sealed harbour words {tag}"
    log = conftest.record_requests(page)
    conftest.sign_in_through_page(page, app_url, OWNER_EMAIL, CORPUS_PASSWORD)
    uid = conftest.create_note_through_page(page, app_url, title, words)
    row = conftest.poll_until(lambda: backend.one("items", uuid=uid),
                              f"no items row appeared for the note {uid}")
    assert row.get("content_type") == "note", (
        f"the stored item {uid} has content_type {row.get('content_type')!r}, expected note")
    for needle in conftest.encodings(tag):
        hits = conftest.rows_containing(backend, needle)
        assert not hits, (
            f"the words of a note written in the browser are readable on the server in "
            f"{hits} (needle {needle!r}); every note must be sealed before it is stored")
    leaked = conftest.requests_carrying(log, conftest.encodings(tag))
    assert not leaked, (
        f"requests carried the note's words in readable form: {leaked[:5]}")


def test_note_reopens_intact_in_a_fresh_browser(browser, app_url):
    """A note closed on one browser opens with the same words on a fresh one."""
    tag = conftest.run_tag()
    title, words = f"Lighthouse {tag}", f"kept across devices {tag}"
    first, first_page = conftest.new_page(browser)
    conftest.sign_in_through_page(first_page, app_url, OWNER_EMAIL, CORPUS_PASSWORD)
    uid = conftest.create_note_through_page(first_page, app_url, title, words)
    first.close()
    second, second_page = conftest.new_page(browser)
    conftest.sign_in_through_page(second_page, app_url, OWNER_EMAIL, CORPUS_PASSWORD)
    second_page.goto(f"{app_url}/notes/{uid}")
    second_page.get_by_text(words).first.wait_for(timeout=conftest.PAGE_TIMEOUT_MS)
    content = second_page.content()
    second.close()
    assert title in content, (
        f"the note {uid} opened on a fresh browser without its title {title!r}")


def test_sign_in_and_signup_requests_never_carry_the_password(page, app_url, backend):
    """Neither creating an account nor signing in sends the password in any form."""
    tag = conftest.run_tag()
    identifier = "probe-" + tag + conftest.PROBE_DOMAIN
    password = f"Lantern-{tag}-harbour"
    log = conftest.record_requests(page)
    page.goto(f"{app_url}/signup")
    page.get_by_label("Email").fill(identifier)
    page.get_by_label("Password", exact=True).fill(password)
    page.get_by_label("Confirm password").fill(password)
    page.get_by_role("button", name="Create account").click()
    page.wait_for_url(re.compile(r".*/notes.*"), timeout=conftest.PAGE_TIMEOUT_MS)
    conftest.poll_until(lambda: backend.count("accounts", identifier=identifier) == 1,
                        f"no accounts row appeared for {identifier}")
    other = page.context.new_page()
    other_log = conftest.record_requests(other)
    conftest.sign_in_through_page(other, app_url, OWNER_EMAIL, CORPUS_PASSWORD)
    for secret in (password, CORPUS_PASSWORD):
        leaked = conftest.requests_carrying(log + other_log, conftest.encodings(secret))
        assert not leaked, (
            f"a request carried the password in readable or encoded form: {leaked[:3]}")
    stored = conftest.rows_containing(backend, password)
    assert not stored, f"the chosen password is stored readable in {stored}"


def test_same_words_saved_twice_produce_different_envelopes(page, app_url, backend):
    """Saving identical words again seals a different envelope under a fresh nonce."""
    tag = conftest.run_tag()
    first_words, other_words = f"same words {tag}", f"other words {tag}"
    conftest.sign_in_through_page(page, app_url, OWNER_EMAIL, CORPUS_PASSWORD)
    uid = conftest.create_note_through_page(page, app_url, f"Nonce {tag}", first_words)
    first = conftest.poll_until(lambda: backend.one("items", uuid=uid),
                                f"no items row for {uid}")
    body = page.get_by_label("Note body")
    body.fill(other_words)
    middle = conftest.poll_until(
        lambda: (lambda r: r if r and r["version"] > first["version"] else None)(
            backend.one("items", uuid=uid)),
        f"the edit of {uid} never reached the server")
    body.fill(first_words)
    last = conftest.poll_until(
        lambda: (lambda r: r if r and r["version"] > middle["version"] else None)(
            backend.one("items", uuid=uid)),
        f"the second save of {uid} never reached the server")
    page.get_by_text(SAVED_STATUS).first.wait_for(timeout=conftest.PAGE_TIMEOUT_MS)
    assert last["envelope"] != first["envelope"], (
        f"the note {uid} saved the same words twice as the identical envelope; every save "
        f"must be sealed under a fresh nonce")


def test_undecryptable_item_is_named_never_shown_empty(page, app_url, api):
    """An item that cannot be opened is shown named, with no editor over it."""
    token = conftest.sign_in_through_page(page, app_url, OWNER_EMAIL, CORPUS_PASSWORD)
    uid = conftest.new_uuid()
    with conftest.client_for(token) as client:
        reply = conftest.sync(client, api, items=[conftest.note_item(uid)])
    assert conftest.saved_version(reply, uid) is not None, (
        f"an opaque note item was not saved for the owner: {json.dumps(reply)[:300]}")
    page.goto(f"{app_url}/notes/{uid}")
    page.get_by_text(UNOPENABLE_HEADING).first.wait_for(timeout=conftest.PAGE_TIMEOUT_MS)
    assert uid in page.content(), (
        f"the unopenable note page does not name its uuid {uid}")
    assert page.get_by_label("Note body").count() == 0, (
        "an unopenable note offers a Note body editor that could save over it")


def test_search_query_never_leaves_the_browser(page, app_url):
    """Typing into Search notes narrows the table without sending the query anywhere."""
    conftest.sign_in_through_page(page, app_url, OWNER_EMAIL, CORPUS_PASSWORD)
    page.goto(f"{app_url}/notes")
    page.get_by_text(PINNED_TITLE).first.wait_for(timeout=conftest.PAGE_TIMEOUT_MS)
    log = conftest.record_requests(page)
    page.get_by_label(SEARCH_LABEL).fill("renewal")
    page.get_by_text(RENEWAL_TITLE).first.wait_for(timeout=conftest.PAGE_TIMEOUT_MS)
    conftest.settle()
    leaked = conftest.requests_carrying(log, ("renewal",))
    assert not leaked, f"the search query left the browser in {leaked[:3]}"


def test_locked_app_holds_no_note_words_in_page(page, app_url):
    """Locking discards unsealed words from the page until the passcode is entered."""
    conftest.sign_in_through_page(page, app_url, OWNER_EMAIL, CORPUS_PASSWORD)
    page.goto(f"{app_url}/settings/lock")
    page.get_by_label("Passcode", exact=True).fill(LOCK_PASSCODE)
    page.get_by_label("Confirm passcode").fill(LOCK_PASSCODE)
    page.get_by_role("button", name="Turn on lock").click()
    page.goto(f"{app_url}/notes")
    page.get_by_text(PINNED_TITLE).first.wait_for(timeout=conftest.PAGE_TIMEOUT_MS)
    page.get_by_text("Lock now").first.click()
    page.wait_for_url(re.compile(r".*/locked.*"), timeout=conftest.PAGE_TIMEOUT_MS)
    content = page.content()
    assert PINNED_TITLE not in content and PINNED_WORDS not in content, (
        "the locked page still holds unsealed note words")
    page.get_by_label("Passcode", exact=True).fill(LOCK_PASSCODE)
    page.get_by_role("button", name="Unlock").click()
    page.get_by_text(PINNED_TITLE).first.wait_for(timeout=conftest.PAGE_TIMEOUT_MS)


def test_item_table_has_no_readable_content_columns(backend):
    """The items table carries its pinned columns and no column for typed content."""
    columns = {r["column_name"] for r in backend.query(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema = 'public' AND table_name = 'items'")}
    for pinned in ("uuid", "account_id", "content_type", "envelope", "version", "deleted",
                   "created_at", "updated_at"):
        assert pinned in columns, f"the items table has no {pinned!r} column: {sorted(columns)}"
    exposed = sorted(columns & set(FORBIDDEN_ITEM_COLUMNS))
    assert not exposed, f"the items table exposes readable content columns {exposed}"


def test_foreign_account_item_read_is_denied(api):
    """One account reading another account's item is denied as not found."""
    owner, stranger = conftest.register_probe(api), conftest.register_probe(api)
    item = conftest.note_item()
    with conftest.client_for(owner["token"]) as client:
        conftest.sync(client, api, items=[item])
        own = conftest.get_item(client, api, item["uuid"])
    assert own.status_code == 200, f"the owner cannot read its own item: {own.status_code}"
    with conftest.client_for(stranger["token"]) as client:
        foreign = conftest.get_item(client, api, item["uuid"])
    assert foreign.status_code in DENIED_OR_MISSING, (
        f"another account read the item {item['uuid']} with {foreign.status_code}; "
        f"body={foreign.text[:200]}")
    assert item["envelope"] not in foreign.text, "the denied reply still carries the envelope"
    with conftest.client_for(None) as client:
        unsigned = conftest.get_item(client, api, item["uuid"])
    assert unsigned.status_code in DENIED, (
        f"a request with no bearer token read an item with {unsigned.status_code}")


def test_foreign_uuid_write_is_refused_as_uuid_conflict(api):
    """Writing to another account's uuid is a uuid_conflict and changes nothing."""
    owner, stranger = conftest.register_probe(api), conftest.register_probe(api)
    item = conftest.note_item()
    with conftest.client_for(owner["token"]) as client:
        conftest.sync(client, api, items=[item])
    intrusion = conftest.note_item(item["uuid"])
    with conftest.client_for(stranger["token"]) as client:
        reply = conftest.sync(client, api, items=[intrusion])
    conflict = conftest.conflict_for(reply, item["uuid"])
    assert conflict and conflict.get("type") == UUID_CONFLICT, (
        f"a write to another account's uuid returned {json.dumps(reply)[:300]}")
    assert item["envelope"] not in json.dumps(reply), "the uuid_conflict disclosed the envelope"
    with conftest.client_for(owner["token"]) as client:
        stored = conftest.get_item(client, api, item["uuid"]).json()
    assert stored.get("envelope") == item["envelope"], "the owner's item changed"


def test_sync_returns_only_the_accounts_own_items(api):
    """A sync from the beginning returns an account's own items and nobody else's."""
    owner, stranger = conftest.register_probe(api), conftest.register_probe(api)
    owned = [conftest.note_item() for _ in range(3)]
    mine = conftest.note_item()
    with conftest.client_for(owner["token"]) as client:
        conftest.sync(client, api, items=owned)
    with conftest.client_for(stranger["token"]) as client:
        conftest.sync(client, api, items=[mine])
        delivered, _ = conftest.pull_all(client, api)
    uuids = {i.get("uuid") for i in delivered}
    assert not uuids & {i["uuid"] for i in owned}, "a sync returned another account's items"
    assert mine["uuid"] in uuids, "a sync from the beginning left out the account's own item"


def test_cursor_pages_deliver_every_item_exactly_once(api):
    """Items written together all arrive exactly once across cursor pages."""
    account = conftest.register_probe(api)
    items = [conftest.note_item() for _ in range(320)]
    with conftest.client_for(account["token"]) as client:
        reply = conftest.sync(client, api, items=items)
        assert len(reply.get("saved_items") or []) == 320, (
            f"a batch of 320 items saved {len(reply.get('saved_items') or [])}")
        delivered, cursor = conftest.pull_all(client, api, limit=conftest.PAGE_LIMIT)
    counts: dict = {}
    for i in delivered:
        counts[i.get("uuid")] = counts.get(i.get("uuid"), 0) + 1
    missing = [i["uuid"] for i in items if counts.get(i["uuid"], 0) == 0]
    repeated = [u for u, n in counts.items() if n > 1]
    assert not missing, f"{len(missing)} of 320 items never arrived across cursor pages"
    assert not repeated, f"{len(repeated)} items arrived more than once"
    assert cursor, "the final page returned no cursor"


def test_replayed_sync_request_changes_nothing(api):
    """A sync replayed with the same request_id returns the same answer and writes nothing."""
    account = conftest.register_probe(api)
    item = conftest.note_item()
    request_id = conftest.run_tag()
    with conftest.client_for(account["token"]) as client:
        first = conftest.sync(client, api, items=[item], request_id=request_id)
        again = conftest.sync(client, api, items=[item], request_id=request_id)
        stored = conftest.get_item(client, api, item["uuid"]).json()
    version = conftest.saved_version(first, item["uuid"])
    assert version is not None, f"the first sync saved nothing: {json.dumps(first)[:300]}"
    assert conftest.saved_version(again, item["uuid"]) == version, (
        "the replayed request reported a different version")
    assert stored.get("version") == version, (
        f"the replay moved the stored version from {version} to {stored.get('version')}")


def test_oversized_envelope_is_refused_whole(api):
    """An envelope past the limit is refused as too_large, never truncated, alone."""
    account = conftest.register_probe(api)
    big = conftest.note_item(envelope="a" * (ENVELOPE_LIMIT + 1))
    fine = conftest.note_item()
    with conftest.client_for(account["token"]) as client:
        reply = conftest.sync(client, api, items=[big, fine])
        lookup = conftest.get_item(client, api, big["uuid"])
    conflict = conftest.conflict_for(reply, big["uuid"])
    assert conflict and conflict.get("type") == TOO_LARGE, (
        f"an oversized envelope was not refused as too_large: {json.dumps(reply)[:300]}")
    assert lookup.status_code == 404, f"the oversized item was stored: {lookup.status_code}"
    assert conftest.saved_version(reply, fine["uuid"]) is not None, (
        "one refused item failed the other item in the same request")


def test_unknown_content_type_is_refused_per_item(api):
    """An item of an unknown type is refused as invalid_type and nothing else fails."""
    account = conftest.register_probe(api)
    odd = conftest.note_item(content_type="gadget")
    fine = conftest.note_item()
    with conftest.client_for(account["token"]) as client:
        reply = conftest.sync(client, api, items=[odd, fine])
    conflict = conftest.conflict_for(reply, odd["uuid"])
    assert conflict and conflict.get("type") == INVALID_TYPE, (
        f"an unknown content_type was not refused as invalid_type: {json.dumps(reply)[:300]}")
    assert conftest.saved_version(reply, fine["uuid"]) is not None, (
        "an invalid item failed the valid item beside it")


def test_stale_version_write_returns_conflict_and_keeps_stored_item(api):
    """A write from an older version comes back as a conflict carrying the stored item."""
    account = conftest.register_probe(api)
    item = conftest.note_item()
    with conftest.client_for(account["token"]) as client:
        v1 = conftest.saved_version(conftest.sync(client, api, items=[item]), item["uuid"])
        newer = conftest.note_item(item["uuid"], version=v1)
        conftest.sync(client, api, items=[newer])
        stale = conftest.note_item(item["uuid"], version=v1)
        reply = conftest.sync(client, api, items=[stale])
        stored = conftest.get_item(client, api, item["uuid"]).json()
    conflict = conftest.conflict_for(reply, item["uuid"])
    assert conflict and conflict.get("type") == VERSION_CONFLICT, (
        f"a stale write was not a version_conflict: {json.dumps(reply)[:300]}")
    assert (conflict.get("server_item") or {}).get("envelope") == newer["envelope"], (
        "the conflict did not carry the stored item as server_item")
    assert stored.get("envelope") == newer["envelope"], (
        "the stale write replaced the stored envelope")


def test_item_version_only_increases(api):
    """Each accepted save of an item raises its version."""
    account = conftest.register_probe(api)
    item = conftest.note_item()
    versions = []
    with conftest.client_for(account["token"]) as client:
        current = None
        for _ in range(3):
            reply = conftest.sync(client, api, items=[conftest.note_item(item["uuid"], version=current)])
            current = conftest.saved_version(reply, item["uuid"])
            versions.append(current)
    assert all(v is not None for v in versions), f"a save reported no version: {versions}"
    assert versions == sorted(versions) and len(set(versions)) == 3, (
        f"versions across three saves were {versions}; each save must raise the version")


def test_tombstone_syncs_to_a_device_holding_an_old_cursor(api):
    """Emptying the trash writes a tombstone that reaches a device holding an old cursor."""
    account = conftest.register_probe(api)
    other = conftest.sign_in_api(api, account["identifier"], account["auth_secret"], "tablet")
    assert other.status_code in OK, f"a second sign-in failed: {other.status_code}"
    item = conftest.note_item()
    with conftest.client_for(account["token"]) as laptop:
        version = conftest.saved_version(conftest.sync(laptop, api, items=[item]), item["uuid"])
    with conftest.client_for(other.json()["token"]) as tablet:
        _, old_cursor = conftest.pull_all(tablet, api)
        with conftest.client_for(account["token"]) as laptop:
            conftest.sync(laptop, api, items=[conftest.note_item(
                item["uuid"], version=version, envelope="", deleted=True)])
        delivered, _ = conftest.pull_all(tablet, api, cursor=old_cursor)
    match = [i for i in delivered if i.get("uuid") == item["uuid"]]
    assert match, "the tombstone never reached the device holding the older cursor"
    assert match[-1].get("deleted") is True and not match[-1].get("envelope"), (
        f"the delivered tombstone is not deleted with an empty envelope: {match[-1]}")


def test_stale_upload_cannot_resurrect_a_tombstone(api):
    """A returning device's older copy of a deleted item never brings the item back."""
    account = conftest.register_probe(api)
    item = conftest.note_item()
    with conftest.client_for(account["token"]) as client:
        v1 = conftest.saved_version(conftest.sync(client, api, items=[item]), item["uuid"])
        conftest.sync(client, api, items=[conftest.note_item(
            item["uuid"], version=v1, envelope="", deleted=True)])
        reply = conftest.sync(client, api, items=[conftest.note_item(item["uuid"], version=v1)])
        stored = conftest.get_item(client, api, item["uuid"]).json()
    conflict = conftest.conflict_for(reply, item["uuid"])
    assert conflict and conflict.get("type") == VERSION_CONFLICT, (
        f"an older copy of a tombstoned item was not a version_conflict: {json.dumps(reply)[:300]}")
    assert (conflict.get("server_item") or {}).get("deleted") is True, (
        "the conflict did not carry the tombstone")
    assert stored.get("deleted") is True, "the deleted item came back"


def change_password(api: str, account: dict) -> tuple:
    new_secret = os.urandom(32).hex()
    new_params = dict(account["key_params"], salt=os.urandom(16).hex())
    with conftest.client_for(account["token"]) as client:
        response = client.post(f"{api}/account/password", json={
            "current_auth_secret": account["auth_secret"], "auth_secret": new_secret,
            "key_params": new_params, "items_keys": []})
    return response, new_secret


def test_password_change_ends_every_other_session(api):
    """A password change ends every other session and the old secret stops working."""
    account = conftest.register_probe(api)
    other = conftest.sign_in_api(api, account["identifier"], account["auth_secret"])
    assert other.status_code in OK, f"a second session could not start: {other.status_code}"
    response, new_secret = change_password(api, account)
    assert response.status_code in OK, (
        f"POST {api}/account/password answered {response.status_code}; body={response.text[:300]}")
    fresh = response.json().get("token")
    with conftest.client_for(other.json()["token"]) as client:
        ended = client.get(f"{api}/sessions")
    assert ended.status_code in DENIED, (
        f"the other session still works after a password change: {ended.status_code}")
    with conftest.client_for(fresh) as client:
        listing = client.get(f"{api}/sessions")
    assert listing.status_code == 200, "the fresh token is refused"
    assert isinstance(listing.json(), list), (
        f"GET {api}/sessions is not a top-level JSON array: {listing.text[:200]}")
    old = conftest.sign_in_api(api, account["identifier"], account["auth_secret"])
    assert conftest.is_client_error(old.status_code), (
        f"the old authentication secret still signs in: {old.status_code}")
    new = conftest.sign_in_api(api, account["identifier"], new_secret)
    assert new.status_code in OK, f"the new authentication secret is refused: {new.status_code}"


def test_password_change_rewrites_no_note(api):
    """A password change leaves every note at the version it had."""
    account = conftest.register_probe(api)
    notes = [conftest.note_item() for _ in range(3)]
    with conftest.client_for(account["token"]) as client:
        reply = conftest.sync(client, api, items=notes)
        before = {n["uuid"]: conftest.saved_version(reply, n["uuid"]) for n in notes}
        _, cursor = conftest.pull_all(client, api)
    response, _ = change_password(api, account)
    assert response.status_code in OK, f"the password change failed: {response.status_code}"
    with conftest.client_for(response.json()["token"]) as client:
        delivered, _ = conftest.pull_all(client, api, cursor=cursor)
        after = {u: conftest.get_item(client, api, u).json().get("version") for u in before}
    touched = [i.get("uuid") for i in delivered if i.get("content_type") == "note"]
    assert not touched, f"the password change rewrote notes {touched}"
    assert after == before, f"note versions moved across a password change: {before} -> {after}"


def test_reused_refresh_token_ends_the_session(api):
    """Presenting a spent refresh token ends the whole session it belongs to."""
    account = conftest.register_probe(api)
    with conftest.client_for(None) as client:
        first = client.post(f"{api}/sessions/refresh",
                            json={"refresh_token": account["refresh_token"]})
        assert first.status_code in OK, f"a first refresh failed: {first.status_code}"
        rotated = first.json()
        reuse = client.post(f"{api}/sessions/refresh",
                            json={"refresh_token": account["refresh_token"]})
        assert conftest.is_client_error(reuse.status_code), (
            f"a spent refresh token was accepted again: {reuse.status_code}")
        chained = client.post(f"{api}/sessions/refresh",
                              json={"refresh_token": rotated["refresh_token"]})
    assert conftest.is_client_error(chained.status_code), (
        f"the refresh token that replaced a reused one still works: {chained.status_code}")
    with conftest.client_for(rotated["token"]) as client:
        ended = client.get(f"{api}/sessions")
    assert ended.status_code in DENIED, (
        f"the access token of a session ended by reuse still works: {ended.status_code}")


def test_unknown_identifier_receives_stable_synthetic_key_params(anonymous, api):
    """Unknown identifiers get stable key parameters shaped like a real account's."""
    real = anonymous.get(f"{api}/auth/params", params={"identifier": OWNER_EMAIL})
    assert real.status_code == 200, f"key parameters for a seeded account: {real.status_code}"
    first_id = "nobody-" + conftest.run_tag() + conftest.PROBE_DOMAIN
    second_id = "nobody-" + conftest.run_tag() + conftest.PROBE_DOMAIN
    one = anonymous.get(f"{api}/auth/params", params={"identifier": first_id})
    two = anonymous.get(f"{api}/auth/params", params={"identifier": first_id})
    three = anonymous.get(f"{api}/auth/params", params={"identifier": second_id})
    assert one.status_code == real.status_code == three.status_code, (
        f"an unknown identifier answered {one.status_code} where a real one answered "
        f"{real.status_code}")
    assert one.json().get("key_params") == two.json().get("key_params"), (
        "synthetic key parameters differ between two requests for one identifier")
    assert one.json().get("key_params") != three.json().get("key_params"), (
        "two unknown identifiers received identical key parameters")
    real_params, fake = real.json().get("key_params"), one.json().get("key_params")
    if isinstance(real_params, dict):
        assert isinstance(fake, dict) and set(fake) == set(real_params), (
            f"synthetic key parameters carry fields {sorted(fake or {})} where a real "
            f"account carries {sorted(real_params)}")


def test_wrong_secret_and_unknown_identifier_are_refused_identically(api):
    """A wrong secret and an unknown identifier fail with the same outcome and body."""
    account = conftest.register_probe(api)
    wrong = conftest.sign_in_api(api, account["identifier"], os.urandom(32).hex())
    unknown = conftest.sign_in_api(api, "nobody-" + conftest.run_tag() + conftest.PROBE_DOMAIN,
                                   os.urandom(32).hex())
    assert conftest.is_client_error(wrong.status_code), (
        f"a wrong authentication secret answered {wrong.status_code}")
    assert wrong.status_code == unknown.status_code, (
        f"wrong secret answered {wrong.status_code} but unknown identifier answered "
        f"{unknown.status_code}")
    assert wrong.text == unknown.text, (
        f"the two refusals differ: {wrong.text[:200]!r} vs {unknown.text[:200]!r}")


def test_duplicate_identifier_signup_is_refused(api, backend):
    """A second account under the same normalised identifier is refused."""
    account = conftest.register_probe(api)
    with conftest.client_for(None) as client:
        again = client.post(f"{api}/accounts", json={
            "identifier": "  " + account["identifier"].upper() + " ",
            "auth_secret": os.urandom(32).hex(), "key_params": account["key_params"]})
    assert conftest.is_client_error(again.status_code), (
        f"a duplicate identifier answered {again.status_code}; body={again.text[:200]}")
    assert backend.count("accounts", identifier=account["identifier"]) == 1, (
        "a duplicate identifier created a second accounts row")


def test_sign_in_offers_start_over_and_no_password_reset(page, app_url):
    """Sign-in offers starting over, never a reset, and starting over needs the typed words."""
    page.goto(f"{app_url}/sign-in")
    resets = page.get_by_role("link", name=re.compile(r"reset|forgot|recover", re.I)).count()
    assert resets == 0, "the sign-in page offers a password reset or recovery link"
    page.get_by_role("link", name=START_OVER_LINK).click()
    page.wait_for_url(re.compile(r".*/start-over.*"), timeout=conftest.PAGE_TIMEOUT_MS)
    button = page.get_by_role("button", name=START_OVER_BUTTON)
    assert button.is_disabled(), "the start-over button is available before the words are typed"
    page.get_by_role("textbox").last.fill(CONFIRMATION_PHRASE)
    assert button.is_enabled(), (
        f"typing {CONFIRMATION_PHRASE!r} did not make the start-over button available")


def test_account_deletion_removes_items_and_frees_identifier(api, backend):
    """Deleting an account removes its items and its sign-in, and frees the identifier."""
    account = conftest.register_probe(api)
    item = conftest.note_item()
    with conftest.client_for(account["token"]) as client:
        conftest.sync(client, api, items=[item])
        gone = client.request("DELETE", f"{api}/account", json={
            "auth_secret": account["auth_secret"], "confirmation": CONFIRMATION_PHRASE})
    assert gone.status_code in OK + (204,), (
        f"DELETE {api}/account answered {gone.status_code}; body={gone.text[:300]}")
    assert backend.count("items", uuid=item["uuid"]) == 0, "the deleted account's item remains"
    after = conftest.sign_in_api(api, account["identifier"], account["auth_secret"])
    unknown = conftest.sign_in_api(api, "nobody-" + conftest.run_tag() + conftest.PROBE_DOMAIN,
                                   account["auth_secret"])
    assert after.status_code == unknown.status_code and after.text == unknown.text, (
        f"signing in to a deleted account differs from an unknown identifier: "
        f"{after.status_code} {after.text[:120]!r} vs {unknown.status_code} {unknown.text[:120]!r}")
    with conftest.client_for(None) as client:
        again = client.post(f"{api}/accounts", json={
            "identifier": account["identifier"], "auth_secret": os.urandom(32).hex(),
            "key_params": account["key_params"]})
    assert again.status_code in OK, (
        f"the identifier of a deleted account is not free again: {again.status_code}")


def storage_client(browser, app_url: str, identifier: str):
    return conftest.client_for(conftest.token_for(browser, app_url, identifier))


def upload(client, api: str, parts: list) -> str:
    uid = conftest.new_uuid()
    started = conftest.start_upload(client, api, uid, len(parts))
    assert started.status_code in OK, (
        f"POST {api}/files answered {started.status_code}; body={started.text[:300]}")
    for index, data in enumerate(parts):
        put = conftest.put_chunk(client, api, uid, index, data)
        assert put.status_code in OK, f"chunk {index} upload answered {put.status_code}"
    return uid


def test_uploaded_chunks_are_stored_under_the_vault_key_scheme(browser, app_url, api, store, backend):
    """A completed upload stores each sealed chunk in the bucket under its vault key."""
    parts = [os.urandom(2048), os.urandom(1024)]
    with storage_client(browser, app_url, OWNER_EMAIL) as client:
        uid = upload(client, api, parts)
        done = client.post(f"{api}/files/{uid}/complete")
    assert done.status_code in OK and done.json().get("status") == COMPLETE, (
        f"completing a fully uploaded file answered {done.status_code}: {done.text[:300]}")
    for index in range(len(parts)):
        key = f"vault/{uid}/{index}"
        assert store.exists(key), f"no object is stored at {key}"
    row = backend.one("file_uploads", file_uuid=uid)
    assert row and row.get("status") == COMPLETE, f"file_uploads row for {uid}: {row}"


def test_upload_missing_a_chunk_cannot_complete(browser, app_url, api, backend):
    """A file missing a chunk is refused completion and stays pending."""
    with storage_client(browser, app_url, OWNER_EMAIL) as client:
        uid = conftest.new_uuid()
        assert conftest.start_upload(client, api, uid, 2).status_code in OK
        assert conftest.put_chunk(client, api, uid, 0, os.urandom(512)).status_code in OK
        done = client.post(f"{api}/files/{uid}/complete")
    assert conftest.is_client_error(done.status_code), (
        f"completing a file missing a chunk answered {done.status_code}")
    row = backend.one("file_uploads", file_uuid=uid)
    assert row and row.get("status") == PENDING, f"the incomplete file is not pending: {row}"


def test_storage_usage_counts_sealed_chunk_bytes(browser, app_url, api):
    """The storage figure rises by exactly the sealed bytes stored."""
    with storage_client(browser, app_url, OWNER_EMAIL) as client:
        before = client.get(f"{api}/account/storage").json()
        uid = upload(client, api, [os.urandom(1000), os.urandom(1500)])
        assert client.post(f"{api}/files/{uid}/complete").status_code in OK
        after = client.get(f"{api}/account/storage").json()
    assert int(after["used_bytes"]) - int(before["used_bytes"]) == 2500, (
        f"used_bytes moved from {before['used_bytes']} to {after['used_bytes']} after "
        f"storing 2500 sealed bytes")
    assert int(after["quota_bytes"]) == CANOPY_QUOTA_BYTES, (
        f"a Canopy account reports quota_bytes {after['quota_bytes']}")


def test_other_account_cannot_download_file_chunk(browser, app_url, api):
    """A file chunk is served to its owner and to no other account."""
    data = os.urandom(777)
    with storage_client(browser, app_url, OWNER_EMAIL) as client:
        uid = upload(client, api, [data])
        client.post(f"{api}/files/{uid}/complete")
        own = client.get(f"{api}/files/{uid}/chunks/0")
    assert own.status_code == 200 and own.content == data, (
        f"the owner could not download its own chunk: {own.status_code}")
    stranger = conftest.register_probe(api)
    with conftest.client_for(stranger["token"]) as client:
        foreign = client.get(f"{api}/files/{uid}/chunks/0")
    assert foreign.status_code in DENIED_OR_MISSING, (
        f"another account downloaded the chunk with {foreign.status_code}")


def lapsed_file_uuids(client, api: str) -> list:
    delivered, _ = conftest.pull_all(client, api)
    return [i["uuid"] for i in delivered
            if i.get("content_type") == "file" and not i.get("deleted")]


def test_expired_account_still_downloads_existing_file_chunks(browser, app_url, api):
    """After a lapse every existing file still downloads."""
    with storage_client(browser, app_url, LAPSED_EMAIL) as client:
        files = lapsed_file_uuids(client, api)
        assert files, "the lapsed account holds no file items to download"
        for uid in files:
            chunk = client.get(f"{api}/files/{uid}/chunks/0")
            assert chunk.status_code == 200 and chunk.content, (
                f"the lapsed account cannot download file {uid}: {chunk.status_code}")


def test_expired_account_new_upload_is_refused(browser, app_url, api, store):
    """A lapsed account cannot start a new upload and nothing is stored."""
    with storage_client(browser, app_url, LAPSED_EMAIL) as client:
        uid = conftest.new_uuid()
        started = conftest.start_upload(client, api, uid, 1)
        subscription = client.get(f"{api}/account/subscription").json()
    assert conftest.is_client_error(started.status_code), (
        f"a lapsed account started an upload: {started.status_code}")
    assert subscription.get("status") == "expired" and subscription.get("effective_plan") == LEAF, (
        f"the lapsed subscription reads {subscription}")
    assert not store.list(f"vault/{uid}/"), "a refused upload stored an object"


def test_expired_account_keeps_its_revisions(browser, app_url, api):
    """A lapsed account keeps every revision it had."""
    with storage_client(browser, app_url, LAPSED_EMAIL) as client:
        delivered, _ = conftest.pull_all(client, api)
    revisions = [i for i in delivered
                 if i.get("content_type") == "revision" and not i.get("deleted")]
    assert len(revisions) >= LAPSED_REVISIONS, (
        f"the lapsed account holds {len(revisions)} revisions, expected {LAPSED_REVISIONS}")


def test_leaf_account_revision_sync_is_refused_as_plan_limit(api):
    """A revision sent from a Leaf account is refused as plan_limit and not stored."""
    account = conftest.register_probe(api)
    revision = conftest.note_item(content_type="revision")
    with conftest.client_for(account["token"]) as client:
        reply = conftest.sync(client, api, items=[revision])
        lookup = conftest.get_item(client, api, revision["uuid"])
    conflict = conftest.conflict_for(reply, revision["uuid"])
    assert conflict and conflict.get("type") == PLAN_LIMIT, (
        f"a Leaf revision was not refused as plan_limit: {json.dumps(reply)[:300]}")
    assert lookup.status_code == 404, f"the refused revision was stored: {lookup.status_code}"


def test_subscription_owner_cannot_reach_member_items(browser, app_url, api):
    """The owner of a shared subscription reaches none of a member's items."""
    with storage_client(browser, app_url, MEMBER_EMAIL) as member:
        delivered, _ = conftest.pull_all(member, api)
    member_items = [i["uuid"] for i in delivered if not i.get("deleted")]
    assert member_items, "the member account holds no items"
    with storage_client(browser, app_url, OWNER_EMAIL) as owner:
        for uid in member_items[:5]:
            response = conftest.get_item(owner, api, uid)
            assert response.status_code in DENIED_OR_MISSING, (
                f"the subscription owner read member item {uid}: {response.status_code}")
        reply = conftest.sync(owner, api, items=[conftest.note_item(member_items[0])])
    conflict = conftest.conflict_for(reply, member_items[0])
    assert conflict and conflict.get("type") == UUID_CONFLICT, (
        f"the owner's write to a member item was not a uuid_conflict: {json.dumps(reply)[:300]}")


def test_member_effective_plan_is_canopy_through_sharing(browser, app_url, api):
    """A member's effective plan is Canopy through the owner's shared subscription."""
    with storage_client(browser, app_url, MEMBER_EMAIL) as member:
        mine = member.get(f"{api}/account/subscription").json()
    with storage_client(browser, app_url, OWNER_EMAIL) as owner:
        theirs = owner.get(f"{api}/account/subscription").json()
    assert mine.get("effective_plan") == CANOPY, f"the member subscription reads {mine}"
    assert mine.get("shared_by") == OWNER_EMAIL, f"the member is not shared by the owner: {mine}"
    assert theirs.get("plan") == CANOPY and theirs.get("status") == ACTIVE, (
        f"the owner subscription reads {theirs}")
    assert MEMBER_EMAIL in json.dumps(theirs.get("members")), (
        f"the owner does not see the member listed: {theirs.get('members')}")


def test_invited_member_keeps_items_after_removal(browser, app_url, api):
    """An accepted invitation grants Canopy, and removal returns Leaf keeping every item."""
    guest = conftest.register_probe(api)
    item = conftest.note_item()
    with conftest.client_for(guest["token"]) as client:
        conftest.sync(client, api, items=[item])
    with storage_client(browser, app_url, OWNER_EMAIL) as owner:
        invited = owner.post(f"{api}/subscription/invitations",
                             json={"identifier": guest["identifier"]})
        assert invited.status_code in OK and invited.json().get("status") == PENDING, (
            f"inviting {guest['identifier']} answered {invited.status_code}: {invited.text[:200]}")
        with conftest.client_for(guest["token"]) as client:
            pending = client.get(f"{api}/subscription/invitations").json()
            ids = [i.get("id") for i in pending if i.get("status") == PENDING]
            assert ids, f"the invited account sees no pending invitation: {pending}"
            accepted = client.post(f"{api}/subscription/invitations/{ids[0]}/accept")
            assert accepted.status_code in OK, f"accepting answered {accepted.status_code}"
            plan = client.get(f"{api}/account/subscription").json().get("effective_plan")
            assert plan == CANOPY, f"an accepted member's effective plan is {plan!r}"
        removed = owner.delete(f"{api}/subscription/members/{guest['identifier']}")
        assert removed.status_code in OK + (204,), f"removing the member answered {removed.status_code}"
    with conftest.client_for(guest["token"]) as client:
        plan = client.get(f"{api}/account/subscription").json().get("effective_plan")
        kept = conftest.get_item(client, api, item["uuid"])
    assert plan == LEAF, f"a removed member's effective plan is {plan!r}"
    assert kept.status_code == 200, "a removed member lost an item"


def test_altered_entitlement_is_not_valid(browser, app_url, api, anonymous):
    """A product-signed entitlement verifies, and an altered one does not."""
    with storage_client(browser, app_url, OWNER_EMAIL) as owner:
        token = owner.get(f"{api}/account/subscription").json().get("entitlement")
    parts = (token or "").split(".")
    assert len(parts) == 3, f"the entitlement is not three dot-separated parts: {token!r}"
    claims = json.loads(base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4)))
    assert claims.get("plan") == CANOPY and claims.get("identifier") == OWNER_EMAIL, (
        f"the entitlement claims read {claims}")
    good = anonymous.post(f"{api}/entitlements/verify", json={"entitlement": token})
    assert good.status_code == 200 and good.json().get("valid") is True, (
        f"a product-signed entitlement did not verify: {good.text[:200]}")
    forged_claims = base64.urlsafe_b64encode(
        json.dumps(dict(claims, plan="Branch")).encode()).decode().rstrip("=")
    forged = ".".join([parts[0], forged_claims, parts[2]])
    bad = anonymous.post(f"{api}/entitlements/verify", json={"entitlement": forged})
    assert bad.status_code == 200 and bad.json().get("valid") is False, (
        f"an altered entitlement verified: {bad.text[:200]}")


def test_health_endpoint_returns_ready(anonymous, api):
    """GET /api/health answers 200 once the app is ready."""
    response = anonymous.get(f"{api}/health")
    assert response.status_code == 200, (
        f"GET {api}/health returned {response.status_code}; body={response.text[:200]}")


def head_meta(page, name: str) -> str | None:
    return page.evaluate(
        "n => { const m = document.querySelector(`meta[name='${n}'], meta[property='${n}']`);"
        " return m ? m.getAttribute('content') : null; }", name)


def test_public_routes_carry_distinct_titles_and_descriptions(page, app_url):
    """Every public route has its own title and meta description."""
    titles, descriptions = {}, {}
    for route in PUBLIC_ROUTES:
        page.goto(f"{app_url}{route}", wait_until="domcontentloaded")
        titles[route] = page.title().strip()
        descriptions[route] = (head_meta(page, "description") or "").strip()
        assert titles[route], f"{route} has no document title"
        assert descriptions[route], f"{route} has no meta description"
    assert len(set(titles.values())) == len(PUBLIC_ROUTES), f"public routes share titles: {titles}"
    assert len(set(descriptions.values())) == len(PUBLIC_ROUTES), (
        f"public routes share descriptions: {descriptions}")


def test_public_routes_declare_resolving_preview_images(page, app_url, anonymous):
    """Every public route declares a social preview title and an image that resolves."""
    for route in PUBLIC_ROUTES:
        page.goto(f"{app_url}{route}", wait_until="domcontentloaded")
        title = head_meta(page, "og:title")
        image = head_meta(page, "og:image")
        assert title, f"{route} declares no social preview title"
        assert image, f"{route} declares no social preview image"
        target = image if image.startswith("http") else f"{app_url}/{image.lstrip('/')}"
        target = re.sub(r"^https?://[^/]+", app_url, target)
        resolved = anonymous.get(target, follow_redirects=True)
        assert resolved.status_code == 200, (
            f"the preview image {image} on {route} answered {resolved.status_code}")


def test_every_internal_link_on_public_routes_resolves(page, app_url, anonymous):
    """Every internal link on every public route resolves."""
    broken = []
    for route in PUBLIC_ROUTES:
        page.goto(f"{app_url}{route}", wait_until="domcontentloaded")
        hrefs = page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
        for href in hrefs:
            if not href.startswith(app_url):
                continue
            target = href.split("#")[0]
            response = anonymous.get(target, follow_redirects=True)
            if response.status_code >= 400:
                broken.append((route, target, response.status_code))
    assert not broken, f"internal links do not resolve: {broken[:10]}"


def test_signup_form_names_invalid_field_and_creates_nothing(page, app_url, backend):
    """A short password is refused beside its field and no account is created."""
    identifier = "short-" + conftest.run_tag() + conftest.PROBE_DOMAIN
    page.goto(f"{app_url}/signup")
    assert SIGNUP_WARNING in page.content(), (
        f"the signup form does not state {SIGNUP_WARNING!r}")
    page.get_by_label("Email").fill(identifier)
    page.get_by_label("Password", exact=True).fill("abcdefghijk")
    page.get_by_label("Confirm password").fill("abcdefghijk")
    page.get_by_role("button", name="Create account").click()
    conftest.settle()
    assert "/signup" in page.url, f"a short password left the signup form for {page.url}"
    field = page.get_by_label("Password", exact=True)
    invalid = field.get_attribute("aria-invalid") == "true"
    message = page.get_by_text(re.compile(r"password", re.I)).count() > 1
    assert invalid or message, "the signup form did not name the invalid password field"
    assert backend.count("accounts", identifier=identifier) == 0, (
        "a refused signup created an accounts row")


def test_no_storage_secret_in_downloaded_assets(page, app_url):
    """Nothing the browser downloads carries a server-held secret."""
    secrets = [os.environ.get("STORAGE_SECRET_KEY", ""), os.environ.get("STORAGE_ACCESS_KEY", "")]
    database = os.environ.get("DATABASE_URL", "")
    found = re.match(r"^[a-z]+://[^:]+:([^@]+)@", database)
    if found:
        secrets.append(found.group(1))
    secrets = [s for s in secrets if s]
    bodies = []
    page.on("response", lambda r: bodies.append(r) if r.url.startswith(app_url) else None)
    for route in PUBLIC_ROUTES + ("/demo",):
        page.goto(f"{app_url}{route}", wait_until="load")
    leaked = []
    for response in bodies:
        text = response.body().decode("utf-8", "replace") if response.status < 300 else ""
        for secret in secrets:
            if secret in text:
                leaked.append(response.url)
    assert secrets, "no server-held secret was available to look for"
    assert not leaked, f"downloaded assets carry a server-held secret: {sorted(set(leaked))}"


def test_unknown_route_renders_not_found_page(page, app_url, anonymous):
    """An unknown address answers not found with the product's own page."""
    route = f"/no-such-page-{conftest.run_tag()}"
    response = anonymous.get(f"{app_url}{route}")
    assert response.status_code == 404, f"an unknown route answered {response.status_code}"
    page.goto(f"{app_url}{route}")
    page.get_by_text(NOT_FOUND_HEADING).first.wait_for(timeout=conftest.PAGE_TIMEOUT_MS)
    hrefs = page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
    for wanted in ("/", "/plans", "/privacy", "/sign-in"):
        assert any(h == wanted or h.endswith(wanted) for h in hrefs if h), (
            f"the not-found page links nowhere near {wanted}; links are {hrefs[:20]}")


def test_demo_writes_nothing_to_the_server(page, app_url, backend):
    """The live demo creates nothing on the server."""
    before = backend.count("items")
    page.goto(f"{app_url}/demo")
    page.get_by_text(DEMO_NOTICE).first.wait_for(timeout=conftest.PAGE_TIMEOUT_MS)
    log = conftest.record_requests(page)
    page.get_by_label("Title").fill(f"Demo {conftest.run_tag()}")
    page.get_by_label("Note body").fill("words that stay on this device")
    conftest.settle()
    writes = [(m, u) for (m, u, _) in log
              if m in ("POST", "PUT", "PATCH", "DELETE") and "/api/" in u]
    assert not writes, f"the demo sent writes to the server: {writes[:5]}"
    assert backend.count("items") == before, "the demo created items rows"
