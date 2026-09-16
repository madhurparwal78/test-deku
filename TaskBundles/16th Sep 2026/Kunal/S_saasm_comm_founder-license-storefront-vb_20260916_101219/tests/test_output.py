"""Graded observations for deku/founder-license-storefront-vb.

One module for every section of the brief and for each declared slot. The
assertions read HTTP responses, the PostgreSQL ledger, the Mailpit inbox, the
Kill Bill tenant and, where the brief pins a rendered surface, a real Chromium
page. Nothing here reads the application's source or assumes its framework.
"""

from __future__ import annotations

import os
import re
import threading
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse

from playwright.sync_api import expect

from appclient import app_url
from conftest import (
    ARTICLE_ROUTES, CHECKOUT_NOTICE, CLOSED_NOTICE, COHORT_CAP, CONTENT_ROUTES,
    CURRENCY, DATA_REQUEST_MESSAGE, DOWNLOAD_CONTROL, EMAIL_RE, HEADING_CONFIRMED,
    HEADING_EXPIRED, HEADING_INVALID, HEADING_UNKNOWN, HEADING_USED_UP,
    HELP_QUESTIONS, HOME_EYEBROWS, HOME_HEADINGS, HOURLY_EMAILS, LICENCE_NOTICE,
    LINE_FIRST, LINE_LATER, LINK_DAYS, MAX_OPENS, OPERATOR_EMAIL, OPERATOR_NAME,
    PALETTE_BLUEPRINTS, PALETTE_DESTINATION_ROUTES, PASSWORD, PLACE_PREFIX,
    REGISTRANT2_EMAIL, REGISTRANT2_NAME, REGISTRANT3_EMAIL, REGISTRANT3_NAME,
    REGISTRANT_EMAIL, REGISTRANT_NAME, RELEASE_NOTE_SECTIONS, RESEND_MESSAGE,
    REVOKED_NOTICE, SEED_EXPIRED, SEED_RELEASES, SEED_REVOKED, SEED_USEDUP,
    STATUS_NO_SESSION, SUBJECT, SUCCESS_MESSAGE, SUPPORT_EMAIL,
    TIER1_PRICE, TIER2_PRICE, TIER_SIZE, TOKEN_RE, TYPE_SIZES_BELOW_DISPLAY,
    USE_CASE_PAGES, allocation, api, backend_secrets, canonical_of,
    composite_contrast_script,
    cookie_seconds, expected_tier, founder_key, headings, heading_pairs, hrefs,
    input_tags, internal_path, ld_types, open_link, page_html,
    placeholder_contrast_script, probe_email, reading_minutes, register,
    register_many, registration_body, release, release_payload, releases, resend,
    section_after, set_cookie_headers, settle, site, status_page_session,
    text_of, wait_for,
)


def test_health_endpoint_reports_ok_status():
    """The readiness route answers 200 with status ok on the published origin."""
    with api() as client:
        response = client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:300]}")
    body = response.json()
    assert body.get("status") == "ok", (
        f"GET /api/health must answer status ok, got {str(body)[:300]}")
    published = urlparse(app_url())
    assert published.scheme in ("http", "https") and published.netloc, (
        f"the app is graded at {app_url()!r}, which names no reachable origin")


def test_seeded_rows_are_stored_once(db):
    """The eight tables exist and each seeded record is stored exactly once."""
    columns = {
        "operators": {"id", "email", "display_name", "password_hash", "created_at"},
        "registrations": {"id", "email", "name", "platform_version", "role",
                          "primary_use", "consent_at", "challenge_status",
                          "created_at", "updated_at"},
        "founder_slots": {"position", "registration_id", "tier", "price_minor",
                          "currency", "killbill_external_key", "claimed_at"},
        "access_links": {"id", "registration_id", "token_hash", "status", "opens",
                         "max_opens", "created_at", "expires_at"},
        "access_clicks": {"id", "access_link_id", "clicked_at"},
        "releases": {"version", "build", "published_at", "min_os", "size_bytes",
                     "sha256", "ed_signature", "download_url", "summary", "notes",
                     "status"},
        "download_events": {"id", "release_version", "access_link_id", "created_at"},
        "data_requests": {"id", "email", "kind", "status", "created_at"},
    }
    for table, wanted in columns.items():
        assert db.table_exists(table), (
            f"the database holds no {table!r} table, so the data model of the brief "
            f"is not stored where the brief puts it")
        missing = wanted - db.columns(table)
        assert not missing, (
            f"table {table!r} is missing the column(s) {sorted(missing)} the brief names")

    operators = db.q("SELECT * FROM operators WHERE email = %s", (OPERATOR_EMAIL,))
    assert len(operators) == 1, (
        f"{len(operators)} operators rows hold {OPERATOR_EMAIL}, expected exactly one "
        f"(seeding must be idempotent)")
    assert operators[0]["display_name"] == OPERATOR_NAME, (
        f"the seeded operator's display_name is {operators[0]['display_name']!r}, "
        f"expected {OPERATOR_NAME!r}")
    stored_password = str(operators[0]["password_hash"] or "")
    assert stored_password and PASSWORD not in stored_password, (
        f"the operator's password_hash is {stored_password[:40]!r}, which carries the "
        f"password in the clear rather than a hash of it")

    seeded = ((REGISTRANT_EMAIL, REGISTRANT_NAME), (REGISTRANT2_EMAIL, REGISTRANT2_NAME),
              (REGISTRANT3_EMAIL, REGISTRANT3_NAME))
    for address, name in seeded:
        assert db.registrations_like(address) == 1, (
            f"{db.registrations_like(address)} registrations rows hold {address}, "
            f"expected exactly one after an idempotent seed")
        row = db.registration(address)
        assert row["name"] == name, (
            f"the seeded registration for {address} is named {row['name']!r}, "
            f"expected {name!r}")
        assert row["consent_at"] is not None, (
            f"the seeded registration for {address} records no consent_at")
        assert str(row["challenge_status"]) == "not_run", (
            f"the seeded registration for {address} records challenge_status "
            f"{row['challenge_status']!r}, expected not_run")

    slot = db.slot_for(REGISTRANT_EMAIL)
    assert slot is not None and int(slot["position"]) == 1, (
        f"{REGISTRANT_EMAIL} must hold founder place 1, found {slot}")
    assert int(slot["tier"]) == 1 and int(slot["price_minor"]) == TIER1_PRICE, (
        f"seeded place 1 stores tier {slot['tier']} at {slot['price_minor']}, "
        f"expected tier 1 at {TIER1_PRICE}")
    assert isinstance(slot["price_minor"], int), (
        f"price_minor is stored as {type(slot['price_minor']).__name__}, expected "
        f"integer minor units")
    assert str(slot["currency"]) == CURRENCY, (
        f"seeded place 1 stores currency {slot['currency']!r}, expected {CURRENCY!r}")
    assert str(slot["killbill_external_key"]) == founder_key(1), (
        f"seeded place 1 stores key {slot['killbill_external_key']!r}, expected "
        f"{founder_key(1)!r}")

    link_states = {str(r["status"]) for r in db.q("SELECT DISTINCT status FROM access_links")}
    assert link_states <= {"active", "revoked", "superseded"}, (
        f"access_links carries the status value(s) {sorted(link_states)}, outside the "
        f"three the brief names")
    challenge_states = {str(r["challenge_status"]) for r in
                        db.q("SELECT DISTINCT challenge_status FROM registrations")}
    assert challenge_states <= {"not_run", "passed", "failed"}, (
        f"registrations carries the challenge_status value(s) {sorted(challenge_states)}, "
        f"outside the three the brief names")
    revoked = [link for link in db.links_for(REGISTRANT_EMAIL)
               if str(link["status"]) == "revoked"]
    assert revoked, (
        f"{REGISTRANT_EMAIL} has no revoked seeded link, so the seeded revoked token "
        f"is missing from access_links")
    for link in db.links_for(REGISTRANT3_EMAIL):
        assert int(link["max_opens"]) == MAX_OPENS, (
            f"a seeded link of {REGISTRANT3_EMAIL} stores max_opens "
            f"{link['max_opens']}, expected {MAX_OPENS}")

    positions = [int(row["position"]) for row in db.slots()]
    assert positions == sorted(positions), (
        f"founder_slots positions are not contiguous from 1: {positions[:8]}")
    assert all(1 <= p <= COHORT_CAP for p in positions), (
        f"founder_slots stores a position outside 1 to {COHORT_CAP}: "
        f"{[p for p in positions if not 1 <= p <= COHORT_CAP][:5]}")


def test_seeded_registry_lists_releases_highest_build_first(db):
    """The release API projects the seeded registry, newest build first."""
    rows = releases()
    assert len(rows) >= len(SEED_RELEASES), (
        f"GET /api/releases returned {len(rows)} releases, fewer than the "
        f"{len(SEED_RELEASES)} the seed pins")
    builds = [int(row["build"]) for row in rows]
    assert builds == sorted(builds, reverse=True), (
        f"GET /api/releases returned builds {builds[:8]}, which are not highest first")
    assert len(set(builds)) == len(builds), (
        f"GET /api/releases repeats a build: {builds[:8]}")

    fields = {"version", "build", "published_at", "min_os", "size_bytes", "sha256",
              "ed_signature", "download_url", "summary", "status", "download_count"}
    for row in rows:
        missing = fields - set(row)
        assert not missing, (
            f"the release {row.get('version')!r} is missing the field(s) "
            f"{sorted(missing)} the API shapes table names")
        assert str(row["status"]) in ("published", "revoked"), (
            f"release {row['version']!r} carries status {row['status']!r}, outside "
            f"published and revoked")

    by_version = {str(row["version"]): row for row in rows}
    for seed in SEED_RELEASES:
        row = by_version.get(seed["version"])
        assert row is not None, (
            f"the seeded release {seed['version']} is absent from GET /api/releases")
        for key in ("build", "min_os", "size_bytes", "sha256", "ed_signature",
                    "download_url", "summary", "status"):
            assert str(row[key]) == str(seed[key]), (
                f"release {seed['version']} stores {key} {row[key]!r}, expected "
                f"{seed[key]!r} from the seed")
        assert str(row["published_at"]).startswith(seed["published_at"]), (
            f"release {seed['version']} is published_at {row['published_at']!r}, "
            f"expected the seeded date {seed['published_at']}")
        assert re.fullmatch(r"[0-9a-f]{64}", str(row["sha256"])), (
            f"release {seed['version']} stores sha256 {row['sha256']!r}, which is not "
            f"64 lowercase hexadecimal characters")

    stored = db.q("SELECT version, build, status FROM releases")
    assert len(stored) == len(rows), (
        f"the releases table holds {len(stored)} rows while GET /api/releases returns "
        f"{len(rows)}, so the route is not a projection of the registry")

    with api() as client:
        one = client.get("/releases/0.2.3")
    assert one.status_code == 200, (
        f"GET /api/releases/0.2.3 returned {one.status_code}: {one.text[:300]}")
    detail = one.json()
    assert str(detail.get("version")) == "0.2.3", (
        f"GET /api/releases/0.2.3 answered for version {detail.get('version')!r}")
    notes = str(detail.get("notes") or "")
    assert notes.strip(), (
        f"GET /api/releases/0.2.3 carries no notes: {str(detail)[:300]}")
    assert "Obelisk" in notes, (
        f"the 0.2.3 notes never name the import source Obelisk: {notes[:300]}")
    with api() as client:
        unknown = client.get("/releases/99.99.99")
    assert unknown.status_code == 404, (
        f"GET /api/releases/99.99.99 returned {unknown.status_code}, expected not "
        f"found for a version the registry does not hold: {unknown.text[:200]}")


def test_registration_row_is_stored_with_a_normalised_email(db):
    """A registration is stored trimmed, lowercased and with a coerced version."""
    local = f"Norm-{os.urandom(5).hex()}"
    submitted = f"  {local}@Example.COM "
    normalised = f"{local.lower()}@example.com"
    response = register(submitted, name="Norm Probe", role="Engineer",
                        primary_use="Client briefs", platform_version="26.2")
    assert 200 <= response.status_code < 300, (
        f"POST /api/beta/register for a valid address returned "
        f"{response.status_code}: {response.text[:300]}")
    body = response.json()
    assert body.get("status") == "sent", (
        f"a successful registration answered status {body.get('status')!r}, "
        f"expected sent: {str(body)[:300]}")
    assert body.get("message") == SUCCESS_MESSAGE, (
        f"a successful registration answered message {body.get('message')!r}, "
        f"expected {SUCCESS_MESSAGE!r}")
    assert body.get("email") == normalised, (
        f"the response echoed {body.get('email')!r} for the submitted "
        f"{submitted!r}, expected the normalised {normalised!r}")

    row = db.registration(normalised)
    assert row is not None, (
        f"no registrations row holds {normalised} after a successful registration")
    assert row["name"] == "Norm Probe" and row["role"] == "Engineer", (
        f"the stored row carries name {row['name']!r} and role {row['role']!r}, "
        f"expected the submitted values")
    assert row["primary_use"] == "Client briefs", (
        f"the stored row carries primary_use {row['primary_use']!r}")
    assert str(row["platform_version"]) == "26.2", (
        f"a supported platform_version was stored as {row['platform_version']!r}, "
        f"expected 26.2")
    assert row["consent_at"] is not None, (
        f"the stored row for {normalised} records no consent_at")
    age = db.seconds_since(normalised)
    assert -120 <= age <= 3600, (
        f"the stored created_at for {normalised} is {age:.0f}s from the database's own "
        f"clock, so the timestamp is not recorded in UTC as the brief requires")

    again = register(f"{local.upper()}@EXAMPLE.COM")
    assert 200 <= again.status_code < 300, (
        f"re-registering the same address in another letter case returned "
        f"{again.status_code}: {again.text[:300]}")
    assert db.registrations_like(normalised) == 1, (
        f"{db.registrations_like(normalised)} rows hold {normalised} after two "
        f"submissions differing only in letter case, expected one")

    coerced = probe_email("version")
    assert 200 <= register(coerced, platform_version="25.4").status_code < 300, (
        "a registration carrying an unsupported platform_version must still succeed")
    stored = db.registration(coerced)
    assert stored is not None and str(stored["platform_version"]) == "", (
        f"platform_version 25.4 was stored as {stored and stored['platform_version']!r}, "
        f"expected an empty value rather than a rejection")

    edge = probe_email("limits")
    accepted = register(edge, name="n" * 120, role="r" * 120, primary_use="u" * 240)
    assert 200 <= accepted.status_code < 300, (
        f"a registration at the exact length limits returned {accepted.status_code}: "
        f"{accepted.text[:300]}")
    assert db.registration(edge) is not None, (
        f"no row was stored for {edge} although the lengths are inside the limits")


def test_repeat_registration_returns_an_identical_response(db):
    """A repeat registration answers the same keys and wording, with one place."""
    address = probe_email("repeat")
    first = register(address, name="Repeat Probe")
    second = register(address, name="Repeat Probe")
    for response in (first, second):
        assert 200 <= response.status_code < 300, (
            f"POST /api/beta/register returned {response.status_code}: "
            f"{response.text[:300]}")
    assert first.json() == second.json(), (
        f"a first registration answered {first.json()} and a repeat answered "
        f"{second.json()}; the brief pins the same keys with the same wording")
    assert first.json().get("message") == SUCCESS_MESSAGE, (
        f"the registration message is {first.json().get('message')!r}, expected "
        f"{SUCCESS_MESSAGE!r}")
    assert db.registrations_like(address) == 1, (
        f"{db.registrations_like(address)} registrations rows hold {address} after two "
        f"submissions, expected one")
    held = db.q(
        "SELECT count(*) AS n FROM founder_slots s JOIN registrations r "
        "ON r.id = s.registration_id WHERE r.email = %s", (address,))[0]["n"]
    assert held <= 1, (
        f"{address} holds {held} founder places after a repeat registration, and an "
        f"address holds at most one")


def test_invalid_registration_is_refused_and_stores_nothing(db, mail):
    """Each invalid registration is refused with a field error and writes nothing."""
    marker = f"Invalid {os.urandom(4).hex()}"
    long_local = "a" * 243
    cases = (
        ("email", registration_body(None, name=marker)),
        ("email", registration_body("not-an-address", name=marker)),
        ("email", registration_body(f"{long_local}@example.com", name=marker)),
        ("consent", registration_body(probe_email("noconsent"), name=marker,
                                      consent=False)),
        ("name", registration_body(probe_email("longname"), name="n" * 121)),
        ("role", registration_body(probe_email("longrole"), name=marker,
                                   role="r" * 121)),
        ("primary_use", registration_body(probe_email("longuse"), name=marker,
                                          primary_use="u" * 241)),
    )
    addresses = []
    for field, body in cases:
        with api() as client:
            response = client.post("/beta/register", json=body)
        assert 400 <= response.status_code < 500, (
            f"POST /api/beta/register with an invalid {field} returned "
            f"{response.status_code}, expected a client error: {response.text[:300]}")
        payload = response.json()
        errors = payload.get("errors")
        assert isinstance(errors, dict), (
            f"a rejected registration answered {str(payload)[:300]}, expected an "
            f"errors object keyed by field name")
        assert field in errors, (
            f"a registration invalid on {field!r} answered errors "
            f"{sorted(errors)}, which never names the field")
        submitted = body.get("email")
        if submitted and "@" in submitted:
            addresses.append(submitted)

    assert db.registrations_named(marker) == 0, (
        f"{db.registrations_named(marker)} registrations rows carry the rejected "
        f"marker name {marker!r}; a rejected registration stores nothing")
    assert db.registrations_named("n" * 121) == 0, (
        "a registration with an over-long name was stored anyway")
    for address in addresses:
        assert db.registrations_like(address) == 0, (
            f"a row was stored for the rejected address {address}")
    settle()
    for address in addresses:
        assert mail.count(address) == 0, (
            f"{mail.count(address)} messages reached the rejected address {address}; a "
            f"rejected registration sends nothing")


def test_trap_field_submission_is_discarded_silently(db, mail):
    """A filled trap field answers the ordinary success and writes nothing."""
    trapped = probe_email("trap")
    control = probe_email("control")
    response = register(trapped, name="Trap Probe",
                        company_website="https://spam.example.org/offer")
    baseline = register(control, name="Control Probe")
    assert 200 <= response.status_code < 300, (
        f"a submission carrying the trap field returned {response.status_code}: "
        f"{response.text[:300]}")
    body = response.json()
    assert body.get("status") == "sent" and body.get("message") == SUCCESS_MESSAGE, (
        f"a trapped submission answered {str(body)[:300]}, expected the ordinary "
        f"success response")
    assert set(body) == set(baseline.json()), (
        f"a trapped submission answered the keys {sorted(body)} while an ordinary one "
        f"answered {sorted(baseline.json())}; the two must be indistinguishable")
    assert db.registrations_like(trapped) == 0, (
        f"a registrations row was stored for the trapped submission {trapped}")
    settle()
    assert mail.count(trapped) == 0, (
        f"{mail.count(trapped)} messages reached {trapped}; a trapped submission sends "
        f"nothing")


def test_repeated_submissions_send_at_most_three_access_emails(mail):
    """Registrations and re-requests share one hourly ceiling of three emails."""
    address = probe_email("limit")
    attempts = [register(address), register(address), resend(address),
                register(address), resend(address)]
    for response in attempts:
        assert 200 <= response.status_code < 300, (
            f"a submission past the hourly limit returned {response.status_code}: "
            f"{response.text[:300]}")
    assert attempts[0].json().get("message") == SUCCESS_MESSAGE, (
        f"a registration answered {attempts[0].json().get('message')!r}")
    assert attempts[2].json().get("message") == RESEND_MESSAGE, (
        f"a re-request answered {attempts[2].json().get('message')!r}, expected "
        f"{RESEND_MESSAGE!r}")
    assert attempts[-1].json().get("message") == RESEND_MESSAGE, (
        f"a re-request past the limit answered {attempts[-1].json().get('message')!r}")
    seen = mail.wait_for_count(address, HOURLY_EMAILS)
    assert seen >= HOURLY_EMAILS, (
        f"{seen} access emails reached {address} after five submissions, expected "
        f"{HOURLY_EMAILS}")
    settle()
    assert mail.count(address) == HOURLY_EMAILS, (
        f"{mail.count(address)} access emails reached {address} after five submissions "
        f"inside one hour, expected at most {HOURLY_EMAILS}")


