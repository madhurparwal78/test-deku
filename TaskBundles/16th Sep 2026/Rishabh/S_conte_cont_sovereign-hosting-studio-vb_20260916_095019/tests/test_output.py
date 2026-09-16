from __future__ import annotations

import datetime as dt
import os
import re
import threading

import httpx

import _shapes
import conftest


def _submit(client, body):
    return client.post("/build-requests", json=body)


def _submit_multipart(client, body, payload, filename="brief.pdf",
                      content_type="application/pdf"):
    return client.post(
        "/build-requests",
        data=conftest.form_fields(body),
        files={"attachment": (filename, payload, content_type)})


def _accepted(response, what):
    assert response.status_code in (200, 201), (
        f"{what} must be accepted: " + conftest.describe(response))
    return response.json()


def _request_row(backend, reference):
    row = backend.one("build_requests", reference=reference)
    assert row is not None, f"request {reference} must exist as a stored row"
    return row


def _attachment_rows(backend, row):
    return backend.rows("attachments", limit=10, build_request_id=row["id"])


def _mine(client):
    response = client.get("/build-requests/mine")
    assert response.status_code == 200, (
        "a signed-in client must list their own requests: "
        + conftest.describe(response))
    return [conftest.reference_of(r) for r in _shapes.items(response.json())]


def _set_status(founder, reference, status):
    return founder.post(f"/build-requests/{reference}/status",
                        json={"status": status})


def _record_listing(anon, **params):
    response = anon.get("/builds", params=params)
    assert response.status_code == 200, (
        "the build index must be public: " + conftest.describe(response))
    return [str(r.get("slug")) for r in _shapes.items(response.json())]


def _create_record(founder, **kw):
    body = conftest.build_record_body(**kw)
    response = founder.post("/builds", json=body)
    assert response.status_code in (200, 201), (
        "the founder must be able to create a build record: "
        + conftest.describe(response))
    return body["slug"]


def _home_links(site):
    page = site.get("/")
    assert page.status_code == 200, "the home route must render: " + conftest.describe(page)
    return conftest.anchors(page.text)


def _link_target(links, label, base):
    for href, text in links:
        if label in text:
            return conftest.path_of(href, base)
    raise AssertionError(f"the home route carries no link reading {label!r}")


def _link_query(links, label):
    for href, text in links:
        if label in text:
            return href
    raise AssertionError(f"no link reading {label!r}")


def test_health_endpoint_reports_ready(anon):
    response = anon.get("/health")
    assert response.status_code == 200, (
        "GET /api/health must answer 200 once the app is ready: "
        + conftest.describe(response))


def test_seeded_accounts_sign_in_with_their_roles(anon):
    for email, role in ((conftest.FOUNDER_EMAIL, "founder"),
                        (conftest.CLIENT_EMAIL, "client"),
                        (conftest.CLIENT2_EMAIL, "client")):
        response = anon.post("/auth/login", json={
            "email": email, "password": conftest.APP_PASSWORD})
        assert response.status_code == 200, (
            f"the seeded account {email} must sign in with the corpus "
            "password: " + conftest.describe(response))
        body = response.json()
        assert body.get("access_token"), (
            f"sign-in for {email} must return an access_token: {response.text[:300]}")
        assert role in _shapes.flatten(body), (
            f"sign-in for {email} must report the role {role}: {response.text[:300]}")


def test_login_with_a_wrong_password_is_denied(anon):
    response = anon.post("/auth/login", json={
        "email": conftest.CLIENT_EMAIL, "password": "not-the-password-2026"})
    assert conftest.is_client_error(response), (
        "a wrong password must be refused as a client error: "
        + conftest.describe(response))


def test_signup_creates_a_client_whatever_role_is_claimed(anon, backend):
    email = conftest.probe_email()
    response = anon.post("/auth/signup", json={
        "email": email, "password": conftest.APP_PASSWORD, "role": "founder"})
    body = _accepted(response, "a signup")
    assert body.get("access_token") or conftest.field(body, "access_token"), (
        f"signup must return an access_token: {response.text[:300]}")
    row = backend.one("accounts", email=email)
    assert row is not None, f"signup must store an account row for {email}"
    assert row.get("role") == "client", (
        f"signup must create a client whatever the body claims; the row "
        f"carries role={row.get('role')!r}")
    login = anon.post("/auth/login", json={
        "email": email, "password": conftest.APP_PASSWORD})
    assert login.status_code == 200, (
        "a new client must be able to sign in: " + conftest.describe(login))


def test_signup_sets_no_cookie_and_stores_a_hashed_password(anon, backend):
    email = conftest.probe_email()
    response = anon.post("/auth/signup", json={
        "email": email, "password": conftest.APP_PASSWORD})
    _accepted(response, "a signup")
    assert "set-cookie" not in {k.lower() for k in response.headers}, (
        "signup must not set a cookie; the response carried "
        f"{dict(response.headers)}")
    row = backend.one("accounts", email=email)
    assert row is not None, f"signup must store an account row for {email}"
    assert conftest.APP_PASSWORD not in [str(v) for v in row.values()], (
        "the password must be stored hashed, never as the literal")


def test_pricing_rules_expose_the_current_and_retired_versions(anon):
    current = anon.get("/pricing-rules")
    assert current.status_code == 200, (
        "the rule table must be public: " + conftest.describe(current))
    assert str(conftest.field(current.json(), "version")) == conftest.CURRENT_RULES, (
        f"the current rule table must be {conftest.CURRENT_RULES}: {current.text[:300]}")
    retired = anon.get(f"/pricing-rules/{conftest.RETIRED_RULES}")
    assert retired.status_code == 200, (
        "a retired rule table must stay readable by version: "
        + conftest.describe(retired))
    assert str(conftest.field(retired.json(), "version")) == conftest.RETIRED_RULES, (
        f"the retired table must name {conftest.RETIRED_RULES}: {retired.text[:300]}")


def test_worked_examples_produce_the_pinned_figures(anon, backend):
    for caps, posture, residency, timeline, expected in conftest.WORKED_EXAMPLES:
        assert conftest.figure(caps, posture, residency, timeline) == expected
        body = conftest.request_body(caps, posture, residency, timeline)
        created = _accepted(_submit(anon, body),
                            f"the worked example {caps} {posture} {residency} {timeline}")
        reference = conftest.reference_of(created)
        assert int(conftest.field(created, "indicative_minor")) == expected, (
            f"{caps} {posture} {residency} {timeline} must give {expected}; "
            f"the response carried {created}")
        assert str(conftest.field(created, "currency")).lower() == conftest.CURRENCY, (
            f"the figure must be in {conftest.CURRENCY}: {created}")
        assert str(conftest.field(created, "rules_version")) == conftest.CURRENT_RULES, (
            f"the created request must name its rule table: {created}")
        assert str(conftest.field(created, "status")) == "new", (
            f"the created request must report the status new: {created}")
        row = _request_row(backend, reference)
        assert int(row["indicative_minor"]) == expected, (
            f"request {reference} must store {expected}; the row carried "
            f"{row['indicative_minor']}")


def test_figure_mismatch_is_rejected_and_writes_nothing(anon, backend):
    body = conftest.request_body()
    body["indicative_minor"] = body["indicative_minor"] + 50000
    response = _submit(anon, body)
    assert conftest.is_client_error(response), (
        "a tampered figure must be rejected as a client error: "
        + conftest.describe(response))
    assert "indicative_minor" in response.text, (
        "the rejection must name indicative_minor: " + conftest.describe(response))
    assert conftest.requests_for(backend, body["contact_email"]) == [], (
        "a rejected submission must write no request row")


def test_retired_or_unknown_rule_version_is_rejected(anon, backend):
    retired = conftest.request_body(
        rules_version=conftest.RETIRED_RULES,
        indicative_minor=conftest.figure(("software",), "managed", "eu",
                                         "standard", conftest.RETIRED_RULES))
    response = _submit(anon, retired)
    assert conftest.is_client_error(response), (
        "a submission naming the retired table must be rejected: "
        + conftest.describe(response))
    assert "rules_version" in response.text, (
        "the rejection must name rules_version: " + conftest.describe(response))
    unknown = conftest.request_body(rules_version="1999-01")
    other = _submit(anon, unknown)
    assert conftest.is_client_error(other), (
        "a submission naming an unknown table must be rejected: "
        + conftest.describe(other))
    for body in (retired, unknown):
        assert conftest.requests_for(backend, body["contact_email"]) == [], (
            "a submission refused for its version must write nothing")


def test_submission_without_a_figure_stores_the_server_figure(anon, backend):
    body = conftest.request_body(("hosting",), "handover", "de", "flexible")
    body.pop("indicative_minor")
    created = _accepted(_submit(anon, body), "a submission carrying no figure")
    expected = conftest.figure(("hosting",), "handover", "de", "flexible")
    row = _request_row(backend, conftest.reference_of(created))
    assert int(row["indicative_minor"]) == expected, (
        f"a submission with no figure must be stored with the server figure "
        f"{expected}; the row carried {row['indicative_minor']}")


def test_budget_band_never_changes_the_figure(anon):
    figures = set()
    for band in conftest.BUDGET_BANDS:
        created = _accepted(_submit(anon, conftest.request_body(budget=band)),
                            f"a submission in band {band}")
        figures.add(int(conftest.field(created, "indicative_minor")))
    assert figures == {conftest.figure(("software",), "managed", "eu", "standard")}, (
        f"the budget band must never change the figure; saw {figures}")


def test_capabilities_are_stored_once_in_canonical_order(anon, backend):
    caps = ["hosting", "software", "software"]
    body = conftest.request_body(caps)
    created = _accepted(_submit(anon, body), "a submission with repeated keys")
    row = _request_row(backend, conftest.reference_of(created))
    stored = row["capabilities"]
    if isinstance(stored, str):
        stored = [s for s in re.split(r"[^a-z]+", stored) if s]
    assert list(stored) == ["software", "hosting"], (
        f"capabilities must be stored once each in the order software, website, "
        f"hosting; the row carried {row['capabilities']!r}")
    assert int(row["indicative_minor"]) == conftest.figure(caps, "managed", "eu", "standard"), (
        "a repeated capability must count once in the figure")


def test_reference_numbers_follow_the_pinned_shape(anon):
    before = dt.datetime.now(dt.timezone.utc).year
    first = conftest.reference_of(_accepted(_submit(anon, conftest.request_body()),
                                            "a first submission"))
    second = conftest.reference_of(_accepted(_submit(anon, conftest.request_body()),
                                             "a second submission"))
    after = dt.datetime.now(dt.timezone.utc).year
    numbers = []
    for reference in (first, second):
        match = conftest.REFERENCE_RE.match(reference)
        assert match, f"reference {reference!r} must read VS-<year>-<NNNN>"
        year, number = int(match.group(1)), int(match.group(2))
        assert before <= year <= after, (
            f"reference {reference} must carry the UTC year of submission")
        if year == 2026:
            assert number >= 3, (
                f"reference {reference} must continue after the seeded "
                "VS-2026-0001 and VS-2026-0002")
        numbers.append((year, number))
    assert first != second, "two requests must never share a reference"
    assert numbers[1] > numbers[0], (
        f"a later request must carry the higher number: {first} then {second}")


def test_concurrent_submissions_receive_distinct_references(anon, api_base):
    results = []
    barrier = threading.Barrier(4)

    def worker():
        body = conftest.request_body()
        with httpx.Client(base_url=api_base, timeout=30.0) as c:
            barrier.wait()
            results.append(c.post("/build-requests", json=body))

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    references = []
    for response in results:
        references.append(conftest.reference_of(
            _accepted(response, "a concurrent submission")))
    assert len(set(references)) == len(references), (
        f"concurrent submissions must receive distinct references: {references}")
    parsed = sorted(conftest.REFERENCE_RE.match(r).groups() for r in references)
    if len({year for year, _ in parsed}) == 1:
        numbers = [int(n) for _, n in parsed]
        assert numbers == list(range(numbers[0], numbers[0] + len(numbers))), (
            f"concurrent references must skip no number: {references}")


def test_decoy_field_submission_is_refused(anon, backend):
    body = conftest.request_body(contact_fax="+49 30 1234567")
    response = _submit(anon, body)
    assert conftest.is_client_error(response), (
        "a submission with a filled decoy field must be refused: "
        + conftest.describe(response))
    assert conftest.requests_for(backend, body["contact_email"]) == [], (
        "a refused decoy submission must write nothing")


