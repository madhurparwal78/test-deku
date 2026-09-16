"""Observations over the deployed Geoform platform.

Every assertion here reads the app over HTTP, the PostgreSQL database behind it
or the MinIO bucket beside it. Nothing reads the source the agent wrote.
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


def test_signup_creates_an_author_account():
    probe = f"probe-{os.urandom(6).hex()}@example.com"
    made = httpx.post(f"{appclient.api_base()}/auth/signup",
                      json={"email": probe, "password": conftest.PASSWORD},
                      timeout=conftest.TIMEOUT)
    assert made.status_code in (200, 201), (
        f"open sign-up for {probe} returned {made.status_code}: {made.text[:300]}"
    )
    token = appclient.login(probe, conftest.PASSWORD)
    assert token, f"the account created for {probe} cannot sign in"


def test_every_seeded_account_signs_in():
    for email in conftest.SEEDED_ACCOUNTS:
        assert appclient.login(email, conftest.PASSWORD), (
            f"the seeded account {email} returned no bearer token"
        )


def test_token_secret_is_shown_once_only():
    author = conftest.session(conftest.AUTHOR_ONE)
    made = author.post("/tokens", json={"name": conftest.unique("probe"), "scopes": ["tiles:read"]})
    assert made.status_code in (200, 201), (
        f"POST /api/tokens returned {made.status_code}: {made.text[:300]}"
    )
    secret = made.json().get("secret")
    assert secret, f"a newly created token returned no secret: {made.json()}"
    listed = _shapes.items(author.get("/tokens").json())
    assert listed, "a created token is absent from the token list"
    flat = _shapes.flatten(listed)
    assert secret not in flat, (
        "the token secret is readable again from the token list; it is shown once only"
    )


def test_public_routes_are_served_with_their_pinned_copy():
    missing = []
    for route, strings in conftest.PINNED_COPY.items():
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=conftest.TIMEOUT,
                         follow_redirects=True)
        assert page.status_code == 200, (
            f"GET {route} returned {page.status_code}, expected a served public page"
        )
        for pinned in strings:
            if pinned not in page.text:
                missing.append((route, pinned))
    assert not missing, f"pinned copy is absent from the served pages: {missing[:8]}"


def test_marketing_pages_render_without_the_map_client():
    for route in conftest.MARKETING_ROUTES:
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=conftest.TIMEOUT,
                         follow_redirects=True)
        body = page.text
        assert len(conftest.visible_text(body)) > conftest.MIN_PRERENDERED_CHARS, (
            f"{route} carries only {len(conftest.visible_text(body))} characters of markup; a "
            f"pre-rendered marketing route must serve its copy in the first response"
        )


def test_security_headers_are_present_on_every_response():
    missing = []
    for route in conftest.MARKETING_ROUTES:
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=conftest.TIMEOUT,
                         follow_redirects=True)
        headers = {k.lower(): v for k, v in page.headers.items()}
        if "strict-transport-security" not in headers:
            missing.append((route, "strict-transport-security"))
        if headers.get("x-content-type-options", "").lower() != "nosniff":
            missing.append((route, "x-content-type-options: nosniff"))
    assert not missing, f"security headers are absent: {missing[:6]}"


def test_sitemap_lists_every_public_route():
    sitemap = httpx.get(f"{appclient.app_url()}/sitemap.xml", timeout=conftest.TIMEOUT)
    assert sitemap.status_code == 200, (
        f"GET /sitemap.xml returned {sitemap.status_code}, expected a served sitemap"
    )
    absent = [r for r in conftest.MARKETING_ROUTES if r not in sitemap.text]
    assert not absent, f"the sitemap omits public routes: {absent}"
    robots = httpx.get(f"{appclient.app_url()}/robots.txt", timeout=conftest.TIMEOUT)
    assert robots.status_code == 200, (
        f"GET /robots.txt returned {robots.status_code}"
    )
    assert "sitemap" in robots.text.lower(), (
        f"robots.txt does not name the sitemap: {robots.text[:200]}"
    )


def test_upload_job_state_is_observable():
    author = conftest.session(conftest.AUTHOR_ONE)
    made = author.post("/uploads", json={"name": conftest.unique("parcels") + ".geojson",
                                         "content": conftest.SAMPLE_DATASET})
    upload_id = made.json().get("id")
    assert made.json().get("state") in conftest.UPLOAD_STATES, (
        f"a new upload reports state {made.json().get('state')!r}, expected one of "
        f"{list(conftest.UPLOAD_STATES)}"
    )
    final = conftest.wait_for_upload(author, upload_id, conftest.TERMINAL_STATES)
    assert final == "complete", (
        f"the upload finished in state {final!r}, expected complete"
    )


def test_style_publish_is_readable_by_reference():
    owner = conftest.session(conftest.AUTHOR_ONE)
    project = conftest.seeded_project(owner)
    versions = _shapes.items(owner.get(f"/projects/{project['id']}/versions").json())
    assert versions, "the seeded project carries no style version"
    published = owner.post(f"/projects/{project['id']}/publish",
                           json={"version": versions[-1].get("version")})
    assert published.status_code in (200, 201), (
        f"publishing returned {published.status_code}: {published.text[:300]}"
    )
    style_id = published.json().get("style") or project.get("style")
    anonymous = httpx.Client(base_url=appclient.api_base(), timeout=conftest.TIMEOUT)
    read = anonymous.get(f"/styles/{style_id}")
    assert read.status_code == 200, (
        f"a published style is not readable without a session: {read.status_code}"
    )
    body = read.json()
    for key in ("sources", "layers"):
        assert key in body, f"the published style document carries no {key}: {list(body)}"


def test_style_document_carries_expressions_and_layer_kinds():
    owner = conftest.session(conftest.AUTHOR_ONE)
    project = conftest.seeded_project(owner)
    style = owner.get(f"/projects/{project['id']}").json().get("style_document") or {}
    layers = style.get("layers") or []
    assert layers, f"the seeded style carries no layers: {list(style)}"
    kinds = {str(layer.get("type")) for layer in layers}
    assert kinds & set(conftest.LAYER_KINDS), (
        f"no layer carries one of the named kinds {sorted(conftest.LAYER_KINDS)}; found {kinds}"
    )
    flat = _shapes.flatten(style)
    assert "interpolate" in flat or "step" in flat or "case" in flat, (
        "no paint or layout value is an expression; a constant-only style cannot key off a "
        "feature attribute or the zoom"
    )


def test_directions_return_geometry_distance_and_maneuvers():
    author = conftest.session(conftest.AUTHOR_ONE)
    response = author.get("/directions/driving", params={"waypoints": conftest.WAYPOINTS})
    assert response.status_code == 200, (
        f"GET /api/directions/driving returned {response.status_code}: {response.text[:300]}"
    )
    route = response.json()
    for field in ("geometry", "distance", "duration", "maneuvers"):
        assert field in route, f"the route carries no {field}: {list(route)}"
    assert route["maneuvers"], "the route carries no maneuvers"
    for step in route["maneuvers"]:
        assert step.get("instruction"), f"a maneuver carries no instruction: {step}"


def test_traffic_profile_differs_from_plain_driving():
    author = conftest.session(conftest.AUTHOR_ONE)
    plain = author.get("/directions/driving", params={"waypoints": conftest.WAYPOINTS})
    aware = author.get("/directions/driving-traffic", params={"waypoints": conftest.WAYPOINTS})
    assert aware.status_code == 200, (
        f"the traffic-aware profile returned {aware.status_code}: {aware.text[:300]}"
    )
    assert aware.json().get("duration") != plain.json().get("duration"), (
        "the traffic-aware profile returned the same duration as plain driving over a seeded "
        "table that carries current speeds differing from base speeds"
    )


def test_isochrone_returns_nested_valid_polygons():
    author = conftest.session(conftest.AUTHOR_ONE)
    response = author.get("/isochrone", params={"origin": conftest.ORIGIN,
                                                "budgets": conftest.BUDGETS})
    assert response.status_code == 200, (
        f"GET /api/isochrone returned {response.status_code}: {response.text[:300]}"
    )
    polygons = _shapes.items(response.json())
    assert len(polygons) == len(conftest.BUDGETS.split(",")), (
        f"asked for {len(conftest.BUDGETS.split(','))} budgets, received {len(polygons)} polygons"
    )
    areas = [conftest.ring_area(p) for p in polygons]
    assert areas == sorted(areas), (
        f"a larger budget did not enclose a smaller one: areas {areas}"
    )


def test_geocoding_types_and_reverse_lookup():
    author = conftest.session(conftest.AUTHOR_ONE)
    forward = author.get("/geocode", params={"q": conftest.PLACE_QUERY})
    assert forward.status_code == 200, (
        f"GET /api/geocode returned {forward.status_code}: {forward.text[:300]}"
    )
    results = _shapes.items(forward.json())
    assert results, f"no geocoding result for {conftest.PLACE_QUERY!r}"
    for row in results:
        assert row.get("type") in conftest.PLACE_TYPES, (
            f"a result carries the type {row.get('type')!r}, expected one of "
            f"{list(conftest.PLACE_TYPES)}"
        )
    reverse = author.get("/reverse", params={"lon": conftest.LON, "lat": conftest.LAT})
    assert reverse.status_code == 200, (
        f"GET /api/reverse returned {reverse.status_code}: {reverse.text[:300]}"
    )


def test_search_ranks_a_nearby_match_first():
    author = conftest.session(conftest.AUTHOR_ONE)
    response = author.get("/search", params={"q": conftest.SEARCH_PREFIX,
                                             "proximity": conftest.ORIGIN})
    assert response.status_code == 200, (
        f"GET /api/search returned {response.status_code}: {response.text[:300]}"
    )
    results = _shapes.items(response.json())
    assert results, f"no suggestion for the prefix {conftest.SEARCH_PREFIX!r}"
    assert str(results[0].get("name", "")).startswith(conftest.NEAR_PLACE[:4]), (
        f"the first suggestion is {results[0].get('name')!r}; the nearby match "
        f"{conftest.NEAR_PLACE!r} must outrank a distant better textual match"
    )


def test_guidance_snaps_and_reroutes():
    author = conftest.session(conftest.AUTHOR_ONE)
    started = author.post("/guidance", json={"waypoints": conftest.WAYPOINTS})
    if started.status_code not in (200, 201):
        assert started.status_code in (400, 404), (
            f"POST /api/guidance returned {started.status_code}: {started.text[:200]}"
        )
        return
    session_id = started.json().get("id")
    on_route = author.post(f"/guidance/{session_id}/position",
                           json={"lon": conftest.LON, "lat": conftest.LAT})
    assert on_route.json().get("snapped_segment"), (
        f"a position update returned no snapped segment: {on_route.json()}"
    )
    assert on_route.json().get("next_maneuver"), (
        "a position update returned no next maneuver"
    )
    off = author.post(f"/guidance/{session_id}/position", json=conftest.OFF_ROUTE)
    assert off.json().get("rerouted") is True, (
        f"leaving the route did not produce a new route: {off.json()}"
    )


def test_boundaries_are_joinable_by_key():
    author = conftest.session(conftest.AUTHOR_ONE)
    response = author.get("/boundaries", params={"kind": "region"})
    assert response.status_code == 200, (
        f"GET /api/boundaries returned {response.status_code}: {response.text[:300]}"
    )
    rows = _shapes.items(response.json())
    assert rows, "no boundary rows over the seeded region"
    for row in rows:
        assert row.get("key"), f"a boundary row carries no shared geographic key: {row}"


def test_app_contract_paths_exist_in_the_image():
    readme = pathlib.Path("/app/USER_README.md")
    assert readme.is_file(), "/app/USER_README.md is absent"
    text = readme.read_text(encoding="utf-8", errors="replace")
    for email in conftest.SEEDED_ACCOUNTS:
        assert email in text, f"/app/USER_README.md does not name {email}"
    assert conftest.PASSWORD in text, "/app/USER_README.md does not carry the seeded password"
    for name in (".browser_screenshots", ".downloads"):
        directory = pathlib.Path("/app") / name
        assert directory.is_dir(), f"/app/{name} is absent"
        assert not any(directory.iterdir()), f"/app/{name} is not empty"


def test_no_binary_asset_is_served():
    offenders = []
    for route in conftest.MARKETING_ROUTES:
        page = httpx.get(f"{appclient.app_url()}{route}", timeout=conftest.TIMEOUT,
                         follow_redirects=True)
        for reference in conftest.asset_refs(page.text):
            if reference.lower().endswith(conftest.BINARY_SUFFIXES):
                offenders.append((route, reference))
    assert not offenders, (
        f"the build references binary assets, which it must produce in code instead: "
        f"{offenders[:6]}"
    )


def test_list_endpoints_return_top_level_arrays():
    author = conftest.session(conftest.AUTHOR_ONE)
    for route in ("/tokens", "/tilesets", "/projects"):
        payload = author.get(route).json()
        assert isinstance(payload, list) or _shapes.items(payload), (
            f"GET /api{route} returned {type(payload).__name__}, expected a top-level JSON array"
        )


def test_login_with_wrong_password_is_denied():
    response = httpx.post(f"{appclient.api_base()}/auth/login",
                          json={"email": conftest.AUTHOR_ONE, "password": "not-the-password"},
                          timeout=conftest.TIMEOUT)
    assert response.status_code in (400, 401, 403), (
        f"a wrong password returned {response.status_code}, expected a denial"
    )
    body = _shapes.flatten(response.text)
    assert "no such" not in body and "not registered" not in body, (
        f"the denial discloses whether the address exists: {response.text[:300]}"
    )


def test_revoked_token_is_refused_and_others_keep_working():
    author = conftest.session(conftest.AUTHOR_ONE)
    first = author.post("/tokens", json={"name": conftest.unique("keep"), "scopes": ["tiles:read"]})
    second = author.post("/tokens", json={"name": conftest.unique("drop"), "scopes": ["tiles:read"]})
    kept, dropped = first.json(), second.json()
    author.delete(f"/tokens/{dropped.get('id')}")
    refused = conftest.keyed(dropped["secret"]).get("/tilesets")
    assert refused.status_code in (401, 403), (
        f"a revoked token still reads: GET /api/tilesets returned {refused.status_code}"
    )
    still = conftest.keyed(kept["secret"]).get("/tilesets")
    assert still.status_code == 200, (
        f"revoking one token broke another: GET /api/tilesets returned {still.status_code}"
    )


def test_token_scope_is_enforced():
    author = conftest.session(conftest.AUTHOR_ONE)
    made = author.post("/tokens", json={"name": conftest.unique("tiles"), "scopes": ["tiles:read"]})
    secret = made.json().get("secret")
    response = conftest.keyed(secret).get("/directions/driving",
                                          params={"waypoints": conftest.WAYPOINTS})
    assert response.status_code in (401, 403), (
        f"a tiles-scoped token reached the directions service: {response.status_code}"
    )
    assert "scope" in _shapes.flatten(response.text), (
        f"the refusal does not name the missing scope: {response.text[:300]}"
    )


def test_private_tileset_is_unreadable_until_published():
    owner = conftest.session(conftest.AUTHOR_ONE)
    tileset = conftest.seeded_private_tileset(owner)
    address = f"/tiles/{tileset['id']}/0/0/0"
    anonymous = httpx.Client(base_url=appclient.api_base(), timeout=conftest.TIMEOUT)
    assert anonymous.get(address).status_code == 404, (
        f"a private tile answered a request carrying no token as something other than not found"
    )
    other = conftest.session(conftest.AUTHOR_TWO)
    assert other.get(address).status_code == 404, (
        f"a private tile answered {conftest.AUTHOR_TWO} as something other than not found; a "
        f"hidden tileset must not be confirmed to exist"
    )
    assert owner.get(address).status_code == 200, (
        "the owning account cannot read its own private tile"
    )
    owner.post(f"/tilesets/{tileset['id']}/publish")
    assert anonymous.get(address).status_code == 200, (
        "publishing did not make the tile readable without a token"
    )
    owner.post(f"/tilesets/{tileset['id']}/unpublish")
    assert anonymous.get(address).status_code == 404, (
        "unpublishing did not close the tile again on the next request"
    )


def test_viewer_cannot_publish():
    owner = conftest.session(conftest.AUTHOR_ONE)
    project = conftest.seeded_project(owner)
    reader = conftest.session(conftest.READER)
    denied = reader.post(f"/projects/{project['id']}/publish", json={"version": 1})
    assert denied.status_code in (401, 403, 404), (
        f"a reader publishing returned {denied.status_code}, expected a server-side denial"
    )


def test_reader_cannot_reach_a_studio_resource():
    reader = conftest.session(conftest.READER)
    for route in ("/projects", "/tilesets", "/tokens", "/usage"):
        response = reader.get(route)
        assert response.status_code in (401, 403, 404), (
            f"GET /api{route} from a reader session returned {response.status_code}, expected a "
            f"denial: {response.text[:200]}"
        )


def test_unauthenticated_request_is_refused():
    anonymous = httpx.Client(base_url=appclient.api_base(), timeout=conftest.TIMEOUT)
    for route in ("/projects", "/tilesets", "/tokens", "/usage", "/uploads"):
        response = anonymous.get(route)
        assert response.status_code in (401, 403), (
            f"GET /api{route} without a token returned {response.status_code}"
        )


def test_private_place_is_findable_only_by_its_owner():
    owner = conftest.session(conftest.AUTHOR_ONE)
    other = conftest.session(conftest.AUTHOR_TWO)
    name = conftest.unique("Berth")
    added = owner.post("/uploads", json={"name": name + ".geojson",
                                         "content": conftest.named_dataset(name)})
    conftest.wait_for_upload(owner, added.json().get("id"), conftest.TERMINAL_STATES)
    mine = _shapes.flatten(owner.get("/search", params={"q": name}).json())
    assert name.lower() in mine, f"the owner cannot find their own added place {name!r}"
    theirs = _shapes.flatten(other.get("/search", params={"q": name}).json())
    assert name.lower() not in theirs, (
        f"{conftest.AUTHOR_TWO} found a place in another account's private dataset"
    )


def test_movement_reads_return_no_individual_trace():
    author = conftest.session(conftest.AUTHOR_ONE)
    response = author.get("/movement", params={"area": conftest.AREA})
    assert response.status_code == 200, (
        f"GET /api/movement returned {response.status_code}: {response.text[:300]}"
    )
    flat = _shapes.flatten(response.json())
    for leak in ("device_id", "trace", "individual", "user_id"):
        assert leak not in flat, (
            f"a movement read exposed {leak!r}; movement products are aggregated at rest"
        )
    rows = _shapes.items(response.json())
    assert rows, "a movement read returned nothing over the seeded area"
    for row in rows:
        assert "count" in row or "speed" in row, (
            f"a movement row carries neither a count nor a speed: {row}"
        )


def test_usage_counts_one_event_per_billable_action():
    author = conftest.session(conftest.AUTHOR_ONE)
    before = author.get("/usage").json()
    start = conftest.service_total(before, "directions")
    for _ in range(3):
        author.get("/directions/driving", params={"waypoints": conftest.WAYPOINTS})
    after = author.get("/usage").json()
    end = conftest.service_total(after, "directions")
    assert end - start == 3, (
        f"three directions calls moved the directions usage total by {end - start}, expected 3"
    )


def test_page_views_are_recorded_and_owner_only():
    author = conftest.session(conftest.AUTHOR_ONE)
    before = len(_shapes.items(author.get("/page-views").json()))
    httpx.get(f"{appclient.app_url()}/pricing", timeout=conftest.TIMEOUT,
              follow_redirects=True)
    rows = conftest.wait_for_rows(author, "/page-views", at_least=before + 1)
    assert len(rows) > before, "a public page view was not recorded"
    assert any("/pricing" in str(r.get("route", "")) for r in rows), (
        f"no recorded page view names /pricing: {rows[-3:]}"
    )
    reader = conftest.session(conftest.READER)
    denied = reader.get("/page-views")
    assert denied.status_code in (401, 403, 404), (
        f"a reader read the page-view records: {denied.status_code}"
    )


def test_identical_upload_creates_no_second_object():
    author = conftest.session(conftest.AUTHOR_ONE)
    name = conftest.unique("repeat") + ".geojson"
    first = author.post("/uploads", json={"name": name, "content": conftest.SAMPLE_DATASET})
    conftest.wait_for_upload(author, first.json().get("id"), conftest.TERMINAL_STATES)
    store = conftest.store()
    before = len(store.list("uploads/"))
    second = author.post("/uploads", json={"name": name, "content": conftest.SAMPLE_DATASET})
    conftest.settle()
    assert len(store.list("uploads/")) == before, (
        "identical bytes sent twice created a second stored object"
    )
    assert second.json().get("object_key") == first.json().get("object_key"), (
        f"the second upload landed at a different key: {second.json().get('object_key')!r} "
        f"against {first.json().get('object_key')!r}"
    )


def test_published_tileset_serves_one_stored_result():
    owner = conftest.session(conftest.AUTHOR_ONE)
    tileset = conftest.published_tileset(owner)
    address = f"/tiles/{tileset['id']}/1/0/0"
    first = owner.get(address)
    assert first.status_code == 200, (
        f"a published tile returned {first.status_code}: {first.text[:200]}"
    )
    second = httpx.Client(base_url=appclient.api_base(), timeout=conftest.TIMEOUT).get(address)
    assert second.status_code == 200, "an anonymous caller cannot read a published tile"
    assert second.content == first.content, (
        "two callers received different bytes for one tile address"
    )


def test_tile_is_produced_on_demand_and_reused():
    owner = conftest.session(conftest.AUTHOR_ONE)
    tileset = conftest.published_tileset(owner)
    cold = conftest.timed(lambda: owner.get(f"/tiles/{tileset['id']}/3/4/2"))
    warm = conftest.timed(lambda: owner.get(f"/tiles/{tileset['id']}/3/4/2"))
    assert warm <= max(cold, conftest.FLOOR_SECONDS), (
        f"a second read of one tile took {warm:.3f}s against a first read of {cold:.3f}s; a "
        f"produced tile must be served again rather than recomputed"
    )


def test_source_change_dirties_only_intersecting_tiles():
    owner = conftest.session(conftest.AUTHOR_ONE)
    tileset = conftest.published_tileset(owner)
    near, far = "/tiles/%s/6/33/22" % tileset["id"], "/tiles/%s/6/1/1" % tileset["id"]
    owner.get(near)
    owner.get(far)
    marked = owner.post(f"/tilesets/{tileset['id']}/touch",
                        json={"bounds": conftest.SMALL_BOUNDS})
    if marked.status_code not in (200, 202):
        assert marked.status_code in (400, 404), (
            f"POST touch returned {marked.status_code}: {marked.text[:200]}"
        )
        return
    dirty = _shapes.items(owner.get(f"/tilesets/{tileset['id']}/dirty").json())
    addresses = {f"{d.get('z')}/{d.get('x')}/{d.get('y')}" for d in dirty}
    assert "6/1/1" not in addresses, (
        f"a local source change marked a distant tile dirty: {sorted(addresses)[:8]}"
    )


def test_two_operations_on_different_paths_both_land():
    one = conftest.session(conftest.AUTHOR_ONE)
    two = conftest.session(conftest.AUTHOR_TWO)
    project = conftest.seeded_project(one)
    base = conftest.current_version(one, project["id"])
    first = one.post(f"/projects/{project['id']}/operations", json={
        "path": "layers.water.paint.fill-color", "before": None, "after": "#1b3b6f",
        "base_version": base})
    second = two.post(f"/projects/{project['id']}/operations", json={
        "path": "layers.road.paint.line-width", "before": None, "after": 2,
        "base_version": base})
    for who, response in ((conftest.AUTHOR_ONE, first), (conftest.AUTHOR_TWO, second)):
        assert response.status_code in (200, 201), (
            f"an operation from {who} on its own path returned {response.status_code}: "
            f"{response.text[:300]}"
        )
    history = _shapes.items(one.get(f"/projects/{project['id']}/operations").json())
    paths = {str(op.get("path")) for op in history}
    for path in ("layers.water.paint.fill-color", "layers.road.paint.line-width"):
        assert path in paths, f"the history does not carry the operation on {path}"


def test_operation_history_replays_in_order_without_repeats():
    one = conftest.session(conftest.AUTHOR_ONE)
    project = conftest.seeded_project(one)
    seen = _shapes.items(one.get(f"/projects/{project['id']}/operations").json())
    cursor = seen[-1].get("id") if seen else 0
    base = conftest.current_version(one, project["id"])
    one.post(f"/projects/{project['id']}/operations", json={
        "path": "layers.sky.paint.sky-opacity", "before": None, "after": 0.5,
        "base_version": base})
    caught = conftest.wait_for_operations(one, project["id"], after=cursor, at_least=1)
    ids = [op.get("id") for op in caught]
    assert ids == sorted(ids), f"replayed operations are out of order: {ids}"
    assert len(ids) == len(set(ids)), f"the replay repeated an operation: {ids}"


def test_version_restore_is_recorded_as_an_operation():
    owner = conftest.session(conftest.AUTHOR_ONE)
    project = conftest.seeded_project(owner)
    versions = _shapes.items(owner.get(f"/projects/{project['id']}/versions").json())
    if len(versions) < 2:
        return
    before = len(_shapes.items(owner.get(f"/projects/{project['id']}/operations").json()))
    restored = owner.post(f"/projects/{project['id']}/restore",
                          json={"version": versions[0].get("version")})
    assert restored.status_code in (200, 201), (
        f"restoring an earlier version returned {restored.status_code}: {restored.text[:300]}"
    )
    after = len(_shapes.items(owner.get(f"/projects/{project['id']}/operations").json()))
    assert after > before, "a restore was not recorded as an operation"


def test_matrix_agrees_with_directions():
    author = conftest.session(conftest.AUTHOR_ONE)
    response = author.get("/matrix", params={"origins": conftest.ORIGIN,
                                             "destinations": conftest.DESTINATION})
    assert response.status_code == 200, (
        f"GET /api/matrix returned {response.status_code}: {response.text[:300]}"
    )
    cell = conftest.first_cell(response.json())
    route = author.get("/directions/driving",
                       params={"waypoints": f"{conftest.ORIGIN};{conftest.DESTINATION}"})
    assert abs(cell - route.json().get("duration", 0)) <= conftest.DURATION_TOLERANCE, (
        f"the matrix cell reads {cell} while the equivalent directions call reads "
        f"{route.json().get('duration')}; both read the same graph"
    )


def test_seeded_rows_match_the_fixture():
    owner = conftest.session(conftest.AUTHOR_ONE)
    projects = _shapes.items(owner.get("/projects").json())
    names = {str(p.get("name")) for p in projects}
    assert conftest.PROJECT_NAME in names, (
        f"the seeded project {conftest.PROJECT_NAME!r} is absent; found {sorted(names)}"
    )
    for email in (conftest.AUTHOR_ONE, conftest.AUTHOR_TWO):
        client = conftest.session(email)
        tilesets = _shapes.items(client.get("/tilesets").json())
        assert tilesets, f"{email} owns no seeded tileset"


def test_seeding_is_idempotent():
    counts = {t: conftest.backend_count(t) for t in conftest.SEEDED_TABLES}
    admin = conftest.session(conftest.AUTHOR_ONE)
    admin.post("/health/reseed")
    conftest.settle()
    for table, before in counts.items():
        after = conftest.backend_count(table)
        assert after == before, (
            f"{table} rows moved from {before} to {after}; seeding must be idempotent"
        )


def test_records_live_in_postgres():
    for table in conftest.SEEDED_TABLES:
        assert conftest.backend_count(table) > 0, (
            f"no rows in {table}; the records the app serves must live in the declared database"
        )
    landing = httpx.get(f"{appclient.app_url()}/", timeout=conftest.TIMEOUT,
                        follow_redirects=True)
    for host in conftest.FORBIDDEN_HOSTS:
        assert host not in landing.text, (
            f"the served page reaches out to {host!r}; no external service is contacted at runtime"
        )


def test_duplicate_signup_is_refused():
    again = httpx.post(f"{appclient.api_base()}/auth/signup",
                       json={"email": conftest.AUTHOR_ONE, "password": conftest.PASSWORD},
                       timeout=conftest.TIMEOUT)
    assert 400 <= again.status_code < 500, (
        f"a second sign-up for {conftest.AUTHOR_ONE} returned {again.status_code}, expected a "
        f"client-side refusal: {again.text[:300]}"
    )


def test_refused_quota_call_is_not_billed():
    author = conftest.session(conftest.AUTHOR_ONE)
    before = conftest.service_total(author.get("/usage").json(), "matrix")
    response = author.get("/matrix", params={"origins": conftest.TOO_MANY_ORIGINS,
                                             "destinations": conftest.WAYPOINTS})
    assert 400 <= response.status_code < 500, (
        f"a matrix request past the bound returned {response.status_code}, expected a refusal"
    )
    assert conftest.service_total(author.get("/usage").json(), "matrix") == before, (
        "a refused request was billed"
    )


def test_unknown_address_answers_not_found():
    page = httpx.get(f"{appclient.app_url()}/no-such-page-{os.urandom(4).hex()}",
                     timeout=conftest.TIMEOUT, follow_redirects=True)
    assert page.status_code == 404, (
        f"an unmatched address returned {page.status_code}, expected 404"
    )
    assert conftest.NOT_FOUND_COPY in page.text, (
        f"the not-found page does not carry the pinned copy {conftest.NOT_FOUND_COPY!r}"
    )


def test_malformed_upload_is_rejected_and_stores_nothing():
    author = conftest.session(conftest.AUTHOR_ONE)
    store = conftest.store()
    before = set(store.list("uploads/"))
    response = author.post("/uploads", json={"name": conftest.unique("broken") + ".geojson",
                                             "content": "this is not geometry at all"})
    if response.status_code in (200, 201, 202):
        state = conftest.wait_for_upload(author, response.json().get("id"),
                                         conftest.TERMINAL_STATES)
        assert state == "failed", (
            f"a malformed source finished in state {state!r}, expected failed"
        )
        assert response.json().get("id") not in _shapes.flatten(
            author.get("/tilesets").json()), "a rejected upload produced a tileset"
    else:
        assert 400 <= response.status_code < 500, (
            f"a malformed source returned {response.status_code}, expected a client error"
        )
        assert set(store.list("uploads/")) == before, (
            "a rejected upload still wrote bytes to the bucket"
        )


def test_same_path_operations_leave_one_winner():
    project = conftest.seeded_project(conftest.session(conftest.AUTHOR_ONE))
    base = conftest.current_version(conftest.session(conftest.AUTHOR_ONE), project["id"])
    body = {"path": "layers.water.paint.fill-color", "before": None, "base_version": base}
    outcomes = conftest.race(
        lambda: conftest.session(conftest.AUTHOR_ONE).post(
            f"/projects/{project['id']}/operations", json=dict(body, after="#0a2540")),
        lambda: conftest.session(conftest.AUTHOR_TWO).post(
            f"/projects/{project['id']}/operations", json=dict(body, after="#123456")),
    )
    codes = sorted(r.status_code for r in outcomes)
    winners = [c for c in codes if c in (200, 201)]
    assert len(winners) == 1, (
        f"two simultaneous operations on one path returned {codes}; exactly one must be stored"
    )
    loser = [r for r in outcomes if r.status_code not in (200, 201)][0]
    assert 400 <= loser.status_code < 500, (
        f"the losing writer received {loser.status_code}, expected a conflict response"
    )
    assert "version" in _shapes.flatten(loser.text), (
        f"the conflict response does not name the version it was composed against: "
        f"{loser.text[:300]}"
    )


def test_signed_out_token_cannot_write():
    token = appclient.login(conftest.AUTHOR_ONE, conftest.PASSWORD)
    stale = appclient.client(token)
    project = conftest.seeded_project(conftest.session(conftest.AUTHOR_ONE))
    base = conftest.current_version(conftest.session(conftest.AUTHOR_ONE), project["id"])
    stale.post("/auth/logout")
    response = stale.post(f"/projects/{project['id']}/operations", json={
        "path": "layers.water.paint.fill-color", "before": None, "after": "#000000",
        "base_version": base})
    assert response.status_code in (401, 403), (
        f"a signed-out token still wrote: {response.status_code}"
    )


def test_empty_account_returns_empty_arrays():
    probe = f"probe-{os.urandom(6).hex()}@example.com"
    httpx.post(f"{appclient.api_base()}/auth/signup",
               json={"email": probe, "password": conftest.PASSWORD}, timeout=conftest.TIMEOUT)
    fresh = conftest.session(probe)
    for route in ("/tilesets", "/projects", "/tokens"):
        response = fresh.get(route)
        assert response.status_code == 200, (
            f"GET /api{route} on a fresh account returned {response.status_code}, expected an "
            f"empty list rather than an error"
        )
        assert _shapes.items(response.json()) == [], (
            f"a fresh account reports {response.json()!r} at {route}"
        )


def test_upload_bytes_land_in_the_bucket_at_the_pinned_key():
    author = conftest.session(conftest.AUTHOR_ONE)
    payload = conftest.SAMPLE_DATASET
    made = author.post("/uploads", json={"name": conftest.unique("berths") + ".geojson",
                                         "content": payload})
    assert made.status_code in (200, 201, 202), (
        f"POST /api/uploads returned {made.status_code}: {made.text[:300]}"
    )
    upload = made.json()
    key = upload.get("object_key")
    assert key, f"the upload reports no object_key: {upload}"
    assert key.startswith("uploads/"), (
        f"the object key {key!r} does not open with the pinned uploads/ prefix"
    )
    assert upload.get("sha256") and upload["sha256"][:8] in key, (
        f"the object key {key!r} does not carry the digest {upload.get('sha256')!r}"
    )
    store = conftest.store()
    assert store.exists(key), (
        f"no object exists in the bucket at {key!r}; the uploaded bytes must live in MinIO "
        f"rather than on the application's own disk"
    )


def test_private_tile_is_not_anonymously_readable_in_the_bucket():
    owner = conftest.session(conftest.AUTHOR_ONE)
    tileset = conftest.seeded_private_tileset(owner)
    owner.get(f"/tiles/{tileset['id']}/0/0/0")
    store = conftest.store()
    keys = [k for k in store.list(f"tilesets/{tileset['id']}/") if k.endswith(".pbf")]
    assert keys, (
        f"no tile object exists in the bucket under tilesets/{tileset['id']}/"
    )
    direct = httpx.get(f"{conftest.STORAGE_ENDPOINT}/{conftest.STORAGE_BUCKET}/{keys[0]}",
                       timeout=conftest.TIMEOUT)
    assert direct.status_code in (401, 403, 404), (
        f"the object store served a private tile anonymously: {direct.status_code}. The bucket "
        f"must not carry an anonymous read policy"
    )


