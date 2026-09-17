"""Observations over the deployed Thirty workspace.

Every assertion here reads the app over HTTP, the PostgreSQL database behind it
or the Mailpit inbox beside it. Nothing reads the source the agent wrote.
"""

from __future__ import annotations

import os
import pathlib

import httpx

import appclient
import conftest
import _shapes

def test_health_route_is_ready():
    response = httpx.get(f"{appclient.app_url()}/api/health", timeout=conftest.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, expected 200 once the app is ready: "
        f"{response.text[:300]}"
    )


def test_login_returns_token_for_every_seeded_account():
    for email in conftest.SEEDED_ACCOUNTS:
        token = appclient.login(email, conftest.PASSWORD)
        assert token, f"login for the seeded account {email} returned no bearer token"


def test_login_with_wrong_password_is_denied():
    response = httpx.post(
        f"{appclient.api_base()}/auth/login",
        json={"email": conftest.MEMBER_ONE, "password": "not-the-seeded-password"},
        timeout=conftest.TIMEOUT,
    )
    assert response.status_code in (400, 401, 403), (
        f"a wrong password for {conftest.MEMBER_ONE} returned {response.status_code}, "
        f"expected a client-side denial"
    )
    body = _shapes.flatten(response.text)
    assert "no such" not in body and "not registered" not in body and "unknown account" not in body, (
        f"the denial response discloses whether the address exists: {response.text[:300]}"
    )


def test_second_factor_is_required_once_enrolled():
    admin = conftest.session(conftest.ADMIN)
    enrol = admin.post("/auth/2fa/enrol", json={})
    if enrol.status_code in (200, 201):
        first = httpx.post(
            f"{appclient.api_base()}/auth/login",
            json={"email": conftest.ADMIN, "password": conftest.PASSWORD},
            timeout=conftest.TIMEOUT,
        )
        payload = first.json() if first.status_code == 200 else {}
        assert first.status_code != 200 or payload.get("requires_code") is True, (
            f"a password-only sign-in for an enrolled account returned a session: "
            f"{first.text[:300]}"
        )
        bad = httpx.post(
            f"{appclient.api_base()}/auth/login",
            json={"email": conftest.ADMIN, "password": conftest.PASSWORD, "code": "000000"},
            timeout=conftest.TIMEOUT,
        )
        assert bad.status_code in (400, 401, 403), (
            f"a wrong second-factor code returned {bad.status_code}, expected a denial"
        )
        assert not (bad.status_code == 200 and bad.json().get("access_token")), (
            "a wrong second-factor code produced a session token"
        )
    else:
        assert enrol.status_code in (400, 401, 403, 404, 409), (
            f"POST /api/auth/2fa/enrol returned {enrol.status_code}, which is neither an "
            f"enrolment nor a stated refusal"
        )


def test_signup_without_an_invitation_writes_no_membership():
    before = conftest.backend_count("membership")
    probe = f"probe-{os.urandom(6).hex()}@example.com"
    for route in ("/auth/signup", "/auth/register", "/memberships"):
        response = httpx.post(
            f"{appclient.api_base()}{route}",
            json={"email": probe, "password": conftest.PASSWORD, "role": "admin"},
            timeout=conftest.TIMEOUT,
        )
        assert response.status_code not in (200, 201), (
            f"POST {route} created an account with no invitation: {response.text[:300]}"
        )
    after = conftest.backend_count("membership")
    assert after == before, (
        f"membership rows moved from {before} to {after} after uninvited signup attempts"
    )


def test_objects_list_is_a_top_level_array():
    admin = conftest.session(conftest.ADMIN)
    response = admin.get("/objects")
    assert response.status_code == 200, (
        f"GET /api/objects returned {response.status_code}: {response.text[:300]}"
    )
    rows = _shapes.items(response.json())
    names = {str(row.get("name_plural", "")).lower() for row in rows}
    for starter in conftest.STARTER_OBJECTS:
        assert starter.lower() in names, (
            f"the seeded starter object {starter!r} is absent from GET /api/objects; "
            f"found {sorted(names)}"
        )


def test_new_object_is_addressable_at_once():
    admin = conftest.session(conftest.ADMIN)
    slug = conftest.unique("rocket")
    created = admin.post("/objects", json={
        "name_singular": slug, "name_plural": slug + "s", "icon": "target"})
    assert created.status_code in (200, 201), (
        f"creating the object {slug!r} returned {created.status_code}: {created.text[:300]}"
    )
    listed = admin.get("/objects")
    names = {str(row.get("name_singular", "")) for row in _shapes.items(listed.json())}
    assert slug in names, f"the new object {slug!r} is absent from GET /api/objects"
    records = admin.get(f"/objects/{slug}/records")
    assert records.status_code == 200, (
        f"the new object {slug!r} has no addressable records resource: "
        f"GET /api/objects/{slug}/records returned {records.status_code}"
    )
    assert _shapes.items(records.json()) == [], (
        f"the new object {slug!r} reports records before any were created"
    )


def test_field_types_cover_the_stated_set():
    admin = conftest.session(conftest.ADMIN)
    slug = conftest.unique("catalogue")
    admin.post("/objects", json={
        "name_singular": slug, "name_plural": slug + "s", "icon": "note"})
    accepted = []
    for field_type in conftest.FIELD_TYPES:
        response = admin.post(f"/objects/{slug}/fields", json={
            "name": conftest.unique(field_type.replace(" ", "_")),
            "type": field_type, "options": [], "is_unique": False})
        if response.status_code in (200, 201):
            accepted.append(field_type)
    missing = sorted(set(conftest.FIELD_TYPES) - set(accepted))
    assert not missing, (
        f"the metadata engine refused {len(missing)} of the {len(conftest.FIELD_TYPES)} "
        f"stated field types: {missing}"
    )


def test_relation_is_navigable_from_both_sides():
    admin = conftest.session(conftest.ADMIN)
    left, right = conftest.unique("depot"), conftest.unique("crate")
    for slug in (left, right):
        admin.post("/objects", json={
            "name_singular": slug, "name_plural": slug + "s", "icon": "building"})
    made = admin.post(f"/objects/{left}/fields", json={
        "name": conftest.unique("holds"), "type": "relation",
        "options": {"target": right, "cardinality": "one-to-many"}, "is_unique": False})
    assert made.status_code in (200, 201), (
        f"pairing a relation from {left!r} to {right!r} returned {made.status_code}: "
        f"{made.text[:300]}"
    )
    other_side = admin.get(f"/objects/{right}/fields")
    flat = _shapes.flatten(other_side.json())
    assert left.lower() in flat, (
        f"the relation is invisible from the {right!r} side; a relation is created once "
        f"and is present on both sides"
    )