def test_duplicate_enquiry_from_one_network_is_refused(anon, backend):
    body = conftest.request_body()
    _accepted(_submit(anon, body), "the first of two identical enquiries")
    repeat = _submit(anon, dict(body))
    assert conftest.is_client_error(repeat), (
        "the same enquiry repeated from one network within ten minutes must be "
        "refused as a duplicate: " + conftest.describe(repeat))
    assert len(conftest.requests_for(backend, body["contact_email"])) == 1, (
        "a refused duplicate must write nothing")


def test_invalid_composer_fields_are_rejected(anon, backend):
    cases = {
        "capabilities": [],
        "posture": "outsourced",
        "residency": "us",
        "timeline": "rush",
        "budget_band": "unlimited",
        "description": "x" * (conftest.DESCRIPTION_MIN - 1),
    }
    for name, value in cases.items():
        body = conftest.request_body()
        body[name] = value
        if name == "capabilities":
            body.pop("indicative_minor")
        response = _submit(anon, body)
        assert conftest.is_client_error(response), (
            f"an invalid {name} must be rejected as a client error: "
            + conftest.describe(response))
        assert name in response.text, (
            f"the rejection must name {name}: " + conftest.describe(response))
        assert conftest.requests_for(backend, body["contact_email"]) == [], (
            f"a submission with an invalid {name} must write nothing")
    long_body = conftest.request_body()
    long_body["description"] = "y" * (conftest.DESCRIPTION_MAX + 1)
    response = _submit(anon, long_body)
    assert conftest.is_client_error(response), (
        "a description over the limit must be rejected: "
        + conftest.describe(response))


def test_attachment_upload_lands_in_the_bucket(anon, backend, store):
    body = conftest.request_body()
    payload = conftest.pdf_payload()
    created = _accepted(_submit_multipart(anon, body, payload),
                        "a submission with an attached PDF brief")
    reference = conftest.reference_of(created)
    key = conftest.ATTACHMENT_KEY_TEMPLATE.format(
        reference=reference, digest=conftest.sha256_hex(payload), ext="pdf")
    row = _request_row(backend, reference)
    attachments = _attachment_rows(backend, row)
    assert len(attachments) == 1, (
        f"request {reference} must hold exactly one attachment row; found "
        f"{len(attachments)}")
    assert attachments[0]["object_key"] == key, (
        f"the attachment must be stored at {key}; the row carried "
        f"{attachments[0]['object_key']}")
    assert store.exists(key), f"the attached bytes must exist in the bucket at {key}"


def test_attached_file_object_is_not_anonymously_readable(anon, store):
    body = conftest.request_body()
    payload = conftest.pdf_payload()
    reference = conftest.reference_of(_accepted(
        _submit_multipart(anon, body, payload), "a submission with a brief"))
    key = conftest.ATTACHMENT_KEY_TEMPLATE.format(
        reference=reference, digest=conftest.sha256_hex(payload), ext="pdf")
    keys = [key] + store.list(prefix=f"requests/{conftest.SEEDED_REQUEST}/")
    for object_key in keys:
        response = httpx.get(conftest.storage_object_url(object_key), timeout=30.0)
        assert response.status_code in (401, 403), (
            f"the stored object {object_key} must be refused without storage "
            f"credentials; the bucket answered {response.status_code}")


def test_seeded_attachment_is_stored_under_its_request(store, backend):
    keys = store.list(prefix=f"requests/{conftest.SEEDED_REQUEST}/")
    assert keys, (
        f"the seeded brief of {conftest.SEEDED_REQUEST} must be stored in the "
        "bucket under its request prefix")
    row = _request_row(backend, conftest.SEEDED_REQUEST)
    attachments = _attachment_rows(backend, row)
    assert len(attachments) == 1, (
        f"{conftest.SEEDED_REQUEST} must carry exactly one attached brief")
    assert attachments[0].get("original_name") == conftest.SEEDED_ATTACHMENT_NAME, (
        f"the seeded brief must be named {conftest.SEEDED_ATTACHMENT_NAME}; the row "
        f"carried {attachments[0].get('original_name')!r}")
    assert attachments[0]["object_key"] in keys, (
        "the seeded attachment row must point at the stored object")


def test_owner_downloads_the_attached_brief(client, client_token, api_base):
    body = conftest.request_body()
    payload = conftest.pdf_payload()
    reference = conftest.reference_of(_accepted(
        _submit_multipart(client, body, payload),
        "a signed-in submission with a brief"))
    with httpx.Client(base_url=api_base, timeout=30.0, follow_redirects=True,
                      headers={"Authorization": f"Bearer {client_token}"}) as c:
        response = c.get(f"/build-requests/{reference}/attachment")
    if response.headers.get("content-type", "").startswith("application/json"):
        link = conftest.field(response.json(), "url", "link", "href")
        assert link, f"the attachment answer must carry the bytes or a link: {response.text[:300]}"
        expires = re.search(r"X-Amz-Expires=(\d+)", str(link))
        assert expires is None or int(expires.group(1)) <= 300, (
            f"a presigned link must expire within five minutes: {link}")
        response = httpx.get(str(link), timeout=30.0)
    assert response.status_code == 200, (
        "the owning client must be able to download the attached brief: "
        + conftest.describe(response))
    assert response.content == payload, (
        "the downloaded brief must be byte-identical to the upload")


def test_other_client_is_denied_the_seeded_request(client2):
    response = client2.get(f"/build-requests/{conftest.SEEDED_REQUEST}")
    assert conftest.is_denied(response), (
        f"client2 must be denied {conftest.SEEDED_REQUEST}: "
        + conftest.describe(response))
    text = response.text.lower()
    for leaked in (conftest.CLIENT_EMAIL, "handover", "25k-60k", "1450000"):
        assert leaked not in text, (
            f"the refusal must reveal nothing about the request; it carried {leaked!r}")


def test_other_client_is_denied_the_seeded_attachment(client2):
    response = client2.get(f"/build-requests/{conftest.SEEDED_REQUEST}/attachment")
    assert conftest.is_denied(response), (
        f"client2 must be denied the brief of {conftest.SEEDED_REQUEST}: "
        + conftest.describe(response))
    assert not response.content.startswith(b"%PDF"), (
        "the refusal must not carry the brief's bytes")


def test_unauthenticated_caller_is_denied_requests_and_briefs(anon):
    for path in (f"/build-requests/{conftest.SEEDED_REQUEST}",
                 f"/build-requests/{conftest.SEEDED_REQUEST}/attachment",
                 "/build-requests", "/build-requests/mine"):
        response = anon.get(path)
        assert conftest.is_denied(response), (
            f"an anonymous caller must be denied {path}: "
            + conftest.describe(response))
        assert conftest.CLIENT_EMAIL not in response.text, (
            f"the refusal for {path} must reveal nothing about any request")


def test_client_lists_only_own_requests(client, client2):
    mine = _mine(client)
    theirs = _mine(client2)
    assert conftest.SEEDED_REQUEST in mine, (
        f"client@example.com must see {conftest.SEEDED_REQUEST}; saw {mine}")
    assert conftest.SECOND_SEEDED_REQUEST not in mine, (
        f"client@example.com must not see {conftest.SECOND_SEEDED_REQUEST}")
    assert conftest.SECOND_SEEDED_REQUEST in theirs, (
        f"client2@example.com must see {conftest.SECOND_SEEDED_REQUEST}; saw {theirs}")
    assert conftest.SEEDED_REQUEST not in theirs, (
        f"client2@example.com must not see {conftest.SEEDED_REQUEST}")


def test_signed_in_submission_is_owned_by_the_client(client, client2):
    created = _accepted(_submit(client, conftest.request_body()),
                        "a signed-in submission")
    reference = conftest.reference_of(created)
    assert str(conftest.field(created, "status")) == "new", (
        f"a new request must start with the status new: {created}")
    assert reference in _mine(client), (
        f"a request sent while signed in must appear in that client's list")
    assert reference not in _mine(client2), (
        f"a request must never appear in another client's list")
    listing = client.get("/build-requests/mine")
    row = next(r for r in _shapes.items(listing.json())
               if conftest.reference_of(r) == reference)
    assert str(conftest.field(row, "status")) == "new", (
        f"the client's list must show the current status: {row}")
    assert conftest.field(row, "indicative_minor") is not None, (
        f"the client's list must show the figure: {row}")


def test_signed_out_submission_joins_no_client_list(anon, client, client2, founder):
    reference = conftest.reference_of(_accepted(
        _submit(anon, conftest.request_body()), "a signed-out submission"))
    assert reference not in _mine(client), (
        "a signed-out request must appear in no client's list")
    assert reference not in _mine(client2), (
        "a signed-out request must appear in no client's list")
    response = founder.get(f"/build-requests/{reference}")
    assert response.status_code == 200, (
        "the founder must read a signed-out request: " + conftest.describe(response))


def test_founder_reads_every_request_with_its_brief(founder):
    listing = founder.get("/build-requests")
    assert listing.status_code == 200, (
        "the founder must list every request: " + conftest.describe(listing))
    rows = listing.json()
    assert isinstance(rows, list), "the request list must be a top-level array"
    references = [conftest.reference_of(r) for r in rows]
    for seeded in (conftest.SEEDED_REQUEST, conftest.SECOND_SEEDED_REQUEST):
        assert seeded in references, f"the founder's list must include {seeded}"
    assert references.index(conftest.SECOND_SEEDED_REQUEST) < references.index(
        conftest.SEEDED_REQUEST), "the founder's list must be newest first"
    detail = founder.get(f"/build-requests/{conftest.SEEDED_REQUEST}")
    assert detail.status_code == 200, (
        "the founder must read the seeded request: " + conftest.describe(detail))
    assert conftest.field(detail.json(), "attachment"), (
        f"the request detail must carry its attachment: {detail.text[:300]}")
    brief = founder.get(f"/build-requests/{conftest.SEEDED_REQUEST}/attachment")
    assert brief.status_code in (200, 302, 303, 307), (
        "the founder must be able to read the seeded brief: "
        + conftest.describe(brief))


def test_attachment_of_another_type_is_rejected(anon, backend, store):
    body = conftest.request_body()
    before = len(store.list(prefix=conftest.ATTACHMENT_PREFIX))
    response = _submit_multipart(anon, body, b"plain text pretending to be a pdf",
                                 filename="brief.pdf",
                                 content_type="application/pdf")
    assert conftest.is_client_error(response), (
        "a file whose bytes are not a PDF, PNG or JPEG must be rejected: "
        + conftest.describe(response))
    assert conftest.requests_for(backend, body["contact_email"]) == [], (
        "a submission rejected for its file must write no request row")
    assert len(store.list(prefix=conftest.ATTACHMENT_PREFIX)) == before, (
        "a submission rejected for its file must store no object")


def test_oversized_attachment_is_rejected(anon, backend):
    body = conftest.request_body()
    payload = conftest.PDF_HEAD + b"0" * conftest.MAX_ATTACHMENT_BYTES
    response = _submit_multipart(anon, body, payload)
    assert conftest.is_client_error(response), (
        "a brief over 5242880 bytes must be rejected: "
        + conftest.describe(response))
    assert conftest.requests_for(backend, body["contact_email"]) == [], (
        "an oversized submission must write nothing")


def test_status_moves_follow_the_review_graph(anon, founder, backend):
    def fresh():
        return conftest.reference_of(_accepted(
            _submit(anon, conftest.request_body()), "a fresh request"))

    reference = fresh()
    for status in ("reviewing", "quoted", "accepted"):
        response = _set_status(founder, reference, status)
        assert response.status_code == 200, (
            f"the founder must move {reference} to {status}: "
            + conftest.describe(response))
    backwards = _set_status(founder, reference, "reviewing")
    assert conftest.is_client_error(backwards), (
        "an accepted request must never change status again: "
        + conftest.describe(backwards))
    assert _request_row(backend, reference)["status"] == "accepted", (
        "a refused move must leave the request unchanged")

    declined = fresh()
    assert _set_status(founder, declined, "declined").status_code == 200, (
        "a new request may go straight to declined")
    reopened = _set_status(founder, declined, "reviewing")
    assert conftest.is_client_error(reopened), (
        "a declined request must never change status again")

    skipping = fresh()
    jump = _set_status(founder, skipping, "quoted")
    assert conftest.is_client_error(jump), (
        "new to quoted is not a legal move and must be rejected: "
        + conftest.describe(jump))
    assert _request_row(backend, skipping)["status"] == "new", (
        "a refused move must leave the request at new")

    reviewing = fresh()
    assert _set_status(founder, reviewing, "reviewing").status_code == 200
    assert _set_status(founder, reviewing, "declined").status_code == 200, (
        "a reviewing request may go straight to declined")


