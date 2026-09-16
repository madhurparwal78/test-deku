from __future__ import annotations

import concurrent.futures

import _shapes
import conftest


def test_home_route_carries_the_thirteen_sections_in_order(anon):
    r = anon.get(f"/pages{conftest.HOME_SLUG}")
    assert r.status_code == 200, (
        f"GET /api/pages{conftest.HOME_SLUG} returned {r.status_code}: "
        f"{conftest.body_excerpt(r)}")
    sections = r.json().get("sections") or []
    assert len(sections) == 13, (
        f"the home route carries {len(sections)} sections, expected the thirteen "
        f"full-width sections in the fixed order: {conftest.body_excerpt(r)}")
    positions = [s.get("position") for s in sections]
    assert positions == sorted(positions), (
        f"home route sections arrived out of position order {positions}: "
        f"{conftest.body_excerpt(r)}")


def test_home_route_copy_deck_renders_in_full(anon, app_origin):
    r = anon.get(f"{app_origin}/")
    assert r.status_code == 200, (
        f"GET / returned {r.status_code}: {conftest.body_excerpt(r)}")
    body = r.text
    assert conftest.HOME_TITLE_PREFIX in body, (
        f"the home route document title does not begin {conftest.HOME_TITLE_PREFIX!r}: "
        f"{conftest.body_excerpt(r)}")
    pinned = (
        (conftest.HERO_HEADLINE, conftest.HERO_PRIMARY, conftest.HERO_SECONDARY,
         conftest.HERO_TERTIARY, conftest.CLOSING_HEADING,
         conftest.SECURITY_CARD_LINE, conftest.ACCESS_RULES_LINE,
         conftest.FLEXIBLE_LAYOUT_LINE)
        + conftest.MENU_TRIGGERS + conftest.MENU_STRIP
        + conftest.CAPABILITY_HEADINGS + conftest.POWER_TOOLS
        + conftest.POWER_TOOL_LINKS + conftest.REFERENCE_CUSTOMERS
        + conftest.FEATURED_TEMPLATES)
    for literal in pinned:
        assert literal in body, (
            f"the home route is missing the pinned copy {literal!r}: "
            f"{conftest.body_excerpt(r)}")
    assert body.count(conftest.PRODUCT_ORIGIN) >= 3, (
        f"the home route links out to {conftest.PRODUCT_ORIGIN} "
        f"{body.count(conftest.PRODUCT_ORIGIN)} times, expected at least the sign in, "
        f"the sign up and a template card: {conftest.body_excerpt(r)}")


def test_published_route_is_served_to_an_anonymous_visitor(anon):
    r = anon.get(f"/pages{conftest.PUBLISHED_SECTOR_SLUG}")
    assert r.status_code == 200, (
        f"GET /api/pages{conftest.PUBLISHED_SECTOR_SLUG} as an anonymous caller "
        f"returned {r.status_code}: {conftest.body_excerpt(r)}")
    payload = r.json()
    assert payload.get("status") == "published", (
        f"the seeded sector route reports status {payload.get('status')!r}, "
        f"expected published: {conftest.body_excerpt(r)}")


def test_sector_route_inherits_the_shared_core_claim(anon):
    r = anon.get(f"/pages{conftest.PUBLISHED_SECTOR_SLUG}")
    assert r.status_code == 200, (
        f"GET /api/pages{conftest.PUBLISHED_SECTOR_SLUG} returned {r.status_code}: "
        f"{conftest.body_excerpt(r)}")
    assert conftest.SHARED_CORE_CLAIM in _shapes.flatten(r.json()), (
        f"the sector route does not carry the shared core claim "
        f"{conftest.SHARED_CORE_CLAIM!r}: {conftest.body_excerpt(r)}")


def test_capability_route_carries_exactly_three_numbered_steps(anon):
    r = anon.get("/pages", params={"template": "capability"})
    assert r.status_code == 200, (
        f"GET /api/pages?template=capability returned {r.status_code}: "
        f"{conftest.body_excerpt(r)}")
    routes = _shapes.items(r.json())
    assert routes, f"no capability route is published: {conftest.body_excerpt(r)}"
    slug = routes[0].get("slug")
    detail = anon.get(f"/pages{slug}")
    assert detail.status_code == 200, (
        f"GET /api/pages{slug} returned {detail.status_code}: "
        f"{conftest.body_excerpt(detail)}")
    body = _shapes.flatten(detail.json())
    for step in ("Build", "Share", "Analyze"):
        assert step in body, (
            f"the capability route {slug} is missing the numbered step {step!r}: "
            f"{conftest.body_excerpt(detail)}")


