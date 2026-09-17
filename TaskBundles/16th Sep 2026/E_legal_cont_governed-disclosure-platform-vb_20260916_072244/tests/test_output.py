from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor

import httpx

import appclient
from conftest import (
    ANCHORS,
    API,
    APP_URL,
    ARCHIVE_PAGE_SIZE,
    ARCHIVE_ROUTE,
    AUTHOR2_EMAIL,
    AUTHOR_EMAIL,
    BLOCK_TYPES,
    CAPITAL_PROPOSITION,
    CHAPTER_ONE_HEADLINE,
    CHAPTER_TWO_HEADING,
    COMPLIANCE_EMAIL,
    CONTACT_ROUTE,
    CORPUS_PASSWORD,
    DISCLOSURE_CLASSES,
    DIVISION_CAPITAL,
    DIVISION_GROUP,
    DIVISION_KEYS,
    DIVISION_MARITIME,
    DIVISION_NAMES,
    DIVISION_TRADING,
    DIVISION_VENTURE,
    DUBAI_EMAIL,
    DUBAI_PHONE,
    EMBARGOED_RELEASE_TITLE,
    FIGURES_FEMALE_GLOBAL,
    FIGURES_FEMALE_MANAGEMENT,
    FIGURES_NATIONALITY_COUNT,
    FIGURES_OFFICE_COUNT,
    GENEVA_EMAIL,
    GENEVA_PHONE,
    GROUP_ADMIN_EMAIL,
    KEY_SCHEME_PREFIX,
    LEGAL_EMAIL,
    MARKER_LABELS,
    MEDIA_EMAIL,
    METALS_PRODUCTS,
    NEWEST_RELEASE_TITLE,
    OIL_PRODUCTS,
    OLDEST_RELEASE_TITLE,
    POLICY_CODES,
    PUBLISHED_RELEASE_COUNT,
    PEOPLE_STATEMENT,
    PUBLISHER_EMAIL,
    RESPONSIBILITY_HEADING,
    SECURITY_HEADER_NAMES,
    SEEDED_EMAILS,
    SINGAPORE_EMAIL,
    SINGAPORE_PHONE,
    SUSTAINABILITY_HEADING,
    TRADING_PROPOSITION,
    VENTURE_PROPOSITION,
    WITHDRAWAL_REASON,
    WITHDRAWN_RELEASE_TITLE,
    anon,
    code_of,
    counter_value,
    describe,
    probe_id,
    public_releases,
    record_titled,
    records_for,
    settle,
    token_for,
)

DENIED = (401, 403, 404)
GONE = 410


def _future(seconds: int) -> str:
    moment = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=seconds)
    return moment.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _past(seconds: int) -> str:
    moment = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=seconds)
    return moment.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _draft(client: httpx.Client, division: str, title: str) -> dict:
    response = client.post(
        "/content/records",
        json={
            "type": "release",
            "division_key": division,
            "title": title,
            "slug": f"probe-{probe_id()}",
            "blocks": [{"block_type": "paragraph", "payload": {"text": "A seeded probe body."}}],
        },
    )
    assert response.status_code in (200, 201), describe(response)
    return response.json()


def _through_legal(author_client, legal_client, division: str, title: str) -> dict:
    record = _draft(author_client, division, title)
    rid = record["id"]
    submitted = author_client.post(
        f"/workflow/records/{rid}/submit", json={"expected_state": "draft"}
    )
    assert submitted.status_code in (200, 201), describe(submitted)
    moved = legal_client.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "compliance_review", "expected_state": "legal_review", "comment": "cleared"},
    )
    assert moved.status_code in (200, 201), describe(moved)
    return record


def test_health_route_returns_ok(stranger):
    response = stranger.get("/health")
    assert response.status_code == 200, describe(response)


def test_seeded_accounts_sign_in_with_the_corpus_password():
    for email in SEEDED_EMAILS:
        token = appclient.login(email, CORPUS_PASSWORD)
        assert token, f"login for {email} returned an empty access_token"


def test_wrong_password_is_refused_without_naming_the_address(stranger):
    known = stranger.post("/auth/login", json={"email": AUTHOR_EMAIL, "password": "not-the-one"})
    unknown_address = f"probe-{probe_id()}@example.com"
    unknown = stranger.post(
        "/auth/login", json={"email": unknown_address, "password": "not-the-one"}
    )
    assert known.status_code in DENIED, describe(known)
    assert known.status_code == unknown.status_code, (
        f"a wrong password and an unknown address answer differently: "
        f"{describe(known)} versus {describe(unknown)}"
    )


def test_logout_refuses_the_previous_bearer_token():
    token = token_for(AUTHOR_EMAIL)
    with appclient.client(token) as handle:
        before = handle.get("/me")
        assert before.status_code == 200, describe(before)
        ended = handle.post("/auth/logout", json={})
        assert ended.status_code in (200, 204), describe(ended)
    with appclient.client(token) as handle:
        after = handle.get("/me")
    assert after.status_code in DENIED, (
        f"a token that was logged out still works: {describe(after)}"
    )


def test_anonymous_request_to_a_console_endpoint_is_denied(stranger):
    for path in ("/me", "/content/records", "/workflow/inbox", "/admin/audit"):
        response = stranger.get(path)
        assert response.status_code in DENIED, f"{path} served an anonymous caller: {describe(response)}"


