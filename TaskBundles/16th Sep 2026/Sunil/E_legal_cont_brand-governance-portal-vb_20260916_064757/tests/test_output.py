from __future__ import annotations

import pathlib
import threading
from concurrent.futures import ThreadPoolExecutor

import httpx

import appclient
from conftest import (
    APPLICATION_CLASSES, ASSET_CLASSES, ASSET_TABLES, AUDIT_TABLES,
    AVAILABILITY_BADGES, CHAPTER_SLUGS, CHAPTER_TABLES, CHAPTER_TITLES,
    CONSENT_CONTROL, CONSENT_TABLES, DOWNLOAD_TABLES, EMPLOYEE,
    FOOTER_DESTINATIONS, FRAME_HEADERS, FRAMEWORK_PRINCIPLES, GRANT_TABLES,
    ICON_DIMENSIONS, MARK_EXPRESSIONS, OUTRO_DESTINATIONS, OWNING_STUDIO,
    PARTNER, PARTNER_ENGAGEMENT_END, PARTNER_GRANTED_CLASSES, PARTNER_SECOND,
    PARTNER_STUDIO, PASSWORD, PRINCIPAL_TABLES, PUBLIC_ROUTES, REQUEST_STATES,
    REQUEST_TABLES, RESERVED_ROUTES, REVIEWER, REVIEWER_SECOND,
    SECURITY_HEADERS, SEEDED_PRINCIPALS, STAGE_TABLES, STATEMENT_IDENTIFIER,
    WORKED_CAMPAIGN_END, asset_detail, asset_of_class, assets, audit, chapters,
    decide, describe, download, future_date, grants,
    holder_of, iso, json_list, now_utc, open_stage_ids, page, parse_date,
    poll_until, probe_token, queue, raw_page, read_request, resolve_table,
    settle, stage_holders, stage_ids, submit_request, withdraw_request,
)


def test_seeded_principals_and_assets_persisted_and_idempotent(backend, anon):
    """Every seeded principal, chapter and asset exists exactly once."""
    principals = resolve_table(backend, PRINCIPAL_TABLES)
    for email in SEEDED_PRINCIPALS:
        seen = backend.count(principals, email=email)
        assert seen == 1, (
            f"the seeded principal {email} appears {seen} times in {principals}; "
            f"seeding must leave exactly one row per principal")
        assert appclient.login(email, PASSWORD), (
            f"the corpus password does not sign {email} in")

    chapter_table = resolve_table(backend, CHAPTER_TABLES)
    for slug in CHAPTER_SLUGS:
        seen = backend.count(chapter_table, slug=slug)
        assert seen == 1, (
            f"the chapter {slug!r} appears {seen} times in {chapter_table}; a slug "
            f"is unique and an unguarded reseed is what duplicates it")

    asset_table = resolve_table(backend, ASSET_TABLES)
    total = backend.count(asset_table)
    assert total >= len(ASSET_CLASSES), (
        f"{asset_table} holds {total} rows; the seed must carry at least one asset "
        f"for each of the {len(ASSET_CLASSES)} asset classes")

    with _employee_session() as session:
        served = assets(session)
    classes_served = {row.get("asset_class") for row in served}
    missing = [name for name in ASSET_CLASSES if name not in classes_served]
    assert not missing, (
        f"the library serves no asset of class {missing}; every asset class needs a "
        f"seeded asset so its rules can be exercised")

    marks = [row for row in served if row.get("asset_class") == "mark"]
    assert len(marks) >= 2, (
        f"only {len(marks)} mark asset(s) are served; the mark is seeded in both "
        f"permitted expressions {list(MARK_EXPRESSIONS)}")

    retired = [row for row in served if row.get("availability") == "Retired"]
    assert retired, (
        "no asset is seeded with availability Retired, so the retirement rules "
        "cannot be exercised")


def _employee_session() -> httpx.Client:
    return appclient.client(appclient.login(EMPLOYEE, PASSWORD))


def test_app_contract_artifacts_present():
    """The App Contract's reserved directories and credentials file exist."""
    root = pathlib.Path("/app")
    readme = root / "USER_README.md"
    assert readme.is_file(), (
        "/app/USER_README.md is missing; the App Contract requires the login "
        "credentials, or an explicit statement that there are none, to be written "
        "there")
    text = readme.read_text(encoding="utf-8", errors="replace")
    assert text.strip(), "/app/USER_README.md exists but is empty"

    for name in (".browser_screenshots", ".downloads"):
        target = root / name
        assert target.is_dir(), (
            f"/app/{name}/ is missing; the App Contract reserves it at the app root")
        assert not any(target.iterdir()), (
            f"/app/{name}/ is not empty; the App Contract reserves it empty")


def test_health_endpoint_reports_database_and_object_store(anon):
    """Readiness names the database state apart from the object store state."""
    response = anon.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health did not answer 200 once the app is ready: "
        f"{describe(response)}")
    body = response.text.lower()
    assert "postgres" in body or "database" in body or "db" in body, (
        f"GET /api/health does not report the database: {response.text[:400]}. A "
        f"readiness answer from the web layer alone cannot tell a degraded run from "
        f"a healthy one")
    assert "minio" in body or "storage" in body or "object" in body, (
        f"GET /api/health does not report the object store: {response.text[:400]}")


def test_collection_endpoints_answer_top_level_arrays(anon):
    """Every collection answers a top-level JSON array."""
    json_list(anon.get("/chapters"), "GET /api/chapters")
    employee = _employee_session()
    with employee:
        json_list(employee.get("/assets"), "GET /api/assets")
        json_list(employee.get("/requests"), "GET /api/requests")
        json_list(employee.get("/grants"), "GET /api/grants")


def test_seeded_login_returns_access_token(anon):
    """A provisioned principal signs in and receives a bearer token."""
    for email in SEEDED_PRINCIPALS:
        response = httpx.post(f"{appclient.api_base()}/auth/login",
                              json={"email": email, "password": PASSWORD},
                              timeout=appclient.TIMEOUT)
        assert response.status_code == 200, (
            f"login for the seeded principal {email} did not answer 200: "
            f"{describe(response)}")
        token = response.json().get("access_token")
        assert token, (
            f"login for {email} answered 200 with no access_token: "
            f"{response.text[:400]}")

    with appclient.client(appclient.login(EMPLOYEE, PASSWORD)) as session:
        assert session.get("/assets").status_code == 200, (
            "the token returned by login does not authorise the library")


def test_failed_signin_returns_no_token_without_disclosing_the_address(anon):
    """An unknown address and a wrong password answer in one shape."""
    unknown = httpx.post(f"{appclient.api_base()}/auth/login",
                         json={"email": f"nobody-{probe_token()}@example.com",
                               "password": PASSWORD},
                         timeout=appclient.TIMEOUT)
    wrong = httpx.post(f"{appclient.api_base()}/auth/login",
                       json={"email": EMPLOYEE, "password": "not-the-password"},
                       timeout=appclient.TIMEOUT)

    for label, response in (("an unknown address", unknown),
                            ("a wrong password", wrong)):
        assert 400 <= response.status_code < 500, (
            f"a failed sign in with {label} answered {response.status_code}; a "
            f"refusal is a client error: {describe(response)}")
        assert "access_token" not in response.text, (
            f"a failed sign in with {label} returned an access_token: "
            f"{response.text[:300]}")

    assert unknown.status_code == wrong.status_code, (
        f"an unknown address answered {unknown.status_code} and a wrong password "
        f"answered {wrong.status_code}; answering them differently turns the sign in "
        f"form into a list of who exists")


