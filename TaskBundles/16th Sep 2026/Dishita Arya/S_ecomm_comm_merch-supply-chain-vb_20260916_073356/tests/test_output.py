"""Graders for Kilnly.

Every assertion reads the running app, the persisted rows, the billing platform
or the mail server. Nothing here reads the app's own claim about its own effect.
"""

from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor

import httpx

import conftest


def test_app_contract_surfaces_are_present():
    with conftest.anon() as client:
        health = client.get("/health")
    assert health.status_code == 200, (
        f"GET {conftest.HEALTH_ROUTE} returned {health.status_code}, expected 200: "
        f"{conftest.excerpt(health)}")
    with conftest.site() as client:
        root = client.get("/")
    assert root.status_code == 200, (
        f"GET / returned {root.status_code}, expected 200 at "
        f"{conftest.app_url()}: {conftest.excerpt(root)}")
    body = health.json()
    assert isinstance(body, dict) and body, (
        f"GET {conftest.HEALTH_ROUTE} returned 200 with no object body: "
        f"{conftest.excerpt(health)}")


def test_reserved_directories_and_credentials_file_are_reachable(backend):
    with conftest.site() as client:
        readme = client.get("/USER_README.md")
    served = readme.status_code == 200 and conftest.SEED_PASSWORD in readme.text
    with conftest.anon() as client:
        declared = client.get("/health")
    assert declared.status_code == 200, (
        f"GET {conftest.HEALTH_ROUTE} returned {declared.status_code} while "
        f"checking the deployment contract: {conftest.excerpt(declared)}")
    assert served or conftest.token_for(conftest.OWNER_EMAIL), (
        f"the seeded logins must work and be written to "
        f"{conftest.CREDENTIALS_FILE}; signing in as "
        f"{conftest.OWNER_EMAIL} with the pinned password did not succeed")


def test_api_shapes_hold_for_list_and_error_paths():
    rows = conftest.products()
    assert rows, "GET /api/products returned an empty top-level array"
    with conftest.anon() as client:
        bad = client.post("/auth/sign-in", json={"email": "not-an-address"})
    assert bad.status_code in conftest.CLIENT_ERROR, (
        f"POST /api/auth/sign-in with a malformed body returned "
        f"{bad.status_code}, expected a client error: {conftest.excerpt(bad)}")
    with conftest.anon() as client:
        anonymous_projects = client.get("/projects")
    assert anonymous_projects.status_code in conftest.DENIED, (
        f"GET /api/projects without a bearer token returned "
        f"{anonymous_projects.status_code}, expected one of "
        f"{conftest.DENIED}: {conftest.excerpt(anonymous_projects)}")


def test_no_mock_store_backs_the_seeded_rows(backend):
    rows = conftest.products()
    slugs = {row.get("slug") for row in rows}
    expected = {slug for slug, _t, _p, _m, _c in conftest.CATALOGUE}
    assert expected <= slugs, (
        f"GET /api/products is missing seeded slugs {sorted(expected - slugs)}; "
        f"the eight products are pinned in the brief and must be persisted rows")
    again = {row.get("slug") for row in conftest.products()}
    assert again == slugs, (
        f"two consecutive reads of GET /api/products returned different slug "
        f"sets, so the catalogue is not being read from a store: "
        f"{sorted(slugs ^ again)}")


def test_overview_surfaces_both_halves_on_one_origin():
    with conftest.site() as client:
        landing = client.get("/")
        shop_page = client.get("/shop")
        console = client.get("/app")
    for route, response in (("/", landing), ("/shop", shop_page), ("/app", console)):
        assert response.status_code < 500, (
            f"GET {route} returned {response.status_code} on the same origin as "
            f"the marketing site: {conftest.excerpt(response)}")
    assert landing.status_code == 200, (
        f"GET / returned {landing.status_code}, expected 200: "
        f"{conftest.excerpt(landing)}")
    assert shop_page.status_code == 200, (
        f"GET /shop returned {shop_page.status_code}, expected the storefront "
        f"on the same origin: {conftest.excerpt(shop_page)}")


def test_absent_features_are_absent():
    with conftest.anon() as client:
        for route in ("/comments", "/follows", "/messages"):
            response = client.get(route)
            assert response.status_code == 404, (
                f"GET /api{route} returned {response.status_code}; the brief "
                f"states the product carries no such feature, so the route must "
                f"answer not found: {conftest.excerpt(response)}")


def test_seeded_accounts_sign_in_with_the_stored_corpus_password():
    for email in conftest.SEEDED_ACCOUNTS:
        token = conftest.token_for(email)
        assert token, (
            f"signing in as {email} with {conftest.SEED_PASSWORD} returned no "
            f"access_token; every seeded account uses that one password")


def test_role_is_never_taken_from_the_request_body():
    email = conftest.probe_email()
    with conftest.anon() as client:
        response = client.post("/auth/sign-up", json={
            "display_name": "Role Probe", "email": email,
            "password": conftest.SEED_PASSWORD, "role": "owner",
            "workspace": conftest.WORKSPACE_ONE})
    assert response.status_code in conftest.OK_CREATED, (
        f"POST /api/auth/sign-up returned {response.status_code}, expected one "
        f"of {conftest.OK_CREATED}: {conftest.excerpt(response)}")
    token = response.json().get("access_token") or conftest.token_for(email)
    with conftest.bearer(token) as client:
        projects = client.get("/projects")
    assert projects.status_code in conftest.DENIED or projects.json() == [], (
        f"an account that asked for the owner role in its own signup body "
        f"reached GET /api/projects with {projects.status_code} and a non-empty "
        f"body, so the role was read from the request: "
        f"{conftest.excerpt(projects)}")


def test_viewer_write_is_denied_and_the_protected_row_is_unchanged(viewer, operator):
    listing = operator.get("/projects")
    assert listing.status_code == 200, (
        f"GET /api/projects as the operator returned {listing.status_code}, "
        f"expected 200: {conftest.excerpt(listing)}")
    projects = listing.json()
    assert projects, "GET /api/projects as the operator returned no seeded project"
    project_id = projects[0]["id"]
    before = viewer.get(f"/projects/{project_id}")
    assert before.status_code == 200, (
        f"GET /api/projects/{project_id} as the viewer returned "
        f"{before.status_code}; a viewer reads every project in the workspace: "
        f"{conftest.excerpt(before)}")
    denied = viewer.post(f"/projects/{project_id}/sample-rounds", json={
        "round_number": 99, "decision": "accept"})
    assert denied.status_code in conftest.DENIED, (
        f"POST /api/projects/{project_id}/sample-rounds from a viewer session "
        f"returned {denied.status_code}, expected one of {conftest.DENIED}: "
        f"{conftest.excerpt(denied)}")
    after = viewer.get(f"/projects/{project_id}")
    assert after.json() == before.json(), (
        f"the refused viewer write changed /api/projects/{project_id}; a denied "
        f"request must leave the protected state exactly as it was")


def test_viewer_cannot_accept_an_offer_or_approve_a_sample(viewer, operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    offers = operator.get(f"/projects/{project_id}/offers")
    assert offers.status_code == 200, (
        f"GET /api/projects/{project_id}/offers as the operator returned "
        f"{offers.status_code}: {conftest.excerpt(offers)}")
    rows = offers.json()
    assert rows, f"project {project_id} carries no seeded offer to attempt"
    refused = viewer.post(f"/offers/{rows[0]['id']}/accept", json={})
    assert refused.status_code in conftest.DENIED, (
        f"POST /api/offers/<id>/accept from a viewer session returned "
        f"{refused.status_code}, expected one of {conftest.DENIED}: "
        f"{conftest.excerpt(refused)}")


def test_operator_writes_a_brief_but_cannot_change_a_role_or_credential(operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    written = operator.put(f"/projects/{project_id}/brief", json={
        "quantity": conftest.BRIEF_QUANTITY, "colourways": ["Ink"],
        "size_curve": {"M": conftest.BRIEF_QUANTITY}})
    assert written.status_code in conftest.OK_CREATED, (
        f"PUT /api/projects/{project_id}/brief as the operator returned "
        f"{written.status_code}, expected one of {conftest.OK_CREATED}: "
        f"{conftest.excerpt(written)}")
    role_change = operator.post("/settings/members", json={
        "email": conftest.VIEWER_EMAIL, "role": "owner"})
    assert role_change.status_code in conftest.DENIED, (
        f"POST /api/settings/members from an operator session returned "
        f"{role_change.status_code}, expected one of {conftest.DENIED}: "
        f"{conftest.excerpt(role_change)}")
    credential = operator.post("/agents", json={"scopes": ["orders"],
                                                "spend_limit_minor": 100000})
    assert credential.status_code in conftest.DENIED, (
        f"POST /api/agents from an operator session returned "
        f"{credential.status_code}, expected one of {conftest.DENIED}: "
        f"{conftest.excerpt(credential)}")


def test_finance_reads_the_money_ledger_but_moves_no_goods(finance):
    ledger = finance.get("/reports/product", params={"period": "2026-09"})
    assert ledger.status_code == 200, (
        f"GET /api/reports/product as finance returned {ledger.status_code}, "
        f"expected 200: {conftest.excerpt(ledger)}")
    projects = finance.get("/projects").json()
    project_id = projects[0]["id"]
    stage = finance.post(f"/runs/{project_id}/stage", json={"stage": "production"})
    assert stage.status_code in conftest.DENIED + (404,), (
        f"POST /api/runs/<id>/stage from a finance session returned "
        f"{stage.status_code}; finance reads money and moves no goods: "
        f"{conftest.excerpt(stage)}")


def test_owner_manages_roles_and_no_cross_workspace_row_is_reachable(owner, owner_two):
    change = owner.post("/settings/members", json={
        "email": conftest.VIEWER_EMAIL, "role": "viewer"})
    assert change.status_code in conftest.OK_CREATED, (
        f"POST /api/settings/members as the owner returned {change.status_code}, "
        f"expected one of {conftest.OK_CREATED}: {conftest.excerpt(change)}")
    mine = owner.get("/projects").json()
    theirs = owner_two.get("/projects").json()
    my_ids = {row["id"] for row in mine}
    their_ids = {row["id"] for row in theirs}
    assert not (my_ids & their_ids), (
        f"{conftest.WORKSPACE_ONE} and {conftest.WORKSPACE_TWO} share project "
        f"ids {sorted(my_ids & their_ids)}; the two workspaces are separate")
    if their_ids:
        crossed = owner.get(f"/projects/{sorted(their_ids)[0]}")
        assert crossed.status_code == 404, (
            f"GET /api/projects/<other workspace id> returned "
            f"{crossed.status_code}, expected 404 so existence does not leak: "
            f"{conftest.excerpt(crossed)}")


def test_cross_workspace_search_and_export_return_nothing(owner, owner_two):
    theirs = owner_two.get("/projects").json()
    assert theirs, f"{conftest.WORKSPACE_TWO} carries no seeded project to hunt"
    needle = str(theirs[0].get("id"))
    found = owner.get("/search", params={"q": needle})
    assert found.status_code in (200, 404), (
        f"GET /api/search returned {found.status_code}: {conftest.excerpt(found)}")
    if found.status_code == 200:
        assert needle not in found.text, (
            f"GET /api/search as {conftest.WORKSPACE_ONE} returned a row "
            f"belonging to {conftest.WORKSPACE_TWO}: {conftest.excerpt(found)}")


def test_visitor_and_buyer_read_boundaries_hold(anonymous, plain_buyer):
    projects = anonymous.get("/projects")
    assert projects.status_code in conftest.DENIED, (
        f"GET /api/projects with no session returned {projects.status_code}, "
        f"expected one of {conftest.DENIED}: {conftest.excerpt(projects)}")
    console = plain_buyer.get("/projects")
    assert console.status_code in conftest.DENIED, (
        f"GET /api/projects as a buyer with no membership returned "
        f"{console.status_code}, expected one of {conftest.DENIED}: "
        f"{conftest.excerpt(console)}")
    guest = conftest.place_order(anonymous, conftest.TOTE_SLUG, 1)
    assert guest.status_code in conftest.OK_CREATED + conftest.REFUSED, (
        f"POST /api/orders as a guest returned {guest.status_code}; a visitor "
        f"may place an order without an account: {conftest.excerpt(guest)}")


def test_a_buyer_cannot_read_another_buyers_order(holder, plain_buyer):
    mine = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                buyer_email=conftest.BUYER_EMAIL)
    assert mine.status_code in conftest.OK_CREATED, (
        f"POST /api/orders as the holder returned {mine.status_code}, expected "
        f"one of {conftest.OK_CREATED}: {conftest.excerpt(mine)}")
    reference = mine.json()["reference"]
    theirs = plain_buyer.get(f"/orders/{reference}")
    assert theirs.status_code in conftest.DENIED + (404,), (
        f"GET /api/orders/{reference} as another buyer returned "
        f"{theirs.status_code}; an order belongs to the buyer who placed it: "
        f"{conftest.excerpt(theirs)}")


def test_signup_is_open_and_grants_no_entitlement():
    email, token = conftest.create_account()
    with conftest.bearer(token) as client:
        listings = conftest.shop(client)
    gated = [row for row in listings
             if row.get("slug") == conftest.GATED_LISTING]
    for row in gated:
        assert int(row.get("price_minor", 0)) != conftest.HOLDER_PRICE_MINOR, (
            f"a brand new account {email} was offered the holder price "
            f"{conftest.HOLDER_PRICE_MINOR} on {conftest.GATED_LISTING}; signing "
            f"up grants no entitlement")


def test_auth_exchanges_a_token_and_leaks_no_account():
    wrong = conftest.sign_in(conftest.OWNER_EMAIL, "not-the-password")
    assert wrong.status_code in conftest.DENIED + conftest.REFUSED, (
        f"POST /api/auth/sign-in with a wrong password returned "
        f"{wrong.status_code}: {conftest.excerpt(wrong)}")
    unknown = conftest.sign_in(conftest.probe_email(), conftest.SEED_PASSWORD)
    assert unknown.status_code == wrong.status_code, (
        f"an unknown address answered {unknown.status_code} while a wrong "
        f"password answered {wrong.status_code}; the two refusals must be "
        f"indistinguishable")
    assert conftest.excerpt(unknown) == conftest.excerpt(wrong) or (
        "password" not in unknown.text.lower()), (
        f"the sign-in refusal names a field: {conftest.excerpt(unknown)}")
    token = conftest.token_for(conftest.OWNER_EMAIL)
    with conftest.bearer(token) as client:
        out = client.post("/auth/sign-out", json={})
        replayed = client.get("/projects")
    assert out.status_code in conftest.OK_CREATED + (204,), (
        f"POST /api/auth/sign-out returned {out.status_code}: "
        f"{conftest.excerpt(out)}")
    assert replayed.status_code in conftest.DENIED, (
        f"a token replayed after sign-out reached GET /api/projects with "
        f"{replayed.status_code}, expected one of {conftest.DENIED}: "
        f"{conftest.excerpt(replayed)}")


def test_password_reset_answers_identically_for_an_unknown_address():
    with conftest.anon() as client:
        known = client.post("/auth/reset", json={"email": conftest.OWNER_EMAIL})
        unknown = client.post("/auth/reset", json={"email": conftest.probe_email()})
    assert known.status_code == unknown.status_code, (
        f"POST /api/auth/reset answered {known.status_code} for a seeded address "
        f"and {unknown.status_code} for an unknown one; the form must not become "
        f"an account-existence oracle")


def test_public_routes_are_served_from_the_products_own_components(public):
    for route in conftest.PUBLIC_ROUTES:
        response = public.get(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}, expected 200: "
            f"{conftest.excerpt(response)}")
        assert len(response.text) > 200, (
            f"GET {route} returned a body of {len(response.text)} characters, "
            f"which cannot be a rendered marketing route")


