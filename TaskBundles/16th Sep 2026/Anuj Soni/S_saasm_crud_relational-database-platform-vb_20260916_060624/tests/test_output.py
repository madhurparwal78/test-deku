"""The one pytest module for Relational Database Platform.

Every section (core features, data integrity, authorization, edge cases) and the one
declared slot (db) are merged here. Fixtures, pinned literals and helpers live in
conftest.py; the shared grader (appclient, capabilities, _shapes) is on
PYTHONPATH=/tests from the deku-verifier-base image.

The checklist obligations each function discharges live in the pytest-provenance-v1
sidecar beside the bundle, not in a comment.

Channel disjointness, per reference/J J.12: the browser pass drives the base editor
through its own journeys, so every check here either reads a seeded record no journey
mutates, or works inside a per-run probe record it created itself and removed again.
"""

from __future__ import annotations

import json
import os
import re

import appclient
import conftest as cf



def test_health_endpoint_answers_two_hundred() -> None:
    """The app answers its health endpoint once it is ready."""
    with appclient.client(None) as client:
        response = client.get("/health")
    assert response.status_code == 200, cf.describe(
        response, "the health endpoint must answer 200 once the app is ready")


def test_login_returns_a_bearer_token() -> None:
    """A seeded account signs in and receives a bearer token."""
    token = appclient.login(cf.EDITOR_EMAIL, cf.SEEDED_PASSWORD)
    assert isinstance(token, str) and token, (
        f"login for {cf.EDITOR_EMAIL} must return a non-empty access_token")
    with appclient.client(token) as client:
        response = client.get(cf.workspaces_path())
        assert response.status_code == 200, cf.describe(
            response, "the token returned by login must reach the workspace list")


def test_every_seeded_account_signs_in_with_the_pinned_password() -> None:
    """All six seeded accounts use the one corpus password."""
    for email in (cf.OWNER_EMAIL, cf.CREATOR_EMAIL, cf.EDITOR_EMAIL,
                  cf.COMMENTER_EMAIL, cf.READER_EMAIL, cf.OWNER2_EMAIL):
        token = appclient.login(email, cf.SEEDED_PASSWORD)
        assert token, f"{email} must sign in with the seeded password"


def test_credentials_file_is_written_at_the_app_root() -> None:
    """The seeded credentials are readable at the documented path."""
    assert os.path.isfile(cf.CREDENTIALS_FILE), (
        f"{cf.CREDENTIALS_FILE} must exist so a signed-in account can be found")
    text = open(cf.CREDENTIALS_FILE, encoding="utf-8", errors="replace").read()
    assert cf.EDITOR_EMAIL in text, (
        f"{cf.CREDENTIALS_FILE} must name {cf.EDITOR_EMAIL}, read {text[:400]}")
    assert cf.SEEDED_PASSWORD in text, (
        f"{cf.CREDENTIALS_FILE} must carry the seeded password, read {text[:400]}")


def test_reserved_directories_exist_and_are_empty() -> None:
    """The two reserved directories exist at the app root and hold nothing."""
    for path in (cf.SCREENSHOT_DIR, cf.DOWNLOAD_DIR):
        assert os.path.isdir(path), f"{path} must exist at the app root"
        assert os.listdir(path) == [], f"{path} must start empty, held {os.listdir(path)}"


def test_field_type_catalogue_lists_all_nineteen_types(editor) -> None:
    """Every field type the brief pins is offered, with its computed flag."""
    rows = cf.read_array(editor, cf.field_types_path())
    slugs = [row.get("slug") for row in rows]
    for slug in cf.FIELD_TYPE_SLUGS:
        assert slug in slugs, f"the field type {slug} must be offered, saw {slugs}"
    assert len(slugs) == cf.FIELD_TYPE_COUNT, (
        f"exactly {cf.FIELD_TYPE_COUNT} field types must be offered, saw {len(slugs)}")
    for row in rows:
        expected = row.get("slug") in cf.COMPUTED_TYPE_SLUGS
        assert bool(row.get("computed")) is expected, (
            f"{row.get('slug')} must report computed={expected}, reported "
            f"{row.get('computed')}")


def test_seeded_base_carries_its_three_tables(editor) -> None:
    """The demonstration base is seeded with the three tables the brief names."""
    _, base = cf.campaign_planning(editor)
    names = [t.get("name") for t in (base.get("tables") or [])]
    for name in cf.CAMPAIGN_PLANNING_TABLES:
        assert name in names, f"the table {name} must be seeded, saw {names}"


def test_every_table_carries_at_least_one_grid_view(editor) -> None:
    """A table always has a grid view to fall back on."""
    _, base = cf.campaign_planning(editor)
    for table in base.get("tables") or []:
        types = [v.get("type") for v in (table.get("views") or [])]
        assert cf.VIEW_GRID in types, (
            f"table {table.get('name')} must carry a grid view, saw {types}")


def test_primary_field_is_first_and_is_never_a_computed_type(editor) -> None:
    """Exactly one primary field per table, and it is writable."""
    _, base = cf.campaign_planning(editor)
    for table in base.get("tables") or []:
        primaries = [f for f in (table.get("fields") or []) if f.get("isPrimary")]
        assert len(primaries) == 1, (
            f"table {table.get('name')} must carry exactly one primary field, saw "
            f"{[f.get('name') for f in primaries]}")
        assert primaries[0].get("type") not in cf.COMPUTED_TYPE_SLUGS, (
            f"the primary field of {table.get('name')} must not be a computed type, "
            f"is {primaries[0].get('type')}")


def test_object_identifiers_carry_their_type_prefix(editor) -> None:
    """Every identifier is seventeen characters behind a three-character prefix."""
    workspace = cf.workspace_by_slug(editor, cf.NORTHFIELD_SLUG)
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    record = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_AUTUMN)
    pairs = (
        (workspace.get("id"), cf.PREFIX_WORKSPACE),
        (base_id, cf.PREFIX_BASE),
        (table.get("id"), cf.PREFIX_TABLE),
        (cf.field_in(table, cf.FIELD_NAME).get("id"), cf.PREFIX_FIELD),
        (cf.grid_view_of(table).get("id"), cf.PREFIX_VIEW),
        (record.get("id"), cf.PREFIX_RECORD),
    )
    for value, prefix in pairs:
        assert isinstance(value, str), f"identifier {value!r} must be a string"
        assert value.startswith(prefix), (
            f"an identifier of that kind must begin {prefix}, saw {value}")
        assert len(value) == cf.IDENTIFIER_LENGTH, (
            f"{value} must be {cf.IDENTIFIER_LENGTH} characters, is {len(value)}")


def test_rollup_offers_all_sixteen_aggregations(editor) -> None:
    """The rollup type declares every aggregation the brief pins."""
    rows = cf.read_array(editor, cf.field_types_path())
    rollup = cf.find_by(rows, "slug", "rollup")
    assert rollup is not None, "the rollup field type must be offered"
    declared = json.dumps(rollup.get("config") or {})
    for name in cf.ROLLUP_AGGREGATIONS:
        assert re.search(rf"\b{name}\b", declared), (
            f"the rollup configuration must offer {name}, declared {declared[:400]}")


def test_formula_offers_all_twelve_functions(editor) -> None:
    """The formula type declares every function the brief pins."""
    rows = cf.read_array(editor, cf.field_types_path())
    formula = cf.find_by(rows, "slug", "formula")
    assert formula is not None, "the formula field type must be offered"
    declared = json.dumps(formula.get("config") or {})
    for name in cf.FORMULA_FUNCTIONS:
        assert re.search(rf"\b{name}\b", declared), (
            f"the formula configuration must offer {name}, declared {declared[:400]}")


def test_select_choices_carry_a_colour_name_from_the_palette(editor) -> None:
    """A select choice names its colour so the meaning survives without sight."""
    _, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    stage = cf.field_in(table, cf.FIELD_STAGE)
    choices = (stage.get("config") or {}).get("choices") or []
    names = [c.get("name") for c in choices if isinstance(c, dict)]
    for stage_name in cf.SEEDED_STAGES:
        assert stage_name in names, (
            f"the choice {stage_name} must be configured on {cf.FIELD_STAGE}, saw {names}")
    for choice in choices:
        colour = (choice or {}).get("color") or (choice or {}).get("colour")
        assert colour in cf.CHOICE_COLOURS, (
            f"the choice {choice.get('name')} must carry a colour name from "
            f"{list(cf.CHOICE_COLOURS)}, carried {colour!r}")