def test_access_link_email_goes_to_the_registrant_only(db, mail):
    """The access email reaches one recipient over Mailpit with the pinned lines."""
    address = probe_email("mail")
    response = register(address, name="Mail Probe")
    assert 200 <= response.status_code < 300, (
        f"POST /api/beta/register returned {response.status_code}: "
        f"{response.text[:300]}")
    assert mail.wait_for_count(address, 1) >= 1, (
        f"no message reached {address} through Mailpit, so the access link was never "
        f"sent over SMTP")
    message = mail.newest(address)
    recipients = [str(entry.get("Address", "")).lower()
                  for entry in message.get("To") or []]
    assert recipients == [address], (
        f"the access email is addressed to {recipients}, expected only {address}")
    assert not (message.get("Cc") or []), (
        f"the access email carries a cc: {message.get('Cc')}")
    assert not (message.get("Bcc") or []), (
        f"the access email carries a bcc: {message.get('Bcc')}")
    assert message.get("Subject") == SUBJECT, (
        f"the access email subject is {message.get('Subject')!r}, expected {SUBJECT!r}")

    text = str(message.get("Text") or "")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    assert lines, f"the access email to {address} carries no plain-text part"
    match = TOKEN_RE.search(lines[0])
    assert match, (
        f"the first plain-text line reads {lines[0]!r}, expected the access link "
        f"<APP_PUBLIC_URL>/beta/access/<token>")
    token = match.group(1)
    assert lines[0] == f"{app_url()}/beta/access/{token}", (
        f"the first line reads {lines[0]!r}, expected the absolute link built from "
        f"APP_PUBLIC_URL {app_url()!r}")
    assert len(token) >= 32, (
        f"the emailed token is {len(token)} characters, expected at least 32")
    second = lines[1] if len(lines) > 1 else None
    assert second == LINE_FIRST, (
        f"the second line reads {second!r}, expected {LINE_FIRST!r} for a first "
        f"registration")

    slot = db.slot_for(address)
    if slot is not None:
        assert f"{PLACE_PREFIX} {int(slot['position'])}" in text, (
            f"the email never names the held founder place "
            f"{int(slot['position'])} after {PLACE_PREFIX!r}: {text[:300]}")
    else:
        assert allocation()["state"] == "closed", (
            f"{address} holds no founder place while the cohort reports "
            f"{allocation()['state']}")


def test_access_link_opens_a_session_and_reports_the_founder_place(db, mail, billing):
    """Opening a live link confirms the place, sets the session and reaches billing."""
    address = probe_email("open")
    assert 200 <= register(address, name="Open Probe").status_code < 300, (
        f"registering {address} failed before the link could be opened")
    assert mail.wait_for_count(address, 1) >= 1, (
        f"no access email reached {address}")
    token = mail.newest_token(address)

    client, page = open_link(token)
    assert page.status_code == 200, (
        f"opening a live access link returned {page.status_code}: {page.text[:300]}")
    rendered = text_of(page.text)
    assert HEADING_CONFIRMED in rendered, (
        f"the access page never shows {HEADING_CONFIRMED!r}: {rendered[:300]}")
    assert DOWNLOAD_CONTROL in rendered, (
        f"the access page never offers a {DOWNLOAD_CONTROL!r} control: {rendered[:300]}")
    assert any(internal_path(href) == "/downloads/latest" for href in hrefs(page.text)), (
        f"the access page's download control points at none of {hrefs(page.text)[:8]}")
    assert re.search(r"<meta[^>]*robots[^>]*noindex|<meta[^>]*noindex[^>]*robots",
                     page.text, re.I), (
        "the access route markup carries no noindex robots instruction, so a crawled "
        "token becomes a leaked credential")

    cookies = set_cookie_headers(page)
    protected = [(raw, hop) for raw, hop in cookies if "httponly" in raw.lower()]
    assert protected, (
        f"opening a live link set no HttpOnly cookie: {[raw[:60] for raw, _ in cookies]}")
    link_rows = db.links_for(address)
    opened = [row for row in link_rows if int(row["opens"]) == 1]
    assert len(opened) == 1, (
        f"{len(opened)} links of {address} record one open after a single open: "
        f"{[(row['status'], row['opens']) for row in link_rows]}")
    life = db.link_lifetime_seconds(opened[0]["id"])
    assert abs(life - LINK_DAYS * 86400) <= 120, (
        f"the opened link lives {life:.0f}s, expected {LINK_DAYS} days")
    remaining = float(db.q(
        "SELECT EXTRACT(EPOCH FROM (expires_at::timestamptz - now())) AS remaining "
        "FROM access_links WHERE id = %s", (opened[0]["id"],))[0]["remaining"])
    for raw, hop in protected:
        assert not re.search(r";\s*secure(\s*;|\s*$)", raw, re.I), (
            f"the access session cookie is marked Secure on a plain-HTTP origin, so no "
            f"browser will ever return it: {raw[:80]}")
        lifetime = cookie_seconds(raw, hop)
        if lifetime is not None:
            assert lifetime <= remaining + 120, (
                f"the access session cookie lasts {lifetime:.0f}s while the link has "
                f"{remaining:.0f}s left, so the session outlives the link")

    status = client.get("/api/beta/status")
    client.close()
    assert status.status_code == 200, (
        f"GET /api/beta/status with an access session returned {status.status_code}: "
        f"{status.text[:300]}")
    body = status.json()
    for field in ("email", "founder_position", "founder_tier", "founder_price_minor",
                  "currency", "billing_account"):
        assert field in body, (
            f"GET /api/beta/status is missing the field {field!r}: {str(body)[:300]}")
    assert str(body["email"]).lower() == address, (
        f"GET /api/beta/status reports {body['email']!r} for the session of {address}")

    slot = db.slot_for(address)
    if slot is None:
        assert allocation()["state"] == "closed", (
            f"{address} holds no place while the cohort is open")
        return
    position = int(slot["position"])
    tier, price = expected_tier(position)
    assert int(body["founder_position"]) == position, (
        f"GET /api/beta/status reports place {body['founder_position']} while the "
        f"ledger holds place {position}")
    assert int(body["founder_tier"]) == tier, (
        f"place {position} is reported as tier {body['founder_tier']}, expected {tier}")
    assert int(body["founder_price_minor"]) == price, (
        f"place {position} is priced {body['founder_price_minor']}, expected {price}")
    assert str(body["currency"]) == CURRENCY, (
        f"GET /api/beta/status reports currency {body['currency']!r}, expected "
        f"{CURRENCY!r}")
    assert str(body["billing_account"]) in ("ready", "pending"), (
        f"GET /api/beta/status reports billing_account {body['billing_account']!r}, "
        f"expected ready or pending")
    account = wait_for(lambda: billing.account(founder_key(position)))
    assert account is not None, (
        f"no Kill Bill account carries externalKey {founder_key(position)} for the "
        f"place {address} holds, so the place exists only in the app's own tables")
    with site() as visitor:
        denied = visitor.get("/api/beta/status")
    assert denied.status_code in (401, 403), (
        f"GET /api/beta/status without a session returned {denied.status_code}, "
        f"expected a denial: {denied.text[:300]}")


def test_registrant_status_page_shows_only_the_registrant_place(db, mail):
    """Two sessions read their own state, and a visitor is sent to re-request."""
    first = probe_email("own-a")
    second = probe_email("own-b")
    for address in (first, second):
        assert 200 <= register(address).status_code < 300, (
            f"registering {address} failed before its status could be read")
        assert mail.wait_for_count(address, 1) >= 1, (
            f"no access email reached {address}")
    tokens = {address: mail.newest_token(address) for address in (first, second)}
    for address, token in tokens.items():
        with status_page_session(token) as client:
            state = client.get("/api/beta/status")
            assert state.status_code == 200, (
                f"GET /api/beta/status for {address} returned {state.status_code}: "
                f"{state.text[:300]}")
            assert str(state.json().get("email")).lower() == address, (
                f"the session of {address} reads the state of "
                f"{state.json().get('email')!r}")
            other = [value for key, value in tokens.items() if key != address][0]
            assert other not in state.text, (
                f"the status payload for {address} carries another registrant's token")
            page = client.get("/beta/status")
            assert page.status_code == 200, (
                f"GET /beta/status with a session returned {page.status_code}: "
                f"{page.text[:300]}")
            slot = db.slot_for(address)
            if slot is not None:
                assert str(int(slot["position"])) in text_of(page.text), (
                    f"/beta/status never shows the founder place "
                    f"{int(slot['position'])} of {address}")

    anonymous = page_html("/beta/status")
    assert anonymous.status_code == 200, (
        f"GET /beta/status without a session returned {anonymous.status_code}: "
        f"{anonymous.text[:300]}")
    body = text_of(anonymous.text)
    assert STATUS_NO_SESSION in body, (
        f"/beta/status without a session never shows {STATUS_NO_SESSION!r}: "
        f"{body[:300]}")
    assert any(tag.get("type", "").lower() == "email" or tag.get("name") == "email"
               for tag in input_tags(anonymous.text)), (
        "/beta/status without a session carries no re-request form")


def test_access_token_is_stored_only_as_a_hash(db, mail):
    """The raw token never reaches a stored column."""
    address = probe_email("hash")
    assert 200 <= register(address).status_code < 300, (
        f"registering {address} failed before its token could be read")
    assert mail.wait_for_count(address, 1) >= 1, f"no access email reached {address}"
    token = mail.newest_token(address)
    assert re.fullmatch(r"[A-Za-z0-9_-]{32,}", token), (
        f"the emailed token {token[:16]!r}... is not at least 32 letters, digits, "
        f"hyphens or underscores")
    rows = db.links_for(address)
    assert rows, f"no access_links row was stored for {address}"
    for row in rows:
        for column, value in row.items():
            assert token not in str(value), (
                f"access_links.{column} stores the raw token for {address}; the brief "
                f"stores a hash of it")
    hashes = {str(row["token_hash"]) for row in rows}
    assert all(value and token not in value for value in hashes), (
        f"a token_hash carries the raw token: {sorted(hashes)[:2]}")


def test_sixth_open_shows_the_used_up_page_and_sends_a_fresh_link(db, mail,
                                                                  operator_token):
    """The fifth open is the last, and revoked beats used up in the precedence."""
    address = probe_email("usedup")
    assert 200 <= register(address).status_code < 300, (
        f"registering {address} failed before its link could be opened")
    assert mail.wait_for_count(address, 1) >= 1, f"no access email reached {address}"
    token = mail.newest_token(address)

    with site() as client:
        for attempt in range(MAX_OPENS):
            response = client.get(f"/beta/access/{token}", follow_redirects=True)
            assert response.status_code == 200, (
                f"open {attempt + 1} of {MAX_OPENS} returned {response.status_code}: "
                f"{response.text[:300]}")
        sixth = client.get(f"/beta/access/{token}", follow_redirects=True)
    assert 400 <= sixth.status_code < 500 and sixth.status_code != 404, (
        f"the sixth open returned {sixth.status_code}, expected a client error other "
        f"than not-found: {sixth.text[:300]}")
    body = text_of(sixth.text)
    assert HEADING_USED_UP in body, (
        f"the sixth open never shows {HEADING_USED_UP!r}: {body[:300]}")
    assert address not in sixth.text, (
        f"the used-up page shows the registrant's address {address}")
    leaked = [found for found in EMAIL_RE.findall(body)
              if found.lower() != SUPPORT_EMAIL]
    assert not leaked, (
        f"the used-up page shows the email address(es) {leaked[:3]}")
    assert any(tag.get("type", "").lower() == "email" or tag.get("name") == "email"
               for tag in input_tags(sixth.text)), (
        "the used-up page carries no re-request form")

    rows = db.links_for(address)
    spent = [row for row in rows if int(row["opens"]) == MAX_OPENS]
    assert len(spent) == 1, (
        f"{len(spent)} links of {address} record {MAX_OPENS} opens: "
        f"{[(row['status'], row['opens']) for row in rows]}")
    assert all(int(row["opens"]) <= int(row["max_opens"]) for row in rows), (
        f"a link of {address} records more opens than its max_opens: "
        f"{[(row['opens'], row['max_opens']) for row in rows]}")
    assert mail.wait_for_count(address, 2) >= 2, (
        f"the first open after the fifth sent no fresh link to {address}")

    with site() as client:
        seventh = client.get(f"/beta/access/{token}", follow_redirects=True)
    assert HEADING_USED_UP in text_of(seventh.text), (
        f"a used-up link that a fresh link has superseded shows "
        f"{text_of(seventh.text)[:200]!r}, and used up outranks superseded")
    settle()
    assert mail.count(address) == 2, (
        f"{mail.count(address)} messages reached {address}; the fresh link is sent "
        f"once, on the first open after the fifth")

    with api(operator_token) as operator:
        revoked = operator.post("/admin/access-links/revoke", json={"email": address})
    assert 200 <= revoked.status_code < 300, (
        f"POST /api/admin/access-links/revoke returned {revoked.status_code}: "
        f"{revoked.text[:300]}")
    with site() as client:
        after = client.get(f"/beta/access/{token}", follow_redirects=True)
    assert HEADING_INVALID in text_of(after.text), (
        f"a revoked link that is also used up shows {text_of(after.text)[:200]!r}, "
        f"and revoked is the first failure in the precedence")


def test_click_log_keeps_one_click_per_link_each_half_hour(db, mail):
    """Repeated opens inside one window record one click."""
    address = probe_email("click")
    assert 200 <= register(address).status_code < 300, (
        f"registering {address} failed before its clicks could be counted")
    assert mail.wait_for_count(address, 1) >= 1, f"no access email reached {address}"
    token = mail.newest_token(address)
    with site() as client:
        for attempt in range(3):
            response = client.get(f"/beta/access/{token}", follow_redirects=True)
            assert response.status_code == 200, (
                f"open {attempt + 1} returned {response.status_code}: "
                f"{response.text[:300]}")
    rows = [row for row in db.links_for(address) if int(row["opens"]) == 3]
    assert len(rows) == 1, (
        f"{len(rows)} links of {address} record three opens: "
        f"{[(row['status'], row['opens']) for row in db.links_for(address)]}")
    clicks = db.clicks_for(rows[0]["id"])
    assert clicks == 1, (
        f"{clicks} access_clicks rows were written for three opens inside one "
        f"30-minute window, expected one")


def test_concurrent_opens_never_exceed_five(db, mail):
    """Eight simultaneous opens of one link leave the ledger at five."""
    address = probe_email("race-open")
    assert 200 <= register(address).status_code < 300, (
        f"registering {address} failed before the contention run")
    assert mail.wait_for_count(address, 1) >= 1, f"no access email reached {address}"
    token = mail.newest_token(address)

    statuses = []
    guard = threading.Lock()
    gate = threading.Barrier(8)

    def one() -> None:
        with site() as client:
            gate.wait()
            response = client.get(f"/beta/access/{token}", follow_redirects=True)
        with guard:
            statuses.append(response.status_code)

    threads = [threading.Thread(target=one) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=120)

    assert len(statuses) == 8, (
        f"{len(statuses)} of 8 simultaneous opens returned at all")
    accepted = [code for code in statuses if code == 200]
    assert len(accepted) == MAX_OPENS, (
        f"{len(accepted)} of 8 simultaneous opens were accepted, expected exactly "
        f"{MAX_OPENS}: {sorted(statuses)}")
    rows = db.links_for(address)
    assert max(int(row["opens"]) for row in rows) == MAX_OPENS, (
        f"the contended link records "
        f"{max(int(row['opens']) for row in rows)} opens, expected {MAX_OPENS}")
    assert all(int(row["opens"]) <= int(row["max_opens"]) for row in rows), (
        f"opens ran past max_opens under contention: "
        f"{[(row['opens'], row['max_opens']) for row in rows]}")


def test_fresh_link_supersedes_the_older_link(db, mail):
    """A re-request issues a new link, supersedes the old one and names the repeat."""
    address = probe_email("supersede")
    assert 200 <= register(address).status_code < 300, (
        f"registering {address} failed before the re-request")
    assert mail.wait_for_count(address, 1) >= 1, f"no access email reached {address}"
    older = mail.newest_token(address)

    answer = resend(address)
    assert 200 <= answer.status_code < 300, (
        f"POST /api/beta/resend returned {answer.status_code}: {answer.text[:300]}")
    payload = answer.json()
    assert payload.get("status") == "sent", (
        f"POST /api/beta/resend answered status {payload.get('status')!r}")
    assert payload.get("message") == RESEND_MESSAGE, (
        f"POST /api/beta/resend answered {payload.get('message')!r}, expected "
        f"{RESEND_MESSAGE!r}")
    assert mail.wait_for_count(address, 2) >= 2, (
        f"the re-request sent no second message to {address}")
    message = mail.newest(address)
    lines = [line.strip() for line in str(message.get("Text") or "").splitlines()
             if line.strip()]
    assert len(lines) > 1 and lines[1] == LINE_LATER, (
        f"the later email's second line reads "
        f"{(lines[1] if len(lines) > 1 else None)!r}, expected {LINE_LATER!r}")
    newer = mail.newest_token(address)
    assert newer != older, (
        f"the re-request emailed the same token {newer[:12]}... again")

    with site() as client:
        stale = client.get(f"/beta/access/{older}", follow_redirects=True)
        fresh = client.get(f"/beta/access/{newer}", follow_redirects=True)
    assert 400 <= stale.status_code < 500 and stale.status_code != 404, (
        f"the superseded link returned {stale.status_code}, expected a client error "
        f"other than not-found")
    assert HEADING_INVALID in text_of(stale.text), (
        f"the superseded link shows {text_of(stale.text)[:200]!r}, expected "
        f"{HEADING_INVALID!r}")
    assert fresh.status_code == 200 and HEADING_CONFIRMED in text_of(fresh.text), (
        f"the fresh link returned {fresh.status_code}: {text_of(fresh.text)[:200]}")

    states = [str(row["status"]) for row in db.links_for(address)]
    assert states.count("superseded") == 1, (
        f"the links of {address} carry the states {states}, expected exactly one "
        f"superseded")


def test_resend_for_an_unknown_address_answers_the_same_sentence(db, mail):
    """A re-request for a stranger writes nothing and sends nothing."""
    address = probe_email("ghost")
    response = resend(address)
    assert 200 <= response.status_code < 300, (
        f"POST /api/beta/resend for an unknown address returned "
        f"{response.status_code}: {response.text[:300]}")
    body = response.json()
    assert body.get("status") == "sent", (
        f"the re-request answered status {body.get('status')!r} for an unknown address")
    assert body.get("message") == RESEND_MESSAGE, (
        f"the re-request answered {body.get('message')!r} for an unknown address, "
        f"expected {RESEND_MESSAGE!r}")
    assert db.registrations_like(address) == 0, (
        f"a registrations row was created for the unknown address {address}")
    settle()
    assert mail.count(address) == 0, (
        f"{mail.count(address)} messages reached the unknown address {address}")


def test_seeded_dead_links_render_their_own_failure_pages():
    """Each unusable link answers a client error with its own heading and form."""
    assert 200 <= resend(REGISTRANT2_EMAIL).status_code < 300, (
        f"the re-request for {REGISTRANT2_EMAIL} failed before the expired link was read")
    unknown = f"unknown{os.urandom(16).hex()}"
    cases = ((SEED_REVOKED, HEADING_INVALID), (SEED_EXPIRED, HEADING_EXPIRED),
             (SEED_USEDUP, HEADING_USED_UP), (unknown, HEADING_UNKNOWN),
             ("short-token", HEADING_UNKNOWN))
    for token, heading in cases:
        response = page_html(f"/beta/access/{token}")
        assert 400 <= response.status_code < 500 and response.status_code != 404, (
            f"the link {token[:18]}... returned {response.status_code}, expected a "
            f"client error other than not-found: {response.text[:200]}")
        body = text_of(response.text)
        assert heading in body, (
            f"the link {token[:18]}... shows {body[:200]!r}, expected {heading!r}")
        for seeded in (REGISTRANT_EMAIL, REGISTRANT2_EMAIL, REGISTRANT3_EMAIL):
            assert seeded not in response.text, (
                f"the failure page for {token[:18]}... shows the address {seeded}")
        assert any(tag.get("type", "").lower() == "email" or tag.get("name") == "email"
                   for tag in input_tags(response.text)), (
            f"the failure page for {token[:18]}... carries no re-request form")
        if heading == HEADING_UNKNOWN:
            assert any(internal_path(href) == "/contact"
                       for href in hrefs(response.text)), (
                f"the not-recognised page links to none of "
                f"{hrefs(response.text)[:8]}, expected /contact")