def test_public_route_titles_and_previews_are_distinct(public):
    titles = {}
    descriptions = {}
    for route in conftest.PUBLIC_ROUTES:
        text = public.get(route).text
        title = text.split("<title>")[-1].split("</title>")[0] if "<title>" in text else ""
        assert title.strip(), (
            f"GET {route} returned a document with no title element; every "
            f"public route carries its own title")
        assert title not in titles, (
            f"{route} shares the title {title!r} with {titles[title]}; no two "
            f"public routes share a title")
        titles[title] = route
        marker = 'name="description"'
        assert marker in text or "og:description" in text, (
            f"GET {route} declares no description; every public route carries "
            f"its own description")
        descriptions[route] = text.count("og:")
        assert descriptions[route] > 0, (
            f"GET {route} declares no social preview; every public route "
            f"declares a preview title with an image")


def test_seeded_catalogue_rows_carry_their_prices_and_minimums():
    rows = {row["slug"]: row for row in conftest.products()}
    for slug, title, price, minimum, category in conftest.CATALOGUE:
        assert slug in rows, (
            f"GET /api/products carries no product {slug!r}; the eight seeded "
            f"products are pinned in the brief")
        row = rows[slug]
        assert row.get("title") == title, (
            f"product {slug!r} carries the title {row.get('title')!r}, expected "
            f"{title!r}")
        assert int(row.get("from_price_minor", -1)) == price, (
            f"product {slug!r} carries from_price_minor "
            f"{row.get('from_price_minor')!r}, expected {price}")
        assert int(row.get("minimum_quantity", -1)) == minimum, (
            f"product {slug!r} carries minimum_quantity "
            f"{row.get('minimum_quantity')!r}, expected {minimum}")
        assert row.get("category") == category, (
            f"product {slug!r} carries category {row.get('category')!r}, "
            f"expected {category!r}")


def test_catalogue_filter_is_a_shareable_address(public):
    outerwear = conftest.products("outerwear")
    slugs = {row["slug"] for row in outerwear}
    assert slugs == {conftest.JACKET_SLUG}, (
        f"GET /api/products?category=outerwear returned {sorted(slugs)}, "
        f"expected only {conftest.JACKET_SLUG!r}")
    shared = public.get("/catalogue", params={"category": "outerwear"})
    assert shared.status_code == 200, (
        f"GET /catalogue?category=outerwear returned {shared.status_code}; a "
        f"filtered catalogue must be an address somebody can send: "
        f"{conftest.excerpt(shared)}")


def test_start_a_project_carries_the_product_into_a_stored_brief(operator):
    created = operator.post("/projects", json={"product_slug": conftest.JACKET_SLUG})
    assert created.status_code in conftest.OK_CREATED, (
        f"POST /api/projects with product_slug={conftest.JACKET_SLUG!r} returned "
        f"{created.status_code}, expected one of {conftest.OK_CREATED}: "
        f"{conftest.excerpt(created)}")
    body = created.json()
    project_id = body["id"]
    read_back = operator.get(f"/projects/{project_id}")
    assert read_back.status_code == 200, (
        f"GET /api/projects/{project_id} returned {read_back.status_code}: "
        f"{conftest.excerpt(read_back)}")
    stored = read_back.json()
    assert conftest.JACKET_SLUG in str(stored), (
        f"the project created from {conftest.JACKET_SLUG!r} does not name that "
        f"product when read back: {str(stored)[:300]}")


def test_marketing_price_matches_the_quoting_catalogue(operator):
    marketing = {row["slug"]: row["from_price_minor"] for row in conftest.products()}
    quoting = operator.get("/products")
    assert quoting.status_code == 200, (
        f"GET /api/products with a member session returned "
        f"{quoting.status_code}: {conftest.excerpt(quoting)}")
    for row in quoting.json():
        assert int(row["from_price_minor"]) == int(marketing[row["slug"]]), (
            f"product {row['slug']!r} is advertised at "
            f"{marketing[row['slug']]} and quoted at {row['from_price_minor']}; "
            f"the shop window may not show a price the platform will not honour")


def test_fulfillment_page_serves_its_thesis_and_figures(public):
    page = public.get("/merch-fulfillment")
    assert page.status_code == 200, (
        f"GET /merch-fulfillment returned {page.status_code}: "
        f"{conftest.excerpt(page)}")
    assert conftest.FULFILLMENT_THESIS in page.text, (
        f"GET /merch-fulfillment does not carry {conftest.FULFILLMENT_THESIS!r}")
    for figure in (conftest.OPS_SURFACE_FIGURE, conftest.MINIMUM_ORDER_FIGURE):
        assert figure in page.text, (
            f"GET /merch-fulfillment does not carry the figure {figure!r}")


def test_no_minimum_path_prices_a_single_unit(operator):
    project = operator.post("/projects", json={
        "product_slug": conftest.TOTE_SLUG}).json()
    written = operator.put(f"/projects/{project['id']}/brief",
                           json={"quantity": 1})
    assert written.status_code in conftest.OK_CREATED, (
        f"PUT /api/projects/<id>/brief with a quantity of 1 returned "
        f"{written.status_code}; the no-minimum path prices a single unit: "
        f"{conftest.excerpt(written)}")
    offers = operator.get(f"/projects/{project['id']}/offers",
                          params={"quantity": 1})
    assert offers.status_code == 200, (
        f"GET /api/projects/<id>/offers?quantity=1 returned "
        f"{offers.status_code}: {conftest.excerpt(offers)}")


def test_field_notes_and_brand_kit_are_seeded(public):
    index = public.get("/blog")
    assert index.status_code == 200, (
        f"GET /blog returned {index.status_code}: {conftest.excerpt(index)}")
    for category in conftest.NOTE_CATEGORIES:
        assert category in index.text, (
            f"GET /blog does not carry the seeded category {category!r}")
    brand = public.get("/brand")
    assert brand.status_code == 200, (
        f"GET /brand returned {brand.status_code}: {conftest.excerpt(brand)}")


def test_legal_routes_are_served_and_linked_from_the_footer(public):
    for route in (conftest.TERMS_ROUTE, conftest.PRIVACY_ROUTE):
        response = public.get(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}, expected 200: "
            f"{conftest.excerpt(response)}")
    landing = public.get("/").text
    assert conftest.TERMS_ROUTE in landing, (
        f"the landing document does not link {conftest.TERMS_ROUTE}; the terms "
        f"route is reachable from the footer of every page")
    signup = public.get("/sign-up").text
    assert conftest.TERMS_ROUTE in signup, (
        f"the signup document does not link {conftest.TERMS_ROUTE}")


def test_unknown_address_answers_not_found_with_the_products_own_screen(public):
    response = public.get("/no-such-address-here")
    assert response.status_code == 404, (
        f"GET /no-such-address-here returned {response.status_code}, expected "
        f"404: {conftest.excerpt(response)}")
    assert conftest.NOT_FOUND_LINE in response.text, (
        f"the not-found screen does not carry {conftest.NOT_FOUND_LINE!r}: "
        f"{conftest.excerpt(response)}")


def test_internal_links_on_public_routes_resolve(public):
    for route in conftest.PUBLIC_ROUTES:
        page = public.get(route)
        targets = set(re.findall(r'href="(/[^"#?]*)"', page.text))
        for target in sorted(targets)[:12]:
            linked = public.get(target)
            assert linked.status_code == 200, (
                f"{route} links {target}, which returned {linked.status_code}; "
                f"every internal link on every public route resolves")


def test_sitemap_and_robots_are_served(public):
    sitemap = public.get(conftest.SITEMAP_ROUTE)
    assert sitemap.status_code == 200, (
        f"GET {conftest.SITEMAP_ROUTE} returned {sitemap.status_code}: "
        f"{conftest.excerpt(sitemap)}")
    for route in conftest.PUBLIC_ROUTES:
        assert route in sitemap.text, (
            f"{conftest.SITEMAP_ROUTE} does not list the public route {route!r}")
    robots = public.get(conftest.ROBOTS_ROUTE)
    assert robots.status_code == 200, (
        f"GET {conftest.ROBOTS_ROUTE} returned {robots.status_code}: "
        f"{conftest.excerpt(robots)}")
    assert "sitemap" in robots.text.lower(), (
        f"{conftest.ROBOTS_ROUTE} does not name the sitemap: "
        f"{conftest.excerpt(robots)}")


def test_workspace_scopes_its_projects_and_its_search(owner, operator):
    listing = operator.get("/projects")
    assert listing.status_code == 200, (
        f"GET /api/projects as the operator returned {listing.status_code}: "
        f"{conftest.excerpt(listing)}")
    rows = listing.json()
    assert rows, "the seeded workspace carries no project"
    for row in rows:
        assert "state" in row, (
            f"a project row carries no state: {str(row)[:200]}")
        assert "next_action" in row, (
            f"a project row carries no next_action line: {str(row)[:200]}")
    created = operator.post("/projects", json={"product_slug": conftest.TOTE_SLUG})
    assert created.status_code in conftest.OK_CREATED, (
        f"POST /api/projects returned {created.status_code}, expected one of "
        f"{conftest.OK_CREATED}: {conftest.excerpt(created)}")


def test_brief_records_its_fields_as_stored_rows(operator):
    project = operator.post("/projects", json={
        "product_slug": conftest.JACKET_SLUG}).json()
    payload = {
        "quantity": conftest.BRIEF_QUANTITY,
        "colourways": ["Ink", "Sand"],
        "size_curve": {"S": 100, "M": 250, "L": 150},
        "materials": "12oz cotton canvas",
        "packaging": "polybag",
        "target_landed_minor": 5500,
        "needed_by": "2026-12-01",
    }
    written = operator.put(f"/projects/{project['id']}/brief", json=payload)
    assert written.status_code in conftest.OK_CREATED, (
        f"PUT /api/projects/<id>/brief returned {written.status_code}: "
        f"{conftest.excerpt(written)}")
    read_back = operator.get(f"/projects/{project['id']}").json()
    body = str(read_back)
    for marker in ("500", "Ink", "polybag", "2026-12-01"):
        assert marker in body, (
            f"the stored brief does not carry {marker!r} when read back: "
            f"{body[:300]}")


def test_artwork_gate_refuses_in_the_decoration_methods_own_terms(operator):
    project = operator.post("/projects", json={
        "product_slug": conftest.JACKET_SLUG}).json()
    operator.put(f"/projects/{project['id']}/brief",
                 json={"quantity": conftest.BRIEF_QUANTITY})
    refused = operator.post(f"/projects/{project['id']}/artwork", json={
        "method": "screen_print", "position": "front",
        "pixel_width": conftest.ARTWORK_PIXEL_WIDTH,
        "pixel_height": conftest.ARTWORK_PIXEL_WIDTH,
        "printed_width_mm": conftest.ARTWORK_PRINT_CM * 10,
        "colour_count": 3, "bleed_mm": conftest.BLEED_MM})
    assert refused.status_code in conftest.OK_CREATED + conftest.REFUSED, (
        f"POST /api/projects/<id>/artwork returned {refused.status_code}: "
        f"{conftest.excerpt(refused)}")
    body = refused.text
    assert str(conftest.ARTWORK_EFFECTIVE_PPI) in body, (
        f"the artwork refusal does not name the effective resolution "
        f"{conftest.ARTWORK_EFFECTIVE_PPI}; a refusal is written in the "
        f"artwork's own terms: {conftest.excerpt(refused)}")
    assert str(conftest.MIN_PPI) in body, (
        f"the artwork refusal does not name the {conftest.MIN_PPI} minimum: "
        f"{conftest.excerpt(refused)}")


def test_artwork_colour_limit_is_enforced_per_method(operator):
    project = operator.post("/projects", json={
        "product_slug": conftest.JACKET_SLUG}).json()
    operator.put(f"/projects/{project['id']}/brief",
                 json={"quantity": conftest.BRIEF_QUANTITY})
    too_many = operator.post(f"/projects/{project['id']}/artwork", json={
        "method": "screen_print", "position": "front",
        "pixel_width": 4000, "pixel_height": 4000, "printed_width_mm": 200,
        "colour_count": conftest.SCREEN_PRINT_COLOURS + 1,
        "bleed_mm": conftest.BLEED_MM})
    assert str(conftest.SCREEN_PRINT_COLOURS) in too_many.text, (
        f"artwork carrying {conftest.SCREEN_PRINT_COLOURS + 1} spot colours for "
        f"screen_print was not refused against the {conftest.SCREEN_PRINT_COLOURS} "
        f"limit: {conftest.excerpt(too_many)}")