def test_seeded_formula_field_is_marked_invalid(editor) -> None:
    """The deliberately broken formula reports itself rather than failing the table."""
    _, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    note = cf.field_in(table, cf.FIELD_OWNER_NOTE)
    assert note.get("isValid") is False, (
        f"{cf.FIELD_OWNER_NOTE} must report isValid false, reported {note.get('isValid')}")


def test_seeded_guards_carry_their_authored_messages(owner) -> None:
    """Both seeded guards exist, in the right mode, with the exact authored wording."""
    base_id, _ = cf.campaign_planning(owner)
    guards = cf.read_array(owner, cf.guards_path(base_id))
    messages = {g.get("message"): g.get("mode") for g in guards}
    assert messages.get(cf.GUARD_BLOCKING_MESSAGE) == cf.GUARD_BLOCKING, (
        f"the blocking guard must read {cf.GUARD_BLOCKING_MESSAGE!r}, saw {messages}")
    assert messages.get(cf.GUARD_ADVISORY_MESSAGE) == cf.GUARD_ADVISORY, (
        f"the advisory guard must read {cf.GUARD_ADVISORY_MESSAGE!r}, saw {messages}")


def test_privacy_page_is_readable_without_signing_in() -> None:
    """The privacy page answers to somebody with no account."""
    response = cf.fetch_document(cf.ROUTE_PRIVACY)
    assert response.status_code == 200, cf.describe(
        response, f"{cf.ROUTE_PRIVACY} must answer without a session")
    assert len(response.text) > 200, (
        f"{cf.ROUTE_PRIVACY} must state what is stored, read {response.text[:200]}")


def test_favicon_is_served_and_declared_in_the_document_head() -> None:
    """The product serves its own mark rather than a blank tab."""
    page = cf.fetch_document(cf.ROUTE_LOGIN)
    assert page.status_code == 200, cf.describe(page, "the login page must answer")
    match = re.search(r'<link[^>]+rel=["\'][^"\']*icon[^"\']*["\'][^>]*>', page.text,
                      re.IGNORECASE)
    assert match, f"the document head must declare a favicon, read {page.text[:400]}"
    href = re.search(r'href=["\']([^"\']+)["\']', match.group(0), re.IGNORECASE)
    assert href, f"the favicon link must carry an href, read {match.group(0)}"
    icon = cf.fetch_document(href.group(1)) if href.group(1).startswith("/") else None
    assert icon is not None and icon.status_code == 200, (
        f"the declared favicon {href.group(1)} must resolve over HTTP")


def test_public_routes_declare_a_social_preview_that_resolves() -> None:
    """Every public route carries its own preview title and a reachable image."""
    for route in cf.PUBLIC_ROUTES:
        page = cf.fetch_document(route)
        assert page.status_code == 200, cf.describe(page, f"{route} must answer")
        title = re.search(
            r'<meta[^>]+property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']',
            page.text, re.IGNORECASE)
        assert title, f"{route} must declare an og:title, read {page.text[:400]}"
        image = re.search(
            r'<meta[^>]+property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
            page.text, re.IGNORECASE)
        assert image, f"{route} must declare an og:image, read {page.text[:400]}"
        target = image.group(1)
        if target.startswith("/"):
            resolved = cf.fetch_document(target)
            assert resolved.status_code == 200, cf.describe(
                resolved, f"the og:image of {route} must resolve")


def test_public_routes_declare_distinct_preview_titles() -> None:
    """No two public routes share a preview title."""
    titles = {}
    for route in cf.PUBLIC_ROUTES:
        page = cf.fetch_document(route)
        found = re.search(
            r'<meta[^>]+property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']',
            page.text, re.IGNORECASE)
        assert found, f"{route} must declare an og:title"
        titles[route] = found.group(1)
    assert len(set(titles.values())) == len(titles), (
        f"every public route must declare its own preview title, saw {titles}")


def test_unknown_address_answers_not_found_with_a_way_back() -> None:
    """An address the app does not recognise renders the product's own page."""
    suffix = cf.unique_suffix()
    response = cf.fetch_document(f"/no-such-place-{suffix}")
    assert response.status_code == 404, cf.describe(
        response, "an unknown address must answer as not found")
    assert cf.ROUTE_WORKSPACES in response.text or "Workspaces" in response.text, (
        f"the not-found page must offer a way back to {cf.ROUTE_WORKSPACES}, read "
        f"{response.text[:400]}")


def test_no_credential_appears_in_anything_the_browser_downloads() -> None:
    """The seeded password and the database address stay out of the client."""
    for route in cf.PUBLIC_ROUTES + (cf.ROUTE_WORKSPACES,):
        page = cf.fetch_document(route)
        body = page.text
        assert cf.SEEDED_PASSWORD not in body, (
            f"{route} must not ship the seeded password to the browser")
        assert "postgresql://" not in body, (
            f"{route} must not ship a database address to the browser")



def test_cell_written_through_the_api_is_persisted_and_survives_a_re_read(editor) -> None:
    """The critical focus: the stored row matches what was written, after a re-read."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    budget = cf.field_in(table, cf.FIELD_BUDGET)
    record = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_AUTUMN)
    original = (record.get("cells") or {}).get(budget["id"])
    response = editor.patch(cf.record_path(base_id, table["id"], record["id"]),
                            json={"cells": {budget["id"]: cf.BUDGET_PROBE}})
    assert response.status_code in cf.OK, cf.describe(
        response, f"an editor must be able to set {cf.FIELD_BUDGET}")
    written = str((response.json().get("cells") or {}).get(budget["id"]))
    assert written == cf.BUDGET_PROBE, (
        f"the write must answer with {cf.BUDGET_PROBE}, answered {written}")
    again = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_AUTUMN)
    stored = str((again.get("cells") or {}).get(budget["id"]))
    assert stored == cf.BUDGET_PROBE, (
        f"the stored row must read {cf.BUDGET_PROBE} on a re-read, read {stored}")
    restore = editor.patch(cf.record_path(base_id, table["id"], record["id"]),
                           json={"cells": {budget["id"]: original}})
    assert restore.status_code in cf.OK, cf.describe(
        restore, "the probe write must be restorable")


def test_stored_row_matches_the_record_endpoint_for_every_seeded_campaign(editor) -> None:
    """Each seeded campaign is a real row with the budget the brief pins."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    budget = cf.field_in(table, cf.FIELD_BUDGET)
    stage = cf.field_in(table, cf.FIELD_STAGE)
    expected = {
        cf.CAMPAIGN_AUTUMN: (cf.BUDGET_AUTUMN, cf.STAGE_LIVE),
        cf.CAMPAIGN_HARBOUR: (cf.BUDGET_HARBOUR, cf.STAGE_PLANNING),
        cf.CAMPAIGN_WINTER: (cf.BUDGET_WINTER, cf.STAGE_WRAPPED),
    }
    for name, (amount, stage_name) in expected.items():
        record = cf.record_by_primary(editor, base_id, table, name)
        cells = record.get("cells") or {}
        assert str(cells.get(budget["id"])) == amount, (
            f"{name} must carry a {cf.FIELD_BUDGET} of {amount}, carried "
            f"{cells.get(budget['id'])}")
        assert cells.get(stage["id"]) == stage_name, (
            f"{name} must carry the stage {stage_name}, carried {cells.get(stage['id'])}")


def test_seeded_deliverable_rows_are_stored_in_the_database(backend) -> None:
    """The seeded deliverables are rows in the declared datastore, not page state."""
    assert backend.count(cf.TABLE_RECORDS) > 0, (
        "the seeded records must be rows in the declared datastore")
    assert backend.count(cf.TABLE_OPERATIONS) > 0, (
        "the seeded operation log must be rows in the declared datastore")