def test_capability_route_with_four_steps_is_refused(author):
    slug = conftest.probe_slug("/probe-capability-")
    payload = {"slug": slug, "template": "capability", "title": "Probe capability",
               "sections": [{"position": n, "style": "default",
                             "heading": f"Step {n}", "body": "probe"}
                            for n in range(1, 5)]}
    r = author.post("/pages", json=payload)
    assert 400 <= r.status_code < 500, (
        f"POST /api/pages with four capability steps returned {r.status_code}, "
        f"expected a client error refusing the step count: {conftest.body_excerpt(r)}")
    follow = author.get(f"/pages{slug}")
    assert follow.status_code == 404, (
        f"the refused capability route {slug} still resolves with "
        f"{follow.status_code}: {conftest.body_excerpt(follow)}")


def test_comparison_claim_renders_its_source_and_checked_date(anon):
    r = anon.get(f"/pages{conftest.PUBLISHED_COMPARISON_SLUG}")
    assert r.status_code == 200, (
        f"GET /api/pages{conftest.PUBLISHED_COMPARISON_SLUG} returned "
        f"{r.status_code}: {conftest.body_excerpt(r)}")
    claims = r.json().get("claims") or []
    assert claims, (
        f"the seeded comparison route carries no claim: {conftest.body_excerpt(r)}")
    for claim in claims:
        assert claim.get("source"), (
            f"a comparative claim on {conftest.PUBLISHED_COMPARISON_SLUG} carries no "
            f"source: {conftest.body_excerpt(r)}")
        assert claim.get("checked_on"), (
            f"a comparative claim on {conftest.PUBLISHED_COMPARISON_SLUG} carries no "
            f"checked_on date: {conftest.body_excerpt(r)}")


def test_claim_without_a_checked_date_is_refused_and_nothing_is_written(author, backend):
    slug = conftest.probe_slug()
    created = author.post("/pages", json={
        "slug": slug, "template": "comparison", "title": "Probe comparison",
        "sections": [{"position": 1, "style": "default", "heading": "Probe",
                      "body": "probe"}]})
    assert created.status_code in (200, 201), (
        f"POST /api/pages for {slug} returned {created.status_code}: "
        f"{conftest.body_excerpt(created)}")
    before = backend.count("claims")
    r = author.patch(f"/pages{slug}", json={"claims": [
        {"competitor": "Rowbase", "statement": "Probe statement",
         "source": "https://example.com/probe"}]})
    assert 400 <= r.status_code < 500, (
        f"saving a claim with no checked_on returned {r.status_code}, expected a "
        f"client error: {conftest.body_excerpt(r)}")
    after = backend.count("claims")
    assert after == before, (
        f"a refused claim still wrote a row: claims went from {before} to {after}")


def test_content_index_carries_one_featured_article(anon):
    r = anon.get(f"/pages{conftest.CASE_STUDY_INDEX_SLUG}")
    assert r.status_code == 200, (
        f"GET /api/pages{conftest.CASE_STUDY_INDEX_SLUG} returned {r.status_code}: "
        f"{conftest.body_excerpt(r)}")
    articles = r.json().get("articles") or []
    featured = [a for a in articles if a.get("tier") == "featured"]
    assert len(featured) == 1, (
        f"the case study index carries {len(featured)} featured articles, expected "
        f"exactly one: {conftest.body_excerpt(r)}")
    assert conftest.ALL_POSTS_HEADING in _shapes.flatten(r.json()), (
        f"the content index carries no {conftest.ALL_POSTS_HEADING!r} heading above "
        f"the paginated remainder: {conftest.body_excerpt(r)}")


def test_case_study_carries_sector_size_and_capability_fields(anon, backend):
    r = anon.get(f"/pages{conftest.CASE_STUDY_INDEX_SLUG}")
    assert r.status_code == 200, (
        f"GET /api/pages{conftest.CASE_STUDY_INDEX_SLUG} returned {r.status_code}: "
        f"{conftest.body_excerpt(r)}")
    articles = [a for a in (r.json().get("articles") or [])
                if a.get("kind") == "case_study"]
    assert len(articles) >= 3, (
        f"the case study index carries {len(articles)} case studies, expected the "
        f"three seeded ones: {conftest.body_excerpt(r)}")
    for article in articles:
        for field in ("sector", "organisation_size", "capability_demonstrated"):
            assert article.get(field), (
                f"case study {article.get('title')!r} carries no {field}: "
                f"{conftest.body_excerpt(r)}")
    stored = backend.rows("articles", kind="case_study")
    assert len(stored) >= 3, (
        f"the articles table holds {len(stored)} case_study rows, expected the three "
        f"seeded ones")