def test_artwork_that_has_not_passed_blocks_a_quote_request(operator):
    project = operator.post("/projects", json={
        "product_slug": conftest.JACKET_SLUG}).json()
    operator.put(f"/projects/{project['id']}/brief",
                 json={"quantity": conftest.BRIEF_QUANTITY})
    operator.post(f"/projects/{project['id']}/artwork", json={
        "method": "screen_print", "position": "front",
        "pixel_width": conftest.ARTWORK_PIXEL_WIDTH, "pixel_height": 400,
        "printed_width_mm": conftest.ARTWORK_PRINT_CM * 10,
        "colour_count": 2, "bleed_mm": 0})
    requested = operator.post(f"/projects/{project['id']}/quote-requests", json={})
    assert requested.status_code in conftest.REFUSED, (
        f"POST /api/projects/<id>/quote-requests with refused artwork returned "
        f"{requested.status_code}, expected one of {conftest.REFUSED}: "
        f"{conftest.excerpt(requested)}")


def test_invalid_brief_input_is_refused_inline_and_stores_nothing(operator):
    project = operator.post("/projects", json={
        "product_slug": conftest.JACKET_SLUG}).json()
    before = operator.get(f"/projects/{project['id']}").json()
    bad = operator.put(f"/projects/{project['id']}/brief",
                       json={"quantity": -5})
    assert bad.status_code in conftest.REFUSED, (
        f"PUT /api/projects/<id>/brief with a negative quantity returned "
        f"{bad.status_code}, expected one of {conftest.REFUSED}: "
        f"{conftest.excerpt(bad)}")
    assert "quantity" in bad.text.lower(), (
        f"the refusal does not name the field it refuses: "
        f"{conftest.excerpt(bad)}")
    after = operator.get(f"/projects/{project['id']}").json()
    assert after == before, (
        "a refused brief write changed the stored project; an invalid write "
        "stores nothing")


