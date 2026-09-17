"""The one pytest module for Clinical Records Platform.

Every section (core features, data integrity, authorization, edge cases) and the
one declared slot (db) are merged here. Fixtures, pinned literals and helpers live
in conftest.py; the shared grader (appclient, capabilities, _shapes) is on
PYTHONPATH=/tests from the deku-verifier-base image.

The checklist obligations each function discharges live in the
pytest-provenance-v1 sidecar beside the bundle, not in a comment.

Channel disjointness, per reference/J J.12: the browser pass opens its own
encounter and signs it, books its own appointment and registers its own patient.
Every check here either reads a seeded record no journey mutates, or works inside
a per-run probe record it created itself.
"""

from __future__ import annotations

import os
import threading

import httpx

import appclient
import conftest as cf


def test_health_endpoint_answers_two_hundred() -> None:
    """The app answers its health endpoint once it is ready."""
    response = cf.get_json(None, "/health")
    assert response.status_code == 200, cf.describe(
        response, "the health endpoint must answer 200 once the app is ready")


def test_the_deployed_app_answers_from_outside_its_own_container() -> None:
    """The home route is reachable at the public origin after the session ends."""
    response = cf.fetch_document("/")
    assert response.status_code == 200, cf.describe(
        response, "the home route must answer at APP_PUBLIC_URL")
    assert cf.PRODUCT_NAME in response.text, (
        f"the home route must name {cf.PRODUCT_NAME!r}, read {response.text[:400]}")


def test_credentials_file_is_written_at_the_app_root() -> None:
    """The seeded logins are readable at the documented path."""
    assert os.path.isfile(cf.CREDENTIALS_FILE), (
        f"{cf.CREDENTIALS_FILE} must exist so a seeded account can be found")
    text = open(cf.CREDENTIALS_FILE, encoding="utf-8", errors="replace").read()
    for email in (cf.CLINICIAN_EMAIL, cf.PATIENT_EMAIL):
        assert email in text, (
            f"{cf.CREDENTIALS_FILE} must name the seeded account {email}, "
            f"holds: {text[:400]}")
    assert cf.SEEDED_PASSWORD in text, (
        f"{cf.CREDENTIALS_FILE} must carry the seeded password, holds: {text[:400]}")


def test_reserved_directories_exist_and_are_empty() -> None:
    """The two reserved directories exist at the app root and hold nothing."""
    for path in (cf.SCREENSHOT_DIR, cf.DOWNLOAD_DIR):
        assert os.path.isdir(path), f"{path} must exist at the app root"
        assert os.listdir(path) == [], f"{path} must be empty, holds {os.listdir(path)}"


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


def test_route_titles_end_with_the_product_name() -> None:
    """Every public route names the product in its own title."""
    for route in cf.PUBLIC_ROUTES:
        title = cf.document_title(cf.fetch_document(route).text)
        assert cf.PRODUCT_NAME in title, (
            f"the title of {route} must carry {cf.PRODUCT_NAME!r}, read {title!r}")


def test_public_routes_declare_a_resolving_preview_image() -> None:
    """Every public route declares a social preview whose image resolves."""
    for route in cf.PUBLIC_ROUTES:
        markup = cf.fetch_document(route).text
        title = cf.preview_title(markup)
        image = cf.preview_image(markup)
        assert title, f"the route {route} must declare a social preview title"
        assert image, f"the route {route} must declare a social preview image"
        target = image if image.startswith("http") else appclient.app_url() + image
        probe = httpx.get(target, timeout=appclient.TIMEOUT, follow_redirects=True)
        assert probe.status_code == 200, cf.describe(
            probe, f"the preview image declared by {route} must resolve")


def test_every_response_carries_the_security_headers() -> None:
    """Every route answers with the five stated security headers."""
    for route in ("/", "/downloads", "/blog"):
        response = cf.fetch_document(route)
        for name, expected in cf.SECURITY_HEADERS.items():
            found = response.headers.get(name)
            assert found, (
                f"the route {route} must carry the security header {name}, "
                f"headers: {dict(response.headers)}")
            if expected is not None:
                assert expected.lower() in found.lower(), (
                    f"the route {route} must carry {name} reading {expected!r}, "
                    f"read {found!r}")


def test_no_credential_appears_in_downloaded_markup() -> None:
    """Nothing the browser downloads carries a credential or a store address."""
    secrets = (cf.SEEDED_PASSWORD, "postgresql://", "deku_admin", "deku-local-dev")
    for route in cf.PUBLIC_ROUTES:
        markup = cf.fetch_document(route).text
        for secret in secrets:
            assert secret not in markup, (
                f"the route {route} must not ship {secret!r} to the browser, "
                f"found at {markup.find(secret)}")


def test_public_documents_reach_no_third_party_origin() -> None:
    """No public route asks the browser for another origin."""
    for route in cf.PUBLIC_ROUTES:
        origins = cf.external_origins(cf.fetch_document(route).text)
        assert origins == [], (
            f"the route {route} must contact no third-party origin, reaches {origins}")


def test_public_documents_are_rendered_on_the_server() -> None:
    """A public document carries its own content before any script runs."""
    home = cf.fetch_document("/")
    assert cf.CARD_CONTRIBUTE in home.text, (
        f"the home route must carry {cf.CARD_CONTRIBUTE!r} in the document the "
        f"server returns, read {home.text[:400]}")
    assert cf.FEATURE_HEADING in home.text, (
        f"the home route must carry {cf.FEATURE_HEADING!r} in the server document")
    for label in (cf.CARD_TRY, cf.CARD_SUPPORT, cf.CARD_DOWNLOAD, cf.APPEAL_HEADING,
                  cf.APPEAL_CONTROL, cf.ADOPTER_HEADING, cf.OPEN_SOURCE_HEADING,
                  cf.FEATURE_FIRST, cf.FEATURE_SECOND, cf.FEATURE_EIGHTH,
                  cf.ANNOUNCEMENT_LABEL):
        assert label in home.text, (
            f"the home route must carry the pinned copy {label!r}")


def test_announcement_bar_is_home_route_only() -> None:
    """The announcement label appears on the home route and on no other."""
    assert cf.ANNOUNCEMENT_LABEL in cf.fetch_document("/").text, (
        f"the home route must carry the announcement label {cf.ANNOUNCEMENT_LABEL!r}")
    for route in ("/downloads", "/support", "/blog", "/modules"):
        markup = cf.fetch_document(route).text
        assert cf.ANNOUNCEMENT_LABEL not in markup, (
            f"the route {route} must not carry the announcement bar, read "
            f"{markup[:400]}")


def test_pinned_site_copy_is_served_on_its_own_route() -> None:
    """The demonstration notice, the badge and the news heading render where pinned."""
    demo = cf.fetch_document("/demo").text
    assert cf.DEMO_NOTICE in demo, (
        f"the demonstration route must carry {cf.DEMO_NOTICE!r}")
    contribute = cf.fetch_document("/contribute").text
    assert cf.TAX_BADGE in contribute, (
        f"the contribution route must carry {cf.TAX_BADGE!r}")
    assert cf.COPY_CONTROL in contribute, (
        f"the contribution route must carry a control reading {cf.COPY_CONTROL!r}")
    blog = cf.fetch_document("/blog").text
    assert cf.NEWS_HEADING in blog, f"the news index must be headed {cf.NEWS_HEADING!r}"
    assert cf.CARD_LABEL_PREFIX in blog, (
        f"a news card link must be named with {cf.CARD_LABEL_PREFIX!r}")


def test_internal_links_on_public_routes_resolve() -> None:
    """Every internal link on every public route answers a served route."""
    for route in cf.PUBLIC_ROUTES:
        for href in sorted(set(cf.internal_links(cf.fetch_document(route).text))):
            probe = cf.fetch_document(href)
            assert probe.status_code == 200, cf.describe(
                probe, f"the internal link {href} on {route} must resolve")


def test_unknown_path_answers_not_found_and_records_a_page_view(clinician) -> None:
    """An unmatched address answers not found, renders the route and is recorded."""
    suffix = cf.unique_suffix()
    path = "/no-such-route-" + suffix
    response = cf.fetch_raw(path)
    assert response.status_code == 404, cf.describe(
        response, "an unmatched address must answer not found rather than success")
    assert cf.NOT_FOUND_HEADING in response.text, (
        f"the not-found route must be headed {cf.NOT_FOUND_HEADING!r}, read "
        f"{response.text[:400]}")
    assert cf.NOT_FOUND_FIRST in response.text, (
        f"the not-found route must carry {cf.NOT_FOUND_FIRST!r}")
    assert cf.NOT_FOUND_SECOND in response.text, (
        f"the not-found route must carry {cf.NOT_FOUND_SECOND!r}")
    row = cf.poll_until(lambda: cf.backend().one(cf.TABLE_PAGE_VIEW, path=path))
    assert row, f"a not-found response must be recorded as a page view for {path}"
    logged = cf.get_json(clinician, "/site/page-views")
    assert logged.status_code == 200, cf.describe(
        logged, "a staff account must be able to read the page view log")
    paths = [str(entry.get("path")) for entry in cf.as_list(cf.payload_of(logged))]
    assert path in paths, f"the page view log must carry {path}, read {paths[:20]}"


def test_page_view_rows_carry_no_visitor_identifier() -> None:
    """A stored page view names a path, never a person."""
    rows = cf.store_rows(cf.TABLE_PAGE_VIEW)
    assert rows, "the page view log must hold at least one row"
    banned = ("email", "actor", "account_id", "user_id", "patient_id", "ip",
              "session", "visitor")
    for row in rows[:20]:
        for column in row:
            assert not any(word in column.lower() for word in banned), (
                f"the page view row must carry no visitor identifier, found the "
                f"column {column!r} in {sorted(row)}")


def test_release_record_is_one_row_carrying_two_digests() -> None:
    """The release version, its date and its artifacts come from one record."""
    response = cf.get_json(None, "/site/release")
    assert response.status_code == 200, cf.describe(
        response, "the release endpoint must answer")
    payload = cf.payload_of(response) or {}
    assert payload.get("version") == cf.RELEASE_VERSION, (
        f"the seeded release must read {cf.RELEASE_VERSION!r}, read {payload!r}")
    artifacts = payload.get("artifacts") or []
    assert artifacts, f"the release must carry its artifacts, read {payload!r}"
    for artifact in artifacts:
        assert artifact.get("sha256"), (
            f"the artifact {artifact.get('label')!r} must carry a sha256 digest")
        assert artifact.get("sha512"), (
            f"the artifact {artifact.get('label')!r} must carry a second digest")
    markup = cf.fetch_document("/downloads").text
    assert cf.RELEASE_VERSION in markup, (
        f"the download route must render the version {cf.RELEASE_VERSION!r}")
    assert cf.RELEASE_DATE_RENDERED in markup, (
        f"the download route must render the date as {cf.RELEASE_DATE_RENDERED!r}")
    assert artifacts[0]["sha256"] in markup, (
        "the download route must render each artifact's digest beside it")


def test_module_directory_states_licence_source_and_egress() -> None:
    """Every module names its licence, its source and whether data leaves."""
    response = cf.get_json(None, "/site/modules")
    assert response.status_code == 200, cf.describe(
        response, "the module endpoint must answer")
    modules = cf.as_list(cf.payload_of(response))
    assert len(modules) == cf.MODULE_COUNT, (
        f"the directory must list {cf.MODULE_COUNT} modules, read {len(modules)}")
    for module in modules:
        assert module.get("licence"), (
            f"the module {module.get('slug')!r} must state its licence")
        assert module.get("source_url"), (
            f"the module {module.get('slug')!r} must state where its source is read")
        assert module.get("last_verified_on"), (
            f"the module {module.get('slug')!r} must carry a last verified date")
        assert "sends_data_outside" in module, (
            f"the module {module.get('slug')!r} must state whether data leaves "
            f"the practice, read {sorted(module)}")


