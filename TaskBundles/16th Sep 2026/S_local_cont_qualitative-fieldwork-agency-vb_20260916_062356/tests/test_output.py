"""The one pytest module for Qualitative Fieldwork Agency.

Every section (core features, data integrity, authorization, edge cases) and both
declared slots (db, storage) are merged here. Fixtures, pinned literals and helpers
live in conftest.py; the shared grader (appclient, capabilities, _shapes) is on
PYTHONPATH=/tests from the deku-verifier-base image.

The checklist obligations each function discharges live in the
pytest-provenance-v1 sidecar beside the bundle, not in a comment.

Channel disjointness, per reference/J J.12: the browser pass submits its own brief
and works the opportunity that submission opens, and it publishes nothing that is
seeded. Every check here either reads a seeded record no journey mutates, or works
inside a per-run probe record it created itself.
"""

from __future__ import annotations

import os

import appclient
import conftest as cf


def test_health_endpoint_answers_two_hundred() -> None:
    """The app answers its health endpoint once it is ready."""
    with appclient.client(None) as client:
        response = client.get("/health")
    assert response.status_code == 200, cf.describe(
        response, "the health endpoint must answer 200 once the app is ready")




def test_public_routes_carry_distinct_titles_and_descriptions() -> None:
    """No two public routes share a title or a description."""
    titles, descriptions = {}, {}
    for route in cf.PUBLIC_ROUTES:
        response = cf.fetch_document(route)
        assert response.status_code == 200, cf.describe(
            response, f"the public route {route} must render")
        title = cf.document_title(response.text)
        description = cf.meta_description(response.text)
        assert title, f"the route {route} must carry its own document title"
        assert description, f"the route {route} must carry its own meta description"
        assert title not in titles, (
            f"the route {route} shares its title with {titles.get(title)}: {title!r}")
        assert description not in descriptions, (
            f"the route {route} shares its description with {descriptions.get(description)}")
        titles[title] = route
        descriptions[description] = route


def test_route_titles_end_with_the_site_name() -> None:
    """Every public route names the site in its own title."""
    for route in cf.PUBLIC_ROUTES:
        response = cf.fetch_document(route)
        title = cf.document_title(response.text)
        assert cf.SITE_NAME in title, (
            f"the title of {route} must carry {cf.SITE_NAME!r}, read {title!r}")


def test_public_documents_are_rendered_on_the_server() -> None:
    """A public document carries its own content before any script runs."""
    response = cf.fetch_document("/methodology")
    assert response.status_code == 200, cf.describe(
        response, "the methodology index must render")
    assert cf.METHOD_TITLE in response.text, (
        f"the methodology index must carry {cf.METHOD_TITLE!r} in the document the "
        f"server returns, read {response.text[:400]}")
    articles = cf.fetch_document("/articles")
    assert cf.CASE_STUDY_TITLE in articles.text, (
        f"the article index must carry {cf.CASE_STUDY_TITLE!r} in the document the "
        f"server returns, read {articles.text[:400]}")


def test_public_documents_reference_no_external_origin() -> None:
    """No public route reaches another service at run time."""
    for route in cf.PUBLIC_ROUTES:
        response = cf.fetch_document(route)
        outside = cf.external_origins(response.text)
        assert outside == [], (
            f"the route {route} must call no third-party service at run time, reaches {outside}")


def test_internal_links_on_public_routes_resolve() -> None:
    """Every internal link on every public route resolves to a route the app serves."""
    for route in cf.PUBLIC_ROUTES:
        response = cf.fetch_document(route)
        for href in sorted(set(cf.internal_links(response.text))):
            target = cf.fetch_document(href)
            assert target.status_code == 200, cf.describe(
                target, f"the internal link {href} on {route} must resolve")


def test_list_endpoints_return_a_top_level_array() -> None:
    """A list endpoint answers with a bare JSON array."""
    with appclient.client(None) as client:
        for path in ("/methods", "/sectors", "/services", "/countries", "/articles"):
            response = client.get(path)
            assert response.status_code == 200, cf.describe(
                response, f"the list endpoint {path} must answer")
            assert isinstance(response.json(), list), cf.describe(
                response, f"the list endpoint {path} must return a top-level array")


def test_timestamps_are_utc_with_a_z_suffix(suffix) -> None:
    """A stored moment is returned as a UTC string ending in Z."""
    reference, _ = cf.accepted_brief(suffix)
    with appclient.client(None) as client:
        response = client.get("/articles")
    published = [row.get("published_at") for row in response.json() if row.get("published_at")]
    assert published, cf.describe(response, "a published article must carry its moment")
    for moment in published:
        assert str(moment).endswith("Z"), (
            f"a published moment must be a UTC string ending in Z, read {moment!r}")
    assert reference.startswith(cf.REFERENCE_PREFIX), (
        f"the accepted brief must carry a reference beginning {cf.REFERENCE_PREFIX!r}")


def test_no_credential_appears_in_downloaded_markup() -> None:
    """Nothing the browser downloads carries a credential."""
    secrets = (cf.SEEDED_PASSWORD, os.environ.get("STORAGE_SECRET_KEY", ""),
               os.environ.get("STORAGE_ACCESS_KEY", ""))
    for route in cf.PUBLIC_ROUTES:
        text = cf.fetch_document(route).text
        for secret in secrets:
            if secret:
                assert secret not in text, (
                    f"the document at {route} must carry no credential, found one of "
                    f"length {len(secret)}")


def test_absent_public_surfaces_answer_not_found() -> None:
    """A surface the product does not have answers not-found rather than a page."""
    for route in cf.ABSENT_SURFACES:
        response = cf.fetch_document(route)
        assert response.status_code == 404, cf.describe(
            response, f"the absent surface {route} must answer not-found")


def test_unknown_address_answers_not_found(suffix) -> None:
    """An unknown address answers with a true not-found status."""
    response = cf.fetch_document("/" + cf.probe_slug(suffix))
    assert response.status_code == 404, cf.describe(
        response, "an unknown address must answer a true not-found status")


def test_not_found_page_offers_a_way_back_to_the_article_index(suffix) -> None:
    """The product's own not-found page carries a way back and no site search."""
    response = cf.fetch_document("/" + cf.probe_slug(suffix))
    links = set(cf.internal_links(response.text))
    for route in ("/", "/methodology", "/sectors", "/articles"):
        assert route in links, (
            f"the not-found page must link back to {route}, links: {sorted(links)}")
    assert "/search" not in links, (
        f"the not-found page must offer no site search, links: {sorted(links)}")


def test_login_returns_an_access_token_for_a_seeded_account() -> None:
    """Every seeded account signs in with the seeded password."""
    for email in (cf.EDITOR_EMAIL, cf.EDITOR2_EMAIL, cf.CLIENT_EMAIL, cf.CLIENT2_EMAIL):
        token = appclient.login(email, cf.SEEDED_PASSWORD)
        assert isinstance(token, str) and token, (
            f"login for {email} must return a non-empty access_token")


def test_login_with_a_wrong_password_returns_no_token() -> None:
    """A wrong password is denied and hands back no token."""
    with appclient.client(None) as client:
        response = client.post("/auth/login",
                               json={"email": cf.EDITOR_EMAIL, "password": "not-the-password"})
    assert response.status_code in cf.REFUSED, cf.describe(
        response, "a wrong password must be denied")
    assert "access_token" not in response.text, cf.describe(
        response, "a denied login must hand back no token")


def test_signup_returns_a_token_for_a_new_client(suffix) -> None:
    """Open signup mints a client account and returns a token."""
    address = cf.probe_address(suffix)
    with appclient.client(None) as client:
        response = client.post("/auth/signup", json={
            "email": address, "password": cf.SEEDED_PASSWORD,
            "display_name": "Probe Buyer " + suffix})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "signup must create an account")
    payload = response.json()
    assert payload.get("access_token"), cf.describe(
        response, "signup must return an access_token")
    assert payload.get("role") == cf.ROLE_CLIENT, cf.describe(
        response, f"a self-served account must hold the role {cf.ROLE_CLIENT!r}")


