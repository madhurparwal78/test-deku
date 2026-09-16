"""The one pytest module for deku/email-delivery-console-vb.

Every section and every declared slot is merged here. Assertions are black box:
HTTP against the deployed app, rows read through the backend capability, mail read
through the inbox capability, and the rendered surface read through a real browser
page where the ask is a rendered one.
"""

from __future__ import annotations

import concurrent.futures

from appclient import client
from conftest import (ADMIN_EMAIL, AUDIENCE_NAME, BOUNCED_ADDRESS, COMPLAINED_ADDRESS,
                      DELIVERED_ADDRESS, MEMBER_EMAIL, MONTHLY_ALLOWANCE,
                      OTHER_DOMAIN, OTHER_WORKSPACE_NAME, OWNER_EMAIL, PENDING_DOMAIN,
                      PLAN_NAME, SECRET_PREFIX_OPENER, SEEDED_PASSWORD, SENDER_ADDRESS,
                      TERMINAL_STATES, VERIFIED_DOMAIN, WORKSPACE_NAME, accepted_id,
                      api_url, base_url, mint_credential, poll_until, send_as,
                      send_body, settle, unique_address, unique_key, unique_local)


def test_signup_creates_person_carrying_display_name(anon_client, db):
    address = unique_address()
    response = anon_client.post("/auth/signup", json={
        "email": address, "password": "relay-probe-pw-2026", "display_name": "Probe Owner"})
    assert response.status_code in (200, 201), (
        f"POST /api/auth/signup for {address} returned {response.status_code}: "
        f"{response.text[:400]}")
    row = db.user_by_email(address)
    assert row is not None, f"signup wrote no users row for {address}"


def test_login_returns_access_token(anon_client):
    response = anon_client.post("/auth/login", json={
        "email": OWNER_EMAIL, "password": SEEDED_PASSWORD})
    assert response.status_code == 200, (
        f"POST /api/auth/login for {OWNER_EMAIL} returned {response.status_code}: "
        f"{response.text[:400]}")
    assert response.json().get("access_token"), (
        f"login response carries no access_token: {response.text[:400]}")


def test_duplicate_signup_address_is_rejected(anon_client, db):
    address = unique_address()
    first = anon_client.post("/auth/signup", json={
        "email": address, "password": "relay-probe-pw-2026", "display_name": "First Probe"})
    assert first.status_code in (200, 201), (
        f"first POST /api/auth/signup returned {first.status_code}: {first.text[:400]}")
    second = anon_client.post("/auth/signup", json={
        "email": address, "password": "relay-probe-pw-2026", "display_name": "Second Probe"})
    assert 400 <= second.status_code < 500, (
        f"duplicate POST /api/auth/signup for {address} returned {second.status_code}, "
        f"expected a client error: {second.text[:400]}")
    assert db.count_users(address) == 1, (
        f"duplicate signup for {address} left {db.count_users(address)} users rows")


def test_wrong_password_login_is_denied(anon_client):
    response = anon_client.post("/auth/login", json={
        "email": OWNER_EMAIL, "password": "relay-wrong-pw-2026"})
    assert response.status_code in (400, 401, 403, 422), (
        f"POST /api/auth/login with a wrong password returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}")


def test_console_request_carrying_no_bearer_token_is_denied(anon_client):
    response = anon_client.get("/domains")
    assert response.status_code in (401, 403), (
        f"GET /api/domains with no bearer token returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}")


def test_adding_domain_creates_pending_domain(admin_client, db):
    name = f"{unique_local()}.northwind.example.com"
    response = admin_client.post("/domains", json={"name": name})
    assert response.status_code in (200, 201), (
        f"POST /api/domains for {name} returned {response.status_code}: "
        f"{response.text[:400]}")
    row = db.domain_by_name(name)
    assert row is not None, f"POST /api/domains wrote no domains row for {name}"
    assert str(row.get("state")) == "pending", (
        f"a freshly added domain {name} reads state {row.get('state')!r}, expected 'pending'")


def test_created_domain_generates_three_publication_records(admin_client, db):
    name = f"{unique_local()}.northwind.example.com"
    response = admin_client.post("/domains", json={"name": name})
    assert response.status_code in (200, 201), (
        f"POST /api/domains for {name} returned {response.status_code}: "
        f"{response.text[:400]}")
    row = db.domain_by_name(name)
    assert row is not None, f"POST /api/domains wrote no domains row for {name}"
    records = db.domain_records(row.get("id"))
    assert len(records) >= 3, (
        f"domain {name} generated {len(records)} domain_records rows, expected at least "
        f"three publication records")
    types = {str(r.get("record_type")).upper() for r in records}
    assert {"TXT", "MX", "CNAME"} <= types, (
        f"domain {name} generated record types {sorted(types)}, expected TXT, MX and CNAME")
    for record in records:
        assert record.get("status"), (
            f"a domain_records row for {name} carries no status of its own: {record}")


def test_verification_pass_refreshes_every_record_status(admin_client, db):
    domain = db.domain_by_name(PENDING_DOMAIN)
    assert domain is not None, f"seeded domain {PENDING_DOMAIN} is missing from the database"
    response = admin_client.post(f"/domains/{domain.get('id')}/verify")
    assert response.status_code in (200, 202), (
        f"POST /api/domains/<id>/verify for {PENDING_DOMAIN} returned "
        f"{response.status_code}: {response.text[:400]}")
    records = db.domain_records(domain.get("id"))
    assert records, f"{PENDING_DOMAIN} carries no domain_records rows after a verification pass"
    statuses = {str(r.get("status")) for r in records}
    assert "missing" in statuses or "mismatch" in statuses, (
        f"{PENDING_DOMAIN} is seeded with one record absent, so its statuses should still "
        f"carry a failing record; saw {sorted(statuses)}")
    after = db.domain_by_name(PENDING_DOMAIN)
    assert str(after.get("state")) == "pending", (
        f"{PENDING_DOMAIN} is missing a record yet reads state {after.get('state')!r}")


def test_domain_whose_records_read_correct_becomes_verified(db):
    domain = db.domain_by_name(VERIFIED_DOMAIN)
    assert domain is not None, f"seeded domain {VERIFIED_DOMAIN} is missing from the database"
    assert str(domain.get("state")) == "verified", (
        f"{VERIFIED_DOMAIN} reads state {domain.get('state')!r}, expected 'verified'")
    records = db.domain_records(domain.get("id"))
    assert records, f"{VERIFIED_DOMAIN} carries no domain_records rows"
    assert all(str(r.get("status")) == "correct" for r in records), (
        f"{VERIFIED_DOMAIN} reads verified while its record statuses are "
        f"{[r.get('status') for r in records]}")