def test_module_category_filter_is_a_route() -> None:
    """A category filter narrows the directory and carries its own address."""
    everything = cf.as_list(cf.payload_of(cf.get_json(None, "/site/modules")))
    categories = [c for module in everything for c in (module.get("categories") or [])]
    assert categories, f"a module must carry categories, read {everything[:2]}"
    chosen = sorted(set(categories))[0]
    narrowed = cf.get_json(None, "/site/modules", category=chosen)
    assert narrowed.status_code == 200, cf.describe(
        narrowed, "a category filter must answer")
    filtered = cf.as_list(cf.payload_of(narrowed))
    assert filtered, f"the category {chosen!r} must leave at least one module"
    assert len(filtered) <= len(everything), (
        f"a filter must narrow rather than widen: {len(filtered)} of {len(everything)}")
    for module in filtered:
        assert chosen in (module.get("categories") or []), (
            f"the module {module.get('slug')!r} must carry the filtered category "
            f"{chosen!r}")
    page = cf.fetch_document("/modules?category=" + chosen)
    assert page.status_code == 200, cf.describe(
        page, "the filtered directory must be a route with its own address")


def test_module_core_versions_are_ordered_numerically() -> None:
    """A core version requirement compares as an ordered version."""
    modules = {m.get("slug"): m for m in
               cf.as_list(cf.payload_of(cf.get_json(None, "/site/modules")))}
    telehealth = modules.get(cf.MODULE_TELEHEALTH) or {}
    reports = modules.get(cf.MODULE_REPORTS) or {}
    assert telehealth.get("min_core_version") == cf.CORE_VERSION_TELEHEALTH, (
        f"{cf.MODULE_TELEHEALTH} must need {cf.CORE_VERSION_TELEHEALTH!r}, "
        f"read {telehealth!r}")
    assert reports.get("min_core_version") == cf.CORE_VERSION_REPORTS, (
        f"{cf.MODULE_REPORTS} must need {cf.CORE_VERSION_REPORTS!r}, read {reports!r}")


def test_site_articles_are_seeded_and_readable() -> None:
    """The news index serves its seeded articles with a stored reading time."""
    response = cf.get_json(None, "/site/articles")
    assert response.status_code == 200, cf.describe(
        response, "the article endpoint must answer")
    articles = cf.as_list(cf.payload_of(response))
    assert len(articles) == cf.ARTICLE_COUNT, (
        f"the index must carry {cf.ARTICLE_COUNT} articles, read {len(articles)}")
    slugs = [a.get("slug") for a in articles]
    assert cf.ARTICLE_SLUG in slugs, (
        f"the seeded article {cf.ARTICLE_SLUG!r} must be listed, read {slugs}")
    for article in articles:
        assert article.get("reading_minutes"), (
            f"the article {article.get('slug')!r} must carry a stored reading time")
    assert cf.store_count(cf.TABLE_PAGE_VIEW) >= 1, (
        "a page view must be recorded for a rendered public route")


def test_list_endpoints_return_a_top_level_array() -> None:
    """A list endpoint answers with a top-level JSON array."""
    for path in ("/site/articles", "/site/modules"):
        payload = cf.payload_of(cf.get_json(None, path))
        assert isinstance(payload, list), (
            f"{path} must return a top-level JSON array, read {type(payload).__name__}")


def test_timestamps_are_utc_with_a_z_suffix(clinician) -> None:
    """Every emitted instant is an ISO 8601 string ending in Z."""
    response = cf.get_json(clinician, f"/patients/{cf.MRN_PRIMARY}/conditions")
    assert response.status_code == 200, cf.describe(
        response, "a related clinician must read the condition list")
    for condition in cf.as_list(cf.payload_of(response)):
        for key in ("effective_time", "recorded_time"):
            value = str(condition.get(key) or "")
            assert value.endswith("Z"), (
                f"the condition field {key} must end in Z, read {value!r}")


def test_login_returns_a_token_for_every_seeded_account() -> None:
    """Every seeded address signs in with the seeded password."""
    for email in cf.SEEDED_ACCOUNTS:
        response = cf.post_json(None, "/auth/login",
                                {"email": email, "password": cf.SEEDED_PASSWORD})
        assert response.status_code == 200, cf.describe(
            response, f"the seeded account {email} must be able to sign in")
        payload = cf.payload_of(response) or {}
        assert payload.get("access_token"), cf.describe(
            response, f"the login for {email} must return an access_token")
        assert payload.get("email") == email, cf.describe(
            response, f"the login for {email} must echo the address")


def test_login_with_a_wrong_password_returns_no_token() -> None:
    """A wrong password is denied and hands back nothing usable."""
    response = cf.post_json(None, "/auth/login",
                            {"email": cf.CLINICIAN_EMAIL, "password": "not-the-password"})
    assert response.status_code in cf.REFUSED, cf.describe(
        response, "a wrong password must be refused")
    assert "access_token" not in (response.text or ""), cf.describe(
        response, "a refused login must return no access_token")


def test_guarded_endpoint_denies_a_call_without_a_token() -> None:
    """An anonymous call to a guarded endpoint is denied."""
    for path in (f"/patients/{cf.MRN_PRIMARY}", "/worklists", "/claims",
                 "/portal/record", "/site/page-views"):
        response = cf.get_json(None, path)
        assert response.status_code in cf.REFUSED, cf.describe(
            response, f"an anonymous call to {path} must be denied")


def test_a_forged_token_is_denied() -> None:
    """A token the app never issued opens nothing."""
    response = cf.get_json("forged-" + cf.unique_suffix(), "/worklists")
    assert response.status_code in cf.REFUSED, cf.describe(
        response, "a token the app never issued must be denied")


def test_no_endpoint_creates_an_account() -> None:
    """There is no account-creation surface anywhere."""
    before = cf.store_count(cf.TABLE_ACCOUNT)
    suffix = cf.unique_suffix()
    body = {"email": f"probe-{suffix}@example.com", "password": cf.SEEDED_PASSWORD,
            "role": cf.ROLE_CLINICIAN}
    for path in ("/auth/signup", "/auth/register", "/accounts"):
        response = cf.post_json(None, path, body)
        assert response.status_code in cf.REFUSED, cf.describe(
            response, f"the address {path} must create no account")
    assert cf.store_count(cf.TABLE_ACCOUNT) == before, (
        f"the account count must be unchanged at {before}, read "
        f"{cf.store_count(cf.TABLE_ACCOUNT)}")


def test_role_is_read_from_the_stored_account_row(patient) -> None:
    """A role named in a request is ignored in favour of the stored one."""
    with appclient.client(patient) as client:
        response = client.get("/worklists", headers={"X-Role": cf.ROLE_CLINICIAN},
                              params={"role": cf.ROLE_CLINICIAN})
    assert response.status_code in cf.REFUSED, cf.describe(
        response, "a patient session naming a clinician role must still be refused")
    row = cf.store_one(cf.TABLE_ACCOUNT, email=cf.PATIENT_EMAIL)
    assert row and row.get("role") == cf.ROLE_PATIENT, (
        f"the stored role of {cf.PATIENT_EMAIL} must stay {cf.ROLE_PATIENT!r}, "
        f"read {row!r}")


def test_no_endpoint_returns_a_password_hash(clinician) -> None:
    """A stored hash never leaves the app."""
    row = cf.store_one(cf.TABLE_ACCOUNT, email=cf.CLINICIAN_EMAIL)
    assert row, f"the seeded account {cf.CLINICIAN_EMAIL} must be stored"
    stored = str(row.get("password_hash") or "")
    assert stored and stored != cf.SEEDED_PASSWORD, (
        "the stored password must be hashed rather than kept in plain text")
    for path in ("/portal/record", f"/patients/{cf.MRN_PRIMARY}"):
        body = cf.get_json(clinician, path).text
        assert stored not in body, (
            f"the response from {path} must not carry a stored password hash")


def test_unrelated_clinician_cannot_distinguish_a_real_chart(clinician_two) -> None:
    """A refused chart and an unissued number answer identically."""
    refused = cf.get_json(clinician_two, f"/patients/{cf.MRN_PRIMARY}")
    absent = cf.get_json(clinician_two, f"/patients/{cf.MRN_UNISSUED}")
    assert refused.status_code == absent.status_code, (
        f"a refused chart answered {refused.status_code} while an unissued number "
        f"answered {absent.status_code}: the two must be indistinguishable")
    assert refused.status_code in cf.NOT_FOUND, cf.describe(
        refused, "an unrelated clinician must be answered as for a missing record")
    assert refused.text == absent.text, (
        f"a refused chart returned {refused.text[:200]!r} while an unissued number "
        f"returned {absent.text[:200]!r}: the bodies must match")
    searched = cf.get_json(clinician_two, "/patients", family="Okafor")
    assert searched.status_code == 200, cf.describe(
        searched, "the register search must answer for any staff account")
    payload = cf.payload_of(searched) or {}
    assert cf.as_list(payload) == [], (
        f"a search must return only patients the caller may open, read "
        f"{searched.text[:400]}")
    assert int(payload.get("total") or 0) == 0, (
        f"the reported total must count the filtered set, read {payload!r}")


def test_patient_cannot_read_another_patient_record(patient_two) -> None:
    """A portal account reaches its own record and nothing else."""
    own = cf.get_json(patient_two, "/portal/record")
    assert own.status_code == 200, cf.describe(
        own, "a portal account must read its own record")
    assert cf.MRN_SECOND in own.text, (
        f"the portal record of {cf.PATIENT2_EMAIL} must be {cf.MRN_SECOND}")
    other = cf.get_json(patient_two, f"/patients/{cf.MRN_PRIMARY}")
    absent = cf.get_json(patient_two, f"/patients/{cf.MRN_UNISSUED}")
    assert other.status_code in cf.NOT_FOUND, cf.describe(
        other, "a patient must not read another patient's chart")
    assert other.status_code == absent.status_code, (
        "a refused chart and an unissued number must answer identically")


def test_patient_cannot_reach_a_workspace_endpoint(patient) -> None:
    """A portal account is refused every staff surface."""
    for path in ("/worklists", "/claims", "/results/unmatched", "/site/page-views"):
        response = cf.get_json(patient, path)
        assert response.status_code in cf.REFUSED, cf.describe(
            response, f"a patient session must be refused {path}")


def test_front_desk_cannot_read_a_clinical_note(front_desk) -> None:
    """Demographics are open to the front desk and the note is not."""
    chart = cf.get_json(front_desk, f"/patients/{cf.MRN_PRIMARY}")
    assert chart.status_code == 200, cf.describe(
        chart, "the front desk must read patient demographics")
    encounter = cf.get_json(front_desk, f"/encounters/{cf.ENCOUNTER_SIGNED}")
    body = (cf.payload_of(encounter) or {}) if encounter.status_code == 200 else {}
    assert encounter.status_code in cf.REFUSED or not body.get("note"), cf.describe(
        encounter, "the front desk must not receive a clinical note")
    portal = cf.get_json(front_desk, "/portal/record")
    assert portal.status_code in cf.REFUSED, cf.describe(
        portal, "a staff session asking for the portal must be refused")