def test_founder_place_opens_one_billing_account_in_killbill(db, billing, mail):
    """Every held place carries its own Kill Bill account with the pinned fields."""
    seeded = billing.account(founder_key(1))
    assert seeded is not None, (
        f"no Kill Bill account carries externalKey {founder_key(1)} for seeded place 1")
    assert str(seeded.get("email", "")).lower() == REGISTRANT_EMAIL, (
        f"the account for place 1 carries email {seeded.get('email')!r}, expected "
        f"{REGISTRANT_EMAIL}")

    state = allocation()
    checks = []
    if state["state"] == "open":
        named = probe_email("kb-named")
        plain = probe_email("kb-plain")
        assert 200 <= register(named, name="Billing Probe").status_code < 300, (
            f"registering {named} failed before its account could be read")
        assert 200 <= register(plain).status_code < 300, (
            f"registering {plain} failed before its account could be read")
        checks = [(named, "Billing Probe"), (plain, plain)]
    else:
        rows = db.q(
            "SELECT r.email AS email, r.name AS name, s.position AS position "
            "FROM founder_slots s JOIN registrations r ON r.id = s.registration_id "
            "ORDER BY s.position DESC LIMIT 2")
        checks = [(str(row["email"]), str(row["name"] or row["email"]))
                  for row in rows]

    for address, name in checks:
        slot = db.slot_for(address)
        assert slot is not None, (
            f"{address} holds no founder place while the cohort reports "
            f"{allocation()['state']}")
        position = int(slot["position"])
        key = founder_key(position)
        assert str(slot["killbill_external_key"]) == key, (
            f"place {position} stores the key {slot['killbill_external_key']!r}, "
            f"expected {key!r}")
        account = wait_for(lambda: billing.account(key))
        assert account is not None, (
            f"no Kill Bill account carries externalKey {key} for the place {address} "
            f"holds, so the place lives only in the app's own tables")
        assert str(account.get("externalKey")) == key, (
            f"the account read back for {key} carries externalKey "
            f"{account.get('externalKey')!r}")
        assert str(account.get("email", "")).lower() == address, (
            f"the account {key} carries email {account.get('email')!r}, expected "
            f"{address}")
        assert str(account.get("currency")) == "USD", (
            f"the account {key} carries currency {account.get('currency')!r}, "
            f"expected USD")
        assert str(account.get("country")) == "US", (
            f"the account {key} carries country {account.get('country')!r}, "
            f"expected US")
        assert str(account.get("name")) == name, (
            f"the account {key} is named {account.get('name')!r}, expected {name!r}")
        assert len(billing.accounts_for_email(address)) == 1, (
            f"{len(billing.accounts_for_email(address))} Kill Bill accounts carry "
            f"{address}, expected one per held place")
        logs = billing.audit_logs(account.get("accountId"))
        authors = {str(entry.get("changedBy") or "") for entry in logs}
        assert logs and all(authors), (
            f"the Kill Bill audit trail for {key} records the author(s) {sorted(authors)}, "
            f"so the write carried no X-Killbill-CreatedBy header naming the storefront")


def test_repeat_registration_creates_no_second_billing_account_or_invoice(db, billing):
    """Registering twice adds no account and no invoice to the tenant."""
    invoices_before = billing.invoice_count()
    if allocation()["state"] == "open":
        address = probe_email("kb-repeat")
        assert 200 <= register(address, name="Repeat Billing").status_code < 300, (
            f"registering {address} failed before the repeat")
        slot = wait_for(lambda: db.slot_for(address))
        assert slot is not None, f"{address} received no founder place"
        assert wait_for(lambda: billing.account(founder_key(int(slot["position"])))), (
            f"no Kill Bill account was opened for the place {address} holds")
    else:
        address = REGISTRANT_EMAIL
    accounts_before = len(billing.all_accounts())
    for _attempt in range(2):
        assert 200 <= register(address).status_code < 300, (
            f"re-registering {address} returned a failure")
    settle()
    assert len(billing.accounts_for_email(address)) == 1, (
        f"{len(billing.accounts_for_email(address))} Kill Bill accounts carry "
        f"{address} after repeat registrations, expected one")
    assert len(billing.all_accounts()) == accounts_before, (
        f"the tenant holds {len(billing.all_accounts())} accounts after two repeat "
        f"registrations, up from {accounts_before}")
    assert billing.invoice_count() == invoices_before, (
        f"the tenant holds {billing.invoice_count()} invoices, up from "
        f"{invoices_before}; registering creates no invoice")


def test_checkout_before_launch_is_refused_and_creates_no_billing_record(billing):
    """Checkout and licence activation are closed until 1.0, in the API and on the page."""
    accounts_before = len(billing.all_accounts())
    invoices_before = billing.invoice_count()
    with api() as client:
        checkout = client.post("/checkout/founder",
                               json={"email": probe_email("checkout"), "position": 7})
        licence = client.post("/licence/activate",
                              json={"key": "LUMEN-PROBE-KEY", "device": "probe"})
    assert 400 <= checkout.status_code < 500, (
        f"POST /api/checkout/founder returned {checkout.status_code}, expected a "
        f"client error: {checkout.text[:300]}")
    assert checkout.json().get("error") == "checkout_not_open", (
        f"POST /api/checkout/founder answered {str(checkout.json())[:200]}, expected "
        f"the error checkout_not_open")
    assert 400 <= licence.status_code < 500, (
        f"POST /api/licence/activate returned {licence.status_code}, expected a "
        f"client error: {licence.text[:300]}")
    assert licence.json().get("error") == "licensing_not_open", (
        f"POST /api/licence/activate answered {str(licence.json())[:200]}, expected "
        f"the error licensing_not_open")
    settle()
    assert len(billing.all_accounts()) == accounts_before, (
        f"a refused checkout left the tenant with {len(billing.all_accounts())} "
        f"accounts, up from {accounts_before}")
    assert billing.invoice_count() == invoices_before, (
        f"a refused checkout left the tenant with {billing.invoice_count()} invoices, "
        f"up from {invoices_before}")

    for path, notice in (("/checkout/founder", CHECKOUT_NOTICE),
                         ("/checkout/return", CHECKOUT_NOTICE),
                         ("/licence/activate", LICENCE_NOTICE)):
        response = page_html(path)
        assert response.status_code == 200, (
            f"GET {path} returned {response.status_code}: {response.text[:200]}")
        body = text_of(response.text)
        assert notice in body, (
            f"{path} never shows {notice!r}: {body[:300]}")
        if notice == CHECKOUT_NOTICE:
            assert any(internal_path(href) == "/download"
                       for href in hrefs(response.text)), (
                f"{path} links to none of {hrefs(response.text)[:8]}, expected /download")


def test_allocation_endpoint_matches_the_stored_founder_places(db):
    """The cohort figures are computed from the places actually held."""
    body = allocation()
    for field in ("cap", "tier_size", "claimed", "remaining", "state", "current_tier",
                  "current_price_minor", "currency"):
        assert field in body, (
            f"GET /api/founder/allocation is missing the field {field!r}: "
            f"{str(body)[:300]}")
    claimed = db.slot_count()
    assert int(body["cap"]) == COHORT_CAP, (
        f"the cohort reports cap {body['cap']}, expected {COHORT_CAP}")
    assert int(body["tier_size"]) == TIER_SIZE, (
        f"the cohort reports tier_size {body['tier_size']}, expected {TIER_SIZE}")
    assert int(body["claimed"]) == claimed, (
        f"the cohort reports {body['claimed']} claimed while founder_slots holds "
        f"{claimed} rows")
    assert int(body["remaining"]) == COHORT_CAP - claimed, (
        f"the cohort reports {body['remaining']} remaining against {claimed} claimed "
        f"places of {COHORT_CAP}")
    assert str(body["currency"]) == CURRENCY, (
        f"the cohort reports currency {body['currency']!r}, expected {CURRENCY!r}")
    if claimed < TIER_SIZE:
        assert str(body["state"]) == "open" and int(body["current_tier"]) == 1, (
            f"with {claimed} places held the cohort reports state {body['state']!r} "
            f"and tier {body['current_tier']!r}, expected open at tier 1")
        assert int(body["current_price_minor"]) == TIER1_PRICE, (
            f"the cohort prices the next place at {body['current_price_minor']}, "
            f"expected {TIER1_PRICE}")
    elif claimed < COHORT_CAP:
        assert str(body["state"]) == "open" and int(body["current_tier"]) == 2, (
            f"with {claimed} places held the cohort reports state {body['state']!r} "
            f"and tier {body['current_tier']!r}, expected open at tier 2")
        assert int(body["current_price_minor"]) == TIER2_PRICE, (
            f"the cohort prices the next place at {body['current_price_minor']}, "
            f"expected {TIER2_PRICE}")
    else:
        assert str(body["state"]) == "closed", (
            f"with every place held the cohort reports state {body['state']!r}")
        assert body["current_tier"] is None and body["current_price_minor"] is None, (
            f"a closed cohort reports tier {body['current_tier']!r} at "
            f"{body['current_price_minor']!r}, expected null for both")

    for slot in db.slots():
        position = int(slot["position"])
        tier, price = expected_tier(position)
        assert int(slot["tier"]) == tier, (
            f"place {position} is stored as tier {slot['tier']}, expected {tier}")
        assert int(slot["price_minor"]) == price, (
            f"place {position} is priced {slot['price_minor']}, expected {price}")
        assert str(slot["currency"]) == CURRENCY, (
            f"place {position} stores currency {slot['currency']!r}")
        assert str(slot["killbill_external_key"]) == founder_key(position), (
            f"place {position} stores the key {slot['killbill_external_key']!r}, "
            f"expected {founder_key(position)!r}")


def test_concurrent_registrations_store_distinct_contiguous_places(db):
    """Simultaneous registrations never share a place and never leave a gap."""
    before = allocation()
    batch = 40 if before["state"] == "open" and int(before["remaining"]) >= 60 else 16
    addresses = [probe_email("race") for _ in range(batch)]
    statuses = register_many(addresses, 10)
    assert len(statuses) == batch, (
        f"{len(statuses)} of {batch} simultaneous registrations answered at all")
    assert all(200 <= code < 300 for code in statuses), (
        f"simultaneous registrations returned {sorted(set(statuses))}, expected every "
        f"one to succeed")

    positions = [int(slot["position"]) for slot in db.slots()]
    assert len(positions) == len(set(positions)), (
        f"founder_slots holds a duplicated position after the contention run: "
        f"{sorted(p for p in positions if positions.count(p) > 1)[:5]}")
    assert positions == list(range(1, len(positions) + 1)), (
        f"the held places are not 1 to N with no gaps: {positions[:10]} ... "
        f"{positions[-5:]}")

    held = [db.slot_for(address) for address in addresses]
    fresh = [slot for slot in held if slot is not None]
    if before["state"] == "open" and int(before["remaining"]) >= batch:
        assert len(fresh) == batch, (
            f"{len(fresh)} of {batch} simultaneous registrations received a place "
            f"while {before['remaining']} remained")
    assert len({int(slot["position"]) for slot in fresh}) == len(fresh), (
        f"two of the simultaneous registrations share one place: "
        f"{sorted(int(slot['position']) for slot in fresh)[:6]}")
    for slot in fresh:
        tier, price = expected_tier(int(slot["position"]))
        assert int(slot["tier"]) == tier and int(slot["price_minor"]) == price, (
            f"place {int(slot['position'])} was stored as tier {slot['tier']} at "
            f"{slot['price_minor']}, expected tier {tier} at {price}")


def test_publishing_a_release_moves_every_release_surface(operator_token, db):
    """A publish becomes current stable everywhere, and a revoke leaves at once."""
    rows = releases()
    top = max(int(row["build"]) for row in rows)
    version = f"9.{int.from_bytes(os.urandom(2), 'big')}.{int.from_bytes(os.urandom(2), 'big')}"
    payload = release_payload(version, top + 1)
    revoked_before = text_of(page_html("/changelog").text).count(REVOKED_NOTICE)
    try:
        with api(operator_token) as operator:
            published = operator.post("/admin/releases", json=payload)
        assert published.status_code in (200, 201), (
            f"POST /api/admin/releases returned {published.status_code}: "
            f"{published.text[:300]}")
        stored = published.json()
        assert str(stored.get("version")) == version, (
            f"the publish answered for version {stored.get('version')!r}")
        assert str(stored.get("status")) == "published", (
            f"the published release carries status {stored.get('status')!r}")

        listed = release(version)
        assert listed is not None and int(listed["build"]) == top + 1, (
            f"GET /api/releases does not carry the published {version} at build "
            f"{top + 1}")
        assert releases()[0]["version"] == version, (
            f"the published build is not first in GET /api/releases: "
            f"{[row['version'] for row in releases()[:3]]}")

        with site() as client:
            redirect = client.get("/downloads/latest")
        assert 300 <= redirect.status_code < 400, (
            f"GET /downloads/latest returned {redirect.status_code}, expected a "
            f"redirect")
        assert redirect.headers.get("location") == payload["download_url"], (
            f"GET /downloads/latest points at {redirect.headers.get('location')!r}, "
            f"expected the published {payload['download_url']!r}")

        feed = page_html("/appcast.xml")
        assert version in feed.text, (
            f"/appcast.xml carries no item for the published {version}")
        changelog = text_of(page_html("/changelog").text)
        assert version in changelog, (
            f"/changelog never shows the published {version}")
        assert payload["summary"] in changelog, (
            f"/changelog never shows the published summary of {version}")
        download = text_of(page_html("/download").text)
        assert version in download, (
            f"the distribution panel on /download never shows the published {version}")
        notes = page_html(f"/release-notes/{version}")
        assert notes.status_code == 200, (
            f"GET /release-notes/{version} returned {notes.status_code} for a "
            f"published release")
    finally:
        with api(operator_token) as operator:
            revoke = operator.post(f"/admin/releases/{version}/revoke", json={})

    assert 200 <= revoke.status_code < 300, (
        f"POST /api/admin/releases/{version}/revoke returned {revoke.status_code}: "
        f"{revoke.text[:300]}")
    assert str(revoke.json().get("status")) == "revoked", (
        f"the revoke answered status {revoke.json().get('status')!r}")
    after = release(version)
    assert after is not None and str(after["status"]) == "revoked", (
        f"GET /api/releases reports {after and after['status']!r} for the revoked "
        f"{version}")

    stable = [row for row in releases() if str(row["status"]) == "published"][0]
    with site() as client:
        redirect = client.get("/downloads/latest")
    assert redirect.headers.get("location") == stable["download_url"], (
        f"after the revoke /downloads/latest points at "
        f"{redirect.headers.get('location')!r}, expected the current stable "
        f"{stable['download_url']!r}")
    feed = page_html("/appcast.xml")
    assert version not in feed.text, (
        f"/appcast.xml still carries an item for the revoked {version}")
    changelog = text_of(page_html("/changelog").text)
    assert version in changelog, (
        f"/changelog drops the revoked {version} instead of showing it as revoked")
    assert changelog.count(REVOKED_NOTICE) == revoked_before + 1, (
        f"/changelog shows {changelog.count(REVOKED_NOTICE)} revoked notices, expected "
        f"{revoked_before + 1} once {version} was revoked")
    assert payload["download_url"] not in page_html("/changelog").text, (
        f"/changelog still offers the download of the revoked {version}")
    assert db.release_rows() == len(releases()), (
        f"the releases table holds {db.release_rows()} rows while the API returns "
        f"{len(releases())}")


def test_invalid_release_publish_is_refused_and_stores_nothing(operator_token, db):
    """A malformed publish is refused and the registry is untouched."""
    rows = releases()
    top = max(int(row["build"]) for row in rows)
    stored_before = db.release_rows()
    base_version = f"8.{int.from_bytes(os.urandom(2), 'big')}.{int.from_bytes(os.urandom(2), 'big')}"
    base = release_payload(base_version, top + 1)
    cases = (
        ("version", dict(base, version="1.2")),
        ("version", dict(base, version="0.2.3")),
        ("build", dict(base, build=top)),
        ("sha256", dict(base, sha256="ABC" + "0" * 61)),
        ("sha256", dict(base, sha256="0" * 63)),
    )
    for field, payload in cases:
        with api(operator_token) as operator:
            response = operator.post("/admin/releases", json=payload)
        assert 400 <= response.status_code < 500, (
            f"POST /api/admin/releases with an invalid {field} returned "
            f"{response.status_code}, expected a client error: {response.text[:300]}")
    assert db.release_rows() == stored_before, (
        f"the releases table holds {db.release_rows()} rows after five rejected "
        f"publishes, up from {stored_before}")
    assert release(base_version) is None, (
        f"the rejected version {base_version} was stored anyway")
    assert str(release("0.2.3")["status"]) == "published", (
        "a rejected publish changed the seeded 0.2.3 release")


def test_download_redirect_records_one_download_event(db, mail):
    """Each redirect is recorded once, and a registrant's redirect names the link."""
    stable = [row for row in releases() if str(row["status"]) == "published"][0]
    version = str(stable["version"])
    count_before = int(stable["download_count"])
    events_before = db.download_events(version)
    with site() as client:
        first = client.get("/downloads/latest")
        second = client.get("/downloads/latest")
    for response in (first, second):
        assert 300 <= response.status_code < 400, (
            f"GET /downloads/latest returned {response.status_code}, expected a "
            f"redirect: {response.text[:200]}")
        assert response.headers.get("location") == str(stable["download_url"]), (
            f"GET /downloads/latest points at {response.headers.get('location')!r}, "
            f"expected {stable['download_url']!r}")
        assert "no-store" in str(response.headers.get("cache-control", "")).lower(), (
            f"GET /downloads/latest carries Cache-Control "
            f"{response.headers.get('cache-control')!r}, expected no-store")
    assert db.download_events(version) == events_before + 2, (
        f"two redirects wrote {db.download_events(version) - events_before} "
        f"download_events rows, expected two")
    after = release(version)
    assert int(after["download_count"]) == count_before + 2, (
        f"the download_count of {version} moved to {after['download_count']} from "
        f"{count_before}, expected exactly two more")
    assert int(after["download_count"]) == db.download_events(version), (
        f"the reported download_count {after['download_count']} differs from the "
        f"{db.download_events(version)} stored download events")

    address = probe_email("download")
    assert 200 <= register(address).status_code < 300, (
        f"registering {address} failed before the session download")
    assert mail.wait_for_count(address, 1) >= 1, f"no access email reached {address}"
    with status_page_session(mail.newest_token(address)) as client:
        followed = client.get("/downloads/latest", follow_redirects=False)
    assert 300 <= followed.status_code < 400, (
        f"a registrant's GET /downloads/latest returned {followed.status_code}")
    event = db.newest_download_event(version)
    assert event is not None and event["access_link_id"] is not None, (
        f"the newest download_events row carries access_link_id "
        f"{event and event['access_link_id']!r}, expected the registrant's link")