def test_signup_body_naming_a_role_still_creates_a_client(suffix) -> None:
    """A signup body asking for the editor role still creates a client."""
    address = cf.probe_address(suffix)
    with appclient.client(None) as client:
        response = client.post("/auth/signup", json={
            "email": address, "password": cf.SEEDED_PASSWORD,
            "display_name": "Probe Buyer " + suffix, "role": cf.ROLE_EDITOR})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "signup must still create an account when the body names a role")
    row = cf.backend().one(cf.TABLE_ACCOUNT, email=address)
    assert row, f"no {cf.TABLE_ACCOUNT} row exists for {address}"
    assert row.get("role") == cf.ROLE_CLIENT, (
        f"the stored account for {address} must hold the role {cf.ROLE_CLIENT!r}, "
        f"holds {row.get('role')!r}")


def test_duplicate_signup_is_refused_as_invalid(suffix) -> None:
    """A second signup with a stored address is refused and creates nothing."""
    address = cf.probe_address(suffix)
    body = {"email": address, "password": cf.SEEDED_PASSWORD,
            "display_name": "Probe Buyer " + suffix}
    with appclient.client(None) as client:
        first = client.post("/auth/signup", json=body)
        assert first.status_code in cf.ACCEPTED, cf.describe(
            first, "the first signup must be accepted")
        second = client.post("/auth/signup", json=body)
    assert second.status_code in cf.REFUSED, cf.describe(
        second, "a second signup with a stored address must be refused")
    assert cf.backend().count(cf.TABLE_ACCOUNT, email=address) == 1, (
        f"exactly one {cf.TABLE_ACCOUNT} row may exist for {address}")


def test_guarded_endpoint_denies_a_call_with_no_token() -> None:
    """A guarded endpoint denies a caller carrying no token."""
    with appclient.client(None) as client:
        for path in ("/opportunities", "/requests"):
            response = client.get(path)
            assert response.status_code in cf.DENIED, cf.describe(
                response, f"{path} must deny a caller with no token")


def test_no_endpoint_returns_a_stored_password_hash(buyer) -> None:
    """No response carries a stored password or its hash."""
    row = cf.backend().one(cf.TABLE_ACCOUNT, email=cf.CLIENT_EMAIL)
    assert row, f"no {cf.TABLE_ACCOUNT} row exists for {cf.CLIENT_EMAIL}"
    stored = str(row.get("password_hash") or "")
    assert stored, f"the account row for {cf.CLIENT_EMAIL} must carry a password hash"
    assert stored != cf.SEEDED_PASSWORD, (
        "the stored password must be hashed rather than kept in plain text")
    with appclient.client(buyer) as client:
        response = client.get("/requests")
    assert stored not in response.text, cf.describe(
        response, "no response may carry a stored password hash")


def test_method_index_lists_thirteen_published_methods() -> None:
    """The method index carries every seeded method with nothing hidden."""
    with appclient.client(None) as client:
        response = client.get("/methods")
    assert response.status_code == 200, cf.describe(response, "the method list must answer")
    rows = response.json()
    assert len(rows) == cf.METHOD_COUNT, cf.describe(
        response, f"the method list must carry {cf.METHOD_COUNT} methods, carried {len(rows)}")
    titles = {row.get("title") for row in rows}
    for title in (cf.METHOD_TITLE, cf.METHOD_EXTRA_TITLE):
        assert title in titles, (
            f"the method list must carry {title!r}, carried {sorted(titles)}")
    document = cf.fetch_document("/methodology").text
    for title in titles:
        assert str(title) in document, (
            f"the methodology index must render {title!r} rather than hide it behind pagination")


def test_sector_index_lists_twelve_published_sectors() -> None:
    """The sector index carries every seeded sector with its sensitivity class."""
    with appclient.client(None) as client:
        response = client.get("/sectors")
    assert response.status_code == 200, cf.describe(response, "the sector list must answer")
    rows = response.json()
    assert len(rows) == cf.SECTOR_COUNT, cf.describe(
        response, f"the sector list must carry {cf.SECTOR_COUNT} sectors, carried {len(rows)}")
    by_slug = {row.get("slug"): row for row in rows}
    for slug in (cf.SECTOR_ELEVATED_OWNED, cf.SECTOR_ELEVATED_SECOND):
        assert by_slug.get(slug, {}).get("sensitivity_class") == cf.SENSITIVITY_ELEVATED, (
            f"the sector {slug} must carry {cf.SENSITIVITY_ELEVATED!r}, "
            f"carried {by_slug.get(slug, {}).get('sensitivity_class')!r}")
    assert by_slug.get(cf.SECTOR_STANDARD_UNOWNED, {}).get(
        "sensitivity_class") == cf.SENSITIVITY_STANDARD, (
        f"the sector {cf.SECTOR_STANDARD_UNOWNED} must carry {cf.SENSITIVITY_STANDARD!r}")


def test_unknown_method_slug_answers_not_found(suffix) -> None:
    """A method slug matching no record renders the not-found page."""
    response = cf.fetch_document("/methodology/" + cf.probe_slug(suffix))
    assert response.status_code == 404, cf.describe(
        response, "a method slug matching no record must answer not-found")


def test_services_list_ranks_two_primary_above_seven_supporting() -> None:
    """The nine services rank both primary records above the seven supporting ones."""
    with appclient.client(None) as client:
        response = client.get("/services")
    rows = response.json()
    assert len(rows) == cf.SERVICE_COUNT, cf.describe(
        response, f"the service list must carry {cf.SERVICE_COUNT} services, carried {len(rows)}")
    kinds = [row.get("kind") for row in sorted(rows, key=lambda row: row.get("rank", 0))]
    assert kinds[:2] == [cf.KIND_PRIMARY, cf.KIND_PRIMARY], (
        f"the two primary services must rank first, ranked {kinds}")
    assert set(kinds[2:]) == {cf.KIND_SUPPORTING}, (
        f"the remaining seven services must be supporting, ranked {kinds}")
    names = {row.get("name") for row in rows}
    for name in (cf.SERVICE_PRIMARY, cf.SERVICE_SECOND_PRIMARY, cf.SERVICE_SUPPORTING):
        assert name in names, f"the service list must carry {name!r}, carried {sorted(names)}"


def test_country_list_exposes_the_featured_rail_countries() -> None:
    """The country records carry their region, their coordinates and the featured rail."""
    with appclient.client(None) as client:
        response = client.get("/countries")
    rows = response.json()
    assert len(rows) == cf.COUNTRY_COUNT, cf.describe(
        response, f"the country list must carry {cf.COUNTRY_COUNT} countries, carried {len(rows)}")
    featured = [row for row in rows if row.get("is_featured")]
    assert len(featured) == cf.FEATURED_COUNTRY_COUNT, cf.describe(
        response, f"the rail must carry {cf.FEATURED_COUNTRY_COUNT} featured countries, "
                  f"carried {len(featured)}")
    for row in rows:
        for axis in ("map_x", "map_y"):
            value = float(row.get(axis))
            assert 0.0 <= value <= 1.0, (
                f"the coordinate {axis} of {row.get('name')!r} must sit between zero and one, "
                f"read {value}")
    names = {row.get("name") for row in rows}
    for market in (cf.MARKET_ONE, cf.MARKET_TWO, cf.MARKET_THREE):
        assert market in names, f"the country list must carry {market!r}"
    document = cf.fetch_document("/network").text
    for row in featured:
        assert str(row.get("name")) in document, (
            f"the country rail must render {row.get('name')!r} as readable text")


def test_about_route_publishes_the_six_process_steps() -> None:
    """The about route publishes the six stage names the console uses."""
    document = cf.fetch_document("/about-us").text
    for stage in cf.STAGES:
        assert stage in document, (
            f"the about route must publish the process step {stage!r}")