def test_unparseable_bearer_token_is_denied():
    with httpx.Client(base_url=API, timeout=30.0) as handle:
        response = handle.get("/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert response.status_code in DENIED, describe(response)


def test_signup_and_reset_surfaces_do_not_exist(stranger):
    for path in ("/auth/signup", "/auth/register", "/auth/reset", "/auth/forgot"):
        response = stranger.post(path, json={"email": f"probe-{probe_id()}@example.com"})
        assert response.status_code in (401, 403, 404, 405), (
            f"{path} answered as though an account could be created or reset: {describe(response)}"
        )


def test_repeated_failed_logins_for_one_address_are_refused(stranger):
    address = AUTHOR2_EMAIL
    seen = []
    limited = False
    for _ in range(8):
        response = stranger.post(
            "/auth/login", json={"email": address, "password": f"wrong-{probe_id()}"}
        )
        seen.append(response.status_code)
        if response.status_code == 429 or code_of(response) == "rate_limited":
            limited = True
            break
    assert limited, (
        f"eight failed password attempts for one address were never refused as rate limited: "
        f"{seen}"
    )


def test_me_returns_the_callers_memberships(author):
    response = author.get("/me")
    assert response.status_code == 200, describe(response)
    body = response.json()
    assert body.get("email") == AUTHOR_EMAIL, describe(response)
    divisions = {m.get("division_key") for m in body.get("memberships", [])}
    assert DIVISION_TRADING in divisions, f"author holds no trading membership: {body}"
    assert DIVISION_CAPITAL in divisions, f"author holds no capital membership: {body}"


def test_five_divisions_are_seeded_with_their_names(stranger):
    response = stranger.get("/public/divisions")
    assert response.status_code == 200, describe(response)
    rows = response.json()
    assert isinstance(rows, list), describe(response)
    seen = {row["key"]: row["name"] for row in rows}
    for key in DIVISION_KEYS:
        assert key in seen, f"division {key!r} is absent: {seen}"
        assert seen[key] == DIVISION_NAMES[key], (
            f"division {key!r} is named {seen[key]!r}, the brief pins {DIVISION_NAMES[key]!r}"
        )


def test_the_venture_division_carries_its_own_mark(stranger):
    response = stranger.get("/public/divisions")
    assert response.status_code == 200, describe(response)
    rows = {row["key"]: row for row in response.json()}
    venture = rows[DIVISION_VENTURE]
    assert venture.get("primary_colour_role") == "own", (
        f"{DIVISION_VENTURE} does not carry its own colour role: {venture}"
    )
    for key in (DIVISION_GROUP, DIVISION_TRADING, DIVISION_CAPITAL, DIVISION_MARITIME):
        assert rows[key].get("primary_colour_role") == "group", (
            f"{key} should default to the group colour role: {rows[key]}"
        )


def test_three_offices_are_seeded_with_their_jurisdictions(stranger):
    response = stranger.get("/public/offices")
    assert response.status_code == 200, describe(response)
    rows = response.json()
    assert isinstance(rows, list) and len(rows) >= 3, describe(response)
    by_jurisdiction = {row["jurisdiction"]: row for row in rows}
    assert set(by_jurisdiction) >= {"CH", "AE-DIFC", "SG"}, by_jurisdiction
    assert by_jurisdiction["CH"]["reception_email"] == GENEVA_EMAIL, by_jurisdiction["CH"]
    assert by_jurisdiction["AE-DIFC"]["reception_email"] == DUBAI_EMAIL, by_jurisdiction["AE-DIFC"]
    assert by_jurisdiction["SG"]["reception_email"] == SINGAPORE_EMAIL, by_jurisdiction["SG"]
    assert by_jurisdiction["CH"]["phone_e164"] == GENEVA_PHONE, by_jurisdiction["CH"]
    assert by_jurisdiction["AE-DIFC"]["phone_e164"] == DUBAI_PHONE, by_jurisdiction["AE-DIFC"]
    assert by_jurisdiction["SG"]["phone_e164"] == SINGAPORE_PHONE, by_jurisdiction["SG"]
    labels = {row["marker_label"] for row in rows}
    assert labels >= set(MARKER_LABELS), f"marker labels are {labels}"


def test_group_figures_are_a_record_not_a_template(stranger):
    response = stranger.get("/public/figures")
    assert response.status_code == 200, describe(response)
    body = response.json()
    assert str(body["office_count"]) == FIGURES_OFFICE_COUNT, body
    assert str(body["nationality_count"]) == FIGURES_NATIONALITY_COUNT, body
    assert str(body["female_share_global"]) == FIGURES_FEMALE_GLOBAL, body
    assert str(body["female_share_management"]) == FIGURES_FEMALE_MANAGEMENT, body
    assert body.get("as_at"), f"the figures record carries no as-at date: {body}"


def test_twelve_products_are_records_in_two_families(stranger):
    response = stranger.get("/public/search", params={"q": "Naphtha"})
    assert response.status_code == 200, describe(response)
    titles = {row["title"] for row in response.json()}
    assert "Naphtha" in titles, f"the seeded product Naphtha is not searchable: {titles}"


def test_the_policy_register_seeds_six_entries(publisher):
    response = publisher.get("/policy/entries")
    assert response.status_code == 200, describe(response)
    codes = {row["reference_code"] for row in response.json()}
    for code in POLICY_CODES:
        assert code in codes, f"register entry {code!r} is absent: {sorted(codes)}"


def test_the_three_privacy_variants_share_a_version(stranger):
    response = stranger.get("/public/policies")
    assert response.status_code == 200, describe(response)
    rows = {row["reference_code"]: row for row in response.json()}
    variants = ["POL-PRIVACY-CH", "POL-PRIVACY-AE", "POL-PRIVACY-SG"]
    for code in variants:
        assert code in rows, f"{code} is not published externally: {sorted(rows)}"
    versions = {rows[code]["version"] for code in variants}
    assert len(versions) == 1, f"the three privacy variants sit at different versions: {versions}"


def test_a_draft_created_by_an_author_starts_in_draft(author):
    record = _draft(author, DIVISION_TRADING, f"Probe draft {probe_id()}")
    assert record["state"] == "draft", record
    assert record["division_key"] == DIVISION_TRADING, record


def test_an_edit_produces_a_new_revision_and_keeps_the_old_one(author):
    record = _draft(author, DIVISION_TRADING, f"Probe revision {probe_id()}")
    rid = record["id"]
    first = author.get(f"/content/records/{rid}/revisions")
    assert first.status_code == 200, describe(first)
    before = len(first.json())
    edited = author.patch(
        f"/content/records/{rid}",
        json={"title": f"Probe revision edited {probe_id()}"},
    )
    assert edited.status_code == 200, describe(edited)
    after_response = author.get(f"/content/records/{rid}/revisions")
    assert after_response.status_code == 200, describe(after_response)
    after = after_response.json()
    assert len(after) == before + 1, (
        f"an edit did not create a revision: {before} then {len(after)}"
    )
    assert len({row["id"] for row in after}) == len(after), "revision ids repeat"


def test_a_revision_carries_both_hashes(author):
    record = _draft(author, DIVISION_TRADING, f"Probe hashes {probe_id()}")
    response = author.get(f"/content/records/{record['id']}/revisions")
    assert response.status_code == 200, describe(response)
    row = response.json()[0]
    assert row.get("content_hash"), f"no content hash on a revision: {row}"
    assert row.get("approved_field_hash"), f"no approved-field hash on a revision: {row}"
    assert row["content_hash"] != row["approved_field_hash"], (
        "both hashes are the same value, so the approved set is not a narrower set"
    )


def test_a_block_type_outside_the_permitted_set_is_refused_at_write(author):
    response = author.post(
        "/content/records",
        json={
            "type": "release",
            "division_key": DIVISION_TRADING,
            "title": f"Probe block {probe_id()}",
            "slug": f"probe-{probe_id()}",
            "blocks": [{"block_type": "iframe_embed", "payload": {"src": "https://example.test"}}],
        },
    )
    assert response.status_code in (400, 422), (
        f"a block type outside {list(BLOCK_TYPES)} was accepted: {describe(response)}"
    )


def test_the_full_chain_moves_a_release_to_approved(author, legal, compliance):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe chain {probe_id()}")
    rid = record["id"]
    classified = compliance.post(
        f"/content/records/{rid}/classify", json={"disclosure_class": "general"}
    )
    assert classified.status_code == 200, describe(classified)
    approved = compliance.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "cleared"},
    )
    assert approved.status_code in (200, 201), describe(approved)
    assert approved.json()["state"] == "approved", approved.json()