def test_sector_route_filters_its_proof_cards_on_sector(anon):
    r = anon.get(f"/pages{conftest.PUBLISHED_SECTOR_SLUG}")
    assert r.status_code == 200, (
        f"GET /api/pages{conftest.PUBLISHED_SECTOR_SLUG} returned {r.status_code}: "
        f"{conftest.body_excerpt(r)}")
    payload = r.json()
    assert payload.get("sector") == conftest.SEEDED_SECTOR, (
        f"the seeded sector route reports sector {payload.get('sector')!r}, expected "
        f"{conftest.SEEDED_SECTOR!r}: {conftest.body_excerpt(r)}")
    for article in payload.get("articles") or []:
        assert article.get("sector") == conftest.SEEDED_SECTOR, (
            f"proof card {article.get('title')!r} carries sector "
            f"{article.get('sector')!r} on a {conftest.SEEDED_SECTOR} route: "
            f"{conftest.body_excerpt(r)}")


def test_route_rows_are_persisted_and_survive_a_reload(author, backend):
    slug = conftest.probe_slug("/lookup/persisted-")
    title = f"Persisted probe {conftest.unique_suffix()}"
    created = author.post("/pages", json={
        "slug": slug, "template": "comparison", "title": title,
        "sections": [{"position": 1, "style": "default", "heading": "Probe",
                      "body": "probe"}]})
    assert created.status_code in (200, 201), (
        f"POST /api/pages for {slug} returned {created.status_code}: "
        f"{conftest.body_excerpt(created)}")
    row = backend.one("routes", slug=slug)
    assert row is not None, (
        f"no row in the routes table for {slug} after a successful create")
    assert row.get("status") == "draft", (
        f"a newly created route reports status {row.get('status')!r}, expected draft")
    reloaded = author.get(f"/pages{slug}")
    assert reloaded.status_code == 200, (
        f"GET /api/pages{slug} as its author returned {reloaded.status_code}: "
        f"{conftest.body_excerpt(reloaded)}")
    assert reloaded.json().get("title") == title, (
        f"the reloaded route title is {reloaded.json().get('title')!r}, expected "
        f"{title!r}")


def test_seeded_accounts_and_routes_are_stored_once(backend):
    for email in (conftest.AUTHOR_EMAIL, conftest.AUTHOR2_EMAIL, conftest.READER_EMAIL):
        found = backend.count("users", email=email)
        assert found == 1, (
            f"the users table holds {found} rows for the seeded account {email}, "
            f"expected exactly one")
    published = backend.count("routes", status="published")
    assert published >= 9, (
        f"the routes table holds {published} published routes, expected at least the "
        f"nine seeded ones")
    drafts = backend.count("routes", status="draft")
    assert drafts >= 2, (
        f"the routes table holds {drafts} draft routes, expected at least the two "
        f"seeded ones")
    legal = backend.one("routes", slug=conftest.DRAFT_SECTOR_SLUG)
    assert legal is not None, (
        f"the seeded draft route {conftest.DRAFT_SECTOR_SLUG} is absent from the "
        f"routes table")
    attached = backend.count("media", route_id=legal.get("id"))
    assert attached == 1, (
        f"the media table holds {attached} rows for the seeded draft route "
        f"{conftest.DRAFT_SECTOR_SLUG}, expected the one seeded attachment")


def test_duplicate_slug_is_refused_and_one_row_remains(author, backend):
    slug = conftest.probe_slug("/lookup/duplicate-")
    first = author.post("/pages", json={
        "slug": slug, "template": "comparison", "title": "First probe",
        "sections": [{"position": 1, "style": "default", "heading": "Probe",
                      "body": "probe"}]})
    assert first.status_code in (200, 201), (
        f"the first POST /api/pages for {slug} returned {first.status_code}: "
        f"{conftest.body_excerpt(first)}")
    second = author.post("/pages", json={
        "slug": slug, "template": "comparison", "title": "Second probe",
        "sections": [{"position": 1, "style": "default", "heading": "Probe",
                      "body": "probe"}]})
    assert 400 <= second.status_code < 500, (
        f"a second route on the taken slug {slug} returned {second.status_code}, "
        f"expected a client error: {conftest.body_excerpt(second)}")
    rows = backend.count("routes", slug=slug)
    assert rows == 1, (
        f"the routes table holds {rows} rows for slug {slug}, expected exactly one")