def test_rollup_climbs_two_tables_when_a_task_minutes_value_changes(editor) -> None:
    """One cell change recomputes the deliverable hours and the campaign total."""
    base_id, base = cf.campaign_planning(editor)
    tasks = cf.table_in(base, cf.TABLE_TASKS)
    deliverables = cf.table_in(base, cf.TABLE_DELIVERABLES)
    campaigns = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    minutes = cf.field_in(tasks, cf.FIELD_MINUTES)
    hours = cf.field_in(deliverables, cf.FIELD_HOURS)
    total = cf.field_in(campaigns, cf.FIELD_TOTAL_HOURS)

    task_rows = cf.read_array(editor, cf.records_path(base_id, tasks["id"]))
    assert task_rows, "the Tasks table must be seeded"
    task = task_rows[0]
    before_hours = json.dumps(cf.read_array(
        editor, cf.records_path(base_id, deliverables["id"])))
    before_total = json.dumps(cf.read_array(
        editor, cf.records_path(base_id, campaigns["id"])))
    original = (task.get("cells") or {}).get(minutes["id"])
    bumped = (int(original) if str(original).isdigit() else 0) + 30

    response = editor.patch(cf.record_path(base_id, tasks["id"], task["id"]),
                            json={"cells": {minutes["id"]: bumped}})
    assert response.status_code in cf.OK, cf.describe(
        response, f"an editor must be able to set {cf.FIELD_MINUTES}")
    after_hours = json.dumps(cf.read_array(
        editor, cf.records_path(base_id, deliverables["id"])))
    after_total = json.dumps(cf.read_array(
        editor, cf.records_path(base_id, campaigns["id"])))
    assert hours["id"] in after_hours, f"{cf.FIELD_HOURS} must appear on a deliverable row"
    assert total["id"] in after_total, f"{cf.FIELD_TOTAL_HOURS} must appear on a campaign row"
    assert after_hours != before_hours, (
        f"changing {cf.FIELD_MINUTES} must change the deliverable {cf.FIELD_HOURS}")
    assert after_total != before_total, (
        f"changing {cf.FIELD_MINUTES} must change the campaign {cf.FIELD_TOTAL_HOURS}")

    restore = editor.patch(cf.record_path(base_id, tasks["id"], task["id"]),
                           json={"cells": {minutes["id"]: original}})
    assert restore.status_code in cf.OK, cf.describe(
        restore, "the probe write must be restorable")


def test_computed_values_are_returned_on_every_record_row(editor) -> None:
    """A record carries the current value of every computed field on that row."""
    base_id, base = cf.campaign_planning(editor)
    campaigns = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    computed_ids = [f["id"] for f in (campaigns.get("fields") or [])
                    if f.get("type") in cf.COMPUTED_TYPE_SLUGS]
    assert computed_ids, "the Campaigns table must carry at least one computed field"
    for row in cf.read_array(editor, cf.records_path(base_id, campaigns["id"])):
        computed = row.get("computed") or {}
        for field_id in computed_ids:
            assert field_id in computed, (
                f"record {row.get('id')} must carry the computed value of {field_id}, "
                f"carried {sorted(computed)}")


def test_count_counta_and_countall_return_three_different_numbers(editor) -> None:
    """The three counting aggregations are distinct, on the worked example."""
    base_id, base = cf.campaign_planning(editor)
    campaigns = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    link = cf.field_in(campaigns, cf.FIELD_DELIVERABLES)
    made = []
    for aggregation, expected in (("COUNT", cf.WORKED_COUNT),
                                  ("COUNTA", cf.WORKED_COUNTA),
                                  ("COUNTALL", cf.WORKED_COUNTALL),
                                  ("SUM", cf.WORKED_SUM)):
        response = editor.post(cf.fields_path(base_id, campaigns["id"]), json={
            "name": f"{aggregation} probe {cf.unique_suffix()}",
            "type": "rollup" if aggregation != "COUNTALL" else "rollup",
            "config": {"recordLinkFieldId": link["id"],
                       "fieldIdInLinkedTable": cf.field_in(
                           cf.table_in(base, cf.TABLE_DELIVERABLES), cf.FIELD_HOURS)["id"],
                       "aggregation": aggregation},
        })
        assert response.status_code in cf.CREATED, cf.describe(
            response, f"a creator must be able to add a {aggregation} rollup")
        made.append((response.json().get("id"), aggregation, expected))
    row = cf.record_by_primary(editor, base_id, campaigns, cf.CAMPAIGN_AUTUMN)
    seen = {}
    for field_id, aggregation, _expected in made:
        seen[aggregation] = (row.get("computed") or {}).get(field_id)
    assert len({seen.get("COUNT"), seen.get("COUNTA"), seen.get("COUNTALL")}) >= 2, (
        f"COUNT, COUNTA and COUNTALL must not all return one number, returned {seen}")
    for field_id, _aggregation, _expected in made:
        editor.delete(cf.field_path(base_id, campaigns["id"], field_id))


def test_operation_sequence_is_gapless_within_the_base(editor) -> None:
    """The log of one base increases strictly from one, with no gap and no repeat."""
    base_id, _ = cf.campaign_planning(editor)
    rows = cf.read_array(editor, cf.operations_path(base_id))
    sequences = sorted(int(row["sequence"]) for row in rows)
    assert sequences, "the operation log must carry the operations that seeded the base"
    assert sequences[0] == 1, f"the first sequence must be 1, was {sequences[0]}"
    assert sequences == list(range(1, len(sequences) + 1)), (
        f"sequences must be gapless from 1, saw {sequences[:20]}")
    assert len(set(sequences)) == len(sequences), (
        "no sequence value may be issued twice within one base")


def test_operation_log_row_is_never_updated_or_deleted(editor) -> None:
    """An appended operation is immutable through every route the app offers."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_TASKS)
    before = cf.read_array(editor, cf.operations_path(base_id))
    oldest = min(before, key=lambda row: int(row["sequence"]))
    suffix = cf.unique_suffix()
    created = editor.post(cf.records_path(base_id, table["id"]), json={
        "cells": {cf.field_in(table, cf.FIELD_TITLE)["id"]: cf.probe_title(suffix)}})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "an editor must be able to create a task row")
    editor.delete(cf.record_path(base_id, table["id"], created.json()["id"]))
    after = cf.read_array(editor, cf.operations_path(base_id))
    still = cf.find_by(after, "id", oldest["id"])
    assert still is not None, "an operation must survive every later write"
    assert still.get("before") == oldest.get("before"), (
        "an operation's before value must never change once written")
    assert still.get("after") == oldest.get("after"), (
        "an operation's after value must never change once written")
    assert len(after) > len(before), (
        f"creating and deleting a record must append operations, went "
        f"{len(before)} to {len(after)}")


def test_two_simultaneous_writes_take_two_different_sequences(editor) -> None:
    """Concurrent writes to one base never share a sequence and never leave a gap."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_TASKS)
    title = cf.field_in(table, cf.FIELD_TITLE)
    suffix = cf.unique_suffix()

    def write(n: int):
        return editor.post(cf.records_path(base_id, table["id"]), json={
            "cells": {title["id"]: cf.probe_title(f"{suffix}-{n}")}})

    results = cf.run_together([lambda: write(1), lambda: write(2),
                               lambda: write(3), lambda: write(4)])
    created = [r for r in results if getattr(r, "status_code", 0) in cf.CREATED]
    assert len(created) == 4, (
        f"four concurrent creates must all be accepted, accepted {len(created)}")
    rows = cf.read_array(editor, cf.operations_path(base_id))
    sequences = sorted(int(row["sequence"]) for row in rows)
    assert len(set(sequences)) == len(sequences), (
        f"concurrent writes must not share a sequence, saw a repeat in {sequences[:20]}")
    assert sequences == list(range(1, len(sequences) + 1)), (
        f"concurrent writes must leave no gap, saw {sequences[:20]}")
    for response in created:
        editor.delete(cf.record_path(base_id, table["id"], response.json()["id"]))


