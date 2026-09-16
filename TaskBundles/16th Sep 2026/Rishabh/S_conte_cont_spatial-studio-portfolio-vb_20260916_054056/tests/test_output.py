from __future__ import annotations

import _shapes
import conftest


def _create_case(editor, number, slug, client_name="Probe Client",
                 title="Probe Case"):
    response = editor.post("/cases", json={
        "slug": slug,
        "number": number,
        "client": client_name,
        "title": title,
        "brief": "A probe case created by the grading session.",
        "result": "The probe case reached its result paragraph.",
    })
    assert response.status_code in (200, 201), (
        "creating a case as the editor should succeed: "
        + conftest.describe(response))
    return response.json()


def _case_id(case):
    for key in ("id", "case_id", "caseId"):
        if key in case:
            return case[key]
    raise AssertionError(f"created case carries no id field: {case}")


def _numbers(payload):
    out = []
    for row in _shapes.items(payload):
        value = row.get("number")
        if value is not None:
            out.append(str(value))
    return out


def _slugs(payload):
    return [str(row.get("slug")) for row in _shapes.items(payload)]


def test_health_endpoint_reports_ready(anon):
    response = anon.get("/health")
    assert response.status_code == 200, (
        "GET /api/health must answer 200 once the app is ready: "
        + conftest.describe(response))


def test_published_cases_are_listed_for_a_visitor(anon):
    response = anon.get("/cases")
    assert response.status_code == 200, (
        "GET /api/cases must be readable without signing in: "
        + conftest.describe(response))
    numbers = _numbers(response.json())
    for expected in conftest.SEEDED_CASE_NUMBERS:
        assert expected in numbers, (
            f"seeded published case {expected} is missing from the public "
            f"listing; listing carried {numbers}: " + conftest.describe(response))


def test_case_detail_returns_its_sections_and_result(anon):
    listing = anon.get("/cases")
    assert listing.status_code == 200, (
        "the public case listing must answer before a detail can be opened: "
        + conftest.describe(listing))
    rows = _shapes.items(listing.json())
    assert rows, (
        "the seeded corpus pins seven published cases, so the listing must not "
        "be empty: " + conftest.describe(listing))
    slug = rows[0].get("slug")
    detail = anon.get(f"/cases/{slug}")
    assert detail.status_code == 200, (
        f"a published case must resolve at /api/cases/{slug} for a signed-out "
        "visitor: " + conftest.describe(detail))
    flat = _shapes.flatten(detail.json())
    assert "result" in flat, (
        f"the case detail for {slug} must carry its result paragraph; body "
        f"excerpt: {detail.text[:400]}")


def test_solutions_listing_carries_three_product_lines(anon):
    response = anon.get("/solutions")
    assert response.status_code == 200, (
        "GET /api/solutions must be readable without signing in: "
        + conftest.describe(response))
    slugs = _slugs(response.json())
    for expected in conftest.SOLUTION_SLUGS:
        assert expected in slugs, (
            f"seeded product line {expected} is missing; listing carried "
            f"{slugs}: " + conftest.describe(response))


def test_solution_detail_carries_exactly_three_mechanism_steps(anon):
    for slug in conftest.SOLUTION_SLUGS:
        response = anon.get(f"/solutions/{slug}")
        assert response.status_code == 200, (
            f"the product line {slug} must resolve at /api/solutions/{slug}: "
            + conftest.describe(response))
        payload = response.json()
        sections = payload.get("sections") or payload.get("solution_sections") or []
        mechanisms = [s for s in sections if str(s.get("kind")) == "mechanism"]
        features = [s for s in sections if str(s.get("kind")) == "feature"]
        assert len(mechanisms) == 3, (
            f"the product line {slug} must carry exactly three mechanism steps, "
            f"found {len(mechanisms)}: " + conftest.describe(response))
        assert 6 <= len(features) <= 9, (
            f"the product line {slug} must carry between six and nine features, "
            f"found {len(features)}: " + conftest.describe(response))


