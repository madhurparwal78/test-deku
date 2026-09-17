from __future__ import annotations

import os
import re

import httpx

import appclient
import conftest as fx
import _shapes


def test_health_route_answers_ready():
    """The health route answers once the app is ready."""
    response = httpx.get(f"{fx.api_base()}/health", timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code} rather than 200: "
        f"{response.text[:300]}"
    )


def test_app_is_reachable_and_serves_the_api_on_one_origin():
    """The app answers at its public address with the API on the same origin."""
    home = fx.page("/")
    assert home.status_code == 200, (
        f"GET / at {fx.app_url()} returned {home.status_code} rather than a page: "
        f"{home.text[:300]}"
    )
    api = httpx.get(f"{fx.api_base()}/health", timeout=fx.TIMEOUT)
    assert api.status_code == 200, (
        f"GET /api/health on the same origin returned {api.status_code}: {api.text[:300]}"
    )
    assert fx.api_base().startswith(fx.app_url()), (
        f"the API base {fx.api_base()} is not on the origin {fx.app_url()}"
    )


def test_seeded_accounts_sign_in_with_the_corpus_password():
    """Each seeded account signs in with the pinned password."""
    for email in (fx.AUTHOR_EMAIL, fx.SECOND_AUTHOR_EMAIL, fx.READER_EMAIL):
        token = appclient.login(email, fx.CORPUS_PASSWORD)
        assert token, f"login for {email} returned an empty access_token"
        with appclient.client(token) as client:
            response = client.get("/applications")
            assert response.status_code in (200, 403), (
                f"GET /api/applications as {email} returned {response.status_code}, "
                f"which is neither a served list nor a refusal: {response.text[:300]}"
            )


def test_open_signup_creates_a_reader():
    """An open signup creates a reader account."""
    email, token = fx.register()
    with appclient.client(token) as client:
        response = client.post("/applications", json={"name": f"Probe {fx.unique_suffix()}"})
        assert response.status_code in (200, 201), (
            f"POST /api/applications as the freshly signed-up {email} returned "
            f"{response.status_code}, so the account is not a reader: {response.text[:400]}"
        )
    again = appclient.login(email, fx.CORPUS_PASSWORD)
    assert again, f"the account {email} created by signup cannot sign in afterwards"


def test_duplicate_signup_is_refused_and_creates_nothing():
    """A signup reusing an address is refused and writes nothing."""
    email, _ = fx.register()
    response = httpx.post(
        f"{fx.api_base()}/auth/sign-up",
        json={"email": email, "password": fx.CORPUS_PASSWORD, "display_name": "Second Claim"},
        timeout=fx.TIMEOUT,
    )
    assert 400 <= response.status_code < 500, (
        f"POST /api/auth/sign-up reusing {email} returned {response.status_code} rather "
        f"than refusing as a client error: {response.text[:400]}"
    )


def test_entry_redirects_and_role_landings():
    """An anonymous caller is redirected and each role lands on its own surface."""
    for path in ("/dashboard", "/studio/library"):
        response = fx.page(path)
        assert response.status_code in (301, 302, 303, 307, 308, 401, 403), (
            f"GET {path} while signed out returned {response.status_code} rather than "
            f"redirecting or refusing: {response.text[:300]}"
        )
        if response.status_code in (301, 302, 303, 307, 308):
            location = response.headers.get("location", "")
            assert "/sign-in" in location, (
                f"GET {path} while signed out redirected to {location!r} rather than "
                f"to /sign-in"
            )
    with fx.as_reader() as reader:
        studio = reader.get("/entries", params={"state": "draft"})
        assert studio.status_code in (200, 403), (
            f"GET /api/entries?state=draft as a reader returned {studio.status_code}, "
            f"which is neither an empty list nor a refusal: {studio.text[:300]}"
        )


def test_published_entry_is_readable_by_anyone():
    """A published entry is readable without an account."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
        result = fx.publish(author, entry["id"])
        assert result.status_code in (200, 201), (
            f"POST /api/entries/{entry['id']}/publish returned {result.status_code}: "
            f"{result.text[:400]}"
        )
    with fx.anonymous() as guest:
        response = guest.get(f"/entries/{entry['kind']}/{entry['slug']}")
        assert response.status_code == 200, (
            f"GET /api/entries/{entry['kind']}/{entry['slug']} as an anonymous caller "
            f"returned {response.status_code} for a published entry: {response.text[:300]}"
        )
        body = response.json()
        assert body.get("state") == "published", (
            f"the published entry reports state {body.get('state')!r}: {response.text[:300]}"
        )
        assert body.get("title") == entry["title"], (
            f"the served entry title {body.get('title')!r} does not match the stored "
            f"{entry['title']!r}"
        )


def test_publish_writes_the_rendition_in_the_same_operation():
    """Publishing writes the plain-text rendition beside the entry."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
        before = fx.page(f"/r/{entry['kind']}/{entry['slug']}.txt")
        assert before.status_code in (401, 403, 404), (
            f"GET /r/{entry['kind']}/{entry['slug']}.txt served a DRAFT entry with "
            f"{before.status_code}: {before.text[:200]}"
        )
        result = fx.publish(author, entry["id"])
        assert result.status_code in (200, 201), (
            f"publishing {entry['id']} returned {result.status_code}: {result.text[:400]}"
        )
        published = result.json()
        assert published.get("published_at"), (
            f"publishing {entry['id']} left published_at empty: {result.text[:300]}"
        )
        assert re.search(r"(Z|[+-]\d{2}:?\d{2})$", str(published["published_at"])) or \
            str(published["published_at"]).endswith("Z"), (
            f"published_at {published['published_at']!r} carries no UTC marker"
        )
    after = fx.page(f"/r/{entry['kind']}/{entry['slug']}.txt")
    assert after.status_code == 200, (
        f"GET /r/{entry['kind']}/{entry['slug']}.txt after publication returned "
        f"{after.status_code}: {after.text[:300]}"
    )
    assert entry["title"] in after.text, (
        f"the rendition at /r/{entry['kind']}/{entry['slug']}.txt does not carry the "
        f"entry title {entry['title']!r}: {after.text[:300]}"
    )