def test_trial_row_is_stored_with_the_derived_team_slug(anon, backend):
    team = conftest.probe_team_name()
    expected_slug = team.lower().replace(" ", "-")
    email = f"probe-{conftest.unique_suffix()}@example.com"
    r = anon.post("/trials", json={"email": email, "team_name": team,
                                   "sector": conftest.SEEDED_SECTOR})
    assert r.status_code in (200, 201), (
        f"POST /api/trials for {team!r} returned {r.status_code}: "
        f"{conftest.body_excerpt(r)}")
    payload = r.json()
    assert payload.get("team_slug") == expected_slug, (
        f"the trial reports team_slug {payload.get('team_slug')!r}, expected "
        f"{expected_slug!r}: {conftest.body_excerpt(r)}")
    assert payload.get("team_site_url") == f"https://{expected_slug}{conftest.TEAM_SITE_SUFFIX}", (
        f"the trial reports team_site_url {payload.get('team_site_url')!r}: "
        f"{conftest.body_excerpt(r)}")
    row = backend.one("trials", team_slug=expected_slug)
    assert row is not None, (
        f"no row in the trials table for team_slug {expected_slug}")


def test_repeated_trial_submission_creates_no_second_row(anon, backend):
    team = conftest.probe_team_name()
    expected_slug = team.lower().replace(" ", "-")
    email = f"probe-{conftest.unique_suffix()}@example.com"
    body = {"email": email, "team_name": team, "sector": conftest.SEEDED_SECTOR}
    first = anon.post("/trials", json=body)
    assert first.status_code in (200, 201), (
        f"the first POST /api/trials returned {first.status_code}: "
        f"{conftest.body_excerpt(first)}")
    second = anon.post("/trials", json=body)
    assert second.status_code in (200, 201), (
        f"replaying an identical trial submission returned {second.status_code}, "
        f"expected the first address returned unchanged: "
        f"{conftest.body_excerpt(second)}")
    assert second.json().get("team_site_url") == first.json().get("team_site_url"), (
        f"the replay returned {second.json().get('team_site_url')!r} rather than the "
        f"first address {first.json().get('team_site_url')!r}")
    rows = backend.count("trials", team_slug=expected_slug)
    assert rows == 1, (
        f"the trials table holds {rows} rows for team_slug {expected_slug}, expected "
        f"exactly one after a replay")


def test_concurrent_team_names_leave_exactly_one_trial(anon, backend):
    team = conftest.probe_team_name()
    expected_slug = team.lower().replace(" ", "-")

    def submit(n):
        return anon.post("/trials", json={
            "email": f"race-{n}-{conftest.unique_suffix()}@example.com",
            "team_name": team, "sector": conftest.SEEDED_SECTOR})

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(submit, range(6)))
    codes = [r.status_code for r in results]
    accepted = [r for r in results if r.status_code in (200, 201)]
    assert len(accepted) == 1, (
        f"{len(accepted)} of six simultaneous submissions of the team name {team!r} "
        f"succeeded, expected exactly one winner; status codes were {codes}")
    losers = [r for r in results if r.status_code not in (200, 201)]
    for loser in losers:
        assert 400 <= loser.status_code < 500, (
            f"a losing submission returned {loser.status_code}, expected a client "
            f"error conflict: {conftest.body_excerpt(loser)}")
    rows = backend.count("trials", team_slug=expected_slug)
    assert rows == 1, (
        f"the trials table holds {rows} rows for team_slug {expected_slug} after the "
        f"race, expected exactly one")


def _create_probe_route(http, template="sector", publish=False):
    slug = conftest.probe_slug("/solutions/probe-")
    created = http.post("/pages", json={
        "slug": slug, "template": template, "title": "Probe route",
        "sections": [{"position": 1, "style": "default", "heading": "Probe",
                      "body": "probe"}]})
    assert created.status_code in (200, 201), (
        f"POST /api/pages for {slug} returned {created.status_code}: "
        f"{conftest.body_excerpt(created)}")
    route_id = created.json().get("id")
    if publish:
        done = http.patch(f"/pages{slug}", json={"status": "published"})
        assert done.status_code in (200, 201), (
            f"publishing {slug} returned {done.status_code}: "
            f"{conftest.body_excerpt(done)}")
    return slug, route_id


def test_uploaded_file_lands_in_the_bucket_at_its_scheme_key(author2, store):
    slug, route_id = _create_probe_route(author2)
    payload = conftest.probe_bytes()
    r = author2.post("/media", files={"file": ("probe.webp", payload, "image/webp")},
                     data={"route_id": str(route_id), "alt_text": "A probe image"})
    assert r.status_code in (200, 201), (
        f"POST /api/media for route {route_id} returned {r.status_code}: "
        f"{conftest.body_excerpt(r)}")
    key = r.json().get("object_key")
    expected = conftest.expected_object_key(route_id, payload, "webp")
    assert key == expected, (
        f"the upload reports object_key {key!r}, expected the scheme key {expected!r}: "
        f"{conftest.body_excerpt(r)}")
    assert conftest.settle(lambda: store.exists(key)), (
        f"no object exists in the bucket at {key} after a successful upload to "
        f"route {route_id}")