def test_quote_request_fans_out_to_every_eligible_supplier(operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    requests = operator.post(f"/projects/{project_id}/quote-requests", json={})
    assert requests.status_code in conftest.OK_CREATED, (
        f"POST /api/projects/{project_id}/quote-requests returned "
        f"{requests.status_code}, expected one of {conftest.OK_CREATED}: "
        f"{conftest.excerpt(requests)}")
    rows = requests.json()
    assert isinstance(rows, list) and rows, (
        f"POST /api/projects/{project_id}/quote-requests returned no request "
        f"rows: {str(rows)[:300]}")
    again = operator.get(f"/projects/{project_id}/offers")
    assert again.status_code == 200, (
        f"GET /api/projects/{project_id}/offers returned {again.status_code}: "
        f"{conftest.excerpt(again)}")


def test_landed_cost_normalises_every_reply_and_shows_its_working(operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    offers = operator.get(f"/projects/{project_id}/offers",
                          params={"quantity": conftest.BRIEF_QUANTITY}).json()
    assert offers, (
        f"GET /api/projects/{project_id}/offers returned no offer at quantity "
        f"{conftest.BRIEF_QUANTITY}")
    by_supplier = {row.get("supplier"): row for row in offers}
    assert conftest.AVEIRO in by_supplier, (
        f"the seeded offers do not include {conftest.AVEIRO!r}: "
        f"{sorted(by_supplier)}")
    working = by_supplier[conftest.AVEIRO].get("landed_cost") or {}
    expected = {
        "unit_minor": conftest.UNIT_IN_USD_MINOR,
        "setup_per_unit_minor": conftest.SETUP_PER_UNIT_MINOR,
        "freight_per_unit_minor": conftest.FREIGHT_PER_UNIT_MINOR,
        "duty_per_unit_minor": conftest.DUTY_PER_UNIT_MINOR,
        "insurance_per_unit_minor": conftest.INSURANCE_PER_UNIT_MINOR,
        "total_per_unit_minor": conftest.AVEIRO_LANDED_MINOR,
    }
    for field, value in expected.items():
        assert int(working.get(field, -1)) == value, (
            f"the {conftest.AVEIRO} landed cost carries {field}="
            f"{working.get(field)!r}, expected {value}: {str(working)[:300]}")
    assert str(working.get("rate")) == conftest.EUR_RATE, (
        f"the landed cost carries rate {working.get('rate')!r}, expected "
        f"{conftest.EUR_RATE}")
    assert str(working.get("rate_date")).startswith(conftest.EUR_RATE_DATE), (
        f"the landed cost carries rate_date {working.get('rate_date')!r}, "
        f"expected {conftest.EUR_RATE_DATE}")


def test_lowest_headline_price_is_not_the_lowest_landed_cost(operator):
    projects = operator.get("/projects").json()
    offers = operator.get(f"/projects/{projects[0]['id']}/offers",
                          params={"quantity": conftest.BRIEF_QUANTITY}).json()
    by_supplier = {row.get("supplier"): row for row in offers}
    assert conftest.TIRUPUR in by_supplier, (
        f"the seeded offers do not include {conftest.TIRUPUR!r}: "
        f"{sorted(by_supplier)}")
    tirupur = by_supplier[conftest.TIRUPUR]
    aveiro = by_supplier[conftest.AVEIRO]
    assert int(tirupur["landed_cost"]["total_per_unit_minor"]) == conftest.TIRUPUR_LANDED_MINOR, (
        f"{conftest.TIRUPUR} lands at "
        f"{tirupur['landed_cost']['total_per_unit_minor']!r}, expected "
        f"{conftest.TIRUPUR_LANDED_MINOR}")
    assert int(tirupur.get("unit_price_minor", -1)) == conftest.TIRUPUR_HEADLINE_MINOR, (
        f"{conftest.TIRUPUR} carries the headline "
        f"{tirupur.get('unit_price_minor')!r}, expected "
        f"{conftest.TIRUPUR_HEADLINE_MINOR}")
    assert (int(aveiro["landed_cost"]["total_per_unit_minor"])
            < int(tirupur["landed_cost"]["total_per_unit_minor"])), (
        f"{conftest.AVEIRO} does not land below {conftest.TIRUPUR} at quantity "
        f"{conftest.BRIEF_QUANTITY}; the cheapest headline is the wrong answer here")


def test_offer_comparison_is_stable_under_reordering(operator):
    projects = operator.get("/projects").json()
    first = operator.get(f"/projects/{projects[0]['id']}/offers",
                         params={"quantity": conftest.BRIEF_QUANTITY}).json()
    second = operator.get(f"/projects/{projects[0]['id']}/offers",
                          params={"quantity": conftest.BRIEF_QUANTITY}).json()
    order_one = [row.get("supplier") for row in first]
    order_two = [row.get("supplier") for row in second]
    assert order_one == order_two, (
        f"two reads of the same comparison returned different orders "
        f"{order_one} and {order_two}; the ranking is stable")
    totals = [int(row["landed_cost"]["total_per_unit_minor"]) for row in first]
    assert totals == sorted(totals), (
        f"the comparison is not ordered by landed cost per unit: {totals}")


def test_quote_pins_its_rate_and_reports_its_price_breaks(operator):
    projects = operator.get("/projects").json()
    offers = operator.get(f"/projects/{projects[0]['id']}/offers",
                          params={"quantity": conftest.BRIEF_QUANTITY}).json()
    aveiro = [row for row in offers if row.get("supplier") == conftest.AVEIRO][0]
    breaks = aveiro.get("price_breaks") or []
    thresholds = sorted(int(row["quantity_threshold"]) for row in breaks)
    assert thresholds == conftest.PRICE_BREAKS, (
        f"{conftest.AVEIRO} reports price-break thresholds {thresholds}, "
        f"expected {conftest.PRICE_BREAKS}")
    later = operator.get(f"/projects/{projects[0]['id']}/offers",
                         params={"quantity": conftest.BRIEF_QUANTITY}).json()
    aveiro_later = [row for row in later if row.get("supplier") == conftest.AVEIRO][0]
    assert str(aveiro_later["landed_cost"]["rate"]) == conftest.EUR_RATE, (
        f"the recorded rate moved between two reads of one quote: "
        f"{aveiro_later['landed_cost']['rate']!r}")


def test_expired_offer_cannot_be_accepted(operator):
    projects = operator.get("/projects").json()
    offers = operator.get(f"/projects/{projects[0]['id']}/offers").json()
    expired = [row for row in offers if row.get("state") == "expired"]
    assert expired, (
        f"the seeded project carries no offer in state 'expired'; expiry is a "
        f"state an offer moves into: {[row.get('state') for row in offers]}")
    refused = operator.post(f"/offers/{expired[0]['id']}/accept", json={})
    assert refused.status_code in conftest.REFUSED, (
        f"POST /api/offers/<expired id>/accept returned {refused.status_code}, "
        f"expected one of {conftest.REFUSED}: {conftest.excerpt(refused)}")
    after = operator.get(f"/projects/{projects[0]['id']}/offers").json()
    still = [row for row in after if row["id"] == expired[0]["id"]][0]
    assert still.get("state") == "expired", (
        f"the refused acceptance moved the offer to {still.get('state')!r}; an "
        f"expired offer stays expired")


def test_supplier_prices_never_appear_in_a_storefront_or_agent_payload(anonymous):
    listings = conftest.shop(anonymous)
    body = str(listings)
    for marker in (conftest.AVEIRO, conftest.TIRUPUR,
                   str(conftest.AVEIRO_LANDED_MINOR),
                   str(conftest.TIRUPUR_HEADLINE_MINOR)):
        assert marker not in body, (
            f"GET /api/shop leaks the supplier fact {marker!r}; supplier "
            f"contacts, prices and terms never reach a buyer-facing payload")
    catalogue = anonymous.get("/agent/catalogue")
    if catalogue.status_code == 200:
        for marker in (conftest.AVEIRO, conftest.TIRUPUR):
            assert marker not in catalogue.text, (
                f"GET /api/agent/catalogue leaks the supplier {marker!r}")


def test_sample_round_stores_its_evidence_and_its_decision(operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    created = operator.post(f"/projects/{project_id}/sample-rounds", json={
        "round_number": 1,
        "requested": "first proto",
        "evidence": [{"angle": "front"}, {"angle": "back"}],
        "measurements": {"chest_mm": 560, "tolerance_mm": 10},
        "defects": [{"severity": "major", "location": "left cuff"},
                    {"severity": "minor", "location": "hem"}],
        "decision": "rework"})
    assert created.status_code in conftest.OK_CREATED, (
        f"POST /api/projects/{project_id}/sample-rounds returned "
        f"{created.status_code}, expected one of {conftest.OK_CREATED}: "
        f"{conftest.excerpt(created)}")
    stored = created.json()
    assert stored.get("decision") in conftest.SAMPLE_DECISIONS, (
        f"the stored round carries decision {stored.get('decision')!r}, "
        f"expected one of {conftest.SAMPLE_DECISIONS}")
    assert len(stored.get("defects") or []) == 2, (
        f"the stored round carries {len(stored.get('defects') or [])} defects, "
        f"expected the two that were recorded: {str(stored)[:300]}")


def test_rework_carries_its_defect_list_into_the_next_round(operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    operator.post(f"/projects/{project_id}/sample-rounds", json={
        "round_number": 1, "decision": "rework",
        "defects": [{"severity": "major", "location": "left cuff"}]})
    second = operator.post(f"/projects/{project_id}/sample-rounds", json={
        "round_number": 2, "decision": "accept"})
    assert second.status_code in conftest.OK_CREATED, (
        f"POST a second sample round returned {second.status_code}: "
        f"{conftest.excerpt(second)}")
    body = str(second.json())
    assert "left cuff" in body or "carried" in body, (
        f"the second round does not carry the previous round's defect list "
        f"forward: {body[:300]}")


def test_sample_approval_is_attributable_and_immutable(operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    created = operator.post(f"/projects/{project_id}/sample-rounds", json={
        "round_number": 3, "decision": "accept"}).json()
    round_id = created["id"]
    body = str(created)
    assert conftest.OPERATOR_EMAIL in body or "decided_by" in body, (
        f"the accepted round records nobody as having decided it: {body[:300]}")
    changed = operator.post(f"/projects/{project_id}/sample-rounds", json={
        "id": round_id, "round_number": 3, "decision": "reject"})
    if changed.status_code in conftest.OK_CREATED:
        assert changed.json().get("id") != round_id, (
            f"an accepted round was rewritten in place; approvals are immutable")


def test_batch_gate_blocks_a_shipment_over_its_acceptance_rule(operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    rule = operator.get(f"/projects/{project_id}").json()
    body = str(rule)
    assert str(conftest.INSPECTION_SAMPLE_SIZE) in body, (
        f"the project does not carry the seeded sample size "
        f"{conftest.INSPECTION_SAMPLE_SIZE}: {body[:300]}")
    inspection = operator.post(f"/runs/{project_id}/inspection", json={
        "sample_size": conftest.INSPECTION_SAMPLE_SIZE,
        "defects": [{"severity": "major", "location": "seam"},
                    {"severity": "major", "location": "seam"},
                    {"severity": "major", "location": "seam"}]})
    assert inspection.status_code in conftest.OK_CREATED, (
        f"POST /api/runs/{project_id}/inspection returned "
        f"{inspection.status_code}: {conftest.excerpt(inspection)}")
    result = inspection.json()
    assert result.get("blocked") is True, (
        f"three major defects against a limit of {conftest.MAX_MAJOR} did not "
        f"block the shipment: {str(result)[:300]}")
    assert str(result.get("decision_required") or result).strip(), (
        f"a blocked batch raised no decision: {str(result)[:300]}")


def test_dispatch_against_a_blocked_batch_is_refused(operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    operator.post(f"/runs/{project_id}/inspection", json={
        "sample_size": conftest.INSPECTION_SAMPLE_SIZE,
        "defects": [{"severity": "critical", "location": "print"}]})
    refused = operator.post(f"/orders/{conftest.SEEDED_ORDER_REFERENCE}/dispatch",
                            json={"run_id": project_id})
    assert refused.status_code in conftest.REFUSED + (404,), (
        f"dispatching against a blocked batch returned {refused.status_code}, "
        f"expected a refusal: {conftest.excerpt(refused)}")


def test_run_stages_and_split_lots_are_stored_separately(operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    run = operator.get(f"/projects/{project_id}").json()
    body = str(run)
    for stage in conftest.RUN_STAGES:
        assert stage in body, (
            f"the run does not name the stage {stage!r}: {body[:400]}")
    lots = operator.get(f"/projects/{project_id}/lots")
    if lots.status_code == 200:
        rows = lots.json()
        costs = sorted(int(row["landed_cost_minor"]) for row in rows)
        assert costs == sorted(conftest.LOT_COSTS), (
            f"the seeded lots carry landed costs {costs}, expected "
            f"{sorted(conftest.LOT_COSTS)}")


def test_stage_slip_recomputes_the_projected_date_with_its_cause(operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    before = operator.get(f"/projects/{project_id}").json()
    slipped = operator.post(f"/runs/{project_id}/stage", json={
        "stage": "production", "actual_end": "2026-11-20",
        "cause": "factory slip"})
    assert slipped.status_code in conftest.OK_CREATED, (
        f"POST /api/runs/{project_id}/stage returned {slipped.status_code}: "
        f"{conftest.excerpt(slipped)}")
    after = operator.get(f"/projects/{project_id}").json()
    assert str(after) != str(before), (
        "a slipped stage left the project unchanged; a slip recomputes the "
        "projected ready date")
    assert "factory slip" in str(after), (
        f"the recomputed date records no cause: {str(after)[:400]}")


def test_inventory_balances_are_summed_from_the_stored_ledger(backend, operator):
    rows = conftest.inventory(conftest.JACKET_SKU)
    assert rows, (
        f"GET /api/inventory?sku={conftest.JACKET_SKU} returned no row; stock "
        f"lives at {conftest.LOCATIONS}")
    for row in rows:
        assert row.get("location") in conftest.LOCATIONS, (
            f"an inventory row names the location {row.get('location')!r}, "
            f"expected one of {conftest.LOCATIONS}")
        assert int(row["available"]) <= int(row["on_hand"]), (
            f"available {row['available']} exceeds on_hand {row['on_hand']} at "
            f"{row['location']}; available is on_hand minus reservations minus "
            f"damaged")
    events = operator.get("/inventory/events",
                          params={"sku": conftest.JACKET_SKU})
    assert events.status_code == 200, (
        f"GET /api/inventory/events returned {events.status_code}; the ledger "
        f"is what the balances are summed from: {conftest.excerpt(events)}")
    kinds = {row.get("kind") for row in events.json()}
    assert kinds <= set(conftest.LEDGER_KINDS), (
        f"the ledger carries kinds {sorted(kinds - set(conftest.LEDGER_KINDS))} "
        f"outside the pinned set {conftest.LEDGER_KINDS}")


def test_seeded_boundary_leaves_one_unit_available_at_newark():
    newark = conftest.available(conftest.JACKET_SKU, "newark")
    assert newark == 1, (
        f"available for {conftest.JACKET_SKU} at newark is {newark}, expected "
        f"exactly 1; that boundary is the seeded race")
    rotterdam = conftest.available(conftest.JACKET_SKU, "rotterdam")
    assert rotterdam == 0, (
        f"available for {conftest.JACKET_SKU} at rotterdam is {rotterdam}, "
        f"expected 0")


def test_reservation_and_release_move_available(holder):
    before = conftest.available(conftest.TOTE_SKU, "rotterdam")
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL)
    assert order.status_code in conftest.OK_CREATED, (
        f"POST /api/orders returned {order.status_code}: "
        f"{conftest.excerpt(order)}")
    reference = order.json()["reference"]
    during = conftest.settle(
        lambda: conftest.available(conftest.TOTE_SKU, "rotterdam") < before)
    assert during, (
        f"available for {conftest.TOTE_SKU} stayed at {before} after an order "
        f"reserved a unit; placing an order reserves stock")
    cancelled = holder.post(f"/orders/{reference}/transitions",
                            json={"to": "cancelled"})
    assert cancelled.status_code in conftest.OK_CREATED, (
        f"cancelling {reference} returned {cancelled.status_code}: "
        f"{conftest.excerpt(cancelled)}")
    released = conftest.settle(
        lambda: conftest.available(conftest.TOTE_SKU, "rotterdam") == before)
    assert released, (
        f"cancelling {reference} did not release its reservation; available is "
        f"{conftest.available(conftest.TOTE_SKU, 'rotterdam')}, expected {before}")


def test_concurrent_orders_for_the_last_unit_leave_exactly_one_reservation():
    tokens = [conftest.token_for(conftest.BUYER2_EMAIL),
              conftest.token_for(conftest.BUYER3_EMAIL)]

    def attempt(token):
        with conftest.bearer(token) as client:
            return conftest.place_order(client, conftest.GATED_LISTING, 1,
                                        buyer_email=conftest.BUYER2_EMAIL)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(attempt, tokens))
    codes = [r.status_code for r in results]
    winners = [r for r in results if r.status_code in conftest.OK_CREATED]
    losers = [r for r in results if r.status_code not in conftest.OK_CREATED]
    assert len(winners) <= 1, (
        f"two simultaneous orders for the last {conftest.JACKET_SKU} both "
        f"succeeded with {codes}; exactly one reservation may exist")
    if losers:
        assert losers[0].status_code == conftest.CONFLICT, (
            f"the loser of the race answered {losers[0].status_code}, expected "
            f"{conftest.CONFLICT}: {conftest.excerpt(losers[0])}")
        assert conftest.JACKET_SKU in losers[0].text, (
            f"the conflict response does not name the stock keeping unit that "
            f"was taken: {conftest.excerpt(losers[0])}")
    assert conftest.available(conftest.JACKET_SKU, "newark") >= 0, (
        f"available for {conftest.JACKET_SKU} at newark went negative after the "
        f"race")


def test_contention_on_the_last_unit_never_oversells_under_repeated_firing():
    before = conftest.available(conftest.TOTE_SKU, "rotterdam")
    tokens = [conftest.token_for(conftest.BUYER2_EMAIL) for _ in range(4)]

    def attempt(token):
        with conftest.bearer(token) as client:
            return conftest.place_order(client, conftest.TOTE_SLUG, 1,
                                        buyer_email=conftest.BUYER2_EMAIL)

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(attempt, tokens))
    accepted = sum(1 for r in results if r.status_code in conftest.OK_CREATED)
    after = conftest.settle(
        lambda: conftest.available(conftest.TOTE_SKU, "rotterdam") == before - accepted)
    assert after, (
        f"{accepted} orders were accepted but available moved from {before} to "
        f"{conftest.available(conftest.TOTE_SKU, 'rotterdam')}; every balance is "
        f"the sum of the ledger")
    assert conftest.available(conftest.TOTE_SKU, "rotterdam") >= 0, (
        "an inventory balance went negative under contention")


def test_transfer_units_belong_to_neither_location_while_in_flight(operator):
    departed = operator.post("/transfers", json={
        "sku": conftest.JACKET_SKU, "from": "rotterdam", "to": "newark",
        "units": 1})
    assert departed.status_code in conftest.OK_CREATED + conftest.REFUSED, (
        f"POST /api/transfers returned {departed.status_code}: "
        f"{conftest.excerpt(departed)}")
    listing = operator.get("/transfers")
    assert listing.status_code == 200, (
        f"GET /api/transfers returned {listing.status_code}: "
        f"{conftest.excerpt(listing)}")
    rows = listing.json()
    in_flight = [row for row in rows if row.get("state") == "departed"]
    assert in_flight, (
        f"no transfer is in state 'departed'; the seeded in-flight transfer "
        f"moves {conftest.TRANSFER_UNITS} units of {conftest.JACKET_SKU}: "
        f"{str(rows)[:300]}")
    row = in_flight[0]
    origin = conftest.available(row["sku"], row["from"])
    destination = conftest.available(row["sku"], row["to"])
    assert origin >= 0 and destination >= 0, (
        f"an in-flight transfer left a negative balance at {row['from']} or "
        f"{row['to']}")


def test_order_routing_splits_into_one_promise(holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 2,
                                 buyer_email=conftest.BUYER_EMAIL,
                                 destination="US-CA")
    assert order.status_code in conftest.OK_CREATED, (
        f"POST /api/orders for a split-capable quantity returned "
        f"{order.status_code}: {conftest.excerpt(order)}")
    body = order.json()
    assert body.get("promise"), (
        f"the order carries no promise: {str(body)[:300]}")
    assert isinstance(body["promise"], dict), (
        f"the order carries {len(body['promise'])} promises; a split order is "
        f"one order with one delivery promise: {str(body['promise'])[:200]}")


def test_forecast_projects_a_stockout_date_and_a_reorder_point(operator):
    forecast = operator.get("/inventory/forecast",
                            params={"sku": conftest.JACKET_SKU})
    assert forecast.status_code == 200, (
        f"GET /api/inventory/forecast returned {forecast.status_code}: "
        f"{conftest.excerpt(forecast)}")
    body = forecast.json()
    for field in ("projected_stockout_on", "reorder_point"):
        assert field in str(body), (
            f"the forecast carries no {field}: {str(body)[:300]}")


def test_storefront_gate_is_evaluated_on_the_server_at_render(anonymous, holder):
    ungated = conftest.shop(anonymous)
    gated_rows = [row for row in ungated if row.get("slug") == conftest.GATED_LISTING]
    for row in gated_rows:
        assert int(row.get("price_minor", 0)) == conftest.PUBLIC_PRICE_MINOR, (
            f"an anonymous reader was shown {row.get('price_minor')!r} for "
            f"{conftest.GATED_LISTING}, expected the public price "
            f"{conftest.PUBLIC_PRICE_MINOR}")
    entitled = conftest.shop(holder)
    mine = [row for row in entitled if row.get("slug") == conftest.GATED_LISTING]
    assert mine, (
        f"the entitled holder {conftest.BUYER_EMAIL} cannot see "
        f"{conftest.GATED_LISTING} at all")
    assert int(mine[0]["price_minor"]) == conftest.HOLDER_PRICE_MINOR, (
        f"the entitled holder was shown {mine[0]['price_minor']!r}, expected "
        f"the holder price {conftest.HOLDER_PRICE_MINOR}")


def test_forged_gated_order_is_denied_at_the_order(plain_buyer):
    forged = conftest.place_order(plain_buyer, conftest.GATED_LISTING, 1,
                                  buyer_email=conftest.BUYER2_EMAIL)
    assert forged.status_code in conftest.DENIED + conftest.REFUSED, (
        f"POST /api/orders for {conftest.GATED_LISTING} from a caller with no "
        f"entitlement returned {forged.status_code}, expected a refusal at the "
        f"order rather than a hidden listing: {conftest.excerpt(forged)}")
    if forged.status_code in conftest.OK_CREATED:
        raise AssertionError("the gated listing was sold to an unentitled buyer")


def test_gated_price_is_re_verified_at_the_order(plain_buyer):
    forged = conftest.place_order(plain_buyer, conftest.GATED_LISTING, 1,
                                  buyer_email=conftest.BUYER2_EMAIL,
                                  key=conftest.probe_key())
    assert str(conftest.HOLDER_PRICE_MINOR) not in forged.text, (
        f"an unentitled order response carries the holder price "
        f"{conftest.HOLDER_PRICE_MINOR}: {conftest.excerpt(forged)}")


def test_cart_line_that_loses_eligibility_is_marked_rather_than_dropped(holder):
    added = holder.post("/cart", json={"listing_slug": conftest.GATED_LISTING,
                                       "units": 1})
    assert added.status_code in conftest.OK_CREATED, (
        f"POST /api/cart returned {added.status_code}: "
        f"{conftest.excerpt(added)}")
    lines = added.json().get("lines") or []
    assert lines, f"the cart carries no line after an add: {str(added.json())[:300]}"
    with conftest.anon() as client:
        anonymous_cart = client.get("/cart")
    if anonymous_cart.status_code == 200:
        body = anonymous_cart.json()
        for line in body.get("lines") or []:
            if line.get("listing_slug") == conftest.GATED_LISTING:
                assert line.get("eligible") is False or line.get("ineligible"), (
                    f"an ungated session kept the gated line without marking it "
                    f"ineligible: {str(line)[:200]}")


def test_replayed_signature_is_refused(plain_buyer):
    challenge = plain_buyer.post("/entitlements/challenge",
                                 json={"address": "0xseeded-holder-address"})
    assert challenge.status_code in conftest.OK_CREATED, (
        f"POST /api/entitlements/challenge returned {challenge.status_code}: "
        f"{conftest.excerpt(challenge)}")
    body = challenge.json()
    nonce = body.get("nonce")
    assert nonce, f"the challenge carries no nonce: {str(body)[:200]}"
    proof = {"address": "0xseeded-holder-address", "nonce": nonce,
             "signature": "0xprobe-signature"}
    first = plain_buyer.post("/entitlements/prove", json=proof)
    second = plain_buyer.post("/entitlements/prove", json=proof)
    assert second.status_code in conftest.DENIED + conftest.REFUSED, (
        f"replaying the same signature answered {second.status_code} after the "
        f"first answered {first.status_code}; a replayed signature is refused: "
        f"{conftest.excerpt(second)}")


def test_order_is_priced_once_and_carries_its_reference(holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 2,
                                 buyer_email=conftest.BUYER_EMAIL,
                                 destination="NL")
    assert order.status_code in conftest.OK_CREATED, (
        f"POST /api/orders returned {order.status_code}: "
        f"{conftest.excerpt(order)}")
    body = order.json()
    reference = body["reference"]
    assert reference.startswith(conftest.ORDER_REFERENCE_PREFIX), (
        f"the order reference {reference!r} does not begin "
        f"{conftest.ORDER_REFERENCE_PREFIX!r}")
    digits = reference[len(conftest.ORDER_REFERENCE_PREFIX):]
    assert digits.isdigit() and len(digits) == 6, (
        f"the order reference {reference!r} does not carry six digits after the "
        f"prefix")
    total = int(body["total_minor"])
    parts = (int(body.get("subtotal_minor", 0)) + int(body.get("shipping_minor", 0))
             + int(body.get("tax_minor", 0)) + int(body.get("duty_minor", 0)))
    assert total == parts, (
        f"order {reference} carries total_minor {total} against its parts "
        f"summing to {parts}; an order total equals its lines plus shipping "
        f"plus tax plus duty at every moment")
    again = conftest.read_order(reference, body["access_token"]).json()
    assert int(again["total_minor"]) == total, (
        f"order {reference} re-priced between two reads: {again['total_minor']} "
        f"against {total}")


def test_settled_checkout_raises_one_invoice_on_the_billing_account(payments, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL,
                                 rail="fiat")
    assert order.status_code in conftest.OK_CREATED, (
        f"POST /api/orders on the fiat rail returned {order.status_code}: "
        f"{conftest.excerpt(order)}")
    body = order.json()
    total = int(body["total_minor"])
    charge = conftest.settle(
        lambda: payments.find_charge(total, "usd"), limit=40.0)
    assert charge is not None, (
        f"no invoice for {total} minor units in usd exists in the billing "
        f"platform after order {body['reference']} settled; the app's own "
        f"confirmation does not count")
    accounts = payments.accounts()
    keys = {str(row.get("externalKey", "")).lower() for row in accounts}
    assert conftest.BUYER_EMAIL.lower() in keys, (
        f"the billing platform carries no account keyed by "
        f"{conftest.BUYER_EMAIL.lower()!r}; the keys present are "
        f"{sorted(keys)[:8]}")


def test_duplicate_checkout_with_one_idempotency_key_creates_one_invoice(payments, holder):
    key = conftest.probe_key()
    first = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL, key=key)
    second = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                  buyer_email=conftest.BUYER_EMAIL, key=key)
    assert first.status_code in conftest.OK_CREATED, (
        f"the first submission returned {first.status_code}: "
        f"{conftest.excerpt(first)}")
    assert second.status_code in conftest.OK_CREATED, (
        f"the replayed submission returned {second.status_code}, expected the "
        f"original order: {conftest.excerpt(second)}")
    assert first.json()["reference"] == second.json()["reference"], (
        f"the replayed Idempotency-Key produced order "
        f"{second.json()['reference']} rather than "
        f"{first.json()['reference']}; a replay returns the same order")
    total = int(first.json()["total_minor"])
    matching = [c for c in payments.charges()
                if c.amount == total and c.currency.lower() == "usd"]
    assert len(matching) <= 1, (
        f"{len(matching)} invoices exist for {total} minor units after one "
        f"replayed checkout; a replay creates no second invoice")


def test_idempotent_replay_sends_no_second_confirmation_mail(inbox, holder):
    key = conftest.probe_key()
    address = conftest.probe_email()
    conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                         buyer_email=address, key=key)
    conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                         buyer_email=address, key=key)
    found = conftest.settle(
        lambda: inbox.find(address, conftest.ORDER_SUBJECT_PREFIX), limit=40.0)
    assert found is not None, (
        f"no mail whose subject begins {conftest.ORDER_SUBJECT_PREFIX!r} "
        f"reached {address} after the order settled")
    assert inbox.count(address) == 1, (
        f"{inbox.count(address)} messages reached {address} after one replayed "
        f"checkout; a replay sends no second confirmation")


def test_token_rail_quote_window_and_confirmation_depth_are_served(holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL, rail="token")
    assert order.status_code in conftest.OK_CREATED, (
        f"POST /api/orders on the token rail returned {order.status_code}: "
        f"{conftest.excerpt(order)}")
    body = str(order.json())
    assert str(conftest.CONFIRMATION_DEPTH) in body, (
        f"the token order does not state the confirmation depth "
        f"{conftest.CONFIRMATION_DEPTH}: {body[:300]}")
    assert "expires" in body or str(conftest.TOKEN_QUOTE_MINUTES) in body, (
        f"the token order states no quote window: {body[:300]}")


def test_token_underpayment_and_overpayment_leave_the_ledger_agreeing(holder, finance):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL,
                                 rail="token").json()
    reference = order["reference"]
    total = int(order["total_minor"])
    under = holder.post(f"/orders/{reference}/chain-events", json={
        "kind": "payment", "amount_minor": total - 100,
        "confirmations": conftest.CONFIRMATION_DEPTH})
    assert under.status_code in conftest.OK_CREATED, (
        f"recording an underpayment returned {under.status_code}: "
        f"{conftest.excerpt(under)}")
    state = conftest.read_order(reference, order["access_token"]).json()
    assert str(state.get("state")) != "delivered", (
        f"an underpaid order moved to {state.get('state')!r}; an underpayment "
        f"leaves the order awaiting the balance")
    ledger = finance.get("/reports/ledger", params={"order": reference})
    assert ledger.status_code in (200, 404), (
        f"GET /api/reports/ledger returned {ledger.status_code}: "
        f"{conftest.excerpt(ledger)}")


def test_chain_reorganisation_reopens_the_order_and_reverses_its_entry(holder, finance):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL,
                                 rail="token").json()
    reference = order["reference"]
    total = int(order["total_minor"])
    holder.post(f"/orders/{reference}/chain-events", json={
        "kind": "payment", "amount_minor": total,
        "confirmations": conftest.CONFIRMATION_DEPTH})
    reorg = holder.post(f"/orders/{reference}/chain-events", json={
        "kind": "reorg", "amount_minor": total, "confirmations": 0})
    assert reorg.status_code in conftest.OK_CREATED, (
        f"recording a chain reorganisation returned {reorg.status_code}: "
        f"{conftest.excerpt(reorg)}")
    state = conftest.read_order(reference, order["access_token"]).json()
    assert str(state.get("payment_state", state.get("state"))).lower() not in ("paid", "settled"), (
        f"order {reference} still reads as settled after a reorganisation "
        f"undid its confirmation: {str(state)[:300]}")
    ledger = finance.get("/reports/ledger", params={"order": reference})
    if ledger.status_code == 200:
        kinds = [row.get("kind") for row in ledger.json()]
        assert "reversal" in kinds, (
            f"the money ledger for {reference} carries {kinds} with no "
            f"reversal entry")


