from __future__ import annotations

import httpx
import pytest

import appclient
from conftest import (
    CASE_COUNT,
    NARROW_VIEWPORT,
    CREATED,
    DENIED,
    DENIED_OR_MISSING,
    ENGINEER2_EMAIL,
    ENGINEER_EMAIL,
    ENGLISH_PREFIX,
    FAMILY_CODES,
    FAMILY_VARIANTS,
    PUBLIC_ROUTES,
    REFUSED,
    REQUEST_TABLE,
    SEEDED_PASSWORD,
    SEEDED_REQUEST_REF,
    SEEDED_REQUEST_STATUS,
    SEEDED_WELL_NUMBER,
    SUBSCRIBER_TABLE,
    enquiry_payload,
    fetch,
    find_request_ref,
    probe_email,
    request_count,
    request_rows,
    submit_enquiry,
    wait_for,
)


def _text(value) -> str:
    return "" if value is None else str(value)


def _walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


def _flat(node) -> str:
    return str(node)




def test_health_endpoint_returns_ok(app_url):
    r = httpx.get(f"{app_url}/api/health", timeout=appclient.TIMEOUT)
    assert r.status_code == 200, (
        f"GET /api/health returned {r.status_code}, expected 200 once the app is "
        f"ready: {r.text[:300]}"
    )


def test_seeded_engineer_can_log_in():
    token = appclient.login(ENGINEER_EMAIL, SEEDED_PASSWORD)
    assert token, (
        f"login as the seeded engineer {ENGINEER_EMAIL} with the seeded password "
        f"returned no bearer token"
    )


def test_products_index_lists_the_five_families(anon_client):
    r = anon_client.get("/products")
    assert r.status_code == 200, (
        f"GET /api/products returned {r.status_code}, expected the public catalogue: "
        f"{r.text[:300]}"
    )
    body = _flat(r.json())
    missing = [c for c in FAMILY_CODES if c not in body]
    assert not missing, (
        f"the products index is missing family code(s) {missing}; the brief pins all "
        f"five of {list(FAMILY_CODES)}"
    )


def test_every_variant_appears_in_its_family_spec_table(anon_client):
    slugs = {"FRS": "frs", "SVR": "svr", "TRANSFER X1": "x1",
             "TRANSFER X3": "x3", "TRANSFER X6": "x6"}
    for code, variants in FAMILY_VARIANTS.items():
        r = anon_client.get(f"/products/{slugs[code]}")
        assert r.status_code == 200, (
            f"GET /api/products/{slugs[code]} returned {r.status_code}, expected the "
            f"{code} detail record: {r.text[:300]}"
        )
        body = _flat(r.json())
        missing = [v for v in variants if v not in body]
        assert not missing, (
            f"the {code} detail record does not carry size variant(s) {missing} in its "
            f"specification table; every declared variant is a column of its own family"
        )


def test_unmeasured_spec_cell_prints_a_dash(anon_client):
    r = anon_client.get("/products/frs")
    assert r.status_code == 200, (
        f"GET /api/products/frs returned {r.status_code}: {r.text[:300]}"
    )
    body = _flat(r.json())
    assert "-" in body, (
        "the FRS specification table carries no dash; an unmeasured cell prints a "
        "single dash character rather than a blank or a zero"
    )
    cells = []
    for node in _walk(r.json()):
        for key, value in node.items():
            if isinstance(value, str) and value.strip() == "":
                cells.append(key)
    assert not cells, (
        f"the FRS detail record carries empty specification cell(s) under key(s) "
        f"{sorted(set(cells))}; an unmeasured value is the dash character, never blank"
    )


def test_cases_index_lists_ten_cases_newest_first(anon_client):
    r = anon_client.get("/cases")
    assert r.status_code == 200, (
        f"GET /api/cases returned {r.status_code}, expected the evidence library: "
        f"{r.text[:300]}"
    )
    cases = r.json()
    assert isinstance(cases, list), (
        f"GET /api/cases returned {type(cases).__name__}, expected a top level JSON "
        f"array: {r.text[:300]}"
    )
    assert len(cases) == CASE_COUNT, (
        f"GET /api/cases returned {len(cases)} case(s), expected exactly {CASE_COUNT}"
    )
    months = []
    for case in cases:
        for key in ("run_month", "runMonth", "date"):
            if key in case:
                months.append(_text(case[key]))
                break
    assert len(months) == CASE_COUNT, (
        f"only {len(months)} of {CASE_COUNT} cases carry a run month; the index is "
        f"ordered by that value"
    )
    assert months == sorted(months, reverse=True) or months[0] != months[-1], (
        f"the evidence index is not ordered newest first; the run months came back "
        f"as {months}"
    )


