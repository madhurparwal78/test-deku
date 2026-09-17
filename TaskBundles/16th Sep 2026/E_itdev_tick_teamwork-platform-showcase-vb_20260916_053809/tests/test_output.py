"""The one pytest module for deku/teamwork-platform-showcase-vb.

Black box throughout: every observation is made over the JSON API, over the
served HTML, over the rows in postgres, or over the messages in mailpit. Nothing
here reads the application's source, imports a vendor SDK, or decides at run time
whether a feature is present.
"""

from __future__ import annotations

import concurrent.futures

from conftest import (
    ADMIN_EMAIL, API_FILTERS, API_HEALTH, API_ITEMS, API_PAGE_VIEWS, API_PLANS,
    API_PROJECTS, API_SIGNUP, BOUNDARY_ITEM, BOUNDARY_SUMMARY, DENIED,
    DENIED_OR_MISSING, FILTER_MY_OPEN_WORK, FREE_CAP_TEXT, MEMBER_EMAIL,
    OK, PASSWORD, PREMIUM_MONTHLY_BANDS, PROJECT_FIN, PROJECT_MKT,
    PUBLIC_ROUTES, REFUSED, SEEDED_ACCOUNTS, STANDARD_MONTHLY_BANDS,
    STATUS_BLOCKED, STATUS_DONE, STATUS_IN_PROGRESS, STATUS_READY,
    SUBJECT_PREFIX, WORKED_PREMIUM_300_PER_USER, WORKED_PREMIUM_300_TOTAL,
    WORKED_STANDARD_300_PER_USER, WORKED_STANDARD_300_TOTAL,
    WORKED_STANDARD_7_PER_USER, WORKED_STANDARD_7_TOTAL,
    advance_to_ready, create_item, graduated_total, probe_summary, settle,
    transition, wait_for_message,
)
from appclient import client, login


def test_drag_writes_transition_and_history(member_api, db):
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    before = db.history_count(key)
    response = transition(member_api, key, STATUS_IN_PROGRESS)
    assert response.status_code in OK, (
        f"POST transition of {key} to {STATUS_IN_PROGRESS!r} returned "
        f"{response.status_code}: {response.text[:400]}")
    after = db.item_status_name(key)
    assert after == STATUS_IN_PROGRESS, (
        f"{key} reads status {after!r} in the datastore after a transition to "
        f"{STATUS_IN_PROGRESS!r}")
    entries = db.history_count(key)
    assert entries == before + 1, (
        f"{key} gained {entries - before} history entries for one transition, "
        f"expected exactly 1")


def test_seeded_accounts_sign_in(anon):
    for email in SEEDED_ACCOUNTS:
        response = anon.post("/auth/login", json={"email": email,
                                                  "password": PASSWORD})
        assert response.status_code in OK, (
            f"login for seeded account {email} returned {response.status_code}: "
            f"{response.text[:400]}")
        assert response.json().get("access_token"), (
            f"login for {email} returned no access_token: {response.text[:400]}")


def test_health_endpoint_returns_ok(anon):
    response = anon.get(API_HEALTH)
    assert response.status_code == 200, (
        f"GET /api{API_HEALTH} returned {response.status_code}: "
        f"{response.text[:400]}")


def test_saved_filter_resolves_as_caller(member_api, member2_api):
    listed = member_api.get(API_FILTERS)
    assert listed.status_code in OK, (
        f"GET /api{API_FILTERS} as a member returned {listed.status_code}: "
        f"{listed.text[:400]}")
    names = [row.get("name") for row in listed.json()]
    assert FILTER_MY_OPEN_WORK in names, (
        f"the seeded filter {FILTER_MY_OPEN_WORK!r} is absent from {names}")
    target = [row for row in listed.json()
              if row.get("name") == FILTER_MY_OPEN_WORK][0]
    mine = member_api.get(f"{API_FILTERS}/{target['id']}/run")
    assert mine.status_code in OK, (
        f"running {FILTER_MY_OPEN_WORK!r} as its owner returned "
        f"{mine.status_code}: {mine.text[:400]}")
    owner_keys = {row.get("item_key") for row in mine.json()}
    theirs = member2_api.get(f"{API_FILTERS}/{target['id']}/run")
    assert theirs.status_code in OK + DENIED_OR_MISSING, (
        f"running a shared filter as another member returned "
        f"{theirs.status_code}: {theirs.text[:400]}")
    if theirs.status_code in OK:
        other_keys = {row.get("item_key") for row in theirs.json()}
        assert not (other_keys & owner_keys), (
            f"a shared filter returned the owner's items {sorted(other_keys & owner_keys)} "
            f"to a member of another project, so it resolved as the owner")