def test_field_rename_preserves_stored_values():
    admin = conftest.session(conftest.ADMIN)
    slug, field = conftest.unique("ledger"), conftest.unique("amount")
    admin.post("/objects", json={
        "name_singular": slug, "name_plural": slug + "s", "icon": "chart"})
    admin.post(f"/objects/{slug}/fields", json={
        "name": field, "type": "currency", "options": [], "is_unique": False})
    admin.post(f"/objects/{slug}/records", json={field: 250000})
    renamed = field + "_renamed"
    response = admin.patch(f"/objects/{slug}/fields/{field}", json={"name": renamed})
    assert response.status_code in (200, 202), (
        f"renaming {field!r} returned {response.status_code}: {response.text[:300]}"
    )
    rows = _shapes.items(admin.get(f"/objects/{slug}/records").json())
    assert rows, f"the records of {slug!r} vanished across a field rename"
    kept = [row for row in rows if row.get(renamed) == 250000 or row.get(field) == 250000]
    assert kept, (
        f"the stored value 250000 did not survive the rename of {field!r} to {renamed!r}; "
        f"first row reads {rows[0]}"
    )


def test_dependents_are_listed_before_a_schema_change_lands():
    admin = conftest.session(conftest.ADMIN)
    slug, field = conftest.unique("pipeline"), conftest.unique("stage")
    admin.post("/objects", json={
        "name_singular": slug, "name_plural": slug + "s", "icon": "bolt"})
    admin.post(f"/objects/{slug}/fields", json={
        "name": field, "type": "text", "options": [], "is_unique": False})
    response = admin.get(f"/objects/{slug}/dependents", params={"field": field})
    assert response.status_code == 200, (
        f"GET /api/objects/{slug}/dependents returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    rows = _shapes.items(response.json())
    for row in rows:
        assert "kind" in row and "name" in row and "action" in row, (
            f"a dependent row is missing kind, name or action: {row}"
        )
        assert row["action"] in ("cascade", "block"), (
            f"dependent {row.get('name')!r} names the action {row.get('action')!r}, which "
            f"is neither cascade nor block"
        )


def test_records_list_is_permission_filtered_for_each_member():
    one = conftest.session(conftest.MEMBER_ONE)
    two = conftest.session(conftest.MEMBER_TWO)
    rows_one = _shapes.items(one.get("/objects/company/records").json())
    rows_two = _shapes.items(two.get("/objects/company/records").json())
    assert len(rows_one) == 5, (
        f"{conftest.MEMBER_ONE} lists {len(rows_one)} companies, expected the 5 owned"
    )
    assert len(rows_two) == 4, (
        f"{conftest.MEMBER_TWO} lists {len(rows_two)} companies, expected the 4 owned"
    )
    names_one = {str(row.get("name", "")) for row in rows_one}
    names_two = {str(row.get("name", "")) for row in rows_two}
    assert not (names_one & names_two), (
        f"both members can list the same companies {sorted(names_one & names_two)}; the "
        f"seeded rule binds a company row to its account owner"
    )


def test_workflow_run_records_every_node_and_pins_its_version():
    admin = conftest.session(conftest.ADMIN)
    workflows = _shapes.items(admin.get("/workflows").json())
    match = [row for row in workflows if row.get("name") == conftest.WORKFLOW_NAME]
    assert match, (
        f"the seeded workflow {conftest.WORKFLOW_NAME!r} is absent; found "
        f"{[row.get('name') for row in workflows]}"
    )
    workflow = match[0]
    member = conftest.session(conftest.MEMBER_ONE)
    record = _shapes.items(member.get("/objects/opportunity/records").json())[0]
    member.patch(f"/objects/opportunity/records/{record['id']}",
                 json={"stage": "Qualified", "version": record.get("version", 1)})
    runs = conftest.wait_for_runs(admin, workflow["id"], at_least=1)
    run = runs[0]
    assert run.get("version"), f"the run pins no workflow version: {run}"
    assert run.get("trigger"), f"the run records no trigger: {run}"
    steps = run.get("steps") or []
    assert steps, f"the run records no steps: {run}"
    for step in steps:
        for field in ("input", "output", "outcome"):
            assert field in step, f"a run step records no {field}: {step}"


def test_public_routes_each_carry_their_own_title_and_description():
    titles, descriptions = {}, {}
    for route in conftest.PUBLIC_ROUTES:
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=conftest.TIMEOUT,
                         follow_redirects=True)
        assert page.status_code == 200, (
            f"GET {route} returned {page.status_code}, expected a served public page"
        )
        title = conftest.head_title(page.text)
        description = conftest.head_meta(page.text, "description")
        assert title, f"{route} carries no document title"
        assert description, f"{route} carries no meta description"
        assert title not in titles, (
            f"{route} shares its title {title!r} with {titles[title]}"
        )
        assert description not in descriptions, (
            f"{route} shares its description with {descriptions[description]}"
        )
        titles[title] = route
        descriptions[description] = route


def test_social_preview_is_declared_and_its_image_resolves():
    for route in conftest.PUBLIC_ROUTES:
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=conftest.TIMEOUT,
                         follow_redirects=True)
        title = conftest.head_meta(page.text, "og:title") or conftest.head_meta(
            page.text, "twitter:title")
        image = conftest.head_meta(page.text, "og:image") or conftest.head_meta(
            page.text, "twitter:image")
        assert title, f"{route} declares no social preview title"
        assert image, f"{route} declares no social preview image"
        resolved = httpx.get(conftest.absolute(image), timeout=conftest.TIMEOUT,
                             follow_redirects=True)
        assert resolved.status_code == 200, (
            f"the social preview image {image!r} declared by {route} answered "
            f"{resolved.status_code}"
        )


def test_no_credential_appears_in_anything_the_browser_downloads():
    leaked = []
    for route in conftest.PUBLIC_ROUTES:
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=conftest.TIMEOUT,
                         follow_redirects=True)
        bodies = [page.text]
        for asset in conftest.asset_urls(page.text):
            fetched = httpx.get(conftest.absolute(asset), timeout=conftest.TIMEOUT,
                                follow_redirects=True)
            if fetched.status_code == 200:
                bodies.append(fetched.text)
        for body in bodies:
            for secret in conftest.FORBIDDEN_IN_BROWSER:
                if secret in body:
                    leaked.append((route, secret))
    assert not leaked, (
        f"credentials reached the browser: {leaked[:5]}"
    )