def test_the_inbox_returns_the_four_queues(author):
    response = author.get("/workflow/inbox")
    assert response.status_code == 200, describe(response)
    body = response.json()
    for queue in (
        "awaiting_my_decision",
        "changes_requested_on_my_work",
        "my_drafts",
        "watching",
    ):
        assert queue in body, f"the inbox is missing {queue!r}: {sorted(body)}"
        assert isinstance(body[queue], list), f"{queue} is not a list: {body[queue]!r}"


def test_a_delegation_beyond_thirty_days_is_refused(publisher, compliance):
    far = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=45)).replace(microsecond=0)
    response = compliance.post(
        "/workflow/delegations",
        json={
            "to_principal_id": PUBLISHER_EMAIL,
            "role": "compliance_officer",
            "division_key": DIVISION_TRADING,
            "expires_at": far.isoformat().replace("+00:00", "Z"),
        },
    )
    assert response.status_code in (400, 422), (
        f"a delegation running 45 days was accepted: {describe(response)}"
    )


def test_the_exception_report_carries_its_four_row_kinds(group_admin):
    response = group_admin.get("/admin/exceptions")
    assert response.status_code == 200, describe(response)
    body = response.json()
    for key in (
        "individual_grants",
        "active_delegations",
        "fast_path_publications",
        "denied_attempts",
    ):
        assert key in body, f"the exception report is missing {key!r}: {sorted(body)}"


def test_an_author_is_denied_every_approval_endpoint(author, legal, compliance):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe self {probe_id()}")
    rid = record["id"]
    attempt = author.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "mine"},
    )
    assert attempt.status_code in DENIED, (
        f"an author approved a stage of their own submission: {describe(attempt)}"
    )
    after = compliance.get(f"/content/records/{rid}")
    assert after.status_code == 200, describe(after)
    assert after.json()["state"] == "compliance_review", (
        f"the refused approval moved the record anyway: {after.json()}"
    )


def test_an_author_holding_a_reviewer_role_cannot_clear_their_own_work(author):
    record = _draft(author, DIVISION_CAPITAL, f"Probe dual hat {probe_id()}")
    rid = record["id"]
    submitted = author.post(
        f"/workflow/records/{rid}/submit", json={"expected_state": "draft"}
    )
    assert submitted.status_code in (200, 201), describe(submitted)
    attempt = author.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "compliance_review", "expected_state": "legal_review", "comment": "mine"},
    )
    assert attempt.status_code in DENIED, (
        f"{AUTHOR_EMAIL} cleared the legal stage on a capital release they authored, "
        f"although they hold legal_reviewer on capital: {describe(attempt)}"
    )


def test_one_principal_cannot_decide_two_stages_of_one_submission(author2, legal, compliance):
    record = _through_legal(author2, legal, DIVISION_TRADING, f"Probe two stamps {probe_id()}")
    rid = record["id"]
    classified = compliance.post(
        f"/content/records/{rid}/classify", json={"disclosure_class": "general"}
    )
    assert classified.status_code == 200, describe(classified)
    attempt = legal.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "again"},
    )
    assert attempt.status_code in DENIED, (
        f"{LEGAL_EMAIL} decided both stages of one submission although they hold "
        f"both reviewer roles on trading: {describe(attempt)}"
    )
    after = compliance.get(f"/content/records/{rid}")
    assert after.json()["state"] == "compliance_review", after.json()


def test_a_group_admin_is_denied_an_unpublished_body(group_admin, author):
    record = _draft(author, DIVISION_TRADING, f"Probe admin deny {probe_id()}")
    rid = record["id"]
    response = group_admin.get(f"/content/records/{rid}")
    if response.status_code in DENIED:
        return
    body = response.json()
    revision = body.get("current_revision") or {}
    fields = revision.get("fields") if isinstance(revision, dict) else None
    assert not fields, (
        f"{GROUP_ADMIN_EMAIL} read the body of an unpublished record: {json.dumps(body)[:400]}"
    )


def test_a_group_admin_reads_record_metadata_and_the_trail(group_admin):
    listing = group_admin.get("/content/records")
    assert listing.status_code == 200, describe(listing)
    rows = listing.json()
    assert isinstance(rows, list) and rows, describe(listing)
    for row in rows[:5]:
        assert "title" in row and "state" in row, f"metadata is incomplete: {row}"
    trail = group_admin.get("/admin/audit")
    assert trail.status_code == 200, describe(trail)
    assert isinstance(trail.json(), list), describe(trail)


def test_a_record_on_an_unheld_division_is_refused_like_an_unissued_identifier(author, author2):
    record = _draft(author, DIVISION_TRADING, f"Probe scope {probe_id()}")
    held = author2.get(f"/content/records/{record['id']}")
    missing = author2.get(f"/content/records/rec-{probe_id()}")
    assert held.status_code in DENIED, (
        f"{AUTHOR2_EMAIL}, who holds capital only, read a trading record: {describe(held)}"
    )
    assert held.status_code == missing.status_code, (
        f"a record on an unheld division is refused differently from one that was never "
        f"issued: {describe(held)} versus {describe(missing)}"
    )


def test_a_publisher_cannot_approve_and_an_approver_cannot_publish(publisher, author, legal, compliance):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe roles {probe_id()}")
    rid = record["id"]
    approving = publisher.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "no"},
    )
    assert approving.status_code in DENIED, describe(approving)
    compliance.post(f"/content/records/{rid}/classify", json={"disclosure_class": "general"})
    compliance.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "cleared"},
    )
    publishing = compliance.post(
        f"/workflow/records/{rid}/publish", json={"expected_state": "approved"}
    )
    assert publishing.status_code in DENIED, (
        f"a compliance officer published a record: {describe(publishing)}"
    )


def test_an_author_cannot_set_a_disclosure_class(author, legal):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe classify {probe_id()}")
    attempt = author.post(
        f"/content/records/{record['id']}/classify",
        json={"disclosure_class": "general"},
    )
    assert attempt.status_code in DENIED, (
        f"an author set a disclosure class: {describe(attempt)}"
    )