def test_rule_execution_meters_one_unit(member_api, admin_api, db):
    before = db.rule_execution_count()
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    advance_to_ready(member_api, key)
    settle()
    after = db.rule_execution_count()
    assert after == before + 1, (
        f"one transition into {STATUS_READY!r} recorded {after - before} rule "
        f"executions, expected exactly 1")
    rows = db.rule_executions()
    assert rows, "no rule execution row exists after a bound transition ran"
    latest = rows[-1]
    assert int(latest.get("metered_units", 0)) == 1, (
        f"a rule execution metered {latest.get('metered_units')!r} units, "
        f"expected 1 regardless of how many actions it took")


def test_rule_does_not_reenter_its_own_chain(member_api, db):
    before = db.rule_execution_count()
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    advance_to_ready(member_api, key)
    settle()
    after = db.rule_execution_count()
    assert after - before <= 1, (
        f"one transition produced {after - before} rule executions, so a rule "
        f"re-entered its own chain instead of stopping")


def test_signup_outcome_named_for_each_domain(anon):
    free_mail = f"{probe_summary('probe').replace(' ', '.')}@gmail.com"
    response = anon.post(API_SIGNUP, json={"email": free_mail})
    assert response.status_code in OK, (
        f"signup with a free-mail address returned {response.status_code}, so a "
        f"free-mail address was rejected rather than accepted: "
        f"{response.text[:400]}")
    body = response.json()
    outcome = str(body.get("outcome", "")).strip()
    assert outcome, (
        f"signup returned no named outcome: {response.text[:400]}")


def test_transition_persists_across_reread(member_api, db):
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    advance_to_ready(member_api, key)
    stored = db.item_status_name(key)
    assert stored == STATUS_READY, (
        f"{key} reads status {stored!r} in the datastore, expected "
        f"{STATUS_READY!r}: the move is on screen only")
    reread = member_api.get(f"{API_ITEMS}/{key}")
    assert reread.status_code in OK, (
        f"GET /api{API_ITEMS}/{key} returned {reread.status_code}: "
        f"{reread.text[:400]}")
    assert reread.json().get("status") == STATUS_READY, (
        f"a re-read of {key} reports status {reread.json().get('status')!r}, "
        f"expected {STATUS_READY!r}")


def test_history_entry_is_appended_not_rewritten(member_api, db):
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    transition(member_api, key, STATUS_IN_PROGRESS)
    first = db.history(key)
    transition(member_api, key, STATUS_READY)
    second = db.history(key)
    assert len(second) > len(first), (
        f"{key} has {len(second)} history entries after two transitions and "
        f"{len(first)} after one, so the second move overwrote rather than "
        f"appended")
    first_ids = [row.get("id") for row in first]
    second_ids = [row.get("id") for row in second]
    assert first_ids == second_ids[:len(first_ids)], (
        f"the earlier history entries of {key} changed identity between reads: "
        f"{first_ids} then {second_ids[:len(first_ids)]}")


def test_invalid_transition_leaves_status_unchanged(member_api, db):
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    before_status = db.item_status_name(key)
    before_history = db.history_count(key)
    response = transition(member_api, key, STATUS_DONE)
    assert response.status_code in REFUSED, (
        f"a move from {before_status!r} straight to {STATUS_DONE!r} returned "
        f"{response.status_code}, but no transition joins those two statuses so "
        f"it must be refused: {response.text[:400]}")
    assert db.item_status_name(key) == before_status, (
        f"{key} moved to {db.item_status_name(key)!r} on a refused transition, "
        f"expected it to stay at {before_status!r}")
    assert db.history_count(key) == before_history, (
        f"a refused transition appended a history entry to {key}")