def test_no_route_creates_a_principal(anon, backend):
    """Signup is closed: no route creates an account."""
    principals = resolve_table(backend, PRINCIPAL_TABLES)
    before = backend.count(principals)
    probe = f"intruder-{probe_token()}@example.com"

    for path in ("/auth/signup", "/auth/register", "/principals", "/users",
                 "/auth/signup/"):
        response = anon.post(path, json={"email": probe, "password": PASSWORD,
                                         "display_name": "Intruder"})
        assert response.status_code != 200 and response.status_code != 201, (
            f"POST /api{path} created something and answered "
            f"{response.status_code}; signup is closed and every principal is "
            f"provisioned: {describe(response)}")

    after = backend.count(principals)
    assert after == before, (
        f"{principals} grew from {before} to {after} rows after the signup probes; "
        f"no path may create a principal")
    assert backend.count(principals, email=probe) == 0, (
        f"the probe address {probe} was created despite signup being closed")


def test_hub_and_eight_chapter_routes_answer_anonymously(anon):
    """All nine public routes render without a credential."""
    for route in PUBLIC_ROUTES:
        response = page(route)
        assert response.status_code == 200, (
            f"the public route {route} did not answer 200 without an account: "
            f"{describe(response)}")
        assert response.text.strip(), (
            f"the public route {route} answered 200 with an empty body")

    served = chapters(anon)
    slugs = [row.get("slug") for row in served]
    for slug in CHAPTER_SLUGS:
        assert slug in slugs, (
            f"the chapter {slug!r} is absent from GET /api/chapters, which served "
            f"{slugs}")

    logo = page("/logo")
    for expression in MARK_EXPRESSIONS:
        assert expression in logo.text, (
            f"the logo chapter does not carry the expression label {expression!r}")

    framework = page("/framework")
    for principle in FRAMEWORK_PRINCIPLES:
        assert principle in framework.text, (
            f"the framework chapter does not publish the principle {principle!r}")

    for destination in OUTRO_DESTINATIONS + FOOTER_DESTINATIONS:
        assert destination in logo.text, (
            f"the chapter outro or footer does not carry {destination!r}; every "
            f"public route closes with the same three destinations and six footer "
            f"links")

    for credit in (OWNING_STUDIO, PARTNER_STUDIO):
        assert credit in page("/").text, (
            f"the hub does not credit {credit!r} on its outro")


def test_reserved_addresses_answer_the_product_not_found_page(anon):
    """A reserved or unknown address answers the product's own page at 404."""
    unknown = f"/{probe_token()}-not-a-chapter"
    for route in RESERVED_ROUTES + (unknown,):
        response = raw_page(route)
        assert response.status_code == 404, (
            f"the reserved address {route} answered {response.status_code} rather "
            f"than 404; a guideline address that quietly becomes a different "
            f"guideline is a governance failure: {describe(response)}")
        body = response.text
        assert body.strip(), (
            f"{route} answered 404 with an empty body rather than the product's own "
            f"designed page")
        named = [slug for slug in CHAPTER_SLUGS if slug in body]
        assert len(named) >= 4, (
            f"the not-found page at {route} names only {named}; it must carry the "
            f"chapter menu as the way back rather than a framework default")


def test_chapter_order_matches_the_stored_display_field(anon, backend):
    """The served chapter order follows the stored display order."""
    served = chapters(anon)
    assert served, "GET /api/chapters served no chapters"
    table = resolve_table(backend, CHAPTER_TABLES)
    rows = backend.rows(table)
    assert rows, f"{table} holds no chapter rows"

    order_field = None
    for candidate in ("display_order", "order", "position", "sort_order", "rank"):
        if candidate in rows[0]:
            order_field = candidate
            break
    assert order_field, (
        f"no display order column is stored on {table}; the row keys are "
        f"{sorted(rows[0])}. The chapter order is an editorial decision held on the "
        f"record rather than fixed in the page")

    stored = [row["slug"] for row in
              sorted(rows, key=lambda row: row[order_field]) if row.get("slug")]
    served_slugs = [row.get("slug") for row in served]
    assert served_slugs == stored, (
        f"GET /api/chapters served {served_slugs} but the stored display order is "
        f"{stored}; the served order must follow the record")

    hub = page("/").text
    positions = [hub.find(CHAPTER_TITLES[slug]) for slug in stored
                 if CHAPTER_TITLES[slug] in hub]
    assert positions == sorted(positions), (
        f"the hub renders the chapter titles out of the stored order; the hub, the "
        f"menu overlay and the outro all repeat one order")


def test_chapter_statements_carry_stable_identifiers(anon):
    """Every published statement carries an identifier a request can cite."""
    found = {}
    for slug in CHAPTER_SLUGS:
        response = anon.get(f"/chapters/{slug}")
        assert response.status_code == 200, (
            f"GET /api/chapters/{slug} did not answer 200: {describe(response)}")
        payload = response.json()
        statements = (payload.get("statements")
                      or (payload.get("version") or {}).get("statements") or [])
        assert statements, (
            f"the chapter {slug!r} publishes no statements; a rule a request cites "
            f"has to exist as a record: {response.text[:400]}")
        for statement in statements:
            identifier = (statement.get("statement_id") or statement.get("id")
                          or statement.get("identifier"))
            assert identifier, (
                f"a statement on {slug!r} carries no identifier: {statement}")
            assert str(identifier).startswith(f"{slug}."), (
                f"the statement identifier {identifier!r} on {slug!r} is not shaped "
                f"<chapter-slug>.<section>.<n>")
            found[str(identifier)] = slug

    assert STATEMENT_IDENTIFIER in found, (
        f"the logo chapter does not publish the statement {STATEMENT_IDENTIFIER!r}; "
        f"it served {sorted(k for k in found if k.startswith('logo.'))}")


def test_reserved_slug_is_refused_at_chapter_creation(anon, backend):
    """A chapter created under a reserved slug is refused."""
    table = resolve_table(backend, CHAPTER_TABLES)
    reserved = ("library", "asset", "requests", "queue", "admin", "studio", "api",
                "auth", "health", "2", "as", "gs")
    reviewer_session = appclient.client(appclient.login(REVIEWER, PASSWORD))
    with reviewer_session:
        for slug in reserved:
            before = backend.count(table, slug=slug)
            response = reviewer_session.post("/chapters", json={
                "slug": slug, "title": "Intruder", "display_order": 99})
            assert response.status_code not in (200, 201), (
                f"creating a chapter under the reserved slug {slug!r} answered "
                f"{response.status_code}; the slug namespace is closed against it: "
                f"{describe(response)}")
            assert backend.count(table, slug=slug) == before, (
                f"a chapter row was written for the reserved slug {slug!r}")


def test_public_route_titles_are_unique_per_route(anon):
    """Every public route carries its own title."""
    titles = {}
    for route in PUBLIC_ROUTES:
        response = page(route)
        body = response.text
        start = body.lower().find("<title")
        assert start != -1, f"the public route {route} declares no title element"
        open_end = body.find(">", start)
        close = body.lower().find("</title>", open_end)
        title = body[open_end + 1:close].strip()
        assert title, f"the public route {route} declares an empty title"
        assert title not in titles, (
            f"{route} and {titles[title]} share the title {title!r}; every public "
            f"route carries a title unique to that route")
        titles[title] = route


def test_every_internal_link_on_public_routes_resolves(anon):
    """No internal link on a public route answers an error."""
    import re
    checked = {}
    failures = []
    for route in PUBLIC_ROUTES:
        body = page(route).text
        for href in re.findall(r'href=["\'](/[^"\'#?]*)', body):
            target = href.rstrip("/") or "/"
            if target in checked:
                continue
            status = raw_page(target).status_code
            checked[target] = status
            if status >= 400 and target not in RESERVED_ROUTES:
                failures.append((route, target, status))
    assert checked, "no internal link was found on any public route"
    assert not failures, (
        f"internal links answer an error: {failures}. Every internal link on every "
        f"public route resolves")