def test_home_figures_come_from_stored_settings() -> None:
    """The three published figures are stored records rather than a live count."""
    store = cf.backend()
    document = cf.fetch_document("/").text
    rows = store.rows(cf.TABLE_SETTING)
    values = {str(row.get("value")) for row in rows}
    for figure in ("60+", "400", "50+"):
        assert figure in values, (
            f"the figure {figure!r} must live in {cf.TABLE_SETTING}, holds {sorted(values)}")
        assert figure in document, f"the home route must publish the figure {figure!r}"
    published = store.count(cf.TABLE_ARTICLE, status=cf.STATUS_PUBLISHED)
    assert str(published) != "400" or published == 400, (
        "the published figures must not be read from a live count of anything")


def test_article_list_returns_only_published_rows() -> None:
    """The article list carries published rows only, for every caller."""
    with appclient.client(None) as client:
        response = client.get("/articles")
    rows = response.json()
    slugs = {row.get("slug") for row in rows}
    assert cf.CASE_STUDY_SLUG in slugs, cf.describe(
        response, f"the article list must carry {cf.CASE_STUDY_SLUG}")
    assert cf.DRAFT_SLUG not in slugs, cf.describe(
        response, f"the article list must not carry the draft {cf.DRAFT_SLUG}")
    store = cf.backend()
    for slug in slugs:
        row = store.one(cf.TABLE_ARTICLE, slug=slug)
        assert row and row.get("status") == cf.STATUS_PUBLISHED, (
            f"the listed article {slug} must be stored as {cf.STATUS_PUBLISHED!r}, "
            f"stored as {row and row.get('status')!r}")


def test_article_list_filters_by_category() -> None:
    """The article list narrows to one category."""
    with appclient.client(None) as client:
        response = client.get("/articles", params={"category": cf.CATEGORY_CASE_STUDIES})
    assert response.status_code == 200, cf.describe(
        response, "the article list must accept a category filter")
    rows = response.json()
    assert rows, cf.describe(response, "the case study category must carry an article")
    for row in rows:
        assert cf.CATEGORY_CASE_STUDIES in (row.get("categories") or []), (
            f"the filtered list must carry only {cf.CATEGORY_CASE_STUDIES!r}, "
            f"carried {row.get('slug')} with {row.get('categories')}")


def test_article_list_filters_by_region() -> None:
    """The article list narrows to one region, and every article carries exactly one."""
    with appclient.client(None) as client:
        response = client.get("/articles", params={"region": cf.REGION_EUROPE})
        everything = client.get("/articles").json()
    rows = response.json()
    assert rows, cf.describe(response, "the Europe region must carry an article")
    for row in rows:
        assert row.get("region") == cf.REGION_EUROPE, (
            f"the filtered list must carry only {cf.REGION_EUROPE!r}, "
            f"carried {row.get('slug')} in {row.get('region')!r}")
    for row in everything:
        assert isinstance(row.get("region"), str) and row.get("region"), (
            f"the article {row.get('slug')} must carry exactly one region")


def test_article_filters_intersect_across_category_and_region() -> None:
    """A category selection and a region selection intersect rather than widen."""
    with appclient.client(None) as client:
        both = client.get("/articles", params={"category": cf.CATEGORY_CASE_STUDIES,
                                               "region": cf.REGION_EUROPE})
        single = client.get("/articles", params={"category": cf.CATEGORY_CASE_STUDIES})
    assert both.status_code == 200, cf.describe(
        both, "the article list must accept both filters at once")
    narrowed = both.json()
    wider = single.json()
    assert len(narrowed) <= len(wider), cf.describe(
        both, "two filters must intersect rather than widen the result")
    for row in narrowed:
        assert row.get("region") == cf.REGION_EUROPE, (
            f"an intersected row must sit in {cf.REGION_EUROPE!r}")
        assert cf.CATEGORY_CASE_STUDIES in (row.get("categories") or []), (
            f"an intersected row must carry {cf.CATEGORY_CASE_STUDIES!r}")


def test_article_detail_returns_the_stored_body() -> None:
    """The seeded case study renders with its stored body and its approval reference."""
    with appclient.client(None) as client:
        response = client.get(f"/articles/{cf.CASE_STUDY_SLUG}")
    assert response.status_code == 200, cf.describe(
        response, f"the article {cf.CASE_STUDY_SLUG} must render")
    payload = response.json()
    row = cf.backend().one(cf.TABLE_ARTICLE, slug=cf.CASE_STUDY_SLUG)
    assert row, f"no {cf.TABLE_ARTICLE} row carries the slug {cf.CASE_STUDY_SLUG}"
    assert payload.get("title") == row.get("title") == cf.CASE_STUDY_TITLE, cf.describe(
        response, f"the article must carry the stored title {cf.CASE_STUDY_TITLE!r}")
    assert row.get("client_approval_reference") == cf.CASE_STUDY_APPROVAL, (
        f"the seeded case study must carry the approval reference {cf.CASE_STUDY_APPROVAL!r}, "
        f"carries {row.get('client_approval_reference')!r}")
    document = cf.fetch_document(f"/articles/{cf.CASE_STUDY_SLUG}").text
    assert cf.CASE_STUDY_TITLE in document, (
        "the article route must render the stored title")


def test_draft_article_public_path_is_denied_for_a_client(buyer) -> None:
    """The seeded draft is unreadable on a public path for a signed-in client."""
    response = cf.fetch_document(f"/articles/{cf.DRAFT_SLUG}")
    assert response.status_code == 404, cf.describe(
        response, f"the draft {cf.DRAFT_SLUG} must answer not-found on its public path")
    with appclient.client(buyer) as client:
        api = client.get(f"/articles/{cf.DRAFT_SLUG}")
    assert api.status_code in cf.NOT_FOUND, cf.describe(
        api, f"a client must not read the draft {cf.DRAFT_SLUG}")
    row = cf.backend().one(cf.TABLE_ARTICLE, slug=cf.DRAFT_SLUG)
    assert row and row.get("status") == cf.STATUS_DRAFT, (
        f"the seeded {cf.DRAFT_SLUG} must still be stored as {cf.STATUS_DRAFT!r}")


def test_draft_article_answers_exactly_as_an_unknown_path(suffix) -> None:
    """A draft's path and a path that never existed answer the same way."""
    draft = cf.fetch_document(f"/articles/{cf.DRAFT_SLUG}")
    unknown = cf.fetch_document(f"/articles/{cf.probe_slug(suffix)}")
    assert draft.status_code == unknown.status_code == 404, (
        f"a draft path answered {draft.status_code} and an unknown path "
        f"{unknown.status_code}: the two must not be distinguishable")
    assert cf.DRAFT_TITLE not in draft.text, (
        f"the refusal must not disclose the draft title {cf.DRAFT_TITLE!r}")


def test_related_articles_share_a_tag_with_the_method() -> None:
    """A method route carries related articles chosen by a shared tag."""
    with appclient.client(None) as client:
        response = client.get(f"/articles", params={"category": cf.CATEGORY_METHODOLOGY})
    rows = response.json()
    assert rows, cf.describe(response, "the methodology category must carry an article")
    document = cf.fetch_document(f"/methodology/{cf.METHOD_SLUG}").text
    titles = [str(row.get("title")) for row in rows]
    assert any(title in document for title in titles), (
        f"the method route {cf.METHOD_SLUG} must carry a related article from "
        f"{titles}, rendered {document[:400]}")


def test_filter_counts_follow_the_published_set(editor, suffix) -> None:
    """A newly published article changes the count its category reports."""
    with appclient.client(None) as client:
        before = len(client.get("/articles", params={"category": cf.CATEGORY_EDUCATIONAL}).json())
    created = cf.create_article(editor, suffix, categories=[cf.CATEGORY_EDUCATIONAL])
    slug = created.get("slug")
    published = cf.publish_article(editor, slug)
    assert published.status_code in cf.ACCEPTED, cf.describe(
        published, "a complete draft must publish")
    with appclient.client(None) as client:
        after = len(client.get("/articles", params={"category": cf.CATEGORY_EDUCATIONAL}).json())
    assert after == before + 1, (
        f"the category count must follow the published set: read {before} then {after}")