def test_client_cannot_change_a_request_status(client, backend):
    reference = conftest.reference_of(_accepted(
        _submit(client, conftest.request_body()), "a signed-in submission"))
    response = _set_status(client, reference, "accepted")
    assert response.status_code in (401, 403), (
        "a client must be denied a status change: " + conftest.describe(response))
    assert _request_row(backend, reference)["status"] == "new", (
        "a denied status change must leave the request unchanged")


def test_seeded_requests_keep_their_rules_version_and_figure(backend):
    first = _request_row(backend, conftest.SEEDED_REQUEST)
    second = _request_row(backend, conftest.SECOND_SEEDED_REQUEST)
    assert first["rules_version"] == conftest.CURRENT_RULES, (
        f"{conftest.SEEDED_REQUEST} must be stored on {conftest.CURRENT_RULES}")
    assert int(first["indicative_minor"]) == conftest.SEEDED_FIRST_REQUEST_FIGURE, (
        f"{conftest.SEEDED_REQUEST} must keep the figure 1450000")
    assert first["status"] == "reviewing", (
        f"{conftest.SEEDED_REQUEST} must be seeded at reviewing")
    assert (first["posture"], first["residency"], first["timeline"],
            first["budget_band"]) == ("handover", "de", "standard", "25k-60k"), (
        f"{conftest.SEEDED_REQUEST} must hold its seeded selections: {first}")
    assert int(second["indicative_minor"]) == conftest.SEEDED_SECOND_REQUEST_FIGURE, (
        f"{conftest.SECOND_SEEDED_REQUEST} must keep the figure 550000")
    assert second["status"] == "new", (
        f"{conftest.SECOND_SEEDED_REQUEST} must be seeded at new")
    assert second["contact_email"] == conftest.CLIENT2_EMAIL
    assert (second["posture"], second["residency"], second["timeline"],
            second["budget_band"]) == ("managed", "eu", "flexible", "under-10k"), (
        f"{conftest.SECOND_SEEDED_REQUEST} must hold its seeded selections: {second}")
    assert second["rules_version"] == conftest.CURRENT_RULES
    assert _attachment_rows(backend, second) == [], (
        f"{conftest.SECOND_SEEDED_REQUEST} must carry no attachment")


def test_request_rows_hold_no_visitor_identifier(backend):
    row = _request_row(backend, conftest.SEEDED_REQUEST)
    for column in row:
        parts = set(re.split(r"[^a-z]+", column.lower()))
        for word in conftest.IDENTIFYING_COLUMN_WORDS:
            assert word not in parts, (
                f"build_requests must hold no network address, browser "
                f"signature or cookie value; found the column {column!r}")


def test_no_script_form_returns_the_summary_page(ui_page, app_base, backend):
    ui_page.goto(f"{app_base}/build-request")
    assert "Describe the build" in conftest.body_text(ui_page), (
        "the composer must carry the heading Describe the build")
    email = conftest.probe_email()
    ui_page.locator("input[name='capabilities'][value='software']").first.check()
    conftest.choose(ui_page, "posture", "handover")
    conftest.choose(ui_page, "residency", "de")
    conftest.choose(ui_page, "timeline", "standard")
    conftest.choose(ui_page, "budget_band", "25k-60k")
    ui_page.fill("[name='description']",
                 f"No-script probe {conftest.unique_token()} for a billing tool.")
    ui_page.fill("[name='contact_name']", "Probe Plainform")
    ui_page.fill("[name='contact_email']", email)
    ui_page.get_by_role("button", name="Send build request").click()
    ui_page.wait_for_load_state()
    text = conftest.body_text(ui_page)
    assert "Request received" in text, (
        f"the no-script submission must render the summary page; saw {text[:300]}")
    found = conftest.REFERENCE_IN_TEXT_RE.findall(text)
    assert found, f"the summary page must show the reference; saw {text[:300]}"
    assert conftest.euros(1450000) in text, (
        f"the summary page must show the server figure EUR 14,500; saw {text[:300]}")
    assert conftest.CURRENT_RULES in text, "the summary must show the rule table version"
    assert "new" in text.lower(), "the summary must show the status new"
    rows = conftest.requests_for(backend, email)
    assert len(rows) == 1 and rows[0]["reference"] == found[0], (
        "the no-script path must store one request carrying the shown reference")
    assert int(rows[0]["indicative_minor"]) == 1450000


def test_composer_address_restores_fields_and_figure(page, app_base):
    page.goto(f"{app_base}/build-request?cap=software,website&posture=handover"
              f"&residency=de&timeline=accelerated&budget=over-60k"
              f"&desc=Restored%20composer%20state%20probe&v=2026-09")
    assert conftest.poll_until(lambda: "EUR 26,500" in conftest.body_text(page), 15), (
        "a composed address must reopen showing the figure EUR 26,500")
    assert "Indicative figure" in conftest.body_text(page)
    for value in ("software", "website"):
        assert page.locator(
            f"input[name='capabilities'][value='{value}']").first.is_checked(), (
            f"the composed address must restore the {value} capability")
    assert not page.locator(
        "input[name='capabilities'][value='hosting']").first.is_checked()
    assert page.input_value("[name='description']") == "Restored composer state probe", (
        "the composed address must restore the description")


def test_retired_version_address_shows_the_quoted_figure(page, app_base):
    page.goto(f"{app_base}/build-request?cap=software&posture=managed"
              f"&residency=eu&timeline=standard&budget=under-10k"
              f"&desc=Retired%20table%20probe&v=2026-03")
    assert conftest.poll_until(lambda: "EUR 10,000" in conftest.body_text(page), 15), (
        "an address naming 2026-03 must show the figure quoted under 2026-03")
    assert conftest.RETIRED_RULES in conftest.body_text(page), (
        "the retired figure must be labelled with its version")


def test_composer_page_carries_the_pinned_controls(ui_page, app_base):
    ui_page.goto(f"{app_base}/build-request")
    text = conftest.body_text(ui_page)
    for copy in conftest.COMPOSER_COPY:
        assert copy in text, f"the composer must show {copy!r}"
    for name in conftest.COMPOSER_CONTROL_NAMES:
        assert ui_page.locator(f"[name='{name}']").count() >= 1, (
            f"the composer must carry a control named {name}")
    decoy = ui_page.locator("[name='contact_fax']").first
    assert not decoy.is_visible(), "the decoy field must be invisible to a person"


def test_status_feed_lists_seeded_systems_in_position_order(anon):
    data = conftest.feed(anon)
    assert "nextCheckAt" in data, "the envelope must carry nextCheckAt"
    projects = data.get("projects")
    assert isinstance(projects, list), "projects must be an array"
    names = [p.get("name") for p in projects]
    assert names[:7] == list(conftest.SEEDED_SYSTEM_NAMES), (
        f"the feed must list the seeded systems first in position order; saw {names}")
    positions = [p.get("position") for p in projects]
    assert positions == sorted(positions), f"projects must be sorted by position: {positions}"
    for project in projects:
        for key in conftest.FEED_PROJECT_FIELDS:
            assert key in project, f"a project must carry {key}: {project}"
        assert project["currentStatus"] in conftest.FEED_STATUSES, (
            f"currentStatus must be one of the five words: {project}")
        for bar in project["bars"]:
            assert set(bar) >= {"status", "checkedAt"}, f"a bar must carry status and checkedAt: {bar}"
    text = str(projects).lower()
    for leaked in ("@", "client"):
        assert leaked not in text, "the feed must carry no client name and no address"


def test_system_without_checks_reports_unknown(anon):
    project = conftest.feed_project(anon, conftest.PORTFOLIO_SLUG)
    assert project["currentStatus"] == "unknown", (
        f"a system with no check must report unknown: {project}")
    assert project["latestCheckedAt"] is None, f"latestCheckedAt must be null: {project}"
    assert project["latestResponseMs"] is None, f"latestResponseMs must be null: {project}"
    assert project["lastStatusChangeAt"] is None, f"lastStatusChangeAt must be null: {project}"
    assert project["uptimePercent"] is None, f"uptimePercent must be null: {project}"


def test_seeded_systems_hold_their_check_history(anon):
    for slug in conftest.SEEDED_SYSTEM_SLUGS[:5]:
        project = conftest.feed_project(anon, slug)
        statuses = conftest.bar_statuses(project)
        assert statuses[-12:] == ["up"] * 12, (
            f"{slug} must end with twelve up checks; saw {statuses[-12:]}")
        assert float(project["uptimePercent"]) == 100.0, (
            f"{slug} must report 100.00 uptime: {project['uptimePercent']}")
        assert project["latestResponseMs"] == conftest.SEEDED_CHECK_RESPONSE_MS, (
            f"{slug} must report the seeded response time 48: {project['latestResponseMs']}")
        assert len(statuses) <= conftest.BAR_WINDOW
    console = conftest.bar_statuses(conftest.feed_project(anon, conftest.CONSOLE_SLUG))
    assert len(console) == conftest.BAR_WINDOW, (
        f"the console's long history must be capped at 90 slots; saw {len(console)}")
    tickets = conftest.bar_statuses(conftest.feed_project(anon, conftest.TICKETS_SLUG))
    assert conftest.feed_project(anon, conftest.TICKETS_SLUG)["latestResponseMs"] == conftest.SEEDED_CHECK_RESPONSE_MS
    assert tickets == ["up"] * 6 + ["unknown"] * 2 + ["up"] * 4, (
        f"the tickets system must show ten checks with the seventh and eighth "
        f"slots missed; saw {tickets}")


def test_feed_derives_unknown_slots_and_uptime(founder, anon):
    slug = conftest.create_system(founder)
    rows = [(conftest.at_minutes(10, 0), "up", 40),
            (conftest.at_minutes(10, 5), "up", 44),
            (conftest.at_minutes(10, 10), "down", None),
            (conftest.at_minutes(10, 25), "up", 52)]
    conftest.record_checks(founder, slug, rows)
    data = conftest.feed(anon)
    project = next(p for p in data["projects"] if p["slug"] == slug)
    assert conftest.bar_statuses(project) == ["up", "up", "down", "unknown", "unknown", "up"], (
        f"the missed 10:15 and 10:20 slots must appear as unknown: {project['bars']}")
    unknown_times = [conftest.parse_time(b["checkedAt"]) for b in project["bars"][3:5]]
    assert unknown_times == [conftest.parse_time(conftest.at_minutes(10, 15)),
                             conftest.parse_time(conftest.at_minutes(10, 20))], (
        f"each unknown slot must carry the time the check was due: {project['bars']}")
    assert abs(float(project["uptimePercent"]) - 75.0) < 0.001, (
        f"uptime must be 75.00 over the four real checks: {project['uptimePercent']}")
    assert project["currentStatus"] == "up"
    assert project["latestResponseMs"] == 52
    assert conftest.parse_time(project["latestCheckedAt"]) == conftest.parse_time(rows[-1][0])
    assert conftest.parse_time(project["lastStatusChangeAt"]) == conftest.parse_time(rows[-1][0]), (
        f"lastStatusChangeAt must be the 10:25 check that began the current run: {project}")
    assert project["position"] > 7, "a later system must take a later position"
    assert data["nextCheckAt"] is not None
    assert conftest.parse_time(data["nextCheckAt"]) <= conftest.parse_time(
        conftest.at_minutes(10, 30)), (
        f"nextCheckAt must be the earliest latest check plus interval: {data['nextCheckAt']}")


def test_slow_counts_as_available_in_uptime(founder, anon):
    first = conftest.create_system(founder)
    conftest.record_checks(founder, first, [
        (conftest.at_minutes(10, 0), "up", 40), (conftest.at_minutes(10, 5), "slow", 900),
        (conftest.at_minutes(10, 10), "degraded", 1500), (conftest.at_minutes(10, 15), "up", 40)])
    assert abs(float(conftest.feed_project(anon, first)["uptimePercent"]) - 75.0) < 0.001, (
        "up, slow, degraded, up must give 75.00")
    second = conftest.create_system(founder)
    conftest.record_checks(founder, second, [
        (conftest.at_minutes(10, 0), "up", 40), (conftest.at_minutes(10, 5), "up", 40),
        (conftest.at_minutes(10, 10), "down", None)])
    assert abs(float(conftest.feed_project(anon, second)["uptimePercent"]) - 66.67) < 0.001, (
        "up, up, down must give 66.67")