def test_security_headers_present_on_every_response(anon):
    """Every response carries the standard security header set."""
    probes = [("the hub", page("/")),
              ("a chapter", page("/logo")),
              ("the chapter collection", anon.get("/chapters")),
              ("a refusal", anon.get("/queue"))]
    for label, response in probes:
        headers = {name.lower() for name in response.headers}
        for required in SECURITY_HEADERS:
            assert required in headers, (
                f"{label} answers without the {required} header; every response "
                f"carries the standard security header set. Present: "
                f"{sorted(headers)}")
        assert any(name in headers for name in FRAME_HEADERS), (
            f"{label} declares no frame ancestry policy; one of {list(FRAME_HEADERS)} "
            f"is required")
        nosniff = response.headers.get("x-content-type-options", "")
        assert nosniff.strip().lower() == "nosniff", (
            f"{label} sets x-content-type-options to {nosniff!r} rather than "
            f"nosniff")


def test_cookie_choice_is_asked_once_and_survives_reload(anon, backend):
    """A recorded consent answer survives a reload and is not asked again."""
    table = resolve_table(backend, CONSENT_TABLES)
    first = page("/")
    assert CONSENT_CONTROL in first.text, (
        f"the hub does not carry the consent control {CONSENT_CONTROL!r} for a "
        f"first time visitor")

    before = backend.count(table)
    recorded = anon.post("/consent", json={"answer": "reject"})
    assert recorded.status_code in (200, 201), (
        f"recording a consent answer did not succeed: {describe(recorded)}")
    after = backend.count(table)
    assert after == before + 1, (
        f"{table} went from {before} to {after} rows after one recorded answer; the "
        f"answer must be stored rather than held in the page")

    read_back = anon.get("/consent")
    assert read_back.status_code == 200, (
        f"GET /api/consent did not answer the recorded choice: "
        f"{describe(read_back)}")
    body = read_back.text.lower()
    assert "reject" in body, (
        f"the recorded consent answer did not survive: {read_back.text[:400]}")


def test_library_lists_every_asset_with_one_availability_badge(employee):
    """The library lists every asset, each with exactly one availability badge."""
    rows = assets(employee)
    assert rows, "the library served no assets to a signed in principal"
    for row in rows:
        badge = row.get("availability")
        assert badge in AVAILABILITY_BADGES, (
            f"the asset {row.get('name')!r} carries availability {badge!r}, which is "
            f"not one of {list(AVAILABILITY_BADGES)}")
        assert row.get("asset_class") in ASSET_CLASSES, (
            f"the asset {row.get('name')!r} carries class {row.get('asset_class')!r}, "
            f"outside the seven named classes")
        assert row.get("formats") is not None, (
            f"the asset {row.get('name')!r} serves no format list")

    filtered = assets(employee, asset_class="pictogram")
    assert all(row.get("asset_class") == "pictogram" for row in filtered), (
        "the asset class filter returned assets of another class")
    for asset_class in ASSET_CLASSES:
        assert any(row.get("asset_class") == asset_class for row in rows), (
            f"no asset of class {asset_class!r} reaches the library")


def test_availability_is_computed_for_the_calling_principal(employee, partner):
    """Two principals see different badges on the same restricted asset."""
    mark = asset_of_class(employee, "mark")
    partner_rows = {row.get("id"): row for row in assets(partner)}
    assert mark["id"] in partner_rows, (
        "the bounded partner cannot see the mark at all; the library is never empty "
        "and shows everything that exists, badged for the reader")

    partner_view = partner_rows[mark["id"]]
    assert partner_view.get("availability") in ("Request required", "Restricted"), (
        f"the partner sees the mark as {partner_view.get('availability')!r}; the "
        f"mark is outside the asset classes the engagement grants")

    granted = asset_of_class(partner, PARTNER_GRANTED_CLASSES[0])
    partner_granted = partner_rows.get(granted["id"], {})
    employee_rows = {row.get("id"): row for row in assets(employee)}
    employee_view = employee_rows.get(mark["id"], {})
    assert employee_view.get("availability") != partner_view.get("availability") or \
        partner_granted.get("availability") == "Available", (
        f"the employee and the bounded partner receive identical availability on "
        f"every asset; availability is decided for the calling principal at the "
        f"moment of asking, never shared between principals")


def test_asset_detail_carries_licence_and_governing_statement(employee):
    """Asset detail states the licence, the governing rule and the lineage."""
    mark = asset_of_class(employee, "mark")
    response = asset_detail(employee, mark["id"])
    assert response.status_code == 200, (
        f"asset detail for the mark did not answer 200: {describe(response)}")
    payload = response.json()

    licence = payload.get("licence") or payload.get("license")
    assert licence, (
        f"asset detail carries no licence record: {response.text[:600]}")
    for field in ("permitted", "prohibited", "territory"):
        assert any(field in str(key).lower() for key in
                   (licence if isinstance(licence, dict) else {})), (
            f"the licence record names nothing about {field}: {licence}")

    statement = (payload.get("statement_id") or payload.get("governing_statement")
                 or payload.get("statement"))
    assert statement, (
        f"asset detail does not link the governing statement identifier: "
        f"{response.text[:600]}")

    assert payload.get("availability") in AVAILABILITY_BADGES, (
        f"asset detail serves availability {payload.get('availability')!r}")
    assert payload.get("dimensions") is not None, (
        "asset detail serves no declared dimensions")


def test_employee_downloads_available_asset_and_row_is_recorded(employee, backend):
    """A released download reaches the principal and leaves a record."""
    table = resolve_table(backend, DOWNLOAD_TABLES)
    target = None
    for row in assets(employee):
        if row.get("availability") == "Available":
            target = row
            break
    assert target, (
        "no asset is Available to the employee; the seed must release at least one")

    before = backend.count(table)
    response = download(employee, target["id"])
    assert response.status_code == 200, (
        f"an Available asset was not released to the employee: "
        f"{describe(response)}")
    assert response.content, (
        f"the download of {target.get('name')!r} answered 200 with an empty body")

    after = poll_until(lambda: backend.count(table) > before)
    assert after, (
        f"{table} still holds {backend.count(table)} rows after a release; every use "
        f"of the identity is recorded")


def test_restricted_download_without_grant_is_refused_with_reason(partner, backend):
    """A restricted asset without a covering grant is refused, writing nothing."""
    table = resolve_table(backend, DOWNLOAD_TABLES)
    mark = None
    for row in assets(partner):
        if row.get("asset_class") == "mark":
            mark = row
            break
    assert mark, "the mark is not served to the partner"

    before = backend.count(table)
    response = download(partner, mark["id"])
    assert 400 <= response.status_code < 500, (
        f"the bounded partner was served the mark with status "
        f"{response.status_code}; a restricted asset needs a covering grant: "
        f"{describe(response)}")
    assert response.text.strip(), (
        "the refusal carries no body; a refusal names what is missing")
    assert backend.count(table) == before, (
        f"{table} grew after a refused download; a refusal writes nothing")

    detail = asset_detail(partner, mark["id"]).json()
    reason = (detail.get("disabled_reason") or detail.get("reason")
              or detail.get("unavailable_reason") or "")
    assert str(reason).strip(), (
        f"asset detail disables the action without stating the reason: "
        f"{list(detail)}. A tool that greys out a control without saying why teaches "
        f"people to route around it")


def test_retired_asset_is_never_downloadable_and_names_successor(employee, backend):
    """A retired asset refuses every download and names its successor."""
    retired = None
    for row in assets(employee):
        if row.get("availability") == "Retired":
            retired = row
            break
    assert retired, "no asset is seeded Retired"

    table = resolve_table(backend, DOWNLOAD_TABLES)
    before = backend.count(table)
    response = download(employee, retired["id"])
    assert 400 <= response.status_code < 500, (
        f"a Retired asset was released with status {response.status_code}: "
        f"{describe(response)}")
    assert backend.count(table) == before, (
        f"{table} grew after a refused retired download")

    detail = asset_detail(employee, retired["id"]).json()
    successor = (detail.get("successor") or detail.get("successor_id")
                 or detail.get("replaced_by") or detail.get("supersedes"))
    assert successor, (
        f"the retired asset names no successor: {list(detail)}. A retirement names "
        f"what replaces it")