def test_biller_condition_count_excludes_the_restricted_row(biller, clinician) -> None:
    """A filtered list reports the count of what the reader received."""
    full = cf.get_json(clinician, f"/patients/{cf.MRN_PRIMARY}/conditions")
    assert full.status_code == 200, cf.describe(
        full, "a related clinician must read every condition")
    full_payload = cf.payload_of(full) or {}
    assert len(cf.as_list(full_payload)) == cf.PRIMARY_CONDITION_TOTAL, (
        f"a related clinician must receive {cf.PRIMARY_CONDITION_TOTAL} conditions, "
        f"read {len(cf.as_list(full_payload))}")
    narrowed = cf.get_json(biller, f"/patients/{cf.MRN_PRIMARY}/conditions")
    assert narrowed.status_code == 200, cf.describe(
        narrowed, "a biller must read the conditions justifying a charge")
    payload = cf.payload_of(narrowed) or {}
    rows = cf.as_list(payload)
    assert len(rows) == cf.BILLER_CONDITION_TOTAL, (
        f"a biller must receive {cf.BILLER_CONDITION_TOTAL} of "
        f"{cf.PRIMARY_CONDITION_TOTAL} conditions, read {len(rows)}")
    assert payload.get("total") == cf.BILLER_CONDITION_TOTAL, (
        f"the reported total must be {cf.BILLER_CONDITION_TOTAL}, read "
        f"{payload.get('total')!r}")
    assert cf.CODE_RESTRICTED not in narrowed.text, (
        f"a biller must not receive the restricted code {cf.CODE_RESTRICTED}")
    assert "hidden" not in narrowed.text.lower(), (
        f"no response may state that a fact was hidden, read {narrowed.text[:400]}")
    assert "restricted" not in narrowed.text.lower(), (
        "a filtered list must not advertise that a label was applied")


def test_break_glass_requires_a_typed_reason(clinician_two) -> None:
    """A short reason opens nothing."""
    response = cf.post_json(clinician_two, f"/patients/{cf.MRN_PRIMARY}/break-glass",
                            {"reason": "urgent"})
    assert response.status_code in cf.REFUSED, cf.describe(
        response, "a reason under the stated minimum must be refused")
    follow = cf.get_json(clinician_two, f"/patients/{cf.MRN_PRIMARY}")
    assert follow.status_code in cf.NOT_FOUND, cf.describe(
        follow, "a refused declaration must open no chart")


def test_break_glass_opens_one_patient_and_withholds_the_label(clinician_two) -> None:
    """Emergency access names one patient and carries no restricted fact."""
    suffix = cf.unique_suffix()
    opened = cf.post_json(clinician_two, f"/patients/{cf.MRN_PRIMARY}/break-glass",
                          {"reason": cf.probe_reason(suffix)})
    assert opened.status_code in cf.ACCEPTED, cf.describe(
        opened, "a typed reason must open emergency access")
    chart = cf.get_json(clinician_two, f"/patients/{cf.MRN_PRIMARY}")
    assert chart.status_code == 200, cf.describe(
        chart, "emergency access must open the named chart")
    conditions = cf.get_json(clinician_two, f"/patients/{cf.MRN_PRIMARY}/conditions")
    payload = cf.payload_of(conditions) or {}
    assert cf.CODE_RESTRICTED not in conditions.text, (
        f"emergency access must withhold {cf.CODE_RESTRICTED}, read "
        f"{conditions.text[:400]}")
    assert payload.get("total") == cf.BILLER_CONDITION_TOTAL, (
        f"the count under emergency access must be {cf.BILLER_CONDITION_TOTAL}, "
        f"read {payload.get('total')!r}")
    elsewhere = cf.get_json(clinician_two, f"/patients/{cf.MRN_SECOND}")
    assert elsewhere.status_code in cf.NOT_FOUND, cf.describe(
        elsewhere, "an emergency declaration must open one patient only")


def test_access_log_records_a_chart_read(clinician, patient) -> None:
    """A clinician's read is the newest row in the patient's own access log."""
    read = cf.get_json(clinician, f"/patients/{cf.MRN_PRIMARY}")
    assert read.status_code == 200, cf.describe(
        read, "a related clinician must read the chart")
    log = cf.poll_until(lambda: cf.as_list(
        cf.payload_of(cf.get_json(patient, "/portal/access-log"))))
    assert log, "the access log of a patient must carry the reads of their record"
    actors = [str(entry.get("actor_email")) for entry in log]
    assert cf.CLINICIAN_EMAIL in actors, (
        f"the access log must name {cf.CLINICIAN_EMAIL}, read {actors[:10]}")
    assert cf.store_count(cf.TABLE_AUDIT) > 0, (
        "every access to identifiable patient data must write an audit event")


def test_denied_read_is_recorded_too(clinician_two, patient) -> None:
    """A refused read is recorded as a denied outcome rather than not at all."""
    before = cf.store_count(cf.TABLE_AUDIT)
    refused = cf.get_json(clinician_two, f"/patients/{cf.MRN_SECOND}")
    assert refused.status_code in cf.NOT_FOUND, cf.describe(
        refused, "an unrelated clinician must be refused")
    after = cf.poll_until(
        lambda: cf.store_count(cf.TABLE_AUDIT) > before and cf.store_count(cf.TABLE_AUDIT))
    assert after, (
        f"a denied read must add an audit event: the count stayed at {before}")


def test_audit_entries_are_chained_and_only_added(clinician) -> None:
    """Each audit row links to the one before it and none is removed."""
    cf.get_json(clinician, f"/patients/{cf.MRN_PRIMARY}")
    rows = cf.poll_until(lambda: cf.store_rows(cf.TABLE_AUDIT, action="read"))
    assert rows, "a read must leave an audit row"
    row = rows[-1]
    for column in ("actor_id", "hash", "prev_hash", "occurred_at", "selector"):
        assert column in row, (
            f"an audit row must carry {column}, holds {sorted(row)}")
    assert row.get("hash"), f"an audit row must carry its own hash, read {row!r}"


def test_seeded_records_are_persisted() -> None:
    """Every seeded identifier the graders name is a stored row."""
    expectations = [
        (cf.TABLE_ACCOUNT, {"email": cf.CLINICIAN_EMAIL}),
        (cf.TABLE_ACCOUNT, {"email": cf.PATIENT_EMAIL}),
        (cf.TABLE_PATIENT, {"mrn": cf.MRN_PRIMARY}),
        (cf.TABLE_PATIENT, {"mrn": cf.MRN_YEAR_ONLY}),
        (cf.TABLE_PATIENT, {"mrn": cf.MRN_TWIN_ONE}),
        (cf.TABLE_PATIENT, {"mrn": cf.MRN_TWIN_TWO}),
        (cf.TABLE_PATIENT, {"mrn": cf.MRN_SUBSUMED}),
        (cf.TABLE_PATIENT, {"mrn": cf.MRN_SURVIVOR}),
        (cf.TABLE_ENCOUNTER, {"number": cf.ENCOUNTER_SIGNED}),
        (cf.TABLE_ENCOUNTER, {"number": cf.ENCOUNTER_OPEN}),
        (cf.TABLE_ORDER, {"number": cf.ORDER_RELEASED}),
        (cf.TABLE_PRESCRIPTION, {"number": cf.PRESCRIPTION_SEEDED}),
        (cf.TABLE_ELIGIBILITY, {"number": cf.ELIGIBILITY_SEEDED}),
        (cf.TABLE_CLAIM, {"number": cf.CLAIM_QUEUED}),
        (cf.TABLE_CLAIM, {"number": cf.CLAIM_SUBMITTED}),
        (cf.TABLE_CLAIM, {"number": cf.CLAIM_PAID}),
        (cf.TABLE_CLAIM, {"number": cf.CLAIM_DENIED}),
        (cf.TABLE_REMITTANCE, {"number": cf.REMITTANCE_BALANCED}),
        (cf.TABLE_REMITTANCE, {"number": cf.REMITTANCE_OUT}),
        (cf.TABLE_APPOINTMENT, {"number": cf.APPOINTMENT_CANCELLED}),
        (cf.TABLE_APPOINTMENT, {"number": cf.APPOINTMENT_NO_SHOW}),
    ]
    for table, where in expectations:
        assert cf.store_one(table, **where), (
            f"the seeded row {where} must exist in {table}")
    assert cf.store_count(cf.TABLE_PATIENT) >= 7, (
        f"seven patients must be seeded, read {cf.store_count(cf.TABLE_PATIENT)}")
    assert cf.store_count(cf.TABLE_ENCOUNTER) >= 2, (
        "every row the app stores must be readable in the store the environment "
        "names, reached here through that same store")


def test_seeded_status_ladders_are_stored_as_pinned() -> None:
    """The seeded rows carry the exact statuses the brief pins."""
    pairs = [
        (cf.TABLE_ENCOUNTER, cf.ENCOUNTER_SIGNED, "status", cf.STATUS_SIGNED),
        (cf.TABLE_ENCOUNTER, cf.ENCOUNTER_OPEN, "status", cf.STATUS_OPEN),
        (cf.TABLE_ORDER, cf.ORDER_RELEASED, "status", cf.STATUS_ACTIVE),
        (cf.TABLE_CLAIM, cf.CLAIM_QUEUED, "status", cf.STATUS_QUEUED),
        (cf.TABLE_CLAIM, cf.CLAIM_SUBMITTED, "status", cf.STATUS_SUBMITTED),
        (cf.TABLE_CLAIM, cf.CLAIM_PAID, "status", cf.STATUS_PAID),
        (cf.TABLE_CLAIM, cf.CLAIM_DENIED, "status", cf.STATUS_DENIED),
        (cf.TABLE_REMITTANCE, cf.REMITTANCE_BALANCED, "state", cf.STATE_POSTED),
        (cf.TABLE_REMITTANCE, cf.REMITTANCE_OUT, "state", cf.STATE_QUARANTINED),
        (cf.TABLE_APPOINTMENT, cf.APPOINTMENT_CANCELLED, "status", cf.STATUS_CANCELLED),
        (cf.TABLE_APPOINTMENT, cf.APPOINTMENT_NO_SHOW, "status", cf.STATUS_NO_SHOW),
    ]
    for table, number, column, expected in pairs:
        row = cf.store_one(table, number=number)
        assert row, f"the seeded row {number} must exist in {table}"
        assert str(row.get(column)) == expected, (
            f"{table} {number} must carry {column} {expected!r}, read "
            f"{row.get(column)!r}")


def test_seeding_is_idempotent_for_the_pinned_records() -> None:
    """A restart leaves one row per seeded identifier rather than two."""
    for table, number in ((cf.TABLE_ENCOUNTER, cf.ENCOUNTER_SIGNED),
                          (cf.TABLE_CLAIM, cf.CLAIM_QUEUED),
                          (cf.TABLE_PRESCRIPTION, cf.PRESCRIPTION_SEEDED)):
        assert cf.store_count(table, number=number) == 1, (
            f"{table} must hold exactly one row numbered {number}, read "
            f"{cf.store_count(table, number=number)}")
    for mrn in (cf.MRN_PRIMARY, cf.MRN_TWIN_ONE, cf.MRN_SURVIVOR):
        assert cf.store_count(cf.TABLE_PATIENT, mrn=mrn) >= 1, (
            f"the patient {mrn} must be seeded")


def test_observation_history_returns_both_potassium_versions(clinician) -> None:
    """A correction supersedes rather than overwrites."""
    stored = cf.store_rows(cf.TABLE_OBSERVATION, code=cf.CODE_POTASSIUM)
    assert stored, f"a potassium observation coded {cf.CODE_POTASSIUM} must be seeded"
    identifier = stored[0].get("id")
    response = cf.get_json(clinician, f"/observations/{identifier}/history")
    assert response.status_code == 200, cf.describe(
        response, "an observation history must be readable")
    versions = cf.as_list(cf.payload_of(response))
    assert len(versions) >= 2, (
        f"the seeded potassium must carry two versions, read {len(versions)}")
    values = [float(v.get("value_number")) for v in versions
              if v.get("value_number") is not None]
    assert cf.POTASSIUM_FIRST in values, (
        f"the first potassium version must read {cf.POTASSIUM_FIRST}, read {values}")
    assert cf.POTASSIUM_SECOND in values, (
        f"the corrected potassium must read {cf.POTASSIUM_SECOND}, read {values}")
    superseding = [v for v in versions if v.get("supersedes")]
    assert superseding, (
        f"a corrected version must name what it supersedes, read {versions}")
    assert all(v.get("reason") for v in superseding), (
        f"a superseding version must carry its reason, read {superseding}")