def test_solutions_path_redirects_to_the_first_product_line(site_direct, site):
    direct = site_direct.get("/solutions/")
    assert direct.status_code in (301, 302, 303, 307, 308), (
        "/solutions/ must redirect rather than render a listing page: "
        + conftest.describe(direct))
    landed = site.get("/solutions/")
    assert landed.status_code == 200, (
        "following /solutions/ must land on a real page: "
        + conftest.describe(landed))
    assert "cirrus" in str(landed.url).lower(), (
        "/solutions/ must land on the first product line at /cirrus/, landed on "
        f"{landed.url}: " + conftest.describe(landed))


def test_services_carry_four_disciplines_with_four_bullets_each(anon):
    response = anon.get("/services")
    assert response.status_code == 200, (
        "GET /api/services must be readable without signing in: "
        + conftest.describe(response))
    rows = _shapes.items(response.json())
    anchors = [str(row.get("anchor")) for row in rows]
    for expected in conftest.SERVICE_ANCHORS:
        assert expected in anchors, (
            f"service discipline {expected} is missing; anchors carried "
            f"{anchors}: " + conftest.describe(response))
    for row in rows:
        bullets = row.get("bullets") or row.get("service_bullets") or []
        assert len(bullets) == 4, (
            f"the discipline {row.get('anchor')} must carry exactly four "
            f"bullets, found {len(bullets)}: " + conftest.describe(response))


def test_legal_routes_answer_for_a_visitor(site):
    for route in conftest.LEGAL_ROUTES:
        response = site.get(route)
        assert response.status_code == 200, (
            f"the legal route {route} must answer for a signed-out visitor: "
            + conftest.describe(response))
        bare = site.get(route.rstrip("/"))
        assert bare.status_code == 200, (
            f"the bare form of {route} must serve the same page: "
            + conftest.describe(bare))


def test_unknown_address_answers_not_found(site_direct):
    probe = f"/no-such-page-{conftest.unique_token()}"
    response = site_direct.get(probe)
    assert response.status_code == 404, (
        f"an address matching no route must answer not-found, {probe} answered "
        + conftest.describe(response))
    assert len(response.text) > 200, (
        "the not-found response must render the product's own page rather than "
        f"a bare error; body was {len(response.text)} characters: "
        + conftest.describe(response))


def test_sitemap_lists_every_public_route(site):
    response = site.get("/sitemap.xml")
    assert response.status_code == 200, (
        "/sitemap.xml must be served: " + conftest.describe(response))
    body = response.text
    for route in conftest.PUBLIC_ROUTES:
        assert route in body, (
            f"the public route {route} is missing from the sitemap: "
            + conftest.describe(response))
    assert conftest.DRAFT_CASE_SLUG not in body, (
        f"the draft case {conftest.DRAFT_CASE_SLUG} must not appear in the "
        "sitemap: " + conftest.describe(response))


def test_robots_names_the_sitemap(site):
    response = site.get("/robots.txt")
    assert response.status_code == 200, (
        "/robots.txt must be served: " + conftest.describe(response))
    assert "sitemap" in response.text.lower(), (
        "/robots.txt must point at the sitemap; body was "
        f"{response.text[:200]!r}: " + conftest.describe(response))


def test_each_public_route_carries_its_own_title_and_description(site):
    seen_titles = {}
    seen_descriptions = {}
    for route in conftest.PUBLIC_ROUTES:
        response = site.get(route)
        assert response.status_code == 200, (
            f"the public route {route} must answer: "
            + conftest.describe(response))
        body = response.text
        start = body.lower().find("<title")
        assert start != -1, (
            f"the route {route} emits no title element: "
            + conftest.describe(response))
        end = body.lower().find("</title>", start)
        title = body[body.find(">", start) + 1:end].strip()
        assert title, f"the route {route} emits an empty title"
        assert title not in seen_titles, (
            f"the route {route} shares its title {title!r} with "
            f"{seen_titles[title]}; no two routes may share a title")
        seen_titles[title] = route
        marker = 'name="description"'
        assert marker in body.replace("'", '"'), (
            f"the route {route} emits no description meta tag: "
            + conftest.describe(response))
        head = body.replace("'", '"')
        at = head.find(marker)
        window = head[max(0, at - 200):at + 400]
        content_at = window.find('content="')
        description = window[content_at + 9:window.find('"', content_at + 9)]
        assert description.strip(), (
            f"the route {route} emits an empty description")
        assert description not in seen_descriptions, (
            f"the route {route} shares its description with "
            f"{seen_descriptions[description]}; no two routes may share one")
        seen_descriptions[description] = route