def test_case_detail_is_addressed_by_well_number(anon_client):
    r = anon_client.get(f"/cases/{SEEDED_WELL_NUMBER}")
    assert r.status_code == 200, (
        f"GET /api/cases/{SEEDED_WELL_NUMBER} returned {r.status_code}; a case is "
        f"addressed by its well number rather than by a slug: {r.text[:300]}"
    )
    assert SEEDED_WELL_NUMBER in _flat(r.json()), (
        f"the case served at /api/cases/{SEEDED_WELL_NUMBER} does not carry that well "
        f"number in its record"
    )


def test_case_names_the_product_family_that_ran(anon_client):
    r = anon_client.get(f"/cases/{SEEDED_WELL_NUMBER}")
    assert r.status_code == 200, (
        f"GET /api/cases/{SEEDED_WELL_NUMBER} returned {r.status_code}: {r.text[:300]}"
    )
    body = _flat(r.json())
    assert any(code in body for code in FAMILY_CODES), (
        f"case {SEEDED_WELL_NUMBER} names no product family; a case names the product "
        f"that ran in it, and the catalogue and the library cross-link both ways"
    )


def test_product_names_the_cases_that_ran_it(anon_client):
    r = anon_client.get("/products/frs")
    assert r.status_code == 200, (
        f"GET /api/products/frs returned {r.status_code}: {r.text[:300]}"
    )
    body = _flat(r.json())
    assert SEEDED_WELL_NUMBER in body, (
        f"the FRS detail record names no case; a product route names the cases that "
        f"ran it, and well {SEEDED_WELL_NUMBER} ran FRS"
    )


def test_engineer_reads_the_request_queue(engineer_client):
    r = engineer_client.get("/requests")
    assert r.status_code == 200, (
        f"GET /api/requests as a signed-in engineer returned {r.status_code}, expected "
        f"the queue: {r.text[:300]}"
    )
    assert isinstance(r.json(), list), (
        f"GET /api/requests returned {type(r.json()).__name__}, expected a top level "
        f"JSON array"
    )


def test_engineer_advances_the_request_status(engineer_client, backend):
    created = submit_enquiry(engineer_client, enquiry_payload())
    assert created.status_code in CREATED, (
        f"POST /api/enquiry returned {created.status_code}: {created.text[:300]}"
    )
    ref = find_request_ref(created.json())
    r = engineer_client.patch(f"/requests/{ref}", json={"status": "modelling"})
    assert r.status_code in (200, 202), (
        f"PATCH /api/requests/{ref} to status modelling returned {r.status_code}; the "
        f"status moves forward one step at a time from new: {r.text[:300]}"
    )
    row = wait_for(lambda: (request_rows(backend, request_ref=ref) or [None])[0],
                   f"the stored row for {ref}")
    assert _text(row.get("status")) == "modelling", (
        f"request {ref} reads status {row.get('status')!r} in {REQUEST_TABLE} after "
        f"being advanced, expected 'modelling'"
    )


def test_engineer_assigns_a_request_to_an_engineer(engineer_client, backend):
    created = submit_enquiry(engineer_client, enquiry_payload())
    assert created.status_code in CREATED, (
        f"POST /api/enquiry returned {created.status_code}: {created.text[:300]}"
    )
    ref = find_request_ref(created.json())
    r = engineer_client.patch(f"/requests/{ref}", json={"assigned_to": ENGINEER2_EMAIL})
    assert r.status_code in (200, 202), (
        f"PATCH /api/requests/{ref} assigning {ENGINEER2_EMAIL} returned "
        f"{r.status_code}: {r.text[:300]}"
    )
    read = engineer_client.get(f"/requests/{ref}")
    assert read.status_code == 200, (
        f"GET /api/requests/{ref} returned {read.status_code} after the assignment: "
        f"{read.text[:300]}"
    )
    assert ENGINEER2_EMAIL in _flat(read.json()), (
        f"request {ref} does not name {ENGINEER2_EMAIL} after being assigned to that "
        f"engineer"
    )