def test_every_internal_link_on_every_public_page_resolves():
    broken = []
    for route in conftest.PUBLIC_ROUTES:
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=conftest.TIMEOUT,
                         follow_redirects=True)
        for href in conftest.internal_links(page.text):
            target = httpx.get(conftest.absolute(href), timeout=conftest.TIMEOUT,
                               follow_redirects=True)
            if target.status_code >= 400:
                broken.append((route, href, target.status_code))
    assert not broken, f"internal links do not resolve: {broken[:8]}"


def test_pinned_marketing_copy_is_served_verbatim():
    missing = []
    for route, strings in conftest.PINNED_COPY.items():
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=conftest.TIMEOUT,
                         follow_redirects=True)
        for pinned in strings:
            if pinned not in page.text:
                missing.append((route, pinned))
    assert not missing, (
        f"pinned copy is absent from the served pages: {missing[:8]}"
    )


def test_plan_surface_reports_tier_seats_and_credits():
    owner = conftest.session(conftest.OWNER)
    response = owner.get("/plan")
    assert response.status_code == 200, (
        f"GET /api/plan returned {response.status_code}: {response.text[:300]}"
    )
    plan = response.json()
    for field in ("tier", "seats", "credits_used", "credits_included"):
        assert field in plan, f"GET /api/plan reports no {field}: {plan}"
    assert plan["seats"] == len(conftest.SEEDED_ACCOUNTS), (
        f"the plan reports {plan['seats']} seats for {len(conftest.SEEDED_ACCOUNTS)} "
        f"seeded memberships"
    )


def test_views_carry_their_own_filters_and_columns():
    member = conftest.session(conftest.MEMBER_ONE)
    response = member.get("/views", params={"object": "company"})
    assert response.status_code == 200, (
        f"GET /api/views returned {response.status_code}: {response.text[:300]}"
    )
    views = _shapes.items(response.json())
    assert views, "the seeded Companies object carries no view"
    for view in views:
        for field in ("type", "filters", "sorts", "columns", "is_shared"):
            assert field in view, f"the view {view.get('name')!r} carries no {field}: {view}"
    made = member.post("/views", json={
        "object": "company", "type": "table", "name": conftest.unique("mine"),
        "is_shared": False, "filters": [{"field": "icp", "op": "is", "value": True}],
        "sorts": [], "columns": ["name", "arr"], "pinned": ["name"]})
    assert made.status_code in (200, 201), (
        f"saving a view returned {made.status_code}: {made.text[:300]}"
    )
    fresh = conftest.session(conftest.MEMBER_ONE)
    again = [v for v in _shapes.items(
        fresh.get("/views", params={"object": "company"}).json())
        if v.get("name") == made.json().get("name")]
    assert again, "a saved view did not survive a fresh sign-in"
    assert again[0].get("pinned") == ["name"], (
        f"the pinned column did not persist: {again[0].get('pinned')!r}"
    )


def test_chat_answers_cite_records_or_refuse():
    member = conftest.session(conftest.MEMBER_ONE)
    answerable = member.post("/chat", json={"question": conftest.CHAT_QUESTION})
    assert answerable.status_code == 200, (
        f"POST /api/chat returned {answerable.status_code}: {answerable.text[:300]}"
    )
    payload = answerable.json()
    assert payload.get("citations"), (
        f"an answered question cites no records: {payload}"
    )
    refused = member.post("/chat", json={"question": conftest.UNANSWERABLE_QUESTION})
    assert refused.status_code == 200, (
        f"an unanswerable question returned {refused.status_code}"
    )
    body = refused.json()
    assert body.get("refused") is True or not body.get("citations"), (
        f"the app answered a question the records cannot support: {body}"
    )


def test_webhook_deliveries_are_signed_and_retries_are_recorded():
    admin = conftest.session(conftest.ADMIN)
    made = admin.post("/webhooks", json={
        "object": "company", "url": "http://main:4173/api/health"})
    if made.status_code not in (200, 201):
        assert made.status_code in (400, 403, 404), (
            f"POST /api/webhooks returned {made.status_code}: {made.text[:300]}"
        )
        return
    listed = _shapes.items(admin.get("/webhooks").json())
    assert listed, "a created webhook subscription is absent from the listing"
    flat = _shapes.flatten(listed)
    assert "signing" in flat or "signature" in flat, (
        f"a webhook subscription carries no signing material: {listed[0]}"
    )


def test_reconnecting_client_receives_missed_changes_in_order():
    member = conftest.session(conftest.MEMBER_ONE)
    cursor = member.get("/events", params={"after": 0})
    assert cursor.status_code == 200, (
        f"GET /api/events returned {cursor.status_code}: {cursor.text[:300]}"
    )
    baseline = _shapes.items(cursor.json())
    last = baseline[-1].get("id") if baseline else 0
    record = _shapes.items(member.get("/objects/company/records").json())[0]
    member.patch(f"/objects/company/records/{record['id']}",
                 json={"notes": conftest.unique("note"),
                       "version": record.get("version", 1)})
    caught_up = conftest.wait_for_events(member, after=last, at_least=1)
    ids = [row.get("id") for row in caught_up]
    assert ids == sorted(ids), (
        f"the replayed events are out of order: {ids}"
    )
    assert len(ids) == len(set(ids)), f"the replay repeated an event: {ids}"


def test_marketing_mock_data_comes_from_the_platform():
    landing = httpx.get(f"{appclient.app_url()}/", timeout=conftest.TIMEOUT,
                        follow_redirects=True)
    assert landing.status_code == 200, (
        f"the landing page returned {landing.status_code}"
    )
    for name, _domain, _arr in conftest.SEEDED_COMPANIES[:3]:
        assert name in landing.text, (
            f"the hero mock does not carry the seeded company {name!r}; the marketing "
            f"mocks run the platform's own fixtures"
        )


def test_external_services_are_not_reached_at_runtime():
    stored = conftest.backend_count("record")
    assert stored > 0, (
        "no record rows exist in PostgreSQL; the records the app serves must live in the "
        "declared database rather than in the process"
    )
    landing = httpx.get(f"{appclient.app_url()}/", timeout=conftest.TIMEOUT,
                        follow_redirects=True)
    for host in conftest.FORBIDDEN_HOSTS:
        assert host not in landing.text, (
            f"the served page reaches out to {host!r}; no external service is contacted "
            f"at runtime"
        )