def test_enquiry_is_persisted_as_a_row(anon, editor, backend):
    email = conftest.probe_email()
    message = f"Enquiry probe {conftest.unique_token()}"
    response = anon.post("/enquiries", json={
        "name": "Probe Visitor",
        "email": email,
        "organisation": "Probe Studio",
        "message": message,
    })
    assert response.status_code in (200, 201), (
        "a complete enquiry must be accepted from a signed-out visitor: "
        + conftest.describe(response))
    stored = conftest.poll_until(
        lambda: backend.count("enquiries", email=email) == 1)
    assert stored, (
        f"the accepted enquiry for {email} must be stored as exactly one row in "
        f"the enquiries table, found {backend.count('enquiries', email=email)}")
    listed = editor.get("/enquiries")
    assert listed.status_code == 200, (
        "an editor must be able to read the enquiry list: "
        + conftest.describe(listed))
    assert message in _shapes.flatten(listed.json()), (
        f"the submitted enquiry message {message!r} must reach the editor's "
        "list: " + conftest.describe(listed))


def test_publishing_a_case_makes_the_stored_row_and_the_listing_agree(
        anon, editor, backend):
    slug = conftest.probe_slug("publish-probe")
    number = "41"
    created = _create_case(editor, number, slug)
    before = anon.get("/cases")
    assert slug not in _slugs(before.json()), (
        f"a newly created case {slug} starts as a draft, so it must not appear "
        "in the public listing: " + conftest.describe(before))
    published = editor.patch(f"/cases/{slug}", json={"status": "published"})
    assert published.status_code in (200, 201, 202), (
        f"an editor must be able to publish {slug}: "
        + conftest.describe(published))
    row = conftest.poll_until(lambda: backend.one("cases", slug=slug))
    assert row is not None, f"the case {slug} must exist as a stored row"
    assert str(row.get("status")) == "published", (
        f"the stored row for {slug} must read published after publishing, read "
        f"{row.get('status')!r}")
    after = conftest.poll_until(lambda: slug in _slugs(anon.get("/cases").json()))
    assert after, (
        f"the published case {slug} must appear in the public listing that the "
        "stored row now agrees with")
    detail = anon.get(f"/cases/{slug}")
    assert detail.status_code == 200, (
        f"the published case {slug} must resolve for a signed-out visitor: "
        + conftest.describe(detail))


def test_seeded_cases_are_stored_with_unique_numbers(backend):
    rows = backend.rows("cases")
    assert rows, "the cases table must carry the seeded corpus"
    numbers = [str(r.get("number")) for r in rows]
    assert len(numbers) == len(set(numbers)), (
        f"every case number must be unique across cases, found {sorted(numbers)}")
    published = [str(r.get("number")) for r in rows
                 if str(r.get("status")) == "published"]
    for expected in conftest.SEEDED_CASE_NUMBERS:
        assert expected in published, (
            f"seeded published case {expected} is not stored as published; "
            f"published numbers were {sorted(published)}")
    assert conftest.DRAFT_CASE_NUMBER in numbers, (
        f"the seeded draft case {conftest.DRAFT_CASE_NUMBER} must be stored; "
        f"numbers were {sorted(numbers)}")