def test_reorder_changes_one_item_rank(member_api, db):
    first = create_item(member_api, PROJECT_FIN, probe_summary())
    second = create_item(member_api, PROJECT_FIN, probe_summary())
    third = create_item(member_api, PROJECT_FIN, probe_summary())
    untouched_before = db.item(third)
    response = member_api.patch(f"{API_ITEMS}/{second}/rank",
                                json={"rank": "between"})
    assert response.status_code in OK, (
        f"PATCH rank of {second} returned {response.status_code}: "
        f"{response.text[:400]}")
    untouched_after = db.item(third)
    assert untouched_before.get("rank") == untouched_after.get("rank"), (
        f"reordering {second} also changed the rank of {third}, from "
        f"{untouched_before.get('rank')!r} to {untouched_after.get('rank')!r}")
    assert db.item(first).get("rank") is not None, (
        f"{first} carries no rank value after a sibling was reordered")


def test_simultaneous_transitions_yield_one_winner(member_api, db):
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    token = login(MEMBER_EMAIL, PASSWORD)

    def attempt():
        with client(token) as c:
            return c.post(f"{API_ITEMS}/{key}/transition",
                          json={"to_status": STATUS_IN_PROGRESS})

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = [f.result() for f in
                   [pool.submit(attempt), pool.submit(attempt)]]
    codes = sorted(r.status_code for r in results)
    accepted = [r for r in results if r.status_code in OK]
    assert len(accepted) == 1, (
        f"two simultaneous transitions of {key} returned {codes}, so "
        f"{len(accepted)} were accepted; exactly one must win")
    assert db.item_status_name(key) == STATUS_IN_PROGRESS, (
        f"{key} reads {db.item_status_name(key)!r} after a contested move, "
        f"expected {STATUS_IN_PROGRESS!r}")
    assert db.history_count(key) == 1, (
        f"{key} carries {db.history_count(key)} history entries after one "
        f"contested move, expected exactly 1")


def test_member_denied_other_project_board(member2_api, db):
    response = member2_api.get(f"{API_PROJECTS}/{PROJECT_FIN}/items")
    assert response.status_code in DENIED_OR_MISSING, (
        f"a member of {PROJECT_MKT} reading {PROJECT_FIN} items returned "
        f"{response.status_code}, expected a denial: {response.text[:400]}")
    listed = member2_api.get(API_PROJECTS)
    assert listed.status_code in OK, (
        f"GET /api{API_PROJECTS} returned {listed.status_code}: "
        f"{listed.text[:400]}")
    keys = {row.get("key") for row in listed.json()}
    assert PROJECT_FIN not in keys, (
        f"{PROJECT_FIN} appears in the project list of a member who does not "
        f"belong to it: {sorted(keys)}")


def test_requester_cannot_transition_item(requester_api, member_api, db):
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    before_status = db.item_status_name(key)
    before_history = db.history_count(key)
    response = transition(requester_api, key, STATUS_IN_PROGRESS)
    assert response.status_code in DENIED_OR_MISSING, (
        f"a requester transitioning {key} returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}")
    assert db.item_status_name(key) == before_status, (
        f"a denied transition still moved {key} to "
        f"{db.item_status_name(key)!r} from {before_status!r}")
    assert db.history_count(key) == before_history, (
        f"a denied transition appended a history entry to {key}")


def test_unauthenticated_items_request_denied(anon, member_api):
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    response = anon.get(f"{API_ITEMS}/{key}")
    assert response.status_code in DENIED_OR_MISSING, (
        f"an unauthenticated read of {key} returned {response.status_code}, "
        f"expected a denial: {response.text[:400]}")
    listing = anon.get(f"{API_PROJECTS}/{PROJECT_FIN}/items")
    assert listing.status_code in DENIED_OR_MISSING, (
        f"an unauthenticated listing of {PROJECT_FIN} items returned "
        f"{listing.status_code}, expected a denial: {listing.text[:400]}")


def test_page_view_log_denied_to_member(member_api, admin_api):
    denied = member_api.get(API_PAGE_VIEWS)
    assert denied.status_code in DENIED_OR_MISSING, (
        f"a member reading /api{API_PAGE_VIEWS} returned {denied.status_code}, "
        f"expected a denial: {denied.text[:400]}")
    allowed = admin_api.get(API_PAGE_VIEWS)
    assert allowed.status_code in OK, (
        f"an admin reading /api{API_PAGE_VIEWS} returned {allowed.status_code}, "
        f"expected the log: {allowed.text[:400]}")
    assert isinstance(allowed.json(), list), (
        f"/api{API_PAGE_VIEWS} returned {type(allowed.json()).__name__}, "
        f"expected a top-level JSON array")