def test_auto_numbers_stay_unique_under_concurrent_creation(editor) -> None:
    """Two records created at the same moment never share an auto number."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_TASKS)
    title = cf.field_in(table, cf.FIELD_TITLE)
    suffix = cf.unique_suffix()

    def write(n: int):
        return editor.post(cf.records_path(base_id, table["id"]), json={
            "cells": {title["id"]: cf.probe_title(f"{suffix}-auto-{n}")}})

    results = cf.run_together([lambda: write(1), lambda: write(2), lambda: write(3)])
    created = [r for r in results if getattr(r, "status_code", 0) in cf.CREATED]
    assert len(created) == 3, (
        f"three concurrent creates must all be accepted, accepted {len(created)}")
    numbers = [r.json().get("autoNumber") for r in created]
    assert len(set(numbers)) == 3, (
        f"three concurrent records must carry three auto numbers, carried {numbers}")
    for response in created:
        editor.delete(cf.record_path(base_id, table["id"], response.json()["id"]))


def test_record_history_reads_back_a_change_that_was_stored(editor) -> None:
    """Record history names the field, the old value and the new one."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_TASKS)
    title = cf.field_in(table, cf.FIELD_TITLE)
    minutes = cf.field_in(table, cf.FIELD_MINUTES)
    suffix = cf.unique_suffix()
    created = editor.post(cf.records_path(base_id, table["id"]), json={
        "cells": {title["id"]: cf.probe_title(suffix), minutes["id"]: 10}})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "an editor must be able to create a task row")
    record_id = created.json()["id"]
    changed = editor.patch(cf.record_path(base_id, table["id"], record_id),
                           json={"cells": {minutes["id"]: 25}})
    assert changed.status_code in cf.OK, cf.describe(changed, "the probe write must land")
    history = cf.read_array(
        editor, cf.record_history_path(base_id, table["id"], record_id))
    assert history, "a changed record must carry history"
    entry = history[0]
    assert entry.get("fieldId") == minutes["id"], (
        f"the newest history entry must name {cf.FIELD_MINUTES}, named "
        f"{entry.get('fieldId')}")
    assert str(entry.get("after")) == "25", (
        f"the newest history entry must carry the new value, carried {entry.get('after')}")
    assert entry.get("actor"), "a history entry must name the account that caused it"
    editor.delete(cf.record_path(base_id, table["id"], record_id))


def test_historical_read_returns_the_values_stored_at_that_sequence(editor) -> None:
    """A read as of a sequence rebuilds the table as it stood then."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    budget = cf.field_in(table, cf.FIELD_BUDGET)
    record = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_HARBOUR)
    original = (record.get("cells") or {}).get(budget["id"])
    mark = cf.latest_sequence(editor, base_id)
    changed = editor.patch(cf.record_path(base_id, table["id"], record["id"]),
                           json={"cells": {budget["id"]: cf.BUDGET_PROBE}})
    assert changed.status_code in cf.OK, cf.describe(changed, "the probe write must land")
    rows = cf.read_array(editor, cf.records_path(base_id, table["id"]), asOf=mark)
    past = cf.find_by(rows, "id", record["id"])
    assert past is not None, "the historical read must still carry the record"
    assert str((past.get("cells") or {}).get(budget["id"])) == str(original), (
        f"the historical read must carry {original}, carried "
        f"{(past.get('cells') or {}).get(budget['id'])}")
    live = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_HARBOUR)
    assert str((live.get("cells") or {}).get(budget["id"])) == cf.BUDGET_PROBE, (
        "the live read must carry the new value while the historical read carries the old")
    editor.patch(cf.record_path(base_id, table["id"], record["id"]),
                 json={"cells": {budget["id"]: original}})


def test_historical_read_recomputes_computed_fields_from_rebuilt_values(editor) -> None:
    """A rollup read as of a sequence is recomputed rather than replayed from a cache."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    total = cf.field_in(table, cf.FIELD_TOTAL_HOURS)
    mark = cf.latest_sequence(editor, base_id)
    rows = cf.read_array(editor, cf.records_path(base_id, table["id"]), asOf=mark)
    assert rows, "the historical read must return the seeded campaigns"
    for row in rows:
        assert total["id"] in (row.get("computed") or {}), (
            f"a historical row must carry the recomputed {cf.FIELD_TOTAL_HOURS}, carried "
            f"{sorted(row.get('computed') or {})}")


def test_replay_verification_agrees_with_the_stored_rows(editor) -> None:
    """Rebuilding the base from the log matches what is stored."""
    base_id, _ = cf.campaign_planning(editor)
    response = editor.get(cf.replay_path(base_id))
    assert response.status_code == 200, cf.describe(
        response, "replay verification must answer for a seeded base")
    payload = response.json()
    assert payload.get("agrees") is True, (
        f"a base with no write outside the log must agree, answered {payload}")


def test_seeding_is_idempotent_across_a_re_read(editor) -> None:
    """The seeded row counts are stable, so a restart duplicated nothing."""
    base_id, base = cf.campaign_planning(editor)
    campaigns = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    deliverables = cf.table_in(base, cf.TABLE_DELIVERABLES)
    campaign_rows = cf.read_array(editor, cf.records_path(base_id, campaigns["id"]))
    deliverable_rows = cf.read_array(editor, cf.records_path(base_id, deliverables["id"]))
    assert len(campaign_rows) == len(cf.SEEDED_CAMPAIGNS), (
        f"exactly {len(cf.SEEDED_CAMPAIGNS)} campaigns must be seeded, saw "
        f"{len(campaign_rows)}")
    assert len(deliverable_rows) == len(cf.SEEDED_DELIVERABLES), (
        f"exactly {len(cf.SEEDED_DELIVERABLES)} deliverables must be seeded, saw "
        f"{len(deliverable_rows)}")


def test_link_deletion_leaves_no_half_of_the_pair_behind(editor) -> None:
    """Removing a record removes both sides of every link naming it."""
    base_id, base = cf.campaign_planning(editor)
    deliverables = cf.table_in(base, cf.TABLE_DELIVERABLES)
    tasks = cf.table_in(base, cf.TABLE_TASKS)
    link = cf.field_in(deliverables, cf.FIELD_TASKS)
    title = cf.field_in(tasks, cf.FIELD_TITLE)
    suffix = cf.unique_suffix()
    task = editor.post(cf.records_path(base_id, tasks["id"]), json={
        "cells": {title["id"]: cf.probe_title(suffix)}})
    assert task.status_code in cf.CREATED, cf.describe(task, "the probe task must be created")
    task_id = task.json()["id"]
    parent = cf.record_by_primary(editor, base_id, deliverables, cf.DELIVERABLE_MAILER)
    existing = list((parent.get("cells") or {}).get(link["id"]) or [])
    joined = editor.patch(cf.record_path(base_id, deliverables["id"], parent["id"]),
                          json={"cells": {link["id"]: existing + [task_id]}})
    assert joined.status_code in cf.OK, cf.describe(joined, "the probe link must be created")
    editor.delete(cf.record_path(base_id, tasks["id"], task_id))
    after = cf.record_by_primary(editor, base_id, deliverables, cf.DELIVERABLE_MAILER)
    remaining = list((after.get("cells") or {}).get(link["id"]) or [])
    assert task_id not in remaining, (
        f"deleting the task must remove it from {cf.FIELD_TASKS}, left {remaining}")


def test_symmetric_link_writes_the_mirrored_reference(editor) -> None:
    """Creating a link from one side puts the record on the other side too."""
    base_id, base = cf.campaign_planning(editor)
    deliverables = cf.table_in(base, cf.TABLE_DELIVERABLES)
    tasks = cf.table_in(base, cf.TABLE_TASKS)
    link = cf.field_in(deliverables, cf.FIELD_TASKS)
    inverse_id = (link.get("config") or {}).get("inverseLinkFieldId")
    assert inverse_id, (
        f"{cf.FIELD_TASKS} must name its inverseLinkFieldId, carried {link.get('config')}")
    title = cf.field_in(tasks, cf.FIELD_TITLE)
    suffix = cf.unique_suffix()
    task = editor.post(cf.records_path(base_id, tasks["id"]), json={
        "cells": {title["id"]: cf.probe_title(suffix)}})
    assert task.status_code in cf.CREATED, cf.describe(task, "the probe task must be created")
    task_id = task.json()["id"]
    parent = cf.record_by_primary(editor, base_id, deliverables, cf.DELIVERABLE_SIGNAGE)
    existing = list((parent.get("cells") or {}).get(link["id"]) or [])
    joined = editor.patch(cf.record_path(base_id, deliverables["id"], parent["id"]),
                          json={"cells": {link["id"]: existing + [task_id]}})
    assert joined.status_code in cf.OK, cf.describe(joined, "the probe link must be created")
    rows = cf.read_array(editor, cf.records_path(base_id, tasks["id"]))
    mirrored = cf.find_by(rows, "id", task_id)
    back = list((mirrored.get("cells") or {}).get(inverse_id) or [])
    assert parent["id"] in back, (
        f"the mirrored reference must name {parent['id']}, named {back}")
    editor.delete(cf.record_path(base_id, tasks["id"], task_id))