def test_page_view_row_is_absent_before_consent_is_recorded(anon, backend):
    token = conftest.unique_token()
    route = f"/cases/?probe={token}"
    before = backend.count("page_views")
    anon.post("/page-views", json={"route": route, "visitor_token": token})
    conftest.settle()
    assert backend.count("page_views", route=route) == 0, (
        f"no page view may be recorded for visitor {token} before that visitor "
        "has answered the cookie choice")
    consent = anon.post("/consent", json={
        "visitor_token": token, "analytics_allowed": True})
    assert consent.status_code in (200, 201), (
        "recording the cookie choice must succeed: "
        + conftest.describe(consent))
    anon.post("/page-views", json={"route": route, "visitor_token": token})
    recorded = conftest.poll_until(
        lambda: backend.count("page_views", route=route) >= 1)
    assert recorded, (
        f"a page view for {route} must be recorded once the visitor has "
        f"answered the cookie choice; the table holds {before} rows in total")


def test_uploaded_media_file_lands_in_the_object_store(editor, store, backend):
    slug = conftest.probe_slug("media-probe")
    created = _create_case(editor, "42", slug)
    case_id = _case_id(created)
    payload = f"probe-bytes-{conftest.unique_token()}".encode("utf-8")
    response = editor.post(
        f"/cases/{slug}/media",
        files={"file": ("cover.webm", payload, "video/webm")},
        data={"kind": "cover", "alt_text": "A probe cover clip",
              "decorative": "false"},
    )
    assert response.status_code in (200, 201), (
        f"an editor must be able to upload cover media for {slug}: "
        + conftest.describe(response))
    key = response.json().get("object_key") or response.json().get("objectKey")
    assert key, (
        "the upload response must name the object key it wrote: "
        + conftest.describe(response))
    assert key.startswith(f"{conftest.MEDIA_KEY_PREFIX}{case_id}/"), (
        f"the object key {key!r} must follow cases/<case_id>/<digest>.<ext> for "
        f"case {case_id}")
    assert conftest.sha256_hex(payload) in key, (
        f"the object key {key!r} must carry the sha256 of the uploaded bytes")
    landed = conftest.poll_until(lambda: store.exists(key))
    assert landed, (
        f"the uploaded bytes must exist in the object store at {key!r}; the "
        f"bucket holds {store.list(conftest.MEDIA_KEY_PREFIX)[:20]}")


def test_media_row_matches_the_object_key_in_the_bucket(editor, store, backend):
    slug = conftest.probe_slug("media-row-probe")
    created = _create_case(editor, "43", slug)
    case_id = _case_id(created)
    payload = f"row-probe-{conftest.unique_token()}".encode("utf-8")
    response = editor.post(
        f"/cases/{slug}/media",
        files={"file": ("body.webm", payload, "video/webm")},
        data={"kind": "body", "alt_text": "A probe body clip",
              "decorative": "false"},
    )
    assert response.status_code in (200, 201), (
        f"an editor must be able to upload body media for {slug}: "
        + conftest.describe(response))
    key = response.json().get("object_key") or response.json().get("objectKey")
    assert key, (
        "the upload response must name the object key it wrote: "
        + conftest.describe(response))
    row = conftest.poll_until(lambda: backend.one("media", object_key=key))
    assert row is not None, (
        f"the media table must carry a row whose object_key is {key!r}")
    assert str(row.get("alt_text")) == "A probe body clip", (
        f"the media row for {key!r} must record the alternative text that was "
        f"uploaded, recorded {row.get('alt_text')!r}")
    assert store.exists(key), (
        f"the media row for {key!r} must point at bytes that really exist in "
        "the bucket, so the row and the store agree")


def test_draft_case_by_slug_is_denied_to_a_visitor(anon, site_direct):
    response = anon.get(f"/cases/{conftest.DRAFT_CASE_SLUG}")
    assert response.status_code in (401, 403, 404), (
        f"the draft case {conftest.DRAFT_CASE_SLUG} must be denied to a "
        "signed-out visitor at the API: " + conftest.describe(response))
    page = site_direct.get(f"/cases/{conftest.DRAFT_CASE_SLUG}")
    assert page.status_code in (401, 403, 404), (
        f"the draft case route /cases/{conftest.DRAFT_CASE_SLUG} must be denied "
        "to a signed-out visitor: " + conftest.describe(page))