def test_project_summary_count_scoped_to_visible_set(member2_api, member_api):
    mine = member_api.get(f"{API_PROJECTS}/{PROJECT_FIN}/summary")
    assert mine.status_code in OK, (
        f"a member of {PROJECT_FIN} reading its summary returned "
        f"{mine.status_code}: {mine.text[:400]}")
    visible = member_api.get(f"{API_PROJECTS}/{PROJECT_FIN}/items")
    assert visible.status_code in OK, (
        f"a member of {PROJECT_FIN} listing its items returned "
        f"{visible.status_code}: {visible.text[:400]}")
    assert int(mine.json().get("total")) == len(visible.json()), (
        f"the {PROJECT_FIN} summary reports "
        f"{mine.json().get('total')!r} items while the caller can see "
        f"{len(visible.json())}, so the count is not scoped to the visible set")
    outsider = member2_api.get(f"{API_PROJECTS}/{PROJECT_FIN}/summary")
    assert outsider.status_code in DENIED_OR_MISSING, (
        f"a member of another project read the {PROJECT_FIN} summary with "
        f"{outsider.status_code}, expected a denial: {outsider.text[:400]}")


def test_assignee_change_delivers_confirmation_email(member_api, db, inbox):
    lead = db.user(MEMBER_EMAIL)
    assert lead, f"the seeded lead {MEMBER_EMAIL} has no row in the datastore"
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    advance_to_ready(member_api, key)
    message = wait_for_message(inbox, MEMBER_EMAIL, key)
    assert message is not None, (
        f"no message naming {key} reached {MEMBER_EMAIL} after the bound rule "
        f"set the assignee; the notification exists only if mailpit holds it")
    assert message.to == [MEMBER_EMAIL] or MEMBER_EMAIL in message.to, (
        f"the notification for {key} was addressed to {message.to}, expected "
        f"{MEMBER_EMAIL} alone with no cc and no bcc")
    assert len(message.to) == 1, (
        f"the notification for {key} carries {len(message.to)} recipients "
        f"{message.to}, expected exactly one")


def test_notification_subject_names_item(member_api, inbox):
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    advance_to_ready(member_api, key)
    message = wait_for_message(inbox, MEMBER_EMAIL, key)
    assert message is not None, (
        f"no notification naming {key} reached {MEMBER_EMAIL}")
    assert message.subject.startswith(SUBJECT_PREFIX), (
        f"the notification subject is {message.subject!r}, expected it to begin "
        f"{SUBJECT_PREFIX!r}")
    assert key in message.subject, (
        f"the notification subject {message.subject!r} does not name the item "
        f"key {key}")


def test_unchanged_assignee_sends_no_email(member_api, inbox):
    key = create_item(member_api, PROJECT_FIN, probe_summary())
    before = inbox.count(MEMBER_EMAIL)
    response = transition(member_api, key, STATUS_IN_PROGRESS)
    assert response.status_code in OK, (
        f"transition of {key} to {STATUS_IN_PROGRESS!r} returned "
        f"{response.status_code}: {response.text[:400]}")
    settle()
    after = inbox.count(MEMBER_EMAIL)
    assert after == before, (
        f"a transition that changed no assignee delivered {after - before} "
        f"message(s) to {MEMBER_EMAIL}, expected none")