def test_update_feed_lists_published_releases_with_registry_values():
    """The appcast repeats the registry byte for byte and drops revoked builds."""
    response = page_html("/appcast.xml")
    assert response.status_code == 200, (
        f"GET /appcast.xml returned {response.status_code}: {response.text[:200]}")
    namespace = "http://www.andymatuschak.org/xml-namespaces/sparkle"
    assert re.search(rf'xmlns:sparkle=["\']{re.escape(namespace)}["\']', response.text), (
        f"/appcast.xml declares no sparkle namespace: {response.text[:300]}")
    root = ET.fromstring(response.content)
    items = root.findall("./channel/item")
    published = [row for row in releases() if str(row["status"]) == "published"]
    assert len(items) == len(published), (
        f"/appcast.xml carries {len(items)} items against {len(published)} published "
        f"releases")
    namespaces = {"sparkle": namespace}
    for item, row in zip(items, published):
        version = str(row["version"])
        assert item.findtext("title") == f"Lumen Prompt {version}", (
            f"the feed item for {version} is titled {item.findtext('title')!r}")
        assert item.findtext("sparkle:version", namespaces=namespaces) == str(row["build"]), (
            f"the feed item for {version} carries sparkle:version "
            f"{item.findtext('sparkle:version', namespaces=namespaces)!r}, expected "
            f"the build {row['build']}")
        assert item.findtext("sparkle:shortVersionString",
                             namespaces=namespaces) == version, (
            f"the feed item carries shortVersionString "
            f"{item.findtext('sparkle:shortVersionString', namespaces=namespaces)!r}, "
            f"expected {version}")
        assert item.findtext("sparkle:minimumSystemVersion",
                             namespaces=namespaces) == str(row["min_os"]), (
            f"the feed item for {version} carries minimumSystemVersion "
            f"{item.findtext('sparkle:minimumSystemVersion', namespaces=namespaces)!r}, "
            f"expected {row['min_os']}")
        notes_link = item.findtext("sparkle:releaseNotesLink",
                                   namespaces=namespaces) or ""
        assert urlparse(notes_link).path == f"/release-notes/{version}", (
            f"the feed item for {version} links its notes at {notes_link!r}")
        enclosures = item.findall("enclosure")
        assert len(enclosures) == 1, (
            f"the feed item for {version} carries {len(enclosures)} enclosures, "
            f"expected one")
        enclosure = enclosures[0]
        assert enclosure.get("url") == str(row["download_url"]), (
            f"the enclosure for {version} points at {enclosure.get('url')!r}, expected "
            f"{row['download_url']!r}")
        assert str(enclosure.get("length")) == str(row["size_bytes"]), (
            f"the enclosure for {version} declares length {enclosure.get('length')!r}, "
            f"expected {row['size_bytes']}")
        assert enclosure.get("type") == "application/octet-stream", (
            f"the enclosure for {version} declares type {enclosure.get('type')!r}")
        signature = enclosure.get(f"{{{namespace}}}edSignature")
        assert signature == str(row["ed_signature"]), (
            f"the enclosure for {version} repeats the signature {str(signature)[:20]!r}, "
            f"expected the registry's {str(row['ed_signature'])[:20]!r}")
    shown = {item.findtext("sparkle:shortVersionString", namespaces=namespaces)
             for item in items}
    withdrawn = {str(row["version"]) for row in releases()
                 if str(row["status"]) == "revoked"}
    assert not (shown & withdrawn), (
        f"/appcast.xml carries the revoked release(s) {sorted(shown & withdrawn)}")


def test_release_notes_render_their_sections_in_order_with_the_cache_policy():
    """The notes route is immutable, ordered and complete without scripting."""
    response = page_html("/release-notes/0.2.3")
    assert response.status_code == 200, (
        f"GET /release-notes/0.2.3 returned {response.status_code}: "
        f"{response.text[:200]}")
    cache = str(response.headers.get("cache-control", "")).replace(" ", "").lower()
    for directive in ("public", "max-age=3600", "stale-while-revalidate=86400"):
        assert directive in cache, (
            f"/release-notes/0.2.3 carries Cache-Control "
            f"{response.headers.get('cache-control')!r}, missing {directive}")
    body = text_of(response.text)
    assert "Lumen Prompt is free during the beta." in body, (
        f"the release notes never carry the beta note: {body[:300]}")
    assert "0.2.3" in body and "2026-08-28" in response.text, (
        f"the release notes never show the version with its published date: "
        f"{body[:300]}")
    found = [text for text in headings(response.text) if text in RELEASE_NOTE_SECTIONS]
    assert found == list(RELEASE_NOTE_SECTIONS), (
        f"the release-note sections read {found}, expected {list(RELEASE_NOTE_SECTIONS)} "
        f"in that order")
    for source in ("Espresso", "Alder", "Rayline", "Obelisk"):
        assert source in body, (
            f"the 0.2.3 notes never name the import source {source}")
    known = section_after(response.text, "Known issues").lower()
    for issue in ("accessibility permission", "clipboard", "browser tab",
                  "mail handler"):
        assert issue in text_of(known).lower(), (
            f"the known issues never mention {issue!r}: {text_of(known)[:300]}")

    unknown = page_html("/release-notes/99.99.99")
    assert unknown.status_code == 404, (
        f"GET /release-notes/99.99.99 returned {unknown.status_code}, expected "
        f"not found")
    assert any(internal_path(href) == "/changelog" for href in hrefs(unknown.text)), (
        f"the unknown-version page links to none of {hrefs(unknown.text)[:8]}, "
        f"expected /changelog")


def test_operator_login_issues_a_token_and_refuses_a_wrong_password(db):
    """The seeded operator signs in, a wrong password does not, and the hash holds."""
    with api() as client:
        good = client.post("/auth/login",
                           json={"email": OPERATOR_EMAIL, "password": PASSWORD})
        bad = client.post("/auth/login",
                          json={"email": OPERATOR_EMAIL,
                                "password": PASSWORD + "-wrong"})
        stranger = client.post("/auth/login",
                               json={"email": probe_email("nobody"),
                                     "password": PASSWORD})
    assert good.status_code == 200, (
        f"POST /api/auth/login with the seeded password returned {good.status_code}: "
        f"{good.text[:300]}")
    token = good.json().get("access_token")
    assert token, (
        f"POST /api/auth/login answered {str(good.json())[:200]}, expected an "
        f"access_token")
    for response, label in ((bad, "a wrong password"), (stranger, "an unknown email")):
        assert response.status_code in (400, 401, 403), (
            f"POST /api/auth/login with {label} returned {response.status_code}, "
            f"expected a denial: {response.text[:300]}")
        if response.headers.get("content-type", "").startswith("application/json"):
            assert not response.json().get("access_token"), (
                f"POST /api/auth/login with {label} still answered a token")

    with api(token) as operator:
        listed = operator.get("/admin/registrations")
    assert listed.status_code == 200, (
        f"GET /api/admin/registrations with a fresh operator token returned "
        f"{listed.status_code}: {listed.text[:300]}")
    with api(f"forged-{os.urandom(8).hex()}") as impostor:
        refused = impostor.get("/admin/registrations")
    assert refused.status_code in (401, 403), (
        f"GET /api/admin/registrations with an invalid bearer token returned "
        f"{refused.status_code}, expected a denial: {refused.text[:300]}")
    hashes = db.q("SELECT password_hash FROM operators")
    for row in hashes:
        assert PASSWORD not in str(row["password_hash"]), (
            f"an operators row stores the password in the clear: "
            f"{str(row['password_hash'])[:40]!r}")


def test_operator_endpoints_are_denied_to_a_visitor_and_a_registrant(db, mail):
    """Every operator endpoint refuses a visitor, a registrant and a forged token."""
    address = probe_email("deny")
    assert 200 <= register(address).status_code < 300, (
        f"registering {address} failed before the denial run")
    assert mail.wait_for_count(address, 1) >= 1, f"no access email reached {address}"
    registrant = status_page_session(mail.newest_token(address))

    links_before = [(row["id"], str(row["status"]))
                    for row in db.links_for(REGISTRANT_EMAIL)]
    releases_before = db.release_rows()
    stable_before = str(release("0.2.3")["status"])
    version = "0.2.2"
    rows = releases()
    top = max(int(row["build"]) for row in rows)
    payload = release_payload(
        f"7.{int.from_bytes(os.urandom(2), 'big')}.{int.from_bytes(os.urandom(2), 'big')}",
        top + 1)
    attempts = (
        ("GET", "/api/admin/registrations", None),
        ("POST", "/api/admin/releases", payload),
        ("POST", f"/api/admin/releases/{version}/revoke", {}),
        ("POST", "/api/admin/access-links/revoke", {"email": REGISTRANT_EMAIL}),
    )
    visitor = site()
    forged = site()
    forged.headers["Authorization"] = f"Bearer forged-{os.urandom(8).hex()}"
    callers = (("a visitor", visitor), ("a registrant session", registrant),
               ("a forged token", forged))
    try:
        for label, client in callers:
            for method, path, body in attempts:
                response = client.request(method, path, json=body)
                assert response.status_code in (401, 403), (
                    f"{method} {path} from {label} returned {response.status_code}, "
                    f"expected a denial: {response.text[:300]}")
    finally:
        visitor.close()
        forged.close()
        registrant.close()

    assert [(row["id"], str(row["status"]))
            for row in db.links_for(REGISTRANT_EMAIL)] == links_before, (
        f"a denied revoke changed the links of {REGISTRANT_EMAIL}")
    assert db.release_rows() == releases_before, (
        f"a denied publish stored a release: the table holds {db.release_rows()} rows, "
        f"up from {releases_before}")
    assert str(release("0.2.3")["status"]) == stable_before, (
        f"a denied call changed the status of 0.2.3 to {release('0.2.3')['status']!r}")
    assert str(release(version)["status"]) == "published", (
        f"a denied revoke changed {version} to {release(version)['status']!r}")
    assert release(payload["version"]) is None, (
        f"a denied publish stored {payload['version']} anyway")


def test_operator_lists_registrations_newest_first_with_their_places(operator_token, db):
    """The console's list is newest first, filterable and empty for a stranger."""
    first = probe_email("list-a")
    second = probe_email("list-b")
    for address in (first, second):
        assert 200 <= register(address, name="List Probe").status_code < 300, (
            f"registering {address} failed before the list was read")
    with api(operator_token) as operator:
        everything = operator.get("/admin/registrations")
        filtered = operator.get("/admin/registrations",
                                params={"email": f"  {first.upper()} "})
        seeded = operator.get("/admin/registrations",
                              params={"email": REGISTRANT_EMAIL})
        stranger = operator.get("/admin/registrations",
                                params={"email": probe_email("stranger")})
    assert everything.status_code == 200, (
        f"GET /api/admin/registrations returned {everything.status_code}: "
        f"{everything.text[:300]}")
    rows = everything.json()
    assert isinstance(rows, list) and rows, (
        f"GET /api/admin/registrations answered {str(rows)[:200]}, expected a "
        f"top-level array")
    for field in ("email", "name", "founder_position", "challenge_status", "created_at"):
        assert field in rows[0], (
            f"a registrations row is missing the field {field!r}: {str(rows[0])[:200]}")
    emails = [str(row["email"]).lower() for row in rows]
    assert first in emails and second in emails, (
        f"the list of {len(emails)} registrations carries neither probe address")
    assert emails.index(second) < emails.index(first), (
        f"the list places the older {first} above the newer {second}, expected newest "
        f"first")

    assert filtered.status_code == 200, (
        f"the filtered list returned {filtered.status_code}: {filtered.text[:300]}")
    matched = filtered.json()
    assert [str(row["email"]).lower() for row in matched] == [first], (
        f"filtering on {first} answered {[row.get('email') for row in matched][:4]}, "
        f"expected only the normalised address")
    seeded_rows = seeded.json()
    assert len(seeded_rows) == 1 and int(seeded_rows[0]["founder_position"]) == 1, (
        f"the console reports {seeded_rows[:1]} for {REGISTRANT_EMAIL}, expected "
        f"founder place 1")
    assert stranger.status_code == 200, (
        f"filtering on an unregistered address returned {stranger.status_code}: "
        f"{stranger.text[:300]}")
    assert stranger.json() == [], (
        f"filtering on an unregistered address answered {str(stranger.json())[:200]}, "
        f"expected an empty array")


def test_operator_revokes_the_access_links_of_one_address(operator_token, db, mail):
    """A revoke counts what it revoked and closes those links only."""
    target = probe_email("revoke-a")
    bystander = probe_email("revoke-b")
    for address in (target, bystander):
        assert 200 <= register(address).status_code < 300, (
            f"registering {address} failed before the revoke")
        assert mail.wait_for_count(address, 1) >= 1, f"no access email reached {address}"
    target_token = mail.newest_token(target)
    bystander_token = mail.newest_token(bystander)

    with api(operator_token) as operator:
        response = operator.post("/admin/access-links/revoke", json={"email": target})
        again = operator.post("/admin/access-links/revoke", json={"email": target})
    assert 200 <= response.status_code < 300, (
        f"POST /api/admin/access-links/revoke returned {response.status_code}: "
        f"{response.text[:300]}")
    assert int(response.json().get("revoked")) == 1, (
        f"the revoke answered {str(response.json())[:200]}, expected revoked 1 for one "
        f"active link")
    assert int(again.json().get("revoked")) == 0, (
        f"a second revoke answered {str(again.json())[:200]}, expected revoked 0")
    states = [str(row["status"]) for row in db.links_for(target)]
    assert states and set(states) == {"revoked"}, (
        f"the links of {target} carry the states {states} after a revoke")

    with site() as client:
        blocked = client.get(f"/beta/access/{target_token}", follow_redirects=True)
        open_still = client.get(f"/beta/access/{bystander_token}", follow_redirects=True)
    assert HEADING_INVALID in text_of(blocked.text), (
        f"the revoked link shows {text_of(blocked.text)[:200]!r}, expected "
        f"{HEADING_INVALID!r}")
    assert open_still.status_code == 200 and HEADING_CONFIRMED in text_of(open_still.text), (
        f"the revoke closed the untouched link of {bystander}: "
        f"{text_of(open_still.text)[:200]}")


def test_data_request_is_stored_open_and_a_bad_one_is_refused(db):
    """Each intake kind is stored open, and anything else is refused."""
    for kind in ("access", "export", "correction", "deletion"):
        address = probe_email(f"dsr-{kind}")
        with api() as client:
            response = client.post("/legal/data-requests",
                                   json={"email": address, "kind": kind})
        assert 200 <= response.status_code < 300, (
            f"POST /api/legal/data-requests with kind {kind} returned "
            f"{response.status_code}: {response.text[:300]}")
        body = response.json()
        assert body.get("status") == "received", (
            f"the intake answered status {body.get('status')!r}, expected received")
        assert body.get("message") == DATA_REQUEST_MESSAGE, (
            f"the intake answered {body.get('message')!r}, expected "
            f"{DATA_REQUEST_MESSAGE!r}")
        rows = db.data_requests(address)
        assert len(rows) == 1, (
            f"{len(rows)} data_requests rows hold {address}, expected one")
        assert str(rows[0]["kind"]) == kind, (
            f"the stored request carries kind {rows[0]['kind']!r}, expected {kind!r}")
        assert str(rows[0]["status"]) == "open", (
            f"the stored request carries status {rows[0]['status']!r}, expected open")

    refused = probe_email("dsr-bad")
    cases = ({"kind": "access"}, {"email": refused, "kind": "erasure"},
             {"email": refused, "kind": ""}, {"email": "not-an-address",
                                              "kind": "access"})
    for payload in cases:
        with api() as client:
            response = client.post("/legal/data-requests", json=payload)
        assert 400 <= response.status_code < 500, (
            f"POST /api/legal/data-requests with {payload} returned "
            f"{response.status_code}, expected a client error: {response.text[:300]}")
    assert db.data_requests(refused) == [], (
        f"{len(db.data_requests(refused))} rows were stored for the refused intake "
        f"of {refused}")

    form = page_html("/legal/data-request")
    assert form.status_code == 200, (
        f"GET /legal/data-request returned {form.status_code}: {form.text[:200]}")
    fields = input_tags(form.text)
    assert any(tag.get("type", "").lower() == "email" or tag.get("name") == "email"
               for tag in fields), (
        "/legal/data-request carries no email field")
    body = text_of(form.text)
    for kind in ("access", "export", "correction", "deletion"):
        assert kind in body.lower(), (
            f"/legal/data-request never offers the kind {kind!r}: {body[:300]}")


def test_every_response_carries_the_security_headers():
    """The three headers ride on every response and the policy stays same-origin."""
    probes = ("/", "/download", "/changelog", "/api/health", "/api/founder/allocation",
              "/appcast.xml", "/robots.txt", "/downloads/latest",
              f"/no-such-address-{os.urandom(4).hex()}")
    for path in probes:
        response = page_html(path)
        headers = response.headers
        transport = str(headers.get("strict-transport-security", "")).replace(" ", "").lower()
        assert transport == "max-age=31536000;includesubdomains", (
            f"GET {path} carries Strict-Transport-Security "
            f"{headers.get('strict-transport-security')!r}, expected "
            f"max-age=31536000; includeSubDomains")
        assert str(headers.get("x-content-type-options", "")).lower() == "nosniff", (
            f"GET {path} carries X-Content-Type-Options "
            f"{headers.get('x-content-type-options')!r}, expected nosniff")
        assert str(headers.get("referrer-policy", "")).lower() == "strict-origin-when-cross-origin", (
            f"GET {path} carries Referrer-Policy {headers.get('referrer-policy')!r}, "
            f"expected strict-origin-when-cross-origin")

    policy = str(page_html("/").headers.get("content-security-policy", ""))
    assert policy, (
        "GET / carries no content security policy, so the page may load from any origin")
    own = urlparse(app_url()).netloc
    for token in re.split(r"[\s;]+", policy):
        assert token not in ("*", "http:", "https:"), (
            f"the content security policy carries the wildcard source {token!r}, so it "
            f"allows more than the site's own origin: {policy[:200]}")
        if "://" in token:
            assert urlparse(token.rstrip("/")).netloc == own, (
                f"the content security policy allows the foreign origin {token!r}, "
                f"and this environment has no analytics, challenge or backend host: "
                f"{policy[:200]}")


def test_sitemap_and_robots_describe_the_content_routes():
    """The sitemap lists the sixteen content routes and robots excludes the rest."""
    response = page_html("/sitemap.xml")
    assert response.status_code == 200, (
        f"GET /sitemap.xml returned {response.status_code}: {response.text[:200]}")
    locations = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", response.text)
    assert locations, f"/sitemap.xml lists no address: {response.text[:300]}"
    for location in locations:
        parsed = urlparse(location)
        assert parsed.scheme in ("http", "https") and parsed.netloc, (
            f"/sitemap.xml lists {location!r}, which is not an absolute address")
    listed = sorted({(urlparse(one).path or "/").rstrip("/") or "/" for one in locations})
    wanted = sorted({route.rstrip("/") or "/" for route in CONTENT_ROUTES})
    assert listed == wanted, (
        f"/sitemap.xml lists {listed}, expected exactly the sixteen content routes "
        f"{wanted}")
    assert len(locations) == len(CONTENT_ROUTES), (
        f"/sitemap.xml carries {len(locations)} entries for "
        f"{len(CONTENT_ROUTES)} content routes")

    robots = page_html("/robots.txt")
    assert robots.status_code == 200, (
        f"GET /robots.txt returned {robots.status_code}: {robots.text[:200]}")
    lines = [line.strip() for line in robots.text.splitlines()]
    for rule in ("Disallow: /downloads/latest", "Disallow: /beta/access/",
                 "Disallow: /checkout/"):
        assert rule in lines, (
            f"/robots.txt carries no {rule!r} line: {robots.text[:300]}")
    api_rule = "Disallow: " + "/api" + "/"
    assert api_rule in lines, (
        f"/robots.txt never excludes the function namespace: {robots.text[:300]}")
    sitemap_lines = [line for line in lines if line.lower().startswith("sitemap:")]
    assert sitemap_lines, (
        f"/robots.txt names no sitemap: {robots.text[:300]}")
    for line in sitemap_lines:
        target = line.split(":", 1)[1].strip()
        assert urlparse(target).path == "/sitemap.xml", (
            f"/robots.txt points at {target!r}, expected the sitemap of this site")