def test_a_membership_grant_from_a_non_admin_session_is_denied(author, group_admin):
    before = group_admin.get("/admin/members")
    assert before.status_code == 200, describe(before)
    attempt = author.post(
        "/admin/memberships",
        json={
            "principal_id": AUTHOR_EMAIL,
            "division_key": DIVISION_MARITIME,
            "role": "publisher",
            "justification": "probe",
        },
    )
    assert attempt.status_code in DENIED, describe(attempt)
    after = group_admin.get("/admin/members")
    assert after.json() == before.json(), "a denied grant changed the membership set anyway"


def test_an_individual_grant_requires_a_justification(group_admin):
    response = group_admin.post(
        "/admin/memberships",
        json={
            "principal_id": AUTHOR2_EMAIL,
            "division_key": DIVISION_MARITIME,
            "role": "author",
        },
    )
    assert response.status_code in (400, 422), (
        f"an individual grant was created with no justification: {describe(response)}"
    )


def test_the_audit_trail_has_no_write_path(group_admin):
    for method, path in (
        ("post", "/admin/audit"),
        ("patch", "/admin/audit/1"),
        ("delete", "/admin/audit/1"),
        ("put", "/admin/audit/1"),
    ):
        response = getattr(group_admin, method)(path, json={})
        assert response.status_code in (401, 403, 404, 405), (
            f"{method.upper()} {path} is not refused: {describe(response)}"
        )


def test_a_denial_is_recorded_in_the_trail(author, group_admin):
    before = group_admin.get("/admin/audit", params={"decision": "deny"})
    assert before.status_code == 200, describe(before)
    count_before = len(before.json())
    author.post(
        "/admin/memberships",
        json={
            "principal_id": AUTHOR_EMAIL,
            "division_key": DIVISION_MARITIME,
            "role": "publisher",
            "justification": "probe",
        },
    )

    def grew():
        after = group_admin.get("/admin/audit", params={"decision": "deny"})
        return after.status_code == 200 and len(after.json()) > count_before

    assert settle(grew), "a denied request left no deny entry in the trail"


def test_the_audit_chain_links_each_entry_to_the_one_before(group_admin):
    response = group_admin.get("/admin/audit")
    assert response.status_code == 200, describe(response)
    rows = response.json()
    assert len(rows) >= 2, f"the trail is too short to chain: {len(rows)} entries"
    ordered = sorted(rows, key=lambda r: (r["occurred_at"], str(r["id"])))
    for earlier, later in zip(ordered, ordered[1:]):
        assert later["prev_entry_hash"] == earlier["entry_hash"], (
            f"the chain breaks between {earlier['id']} and {later['id']}"
        )


def test_the_trail_answers_who_approved_a_record(author, legal, compliance, group_admin):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe trail {probe_id()}")
    rid = record["id"]
    compliance.post(f"/content/records/{rid}/classify", json={"disclosure_class": "general"})
    compliance.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "cleared"},
    )

    def has_entry():
        response = group_admin.get("/admin/audit", params={"resource_id": rid})
        if response.status_code != 200:
            return None
        rows = response.json()
        return [r for r in rows if "approve" in str(r.get("action", ""))] or None

    rows = settle(has_entry)
    assert rows, f"no approval entry for {rid} in the trail"
    assert rows[0].get("after_hash"), f"an approval entry carries no after hash: {rows[0]}"


def test_an_edit_inside_the_approved_set_voids_the_approvals(author, legal, compliance):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe void {probe_id()}")
    rid = record["id"]
    compliance.post(f"/content/records/{rid}/classify", json={"disclosure_class": "general"})
    approved = compliance.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "cleared"},
    )
    assert approved.status_code in (200, 201), describe(approved)
    edited = author.patch(
        f"/content/records/{rid}",
        json={"blocks": [{"block_type": "paragraph", "payload": {"text": "A changed body."}}]},
    )
    assert edited.status_code == 200, describe(edited)
    after = author.get(f"/content/records/{rid}")
    assert after.json()["state"] == "draft", (
        f"editing the body of an approved release left the record at "
        f"{after.json()['state']!r} rather than returning it to draft"
    )


def test_an_edit_outside_the_approved_set_leaves_the_approvals_standing(author, legal, compliance):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe credit {probe_id()}")
    rid = record["id"]
    compliance.post(f"/content/records/{rid}/classify", json={"disclosure_class": "general"})
    compliance.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "cleared"},
    )
    edited = author.patch(f"/content/records/{rid}", json={"credit": f"Photo {probe_id()}"})
    assert edited.status_code == 200, describe(edited)
    after = author.get(f"/content/records/{rid}")
    assert after.json()["state"] == "approved", (
        f"editing only the image credit voided the approvals, leaving the record at "
        f"{after.json()['state']!r}"
    )


def test_a_market_sensitive_release_cannot_be_published_without_a_schedule(
    author, legal, compliance, publisher
):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe sensitive {probe_id()}")
    rid = record["id"]
    compliance.post(
        f"/content/records/{rid}/classify", json={"disclosure_class": "market_sensitive"}
    )
    compliance.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "cleared"},
    )
    attempt = publisher.post(
        f"/workflow/records/{rid}/publish", json={"expected_state": "approved"}
    )
    assert attempt.status_code in (400, 409, 422), (
        f"a market_sensitive release published with no scheduled instant: {describe(attempt)}"
    )
    after = publisher.get(f"/content/records/{rid}")
    assert after.json()["state"] == "approved", after.json()


def test_a_record_cannot_leave_compliance_review_without_a_class(author2, legal, compliance):
    record = _through_legal(author2, legal, DIVISION_CAPITAL, f"Probe unclassified {probe_id()}")
    attempt = compliance.post(
        f"/workflow/records/{record['id']}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "cleared"},
    )
    assert attempt.status_code in (400, 409, 422), (
        f"a record with no disclosure class reached approved: {describe(attempt)}"
    )


def test_an_embargo_instant_in_the_past_is_rejected(author, legal, compliance, publisher):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe past {probe_id()}")
    rid = record["id"]
    compliance.post(f"/content/records/{rid}/classify", json={"disclosure_class": "general"})
    compliance.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "cleared"},
    )
    attempt = publisher.post(
        f"/workflow/records/{rid}/schedule",
        json={"embargo_at": _past(3600), "expected_state": "approved"},
    )
    assert attempt.status_code in (400, 409, 422), (
        f"an embargo instant in the past was accepted: {describe(attempt)}"
    )
    after = publisher.get(f"/content/records/{rid}")
    assert after.json()["state"] == "approved", (
        f"the rejected schedule published the record anyway: {after.json()}"
    )


def test_a_transition_from_a_stale_state_is_rejected_as_a_conflict(author, legal):
    record = _draft(author, DIVISION_TRADING, f"Probe stale {probe_id()}")
    rid = record["id"]
    author.post(f"/workflow/records/{rid}/submit", json={"expected_state": "draft"})
    attempt = legal.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "compliance_review", "expected_state": "draft", "comment": "stale"},
    )
    assert attempt.status_code in (400, 409, 422), (
        f"a transition naming the wrong current state was accepted: {describe(attempt)}"
    )


