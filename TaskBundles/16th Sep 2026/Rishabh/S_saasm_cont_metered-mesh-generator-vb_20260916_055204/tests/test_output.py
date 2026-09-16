"""Deterministic substeps for deku/metered-mesh-generator-vb.

Every assertion here observes a side effect the brief pins: an HTTP status, a
response body, a row in the datastore or an object in the store. What a person
sees and what needs judgment are graded elsewhere.
"""

from __future__ import annotations

import os

import httpx
from _shapes import flatten, items
from appclient import api_base, app_url, client, login
from conftest import (ACCEPTED_SOURCE_FORMATS, ANONYMOUS_ALLOWANCE,
                      CLAIM_WINDOW_HOURS, CONVERTER_PAIR_COUNT, CREATOR2_EMAIL,
                      CREATOR3_EMAIL, CREATOR_EMAIL, DOWNLOAD_KINDS,
                      GALLERY_ITEMS, JOB_STATES, PLAN_KEYS,
                      PLAN_MONTHLY_CREDITS, PLAN_QUEUE, POLYGON_CEILING,
                      PROMOTION_END, PROMOTION_START, PUBLISHED_CLAIM_KEYS,
                      SAMPLE_KEYS, SEED_PASSWORD, SUCCESS_RATE_VALUE, TIERS,
                      balance_of, completed_asset, expected_cost, settle,
                      submit_job, unique_key, wait_for_job_state)


def test_health_endpoint_answers_ready(anon_client):
    """GET /api/health answers 200 once the app is ready."""
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:400]}"
    )


def test_seeded_creator_signs_in_with_pinned_password(creator_client):
    """The seeded creator signs in with the pinned corpus password."""
    response = creator_client.get("/session")
    assert response.status_code == 200, (
        f"GET /api/session for {CREATOR_EMAIL} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    assert CREATOR_EMAIL in flatten(response.json()), (
        f"GET /api/session does not identify {CREATOR_EMAIL}: {response.text[:400]}"
    )


def test_sign_in_with_wrong_password_is_refused(anon_client):
    """A wrong password is refused and the message names neither half."""
    response = anon_client.post(
        "/auth/login", json={"email": CREATOR_EMAIL, "password": "not-the-seeded-password"}
    )
    assert response.status_code == 401, (
        f"login with a wrong password returned {response.status_code}, expected 401: "
        f"{response.text[:400]}"
    )
    body = response.text.lower()
    assert "password" not in body or "email" not in body, (
        f"the refusal names both halves of the pair, which discloses which was wrong: "
        f"{response.text[:400]}"
    )


def test_library_request_without_session_is_refused(anon_client):
    """A library read with no session is refused at the API."""
    response = anon_client.get("/assets")
    assert response.status_code == 401, (
        f"GET /api/assets with no session returned {response.status_code}, expected "
        f"401: {response.text[:400]}"
    )


def test_tier_table_carries_the_four_pinned_tiers(anon_client):
    """One stored tier table carries all four tiers with their pinned parameters."""
    response = anon_client.get("/tiers")
    assert response.status_code == 200, (
        f"GET /api/tiers returned {response.status_code}: {response.text[:400]}"
    )
    rows = {row.get("key"): row for row in items(response.json())}
    assert set(rows) == set(TIERS), (
        f"GET /api/tiers carries {sorted(rows)}, expected {sorted(TIERS)}"
    )
    for key, pinned in TIERS.items():
        row = rows[key]
        blob = flatten(row)
        for field, value in pinned.items():
            assert str(value) in blob, (
                f"tier {key!r} does not carry its pinned {field} of {value}: {row}"
            )


def test_tier_ultra_carries_the_published_polygon_ceiling(anon_client):
    """The site's maximum polygon ceiling is one number, and ultra carries it."""
    response = anon_client.get("/tiers")
    assert response.status_code == 200, (
        f"GET /api/tiers returned {response.status_code}: {response.text[:400]}"
    )
    rows = {row.get("key"): row for row in items(response.json())}
    assert str(POLYGON_CEILING) in flatten(rows["ultra"]), (
        f"the ultra tier does not carry the published ceiling {POLYGON_CEILING}: "
        f"{rows['ultra']}"
    )
    ceilings = []
    for row in rows.values():
        for field in ("polygons", "polygon_ceiling", "max_polygons"):
            if isinstance(row.get(field), int):
                ceilings.append(row[field])
    assert ceilings and max(ceilings) == POLYGON_CEILING, (
        f"the highest stored polygon ceiling is {max(ceilings) if ceilings else None}, "
        f"but the site publishes {POLYGON_CEILING}"
    )