def test_every_internal_link_on_the_public_routes_resolves():
    """No link on a public route leads to the not-found page or an error."""
    surfaces = list(CONTENT_ROUTES) + list(ARTICLE_ROUTES) + ["/legal/data-request"]
    discovered = set()
    for path in surfaces:
        response = page_html(path)
        assert response.status_code == 200, (
            f"GET {path} returned {response.status_code}: {response.text[:200]}")
        links = [internal_path(href) for href in hrefs(response.text)]
        links = [link for link in links if link]
        assert links, f"{path} carries no internal link at all"
        discovered.update(links)
        for expected in ("/privacy", "/terms", "/download"):
            assert expected in links, (
                f"{path} never links to {expected}, which every page owes")
        assert "Join beta" in text_of(response.text), (
            f"{path} never carries the Join beta action")

    with site() as client:
        for path in sorted(discovered):
            response = client.get(path)
            assert response.status_code < 400, (
                f"the internal link {path} answers {response.status_code}, so a link on "
                f"a public route leads to an error or the not-found page")

    for route in PALETTE_DESTINATION_ROUTES:
        assert route in discovered, (
            f"the palette destination {route} is reachable from no link on any public "
            f"route, so a visitor without scripting cannot reach it")

    home = page_html("/").text
    anchors = [href for href in hrefs(home) if "#" in href]
    for anchor in ("#features", "#workflow", "#pricing", "#help"):
        assert any(href.endswith(anchor) for href in anchors), (
            f"the home route carries no link to {anchor}: {anchors[:8]}")

    missing = page_html(f"/no-such-address-{os.urandom(4).hex()}")
    assert missing.status_code == 404, (
        f"an unknown address returned {missing.status_code}, expected not found")
    body = text_of(missing.text)
    assert "Lumen Prompt" in body, (
        f"the not-found page is not branded: {body[:300]}")
    targets = {internal_path(href) for href in hrefs(missing.text)}
    for expected in ("/", "/download", "/changelog", "/contact"):
        assert expected in targets, (
            f"the not-found page links to {sorted(t for t in targets if t)[:8]}, "
            f"missing {expected}")
    assert re.search(r"\bK\b", body), (
        f"the not-found page offers no palette shortcut hint: {body[:300]}")


def test_home_sections_render_in_the_pinned_order_without_scripts():
    """The fourteen sections, their eyebrows and the hero survive with no scripting."""
    response = page_html("/")
    assert response.status_code == 200, (
        f"GET / returned {response.status_code}: {response.text[:200]}")
    html = response.text
    body = text_of(html)
    found = [text for text in headings(html) if text in HOME_HEADINGS]
    assert found == list(HOME_HEADINGS), (
        f"the home headings read {found}, expected the fourteen pinned headings in "
        f"order")
    marked = {text.lower() for text in headings(html)}
    for eyebrow in HOME_EYEBROWS:
        assert eyebrow.lower() in body.lower(), (
            f"the home route never shows the eyebrow {eyebrow!r}")
        assert eyebrow.lower() not in marked, (
            f"the eyebrow {eyebrow!r} is marked up as a heading, and an eyebrow is not "
            f"a heading")
    for anchor in ("features", "workflow", "pricing", "help"):
        assert re.search(rf'id=["\']{anchor}["\']', html), (
            f"the home route carries no element with the section anchor {anchor!r}")

    for key in ("Cmd", "Shift", "Space"):
        assert key in body, f"the hero never shows the key cap {key!r}"
    hero_copy = (
        "Lumen Prompt keeps the prompts you reuse at work one keystroke away, with "
        "their variables, files and history.",
        "Free during beta. No card required.",
        "Local-first", "Signed builds", "No subscription",
        "FREE DURING BETA", "Join beta", "Try the hotkey",
    )
    for phrase in hero_copy:
        assert phrase in body, (
            f"the hero never carries the pinned copy {phrase!r}: {body[:300]}")
    assert "Requires macOS 26.1 or later" in body, (
        "the closing section never states the system requirement")
    assert ld_types(html) & {"SoftwareApplication"}, (
        f"the home route carries no SoftwareApplication structured data: "
        f"{sorted(ld_types(html))}")


def test_home_instrument_copy_and_bullets_are_pinned():
    """The beats, the runner, the surface bullets and the ledger read as pinned."""
    html = page_html("/").text
    body = text_of(html)
    beats = (
        ("Summon hotkey", "Press the hotkey over your current Mac workspace."),
        ("Search library", "Type a few letters to filter your Blueprint Library."),
        ("Fill variables", "Variables become visible fields."),
        ("Inject history", "Copy the rendered prompt or inject it with context files."),
    )
    for name, sentence in beats:
        assert name in body, f"the workflow section never names the beat {name!r}"
        assert sentence in body, (
            f"the beat {name!r} never carries its pinned description {sentence!r}")
    for phrase in ("Client brief summary", "No context switch", "Finished prompt"):
        assert phrase in body, (
            f"the workflow runner never shows {phrase!r}: {body[:300]}")

    bullets = (
        "search and filter instantly",
        "organise by workflow, tag and variable count",
        "open for editing, injection or history",
        "turn placeholders into visible fields",
        "include or exclude files before injection",
        "remember project-level variables",
        "a version scrubber per blueprint",
        "star ratings for strong versions",
        "compare and restore controls",
    )
    lowered = body.lower()
    for bullet in bullets:
        assert bullet in lowered, (
            f"the product-surface sections never carry the bullet {bullet!r}")

    for term in ("Blueprint", "Context", "Time Machine", "Injection History"):
        assert term in body, f"the home route never uses the product noun {term!r}"
    assert "Demonstration data" in body, (
        "the injection history ledger carries no demonstration-data label")
    assert "Quick copy" in body, (
        "the ledger rows never show the Quick copy detail")
    for app in ("Chatwell", "Cadence", "Vertan", "Caret"):
        assert app in body, f"the ledger never names the target application {app!r}"
    assert "Devrim" in body and "See the roadmap" in body, (
        "the beta note is not signed by Devrim with a forward link to the roadmap")
    assert any(internal_path(href) == "/roadmap" for href in hrefs(html)), (
        "the beta note links to no roadmap route")
    assert "stay on your Mac" in body, (
        f"the local-first section never states that prompt work stays on the Mac: "
        f"{body[:300]}")


def test_home_comparison_renders_as_a_real_table():
    """The comparison is a table with a caption, headers and the qualified cells."""
    html = page_html("/").text
    body = text_of(html)
    tables = re.findall(r"<table\b.*?</table>", html, flags=re.S | re.I)
    assert tables, "the comparison section renders no table element"
    captions = re.findall(r"<caption\b[^>]*>(.*?)</caption>", html, flags=re.S | re.I)
    assert captions, "the comparison table carries no caption"
    assert len({text_of(one).strip().lower() for one in captions}) == len(captions), (
        f"two comparison tables share a caption: {[text_of(one) for one in captions]}")
    features = (
        "Global hotkey launcher", "Variables with remembered values",
        "Version history per prompt", "Context files attached before sending",
        "Injection history", "Stored on your Mac", "One-time licence",
    )
    joined = "\n".join(tables)
    for feature in features:
        assert re.search(rf"<th\b[^>]*>(?:\s|<[^>]+>)*{re.escape(feature)}",
                         joined, re.I | re.S), (
            f"the feature {feature!r} is not a row header in the comparison table")
    for tool in ("Notary Docs", "Rayline Snippets", "Provider Projects", "Lumen Prompt"):
        assert tool in text_of(joined), (
            f"the comparison table never names the column {tool!r}")
    for qualified in ("Plain placeholders only", "Page history, not per prompt",
                      "Per project, in the vendor's cloud"):
        assert qualified in text_of(joined), (
            f"the comparison table never shows the qualified cell {qualified!r}")
    marks = text_of(joined).lower() + " " + joined.lower()
    assert "present" in marks and "absent" in marks, (
        "the comparison marks never carry present or absent in their accessible names")
    assert ("Comparison checked on 2026-08-15 against each tool's public "
            "documentation.") in body, (
        f"the dated comparison footnote is absent: {body[:300]}")


def test_home_pricing_and_help_copy_is_pinned():
    """The three pricing cards and the eight help questions read as pinned."""
    html = page_html("/").text
    body = text_of(html)
    pricing = (
        "$0", "Everything, during the beta", "25 Blueprints", "3 contexts",
        "30 days", "About the cost of 15 billable minutes",
        "Every 1.x update, for life", "One-time payment", "Numbered founder place",
        "Signed builds and updates", "Price locked to your place",
        "Standard licence at 1.0: $49", "Claim a founder place",
        "Checkout is not open yet. Registering holds your place.",
        "Extended licence", "$79", "Update renewal", "$19",
    )
    for phrase in pricing:
        assert phrase in body, (
            f"the pricing section never carries the pinned copy {phrase!r}")
    assert any(internal_path(href) == "/download" for href in hrefs(html)), (
        "the founder card action leads to no /download route")
    for recurring in ("per month", "/month", "per year", "/year", "billed annually",
                      "billed monthly"):
        assert recurring not in body.lower(), (
            f"the pricing section reads {recurring!r}, and the published pricing is "
            f"one-time")

    for number, question in enumerate(HELP_QUESTIONS, start=1):
        assert question in body, (
            f"the help panel never asks question {number:02d} {question!r}")
        assert re.search(rf'id=["\']faq-{number:02d}["\']', html), (
            f"the help item {number:02d} carries no faq-{number:02d} identifier")
    order = [body.index(question) for question in HELP_QUESTIONS]
    assert order == sorted(order), (
        f"the help questions are out of the pinned order: {order}")
    for chip in ("Privacy", "Pricing", "Beta", "Platform"):
        assert chip in body, f"the help panel never offers the category chip {chip!r}"
    triggers = re.findall(r"<h[2-6][^>]*>\s*<button\b[^>]*aria-expanded", html, re.I)
    assert len(triggers) >= len(HELP_QUESTIONS), (
        f"{len(triggers)} help triggers are buttons inside a heading with an expanded "
        f"state, expected {len(HELP_QUESTIONS)}")
    answer = section_after(html, HELP_QUESTIONS[7]) or html
    for app in ("Chatwell", "Cadence", "Vertan", "Caret"):
        assert app in text_of(answer), (
            f"help answer 08 never names the destination application {app!r}")


def test_site_chrome_carries_the_navigation_and_footer_copy():
    """Every route ships the capsule links, the skip link and the four footer columns."""
    footer_items = {
        "Product": ("Features", "Workflow", "Beta", "Use cases", "Changelog", "Roadmap"),
        "Resources": ("FAQ", "Blog", "Templates", "Version history", "Join beta"),
        "Company": ("Contact", "Privacy", "Terms", "Press"),
    }
    for path in ("/", "/download", "/changelog", "/press", "/privacy"):
        html = page_html(path).text
        body = text_of(html)
        for label in ("Product", "Workflow", "Use cases", "Pricing", "Blog", "FAQ"):
            assert label in body, (
                f"{path} never carries the navigation link {label!r}")
        assert "Join beta" in body, f"{path} never carries the Join beta action"
        assert "Skip to content" in body, f"{path} carries no skip link"
        for column, items in footer_items.items():
            assert column in body, f"{path} carries no footer column {column!r}"
            for item in items:
                assert item in body, (
                    f"the footer of {path} never lists {item!r} under {column}")
        sign = chr(169)
        assert ("(c) 2026 Halyard Labs" in body
                or f"{sign} 2026 Halyard Labs" in body), (
            f"the footer base line of {path} never reads the pinned copyright: "
            f"{body[-300:]}")
        assert ("Lumen Prompt is not affiliated with Northgate, Bellweather or "
                "Halcyon.") in body, (
            f"the footer of {path} carries no affiliation disclaimer")
        targets = {internal_path(href) for href in hrefs(html)}
        for route in ("/privacy", "/terms", "/use-cases/reusable-ai-prompt-templates",
                      "/use-cases/prompt-version-history"):
            assert route in targets, (
                f"the footer of {path} links to none of the pinned route {route}")
        canonical = canonical_of(html)
        assert canonical and (urlparse(canonical).path or "/").rstrip("/") == (
            path.rstrip("/") or "/"), (
            f"{path} canonicalises to {canonical!r}, expected itself")


def test_download_page_carries_the_form_and_the_distribution_panel():
    """The registration form and the panel read from the registry, without scripting."""
    response = page_html("/download")
    assert response.status_code == 200, (
        f"GET /download returned {response.status_code}: {response.text[:200]}")
    html = response.text
    body = text_of(html)
    stable = [row for row in releases() if str(row["status"]) == "published"][0]

    for chip in ("Free during beta", "No card required", "Open registration",
                 "Founder pricing before 1.0"):
        assert chip in body, f"/download never shows the confirmation chip {chip!r}"
    assert "Official distribution" in body, (
        "the distribution panel carries no Official distribution heading")
    assert ("Signed and notarised binary; update feed signed with a separate "
            "key") in body, (
        f"the distribution panel never states its verification claim: {body[:400]}")
    for label in ("Current version", "Verification", "Download route", "Update feed",
                  "Requirements", "Checksum"):
        assert label in body, f"the distribution panel carries no {label!r} row"
    assert str(stable["version"]) in body, (
        f"the distribution panel never shows the current stable "
        f"{stable['version']}, so it is not read from the registry")
    assert str(stable["build"]) in body, (
        f"the distribution panel never shows the current build {stable['build']}")
    assert f"macOS {stable['min_os']} or later" in body, (
        f"the distribution panel never states the requirement macOS "
        f"{stable['min_os']} or later")
    assert str(stable["sha256"])[:8] in body, (
        f"the distribution panel never shows the checksum of {stable['version']}")
    for route in ("/downloads/latest", "/appcast.xml"):
        assert route in body, (
            f"the distribution panel never names the route {route}")
    assert any(internal_path(href) == "/changelog" for href in hrefs(html)), (
        "the distribution panel links to no changelog")

    steps = [block for block in re.findall(r"<ol\b[^>]*>(.*?)</ol>", html,
                                           flags=re.S | re.I)
             if len(re.findall(r"<li\b", block, re.I)) == 4]
    assert steps, (
        "the four-step explainer is not a numbered list of exactly four steps")

    fields = input_tags(html)
    trap = [tag for tag in fields if tag.get("name") == "company_website"]
    assert trap, "the form carries no company_website trap field"
    assert trap[0].get("tabindex") == "-1", (
        f"the trap field carries tabindex {trap[0].get('tabindex')!r}, expected -1 so "
        f"no keyboard reaches it")
    assert "aria-hidden" in trap[0], (
        f"the trap field is not hidden from assistive technology: {trap[0]}")
    email_field = [tag for tag in fields if tag.get("type", "").lower() == "email"]
    assert email_field, "the form carries no email field of type email"
    assert "required" in email_field[0], (
        f"the email field is not marked required: {email_field[0]}")
    assert email_field[0].get("autocomplete", "").startswith("email"), (
        f"the email field carries autocomplete {email_field[0].get('autocomplete')!r}, "
        f"expected an email autofill hint")
    assert email_field[0].get("spellcheck", "").lower() == "false", (
        f"the email field carries spellcheck {email_field[0].get('spellcheck')!r}, "
        f"expected false")
    consent = [tag for tag in fields if tag.get("type", "").lower() == "checkbox"]
    assert consent and "required" in consent[0], (
        f"the consent checkbox is not marked required: {consent[:1]}")
    placeholders = {tag.get("placeholder") for tag in fields}
    for placeholder in ("Optional", "Consultant, researcher or engineer",
                        "Client briefs, code review or research notes"):
        assert placeholder in placeholders, (
            f"the form carries no field with the placeholder {placeholder!r}: "
            f"{sorted(p for p in placeholders if p)}")
    options = [text_of(one) for one in
               re.findall(r"<option\b[^>]*>(.*?)</option>", html, flags=re.S | re.I)]
    for option in ("Not sure", "macOS 26.1", "macOS 26.2", "macOS 26.3", "macOS 27"):
        assert option in options, (
            f"the platform select never offers {option!r}: {options[:8]}")
    for sentence in (
        "Send me my beta access link and occasional beta updates at this address. "
        "I have read the privacy policy.",
        "Join the beta",
        "One email with your link. No newsletter.",
        "If no build is ready when you open your link, the page confirms your "
        "registration and we email you when the first build ships.",
    ):
        assert sentence in body, (
            f"/download never carries the pinned copy {sentence!r}")
    assert ld_types(html) & {"SoftwareApplication"}, (
        f"/download carries no SoftwareApplication structured data: "
        f"{sorted(ld_types(html))}")


def test_use_case_index_and_pages_carry_their_pinned_copy():
    """The five cards, the radial diagram and each acquisition page read as pinned."""
    index = page_html("/use-cases")
    assert index.status_code == 200, (
        f"GET /use-cases returned {index.status_code}: {index.text[:200]}")
    index_body = text_of(index.text)
    cards = (
        ("Reusable templates", "reusable prompt templates"),
        ("Time Machine", "prompt version history"),
        ("Mac prompt manager", "prompt manager for Mac"),
        ("Local-first", "local-first prompt library"),
        ("Hotkey launcher", "prompt launcher for Mac"),
    )
    for eyebrow, title in cards:
        assert eyebrow in index_body, (
            f"/use-cases never shows the card eyebrow {eyebrow!r}")
        assert title.lower() in index_body.lower(), (
            f"/use-cases never shows the card title {title!r}")
    for label in ("Client briefs", "Code reviews", "Research notes"):
        assert label in index_body, (
            f"the radial diagram never carries the label {label!r}")
    index_targets = [internal_path(href) for href in hrefs(index.text)]
    for route, _eyebrow, _heading in USE_CASE_PAGES:
        assert index_targets.count(route) >= 2, (
            f"/use-cases links to {route} {index_targets.count(route)} times, expected "
            f"the card and the diagram node")

    disclaimer = ("The visual language follows the running application, but the content "
                  "is purpose-built synthetic marketing data, not real workspace text.")
    for route, eyebrow, heading in USE_CASE_PAGES:
        response = page_html(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}: {response.text[:200]}")
        html = response.text
        body = text_of(html)
        first_level = [text for level, text in heading_pairs(html) if level == 1]
        assert first_level == [heading], (
            f"{route} carries the first-level heading(s) {first_level}, expected only "
            f"{heading!r}")
        assert eyebrow in body, f"{route} never shows its eyebrow {eyebrow!r}"
        for column in ("Without Lumen Prompt", "With Lumen Prompt"):
            assert column in body, (
                f"{route} carries no contrast column headed {column!r}")
        assert disclaimer in body, (
            f"{route} carries no synthetic-data disclaimer: {body[:300]}")
        assert "Demonstration data" in body, (
            f"the mockup on {route} carries no demonstration-data label")
        assert {"BreadcrumbList", "FAQPage"} <= ld_types(html), (
            f"{route} carries the structured data {sorted(ld_types(html))}, expected "
            f"BreadcrumbList with FAQPage")
        canonical = canonical_of(html)
        assert canonical and urlparse(canonical).path.rstrip("/") == route, (
            f"{route} canonicalises to {canonical!r}, expected itself rather than the "
            f"index")
        related = section_after(html, "Related use cases")
        assert related, f"{route} carries no Related use cases section"
        neighbours = {internal_path(href) for href in hrefs(related)}
        others = {other for other, _e, _h in USE_CASE_PAGES if other != route}
        assert others <= neighbours, (
            f"the Related use cases section of {route} links {sorted(n for n in neighbours if n)}, "
            f"expected the other four pages")
        assert route not in neighbours, (
            f"the Related use cases section of {route} links back to the page itself")


def test_changelog_projects_the_release_registry():
    """The changelog shows the stable block, the earlier releases and the revoked one."""
    response = page_html("/changelog")
    assert response.status_code == 200, (
        f"GET /changelog returned {response.status_code}: {response.text[:200]}")
    html = response.text
    body = text_of(html)
    assert "no-store" in str(response.headers.get("cache-control", "")).lower(), (
        f"GET /changelog carries Cache-Control "
        f"{response.headers.get('cache-control')!r}, expected no-store so a publish or "
        f"a revoke shows on the next request")
    assert ("Release notes are linked from each version, so this page and the in-app "
            "updater share one source of truth.") in body, (
        f"/changelog carries no pinned sub-heading: {body[:300]}")
    rows = releases()
    stable = [row for row in rows if str(row["status"]) == "published"][0]
    assert str(stable["version"]) in body, (
        f"/changelog never shows the current stable {stable['version']}")
    assert str(stable["summary"]) in body, (
        f"/changelog never shows the summary of {stable['version']}")
    assert str(stable["sha256"]) in body, (
        f"/changelog never shows the full checksum of {stable['version']}")
    assert str(stable["download_count"]) in body, (
        f"/changelog never shows the recorded download count of {stable['version']}")
    assert "Download" in body and "Read the notes" in body, (
        f"the current stable block offers no Download with Read the notes: {body[:400]}")
    assert re.search(r"<video\b[^>]*poster=", html, re.I), (
        "the current stable block carries no release film with a poster image")
    targets = {internal_path(href) for href in hrefs(html)}
    assert f"/release-notes/{stable['version']}" in targets, (
        f"/changelog links to no notes for {stable['version']}")
    assert "/downloads/latest" in targets, (
        "/changelog offers no download of the current stable release")
    for row in rows:
        version = str(row["version"])
        assert version in body, f"/changelog never shows the release {version}"
        assert str(row["summary"]) in body, (
            f"/changelog never shows the summary of {version}")
        if str(row["status"]) == "published" and version != str(stable["version"]):
            assert str(row["sha256"])[:8] in body, (
                f"/changelog shows no truncated checksum for the earlier {version}")
            assert f"/release-notes/{version}" in targets, (
                f"/changelog links to no notes for the earlier {version}")
    assert REVOKED_NOTICE in body, (
        f"/changelog never shows the revoked notice for release 0.2.0: {body[:300]}")
    assert str(release("0.2.0")["download_url"]) not in html, (
        "/changelog still offers the download of the revoked 0.2.0")