def test_protected_object_address_is_refused_anonymously(employee, anon):
    """An anonymous caller holding a protected object address is refused."""
    mark = asset_of_class(employee, "mark")
    detail = asset_detail(employee, mark["id"]).json()

    candidates = []
    for key in ("master", "master_url", "object_url", "object_key", "derivative",
                "derivative_url", "preview", "preview_url", "storage_key"):
        value = detail.get(key)
        if isinstance(value, str) and value:
            candidates.append(value)

    refused = download(anon, mark["id"])
    assert 400 <= refused.status_code < 500, (
        f"the download endpoint served a restricted asset to an anonymous caller "
        f"with status {refused.status_code}: {describe(refused)}")

    for address in candidates:
        if not address.startswith("http"):
            continue
        response = httpx.get(address, timeout=appclient.TIMEOUT)
        assert response.status_code >= 400, (
            f"the object address {address} served the binary directly with status "
            f"{response.status_code}; a protected object is never publicly readable "
            f"and every release passes the decision")


def test_released_icon_dimensions_must_match_its_class(employee, backend):
    """A released icon whose declared dimensions mismatch its class is refused."""
    served = {row.get("id"): row for row in assets(employee)}
    for row in served.values():
        asset_class = row.get("asset_class")
        if asset_class not in ICON_DIMENSIONS:
            continue
        detail = asset_detail(employee, row["id"]).json()
        dimensions = detail.get("dimensions") or {}
        expected = ICON_DIMENSIONS[asset_class]
        text = str(dimensions)
        assert str(expected) in text, (
            f"the {asset_class} {row.get('name')!r} declares dimensions "
            f"{dimensions} rather than the published {expected} by {expected} its "
            f"class is drawn at")

    reviewer_session = appclient.client(appclient.login(REVIEWER, PASSWORD))
    table = resolve_table(backend, ASSET_TABLES)
    with reviewer_session:
        before = backend.count(table)
        response = reviewer_session.post("/assets", json={
            "name": f"probe-{probe_token()}",
            "asset_class": "ui_icon",
            "chapter": "iconography",
            "dimensions": {"width": 999, "height": 999},
            "availability": "Available",
        })
        assert response.status_code not in (200, 201), (
            f"an icon declaring the wrong dimensions for its class was released with "
            f"status {response.status_code}: {describe(response)}")
        assert backend.count(table) == before, (
            f"{table} grew after a refused icon release")


def test_request_submission_records_chapter_and_policy_version(partner, backend):
    """A submitted request stores the rules that applied when it was asked."""
    table = resolve_table(backend, REQUEST_TABLES)
    mark = asset_of_class(partner, "mark")
    before = backend.count(table)

    response = submit_request(partner, mark["id"], "co_brand",
                              campaign_end=WORKED_CAMPAIGN_END)
    assert response.status_code in (200, 201), (
        f"the partner could not raise a usage request against the mark: "
        f"{describe(response)}")
    payload = response.json()
    assert backend.count(table) == before + 1, (
        f"{table} did not grow by exactly one row after one submission")

    for field, names in (
        ("the chapter version", ("chapter_version_id", "chapter_version",
                                 "chapterVersionId")),
        ("the cited statements", ("cited_statement_ids", "citedStatementIdentifiers",
                                 "cited_statements")),
        ("the policy version", ("policy_version", "policyVersion")),
    ):
        assert any(payload.get(name) for name in names), (
            f"the stored request does not record {field}; a request is self "
            f"describing years later rather than joined against current state. "
            f"Served keys: {sorted(payload)}")

    assert payload.get("state") in REQUEST_STATES, (
        f"the new request carries state {payload.get('state')!r}, outside the nine "
        f"named states")
    assert payload.get("deadline") or payload.get("deadline_at"), (
        f"the request carries no deadline stored at submission: {sorted(payload)}")
    assert payload.get("application_class") in APPLICATION_CLASSES, (
        f"the request carries application class {payload.get('application_class')!r}")


def test_requester_reads_only_their_own_requests(partner, partner_second, employee):
    """A request collection is narrowed to the calling principal."""
    mark = asset_of_class(partner, "mark")
    created = submit_request(partner, mark["id"], "co_brand",
                             campaign_end=WORKED_CAMPAIGN_END)
    assert created.status_code in (200, 201), (
        f"the partner could not raise a request: {describe(created)}")
    request_id = created.json().get("id")
    assert request_id is not None, "the created request carries no identifier"

    mine = [row.get("id") for row in json_list(partner.get("/requests"),
                                               "GET /api/requests")]
    assert request_id in mine, "the requester cannot read their own request"

    theirs = [row.get("id") for row in json_list(partner_second.get("/requests"),
                                                 "GET /api/requests")]
    assert request_id not in theirs, (
        f"the request {request_id} raised by {PARTNER} reaches {PARTNER_SECOND}; a "
        f"principal reads their own requests only")

    direct = read_request(partner_second, request_id)
    assert 400 <= direct.status_code < 500, (
        f"a direct read of another principal's request answered "
        f"{direct.status_code}: {describe(direct)}")

    as_employee = read_request(employee, request_id)
    assert 400 <= as_employee.status_code < 500, (
        f"an employee read another principal's request with status "
        f"{as_employee.status_code}")


def test_co_brand_application_class_adds_a_legal_stage(partner):
    """A co-brand application class adds a legal stage."""
    pictogram = asset_of_class(partner, "pictogram")
    internal = submit_request(partner, pictogram["id"], "internal")
    assert internal.status_code in (200, 201), (
        f"an internal request was refused: {describe(internal)}")
    internal_stages = stage_ids(internal.json())

    co_brand = submit_request(partner, pictogram["id"], "co_brand")
    assert co_brand.status_code in (200, 201), (
        f"a co_brand request was refused: {describe(co_brand)}")
    co_brand_stages = stage_ids(co_brand.json())

    assert len(co_brand_stages) > len(internal_stages), (
        f"an internal request carries {len(internal_stages)} stage(s) and a co_brand "
        f"request carries {len(co_brand_stages)}; co_brand, merchandise and "
        f"partnership always add a legal stage, decided from what is asked for "
        f"rather than from a fixed chart")

    kinds = " ".join(str(stage) for stage in
                     (co_brand.json().get("stages")
                      or co_brand.json().get("request_stages") or []))
    assert "legal" in kinds.lower(), (
        f"no stage on the co_brand request is a legal stage: {kinds[:400]}")


def test_mark_asset_class_adds_a_second_distinct_reviewer_stage(partner):
    """A request against the mark carries two stages held by distinct reviewers."""
    mark = asset_of_class(partner, "mark")
    response = submit_request(partner, mark["id"], "co_brand",
                              campaign_end=WORKED_CAMPAIGN_END)
    assert response.status_code in (200, 201), (
        f"a request against the mark was refused: {describe(response)}")
    payload = response.json()

    stages = stage_ids(payload)
    assert len(stages) >= 2, (
        f"a request against a mark asset carries {len(stages)} stage(s); the mark "
        f"adds a second stage on top of any legal stage")

    holders = stage_holders(payload)
    assert len(holders) >= 2, (
        f"the mark request names {len(holders)} stage holder(s): {holders}. Every "
        f"open stage names exactly one reviewer")
    assert len(set(holders)) == len(holders), (
        f"the mark request assigns the same reviewer to more than one stage: "
        f"{holders}. The second stage is held by a distinct reviewer")