def test_draft_case_by_slug_is_denied_to_a_reader(reader):
    response = reader.get(f"/cases/{conftest.DRAFT_CASE_SLUG}")
    assert response.status_code in (401, 403, 404), (
        f"the draft case {conftest.DRAFT_CASE_SLUG} must be denied to a signed-in "
        "reader: " + conftest.describe(response))


def test_draft_case_is_absent_from_the_public_listing(anon, reader):
    for label, client in (("a signed-out visitor", anon), ("a reader", reader)):
        response = client.get("/cases")
        assert response.status_code == 200, (
            f"the public case listing must answer for {label}: "
            + conftest.describe(response))
        slugs = _slugs(response.json())
        assert conftest.DRAFT_CASE_SLUG not in slugs, (
            f"the draft case {conftest.DRAFT_CASE_SLUG} must be absent from the "
            f"listing {label} reads; listing carried {slugs}: "
            + conftest.describe(response))
        assert conftest.DRAFT_CASE_TITLE.lower() not in _shapes.flatten(
            response.json()), (
            f"the draft case title must not leak into the listing {label} reads: "
            + conftest.describe(response))


def test_draft_case_media_object_is_denied_to_a_reader(editor, reader, anon):
    slug = conftest.probe_slug("held-back-probe")
    _create_case(editor, "44", slug)
    payload = f"held-back-{conftest.unique_token()}".encode("utf-8")
    upload = editor.post(
        f"/cases/{slug}/media",
        files={"file": ("cover.webm", payload, "video/webm")},
        data={"kind": "cover", "alt_text": "A held back cover clip",
              "decorative": "false"},
    )
    assert upload.status_code in (200, 201), (
        f"an editor must be able to upload cover media for {slug}: "
        + conftest.describe(upload))
    body = upload.json()
    media_id = body.get("id") or body.get("media_id")
    assert media_id, (
        "the upload response must name the media row it created: "
        + conftest.describe(upload))
    for label, client in (("a reader", reader), ("a signed-out visitor", anon)):
        response = client.get(f"/media/{media_id}")
        assert response.status_code in (401, 403, 404), (
            f"media belonging to the draft case {slug} must be denied to "
            f"{label}: " + conftest.describe(response))


def test_reader_cannot_publish_a_case(editor, reader, backend):
    slug = conftest.probe_slug("reader-publish-probe")
    _create_case(editor, "45", slug)
    response = reader.patch(f"/cases/{slug}", json={"status": "published"})
    assert response.status_code in (401, 403, 404), (
        f"a reader calling the publish endpoint for {slug} must be denied: "
        + conftest.describe(response))
    conftest.settle()
    row = backend.one("cases", slug=slug)
    assert row is not None, f"the case {slug} must still exist after the denial"
    assert str(row.get("status")) == "draft", (
        f"the stored status for {slug} must be unchanged by the denied call, "
        f"read {row.get('status')!r}")


def test_signup_cannot_grant_the_editor_role(anon, backend):
    email = conftest.probe_email()
    response = anon.post("/auth/signup", json={
        "email": email,
        "password": conftest.APP_PASSWORD,
        "role": "editor",
    })
    assert response.status_code in (200, 201), (
        f"signup must be open and must accept {email}: "
        + conftest.describe(response))
    row = conftest.poll_until(lambda: backend.one("accounts", email=email))
    assert row is not None, f"the signup for {email} must create an account row"
    assert str(row.get("role")) == "reader", (
        f"a signup asking for the editor role must still create a reader; the "
        f"stored role for {email} was {row.get('role')!r}")


def test_studio_endpoints_are_denied_to_an_unauthenticated_caller(anon):
    for route in conftest.STUDIO_API_ROUTES:
        response = anon.get(route.replace("/api", "", 1))
        assert response.status_code in (401, 403), (
            f"{route} must be denied to a caller with no bearer token: "
            + conftest.describe(response))


def test_reader_is_forbidden_the_enquiry_list(reader):
    response = reader.get("/enquiries")
    assert response.status_code in (401, 403), (
        "the full enquiry list must be denied to a reader: "
        + conftest.describe(response))
    log = reader.get("/page-views")
    assert log.status_code in (401, 403), (
        "the page-view log must be denied to a reader: "
        + conftest.describe(log))


