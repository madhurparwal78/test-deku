"""Graders for Aurelia.

Every assertion reads the running app, the persisted rows, the object store or a
rendered page. Nothing here reads the app's own claim about its own effect.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import httpx

from conftest import (
    ACCOUNT_CREDIT,
    ACCOUNT_OPERATING,
    ACCOUNT_OPERATING_TWO,
    ACCOUNT_TREASURY,
    ANNOUNCEMENT,
    APPLY_MINUTES,
    BREAK_KINDS,
    CAMPAIGN_PATHS,
    CARD_AUTHORISATION_MINOR,
    CARD_CLEARING_MINOR,
    CLAIMING_ROUTES,
    CLASS_HOLD,
    CLASS_IN_TRANSIT,
    CLASS_RESIDUAL,
    CLASS_RETURNS_SUSPENSE,
    CLASS_UNMATCHED,
    CLI_CONTROL,
    CONCURRENT_IDEMPOTENT_CALLS,
    CONCURRENT_POSTINGS,
    CONFLICT_STATUSES,
    CONTRAST_BAR,
    CORRELATION_FIELD,
    CURRENCY_STORED,
    CURRENCY_WIRE,
    CUTOFF_ACH,
    CUTOFF_TIMEZONE,
    DENIAL_STATUSES,
    DEVELOPER_HEADLINE,
    DEVELOPER_TITLE,
    DISCLOSURE,
    DRAFT_PAGE_ROUTE,
    DRAFT_PAGE_TITLE,
    FEATURE_HEADING,
    FEES,
    FEE_EFFECTIVE_FROM,
    FEE_WIRE_DOMESTIC,
    FEE_WIRE_DOMESTIC_MINOR,
    FOOTNOTE_MARKERS,
    HERO_FIELD,
    HERO_HEADLINE,
    HERO_PRIMARY,
    HERO_SECONDARY,
    HOLIDAY_ONE,
    HOME_TITLE,
    IDEMPOTENCY_HEADER,
    INITIATOR_EMAIL,
    LEDGER_CLASSES,
    MERCHANT_RESTAURANT,
    NAV_ITEMS,
    NOT_FOUND_STATUSES,
    OBJECT_KEY_PREFIX,
    OWNER_EMAIL,
    PAGE_STATE_DRAFT,
    PAGE_STATE_PUBLISHED,
    PARTNER_BANK_ONE,
    PARTNER_BANK_TWO,
    PASSWORD,
    PAYMENT_LIMIT_PER_MINUTE,
    POLICY_REQUIRED_APPROVALS,
    POLICY_THRESHOLD_MINOR,
    POLICY_VERSION,
    PRODUCT_ROUTES,
    PUBLIC_ROUTES,
    RAILS,
    RAIL_ACH,
    RAIL_REALTIME,
    RAIL_WIRE,
    READ_LIMIT_PER_MINUTE,
    RECIPIENT_CLEAN,
    RECIPIENT_CLEAN_ID,
    RECIPIENT_LISTED,
    RECIPIENT_LISTED_ID,
    RECONCILIATION_RUN_DATE,
    REDIRECT_STATUSES,
    REFUSAL_STATUSES,
    RESOURCES,
    RESPONSIVE_TIERS,
    ROLES,
    SANCTIONS_VERSION_CLEAN,
    SANCTIONS_VERSION_LISTED,
    SERVER_ERROR_TITLE,
    SKIP_LINK,
    STATEMENT_PERIOD,
    STATUSES,
    STATUS_APPROVED,
    STATUS_PENDING,
    STATUS_RECALL_REQUESTED,
    STATUS_RETURNED,
    STATUS_SCHEDULED,
    STATUS_SETTLED,
    STEP_UP_ACTIONS,
    STUDIO_ROUTES,
    SUCCESS_STATUSES,
    SUPPORT_TITLE,
    WORDMARK,
    YIELD_AS_OF,
    YIELD_BASIS_POINTS,
    YIELD_DAY_COUNT,
    ORG_ONE,
    ORG_ONE_SLUG,
    ORG_TWO,
    ORG_TWO_SLUG,
    Session,
    APP_DB_ROLE,
    BINARY_ASSET_SUFFIXES,
    contrast_ratio,
    describe,
    field_of,
    first_operating_account,
    idempotency_key,
    minor_to_decimal,
    parse_rgb,
    payload_of,
    payment_body,
    poll_until,
    probe_email,
    rows_of,
    settle,
    unique_suffix,
)

import appclient


def test_health_route_and_reserved_directories_exist(app_base, store):
    response = httpx.get(f"{app_base}/health", timeout=30.0)
    assert response.status_code == 200, describe(response)

    missing = httpx.get(f"{app_base}/no-such-resource", timeout=30.0)
    assert missing.status_code in REFUSAL_STATUSES, describe(missing)
    assert CORRELATION_FIELD in missing.json(), (
        f"an error body carries {CORRELATION_FIELD}: {describe(missing)}")

    assert store.count("organisation") > 0, (
        "the organisations must live in PostgreSQL, not in the process")


def test_seeded_organisations_and_bank_accounts_are_stored_rows(store):
    for slug, legal_name in ((ORG_ONE_SLUG, ORG_ONE), (ORG_TWO_SLUG, ORG_TWO)):
        row = store.organisation(slug)
        assert row is not None, f"seeded organisation {slug} is absent from the store"
        assert row["legal_name"] == legal_name, (
            f"{slug} legal_name is {row['legal_name']!r}")

    for name, kind, bank in ((ACCOUNT_OPERATING, "operating", PARTNER_BANK_ONE),
                             (ACCOUNT_TREASURY, "treasury", PARTNER_BANK_TWO),
                             (ACCOUNT_CREDIT, "credit", PARTNER_BANK_ONE)):
        account = store.bank_account(name)
        assert account is not None, f"seeded account {name} is absent from the store"
        assert account["kind"] == kind, f"{name} kind is {account['kind']!r}"

    other = store.bank_account(ACCOUNT_OPERATING_TWO)
    assert other is not None, f"{ACCOUNT_OPERATING_TWO} is absent from the store"

    for role in ROLES:
        assert store.count("membership", role=role) >= 1, (
            f"no seeded membership carries the role {role!r}")


def test_seed_is_idempotent_no_duplicate_rows(store):
    for table, column in (("organisation", "slug"), ("account", "email"),
                          ("fee", "code"), ("recipient", "external_id"),
                          ("page", "route")):
        rows = store.query(f"SELECT {column}, count(*) AS n FROM {table} "
                           f"GROUP BY {column} HAVING count(*) > 1")
        assert rows == [], f"{table} carries duplicate {column} values: {rows}"

    signed_in = appclient.login(OWNER_EMAIL, PASSWORD)
    assert signed_in, (
        f"the pinned password must work at login for {OWNER_EMAIL}")


def test_seeded_fee_records_carry_the_pinned_amounts(store):
    for code, amount in FEES.items():
        row = store.fee(code)
        assert row is not None, f"seeded fee {code} is absent from the store"
        assert int(row["amount_minor"]) == amount, (
            f"{code} amount_minor is {row['amount_minor']!r}, expected {amount}")
        assert row["currency"] == CURRENCY_STORED, (
            f"{code} currency is {row['currency']!r}")
        assert str(row["effective_from"]).startswith(FEE_EFFECTIVE_FROM), (
            f"{code} effective_from is {row['effective_from']!r}")


def test_seeded_footnote_registry_holds_seven_markers(store):
    markers = {int(row["marker"]) for row in store.rows("footnote")}
    assert markers == set(FOOTNOTE_MARKERS), (
        f"the footnote registry holds markers {sorted(markers)}, "
        f"expected {list(FOOTNOTE_MARKERS)}")
    for row in store.rows("footnote"):
        assert str(row["text"]).strip(), (
            f"footnote {row['marker']} carries no text")
        assert str(row["as_of_date"]).strip(), (
            f"footnote {row['marker']} carries no as-of date")


def test_every_public_route_carries_a_unique_title_and_description(site_base):
    titles, descriptions = {}, {}
    for route in PUBLIC_ROUTES:
        response = httpx.get(f"{site_base}{route}", timeout=30.0,
                             follow_redirects=True)
        assert response.status_code in SUCCESS_STATUSES, describe(response)
        body = response.text
        title = body.split("<title>", 1)[-1].split("</title>", 1)[0].strip()
        assert title, f"{route} serves no title: {describe(response)}"
        assert title not in titles, (
            f"{route} shares its title with {titles[title]}")
        titles[title] = route
        marker = 'name="description"'
        assert marker in body, f"{route} declares no description"
        description = body.split(marker, 1)[1].split(">", 1)[0]
        assert description not in descriptions, (
            f"{route} shares its description with {descriptions[description]}")
        descriptions[description] = route

    home = httpx.get(f"{site_base}/", timeout=30.0)
    assert HOME_TITLE in home.text, f"the home title is absent: {describe(home)}"
    developer = httpx.get(f"{site_base}/developers", timeout=30.0)
    assert DEVELOPER_TITLE in developer.text, describe(developer)
    support = httpx.get(f"{site_base}/faq", timeout=30.0)
    assert SUPPORT_TITLE in support.text, describe(support)


def test_disclosure_is_served_in_the_document_of_every_claiming_route(site_base):
    for route in CLAIMING_ROUTES:
        response = httpx.get(f"{site_base}{route}", timeout=30.0)
        assert response.status_code in SUCCESS_STATUSES, describe(response)
        assert DISCLOSURE in response.text, (
            f"{route} does not carry the disclosure sentence in the served "
            f"document: {describe(response)}")
        assert PARTNER_BANK_ONE in response.text, f"{route} omits the first bank"
        assert PARTNER_BANK_TWO in response.text, f"{route} omits the second bank"


def test_unknown_path_is_not_found_and_no_path_serves_home_with_success(site_base):
    unknown = httpx.get(f"{site_base}/no-such-page-{unique_suffix()}",
                        timeout=30.0)
    assert unknown.status_code in NOT_FOUND_STATUSES, describe(unknown)
    assert HOME_TITLE not in unknown.text, (
        "an unknown address must not serve the home document")
    assert "/faq" in unknown.text, (
        "the not-found page offers a route to the support library")


def test_campaign_paths_redirect_permanently(site_base):
    for path in CAMPAIGN_PATHS:
        response = httpx.get(f"{site_base}{path}", timeout=30.0,
                             follow_redirects=False)
        assert response.status_code in REDIRECT_STATUSES, (
            f"{path} answers {response.status_code} instead of redirecting: "
            f"{describe(response)}")
        assert response.headers.get("location"), (
            f"{path} redirects with no destination: {describe(response)}")


def test_sitemap_lists_published_routes_and_robots_names_the_sitemap(site_base):
    sitemap = httpx.get(f"{site_base}/sitemap.xml", timeout=30.0)
    assert sitemap.status_code in SUCCESS_STATUSES, describe(sitemap)
    for route in ("/pricing", "/faq", "/developers"):
        assert route in sitemap.text, f"{route} is absent from the sitemap"
    assert DRAFT_PAGE_ROUTE not in sitemap.text, (
        "a draft route must not appear in the sitemap")

    robots = httpx.get(f"{site_base}/robots.txt", timeout=30.0)
    assert robots.status_code in SUCCESS_STATUSES, describe(robots)
    assert "sitemap" in robots.text.lower(), describe(robots)


def test_favicon_asset_is_served_and_declared_in_the_document_head(site_base):
    home = httpx.get(f"{site_base}/", timeout=30.0)
    assert "icon" in home.text.lower(), (
        f"the document head declares no icon: {describe(home)}")
    icon = httpx.get(f"{site_base}/favicon.ico", timeout=30.0)
    assert icon.status_code in SUCCESS_STATUSES, describe(icon)


def test_every_internal_link_on_a_public_route_resolves(site_base):
    seen = set()
    for route in ("/", "/pricing", "/faq", "/developers"):
        response = httpx.get(f"{site_base}{route}", timeout=30.0)
        assert response.status_code in SUCCESS_STATUSES, describe(response)
        for chunk in response.text.split('href="')[1:]:
            target = chunk.split('"', 1)[0]
            if target.startswith("/") and not target.startswith("//"):
                seen.add(target.split("#", 1)[0] or "/")
    assert seen, "no internal link was found on the sampled public routes"
    for target in sorted(seen):
        linked = httpx.get(f"{site_base}{target}", timeout=30.0,
                           follow_redirects=True)
        assert linked.status_code in SUCCESS_STATUSES, (
            f"internal link {target} does not resolve: {describe(linked)}")


def test_page_view_record_is_stored_and_read_only_by_the_editor(
        store, editor, owner, site_base):
    before = store.count("page_view")
    httpx.get(f"{site_base}/pricing", timeout=30.0)
    settle()
    after = poll_until(lambda: store.count("page_view") > before)
    assert after, "a page view was not recorded as a row"

    allowed = editor.get("/page-views")
    assert allowed.status_code in SUCCESS_STATUSES, describe(allowed)
    denied = owner.get("/page-views")
    assert denied.status_code in DENIAL_STATUSES, (
        f"an organisation owner must not read the page-view record: "
        f"{describe(denied)}")


def test_one_fee_source_agrees_across_pricing_schedule_and_support_answer(
        site_base, anonymous):
    decimal = minor_to_decimal(FEE_WIRE_DOMESTIC_MINOR)
    for route in ("/pricing", "/legal/fees", "/faq"):
        response = httpx.get(f"{site_base}{route}", timeout=30.0)
        assert response.status_code in SUCCESS_STATUSES, describe(response)
        assert decimal in response.text, (
            f"{route} does not state the domestic wire fee as {decimal}: "
            f"{describe(response)}")

    complaints = httpx.get(f"{site_base}/legal/complaints", timeout=30.0)
    assert complaints.status_code in SUCCESS_STATUSES, describe(complaints)

    fees = anonymous.fees()
    assert fees.status_code in SUCCESS_STATUSES, describe(fees)
    published = {row["code"]: int(row["amount_minor"]) for row in rows_of(fees)}
    assert published.get(FEE_WIRE_DOMESTIC) == FEE_WIRE_DOMESTIC_MINOR, (
        f"the fee source states {published.get(FEE_WIRE_DOMESTIC)!r}")


def test_support_answers_carry_stable_anchors_and_structured_data(site_base):
    response = httpx.get(f"{site_base}/faq", timeout=30.0)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    assert 'id="' in response.text, (
        f"no answer carries an anchor: {describe(response)}")
    assert "FAQPage" in response.text or "Question" in response.text, (
        f"the support library carries no question structured data: "
        f"{describe(response)}")

    searched = httpx.get(f"{site_base}/faq", params={"q": "wire"}, timeout=30.0)
    assert searched.status_code in SUCCESS_STATUSES, describe(searched)
    assert "q=wire" in str(searched.url), (
        f"the search is not reflected in the address: {describe(searched)}")


def test_developer_reference_lists_fifteen_resources_with_descriptions(site_base):
    response = httpx.get(f"{site_base}/developers", timeout=30.0)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.text
    assert DEVELOPER_HEADLINE in body, describe(response)
    assert CLI_CONTROL in body, describe(response)
    for name, description in RESOURCES.items():
        assert name in body, f"resource {name} is absent from the reference"
        assert description in body, (
            f"the description for {name} is absent from the reference")


def test_worked_request_and_response_state_one_amount(site_base):
    response = httpx.get(f"{site_base}/developers", timeout=30.0)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.text
    assert "idempotency-key" in body.lower(), (
        f"the worked request does not carry an idempotency key: "
        f"{describe(response)}")
    assert "preq_" in body, "the worked response carries no prefixed payment id"
    assert "rcpt_" in body, "the worked response carries no prefixed recipient id"
    assert CURRENCY_WIRE in body, "the worked response carries no currency"

    amounts = set()
    for chunk in body.split("--amount ")[1:]:
        amounts.add(chunk.split()[0].strip().strip('",'))
    for chunk in body.split('"amount"')[1:]:
        amounts.add(chunk.split(":", 1)[1].split(",", 1)[0].strip().strip('" '))
    assert len(amounts) == 1, (
        f"the worked request and its response state different amounts: "
        f"{sorted(amounts)}")


def test_draft_page_is_denied_to_a_signed_out_caller(store, site_base, anonymous):
    row = store.page(DRAFT_PAGE_ROUTE)
    assert row is not None, f"the seeded draft page {DRAFT_PAGE_ROUTE} is absent"
    assert row["state"] == PAGE_STATE_DRAFT, (
        f"the seeded page state is {row['state']!r}")
    assert row["title"] == DRAFT_PAGE_TITLE, (
        f"the seeded draft title is {row['title']!r}")

    direct = httpx.get(f"{site_base}{DRAFT_PAGE_ROUTE}", timeout=30.0)
    assert direct.status_code in DENIAL_STATUSES, (
        f"a signed-out caller reached a draft page: {describe(direct)}")
    over_api = anonymous.get(f"/pages{DRAFT_PAGE_ROUTE}")
    assert over_api.status_code in DENIAL_STATUSES, (
        f"a draft page is readable over the API: {describe(over_api)}")


def test_publishing_a_draft_makes_the_page_readable_and_listed(editor, site_base):
    route = f"/resources/guides/probe-{unique_suffix()}"
    created = editor.post("/pages", {"route": route, "title": "Sweep and cover",
                                     "description": "How the sweep works",
                                     "body": "A guide to the sweep program."})
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    page_id = field_of(payload_of(created), "id")

    before = httpx.get(f"{site_base}{route}", timeout=30.0)
    assert before.status_code in DENIAL_STATUSES, (
        f"a freshly written page is readable before publication: "
        f"{describe(before)}")

    published = editor.post(f"/pages/{page_id}/publish", {})
    assert published.status_code in SUCCESS_STATUSES, describe(published)
    assert field_of(payload_of(published), "state") == PAGE_STATE_PUBLISHED

    after = httpx.get(f"{site_base}{route}", timeout=30.0)
    assert after.status_code in SUCCESS_STATUSES, (
        f"a published page is still unreadable: {describe(after)}")

    sitemap = httpx.get(f"{site_base}/sitemap.xml", timeout=30.0)
    assert route in sitemap.text, "a published route is absent from the sitemap"


def test_editorial_form_refuses_invalid_input_and_writes_nothing(editor, store):
    before = store.count("page")
    refused = editor.post("/pages", {"route": "", "title": "",
                                     "description": "", "body": ""})
    assert refused.status_code in REFUSAL_STATUSES, describe(refused)
    body = refused.json()
    assert "route" in str(body).lower() or "title" in str(body).lower(), (
        f"the refusal does not name the field that was wrong: {describe(refused)}")
    assert store.count("page") == before, (
        "a refused form wrote a page row anyway")


def test_page_with_an_unregistered_marker_cannot_be_published(editor):
    route = f"/resources/guides/probe-{unique_suffix()}"
    created = editor.post("/pages", {"route": route, "title": "Instant claims",
                                     "description": "A claim with no footnote",
                                     "body": "Payments are instant[99]."})
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    page_id = field_of(payload_of(created), "id")
    refused = editor.post(f"/pages/{page_id}/publish", {})
    assert refused.status_code in REFUSAL_STATUSES, (
        f"a page carrying an unregistered marker was published: "
        f"{describe(refused)}")


def test_application_provisions_an_organisation_with_balanced_opening_entries(
        anonymous, store):
    email = probe_email()
    started = anonymous.post("/applications", {"email": email})
    assert started.status_code in SUCCESS_STATUSES, describe(started)
    application_id = field_of(payload_of(started), "id")

    legal_name = f"Probe Instruments {unique_suffix()}"
    business = anonymous.patch(f"/applications/{application_id}", {
        "legal_name": legal_name,
        "trading_name": "Probe",
        "entity_type": "corporation",
        "formation_jurisdiction": "DE",
        "registration_number": "PR-0001",
        "formation_date": "2024-01-15",
        "tax_identifier": "00-0000000",
        "business_classification": "5045",
        "registered_address": "1 Probe Way",
        "operating_address": "2 Probe Way",
        "expected_activity": {"monthly_volume_minor": 500000,
                              "counterparties": 4, "geographies": ["US"]},
    })
    assert business.status_code in SUCCESS_STATUSES, describe(business)

    owner_added = anonymous.post(f"/applications/{application_id}/owners", {
        "legal_name": "Ada Probe", "kind": "person",
        "ownership_percent_basis_points": 6000, "is_control_person": True,
        "date_of_birth": "1985-04-02", "address": "3 Probe Way",
        "government_identifier_last4": "1234"})
    assert owner_added.status_code in SUCCESS_STATUSES, describe(owner_added)

    attested = anonymous.post(f"/applications/{application_id}/attestations",
                              {"text_shown": "I confirm the details are true."})
    assert attested.status_code in SUCCESS_STATUSES, describe(attested)

    decided = anonymous.post(f"/applications/{application_id}/submit", {})
    assert decided.status_code in SUCCESS_STATUSES, describe(decided)
    decision = field_of(payload_of(decided), "decision")
    assert decision in ("approve", "approved", "decline", "declined", "refer",
                        "referred"), f"unexpected decision {decision!r}"

    if decision in ("approve", "approved"):
        organisation = store.query(
            "SELECT * FROM organisation WHERE legal_name = %s", (legal_name,))
        assert organisation, "approval created no organisation row"
        accounts = store.query(
            "SELECT * FROM bank_account WHERE organisation_id = %s",
            (organisation[0]["id"],))
        assert accounts, "approval opened no operating account"
        postings = store.query(
            "SELECT * FROM posting WHERE organisation_id = %s",
            (organisation[0]["id"],))
        assert postings, "approval wrote no opening posting"
        for posting in postings:
            assert store.posting_is_balanced(posting["id"]), (
                f"opening posting {posting['id']} does not balance")


def test_application_stores_attestation_text_shown_at_acceptance(
        anonymous, store):
    email = probe_email()
    started = anonymous.post("/applications", {"email": email})
    assert started.status_code in SUCCESS_STATUSES, describe(started)
    application_id = field_of(payload_of(started), "id")

    shown = f"I accept the deposit agreement dated {unique_suffix()}."
    accepted = anonymous.post(f"/applications/{application_id}/attestations",
                              {"text_shown": shown})
    assert accepted.status_code in SUCCESS_STATUSES, describe(accepted)

    rows = store.query("SELECT * FROM attestation WHERE application_id = %s",
                       (application_id,))
    assert rows, "the acceptance wrote no attestation row"
    assert any(row["text_shown"] == shown for row in rows), (
        "the attestation stored a reference rather than the text that was shown")
    assert all(row["accepted_at"] is not None for row in rows), (
        "an attestation carries no acceptance moment")

    parent = anonymous.post(f"/applications/{application_id}/owners", {
        "legal_name": "Holdco Probe", "kind": "entity",
        "ownership_percent_basis_points": 10000, "is_control_person": False})
    assert parent.status_code in SUCCESS_STATUSES, describe(parent)
    parent_id = field_of(payload_of(parent), "id")
    child = anonymous.post(f"/applications/{application_id}/owners", {
        "legal_name": "Bea Probe", "kind": "person",
        "parent_owner_id": parent_id,
        "ownership_percent_basis_points": 10000, "is_control_person": True,
        "date_of_birth": "1979-11-30", "address": "4 Probe Way",
        "government_identifier_last4": "5678"})
    assert child.status_code in SUCCESS_STATUSES, describe(child)
    graph = store.query(
        "SELECT * FROM beneficial_owner WHERE application_id = %s",
        (application_id,))
    assert any(row["parent_owner_id"] is not None for row in graph), (
        "ownership through an intermediate entity was flattened to a list")
    assert any(row["is_control_person"] for row in graph), (
        "no control person was identified")

    checks = store.query(
        "SELECT * FROM identity_check WHERE beneficial_owner_id IN "
        "(SELECT id FROM beneficial_owner WHERE application_id = %s)",
        (application_id,))
    for row in checks:
        assert row["evidence"], (
            "an identity check stored a verdict with no evidence behind it")


def test_uploaded_formation_document_lands_in_the_object_store_at_its_key(
        anonymous, store, objects):
    email = probe_email()
    started = anonymous.post("/applications", {"email": email})
    assert started.status_code in SUCCESS_STATUSES, describe(started)
    application_id = field_of(payload_of(started), "id")

    payload = f"formation-document-{unique_suffix()}".encode("utf-8")
    uploaded = anonymous.request(
        "POST", f"/applications/{application_id}/documents",
        body={"kind": "formation", "filename": "formation.pdf",
              "content_base64": payload.hex()})
    assert uploaded.status_code in SUCCESS_STATUSES, describe(uploaded)
    key = field_of(payload_of(uploaded), "object_key", "key")

    assert key.startswith(f"{OBJECT_KEY_PREFIX}/formation/"), (
        f"the stored key {key!r} does not follow the pinned scheme")
    assert objects.exists(key), (
        f"the uploaded bytes are not an object in the store at {key!r}")

    rows = store.query("SELECT * FROM document WHERE object_key = %s", (key,))
    assert rows, "the upload wrote no document row naming the object"


def test_two_hundred_concurrent_postings_keep_the_derived_balance_exact(
        owner, store):
    account = first_operating_account(owner)
    ledger_account_id = field_of(account, "ledger_account_id")
    before = store.derived_balance(ledger_account_id)

    def one_posting(index: int) -> httpx.Response:
        session = Session(owner.token, owner.email)
        return session.post("/postings", {
            "ledger_account_id": ledger_account_id,
            "amount": "1.00", "currency": CURRENCY_WIRE,
            "cause_kind": "probe", "cause_id": f"probe-{index}",
            "effective_date": FEE_EFFECTIVE_FROM})

    with ThreadPoolExecutor(max_workers=25) as pool:
        responses = list(pool.map(one_posting, range(CONCURRENT_POSTINGS)))

    accepted = [r for r in responses if r.status_code in SUCCESS_STATUSES]
    assert accepted, (
        f"no posting was accepted: {describe(responses[0])}")
    settle()
    after = store.derived_balance(ledger_account_id)
    assert after - before == 100 * len(accepted), (
        f"the derived balance moved by {after - before} minor units against "
        f"{len(accepted)} accepted postings of 100 each")

    for posting in store.rows("posting", limit=50):
        assert store.posting_is_balanced(posting["id"]), (
            f"posting {posting['id']} does not balance")
        assert posting["effective_date"] is not None, (
            f"posting {posting['id']} carries no effective date")
        assert posting["recorded_at"] is not None, (
            f"posting {posting['id']} carries no recorded-at instant")
        assert posting["cause_kind"], (
            f"posting {posting['id']} names no cause")


def test_ledger_entry_update_and_delete_are_refused_by_the_database(store):
    rows = store.rows("entry", limit=1)
    assert rows, "the ledger carries no entry to attempt an edit against"
    entry_id = rows[0]["id"]

    grants = store.query(
        "SELECT has_table_privilege(%s, 'entry', 'UPDATE') AS may_update, "
        "has_table_privilege(%s, 'entry', 'DELETE') AS may_delete",
        (APP_DB_ROLE, APP_DB_ROLE))
    assert grants, "the engine reported no privilege row for the application role"
    guards = store.query(
        "SELECT tgname FROM pg_trigger WHERE tgrelid = 'entry'::regclass "
        "AND NOT tgisinternal")
    engine_refuses = (
        (grants[0]["may_update"] is False and grants[0]["may_delete"] is False)
        or bool(guards))
    assert engine_refuses, (
        f"the application role may still update and delete ledger entry "
        f"{entry_id} and the engine carries no guard against it: {grants[0]}")

    classes = {row["class"] for row in store.rows("ledger_account")}
    for required in (CLASS_IN_TRANSIT, CLASS_RETURNS_SUSPENSE, CLASS_UNMATCHED,
                     CLASS_RESIDUAL, CLASS_HOLD):
        assert required in classes, (
            f"the ledger carries no {required} account; classes are "
            f"{sorted(classes)}")
    assert set(classes).issubset(set(LEDGER_CLASSES)), (
        f"unexpected ledger account classes {sorted(set(classes) - set(LEDGER_CLASSES))}")


def test_balance_as_at_a_past_date_is_answerable(owner, store):
    account = first_operating_account(owner)
    account_id = field_of(account, "id")
    response = owner.balance(account_id, as_of=FEE_EFFECTIVE_FROM)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = payload_of(response)
    current = field_of(body, "current", "current_minor")
    assert isinstance(current, (int, str)), (
        f"a balance is an integer or a decimal string, got {type(current).__name__}")
    assert not isinstance(current, float), (
        "a money value must never be a floating-point number")


def test_available_balance_excludes_a_live_hold_and_spending_uses_available(
        owner, store):
    account = first_operating_account(owner)
    account_id = field_of(account, "id")
    before = owner.balance(account_id)
    assert before.status_code in SUCCESS_STATUSES, describe(before)
    body = payload_of(before)
    current = int(field_of(body, "current_minor"))
    available = int(field_of(body, "available_minor"))
    assert "current_minor" in body and "available_minor" in body, (
        f"the balance response does not label which figure is which: {body}")

    cards = owner.cards()
    assert cards.status_code in SUCCESS_STATUSES, describe(cards)
    card_id = field_of(rows_of(cards)[0], "id")
    authorised = owner.authorise_card(card_id, {
        "amount": minor_to_decimal(CARD_AUTHORISATION_MINOR),
        "currency": CURRENCY_WIRE, "merchant_category": MERCHANT_RESTAURANT,
        "merchant_name": "Probe Diner"})
    assert authorised.status_code in SUCCESS_STATUSES, describe(authorised)

    settle()
    after = payload_of(owner.balance(account_id))
    assert int(field_of(after, "current_minor")) == current, (
        "an authorisation posted a settled movement instead of a hold")
    assert int(field_of(after, "available_minor")) == available - CARD_AUTHORISATION_MINOR, (
        "the hold was not taken off the available balance")

    hold_account = store.ledger_account(CLASS_HOLD)
    assert hold_account is not None, "there is no hold ledger account"
    assert store.entries_for(hold_account["id"]), (
        "the hold is a flag rather than a posting in the ledger")


def test_expired_card_hold_is_released_by_a_posting_without_a_prior_read(
        owner, store):
    cards = owner.cards()
    assert cards.status_code in SUCCESS_STATUSES, describe(cards)
    card_id = field_of(rows_of(cards)[0], "id")
    authorised = owner.authorise_card(card_id, {
        "amount": minor_to_decimal(CARD_AUTHORISATION_MINOR),
        "currency": CURRENCY_WIRE, "merchant_category": MERCHANT_RESTAURANT,
        "merchant_name": "Probe Diner"})
    assert authorised.status_code in SUCCESS_STATUSES, describe(authorised)
    authorisation_id = field_of(payload_of(authorised), "id")

    advanced = owner.post("/operations/advance-clock",
                          {"days": 3, "scope": "card_holds"})
    assert advanced.status_code in SUCCESS_STATUSES, describe(advanced)

    released = poll_until(lambda: store.query(
        "SELECT * FROM hold WHERE cause_id = %s AND released_posting_id IS NOT NULL",
        (str(authorisation_id),)))
    assert released, (
        "an expired authorisation hold was not released by a posting")


def test_interest_residual_account_absorbs_the_rounding_difference(owner, store):
    run = owner.post("/operations/accrue-interest", {"days": 30})
    assert run.status_code in SUCCESS_STATUSES, describe(run)
    body = payload_of(run)
    credited = int(field_of(body, "credited_minor"))
    residual = int(field_of(body, "residual_minor"))
    exact = int(field_of(body, "exact_micro_minor"))
    assert (credited * 1000000 + residual * 1000000) >= 0, (
        "the accrual reported a negative total")
    assert abs(exact - (credited + residual) * 1000000) < 1000000, (
        f"credited {credited} plus residual {residual} does not reconcile with "
        f"the exactly computed total {exact}")

    residual_account = store.ledger_account(CLASS_RESIDUAL)
    assert residual_account is not None, "there is no rounding residual account"

    rates = store.rows("rate_version")
    assert any(int(row["rate_basis_points"]) == YIELD_BASIS_POINTS
               and int(row["day_count"]) == YIELD_DAY_COUNT
               and str(row["effective_from"]).startswith(YIELD_AS_OF)
               for row in rates), (
        f"the seeded rate version is absent from {rates}")


def test_credit_account_balance_carries_the_opposite_sign(owner):
    response = owner.accounts()
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    rows = rows_of(response)
    deposit = [r for r in rows if r.get("kind") == "operating"]
    credit = [r for r in rows if r.get("kind") == "credit"]
    assert deposit and credit, f"both account kinds must be listed: {rows}"
    for row in credit:
        assert row.get("kind") == "credit", row
        assert "owed" in str(row).lower() or int(row.get("current_minor", 0)) <= 0, (
            f"a credit balance is presented as a deposit: {row}")

    treasury = owner.treasury()
    assert treasury.status_code in SUCCESS_STATUSES, describe(treasury)
    exposure = payload_of(treasury)
    per_bank = field_of(exposure, "per_bank_exposure_minor")
    assert PARTNER_BANK_ONE in per_bank and PARTNER_BANK_TWO in per_bank, (
        f"per-bank exposure is not reported for both banks: {per_bank}")
    coverage = int(field_of(exposure, "insured_coverage_minor"))
    assert coverage == sum(min(int(v), 25000000) for v in per_bank.values()), (
        "the coverage figure is asserted rather than derived from the allocation")


def test_ach_payment_moves_through_in_transit_to_settled(
        initiator, approver, owner, store):
    account = first_operating_account(owner)
    created = initiator.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_CLEAN_ID, "125.00", RAIL_ACH))
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    body = payload_of(created)
    payment_id = field_of(body, "id")
    assert field_of(body, "status") == STATUS_PENDING, (
        f"a policy-governed payment did not enter {STATUS_PENDING}: {body}")
    assert field_of(body, "currency") == CURRENCY_WIRE, body
    assert field_of(body, "amount") == "125.00", body

    approved = approver.approve_payment(payment_id)
    assert approved.status_code in SUCCESS_STATUSES, describe(approved)
    assert field_of(payload_of(approved), "status") in (
        STATUS_APPROVED, STATUS_SCHEDULED), payload_of(approved)

    submitted = owner.post(f"/payments/{payment_id}/submit", {})
    assert submitted.status_code in SUCCESS_STATUSES, describe(submitted)

    in_transit = store.ledger_account(CLASS_IN_TRANSIT)
    assert in_transit is not None, "there is no in-transit ledger account"
    assert store.entries_for(in_transit["id"]), (
        "a submitted payment did not move value through an in-transit account")

    settled = owner.post(f"/payments/{payment_id}/settle", {})
    assert settled.status_code in SUCCESS_STATUSES, describe(settled)
    assert field_of(payload_of(settled), "status") == STATUS_SETTLED

    stored = store.query("SELECT * FROM payment WHERE id = %s", (payment_id,))
    assert stored, "the payment is absent from the store"
    assert stored[0]["rail"] in RAILS, stored[0]
    assert stored[0]["status"] in STATUSES, stored[0]
    assert int(stored[0]["policy_version"]) == POLICY_VERSION, stored[0]
    assert stored[0]["currency"] == CURRENCY_STORED, stored[0]


def test_settled_ach_payment_returned_after_five_days_posts_a_reversal(
        initiator, approver, owner, store):
    account = first_operating_account(owner)
    account_id = field_of(account, "id")
    created = initiator.create_payment(payment_body(
        account_id, RECIPIENT_CLEAN_ID, "90.00", RAIL_ACH))
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    payment_id = field_of(payload_of(created), "id")
    assert approver.approve_payment(payment_id).status_code in SUCCESS_STATUSES
    assert owner.post(f"/payments/{payment_id}/submit", {}).status_code in SUCCESS_STATUSES
    assert owner.post(f"/payments/{payment_id}/settle", {}).status_code in SUCCESS_STATUSES

    returned = owner.post(f"/payments/{payment_id}/return",
                          {"return_code": "insufficient_funds",
                           "days_after_settlement": 5})
    assert returned.status_code in SUCCESS_STATUSES, describe(returned)
    assert field_of(payload_of(returned), "status") == STATUS_RETURNED, (
        f"a settled payment could not reach {STATUS_RETURNED}")

    suspense = store.ledger_account(CLASS_RETURNS_SUSPENSE)
    assert suspense is not None, "there is no returns suspense account"
    assert store.entries_for(suspense["id"]), (
        "the return posted no reversing entry against the returns suspense account")

    balance = payload_of(owner.balance(account_id))
    assert isinstance(int(field_of(balance, "current_minor")), int), balance


def test_return_codes_drive_different_recipient_behaviour(owner, store):
    recipient = store.recipient(RECIPIENT_CLEAN_ID)
    assert recipient is not None, f"seeded recipient {RECIPIENT_CLEAN_ID} is absent"
    assert recipient["name"] == RECIPIENT_CLEAN, recipient

    response = owner.post("/operations/apply-return-code",
                          {"recipient_id": RECIPIENT_CLEAN_ID,
                           "return_code": "account_closed"})
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    settle()
    after = store.recipient(RECIPIENT_CLEAN_ID)
    assert after["screening_state"] != recipient["screening_state"] or \
        str(after.get("rail_details")) != str(recipient.get("rail_details")) or \
        after.get("disabled_at") is not None, (
        "an account-closed return left the recipient exactly as it was")


def test_post_cutoff_payment_is_scheduled_to_the_next_banking_day(
        initiator, approver, owner, store):
    account = first_operating_account(owner)
    created = initiator.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_CLEAN_ID, "40.00", RAIL_ACH))
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    payment_id = field_of(payload_of(created), "id")
    approved = approver.approve_payment(payment_id)
    assert approved.status_code in SUCCESS_STATUSES, describe(approved)
    body = payload_of(approved)
    scheduled_date = field_of(body, "scheduled_date")
    assert scheduled_date, (
        f"an approved payment does not state the date it is scheduled for: {body}")

    cutoffs = store.rows("cutoff", rail=RAIL_ACH)
    assert cutoffs, "no ACH cutoff is stored"
    assert str(cutoffs[0]["local_time"]).startswith(CUTOFF_ACH), cutoffs[0]
    assert cutoffs[0]["timezone"] == CUTOFF_TIMEZONE, (
        f"a cutoff stores {cutoffs[0]['timezone']!r} rather than a timezone identifier")

    holidays = store.query(
        "SELECT * FROM banking_calendar WHERE calendar_date = %s", (HOLIDAY_ONE,))
    assert holidays, f"the banking calendar has no row for {HOLIDAY_ONE}"
    assert all(row["is_banking_day"] is False for row in holidays
               if row["rail"] in (RAIL_ACH, RAIL_WIRE)), holidays


def test_realtime_payment_sends_on_a_holiday_sunday(owner, initiator, store):
    account = first_operating_account(owner)
    created = initiator.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_CLEAN_ID, "10.00", RAIL_REALTIME))
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    payment_id = field_of(payload_of(created), "id")

    sent = owner.post(f"/payments/{payment_id}/send",
                      {"as_at": f"{HOLIDAY_ONE}T02:00:00Z"})
    assert sent.status_code in SUCCESS_STATUSES, describe(sent)
    status = field_of(payload_of(sent), "status")
    assert status in (STATUS_SETTLED, "submitted"), (
        f"a real-time payment was gated on a banking day: {status!r}")
    assert status != STATUS_SCHEDULED, (
        "a real-time payment was queued for the next banking day")

    calendar_rows = store.query(
        "SELECT * FROM banking_calendar WHERE rail = %s AND calendar_date = %s",
        (RAIL_REALTIME, HOLIDAY_ONE))
    for row in calendar_rows:
        assert row["is_banking_day"] is True, (
            "the real-time rail declares a non-banking day")


def test_wire_recall_is_recorded_as_a_request_not_a_cancellation(
        owner, initiator, approver):
    account = first_operating_account(owner)
    created = initiator.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_CLEAN_ID, "60.00", RAIL_WIRE))
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    payment_id = field_of(payload_of(created), "id")
    assert approver.approve_payment(payment_id).status_code in SUCCESS_STATUSES
    assert owner.post(f"/payments/{payment_id}/submit", {}).status_code in SUCCESS_STATUSES

    recalled = owner.recall_payment(payment_id)
    assert recalled.status_code in SUCCESS_STATUSES, describe(recalled)
    assert field_of(payload_of(recalled), "status") == STATUS_RECALL_REQUESTED, (
        "a wire recall was recorded as a cancellation")


def test_card_clearing_above_its_authorisation_posts_and_releases_the_hold(
        owner, store):
    cards = owner.cards()
    assert cards.status_code in SUCCESS_STATUSES, describe(cards)
    card_id = field_of(rows_of(cards)[0], "id")

    authorised = owner.authorise_card(card_id, {
        "amount": minor_to_decimal(CARD_AUTHORISATION_MINOR),
        "currency": CURRENCY_WIRE, "merchant_category": MERCHANT_RESTAURANT,
        "merchant_name": "Probe Diner"})
    assert authorised.status_code in SUCCESS_STATUSES, describe(authorised)
    authorisation_id = field_of(payload_of(authorised), "id")

    cleared = owner.clear_card(card_id, {
        "amount": minor_to_decimal(CARD_CLEARING_MINOR),
        "currency": CURRENCY_WIRE, "authorisation_id": authorisation_id})
    assert cleared.status_code in SUCCESS_STATUSES, (
        f"a tip taking the clearing above its authorisation was refused: "
        f"{describe(cleared)}")
    posting_id = field_of(payload_of(cleared), "posting_id")
    assert store.posting_is_balanced(posting_id), (
        f"the clearing posting {posting_id} does not balance")

    holds = store.query("SELECT * FROM hold WHERE cause_id = %s",
                        (str(authorisation_id),))
    assert holds, "the authorisation created no hold"
    assert holds[0]["released_posting_id"] is not None, (
        "the clearing did not release the hold it cleared")


def test_card_clearing_with_no_authorisation_posts_to_the_unmatched_account(
        owner, store):
    cards = owner.cards()
    card_id = field_of(rows_of(cards)[0], "id")
    cleared = owner.clear_card(card_id, {
        "amount": "12.34", "currency": CURRENCY_WIRE, "authorisation_id": None})
    assert cleared.status_code in SUCCESS_STATUSES, (
        f"a clearing with no authorisation was rejected: {describe(cleared)}")

    unmatched = store.ledger_account(CLASS_UNMATCHED)
    assert unmatched is not None, "there is no unmatched clearing account"
    assert store.entries_for(unmatched["id"]), (
        "the unmatched clearing did not post to the unmatched account")

    for row in store.rows("card"):
        assert "pan" not in {k.lower() for k in row}, (
            f"a card row carries a primary account number column: {sorted(row)}")
        assert len(str(row["last_four"])) == 4, row


def test_spend_control_decline_names_the_rule_that_fired(cardholder, owner):
    cards = owner.cards()
    card_id = field_of(rows_of(cards)[0], "id")
    control = owner.post(f"/cards/{card_id}/controls", {
        "dimension": "amount", "parameters": {"per_transaction_minor": 1000},
        "active": True})
    assert control.status_code in SUCCESS_STATUSES, describe(control)

    declined = owner.authorise_card(card_id, {
        "amount": "500.00", "currency": CURRENCY_WIRE,
        "merchant_category": MERCHANT_RESTAURANT, "merchant_name": "Probe Diner"})
    assert declined.status_code in REFUSAL_STATUSES, (
        f"a transaction above the control was authorised: {describe(declined)}")
    assert "amount" in declined.text.lower(), (
        f"the decline does not name the rule that fired: {describe(declined)}")

    foreign = cardholder.get("/payments")
    assert foreign.status_code in DENIAL_STATUSES, (
        f"a card-only member reached the payment queue: {describe(foreign)}")


def test_initiator_cannot_approve_their_own_payment(initiator, approver, owner,
                                                    store):
    account = first_operating_account(owner)
    created = initiator.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_CLEAN_ID, "75.00", RAIL_ACH))
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    payment_id = field_of(payload_of(created), "id")

    refused = initiator.approve_payment(payment_id)
    assert refused.status_code in DENIAL_STATUSES + CONFLICT_STATUSES, (
        f"the initiator approved their own payment: {describe(refused)}")
    rows = store.query("SELECT * FROM payment WHERE id = %s", (payment_id,))
    assert rows[0]["status"] == STATUS_PENDING, (
        f"the protected state changed to {rows[0]['status']!r}")

    policy_change = initiator.post("/policies", {"threshold_minor": 1,
                                                 "required_approvals": 1})
    assert policy_change.status_code in DENIAL_STATUSES, (
        f"an initiator changed approval policy: {describe(policy_change)}")


def test_editing_an_approved_payment_returns_it_to_pending(
        initiator, approver, owner, store):
    account = first_operating_account(owner)
    created = initiator.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_CLEAN_ID, "55.00", RAIL_ACH))
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    payment_id = field_of(payload_of(created), "id")
    approved = approver.approve_payment(payment_id)
    assert approved.status_code in SUCCESS_STATUSES, describe(approved)

    amended = initiator.amend_payment(payment_id, {"amount": "900.00"})
    assert amended.status_code in SUCCESS_STATUSES, describe(amended)
    assert field_of(payload_of(amended), "status") == STATUS_PENDING, (
        "an approved payment kept its approval after its amount changed")

    rows = store.query("SELECT * FROM payment WHERE id = %s", (payment_id,))
    assert rows[0]["status"] == STATUS_PENDING, rows[0]


def test_bookkeeper_cannot_move_money_at_the_api(bookkeeper, owner, store):
    account = first_operating_account(owner)
    refused = bookkeeper.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_CLEAN_ID, "5.00", RAIL_ACH))
    assert refused.status_code in DENIAL_STATUSES, (
        f"a bookkeeper created a payment: {describe(refused)}")

    recipient = bookkeeper.create_recipient({"name": "Probe Payee",
                                             "rail_details": {"rail": RAIL_ACH}})
    assert recipient.status_code in DENIAL_STATUSES, (
        f"a bookkeeper added a recipient: {describe(recipient)}")

    reading = bookkeeper.transactions()
    assert reading.status_code in SUCCESS_STATUSES, describe(reading)
    rows = rows_of(reading)
    assert rows, "the bookkeeper sees no transactions to categorise"
    posting_id = field_of(rows[0], "posting_id", "id")
    before = store.derived_balance(
        store.ledger_account("customer_deposit")["id"])
    categorised = bookkeeper.patch(f"/transactions/{posting_id}",
                                   {"category_id": None, "category": "Travel"})
    assert categorised.status_code in SUCCESS_STATUSES, describe(categorised)
    after = store.derived_balance(
        store.ledger_account("customer_deposit")["id"])
    assert before == after, "categorisation moved the ledger"


def test_cross_organisation_statement_download_is_denied(
        owner, owner_two, store, objects):
    statements = owner.statements()
    assert statements.status_code in SUCCESS_STATUSES, describe(statements)
    rows = rows_of(statements)
    assert rows, "the seeded statement is absent from the listing"
    statement_id = field_of(rows[0], "id")

    own = owner.statement_content(statement_id)
    assert own.status_code in SUCCESS_STATUSES, describe(own)

    across = owner_two.statement_content(statement_id)
    assert across.status_code in DENIAL_STATUSES, (
        f"another organisation downloaded the statement: {describe(across)}")

    anonymous_read = httpx.get(
        f"{appclient.api_base()}/statements/{statement_id}/content", timeout=30.0)
    assert anonymous_read.status_code in DENIAL_STATUSES, (
        f"a signed-out caller downloaded the statement: {describe(anonymous_read)}")

    stored = store.statement(STATEMENT_PERIOD)
    assert stored is not None, f"no statement row for {STATEMENT_PERIOD}"
    assert objects.exists(stored["object_key"]), (
        f"the statement bytes are not an object at {stored['object_key']!r}")


def test_unauthenticated_product_and_editorial_routes_are_denied(site_base):
    for route in PRODUCT_ROUTES + STUDIO_ROUTES:
        response = httpx.get(f"{site_base}{route}", timeout=30.0,
                             follow_redirects=False)
        assert response.status_code in DENIAL_STATUSES + REDIRECT_STATUSES, (
            f"{route} served a product surface to a signed-out caller: "
            f"{describe(response)}")
        if response.status_code in REDIRECT_STATUSES:
            assert "/login" in response.headers.get("location", ""), (
                f"{route} redirects somewhere other than the sign-in page")

    wrong = httpx.post(f"{appclient.api_base()}/auth/login",
                       json={"email": OWNER_EMAIL, "password": "not-the-password"},
                       timeout=30.0)
    assert wrong.status_code in DENIAL_STATUSES + REFUSAL_STATUSES, describe(wrong)


def test_step_up_grant_is_scoped_to_one_action(owner):
    granted = owner.step_up("add_recipient")
    assert granted.status_code in SUCCESS_STATUSES, describe(granted)
    body = payload_of(granted)
    assert field_of(body, "action") == "add_recipient", body
    assert field_of(body, "expires_at"), "a step-up grant carries no expiry"
    assert set(STEP_UP_ACTIONS), "the step-up action set is empty"

    account = first_operating_account(owner)
    large = owner.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_CLEAN_ID,
        minor_to_decimal(POLICY_THRESHOLD_MINOR + 100), RAIL_ACH))
    assert large.status_code in REFUSAL_STATUSES + DENIAL_STATUSES, (
        f"a payment above the step-up threshold was accepted on a grant for a "
        f"different action: {describe(large)}")


def test_sanctions_list_update_blocks_a_newly_matching_recipient(owner, store):
    versions = {row["version"] for row in store.rows("sanctions_list_version")}
    assert SANCTIONS_VERSION_CLEAN in versions, versions
    assert SANCTIONS_VERSION_LISTED in versions, versions

    recipient = store.recipient(RECIPIENT_LISTED_ID)
    assert recipient is not None, f"{RECIPIENT_LISTED_ID} is absent from the store"
    assert recipient["name"] == RECIPIENT_LISTED, recipient

    loaded = owner.post("/operations/load-sanctions-version",
                        {"version": SANCTIONS_VERSION_LISTED})
    assert loaded.status_code in SUCCESS_STATUSES, describe(loaded)
    settle()

    after = store.recipient(RECIPIENT_LISTED_ID)
    assert after["screening_state"] in ("blocked", "under_review", "match"), (
        f"a newly listed recipient is still {after['screening_state']!r}")

    results = store.query(
        "SELECT * FROM screening_result WHERE subject_id = %s",
        (str(after["id"]),))
    assert results, "the list update raised no screening result"
    assert any(row["sanctions_list_version_id"] is not None for row in results), (
        "a screening decision names no list version")


def test_payment_to_a_listed_counterparty_is_blocked_before_submission(
        initiator, owner):
    account = first_operating_account(owner)
    refused = initiator.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_LISTED_ID, "20.00", RAIL_ACH))
    assert refused.status_code in REFUSAL_STATUSES, (
        f"a payment to a listed counterparty was accepted: {describe(refused)}")


def test_erasure_request_restricts_access_and_preserves_the_ledger(owner, store):
    before_entries = store.count("entry")
    before_audit = store.count("audit_entry")
    requested = owner.post("/operations/erasure", {"subject_email": OWNER_EMAIL})
    assert requested.status_code in SUCCESS_STATUSES, describe(requested)
    settle()
    assert store.count("entry") >= before_entries, (
        "an erasure request destroyed ledger entries")
    assert store.count("audit_entry") >= before_audit, (
        "an erasure request destroyed audit entries")


def test_statement_object_regenerates_byte_identical_after_a_correction(
        owner, store, objects):
    stored = store.statement(STATEMENT_PERIOD)
    assert stored is not None, f"no statement row for {STATEMENT_PERIOD}"
    digest_before = stored["digest"]
    key_before = stored["object_key"]

    correction = owner.post("/postings", {
        "ledger_account_id": store.ledger_account("customer_deposit")["id"],
        "amount": "1.00", "currency": CURRENCY_WIRE, "cause_kind": "correction",
        "cause_id": f"probe-{unique_suffix()}",
        "effective_date": f"{STATEMENT_PERIOD}-15"})
    assert correction.status_code in SUCCESS_STATUSES, describe(correction)
    settle()

    after = store.statement(STATEMENT_PERIOD)
    assert after["digest"] == digest_before, (
        "a back-dated correction changed the issued statement")
    assert after["object_key"] == key_before, (
        "the issued statement was written to a new object")
    assert objects.exists(key_before), (
        f"the issued statement object {key_before!r} no longer exists")


def test_reconciliation_break_is_raised_with_no_automatic_posting(owner, store):
    before = store.count("posting")
    loaded = owner.post("/operations/load-partner-file",
                        {"run_date": RECONCILIATION_RUN_DATE,
                         "partner_bank": PARTNER_BANK_ONE})
    assert loaded.status_code in SUCCESS_STATUSES, describe(loaded)
    settle()

    run = owner.reconciliation(RECONCILIATION_RUN_DATE)
    assert run.status_code in SUCCESS_STATUSES, describe(run)
    body = payload_of(run)
    breaks = field_of(body, "breaks")
    assert breaks, "the injected discrepancy raised no break"
    for row in breaks:
        assert field_of(row, "kind") in BREAK_KINDS, row
        assert field_of(row, "opened_at"), row
    assert store.count("posting") == before, (
        "reconciliation made an automatic posting to match the bank")


def test_audit_chain_names_the_agent_and_its_authorising_human(owner, store):
    created = owner.create_token({"kind": "agent", "scopes": ["payments:write"],
                                  "velocity_per_transaction_minor": 100000,
                                  "velocity_per_day_minor": 500000,
                                  "velocity_per_counterparty_minor": 100000})
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    body = payload_of(created)
    token_id = field_of(body, "id")
    secret = field_of(body, "token", "secret")

    agent = Session(secret, "agent")
    account = first_operating_account(owner)
    payment = agent.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_CLEAN_ID, "1.00", RAIL_ACH))
    assert payment.status_code in SUCCESS_STATUSES, describe(payment)
    assert field_of(payload_of(payment), "status") == STATUS_PENDING, (
        "an agent completed a payment without a human approval")

    organisation = store.organisation(ORG_ONE_SLUG)
    chain = store.audit_chain(organisation["id"])
    assert chain, "the agent action left no audit entry"
    agent_rows = [row for row in chain if row["actor_agent_id"] is not None]
    assert agent_rows, "no audit entry names the agent that acted"
    assert all(row["actor_account_id"] is not None for row in agent_rows), (
        "an agent action names no authorising human")
    previous = None
    for row in chain:
        assert row["hash"], f"audit entry {row['id']} carries no fingerprint"
        if previous is not None:
            assert row["prev_hash"] == previous["hash"], (
                f"the audit chain breaks at entry {row['id']}")
        previous = row

    revoked = owner.revoke_token(token_id)
    assert revoked.status_code in SUCCESS_STATUSES, describe(revoked)
    still_signed_in = owner.accounts()
    assert still_signed_in.status_code in SUCCESS_STATUSES, (
        "revoking an agent disturbed the authorising human's own access")


def test_fifty_concurrent_requests_on_one_idempotency_key_create_one_payment(
        initiator, owner, store):
    account = first_operating_account(owner)
    account_id = field_of(account, "id")
    key = idempotency_key()
    body = payment_body(account_id, RECIPIENT_CLEAN_ID, "33.00", RAIL_ACH)

    def one_call(_: int) -> httpx.Response:
        session = Session(initiator.token, initiator.email)
        return session.request("POST", "/payments", body=body,
                               headers={IDEMPOTENCY_HEADER: key})

    with ThreadPoolExecutor(max_workers=25) as pool:
        responses = list(pool.map(one_call, range(CONCURRENT_IDEMPOTENT_CALLS)))

    accepted = [r for r in responses if r.status_code in SUCCESS_STATUSES]
    assert len(accepted) == CONCURRENT_IDEMPOTENT_CALLS, (
        f"{len(accepted)} of {CONCURRENT_IDEMPOTENT_CALLS} replays were served: "
        f"{describe(responses[0])}")
    bodies = {r.text for r in accepted}
    assert len(bodies) == 1, (
        f"the replays returned {len(bodies)} different response bodies")

    rows = store.query(
        "SELECT * FROM payment WHERE idempotency_key = %s", (key,))
    assert len(rows) == 1, (
        f"one idempotency key produced {len(rows)} payment rows")


def test_same_idempotency_key_with_a_changed_amount_is_refused(
        initiator, owner, store):
    account = first_operating_account(owner)
    account_id = field_of(account, "id")
    key = idempotency_key()
    first = initiator.create_payment(
        payment_body(account_id, RECIPIENT_CLEAN_ID, "21.00", RAIL_ACH), key=key)
    assert first.status_code in SUCCESS_STATUSES, describe(first)

    changed = initiator.create_payment(
        payment_body(account_id, RECIPIENT_CLEAN_ID, "22.00", RAIL_ACH), key=key)
    assert changed.status_code in REFUSAL_STATUSES, (
        f"a reused key carrying a different amount was served: {describe(changed)}")
    rows = store.query("SELECT * FROM payment WHERE idempotency_key = %s", (key,))
    assert len(rows) == 1, f"the refused replay wrote {len(rows)} payment rows"


def test_out_of_order_webhook_delivery_leaves_the_correct_final_state(
        owner, initiator, approver, store):
    account = first_operating_account(owner)
    created = initiator.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_CLEAN_ID, "44.00", RAIL_ACH))
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    payment_id = field_of(payload_of(created), "id")
    assert approver.approve_payment(payment_id).status_code in SUCCESS_STATUSES
    assert owner.post(f"/payments/{payment_id}/submit", {}).status_code in SUCCESS_STATUSES

    deliveries = [
        {"type": "payment.settled", "sequence": 1, "state": STATUS_SETTLED},
        {"type": "payment.returned", "sequence": 2, "state": STATUS_RETURNED},
        {"type": "payment.settled", "sequence": 1, "state": STATUS_SETTLED},
        {"type": "payment.returned", "sequence": 2, "state": STATUS_RETURNED},
    ]
    for delivery in deliveries:
        response = owner.post("/hooks/partner-bank", {
            "payment_id": payment_id, "occurred_at": "2026-09-15T10:00:00Z",
            **delivery})
        assert response.status_code in SUCCESS_STATUSES, describe(response)
    settle()

    rows = store.query("SELECT * FROM payment WHERE id = %s", (payment_id,))
    assert rows[0]["status"] == STATUS_RETURNED, (
        f"out-of-order delivery left the payment {rows[0]['status']!r}")

    events = owner.events(resource_kind="payment")
    assert events.status_code in SUCCESS_STATUSES, describe(events)
    sequences = [int(field_of(row, "sequence")) for row in rows_of(events)]
    assert sequences == sorted(sequences), "the event log is not ordered"


def test_payment_rate_limit_is_lower_than_the_read_limit(owner):
    reads = owner.get("/limits")
    assert reads.status_code in SUCCESS_STATUSES, describe(reads)
    body = payload_of(reads)
    read_limit = int(field_of(body, "read_per_minute"))
    payment_limit = int(field_of(body, "payment_per_minute"))
    assert read_limit == READ_LIMIT_PER_MINUTE, body
    assert payment_limit == PAYMENT_LIMIT_PER_MINUTE, body
    assert payment_limit < read_limit, (
        "payment-initiating calls are not limited below reads")


def test_money_travels_as_a_decimal_string_with_its_currency(owner, initiator):
    account = first_operating_account(owner)
    created = initiator.create_payment(payment_body(
        field_of(account, "id"), RECIPIENT_CLEAN_ID, "4850.00", RAIL_ACH))
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    body = payload_of(created)
    amount = field_of(body, "amount")
    assert isinstance(amount, str), (
        f"an amount crossed the wire as {type(amount).__name__}")
    assert amount == "4850.00", body
    assert field_of(body, "currency") == CURRENCY_WIRE, body


def test_logs_carry_a_request_identifier_and_no_amount(owner, app_base):
    failed = owner.get("/payments/no-such-payment")
    assert failed.status_code in REFUSAL_STATUSES, describe(failed)
    body = failed.json()
    assert CORRELATION_FIELD in body, (
        f"an error body carries no {CORRELATION_FIELD}: {describe(failed)}")
    assert str(body[CORRELATION_FIELD]).strip(), body


def test_developer_reference_resources_match_the_served_api(owner):
    for path in ("/accounts", "/payments", "/recipients", "/cards",
                 "/statements", "/transactions"):
        response = owner.get(path)
        assert response.status_code in SUCCESS_STATUSES, describe(response)
        rows_of(response)


def test_rows_live_in_postgres_and_survive_a_restart_of_the_process(store, owner):
    for table in ("organisation", "bank_account", "ledger_account", "posting",
                  "entry", "payment", "fee", "footnote", "page"):
        assert store.count(table) > 0, (
            f"{table} holds no rows in PostgreSQL")
    response = owner.accounts()
    assert response.status_code in SUCCESS_STATUSES, describe(response)


def test_page_home_leads_with_one_primary_action(page, site_base):
    page.goto(f"{site_base}/", wait_until="load")
    content = page.content()
    assert HERO_HEADLINE in content, "the hero headline is absent"
    assert HERO_FIELD in content, "the hero capture field label is absent"
    assert HERO_PRIMARY in content, "the hero primary action is absent"
    assert HERO_SECONDARY in content, "the quieter alternative is absent"
    assert FEATURE_HEADING in content, "the feature heading is absent"
    assert ANNOUNCEMENT in content, "the announcement copy is absent"
    assert WORDMARK in content, "the letterspaced wordmark is absent"
    for item in NAV_ITEMS:
        assert item in content, f"navigation item {item} is absent"
    assert APPLY_MINUTES in content, "the stated application duration is absent"

    primary = page.locator("[data-primary-action]")
    assert primary.count() == 1, (
        f"the home page carries {primary.count()} primary actions, expected one")


def test_page_body_text_meets_the_contrast_bar(page, site_base):
    page.goto(f"{site_base}/", wait_until="load")
    headings = page.locator("h1")
    assert headings.count() == 1, (
        f"the home route carries {headings.count()} first-rank headings")

    sample = page.locator("main p").first
    colours = sample.evaluate(
        "node => { const s = getComputedStyle(node);"
        " return [s.color, getComputedStyle(document.body).backgroundColor]; }")
    ratio = contrast_ratio(parse_rgb(colours[0]), parse_rgb(colours[1]))
    assert ratio >= CONTRAST_BAR, (
        f"body text contrast is {ratio:.2f}, below the {CONTRAST_BAR} bar")

    assert SKIP_LINK in page.content(), (
        "the skip link is absent from the document")


def test_page_narrow_viewport_has_no_sideways_overflow(page, site_base):
    page.set_viewport_size({"width": NARROW_VIEWPORT_WIDTH, "height": 780})
    page.goto(f"{site_base}/", wait_until="load")
    overflow = page.evaluate(
        "() => document.documentElement.scrollWidth - "
        "document.documentElement.clientWidth")
    assert overflow <= 1, (
        f"the home page overflows sideways by {overflow} at a narrow viewport")
    assert RESPONSIVE_TIERS == 6, "the brief pins six ascending tiers"

    navigation = page.locator("nav a, nav button")
    assert navigation.count() > 0, "no navigation target is reachable when narrow"


def test_page_content_images_carry_alternative_text(page, site_base):
    page.goto(f"{site_base}/", wait_until="load")
    missing = page.evaluate(
        "() => Array.from(document.images)"
        ".filter(i => !i.hasAttribute('alt')).map(i => i.currentSrc)")
    assert missing == [], f"images carry no alternative text: {missing}"

    unlabelled = page.evaluate(
        "() => Array.from(document.querySelectorAll('button, a'))"
        ".filter(e => !e.textContent.trim() && !e.getAttribute('aria-label'))"
        ".map(e => e.outerHTML.slice(0, 80))")
    assert unlabelled == [], f"icon-only controls carry no name: {unlabelled}"


def test_page_keyboard_focus_ring_is_visible_on_every_control(page, site_base):
    page.goto(f"{site_base}/", wait_until="load")
    page.keyboard.press("Tab")
    outline = page.evaluate(
        "() => { const e = document.activeElement;"
        " const s = getComputedStyle(e);"
        " return [e.tagName, s.outlineStyle, s.outlineWidth, s.boxShadow]; }")
    assert outline[0] != "BODY", "the first Tab reached no focusable element"
    assert outline[1] != "none" or outline[3] != "none", (
        f"the focused control carries no visible focus ring: {outline}")

    legal = page.context.new_page()
    legal.goto(f"{site_base}/legal/terms", wait_until="load")
    animated = legal.evaluate("() => document.getAnimations().length")
    assert animated == 0, (
        f"the legal pages run {animated} animations, expected stillness")
    legal.close()


def test_page_money_columns_use_tabular_figures(page, site_base):
    page.goto(f"{site_base}/pricing", wait_until="load")
    amounts = page.locator("[data-amount]")
    assert amounts.count() > 0, "no amount is marked on the pricing page"
    settings = amounts.first.evaluate(
        "node => getComputedStyle(node).fontVariantNumeric")
    assert "tabular-nums" in settings, (
        f"amounts are not set with tabular figures: {settings!r}")

    fetched = page.evaluate(
        "() => performance.getEntriesByType('resource').map(r => r.name)")
    binaries = [name for name in fetched
                if name.lower().split("?", 1)[0].endswith(BINARY_ASSET_SUFFIXES)]
    assert binaries == [], (
        f"the build fetched binary assets at run time: {binaries}")