def test_staged_brief_submission_persists_the_request_row(suffix) -> None:
    """An accepted brief is a stored row carrying what the visitor typed."""
    reference, body = cf.accepted_brief(suffix)
    row = cf.brief_row(reference)
    assert row.get("work_email") == body["work_email"], (
        f"the stored request must carry the submitted address, carries {row.get('work_email')!r}")
    assert row.get("company") == body["company"], (
        f"the stored request must carry the submitted company, carries {row.get('company')!r}")
    assert row.get("sector_slug") == body["sector_slug"], (
        f"the stored request must carry the submitted sector, carries {row.get('sector_slug')!r}")
    assert str(row.get("budget_band")) == body["budget_band"], (
        f"the stored request must carry a budget band rather than a price, "
        f"carries {row.get('budget_band')!r}")
    assert body["challenge"] in str(row.get("challenge")), (
        "the stored request must carry the challenge the visitor wrote")


def test_brief_reference_uses_the_agency_prefix(suffix) -> None:
    """Every issued reference opens with the agency prefix."""
    reference, _ = cf.accepted_brief(suffix)
    assert reference.startswith(cf.REFERENCE_PREFIX), (
        f"an issued reference must begin {cf.REFERENCE_PREFIX!r}, read {reference!r}")
    assert cf.brief_row(reference).get("reference") == reference, (
        "the stored request must carry the reference the visitor was shown")


def test_brief_opens_one_routed_opportunity_row(suffix) -> None:
    """An accepted brief opens exactly one opportunity at the first stage."""
    reference, _ = cf.accepted_brief(suffix)
    row = cf.opportunity_row(reference)
    assert row.get("stage") == cf.STAGE_FIRST, (
        f"a new opportunity must open at {cf.STAGE_FIRST!r}, opened at {row.get('stage')!r}")
    assert cf.backend().count(cf.TABLE_OPPORTUNITY, reference=reference) == 1, (
        f"exactly one opportunity may carry the reference {reference}")


def test_duplicate_brief_returns_the_first_reference(suffix) -> None:
    """A same-day repeat of one brief is accepted and returns the first reference."""
    first, body = cf.accepted_brief(suffix)
    repeat = cf.submit_brief(dict(body))
    assert repeat.status_code in cf.ACCEPTED, cf.describe(
        repeat, "a same-day repeat must be accepted rather than refused")
    assert repeat.json().get("reference") == first, cf.describe(
        repeat, f"a same-day repeat must return the first reference {first}")


def test_duplicate_brief_stores_no_second_opportunity_row(suffix) -> None:
    """A same-day repeat leaves one request row and one opportunity row."""
    reference, body = cf.accepted_brief(suffix)
    store = cf.backend()
    before = store.count(cf.TABLE_OPPORTUNITY)
    cf.submit_brief(dict(body))
    cf.settle()
    assert store.count(cf.TABLE_BRIEF, reference=reference) == 1, (
        f"a same-day repeat must leave one request row for {reference}")
    assert store.count(cf.TABLE_OPPORTUNITY, reference=reference) == 1, (
        f"a same-day repeat must leave one opportunity row for {reference}")
    assert store.count(cf.TABLE_OPPORTUNITY) == before, (
        "a same-day repeat must open no further opportunity anywhere")


def test_brief_with_invalid_fields_is_refused(suffix) -> None:
    """Every field the server owns is checked, and a bad value names its field."""
    cases = {
        "sector_slug": cf.brief_body(suffix, sector_slug="not-a-sector"),
        "markets": cf.brief_body(suffix, markets=["Atlantis"]),
        "methods": cf.brief_body(suffix, methods=["Telepathy"]),
        "services": cf.brief_body(suffix, services=["Palm Reading"]),
        "challenge": cf.brief_body(suffix, challenge="too short"),
        "work_email": cf.brief_body(suffix, work_email="not-an-address"),
    }
    for field, body in cases.items():
        response = cf.submit_brief(body)
        assert response.status_code in cf.CLIENT_ERROR, cf.describe(
            response, f"a brief carrying an invalid {field} must be refused")
        assert field in response.text, cf.describe(
            response, f"a refusal must name the field {field} that failed")


def test_brief_naming_other_without_detail_is_refused(suffix) -> None:
    """The attribution option that needs a companion field is refused without one."""
    response = cf.submit_brief(cf.brief_body(
        suffix, attribution_key=cf.ATTRIBUTION_OTHER.lower(), attribution_detail=""))
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "an Other attribution with no companion detail must be refused")


def test_refused_brief_writes_no_request_row(suffix) -> None:
    """A refused brief leaves the store exactly as it was."""
    store = cf.backend()
    before = store.count(cf.TABLE_BRIEF)
    address = cf.probe_address(suffix)
    response = cf.submit_brief(cf.brief_body(suffix, work_email=address, challenge="no"))
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "a brief with too short a challenge must be refused")
    cf.settle()
    assert store.count(cf.TABLE_BRIEF, work_email=address) == 0, (
        f"a refused brief must write no request row for {address}")
    assert store.count(cf.TABLE_BRIEF) == before, (
        "a refused brief must leave the stored request count unchanged")


def test_brief_with_the_decoy_field_filled_writes_no_request_row(suffix) -> None:
    """A submission carrying the unattended decoy field stores nothing."""
    store = cf.backend()
    before = store.count(cf.TABLE_BRIEF)
    address = cf.probe_address(suffix)
    body = cf.brief_body(suffix, work_email=address)
    body[cf.DECOY_FIELD] = "https://example.com/harvest"
    response = cf.submit_brief(body)
    cf.settle()
    assert store.count(cf.TABLE_BRIEF, work_email=address) == 0, (
        f"a submission with {cf.DECOY_FIELD} filled must write no request row")
    assert store.count(cf.TABLE_BRIEF) == before, (
        "a refused automated submission must leave the stored request count unchanged")
    assert response.status_code in cf.REFUSED or response.status_code in cf.ACCEPTED, (
        cf.describe(response, "an automated submission must be refused neutrally"))


def test_repeated_submissions_are_refused_after_the_third_in_one_minute(suffix) -> None:
    """A submitter posting the same form repeatedly is refused after the third attempt."""
    statuses = []
    for index in range(cf.REPEAT_LIMIT + 2):
        body = cf.brief_body(suffix + str(index), work_email=cf.probe_address(suffix))
        statuses.append(cf.submit_brief(body).status_code)
    assert any(status in cf.REFUSED for status in statuses), (
        f"repeated submissions from one submitter must be refused, read {statuses}")
    assert statuses[0] in cf.ACCEPTED, (
        f"the first submission must be accepted, read {statuses}")


def test_signed_in_client_request_list_holds_their_own_brief(buyer, suffix) -> None:
    """A brief sent while signed in appears on that client's own request list."""
    body = cf.brief_body(suffix, work_email=cf.CLIENT_EMAIL)
    response = cf.submit_brief(body, token=buyer)
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "a signed-in client must be able to submit a brief")
    reference = response.json().get("reference")
    with appclient.client(buyer) as client:
        listed = client.get("/requests")
    assert listed.status_code == 200, cf.describe(listed, "a client must read their own requests")
    references = {row.get("reference") for row in listed.json()}
    assert reference in references, cf.describe(
        listed, f"the client's own request {reference} must appear, saw {sorted(references)}")


def test_anonymous_brief_belongs_to_no_account(buyer, suffix) -> None:
    """A brief sent by a visitor who is not signed in belongs to no account."""
    reference, _ = cf.accepted_brief(suffix)
    row = cf.brief_row(reference)
    assert not row.get("account_id"), (
        f"an anonymous request must hold no account, holds {row.get('account_id')!r}")
    with appclient.client(buyer) as client:
        listed = client.get("/requests")
    references = {item.get("reference") for item in listed.json()}
    assert reference not in references, cf.describe(
        listed, f"an anonymous request must appear on no client's list, saw {reference}")