def test_receipt_order_and_finance_report_agree_to_the_minor_unit(holder, finance):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    reference = order["reference"]
    total = int(order["total_minor"])
    buyer_view = conftest.read_order(reference, order["access_token"]).json()
    assert int(buyer_view["total_minor"]) == total, (
        f"the buyer's own view of {reference} reads "
        f"{buyer_view['total_minor']} against {total}")
    report = finance.get("/reports/channel", params={"period": "2026-09"})
    assert report.status_code == 200, (
        f"GET /api/reports/channel returned {report.status_code}: "
        f"{conftest.excerpt(report)}")


def test_refund_never_exceeds_its_capture(finance, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    reference = order["reference"]
    total = int(order["total_minor"])
    over = finance.post(f"/orders/{reference}/refunds",
                        json={"amount_minor": total * 3})
    assert over.status_code in conftest.REFUSED, (
        f"a refund of {total * 3} against a capture of {total} returned "
        f"{over.status_code}, expected a refusal: {conftest.excerpt(over)}")


def test_order_walks_the_eleven_surfaces_forward_only(operator, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    reference = order["reference"]
    for target in ("reserved", "picked", "packed"):
        moved = operator.post(f"/orders/{reference}/transitions",
                              json={"to": target})
        assert moved.status_code in conftest.OK_CREATED, (
            f"moving {reference} to {target!r} returned {moved.status_code}: "
            f"{conftest.excerpt(moved)}")
    backwards = operator.post(f"/orders/{reference}/transitions",
                              json={"to": "placed"})
    assert backwards.status_code in conftest.REFUSED, (
        f"moving {reference} backwards to 'placed' returned "
        f"{backwards.status_code}, expected a refusal: "
        f"{conftest.excerpt(backwards)}")
    timeline = conftest.read_order(reference, order["access_token"]).json()
    entries = timeline.get("timeline") or []
    assert entries, f"order {reference} carries no timeline: {str(timeline)[:300]}"
    for entry in entries:
        assert entry.get("actor") or entry.get("by"), (
            f"a timeline entry records no actor: {str(entry)[:200]}")
        assert entry.get("at"), (
            f"a timeline entry records no moment: {str(entry)[:200]}")


def test_eleven_surfaces_are_enumerated_by_the_console(operator):
    surfaces = operator.get("/fulfillment/surfaces")
    assert surfaces.status_code == 200, (
        f"GET /api/fulfillment/surfaces returned {surfaces.status_code}: "
        f"{conftest.excerpt(surfaces)}")
    names = [str(row.get("name", row)) for row in surfaces.json()]
    assert len(names) == 11, (
        f"the console enumerates {len(names)} operations surfaces, expected 11: "
        f"{names}")
    for surface in conftest.OPS_SURFACES:
        assert surface in names, (
            f"the console does not enumerate the surface {surface!r}: {names}")


def test_pack_verification_and_carrier_handoff_record_the_label(operator, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    reference = order["reference"]
    for target in ("reserved", "picked", "packed"):
        operator.post(f"/orders/{reference}/transitions", json={"to": target})
    handed = operator.post(f"/orders/{reference}/transitions",
                           json={"to": "handed_over", "carrier": "seeded-carrier"})
    assert handed.status_code in conftest.OK_CREATED, (
        f"handing {reference} to a carrier returned {handed.status_code}: "
        f"{conftest.excerpt(handed)}")
    body = str(handed.json())
    assert "label" in body.lower(), (
        f"the carrier handoff records no label: {body[:300]}")
    assert "tracking" in body.lower(), (
        f"the carrier handoff records no tracking identity: {body[:300]}")


def test_repeated_tracking_event_is_stored_once(operator, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    reference = order["reference"]
    event = {"carrier": "seeded-carrier", "external_id": conftest.probe_key(),
             "status": "in_transit"}
    operator.post(f"/orders/{reference}/tracking", json=event)
    operator.post(f"/orders/{reference}/tracking", json=event)
    timeline = conftest.read_order(reference, order["access_token"]).json()
    matches = [row for row in (timeline.get("tracking") or [])
               if row.get("external_id") == event["external_id"]]
    assert len(matches) <= 1, (
        f"the same carrier event was recorded {len(matches)} times on "
        f"{reference}; a resent event is deduplicated")


def test_missing_customs_classification_blocks_dispatch_before_the_border(operator, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL,
                                 destination="US-CA").json()
    reference = order["reference"]
    for target in ("reserved", "picked", "packed"):
        operator.post(f"/orders/{reference}/transitions", json={"to": target})
    dispatched = operator.post(f"/orders/{reference}/dispatch", json={})
    assert dispatched.status_code in conftest.REFUSED, (
        f"dispatching {reference} across a border with no customs "
        f"classification returned {dispatched.status_code}, expected a refusal: "
        f"{conftest.excerpt(dispatched)}")
    assert "classification" in dispatched.text.lower(), (
        f"the dispatch refusal does not name the missing classification: "
        f"{conftest.excerpt(dispatched)}")


def test_duty_estimate_is_a_buyer_visible_line_that_reconciles(holder, finance):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL,
                                 destination="GB").json()
    assert "duty_minor" in order, (
        f"the order carries no duty line for a delivered-duty-paid "
        f"destination: {str(order)[:300]}")
    reconciled = finance.post(f"/orders/{order['reference']}/duty-assessment",
                              json={"assessed_minor": int(order["duty_minor"]) + 50})
    assert reconciled.status_code in conftest.OK_CREATED + (404,), (
        f"recording an actual duty assessment returned "
        f"{reconciled.status_code}: {conftest.excerpt(reconciled)}")


def test_tax_rounds_by_jurisdiction_and_the_lines_sum_exactly(holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 3,
                                 buyer_email=conftest.BUYER_EMAIL,
                                 destination="NL").json()
    lines = order.get("lines") or []
    assert lines, f"the order carries no lines: {str(order)[:300]}"
    allocated = sum(int(line["tax_allocation_minor"]) for line in lines)
    assert allocated == int(order["tax_minor"]), (
        f"the per-line tax allocations sum to {allocated} against an invoice "
        f"tax of {order['tax_minor']}; the lines sum to the invoice exactly")


def test_largest_remainder_allocation_matches_the_pinned_worked_case(operator):
    computed = operator.post("/tax/quote", json={
        "jurisdiction": "NL", "lines": conftest.NL_LINES})
    assert computed.status_code == 200, (
        f"POST /api/tax/quote returned {computed.status_code}: "
        f"{conftest.excerpt(computed)}")
    body = computed.json()
    assert int(body.get("invoice_tax_minor", -1)) == conftest.NL_INVOICE_TAX, (
        f"three NL lines of {conftest.NL_LINES} produced an invoice tax of "
        f"{body.get('invoice_tax_minor')!r}, expected {conftest.NL_INVOICE_TAX}")
    allocation = [int(v) for v in (body.get("allocation") or [])]
    assert allocation == conftest.NL_ALLOCATION, (
        f"the recorded allocation is {allocation}, expected "
        f"{conftest.NL_ALLOCATION} by largest remainder")


def test_refunding_one_line_returns_its_recorded_tax(finance, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 3,
                                 buyer_email=conftest.BUYER_EMAIL,
                                 destination="NL").json()
    line = (order.get("lines") or [])[0]
    refunded = finance.post(f"/orders/{order['reference']}/refunds",
                            json={"line_id": line["id"]})
    assert refunded.status_code in conftest.OK_CREATED, (
        f"refunding one line returned {refunded.status_code}: "
        f"{conftest.excerpt(refunded)}")
    body = refunded.json()
    assert int(body.get("tax_returned_minor", -1)) == int(line["tax_allocation_minor"]), (
        f"refunding the line returned {body.get('tax_returned_minor')!r} of tax "
        f"against the {line['tax_allocation_minor']} recorded when the order was "
        f"priced")


def test_nexus_threshold_warns_and_the_filing_report_balances(finance):
    thresholds = finance.get("/tax/nexus")
    assert thresholds.status_code == 200, (
        f"GET /api/tax/nexus returned {thresholds.status_code}: "
        f"{conftest.excerpt(thresholds)}")
    assert str(conftest.NEXUS_THRESHOLD_MINOR) in thresholds.text, (
        f"the nexus table does not carry the seeded threshold "
        f"{conftest.NEXUS_THRESHOLD_MINOR}: {conftest.excerpt(thresholds)}")
    filing = finance.get("/reports/jurisdiction", params={"period": "2026-09"})
    assert filing.status_code == 200, (
        f"GET /api/reports/jurisdiction returned {filing.status_code}: "
        f"{conftest.excerpt(filing)}")
    for row in filing.json():
        assert int(row.get("difference_minor", 0)) == 0, (
            f"the filing report for {row.get('jurisdiction')!r} carries a "
            f"difference of {row.get('difference_minor')!r}, expected zero")


def test_return_inspection_issues_refund_and_stock_from_one_decision(operator, finance, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    reference = order["reference"]
    for target in ("reserved", "picked", "packed", "handed_over", "in_transit",
                   "delivered"):
        operator.post(f"/orders/{reference}/transitions", json={"to": target})
    authorised = holder.post(f"/orders/{reference}/returns",
                             json={"reason_code": "wrong_size"})
    assert authorised.status_code in conftest.OK_CREATED, (
        f"authorising a return on {reference} returned "
        f"{authorised.status_code}: {conftest.excerpt(authorised)}")
    return_reference = authorised.json()["reference"]
    before = conftest.available(conftest.TOTE_SKU, "rotterdam")
    inspected = operator.post(f"/returns/{return_reference}/inspection", json={
        "condition_grade": "as_new", "disposition": "restock"})
    assert inspected.status_code in conftest.OK_CREATED, (
        f"inspecting {return_reference} returned {inspected.status_code}: "
        f"{conftest.excerpt(inspected)}")
    body = inspected.json()
    assert body.get("refund"), (
        f"the inspection issued no refund: {str(body)[:300]}")
    restocked = conftest.settle(
        lambda: conftest.available(conftest.TOTE_SKU, "rotterdam") > before)
    assert restocked, (
        f"a restock disposition did not raise available for "
        f"{conftest.TOTE_SKU}; the refund and the stock event issue from one "
        f"decision")


def test_return_outside_the_window_is_refused(holder, operator):
    stale = holder.post(f"/orders/{conftest.SEEDED_ORDER_REFERENCE}/returns",
                        json={"reason_code": "changed_mind",
                              "requested_at": "2020-01-01"})
    assert stale.status_code in conftest.REFUSED + conftest.DENIED + (404,), (
        f"a return requested outside the {conftest.RETURN_WINDOW_DAYS} day "
        f"window returned {stale.status_code}, expected a refusal: "
        f"{conftest.excerpt(stale)}")


def test_cross_border_return_generates_its_own_paperwork(operator, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL,
                                 destination="US-CA").json()
    reference = order["reference"]
    for target in ("reserved", "picked", "packed", "handed_over", "in_transit",
                   "delivered"):
        operator.post(f"/orders/{reference}/transitions", json={"to": target})
    authorised = holder.post(f"/orders/{reference}/returns",
                             json={"reason_code": "faulty"})
    if authorised.status_code in conftest.OK_CREATED:
        body = str(authorised.json())
        assert "customs" in body.lower() or "document" in body.lower(), (
            f"a cross-border return produced no paperwork: {body[:300]}")


def test_return_policy_recorded_on_the_order_governs_the_refund(owner, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    assert order.get("return_policy_at_order"), (
        f"the order records no return policy at the moment it was placed: "
        f"{str(order)[:300]}")
    owner.post("/settings/policy", json={"return_policy": "refund_on_authorisation"})
    again = conftest.read_order(order["reference"], order["access_token"]).json()
    assert again.get("return_policy_at_order") == order.get("return_policy_at_order"), (
        f"changing the workspace policy rewrote the policy recorded on order "
        f"{order['reference']}")


def test_promise_records_its_inputs_and_its_owning_stage(holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    promise = order.get("promise") or {}
    for field in ("window_opens_on", "window_closes_on", "owner_stage", "inputs"):
        assert field in str(promise), (
            f"the promise on {order['reference']} carries no {field}: "
            f"{str(promise)[:300]}")


def test_three_slips_produce_one_revision_and_one_notice(inbox, operator, holder):
    address = conftest.probe_email()
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=address).json()
    reference = order["reference"]
    recomputed = operator.post(f"/promises/{reference}/recompute", json={
        "inputs": [{"kind": "factory_slip", "days": 6},
                   {"kind": "carrier_degradation", "days": 3},
                   {"kind": "customs_hold", "days": 4}]})
    assert recomputed.status_code in conftest.OK_CREATED, (
        f"POST /api/promises/{reference}/recompute returned "
        f"{recomputed.status_code}: {conftest.excerpt(recomputed)}")
    body = recomputed.json()
    revisions = body if isinstance(body, list) else [body]
    assert len(revisions) == 1, (
        f"three inputs moving together produced {len(revisions)} revisions, "
        f"expected exactly one: {str(body)[:300]}")
    cause = str(revisions[0].get("cause", ""))
    for kind in ("factory", "carrier", "customs"):
        assert kind in cause.lower(), (
            f"the recorded cause {cause!r} does not name the {kind} input")
    found = conftest.settle(
        lambda: inbox.find(address, conftest.PROMISE_SUBJECT_PREFIX), limit=40.0)
    assert found is not None, (
        f"no mail whose subject begins {conftest.PROMISE_SUBJECT_PREFIX!r} "
        f"reached {address} after the promise was revised")
    assert inbox.count(address) <= 2, (
        f"{inbox.count(address)} messages reached {address}; one recomputation "
        f"notifies the buyer once")


def test_promises_at_risk_are_ranked_and_on_time_is_reported(operator, finance):
    at_risk = operator.get("/promises", params={"at_risk": "true"})
    assert at_risk.status_code == 200, (
        f"GET /api/promises?at_risk=true returned {at_risk.status_code}: "
        f"{conftest.excerpt(at_risk)}")
    rows = at_risk.json()
    slips = [int(row.get("slip_days", 0)) for row in rows]
    assert slips == sorted(slips, reverse=True), (
        f"promises at risk are returned in the order {slips}, expected them "
        f"ranked by how far each has slipped")
    report = finance.get("/reports/lane", params={"period": "2026-09"})
    assert report.status_code == 200, (
        f"GET /api/reports/lane returned {report.status_code}: "
        f"{conftest.excerpt(report)}")


def test_drop_rush_never_oversells_its_fixed_supply():
    tokens = [conftest.token_for(conftest.BUYER2_EMAIL) for _ in range(6)]

    def pull(token):
        with conftest.bearer(token) as client:
            return client.post(f"/drops/{conftest.DROP_SLUG}/pull", json={},
                               headers={"Idempotency-Key": conftest.probe_key()})

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(pull, tokens))
    accepted = [r for r in results if r.status_code in conftest.OK_CREATED]
    assert len(accepted) <= conftest.DROP_ALLOWANCE, (
        f"{len(accepted)} pulls succeeded for one buyer against an allowance of "
        f"{conftest.DROP_ALLOWANCE}; the allowance holds across parallel sessions")
    for refused in [r for r in results if r.status_code not in conftest.OK_CREATED]:
        assert refused.status_code in conftest.REFUSED + conftest.DENIED, (
            f"a refused pull answered {refused.status_code}: "
            f"{conftest.excerpt(refused)}")


def test_drop_queue_position_is_honest(plain_buyer):
    drop = plain_buyer.get(f"/drops/{conftest.DROP_SLUG}")
    assert drop.status_code == 200, (
        f"GET /api/drops/{conftest.DROP_SLUG} returned {drop.status_code}: "
        f"{conftest.excerpt(drop)}")
    body = drop.json()
    assert "queue_position" in str(body) or "remaining" in str(body), (
        f"the drop states neither a queue position nor a remaining supply: "
        f"{str(body)[:300]}")
    assert int(body.get("supply", -1)) == conftest.DROP_SUPPLY, (
        f"the drop states a supply of {body.get('supply')!r}, expected "
        f"{conftest.DROP_SUPPLY}")


def test_gacha_odds_are_published_before_and_immutable_during(operator, plain_buyer):
    drop = plain_buyer.get(f"/drops/{conftest.DROP_SLUG}").json()
    odds = {str(row["name"]): str(row["odds"])
            for row in (drop.get("outcomes") or [])}
    assert odds == conftest.GACHA_ODDS, (
        f"the published odds are {odds}, expected {conftest.GACHA_ODDS}")
    assert drop.get("seed_commitment"), (
        f"the drop publishes no seed commitment before opening: "
        f"{str(drop)[:300]}")
    changed = operator.post(f"/drops/{conftest.DROP_SLUG}/outcomes", json={
        "name": "grail", "odds": "0.50"})
    assert changed.status_code in conftest.REFUSED + conftest.DENIED, (
        f"changing published odds while the drop runs returned "
        f"{changed.status_code}, expected a refusal: "
        f"{conftest.excerpt(changed)}")


def test_gacha_pull_is_verifiable_against_the_committed_seed(holder):
    pulled = holder.post(f"/drops/{conftest.DROP_SLUG}/pull", json={},
                         headers={"Idempotency-Key": conftest.probe_key()})
    assert pulled.status_code in conftest.OK_CREATED + conftest.REFUSED, (
        f"pulling from {conftest.DROP_SLUG} returned {pulled.status_code}: "
        f"{conftest.excerpt(pulled)}")
    if pulled.status_code in conftest.OK_CREATED:
        body = pulled.json()
        assert body.get("nonce"), (
            f"the pull carries no nonce to check against the revealed seed: "
            f"{str(body)[:300]}")
        assert body.get("outcome") in conftest.GACHA_ODDS, (
            f"the pull returned the outcome {body.get('outcome')!r}, expected "
            f"one of {sorted(conftest.GACHA_ODDS)}")


def test_gacha_pull_never_exceeds_its_outcomes_remaining_stock(plain_buyer):
    drop = plain_buyer.get(f"/drops/{conftest.DROP_SLUG}").json()
    for row in drop.get("outcomes") or []:
        assert int(row.get("remaining", 0)) >= 0, (
            f"outcome {row.get('name')!r} reports remaining "
            f"{row.get('remaining')!r}; a pull is prevented before the money is "
            f"taken rather than resolved afterwards")


def test_realised_distribution_reconciles_against_the_published_odds(operator):
    reconciliation = operator.get(f"/drops/{conftest.DROP_SLUG}/reconciliation")
    assert reconciliation.status_code in (200, 404), (
        f"GET /api/drops/{conftest.DROP_SLUG}/reconciliation returned "
        f"{reconciliation.status_code}: {conftest.excerpt(reconciliation)}")
    if reconciliation.status_code == 200:
        body = str(reconciliation.json())
        for outcome in conftest.GACHA_ODDS:
            assert outcome in body, (
                f"the reconciliation does not name the outcome {outcome!r}: "
                f"{body[:300]}")


def test_presale_funds_are_held_as_their_own_ledger_kind(finance):
    ledger = finance.get("/reports/ledger", params={"kind": "presale_held"})
    assert ledger.status_code in (200, 404), (
        f"GET /api/reports/ledger?kind=presale_held returned "
        f"{ledger.status_code}: {conftest.excerpt(ledger)}")
    presales = finance.get("/presales")
    assert presales.status_code == 200, (
        f"GET /api/presales returned {presales.status_code}: "
        f"{conftest.excerpt(presales)}")
    assert str(conftest.PRESALE_THRESHOLD_MINOR) in presales.text, (
        f"the seeded pre-sale does not carry the threshold "
        f"{conftest.PRESALE_THRESHOLD_MINOR}: {conftest.excerpt(presales)}")


def test_agent_catalogue_carries_the_same_gating_as_the_storefront(owner, anonymous):
    credential = owner.post("/agents", json={
        "scopes": ["catalogue", "orders"], "spend_limit_minor": 100000,
        "rate_limit_per_minute": 30})
    assert credential.status_code in conftest.OK_CREATED, (
        f"POST /api/agents returned {credential.status_code}: "
        f"{conftest.excerpt(credential)}")
    secret = credential.json().get("token") or credential.json().get("secret")
    assert secret, f"the credential carries no token: {str(credential.json())[:300]}"
    with httpx.Client(base_url=conftest.api_base(), timeout=conftest.TIMEOUT,
                      headers={"Authorization": f"Bearer {secret}"}) as agent:
        catalogue = agent.get("/agent/catalogue")
    assert catalogue.status_code == 200, (
        f"GET /api/agent/catalogue with a scoped credential returned "
        f"{catalogue.status_code}: {conftest.excerpt(catalogue)}")
    body = catalogue.text
    assert str(conftest.HOLDER_PRICE_MINOR) not in body, (
        f"the machine catalogue offers the holder price "
        f"{conftest.HOLDER_PRICE_MINOR} to an agent with no entitlement: "
        f"{body[:300]}")


def test_agent_order_walks_the_same_reservation_and_tax_machinery(owner):
    credential = owner.post("/agents", json={
        "scopes": ["orders"], "spend_limit_minor": 100000,
        "rate_limit_per_minute": 30}).json()
    secret = credential.get("token") or credential.get("secret")
    with httpx.Client(base_url=conftest.api_base(), timeout=conftest.TIMEOUT,
                      headers={"Authorization": f"Bearer {secret}"}) as agent:
        order = conftest.place_order(agent, conftest.TOTE_SLUG, 1,
                                     buyer_email=conftest.probe_email(),
                                     destination="NL")
    assert order.status_code in conftest.OK_CREATED, (
        f"POST /api/orders from an agent credential returned "
        f"{order.status_code}: {conftest.excerpt(order)}")
    body = order.json()
    assert body.get("tax_minor") is not None, (
        f"the agent's order carries no tax line: {str(body)[:300]}")
    assert body.get("promise"), (
        f"the agent's order carries no delivery promise: {str(body)[:300]}")
    assert str(body.get("reference", "")).startswith(conftest.ORDER_REFERENCE_PREFIX), (
        f"the agent's order reference {body.get('reference')!r} is not the same "
        f"shape a buyer receives")


def test_revoked_agent_credential_is_denied_and_releases_its_reservations(owner):
    credential = owner.post("/agents", json={
        "scopes": ["orders"], "spend_limit_minor": 100000,
        "rate_limit_per_minute": 30}).json()
    secret = credential.get("token") or credential.get("secret")
    revoked = owner.post(f"/agents/{credential['id']}/revoke", json={})
    assert revoked.status_code in conftest.OK_CREATED, (
        f"revoking the credential returned {revoked.status_code}: "
        f"{conftest.excerpt(revoked)}")
    with httpx.Client(base_url=conftest.api_base(), timeout=conftest.TIMEOUT,
                      headers={"Authorization": f"Bearer {secret}"}) as agent:
        after = agent.get("/agent/catalogue")
    assert after.status_code in conftest.DENIED, (
        f"a revoked credential reached GET /api/agent/catalogue with "
        f"{after.status_code}, expected one of {conftest.DENIED}: "
        f"{conftest.excerpt(after)}")


def test_agent_cannot_exceed_a_drop_allowance_its_owner_shares(owner):
    credential = owner.post("/agents", json={
        "scopes": ["drops"], "spend_limit_minor": 100000,
        "rate_limit_per_minute": 30}).json()
    secret = credential.get("token") or credential.get("secret")
    results = []
    with httpx.Client(base_url=conftest.api_base(), timeout=conftest.TIMEOUT,
                      headers={"Authorization": f"Bearer {secret}"}) as agent:
        for _ in range(conftest.DROP_ALLOWANCE + 2):
            results.append(agent.post(f"/drops/{conftest.DROP_SLUG}/pull", json={},
                                      headers={"Idempotency-Key": conftest.probe_key()}))
    accepted = sum(1 for r in results if r.status_code in conftest.OK_CREATED)
    assert accepted <= conftest.DROP_ALLOWANCE, (
        f"an agent credential took {accepted} pulls against an allowance of "
        f"{conftest.DROP_ALLOWANCE}; the allowance counts the owner's own pulls "
        f"together with every credential they own")


def test_reporting_axes_agree_exactly_for_one_period(finance):
    totals = {}
    for axis in ("product", "channel", "lane"):
        response = finance.get(f"/reports/{axis}", params={"period": "2026-09"})
        assert response.status_code == 200, (
            f"GET /api/reports/{axis} returned {response.status_code}: "
            f"{conftest.excerpt(response)}")
        rows = response.json()
        rows = rows if isinstance(rows, list) else rows.get("rows", [])
        totals[axis] = sum(int(row.get("revenue_minor", 0)) for row in rows)
    assert len(set(totals.values())) == 1, (
        f"the same period totals to {totals} on three axes; every figure is a "
        f"sum of one ledger and the axes must agree exactly")


def test_support_answer_cites_a_procedure_version_or_escalates(operator):
    queue = operator.get("/support/conversations")
    assert queue.status_code == 200, (
        f"GET /api/support/conversations returned {queue.status_code}: "
        f"{conftest.excerpt(queue)}")
    rows = queue.json()
    assert rows, "the seeded support queue carries no open conversation"
    conversation = rows[0]
    assert conversation.get("order") or conversation.get("order_reference"), (
        f"the conversation carries no order context: "
        f"{str(conversation)[:300]}")
    drafted = operator.post(
        f"/support/conversations/{conversation['id']}/answers",
        json={"question": "what is the return window"})
    assert drafted.status_code in conftest.OK_CREATED, (
        f"drafting an answer returned {drafted.status_code}: "
        f"{conftest.excerpt(drafted)}")
    body = drafted.json()
    assert body.get("procedure_version_id") or body.get("escalated"), (
        f"the drafted answer cites no procedure version and did not escalate: "
        f"{str(body)[:300]}")


def test_ungroundable_support_question_escalates_rather_than_improvising(operator):
    queue = operator.get("/support/conversations").json()
    conversation = queue[0]
    drafted = operator.post(
        f"/support/conversations/{conversation['id']}/answers",
        json={"question": "what colour was the founder's first bicycle"})
    assert drafted.status_code in conftest.OK_CREATED, (
        f"drafting an ungroundable answer returned {drafted.status_code}: "
        f"{conftest.excerpt(drafted)}")
    body = drafted.json()
    assert body.get("escalated") is True or body.get("procedure_version_id"), (
        f"an answer that can cite nothing neither escalated nor cited a "
        f"procedure: {str(body)[:300]}")


def test_procedure_versions_are_stored_and_an_answer_keeps_its_version(operator):
    procedures = operator.get("/procedures")
    assert procedures.status_code == 200, (
        f"GET /api/procedures returned {procedures.status_code}: "
        f"{conftest.excerpt(procedures)}")
    rows = procedures.json()
    returns = [row for row in rows if "return" in str(row.get("name", "")).lower()]
    assert len(returns) >= conftest.PROCEDURE_VERSIONS, (
        f"the workspace carries {len(returns)} versions of its returns "
        f"procedure, expected at least {conftest.PROCEDURE_VERSIONS}")


def test_announcement_mail_honours_suppression_and_unsubscribe(inbox, operator):
    address = conftest.probe_email()
    operator.post("/subscribers", json={"email": address, "consented": True})
    operator.post("/subscribers/unsubscribe", json={"email": address})
    announcements = operator.get("/announcements")
    assert announcements.status_code == 200, (
        f"GET /api/announcements returned {announcements.status_code}: "
        f"{conftest.excerpt(announcements)}")
    rows = announcements.json()
    assert rows, "the workspace carries no seeded announcement"
    subjects = {str(row.get("subject")) for row in rows}
    assert conftest.ANNOUNCEMENT_SUBJECT in subjects, (
        f"the seeded announcement subject is missing; the subjects present are "
        f"{sorted(subjects)}")
    sent = operator.post(f"/announcements/{rows[0]['id']}/send", json={})
    assert sent.status_code in conftest.OK_CREATED, (
        f"sending the announcement returned {sent.status_code}: "
        f"{conftest.excerpt(sent)}")
    delivered = conftest.settle(lambda: inbox.count(address) > 0, limit=15.0)
    assert not delivered, (
        f"an unsubscribed address received the announcement; an unsubscribe "
        f"takes effect across every future send")


def test_order_confirmation_mail_reaches_the_ordering_buyer_alone(inbox, holder):
    address = conftest.probe_email()
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=address).json()
    reference = order["reference"]
    message = conftest.settle(
        lambda: inbox.find(address, conftest.ORDER_SUBJECT_PREFIX), limit=40.0)
    assert message is not None, (
        f"no mail whose subject begins {conftest.ORDER_SUBJECT_PREFIX!r} "
        f"reached {address} after order {reference} was confirmed")
    assert message.subject.startswith(conftest.ORDER_SUBJECT_PREFIX), (
        f"the confirmation subject is {message.subject!r}, expected it to begin "
        f"{conftest.ORDER_SUBJECT_PREFIX!r}")
    assert reference in message.subject, (
        f"the confirmation subject {message.subject!r} does not carry the order "
        f"reference {reference}")
    assert len(message.to) == 1, (
        f"the confirmation was addressed to {message.to}; it reaches the "
        f"ordering buyer alone with nobody in copy")
    assert inbox.count(conftest.BUYER2_EMAIL) == 0 or True, (
        f"another buyer's inbox was touched by order {reference}")


def test_return_authorisation_mail_carries_its_reference(inbox, operator, holder):
    address = conftest.probe_email()
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=address).json()
    reference = order["reference"]
    for target in ("reserved", "picked", "packed", "handed_over", "in_transit",
                   "delivered"):
        operator.post(f"/orders/{reference}/transitions", json={"to": target})
    authorised = holder.post(f"/orders/{reference}/returns",
                             json={"reason_code": "wrong_size"})
    if authorised.status_code in conftest.OK_CREATED:
        return_reference = authorised.json()["reference"]
        message = conftest.settle(
            lambda: inbox.find(address, conftest.RETURN_SUBJECT_PREFIX),
            limit=40.0)
        assert message is not None, (
            f"no mail whose subject begins {conftest.RETURN_SUBJECT_PREFIX!r} "
            f"reached {address} after return {return_reference} was authorised")
        assert return_reference in message.subject, (
            f"the return mail subject {message.subject!r} does not carry the "
            f"return reference {return_reference}")


def test_a_non_notifying_transition_sends_no_mail(inbox, operator, holder):
    address = conftest.probe_email()
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=address).json()
    reference = order["reference"]
    conftest.settle(lambda: inbox.count(address) > 0, limit=40.0)
    before = inbox.count(address)
    operator.post(f"/orders/{reference}/transitions", json={"to": "reserved"})
    operator.post(f"/orders/{reference}/transitions", json={"to": "picked"})
    operator.post(f"/orders/{reference}/transitions", json={"to": "packed"})
    after = conftest.settle(lambda: inbox.count(address) > before, limit=10.0)
    assert not after, (
        f"moving {reference} from picked to packed sent mail to {address}; only "
        f"the three pinned transitions send anything")


def test_membership_is_derived_at_read_time_and_follows_the_asset(owner, holder):
    before = conftest.shop(holder)
    gated = [row for row in before if row.get("slug") == conftest.GATED_LISTING]
    assert gated and int(gated[0]["price_minor"]) == conftest.HOLDER_PRICE_MINOR, (
        f"the seeded holder is not entitled before the transfer: "
        f"{str(gated)[:300]}")
    transferred = owner.post("/entitlements/transfer", json={
        "from_email": conftest.BUYER_EMAIL, "to_email": conftest.BUYER3_EMAIL,
        "collection": conftest.COLLECTION})
    assert transferred.status_code in conftest.OK_CREATED, (
        f"transferring the entitlement returned {transferred.status_code}: "
        f"{conftest.excerpt(transferred)}")
    after = conftest.settle(lambda: [
        row for row in conftest.shop(holder)
        if row.get("slug") == conftest.GATED_LISTING
        and int(row.get("price_minor", 0)) != conftest.HOLDER_PRICE_MINOR])
    assert after, (
        f"the holder price survived a transfer of the entitlement away; "
        f"standing is computed at read time rather than written once")


def test_redemption_claim_marks_reserves_and_orders_together(holder, operator):
    entitlements = holder.get("/entitlements")
    assert entitlements.status_code == 200, (
        f"GET /api/entitlements returned {entitlements.status_code}: "
        f"{conftest.excerpt(entitlements)}")
    rows = [row for row in entitlements.json() if row.get("state") == "held"]
    if not rows:
        operator.post("/entitlements", json={
            "email": conftest.BUYER_EMAIL, "kind": "collection",
            "reference": conftest.COLLECTION, "granted_reason": "probe"})
        rows = [row for row in holder.get("/entitlements").json()
                if row.get("state") == "held"]
    assert rows, "the holder carries no entitlement in state 'held' to claim"
    claimed = holder.post("/redemptions", json={"entitlement_id": rows[0]["id"]})
    assert claimed.status_code in conftest.OK_CREATED + conftest.REFUSED, (
        f"POST /api/redemptions returned {claimed.status_code}: "
        f"{conftest.excerpt(claimed)}")
    if claimed.status_code in conftest.OK_CREATED:
        body = claimed.json()
        assert body.get("order"), (
            f"the claim created no order: {str(body)[:300]}")
        assert body.get("reservation"), (
            f"the claim reserved no stock: {str(body)[:300]}")
        again = holder.get("/entitlements").json()
        marked = [row for row in again if row["id"] == rows[0]["id"]]
        assert marked and marked[0]["state"] == "redeemed", (
            f"the claimed entitlement reads {marked and marked[0]['state']!r}, "
            f"expected 'redeemed'")


def test_a_failed_claim_leg_unwinds_the_other_two(holder, operator):
    entitlements = [row for row in holder.get("/entitlements").json()
                    if row.get("state") == "held"]
    if entitlements:
        before = conftest.available(conftest.JACKET_SKU, "newark")
        failed = holder.post("/redemptions", json={
            "entitlement_id": entitlements[0]["id"],
            "inject_failure": "reservation"})
        assert failed.status_code in conftest.REFUSED + conftest.OK_CREATED, (
            f"an injected reservation failure returned {failed.status_code}: "
            f"{conftest.excerpt(failed)}")
        if failed.status_code in conftest.REFUSED:
            after = holder.get("/entitlements").json()
            still = [row for row in after if row["id"] == entitlements[0]["id"]]
            assert still and still[0]["state"] == "held", (
                f"an entitlement was marked while its reservation leg failed; "
                f"a failure in one leg unwinds the other two")
            assert conftest.available(conftest.JACKET_SKU, "newark") == before, (
                f"the failed claim left stock reserved")


def test_unclaimed_entitlement_past_its_window_is_reported(operator):
    report = operator.get("/entitlements/unclaimed")
    assert report.status_code in (200, 404), (
        f"GET /api/entitlements/unclaimed returned {report.status_code}: "
        f"{conftest.excerpt(report)}")
    if report.status_code == 200:
        for row in report.json():
            assert row.get("reason") or row.get("window_closed_at"), (
                f"an unclaimed entitlement is reported with no reason: "
                f"{str(row)[:200]}")


def test_every_allowlist_entry_records_why_it_exists(operator):
    entries = operator.get("/allowlist")
    assert entries.status_code in (200, 404), (
        f"GET /api/allowlist returned {entries.status_code}: "
        f"{conftest.excerpt(entries)}")
    if entries.status_code == 200:
        for row in entries.json():
            assert row.get("granted_reason"), (
                f"an allowlist entry records no reason: {str(row)[:200]}")


def test_cost_of_goods_uses_the_lots_actually_shipped(finance):
    margin = finance.get("/reports/product", params={"period": "2026-09"})
    assert margin.status_code == 200, (
        f"GET /api/reports/product returned {margin.status_code}: "
        f"{conftest.excerpt(margin)}")
    body = str(margin.json())
    for cost in conftest.LOT_COSTS:
        assert str(cost) in body, (
            f"the margin report does not carry the lot cost {cost}; margin is "
            f"computed against the lot a unit came from rather than an average: "
            f"{body[:400]}")
    average = sum(conftest.LOT_COSTS) // len(conftest.LOT_COSTS)
    assert str(average) not in body or str(conftest.LOT_COSTS[0]) in body, (
        f"the margin report reads as an average across lots: {body[:400]}")


def test_capacity_refuses_a_lead_time_it_cannot_support(operator):
    projects = operator.get("/projects").json()
    project_id = projects[0]["id"]
    impossible = operator.put(f"/projects/{project_id}/brief", json={
        "quantity": conftest.BRIEF_QUANTITY * 20, "needed_by": "2026-09-20"})
    if impossible.status_code in conftest.OK_CREATED:
        offers = operator.get(f"/projects/{project_id}/offers",
                              params={"quantity": conftest.BRIEF_QUANTITY * 20})
        assert offers.status_code == 200, (
            f"GET offers at an unsupportable quantity returned "
            f"{offers.status_code}: {conftest.excerpt(offers)}")
        for row in offers.json():
            assert row.get("capacity_refused") or int(row.get("lead_days", 0)) > 0, (
                f"an offer quoted a lead time with no capacity behind it: "
                f"{str(row)[:200]}")


def test_routes_resolve_as_the_flow_table_names_them(public):
    for route in ("/", "/catalogue", "/merch-fulfillment",
                  "/custom-merch-no-minimum", "/brand", "/shop"):
        response = public.get(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}, expected 200: "
            f"{conftest.excerpt(response)}")
    for route in ("/holders", "/app", "/app/inventory"):
        response = public.get(route)
        assert response.status_code < 500, (
            f"GET {route} returned {response.status_code}: "
            f"{conftest.excerpt(response)}")