def test_roadmap_and_blog_pages_carry_their_pinned_copy():
    """The three buckets carry eleven dateless items and the index is newest first."""
    roadmap = page_html("/roadmap")
    assert roadmap.status_code == 200, (
        f"GET /roadmap returned {roadmap.status_code}: {roadmap.text[:200]}")
    body = text_of(roadmap.text)
    for bucket, label in (("Now", "Active in the current open beta"),
                          ("Next", "Coming before 1.0"),
                          ("Later", "Planned for 1.0 and beyond")):
        assert bucket in body, f"/roadmap carries no {bucket!r} bucket"
        assert label in body, f"the {bucket!r} bucket carries no label {label!r}"
    items = ("Open beta hardening", "Version-history refinements",
             "Context workflow polish", "Injection history",
             "Organisation improvements", "Variable memory per Blueprint",
             "Founder-terms finalisation", "Release polish", "The 1.0 release",
             "Sharing and export", "Deeper injection options")
    for item in items:
        assert item in body, f"/roadmap never lists the item {item!r}"
    assert "Order and scope change with beta feedback." in body, (
        f"/roadmap carries no caveat: {body[:300]}")
    assert not re.search(r"\b\d{1,3}\s*%|\b20\d\d-\d\d-\d\d\b", body), (
        f"/roadmap shows a date or a percentage: {body[:300]}")
    assert not re.search(r"<progress\b", roadmap.text, re.I), (
        "/roadmap renders a progress bar")
    scoped = section_after(roadmap.text, "Variable memory per Blueprint") or roadmap.text
    assert "per Blueprint" in text_of(scoped), (
        "the variable-memory item never states per-Blueprint scoping")
    assert "account" in body.lower() and "server" in body.lower(), (
        f"the sharing item never states that sharing needs no account layer or shared "
        f"server: {body[:300]}")

    index = page_html("/blog")
    assert index.status_code == 200, (
        f"GET /blog returned {index.status_code}: {index.text[:200]}")
    index_body = text_of(index.text)
    first = "Stop rewriting your best prompt"
    second = "Prompts are work product"
    assert first in index_body and second in index_body, (
        f"/blog never lists both articles: {index_body[:300]}")
    assert index_body.index(first) < index_body.index(second), (
        "/blog lists the older article above the newer one")
    for category in ("Workflow", "Essay"):
        assert category in index_body, (
            f"/blog never shows the category {category!r}")
    for date in ("2026-08-20", "2026-07-30"):
        assert date in index.text, (
            f"/blog never carries the article date {date}")
    assert len(re.findall(r"min read", index_body)) >= 2, (
        f"/blog shows no reading time on each card: {index_body[:300]}")

    for route in ARTICLE_ROUTES:
        article = page_html(route)
        assert article.status_code == 200, (
            f"GET {route} returned {article.status_code}: {article.text[:200]}")
        article_body = text_of(article.text)
        assert "min read" in article_body, (
            f"{route} shows no reading time")
        others = [other for other in ARTICLE_ROUTES if other != route]
        targets = {internal_path(href) for href in hrefs(article.text)}
        assert set(others) <= targets, (
            f"{route} links to no related article: {sorted(t for t in targets if t)[:8]}")
        assert not re.search(r"<video\b", article.text, re.I), (
            f"{route} carries a mockup or instrument, and the articles carry none")


def test_press_contact_and_legal_pages_carry_their_pinned_copy():
    """The press kit, the single address and the two legal pages read as pinned."""
    press = page_html("/press")
    assert press.status_code == 200, (
        f"GET /press returned {press.status_code}: {press.text[:200]}")
    press_html = press.text
    press_body = text_of(press_html)
    assert "Download the press kit (48 MB)" in press_body, (
        f"/press never states the press kit size before the click: {press_body[:300]}")
    assert "https://downloads.example.com/lumen-prompt/press-kit.zip" in press_html, (
        "/press points at no press kit archive on the asset host")
    for row in ("Name", "One-liner", "Platform and distribution", "Status",
                "Developer", "Contact", "Site"):
        assert row in press_body, f"the press fact sheet carries no {row!r} row"
    for fact in ("macOS 26.1 or later", "direct download", "open beta", "$29", "$39",
                 "Halyard Labs", "Devrim"):
        assert fact in press_body, (
            f"the press fact sheet never states {fact!r}")
    figures = re.findall(r"<figure\b.*?</figure>", press_html, flags=re.S | re.I)
    captioned = [figure for figure in figures
                 if re.search(r"<figcaption\b", figure, re.I)
                 and re.search(r"<img\b", figure, re.I)]
    assert len(captioned) >= 23, (
        f"/press carries {len(captioned)} captioned captures, expected at least the "
        f"twenty-three the brief pins")
    for figure in captioned:
        caption = text_of(re.search(r"<figcaption\b[^>]*>(.*?)</figcaption>", figure,
                                    flags=re.S | re.I).group(1)).strip()
        image = input_tags(figure.replace("<img", "<input"))
        attrs = image[0] if image else {}
        assert attrs.get("alt", "").strip() == caption, (
            f"a capture's alternative text is {attrs.get('alt')!r} while its caption "
            f"reads {caption!r}; the caption is reused as the alternative text")
        assert attrs.get("width") and attrs.get("height"), (
            f"the capture {caption!r} carries no explicit dimensions, so the page "
            f"shifts as it loads")
    assert len(re.findall(r"<source\b[^>]*type=[\"']image/(?:avif|webp)", press_html,
                          re.I)) >= 23, (
        "the captures ship in no modern image format with a fallback")
    lazy = re.findall(r"<img\b[^>]*loading=[\"']lazy[\"']", press_html, re.I)
    assert len(lazy) >= len(captioned) - 3, (
        f"{len(lazy)} of {len(captioned)} captures load lazily, so the page below the "
        f"fold is not deferred")
    videos = re.findall(r"<video\b[^>]*>", press_html, re.I)
    assert len(videos) >= 2, (
        f"/press carries {len(videos)} motion loops, expected the two the brief pins")
    for video in videos:
        assert "muted" in video.lower(), f"a press motion loop is not muted: {video}"
        assert "poster=" in video.lower(), (
            f"a press motion loop carries no poster frame: {video}")
        assert re.search(r"preload=[\"']none[\"']", video, re.I), (
            f"a press motion loop preloads: {video}")
    for heading in ("You may", "You may not"):
        assert heading in press_body, (
            f"the usage guidelines carry no visible {heading!r} heading")

    contact = page_html("/contact")
    assert contact.status_code == 200, (
        f"GET /contact returned {contact.status_code}: {contact.text[:200]}")
    contact_body = text_of(contact.text)
    assert ("Beta questions, support, privacy requests and press all reach a person at "
            "one address.") in contact_body, (
        f"/contact carries no pinned one-address sentence: {contact_body[:300]}")
    assert SUPPORT_EMAIL in contact_body, (
        f"/contact never shows {SUPPORT_EMAIL} as selectable text")
    mail_links = [href for href in hrefs(contact.text) if href.startswith("mailto:")]
    assert mail_links, "/contact carries no mail link"
    target = unquote(mail_links[0])
    assert SUPPORT_EMAIL in target, (
        f"the contact mail link points at {target[:80]!r}")
    assert "Lumen Prompt support" in target, (
        f"the contact mail link carries no pinned subject: {target[:120]}")
    for blank in ("macOS version:", "Lumen Prompt version:"):
        assert blank in target, (
            f"the contact mail link carries no {blank!r} blank: {target[:160]}")

    legal = {
        "/privacy": ("what-the-website-stores", "what-never-leaves-your-mac",
                     "access-links-and-sessions", "processors", "analytics",
                     "your-rights", "contact"),
        "/terms": ("the-beta", "founder-licences", "updates-and-signing",
                   "acceptable-use", "liability", "contact"),
    }
    for route, identifiers in legal.items():
        response = page_html(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}: {response.text[:200]}")
        html = response.text
        for identifier in identifiers:
            assert re.search(rf'id=["\']{identifier}["\']', html), (
                f"{route} carries no heading with the identifier {identifier!r}")
        contents = {internal_path(href) or href for href in hrefs(html)}
        assert any(str(href).startswith("#") for href in hrefs(html)), (
            f"{route} carries no generated table of contents")
        if route == "/privacy":
            body = text_of(html)
            assert "fourteen days" in body.lower() or "14 days" in body.lower(), (
                f"/privacy never states how long an access session lasts: {body[:300]}")
            assert "analytics" in body.lower(), (
                "/privacy never states that no analytics load")
            assert "/legal/data-request" in contents, (
                f"the privacy rights section links to none of {sorted(str(c) for c in contents)[:8]}")


def test_no_backend_secret_appears_in_anything_the_browser_downloads():
    """No provider credential reaches the markup or the bundles it loads."""
    blobs = []
    for path in ("/", "/download", "/operator"):
        response = page_html(path)
        assert response.status_code == 200, (
            f"GET {path} returned {response.status_code}: {response.text[:200]}")
        blobs.append(response.text)
        assets = re.findall(r'<script\b[^>]*\bsrc=["\']([^"\']+)["\']', response.text, re.I)
        assets += re.findall(r'<link\b[^>]*\bhref=["\']([^"\']+\.css[^"\']*)["\']',
                             response.text, re.I)
        for asset in sorted(set(assets)):
            target = internal_path(asset)
            if not target:
                continue
            fetched = page_html(asset)
            assert fetched.status_code < 400, (
                f"the asset {asset} referenced by {path} answers "
                f"{fetched.status_code}")
            blobs.append(fetched.text)
    joined = "\n".join(blobs)
    secrets = backend_secrets()
    assert secrets, (
        "this run configured no provider credential, so the leak check would prove "
        "nothing")
    for secret in secrets:
        assert secret not in joined, (
            f"the credential {secret[:6]}... reaches the browser in the markup or an "
            f"asset it downloads")
    assert PASSWORD not in joined, (
        "the seeded password reaches the browser in the markup or an asset")


def test_no_public_route_offers_a_file_upload():
    """Nothing on the site accepts a file, because nothing here stores one."""
    for path in list(CONTENT_ROUTES) + list(ARTICLE_ROUTES) + ["/legal/data-request",
                                                              "/beta/status"]:
        response = page_html(path)
        assert response.status_code == 200, (
            f"GET {path} returned {response.status_code}: {response.text[:200]}")
        uploads = [tag for tag in input_tags(response.text)
                   if tag.get("type", "").lower() == "file"]
        assert not uploads, (
            f"{path} offers a file upload: {uploads[:1]}")
        assert "multipart/form-data" not in response.text, (
            f"{path} carries a form that accepts a file body")


def test_page_text_meets_the_contrast_bars(page):
    """Composited text clears 4.5:1, primary text on the ground clears 7:1."""
    script = composite_contrast_script()
    for path in ("/", "/download", "/changelog", "/press", "/use-cases"):
        page.goto(path)
        page.wait_for_load_state("networkidle")
        rows = page.evaluate(script, "main p, main li, main td, main dd, main label, "
                                     "main figcaption, footer p, footer li")
        assert rows, f"{path} rendered no body text to measure"
        weak = [row for row in rows if row["ratio"] < 4.45]
        assert not weak, (
            f"{len(weak)} text run(s) on {path} sit under 4.5:1 against the background "
            f"actually behind them, the worst being {weak[0]['text']!r} at "
            f"{weak[0]['ratio']:.2f}")
    page.goto("/")
    page.wait_for_load_state("networkidle")
    primary = page.evaluate(script, "main h1, main h2, main h3")
    dim = [row for row in primary if row["ratio"] < 6.9]
    assert not dim, (
        f"{len(dim)} heading(s) on the home route sit under 7:1 on the page ground, "
        f"the worst being {dim[0]['text']!r} at {dim[0]['ratio']:.2f}")
    page.goto("/download")
    page.wait_for_load_state("networkidle")
    holders = page.evaluate(placeholder_contrast_script(), "input, textarea")
    assert holders, "the registration form renders no placeholder text to measure"
    faint = [row for row in holders if row["ratio"] < 2.95]
    assert not faint, (
        f"the placeholder {faint[0]['text']!r} sits at {faint[0]['ratio']:.2f}, under "
        f"the 3:1 bar")


def test_page_typography_uses_the_pinned_family_and_sizes(page):
    """One downloaded family, the pinned body metrics and a bounded size set."""
    page.goto("/")
    page.wait_for_load_state("networkidle")
    faces = page.evaluate(
        "async () => { await document.fonts.ready; "
        "return [...document.fonts].map(f => ({family: f.family.replace(/[\"']/g, ''), "
        "weight: String(f.weight), display: String(f.display)})); }")
    assert faces, "the home route downloads no font face at all"
    families = {face["family"] for face in faces}
    assert all(family.startswith("IBM Plex Mono") for family in families), (
        f"the site downloads the families {sorted(families)}, and IBM Plex Mono is the "
        f"only downloaded family")
    covered = set()
    for face in faces:
        numbers = [int(token) for token in re.findall(r"\d+", face["weight"])]
        if len(numbers) == 1:
            covered.add(numbers[0])
        elif len(numbers) > 1:
            covered.update(value for value in (400, 500, 600)
                           if numbers[0] <= value <= numbers[-1])
    for wanted in (400, 500, 600):
        assert wanted in covered, (
            f"IBM Plex Mono ships the weights {sorted(covered)}, missing {wanted}")
    assert all(face["display"] == "swap" for face in faces), (
        f"a downloaded face sets font-display "
        f"{sorted({face['display'] for face in faces})}, expected swap so text is never "
        f"invisible while it loads")

    body_font = page.evaluate("() => getComputedStyle(document.body).fontFamily")
    assert "IBM Plex Mono" not in body_font.split(",")[0], (
        f"body prose is set in {body_font!r}, and body prose is never monospace")
    metrics = page.evaluate(
        "() => { const p = document.querySelector('main p'); const s = getComputedStyle(p); "
        "return [s.fontSize, s.lineHeight]; }")
    assert metrics == ["16px", "24px"], (
        f"body prose renders at {metrics}, expected 16px on a 24px line height")
    sizes = page.evaluate(
        "() => { const out = new Set(); "
        "for (const el of document.querySelectorAll('body *')) { "
        "if (['INPUT','SELECT','TEXTAREA','OPTION','SCRIPT','STYLE','SVG'].includes(el.tagName)) continue; "
        "if (el.closest('[aria-hidden=\"true\"]')) continue; "
        "const direct = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()); "
        "if (!direct) continue; const r = el.getBoundingClientRect(); "
        "if (!r.width || !r.height) continue; "
        "out.add(parseFloat(getComputedStyle(el).fontSize)); } return [...out]; }")
    below = sorted({size for size in sizes if size < 24})
    stray = [size for size in below if size not in TYPE_SIZES_BELOW_DISPLAY]
    assert not stray, (
        f"the home route renders text at {stray} below display size, outside the "
        f"pinned scale {list(TYPE_SIZES_BELOW_DISPLAY)}")

    eyebrow = page.evaluate(
        "() => { const el = [...document.querySelectorAll('main *')].find(e => "
        "[...e.childNodes].some(n => n.nodeType === 3 && "
        "n.textContent.trim().toLowerCase() === 'command flow')); if (!el) return null; "
        "const s = getComputedStyle(el); return {size: parseFloat(s.fontSize), "
        "weight: s.fontWeight, transform: s.textTransform, "
        "spacing: s.letterSpacing === 'normal' ? 0 : parseFloat(s.letterSpacing)}; }")
    assert eyebrow, "the Command flow eyebrow renders nowhere on the home route"
    assert eyebrow["size"] == 11.0, (
        f"the eyebrow renders at {eyebrow['size']}px, expected 11px")
    assert str(eyebrow["weight"]) == "700", (
        f"the eyebrow renders at weight {eyebrow['weight']}, expected 700")
    tracked = page.evaluate(
        "() => { const bad = []; for (const el of document.querySelectorAll('body *')) { "
        "const s = getComputedStyle(el); "
        "const direct = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()); "
        "if (!direct) continue; if (s.textTransform !== 'uppercase') continue; "
        "if (parseFloat(s.fontSize) >= 13) continue; "
        "const ls = s.letterSpacing === 'normal' ? 0 : parseFloat(s.letterSpacing); "
        "if (!(ls > 0)) bad.push(el.textContent.trim().slice(0, 30)); } return bad; }")
    assert not tracked, (
        f"the uppercase label(s) {tracked[:3]} render below 13px with no open letter "
        f"spacing")

    wide = page.evaluate(
        "() => parseFloat(getComputedStyle(document.querySelector('h1')).fontSize)")
    page.set_viewport_size({"width": 390, "height": 844})
    narrow = page.evaluate(
        "() => parseFloat(getComputedStyle(document.querySelector('h1')).fontSize)")
    assert narrow < wide, (
        f"the hero headline renders at {narrow}px at phone width and {wide}px at "
        f"desktop width, so display type does not scale with the viewport")
    disclaimer = page.evaluate(
        "() => { const el = [...document.querySelectorAll('footer *')].find(e => "
        "(e.textContent || '').includes('not affiliated with Northgate')); "
        "return el ? parseFloat(getComputedStyle(el).fontSize) : null; }")
    assert disclaimer and disclaimer >= 12, (
        f"the affiliation disclaimer renders at {disclaimer}px, under the 12px floor")