def test_plans_endpoint_carries_the_three_pinned_plans(anon_client):
    """The three plans carry their pinned credits, queue placement and licence."""
    response = anon_client.get("/plans")
    assert response.status_code == 200, (
        f"GET /api/plans returned {response.status_code}: {response.text[:400]}"
    )
    payload = response.json()
    rows = {row.get("key"): row for row in items(payload.get("plans", payload))}
    assert set(rows) == set(PLAN_KEYS), (
        f"GET /api/plans carries {sorted(rows)}, expected {sorted(PLAN_KEYS)}"
    )
    for key, credits in PLAN_MONTHLY_CREDITS.items():
        assert str(credits) in flatten(rows[key]), (
            f"plan {key!r} does not carry its pinned monthly credits {credits}: {rows[key]}"
        )
    for key, queue in PLAN_QUEUE.items():
        assert queue in flatten(rows[key]), (
            f"plan {key!r} does not carry its pinned queue placement {queue!r}: {rows[key]}"
        )


def test_promotion_carries_a_start_and_an_end_date(anon_client):
    """The promotional price is data with a start and an end, not open-ended copy."""
    response = anon_client.get("/plans")
    assert response.status_code == 200, (
        f"GET /api/plans returned {response.status_code}: {response.text[:400]}"
    )
    blob = flatten(response.json())
    assert PROMOTION_START in blob, (
        f"GET /api/plans carries no promotion start of {PROMOTION_START}: {blob[:600]}"
    )
    assert PROMOTION_END in blob, (
        f"GET /api/plans carries no promotion end of {PROMOTION_END}: {blob[:600]}"
    )


def test_job_submission_returns_a_queued_job(creator_client):
    """A submitted job is observably queued rather than already finished."""
    response = submit_job(creator_client, tier="standard")
    assert response.status_code in (200, 201, 202), (
        f"POST /api/jobs returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    assert body.get("state") in ("queued", "processing"), (
        f"a freshly submitted job reports state {body.get('state')!r}; a conversion "
        f"that is complete at the instant of submission is not the product: {body}"
    )