def test_identical_bytes_uploaded_twice_leave_one_media_row(author2, backend, store):
    slug, route_id = _create_probe_route(author2)
    payload = conftest.probe_bytes()
    first = author2.post("/media", files={"file": ("probe.webp", payload, "image/webp")},
                         data={"route_id": str(route_id), "alt_text": "A probe image"})
    assert first.status_code in (200, 201), (
        f"the first upload returned {first.status_code}: "
        f"{conftest.body_excerpt(first)}")
    second = author2.post("/media", files={"file": ("probe.webp", payload, "image/webp")},
                          data={"route_id": str(route_id), "alt_text": "A probe image"})
    assert second.status_code in (200, 201), (
        f"re-uploading identical bytes returned {second.status_code}, expected the "
        f"existing key returned: {conftest.body_excerpt(second)}")
    assert second.json().get("object_key") == first.json().get("object_key"), (
        f"the second upload reports {second.json().get('object_key')!r} rather than "
        f"the existing key {first.json().get('object_key')!r}")
    rows = backend.count("media", route_id=route_id)
    assert rows == 1, (
        f"the media table holds {rows} rows for route {route_id} after uploading "
        f"identical bytes twice, expected exactly one")
    keys = store.list(f"{conftest.MEDIA_PREFIX}{route_id}/")
    assert len(keys) == 1, (
        f"the bucket holds {len(keys)} objects under "
        f"{conftest.MEDIA_PREFIX}{route_id}/, expected exactly one: {keys}")


def test_draft_attachment_is_not_publicly_readable(author2, anon):
    slug, route_id = _create_probe_route(author2)
    payload = conftest.probe_bytes()
    upload = author2.post("/media",
                          files={"file": ("probe.webp", payload, "image/webp")},
                          data={"route_id": str(route_id), "alt_text": "A probe image"})
    assert upload.status_code in (200, 201), (
        f"POST /api/media for the draft route {slug} returned {upload.status_code}: "
        f"{conftest.body_excerpt(upload)}")
    key = upload.json().get("object_key")
    denied = anon.get(f"/media/{key}")
    assert denied.status_code in (401, 403, 404), (
        f"GET /api/media/{key} as an anonymous caller returned {denied.status_code} "
        f"while the route is still a draft: {conftest.body_excerpt(denied)}")
    published = author2.patch(f"/pages{slug}", json={"status": "published"})
    assert published.status_code in (200, 201), (
        f"publishing {slug} returned {published.status_code}: "
        f"{conftest.body_excerpt(published)}")
    allowed = conftest.settle(
        lambda: anon.get(f"/media/{key}").status_code == 200)
    assert allowed, (
        f"GET /api/media/{key} is still refused after {slug} was published")


def test_image_without_alternative_text_is_refused(author2, backend):
    slug, route_id = _create_probe_route(author2)
    before = backend.count("media", route_id=route_id)
    payload = conftest.probe_bytes()
    r = author2.post("/media", files={"file": ("probe.webp", payload, "image/webp")},
                     data={"route_id": str(route_id)})
    assert 400 <= r.status_code < 500, (
        f"POST /api/media with no alt_text returned {r.status_code}, expected a "
        f"client error naming the field: {conftest.body_excerpt(r)}")
    after = backend.count("media", route_id=route_id)
    assert after == before, (
        f"a refused image save still wrote a media row for route {route_id}: "
        f"{before} to {after}")


def test_draft_route_is_denied_to_an_anonymous_caller(anon):
    r = anon.get(f"/pages{conftest.DRAFT_SECTOR_SLUG}")
    assert r.status_code == 404, (
        f"GET /api/pages{conftest.DRAFT_SECTOR_SLUG} as an anonymous caller returned "
        f"{r.status_code}, expected the draft to be answered as not found: "
        f"{conftest.body_excerpt(r)}")
    body = r.text
    for leaked in ("section", "media/", "draft"):
        assert leaked not in body.lower(), (
            f"the not found answer for a draft slug leaks {leaked!r}: "
            f"{conftest.body_excerpt(r)}")