def test_request_always_names_exactly_one_holder(partner, reviewer):
    """A request in any state names exactly one holder."""
    pictogram = asset_of_class(partner, "pictogram")
    created = submit_request(partner, pictogram["id"], "advertising")
    assert created.status_code in (200, 201), (
        f"the request was refused: {describe(created)}")
    payload = created.json()
    request_id = payload.get("id")

    holder = holder_of(payload)
    assert holder, (
        f"the submitted request names no holder: {sorted(payload)}. 'With the brand "
        f"team' is not a holder and the app never lets a request be in that "
        f"condition")
    assert not isinstance(holder, list), (
        f"the request names {holder} as its holder; exactly one holder is named")

    read_back = read_request(partner, request_id)
    assert read_back.status_code == 200, (
        f"the requester cannot read their own request: {describe(read_back)}")
    assert holder_of(read_back.json()), (
        "the request desk serves a request with no named holder")


def test_reviewer_is_never_assigned_their_own_request(reviewer, reviewer_second):
    """A reviewer is never assigned a stage of a request they raised."""
    pictogram = asset_of_class(reviewer, "pictogram")
    created = submit_request(reviewer, pictogram["id"], "co_brand")
    assert created.status_code in (200, 201), (
        f"a reviewer could not raise a request of their own: {describe(created)}")
    payload = created.json()
    request_id = payload.get("id")

    holders = stage_holders(payload)
    assert REVIEWER not in holders, (
        f"the reviewer {REVIEWER} holds a stage of their own request: {holders}")

    for stage_id in open_stage_ids(payload):
        response = decide(reviewer, stage_id)
        assert 400 <= response.status_code < 500, (
            f"the requester decided a stage of their own request with status "
            f"{response.status_code}: {describe(response)}")

    after = read_request(reviewer, request_id).json()
    assert after.get("state") == payload.get("state"), (
        f"the request moved from {payload.get('state')!r} to {after.get('state')!r} "
        f"after a refused self decision; the protected state must be unchanged")


def test_queue_is_ordered_by_the_stored_deadline(partner, reviewer):
    """The queue lists waiting stages in stored deadline order."""
    mark = asset_of_class(partner, "mark")
    for _ in range(2):
        submit_request(partner, mark["id"], "co_brand",
                       campaign_end=WORKED_CAMPAIGN_END)

    rows = queue(reviewer)
    assert rows, (
        "the approval queue is empty for the reviewer after two submissions against "
        "the mark")

    deadlines = []
    for row in rows:
        value = (row.get("deadline") or row.get("deadline_at")
                 or (row.get("request") or {}).get("deadline"))
        assert value, (
            f"a queue entry carries no deadline: {row}. The queue is ordered by the "
            f"deadline stored on the request")
        deadlines.append(parse_date(str(value)))
    assert deadlines == sorted(deadlines), (
        f"the queue served deadlines in the order {deadlines}; a reviewer reads the "
        f"closest deadline first")


def test_stored_deadline_survives_a_policy_change(partner, reviewer, backend):
    """A deadline stored at submission is not moved by a later policy change."""
    table = resolve_table(backend, REQUEST_TABLES)
    pictogram = asset_of_class(partner, "pictogram")
    created = submit_request(partner, pictogram["id"], "advertising")
    assert created.status_code in (200, 201), (
        f"the request was refused: {describe(created)}")
    request_id = created.json().get("id")
    first = created.json().get("deadline") or created.json().get("deadline_at")
    assert first, "the request carries no deadline at submission"

    reviewer.post("/policies", json={"application_class": "advertising",
                                     "deadline_days": 1})
    settle(1.0)

    after = read_request(partner, request_id).json()
    second = after.get("deadline") or after.get("deadline_at")
    assert second == first, (
        f"the stored deadline moved from {first} to {second} after a policy change; "
        f"a deadline is set at submission and stored on the request so a later "
        f"policy change cannot silently move a live deadline")

    rows = [row for row in backend.rows(table) if str(row.get("id")) == str(request_id)]
    assert rows, f"the request {request_id} has no row in {table}"


def test_requester_withdraws_their_own_request(partner, partner_second):
    """A requester withdraws their own request before a decision."""
    pictogram = asset_of_class(partner, "pictogram")
    created = submit_request(partner, pictogram["id"], "advertising")
    request_id = created.json().get("id")

    foreign = withdraw_request(partner_second, request_id)
    assert 400 <= foreign.status_code < 500, (
        f"another principal withdrew a request that is not theirs with status "
        f"{foreign.status_code}: {describe(foreign)}")

    response = withdraw_request(partner, request_id)
    assert response.status_code in (200, 201), (
        f"the requester could not withdraw their own request: {describe(response)}")
    state = (response.json().get("state")
             or read_request(partner, request_id).json().get("state"))
    assert state == "withdrawn", (
        f"the withdrawn request reads state {state!r} rather than withdrawn")


def test_changes_requested_resubmission_returns_to_routed(partner, reviewer):
    """A resubmitted request returns to routed for a fresh policy evaluation."""
    pictogram = asset_of_class(partner, "pictogram")
    created = submit_request(partner, pictogram["id"], "advertising")
    request_id = created.json().get("id")
    stages = open_stage_ids(created.json())
    assert stages, f"the new request carries no open stage: {created.text[:400]}"

    asked = decide(reviewer, stages[0], decision="request_changes",
                   reason="Tighten the stated territory")
    assert asked.status_code in (200, 201), (
        f"a reviewer could not request changes: {describe(asked)}")
    state = read_request(partner, request_id).json().get("state")
    assert state == "changes_requested", (
        f"after a request for changes the request reads {state!r} rather than "
        f"changes_requested")

    resubmitted = partner.post(f"/requests/{request_id}/submit", json={})
    if resubmitted.status_code not in (200, 201):
        resubmitted = partner.post(f"/requests/{request_id}/resubmit", json={})
    assert resubmitted.status_code in (200, 201), (
        f"the requester could not resubmit after changes were asked for: "
        f"{describe(resubmitted)}")

    after = read_request(partner, request_id).json()
    assert after.get("state") in ("routed", "under_review"), (
        f"a resubmitted request reads {after.get('state')!r}; it returns to routed "
        f"so policy is evaluated again, because the request has changed")


def test_concurrent_stage_decisions_admit_exactly_one(partner, reviewer, backend):
    """Two approvals of one open stage at one instant leave exactly one decision."""
    stage_table = resolve_table(backend, STAGE_TABLES)
    mark = asset_of_class(partner, "mark")
    created = submit_request(partner, mark["id"], "co_brand",
                             campaign_end=WORKED_CAMPAIGN_END)
    assert created.status_code in (200, 201), (
        f"the contested request could not be raised: {describe(created)}")
    payload = created.json()
    request_id = payload.get("id")
    stages = open_stage_ids(payload)
    assert stages, f"the request carries no open stage: {created.text[:400]}"
    contested = stages[0]

    barrier = threading.Barrier(2)
    tokens = [appclient.login(REVIEWER, PASSWORD),
              appclient.login(REVIEWER_SECOND, PASSWORD)]

    def attempt(token: str) -> int:
        with appclient.client(token) as session:
            barrier.wait(timeout=30)
            return decide(session, contested).status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        statuses = sorted(future.result() for future in
                          [pool.submit(attempt, tokens[0]),
                           pool.submit(attempt, tokens[1])])

    accepted = [code for code in statuses if code in (200, 201)]
    refused = [code for code in statuses if 400 <= code < 500]
    assert len(accepted) == 1 and len(refused) == 1, (
        f"two simultaneous approvals of one open stage returned {statuses}; exactly "
        f"one must be recorded and the other refused as a conflict, never merged and "
        f"never a server error")

    rows = [row for row in backend.rows(stage_table)
            if str(row.get("id")) == str(contested)]
    assert len(rows) == 1, (
        f"{len(rows)} rows in {stage_table} carry the contested stage identifier "
        f"{contested}")
    decided = rows[0]
    outcome = decided.get("outcome") or decided.get("decision")
    assert outcome, (
        f"the contested stage recorded no outcome: {decided}. The decision a "
        f"reviewer holds must be a real row a second decision cannot overwrite")

    final = read_request(partner, request_id).json()
    assert final.get("state") in REQUEST_STATES, (
        f"after the contested decision the request reads {final.get('state')!r}")