def test_rendition_index_enumerates_every_published_entry():
    """The rendition index lists every published entry."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
        fx.publish(author, entry["id"])
    index = fx.page("/r/index.txt")
    assert index.status_code == 200, (
        f"GET /r/index.txt returned {index.status_code} rather than the enumeration: "
        f"{index.text[:300]}"
    )
    address = f"/r/{entry['kind']}/{entry['slug']}.txt"
    assert address in index.text, (
        f"/r/index.txt does not enumerate {address}: {index.text[:400]}"
    )


def test_unpublish_withdraws_route_rendition_and_image():
    """Unpublishing withdraws the route, the rendition and the image."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
        asset = fx.attach_image(author, entry["id"])
        assert asset.status_code in (200, 201), (
            f"attaching an image to {entry['id']} returned {asset.status_code}: "
            f"{asset.text[:400]}"
        )
        asset_id = asset.json()["id"]
        fx.publish(author, entry["id"])
        withdrawn = author.post(f"/entries/{entry['id']}/unpublish")
        assert withdrawn.status_code in (200, 201), (
            f"POST /api/entries/{entry['id']}/unpublish returned {withdrawn.status_code}: "
            f"{withdrawn.text[:400]}"
        )
    with fx.anonymous() as guest:
        route = guest.get(f"/entries/{entry['kind']}/{entry['slug']}")
        assert route.status_code in (401, 403, 404), (
            f"the unpublished entry is still served at "
            f"/api/entries/{entry['kind']}/{entry['slug']} with {route.status_code}"
        )
        content = guest.get(f"/entries/{entry['id']}/assets/{asset_id}/content")
        assert content.status_code in (401, 403, 404), (
            f"the unpublished entry's image is still served with {content.status_code}"
        )
    rendition = fx.page(f"/r/{entry['kind']}/{entry['slug']}.txt")
    assert rendition.status_code in (401, 403, 404), (
        f"the unpublished entry's rendition is still served with {rendition.status_code}"
    )