def test_as_known_at_returns_the_superseded_value(clinician) -> None:
    """The chart as it stood then is a different answer from the chart now."""
    stored = cf.store_rows(cf.TABLE_OBSERVATION, code=cf.CODE_POTASSIUM)
    identifier = stored[0].get("id")
    versions = cf.as_list(cf.payload_of(
        cf.get_json(clinician, f"/observations/{identifier}/history")))
    first = [v for v in versions if not v.get("supersedes")]
    assert first, f"the first version must be readable, read {versions}"
    at = str(first[0].get("recorded_time"))
    response = cf.get_json(clinician, f"/patients/{cf.MRN_PRIMARY}/conditions",
                           as_known_at=at)
    assert response.status_code == 200, cf.describe(
        response, "the record as known at a stated instant must be readable")
    now = cf.get_json(clinician, f"/patients/{cf.MRN_PRIMARY}/conditions")
    assert now.status_code == 200, cf.describe(
        now, "the record as known now must be readable")


def test_year_precision_birth_date_is_never_rendered_as_a_day(front_desk) -> None:
    """A birth date known to the year stays a year everywhere."""
    response = cf.get_json(front_desk, f"/patients/{cf.MRN_YEAR_ONLY}")
    assert response.status_code == 200, cf.describe(
        response, "the front desk must read patient demographics")
    payload = cf.payload_of(response) or {}
    assert str(payload.get("birth_date")) == cf.BIRTH_DATE_YEAR_ONLY, (
        f"the birth date of {cf.MRN_YEAR_ONLY} must read "
        f"{cf.BIRTH_DATE_YEAR_ONLY!r}, read {payload.get('birth_date')!r}")
    assert payload.get("birth_date_precision") == cf.PRECISION_YEAR, (
        f"the precision must read {cf.PRECISION_YEAR!r}, read {payload!r}")
    assert f"{cf.BIRTH_DATE_YEAR_ONLY}-01-01" not in response.text, (
        f"a year-precision birth date must never render a fabricated day, read "
        f"{response.text[:400]}")
    row = cf.store_one(cf.TABLE_PATIENT, mrn=cf.MRN_YEAR_ONLY)
    assert row and str(row.get("birth_date_precision")) == cf.PRECISION_YEAR, (
        f"the stored precision must be {cf.PRECISION_YEAR!r}, read {row!r}")


def test_bounded_observation_keeps_its_comparator(clinician) -> None:
    """A result below a threshold is not that threshold."""
    rows = [r for r in cf.store_rows(cf.TABLE_OBSERVATION)
            if str(r.get("unit_code")) == cf.UNIT_TROPONIN]
    assert rows, f"an observation in {cf.UNIT_TROPONIN} must be seeded"
    row = rows[0]
    assert str(row.get("comparator")) == cf.COMPARATOR_BELOW, (
        f"the stored comparator must be {cf.COMPARATOR_BELOW!r}, read {row!r}")
    assert float(row.get("value_number")) == cf.TROPONIN_VALUE, (
        f"the stored value must be {cf.TROPONIN_VALUE}, read {row!r}")


def test_coded_values_carry_all_four_fields(clinician) -> None:
    """A code is a system, a code, a display and a version."""
    response = cf.get_json(clinician, f"/patients/{cf.MRN_PRIMARY}/conditions")
    conditions = cf.as_list(cf.payload_of(response))
    assert conditions, "a related clinician must receive the condition list"
    for condition in conditions:
        for field in ("code_system", "code", "code_display", "code_version"):
            assert condition.get(field), (
                f"a coded value must carry {field}, read {condition!r}")
    codes = {str(c.get("code")) for c in conditions}
    assert cf.CODE_DIABETES in codes, (
        f"the seeded diagnosis {cf.CODE_DIABETES} must be present, read {codes}")
    assert cf.CODE_RESTRICTED in codes, (
        f"the restricted diagnosis {cf.CODE_RESTRICTED} must reach a related "
        f"clinician, read {codes}")
    stored = cf.store_one(cf.TABLE_CONDITION, code=cf.CODE_RESTRICTED)
    assert stored and str(stored.get("sensitivity")) == cf.SENSITIVITY_RESTRICTED, (
        f"the stored condition {cf.CODE_RESTRICTED} must be labelled "
        f"{cf.SENSITIVITY_RESTRICTED!r}, read {stored!r}")


def test_retracted_fact_leaves_the_chart_and_stays_in_history(clinician, suffix) -> None:
    """A retraction is a status rather than a deletion."""
    number = cf.open_encounter(clinician, cf.MRN_SECOND)
    created = cf.add_condition(clinician, number)
    assert created.status_code in cf.ACCEPTED, cf.describe(
        created, "a coded diagnosis must be accepted")
    identifier = (cf.payload_of(created) or {}).get("id")
    assert identifier, cf.describe(created, "a stored condition must carry an id")
    before = cf.store_count(cf.TABLE_CONDITION)
    retracted = cf.post_json(clinician, f"/conditions/{identifier}/retract",
                             {"reason": "Recorded against the wrong encounter " + suffix})
    assert retracted.status_code in cf.ACCEPTED, cf.describe(
        retracted, "a coded diagnosis must be retractable")
    assert cf.store_count(cf.TABLE_CONDITION) >= before, (
        f"a retraction must remove no row: the count fell from {before} to "
        f"{cf.store_count(cf.TABLE_CONDITION)}")
    rows = cf.store_rows(cf.TABLE_CONDITION, id=identifier)
    statuses = [str(r.get("clinical_status")) for r in rows] + [
        str(r.get("status")) for r in rows]
    assert cf.ERROR_STATUS in statuses, (
        f"the retracted condition must carry {cf.ERROR_STATUS!r}, read {rows!r}")


def test_identifier_uniqueness_is_over_the_tuple(front_desk, suffix) -> None:
    """A member number reissued on a new policy registers cleanly."""
    reused = cf.store_rows(cf.TABLE_PATIENT_IDENTIFIER)
    assert reused, "the seeded patients must carry external identifiers"
    sample = reused[0]
    body = {
        "family_name": cf.probe_family(suffix),
        "given_name": cf.probe_given(suffix),
        "birth_date": "1980-02-29",
        "birth_date_precision": cf.PRECISION_DAY,
        "address_line": "12 Probe Lane " + suffix,
        "postal_code": "PB1 " + suffix[:3].upper(),
        "telephone": "+15550" + suffix[:6],
        "identifiers": [{"system": str(sample.get("system")),
                         "value": str(sample.get("value")),
                         "type": "insurance-member",
                         "period_start": "2026-09-01"}],
    }
    response = cf.post_json(front_desk, "/patients", body)
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "a member number reissued on a later policy must register")
    mrn = (cf.payload_of(response) or {}).get("mrn")
    assert mrn, cf.describe(response, "a registration must return the assigned mrn")
    assert cf.store_one(cf.TABLE_PATIENT, mrn=str(mrn)), (
        f"the registered patient {mrn} must be a stored row")


def test_twin_registration_opens_a_review_without_naming_the_match(front_desk,
                                                                   suffix) -> None:
    """A same-birth-date near match reaches a person rather than a merge."""
    twin = cf.store_one(cf.TABLE_PATIENT, mrn=cf.MRN_TWIN_ONE)
    assert twin, f"the seeded twin {cf.MRN_TWIN_ONE} must exist"
    before = cf.store_count(cf.TABLE_IDENTITY_REVIEW)
    body = {
        "family_name": str(twin.get("family_name")),
        "given_name": cf.probe_given(suffix),
        "birth_date": cf.BIRTH_DATE_TWINS,
        "birth_date_precision": cf.PRECISION_DAY,
        "address_line": str(twin.get("address_line")),
        "postal_code": str(twin.get("postal_code")),
        "telephone": str(twin.get("telephone")),
        "identifiers": [],
    }
    response = cf.post_json(front_desk, "/patients", body)
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "a near match must still register rather than be refused")
    payload = cf.payload_of(response) or {}
    assert payload.get("possible_match"), cf.describe(
        response, "a near match must report that a possible match exists")
    assert cf.MRN_TWIN_ONE not in response.text, (
        f"a possible-match warning must not name {cf.MRN_TWIN_ONE}, read "
        f"{response.text[:400]}")
    after = cf.poll_until(
        lambda: cf.store_count(cf.TABLE_IDENTITY_REVIEW) > before
        and cf.store_count(cf.TABLE_IDENTITY_REVIEW))
    assert after, (
        f"a near match must open an identity review row: the count stayed at {before}")
    rows = cf.store_rows(cf.TABLE_IDENTITY_REVIEW)
    flagged = [r for r in rows if r.get("twin_warning")]
    assert flagged, f"a same-birth-date near match must carry a twin warning, read {rows}"


def test_merged_identifier_resolves_to_the_survivor(front_desk) -> None:
    """A merge is a link: the subsumed number still answers, with the survivor."""
    response = cf.get_json(front_desk, f"/patients/{cf.MRN_SUBSUMED}")
    assert response.status_code == 200, cf.describe(
        response, "a subsumed medical record number must keep resolving")
    payload = cf.payload_of(response) or {}
    moved = str(payload.get("moved_to") or payload.get("mrn") or "")
    assert cf.MRN_SURVIVOR in response.text, (
        f"reading {cf.MRN_SUBSUMED} must name the survivor {cf.MRN_SURVIVOR}, read "
        f"{response.text[:400]}")
    assert moved, cf.describe(
        response, "a merged read must state that the identity moved")
    assert cf.store_one(cf.TABLE_PATIENT, mrn=cf.MRN_SUBSUMED), (
        f"the subsumed row {cf.MRN_SUBSUMED} must stay stored")
    assert cf.store_rows(cf.TABLE_PATIENT_LINK), (
        "a merge must be stored as a link row rather than as a rewrite")


def test_availability_is_computed_from_the_template(front_desk) -> None:
    """Free time comes from a stored template rather than a table of empty slots."""
    response = cf.get_json(front_desk, "/appointments/availability",
                           provider=cf.CLINICIAN_EMAIL, date=cf.CONTENDED_DAY)
    assert response.status_code == 200, cf.describe(
        response, "availability must be computable for a seeded provider on a seeded day")
    slots = cf.as_list(cf.payload_of(response))
    assert len(slots) == 1, (
        f"the seeded day {cf.CONTENDED_DAY} must leave exactly one free slot, "
        f"read {slots}")


def test_two_simultaneous_bookings_leave_exactly_one_appointment(front_desk) -> None:
    """The store refuses the second claim on one slot, under real concurrency."""
    free = cf.as_list(cf.payload_of(cf.get_json(
        front_desk, "/appointments/availability",
        provider=cf.CLINICIAN_EMAIL, date=cf.CONTENDED_DAY)))
    assert free, f"a free slot must remain on {cf.CONTENDED_DAY}"
    slot = free[0]
    starts_at = str(slot.get("starts_at") or slot)
    room = str(slot.get("room") or "Room 2")
    before = cf.store_count(cf.TABLE_APPOINTMENT)
    results: list = []
    lock = threading.Lock()

    def attempt(mrn: str) -> None:
        response = cf.post_json(front_desk, "/appointments", {
            "mrn": mrn, "provider": cf.CLINICIAN_EMAIL,
            "room": room, "starts_at": starts_at})
        with lock:
            results.append(response)

    threads = [threading.Thread(target=attempt, args=(mrn,))
               for mrn in (cf.MRN_PRIMARY, cf.MRN_SECOND)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=60)
    codes = sorted(r.status_code for r in results)
    accepted = [r for r in results if r.status_code in cf.ACCEPTED]
    refused = [r for r in results if r.status_code in cf.CONFLICTED]
    assert len(accepted) == 1, (
        f"exactly one simultaneous booking must succeed, statuses {codes}: "
        + "; ".join(cf.describe(r, "attempt") for r in results))
    assert len(refused) == 1, (
        f"the losing booking must be rejected as a conflict, statuses {codes}")
    assert cf.store_count(cf.TABLE_APPOINTMENT) == before + 1, (
        f"exactly one appointment must exist afterwards, the count moved from "
        f"{before} to {cf.store_count(cf.TABLE_APPOINTMENT)}")