def test_grant_minting_is_idempotent_on_a_retried_approval(partner, reviewer,
                                                           reviewer_second, backend):
    """A retried approval yields the grant that exists rather than a second one."""
    grant_table = resolve_table(backend, GRANT_TABLES)
    pictogram = asset_of_class(partner, "pictogram")
    created = submit_request(partner, pictogram["id"], "co_brand")
    request_id = created.json().get("id")

    before = backend.count(grant_table)
    approved = _approve_every_stage(created.json(), reviewer, reviewer_second)
    assert approved, "no stage of the request could be approved"

    settle(1.0)
    after_first = backend.count(grant_table)
    assert after_first == before + 1, (
        f"{grant_table} went from {before} to {after_first} after one full approval; "
        f"the last approval mints exactly one grant")

    payload = read_request(partner, request_id).json()
    for stage_id in stage_ids(payload):
        decide(reviewer, stage_id)
        decide(reviewer_second, stage_id)
    settle(1.0)

    after_retry = backend.count(grant_table)
    assert after_retry == after_first, (
        f"{grant_table} grew from {after_first} to {after_retry} after the approvals "
        f"were retried; minting is keyed on the request identifier so a retry yields "
        f"the same grant")

    mine = [row for row in grants(partner)
            if str(row.get("request_id")) == str(request_id)]
    assert len(mine) == 1, (
        f"{len(mine)} grants carry the request identifier {request_id}; exactly one "
        f"grant exists per approved request")
    assert mine[0].get("request_id") is not None, (
        "the grant does not carry the identifier of the request that justified it")


def _approve_every_stage(payload: dict, reviewer, reviewer_second) -> bool:
    """Approve each open stage with whichever reviewer holds it."""
    approved = False
    for stage_id in open_stage_ids(payload):
        for session in (reviewer, reviewer_second):
            response = decide(session, stage_id)
            if response.status_code in (200, 201):
                approved = True
                break
    return approved


def test_grant_end_date_is_the_earliest_of_four_candidates(partner, reviewer,
                                                           reviewer_second):
    """A grant ends at the engagement end when that is the earliest candidate."""
    pictogram = asset_of_class(partner, "pictogram")
    created = submit_request(partner, pictogram["id"], "co_brand",
                             campaign_end=WORKED_CAMPAIGN_END)
    assert created.status_code in (200, 201), (
        f"the request was refused: {describe(created)}")
    request_id = created.json().get("id")

    assert _approve_every_stage(created.json(), reviewer, reviewer_second), (
        "no stage of the request could be approved")
    settle(1.0)

    mine = [row for row in grants(partner)
            if str(row.get("request_id")) == str(request_id)]
    assert mine, (
        f"no grant carries the request identifier {request_id} after full approval")
    grant = mine[0]

    ends_at = grant.get("ends_at") or grant.get("not_after") or grant.get("notAfter")
    assert ends_at, f"the grant carries no end date: {sorted(grant)}"

    engagement_end = parse_date(PARTNER_ENGAGEMENT_END)
    campaign_end = parse_date(WORKED_CAMPAIGN_END)
    actual = parse_date(str(ends_at))
    assert actual <= engagement_end, (
        f"the grant ends {iso(actual)} but the requester's engagement ends "
        f"{PARTNER_ENGAGEMENT_END}; the engagement end always wins when it is the "
        f"smallest of the four candidates, even when that makes the grant expire the "
        f"same afternoon")
    assert actual < campaign_end, (
        f"the grant ends {iso(actual)}, which is the requested campaign end "
        f"{WORKED_CAMPAIGN_END} rather than the earlier engagement end; a permission "
        f"may not outlive the contract that justified it")


def test_proof_required_condition_holds_the_grant_until_accepted(partner, reviewer,
                                                                 reviewer_second):
    """A grant waiting on an unaccepted proof releases nothing."""
    pictogram = asset_of_class(partner, "pictogram")
    created = submit_request(partner, pictogram["id"], "merchandise")
    request_id = created.json().get("id")
    stages = open_stage_ids(created.json())
    assert stages, f"the request carries no open stage: {created.text[:400]}"

    first = decide(reviewer, stages[0], conditions=[{"kind": "proof_required",
                                                     "text": "Show final artwork"}])
    if first.status_code not in (200, 201):
        first = decide(reviewer_second, stages[0],
                       conditions=[{"kind": "proof_required",
                                    "text": "Show final artwork"}])
    assert first.status_code in (200, 201), (
        f"a reviewer could not approve with a proof condition: {describe(first)}")

    remaining = open_stage_ids(read_request(partner, request_id).json())
    for stage_id in remaining:
        for session in (reviewer, reviewer_second):
            if decide(session, stage_id).status_code in (200, 201):
                break
    settle(1.0)

    payload = read_request(partner, request_id).json()
    conditions = payload.get("conditions") or []
    assert any("proof" in str(item).lower() for item in conditions), (
        f"the request records no proof condition: {conditions}. A condition is a "
        f"record rather than a note in a comment box")

    blocked = download(partner, pictogram["id"])
    assert 400 <= blocked.status_code < 500, (
        f"the binary was released with status {blocked.status_code} while the proof "
        f"condition was unsatisfied; the grant is created with a future start date "
        f"and activates only on acceptance: {describe(blocked)}")

    mine = [row for row in grants(partner)
            if str(row.get("request_id")) == str(request_id)]
    assert mine, f"no grant was minted for the request {request_id}"
    starts_at = (mine[0].get("starts_at") or mine[0].get("not_before")
                 or mine[0].get("notBefore"))
    assert starts_at, (
        f"the pending grant carries no start date: {sorted(mine[0])}")
    assert parse_date(str(starts_at)) > now_utc(), (
        f"the grant starts {starts_at}, which is not in the future; a proof_required "
        f"condition holds the grant pending until a reviewer accepts the proof")


def test_proof_upload_size_and_sniffed_type_are_enforced(partner, reviewer,
                                                         reviewer_second):
    """A proof upload is size capped and typed by content rather than by name."""
    pictogram = asset_of_class(partner, "pictogram")
    created = submit_request(partner, pictogram["id"], "merchandise")
    request_id = created.json().get("id")
    stages = open_stage_ids(created.json())
    condition_id = None
    for session in (reviewer, reviewer_second):
        response = decide(session, stages[0],
                          conditions=[{"kind": "proof_required",
                                       "text": "Show final artwork"}])
        if response.status_code in (200, 201):
            for item in (read_request(partner, request_id).json().get("conditions")
                         or []):
                if "proof" in str(item.get("kind", "")).lower():
                    condition_id = item.get("id")
            break
    assert condition_id is not None, (
        "no proof condition identifier was served after an approval carrying one")

    disguised = partner.post(
        f"/conditions/{condition_id}/proof",
        files={"file": ("artwork.png", b"#!/bin/sh\necho not-an-image\n",
                        "image/png")})
    assert 400 <= disguised.status_code < 500, (
        f"a script uploaded under an image name and an image type was accepted with "
        f"status {disguised.status_code}; the type is decided by inspecting the "
        f"content of the file rather than by trusting the name it arrives under: "
        f"{describe(disguised)}")

    oversized = partner.post(
        f"/conditions/{condition_id}/proof",
        files={"file": ("big.png", b"\x89PNG\r\n\x1a\n" + b"0" * (64 * 1024 * 1024),
                        "image/png")})
    assert 400 <= oversized.status_code < 500, (
        f"an upload past the size cap was accepted with status "
        f"{oversized.status_code}: {describe(oversized)}")