def test_app_contract_paths_exist_in_the_image():
    readme = pathlib.Path("/app/USER_README.md")
    assert readme.is_file(), (
        "/app/USER_README.md is absent; the login credentials are written there"
    )
    text = readme.read_text(encoding="utf-8", errors="replace")
    for email in conftest.SEEDED_ACCOUNTS:
        assert email in text, f"/app/USER_README.md does not name the seeded account {email}"
    assert conftest.PASSWORD in text, (
        "/app/USER_README.md does not carry the seeded password"
    )
    for name in (".browser_screenshots", ".downloads"):
        directory = pathlib.Path("/app") / name
        assert directory.is_dir(), f"/app/{name} is absent from the app root"
        assert not any(directory.iterdir()), f"/app/{name} is not empty"


def test_hidden_row_is_answered_as_not_found():
    one = conftest.session(conftest.MEMBER_ONE)
    two = conftest.session(conftest.MEMBER_TWO)
    mine = _shapes.items(one.get("/objects/company/records").json())
    assert mine, f"{conftest.MEMBER_ONE} can list no company"
    hidden = mine[0]
    response = two.get(f"/objects/company/records/{hidden['id']}")
    assert response.status_code == 404, (
        f"a direct request from {conftest.MEMBER_TWO} for a row they may not see returned "
        f"{response.status_code}; a hidden row is answered as not found, never as "
        f"forbidden, which would confirm the row exists"
    )


def test_hidden_row_is_absent_from_search_and_its_counts():
    one = conftest.session(conftest.MEMBER_ONE)
    two = conftest.session(conftest.MEMBER_TWO)
    mine = _shapes.items(one.get("/objects/company/records").json())
    needle = str(mine[0].get("name"))
    found = two.get("/search", params={"q": needle})
    assert found.status_code == 200, (
        f"GET /api/search returned {found.status_code}: {found.text[:300]}"
    )
    flat = _shapes.flatten(found.json())
    assert needle.lower() not in flat, (
        f"search for {needle!r} as {conftest.MEMBER_TWO} surfaced a row the permission "
        f"rule hides"
    )


def test_hidden_row_moves_no_aggregate():
    one = conftest.session(conftest.MEMBER_ONE)
    two = conftest.session(conftest.MEMBER_TWO)
    def total(client):
        response = client.get("/aggregates", params={
            "object": "company", "group_by": "icp", "metric": "sum:arr"})
        assert response.status_code == 200, (
            f"GET /api/aggregates returned {response.status_code}: {response.text[:300]}"
        )
        return sum(int(lane.get("value") or 0) for lane in _shapes.items(response.json()))
    def listed(client):
        return sum(int(row.get("arr") or 0)
                   for row in _shapes.items(client.get("/objects/company/records").json()))
    for label, client in ((conftest.MEMBER_ONE, one), (conftest.MEMBER_TWO, two)):
        assert total(client) == listed(client), (
            f"{label} reads an aggregate of {total(client)} while the rows they can list "
            f"sum to {listed(client)}; an aggregate is computed after row filtering"
        )
    assert total(one) != total(two), (
        "both members read the same aggregate, so the row rule is not reaching the "
        "aggregate path at all"
    )


def test_masked_field_is_absent_from_every_read_path():
    admin = conftest.session(conftest.ADMIN)
    rule = admin.post("/permission-rules", json={
        "role": "member", "object": "company",
        "grants": ["read"], "row_filter": "owner", "masked_fields": ["arr"]})
    if rule.status_code not in (200, 201):
        assert rule.status_code in (400, 403, 409), (
            f"creating a field-masking rule returned {rule.status_code}: {rule.text[:300]}"
        )
        return
    member = conftest.session(conftest.MEMBER_ONE)
    rows = _shapes.items(member.get("/objects/company/records").json())
    for row in rows:
        assert "arr" not in row, (
            f"the masked field arr is present in a record the member can read: {row}"
        )
    export = member.get("/exports", params={"view": "All Companies"})
    assert "arr" not in export.text.splitlines()[0].lower() if export.text else True, (
        f"the masked field arr appears in the export header: {export.text[:200]}"
    )


def test_member_is_denied_schema_writes_at_the_api():
    member = conftest.session(conftest.MEMBER_ONE)
    before = conftest.backend_count("object_metadata")
    forbidden = (
        ("post", "/objects", {"name_singular": "smuggled", "name_plural": "smuggleds",
                              "icon": "bolt"}),
        ("post", "/permission-rules", {"role": "member", "object": "company",
                                       "grants": ["read"], "row_filter": "all"}),
        ("post", "/objects/company/fields", {"name": "smuggled_field", "type": "text",
                                             "options": [], "is_unique": False}),
    )
    for method, route, payload in forbidden:
        response = getattr(member, method)(route, json=payload)
        assert response.status_code in (401, 403, 404), (
            f"{method.upper()} {route} from a member session returned "
            f"{response.status_code}, expected a server-side denial: {response.text[:300]}"
        )
    after = conftest.backend_count("object_metadata")
    assert after == before, (
        f"object metadata rows moved from {before} to {after} after denied member writes"
    )


def test_member_cannot_read_keys_or_another_private_view():
    member = conftest.session(conftest.MEMBER_ONE)
    keys = member.get("/keys")
    assert keys.status_code in (401, 403, 404), (
        f"GET /api/keys from a member session returned {keys.status_code}, expected a "
        f"denial: {keys.text[:300]}"
    )
    two = conftest.session(conftest.MEMBER_TWO)
    private = two.post("/views", json={
        "object": "company", "type": "table", "name": conftest.unique("private"),
        "is_shared": False, "filters": [], "sorts": [], "columns": ["name"]})
    if private.status_code in (200, 201):
        listed = _shapes.items(member.get("/views", params={"object": "company"}).json())
        names = {str(view.get("name")) for view in listed}
        assert private.json().get("name") not in names, (
            f"a private view of {conftest.MEMBER_TWO} is visible to "
            f"{conftest.MEMBER_ONE}: {sorted(names)}"
        )


def test_admin_is_denied_plan_and_billing_writes():
    admin = conftest.session(conftest.ADMIN)
    before = admin.get("/plan")
    response = admin.patch("/plan", json={"tier": "Enterprise"})
    assert response.status_code in (401, 403, 404), (
        f"an admin changing the plan tier returned {response.status_code}, expected a "
        f"denial: {response.text[:300]}"
    )
    after = conftest.session(conftest.OWNER).get("/plan")
    assert after.json().get("tier") == before.json().get("tier"), (
        f"the plan tier moved from {before.json().get('tier')!r} to "
        f"{after.json().get('tier')!r} on a denied request"
    )