def test_seeded_request_exists_at_status_new(backend):
    rows = request_rows(backend, request_ref=SEEDED_REQUEST_REF)
    assert rows, (
        f"no row in {REQUEST_TABLE} carries request_ref {SEEDED_REQUEST_REF}; the "
        f"seeded request exists so the queue is never empty on a fresh install"
    )
    assert _text(rows[0].get("status")) == SEEDED_REQUEST_STATUS, (
        f"seeded request {SEEDED_REQUEST_REF} reads status "
        f"{rows[0].get('status')!r}, expected {SEEDED_REQUEST_STATUS!r}"
    )


def test_locale_switch_holds_the_path(app_url):
    r_en = fetch(app_url, "/en/products/x3")
    assert r_en.status_code == 200, (
        f"GET /en/products/x3 returned {r_en.status_code}, expected the English "
        f"TRANSFER X3 route"
    )
    r_default = fetch(app_url, "/products/x3")
    assert r_default.status_code == 200, (
        f"GET /products/x3 returned {r_default.status_code}; the locale prefix is the "
        f"only difference between the two route trees, so the same path resolves "
        f"under the unprefixed default locale"
    )


def test_list_endpoints_return_top_level_arrays(anon_client):
    for route in ("/products", "/cases"):
        r = anon_client.get(route)
        assert r.status_code == 200, (
            f"GET /api{route} returned {r.status_code}: {r.text[:300]}"
        )
        assert isinstance(r.json(), list), (
            f"GET /api{route} returned {type(r.json()).__name__}, expected a top "
            f"level JSON array"
        )




def test_enquiry_creates_one_modelling_request(anon_client, backend):
    payload = enquiry_payload()
    before = request_count(backend, email=payload["email"])
    r = submit_enquiry(anon_client, payload)
    assert r.status_code in CREATED, (
        f"POST /api/enquiry with consent returned {r.status_code}, expected the "
        f"request to be created: {r.text[:300]}"
    )
    after = wait_for(
        lambda: request_count(backend, email=payload["email"]) or None,
        f"a row in {REQUEST_TABLE} for {payload['email']}")
    assert after == before + 1, (
        f"{REQUEST_TABLE} holds {after} row(s) for {payload['email']} after one "
        f"submission, expected {before + 1}"
    )


def test_stored_request_matches_every_submitted_field(anon_client, backend):
    payload = enquiry_payload()
    r = submit_enquiry(anon_client, payload)
    assert r.status_code in CREATED, (
        f"POST /api/enquiry returned {r.status_code}: {r.text[:300]}"
    )
    row = wait_for(lambda: (request_rows(backend, email=payload["email"]) or [None])[0],
                   f"the stored row for {payload['email']}")
    stored = {k: _text(v) for k, v in row.items()}
    flat = " | ".join(stored.values())
    for field in ("firstName", "lastName", "email", "phone", "message"):
        assert _text(payload[field]) in flat, (
            f"the stored request does not carry the submitted {field} "
            f"{payload[field]!r}; the persisted row must match what the visitor's "
            f"form displayed. Stored row: {stored}"
        )


def test_stored_request_records_the_source_route(anon_client, backend):
    payload = enquiry_payload(source_route="/en/cases/22061")
    r = submit_enquiry(anon_client, payload)
    assert r.status_code in CREATED, (
        f"POST /api/enquiry returned {r.status_code}: {r.text[:300]}"
    )
    row = wait_for(lambda: (request_rows(backend, email=payload["email"]) or [None])[0],
                   f"the stored row for {payload['email']}")
    flat = " | ".join(_text(v) for v in row.values())
    assert payload["sourceRoute"] in flat, (
        f"the stored request does not record sourceRoute "
        f"{payload['sourceRoute']!r}; the same band sits at the foot of nine routes "
        f"and the record says which one it came from. Stored row: {row}"
    )


def test_request_survives_a_reload_unchanged(anon_client, engineer_client, backend):
    payload = enquiry_payload()
    r = submit_enquiry(anon_client, payload)
    assert r.status_code in CREATED, (
        f"POST /api/enquiry returned {r.status_code}: {r.text[:300]}"
    )
    ref = find_request_ref(r.json())
    first = wait_for(lambda: (request_rows(backend, request_ref=ref) or [None])[0],
                     f"the stored row for {ref}")
    read = engineer_client.get(f"/requests/{ref}")
    assert read.status_code == 200, (
        f"GET /api/requests/{ref} returned {read.status_code} on a fresh read: "
        f"{read.text[:300]}"
    )
    served = _flat(read.json())
    for field in ("firstName", "lastName", "email"):
        assert _text(payload[field]) in served, (
            f"request {ref} no longer serves the submitted {field} "
            f"{payload[field]!r} when read back; the stored row was {first}"
        )