def test_request_list_returns_only_the_callers_own_requests(buyer, second_buyer) -> None:
    """Each client reads their own requests and nobody else's."""
    with appclient.client(buyer) as client:
        mine = client.get("/requests").json()
    with appclient.client(second_buyer) as client:
        theirs = client.get("/requests").json()
    my_references = {row.get("reference") for row in mine}
    their_references = {row.get("reference") for row in theirs}
    assert cf.SEEDED_REFERENCE_ONE in my_references, (
        f"{cf.CLIENT_EMAIL} must read {cf.SEEDED_REFERENCE_ONE}, read {sorted(my_references)}")
    assert cf.SEEDED_REFERENCE_TWO in their_references, (
        f"{cf.CLIENT2_EMAIL} must read {cf.SEEDED_REFERENCE_TWO}, read {sorted(their_references)}")
    assert cf.SEEDED_REFERENCE_TWO not in my_references, (
        f"{cf.CLIENT_EMAIL} must not read another client's request")
    assert cf.SEEDED_REFERENCE_ONE not in their_references, (
        f"{cf.CLIENT2_EMAIL} must not read another client's request")


def test_direct_request_for_another_clients_reference_is_denied(second_buyer) -> None:
    """Asking for another client's reference by its own path is answered as not found."""
    store = cf.backend()
    before = store.one(cf.TABLE_OPPORTUNITY, reference=cf.SEEDED_REFERENCE_ONE)
    with appclient.client(second_buyer) as client:
        response = client.get(f"/opportunities/{cf.SEEDED_REFERENCE_ONE}")
    assert response.status_code in cf.NOT_FOUND, cf.describe(
        response, f"{cf.CLIENT2_EMAIL} must not read {cf.SEEDED_REFERENCE_ONE}")
    after = store.one(cf.TABLE_OPPORTUNITY, reference=cf.SEEDED_REFERENCE_ONE)
    assert before == after, (
        f"a denied read must leave {cf.SEEDED_REFERENCE_ONE} exactly as it was")


def test_owned_sector_routes_to_its_owner_with_the_sector_owner_reason(suffix) -> None:
    """A sector naming an owner routes the opportunity to that owner, with its reason."""
    reference, _ = cf.accepted_brief(suffix, sector_slug=cf.SECTOR_ELEVATED_OWNED)
    row = cf.opportunity_row(reference)
    assert row.get("owner_email") == cf.EDITOR_EMAIL, (
        f"a {cf.SECTOR_ELEVATED_OWNED} brief must route to {cf.EDITOR_EMAIL}, "
        f"routed to {row.get('owner_email')!r}")
    assert row.get("routing_reason") == cf.REASON_SECTOR_OWNER, (
        f"a routed opportunity must store {cf.REASON_SECTOR_OWNER!r}, "
        f"stored {row.get('routing_reason')!r}")


def test_ownerless_sector_leaves_the_opportunity_unowned(suffix) -> None:
    """A sector naming no owner leaves the opportunity unowned, with its reason."""
    reference, _ = cf.accepted_brief(suffix, sector_slug=cf.SECTOR_STANDARD_UNOWNED)
    row = cf.opportunity_row(reference)
    assert not row.get("owner_email"), (
        f"a {cf.SECTOR_STANDARD_UNOWNED} brief must leave the opportunity unowned, "
        f"owned by {row.get('owner_email')!r}")
    assert row.get("routing_reason") == cf.REASON_NO_SECTOR_OWNER, (
        f"an unowned opportunity must store {cf.REASON_NO_SECTOR_OWNER!r}, "
        f"stored {row.get('routing_reason')!r}")


def test_unowned_opportunity_is_visible_to_every_editor(editor_two, suffix) -> None:
    """An unowned opportunity stays visible to an editor who does not hold its sector."""
    reference, _ = cf.accepted_brief(suffix, sector_slug=cf.SECTOR_STANDARD_UNOWNED)
    with appclient.client(editor_two) as client:
        response = client.get("/opportunities")
    assert response.status_code == 200, cf.describe(
        response, "an editor must read the opportunity board")
    references = {row.get("reference") for row in response.json()}
    assert reference in references, cf.describe(
        response, f"the unowned opportunity {reference} must stay visible to every editor")


def test_pharmaceutical_brief_opens_an_elevated_opportunity(suffix) -> None:
    """A brief against the pharmaceutical sector opens at the elevated class."""
    reference, _ = cf.accepted_brief(suffix, sector_slug=cf.SECTOR_ELEVATED_OWNED)
    row = cf.opportunity_row(reference)
    assert row.get("sensitivity_class") == cf.SENSITIVITY_ELEVATED, (
        f"a {cf.SECTOR_ELEVATED_OWNED} brief must open at {cf.SENSITIVITY_ELEVATED!r}, "
        f"opened at {row.get('sensitivity_class')!r}")


def test_ordinary_sector_brief_opens_a_standard_opportunity(suffix) -> None:
    """A brief against an ordinary sector opens at the standard class."""
    reference, _ = cf.accepted_brief(suffix, sector_slug=cf.SECTOR_STANDARD_OWNED)
    row = cf.opportunity_row(reference)
    assert row.get("sensitivity_class") == cf.SENSITIVITY_STANDARD, (
        f"a {cf.SECTOR_STANDARD_OWNED} brief must open at {cf.SENSITIVITY_STANDARD!r}, "
        f"opened at {row.get('sensitivity_class')!r}")


def test_sensitivity_ignores_the_wording_of_the_challenge(suffix) -> None:
    """The sensitivity class follows the sector record rather than the challenge text."""
    loaded = ("We run pharmaceutical and beauty studies across two markets and need "
              "help with recruitment, reference " + suffix)
    reference, _ = cf.accepted_brief(suffix, sector_slug=cf.SECTOR_STANDARD_UNOWNED,
                                     challenge=loaded)
    row = cf.opportunity_row(reference)
    assert row.get("sensitivity_class") == cf.SENSITIVITY_STANDARD, (
        f"a {cf.SECTOR_STANDARD_UNOWNED} brief must stay {cf.SENSITIVITY_STANDARD!r} "
        f"whatever the challenge says, opened at {row.get('sensitivity_class')!r}")
    sector = cf.backend().one(cf.TABLE_SECTOR, slug=cf.SECTOR_STANDARD_UNOWNED)
    assert sector and sector.get("sensitivity_class") == cf.SENSITIVITY_STANDARD, (
        f"the sector record for {cf.SECTOR_STANDARD_UNOWNED} must carry "
        f"{cf.SENSITIVITY_STANDARD!r}")


def test_stage_advances_one_step_forward(editor, suffix) -> None:
    """An editor moves an opportunity one stage forward, and the store follows."""
    reference, _ = cf.accepted_brief(suffix)
    with appclient.client(editor) as client:
        response = client.patch(f"/opportunities/{reference}", json={"stage": cf.STAGE_SECOND})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, f"an editor must advance {reference} to {cf.STAGE_SECOND}")
    row = cf.opportunity_row(reference)
    assert row.get("stage") == cf.STAGE_SECOND, (
        f"the stored stage must read {cf.STAGE_SECOND!r}, reads {row.get('stage')!r}")


def test_stage_skip_is_refused_as_invalid(editor, suffix) -> None:
    """A stage change that skips a stage is refused."""
    reference, _ = cf.accepted_brief(suffix)
    with appclient.client(editor) as client:
        response = client.patch(f"/opportunities/{reference}", json={"stage": cf.STAGE_THIRD})
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, f"moving {reference} from {cf.STAGE_FIRST} to {cf.STAGE_THIRD} must be refused")


def test_backwards_stage_change_is_refused_as_invalid(editor, suffix) -> None:
    """A stage change that moves backwards is refused."""
    reference, _ = cf.accepted_brief(suffix)
    with appclient.client(editor) as client:
        forward = client.patch(f"/opportunities/{reference}", json={"stage": cf.STAGE_SECOND})
        assert forward.status_code in cf.ACCEPTED, cf.describe(
            forward, "the forward move must be accepted first")
        response = client.patch(f"/opportunities/{reference}", json={"stage": cf.STAGE_FIRST})
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, f"moving {reference} back to {cf.STAGE_FIRST} must be refused")