def test_page_command_palette_lists_blueprints_then_destinations(page):
    """The palette opens on the shortcut with the pinned contents and semantics."""
    calls = []
    page.on("request", lambda request: calls.append(request.method))
    page.goto("/", wait_until="domcontentloaded")
    page.keyboard.press("Control+k")
    box = page.get_by_role("combobox").first
    expect(box).to_be_visible(timeout=15000)
    assert box.get_attribute("aria-expanded") == "true", (
        f"the palette input reports aria-expanded "
        f"{box.get_attribute('aria-expanded')!r}, expected true")
    assert box.get_attribute("aria-autocomplete") == "list", (
        f"the palette input reports aria-autocomplete "
        f"{box.get_attribute('aria-autocomplete')!r}, expected list")
    controls = box.get_attribute("aria-controls")
    assert controls and page.locator(f'[id="{controls}"]').count() == 1, (
        f"the palette input controls {controls!r}, which resolves to no single element")
    active = box.get_attribute("aria-activedescendant")
    assert active, "the palette input points at no active option"
    active_text = page.locator(f'[id="{active}"]').inner_text()
    assert PALETTE_BLUEPRINTS[0][0] in active_text, (
        f"the initial active option reads {active_text[:60]!r}, expected the first "
        f"Blueprint {PALETTE_BLUEPRINTS[0][0]!r}")
    assert (box.get_attribute("spellcheck") or "").lower() == "false", (
        f"the palette input carries spellcheck {box.get_attribute('spellcheck')!r}")
    assert (box.get_attribute("autocomplete") or "").lower() in ("off", "none"), (
        f"the palette input carries autocomplete {box.get_attribute('autocomplete')!r}")

    dialog = page.get_by_role("dialog").first
    labelled = dialog.get_attribute("aria-labelledby") or dialog.get_attribute("aria-label")
    assert labelled, "the palette dialog carries no accessible name"
    options = page.get_by_role("option")
    texts = options.all_inner_texts()
    assert len(texts) == 22, (
        f"the palette lists {len(texts)} entries, expected five Blueprints and "
        f"seventeen destinations")
    for index, (title, category) in enumerate(PALETTE_BLUEPRINTS):
        assert title in texts[index], (
            f"palette entry {index} reads {texts[index][:60]!r}, expected the Blueprint "
            f"{title!r} in the pinned order")
        assert category in texts[index].upper(), (
            f"the Blueprint {title!r} shows the category "
            f"{texts[index][:60]!r}, expected {category!r}")
        assert "{{" in texts[index], (
            f"the Blueprint {title!r} shows no double-brace variable in its body")
    assert any("Release notes 0.2.3" in text for text in texts[5:]), (
        f"the destinations group never offers Release notes 0.2.3: {texts[5:8]}")
    assert "Inject" in dialog.inner_text(), (
        f"the palette footer hint never uses the verb Inject: "
        f"{dialog.inner_text()[-200:]!r}")
    inert = page.evaluate(
        "() => { const m = document.querySelector('main'); return !!(m && "
        "(m.closest('[inert]') || m.closest('[aria-hidden=\"true\"]') || "
        "m.hasAttribute('inert') || m.getAttribute('aria-hidden') === 'true')); }")
    assert inert, (
        "the page behind the open palette is not inert, so assistive technology and "
        "the Tab key walk straight past the panel edge")

    before = len(calls)
    page.keyboard.press("Enter")
    settle(1.0)
    sent = [method for method in calls[before:] if method != "GET"]
    assert not sent, (
        f"activating a palette Blueprint sent {sent}, and the demonstration sends "
        f"nothing anywhere")
    assert urlparse(page.url).path == "/", (
        f"activating a Blueprint navigated to {page.url}, expected a scroll inside the "
        f"home route")


def test_page_command_palette_keyboard_and_search_behave(page):
    """Arrows wrap, Escape returns focus, search ranks and marks its matches."""
    page.goto("/")
    page.wait_for_load_state("networkidle")
    trigger = page.get_by_role("link", name="Product", exact=True).first
    trigger.focus()
    page.keyboard.press("Control+k")
    box = page.get_by_role("combobox").first
    expect(box).to_be_visible(timeout=15000)
    options = page.get_by_role("option")
    total = options.count()
    assert total == 22, f"the palette lists {total} entries, expected 22"
    page.keyboard.press("ArrowUp")
    last = box.get_attribute("aria-activedescendant")
    assert PALETTE_BLUEPRINTS[0][0] not in page.locator(f'[id="{last}"]').inner_text(), (
        "ArrowUp from the first option does not wrap to the end of the list")
    page.keyboard.press("ArrowDown")
    first = box.get_attribute("aria-activedescendant")
    assert PALETTE_BLUEPRINTS[0][0] in page.locator(f'[id="{first}"]').inner_text(), (
        "ArrowDown from the last option does not wrap back to the first Blueprint")
    for _step in range(4):
        page.keyboard.press("Tab")
    trapped = page.evaluate(
        "() => { const d = document.querySelector('[role=dialog]'); "
        "return !!(d && d.contains(document.activeElement)); }")
    assert trapped, "Tab leaves the open palette, so focus is not trapped inside it"

    box.fill("re")
    settle(1.0)
    ranked = page.get_by_role("option").all_inner_texts()
    assert ranked, "a palette query matching several entries shows nothing"
    joined = " | ".join(ranked)
    assert "Research synthesis" in joined and "Release notes draft" in joined, (
        f"the query 're' never offers the Blueprints whose titles start with it: "
        f"{ranked[:4]}")
    if "Code review checklist" in joined:
        exact = min(joined.index("Research synthesis"), joined.index("Release notes draft"))
        assert exact < joined.index("Code review checklist"), (
            f"a title prefix ranks below a word prefix inside the Blueprints group: "
            f"{ranked[:5]}")
    assert page.locator("[role=option] mark").count() > 0, (
        "a palette search wraps no matched run in a mark element")

    box.fill("OPERATIONS")
    settle(1.0)
    assert any("Meeting follow-up" in text for text in
               page.get_by_role("option").all_inner_texts()), (
        "a palette search over categories never finds the OPERATIONS Blueprint")
    box.fill("style_guide")
    settle(1.0)
    assert any("Code review checklist" in text for text in
               page.get_by_role("option").all_inner_texts()), (
        "a palette search over Blueprint bodies never finds the double-brace variable")
    box.fill(f"zzq{os.urandom(3).hex()}")
    settle(1.0)
    assert page.get_by_role("option").count() == 0, (
        "a palette query matching nothing still lists entries")
    empty = page.get_by_role("dialog").first
    targets = empty.locator("a[href]").evaluate_all(
        "nodes => nodes.map(n => new URL(n.href).pathname)")
    assert "/download" in targets and "/contact" in targets, (
        f"the empty palette state offers {targets}, expected /download with /contact")
    box.fill("")
    settle(1.0)
    assert page.get_by_role("option").count() == 22, (
        f"an empty query lists {page.get_by_role('option').count()} entries, expected "
        f"the full list of 22")

    page.keyboard.press("Escape")
    expect(page.get_by_role("combobox").first).to_be_hidden(timeout=10000)
    returned = trigger.evaluate("node => node === document.activeElement")
    assert returned, "closing the palette does not return focus to its trigger"

    field = page.get_by_role("link", name="Blog", exact=True).first
    field.click()
    page.wait_for_url("**/blog", timeout=15000)
    page.keyboard.press("/")
    expect(page.get_by_role("combobox").first).to_be_visible(timeout=10000)
    page.keyboard.press("Escape")
    page.goto("/download")
    page.wait_for_load_state("networkidle")
    email_box = page.locator("input[type=email]").first
    email_box.click()
    page.keyboard.type("/")
    assert page.get_by_role("dialog").count() == 0 or not page.get_by_role(
        "dialog").first.is_visible(), (
        "a forward slash typed inside a text field opened the palette")
    assert "/" in email_box.input_value(), (
        f"the slash never reached the field: {email_box.input_value()!r}")


def test_page_narrow_viewport_holds_and_the_menu_opens(page):
    """Nothing overflows sideways and the six links collapse into a menu dialog."""
    page.set_viewport_size({"width": 390, "height": 844})
    for path in ("/", "/download", "/changelog", "/release-notes/0.2.3", "/press",
                 "/use-cases"):
        page.goto(path)
        page.wait_for_load_state("networkidle")
        overflow = page.evaluate(
            "() => document.documentElement.scrollWidth - "
            "document.documentElement.clientWidth")
        assert overflow <= 1, (
            f"{path} overflows sideways by {overflow}px at a 390px viewport")
    page.goto("/")
    page.wait_for_load_state("networkidle")
    menu = page.get_by_role("button", name=re.compile("menu", re.I)).first
    expect(menu).to_be_visible(timeout=10000)
    menu.click()
    dialog = page.get_by_role("dialog").first
    expect(dialog).to_be_visible(timeout=10000)
    for label in ("Product", "Workflow", "Use cases", "Pricing", "Blog", "FAQ"):
        expect(dialog.get_by_text(label, exact=True).first).to_be_visible(timeout=10000)
    searchable = dialog.get_by_text(re.compile("search", re.I)).count()
    assert searchable > 0, (
        "the small-width menu carries no labelled search entry, so a visitor without "
        "the key cap loses the palette entirely")
    inert = page.evaluate(
        "() => { const m = document.querySelector('main'); return !!(m && "
        "(m.closest('[inert]') || m.hasAttribute('inert') || "
        "m.getAttribute('aria-hidden') === 'true')); }")
    assert inert, "the page behind the open menu is not inert"
    before = page.evaluate("() => window.scrollY")
    page.mouse.wheel(0, 600)
    settle(1.0)
    assert page.evaluate("() => window.scrollY") == before, (
        "page scroll is not locked while the small-width menu is open")
    for _step in range(6):
        page.keyboard.press("Tab")
        inside = page.evaluate(
            "() => { const d = document.querySelector('[role=dialog]'); "
            "return !!(d && d.contains(document.activeElement)); }")
        assert inside, "Tab leaves the small-width menu, so focus is not trapped"
    page.keyboard.press("Escape")
    expect(dialog).to_be_hidden(timeout=10000)
    assert menu.evaluate("node => node === document.activeElement"), (
        "closing the small-width menu does not return focus to the menu button")


def test_page_access_link_drops_the_token_and_focuses_the_download(page, db, mail):
    """The address bar keeps no token and the download control takes focus."""
    address = probe_email("page-access")
    assert 200 <= register(address, name="Page Probe").status_code < 300, (
        f"registering {address} failed before the page opened its link")
    assert mail.wait_for_count(address, 1) >= 1, f"no access email reached {address}"
    token = mail.newest_token(address)

    origins = []
    page.on("request", lambda request: origins.append(urlparse(request.url).netloc))
    page.emulate_media(reduced_motion="reduce")
    page.goto(f"/beta/access/{token}")
    page.wait_for_load_state("networkidle")
    assert token not in page.url, (
        f"the address bar still carries the token: {page.url}")
    assert urlparse(page.url).path.rstrip("/") == "/beta/access", (
        f"the access route settled at {urlparse(page.url).path!r}, expected "
        f"/beta/access with the token dropped")
    focused = page.evaluate(
        "() => (document.activeElement && document.activeElement.innerText) || ''")
    assert DOWNLOAD_CONTROL in focused, (
        f"the focused element reads {focused[:60]!r}, expected the "
        f"{DOWNLOAD_CONTROL!r} control")
    settle(3.0)
    assert urlparse(page.url).path.rstrip("/") == "/beta/access", (
        f"the access page forwarded on its own to {page.url} under a reduced-motion "
        f"preference")
    slot = db.slot_for(address)
    page.goto("/beta/status")
    page.wait_for_load_state("networkidle")
    if slot is not None:
        expect(page.locator("main")).to_contain_text(str(int(slot["position"])),
                                                     timeout=10000)
    own = urlparse(app_url()).netloc
    foreign = sorted({netloc for netloc in origins if netloc and netloc != own})
    assert not foreign, (
        f"the access route loaded from the foreign origin(s) {foreign}, and no "
        f"analytics of any kind load anywhere on the site")


def test_page_keyboard_focus_and_icon_labels_hold(page):
    """The skip link leads the order, the ring is keyboard-only, icons stay labelled."""
    page.goto("/")
    page.wait_for_load_state("networkidle")
    offscreen = page.evaluate(
        "() => { const a = [...document.querySelectorAll('a')].find(x => "
        "x.textContent.trim() === 'Skip to content'); if (!a) return null; "
        "return a.getBoundingClientRect().bottom; }")
    assert offscreen is not None, "the home route carries no Skip to content link"
    assert offscreen <= 0, (
        f"the skip link sits {offscreen}px into the viewport before it is focused")
    page.keyboard.press("Tab")
    first = page.evaluate(
        "() => (document.activeElement && document.activeElement.textContent || '').trim()")
    assert first == "Skip to content", (
        f"the first Tab reaches {first[:40]!r}, expected the skip link")
    page.keyboard.press("Enter")
    landed = page.evaluate(
        "() => { const a = document.activeElement; return !!(a && (a.tagName === 'MAIN' "
        "|| a.closest('main'))); }")
    assert landed, (
        "following the skip link moves focus nowhere inside the main landmark")

    trigger = page.get_by_role("button", name=HELP_QUESTIONS[0]).first
    trigger.scroll_into_view_if_needed()
    trigger.click()
    pointer_ring = trigger.evaluate(
        "node => { const s = getComputedStyle(node); "
        "return [s.outlineStyle, s.outlineWidth, s.boxShadow].join('|'); }")
    page.keyboard.press("Shift+Tab")
    page.keyboard.press("Tab")
    keyboard_ring = trigger.evaluate(
        "node => { const s = getComputedStyle(node); "
        "return [s.outlineStyle, s.outlineWidth, s.boxShadow].join('|'); }")
    assert keyboard_ring != pointer_ring, (
        f"the focus ring reads {keyboard_ring!r} after a keyboard focus and "
        f"{pointer_ring!r} after a pointer click, so the ring is not keyboard-only")
    outline_style, outline_width, shadow = keyboard_ring.split("|")
    assert (outline_style != "none" and outline_width != "0px") or shadow != "none", (
        f"keyboard focus draws no visible ring at all: {keyboard_ring!r}")

    unlabelled = page.evaluate(
        "() => { const out = []; for (const el of "
        "document.querySelectorAll('a svg, button svg')) { "
        "const host = el.closest('a, button'); "
        "if (!host || !(host.textContent || '').trim()) continue; "
        "if (el.getAttribute('aria-hidden') === 'true' || "
        "el.closest('[aria-hidden=\"true\"]') || "
        "el.getAttribute('role') === 'presentation') continue; "
        "out.push((host.textContent || '').trim().slice(0, 30)); } return out; }")
    assert not unlabelled, (
        f"the decorative icon(s) inside the labelled control(s) {unlabelled[:3]} are "
        f"exposed to assistive technology")
    nameless = page.evaluate(
        "() => { const out = []; for (const el of "
        "document.querySelectorAll('a, button, [role=button]')) { "
        "const text = (el.innerText || '').trim(); "
        "if (text) continue; const r = el.getBoundingClientRect(); "
        "if (!r.width || !r.height) continue; "
        "if (el.closest('[aria-hidden=\"true\"]')) continue; "
        "if (el.getAttribute('aria-label') || el.getAttribute('title') || "
        "el.getAttribute('aria-labelledby')) continue; "
        "out.push(el.outerHTML.slice(0, 60)); } return out; }")
    assert not nameless, (
        f"the icon-only control(s) {nameless[:2]} carry no accessible name")

    page.get_by_role("link", name="Blog", exact=True).first.click()
    page.wait_for_url("**/blog", timeout=15000)
    settle(1.5)
    arrived = page.evaluate(
        "() => { const a = document.activeElement; return !!(a && (a.tagName === 'MAIN' "
        "|| a.closest('main'))); }")
    assert arrived, (
        "after a route change the incoming main landmark receives no focus, so a "
        "keyboard reader restarts at the top of the document")


def test_page_help_panel_opens_links_and_filters(page):
    """A linked item opens, several stay open and a chip filters without navigating."""
    page.goto("/#faq-03")
    page.wait_for_load_state("networkidle")
    third = page.get_by_role("button", name=HELP_QUESTIONS[2]).first
    expect(third).to_have_attribute("aria-expanded", "true", timeout=10000)
    first = page.get_by_role("button", name=HELP_QUESTIONS[0]).first
    first.scroll_into_view_if_needed()
    first.click()
    expect(first).to_have_attribute("aria-expanded", "true", timeout=10000)
    assert third.get_attribute("aria-expanded") == "true", (
        "opening a second help item closed the item that was already open, and several "
        "may be open at once")
    answer = page.locator(f'[id="{first.get_attribute("aria-controls")}"]')
    assert answer.count() == 1, (
        f"the help trigger controls {first.get_attribute('aria-controls')!r}, which "
        f"resolves to no single region")
    assert answer.first.inner_text().strip(), (
        "the opened help item carries no answer in the delivered markup")

    before_url = page.url
    chip = page.locator("#help").get_by_text("Pricing", exact=True).first
    chip.click()
    settle(1.0)
    assert page.url == before_url, (
        f"a help category chip navigated from {before_url} to {page.url}")
    expect(third).to_be_visible(timeout=10000)
    assert third.get_attribute("aria-expanded") == "true", (
        "filtering closed a help item that stayed visible")
    assert not first.is_visible(), (
        "filtering on Pricing still shows the privacy question")


def test_page_release_notes_follow_a_dark_appearance(page):
    """Only the release notes invert with the system appearance."""
    reading = "() => [getComputedStyle(document.documentElement).backgroundColor, " \
              "getComputedStyle(document.body).backgroundColor, " \
              "getComputedStyle(document.body).color].join('|')"
    page.emulate_media(color_scheme="light")
    page.goto("/release-notes/0.2.3")
    page.wait_for_load_state("networkidle")
    light_notes = page.evaluate(reading)
    page.goto("/")
    page.wait_for_load_state("networkidle")
    light_home = page.evaluate(reading)
    page.emulate_media(color_scheme="dark")
    page.goto("/release-notes/0.2.3")
    page.wait_for_load_state("networkidle")
    dark_notes = page.evaluate(reading)
    page.goto("/")
    page.wait_for_load_state("networkidle")
    dark_home = page.evaluate(reading)
    assert dark_notes != light_notes, (
        f"the release notes render {dark_notes} under a dark system appearance and "
        f"{light_notes} under a light one, so the route follows neither")
    assert dark_home == light_home, (
        f"the home route renders {dark_home} under a dark system appearance and "
        f"{light_home} under a light one, and only the release notes follow it")
    page.emulate_media(color_scheme="light")
    page.goto("/release-notes/0.2.3")
    page.set_viewport_size({"width": 390, "height": 844})
    overflow = page.evaluate(
        "() => document.documentElement.scrollWidth - "
        "document.documentElement.clientWidth")
    assert overflow <= 1, (
        f"the release notes overflow by {overflow}px in a small panel at 390px")


def test_page_registration_form_reports_errors_and_keeps_values(page, mail):
    """The summary takes focus, the messages are pinned and the values survive."""
    page.goto("/download")
    page.wait_for_load_state("networkidle")
    page.evaluate(
        "() => { const f = document.querySelector('form'); if (f) f.noValidate = true; }")
    name_field = page.locator("input[name=name]").first
    if name_field.count():
        name_field.fill("Kept Name")
    submit = page.get_by_role("button", name="Join the beta").first
    submit.click()
    settle(1.5)
    body = page.locator("body").inner_text()
    assert "Enter an email address so we can send your access link." in body, (
        f"a submission with no address never shows the pinned missing-email message: "
        f"{body[:300]}")
    assert "Confirm you want the access link." in body, (
        f"a submission with no consent never shows the pinned consent message: "
        f"{body[:300]}")
    summary_focused = page.evaluate(
        "() => { const a = document.activeElement; if (!a) return null; "
        "const holder = a.closest('[role=alert],[aria-live]') || a; "
        "return {role: a.getAttribute('role') || '', live: a.getAttribute('aria-live') || '', "
        "links: holder.querySelectorAll('a[href^=\"#\"]').length, "
        "text: (holder.innerText || '').slice(0, 200)}; }")
    assert summary_focused and summary_focused["links"] >= 2, (
        f"the focused element after a failed submission is {summary_focused}, expected "
        f"an error summary linking to each invalid field")
    assert (summary_focused["role"] == "alert"
            or summary_focused["live"] in ("assertive", "polite")), (
        f"the error summary announces itself as {summary_focused}, expected an "
        f"assertive live region")
    invalid = page.locator("input[type=email][aria-invalid=true]")
    assert invalid.count() == 1, (
        f"{invalid.count()} email fields are marked invalid after a failed submission")
    described = invalid.first.get_attribute("aria-describedby")
    assert described, "the invalid email field points at no message of its own"

    email_box = page.locator("input[type=email]").first
    email_box.click()
    page.keyboard.type("not-an-address")
    settle(1.0)
    assert "Enter an email address so we can send your access link." not in \
        page.locator("body").inner_text(), (
        "the missing-address message survives typing, and errors clear as the visitor "
        "types")
    page.locator("input[type=checkbox]").first.check()
    submit.click()
    settle(1.5)
    body = page.locator("body").inner_text()
    assert "Check the address, it looks like a typo." in body, (
        f"a malformed address never shows the pinned typo message: {body[:300]}")
    assert email_box.input_value() == "not-an-address", (
        f"the entered address became {email_box.input_value()!r} after a failed "
        f"submission")
    if name_field.count():
        assert name_field.input_value() == "Kept Name", (
            f"the entered name became {name_field.input_value()!r} after a failed "
            f"submission")

    unusual = f"o'brien+{os.urandom(4).hex()}@example.co.uk"
    email_box.fill(unusual)
    page.context.set_offline(True)
    submit.click()
    settle(2.0)
    offline_body = page.locator("body").inner_text()
    assert "offline" in offline_body.lower(), (
        f"submitting offline shows no message saying so: {offline_body[:300]}")
    assert email_box.input_value() == unusual, (
        f"the entered address became {email_box.input_value()!r} after an offline "
        f"submission")
    page.context.set_offline(False)
    submit.click()
    expect(page.get_by_text("Check your inbox").first).to_be_visible(timeout=20000)
    panel = page.locator("body").inner_text()
    assert unusual in panel, (
        f"the success panel never names the submitted address: {panel[:300]}")
    assert "spam" in panel.lower(), (
        f"the success panel never suggests the spam folder: {panel[:300]}")
    assert "Resend link" in panel, (
        f"the success panel offers no Resend link control: {panel[:300]}")
    assert re.search(r"\b60\b|\b59\b|\b58\b", panel), (
        f"the success panel shows no count down from 60 seconds: {panel[:300]}")
    assert mail.wait_for_count(unusual, 1) >= 1, (
        f"no access email reached {unusual} after a successful submission through the "
        f"rendered form")