def test_draft_route_denied_to_a_reader_looks_like_a_missing_slug(reader):
    draft = reader.get(f"/pages{conftest.DRAFT_COMPARISON_SLUG}")
    missing = reader.get(f"/pages{conftest.probe_slug('/lookup/never-created-')}")
    assert draft.status_code == 404, (
        f"GET /api/pages{conftest.DRAFT_COMPARISON_SLUG} as a reader returned "
        f"{draft.status_code}, expected not found: {conftest.body_excerpt(draft)}")
    assert missing.status_code == 404, (
        f"a slug that was never created returned {missing.status_code}, expected not "
        f"found: {conftest.body_excerpt(missing)}")
    assert draft.text == missing.text, (
        f"the answer for a draft slug differs from the answer for a slug that does "
        f"not exist, so the response confirms the draft exists: draft "
        f"{conftest.body_excerpt(draft)} versus missing {conftest.body_excerpt(missing)}")


def test_reader_cannot_publish_a_route_and_the_row_is_unchanged(reader, backend):
    before = backend.one("routes", slug=conftest.DRAFT_SECTOR_SLUG)
    assert before is not None, (
        f"the seeded draft route {conftest.DRAFT_SECTOR_SLUG} is missing from the "
        f"routes table")
    r = reader.patch(f"/pages{conftest.DRAFT_SECTOR_SLUG}",
                     json={"status": "published"})
    assert r.status_code in (401, 403, 404), (
        f"a reader publishing {conftest.DRAFT_SECTOR_SLUG} returned {r.status_code}, "
        f"expected the server to refuse: {conftest.body_excerpt(r)}")
    after = backend.one("routes", slug=conftest.DRAFT_SECTOR_SLUG)
    assert after.get("status") == "draft", (
        f"the protected route changed to {after.get('status')!r} after a refused "
        f"reader request")


def test_unauthenticated_write_to_pages_is_denied(anon, backend):
    slug = conftest.probe_slug("/lookup/anonymous-")
    r = anon.post("/pages", json={
        "slug": slug, "template": "comparison", "title": "Anonymous probe",
        "sections": [{"position": 1, "style": "default", "heading": "Probe",
                      "body": "probe"}]})
    assert r.status_code in (401, 403), (
        f"POST /api/pages with no bearer token returned {r.status_code}, expected the "
        f"server to refuse: {conftest.body_excerpt(r)}")
    rows = backend.count("routes", slug=slug)
    assert rows == 0, (
        f"an unauthenticated create still wrote {rows} row(s) for {slug}")


def test_reader_cannot_upload_and_no_object_reaches_the_bucket(reader, author, store):
    created = author.post("/pages", json={
        "slug": conftest.probe_slug("/solutions/reader-probe-"),
        "template": "sector", "title": "Reader probe",
        "sections": [{"position": 1, "style": "default", "heading": "Probe",
                      "body": "probe"}]})
    assert created.status_code in (200, 201), (
        f"POST /api/pages returned {created.status_code}: "
        f"{conftest.body_excerpt(created)}")
    route_id = created.json().get("id")
    payload = conftest.probe_bytes()
    r = reader.post("/media", files={"file": ("probe.webp", payload, "image/webp")},
                    data={"route_id": str(route_id), "alt_text": "A probe image"})
    assert r.status_code in (401, 403), (
        f"a reader uploading to route {route_id} returned {r.status_code}, expected "
        f"the server to refuse: {conftest.body_excerpt(r)}")
    keys = store.list(f"{conftest.MEDIA_PREFIX}{route_id}/")
    assert keys == [], (
        f"a refused reader upload still put {len(keys)} object(s) in the bucket under "
        f"{conftest.MEDIA_PREFIX}{route_id}/: {keys}")


def test_reader_cannot_read_another_readers_trial(reader, anon):
    team = conftest.probe_team_name()
    other = anon.post("/trials", json={
        "email": f"other-{conftest.unique_suffix()}@example.com",
        "team_name": team, "sector": conftest.SEEDED_SECTOR})
    assert other.status_code in (200, 201), (
        f"POST /api/trials for the other reader returned {other.status_code}: "
        f"{conftest.body_excerpt(other)}")
    slug = other.json().get("team_slug")
    r = reader.get(f"/trials/{slug}")
    assert r.status_code in (401, 403, 404), (
        f"a reader reading the trial {slug} belonging to somebody else returned "
        f"{r.status_code}, expected the server to refuse: {conftest.body_excerpt(r)}")


def test_trial_signup_list_is_forbidden_to_a_reader(reader, author):
    denied = reader.get("/trials")
    assert denied.status_code in (401, 403), (
        f"GET /api/trials as a reader returned {denied.status_code}, expected the "
        f"server to refuse the signup list: {conftest.body_excerpt(denied)}")
    allowed = author.get("/trials")
    assert allowed.status_code == 200, (
        f"GET /api/trials as an author returned {allowed.status_code}, expected the "
        f"signup list: {conftest.body_excerpt(allowed)}")
    assert isinstance(allowed.json(), list), (
        f"GET /api/trials returned {type(allowed.json()).__name__}, expected a "
        f"top-level JSON array: {conftest.body_excerpt(allowed)}")