def test_two_concurrent_approvals_produce_one_success(author, legal, compliance):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe race {probe_id()}")
    rid = record["id"]
    compliance.post(f"/content/records/{rid}/classify", json={"disclosure_class": "general"})
    token = token_for(COMPLIANCE_EMAIL)
    payload = {"to": "approved", "expected_state": "compliance_review", "comment": "cleared"}

    def approve():
        with appclient.client(token) as handle:
            return handle.post(f"/workflow/records/{rid}/transition", json=payload).status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: approve(), range(2)))

    wins = [code for code in results if code in (200, 201)]
    assert len(wins) == 1, (
        f"two simultaneous approvals both succeeded or both failed: {results}"
    )
    after = compliance.get(f"/content/records/{rid}")
    assert after.json()["state"] == "approved", after.json()


def test_two_concurrent_edits_from_one_revision_produce_one_success(author):
    record = _draft(author, DIVISION_TRADING, f"Probe edit race {probe_id()}")
    rid = record["id"]
    revision = author.get(f"/content/records/{rid}").json()["current_revision"]["id"]
    token = token_for(AUTHOR_EMAIL)

    def edit(label):
        with appclient.client(token) as handle:
            return handle.patch(
                f"/content/records/{rid}",
                json={"title": f"Probe edit race {label}", "expected_revision_id": revision},
            ).status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(edit, ("a", "b")))

    wins = [code for code in results if code == 200]
    assert len(wins) == 1, f"two edits from one revision both succeeded: {results}"


def test_a_repeated_publish_with_one_idempotency_key_publishes_once(
    author, legal, compliance, publisher, stranger
):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe idem {probe_id()}")
    rid = record["id"]
    compliance.post(f"/content/records/{rid}/classify", json={"disclosure_class": "general"})
    compliance.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "cleared"},
    )
    key = f"probe-{probe_id()}"
    before = counter_value(stranger)
    first = publisher.post(
        f"/workflow/records/{rid}/publish",
        json={"expected_state": "approved"},
        headers={"Idempotency-Key": key},
    )
    second = publisher.post(
        f"/workflow/records/{rid}/publish",
        json={"expected_state": "approved"},
        headers={"Idempotency-Key": key},
    )
    assert first.status_code in (200, 201), describe(first)
    assert second.status_code in (200, 201, 409), describe(second)

    def settled():
        return counter_value(stranger) == before + 1

    assert settle(settled), (
        f"the counter moved by more than one for a repeated publish: "
        f"{before} then {counter_value(stranger)}"
    )


def test_an_unknown_field_in_a_request_body_is_refused(author):
    response = author.post(
        "/content/records",
        json={
            "type": "release",
            "division_key": DIVISION_TRADING,
            "title": f"Probe unknown {probe_id()}",
            "slug": f"probe-{probe_id()}",
            "blocks": [],
            "not_a_real_field": True,
        },
    )
    assert response.status_code in (400, 422), (
        f"an unknown field was ignored rather than refused: {describe(response)}"
    )


def test_the_enquiry_form_rejects_a_short_message_and_writes_nothing(stranger):
    response = stranger.post(
        "/public/enquiries",
        json={
            "subject_area": DIVISION_TRADING,
            "name": "Probe Caller",
            "country": "Singapore",
            "email": f"probe-{probe_id()}@example.com",
            "message": "too short",
            "consent": True,
        },
    )
    assert response.status_code in (400, 422), (
        f"a message under the stated floor was accepted: {describe(response)}"
    )
    assert code_of(response) == "validation_failed", describe(response)


def test_the_enquiry_form_requires_an_explicit_consent(stranger):
    response = stranger.post(
        "/public/enquiries",
        json={
            "subject_area": "general",
            "name": "Probe Caller",
            "country": "Switzerland",
            "email": f"probe-{probe_id()}@example.com",
            "message": "A probe enquiry long enough to clear the stated floor of twenty.",
            "consent": False,
        },
    )
    assert response.status_code in (400, 422), (
        f"an enquiry with consent refused was accepted: {describe(response)}"
    )


def test_an_enquiry_routes_by_the_declared_country(stranger):
    cases = {
        "Singapore": "Singapore",
        "United Arab Emirates": "Dubai",
        "Switzerland": "Geneva",
        "Brazil": "Geneva",
    }
    for country, office in cases.items():
        response = stranger.post(
            "/public/enquiries",
            json={
                "subject_area": "general",
                "name": "Probe Caller",
                "country": country,
                "email": f"probe-{probe_id()}@example.com",
                "message": "A probe enquiry long enough to clear the stated floor of twenty.",
                "consent": True,
            },
        )
        assert response.status_code in (200, 201), describe(response)
        body = response.json()
        assert body.get("public_reference"), f"no reference returned: {body}"
        assert office.lower() in str(body.get("responding_office", "")).lower(), (
            f"{country!r} routed to {body.get('responding_office')!r}, the brief routes "
            f"it to {office}"
        )


def test_an_unknown_subject_area_is_refused(stranger):
    response = stranger.post(
        "/public/enquiries",
        json={
            "subject_area": f"not-a-division-{probe_id()}",
            "name": "Probe Caller",
            "country": "Switzerland",
            "email": f"probe-{probe_id()}@example.com",
            "message": "A probe enquiry long enough to clear the stated floor of twenty.",
            "consent": True,
        },
    )
    assert response.status_code in (400, 422), describe(response)


def test_a_slug_that_was_never_issued_answers_not_found(stranger):
    response = stranger.get(f"/public/releases/probe-{probe_id()}")
    assert response.status_code == 404, describe(response)


def test_a_search_query_under_two_characters_returns_the_no_query_state(stranger):
    response = stranger.get("/public/search", params={"q": "a"})
    assert response.status_code == 200, (
        f"a one-character query answered as an error rather than as the no-query state: "
        f"{describe(response)}"
    )
    assert response.json() == [], f"a one-character query returned results: {response.json()}"


def test_seeded_rows_are_stored_exactly_once(backend):
    rows = backend.query(
        "SELECT email, COUNT(*) AS n FROM principals GROUP BY email HAVING COUNT(*) > 1"
    )
    assert not rows, f"seeding duplicated principals: {rows}"


def test_the_counter_matches_the_published_releases_in_the_store(stranger):
    value = counter_value(stranger)
    assert value == PUBLISHED_RELEASE_COUNT, (
        f"the counter reads {value}, the brief seeds {PUBLISHED_RELEASE_COUNT} published releases"
    )
    page_one = public_releases(stranger)
    page_two = public_releases(stranger, page=2)
    total = len(page_one["items"]) + len(page_two["items"])
    assert total == PUBLISHED_RELEASE_COUNT, (
        f"the archive carries {total} releases across two pages, the counter says {value}"
    )