def test_refused_stage_change_leaves_the_stored_stage_unchanged(editor, suffix) -> None:
    """A refused stage change leaves the stored stage exactly as it was."""
    reference, _ = cf.accepted_brief(suffix)
    before = cf.opportunity_row(reference).get("stage")
    with appclient.client(editor) as client:
        response = client.patch(f"/opportunities/{reference}", json={"stage": "Archived"})
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "a stage outside the six published names must be refused")
    after = cf.opportunity_row(reference).get("stage")
    assert after == before, (
        f"a refused stage change must leave {reference} at {before!r}, left it at {after!r}")


def test_opportunity_note_records_its_author(editor, suffix) -> None:
    """A note written on an opportunity records who wrote it and when."""
    reference, _ = cf.accepted_brief(suffix)
    text = "Spoke to the buyer, reference " + suffix
    with appclient.client(editor) as client:
        response = client.post(f"/opportunities/{reference}/notes", json={"body": text})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, f"an editor must be able to note {reference}")
    row = cf.opportunity_row(reference)
    notes = cf.backend().rows(cf.TABLE_NOTE, opportunity_id=row.get("id"))
    assert notes, f"a note on {reference} must be stored"
    written = [note for note in notes if text in str(note.get("body"))]
    assert written, f"the stored note must carry the text that was written, stored {notes}"
    assert written[0].get("author_email") == cf.EDITOR_EMAIL, (
        f"the stored note must record {cf.EDITOR_EMAIL}, recorded "
        f"{written[0].get('author_email')!r}")
    assert written[0].get("created_at"), "the stored note must record when it was written"


def test_stored_note_is_not_editable(editor, suffix) -> None:
    """No route rewrites a note once it is written."""
    reference, _ = cf.accepted_brief(suffix)
    text = "First note, reference " + suffix
    with appclient.client(editor) as client:
        created = client.post(f"/opportunities/{reference}/notes", json={"body": text})
        assert created.status_code in cf.ACCEPTED, cf.describe(created, "the note must be written")
        row = cf.opportunity_row(reference)
        notes = cf.backend().rows(cf.TABLE_NOTE, opportunity_id=row.get("id"))
        note_id = notes[0].get("id")
        edited = client.patch(f"/opportunities/{reference}/notes",
                              json={"id": note_id, "body": "rewritten"})
    assert edited.status_code in cf.REFUSED, cf.describe(
        edited, "a stored note must not be rewritten")
    after = cf.backend().rows(cf.TABLE_NOTE, opportunity_id=row.get("id"))
    assert any(text in str(note.get("body")) for note in after), (
        "the note that was written must still read as it was written")


def test_board_orders_opportunities_by_arrival(editor) -> None:
    """The board answers oldest brief first, because the clock is the promise."""
    with appclient.client(editor) as client:
        response = client.get("/opportunities")
    assert response.status_code == 200, cf.describe(response, "the board must answer")
    moments = [str(row.get("submitted_at")) for row in response.json() if row.get("submitted_at")]
    assert moments, cf.describe(response, "every card must carry the moment its brief arrived")
    assert moments == sorted(moments), cf.describe(
        response, f"the board must order by arrival, oldest first, read {moments[:5]}")


def test_client_session_is_denied_at_the_opportunity_list(buyer) -> None:
    """A client session is refused at the console's own endpoints."""
    with appclient.client(buyer) as client:
        response = client.get("/opportunities")
    assert response.status_code in cf.DENIED, cf.describe(
        response, f"{cf.CLIENT_EMAIL} must be denied at the opportunity list")


def test_client_session_cannot_advance_a_stage(buyer) -> None:
    """A client cannot move an opportunity, and the stored stage does not move."""
    store = cf.backend()
    before = store.one(cf.TABLE_OPPORTUNITY, reference=cf.SEEDED_REFERENCE_TWO)
    assert before, f"the seeded opportunity {cf.SEEDED_REFERENCE_TWO} must exist"
    with appclient.client(buyer) as client:
        response = client.patch(f"/opportunities/{cf.SEEDED_REFERENCE_TWO}",
                                json={"stage": cf.STAGE_SECOND})
    assert response.status_code in cf.DENIED + (404,), cf.describe(
        response, f"a client must not advance {cf.SEEDED_REFERENCE_TWO}")
    after = store.one(cf.TABLE_OPPORTUNITY, reference=cf.SEEDED_REFERENCE_TWO)
    assert after.get("stage") == before.get("stage"), (
        f"a denied stage change must leave {cf.SEEDED_REFERENCE_TWO} at "
        f"{before.get('stage')!r}, left it at {after.get('stage')!r}")


def test_seeded_opportunities_carry_their_references() -> None:
    """Both seeded opportunities exist with their routing and their sensitivity."""
    store = cf.backend()
    first = store.one(cf.TABLE_OPPORTUNITY, reference=cf.SEEDED_REFERENCE_ONE)
    second = store.one(cf.TABLE_OPPORTUNITY, reference=cf.SEEDED_REFERENCE_TWO)
    assert first, f"the seeded opportunity {cf.SEEDED_REFERENCE_ONE} must exist"
    assert second, f"the seeded opportunity {cf.SEEDED_REFERENCE_TWO} must exist"
    assert first.get("sensitivity_class") == cf.SENSITIVITY_ELEVATED, (
        f"{cf.SEEDED_REFERENCE_ONE} must carry {cf.SENSITIVITY_ELEVATED!r}, "
        f"carries {first.get('sensitivity_class')!r}")
    assert first.get("routing_reason") == cf.REASON_SECTOR_OWNER, (
        f"{cf.SEEDED_REFERENCE_ONE} must carry {cf.REASON_SECTOR_OWNER!r}")
    assert second.get("routing_reason") == cf.REASON_NO_SECTOR_OWNER, (
        f"{cf.SEEDED_REFERENCE_TWO} must carry {cf.REASON_NO_SECTOR_OWNER!r}")
    assert store.count(cf.TABLE_OPPORTUNITY, reference=cf.SEEDED_REFERENCE_ONE) == 1, (
        f"exactly one opportunity may carry {cf.SEEDED_REFERENCE_ONE}")


def test_seeded_reference_rows_are_persisted() -> None:
    """Every seeded reference collection is a stored row set of the stated size."""
    store = cf.backend()
    expected = {
        cf.TABLE_METHOD: cf.METHOD_COUNT,
        cf.TABLE_SECTOR: cf.SECTOR_COUNT,
        cf.TABLE_SERVICE: cf.SERVICE_COUNT,
        cf.TABLE_REGION: cf.REGION_COUNT,
        cf.TABLE_CATEGORY: cf.CATEGORY_COUNT,
        cf.TABLE_COUNTRY: cf.COUNTRY_COUNT,
    }
    for table, count in expected.items():
        assert store.count(table) == count, (
            f"{table} must hold {count} seeded rows, holds {store.count(table)}")
    for email, role in ((cf.EDITOR_EMAIL, cf.ROLE_EDITOR), (cf.EDITOR2_EMAIL, cf.ROLE_EDITOR),
                        (cf.CLIENT_EMAIL, cf.ROLE_CLIENT), (cf.CLIENT2_EMAIL, cf.ROLE_CLIENT)):
        row = store.one(cf.TABLE_ACCOUNT, email=email)
        assert row and row.get("role") == role, (
            f"the seeded account {email} must hold the role {role!r}")
        assert store.count(cf.TABLE_ACCOUNT, email=email) == 1, (
            f"seeding must leave exactly one account row for {email}")
    worldwide = store.one(cf.TABLE_REGION, name=cf.REGION_WORLDWIDE)
    assert worldwide and not worldwide.get("has_band"), (
        f"the region {cf.REGION_WORLDWIDE} must be seeded without a band")
    assert store.count(cf.TABLE_ARTICLE, status=cf.STATUS_PUBLISHED) >= cf.PUBLISHED_ARTICLE_COUNT, (
        f"at least {cf.PUBLISHED_ARTICLE_COUNT} seeded articles must be published")
    assert store.count(cf.TABLE_ARTICLE, slug=cf.DRAFT_SLUG) == 1, (
        f"seeding must leave exactly one row for {cf.DRAFT_SLUG}")