def test_unknown_gap_does_not_break_the_status_run(founder, anon):
    slug = conftest.create_system(founder)
    conftest.record_checks(founder, slug, [
        (conftest.at_minutes(9, 0), "down", None), (conftest.at_minutes(9, 5), "up", 40),
        (conftest.at_minutes(9, 30), "up", 40)])
    project = conftest.feed_project(anon, slug)
    assert conftest.parse_time(project["lastStatusChangeAt"]) == conftest.parse_time(
        conftest.at_minutes(9, 5)), (
        f"an unknown gap must not start a new run: {project['lastStatusChangeAt']}")


def test_bars_hold_at_most_ninety_slots_ending_with_the_latest(founder, anon):
    slug = conftest.create_system(founder)
    start = conftest.parse_time(conftest.at_minutes(8, 0))
    later = start + dt.timedelta(seconds=conftest.DEFAULT_INTERVAL * 100)
    conftest.record_checks(founder, slug, [
        (conftest.at_minutes(8, 0), "down", None),
        (later.strftime("%Y-%m-%dT%H:%M:%SZ"), "up", 40)])
    project = conftest.feed_project(anon, slug)
    bars = project["bars"]
    assert len(bars) == conftest.BAR_WINDOW, f"bars must hold at most 90 slots; saw {len(bars)}"
    assert bars[-1]["status"] == "up" and conftest.parse_time(bars[-1]["checkedAt"]) == later, (
        f"bars must end with the latest check: {bars[-1]}")
    assert abs(float(project["uptimePercent"]) - 100.0) < 0.001, (
        "only the one real check inside the window may count toward uptime")


def test_exact_repeat_check_changes_nothing(founder, backend):
    slug = conftest.create_system(founder)
    moment = conftest.at_minutes(12, 0)
    conftest.record_checks(founder, slug, [(moment, "up", 40)])
    repeat = conftest.post_check(founder, slug, moment, "up", 99)
    assert repeat.status_code in (200, 201), (
        "an exact repeat must be accepted: " + conftest.describe(repeat))
    system = backend.one("systems", slug=slug)
    assert backend.count("checks", system_id=system["id"]) == 1, (
        "an exact repeat must leave one check row")


def test_conflicting_or_invalid_checks_are_rejected(founder, backend):
    slug = conftest.create_system(founder)
    conftest.record_checks(founder, slug, [
        (conftest.at_minutes(13, 0), "up", 40), (conftest.at_minutes(13, 5), "up", 40)])
    cases = (
        (conftest.at_minutes(13, 5), "down", None, "a different status for a recorded time"),
        (conftest.at_minutes(12, 55), "up", 40, "a check older than the latest"),
        (conftest.at_minutes(13, 10), "unknown", None, "a check posted as unknown"),
        (conftest.at_minutes(13, 15), "up", -5, "a negative response time"),
    )
    for moment, status, response_ms, what in cases:
        response = conftest.post_check(founder, slug, moment, status, response_ms)
        assert conftest.is_client_error(response), (
            f"{what} must be rejected: " + conftest.describe(response))
    system = backend.one("systems", slug=slug)
    assert backend.count("checks", system_id=system["id"]) == 2, (
        "rejected checks must write nothing")
    stored = backend.rows("checks", limit=10, system_id=system["id"])
    assert "unknown" not in {r["status"] for r in stored}
    missing = conftest.post_check(founder, "no-such-system-" + conftest.unique_token(),
                                  conftest.at_minutes(13, 20), "up", 40)
    assert missing.status_code == 404, (
        "a check for an unknown slug must answer not-found: " + conftest.describe(missing))


def test_concurrent_identical_checks_leave_one_row(founder, backend, api_base):
    slug = conftest.create_system(founder)
    token_header = founder.headers.get("Authorization")
    moment = conftest.at_minutes(14, 0)
    barrier = threading.Barrier(4)
    results = []

    def worker():
        with httpx.Client(base_url=api_base, timeout=30.0,
                          headers={"Authorization": token_header}) as c:
            barrier.wait()
            results.append(c.post(f"/systems/{slug}/checks", json={
                "checked_at": moment, "status": "up", "response_ms": 40}))

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert all(r.status_code < 500 for r in results), (
        f"concurrent identical checks must never cause a server error: "
        f"{[r.status_code for r in results]}")
    system = backend.one("systems", slug=slug)
    assert backend.count("checks", system_id=system["id"]) == 1, (
        "the same check sent at the same moment must leave one row")


def test_system_creation_rejects_bad_input_and_applies_defaults(founder, backend):
    slug = conftest.create_system(founder)
    row = backend.one("systems", slug=slug)
    assert (row["interval_seconds"], row["open_after"], row["close_after"]) == (
        conftest.DEFAULT_INTERVAL, conftest.DEFAULT_OPEN_AFTER, conftest.DEFAULT_CLOSE_AFTER), (
        f"a new system must default to 300, 3 and 2: {row}")
    for body, what in (
            ({"slug": slug, "name": "Duplicate"}, "a taken slug"),
            ({"slug": conftest.probe_slug("short"), "name": "Short",
              "interval_seconds": conftest.MINIMUM_INTERVAL - 1}, "an interval under 60"),
            ({"slug": conftest.probe_slug("zero"), "name": "Zero",
              "open_after": 0}, "a threshold under 1")):
        response = founder.post("/systems", json=body)
        assert conftest.is_client_error(response), (
            f"{what} must be rejected: " + conftest.describe(response))
        if body["slug"] != slug:
            assert backend.one("systems", slug=body["slug"]) is None, (
                f"{what} must create nothing")


def test_flapping_system_opens_exactly_one_incident(founder, anon):
    slug = conftest.create_system(founder, open_after=2, close_after=3)
    conftest.record_checks(founder, slug, conftest.flapping_rows())
    incidents = conftest.incidents_for(anon, slug)
    assert len(incidents) == 1, (
        f"a flapping system must hold exactly one incident; saw {incidents}")
    incident = incidents[0]
    assert incident["ref"] == f"{slug}-20260302-1100", (
        f"the reference must join slug, date and time: {incident['ref']}")
    assert conftest.parse_time(incident["opened_at"]) == conftest.parse_time(conftest.at_minutes(11, 0))
    assert conftest.parse_time(incident["resolved_at"]) == conftest.parse_time(conftest.at_minutes(11, 40)), (
        f"the incident must resolve at the check completing three available checks: {incident}")
    entries = conftest.incident_entries(anon, incident["ref"])
    assert [(int(e["seq"]), e["kind"]) for e in entries] == [(1, "opened"), (2, "resolved")], (
        f"opening and resolving must write one entry each, seq 1 and 2: {entries}")
    for entry in entries:
        assert {"seq", "kind", "body", "recorded_at"} <= set(entry), f"entry fields: {entry}"


def test_replaying_a_check_stream_keeps_the_same_incidents(founder, anon, backend):
    slug = conftest.create_system(founder, open_after=2, close_after=3)
    rows = conftest.flapping_rows()
    conftest.record_checks(founder, slug, rows)
    first = [i["ref"] for i in conftest.incidents_for(anon, slug)]
    conftest.record_checks(founder, slug, rows)
    second = [i["ref"] for i in conftest.incidents_for(anon, slug)]
    assert first == second and len(second) == 1, (
        f"replaying the stream must keep the same single incident: {first} then {second}")
    assert len(conftest.incident_entries(anon, second[0])) == 2, (
        "replaying must add no entry")
    system = backend.one("systems", slug=slug)
    assert backend.count("checks", system_id=system["id"]) == len(rows), (
        "replaying must add no check row")


def test_a_system_holds_at_most_one_open_incident(founder, anon):
    slug = conftest.create_system(founder, open_after=1, close_after=1)
    times = conftest.probe_times(5, start=conftest.at_minutes(15, 0))
    conftest.record_checks(founder, slug, [
        (times[0], "down", None), (times[1], "down", None), (times[2], "down", None)])
    open_rows = [i for i in conftest.incidents_for(anon, slug) if i["resolved_at"] is None]
    assert len(open_rows) == 1 and len(conftest.incidents_for(anon, slug)) == 1, (
        "consecutive failing checks must keep one open incident")
    conftest.record_checks(founder, slug, [(times[3], "up", 40), (times[4], "down", None)])
    incidents = conftest.incidents_for(anon, slug)
    assert len(incidents) == 2, f"a failure after recovery opens a second incident: {incidents}"
    seqs = []
    for incident in sorted(incidents, key=lambda i: conftest.parse_time(i["opened_at"])):
        seqs += [int(e["seq"]) for e in conftest.incident_entries(anon, incident["ref"])]
    assert seqs == [1, 2, 3], f"seq must rise by one across the system's incidents: {seqs}"


def test_founder_note_appends_without_rewriting(founder, anon):
    slug = conftest.create_system(founder, open_after=2, close_after=3)
    conftest.record_checks(founder, slug, conftest.flapping_rows())
    ref = conftest.incidents_for(anon, slug)[0]["ref"]
    before = conftest.incident_entries(anon, ref)
    note = founder.post(f"/uptime/incidents/{ref}/notes",
                        json={"body": "Post-mortem: a flapping probe."})
    assert note.status_code in (200, 201), (
        "the founder must append a note: " + conftest.describe(note))
    after = conftest.incident_entries(anon, ref)
    assert after[:len(before)] == before, "a note must leave every earlier entry unchanged"
    assert (int(after[-1]["seq"]), after[-1]["kind"]) == (3, "note"), (
        f"the note must join the log as seq 3: {after[-1]}")
    empty = founder.post(f"/uptime/incidents/{ref}/notes", json={"body": ""})
    assert conftest.is_client_error(empty), (
        "an empty note must be rejected: " + conftest.describe(empty))


def test_incident_entries_cannot_be_edited_or_deleted(founder, anon):
    slug = conftest.create_system(founder, open_after=2, close_after=3)
    conftest.record_checks(founder, slug, conftest.flapping_rows())
    ref = conftest.incidents_for(anon, slug)[0]["ref"]
    before = conftest.incident_entries(anon, ref)
    for method, path in (("PATCH", f"/uptime/incidents/{ref}/entries/1"),
                         ("PUT", f"/uptime/incidents/{ref}/entries/1"),
                         ("DELETE", f"/uptime/incidents/{ref}/entries/1"),
                         ("DELETE", f"/uptime/incidents/{ref}")):
        response = founder.request(method, path, json={"body": "rewritten"})
        assert conftest.is_client_error(response), (
            f"{method} {path} must be rejected: " + conftest.describe(response))
    assert conftest.incident_entries(anon, ref) == before, (
        "a refused edit or delete must leave the log unchanged")