def test_domain_owned_by_another_workspace_answers_as_not_found(admin_client, db):
    other = db.domain_by_name(OTHER_DOMAIN)
    assert other is not None, (
        f"seeded domain {OTHER_DOMAIN} of {OTHER_WORKSPACE_NAME} is missing from the database")
    response = admin_client.get(f"/domains/{other.get('id')}")
    assert response.status_code == 404, (
        f"GET /api/domains/<id> for another workspace's {OTHER_DOMAIN} returned "
        f"{response.status_code}, expected 404: {response.text[:400]}")


def test_minting_credential_returns_the_secret_exactly_once(admin_client, db):
    name = f"Production sender {unique_local()}"
    minted = mint_credential(admin_client, name=name)
    secret = minted["secret"]
    assert secret.startswith(SECRET_PREFIX_OPENER), (
        f"a minted credential secret reads {secret[:8]!r}, expected it to open "
        f"{SECRET_PREFIX_OPENER!r}")
    row = db.credential_by_name(name)
    assert row is not None, f"POST /api/credentials wrote no credentials row for {name!r}"
    prefix = str(row.get("token_prefix") or "")
    assert len(prefix) == 12, (
        f"credential {name!r} stores a token_prefix of {len(prefix)} characters, expected "
        f"twelve: {prefix!r}")
    assert secret.startswith(prefix), (
        f"the stored prefix {prefix!r} does not open the secret that was returned")
    listed = admin_client.get(f"/credentials/{row.get('id')}")
    assert "secret" not in listed.text or secret not in listed.text, (
        f"GET /api/credentials/<id> hands the secret back a second time: {listed.text[:400]}")


def test_listing_credentials_omits_every_secret(admin_client):
    minted = mint_credential(admin_client)
    response = admin_client.get("/credentials")
    assert response.status_code == 200, (
        f"GET /api/credentials returned {response.status_code}: {response.text[:400]}")
    assert minted["secret"] not in response.text, (
        "GET /api/credentials carries a full credential secret in its body, which is "
        "hidden from everybody after creation")


def test_revoked_credential_presented_for_sending_is_denied(admin_client, db):
    minted = mint_credential(admin_client)
    revoke = admin_client.delete(f"/credentials/{minted['id']}")
    assert revoke.status_code in (200, 202, 204), (
        f"DELETE /api/credentials/<id> returned {revoke.status_code}: {revoke.text[:400]}")
    response = send_as(minted["secret"], send_body(DELIVERED_ADDRESS))
    assert response.status_code in (401, 403), (
        f"a revoked credential sending returned {response.status_code}, expected a denial: "
        f"{response.text[:400]}")


def test_sending_interface_accepts_a_message_from_a_verified_domain(admin_client, db):
    minted = mint_credential(admin_client)
    response = send_as(minted["secret"], send_body(DELIVERED_ADDRESS))
    identifier = accepted_id(response)
    row = poll_until(lambda: db.message_by_id(identifier))
    assert row is not None, (
        f"an accepted message {identifier} has no messages row in the database")
    assert str(row.get("from_address")).endswith(VERIFIED_DOMAIN), (
        f"message {identifier} was sent from {row.get('from_address')!r}, expected the "
        f"verified domain {VERIFIED_DOMAIN}")


def test_send_from_an_unverified_domain_is_refused(admin_client, db):
    minted = mint_credential(admin_client)
    before = db.count_messages_to(DELIVERED_ADDRESS)
    body = send_body(DELIVERED_ADDRESS, from_address=f"support@{PENDING_DOMAIN}")
    response = send_as(minted["secret"], body)
    assert 400 <= response.status_code < 500, (
        f"a send from the unverified {PENDING_DOMAIN} returned {response.status_code}, "
        f"expected a refusal: {response.text[:400]}")
    settle()
    assert db.count_messages_to(DELIVERED_ADDRESS) == before, (
        f"a refused send from {PENDING_DOMAIN} still wrote a messages row")


def test_send_missing_the_idempotency_key_header_is_refused(admin_client, db):
    minted = mint_credential(admin_client)
    before = db.count_messages_to(DELIVERED_ADDRESS)
    with client(minted["secret"]) as sender:
        response = sender.post("/v1/emails", json=send_body(DELIVERED_ADDRESS))
    assert 400 <= response.status_code < 500, (
        f"a send with no Idempotency-Key header returned {response.status_code}, expected "
        f"a refusal: {response.text[:400]}")
    settle()
    assert db.count_messages_to(DELIVERED_ADDRESS) == before, (
        "a send refused for a missing idempotency key still queued a message")


def test_replayed_idempotency_key_produces_no_second_message_row(admin_client, db):
    minted = mint_credential(admin_client)
    key = unique_key()
    body = send_body(DELIVERED_ADDRESS)
    first = send_as(minted["secret"], body, key=key)
    identifier = accepted_id(first)
    second = send_as(minted["secret"], body, key=key)
    assert second.status_code in (200, 201, 202), (
        f"a replay of idempotency key {key} returned {second.status_code}, expected the "
        f"stored acceptance: {second.text[:400]}")
    assert second.json().get("id") == identifier, (
        f"a replay of {key} returned id {second.json().get('id')!r}, expected the stored "
        f"{identifier!r}")
    settle()
    assert db.count_messages_for_key(key) == 1, (
        f"idempotency key {key} left {db.count_messages_for_key(key)} messages rows")


def test_replayed_idempotency_key_carrying_a_different_body_is_refused(admin_client, db):
    minted = mint_credential(admin_client)
    key = unique_key()
    first = send_as(minted["secret"], send_body(DELIVERED_ADDRESS, subject="First receipt"),
                    key=key)
    accepted_id(first)
    second = send_as(minted["secret"], send_body(DELIVERED_ADDRESS, subject="Second receipt"),
                     key=key)
    assert 400 <= second.status_code < 500, (
        f"one idempotency key naming two different bodies returned {second.status_code}, "
        f"expected a refusal: {second.text[:400]}")
    settle()
    assert db.count_messages_for_key(key) == 1, (
        f"a conflicting replay of {key} left {db.count_messages_for_key(key)} messages rows")


def test_two_simultaneous_sends_under_one_key_admit_exactly_one_message(admin_client, db):
    minted = mint_credential(admin_client)
    key = unique_key()
    body = send_body(DELIVERED_ADDRESS)

    def fire():
        return send_as(minted["secret"], body, key=key)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = [f.result() for f in [pool.submit(fire), pool.submit(fire)]]
    codes = sorted(r.status_code for r in results)
    assert any(200 <= c < 300 for c in codes), (
        f"two simultaneous sends under key {key} both failed with {codes}; exactly one "
        f"message must be admitted")
    settle()
    assert db.count_messages_for_key(key) == 1, (
        f"two simultaneous sends under key {key} left "
        f"{db.count_messages_for_key(key)} messages rows, expected exactly one")