def test_the_archive_pages_at_the_stated_size(stranger):
    page_one = public_releases(stranger)
    assert len(page_one["items"]) == ARCHIVE_PAGE_SIZE, (
        f"page one carries {len(page_one['items'])} cards, the brief pins {ARCHIVE_PAGE_SIZE}"
    )
    page_two = public_releases(stranger, page=2)
    assert len(page_two["items"]) == PUBLISHED_RELEASE_COUNT - ARCHIVE_PAGE_SIZE, page_two
    first_ids = {row["slug"] for row in page_one["items"]}
    second_ids = {row["slug"] for row in page_two["items"]}
    assert not (first_ids & second_ids), f"a release appears on both pages: {first_ids & second_ids}"


def test_the_archive_is_ordered_newest_first(stranger):
    items = public_releases(stranger)["items"]
    assert items[0]["title"] == NEWEST_RELEASE_TITLE, (
        f"the archive opens on {items[0]['title']!r}, the brief seeds "
        f"{NEWEST_RELEASE_TITLE!r} as the newest"
    )
    tail = public_releases(stranger, page=2)["items"]
    assert tail[-1]["title"] == OLDEST_RELEASE_TITLE, (
        f"the archive ends on {tail[-1]['title']!r}, the brief seeds "
        f"{OLDEST_RELEASE_TITLE!r} as the oldest"
    )


def test_the_archive_filters_by_division_and_by_year(stranger):
    trading = public_releases(stranger, division=DIVISION_TRADING)
    for row in trading["items"]:
        assert row["division_key"] == DIVISION_TRADING, row
    year = public_releases(stranger, year=2023)
    for row in year["items"]:
        assert row["published_at"].startswith("2023"), row
    assert len(year["items"]) < PUBLISHED_RELEASE_COUNT, (
        "the year filter returned every release, so it filtered nothing"
    )


def test_a_filter_combination_with_no_result_is_empty_rather_than_an_error(stranger):
    body = public_releases(stranger, division=DIVISION_VENTURE, year=2019)
    assert body["items"] == [], f"an impossible filter returned rows: {body['items']}"


def test_a_published_release_reads_back_what_the_record_holds(stranger, publisher):
    items = public_releases(stranger)["items"]
    slug = items[0]["slug"]
    public = stranger.get(f"/public/releases/{slug}")
    assert public.status_code == 200, describe(public)
    body = public.json()
    assert body["title"] == items[0]["title"], (
        f"the archive card and the release page disagree: {items[0]['title']!r} "
        f"versus {body['title']!r}"
    )
    assert body.get("blocks"), f"the release page carries no body blocks: {body}"
    assert body.get("published_at"), f"the release page carries no publication instant: {body}"


def test_a_regulated_release_carries_a_frozen_disclaimer_version(stranger):
    found = None
    for page in (1, 2):
        for row in public_releases(stranger, page=page)["items"]:
            detail = stranger.get(f"/public/releases/{row['slug']}").json()
            if detail.get("disclaimer"):
                found = detail
                break
        if found:
            break
    if found is None:
        return
    disclaimer = found["disclaimer"]
    assert disclaimer.get("policy_reference_code"), f"no register code on a disclaimer: {disclaimer}"
    assert disclaimer.get("policy_version"), f"no frozen version on a disclaimer: {disclaimer}"


def test_the_withdrawn_release_answers_gone_and_keeps_its_record(stranger, publisher):
    record = record_titled(publisher, WITHDRAWN_RELEASE_TITLE, division=DIVISION_GROUP)
    assert record is not None, f"the seeded withdrawn release is absent"
    assert record["state"] == "unpublished", record
    response = stranger.get(f"/public/releases/{record['slug']}")
    assert response.status_code == GONE, (
        f"a withdrawn release answered {response.status_code} rather than gone: "
        f"{describe(response)}"
    )
    assert code_of(response) == "gone", describe(response)
    titles = {row["title"] for page in (1, 2) for row in public_releases(stranger, page=page)["items"]}
    assert WITHDRAWN_RELEASE_TITLE not in titles, "a withdrawn release is still in the archive"


def test_a_withdrawal_carries_its_reason_and_instant(publisher):
    record = record_titled(publisher, WITHDRAWN_RELEASE_TITLE, division=DIVISION_GROUP)
    detail = publisher.get(f"/content/records/{record['id']}")
    assert detail.status_code == 200, describe(detail)
    body = detail.json()
    assert body.get("unpublish_reason") == WITHDRAWAL_REASON, (
        f"the seeded withdrawal reason is {body.get('unpublish_reason')!r}, the brief pins "
        f"{WITHDRAWAL_REASON!r}"
    )
    assert body.get("unpublished_at"), f"no withdrawal instant on the record: {body}"


def test_a_retitled_published_release_keeps_its_old_address(publisher, stranger):
    items = public_releases(stranger)["items"]
    slug = items[0]["slug"]
    record = None
    for row in records_for(publisher, type="release", state="published"):
        if row.get("slug") == slug:
            record = row
            break
    assert record is not None, f"the published release at {slug!r} was not found in the console"
    renamed = publisher.patch(
        f"/content/records/{record['id']}", json={"title": f"{record['title']} (revised)"}
    )
    assert renamed.status_code == 200, describe(renamed)

    def old_still_resolves():
        response = stranger.get(f"/public/releases/{slug}", follow_redirects=True)
        return response.status_code == 200

    assert settle(old_still_resolves), (
        f"the address {slug!r} stopped resolving after the release was retitled"
    )


def test_the_published_projection_carries_no_unpublished_record(stranger, publisher):
    drafts = records_for(publisher, state="draft")
    assert drafts, "no draft record is seeded, so the projection boundary cannot be observed"
    for row in drafts:
        response = stranger.get(f"/public/releases/{row['slug']}")
        assert response.status_code in (404, 410), (
            f"a draft record is readable at its public address: {describe(response)}"
        )


def test_a_seeded_release_has_a_stable_block_identifier_across_revisions(author):
    record = _draft(author, DIVISION_TRADING, f"Probe block id {probe_id()}")
    rid = record["id"]
    first = author.get(f"/content/records/{rid}").json()
    before = [b["stable_block_id"] for b in first["current_revision"]["blocks"]]
    author.patch(f"/content/records/{rid}", json={"title": f"Probe block id {probe_id()}"})
    second = author.get(f"/content/records/{rid}").json()
    after = [b["stable_block_id"] for b in second["current_revision"]["blocks"]]
    assert before == after, (
        f"the stable block identifiers changed across a revision: {before} then {after}"
    )