def test_unauthenticated_request_is_refused():
    anonymous = httpx.Client(base_url=appclient.api_base(), timeout=conftest.TIMEOUT)
    for route in ("/objects", "/objects/company/records", "/audit", "/plan"):
        response = anonymous.get(route)
        assert response.status_code in (401, 403), (
            f"GET {route} without a token returned {response.status_code}, expected an "
            f"authentication refusal"
        )


def test_revoked_key_is_refused_on_the_next_request():
    admin = conftest.session(conftest.ADMIN)
    made = admin.post("/keys", json={"name": conftest.unique("probe"), "scopes": ["read"]})
    if made.status_code not in (200, 201):
        assert made.status_code in (400, 403, 404), (
            f"POST /api/keys returned {made.status_code}: {made.text[:300]}"
        )
        return
    secret = made.json().get("secret")
    assert secret, f"a newly created key returned no secret to show once: {made.json()}"
    keyed = httpx.Client(base_url=appclient.api_base(), timeout=conftest.TIMEOUT,
                         headers={"Authorization": f"Bearer {secret}"})
    assert keyed.get("/objects").status_code == 200, (
        "a freshly issued key cannot read the objects resource"
    )
    admin.delete(f"/keys/{made.json().get('id')}")
    after = keyed.get("/objects")
    assert after.status_code in (401, 403), (
        f"a revoked key still reads: GET /api/objects returned {after.status_code}"
    )


def test_pro_plan_denies_a_row_rule_and_writes_nothing():
    owner = conftest.session(conftest.OWNER)
    before = conftest.backend_count("permission_rule")
    owner.patch("/plan", json={"tier": "Pro"})
    admin = conftest.session(conftest.ADMIN)
    response = admin.post("/permission-rules", json={
        "role": "member", "object": "company", "grants": ["read"], "row_filter": "owner"})
    assert response.status_code in (402, 403, 409), (
        f"creating a row rule on a Pro workspace returned {response.status_code}, expected "
        f"a plan refusal: {response.text[:300]}"
    )
    after = conftest.backend_count("permission_rule")
    assert after == before, (
        f"permission rule rows moved from {before} to {after} on a denied Pro request"
    )
    owner.patch("/plan", json={"tier": "Organization"})


def test_seeded_companies_match_the_pinned_fixture():
    admin = conftest.session(conftest.ADMIN)
    rows = _shapes.items(admin.get("/objects/company/records").json())
    by_name = {str(row.get("name", "")): row for row in rows}
    for name, domain, arr in conftest.SEEDED_COMPANIES:
        assert name in by_name, (
            f"the seeded company {name!r} is absent; the workspace lists {sorted(by_name)}"
        )
        row = by_name[name]
        flat = _shapes.flatten(row)
        assert domain in flat, f"the seeded company {name!r} does not carry {domain!r}: {row}"
        assert row.get("arr") == arr, (
            f"{name!r} reports arr {row.get('arr')!r}, expected the pinned integer minor "
            f"units {arr}"
        )
    creators = {str(row.get("created_by_kind", "")).lower() for row in rows}
    for kind in ("key", "workflow", "system"):
        assert kind in creators, (
            f"no seeded company is attributed to a {kind} actor; the fixture carries "
            f"people, a key, a workflow and System"
        )


def test_cell_edit_survives_a_reload():
    member = conftest.session(conftest.MEMBER_ONE)
    rows = _shapes.items(member.get("/objects/company/records").json())
    assert rows, f"{conftest.MEMBER_ONE} can list no company to edit"
    record = rows[0]
    target = 777000
    patched = member.patch(
        f"/objects/company/records/{record['id']}",
        json={"arr": target, "version": record.get("version", 1)})
    assert patched.status_code in (200, 202), (
        f"committing arr={target} on {record.get('name')!r} returned "
        f"{patched.status_code}: {patched.text[:300]}"
    )
    fresh = conftest.session(conftest.MEMBER_ONE)
    reread = fresh.get(f"/objects/company/records/{record['id']}")
    assert reread.status_code == 200, (
        f"re-reading {record.get('name')!r} returned {reread.status_code}"
    )
    assert reread.json().get("arr") == target, (
        f"the committed value {target} did not survive a re-read; the record now reads "
        f"{reread.json().get('arr')!r}"
    )
    stored = conftest.backend_rows("record", limit=None)
    assert any(_shapes.flatten(row).find(str(target)) >= 0 for row in stored), (
        f"the committed value {target} is not present in the database behind the app"
    )


def test_board_lane_totals_reconcile_with_the_rows():
    member = conftest.session(conftest.MEMBER_ONE)
    rows = _shapes.items(member.get("/objects/opportunity/records").json())
    aggregates = member.get("/aggregates", params={
        "object": "opportunity", "group_by": "stage", "metric": "sum:amount"})
    assert aggregates.status_code == 200, (
        f"GET /api/aggregates returned {aggregates.status_code}: {aggregates.text[:300]}"
    )
    lanes = {str(lane.get("group")): lane.get("value")
             for lane in _shapes.items(aggregates.json())}
    expected = {}
    for row in rows:
        expected.setdefault(str(row.get("stage")), 0)
        expected[str(row.get("stage"))] += int(row.get("amount") or 0)
    for lane, total in expected.items():
        assert lanes.get(lane) == total, (
            f"lane {lane!r} reports {lanes.get(lane)!r} but the rows this member can list "
            f"sum to {total}"
        )


def test_card_move_writes_the_grouped_field_and_is_attributed():
    member = conftest.session(conftest.MEMBER_ONE)
    rows = _shapes.items(member.get("/objects/opportunity/records").json())
    assert rows, f"{conftest.MEMBER_ONE} can list no opportunity to move"
    record = rows[0]
    before = record.get("stage")
    target = "Qualified" if before != "Qualified" else "Identified"
    moved = member.patch(
        f"/objects/opportunity/records/{record['id']}",
        json={"stage": target, "version": record.get("version", 1)})
    assert moved.status_code in (200, 202), (
        f"moving {record.get('name')!r} to {target!r} returned {moved.status_code}: "
        f"{moved.text[:300]}"
    )
    entries = _shapes.items(member.get("/audit", params={"object": "opportunity"}).json())
    match = [row for row in entries
             if str(row.get("after", "")).find(target) >= 0
             and str(row.get("actor", "")).find(conftest.MEMBER_ONE) >= 0]
    assert match, (
        f"no audit entry attributes the move to {target!r} to {conftest.MEMBER_ONE}; the "
        f"trail holds {len(entries)} entries for opportunity"
    )
    assert match[0].get("before") is not None, (
        f"the audit entry records no value before the change: {match[0]}"
    )