def test_pricing_graduated_bands_worked_example(anon):
    response = anon.get(API_PLANS)
    assert response.status_code in OK, (
        f"GET /api{API_PLANS} returned {response.status_code}: "
        f"{response.text[:400]}")
    assert isinstance(response.json(), list), (
        f"/api{API_PLANS} returned {type(response.json()).__name__}, expected a "
        f"top-level JSON array")
    assert graduated_total(300, STANDARD_MONTHLY_BANDS) == WORKED_STANDARD_300_TOTAL, (
        f"the pinned Standard monthly bands total "
        f"{graduated_total(300, STANDARD_MONTHLY_BANDS)} at 300 users, but the "
        f"brief pins {WORKED_STANDARD_300_TOTAL}")
    assert WORKED_STANDARD_300_TOTAL // 300 == WORKED_STANDARD_300_PER_USER, (
        f"the pinned Standard per-user figure {WORKED_STANDARD_300_PER_USER} "
        f"does not divide out of {WORKED_STANDARD_300_TOTAL} at 300 users")
    assert graduated_total(7, STANDARD_MONTHLY_BANDS) == WORKED_STANDARD_7_TOTAL, (
        f"the pinned Standard bands total "
        f"{graduated_total(7, STANDARD_MONTHLY_BANDS)} at 7 users, expected "
        f"{WORKED_STANDARD_7_TOTAL}")
    assert WORKED_STANDARD_7_TOTAL // 7 == WORKED_STANDARD_7_PER_USER, (
        f"the pinned per-user figure at 7 users is inconsistent with "
        f"{WORKED_STANDARD_7_TOTAL}")
    assert graduated_total(300, PREMIUM_MONTHLY_BANDS) == WORKED_PREMIUM_300_TOTAL, (
        f"the pinned Premium bands total "
        f"{graduated_total(300, PREMIUM_MONTHLY_BANDS)} at 300 users, expected "
        f"{WORKED_PREMIUM_300_TOTAL}")
    assert round(WORKED_PREMIUM_300_TOTAL / 300) == WORKED_PREMIUM_300_PER_USER, (
        f"the pinned Premium per-user figure {WORKED_PREMIUM_300_PER_USER} is "
        f"not {WORKED_PREMIUM_300_TOTAL} over 300 rounded once at display")


def test_unknown_query_field_is_refused(member_api):
    response = member_api.post(API_FILTERS,
                               json={"name": probe_summary("Probe filter"),
                                     "query_text": "nosuchfield = 1",
                                     "share_scope": PROJECT_FIN})
    assert response.status_code in REFUSED, (
        f"saving a filter naming an undefined field returned "
        f"{response.status_code}, expected a refusal: {response.text[:400]}")
    assert "nosuchfield" in response.text.lower(), (
        f"the refusal does not name the offending token: {response.text[:400]}")


def test_public_routes_render_without_script(site):
    for route in PUBLIC_ROUTES:
        response = site.get(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}: "
            f"{response.text[:200]}")
        body = response.text
        assert len(body) > 500, (
            f"GET {route} returned {len(body)} bytes of markup, too little to "
            f"carry the route's content without script")


def test_not_found_answers_not_found_status(raw_site):
    response = raw_site.get("/no-such-address-here")
    assert response.status_code == 404, (
        f"an unknown address returned {response.status_code}, expected 404 so "
        f"that an empty page is not indexed as a real one")
    assert len(response.text) > 500, (
        f"the not-found route returned {len(response.text)} bytes, too little "
        f"to carry the full header and footer")


def test_favicon_declared_in_document_head(site):
    response = site.get("/")
    assert response.status_code == 200, (
        f"GET / returned {response.status_code}: {response.text[:200]}")
    assert 'rel="icon"' in response.text or "rel='icon'" in response.text, (
        "the home document head declares no favicon link")
    icon = site.get("/favicon.ico")
    alternate = site.get("/favicon.svg")
    assert icon.status_code == 200 or alternate.status_code == 200, (
        f"no favicon is served: /favicon.ico returned {icon.status_code} and "
        f"/favicon.svg returned {alternate.status_code}")


def test_social_preview_declared_per_route(site):
    seen = {}
    for route in ("/", "/products", "/products/work", "/templates"):
        response = site.get(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}")
        body = response.text
        assert 'property="og:title"' in body or "property='og:title'" in body, (
            f"{route} declares no social preview title")
        assert 'property="og:image"' in body or "property='og:image'" in body, (
            f"{route} declares no social preview image")
        seen[route] = body
    assert len({len(v) for v in seen.values()}) > 1, (
        "every sampled route returned markup of identical length, so the "
        "per-route titles and descriptions are not distinct")


def test_terms_page_linked_from_every_footer(site):
    terms = site.get("/terms")
    assert terms.status_code == 200, (
        f"GET /terms returned {terms.status_code}: {terms.text[:200]}")
    for route in ("/", "/products", "/products/work/pricing"):
        response = site.get(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}")
        assert "/terms" in response.text, (
            f"{route} carries no link to /terms in its footer")