def test_the_published_route_declares_its_own_title_and_description(site):
    seen = {}
    for route in ("/", "/trading/", "/news/", "/contact/"):
        response = site.get(route)
        assert response.status_code == 200, describe(response)
        html = response.text
        title = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
        description = re.search(
            r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.S | re.I
        )
        assert title, f"{route} declares no title"
        assert description, f"{route} declares no description"
        seen[route] = (title.group(1).strip(), description.group(1).strip())
    assert len(set(seen.values())) == len(seen), (
        f"two public routes share a title and a description: {seen}"
    )


def test_every_public_route_declares_a_social_preview_image_that_resolves(site):
    for route in ("/", "/news/", "/contact/"):
        response = site.get(route)
        assert response.status_code == 200, describe(response)
        image = re.search(
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']',
            response.text,
            re.S | re.I,
        )
        assert image, f"{route} declares no social preview image"
        target = image.group(1)
        if target.startswith("/"):
            target = APP_URL.rstrip("/") + target
        head = httpx.get(target, timeout=30.0, follow_redirects=True)
        assert head.status_code == 200, f"{route} declares an image that does not resolve: {target}"


def test_the_document_head_declares_a_favicon_that_resolves(site):
    response = site.get("/")
    assert response.status_code == 200, describe(response)
    icon = re.search(
        r'<link[^>]+rel=["\'][^"\']*icon[^"\']*["\'][^>]+href=["\'](.*?)["\']',
        response.text,
        re.S | re.I,
    )
    assert icon, "the document head declares no favicon"
    target = icon.group(1)
    if target.startswith("/"):
        target = APP_URL.rstrip("/") + target
    fetched = httpx.get(target, timeout=30.0, follow_redirects=True)
    assert fetched.status_code == 200, f"the declared favicon does not resolve: {target}"


def test_every_response_carries_the_security_headers(site):
    response = site.get("/")
    assert response.status_code == 200, describe(response)
    lowered = {name.lower() for name in response.headers}
    for name in SECURITY_HEADER_NAMES:
        assert name in lowered, f"{name} is absent: {sorted(lowered)}"
    assert response.headers.get("x-content-type-options", "").lower() == "nosniff", (
        response.headers.get("x-content-type-options")
    )


def test_nothing_the_browser_downloads_carries_a_credential(site):
    secrets = [
        CORPUS_PASSWORD,
        os.environ.get("STORAGE_ACCESS_KEY", "minioadmin"),
        os.environ.get("STORAGE_SECRET_KEY", "minio-root-3d81f7a2"),
    ]
    response = site.get("/")
    assert response.status_code == 200, describe(response)
    documents = [response.text]
    for match in re.findall(r'src=["\'](/[^"\']+\.js)["\']', response.text):
        fetched = site.get(match)
        if fetched.status_code == 200:
            documents.append(fetched.text)
    for body in documents:
        for secret in secrets:
            assert secret not in body, (
                f"the browser downloaded a document carrying the credential {secret!r}"
            )


def test_an_unknown_address_renders_the_products_own_not_found_page(site):
    response = site.get(f"/definitely-not-a-route-{probe_id()}")
    assert response.status_code == 404, describe(response)
    body = response.text
    assert "Calder" in body, "the not-found page is a bare server document, not the product's own"
    assert "/news/" in body, "the not-found page offers no way back to the release archive"


def test_the_error_shape_is_one_shape_everywhere(stranger, author):
    rejections = [
        stranger.get("/content/records"),
        stranger.get(f"/public/releases/probe-{probe_id()}"),
        author.post("/content/records", json={"type": "release"}),
    ]
    for response in rejections:
        assert response.status_code >= 400, describe(response)
        body = response.json()
        error = body.get("error") if isinstance(body, dict) else None
        assert isinstance(error, dict), f"the rejection is not the one error shape: {body}"
        assert error.get("code"), f"no machine-readable code: {error}"
        assert error.get("message"), f"no human-readable message: {error}"
        assert error.get("request_id"), f"no request identifier: {error}"


def test_a_request_identifier_is_echoed_on_the_response(stranger):
    supplied = f"probe-{probe_id()}"
    response = stranger.get("/health", headers={"X-Request-Id": supplied})
    assert response.status_code == 200, describe(response)
    echoed = response.headers.get("x-request-id")
    assert echoed, "no request identifier on the response"
    assert echoed == supplied, f"the caller supplied {supplied!r}, the app echoed {echoed!r}"




def _document_text(html: str) -> str:
    stripped = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S | re.I)
    stripped = re.sub(r"<style\b.*?</style>", " ", stripped, flags=re.S | re.I)
    stripped = re.sub(r"<[^>]+>", " ", stripped)
    return re.sub(r"\s+", " ", stripped)


def test_the_home_route_carries_its_pinned_copy(site):
    response = site.get("/")
    assert response.status_code == 200, describe(response)
    text = _document_text(response.text)
    for pinned in (
        CHAPTER_ONE_HEADLINE,
        CHAPTER_TWO_HEADING,
        TRADING_PROPOSITION,
        CAPITAL_PROPOSITION,
        VENTURE_PROPOSITION,
        SUSTAINABILITY_HEADING,
        PEOPLE_STATEMENT,
        RESPONSIBILITY_HEADING,
    ):
        assert pinned in text, (
            f"the home document does not carry the pinned string {pinned!r}. A headline "
            f"split into characters must still read as one continuous string."
        )
    for label in ("Calder Group", "Calder Trading", "Calder Capital", "Calder Maritime",
                  "Kite Energy", "News", "Menu"):
        assert label in text, f"the home document does not carry the label {label!r}"
    year = str(dt.datetime.now(dt.timezone.utc).year)
    assert re.search(r"\(c\)\s*(20\d\d)", text), "the footer carries no copyright line"
    stated = re.search(r"\(c\)\s*(20\d\d)", text).group(1)
    assert stated in (year, "2023"), (
        f"the copyright year reads {stated!r}; it is derived from the latest publication "
        f"instant or the build instant, never authored"
    )


def test_the_home_route_exposes_its_four_chapter_anchors(site):
    response = site.get("/")
    assert response.status_code == 200, describe(response)
    html = response.text
    for anchor in ANCHORS:
        ident = anchor.lstrip("#")
        assert re.search(rf'id=["\']{ident}["\']', html), (
            f"{anchor} is not a real address on the home document"
        )
        landed = site.get("/" + anchor)
        assert landed.status_code == 200, describe(landed)
    footer = site.get("/news/")
    assert footer.status_code == 200, describe(footer)
    assert "/#Sustainability" in footer.text, (
        "the footer of a route other than the home page does not link to /#Sustainability"
    )