def test_job_reaches_a_terminal_completed_state(creator_client):
    """A submitted job advances on its own to a terminal completed state."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    assert asset_id, f"job {job_id} completed without naming an asset"
    response = creator_client.get(f"/jobs/{job_id}")
    assert response.status_code == 200, (
        f"GET /api/jobs/{job_id} returned {response.status_code}: {response.text[:400]}"
    )
    assert response.json().get("state") in JOB_STATES, (
        f"job {job_id} carries a state outside the closed set {JOB_STATES}: "
        f"{response.text[:400]}"
    )


def test_cost_charged_equals_cost_shown(creator_client, db):
    """The credit a job settles at is the credit its creator was shown."""
    before = balance_of(creator_client)
    response = submit_job(creator_client, tier="pro")
    assert response.status_code in (200, 201, 202), (
        f"POST /api/jobs returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    job_id = body.get("id") or body.get("job_id")
    shown = body.get("cost_shown")
    assert shown == expected_cost("pro"), (
        f"job {job_id} reports cost_shown {shown!r}, expected {expected_cost('pro')} "
        f"for the pro tier with textures off"
    )

    def read():
        got = creator_client.get(f"/jobs/{job_id}")
        return got.json() if got.status_code == 200 else None

    final = wait_for_job_state(read, {"completed", "failed"})
    assert final is not None and final.get("state") == "completed", (
        f"job {job_id} did not complete, last state was "
        f"{final.get('state') if final else None!r}"
    )
    assert final.get("cost_charged") == shown, (
        f"job {job_id} was shown {shown} credits and charged "
        f"{final.get('cost_charged')}"
    )
    after = balance_of(creator_client)
    assert before - after == shown, (
        f"the balance moved by {before - after} credits for a job shown at {shown}"
    )
    rows = db.rows("job", id=job_id)
    if rows:
        assert str(shown) in flatten(rows[0]), (
            f"the stored job row does not carry the charged cost {shown}: {rows[0]}"
        )


def test_default_generator_selection_costs_ten_credits(anon_client):
    """The default generator selection costs the pinned ten credits."""
    response = anon_client.get("/tiers")
    assert response.status_code == 200, (
        f"GET /api/tiers returned {response.status_code}: {response.text[:400]}"
    )
    rows = {row.get("key"): row for row in items(response.json())}
    blob = flatten(rows["pro"])
    assert str(expected_cost("pro")) in blob, (
        f"the pro tier does not cost the pinned {expected_cost('pro')} credits: "
        f"{rows['pro']}"
    )


def test_completed_asset_carries_three_download_formats(creator_client):
    """One generation yields one asset carrying glb, obj and stl representations."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    response = creator_client.get(f"/assets/{asset_id}")
    assert response.status_code == 200, (
        f"GET /api/assets/{asset_id} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    blob = flatten(response.json())
    for kind in DOWNLOAD_KINDS:
        assert kind in blob, (
            f"asset {asset_id} from job {job_id} carries no {kind!r} representation: "
            f"{response.text[:600]}"
        )


def test_samples_endpoint_serves_four_precomputed_assets(anon_client):
    """The four samples resolve to stored assets rather than starting a conversion."""
    response = anon_client.get("/samples")
    assert response.status_code == 200, (
        f"GET /api/samples returned {response.status_code}: {response.text[:400]}"
    )
    rows = items(response.json())
    keys = {row.get("key") for row in rows}
    assert set(SAMPLE_KEYS) <= keys, (
        f"GET /api/samples carries {sorted(k for k in keys if k)}, expected the four "
        f"pinned samples {sorted(SAMPLE_KEYS)}"
    )
    for row in rows:
        if row.get("key") in SAMPLE_KEYS:
            assert row.get("asset_id") or row.get("asset"), (
                f"sample {row.get('key')!r} names no pre-computed asset, so choosing "
                f"it would re-run the conversion: {row}"
            )


def test_gallery_items_name_their_source_and_tier(anon_client):
    """Every published gallery item names its source image and its quality tier."""
    response = anon_client.get("/gallery")
    assert response.status_code == 200, (
        f"GET /api/gallery returned {response.status_code}: {response.text[:400]}"
    )
    rows = {row.get("title"): row for row in items(response.json())}
    for title, tier in GALLERY_ITEMS.items():
        assert title in rows, (
            f"the gallery does not publish {title!r}: {sorted(t for t in rows if t)}"
        )
        blob = flatten(rows[title])
        assert tier in blob, (
            f"gallery item {title!r} does not name its tier {tier!r}: {rows[title]}"
        )
        assert "source" in blob, (
            f"gallery item {title!r} does not name its source image: {rows[title]}"
        )


def test_published_claims_carry_a_basis_and_a_measured_date(anon_client):
    """Every published figure is a stored row with a basis and a measurement date."""
    response = anon_client.get("/claims/published")
    assert response.status_code == 200, (
        f"GET /api/claims/published returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    rows = {row.get("key"): row for row in items(response.json())}
    assert set(PUBLISHED_CLAIM_KEYS) <= set(rows), (
        f"the stored figures are {sorted(k for k in rows if k)}, expected at least "
        f"{sorted(PUBLISHED_CLAIM_KEYS)}"
    )
    for key in PUBLISHED_CLAIM_KEYS:
        row = rows[key]
        assert row.get("basis"), f"published figure {key!r} carries no basis: {row}"
        assert row.get("measured_on"), (
            f"published figure {key!r} carries no measurement date: {row}"
        )


def test_success_rate_claim_holds_a_single_value(anon_client):
    """The success rate is one stored row with one value, not two typed numbers."""
    response = anon_client.get("/claims/published")
    assert response.status_code == 200, (
        f"GET /api/claims/published returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    rows = [row for row in items(response.json()) if row.get("key") == "success_rate"]
    assert len(rows) == 1, (
        f"the success rate appears as {len(rows)} stored rows; one metric is one row"
    )
    assert SUCCESS_RATE_VALUE in flatten(rows[0]), (
        f"the stored success rate is not the published {SUCCESS_RATE_VALUE}: {rows[0]}"
    )


def test_converter_pair_count_matches_its_matrix(anon_client):
    """The converter's advertised pair count equals its supported matrix length."""
    response = httpx.get(f"{app_url()}/3d-tools/file-converter", timeout=30.0)
    assert response.status_code == 200, (
        f"GET /3d-tools/file-converter returned {response.status_code}"
    )
    assert str(CONVERTER_PAIR_COUNT) in response.text, (
        f"the converter route does not print its pinned supported pair count of "
        f"{CONVERTER_PAIR_COUNT}"
    )


def test_unknown_address_answers_not_found(anon_client):
    """An unknown address answers not found rather than rendering something else."""
    response = httpx.get(
        f"{app_url()}/no-such-route-a1b2c3", timeout=30.0, follow_redirects=False
    )
    assert response.status_code == 404, (
        f"an unknown address returned {response.status_code}, expected 404"
    )


def test_privacy_page_is_reachable(anon_client):
    """The privacy page is served and is reachable."""
    response = httpx.get(f"{app_url()}/privacy", timeout=30.0)
    assert response.status_code == 200, (
        f"GET /privacy returned {response.status_code}"
    )


def test_foreign_creator_reading_an_asset_is_refused(creator_client, creator2_client):
    """A second creator is refused an asset owned by the first, at the API."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    response = creator2_client.get(f"/assets/{asset_id}")
    assert response.status_code == 404, (
        f"{CREATOR2_EMAIL} reading asset {asset_id} owned by {CREATOR_EMAIL} returned "
        f"{response.status_code}, expected 404 so the asset's existence stays "
        f"undisclosed: {response.text[:400]}"
    )


def test_anonymous_request_for_an_asset_is_refused(creator_client, anon_client):
    """An unauthenticated request for an owned asset is refused."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    response = anon_client.get(f"/assets/{asset_id}")
    assert response.status_code == 401, (
        f"an unauthenticated read of asset {asset_id} returned {response.status_code}, "
        f"expected 401: {response.text[:400]}"
    )


def test_foreign_asset_row_is_unchanged_after_a_refused_read(
    creator_client, creator2_client, db
):
    """A refused cross-account read leaves the asset row exactly as it was."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    before = db.rows("asset", id=asset_id)
    assert before, f"asset {asset_id} is not present in the datastore"
    creator2_client.get(f"/assets/{asset_id}")
    creator2_client.get(f"/assets/{asset_id}/download/glb")
    after = db.rows("asset", id=asset_id)
    assert after == before, (
        f"asset {asset_id} changed after a refused cross-account read: "
        f"{before[0]} became {after[0] if after else None}"
    )


def test_foreign_creator_patching_an_asset_is_refused(creator_client, creator2_client, db):
    """A second creator cannot rename an asset belonging to the first."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    response = creator2_client.patch(
        f"/assets/{asset_id}", json={"title": "taken-by-another-account"}
    )
    assert response.status_code == 404, (
        f"{CREATOR2_EMAIL} patching asset {asset_id} returned {response.status_code}, "
        f"expected 404: {response.text[:400]}"
    )
    rows = db.rows("asset", id=asset_id)
    assert rows and "taken-by-another-account" not in flatten(rows[0]), (
        f"the refused patch still reached the stored row: {rows[0] if rows else None}"
    )


def test_credit_ledger_rows_are_append_only(creator_client, db):
    """Ledger rows are inserted and never rewritten, so history stays readable."""
    before = db.rows("credit_ledger", account_email=CREATOR_EMAIL)
    if not before:
        before = db.rows("credit_ledger")
    completed_asset(creator_client, tier="standard")
    settle()
    after = db.rows("credit_ledger", account_email=CREATOR_EMAIL)
    if not after:
        after = db.rows("credit_ledger")
    assert len(after) > len(before), (
        f"the ledger holds {len(after)} rows after a generation and {len(before)} "
        f"before; a settled job writes history rather than editing it"
    )
    kept = {str(row.get("id")) for row in before}
    still = {str(row.get("id")) for row in after}
    assert kept <= still, (
        f"ledger rows disappeared across a generation: {sorted(kept - still)[:5]}"
    )


def test_balance_equals_the_sum_of_ledger_amounts(creator_client, db):
    """The readable balance is the sum of the account's ledger amounts."""
    completed_asset(creator_client, tier="standard")
    settle()
    rows = db.rows("credit_ledger", account_email=CREATOR_EMAIL)
    assert rows, (
        f"{CREATOR_EMAIL} has no credit_ledger rows after a settled generation"
    )
    total = sum(int(row.get("amount") or 0) for row in rows)
    assert balance_of(creator_client) == total, (
        f"GET /api/session reports {balance_of(creator_client)} credits while the "
        f"ledger sums to {total}"
    )


def test_failed_job_returns_the_reservation_in_full(creator_client, db):
    """A job that ends failed leaves the balance exactly as it found it."""
    before = balance_of(creator_client)
    response = submit_job(creator_client, tier="standard", source_mode="force-failure")
    if response.status_code not in (200, 201, 202):
        assert balance_of(creator_client) == before, (
            f"a refused submission moved the balance from {before} to "
            f"{balance_of(creator_client)}; nothing is reserved on a refusal"
        )
        return
    job_id = response.json().get("id") or response.json().get("job_id")

    def read():
        got = creator_client.get(f"/jobs/{job_id}")
        return got.json() if got.status_code == 200 else None

    final = wait_for_job_state(read, {"completed", "failed"})
    assert final is not None and final.get("state") == "failed", (
        f"job {job_id} was expected to fail, last state was "
        f"{final.get('state') if final else None!r}"
    )
    settle()
    assert balance_of(creator_client) == before, (
        f"a failed job left the balance at {balance_of(creator_client)} against "
        f"{before} before it started; a failed job costs nothing"
    )


def test_licence_survives_a_plan_upgrade(creator2_client, db):
    """An asset made on the free plan stays openly licensed after an upgrade."""
    job_id, asset_id = completed_asset(creator2_client, tier="standard")
    before = creator2_client.get(f"/assets/{asset_id}")
    assert before.status_code == 200, (
        f"GET /api/assets/{asset_id} returned {before.status_code}: {before.text[:400]}"
    )
    stamped = before.json().get("licence") or before.json().get("license")
    assert stamped == "CC-BY-4.0", (
        f"an asset made on the free plan carries licence {stamped!r}, expected "
        f"CC-BY-4.0"
    )
    creator2_client.patch("/session", json={"plan": "pro"})
    settle()
    after = creator2_client.get(f"/assets/{asset_id}")
    assert after.status_code == 200, (
        f"GET /api/assets/{asset_id} after the upgrade returned {after.status_code}"
    )
    now = after.json().get("licence") or after.json().get("license")
    assert now == "CC-BY-4.0", (
        f"asset {asset_id} was relicensed to {now!r} by an upgrade; a grant already "
        f"made cannot be withdrawn"
    )
    creator2_client.patch("/session", json={"plan": "free"})


def test_deletion_date_survives_a_downgrade(creator_client, db):
    """A deletion date set at creation is not shortened by a later downgrade."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    before = creator_client.get(f"/assets/{asset_id}")
    assert before.status_code == 200, (
        f"GET /api/assets/{asset_id} returned {before.status_code}"
    )
    stamped = before.json().get("deletion_date")
    assert stamped, f"asset {asset_id} carries no deletion date: {before.text[:400]}"
    creator_client.patch("/session", json={"plan": "free"})
    settle()
    after = creator_client.get(f"/assets/{asset_id}")
    assert after.status_code == 200, (
        f"GET /api/assets/{asset_id} after the downgrade returned {after.status_code}"
    )
    assert after.json().get("deletion_date") == stamped, (
        f"asset {asset_id} moved its deletion date from {stamped!r} to "
        f"{after.json().get('deletion_date')!r} on a downgrade"
    )
    creator_client.patch("/session", json={"plan": "pro"})


def test_archiving_leaves_the_deletion_date_unchanged(creator_client):
    """Archiving takes an asset out of the default view without pausing the clock."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    before = creator_client.get(f"/assets/{asset_id}")
    stamped = before.json().get("deletion_date")
    assert stamped, f"asset {asset_id} carries no deletion date"
    patched = creator_client.patch(f"/assets/{asset_id}", json={"archived": True})
    assert patched.status_code in (200, 204), (
        f"archiving asset {asset_id} returned {patched.status_code}: "
        f"{patched.text[:400]}"
    )
    after = creator_client.get(f"/assets/{asset_id}")
    assert after.json().get("deletion_date") == stamped, (
        f"archiving moved the deletion date of {asset_id} from {stamped!r} to "
        f"{after.json().get('deletion_date')!r}"
    )
    listed = creator_client.get("/assets")
    assert listed.status_code == 200, (
        f"GET /api/assets returned {listed.status_code}: {listed.text[:400]}"
    )
    ids = {str(row.get("id")) for row in items(listed.json())}
    assert str(asset_id) not in ids, (
        f"archived asset {asset_id} is still in the default library view"
    )


def test_queue_placement_is_recorded_at_submission(creator_client, db):
    """A job records the queue placement of the plan held when it was submitted."""
    response = submit_job(creator_client, tier="standard")
    assert response.status_code in (200, 201, 202), (
        f"POST /api/jobs returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    job_id = body.get("id") or body.get("job_id")
    placement = body.get("queue_priority") or body.get("queue_placement")
    assert placement == PLAN_QUEUE["pro"], (
        f"job {job_id} recorded queue placement {placement!r}, expected "
        f"{PLAN_QUEUE['pro']!r} for the pro plan"
    )


def test_monthly_grant_is_idempotent_within_a_period(creator_client, db):
    """Running the monthly grant twice for one period grants once."""
    rows = db.rows("credit_ledger", kind="monthly")
    periods = [str(row.get("period_start")) for row in rows]
    assert len(periods) == len(set(periods)) or not periods, (
        f"the monthly ledger carries a repeated period: "
        f"{sorted(p for p in periods if periods.count(p) > 1)[:4]}"
    )


def test_job_records_its_octree_and_inference_parameters(creator_client):
    """A job records the resolution and step count that produced its result."""
    job_id, asset_id = completed_asset(creator_client, tier="pro")
    response = creator_client.get(f"/jobs/{job_id}")
    assert response.status_code == 200, (
        f"GET /api/jobs/{job_id} returned {response.status_code}"
    )
    blob = flatten(response.json())
    assert str(TIERS["pro"]["octree"]) in blob, (
        f"job {job_id} does not record the pro tier octree resolution "
        f"{TIERS['pro']['octree']}: {response.text[:600]}"
    )
    assert str(TIERS["pro"]["steps"]) in blob, (
        f"job {job_id} does not record the pro tier inference step count "
        f"{TIERS['pro']['steps']}: {response.text[:600]}"
    )


def test_library_filters_compose(creator_client):
    """Status, tag and favourite filters apply together rather than one at a time."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    creator_client.post(f"/assets/{asset_id}/tags", json={"tag": "grader-prop"})
    creator_client.patch(f"/assets/{asset_id}", json={"favourite": True})
    response = creator_client.get(
        "/assets",
        params={"status": "completed", "tag": "grader-prop", "favourite": "true"},
    )
    assert response.status_code == 200, (
        f"GET /api/assets with three filters returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    rows = items(response.json())
    assert rows, "the composed filter returned nothing, though one asset satisfies all three"
    for row in rows:
        assert row.get("favourite") is True, (
            f"asset {row.get('id')} is in a favourite-filtered result without the flag: {row}"
        )
        assert "grader-prop" in flatten(row), (
            f"asset {row.get('id')} is in a tag-filtered result without the tag: {row}"
        )


def test_two_simultaneous_submissions_leave_one_accepted(creator3_client, db):
    """Two jobs against a balance with room for one leave one accepted, one refused."""
    before = balance_of(creator3_client)
    cost = expected_cost("standard")
    assert before < 2 * cost, (
        f"{CREATOR3_EMAIL} holds {before} credits, which is room for more than one "
        f"{cost}-credit job; the contended case cannot be observed"
    )
    first = submit_job(creator3_client, tier="standard")
    second = submit_job(creator3_client, tier="standard")
    codes = sorted([first.status_code, second.status_code])
    accepted = [r for r in (first, second) if r.status_code in (200, 201, 202)]
    refused = [r for r in (first, second) if r.status_code == 402]
    assert len(accepted) == 1 and len(refused) == 1, (
        f"two simultaneous submissions against a balance of {before} returned "
        f"{codes}; exactly one must be accepted and one refused with 402"
    )
    settle()
    assert balance_of(creator3_client) >= 0, (
        f"the balance fell to {balance_of(creator3_client)} after the contended pair"
    )


def test_balance_never_falls_below_zero(creator3_client, db):
    """No readable ledger row leaves a balance below zero."""
    rows = db.rows("credit_ledger")
    negatives = [row for row in rows if int(row.get("balance_after") or 0) < 0]
    assert not negatives, (
        f"{len(negatives)} ledger row(s) record a balance below zero, the first being "
        f"{negatives[0]}"
    )


def test_repeated_idempotency_key_returns_the_existing_job(creator_client):
    """A resubmission on an existing key yields one job and spends one reservation."""
    key = unique_key()
    before = balance_of(creator_client)
    first = submit_job(creator_client, tier="standard", idempotency_key=key)
    assert first.status_code in (200, 201, 202), (
        f"POST /api/jobs returned {first.status_code}: {first.text[:400]}"
    )
    first_id = first.json().get("id") or first.json().get("job_id")
    second = submit_job(creator_client, tier="standard", idempotency_key=key)
    assert second.status_code in (200, 201, 202, 409), (
        f"a resubmission on key {key} returned {second.status_code}: "
        f"{second.text[:400]}"
    )
    if second.status_code != 409:
        second_id = second.json().get("id") or second.json().get("job_id")
        assert second_id == first_id, (
            f"a resubmission on key {key} created job {second_id} beside {first_id}"
        )

    def read():
        got = creator_client.get(f"/jobs/{first_id}")
        return got.json() if got.status_code == 200 else None

    wait_for_job_state(read, {"completed", "failed"})
    settle()
    spent = before - balance_of(creator_client)
    assert spent == expected_cost("standard"), (
        f"a retried submission spent {spent} credits, expected one charge of "
        f"{expected_cost('standard')}"
    )


def test_submission_over_balance_is_refused(creator3_client):
    """A submission costing more than the balance is refused and reserves nothing."""
    before = balance_of(creator3_client)
    response = submit_job(creator3_client, tier="ultra", textures=True)
    assert response.status_code in (402, 403, 422), (
        f"a submission costing {expected_cost('ultra', textures=True)} against a "
        f"balance of {before} returned {response.status_code}, expected a refusal: "
        f"{response.text[:400]}"
    )
    assert balance_of(creator3_client) == before, (
        f"a refused submission moved the balance from {before} to "
        f"{balance_of(creator3_client)}"
    )


def test_second_anonymous_generation_is_refused(anon_client):
    """A visitor gets one anonymous model and the second attempt is refused by name."""
    with client() as fresh:
        first = submit_job(fresh, tier="standard", sample=SAMPLE_KEYS[0])
        assert first.status_code in (200, 201, 202), (
            f"the first anonymous generation returned {first.status_code}, but the "
            f"allowance is {ANONYMOUS_ALLOWANCE}: {first.text[:400]}"
        )
        second = submit_job(fresh, tier="standard", sample=SAMPLE_KEYS[1])
        assert second.status_code == 429, (
            f"a second anonymous generation returned {second.status_code}, expected "
            f"429: {second.text[:400]}"
        )
        assert second.text.strip(), (
            "the refusal carries no message, so the visitor is shown a generic failure"
        )


def test_expired_claim_token_is_refused(anon_client):
    """A claim token presented after its window is refused."""
    response = anon_client.post(
        "/claims", json={"claim_token": "expired-token-000000000000000000000000"}
    )
    assert response.status_code in (404, 410), (
        f"an unknown or expired claim token returned {response.status_code}, expected "
        f"410 after a {CLAIM_WINDOW_HOURS}-hour window: {response.text[:400]}"
    )


def test_rejected_source_format_is_not_stored(creator_client, db):
    """A source format outside the accepted set is refused and nothing is written."""
    before = len(db.rows("job"))
    response = creator_client.post(
        "/jobs",
        json={
            "source_mode": "image-to-3d",
            "input_mode": "single-image",
            "tier": "standard",
            "textures": False,
            "source_format": "GIF",
            "idempotency_key": unique_key(),
        },
    )
    assert response.status_code in (400, 415, 422), (
        f"a GIF source returned {response.status_code}, expected a refusal naming the "
        f"format; accepted formats are {ACCEPTED_SOURCE_FORMATS}: {response.text[:400]}"
    )
    assert "gif" in response.text.lower(), (
        f"the refusal does not name the format it found: {response.text[:400]}"
    )
    settle()
    assert len(db.rows("job")) == before, (
        f"a refused source format still wrote a job row: {before} rows became "
        f"{len(db.rows('job'))}"
    )


def test_tier_outside_the_closed_set_is_refused(creator_client, db):
    """A tier outside the four stored keys is refused rather than stored."""
    before = len(db.rows("job"))
    response = submit_job(creator_client, tier="hyper")
    assert response.status_code == 422, (
        f"the tier 'hyper' returned {response.status_code}, expected 422; the stored "
        f"keys are {sorted(TIERS)}: {response.text[:400]}"
    )
    settle()
    assert len(db.rows("job")) == before, (
        f"a refused tier still wrote a job row: {before} became {len(db.rows('job'))}"
    )


def test_licence_change_request_is_refused(creator_client, db):
    """A request to rewrite a stored licence is refused and the row is untouched."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    before = creator_client.get(f"/assets/{asset_id}").json()
    stamped = before.get("licence") or before.get("license")
    response = creator_client.patch(
        f"/assets/{asset_id}", json={"licence": "customer-owned-by-request"}
    )
    assert response.status_code in (400, 409, 422), (
        f"a licence rewrite returned {response.status_code}, expected a refusal: "
        f"{response.text[:400]}"
    )
    after = creator_client.get(f"/assets/{asset_id}").json()
    assert (after.get("licence") or after.get("license")) == stamped, (
        f"the licence of {asset_id} moved from {stamped!r} to "
        f"{after.get('licence') or after.get('license')!r}"
    )


def test_decoy_field_submission_is_refused(anon_client, db):
    """A form filling the unattended decoy field is refused and writes nothing."""
    before = len(db.rows("contact_message"))
    response = anon_client.post(
        "/contact",
        json={
            "name": "Grader Probe",
            "email": CREATOR3_EMAIL,
            "body": "a message from an automated client",
            "website": "https://filled-by-a-bot.example",
        },
    )
    assert response.status_code == 429, (
        f"a submission filling the decoy field returned {response.status_code}, "
        f"expected 429: {response.text[:400]}"
    )
    settle()
    assert len(db.rows("contact_message")) == before, (
        f"a refused automated submission still wrote a row: {before} became "
        f"{len(db.rows('contact_message'))}"
    )


def test_completed_job_writes_its_glb_object_to_the_bucket(creator_client, db, store):
    """A completed generation leaves its glb object in the object store bucket."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    settle()
    rows = db.rows("asset_representation", asset_id=asset_id, kind="glb")
    assert rows, (
        f"asset {asset_id} from job {job_id} records no glb representation row"
    )
    key = rows[0].get("object_key")
    assert key, f"the glb representation of {asset_id} records no object key: {rows[0]}"
    assert store.exists(key), (
        f"the glb object {key!r} for asset {asset_id} is not in the bucket; the row "
        f"claims an upload that did not happen"
    )


def test_completed_job_writes_its_obj_and_stl_objects_to_the_bucket(
    creator_client, db, store
):
    """The obj and stl representations are real objects in the bucket, not rows alone."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    settle()
    for kind in ("obj", "stl"):
        rows = db.rows("asset_representation", asset_id=asset_id, kind=kind)
        assert rows, f"asset {asset_id} records no {kind} representation row"
        key = rows[0].get("object_key")
        assert key and store.exists(key), (
            f"the {kind} object {key!r} for asset {asset_id} is not in the bucket"
        )


def test_bucket_is_not_publicly_readable(creator_client, db, store):
    """An object in the bucket is not readable by an unauthenticated direct request."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    settle()
    rows = db.rows("asset_representation", asset_id=asset_id, kind="glb")
    assert rows and rows[0].get("object_key"), (
        f"asset {asset_id} records no glb object key to probe"
    )
    key = rows[0]["object_key"]
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    bucket = os.environ["STORAGE_BUCKET"]
    probe = httpx.get(f"{endpoint}/{bucket}/{key}", timeout=30.0)
    assert probe.status_code in (401, 403, 404), (
        f"the object {key!r} answered {probe.status_code} to an unauthenticated "
        f"request straight at the bucket; a private asset must not be world-readable"
    )


def test_foreign_creator_download_of_an_object_is_refused(
    creator_client, creator2_client, anon_client
):
    """A second creator and an anonymous caller are both refused a stored object."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    foreign = creator2_client.get(f"/assets/{asset_id}/download/glb")
    assert foreign.status_code == 404, (
        f"{CREATOR2_EMAIL} downloading the object behind asset {asset_id} returned "
        f"{foreign.status_code}, expected 404: {foreign.text[:400]}"
    )
    stranger = anon_client.get(f"/assets/{asset_id}/download/glb")
    assert stranger.status_code == 401, (
        f"an unauthenticated download of the object behind asset {asset_id} returned "
        f"{stranger.status_code}, expected 401: {stranger.text[:400]}"
    )


def test_second_download_creates_no_second_asset(creator_client, db):
    """Downloading a second representation spends no credit and adds no asset."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    settle()
    assets_before = len(db.rows("asset"))
    balance_before = balance_of(creator_client)
    for kind in ("glb", "stl"):
        got = creator_client.get(f"/assets/{asset_id}/download/{kind}")
        assert got.status_code in (200, 302), (
            f"the owner downloading {kind} of asset {asset_id} returned "
            f"{got.status_code}: {got.text[:200]}"
        )
    settle()
    assert len(db.rows("asset")) == assets_before, (
        f"downloading two representations created {len(db.rows('asset')) - assets_before} "
        f"further asset row(s)"
    )
    assert balance_of(creator_client) == balance_before, (
        f"downloading two representations moved the balance from {balance_before} to "
        f"{balance_of(creator_client)}; a download is not a generation"
    )


def test_download_events_are_recorded_per_representation(creator_client, db):
    """Each download of an asset is recorded against it with its representation."""
    job_id, asset_id = completed_asset(creator_client, tier="standard")
    settle()
    before = len(db.rows("download_event", asset_id=asset_id))
    for kind in ("glb", "obj"):
        creator_client.get(f"/assets/{asset_id}/download/{kind}")
    settle()
    rows = db.rows("download_event", asset_id=asset_id)
    assert len(rows) - before == 2, (
        f"two downloads of asset {asset_id} recorded {len(rows) - before} event(s), "
        f"expected 2"
    )
    kinds = {row.get("representation_kind") or row.get("kind") for row in rows}
    assert {"glb", "obj"} <= kinds, (
        f"the recorded downloads of asset {asset_id} do not name both representations: "
        f"{sorted(k for k in kinds if k)}"
    )