def test_duplicate_enquiry_creates_no_second_request(anon_client, backend):
    payload = enquiry_payload()
    first = submit_enquiry(anon_client, payload)
    assert first.status_code in CREATED, (
        f"the first POST /api/enquiry returned {first.status_code}: "
        f"{first.text[:300]}"
    )
    first_ref = find_request_ref(first.json())
    second = submit_enquiry(anon_client, payload)
    assert second.status_code in CREATED + REFUSED, (
        f"the repeated POST /api/enquiry returned {second.status_code}; an immediate "
        f"resubmission either reports the first reference or is refused: "
        f"{second.text[:300]}"
    )
    count = wait_for(lambda: request_count(backend, email=payload["email"]) or None,
                     f"a row in {REQUEST_TABLE} for {payload['email']}")
    assert count == 1, (
        f"{REQUEST_TABLE} holds {count} rows for {payload['email']} after the same "
        f"enquiry was sent twice in immediate succession, expected exactly 1"
    )
    if second.status_code in CREATED:
        assert find_request_ref(second.json()) == first_ref, (
            f"the repeated submission reported a different reference "
            f"{find_request_ref(second.json())!r} rather than the first one "
            f"{first_ref!r}"
        )


def test_duplicate_subscribe_creates_no_second_subscriber(anon_client, backend):
    email = probe_email()
    body = {"email": email, "consent": True, "locale": "en"}
    first = anon_client.post("/subscribe", json=body)
    assert first.status_code in CREATED, (
        f"the first POST /api/subscribe returned {first.status_code}: "
        f"{first.text[:300]}"
    )
    second = anon_client.post("/subscribe", json=body)
    assert second.status_code in CREATED + REFUSED, (
        f"the repeated POST /api/subscribe returned {second.status_code}: "
        f"{second.text[:300]}"
    )
    count = wait_for(lambda: backend.count(SUBSCRIBER_TABLE, email=email) or None,
                     f"a row in {SUBSCRIBER_TABLE} for {email}")
    assert count == 1, (
        f"{SUBSCRIBER_TABLE} holds {count} rows for {email} after the same address "
        f"subscribed twice, expected exactly 1"
    )


def test_every_case_metric_carries_a_provenance(anon_client):
    index = anon_client.get("/cases")
    assert index.status_code == 200, (
        f"GET /api/cases returned {index.status_code}: {index.text[:300]}"
    )
    bare = []
    for case in index.json():
        key = None
        for candidate in ("well_number", "wellNumber"):
            if candidate in case:
                key = _text(case[candidate])
                break
        assert key, f"a case on the index carries no well number: {str(case)[:200]}"
        detail = anon_client.get(f"/cases/{key}")
        assert detail.status_code == 200, (
            f"GET /api/cases/{key} returned {detail.status_code}: "
            f"{detail.text[:300]}"
        )
        for node in _walk(detail.json()):
            if "delta" in node or "before" in node or "after" in node:
                prov = node.get("provenance")
                if not _text(prov).strip():
                    bare.append((key, node))
    assert not bare, (
        f"{len(bare)} published case metric(s) carry no provenance, first at well "
        f"{bare[0][0]}: {str(bare[0][1])[:200]}. Provenance is required on every "
        f"figure and has no default"
    )




def test_anonymous_cannot_read_the_request_queue(anon_client):
    r = anon_client.get("/requests")
    assert r.status_code in DENIED, (
        f"GET /api/requests with no token returned {r.status_code}, expected the "
        f"server to deny an anonymous read of the modelling request queue. Hiding "
        f"the link in the interface is not authorization: {r.text[:300]}"
    )


def test_anonymous_cannot_change_a_request(anon_client):
    r = anon_client.patch(f"/requests/{SEEDED_REQUEST_REF}",
                          json={"status": "declined"})
    assert r.status_code in DENIED_OR_MISSING, (
        f"PATCH /api/requests/{SEEDED_REQUEST_REF} with no token returned "
        f"{r.status_code}, expected the server to deny an anonymous change: "
        f"{r.text[:300]}"
    )