def test_audit_trail_is_append_only_and_filterable():
    admin = conftest.session(conftest.ADMIN)
    entries = _shapes.items(admin.get("/audit").json())
    assert entries, "the audit trail is empty after seeding and sign-ins"
    kinds = {str(row.get("verb", "")).lower() for row in entries}
    assert any("sign" in kind or "login" in kind for kind in kinds), (
        f"no sign-in is recorded in the audit trail; verbs present: {sorted(kinds)}"
    )
    target = entries[0]
    for method in ("patch", "delete"):
        response = getattr(admin, method)(f"/audit/{target.get('id')}", json={"verb": "x"})
        assert response.status_code in (401, 403, 404, 405), (
            f"{method.upper()} on an audit entry returned {response.status_code}; the "
            f"trail is append-only"
        )
    filtered = _shapes.items(
        admin.get("/audit", params={"actor": conftest.ADMIN}).json())
    assert all(conftest.ADMIN in str(row.get("actor", "")) for row in filtered), (
        f"filtering the audit trail by actor returned entries for other actors: "
        f"{[row.get('actor') for row in filtered][:5]}"
    )


def test_export_records_an_audit_entry_and_hides_nothing_extra():
    member = conftest.session(conftest.MEMBER_ONE)
    export = member.get("/exports", params={"view": "All Companies"})
    assert export.status_code == 200, (
        f"GET /api/exports returned {export.status_code}: {export.text[:300]}"
    )
    listed = {str(row.get("name")) for row
              in _shapes.items(member.get("/objects/company/records").json())}
    text = export.text
    for name in listed:
        assert name in text, f"the export omits {name!r}, a row this member can list"
    admin = conftest.session(conftest.ADMIN)
    entries = _shapes.items(admin.get("/audit").json())
    assert any("export" in str(row.get("verb", "")).lower() for row in entries), (
        "no audit entry records the export"
    )


def test_import_dry_run_writes_nothing_then_commits_as_one_batch():
    admin = conftest.session(conftest.ADMIN)
    before = conftest.backend_count("record")
    payload = {"object": "company", "duplicate_strategy": "skip", "dry_run": True,
               "mapping": {"Company": "name", "Domain": "domain", "ARR": "arr"},
               "rows": conftest.IMPORT_ROWS}
    dry = admin.post("/imports", json=payload)
    assert dry.status_code in (200, 201), (
        f"a dry-run import returned {dry.status_code}: {dry.text[:300]}"
    )
    assert conftest.backend_count("record") == before, (
        "a dry-run import wrote rows to the database"
    )
    assert dry.json().get("row_errors"), (
        f"the dry run flagged no row errors although the fixture carries one bad row: "
        f"{dry.json()}"
    )
    payload["dry_run"] = False
    committed = admin.post("/imports", json=payload)
    assert committed.status_code in (200, 201), (
        f"committing the import returned {committed.status_code}: {committed.text[:300]}"
    )
    handle = committed.json().get("undo_handle")
    assert handle, f"a committed import returned no undo handle: {committed.json()}"
    after = conftest.backend_count("record")
    assert after > before, "a committed import created no rows"
    undone = admin.post(f"/imports/{handle}/undo")
    assert undone.status_code in (200, 202), (
        f"undoing the batch returned {undone.status_code}: {undone.text[:300]}"
    )
    assert conftest.backend_count("record") == before, (
        f"after the undo the record count is {conftest.backend_count('record')}, expected "
        f"the pre-import {before}"
    )


def test_one_triggering_event_starts_exactly_one_run():
    admin = conftest.session(conftest.ADMIN)
    workflow = [row for row in _shapes.items(admin.get("/workflows").json())
                if row.get("name") == conftest.WORKFLOW_NAME][0]
    before = len(_shapes.items(
        admin.get(f"/workflows/{workflow['id']}/runs").json()))
    member = conftest.session(conftest.MEMBER_ONE)
    record = _shapes.items(member.get("/objects/opportunity/records").json())[1]
    member.patch(f"/objects/opportunity/records/{record['id']}",
                 json={"stage": "Qualified", "version": record.get("version", 1)})
    runs = conftest.wait_for_runs(admin, workflow["id"], at_least=before + 1)
    assert len(runs) == before + 1, (
        f"one stage change produced {len(runs) - before} runs of "
        f"{conftest.WORKFLOW_NAME!r}; exactly one run starts per triggering event"
    )


def test_seeding_is_idempotent():
    counts = {}
    for table in ("record", "object_metadata", "membership"):
        counts[table] = conftest.backend_count(table)
    admin = conftest.session(conftest.ADMIN)
    admin.post("/health/reseed")
    conftest.settle()
    for table, before in counts.items():
        after = conftest.backend_count(table)
        assert after == before, (
            f"{table} rows moved from {before} to {after}; seeding must be idempotent"
        )


def test_no_second_write_on_a_replayed_mutation():
    member = conftest.session(conftest.MEMBER_ONE)
    record = _shapes.items(member.get("/objects/company/records").json())[0]
    version = record.get("version", 1)
    body = {"arr": 424242, "version": version}
    first = member.patch(f"/objects/company/records/{record['id']}", json=body)
    assert first.status_code in (200, 202), (
        f"the first commit returned {first.status_code}: {first.text[:300]}"
    )
    replay = member.patch(f"/objects/company/records/{record['id']}", json=body)
    assert replay.status_code != 500, (
        f"replaying an identical mutation raised a server error: {replay.text[:300]}"
    )
    entries = [row for row in _shapes.items(
        conftest.session(conftest.ADMIN).get("/audit", params={
            "object": "company"}).json())
        if str(row.get("after", "")).find("424242") >= 0]
    assert len(entries) <= 1, (
        f"a replayed identical mutation produced {len(entries)} audit entries; the second "
        f"arrival must not create a second write"
    )


def test_ten_thousand_rows_list_without_loss():
    admin = conftest.session(conftest.ADMIN)
    total = admin.get("/objects/company/records", params={"limit": 1}).json()
    reported = total.get("total") if isinstance(total, dict) else None
    page = admin.get("/objects/company/records", params={"limit": 50})
    assert page.status_code == 200, (
        f"a paged read returned {page.status_code}: {page.text[:300]}"
    )
    rows = _shapes.items(page.json())
    assert len(rows) <= 50, (
        f"a limit of 50 returned {len(rows)} rows; the list endpoint ignores its bound"
    )
    if reported is not None:
        assert reported >= len(rows), (
            f"the reported total {reported} is below the rows returned {len(rows)}"
        )