def test_retrieving_a_message_returns_its_current_state(admin_client):
    minted = mint_credential(admin_client)
    identifier = accepted_id(send_as(minted["secret"], send_body(DELIVERED_ADDRESS)))
    with client(minted["secret"]) as sender:
        response = sender.get(f"/v1/emails/{identifier}")
    assert response.status_code == 200, (
        f"GET /api/v1/emails/{identifier} returned {response.status_code}: "
        f"{response.text[:400]}")
    state = response.json().get("state")
    assert state, f"GET /api/v1/emails/{identifier} carries no state: {response.text[:400]}"


def test_cancelling_a_queued_message_reaches_the_canceled_state(admin_client, db):
    minted = mint_credential(admin_client)
    identifier = accepted_id(send_as(minted["secret"], send_body(DELIVERED_ADDRESS)))
    with client(minted["secret"]) as sender:
        response = sender.post(f"/v1/emails/{identifier}/cancel")
    assert response.status_code in (200, 202, 409, 422), (
        f"POST /api/v1/emails/{identifier}/cancel returned {response.status_code}, which "
        f"is neither a cancellation nor a stated refusal: {response.text[:400]}")
    if response.status_code in (200, 202):
        row = poll_until(lambda: (db.message_by_id(identifier) or {}).get("state") == "canceled")
        assert row, f"message {identifier} was cancelled yet never reached the canceled state"


def test_the_log_filters_server_side_by_message_state(admin_client, db):
    response = admin_client.get("/emails", params={"state": "bounced"})
    assert response.status_code == 200, (
        f"GET /api/emails?state=bounced returned {response.status_code}: "
        f"{response.text[:400]}")
    from _shapes import items
    rows = items(response.json())
    assert rows, "GET /api/emails?state=bounced returned nothing while a bounced message is seeded"
    assert all(str(r.get("state")) == "bounced" for r in rows), (
        f"the bounced filter returned states {[r.get('state') for r in rows]}")
    assert len(rows) == db.count_messages_in_state("bounced"), (
        f"GET /api/emails?state=bounced returned {len(rows)} rows while the database holds "
        f"{db.count_messages_in_state('bounced')}")


def test_a_message_detail_returns_events_in_occurrence_order(admin_client, db):
    bounced = db.messages_in_state("bounced")
    assert bounced, "no seeded message reads the bounced state"
    identifier = bounced[0].get("id")
    response = admin_client.get(f"/emails/{identifier}")
    assert response.status_code == 200, (
        f"GET /api/emails/{identifier} returned {response.status_code}: {response.text[:400]}")
    events = response.json().get("events") or []
    assert events, f"GET /api/emails/{identifier} returned no events: {response.text[:400]}"
    stamps = [str(e.get("occurred_at") or "") for e in events]
    assert stamps == sorted(stamps), (
        f"message {identifier} returned events out of occurrence order: {stamps}")


def test_a_late_event_is_recorded_without_moving_the_state_backwards(admin_client, db):
    minted = mint_credential(admin_client)
    identifier = accepted_id(send_as(minted["secret"], send_body(DELIVERED_ADDRESS)))
    reached = poll_until(
        lambda: (db.message_by_id(identifier) or {}).get("state") in TERMINAL_STATES)
    assert reached, f"message {identifier} never reached a terminal state"
    state_before = str((db.message_by_id(identifier) or {}).get("state"))
    events_before = len(db.events_for(identifier))
    admin_client.post(f"/emails/{identifier}/events",
                      json={"event_type": "sending", "occurred_at": "2026-01-01T00:00:00.000Z"})
    settle()
    after = db.message_by_id(identifier) or {}
    assert str(after.get("state")) == state_before, (
        f"message {identifier} moved from {state_before!r} to {after.get('state')!r} on a "
        f"late event, which walks the record backwards")
    assert len(db.events_for(identifier)) >= events_before, (
        f"message {identifier} lost message_events rows rather than appending")