def test_commenter_is_denied_changing_a_cell_value(commenter, editor) -> None:
    """A commenter may read everything and may never change a value."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    budget = cf.field_in(table, cf.FIELD_BUDGET)
    record = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_WINTER)
    before = (record.get("cells") or {}).get(budget["id"])
    response = commenter.patch(cf.record_path(base_id, table["id"], record["id"]),
                               json={"cells": {budget["id"]: cf.BUDGET_PROBE}})
    assert response.status_code in cf.DENIED, cf.describe(
        response, "a commenter must be denied changing a cell value")
    after = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_WINTER)
    assert (after.get("cells") or {}).get(budget["id"]) == before, (
        f"the stored row must be untouched by a denied write, went {before} to "
        f"{(after.get('cells') or {}).get(budget['id'])}")


def test_reader_is_denied_creating_a_record(reader, editor) -> None:
    """A reader writes nothing anywhere."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_TASKS)
    title = cf.field_in(table, cf.FIELD_TITLE)
    before = len(cf.read_array(editor, cf.records_path(base_id, table["id"])))
    response = reader.post(cf.records_path(base_id, table["id"]), json={
        "cells": {title["id"]: cf.probe_title(cf.unique_suffix())}})
    assert response.status_code in cf.DENIED, cf.describe(
        response, "a reader must be denied creating a record")
    after = len(cf.read_array(editor, cf.records_path(base_id, table["id"])))
    assert after == before, f"a denied create must store no row, went {before} to {after}"


def test_editor_is_denied_creating_a_field(editor) -> None:
    """Shaping the schema belongs to a creator and above."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_TASKS)
    before = len(table.get("fields") or [])
    response = editor.post(cf.fields_path(base_id, table["id"]), json={
        "name": f"Probe {cf.unique_suffix()}", "type": "singleLineText", "config": {}})
    assert response.status_code in cf.DENIED, cf.describe(
        response, "an editor must be denied creating a field")
    _, again = cf.campaign_planning(editor)
    after = len(cf.table_in(again, cf.TABLE_TASKS).get("fields") or [])
    assert after == before, f"a denied create must add no field, went {before} to {after}"


def test_creator_is_denied_creating_a_guard(creator, owner) -> None:
    """Declaring an invariant belongs to the owner of the workspace."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_TASKS)
    before = len(cf.read_array(owner, cf.guards_path(base_id)))
    response = creator.post(cf.guards_path(base_id), json={
        "tableId": table["id"], "name": f"Probe {cf.unique_suffix()}",
        "condition": {"field": cf.FIELD_MINUTES, "operator": "is empty"},
        "mode": cf.GUARD_ADVISORY, "message": "Probe guard."})
    assert response.status_code in cf.DENIED, cf.describe(
        response, "a creator must be denied creating a guard")
    after = len(cf.read_array(owner, cf.guards_path(base_id)))
    assert after == before, f"a denied create must add no guard, went {before} to {after}"


def test_cross_workspace_request_cannot_read_a_base(outsider, editor) -> None:
    """A member of another workspace is answered as though the base does not exist."""
    base_id, _ = cf.campaign_planning(editor)
    response = outsider.get(cf.base_path(base_id))
    assert response.status_code in cf.NOT_FOUND, cf.describe(
        response, "an outsider must be answered as though the base does not exist")


def test_cross_workspace_request_cannot_read_a_record_by_identifier(outsider, editor) -> None:
    """Naming a record directly reaches no further than naming its base."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    record = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_AUTUMN)
    response = outsider.get(cf.record_path(base_id, table["id"], record["id"]))
    assert response.status_code in cf.NOT_FOUND, cf.describe(
        response, "an outsider must not reach a record by its own identifier")


def test_workspace_list_holds_only_workspaces_the_caller_reaches(editor, outsider) -> None:
    """Each account sees the workspaces it holds a grant in, and no others."""
    mine = [row.get("slug") for row in cf.read_array(editor, cf.workspaces_path())]
    theirs = [row.get("slug") for row in cf.read_array(outsider, cf.workspaces_path())]
    assert cf.NORTHFIELD_SLUG in mine, f"{cf.EDITOR_EMAIL} must see {cf.NORTHFIELD_SLUG}"
    assert cf.HARBOURLINE_SLUG not in mine, (
        f"{cf.EDITOR_EMAIL} must not see {cf.HARBOURLINE_SLUG}, saw {mine}")
    assert cf.HARBOURLINE_SLUG in theirs, f"{cf.OWNER2_EMAIL} must see {cf.HARBOURLINE_SLUG}"
    assert cf.NORTHFIELD_SLUG not in theirs, (
        f"{cf.OWNER2_EMAIL} must not see {cf.NORTHFIELD_SLUG}, saw {theirs}")


def test_anonymous_request_is_denied_at_the_api(anonymous) -> None:
    """A caller with no bearer token reaches nothing behind the boundary."""
    response = anonymous.get(cf.workspaces_path())
    assert response.status_code in cf.DENIED, cf.describe(
        response, "an unauthenticated caller must be denied the workspace list")


def test_expired_or_forged_token_reads_as_not_signed_in() -> None:
    """A token the app never issued is refused."""
    with appclient.client("not-a-real-token-" + cf.unique_suffix()) as client:
        response = client.get(cf.workspaces_path())
    assert response.status_code in cf.DENIED, cf.describe(
        response, "a token the app never issued must read as not signed in")


def test_workspace_role_is_reported_for_each_seeded_account() -> None:
    """The effective role each seeded account holds is what the brief pins."""
    expected = {
        cf.OWNER_EMAIL: cf.ROLE_OWNER,
        cf.CREATOR_EMAIL: cf.ROLE_CREATOR,
        cf.EDITOR_EMAIL: cf.ROLE_EDITOR,
        cf.COMMENTER_EMAIL: cf.ROLE_COMMENTER,
        cf.READER_EMAIL: cf.ROLE_READER,
    }
    for email, role in expected.items():
        with appclient.client(appclient.login(email, cf.SEEDED_PASSWORD)) as client:
            workspace = cf.workspace_by_slug(client, cf.NORTHFIELD_SLUG)
            assert workspace.get("role") == role, (
                f"{email} must hold {role} in {cf.NORTHFIELD_SLUG}, holds "
                f"{workspace.get('role')}")


def test_computed_field_refuses_a_written_value(editor) -> None:
    """A computed field is never writable through any route."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    total = cf.field_in(table, cf.FIELD_TOTAL_HOURS)
    record = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_AUTUMN)
    before = (record.get("computed") or {}).get(total["id"])
    response = editor.patch(cf.record_path(base_id, table["id"], record["id"]),
                            json={"cells": {total["id"]: 999}})
    assert cf.is_client_error(response), cf.describe(
        response, f"writing {cf.FIELD_TOTAL_HOURS} must be refused")
    after = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_AUTUMN)
    assert (after.get("computed") or {}).get(total["id"]) == before, (
        "a refused write to a computed field must leave the value unchanged")


def test_personal_view_refuses_configuration_from_another_account(creator, editor) -> None:
    """A personal view belongs to the account that made it."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    suffix = cf.unique_suffix()
    created = creator.post(cf.fields_path(base_id, table["id"]).replace("/fields", "/views"),
                           json={"name": f"Personal {suffix}", "type": cf.VIEW_GRID,
                                 "mode": cf.MODE_PERSONAL, "config": {}})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a creator must be able to add a personal view")
    view_id = created.json()["id"]
    response = editor.patch(cf.view_path(base_id, view_id),
                            json={"name": f"Taken {suffix}"})
    assert response.status_code in cf.DENIED, cf.describe(
        response, "another account must be denied configuring a personal view")
    creator.delete(cf.view_path(base_id, view_id))


def test_locked_view_refuses_configuration_until_unlocked(creator, owner) -> None:
    """Locking protects the configuration of a view, and nothing else."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    suffix = cf.unique_suffix()
    created = creator.post(cf.fields_path(base_id, table["id"]).replace("/fields", "/views"),
                           json={"name": f"Locked {suffix}", "type": cf.VIEW_GRID,
                                 "mode": cf.MODE_LOCKED, "config": {}})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a creator must be able to add a locked view")
    view_id = created.json()["id"]
    response = creator.patch(cf.view_path(base_id, view_id),
                             json={"config": {"rowHeight": "tall"}})
    assert cf.is_client_error(response), cf.describe(
        response, "a locked view must refuse a configuration change")
    unlocked = owner.patch(cf.view_path(base_id, view_id),
                           json={"mode": cf.MODE_COLLABORATIVE})
    assert unlocked.status_code in cf.OK, cf.describe(
        unlocked, "an owner must be able to unlock a view")
    owner.delete(cf.view_path(base_id, view_id))