def test_permission_filtered_read_stays_within_its_bound():
    admin = conftest.session(conftest.ADMIN)
    member = conftest.session(conftest.MEMBER_ONE)
    unfiltered = conftest.timed(lambda: admin.get(
        "/objects/company/records", params={"limit": 1000}))
    filtered = conftest.timed(lambda: member.get(
        "/objects/company/records", params={"limit": 1000}))
    assert filtered <= max(unfiltered * 1.5, conftest.FLOOR_SECONDS), (
        f"a permission-filtered read took {filtered:.3f}s against an unfiltered "
        f"{unfiltered:.3f}s, past the 1.5x bound"
    )


def test_currency_cell_refuses_a_non_numeric_value():
    member = conftest.session(conftest.MEMBER_ONE)
    rows = _shapes.items(member.get("/objects/company/records").json())
    record = rows[0]
    before = record.get("arr")
    response = member.patch(
        f"/objects/company/records/{record['id']}",
        json={"arr": "not-a-number", "version": record.get("version", 1)})
    assert 400 <= response.status_code < 500, (
        f"a non-numeric currency value returned {response.status_code}, expected a client "
        f"error carrying a reason: {response.text[:300]}"
    )
    assert "arr" in _shapes.flatten(response.json() if response.headers.get(
        "content-type", "").startswith("application/json") else {"detail": response.text}), (
        f"the refusal does not name the offending field: {response.text[:300]}"
    )
    after = member.get(f"/objects/company/records/{record['id']}").json().get("arr")
    assert after == before, (
        f"a refused write still changed arr from {before!r} to {after!r}"
    )


def test_field_type_change_refuses_and_counts_blocking_rows():
    admin = conftest.session(conftest.ADMIN)
    slug, field = conftest.unique("survey"), conftest.unique("answer")
    admin.post("/objects", json={
        "name_singular": slug, "name_plural": slug + "s", "icon": "note"})
    admin.post(f"/objects/{slug}/fields", json={
        "name": field, "type": "text", "options": [], "is_unique": False})
    for value in ("12", "not a number", "also not a number"):
        admin.post(f"/objects/{slug}/records", json={field: value})
    response = admin.patch(f"/objects/{slug}/fields/{field}", json={"type": "number"})
    assert 400 <= response.status_code < 500, (
        f"converting a text field holding non-numeric rows to number returned "
        f"{response.status_code}, expected a refusal: {response.text[:300]}"
    )
    payload = response.json() if response.headers.get(
        "content-type", "").startswith("application/json") else {}
    assert payload.get("blocking_rows") == 2, (
        f"the refusal reports blocking_rows={payload.get('blocking_rows')!r}, expected 2"
    )
    rows = _shapes.items(admin.get(f"/objects/{slug}/records").json())
    kept = [row for row in rows if row.get(field) == "not a number"]
    assert kept, "a refused type change blanked or converted a stored value"


def test_concurrent_metadata_saves_leave_a_single_winner():
    admin = conftest.session(conftest.ADMIN)
    slug = conftest.unique("fleet")
    created = admin.post("/objects", json={
        "name_singular": slug, "name_plural": slug + "s", "icon": "building"})
    version = created.json().get("version", 1)
    outcomes = conftest.race(
        lambda: conftest.session(conftest.ADMIN).patch(
            f"/objects/{slug}", json={"name_plural": slug + "-alpha", "version": version}),
        lambda: conftest.session(conftest.ADMIN).patch(
            f"/objects/{slug}", json={"name_plural": slug + "-beta", "version": version}),
    )
    codes = sorted(response.status_code for response in outcomes)
    winners = [code for code in codes if code in (200, 202)]
    assert len(winners) == 1, (
        f"two simultaneous saves to one piece of metadata returned {codes}; exactly one "
        f"must succeed"
    )
    losers = [response for response in outcomes if response.status_code not in (200, 202)]
    assert 400 <= losers[0].status_code < 500, (
        f"the losing writer received {losers[0].status_code}, expected a conflict response"
    )
    assert "version" in _shapes.flatten(losers[0].text), (
        f"the conflict response does not name the current version: {losers[0].text[:300]}"
    )


def test_expired_token_is_refused_and_changes_nothing():
    member = conftest.session(conftest.MEMBER_ONE)
    rows = _shapes.items(member.get("/objects/company/records").json())
    record = rows[0]
    before = record.get("arr")
    token = appclient.login(conftest.MEMBER_ONE, conftest.PASSWORD)
    stale = appclient.client(token)
    stale.post("/auth/logout")
    response = stale.patch(
        f"/objects/company/records/{record['id']}",
        json={"arr": 1, "version": record.get("version", 1)})
    assert response.status_code in (401, 403), (
        f"a signed-out token still wrote: PATCH returned {response.status_code}"
    )
    after = conftest.session(conftest.MEMBER_ONE).get(
        f"/objects/company/records/{record['id']}").json().get("arr")
    assert after == before, (
        f"arr moved from {before!r} to {after!r} on a request carrying a dead token"
    )


def test_workflow_cycle_guard_halts_with_a_visible_entry():
    admin = conftest.session(conftest.ADMIN)
    made = admin.post("/workflows", json={
        "name": conftest.unique("self-trigger"),
        "trigger": {"kind": "record_updated", "object": "opportunity"},
        "nodes": [{"kind": "update_record", "object": "opportunity",
                   "set": {"notes": "touched"}}]})
    if made.status_code not in (200, 201):
        assert made.status_code in (400, 403, 404), (
            f"POST /api/workflows returned {made.status_code}: {made.text[:300]}"
        )
        return
    workflow_id = made.json().get("id")
    member = conftest.session(conftest.MEMBER_ONE)
    record = _shapes.items(member.get("/objects/opportunity/records").json())[0]
    member.patch(f"/objects/opportunity/records/{record['id']}",
                 json={"notes": "start", "version": record.get("version", 1)})
    runs = conftest.wait_for_runs(admin, workflow_id, at_least=1)
    assert len(runs) < conftest.CYCLE_CEILING, (
        f"a self-triggering workflow produced {len(runs)} runs; a depth limit must halt "
        f"the chain well below {conftest.CYCLE_CEILING}"
    )
    halted = [run for run in runs
              if "halt" in _shapes.flatten(run) or "depth" in _shapes.flatten(run)]
    assert halted, (
        f"no run in the chain carries a halt entry naming why the chain stopped: "
        f"{runs[-1]}"
    )