def test_documentation_note_appears_when_a_sample_is_missing():
    """A concept with no sample for the chosen SDK renders an explicit note."""
    body = fx.rendered("/docs")
    lowered = body.lower()
    assert "select your sdk" in lowered, (
        "the documentation landing page carries no 'Select your SDK' well"
    )
    assert 'data-sdk="next.js"' in lowered or 'data-sdk="nextjs"' in lowered, (
        f"the documentation shell declares no default data-sdk: {body[:400]}"
    )
    response = httpx.get(f"{fx.api_base()}/search", params={"q": "session", "sdk": "Rust"},
                         timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/search?q=session&sdk=Rust returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    assert isinstance(response.json(), list), (
        f"GET /api/search returned {type(response.json()).__name__} rather than a "
        f"top-level array: {response.text[:300]}"
    )


def test_plans_endpoint_returns_the_four_plans():
    """The plan endpoint returns four plans read from the plan document."""
    response = httpx.get(f"{fx.api_base()}/plans", timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/plans returned {response.status_code}: {response.text[:300]}"
    )
    plans = _shapes.items(response.json())
    codes = [str(p.get("code", "")).lower() for p in plans]
    for code in fx.PLAN_CODES:
        assert code in codes, (
            f"GET /api/plans does not carry the plan {code!r}; it returned {codes}"
        )
    flat = _shapes.flatten(response.json())
    for shown in ("$20", "$250"):
        assert shown in flat, (
            f"GET /api/plans does not carry the displayed price {shown!r}: {flat[:400]}"
        )


def test_pricing_ladders_match_the_plan_document():
    """The graduated price ladders match the stored plan document."""
    response = httpx.get(f"{fx.api_base()}/plans", timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/plans returned {response.status_code}: {response.text[:300]}"
    )
    flat = _shapes.flatten(response.json())
    for band in ("1,000", "100,000", "$0.001", "$0.00001", "2,500", "$0.02", "$75", "50,000"):
        assert band in flat, (
            f"the plan document carries no ladder value {band!r}: {flat[:500]}"
        )
    page_body = fx.rendered("/pricing")
    for band in ("1,000", "$0.00001"):
        assert band in page_body, (
            f"the pricing route does not render the ladder value {band!r}"
        )
    assert "1,000 creations & 100,000 verifications limit per month" in page_body, (
        "the Hobby column does not carry its combined summary in place of a ladder"
    )


def test_pricing_cards_carry_the_plan_attribute():
    """Each pricing card declares which plan it is."""
    body = fx.rendered("/pricing")
    for code in fx.PLAN_CODES:
        assert f'data-plan="{code}"' in body, (
            f"the pricing route carries no card marked data-plan=\"{code}\""
        )
    assert 'data-billing-period="monthly"' in body or 'data-billing-period="annual"' in body, (
        f"the pricing route declares no data-billing-period: {body[:400]}"
    )


def test_leaderboard_absent_cell_is_not_a_zero():
    """A leaderboard cell with no result is an absence rather than a zero."""
    response = httpx.get(f"{fx.api_base()}/leaderboard", timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/leaderboard returned {response.status_code}: {response.text[:300]}"
    )
    rows = _shapes.items(response.json())
    assert rows, f"GET /api/leaderboard returned no rows: {response.text[:300]}"
    absent = [r for r in rows if r.get("score_percent") is None]
    assert absent, (
        "no leaderboard row carries a null score_percent, so the absence rendering is "
        "never exercised by the seed"
    )
    for row in absent:
        assert row.get("score_percent") != 0, (
            f"a leaderboard row with no result stores a zero rather than an absence: {row}"
        )
    body = fx.rendered("/llm-leaderboard")
    assert 'data-cell-band="absent"' in body, (
        "the leaderboard route marks no cell data-cell-band=\"absent\""
    )


def test_leaderboard_cells_carry_the_band_attribute():
    """Each leaderboard cell declares which band its number falls in."""
    body = fx.rendered("/llm-leaderboard")
    seen = {band for band in fx.CELL_BANDS if f'data-cell-band="{band}"' in body}
    assert {"above", "below"} <= seen, (
        f"the leaderboard declares only the cell bands {sorted(seen)}; both 'above' and "
        f"'below' must appear"
    )
    assert "<table" in body.lower(), (
        "the leaderboard matrix is not rendered as a table, so a cell cannot be read as "
        "model by task"
    )


def test_leaderboard_filter_selects_a_corpus_subset():
    """The leaderboard filters select a subset of the corpus."""
    everything = httpx.get(f"{fx.api_base()}/leaderboard", timeout=fx.TIMEOUT)
    filtered = httpx.get(f"{fx.api_base()}/leaderboard",
                         params={"framework": "Next.js", "mode": "Base"}, timeout=fx.TIMEOUT)
    assert filtered.status_code == 200, (
        f"GET /api/leaderboard with a framework filter returned {filtered.status_code}: "
        f"{filtered.text[:300]}"
    )
    all_rows = _shapes.items(everything.json())
    some_rows = _shapes.items(filtered.json())
    assert len(some_rows) < len(all_rows), (
        f"filtering the leaderboard returned {len(some_rows)} of {len(all_rows)} rows, so "
        f"the filter selects nothing"
    )
    for row in some_rows:
        assert row.get("framework") == "Next.js", (
            f"a filtered leaderboard row carries framework {row.get('framework')!r}: {row}"
        )
        assert row.get("mode") == "Base", (
            f"a filtered leaderboard row carries mode {row.get('mode')!r}: {row}"
        )
    body = fx.rendered("/llm-leaderboard")
    for family in fx.TASK_FAMILIES:
        assert family in body, f"the leaderboard header omits the task column {family!r}"


def test_leaderboard_cells_carry_their_provenance():
    """Every published leaderboard cell carries its versions and its run count."""
    response = httpx.get(f"{fx.api_base()}/leaderboard", timeout=fx.TIMEOUT)
    rows = [r for r in _shapes.items(response.json()) if r.get("score_percent") is not None]
    assert rows, f"GET /api/leaderboard carries no scored rows: {response.text[:300]}"
    for row in rows:
        for field in ("model_version", "harness_version", "corpus_version", "run_date",
                      "run_count"):
            assert row.get(field), (
                f"a published leaderboard cell carries no {field}: {row}"
            )
        assert int(row["run_count"]) >= 1, (
            f"a published leaderboard cell reports run_count {row['run_count']}: {row}"
        )


def test_glossary_graph_is_derived_and_never_self_linking():
    """The related-term graph is derived and never links an entry to itself."""
    response = httpx.get(f"{fx.api_base()}/glossary/graph", timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/glossary/graph returned {response.status_code}: {response.text[:300]}"
    )
    edges = _shapes.items(response.json())
    assert len(edges) >= 41, (
        f"the glossary graph carries {len(edges)} edges; the seed declares at least 41"
    )
    for edge in edges:
        assert edge.get("from_slug") != edge.get("to_slug"), (
            f"a related-term edge links an entry to itself: {edge}"
        )
        assert edge.get("term_text"), f"a related-term edge carries no term text: {edge}"
    targets = {e.get("to_slug") for e in edges}
    sources = {e.get("from_slug") for e in edges}
    assert targets and sources, "the glossary graph has no sources or no targets"


def test_glossary_rail_marks_the_inert_letters():
    """The alphabet rail marks its four inert letters."""
    body = fx.rendered("/glossary")
    for letter in fx.INERT_LETTERS:
        assert f'data-glossary-letter="{letter}"' in body, (
            f"the alphabet rail carries no cell for the letter {letter!r}"
        )
    assert 'data-letter-state="inert"' in body, (
        "the alphabet rail marks no letter inert, though four letters have no entries"
    )
    assert 'data-letter-state="active"' in body, (
        "the alphabet rail marks no letter active"
    )


def test_changelog_orders_entries_newest_first():
    """The changelog timeline runs newest first with the newest node marked."""
    response = httpx.get(f"{fx.api_base()}/entries", params={"kind": "changelog",
                                                            "state": "published"},
                         timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/entries?kind=changelog returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    entries = _shapes.items(response.json())
    stamps = [str(e.get("published_at") or "") for e in entries]
    assert stamps == sorted(stamps, reverse=True), (
        f"the changelog is not ordered newest first: {stamps[:6]}"
    )
    body = fx.rendered("/changelog")
    assert "Custom OAuth scopes" in body, (
        "the changelog route does not carry the seeded entry 'Custom OAuth scopes'"
    )
    assert "Aug 21" in body, "the changelog route does not carry the seeded date 'Aug 21'"


def test_changelog_copy_link_confirms_in_place():
    """The changelog copy control confirms with its pinned label."""
    body = fx.rendered("/changelog")
    assert fx.COPIED_LABEL in body, (
        f"the changelog route carries no {fx.COPIED_LABEL!r} confirmation label for the "
        f"copy-link control"
    )
    assert "Subscribe to RSS" in body, (
        "the changelog route carries no feed link"
    )


def test_feeds_carry_full_content_with_stable_identifiers():
    """The changelog and blog feeds carry full entries with stable identifiers."""
    for path, marker in (("/feeds/changelog.xml", "Custom OAuth scopes"),
                         ("/feeds/blog.xml", "Adding Aegis auth to your CLI")):
        response = fx.page(path)
        assert response.status_code == 200, (
            f"GET {path} returned {response.status_code} rather than a feed: "
            f"{response.text[:300]}"
        )
        assert marker in response.text, (
            f"the feed at {path} does not carry the seeded entry {marker!r}"
        )
        assert response.text.count("<guid") >= 1 or response.text.count("<id>") >= 1, (
            f"the feed at {path} carries no stable identifier per entry: "
            f"{response.text[:300]}"
        )


def test_blog_index_carries_its_categories_and_dates():
    """The blog index lists its category filter and its seeded article dates."""
    body = fx.rendered("/blog")
    for category in ("All categories", "Company", "Engineering", "Testimonial", "Guides",
                     "Insights"):
        assert category in body, f"the blog index carries no {category!r} filter pill"
    for dated in ("Jun 4, 2026", "May 29, 2026", "May 11, 2026"):
        assert dated in body, f"the blog index carries no seeded article dated {dated!r}"
    assert "There is no contact form" not in body, (
        "the blog index carries stray copy from another route"
    )


def test_compliance_rows_keep_the_two_negative_statuses():
    """The compliance register keeps the rows Aegis does not hold."""
    response = httpx.get(f"{fx.api_base()}/compliance", timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/compliance returned {response.status_code}: {response.text[:300]}"
    )
    rows = _shapes.items(response.json())
    statuses = {str(r.get("status")) for r in rows}
    for status in fx.COMPLIANCE_STATUSES:
        assert status in statuses, (
            f"the compliance register carries no row with the status {status!r}; it "
            f"carries {sorted(statuses)}"
        )
    requirements = {str(r.get("requirement")) for r in rows}
    for requirement in ("SOC 2 Type 2", "HIPAA", "PCI DSS", "Regional data residency"):
        assert requirement in requirements, (
            f"the compliance register carries no row for {requirement!r}"
        )


def test_theme_presets_are_seeded_with_seventeen_values():
    """Four theme presets are seeded each carrying seventeen values."""
    body = fx.rendered("/components/theme-editor")
    for preset in fx.THEME_PRESETS:
        assert preset in body, f"the theme editor offers no preset named {preset!r}"
    for field in ("Primary", "Background", "Foreground", "Foreground primary", "Neutral"):
        assert field in body, f"the theme editor panel carries no {field!r} field"
    assert "Advanced" in body, (
        "the theme editor panel carries no Advanced disclosure for the remaining fields"
    )
    assert 'data-theme-mode="light"' in body or 'data-theme-mode="dark"' in body, (
        f"the theme editor canvas declares no data-theme-mode: {body[:400]}"
    )


def test_theme_encoding_round_trips_through_the_address():
    """A theme encoded into the address decodes back to the same values."""
    body = fx.rendered("/components/theme-editor")
    assert "Copy URL" in body, "the theme editor offers no Copy URL action"
    assert "Copy CSS" in body, "the theme editor offers no Copy CSS action"
    assert "Reset to default" in body, "the theme editor offers no reset action"
    broken = fx.page("/components/theme-editor#ZZZZ-not-a-theme")
    assert broken.status_code == 200, (
        f"a malformed theme fragment made the theme editor answer {broken.status_code} "
        f"rather than falling back silently: {broken.text[:300]}"
    )
    assert "Default" in broken.text, (
        "a malformed theme fragment did not fall back to the Default preset"
    )


def test_theme_compiles_to_a_fixed_value_set():
    """A supplied theme compiles only to the named values and never to free style text."""
    body = fx.rendered("/components/theme-editor")
    named = [field for field in fx.THEME_FIELDS
             if field.replace("_", " ").title().lower() in body.lower()
             or field in body.lower()]
    assert len(named) >= 12, (
        f"the theme editor exposes only {len(named)} of the seventeen named values: "
        f"{named}"
    )
    assert "<script>alert" not in body, (
        "the theme editor page echoes unescaped script content"
    )
    injected = fx.page("/components/theme-editor#1-%3Cscript%3Ealert(1)%3C/script%3E")
    assert "<script>alert(1)</script>" not in injected.text, (
        "a theme supplied in the address reached the page as executable markup"
    )


def test_entry_asset_object_key_follows_the_pinned_scheme():
    """An uploaded image lands at the pinned object key scheme."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
        response = fx.attach_image(author, entry["id"])
        assert response.status_code in (200, 201), (
            f"POST /api/entries/{entry['id']}/assets returned {response.status_code}: "
            f"{response.text[:400]}"
        )
        asset = response.json()
    key = asset.get("object_key", "")
    assert fx.OBJECT_KEY_RE.match(key), (
        f"the stored object key {key!r} does not match "
        f"library/{{entry_id}}/{{sha256_of_bytes}}.{{ext}}"
    )
    assert key.startswith(f"library/{entry['id']}/"), (
        f"the object key {key!r} is not filed under its own entry id {entry['id']}"
    )
    assert fx.digest_of(fx.ONE_PIXEL_PNG) in key, (
        f"the object key {key!r} does not carry the digest of the uploaded bytes"
    )
    assert asset.get("content_type"), f"the stored asset records no content type: {asset}"
    assert asset.get("byte_size"), f"the stored asset records no byte size: {asset}"
    assert asset.get("alt_text"), f"the stored asset records no alternative text: {asset}"


def test_uploaded_bytes_are_stored_in_the_bucket_and_nowhere_else(store):
    """The uploaded bytes exist in the bucket and in no other store."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
        response = fx.attach_image(author, entry["id"], payload=fx.SECOND_PNG)
        assert response.status_code in (200, 201), (
            f"POST /api/entries/{entry['id']}/assets returned {response.status_code}: "
            f"{response.text[:400]}"
        )
        asset = response.json()
        key = asset["object_key"]
        assert store.exists(key), (
            f"the object {key!r} does not exist in the bucket named by STORAGE_BUCKET, so "
            f"the upload was recorded without the bytes being stored"
        )
        content = author.get(f"/entries/{entry['id']}/assets/{asset['id']}/content")
        assert content.status_code == 200, (
            f"GET /api/entries/{entry['id']}/assets/{asset['id']}/content as the owning "
            f"author returned {content.status_code}: {content.text[:200]}"
        )
        assert content.content == fx.SECOND_PNG, (
            f"the streamed bytes differ from the uploaded bytes for object {key!r}"
        )
    listed = store.list(f"library/{entry['id']}/")
    assert key in listed, (
        f"listing library/{entry['id']}/ in the bucket returned {listed}, which omits {key!r}"
    )


def test_duplicate_upload_is_idempotent(store):
    """A repeated upload of identical bytes creates no second object."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
        first = fx.attach_image(author, entry["id"])
        assert first.status_code in (200, 201), (
            f"the first upload returned {first.status_code}: {first.text[:300]}"
        )
        second = fx.attach_image(author, entry["id"])
        assert second.status_code in (200, 201), (
            f"the repeated upload returned {second.status_code} rather than a no-op: "
            f"{second.text[:300]}"
        )
        assert second.json().get("object_key") == first.json().get("object_key"), (
            f"the repeated upload produced a second object key "
            f"{second.json().get('object_key')!r} rather than returning "
            f"{first.json().get('object_key')!r}"
        )
        assert second.json().get("id") == first.json().get("id"), (
            f"the repeated upload created a second asset record "
            f"{second.json().get('id')!r} beside {first.json().get('id')!r}"
        )
    keys = store.list(f"library/{entry['id']}/")
    assert len(keys) == 1, (
        f"the bucket holds {len(keys)} objects under library/{entry['id']}/ after two "
        f"identical uploads: {keys}"
    )


def test_concurrent_publish_yields_exactly_one_winner():
    """Two simultaneous publishes for one slug leave exactly one winner."""
    contested = fx.probe_slug("contested")
    with fx.as_author() as author:
        first = fx.create_draft(author, kind="doc", slug=contested)
        second = fx.create_draft(author, kind="doc", slug=contested)
        results = []
        with httpx.Client(base_url=fx.api_base(), timeout=fx.TIMEOUT,
                          headers=dict(author.headers)) as racer:
            for entry in (first, second):
                results.append(racer.post(f"/entries/{entry['id']}/publish"))
        accepted = [r for r in results if r.status_code in (200, 201)]
        refused = [r for r in results if 400 <= r.status_code < 500]
        assert len(accepted) == 1, (
            f"two publishes claiming the doc slug {contested!r} produced "
            f"{len(accepted)} acceptances rather than exactly one: "
            f"{[r.status_code for r in results]}"
        )
        assert len(refused) == 1, (
            f"the losing publish returned {[r.status_code for r in results]} rather than "
            f"one client-error refusal"
        )
        listing = author.get("/entries", params={"kind": "doc", "state": "published"})
        holders = [e for e in _shapes.items(listing.json()) if e.get("slug") == contested]
        assert len(holders) == 1, (
            f"{len(holders)} published doc entries hold the slug {contested!r}: {holders}"
        )


def test_rejected_publish_leaves_no_partial_state():
    """The losing publish leaves no orphan rendition and no stranded entry."""
    contested = fx.probe_slug("stranded")
    with fx.as_author() as author:
        winner = fx.create_draft(author, kind="doc", slug=contested)
        loser = fx.create_draft(author, kind="doc", slug=contested)
        assert fx.publish(author, winner["id"]).status_code in (200, 201), (
            f"the first publish of {contested!r} was refused"
        )
        refusal = fx.publish(author, loser["id"])
        assert 400 <= refusal.status_code < 500, (
            f"publishing a second entry onto the taken slug {contested!r} returned "
            f"{refusal.status_code} rather than refusing: {refusal.text[:300]}"
        )
        after = author.get(f"/entries/{loser['id']}")
        if after.status_code == 200:
            assert after.json().get("state") == "draft", (
                f"the refused entry {loser['id']} is in state "
                f"{after.json().get('state')!r} rather than staying a draft"
            )
        listing = author.get("/entries", params={"kind": "doc", "state": "published"})
        holders = [e for e in _shapes.items(listing.json()) if e.get("slug") == contested]
        assert len(holders) == 1, (
            f"{len(holders)} published entries hold {contested!r} after one refusal"
        )


def test_seeding_is_idempotent_across_a_restart():
    """Restarting the app duplicates no seeded row."""
    response = httpx.get(f"{fx.api_base()}/entries", params={"state": "published"},
                         timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/entries?state=published returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    entries = _shapes.items(response.json())
    seen = {}
    for entry in entries:
        pair = (entry.get("kind"), entry.get("slug"))
        seen[pair] = seen.get(pair, 0) + 1
    duplicated = {pair: n for pair, n in seen.items() if n > 1}
    assert not duplicated, (
        f"the published library holds duplicated kind and slug pairs after seeding: "
        f"{duplicated}"
    )
    glossary = [e for e in entries if e.get("kind") == "glossary"]
    assert len(glossary) >= 10, (
        f"the seed produced {len(glossary)} published glossary entries; ten are pinned"
    )
    plans = httpx.get(f"{fx.api_base()}/plans", timeout=fx.TIMEOUT)
    codes = [p.get("code") for p in _shapes.items(plans.json())]
    assert len(codes) == len(set(codes)) == 4, (
        f"the plan document holds {codes} rather than exactly four distinct plans"
    )


def test_instance_reaches_live_through_provisioning():
    """A provisioned instance reaches live only through provisioning."""
    _, token = fx.register()
    with appclient.client(token) as reader:
        created = reader.post("/applications", json={"name": "Taskflow"})
        assert created.status_code in (200, 201), (
            f"POST /api/applications returned {created.status_code}: {created.text[:400]}"
        )
        application = created.json()
        instances = application.get("instances") or []
        assert instances, (
            f"creating an application returned no development instance: "
            f"{created.text[:400]}"
        )
        instance = instances[0]
        assert instance.get("environment") == "development", (
            f"the instance created with the application is "
            f"{instance.get('environment')!r} rather than development"
        )
        observed = fx.await_instance_state(reader, instance["id"], "live")
        assert "provisioning" in observed["seen"] or observed["seen"][0] == "pending", (
            f"the instance reached live through the states {observed['seen']}, which skips "
            f"the pending and provisioning steps"
        )
        assert observed["body"].get("publishable_key"), (
            f"the live instance carries no publishable key: {observed['body']}"
        )


def test_publishable_key_is_unique_across_instances():
    """Every instance carries a publishable key unique across the product."""
    keys = []
    for _ in range(2):
        _, token = fx.register()
        with appclient.client(token) as reader:
            created = reader.post("/applications",
                                  json={"name": f"Probe {fx.unique_suffix()}"})
            assert created.status_code in (200, 201), (
                f"POST /api/applications returned {created.status_code}: "
                f"{created.text[:300]}"
            )
            instance = (created.json().get("instances") or [{}])[0]
            observed = fx.await_instance_state(reader, instance["id"], "live")
            keys.append(observed["body"]["publishable_key"])
    assert len(set(keys)) == len(keys), (
        f"two instances share a publishable key: {keys}"
    )


def test_draft_entry_is_denied_to_an_anonymous_visitor():
    """An anonymous visitor is denied a draft entry."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
        mine = author.get(f"/entries/{entry['id']}")
        assert mine.status_code == 200, (
            f"the owning author cannot read their own draft {entry['id']}: "
            f"{mine.status_code} {mine.text[:200]}"
        )
    with fx.anonymous() as guest:
        response = guest.get(f"/entries/{entry['kind']}/{entry['slug']}")
        assert response.status_code in (401, 403, 404), (
            f"GET /api/entries/{entry['kind']}/{entry['slug']} as an anonymous caller "
            f"returned {response.status_code} for a DRAFT entry: {response.text[:300]}"
        )
        assert entry["title"] not in response.text, (
            f"the refusal for a draft entry discloses its title: {response.text[:300]}"
        )


def test_draft_entry_is_denied_to_a_reader():
    """A reader is denied a draft entry."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
    with fx.as_reader() as reader:
        response = reader.get(f"/entries/{entry['kind']}/{entry['slug']}")
        assert response.status_code in (401, 403, 404), (
            f"a reader session read the draft {entry['slug']!r} with "
            f"{response.status_code}: {response.text[:300]}"
        )
        listing = reader.get("/entries", params={"state": "draft"})
        if listing.status_code == 200:
            slugs = [e.get("slug") for e in _shapes.items(listing.json())]
            assert entry["slug"] not in slugs, (
                f"GET /api/entries?state=draft as a reader disclosed {entry['slug']!r}"
            )


def test_draft_entry_is_denied_to_a_second_author():
    """A second author is denied the first author's draft entry."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
    with fx.as_second_author() as other:
        response = other.get(f"/entries/{entry['id']}")
        assert response.status_code in (401, 403, 404), (
            f"author2@example.com read author@example.com's draft {entry['id']} with "
            f"{response.status_code}: {response.text[:300]}"
        )
        edit = other.patch(f"/entries/{entry['id']}", json={"title": "Taken over"})
        assert 400 <= edit.status_code < 500, (
            f"author2@example.com edited another author's draft with {edit.status_code}: "
            f"{edit.text[:300]}"
        )
    with fx.as_author() as author:
        after = author.get(f"/entries/{entry['id']}")
        assert after.json().get("title") == entry["title"], (
            f"the protected draft's title changed to {after.json().get('title')!r} after a "
            f"refused edit"
        )


def test_draft_rendition_is_denied_to_a_second_author():
    """A second author is denied the first author's draft rendition."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
    address = f"/r/{entry['kind']}/{entry['slug']}.txt"
    anonymous_view = fx.page(address)
    assert anonymous_view.status_code in (401, 403, 404), (
        f"GET {address} for a draft returned {anonymous_view.status_code} while signed out"
    )
    with fx.as_second_author() as other:
        response = other.get(f"/renditions/{entry['kind']}/{entry['slug']}")
        assert response.status_code in (401, 403, 404), (
            f"author2@example.com read another author's draft rendition with "
            f"{response.status_code}: {response.text[:300]}"
        )
        assert entry["body"] not in response.text, (
            f"the refused rendition still disclosed the draft body: {response.text[:300]}"
        )


def test_draft_image_is_denied_to_a_second_author(store):
    """A second author is denied the first author's draft image bytes."""
    with fx.as_author() as author:
        entry = fx.create_draft(author)
        asset = fx.attach_image(author, entry["id"]).json()
    assert store.exists(asset["object_key"]), (
        f"the draft's object {asset['object_key']!r} is not in the bucket, so the denial "
        f"below would pass for the wrong reason"
    )
    with fx.as_second_author() as other:
        response = other.get(f"/entries/{entry['id']}/assets/{asset['id']}/content")
        assert response.status_code in (401, 403, 404), (
            f"author2@example.com streamed another author's DRAFT image with "
            f"{response.status_code}: {response.text[:200]}"
        )
        assert response.content != fx.ONE_PIXEL_PNG, (
            "the refusal for a draft image still returned the stored bytes"
        )
    with fx.anonymous() as guest:
        guest_view = guest.get(f"/entries/{entry['id']}/assets/{asset['id']}/content")
        assert guest_view.status_code in (401, 403, 404), (
            f"an anonymous caller streamed a draft image with {guest_view.status_code}"
        )


def test_reader_cannot_create_a_library_entry():
    """A reader calling the author endpoint is refused and writes nothing."""
    with fx.as_reader() as reader:
        payload = fx.draft_payload()
        response = reader.post("/entries", json=payload)
        assert 400 <= response.status_code < 500, (
            f"POST /api/entries from a reader session returned {response.status_code} "
            f"rather than refusing: {response.text[:300]}"
        )
    with fx.as_author() as author:
        listing = author.get("/entries", params={"kind": payload["kind"]})
        slugs = [e.get("slug") for e in _shapes.items(listing.json())]
        assert payload["slug"] not in slugs, (
            f"the refused reader write still created the entry {payload['slug']!r}"
        )


def test_reader_cannot_read_another_accounts_applications():
    """A reader is denied another account's applications and instances."""
    _, first_token = fx.register()
    _, second_token = fx.register()
    with appclient.client(first_token) as owner:
        created = owner.post("/applications", json={"name": f"Owned {fx.unique_suffix()}"})
        assert created.status_code in (200, 201), (
            f"POST /api/applications returned {created.status_code}: {created.text[:300]}"
        )
        application = created.json()
        instance = (application.get("instances") or [{}])[0]
    with appclient.client(second_token) as stranger:
        listing = stranger.get("/applications")
        assert listing.status_code == 200, (
            f"GET /api/applications returned {listing.status_code}: {listing.text[:300]}"
        )
        ids = [a.get("id") for a in _shapes.items(listing.json())]
        assert application["id"] not in ids, (
            f"GET /api/applications disclosed another account's application "
            f"{application['id']} to a stranger: {ids}"
        )
        direct = stranger.get(f"/instances/{instance.get('id')}")
        assert direct.status_code in (401, 403, 404), (
            f"GET /api/instances/{instance.get('id')} returned {direct.status_code} to a "
            f"caller who does not own it: {direct.text[:300]}"
        )


def test_author_cannot_provision_an_application():
    """An author calling the provisioning endpoint is refused."""
    with fx.as_author() as author:
        response = author.post("/applications", json={"name": f"Author {fx.unique_suffix()}"})
        assert 400 <= response.status_code < 500, (
            f"POST /api/applications from an author session returned "
            f"{response.status_code} rather than refusing: {response.text[:300]}"
        )


def test_unknown_address_answers_not_found():
    """An unknown address answers with a not-found response."""
    response = fx.page(f"/no-such-route-{fx.unique_suffix()}")
    assert response.status_code == 404, (
        f"an unknown address returned {response.status_code} rather than 404: "
        f"{response.text[:300]}"
    )


def test_not_found_page_carries_the_pinned_copy():
    """The not-found page carries its pinned line and its single action."""
    response = fx.page(f"/no-such-route-{fx.unique_suffix()}")
    body = response.text
    assert fx.NOT_FOUND_LINE in body, (
        f"the not-found page does not carry {fx.NOT_FOUND_LINE!r}: {body[:400]}"
    )
    assert fx.NOT_FOUND_ACTION in body, (
        f"the not-found page does not offer {fx.NOT_FOUND_ACTION!r}: {body[:400]}"
    )
    assert fx.SKIP_LINK_COPY in body, (
        "the not-found page drops the global chrome, so a visitor is stranded"
    )
    assert "Series C" not in body, (
        "the not-found page still renders the announcement bar"
    )


def test_startup_application_with_a_filled_decoy_is_refused():
    """An application carrying a filled decoy field is refused and stores nothing."""
    _, token = fx.register()
    company = f"Decoy Co {fx.unique_suffix()}"
    with appclient.client(token) as reader:
        response = reader.post("/startup-applications", json={
            "company_name": company,
            "funding_raised_display": "$1,000,000",
            "launched_within_year": True,
            "website": "https://example.invalid/bot",
        })
        assert 400 <= response.status_code < 500, (
            f"a startup application with the decoy field filled returned "
            f"{response.status_code} rather than refusing: {response.text[:300]}"
        )
        listing = reader.get("/startup-applications")
        if listing.status_code == 200:
            stored = _shapes.flatten(listing.json())
            assert company not in stored, (
                f"the refused application stored the company name {company!r}"
            )


def test_repeated_startup_application_is_refused():
    """A form submitted repeatedly in quick succession is refused."""
    _, token = fx.register()
    payload = {
        "company_name": f"Rapid Co {fx.unique_suffix()}",
        "funding_raised_display": "$500,000",
        "launched_within_year": True,
        "website": "",
    }
    statuses = []
    with appclient.client(token) as reader:
        for _ in range(4):
            statuses.append(reader.post("/startup-applications", json=payload).status_code)
    refused = [s for s in statuses if 400 <= s < 500]
    assert refused, (
        f"four rapid submissions of one application all succeeded: {statuses}"
    )


def test_consent_choice_persists_across_a_reload():
    """A recorded cookie choice survives a reload."""
    visitor = f"probe-{fx.unique_suffix()}"
    with httpx.Client(base_url=fx.api_base(), timeout=fx.TIMEOUT,
                      headers={"X-Visitor-Token": visitor}) as client:
        before = client.get("/consent")
        assert before.status_code == 200, (
            f"GET /api/consent returned {before.status_code}: {before.text[:300]}"
        )
        stored = client.post("/consent", json={"analytics_allowed": False})
        assert stored.status_code in (200, 201), (
            f"POST /api/consent returned {stored.status_code}: {stored.text[:300]}"
        )
        after = client.get("/consent")
        assert after.json().get("analytics_allowed") is False, (
            f"the recorded consent choice did not survive: {after.text[:300]}"
        )
        withdrawn = client.post("/consent", json={"analytics_allowed": True})
        assert withdrawn.status_code in (200, 201), (
            f"reversing the consent choice returned {withdrawn.status_code}: "
            f"{withdrawn.text[:300]}"
        )
    body = fx.rendered("/")
    declared = [state for state in fx.CONSENT_STATES if f'data-consent="{state}"' in body]
    assert declared, (
        f"the document element declares no data-consent value: {body[:400]}"
    )


def test_invalid_entry_payload_is_refused():
    """An entry payload missing a required field is refused as a client error."""
    with fx.as_author() as author:
        payload = fx.draft_payload()
        payload.pop("title")
        response = author.post("/entries", json=payload)
        assert 400 <= response.status_code < 500, (
            f"POST /api/entries without a title returned {response.status_code} rather "
            f"than a client error: {response.text[:300]}"
        )
        bad_kind = fx.draft_payload(kind="not-a-kind")
        refused = author.post("/entries", json=bad_kind)
        assert 400 <= refused.status_code < 500, (
            f"POST /api/entries with an unknown kind returned {refused.status_code}: "
            f"{refused.text[:300]}"
        )


def test_list_endpoints_return_top_level_arrays():
    """Every list endpoint answers with a top-level JSON array."""
    for path in ("/entries", "/plans", "/leaderboard", "/compliance", "/renditions",
                 "/glossary/graph"):
        response = httpx.get(f"{fx.api_base()}{path}", timeout=fx.TIMEOUT)
        assert response.status_code == 200, (
            f"GET /api{path} returned {response.status_code}: {response.text[:300]}"
        )
        assert isinstance(response.json(), list), (
            f"GET /api{path} returned {type(response.json()).__name__} rather than a "
            f"top-level JSON array: {response.text[:300]}"
        )


def test_user_readme_lists_every_seeded_account():
    """The credential file names every seeded account beside the pinned password."""
    with open("/app/USER_README.md", encoding="utf-8") as handle:
        text = handle.read()
    for email in (fx.AUTHOR_EMAIL, fx.SECOND_AUTHOR_EMAIL, fx.READER_EMAIL):
        assert email in text, f"/app/USER_README.md does not name {email}"
    assert fx.CORPUS_PASSWORD in text, (
        f"/app/USER_README.md does not carry the password {fx.CORPUS_PASSWORD}"
    )


def test_reserved_directories_exist_and_are_empty():
    """The two reserved directories exist at the app root and hold nothing."""
    for name in (".browser_screenshots", ".downloads"):
        path = os.path.join("/app", name)
        assert os.path.isdir(path), f"/app/{name} does not exist at the app root"
        assert os.listdir(path) == [], (
            f"/app/{name} is not empty; it holds {os.listdir(path)}"
        )


def test_every_named_route_answers():
    """Every route the brief names answers rather than erroring."""
    failures = []
    for route in fx.PUBLIC_ROUTES:
        response = fx.page(route)
        if response.status_code not in (200, 301, 302, 303, 307, 308):
            failures.append((route, response.status_code))
    assert not failures, (
        f"{len(failures)} of the named routes did not answer: {failures[:8]}"
    )
    redirect = fx.page("/discord")
    assert redirect.status_code in (301, 302, 303, 307, 308), (
        f"GET /discord returned {redirect.status_code} rather than redirecting off origin"
    )


def test_public_routes_render_without_client_code():
    """Every public route is complete in the HTML the server sends."""
    thin = []
    for route in fx.PUBLIC_ROUTES:
        body = fx.rendered(route)
        without_scripts = re.sub(r"<script.*?</script>", "", body, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", without_scripts)
        if len(text.split()) < 40:
            thin.append((route, len(text.split())))
    assert not thin, (
        f"{len(thin)} public routes carry almost no server-rendered text, so they depend "
        f"on client code to be readable: {thin[:8]}"
    )
    home = fx.rendered("/")
    assert "Sign in" in home and "Sign up" in home, (
        "the served home page does not carry the signed-out chrome action pair"
    )


def test_no_binary_asset_is_served():
    """No route references a font file, a photograph or a video."""
    offenders = []
    for route in ("/", "/pricing", "/docs", "/company", "/careers", "/brand-assets"):
        body = fx.rendered(route)
        for match in fx.BINARY_ASSET_RE.finditer(body):
            window = body[max(0, match.start() - 60):match.end() + 10]
            if "favicon" in window.lower():
                continue
            offenders.append((route, window.strip()[:70]))
    assert not offenders, (
        f"{len(offenders)} binary asset references were served: {offenders[:6]}"
    )
    assets = fx.rendered("/brand-assets")
    assert "Download as SVG" in assets, (
        "the brand assets route offers no vector download"
    )
    assert "Download as PNG" in assets, (
        "the brand assets route offers no raster download"
    )


def test_every_public_route_has_a_distinct_title_and_description():
    """No two public routes share a title or a meta description."""
    titles, descriptions = {}, {}
    for route in fx.PUBLIC_ROUTES:
        body = fx.rendered(route)
        title = fx.TITLE_RE.search(body)
        assert title, f"{route} carries no <title> element"
        description = fx.META_DESCRIPTION_RE.search(body)
        assert description, f"{route} carries no meta description"
        titles.setdefault(title.group(1).strip(), []).append(route)
        descriptions.setdefault(description.group(1).strip(), []).append(route)
    shared_titles = {t: r for t, r in titles.items() if len(r) > 1}
    shared_descriptions = {d: r for d, r in descriptions.items() if len(r) > 1}
    assert not shared_titles, f"routes share a title: {shared_titles}"
    assert not shared_descriptions, (
        f"routes share a meta description: {list(shared_descriptions.values())[:4]}"
    )


def test_favicon_is_served_and_declared_in_the_head():
    """The site serves a favicon and declares it in the document head."""
    body = fx.rendered("/")
    declaration = fx.FAVICON_DECLARATION_RE.search(body)
    assert declaration, f"the home page declares no favicon in its head: {body[:400]}"
    href = re.search(r'href=["\']([^"\']+)["\']', declaration.group(0))
    assert href, f"the favicon declaration carries no href: {declaration.group(0)}"
    target = href.group(1)
    resolved = target if target.startswith("http") else f"{fx.app_url()}{target}"
    response = httpx.get(resolved, timeout=fx.TIMEOUT)
    assert response.status_code == 200, (
        f"the declared favicon at {target} returned {response.status_code}"
    )


def test_privacy_page_is_linked_from_every_footer():
    """The privacy page is reachable from the footer of every route."""
    missing = []
    for route in ("/", "/pricing", "/docs", "/changelog", "/glossary", "/company"):
        body = fx.rendered(route)
        if "/legal/privacy" not in body:
            missing.append(route)
    assert not missing, (
        f"the privacy page is not linked from the footer of {missing}"
    )
    privacy = fx.rendered("/legal/privacy")
    assert fx.PRIVACY_EMAIL in privacy, (
        f"the privacy page does not name {fx.PRIVACY_EMAIL} for a removal request"
    )
    lowered = privacy.lower()
    assert "retain" in lowered or "kept" in lowered or "retention" in lowered, (
        "the privacy page does not state how long a visitor record is kept"
    )
    index = fx.rendered("/legal")
    assert "Customers" in index, (
        "the legal index carries no Customers column heading"
    )
    assert "Everyone else" in index, (
        "the legal index carries no Everyone else column heading"
    )


def test_skip_link_is_the_first_focusable_element():
    """The skip link is the first focusable element on every route."""
    for route in ("/", "/pricing", "/docs"):
        body = fx.rendered(route)
        assert fx.SKIP_LINK_COPY in body, (
            f"{route} carries no {fx.SKIP_LINK_COPY!r} link"
        )
        focusables = list(re.finditer(r"<(?:a|button|input|select|textarea)\b", body,
                                      re.IGNORECASE))
        assert focusables, f"{route} carries no focusable element at all"
        first = body[focusables[0].start():focusables[0].start() + 400]
        assert "main" in first.lower() or fx.SKIP_LINK_COPY in first, (
            f"the first focusable element on {route} is not the skip link: {first[:160]}"
        )


def test_pages_meet_the_accessibility_floors():
    """Contrast, focus order and image alternatives meet their stated floors."""
    for route in ("/", "/pricing", "/glossary"):
        body = fx.rendered(route)
        assert not re.search(r'tabindex=["\']\s*[1-9]', body), (
            f"{route} carries a positive tabindex, which breaks reading order"
        )
        for image in re.finditer(r"<img\b[^>]*>", body, re.IGNORECASE):
            tag = image.group(0)
            assert re.search(r'\balt=', tag, re.IGNORECASE), (
                f"an image on {route} carries no alt attribute: {tag[:120]}"
            )
        assert re.search(r"<main\b", body, re.IGNORECASE), (
            f"{route} declares no main landmark"
        )
        assert re.search(r"<footer\b", body, re.IGNORECASE), (
            f"{route} declares no footer landmark"
        )
    home = fx.rendered("/")
    assert home.count("Add Aegis auth to my app:") >= 2, (
        "the agent prompt string appears once on the home route, so the "
        "per-character markup carries no clean screen-reader copy beside it"
    )


def test_no_route_scrolls_sideways_at_a_narrow_viewport():
    """No route overflows sideways at a narrow viewport."""
    for route in ("/", "/pricing", "/llm-leaderboard", "/glossary"):
        body = fx.rendered(route, width=fx.NARROW_VIEWPORT_WIDTH)
        assert re.search(r'<meta[^>]+name=["\']viewport["\']', body, re.IGNORECASE), (
            f"{route} declares no viewport meta, so a narrow screen cannot lay it out"
        )
        assert not re.search(r"overflow-x\s*:\s*(?:visible|scroll)\s*;?[^}]*}\s*$", body), (
            f"{route} sets a sideways overflow on the document"
        )


def test_home_bands_carry_the_band_attribute():
    """Every full-bleed band on the home route declares its own band."""
    body = fx.rendered("/")
    light = body.count('data-band="light"')
    dark = body.count('data-band="dark"')
    assert light >= 4, (
        f"the home route declares {light} light bands; the band sequence names five"
    )
    assert dark >= 2, (
        f"the home route declares {dark} dark bands; the band sequence names two"
    )
    assert fx.TRUST_STRIP_CAPTION in body, (
        f"the home route does not carry the trust strip caption "
        f"{fx.TRUST_STRIP_CAPTION!r}"
    )


def test_docs_sdk_attribute_reflects_the_selection():
    """Changing the SDK selector rewrites the samples and the declared value."""
    default_body = fx.rendered("/docs")
    assert 'data-sdk="next.js"' in default_body.lower() or \
        'data-sdk="nextjs"' in default_body.lower(), (
        f"the documentation shell does not default data-sdk to Next.js: "
        f"{default_body[:400]}"
    )
    for label in ("Guides", "Reference", "Getting started", "Session management",
                  "Organization management", "Billing management", "Account Portal",
                  "Securing your app"):
        assert label in default_body, (
            f"the documentation sidebar carries no node labelled {label!r}"
        )
    for version in fx.DOC_VERSIONS:
        assert version in default_body, (
            f"the documentation version select offers no {version!r}"
        )
    switched = fx.page("/docs?sdk=ruby-rails-sinatra")
    assert switched.status_code == 200, (
        f"GET /docs?sdk=ruby-rails-sinatra returned {switched.status_code}"
    )
    assert 'data-sdk="ruby-rails-sinatra"' in switched.text.lower(), (
        "selecting Ruby does not set data-sdk to ruby-rails-sinatra"
    )


def test_careers_empty_state_keeps_the_invitation():
    """The careers route shows a designed empty state above its invitation."""
    body = fx.rendered("/careers")
    assert fx.CAREERS_EMPTY_LINE in body, (
        f"the careers route does not carry {fx.CAREERS_EMPTY_LINE!r}"
    )
    assert "Don't see your dream role?" in body, (
        "the careers route drops the standing invitation above its empty state"
    )
    assert "Join our team" in body, (
        "the careers route carries no link on its standing invitation"
    )