def test_the_public_document_loads_no_third_party_origin(site):
    response = site.get("/")
    assert response.status_code == 200, describe(response)
    own = APP_URL.rstrip("/")
    references = re.findall(r'(?:src|href)=["\'](https?://[^"\']+)["\']', response.text)
    outside = [ref for ref in references if not ref.startswith(own)]
    assert not outside, (
        f"the public document reaches {len(outside)} origin(s) other than its own: "
        f"{outside[:5]}"
    )



def test_an_uploaded_object_lands_in_the_bucket_at_the_key_scheme(author, store):
    record = _draft(author, DIVISION_TRADING, f"Probe media {probe_id()}")
    payload = f"probe-bytes-{probe_id()}".encode()
    digest = hashlib.sha256(payload).hexdigest()
    response = author.post(
        f"/content/records/{record['id']}/media",
        files={"file": ("probe.png", payload, "image/png")},
        data={"filename": "probe.png", "alt_text": "A probe image."},
    )
    assert response.status_code in (200, 201), describe(response)
    body = response.json()
    key = body["object_key"]
    assert key.startswith(KEY_SCHEME_PREFIX + DIVISION_TRADING + "/"), (
        f"the object key {key!r} does not follow media/{{division_key}}/..."
    )
    assert digest in key, f"the object key {key!r} carries no checksum of the bytes"
    assert store.object_exists(key), (
        f"nothing is in the bucket at {key!r}, so the bytes were not written to the store"
    )
    assert store.object_bytes(key) == payload, "the stored object does not match the uploaded bytes"


def test_media_without_alternative_text_is_refused(author):
    record = _draft(author, DIVISION_TRADING, f"Probe alt {probe_id()}")
    response = author.post(
        f"/content/records/{record['id']}/media",
        files={"file": ("probe.png", b"probe-bytes", "image/png")},
        data={"filename": "probe.png", "alt_text": ""},
    )
    assert response.status_code in (400, 422), (
        f"a media record with empty alternative text was created: {describe(response)}"
    )


def test_an_unpublished_records_object_is_refused_to_an_anonymous_caller(author, stranger):
    record = _draft(author, DIVISION_TRADING, f"Probe closed media {probe_id()}")
    response = author.post(
        f"/content/records/{record['id']}/media",
        files={"file": ("probe.png", f"probe-{probe_id()}".encode(), "image/png")},
        data={"filename": "probe.png", "alt_text": "A probe image."},
    )
    assert response.status_code in (200, 201), describe(response)
    media_id = response.json()["id"]
    public = stranger.get(f"/public/media/{media_id}")
    assert public.status_code in (403, 404), (
        f"the lead image of a draft release is served to an anonymous caller: {describe(public)}"
    )
    private = stranger.get(f"/media/{media_id}")
    assert private.status_code in DENIED, describe(private)


def test_the_embargoed_release_lead_image_is_closed_to_the_public(embargoed_release, publisher, stranger):
    detail = publisher.get(f"/content/records/{embargoed_release['id']}")
    assert detail.status_code == 200, describe(detail)
    media = detail.json().get("lead_media_id")
    assert media, f"the seeded embargoed release carries no lead image: {detail.json()}"
    response = stranger.get(f"/public/media/{media}")
    assert response.status_code in (403, 404), (
        f"the lead image of an embargoed release is public: {describe(response)}"
    )


def test_a_media_object_belonging_to_a_published_release_is_public(stranger):
    for page in (1, 2):
        for row in public_releases(stranger, page=page)["items"]:
            detail = stranger.get(f"/public/releases/{row['slug']}").json()
            media = detail.get("lead_media_id")
            if not media:
                continue
            response = stranger.get(f"/public/media/{media}")
            assert response.status_code == 200, (
                f"the lead image of a published release is refused: {describe(response)}"
            )
            assert response.content, "the lead image responded with no bytes"
            return
    assert False, "no published release carries a lead image"


def test_an_embargoed_release_does_not_exist_publicly(embargoed_release, stranger, publisher):
    slug = embargoed_release["slug"]
    direct = stranger.get(f"/public/releases/{slug}")
    unissued = stranger.get(f"/public/releases/probe-{probe_id()}")
    assert direct.status_code == 404, (
        f"an embargoed release answers {direct.status_code} at its own address: {describe(direct)}"
    )
    assert direct.status_code == unissued.status_code, (
        f"an embargoed slug is refused differently from one never issued: "
        f"{describe(direct)} versus {describe(unissued)}"
    )
    titles = {
        row["title"] for page in (1, 2) for row in public_releases(stranger, page=page)["items"]
    }
    assert EMBARGOED_RELEASE_TITLE not in titles, "an embargoed release is listed in the archive"
    found = stranger.get("/public/search", params={"q": "naphtha supply arrangement"})
    assert found.status_code == 200, describe(found)
    assert all(row["title"] != EMBARGOED_RELEASE_TITLE for row in found.json()), (
        "an embargoed release is findable in the public search"
    )
    to_publisher = publisher.get(f"/content/records/{embargoed_release['id']}")
    assert to_publisher.status_code == 200, (
        f"a publisher on the record's own division cannot read the embargoed record: "
        f"{describe(to_publisher)}"
    )
    assert to_publisher.json().get("embargo_at"), to_publisher.json()


def test_a_scheduled_release_publishes_once_when_its_instant_passes(
    author, legal, compliance, publisher, stranger
):
    record = _through_legal(author, legal, DIVISION_TRADING, f"Probe schedule {probe_id()}")
    rid = record["id"]
    slug = publisher.get(f"/content/records/{rid}").json()["slug"]
    compliance.post(
        f"/content/records/{rid}/classify", json={"disclosure_class": "market_sensitive"}
    )
    compliance.post(
        f"/workflow/records/{rid}/transition",
        json={"to": "approved", "expected_state": "compliance_review", "comment": "cleared"},
    )
    before = counter_value(stranger)
    scheduled = publisher.post(
        f"/workflow/records/{rid}/schedule",
        json={"embargo_at": _future(10), "expected_state": "approved"},
    )
    assert scheduled.status_code in (200, 201), describe(scheduled)
    assert scheduled.json()["state"] == "embargoed", scheduled.json()
    closed = stranger.get(f"/public/releases/{slug}")
    assert closed.status_code == 404, (
        f"the release was public before its instant: {describe(closed)}"
    )

    def became_public():
        return stranger.get(f"/public/releases/{slug}").status_code == 200

    assert settle(became_public, attempts=40), (
        f"the release never became public after its embargo instant passed"
    )
    assert counter_value(stranger) == before + 1, (
        f"the counter moved by more than one for one scheduled publication: "
        f"{before} then {counter_value(stranger)}"
    )