def test_page_checksum_copy_control_copies_the_full_digest(page):
    """The panel shows a truncated checksum and copies the whole one."""
    stable = [row for row in releases() if str(row["status"]) == "published"][0]
    digest = str(stable["sha256"])
    page.context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.goto("/download")
    page.wait_for_load_state("networkidle")
    shown = page.locator("main").inner_text()
    assert digest[:8] in shown, (
        f"the distribution panel shows no checksum for {stable['version']}: "
        f"{shown[:300]}")
    assert digest not in shown, (
        "the distribution panel shows the whole checksum, and the brief shows it "
        "truncated behind a copy control")
    control = page.get_by_role("button", name=re.compile("copy", re.I)).first
    expect(control).to_be_visible(timeout=10000)
    control.click()
    settle(1.0)
    copied = page.evaluate("async () => await navigator.clipboard.readText()")
    assert copied.strip() == digest, (
        f"the copy control put {copied.strip()[:20]!r}... on the clipboard, expected "
        f"the full digest {digest[:20]}...")
    monospace = page.evaluate(
        "(head) => { const el = [...document.querySelectorAll('main *')].find(e => "
        "[...e.childNodes].some(n => n.nodeType === 3 && n.textContent.includes(head))); "
        "return el ? getComputedStyle(el).fontFamily : null; }", digest[:8])
    assert monospace and "IBM Plex Mono" in monospace, (
        f"the checksum renders in {monospace!r}, and a machine-read value is monospace")


def test_page_hotkey_demonstration_renders_a_prompt(page):
    """The demonstration filters, renders and leaves the clipboard alone."""
    page.context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.goto("/")
    page.wait_for_load_state("networkidle")
    page.evaluate("async () => await navigator.clipboard.writeText('sentinel-value')")
    trigger = page.get_by_role("button", name="Try the hotkey").first
    expect(trigger).to_be_visible(timeout=10000)
    trigger.click()
    dialog = page.get_by_role("dialog").first
    expect(dialog).to_be_visible(timeout=10000)
    assert (dialog.get_attribute("aria-label")
            or dialog.get_attribute("aria-labelledby")), (
        "the hotkey demonstration dialog carries no accessible name")
    assert dialog.locator("[aria-live=polite]").count() >= 1, (
        "the hotkey demonstration announces its result count through no polite live "
        "region")
    page.keyboard.type("code")
    settle(1.5)
    listed = dialog.inner_text()
    assert "Code review checklist" in listed, (
        f"typing in the demonstration never filters to the matching Blueprint: "
        f"{listed[:200]}")
    page.keyboard.press("Enter")
    settle(1.5)
    rendered = dialog.inner_text()
    assert "Review" in rendered, (
        f"the demonstration renders no finished prompt: {rendered[:200]}")
    assert "{{" not in rendered, (
        f"the finished prompt still carries an unfilled blank: {rendered[:200]}")
    for _step in range(6):
        page.keyboard.press("Tab")
        inside = page.evaluate(
            "() => { const d = document.querySelector('[role=dialog]'); "
            "return !!(d && d.contains(document.activeElement)); }")
        assert inside, "Tab leaves the hotkey demonstration, so focus is not trapped"
    clipboard = page.evaluate("async () => await navigator.clipboard.readText()")
    assert clipboard == "sentinel-value", (
        f"the demonstration wrote {clipboard[:40]!r} to the clipboard without its Copy "
        f"control being pressed")
    page.keyboard.press("Escape")
    expect(dialog).to_be_hidden(timeout=10000)
    assert trigger.evaluate("node => node === document.activeElement"), (
        "closing the hotkey demonstration does not return focus to its trigger")

    page.set_viewport_size({"width": 844, "height": 390})
    page.goto("/")
    page.wait_for_load_state("networkidle")
    page.keyboard.press("Control+Shift+Space")
    settle(1.0)
    dialogs = page.get_by_role("dialog")
    opened = dialogs.count() > 0 and dialogs.first.is_visible()
    assert not opened, (
        "the hotkey demonstration opened on a short landscape phone, where it does not "
        "fit")


def test_page_instruments_answer_the_keyboard_and_keep_their_own_scroll(page):
    """The scrubber steps, the capsule stays and the ledger never chains its scroll."""
    page.goto("/")
    page.wait_for_load_state("networkidle")
    slider = page.get_by_role("slider").first
    expect(slider).to_be_visible(timeout=10000)
    slider.scroll_into_view_if_needed()
    slider.focus()
    reading = "node => node.getAttribute('aria-valuenow') || node.value"
    page.keyboard.press("Home")
    settle(0.5)
    lowest = slider.evaluate(reading)
    page.keyboard.press("End")
    settle(0.5)
    highest = slider.evaluate(reading)
    assert lowest != highest, (
        f"Home and End both leave the version scrubber at {lowest!r}, so it is not a "
        f"range control the keyboard drives")
    page.keyboard.press("ArrowLeft")
    settle(0.5)
    stepped = slider.evaluate(reading)
    assert stepped != highest, (
        f"the arrow keys leave the version scrubber at {highest!r}")
    label = slider.get_attribute("aria-valuetext") or ""
    assert "Version" in label, (
        f"the scrubber announces {label!r}, expected a version label such as "
        f"Version 3, starred")

    page.evaluate("() => document.activeElement && document.activeElement.blur()")
    page.keyboard.press("End")
    settle(1.5)
    bottom = page.evaluate("() => window.scrollY")
    assert bottom > 500, (
        f"the End key left the page at {bottom}px, so it no longer pages the document")
    capsule = page.get_by_role("navigation").first
    box = capsule.bounding_box()
    assert box and 0 <= box["y"] < 200, (
        f"the navigation capsule sits at {box} once the page is scrolled to the end, so "
        f"it hides on scroll")
    page.keyboard.press("Home")
    settle(1.5)
    assert page.evaluate("() => window.scrollY") <= 5, (
        "the Home key no longer pages the document back to the top")
    page.keyboard.press("Space")
    settle(1.5)
    assert page.evaluate("() => window.scrollY") > 50, (
        "the Space key no longer pages the document")

    nested = page.evaluate(
        "() => { const els = [...document.querySelectorAll('*')].filter(e => { "
        "const s = getComputedStyle(e); "
        "return (s.overflowY === 'auto' || s.overflowY === 'scroll') && "
        "e.scrollHeight > e.clientHeight + 8 && e.clientHeight > 80; }); "
        "if (!els.length) return null; const el = els[els.length - 1]; "
        "el.scrollTop = el.scrollHeight; const r = el.getBoundingClientRect(); "
        "return {x: r.x + r.width / 2, y: r.y + r.height / 2}; }")
    assert nested, (
        "no region on the home route scrolls inside its own container, and the history "
        "ledger does")
    page.mouse.move(nested["x"], nested["y"])
    anchored = page.evaluate("() => window.scrollY")
    page.mouse.wheel(0, 400)
    settle(1.0)
    assert page.evaluate("() => window.scrollY") == anchored, (
        "scrolling inside the history ledger chained its scroll to the page")

    page.goto("/")
    page.wait_for_load_state("networkidle")
    page.evaluate("() => window.scrollTo(0, 1200)")
    settle(1.0)
    page.get_by_role("link", name="Blog", exact=True).first.click()
    page.wait_for_url("**/blog", timeout=15000)
    page.go_back()
    page.wait_for_url(re.compile(r".*/$"), timeout=15000)
    settle(1.5)
    restored = page.evaluate("() => window.scrollY")
    assert restored > 400, (
        f"back navigation restored the home route at {restored}px, losing the earlier "
        f"scroll position")


def test_page_press_captures_switch_variants_and_rest_under_reduced_motion(page):
    """The Light and Dark control chooses the variant and the loops stay still."""
    page.goto("/press")
    page.wait_for_load_state("networkidle")
    before = page.evaluate(
        "() => { const img = document.querySelector('main figure img'); "
        "return img ? img.currentSrc || img.src : null; }")
    assert before, "/press renders no capture at all"
    control = page.get_by_text(re.compile(r"^\s*Dark\s*$"), exact=False).first
    control.scroll_into_view_if_needed()
    control.click()
    settle(1.5)
    after = page.evaluate(
        "() => { const img = document.querySelector('main figure img'); "
        "return img ? img.currentSrc || img.src : null; }")
    assert after != before, (
        f"the Light and Dark control left the capture at {before}, so the page never "
        f"chooses a variant independently of the reader's system setting")

    page.emulate_media(reduced_motion="reduce")
    page.goto("/press")
    page.wait_for_load_state("networkidle")
    settle(2.0)
    playing = page.evaluate(
        "() => [...document.querySelectorAll('video')].filter(v => !v.paused).length")
    assert playing == 0, (
        f"{playing} press motion loop(s) play under a reduced-motion preference")
    paused_loops = page.evaluate(
        "() => [...document.querySelectorAll('video')].map(v => ({muted: v.muted, "
        "poster: !!v.poster, preload: v.preload}))")
    assert len(paused_loops) >= 2, (
        f"/press renders {len(paused_loops)} motion loops, expected the two the brief "
        f"pins")
    for loop in paused_loops:
        assert loop["muted"] and loop["poster"] and loop["preload"] == "none", (
            f"a press motion loop reports {loop}, expected muted with a poster and no "
            f"preloading")


def test_page_blog_reading_time_matches_the_article_word_count(page):
    """Each reading time is computed from the body rather than typed by hand."""
    for route in ARTICLE_ROUTES:
        page.goto(route)
        page.wait_for_load_state("networkidle")
        words = page.evaluate(
            "() => { const a = document.querySelector('article') || "
            "document.querySelector('main'); "
            "return (a.innerText || '').trim().split(/\\s+/).filter(Boolean).length; }")
        shown = page.locator("main").inner_text()
        match = re.search(r"(\d+)\s*min read", shown)
        assert match, f"{route} shows no reading time in the form N min read"
        stated = int(match.group(1))
        expected = reading_minutes(words)
        assert abs(stated - expected) <= 1, (
            f"{route} states {stated} min read against {words} words, which divide by "
            f"200 and round up to {expected}")


def test_page_legal_pages_print_without_backgrounds(page):
    """The print styles drop the backgrounds and write each address out."""
    page.emulate_media(media="print")
    for route in ("/privacy", "/terms"):
        page.goto(route)
        page.wait_for_load_state("networkidle")
        ground = page.evaluate(
            "() => { const h = getComputedStyle(document.documentElement); "
            "const b = getComputedStyle(document.body); "
            "return [h.backgroundColor, b.backgroundColor, b.backgroundImage, "
            "h.backgroundImage].join('|'); }")
        parts = ground.split("|")
        for colour in parts[:2]:
            assert colour in ("rgba(0, 0, 0, 0)", "transparent", "rgb(255, 255, 255)"), (
                f"{route} keeps the background {colour!r} in print, and the print "
                f"styles suppress backgrounds")
        for image in parts[2:]:
            assert image == "none", (
                f"{route} keeps the background image {image!r} in print")
        expanded = page.evaluate(
            "() => { const a = document.querySelector('main a[href]'); "
            "return a ? getComputedStyle(a, '::after').content : null; }")
        assert expanded and expanded not in ("none", "normal", '""'), (
            f"{route} writes no link address after its text in print: {expanded!r}")
    page.emulate_media(media="screen")


def test_page_founder_card_reads_the_live_cohort(page):
    """The middle pricing card states the cohort the ledger actually holds."""
    state = allocation()
    page.goto("/")
    page.wait_for_load_state("networkidle")
    card = page.locator("#pricing")
    expect(card).to_be_visible(timeout=10000)
    card.scroll_into_view_if_needed()
    settle(1.5)
    shown = card.inner_text()
    claimed = int(state["claimed"])
    if state["state"] == "closed":
        assert CLOSED_NOTICE in shown, (
            f"with every place held the founder card reads {shown[:200]!r}, expected "
            f"{CLOSED_NOTICE!r}")
        assert "Join the beta" in shown, (
            f"the closed founder card offers {shown[:200]!r}, expected the action Join "
            f"the beta")
    elif claimed < TIER_SIZE:
        assert "$29" in shown, (
            f"with {claimed} places held the founder card reads {shown[:200]!r}, "
            f"expected the tier one price")
        assert f"{TIER_SIZE - claimed} of {TIER_SIZE} founder places left at $29" in shown, (
            f"the founder card reads {shown[:200]!r}, expected "
            f"{TIER_SIZE - claimed} of {TIER_SIZE} founder places left at $29")
    else:
        assert "$39" in shown, (
            f"with {claimed} places held the founder card reads {shown[:200]!r}, "
            f"expected the tier two price")
        assert "claimed" in shown.lower() and "left" in shown.lower(), (
            f"the tier two founder card states no claimed and left counts: "
            f"{shown[:200]}")
    assert "Standard licence at 1.0: $49" in shown, (
        f"the founder card never states the standard licence value: {shown[:200]}")
    assert "loading" not in shown.lower(), (
        f"the founder card shows a loading state rather than its static content: "
        f"{shown[:200]}")


def test_page_double_submission_sends_one_email(page, mail):
    """A doubled press of the action registers once and emails once."""
    address = probe_email("double")
    page.goto("/download")
    page.wait_for_load_state("networkidle")
    page.locator("input[type=email]").first.fill(address)
    page.locator("input[type=checkbox]").first.check()
    submit = page.get_by_role("button", name="Join the beta").first
    submit.dblclick()
    expect(page.get_by_text("Check your inbox").first).to_be_visible(timeout=20000)
    assert mail.wait_for_count(address, 1) >= 1, (
        f"no access email reached {address} after the form was submitted")
    settle(3.0)
    assert mail.count(address) == 1, (
        f"{mail.count(address)} access emails reached {address} after one doubled "
        f"press, and a second submission is absorbed rather than duplicated")


def test_page_registrant_session_never_opens_the_operator_console(page, mail):
    """An access session reaches the sign-in form and nothing behind it."""
    address = probe_email("console")
    assert 200 <= register(address).status_code < 300, (
        f"registering {address} failed before the console was opened")
    assert mail.wait_for_count(address, 1) >= 1, f"no access email reached {address}"
    token = mail.newest_token(address)
    page.goto(f"/beta/access/{token}")
    page.wait_for_load_state("networkidle")
    page.goto("/operator")
    page.wait_for_load_state("networkidle")
    shown = page.locator("body").inner_text()
    assert page.locator("input[type=password]").count() == 1, (
        f"/operator shows {page.locator('input[type=password]').count()} password "
        f"fields to a registrant session, expected the sign-in form")
    assert REGISTRANT_EMAIL not in shown, (
        f"/operator shows the registrations list to a registrant session: {shown[:300]}")
    assert address not in shown, (
        f"/operator shows the registrant's own address to an access session: "
        f"{shown[:300]}")
    for offer in ("forgot", "reset your password", "create an account", "sign up"):
        assert offer not in shown.lower(), (
            f"the operator sign-in offers {offer!r}, and there is neither a password "
            f"reset nor an operator signup")


def test_founder_cap_closes_at_one_thousand_places(db, page):
    """The thousandth place is the last, and the card and the ledger both say so."""
    opening = allocation()
    held_before = {str(row["email"]): int(row["position"]) for row in db.q(
        "SELECT r.email AS email, s.position AS position FROM founder_slots s "
        "JOIN registrations r ON r.id = s.registration_id")}
    tier_two_seen = False
    rounds = 0
    while allocation()["state"] == "open" and rounds < 60:
        rounds += 1
        state = allocation()
        batch = min(48, COHORT_CAP - int(state["claimed"]) + 4)
        statuses = register_many([probe_email("cap") for _ in range(batch)], 12)
        assert all(200 <= code < 300 for code in statuses), (
            f"a registration during the fill returned {sorted(set(statuses))}")
        filled = allocation()
        if not tier_two_seen and TIER_SIZE <= int(filled["claimed"]) < COHORT_CAP:
            assert int(filled["current_tier"]) == 2, (
                f"with {filled['claimed']} places held the cohort reports tier "
                f"{filled['current_tier']}, expected tier 2")
            assert int(filled["current_price_minor"]) == TIER2_PRICE, (
                f"the cohort prices the next place at "
                f"{filled['current_price_minor']}, expected {TIER2_PRICE}")
            page.goto("/")
            page.wait_for_load_state("networkidle")
            card = page.locator("#pricing")
            card.scroll_into_view_if_needed()
            expect(card).to_contain_text("$39", timeout=20000)
            shown = card.inner_text()
            assert "claimed" in shown.lower() and "left" in shown.lower(), (
                f"the tier two founder card states no claimed and left counts: "
                f"{shown[:200]}")
            tier_two_seen = True

    final = allocation()
    assert str(final["state"]) == "closed", (
        f"after {rounds} rounds of registrations the cohort reports state "
        f"{final['state']!r} with {final['claimed']} claimed")
    assert int(final["claimed"]) == COHORT_CAP, (
        f"the closed cohort reports {final['claimed']} claimed, expected {COHORT_CAP}")
    assert int(final["remaining"]) == 0, (
        f"the closed cohort reports {final['remaining']} remaining")
    assert final["current_tier"] is None and final["current_price_minor"] is None, (
        f"the closed cohort reports tier {final['current_tier']!r} at "
        f"{final['current_price_minor']!r}, expected null for both")
    if opening["state"] == "open" and int(opening["claimed"]) < TIER_SIZE:
        assert tier_two_seen, (
            "the cohort passed 500 held places without the card ever showing the tier "
            "two price")

    positions = [int(slot["position"]) for slot in db.slots()]
    assert positions == list(range(1, COHORT_CAP + 1)), (
        f"the held places are not 1 to {COHORT_CAP} with no gaps: {positions[:5]} ... "
        f"{positions[-5:]}")
    for late in [probe_email("late") for _ in range(3)]:
        response = register(late)
        assert 200 <= response.status_code < 300, (
            f"a registration after the cohort closed returned "
            f"{response.status_code}: {response.text[:300]}")
        body = response.json()
        assert body.get("status") == "sent" and body.get("message") == SUCCESS_MESSAGE, (
            f"a registration after the cohort closed answered {str(body)[:200]}, "
            f"expected the same success response")
        assert db.registration(late) is not None, (
            f"the registration of {late} after the cohort closed was not stored")
        assert db.slot_for(late) is None, (
            f"{late} received a founder place after the cohort closed")
    assert db.slot_count() == COHORT_CAP, (
        f"founder_slots holds {db.slot_count()} rows, and a thousand-and-first place "
        f"never exists")
    held_after = {str(row["email"]): int(row["position"]) for row in db.q(
        "SELECT r.email AS email, s.position AS position FROM founder_slots s "
        "JOIN registrations r ON r.id = s.registration_id")}
    for address, position in held_before.items():
        assert held_after.get(address) == position, (
            f"{address} held place {position} and now holds "
            f"{held_after.get(address)!r}; a place is never reassigned")

    page.goto("/")
    page.wait_for_load_state("networkidle")
    card = page.locator("#pricing")
    card.scroll_into_view_if_needed()
    expect(card).to_contain_text(CLOSED_NOTICE, timeout=20000)
    closed = card.inner_text()
    assert "Join the beta" in closed, (
        f"the closed founder card offers {closed[:200]!r}, expected the action Join the "
        f"beta")