def test_withdrawal_during_a_decision_wins(partner, reviewer, reviewer_second):
    """A recorded withdrawal wins over a decision arriving after it."""
    pictogram = asset_of_class(partner, "pictogram")
    created = submit_request(partner, pictogram["id"], "advertising")
    request_id = created.json().get("id")
    stages = open_stage_ids(created.json())
    assert stages, f"the request carries no open stage: {created.text[:400]}"

    withdrawn = withdraw_request(partner, request_id)
    assert withdrawn.status_code in (200, 201), (
        f"the requester could not withdraw: {describe(withdrawn)}")

    for session in (reviewer, reviewer_second):
        response = decide(session, stages[0])
        assert 400 <= response.status_code < 500, (
            f"a decision on a withdrawn request was accepted with status "
            f"{response.status_code}; withdrawal wins and the reviewer is told why: "
            f"{describe(response)}")
        assert response.text.strip(), (
            "the refused decision carries no body explaining why")

    final = read_request(partner, request_id).json()
    assert final.get("state") == "withdrawn", (
        f"the request reads {final.get('state')!r} after a decision arrived on a "
        f"withdrawn request")


def test_retiring_an_asset_under_review_rejects_the_request(partner, reviewer):
    """Retiring an asset with an open request rejects it and names the successor."""
    pictogram = asset_of_class(partner, "pictogram")
    created = submit_request(partner, pictogram["id"], "advertising")
    assert created.status_code in (200, 201), (
        f"the request was refused: {describe(created)}")
    request_id = created.json().get("id")

    retired = reviewer.post(f"/assets/{pictogram['id']}/retire",
                            json={"successor_id": None})
    if retired.status_code not in (200, 201):
        successor = asset_of_class(reviewer, "spot_icon")
        retired = reviewer.post(f"/assets/{pictogram['id']}/retire",
                                json={"successor_id": successor["id"]})
    assert retired.status_code in (200, 201), (
        f"the asset under review could not be retired: {describe(retired)}")
    settle(1.0)

    payload = read_request(partner, request_id).json()
    assert payload.get("state") == "rejected", (
        f"the open request reads {payload.get('state')!r} after its asset was "
        f"retired; the request is rejected automatically and the requester is invited "
        f"to resubmit")
    reason = str(payload.get("reason") or payload.get("rejection_reason") or "")
    assert reason.strip(), (
        f"the automatic rejection states no reason: {sorted(payload)}. A rejection "
        f"always shows a reason")
    detail = asset_detail(reviewer, pictogram["id"]).json()
    successor = (detail.get("successor") or detail.get("successor_id")
                 or detail.get("replaced_by"))
    assert successor, (
        "the retired asset names no successor, so the requester cannot resubmit "
        "against it")


def test_duplicate_submission_in_quick_succession_produces_one(partner, backend):
    """One request submitted twice by a double click produces one submission."""
    table = resolve_table(backend, REQUEST_TABLES)
    pictogram = asset_of_class(partner, "pictogram")
    before = backend.count(table)

    body = {
        "asset_id": pictogram["id"],
        "application_class": "advertising",
        "territory": "worldwide",
        "campaign_start": future_date(7),
        "campaign_end": future_date(120),
        "cited_statement_ids": [STATEMENT_IDENTIFIER],
        "idempotency_key": probe_token(),
    }
    first = partner.post("/requests", json=body)
    second = partner.post("/requests", json=body)

    assert first.status_code in (200, 201), (
        f"the first submission was refused: {describe(first)}")
    after = backend.count(table)
    assert after == before + 1, (
        f"{table} went from {before} to {after} rows after the same request was "
        f"submitted twice in quick succession; a double click produces one "
        f"submission, not two. Second answer: {describe(second)}")


def test_audit_record_is_written_once_per_transition(partner, reviewer,
                                                     reviewer_second, backend):
    """Every request transition writes exactly one audit record."""
    table = resolve_table(backend, AUDIT_TABLES)
    pictogram = asset_of_class(partner, "pictogram")
    before = backend.count(table)

    created = submit_request(partner, pictogram["id"], "co_brand")
    request_id = created.json().get("id")
    assert _approve_every_stage(created.json(), reviewer, reviewer_second), (
        "no stage could be approved")
    settle(2.0)

    after = backend.count(table)
    assert after > before, (
        f"{table} did not grow while a request moved from submission to grant; every "
        f"transition writes a record")

    response = audit(reviewer, request_id=request_id)
    assert response.status_code == 200, (
        f"the audit surface did not answer a query by request identifier: "
        f"{describe(response)}")
    rows = response.json()
    rows = rows if isinstance(rows, list) else rows.get("records") or []
    assert rows, (
        f"the audit record holds nothing for the request {request_id}")

    for row in rows:
        for field, names in (
            ("the acting principal", ("actor", "actor_email", "principal",
                                      "acting_principal")),
            ("the principal type", ("principal_type", "actor_type")),
            ("the address the action came from", ("address", "source_address",
                                                  "ip", "remote_address")),
            ("the request identifier", ("request_id", "requestId")),
            ("the state before", ("state_before", "before_state", "before")),
            ("the state after", ("state_after", "after_state", "after")),
        ):
            assert any(row.get(name) is not None for name in names), (
                f"an audit record does not carry {field}: {sorted(row)}")

    signatures = [(str(row.get("request_id")),
                   str(row.get("state_before") or row.get("before")),
                   str(row.get("state_after") or row.get("after")))
                  for row in rows]
    assert len(signatures) == len(set(signatures)), (
        f"the audit record holds duplicate transitions for the request "
        f"{request_id}: {signatures}. Exactly one record is written per transition")


def test_audit_record_cannot_be_altered_or_removed(reviewer, employee, backend):
    """An audit record survives every attempt to alter or remove it."""
    table = resolve_table(backend, AUDIT_TABLES)
    response = audit(reviewer)
    assert response.status_code == 200, (
        f"the reviewer cannot read the audit record: {describe(response)}")
    rows = response.json()
    rows = rows if isinstance(rows, list) else rows.get("records") or []
    assert rows, "the audit record is empty, so tamper resistance cannot be observed"

    before = backend.count(table)
    target = rows[0]
    record_id = target.get("id")
    assert record_id is not None, f"an audit record carries no identifier: {target}"

    attempts = [
        ("delete", reviewer.delete(f"/audit/{record_id}")),
        ("patch", reviewer.patch(f"/audit/{record_id}", json={"actor": "nobody"})),
        ("put", reviewer.put(f"/audit/{record_id}", json={"actor": "nobody"})),
        ("employee delete", employee.delete(f"/audit/{record_id}")),
    ]
    for label, attempt in attempts:
        assert attempt.status_code not in (200, 201, 204), (
            f"an audit record accepted a {label} with status "
            f"{attempt.status_code}; no endpoint, no control and no role edits or "
            f"deletes one: {describe(attempt)}")

    after = backend.count(table)
    assert after >= before, (
        f"{table} shrank from {before} to {after} rows after the tamper attempts")

    again = audit(reviewer)
    rows_again = again.json()
    rows_again = rows_again if isinstance(rows_again, list) else \
        rows_again.get("records") or []
    survivor = [row for row in rows_again if row.get("id") == record_id]
    assert survivor, (
        f"the audit record {record_id} no longer answers the same query after the "
        f"tamper attempts")
    assert survivor[0] == target, (
        f"the audit record {record_id} changed from {target} to {survivor[0]}")