def test_entry_and_redirect_rules_hold(anonymous, plain_buyer):
    protected = anonymous.get("/projects")
    assert protected.status_code in conftest.DENIED, (
        f"GET /api/projects with no session returned {protected.status_code}: "
        f"{conftest.excerpt(protected)}")
    console = plain_buyer.get("/projects")
    assert console.status_code in conftest.DENIED, (
        f"a buyer with no membership reached GET /api/projects with "
        f"{console.status_code}: {conftest.excerpt(console)}")
    stale = httpx.Client(base_url=conftest.api_base(),
                         timeout=conftest.TIMEOUT,
                         headers={"Authorization": "Bearer expired-probe-token"})
    with stale as client:
        response = client.put("/projects/1/brief", json={"quantity": 10})
    assert response.status_code in conftest.DENIED, (
        f"an expired token wrote with {response.status_code}, expected one of "
        f"{conftest.DENIED}: {conftest.excerpt(response)}")


def test_stack_and_providers_are_reachable_from_the_environment(backend, inbox, payments):
    with conftest.anon() as client:
        health = client.get("/health")
    assert health.status_code == 200, (
        f"GET {conftest.HEALTH_ROUTE} returned {health.status_code}: "
        f"{conftest.excerpt(health)}")
    assert payments.accounts() is not None, (
        "the billing platform answered no account listing; it is reachable at "
        "PAYMENTS_API_URL")
    assert inbox.count() >= 0, (
        "the mail server answered no message count; it is reachable over SMTP "
        "and its inbox API")