def test_trial_without_an_at_sign_in_the_email_is_refused(anon, backend):
    team = conftest.probe_team_name()
    before = backend.count("trials")
    r = anon.post("/trials", json={"email": "no-at-sign-here",
                                   "team_name": team,
                                   "sector": conftest.SEEDED_SECTOR})
    assert 400 <= r.status_code < 500, (
        f"POST /api/trials with an email carrying no at sign returned "
        f"{r.status_code}, expected a client error naming the email field: "
        f"{conftest.body_excerpt(r)}")
    assert "email" in r.text.lower(), (
        f"the refusal does not name the email field: {conftest.body_excerpt(r)}")
    after = backend.count("trials")
    assert after == before, (
        f"a refused trial still wrote a row: trials went from {before} to {after}")


def test_trial_with_an_unknown_sector_is_refused(anon, backend):
    team = conftest.probe_team_name()
    before = backend.count("trials")
    r = anon.post("/trials", json={
        "email": f"probe-{conftest.unique_suffix()}@example.com",
        "team_name": team, "sector": "not-a-published-sector"})
    assert 400 <= r.status_code < 500, (
        f"POST /api/trials with a sector outside the published list returned "
        f"{r.status_code}, expected a client error: {conftest.body_excerpt(r)}")
    after = backend.count("trials")
    assert after == before, (
        f"a trial carrying an unknown sector still wrote a row: {before} to {after}")


def test_content_index_count_excludes_drafts(anon, author):
    public = anon.get("/pages", params={"status": "published"})
    assert public.status_code == 200, (
        f"GET /api/pages?status=published returned {public.status_code}: "
        f"{conftest.body_excerpt(public)}")
    public_slugs = {row.get("slug") for row in _shapes.items(public.json())}
    assert conftest.DRAFT_SECTOR_SLUG not in public_slugs, (
        f"the public route listing carries the draft slug "
        f"{conftest.DRAFT_SECTOR_SLUG}: {conftest.body_excerpt(public)}")
    assert conftest.DRAFT_COMPARISON_SLUG not in public_slugs, (
        f"the public route listing carries the draft slug "
        f"{conftest.DRAFT_COMPARISON_SLUG}: {conftest.body_excerpt(public)}")
    every = anon.get("/pages")
    assert every.status_code == 200, (
        f"GET /api/pages returned {every.status_code}: "
        f"{conftest.body_excerpt(every)}")
    anonymous_slugs = {row.get("slug") for row in _shapes.items(every.json())}
    assert conftest.DRAFT_SECTOR_SLUG not in anonymous_slugs, (
        f"an unfiltered anonymous listing reveals the draft slug "
        f"{conftest.DRAFT_SECTOR_SLUG}: {conftest.body_excerpt(every)}")


def test_unknown_address_renders_the_not_found_page(anon, app_origin):
    address = f"{app_origin}/never-created-{conftest.unique_suffix()}/"
    r = anon.get(address)
    assert r.status_code == 404, (
        f"GET {address} returned {r.status_code}, expected the site own not found "
        f"page to answer not found: {conftest.body_excerpt(r)}")
    assert "Sheaf" in r.text, (
        f"the not found answer is not the site own page: {conftest.body_excerpt(r)}")


def test_every_internal_link_resolves_to_a_published_route(anon):
    r = anon.get("/links")
    assert r.status_code == 200, (
        f"GET /api/links returned {r.status_code}: {conftest.body_excerpt(r)}")
    links = _shapes.items(r.json())
    assert links, f"GET /api/links returned no links at all: {conftest.body_excerpt(r)}"
    broken = [row for row in links if not row.get("resolved")]
    assert broken == [], (
        f"{len(broken)} internal link(s) do not resolve to a published route, first "
        f"few: {broken[:5]}")


def test_health_route_answers_ready(anon):
    r = anon.get("/health")
    assert r.status_code == 200, (
        f"GET /api/health returned {r.status_code}, expected 200 once the app is "
        f"ready: {conftest.body_excerpt(r)}")


def test_security_headers_are_present_on_every_response(anon, app_origin):
    page = anon.get(f"{app_origin}/")
    api = anon.get("/health")
    missing = anon.get(f"{app_origin}/never-created-{conftest.unique_suffix()}/")
    for label, response in (("the home route", page), ("GET /api/health", api),
                            ("the not found answer", missing)):
        headers = {k.lower(): v for k, v in response.headers.items()}
        assert "strict-transport-security" in headers, (
            f"{label} carries no strict transport policy header, headers were "
            f"{sorted(headers)}")
        assert headers.get("x-content-type-options", "").lower() == "nosniff", (
            f"{label} carries x-content-type-options "
            f"{headers.get('x-content-type-options')!r}, expected nosniff")