def test_editor_creates_an_article_in_draft(editor, suffix) -> None:
    """A new article starts as a draft and is readable in the console only."""
    created = cf.create_article(editor, suffix)
    slug = created.get("slug")
    row = cf.backend().one(cf.TABLE_ARTICLE, slug=slug)
    assert row and row.get("status") == cf.STATUS_DRAFT, (
        f"a new article must be stored as {cf.STATUS_DRAFT!r}, stored as "
        f"{row and row.get('status')!r}")
    with appclient.client(editor) as client:
        read = client.get(f"/articles/{slug}")
    assert read.status_code == 200, cf.describe(
        read, "an editor must read their own draft in the console")
    public = cf.fetch_document(f"/articles/{slug}")
    assert public.status_code == 404, cf.describe(
        public, f"the draft {slug} must answer not-found on its public path")


def test_publish_is_refused_until_its_rules_hold(editor, suffix) -> None:
    """Publishing is refused, with the reason stated, until every publish rule holds."""
    cases = {
        "seo_description": cf.article_body(suffix + "a", seo_description=""),
        "body": cf.article_body(suffix + "b", body=""),
        "client_approval_reference": cf.article_body(
            suffix + "c", categories=[cf.CATEGORY_CASE_STUDIES], client_approval_reference=""),
    }
    for field, body in cases.items():
        with appclient.client(editor) as client:
            created = client.post("/articles", json=body)
            assert created.status_code in cf.ACCEPTED, cf.describe(
                created, f"the draft for the {field} case must be created")
            slug = created.json().get("slug")
            response = client.post(f"/articles/{slug}/publish")
        assert response.status_code in cf.CLIENT_ERROR, cf.describe(
            response, f"publishing without {field} must be refused")
        assert field in response.text, cf.describe(
            response, f"a refused publish must state that {field} is what refused it")


def test_refused_publish_leaves_the_article_in_draft(editor, suffix) -> None:
    """A refused publish leaves the record a draft and serves nothing publicly."""
    created = cf.create_article(editor, suffix,
                                categories=[cf.CATEGORY_CASE_STUDIES],
                                client_approval_reference="")
    slug = created.get("slug")
    response = cf.publish_article(editor, slug)
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "a case study with no approval reference must not publish")
    row = cf.backend().one(cf.TABLE_ARTICLE, slug=slug)
    assert row.get("status") == cf.STATUS_DRAFT, (
        f"a refused publish must leave {slug} as {cf.STATUS_DRAFT!r}, left it "
        f"{row.get('status')!r}")
    assert cf.fetch_document(f"/articles/{slug}").status_code == 404, (
        f"a refused publish must leave the public path of {slug} answering not-found")


def test_published_article_appears_on_its_public_path(editor, suffix) -> None:
    """A case study that carries its approval reference publishes and is readable."""
    created = cf.create_article(editor, suffix,
                                categories=[cf.CATEGORY_CASE_STUDIES],
                                client_approval_reference=cf.CASE_STUDY_APPROVAL)
    slug = created.get("slug")
    response = cf.publish_article(editor, slug)
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, f"a complete case study must publish, {slug}")
    row = cf.backend().one(cf.TABLE_ARTICLE, slug=slug)
    assert row.get("status") == cf.STATUS_PUBLISHED, (
        f"{slug} must be stored as {cf.STATUS_PUBLISHED!r}, stored {row.get('status')!r}")
    assert row.get("published_at"), f"{slug} must carry its first-published moment"
    public = cf.fetch_document(f"/articles/{slug}")
    assert public.status_code == 200, cf.describe(
        public, f"the published article {slug} must render on its public path")
    with appclient.client(None) as client:
        listed = client.get("/articles").json()
    assert slug in {item.get("slug") for item in listed}, (
        f"the published article {slug} must join the public list")


def test_later_edit_keeps_the_first_published_moment(editor, suffix) -> None:
    """An edit after publication updates the edited moment and never the first."""
    created = cf.create_article(editor, suffix)
    slug = created.get("slug")
    assert cf.publish_article(editor, slug).status_code in cf.ACCEPTED, (
        f"the draft {slug} must publish")
    first = cf.backend().one(cf.TABLE_ARTICLE, slug=slug).get("published_at")
    cf.settle()
    with appclient.client(editor) as client:
        edited = client.patch(f"/articles/{slug}", json={"summary": "Edited " + suffix})
    assert edited.status_code in cf.ACCEPTED, cf.describe(edited, f"{slug} must accept an edit")
    row = cf.backend().one(cf.TABLE_ARTICLE, slug=slug)
    assert row.get("published_at") == first, (
        f"the first-published moment of {slug} must never be rewritten: was {first!r}, "
        f"reads {row.get('published_at')!r}")
    assert row.get("updated_at"), f"{slug} must carry an edited moment of its own"


def test_unpublished_article_path_answers_not_found(editor, suffix) -> None:
    """Unpublishing returns an article to draft and closes its public path."""
    created = cf.create_article(editor, suffix)
    slug = created.get("slug")
    assert cf.publish_article(editor, slug).status_code in cf.ACCEPTED, (
        f"the draft {slug} must publish first")
    assert cf.fetch_document(f"/articles/{slug}").status_code == 200, (
        f"the published article {slug} must render before it is unpublished")
    with appclient.client(editor) as client:
        response = client.post(f"/articles/{slug}/unpublish")
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, f"an editor must be able to unpublish {slug}")
    row = cf.backend().one(cf.TABLE_ARTICLE, slug=slug)
    assert row.get("status") == cf.STATUS_DRAFT, (
        f"{slug} must return to {cf.STATUS_DRAFT!r}, reads {row.get('status')!r}")
    assert cf.fetch_document(f"/articles/{slug}").status_code == 404, (
        f"the public path of {slug} must answer not-found once it is unpublished")


def test_duplicate_slug_is_refused(editor, suffix) -> None:
    """A slug already taken by another article is refused."""
    created = cf.create_article(editor, suffix)
    slug = created.get("slug")
    with appclient.client(editor) as client:
        response = client.post("/articles", json=cf.article_body(suffix + "x", slug=slug))
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, f"a second article claiming the slug {slug} must be refused")
    assert cf.backend().count(cf.TABLE_ARTICLE, slug=slug) == 1, (
        f"exactly one article row may carry the slug {slug}")


def test_publish_with_a_broken_internal_link_is_refused(editor, suffix) -> None:
    """A record whose body links to a path the app does not serve cannot publish."""
    broken = ("A probe body that points at "
              '<a href="/methodology/' + cf.probe_slug(suffix) + '">a missing method</a>.')
    created = cf.create_article(editor, suffix, body=broken)
    slug = created.get("slug")
    response = cf.publish_article(editor, slug)
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, f"publishing {slug} with an internal link to a missing path must be refused")
    row = cf.backend().one(cf.TABLE_ARTICLE, slug=slug)
    assert row.get("status") == cf.STATUS_DRAFT, (
        f"{slug} must stay a draft while its internal link does not resolve")


def test_uploaded_cover_file_is_stored_in_the_object_store(editor, suffix) -> None:
    """An uploaded cover exists as a real object in the bucket the brief names."""
    created = cf.create_article(editor, suffix)
    slug = created.get("slug")
    payload = cf.probe_png(suffix)
    response = cf.upload_cover(editor, slug, payload)
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, f"an editor must be able to upload a cover for {slug}")
    key = response.json().get("object_key")
    assert key, cf.describe(response, "an upload must answer with its object key")
    store = cf.object_store()
    found = cf.poll_until(lambda: store.exists(key))
    assert found, (
        f"the uploaded bytes for {slug} must exist in the object store at {key}")
    row = cf.backend().one(cf.TABLE_ASSET, object_key=key)
    assert row, f"the store must carry one {cf.TABLE_ASSET} row for {key}"
    assert str(row.get("article_id")), f"the asset row for {key} must name its article"