def test_blocking_guard_refuses_the_write_with_its_authored_message(editor, owner) -> None:
    """A blocking guard refuses, in its author's own words."""
    base_id, base = cf.campaign_planning(editor)
    deliverables = cf.table_in(base, cf.TABLE_DELIVERABLES)
    done = cf.field_in(deliverables, cf.FIELD_DONE)
    estimate = cf.field_in(deliverables, cf.FIELD_ESTIMATE)
    target = None
    for row in cf.read_array(editor, cf.records_path(base_id, deliverables["id"])):
        cells = row.get("cells") or {}
        if not cells.get(estimate["id"]) and not cells.get(done["id"]):
            target = row
            break
    assert target is not None, (
        f"one seeded deliverable must carry an empty {cf.FIELD_ESTIMATE}")
    response = editor.patch(cf.record_path(base_id, deliverables["id"], target["id"]),
                            json={"cells": {done["id"]: True}})
    assert cf.is_client_error(response), cf.describe(
        response, "a blocking guard must refuse the write")
    assert cf.error_message(response) == cf.GUARD_BLOCKING_MESSAGE, (
        f"the refusal must read {cf.GUARD_BLOCKING_MESSAGE!r}, read "
        f"{cf.error_message(response)!r}")


def test_blocking_guard_leaves_no_stored_row_and_appends_no_operation(editor) -> None:
    """A refused write leaves nothing at all behind."""
    base_id, base = cf.campaign_planning(editor)
    deliverables = cf.table_in(base, cf.TABLE_DELIVERABLES)
    done = cf.field_in(deliverables, cf.FIELD_DONE)
    estimate = cf.field_in(deliverables, cf.FIELD_ESTIMATE)
    target = None
    for row in cf.read_array(editor, cf.records_path(base_id, deliverables["id"])):
        cells = row.get("cells") or {}
        if not cells.get(estimate["id"]) and not cells.get(done["id"]):
            target = row
            break
    assert target is not None, (
        f"one seeded deliverable must carry an empty {cf.FIELD_ESTIMATE}")
    before = cf.latest_sequence(editor, base_id)
    response = editor.patch(cf.record_path(base_id, deliverables["id"], target["id"]),
                            json={"cells": {done["id"]: True}})
    assert cf.is_client_error(response), cf.describe(
        response, "a blocking guard must refuse the write")
    after = cf.latest_sequence(editor, base_id)
    assert after == before, (
        f"a refused write must append no operation, sequence went {before} to {after}")
    again = cf.find_by(cf.read_array(
        editor, cf.records_path(base_id, deliverables["id"])), "id", target["id"])
    assert not (again.get("cells") or {}).get(done["id"]), (
        f"a refused write must leave {cf.FIELD_DONE} unticked")


def test_advisory_guard_allows_the_write_and_records_a_violation(owner) -> None:
    """An advisory guard is a note, not a refusal."""
    base_id, _ = cf.campaign_planning(owner)
    guards = cf.read_array(owner, cf.guards_path(base_id))
    advisory = cf.find_by(guards, "message", cf.GUARD_ADVISORY_MESSAGE)
    assert advisory is not None, "the advisory guard must be seeded"
    assert advisory.get("mode") == cf.GUARD_ADVISORY, (
        f"that guard must be advisory, is {advisory.get('mode')}")
    violations = advisory.get("violations")
    assert violations, (
        f"the advisory guard must list an outstanding violation, listed {violations}")


def test_guard_refuses_a_direct_request_exactly_as_it_refuses_the_grid(editor) -> None:
    """A guard applies on every path into the data."""
    base_id, base = cf.campaign_planning(editor)
    deliverables = cf.table_in(base, cf.TABLE_DELIVERABLES)
    done = cf.field_in(deliverables, cf.FIELD_DONE)
    estimate = cf.field_in(deliverables, cf.FIELD_ESTIMATE)
    title = cf.field_in(deliverables, cf.FIELD_TITLE)
    suffix = cf.unique_suffix()
    created = editor.post(cf.records_path(base_id, deliverables["id"]), json={
        "cells": {title["id"]: cf.probe_title(suffix), done["id"]: True,
                  estimate["id"]: None}})
    assert cf.is_client_error(created), cf.describe(
        created, "a create that violates a blocking guard must be refused")
    assert cf.error_message(created) == cf.GUARD_BLOCKING_MESSAGE, (
        f"the refusal must read {cf.GUARD_BLOCKING_MESSAGE!r}, read "
        f"{cf.error_message(created)!r}")


def test_view_refuses_a_fiftieth_filter_condition(creator) -> None:
    """The condition limit is enforced and the refusal names it."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    stage = cf.field_in(table, cf.FIELD_STAGE)
    view = cf.grid_view_of(table)
    conditions = [{"fieldId": stage["id"], "operator": "is", "value": cf.STAGE_LIVE}
                  for _ in range(cf.MAX_FILTER_CONDITIONS + 1)]
    response = creator.patch(cf.view_path(base_id, view["id"]),
                             json={"config": {"filters": {"conjunction": "AND",
                                                          "conditions": conditions}}})
    assert cf.is_client_error(response), cf.describe(
        response, f"a view must refuse more than {cf.MAX_FILTER_CONDITIONS} conditions")
    assert str(cf.MAX_FILTER_CONDITIONS) in response.text, (
        f"the refusal must name the limit {cf.MAX_FILTER_CONDITIONS}, read "
        f"{response.text[:400]}")


def test_view_refuses_a_fourth_grouping_level(creator) -> None:
    """Grouping stops at three levels and says so."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    stage = cf.field_in(table, cf.FIELD_STAGE)
    view = cf.grid_view_of(table)
    response = creator.patch(cf.view_path(base_id, view["id"]), json={
        "config": {"groups": [{"fieldId": stage["id"]}] * (cf.MAX_GROUP_LEVELS + 1)}})
    assert cf.is_client_error(response), cf.describe(
        response, f"a view must refuse more than {cf.MAX_GROUP_LEVELS} group levels")
    assert str(cf.MAX_GROUP_LEVELS) in response.text, (
        f"the refusal must name the limit {cf.MAX_GROUP_LEVELS}, read "
        f"{response.text[:400]}")


def test_view_refuses_an_eleventh_sort_level(creator) -> None:
    """Sorting stops at ten levels and says so."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    stage = cf.field_in(table, cf.FIELD_STAGE)
    view = cf.grid_view_of(table)
    response = creator.patch(cf.view_path(base_id, view["id"]), json={
        "config": {"sorts": [{"fieldId": stage["id"], "direction": "asc"}]
                   * (cf.MAX_SORT_LEVELS + 1)}})
    assert cf.is_client_error(response), cf.describe(
        response, f"a view must refuse more than {cf.MAX_SORT_LEVELS} sort levels")
    assert str(cf.MAX_SORT_LEVELS) in response.text, (
        f"the refusal must name the limit {cf.MAX_SORT_LEVELS}, read "
        f"{response.text[:400]}")


def test_view_refuses_a_fourth_level_of_filter_nesting(creator) -> None:
    """Filter nesting stops at three levels and says so."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    stage = cf.field_in(table, cf.FIELD_STAGE)
    view = cf.grid_view_of(table)
    leaf = {"fieldId": stage["id"], "operator": "is", "value": cf.STAGE_LIVE}
    group = {"conjunction": "AND", "conditions": [leaf]}
    for _ in range(cf.MAX_FILTER_NESTING):
        group = {"conjunction": "AND", "conditions": [group]}
    response = creator.patch(cf.view_path(base_id, view["id"]),
                             json={"config": {"filters": group}})
    assert cf.is_client_error(response), cf.describe(
        response, f"a view must refuse nesting deeper than {cf.MAX_FILTER_NESTING}")