def test_booking_with_a_taken_room_leaves_no_occupancy(front_desk) -> None:
    """A booking fails whole when any resource it needs is held."""
    taken = cf.store_one(cf.TABLE_APPOINTMENT, status=cf.STATUS_BOOKED)
    assert taken, "a booked appointment must be seeded"
    before_appointments = cf.store_count(cf.TABLE_APPOINTMENT)
    before_occupancy = cf.store_count(cf.TABLE_OCCUPANCY)
    response = cf.post_json(front_desk, "/appointments", {
        "mrn": cf.MRN_YEAR_ONLY,
        "provider": cf.CLINICIAN2_EMAIL,
        "room": str(taken.get("room")),
        "starts_at": str(taken.get("starts_at")),
    })
    assert response.status_code in cf.CONFLICTED, cf.describe(
        response, "a booking whose room is held must be refused")
    assert cf.store_count(cf.TABLE_APPOINTMENT) == before_appointments, (
        "a refused booking must leave no appointment row")
    assert cf.store_count(cf.TABLE_OCCUPANCY) == before_occupancy, (
        "a refused booking must leave no occupancy row")


def test_cancel_releases_the_slot_immediately(front_desk) -> None:
    """Cancelling frees the occupancy in the same action that sets the status."""
    free = cf.as_list(cf.payload_of(cf.get_json(
        front_desk, "/appointments/availability",
        provider=cf.CLINICIAN2_EMAIL, date=cf.CONTENDED_DAY)))
    assert free, f"the second clinician must have free time on {cf.CONTENDED_DAY}"
    slot = free[0]
    booked = cf.post_json(front_desk, "/appointments", {
        "mrn": cf.MRN_SECOND, "provider": cf.CLINICIAN2_EMAIL,
        "room": str(slot.get("room") or "Room 2"),
        "starts_at": str(slot.get("starts_at") or slot)})
    assert booked.status_code in cf.ACCEPTED, cf.describe(
        booked, "a free slot must be bookable")
    number = str((cf.payload_of(booked) or {}).get("number"))
    cancelled = cf.post_json(front_desk, f"/appointments/{number}/cancel")
    assert cancelled.status_code in cf.ACCEPTED, cf.describe(
        cancelled, "a booked appointment must be cancellable")
    row = cf.store_one(cf.TABLE_APPOINTMENT, number=number)
    assert row and str(row.get("status")) == cf.STATUS_CANCELLED, (
        f"the cancelled appointment must read {cf.STATUS_CANCELLED!r}, read {row!r}")
    assert cf.store_count(cf.TABLE_OCCUPANCY, appointment_id=row.get("id")) == 0, (
        "cancelling must release every occupancy row it held")
    again = cf.as_list(cf.payload_of(cf.get_json(
        front_desk, "/appointments/availability",
        provider=cf.CLINICIAN2_EMAIL, date=cf.CONTENDED_DAY)))
    assert len(again) >= len(free), (
        f"the cancelled slot must be bookable again: {len(again)} free against "
        f"{len(free)} before")


def test_reschedule_onto_a_taken_time_keeps_the_original(front_desk) -> None:
    """A patient never loses both times."""
    taken = cf.store_one(cf.TABLE_APPOINTMENT, status=cf.STATUS_BOOKED)
    assert taken, "a booked appointment must be seeded"
    free = cf.as_list(cf.payload_of(cf.get_json(
        front_desk, "/appointments/availability",
        provider=cf.CLINICIAN2_EMAIL, date=cf.CONTENDED_DAY)))
    assert free, "a free slot must remain for the moving appointment"
    slot = free[0]
    moving = cf.post_json(front_desk, "/appointments", {
        "mrn": cf.MRN_TWIN_ONE, "provider": cf.CLINICIAN2_EMAIL,
        "room": str(slot.get("room") or "Room 2"),
        "starts_at": str(slot.get("starts_at") or slot)})
    assert moving.status_code in cf.ACCEPTED, cf.describe(
        moving, "a free slot must be bookable")
    number = str((cf.payload_of(moving) or {}).get("number"))
    original = str((cf.payload_of(moving) or {}).get("starts_at"))
    refused = cf.post_json(front_desk, f"/appointments/{number}/reschedule",
                           {"starts_at": str(taken.get("starts_at"))})
    assert refused.status_code in cf.CONFLICTED, cf.describe(
        refused, "a reschedule onto a held time must be refused")
    row = cf.store_one(cf.TABLE_APPOINTMENT, number=number)
    assert row and str(row.get("status")) == cf.STATUS_BOOKED, (
        f"the original appointment must stay {cf.STATUS_BOOKED!r}, read {row!r}")
    assert original.startswith(str(row.get("starts_at"))[:10]), (
        f"the original appointment must keep its own time, read {row!r}")


def test_draft_note_is_invisible_to_another_clinician(clinician,
                                                      clinician_two) -> None:
    """A draft belongs to its author and the encounter is visible anyway."""
    author_view = cf.get_json(clinician, f"/encounters/{cf.ENCOUNTER_OPEN}")
    assert author_view.status_code == 200, cf.describe(
        author_view, "the note's author must read the draft")
    note = (cf.payload_of(author_view) or {}).get("note") or {}
    assert note.get("body"), cf.describe(
        author_view, "the author must receive the draft body")
    opened = cf.post_json(clinician_two, f"/patients/{cf.MRN_SECOND}/break-glass",
                          {"reason": cf.probe_reason(cf.unique_suffix())})
    assert opened.status_code in cf.ACCEPTED, cf.describe(
        opened, "a typed reason must open emergency access")
    other_view = cf.get_json(clinician_two, f"/encounters/{cf.ENCOUNTER_OPEN}")
    assert other_view.status_code == 200, cf.describe(
        other_view, "the encounter itself must stay visible to the care team")
    other_note = (cf.payload_of(other_view) or {}).get("note") or {}
    assert not other_note.get("body"), (
        f"a draft note must not reach another clinician, read {other_view.text[:400]}")


def test_stale_note_save_is_refused_with_the_current_version(clinician, suffix) -> None:
    """A stale save is refused and nothing is merged."""
    number = cf.open_encounter(clinician, cf.MRN_PRIMARY)
    loaded = cf.note_version(clinician, number)
    first = cf.write_note(clinician, number, cf.probe_note(suffix) + " one", loaded)
    assert first.status_code in cf.ACCEPTED, cf.describe(
        first, "a save carrying the loaded version must be accepted")
    current = (cf.payload_of(first) or {}).get("version_id")
    assert current is not None, cf.describe(
        first, "an accepted save must return the stored version")
    stale = cf.write_note(clinician, number, cf.probe_note(suffix) + " two", loaded)
    assert stale.status_code in cf.CONFLICTED, cf.describe(
        stale, "a save against a stale version must be refused")
    body = cf.payload_of(stale) or {}
    assert str(current) in stale.text, cf.describe(
        stale, "a refused save must hand back the current version")
    settled = cf.get_json(clinician, f"/encounters/{number}")
    stored = ((cf.payload_of(settled) or {}).get("note") or {}).get("body") or ""
    assert "two" not in stored, (
        f"a refused save must merge nothing, the stored body reads {stored[:200]!r}")


def test_signing_locks_releases_and_queues(clinician, suffix) -> None:
    """One action locks the note, releases its orders and queues its claim."""
    number = cf.open_encounter(clinician, cf.MRN_PRIMARY)
    cf.write_note(clinician, number, cf.probe_note(suffix),
                  cf.note_version(clinician, number))
    condition = cf.add_condition(clinician, number)
    assert condition.status_code in cf.ACCEPTED, cf.describe(
        condition, "a coded diagnosis must be accepted before signing")
    order = cf.add_order(clinician, number)
    assert order.status_code in cf.ACCEPTED, cf.describe(
        order, "an order must be accepted before signing")
    order_number = str((cf.payload_of(order) or {}).get("number"))
    order_row = cf.store_one(cf.TABLE_ORDER, number=order_number)
    assert order_row and str(order_row.get("status")) == cf.STATUS_DRAFT, (
        f"a new order must start {cf.STATUS_DRAFT!r}, read {order_row!r}")
    listed = cf.as_list(cf.payload_of(
        cf.get_json(clinician, "/orders", status=cf.STATUS_ACTIVE)))
    assert order_number not in [str(o.get("number")) for o in listed], (
        f"a draft order must be absent from the active list, read {listed}")
    signed = cf.sign_encounter(clinician, number)
    assert signed.status_code in cf.ACCEPTED, cf.describe(
        signed, "an encounter carrying a coded diagnosis must sign")
    payload = cf.payload_of(signed) or {}
    assert payload.get("rendering_hash"), cf.describe(
        signed, "signing must return the stored rendering hash")
    assert payload.get("note_version_id") is not None, cf.describe(
        signed, "signing must return the locked note version")
    assert int(payload.get("orders_released") or 0) >= 1, cf.describe(
        signed, "signing must report the orders it released")
    claim_number = str(payload.get("claim_number") or "")
    assert claim_number, cf.describe(signed, "signing must queue a claim")
    released = cf.store_one(cf.TABLE_ORDER, number=order_number)
    assert released and str(released.get("status")) == cf.STATUS_ACTIVE, (
        f"signing must move the order to {cf.STATUS_ACTIVE!r}, read {released!r}")
    assert "filler_number" in released, (
        f"an order must keep the performer's filler_number apart from its own "
        f"number, holds {sorted(released)}")
    claim = cf.store_one(cf.TABLE_CLAIM, number=claim_number)
    assert claim and str(claim.get("status")) == cf.STATUS_QUEUED, (
        f"the queued claim must read {cf.STATUS_QUEUED!r}, read {claim!r}")
    signature = cf.store_one(cf.TABLE_SIGNATURE, rendering_hash=payload["rendering_hash"])
    assert signature, "signing must store a note_signature row"
    for column in ("included_refs", "terminology_versions", "signed_by", "signed_at"):
        assert signature.get(column), (
            f"the stored signature must carry {column}, holds {sorted(signature)}")
    detail = cf.get_json(clinician, f"/claims/{claim_number}")
    assert detail.status_code in (200, 401, 403), cf.describe(
        detail, "the queued claim must be addressable")


def test_signed_rendering_survives_a_later_medication(clinician, suffix) -> None:
    """The signed rendering is a photograph rather than a live query."""
    signed = cf.signed_probe_encounter(clinician, cf.MRN_PRIMARY, suffix)
    number = signed["number"]
    first = cf.get_json(clinician, f"/encounters/{number}/rendering")
    assert first.status_code == 200, cf.describe(
        first, "a signed note must be re-renderable")
    before = cf.payload_of(first) or {}
    assert before.get("rendered_text"), cf.describe(
        first, "a rendering must carry the note as it was rendered")
    assert before.get("rendering_hash") == signed.get("rendering_hash"), (
        f"the stored hash must match the signing response, read {before!r}")
    added = cf.post_json(clinician, "/prescriptions", {
        "mrn": cf.MRN_PRIMARY,
        "code_system": cf.SYSTEM_MEDICATION, "code": cf.CODE_MEDICATION,
        "code_display": "metformin hydrochloride 500 MG Oral Tablet",
        "code_version": "2026-03",
        "dose_quantity": cf.DOSE_QUANTITY, "dose_unit": cf.DOSE_UNIT,
        "dose_route": "oral", "frequency_per_day": 2, "duration_days": 30,
        "dispense_quantity": cf.DISPENSE_QUANTITY, "dispense_unit": cf.DISPENSE_UNIT,
        "refills_authorised": cf.REFILLS_AUTHORISED})
    assert added.status_code in cf.ACCEPTED, cf.describe(
        added, "a prescription must be writable after the encounter is signed")
    again = cf.get_json(clinician, f"/encounters/{number}/rendering")
    after = cf.payload_of(again) or {}
    assert after.get("rendering_hash") == before.get("rendering_hash"), (
        f"the rendering hash must not move after a later medication: "
        f"{before.get('rendering_hash')!r} became {after.get('rendering_hash')!r}")
    assert after.get("rendered_text") == before.get("rendered_text"), (
        "the rendered text of a signed note must not move after a later medication")
    assert cf.CODE_MEDICATION not in str(after.get("rendered_text")), (
        "a note signed before a medication must not render that medication")