def test_employee_is_refused_the_queue_and_the_decision_endpoint(employee, partner,
                                                                 reviewer, backend):
    """An employee session is refused the queue and the decision endpoint."""
    stage_table = resolve_table(backend, STAGE_TABLES)
    mark = asset_of_class(partner, "mark")
    created = submit_request(partner, mark["id"], "co_brand",
                             campaign_end=WORKED_CAMPAIGN_END)
    stages = open_stage_ids(created.json())
    assert stages, f"the request carries no open stage: {created.text[:400]}"
    stage_id = stages[0]

    before = [row for row in backend.rows(stage_table)
              if str(row.get("id")) == str(stage_id)]
    assert before, f"the stage {stage_id} has no row in {stage_table}"

    refused_queue = employee.get("/queue")
    assert 400 <= refused_queue.status_code < 500, (
        f"an employee opened the approval queue with status "
        f"{refused_queue.status_code}: {describe(refused_queue)}")

    refused_decision = decide(employee, stage_id)
    assert 400 <= refused_decision.status_code < 500, (
        f"an employee decided a stage with status {refused_decision.status_code}; "
        f"hiding a control in the interface is not authorization: "
        f"{describe(refused_decision)}")

    refused_audit = audit(employee)
    assert 400 <= refused_audit.status_code < 500, (
        f"an employee read the audit record with status "
        f"{refused_audit.status_code}")

    after = [row for row in backend.rows(stage_table)
             if str(row.get("id")) == str(stage_id)]
    assert after == before, (
        f"the stage row changed from {before} to {after} after refused calls; the "
        f"protected state is unchanged")

    anonymous = httpx.post(f"{appclient.api_base()}/stages/{stage_id}/decision",
                           json={"decision": "approve"}, timeout=appclient.TIMEOUT)
    assert 400 <= anonymous.status_code < 500, (
        f"an unauthenticated call decided a stage with status "
        f"{anonymous.status_code}")


def test_partner_engagement_bounds_downloads_and_expires_with_the_engagement(
        partner, partner_second, backend):
    """A partner downloads inside their engagement only, and not past its end."""
    table = resolve_table(backend, DOWNLOAD_TABLES)
    for asset_class in PARTNER_GRANTED_CLASSES:
        row = asset_of_class(partner, asset_class)
        response = download(partner, row["id"])
        assert response.status_code in (200, 400, 401, 403, 404, 409), (
            f"downloading a {asset_class} as the granted partner answered "
            f"{response.status_code}: {describe(response)}")

    outside = asset_of_class(partner, "mark")
    before = backend.count(table)
    refused = download(partner, outside["id"])
    assert 400 <= refused.status_code < 500, (
        f"the partner downloaded the mark, outside the asset classes the engagement "
        f"grants, with status {refused.status_code}: {describe(refused)}")
    assert backend.count(table) == before, (
        f"{table} grew after a refused out-of-engagement download")

    engagement_end = parse_date(PARTNER_ENGAGEMENT_END)
    if engagement_end < now_utc():
        for asset_class in PARTNER_GRANTED_CLASSES:
            row = asset_of_class(partner, asset_class)
            lapsed = download(partner, row["id"])
            assert 400 <= lapsed.status_code < 500, (
                f"the partner downloaded a {asset_class} with status "
                f"{lapsed.status_code} after the engagement ended "
                f"{PARTNER_ENGAGEMENT_END}; expiry is decided when the download is "
                f"asked for")
            assert PARTNER_ENGAGEMENT_END in lapsed.text or "engagement" in \
                lapsed.text.lower(), (
                f"the refusal does not name the engagement end date: "
                f"{lapsed.text[:300]}")

    foreign = asset_of_class(partner_second, "photograph")
    crossed = download(partner, foreign["id"])
    assert crossed.status_code != 200 or "photograph" in PARTNER_GRANTED_CLASSES, (
        f"the first partner downloaded a photograph, which only the second "
        f"partner's engagement grants: {describe(crossed)}")


def test_draft_chapter_version_is_unreachable_publicly(reviewer, anon):
    """A draft chapter version is readable by a reviewer and never publicly."""
    slug = f"probe-{probe_token()}"
    created = reviewer.post("/chapters", json={
        "slug": slug, "title": "Probe Chapter", "display_order": 90})
    if created.status_code not in (200, 201):
        served = [row.get("slug") for row in json_list(anon.get("/chapters"),
                                                       "GET /api/chapters")]
        for candidate in served:
            response = anon.get(f"/chapters/{candidate}")
            payload = response.json() if response.status_code == 200 else {}
            published = payload.get("published")
            if published is not None:
                assert published, (
                    f"the public chapter {candidate!r} serves published={published!r}; "
                    f"an unpublished chapter version is never reachable publicly")
        return

    public = raw_page(f"/{slug}")
    assert public.status_code == 404, (
        f"the unpublished chapter {slug!r} answered {public.status_code} on the "
        f"public surface; a draft leaks a rebrand or a launch")
    api = anon.get(f"/chapters/{slug}")
    assert 400 <= api.status_code < 500, (
        f"the unpublished chapter {slug!r} was served anonymously with status "
        f"{api.status_code}: {describe(api)}")


def test_invalid_request_body_names_the_field_and_writes_nothing(partner, backend):
    """A rejected body names the field at fault and writes nothing."""
    table = resolve_table(backend, REQUEST_TABLES)
    pictogram = asset_of_class(partner, "pictogram")
    before = backend.count(table)

    cases = [
        ("campaign_end", {"campaign_start": future_date(120),
                          "campaign_end": future_date(7)}),
        ("application_class", {"application_class": "not-a-class"}),
        ("cited_statement_ids", {"cited_statement_ids": ["logo.nowhere.99"]}),
        ("territory", {"territory": "not-a-territory"}),
    ]
    for field, override in cases:
        body = {
            "asset_id": pictogram["id"],
            "application_class": "advertising",
            "territory": "worldwide",
            "campaign_start": future_date(7),
            "campaign_end": future_date(120),
            "cited_statement_ids": [STATEMENT_IDENTIFIER],
        }
        body.update(override)
        response = partner.post("/requests", json=body)
        assert 400 <= response.status_code < 500, (
            f"an invalid {field} was accepted with status {response.status_code}: "
            f"{describe(response)}")
        assert field.split("_")[0] in response.text.lower(), (
            f"the rejection for an invalid {field} does not name the field at fault: "
            f"{response.text[:400]}")

    assert backend.count(table) == before, (
        f"{table} grew from {before} rows while every submission was rejected; a "
        f"rejected body writes nothing")


def test_decoy_and_repeated_form_submissions_are_refused(anon, partner, backend):
    """An automated submission is refused and writes nothing."""
    table = resolve_table(backend, REQUEST_TABLES)
    pictogram = asset_of_class(partner, "pictogram")
    before = backend.count(table)

    decoy = partner.post("/requests", json={
        "asset_id": pictogram["id"],
        "application_class": "advertising",
        "territory": "worldwide",
        "campaign_start": future_date(7),
        "campaign_end": future_date(120),
        "cited_statement_ids": [STATEMENT_IDENTIFIER],
        "website": "http://spam.example.invalid",
    })
    assert 400 <= decoy.status_code < 500, (
        f"a submission filling the unattended decoy field was accepted with status "
        f"{decoy.status_code}: {describe(decoy)}")
    assert backend.count(table) == before, (
        f"{table} grew after a refused decoy submission; a refusal writes nothing")

    statuses = []
    for _ in range(12):
        response = anon.post("/consent", json={"answer": "accept"})
        statuses.append(response.status_code)
    assert any(code == 429 or 400 <= code < 500 for code in statuses), (
        f"twelve identical submissions in quick succession from one origin all "
        f"answered {sorted(set(statuses))}; the same form arriving repeatedly is "
        f"refused")