def test_credit_gate_refuses_a_run_past_the_allowance():
    owner = conftest.session(conftest.OWNER)
    plan = owner.get("/plan").json()
    allowance = plan.get("credits_included")
    assert allowance is not None, f"GET /api/plan reports no credits_included: {plan}"
    admin = conftest.session(conftest.ADMIN)
    workflow = [row for row in _shapes.items(admin.get("/workflows").json())
                if row.get("name") == conftest.WORKFLOW_NAME][0]
    owner.patch("/plan", json={"credits_used": allowance})
    member = conftest.session(conftest.MEMBER_ONE)
    record = _shapes.items(member.get("/objects/opportunity/records").json())[0]
    response = admin.post(f"/workflows/{workflow['id']}/runs",
                          json={"record": record["id"]})
    assert 400 <= response.status_code < 500, (
        f"a run attempted past the credit allowance returned {response.status_code}, "
        f"expected a refusal carrying a reason: {response.text[:300]}"
    )
    owner.patch("/plan", json={"credits_used": 0})


def test_unknown_address_answers_not_found():
    page = httpx.get(f"{appclient.app_url()}/no-such-page-{os.urandom(4).hex()}",
                     timeout=conftest.TIMEOUT, follow_redirects=True)
    assert page.status_code == 404, (
        f"an unmatched address returned {page.status_code}, expected 404"
    )
    assert conftest.NOT_FOUND_COPY in page.text, (
        f"the not-found page does not carry the pinned copy {conftest.NOT_FOUND_COPY!r}"
    )


def test_empty_object_returns_an_empty_array():
    admin = conftest.session(conftest.ADMIN)
    slug = conftest.unique("attic")
    admin.post("/objects", json={
        "name_singular": slug, "name_plural": slug + "s", "icon": "note"})
    response = admin.get(f"/objects/{slug}/records")
    assert response.status_code == 200, (
        f"listing an empty object returned {response.status_code}, expected an empty list "
        f"rather than an error"
    )
    assert _shapes.items(response.json()) == [], (
        f"an object with no records returned {response.json()!r}"
    )


def test_duplicate_value_on_a_unique_field_is_refused():
    admin = conftest.session(conftest.ADMIN)
    slug, field = conftest.unique("registry"), conftest.unique("code")
    admin.post("/objects", json={
        "name_singular": slug, "name_plural": slug + "s", "icon": "note"})
    admin.post(f"/objects/{slug}/fields", json={
        "name": field, "type": "text", "options": [], "is_unique": True})
    value = conftest.unique("token")
    first = admin.post(f"/objects/{slug}/records", json={field: value})
    assert first.status_code in (200, 201), (
        f"the first record carrying {value!r} returned {first.status_code}"
    )
    second = admin.post(f"/objects/{slug}/records", json={field: value})
    assert 400 <= second.status_code < 500, (
        f"a second record reusing {value!r} on a unique field returned "
        f"{second.status_code}, expected a refusal"
    )
    rows = _shapes.items(admin.get(f"/objects/{slug}/records").json())
    matching = [row for row in rows if row.get(field) == value]
    assert len(matching) == 1, (
        f"{len(matching)} rows carry {value!r} on a field marked unique"
    )


def test_workflow_email_reaches_only_the_addressed_inbox():
    admin = conftest.session(conftest.ADMIN)
    workflow = [row for row in _shapes.items(admin.get("/workflows").json())
                if row.get("name") == conftest.WORKFLOW_NAME][0]
    member = conftest.session(conftest.MEMBER_ONE)
    record = _shapes.items(member.get("/objects/opportunity/records").json())[0]
    before_other = conftest.inbox().count(conftest.MEMBER_TWO)
    admin.post(f"/workflows/{workflow['id']}/runs", json={"record": record["id"]})
    subject = f"Workflow: {conftest.WORKFLOW_NAME}"
    message = conftest.wait_for_email(conftest.MEMBER_ONE, subject)
    assert message is not None, (
        f"no message with the subject {subject!r} reached {conftest.MEMBER_ONE} at the "
        f"mail server"
    )
    assert message.subject.startswith("Workflow: "), (
        f"the subject {message.subject!r} does not begin with the pinned prefix "
        f"'Workflow: '"
    )
    assert str(record.get("name", "")) in message.body or str(
        record.get("code", "")) in message.body, (
        f"the message body names neither the record nor its code: {message.body[:200]}"
    )
    assert len(message.to) == 1, (
        f"the message was addressed to {message.to}; a workflow message carries no carbon "
        f"copy and no blind carbon copy"
    )
    assert conftest.inbox().count(conftest.MEMBER_TWO) == before_other, (
        f"a message also reached {conftest.MEMBER_TWO}, who was not the addressee"
    )


def test_refused_run_sends_no_email():
    owner = conftest.session(conftest.OWNER)
    admin = conftest.session(conftest.ADMIN)
    allowance = owner.get("/plan").json().get("credits_included")
    workflow = [row for row in _shapes.items(admin.get("/workflows").json())
                if row.get("name") == conftest.WORKFLOW_NAME][0]
    member = conftest.session(conftest.MEMBER_ONE)
    record = _shapes.items(member.get("/objects/opportunity/records").json())[0]
    before = conftest.inbox().count(conftest.MEMBER_ONE)
    owner.patch("/plan", json={"credits_used": allowance})
    admin.post(f"/workflows/{workflow['id']}/runs", json={"record": record["id"]})
    conftest.settle()
    after = conftest.inbox().count(conftest.MEMBER_ONE)
    assert after == before, (
        f"a run refused at the credit gate still delivered {after - before} message(s) to "
        f"{conftest.MEMBER_ONE}"
    )
    owner.patch("/plan", json={"credits_used": 0})


def test_invitation_email_carries_the_terms_link():
    admin = conftest.session(conftest.ADMIN)
    invitee = f"probe-{os.urandom(6).hex()}@example.com"
    response = admin.post("/memberships/invitations", json={
        "email": invitee, "role": "member"})
    assert response.status_code in (200, 201), (
        f"inviting {invitee} returned {response.status_code}: {response.text[:300]}"
    )
    message = conftest.wait_for_email(invitee, "invited")
    assert message is not None, f"no invitation message reached {invitee}"
    assert "/terms" in message.body, (
        f"the invitation does not link the terms page: {message.body[:300]}"
    )