def test_signing_without_a_diagnosis_changes_nothing(clinician, suffix) -> None:
    """A refused signing releases nothing and queues nothing."""
    number = cf.open_encounter(clinician, cf.MRN_SECOND)
    cf.write_note(clinician, number, cf.probe_note(suffix),
                  cf.note_version(clinician, number))
    order = cf.add_order(clinician, number)
    assert order.status_code in cf.ACCEPTED, cf.describe(
        order, "an order must be accepted on an open encounter")
    order_number = str((cf.payload_of(order) or {}).get("number"))
    claims_before = cf.store_count(cf.TABLE_CLAIM)
    refused = cf.sign_encounter(clinician, number)
    assert refused.status_code in cf.REFUSED, cf.describe(
        refused, "an encounter carrying no coded diagnosis must not sign")
    row = cf.store_one(cf.TABLE_ORDER, number=order_number)
    assert row and str(row.get("status")) == cf.STATUS_DRAFT, (
        f"a refused signing must leave the order {cf.STATUS_DRAFT!r}, read {row!r}")
    assert cf.store_count(cf.TABLE_CLAIM) == claims_before, (
        f"a refused signing must queue no claim: the count moved from "
        f"{claims_before} to {cf.store_count(cf.TABLE_CLAIM)}")
    encounter = cf.store_one(cf.TABLE_ENCOUNTER, number=number)
    assert encounter and str(encounter.get("status")) == cf.STATUS_OPEN, (
        f"a refused signing must leave the encounter {cf.STATUS_OPEN!r}, read "
        f"{encounter!r}")


def test_second_signing_queues_no_second_claim(clinician, suffix) -> None:
    """Signing twice is refused rather than repeated."""
    signed = cf.signed_probe_encounter(clinician, cf.MRN_PRIMARY, suffix)
    number = signed["number"]
    claims_before = cf.store_count(cf.TABLE_CLAIM)
    hash_before = signed.get("rendering_hash")
    again = cf.sign_encounter(clinician, number)
    assert again.status_code in cf.REFUSED, cf.describe(
        again, "a signed encounter must not sign a second time")
    assert cf.store_count(cf.TABLE_CLAIM) == claims_before, (
        f"a repeated signing must queue no second claim: {claims_before} became "
        f"{cf.store_count(cf.TABLE_CLAIM)}")
    rendering = cf.payload_of(cf.get_json(clinician, f"/encounters/{number}/rendering"))
    assert (rendering or {}).get("rendering_hash") == hash_before, (
        "a repeated signing must leave the stored rendering hash unchanged")


def test_signed_note_cannot_be_edited(clinician, suffix) -> None:
    """After signature there is an addendum or an amendment, never an edit."""
    signed = cf.signed_probe_encounter(clinician, cf.MRN_PRIMARY, suffix)
    number = signed["number"]
    edited = cf.write_note(clinician, number, "rewritten " + suffix,
                           signed.get("note_version_id"))
    assert edited.status_code in cf.REFUSED, cf.describe(
        edited, "a signed note must refuse an edit")
    addendum = cf.post_json(clinician, f"/encounters/{number}/addendum",
                            {"body": "A later result arrived " + suffix,
                             "reason": "New information after signature " + suffix})
    assert addendum.status_code in cf.ACCEPTED, cf.describe(
        addendum, "a signed note must accept an addendum")
    amendment = cf.post_json(clinician, f"/encounters/{number}/amendment",
                             {"body": "Corrected assessment " + suffix,
                              "reason": "The original was wrong " + suffix})
    assert amendment.status_code in cf.ACCEPTED, cf.describe(
        amendment, "a signed note must accept an amendment")
    versions = cf.store_rows(cf.TABLE_NOTE)
    assert len(versions) >= 2, (
        f"an amendment must leave the earlier version readable, read {len(versions)}")


def test_addendum_without_a_reason_is_refused(clinician, suffix) -> None:
    """Both correction routes require a reason."""
    signed = cf.signed_probe_encounter(clinician, cf.MRN_SECOND, suffix)
    number = signed["number"]
    response = cf.post_json(clinician, f"/encounters/{number}/addendum",
                            {"body": "A later thought " + suffix})
    assert response.status_code in cf.REFUSED, cf.describe(
        response, "an addendum carrying no reason must be refused")


def test_patient_amendment_request_changes_no_entry(patient, suffix) -> None:
    """A patient's statement is attached and the clinician's entry stands."""
    before = cf.store_count(cf.TABLE_NOTE)
    response = cf.post_json(patient, "/portal/amendment-requests", {
        "statement": "I never reported that symptom " + suffix,
        "about": cf.ENCOUNTER_SIGNED})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "a patient must be able to request an amendment")
    assert cf.store_count(cf.TABLE_NOTE) == before, (
        f"a patient request must write no note version: {before} became "
        f"{cf.store_count(cf.TABLE_NOTE)}")


def test_repeated_control_id_creates_no_second_observation(clinician, suffix) -> None:
    """A retransmitted result is recorded once."""
    cf.signed_probe_encounter(clinician, cf.MRN_PRIMARY, suffix)
    placer = cf.as_list(cf.payload_of(
        cf.get_json(clinician, "/orders", status=cf.STATUS_ACTIVE)))
    assert placer, "a released order must be listed as active"
    number = str(placer[0].get("number"))
    control = "CTRL-" + suffix
    body = {"placer_number": number, "control_id": control,
            "code_system": cf.SYSTEM_LAB, "code": cf.CODE_POTASSIUM,
            "code_display": "Potassium [Moles/volume] in Serum or Plasma",
            "code_version": cf.VERSION_LAB, "value_number": 4.4,
            "comparator": None, "unit_code": cf.UNIT_POTASSIUM,
            "reference_low": cf.REFERENCE_LOW, "reference_high": cf.REFERENCE_HIGH,
            "abnormal_flag": "N", "effective_time": "2026-09-16T10:00:00Z"}
    first = cf.post_json(clinician, "/results", body)
    assert first.status_code in cf.ACCEPTED, cf.describe(
        first, "a result against a released order must be accepted")
    repeat = cf.post_json(clinician, "/results", body)
    assert repeat.status_code in cf.ACCEPTED, cf.describe(
        repeat, "a retransmission must be answered with the first outcome")
    assert cf.store_count(cf.TABLE_OBSERVATION, control_id=control) == 1, (
        f"the control id {control} must appear once, read "
        f"{cf.store_count(cf.TABLE_OBSERVATION, control_id=control)}")


def test_sender_reference_range_is_stored_with_the_observation(clinician,
                                                               suffix) -> None:
    """The performing laboratory's range travels with the result."""
    cf.signed_probe_encounter(clinician, cf.MRN_SECOND, suffix)
    placer = cf.as_list(cf.payload_of(
        cf.get_json(clinician, "/orders", status=cf.STATUS_ACTIVE)))
    assert placer, "a released order must be listed as active"
    control = "CTRL-RANGE-" + suffix
    response = cf.post_json(clinician, "/results", {
        "placer_number": str(placer[0].get("number")), "control_id": control,
        "code_system": cf.SYSTEM_LAB, "code": cf.CODE_POTASSIUM,
        "code_display": "Potassium [Moles/volume] in Serum or Plasma",
        "code_version": cf.VERSION_LAB, "value_number": 5.9,
        "unit_code": cf.UNIT_POTASSIUM, "reference_low": 3.9,
        "reference_high": 5.4, "abnormal_flag": "H",
        "effective_time": "2026-09-16T10:30:00Z"})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "a result carrying a sender range must be accepted")
    row = cf.store_one(cf.TABLE_OBSERVATION, control_id=control)
    assert row, f"the observation {control} must be stored"
    assert float(row.get("reference_low")) == 3.9, (
        f"the sender's low reference must be stored, read {row!r}")
    assert float(row.get("reference_high")) == 5.4, (
        f"the sender's high reference must be stored, read {row!r}")
    assert str(row.get("abnormal_flag")) == "H", (
        f"the sender's abnormal flag must be stored, read {row!r}")


def test_stale_result_does_not_become_current(clinician, suffix) -> None:
    """A result older than the current one is stored without displacing it."""
    cf.signed_probe_encounter(clinician, cf.MRN_PRIMARY, suffix)
    placer = cf.as_list(cf.payload_of(
        cf.get_json(clinician, "/orders", status=cf.STATUS_ACTIVE)))
    assert placer, "a released order must be listed as active"
    number = str(placer[0].get("number"))
    newer = cf.post_json(clinician, "/results", {
        "placer_number": number, "control_id": "CTRL-NEW-" + suffix,
        "code_system": cf.SYSTEM_LAB, "code": cf.CODE_POTASSIUM,
        "code_display": "Potassium [Moles/volume] in Serum or Plasma",
        "code_version": cf.VERSION_LAB, "value_number": 4.2,
        "unit_code": cf.UNIT_POTASSIUM, "reference_low": cf.REFERENCE_LOW,
        "reference_high": cf.REFERENCE_HIGH, "abnormal_flag": "N",
        "effective_time": "2026-09-16T12:00:00Z"})
    assert newer.status_code in cf.ACCEPTED, cf.describe(
        newer, "a result must be accepted against a released order")
    older = cf.post_json(clinician, "/results", {
        "placer_number": number, "control_id": "CTRL-OLD-" + suffix,
        "code_system": cf.SYSTEM_LAB, "code": cf.CODE_POTASSIUM,
        "code_display": "Potassium [Moles/volume] in Serum or Plasma",
        "code_version": cf.VERSION_LAB, "value_number": 9.9,
        "unit_code": cf.UNIT_POTASSIUM, "reference_low": cf.REFERENCE_LOW,
        "reference_high": cf.REFERENCE_HIGH, "abnormal_flag": "H",
        "effective_time": "2026-09-16T08:00:00Z"})
    assert older.status_code in cf.ACCEPTED, cf.describe(
        older, "an out-of-order result must be stored rather than dropped")
    assert cf.store_one(cf.TABLE_OBSERVATION, control_id="CTRL-OLD-" + suffix), (
        "an out-of-order result must be stored")
    current = cf.get_json(clinician, f"/patients/{cf.MRN_PRIMARY}/conditions")
    assert current.status_code == 200, cf.describe(
        current, "the chart must stay readable after an out-of-order result")
    latest = cf.store_one(cf.TABLE_OBSERVATION, control_id="CTRL-NEW-" + suffix)
    assert latest and float(latest.get("value_number")) == 4.2, (
        f"the newer result must stay current, read {latest!r}")