def test_concurrent_notes_receive_consecutive_seq(founder, anon, api_base):
    slug = conftest.create_system(founder, open_after=2, close_after=3)
    conftest.record_checks(founder, slug, conftest.flapping_rows())
    ref = conftest.incidents_for(anon, slug)[0]["ref"]
    token_header = founder.headers.get("Authorization")
    barrier = threading.Barrier(2)
    results = []

    def worker(text):
        with httpx.Client(base_url=api_base, timeout=30.0,
                          headers={"Authorization": token_header}) as c:
            barrier.wait()
            results.append(c.post(f"/uptime/incidents/{ref}/notes", json={"body": text}))

    threads = [threading.Thread(target=worker, args=(f"note {n}",)) for n in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert all(r.status_code in (200, 201) for r in results), (
        f"both concurrent notes must be accepted: {[r.status_code for r in results]}")
    seqs = [int(e["seq"]) for e in conftest.incident_entries(anon, ref)]
    assert seqs == [1, 2, 3, 4], f"concurrent notes must take consecutive seq values: {seqs}"


def test_notes_and_checks_are_denied_to_clients_and_anonymous(client, anon, backend):
    for caller in (client, anon):
        note = caller.post(f"/uptime/incidents/{conftest.SEEDED_INCIDENT}/notes",
                           json={"body": "not the studio"})
        assert note.status_code in (401, 403), (
            "a note from anybody but the founder must be denied: " + conftest.describe(note))
        check = caller.post(f"/systems/{conftest.PORTFOLIO_SLUG}/checks", json={
            "checked_at": conftest.at_minutes(16, 0), "status": "up", "response_ms": 1})
        assert check.status_code in (401, 403), (
            "a check from anybody but the founder must be denied: " + conftest.describe(check))
        system = caller.post("/systems", json={"slug": conftest.probe_slug("x"), "name": "X"})
        assert system.status_code in (401, 403), (
            "creating a system must be denied to anybody but the founder")
    portfolio = backend.one("systems", slug=conftest.PORTFOLIO_SLUG)
    assert backend.count("checks", system_id=portfolio["id"]) == 0, (
        "a denied check must write nothing")
    assert all(e["body"] != "not the studio"
               for e in conftest.incident_entries(anon, conftest.SEEDED_INCIDENT)), (
        "a denied note must write nothing")


def test_seeded_incident_record_is_public(anon, backend):
    console = backend.one("systems", slug=conftest.CONSOLE_SLUG)
    history = [r for r in backend.rows("checks", limit=500, system_id=console["id"])
               if str(r["checked_at"]).startswith("2026-09-01")]
    assert len(history) >= 6, "the console must hold the seeded 2026-09-01 checks behind its incident"
    rows = conftest.incidents_for(anon, conftest.CONSOLE_SLUG)
    seeded = [r for r in rows if r["ref"] == conftest.SEEDED_INCIDENT]
    assert seeded, f"the seeded console incident must be listed: {rows}"
    assert conftest.parse_time(seeded[0]["opened_at"]) == conftest.parse_time(conftest.SEEDED_INCIDENT_OPENED)
    assert conftest.parse_time(seeded[0]["resolved_at"]) == conftest.parse_time(conftest.SEEDED_INCIDENT_RESOLVED)
    entries = conftest.incident_entries(anon, conftest.SEEDED_INCIDENT)
    assert [e["kind"] for e in entries[:3]] == ["opened", "resolved", "note"], (
        f"the seeded incident must carry opened, resolved, then a note: {entries}")
    assert str(entries[2]["body"]).startswith(conftest.SEEDED_NOTE_PREFIX), (
        f"the seeded note must begin with the pinned text: {entries[2]}")
    listing = anon.get("/uptime/incidents").json()
    opened = [conftest.parse_time(r["opened_at"]) for r in listing]
    assert opened == sorted(opened, reverse=True), "the incident list must be newest first"


def test_public_build_index_lists_published_records_only(anon):
    slugs = _record_listing(anon)
    for slug in conftest.PUBLISHED_RECORDS.values():
        assert slug in slugs, f"the published record {slug} must be listed: {slugs}"
    assert conftest.DRAFT_RECORD not in slugs, "the draft record must be absent from the index"
    seeded = [s for s in slugs if s in conftest.PUBLISHED_RECORDS.values()]
    assert seeded == ["kestrel-storefront", "harbour-ledger", "lahn-clinic-hosting"], (
        f"the index must list the newest delivery first: {seeded}")


def test_build_index_filters_by_capability(anon):
    for capability, slug in conftest.PUBLISHED_RECORDS.items():
        response = anon.get("/builds", params={"capability": capability})
        assert response.status_code == 200, conftest.describe(response)
        rows = _shapes.items(response.json())
        assert rows and all(r.get("capability") == capability for r in rows), (
            f"filtering on {capability} must return only {capability} records: {rows}")
        assert slug in [r.get("slug") for r in rows]


def test_draft_record_answers_not_found(anon, site_direct):
    api = anon.get(f"/builds/{conftest.DRAFT_RECORD}")
    assert api.status_code == 404, (
        "the draft record must answer not-found publicly: " + conftest.describe(api))
    page = site_direct.get(f"/builds/{conftest.DRAFT_RECORD}")
    assert page.status_code == 404, (
        "the draft record's page must answer not-found: " + conftest.describe(page))
    assert "Aurora" not in page.text, "the not-found page must reveal nothing about the draft"


def test_record_detail_carries_dated_measurements_and_diagram(anon):
    kestrel = anon.get("/builds/kestrel-storefront")
    assert kestrel.status_code == 200, conftest.describe(kestrel)
    body = kestrel.json()
    measured = {(m.get("metric"), float(m.get("value")), str(m.get("measured_on"))[:10])
                for m in body.get("measurements") or []}
    assert ("lcp_ms", 640.0, "2026-08-20") in measured and ("cls", 0.01, "2026-08-20") in measured, (
        f"kestrel-storefront must carry lcp_ms 640 and cls 0.01 measured 2026-08-20: {measured}")
    assert str(body.get("delivered_on"))[:10] == conftest.DELIVERED_ON["kestrel-storefront"]
    assert str(body.get("started_on"))[:10] == conftest.STARTED_ON["kestrel-storefront"]
    harbour = anon.get("/builds/harbour-ledger").json()
    assert ("p95_api_ms", 180.0, "2026-07-14") in {
        (m.get("metric"), float(m.get("value")), str(m.get("measured_on"))[:10])
        for m in harbour.get("measurements") or []}, "harbour-ledger must carry p95_api_ms 180"
    assert str(harbour.get("started_on"))[:10] == conftest.STARTED_ON["harbour-ledger"]
    lahn = anon.get("/builds/lahn-clinic-hosting").json()
    assert not lahn.get("measurements"), "lahn-clinic-hosting must carry no measurement"
    assert str(lahn.get("started_on"))[:10] == conftest.STARTED_ON["lahn-clinic-hosting"]
    for record in (body, harbour, lahn):
        diagram = record.get("diagram")
        assert isinstance(diagram, list) and len(diagram) >= 4, (
            f"every seeded record must carry a diagram of at least four primitives: {diagram}")
        for primitive in diagram:
            assert primitive.get("kind") in conftest.PRIMITIVE_KINDS, primitive
            assert primitive.get("role") in conftest.PRIMITIVE_ROLES, primitive


def test_record_pages_state_client_and_missing_measurement(site):
    lahn = site.get("/builds/lahn-clinic-hosting")
    assert lahn.status_code == 200, conftest.describe(lahn)
    assert "Client withheld" in lahn.text, "a withheld client must show Client withheld"
    assert "Not yet measured" in lahn.text, "a record without measurement must say Not yet measured"
    harbour = site.get("/builds/harbour-ledger")
    assert conftest.HARBOUR_CLIENT in harbour.text, "harbour-ledger must show its client"
    assert "2026-07-14" in harbour.text or "14 Jul 2026" in harbour.text, (
        "a record figure must show the date it was measured")
    kestrel = site.get("/builds/kestrel-storefront")
    assert conftest.KESTREL_CLIENT in kestrel.text, "kestrel-storefront must show its client"


def test_founder_publishes_and_unpublishes_a_record(founder, anon, backend):
    slug = _create_record(founder)
    row = backend.one("build_records", slug=slug)
    assert row is not None and not row["published"], "a new record must be stored unpublished"
    assert row["published_at"] is None, "an unpublished record must carry no published_at"
    assert slug not in _record_listing(anon), "an unpublished record must not be listed"
    assert anon.get(f"/builds/{slug}").status_code == 404
    listed = founder.get("/studio/builds")
    assert listed.status_code == 200 and slug in _shapes.flatten(listed.json()), (
        "the founder's list must include unpublished records")
    published = founder.post(f"/builds/{slug}/publish")
    assert published.status_code == 200, conftest.describe(published)
    assert slug in _shapes.flatten(published.json()), "publishing must return the published record"
    assert slug in _record_listing(anon), "publishing must list the record"
    assert anon.get(f"/builds/{slug}").status_code == 200, "publishing must make the record readable"
    assert backend.one("build_records", slug=slug)["published_at"] is not None
    withdrawn = founder.post(f"/builds/{slug}/unpublish")
    assert withdrawn.status_code == 200, conftest.describe(withdrawn)
    assert slug in _shapes.flatten(withdrawn.json()), "unpublishing must return the unpublished record"
    assert slug not in _record_listing(anon), "unpublishing must withdraw the listing"
    assert anon.get(f"/builds/{slug}").status_code == 404, "unpublishing must withdraw the address"
    assert backend.one("build_records", slug=slug)["published_at"] is None


def test_record_with_invalid_diagram_or_taken_slug_is_rejected(founder, backend):
    bad_kind = conftest.build_record_body()
    bad_kind["diagram"][0]["kind"] = "polygon"
    no_role = conftest.build_record_body()
    no_role["diagram"][1].pop("role")
    taken = conftest.build_record_body(slug="harbour-ledger")
    for body, what in ((bad_kind, "an unknown primitive kind"),
                       (no_role, "a primitive without a role"),
                       (taken, "a taken slug")):
        response = founder.post("/builds", json=body)
        assert conftest.is_client_error(response), (
            f"{what} must be rejected: " + conftest.describe(response))
    for body in (bad_kind, no_role):
        assert backend.one("build_records", slug=body["slug"]) is None, (
            "a rejected record must save nothing")
    assert backend.count("build_records", slug="harbour-ledger") == 1


def test_measurements_are_validated(founder, anon, backend):
    slug = _create_record(founder)
    good = founder.post(f"/builds/{slug}/measurements", json={
        "metric": "uptime_percent", "value": 99.97, "measured_on": "2026-08-01",
        "source": "probe collector"})
    assert good.status_code in (200, 201), conftest.describe(good)
    record = backend.one("build_records", slug=slug)
    for body, what in (
            ({"metric": "fps", "value": 60, "measured_on": "2026-08-01", "source": "x"},
             "an unknown metric"),
            ({"metric": "lcp_ms", "value": -1, "measured_on": "2026-08-01", "source": "x"},
             "a negative value"),
            ({"metric": "lcp_ms", "value": 500, "measured_on": "yesterday", "source": "x"},
             "a value with no date")):
        response = founder.post(f"/builds/{slug}/measurements", json=body)
        assert conftest.is_client_error(response), (
            f"{what} must be rejected: " + conftest.describe(response))
    assert backend.count("measurements", build_record_id=record["id"]) == 1, (
        "rejected measurements must save nothing")
    denied = anon.post(f"/builds/{slug}/measurements", json={
        "metric": "lcp_ms", "value": 1, "measured_on": "2026-08-01", "source": "x"})
    assert denied.status_code in (401, 403), "measurements must be denied without a session"


def test_capability_links_open_the_latest_published_record(site, founder, app_base):
    links = _home_links(site)
    for label, capability in conftest.CAPABILITY_LINKS.items():
        target = _link_target(links, label, app_base)
        assert target == f"/builds/{conftest.PUBLISHED_RECORDS[capability]}", (
            f"{label} must open the latest published {capability} record; it opens {target}")
        assert conftest.DRAFT_RECORD not in target
    assert _link_target(links, "Status & uptime", app_base) == "/uptime"
    assert _link_target(links, "Talk to an engineer", app_base) == "/build-request"
    assert _link_target(links, "talk to an engineer_", app_base) == "/build-request"
    slug = _create_record(founder, capability="hosting", delivered_on="2026-10-01")
    assert founder.post(f"/builds/{slug}/publish").status_code == 200
    assert _link_target(_home_links(site), "See the stack", app_base) == f"/builds/{slug}", (
        "publishing a later hosting record must retarget See the stack")
    assert founder.post(f"/builds/{slug}/unpublish").status_code == 200
    assert _link_target(_home_links(site), "See the stack", app_base) != f"/builds/{slug}", (
        "an unpublished record must never be a capability link target")


def test_record_diagram_is_labelled_with_the_title(ui_page, app_base):
    ui_page.goto(f"{app_base}/builds/kestrel-storefront")
    drawing = ui_page.get_by_role("img", name="Diagram: Kestrel Storefront")
    assert drawing.count() >= 1, "the record drawing must be labelled Diagram: Kestrel Storefront"


def test_build_filters_are_plain_links_without_scripts(ui_page, app_base):
    ui_page.goto(f"{app_base}/builds")
    text = conftest.body_text(ui_page)
    for copy in conftest.BUILDS_COPY:
        assert copy in text, f"the library must show {copy!r}"
    link = ui_page.get_by_role("link", name="Software & Platforms").first
    href = link.get_attribute("href") or ""
    assert "capability=software" in href, f"the software filter must be a link to ?capability=software: {href}"
    link.click()
    ui_page.wait_for_load_state()
    assert "capability=software" in ui_page.url
    shown = conftest.body_text(ui_page)
    assert "Harbour Ledger" in shown and "Kestrel Storefront" not in shown, (
        "the software filter must narrow the list without scripts")


def test_every_public_route_renders_complete_copy_without_scripts(ui_page, app_base):
    expectations = {
        "/": conftest.HOME_COPY,
        "/about": conftest.ABOUT_COPY,
        "/uptime": conftest.UPTIME_COPY,
        "/impressum": conftest.IMPRESSUM_COPY,
        "/agb": conftest.AGB_COPY,
    }
    for route, copies in expectations.items():
        ui_page.goto(f"{app_base}{route}")
        text = conftest.body_text(ui_page)
        for copy in copies:
            assert copy in text, f"{route} must render {copy!r} with scripts off"
        if route not in conftest.LEGAL_ROUTES:
            assert "6421 555 0142" not in text, (
                f"the phone number must appear only on the legal pages, not on {route}")
    ui_page.goto(f"{app_base}/uptime")
    assert conftest.SEEDED_INCIDENT in ui_page.content() or "Vela Studio Console" in conftest.body_text(ui_page), (
        "the incident history must render with scripts off")


def test_home_diagrams_are_complete_and_described(ui_page, app_base):
    ui_page.goto(f"{app_base}/")
    for anchor in ("leistungen", "kontakt"):
        assert ui_page.locator(f"#{anchor}").count() == 1, f"the home page must carry the anchor #{anchor}"
    for label in conftest.DIAGRAM_LABELS:
        assert ui_page.get_by_role("img", name=label).count() >= 1, (
            f"the home page must carry a drawing described {label!r}")
    text = conftest.body_text(ui_page) + ui_page.content()
    for word in conftest.DIAGRAM_WORDS:
        assert word in text, f"the home drawings must carry the word {word!r}"
    for route in ("/", "/about", "/builds"):
        ui_page.goto(f"{app_base}{route}")
        missing = ui_page.evaluate(
            "Array.from(document.images).filter(i => !i.hasAttribute('alt')).length")
        assert missing == 0, f"every image on {route} must carry alternative text"


def test_each_public_route_carries_its_own_title_and_description(site):
    descriptions = {}
    for route, title in conftest.ROUTE_TITLES.items():
        page = site.get(route)
        assert page.status_code == 200, f"{route} must render: " + conftest.describe(page)
        found = re.search(r"<title[^>]*>(.*?)</title>", page.text, re.S | re.I)
        assert found and found.group(1).strip().replace("&amp;", "&") == title, (
            f"{route} must carry the title {title!r}; found {found.group(1) if found else None!r}")
        description = re.search(
            r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"'](.*?)[\"']", page.text, re.S | re.I)
        assert description, f"{route} must carry a description"
        descriptions[route] = description.group(1).strip()
        assert re.search(r"<link[^>]+rel=[\"']canonical[\"']", page.text, re.I), (
            f"{route} must declare a canonical address")
        image = re.search(
            r"<meta[^>]+property=[\"']og:image[\"'][^>]+content=[\"'](.*?)[\"']", page.text, re.I)
        assert image, f"{route} must declare a social preview image"
        resolved = site.get(image.group(1))
        assert resolved.status_code == 200, f"the preview image of {route} must resolve"
    assert len(set(descriptions.values())) == len(descriptions), (
        f"no two public routes may share a description: {descriptions}")
    assert conftest.HOME_DESCRIPTION_PHRASE in descriptions["/"]
    assert conftest.PREVIEW_ALT in site.get("/").text.replace("&amp;", "&"), (
        "the preview image must carry its alternative text")


def test_footer_lists_the_other_routes_only(site, app_base):
    for route in conftest.FOOTER_ROUTES:
        page = site.get(route)
        links = conftest.anchors(page.text)
        for label, target in conftest.FOOTER_LINKS.items():
            hits = [conftest.path_of(h, app_base) for h, t in links if t == label]
            if target == route:
                assert target not in hits, f"the footer on {route} must not link to {route}"
            else:
                assert target in hits, f"the footer on {route} must link {label} to {target}"


def test_back_links_return_home(site, app_base):
    for route in ("/about", "/uptime"):
        links = conftest.anchors(site.get(route).text)
        assert any(t.endswith("Back") and conftest.path_of(h, app_base) == "/" for h, t in links), (
            f"{route} must carry a back pill reading Back that returns to /")
    for route in conftest.LEGAL_ROUTES:
        links = conftest.anchors(site.get(route).text)
        assert any("Back to Vela Studio" in t and conftest.path_of(h, app_base) == "/" for h, t in links), (
            f"{route} must carry the back link Back to Vela Studio")


def test_every_internal_link_resolves(site, app_base):
    origin = httpx.URL(app_base)
    seen = set()
    for route in conftest.PUBLIC_ROUTES + ("/builds/harbour-ledger",):
        page = site.get(route)
        for href, _ in conftest.anchors(page.text):
            if href.startswith(("mailto:", "tel:", "#", "javascript:")):
                continue
            target = origin.join(href)
            if target.host != origin.host:
                continue
            path = target.copy_with(fragment=None)
            if str(path) in seen:
                continue
            seen.add(str(path))
            response = site.get(str(path))
            assert response.status_code < 400, (
                f"the internal link {href} on {route} must resolve; it answered "
                f"{response.status_code}")
    assert seen, "the public routes must carry internal links"
    allowed = {"anton-ferber.example.com", "portal.vela.example.com"}
    for route in ("/", "/about", "/uptime"):
        for href, _ in conftest.anchors(site.get(route).text):
            target = origin.join(href)
            if target.scheme in ("http", "https") and target.host != origin.host:
                assert target.host in allowed, (
                    f"{route} may link out only to the founder site and the portal; found {href}")


def test_legal_routes_load_no_script(page, app_base, site):
    for route in conftest.LEGAL_ROUTES:
        html = site.get(route).text
        assert "<script" not in html.lower(), f"{route} must carry no script element"
        scripts = []
        page.on("request", lambda r: scripts.append(r.url) if r.resource_type == "script" else None)
        page.goto(f"{app_base}{route}")
        page.wait_for_load_state("networkidle")
        assert scripts == [], f"{route} must load no script; it loaded {scripts}"


def test_no_route_sets_a_cookie(page, site, app_base, anon):
    for route in conftest.PUBLIC_ROUTES:
        response = site.get(route)
        assert "set-cookie" not in {k.lower() for k in response.headers}, (
            f"{route} must set no cookie")
    login = anon.post("/auth/login", json={
        "email": conftest.CLIENT_EMAIL, "password": conftest.APP_PASSWORD})
    assert "set-cookie" not in {k.lower() for k in login.headers}, "sign-in must set no cookie"
    for route in conftest.SCRIPTED_ROUTES:
        page.goto(f"{app_base}{route}")
        page.wait_for_load_state("networkidle")
    assert page.context.cookies() == [], (
        f"no route may leave a cookie behind: {page.context.cookies()}")
    assert page.evaluate("window.localStorage.length") == 0, (
        "the public routes must remember nothing about the visitor between pages")


def test_pages_request_nothing_from_other_origins(page, app_base):
    origin = httpx.URL(app_base)
    foreign = []

    def watch(request):
        url = httpx.URL(request.url)
        if url.scheme in ("http", "https") and (url.host, url.port) != (origin.host, origin.port):
            foreign.append(request.url)

    page.on("request", watch)
    for route in conftest.SCRIPTED_ROUTES + ("/impressum",):
        page.goto(f"{app_base}{route}")
        page.wait_for_load_state("networkidle")
    assert foreign == [], f"the site must request nothing from another origin: {foreign}"


def test_nothing_scrolls_sideways_at_a_narrow_viewport(page, app_base):
    page.set_viewport_size(conftest.NARROW_VIEWPORT)
    for route in conftest.PUBLIC_ROUTES:
        page.goto(f"{app_base}{route}")
        page.wait_for_load_state("networkidle")
        overflow = page.evaluate(
            "document.documentElement.scrollWidth - document.documentElement.clientWidth")
        assert overflow <= 1, f"{route} must not scroll sideways at 320 wide; overflow {overflow}"
        for label in conftest.FOOTER_LINKS:
            links = page.get_by_role("link", name=label, exact=True)
            for index in range(links.count()):
                box = links.nth(index).bounding_box()
                if box:
                    assert box["x"] >= 0 and box["x"] + box["width"] <= conftest.NARROW_VIEWPORT["width"] + 1, (
                        f"the footer link {label} on {route} must stay reachable at 320 wide")


def test_focus_ring_is_visible_on_keyboard_focus(page, app_base):
    page.goto(f"{app_base}/about")
    checked = 0
    for _ in range(6):
        page.keyboard.press("Tab")
        style = page.evaluate(
            "() => { const e = document.activeElement; if (!e || e === document.body) return null;"
            " const s = getComputedStyle(e); return {tag: e.tagName, outline: s.outlineStyle,"
            " width: parseFloat(s.outlineWidth) || 0, shadow: s.boxShadow}; }")
        if not style:
            continue
        checked += 1
        named = page.evaluate(
            "() => { const e = document.activeElement; return ((e.innerText || '') +"
            " (e.getAttribute('aria-label') || '') + (e.getAttribute('title') || '')).trim().length; }")
        assert named > 0, f"a focusable {style['tag']} must carry a label"
        visible = (style["outline"] != "none" and style["width"] >= 1) or style["shadow"] not in ("none", "")
        assert visible, f"a keyboard-focused {style['tag']} must show a visible focus ring: {style}"
    assert checked, "keyboard focus must reach interactive elements"


def test_footer_links_meet_the_contrast_bar(page, app_base):
    page.emulate_media(color_scheme="light")
    page.goto(f"{app_base}/")
    light_ground = page.evaluate("getComputedStyle(document.documentElement).backgroundColor")
    assert conftest.relative_luminance(conftest.parse_rgb(light_ground)) < 0.05, (
        "the site must stay dark even when the visitor prefers a light scheme")
    ground = page.evaluate("getComputedStyle(document.documentElement).backgroundColor")
    for label in ("About", "Legal Notice", "Terms", "Status/Uptime"):
        colour = page.get_by_role("link", name=label, exact=True).last.evaluate(
            "e => getComputedStyle(e).color")
        ratio = conftest.contrast(colour, ground)
        assert ratio >= conftest.CONTRAST_FLOOR, (
            f"the footer link {label} must reach 4.5:1 against the ground; it reaches {ratio:.2f}")


def test_reduced_motion_shows_every_word_revealed(browser_page, app_base):
    browser_page.goto(f"{app_base}/")
    browser_page.wait_for_load_state("networkidle")
    states = browser_page.locator(
        "p", has_text="We build privacy-first software").first.evaluate(
        "p => Array.from(p.querySelectorAll('*')).concat([p]).map(e => {"
        " const s = getComputedStyle(e); return [s.opacity, s.filter]; })")
    for opacity, filt in states:
        assert float(opacity) == 1.0 and filt in ("none", ""), (
            f"under reduced motion every word must show finished: opacity {opacity}, filter {filt}")
    looping = browser_page.evaluate(
        "document.getAnimations().filter(a => a.playState === 'running' &&"
        " a.effect && a.effect.getTiming().iterations === Infinity).length")
    assert looping == 0, f"under reduced motion no animation may loop; {looping} running"
    drawn = browser_page.evaluate(
        "Array.from(document.querySelectorAll('svg [stroke-dashoffset], svg *'))"
        ".filter(e => { const s = getComputedStyle(e); return parseFloat(s.opacity) < 1 ||"
        " (s.strokeDashoffset && parseFloat(s.strokeDashoffset) > 0.5); }).length")
    assert drawn == 0, f"under reduced motion every diagram must be complete; {drawn} shapes are not"


def test_shared_position_lands_on_the_named_section(page, app_base):
    page.goto(f"{app_base}{conftest.POSITION_ADDRESS}")
    page.wait_for_load_state("networkidle")
    assert conftest.poll_until(lambda: conftest.in_viewport(page, conftest.POSITION_HEADING), 15), (
        "a shared managed-hosting address must land on that card")


def test_reduced_motion_position_lands_revealed(browser_page, app_base):
    browser_page.goto(f"{app_base}{conftest.POSITION_ADDRESS}")
    browser_page.wait_for_load_state("networkidle")
    assert conftest.poll_until(
        lambda: conftest.in_viewport(browser_page, conftest.POSITION_HEADING), 15), (
        "under reduced motion a shared address must land on the named section")
    states = browser_page.locator("p", has_text="Your workload runs on").first.evaluate(
        "p => Array.from(p.querySelectorAll('*')).concat([p]).map(e => getComputedStyle(e).opacity)")
    assert all(float(o) == 1.0 for o in states), "the named section must be fully revealed"


def test_status_board_renders_tiles_cards_and_history(page, app_base, founder):
    overdue = conftest.create_system(founder, stem="overdue-system")
    conftest.record_checks(founder, overdue, [(conftest.at_minutes(9, 0), "up", 40)])
    page.goto(f"{app_base}/uptime")
    assert conftest.poll_until(lambda: "Awaiting checks" in conftest.body_text(page), 20), (
        "the portfolio card must read Awaiting checks")
    text = conftest.body_text(page)
    for copy in conftest.UPTIME_TILE_LABELS + conftest.UPTIME_CARD_LABELS:
        assert copy in text, f"the status board must show {copy!r}"
    assert "Operational" in text and "Unknown" in text, "status pills must state their status in words"
    assert re.search(r"\b\d+/\d+\b", text), "the Operational tile must read up count slash total"
    assert "Incident history" in text
    assert "Due now" in text, "an overdue next check must read Due now"
    with httpx.Client(base_url=app_base + "/api", timeout=30.0) as api:
        projects = conftest.feed(api)["projects"]
    numeric = [float(p["uptimePercent"]) for p in projects if p["uptimePercent"] is not None]
    mean = f"{sum(numeric) / len(numeric):.2f}"
    assert mean in text, f"the Average uptime tile must show the mean {mean} to two decimals"
    figures = page.get_by_text(mean, exact=True).first.evaluate(
        "e => getComputedStyle(e).fontVariantNumeric + ' ' + getComputedStyle(e).fontFeatureSettings")
    assert "tabular-nums" in figures or "tnum" in figures, (
        f"changing status numbers must use figures of equal width; computed {figures!r}")
    titles = page.locator("[title]").evaluate_all("els => els.map(e => e.getAttribute('title'))")
    assert any(re.match(conftest.BAR_TITLE_RE, str(t)) for t in titles), (
        f"each bar must carry a title like Operational at 1 Sept 2026, 15:38; saw {titles[:5]}")
    portal = page.get_by_role("link", name=re.compile("Open customer portal")).first
    assert portal.get_attribute("target") == "_blank", "the portal link must open a new tab"
    assert "noreferrer" in (portal.get_attribute("rel") or ""), "the portal link must pass no referrer"
    assert page.locator("h2").count() >= 1, "a heading level must sit between the title and each system"
    assert page.locator("[aria-live], [role='status']").count() >= 1, (
        "the board must announce loading and failure")
    link = page.locator(f"a[href*='/uptime/incidents/{conftest.SEEDED_INCIDENT}']")
    assert link.count() >= 1, "the incident history must link to the seeded incident page"
    assert page.locator("[aria-label^='Recent uptime history for']").count() >= 6, (
        "each bar strip must be described as Recent uptime history for its system")


def test_portrait_stand_in_is_named_until_an_upload(ui_page, app_base, anon):
    assert anon.get("/portrait").status_code == 404, (
        "with no portrait uploaded GET /api/portrait must answer not-found")
    ui_page.goto(f"{app_base}/about")
    assert ui_page.get_by_role("img", name="Portrait placeholder").count() >= 1, (
        "the founder page must name the drawn stand-in Portrait placeholder")


def test_founder_uploads_a_portrait_to_the_bucket(founder, client, anon, store, backend, site):
    payload = conftest.png_payload()
    response = founder.post("/studio/portrait",
                            files={"portrait": ("anton.png", payload, "image/png")})
    body = _accepted(response, "a portrait upload")
    key = conftest.PORTRAIT_KEY_TEMPLATE.format(digest=conftest.sha256_hex(payload), ext="png")
    assert conftest.field(body, "object_key") == key, (
        f"the portrait must be stored at {key}: {body}")
    assert store.exists(key), f"the portrait bytes must exist in the bucket at {key}"
    served = anon.get("/portrait", follow_redirects=True)
    assert served.status_code == 200 and served.content == payload, (
        "GET /api/portrait must serve the newest portrait to anyone")
    assert backend.one("portraits", object_key=key) is not None
    assert conftest.PORTRAIT_ALT in site.get("/about").text, (
        "the portrait must carry its alternative text")
    rejected = founder.post("/studio/portrait",
                            files={"portrait": ("anton.png", b"not an image", "image/png")})
    assert conftest.is_client_error(rejected), "a non-image portrait must be rejected"
    denied = client.post("/studio/portrait",
                         files={"portrait": ("x.png", conftest.png_payload(), "image/png")})
    assert denied.status_code in (401, 403), "a client must be denied the portrait upload"
    assert anon.get("/portrait", follow_redirects=True).content == payload, (
        "refused uploads must leave the shown portrait unchanged")


def test_page_views_are_recorded_without_identity(anon, founder, client, backend, site):
    before = backend.count("page_views")
    assert site.get("/impressum").status_code == 200
    assert conftest.poll_until(lambda: backend.count("page_views") > before), (
        "rendering a public route must record a page view")
    middle = backend.count("page_views")
    recorded = anon.post("/page-views", json={"route": "/agb"})
    assert recorded.status_code in (200, 201), conftest.describe(recorded)
    assert conftest.poll_until(lambda: backend.count("page_views") > middle), (
        "POST /api/page-views must record one row")
    row = backend.rows("page_views", limit=1, route="/agb")[0]
    assert set(row) <= set(conftest.PAGE_VIEW_COLUMNS), (
        f"a page view row must hold only the route and the time: {sorted(row)}")
    log = founder.get("/page-views")
    assert log.status_code == 200 and isinstance(log.json(), list), conftest.describe(log)
    stamps = [conftest.parse_time(r.get("viewed_at")) for r in log.json() if r.get("viewed_at")]
    assert stamps == sorted(stamps, reverse=True), "the page-view log must be newest first"
    for caller in (client, anon):
        assert caller.get("/page-views").status_code in (401, 403), (
            "only the founder may read the page-view log")


def test_studio_endpoints_are_denied_to_clients(client, backend):
    for method, path, body in (
            ("GET", "/build-requests", None),
            ("GET", "/studio/builds", None),
            ("GET", "/page-views", None),
            ("POST", "/builds", conftest.build_record_body()),
            ("POST", "/builds/harbour-ledger/unpublish", None),
            ("POST", f"/build-requests/{conftest.SECOND_SEEDED_REQUEST}/status", {"status": "declined"})):
        response = client.request(method, path, json=body)
        assert response.status_code in (401, 403), (
            f"a client must be denied {method} {path}: " + conftest.describe(response))
    assert backend.one("build_records", slug="harbour-ledger")["published"], (
        "a denied unpublish must leave the record published")
    assert backend.one("build_requests", reference=conftest.SECOND_SEEDED_REQUEST)["status"] == "new"


def test_studio_endpoints_are_denied_without_a_session(anon):
    for method, path in (("GET", "/build-requests"), ("GET", "/studio/builds"),
                         ("POST", "/builds"), ("POST", "/studio/portrait"),
                         ("GET", "/build-requests/mine")):
        response = anon.request(method, path)
        assert response.status_code in (401, 403), (
            f"an anonymous caller must be denied {method} {path}: " + conftest.describe(response))


def test_account_page_sends_a_signed_out_visitor_to_login(page, app_base, site):
    for route in ("/account", "/studio"):
        html = site.get(route).text
        for private in (conftest.SEEDED_REQUEST, conftest.CLIENT_EMAIL):
            assert private not in html, f"{route} must carry no private data in its markup"
        page.goto(f"{app_base}{route}")
        assert conftest.poll_until(lambda: page.url.split("?")[0].endswith("/login"), 15), (
            f"a signed-out visitor opening {route} must be sent to /login; ended at {page.url}")


def test_list_endpoints_return_top_level_arrays(anon, founder):
    for client, path in ((anon, "/builds"), (anon, "/uptime/incidents"),
                         (founder, "/build-requests"), (founder, "/page-views"),
                         (founder, "/studio/builds")):
        response = client.get(path)
        assert response.status_code == 200 and isinstance(response.json(), list), (
            f"{path} must return a top-level JSON array: " + conftest.describe(response))


def test_legal_notice_marks_german_terms(ui_page, app_base):
    ui_page.goto(f"{app_base}/impressum")
    assert ui_page.locator("[lang='de']").count() >= 1, (
        "German legal terms in the English notice must be marked as German")


def test_seed_is_idempotent(backend):
    for slug in conftest.SEEDED_SYSTEM_SLUGS:
        row = backend.one("systems", slug=slug)
        assert (row["interval_seconds"], row["open_after"], row["close_after"]) == (300, 3, 2), (
            f"seeded system {slug} must use interval 300 with thresholds 3 and 2: {row}")
    aurora = backend.one("build_records", slug=conftest.DRAFT_RECORD)
    assert str(aurora["started_on"])[:10] == "2026-07-01" and aurora["client_name"] == "Aurora Personal"
    for email in (conftest.FOUNDER_EMAIL, conftest.CLIENT_EMAIL, conftest.CLIENT2_EMAIL):
        assert backend.count("accounts", email=email) == 1, f"{email} must be seeded exactly once"
    for slug in conftest.SEEDED_SYSTEM_SLUGS:
        assert backend.count("systems", slug=slug) == 1, f"system {slug} must be seeded exactly once"
    for slug in list(conftest.PUBLISHED_RECORDS.values()) + [conftest.DRAFT_RECORD]:
        assert backend.count("build_records", slug=slug) == 1, f"record {slug} must be seeded exactly once"
    for reference in (conftest.SEEDED_REQUEST, conftest.SECOND_SEEDED_REQUEST):
        assert backend.count("build_requests", reference=reference) == 1
    assert backend.count("incidents", ref=conftest.SEEDED_INCIDENT) == 1
    draft = backend.one("build_records", slug=conftest.DRAFT_RECORD)
    assert not draft["published"] and str(draft["delivered_on"])[:10] == "2026-09-05"
    titles = dict(conftest.RECORD_TITLES)
    titles[conftest.DRAFT_RECORD] = "Aurora Payroll Portal"
    for slug, title in titles.items():
        assert backend.one("build_records", slug=slug)["title"] == title, f"record {slug} must be titled {title}"
    for slug, names in (("harbour-ledger", ("Python", "PostgreSQL")),
                        ("kestrel-storefront", ("Python", "Alpine.js")),
                        ("lahn-clinic-hosting", ("PostgreSQL",))):
        stack = str(backend.one("build_records", slug=slug)["stack"])
        for name in names:
            assert name in stack, f"the {slug} stack must list {name}: {stack}"
    console = backend.one("systems", slug=conftest.CONSOLE_SLUG)
    for minute, status in ((15, "up"), (20, "down"), (25, "down"), (30, "down"), (35, "up"), (40, "up")):
        moment = conftest.parse_time(f"2026-09-01T14:{minute:02d}:00Z")
        row = backend.one("checks", system_id=console["id"], checked_at=moment)
        assert row is not None and row["status"] == status, (
            f"the console must hold a seeded {status} check at 14:{minute:02d} on 2026-09-01: {row}")


def test_schema_holds_the_named_tables_and_columns(backend):
    expected = {
        "accounts": {"email", "role"},
        "systems": {"slug", "name", "position", "interval_seconds", "open_after", "close_after"},
        "checks": {"checked_at", "status", "response_ms"},
        "incidents": {"ref", "opened_at", "resolved_at"},
        "incident_entries": {"seq", "kind", "body", "recorded_at"},
        "build_records": {"slug", "title", "capability", "stack", "delivered_on",
                          "client_visible", "diagram", "published", "published_at"},
        "measurements": {"metric", "value", "measured_on", "source"},
        "build_requests": {"reference", "contact_email", "capabilities", "rules_version",
                           "indicative_minor", "currency", "status", "status_changed_at"},
        "attachments": {"object_key", "content_type", "byte_size", "sha256", "original_name"},
        "page_views": {"route", "viewed_at"},
        "portraits": {"object_key", "content_type", "uploaded_at"},
    }
    for table, columns in expected.items():
        rows = backend.query(
            "select column_name from information_schema.columns where table_name = %s",
            (table,))
        found = {r["column_name"] for r in rows}
        assert found, f"the table {table} must exist"
        assert columns <= found, f"{table} must carry {sorted(columns - found)}"
    kinds = {r["content_type"] for r in backend.rows("attachments", limit=200)}
    assert kinds <= {"application/pdf", "image/png", "image/jpeg"}, kinds


def test_downloaded_assets_carry_no_credential(page, app_base):
    secrets = [os.environ.get(name) for name in
               ("STORAGE_SECRET_KEY", "STORAGE_ACCESS_KEY")]
    secrets = [s for s in secrets if s] + ["deku-local-dev"]
    bodies = []

    def keep(response):
        if response.request.resource_type in ("script", "stylesheet", "document"):
            bodies.append((response.url, response.text()))

    page.on("response", keep)
    for route in conftest.SCRIPTED_ROUTES:
        page.goto(f"{app_base}{route}")
        page.wait_for_load_state("networkidle")
    assert bodies, "the public routes must download at least their documents"
    for url, text in bodies:
        for secret in secrets:
            assert secret not in text, f"{url} must carry no storage secret or database password"


def test_form_submission_accepts_both_capability_shapes(anon, backend):
    repeated = conftest.request_body(("software", "hosting"))
    fields = conftest.form_fields(repeated)
    fields["capabilities"] = ["software", "hosting"]
    first = anon.post("/build-requests", data=fields)
    created = _accepted(first, "a form submission with repeated capabilities")
    row = _request_row(backend, conftest.reference_of(created))
    assert int(row["indicative_minor"]) == conftest.figure(("software", "hosting"), "managed", "eu", "standard")
    joined = conftest.request_body(("software", "hosting"))
    second = anon.post("/build-requests", data=conftest.form_fields(joined))
    created = _accepted(second, "a form submission with comma-separated capabilities")
    row = _request_row(backend, conftest.reference_of(created))
    assert int(row["indicative_minor"]) == conftest.figure(("software", "hosting"), "managed", "eu", "standard")


def test_a_rendered_page_records_exactly_one_view(page, app_base, backend):
    before = backend.count("page_views", route="/about")
    page.goto(f"{app_base}/about")
    page.wait_for_load_state("networkidle")
    conftest.settle()
    after = backend.count("page_views", route="/about")
    assert after == before + 1, (
        f"one render of /about must record exactly one page view; saw {after - before}")


def test_drawings_keep_their_strokes_in_forced_colours(page, app_base):
    page.emulate_media(forced_colors="active")
    page.goto(f"{app_base}/")
    page.wait_for_load_state("networkidle")
    invisible = page.evaluate(
        "Array.from(document.querySelectorAll('[role=img] rect, [role=img] path'))"
        ".filter(e => { const s = getComputedStyle(e); return (s.stroke === 'none' ||"
        " s.stroke === 'transparent' || s.stroke === 'rgba(0, 0, 0, 0)') && (s.fill === 'none'"
        " || s.fill === 'rgba(0, 0, 0, 0)'); }).length")
    assert invisible == 0, f"in forced colours every drawn shape must keep a stroke; {invisible} vanish"


def test_modifier_click_on_an_in_page_link_opens_a_new_tab(page, app_base):
    page.goto(f"{app_base}/")
    page.wait_for_load_state("networkidle")
    link = page.locator("a[href^='#']").first
    assert link.count() == 1, "the home page must carry an in-page link"
    with page.context.expect_page(timeout=15000) as opened:
        link.click(modifiers=["ControlOrMeta"])
    assert opened.value is not None, "a modified click on an in-page link must open a new tab"
    assert page.url.split("#")[0].rstrip("/") == app_base.rstrip("/"), (
        "a modified click must leave the current page where it is")


def test_type_scale_matches_the_pinned_sizes(page, app_base):
    for width, sizes in conftest.TYPE_SCALE.items():
        page.set_viewport_size({"width": width, "height": 900})
        page.goto(f"{app_base}/")
        page.wait_for_load_state("networkidle")
        found = {
            "hero": conftest.font_px(page, page.get_by_text("Software built in Germany.", exact=True).first),
            "statement": conftest.font_px(page, page.locator("p", has_text="We build privacy-first software").first),
            "card_body": conftest.font_px(page, page.locator("p", has_text="SaaS products, internal tools").first),
            "contact": conftest.font_px(page, page.get_by_text("talk to an engineer_").first),
        }
        if "card_heading" in sizes:
            found["card_heading"] = conftest.font_px(
                page, page.get_by_role("heading", name="Software & Platforms").first)
        lede = conftest.font_px(page, page.locator("p", has_text="We write production software").first)
        expected_lede = 18.0 if width == 1440 else 16.0
        assert abs(lede - expected_lede) <= conftest.TYPE_TOLERANCE, (
            f"at {width} wide the hero lede must be {expected_lede}px; it is {lede}px")
        for role, expected in sizes.items():
            assert abs(found[role] - expected) <= conftest.TYPE_TOLERANCE, (
                f"at {width} wide the {role} must be {expected}px; it is {found[role]}px")
        eyebrow_px = conftest.font_px(page, page.get_by_text("01 - Philosophy").first)
        assert abs(eyebrow_px - 11.0) <= conftest.TYPE_TOLERANCE, f"an eyebrow must stay 11px at {width} wide"
        body = float(page.evaluate("parseFloat(getComputedStyle(document.body).fontSize)"))
        assert abs(body - 16.0) <= conftest.TYPE_TOLERANCE, f"body copy must stay 16px at {width} wide"
    page.set_viewport_size(conftest.WIDE_VIEWPORT)
    page.goto(f"{app_base}/")
    eyebrow = page.get_by_text("01 - Philosophy").first
    assert abs(conftest.font_px(page, eyebrow) - 11.0) <= conftest.TYPE_TOLERANCE
    assert "Geist Mono" in conftest.font_family(page, eyebrow), "labels must be set in Geist Mono"
    assert "Geist" in conftest.font_family(page, page.locator("p", has_text="We build privacy-first").first)
    assert "Geist Mono" not in conftest.font_family(
        page, page.locator("p", has_text="We build privacy-first").first), "sentences must be set in Geist"
    for label in ("Marburg, DE", "02"):
        size = conftest.font_px(page, page.get_by_text(label, exact=True).first)
        assert abs(size - 12.0) <= conftest.TYPE_TOLERANCE, f"the mono label {label!r} must be 12px; it is {size}px"
    section = conftest.font_px(page, page.get_by_role("heading", name="What we build").first)
    assert abs(section - 48.0) <= conftest.TYPE_TOLERANCE, f"What we build must be 48px; it is {section}px"
    page.goto(f"{app_base}/impressum")
    assert abs(conftest.font_px(page, page.locator("p", has_text="Ketzerbach 21").first) - 15.0) <= conftest.TYPE_TOLERANCE
    assert abs(conftest.font_px(page, page.get_by_role("heading", name="Provider").first) - 20.0) <= conftest.TYPE_TOLERANCE
    page.goto(f"{app_base}/uptime")
    assert conftest.poll_until(lambda: "Vela Studio Finance" in conftest.body_text(page), 20)
    heading = conftest.font_px(page, page.get_by_role("heading", name="Live reliability, shown in public.").first)
    assert heading <= 64.0 + conftest.TYPE_TOLERANCE, f"the status heading must be at most 64px; it is {heading}px"
    assert abs(conftest.font_px(page, page.get_by_role("heading", name="Vela Studio Finance").first) - 19.0) <= conftest.TYPE_TOLERANCE
    for label in ("Uptime", "Operational"):
        size = conftest.font_px(page, page.get_by_text(label, exact=True).first)
        assert abs(size - 10.0) <= conftest.TYPE_TOLERANCE, f"the status label {label!r} must be 10px; it is {size}px"
    page.goto(f"{app_base}/about")
    back = conftest.font_px(page, page.get_by_text("Back", exact=True).first)
    assert abs(back - 11.0) <= conftest.TYPE_TOLERANCE, f"the back pill label must be 11px; it is {back}px"
    page.goto(f"{app_base}/uptime")
    assert conftest.poll_until(lambda: "Vela Studio Finance" in conftest.body_text(page), 20)
    tile_label = conftest.font_px(page, page.get_by_text("Average uptime", exact=False).first)
    assert abs(tile_label - 10.0) <= conftest.TYPE_TOLERANCE, f"a status tile label must be 10px; it is {tile_label}px"
    footer_link = conftest.font_px(page, page.locator("footer a").first)
    assert abs(footer_link - 12.0) <= conftest.TYPE_TOLERANCE, f"a footer link must be 12px; it is {footer_link}px"
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{app_base}/impressum")
    assert abs(conftest.font_px(page, page.locator("p", has_text="Ketzerbach 21").first) - 14.0) <= conftest.TYPE_TOLERANCE, (
        "legal body text must drop to 14px on a phone")
    assert abs(conftest.font_px(page, page.get_by_role("heading", name="Provider").first) - 17.0) <= conftest.TYPE_TOLERANCE, (
        "a legal clause heading must drop to 17px on a phone")


def test_status_board_states_failure_and_empty_feeds(page, app_base):
    page.route("**/api/uptime/projects*", lambda route: route.fulfill(
        status=503, content_type="application/json", body="{}"))
    page.goto(f"{app_base}/uptime")
    assert conftest.poll_until(lambda: "Status temporarily unavailable" in conftest.body_text(page), 20), (
        "a failed feed must replace the list with the failure block")
    text = conftest.body_text(page)
    assert "The live status feed could not be loaded right now." in text
    assert "The uptime feed is unavailable." in text, "a failure without a message must use the default body"
    assert "Average uptime" not in text, "a failed feed must remove the tiles"
    assert page.locator("[role='status']").count() >= 1, "the failure block must be announced"
    feedback = conftest.font_px(page, page.get_by_text("Status temporarily unavailable").first)
    assert abs(feedback - 20.0) <= conftest.TYPE_TOLERANCE, f"a feedback heading must be 20px; it is {feedback}px"
    page.unroute("**/api/uptime/projects*")
    page.route("**/api/uptime/projects*", lambda route: route.fulfill(
        status=503, content_type="application/json",
        body='{"error": {"message": "Collector maintenance in progress."}}'))
    page.goto(f"{app_base}/uptime")
    assert conftest.poll_until(lambda: "Collector maintenance in progress." in conftest.body_text(page), 20), (
        "a failed feed with its own message must show that message")
    page.unroute("**/api/uptime/projects*")
    page.route("**/api/uptime/projects*", lambda route: route.fulfill(
        status=200, content_type="application/json",
        body='{"data": {"nextCheckAt": null, "projects": []}}'))
    page.goto(f"{app_base}/uptime")
    assert conftest.poll_until(lambda: "No systems available" in conftest.body_text(page), 20), (
        "an empty feed must show the empty block")
    text = conftest.body_text(page)
    assert "No monitored systems are currently visible." in text
    assert "The monitoring feed returned an empty project scope." in text
    assert page.locator("[role='status'], [aria-live]").count() >= 1, "the empty block must be announced"
    assert "Average uptime" not in text, "an empty feed must show no tiles"


def test_incident_history_shows_an_ongoing_incident(page, app_base, founder, anon):
    slug = conftest.create_system(founder, open_after=1, close_after=2)
    conftest.record_checks(founder, slug, [(conftest.at_minutes(17, 0), "down", None)])
    incident = conftest.incidents_for(anon, slug)[0]
    assert incident["resolved_at"] is None
    page.goto(f"{app_base}/uptime")
    row = page.locator(f"a[href*='/uptime/incidents/{incident['ref']}']").first
    assert conftest.poll_until(lambda: row.count() == 1, 20), "the open incident must be listed"
    container = row.locator("xpath=ancestor::*[self::li or self::tr or self::article][1]")
    assert "Ongoing" in conftest.RenderedText(container.inner_text() if container.count() else conftest.body_text(page)), (
        "an unresolved incident must read Ongoing in the incident history")


def test_hover_transitions_stay_under_a_fifth_of_a_second(page, app_base):
    for route in ("/", "/about", "/uptime"):
        page.goto(f"{app_base}{route}")
        page.wait_for_load_state("networkidle")
        longest = page.evaluate(
            "() => Math.max(0, ...Array.from(document.querySelectorAll('a, button')).flatMap(e =>"
            " getComputedStyle(e).transitionDuration.split(',').map(v => parseFloat(v) *"
            " (v.trim().endsWith('ms') ? 0.001 : 1))))")
        assert longest <= conftest.HOVER_CEILING_SECONDS + 1e-6, (
            f"no hover transition on {route} may exceed a fifth of a second; the longest is {longest}s")


def test_home_page_loads_without_layout_shift(page, app_base):
    page.add_init_script(
        "window.__shift = 0; new PerformanceObserver(l => { for (const e of l.getEntries())"
        " { if (!e.hadRecentInput) window.__shift += e.value; } })"
        ".observe({type: 'layout-shift', buffered: true});")
    page.goto(f"{app_base}/")
    page.wait_for_load_state("networkidle")
    conftest.settle()
    shift = page.evaluate("window.__shift")
    assert shift < conftest.LAYOUT_SHIFT_CEILING, (
        f"the arriving font must not move a line; cumulative layout shift was {shift}")


def test_the_portrait_is_the_only_photograph(page, app_base):
    photos = []

    def watch(request):
        path = request.url.split("?")[0].lower()
        if request.resource_type == "image" and path.endswith(conftest.PHOTO_EXTENSIONS):
            if "/api/portrait" not in path and "favicon" not in path and "icon" not in path.rsplit("/", 1)[-1]:
                photos.append(request.url)

    page.on("request", watch)
    for route in conftest.SCRIPTED_ROUTES:
        page.goto(f"{app_base}{route}")
        page.wait_for_load_state("networkidle")
    assert photos == [], f"the uploaded portrait must be the only photograph; the pages loaded {photos}"