def test_duplicate_field_name_in_one_table_is_refused(creator) -> None:
    """Two fields in one table never share a name."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_TASKS)
    response = creator.post(cf.fields_path(base_id, table["id"]), json={
        "name": cf.FIELD_MINUTES, "type": "number", "config": {"precision": 0}})
    assert cf.is_client_error(response), cf.describe(
        response, f"a second field named {cf.FIELD_MINUTES} must be refused")


def test_historical_read_refuses_every_change(editor) -> None:
    """Nothing is editable while reading the past."""
    base_id, base = cf.campaign_planning(editor)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    budget = cf.field_in(table, cf.FIELD_BUDGET)
    record = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_WINTER)
    before = (record.get("cells") or {}).get(budget["id"])
    mark = cf.latest_sequence(editor, base_id)
    response = editor.patch(
        cf.record_path(base_id, table["id"], record["id"]),
        params={"asOf": mark}, json={"cells": {budget["id"]: cf.BUDGET_PROBE}})
    assert cf.is_client_error(response), cf.describe(
        response, "a change naming asOf must be refused")
    after = cf.record_by_primary(editor, base_id, table, cf.CAMPAIGN_WINTER)
    assert (after.get("cells") or {}).get(budget["id"]) == before, (
        "a refused historical change must leave the live value unchanged")


def test_cyclic_computed_configuration_is_refused_at_save(creator) -> None:
    """A field that would depend on itself is refused when it is configured."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    total = cf.field_in(table, cf.FIELD_TOTAL_HOURS)
    response = creator.patch(cf.field_path(base_id, table["id"], total["id"]), json={
        "type": "formula",
        "config": {"formula": f"{{{cf.FIELD_TOTAL_HOURS}}} + 1",
                   "referencedFieldIds": [total["id"]]}})
    assert cf.is_client_error(response), cf.describe(
        response, "a self-referential computed field must be refused at save")


def test_group_on_a_computed_field_refuses_a_direct_create(creator, editor) -> None:
    """There is no value to write into a group formed on a computed field."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    count_field = cf.field_in(table, cf.FIELD_DELIVERABLE_COUNT)
    view = cf.grid_view_of(table)
    grouped = creator.patch(cf.view_path(base_id, view["id"]), json={
        "config": {"groups": [{"fieldId": count_field["id"]}]}})
    assert grouped.status_code in cf.OK, cf.describe(
        grouped, "a view must accept a group on a computed field")
    name = cf.field_in(table, cf.FIELD_NAME)
    response = editor.post(cf.records_path(base_id, table["id"]), json={
        "viewId": view["id"], "groupValue": 1,
        "cells": {name["id"]: cf.probe_title(cf.unique_suffix())}})
    assert cf.is_client_error(response), cf.describe(
        response, "creating into a group formed on a computed field must be refused")
    creator.patch(cf.view_path(base_id, view["id"]), json={"config": {"groups": []}})


def test_long_field_name_and_long_cell_value_are_both_accepted(creator, editor) -> None:
    """A two hundred character name and a ten thousand character value both land."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_TASKS)
    long_name = ("Probe " + cf.unique_suffix() + " ") * 10
    long_name = long_name[:200].ljust(200, "x")
    created = creator.post(cf.fields_path(base_id, table["id"]), json={
        "name": long_name, "type": "multilineText", "config": {}})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a 200 character field name must be accepted")
    field_id = created.json()["id"]
    title = cf.field_in(table, cf.FIELD_TITLE)
    row = editor.post(cf.records_path(base_id, table["id"]), json={
        "cells": {title["id"]: cf.probe_title(cf.unique_suffix()),
                  field_id: "y" * 10000}})
    assert row.status_code in cf.CREATED, cf.describe(
        row, "a 10000 character cell value must be accepted")
    stored = (row.json().get("cells") or {}).get(field_id)
    assert stored is not None and len(str(stored)) == 10000, (
        f"the stored value must keep its 10000 characters, kept "
        f"{len(str(stored)) if stored else 0}")
    editor.delete(cf.record_path(base_id, table["id"], row.json()["id"]))
    creator.delete(cf.field_path(base_id, table["id"], field_id))


def test_duration_stores_whole_seconds(creator, editor) -> None:
    """Ninety minutes is five thousand four hundred seconds, whatever it displays as."""
    base_id, base = cf.campaign_planning(creator)
    deliverables = cf.table_in(base, cf.TABLE_DELIVERABLES)
    estimate = cf.field_in(deliverables, cf.FIELD_ESTIMATE)
    record = cf.record_by_primary(editor, base_id, deliverables, cf.DELIVERABLE_PRESS_PACK)
    original = (record.get("cells") or {}).get(estimate["id"])
    response = editor.patch(cf.record_path(base_id, deliverables["id"], record["id"]),
                            json={"cells": {estimate["id"]: cf.NINETY_MINUTES_SECONDS}})
    assert response.status_code in cf.OK, cf.describe(
        response, f"an editor must be able to set {cf.FIELD_ESTIMATE}")
    again = cf.record_by_primary(editor, base_id, deliverables, cf.DELIVERABLE_PRESS_PACK)
    assert int((again.get("cells") or {}).get(estimate["id"])) == cf.NINETY_MINUTES_SECONDS, (
        f"{cf.FIELD_ESTIMATE} must store {cf.NINETY_MINUTES_SECONDS} whole seconds, "
        f"stored {(again.get('cells') or {}).get(estimate['id'])}")
    editor.patch(cf.record_path(base_id, deliverables["id"], record["id"]),
                 json={"cells": {estimate["id"]: original}})


def test_precision_changes_display_and_never_storage(creator, editor) -> None:
    """A number keeps every digit it was given."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_TASKS)
    created = creator.post(cf.fields_path(base_id, table["id"]), json={
        "name": f"Precision probe {cf.unique_suffix()}", "type": "number",
        "config": {"precision": 2}})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a creator must be able to add a number field")
    field_id = created.json()["id"]
    title = cf.field_in(table, cf.FIELD_TITLE)
    row = editor.post(cf.records_path(base_id, table["id"]), json={
        "cells": {title["id"]: cf.probe_title(cf.unique_suffix()), field_id: 3.14159}})
    assert row.status_code in cf.CREATED, cf.describe(row, "the probe row must be created")
    stored = float((row.json().get("cells") or {}).get(field_id))
    assert abs(stored - 3.14159) < 1e-9, (
        f"the stored number must keep 3.14159, kept {stored}")
    editor.delete(cf.record_path(base_id, table["id"], row.json()["id"]))
    creator.delete(cf.field_path(base_id, table["id"], field_id))


def test_find_is_case_sensitive_and_search_is_not(creator, editor) -> None:
    """The one deliberate difference between the two text locators survives."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_TASKS)
    title = cf.field_in(table, cf.FIELD_TITLE)
    made = []
    for name, expression in (("FIND probe", 'FIND("ab", "AB")'),
                             ("SEARCH probe", 'SEARCH("ab", "AB")')):
        response = creator.post(cf.fields_path(base_id, table["id"]), json={
            "name": f"{name} {cf.unique_suffix()}", "type": "formula",
            "config": {"formula": expression, "referencedFieldIds": []}})
        assert response.status_code in cf.CREATED, cf.describe(
            response, f"a creator must be able to add {name}")
        made.append((name, response.json()["id"]))
    row = editor.post(cf.records_path(base_id, table["id"]), json={
        "cells": {title["id"]: cf.probe_title(cf.unique_suffix())}})
    assert row.status_code in cf.CREATED, cf.describe(row, "the probe row must be created")
    computed = (row.json().get("computed") or {})
    find_value = computed.get(made[0][1])
    search_value = computed.get(made[1][1])
    assert not find_value, (
        f"FIND must find nothing in a case mismatch, returned {find_value}")
    assert search_value, (
        f"SEARCH must find a match in a case mismatch, returned {search_value}")
    editor.delete(cf.record_path(base_id, table["id"], row.json()["id"]))
    for _name, field_id in made:
        creator.delete(cf.field_path(base_id, table["id"], field_id))