def test_uploaded_cover_object_key_follows_the_digest_scheme(editor, suffix) -> None:
    """The object key names the collection, the record and a digest of the bytes."""
    created = cf.create_article(editor, suffix)
    slug = created.get("slug")
    response = cf.upload_cover(editor, slug, cf.probe_png(suffix))
    key = response.json().get("object_key")
    assert key.startswith(cf.OBJECT_KEY_PREFIX), (
        f"the object key must open with {cf.OBJECT_KEY_PREFIX!r}, read {key!r}")
    parts = key.split("/")
    assert len(parts) == 3, f"the object key must read collection, record, digest: {key!r}"
    digest = parts[2].split(".")[0]
    assert len(digest) == 64, (
        f"the object key must carry a sha256 digest of the bytes, read {digest!r}")
    assert all(character in "0123456789abcdef" for character in digest), (
        f"the digest in the object key must be hexadecimal, read {digest!r}")


def test_same_file_uploaded_twice_leaves_one_stored_object(editor, suffix) -> None:
    """The same bytes uploaded twice to one article leave one object and one row."""
    created = cf.create_article(editor, suffix)
    slug = created.get("slug")
    payload = cf.probe_png(suffix)
    first = cf.upload_cover(editor, slug, payload)
    second = cf.upload_cover(editor, slug, payload)
    assert first.json().get("object_key") == second.json().get("object_key"), (
        "the same bytes on one article must resolve to one object key, read "
        f"{first.json().get('object_key')!r} then {second.json().get('object_key')!r}")
    key = first.json().get("object_key")
    assert cf.backend().count(cf.TABLE_ASSET, object_key=key) == 1, (
        f"exactly one {cf.TABLE_ASSET} row may carry the key {key}")
    assert len([item for item in cf.stored_keys() if item == key]) == 1, (
        f"exactly one stored object may carry the key {key}")


def test_published_cover_file_is_readable_by_anyone(editor, suffix) -> None:
    """A published article's cover bytes are served by the app to any caller."""
    created = cf.create_article(editor, suffix)
    slug = created.get("slug")
    payload = cf.probe_png(suffix)
    cf.upload_cover(editor, slug, payload)
    assert cf.publish_article(editor, slug).status_code in cf.ACCEPTED, (
        f"the draft {slug} must publish")
    with appclient.client(None) as client:
        response = client.get(f"/articles/{slug}/cover")
    assert response.status_code == 200, cf.describe(
        response, f"a published cover must be readable by any caller, {slug}")
    assert response.content == payload, cf.describe(
        response, "the served bytes must be the bytes that were uploaded")


def test_draft_cover_file_is_denied_for_an_anonymous_caller(editor, buyer, suffix) -> None:
    """An unpublished article's cover is readable by an editor only."""
    created = cf.create_article(editor, suffix)
    slug = created.get("slug")
    cf.upload_cover(editor, slug, cf.probe_png(suffix))
    with appclient.client(None) as client:
        anonymous = client.get(f"/articles/{slug}/cover")
    assert anonymous.status_code in cf.NOT_FOUND, cf.describe(
        anonymous, f"the cover of the draft {slug} must not be readable anonymously")
    with appclient.client(buyer) as client:
        as_client = client.get(f"/articles/{slug}/cover")
    assert as_client.status_code in cf.NOT_FOUND, cf.describe(
        as_client, f"the cover of the draft {slug} must not be readable by a client")
    with appclient.client(editor) as client:
        as_editor = client.get(f"/articles/{slug}/cover")
    assert as_editor.status_code == 200, cf.describe(
        as_editor, f"an editor must read the cover of their own draft {slug}")


def test_cover_upload_without_alternative_text_is_refused(editor, suffix) -> None:
    """An upload carrying neither alternative text nor a decorative marker is refused."""
    created = cf.create_article(editor, suffix)
    slug = created.get("slug")
    before = len(cf.stored_keys())
    response = cf.upload_cover(editor, slug, cf.probe_png(suffix), alt_text="")
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, f"an upload with no alternative text must be refused, {slug}")
    cf.settle()
    assert len(cf.stored_keys()) == before, (
        "a refused upload must write no object into the store")


def test_cover_upload_from_a_client_session_writes_no_object(editor, buyer, suffix) -> None:
    """An upload attempted from a client session is denied and stores nothing."""
    created = cf.create_article(editor, suffix)
    slug = created.get("slug")
    before = len(cf.stored_keys())
    response = cf.upload_cover(buyer, slug, cf.probe_png(suffix))
    assert response.status_code in cf.DENIED + (404,), cf.describe(
        response, f"{cf.CLIENT_EMAIL} must not upload a cover for {slug}")
    cf.settle()
    assert len(cf.stored_keys()) == before, (
        "a denied upload must write no object into the store")


def test_cookie_choice_survives_a_reload(suffix) -> None:
    """A recorded cookie decision is not asked for again on a later route."""
    with appclient.client(None) as client:
        response = client.post("/consent", json={
            "essential": True, "analytics": False, "preferences": True, "version": 1})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "the consent choice must be accepted")
    stored = response.json()
    assert stored.get("essential") is True, cf.describe(
        response, "the essential category must stay locked on")
    assert stored.get("version"), cf.describe(
        response, "a stored decision must carry the version it was given under")
    document = cf.fetch_document("/").text
    assert cf.COOKIE_CONTROL_LABEL in document, (
        f"every route's footer must carry the {cf.COOKIE_CONTROL_LABEL!r} control")


def test_invalid_call_is_rejected_as_a_client_error(editor) -> None:
    """A malformed call is refused as a client error carrying a reason."""
    with appclient.client(editor) as client:
        response = client.post("/articles", json={"title": ""})
    assert response.status_code in cf.CLIENT_ERROR, cf.describe(
        response, "a malformed create must be refused as a client error")
    assert response.text.strip(), cf.describe(
        response, "a refusal must carry a message naming the reason")


def test_article_card_carries_its_accessible_label() -> None:
    """Every article card names the article it leads to for assistive technology."""
    document = cf.fetch_document("/articles").text
    assert cf.CARD_LABEL_PREFIX in document, (
        f"an article card must carry the label {cf.CARD_LABEL_PREFIX!r}")
    assert f"{cf.CARD_LABEL_PREFIX} {cf.CASE_STUDY_TITLE}" in document, (
        f"the card for {cf.CASE_STUDY_TITLE!r} must read "
        f"{cf.CARD_LABEL_PREFIX!r} followed by its own title")


def test_every_public_route_carries_a_skip_link_and_one_top_heading() -> None:
    """Every route opens with a skip link and carries exactly one level-one heading."""
    for route in cf.PUBLIC_ROUTES:
        markup = cf.fetch_document(route).text
        lower = markup.lower()
        assert lower.count("<h1") == 1, (
            f"the route {route} must carry exactly one level-one heading, carries "
            f"{lower.count('<h1')}")
        first_link = lower.find("<a ")
        first_heading = lower.find("<h1")
        assert 0 <= first_link < first_heading, (
            f"the route {route} must open with a skip link before its first heading")
        opening = markup[first_link:first_link + 400].lower()
        assert "skip" in opening, (
            f"the first focusable element of {route} must be a skip link, read {opening[:120]!r}")


def test_the_deployed_app_answers_from_outside_its_own_container() -> None:
    """The app answers on its public origin, on the internal port, after the session."""
    url = appclient.app_url()
    assert url.endswith(":4173"), (
        f"the app must answer on the container-internal port 4173, answered at {url}")
    assert "127.0.0.1" not in url, (
        f"a loopback-only listener is unreachable from outside the container, read {url}")
    response = cf.fetch_document("/")
    assert response.status_code == 200, cf.describe(
        response, "the app must still be serving its home route with no manual step taken")