def test_denied_change_leaves_the_request_row_unchanged(anon_client, backend):
    before = request_rows(backend, request_ref=SEEDED_REQUEST_REF)
    assert before, (
        f"no row in {REQUEST_TABLE} carries request_ref {SEEDED_REQUEST_REF} before "
        f"the denied attempt"
    )
    anon_client.patch(f"/requests/{SEEDED_REQUEST_REF}", json={"status": "declined"})
    after = request_rows(backend, request_ref=SEEDED_REQUEST_REF)
    assert after, (
        f"row {SEEDED_REQUEST_REF} is gone from {REQUEST_TABLE} after an anonymous "
        f"change was attempted"
    )
    assert _text(after[0].get("status")) == _text(before[0].get("status")), (
        f"request {SEEDED_REQUEST_REF} moved from status "
        f"{before[0].get('status')!r} to {after[0].get('status')!r} after a denied "
        f"anonymous change; a denied call leaves the protected state unchanged"
    )


def test_engineer_cannot_delete_a_request(engineer_client, backend):
    r = engineer_client.delete(f"/requests/{SEEDED_REQUEST_REF}")
    assert r.status_code not in (200, 202, 204), (
        f"DELETE /api/requests/{SEEDED_REQUEST_REF} returned {r.status_code}; no "
        f"engineer can remove a modelling request: {r.text[:300]}"
    )
    rows = request_rows(backend, request_ref=SEEDED_REQUEST_REF)
    assert rows, (
        f"row {SEEDED_REQUEST_REF} is gone from {REQUEST_TABLE} after a deletion was "
        f"attempted; no request row is ever removed"
    )


def test_login_with_wrong_password_is_rejected():
    r = httpx.post(
        f"{appclient.api_base()}/auth/login",
        json={"email": ENGINEER_EMAIL, "password": "not-the-seeded-password"},
        timeout=appclient.TIMEOUT,
    )
    assert r.status_code in DENIED + REFUSED, (
        f"login for {ENGINEER_EMAIL} with a wrong password returned {r.status_code}, "
        f"expected the attempt to be refused: {r.text[:300]}"
    )
    body = r.text
    assert "access_token" not in body, (
        f"a login with the wrong password handed back a token: {body[:300]}"
    )




def test_enquiry_without_consent_is_rejected(anon_client):
    payload = enquiry_payload(consent=False)
    r = submit_enquiry(anon_client, payload)
    assert r.status_code in REFUSED, (
        f"POST /api/enquiry with consent false returned {r.status_code}, expected the "
        f"submission to be refused as a client error with a reason: {r.text[:300]}"
    )


def test_rejected_enquiry_writes_no_row(anon_client, backend):
    payload = enquiry_payload(consent=False)
    r = submit_enquiry(anon_client, payload)
    assert r.status_code in REFUSED, (
        f"POST /api/enquiry with consent false returned {r.status_code}, expected a "
        f"refusal: {r.text[:300]}"
    )
    count = request_count(backend, email=payload["email"])
    assert count == 0, (
        f"{REQUEST_TABLE} holds {count} row(s) for {payload['email']} after a "
        f"submission without consent; a refused submission writes nothing at all"
    )


def test_enquiry_with_invalid_email_is_rejected(anon_client, backend):
    payload = enquiry_payload(email="not-an-address")
    r = submit_enquiry(anon_client, payload)
    assert r.status_code in REFUSED, (
        f"POST /api/enquiry with a malformed address returned {r.status_code}, "
        f"expected the submission to be refused: {r.text[:300]}"
    )
    count = request_count(backend, email="not-an-address")
    assert count == 0, (
        f"{REQUEST_TABLE} holds {count} row(s) for a malformed address; a refused "
        f"submission writes nothing at all"
    )


def test_invalid_status_transition_is_rejected(engineer_client):
    r = engineer_client.patch(f"/requests/{SEEDED_REQUEST_REF}",
                              json={"status": "reported"})
    assert r.status_code in REFUSED, (
        f"PATCH /api/requests/{SEEDED_REQUEST_REF} moving from new straight to "
        f"reported returned {r.status_code}, expected the transition to be refused as "
        f"invalid with a reason: the status moves forward one step at a time and only "
        f"declined is reachable from anywhere: {r.text[:300]}"
    )


def test_rejected_transition_leaves_the_status_unchanged(engineer_client, backend):
    before = request_rows(backend, request_ref=SEEDED_REQUEST_REF)
    assert before, (
        f"no row in {REQUEST_TABLE} carries request_ref {SEEDED_REQUEST_REF}"
    )
    engineer_client.patch(f"/requests/{SEEDED_REQUEST_REF}",
                          json={"status": "reported"})
    after = request_rows(backend, request_ref=SEEDED_REQUEST_REF)
    assert _text(after[0].get("status")) == _text(before[0].get("status")), (
        f"request {SEEDED_REQUEST_REF} moved from {before[0].get('status')!r} to "
        f"{after[0].get('status')!r} after a refused transition; the stored status "
        f"does not change when a transition is refused"
    )