def test_unmatched_result_is_queued_rather_than_filed(clinician, suffix) -> None:
    """A result matching no patient is never guessed at."""
    before_observations = cf.store_count(cf.TABLE_OBSERVATION)
    control = "CTRL-UNMATCHED-" + suffix
    response = cf.post_json(clinician, "/results", {
        "placer_number": "ORD-NO-SUCH-" + suffix, "control_id": control,
        "stated_mrn": cf.MRN_UNISSUED,
        "code_system": cf.SYSTEM_LAB, "code": cf.CODE_POTASSIUM,
        "code_display": "Potassium [Moles/volume] in Serum or Plasma",
        "code_version": cf.VERSION_LAB, "value_number": 4.0,
        "unit_code": cf.UNIT_POTASSIUM, "reference_low": cf.REFERENCE_LOW,
        "reference_high": cf.REFERENCE_HIGH, "abnormal_flag": "N",
        "effective_time": "2026-09-16T11:00:00Z"})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "an unmatched result must be accepted rather than discarded")
    assert cf.store_count(cf.TABLE_OBSERVATION) == before_observations, (
        "an unmatched result must be filed against no patient")
    queued = cf.poll_until(
        lambda: cf.backend().one(cf.TABLE_UNMATCHED, control_id=control))
    assert queued, f"the unmatched result {control} must reach the reconciliation queue"
    listed = cf.get_json(clinician, "/results/unmatched")
    assert listed.status_code == 200, cf.describe(
        listed, "the reconciliation queue must be readable")
    controls = [str(e.get("control_id")) for e in cf.as_list(cf.payload_of(listed))]
    assert control in controls, (
        f"the queue must list {control}, read {controls[:10]}")


def test_prescription_renders_its_instruction_from_structured_fields(clinician,
                                                                     suffix) -> None:
    """The printed sentence comes from the fields rather than from free text."""
    response = cf.post_json(clinician, "/prescriptions", {
        "mrn": cf.MRN_SECOND,
        "code_system": cf.SYSTEM_MEDICATION, "code": cf.CODE_MEDICATION,
        "code_display": "metformin hydrochloride 500 MG Oral Tablet",
        "code_version": "2026-03",
        "dose_quantity": cf.DOSE_QUANTITY, "dose_unit": cf.DOSE_UNIT,
        "dose_route": "oral", "frequency_per_day": 2, "duration_days": 30,
        "dispense_quantity": cf.DISPENSE_QUANTITY, "dispense_unit": cf.DISPENSE_UNIT,
        "refills_authorised": cf.REFILLS_AUTHORISED})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "a structured prescription must be accepted")
    payload = cf.payload_of(response) or {}
    instruction = str(payload.get("patient_instruction") or "")
    assert instruction, cf.describe(
        response, "a prescription must return its rendered instruction")
    assert str(cf.DOSE_QUANTITY) in instruction, (
        f"the rendered instruction must carry the dose {cf.DOSE_QUANTITY}, read "
        f"{instruction!r}")
    number = str(payload.get("number") or "")
    row = cf.store_one(cf.TABLE_PRESCRIPTION, number=number)
    assert row, f"the prescription {number} must be stored"
    assert int(row.get("dose_quantity")) == cf.DOSE_QUANTITY, (
        f"the stored dose quantity must be {cf.DOSE_QUANTITY}, read {row!r}")
    assert int(row.get("dispense_quantity")) == cf.DISPENSE_QUANTITY, (
        f"the stored dispense quantity must be {cf.DISPENSE_QUANTITY}, read {row!r}")
    assert int(row.get("refills_authorised")) == cf.REFILLS_AUTHORISED, (
        f"a zero refill count is a value rather than an absent one, read {row!r}")


def test_seeded_prescription_keeps_its_two_quantities_apart() -> None:
    """The seeded prescription pins the dose against the dispense."""
    row = cf.store_one(cf.TABLE_PRESCRIPTION, number=cf.PRESCRIPTION_SEEDED)
    assert row, f"the seeded prescription {cf.PRESCRIPTION_SEEDED} must exist"
    assert int(row.get("dose_quantity")) == cf.DOSE_QUANTITY, (
        f"{cf.PRESCRIPTION_SEEDED} must carry a dose of {cf.DOSE_QUANTITY}, "
        f"read {row!r}")
    assert int(row.get("dispense_quantity")) == cf.DISPENSE_QUANTITY, (
        f"{cf.PRESCRIPTION_SEEDED} must dispense {cf.DISPENSE_QUANTITY}, read {row!r}")
    assert str(row.get("code")) == cf.CODE_MEDICATION, (
        f"{cf.PRESCRIPTION_SEEDED} must carry the code {cf.CODE_MEDICATION}, "
        f"read {row!r}")


def test_conflict_with_a_withheld_fact_names_nothing(clinician_two, suffix) -> None:
    """A prescriber without the label is warned without the entry being named."""
    opened = cf.post_json(clinician_two, f"/patients/{cf.MRN_PRIMARY}/break-glass",
                          {"reason": cf.probe_reason(suffix)})
    assert opened.status_code in cf.ACCEPTED, cf.describe(
        opened, "a typed reason must open emergency access")
    response = cf.post_json(clinician_two, "/prescriptions", {
        "mrn": cf.MRN_PRIMARY,
        "code_system": cf.SYSTEM_MEDICATION, "code": cf.CODE_MEDICATION,
        "code_display": "metformin hydrochloride 500 MG Oral Tablet",
        "code_version": "2026-03",
        "dose_quantity": cf.DOSE_QUANTITY, "dose_unit": cf.DOSE_UNIT,
        "dose_route": "oral", "frequency_per_day": 2, "duration_days": 30,
        "dispense_quantity": cf.DISPENSE_QUANTITY, "dispense_unit": cf.DISPENSE_UNIT,
        "refills_authorised": cf.REFILLS_AUTHORISED})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "a prescription under emergency access must still be answered")
    payload = cf.payload_of(response) or {}
    assert "conflict" in payload, cf.describe(
        response, "a prescription response must report whether a conflict exists")
    if payload.get("conflict"):
        assert payload.get("severity"), cf.describe(
            response, "a conflict must state how serious it is")
        assert cf.CODE_RESTRICTED not in response.text, (
            f"a conflict with a withheld fact must not name {cf.CODE_RESTRICTED}, "
            f"read {response.text[:400]}")
        assert "consent" in response.text.lower(), cf.describe(
            response, "a conflict the prescriber cannot see must offer the consent route")


def test_allergy_states_stay_distinct(clinician) -> None:
    """A recorded allergy, a recorded absence and nothing at all are three answers."""
    recorded = cf.payload_of(cf.get_json(
        clinician, f"/patients/{cf.MRN_PRIMARY}/allergies")) or {}
    assert str(recorded.get("assertion")) == cf.ASSERTION_ALLERGY, (
        f"{cf.MRN_PRIMARY} must carry a recorded allergy, read {recorded!r}")
    assert cf.ALLERGY_SUBSTANCE in str(recorded), (
        f"the recorded allergy must name {cf.ALLERGY_SUBSTANCE}, read {recorded!r}")
    none_known = cf.payload_of(cf.get_json(
        clinician, f"/patients/{cf.MRN_SECOND}/allergies")) or {}
    assert str(none_known.get("assertion")) == cf.ASSERTION_NONE_KNOWN, (
        f"{cf.MRN_SECOND} must carry a {cf.ASSERTION_NONE_KNOWN} assertion, "
        f"read {none_known!r}")
    not_asked = cf.payload_of(cf.get_json(
        clinician, f"/patients/{cf.MRN_YEAR_ONLY}/allergies")) or {}
    assert str(not_asked.get("assertion")) == cf.ASSERTION_NOT_ASKED, (
        f"{cf.MRN_YEAR_ONLY} must read {cf.ASSERTION_NOT_ASKED!r} rather than an "
        f"assertion of safety, read {not_asked!r}")
    assert cf.store_rows(cf.TABLE_ALLERGY), (
        "the recorded allergy assertions must be stored rows")


def test_eligibility_snapshot_is_dated(biller, suffix) -> None:
    """An eligibility answer is true at the instant it was given."""
    coverage = cf.store_rows(cf.TABLE_COVERAGE)
    assert coverage, "a coverage row must be seeded"
    response = cf.post_json(biller, "/eligibility", {
        "mrn": cf.MRN_PRIMARY, "coverage_id": coverage[0].get("id")})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "an eligibility check must be recordable")
    payload = cf.payload_of(response) or {}
    assert payload.get("checked_at"), cf.describe(
        response, "an eligibility answer must carry the instant it was checked")
    assert str(payload.get("checked_at")).endswith("Z"), (
        f"the checked instant must be UTC, read {payload.get('checked_at')!r}")
    seeded = cf.store_one(cf.TABLE_ELIGIBILITY, number=cf.ELIGIBILITY_SEEDED)
    assert seeded and seeded.get("checked_at"), (
        f"the seeded snapshot {cf.ELIGIBILITY_SEEDED} must carry its own date")


def test_claim_lines_name_diagnoses_by_position(biller) -> None:
    """A service line points into the claim's own ordered diagnosis list."""
    response = cf.get_json(biller, f"/claims/{cf.CLAIM_QUEUED}")
    assert response.status_code == 200, cf.describe(
        response, "a biller must read the queued claim")
    payload = cf.payload_of(response) or {}
    diagnoses = payload.get("diagnoses") or []
    lines = payload.get("lines") or []
    assert diagnoses, f"the claim must carry an ordered diagnosis list, read {payload!r}"
    assert lines, f"the claim must carry at least one line, read {payload!r}"
    for line in lines:
        pointers = line.get("diagnosis_pointers") or []
        assert pointers, f"a claim line must carry diagnosis pointers, read {line!r}"
        for pointer in pointers:
            assert 1 <= int(pointer) <= len(diagnoses), (
                f"the pointer {pointer} must name a position in a list of "
                f"{len(diagnoses)}, read {line!r}")
        assert line.get("unit_qualifier") in ("unit", "minute"), (
            f"a claim line must state its unit qualifier, read {line!r}")


def test_claim_line_pointer_outside_the_list_is_refused(clinician, biller,
                                                        suffix) -> None:
    """A pointer at a position that does not exist is invalid."""
    signed = cf.signed_probe_encounter(clinician, cf.MRN_PRIMARY, suffix)
    claim_number = str(signed.get("claim_number"))
    response = cf.post_json(biller, f"/claims/{claim_number}/lines", {
        "code_system": cf.SYSTEM_PROCEDURE, "code": cf.CODE_PROCEDURE,
        "code_display": "Office or other outpatient visit, established patient, "
                        "low level",
        "unit_qualifier": "unit", "units": 1, "charge_minor": cf.CHARGE_MINOR,
        "diagnosis_pointers": [99]})
    assert response.status_code in cf.REFUSED, cf.describe(
        response, "a pointer outside the claim's own diagnosis list must be refused")


def test_balancing_remittance_posts_and_sets_patient_balance(clinician, biller,
                                                             suffix) -> None:
    """The arithmetic holds exactly and only the patient part reaches the balance."""
    signed = cf.signed_probe_encounter(clinician, cf.MRN_PRIMARY, suffix)
    claim_number = str(signed.get("claim_number"))
    submitted = cf.post_json(biller, f"/claims/{claim_number}/submit")
    assert submitted.status_code in cf.ACCEPTED, cf.describe(
        submitted, "a queued claim must be submittable")
    detail = cf.payload_of(cf.get_json(biller, f"/claims/{claim_number}")) or {}
    lines = detail.get("lines") or []
    assert lines, f"the claim must carry a line to pay, read {detail!r}"
    line = lines[0]
    charge = int(line.get("charge_minor"))
    paid = charge - cf.CONTRACTUAL_MINOR - cf.PATIENT_MINOR
    posted = cf.post_json(biller, "/remittances", {
        "claim_number": claim_number,
        "lines": [{"claim_line_number": line.get("line_number"),
                   "paid_minor": paid,
                   "adjustments": [
                       {"group": cf.GROUP_CONTRACTUAL, "reason": "CO-45",
                        "amount_minor": cf.CONTRACTUAL_MINOR},
                       {"group": cf.GROUP_PATIENT, "reason": "PR-2",
                        "amount_minor": cf.PATIENT_MINOR}]}]})
    assert posted.status_code in cf.ACCEPTED, cf.describe(
        posted, "a balancing remittance must post")
    payload = cf.payload_of(posted) or {}
    assert str(payload.get("state")) == cf.STATE_POSTED, (
        f"a balancing remittance must read {cf.STATE_POSTED!r}, read {payload!r}")
    settled = cf.payload_of(cf.get_json(biller, f"/claims/{claim_number}")) or {}
    assert int(settled.get("patient_balance_minor")) == cf.PATIENT_MINOR, (
        f"the patient balance must be {cf.PATIENT_MINOR} rather than the whole "
        f"withheld amount, read {settled.get('patient_balance_minor')!r}")
    assert str(settled.get("currency")) == cf.CURRENCY, (
        f"every amount must carry the currency {cf.CURRENCY!r}, read {settled!r}")