def test_round_rounds_half_away_from_zero(creator, editor) -> None:
    """The rounding mode is stated rather than inherited."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_TASKS)
    title = cf.field_in(table, cf.FIELD_TITLE)
    created = creator.post(cf.fields_path(base_id, table["id"]), json={
        "name": f"Round probe {cf.unique_suffix()}", "type": "formula",
        "config": {"formula": "ROUND(2.5, 0)", "referencedFieldIds": []}})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a creator must be able to add a rounding formula")
    field_id = created.json()["id"]
    row = editor.post(cf.records_path(base_id, table["id"]), json={
        "cells": {title["id"]: cf.probe_title(cf.unique_suffix())}})
    assert row.status_code in cf.CREATED, cf.describe(row, "the probe row must be created")
    value = (row.json().get("computed") or {}).get(field_id)
    assert str(value) in ("3", "3.0"), (
        f"ROUND(2.5, 0) must give 3 under half away from zero, gave {value}")
    editor.delete(cf.record_path(base_id, table["id"], row.json()["id"]))
    creator.delete(cf.field_path(base_id, table["id"], field_id))


def test_decimal_addition_on_money_is_exact(creator, editor) -> None:
    """A tenth plus two tenths is three tenths."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_TASKS)
    title = cf.field_in(table, cf.FIELD_TITLE)
    created = creator.post(cf.fields_path(base_id, table["id"]), json={
        "name": f"Decimal probe {cf.unique_suffix()}", "type": "formula",
        "config": {"formula": "0.1 + 0.2", "referencedFieldIds": []}})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a creator must be able to add a decimal formula")
    field_id = created.json()["id"]
    row = editor.post(cf.records_path(base_id, table["id"]), json={
        "cells": {title["id"]: cf.probe_title(cf.unique_suffix())}})
    assert row.status_code in cf.CREATED, cf.describe(row, "the probe row must be created")
    value = str((row.json().get("computed") or {}).get(field_id))
    assert value in ("0.3", "0.30"), (
        f"0.1 + 0.2 must give exactly 0.3, gave {value}")
    editor.delete(cf.record_path(base_id, table["id"], row.json()["id"]))
    creator.delete(cf.field_path(base_id, table["id"], field_id))


def test_invalid_lookup_configuration_blanks_the_field(creator, editor) -> None:
    """A broken configuration signals itself rather than failing the table."""
    base_id, base = cf.campaign_planning(creator)
    campaigns = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    deliverables = cf.table_in(base, cf.TABLE_DELIVERABLES)
    link = cf.field_in(campaigns, cf.FIELD_DELIVERABLES)
    source = creator.post(cf.fields_path(base_id, deliverables["id"]), json={
        "name": f"Source probe {cf.unique_suffix()}", "type": "singleLineText",
        "config": {}})
    assert source.status_code in cf.CREATED, cf.describe(
        source, "a creator must be able to add the source field")
    source_id = source.json()["id"]
    lookup = creator.post(cf.fields_path(base_id, campaigns["id"]), json={
        "name": f"Lookup probe {cf.unique_suffix()}", "type": "multipleLookupValues",
        "config": {"recordLinkFieldId": link["id"], "fieldIdInLinkedTable": source_id}})
    assert lookup.status_code in cf.CREATED, cf.describe(
        lookup, "a creator must be able to add the lookup")
    lookup_id = lookup.json()["id"]
    removed = creator.delete(cf.field_path(base_id, deliverables["id"], source_id))
    assert removed.status_code in cf.OK, cf.describe(
        removed, "a creator must be able to remove the source field")
    _, again = cf.campaign_planning(creator)
    field = cf.find_by(cf.table_in(again, cf.TABLE_CAMPAIGNS).get("fields") or [],
                       "id", lookup_id)
    assert field is not None and field.get("isValid") is False, (
        f"the lookup must report isValid false once its source is gone, reported "
        f"{field.get('isValid') if field else None}")
    for row in cf.read_array(editor, cf.records_path(base_id, campaigns["id"])):
        assert not (row.get("computed") or {}).get(lookup_id), (
            f"an invalid lookup must blank every cell, row {row.get('id')} kept "
            f"{(row.get('computed') or {}).get(lookup_id)}")
    creator.delete(cf.field_path(base_id, campaigns["id"], lookup_id))


def test_empty_operations_page_after_the_newest_sequence(editor) -> None:
    """Asking for what happened after the newest operation returns nothing."""
    base_id, _ = cf.campaign_planning(editor)
    newest = cf.latest_sequence(editor, base_id)
    rows = cf.read_array(editor, cf.operations_path(base_id), since=newest)
    assert rows == [], (
        f"nothing has happened after sequence {newest}, returned {len(rows)} rows")


def test_structural_limits_are_declared_on_the_base(editor) -> None:
    """Every structural limit is named with its value, so a refusal can name it."""
    base_id, base = cf.campaign_planning(editor)
    limits = base.get("limits") or {}
    expected = {
        "recordsPerBase": cf.MAX_RECORDS_PER_BASE,
        "tablesPerBase": cf.MAX_TABLES_PER_BASE,
        "basesPerWorkspace": cf.MAX_BASES_PER_WORKSPACE,
        "fieldsPerTable": cf.MAX_FIELDS_PER_TABLE,
        "viewsPerTable": cf.MAX_VIEWS_PER_TABLE,
        "filterConditionsPerView": cf.MAX_FILTER_CONDITIONS,
        "filterNesting": cf.MAX_FILTER_NESTING,
        "groupLevels": cf.MAX_GROUP_LEVELS,
        "sortLevels": cf.MAX_SORT_LEVELS,
        "kanbanStacks": cf.MAX_KANBAN_STACKS,
        "guardsPerBase": cf.MAX_GUARDS_PER_BASE,
    }
    for key, value in expected.items():
        assert int(limits.get(key, -1)) == value, (
            f"the base must declare {key} as {value}, declared {limits.get(key)}")


def test_kanban_view_stacks_by_exactly_one_single_select_field(creator) -> None:
    """A kanban view has one stacking level, named by one single-select field."""
    base_id, base = cf.campaign_planning(creator)
    table = cf.table_in(base, cf.TABLE_CAMPAIGNS)
    stage = cf.field_in(table, cf.FIELD_STAGE)
    title = cf.field_in(table, cf.FIELD_NAME)
    suffix = cf.unique_suffix()
    created = creator.post(cf.fields_path(base_id, table["id"]).replace("/fields", "/views"),
                           json={"name": f"Board {suffix}", "type": cf.VIEW_KANBAN,
                                 "mode": cf.MODE_COLLABORATIVE,
                                 "config": {"stackFieldId": stage["id"]}})
    assert created.status_code in cf.CREATED, cf.describe(
        created, "a creator must be able to add a kanban view")
    view_id = created.json()["id"]
    assert (created.json().get("config") or {}).get("stackFieldId") == stage["id"], (
        f"the kanban view must stack by {cf.FIELD_STAGE}, stacks by "
        f"{(created.json().get('config') or {}).get('stackFieldId')}")
    refused = creator.patch(cf.view_path(base_id, view_id), json={
        "config": {"stackFieldId": [stage["id"], title["id"]]}})
    assert cf.is_client_error(refused), cf.describe(
        refused, "a second stacking level must be refused")
    creator.delete(cf.view_path(base_id, view_id))


def test_absent_surfaces_answer_as_not_found(editor) -> None:
    """The product holds records only: every surface this brief leaves out is absent."""
    for path in ("/uploads", "/attachments", "/messages", "/notifications", "/comments",
                 "/payments", "/subscriptions", "/automations", "/webhooks", "/sync"):
        response = editor.get(path)
        assert response.status_code in (404, 405), cf.describe(
            response, f"the product declares no {path} surface")


def test_first_paint_delivers_complete_html_for_a_route() -> None:
    """A route arrives as readable HTML rather than as an empty shell."""
    page = cf.fetch_document(cf.ROUTE_LOGIN)
    assert page.status_code == 200, cf.describe(page, "the login page must answer")
    body = re.sub(r"(?is)<script.*?</script>", "", page.text)
    text = re.sub(r"(?s)<[^>]+>", " ", body)
    assert len(text.split()) >= 5, (
        f"the first paint must carry readable text for the route, carried {text[:200]}")