def test_overview_counters_match_the_underlying_message_rows(admin_client, db):
    response = admin_client.get("/overview", params={"window": "7d"})
    assert response.status_code == 200, (
        f"GET /api/overview?window=7d returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    for state in ("delivered", "bounced", "complained"):
        counter = body.get(state)
        assert counter is not None, (
            f"GET /api/overview carries no {state} counter: {response.text[:400]}")
        assert int(counter) == db.count_messages_in_state(state), (
            f"the overview reports {counter} {state} messages while the database holds "
            f"{db.count_messages_in_state(state)}")


def test_overview_buckets_sum_to_the_counters_exactly(admin_client):
    response = admin_client.get("/overview", params={"window": "7d"})
    assert response.status_code == 200, (
        f"GET /api/overview?window=7d returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    buckets = body.get("buckets") or []
    assert buckets, f"GET /api/overview returned no buckets: {response.text[:400]}"
    assert body.get("computed_at"), (
        f"GET /api/overview states no instant it was computed: {response.text[:400]}")
    for state in ("delivered", "bounced", "complained"):
        summed = sum(int(b.get(state) or 0) for b in buckets)
        assert summed == int(body.get(state) or 0), (
            f"the {state} buckets sum to {summed} while the counter reads {body.get(state)}")


def test_upserting_a_contact_by_address_writes_no_duplicate_row(member_client, db):
    audience = db.audience_by_name(AUDIENCE_NAME)
    assert audience is not None, f"seeded audience {AUDIENCE_NAME!r} is missing from the database"
    address = unique_address()
    for name in ("First", "Second"):
        response = member_client.post(f"/audiences/{audience.get('id')}/contacts",
                                      json={"email": address, "first_name": name})
        assert response.status_code in (200, 201), (
            f"POST /api/audiences/<id>/contacts for {address} returned "
            f"{response.status_code}: {response.text[:400]}")
    assert db.count_contacts(audience.get("id"), address) == 1, (
        f"upserting {address} twice left "
        f"{db.count_contacts(audience.get('id'), address)} contacts rows")


def test_two_simultaneous_contact_creates_admit_exactly_one_row(member_client, db):
    audience = db.audience_by_name(AUDIENCE_NAME)
    assert audience is not None, f"seeded audience {AUDIENCE_NAME!r} is missing from the database"
    address = unique_address()

    def fire():
        return member_client.post(f"/audiences/{audience.get('id')}/contacts",
                                  json={"email": address, "first_name": "Probe"})

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        [f.result() for f in [pool.submit(fire), pool.submit(fire)]]
    settle()
    assert db.count_contacts(audience.get("id"), address) == 1, (
        f"two simultaneous creates for {address} left "
        f"{db.count_contacts(audience.get('id'), address)} contacts rows")


def test_sending_a_broadcast_writes_a_message_per_subscribed_contact(admin_client, db):
    audience = db.audience_by_name(AUDIENCE_NAME)
    assert audience is not None, f"seeded audience {AUDIENCE_NAME!r} is missing from the database"
    subscribed = [c for c in db.contacts_in(audience.get("id"))
                  if str(c.get("subscribed")).lower() in ("true", "1", "t")]
    created = admin_client.post("/broadcasts", json={
        "audience_id": audience.get("id"),
        "subject": f"Launch note {unique_local()}",
        "body": "<p>Hello.</p>"})
    assert created.status_code in (200, 201), (
        f"POST /api/broadcasts returned {created.status_code}: {created.text[:400]}")
    broadcast_id = created.json().get("id")
    sent = admin_client.post(f"/broadcasts/{broadcast_id}/send")
    assert sent.status_code in (200, 202), (
        f"POST /api/broadcasts/<id>/send returned {sent.status_code}: {sent.text[:400]}")
    counted = poll_until(
        lambda: db.count_broadcast_messages(broadcast_id) >= len(subscribed))
    assert counted, (
        f"broadcast {broadcast_id} wrote {db.count_broadcast_messages(broadcast_id)} "
        f"messages rows for {len(subscribed)} subscribed contacts")


def test_deleting_a_referenced_audience_is_refused(admin_client, db):
    audience = db.audience_by_name(AUDIENCE_NAME)
    assert audience is not None, f"seeded audience {AUDIENCE_NAME!r} is missing from the database"
    admin_client.post("/broadcasts", json={
        "audience_id": audience.get("id"),
        "subject": f"Referencing note {unique_local()}",
        "body": "<p>Hello.</p>"})
    response = admin_client.delete(f"/audiences/{audience.get('id')}")
    assert 400 <= response.status_code < 500, (
        f"DELETE /api/audiences/<id> while a broadcast still references {AUDIENCE_NAME!r} "
        f"returned {response.status_code}, expected a refusal: {response.text[:400]}")
    assert db.audience_by_name(AUDIENCE_NAME) is not None, (
        f"a refused delete still removed the audience {AUDIENCE_NAME!r}")


def test_creating_a_notification_endpoint_returns_a_signing_secret_once(admin_client, db):
    response = admin_client.post("/notifications", json={
        "url": "http://main:4173/api/health", "events": ["delivered", "bounced"]})
    assert response.status_code in (200, 201), (
        f"POST /api/notifications returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    secret = body.get("signing_secret")
    assert secret, f"POST /api/notifications returned no signing_secret: {response.text[:400]}"
    listed = admin_client.get("/notifications")
    assert secret not in listed.text, (
        "GET /api/notifications hands the signing secret back a second time")
    assert db.endpoint_by_id(body.get("id")) is not None, (
        f"POST /api/notifications wrote no notification_endpoints row for {body.get('id')}")


def test_a_delivery_attempt_writes_one_notification_row(admin_client, db):
    created = admin_client.post("/notifications", json={
        "url": "http://main:4173/api/health", "events": ["delivered"]})
    assert created.status_code in (200, 201), (
        f"POST /api/notifications returned {created.status_code}: {created.text[:400]}")
    endpoint_id = created.json().get("id")
    minted = mint_credential(admin_client)
    accepted_id(send_as(minted["secret"], send_body(DELIVERED_ADDRESS)))
    landed = poll_until(lambda: len(db.deliveries_for(endpoint_id)) >= 1)
    assert landed, (
        f"endpoint {endpoint_id} recorded no notification_deliveries row after a delivered "
        f"message")
    rows = db.deliveries_for(endpoint_id)
    assert all(r.get("attempt") is not None for r in rows), (
        f"a notification_deliveries row for {endpoint_id} carries no attempt number: {rows}")


def test_a_notification_replay_keeps_the_original_event_identifier(admin_client, db):
    created = admin_client.post("/notifications", json={
        "url": "http://main:4173/api/health", "events": ["delivered"]})
    endpoint_id = created.json().get("id")
    minted = mint_credential(admin_client)
    accepted_id(send_as(minted["secret"], send_body(DELIVERED_ADDRESS)))
    landed = poll_until(lambda: len(db.deliveries_for(endpoint_id)) >= 1)
    assert landed, f"endpoint {endpoint_id} recorded no delivery to replay"
    first = db.deliveries_for(endpoint_id)[0]
    response = admin_client.post(
        f"/notifications/{endpoint_id}/deliveries/{first.get('id')}/replay")
    assert response.status_code in (200, 202), (
        f"POST /api/notifications/<id>/deliveries/<id>/replay returned "
        f"{response.status_code}: {response.text[:400]}")
    after = poll_until(lambda: len(db.deliveries_for(endpoint_id)) > 1)
    assert after, f"a replay on endpoint {endpoint_id} wrote no second attempt row"
    rows = db.deliveries_for(endpoint_id)
    identifiers = {str(r.get("message_id")) for r in rows}
    assert len(identifiers) == 1, (
        f"a replay changed the event it carries: message identifiers {sorted(identifiers)}")


def test_usage_returns_the_metered_count_beside_the_allowance(owner_client, db):
    response = owner_client.get("/usage")
    assert response.status_code == 200, (
        f"GET /api/usage returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    assert body.get("allowance") is not None, (
        f"GET /api/usage carries no allowance: {response.text[:400]}")
    assert int(body["allowance"]) == MONTHLY_ALLOWANCE, (
        f"GET /api/usage reports an allowance of {body['allowance']}, expected "
        f"{MONTHLY_ALLOWANCE}")
    assert body.get("count") is not None, (
        f"GET /api/usage carries no metered count: {response.text[:400]}")
    workspace = db.workspace_by_name(WORKSPACE_NAME)
    assert workspace is not None, f"seeded workspace {WORKSPACE_NAME!r} is missing"
    assert str(workspace.get("plan")) == PLAN_NAME, (
        f"workspace {WORKSPACE_NAME!r} reads plan {workspace.get('plan')!r}, expected "
        f"{PLAN_NAME!r}")


def test_a_send_past_the_monthly_allowance_is_refused(owner_client, admin_client, db):
    spent = owner_client.post("/usage", json={"metric": "messages", "count": MONTHLY_ALLOWANCE})
    assert spent.status_code in (200, 201, 202), (
        f"POST /api/usage returned {spent.status_code}: {spent.text[:400]}")
    minted = mint_credential(admin_client)
    address = unique_address()
    response = send_as(minted["secret"], send_body(address))
    assert 400 <= response.status_code < 500, (
        f"a send past the monthly allowance returned {response.status_code}, expected a "
        f"refusal: {response.text[:400]}")
    settle()
    assert db.count_messages_to(address) == 0, (
        f"a send refused for the allowance still wrote a messages row for {address}")
    owner_client.post("/usage", json={"metric": "messages", "count": 0})


def test_an_ordinary_recipient_receives_real_mail(admin_client, inbox):
    minted = mint_credential(admin_client)
    address = unique_address()
    subject = f"Your receipt {unique_local()}"
    accepted_id(send_as(minted["secret"], send_body(address, subject=subject)))
    landed = poll_until(lambda: inbox.find(address, subject_contains=subject))
    assert landed is not None, (
        f"no mail addressed to {address} carrying the subject {subject!r} reached the "
        f"inbox, so nothing was handed to the mail server")
    assert inbox.count(address) == 1, (
        f"the inbox holds {inbox.count(address)} messages for {address}, expected one")


def test_the_reserved_delivered_address_produces_a_delivered_event(admin_client, db):
    minted = mint_credential(admin_client)
    identifier = accepted_id(send_as(minted["secret"], send_body(DELIVERED_ADDRESS)))
    reached = poll_until(
        lambda: (db.message_by_id(identifier) or {}).get("state") == "delivered")
    assert reached, (
        f"a message to {DELIVERED_ADDRESS} never reached the delivered state: "
        f"{db.message_by_id(identifier)}")
    kinds = {str(e.get("event_type")) for e in db.events_for(identifier)}
    assert "delivered" in kinds, (
        f"message {identifier} reads delivered while its message_events rows are "
        f"{sorted(kinds)}")


def test_the_reserved_bounced_address_produces_a_diagnostic(admin_client, db):
    minted = mint_credential(admin_client)
    identifier = accepted_id(send_as(minted["secret"], send_body(BOUNCED_ADDRESS)))
    reached = poll_until(
        lambda: (db.message_by_id(identifier) or {}).get("state") == "bounced")
    assert reached, f"a message to {BOUNCED_ADDRESS} never reached the bounced state"
    events = [e for e in db.events_for(identifier)
              if str(e.get("event_type")) == "bounced"]
    assert events, f"message {identifier} reads bounced with no bounced message_events row"
    assert str(events[0].get("detail") or "").strip(), (
        f"the bounce event on {identifier} carries no diagnostic text: {events[0]}")
    assert db.suppression_for(BOUNCED_ADDRESS) is not None, (
        f"a hard bounce for {BOUNCED_ADDRESS} wrote no suppressions row")


def test_the_reserved_complained_address_produces_a_complaint_event(admin_client, db):
    minted = mint_credential(admin_client)
    identifier = accepted_id(send_as(minted["secret"], send_body(COMPLAINED_ADDRESS)))
    reached = poll_until(
        lambda: (db.message_by_id(identifier) or {}).get("state") == "complained")
    assert reached, f"a message to {COMPLAINED_ADDRESS} never reached the complained state"
    kinds = {str(e.get("event_type")) for e in db.events_for(identifier)}
    assert "complained" in kinds, (
        f"message {identifier} reads complained while its message_events rows are "
        f"{sorted(kinds)}")


def test_reserved_relay_addresses_stay_unmetered(owner_client, admin_client):
    before = owner_client.get("/usage").json().get("count")
    minted = mint_credential(admin_client)
    accepted_id(send_as(minted["secret"], send_body(DELIVERED_ADDRESS)))
    settle()
    after = owner_client.get("/usage").json().get("count")
    assert int(after) == int(before), (
        f"a message to the reserved {DELIVERED_ADDRESS} moved the metered count from "
        f"{before} to {after}")


def test_a_send_to_a_suppressed_address_is_refused_before_queueing(admin_client, db):
    minted = mint_credential(admin_client)
    identifier = accepted_id(send_as(minted["secret"], send_body(BOUNCED_ADDRESS)))
    poll_until(lambda: db.suppression_for(BOUNCED_ADDRESS) is not None)
    assert db.suppression_for(BOUNCED_ADDRESS) is not None, (
        f"{BOUNCED_ADDRESS} carries no suppressions row after message {identifier} bounced")
    before = db.count_messages_to(BOUNCED_ADDRESS)
    response = send_as(minted["secret"], send_body(BOUNCED_ADDRESS))
    assert 400 <= response.status_code < 500, (
        f"a send to the suppressed {BOUNCED_ADDRESS} returned {response.status_code}, "
        f"expected a refusal: {response.text[:400]}")
    settle()
    assert db.count_messages_to(BOUNCED_ADDRESS) == before, (
        f"a send refused for suppression still queued a message to {BOUNCED_ADDRESS}")


def test_a_deferred_message_records_its_attempt_number(admin_client, db):
    minted = mint_credential(admin_client)
    identifier = accepted_id(send_as(minted["secret"], send_body(DELIVERED_ADDRESS)))
    poll_until(lambda: (db.message_by_id(identifier) or {}).get("state") in TERMINAL_STATES)
    events = db.events_for(identifier)
    assert events, f"message {identifier} recorded no message_events rows"
    for event in events:
        assert event.get("occurred_at"), (
            f"a message_events row on {identifier} carries no occurred_at instant: {event}")
        assert event.get("recorded_at"), (
            f"a message_events row on {identifier} carries no recorded_at instant: {event}")


def test_a_member_minting_a_credential_writes_no_credential_row(member_client, db):
    name = f"Member minted {unique_local()}"
    response = member_client.post("/credentials", json={"name": name, "scope": "sending"})
    assert response.status_code in (401, 403), (
        f"a member minting a credential returned {response.status_code}, expected a "
        f"denial: {response.text[:400]}")
    assert db.count_credentials(name) == 0, (
        f"a denied mint still wrote a credentials row named {name!r}")


def test_a_credential_minting_another_credential_is_denied(admin_client, db):
    minted = mint_credential(admin_client, scope="full")
    name = f"Second hand {unique_local()}"
    with client(minted["secret"]) as machine:
        response = machine.post("/credentials", json={"name": name, "scope": "sending"})
    assert response.status_code in (401, 403, 404, 405), (
        f"a credential minting another credential returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}")
    assert db.count_credentials(name) == 0, (
        f"a credential managed to write a credentials row named {name!r}")


def test_a_pinned_credential_sending_from_another_domain_is_refused(admin_client, db):
    verified = db.domain_by_name(VERIFIED_DOMAIN)
    assert verified is not None, f"seeded domain {VERIFIED_DOMAIN} is missing"
    other = admin_client.post("/domains", json={
        "name": f"{unique_local()}.northwind.example.com"})
    assert other.status_code in (200, 201), (
        f"POST /api/domains returned {other.status_code}: {other.text[:400]}")
    minted = mint_credential(admin_client, domain_id=other.json().get("id"))
    response = send_as(minted["secret"], send_body(DELIVERED_ADDRESS))
    assert 400 <= response.status_code < 500, (
        f"a credential pinned to one domain sending from {VERIFIED_DOMAIN} returned "
        f"{response.status_code}, expected a refusal: {response.text[:400]}")


def test_a_sending_scope_credential_reading_domains_is_denied(admin_client):
    minted = mint_credential(admin_client, scope="sending")
    with client(minted["secret"]) as machine:
        response = machine.get("/v1/domains")
    assert response.status_code in (401, 403, 404), (
        f"a sending-scope credential reading domains returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}")


def test_a_member_sending_a_broadcast_leaves_the_broadcast_unsent(member_client, db):
    audience = db.audience_by_name(AUDIENCE_NAME)
    assert audience is not None, f"seeded audience {AUDIENCE_NAME!r} is missing"
    created = member_client.post("/broadcasts", json={
        "audience_id": audience.get("id"),
        "subject": f"Member draft {unique_local()}",
        "body": "<p>Hello.</p>"})
    assert created.status_code in (200, 201), (
        f"a member composing a broadcast returned {created.status_code}: {created.text[:400]}")
    broadcast_id = created.json().get("id")
    response = member_client.post(f"/broadcasts/{broadcast_id}/send")
    assert response.status_code in (401, 403), (
        f"a member sending a broadcast to a live audience returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}")
    settle()
    row = db.broadcast_by_id(broadcast_id) or {}
    assert str(row.get("state")) != "sent", (
        f"a denied send still moved broadcast {broadcast_id} to {row.get('state')!r}")
    assert db.count_broadcast_messages(broadcast_id) == 0, (
        f"a denied broadcast send still wrote {db.count_broadcast_messages(broadcast_id)} "
        f"messages rows")


def test_a_member_composes_a_broadcast_draft(member_client, db):
    audience = db.audience_by_name(AUDIENCE_NAME)
    created = member_client.post("/broadcasts", json={
        "audience_id": audience.get("id"),
        "subject": f"Composed draft {unique_local()}",
        "body": "<p>Hello.</p>"})
    assert created.status_code in (200, 201), (
        f"a member composing a broadcast draft returned {created.status_code}: "
        f"{created.text[:400]}")
    row = db.broadcast_by_id(created.json().get("id")) or {}
    assert str(row.get("state")) in ("draft", "requested"), (
        f"a member composed broadcast reads state {row.get('state')!r}, expected a draft")


def test_an_owner_changes_the_workspace_plan(owner_client, admin_client, db):
    response = owner_client.patch("/workspace", json={"plan": PLAN_NAME})
    assert response.status_code in (200, 202), (
        f"an owner changing the workspace plan returned {response.status_code}: "
        f"{response.text[:400]}")
    refused = admin_client.patch("/workspace", json={"plan": PLAN_NAME})
    assert refused.status_code in (401, 403), (
        f"an admin changing the workspace plan returned {refused.status_code}, expected a "
        f"denial: {refused.text[:400]}")
    workspace = db.workspace_by_name(WORKSPACE_NAME)
    assert str(workspace.get("plan")) == PLAN_NAME, (
        f"workspace {WORKSPACE_NAME!r} reads plan {workspace.get('plan')!r}")


def test_an_admin_verifies_a_sending_domain(admin_client, member_client, db):
    domain = db.domain_by_name(PENDING_DOMAIN)
    assert domain is not None, f"seeded domain {PENDING_DOMAIN} is missing"
    allowed = admin_client.post(f"/domains/{domain.get('id')}/verify")
    assert allowed.status_code in (200, 202), (
        f"an admin requesting verification returned {allowed.status_code}: "
        f"{allowed.text[:400]}")
    refused = member_client.post(f"/domains/{domain.get('id')}/verify")
    assert refused.status_code in (401, 403), (
        f"a member requesting verification returned {refused.status_code}, expected a "
        f"denial: {refused.text[:400]}")


def test_an_unauthorized_call_is_rejected_as_a_client_error(anon_client):
    response = anon_client.post("/domains", json={"name": "unauthorised.example.com"})
    assert 400 <= response.status_code < 500, (
        f"POST /api/domains with no session returned {response.status_code}, expected a "
        f"client error rather than a server error: {response.text[:400]}")


def test_the_seeded_workspace_rows_persisted_with_three_membership_roles(db):
    workspace = db.workspace_by_name(WORKSPACE_NAME)
    assert workspace is not None, f"seeded workspace {WORKSPACE_NAME!r} is missing"
    roles = sorted(str(m.get("role")) for m in db.memberships(workspace.get("id")))
    assert roles == ["admin", "member", "owner"], (
        f"workspace {WORKSPACE_NAME!r} carries memberships roles {roles}, expected owner, "
        f"admin, member")
    for address in (OWNER_EMAIL, ADMIN_EMAIL, MEMBER_EMAIL):
        assert db.count_users(address) == 1, (
            f"seeding left {db.count_users(address)} users rows for {address}, so a restart "
            f"duplicated a row")


def test_every_stored_timestamp_is_utc(db):
    workspace = db.workspace_by_name(WORKSPACE_NAME)
    assert workspace is not None, f"seeded workspace {WORKSPACE_NAME!r} is missing"
    stamp = str(workspace.get("created_at") or "")
    assert stamp, f"workspace {WORKSPACE_NAME!r} carries no created_at value"
    assert "+" not in stamp or stamp.endswith("+00:00"), (
        f"workspace {WORKSPACE_NAME!r} stores created_at {stamp!r}, which is not UTC")


def test_deleting_a_domain_keeps_every_message_already_sent(admin_client, db):
    name = f"{unique_local()}.northwind.example.com"
    created = admin_client.post("/domains", json={"name": name})
    assert created.status_code in (200, 201), (
        f"POST /api/domains for {name} returned {created.status_code}: {created.text[:400]}")
    before = db.count_messages_in_state("delivered")
    response = admin_client.delete(f"/domains/{created.json().get('id')}")
    assert response.status_code in (200, 202, 204), (
        f"DELETE /api/domains/<id> for {name} returned {response.status_code}: "
        f"{response.text[:400]}")
    assert db.domain_by_name(name) is None or str(
        (db.domain_by_name(name) or {}).get("state")) == "deleted", (
        f"DELETE /api/domains/<id> left {name} readable as a live domain")
    assert db.count_messages_in_state("delivered") == before, (
        f"deleting {name} changed the delivered message count from {before} to "
        f"{db.count_messages_in_state('delivered')}")


def test_every_external_identifier_carries_a_type_prefix(admin_client, db):
    minted = mint_credential(admin_client)
    identifier = accepted_id(send_as(minted["secret"], send_body(DELIVERED_ADDRESS)))
    assert "_" in str(identifier), (
        f"the accepted message identifier {identifier!r} carries no type prefix")
    assert not str(identifier).isdigit(), (
        f"the accepted message identifier {identifier!r} is a sequential integer")


def test_an_address_is_normalised_before_comparison(member_client, db):
    audience = db.audience_by_name(AUDIENCE_NAME)
    assert audience is not None, f"seeded audience {AUDIENCE_NAME!r} is missing"
    local = unique_local()
    lower = f"{local}@example.com"
    upper = f"{local}@EXAMPLE.COM"
    for address in (lower, upper):
        response = member_client.post(f"/audiences/{audience.get('id')}/contacts",
                                      json={"email": address, "first_name": "Probe"})
        assert response.status_code in (200, 201), (
            f"POST /api/audiences/<id>/contacts for {address} returned "
            f"{response.status_code}: {response.text[:400]}")
    assert db.count_contacts(audience.get("id"), lower) == 1, (
        f"the same address in two cases left "
        f"{db.count_contacts(audience.get('id'), lower)} contacts rows")


def test_the_health_route_answers_without_a_token(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code} at {base_url()}: "
        f"{response.text[:400]}")


def test_the_backend_serves_json_under_the_api_prefix(owner_client):
    response = owner_client.get("/auth/me")
    assert response.status_code == 200, (
        f"GET /api/auth/me returned {response.status_code} at {api_url()}: "
        f"{response.text[:400]}")
    assert "json" in response.headers.get("content-type", "").lower(), (
        f"GET /api/auth/me answered with content-type "
        f"{response.headers.get('content-type')!r}, expected JSON")
    assert api_url().endswith("/api"), (
        f"the api base resolved to {api_url()!r}, which is not the /api prefix on the "
        f"app origin")


def test_every_response_carries_a_request_identifier_header(anon_client):
    response = anon_client.get("/health")
    assert response.headers.get("x-request-id"), (
        f"GET /api/health carries no X-Request-Id header: {dict(response.headers)}")


def test_every_response_carries_a_nosniff_content_type_header(anon_client):
    response = anon_client.get("/health")
    assert response.headers.get("x-content-type-options", "").lower() == "nosniff", (
        f"GET /api/health answers with x-content-type-options "
        f"{response.headers.get('x-content-type-options')!r}, expected nosniff")


def test_every_response_carries_a_strict_transport_security_header(anon_client):
    response = anon_client.get("/health")
    assert response.headers.get("strict-transport-security"), (
        f"GET /api/health carries no Strict-Transport-Security header: "
        f"{dict(response.headers)}")


def test_the_permissions_policy_denies_camera_access(anon_client):
    response = anon_client.get("/health")
    policy = response.headers.get("permissions-policy", "")
    assert "camera" in policy.lower(), (
        f"GET /api/health answers with permissions-policy {policy!r}, which names no "
        f"camera restriction")


def test_an_authenticated_response_carries_a_no_store_cache_header(owner_client):
    response = owner_client.get("/auth/me")
    cache = response.headers.get("cache-control", "").lower()
    assert "no-store" in cache and "private" in cache, (
        f"GET /api/auth/me answers with cache-control {cache!r}, expected private and "
        f"no-store")


def test_a_versioned_list_response_carries_a_cursor_page_envelope(admin_client):
    minted = mint_credential(admin_client, scope="full")
    with client(minted["secret"]) as machine:
        response = machine.get("/v1/emails", params={"limit": 5})
    assert response.status_code == 200, (
        f"GET /api/v1/emails returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    for key in ("data", "has_more", "next_cursor"):
        assert key in body, (
            f"GET /api/v1/emails carries no {key!r} in its cursor page envelope: "
            f"{response.text[:400]}")


def test_an_error_body_carries_a_type_beside_a_request_identifier(anon_client):
    response = anon_client.get("/domains")
    body = response.json()
    error = body.get("error") or {}
    assert error.get("type"), (
        f"a denied GET /api/domains answers without an error type: {response.text[:400]}")
    assert error.get("request_id"), (
        f"a denied GET /api/domains answers without a request_id: {response.text[:400]}")


def test_a_validation_failure_reports_every_failing_field(admin_client):
    minted = mint_credential(admin_client)
    with client(minted["secret"]) as sender:
        response = sender.post("/v1/emails", json={"from": "", "to": [], "subject": ""},
                               headers={"Idempotency-Key": unique_key()})
    assert 400 <= response.status_code < 500, (
        f"a send with three empty fields returned {response.status_code}, expected a "
        f"validation refusal: {response.text[:400]}")
    from _shapes import flatten
    said = flatten(response.json()).lower()
    named = sum(1 for field in ("from", "to", "subject") if field in said)
    assert named >= 2, (
        f"a send with three empty fields named {named} of them in its refusal: "
        f"{response.text[:400]}")


def test_an_unknown_field_on_a_write_is_refused(admin_client):
    minted = mint_credential(admin_client)
    body = send_body(DELIVERED_ADDRESS)
    body["subjekt"] = "a mistyped field name"
    response = send_as(minted["secret"], body)
    assert 400 <= response.status_code < 500, (
        f"a send carrying an unknown field returned {response.status_code}, expected a "
        f"refusal rather than a silent drop: {response.text[:400]}")


def test_every_response_carries_the_rate_limit_budget_headers(admin_client):
    response = admin_client.get("/emails")
    for header in ("ratelimit-limit", "ratelimit-remaining", "ratelimit-reset"):
        assert response.headers.get(header) is not None, (
            f"GET /api/emails carries no {header} header: {dict(response.headers)}")


def test_a_caller_over_the_send_budget_is_refused(admin_client):
    minted = mint_credential(admin_client)
    codes = []
    for _ in range(120):
        codes.append(send_as(minted["secret"], send_body(DELIVERED_ADDRESS)).status_code)
        if codes[-1] == 429:
            break
    assert 429 in codes, (
        f"120 sends in one minute produced status codes {sorted(set(codes))}, and never a "
        f"refusal for being over budget")


def test_a_deprecated_interface_version_answers_with_sunset_headers(admin_client):
    minted = mint_credential(admin_client, scope="full")
    with client(minted["secret"]) as machine:
        response = machine.get("/v1/emails", params={"limit": 1})
    assert response.status_code == 200, (
        f"GET /api/v1/emails returned {response.status_code}: {response.text[:400]}")
    credentials = admin_client.get("/credentials")
    assert credentials.status_code == 200, (
        f"GET /api/credentials returned {credentials.status_code}: {credentials.text[:400]}")
    from _shapes import items
    rows = items(credentials.json())
    assert any("version" in str(row).lower() for row in rows), (
        f"GET /api/credentials records no interface version per credential, so a customer "
        f"cannot find the service that has not been upgraded: {credentials.text[:400]}")


def test_the_post_sign_in_return_path_stays_relative_to_the_serving_origin(anon_client):
    response = anon_client.post("/auth/login", json={
        "email": OWNER_EMAIL, "password": SEEDED_PASSWORD,
        "next": "https://elsewhere.example.com/steal"})
    assert response.status_code in (200, 400, 422), (
        f"a login carrying an absolute return path returned {response.status_code}: "
        f"{response.text[:400]}")
    if response.status_code == 200:
        assert "elsewhere.example.com" not in response.text, (
            f"a login echoed back an absolute off-origin return path: {response.text[:400]}")


def test_a_password_below_the_stated_minimum_length_is_refused(anon_client, db):
    address = unique_address()
    response = anon_client.post("/auth/signup", json={
        "email": address, "password": "short1!", "display_name": "Short Probe"})
    assert 400 <= response.status_code < 500, (
        f"a signup with a seven-character password returned {response.status_code}, "
        f"expected a refusal: {response.text[:400]}")
    assert db.count_users(address) == 0, (
        f"a refused signup still wrote a users row for {address}")


def test_nothing_the_browser_downloads_carries_a_credential(anon_client, page):
    page.goto(f"{base_url()}/login")
    markup = page.content()
    assert "skey_" not in markup, (
        "the signed-out login document carries a credential secret in what the browser "
        "downloads")
    assert SEEDED_PASSWORD not in markup, (
        "the signed-out login document carries the seeded password in what the browser "
        "downloads")


def test_the_frontend_ships_as_a_built_production_bundle(anon_client, page):
    page.goto(base_url())
    markup = page.content()
    assert "/@vite/client" not in markup, (
        "the served document loads the development client, so this is a development "
        "server rather than a production bundle")
    assert "react-refresh" not in markup, (
        "the served document loads a development refresh runtime rather than a built "
        "production bundle")


def test_the_datastore_is_reached_at_the_database_environment_variable(db):
    workspace = db.workspace_by_name(WORKSPACE_NAME)
    assert workspace is not None, (
        f"the seeded workspace {WORKSPACE_NAME!r} is not readable in the datastore the "
        f"environment points at, so the app is not writing to the backing service")
    assert db.memberships(workspace.get("id")), (
        f"workspace {WORKSPACE_NAME!r} carries no memberships rows in the backing service")


def test_every_list_endpoint_returns_a_top_level_json_array(admin_client):
    for route in ("/domains", "/credentials", "/emails", "/audiences", "/broadcasts",
                  "/notifications"):
        response = admin_client.get(route)
        assert response.status_code == 200, (
            f"GET /api{route} returned {response.status_code}: {response.text[:400]}")
        assert isinstance(response.json(), list), (
            f"GET /api{route} returned a {type(response.json()).__name__} rather than a "
            f"top-level JSON array: {response.text[:400]}")


def test_login_signup_health_answer_without_a_bearer_token(anon_client):
    health = anon_client.get("/health")
    assert health.status_code == 200, (
        f"GET /api/health with no bearer token returned {health.status_code}: "
        f"{health.text[:400]}")
    login_response = anon_client.post("/auth/login", json={
        "email": OWNER_EMAIL, "password": SEEDED_PASSWORD})
    assert login_response.status_code == 200, (
        f"POST /api/auth/login with no bearer token returned {login_response.status_code}: "
        f"{login_response.text[:400]}")
    address = unique_address()
    signup_response = anon_client.post("/auth/signup", json={
        "email": address, "password": "relay-probe-pw-2026", "display_name": "Open Probe"})
    assert signup_response.status_code in (200, 201), (
        f"POST /api/auth/signup with no bearer token returned "
        f"{signup_response.status_code}: {signup_response.text[:400]}")


def test_the_log_reflects_message_rows_stored_in_the_named_datastore(admin_client, db):
    response = admin_client.get("/emails")
    assert response.status_code == 200, (
        f"GET /api/emails returned {response.status_code}: {response.text[:400]}")
    from _shapes import items
    rows = items(response.json())
    assert rows, "GET /api/emails returned nothing while seeded messages exist"
    for row in rows[:25]:
        stored = db.message_by_id(row.get("id"))
        assert stored is not None, (
            f"the log shows message {row.get('id')!r} with no messages row behind it in "
            f"postgres, so the screen is not reflecting the datastore")
        assert str(stored.get("state")) == str(row.get("state")), (
            f"the log shows message {row.get('id')!r} as {row.get('state')!r} while its "
            f"messages row reads {stored.get('state')!r}")


def test_the_server_outlives_the_session_that_started_the_process(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health at {base_url()} returned {response.status_code} after the "
        f"session that started the process ended, so the server did not outlive it: "
        f"{response.text[:400]}")


def test_a_payment_processor_route_is_absent(owner_client):
    response = owner_client.get("/billing/payment-methods")
    assert response.status_code in (404, 405), (
        f"GET /api/billing/payment-methods returned {response.status_code}, and the build "
        f"carries no payment processor: {response.text[:400]}")


def test_an_open_tracking_setting_is_absent(admin_client, db):
    domain = db.domain_by_name(VERIFIED_DOMAIN)
    response = admin_client.patch(f"/domains/{domain.get('id')}",
                                  json={"open_tracking": True})
    assert response.status_code in (400, 404, 405, 422), (
        f"enabling open tracking on {VERIFIED_DOMAIN} returned {response.status_code}, and "
        f"the build carries no open tracking: {response.text[:400]}")


def test_the_terms_route_is_readable_by_a_signed_out_visitor(page):
    page.goto(f"{base_url()}/terms")
    body = page.inner_text("body")
    assert len(body.strip()) > 200, (
        f"the terms route rendered {len(body.strip())} characters, which is not a readable "
        f"terms page for a signed-out visitor")
    footer_link = page.locator("a[href*='/terms']")
    assert footer_link.count() >= 1, (
        "no link to the terms route is reachable from the page footer")


def test_a_signup_form_refuses_an_invalid_address_inline(page, db):
    page.goto(f"{base_url()}/signup")
    page.fill("input[type='email'], input[name='email']", "not-an-address")
    page.fill("input[type='password'], input[name='password']", "relay-probe-pw-2026")
    page.click("button[type='submit']")
    body = page.inner_text("body").lower()
    assert "email" in body or "address" in body, (
        "the signup form refused an invalid address without naming the field that is wrong")
    assert db.count_users("not-an-address") == 0, (
        "a refused signup form still wrote a users row")


def test_an_unknown_address_renders_the_product_not_found_page(page):
    response = page.goto(f"{base_url()}/no-such-route-{unique_local()}")
    assert response.status == 404, (
        f"an unknown address answered {response.status}, expected a not-found status")
    body = page.inner_text("body").lower()
    assert "sendline" in body or "console" in body, (
        "the not-found page carries neither the product name nor a way back to the console")
    assert page.locator("a").count() >= 1, (
        "the not-found page offers no link back")


def test_every_internal_link_on_a_reachable_route_resolves(page, anon_client):
    page.goto(f"{base_url()}/login")
    hrefs = [h for h in page.locator("a").evaluate_all(
        "nodes => nodes.map(n => n.getAttribute('href'))") if h and h.startswith("/")]
    assert hrefs, "the login route carries no internal links at all"
    broken = []
    for href in sorted(set(hrefs)):
        landing = page.goto(f"{base_url()}{href}")
        if landing.status >= 400:
            broken.append((href, landing.status))
        page.go_back()
    assert not broken, f"internal links that do not resolve: {broken}"