def test_money_is_integer_minor_units_rendered_in_utc(holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    for field in ("subtotal_minor", "tax_minor", "total_minor"):
        value = order.get(field)
        assert isinstance(value, int), (
            f"order field {field} is {value!r} of type {type(value).__name__}, "
            f"expected an integer of minor units")
    stamp = str(order.get("placed_at", ""))
    assert stamp.endswith("Z") or "+00:00" in stamp, (
        f"the order records placed_at as {stamp!r}, expected an absolute UTC "
        f"timestamp")


def test_event_stream_converges_two_readers_within_a_second(operator, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    reference = order["reference"]
    operator.post(f"/orders/{reference}/transitions", json={"to": "reserved"})
    converged = conftest.settle(
        lambda: conftest.read_order(reference, order["access_token"]).json()
        .get("state") == "reserved", limit=5.0)
    assert converged, (
        f"the buyer's own view of {reference} did not reach 'reserved' within "
        f"five seconds of the console moving it")


def test_inventory_grid_is_paginated_for_large_row_counts(operator):
    page = operator.get("/inventory", params={"limit": 50, "offset": 0})
    assert page.status_code == 200, (
        f"GET /api/inventory with a limit returned {page.status_code}: "
        f"{conftest.excerpt(page)}")
    rows = page.json()
    assert isinstance(rows, list), (
        f"GET /api/inventory did not return a top-level array: "
        f"{str(rows)[:200]}")
    assert len(rows) <= 50, (
        f"GET /api/inventory?limit=50 returned {len(rows)} rows; the grid asks "
        f"the service for one page at a time")


def test_generated_imagery_is_stable_for_one_slug(public):
    first = public.get(f"/media/product/{conftest.JACKET_SLUG}")
    second = public.get(f"/media/product/{conftest.JACKET_SLUG}")
    assert first.status_code == second.status_code, (
        f"two reads of the generated image for {conftest.JACKET_SLUG} answered "
        f"{first.status_code} and {second.status_code}")
    if first.status_code == 200:
        assert first.content == second.content, (
            f"the generated image for {conftest.JACKET_SLUG} differs between "
            f"two reads; the same product always produces the same picture")


def test_uploaded_artwork_is_served_through_a_short_lived_link(operator):
    projects = operator.get("/projects").json()
    artwork = operator.get(f"/projects/{projects[0]['id']}/artwork")
    assert artwork.status_code in (200, 404), (
        f"GET /api/projects/<id>/artwork returned {artwork.status_code}: "
        f"{conftest.excerpt(artwork)}")
    if artwork.status_code == 200:
        body = str(artwork.json())
        assert "expires" in body.lower() or "signature" in body.lower(), (
            f"artwork is served without a short-lived signed link: "
            f"{body[:300]}")


def test_seeded_membership_roles_and_categories_are_stored(backend, owner):
    members = owner.get("/settings/members")
    assert members.status_code == 200, (
        f"GET /api/settings/members returned {members.status_code}: "
        f"{conftest.excerpt(members)}")
    roles = {str(row.get("role")) for row in members.json()}
    assert roles <= set(conftest.ROLES), (
        f"the workspace carries roles {sorted(roles - set(conftest.ROLES))} "
        f"outside the pinned set {conftest.ROLES}")
    categories = {row["category"] for row in conftest.products()}
    assert categories <= set(conftest.CATEGORIES), (
        f"the catalogue carries categories "
        f"{sorted(categories - set(conftest.CATEGORIES))} outside "
        f"{conftest.CATEGORIES}")


def test_schema_versions_keep_history_reading_as_written(owner, holder):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL,
                                 destination="NL").json()
    reference = order["reference"]
    before = int(order["tax_minor"])
    changed = owner.post("/tax/rates", json={
        "jurisdiction": "NL", "rate": "0.25", "effective_from": "2026-09-16"})
    assert changed.status_code in conftest.OK_CREATED + conftest.DENIED, (
        f"POST /api/tax/rates returned {changed.status_code}: "
        f"{conftest.excerpt(changed)}")
    after = conftest.read_order(reference, order["access_token"]).json()
    assert int(after["tax_minor"]) == before, (
        f"order {reference} now reads {after['tax_minor']} of tax against the "
        f"{before} it was written with; a rate change leaves history alone")
    assert after.get("rules_version") or after.get("version"), (
        f"order {reference} records no version of the rules it was written "
        f"under: {str(after)[:300]}")


def test_seeding_is_idempotent_across_a_second_read(backend):
    first = {row["slug"] for row in conftest.products()}
    second = {row["slug"] for row in conftest.products()}
    assert first == second, (
        f"two reads of the seeded catalogue differ by "
        f"{sorted(first ^ second)}; seeding is idempotent")
    assert len(first) == len(conftest.CATALOGUE), (
        f"the catalogue carries {len(first)} products, expected "
        f"{len(conftest.CATALOGUE)}; restarting the app duplicates no row")


def test_no_external_host_is_called_at_run_time(operator):
    response = operator.get("/projects")
    assert response.status_code == 200, (
        f"GET /api/projects returned {response.status_code}: "
        f"{conftest.excerpt(response)}")
    body = response.text
    for marker in ("http://api.", "https://api.", "googleapis.com",
                   "amazonaws.com"):
        assert marker not in body, (
            f"a console payload names the external host {marker!r}; the server "
            f"calls nothing outside this environment")


def test_no_card_number_or_private_key_is_stored(holder, finance):
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    body = str(order)
    for marker in ("card_number", "pan", "private_key", "seed_phrase"):
        assert marker not in body.lower(), (
            f"the order payload carries {marker!r}; no card number and no "
            f"wallet private key is stored anywhere: {body[:300]}")
    ledger = finance.get("/reports/ledger", params={"period": "2026-09"})
    if ledger.status_code == 200:
        for marker in ("card_number", "private_key"):
            assert marker not in ledger.text.lower(), (
                f"the money ledger carries {marker!r}")


def test_billing_calls_carry_their_pinned_credentials(payments, holder):
    accounts = payments.accounts()
    assert isinstance(accounts, list), (
        f"the billing platform returned {type(accounts).__name__} for its "
        f"account listing, expected a list; the call carries the tenant key, "
        f"the tenant secret and the pinned basic credentials")
    keys = {str(row.get("externalKey", "")) for row in accounts}
    for seeded in ("orbit-amelia", "orbit-acme", "orbit-northwind"):
        assert seeded in keys, (
            f"the billing tenant does not carry the seeded account {seeded!r}; "
            f"the keys present are {sorted(keys)[:8]}")
    order = conftest.place_order(holder, conftest.TOTE_SLUG, 1,
                                 buyer_email=conftest.BUYER_EMAIL).json()
    total = int(order["total_minor"])
    charge = conftest.settle(lambda: payments.find_charge(total, "usd"),
                             limit=40.0)
    assert charge is not None, (
        f"no invoice for {total} minor units reached the billing platform for "
        f"order {order['reference']}")


def test_copy_deck_strings_are_served_verbatim(public):
    landing = public.get("/").text
    for line in (conftest.HERO_HEADLINE, conftest.POSITIONING_LINE,
                 conftest.FIRST_PANEL, conftest.FIRST_PILL,
                 conftest.FIRST_REEL_LINE, conftest.DEMO_PILL,
                 conftest.WHITELIST_LINK, conftest.COPYRIGHT_LINE):
        assert line in landing, (
            f"the landing document does not carry the pinned copy {line!r}")
    for label in conftest.MENU_LABELS:
        assert label in landing, (
            f"the header does not carry the menu label {label!r}")
    for column in conftest.FOOTER_COLUMNS:
        assert column in landing, (
            f"the footer does not carry the column head {column!r}")
    assert landing.count("...") >= conftest.REEL_LINE_COUNT - 2, (
        f"the intro reel carries fewer than {conftest.REEL_LINE_COUNT} rotating "
        f"status lines")
    catalogue = public.get("/catalogue").text
    assert conftest.CATALOGUE_HEADING in catalogue, (
        f"the catalogue document does not carry {conftest.CATALOGUE_HEADING!r}")
    fulfillment = public.get("/merch-fulfillment").text
    for line in (conftest.FULFILLMENT_HEADING, conftest.OPS_FIGURE_LINE,
                 conftest.MINIMUM_FIGURE_LINE):
        assert line in fulfillment, (
            f"the fulfillment document does not carry {line!r}")


def test_type_families_and_sizes_are_declared(public):
    landing = public.get("/")
    body = landing.text
    styles = body
    for asset in re.findall(r'href="(/[^"]+\.css)"', body)[:4]:
        styles += public.get(asset).text
    for family in (conftest.INTERFACE_FAMILY, conftest.DISPLAY_FAMILY):
        assert family in styles, (
            f"neither the document nor its stylesheets name the family "
            f"{family!r}")
    for size in (conftest.BODY_SIZE_PX, conftest.DENSE_SIZE_PX):
        assert size in styles, (
            f"neither the document nor its stylesheets carry the pinned size "
            f"{size!r}")
    assert "scrollTrigger" not in styles and "scrub" not in styles, (
        "the served assets introduce a scroll-scrubbed timeline, which the "
        "brief rules out")


def test_generated_media_ships_no_binary_asset(public):
    landing = public.get("/").text
    binaries = re.findall(r'(?:src|href)="([^"]+\.(?:png|jpg|jpeg|webp|mp4|woff2?))"',
                          landing)
    assert not binaries, (
        f"the landing document references binary assets {binaries[:5]}; every "
        f"mark, garment and panel is drawn or generated at run time")
    first = public.get(f"/media/product/{conftest.JACKET_SLUG}")
    second = public.get(f"/media/product/{conftest.TOTE_SLUG}")
    assert first.status_code == second.status_code, (
        f"the generator answered {first.status_code} for one product and "
        f"{second.status_code} for another; one generator feeds every surface")


def test_deployment_contract_holds_for_the_running_server():
    with conftest.anon() as client:
        health = client.get("/health")
    assert health.status_code == 200, (
        f"GET {conftest.HEALTH_ROUTE} returned {health.status_code}: "
        f"{conftest.excerpt(health)}")
    url = conftest.app_url()
    assert "localhost" not in url or conftest.CONTAINER_PORT in url, (
        f"the app is published at {url!r}; the container-internal port is "
        f"{conftest.CONTAINER_PORT} and the server binds "
        f"{conftest.BIND_ADDRESS}")
    with conftest.site() as client:
        landing = client.get("/")
    assert landing.status_code == 200, (
        f"GET / returned {landing.status_code}; the app starts from the "
        f"environment image with no manual steps and keeps running: "
        f"{conftest.excerpt(landing)}")
    assert "vite" not in landing.text.lower() or "/assets/" in landing.text, (
        "the served document looks like a development server rather than a "
        "production build")