def test_login_with_a_wrong_password_is_denied(anon):
    response = anon.post("/auth/login", json={
        "email": conftest.EDITOR_EMAIL,
        "password": conftest.APP_PASSWORD + "-wrong",
    })
    assert response.status_code in (400, 401, 403), (
        "a sign-in with a wrong password must be denied: "
        + conftest.describe(response))
    assert "access_token" not in response.text, (
        "a denied sign-in must issue no bearer token: "
        + conftest.describe(response))


def test_invalid_enquiry_is_refused_and_writes_no_row(anon, backend):
    before = backend.count("enquiries")
    email = conftest.probe_email()
    response = anon.post("/enquiries", json={
        "name": "Probe Visitor",
        "email": "not-an-email-address",
        "message": "",
    })
    assert 400 <= response.status_code < 500, (
        "an enquiry with an unparseable address and an empty message must be "
        "refused as a client error: " + conftest.describe(response))
    conftest.settle()
    assert backend.count("enquiries") == before, (
        "a refused enquiry must write no row; the table grew from "
        f"{before} to {backend.count('enquiries')}")
    assert backend.count("enquiries", email=email) == 0, (
        "a refused enquiry must leave no partial row behind")


def test_enquiry_with_the_decoy_field_filled_is_refused(anon, backend):
    before = backend.count("enquiries")
    email = conftest.probe_email()
    response = anon.post("/enquiries", json={
        "name": "Probe Bot",
        "email": email,
        "message": f"Decoy probe {conftest.unique_token()}",
        "organisation_url": "https://example.test/decoy",
        "website": "https://example.test/decoy",
    })
    assert 400 <= response.status_code < 500, (
        "an enquiry arriving with the unattended decoy field filled must be "
        "refused: " + conftest.describe(response))
    conftest.settle()
    assert backend.count("enquiries", email=email) == 0, (
        f"the refused decoy enquiry for {email} must write nothing")
    assert backend.count("enquiries") == before, (
        "the refused decoy enquiry must leave the enquiries table unchanged; it "
        f"grew from {before} to {backend.count('enquiries')}")


def test_repeated_enquiry_submission_is_refused_after_the_first(anon, backend):
    email = conftest.probe_email()
    body = {
        "name": "Probe Visitor",
        "email": email,
        "message": f"Repeat probe {conftest.unique_token()}",
    }
    first = anon.post("/enquiries", json=body)
    assert first.status_code in (200, 201), (
        "the first enquiry of a burst must be accepted: "
        + conftest.describe(first))
    refusals = []
    for _ in range(4):
        again = anon.post("/enquiries", json=body)
        refusals.append(again.status_code)
    assert any(400 <= code < 500 for code in refusals), (
        "the same enquiry submitted repeatedly in quick succession must be "
        f"refused after the first; the burst answered {refusals}")
    conftest.settle()
    assert backend.count("enquiries", email=email) == 1, (
        f"only the first enquiry of the burst for {email} may be stored, found "
        f"{backend.count('enquiries', email=email)} rows")


def test_duplicate_case_number_is_refused(editor, backend):
    first_slug = conftest.probe_slug("number-probe-a")
    second_slug = conftest.probe_slug("number-probe-b")
    _create_case(editor, "46", first_slug)
    response = editor.post("/cases", json={
        "slug": second_slug,
        "number": "46",
        "client": "Probe Client",
        "title": "Duplicate number probe",
        "brief": "A second case claiming a number already in use.",
        "result": "The second case must not be created.",
    })
    assert 400 <= response.status_code < 500, (
        "a second case claiming a number already in use must be refused: "
        + conftest.describe(response))
    conftest.settle()
    assert backend.count("cases", number="46") == 1, (
        "exactly one case may hold the number 46 after the refusal, found "
        f"{backend.count('cases', number='46')}")
    assert backend.one("cases", slug=second_slug) is None, (
        f"the refused case {second_slug} must not have been written")