def test_no_storage_secret_appears_in_downloaded_assets(anon, app_origin):
    r = anon.get(f"{app_origin}/")
    assert r.status_code == 200, (
        f"GET / returned {r.status_code}: {conftest.body_excerpt(r)}")
    import os
    secret = os.environ.get("STORAGE_SECRET_KEY", "")
    access = os.environ.get("STORAGE_ACCESS_KEY", "")
    assert secret and secret not in r.text, (
        f"the object store secret appears in what the browser downloads from /")
    assert access and access not in r.text, (
        f"the object store access key appears in what the browser downloads from /")
    assert conftest.PASSWORD not in r.text, (
        f"the seeded password appears in what the browser downloads from /")


def test_announcement_bar_dismissal_persists_for_the_visitor(anon, app_origin):
    page = anon.get(f"{app_origin}{conftest.PRICING_SLUG}")
    assert page.status_code == 200, (
        f"GET {conftest.PRICING_SLUG} returned {page.status_code}: "
        f"{conftest.body_excerpt(page)}")
    assert conftest.ANNOUNCEMENT_COPY in page.text, (
        f"the announcement bar copy is missing from {conftest.PRICING_SLUG}: "
        f"{conftest.body_excerpt(page)}")
    dismissed = anon.post("/announcement/dismiss")
    assert dismissed.status_code in (200, 201, 204), (
        f"dismissing the announcement bar returned {dismissed.status_code}, expected "
        f"the dismissal to be accepted: {conftest.body_excerpt(dismissed)}")
    again = anon.get(f"{app_origin}{conftest.PRICING_SLUG}")
    assert conftest.ANNOUNCEMENT_COPY not in again.text, (
        f"the announcement bar returned after being dismissed: "
        f"{conftest.body_excerpt(again)}")


def test_star_count_control_degrades_without_a_number(anon, app_origin):
    r = anon.get("/stars")
    assert r.status_code == 200, (
        f"GET /api/stars returned {r.status_code}: {conftest.body_excerpt(r)}")
    assert "count" in r.json(), (
        f"GET /api/stars carries no count field: {conftest.body_excerpt(r)}")
    home = anon.get(f"{app_origin}/")
    assert conftest.STAR_LABEL in home.text, (
        f"the header carries no {conftest.STAR_LABEL!r} control, so the count cannot "
        f"degrade gracefully: {conftest.body_excerpt(home)}")


def test_closing_action_band_appears_on_every_route_but_home(anon, app_origin):
    home = anon.get(f"{app_origin}/")
    assert conftest.CLOSING_BAND_HEADING not in home.text, (
        f"the home route carries the closing action band heading "
        f"{conftest.CLOSING_BAND_HEADING!r}, which belongs to every other route: "
        f"{conftest.body_excerpt(home)}")
    for slug in (conftest.PRICING_SLUG, conftest.PUBLISHED_SECTOR_SLUG,
                 conftest.CASE_STUDY_INDEX_SLUG):
        page = anon.get(f"{app_origin}{slug}")
        assert page.status_code == 200, (
            f"GET {slug} returned {page.status_code}: {conftest.body_excerpt(page)}")
        assert conftest.CLOSING_BAND_HEADING in page.text, (
            f"{slug} does not end with the closing action band heading "
            f"{conftest.CLOSING_BAND_HEADING!r}: {conftest.body_excerpt(page)}")


def test_cookie_choice_persists_and_gates_third_party_scripts(anon, app_origin):
    first = anon.get(f"{app_origin}/")
    assert first.status_code == 200, (
        f"GET / returned {first.status_code}: {conftest.body_excerpt(first)}")
    stored = anon.post("/consent", json={"choice": "decline"})
    assert stored.status_code in (200, 201), (
        f"POST /api/consent returned {stored.status_code}: "
        f"{conftest.body_excerpt(stored)}")
    assert stored.json().get("choice") == "decline", (
        f"the stored consent choice is {stored.json().get('choice')!r}, expected "
        f"decline: {conftest.body_excerpt(stored)}")
    again = anon.get(f"{app_origin}/")
    for vendor in ("googletagmanager.com", "google-analytics.com", "connect.facebook",
                   "licdn.com", "hotjar.com"):
        assert vendor not in again.text, (
            f"the home route requests the third-party origin {vendor} after consent "
            f"was declined: {conftest.body_excerpt(again)}")