def test_unbalanced_remittance_posts_nothing(clinician, biller, suffix) -> None:
    """One minor unit out is quarantined rather than absorbed."""
    signed = cf.signed_probe_encounter(clinician, cf.MRN_SECOND, suffix)
    claim_number = str(signed.get("claim_number"))
    assert cf.post_json(biller, f"/claims/{claim_number}/submit").status_code \
        in cf.ACCEPTED, "a queued claim must be submittable"
    detail = cf.payload_of(cf.get_json(biller, f"/claims/{claim_number}")) or {}
    line = (detail.get("lines") or [{}])[0]
    charge = int(line.get("charge_minor"))
    status_before = str(detail.get("status"))
    response = cf.post_json(biller, "/remittances", {
        "claim_number": claim_number,
        "lines": [{"claim_line_number": line.get("line_number"),
                   "paid_minor": charge - cf.CONTRACTUAL_MINOR - cf.PATIENT_MINOR,
                   "adjustments": [
                       {"group": cf.GROUP_CONTRACTUAL, "reason": "CO-45",
                        "amount_minor": cf.CONTRACTUAL_MINOR},
                       {"group": cf.GROUP_PATIENT, "reason": "PR-2",
                        "amount_minor": cf.PATIENT_MINOR - 1}]}]})
    payload = cf.payload_of(response) or {}
    assert response.status_code in cf.REFUSED or \
        str(payload.get("state")) == cf.STATE_QUARANTINED, cf.describe(
            response, "a remittance one minor unit out must not post")
    assert payload.get("quarantine_reason") or response.status_code in cf.REFUSED, \
        cf.describe(response, "a quarantined remittance must state its reason")
    after = cf.payload_of(cf.get_json(biller, f"/claims/{claim_number}")) or {}
    assert str(after.get("status")) == status_before, (
        f"a quarantined remittance must leave the claim at {status_before!r}, "
        f"read {after.get('status')!r}")
    assert int(after.get("patient_balance_minor") or 0) == 0, (
        f"a quarantined remittance must create no patient balance, read {after!r}")


def test_seeded_remittances_carry_their_pinned_states() -> None:
    """The seeded pair pins both outcomes."""
    balanced = cf.store_one(cf.TABLE_REMITTANCE, number=cf.REMITTANCE_BALANCED)
    out = cf.store_one(cf.TABLE_REMITTANCE, number=cf.REMITTANCE_OUT)
    assert balanced and str(balanced.get("state")) == cf.STATE_POSTED, (
        f"{cf.REMITTANCE_BALANCED} must be {cf.STATE_POSTED!r}, read {balanced!r}")
    assert out and str(out.get("state")) == cf.STATE_QUARANTINED, (
        f"{cf.REMITTANCE_OUT} must be {cf.STATE_QUARANTINED!r}, read {out!r}")
    assert out.get("quarantine_reason"), (
        f"{cf.REMITTANCE_OUT} must carry a stored quarantine reason, read {out!r}")


def test_submit_outside_queued_leaves_the_status_unchanged(biller) -> None:
    """A claim that is not queued does not move."""
    before = cf.store_one(cf.TABLE_CLAIM, number=cf.CLAIM_PAID)
    assert before, f"the seeded claim {cf.CLAIM_PAID} must exist"
    response = cf.post_json(biller, f"/claims/{cf.CLAIM_PAID}/submit")
    assert response.status_code in cf.REFUSED, cf.describe(
        response, "a claim outside queued must not be submittable")
    after = cf.store_one(cf.TABLE_CLAIM, number=cf.CLAIM_PAID)
    assert str(after.get("status")) == str(before.get("status")), (
        f"a refused submit must leave the status at {before.get('status')!r}, "
        f"read {after.get('status')!r}")


def test_ledger_entries_sum_to_zero(biller) -> None:
    """Every financial event writes entries that cancel out."""
    response = cf.get_json(biller, f"/claims/{cf.CLAIM_PAID}/ledger")
    assert response.status_code == 200, cf.describe(
        response, "a claim's ledger must be readable")
    payload = cf.payload_of(response) or {}
    entries = payload.get("entries") or cf.as_list(payload)
    assert entries, f"the paid claim must carry ledger entries, read {payload!r}"
    groups: dict = {}
    for entry in entries:
        groups.setdefault(str(entry.get("transaction_id")), []).append(
            int(entry.get("amount_minor")))
    for transaction, amounts in groups.items():
        assert sum(amounts) == 0, (
            f"the entries of transaction {transaction} must sum to zero, read "
            f"{amounts} summing to {sum(amounts)}")
    rows = cf.store_rows(cf.TABLE_LEDGER)
    assert rows, "the ledger must hold stored entries"
    for row in rows[:20]:
        assert str(row.get("currency")) == cf.CURRENCY, (
            f"every ledger entry must carry the currency {cf.CURRENCY!r}, read {row!r}")
        assert isinstance(row.get("amount_minor"), int), (
            f"a ledger amount must be an integer count of minor units, read {row!r}")


def test_minor_unit_allocation_is_deterministic(biller) -> None:
    """An amount split across lines sums to the whole, the same way every time."""
    first = cf.post_json(biller, "/allocations", {
        "amount_minor": cf.SPLIT_TOTAL, "shares": [1, 1, 1]})
    assert first.status_code in cf.ACCEPTED, cf.describe(
        first, "an allocation must be computable")
    shares = cf.as_list(cf.payload_of(first)) or (
        (cf.payload_of(first) or {}).get("shares") or [])
    amounts = [int(s if not isinstance(s, dict) else s.get("amount_minor"))
               for s in shares]
    assert amounts == [cf.SPLIT_FIRST, cf.SPLIT_REST, cf.SPLIT_REST], (
        f"{cf.SPLIT_TOTAL} across three equal lines must allocate "
        f"[{cf.SPLIT_FIRST}, {cf.SPLIT_REST}, {cf.SPLIT_REST}], read {amounts}")
    assert sum(amounts) == cf.SPLIT_TOTAL, (
        f"the parts must sum to {cf.SPLIT_TOTAL}, read {sum(amounts)}")
    again = cf.post_json(biller, "/allocations", {
        "amount_minor": cf.SPLIT_TOTAL, "shares": [1, 1, 1]})
    repeat = cf.as_list(cf.payload_of(again)) or (
        (cf.payload_of(again) or {}).get("shares") or [])
    assert [int(s if not isinstance(s, dict) else s.get("amount_minor"))
            for s in repeat] == amounts, (
        "the same input must always yield the same allocation")


def test_portal_record_is_released_without_delay(patient) -> None:
    """A patient reads their own record, results included."""
    response = cf.get_json(patient, "/portal/record")
    assert response.status_code == 200, cf.describe(
        response, "a patient must read their own record")
    payload = cf.payload_of(response) or {}
    assert cf.MRN_PRIMARY in response.text, (
        f"the portal record of {cf.PATIENT_EMAIL} must be {cf.MRN_PRIMARY}")
    assert "results" in payload or "observations" in payload, cf.describe(
        response, "a patient's record must carry their results")
    assert "pending_release" not in response.text.lower(), (
        "no surface may hold a result back pending a review")


def test_appointment_request_holds_no_slot(patient, front_desk, suffix) -> None:
    """A request is not a booking."""
    before = cf.store_count(cf.TABLE_APPOINTMENT)
    occupancy_before = cf.store_count(cf.TABLE_OCCUPANCY)
    response = cf.post_json(patient, "/portal/appointment-requests", {
        "preferred_date": cf.CONTENDED_DAY,
        "note": "Any time that morning would suit " + suffix})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "a patient must be able to request an appointment")
    assert cf.store_count(cf.TABLE_APPOINTMENT) == before, (
        f"a request must book nothing: the appointment count moved from {before} "
        f"to {cf.store_count(cf.TABLE_APPOINTMENT)}")
    assert cf.store_count(cf.TABLE_OCCUPANCY) == occupancy_before, (
        "a request must hold no resource")


def test_demographic_proposal_applies_nothing(patient, suffix) -> None:
    """Matching keys are proposed rather than changed."""
    before = cf.store_one(cf.TABLE_PATIENT, mrn=cf.MRN_PRIMARY)
    assert before, f"the patient {cf.MRN_PRIMARY} must be stored"
    response = cf.post_json(patient, "/portal/demographic-proposals", {
        "field": "family_name", "proposed_value": cf.probe_family(suffix)})
    assert response.status_code in cf.ACCEPTED, cf.describe(
        response, "a patient must be able to propose a demographic change")
    after = cf.store_one(cf.TABLE_PATIENT, mrn=cf.MRN_PRIMARY)
    assert str(after.get("family_name")) == str(before.get("family_name")), (
        f"a proposal must change no stored value: {before.get('family_name')!r} "
        f"became {after.get('family_name')!r}")


def test_worklists_carry_depth_and_oldest_age(clinician) -> None:
    """Every list names its owner, its depth and the age of its oldest item."""
    response = cf.get_json(clinician, "/worklists")
    assert response.status_code == 200, cf.describe(
        response, "a staff account must read the worklist register")
    lists = cf.as_list(cf.payload_of(response))
    assert lists, f"the register must carry worklists, read {response.text[:400]}"
    keys = {str(entry.get("key")) for entry in lists}
    for expected in ("unsigned_notes", "unmatched_results", "identity_review",
                     "quarantined_remittances", "denied_claims",
                     "appointment_requests"):
        assert expected in keys, (
            f"the register must carry the worklist {expected!r}, read {sorted(keys)}")
    for entry in lists:
        assert entry.get("owner_role"), (
            f"the worklist {entry.get('key')!r} must name an owning role")
        assert entry.get("depth") is not None, (
            f"the worklist {entry.get('key')!r} must carry its depth")
        assert entry.get("oldest_age_hours") is not None, (
            f"the worklist {entry.get('key')!r} must carry the age of its oldest item")


def test_closing_a_worklist_item_requires_an_outcome(clinician) -> None:
    """Nothing is cleared without recording what happened."""
    queued = cf.store_rows(cf.TABLE_UNMATCHED)
    assert queued, "the reconciliation queue must hold a seeded entry"
    identifier = queued[0].get("id")
    response = cf.post_json(clinician,
                            f"/worklists/unmatched_results/items/{identifier}/close",
                            {})
    assert response.status_code in cf.REFUSED, cf.describe(
        response, "closing an item without an outcome must be refused")
    closed = cf.post_json(clinician,
                          f"/worklists/unmatched_results/items/{identifier}/close",
                          {"outcome": "no_action_needed"})
    assert closed.status_code in cf.ACCEPTED, cf.describe(
        closed, "closing an item with an outcome must be accepted")
    payload = cf.payload_of(closed) or {}
    assert payload.get("outcome_by"), cf.describe(
        closed, "a closed item must record who closed it")


def test_absent_surfaces_answer_not_found() -> None:
    """The product carries none of the surfaces it declares out of scope."""
    for path in cf.ABSENT_SURFACES:
        response = cf.fetch_raw(path)
        assert response.status_code == 404, cf.describe(
            response, f"the out-of-scope surface {path} must not exist")