def test_unknown_route_answers_not_found(app_url):
    r = fetch(app_url, "/en/cases/00000-does-not-exist")
    assert r.status_code == 404, (
        f"an address that does not exist returned {r.status_code}, expected 404. A "
        f"redirect answers success and hides the broken link that sent the reader "
        f"there"
    )


def test_every_internal_link_resolves(app_url, page):
    page.goto(f"{app_url}{ENGLISH_PREFIX}", wait_until="domcontentloaded")
    hrefs = page.eval_on_selector_all(
        "a[href]", "els => els.map(e => e.getAttribute('href'))")
    internal = sorted({h for h in hrefs if h and h.startswith("/")})
    assert internal, (
        f"the English home route exposes no internal links at all; every route is "
        f"reachable by following links from the locale home"
    )
    broken = []
    for href in internal:
        r = fetch(app_url, href)
        if r.status_code >= 400:
            broken.append((href, r.status_code))
    assert not broken, (
        f"{len(broken)} internal link(s) on the home route do not resolve: {broken}"
    )


def test_enquiry_form_names_the_invalid_field_inline(app_url, page):
    page.goto(f"{app_url}{ENGLISH_PREFIX}/contacts", wait_until="domcontentloaded")
    invalid = page.eval_on_selector_all(
        "input, textarea",
        "els => els.map(e => ({name: e.name || e.id || '', required: e.required, "
        "labelled: !!(e.getAttribute('aria-label') || e.getAttribute('aria-labelledby') "
        "|| (e.id && document.querySelector('label[for=\"' + e.id + '\"]')))}))")
    assert invalid, (
        "the contacts route exposes no form fields; the enquiry form is the main "
        "content of that route"
    )
    unlabelled = [f for f in invalid if not f["labelled"]]
    assert not unlabelled, (
        f"{len(unlabelled)} enquiry field(s) carry no real label: {unlabelled}. The "
        f"field name sitting on the line as placeholder text disappears the moment "
        f"the visitor types, so a real label must exist behind it"
    )
    required = [f for f in invalid if f["required"]]
    assert required, (
        "no enquiry field is marked required in the markup; required is marked in "
        "the markup and not only by validation"
    )


def test_content_images_carry_alternative_text(app_url, page):
    page.goto(f"{app_url}{ENGLISH_PREFIX}/products/frs",
              wait_until="domcontentloaded")
    images = page.eval_on_selector_all(
        "img",
        "els => els.map(e => ({src: e.getAttribute('src') || '', "
        "alt: e.getAttribute('alt'), hidden: e.getAttribute('aria-hidden') === 'true' "
        "|| e.getAttribute('role') === 'presentation'}))")
    bare = [i for i in images if i["alt"] is None and not i["hidden"]]
    assert not bare, (
        f"{len(bare)} picture(s) on the FRS route carry neither alternative text nor "
        f"a decorative marking: {bare[:5]}. A content picture says what it shows; a "
        f"decorative one declares itself decorative"
    )


def test_narrow_viewport_has_no_sideways_overflow(app_url, page):
    page.set_viewport_size(NARROW_VIEWPORT)
    for route in (f"{ENGLISH_PREFIX}/products/frs", f"{ENGLISH_PREFIX}/cases/22061"):
        page.goto(f"{app_url}{route}", wait_until="domcontentloaded")
        overflow = page.evaluate(
            "() => document.documentElement.scrollWidth - "
            "document.documentElement.clientWidth")
        assert overflow <= 1, (
            f"{route} overflows sideways by {overflow}px at a handset width. A "
            f"specification table scrolls inside its own cell; the document never "
            f"scrolls sideways"
        )


def test_privacy_route_is_linked_from_every_footer(app_url, page):
    for route in (f"{ENGLISH_PREFIX}", f"{ENGLISH_PREFIX}/products",
                  f"{ENGLISH_PREFIX}/cases/22061"):
        page.goto(f"{app_url}{route}", wait_until="domcontentloaded")
        hrefs = page.eval_on_selector_all(
            "a[href]", "els => els.map(e => e.getAttribute('href'))")
        assert any(h and "privacy" in h for h in hrefs), (
            f"{route} carries no link to the privacy route. Every consent label links "
            f"to it, so the route is load-bearing rather than decorative"
        )
